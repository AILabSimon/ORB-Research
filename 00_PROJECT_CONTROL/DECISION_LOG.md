# DECISION LOG

Material decisions only.

## 2026-09-12 — D-001: Do not begin strategy testing; census blocked
The project directory was empty; `INITIAL_ANALYST_HANDOFF.md` does not exist. No Max rule has
been assumed. Conventional ORB defaults (09:30–09:45 New York, touch-based break) were
deliberately NOT substituted, because a wrong event definition produces a representation
failure indistinguishable from absence of edge. RR-001 raised as BLOCKING.

## 2026-09-12 — D-002: Reuse shared Dukascopy store read-only; no acquisition
Required 1m BID+ASK series for both tracks already exist and pass validation. No download
performed; nothing duplicated into the project. Derived data only will be written to
`06_DATA/DERIVED`.

## 2026-09-12 — D-003: NAS100/US500 designated explicit proxies, not source-native
Both are `INDEX_CFD_OTC`. They will be used for Track A as an explicitly identified proxy
and separately assessed. They will not be labelled NQ, MNQ, ES, MES or SPX at any point.
Any options implementation is recorded as unvalidated for the life of the project unless
contract data is obtained.

## 2026-09-12 — D-004: MC-1 on the taught 15-minute-close entry — DO NOT CONSTRUCT
P(MFE>MAE) is 50.3–51.9% at every horizon, in both directions, in every year, on two instruments.
Gross expectancy is flat across 1R/2R/3R targets, which is the martingale signature and excludes
a bad-exit explanation. Median stop distance is 7.99 points and 29.4% of signals have a stop
smaller than a round-trip cost. Classified FALSIFIED for this representation. Reported as a
failure of **the tested representation**, not of "Max's ORB" — eight other families remain.

## 2026-09-12 — D-005: CL-012 / filter F-d FALSIFIED
"ORB works best on large move mornings" was the highest-value filter hypothesis in the evidence
pack. Measured against lagged volatility it points the wrong way: the widest quintile is the
worst on both P(MFE>MAE) and net expectancy, with no monotone structure.

## 2026-09-12 — D-006: MC-2 / F4a RETIRED against this mandate
Not on statistics but on geometry. From the return-inside close the source-supported targets
(midline 0.32R, opposite edge 0.87R median) sit nearer than the source-implied stop, and only
12.0% of events have a ≥2R opposite edge. The mandate requires ≥2R potential. This cannot be
fixed by a better entry or a better sample.

## 2026-09-12 — D-007: R≥15pt screen NOT advanced
It survives the control test but fails monotonicity, the holdout CI and per-year stability. It is
also an unsupported Analyst construct that contradicts the source's preference for tight entries.
Recorded as provisional so it cannot quietly re-enter under another name.

## 2026-09-12 — D-008: C-03 resolved by data, not by source
180 minutes captures 76% of end-of-day MFE and median time to 2R is 38 minutes. The project's
180-minute cap is not the binding constraint. No research request needed for C-03.

---
## 2026-09-12 — D-005R: CORRECTION to D-005. Researcher Challenge RC-001 ACCEPTED
Cycle 1 recorded CL-012 as FALSIFIED. That was wrong. EXP-004 sorted on **opening-range width**,
and Max's "larger than expected move" attaches to **compression** — a *narrow* early range — not
to width. EXP-004 falsifies width-as-a-filter, an Analyst hypothesis. The cycle-1 verdict
over-claimed and is corrected. CL-012 has now been properly tested by EXP-008-G4 and EXP-009, and
its tradable branch does not hold — but that is a different, later finding, established on the
right variable.

## 2026-09-12 — D-009: pre-registered EXP-008 was contradicted by RR-002 and was NEVER RUN
The cycle-1 plan was a resting **stop order** at the ORB boundary with a fixed ~20-point stop from
R-031. RR-002 established that (a) a pre-placed resting stop order beyond the ORB is **NOT FOUND**
in twelve videos, and (b) R-031's 80 ticks is a **trail**, not an initial stop. Two of three
components were wrong. No results were discarded because none existed. EXP-008 was rebuilt to the
corrected MC-7 specification before being run. Recorded so the plan/execution distinction is not
lost.

## 2026-09-12 — D-010: MC-7 / F2 FALSIFIED against a VERIFIED-FAITHFUL representation
For the first time in this project a reconstruction was validated against the source's own stated
numbers: Max states live stops of 6–17 NQ points with a mode near 9–10; the representation produces
a median of 9.3. Gross expectancy is +0.019R (+0.110R at zero slippage, the impossible bound).
Net is −0.271R at realistic MNQ cost and negative in every arm and under every source-supported
gate. This can no longer be attributed to representation failure.

## 2026-09-12 — D-011: the binding constraint is structural, not statistical
Max's own stop distance of 6–17 points means a realistic MNQ round trip consumes 10.7%–32.2% of
the risk unit. Breakeven requires a gross edge of +0.290R; the best-case measured edge is +0.110R.
At the measured edge the stop would have to exceed 16–88 points to pay for itself. No source
detail, filter, sample or instrument changes this arithmetic. **No further research request is
warranted on this ground** (mandate §25: the answer cannot change the decision).

## 2026-09-12 — D-012: F5 RETIRED; C-11 resolved empirically
EXP-009 found that compression predicts **containment**, not expansion — which pointed at the fade
(R-021) rather than the confirmed break (V12 28:55). The fade was then tested rather than asserted,
and failed on all four arms, gross as well as net. Contradiction C-11 therefore no longer needs
resolving from source: neither branch is tradable.

## 2026-09-12 — D-013: Track A (Max ORB, US cash open) recommended CLOSED
Six representations have now been tested against source-supported specifications: 15m-close
continuation, failed-breakout reversal, print-through boundary entry, the OCO bracket, the
compression-gated break, and the compression-gated fade — plus the 5-minute ORB and two
source-supported gates. Every one is negative after cost. Per mandate §24 the existing FX ORB V1
control (+0.049R) is **not** replaced and nothing from this branch improves it.

---
## 2026-09-12 — D-014: cost arithmetic CORRECTED (two errors), conclusion unchanged
"18.8%" and "+0.290R" were the median and the mean of the same per-trade cost ratio; only the mean
is a breakeven requirement. Separately, EXP-008 carried 0.5 pt of entry slippage inside the fill,
so adding a 1.75 pt round trip double-counted it. Corrected from an explicit MNQ dollar build-up:
S2 realistic = 1.335 pts = $2.67 round trip against a median $17.62 of risk; breakeven +0.2806R;
raw gross +0.1100R; net −0.1707R; shortfall 2.55×. Corrected figures are **less** unfavourable
than cycle 2 reported. Propagated to all reports; superseded figures marked, not explained around.

