#!/usr/bin/env python3
"""PHASE A - cross-market behaviour-only opening-range census.
Pre-registered in 13_CROSS_MARKET/SPECIFICATION/. No stops, no targets, no R-multiples.
Excursions normalised by opening-range width W and reported in instrument points.
Deterministic. Read-only on the shared Dukascopy store."""
import os, sys, json, hashlib
import numpy as np, pandas as pd

SH=os.path.expanduser("~/mnt/Dukascopy")
BR=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/13_CROSS_MARKET")
OUT=os.path.join(BR,"CENSUS","RESULTS"); os.makedirs(OUT,exist_ok=True)
HOR=[30,60,90,120,180]
RETEST_TOL=0.10   # ANALYST-DEFINED: retest = return to within 0.10 x W of the broken edge

MARKETS={
 "NAS100": dict(file="NAS100_1m.csv", tz="America/New_York", unit=1.0, uname="index pts",
                events={"CASH0930":570}, send=960, ctrl=720, repr="INDEX_CFD_OTC proxy for NQ/MNQ"),
 "US500":  dict(file="US500_1m.csv",  tz="America/New_York", unit=1.0, uname="index pts",
                events={"CASH0930":570}, send=960, ctrl=720, repr="INDEX_CFD_OTC proxy for ES/MES"),
 "XAUUSD": dict(file="XAUUSD_1m.csv", tz="America/New_York", unit=1.0, uname="USD",
                events={"COMEX0820":500,"CASH0930":570}, send=960, ctrl=720, repr="SPOT proxy for GC/MGC"),
 "EURUSD": dict(file="EURUSD_1M.csv", tz="Europe/London",   unit=0.0001, uname="pips",
                events={"LON0800":480}, send=1020, ctrl=720, repr="SPOT (native)"),
 "GBPUSD": dict(file="GBPUSD_1M.csv", tz="Europe/London",   unit=0.0001, uname="pips",
                events={"LON0800":480}, send=1020, ctrl=720, repr="SPOT (native)"),
}

def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda: f.read(1<<22), b""): h.update(c)
    return h.hexdigest()

_CACHE={}
def load(mk):
    if mk in _CACHE: return _CACHE[mk]
    cfg=MARKETS[mk]; p=os.path.join(SH,cfg["file"])
    d=pd.read_csv(p,usecols=["timestamp","open","high","low","close"])
    d["timestamp"]=pd.to_datetime(d["timestamp"],utc=True).dt.tz_convert(cfg["tz"])
    bad=((d.high<d[["open","close"]].max(axis=1))|(d.low>d[["open","close"]].min(axis=1))|(d.high<d.low))
    nbad=int(bad.sum()); d=d[~bad]
    for c in ["open","high","low","close"]: d[c]=d[c]/cfg["unit"]
    d["m"]=d.timestamp.dt.hour*60+d.timestamp.dt.minute
    d["dt"]=d.timestamp.dt.normalize()
    d=d[d.timestamp.dt.dayofweek<5]
    _CACHE[mk]=(d.reset_index(drop=True), nbad, p)
    return _CACHE[mk]

def path_block(pm,ph,pl,pc,entry,d_,W,prefix,row,thr=(0.5,1.0,2.0,3.0)):
    """excursion measures from an already-offset path. pm = minutes since event."""
    if len(pm)==0 or W<=0: return
    fav=(ph-entry) if d_==1 else (entry-pl)
    adv=(entry-pl) if d_==1 else (ph-entry)
    for H in HOR+[10**9]:
        hn="EOD" if H>10**8 else str(H); s=pm<H
        if not s.any(): continue
        row[f"{prefix}mfe_W_{hn}"]=fav[s].max()/W
        row[f"{prefix}mae_W_{hn}"]=adv[s].max()/W
        row[f"{prefix}net_W_{hn}"]=((pc[s][-1]-entry)*d_)/W
    for t in thr:
        w=np.where(fav>=t*W)[0]
        row[f"{prefix}t_{t}W_min"]=int(pm[w[0]]) if len(w) else -1
    # opportunity remaining: MFE from horizon H to EOD, in W
    for H in HOR:
        s=pm>=H
        if s.any():
            row[f"{prefix}remain_W_{H}"]=max(ph[s].max()-pc[pm<H][-1] if (pm<H).any() else 0,
                                             (pc[pm<H][-1] if (pm<H).any() else 0)-pl[s].min())/W

