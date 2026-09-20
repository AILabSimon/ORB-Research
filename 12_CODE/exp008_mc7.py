#!/usr/bin/env python3
"""EXP-008 / MC-7 - SOURCE-FAITHFUL boundary entry per RR-002.
Entry : price trades beyond the ORB boundary, then a PRINT-THROUGH (P-2/R-009):
        a 1m candle trading beyond the previous (already-beyond-boundary) candle's extreme.
        Fill at that previous candle's extreme + slippage (manual market entry, R-038).
Stop  : beyond the entry-reference candle's opposite extreme (R-040, "under the candle").
Exit  : invalidation = close back inside the ORB (R-045/R-041) | stop | 180m time exit.
Bracket P-1/R-036: on invalidation of the continuation, take the opposite side (OCO representation).
No fixed R target is source-supported (RR-002 s8); a 2R arm is run separately and LABELLED.
"""
import os,sys,json
import numpy as np, pandas as pd
SH=os.path.expanduser("~/mnt/Dukascopy"); PROJ=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0")
OUT=os.path.join(PROJ,"08_EXPERIMENTS","CANDIDATES"); os.makedirs(OUT,exist_ok=True)

def load(f,tz="America/New_York"):
    d=pd.read_csv(os.path.join(SH,f),usecols=["timestamp","open","high","low","close"])
    d["timestamp"]=pd.to_datetime(d["timestamp"],utc=True).dt.tz_convert(tz)
    bad=((d.high<d[["open","close"]].max(axis=1))|(d.low>d[["open","close"]].min(axis=1))|(d.high<d.low))
    d=d[~bad]
    d["m"]=d.timestamp.dt.hour*60+d.timestamp.dt.minute; d["d"]=d.timestamp.dt.normalize()
    return d[(d.timestamp.dt.dayofweek<5)&(d.m>=570)&(d.m<960)].reset_index(drop=True)

def sess_map(df):
    """per-date arrays"""
    out={}
    for dt,g in df.groupby("d",sort=True):
        out[dt]=(g.m.values,g.open.values,g.high.values,g.low.values,g.close.values)
    return out

def run(inst="NAS100", fname="NAS100_1m.csv", conf_inst=None, conf_fname=None,
        r0=570,r1=585, slip=0.5, tag="base", max_trades=2, bracket=True,
        target_R=None, compression_N=None, invalidation="1m", optimistic=False):
    A=sess_map(load(fname))
    C=sess_map(load(conf_fname)) if conf_fname else None
    trades=[]
    for dt,(m,o,h,l,c) in A.items():
        rm=(m>=r0)&(m<r1)
        if rm.sum()<(r1-r0): continue
        oh=h[rm].max(); ol=l[rm].min(); mid=(oh+ol)/2; width=oh-ol
        if width<=0: continue
        post=m>=r1
        pm=m[post];ph=h[post];pl=l[post];pc=c[post];po=o[post]
        if len(pm)<30: continue
        # compression gate G-4 / P-6: N consecutive 15m candles with NO close outside the range
        if compression_N is not None:
            b=(pm-r1)//15; ok=True
            for k in range(compression_N):
                s=b==k
                if not s.any(): ok=False;break
                cc=pc[s][-1]
                if cc>oh or cc<ol: ok=False;break
            if not ok: continue
            start_i=int(np.argmax(pm>=r1+compression_N*15))
        else:
            start_i=0
        # confirming instrument ORB (G-1 / P-4)
        cf=None
        if C is not None and dt in C:
            cm,co,ch,cl_,cc_=C[dt]
            crm=(cm>=r0)&(cm<r1)
            if crm.sum()>=(r1-r0):
                cf=(cm,ch[crm].max(),cl_[crm].min(),ch,cl_)
        i=start_i; ntr=0; forced_dir=None
        while i<len(pm)-2 and ntr<max_trades:
            # find boundary breach
            bi=None;d_=0
            for j in range(i,len(pm)):
                if forced_dir is None:
                    if ph[j]>oh: bi,d_=j,1;break
                    if pl[j]<ol: bi,d_=j,-1;break
                else:
                    d_=forced_dir
                    if (d_==1 and ph[j]>oh) or (d_==-1 and pl[j]<ol): bi=j;break
            if bi is None: break
            # PRINT-THROUGH: next bar trading beyond previous bar's extreme, previous bar beyond boundary
            ei=None
            for j in range(bi+1,min(bi+60,len(pm))):
                prev_beyond=(ph[j-1]>oh) if d_==1 else (pl[j-1]<ol)
                if not prev_beyond: continue
                trig=ph[j-1] if d_==1 else pl[j-1]
                hit=(ph[j]>trig) if d_==1 else (pl[j]<trig)
                if hit: ei=j; break
            if ei is None: break
            entry=(ph[ei-1]+slip) if d_==1 else (pl[ei-1]-slip)
            stop=pl[ei-1] if d_==1 else ph[ei-1]
            Rp=abs(entry-stop)
            if Rp<=0: i=ei+1; continue
            # cross-instrument gate
            conf_ok=True
            if cf is not None:
                cm,coh,col,chh,cll=cf
                t=pm[ei]; k=np.where(cm==t)[0]
                if len(k):
                    kk=k[0]
                    conf_ok = (chh[kk]>coh) if d_==1 else (cll[kk]<col)
                else: conf_ok=False
            elif C is not None: conf_ok=False
            # walk forward
            ex=None;exr=None;mfe=0.0;mae=0.0
            t0=pm[ei]
            for j in range(ei,len(pm)):
                if pm[j]-t0>180: ex=pc[j-1] if j>ei else entry; exr="time"; break
                fav=(ph[j]-entry) if d_==1 else (entry-pl[j])
                adv=(entry-pl[j]) if d_==1 else (ph[j]-entry)
                mfe=max(mfe,fav); mae=max(mae,adv)
                hit_stop=(pl[j]<=stop) if d_==1 else (ph[j]>=stop)
                hit_tgt=(target_R is not None) and (fav>=target_R*Rp)
                inval = (ol<=pc[j]<=oh) if invalidation=="1m" else ((pm[j]-r1+1)%15==0 and ol<=pc[j]<=oh)
                if optimistic:
                    # OPTIMISTIC same-bar resolution: favourable outcome wins the bar
                    if hit_tgt: ex=entry+d_*target_R*Rp; exr="target"; break
                    if inval and hit_stop: ex=pc[j]; exr="invalid"; break
                if hit_stop and hit_tgt: ex=stop; exr="ambiguous_stop"; break   # conservative
                if hit_stop: ex=stop; exr="stop"; break
                if hit_tgt: ex=entry+d_*target_R*Rp; exr="target"; break
                # invalidation: close back inside ORB
                if invalidation=="1m":
                    if ol<=pc[j]<=oh: ex=pc[j]; exr="invalid"; break
                else:
                    if (pm[j]-r1+1)%15==0 and ol<=pc[j]<=oh: ex=pc[j]; exr="invalid"; break
            if ex is None: ex=pc[-1]; exr="eod"
            gross=(ex-entry)*d_
            trades.append(dict(date=str(pd.Timestamp(dt).date()),inst=inst,tag=tag,dir=d_,
                seq=ntr+1,entry=entry,stop=stop,R_pts=Rp,exit=ex,exit_reason=exr,
                gross_pts=gross,gross_R=gross/Rp,mfe_R=mfe/Rp,mae_R=mae/Rp,
                orb_width=width,conf_ok=int(conf_ok),entry_min=int(pm[ei]-r1),
                hold_min=int(pm[min(j,len(pm)-1)]-t0)))
            ntr+=1
            if bracket and exr=="invalid":
                forced_dir=-d_; i=j+1
            else: break
    t=pd.DataFrame(trades)
    t.to_csv(os.path.join(OUT,f"EXP008_{inst}_{tag}.csv"),index=False)
    return t

