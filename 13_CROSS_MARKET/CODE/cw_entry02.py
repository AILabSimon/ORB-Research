#!/usr/bin/env python3
"""
CEEWILLI ENTRY-02 (BREAK & RETEST) — built to RESEARCH_CURRENT v2.3 §D.11 / §E.2.
Authority: v2.3 §D.11 (rewritten) + §E.2 + §F + §H19-H29 + §I. Max rules are NOT used here.
No optimisation, no thresholds, no filters. 16 cells = {1m,5m} x {HOLD,DEEP} x {BE off,BE on}
x {DRAW-NQ, DRAW-SQ}. Strict-nearest (v2.2) is WITHDRAWN and is not a cell (§D.11.2, H29).
"""
import numpy as np, pandas as pd, mdload

R0,R1 = 9*60+30, 9*60+45          # ORB 09:30-09:44:59
DAY_STOP = 11*60+30               # no entry after 11:30 ET          [B.2]
SESS_END = 16*60
TICK = {"NAS100":0.25,"US500":0.25,"YF_NQ":0.25,"YF_ES":0.25}   # DECLARED
COST = {"NAS100":2.92,"US500":1.26,"YF_NQ":1.25,"YF_ES":1.10}

def load_ny(inst):
    d = mdload.load(inst,side="TRADE") if inst.startswith("YF_") else mdload.load(inst)
    d = d.copy(); d["timestamp"]=pd.to_datetime(d.timestamp,utc=True)
    loc = d.timestamp.dt.tz_convert("America/New_York")
    d["m"]=loc.dt.hour*60+loc.dt.minute
    d["day"]=loc.dt.normalize()
    d["dow"]=loc.dt.dayofweek
    return d.reset_index(drop=True)

# ------------------------------------------------------------------ DRAW  [D.11, H20]
def build_draws(d):
    """Pre-marked levels, ALL computable before 09:30 of the trade day. No lookahead."""
    days = sorted(d.day.unique())
    cash = d[(d.m>=R0)&(d.m<SESS_END)]
    sess = cash.groupby("day").agg(hi=("high","max"), lo=("low","min"))
    full = d.groupby("day").agg(hi=("high","max"), lo=("low","min"), o=("open","first"),
                                c=("close","last"), dow=("dow","first"))
    draws={}
    for k,day in enumerate(days):
        if k==0: continue
        prev = days[k-1]
        lv=[]
        if prev in sess.index: lv += [("prev_session_H",sess.hi[prev]),("prev_session_L",sess.lo[prev])]
        if prev in full.index: lv += [("prev_day_H",full.hi[prev]),("prev_day_L",full.lo[prev])]
        # New Week Opening Gap: last week's final close -> this week's first open   [D.11 #3]
        if full.dow[day] == 0 and prev in full.index:
            lv += [("NWOG_close",full.c[prev]),("NWOG_open",full.o[day])]
        draws[day]=lv
    # --- 15m swing H/L and 5m/15m FVGs from the PREVIOUS session only
    for tf,lab in ((5,"5m"),(15,"15m")):
        r = (d.set_index(d.timestamp)
               .groupby("day")
               .apply(lambda g: g.resample(f"{tf}min",on="timestamp")
                        .agg(high=("high","max"),low=("low","min")).dropna(),
                      include_groups=False))
        for k,day in enumerate(days):
            if k==0: continue
            prev=days[k-1]
            try: g=r.loc[prev]
            except Exception: continue
            H=g.high.values; L=g.low.values
            if len(H)<3: continue
            for i in range(1,len(H)-1):
                if tf==15:                                   # 15m swing H/L   [D.11 #5]
                    if H[i]>H[i-1] and H[i]>H[i+1]: draws[day].append(("15m_swingH",H[i]))
                    if L[i]<L[i-1] and L[i]<L[i+1]: draws[day].append(("15m_swingL",L[i]))
                if H[i-1] < L[i+1]: draws[day].append((f"FVG_{lab}_up", (H[i-1]+L[i+1])/2))
                if L[i-1] > H[i+1]: draws[day].append((f"FVG_{lab}_dn", (L[i-1]+H[i+1])/2))
    return draws

def resample(g, tf):
    if tf==1: return g.reset_index(drop=True)
    if len(g)==0: return g.reset_index(drop=True)   # empty-resample guard [defect fix]
    agg=dict(open=("open","first"),high=("high","max"),low=("low","min"),
             close=("close","last"),m=("m","first"))
    if "volume" in g.columns: agg["volume"]=("volume","sum")
    r = g.set_index("timestamp").resample(f"{tf}min").agg(**agg).dropna().reset_index()
    return r

