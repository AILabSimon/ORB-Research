#!/usr/bin/env python3
"""CENSUS-02 (MC-2 / F4a) - failed-breakout reversal, measured FROM THE RETURN POINT.
Completes handoff section 10(c). Behaviour only. Deterministic."""
import os,json,hashlib
import numpy as np, pandas as pd
SH=os.path.expanduser("~/mnt/Dukascopy"); PROJ=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0")
OUT=os.path.join(PROJ,"07_BEHAVIOURAL_CENSUS","RESULTS"); HOR=[5,15,30,60,90,120,180]

def run(inst,fname,tz="America/New_York",r0=570,r1=585):
    p=os.path.join(SH,fname)
    df=pd.read_csv(p,usecols=["timestamp","open","high","low","close"])
    df["timestamp"]=pd.to_datetime(df["timestamp"],utc=True).dt.tz_convert(tz)
    bad=((df.high<df[["open","close"]].max(axis=1))|(df.low>df[["open","close"]].min(axis=1))|(df.high<df.low))
    df=df[~bad]
    df["m"]=df.timestamp.dt.hour*60+df.timestamp.dt.minute; df["d"]=df.timestamp.dt.normalize()
    df=df[(df.timestamp.dt.dayofweek<5)&(df.m>=r0)&(df.m<960)]
    rows=[]
    for d,g in df.groupby("d",sort=True):
        m=g.m.values;hi=g.high.values;lo=g.low.values;cl=g.close.values;op=g.open.values
        rm=(m>=r0)&(m<r1)
        if rm.sum()<(r1-r0): continue
        oh=hi[rm].max(); ol=lo[rm].min(); mid=(oh+ol)/2; w=oh-ol
        if w<=0: continue
        post=m>=r1; mp=m[post];hp=hi[post];lp=lo[post];cp=cl[post]
        b=(mp-r1)//15; nb=int(b.max())+1 if len(b) else 0
        sk=-1;sd=0
        for k in range(nb):
            s=b==k
            if not s.any(): continue
            c=cp[s][-1]
            if c>oh: sk,sd=k,1;break
            if c<ol: sk,sd=k,-1;break
        if sk<0: continue
        # find first 15m bar AFTER the signal bar whose close is back inside
        rk=-1
        for k in range(sk+1,nb):
            s=b==k
            if not s.any(): continue
            c=cp[s][-1]
            if ol<=c<=oh: rk=k;break
        if rk<0: continue
        s=b==rk
        entry=cp[s][-1]                       # reversal entry = close of the return-inside bar
        rev_dir=-sd                           # opposite to the failed break
        # failed-breakout extreme between signal bar start and return bar end (ANALYST CONSTRUCT, U-05)
        span=(b>=sk)&(b<=rk)
        fail_ext = hp[span].max() if sd==1 else lp[span].min()
        Rrev=abs(fail_ext-entry)
        pstart=r1+(rk+1)*15
        sel=mp>=pstart; pm=mp[sel]-pstart; ph=hp[sel]; pl=lp[sel]; pc=cp[sel]
        if len(pm)==0 or Rrev<=0: continue
        fav=(ph-entry) if rev_dir==1 else (entry-pl)
        adv=(entry-pl) if rev_dir==1 else (ph-entry)
        def first(c):
            wi=np.where(c)[0]; return int(pm[wi[0]]) if len(wi) else -1
        r=dict(date=str(pd.Timestamp(d).date()),instrument=inst,orb_width=w,
               break_dir=sd,rev_dir=rev_dir,signal_bar=sk+1,return_bar=rk+1,
               entry=entry,R_rev_pts=Rrev,fail_extreme=fail_ext,
               entry_pos_in_range=(entry-ol)/w,
               dist_mid_pts=abs(entry-mid),dist_opp_pts=abs(entry-(ol if sd==1 else oh)),
               dist_mid_R=abs(entry-mid)/Rrev,dist_opp_R=abs(entry-(ol if sd==1 else oh))/Rrev)
        # source-supported targets (R-016 mid, R-017 opposite edge) - reachable only in rev_dir
        r["t_mid_min"]  = first(pl<=mid) if rev_dir==-1 else first(ph>=mid)
        r["t_opp_min"]  = first(pl<=ol)  if rev_dir==-1 else first(ph>=oh)
        r["t_failext_min"]= first(ph>=fail_ext) if sd==1 else first(pl<=fail_ext)   # stop hit
        for k in (1,2,3): r[f"t_{k}R_min"]=first(fav>=k*Rrev)
        for H in HOR+[10**9]:
            hh="EOD" if H>10**8 else str(H); wsel=pm<H
            if not wsel.any(): r[f"mfe_R_{hh}"]=np.nan; r[f"mae_R_{hh}"]=np.nan; r[f"net_R_{hh}"]=np.nan; continue
            r[f"mfe_R_{hh}"]=fav[wsel].max()/Rrev; r[f"mae_R_{hh}"]=adv[wsel].max()/Rrev
            r[f"net_R_{hh}"]=((pc[wsel][-1]-entry)*rev_dir)/Rrev
        rows.append(r)
    o=pd.DataFrame(rows); os.makedirs(OUT,exist_ok=True)
    o.to_csv(os.path.join(OUT,f"CENSUS02_MC2_{inst}.csv"),index=False)
    print(inst,"reversal events:",len(o))
    return o

if __name__=="__main__":
    run("NAS100","NAS100_1m.csv")
