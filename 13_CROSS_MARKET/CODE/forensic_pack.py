#!/usr/bin/env python3
"""STAGE 4 — forensic visual pack for MODEL V1. Draws the actual event sequence."""
import numpy as np, pandas as pd, mdload, exp_matrix as E
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R0=9*60+30; L=30; TOL=.10; STOPF=.50; MAXWAIT=60; MAXHOLD=180
TP_MIN,TP_CAP=2.,4.
COST={'NAS100':2.92,'US500':1.26,'XAUUSD':0.75}; GATE=0.15

def trades(inst):
    raw=mdload.load(inst); df=E.prep(raw); cost=COST[inst]; r1=R0+L; out=[]
    for day,g in df.groupby("day",sort=True):
        m=g.m.values;o=g.open.values;h=g.high.values;l=g.low.values;c=g.close.values
        rm=(m>=R0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
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
        bs=(b==sk); blk_h,blk_l=ph[bs].max(),pl[bs].min()
        blk_o,blk_c=po[bs][0],pc[bs][-1]
        conf=(sk+1)*L; edge=oh if dr==1 else ol; tol=TOL*W
        after=np.where(pm>=conf)[0]
        if len(after)==0: continue
        ci=after[0]
        # FIRST BREAK (not used by V1 -- recorded here to show it is ignored)
        fb=None
        for i in range(len(pm)):
            if (ph[i]>oh) if dr==1 else (pl[i]<ol): fb=i; break
        rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
        if not rt: continue
        ei=rt[0]
        if int(pm[ei]-conf)>MAXWAIT or ei>=len(pm)-5: continue
        reached=(pl[ei]<=edge) if dr==1 else (ph[ei]>=edge)
        px=edge if reached else edge+dr*tol
        stop=edge-dr*STOPF*W; R=abs(px-stop)
        if R<=0: continue
        ext=ph[:ei+1].max() if dr==1 else pl[:ei+1].min(); dist=(ext-px)*dr
        tpR=min(max(dist/R,TP_MIN),TP_CAP); tp=px+dr*tpR*R
        t0=pm[ei]; ex=exr=None; be=False; trail=stop; mfe=0.; term=ei
        for j in range(ei,len(pm)):
            term=j
            if pm[j]-t0>MAXHOLD: ex,exr=pc[j],"time"; break
            fav=(ph[j]-px) if dr==1 else (px-pl[j]); mfe=max(mfe,fav)
            hs=(pl[j]<=trail) if dr==1 else (ph[j]>=trail)
            ht=(ph[j]>=tp) if dr==1 else (pl[j]<=tp)
            if hs and ht: ex,exr=trail,"ambig"; break
            if hs: ex,exr=trail,("trailstop" if be else "stop"); break
            if ht: ex,exr=tp,"target"; break
            if fav>=R:
                be=True; nt=(ph[j]-R) if dr==1 else (pl[j]+R)
                trail=max(trail,nt,px) if dr==1 else min(trail,nt,px)
        if ex is None: ex,exr=pc[-1],"eod"
        gross=((ex-px)*dr)/R
        # bars for drawing: from 09:30 to exit + 20 min
        n_end=min(term+20,len(pm)-1)
        bars=dict(rm_o=o[rm],rm_h=h[rm],rm_l=l[rm],rm_c=c[rm],
                  po=po[:n_end+1],ph=ph[:n_end+1],pl=pl[:n_end+1],pc=pc[:n_end+1],pm=pm[:n_end+1])
        out.append(dict(date=str(pd.Timestamp(day).date()),inst=inst,dir=dr,W=W,R=R,oh=oh,ol=ol,
            mid=(oh+ol)/2,edge=edge,px=px,stop=stop,tp=tp,tpR=tpR,exit=ex,exr=exr,
            gross=gross,net=gross-cost/R,mfe_R=mfe/R,term=term,ci=ci,ei=ei,fb=fb,
            conf_idx=int(np.where(bs)[0][-1]), blk_h=blk_h,blk_l=blk_l,
            block_range_W=(blk_h-blk_l)/W, reached=int(reached),
            lat=int(pm[ei]-conf), bars=bars))
    return out

def draw(ax,t,title):
    b=t['bars']; dr=t['dir']
    ro,rh,rl,rc=b['rm_o'],b['rm_h'],b['rm_l'],b['rm_c']
    po,ph,pl,pc=b['po'],b['ph'],b['pl'],b['pc']
    n1=len(ro); O=np.concatenate([ro,po]); H=np.concatenate([rh,ph])
    Lo=np.concatenate([rl,pl]); C=np.concatenate([rc,pc])
    x=np.arange(len(O))
    # ORB band
    ax.add_patch(Rectangle((0,t['ol']),len(O),t['oh']-t['ol'],
                 facecolor="#cfe4cb",alpha=.55,edgecolor="none",zorder=0))
    ax.axhline(t['oh'],color="#6f9c68",lw=1.0,zorder=1)
    ax.axhline(t['ol'],color="#6f9c68",lw=1.0,zorder=1)
    ax.axhline(t['mid'],color="#6f9c68",lw=.8,ls=":",zorder=1)
    for i in range(len(O)):
        up=C[i]>=O[i]
        col = "#c99a2e" if i<n1 else ("#2c7d72" if up else "#a33c26")
        ax.plot([i,i],[Lo[i],H[i]],color=col,lw=.6,zorder=2)
        ax.add_patch(Rectangle((i-.32,min(O[i],C[i])),.64,max(abs(C[i]-O[i]),1e-9),
                     facecolor=col,edgecolor=col,lw=.3,zorder=3))
    def V(idx,col,lab,ls="-"):
        ax.axvline(n1+idx,color=col,lw=1.0,ls=ls,alpha=.9,zorder=4)
    if t['fb'] is not None: V(t['fb'],"#8a6209","break",":")
    V(t['conf_idx'],"#1f5fa8","confirm")
    V(t['ci'],"#7a8b99","eligible","--")
    V(t['ei'],"#111111","entry")
    V(t['term'],"#666666","exit","--")
    ax.axhline(t['px'],color="#1f5fa8",lw=1.1,zorder=4)
    ax.axhline(t['stop'],color="#a33c26",lw=1.1,zorder=4)
    ax.axhline(t['tp'],color="#0f6b64",lw=1.1,zorder=4)
    ax.set_title(title,fontsize=7.2,loc="left")
    ax.tick_params(labelsize=5.5); ax.set_xticks([])
    lo=min(Lo.min(),t['stop'])-.03*(H.max()-Lo.min()); hi=max(H.max(),t['tp'])+.03*(H.max()-Lo.min())
    ax.set_ylim(lo,hi); ax.set_xlim(-1,len(O))

def grid(ts,fn,sup):
    n=len(ts); rows=(n+1)//2
    fig,axes=plt.subplots(rows,2,figsize=(13,2.5*rows))
    axes=np.array(axes).reshape(-1)
    for a in axes[n:]: a.axis("off")
    for a,t in zip(axes,ts):
        ttl=(f"{t['inst']} {t['date']} {'LONG' if t['dir']==1 else 'SHORT'} | "
             f"blkRng={t['block_range_W']:.2f}W lat={t['lat']}m | {t['exr']} "
             f"{t['gross']:+.2f}R mfe={t['mfe_R']:.2f}R tp={t['tpR']:.1f}R")
        draw(a,t,ttl)
    fig.suptitle(sup,fontsize=10,y=.999)
    fig.tight_layout(rect=[0,0,1,.985]); fig.savefig(fn,dpi=105); plt.close(fig)
