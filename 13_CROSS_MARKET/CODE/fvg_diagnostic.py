#!/usr/bin/env python3
"""
EXTERNAL FVG / FAILED-BREAK DIAGNOSTIC — issue #3, built against RESEARCH_CURRENT v2.3.

Observed hypothesis under test: a break of one ORB boundary may only tap/fill an FVG
sitting just beyond that boundary, after which price reverses through the ORB and
targets the opposite ORB boundary. DIAGNOSTIC ONLY:
  - not wired into Entry-02 as a filter;
  - no FVG size/distance/tolerance is optimised — the gap definition is the SAME
    3-candle causal gap already used for pre-market draws in cw_entry02.build_draws
    (§D.11), just evaluated continuously instead of "previous session only";
  - no trend/bias rule is invented. RESEARCH_CURRENT v2.3 §D.3/§D.14/§I U-24 is explicit
    that CeeWilli's overall-bias primitive has no mechanical definition anywhere in the
    source, and cw_entry02.py computes no such field. There is therefore NO objective
    trend/bias column in this dataset to cross-tab against — see `trend_bias_note()`.
    That is a finding in its own right, not an omission.

Depends on cw_entry02.py for the ORB/break/draw machinery and the same canonical bar
series (mdload -> load_ny). Reuses cw_entry02.run() for the actual Entry-02 population
(wins/losses) and adds an independent, gate-free break scan for the broader "every
eligible ORB day" population the reversal-sequence measurement needs (§ISSUE-3
"PRIMARY COUNT REQUEST" is entry-linked; the reversal-sequence measurement is not).

STATUS: NOT EXECUTED. This module was written in an environment with no access to the
canonical market-data store (see ANALYST_CURRENT.md) and therefore has not been run
against real data, has not passed a single one of its own sanity checks, and has not
been visually validated — which RESEARCH_CURRENT.md's own discipline (§H, "V2 must pass
all of these on a small sample before any historical economics are computed") requires
before any number from it is trusted. Do not quote counts from a run of this file
without first confirming H-style acceptance checks pass on a small sample.
"""
import numpy as np, pandas as pd
import cw_entry02 as CW

R0, R1, SESS_END, DAY_STOP = CW.R0, CW.R1, CW.SESS_END, CW.DAY_STOP

# ------------------------------------------------------------------ causal FVG registry
def build_bars(d, tf):
    """Continuous tf-resampled bars across the WHOLE series (not sliced per trading day),
    so an FVG formed on a previous session and still open remains visible to later days
    [issue #3: 'whether the FVG existed before the ORB completed']. Same bar construction
    as cw_entry02.resample, with `day` carried through for day-boundary lookups.
    CAVEAT (tf=5 only, unresolved pending a run): this resamples continuously from the
    start of the series, whereas cw_entry02.run() resamples per day starting at 09:30.
    The two 5-minute bin grids are not guaranteed to align, so the entry/draw timestamps
    from a cw_entry02 trade may fall mid-bar here. Before trusting any tf=5 touch/order
    result, verify bin alignment on a sample day or rebuild this from cw_entry02.resample
    applied per day and re-concatenated."""
    if tf == 1:
        return d.reset_index(drop=True)
    agg = dict(open=("open", "first"), high=("high", "max"), low=("low", "min"),
               close=("close", "last"), m=("m", "first"), day=("day", "first"))
    return d.set_index("timestamp").resample(f"{tf}min").agg(**agg).dropna().reset_index()

