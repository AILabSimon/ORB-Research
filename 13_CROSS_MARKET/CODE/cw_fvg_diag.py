#!/usr/bin/env python3
"""
EXTERNAL FVG / FAILED-BREAK DIAGNOSTIC — v2.3 cycle, issue #3.

Measures the observed hypothesis: a break of one ORB boundary may only tap/fill an FVG
sitting just beyond that boundary, after which price reverses through the ORB and targets
the opposite boundary. DIAGNOSTIC ONLY (per mandate): this module does not gate, filter or
select Entry-02 trades, does not add an FVG distance/size/tolerance threshold, and does not
invent a trend/bias rule. It reuses the same causal, no-lookahead 3-bar FVG test already in
cw_entry02.build_draws (H[i-2] < L[i] up-gap / L[i-2] > H[i] down-gap) -- applied here to a
day's own bars (pre-market through session end) so intraday gaps are found too, not just the
previous-session gaps build_draws pre-marks as DRAW candidates.

Every break event classified here is keyed off an existing cw_entry02 T (trade) or J (gate
reject) row, so "winner"/"loser" always means the actual, already-computed Entry-02 outcome
for that cell -- this module never re-derives win/loss itself.
"""
import numpy as np, pandas as pd
import cw_entry02 as CW

# ------------------------------------------------------------------ causal FVG scan
def scan_fvgs(b):
    """b: a resampled bar frame (open/high/low/close/m columns), ONE day, session-ordered.
    Returns every 3-bar gap CONFIRMED (i.e. known) at bar i, the source-faithful geometric
    test unchanged from build_draws. No gap-size/tolerance threshold added."""
    H, L, M = b.high.values, b.low.values, b.m.values
    out = []
    for i in range(2, len(b)):
        if H[i-2] < L[i]:
            out.append(dict(i=i, m=int(M[i]), top=float(L[i]), bot=float(H[i-2]), dir=1))
        if L[i-2] > H[i]:
            out.append(dict(i=i, m=int(M[i]), top=float(L[i-2]), bot=float(H[i]), dir=-1))
    return out

def formation_cohort(m):
    """Descriptive cohort only -- never a filter (per mandate)."""
    if m < CW.R0: return "pre_orb"
    if m < CW.R1: return "during_orb"
    return "post_orb"

def _bars_for_day(d, inst, tf, day, cache):
    # DEFECT FIX: trade/reject `date` fields are naive date strings, while d.day is
    # tz-aware America/New_York. A naive == tz-aware comparison matched ZERO rows for
    # every trade, so annotate() silently skipped the entire population and the
    # diagnostic returned an empty (false-null) result. Localise before matching.
    day = pd.Timestamp(day)
    if day.tz is None: day = day.tz_localize("America/New_York")
    key = (inst, tf, day)
    if key in cache: return cache[key]
    g = d[d.day == day]
    g = g[g.m < CW.SESS_END]
    # DEFECT FIX: weekend/holiday sessions in the CFD feed carry only post-16:00 bars,
    # leaving an empty frame that pandas' empty-resample cannot reset_index().
    if len(g) == 0:
        cache[key] = (g, []); return g, []
    b = CW.resample(g, tf).reset_index(drop=True)
    fvgs = scan_fvgs(b)
    cache[key] = (b, fvgs)
    return b, fvgs

