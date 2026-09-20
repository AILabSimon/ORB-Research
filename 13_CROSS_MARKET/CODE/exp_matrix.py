#!/usr/bin/env python3
"""EXP-MATRIX — 15m vs 30m opening range, close vs body-close direction,
immediate vs print-through-confirmed entry, with the 2R-min / next-extreme / 4R-cap target."""
import numpy as np, pandas as pd

R0_DEFAULT=9*60+30; SEND=16*60; MAXHOLD=180; TOL=0.10; STOPF=0.50
TP_MIN, TP_CAP = 2.0, 4.0
NQ = dict(pv=20.0, comm=2.50, spr=0.25, es=0.25, xs=0.25, sx=0.25)
def rt_cost(exit_reason):
    c = NQ["spr"]+NQ["es"]+NQ["xs"]+(NQ["sx"] if exit_reason in ("stop","trailstop") else 0.0)
    return c + (2*NQ["comm"])/NQ["pv"]

def prep(df,tz="America/New_York",r0=R0_DEFAULT,send=SEND):
    d=df.copy(); d["timestamp"]=pd.to_datetime(d["timestamp"],utc=True)
    loc=d["timestamp"].dt.tz_convert(tz)
    d["m"]=loc.dt.hour*60+loc.dt.minute; d["day"]=loc.dt.normalize()
    return d[(loc.dt.dayofweek<5)&(d.m>=r0)&(d.m<send)]

def run(df, L=30, direction="close", entry="immediate", r0=R0_DEFAULT, cost_fn=None):
    R0=r0; r1=R0+L; tr=[]
    for day,g in df.groupby("day",sort=True):
        m,o,h,l,c = g.m.values,g.open.values,g.high.values,g.low.values,g.close.values
        rm=(m>=R0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
        if W<=0: continue
        post=m>=r1
        if post.sum()<60: continue
        pm,ph,pl,pc,po = m[post]-r1,h[post],l[post],c[post],o[post]
        b=pm//L
        # --- direction: first L-bar qualifying outside ---
        sk,dr=-1,0
        for k in range(int(b.max())+1):
            s=b==k
            if not s.any(): continue
            cc, oo = pc[s][-1], po[s][0]
            if direction=="close":
                if cc>oh: sk,dr=k,1;break
                if cc<ol: sk,dr=k,-1;break
            else:  # body_close: the ENTIRE body outside
                if min(oo,cc)>oh: sk,dr=k,1;break
                if max(oo,cc)<ol: sk,dr=k,-1;break
        if sk<0: continue
        edge = oh if dr==1 else ol
        # --- retest touch ---
        after=np.where(pm>=(sk+1)*L)[0]; tol=TOL*W
        rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
        if not rt: continue
        ti=rt[0]
        # --- entry ---
        if entry=="immediate":
            ei, px = ti, edge
        else:  # confirmed: next candle trading beyond the PREVIOUS candle's extreme (R-009 print-through)
            ei=None
            for j in range(ti+1, min(ti+60, len(pm))):
                trig = ph[j-1] if dr==1 else pl[j-1]
                if (ph[j]>trig) if dr==1 else (pl[j]<trig): ei,px=j,trig; break
            if ei is None: continue
        if ei>=len(pm)-5: continue
        stop = px - dr*STOPF*W; R=abs(px-stop)
        if R<=0: continue
        # --- target: next extreme beyond entry, floored 2R capped 4R ---
        hist=slice(0,ei+1)
        ext = ph[hist].max() if dr==1 else pl[hist].min()
        dist = (ext-px)*dr
        tp_R = min(max(dist/R, TP_MIN), TP_CAP) if dist>0 else TP_MIN
        tp = px + dr*tp_R*R
        # --- walk forward ---
        t0=pm[ei]; ex=exr=None; be=False; trail=stop; mfe=0.0
        for j in range(ei,len(pm)):
            if pm[j]-t0>MAXHOLD: ex,exr=pc[j],"time"; break
            fav=(ph[j]-px) if dr==1 else (px-pl[j]); mfe=max(mfe,fav)
            hit_s=(pl[j]<=trail) if dr==1 else (ph[j]>=trail)
            hit_t=(ph[j]>=tp) if dr==1 else (pl[j]<=tp)
            if hit_s and hit_t: ex,exr=trail,"ambig"; break      # conservative
            if hit_s: ex,exr=trail,("trailstop" if be else "stop"); break
            if hit_t: ex,exr=tp,"target"; break
            if fav>=R:
                be=True; nt=(ph[j]-R) if dr==1 else (pl[j]+R)
                trail = max(trail,nt,px) if dr==1 else min(trail,nt,px)
        if ex is None: ex,exr=pc[-1],"eod"
        tr.append(dict(date=str(pd.Timestamp(day).date()),dir=dr,W=W,R_pts=R,entry=px,
                       tp_R=tp_R,exit=ex,exit_reason=exr,gross_R=((ex-px)*dr)/R,
                       mfe_R=mfe/R,hold=int(pm[min(j,len(pm)-1)]-t0)))
    return pd.DataFrame(tr)

def summ(t,lbl,rng,cf=None,yrs=10.7):
    if len(t)<60: print(f"  {lbl:44s} n={len(t)} too few"); return None
    cost=np.array([(cf or rt_cost)(r) for r in t.exit_reason]); net=t.gross_R.values-cost/t.R_pts.values
    bs=np.array([rng.choice(net,len(net),True).mean() for _ in range(2500)])
    y=t.date.str[:4].astype(int)
    dev=net[y<=2021].mean(); hol=net[y>2021].mean()
    eq=np.cumsum(net); dd=float(np.max(np.maximum.accumulate(eq)-eq))
    BE=np.abs(net)<0.05
    print(f"  {lbl:44s} n={len(t):5d} {len(t)/yrs:5.0f}/yr net={net.mean():+.4f} "
          f"CI[{np.percentile(bs,2.5):+.4f},{np.percentile(bs,97.5):+.4f}] "
          f"W/L/BE={(net>=.05).sum()}/{(net<=-.05).sum()}/{BE.sum()} "
          f"win={100*(net>=.05).mean():4.1f}% dev={dev:+.3f} hold={hol:+.3f} DD={dd:4.0f}R "
          f"medTP={t.tp_R.median():.2f}R")
    return dict(lbl=lbl,n=len(t),net=net.mean(),lo=np.percentile(bs,2.5),hi=np.percentile(bs,97.5),
                dev=dev,hold=hol,dd=dd,win=100*(net>=.05).mean())
