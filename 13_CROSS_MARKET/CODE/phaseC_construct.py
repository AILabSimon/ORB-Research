#!/usr/bin/env python3
"""PHASE C - trade construction on cells that passed the Phase-B behavioural gate AND the
Phase-C cost/R gate. Path asymmetry is NOT expectancy; this converts behaviour into trades.
Entry families: TOUCH (first wick beyond the edge) and RETEST (return to within 0.10W of the
broken edge after a completed close outside). Stops: opposite edge (R=W) and midpoint (R=0.5W).
Exits: fixed 2R, fixed 3R, and trail-from-1R. Hard time exit 180 min. Same-bar conflicts resolved
AGAINST the trade (conservative) and flagged."""
import os, sys, json
import numpy as np, pandas as pd
SH=os.path.expanduser("~/mnt/Dukascopy")
BR=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/13_CROSS_MARKET")
CFG={
 "NAS100": dict(f="NAS100_1m.csv", tz="America/New_York", unit=1.0, ev={"CASH0930":570}, send=960, cost_cfd=2.920, cost_fut=1.250, futname="NQ"),
 "US500" : dict(f="US500_1m.csv",  tz="America/New_York", unit=1.0, ev={"CASH0930":570}, send=960, cost_cfd=1.260, cost_fut=1.100, futname="ES"),
 "XAUUSD": dict(f="XAUUSD_1m.csv", tz="America/New_York", unit=1.0, ev={"COMEX0820":500,"CASH0930":570}, send=960, cost_cfd=0.750, cost_fut=0.450, futname="GC"),
 "EURUSD": dict(f="EURUSD_1M.csv", tz="Europe/London",   unit=0.0001,ev={"LON0800":480}, send=1020, cost_cfd=2.700, cost_fut=None, futname=None),
 "GBPUSD": dict(f="GBPUSD_1M.csv", tz="Europe/London",   unit=0.0001,ev={"LON0800":480}, send=1020, cost_cfd=4.900, cost_fut=None, futname=None),
}
_C={}
def load(mk):
    if mk in _C: return _C[mk]
    c=CFG[mk]; d=pd.read_csv(os.path.join(SH,c["f"]),usecols=["timestamp","open","high","low","close"])
    d["timestamp"]=pd.to_datetime(d["timestamp"],utc=True).dt.tz_convert(c["tz"])
    bad=((d.high<d[["open","close"]].max(axis=1))|(d.low>d[["open","close"]].min(axis=1))|(d.high<d.low)); d=d[~bad]
    for x in ["open","high","low","close"]: d[x]=d[x]/c["unit"]
    d["m"]=d.timestamp.dt.hour*60+d.timestamp.dt.minute; d["dt"]=d.timestamp.dt.normalize()
    d=d[d.timestamp.dt.dayofweek<5].reset_index(drop=True); _C[mk]=d; return d

