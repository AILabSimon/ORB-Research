#!/usr/bin/env python3
"""TSUGI v6 — the tradeable form of the edge-interaction hypothesis.

The v5 result showed that most of the apparent edge-interaction signal lived in
the ENTRY BAR ITSELF, which a touch-triggered entry cannot observe. The only way
to use it is to stop entering on the touch and instead enter on the CLOSE of the
retest bar, having seen its shape. That costs entry price and one minute of
delay; this tests whether the information is worth the cost.

ARMS (all share the frozen CM-C1 spec otherwise):
  arm0  baseline: enter at the ORB edge on the touch                [control]
  arm1  enter at the CLOSE of the retest bar, unconditional         [isolates the delay cost]
  arm1 is then split on the retest bar's own body:
        ebar_sb=0  body does NOT span the edge -> "closed cleanly outside"
        ebar_sb=1  body DOES span the edge     -> "in and out in the same candle"
  Simon's hypothesis predicts ebar_sb=1 is the WINNING subset.

Stop stays structural: edge - 0.5*W (same absolute level as the baseline), so a
worse entry gives a smaller R, which is charged honestly.
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E
from tsugi_test import _walk, COSTS, R0, L, TOL, STOPF, MAXWAIT

def build(inst, tz="America/New_York", r0=R0):
    raw=mdload.load(inst); df=E.prep(raw,tz=tz,r0=r0)
    cost_pts=COSTS[inst]; r1=r0+L; a0=[]; a1=[]
    for day,g in df.groupby("day",sort=True):
        m=g.m.values;o=g.open.values;h=g.high.values;l=g.low.values;c=g.close.values
        rm=(m>=r0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
        if W<=0: continue
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
        ei=rt[0]; lat=int(pm[ei]-conf)
        if lat>MAXWAIT or ei>=len(pm)-6: continue
        D=str(pd.Timestamp(day).date())
        stop_lvl=edge-dr*STOPF*W
        r=_walk(edge,dr,W,ph,pl,pc,pm,ei,abs(edge-stop_lvl),cost_pts)
        if r: r.update(date=D,inst=inst,dir=dr,W=W,lat=lat,arm="arm0"); a0.append(r)
        # --- arm1: act on the retest bar's CLOSE, one bar later ---
        px=pc[ei]
        sd=abs(px-stop_lvl)
        if sd<=0: continue
        bl,bh=min(po[ei],pc[ei]),max(po[ei],pc[ei])
        sb=int(bl<=edge<=bh)
        sw=int(pl[ei]<=edge<=ph[ei])
        # entry takes effect from the NEXT bar
        r=_walk(px,dr,W,ph,pl,pc,pm,ei+1,sd,cost_pts)
        if r:
            r.update(date=D,inst=inst,dir=dr,W=W,lat=lat,arm="arm1",
                     ebar_sb=sb,ebar_sw=sw,slip_W=(px-edge)*dr/W)
            a1.append(r)
    return pd.DataFrame(a0),pd.DataFrame(a1)
