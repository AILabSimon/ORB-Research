# COST ARITHMETIC AUDIT — full reconciliation

Date 2026-09-12 · Script `12_CODE/cost_audit.py` · Supersedes the cost figures in the cycle-2 report.

## 1. The discrepancy explained

Two figures were reported in cycle 2 and they are **the median and the mean of the same per-trade
cost ratio**:

| Statistic | Value (at the then-assumed 1.75 pt round trip) |
|---|---|
| **Median** of per-trade (cost ÷ R_pts) | **0.1880** ← reported as "18.8% of the risk unit" |
| **Mean** of per-trade (cost ÷ R_pts) | **0.2896** ← reported as "breakeven +0.290R" |
| cost ÷ median(R_pts) = 1.75 ÷ 9.309 | 0.1880 |

Expectancy is a **mean**, so the breakeven requirement is the **mean** cost ratio. The two numbers
were both arithmetically correct but were labelled as though they were the same quantity. They are
not, and the median must never be used as a breakeven requirement.

The mean exceeds the median because the per-trade ratio has a long right tail: 13.5% of trades have
R < 3 points, where cost ÷ R explodes. Percentiles of cost ÷ R: p25 0.093 · p50 0.188 · p75 0.385 ·
p90 0.656 · p95 0.831 · **p99 1.309** (cost exceeds the entire risk unit).

## 2. A SECOND error found and corrected

EXP-008 filled entries at the trigger price ± **0.5 pt slippage inside the fill**, so the reported
"gross" already carried 0.5 pt of entry slippage. Charging a further 1.75 pt round trip on top
**double-counted entry slippage**. Both errors are corrected below by recomputing raw gross with
slippage set to zero and then applying every cost component once, explicitly.

## 3. MNQ contract specification

| | |
|---|---|
| Point value | **$2.00** per index point per contract |
| Tick size | **0.25** index points |
| Tick value | **$0.50** |

## 4. Cost component build-up (per round trip, 1 contract)

| Scenario | Commission/side | Commission RT | Entry slip | Exit slip | Stop-specific extra | Stop-exit total | Other-exit total |
|---|---|---|---|---|---|---|---|
| **S1 MNQ optimistic** | $0.35 | $0.70 = 0.350 pt | 0.25 | 0.25 | 0.00 | 0.850 pt ($1.70) | 0.850 pt ($1.70) |
| **S2 MNQ realistic** | $0.50 | $1.00 = 0.500 pt | 0.50 | 0.25 | 0.25 | **1.500 pt ($3.00)** | **1.250 pt ($2.50)** |
| **S3 MNQ poor fill** | $0.75 | $1.50 = 0.750 pt | 1.00 | 0.50 | 0.50 | 2.750 pt ($5.50) | 2.250 pt ($4.50) |
| **S4 Dukascopy CFD** | — | — | 1.46 | 1.46 | 0.50 | 3.420 pt ($6.84) | 2.920 pt ($5.84) |
| **S5 retail / FTMO CFD** | — | — | 3.00 | 2.50 | 0.50 | 6.000 pt ($12.00) | 5.500 pt ($11.00) |

Exit-reason mix: invalidation 55.1% · stop 34.0% · time 10.1% · EOD 0.7%.
Weighted **S2 average round trip = 1.335 pts = $2.67**. (Cycle 2's 1.75 pt was an unjustified
round number; it is replaced by this build-up throughout.)

## 5. Reconciliation — ALL TRADES (n = 3,895; median R = 8.81 pts = **$17.62** risk)

**Raw gross expectancy (zero slippage, zero commission) = +0.1100R**