## 2026-09-12 — D-015: the edge is inversely related to tradability
Raw gross falls monotonically with the size of the risk unit: +0.110R all trades, +0.063R at
R≥5 pts, +0.031R at R≥10 pts, −0.034R at R≥20 pts. This is independent of any cost assumption and
is a stronger result than the cost comparison. Combined with the uncertainty battery — holdout CI
includes zero, optimistic same-bar resolution CI includes zero, and a single tick of entry slippage
removes significance — the +0.1100R figure is not a robust edge.

## 2026-09-12 — D-016: Track A wording CORRECTED for scope
Earlier reports said "Max ORB falsified". That over-states what was tested. Corrected scope: the
**reconstructed** Max ORB families, tested on **Dukascopy OTC index-CFD proxies**, did not produce
a viable costs-adjusted strategy. Source-native NQ/MNQ/ES/SPX and all options implementations
remain **UNVALIDATED because suitable data was unavailable** — not falsified. Proxy agreement
across two instruments and source-matched stop geometry raise confidence; they do not remove the
instrument limitation.

## 2026-09-12 — D-017: compression finding RECLASSIFIED
From "reusable input for the existing FX ORB control" to
**PROVISIONALLY VALIDATED ON US INDEX-CFD PROXIES**, with FX replication recorded separately.
It is a day-state hypothesis — *prolonged opening-range containment may identify suppressed
subsequent range expansion* — not a strategy and not an input to another project until it
replicates under that project's own instrument, session and range definition.

## 2026-09-12 — D-018: Track B CLOSED
Six pre-registered series (2 pairs × 3 anchors), ~5,600 print-through events each. Directional
information absent or slightly negative (P(MFE>MAE) 43.9%–51.5%); the print-through **destroys**
information relative to the completed close, the reverse of its role in the source. The ≥2R
geometry that Track A lacked **is** present in FX (opposite edge a median 4.1–4.8R away, P(MFE≥2R)
65–70%), so Track B fails for a different and more decisive reason: the source-faithful stop is
1.9–3.6 pips, making a realistic round trip **72%–124% of the entire risk unit**. Net −0.64R to
−1.05R, CIs nowhere near zero. Closed under stopping rules (a), (c) and partially (b).

## 2026-09-12 — D-019: PROJECT CLOSED. No candidate advances.
Both tracks complete. Nine strategy families dispositioned. The existing FX ORB V1 control
(+0.049R) is NOT replaced and nothing in this project improves on it. One reusable hypothesis is
carried forward (D-017). No further Research Agent work required.

---
## 2026-09-13 — D-020: DATA ACQUISITION BLOCKED — two independent blockers, both verified

SVP authorised acquisition of NQ/MNQ (and GC/MGC) data via Dukascopy using a Python route.
Acquisition was attempted and **could not be completed**. Two separate blockers, verified rather
than assumed:

**Blocker 1 — Dukascopy does not sell futures data at all.** The full instrument catalogue in
`dukascopy-python` 4.0.1 was enumerated: **1,380 instruments, zero futures contracts.** The
apparent matches are false positives:

| Looks like | Actually is |
|---|---|
| `INSTRUMENT_IDX_AMERICA_E_NQ_100` → `E_NQ-100` | NASDAQ-100 **index CFD** — the series we already hold |
| `INSTRUMENT_US_CME_US_USD` → `CME.US/USD` | CME Group Inc **equity share** |
| `INSTRUMENT_US_ES_US_USD` → `ES.US/USD` | Eversource Energy **stock** |
| `INSTRUMENT_IDX_EUROPE_E_FUTSEE_100` | FTSE 100 index CFD |
| gold | only `INSTRUMENT_FX_METALS_XAU_USD` → `XAU/USD` **spot**. No GC, no MGC. |

Therefore **the authorisation as written cannot deliver the recommendation.** Re-running the
candidate on Dukascopy index-CFD data would reproduce the −0.001R result already in the record,
because that *is* the instrument it was measured on.

**Blocker 2 — `freeserv.dukascopy.com` is not on the network allowlist.** Both available shells
(the cloud container and the desktop Linux VM) return HTTP 403 at the proxy CONNECT stage. The
agent-proxy status endpoint reports `connect_rejected — gateway answered 403 to CONNECT (policy
denial)`. This is a policy denial, not a transient failure, so per project rules the endpoint was
not retried repeatedly and the raw `datafeed.dukascopy.com/*.bi5` route was not rebuilt.

**Decision.** No data acquired. `13_CROSS_MARKET` candidate CM-C1 remains **DATA-LIMITED** and its
classification is unchanged. Two deliverables produced instead:
1. `acquire_tick_data.py` — a complete, resumable tick-acquisition script, ready to run the moment
   either blocker is lifted. It downloads bid/ask ticks for NAS100 and XAUUSD restricted to the
   session windows the candidate trades, with provenance in the existing store's schema.
2. A corrected vendor recommendation for the SVP (see `13_CROSS_MARKET/OUTPUTS/DATA_ACQUISITION_STATUS.md`).

**What tick data would still be worth acquiring from Dukascopy**, even though it is not futures:
it removes two of the three remaining modelling assumptions on the instrument we do hold —
spread at the moment of entry (currently approximated from 1-minute closes) and same-bar
stop/target sequencing (currently resolved by a conservative rule, affecting 11.3% of trades).
That would harden the −0.001R figure but **would not change which instrument it describes**.

---
## 2026-09-17 — D-021: migrated to the canonical Market Data store; own downloader retired
Per the Market Data Engineer's guide (17 Sep). `acquire_tick_data.py` moved to
`05_ARCHIVE/retired_scripts/`. Future data needs go through the DATA REQUEST process, not our own
acquisition code.

**Migration verified, not assumed.** `USATECHIDXUSD` (canonical NAS100) and the legacy `E_NQ-100`
are the SAME series: 205,732 overlapping minutes, zero differences, 1-min return correlation
1.000000, opening range identical on 100% of shared sessions. The earlier concern that these were
different products is resolved — they are not.

**CM-C1 reproduces on the canonical store**, like-for-like 2016→2026: +0.1508R vs +0.1534R legacy.

## 2026-09-17 — D-022: the canonical window FLATTERS our result — carry both figures
The canonical store starts 2016-01-04; our published result ran from 2013-08-21. The dropped 2.4
years contain our worst period (2014, −0.19R). Same frozen strategy:

| Window | Net | Dev ≤2021 | Max DD |
|---|---|---|---|
| 2013-08 → 2026 (published) | +0.1152R | +0.0491R | 54R |
| 2016-01 → 2026 (canonical) | +0.1508R | +0.0917R | 29R |

A 31% improvement and half the drawdown, none of it real. **Both figures are to be reported
together wherever CM-C1 is cited**, so the shorter window is never mistaken for an improvement.
Back-extension requested.

