# DECISION LOG — cross-market ORB branch

## 2026-09-12 — X-001: branch created inside the connected folder, not as a new project
Access to `.../Projects/Trading/` was not granted this session, so the ORB Programme root could not
be located. The branch lives at `ORB Reserach Sub 2.0/13_CROSS_MARKET/` and should be relocated
under the Programme root when that folder is reachable. **No separate per-instrument project was
created**, per the mandate.

## 2026-09-12 — X-002: no futures data exists; proxies labelled, work proceeds
NQ, MNQ, ES, MES, GC and MGC are absent from the shared store. Index and gold work proceeds on
explicitly labelled CFD/spot proxies; proxy and futures evidence are never combined; futures cost
figures are sizing estimates, never measurements. Acquisition is a separate, non-blocking workstream
— the available markets were not held up for it.

## 2026-09-12 — X-003: events and range lengths PRE-REGISTERED before measurement
09:30 NY for the indices; **08:20 NY COMEX and 09:30 NY for gold, reported separately and never
merged**; 08:00 London for FX, preserving the existing programme's anchor rather than forcing the
US cash-open construction onto FX. L ∈ {5,15,30} everywhere. The 60-minute range was excluded and
its inclusion made conditional on Phase A evidence; that evidence did not appear, so it stays out.

## 2026-09-12 — X-004: the retest family is the cross-market behavioural finding
Positive in 16 of 18 cells, significant in 9, strengthening with range length, and positive in gross
trade terms in all five markets. Recorded as BEHAVIOURAL EFFECT CONFIRMED.

## 2026-09-12 — X-005: the completed close destroys information — confirmed cross-market
Touch beats close in 13 of 18 cells. Independently reproduces, on four new markets, the result the
closed Max project found in FX. The two projects are not pooled; this is a separate replication.

## 2026-09-12 — X-006: the cost problem was the stop construction, not opening-range trading
Sizing the stop off the opening range rather than the entry candle moves cost/R from ~0.28 to
0.04–0.18 on the index and gold proxies. This does **not** reopen the closed Max project; it is a
new construction on a new branch, and it is the branch's most reusable finding.

## 2026-09-12 — X-007: CM-C1 does NOT advance — DATA-LIMITED
Nasdaq retest is +0.105R [+0.060,+0.151] under NQ sizing and **−0.001R [−0.046,+0.047]** on the
measured CFD cost that is the only basis this data supports. It fails to replicate on US500, EURUSD
and GBPUSD (all negative net, positive gross). Development is materially weaker than holdout. With
72 behavioural measurements and ~40 arms examined, one positive under an assumed cost model is a
reason to acquire data, not to advance a candidate.

## 2026-09-12 — X-008: gold PARKED, not rejected
Best 2R geometry in the panel and the cheapest cost/R, but 825 sessions over 3.2 years and every
CI includes zero. Parked pending GC/MGC data. A short-sample point estimate is not permitted to
advance or to kill it.

## 2026-09-12 — X-009: FX and S&P arms COST-DESTROYED — no filtering
Gross is positive in both; the shortfall is arithmetic. Adding filters to close it would be fitting
noise. Recorded so they cannot re-enter under a new construction without new economics.

## 2026-09-12 — X-010: existing FX ORB V1 control NOT modified
Compared conceptually only; results never pooled. The structural contrast supports V1's design.

## 2026-09-12 — X-011: highest-value action is DATA ACQUISITION, not more analysis
NQ/MNQ first, then GC/MGC. Do not extend the market panel. Do not filter the cost-destroyed arms.

## 2026-09-22 — D-060: RECORD CORRECTION — Max HAS a mechanical bias rule
V5 [10:43]-[11:37] states a complete deterministic price-vs-midline bias rule. The standing note
"no mechanical bias definition exists in the Max corpus" was wrong and is retired. The quotation
was in the transcript extract the whole time; this was a reading failure, not a data gap.

## 2026-09-22 — D-061: conditional failed-break hit rates are NOT to be quoted as the effect size
The 70.8% / 77.3% figures condition on an event that is itself on the causal path to the outcome
and are measured from the break, not from the trigger. The only quotable numbers are the
forward-measured ones against the unconditional base: +4.8 to +11.5 pp. Recorded so the larger
numbers cannot re-enter a later summary.

## 2026-09-22 — D-062: much of the failed-break "edge" is geometry, not signal
Median distance remaining at the confirmation bar is 0.51-0.54 ORB widths. Hit rate falls to
46-59% where a full box remains and rises to ~79% where a quarter-box remains. Any future
economics must condition on remaining distance or it will report the geometry as an edge.

## 2026-09-22 — D-063: external FVG is NOT the continuation/failure discriminator
Within the failed-break population, far-side FVG present vs absent: 69.7% vs 73.0% (NAS100),
77.3% vs 77.4% (US500). Null on both. This does not overturn the earlier FVG-touch result
(different conditioning event) but it closes FVG as the state discriminator.

## 2026-09-22 — D-064: "it needs to hold outside of it" (V4 05:37) is NOT elapsed time
Opposite-reach by minutes held outside before invalidating: 70.3/74.1/65.4/72.1/62.1% (NAS100).
Flat. The obvious mechanisation is falsified. No replacement invented. Requires screenshot D4 —
a break Max REJECTED for not holding outside. Positive examples cannot resolve it.

## 2026-09-22 — D-065: Max's midline TP1 is internally inconsistent with his failed-break trigger
Midline already crossed before the confirmation on 53.8% / 57.6% of confirmed failed breaks.
Escalated to Research as a source-interpretation question, not resolved by the Analyst.

## 2026-09-22 — D-066: consolidation-then-failure (~17:1) is the only live lead; NOT acted on
10-bar: failed-break 441 vs continuation 27 (NAS100), 482 vs 22 (US500). The window length is a
free parameter. Three windows reported, none chosen. Measuring it properly is next cycle's work;
selecting a window on this data would be the optimisation the mandate forbids.

## 2026-09-22 — D-067: figure review changed the reported finding
Panel inspection of FAILED_BREAK_TIMING.png revealed days where the confirmation bar and the
opposite-touch bar coincide, because the "newer extreme against" reference sits at the opposite
boundary. That observation produced the remaining-distance analysis (D-062). Without the visual
review the conditional 70.8% would have been published as the result.