def census(mk,ev,L,anchor,control=False):
    cfg=MARKETS[mk]; d,nbad,src=load(mk)
    r0 = cfg["ctrl"] if control else anchor
    r1 = r0+L; send=cfg["send"]
    rows=[]; excl=0
    prev_close={}
    for dt,g in d.groupby("dt",sort=True):
        m=g.m.values;o=g.open.values;h=g.high.values;l=g.low.values;c=g.close.values
        rm=(m>=r0)&(m<r1)
        if rm.sum()<L: excl+=1; continue
        oh=h[rm].max(); ol=l[rm].min(); W=oh-ol; mid=(oh+ol)/2
        if W<=0: excl+=1; continue
        post=(m>=r1)&(m<send)
        if post.sum()<60: excl+=1; continue
        pm=m[post]-r1; ph=h[post]; pl=l[post]; pc=c[post]; 
        row=dict(date=str(pd.Timestamp(dt).date()),market=mk,event=("CTRL1200" if control else ev),
                 L=L,W=W,orb_high=oh,orb_low=ol,orb_mid=mid,
                 orb_dir=int(np.sign(c[rm][-1]-o[rm][0])),
                 orb_body_ratio=abs(c[rm][-1]-o[rm][0])/W,
                 post_bars=int(post.sum()))
        # ---- touches ----
        ta=np.where(ph>oh)[0]; tb=np.where(pl<ol)[0]
        tu=int(pm[ta[0]]) if len(ta) else -1
        td=int(pm[tb[0]]) if len(tb) else -1
        row["first_touch_up_min"]=tu; row["first_touch_dn_min"]=td
        row["first_wick_outside_min"]=min([x for x in (tu,td) if x>=0],default=-1)
        row["two_sided"]=int(tu>=0 and td>=0); row["one_sided"]=int((tu>=0)!=(td>=0))
        # ---- first completed L-minute close outside ----
        b=pm//L; sk=-1; sd=0
        for k in range(int(b.max())+1):
            s=b==k
            if not s.any(): continue
            cc=pc[s][-1]
            if cc>oh: sk,sd=k,1; break
            if cc<ol: sk,sd=k,-1; break
        row["close_signal"]=int(sk>=0); row["close_bar"]=sk+1
        row["first_close_outside_min"]=int((sk+1)*L) if sk>=0 else -1
        row["close_dir"]=sd
        # ---- X-3 TOUCH qualification path (first wick outside) ----
        fw=row["first_wick_outside_min"]
        if fw>=0:
            dt_=1 if (tu>=0 and (td<0 or tu<=td)) else -1
            row["touch_dir"]=dt_
            edge=oh if dt_==1 else ol
            sel=pm>fw                      # strictly AFTER the touch bar
            if sel.any():
                row["touch_entry"]=edge
                path_block(pm[sel]-fw,ph[sel],pl[sel],pc[sel],edge,dt_,W,"tch_",row)
                # break distance within 30 min of first touch
                s30=(pm>fw)&(pm<=fw+30)
                if s30.any():
                    row["break_dist_30_W"]=((ph[s30].max()-oh) if dt_==1 else (ol-pl[s30].min()))/W
        # ---- X-3 CLOSE qualification path ----
        if sk>=0:
            t0=(sk+1)*L; entry=pc[b==sk][-1]; edge=oh if sd==1 else ol
            row["close_entry"]=entry; row["close_beyond_W"]=abs(entry-edge)/W
            sel=pm>=t0
            if sel.any():
                path_block(pm[sel]-t0,ph[sel],pl[sel],pc[sel],entry,sd,W,"cls_",row)
                pmm=pm[sel]-t0; hh=ph[sel]; ll=pl[sel]; cc2=pc[sel]; bb=b[sel]
                # return inside: touch and completed close
                ri=np.where((ll<=oh) if sd==1 else (hh>=ol))[0]
                row["ret_inside_touch_min"]=int(pmm[ri[0]]) if len(ri) else -1
                rc=-1
                for k in sorted(set(bb.tolist())):
                    s2=bb==k; v=cc2[s2][-1]
                    if ol<=v<=oh: rc=int(pmm[s2][-1]); break
                row["ret_inside_close_min"]=rc
                # opposite-side breach after the signal
                ob=np.where((ll<=ol) if sd==1 else (hh>=oh))[0]
                row["opp_breach_min"]=int(pmm[ob[0]]) if len(ob) else -1
                # ---- RETEST path (Analyst-defined tolerance, labelled) ----
                rt=np.where((ll<=edge+RETEST_TOL*W) if sd==1 else (hh>=edge-RETEST_TOL*W))[0]
                if len(rt):
                    i=rt[0]; row["retest_min"]=int(pmm[i])
                    sel2=pmm>pmm[i]
                    if sel2.any():
                        path_block(pmm[sel2]-pmm[i],hh[sel2],ll[sel2],cc2[sel2],edge,sd,W,"rts_",row)
                else: row["retest_min"]=-1
                # ---- FAILED-BREAK REVERSAL path (from close back inside) ----
                if rc>=0:
                    j=np.where(pmm==rc)[0]
                    if len(j):
                        i=j[0]; rev_entry=cc2[i]; rd=-sd
                        sel3=pmm>rc
                        if sel3.any():
                            path_block(pmm[sel3]-rc,hh[sel3],ll[sel3],cc2[sel3],rev_entry,rd,W,"rev_",row)
                            row["rev_entry"]=rev_entry
                            row["rev_dist_mid_W"]=abs(rev_entry-mid)/W
                            row["rev_dist_opp_W"]=abs(rev_entry-(ol if sd==1 else oh))/W
        # ---- X-2 unconditional: excursion both ways from range completion ----
        row["unc_up_W_180"]=(ph[pm<180].max()-pc[0])/W if (pm<180).any() else np.nan
        row["unc_dn_W_180"]=(pc[0]-pl[pm<180].min())/W if (pm<180).any() else np.nan
        row["unc_range_W_EOD"]=(ph.max()-pl.min())/W
        rows.append(row)
    out=pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    out["W_med20_lag"]=out["W"].rolling(20,min_periods=10).median().shift(1)
    out["W_rel"]=out["W"]/out["W_med20_lag"]
    tag=("CTRL1200" if control else ev)
    f=os.path.join(OUT,f"PHASEA_{mk}_{tag}_L{L}.csv"); out.to_csv(f,index=False)
    return out, dict(market=mk,event=tag,L=L,rows=len(out),excluded=excl,ohlc_dropped=nbad,
                     src=src,sha256=sha(src),tz=cfg["tz"],repr=cfg["repr"],unit=cfg["uname"])

if __name__=="__main__":
    prov=[]
    only=sys.argv[1] if len(sys.argv)>1 else None
    for mk,cfg in MARKETS.items():
        if only and mk!=only: continue
        for ev,anc in cfg["events"].items():
            for L in (5,15,30):
                _,p=census(mk,ev,L,anc); prov.append(p); print(f"{mk:7s} {ev:10s} L={L:2d}  n={p['rows']:5d} excl={p['excluded']}")
        for L in (5,15,30):
            _,p=census(mk,"CTRL",L,cfg["ctrl"],control=True); prov.append(p); print(f"{mk:7s} {'CTRL1200':10s} L={L:2d}  n={p['rows']:5d} excl={p['excluded']}")
    pf=os.path.join(BR,"DATA",f"PHASEA_PROVENANCE_{only or 'ALL'}.json")
    with open(pf,"w") as f: json.dump(prov,f,indent=2)
    print("cells:",len(prov))
