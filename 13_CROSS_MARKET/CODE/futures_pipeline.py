#!/usr/bin/env python3
"""
futures_pipeline.py — ingest source-native futures data and decide candidate CM-C1.

Two subcommands:

    ingest   Normalise and validate a futures file from any common vendor into the
             shared store's schema, with provenance and SHA256.
    decide   Run the exact CM-C1 construction on that data, with true futures economics
             and the full validation battery, and print the verdict.

WHY THIS EXISTS
---------------
CM-C1 (Nasdaq opening-range retest) is PROVISIONALLY SUPPORTED / DATA-LIMITED. It measures
+0.105R under assumed NQ futures costs and -0.001R on the Dukascopy index-CFD data we hold.
That gap is one missing dataset. This script removes all latency between the data arriving
and the decision being made: nothing needs to be re-derived or re-specified.

The construction below is FROZEN. It is exactly what was pre-registered and tested on the
proxy — same range, same entry, same stop, same exit, same same-bar rule. Do not tune it.
A different result on native data is the answer; a tuned result is not.

USAGE
-----
    pip install pandas pyarrow
    python3 futures_pipeline.py ingest --input NQ_1min.csv --instrument NQ --out-dir <store>
    python3 futures_pipeline.py decide --data <store>/NQ_1m.csv --instrument NQ

Vendor formats auto-detected: Databento (ts_event/open/high/low/close), CME DataMine,
Firstrate Data, Kibot, and generic OHLC CSV. If detection fails the script says which
columns it found and stops — it does not guess.
"""

import argparse, hashlib, json, os, sys
import datetime as dt
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------------------
# FROZEN CM-C1 SPECIFICATION — do not change without a new candidate ID
# ----------------------------------------------------------------------------------------
SPEC = dict(
    session_tz      = "America/New_York",
    range_start_min = 9 * 60 + 30,     # 09:30 cash open
    range_len_min   = 30,              # L = 30
    session_end_min = 16 * 60,
    retest_tol_W    = 0.10,            # entry: return to within 0.10 x W of the broken edge
    stop_frac_W     = 0.50,            # stop at 0.5 x W  =>  R = 0.5 x W
    trail_from_R    = 1.0,             # trail 1R behind the extreme once +1R is reached
    max_hold_min    = 180,
    max_trades_day  = 1,
    same_bar_rule   = "against the trade (conservative)",
)

# Instrument economics. Micro and full contracts are NOT the same in points, because
# commission is a fixed dollar amount divided by a different point value.
INSTRUMENTS = {
    #            $/point  tick  comm/side  spread  entry  exit  stop-extra
    "NQ":  dict(pv=20.0,  tick=0.25, comm=2.50, spr=0.25, es=0.25, xs=0.25, sx=0.25, unit="index points"),
    "MNQ": dict(pv=2.00,  tick=0.25, comm=0.50, spr=0.25, es=0.25, xs=0.25, sx=0.25, unit="index points"),
    "ES":  dict(pv=50.0,  tick=0.25, comm=2.50, spr=0.25, es=0.25, xs=0.25, sx=0.25, unit="index points"),
    "MES": dict(pv=5.00,  tick=0.25, comm=0.50, spr=0.25, es=0.25, xs=0.25, sx=0.25, unit="index points"),
    "GC":  dict(pv=100.0, tick=0.10, comm=2.50, spr=0.10, es=0.10, xs=0.10, sx=0.10, unit="USD/oz"),
    "MGC": dict(pv=10.0,  tick=0.10, comm=0.50, spr=0.10, es=0.10, xs=0.10, sx=0.10, unit="USD/oz"),
}

# The proxy result this run is being compared against (from the cross-market branch).
PROXY_BASELINE = dict(
    net_R=0.1052, ci=(0.060, 0.151), dev=0.035, holdout=0.229,
    n=2578, win_pct=51.2, max_dd=62.1, med_R_pts=25.68, per_year=184,
    source="NAS100 Dukascopy index CFD, NQ futures COST SIZING (assumed, not measured)",
)


def rt_cost_pts(inst, exit_reason):
    """Round-trip cost in instrument points. Each component applied exactly once."""
    i = INSTRUMENTS[inst]
    pts = i["spr"] + i["es"] + i["xs"] + (i["sx"] if exit_reason == "stop" else 0.0)
    return pts + (2 * i["comm"]) / i["pv"]