# ------------------------------------------------------------------ per-break classification
def classify_break(b, fvgs, side, ORH, ORL, break_m):
    """One break event -> issue fields 1-3,4(partial),5,7. Field 6 (vs continuation-side
    draw/target) is added by annotate() where the trade's own draw price is available.
    `side`: +1 = ORH broke (long), -1 = ORL broke (short). All scanning is causal: only bars
    at or before `break_m` establish "known" FVGs; only bars after `break_m` are scanned for
    touch/reach outcomes."""
    O, H, L, C, M = b.open.values, b.high.values, b.low.values, b.close.values, b.m.values

    known = [f for f in fvgs if f["m"] <= break_m]
    ext_above = [f for f in known if f["bot"] >= ORH]
    ext_below = [f for f in known if f["top"] <= ORL]
    broken = ext_above if side == 1 else ext_below
    # "first" = nearest to the broken boundary, i.e. the one price meets first moving away
    # from the ORB -- regardless of the gap's own bull/bear polarity (fields 1-2 don't
    # distinguish polarity; polarity is recorded separately as a descriptive field).
    first = None
    if broken:
        first = min(broken, key=lambda f: f["bot"]) if side == 1 else max(broken, key=lambda f: f["top"])

    out = dict(
        ext_above_present=len(ext_above) > 0, ext_below_present=len(ext_below) > 0,
        ext_above_n=len(ext_above), ext_below_n=len(ext_below),
        broken_side_fvg_present=first is not None,
        broken_fvg_top=(first["top"] if first else np.nan),
        broken_fvg_bot=(first["bot"] if first else np.nan),
        broken_fvg_dir=(first["dir"] if first else np.nan),
        broken_fvg_formed_m=(first["m"] if first else np.nan),
        broken_fvg_cohort=(formation_cohort(first["m"]) if first else "none"),
    )

    opp = ORL if side == 1 else ORH
    start = int(np.searchsorted(M, break_m, side="right"))
    touch_m = None; body_entered = False; full = False
    opp_touch_m = None; return_inside_m = None
    for j in range(start, len(b)):
        Mj = int(M[j])
        if first is not None:
            hi, lo = H[j], L[j]
            if hi >= first["bot"] and lo <= first["top"]:                      # wick-or-body overlap
                if touch_m is None: touch_m = Mj
                blo, bhi = min(O[j], C[j]), max(O[j], C[j])
                if bhi >= first["bot"] and blo <= first["top"]: body_entered = True
                # "full fill" = price traded all the way through the gap from the approach side
                if side == 1 and hi >= first["top"]: full = True
                if side == -1 and lo <= first["bot"]: full = True
        if return_inside_m is None and (ORL <= C[j] <= ORH): return_inside_m = Mj   # D.10, mirrored
        if opp_touch_m is None and (L[j] <= opp <= H[j]): opp_touch_m = Mj
    kind = "none" if touch_m is None else ("full_fill" if full else ("partial_fill" if body_entered else "wick_only"))
    out.update(fvg_touch_m=touch_m, fvg_touch_kind=kind,
               opposite_touch_m=opp_touch_m, opposite_reached=opp_touch_m is not None,
               return_inside_m=return_inside_m)

    events = [("break", break_m)]
    if touch_m is not None: events.append(("fvg_touch", touch_m))
    if return_inside_m is not None: events.append(("return_inside", return_inside_m))
    if opp_touch_m is not None: events.append(("opposite_touch", opp_touch_m))
    events.sort(key=lambda e: e[1])
    out["sequence"] = ">".join(e[0] for e in events)
    return out

def _target_touch(b, side, break_m, draw):
    O, H, L, C, M = b.open.values, b.high.values, b.low.values, b.close.values, b.m.values
    start = int(np.searchsorted(M, break_m, side="right"))
    for j in range(start, len(b)):
        if (H[j] >= draw) if side == 1 else (L[j] <= draw):
            return int(M[j])
    return None

