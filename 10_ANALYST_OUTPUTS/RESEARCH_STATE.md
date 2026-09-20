# RESEARCH STATE — Analyst Agent

Last updated: 2026-09-12 · **PROJECT CLOSED (cycle 3, controlled closeout)**
Authoritative summary: `ANALYST_DECISION_REPORT.md`.

## Main objective
Determine whether any Max Options Trading ORB concept can be transformed into a simple,
mechanically replicable, costs-adjusted intraday edge with ≥2R potential, normally resolved within
180 minutes, and realistically automatable. **Answer: no, on the evidence available.**

## Scope of the answer — precise
- The **reconstructed** Max ORB families, tested on **Dukascopy OTC index-CFD proxies** (NAS100,
  US500) and on **EURUSD/GBPUSD spot**, did not produce a viable costs-adjusted strategy.
- The completed-close and print-through boundary representations showed no sufficient economic edge.
- Several related source-supported constructions were falsified, cost-destroyed or retired on
  geometry.
- **Source-native futures (NQ/MNQ/ES) and index/options implementations (SPX, options) remain
  UNVALIDATED because suitable data was unavailable — they have NOT been falsified.**
- Proxy agreement across two instruments and source-matched stop geometry raise confidence; they do
  not remove the instrument limitation.

## Validated findings
1. **No prospective continuation-vs-reversal selector exists.** Source-side confirmed negative
   across twelve videos, independently corroborated by P(MFE>MAE) ≈ 51% at every horizon. U-01 closed.
2. **Structural cost arithmetic.** MNQ $2.00/pt, tick 0.25 pt/$0.50. S2 realistic round trip
   1.335 pts = $2.67 against a median $17.62 risk. Breakeven = **mean** cost/R = **+0.2806R**;
   raw gross **+0.1100R**; net **−0.1707R**; shortfall **2.55×**. Audited in
   `09_VALIDATION/COSTS/COST_RECONCILIATION.md`.
3. **The edge is inversely related to tradability** — raw gross +0.110R (all) → +0.063R (R≥5) →
   +0.031R (R≥10) → **−0.034R (R≥20)**. Independent of any cost assumption.
4. **180-minute cap is not binding** — 76% of EOD excursion captured; median 38 min to 2R.
5. **The reconstruction is source-faithful** — median R 9.3 pts vs a stated 6–17, mode 9–10.
6. **Track B: the ORB concept does not transfer to FX.** Six pre-registered series; direction
   absent or negative; the print-through *destroys* information relative to the completed close;
   execution consumes **72%–124%** of the risk unit; net −0.639R to −1.050R.
7. **Track B ≥2R geometry IS present in FX** (opposite edge 4.1–4.8R away; P(MFE₁₈₀≥2R) 65–70%) —
   so FX fails on cost alone, not on geometry as Track A's reversal did.
8. **Data/cost infrastructure validated**, DST verified against the UK/US misaligned weeks.

## Provisional findings
**Compression → containment — PROVISIONALLY VALIDATED ON US INDEX-CFD PROXIES.**
Six 15-minute candles inside the range → subsequent excursion materially smaller (NAS100 27.0 vs
58.7 pts), containment probability up (36.1% vs 14.9% within ±15 pts), **breakout expansion not
supported**, and **the corresponding fade construction also fails**.
**Replicated in FX** (EXP-016): ratio 0.56–0.89 in all four series, permutation p ≤ 0.0065, below 1
in development and holdout, strongest at the 09:30 New York anchor.
Legitimate value: a **day-state hypothesis** — *prolonged opening-range containment may identify
suppressed subsequent range expansion*. Transferable to another project **only after replication
under that project's instrument, session and range definition.** Not a reusable input yet.

## Falsified representations
F1 · F2 · F5 · F6 · P-1 · G-4 · 5-minute ORB — on proxies, per the scope above.
Also CL-012 as opening-range *width* (an Analyst hypothesis) and the tradable branch of CL-012
proper (compression → larger move).

## Corrections made rather than explained around
- **D-005R** — cycle 1's "CL-012 FALSIFIED" came from a width test. RC-001 accepted; the width
  result was in fact consistent with the source's framework. CL-012 then tested properly.
- **D-014** — two cost errors (median-vs-mean labelling; double-counted entry slippage). Corrected
  and propagated; superseded figures marked in place.
- **D-016** — Track A wording corrected for scope (see above).

## Cost-destroyed constructions
MC-7 on NAS100 (−0.171R) and US500 (−0.929R); all six Track B FX series (−0.639R to −1.050R);
G-1-gated MC-7 (−0.230R); the 5-minute ORB (−0.236R).

## Retired / parked
**Retired:** F1, F2, F4a/b, F5, F6, P-1, 5-minute ORB, and the cycle-1 R≥15pt screen (does not
replicate: gross −0.048R).
**Parked:** F3 break-and-retest (with reason), MC-4 three-bar pattern, G-3 news veto (untestable —
shared calendar holds 13 recent rows).

## Unresolved, and closed for decision
Advanced ORB indicator logic (paid, out of scope) · U-02 retest tolerance (the source declines to
define it, C-09) · G-3 news veto (no data). None can close a 2.55× gap.

## Active candidates
**None.** Both tracks closed.

## Open Research Agent requests
**None.** RR-001 and RR-002 INCORPORATED; RC-001 ACCEPTED and actioned. Queue closed.

## Comparison with the existing FX ORB control
Conceptual only; results never pooled. V1 (00:00–08:00 range, 0.10×ATR14 buffer, opposite-side
stop, 16:00 exit, ≈ +0.049R) is **not replaced**. The salient contrast: V1's opposite-side stop
produces a risk unit large enough to absorb FX costs; the Max construction's few-pip stop does not.

## Current highest-value action
**Outside this project.** (1) Test H-01 in the existing ORB project under its own definitions.
(2) Adopt the risk-unit screen — compute mean cost ÷ R **before** any backtest. (3) Do not pursue
the marketed options implementation on the strength of anything here.