## 2026-09-17 — D-023: store defect reported (silent 7.2% read)
Reading `Canonical/<tf>/<inst>/<side>/CURRENT/` directly returns only the years in that delta
version — 241,688 of 3,366,965 NAS100 rows (7.2%) with no error. `mdlib` (the documented safe
loader) is not importable. Both reported to the Market Data Engineer; a local version-chain
resolver is in use as a stopgap and will be deleted once `mdlib` is available.

## 2026-09-17 — D-024: second source (@tsugitrades) opened as a SEPARATE branch, not merged
A 15-slide Instagram carousel, "15Min ORB Trading Strategy", from **@tsugitrades** — a different
author from Max Options Trading. Filed under `14_SECOND_SOURCE/`. It does **not** enter the Max
evidence pack and has no bearing on Track A. Nothing in it is treated as corroborating Max.

Three claims in it were not already in the register and were pre-registered and tested:
TSUGI-01 (VWAP as directional confirmation), TSUGI-02 (sweep / V-shape recovery),
TSUGI-03 (edge-interaction / "straddle", raised by Simon in the same session).
Everything else in the carousel maps onto families already decided.

## 2026-09-17 — D-025: TSUGI-01 VWAP confirmation — NO SIGNAL
Session-anchored VWAP is mechanically pinned inside the opening range, so "price vs VWAP" is 98.9%
collinear with the ORB direction rule and cannot filter. Re-tested fairly with an **overnight-
anchored** VWAP (18:00 NY prior day), which is not pinned inside the range:

pooled 5 instruments, n=9,360 — agree +0.0801R (n=7,367) vs disagree +0.0706R (n=1,990),
difference **+0.0094R, permutation p=0.737**. Per-instrument signs disagree (+0.165 XAUUSD,
−0.162 GBPUSD). The filter discards 21.3% of trades and buys nothing.
**Classification: NO SIGNAL. Not adopted.**

## 2026-09-17 — D-026: TSUGI-02 sweep / V-shape recovery — FALSIFIED
Failed break beyond an ORB edge, reclaimed within 30 minutes, traded in the opposite direction.
Pooled n=10,870: **−0.105R** (R = 0.5W) and **−0.130R** (structural stop beyond the sweep extreme).
Negative on 5/5 and 4/5 instruments respectively; development and holdout both negative. Twelve
sub-cuts on NAS100 (sweep depth quintiles, decisive reclaim, reclaim speed, VWAP agreement) produced
no positive subset that held its sign across dev/holdout.
**Classification: FALSIFIED. Reversal at the opening range is not a viable family here.**

## 2026-09-17 — D-027: TSUGI-03 edge interaction — right variable, WRONG SIGN, and unharvestable
Hypothesis (Simon): winners range along the ORB edge with candles printing body/wick on both sides
of the level in the same candle; losers sit cleanly outside, return, and run straight to stop.

**The variable discriminates. The sign is the reverse of the hypothesis.**

1. Look-ahead version (20-bar window ending AT the entry bar): zero-straddle +0.168R vs any-straddle
   +0.026R, difference +0.142R, p=0.0001, same sign on 5/5 instruments.
2. **That version is contaminated.** The entry bar's body needs its close, which is unknown when a
   touch-triggered entry fires. Re-run with the window ending at ei−1: difference falls to
   **+0.044R, p=0.062**, XAUUSD flips sign, and development does not improve at all (+0.043 vs
   +0.041 baseline). **Not established.**
3. The only way to observe the candle's body is to enter on its close instead of on the touch.
   That delay costs **−0.1554R** pooled and takes the candidate from +0.078R to −0.078R — an
   independent replication of the confirmation-candle finding (−0.16R), now reproduced with the
   weakest possible confirmation, a single bar. Within that arm the hypothesis is again reversed:
   in-and-out −0.136R vs clean-outside −0.065R, difference −0.071R, p=0.015, 4/5 instruments.

**Conclusion: the edge-interaction variable carries roughly 0.07R of information, and extracting it
costs 0.155R. It is real and it is not worth having.** The governing constraint stands: the entry
price is the ORB edge, and any delay past the touch destroys the candidate.
**Classification: HYPOTHESIS CONTRADICTED IN SIGN; effect real but unharvestable.**

## 2026-09-17 — D-028: correction issued mid-analysis
I reported to Simon that the edge-interaction effect "replicates on all five instruments" before
running the causality check. That statement was made on the contaminated window and is withdrawn;
the causal figure is +0.044R at p=0.062, which does not support the word "replicates". Recorded here
because the claim was made aloud before it was verified.

## 2026-09-17 — D-029: futures 1m data now exists but CANNOT decide CM-C1
The canonical store gained `YF_*` Yahoo Finance futures on 17 Sep: YF_NQ, YF_MNQ, YF_ES, YF_MES,
YF_GC, YF_MGC, YF_CL, YF_MCL, YF_SI, YF_SIL. **1-minute history is ~30 days** (YF_NQ: 2026-08-19 →
2026-09-17, 27,986 rows, ~21 sessions), hourly ~2 years, daily to 2002. At one trade per day this is
roughly 15 trades — two orders of magnitude short of a decision, and the series is front-month
continuous with an undocumented roll, no back-adjustment and last-trade prices only (no bid/ask, so
no measurable spread). **CM-C1 remains DATA-LIMITED.** The 1m history grows weekly; a decision
becomes possible in roughly 2–3 years of accumulation, or immediately with a paid futures vendor.

## 2026-09-17 — D-030: COST ERROR in the same-day TSUGI runs — corrected, figures restated
The TSUGI-01/02/03 runs charged **half or less** of the registered round-trip cost on four of five
instruments: NAS100 1.23 vs registered **2.92**, US500 0.50 vs **1.26**, XAUUSD 0.35 vs **0.75**,
EURUSD 0.3 pips vs **2.7**, GBPUSD 0.8 pips vs **4.9** (`COST_R_FEASIBILITY.csv`). The spread was
charged once instead of on both legs, and FX commission was omitted entirely.

Restated pooled CM-C1 baseline, n=9,360:

| Cost basis | net | dev ≤2021 | holdout >2021 |
|---|---|---|---|
| as run (undercharged) | +0.0780R | +0.041 | +0.127 |
| registered futures/spot | **−0.1263R** | −0.177 | −0.059 |
| registered CFD/spot | **−0.1761R** | −0.245 | −0.086 |

Per instrument on registered CFD/spot: NAS100 **+0.065**, US500 −0.105, XAUUSD −0.160,
EURUSD −0.257, GBPUSD −0.416. The record itself was not wrong — the published +0.150R was always on
NQ-futures cost sizing and the CFD figure was always ~0 — but the same-day cross-market figures were
overstated and are withdrawn.

## 2026-09-17 — D-031: there is NO directional information in this data; every "pattern" is cost/R
Testing each same-day finding on **gross** returns, which contain no cost at all:

