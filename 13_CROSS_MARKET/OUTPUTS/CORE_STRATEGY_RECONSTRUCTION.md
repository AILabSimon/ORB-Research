# ORB CORE-STRATEGY RECONSTRUCTION
**Analyst Agent · 2026-09-22 · NAS100 + US500, 1-minute, 2016-01-04 → 2026-09-15**

Mandate: pull the research back to `ORB HIGH/LOW → BIAS → BREAK → RETRACE → CONFIRMATION → ENTRY`,
reconstructed separately for MAX, CEEWILLI and COMBINED. Primary question: **after the break and
during/after the retrace, what determines whether price CONTINUES or FAILS and reverses toward the
opposite ORB boundary?** Counts and path counts only. No optimisation, no thresholds, no scoring,
no indicators, no economics.

Data: 2754 NAS100 ORB days, 2753 US500 ORB days. 2750 / 2749 produce a 1-minute close beyond a
boundary. Every state below is defined in the source's own words; nothing is invented.

---

## 0. HEADLINE ANSWER TO THE PRIMARY QUESTION

**The failed break is the modal outcome of an ORB break, not the exception.**
Of days that break and then retrace, 57-63% resolve as a failed break, and only 22-25% as a
continuation. Both sources already say this in words; the counts confirm it on 5 500 instrument-days.

**But the size of the effect is much smaller than the raw hit rate suggests, for one structural
reason: by the time either source's confirmation prints, price has usually already travelled half
the box.** Median distance remaining from the confirmation bar to the opposite boundary is
**+0.54 W (NAS100) / +0.51 W (US500)** — about half an ORB width. Measured strictly forward from
the trigger, against the correct unconditional benchmark:

| | NAS100 | US500 |
|---|---|---|
| unconditional: opposite boundary reached after any break | 48.8% | 56.0% |
| after CeeWilli Entry-04 trigger (close back inside) | 53.6% (**+4.8 pp**) | 61.0% (**+5.0 pp**) |
| after Max V8 trigger (close inside **then** newer extreme against) | 60.3% (**+11.5 pp**) | 60.8% (**+4.8 pp**) |

That is the honest answer. The pattern is real and directionally consistent, it is stable
year-by-year, and it is **worth between +5 and +11 percentage points of forward probability** —
not the +20-29 pp that the naive conditional tables imply.

**What determines continuation vs failure, mechanically, from the sources' own primitives: nothing
yet identified does so in advance.** The two states are distinguished *after the fact* by which
confirmation fires first. Every candidate discriminator tested here — ORB width, how long price
held outside before invalidating, presence of an external FVG on the far side — is flat. See §6.

---

## 1. MAX — RECONSTRUCTED SEQUENCE

| # | Step | Source's own words | Class |
|---|---|---|---|
| 1 | **ORB** | 09:30-09:45, first 15-minute candle, high and low | EXPLICIT |
| 2 | **Midline** | V1 [12:10]-[12:53] arithmetic; V5 [06:52] "the midline is the middle of the 15minute candle, the opening print" | EXPLICIT |
| 3 | **BIAS** | V5 [10:43]-[11:37] "Take the orb midline. If it's below the orb midline — ready for how simple this is — **we are bearish**. If we are above the orb midline, **we are bullish**. If we are below orb … we are downtrending. If we are above orb, we are uptrending. I don't need to know much more than that." | **EXPLICIT AND FULLY MECHANICAL** |
| 4 | **BREAK** | 15-minute closure, then drop to a lower timeframe (V1 [27:18]) | EXPLICIT |
| 5 | **Continuation requirement** | V4 [05:37] "**it needs to hold outside of it**" | EXPLICIT (concept), UNKNOWN (duration) |
| 6 | **RETRACE** | V12 [27:23] "**the retest is always the best way to go** … retest, dog[i] retest, usually could pump to a newer high" | EXPLICIT preference |
| 7 | **CONFIRMATION (continue)** | print-through: V11 [08:34] "I want to see the print through — the next candle's wick hit 308 and then go"; V10 [24:18] "as soon as I see a candle flip up or **print through the previous candle**, I'm going long" | EXPLICIT (concept), mechanisable |
| 8 | **INVALIDATION** | V8 [06:11] "**Once your candle closed inside of orb, then that is not a confirmation for entrance for you**" | **EXPLICIT AND MECHANICAL** |
| 9 | **CONFIRMATION (fail)** | V8 [16:33] "now that we have failed to break to the upside and we have broke back inside of the opening range, I would play a short all the way down to the bottom … **this confirmation, newer low**, I would play a short onto the bottom" | **EXPLICIT AND MECHANICAL** |
| 10 | **Targets** | V8 [18:07] "**You could take profit on the break of the midline** … Real diamond handers, **you ride the top of orb to the bottom of orb**" | EXPLICIT, two-stage |
| 11 | **Exit / trim** | V12 [26:21] "your first trim is **that newer low** — and then any newer low after that would have been a full exit"; V3 [12:24] a lower low after higher lows "is an invalidation of your current analysis, it's time to get out" | EXPLICIT |
| 12 | **Axiom** | V1 [31:47], V2 [34:20], V4 [05:37], V5 [08:34], V8 [16:33] — five independent statements of "**nothing more bearish than a failed bullish move**" | EXPLICIT, repeated |

**Correction to the standing record.** The programme has been carrying "no mechanical bias
definition exists in the Max corpus". That is wrong. V5 [10:43]-[11:37] is a complete,
deterministic, price-vs-midline bias rule. It was in the transcript the whole time.

---

## 2. CEEWILLI — RECONSTRUCTED SEQUENCE