def causal_fvgs(b):
    """Detects the SAME 3-candle gap already used for pre-market draws [D.11]: no new
    definition, no size/tolerance threshold. A gap is only KNOWN once its 3rd
    (confirming) bar has closed — `known_idx` is the causal cutoff for every use below,
    and it is a positional index into `b`, matching every other index used here."""
    H, L = b.high.values, b.low.values
    rows = []
    for i in range(1, len(b) - 1):
        if L[i + 1] > H[i - 1]:
            rows.append(dict(kind="up", lo=H[i - 1], hi=L[i + 1], form_idx=i, known_idx=i + 1))
        if H[i + 1] < L[i - 1]:
            rows.append(dict(kind="down", lo=H[i + 1], hi=L[i - 1], form_idx=i, known_idx=i + 1))
    return pd.DataFrame(rows, columns=["kind", "lo", "hi", "form_idx", "known_idx"])

def already_filled(fvg, upto_idx, H, L):
    """True if price has fully traded through [lo,hi] at any point strictly between the
    gap becoming known and `upto_idx` (inclusive) — such a gap is no longer a live
    external target by decision time and must not be offered as 'present'."""
    lo_idx = fvg.known_idx + 1
    if upto_idx < lo_idx:
        return False
    seg_lo = L[lo_idx:upto_idx + 1].min()
    seg_hi = H[lo_idx:upto_idx + 1].max()
    return seg_lo <= fvg.lo and seg_hi >= fvg.hi

def formation_cohort(fvg, M):
    """[issue #3, descriptive cohort, never a filter] pre-ORB / during-ORB / post-ORB,
    keyed off the minute-of-day at which the gap's 3rd bar closed (`known_idx`)."""
    known_m = M[fvg.known_idx]
    if known_m < R0:
        return "pre_orb"
    if known_m < R1:
        return "during_orb"
    return "post_orb"

# ------------------------------------------------------------------ break scan (gate-free)
def scan_breaks(CB, day_mask, ORH, ORL):
    """First body close beyond ORH and first beyond ORL after the ORB, independent of
    pullback/rejection/the RR gate — mirrors cw_entry02's S1 definition exactly [D.2],
    but is evaluated for 'every eligible ORB day' per issue #3, not just entered trades.
    `day_mask` restricts to this day's bars in [R1, DAY_STOP). Returns {side: idx or None}
    where idx is a positional index into CB."""
    idx = np.where(day_mask)[0]
    C = CB.close.values
    out = {}
    for side, bnd in ((1, ORH), (-1, ORL)):
        hit = None
        for k in idx:
            if (C[k] > bnd) if side == 1 else (C[k] < bnd):
                hit = k
                break
        out[side] = hit
    return out

# ------------------------------------------------------------------ touch / fill classification
def touch_and_fill(CB, zone_lo, zone_hi, start_idx, stop_idx):
    """Scans CB[start_idx:stop_idx] for the first wick interaction with [zone_lo,zone_hi]
    and classifies the resulting fill state [issue #3 field 4]:
      full        — some single bar's [low,high] spans the WHOLE zone in one print;
      partial     — the zone was entered by at least one bar's BODY (open/close), short
                    of a full span;
      wick_only   — the zone was only ever pierced by wicks, never by a body.
    No tolerance/threshold is added; comparisons are exact against the zone bounds."""
    O, H, L, C = CB.open.values, CB.high.values, CB.low.values, CB.close.values
    touch_idx = None
    body_entered = False
    full = False
    for k in range(start_idx, stop_idx):
        wick_overlap = (L[k] <= zone_hi) and (H[k] >= zone_lo)
        if not wick_overlap:
            continue
        if touch_idx is None:
            touch_idx = k
        if L[k] <= zone_lo and H[k] >= zone_hi:
            full = True
        bl, bh = min(O[k], C[k]), max(O[k], C[k])
        if bl <= zone_hi and bh >= zone_lo:
            body_entered = True
        if full:
            break
    if touch_idx is None:
        return dict(touched=False, touch_idx=None, fill="none")
    fill = "full" if full else ("partial" if body_entered else "wick_only")
    return dict(touched=True, touch_idx=touch_idx, fill=fill)