| Split | net difference | **gross** difference | p (gross) |
|---|---|---|---|
| VWAP agrees vs disagrees | +0.113R | **+0.0005R** | 0.985 |
| retest bar clean vs in-and-out | +0.323R | **−0.005R** | 0.857 |

Both collapse to zero. The mechanism is range width: the "bad" subsets have systematically narrower
opening ranges (in-and-out bars median R = 0.97 pts vs 3.07 pts clean), so a fixed cost consumes a
larger fraction of R. Controlling for cost/R quintile, the straddle effect is absent in Q1–Q4
(p = 0.65–0.95) and present only in Q5, where cost/R runs to 49.0 — trades that should never be taken.

**This supersedes the earlier discriminant work.** The impulse filter (imp_R), the W_rel width
finding and the edge-interaction variable are three views of the same quantity. There is no
directional edge in the ORB signal on this data. The only thing separating winners from losers is
**cost relative to the risk unit**.

## 2026-09-17 — D-032: CM-C2 — the cost/R gate. Positive, and it passes the tests that retired R≥15pt
Rule, knowable at 10:00 NY before any entry: take the trade only if
**round-trip cost ÷ R ≤ 0.15**, i.e. **opening-range width W ≥ 13.3 × round-trip cost**.
(NAS100 CFD W ≥ 38.9 pts; US500 ≥ 16.8; XAUUSD ≥ 10.0; EURUSD ≥ 36 pips — which eliminates FX.)

Registered CFD/spot costs, pooled NAS100 + US500 + XAUUSD:

| | n | net | 95% CI |
|---|---|---|---|
| ungated | 9,360 | −0.176R | [−0.198, −0.152] |
| **cost/R ≤ 0.15** | **2,445 (26%)** | **+0.1292R** | **[+0.086, +0.174]** |
| dev ≤2021 | 783 | +0.1081R | [+0.030, +0.183] |
| holdout >2021 | 1,662 | +0.1392R | [+0.088, +0.190] |

**Both halves are independently significant.** This is the first candidate in the programme where
that is true.

Against the three criteria that retired the R≥15pt screen:
1. **Monotonic** across seven disjoint bands: +0.167 / +0.125 / +0.110 / −0.000 / −0.079 / −0.267 /
   −0.554, with win rate monotone too (55.1% → 27.1%).
2. **Per-year stable**: positive in 9/11 years; the two exceptions are 2017 (n=14) and 2018 (−0.012,
   flat). The **rejected** bucket is negative in 11/11 years.
3. **Holdout CI excludes zero**, and so does development.

Frequency and drawdown: NAS100 122 trades/yr +0.158R maxDD 20.6R; US500 62/yr +0.119R maxDD 16.3R;
XAUUSD 37/yr +0.077R maxDD 16.0R.

**Classification: CM-C2, PROVISIONALLY SUPPORTED, awaiting pre-registered forward confirmation.**
The 0.15 threshold was selected from a grid; the mechanism is principled and monotone, but the exact
number is not yet out-of-sample.

## 2026-09-17 — D-033: the dev/holdout asymmetry is EXPLAINED — it was nominal index level
The unexplained gap (dev +0.083 vs holdout +0.234) has been the programme's largest open worry.
Median NAS100 cost/R by year: **0.286 (2016) → 0.033 (2026)**, as median opening-range width went
20.4 → 176.2 points while round-trip cost stayed fixed at 2.92. The index rose roughly fivefold; the
cost did not. The ungated strategy therefore improved over time for reasons that have nothing to do
with edge.

**The gate is not itself a regime artefact** — within 2022–2026 alone it still adds:
gated +0.1407R [+0.089, +0.193] vs ungated +0.0656R [+0.022, +0.109], and the rejected bucket is
negative in every year. But the tailwind must be named: it persists while nominal index levels rise
and spreads do not. If CFD spreads widen proportionally with price, it reverses.

## 2026-09-17 — D-034: Track B (FX) closed on cost arithmetic
EURUSD and GBPUSD opening ranges are too narrow relative to registered round-trip costs (2.7 and 4.9
pips including commission). At the cost/R ≤ 0.15 gate, **12 and 3 trades** respectively survive out
of ~1,900 each. Ungated: EURUSD −0.257R, GBPUSD −0.416R. This is an arithmetic closure, not a
behavioural one. **Track B: CLOSED.**

## 2026-09-17 — D-035: FILL DEFECT in the frozen spec — CM-C2 does not survive it, and CM-C1 is affected
Found while writing the TradingView implementation. The frozen spec has `retest_tol_W = 0.10`: a
retest counts when price comes within 0.10 × W of the range edge, and the model then fills the trade
**at the edge**. On this data:

> **Only 25.8% of entries actually reach the edge.** The other 74.2% are filled at a price that
> never traded.

Restated on the gated set, registered CFD costs, pooled NAS100 + US500 + XAUUSD (n = 2,370):

| Fill convention | net | 95% CI | dev | holdout |
|---|---|---|---|---|
| A — research: always fill at the edge | +0.1328R | [+0.088, +0.175] | +0.117 | +0.140 |
| **B — realistic: limit rests in the tolerance band** | **−0.0257R** | [−0.066, +0.015] | −0.038 | −0.020 |
| **C — limit exactly at the edge (n=618 only)** | **−0.0655R** | [−0.148, +0.020] | −0.073 | −0.062 |

Per instrument under B: NAS100 −0.009, US500 −0.040, XAUUSD −0.057. Portfolio of the three, 1R each:
**−60.8R over 1,507 trading days, 51.6% negative days, max drawdown 82.1R.**

**CM-C2 is withdrawn.** The +0.129R of D-032 was the fill convention, worth ≈ +0.16R, not an edge.

**This defect is older than today.** `retest_tol_W = 0.10` is in the CM-C1 spec that produced the
published +0.115R / +0.150R, so those figures carry the same bias and must be re-derived under
convention B before being cited again. The gate of D-032 and the asymmetry explanation of D-033
remain valid as *descriptions of the cost structure* — cost/R is still the dominant variable and the
index-level drift is still real — but neither delivers a positive expectancy.

Convention A cannot be implemented in TradingView at all, because the platform will not fill a limit
at a price the bar did not trade through. That is the cleanest available proof that it was not real.

**Classification: CM-C2 FALSIFIED. CM-C1 published figures SUSPENDED pending re-derivation.**

## 2026-09-17 — D-036: LOSS FORENSICS II — the loss count is real, and it is not fixable
SVP challenge: the number of losses is not accepted. Re-run on the honest fill (convention B),
registered costs, gated set, n=2,370 across NAS100/US500/XAUUSD. Losses regrouped by the price
path BEFORE the stop was hit, on axes that are free to vary.

