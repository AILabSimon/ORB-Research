#!/usr/bin/env python3
import pandas as pd, numpy as np, os
R=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/07_BEHAVIOURAL_CENSUS/RESULTS")
def load(f):
    d=pd.read_csv(os.path.join(R,f)); return d[d.signal==1].copy()
def race(x,tgt=2.0,stop="ret_inside_touch_min"):
    t=x[f"t_{int(tgt)}R_min"]; r=x[stop]
    win=(t>=0)&((r<0)|(t<r)); lose=(r>=0)&((t<0)|(r<t)); nb=~(win|lose)
    tail=x.loc[nb,"net_R_180"].clip(-1,tgt).mean() if nb.any() else 0.0
    return win.mean()*tgt - lose.mean() + nb.mean()*tail, win.mean()

print("### J. TEMPORAL STABILITY — NAS100, viable signals, 2R touch-stop")
s=load("CENSUS01_NAS100_ORB0930.csv"); COST=3.42
v=s[s.R_pts>=2*COST].copy(); v["yr"]=v.date.str[:4].astype(int)
for y,g in v.groupby("yr"):
    if len(g)<40: continue
    e,w=race(g); c=(COST/g.R_pts).median()
    print(f"  {y} n={len(g):4d} P(MFE>MAE,180)={100*(g.mfe_R_180>g.mae_R_180).mean():5.1f}%  win2R={100*w:5.1f}%  grossE={e:+.3f}R  netE={e-c:+.3f}R")

print("\n### K. DIRECTION")
for dlab,dv in [("UP breaks",1),("DOWN breaks",-1)]:
    g=v[v.dir==dv]; e,w=race(g); c=(COST/g.R_pts).median()
    print(f"  {dlab:12s} n={len(g):4d} P(MFE>MAE,180)={100*(g.mfe_R_180>g.mae_R_180).mean():5.1f}% win2R={100*w:5.1f}% grossE={e:+.3f}R netE={e-c:+.3f}R")

print("\n### L. CROSS-INSTRUMENT — US500 (proxy for ES/MES/SPX)")
s5=load("CENSUS01_US500_ORB0930.csv"); C5=0.55+2*0.5   # measured US500 spread + slippage
v5=s5[s5.R_pts>=2*C5]
print(f"  US500 viable n={len(v5)} of {len(s5)} ({100*len(v5)/len(s5):.1f}%) medR={v5.R_pts.median():.2f}pts")
for h in ["30","60","180","EOD"]:
    print(f"   h={h:>4}: P(MFE>MAE)={100*(v5[f'mfe_R_{h}']>v5[f'mae_R_{h}']).mean():5.1f}%  medMFE={v5[f'mfe_R_{h}'].median():.2f}R medMAE={v5[f'mae_R_{h}'].median():.2f}R")
e,w=race(v5); c=(C5/v5.R_pts).median()
print(f"  2R race: win={100*w:.1f}% grossE={e:+.3f}R  cost={c:.3f}R  netE={e-c:+.3f}R")

print("\n### M. MARTINGALE DIAGNOSTIC — flat expectancy across targets is the signature of no drift")
for nm,x,cc in [("NAS100",v,COST),("US500",v5,C5)]:
    line=[]
    for tgt in [1,2,3]:
        e,w=race(x,tgt); line.append(f"{tgt}R: gross{e:+.3f}")
    print(f"  {nm}: "+"  ".join(line)+"   (a driftless walk gives ~0 at every target)")

print("\n### N. Q7 RE-EXAMINED — is the reversal result mechanical?")
print("  Conditional on a 15m close back inside, price is already inside the range, so")
print("  'reaches the mid' is largely structural. Proper test needs a path measured FROM the")
print("  return point, which CENSUS-01 does not capture. Reporting the position of the")
print("  return-close within the range instead:")
rev=v[v.ret_inside_close_min>=0]
print(f"  n={len(rev)}; of these, fraction that later reach the OPPOSITE edge: {100*(rev.opp_edge_touch_min>=0).mean():.1f}%")
print(f"  fraction that instead resume in the ORIGINAL break direction to a new extreme:")
resume=rev.apply(lambda r: r.mfe_R_EOD> max(r.mae_R_EOD,0), axis=1)
print(f"    {100*resume.mean():.1f}%  -> return-inside does NOT reliably mean reversal")
