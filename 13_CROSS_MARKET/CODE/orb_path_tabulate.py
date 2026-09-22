#!/usr/bin/env python3
"""
ORB PATH CENSUS -- TABULATION. Counts only. No thresholds, no optimisation, no scoring.

Classification rule (stated, not tuned): a day's OUTCOME after the first break is decided by
which source-defined confirmation fires FIRST in clock time:
    continuation   -- newer extreme in the break direction, after the retrace, with no prior
                      1m close back inside the ORB        (V4 05:37 "it needs to hold outside of it")
    failed-break   -- a 1m close back inside the ORB (V8 06:11 invalidation) followed by a newer
                      extreme AGAINST                     (V8 16:33 "this confirmation, newer low")
    neither        -- no confirmation of either kind before 16:00
Ties are impossible: the two events are defined on disjoint time ranges by construction.
"""
import numpy as np, pandas as pd

INF = 10**9
def _m(v):
    return INF if (v is None or (isinstance(v, float) and np.isnan(v))) else float(v)

def classify(df):
    d = df.copy()
    cont_m, fail_m = [], []
    for _, r in d.iterrows():
        if not r.get("broke", False):
            cont_m.append(INF); fail_m.append(INF); continue
        ins = _m(r.get("inside_m")); nw = _m(r.get("newer_extreme_with_m")); na = _m(r.get("newer_extreme_against_m"))
        cont_m.append(nw if nw < ins else INF)                       # newer extreme WITH, before any close back inside
        fail_m.append(na if (ins < INF and na < INF) else INF)       # close back inside, THEN newer extreme against
    d["cont_m"] = cont_m; d["fail_m"] = fail_m
    lab = np.where(d.cont_m < d.fail_m, "continuation",
          np.where(d.fail_m < d.cont_m, "failed-break", "neither"))
    d["outcome"] = np.where(d.broke.fillna(False).astype(bool), lab, "no-break")
    d.loc[(d.cont_m >= INF) & (d.fail_m >= INF) & d.broke.fillna(False).astype(bool), "outcome"] = "neither"
    return d

def pct(n, N): return f"{n:5d}  ({100.0*n/N:5.1f}%)" if N else f"{n:5d}      -- "

