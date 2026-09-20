# EXPERIMENT REGISTER

## EXP-001 — CENSUS-01 primary
- **Date** 2026-09-12 · **Candidate** MC-1 / F1 (pre-construction behavioural census)
- **Hypothesis** A 15-minute close outside the 09:30–09:45 ET opening range is followed by
  directionally asymmetric movement favouring continuation.
- **Reason** Research Agent handoff §10; mandate §12. Settles U-01 before anything is built.
- **Control** CTRL-B (opposite-direction excursion, same entry, same R) + CTRL-A (EXP-002).
- **Comparison** Coherent: all horizons, both stop readings of U-03, all targets 1R/2R/3R at once.
- **Data** NAS100 1m BID Dukascopy CFD (**proxy**), 2013-08→2026-08, 3,308 sessions, 3,283 signals.
- **Costs** Not applied in the census; applied in EXP-005.
- **Primary metrics** P(MFE>MAE) by horizon; race to 1R/2R/3R vs ORB-edge stop; R_pts distribution.
- **Result** P(MFE>MAE) 50.3–51.9% at every horizon. Gross E flat at +0.069/+0.072/+0.073R for
  1R/2R/3R. Median R only 7.99 pts; 29.4% of signals have R below a CFD round trip.
- **Interpretation** No directional information in the event. The flat-across-targets profile is
  the martingale signature, which excludes "the exit destroyed the payoff" as an explanation.
- **Classification** **FALSIFIED** (no behavioural effect) for the taught 15m-close entry.
- **Decision** Do not construct MC-1 on the 15-minute-close entry.
- **Next** EXP-006 — the pending-order entry at the ORB edge (C-01), which has different geometry.
- **Related request** RR-002.

## EXP-002 — CTRL-A pseudo-range control
- **Date** 2026-09-12 · Identical machinery, range = the 11:00–11:15 ET candle.
- **Question** Is the *opening* range special, or would any 15-minute range do?
- **Result** Real ORB gross +0.072R vs pseudo +0.006R. Difference +0.063R, 95% CI [−0.030, +0.166].
- **Interpretation** The opening range plausibly carries marginally more information than an
  arbitrary intraday range, but the margin is not significant and is far below cost.
- **Classification** **PROVISIONALLY SUPPORTED, ECONOMICALLY IRRELEVANT.**

## EXP-003 — Cross-instrument replication, US500
- **Date** 2026-09-12 · Same census on US500 (proxy for ES/MES/SPX), 3,285 signals.
- **Result** P(MFE>MAE) 49.7–51.3%. Gross E flat +0.056/+0.067/+0.098R at 1R/2R/3R. Net −0.192R.
- **Classification** **FALSIFIED — replicates EXP-001.** Not instrument-specific.

## EXP-004 — CL-012 conditioner (filter F-d), "ORB works best on large move mornings"
- **Date** 2026-09-12 · ORB width ÷ lagged 20-session median width, quintiles.
- **Result** Widest quintile is the **worst** (P(MFE>MAE) 48.2%, net −0.182R). No monotone structure.
- **Classification** **FALSIFIED** on this proxy. Max's own stated conditioner does not hold.
- **Note** This was the single highest-value filter hypothesis in the evidence pack.

## EXP-005 — Cost sensitivity and bootstrap CIs
- **Date** 2026-09-12 · Five execution scenarios from MNQ-tight (1.00 pt round trip) to
  retail/FTMO CFD (6.00 pts), applied per trade as cost ÷ R_pts.
- **Result** All-signal population negative under every scenario. R≥7 pts: net −0.032R at
  realistic MNQ cost. R≥15 pts: net +0.073R — but see EXP-005b.
- **Classification** **COST-DESTROYED** at the taught entry; the effect is smaller than execution.

## EXP-005b — Is the R≥15pt screen real?
- **Date** 2026-09-12 · Four tests: monotonicity by decile, dev/holdout split, per-year stability,
  replication on CTRL-A.
