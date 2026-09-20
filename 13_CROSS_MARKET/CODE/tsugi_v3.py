#!/usr/bin/env python3
"""TSUGI v3 — adds the EDGE-INTERACTION (straddle) hypothesis.

PRE-REGISTERED 2026-09-17 BEFORE MEASUREMENT.

HYPOTHESIS (Simon, 2026-09-17):
  Winners are characterised by price RANGING ALONG the ORB edge -- a majority of
  1-minute candles having body and/or wick on BOTH sides of the level in the same
  candle -- before moving away. Losers are characterised by price sitting CLEANLY
  OUTSIDE the level (whole candle, body and wick, beyond the ORB) and then
  returning and running straight to the stop.

MEASUREMENT WINDOW: direction-confirmation bar -> entry bar inclusive. This is
strictly pre-entry, so any rule derived from it is tradeable. A post-entry window
is also recorded but is flagged NON-TRADEABLE and used for description only.

PER-BAR CLASSIFICATION against the edge E, for direction dr:
  straddle_wick  low <= E <= high                 (wick spans the level)
  straddle_body  min(o,c) <= E <= max(o,c)        (body spans the level)
  outside        low > E  (long)  /  high < E     (whole candle beyond)
  inside         high < E (long)  /  low > E      (whole candle within)
Features are the fractions of each, plus the longest consecutive OUTSIDE run
normalised by window length (the "clean excursion" the hypothesis contrasts with).
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E
from tsugi_test import _walk, report, perm_diff, COSTS, R0, L, TOL, STOPF, MAXWAIT, RNG
from tsugi_v2 import vwaps, _ag

def edge_features(o,h,l,c,Eg,dr):
    n=len(o)
    if n==0: return {}
    bl=np.minimum(o,c); bh=np.maximum(o,c)
    sw=(l<=Eg)&(h>=Eg)
    sb=(bl<=Eg)&(bh>=Eg)
    out=(l>Eg) if dr==1 else (h<Eg)
    ins=(h<Eg) if dr==1 else (l>Eg)
    run=mx=0
    for f in out:
        run = run+1 if f else 0
        mx=max(mx,run)
    return dict(n_bars=n, straddle_wick=sw.mean(), straddle_body=sb.mean(),
                outside_frac=out.mean(), inside_frac=ins.mean(),
                max_out_run=mx/n, touches=int(np.diff(np.concatenate([[0],sw.astype(int)])).clip(min=0).sum()))

def build(inst, tz="America/New_York", r0=R0):
    raw = vwaps(mdload.load(inst), tz)
    df = E.prep(raw, tz=tz, r0=r0)
    cost_pts=COSTS[inst]; r1=r0+L; rows=[]
    for day,g in df.groupby("day",sort=True):
        m=g.m.values; o=g.open.values; h=g.high.values; l=g.low.values; c=g.close.values
        ve=g.vw_eth.values
        rm=(m>=r0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
        if W<=0: continue
        post=m>=r1
        if post.sum()<60: continue
        pm=m[post]-r1; po=o[post]; ph=h[post]; pl=l[post]; pc=c[post]; pve=ve[post]
        b=pm//L; sk=-1; dr=0
        for k in range(int(b.max())+1):
            s=b==k
            if not s.any(): continue
            if pc[s][-1]>oh: sk,dr=k,1; break
            if pc[s][-1]<ol: sk,dr=k,-1; break
        if sk<0: continue
        conf=(sk+1)*L; edge=oh if dr==1 else ol; tol=TOL*W
        after=np.where(pm>=conf)[0]
        if len(after)==0: continue
        ci=after[0]
        rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
        if not rt: continue
        ei=rt[0]; lat=int(pm[ei]-conf)
        if lat>MAXWAIT or ei>=len(pm)-5: continue
        wimp=(pm>=conf)&(np.arange(len(pm))<=ei)
        imp=ph[wimp].max() if dr==1 else pl[wimp].min()
        res=_walk(edge,dr,W,ph,pl,pc,pm,ei,STOPF*W,cost_pts)
        if not res: continue
        sl=slice(ci,ei+1)                                   # PRE-ENTRY, tradeable
        pre=edge_features(po[sl],ph[sl],pl[sl],pc[sl],edge,dr)
        j2=min(ei+16,len(pm))
        post_f=edge_features(po[ei:j2],ph[ei:j2],pl[ei:j2],pc[ei:j2],edge,dr)
        res.update(date=str(pd.Timestamp(day).date()),inst=inst,dir=dr,W=W,lat=lat,
                   imp_R=abs(imp-edge)/res["R_pts"],
                   agree_eth=_ag(pc[max(ei-1,0)],pve[max(ei-1,0)],dr))
        res.update({f"pre_{k}":v for k,v in pre.items()})
        res.update({f"post_{k}":v for k,v in post_f.items()})
        rows.append(res)
    return pd.DataFrame(rows)
