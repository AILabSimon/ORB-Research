#!/usr/bin/env python3
"""FAILED-BREAK TIMING SUB-CASES. Three columns per instrument:
   1 confirmation BEFORE the opposite touch (actionable)
   2 opposite boundary ALREADY touched before the confirmation printed (too late)
   3 confirmation printed, opposite boundary never reached
Deterministic selection: first N by date. No filters beyond the class."""
import os, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import cw_entry02 as CW
from orb_path_figs import panel, hhmm, OUT, TF

def build(n_each=3):
    fig, axes = plt.subplots(n_each, 6, figsize=(24, 4.2*n_each)); axes=np.atleast_2d(axes)
    col=0
    for inst in ("NAS100","US500"):
        c=pd.read_parquet(f"../WORK/PATH_CENSUS_{inst}_CLASSIFIED.parquet")
        c=c[c.broke.fillna(False).astype(bool)].copy()
        c["opp_any"]=c.opp_any.fillna(False).astype(bool)
        f=c[c.newer_extreme_against.fillna(False).astype(bool)].copy().sort_values("date")
        cases=[("1 ACTIONABLE confirm->opp", f[f.opp_any & (f.opp_any_m>f.newer_extreme_against_m)]),
               ("2 TOO LATE opp before confirm", f[f.opp_any & (f.opp_any_m<=f.newer_extreme_against_m)]),
               ("3 CONFIRMED but opp NEVER reached", f[~f.opp_any])]
        raw=CW.load_ny(inst); cache={}
        def bars(day):
            if day in cache: return cache[day]
            dd=pd.Timestamp(day)
            if dd.tz is None: dd=dd.tz_localize("America/New_York")
            g=raw[raw.day==dd]; g=g[g.m<CW.SESS_END]
            b=CW.resample(g,TF).reset_index(drop=True) if len(g) else g
            cache[day]=b; return b
        for name,s in cases:
            for i in range(n_each):
                ax=axes[i,col]
                if i>=len(s): ax.axis("off"); continue
                r=s.iloc[i]; b=bars(r["date"])
                if not len(b): ax.axis("off"); continue
                rr=dict(r); rr["opp_m"]=r["opp_any_m"]
                panel(ax,b,rr,f"{name}\n{inst} {r['date']} W={r['W']:.1f} side={int(r['side']):+d}\n"
                              f"brk {hhmm(r['break_m'])} inside {hhmm(r['inside_m'])} confirm {hhmm(r['newer_extreme_against_m'])}\n"
                              f"mid {hhmm(r['mid_any_m'])}  opp {hhmm(r['opp_any_m'])}")
            col+=1
    fig.suptitle("FAILED-BREAK timing sub-cases (5m). NAS100 cols 1-3 | US500 cols 4-6.  "
                 "dotted amber=break  dashed grey=close back inside  solid red=newer extreme against  solid blue=opposite ORB",fontsize=10)
    fig.tight_layout(rect=[0,0,1,0.965])
    p=f"{OUT}/FAILED_BREAK_TIMING.png"; fig.savefig(p,dpi=115); plt.close(fig); print("wrote",p); return p
if __name__=="__main__": build()