- **Result** Fails monotonicity (decile gross E has no structure; decile 7 is −0.071R), fails the
  holdout CI test (2022–2026 gross +0.099R, CI [−0.007, +0.206]), fails per-year stability
  (+0.188 / −0.111 / +0.171 / +0.035 / −0.004). Passes only the control test (−0.045R on pseudo).
- **Classification** **SAMPLE-LIMITED / PROVISIONAL.** Not advanced. Also an Analyst construct
  with no source support that contradicts the source's own preference for tight entries.

## EXP-006 — CENSUS-02, MC-2 / F4a failed-breakout reversal
- **Date** 2026-09-12 · 2,250 events measured **from the return-inside 15m close**.
- **Hypothesis** A return inside the range after a qualifying break predicts travel to the
  midline (R-016) and opposite edge (R-017).
- **Result** P(MFE>MAE) 49.6–52.9%. Midline is a median 0.32R away, opposite edge 0.87R; only
  **12.0%** of events have an opposite edge ≥2R distant. TP2: hit 47.6%, gross +0.042R,
  net −0.055R; holdout gross **negative**.
- **Interpretation** The source-supported targets sit closer than the source-implied stop. The
  mandate's ≥2R requirement is unreachable by construction, independent of the sample.
- **Classification** **FALSIFIED (geometric), and cost-destroyed.**
- **Decision** MC-2 **RETIRED** as a standalone candidate against this mandate.

## EXP-007 — C-03 holding-period resolution
- **Date** 2026-09-12 · Derived from EXP-001 path data.
- **Result** 180 min captures 76% of EOD MFE; median 38 min to first 2R; P(MFE≥2R) 53.5% at
  180 min vs 62.8% at EOD.
- **Classification** **VALIDATED.** The 180-minute mandate cap is not the binding constraint and
  C-03 need not be resolved from source.

---
# CYCLE 2 — after RR-002

## EXP-004R — RE-LABEL of EXP-004 (accepting Researcher Challenge RC-001)
- **Date** 2026-09-12 · **Arithmetic unchanged.** What the result is *about* is changed.
- RC-001 is **ACCEPTED**. Max's own usage of "larger than expected move" attaches it to
  **compression** — six 15-minute candles held inside the range, i.e. a *narrow* early range —
  not to a wide opening range (V12 20:10, 28:55, 38:11; V3 01:26).
- **Corrected classification:** EXP-004 **falsifies opening-range width as a filter** (an Analyst
  hypothesis). It is **not** a test of CL-012 and the cycle-1 "CL-012 FALSIFIED" verdict was wrong.
- Note: the finding that the widest quintile is worst is **consistent with** Max's framework, not
  contradictory to it. Cycle 1 over-claimed. Corrected in DECISION_LOG D-005R.
- The real test of CL-012 is EXP-008-G4 and EXP-009 below.

## EXP-008 — MC-7 source-faithful boundary entry
- **Date** 2026-09-12 · **Candidate** MC-7 / F2 · Data NAS100 1m **proxy**, 2013–2026.
- **Pre-registered version was CONTRADICTED by RR-002 and was never run** — see D-009. Rebuilt to
  the corrected MC-7 spec: entry = print-through (P-2/R-009) after the boundary trades, filled at
  the prior candle's extreme + 0.5 pt slippage (manual market, R-038); initial stop = beyond that
  candle's opposite extreme (R-040); exit = close back inside the ORB (R-045/R-041) or 180 min.
  All four components SOURCE SUPPORTED AND REPEATED.
- **SOURCE-FIDELITY CHECK (passed).** Max states live stops of 6–17 NQ points, mode ≈9–10.
  The representation produces **median R = 9.3 points**. The representation is faithful; this is
  the first time in the project that a reconstruction has been validated against the source's own
  stated numbers.

