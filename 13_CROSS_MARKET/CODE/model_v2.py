#!/usr/bin/env python3
"""
MODEL V2 — minimum source-faithful ORB, built to SPEC-SF-1 (Representation Audit 20.1 Part 12).
Written 2026-09-20. No optimisation. No filters. No parameter search.

EXPLICIT STATE MACHINE. Every transition causal, inspectable, no lookahead.

  S0 ORB_BUILD      09:30-09:45 ET, wick to wick -> ORH, ORL
  S1 ARMED          from 09:46
  S2 BREAK          first 1m bar to CLOSE beyond ORH (long) / ORL (short)      [SPEC 5]
                    the break places NO order                                   [SPEC 6]
  S3 RETURN         first later bar to TRADE back to the boundary               [SPEC 7, A-01]
                    low <= ORH (long) / high >= ORL (short)
                    a CLOSE back inside is PERMITTED and does not cancel        [SPEC 7]
  S4 REJECTION      arm REJ only: first bar after RETURN whose close is on the
                    trade side of its own midpoint AND which fails to close
                    beyond the boundary                                         [SPEC 8, A-02]
                    arm BASE (= A-02(iii)) skips S4 entirely
  S5 ENTRY_SIGNAL   first later bar to CLOSE beyond the boundary again          [SPEC 9]
  S6 FILL           at the NEXT bar's OPEN -- a price that certainly traded     [SPEC 9]
  S7 MANAGE         stop A: beyond the ENTRY BAR's extreme                      [SPEC 10, Max]
                    stop B: beyond the RETURN CLUSTER extreme (break->entry)    [SPEC 11, CeeWilli]
                    target: nearest PRIOR-SESSION extreme beyond entry          [SPEC 12]
                    post-entry invalidation: first 1m CLOSE back inside the ORB [SPEC 14]
  EXPIRY            abandon the attempt if no fill by 11:30 ET                  [SPEC 15, U-04]
                    one entry attempt per side per day                          [A-03]
                    direction may be re-earned on either side                   [A-04]

DECLARED, VISIBLE, NOT OPTIMISED:
  * no post-entry time stop in the source. Final exit is the 16:00 cash close.
    (V1 used 180 min. That was ours, not theirs. Recorded, not tuned.)
  * SPEC 12 can produce NO target when the prior-session extreme is already
    behind the entry. Those trades are carried with target=None and reported
    separately rather than given an invented target.
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E

R0 = 9*60+30            # 09:30
R1 = 9*60+45            # 09:45  -> 15-minute range          [SPEC 2]
EXPIRY = 11*60+30       # 11:30  day stop for ENTRY          [SPEC 15]
SESS_END = 16*60        # 16:00  final exit
COST = {"NAS100":2.92, "US500":1.26, "YF_NQ":1.25, "YF_ES":1.10}

def _prior_extremes(df):
    """prior CASH-SESSION high/low per day, shifted. No lookahead."""
    g = df.groupby("day").agg(hi=("high","max"), lo=("low","min"))
    return g.hi.shift(1), g.lo.shift(1)

def build(inst, arm="BASE", stop_mode="B", tz="America/New_York", verbose_day=None):
    raw = mdload.load(inst, side="TRADE") if inst.startswith("YF_") else mdload.load(inst)
    d = raw.copy(); d["timestamp"]=pd.to_datetime(d["timestamp"],utc=True)
    loc = d["timestamp"].dt.tz_convert(tz)
    d["m"]=loc.dt.hour*60+loc.dt.minute; d["day"]=loc.dt.normalize()
    d = d[(loc.dt.dayofweek<5)&(d.m>=R0)&(d.m<SESS_END)]
    pri_hi, pri_lo = _prior_extremes(d)
    cost = COST[inst]; rows=[]; trace=[]
    for day, g in d.groupby("day", sort=True):
        m=g.m.values; o=g.open.values; h=g.high.values; l=g.low.values; c=g.close.values
        rm=(m>=R0)&(m<R1)
        if rm.sum()<15: continue
        ORH, ORL = h[rm].max(), l[rm].min()
        if not np.isfinite(ORH) or ORH<=ORL: continue
        post = np.where(m>=R1)[0]
        if len(post)<60: continue
        PH, PL = pri_hi.get(day, np.nan), pri_lo.get(day, np.nan)
        used = {1:False, -1:False}          # one attempt per side           [A-03]
        i = post[0]; n = len(m)
        # ---------------- scan the day ----------------
        while i < n-2:
            # ---- S2 BREAK : first 1m CLOSE beyond a boundary, side not yet used
            side = 0
            if c[i] > ORH and not used[1]:   side = 1;  bnd = ORH
            elif c[i] < ORL and not used[-1]: side = -1; bnd = ORL
            if side == 0: i += 1; continue
            bi = i
            # ---- S3 RETURN : trade back to the boundary                    [A-01]
            ri = None
            for j in range(bi+1, n):
                if m[j] >= EXPIRY: break
                if (l[j] <= bnd) if side==1 else (h[j] >= bnd): ri = j; break
            if ri is None:
                used[side]=True; i = bi+1; continue
            # ---- S4 REJECTION (arm REJ only)                               [A-02]
            start = ri
            if arm == "REJ":
                kj = None
                for j in range(ri, n):
                    if m[j] >= EXPIRY: break
                    mid = (h[j]+l[j])/2.0
                    on_side = (c[j] > mid) if side==1 else (c[j] < mid)
                    not_beyond = (c[j] <= bnd) if side==1 else (c[j] >= bnd)
                    if on_side and not_beyond: kj = j; break
                if kj is None:
                    used[side]=True; i = ri+1; continue
                start = kj
            # ---- S5 ENTRY SIGNAL : first later CLOSE beyond the boundary   [SPEC 9]
            si = None
            for j in range(start+1, n):
                if m[j] >= EXPIRY: break
                if (c[j] > bnd) if side==1 else (c[j] < bnd): si = j; break
            if si is None or si >= n-2:
                used[side]=True; i = (si or start)+1; continue
            # ---- S6 FILL at the NEXT bar's OPEN                            [SPEC 9]
            fi = si+1; px = o[fi]
            # ---- S7 stop                                                    [SPEC 10/11]
            if stop_mode == "A":
                stop = l[si] if side==1 else h[si]            # entry bar extreme
            else:
                seg = slice(bi, si+1)                          # return cluster
                stop = l[seg].min() if side==1 else h[seg].max()
            R = abs(px-stop)
            if R <= 0: used[side]=True; i = fi+1; continue
            # ---- target: nearest PRIOR-SESSION extreme beyond entry        [SPEC 12]
            tgt = None
            if side==1 and np.isfinite(PH) and PH > px: tgt = PH
            if side==-1 and np.isfinite(PL) and PL < px: tgt = PL
            # ---- walk forward
            ex=exr=None; mfe=mae=0.0; term=fi
            for j in range(fi, n):
                term=j
                fav=(h[j]-px) if side==1 else (px-l[j])
                adv=(px-l[j]) if side==1 else (h[j]-px)
                mfe=max(mfe,fav); mae=max(mae,adv)
                hs=(l[j]<=stop) if side==1 else (h[j]>=stop)
                ht=(tgt is not None) and ((h[j]>=tgt) if side==1 else (l[j]<=tgt))
                if hs and ht: ex,exr=stop,"ambig"; break        # conservative
                if hs: ex,exr=stop,"stop"; break
                if ht: ex,exr=tgt,"target"; break
                if ORL <= c[j] <= ORH: ex,exr=c[j],"invalidation"; break   # [SPEC 14]
                if m[j] >= SESS_END-1: ex,exr=c[j],"eod"; break
            if ex is None: ex,exr=c[-1],"eod"
            gross=((ex-px)*side)/R
            rows.append(dict(date=str(pd.Timestamp(day).date()), inst=inst, arm=arm,
                stop_mode=stop_mode, side=side, ORH=ORH, ORL=ORL, W=ORH-ORL,
                break_m=int(m[bi]), return_m=int(m[ri]), sig_m=int(m[si]), entry_m=int(m[fi]),
                entry=px, stop=stop, R_pts=R, target=(tgt if tgt is not None else np.nan),
                has_target=int(tgt is not None), tgt_R=((abs(tgt-px)/R) if tgt is not None else np.nan),
                exit=ex, exit_reason=exr, gross=gross, net=gross-cost/R,
                mfe_R=mfe/R, mae_R=mae/R, hold=int(m[term]-m[fi]),
                bars_break_to_entry=int(m[fi]-m[bi]), cost_R=cost/R))
            used[side]=True
            i = term+1                                          # no concurrent positions
        if verbose_day is not None and str(pd.Timestamp(day).date())==verbose_day:
            trace.append(dict(ORH=ORH,ORL=ORL,m=m,o=o,h=h,l=l,c=c))
    out=pd.DataFrame(rows)
    if len(out): out["yr"]=out.date.str[:4].astype(int)
    return (out, trace) if verbose_day is not None else out
