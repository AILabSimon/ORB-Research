#!/usr/bin/env python3
import pandas as pd, numpy as np, os
R=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/13_CROSS_MARKET/CENSUS/RESULTS")
rng=np.random.default_rng(31337)
CELLS=[("NAS100","CASH0930"),("US500","CASH0930"),("XAUUSD","COMEX0820"),
       ("XAUUSD","CASH0930"),("EURUSD","LON0800"),("GBPUSD","LON0800")]
def get(mk,ev,L): return pd.read_csv(f"{R}/PHASEA_{mk}_{ev}_L{L}.csv")
def boot(x,n=2000):
    x=np.asarray(x,float); x=x[~np.isnan(x)]
    if len(x)<30: return np.nan,np.nan,np.nan
    b=np.array([rng.choice(x,len(x),True).mean() for _ in range(n)]); return x.mean(),np.percentile(b,2.5),np.percentile(b,97.5)

print("### PHASE B-1 — W pathology screen (a near-zero opening range makes W-normalised metrics explode)")
print(f"{'cell':24s} {'L':>3} {'medW':>9} {'p5 W':>9} {'share W < 0.25*medW':>21}")
for mk,ev in CELLS:
    for L in (5,15,30):
        d=get(mk,ev,L); w=d.W.values
        print(f"{mk+' '+ev:24s} {L:3d} {np.median(w):9.3f} {np.percentile(w,5):9.3f} {100*np.mean(w<0.25*np.median(w)):20.1f}%")

print("\n### PHASE B-2 — MARKET x FAMILY MATRIX")
print("Entry at the ORB edge with an OPPOSITE-EDGE stop makes R = W exactly, so MFE in W IS MFE in R.")
print("Effect = mean(MFE-MAE) in W. P2R = P(MFE_180 >= 2W). Robust screen: W >= 0.5 x lagged median W.\n")
hdr=f"{'cell':24s} {'L':>3} | {'family':10s} {'n':>6} {'P%':>6} {'eff(W)':>8} {'95% CI':>19} {'medMFE':>7} {'P2R%':>6} {'P3R%':>6} {'med t2R':>8}"
print(hdr); print("-"*len(hdr))
rows=[]
for mk,ev in CELLS:
    for L in (5,15,30):
        d=get(mk,ev,L)
        d=d[d.W>=0.5*d.W_med20_lag]                      # robust screen, pre-declared
        for fam,p in [("touch","tch_"),("close","cls_"),("retest","rts_"),("failrev","rev_")]:
            f=d.get(f"{p}mfe_W_180"); a=d.get(f"{p}mae_W_180")
            if f is None: continue
            m=(~f.isna())&(~a.isna())
            if m.sum()<40: continue
            e,lo,hi=boot((f[m]-a[m]).values)
            t2=d.loc[m,f"{p}t_2.0W_min"] if f"{p}t_2.0W_min" in d else pd.Series([-1])
            rows.append(dict(cell=f"{mk} {ev}",mk=mk,ev=ev,L=L,fam=fam,n=int(m.sum()),
                P=100*(f[m]>a[m]).mean(),eff=e,lo=lo,hi=hi,mfe=f[m].median(),
                P2R=100*(f[m]>=2).mean(),P3R=100*(f[m]>=3).mean(),
                t2R=float(t2[t2>=0].median()) if (t2>=0).any() else np.nan))
            r=rows[-1]
            print(f"{r['cell']:24s} {L:3d} | {fam:10s} {r['n']:6d} {r['P']:6.1f} {r['eff']:+8.3f} [{r['lo']:+.3f},{r['hi']:+.3f}] {r['mfe']:7.2f} {r['P2R']:6.1f} {r['P3R']:6.1f} {r['t2R']:8.0f}")
pd.DataFrame(rows).to_csv(os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/13_CROSS_MARKET/COMPARISON/MARKET_FAMILY_MATRIX.csv"),index=False)
