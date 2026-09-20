#!/usr/bin/env python3
"""
LOSS FORENSICS II — what happened BEFORE the stop was hit.
Pre-registered 2026-09-17 before measurement. Analyst Agent.

Built on the HONEST fill (convention B: the limit rests in the tolerance band) and
REGISTERED round-trip costs. Everything earlier than this used a fill at a price that
often never traded, so the previous loss study is superseded.

WHY THE OLD TAXONOMY WAS USELESS
  Entry sits at the range edge and the stop at edge - 0.5*W, which IS the opening-range
  midline. Every stop-out is therefore a "range recapture" by construction, and 95% of
  losses landed in one bucket. This study only uses axes that are free to vary.

RECORDED FOR EVERY TRADE, bar by bar from entry to exit
  mfe_R, mae_R          favourable / adverse excursion in R
  t_mfe                 minutes from entry to the favourable extreme
  pre_stop_path         the ordered 1-minute closes between entry and exit
  cross_n               how many times price crossed back through the entry price
  term_bar_R            the range of the bar that finally hit the stop, in R
  term_gap_R            how far THROUGH the stop that bar opened (slippage exposure)
  ambig                 stop and target both inside the same 1-minute bar
  stall_min             minutes spent within +/-0.1R of entry before the first real move
  armed                 whether the +1R trail was ever armed
  recov_R               AFTER the stop: the best excursion in the trade's original
                        direction, within the remaining hold window. This is the
                        "would a wider stop have saved it" measurement.
  mae_at_mfe            how much heat was taken before the favourable extreme
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E

R0=9*60+30; L=30; TOL=.10; STOPF=.50; MAXWAIT=60; MAXHOLD=180
TP_MIN,TP_CAP=2.,4.
COST={'NAS100':2.92,'US500':1.26,'XAUUSD':0.75}
GATE=0.15

def build(inst, gate=GATE):
    raw=mdload.load(inst); df=E.prep(raw); cost=COST[inst]; r1=R0+L; rows=[]
    for day,g in df.groupby("day",sort=True):
        m=g.m.values;o=g.open.values;h=g.high.values;l=g.low.values;c=g.close.values
        rm=(m>=R0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
        if W<=0: continue
        if gate and cost/(STOPF*W) > gate: continue
        post=m>=r1
        if post.sum()<60: continue
        pm=m[post]-r1; po=o[post]; ph=h[post]; pl=l[post]; pc=c[post]
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
        px = edge if reached else edge+dr*tol          # convention B
        stop = edge - dr*STOPF*W; R=abs(px-stop)
        if R<=0: continue
        ext=ph[:ei+1].max() if dr==1 else pl[:ei+1].min(); dist=(ext-px)*dr
        tp=px+dr*min(max(dist/R,TP_MIN),TP_CAP)*R
        # ---------------- walk forward, recording the path ----------------
        t0=pm[ei]; ex=exr=None; be=False; trail=stop
        mfe=mae=0.; t_mfe=0; cross=0; last_side=0
        stall=0; term=ei; ambig=0; mae_at_mfe=0.
        for j in range(ei,len(pm)):
            term=j
            if pm[j]-t0>MAXHOLD: ex,exr=pc[j],"time"; break
            fav=(ph[j]-px)*dr if dr==1 else (px-pl[j])
            fav=(ph[j]-px) if dr==1 else (px-pl[j])
            adv=(px-pl[j]) if dr==1 else (ph[j]-px)
            if fav>mfe: mfe=fav; t_mfe=int(pm[j]-t0); mae_at_mfe=mae
            mae=max(mae,adv)
            side=1 if (pc[j]-px)*dr>0 else -1
            if last_side!=0 and side!=last_side: cross+=1
            last_side=side
            if abs(pc[j]-px)<=0.10*R: stall+=1
            hs=(pl[j]<=trail) if dr==1 else (ph[j]>=trail)
            ht=(ph[j]>=tp) if dr==1 else (pl[j]<=tp)
            if hs and ht: ambig=1; ex,exr=trail,"ambig"; break
            if hs: ex,exr=trail,("trailstop" if be else "stop"); break
            if ht: ex,exr=tp,"target"; break
            if fav>=R:
                be=True; nt=(ph[j]-R) if dr==1 else (pl[j]+R)
                trail=max(trail,nt,px) if dr==1 else min(trail,nt,px)
        if ex is None: ex,exr=pc[-1],"eod"
        gross=((ex-px)*dr)/R; net=gross-cost/R
        # terminal bar character
        term_bar_R=(ph[term]-pl[term])/R
        term_gap_R=max(0.,((trail-po[term])*dr if dr==-1 else (po[term]-trail)*dr))/R
        term_gap_R=abs(min(0.,(po[term]-trail)*dr))/R if exr in("stop","trailstop","ambig") else 0.
        # would a wider stop have saved it? best excursion AFTER the exit bar,
        # within what remained of the 180-minute window
        recov=np.nan
        if exr in ("stop","ambig"):
            rest=[k for k in range(term+1,len(pm)) if pm[k]-t0<=MAXHOLD]
            if rest:
                bext=ph[rest].max() if dr==1 else pl[rest].min()
                recov=((bext-px)*dr)/R
        rows.append(dict(date=str(pd.Timestamp(day).date()),inst=inst,dir=dr,W=W,R_pts=R,
            reached=int(reached),entry=px,exit_reason=exr,gross=gross,net=net,
            mfe_R=mfe/R,mae_R=mae/R,t_mfe=t_mfe,hold=int(pm[term]-t0),
            cross_n=cross,stall_min=stall,armed=int(be),ambig=ambig,
            term_bar_R=term_bar_R,term_gap_R=term_gap_R,recov_R=recov,
            mae_at_mfe_R=mae_at_mfe/R,cost_R=cost/R,
            lat=int(pm[ei]-conf)))
    d=pd.DataFrame(rows); d['yr']=d.date.str[:4].astype(int)
    return d
