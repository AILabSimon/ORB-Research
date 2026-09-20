#!/usr/bin/env python3
"""COST ARITHMETIC AUDIT - explicit dollar build-up, no double counting.
Raw gross is computed with slip=0 so that every cost component is applied ONCE, explicitly."""
import numpy as np, pandas as pd, os, json
import exp008_mc7 as E
rng=np.random.default_rng(2026)

# ---- MNQ contract specification ----
SPEC=dict(point_value_usd=2.00, tick_size_pts=0.25, tick_value_usd=0.50)
SCEN={
 "S1 MNQ optimistic": dict(comm_side=0.35, entry_slip=0.25, exit_slip=0.25, stop_extra=0.00),
 "S2 MNQ realistic" : dict(comm_side=0.50, entry_slip=0.50, exit_slip=0.25, stop_extra=0.25),
 "S3 MNQ poor fill" : dict(comm_side=0.75, entry_slip=1.00, exit_slip=0.50, stop_extra=0.50),
 "S4 Dukascopy CFD" : dict(comm_side=0.00, entry_slip=1.46, exit_slip=1.46, stop_extra=0.50),  # 1.42pt spread+slip
 "S5 retail/FTMO"   : dict(comm_side=0.00, entry_slip=3.00, exit_slip=2.50, stop_extra=0.50),
}
def cost_pts(row, s):
    pts = s["entry_slip"] + s["exit_slip"] + (s["stop_extra"] if row=="stop" else 0.0)
    pts += (2*s["comm_side"])/SPEC["point_value_usd"]
    return pts

def audit(t, label):
    raw=t.gross_R.values; R=t.R_pts.values
    print(f"\n########## {label}  (n={len(t)}, median R = {np.median(R):.2f} pts = ${np.median(R)*2:.2f}) ##########")
    print(f"RAW GROSS expectancy (zero slippage, zero commission) = {raw.mean():+.4f}R")
    print(f"{'scenario':20s} {'cost pts':>9} {'cost $':>8} {'cost/R mean':>12} {'cost/R med':>11} {'NET E':>9} {'breakeven':>10} {'obs/req':>8}")
    out={}
    for nm,s in SCEN.items():
        c=np.array([cost_pts(r,s) for r in t.exit_reason.values])
        ratio=c/R
        net=raw-ratio
        out[nm]=dict(cost_pts=float(np.mean(c)),cost_usd=float(np.mean(c)*2),
                     mean_ratio=float(ratio.mean()),med_ratio=float(np.median(ratio)),
                     net=float(net.mean()),breakeven=float(ratio.mean()),
                     obs_over_req=float(raw.mean()/ratio.mean()) if ratio.mean()>0 else np.nan)
        print(f"{nm:20s} {np.mean(c):9.3f} {np.mean(c)*2:8.2f} {ratio.mean():12.4f} {np.median(ratio):11.4f} "
              f"{net.mean():+9.4f} {ratio.mean():+10.4f} {raw.mean()/ratio.mean():8.2f}x")
    return out

if __name__=="__main__":
    print("=== MNQ CONTRACT SPECIFICATION ===")
    print(f"  point value ${SPEC['point_value_usd']:.2f}/pt | tick {SPEC['tick_size_pts']} pts | tick value ${SPEC['tick_value_usd']:.2f}")
    print("\n=== COST COMPONENT BUILD-UP (per round trip, 1 contract) ===")
    for nm,s in SCEN.items():
        cs=cost_pts("stop",s); cn=cost_pts("invalid",s)
        print(f"  {nm:20s} comm ${s['comm_side']:.2f}/side (${2*s['comm_side']:.2f} rt = {2*s['comm_side']/2:.3f} pts) | "
              f"entry slip {s['entry_slip']:.2f} | exit slip {s['exit_slip']:.2f} | stop extra {s['stop_extra']:.2f} "
              f"=> stop-exit {cs:.3f} pts (${cs*2:.2f}), other-exit {cn:.3f} pts (${cn*2:.2f})")
    base=E.run(tag="audit_slip0", slip=0.0)
    base.to_csv(os.path.expanduser("~/mnt/ORB Reserach Sub 2.0/08_EXPERIMENTS/CANDIDATES/EXP008_NAS100_audit_slip0.csv"),index=False)
    print(f"\nexit-reason mix: "+", ".join(f"{k} {100*v:.1f}%" for k,v in base.exit_reason.value_counts(normalize=True).items()))
    a=audit(base,"ALL TRADES (as reported in cycle 2)")
    for thr in [5,10,20]:
        audit(base[base.R_pts>=thr], f"TRADABLE SUBSET  R >= {thr} pts")
