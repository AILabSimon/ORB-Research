#!/usr/bin/env python3
"""
ORB PATH CENSUS — observation-first. Counts only; no strategy, no thresholds, no filters.

Every state below is expressed in the SOURCE'S OWN primitives, quoted in the cycle report:
  break            a 1-minute CLOSE beyond ORH/ORL after 09:45        (V8 02:37, V5 05:24)
  retrace          price trades back to the broken level               (V10 12:50 "retest the orb")
  hold outside     no 1m close back inside the ORB                    (V4 05:37 "it needs to hold outside of it")
  close back in    a 1m close inside [ORL, ORH] = invalidation        (V8 06:11 "closed inside of orb ... not a confirmation")
  newer extreme    a new high/low beyond the prior one                (V8 06:11, V11 26:21 "newer low")
  consolidation    NEITHER a newer high NOR a newer low               (V12 20:34 "failed to make a newer high, failed to make a newer low")
  midline          (ORH+ORL)/2                                        (V5 06:52) -- failed-break TP1 (V8 18:07)
  opposite ORB     the far boundary                                   (V8 18:07 "ride the top of orb to the bottom of orb")

NOTHING here is tuned. The only free choice is the consolidation observation window, and it is
reported across several values rather than picked, because no source states one for the
post-break state (Max's "six or seven candles" is a DAY-level containment rule, not this).
"""
import numpy as np, pandas as pd, cw_entry02 as CW

R0, R1, SESS_END = CW.R0, CW.R1, CW.SESS_END

def census(inst, d=None, cons_windows=(10, 20, 30)):
    if d is None: d = CW.load_ny(inst)
    rows = []
    for day, g in d.groupby("day", sort=True):
        rm = g[(g.m >= R0) & (g.m < R1)]
        if len(rm) < 10: continue
        ORH, ORL = rm.high.max(), rm.low.min()
        if not np.isfinite(ORH) or ORH <= ORL: continue
        mid = (ORH + ORL) / 2.0
        p = g[(g.m >= R1) & (g.m < SESS_END)].reset_index(drop=True)
        if len(p) < 60: continue
        H, L, C, M = p.high.values, p.low.values, p.close.values, p.m.values
        rec = dict(date=str(pd.Timestamp(day).date()), inst=inst, ORH=ORH, ORL=ORL, mid=mid, W=ORH-ORL)
        # ---- first break (1m close beyond a boundary)
        up = np.where(C > ORH)[0]; dn = np.where(C < ORL)[0]
        bi = None
        if len(up) and (not len(dn) or up[0] < dn[0]): bi, side, bnd = up[0], 1, ORH
        elif len(dn): bi, side, bnd = dn[0], -1, ORL
        if bi is None:
            rec.update(broke=False); rows.append(rec); continue
        rec.update(broke=True, side=side, break_m=int(M[bi]))
        post = slice(bi + 1, len(M))
        # ---- extreme reached on the break leg before any retrace
        # ---- retrace: price trades back to the broken level
        back = np.where((L[post] <= bnd) if side == 1 else (H[post] >= bnd))[0]
        rec["retraced"] = bool(len(back))
        rec["retrace_m"] = int(M[bi + 1 + back[0]]) if len(back) else np.nan
        # ---- close back inside the ORB at any point after the break
        ins = np.where((C[post] >= ORL) & (C[post] <= ORH))[0]
        rec["closed_back_inside"] = bool(len(ins))
        rec["inside_m"] = int(M[bi + 1 + ins[0]]) if len(ins) else np.nan
        rec["held_outside"] = not rec["closed_back_inside"]
        # ---- newer extreme in the break direction, AFTER the retrace (continuation)
        if len(back):
            r0 = bi + 1 + back[0]
            ext_at_retrace = H[:r0+1].max() if side == 1 else L[:r0+1].min()
            after = slice(r0 + 1, len(M))
            nx = np.where((H[after] > ext_at_retrace) if side == 1 else (L[after] < ext_at_retrace))[0]
            rec["newer_extreme_with"] = bool(len(nx))
            rec["newer_extreme_with_m"] = int(M[r0 + 1 + nx[0]]) if len(nx) else np.nan
            # newer extreme AGAINST after a close back inside  (V8 16:33 "this confirmation, newer low")
            if rec["closed_back_inside"]:
                i0 = bi + 1 + ins[0]
                opp_ext = L[:i0+1].min() if side == 1 else H[:i0+1].max()
                aft = slice(i0 + 1, len(M))
                na = np.where((L[aft] < opp_ext) if side == 1 else (H[aft] > opp_ext))[0]
                rec["newer_extreme_against"] = bool(len(na))
                rec["newer_extreme_against_m"] = int(M[i0 + 1 + na[0]]) if len(na) else np.nan
            # consolidation: neither a newer high nor a newer low over N bars from the retrace
            for N in cons_windows:
                w = slice(r0, min(r0 + N, len(M)))
                hh = H[w]; ll = L[w]
                if len(hh) < 3: rec[f"consol_{N}"] = False; continue
                rec[f"consol_{N}"] = bool((hh.max() <= H[:r0+1].max()) and (ll.min() >= L[:r0+1].min()))
        # ---- draws after a failure: midline, then the opposite boundary
        if rec["closed_back_inside"]:
            i0 = bi + 1 + ins[0]; aft = slice(i0 + 1, len(M))
            hit_mid = np.where((L[aft] <= mid) if side == 1 else (H[aft] >= mid))[0]
            opp = ORL if side == 1 else ORH
            hit_opp = np.where((L[aft] <= opp) if side == 1 else (H[aft] >= opp))[0]
            rec["mid_reached"] = bool(len(hit_mid)); rec["opp_reached"] = bool(len(hit_opp))
            rec["mid_m"] = int(M[i0+1+hit_mid[0]]) if len(hit_mid) else np.nan
            rec["opp_m"] = int(M[i0+1+hit_opp[0]]) if len(hit_opp) else np.nan
        rows.append(rec)
    return pd.DataFrame(rows)