| Arm | n | /yr | med R | win | gross E | **net E (MNQ 1.75)** | 95% CI |
|---|---|---|---|---|---|---|---|
| A1 source-faithful, 1m close invalidation | 3,896 | 312 | 9.3 | 10.6% | +0.019R | **−0.271R** | [−0.359, −0.177] |
| A2 first trade only | 3,052 | 244 | 9.6 | 10.8% | −0.002R | −0.283R | — |
| A3 bracket reversal leg (P-1/R-036) | 844 | 68 | 8.5 | 9.8% | +0.096R | −0.226R | [−0.466, +0.050] |
| A4 invalidation on 15m close | 3,182 | 255 | 9.4 | 14.8% | −0.011R | −0.295R | [−0.391, −0.196] |
| A5 + 2R target (**Analyst construct — NOT FOUND**) | 3,802 | 304 | 9.3 | 23.8% | −0.065R | −0.355R | — |
| A6 A1 at Dukascopy CFD cost 3.42 | 3,896 | 312 | 9.3 | 10.6% | +0.019R | −0.547R | — |
| **A7 zero slippage, ZERO cost (impossible upper bound)** | 3,895 | 312 | 8.8 | 10.6% | **+0.110R** | +0.110R | [+0.008, +0.220] |

- **Source-supported gates (RR-002 §4), none rescues it:**
  G-1 cross-instrument confirmation (P-4/R-042), NAS100 gated on US500 beyond its own ORB:
  confirmed n=2,602 gross +0.043R **net −0.230R**; unconfirmed gross −0.030R. The gate is
  directionally real and economically insufficient.
  G-4 compression N=4/6/7 (P-6): gross −0.019 / **−0.120** / −0.135R; net −0.435 / −0.575 / −0.566R.
  5-minute ORB 09:30–09:35 (C-10/R-044): n=4,127, gross +0.030R, net −0.236R.
  G-1+G-4 combined: n=173, net −0.423R.
  G-3 news veto: **NOT TESTABLE** — the shared news calendar covers 13 rows of recent days only.
- **Profile:** avg win +6.15R, avg loss −0.71R, win rate 10.6%, **median hold 3 minutes**, exit mix
  55.1% invalidation / 34.0% stop / 10.2% time. A lottery-ticket distribution with gross E ≈ 0.
  The 3-minute median hold corroborates Max's own live experience of being repeatedly "edged out".
- **Classification** **COST-DESTROYED** on the NAS100 index-CFD proxy, against a verified-faithful
  representation. Cost figures in this entry are SUPERSEDED by `09_VALIDATION/COSTS/COST_RECONCILIATION.md`
  (corrected: raw gross +0.1100R, S2 realistic cost 1.335 pts = $2.67, breakeven +0.2806R, net −0.1707R).
- **Decision** MC-7 not advanced. F2 closed.

## EXP-008B — the structural cost arithmetic (the decisive result)
- **SUPERSEDED — see `09_VALIDATION/COSTS/COST_RECONCILIATION.md`.** The percentages quoted here
  were the MEDIAN per-trade cost ratio; the breakeven requirement is the MEAN (expectancy is a
  mean). Corrected: S2 realistic cost 1.335 pts = $2.67 round trip, mean cost/R = **0.2806R**
  (median 0.150R), raw gross +0.1100R, net −0.1707R, shortfall **2.55×**.
- Corrected: breakeven **+0.2806R** (mean cost ratio at S2) vs raw gross **+0.1100R** → **2.55×**.
  New and stronger: raw gross **declines** with tradability — +0.110R all trades, +0.063R at
  R≥5pts, +0.031R at R≥10pts, **−0.034R at R≥20pts**.
- Breakeven stop distance: at +0.02R gross, R must exceed **88 points**; at +0.11R gross, **16
  points**. Max's own stated stop is 6–17 points.
- **Classification** **VALIDATED.** This is structural, not statistical, and no source detail,
  filter or sample can alter it.

## EXP-009 — P-6 second branch: the falsifiable ±15-point claim (V12 28:55)
- **Date** 2026-09-12 · Post-11:15 excursion beyond the nearer ORB edge, compression vs all others.

