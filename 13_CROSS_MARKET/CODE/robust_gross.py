#!/usr/bin/env python3
"""Is the +0.046R gross edge real, or is it a product of the selected gate?
Also: the ONE entry geometry with no fill ambiguity at all.

A1  retest entry, UNGATED, all 5 instruments  -> is gross still ~+0.046R?
A2  immediate entry at the CLOSE of the confirming block. No retest, no tolerance,
    no fill ambiguity: that close is a price that definitely traded. Stop and target
    scaled off W exactly as before.
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E
R0=9*60+30; L=30; TOL=.10; STOPF=.50; MAXWAIT=60; MAXHOLD=180
TP_MIN,TP_CAP=2.,4.
COST={'NAS100':2.92,'US500':1.26,'XAUUSD':0.75,'EURUSD':0.00027,'GBPUSD':0.00049}

def walk(px,dr,R,tp,ph,pl,pc,pm,ei,stop0):
    t0=pm[ei]; trail=stop0; be=False
    for j in range(ei,len(pm)):
        if pm[j]-t0>MAXHOLD: return ((pc[j]-px)*dr)/R,"time"
        fav=(ph[j]-px) if dr==1 else (px-pl[j])
        hs=(pl[j]<=trail) if dr==1 else (ph[j]>=trail)
        ht=(ph[j]>=tp) if dr==1 else (pl[j]<=tp)
        if hs and ht: return ((trail-px)*dr)/R,"ambig"
        if hs: return ((trail-px)*dr)/R,("trailstop" if be else "stop")
        if ht: return ((tp-px)*dr)/R,"target"
        if fav>=R:
            be=True; nt=(ph[j]-R) if dr==1 else (pl[j]+R)
            trail=max(trail,nt,px) if dr==1 else min(trail,nt,px)
    return ((pc[-1]-px)*dr)/R,"eod"

def build(inst):
    raw=mdload.load(inst); df=E.prep(raw); cost=COST[inst]; r1=R0+L; A=[]; B=[]
    for day,g in df.groupby("day",sort=True):
        m=g.m.values;h=g.high.values;l=g.low.values;c=g.close.values
        rm=(m>=R0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
        if W<=0: continue
        post=m>=r1
        if post.sum()<60: continue
        pm=m[post]-r1; ph=h[post]; pl=l[post]; pc=c[post]
        b=pm//L; sk=-1; dr=0
        for k in range(int(b.max())+1):
            s=b==k
            if not s.any(): continue
            if pc[s][-1]>oh: sk,dr=k,1;break
            if pc[s][-1]<ol: sk,dr=k,-1;break
        if sk<0: continue
        conf=(sk+1)*L; edge=oh if dr==1 else ol; tol=TOL*W
        after=np.where(pm>=conf)[0]
        if len(after)==0: continue
        ci=after[0]; D=str(pd.Timestamp(day).date())
        # ---------- A2: immediate at the confirming block's close ----------
        bs=(b==sk); px2=pc[bs][-1]; ei2=ci
        if ei2<len(pm)-5:
            stop2=edge-dr*STOPF*W; R2=abs(px2-stop2)
            if R2>0:
                ext=ph[:ei2+1].max() if dr==1 else pl[:ei2+1].min(); dist=(ext-px2)*dr
                tp2=px2+dr*min(max(dist/R2,TP_MIN),TP_CAP)*R2
                gr,er=walk(px2,dr,R2,tp2,ph,pl,pc,pm,ei2,stop2)
                B.append(dict(date=D,inst=inst,dir=dr,W=W,R_pts=R2,gross=gr,
                              net=gr-cost/R2,exit_reason=er,cost_R=cost/R2))
        # ---------- A1: retest entry, ungated, honest fill ----------
        rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
        if not rt: continue
        ei=rt[0]
        if int(pm[ei]-conf)>MAXWAIT or ei>=len(pm)-5: continue
        reached=(pl[ei]<=edge) if dr==1 else (ph[ei]>=edge)
        px=edge if reached else edge+dr*tol
        stop=edge-dr*STOPF*W; R=abs(px-stop)
        if R<=0: continue
        ext=ph[:ei+1].max() if dr==1 else pl[:ei+1].min(); dist=(ext-px)*dr
        tp=px+dr*min(max(dist/R,TP_MIN),TP_CAP)*R
        gr,er=walk(px,dr,R,tp,ph,pl,pc,pm,ei,stop)
        A.append(dict(date=D,inst=inst,dir=dr,W=W,R_pts=R,gross=gr,net=gr-cost/R,
                      exit_reason=er,cost_R=cost/R,reached=int(reached)))
    a=pd.DataFrame(A); b_=pd.DataFrame(B)
    for d in (a,b_): d['yr']=d.date.str[:4].astype(int)
    return a,b_
