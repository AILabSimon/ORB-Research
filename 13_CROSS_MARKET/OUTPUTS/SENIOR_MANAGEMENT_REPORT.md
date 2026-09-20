# CROSS-MARKET ORB — SENIOR MANAGEMENT REPORT
### Phases A–D · 2026-09-12 · ORB Programme, cross-market branch

---

## 1. WHICH MARKETS SHOW USEFUL OPENING-SPECIFIC BEHAVIOUR

**All five, in the same family, and the family is not the one the literature or the closed Max
project assumed.**

The **post-break retest of the opening range** carries positive directional information in
**every market tested** — Nasdaq, S&P 500, gold, EURUSD and GBPUSD — at every range length from
15 minutes upward. It is positive in 16 of 18 behavioural cells and statistically significant in 9,
and it *strengthens* monotonically with range length. Constructed as trades it produces a positive
**gross** expectancy in all five markets (+0.048R to +0.229R).

Two supporting cross-market facts:

- **A completed close outside the range destroys information.** A touch qualification beats a
  completed-close qualification in 13 of 18 cells; the close is significant in 1. This reproduces,
  on four new markets and three range lengths, the result the closed Max project found in FX.
- **The opening event does add information over an arbitrary intraday range** — the 12:00 control
  sits consistently below 50% while opening ranges sit above — but the margin is modest and not
  tradable on its own.

**Gold is the most interesting new market behaviourally**: at the COMEX open with a 5-minute range,
59–63% of sessions offer a 2R move — by far the best 2R geometry in the panel. Gold's opening range
is unusually small relative to its subsequent travel.

## 2. WHICH DO NOT

No market shows useful **raw continuation**. Across 72 measurements P(MFE>MAE) spans 42.8%–59.9%;
nothing resembles a large asymmetry on a simple touch or close of the opening range. Immediate
continuation, close-confirmed continuation and failed-break reversal are all weak or inconsistent
everywhere.

**Economically**, four of five markets do not survive their own costs:

| Market | gross (best retest arm) | net | verdict |
|---|---|---|---|
| US500 (ES/MES sizing) | +0.048 to +0.155 | **−0.079 to −0.229** | cost-destroyed |
| EURUSD (measured spot) | +0.114 to +0.218 | **−0.101 to −0.211** | cost-destroyed |
| GBPUSD (measured spot) | +0.105 to +0.229 | **−0.184 to −0.350** | cost-destroyed |
| XAUUSD/gold (GC sizing) | +0.080 to +0.233 | +0.006 to +0.096 | **sample-limited — every CI includes zero** |
| NAS100 (NQ sizing) | +0.086 to +0.184 | **+0.047 to +0.105** | provisionally supported |

The striking case is **GBPUSD: the largest gross effect in the whole panel (+0.229R) and the worst
net (−0.350R)**, because a 2.4-pip round trip sits against a 19-pip range. The behaviour is there;
the economics are not.

## 3. STRONGEST CANDIDATE BY MARKET

**CM-C1 — Nasdaq opening-range retest** (the only candidate that constructs profitably):
30-minute opening range from the 09:30 New York cash open, wick to wick · wait for a completed
30-minute close outside the range · enter on the first return to within 0.10 × W of the broken edge
· stop 0.50 × W · trail from +1R · hard exit at 180 minutes. 206 trades/year, 58.8% win rate,
maximum drawdown 62R over 2,578 trades.

Runners-up: gold at the COMEX open (positive point estimates, inconclusive on 3.2 years);
nothing in S&P 500 or FX at this construction.

## 4. ECONOMIC VALUE AFTER COSTS — **and the finding that governs everything**

| Cost basis | net expectancy | 95% CI | dev ≤2021 | holdout >2021 |
|---|---|---|---|---|
| NQ futures sizing — **no data held** | +0.105R | [+0.060, +0.151] | +0.035 | +0.229 |
| MNQ futures sizing — **no data held** | +0.089R | [+0.045, +0.136] | +0.014 | +0.223 |
| **NAS100 CFD, spread MEASURED** | **−0.001R** | **[−0.046, +0.047]** | −0.110 | +0.193 |

**On the only cost basis we can actually measure, the candidate is exactly zero.** Its positive
result rests entirely on futures economics for an instrument whose price data this programme does
not hold. That is the single most important sentence in this report.

**The structural good news, and it is genuinely new.** The closed Max project died because its
source-faithful stop was 9 points, making a realistic round trip 28% of the risk unit. Sizing the
stop off the **opening range instead of the entry candle** raises R to 10–70 instrument units and
drops cost/R to **0.04–0.18** across the index and gold proxies. **The cost problem was a property
of that stop construction, not of opening-range trading.** That insight is reusable regardless of
what happens to this candidate.

## 5. FREQUENCY
206 trades/year for the Nasdaq candidate; 52–59/year for gold; 200–230/year for the others. Ample
everywhere — frequency is not a constraint in this branch. Median holding period sits well inside
the 180-minute mandate.

## 6. DRAWDOWN
Nasdaq candidate: **62R** peak-to-trough over 2,578 trades (46R on the wider opposite-edge stop,
which is the lower-drawdown variant at lower expectancy). Acceptable at 0.5% risk per trade.
The cost-destroyed markets show drawdowns of 215R–979R and are not survivable at any sizing.

