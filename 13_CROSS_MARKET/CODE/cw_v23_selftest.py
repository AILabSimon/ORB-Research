#!/usr/bin/env python3
"""
SELF-TESTS — CeeWilli v2.3 rebuild + external FVG diagnostic (issue #3).

Synthetic data only. Does NOT touch the market-data store, so this is the one piece of the
v2.3 deliverable runnable in an environment without `~/mnt/Market Data` -- e.g. CI. Plain
assertions, no pytest (matches the rest of this codebase). Run:

    python3 cw_v23_selftest.py

NOTE: the sandboxed session that wrote this file could not execute Python at all (every
`python3` invocation was denied by the harness), so these tests are believed correct by
manual review but have NOT been run anywhere yet. Run them first on the Mac, before trusting
any of this cycle's code against real data.
"""
import numpy as np, pandas as pd
import cw_entry02 as CW
import cw_fvg_diag as FD

PASS = []; FAIL = []

def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(f"{name}" + (f" -- {detail}" if detail and not cond else ""))

# ------------------------------------------------------------------ synthetic day builder
DAY = pd.Timestamp("2026-01-05")   # Monday; NWOG logic irrelevant here, draws are injected directly

def mkbars(rows):
    """rows: list of (m, o, h, l, c) 1-minute bars. Returns a `d`-shaped frame matching
    cw_entry02.load_ny's output schema (day, m, dow, timestamp, open/high/low/close)."""
    df = pd.DataFrame(rows, columns=["m", "open", "high", "low", "close"])
    df["day"] = DAY
    df["dow"] = 0
    df["timestamp"] = DAY + pd.to_timedelta(df["m"], unit="m")
    return df

def orb_bars(orh=100.0, orl=99.0):
    """15 1m bars spanning the 09:30-09:44 ORB window. The first bar carries both extremes
    exactly (orh, orl); the rest sit safely inside them, so ORH/ORL are deterministic."""
    rows = [(CW.R0, 99.5, orh, orl, 99.5)]
    rows += [(m, 99.5, 99.55, 99.45, 99.5) for m in range(CW.R0 + 1, CW.R1)]
    return rows

# ------------------------------------------------------------------ FVG scan
def test_fvg_scan_up_gap():
    b = pd.DataFrame(dict(open=[9.0, 9.3, 10.8], high=[9.5, 11.0, 11.2],
                           low=[8.8, 9.2, 10.5], close=[9.3, 10.8, 11.0], m=[0, 1, 2]))
    fvgs = FD.scan_fvgs(b)
    ok = len(fvgs) == 1 and fvgs[0]["dir"] == 1 and fvgs[0]["bot"] == 9.5 and fvgs[0]["top"] == 10.5 and fvgs[0]["i"] == 2
    check("fvg_scan_up_gap", ok, str(fvgs))

def test_fvg_scan_down_gap():
    b = pd.DataFrame(dict(open=[11.0, 10.5, 8.8], high=[11.2, 10.7, 9.0],
                           low=[10.8, 9.5, 8.5], close=[11.0, 9.7, 8.9], m=[0, 1, 2]))
    fvgs = FD.scan_fvgs(b)
    ok = len(fvgs) == 1 and fvgs[0]["dir"] == -1 and fvgs[0]["top"] == 10.8 and fvgs[0]["bot"] == 9.0 and fvgs[0]["i"] == 2
    check("fvg_scan_down_gap", ok, str(fvgs))

def test_fvg_scan_no_gap():
    b = pd.DataFrame(dict(open=[9.0, 9.3, 9.6], high=[9.5, 9.8, 10.0],
                           low=[8.8, 9.1, 9.4], close=[9.3, 9.6, 9.9], m=[0, 1, 2]))
    check("fvg_scan_no_gap", len(FD.scan_fvgs(b)) == 0)

# ------------------------------------------------------------------ Entry-02 v2.3 draw mechanics
def _base_rows():
    rows = orb_bars(100.0, 99.0)
    rows += [
        (585, 99.5, 100.6, 99.4, 100.6),   # break: close > ORH=100
        (586, 100.6, 100.6, 99.9, 100.3),  # touches ORH (low<=100<=high) and closes beyond -> rejection
        (587, 100.35, 100.9, 100.2, 100.5),# fill bar: open = entry px = 100.35
    ]
    # padding so the management loop and n-2 index guards have room
    rows += [(m, 103.5, 103.6, 103.4, 103.5) for m in range(588, 620)]
    return rows

