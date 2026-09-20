#!/usr/bin/env python3
import pandas as pd, numpy as np, os
R=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/07_BEHAVIOURAL_CENSUS/RESULTS")
def load(f): 
    d=pd.read_csv(os.path.join(R,f)); return d,d[d.signal==1].copy()
d,s=load("CENSUS01_NAS100_ORB0930.csv")

SPREAD=1.42   # measured recent-3y median, 09:30-09:45, index points
SLIP=1.0      # analyst assumption
COST=SPREAD+SLIP*2   # entry+exit slippage, round trip, points

print("### A. THE R-GEOMETRY PROBLEM")
print(f"R_pts (entry to ORB edge) percentiles: "+", ".join(f"p{p}={s.R_pts.quantile(p/100):.2f}" for p in [5,10,25,50,75,90]))
print(f"share of signals with R_pts < round-trip cost ({COST:.2f} pts): {100*(s.R_pts<COST).mean():.1f}%")
print(f"share with R_pts < 2x cost: {100*(s.R_pts<2*COST).mean():.1f}%")
print("=> R-multiple MEANS are meaningless (tiny-R tail). All results below are medians/rates,")
print("   and the economic screen R_pts >= 2x round-trip cost is applied where stated.\n")

def race(x, stopcol, target=2.0):
    t=x[f"t_{int(target)}R_min"]; r=x[stopcol]
    win=(t>=0)&((r<0)|(t<r)); lose=(r>=0)&((t<0)|(r<t))
    return win.mean(), lose.mean(), 1-win.mean()-lose.mean()

def exp_gross(x,stopcol,target=2.0):
    w,l,n=race(x,stopcol,target)
    # 'neither' resolved at the 180-min time exit: net_R_180 for those
    t=x[f"t_{int(target)}R_min"]; r=x[stopcol]
    nb=~(((t>=0)&((r<0)|(t<r)))|((r>=0)&((t<0)|(r<t))))
    tail=x.loc[nb,"net_R_180"].clip(-1,target).mean() if nb.any() else 0.0
    return w*target - l*1.0 + n*tail, w,l,n,tail

print("### B. Q1/CTRL-B — does the break carry DIRECTIONAL information?")
print("P(MFE>MAE) from the same entry, same R scaling. 50% = no directional information.")
for h in ["5","15","30","60","90","120","180","EOD"]:
    f=s[f"mfe_R_{h}"];a=s[f"mae_R_{h}"]
    print(f"  h={h:>4}: P(MFE>MAE)={100*(f>a).mean():5.1f}%   median MFE={f.median():.2f}R  median MAE={a.median():.2f}R")

print("\n### C. Q2 — the 2R race, ORB-edge stop (source rule R-012), by stop interpretation")
for lbl,c in [("TOUCH back inside (U-03 strict)","ret_inside_touch_min"),("15m CLOSE back inside (U-03 loose)","ret_inside_close_min")]:
    e,w,l,n,tl=exp_gross(s,c)
    print(f"  {lbl:36s} win2R={100*w:.1f}% lose={100*l:.1f}% unresolved={100*n:.1f}% -> gross E={e:+.3f}R")
print("  NOTE: the loose stop is NOT a 1R loss - it is a variable, larger loss. Its 'gross E' above")
print("        overstates it because the loss is charged at 1R. Measured true loss size below.")
lo=s[(s.ret_inside_close_min>=0)]
print(f"  actual adverse excursion at the moment of a 15m close back inside: median {lo.mae_R_30.median():.2f}R at h=30")

print("\n### D. ECONOMIC SCREEN — only signals where the stop is big enough to trade")
v=s[s.R_pts>=2*COST].copy()
print(f"  viable signals: {len(v)} of {len(s)} ({100*len(v)/len(s):.1f}%) ; median R = {v.R_pts.median():.1f} pts")
e,w,l,n,tl=exp_gross(v,"ret_inside_touch_min")
cost_R=(COST/v.R_pts).median()
print(f"  2R race (touch stop): win={100*w:.1f}% lose={100*l:.1f}% unresolved={100*n:.1f}% -> gross E={e:+.3f}R")
print(f"  median cost as fraction of R = {cost_R:.3f}R  -> NET E ~= {e-cost_R:+.3f}R")
for tgt in [1,2,3]:
    e2,w2,l2,n2,_=exp_gross(v,"ret_inside_touch_min",tgt)
    print(f"    target {tgt}R: win={100*w2:.1f}% gross E={e2:+.3f}R  net~={e2-cost_R:+.3f}R")