**First, the count is not an artefact.** The conservative same-bar rule (charge the worse outcome
when stop and target both fall inside one minute) fires on **0 of 2,370 trades** in this
configuration. The 11.3% figure in the earlier record belonged to a different entry geometry. No
loss in this book is a coin flip resolved against us.

**Exit census**

| Exit | n | % | mean gross | mean net | total net |
|---|---|---|---|---|---|
| full stop | 882 | 37.2 | −1.000 | −1.072 | **−945.8R** |
| time (180 min) | 591 | 24.9 | +0.426 | +0.362 | +213.7R |
| trail stop | 488 | 20.6 | +0.399 | +0.324 | +157.9R |
| target | 256 | 10.8 | +2.002 | +1.922 | +492.0R |
| end of day | 153 | 6.5 | +0.206 | +0.140 | +21.4R |

**Loss taxonomy — what happened before the stop** (a stop exit has MFE < 1R by construction, since
the trail arms at +1R and moves above entry)

| Group | n | % of stops | mean MFE | mean hold | crossings | total net |
|---|---|---|---|---|---|---|
| L1a never favourable, stopped ≤10 min | 9 | 1.0 | 0.06R | 6.8 min | 0.1 | −9.8R |
| L1b never favourable, ground down | 78 | 8.8 | 0.06R | 48.7 min | 1.0 | −83.5R |
| **L2 small push 0.10–0.40R** | **464** | **52.6** | 0.24R | 44.9 min | 3.3 | **−496.9R** |
| L3 half way 0.40–0.75R | 228 | 25.9 | 0.54R | 67.8 min | 6.1 | −244.6R |
| L4 nearly armed 0.75–1.00R | 103 | 11.7 | 0.88R | 86.2 min | 6.9 | −111.1R |

**90% of losses go favourable before they fail.** Instant rejection is 1% of stops. The picture is
not a bad entry — it is a trade that works, then does not.

**A wider stop does not rescue them.** After being stopped, only **39.0%** ever return to breakeven
inside what remains of the 180-minute window; 13.6% reach +1R, 6.0% reach +2R. Median post-stop
excursion **−0.285R**. The stop is not premature.

## 2026-09-17 — D-037: exit-policy sweep — eight policies, all negative, spread 0.025R
Entry and stop held fixed; only post-entry management varied. Pooled, n=2,370:

| Policy | net | 95% CI | dev | holdout |
|---|---|---|---|---|
| V0 current (2–4R target, trail extreme−1.0R) | −0.0257 | [−0.067, +0.015] | −0.038 | −0.020 |
| V1 trail extreme−0.5R | −0.0204 | [−0.059, +0.019] | −0.036 | −0.013 |
| **V2 trail extreme−0.25R (best)** | **−0.0114** | [−0.050, +0.026] | −0.033 | −0.001 |
| V3 hard TP +1.0R | −0.0218 | [−0.059, +0.013] | −0.045 | −0.011 |
| V4 hard TP +1.5R | −0.0205 | [−0.063, +0.022] | −0.041 | −0.011 |
| V5 hard TP +2.0R | −0.0309 | [−0.076, +0.014] | −0.067 | −0.014 |
| V6 half off +1R, rest trail −0.5R | −0.0363 | [−0.072, −0.000] | −0.057 | −0.027 |
| V7 breakeven at +1R, run to 2–4R | −0.0248 | [−0.068, +0.019] | −0.043 | −0.017 |

The stop count is **882 in every policy** — management cannot touch it. The entire achievable range
on the winning side is 0.025R, against a 0.041R shortfall. Best policy is negative on 2 of 3
instruments and its development half is −0.033. **No exit rule rescues this.**

## 2026-09-17 — D-038: nothing observable at entry predicts the stop
Ten pre-entry features tested against full-stop-versus-not (base rate 37.2%):

| feature | rank-biserial | p |
|---|---|---|
| reached the edge | +0.051 | 0.010 |
| direction | −0.052 | 0.016 |
| W_rel | −0.049 | 0.044 |
| imp_R | +0.049 | 0.053 |
| cost/R, latency, W, day-of-week, straddle, outside-fraction | ≤ 0.030 | 0.22–0.92 |

Largest effect size 0.052. Ten features screened, three at p<0.05, effects at the noise floor. No
quartile of any feature produces a positive bucket. **The loss groups are defined by post-entry path
and post-entry path is not knowable at entry.** This closes the discriminant search.

## 2026-09-17 — D-039: the shortfall is 0.041R per surviving trade — and direction is beta, not edge
| | n | % | mean | total |
|---|---|---|---|---|
| full stops | 882 | 37.2 | −1.0723R | −945.8R |
| everything else | 1,488 | 62.8 | +0.5948R | +885.0R |

Survivors must average **+0.6356R** to break even and deliver **+0.5948R** — short by **0.0409R**
each, which is the −60.8R result. Equivalently, the stop rate must fall from 37.2% to **35.0%**.

This is a near miss, which is why the family keeps looking promising. It is still a miss.

**Direction.** Long +0.0054R [−0.048, +0.057], short −0.0634R [−0.124, +0.002]. But the split
**reverses on gold** (long −0.122, short +0.023) while holding on both indices (NAS100 +0.034/−0.063,
US500 +0.024/−0.114). A directional effect that follows each instrument's own decade-long trend and
flips where the trend flips is **beta, not edge**. Long-only is not adopted.

**Conclusion: the loss count is accepted as real, correctly measured, structurally unavoidable given
the stop, and not attributable to any conservative modelling rule. The family is exhausted from the
exit side and from the entry-filter side.**

## 2026-09-17 — D-040: the stop rate is a DIAL, not a defect. Gross is invariant.
SVP follow-up: segment the full stops by candle overlap, by whether price returns through the ORB
level after the direction is set, by direction strength, and by ORB size. n=2,370, 882 stops,
honest fill, registered costs.

**Q1 — overlapping candles: NO.** Mean pairwise overlap of consecutive 1-minute bars
(overlap ÷ union of ranges) is identical for stops and survivors: within the confirming block
0.4378 vs 0.4370, r=+0.015, p=0.56; during the wait to entry 0.4552 vs 0.4677, r=−0.059, p=0.11.
Chop around the level carries no information.

**Q2 — return through the ORB level after the direction: STRUCTURALLY IMPOSSIBLE before entry.**
**0.0%** of all 2,370 trades — stops and survivors alike — post a 1-minute close back inside the
opening range between direction confirmation and entry. The reason is mechanical: the retest
tolerance band sits *between* the direction and the range, so the entry always fires before price
can get back inside. **Max's price-based invalidation (close back inside the ORB before the retest)
can never trigger in this implementation.** That is a spec finding, and it retires the optional test
carried since RR-002.
After entry, 42.0% of stopped trades DID exceed the pre-entry impulse and still failed (survivors
91.3%) — post-entry, and largely tautological.

