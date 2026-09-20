# ANALYST_CURRENT
**20 Sep 2026 · Analyst Agent · built against RESEARCH_CURRENT v2.2 (blob `27826b1`, verified byte-identical to the GitHub copy)**

---
# CEEWILLI V2.2 — CURRENT

## Specification built (v2.2 §D / §E.2 / §F, Entry 02 only)
PRE-MARK DRAW → ORB 09:30–09:44:59 wick-to-wick → **BREAK** (body close beyond the edge; body/range
and volume/median-20 recorded, never filtered) → **PULLBACK** to the broken level (**no candle
count**) → **REJECTION** (bar with `low ≤ ORH ≤ high` **and** a close beyond the edge; a wick alone
is not enough) → **STOP** = beyond the retest cluster, `min(low)[break…rejection] − 1 tick` →
**RR_GATE** `dist(entry,draw)/dist(entry,stop) ≥ 2.0` else **NO TRADE** → **ENTRY** at the rejection
close, filled at the next bar's open → target = the qualifying draw; exit on stop, on the first close
back inside the ORB (his own rule), at 16:00 → 11:30 entry cut-off → **two-loss day stop**.
Entries 01/03/04 and Max's continuation model are not in this population. 8 cells; nothing selected.

## Representation gate — H19–H27 all PASS
H19 RR gate enforced, min rr = 2.000, **no-target bucket = 0** · H20 draws pre-marked and causal
(12 permitted types, prior sessions only) · H21 **no candle count** — the only `>=2` in the engine is
the two-loss stop; 83% of entries have a single-bar pullback and are kept · H22 HOLD and DEEP both
built, populations differ · H23 1m and 5m built end to end (stop and gate included) · H24 break
diagnostics on 100% of breaks, no threshold anywhere · H25 invalidation is CeeWilli's own · H26 BE
and no-BE arms · H27 zero trades after two losses. Retained: H1 ORB, H3 break ≠ entry (min gap
2 min), H4 real interaction, H6 wick-only ≠ rejection, H9 no lookahead, H13 day stop, honest fills
(next-bar open). **H14 VRC-01 FAILS under the literal §E.2 reading — see defect 1.**

## Visual validation — PASS for geometry, and it exposed the gate defect
Sampled 1m/5m × HOLD/DEEP, each a win, a loss and a gate reject. Break → rejection → fill are
properly separated and the trades read as Entry 02. **Stop realism is good:** median stop 0.087% of
price (NAS100 1m) against CeeWilli's on-screen 0.076%. Two reject panels show the defect plainly —
NAS100 2024-11-18 (R=58.0, preRR **0.0**) and 2022-08-24 (R=48.4, preRR **0.0**) were refused
because a 5-minute FVG sat on top of the entry, and price then ran hard in the trade's direction.

## Economics — 8 cells, gross first, full unselected population
Full table (candidates, gate passes/rejects, MFE/MAE, 1R/2R/3R, exit mix, year-by-year,
available_RR and draw-type distributions) is in `13_CROSS_MARKET/OUTPUTS/CW_ENTRY02_ECONOMICS.md`.
US500 headline:

| cell | cand | pass | rej (no draw / rr<2) | /yr | GROSS | 95% CI | win% | 2R | stop | inval | target | BE | NET |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1m HOLD BE0 | 2587 | 361 | 694 / 1532 | 34 | −0.0913 | [−0.289, +0.117] | 13.3 | 28% | 34% | 52% | 13% | — | −1.008 |
| 1m HOLD BE1 | 2587 | 361 | 694 / 1532 | 34 | −0.0453 | [−0.214, +0.153] | 9.7 | 23% | 25% | 36% | 9% | 29% | −0.962 |
| 1m DEEP BE0 | 2948 | 311 | 801 / 1836 | 29 | −0.1211 | [−0.291, +0.079] | 12.2 | 26% | 24% | 64% | 11% | — | −0.864 |
| 1m DEEP BE1 | 2948 | 311 | 801 / 1836 | 29 | −0.0315 | [−0.193, +0.149] | 10.0 | 23% | 17% | 47% | 9% | 27% | −0.775 |
| 5m HOLD BE0 | 1777 | 124 | 505 / 1148 | 12 | −0.3076 | [−0.513, −0.076] | 9.7 | 21% | 43% | 47% | 10% | — | −0.879 |
| 5m HOLD BE1 | 1777 | 124 | 505 / 1148 | 12 | −0.2808 | [−0.449, −0.097] | 5.6 | 15% | 35% | 28% | 6% | 31% | −0.852 |
| 5m DEEP BE0 | 2221 | 130 | 632 / 1459 | 12 | −0.2152 | [−0.414, +0.005] | 13.8 | 25% | 35% | 52% | 12% | — | −0.719 |
| 5m DEEP BE1 | 2221 | 130 | 632 / 1459 | 12 | −0.1918 | [−0.362, −0.004] | 9.2 | 20% | 29% | 32% | 8% | 30% | −0.696 |

