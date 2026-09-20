#!/usr/bin/env python3
"""TSUGI v2 — fair-test refinements, pre-registered 2026-09-17 before measurement.

Two objections to v1 that must be answered before either claim is judged:

R1  The session-anchored VWAP is mechanically inside the opening range, so
    "price vs VWAP" is ~99% collinear with the ORB direction and cannot filter.
    That is a degenerate test of the slide's claim, not a fair one. Re-test with
    an OVERNIGHT-anchored VWAP (18:00 NY prior day -> 17:00 NY), which is the
    anchor a futures day-trader actually reads and which is NOT pinned inside
    the opening range.

R2  v1 fires the sweep on the FIRST 1-minute excursion beyond an edge (median
    reclaim 2 min, 2150 of ~2700 days). The slide describes a distinct
    manipulation leg, not any tick through the level. Segment by sweep DEPTH
    and require the reclaim to be decisive, so the model is judged on the
    population it actually describes.
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E
from tsugi_test import (_walk, report, perm_diff, COSTS, R0, L, TOL, STOPF,
                        MAXWAIT, RECLAIM_MAX, SWEEP_MIN_W, RNG)

def vwaps(raw, tz="America/New_York"):
    """Return the raw frame with two cumulative VWAP columns:
       vw_rth  anchored 09:30 NY ; vw_eth anchored 18:00 NY prior day."""
    d = raw.copy()
    loc = d.timestamp.dt.tz_convert(tz)
    d["m"] = loc.dt.hour*60 + loc.dt.minute
    d["cday"] = loc.dt.normalize()
    # ETH session day: bars at/after 18:00 belong to the NEXT calendar day's session
    d["sday"] = d["cday"] + pd.to_timedelta((d.m >= 18*60).astype(int), unit="D")
    tp = (d.high + d.low + d.close)/3.0
    d["_pv"] = tp*d.volume
    for tag, key in (("vw_eth","sday"), ("vw_rth","cday")):
        if tag == "vw_rth":
            mask = d.m >= R0
            num = (d._pv*mask).groupby(d[key]).cumsum()
            den = (d.volume*mask).groupby(d[key]).cumsum()
        else:
            num = d._pv.groupby(d[key]).cumsum()
            den = d.volume.groupby(d[key]).cumsum()
        d[tag] = np.where(den > 0, num/den.replace(0, np.nan), np.nan)
    return d.drop(columns=["_pv"])

def build(inst, tz="America/New_York", r0=R0):
    raw = vwaps(mdload.load(inst), tz)
    df = E.prep(raw, tz=tz, r0=r0)
    cost_pts = COSTS[inst]; r1 = r0+L
    cm, sw = [], []
    for day, g in df.groupby("day", sort=True):
        m=g.m.values; h=g.high.values; l=g.low.values; c=g.close.values
        vr=g.vw_rth.values; ve=g.vw_eth.values
        rm=(m>=r0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol = h[rm].max(), l[rm].min(); W = oh-ol
        if W<=0: continue
        post = m>=r1
        if post.sum()<60: continue
        pm=m[post]-r1; ph=h[post]; pl=l[post]; pc=c[post]
        pvr=vr[post]; pve=ve[post]
        D = str(pd.Timestamp(day).date())

        # ---- CM-C1 with both VWAP anchors as features ----
        b=pm//L; sk=-1; dr=0
        for k in range(int(b.max())+1):
            s=b==k
            if not s.any(): continue
            if pc[s][-1]>oh: sk,dr=k,1; break
            if pc[s][-1]<ol: sk,dr=k,-1; break
        if sk>=0:
            conf=(sk+1)*L; edge=oh if dr==1 else ol; tol=TOL*W
            after=np.where(pm>=conf)[0]
            rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
            if rt:
                ei=rt[0]; lat=int(pm[ei]-conf)
                if lat<=MAXWAIT and ei<len(pm)-5:
                    k0=max(ei-1,0); ref=pc[k0]
                    res=_walk(edge,dr,W,ph,pl,pc,pm,ei,STOPF*W,cost_pts)
                    if res:
                        res.update(date=D,inst=inst,dir=dr,W=W,lat=lat,
                            agree_rth=_ag(ref,pvr[k0],dr), agree_eth=_ag(ref,pve[k0],dr),
                            dist_rth=(ref-pvr[k0])/W, dist_eth=(ref-pve[k0])/W)
                        cm.append(res)

        # ---- sweep / V-shape recovery, with depth recorded ----
        si=None
        for i in range(len(pm)):
            up=ph[i]>oh+SWEEP_MIN_W*W; dn=pl[i]<ol-SWEEP_MIN_W*W
            if up or dn: si=i; sdir=1 if up else -1; break
        if si is None: continue
        ext=ph[si] if sdir==1 else pl[si]; ri=None
        for j in range(si,len(pm)):
            if pm[j]-pm[si]>RECLAIM_MAX: break
            ext = max(ext,ph[j]) if sdir==1 else min(ext,pl[j])
            inside=(pc[j]<oh) if sdir==1 else (pc[j]>ol)
            if j>si and inside: ri=j; break
        if ri is None or ri>=len(pm)-5: continue
        td=-sdir; px=pc[ri]
        depth=abs(ext-(oh if sdir==1 else ol))/W
        # decisive reclaim: close back inside by >10% of W, not a marginal tick
        edge_sw = oh if sdir==1 else ol
        decisive = int(abs(px-edge_sw) > 0.10*W)
        for tag,sd in (("a_halfW",STOPF*W),("b_struct",abs(ext-px)+0.02*W)):
            res=_walk(px,td,W,ph,pl,pc,pm,ri,sd,cost_pts)
            if res:
                res.update(date=D,inst=inst,dir=td,W=W,stopmode=tag,
                    sweep_depth_W=depth, reclaim_min=int(pm[ri]-pm[si]),
                    decisive=decisive, sweep_clock=int(r1+pm[si]),
                    agree_eth=_ag(px,pve[ri],td), agree_rth=_ag(px,pvr[ri],td))
                sw.append(res)
    return pd.DataFrame(cm), pd.DataFrame(sw)

def _ag(px, vw, dr):
    if not np.isfinite(vw): return -1
    return int(np.sign(px-vw)==dr)
