#!/usr/bin/env python3
"""EXP-010 / MC-3 (F5) - inside-range fade under the compression gate.
Gate   : N consecutive 15m candles with no close outside the ORB (P-6, U-04 resolved = 15m).
Entry  : limit at the ORB boundary on a touch  (R-021: long at ORB low, short at ORB high).
Stop   : ANALYST-OPERATIONALISED from the source's own quantified band - price "stays within about
         15 points on each side" (V12 28:55). Arms: 15 pts, and 0.25 x ORB width.
Targets: ORB midline (R-016) then opposite ORB edge (R-017) - both SOURCE SUPPORTED AND REPEATED.
"""
import numpy as np, pandas as pd, os
import exp008_mc7 as E
def run(N=6, stop_mode="fixed15", stop_pts=15.0, target="opp", max_trades=2, cost=1.75, slip=0.25):
    A=E.sess_map(E.load("NAS100_1m.csv")); tr=[]
    for dt,(m,o,h,l,c) in A.items():
        rm=(m>=570)&(m<585)
        if rm.sum()<15: continue
        oh=h[rm].max(); ol=l[rm].min(); mid=(oh+ol)/2; w=oh-ol
        if w<=0: continue
        post=m>=585; pm=m[post];ph=h[post];pl=l[post];pc=c[post]
        if len(pm)<60: continue
        b=(pm-585)//15; ok=True
        for k in range(N):
            s=b==k
            if not s.any(): ok=False;break
            if pc[s][-1]>oh or pc[s][-1]<ol: ok=False;break
        if not ok: continue
        i0=int(np.argmax(pm>=585+N*15)); n=0; i=i0
        while i<len(pm)-5 and n<max_trades:
            ei=None;d_=0
            for j in range(i,len(pm)):
                if ph[j]>=oh: ei,d_=j,-1;break
                if pl[j]<=ol: ei,d_=j,1;break
            if ei is None: break
            entry=(ol-slip) if d_==1 else (oh+slip)
            sp = stop_pts if stop_mode=="fixed15" else 0.25*w
            stop = entry-sp if d_==1 else entry+sp
            R=abs(entry-stop)
            tgt = mid if target=="mid" else (oh if d_==1 else ol)
            t0=pm[ei]; ex=None;exr=None;mfe=0;mae=0
            for j in range(ei,len(pm)):
                if pm[j]-t0>180: ex=pc[j]; exr="time"; break
                fav=(ph[j]-entry) if d_==1 else (entry-pl[j])
                adv=(entry-pl[j]) if d_==1 else (ph[j]-entry)
                mfe=max(mfe,fav);mae=max(mae,adv)
                hs=(pl[j]<=stop) if d_==1 else (ph[j]>=stop)
                ht=(ph[j]>=tgt) if d_==1 else (pl[j]<=tgt)
                if hs and ht: ex=stop;exr="ambiguous";break
                if hs: ex=stop;exr="stop";break
                if ht: ex=tgt;exr="target";break
            if ex is None: ex=pc[-1];exr="eod"
            g=(ex-entry)*d_
            tr.append(dict(date=str(pd.Timestamp(dt).date()),dir=d_,entry=entry,R_pts=R,
                exit_reason=exr,gross_R=g/R,mfe_R=mfe/R,mae_R=mae/R,orb_w=w,
                tgt_R=abs(tgt-entry)/R,hold=int(pm[min(j,len(pm)-1)]-t0)))
            n+=1; i=j+1
    return pd.DataFrame(tr)

if __name__=="__main__":
    rng=np.random.default_rng(5)
    print("=== EXP-010 / F5 inside-range fade under compression (N=6 fifteen-minute candles) ===")
    for tgt in ["mid","opp"]:
        for sm,sp in [("fixed15",15.0),("qwidth",0)]:
            t=run(N=6,stop_mode=sm,stop_pts=sp,target=tgt)
            if len(t)==0: continue
            net=t.gross_R-1.75/t.R_pts
            bs=np.array([rng.choice(net.values,len(net),True).mean() for _ in range(3000)])
            print(f"  target={tgt:3s} stop={sm:8s} n={len(t):4d} ({len(t)/12.5:.0f}/yr) medR={t.R_pts.median():5.1f}pts "
                  f"tgt_dist={t.tgt_R.median():.2f}R win={100*(t.gross_R>0).mean():4.1f}% "
                  f"grossE={t.gross_R.mean():+.3f}R netE={net.mean():+.3f}R CI[{np.percentile(bs,2.5):+.3f},{np.percentile(bs,97.5):+.3f}]")
    t=run(N=6,target="opp"); t["yr"]=t.date.str[:4].astype(int); t["net"]=t.gross_R-1.75/t.R_pts
    print(f"\n  temporal: dev<=2021 netE={t[t.yr<=2021].net.mean():+.3f}R (n={len(t[t.yr<=2021])}) | holdout>=2022 netE={t[t.yr>=2022].net.mean():+.3f}R (n={len(t[t.yr>=2022])})")
    print(f"  P(MFE>=2R) = {100*(t.mfe_R>=2).mean():.1f}% ; median hold {t.hold.median():.0f} min")
