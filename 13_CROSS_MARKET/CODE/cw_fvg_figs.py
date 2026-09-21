#!/usr/bin/env python3
"""
EXTERNAL FVG VISUAL REVIEW PACK — v2.3 diagnostic, issue #3.
Same candle/ORB-band drawing convention as v22_figs.py / forensic_pack.py. Renders the five
requested scenario classes; selection is deterministic (first N matches by date), never a
economics- or size-based filter.
"""
import os
import numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import cw_entry02 as CW

def panel(ax, b, row, title):
    M = b.m.values
    bi = int(np.searchsorted(M, row["break_m"]))
    # DEFECT FIX: the window was a fixed +60 bars from the break, which frequently ended
    # BEFORE the opposite-ORB touch the panel is meant to evidence (e.g. NAS100 2016-01-07:
    # fvg touch 10:28, opposite touch 13:12). Extend to cover every marked event + padding.
    end_m = row["break_m"]
    for k in ("fvg_touch_m", "return_inside_m", "opposite_touch_m"):
        v = row.get(k)
        if v is not None and not (isinstance(v, float) and np.isnan(v)): end_m = max(end_m, v)
    ei = int(np.searchsorted(M, end_m))
    lo_i, hi_i = max(0, bi - 20), min(len(b), max(bi + 60, ei + 15))
    O, H, L, C, M = (b.open.values[lo_i:hi_i], b.high.values[lo_i:hi_i], b.low.values[lo_i:hi_i],
                      b.close.values[lo_i:hi_i], b.m.values[lo_i:hi_i])
    ORH, ORL = row["ORH"], row["ORL"]
    ax.add_patch(Rectangle((0, ORL), len(O), ORH - ORL, fc="#cfe4cb", alpha=.55, ec="none", zorder=0))
    ax.axhline(ORH, color="#6f9c68", lw=1); ax.axhline(ORL, color="#6f9c68", lw=1)
    if row.get("broken_side_fvg_present"):
        top, bot = row["broken_fvg_top"], row["broken_fvg_bot"]
        ax.add_patch(Rectangle((0, bot), len(O), top - bot, fc="#d9b25b", alpha=.35, ec="#a5780f", lw=.6, zorder=1))
    for i in range(len(O)):
        col = "#2c7d72" if C[i] >= O[i] else "#a33c26"
        ax.plot([i, i], [L[i], H[i]], color=col, lw=.6, zorder=2)
        ax.add_patch(Rectangle((i - .32, min(O[i], C[i])), .64, max(abs(C[i] - O[i]), 1e-9),
                                fc=col, ec=col, lw=.3, zorder=3))
    def V(mm, col, ls="-"):
        if mm is None or (isinstance(mm, float) and np.isnan(mm)): return
        w = np.where(M >= mm)[0]
        if len(w): ax.axvline(w[0], color=col, lw=1.0, ls=ls, alpha=.9, zorder=4)
    V(row["break_m"], "#8a6209", ":")
    V(row.get("fvg_touch_m"), "#a5780f")
    V(row.get("return_inside_m"), "#555555", "--")
    V(row.get("opposite_touch_m"), "#1f5fa8")
    if row.get("is_trade") and pd.notna(row.get("entry", np.nan)):
        ax.axhline(row["entry"], color="#1f5fa8", lw=1.0)
        if pd.notna(row.get("draw", np.nan)): ax.axhline(row["draw"], color="#0f6b64", lw=1.0)
    ax.set_title(title, fontsize=6.2, loc="left")
    ax.set_xticks([]); ax.tick_params(labelsize=5.2)
    y_lo, y_hi = L.min(), H.max()
    if row.get("broken_side_fvg_present"):
        y_lo, y_hi = min(y_lo, row["broken_fvg_bot"]), max(y_hi, row["broken_fvg_top"])
    pad = .04 * (y_hi - y_lo)
    ax.set_ylim(y_lo - pad, y_hi + pad); ax.set_xlim(-1, len(O))

def select_examples(ann, n_each=2):
    """Deterministic, unfiltered-beyond-class selection for the five requested scenarios."""
    touched = ann.broken_side_fvg_present & (ann.fvg_touch_kind != "none")
    scen = {
        "ORH_break_FVG_touched_ORL_reached":  ann[(ann.side == 1)  & touched & ann.opposite_reached],
        "ORH_break_FVG_touched_continuation": ann[(ann.side == 1)  & touched & ~ann.opposite_reached],
        "ORL_break_FVG_touched_ORH_reached":  ann[(ann.side == -1) & touched & ann.opposite_reached],
        "ORL_break_FVG_touched_continuation": ann[(ann.side == -1) & touched & ~ann.opposite_reached],
        "FVG_present_not_touched":            ann[ann.broken_side_fvg_present & (ann.fvg_touch_kind == "none")],
    }
    return {k: v.sort_values("date").head(n_each) for k, v in scen.items()}

def grid(rows_df, bars_by_idx, fn, sup):
    n = len(rows_df)
    if n == 0: return False
    r = (n + 1) // 2
    fig, axes = plt.subplots(r, 2, figsize=(13, 5.2 * r)); axes = np.array(axes).reshape(-1)
    for a in axes[n:]: a.axis("off")
    for a, (idx, row) in zip(axes, rows_df.iterrows()):
        title = (f"{row['inst']} {row['date']} {'L' if row['side']==1 else 'S'} | "
                 f"brk {int(row['break_m'])//60:02d}:{int(row['break_m'])%60:02d} "
                 f"touch={row['fvg_touch_kind']} opp={'Y' if row['opposite_reached'] else 'N'} "
                 f"seq={row['sequence']}"
                 + (f" | {row['exit_reason']} {row['gross']:+.2f}R" if row.get("is_trade") else " | no trade"))
        panel(a, bars_by_idx[idx], row, title)
    fig.suptitle(sup, fontsize=10, y=.999)
    fig.tight_layout(rect=[0, 0, 1, .985]); fig.savefig(fn, dpi=125); plt.close(fig)
    return True

def build_pack(ann, d_by_inst, outdir, n_each=2):
    """d_by_inst: {inst: CW.load_ny(inst) frame}. Writes one PNG per scenario class that has
    at least one example. Returns the list of files actually written."""
    os.makedirs(outdir, exist_ok=True)
    scen = select_examples(ann, n_each=n_each)
    written = []
    for name, rows in scen.items():
        if len(rows) == 0: continue
        bars_by_idx = {}
        for idx, row in rows.iterrows():
            d = d_by_inst[row["inst"]]
            # DEFECT FIX (same class as cw_fvg_diag._bars_for_day): row["date"] is a naive
            # date string, d.day is tz-aware NY -- a naive comparison matched zero rows and
            # produced empty panels. Localise before matching.
            _day = pd.Timestamp(row["date"])
            if _day.tz is None: _day = _day.tz_localize("America/New_York")
            g = d[d.day == _day]
            g = g[g.m < CW.SESS_END]
            bars_by_idx[idx] = CW.resample(g, row["tf"]).reset_index(drop=True)
        fn = os.path.join(outdir, f"FVG_{name}.png")
        if grid(rows, bars_by_idx, fn, f"External FVG diagnostic -- {name} -- n={len(rows)}"):
            written.append(fn)
    return written