## 7. ROBUSTNESS

**Strong within the cost assumption.** Stop-fraction neighbourhood 0.35→1.00 × W gives +0.148 →
+0.047R, monotone and positive throughout — a stable region, not a spike. Range-length neighbourhood
L = 15/20/30/45 gives +0.082/+0.086/+0.105/+0.126R, all positive. Execution delay of 0/1/2 minutes
changes almost nothing (+0.105/+0.102/+0.099R). Positive in 11 of 13 years and strengthening
(2022–2026: +0.163, +0.274, +0.315, +0.126, +0.288).

**Two reservations.** Development (+0.035R) is materially weaker than holdout (+0.229R) on every
cost basis — the effect looks recent, not stable-through-time. And **cross-market selection**: 72
behavioural measurements and ~40 constructed arms were examined; one market positive under an
assumed cost model, four negative, is not by itself evidence of an edge.

## 8. AUTOMATION FEASIBILITY
High. Every rule is objective and codeable: a fixed clock window, wick-to-wick extremes, a completed
close, a 0.10 × W retest tolerance, a fractional stop, a 1R trail and a hard time exit. No
discretion, no indicators, no higher-timeframe bias. Same-bar conflicts are resolved against the
trade. One Analyst-introduced parameter only — the 0.10 × W retest tolerance — and it is labelled.

## 9. MATERIAL LIMITATIONS

1. **No source-native futures data exists anywhere in the shared store.** NQ, MNQ, ES, MES, GC and
   MGC are all absent. Index and gold results are explicitly proxy results and are never called
   futures results. Futures cost figures are *sizing estimates*, not measurements.
2. **Gold is sample-limited** — 825 sessions over 3.2 years versus ~3,300 over 12–13 years
   elsewhere. No gold conclusion is drawn on a short-sample point estimate.
3. **Gold is cost-limited** — XAUUSD has no ASK series, so its spread is assumed, never measured.
   It is never used as a GC/MGC commission figure.
4. Development weaker than holdout on the lead candidate (§7).
5. Cross-market selection has not been formally corrected for, only recorded.
6. FX results here use a 15/30-minute opening range and must **never** be pooled with the existing
   FX ORB V1 control, which uses a different 8-hour range.

## 10. RECOMMENDED NEXT INVESTMENT OF RESEARCH TIME

**Acquire NQ/MNQ 1-minute futures data. That single acquisition decides the only live candidate in
the programme, and nothing else can.** The candidate is +0.105R under futures sizing and −0.001R on
measured CFD costs; the gap between those two numbers *is* the missing dataset. No further
behavioural work, no additional market, and no further filtering can resolve it.

In priority order:

1. **NQ/MNQ 1-minute history** (decides CM-C1). Then re-run CM-006/CM-008 unchanged on native data.
   If the effect holds on true futures prices and costs, it advances to Phase D validation.
2. **GC/MGC 1-minute history** (decides gold). Gold has the best 2R geometry in the panel and the
   cheapest cost/R, and is currently blocked only by 3.2 years of proxy data.
3. **Do not** extend the market panel further. Five markets, three range lengths and four families
   already answer the behavioural question consistently; adding markets adds selection risk, not
   information.
4. **Do not** add filters to the S&P 500 or FX arms. Their gross effects are positive and their
   costs are simply larger — that is arithmetic, not a modelling gap.

---

## Comparison with the existing FX ORB V1 control (Phase E — conceptual only, never pooled)

V1 uses a 00:00–08:00 range with a 0.10 × ATR14 buffer, an opposite-side stop and a 16:00 exit,
at ≈ **+0.049R**. This branch's FX arms use a 15/30-minute London-open range and are **negative
after measured spot costs** (−0.101R to −0.350R). **Nothing here warrants modifying V1.**

The instructive contrast is structural and supports V1's design: **V1's opposite-side stop on an
8-hour range produces a risk unit large enough to absorb FX commission; a 15-minute opening range
does not.** The same mechanism explains why the Nasdaq candidate works where the S&P 500 one does
not — Nasdaq's range is wide relative to its tick and commission economics, and the S&P 500's is not.

## Decision classifications

| Market / family | Classification |
|---|---|
| Retest family, all markets (behavioural) | **BEHAVIOURAL EFFECT CONFIRMED** |
| Completed close destroys information, all markets | **BEHAVIOURAL EFFECT CONFIRMED** |
| Opening event vs 12:00 control | **PROVISIONALLY SUPPORTED** |
| **NAS100 retest candidate CM-C1** | **PROVISIONALLY SUPPORTED / DATA-LIMITED** — does not advance |
| Gold, both anchors | **SAMPLE-LIMITED** and **DATA-LIMITED** — parked pending GC data |
| US500 retest | **COST-DESTROYED** |
| EURUSD / GBPUSD, 15–30 min opening range | **COST-DESTROYED** |
| Touch, close and failed-reversal families | **NO OPENING-SPECIFIC EFFECT** of tradable size |
| 60-minute range | not tested — Phase A gave no delayed-discovery evidence to trigger it |