From *The ORB Playbook* (the source's own written specification — stronger evidence than any video).

| # | Step | Source's own words | Class |
|---|---|---|---|
| 1 | **ORB** | 09:30-09:45, "The high of that candle = ORH. The low = ORL." | EXPLICIT (wick-to-wick) |
| 2 | **Midline** | **absent from the document entirely** | UNKNOWN |
| 3 | **BIAS** | "Overall market bias (bullish or bearish)" is on the pre-market checklist — **no method is given anywhere** | **DISCRETIONARY — the single largest gap** |
| 4 | **BREAK** | "Let price break the ORH (bullish) or ORL (bearish). You're not entering here — just watching and **confirming the break is real**." | EXPLICIT that the break is not an entry; "real" **undefined** |
| 5 | **RETRACE** | "Price breaks out and **pulls back to the level it just broke**. … You want to see this happen." | EXPLICIT, **mandatory**. No candle count given anywhere. |
| 6 | **CONFIRMATION (continue)** | "**The critical step.** Price retests the level **and rejects it**. On a bullish setup, **the ORH now acts as support**. That rejection is your entry trigger." | EXPLICIT as a requirement; **"rejects" is not mechanically defined in Entry 02** |
| 7 | **INVALIDATION** | Entry 01: "**If price returns back inside the ORB, the setup is invalidated.**" | EXPLICIT AND MECHANICAL |
| 8 | **CONFIRMATION (fail) = Entry 04** | "It wicks through and closes back inside the range. **The candle body must close back inside the range. A wick above with the body still outside is NOT a fake — wait for the close.** Failed bullish = enter short, **target ORL**." | **EXPLICIT AND FULLY MECHANICAL** |
| 9 | **Targets** | Entry 04: the opposite ORB level. Entry 02: "next liquidity level … previous session high/low, new week opening gap, or the next key FVG" | EXPLICIT (E04), EXTERNAL (E02) |
| 10 | **Gate** | "**Minimum 1:2 R:R. Never take a trade unless your target is at least 2x your stop loss distance.**" | EXPLICIT, hard pre-trade gate |
| 11 | **Management** | "**Move to break even once at 1:1.**" · "**Stop trading after two losses in a day.**" | EXPLICIT, mechanical |
| 12 | **Axiom** | "There's nothing more bullish than a failed bearish move. Nothing more bearish than a failed bullish move." | EXPLICIT — **stated independently of Max, in identical words** |

**The source names its own primary model and tells you to isolate it**: Entry 02 is "the money
entry", and the 7-day plan says "**Backtest Entry 2 (Break & Retest) only**" three separate times.

---

## 3. WHERE THE TWO SOURCES AGREE, AND WHERE THEY SPLIT

| Element | Max | CeeWilli | Verdict |
|---|---|---|---|
| ORB window / construction | 09:30-09:45 wick-to-wick | identical | **converge** |
| Midline | central: bias filter **and** first target | absent from the playbook | **split** |
| Bias | mechanical (price vs midline) | discretionary, undefined | **Max is strictly more specified** |
| Break is not an entry | implied (wants print-through / hold) | explicit | converge |
| Retrace | preferred ("the retest is always the best way") | **mandatory** | converge in spirit |
| Continuation trigger | print-through / newer extreme | "rejects it" — undefined | **both under-specified; Max marginally more so in words, less so in mechanics** |
| Invalidation | close inside ORB = not a confirmation | close inside ORB = setup invalidated | **converge exactly** |
| Failed-break trigger | close inside **then a newer extreme against** | **the close inside itself** | **split — and it is measurable (§7)** |
| Failed-break target | midline, then opposite ORB | opposite ORB | converge |
| Failed-move axiom | stated 5× | stated verbatim | **independent convergence — the strongest cross-source agreement in the programme** |
| RR gate | never stated | ≥ 1:2, hard | CeeWilli only |
| BE at 1R, two-loss day stop | never stated | explicit | CeeWilli only |

---

## 4. THE FAILED BREAK, IN DETAIL (the priority pattern)

Nested path counts. `W` = ORB width. All 1-minute closes.

### 4.1 Break and first resolution

| | NAS100 | US500 |
|---|---|---|
| total ORB days | 2754 | 2753 |
| ORH breaks first | 1422 (51.6%) | 1418 (51.5%) |
| ORL breaks first | 1328 (48.2%) | 1331 (48.3%) |
| no close beyond either | 4 (0.1%) | 4 (0.1%) |

| after an ORH break | NAS100 | US500 | | after an ORL break | NAS100 | US500 |
|---|---|---|---|---|---|---|
| retraces to the level | 1341 (94.3%) | 1336 (94.2%) | | retraces to the level | 1270 (95.6%) | 1275 (95.8%) |
| never retraces | 81 (5.7%) | 82 (5.8%) | | never retraces | 58 (4.4%) | 56 (4.2%) |
| closes back inside | 1271 (89.4%) | 1272 (89.7%) | | closes back inside | 1227 (92.4%) | 1240 (93.2%) |
| holds outside all day | 151 (10.6%) | 146 (10.3%) | | holds outside all day | 101 (7.6%) | 91 (6.8%) |

**The retrace is near-universal (94-96%) and so is the close back inside (89-93%).** Neither is
selective. A rule that only requires "it broke and came back" selects nine days in ten.

### 4.2 Which confirmation fires first, among days that broke and retraced

| | NAS100 ORH | NAS100 ORL | US500 ORH | US500 ORL |
|---|---|---|---|---|
| continuation | 330 (24.6%) | 282 (22.2%) | 327 (24.5%) | 304 (23.8%) |
| **failed-break** | **760 (56.7%)** | **760 (59.8%)** | **785 (58.8%)** | **804 (63.1%)** |
| neither by 16:00 | 251 (18.7%) | 228 (18.0%) | 224 (16.8%) | 167 (13.1%) |

Symmetric across both sides and both instruments. **Failure is roughly 2.5× as common as
continuation.**

### 4.3 What happens after the failed-break confirmation

Measured **strictly forward from the confirmation bar** — this is the only measurement that could
be acted on.

| | NAS100 (n=1888) | US500 (n=2000) |
|---|---|---|
| opposite ORB reached **after** confirmation | 1139 (**60.3%**) | 1216 (**60.8%**) |
| opposite ORB **already reached before** confirmation | 197 (10.4%) | 316 (15.8%) |
| opposite ORB never reached | 552 (29.2%) | 468 (23.4%) |
| median minutes confirmation → opposite touch | 21 (IQR 6-60) | 20 (IQR 6-61) |

**Max's stated first target is frequently already gone.** The midline had already been crossed
before the confirmation printed on **53.8% (NAS100) / 57.6% (US500)** of confirmed failed breaks.
V8 [18:07] "take profit on the break of the midline" is unreachable as TP1 on more than half of
the setups it is meant to describe.

### 4.4 The structural problem: where is price when the confirmation prints?

Distance from the confirmation close to the opposite boundary, in ORB widths. 1.00 = the
confirmation printed at the broken boundary with the whole box still to travel.

| remaining | NAS100 n (%) | reach opposite after | US500 n (%) | reach opposite after |
|---|---|---|---|---|
| ≤ 0.00 (already there) | 146 (7.7%) | 0.0% | 211 (10.6%) | 0.0% |
| 0.00 - 0.25 | 278 (14.7%) | 79.1% | 348 (17.4%) | 67.0% |
| 0.25 - 0.50 | 423 (22.4%) | 79.4% | 427 (21.4%) | 80.6% |
| 0.50 - 0.75 | 567 (30.0%) | 65.4% | 540 (27.0%) | 66.5% |
| 0.75 - 1.00 | 422 (22.4%) | 46.4% | 437 (21.9%) | 59.3% |
| > 1.00 (still outside) | 52 (2.8%) | 30.8% | 37 (1.9%) | 56.8% |
| **median remaining** | **+0.54 W** | | **+0.51 W** | |

**Read this row by row.** The high hit rates belong to the rows where there was almost nothing left
to travel. Where a full box remains — the only case in which the stated target is worth taking —
the rate falls to **46-59%**. This is the single most important finding in this cycle: much of the
apparent edge in the failed-break pattern is the trivial fact that price is already most of the way
to the target when the pattern completes.

### 4.5 Failures of the failed break

Of the days that confirm and never reach the opposite boundary (NAS100 552, US500 468), travel
toward it as a fraction of W: p25 0.44/0.47, **p50 0.65/0.66**, p75 0.83/0.83, p90 0.93/0.92.
So the typical failure still travels about two-thirds of the way. It is a shortfall, not a reversal.

### 4.6 Time of day

| confirmation time | NAS100 n (%) | reach opp | median remaining | US500 n (%) | reach opp | median remaining |
|---|---|---|---|---|---|---|
| 09:45-10:00 | 580 (30.7%) | 60.5% | +0.74 W | 597 (29.9%) | 67.8% | +0.74 W |
| 10:00-11:00 | 762 (40.4%) | 64.4% | +0.47 W | 818 (40.9%) | 60.6% | +0.44 W |
| 11:00-13:00 | 342 (18.1%) | 56.1% | +0.35 W | 359 (17.9%) | 56.8% | +0.28 W |
| 13:00-15:00 | 141 (7.5%) | 56.7% | +0.33 W | 156 (7.8%) | 53.8% | +0.29 W |
| 15:00-16:00 | 63 (3.3%) | 39.7% | +0.29 W | 70 (3.5%) | 38.6% | +0.22 W |

71% of all confirmations print before 11:00. The early window is the only one that combines a
useful remaining distance with an above-base hit rate. **This is an observation, not a filter
proposal** — it has not been out-of-sample tested and no cut-off is being recommended.

---

## 5. EVIDENCE FOR CONTINUATION vs FAILURE — WHAT THE SOURCES ACTUALLY SAY

Both sources define **failure** mechanically and **continuation** loosely. That asymmetry is in the
source material itself, not an artefact of this reconstruction.

**Failure — mechanical in both:**
- Max V8 [06:11] close inside ORB ⇒ not a confirmation (invalidation).
- Max V8 [16:33] close back inside **then** "this confirmation, newer low" ⇒ trigger.
- CeeWilli E04 "The candle body must close back inside the range … wait for the close" ⇒ trigger.
- CeeWilli E01 "If price returns back inside the ORB, the setup is invalidated."

**Continuation — never mechanical:**
- Max V4 [05:37] "it needs to hold outside of it" — **no duration, no bar count, anywhere.**
- Max V10 [26:00] "I want to see a print through and a continuation … I'm going to wait for the
  confirmation of the reversal" — the trigger is a candle relationship, but which candle, on which
  timeframe, is stated only by example.
- CeeWilli E02 step 3 "Price retests the level **and rejects it**" — **"rejects" is undefined in
  Entry 02.** The playbook's only mechanical rejection definition is in **Entry 03**: "a strong
  reversal candle **closes back on the correct side of the level**."

**Per the mandate, no continuation confirmation has been invented here.** The census measures
continuation as "a newer extreme in the break direction after the retrace, with no prior close back
inside" — that is the weakest reading consistent with V4 [05:37] and V12 [27:23], and it is
reported as a measurement, not proposed as a rule.

---

## 6. CANDIDATE DISCRIMINATORS — ALL FLAT

Every variable the programme has previously reached for was tested as a plain cross-tab. None
separates continuation from failure.

**ORB width** (quartiles, days that broke and retraced):

| | Q1 narrow | Q2 | Q3 | Q4 wide |
|---|---|---|---|---|
| NAS100 failed-break rate | 57.6% | 57.7% | 60.0% | 57.6% |
| NAS100 opposite reached | 51.6% | 54.2% | 52.3% | 47.6% |
| US500 failed-break rate | 65.8% | 58.9% | 62.5% | 56.2% |
| US500 opposite reached | 63.4% | 60.1% | 58.3% | 54.1% |

Width does not predict failure. It weakly *anti*-predicts reaching the far side, which is what
geometry alone would produce.

**How long price held outside before invalidating** — the natural reading of "it needs to hold
outside of it":

| held outside | ≤1 min | 2-5 | 6-15 | 16-60 | >60 |
|---|---|---|---|---|---|
| NAS100 opposite reached | 70.3% | 74.1% | 65.4% | 72.1% | 62.1% |
| US500 opposite reached | 78.8% | 77.8% | 74.8% | 78.6% | 69.6% |

**Flat.** A break that held outside for an hour before failing behaves like one that lasted a
minute. This is a direct negative result against the most intuitive mechanisation of V4 [05:37].

**External FVG on the far side** (1-minute, formation any time):

| | FVG present | FVG absent |
|---|---|---|
| NAS100 failed-break → opposite reached | 69.7% (n=1020) | 73.0% (n=500) |
| US500 failed-break → opposite reached | 77.3% (n=1133) | 77.4% (n=456) |

**Null, on both instruments.** Within the failed-break population the external FVG carries no
information about whether the opposite boundary is reached. This does not contradict the earlier
+4.8 pp FVG-touch result (a different conditioning event), but it does mean **FVG presence cannot
be used as the continuation/failure discriminator**, and it is further reason not to treat FVG as
the strategy.

**Consolidation after the retrace** (V1 [20:34] "failed to make a newer high, failed to make a
newer low") — NAS100 27.0% / 17.0% / 11.9% of retrace days at 10/20/30 bars; US500 26.3% / 14.3% /
9.7%. Of the 10-bar consolidations, NAS100 441 resolved as failed-break vs 27 as continuation
(US500 482 vs 22). **Consolidation after a break is overwhelmingly followed by failure, ~17:1.**
This is the one candidate discriminator that is *not* flat, and it is the recommended target for
the next cycle — with the caveat that the window length is a free parameter and three values were
reported rather than one chosen.

---

## 7. HEAD-TO-HEAD: THE TWO FAILED-BREAK TRIGGERS ON THE SAME DAYS

| | NAS100 | US500 |
|---|---|---|
| unconditional opposite-reach after any break | 48.8% | 56.0% |
| **CeeWilli E04** (close back inside) — setups | 2498 (90.8% of broken days) | 2512 (91.4%) |
| … opposite reached after trigger | 53.6% (**+4.8 pp**) | 61.0% (**+5.0 pp**) |
| … midline reached after trigger | 75.7% | 79.2% |
| **Max V8** (close inside **+** newer extreme against) — setups | 1888 (68.7%) | 2000 (72.8%) |
| … opposite reached after trigger | 60.3% (**+11.5 pp**) | 60.8% (**+4.8 pp**) |
| … midline reached after trigger | 37.4% | 35.9% |

Max's extra confirmation discards 24.4% / 20.4% of CeeWilli's setups. It buys +6.7 pp of forward
hit rate on NAS100 and −0.2 pp on US500. **It is not a reliable improvement.** What it unambiguously
does is destroy the midline target: waiting for the newer extreme against means the midline has
already been crossed on more than half the setups (75.7% → 37.4%).

**Year-by-year stability of the failed-break → opposite-boundary rate** (conditional form):
NAS100 64.5-74.8% across 2016-2026, US500 70.2-84.5%. No trend, no regime break, 2026 lowest in
both (64.5% / 70.2%, n=110 / 104 — partial year).

---

## 8. PROPOSED COMBINED / SPLICED STATE MAP

Stated as a **map of observed states**, not a trading rule. No parameter in it has been fitted.

```
  09:30-09:45  ORB forms.  ORH = high, ORL = low, MID = (ORH+ORL)/2        [both sources]
        |
        v
  S0  PRE-BREAK.  Bias = price vs MID                                       [Max V5 10:43 only;
        |                                                                    CeeWilli: undefined]
        v
  S1  BREAK      first 1m close beyond ORH or ORL           99.9% of days
        |         (neither source enters here)              [CW E02 s1; Max V1 27:18]
        v
  S2  RETRACE    price trades back to the broken level      94-96% of breaks
        |         [CW E02 s2 mandatory; Max V12 27:23 preferred]
        |
        +--> S3a  HOLDS OUTSIDE, newer extreme with          22-25%   CONTINUATION
        |          [Max V4 05:37 + print-through; CW E02 s3 "rejects it"]
        |          *** trigger not mechanically defined by either source ***
        |
        +--> S3b  1m BODY CLOSES BACK INSIDE                 89-93% of breaks
        |          [Max V8 06:11 invalidation; CW E01/E04 invalidation]
        |          |
        |          +--> S4a  CeeWilli E04 fires HERE — enter, target opposite ORB
        |          |          forward opposite-reach 53.6% / 61.0%
        |          |
        |          +--> S4b  NEWER EXTREME AGAINST prints    68.7-72.8% of breaks
        |                     [Max V8 16:33] Max fires HERE
        |                     forward opposite-reach 60.3% / 60.8%
        |                     median distance left at this point: 0.51-0.54 W
        |                     TP1 (MID) already gone on 54-58% of these
        |
        +--> S3c  NEITHER by 16:00                           13-19%
```

**The splice point is S3b→S4.** That single choice — enter on the close back inside (CeeWilli) or
wait for the newer extreme against (Max) — is the only place the two reconstructions materially
disagree, and §7 measures it. Everything upstream of S3b is common ground.

---

## 9. VISUALS

Two figures, both reviewed panel by panel before publication.

- `OUTPUTS/FIGS/CORE_PATH/PATH_CLASSES_{NAS100,US500}.png` — the six mandated scenario classes,
  three deterministic examples each (first by date, no other filter): ORH continuation ·
  ORH failed→ORL · ORH ambiguous · ORL continuation · ORL failed→ORH · ORL ambiguous.
- `OUTPUTS/FIGS/CORE_PATH/FAILED_BREAK_TIMING.png` — the three failed-break timing sub-cases of
  §4.3, both instruments: actionable · confirmation-arrives-after-the-move · confirmed-but-never-reached.

**What review of the figures changed.** Inspecting `FAILED_BREAK_TIMING.png` column 2 showed panels
where the confirmation minute and the opposite-touch minute are the *same bar* (e.g. NAS100
2016-02-08, confirm 15:44 / opposite 15:44). On those days the reference extreme used by "newer
extreme against" sits at or near the opposite boundary itself, so the confirmation is structurally
incapable of preceding the draw. That observation is what prompted §4.4, which is the most
consequential table in this report. Without looking at the pictures the 70.8% conditional number
would have been reported as the finding.

---

## 10. WHAT IS STILL VISUALLY OBVIOUS BUT NOT MECHANICALLY DEFINED

Ordered by how much it blocks progress.

1. **"It needs to hold outside of it."** (Max V4 [05:37]) No duration is given in any of the twelve
   transcripts. The obvious mechanisation — minutes held outside before invalidation — is **flat**
   (§6). Something other than elapsed time is meant. *Not invented here.*
2. **"Rejects it."** (CeeWilli E02 step 3, "the critical step") Undefined in Entry 02. The only
   mechanical rejection definition in the whole playbook is Entry 03's "a strong reversal candle
   closes back on the correct side of the level". Whether that definition is intended to carry over
   to Entry 02 is **unknown and must not be assumed.**
3. **CeeWilli's bias.** "Overall market bias (bullish or bearish)" is on the pre-market checklist
   with no method anywhere in the document. Max has a complete rule (V5 [10:43]); CeeWilli has none.
4. **The "one-two punch".** Max V8 [11:18]: "the one-two punch is always going to be the fail and
   the retest … **the second retest candle that failed and closed outside of orb** — the second this
   candle made a newer low, that's the retest confirmation". This describes a **second** failed
   retest, which is strictly narrower than the single close-back-inside measured here, and it was
   *not* measured in this cycle. It is mechanisable as stated and is the clearest unexploited
   specification in the corpus.
5. **Timeframe.** CeeWilli's own backtest instruction is **5-minute**; the programme executes on
   1-minute. Unresolved (U-23).
6. **Which candle, on which timeframe, is a "print through".** Stated only by example.
7. **The consolidation window.** V1 [20:34] defines consolidation qualitatively. No bar count is
   given. Three windows were reported rather than one chosen (§6).

### Exactly which Discord screenshots would resolve these

A screenshot is useful here only if it shows a **marked-up chart with the author's own annotation
of the decision point**, not a P&L or a call-out.

| # | What to capture | Resolves |
|---|---|---|
| D1 | **CeeWilli** marking an Entry 02 **rejection candle** on a chart — the exact candle he calls the trigger, with the ORB level drawn | Item 2 — the single biggest CeeWilli gap |
| D2 | **CeeWilli** stating or marking **how he sets bias** pre-market (any message where he says "I'm bullish today because…") | Item 3 |
| D3 | **CeeWilli** on **which timeframe he actually executes** Entry 02 (1m or 5m) — a chart screenshot with the timeframe selector visible is enough | Item 5 / U-23 |
| D4 | **Max** marking a break he **rejected** because it "didn't hold outside" — a negative example with the bar count visible | Item 1. Positive examples cannot resolve this; only a rejected one can. |
| D5 | **Max** marking the **one-two punch** — first retest, second retest, the newer low — on one chart | Item 4 |
| D6 | Either author marking a **print-through candle** with the timeframe visible | Item 6 |
| D7 | Either author marking a **consolidation** with the candles he counted visible | Item 7 |
| D8 | Any message where either author **states a target other than the midline / opposite ORB**, with the reasoning | Entry-02 target definition |

**D1 and D4 are the two that matter.** Without D4 the continuation branch of the state map cannot
be closed for Max, and without D1 it cannot be closed for CeeWilli. Everything else in §10 is
refinement.

---

## 11. LIMITS OF THIS CYCLE — STATED PLAINLY

- **No fresh primary-source video review was performed by the Analyst.** No video files, no PDFs and
  no CeeWilli C1-C4 transcripts exist in the repository. The twelve V1-V12 files are the Research
  Agent's **evidence extracts, not full transcripts**. Every Max quotation here is re-verified
  against those extracts; none is quoted from memory. **Fresh video review remains Research Agent
  work.** The CeeWilli reconstruction rests entirely on the playbook audit.
- **No economics.** No cost, no R, no fills, no entries. The mandate excluded them and they are
  excluded. None of the counts above should be read as an edge estimate.
- **"Newer extreme against" uses the extreme since 09:45 as its reference.** For breaks at 09:45-09:47
  (38-40% of failed breaks) that reference window is very short, which makes the confirmation easy
  to satisfy. This is a faithful but loose reading of "newer low"; a swing-based reference would be
  a different measurement. **No swing definition was invented to fix it.** It is flagged, not patched.
- **The "neither" bucket is not a valid control** — 22-27% of it is days that never closed back
  inside, which cannot reach the opposite boundary by construction. The valid benchmark is the
  unconditional rate, and that is what §0 and §7 use.
- **§4.6 time-of-day and §6 consolidation are observations, not proposals.** Neither has been
  out-of-sample tested. Acting on either would be exactly the optimisation this mandate forbids.

---

## 12. WHAT THIS CHANGES

1. **The bias step is solved for Max and open for CeeWilli.** V5 [10:43] must be written into the
   Max specification and the "no mechanical bias definition" note retired.
2. **The failed break is the main event, and it is the state both sources specify mechanically.**
   The continuation branch is under-specified in *both* corpora. The programme has been spending its
   effort on the branch the sources describe least.
3. **The honest effect size is +5 to +11 pp of forward probability, not +20 to +29 pp.** Any future
   economics must start from the forward-measured numbers in §7, never the conditional ones.
4. **Max's midline TP1 is incompatible with Max's own failed-break trigger** on 54-58% of setups.
   That is an internal inconsistency in the source, surfaced by measurement, and Research should be
   asked which of the two he actually means.
5. **External FVG is not the discriminator.** Null on both instruments within the failed-break
   population.
6. **Consolidation-then-failure (~17:1) is the one live lead.** Next cycle should measure it
   properly — including the window-length sensitivity — before anything else.

---

## 13. CYCLE 2 ADDENDUM — SOURCE RE-REVIEW AND MECHANISATION (Analyst, 22 Sep 2026b)

**Everything in §§1-12 above is unchanged and preserved as historical evidence from the
first reconstruction cycle.** This addendum is a second, same-day pass requested to
re-review V1-V12 and the CeeWilli sources specifically for the hover/consolidation
structure, the one-two-punch, and the "rejects it" gap. **No market-data access and no
Python execution were available in this sandbox this cycle** (same blocker as the
`claude/issue-3-20260921-*` cycles on this issue) — §§13.5-13.7 are specifications and
code for the next local run, not new counts. Nothing below revises the counts in §§1-12;
it revises what should be *measured next* and corrects one mischaracterisation.

### 13.1 Correction: CeeWilli's "rejects it" is not actually undefined

§10 item 2 of this report (first cycle) states: *"'Rejects it.' Undefined in Entry 02
... Whether \[Entry 03's definition\] is intended to carry over to Entry 02 is unknown
and must not be assumed."* Re-reading `RESEARCH_CURRENT.md` against the CeeWilli
playbook audit shows this overstates the gap. **§D.6 of `RESEARCH_CURRENT.md` (v2.2)
already makes exactly that carry-over, explicitly and by name:**

> "The mechanical form is given explicitly in Entry 03 and carries over: 'a strong
> reversal candle closes back on the correct side of the level.' **REJECTION candle
> (long) = a candle that interacts with ORH (`low <= ORH <= high`) and closes above
> ORH.**" — classified EXPLICIT (03) / STRONGLY IMPLIED (02).

This is also independently corroborated by the CeewilliTradez video evidence (C1-C4,
same author as the playbook — confirmed by `RESEARCH_CURRENT.md`'s own source line
"@MaxOptionsTrading (V1-V14) · @CeewilliTradez (C1-C4)"), which `RESEARCH_CURRENT.md`
already cites for exactly this state:
- C1 [04:41] "I'm just waiting for another **body stick candle closure**. Okay, so I get
  a body stick candle closure right here. Boom, it's entered in here."
- C4 [05:36] "We don't just want a wick. We want a lot of displacement outside of the
  orb." — confirming a wick alone does not qualify (matches D.6's `close above ORH`,
  not `high above ORH`).
- C2 [03:34] "Wait, confirmation, execute" — the three-step frame this candle sits in.

**What is genuinely still open is narrower than "rejects it is undefined."** It is U-22
(`RESEARCH_CURRENT.md` §D.5): *whether a genuine body close back inside the ORB, before
the rejection candle, invalidates the setup or is compatible with a deep Entry-02
retest.* That is a real, unresolved contradiction (playbook Entry 01's unconditional
invalidation vs. CeeWilli's own worked example VRC-01, which shows six consecutive 1m
closes back inside before the entry) — and it is **already being run as two arms**, HOLD
and DEEP, in the v2.3 CeeWilli Entry-02 rebuild this issue commissioned separately. It
does not need re-opening here; it needs the results of that run.

**Correction to carry forward:** CeeWilli's rejection candle has a stated mechanical
definition (§D.6) borrowed explicitly from Entry 03 by the Research Agent's own ruling.
The open question is not "what does rejection mean" but "does a prior close-back-inside
disqualify it" (U-22 / HOLD vs DEEP). Bias remains genuinely unresolved for CeeWilli, as
the first cycle found — the playbook gives no method anywhere and this addendum found no
new evidence that changes that (§13.8, item 3).

### 13.2 MAX — refined event sequence: three-bar and the double-retest pattern

Re-reading V1-V12 beyond the passages already quoted in §1 surfaced a primitive not used
in the first cycle: **the "three bar" pattern**, stated independently in two videos and
tied explicitly to ORB by a third.

- V2 [41:21]-[42:03]: "the market can only do two things. Trend, range, trend ... A
  three bar is just a three to four candlestick pattern that perfectly displays this. So,
  we trend up, we range within the candle body, and then we continue upwards ... **Bar
  number one. Bar number two. Bar number three is the continuation pattern.**" [42:03]
  "You wait for bar number two to form. **As soon as bar number three breaks above bar
  number two, you enter the trade** with a stop-loss at the bottom or right below candle
  2's wick."
- V5 [15:02]-[16:22]: "what we're looking for is a green candle, red candle — it doesn't
  have to be red — and then a continuation candle. What it's really just showing you is
  **trend, range, trend**." [16:49] "**These candles work significantly better around
  areas of liquidity like orb.**"
- V2 [18:41]: "I only trade two candlestick patterns. I only trade two, **break and
  retest and a three bar.**" — presented as a second, general-purpose pattern, not
  explicitly stated to *be* the ORB hover. The V5 [16:49] proximity endorsement is the
  only stated link between the two. **This is a plausible, source-consistent
  mechanisation, not a proven identity — flagged, not assumed.**

**Why this matters for the hover/consolidation question (item 3/4 of the mandate).**
Bar 2 of the three-bar pattern — "we range within the candle body" — is structurally the
same primitive V1 uses for consolidation: "we failed to make a newer high, we failed to
make a newer low" (V1 [20:34]). Bar 3 is the event that ends it, in either direction. So
the source's own vocabulary already supplies an **event-based start and end for the
hover state**, without inventing a bar count:

```
START:  first bar after the retrace that fails to extend the post-break extreme
        (a "range" bar — V1's "failed to make a newer high, failed to make a newer low")
HOVER:  however many consecutive bars keep failing to extend it (length is MEASURED,
        never chosen)
END:    the first bar that either
          (a) extends the extreme in the break direction  -> CONTINUATION (three-bar's
              "bar 3 breaks above bar 2")
          (b) sets a newer extreme in the OPPOSITE direction -> FAILURE
              (V8 [16:33] "this confirmation, newer low")
```

This is a direct answer to the mandate's question — *"what event finally distinguishes
continuation from failure?"* — read from the source's own words: **not a duration, an
outcome.** The hover ends when it ends; what matters is which side resolves it first,
and §13.3 below gives it as code, not a fitted window.

**The double-retest pattern, independently corroborated three times.** Re-reading V8's
"one-two punch" passage in full alongside two other passages not previously connected to
it in this programme's reconstructions:

- V8 [11:18]-[12:20]: "the one-two punch is always going to be the fail and the retest
  ... when you get the retest of the candle or the liquidity zone and it fails, this
  candle here was entry 100% ... **the second retest candle that failed and closed
  outside of orb — the second this candle made a newer low, that's the retest
  confirmation** and this was your entry today."
- V8 [14:52] (blind bar-replay, a different, bullish example): "close outside of orb,
  **retest, retest**, breakout, the higher high ... this is your entry."
- V12 [27:23]: "the retest is always the best way to go ... **retest, doji retest**,
  usually could pump to a newer high."

**Reading, stated plainly (ASR transcript, so flagged rather than asserted as certain):**
the one-two-punch is a **continuation-side** confirmation — the break holds, price
retests the broken level and is rejected *twice* (never reclaiming it), and the second
rejection prints a newer extreme in the break direction. This is a stricter, doubly
confirmed version of the simple print-through trigger already measured in §1 row 7, not
a third failure trigger. Three independent passages across two videos describe
continuation this way; none describes it as a single event. **This reframes "it needs to
hold outside of it" (V4 [05:37]) as "surviving N discrete retest failures without a body
close back inside," where the one-two-punch is the source's own worked N=2 case** — not
as elapsed time, which §6 of the first cycle already showed is flat. No duration is
invented; N is counted, not chosen.

### 13.3 Mechanisation — event-based consolidation and one-two-punch (spec + code)

Both are specified precisely enough to code, and code has been written extending
`orb_path_census.py`'s existing per-day loop (same `H, L, C, M, bi, side, bnd, back`
objects it already computes). **The code below has not been executed — no Python
execution was available in this sandbox.** It must be run against a small labelled
sample (5-10 known days, visually checked) before any count from it is trusted, exactly
as this programme's own self-test discipline requires elsewhere.

New file: `13_CROSS_MARKET/CODE/orb_path_census_v2.py`

```python
#!/usr/bin/env python3
"""
UNTESTED THIS CYCLE — no Python execution was available. Validate against a small
labelled sample (5-10 days, visually checked) before trusting any count from this file.

Extends orb_path_census.census() with two event-based mechanisations requested in
issue #3 (22 Sep 2026b cycle):
  event_consolidation()  -- hover/consolidation with a measured, not chosen, length
                            (V1 20:34 "failed to make a newer high, failed to make a
                            newer low"; V2/V5 "three bar" / trend-range-trend)
  one_two_punch()         -- Max's double-retest continuation confirmation (V8 11:18,
                            corroborated by V8 14:52 and V12 27:23)
Both take the same per-day arrays orb_path_census.census() already computes and return
None (not measured) rather than a fabricated boolean when the source primitives don't
resolve within the session.
"""
import numpy as np


def event_consolidation(H, L, C, M, bi, side, back):
    """
    Event-based hover state, starting at the first bar after the retrace that fails to
    extend the post-break extreme, ending at the first bar that resolves it either way.
    Returns a dict or None if there was no retrace (back is empty) to start from.
    """
    if not len(back):
        return None
    r0 = bi + 1 + back[0]
    ext = H[:r0 + 1].max() if side == 1 else L[:r0 + 1].min()
    n = len(M)
    i = r0 + 1
    hover_len = 0
    while i < n:
        newer_with = (H[i] > ext) if side == 1 else (L[i] < ext)
        # "opposite" extreme tracked only from r0 forward, i.e. the retrace low/high --
        # this is the invalidation boundary, not the pre-break range.
        opp_ref = L[r0:i].min() if side == 1 else H[r0:i].max()
        newer_against = (L[i] < opp_ref) if side == 1 else (H[i] > opp_ref)
        if newer_with:
            return dict(start_m=int(M[r0]), end_m=int(M[i]), hover_bars=hover_len,
                        resolution="continuation")
        if newer_against:
            return dict(start_m=int(M[r0]), end_m=int(M[i]), hover_bars=hover_len,
                        resolution="failure")
        hover_len += 1
        i += 1
    return dict(start_m=int(M[r0]), end_m=None, hover_bars=hover_len,
                resolution="unresolved_by_session_end")


def one_two_punch(H, L, C, M, bi, side, bnd, back):
    """
    Double-retest continuation confirmation (V8 11:18). Requires the level to be
    retested and fail to reclaim TWICE before confirming on a newer extreme.
    "Fail to reclaim" = price touches the boundary again but does not CLOSE back inside
    the ORB (the source's own invalidation event, D.6/V8 06:11, is what "reclaiming"
    means here -- so absence of that event is the retest's failure).
    Returns None if fewer than two distinct retest touches occur before either an
    inside close (disqualifies -- this is Entry 04 / V8 06:11 territory, not one-two-
    punch) or the session ends.
    """
    if not len(back):
        return None
    n = len(M)
    touches = []
    i = bi + 1
    in_touch = False
    while i < n:
        touching = (L[i] <= bnd <= H[i]) if side == 1 else (L[i] <= bnd <= H[i])
        closed_inside = (C[i] < bnd) if side == 1 else (C[i] > bnd)
        if closed_inside:
            return dict(disqualified_at_m=int(M[i]), reason="closed_back_inside")
        if touching and not in_touch:
            touches.append(i)
            in_touch = True
        elif not touching:
            in_touch = False
        if len(touches) >= 2:
            ext_after_first = (H[touches[0]:i + 1].max() if side == 1
                                else L[touches[0]:i + 1].min())
            ext_before_second = (H[touches[0]:touches[1]].max() if side == 1
                                  else L[touches[0]:touches[1]].min())
            newer = (H[i] > ext_before_second) if side == 1 else (L[i] < ext_before_second)
            if newer:
                return dict(retest1_m=int(M[touches[0]]), retest2_m=int(M[touches[1]]),
                            confirm_m=int(M[i]), n_retests=len(touches))
        i += 1
    return dict(n_retests=len(touches), reason="unresolved_by_session_end")
```

**What this is not.** It is not run, it is not validated, and no count derived from it
appears anywhere in this addendum. Per the mandate, no economics, no thresholds, no
scoring were added — both functions return a measured length / a "which side resolved
it," never a chosen window.

### 13.4 Comparison framing (spec, not numbers)

The mandate asks for the one-two-punch population's path outcome compared against (A)
simple CeeWilli close-back-inside and (B) existing Max close-inside + newer-extreme-
against (§7 of the first cycle). Those two are **failure-side** triggers; one-two-punch
as reconstructed in §13.2 is a **continuation-side** trigger. The honest comparison is
therefore not "which one predicts the same outcome better" but a **representation
comparison across all three of how much confirmation the source demands before it calls
the moment resolved**:

| trigger | side | events required | population (this cycle) |
|---|---|---|---|
| CeeWilli E04 close-back-inside | failure | 1 (single body close inside) | measured, §7 |
| Max close-inside + newer-extreme-against | failure | 2 (close inside, then a newer extreme against) | measured, §7 |
| Max one-two-punch | continuation | 2 (two failed retests, second sets a newer extreme with) | **spec only — §13.3, pending local run** |

Once run, this table should carry: n, % of all breaks selected, forward opposite-reach /
continuation-reach rate, and median remaining distance at confirmation (same columns as
§4.4), so it is comparable on the same basis as the first cycle's numbers.

### 13.5 Nested path-count table (spec, no numbers invented)

Requested shape for the next local run, forward-only from the actionable confirmation,
mirroring §4/§7's structure exactly so it appends rather than replaces:

```
ORB side broken (ORH / ORL)
  -> retrace (yes / no)
    -> resolution class: continuation / failed-break / one-two-punch-continuation /
       unresolved-by-16:00   [event_consolidation() + one_two_punch(), §13.3]
      -> one-two-punch present / absent, WITHIN the continuation class only
        -> opposite ORB subsequently reached (forward from confirmation) / not reached
      -> remaining ORB distance (in W) at the confirmation bar  [same measure as §4.4]
```

Pooled + by direction (ORH/ORL) + by instrument (NAS100/US500), same as §4-§7.

### 13.6 Visual pack (spec, no charts rendered — no data access)

Extending `orb_failbreak_figs.py`'s conventions, five panels requested by the mandate:
break -> retrace -> clean continuation; break -> retrace -> hover -> failed break ->
opposite ORB; first retest fails but second resolves (the one-two-punch case,
`retest1_m`/`retest2_m`/`confirm_m` from §13.3 marked on the chart); visually similar
hover that continues instead; ambiguous/no-resolution case
(`resolution="unresolved_by_session_end"`). Each panel must mark ORH, ORL, midline, the
break bar, every retest touch, and the resolving bar — same rule the first cycle's
visual review already established mattered (§9: reviewing figures is what surfaced §4.4).

### 13.7 Revised state map — the hover branch made explicit

Extends the first cycle's S3a/S3b map (§8) with the hover state and its two exits:

```
  S2  RETRACE    (unchanged, §8)
        |
        v
  S2h HOVER      event_consolidation() start: first bar failing to extend the
        |         post-break extreme. Length MEASURED, not chosen (§13.2/§13.3).
        |
        +--> resolves WITH the break  -> S3a CONTINUATION
        |      one_two_punch() is the source's own worked N=2 sub-case of this exit
        |      (V8 11:18); simple print-through (§1 row 7) is the N=1 case.
        |
        +--> resolves AGAINST the break -> S3b (unchanged, §8's existing failed-break
        |      branch: close-inside, then newer-extreme-against)
        |
        +--> unresolved by session end (S3c, unchanged, §8)
```

The splice point identified in the first cycle (§8: "the splice point is S3b->S4") is
unchanged by this addendum. What's new is only that S2's internal structure — the part
between the retrace and whichever confirmation fires — now has a source-derived shape
instead of being an unstructured gap.

### 13.8 Explicit unresolved human-visual distinctions (revised from §10)

1. **Whether the three-bar / hover identity (§13.2) actually holds on ORB days**, as
   opposed to being two separately-taught patterns that happen to share vocabulary. Only
   resolvable by running `event_consolidation()` and checking whether its detected hover
   bars visually match a three-bar "range" candle, or by a **new** screenshot: Max
   marking a three-bar pattern **at an ORB retrace specifically** (not a standalone
   setup elsewhere in the session).
2. **The one-two-punch's ASR ambiguity** (§13.2/§13.3) — "the second retest candle that
   failed and closed outside of orb" is transcribed speech, not written source. **D5**
   (Max marking the one-two-punch on one chart, per §10's original request) remains the
   single highest-value unresolved screenshot; §13.3's code is one reasonable
   mechanisation of the ASR text, not a certainty.
3. **CeeWilli's bias** is unchanged from the first cycle: no method anywhere in the
   playbook; the video veto (C4 07:08) is discretionary and not in the written spec.
   **D2** still resolves it if it exists; nothing found this cycle changes that.
4. **D4** (Max rejecting a break that didn't "hold outside") is still the only evidence
   that could directly confirm or break the §13.2 N-failed-retests reframing of "hold
   outside" — a positive one-two-punch example doesn't do this; only a **rejected**
   candidate does, per the original §10 reasoning, which still holds.

### 13.9 What remains for local execution

Everything numeric in §§13.3-13.6 is pending the same local run already commissioned
for the v2.3 CeeWilli/FVG cycle on this issue (`python3 run_v23_cycle.py` from
`13_CROSS_MARKET/CODE/`). `orb_path_census_v2.py` (§13.3) is new and separate from that
entry point — it extends `orb_path_census.py`'s per-day loop and should be wired in and
validated on a small sample (5-10 days, visually checked against `orb_failbreak_figs.py`
output) before it contributes any count to this file.