# ----------------------------------------------------------------------------------------
# INGEST
# ----------------------------------------------------------------------------------------
TS_CANDIDATES = ["ts_event", "timestamp", "datetime", "date_time", "time", "date", "Date",
                 "DateTime", "Timestamp", "ts_recv"]
OHLC_MAP = {"open": ["open", "Open", "o", "px_open"], "high": ["high", "High", "h", "px_high"],
            "low": ["low", "Low", "l", "px_low"], "close": ["close", "Close", "c", "px_close"],
            "volume": ["volume", "Volume", "v", "vol", "size"]}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()


def detect_and_load(path, assume_tz=None):
    if str(path).endswith((".parquet", ".pq")):
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path)
        if len(df.columns) >= 6 and not any(c in df.columns for c in TS_CANDIDATES):
            # headerless vendor dump: date,time,o,h,l,c,v  or  datetime,o,h,l,c,v
            df = pd.read_csv(path, header=None)
            if df.shape[1] == 7:
                df.columns = ["date", "time", "open", "high", "low", "close", "volume"]
                df["timestamp"] = df["date"].astype(str) + " " + df["time"].astype(str)
                df = df.drop(columns=["date", "time"])
            elif df.shape[1] == 6:
                df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
            else:
                sys.exit(f"Unrecognised headerless layout with {df.shape[1]} columns.")

    tscol = next((c for c in TS_CANDIDATES if c in df.columns), None)
    if tscol is None:
        sys.exit(f"No timestamp column found. Columns present: {list(df.columns)}\n"
                 f"Rename the timestamp column to one of: {TS_CANDIDATES}")

    out = pd.DataFrame()
    ts = df[tscol]
    if pd.api.types.is_numeric_dtype(ts):
        unit = "ns" if ts.iloc[0] > 1e17 else ("ms" if ts.iloc[0] > 1e11 else "s")
        out["timestamp"] = pd.to_datetime(ts, unit=unit, utc=True)
        print(f"  timestamp: epoch {unit} -> UTC")
    else:
        parsed = pd.to_datetime(ts, errors="coerce")
        if parsed.dt.tz is None:
            if assume_tz is None:
                sys.exit("Timestamps are naive and no --assume-tz given. Vendor files are "
                         "usually exchange time (America/Chicago) or UTC. Re-run with "
                         "--assume-tz America/Chicago (or UTC). Never guess this.")
            out["timestamp"] = parsed.dt.tz_localize(assume_tz, ambiguous="infer",
                                                     nonexistent="shift_forward").dt.tz_convert("UTC")
            print(f"  timestamp: naive, localised as {assume_tz} -> UTC")
        else:
            out["timestamp"] = parsed.dt.tz_convert("UTC")
            print("  timestamp: tz-aware -> UTC")

    for want, alts in OHLC_MAP.items():
        col = next((c for c in alts if c in df.columns), None)
        if col is None and want != "volume":
            sys.exit(f"Missing required column '{want}'. Columns present: {list(df.columns)}")
        if col is not None:
            out[want] = pd.to_numeric(df[col], errors="coerce")
    if "volume" not in out:
        out["volume"] = np.nan
    return out.dropna(subset=["open", "high", "low", "close"]).sort_values("timestamp")


def validate(df, inst):
    tz = SPEC["session_tz"]
    loc = df["timestamp"].dt.tz_convert(tz)
    m = loc.dt.hour * 60 + loc.dt.minute
    r0, r1 = SPEC["range_start_min"], SPEC["range_start_min"] + SPEC["range_len_min"]
    sel = (m >= r0) & (m < r1) & (loc.dt.dayofweek < 5)
    cnt = df[sel].groupby(loc[sel].dt.date).size()
    bad = ((df.high < df[["open", "close"]].max(axis=1)) |
           (df.low > df[["open", "close"]].min(axis=1)) | (df.high < df.low))
    rep = dict(
        rows=int(len(df)),
        coverage_start_utc=str(df["timestamp"].iloc[0]),
        coverage_end_utc=str(df["timestamp"].iloc[-1]),
        duplicate_timestamps=int(df["timestamp"].duplicated().sum()),
        monotonic=bool(df["timestamp"].is_monotonic_increasing),
        ohlc_violations=int(bad.sum()),
        nonpositive_prices=int((df[["open", "high", "low", "close"]] <= 0).any(axis=1).sum()),
        range_window_days=int(len(cnt)),
        range_windows_complete=int((cnt == SPEC["range_len_min"]).sum()),
        range_complete_pct=round(100 * (cnt == SPEC["range_len_min"]).mean(), 2) if len(cnt) else 0.0,
        years=sorted({d.year for d in cnt.index}) if len(cnt) else [],
    )
    print("\n  VALIDATION")
    for k, v in rep.items():
        print(f"    {k:26s} {v}")
    if rep["range_complete_pct"] < 90:
        print("    ** WARNING: opening-range completeness below 90%. Check the session filter "
              "and whether this file is RTH-only or includes the full 23-hour session.")
    if rep["duplicate_timestamps"]:
        print("    ** WARNING: duplicate timestamps present. Common when a per-contract file has "
              "not been rolled. Dedupe or supply a continuous series.")
    return rep


