# RESEARCH STATE — cross-market ORB branch
Updated 2026-09-12 · Phases A–D complete · Authoritative summary: `SENIOR_MANAGEMENT_REPORT.md`

## Objective
Identify which combinations of market, opening event, range length, entry, stop and exit produce a
simple, mechanically replicable, costs-adjusted intraday edge. Not one universal rule — market-
specific candidates are expected and allowed.

## VALIDATED
1. **The post-break retest is the strongest family in every market** — positive in 16 of 18
   behavioural cells, significant in 9, strengthening with range length, and positive in **gross**
   trade terms in all five markets (+0.048R to +0.229R).
2. **A completed close outside the opening range destroys information** — touch beats close in 13
   of 18 cells; close significant in 1. Confirmed on four markets new to the programme.
3. **Cost/R is a property of the stop construction, not of opening-range trading.** Sizing the stop
   off the range rather than the entry candle moves cost/R from ~0.28 to **0.04–0.18** on the index
   and gold proxies. This is the reusable lesson of the branch.
4. **Instrument economics dominate the cross-market outcome.** Gross is positive everywhere; net is
   positive only where the range is wide relative to tick and commission. GBPUSD has the largest
   gross (+0.229R) and the worst net (−0.350R).
5. Data and session infrastructure validated; DST handled tz-aware and verified.

## PROVISIONALLY SUPPORTED
- **CM-C1, Nasdaq opening-range retest.** 30-min range from the 09:30 NY open; completed close
  outside; entry on return to within 0.10×W of the broken edge; stop 0.50×W; trail from +1R; hard
  180-min exit. 206/yr, 58.8% win, maxDD 62R. Net +0.105R [+0.060,+0.151] under NQ sizing.
  **Governed by the DATA-LIMITED finding below — does not advance.**
- The opening event adds information over a 12:00 control (delta +0.04 to +0.22W), modest.

## DATA-LIMITED (the governing constraint)
On the only cost basis measurable here — NAS100 CFD with a measured BID/ASK spread — CM-C1 is
**−0.001R, CI [−0.046,+0.047]**. Its positive result depends entirely on NQ/MNQ futures economics
for an instrument whose price data the programme does not hold. **No source-native futures data
(NQ, MNQ, ES, MES, GC, MGC) exists anywhere in the shared store.**

## SAMPLE-LIMITED
Gold, both anchors: 825 sessions over 3.2 years. Point estimates positive (net +0.006R to +0.096R
under GC sizing); **every confidence interval includes zero**. Best 2R geometry in the panel
(P2R 59–63% at L=5) and the cheapest cost/R. Parked pending GC/MGC data, not rejected.

## COST-DESTROYED
US500 retest (−0.079R to −0.229R under ES/MES sizing) · EURUSD 15–30 min opening range (−0.101R to
−0.211R) · GBPUSD 15–30 min opening range (−0.184R to −0.350R). All have **positive gross**; the
cost is arithmetic, not a modelling gap, so filters are not the remedy.

## NO OPENING-SPECIFIC EFFECT of tradable size
Touch-qualified continuation · close-qualified continuation · failed-break reversal — in every
market and at every range length tested.

## NOT TESTED / PARKED
60-minute range (no delayed-discovery evidence in Phase A to trigger it, per the pre-registered
rule) · six-candle compression as a gate in this branch (its prerequisite — that it replicate under
each market's own range definition — was not reached before the cost gate closed the relevant arms)
· true futures panels for all six contracts.

## SELECTION RISK — recorded, not corrected
72 behavioural measurements and ~40 constructed arms examined. One market positive under an assumed
cost model, four negative. Development (+0.035R) is materially weaker than holdout (+0.229R) on the
lead candidate. Neither fact is fatal; both mean CM-C1 must be decided by new data rather than by
more analysis of the same data.

## Relationship to the existing FX ORB V1 control
Conceptual comparison only; results never pooled. V1 (00:00–08:00 range, 0.10×ATR14 buffer,
opposite-side stop, 16:00 exit, ≈ +0.049R) is **not modified**. This branch's FX arms are negative
and use a different range entirely. The structural contrast supports V1's design: an 8-hour range
with an opposite-side stop produces a risk unit large enough to absorb FX commission; a 15-minute
opening range does not.

## Highest-value next action
**Acquire NQ/MNQ 1-minute futures history, then GC/MGC.** That decides the only live candidate and
the only parked one. No further behavioural work, market, or filter can resolve either.
Do not extend the market panel; do not filter the cost-destroyed arms.
