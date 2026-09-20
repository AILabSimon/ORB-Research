#!/usr/bin/env python3
"""COST/R FEASIBILITY GATE. Entry at the ORB edge, stop at the opposite edge => R = W exactly,
in instrument units. Each cost component applied EXACTLY ONCE. Instrument economics are distinct:
NQ != MNQ, ES != MES, GC != MGC, CFD != futures, XAUUSD spread != GC commission."""
import pandas as pd, numpy as np, os
R=os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/13_CROSS_MARKET/CENSUS/RESULTS")

# name, value per point/$move, tick, comm/side $, spread pts, entry slip, exit slip, stop extra, MEASURED?
INSTR={
 # --- true futures economics (NO DATA - shown to size the opportunity, never as a result) ---
 "NQ  (futures)"  : dict(pv=20.0, tick=0.25, comm=2.50, spr=0.25, es=0.25, xs=0.25, sx=0.25, data=False),
 "MNQ (futures)"  : dict(pv=2.00, tick=0.25, comm=0.50, spr=0.25, es=0.25, xs=0.25, sx=0.25, data=False),
 "ES  (futures)"  : dict(pv=50.0, tick=0.25, comm=2.50, spr=0.25, es=0.25, xs=0.25, sx=0.25, data=False),
 "MES (futures)"  : dict(pv=5.00, tick=0.25, comm=0.50, spr=0.25, es=0.25, xs=0.25, sx=0.25, data=False),
 "GC  (futures)"  : dict(pv=100.0,tick=0.10, comm=2.50, spr=0.10, es=0.10, xs=0.10, sx=0.10, data=False),
 "MGC (futures)"  : dict(pv=10.0, tick=0.10, comm=0.50, spr=0.10, es=0.10, xs=0.10, sx=0.10, data=False),
 # --- what we actually hold ---
 "NAS100 CFD"     : dict(pv=1.00, tick=0.01, comm=0.00, spr=1.42, es=0.50, xs=0.50, sx=0.50, data=True,  note="spread MEASURED from BID/ASK"),
 "US500 CFD"      : dict(pv=1.00, tick=0.01, comm=0.00, spr=0.51, es=0.25, xs=0.25, sx=0.25, data=True,  note="spread MEASURED from BID/ASK"),
 "XAUUSD spot"    : dict(pv=1.00, tick=0.01, comm=0.00, spr=0.30, es=0.15, xs=0.15, sx=0.15, data=True,  note="spread ASSUMED - no ASK series exists"),
 "EURUSD spot"    : dict(pv=1.00, tick=0.1,  comm=0.70, spr=0.50, es=0.30, xs=0.30, sx=0.20, data=True,  note="spread MEASURED p90; commission in pips"),
 "GBPUSD spot"    : dict(pv=1.00, tick=0.1,  comm=1.20, spr=1.20, es=0.50, xs=0.50, sx=0.30, data=True,  note="spread MEASURED p90; commission in pips"),
}
def rt_cost(k):
    """round-trip cost in INSTRUMENT POINTS (one application of each component)"""
    i=INSTR[k]
    comm_pts = (2*i["comm"])/i["pv"] if i["pv"]>0 else 0.0
    return i["spr"] + i["es"] + i["xs"] + i["sx"] + comm_pts, comm_pts

MAP={("NAS100","CASH0930"):["NAS100 CFD","NQ  (futures)","MNQ (futures)"],
     ("US500","CASH0930"):["US500 CFD","ES  (futures)","MES (futures)"],
     ("XAUUSD","COMEX0820"):["XAUUSD spot","GC  (futures)","MGC (futures)"],
     ("XAUUSD","CASH0930"):["XAUUSD spot","GC  (futures)","MGC (futures)"],
     ("EURUSD","LON0800"):["EURUSD spot"],
     ("GBPUSD","LON0800"):["GBPUSD spot"]}

print("### COST COMPONENT BUILD-UP (round trip, 1 contract/lot, instrument points)")
print(f"{'instrument':16s} {'pt value':>9} {'tick':>6} {'comm/side':>10} {'comm RT pts':>12} {'spread':>7} {'entry':>6} {'exit':>6} {'stopX':>6} {'TOTAL pts':>10}  note")
for k in INSTR:
    c,cp=rt_cost(k); i=INSTR[k]
    print(f"{k:16s} {i['pv']:9.2f} {i['tick']:6.2f} {i['comm']:10.2f} {cp:12.3f} {i['spr']:7.2f} {i['es']:6.2f} {i['xs']:6.2f} {i['sx']:6.2f} {c:10.3f}  {i.get('note','NO DATA HELD - sizing only')}")

print("\n### COST/R FEASIBILITY TABLE  (R = W, i.e. ORB-edge entry with opposite-edge stop)")
print(f"{'cell':22s} {'L':>3} {'instrument':16s} {'meanW':>8} {'medW':>8} {'cost pts':>9} {'costR mean':>11} {'costR med':>10} {'costR p90':>10} {'req gross E':>12} {'P2R%':>6} {'gate':>6}")
mx=pd.read_csv("COMPARISON/MARKET_FAMILY_MATRIX.csv")
rows=[]
for (mk,ev),insts in MAP.items():
    for L in (5,15,30):
        d=pd.read_csv(f"{R}/PHASEA_{mk}_{ev}_L{L}.csv"); d=d[d.W>=0.5*d.W_med20_lag]
        W=d.W.values
        sub=mx[(mk==mx.mk)&(ev==mx.ev)&(mx.L==L)&(mx.fam=="touch")]
        p2r=float(sub.P2R.iloc[0]) if len(sub) else np.nan
        for k in insts:
            c,_=rt_cost(k); ratio=c/W
            req=ratio.mean()
            gate="PASS" if req<=0.15 else ("MARGINAL" if req<=0.30 else "FAIL")
            rows.append(dict(cell=f"{mk} {ev}",L=L,instr=k,meanW=W.mean(),medW=np.median(W),cost=c,
                             mean=req,med=np.median(ratio),p90=np.percentile(ratio,90),P2R=p2r,gate=gate,
                             held=INSTR[k]["data"]))
            print(f"{mk+' '+ev:22s} {L:3d} {k:16s} {W.mean():8.2f} {np.median(W):8.2f} {c:9.3f} {req:11.4f} {np.median(ratio):10.4f} {np.percentile(ratio,90):10.4f} {req:+12.4f} {p2r:6.1f} {gate:>6}")
pd.DataFrame(rows).to_csv("COSTS/COST_R_FEASIBILITY.csv",index=False)
