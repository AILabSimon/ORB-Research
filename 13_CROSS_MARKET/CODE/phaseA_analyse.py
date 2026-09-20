#!/usr/bin/env python3
import pandas as pd, numpy as np, os, itertools
R=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/13_CROSS_MARKET/CENSUS/RESULTS")
rng=np.random.default_rng(2026)
CELLS=[("NAS100","CASH0930"),("US500","CASH0930"),("XAUUSD","COMEX0820"),
       ("XAUUSD","CASH0930"),("EURUSD","LON0800"),("GBPUSD","LON0800")]
def get(mk,ev,L): return pd.read_csv(f"{R}/PHASEA_{mk}_{ev}_L{L}.csv")
def ci(x,n=2000):
    x=np.asarray(x,float); x=x[~np.isnan(x)]
    if len(x)<20: return (np.nan,np.nan,np.nan)
    b=np.array([rng.choice(x,len(x),True).mean() for _ in range(n)])
    return x.mean(),np.percentile(b,2.5),np.percentile(b,97.5)
def asym(d,pfx,h="180"):
    """directional asymmetry: P(MFE>MAE) and the effect size mean(MFE-MAE) in W"""
    f=d.get(f"{pfx}mfe_W_{h}"); a=d.get(f"{pfx}mae_W_{h}")
    if f is None: return None
    m=(~f.isna())&(~a.isna())
    if m.sum()<50: return None
    p=100*(f[m]>a[m]).mean(); e,lo,hi=ci((f[m]-a[m]).values)
    return dict(n=int(m.sum()),p=p,eff=e,lo=lo,hi=hi,mfe=f[m].median(),mae=a[m].median())

print("="*110)
print("PHASE A — X-3: TOUCH vs COMPLETED CLOSE qualification.  P(MFE>MAE) at 180 min; effect size in W")
print("="*110)
print(f"{'market/event':22s} {'L':>3} | {'TOUCH n':>8} {'P%':>6} {'eff(W)':>8} {'95% CI':>20} | {'CLOSE n':>8} {'P%':>6} {'eff(W)':>8} {'95% CI':>20}")
for mk,ev in CELLS:
    for L in (5,15,30):
        d=get(mk,ev,L); t=asym(d,"tch_"); c=asym(d,"cls_")
        ts=f"{t['n']:8d} {t['p']:6.1f} {t['eff']:+8.3f} [{t['lo']:+.3f},{t['hi']:+.3f}]" if t else " "*8+"   n/a"+" "*22
        cs=f"{c['n']:8d} {c['p']:6.1f} {c['eff']:+8.3f} [{c['lo']:+.3f},{c['hi']:+.3f}]" if c else " "*8+"   n/a"
        print(f"{mk+' '+ev:22s} {L:3d} | {ts} | {cs}")

print("\n"+"="*110)
print("X-1 CONTROL — does the OPENING event add information? (same measure at a 12:00 non-opening range)")
print("="*110)
print(f"{'market':22s} {'L':>3} | {'OPEN close-qual P%':>19} {'eff(W)':>9} | {'CTRL 12:00 P%':>14} {'eff(W)':>9} | {'delta eff':>10}")
for mk,ev in CELLS:
    for L in (5,15,30):
        c=asym(get(mk,ev,L),"cls_"); k=asym(get(mk,"CTRL1200",L),"cls_")
        if not c or not k: continue
        print(f"{mk+' '+ev:22s} {L:3d} | {c['p']:19.1f} {c['eff']:+9.3f} | {k['p']:14.1f} {k['eff']:+9.3f} | {c['eff']-k['eff']:+10.3f}")