# ------------------------------------------------------------------ join with existing Entry-02 T/J
def annotate(T, J, inst, tf, d=None, cache=None):
    """T, J: the cw_entry02.run() outputs for ONE cell (tf, u22, be, draw_rule). Returns one
    row per existing Entry-02 event (trade or gate-reject) with the FVG/reversal fields
    attached. Never re-derives win/loss -- `win` is read straight off T.gross.
    `cache`: pass the same dict across calls sharing (inst, tf) to skip re-resampling the
    same day's bars for every cell -- purely a performance aid, no effect on results."""
    if d is None: d = CW.load_ny(inst)
    if cache is None: cache = {}
    rows = []
    for is_trade, src in ((True, T), (False, J)):
        if src is None or len(src) == 0: continue
        for _, row in src.iterrows():
            day = pd.Timestamp(row["date"])
            b, fvgs = _bars_for_day(d, inst, tf, day, cache)
            if len(b) == 0: continue
            side = int(row["side"]); ORH = float(row["ORH"]); ORL = float(row["ORL"])
            break_m = int(row["break_m"])
            cls = classify_break(b, fvgs, side, ORH, ORL, break_m)
            if is_trade:
                draw = row.get("draw", np.nan)
                tgt_m = _target_touch(b, side, break_m, draw) if pd.notna(draw) else None
                opp_m = cls["opposite_touch_m"]
                if tgt_m is not None and (opp_m is None or tgt_m <= opp_m): first_hit = "target"
                elif opp_m is not None: first_hit = "opposite"
                else: first_hit = "neither"
                cls.update(target_touch_m=tgt_m, target_or_opposite_first=first_hit,
                           is_trade=True, win=bool(row["gross"] > 0), gross=row["gross"],
                           exit_reason=row.get("exit_reason"), entry=row.get("entry", np.nan),
                           draw=draw, draw_type=row.get("draw_type"))
            else:
                cls.update(target_touch_m=None, target_or_opposite_first="no_trade",
                           is_trade=False, win=np.nan, gross=np.nan,
                           exit_reason=row.get("exit_reason", "GATE_REJECT"), entry=np.nan,
                           draw=np.nan, draw_type=row.get("draw_type"))
            cls.update(date=row["date"], inst=inst, tf=tf, side=side, ORH=ORH, ORL=ORL,
                       break_m=break_m, u22=row.get("u22"), be=row.get("be"),
                       draw_rule=row.get("draw_rule"))
            rows.append(cls)
    return pd.DataFrame(rows)

def census_all_days(inst, tf, d=None, cache=None):
    """Fields 1-2 for EVERY well-formed ORB day, independent of whether either boundary was
    broken -- the full population, not conditioned on an Entry-02 attempt. Decision time is
    ORB completion (09:45), since presence here is not tied to a specific break."""
    if d is None: d = CW.load_ny(inst)
    if cache is None: cache = {}
    rows = []
    for day, g in d.groupby("day", sort=True):
        rm = g[(g.m >= CW.R0) & (g.m < CW.R1)]
        if len(rm) < 10: continue
        ORH, ORL = rm.high.max(), rm.low.min()
        if not np.isfinite(ORH) or ORH <= ORL: continue
        b, fvgs = _bars_for_day(d, inst, tf, day, cache)
        known = [f for f in fvgs if f["m"] < CW.R1]
        ext_above = [f for f in known if f["bot"] >= ORH]
        ext_below = [f for f in known if f["top"] <= ORL]
        rows.append(dict(date=str(pd.Timestamp(day).date()), inst=inst, tf=tf, ORH=ORH, ORL=ORL,
            ext_above_present=len(ext_above) > 0, ext_below_present=len(ext_below) > 0,
            ext_above_n=len(ext_above), ext_below_n=len(ext_below)))
    return pd.DataFrame(rows)

# ------------------------------------------------------------------ contingency counts
def _touched(ann):
    return ann.broken_side_fvg_present & (ann.fvg_touch_kind != "none")

def primary_counts(ann):
    """Existing Entry-02 winners/losers WITH vs WITHOUT the relevant external-FVG touch,
    counts and rates, as requested."""
    tr = ann[ann.is_trade == True]
    if len(tr) == 0:
        return dict(n_with=0, n_without=0, winners_with=0, winners_without=0,
                     losers_with=0, losers_without=0, win_rate_with=np.nan,
                     win_rate_without=np.nan, loss_rate_with=np.nan, loss_rate_without=np.nan)
    touch = _touched(tr)
    with_t, without_t = tr[touch], tr[~touch]
    n_with, n_without = len(with_t), len(without_t)
    winners_with = int(with_t.win.sum()); winners_without = int(without_t.win.sum())
    losers_with = n_with - winners_with; losers_without = n_without - winners_without
    return dict(
        n_with=n_with, n_without=n_without,
        winners_with=winners_with, winners_without=winners_without,
        losers_with=losers_with, losers_without=losers_without,
        win_rate_with=(winners_with / n_with if n_with else np.nan),
        win_rate_without=(winners_without / n_without if n_without else np.nan),
        loss_rate_with=(losers_with / n_with if n_with else np.nan),
        loss_rate_without=(losers_without / n_without if n_without else np.nan),
    )

