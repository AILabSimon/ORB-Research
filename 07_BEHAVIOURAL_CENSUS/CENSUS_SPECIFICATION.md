# CENSUS-01 SPECIFICATION — pre-registered

Written 2026-09-12 by the Analyst Agent **before any measurement was run**.
Inputs: Research Agent cycle-1 handoff (`Max Options Trading ORB/04_HANDOFF_TO_ANALYST/`).
Executes the Research Agent's recommended first action (handoff §10) and satisfies the
Analyst mandate §12–§14.

This is a **behaviour-only census**. No stop, no target, no R-multiple exit, no trade, no
equity curve. Nothing here is a strategy test.

---

## 1. Event

Source-supported, from R-001 / R-002 / R-003 / R-006, all classified "explicit and repeated":

- **Opening range** = the first 15-minute candle of the US cash session, 09:30:00–09:44:59
  US Eastern. `ORB_high` = highest high, `ORB_low` = lowest low, **wick to wick** (R-003).
  `ORB_mid` = (high+low)/2. `ORB_width` = high − low.
- **Signal** = the **first** subsequent 15-minute candle whose **CLOSE** is strictly outside
  the range (R-006). Up-signal if close > ORB_high; down-signal if close < ORB_low.
- **Signal direction** = the side of the break. **No buffer** — the source specifies none, and
  importing one would be an unlabelled Analyst construct.
- 15-minute candles are aligned to the cash open: 09:45–10:00, 10:00–10:15, … 15:45–16:00.
- A session with no qualifying close by 16:00 is recorded as **NO-SIGNAL** and retained in the
  denominator. No session is silently dropped.

## 2. Population

| | Track A (primary) | Track B (secondary, later cycle) |
|---|---|---|
| Instrument | NAS100 1m BID (Dukascopy) | EURUSD, GBPUSD |
| Represents | **proxy** for NQ/MNQ — `INDEX_CFD_OTC`, NOT futures, NOT options | — |
| Period | 2013-08 → 2026-08 | — |
| Secondary | US500 1m BID (**proxy** for ES/MES/SPX) | — |

Track B is **not** run in CENSUS-01. Max teaches the US cash open; an FX translation is a
separate question and results may never be pooled with Track A.

**Session inclusion:** all 15 one-minute bars of the 09:30–09:45 window present. Days failing
this are excluded and **counted**. Weekdays only. Early-close days are not excluded but the
16:00 horizon will simply be short; they are flagged by session bar count.

## 3. Analyst decisions, pre-registered

Each is an Analyst construct, not a Max rule, and is recorded as such.

| # | Decision | Choice | Reason |
|---|---|---|---|
| AD-01 | Timezone | `America/New_York`, DST-aware | U-06: no source evidence. Max works in Eastern wall-clock. |
| AD-02 | Entry price reference | close of the qualifying 15-minute bar | R-007 states it. The alternative (next-bar open) is deferred to construction, not census. |
| AD-03 | Path measurement start | the **first 1-minute bar after** the signal bar closes | Removes the signal bar's mechanically predetermined excursion. Mandate §12. |
| AD-04 | R for the continuation branch | `R = \|entry − breached ORB edge\|` | R-012: the stop is "back inside the range". This is the only source-anchored risk unit. |
| AD-05 | Return-inside measured **both** ways | 1-minute **touch** back inside, and 15-minute **close** back inside, reported separately | U-03 is unresolved; the census settles it empirically instead of guessing. |
| AD-06 | Reversal-branch R | **not assigned in CENSUS-01** | U-05: the stop is never stated. Inventing it now would contaminate a behavioural measurement. Reversal excursion is reported in points and in continuation-R units only. |
| AD-07 | Signal is first-only | one signal per session | Avoids double-counting the same day's information. Re-entry is a construction question. |

**Not decided, deliberately:** stop touch-vs-close as an executed rule, scale-out fractions,
09:55-vs-16:00 holding (C-03), one-and-done vs re-entry (C-04). None is needed to measure
behaviour, and all four are recorded as open.

## 4. Measurements

### 4.1 Range block (per session)
date · ORB_high · ORB_low · ORB_mid · ORB_width_pts · ORB_width_rel (= width ÷ trailing
20-session median width, **lagged**, no look-ahead) · ORB candle open/close/direction ·
body-to-range ratio · overnight gap (09:30 open − prior 16:00 close).