# ------------------------------------------------------------------ reversal sequence
def reversal_outcome(CB, side, ORH, ORL, touch_idx, stop_idx, draw_px=None):
    """From the FVG touch onward, does price return inside the ORB and then reach the
    OPPOSITE boundary, and where does that sit relative to the Entry-02 continuation-side
    draw (only defined when an actual Entry-02 trade exists that day/side)?
    [issue #3 fields 5-7]"""
    H, L, C = CB.high.values, CB.low.values, CB.close.values
    opp = ORL if side == 1 else ORH
    return_idx = opp_idx = draw_idx = None
    for k in range(touch_idx, stop_idx):
        if return_idx is None and (ORL <= C[k] <= ORH):
            return_idx = k
        if opp_idx is None and (L[k] <= opp <= H[k]):
            opp_idx = k
        if draw_px is not None and draw_idx is None:
            hit = (H[k] >= draw_px) if side == 1 else (L[k] <= draw_px)
            if hit:
                draw_idx = k
        if opp_idx is not None and (draw_idx is not None or draw_px is None):
            break
    if opp_idx is not None and (draw_idx is None or opp_idx < draw_idx):
        order = "opposite_first"
    elif draw_idx is not None:
        order = "continuation_first"
    else:
        order = "neither_reached"
    return dict(returned_inside=return_idx is not None, return_idx=return_idx,
                opposite_reached=opp_idx is not None, opposite_idx=opp_idx,
                continuation_reached=(None if draw_px is None else draw_idx is not None),
                continuation_idx=draw_idx, order=order)

# ------------------------------------------------------------------ driver
def diagnose(inst, tf=1, u22="DEEP", be=False, draw_rule="DRAW-NQ", d=None, draws=None):
    """Builds the per-break-event diagnostic table for one (inst, tf, u22, be, draw_rule)
    cell. One row per side that broke on an eligible day, whether or not an Entry-02
    trade resulted. Joins to the matching Entry-02 outcome (win/loss) when one exists."""
    if d is None:
        d = CW.load_ny(inst)
    if draws is None:
        draws = CW.build_draws(d)
    trades, _ = CW.run(inst, tf=tf, u22=u22, be=be, draws=draws, d=d, draw_rule=draw_rule)
    tmap = {(r.date, r.side): r for r in trades.itertuples()} if len(trades) else {}

    CB = build_bars(d, tf)
    M = CB.m.values
    FVG = causal_fvgs(CB)
    Hc, Lc = CB.high.values, CB.low.values

    rows = []
    for day, g in d.groupby("day", sort=True):
        rm = g[(g.m >= R0) & (g.m < R1)]
        if len(rm) < 10:
            continue
        ORH, ORL = rm.high.max(), rm.low.min()
        if not np.isfinite(ORH) or ORH <= ORL:
            continue
        day_mask = (CB.day == day).values & (M >= R1) & (M < DAY_STOP)
        if not day_mask.any():
            continue
        session_end_pos = np.where((CB.day == day).values & (M < SESS_END))[0]
        if len(session_end_pos) == 0:
            continue
        stop_idx = session_end_pos.max() + 1
        breaks = scan_breaks(CB, day_mask, ORH, ORL)
        date_str = str(pd.Timestamp(day).date())

        for side, bi_pos in breaks.items():
            if bi_pos is None:
                continue
            bnd = ORH if side == 1 else ORL
            live = FVG[(FVG.known_idx <= bi_pos)].copy()
            live = live[~live.apply(lambda f: already_filled(f, bi_pos, Hc, Lc), axis=1)]
            above = live[live.lo >= ORH]
            below = live[live.hi <= ORL]
            broken_side = above if side == 1 else below
            fvg_above_present = len(above) > 0
            fvg_below_present = len(below) > 0

            if len(broken_side) == 0:
                rows.append(dict(inst=inst, tf=tf, u22=u22, be=int(be), draw_rule=draw_rule,
                    date=date_str, side=side,
                    fvg_above_present=fvg_above_present, fvg_below_present=fvg_below_present,
                    broken_side_fvg_present=False, touched=None, fill=None,
                    formation_cohort=None, returned_inside=None, opposite_reached=None,
                    continuation_reached=None, order=None,
                    entry02_trade=(date_str, side) in tmap,
                    entry02_win=(tmap.get((date_str, side)).gross > 0
                                 if (date_str, side) in tmap else None)))
                continue

            nearest = (min(broken_side.itertuples(), key=lambda f: f.lo) if side == 1
                       else min(broken_side.itertuples(), key=lambda f: -f.hi))
            tf_res = touch_and_fill(CB, nearest.lo, nearest.hi, bi_pos + 1, stop_idx)
            rec = dict(inst=inst, tf=tf, u22=u22, be=int(be), draw_rule=draw_rule,
                date=date_str, side=side,
                fvg_above_present=fvg_above_present, fvg_below_present=fvg_below_present,
                broken_side_fvg_present=True, touched=tf_res["touched"], fill=tf_res["fill"],
                formation_cohort=formation_cohort(nearest, M),
                returned_inside=None, opposite_reached=None, continuation_reached=None,
                order=None,
                entry02_trade=(date_str, side) in tmap,
                entry02_win=(tmap.get((date_str, side)).gross > 0
                             if (date_str, side) in tmap else None))
            if tf_res["touched"]:
                trow = tmap.get((date_str, side))
                draw_px = trow.draw if trow is not None else None
                rev = reversal_outcome(CB, side, ORH, ORL, tf_res["touch_idx"], stop_idx, draw_px)
                rec.update(returned_inside=rev["returned_inside"],
                           opposite_reached=rev["opposite_reached"],
                           continuation_reached=rev["continuation_reached"],
                           order=rev["order"])
            rows.append(rec)
    return pd.DataFrame(rows)

