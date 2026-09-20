#!/usr/bin/env python3
import pandas as pd, numpy as np, os
rng=np.random.default_rng(20260912)
R=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/07_BEHAVIOURAL_CENSUS/RESULTS")
s=pd.read_csv(os.path.join(R,"CENSUS01_NAS100_ORB0930.csv")); s=s[s.signal==1].copy()

def outcomes(x,tgt=2.0,stop="ret_inside_touch_min"):
    """per-trade gross R outcome vector"""
    t=x[f"t_{int(tgt)}R_min"].values; r=x[stop].values; net=x["net_R_180"].values
    win=(t>=0)&((r<0)|(t<r)); lose=(r>=0)&((t<0)|(r<t)); nb=~(win|lose)
    o=np.where(win,tgt,np.where(lose,-1.0,np.clip(np.nan_to_num(net),-1,tgt)))
    return o

def boot(o,n=4000):
    m=np.array([rng.choice(o,len(o),replace=True).mean() for _ in range(n)])
    return o.mean(), np.percentile(m,2.5), np.percentile(m,97.5)

print("### O. COST SENSITIVITY — the verdict depends on execution venue, so all three are shown")
print("R_pts median by screen; cost charged as round-trip points / R_pts, per trade.\n")
SCEN=[("MNQ/NQ futures, tight  ", 1.00),
      ("MNQ/NQ futures, realistic",1.75),
      ("MNQ/NQ futures, poor fill",3.00),
      ("Dukascopy NAS100 CFD    ", 3.42),
      ("Retail/FTMO-style CFD   ", 6.00)]
for screen_lbl, minR in [("no screen (all signals)",0.0),("R>=7 pts",7.0),("R>=15 pts",15.0)]:
    v=s[s.R_pts>=minR]
    o=outcomes(v); g,lo,hi=boot(o)
    print(f"-- {screen_lbl:24s} n={len(v):4d}  medR={v.R_pts.median():5.1f}pts")
    print(f"   GROSS E = {g:+.4f}R   95% CI [{lo:+.4f}, {hi:+.4f}]  <- {'INCLUDES ZERO' if lo<0<hi else 'excludes zero'}")
    for lbl,c in SCEN:
        cr=(c/v.R_pts.values)
        net=o-cr
        print(f"     {lbl} cost={np.median(cr):.3f}R  NET E = {net.mean():+.4f}R")
    print()

print("### P. IS THE GROSS EFFECT DISTINGUISHABLE FROM THE CONTROL?")
sc=pd.read_csv(os.path.join(R,"CENSUS01_NAS100_PSEUDO1100.csv")); sc=sc[sc.signal==1]
for lbl,x in [("ORB 09:30",s[s.R_pts>=7]),("PSEUDO 11:00",sc[sc.R_pts>=7])]:
    o=outcomes(x); g,lo,hi=boot(o)
    print(f"  {lbl:14s} n={len(x):4d}  gross E={g:+.4f}R  CI[{lo:+.4f},{hi:+.4f}]")
a=outcomes(s[s.R_pts>=7]); b=outcomes(sc[sc.R_pts>=7])
diff=np.array([rng.choice(a,len(a),True).mean()-rng.choice(b,len(b),True).mean() for _ in range(4000)])
print(f"  difference ORB - PSEUDO = {a.mean()-b.mean():+.4f}R  CI[{np.percentile(diff,2.5):+.4f},{np.percentile(diff,97.5):+.4f}]")

print("\n### Q. BEST-CASE SUBSET (bar-1 signal, R>=7pts) — does anything survive?")
bv=s[(s.R_pts>=7)&(s.signal_bar==1)]
o=outcomes(bv); g,lo,hi=boot(o)
print(f"  n={len(bv)}  medR={bv.R_pts.median():.1f}pts  gross E={g:+.4f}R CI[{lo:+.4f},{hi:+.4f}]")
for lbl,c in SCEN:
    print(f"    {lbl} NET E = {(o-(c/bv.R_pts.values)).mean():+.4f}R")
print(f"  trades/year at this frequency: ~{len(bv)/12.5:.0f}")
