#!/usr/bin/env python3
"""Loss forensics — rich ledger + mutually exclusive loss taxonomy."""
import numpy as np, pandas as pd, mdload, exp_matrix as E
R0=9*60+30; L=30; SEND=16*60; TOL=.10; STOPF=.50; MAXHOLD=180; MAXWAIT=60
def cost(r): return .25+.25+.25+(.25 if r in("stop","trailstop") else 0)+(2*2.50)/20.

def build(inst="NAS100"):
    raw=mdload.load(inst); df=E.prep(raw); r1=R0+L; rows=[]
    prev_close={}
    for day,g in df.groupby("day",sort=True):
        m,o,h,l,c=g.m.values,g.open.values,g.high.values,g.low.values,g.close.values
        rm=(m>=R0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol; mid=(oh+ol)/2
        if W<=0: continue
        post=m>=r1
        if post.sum()<60: continue
        pm,ph,pl,pc=m[post]-r1,h[post],l[post],c[post]
        b=pm//L; sk=-1;dr=0
        for k in range(int(b.max())+1):
            s=b==k
            if not s.any(): continue
            if pc[s][-1]>oh: sk,dr=k,1;break
            if pc[s][-1]<ol: sk,dr=k,-1;break
        if sk<0: continue
        conf=(sk+1)*L; edge=oh if dr==1 else ol; tol=TOL*W
        after=np.where(pm>=conf)[0]
        rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
        if not rt: continue
        ei=rt[0]; lat=int(pm[ei]-conf)
        if lat>MAXWAIT: continue                       # the agreed 60-minute rule
        if ei>=len(pm)-5: continue
        wimp=(pm>=conf)&(np.arange(len(pm))<=ei)
        imp=ph[wimp].max() if dr==1 else pl[wimp].min()
        # ORB candle shape
        orb_o,orb_c=o[rm][0],c[rm][-1]
        # pre-entry realised movement (cumulative abs 1m travel from range end to entry)
        trav=np.abs(np.diff(pc[:ei+1])).sum() if ei>0 else 0.0
        px=edge; stop=px-dr*STOPF*W; R=abs(px-stop)
        if R<=0: continue
        ext=ph[:ei+1].max() if dr==1 else pl[:ei+1].min(); dist=(ext-px)*dr
        tp=px+dr*min(max(dist/R,2.),4.)*R
        t0=pm[ei]; ex=exr=None; be=False; trail=stop; mfe=0.; mae=0.
        recap=False; recap_t=-1
        for j in range(ei,len(pm)):
            if pm[j]-t0>MAXHOLD: ex,exr=pc[j],"time";break
            fav=(ph[j]-px) if dr==1 else (px-pl[j]); adv=(px-pl[j]) if dr==1 else (ph[j]-px)
            mfe=max(mfe,fav); mae=max(mae,adv)
            if not recap and (ol<=pc[j]<=oh): recap=True; recap_t=int(pm[j]-t0)
            hs=(pl[j]<=trail) if dr==1 else (ph[j]>=trail)
            ht=(ph[j]>=tp) if dr==1 else (pl[j]<=tp)
            if hs and ht: ex,exr=trail,"ambig";break
            if hs: ex,exr=trail,("trailstop" if be else "stop");break
            if ht: ex,exr=tp,"target";break
            if fav>=R:
                be=True; nt=(ph[j]-R) if dr==1 else (pl[j]+R)
                trail=max(trail,nt,px) if dr==1 else min(trail,nt,px)
        if ex is None: ex,exr=pc[-1],"eod"
        gross=((ex-px)*dr)/R; net=gross-cost(exr)/R
        rows.append(dict(date=str(pd.Timestamp(day).date()),dir=dr,W=W,R_pts=R,
            entry_clock=int(r1+conf+lat),conf_min=conf,lat=lat,
            mfe_R=mfe/R,mae_R=mae/R,imp_R=abs(imp-px)/R,net=net,gross=gross,exr=exr,
            be_armed=int(be),recap=int(recap),recap_t=recap_t,
            orb_body=abs(orb_c-orb_o)/W, orb_dir=int(np.sign(orb_c-orb_o)),
            travel_W=trav/W, hold=int(pm[min(j,len(pm)-1)]-t0),
            both_edges=int((ph[:ei+1].max()>oh) and (pl[:ei+1].min()<ol))))
    d=pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    d["W_med20"]=d.W.rolling(20,min_periods=10).median().shift(1)
    d["W_rel"]=d.W/d.W_med20
    d["yr"]=d.date.str[:4].astype(int)
    d["dow"]=pd.to_datetime(d.date).dt.dayofweek
    return d

def classify(r):
    """Mutually exclusive, priority-ordered."""
    if r.net>=0.05: return "WIN"
    if abs(r.net)<0.05: return "SCRATCH"
    if r.exr in ("time","eod"): return "L5 time drift"
    if r.be_armed==1:           return "L4 trail give-back"
    if r.recap==1:              return "L3 range recapture"
    if r.mfe_R<0.25:            return "L1 instant rejection"
    return "L2 stall and fade"