def cmd_ingest(a):
    print(f"Ingesting {a.input}  (instrument {a.instrument})")
    df = detect_and_load(a.input, a.assume_tz)
    rep = validate(df, a.instrument)
    out_dir = a.out_dir or os.path.dirname(os.path.abspath(a.input))
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{a.instrument}_1m.csv")
    df.to_csv(out, index=False)
    prov = dict(
        schema_version="futures_ingest_provenance_v1", research_instrument=a.instrument,
        market_representation="FUTURES (source-native)", vendor=a.vendor or "unspecified",
        roll_convention=a.roll or "UNSPECIFIED - record this before citing the file",
        source_file=os.path.abspath(a.input), file=out, sha256=sha256(out),
        assumed_tz=a.assume_tz, session_tz=SPEC["session_tz"],
        unit=INSTRUMENTS[a.instrument]["unit"], validation=rep,
        written_by="futures_pipeline.py ingest",
        written_at_utc=dt.datetime.utcnow().isoformat() + "Z",
        note="Source-native futures. May be compared with, but NEVER pooled with, CFD/spot proxy results.",
    )
    with open(out.replace(".csv", ".provenance.json"), "w") as f:
        json.dump(prov, f, indent=2)
    print(f"\n  WROTE {out}\n  sha256 {prov['sha256'][:16]}...")
    if not a.roll:
        print("  ** Record the roll convention before citing this file in any result.")


# ----------------------------------------------------------------------------------------
# DECIDE — the frozen CM-C1 construction
# ----------------------------------------------------------------------------------------
def run_cm_c1(df, stop_frac=None, L=None, delay=0):
    """Returns a trade ledger. Frozen construction; the optional args exist ONLY for the
    parameter-neighbourhood robustness check, never for tuning."""
    stop_frac = SPEC["stop_frac_W"] if stop_frac is None else stop_frac
    L = SPEC["range_len_min"] if L is None else L
    tz, r0 = SPEC["session_tz"], SPEC["range_start_min"]
    r1, send = r0 + L, SPEC["session_end_min"]
    d = df.copy()
    loc = d["timestamp"].dt.tz_convert(tz)
    d["m"] = loc.dt.hour * 60 + loc.dt.minute
    d["day"] = loc.dt.normalize()
    d = d[(loc.dt.dayofweek < 5) & (d.m >= r0) & (d.m < send)]
    tr = []
    for day, g in d.groupby("day", sort=True):
        m, h, l, c = g.m.values, g.high.values, g.low.values, g.close.values
        rm = (m >= r0) & (m < r1)
        if rm.sum() < L:
            continue
        oh, ol = h[rm].max(), l[rm].min()
        W = oh - ol
        if W <= 0:
            continue
        post = m >= r1
        if post.sum() < 60:
            continue
        pm, ph, pl, pc = m[post] - r1, h[post], l[post], c[post]
        b = pm // L
        # 1-3: completed close outside the range
        sk, dr = -1, 0
        for k in range(int(b.max()) + 1):
            s = b == k
            if not s.any():
                continue
            v = pc[s][-1]
            if v > oh: sk, dr = k, 1; break
            if v < ol: sk, dr = k, -1; break
        if sk < 0:
            continue
        edge = oh if dr == 1 else ol
        # 4: first retest to within tol x W of the broken edge
        after = np.where(pm >= (sk + 1) * L)[0]
        tol = SPEC["retest_tol_W"] * W
        rt = [i for i in after if ((pl[i] <= edge + tol) if dr == 1 else (ph[i] >= edge - tol))]
        if not rt:
            continue
        ei = rt[0] + delay
        if ei >= len(pm) - 5:
            continue
        entry = edge
        stop = entry - dr * stop_frac * W
        R = abs(entry - stop)
        if R <= 0:
            continue
        # 5-6: trail from +1R, hard time exit, same-bar resolved against the trade
        t0, ex, exr, be, trail, mfe = pm[ei], None, None, False, stop, 0.0
        for j in range(ei, len(pm)):
            if pm[j] - t0 > SPEC["max_hold_min"]:
                ex, exr = pc[j], "time"; break
            fav = (ph[j] - entry) if dr == 1 else (entry - pl[j])
            mfe = max(mfe, fav)
            hit = (pl[j] <= trail) if dr == 1 else (ph[j] >= trail)
            if hit:
                ex, exr = trail, ("trailstop" if be else "stop"); break
            if fav >= SPEC["trail_from_R"] * R:
                be = True
                nt = (ph[j] - R) if dr == 1 else (pl[j] + R)
                trail = max(trail, nt, entry) if dr == 1 else min(trail, nt, entry)
        if ex is None:
            ex, exr = pc[-1], "eod"
        tr.append(dict(date=str(pd.Timestamp(day).date()), dir=dr, W=W, R_pts=R, entry=entry,
                       exit=ex, exit_reason=exr, gross_R=((ex - entry) * dr) / R, mfe_R=mfe / R,
                       hold=int(pm[min(j, len(pm) - 1)] - t0)))
    return pd.DataFrame(tr)