| Scenario | Avg cost pts | Avg cost $ | **cost/R mean = breakeven** | cost/R median | **Net E** | observed ÷ required |
|---|---|---|---|---|---|---|
| S1 MNQ optimistic | 0.850 | $1.70 | +0.1749R | 0.0965 | **−0.0649R** | 0.63× |
| **S2 MNQ realistic** | 1.335 | $2.67 | **+0.2806R** | 0.1504 | **−0.1707R** | **0.39×** |
| S3 MNQ poor fill | 2.420 | $4.84 | +0.5098R | 0.2708 | −0.3998R | 0.22× |
| S4 Dukascopy CFD | 3.090 | $6.18 | +0.6476R | 0.3489 | −0.5377R | 0.17× |
| S5 retail / FTMO | 5.670 | $11.34 | +1.1784R | 0.6430 | −1.0684R | 0.09× |

**Corrected headline:** observed raw gross +0.1100R against a required +0.2806R at S2 —
a shortfall factor of **2.55×** (cycle 2's "2.6×" was right, but only because two errors
partly cancelled). Every scenario, including the optimistic one, is negative.

## 6. The decisive cut — the apparent edge lives where it cannot be traded

| Population | n | median R | median $ risk | **raw gross** | S1 net (best case) | S2 net |
|---|---|---|---|---|---|---|
| All trades | 3,895 | 8.81 pt | $17.62 | **+0.1100R** | −0.0649R | −0.1707R |
| R ≥ 5 pts | 2,656 | 14.23 pt | $28.46 | **+0.0632R** | −0.0076R | −0.0474R |
| R ≥ 10 pts | 1,801 | 19.68 pt | $39.36 | **+0.0305R** | −0.0149R | −0.0404R |
| R ≥ 20 pts | 879 | 28.56 pt | $57.12 | **−0.0340R** | −0.0631R | −0.0788R |

Raw gross **declines monotonically as the trade becomes more tradable**, and turns negative at
R ≥ 20 points. The effect and its tradability are inversely related. This is a stronger and cleaner
result than cycle 2 reported, and it does not depend on the cost model at all.

## 7. Uncertainty around the +0.1100R raw gross estimate

| Test | Result |
|---|---|
| Sample size | n = 3,895 trades, 13 years |
| Bootstrap 95% CI (4,000 resamples) | **[+0.0097, +0.2194]** — barely excludes zero |
| Development 2013–2021 | +0.1491R, CI [+0.0157, +0.3082] |
| **Holdout 2022–2026** | **+0.0394R, CI [−0.0941, +0.1819] — includes zero** |
| Per-year stability | −0.243R to +0.522R. 2016 (+0.522) and 2017 (+0.507) carry most of the full-sample result; 2015 (−0.243), 2020 (−0.028), 2024 (−0.034) negative |
| NAS100 (NQ/MNQ proxy) | +0.1100R; S2 net −0.1707R |
| US500 (ES/SPX proxy) | +0.1399R, CI [+0.0403, +0.2453], **median R only 2.00 pts** → S2 net **−0.9291R** |
| Same-bar ambiguity sensitivity | Optimistic resolution: +0.0710R, CI **[−0.0230, +0.1771] — includes zero** |
| Slippage sensitivity (inside the fill) | 0.00 pt → +0.1100R · 0.25 pt → +0.0762R (CI includes zero) · 0.50 pt → +0.0189R · **1.00 pt → −0.0595R** |

**One tick (0.25 pt) of entry slippage removes statistical significance.** RR-002 documents Max
complaining about exactly this on a manual market entry ("It filled me really bad… I tried to fill
at 59"). The +0.1100R figure requires simultaneously: zero slippage, conservative same-bar
sequencing, and inclusion of trades too small to execute. Relax any one and it is indistinguishable
from zero.

## 8. Conclusion of the audit

The economic gap is **real and is not a reporting inconsistency**. Two labelling/accounting errors
were found and are corrected here and propagated to every report. The corrected figures are
**less** unfavourable than cycle 2 stated (net −0.171R rather than −0.271R at realistic cost) and
the conclusion is unchanged, because the gap is structural: at a median $17.62 of risk per
contract, a $2.67 round trip is unrecoverable from an edge that is itself not robustly positive.
