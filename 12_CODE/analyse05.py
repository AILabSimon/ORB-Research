#!/usr/bin/env python3
import pandas as pd, numpy as np, os
rng=np.random.default_rng(7)
R=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/07_BEHAVIOURAL_CENSUS/RESULTS")
def prep(f):
    d=pd.read_csv(os.path.join(R,f)); d=d[d.signal==1].copy(); d["yr"]=d.date.str[:4].astype(int); return d
def outc(x,tgt=2.0):
    t=x[f"t_{int(tgt)}R_min"].values; r=x["ret_inside_touch_min"].values; net=np.nan_to_num(x["net_R_180"].values)
    win=(t>=0)&((r<0)|(t<r)); lose=(r>=0)&((t<0)|(r<t)); nb=~(win|lose)
    return np.where(win,tgt,np.where(lose,-1.0,np.clip(net,-1,tgt)))
def boot(o,n=3000):
    m=np.array([rng.choice(o,len(o),True).mean() for _ in range(n)]); return o.mean(),np.percentile(m,2.5),np.percentile(m,97.5)
s=prep("CENSUS01_NAS100_ORB0930.csv")

print("### R. IS THE R-SIZE EFFECT MONOTONE, OR IS R>=15 A LUCKY CUT?")
s["dec"]=pd.qcut(s.R_pts,10,labels=False,duplicates="drop")
for k,g in s.groupby("dec"):
    o=outc(g); m,lo,hi=boot(o)
    print(f"  decile {k+1:2d}  R_pts {g.R_pts.min():7.2f}-{g.R_pts.max():7.2f}  n={len(g):4d}  grossE={m:+.3f}R CI[{lo:+.3f},{hi:+.3f}]")

print("\n### S. TEMPORAL VALIDATION of the Analyst-introduced R>=15pt screen")
print("    Development 2013-2021 | Holdout 2022-2026 (never used to choose anything)")
v=s[s.R_pts>=15]
for lbl,g in [("DEV 2013-2021",v[v.yr<=2021]),("HOLDOUT 2022-2026",v[v.yr>=2022])]:
    o=outc(g); m,lo,hi=boot(o)
    cost=np.median(1.75/g.R_pts.values)
    print(f"  {lbl:18s} n={len(g):4d} grossE={m:+.4f}R CI[{lo:+.4f},{hi:+.4f}]  netE(MNQ realistic)={(o-1.75/g.R_pts.values).mean():+.4f}R")
print("  per-year net (MNQ realistic cost 1.75 pts round trip):")
for y,g in v.groupby("yr"):
    if len(g)<25: continue
    o=outc(g); n=(o-1.75/g.R_pts.values).mean()
    print(f"    {y} n={len(g):3d} netE={n:+.3f}R  cum trades ok")

print("\n### T. SAME SCREEN ON THE CONTROL (pseudo 11:00 range) — does R>=15 'work' there too?")
sc=prep("CENSUS01_NAS100_PSEUDO1100.csv"); vc=sc[sc.R_pts>=15]
o=outc(vc); m,lo,hi=boot(o)
print(f"  PSEUDO 11:00, R>=15: n={len(vc)} grossE={m:+.4f}R CI[{lo:+.4f},{hi:+.4f}] netE={(o-1.75/vc.R_pts.values).mean():+.4f}R")
print("  => if the control also 'works', the screen is a cost-geometry artefact, not an ORB edge.")

print("\n### U. CROSS-INSTRUMENT: US500 with the same screen (scaled: R>=15pts NAS ~ R>=4pts US500)")
s5=prep("CENSUS01_US500_ORB0930.csv")
for thr in [4,6]:
    g=s5[s5.R_pts>=thr]; o=outc(g); m,lo,hi=boot(o)
    print(f"  US500 R>={thr}pts n={len(g):4d} grossE={m:+.4f}R CI[{lo:+.4f},{hi:+.4f}] netE(ES 0.5pt rt)={(o-0.5/g.R_pts.values).mean():+.4f}R")
