#!/usr/bin/env python3
"""
TSUGI-01 / TSUGI-02  — testing the two genuinely-new claims in the @tsugitrades
15-min ORB carousel against the canonical 1m store.

PRE-REGISTERED 2026-09-17, BEFORE ANY MEASUREMENT.

Source note: @tsugitrades is a DIFFERENT source from Max Options Trading. Results
here do not enter the Max evidence pack and do not bear on Track A.

TSUGI-01  VWAP directional agreement as a filter on the existing CM-C1 candidate.
          Claim on slide: "Above VWAP = Bullish Confirmation" (and mirror).
          Test: gate CM-C1 entries on price-vs-session-VWAP agreeing with the
          ORB direction. Hypothesis: agreeing subset has higher net R than
          disagreeing subset. Pre-registered primary statistic: difference in
          mean net R, agree minus disagree, with a 10,000-draw label permutation.
          Secondary: dev (<=2021) / holdout (>2021) split must agree in sign.

TSUGI-02  Sweep / V-shape recovery (failed break then reverse).
          Claim on slide: price sweeps an ORB level as "manipulation", fails,
          and reverses; enter on the recovery.
          Test: first post-range excursion beyond an ORB edge that closes back
          inside within RECLAIM_MAX minutes -> enter on the reclaiming close in
          the OPPOSITE direction. Two stop constructions reported:
            (a) R = 0.5 * W                       [comparable with CM-C1]
            (b) stop beyond the sweep extreme     [what the model specifies]
          Target in both: next extreme, floored 2R, capped 4R. Max hold 180m.

Everything else is held at the frozen CM-C1 spec.
"""
import numpy as np, pandas as pd, mdload, exp_matrix as E

R0 = 9*60+30; L = 30; SEND = 16*60
TOL = .10; STOPF = .50; MAXHOLD = 180; MAXWAIT = 60
RECLAIM_MAX = 30          # minutes allowed for the sweep to be reclaimed
SWEEP_MIN_W = 0.05        # excursion must exceed 5% of W to count as a sweep
TP_MIN, TP_CAP = 2.0, 4.0
NSHUF = 10000
RNG = np.random.default_rng(20260917)

COSTS = {  # points per round trip, from COST_BASELINE (measured, not assumed)
    "NAS100": 1.23, "US500": 0.50, "XAUUSD": 0.35,
    "EURUSD": 0.00003, "GBPUSD": 0.00008,
}

def vwap_series(h, l, c, v):
    """Session-cumulative VWAP on typical price. Tick volume for CFDs -- proxy."""
    tp = (h + l + c) / 3.0
    cv = np.cumsum(v)
    cv = np.where(cv <= 0, np.nan, cv)
    return np.cumsum(tp * v) / cv

def build(inst, tz="America/New_York", r0=R0):
    raw = mdload.load(inst)
    df = E.prep(raw, tz=tz, r0=r0)
    cost_pts = COSTS[inst]
    r1 = r0 + L
    cm, sw = [], []
    for day, g in df.groupby("day", sort=True):
        m = g.m.values; o=g.open.values; h=g.high.values; l=g.low.values
        c=g.close.values; v=g.volume.values
        rm = (m >= r0) & (m < r1)
        if rm.sum() < L: continue
        oh, ol = h[rm].max(), l[rm].min(); W = oh - ol
        if W <= 0: continue
        vw_all = vwap_series(h, l, c, v)          # anchored at session open (r0)
        post = m >= r1
        if post.sum() < 60: continue
        pm = m[post]-r1; ph=h[post]; pl=l[post]; pc=c[post]; pvw=vw_all[post]

        # ================= CM-C1 (unchanged) + VWAP feature =================
        b = pm // L; sk=-1; dr=0
        for k in range(int(b.max())+1):
            s = b==k
            if not s.any(): continue
            if pc[s][-1] > oh: sk,dr = k,1; break
            if pc[s][-1] < ol: sk,dr = k,-1; break
        if sk >= 0:
            conf=(sk+1)*L; edge = oh if dr==1 else ol; tol=TOL*W
            after = np.where(pm>=conf)[0]
            rt=[i for i in after if ((pl[i]<=edge+tol) if dr==1 else (ph[i]>=edge-tol))]
            if rt:
                ei = rt[0]; lat = int(pm[ei]-conf)
                if lat <= MAXWAIT and ei < len(pm)-5:
                    wimp=(pm>=conf)&(np.arange(len(pm))<=ei)
                    imp = ph[wimp].max() if dr==1 else pl[wimp].min()
                    px = edge
                    # VWAP measured at the bar BEFORE entry -- no look-ahead
                    vw_e = pvw[max(ei-1,0)]; px_ref = pc[max(ei-1,0)]
                    agree = int(np.sign(px_ref - vw_e) == dr) if np.isfinite(vw_e) else -1
                    res = _walk(px, dr, W, ph, pl, pc, pm, ei, STOPF*W, cost_pts)
                    if res:
                        res.update(date=str(pd.Timestamp(day).date()), inst=inst, dir=dr,
                                   W=W, lat=lat, imp_R=abs(imp-px)/res["R_pts"],
                                   vwap_agree=agree,
                                   vwap_dist_W=(px_ref-vw_e)/W if np.isfinite(vw_e) else np.nan)
                        cm.append(res)

        # ================= TSUGI-02  sweep / V-shape recovery ================
        si = None
        for i in range(len(pm)):
            up = ph[i] > oh + SWEEP_MIN_W*W
            dn = pl[i] < ol - SWEEP_MIN_W*W
            if up or dn: si = i; sdir = 1 if up else -1; break
        if si is not None:
            sweep_ext = ph[si] if sdir==1 else pl[si]
            ri = None
            for j in range(si, len(pm)):
                if pm[j] - pm[si] > RECLAIM_MAX: break
                if sdir==1: sweep_ext = max(sweep_ext, ph[j])
                else:       sweep_ext = min(sweep_ext, pl[j])
                inside = (pc[j] < oh) if sdir==1 else (pc[j] > ol)
                if j > si and inside: ri = j; break
            if ri is not None and ri < len(pm)-5:
                tdir = -sdir                       # trade AGAINST the swept side
                px = pc[ri]
                vw_e = pvw[ri]
                agree = int(np.sign(px - vw_e) == tdir) if np.isfinite(vw_e) else -1
                for tag, stop_dist in (("a_halfW", STOPF*W),
                                       ("b_struct", abs(sweep_ext-px)+0.02*W)):
                    res = _walk(px, tdir, W, ph, pl, pc, pm, ri, stop_dist, cost_pts)
                    if res:
                        res.update(date=str(pd.Timestamp(day).date()), inst=inst,
                                   dir=tdir, W=W, stopmode=tag, vwap_agree=agree,
                                   sweep_depth_W=abs(sweep_ext - (oh if sdir==1 else ol))/W,
                                   reclaim_min=int(pm[ri]-pm[si]))
                        sw.append(res)
    return pd.DataFrame(cm), pd.DataFrame(sw)