print("\n### E. Q5 / CL-012 — Max's own conditioner: opening-range width vs lagged volatility")
v2=v.dropna(subset=["orb_width_rel"]).copy()
v2["q"]=pd.qcut(v2.orb_width_rel,5,labels=["Q1 narrow","Q2","Q3","Q4","Q5 wide"])
for q,g in v2.groupby("q",observed=True):
    e3,w3,l3,n3,_=exp_gross(g,"ret_inside_touch_min")
    c3=(COST/g.R_pts).median()
    print(f"  {q:10s} n={len(g):4d} medR={g.R_pts.median():6.1f}pts  P(MFE>MAE,180)={100*(g.mfe_R_180>g.mae_R_180).mean():5.1f}%  win2R={100*w3:.1f}%  grossE={e3:+.3f}R netE={e3-c3:+.3f}R")

print("\n### F. Q_TIMING — early vs delayed signal (bar 1 = 09:45-10:00)")
for lab,sel in [("bar 1 only",v.signal_bar==1),("bars 2-3",v.signal_bar.isin([2,3])),("bars 4+",v.signal_bar>=4)]:
    g=v[sel]; e4,w4,l4,n4,_=exp_gross(g,"ret_inside_touch_min"); c4=(COST/g.R_pts).median()
    print(f"  {lab:12s} n={len(g):4d} P(MFE>MAE,180)={100*(g.mfe_R_180>g.mae_R_180).mean():5.1f}% win2R={100*w4:.1f}% grossE={e4:+.3f}R netE={e4-c4:+.3f}R")

print("\n### G. CTRL-A — is the 09:30 range special? (pseudo-ORB from the 11:00-11:15 candle)")
dc,sc=load("CENSUS01_NAS100_PSEUDO1100.csv")
vc=sc[sc.R_pts>=2*COST]
for nm,x in [("ORB 09:30 (real)",v),("PSEUDO 11:00 (control)",vc)]:
    e5,w5,l5,n5,_=exp_gross(x,"ret_inside_touch_min"); c5=(COST/x.R_pts).median()
    print(f"  {nm:24s} n={len(x):4d} medR={x.R_pts.median():5.1f} P(MFE>MAE,180)={100*(x.mfe_R_180>x.mae_R_180).mean():5.1f}% win2R={100*w5:.1f}% grossE={e5:+.3f}R netE={e5-c5:+.3f}R")

print("\n### H. Q3 — 180-minute constraint (C-03)")
print(f"  median MFE: 180min={v.mfe_R_180.median():.2f}R  EOD={v.mfe_R_EOD.median():.2f}R  -> 180min captures {100*v.mfe_R_180.median()/v.mfe_R_EOD.median():.0f}%")
print(f"  P(MFE>=2R): 180min={100*(v.mfe_R_180>=2).mean():.1f}%  EOD={100*(v.mfe_R_EOD>=2).mean():.1f}%")
print(f"  median minutes to first 2R touch (when reached): {v.loc[v.t_2R_min>=0,'t_2R_min'].median():.0f}")

print("\n### I. Q7 — MC-2 failed-breakout reversal")
rev=v[v.ret_inside_close_min>=0]
print(f"  n={len(rev)} ({100*len(rev)/len(v):.1f}% of viable signals)")
print(f"  of those, reached ORB mid {100*(rev.mid_touch_min>=0).mean():.1f}%, opposite edge {100*(rev.opp_edge_touch_min>=0).mean():.1f}%")
norev=v[v.ret_inside_close_min<0]
print(f"  BASELINE (no return inside, n={len(norev)}): reached ORB mid {100*(norev.mid_touch_min>=0).mean():.1f}%, opposite edge {100*(norev.opp_edge_touch_min>=0).mean():.1f}%")