### 4.2 Break block (per session)
first 1m touch above / below ORB and their times · first 15m **close** outside and its time ·
signal direction · signal bar ordinal (1 = 09:45–10:00) · minutes from range completion to
signal · signal bar body/range ratio and close position within its own bar · whether the
**other** edge was ever touched before the signal · whether both edges are ever breached in
the session.

### 4.3 Path block (from AD-03 start, per horizon)
Horizons: **5, 15, 30, 60, 90, 120, 180 minutes, and to 16:00.**
- MFE and MAE **in the signal direction**, in points and in R (AD-04).
- MFE **in the opposite direction** — this is control CTRL-B (§5).
- Net displacement.
- Time to first touch of: 1R, 2R, 3R (continuation); ORB edge re-entry (touch); ORB_mid;
  opposite ORB edge.
- Flags: returned inside (touch) · returned inside (15m close) · reached opposite edge ·
  reached ≥2R before returning inside · returned inside before reaching 1R.

### 4.4 Sequencing rule (critical, mandate §28)
Within any 1-minute bar where both an adverse and a favourable threshold could be struck, the
census records **both touches with the same timestamp and makes no ordering assumption**. A
`same_bar_ambiguous` flag is set. No result may be reported that silently resolves it — this
is exactly the field the Research Agent flagged as "NOT ADDRESSED ANYWHERE" in MC-1.

## 5. Controls — two only, each addressing a real identification problem

| ID | Control | Identification problem it addresses |
|---|---|---|
| CTRL-A | **Pseudo-ORB**: identical machinery, range built from the 11:00–11:15 ET candle, signals from 11:15 | Is the **opening** range special, or would any 15-minute range produce the same post-break behaviour? |
| CTRL-B | **Opposite-direction excursion** from the same event, same R scaling | Does the break carry **directional** information, or is post-break movement symmetric noise? |

No further controls. Time-matched random levels and width-matched non-opening ranges are
**not** built: CTRL-A already tests the "any range would do" hypothesis and CTRL-B already
tests directionality. Additional controls would be decorative (mandate §13).

## 6. Segmentation

Applied to the primary result, not searched over:
`ORB_width_rel` quintiles (**CL-012 / filter F-d — Max's own stated conditioner, the highest-value
hypothesis in the pack**) · signal bar ordinal (early vs delayed) · signal direction ·
one-sided vs two-sided breach day · year · `ORB_width_pts` absolute.

## 7. Decision questions

1. **Q1 (U-01, the central question).** Conditional on a qualifying close outside the ORB, is
   continuation economically distinguishable from reversal? If continuation MFE and
   opposite-direction MFE are near-symmetric, no entry refinement can rescue MC-1 and that is
   established before anything is built.
2. **Q2 (mandate hard requirement).** Is **≥2R reachable at all** from ORB-edge risk, and at
   what frequency, within 180 minutes?
3. **Q3 (C-03, the 180-minute constraint).** How much of the total available excursion is
   captured by 180 minutes versus holding to 16:00? This decides whether Max's method is even
   compatible with this project's mandate.
4. **Q4 (U-03).** Touch-back-inside vs 15m-close-back-inside — how different are the survival
   rates? This will dominate MC-1's measured expectancy.
5. **Q5 (CL-012 / F-d).** Does opening-range width relative to lagged volatility change any of
   the above materially?
6. **Q6 (CTRL-A).** Is the 09:30 range special?
7. **Q7 (MC-2).** Conditional on a return inside, what is the excursion distribution toward
   ORB_mid and the opposite edge — i.e. is the failed-breakout reversal a real behaviour?

## 8. Artefact protections

DST-aware tz (never fixed offsets) · lagged-only volatility normalisation · path starts strictly
after the signal bar · no future pivots · complete denominator including NO-SIGNAL days ·
duplicate timestamps already verified zero · incomplete-ORB days excluded and counted ·
missing interior minutes counted per session · same-bar ambiguity flagged, never resolved ·
NAS100's 338 OHLC-violating bars excluded and counted · dataset SHA256 frozen at run time ·
deterministic, no randomness anywhere in CENSUS-01.

## 9. What CENSUS-01 explicitly does NOT do

No trade construction · no costs applied (costs belong to construction; the cost floor is
already measured in `09_VALIDATION/COSTS/COST_BASELINE.md`) · no filter search · no parameter
optimisation · no F2/F3/F5/F6/F7/F8/F9 · no pooling of F1 and F4 · no use of any figure from
`CLAIMS_REGISTER.csv`.