| | n | median max excursion | p75 | p90 | stays within 15 pts **each** side |
|---|---|---|---|---|---|
| Compression (6 candles inside) | 288 | **27.0 pts** | 71.3 | 133.2 | **36.1%** |
| All other days | 3,031 | 58.7 pts | 133.0 | 223.5 | 14.9% |

- **Interpretation** Compression **is** informative — a real 2.4× effect on containment — but it
  predicts a **quieter** rest of day, **not** a larger move. Branch (a) of R-020/P-6 ("larger than
  expected move") is **FALSIFIED**; branch (b) ("stays within about 15 points each side") is
  directionally supported but 36.1% does not support the word "usually".
- This explains EXP-008-G4 coherently: gating a breakout on compression makes it worse because
  compression predicts containment.
- **Classification** **VALIDATED behavioural finding; the tradable branch of the claim FALSIFIED.**
- **Note** This is the correct test of CL-012 that RC-001 asked for. CL-012 is now properly tested
  and does not hold in its tradable form.

## EXP-010 — MC-3 / F5 inside-range fade under the compression gate
- **Date** 2026-09-12 · Raised by EXP-009, not by preference: if compression predicts containment,
  the **fade** (R-021) is the behaviourally indicated action, not the break (C-11).
- Entry limit at the ORB boundary on touch; stop operationalised from the source's own quantified
  band (±15 pts, V12 28:55) and from 0.25×width; targets midline (R-016) and opposite edge (R-017).

| Target | Stop | n | /yr | target distance | win | gross E | **net E** | 95% CI |
|---|---|---|---|---|---|---|---|---|
| midline | 15 pts | 499 | 40 | 1.36R | 32.7% | −0.269R | −0.386R | [−0.480, −0.284] |
| midline | 0.25×w | 514 | 41 | 2.03R | 24.7% | −0.306R | −0.568R | [−0.681, −0.458] |
| opposite edge | 15 pts | 496 | 40 | 2.73R | 25.0% | −0.327R | −0.443R | [−0.559, −0.325] |
| opposite edge | 0.25×w | 513 | 41 | 4.03R | 17.2% | −0.419R | −0.680R | [−0.799, −0.554] |

- Holdout 2022–2026 net −0.739R, worse than development. P(MFE≥2R) = 10.3%.
- **Classification** **FALSIFIED** on all four arms, gross as well as net. The containment effect
  of EXP-009 is real at the day level but does not survive contact with a boundary-fade entry:
  64% of compression days still exceed 15 points on at least one side.
- **Decision** F5 **RETIRED**. C-11 is resolved empirically — neither branch of the contradiction
  is tradable, so the contradiction no longer needs resolving from source.

## EXP-011 — does the cycle-1 R≥15pt screen replicate on the faithful representation?
- Applied to EXP-008 A1: n=1,309, **gross −0.048R**, net −0.121R.
- **Classification** **DOES NOT REPLICATE.** D-007 confirmed; the screen was noise. Retired.

---
# CYCLE 3 — CONTROLLED CLOSEOUT

## EXP-012 — Cost arithmetic audit
- **Date** 2026-09-12 · `12_CODE/cost_audit.py` · Full detail: `09_VALIDATION/COSTS/COST_RECONCILIATION.md`
- **Two errors found and corrected.** (1) "18.8%" and "+0.290R" were the **median** and the **mean**
  of the same per-trade cost ratio; expectancy is a mean, so only the mean is a breakeven
  requirement. (2) EXP-008 carried 0.5 pt of entry slippage **inside the fill**, so adding a 1.75 pt
  round trip double-counted it. Both corrected by recomputing raw gross at zero slippage and
  applying every component once, from an explicit MNQ dollar build-up.
- **Corrected:** MNQ $2.00/pt, tick 0.25 pt = $0.50; S2 realistic = $0.50/side commission + 0.50 pt
  entry slip + 0.25 pt exit slip + 0.25 pt stop extra = **1.335 pts avg = $2.67** round trip.
  Median risk 8.81 pts = **$17.62**. Mean cost/R = **0.2806R** (median 0.150R).
  Raw gross **+0.1100R**. Net **−0.1707R**. Shortfall **2.55×**. Negative in all five scenarios
  including the optimistic one (−0.0649R).
- **New and stronger finding:** raw gross **falls monotonically as trades become tradable** —
  +0.110R (all) → +0.063R (R≥5) → +0.031R (R≥10) → **−0.034R (R≥20)**. The apparent edge lives
  where it cannot be executed. Independent of any cost assumption.
- **Uncertainty on +0.1100R:** n=3,895; bootstrap CI [+0.0097, +0.2194]; dev +0.1491R vs
  **holdout +0.0394R, CI [−0.0941, +0.1819] — includes zero**; per-year −0.243R to +0.522R with
  2016–17 carrying the sample; US500 +0.1399R but median R 2.00 pts → net −0.9291R; optimistic
  same-bar resolution +0.0710R, **CI includes zero**; **0.25 pt of entry slippage removes
  significance** (+0.0762R, CI includes zero), 1.00 pt turns it negative.
- **Classification** **VALIDATED.** The economic gap is real and is not a reporting artefact.

## EXP-013 — Track B FX census, pre-registered anchors
- **Date** 2026-09-12 · `12_CODE/trackb_fx.py` · EURUSD + GBPUSD 1m BID, 2014-06 → 2026-08.
- **Anchors pre-registered, not searched:** London **08:00 Europe/London** (= the MC-6 03:00 ET
  anchor) with a single alternative at 07:00; New York **09:30 America/New_York**. Three anchors
  total, no optimisation across times.
- **DST verified:** London-minus-New-York wall-clock offsets observed are 300 min (4,242,841 bars)
  and **240 min (301,626 bars)** — the misaligned weeks are present and are handled by tz-aware
  conversion, not by a fixed UTC offset.
- No indicators, no bias, no VWAP/EMA/FVG, no day-of-week or news filters, no volatility screens.

| Series | n (close) | P(MFE>MAE) 60m | 180m | EOD | n (print-through) | PT P(MFE>MAE) |
|---|---|---|---|---|---|---|
| EURUSD LON0800 | 3,161 | 50.9% | 51.5% | 50.6% | 5,598 | 49.5% |
| EURUSD LON0700 | 3,155 | 49.3% | 49.7% | 50.5% | 5,697 | 47.7% |
| EURUSD NY0930 | 3,147 | 50.3% | 51.2% | 50.8% | 5,624 | 46.6% |
| GBPUSD LON0800 | 3,157 | 50.4% | 50.7% | 50.3% | 5,635 | 47.6% |
| GBPUSD LON0700 | 3,153 | 50.8% | 49.2% | 49.2% | 5,664 | 47.0% |
| GBPUSD NY0930 | 3,147 | 49.3% | 49.5% | 49.2% | 5,621 | 43.9% |

- **Q1** The print-through carries **no positive** continuation information in FX — 43.9%–49.5%,
  i.e. below 50% in all six series.
- **Q2** The completed close is **nearer neutral** (49.2%–51.5%) than the print-through. In FX the
  print-through **destroys** information rather than adding it — the opposite of its role in the
  source material.
- **Q7** London and New York are **not structurally different** in tradability. NY shows slightly
  lower print-through P(MFE>MAE) and materially smaller excursions; neither is exploitable.
- **Q6** EURUSD and GBPUSD are **consistent** — same sign, same magnitude, on every measure.

## EXP-014 — Track B geometry and reversal (Q3, Q4)

| Series | close-entry med R | P(MFE₁₈₀ ≥ 2R) | returned inside | dist to opposite edge | share ≥2R away |
|---|---|---|---|---|---|
| EURUSD LON0800 | 3.10 pip | 66.7% | 90.0% | 4.59R | 92.7% |
| EURUSD NY0930 | 3.80 pip | 64.7% | 82.4% | 4.24R | 89.9% |
| GBPUSD LON0800 | 4.00 pip | 69.9% | 90.6% | 4.75R | 92.9% |
| GBPUSD NY0930 | 4.70 pip | 65.9% | 83.9% | 4.35R | 90.7% |

- **Q4 — YES, the geometry permits ≥2R in FX**, and this is the one structural respect in which FX
  differs from Track A. The opposite ORB edge sits a median **4.1–4.8R** away (Track A: 0.87R), so
  MC-2's geometric kill does **not** apply in FX, and P(MFE ≥ 2R) is 65–70% within 180 minutes.
- **Q3** A return inside occurs on 82–91% of signals — so common that it is close to
  non-informative. Combined with P(MFE>MAE) ≈ 50%, it carries no usable reversal information.

## EXP-015 — Track B costed economics (Q8) — the closing result
Cost model, round trip: EURUSD **1.5 pip** (0.5 measured p90 spread + 0.3 slip + 0.7 commission);
GBPUSD **2.4 pip** (1.2 + 0.5 + 0.7). Commission ≈ $7/lot round turn, FTMO-style.

| Series | n | /yr | med R | mean cost/R | raw gross | **NET** | 95% CI on net |
|---|---|---|---|---|---|---|---|
| EURUSD LON0800 | 5,598 | 459 | 2.20 pip | 0.845 | +0.117R | **−0.728R** | [−0.833, −0.615] |
| EURUSD LON0700 | 5,697 | 467 | 1.90 pip | 1.005 | +0.025R | −0.980R | [−1.082, −0.877] |
| EURUSD NY0930 | 5,624 | 461 | 2.70 pip | 0.716 | +0.078R | −0.639R | [−0.741, −0.536] |
| GBPUSD LON0800 | 5,635 | 462 | 3.10 pip | 1.012 | +0.091R | −0.921R | [−1.027, −0.811] |
| GBPUSD LON0700 | 5,664 | 464 | 2.60 pip | 1.244 | +0.194R | −1.050R | [−1.174, −0.916] |
| GBPUSD NY0930 | 5,621 | 461 | 3.60 pip | 0.858 | +0.061R | −0.797R | [−0.891, −0.691] |

- **The FX failure mode is worse than Track A's and is purely economic.** The source-faithful stop
  is 1.9–3.6 pips, so a realistic round trip is **72%–124% of the entire risk unit**. Net is
  −0.64R to −1.05R with confidence intervals nowhere near zero.
- **Classification** **COST-DESTROYED — decisive.** Track B closes under stopping rules (a), (c)
  and partially (b).

## EXP-016 — Q5: does compression → containment replicate in FX? **YES**
Same measure as EXP-009: six 15-minute candles with no close outside the range, then excursion
beyond the nearer edge for the remainder of the session.

| Series | n compression | excursion ratio (comp ÷ other) | permutation p | dev ≤2020 | holdout ≥2021 | contained ≤0.5×width |
|---|---|---|---|---|---|---|
| EURUSD LON0800 | 223 | 0.83 | 0.0000 | 0.85 | 0.75 | 2.2% vs 0.3% |
| EURUSD NY0930 | 126 | **0.68** | 0.0000 | 0.66 | 0.67 | **24.6% vs 3.7%** |
| GBPUSD LON0800 | 189 | 0.89 | 0.0065 | 0.90 | 0.77 | 4.8% vs 0.4% |
| GBPUSD NY0930 | 110 | **0.56** | 0.0000 | 0.73 | 0.48 | **27.3% vs 4.4%** |
| *NAS100 NY0930 (Track A)* | *288* | *0.46* | — | — | — | *36.1% vs 14.9% (±15 pts)* |

- Replicates in **both pairs**, at **both anchors**, in **development and holdout**, in a different
  asset class. Strongest at the **09:30 New York** anchor — Max's own session — in both pairs.
- **Classification** **REPLICATED IN FX.** Recorded as a candidate hypothesis for the existing ORB
  project. **Not implemented there in this cycle**, per instruction.
- It remains a **day-state** observation, not a strategy: EXP-010 showed the corresponding fade
  construction fails on the proxy, and no fade was built in FX because the Track B cost arithmetic
  (cost 72%–124% of the risk unit) forecloses any boundary construction.