NAS100 runs slightly positive gross on the same cells (1m DEEP +0.048, 1m HOLD +0.018); **the two
instruments do not agree in sign.** Mean winner +2.6 to +4.0R, mean loser −0.6 to −0.8R.
**DIAGNOSTIC, not selected:** the §D.11 hierarchy reading yields 146–150 trades/yr at gross −0.009
to +0.019, all intervals spanning zero.

## Material defects
1. **§E.2 "nearest" contradicts §D.11 "hierarchy" — blocks H14.** `available_RR` is below 0.5 on
   **61%** of gate evaluations and below 0.10 on **~33%** of the rr-rejects: with ~120 pre-marked
   levels the nearest one is usually adjacent to the entry. On 28 May 2026 that gives rr ≈ 0 and no
   trade; under the hierarchy the same day gives preRR 2.59 against CeeWilli's on-screen 2.26.
   Both built, both reported, **neither selected. Research must rule.**
2. **Fixed, mine:** a 15-minute swing **low** was admitted as an upside draw for a long (and a
   bearish FVG likewise). Draws are now direction-typed. Counts roughly doubled; conclusions unchanged.
3. **VRC-01's six inside closes are absent from every series we hold.** Native ES 1m begins
   2026-08-19, so the acceptance case can only be run on the US500 proxy, whose microstructure that
   day differs. H14 is therefore not fully demonstrable on available data.
4. **Cost, not signal, is what kills every cell.** cost/R median 0.30 (NAS100 1m), 0.53 (US500 1m).
   Every arm's gross is smaller than its own cost.

## What was learned
The setup is now represented credibly and the numbers are honest: stop distances match the source,
the gate is enforced with an empty no-target bucket, and 2R is naturally reached on 20–28% of trades.
Gross sits at or just below zero on every cell, on both instruments, in both U-22 readings and on
both timeframes — and the intervals span zero except where they are significantly **negative**.
BE-at-1R improves gross in all eight cells and leaves every one of them negative. The dominant exit
is **invalidation** (28–64%), i.e. his own close-back-inside rule cutting trades early.

## Is Entry 02 now represented credibly?
**Yes, with one caveat.** The state machine, stop construction, gate and management follow v2.2
exactly, and the visual sample reads as Entry 02. The caveat is defect 1: the draw-selection rule is
genuinely ambiguous in the source, and it changes trade count roughly five-fold (311 → 1,607 on
US500 1m). Until that is ruled on, the *population* is provisional even though the *mechanism* is right.

## Highest-value next action
**The §E.2 / §D.11 draw ruling.** It is the only open representation question, it is the blocker on
H14, and it moves the trade population by a factor of five. Everything else is measured.

---
# MAX V2.1 — PENDING SEPARATE CYCLE
Not run this cycle, per mandate. Existing results stand unchanged: RETEST S1 n=1,355, gross +0.1871
[+0.015, +0.361], net −0.238 — **with the caveat already on the record that the top 1% of trades is
100% of total R and removing the best 10 trades takes gross to +0.0330R.**

---
# V2.0 — SUPERSEDED REPRESENTATION
Diagnostic history only, not strategy evidence: +0.0528R pooled gross; the CFD net result; the 31.8%
no-target population; the rejection-arm result; the unfloored MAX stop-A failure.