# ------------------------------------------------------------------ contingency counts
def primary_counts(diag):
    """[issue #3 PRIMARY COUNT REQUEST] Existing Entry-02 winners/losers x broken-side
    external-FVG touch. Restricted to rows where an Entry-02 trade actually exists."""
    t = diag[diag.entry02_trade & diag.broken_side_fvg_present].copy()
    t["touch_flag"] = t.touched.fillna(False)
    tab = (t.groupby(["entry02_win", "touch_flag"]).size()
             .unstack(fill_value=0).reindex(index=[True, False], columns=[True, False], fill_value=0))
    out = {"n": len(t), "counts": tab}
    for flag, label in ((True, "touched"), (False, "not_touched")):
        sub = t[t.touch_flag == flag]
        n = len(sub)
        out[f"win_rate_{label}"] = (sub.entry02_win.mean() if n else np.nan)
        out[f"n_{label}"] = n
    return out

def reversal_counts(diag, by=None):
    """[issue #3] broken-side FVG touched -> opposite ORB reached, 2x2, over ALL break
    events (not just Entry-02 trades). `by` groups additionally (e.g. ['side'] or
    ['inst','side'])."""
    t = diag[diag.broken_side_fvg_present].copy()
    t["touch_flag"] = t.touched.fillna(False)
    t["opp_flag"] = t.opposite_reached.fillna(False)
    keys = (by or []) + ["touch_flag", "opp_flag"]
    return t.groupby(keys).size().rename("n").reset_index()

def formation_timing_table(diag):
    """[issue #3] descriptive cohort: pre_orb / during_orb / post_orb x touch x reversal.
    Not a filter."""
    t = diag[diag.broken_side_fvg_present].copy()
    return (t.groupby(["formation_cohort", "touched", "opposite_reached"])
              .size().rename("n").reset_index())

