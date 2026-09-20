# ANALYST DECISION REPORT — Max Options Trading ORB
### Senior quantitative review · final · 2026-09-12

Supersedes all earlier versions. Three Analyst cycles, two Research Agent cycles, twelve source
videos, two tracks, ~13 years of 1-minute data across four instruments.

---

## 1. EXECUTIVE DECISION

**Close the project. No candidate advances to construction, validation or implementation.**
The existing FX ORB V1 control (+0.049R) is **not** replaced; nothing here improves on it.

Both tracks fail, and they fail for the same structural reason rather than for a statistical one:
**the source's own risk unit is too small to carry its own execution costs.** Max's stated stop is
6–17 NQ points; the faithful reconstruction produces a median of 9.3. Against a $17.62 median risk
per MNQ contract, a realistic $2.67 round trip requires a gross edge of +0.2806R. The best-case
measured gross edge is +0.1100R — and that figure is not itself robust.

In FX the same arithmetic is worse: a 1.9–3.6 pip stop against a 1.5–2.4 pip round trip means
execution costs consume **72%–124% of the entire risk unit**.

No filter, session, instrument, sample or source clarification changes this.

---

## 2. TRACK A EVIDENCE

**Behavioural.** Across 3,283 qualifying events, the probability that favourable excursion exceeds
adverse excursion from the taught entry is **50.3%–51.9% at every horizon** (5m → EOD), in both
directions, in every year, on two instruments. Gross expectancy is flat across 1R/2R/3R targets
(+0.069 / +0.072 / +0.073R) — the martingale signature, which excludes "the exit destroyed the
payoff" as an explanation.

**Corroborated from the source side.** The Research Agent's confirmed negative — no prospective
continuation-versus-reversal *selector* exists in twelve videos, and the source forecloses the
question himself (*"There's no correct answer"*, V12 37:09) — is an independent line of evidence
reaching the same conclusion. Two methods, one answer. **U-01 is closed.**

**The strongest single result** is not statistical. Raw gross expectancy **declines monotonically
as trades become tradable**: +0.110R over all trades, +0.063R at R≥5 pts, +0.031R at R≥10 pts,
**−0.034R at R≥20 pts**. The apparent edge lives precisely where it cannot be executed. This holds
under any cost assumption, including none.

---

## 3. CORRECTED COST RECONCILIATION

Full detail: `09_VALIDATION/COSTS/COST_RECONCILIATION.md`. **Two errors were found and corrected.**

1. **"18.8%" and "+0.290R" were the median and the mean of the same per-trade cost ratio.**
   Expectancy is a mean, so only the mean is a breakeven requirement. The mean exceeds the median
   because 13.5% of trades have R < 3 points, where cost ÷ R explodes (p99 = 1.309 — cost exceeds
   the whole risk unit).
2. **Entry slippage was double-counted.** EXP-008 filled at trigger ± 0.5 pt *inside the fill*, so
   adding a further 1.75 pt round trip charged part of it twice.

### MNQ specification and cost build-up

| | |
|---|---|
| Point value | $2.00 / index point / contract |
| Tick size | 0.25 index points |
| Tick value | $0.50 |

| Scenario | Comm/side | Comm RT | Entry slip | Exit slip | Stop extra | Avg RT (weighted) |
|---|---|---|---|---|---|---|
| S1 optimistic | $0.35 | $0.70 (0.350 pt) | 0.25 | 0.25 | 0.00 | 0.850 pt = $1.70 |
| **S2 realistic** | $0.50 | $1.00 (0.500 pt) | 0.50 | 0.25 | 0.25 | **1.335 pt = $2.67** |
| S3 poor fill | $0.75 | $1.50 (0.750 pt) | 1.00 | 0.50 | 0.50 | 2.420 pt = $4.84 |
| S4 Dukascopy CFD | — | — | 1.46 | 1.46 | 0.50 | 3.090 pt = $6.18 |
| S5 retail/FTMO | — | — | 3.00 | 2.50 | 0.50 | 5.670 pt = $11.34 |

Exit mix: invalidation 55.1% · stop 34.0% · time 10.1% · EOD 0.7%.

### Reconciliation (n = 3,895; median R = 8.81 pts = **$17.62**)

| | Value |
|---|---|
| Raw gross expectancy (zero slippage, zero commission) | **+0.1100R** |
| Cost expressed in R (S2), **mean** = breakeven requirement | **+0.2806R** |
| Cost expressed in R (S2), median | 0.1504R |
| Net expectancy (S2) | **−0.1707R** |
| Observed ÷ required | **0.39× (shortfall 2.55×)** |
| Net at S1 optimistic | −0.0649R |
| Net at S5 retail/FTMO | −1.0684R |

**The corrected figures are less unfavourable than cycle 2 reported** (net −0.171R, not −0.271R)
and the conclusion is unchanged.