def run(mk,ev,L,family,stop_frac,exit_mode,delay=0):
    c=CFG[mk]; d=load(mk); r0=c["ev"][ev]; r1=r0+L; send=c["send"]; tr=[]
    for dt,g in d.groupby("dt",sort=True):
        m=g.m.values;h=g.high.values;l=g.low.values;cl=g.close.values
        rm=(m>=r0)&(m<r1)
        if rm.sum()<L: continue
        oh=h[rm].max(); ol=l[rm].min(); W=oh-ol; mid=(oh+ol)/2
        if W<=0: continue
        post=(m>=r1)&(m<send)
        if post.sum()<60: continue
        pm=m[post]-r1; ph=h[post]; pl=l[post]; pc=cl[post]
        b=pm//L
        if family=="touch":
            ta=np.where(ph>oh)[0]; tb=np.where(pl<ol)[0]
            if not len(ta) and not len(tb): continue
            i0=ta[0] if (len(ta) and (not len(tb) or ta[0]<=tb[0])) else tb[0]
            d_=1 if (len(ta) and (not len(tb) or ta[0]<=tb[0])) else -1
            edge=oh if d_==1 else ol; ei=i0
        else:  # retest
            sk=-1;d_=0
            for k in range(int(b.max())+1):
                s=b==k
                if not s.any(): continue
                v=pc[s][-1]
                if v>oh: sk,d_=k,1;break
                if v<ol: sk,d_=k,-1;break
            if sk<0: continue
            edge=oh if d_==1 else ol
            sel=np.where(pm>=(sk+1)*L)[0]
            if not len(sel): continue
            rt=[i for i in sel if ((pl[i]<=edge+0.10*W) if d_==1 else (ph[i]>=edge-0.10*W))]
            if not rt: continue
            ei=rt[0]
        ei=ei+delay
        if ei>=len(pm)-5: continue
        entry=edge
        stop = entry - d_*stop_frac*W
        Rp=abs(entry-stop)
        if Rp<=0: continue
        t0=pm[ei]; ex=None; exr=None; mfe=0.0; be=False; trail=stop
        for j in range(ei,len(pm)):
            if pm[j]-t0>180: ex=pc[j]; exr="time"; break
            fav=(ph[j]-entry)*d_ if d_==1 else (entry-pl[j])
            fav=(ph[j]-entry) if d_==1 else (entry-pl[j])
            mfe=max(mfe,fav)
            hit_stop=(pl[j]<=trail) if d_==1 else (ph[j]>=trail)
            if exit_mode in ("2R","3R"):
                T=2.0 if exit_mode=="2R" else 3.0
                hit_t=fav>=T*Rp
                if hit_stop and hit_t: ex=trail; exr="ambig"; break
                if hit_stop: ex=trail; exr="stop"; break
                if hit_t: ex=entry+d_*T*Rp; exr="target"; break
            else:  # trail from +1R: once +1R, stop to breakeven, then trail 1R behind the high
                if hit_stop: ex=trail; exr=("trailstop" if be else "stop"); break
                if fav>=Rp:
                    be=True
                    nt=(ph[j]-Rp) if d_==1 else (pl[j]+Rp)
                    trail = max(trail,nt) if d_==1 else min(trail,nt)
                    trail = max(trail,entry) if d_==1 else min(trail,entry)
        if ex is None: ex=pc[-1]; exr="eod"
        tr.append(dict(date=str(pd.Timestamp(dt).date()),mk=mk,ev=ev,L=L,fam=family,
            stop_frac=stop_frac,exit=exit_mode,dir=d_,W=W,R_pts=Rp,gross_R=((ex-entry)*d_)/Rp,
            mfe_R=mfe/Rp,exit_reason=exr,entry_min=int(t0),hold=int(pm[min(j,len(pm)-1)]-t0)))
    return pd.DataFrame(tr)

def rep(t,lbl,cost,yr_split=2021):
    if len(t)<50: print(f"  {lbl:52s} n={len(t)} too few"); return None
    rng=np.random.default_rng(9)
    net=t.gross_R.values-cost/t.R_pts.values
    bs=np.array([rng.choice(net,len(net),True).mean() for _ in range(2000)])
    t=t.copy(); t["yr"]=t.date.str[:4].astype(int); t["net"]=net
    dv=t[t.yr<=yr_split].net.mean(); ho=t[t.yr>yr_split].net.mean()
    eq=np.cumsum(net); dd=float(np.max(np.maximum.accumulate(eq)-eq))
    print(f"  {lbl:52s} n={len(t):5d} {len(t)/12.5:5.1f}/yr medR={t.R_pts.median():7.2f} "
          f"win={100*(t.gross_R>0).mean():4.1f}% gross={t.gross_R.mean():+.3f} NET={net.mean():+.3f} "
          f"CI[{np.percentile(bs,2.5):+.3f},{np.percentile(bs,97.5):+.3f}] dev={dv:+.3f} hold={ho:+.3f} maxDD={dd:.1f}R")
    return dict(lbl=lbl,n=len(t),net=float(net.mean()),lo=float(np.percentile(bs,2.5)),
                hi=float(np.percentile(bs,97.5)),dev=float(dv),hold=float(ho),dd=dd,
                medR=float(t.R_pts.median()),win=float(100*(t.gross_R>0).mean()))