# ------------------------------------------------------------------ engine
# permitted draw types BY TRADE DIRECTION. A 15m swing LOW is not an upside target for a
# long, and a bearish FVG is not either. [implementation-defect fix, mandate 21]
# [v2.3 §D.11.3] Two permitted arms span the source's unranked-set ambiguity (classification
# D, U-25). Strict-nearest (v2.2) is WITHDRAWN — a nearer non-qualifying level must never
# veto the trade (H28); the engine scans outward and takes the first level that reaches 2R.
DRAW_NQ = {1:{"prev_session_H","prev_day_H","NWOG_close","NWOG_open","15m_swingH","FVG_5m_up","FVG_15m_up"},
          -1:{"prev_session_L","prev_day_L","NWOG_close","NWOG_open","15m_swingL","FVG_5m_dn","FVG_15m_dn"}}
# DRAW-SQ: prior-session structural levels only. FVGs excluded as targets (§D.11.3) — the
# only FVG target the source names is "the next KEY fair value gap" and "key" is undefined;
# the only FVG placed at a specific price (the ORB level) is named an entry confluence, not
# a target (§D.11.1 pro tip).
DRAW_SQ = {1:{"prev_session_H","prev_day_H","NWOG_close","NWOG_open","15m_swingH"},
          -1:{"prev_session_L","prev_day_L","NWOG_close","NWOG_open","15m_swingL"}}
DRAW_SET = {"NQ":DRAW_NQ, "SQ":DRAW_SQ}