**Q3 — direction strength: it moves the stop rate, and it does not pay.**
Confirming-block range ÷ W: stops 0.838 vs survivors 0.772, **r=+0.126, p=0.0005** — the largest
effect size found anywhere in this programme. Stop rate by quintile: **26.8 / 37.1 / 37.3 / 42.0 /
42.8%**, monotone. Block body ÷ W r=+0.056 p=0.023; close-beyond ÷ W r=+0.048 p=0.048; efficiency
r=−0.051 p=0.040.

**Q4 — ORB size: relative size matters, absolute size does not.**
W in points: r=+0.015, p=0.55 — nothing. W ÷ yesterday's true range: **r=−0.121, p=0.0005**, stop
rate by quintile **42.8 / 40.7 / 39.5 / 33.3 / 29.7%**, monotone. W ÷ own 20-day median: r=−0.049,
p=0.046.

**Q3 and Q4 are the same variable: ORB size relative to realised volatility.** Combined into one
rank score, it is the strongest control on the loss count in the programme — and it is priced at par:

| Quintile | n | stop rate | survivor mean | **gross** | net |
|---|---|---|---|---|---|
| Q1 | 474 | 44.1% | +0.823R | +0.066R | −0.016R |
| Q2 | 474 | 41.6% | +0.726R | +0.053R | −0.021R |
| Q3 | 474 | 38.4% | +0.595R | +0.025R | −0.045R |
| Q4 | 474 | 36.7% | +0.554R | +0.025R | −0.042R |
| Q5 | 474 | 25.3% | +0.355R | +0.061R | −0.004R |

Stop rate falls 44.1% → 25.3%. Survivor payoff falls +0.823 → +0.355, in exact step.
**Gross spread across the five settings is 0.041R at permutation p = 0.973 — statistically identical.**

**The loss count can be set anywhere between 25% and 44% and the expectancy does not move.** It is a
dial, not a defect. Q5 reaches a 25.3% stop rate — far below the 35.0% the D-039 arithmetic asks for
— and is still negative, because its survivors deliver +0.355R against the +0.361R that stop rate
requires.

## 2026-09-17 — D-041: the whole programme in one line, and the last escape closed
**Whole book: gross +0.0457R (CI [+0.0057, +0.0866]) − cost 0.0713R = net −0.0252R.**

There is a real raw edge in the opening-range retest. It is worth about **0.046R**. Harvesting it
costs **0.071R**. That single subtraction is the entire eleven-year result.

The obvious escape — pay less than 0.046R by tightening the cost gate — **fails, because the gross
edge is not independent of the cost**:

| gate cost/R ≤ | n | trades/yr | gross | cost | net | dev |
|---|---|---|---|---|---|---|
| 0.15 | 2,369 | 221 | +0.046 | 0.071 | −0.025 | −0.038 |
| 0.10 | 1,856 | 173 | +0.027 | 0.059 | −0.032 | −0.055 |
| 0.07 | 1,220 | 114 | +0.027 | 0.045 | −0.018 | −0.017 |
| 0.05 | 718 | 67 | +0.015 | 0.035 | −0.020 | −0.085 |
| 0.04 | 458 | 43 | **−0.016** | 0.030 | −0.045 | −0.219 |
| 0.03 | 220 | 21 | +0.027 | 0.024 | +0.004 | −0.098 |

Gross falls as the gate tightens. Low cost/R means a wide opening range, and the raw edge lives in
the narrow ones — the same trades where cost consumes it. The 0.03 bucket is +0.004R on 220 trades
with a CI of [−0.115, +0.126] and a development half of −0.098: noise.

**Conclusion. The opening-range retest family is closed on this data.** The SVP's challenge is
answered: the loss count is real, correctly measured, free of modelling artefact, tunable across a
19-point range with no effect on expectancy, and not the reason the strategy fails. The reason is
that a 0.046R signal cannot pay a 0.071R toll.

**Only two things could reopen it:** a materially larger raw edge from a different entry geometry
(not a filter on this one), or a cost structure below ~0.046R per trade — which on current spreads
means native futures with a range wide enough to carry them, and that needs history the store does
not yet have.

## 2026-09-18 — D-042: the +0.046R gross was SELECTED. Unselected it is +0.023R, and it is decaying.
Asked whether the programme is worth continuing. Before answering, the one number that would justify
it was pressure-tested. It does not hold up.

**The gross figure quoted in D-041 was measured on the gated, three-instrument subset — a selected
population.** Unselected:

| Population | n | gross | 95% CI |
|---|---|---|---|
| gated cost/R ≤ 0.15, indices + gold (**selected**) | 2,665 | +0.0482R | — |
| **ungated, all five instruments (unselected)** | **9,360** | **+0.0230R** | **[+0.0013, +0.0450]** |

The honest interval's lower bound is **+0.0013R**. The raw edge touches zero.

**And it is decaying.** Gross by year, ungated, all five:

| 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| −0.011 | +0.027 | −0.002 | +0.037 | +0.037 | −0.012 | **+0.073** | **+0.070** | +0.016 | +0.009 | **+0.001** |

Essentially all of it is 2022–2023. The three most recent years run +0.016, +0.009, +0.001 — the raw
signal has decayed to nothing in the period a deployment would actually trade.

**The ceiling, priced.** Gated three-instrument set, 249 trades/yr:

| | per year | max DD | at 1% risk |
|---|---|---|---|
| **gross, at literally zero cost** | +12.0R | 31.4R | +12% a year, 31% peak drawdown |
| net, registered costs | −7.6R | 89.4R | −7.6% a year, 89% drawdown |

A zero-cost fantasy returns 12% a year against a 31% drawdown — a 0.38 return-to-drawdown ratio
**before a single penny of cost**. Nobody trades at zero cost.

## 2026-09-18 — D-043: the no-fill-ambiguity geometry has no edge either
The one entry that cannot suffer the D-035 fill defect — immediate entry at the CLOSE of the
confirming 30-minute block, a price that certainly traded, no retest and no tolerance:

| | n | gross | 95% CI | gross dev | gross holdout |
|---|---|---|---|---|---|
| retest entry, ungated | 9,360 | +0.0230R | [+0.0013, +0.0450] | +0.013 | +0.036 |
| **immediate at block close, ungated** | **13,109** | **+0.0088R** | **[−0.0075, +0.0255]** | **−0.009** | +0.031 |

**The immediate entry's gross interval includes zero and its development half is negative.** Costed
and gated it is worse than the retest (−0.048R vs −0.033R). Gross is positive on the three index and
metal series and negative on both FX. This closes the most obvious "different entry geometry".

## 2026-09-18 — D-044: RECOMMENDATION — do not carry this forward. Carry the method forward.
The opening-range retest family is **closed**, and so is the nearest alternative geometry. The
position is not a near miss waiting for one more idea; it is a signal worth about 0.023R that has
faded to 0.001R, against a toll of 0.071R, with every lever measured:

