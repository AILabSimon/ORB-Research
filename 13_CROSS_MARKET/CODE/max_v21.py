#!/usr/bin/env python3
"""
MAX ARM — RESEARCH_CURRENT v2.2 §C / §E.1 / §F. CeeWilli rules are NOT used here:
no RR_GATE, no Entry-02 rejection, no two-loss stop, no BE, no draw targets.
Arms: {RETEST, CONTINUATION} x {MAX-S1 floored, MAX-S2}.
"""
import numpy as np, pandas as pd, cw_entry02 as CW
R0,R1 = 9*60+30, 9*60+45
DAY_STOP, SESS_END = 11*60+30, 16*60
TICK = CW.TICK; COST = CW.COST

def wick_floor(o,h,l,c,i,n=20):
    a=max(0,i-n); 
    if i<=a: return np.nan
    O,H,L,C=o[a:i],h[a:i],l[a:i],c[a:i]
    up=H-np.maximum(O,C); dn=np.minimum(O,C)-L
    return float(np.nanmax(np.maximum(up,dn))) if len(H) else np.nan

def run(inst, arm="RETEST", stop_rule="S1", d=None):
    if d is None: d=CW.load_ny(inst)
    tick=TICK[inst]; cost=COST[inst]; rows=[]; armed_unfilled=0
    for day,g in d.groupby("day",sort=True):
        rm=g[(g.m>=R0)&(g.m<R1)]
        if len(rm)<10: continue
        ORH,ORL=rm.high.max(),rm.low.min()
        if not np.isfinite(ORH) or ORH<=ORL: continue
        gs=g[(g.m>=R0)&(g.m<SESS_END)].reset_index(drop=True)
        O,H,L,C,M=gs.open.values,gs.high.values,gs.low.values,gs.close.values,gs.m.values
        # ---- S1: 15-minute close outside                                  [C.1]
        b15=CW.resample(gs[gs.m>=R1],15)
        if len(b15)<2: continue
        side=0
        for _,r15 in b15.iterrows():
            if r15.close>ORH: side,bnd=1,ORH; tb=int(r15.m)+15; break
            if r15.close<ORL: side,bnd=-1,ORL; tb=int(r15.m)+15; break
        if side==0: continue
        idx=np.where(M>=tb)[0]
        if len(idx)<10: continue
        used=False; i=idx[0]; n=len(M)
        while i<n-2 and not used:
            if M[i]>=DAY_STOP: break
            # ---- S2 RETEST: >=2 SEPARATE 1m bars interacting with the edge  [H15]
            if arm=="RETEST":
                touches=[]; ri=None
                for j in range(i,n):
                    if M[j]>=DAY_STOP: break
                    if L[j]<=bnd<=H[j]: touches.append(j)
                    if len(touches)>=2 and ((C[j]>bnd) if side==1 else (C[j]<bnd)) and (L[j]<=bnd<=H[j] or j>touches[1]):
                        ri=j; break
                if ri is None: break
            else:                                    # CONTINUATION, no return   [A.1/H16]
                ri=None
                for j in range(i,n):
                    if M[j]>=DAY_STOP: break
                    if (C[j]>bnd) if side==1 else (C[j]<bnd): ri=j; break
                if ri is None: break
                touches=[k for k in range(i,ri+1) if L[k]<=bnd<=H[k]]
            if ri>=n-2: break
            # ---- S4: stop order at the reclaim candle's extreme            [C.3/H17]
            trig = (H[ri]+tick) if side==1 else (L[ri]-tick)
            fi=ri+1
            hit = (H[fi]>=trig) if side==1 else (L[fi]<=trig)
            if not hit:
                armed_unfilled+=1; i=ri+1; continue          # genuine non-fill  [H10]
            px = trig if ((O[fi]<trig) if side==1 else (O[fi]>trig)) else O[fi]
            wf = wick_floor(O,H,L,C,ri)
            if not np.isfinite(wf) or wf<=0: i=fi+1; continue
            raw = abs(px-((L[ri]-tick) if side==1 else (H[ri]+tick)))
            Rd  = max(raw,wf) if stop_rule=="S1" else wf     # [C.4 R3 floor / MAX-S2]
            stop = px - side*Rd
            ex=exr=None; mfe=mae=0.; term=fi
            for j in range(fi,n):
                term=j
                fav=(H[j]-px) if side==1 else (px-L[j]); adv=(px-L[j]) if side==1 else (H[j]-px)
                mfe=max(mfe,fav); mae=max(mae,adv)
                if (L[j]<=stop) if side==1 else (H[j]>=stop): ex,exr=stop,"stop"; break
                if ORL<=C[j]<=ORH: ex,exr=C[j],"invalidation"; break          # [F.3]
                if M[j]>=SESS_END-1: ex,exr=C[j],"eod"; break
            if ex is None: ex,exr=C[-1],"eod"
            gross=((ex-px)*side)/Rd
            rows.append(dict(date=str(pd.Timestamp(day).date()),inst=inst,arm=arm,stop_rule=stop_rule,
                side=side,break_m=tb,reclaim_m=int(M[ri]),entry_m=int(M[fi]),entry=px,stop=stop,
                R_pts=Rd,raw_stop=raw,wick_floor=wf,touches=len(touches),exit=ex,exit_reason=exr,
                gross=gross,net=gross-cost/Rd,mfe_R=mfe/Rd,mae_R=mae/Rd,hold=int(M[term]-M[fi]),
                cost_R=cost/Rd))
            used=True
    T=pd.DataFrame(rows)
    if len(T): T["yr"]=T.date.str[:4].astype(int)
    return T, armed_unfilled