def test_h28_nearer_nonqualifying_never_vetoes():
    """§D.11.3 / H28: a nearer level that does NOT reach 2R must not refuse the trade -- the
    farther qualifying level must be selected instead."""
    d = mkbars(_base_rows())
    day = DAY
    # entry px will be 100.35, stop ~99.15, R ~1.20 -> 2R ~2.40
    # near level (0.65 away) does NOT qualify; far level (2.65 away, ~2.21R) DOES.
    draws = {day: [("prev_session_H", 101.0), ("NWOG_open", 103.0)]}
    T, J = CW.run("NAS100", tf=1, u22="DEEP", be=False, draws=draws, d=d, draw_rule="NQ")
    check("h28_trade_taken_not_gate_rejected", len(T) == 1 and len(J) == 0, f"T={T.to_dict('records')} J={J.to_dict('records')}")
    if len(T) == 1:
        check("h28_farther_qualifying_level_selected", T.iloc[0].draw_type == "NWOG_open" and abs(T.iloc[0].draw - 103.0) < 1e-9)
        check("h28_rr_at_least_2", T.iloc[0].rr_pre >= 2.0)

def test_draw_sq_excludes_fvg():
    """DRAW-SQ must exclude FVG target types even when an FVG is the only qualifying level --
    NQ takes the trade via the FVG, SQ gate-rejects the same day/side."""
    d = mkbars(_base_rows())
    day = DAY
    draws = {day: [("prev_session_H", 100.5), ("FVG_5m_up", 103.5)]}   # only FVG_5m_up reaches 2R
    T_nq, J_nq = CW.run("NAS100", tf=1, u22="DEEP", be=False, draws=draws, d=d, draw_rule="NQ")
    T_sq, J_sq = CW.run("NAS100", tf=1, u22="DEEP", be=False, draws=draws, d=d, draw_rule="SQ")
    check("draw_nq_takes_fvg_target", len(T_nq) == 1 and T_nq.iloc[0].draw_type == "FVG_5m_up",
          f"T_nq={T_nq.to_dict('records')}")
    check("draw_sq_gate_rejects_no_structural_qualifies", len(T_sq) == 0 and len(J_sq) == 1,
          f"T_sq={T_sq.to_dict('records')} J_sq={J_sq.to_dict('records')}")
    if len(J_sq) == 1:
        check("draw_sq_reject_reason_rr_below_2", J_sq.iloc[0].reason == "rr_below_2")

def test_run_rejects_invalid_draw_rule():
    d = mkbars(_base_rows())
    try:
        CW.run("NAS100", tf=1, d=d, draws={DAY: []}, draw_rule="nearest")
        check("run_rejects_invalid_draw_rule", False, "did not raise")
    except ValueError:
        check("run_rejects_invalid_draw_rule", True)

# ------------------------------------------------------------------ FVG diagnostic: touch/fill classification
def _synthetic_break_frame(post_break_rows, orh=100.0, orl=99.0, break_m=585):
    """A minimal bars frame: ORB window + a break bar + whatever post-break path is supplied."""
    rows = orb_bars(orh, orl) + [(break_m, 99.5, orh + 0.6, 99.4, orh + 0.6)] + post_break_rows
    return mkbars(rows)

def test_touch_kind_full_fill():
    # external FVG sitting 100.8-101.5 (bot=100.8>=ORH=100). Price trades straight through it.
    post = [(586, 100.6, 101.6, 100.5, 101.5)]   # high=101.6 >= top=101.5 -> full fill
    d = _synthetic_break_frame(post)
    b = d[d.m < CW.SESS_END].reset_index(drop=True)
    fvgs = [dict(i=0, m=580, top=101.5, bot=100.8, dir=1)]   # known before the break (pre_orb-ish)
    cls = FD.classify_break(b, fvgs, side=1, ORH=100.0, ORL=99.0, break_m=585)
    check("touch_full_fill", cls["fvg_touch_kind"] == "full_fill" and cls["broken_side_fvg_present"], str(cls))

def test_touch_kind_wick_only():
    # bar wicks into the zone (high=100.9) but closes/opens below bot=100.8 -> body never enters
    post = [(586, 100.5, 100.9, 100.4, 100.6)]
    d = _synthetic_break_frame(post)
    b = d[d.m < CW.SESS_END].reset_index(drop=True)
    fvgs = [dict(i=0, m=580, top=101.5, bot=100.8, dir=1)]
    cls = FD.classify_break(b, fvgs, side=1, ORH=100.0, ORL=99.0, break_m=585)
    check("touch_wick_only", cls["fvg_touch_kind"] == "wick_only", str(cls))

def test_touch_kind_partial_fill():
    # body enters (close=100.9, inside 100.8-101.5) but high=101.1 never reaches top=101.5
    post = [(586, 100.6, 101.1, 100.5, 100.9)]
    d = _synthetic_break_frame(post)
    b = d[d.m < CW.SESS_END].reset_index(drop=True)
    fvgs = [dict(i=0, m=580, top=101.5, bot=100.8, dir=1)]
    cls = FD.classify_break(b, fvgs, side=1, ORH=100.0, ORL=99.0, break_m=585)
    check("touch_partial_fill", cls["fvg_touch_kind"] == "partial_fill", str(cls))

