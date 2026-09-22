#!/usr/bin/env python3
"""
BASE-RATE CONTROL for the failed-break claim. The census measures 'opposite ORB reached' only
AFTER the invalidation, which cannot on its own show that the failed-break state carries
information. This adds the unconditional comparison:

  opp_any        opposite boundary touched at ANY time after the first break (whatever the path)
  opp_after_brk  same, measured from the bar after the break, for every broken day

If failed-break days and all-broken days reach the opposite boundary at the same rate, the
'failed break' state predicts nothing and only the timing differs. Counts only; no tuning.
"""
import numpy as np, pandas as pd, cw_entry02 as CW
R0,R1,SESS_END = CW.R0,CW.R1,CW.SESS_END

def add_base(inst):
    d = CW.load_ny(inst)
    cl = pd.read_parquet(f"../WORK/PATH_CENSUS_{inst}_CLASSIFIED.parquet").set_index("date")
    out={}
    for day,g in d.groupby("day",sort=True):
        k=str(pd.Timestamp(day).date())
        if k not in cl.index: continue
        r=cl.loc[k]
        if not bool(r.broke): continue
        p=g[(g.m>=R1)&(g.m<SESS_END)].reset_index(drop=True)
        M,H,L=p.m.values,p.high.values,p.low.values
        bi=int(np.searchsorted(M,r.break_m))
        aft=slice(bi+1,len(M))
        opp = r.ORL if r.side==1 else r.ORH
        hit = np.where((L[aft]<=opp) if r.side==1 else (H[aft]>=opp))[0]
        mid = np.where((L[aft]<=r["mid"]) if r.side==1 else (H[aft]>=r["mid"]))[0]
        out[k]=dict(opp_any=bool(len(hit)), opp_any_m=int(M[bi+1+hit[0]]) if len(hit) else np.nan,
                    mid_any=bool(len(mid)), mid_any_m=int(M[bi+1+mid[0]]) if len(mid) else np.nan)
    b=pd.DataFrame(out).T
    cl=cl.join(b).reset_index()
    cl.to_parquet(f"../WORK/PATH_CENSUS_{inst}_CLASSIFIED.parquet")
    return cl

L=[]
for inst in ("NAS100","US500"):
    c=add_base(inst); br=c[c.broke.fillna(False).astype(bool)]
    L.append(f"## {inst}  BASE-RATE CONTROL  (n broken days = {len(br)})")
    L.append("  Unconditional: after the first break, does price ever touch the OPPOSITE ORB boundary")
    L.append("  before 16:00?  (this is the quantity the failed-break state is supposed to predict)")
    L.append(f"  ALL broken days                 opp reached {100*br.opp_any.fillna(False).mean():5.1f}%   midline {100*br.mid_any.fillna(False).mean():5.1f}%   n={len(br)}")
    for k in ("continuation","failed-break","neither"):
        s=br[br.outcome==k]
        L.append(f"  {k:<22s} opp reached {100*s.opp_any.fillna(False).mean():5.1f}%   midline {100*s.mid_any.fillna(False).mean():5.1f}%   n={len(s)}")
    fb=br[br.outcome=="failed-break"]
    L.append(f"  LIFT of failed-break vs all broken days: {100*(fb.opp_any.fillna(False).mean()-br.opp_any.fillna(False).mean()):+5.1f} pp")
    ot=br[br.outcome!="failed-break"]
    L.append(f"  LIFT of failed-break vs NOT-failed-break: {100*(fb.opp_any.fillna(False).mean()-ot.opp_any.fillna(False).mean()):+5.1f} pp")
    # timing: does the confirmation precede the opposite touch, i.e. is it tradeable at all?
    f2=fb[fb.opp_any.fillna(False).astype(bool)]
    pre=(f2.newer_extreme_against_m < f2.opp_any_m)
    L.append(f"  of failed-break days that reach the opposite boundary (n={len(f2)}),")
    L.append(f"    confirmation fires BEFORE the opposite touch: {int(pre.sum())} ({100*pre.mean():.1f}%)")
    lag=(f2.opp_any_m-f2.newer_extreme_against_m)[pre]
    L.append(f"    median minutes confirmation -> opposite touch: {lag.median():.0f}  (IQR {lag.quantile(.25):.0f}-{lag.quantile(.75):.0f})")
    L.append("")
t="\n".join(L); print(t); open("../WORK/PATH_BASE_CONTROL.txt","w").write(t)