def report(d, inst, fvg=None, out=None):
    P = []
    def w(s=""): P.append(s)
    N = len(d)
    w(f"## {inst}   --  {N} ORB days  (2016-01-04 .. {d.date.max()})")
    w()
    up = d[d.side == 1]; dn = d[d.side == -1]; nb = d[~d.broke.fillna(False).astype(bool)]
    w("### 1. TOTAL ORB DAYS -> FIRST BREAK")
    w(f"  total ORB days                 {N:5d}")
    w(f"  ORH breaks first               {pct(len(up), N)}")
    w(f"  ORL breaks first               {pct(len(dn), N)}")
    w(f"  no 1m close beyond either      {pct(len(nb), N)}")
    w()
    for nm, s in (("ORH BREAK (long side)", up), ("ORL BREAK (short side)", dn)):
        n = len(s)
        w(f"### 2. {nm}  -- n={n}")
        rt = s[s.retraced.astype(bool)]; nrt = s[~s.retraced.astype(bool)]
        w(f"  retraces to the broken level   {pct(len(rt), n)}")
        w(f"  never retraces                 {pct(len(nrt), n)}")
        w(f"  closes back inside the ORB     {pct(int(s.closed_back_inside.astype(bool).sum()), n)}")
        w(f"  holds outside all session      {pct(int(s.held_outside.astype(bool).sum()), n)}")
        w()
        w(f"### 3. {nm} + RETRACE  -- n={len(rt)}   (first confirmation to fire)")
        for k in ("continuation", "failed-break", "neither"):
            w(f"  {k:<28s} {pct(int((rt.outcome == k).sum()), len(rt))}")
        w()
        fb = s[(s.outcome == "failed-break")]
        w(f"### 4. FAILED {'ORH' if nm.startswith('ORH') else 'ORL'} BREAK  -- n={len(fb)}   (draws after invalidation)")
        w(f"  midline reached                {pct(int(fb.mid_reached.fillna(False).astype(bool).sum()), len(fb))}")
        w(f"  OPPOSITE ORB boundary reached  {pct(int(fb.opp_reached.fillna(False).astype(bool).sum()), len(fb))}")
        w(f"  opposite NOT reached           {pct(int((~fb.opp_reached.fillna(False).astype(bool)).sum()), len(fb))}")
        if len(fb):
            lag = (fb.opp_m - fb.inside_m).dropna()
            if len(lag): w(f"  median minutes invalidation->opposite   {lag.median():.0f}   (IQR {lag.quantile(.25):.0f}-{lag.quantile(.75):.0f})")
        w()
    w("### 5. BASE RATE OF REACHING THE OPPOSITE BOUNDARY  (all broken days, by outcome)")
    br = d[d.broke.fillna(False).astype(bool)]
    for k in ("continuation", "failed-break", "neither"):
        s = br[br.outcome == k]
        if not len(s): continue
        # opp_reached is only computed for days that closed back inside; recompute marginal honestly
        oc = s.opp_reached.fillna(False).astype(bool).sum()
        w(f"  {k:<14s} n={len(s):5d}   opposite reached after invalidation {pct(int(oc), len(s))}")
    w("  NOTE: opp_reached is measured only AFTER the FIRST 1m close back inside the ORB. On a")
    w("        'continuation' day that close occurs LATER than the continuation confirmation, so the")
    w("        continuation row counts days that ran, then failed, then reversed all the way across.")
    w()
    w("### 6. CONSOLIDATION AFTER THE RETRACE  (neither a newer high nor a newer low)")
    rt = br[br.retraced.astype(bool)]
    for Nw in (10, 20, 30):
        c = rt[rt[f"consol_{Nw}"].fillna(False).astype(bool)]
        w(f"  {Nw:2d}-bar window: {pct(len(c), len(rt))}   of which continuation {int((c.outcome=='continuation').sum()):4d}  failed-break {int((c.outcome=='failed-break').sum()):4d}  neither {int((c.outcome=='neither').sum()):4d}")
    w()
    if fvg is not None:
        w("### 7. CROSS-TAB WITH EXTERNAL FVG PRESENT (1m, formed any time before the outcome)")
        m = br.merge(fvg[["date", "ext_above_present", "ext_below_present"]], on="date", how="left")
        # the FVG that matters is the one on the side price would travel to on FAILURE
        m["fvg_opp"] = np.where(m.side == 1, m.ext_below_present, m.ext_above_present)
        m["fvg_opp"] = m.fvg_opp.fillna(False).astype(bool)
        w(f"  {'':<22s} {'FVG opposite side PRESENT':>28s} {'ABSENT':>18s}")
        for k in ("continuation", "failed-break", "neither"):
            a = int(((m.outcome == k) & m.fvg_opp).sum()); b = int(((m.outcome == k) & ~m.fvg_opp).sum())
            w(f"  {k:<22s} {a:12d} {100.0*a/max(1,int(m.fvg_opp.sum())):9.1f}% {b:10d} {100.0*b/max(1,int((~m.fvg_opp).sum())):7.1f}%")
        w(f"  totals                 {int(m.fvg_opp.sum()):12d}            {int((~m.fvg_opp).sum()):10d}")
        fb = m[m.outcome == "failed-break"]
        a = fb[fb.fvg_opp]; b = fb[~fb.fvg_opp]
        w(f"  failed-break -> opposite ORB reached | FVG present {100.0*a.opp_reached.fillna(False).mean():5.1f}%  (n={len(a)})"
          f"   | absent {100.0*b.opp_reached.fillna(False).mean():5.1f}%  (n={len(b)})")
        w()
    txt = "\n".join(P)
    print(txt)
    return txt

if __name__ == "__main__":
    import sys
    blocks = []
    for inst in ("NAS100", "US500"):
        d = classify(pd.read_parquet(f"../WORK/PATH_CENSUS_{inst}.parquet"))
        d.to_parquet(f"../WORK/PATH_CENSUS_{inst}_CLASSIFIED.parquet")
        try: fvg = pd.read_parquet(f"../WORK/FVG_CENSUS_{inst}_1m.parquet")
        except Exception: fvg = None
        blocks.append(report(d, inst, fvg))
        print()
    open("../WORK/PATH_CENSUS_TABLES.txt", "w").write("\n\n".join(blocks))
