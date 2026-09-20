#!/usr/bin/env python3
"""TRACK B - minimal behaviour-first FX transferability census.
Reuses the Track A machinery. No new indicators, no filters, no optimisation.
Anchors are PRE-REGISTERED: London 08:00 Europe/London (= 03:00 ET, the MC-6 anchor) with a single
alternative at 07:00; New York 09:30 America/New_York (the evidence-supported Max session).
Timezones are tz-aware, so the weeks when UK and US DST are misaligned are handled by the tz
database rather than by a fixed UTC offset."""
import os, numpy as np, pandas as pd
SH=os.path.expanduser("~/mnt/Dukascopy")
PIP=0.0001; HOR=[5,15,30,60,90,120,180]

def load(fname,tz,lo,hi):
    d=pd.read_csv(os.path.join(SH,fname),usecols=["timestamp","open","high","low","close"])
    d["timestamp"]=pd.to_datetime(d["timestamp"],utc=True).dt.tz_convert(tz)
    bad=((d.high<d[["open","close"]].max(axis=1))|(d.low>d[["open","close"]].min(axis=1))|(d.high<d.low))
    d=d[~bad]
    d["m"]=d.timestamp.dt.hour*60+d.timestamp.dt.minute; d["d"]=d.timestamp.dt.normalize()
    d=d[(d.timestamp.dt.dayofweek<5)&(d.m>=lo)&(d.m<hi)]
    for c in ["open","high","low","close"]: d[c]=d[c]/PIP
    return d.reset_index(drop=True)

def census(fname,tz,r0,r1,send,label):
    d=load(fname,tz,r0,send); rows=[]; rev=[]; comp=[]
    for dt,g in d.groupby("d",sort=True):
        m=g.m.values;o=g.open.values;h=g.high.values;l=g.low.values;c=g.close.values
        rm=(m>=r0)&(m<r1)
        if rm.sum()<(r1-r0): continue
        oh=h[rm].max(); ol=l[rm].min(); mid=(oh+ol)/2; w=oh-ol
        if w<=0: continue
        post=m>=r1; pm=m[post];ph=h[post];pl=l[post];pc=c[post]
        if len(pm)<120: continue
        b=(pm-r1)//15
        # ---- Q5: six-15m-candle containment ----
        cg=True
        for k in range(6):
            s=b==k
            if not s.any(): cg=False;break
            if pc[s][-1]>oh or pc[s][-1]<ol: cg=False;break
        aft=pm>=r1+90
        if aft.any():
            comp.append(dict(date=str(pd.Timestamp(dt).date()),comp=int(cg),
                exc=max(max(ph[aft].max()-oh,0),max(ol-pl[aft].min(),0)),
                up=max(ph[aft].max()-oh,0),dn=max(ol-pl[aft].min(),0),w=w))
        # ---- Q2: completed 15m CLOSE outside (CENSUS-01 representation) ----
        sk=-1;sd=0
        for k in range(int(b.max())+1):
            s=b==k
            if not s.any(): continue
            cc=pc[s][-1]
            if cc>oh: sk,sd=k,1;break
            if cc<ol: sk,sd=k,-1;break
        row=dict(date=str(pd.Timestamp(dt).date()),label=label,orb_w=w,signal=int(sk>=0))
        if sk>=0:
            s=b==sk; entry=pc[s][-1]; edge=oh if sd==1 else ol; R=abs(entry-edge)
            ps=pm>=r1+(sk+1)*15
            if R>0 and ps.any():
                pmm=pm[ps]-(r1+(sk+1)*15);hh=ph[ps];ll=pl[ps]
                fav=(hh-entry) if sd==1 else (entry-ll); adv=(entry-ll) if sd==1 else (hh-entry)
                row.update(dir=sd,R_pips=R,close_entry=entry,sig_bar=sk+1,
                    dist_opp_R=abs(entry-(ol if sd==1 else oh))/R)
                for H in HOR+[10**9]:
                    hn="EOD" if H>10**8 else str(H); wsel=pmm<H
                    if wsel.any():
                        row[f"mfe_R_{hn}"]=fav[wsel].max()/R; row[f"mae_R_{hn}"]=adv[wsel].max()/R
                # Q3 return inside
                ri=np.where((ll<=oh) if sd==1 else (hh>=ol))[0]
                row["ret_inside_min"]=int(pmm[ri[0]]) if len(ri) else -1
        rows.append(row)
        # ---- Q1/Q4: print-through boundary entry (EXP-008 representation) ----
        i=0;n=0
        while i<len(pm)-2 and n<2:
            bi=None;d_=0
            for j in range(i,len(pm)):
                if ph[j]>oh: bi,d_=j,1;break
                if pl[j]<ol: bi,d_=j,-1;break
            if bi is None: break
            ei=None
            for j in range(bi+1,min(bi+60,len(pm))):
                pb=(ph[j-1]>oh) if d_==1 else (pl[j-1]<ol)
                if not pb: continue
                trig=ph[j-1] if d_==1 else pl[j-1]
                if (ph[j]>trig) if d_==1 else (pl[j]<trig): ei=j;break
            if ei is None: break
            entry=ph[ei-1] if d_==1 else pl[ei-1]          # slip applied later, explicitly
            stop=pl[ei-1] if d_==1 else ph[ei-1]; R=abs(entry-stop)
            if R<=0: i=ei+1; continue
            t0=pm[ei];ex=None;exr=None;mfe=0;mae=0
            for j in range(ei,len(pm)):
                if pm[j]-t0>180: ex=pc[j];exr="time";break
                fav=(ph[j]-entry) if d_==1 else (entry-pl[j]); adv=(entry-pl[j]) if d_==1 else (ph[j]-entry)
                mfe=max(mfe,fav);mae=max(mae,adv)
                if (pl[j]<=stop) if d_==1 else (ph[j]>=stop): ex=stop;exr="stop";break
                if ol<=pc[j]<=oh: ex=pc[j];exr="invalid";break
            if ex is None: ex=pc[-1];exr="eod"
            rev.append(dict(date=str(pd.Timestamp(dt).date()),label=label,dir=d_,R_pips=R,
                gross_R=((ex-entry)*d_)/R,exit_reason=exr,mfe_R=mfe/R,mae_R=mae/R,orb_w=w,
                dist_opp_R=abs((ol if d_==1 else oh)-entry)/R))
            n+=1;i=j+1
    return pd.DataFrame(rows),pd.DataFrame(rev),pd.DataFrame(comp)