| Lever | Result |
|---|---|
| Entry filters (14+ features, 3 studies) | zero on gross |
| Stop width | wider is worse; only 39% of stops ever recover |
| Exit management (8 policies) | 0.025R total range, all negative |
| Stop-rate dial (ORB vs realised vol) | moves 44%→25%, gross invariant, p=0.973 |
| Cost gate | gross falls as the gate tightens |
| Alternative entry geometry | gross CI includes zero |

**A concrete bar for any future candidate in this programme: gross expectancy must exceed ~0.07R
per trade to survive measured CFD costs, or ~0.05R on futures economics. Measure gross first.**
Everything that failed here failed that bar, and every apparent success was either a cost artefact,
a fill that never traded, or a selected subset.

**What is worth keeping:** the canonical data pipeline, the registered cost model, the honest-fill
discipline, the gross-before-net test, and the stop-rate-dial result. Those tools found four
independent errors of mine in a single day. They make the next hypothesis cheap to test, and they are
the actual asset this programme produced.

## 2026-09-20 — D-045: IMPLEMENTATION AUDIT — MODEL V1 does not implement break→retest→rejection
Mandate 20.1. Audit performed before any new backtest. Code reference: `stop_segment.py` / `loss_deep.py`,
frozen SPEC in `futures_pipeline.py`.

**MODEL V1's actual event sequence has no break state and no rejection state.** The code goes directly
from range completion to "first 30-minute block whose last 1-minute close lies outside the range", then
to "first subsequent bar whose low comes within 0.10·W of the broken edge", then fills. There is no
T2 (first break) and no T-rejection. Measured on 2,370 trades:

| | |
|---|---|
| entries on the confirming bar itself (lat = 0) | **52.1%** |
| entries with lat ≤ 2 minutes | 61.8% |
| entries where price actually **touched** the edge | 26.1% |
| **entries with a real wait (>2 min) AND a real touch** | **4.6%** |
| confirming close already inside the 0.10·W tolerance band | 35.5% |

**In the majority of trades there is no retest.** The retest condition `low ≤ edge + 0.10·W` is satisfied
by the confirming block's own final bar whenever that block closes within 0.10·W of the edge. V1 is
therefore trading *"a 30-minute candle closed marginally outside the range — buy at edge + 0.10·W"*,
which is a different trade from the one the sources describe.

**The direction signal is also stale.** First break → confirmation: median **28 minutes**, mean 44.7,
p90 **107 minutes**. By the time V1 declares direction, the break is on average three quarters of an
hour old. Visual forensics (figs A–E, `13_CROSS_MARKET/WORK/figs/`) show the characteristic failure:
the directional move completes between the break and the confirmation, and V1 enters on the exhaustion.

None of this changes gross: lat=0 +0.037R, lat 3–15m +0.085R, lat>15m +0.053R; confirm-inside-band
+0.047R vs outside +0.045R.

## 2026-09-20 — D-046: pre-entry ORB re-entry is a THEOREM, not a measurement
The 0.0% reported in D-040 carried no information. Proof, for a long (dr=+1, edge = ORB high = `oh`):

- entry index `ei` = **first** i ≥ ci with `low_i ≤ oh + 0.10·W`
- re-entry at bar i requires `close_i ≤ oh`
- but `low_i ≤ close_i ≤ oh < oh + 0.10·W`, so any bar satisfying re-entry also satisfies the entry
  condition, hence its index is ≥ `ei`
- the re-entry window measured was `[ci, ei−1]`, strictly before `ei` ⟹ **empty by construction**

Verified: 1,135 trades have a non-empty wait window; **0 violations**, as the algebra requires.

**Generalisation, and this is the operative point:** *any price-based invalidation requiring price at or
inside the ORB edge can never fire ahead of an entry trigger placed at or outside that edge.* The
invalidation is strictly dominated by the entry. To make invalidation testable the entry must require
something **beyond proximity** — specifically a rejection event (price reaches the level and is refused).
**MODEL V1 has no rejection state, and that absence is exactly what makes invalidation unreachable.**

## 2026-09-20 — D-047: CONCEDED — "direction strength" was the wrong name, and the wrong claim
D-040 reported `block_range_W` = (confirming block high − low) ÷ W under the heading "direction
strength". That was my phrasing and it is not supportable. Decomposition:

| against | spearman |
|---|---|
| block body ÷ W (displacement) | +0.776 |
| block close beyond edge ÷ W (displacement) | +0.418 |
| ORB width ÷ yesterday TR | −0.365 |
| ORB width in points (the denominator) | −0.097 |
| cost ÷ R | +0.158 |

So it is a genuine **magnitude/displacement composite**, not a pure volatility artefact — "confirming-block
magnitude" is the correct name. But the substantive error is larger than the label: it was reported as
though it established directional *quality*, and it does not. Every member of the family — raw block
range in points, range ÷ W, close-beyond ÷ W, body ÷ W, efficiency — moves the **stop rate**
(p = 0.0005 to 0.05) and moves **gross by nothing** (p = 0.21 to 0.76). They reallocate outcomes between
stop and non-stop without changing expected return. **The term "direction strength" is withdrawn from the
record.**

## 2026-09-20 — D-048: STAGE 12 — native futures audit. 21 sessions. Cannot test a 15-minute ORB.
| Instrument | 1m | 15m | 1h | 1d | Sides | Roll |
|---|---|---|---|---|---|---|
| YF_NQ / MNQ / ES / MES / GC / MGC / CL | **2026-08-19 → 09-17 (21 sessions)** | same 21 sessions | 2024-09-22 → (2 yrs) | 2000 → (NQ/ES/GC/CL), 2019 → (MNQ/MES) | **TRADE only** | **undocumented, unadjusted** |

No BID/ASK on any futures series, so **spread is not measurable** and cost must be assumed. 1-hour
history is two years but cannot build a 15-minute opening range. **21 sessions ≈ 21 trades: adequate for
a plumbing check, not for economics.** Missing, stated exactly: 1-minute NQ/MNQ bid+ask, 2016→present,
documented roll. Dukascopy cannot supply it (D-029); a paid vendor or an exchange feed can.

## 2026-09-20 — D-049: OUTCOME B — MODEL V2 is justified. Three minimum corrections, no optimisation.
Research specification (20 Sep, 18 videos, two independent authors) versus MODEL V1:

