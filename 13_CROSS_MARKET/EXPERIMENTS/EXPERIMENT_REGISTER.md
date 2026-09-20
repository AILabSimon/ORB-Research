# EXPERIMENT REGISTER — cross-market branch

## CM-001 — Phase A behaviour-only census, 33 cells
2026-09-12 · `CODE/phaseA_census.py` · Pre-registered in `SPECIFICATION/`.
5 markets × 6 market/event cells × L∈{5,15,30}, plus the X-1 12:00 control at all three lengths.
No stops, targets or R-multiples. Excursions normalised by W and by lagged 20-session median W.
Sessions excluded for incomplete range windows: 8–21 per cell (counted, never dropped silently).
**Classification: infrastructure — VALIDATED.**

## CM-002 — X-3 touch vs completed-close qualification
**The completed close DESTROYS information in every market.** Touch beats close in 13 of 18 cells;
close is significant in 1 of 18. Reproduces on four new markets what the closed Max project found
in FX. **Classification: BEHAVIOURAL EFFECT CONFIRMED (negative for the close).**

## CM-003 — X-1 opening vs 12:00 non-opening range
Control P(MFE>MAE) 47.8–50.5% (consistently below 50) vs opening 48.1–53.2%. The opening event adds
a small amount of information in most cells, delta +0.04 to +0.22W.
**Classification: PROVISIONALLY SUPPORTED, economically insufficient alone.**

## CM-004 — Phase B family discrimination
**The post-break RETEST is the strongest family in every market**, positive in 16 of 18 cells,
significant in 9, and strengthening monotonically with range length.
**Classification: BEHAVIOURAL EFFECT CONFIRMED, cross-market.**

## CM-005 — Cost/R feasibility gate
2026-09-12 · `CODE/phaseC_costgate.py` · `COSTS/COST_R_FEASIBILITY.csv`.
Each cost component applied exactly once. Instrument economics kept distinct — NQ 1.250 pts RT vs
**MNQ 1.500** (micro commission is larger *in points*); ES 1.100 vs **MES 1.200**; GC 0.450 vs
**MGC 0.500**. CFD costs never presented as futures costs; **XAUUSD spread is ASSUMED (no ASK
series) and is never used as a GC commission**.

**The decisive structural result:** an opposite-edge stop makes R = W, and W is 10–70 instrument
units, so cost/R falls to **0.04–0.18** for the index and gold proxies — versus 0.28R for the
9-point entry-candle stop that destroyed the closed Max project. *The cost problem was a property
of that stop construction, not of opening-range trading.* Gates: index and gold mostly PASS;
**EURUSD L5 and GBPUSD L5/L15 FAIL** (0.37–0.60R) because FX commission is huge relative to a
6–19 pip range. **Classification: VALIDATED.**

## CM-006 — Phase C construction, NAS100 (proxy for NQ/MNQ)
Entry families touch and retest; stops at 1.00×W and 0.50×W; exits 2R, 3R, trail-from-1R; hard
180-minute exit; same-bar conflicts resolved against the trade.

| Arm (L30, retest) | n | /yr | med R | win | gross | **net (NQ sizing)** | 95% CI | maxDD |
|---|---|---|---|---|---|---|---|---|
| opp-edge, trail1R | 2,578 | 206 | 51.4 | 56.9% | +0.086 | +0.047 | [+0.015,+0.078] | 46R |
| **midpoint, trail1R** | 2,578 | 206 | 25.7 | 58.8% | +0.184 | **+0.105** | [+0.060,+0.151] | 62R |
| midpoint, 2R | 2,578 | 206 | 25.7 | 47.9% | +0.163 | +0.083 | [+0.036,+0.132] | 74R |

Touch-family arms are ~zero or negative. **Retest is the only family that constructs.**
**Classification: PROVISIONALLY SUPPORTED — see CM-009 for the limitation that governs it.**

## CM-007 — Phase C cross-market replication: **it does NOT replicate**

| Market | best retest arm | gross | **net** | CI | verdict |
|---|---|---|---|---|---|
| NAS100 (NQ sizing) | L30 midpoint trail1R | +0.184 | **+0.105** | [+0.060,+0.151] | positive |
| US500 (ES sizing) | L30 opp-edge trail1R | +0.048 | **−0.079** | [−0.113,−0.045] | **negative** |
| US500 (ES sizing) | L15 midpoint trail1R | +0.155 | **−0.179** | [−0.224,−0.132] | **negative** |
| XAUUSD COMEX (GC sizing) | L30 midpoint 2R | +0.212 | +0.096 | [−0.014,+0.203] | **CI includes zero** |
| EURUSD (measured spot) | L30 opp-edge trail1R | +0.114 | **−0.101** | [−0.140,−0.062] | **negative** |
| GBPUSD (measured spot) | L30 midpoint trail1R | +0.229 | **−0.350** | [−0.401,−0.300] | **negative** |

**Crucially, gross is POSITIVE in all five markets** (+0.048 to +0.229) — the behavioural effect is
real and cross-market. What differs is entirely cost/R. GBPUSD has the **largest gross effect in
the panel** (+0.229) and the **worst net** (−0.350), because its commission is 2.4 pips against a
19-pip range. **Classification: the behaviour replicates; the economics do not.**

## CM-008 — NAS100 robustness battery
- **Parameter neighbourhood (stop):** 0.35/0.50/0.65/0.80/1.00 × W → +0.148/+0.105/+0.069/+0.056/
  +0.047R. Monotone, all positive, **a stable region rather than a spike**.
- **Range-length neighbourhood:** L = 15/20/30/45 → +0.082/+0.086/+0.105/+0.126R. All positive.
- **Execution delay:** 0/1/2 minutes → +0.105/+0.102/+0.099R. Essentially insensitive.
- **Per-year:** negative in 2 of 13 years only (2014 −0.189, 2015 −0.006); positive in 11, and
  strengthening — 2022–2026: +0.163, +0.274, +0.315, +0.126, +0.288.
- **Drawdown:** 62R peak-to-trough over 2,578 trades. Acceptable.
- **Frequency:** 206 trades/year. Ample.
**Classification: robust *within the cost assumption*.**

## CM-009 — the governing limitation: the candidate is DATA-LIMITED

| Cost basis | net | 95% CI | dev ≤2021 | holdout >2021 |
|---|---|---|---|---|
| NQ futures sizing (**no data held**) | +0.105R | [+0.060,+0.151] | +0.035 | +0.229 |
| MNQ futures sizing (**no data held**) | +0.089R | [+0.045,+0.136] | +0.014 | +0.223 |
| **NAS100 CFD, spread MEASURED** | **−0.001R** | **[−0.046,+0.047]** | −0.110 | +0.193 |

**On the only cost basis this project can actually measure, the candidate is exactly zero.** Its
positive result depends entirely on futures economics for an instrument whose price data we do not
hold. Development is also materially weaker than holdout on every basis.
**Classification: DATA-LIMITED. Does NOT advance to validation.**

## CM-010 — cross-market selection
72 behavioural measurements and ~40 constructed arms were examined. One market is positive under an
assumed cost model, four are not. A single positive under that much search, with development weaker
than holdout, is not evidence of an edge — it is a reason to acquire the data that would settle it.
**Classification: recorded; governs CM-006/CM-008.**