def summarise(t, inst, label, rng):
    if len(t) < 30:
        print(f"  {label:44s} n={len(t)} — too few to assess"); return None
    cost = np.array([rt_cost_pts(inst, r) for r in t.exit_reason])
    net = t.gross_R.values - cost / t.R_pts.values
    bs = np.array([rng.choice(net, len(net), True).mean() for _ in range(3000)])
    lo, hi = np.percentile(bs, 2.5), np.percentile(bs, 97.5)
    eq = np.cumsum(net)
    dd = float(np.max(np.maximum.accumulate(eq) - eq))
    yrs = t.date.str[:4].astype(int)
    BE = np.abs(net) < 0.05
    print(f"  {label:44s} n={len(t):5d} net={net.mean():+.4f}R CI[{lo:+.4f},{hi:+.4f}] "
          f"win={100*(net>=0.05).mean():4.1f}% DD={dd:5.1f}R")
    return dict(label=label, n=int(len(t)), net=float(net.mean()), lo=float(lo), hi=float(hi),
                win=float(100 * (net >= 0.05).mean()), be=int(BE.sum()), dd=dd,
                med_R=float(t.R_pts.median()), per_year=float(len(t) / yrs.nunique()),
                dev=float(net[yrs <= 2021].mean()) if (yrs <= 2021).any() else None,
                hold=float(net[yrs > 2021].mean()) if (yrs > 2021).any() else None,
                mean_cost_R=float(np.mean(cost / t.R_pts.values)), net_vec=net, yrs=yrs)