### Uncertainty around +0.1100R

| Test | Result |
|---|---|
| Sample | n = 3,895 trades, 13 years |
| Bootstrap 95% CI | [+0.0097, +0.2194] — barely excludes zero |
| Development 2013–2021 | +0.1491R [+0.0157, +0.3082] |
| **Holdout 2022–2026** | **+0.0394R [−0.0941, +0.1819] — includes zero** |
| Per-year | −0.243R … +0.522R; 2016 (+0.522) and 2017 (+0.507) carry the sample |
| NAS100 | +0.1100R → net −0.1707R |
| US500 | +0.1399R [+0.0403, +0.2453], but median R 2.00 pts → net **−0.9291R** |
| Same-bar ambiguity, optimistic resolution | +0.0710R **[−0.0230, +0.1771] — includes zero** |
| Entry slippage 0.25 / 0.50 / 1.00 pt | +0.0762R (CI includes zero) / +0.0189R / **−0.0595R** |

**One tick of entry slippage removes significance** — on an entry the source himself describes
filling badly. The +0.1100R figure requires zero slippage, conservative same-bar sequencing, *and*
the inclusion of trades too small to execute. It is not an edge.

---

## 4. SOURCE AND PROXY LIMITATIONS — precise scope

What has been established is this, and no more:

- **The reconstructed Max ORB families, tested on Dukascopy OTC index-CFD proxies (NAS100, US500),
  did not produce a viable costs-adjusted strategy.**
- **The completed-close and print-through boundary representations showed no sufficient economic
  edge.**
- **Several related source-supported constructions were falsified, cost-destroyed, or retired on
  geometry.**
- **Source-native futures (NQ, MNQ, ES) and index/options implementations (SPX, options on any
  underlying) remain UNVALIDATED because suitable data was unavailable.** They have **not** been
  directly falsified.
- **Proxy agreement across two instruments, and a stop geometry that matches the source's own
  stated numbers (median 9.3 pts vs a stated 6–17, mode 9–10), increase confidence — but they do
  not remove the instrument limitation.**

Further: no options data of any kind exists in the shared store, so the options implementation Max
markets is untestable here. **Nothing in this project is evidence for or against it.**

---

## 5. TRACK B FX EVIDENCE

Pre-registered anchors, no optimisation: London **08:00 Europe/London** (= the MC-6 03:00 ET
anchor) with one alternative at 07:00; New York **09:30 America/New_York**. DST verified — both the
300-minute and the 240-minute London-minus-New-York offsets appear in the data (4,242,841 and
301,626 bars), so the misaligned weeks are handled by tz-aware conversion, not an approximation.

| Q | Question | Answer |
|---|---|---|
| **1** | Does the first print-through contain directional continuation information? | **No.** P(MFE>MAE) 43.9%–49.5% — below 50% in all six series. |
| **2** | Does a completed close add or destroy information? | The completed close is **nearer neutral** (49.2%–51.5%). In FX the print-through **destroys** information — the reverse of its role in the source. |
| **3** | Does a return inside contain reversal information? | **No.** It occurs on 82%–91% of signals — so common as to be near non-informative — and P(MFE>MAE) stays ≈50%. |
| **4** | Does source-faithful stop geometry permit ≥2R? | **Yes — and this is where FX differs from Track A.** The opposite edge sits a median **4.1–4.8R** away (Track A: 0.87R) and P(MFE₁₈₀ ≥ 2R) is 65%–70%. MC-2's geometric kill does not apply in FX. |
| **5** | Does six-candle containment predict reduced excursion in FX? | **Yes — it replicates.** See §8. |
| **6** | Consistent across EURUSD and GBPUSD? | **Yes** — same sign and magnitude on every measure. |
| **7** | Are London and New York structurally different? | **Not in tradability.** NY shows slightly lower print-through P(MFE>MAE) and materially smaller excursions; neither is exploitable. |
| **8** | Large enough to survive realistic FX spread and slippage? | **No — decisively.** |

### Q8, the closing number

| Series | n | /yr | med R | mean cost/R | raw gross | **NET** | 95% CI |
|---|---|---|---|---|---|---|---|
| EURUSD LON0800 | 5,598 | 459 | 2.20 pip | 0.845 | +0.117R | **−0.728R** | [−0.833, −0.615] |
| EURUSD LON0700 | 5,697 | 467 | 1.90 pip | 1.005 | +0.025R | −0.980R | [−1.082, −0.877] |
| EURUSD NY0930 | 5,624 | 461 | 2.70 pip | 0.716 | +0.078R | −0.639R | [−0.741, −0.536] |
| GBPUSD LON0800 | 5,635 | 462 | 3.10 pip | 1.012 | +0.091R | −0.921R | [−1.027, −0.811] |
| GBPUSD LON0700 | 5,664 | 464 | 2.60 pip | 1.244 | +0.194R | −1.050R | [−1.174, −0.916] |
| GBPUSD NY0930 | 5,621 | 461 | 3.60 pip | 0.858 | +0.061R | −0.797R | [−0.891, −0.691] |