def test_touch_kind_none():
    post = [(586, 100.6, 100.7, 100.5, 100.6)]   # never reaches bot=100.8
    d = _synthetic_break_frame(post)
    b = d[d.m < CW.SESS_END].reset_index(drop=True)
    fvgs = [dict(i=0, m=580, top=101.5, bot=100.8, dir=1)]
    cls = FD.classify_break(b, fvgs, side=1, ORH=100.0, ORL=99.0, break_m=585)
    check("touch_none", cls["fvg_touch_kind"] == "none", str(cls))
    # broken_side_fvg_present should still be True (the FVG exists and is known); only the touch is "none"
    check("touch_none_fvg_still_present", cls["broken_side_fvg_present"] is True, str(cls))

def test_opposite_reach_and_sequence_order():
    # touches FVG at m=586, returns inside ORB at m=587, reaches ORL (opposite) at m=588
    post = [
        (586, 100.6, 101.6, 100.5, 101.4),   # fvg touch (full fill)
        (587, 100.6, 100.7, 99.5, 99.6),     # closes back inside ORB [99,100]
        (588, 99.4, 99.5, 98.8, 98.9),       # trades through ORL=99 -> opposite reached
    ]
    d = _synthetic_break_frame(post)
    b = d[d.m < CW.SESS_END].reset_index(drop=True)
    fvgs = [dict(i=0, m=580, top=101.5, bot=100.8, dir=1)]
    cls = FD.classify_break(b, fvgs, side=1, ORH=100.0, ORL=99.0, break_m=585)
    check("opposite_reached_true", cls["opposite_reached"] is True, str(cls))
    check("sequence_order_correct", cls["sequence"] == "break>fvg_touch>return_inside>opposite_touch", cls["sequence"])

def test_no_external_fvg_present():
    post = [(586, 100.6, 100.7, 100.5, 100.6)]
    d = _synthetic_break_frame(post)
    b = d[d.m < CW.SESS_END].reset_index(drop=True)
    cls = FD.classify_break(b, [], side=1, ORH=100.0, ORL=99.0, break_m=585)
    check("no_fvg_present_flags_false", not cls["broken_side_fvg_present"] and cls["fvg_touch_kind"] == "none", str(cls))

# ------------------------------------------------------------------ contingency helpers on a tiny frame
def test_primary_counts_and_reversal_sequence():
    ann = pd.DataFrame([
        dict(is_trade=True, win=True,  broken_side_fvg_present=True,  fvg_touch_kind="full_fill", opposite_reached=True),
        dict(is_trade=True, win=False, broken_side_fvg_present=True,  fvg_touch_kind="wick_only",  opposite_reached=False),
        dict(is_trade=True, win=False, broken_side_fvg_present=False, fvg_touch_kind="none",       opposite_reached=False),
        dict(is_trade=True, win=True,  broken_side_fvg_present=False, fvg_touch_kind="none",       opposite_reached=True),
        dict(is_trade=False, win=np.nan, broken_side_fvg_present=True, fvg_touch_kind="none",      opposite_reached=False),
    ])
    pc = FD.primary_counts(ann)
    # rows 1,2 are "touched" (present & kind!="none"); rows 3,4 are not (row 5 is a gate-reject,
    # excluded from is_trade==True entirely regardless of its own touch state)
    check("primary_counts_n_with", pc["n_with"] == 2, str(pc))
    check("primary_counts_n_without", pc["n_without"] == 2, str(pc))
    check("primary_counts_winners_with", pc["winners_with"] == 1, str(pc))
    check("primary_counts_winners_without", pc["winners_without"] == 1, str(pc))
    check("primary_counts_losers_with", pc["losers_with"] == 1, str(pc))
    check("primary_counts_losers_without", pc["losers_without"] == 1, str(pc))
    rs = FD.reversal_sequence(ann)
    check("reversal_sequence_counts_sum_to_n", sum([rs["fvg_touch_opp_reached"], rs["fvg_touch_opp_not_reached"],
          rs["no_touch_opp_reached"], rs["no_touch_opp_not_reached"]]) == len(ann), str(rs))

# ------------------------------------------------------------------ visual-pack selection doesn't crash on empty input
def test_select_examples_handles_empty():
    import cw_fvg_figs as FF
    empty = pd.DataFrame(columns=["side", "broken_side_fvg_present", "fvg_touch_kind", "opposite_reached", "date"])
    scen = FF.select_examples(empty)
    check("select_examples_empty_ok", all(len(v) == 0 for v in scen.values()))

def run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests: t()
    print(f"PASS {len(PASS)}  FAIL {len(FAIL)}")
    for f in FAIL: print("  FAIL:", f)
    if FAIL: raise SystemExit(1)
    print("ALL PASS")

if __name__ == "__main__":
    run_all()