def trend_bias_note():
    return ("RESEARCH_CURRENT v2.3 §D.3/§D.14 and §I U-24 state that CeeWilli's overall "
            "market-bias primitive is named once, in the pre-market checklist, with no "
            "mechanical method and no gate on any of his four models. cw_entry02.py "
            "computes no trend/bias field for this reason (the HTF bias veto was removed "
            "in v2.2). There is therefore no objective trend/bias column in this dataset "
            "to cross-tab the FVG-touch/reversal counts against. Per the issue's own "
            "instruction, this is reported and left for a Research ruling rather than "
            "fitted from economics.")

# ------------------------------------------------------------------ visual pack
def visual_pack(diag, CB_by_inst, out_dir, n_per_category=2):
    """[issue #3 VISUAL CHECK] Renders representative examples of the five requested
    categories, reusing the ORB/candle drawing conventions in v22_figs.py and adding the
    FVG zone, the touch bar and the outcome. Requires matplotlib and the bar cache used
    elsewhere in this branch (`../WORK/ny_{inst}.parquet` via v22_figs.bars); NOT run in
    this cycle (no data access) — this is the code that will produce the pack once the
    diagnostic has been executed and passed its own sanity checks."""
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import os
    os.makedirs(out_dir, exist_ok=True)

    categories = {
        "ORH_break_FVG_touched_ORL_reached":
            diag[(diag.side == 1) & diag.touched.fillna(False) & diag.opposite_reached.fillna(False)],
        "ORH_break_FVG_touched_continuation_wins":
            diag[(diag.side == 1) & diag.touched.fillna(False) & ~diag.opposite_reached.fillna(False)],
        "ORL_break_FVG_touched_ORH_reached":
            diag[(diag.side == -1) & diag.touched.fillna(False) & diag.opposite_reached.fillna(False)],
        "ORL_break_FVG_touched_continuation_wins":
            diag[(diag.side == -1) & diag.touched.fillna(False) & ~diag.opposite_reached.fillna(False)],
        "FVG_present_not_touched":
            diag[diag.broken_side_fvg_present & ~diag.touched.fillna(False)],
    }
    for name, rows in categories.items():
        sample = rows.head(n_per_category)
        if len(sample) == 0:
            continue
        fig, axes = plt.subplots(len(sample), 1, figsize=(11, 3.2 * len(sample)))
        axes = np.atleast_1d(axes)
        for ax, r in zip(axes, sample.itertuples()):
            bars = CB_by_inst[r.inst]
            day_bars = bars[(bars.day == pd.Timestamp(r.date, tz="America/New_York")) & (bars.m < SESS_END)]
            O, H, L, C, M = (day_bars.open.values, day_bars.high.values, day_bars.low.values,
                              day_bars.close.values, day_bars.m.values)
            for i in range(len(O)):
                col = "#2c7d72" if C[i] >= O[i] else "#a33c26"
                ax.plot([i, i], [L[i], H[i]], color=col, lw=.6)
                ax.add_patch(Rectangle((i - .32, min(O[i], C[i])), .64,
                                        max(abs(C[i] - O[i]), 1e-9), fc=col, ec=col, lw=.3))
            ax.set_title(f"{r.inst} {r.date} {'L' if r.side==1 else 'S'} | fill={r.fill} "
                          f"order={r.order}", fontsize=7, loc="left")
            ax.set_xticks([])
        fig.suptitle(name, fontsize=10)
        fig.tight_layout()
        fig.savefig(f"{out_dir}/{name}.png", dpi=105)
        plt.close(fig)

if __name__ == "__main__":
    # Not executed this cycle — no access to the canonical market-data store. Left as the
    # entry point for the run this module needs once data access is restored.
    raise SystemExit(
        "fvg_diagnostic.py: no canonical market-data store reachable in this environment. "
        "See ANALYST_CURRENT.md 'EXTERNAL FVG DIAGNOSTIC v2.3' for what this cycle could "
        "and could not do. Run diagnose()/primary_counts()/reversal_counts() from an "
        "environment with mdload access, validate against RESEARCH_CURRENT.md-style "
        "acceptance checks on a small sample, THEN trust the numbers.")