Cost: EURUSD 1.5 pip (0.5 measured p90 spread + 0.3 slip + 0.7 commission); GBPUSD 2.4 pip
(1.2 + 0.5 + 0.7). **Execution consumes 72%–124% of the entire risk unit.** Track B closes under
stopping rules (a) *continuation and reversal both effectively neutral*, (c) *the effect is smaller
than realistic execution costs*, and partially (b).

**Transferability decision: the Max ORB concept does not transfer to FX.** Not because FX lacks the
2R geometry — it has it — but because the source-faithful stop is a handful of pips.

---

## 6. STRATEGY-FAMILY DISPOSITION

| ID | Family | Disposition |
|---|---|---|
| F1 | 15-minute close-confirmed continuation (MC-1) | **FALSIFIED** on proxies — no behavioural effect |
| F2 | Print-through boundary entry (MC-7) | **COST-DESTROYED** on proxies, against a verified-faithful representation |
| F3 | Break-and-retest | **PARKED** — requires inventing the tolerance the source declines to define (C-09); shares MC-7's small-R geometry, so it cannot escape the cost arithmetic |
| F4a/b | Failed-breakout reversal (MC-2) | **RETIRED on geometry** — targets sit nearer than the stop (mid 0.32R, opposite edge 0.87R; only 12.0% ≥2R) |
| P-1 | OCO bracket, both branches pre-committed | **FALSIFIED** — bracket leg net −0.226R |
| F5 | Inside-range fade (MC-3) | **RETIRED** — four arms negative **gross as well as net**; holdout worse |
| F6 | Delayed afternoon expansion | **FALSIFIED IN PREMISE** — compression predicts containment, not expansion |
| F7 | Pre-ORB | **OUT OF SCOPE** — undisclosed paid content |
| F8 | Non-US-session ORB | **CLOSED via Track B** — tested as the ORB *concept* in FX, cost-destroyed. Never demonstrated by the source, so this is not evidence about his method |
| F9 | Power-hour ORB | **REJECTED** — Research Agent found no evidence it exists |
| — | 5-minute ORB (C-10) | **FALSIFIED** — gross +0.030R, net −0.236R |
| — | MC-4 three-bar pattern | **PARKED** — a candlestick pattern, not an opening-range method |
| G-1 | Cross-instrument confirmation (P-4) | **REAL BUT INSUFFICIENT** — confirmed +0.043R vs unconfirmed −0.030R; net still −0.230R |
| G-4 | Compression gate (the real CL-012) | **FALSIFIED** — gross −0.019 / −0.120 / −0.135R at N=4/6/7 |
| G-3 | News-day veto (P-7) | **NOT TESTABLE** — shared news calendar holds 13 recent rows |

---

## 7. VALIDATED FINDINGS

1. **No prospective continuation-versus-reversal selector exists** — confirmed from the source side
   across twelve videos, and independently corroborated by P(MFE>MAE) ≈ 51% at every horizon on two
   instruments. U-01 closed.
2. **The structural cost arithmetic** (§3), audited and corrected.
3. **The edge is inversely related to tradability** — raw gross +0.110R → +0.063R → +0.031R →
   −0.034R as the risk unit grows. Independent of any cost assumption.
4. **The 180-minute mandate cap is not a binding constraint** — 180 minutes captures 76% of
   end-of-day excursion; median time to 2R is 38 minutes. C-03 resolved by data, not source.
5. **The reconstruction is source-faithful** — median R 9.3 pts against a stated 6–17, mode 9–10.
   The negative result is a property of the method, not of the coding. *This is the project's one
   clean methodological success.*
6. **Data and cost infrastructure validated** — four instruments, BID+ASK, zero duplicate
   timestamps, >99% ORB-window completeness; spread measured rather than assumed and flat across
   the session; DST handled by tz-aware conversion, verified against the misaligned weeks.

---

## 8. PROVISIONAL FINDINGS

**Compression → containment.**
Classification: **PROVISIONALLY VALIDATED ON US INDEX-CFD PROXIES**, with independent replication
in FX recorded separately.

- Six 15-minute candles remain inside the opening range.
- Subsequent excursion is materially smaller — NAS100 median 27.0 vs 58.7 points (ratio 0.46).
- Containment probability increases — within ±15 points, 36.1% vs 14.9%.
- **Breakout expansion is not supported** — branch (a) of R-020 ("a larger than expected move") is
  falsified; gating a breakout on compression makes it worse.
- **The corresponding fade construction also fails** (EXP-010, four arms, negative gross and net).