def run(inst, tf=1, u22="DEEP", be=False, draws=None, d=None, draw_rule="NQ"):
    """draw_rule: 'NQ' (all permitted types) or 'SQ' (prior-session structural only,
    FVGs excluded) — the two v2.3 §D.11.3 draw arms. No other value is a valid cell."""
    if draw_rule not in DRAW_SET: raise ValueError(f"draw_rule must be 'NQ' or 'SQ', got {draw_rule!r}")
    DRAW_OK = DRAW_SET[draw_rule]
    if d is None: d = load_ny(inst)
    if draws is None: draws = build_draws(d)
    tick = TICK[inst]; cost = COST[inst]; rows=[]; rejects=[]
    for day, g in d.groupby("day", sort=True):
        if day not in draws: continue
        rm = g[(g.m>=R0)&(g.m<R1)]
        if len(rm)<10: continue
        ORH, ORL = rm.high.max(), rm.low.min()
        if not np.isfinite(ORH) or ORH<=ORL: continue
        # resample from 09:30 so the rolling-20 volume median has warm-up, then
        # slice to >=09:45 for the state machine (the scan never sees ORB bars)
        ball = resample(g[(g.m>=R0)&(g.m<SESS_END)], tf)
        if "volume" in ball.columns:
            ball = ball.assign(vmed20=ball.volume.rolling(20,min_periods=3).median().shift(1))
        b = ball[ball.m>=R1].reset_index(drop=True)
        if len(b)<10: continue
        O,H,L,C,M = b.open.values,b.high.values,b.low.values,b.close.values,b.m.values
        # break-quality DIAGNOSTICS, recorded never filtered                [H24, D.2]
        if "volume" in b.columns:
            V = b.volume.values.astype(float); VMED = b.vmed20.values.astype(float)
        else:
            V = np.full(len(b),np.nan); VMED = V
        lv = draws[day]
        used={1:False,-1:False}; losses=0; i=0; n=len(b)
        while i < n-2:
            if losses>=2: break                                            # [H27]
            side=0
            if C[i]>ORH and not used[1]:  side, bnd = 1, ORH
            elif C[i]<ORL and not used[-1]: side, bnd = -1, ORL
            if side==0: i+=1; continue
            bi=i
            brk_body = abs(C[bi]-O[bi]); brk_rng = max(H[bi]-L[bi],1e-12)
            brk_vol_ratio = (V[bi]/VMED[bi]) if (np.isfinite(VMED[bi]) and VMED[bi]>0) else np.nan
            # ---- pullback + rejection scan
            r_i=None; aborted=False; inside_closes=0; touched=False
            for j in range(bi+1, n):
                if M[j] >= DAY_STOP: break
                inside_now = (ORL <= C[j] <= ORH)
                if inside_now: inside_closes += 1
                if (L[j] <= bnd <= H[j]): touched = True
                # REJECTION: interacts with the level AND closes beyond it   [D.6]
                if touched and (L[j] <= bnd <= H[j]) and ((C[j] > bnd) if side==1 else (C[j] < bnd)):
                    r_i=j; break
                if u22=="HOLD" and inside_now:                              # [D.5 arm a]
                    aborted=True; break
            if r_i is None or aborted or r_i>=n-2:
                i = (r_i or bi)+1
                if aborted: i = j+1
                continue
            # ---- stop, entry, RR gate                                     [D.8/D.9]
            seg = slice(bi, r_i+1)
            stop = (L[seg].min()-tick) if side==1 else (H[seg].max()+tick)
            fi = r_i+1; px = O[fi]
            R = abs(px-stop)
            if R<=0: i=fi+1; continue
            # [v2.3 §D.11.3/H28] scan outward from entry; the NEAREST level that ALREADY
            # satisfies >=2R is the draw. A nearer level that does not qualify is a
            # partial-profit level — it is skipped and NEVER vetoes the trade.
            cands = [(nm,v) for nm,v in lv
                     if (v>px if side==1 else v<px) and nm in DRAW_OK[side]]
            cands.sort(key=lambda t: abs(t[1]-px))
            qualifying = [(nm,v) for nm,v in cands if abs(v-px)/R >= 2.0]
            draw_nm, draw = qualifying[0] if qualifying else (None, None)
            rr = (abs(draw-px)/R) if draw is not None else np.nan
            if draw is None:                                                  # [H19] HARD GATE
                rejects.append(dict(date=str(pd.Timestamp(day).date()),inst=inst,tf=tf,u22=u22,
                    draw_rule=draw_rule,be=int(be),
                    side=side,reason=("no_draw" if not cands else "rr_below_2"),
                    rr=rr,R_pts=R,inside_closes=inside_closes,
                    brk_body_ratio=brk_body/brk_rng,brk_vol_ratio=brk_vol_ratio,
                    ORH=ORH,ORL=ORL,break_m=int(M[bi]),rej_m=int(M[r_i]),entry_m=int(M[fi]),
                    entry=px,stop=stop,draw=(draw if draw is not None else np.nan),
                    draw_type=(draw_nm or "NONE"),rr_pre=rr,exit_reason="GATE_REJECT",
                    gross=np.nan,mfe_R=np.nan))
                used[side]=True; i=fi+1; continue
            # ---- manage
            ex=exr=None; mfe=mae=0.; trail=stop; armed=False; term=fi
            for j in range(fi,n):
                term=j
                fav=(H[j]-px) if side==1 else (px-L[j]); adv=(px-L[j]) if side==1 else (H[j]-px)
                mfe=max(mfe,fav); mae=max(mae,adv)
                hs=(L[j]<=trail) if side==1 else (H[j]>=trail)
                ht=(H[j]>=draw) if side==1 else (L[j]<=draw)
                if hs and ht: ex,exr=trail,"ambig"; break
                if hs: ex,exr=trail,("be_stop" if armed else "stop"); break
                if ht: ex,exr=draw,"target"; break
                if ORL <= C[j] <= ORH: ex,exr=C[j],"invalidation"; break     # [D.10]
                if M[j] >= SESS_END-tf: ex,exr=C[j],"eod"; break
                if be and not armed and fav>=R:                              # [D.12 BE arm]
                    armed=True; trail=px
            if ex is None: ex,exr=C[-1],"eod"
            gross=((ex-px)*side)/R
            rows.append(dict(date=str(pd.Timestamp(day).date()),inst=inst,tf=tf,u22=u22,be=int(be),
                draw_rule=draw_rule,
                side=side,ORH=ORH,ORL=ORL,break_m=int(M[bi]),rej_m=int(M[r_i]),entry_m=int(M[fi]),
                entry=px,stop=stop,R_pts=R,draw=draw,draw_type=draw_nm,rr_pre=rr,
                exit=ex,exit_reason=exr,gross=gross,net=gross-cost/R,mfe_R=mfe/R,mae_R=mae/R,
                hold=int(M[term]-M[fi]),inside_closes=inside_closes,
                brk_body_ratio=brk_body/brk_rng, brk_vol_ratio=brk_vol_ratio, cost_R=cost/R,
                pullback_bars=int(sum(1 for q in range(bi+1,r_i+1) if L[q]<=bnd<=H[q])),
                bars_break_to_entry=int(M[fi]-M[bi])))
            if gross<0: losses+=1
            used[side]=True; i=term+1
    T=pd.DataFrame(rows); J=pd.DataFrame(rejects)
    if len(T): T["yr"]=T.date.str[:4].astype(int)
    return T,J