def reversal_sequence(ann):
    """broken-side FVG touched -> opposite ORB reached, all four cells -- over EVERY break
    event in `ann` (trades AND gate-rejects), since the reversal hypothesis is about raw
    price behaviour, not only trades that cleared the RR gate."""
    touch = _touched(ann); reached = ann.opposite_reached
    n11 = int((touch & reached).sum()); n10 = int((touch & ~reached).sum())
    n01 = int((~touch & reached).sum()); n00 = int((~touch & ~reached).sum())
    return dict(
        fvg_touch_opp_reached=n11, fvg_touch_opp_not_reached=n10,
        no_touch_opp_reached=n01, no_touch_opp_not_reached=n00,
        rate_opp_given_touch=(n11 / (n11 + n10) if (n11 + n10) else np.nan),
        rate_opp_given_no_touch=(n01 / (n01 + n00) if (n01 + n00) else np.nan),
    )

def cohort_counts(ann):
    """Descriptive only: when the broken-side external FVG formed, relative to the ORB."""
    have = ann[ann.broken_side_fvg_present]
    return have.broken_fvg_cohort.value_counts().to_dict()

TREND_BIAS_NOTE = (
    "Trend/bias interaction cannot be tested source-faithfully this cycle. RESEARCH_CURRENT "
    "v2.3 D.3/U-24: CeeWilli's HTF bias has no mechanical definition anywhere in the source "
    "-- a single undated pre-open judgement, gating none of the four models. No objective "
    "trend/bias field exists in this dataset to cross-tab against. This is withheld pending a "
    "Research ruling that supplies a mechanical definition; it is not computed, approximated, "
    "or proxied here."
)

def build_report(ann, label):
    """Markdown block: primary counts, reversal sequence, formation cohorts, pooled and by
    side, for one (inst,tf,u22,be,draw_rule) cell's annotated frame."""
    out = [f"\n### {label}  (n_events={len(ann)}, n_trades={int((ann.is_trade==True).sum())})\n"]
    def block(sub, name):
        pc = primary_counts(sub); rs = reversal_sequence(sub)
        out.append(f"**{name}**")
        out.append(f"- winners WITH touch: {pc['winners_with']}  ·  winners WITHOUT: {pc['winners_without']}")
        out.append(f"- losers WITH touch: {pc['losers_with']}  ·  losers WITHOUT: {pc['losers_without']}")
        out.append(f"- n(touched)={pc['n_with']} n(not touched)={pc['n_without']}")
        out.append(f"- win rate touched: {pc['win_rate_with']}  ·  win rate not touched: {pc['win_rate_without']}")
        out.append(f"- loss rate touched: {pc['loss_rate_with']}  ·  loss rate not touched: {pc['loss_rate_without']}")
        out.append(f"- reversal: touch->opp reached {rs['fvg_touch_opp_reached']}, "
                    f"touch->opp NOT reached {rs['fvg_touch_opp_not_reached']}, "
                    f"no touch->opp reached {rs['no_touch_opp_reached']}, "
                    f"no touch->opp NOT reached {rs['no_touch_opp_not_reached']}")
        out.append(f"- P(opp reached | touched)={rs['rate_opp_given_touch']}  "
                    f"P(opp reached | not touched)={rs['rate_opp_given_no_touch']}")
        out.append(f"- formation cohorts (broken-side FVG): {cohort_counts(sub)}\n")
    block(ann, "POOLED")
    block(ann[ann.side == 1], "LONG (ORH break)")
    block(ann[ann.side == -1], "SHORT (ORL break)")
    out.append(TREND_BIAS_NOTE)
    return "\n".join(out)
