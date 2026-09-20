import numpy as np, pandas as pd, mdload, exp_matrix as E
R0=9*60+30; L=30; TOL=.10; STOPF=.50; MAXWAIT=60; MAXHOLD=180
TP_MIN,TP_CAP=2.,4.
CFD={'NAS100':2.92,'US500':1.26,'XAUUSD':0.75}
def run(inst, fill_mode):
    """fill_mode 'edge'  = research model (fill at the edge whenever within tol)
       fill_mode 'tol'   = conservative (fill at edge +/- tol, the worse price)"""
    raw=mdload.load(inst); df=E.prep(raw); cost=CFD[inst]; r1=R0+L; rows=[]
    for day,g in df.groupby("day",sort=True):
        m=g.m.values;h=g.high.values;l=g.low.values;c=g.close.values
        rm=(m>=R0)&(m<r1)
        if rm.sum()<L: continue
        oh,ol=h[rm].max(),l[rm].min(); W=oh-ol
        if W<=0 or W < cost/0.075: continue          # THE GATE
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
        reached = (pl[ei]<=edge) if dr==1 else (ph[ei]>=edge)
        px = edge if fill_mode=='edge' else (edge if reached else (edge+dr*tol))
        stop = edge - dr*STOPF*W; R=abs(px-stop)
        if R<=0: continue
        ext=ph[:ei+1].max() if dr==1 else pl[:ei+1].min(); dist=(ext-px)*dr
        tp=px+dr*min(max(dist/R,TP_MIN),TP_CAP)*R
        t0=pm[ei]; ex=exr=None; be=False; trail=stop; j=ei
        for j in range(ei,len(pm)):
            if pm[j]-t0>MAXHOLD: ex,exr=pc[j],"time";break
            fav=(ph[j]-px) if dr==1 else (px-pl[j])
            hs=(pl[j]<=trail) if dr==1 else (ph[j]>=trail)
            ht=(ph[j]>=tp) if dr==1 else (pl[j]<=tp)
            if hs and ht: ex,exr=trail,"ambig";break
            if hs: ex,exr=trail,("trailstop" if be else "stop");break
            if ht: ex,exr=tp,"target";break
            if fav>=R:
                be=True; nt=(ph[j]-R) if dr==1 else (pl[j]+R)
                trail=max(trail,nt,px) if dr==1 else min(trail,nt,px)
        if ex is None: ex,exr=pc[-1],"eod"
        rows.append(dict(date=str(pd.Timestamp(day).date()),inst=inst,reached=int(reached),
                         net=((ex-px)*dr)/R - cost/R, R_pts=R))
    return pd.DataFrame(rows)