| # | Source requirement | MODEL V1 | Verdict | Material? |
|---|---|---|---|---|
| 1 | 15-minute range, 09:30–09:45; **both authors explicitly reject 30-minute** | 30-minute range | **MISMATCH** | Yes |
| 2 | Direction = **15-minute** close outside | 30-minute block close | **MISMATCH** | Yes — causes the 28-min median staleness |
| 3 | "Then wait one more candle" | no wait; 52% enter on the confirming bar | **MISMATCH** | Yes |
| 4 | Entry on a **rejection** (TRT / break-and-retest) | proximity touch, no rejection state | **MISMATCH** | Yes |
| 5 | Stop sized to **recent wicks** (~25 pts NQ) | 0.5 × W = the ORB midline | **MISMATCH** | Yes |
| 6 | Pre-entry invalidation: close back inside ORB | unreachable by construction (D-046) | **MISMATCH** | Yes |
| 7 | Target: Max ~1R on ORB levels; CeeWilli 2.75–3.75R external liquidity | next extreme, 2R floor 4R cap | PARTIAL | Moderate |
| 8 | NQ/MNQ futures | OTC index-CFD proxies | MISMATCH | Known, data-limited |

**The stop is the one that cannot be settled from existing evidence, and the record must not pretend
otherwise.** The R-band measurement already in the log (+0.110R all → −0.034R at R≥20) varied R by
**selecting days with wider ranges**, which changes the trade population. Changing the stop *rule*
changes the payoff on the **same** population. Those are different experiments and the first does not
answer the second. Treating it as settled would be exactly the conflation this audit exists to catch.

**MODEL V2, minimum source-supported form, no parameter search:** 15-minute range → 15-minute close
outside → wait one further 15-minute candle → entry requires a **rejection** at the level (not mere
proximity) → stop beyond the rejection swing, decoupled from W → pre-entry invalidation now reachable
and therefore testable. Continuation and failed-break populations reported separately (Stage 11).
Gross first, full unselected population first.

**What does NOT get relitigated:** the fill discipline (D-035), the cost model (D-030), gross-before-net
(D-031), and the confirmation-delay measurement as a *fill-timing* result. Note carefully that the
−0.155R confirmation finding measured **one minute** of delay on V1 geometry; the source's "wait one
more 15-minute candle" is a different object and is not pre-judged by it.

## 2026-09-20 — D-050: MODEL V2 built to SPEC-SF-1. Acceptance case PASSES, population gate FAILS.
Explicit state machine (`13_CROSS_MARKET/CODE/model_v2.py`): ORB 09:30–09:45 wick-to-wick → BREAK
(1m close beyond boundary, no order) → RETURN (trade back to boundary; close inside permitted) →
[REJ arm: rejection bar] → ENTRY SIGNAL (first later 1m close beyond) → FILL at the next bar's open →
stop A (entry-bar extreme) or B (return-cluster extreme) → target = nearest prior-session extreme →
post-entry invalidation on first close back inside → 11:30 expiry → one attempt per side.

**Acceptance case V-01 (CeeWilli ES1! 28 May 2026): PASS.** Native ES 1m begins 2026-08-19, so run on
US500 as the closest series (flagged proxy). Reproduced bar for bar: break 10:00, close back inside
10:02, **wick above ORH with close inside at 10:02 and 10:05 correctly refused entry**, qualifying body
close 10:07, fill 10:08 at the next open.

**Population gate: FAIL.** Median break→fill is **5 minutes**; **31.1%** are the mechanical minimum of
3; 58.0% return on the very next bar; 54.4% signal on the very next bar after that. The reference case
is an 8-bar pullback with six closes back inside. **The "return" is satisfied by a one-bar wick — V1's
"proximity became entry" defect arriving by a different route.** The 7–12-minute bucket (V-01-like) is
17.8% of trades and its gross is −0.0016R.

## 2026-09-20 — D-051: stop variant A is NOT MECHANISABLE on 1-minute bars
"Beyond the entry bar's extreme" gives R→0 whenever that bar is small. R < 0.0002 × price on **20.5%**
(NAS100) and **26.2%** (US500) of trades; maximum single-trade outcome **699R** on US500. The arm's
mean is meaningless (1%-trimmed mean +1.10R). **Reported, not patched — a floor would be an invented
rule.** Variant B carried forward; its median stop is 0.085–0.129% of price against the sources'
0.076% (CeeWilli, on-screen) and ~0.10% (Max), so **variant B is faithful and variant A is not.**

## 2026-09-20 — D-052: two further specification defects, flagged not resolved
1. **SPEC-9 fill collides with SPEC-14 invalidation.** The fill is the next bar's open, which can land
   back inside the range, so invalidation can fire immediately: **49.4%** of invalidation exits occur
   within one bar of the fill.
2. **SPEC-12 produces no target on 31.8% of trades.** Those trades carry the entire apparent gross:
   **+0.2016R without a target vs −0.0166R with one** — i.e. the edge sits in trades that have no exit
   rule but invalidation, stop and the close.

## 2026-09-20 — D-053: V2 economics — gross indistinguishable from zero; CFDs cannot afford the spec
BASE-B, full unselected population, 5,689 trades, 532/yr:

| | n | gross | 95% CI | dev ≤2021 | val >2021 |
|---|---|---|---|---|---|
| NAS100 | 2,813 | +0.0654R | [−0.014, +0.149] | +0.071 | +0.059 |
| US500 | 2,876 | +0.0406R | [−0.046, +0.134] | **−0.066** | **+0.167** |
| POOLED | 5,689 | **+0.0528R** | **[−0.008, +0.113]** | +0.002 | +0.114 |

Win 14.6%, mean winner +3.72R, mean loser −0.58R, median target 5.28R. MFE reach 2R **20.2%**, 3R 13.5%,
4R 9.9%. Exits: invalidation 65.5% (−0.442R), stop 20.1% (−0.997R), target 9.2% (+2.615R), eod 5.2%
(+5.819R). Other arms: REJ removes ~29% of trades and lowers gross.

**cost/R median 0.277 → NET −0.8645R.** The source-faithful stop is ~0.1% of price; the measured CFD
round trip is 0.025–0.04% of price. **SPEC-SF-1 is unaffordable on CFD proxies.** On 21 sessions of
native futures, cost/R is **0.023 (NQ)** and 0.129 (ES) — roughly **8× better** than the proxy. This is
the first result in the programme where instrument choice is decisive rather than cosmetic.

## 2026-09-20 — D-054: STOP AND FLAG. Two blockers, no tuning.
Per mandate stop conditions: representation cannot be made objective, and required data is unavailable.

1. **Research ruling needed:** what distinguishes a qualifying return from a one-bar touch of the
   boundary? Choosing a threshold ourselves is parameter mining and is refused.
2. **Data needed:** 1-minute NQ (and ES) **bid + ask**, 2016 → present, documented roll. Section G of
   ANALYST_CURRENT shows cost/R falls ~8× on native futures — the only change measured so far that
   could make a ~0.05R gross edge tradeable.

Until (1) is answered, V2's economics describe a five-minute compression around the boundary, **not the
taught setup**, and must not be quoted as a test of the source method. `ANALYST_CURRENT.md` created.