**FX replication (EXP-016):** ratio < 1 in all four series — EURUSD LON 0.83, EURUSD NY 0.68,
GBPUSD LON 0.89, GBPUSD NY **0.56** — permutation p ≤ 0.0065 throughout, and below 1 in both
development and holdout. Strongest at the **09:30 New York** anchor in both pairs. Containment
within ±0.5×width at the NY anchor: 24.6% vs 3.7% (EURUSD), 27.3% vs 4.4% (GBPUSD).

Its legitimate value is as a **day-state hypothesis**, not a strategy:
> *Prolonged opening-range containment may identify suppressed subsequent range expansion.*

This may be transferred to another project **only after it replicates under that project's own
instrument, session and range definition.**

---

## 9. FALSIFIED REPRESENTATIONS
F1 · F2 · F5 · F6 · P-1 · G-4 · the 5-minute ORB — all on index-CFD proxies, per the scope in §4.
Also: **CL-012 as opening-range width** (an Analyst hypothesis, not the source's claim — see §11),
and **the tradable branch of CL-012 proper** (compression → larger move).

## 10. COST-DESTROYED CONSTRUCTIONS
MC-7 on NAS100 (net −0.171R at S2) and on US500 (net −0.929R). All six Track B FX series
(net −0.639R to −1.050R). G-1-gated MC-7 (net −0.230R). The 5-minute ORB (net −0.236R).

## 11. RETIRED AND PARKED
**Retired:** F1, F2, F4a/b, F5, F6, P-1, the 5-minute ORB, and the cycle-1 **R≥15pt screen**
(EXP-011: gross −0.048R on the faithful representation — it was noise, retired explicitly so it
cannot re-enter renamed).
**Parked:** F3 break-and-retest (with reason, not pending), MC-4 three-bar pattern, G-3 news veto
(untestable on available calendar data).

**Two cycle-1 errors corrected rather than explained around:**
- **D-005R** — cycle 1 recorded "CL-012 FALSIFIED" from a test of opening-range *width*. Researcher
  Challenge RC-001 accepted: width is not CL-012, and the width result was in fact *consistent*
  with the source's framework. CL-012 was then tested properly.
- **D-014** — the cost arithmetic, §3.

## 12. REUSABLE HYPOTHESES
**H-01 — opening-range containment → suppressed subsequent expansion.** §8. The only asset this
project produced. Not implemented anywhere; recorded as a candidate hypothesis for later testing in
the existing ORB project under that project's own definitions.

## 13. COMPARISON WITH THE EXISTING FX ORB CONTROL
Conceptual only — **the results are not pooled and must never be.** The existing V1 uses a
00:00–08:00 range with a 0.10×ATR14 buffer, opposite-side stop and 16:00 exit (≈ +0.049R). The Max
Track B test uses a 15-minute session-opening range, a source-faithful entry-candle stop and a
180-minute cap. They are different objects on a different range, a different risk unit and a
different holding period. The salient structural contrast: **V1's opposite-side stop produces a
risk unit large enough to absorb FX costs; the Max construction's few-pip stop does not.**
Nothing in this project warrants modifying V1.

## 14. SHOULD ANY CANDIDATE ADVANCE?
**No.** See `IMPLEMENTATION_READINESS.md`. Mechanical completeness was achieved and was never the
blocker; the economics are.

## 15. SHOULD THE PROJECT CLOSE?
**Yes.** Both tracks are complete, nine families dispositioned, both open requests incorporated and
the researcher challenge accepted and actioned. The mandate forbids continuing when further work
cannot change the decision. **No further Research Agent work is required.**

The two genuinely open items cannot close a 2.55× gap: the Advanced ORB indicator's logic (paid
subscription, correctly out of scope) and the F3 retest tolerance (the source explicitly declines
to define it, C-09).

## 16. HIGHEST-VALUE ACTION OUTSIDE THIS PROJECT

1. **Test H-01 in the existing ORB project**, under its own 00:00–08:00 range, its own instruments
   and its own session definition. It has now replicated across two asset classes, two FX pairs,
   two session anchors and both development and holdout — which is more cross-validation than
   anything else this project produced. It is a day-state classifier, not a strategy, and its
   plausible use is *sizing or standing aside*, not entries.
2. **Apply the risk-unit screen to any future intraday research.** The generalisable lesson is that
   a strategy whose stop is a handful of points or pips must clear a very high gross-expectancy bar,
   and the bar should be computed — mean cost ÷ R, never median — **before** a backtest is run, not
   after. That single check would have closed this project in a day.
3. **Do not pursue the marketed options implementation on the strength of anything here.** It was
   never tested, no data exists to test it, and this project is evidence neither for nor against it.

---
*What should not happen: adding filters to close a gap between +0.110R and +0.281R. Anything that
appears to bridge it is fitting noise.*
