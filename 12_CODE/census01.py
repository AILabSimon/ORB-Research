#!/usr/bin/env python3
"""CENSUS-01 — behaviour-only census of the Max ORB event.
Pre-registered in 07_BEHAVIOURAL_CENSUS/CENSUS_SPECIFICATION.md. No trades, no stops, no costs.
Deterministic. Read-only on the shared Dukascopy store."""
import os, sys, json, hashlib
import numpy as np, pandas as pd

SH   = os.path.expanduser("~/mnt/Dukascopy")
PROJ = os.path.expanduser("~/mnt/ORB Reserach Sub 2.0")
OUT  = os.path.join(PROJ, "07_BEHAVIOURAL_CENSUS", "RESULTS")
PROV = os.path.join(PROJ, "06_DATA", "PROVENANCE")
HORIZONS = [5, 15, 30, 60, 90, 120, 180]

def sha256(path, cap=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()

def load(fname, tz):
    p = os.path.join(SH, fname)
    df = pd.read_csv(p, usecols=["timestamp", "open", "high", "low", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_convert(tz)
    bad = ((df.high < df[["open", "close"]].max(axis=1)) |
           (df.low  > df[["open", "close"]].min(axis=1)) |
           (df.high < df.low))
    n_bad = int(bad.sum())
    df = df[~bad]
    df["m"] = df.timestamp.dt.hour * 60 + df.timestamp.dt.minute
    df["d"] = df.timestamp.dt.normalize()
    df = df[(df.timestamp.dt.dayofweek < 5) & (df.m >= 540) & (df.m < 960)]
    return df.reset_index(drop=True), n_bad, p

def run(inst, fname, tz, r_start, r_end, tag):
    df, n_bad, path = load(fname, tz)
    rows, excl_incomplete = [], 0
    prev_close = {}
    last_close_by_day = df.groupby("d")["close"].last()
    days = sorted(df.d.unique())
    prev_map = {d: last_close_by_day.get(days[i-1], np.nan) for i, d in enumerate(days) if i > 0}

    nbars = (r_end - r_start)
    for d, g in df.groupby("d", sort=True):
        m = g.m.values; hi = g.high.values; lo = g.low.values; cl = g.close.values; op = g.open.values
        rmask = (m >= r_start) & (m < r_end)
        if rmask.sum() < nbars:
            excl_incomplete += 1
            continue
        orb_h = hi[rmask].max(); orb_l = lo[rmask].min()
        orb_mid = (orb_h + orb_l) / 2.0; width = orb_h - orb_l
        if width <= 0:
            excl_incomplete += 1; continue
        orb_open = op[rmask][0]; orb_close = cl[rmask][-1]
        body = abs(orb_close - orb_open)

        post = m >= r_end
        mp = m[post]; hp = hi[post]; lp = lo[post]; cp = cl[post]; opn = op[post]
        row = dict(date=str(pd.Timestamp(d).date()), instrument=inst, tag=tag,
                   orb_high=orb_h, orb_low=orb_l, orb_mid=orb_mid, orb_width=width,
                   orb_dir=int(np.sign(orb_close - orb_open)),
                   orb_body_ratio=body / width,
                   gap=orb_open - prev_map.get(d, np.nan),
                   session_bars=int(len(g)), post_bars=int(post.sum()),
                   n_missing_post=int((960 - r_end) - post.sum()))
        # first 1m touches of each edge (post-range)
        ta = np.where(hp > orb_h)[0]; tb = np.where(lp < orb_l)[0]
        row["first_touch_up_min"]   = int(mp[ta[0]] - r_end) if len(ta) else -1
        row["first_touch_down_min"] = int(mp[tb[0]] - r_end) if len(tb) else -1
        row["both_edges_touched"]   = int(len(ta) > 0 and len(tb) > 0)

        # 15-minute buckets aligned to range end
        b = (mp - r_end) // 15
        nb = int(b.max()) + 1 if len(b) else 0
        sig_k = -1; sig_dir = 0
        for k in range(nb):
            sel = b == k
            if not sel.any(): continue
            c = cp[sel][-1]
            if c > orb_h: sig_k, sig_dir = k, 1; break
            if c < orb_l: sig_k, sig_dir = k, -1; break
        row["signal"] = int(sig_k >= 0); row["signal_bar"] = sig_k + 1; row["dir"] = sig_dir
        if sig_k < 0:
            rows.append(row); continue

        sel = b == sig_k
        entry = cp[sel][-1]; sb_hi = hp[sel].max(); sb_lo = lp[sel].min(); sb_op = opn[sel][0]
        row["entry"] = entry
        row["signal_time_min"] = int((sig_k + 1) * 15)
        row["sig_body_ratio"] = abs(entry - sb_op) / max(sb_hi - sb_lo, 1e-9)
        row["sig_close_pos"]  = (entry - sb_lo) / max(sb_hi - sb_lo, 1e-9)
        row["other_edge_touched_before_signal"] = int(
            (len(tb) > 0 and mp[tb[0]] < r_end + (sig_k + 1) * 15) if sig_dir == 1
            else (len(ta) > 0 and mp[ta[0]] < r_end + (sig_k + 1) * 15))

        edge = orb_h if sig_dir == 1 else orb_l
        R = abs(entry - edge)
        row["R_pts"] = R; row["R_over_width"] = R / width
        row["dist_mid_R"] = abs(entry - orb_mid) / R if R > 0 else np.nan
        row["dist_opp_R"] = abs(entry - (orb_l if sig_dir == 1 else orb_h)) / R if R > 0 else np.nan

        # path: strictly after the signal bar closes (AD-03)
        pstart = r_end + (sig_k + 1) * 15
        pm = mp[mp >= pstart] - pstart
        ph = hp[mp >= pstart]; pl = lp[mp >= pstart]; pc = cp[mp >= pstart]
        pb = b[mp >= pstart]
        row["path_bars"] = int(len(pm))
        if len(pm) == 0 or R <= 0:
            rows.append(row); continue

        fav = (ph - entry) if sig_dir == 1 else (entry - pl)
        adv = (entry - pl) if sig_dir == 1 else (ph - entry)

        def first(cond):
            w = np.where(cond)[0]
            return int(pm[w[0]]) if len(w) else -1

        # levels (behind the entry, i.e. adverse side for a continuation)
        ret_touch = first(pl <= orb_h) if sig_dir == 1 else first(ph >= orb_l)
        mid_touch = first(pl <= orb_mid) if sig_dir == 1 else first(ph >= orb_mid)
        opp_touch = first(pl <= orb_l) if sig_dir == 1 else first(ph >= orb_h)
        # 15m close back inside
        rc = -1
        for k in sorted(set(pb.tolist())):
            s = pb == k
            c = pc[s][-1]
            if orb_l <= c <= orb_h: rc = int(pm[s][-1]); break
        row["ret_inside_touch_min"] = ret_touch
        row["ret_inside_close_min"] = rc
        row["mid_touch_min"] = mid_touch
        row["opp_edge_touch_min"] = opp_touch

        for mult in (1, 2, 3):
            row[f"t_{mult}R_min"] = first(fav >= mult * R)
        for H in HORIZONS + [10**9]:
            hh = "EOD" if H > 10**8 else str(H)
            w = pm < H
            if not w.any():
                row[f"mfe_R_{hh}"] = np.nan; row[f"mae_R_{hh}"] = np.nan; row[f"net_R_{hh}"] = np.nan
                continue
            row[f"mfe_R_{hh}"] = fav[w].max() / R
            row[f"mae_R_{hh}"] = adv[w].max() / R
            row[f"net_R_{hh}"] = ((pc[w][-1] - entry) * sig_dir) / R
        # same-bar ambiguity: does the 2R bar also touch the return-inside level?
        w2 = np.where(fav >= 2 * R)[0]
        if len(w2):
            i = w2[0]
            row["same_bar_ambiguous_2R"] = int((pl[i] <= orb_h) if sig_dir == 1 else (ph[i] >= orb_l))
        else:
            row["same_bar_ambiguous_2R"] = 0
        rows.append(row)

    out = pd.DataFrame(rows)
    # lagged volatility normalisation (no look-ahead)
    out = out.sort_values("date").reset_index(drop=True)
    out["width_med20_lag"] = out["orb_width"].rolling(20, min_periods=10).median().shift(1)
    out["orb_width_rel"] = out["orb_width"] / out["width_med20_lag"]
    os.makedirs(OUT, exist_ok=True); os.makedirs(PROV, exist_ok=True)
    f = os.path.join(OUT, f"CENSUS01_{inst}_{tag}.csv")
    out.to_csv(f, index=False)
    prov = dict(census="CENSUS-01", instrument=inst, tag=tag, source_file=path,
                source_sha256=sha256(path), tz=tz, range_window_min=[r_start, r_end],
                sessions_written=int(len(out)), excluded_incomplete_range=int(excl_incomplete),
                ohlc_violating_bars_dropped=int(n_bad), horizons=HORIZONS,
                script="12_CODE/census01.py", run_utc=str(pd.Timestamp.utcnow()))
    with open(os.path.join(PROV, f"PROVENANCE_CENSUS01_{inst}_{tag}.json"), "w") as fh:
        json.dump(prov, fh, indent=2)
    print(json.dumps({k: v for k, v in prov.items() if k != "source_sha256"}, indent=1))
    print("signal rate:", round(100 * out.signal.mean(), 2), "%  n=", len(out))
    return out

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "main":
        run("NAS100", "NAS100_1m.csv", "America/New_York", 570, 585, "ORB0930")
    elif which == "ctrlA":
        run("NAS100", "NAS100_1m.csv", "America/New_York", 660, 675, "PSEUDO1100")
    elif which == "us500":
        run("US500", "US500_1m.csv", "America/New_York", 570, 585, "ORB0930")