def report(t,label,cost_pts,conf_only=False):
    if conf_only: t=t[t.conf_ok==1]
    if len(t)==0: print(f"  {label}: no trades"); return
    net=t.gross_R - cost_pts/t.R_pts
    rng=np.random.default_rng(3)
    bs=np.array([rng.choice(net.values,len(net),True).mean() for _ in range(3000)])
    wr=(t.gross_R>0).mean()
    print(f"  {label:44s} n={len(t):5d} ({len(t)/12.5:5.1f}/yr) medR_pts={t.R_pts.median():5.1f} "
          f"win={100*wr:4.1f}% grossE={t.gross_R.mean():+.3f}R netE={net.mean():+.3f}R "
          f"CI[{np.percentile(bs,2.5):+.3f},{np.percentile(bs,97.5):+.3f}]")

if __name__=="__main__":
    COST_MNQ=1.75; COST_CFD=3.42
    print("=== EXP-008 / MC-7 : source-faithful boundary entry (print-through gated) ===")
    base=run(tag="base")
    print(f"\nSOURCE-FIDELITY CHECK - Max states live stops of 6-17 NQ pts, mode ~9-10.")
    print(f"  representation gives R_pts: p25={base.R_pts.quantile(.25):.1f} med={base.R_pts.median():.1f} p75={base.R_pts.quantile(.75):.1f} mode-ish={base.R_pts.round().mode().iloc[0]:.0f}")
    print(f"  share in the 6-17pt band: {100*base.R_pts.between(6,17).mean():.1f}%")
    print("\n-- ARMS (MNQ-realistic cost 1.75 pts round trip) --")
    report(base,"A1 source-faithful, exit on 1m close inside",COST_MNQ)
    report(base[base.seq==1],"A2 first trade only (no bracket leg)",COST_MNQ)
    report(base[base.seq==2],"A3 bracket reversal leg only (P-1)",COST_MNQ)
    b15=run(tag="inval15m",invalidation="15m"); report(b15,"A4 invalidation on 15m close inside",COST_MNQ)
    t2=run(tag="t2R",target_R=2.0); report(t2,"A5 + 2R target (ANALYST CONSTRUCT, not found)",COST_MNQ)
    report(base,"A6 same, Dukascopy CFD cost 3.42",COST_CFD)
