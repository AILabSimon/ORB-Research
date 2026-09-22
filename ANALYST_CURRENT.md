# ANALYST_CURRENT
**22 Sep 2026 · Analyst Agent · CORE-STRATEGY RECONSTRUCTION cycle complete, + addendum cycle 2**
Sections: **CORE STRATEGY — CURRENT** · **CEEWILLI V2.3** · **MAX V2.1 — PENDING** · **V2.0/V2.2 — SUPERSEDED**

**Addendum (22 Sep 2026b, this issue's continuation request):** re-reviewed V1-V12 and
the CeeWilli sources for the hover/consolidation and one-two-punch questions. No
market-data access or Python execution was available in that sandbox, so this is a
source-evidence and mechanisation pass, not new counts — see §13 of the full report for
the two findings (CeeWilli's "rejects it" is already mechanically defined in
`RESEARCH_CURRENT.md` §D.6, narrower than previously stated; Max's "three bar" pattern
gives an event-based, unfitted definition of the hover state) and
`13_CROSS_MARKET/CODE/orb_path_census_v2.py` (new, untested, pending local validation)
for the one-two-punch / event-consolidation code.

---
# CORE STRATEGY RECONSTRUCTION — CURRENT (22 Sep 2026)

Full report: `13_CROSS_MARKET/OUTPUTS/CORE_STRATEGY_RECONSTRUCTION.md` (§§1-12 first
cycle, §13 addendum)
Raw counts: `13_CROSS_MARKET/OUTPUTS/CORE_STRATEGY_COUNT_APPENDIX.txt`
Figures: `13_CROSS_MARKET/OUTPUTS/FIGS/CORE_PATH/`
Code: `orb_path_census.py`, `orb_path_tabulate.py`, `orb_path_basecontrol.py`, `orb_path_figs.py`, `orb_failbreak_figs.py`, `orb_path_census_v2.py` (new, untested — hover/one-two-punch mechanisation)

Counts only. No economics, no thresholds, no optimisation. 2754 NAS100 + 2753 US500 ORB days.

**1. The failed break is the modal outcome.** Of days that break and retrace: failed-break
57-63%, continuation 22-25%, neither 13-19%. Symmetric across both sides and both instruments.

**2. Honest effect size, measured strictly forward from each trigger, vs the unconditional
opposite-reach base rate (NAS100 48.8% / US500 56.0%):**
| trigger | NAS100 | US500 |
|---|---|---|
| CeeWilli E04 — close back inside | 53.6% (+4.8 pp) | 61.0% (+5.0 pp) |
| Max V8 — close inside **then** newer extreme against | 60.3% (+11.5 pp) | 60.8% (+4.8 pp) |
Not the +20-29 pp the conditional tables imply. Stable year-by-year 2016-2026.

**3. Why: the confirmation prints late.** Median distance left to the opposite boundary at the
confirmation bar is **+0.54 W / +0.51 W** — half the box. Where a full box remains the hit rate
falls to 46-59%. Much of the apparent edge is geometry.

**4. Max's midline TP1 contradicts Max's own failed-break trigger.** The midline was already
crossed before the confirmation on **53.8% / 57.6%** of confirmed failed breaks. V8 [18:07]
TP1 is unreachable on more than half the setups it describes. → Research question.

**5. RECORD CORRECTION — Max DOES have a mechanical bias rule.** V5 [10:43]-[11:37]: *"Take the
orb midline. If it's below the orb midline … we are bearish. If we are above the orb midline,
we are bullish."* The standing "no mechanical bias definition exists" note is **retired.**

**6. Candidate discriminators — all flat.** ORB width (57.6/57.7/60.0/57.6% failed-break by
quartile); minutes held outside before invalidating (70.3/74.1/65.4/72.1/62.1% opposite-reach —
flat, a direct negative against the obvious reading of V4 [05:37] "it needs to hold outside of
it"); **external FVG on the far side — NULL on both instruments** (69.7% vs 73.0%; 77.3% vs 77.4%).
FVG is not the continuation/failure discriminator.

**7. The one live lead: consolidation → failure ~17:1.** 10-bar consolidation after the retrace
resolved failed-break 441 vs continuation 27 (NAS100), 482 vs 22 (US500). Window length is a free
parameter; three values reported, none chosen. Next cycle.

**8. Continuation is under-specified in BOTH corpora.** Max "it needs to hold outside of it" has
no duration anywhere in V1-V12; CeeWilli E02 "rejects it" is undefined in Entry 02. **No
confirmation was invented.** Blocking screenshots: **D1** (CeeWilli marking an E02 rejection
candle) and **D4** (Max marking a break he *rejected* for not holding outside — a negative
example; positive ones cannot resolve it). Full list in §10 of the report.

**9. Analyst limits.** No video files, PDFs or CeeWilli C1-C4 transcripts exist locally. V1-V12
are the Research Agent's evidence extracts, not full transcripts. **Fresh video review remains
Research Agent work.** CeeWilli's reconstruction rests entirely on the playbook audit.

---
# CEEWILLI V2.3 — CURRENT (executed)

## Run
`run_v23_cycle.py` on the Mac, canonical store via `mdload`. Supplied self-tests: **26/26 PASS**
before and after my fixes. 16 cells per instrument = {1m,5m} × {HOLD,DEEP} × {BE off,on} ×
{DRAW-NQ, DRAW-SQ}, NAS100 + US500. **Neither draw arm is selected** (§D.11.3, H29).

## Headline economics — gross first, full unselected population
| instrument | arm | gross range (16 cells) | best cell | net range |
|---|---|---|---|---|
| NAS100 | DRAW-NQ | −0.0454 → **+0.0291** | 1m DEEP BE0 | −0.550 → −0.271 |
| NAS100 | DRAW-SQ | −0.0615 → **+0.0244** | 1m DEEP BE0 | −0.548 → −0.267 |
| US500 | DRAW-NQ | −0.1032 → −0.0261 | 1m HOLD BE1 | −0.805 → −0.425 |
| US500 | DRAW-SQ | −0.0939 → −0.0139 | 1m HOLD BE1 | −0.797 → −0.418 |

Every cell's 95% interval spans zero. NAS100 mildly positive gross, US500 mildly negative — **the
two instruments still disagree in sign.** Net is deeply negative throughout (cost/R 0.27–0.53).
The v2.3 gate is doing its job: `available_RR ≥ 2` on **100%** of accepted trades, no-target
bucket empty, median accepted RR 2.30. Full 16-cell table: `OUTPUTS/CW_ENTRY02_V23_ECONOMICS.md`.

## External-FVG diagnostic — the substantive result
Measured on **10,288 unique (instrument, timeframe, date, side) break events**, de-duplicated
across the 16 overlapping cells so no event is counted twice.

**1. Entry-02 win/loss: NO EFFECT.** FVG touch does not predict whether the Entry-02 trade wins.
| cell | win \| touched | win \| not touched | diff | p |
|---|---|---|---|---|
| NAS100 NQ 1m DEEP BE0 | 222/1164 = 0.191 | 86/488 = 0.176 | +0.015 | 0.490 |
| NAS100 SQ 1m DEEP BE0 | 194/1164 = 0.167 | 70/488 = 0.143 | +0.023 | 0.240 |
| US500 NQ 1m DEEP BE0 | 227/1323 = 0.172 | 56/385 = 0.145 | +0.026 | 0.225 |
| US500 SQ 1m DEEP BE0 | 195/1323 = 0.147 | 49/385 = 0.127 | +0.020 | 0.321 |

**2. FVG touch → opposite ORB reached: SMALL, REAL, AND CONSISTENT.** Ordering enforced
(opposite touch must follow the FVG touch; 99.1% of cases were already correctly ordered).
| cut | P(opp \| touched) | P(opp \| not touched) | diff | p |
|---|---|---|---|---|
| **POOLED** | 3183/6066 = **0.525** | 2013/4222 = **0.477** | **+0.048 ± 0.020** | **<0.0001** |
| NAS100 | 0.496 | 0.445 | +0.051 | 0.0003 |
| US500 | 0.548 | 0.517 | +0.032 | 0.0276 |
| 1m | 0.540 | 0.494 | +0.046 | 0.0006 |
| 5m | 0.501 | 0.458 | +0.043 | 0.0045 |
| LONG (ORH break) | 0.508 | 0.458 | +0.050 | 0.0003 |
| SHORT (ORL break) | 0.541 | 0.500 | +0.041 | 0.0052 |

Same sign and similar size in **every** cut. The dominant path is literally the hypothesised one:
`break > fvg_touch > return_inside > opposite_touch` — 3,082 of 3,211 touched-and-reversed events.

**3. FVG formation:** **91.3% pre-ORB**, 5.7% post-ORB, 2.9% during the 09:30–09:45 ORB.

**4. Timing — the practical caveat.** Median **74 minutes** from FVG touch to the opposite ORB;
only 24% inside 30 minutes, 45% inside an hour, 33.5% take over two hours. This is a slow
session-scale drift, not a sharp reversal, and that bears directly on whether it is tradeable.

**5. Trend/bias: not tested.** v2.3 §D.3/U-24 gives no mechanical definition of CeeWilli's
pre-open bias. The FVG effect above is therefore measured **independently of trend**, and the
interaction is left **unresolved**. No proxy was invented.

## 5-minute alignment — VERIFIED
Previously flagged as unverified. Checked directly: every 5m bar starts on a multiple of 5
(labels 570/575/580/585 = 09:30/09:35/09:40/09:45), 09:30–09:45 is **exactly 3 bars** on every day
sampled, and the ORB computed from 5m bars is **identical** to the 1m ORB. **5m results are valid.**

## Visual validation — SUPPORTS the detected pattern
Five scenario panels rendered and reviewed. The detected structures are genuine external FVGs
sitting immediately beyond the broken boundary, and the break → tap → return-inside → opposite-ORB
sequence is clearly visible (e.g. NAS100 2016-01-07: ORH 4371.99 broken 10:27, FVG 4372.0–4374.8
tapped 10:28, ORL 4338.86 reached 13:12 and carried on to 4320).

## Material defects found and fixed (all genuine implementation bugs; no strategy rule changed)
1. **Silent total failure in the FVG diagnostic.** `_bars_for_day` matched a tz-naive `date`
   against a tz-aware `day` column → **zero rows for every trade**. `annotate()` skipped the whole
   population, so the diagnostic would have reported a **false null** ("no FVG touches anywhere").
   The supplied self-tests passed both before and after this fix — they use synthetic data and do
   not cover the timezone path. **That is a real coverage gap in the test suite.**
2. Same tz defect in `cw_fvg_figs.build_pack` → empty panels.
3. Empty-resample crash on weekend/holiday sessions (CFD feed carries post-16:00 Sunday bars);
   guarded in `cw_entry02.resample` and `_bars_for_day`.
4. **Figure window truncation:** panels used a fixed break+60 bars and frequently ended *before*
   the opposite-ORB touch they were meant to evidence. Window now extends to cover all marked
   events. Without this the visual review would have falsely contradicted correct data.
5. Added a resume guard to `run_cells` (reuses completed deterministic cells) so the cycle
   completes inside a bounded shell. No rule affected.
6. Stale "PENDING LOCAL EXECUTION" headers in both OUTPUTS reports corrected.

## Unresolved
- DRAW-NQ vs DRAW-SQ remains a representation-uncertainty pair; neither selected.
- Trend/bias interaction (U-24) — no mechanical source definition exists.
- Cost remains decisive: every cell's gross is smaller than its own cost/R on CFD proxies.
  Native NQ/ES 1m history is still ~21 sessions, so futures economics remain untestable.

## Recommended next action
The FVG-touch → opposite-ORB effect is **materially recurrent** (+4.8pp, p<0.0001, stable across
instrument, timeframe and direction). Per the issue's own instruction this is **evidence supporting
a separate reconstruction of CeeWilli Entry 04 / failed-break reversal** in a later cycle. It is
*not* implemented here and must not be bolted onto Entry 02. The 74-minute median lag is the first
thing that reconstruction has to confront.

---
# MAX V2.1 — PENDING SEPARATE CYCLE
Unchanged, not run this cycle. RETEST S1 n=1,355, gross +0.1871 [+0.015, +0.361], net −0.238 —
with the standing caveat that the top 1% of trades is 100% of total R and removing the best 10
trades takes gross to +0.0330R.

---
# V2.0 / V2.2 — SUPERSEDED REPRESENTATION
Diagnostic history only: +0.0528R pooled gross; the 31.8% no-target population; the strict-nearest
draw rule (withdrawn in v2.3); the unfloored MAX stop-A failure.
