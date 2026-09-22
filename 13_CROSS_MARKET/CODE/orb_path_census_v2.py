#!/usr/bin/env python3
"""
UNTESTED THIS CYCLE — no Python execution was available in the sandbox that wrote this
file (issue #3, 22 Sep 2026b continuation cycle). Validate against a small labelled
sample (5-10 days, visually checked) before trusting any count derived from this file.
See 13_CROSS_MARKET/OUTPUTS/CORE_STRATEGY_RECONSTRUCTION.md §13 for the source
reasoning and citations behind both functions.

Extends orb_path_census.census() with two event-based mechanisations:
  event_consolidation()  -- hover/consolidation with a MEASURED, not chosen, length
                            (V1 20:34 "failed to make a newer high, failed to make a
                            newer low"; V2/V5 "three bar" / trend-range-trend)
  one_two_punch()         -- Max's double-retest continuation confirmation (V8 11:18,
                            corroborated by V8 14:52 and V12 27:23)

Both take the same per-day arrays orb_path_census.census() already computes
(H, L, C, M, bi, side, bnd, back) and return None when the source primitives don't
resolve within the session, rather than a fabricated boolean.
"""
import numpy as np


def event_consolidation(H, L, C, M, bi, side, back):
    """
    Event-based hover state, starting at the first bar after the retrace that fails to
    extend the post-break extreme, ending at the first bar that resolves it either way.
    Returns a dict, or None if there was no retrace (back is empty) to start from.
    """
    if not len(back):
        return None
    r0 = bi + 1 + back[0]
    ext = H[:r0 + 1].max() if side == 1 else L[:r0 + 1].min()
    n = len(M)
    i = r0 + 1
    hover_len = 0
    while i < n:
        newer_with = (H[i] > ext) if side == 1 else (L[i] < ext)
        # opposite-side reference tracked only from r0 forward -- this is the
        # invalidation boundary for the hover state, not the pre-break range.
        opp_ref = L[r0:i].min() if side == 1 else H[r0:i].max()
        newer_against = (L[i] < opp_ref) if side == 1 else (H[i] > opp_ref)
        if newer_with:
            return dict(start_m=int(M[r0]), end_m=int(M[i]), hover_bars=hover_len,
                        resolution="continuation")
        if newer_against:
            return dict(start_m=int(M[r0]), end_m=int(M[i]), hover_bars=hover_len,
                        resolution="failure")
        hover_len += 1
        i += 1
    return dict(start_m=int(M[r0]), end_m=None, hover_bars=hover_len,
                resolution="unresolved_by_session_end")


def one_two_punch(H, L, C, M, bi, side, bnd, back):
    """
    Double-retest continuation confirmation (V8 11:18). Requires the level to be
    retested and fail to reclaim TWICE before confirming on a newer extreme.
    "Fail to reclaim" = price touches the boundary again but does not CLOSE back inside
    the ORB (the source's own invalidation event, RESEARCH_CURRENT.md §D.6 / V8 06:11,
    is what "reclaiming" means here -- so absence of that event is the retest's
    failure).
    Returns None if there was no retrace to start from; otherwise a dict describing
    either the confirmation, a disqualifying inside close (Entry 04 / V8 06:11
    territory, not one-two-punch), or an unresolved session.
    """
    if not len(back):
        return None
    n = len(M)
    touches = []
    i = bi + 1
    in_touch = False
    while i < n:
        touching = L[i] <= bnd <= H[i]
        closed_inside = (C[i] < bnd) if side == 1 else (C[i] > bnd)
        if closed_inside:
            return dict(disqualified_at_m=int(M[i]), reason="closed_back_inside")
        if touching and not in_touch:
            touches.append(i)
            in_touch = True
        elif not touching:
            in_touch = False
        if len(touches) >= 2:
            ext_before_second = (H[touches[0]:touches[1]].max() if side == 1
                                  else L[touches[0]:touches[1]].min())
            newer = (H[i] > ext_before_second) if side == 1 else (L[i] < ext_before_second)
            if newer:
                return dict(retest1_m=int(M[touches[0]]), retest2_m=int(M[touches[1]]),
                            confirm_m=int(M[i]), n_retests=len(touches))
        i += 1
    return dict(n_retests=len(touches), reason="unresolved_by_session_end")
