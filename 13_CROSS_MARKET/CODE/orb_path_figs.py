#!/usr/bin/env python3
"""
CORE-STRATEGY PATH VISUALS -- six scenario classes, side by side.
Same candle/ORB-band convention as cw_fvg_figs.py. Selection is deterministic (first N days of
the class, by date). No economics, no size, no outcome-quality filter.

Markers:  dotted amber = break   dashed grey = 1m close back inside (invalidation, V8 06:11)
          solid teal  = newer extreme WITH (continuation, V4 05:37)
          solid red   = newer extreme AGAINST (failed-break confirmation, V8 16:33)
          solid blue  = opposite ORB boundary touched      dashed green = midline
"""
import os
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cw_entry02 as CW

OUT = "../OUTPUTS/FIGS/CORE_PATH"; os.makedirs(OUT, exist_ok=True)
TF = 5

def _mm(v):
    return None if (v is None or (isinstance(v, float) and np.isnan(v))) else float(v)

def panel(ax, b, r, title):
    M0 = b.m.values
    bi = int(np.searchsorted(M0, r["break_m"]))
    end_m = r["break_m"]
    for k in ("inside_m", "newer_extreme_with_m", "newer_extreme_against_m", "opp_m", "mid_m"):
        v = _mm(r.get(k))
        if v is not None: end_m = max(end_m, v)
    ei = int(np.searchsorted(M0, end_m))
    lo_i, hi_i = max(0, bi - 12), min(len(b), max(bi + 40, ei + 12))
    O, H, L, C, M = (b.open.values[lo_i:hi_i], b.high.values[lo_i:hi_i], b.low.values[lo_i:hi_i],
                     b.close.values[lo_i:hi_i], b.m.values[lo_i:hi_i])
    ORH, ORL, mid = r["ORH"], r["ORL"], r["mid"]
    ax.add_patch(Rectangle((0, ORL), len(O), ORH - ORL, fc="#cfe4cb", alpha=.55, ec="none", zorder=0))
    ax.axhline(ORH, color="#6f9c68", lw=1); ax.axhline(ORL, color="#6f9c68", lw=1)
    ax.axhline(mid, color="#6f9c68", lw=.8, ls="--", alpha=.8)
    for i in range(len(O)):
        col = "#2c7d72" if C[i] >= O[i] else "#a33c26"
        ax.plot([i, i], [L[i], H[i]], color=col, lw=.7, zorder=2)
        ax.add_patch(Rectangle((i - .32, min(O[i], C[i])), .64, max(abs(C[i] - O[i]), 1e-9),
                               fc=col, ec=col, lw=.3, zorder=3))
    def V(mm, col, ls="-"):
        mm = _mm(mm)
        if mm is None: return
        w = np.where(M >= mm)[0]
        if len(w): ax.axvline(w[0], color=col, lw=1.1, ls=ls, alpha=.92, zorder=4)
    V(r["break_m"], "#8a6209", ":")
    V(r.get("inside_m"), "#555555", "--")
    if r["outcome"] == "continuation": V(r.get("newer_extreme_with_m"), "#0f6b64")
    if r["outcome"] == "failed-break": V(r.get("newer_extreme_against_m"), "#c0392b")
    V(r.get("opp_m"), "#1f5fa8")
    ax.set_title(title, fontsize=6.0, loc="left")
    ax.set_xticks([]); ax.tick_params(labelsize=5.0)
    y_lo, y_hi = min(L.min(), ORL), max(H.max(), ORH)
    pad = .05 * (y_hi - y_lo)
    ax.set_ylim(y_lo - pad, y_hi + pad); ax.set_xlim(-1, len(O))

def hhmm(m):
    m = _mm(m)
    return "--" if m is None else f"{int(m)//60:02d}:{int(m)%60:02d}"

CLASSES = [
    ("A_ORH_break_retrace_CONTINUATION",  1, "continuation", None),
    ("B_ORH_break_FAILED_to_ORL",        1, "failed-break", True),
    ("C_ORH_break_AMBIGUOUS",            1, "neither",      None),
    ("D_ORL_break_retrace_CONTINUATION", -1, "continuation", None),
    ("E_ORL_break_FAILED_to_ORH",        -1, "failed-break", True),
    ("F_ORL_break_AMBIGUOUS",            -1, "neither",      None),
]

def build(inst, n_each=3):
    d = pd.read_parquet(f"../WORK/PATH_CENSUS_{inst}_CLASSIFIED.parquet")
    raw = CW.load_ny(inst)
    cache = {}
    def bars(day):
        if day in cache: return cache[day]
        dd = pd.Timestamp(day)
        if dd.tz is None: dd = dd.tz_localize("America/New_York")
        g = raw[raw.day == dd]; g = g[g.m < CW.SESS_END]
        b = CW.resample(g, TF).reset_index(drop=True) if len(g) else g
        cache[day] = b; return b
    picks = []
    for name, side, out, need_opp in CLASSES:
        s = d[(d.side == side) & (d.outcome == out) & (d.retraced.astype(bool))]
        if need_opp: s = s[s.opp_reached.fillna(False).astype(bool)]
        s = s.sort_values("date")
        picks.append((name, s.head(n_each)))
    rows = max(len(p[1]) for p in picks)
    fig, axes = plt.subplots(rows, 6, figsize=(24, 4.2 * rows))
    axes = np.atleast_2d(axes)
    for c, (name, s) in enumerate(picks):
        for rI in range(rows):
            ax = axes[rI, c]
            if rI >= len(s): ax.axis("off"); continue
            r = s.iloc[rI]
            b = bars(r["date"])
            if not len(b): ax.axis("off"); continue
            t = (f"{name}\n{inst} {r['date']}  W={r['W']:.1f}\n"
                 f"brk {hhmm(r['break_m'])}  ret {hhmm(r['retrace_m'])}  inside {hhmm(r['inside_m'])}\n"
                 f"with {hhmm(r['newer_extreme_with_m'])}  agst {hhmm(r['newer_extreme_against_m'])}  "
                 f"mid {hhmm(r['mid_m'])}  opp {hhmm(r['opp_m'])}")
            panel(ax, b, r, t)
    fig.suptitle(f"{inst} -- ORB core-strategy path classes (5m bars). Columns A-F: "
                 "ORH continuation | ORH failed->ORL | ORH ambiguous | ORL continuation | ORL failed->ORH | ORL ambiguous",
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.965])
    p = f"{OUT}/PATH_CLASSES_{inst}.png"
    fig.savefig(p, dpi=115); plt.close(fig)
    print("wrote", p)
    return p

if __name__ == "__main__":
    for inst in ("NAS100", "US500"): build(inst)
