#!/usr/bin/env python3
"""EXIT POLICY SWEEP — motivated by LOSS FORENSICS II.
Pre-registered 2026-09-17 before measurement.

The loss study says the losses are not the fixable part: only 39% of stopped trades ever
recover to breakeven inside the remaining window and the median post-stop excursion is
-0.285R, so a wider stop does not rescue them. What it does say is that 488 trades reached
a mean favourable excursion of 1.399R and were trailed out at +0.399R -- a full 1R given
back -- while only 10.8% of the book ever reaches the 2R target.

So: hold ENTRY and STOP fixed (convention B fill, registered costs, cost/R <= 0.15 gate)
and vary only what happens after the trade is working.

POLICIES
  V0  current: target = next extreme floored 2R capped 4R; trail = extreme - 1.0R from +1R
  V1  same, trail tightened to extreme - 0.5R
  V2  same, trail tightened to extreme - 0.25R
  V3  hard take-profit at +1.0R, nothing else
  V4  hard take-profit at +1.5R
  V5  hard take-profit at +2.0R
  V6  half off at +1.0R, remainder trailed at extreme - 0.5R (exit cost charged 1.5x)
  V7  stop to breakeven at +1R, no trail, run to the 2R-4R target
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E
R0=9*60+30; L=30; TOL=.10; STOPF=.50; MAXWAIT=60; MAXHOLD=180
TP_MIN,TP_CAP=2.,4.
COST={'NAS100':2.92,'US500':1.26,'XAUUSD':0.75}
GATE=0.15
POLICIES=["V0","V1","V2","V3","V4","V5","V6","V7"]

def _walk(pol,px,dr,R,tp,ph,pl,pc,pm,ei,stop0):
    """returns (gross_R, exit_reason, cost_multiplier)"""
    t0=pm[ei]; trail=stop0; armed=False; part=False; part_R=0.
    give={"V0":1.0,"V1":0.5,"V2":0.25,"V6":0.5}.get(pol,None)
    hard={"V3":1.0,"V4":1.5,"V5":2.0}.get(pol,None)
    cm=1.0
    for j in range(ei,len(pm)):
        if pm[j]-t0>MAXHOLD:
            g=((pc[j]-px)*dr)/R
            return (part_R+0.5*g if part else g),"time",cm
        fav=(ph[j]-px) if dr==1 else (px-pl[j])
        hs=(pl[j]<=trail) if dr==1 else (ph[j]>=trail)
        # --- hard TP policies
        if hard is not None:
            ht=(ph[j]>=px+dr*hard*R) if dr==1 else (pl[j]<=px+dr*hard*R)
            if hs and ht: return ((trail-px)*dr)/R,"ambig",cm
            if hs: return ((trail-px)*dr)/R,("stop" if not armed else "trailstop"),cm
            if ht: return hard,"target",cm
            continue
        # --- target + trail policies
        ht=(ph[j]>=tp) if dr==1 else (pl[j]<=tp)
        if hs and ht: 
            g=((trail-px)*dr)/R
            return (part_R+0.5*g if part else g),"ambig",cm
        if hs:
            g=((trail-px)*dr)/R
            return (part_R+0.5*g if part else g),("trailstop" if armed else "stop"),cm
        if ht:
            g=((tp-px)*dr)/R
            return (part_R+0.5*g if part else g),"target",cm
        if pol=="V6" and not part and fav>=1.0*R:
            part=True; part_R=0.5*1.0; cm=1.5
        if fav>=1.0*R:
            armed=True
            if pol=="V7":
                trail=max(trail,px) if dr==1 else min(trail,px)
            else:
                nt=(ph[j]-give*R) if dr==1 else (pl[j]+give*R)
                trail=max(trail,nt,px) if dr==1 else min(trail,nt,px)
    g=((pc[-1]-px)*dr)/R
    return (part_R+0.5*g if part else g),"eod",cm

def build(inst):
    raw=mdload.load(inst); df=E.prep(raw); cost=COST[inst]; r1=R0+L; rows=[]
    for day,g in df.groupby("day",sort=True):
        m=g.m.values;h=g.high.values;l=g.low.values;c=g.close.values
        rm=(m>=R0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
        if W<=0 or cost/(STOPF*W)>GATE: continue
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
        rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
        if not rt: continue
        ei=rt[0]
        if int(pm[ei]-conf)>MAXWAIT or ei>=len(pm)-5: continue
        reached=(pl[ei]<=edge) if dr==1 else (ph[ei]>=edge)
        px=edge if reached else edge+dr*tol
        stop0=edge-dr*STOPF*W; R=abs(px-stop0)
        if R<=0: continue
        ext=ph[:ei+1].max() if dr==1 else pl[:ei+1].min(); dist=(ext-px)*dr
        tp=px+dr*min(max(dist/R,TP_MIN),TP_CAP)*R
        rec=dict(date=str(pd.Timestamp(day).date()),inst=inst,R_pts=R,cost_R=cost/R)
        for pol in POLICIES:
            gr,er,cm=_walk(pol,px,dr,R,tp,ph,pl,pc,pm,ei,stop0)
            rec[f"g_{pol}"]=gr; rec[f"n_{pol}"]=gr-cm*cost/R; rec[f"r_{pol}"]=er
        rows.append(rec)
    d=pd.DataFrame(rows); d["yr"]=d.date.str[:4].astype(int); return d