def _walk(px, dr, W, ph, pl, pc, pm, ei, stop_dist, cost_pts):
    stop = px - dr*stop_dist; R = abs(px-stop)
    if R <= 0: return None
    ext = ph[:ei+1].max() if dr==1 else pl[:ei+1].min()
    dist = (ext-px)*dr
    tp_R = min(max(dist/R, TP_MIN), TP_CAP) if dist>0 else TP_MIN
    tp = px + dr*tp_R*R
    t0 = pm[ei]; ex=exr=None; be=False; trail=stop; mfe=0.; mae=0.; j=ei
    for j in range(ei, len(pm)):
        if pm[j]-t0 > MAXHOLD: ex,exr = pc[j],"time"; break
        fav = (ph[j]-px) if dr==1 else (px-pl[j])
        adv = (px-pl[j]) if dr==1 else (ph[j]-px)
        mfe=max(mfe,fav); mae=max(mae,adv)
        hs = (pl[j]<=trail) if dr==1 else (ph[j]>=trail)
        ht = (ph[j]>=tp)  if dr==1 else (pl[j]<=tp)
        if hs and ht: ex,exr = trail,"ambig"; break
        if hs: ex,exr = trail,("trailstop" if be else "stop"); break
        if ht: ex,exr = tp,"target"; break
        if fav >= R:
            be=True; nt = (ph[j]-R) if dr==1 else (pl[j]+R)
            trail = max(trail,nt,px) if dr==1 else min(trail,nt,px)
    if ex is None: ex,exr = pc[-1],"eod"
    gross = ((ex-px)*dr)/R
    return dict(R_pts=R, entry=px, tp_R=tp_R, exit_reason=exr, gross=gross,
                net=gross - cost_pts/R, mfe_R=mfe/R, mae_R=mae/R,
                hold=int(pm[j]-t0), yr=None)

def perm_diff(a, b, n=NSHUF):
    """Two-sample permutation on the difference of means. Returns obs, p."""
    a=np.asarray(a,float); b=np.asarray(b,float)
    obs = a.mean()-b.mean()
    pool = np.concatenate([a,b]); na=len(a)
    cnt=0
    for _ in range(n):
        RNG.shuffle(pool)
        if abs(pool[:na].mean()-pool[na:].mean()) >= abs(obs): cnt+=1
    return obs, (cnt+1)/(n+1)

def report(t, label):
    if len(t) < 40:
        print(f"  {label:38s} n={len(t)} too few"); return
    net = t.net.values; y = t.date.str[:4].astype(int).values
    bs = np.array([RNG.choice(net,len(net),True).mean() for _ in range(2500)])
    dev = net[y<=2021].mean() if (y<=2021).any() else np.nan
    hol = net[y>2021].mean()  if (y>2021).any()  else np.nan
    print(f"  {label:38s} n={len(net):5d} net={net.mean():+.4f} "
          f"CI[{np.percentile(bs,2.5):+.4f},{np.percentile(bs,97.5):+.4f}] "
          f"win={100*(net>=.05).mean():4.1f}% dev={dev:+.3f} hol={hol:+.3f} "
          f"totR={net.sum():+7.1f}")