def cmd_decide(a):
    rng = np.random.default_rng(2026)
    print(f"Loading {a.data}")
    df = pd.read_csv(a.data)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    print(f"  {len(df):,} bars, {df.timestamp.iloc[0]} -> {df.timestamp.iloc[-1]}")
    print(f"\nCM-C1 frozen spec: {SPEC['range_len_min']}-min range from 09:30 {SPEC['session_tz']}, "
          f"completed close outside, retest within {SPEC['retest_tol_W']}xW, "
          f"stop {SPEC['stop_frac_W']}xW, trail from +{SPEC['trail_from_R']}R, "
          f"{SPEC['max_hold_min']}-min cap, same-bar {SPEC['same_bar_rule']}.")
    i = INSTRUMENTS[a.instrument]
    print(f"\nEconomics {a.instrument}: ${i['pv']:.2f}/pt, tick {i['tick']}, "
          f"commission ${i['comm']:.2f}/side -> round trip "
          f"{rt_cost_pts(a.instrument,'stop'):.3f} pts on a stop exit, "
          f"{rt_cost_pts(a.instrument,'time'):.3f} otherwise.")

    print("\n=== HEADLINE ===")
    base = run_cm_c1(df)
    head = summarise(base, a.instrument, "CM-C1 as frozen", rng)
    if head is None:
        sys.exit("Not enough trades to decide. Check data coverage.")

    print("\n=== TEMPORAL ===")
    print(f"  development <=2021  net={head['dev']:+.4f}R" if head['dev'] is not None else "  development: none")
    print(f"  holdout      >2021  net={head['hold']:+.4f}R" if head['hold'] is not None else "  holdout: none")
    print("  per year:")
    for y in sorted(head["yrs"].unique()):
        s = head["net_vec"][head["yrs"] == y]
        if len(s) >= 25:
            print(f"    {y}  n={len(s):4d}  net={s.mean():+.4f}R")

    print("\n=== PARAMETER NEIGHBOURHOOD (robustness only — not tuning) ===")
    for sf in (0.35, 0.50, 0.65, 0.80, 1.00):
        summarise(run_cm_c1(df, stop_frac=sf), a.instrument, f"stop = {sf:.2f} x W", rng)
    for L in (15, 20, 30, 45):
        summarise(run_cm_c1(df, L=L), a.instrument, f"range length = {L} min", rng)

    print("\n=== EXECUTION DELAY ===")
    for dl in (0, 1, 2):
        summarise(run_cm_c1(df, delay=dl), a.instrument, f"delay {dl} min after trigger", rng)

    print("\n=== COST SENSITIVITY (multiples of the modelled round trip) ===")
    cost = np.array([rt_cost_pts(a.instrument, r) for r in base.exit_reason])
    for k in (1.0, 1.5, 2.0, 3.0):
        n = (base.gross_R.values - k * cost / base.R_pts.values).mean()
        print(f"  {k:.1f}x cost   net={n:+.4f}R")

    print("\n=== VERDICT ===")
    p = PROXY_BASELINE
    print(f"  proxy baseline  net={p['net_R']:+.4f}R CI[{p['ci'][0]:+.3f},{p['ci'][1]:+.3f}] "
          f"n={p['n']} ({p['source']})")
    print(f"  native futures  net={head['net']:+.4f}R CI[{head['lo']:+.4f},{head['hi']:+.4f}] n={head['n']}")
    print(f"  mean cost/R {head['mean_cost_R']:.4f}  median R {head['med_R']:.2f} pts  "
          f"{head['per_year']:.0f} trades/yr  max DD {head['dd']:.1f}R")
    print()
    if head["lo"] > 0 and (head["hold"] or 0) > 0:
        print("  >>> ADVANCE TO VALIDATION. Positive with a CI excluding zero, and holdout positive.")
        print("      Next: cross-instrument (MNQ vs NQ), regime split, and forward/paper stage.")
    elif head["lo"] > 0:
        print("  >>> PROVISIONALLY SUPPORTED. CI excludes zero but holdout is not positive.")
        print("      Do NOT advance on this alone — investigate the temporal split first.")
    else:
        print("  >>> NOT SUPPORTED on source-native data. CI includes zero or is negative.")
        print("      This settles CM-C1. Retire it and close the cross-market branch;")
        print("      do not tune the construction to rescue the result.")
    print("\n  Whatever the verdict: record it, update RESEARCH_STATE and DECISION_LOG, and")
    print("  keep native and proxy results in separate tables. Never pool them.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("ingest", help="normalise + validate a vendor futures file")
    g.add_argument("--input", required=True)
    g.add_argument("--instrument", required=True, choices=sorted(INSTRUMENTS))
    g.add_argument("--out-dir")
    g.add_argument("--assume-tz", help="tz of naive timestamps, e.g. America/Chicago or UTC")
    g.add_argument("--vendor", help="e.g. databento, cme-datamine, firstrate, kibot")
    g.add_argument("--roll", help="roll convention, e.g. 'volume-based, front month, no adjustment'")
    g.set_defaults(func=cmd_ingest)
    d = sub.add_parser("decide", help="run frozen CM-C1 and print the verdict")
    d.add_argument("--data", required=True, help="normalised CSV from ingest")
    d.add_argument("--instrument", required=True, choices=sorted(INSTRUMENTS))
    d.set_defaults(func=cmd_decide)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
