#!/usr/bin/env python3
"""
STOP SEGMENTATION III — four questions put by the SVP, 17 Sep 2026.
Pre-registered before measurement. Honest fill (convention B), registered costs, gate 0.15.

Q1  OVERLAP.  Are the stopped trades built out of overlapping candles?
      ovl = mean over consecutive 1-minute bars of  overlap(range_i, range_i-1) / union
      1.0 = every bar sits inside the last one (pure chop).  0.0 = every bar clears the
      last one entirely (pure trend).  Measured separately over the confirming 30-minute
      block and over the wait from confirmation to the bar BEFORE entry.

Q2  DOES PRICE GO BACK THROUGH THE ORB LEVEL AFTER THE DIRECTION IS SET?
      reentry_bars   1-minute CLOSES back inside the opening range, after confirmation,
                     before entry  (the price-based invalidation Max describes)
      reentry_any    binary version
      new_ext_pre    price made a NEW extreme beyond the confirming block's extreme
                     before entry
      new_ext_post   price made a new extreme beyond the pre-entry impulse AFTER entry
                     (descriptive only -- not knowable at entry)

Q3  DIRECTION STRENGTH.  Does a stronger confirming move do better?
      close_beyond_W  (block close - edge) / W        how decisively it closed away
      block_body_W    |block close - block open| / W  how much of the block was body
      block_range_W   (block high - block low) / W
      block_eff       body / range                    trend efficiency of the block

Q4  ORB SIZE.  W in points, W relative to its own 20-day median, W as a fraction of the
      prior day's true range, and cost/R.

All Q1-Q4 features are strictly pre-entry and therefore tradeable. new_ext_post is not.
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E
R0=9*60+30; L=30; TOL=.10; STOPF=.50; MAXWAIT=60; MAXHOLD=180
TP_MIN,TP_CAP=2.,4.
COST={'NAS100':2.92,'US500':1.26,'XAUUSD':0.75}
GATE=0.15

def overlap(h,l):
    if len(h)<2: return np.nan
    o=[]
    for i in range(1,len(h)):
        ov=max(0.,min(h[i],h[i-1])-max(l[i],l[i-1]))
        un=max(h[i],h[i-1])-min(l[i],l[i-1])
        o.append(ov/un if un>0 else 1.0)
    return float(np.mean(o))

def build(inst):
    raw=mdload.load(inst); df=E.prep(raw); cost=COST[inst]; r1=R0+L; rows=[]
    prev_tr={}
    for day,g in df.groupby("day",sort=True):
        m=g.m.values;o=g.open.values;h=g.high.values;l=g.low.values;c=g.close.values
        dr_hi,dr_lo=h.max(),l.min()
        rm=(m>=R0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
        ptr=prev_tr.get('v'); prev_tr['v']=dr_hi-dr_lo
        if W<=0 or cost/(STOPF*W)>GATE: continue
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
        bs=(b==sk)                                   # the confirming block
        blk_o,blk_c=po[bs][0],pc[bs][-1]
        blk_h,blk_l=ph[bs].max(),pl[bs].min()
        conf=(sk+1)*L; edge=oh if dr==1 else ol; tol=TOL*W
        after=np.where(pm>=conf)[0]
        if len(after)==0: continue
        ci=after[0]
        rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
        if not rt: continue
        ei=rt[0]
        if int(pm[ei]-conf)>MAXWAIT or ei>=len(pm)-5: continue
        # ---- strictly pre-entry windows
        ovl_blk=overlap(ph[bs],pl[bs])
        e1=ei-1
        if e1>=ci:
            ovl_wait=overlap(ph[ci:e1+1],pl[ci:e1+1])
            wc=pc[ci:e1+1]
            reentry=int(((wc<=oh)&(wc>=ol)).sum())
            newext=int((ph[ci:e1+1].max()>blk_h) if dr==1 else (pl[ci:e1+1].min()<blk_l))
            wait_n=e1-ci+1
        else:
            ovl_wait=np.nan; reentry=0; newext=0; wait_n=0
        impulse=(ph[ci:ei+1].max() if dr==1 else pl[ci:ei+1].min())
        reached=(pl[ei]<=edge) if dr==1 else (ph[ei]>=edge)
        px=edge if reached else edge+dr*tol
        stop=edge-dr*STOPF*W; R=abs(px-stop)
        if R<=0: continue
        ext=ph[:ei+1].max() if dr==1 else pl[:ei+1].min(); dist=(ext-px)*dr
        tp=px+dr*min(max(dist/R,TP_MIN),TP_CAP)*R
        t0=pm[ei]; ex=exr=None; be=False; trail=stop; mfe=0.; term=ei
        post_ext=0
        for j in range(ei,len(pm)):
            term=j
            if pm[j]-t0>MAXHOLD: ex,exr=pc[j],"time";break
            fav=(ph[j]-px) if dr==1 else (px-pl[j])
            mfe=max(mfe,fav)
            if (ph[j]>impulse) if dr==1 else (pl[j]<impulse): post_ext=1
            hs=(pl[j]<=trail) if dr==1 else (ph[j]>=trail)
            ht=(ph[j]>=tp) if dr==1 else (pl[j]<=tp)
            if hs and ht: ex,exr=trail,"ambig";break
            if hs: ex,exr=trail,("trailstop" if be else "stop");break
            if ht: ex,exr=tp,"target";break
            if fav>=R:
                be=True; nt=(ph[j]-R) if dr==1 else (pl[j]+R)
                trail=max(trail,nt,px) if dr==1 else min(trail,nt,px)
        if ex is None: ex,exr=pc[-1],"eod"
        gross=((ex-px)*dr)/R
        rows.append(dict(date=str(pd.Timestamp(day).date()),inst=inst,dir=dr,W=W,R_pts=R,
            exit_reason=exr,gross=gross,net=gross-cost/R,mfe_R=mfe/R,
            cost_R=cost/R, lat=int(pm[ei]-conf), wait_n=wait_n,
            ovl_blk=ovl_blk, ovl_wait=ovl_wait,
            reentry_bars=reentry, reentry_any=int(reentry>0),
            new_ext_pre=newext, new_ext_post=post_ext,
            close_beyond_W=abs(blk_c-edge)/W,
            block_body_W=abs(blk_c-blk_o)/W,
            block_range_W=(blk_h-blk_l)/W,
            block_eff=abs(blk_c-blk_o)/max(blk_h-blk_l,1e-12),
            prev_tr=ptr, W_over_prevTR=(W/ptr if ptr and ptr>0 else np.nan)))
    d=pd.DataFrame(rows)
    d['W_med20']=d.W.rolling(20,min_periods=10).median().shift(1)
    d['W_rel']=d.W/d.W_med20
    d['yr']=d.date.str[:4].astype(int)
    d['is_stop']=(d.exit_reason=='stop').astype(int)
    return d
