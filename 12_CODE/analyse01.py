#!/usr/bin/env python3
import pandas as pd, numpy as np, os
pd.set_option("display.width",200)
R=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/07_BEHAVIOURAL_CENSUS/RESULTS")
d=pd.read_csv(os.path.join(R,"CENSUS01_NAS100_ORB0930.csv"))
s=d[d.signal==1].copy()
print("sessions",len(d),"signals",len(s),f"{100*len(s)/len(d):.2f}%")
print("\n=== Q_TIMING: signal bar ordinal (1 = 09:45-10:00) ===")
vc=s.signal_bar.value_counts().sort_index()
cum=vc.cumsum()/len(d)*100
print(pd.DataFrame({"n":vc,"cum% of all sessions":cum.round(1)}).head(12).to_string())
print("\n=== R geometry (R = entry to breached ORB edge) ===")
print(s[["orb_width","R_pts","R_over_width","dist_mid_R","dist_opp_R"]].describe(percentiles=[.1,.25,.5,.75,.9]).round(3).to_string())
print("\n=== Q1/Q2 CORE: MFE vs MAE in R, all signals ===")
for h in ["5","15","30","60","90","120","180","EOD"]:
    f=s[f"mfe_R_{h}"]; a=s[f"mae_R_{h}"]; n=s[f"net_R_{h}"]
    print(f"h={h:>4}  MFE med={f.median():.2f} mean={f.mean():.2f} | MAE med={a.median():.2f} mean={a.mean():.2f} | net med={n.median():+.3f} mean={n.mean():+.3f} | P(MFE>=1R)={100*(f>=1).mean():.1f}% P(MFE>=2R)={100*(f>=2).mean():.1f}% P(MFE>=3R)={100*(f>=3).mean():.1f}%")
print("\n=== CTRL-B symmetry test: is MFE systematically > MAE? ===")
for h in ["30","60","180","EOD"]:
    f=s[f"mfe_R_{h}"];a=s[f"mae_R_{h}"];dd=(f-a).dropna()
    from statistics import NormalDist
    t=dd.mean()/(dd.std()/np.sqrt(len(dd)))
    print(f"h={h:>4} mean(MFE-MAE)={dd.mean():+.3f}R  t={t:+.2f}  P(MFE>MAE)={100*(f>a).mean():.1f}%")
print("\n=== Q3: 180min vs EOD capture ===")
print(f"median MFE 180 / EOD = {s.mfe_R_180.median():.2f} / {s.mfe_R_EOD.median():.2f} = {100*s.mfe_R_180.median()/s.mfe_R_EOD.median():.0f}%")
print(f"P(>=2R) 180 = {100*(s.mfe_R_180>=2).mean():.1f}%   EOD = {100*(s.mfe_R_EOD>=2).mean():.1f}%")
print("\n=== Q4: return inside — touch vs 15m close ===")
rt=s.ret_inside_touch_min; rc=s.ret_inside_close_min
print(f"returned inside by TOUCH at any time: {100*(rt>=0).mean():.1f}%   by 15m CLOSE: {100*(rc>=0).mean():.1f}%")
print(f"median minutes to touch-back {rt[rt>=0].median():.0f}   to close-back {rc[rc>=0].median():.0f}")
print("\n--- race: 2R before return-inside? ---")
for lbl,col in [("TOUCH","ret_inside_touch_min"),("15m CLOSE","ret_inside_close_min")]:
    t2=s.t_2R_min; r_=s[col]
    reach=(t2>=0)&((r_<0)|(t2<r_))
    stopfirst=(r_>=0)&((t2<0)|(r_<t2))
    print(f"stop={lbl:>9}: reached 2R first {100*reach.mean():.1f}% | invalidated first {100*stopfirst.mean():.1f}% | neither {100*(1-reach.mean()-stopfirst.mean()):.1f}%")
    t1=s.t_1R_min; reach1=(t1>=0)&((r_<0)|(t1<r_))
    print(f"            reached 1R first {100*reach1.mean():.1f}%")
print(f"\nsame-bar ambiguity at the 2R touch: {100*s.same_bar_ambiguous_2R.mean():.2f}% of signals")
print("\n=== Q7 MC-2 reversal branch: after returning inside (by 15m close) ===")
rev=s[s.ret_inside_close_min>=0]
print(f"n={len(rev)} ({100*len(rev)/len(s):.1f}% of signals)")
print("of those, subsequently reached (as measured from signal, so a lower bound):")
print(f"  ORB mid : {100*((rev.mid_touch_min>=0)).mean():.1f}%")
print(f"  opposite edge: {100*((rev.opp_edge_touch_min>=0)).mean():.1f}%")
