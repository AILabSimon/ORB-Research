# ORB PROGRAMME — SOURCE-FAITHFUL STRATEGY RECONSTRUCTION
# 20.1 REPRESENTATION AUDIT
Research Agent (Agent 1) · 2026-09-20 · Cycle 4
Sources studied independently: @MaxOptionsTrading (14 videos, V1-V14) and
@CeewilliTradez (4 videos, C1-C4). Third source @TsugiTrades assessed separately by
the Analyst and not merged here.

Narrow purpose of this document, as set by the brief: **make sure we are testing the
right trade.** It is not a performance evaluation, not an optimisation, and contains
no recommendation to trade.

## EVIDENCE CLASSES USED ON EVERY ELEMENT
- **EXPLICIT** — stated in words by the source, quotable.
- **REPEATED** — stated explicitly on two or more separate occasions/videos.
- **VISUAL** — observed on the source's own chart; not stated in words.
- **INFERENCE** — a reasonable reading that the source did not state and did not
  demonstrate unambiguously. Carries no authority to become a rule.
- **UNKNOWN** — not determinable from available material.

---

# PART 1 — EXECUTIVE CONCLUSION

**We are probably not testing the trade either source teaches.** The mismatch is not
in the opening range, the direction definition, or the targets. It is concentrated in
one place: **the segment between the first break and the entry.**

Three findings carry this conclusion.

**(a) The break is a signal to watch, not a signal to enter. Both sources say so
explicitly and repeatedly.**
- Max V1 22:36 — the 15-minute close beyond the range is "your signal… the casting
  the bat signal. **Get ready**." He then drops to a 1-minute chart and waits.
- Max V13, three separate times inside twelve minutes — "It's not the candle you
  think you should enter on. **It's usually the next one.**"
- CeeWilli C1 08:59 — "the indicator is telling us to enter. **I don't enter just
  yet.** I want a little bit more of a better break and a better retest."
Classification: EXPLICIT and REPEATED for both sources.

**(b) The retest is not a touch. It is a return into the range followed by a reclaim.**
The Analyst reports **zero of 2,370 generated trades closed back inside the ORB
between confirmation and entry**. That is a mechanical consequence of a candidate
generator that places the entry region *between* the confirmed direction and the ORB
edge — i.e. one that assumes price stays outside. In CeeWilli's own worked example
(Exhibit V-01, ES1! 1-minute, 28 May 2026) **six consecutive 1-minute bars closed back
inside the range** between the break and the entry, and the entry bar is the bar that
closes back *outside*. Max describes the same topology in words: V12 08:49 — "**Until
it breaks back outside of orb there's no confirmations.**"
Classification: EXPLICIT (Max, verbal) + VISUAL (CeeWilli, one example) + EXPLICIT
(CeeWilli, verbal C1/C3/C4).

**(c) A wick through the level is explicitly not an entry; a body close is.**
CeeWilli C4 05:36 — "We don't just want a wick. We want a lot of displacement outside
of the orb." Exhibit V-01 shows the bar immediately before entry piercing the ORB high
with its wick and closing back inside — and it is not taken. The next bar closes
beyond the level and *is* taken.
Classification: EXPLICIT (CeeWilli) + VISUAL corroboration.

**What this does and does not mean.**
It means the candidate generator is very likely producing a *different population of
trades* from the one either source describes, and that our measured result therefore
does not yet falsify what they teach. It does **not** mean the taught version works.
The Analyst's separate measurement — gross edge at R>=20 of **-0.034R** — already
covers the widest plausible stop construction, and R-050 (Max teaches sizing the stop
to the recent wick distribution, ~25 NQ points) pushes cost/R to ~0.053R against a
~0.046R reopening threshold. The honest statement is: **the closure survives the cost
objection, but it has not yet been tested against the correct entry sequence.**

**Single recommended action.** Re-specify the candidate generator per Part 12 and
re-run. Change nothing else. Do not add indicators, filters, or discretion.

---

# PART 2 — MAX SPECIFICATION (studied independently)

## 2.1 Instruments and timeframes
| Element | Content | Class |
|---|---|---|
| Primary instrument | NQ (Nasdaq E-mini/micro futures) | EXPLICIT, REPEATED |
| Also shown | ES, and options on index underlyings in older material | EXPLICIT but ISOLATED |
| Range-defining timeframe | 15 minutes | EXPLICIT, REPEATED |
| Execution timeframe | 1 minute, and 30 seconds in live trades | EXPLICIT + VISUAL |
| Chart timezone | ET in most videos; **V14 charts are Central (08:30 open)** | VISUAL |
| Session | US equity RTH open | EXPLICIT |

## 2.2 Opening range construction
| Element | Content | Class |
|---|---|---|
| Window | 09:30-09:45 ET, the first 15-minute candle | EXPLICIT, REPEATED, stable 2024→2026 |
| Boundaries | wick to wick (high and low of that candle) | EXPLICIT, REPEATED |
| Midline | (H+L)/2, plotted and referred to | EXPLICIT |
| Range redefinition intraday | none taught | NOT FOUND |

## 2.3 What Max calls the signal
A **15-minute body close** beyond the range boundary. V1 22:36: this is "your signal…
the casting the bat signal. Get ready." It is explicitly a **preparation** trigger, not
an entry trigger. (EXPLICIT; the "get ready" framing is EXPLICIT and reinforced by the
V13 repetitions.)

## 2.4 Entry
| Element | Content | Class |
|---|---|---|
| Entry timeframe | 1-minute, 30-second in live execution | EXPLICIT + VISUAL |
| Entry event | "the continuation **print through**" (V1 27:18) | EXPLICIT, REPEATED |
| "Print through" defined | a candle trading beyond the previous candle's extreme in the trade direction, **then continuing** | EXPLICIT (definition given in V12 cycle) |
| Entry bar | "It's not the candle you think you should enter on. It's usually the next one." (V13 x3) | EXPLICIT, REPEATED |
| Mechanism used live | resting **pending orders** (stop orders) placed at the print-through level, on 30s/1m | VISUAL, REPEATED |
| Resting stop order beyond the ORB edge | **NOT FOUND in any video** | NOT FOUND |
| Prospective continuation-vs-reversal selector | **does not exist**; what exists is a conditional pre-commitment to both branches (an OCO bracket) | CONFIRMED NEGATIVE (RR-002) |

## 2.5 Direction — how Max decides which way
Max's direction language is **structural and persistence-based**, not magnitude-based.
- The TRT three-bar pattern: bar 2 ranges **inside** bar 1's body, then bar 3 resolves.
  (EXPLICIT)
- "No close, no close, no close, **close**" — the level must survive repeated attempts
  and then be closed through. (EXPLICIT)
- A close back inside the range **removes** the confirmation: V12 08:49 — "Until it
  breaks back outside of orb there's no confirmations." (EXPLICIT)
- He does **not** use "confirming-block range / ORB range" or any displacement ratio.
  (NOT FOUND — and this is the metric our model uses; see Part 10.)

## 2.6 Stops
| Element | Content | Class |
|---|---|---|
| Initial stop | beyond the **entry candle's extreme** | VISUAL, REPEATED (observed 6, 6, 9, 9, 9, 10, 16.5, 17 NQ points) |
| Later teaching (R-050) | size the stop to the **recent wick distribution**, ~25 NQ points | EXPLICIT (V13/V14) |
| 80-tick figure (R-031) | a **trail**, not an initial stop — corrected in Cycle 2 | EXPLICIT (corrected) |
| Stop behind a pending-order entry | **NOT FOUND** | NOT FOUND |

## 2.7 Invalidation
- "**Anytime we see a close back inside of orb anywhere, that's an invalidation and
  you can simply exit the trade.**" (V12 05:44) — EXPLICIT.
- Before entry, the same event resets confirmation rather than ending the day:
  V12 08:49 — EXPLICIT.
- Time: the six-or-seven candle count is on the **15-minute** chart (U-04, resolved),
  independently confirmed by a clock-time statement in V13/V14 — "still within orb by
  11:30, noon". EXPLICIT + REPEATED.

## 2.8 Targets
| Element | Content | Class |
|---|---|---|
| Structural targets | prior day high/low, session extremes, liquidity pools | EXPLICIT |
| Measured-move / 1R multiples | referenced loosely; no fixed multiple taught | EXPLICIT but ISOLATED |
| The only falsifiable number found (CL-021) | "85 to 87% chance of success if you break orb and previous day highs or lows at the same time" | MARKETING CLAIM — no denominator, no sample, no period |

## 2.9 Known error in Max's own explanation
R-056: the mechanism Max gives for the MVG ("CME data-feed lag") is **technically
wrong**. Recorded because it bears on how much weight his causal explanations carry,
not on whether the pattern exists.

---

# PART 3 — CEEWILLI SPECIFICATION (studied independently)

## 3.1 Instruments and timeframes
| Element | Content | Class |
|---|---|---|
| Instrument shown in the full-strategy video | **ES1!** (S&P 500 E-mini, CME) | VISUAL, read from the chart header |
| Range-defining timeframe | 15 minutes | EXPLICIT, REPEATED |
| Execution timeframe | **1 minute** | EXPLICIT + VISUAL (watermark `ES1! (1m)`) |
| Chart timezone | UTC-4 | VISUAL |
| Tooling | his own indicator, watermark "**ORB Ultimate+ | CeeWilli x Taking Prophets**", which plots the range box projected forward, an **ORH/ORL** line, liquidity levels (**BSL**), sweep markers and **SMT w/ NQ** divergence markers | VISUAL |

## 3.2 The four-stage formalisation (his own words)
C3 17:18 — "we just wait for a **1-minute candle closure** above or below. We wait for
price to **retest**. We get a **rejection**, and then **we enter** our trade targeting
that liquidity and putting our stop loss at a low or a high."
Classification: EXPLICIT. Note that **rejection is a separate stage from retest.**

| Stage | Trigger | Class |
|---|---|---|
| 1. Break | a 1-minute **body close** beyond the ORB edge | EXPLICIT |
| 2. Retest | price returns to / into the range | EXPLICIT |
| 3. Rejection | a bar shows refusal at the level (engulfing, wick, displacement) | EXPLICIT |
| 4. Entry | **the next body close** beyond the edge after the rejection | EXPLICIT (C1 04:41) + VISUAL (Exhibit V-01) |

## 3.3 Entry — verbatim and verified
C1 04:41 — "we see the buyers come in, nice bullish engulfing candlestick… I'm just
really right here, I'm just **waiting for another body stick candle closure**. Okay, so
I get a body stick candle closure right here. Boom, it's entered in here, put our stop
loss under this low."
C1 08:59 — "the indicator is telling us to enter. **I don't enter just yet.** I want a
little bit more of a better break and a better retest." — he explicitly declines
touch-as-entry.
C4 07:39 — "wait for our retest **and** rejection of the orb with confirmation."
Exhibit V-01 (t=308s) matches these words bar for bar: engulfing bar with an upper
wick through ORH that closes back inside is NOT taken; the following bar, which closes
above ORH, IS taken.

## 3.4 Direction — how CeeWilli decides which way
CeeWilli's direction language is **magnitude/displacement-based**, not structural.
- C4 05:36 — "We don't just want a wick. **We want a lot of displacement outside of the
  orb.**" (EXPLICIT)
- He also stacks context his indicator supplies: unswept liquidity, SMT divergence with
  NQ, prior-session structure. These are **confirmation**, not the direction primitive.
- He does **not** use "confirming-block range / ORB range". (NOT FOUND.)

## 3.5 CW-01 — the one genuinely new, cheaply testable idea
**Unswept liquidity resting beyond the ORB edge predicts a fake-out on that side.**
- Evaluable at 09:45 with **zero extraction cost** (prior-session highs/lows are known).
- Verified against the Analyst's D-038 ten-feature screen (reached the edge, direction,
  W_rel, imp_R, cost/R, latency, W, day-of-week, straddle, outside-fraction): **none of
  those ten is prior-session structural context**, and D-038 screened against
  full-stop-or-not (a loss predictor) whereas CW-01 predicts **which side resolves**.
  It is therefore not a re-test of something already rejected.
- Classification: EXPLICIT (taught), UNVALIDATED (no denominator offered).

## 3.6 Stops
| Element | Content | Class |
|---|---|---|
| Stated rule | "putting our stop loss at a low or a high" / "put our stop loss under this low" | EXPLICIT |
| Which low, observed | the extreme of the **pullback/retest cluster**, not the entry bar's own low | VISUAL (Exhibit V-01) |
| Observed magnitude | **5.75 ES points** (on-screen position-tool label) | VISUAL, single example |
| Observed R:R on that trade | **2.26** (on-screen label) | VISUAL, single example |

## 3.7 Targets
"targeting that liquidity" (C3 17:18) — the target is a **named liquidity level**
(BSL/SSL, prior-session extremes), not a fixed R multiple. EXPLICIT.

## 3.8 Invalidation
Not formalised as a separate rule in the material reviewed. The only invalidation
implied is failure of the rejection to produce the confirming close. **UNKNOWN** —
recorded as a gap, not filled by analogy with Max.

---

# PART 4 — SHARED-CORE SPECIFICATION
Only elements where **both** sources are EXPLICIT, and where they agree, appear here.
Anything supported by one source alone is excluded by construction.

| # | Shared element | Max evidence | CeeWilli evidence |
|---|---|---|---|
| S1 | Range = the first **15-minute** candle of the RTH session, **wick to wick** | EXPLICIT, REPEATED | EXPLICIT, REPEATED |
| S2 | The range boundary is the only level that matters for the setup | EXPLICIT | EXPLICIT |
| S3 | Direction is declared by a **body close** beyond a boundary, not by a touch or a wick | EXPLICIT | EXPLICIT (C4 05:36) |
| S4 | The declaring close is a **signal to prepare**, not an entry | V1 22:36, V13 x3 | C1 08:59 |
| S5 | Execution happens on a **sub-minute-to-1-minute** chart, not on the declaring timeframe | EXPLICIT + VISUAL | EXPLICIT + VISUAL |
| S6 | Between declaration and entry there is a **return toward/into the range** | V10 12:50 ("looking for the next candle to just retest the orb") | C3 17:18, C1 04:41 |
| S7 | Entry is a **second, later** body event — not the first return | V13 x3 ("it's usually the next one") | C1 04:41 ("another body stick candle closure") |
| S8 | A close back **inside** the range is materially adverse | V12 05:44 / 08:49 | implied by requiring the reclaim |
| S9 | Initial stop is anchored to a **local price extreme**, not a fixed tick count | VISUAL, REPEATED | EXPLICIT + VISUAL |
| S10 | Targets are **named structural levels**, not fixed R multiples | EXPLICIT | EXPLICIT |

**Not shared, and therefore excluded from the core:** the direction *primitive*
(structure vs displacement — Part 5), SMT/NQ divergence (CeeWilli only), liquidity-sweep
context and CW-01 (CeeWilli only), the TRT three-bar pattern and the MVG (Max only),
the 15-minute six/seven-candle time stop (Max only).

---

# PART 5 — EXACT DEFINITION OF "DIRECTION", PER SOURCE

The brief asks for this precisely because our model uses a third definition neither
source uses.

## 5.1 Max — direction by *structure and persistence*
Direction is established when the boundary has been **repeatedly defended and then
closed through**, and it is **withdrawn** when price closes back inside.
Primitives Max actually names:
- "no close, no close, no close, **close**" — the level is tested and holds, then a
  body closes through. (EXPLICIT)
- TRT: bar 2 contained **inside bar 1's body**, then resolution. (EXPLICIT)
- "print through": a candle trades beyond the prior candle's extreme in the trade
  direction **and continues**. (EXPLICIT)
- Withdrawal: "Until it breaks back outside of orb there's no confirmations." (EXPLICIT)
There is **no magnitude term** anywhere in Max's direction definition. NOT FOUND.

## 5.2 CeeWilli — direction by *displacement magnitude*
Direction is established by a body close beyond the boundary **with size**.
- "We don't just want a wick. We want a **lot of displacement** outside of the orb."
  (C4 05:36, EXPLICIT)
- The magnitude is **not quantified**. He gives no threshold, no ratio, no tick count.
  → **UNRESOLVED U-11** (Part 13).
There is no persistence/repeat-test term in CeeWilli's direction definition. NOT FOUND.

## 5.3 What this means for us
The two sources use **different, non-interchangeable** direction primitives. They are
not two observations of one rule. Merging them into a single "direction strength"
number is an act of ours, not of theirs, and must be labelled as such.
Critically: **neither source uses "confirming-block range / ORB range"**, which is the
quantity our current model uses. That metric is our invention. It is not wrong because
it is ours — but it is not source-faithful, and it should not be described as
implementing what either of them teaches.

---

# PART 6 — THE EXACT RETEST / REJECTION / ENTRY SEQUENCE

**The brief's question: is it TOUCH = ENTRY, or TOUCH → REJECTION OBSERVED → ENTRY?**

**Answer: neither, exactly. It is:**

```
  BREAK          body close beyond the boundary on the execution timeframe
    ↓            (Max: 15m close = "get ready", then watch 1m/30s
                  CeeWilli: 1m body close)
  RETURN         price comes back to the boundary — and, observed, may close
    ↓            back INSIDE the range for several bars
  REJECTION      a bar refuses the level: engulfing / long wick / displacement
    ↓            THIS BAR IS NOT THE ENTRY
  RECLAIM        the NEXT body close beyond the boundary
    ↓            ← THIS IS THE ENTRY
  ENTRY
```

Evidence, per link:

| Link | Max | CeeWilli |
|---|---|---|
| Break ≠ entry | V1 22:36 "get ready"; V13 x3 "it's usually the next one" | C1 08:59 "I don't enter just yet" |
| Return happens | V10 12:50 "looking for the next candle to just retest the orb" | C3 17:18 "We wait for price to retest" |
| Return may go back INSIDE | V12 08:49 "Until it breaks back outside of orb there's no confirmations" (presupposes being back inside) | Exhibit V-01: six consecutive 1-minute closes inside |
| Rejection is a separate stage | V10 12:50 "We need to see **printage**, though. If I don't see printage, I'm not a fan." | C3 17:18 lists rejection separately from retest; C4 07:39 "retest **and** rejection" |
| Rejection bar is not the entry bar | V13 x3 | C1 04:41: engulfing bar, then "another body stick candle closure" = entry |
| Wick ≠ entry | implied by "body close" language | C4 05:36 EXPLICIT; Exhibit V-01 bar 10 |

**Therefore: TOUCH is not ENTRY, and REJECTION is not ENTRY either. Entry is the
confirming close that follows the rejection.** This is a three-bar-minimum structure
(rejection bar, confirming bar, fill), not a one-bar structure.

**Tolerances — what is NOT specified:**
- How close to the boundary the return must come. **UNKNOWN (U-12).**
- How long the return may take. Max caps the *day* at six/seven 15-minute candles
  (~11:30-noon) but gives no cap on the break→entry interval. CeeWilli gives none.
  **UNKNOWN (U-13).**
- Whether multiple retests are permitted, and whether each resets the count.
  **UNKNOWN (U-14).**
- Whether direction may flip after one side has been broken. Max's "no confirmations"
  language implies confirmation is withdrawn and can be re-earned on **either** side;
  he never says so explicitly. **UNKNOWN (U-15) — flagged because it is a live
  modelling choice, and filling it silently would be exactly the failure the mandate
  forbids.**

---

# PART 7 — INVALIDATION RULES

| Rule | Source | Class | Applies |
|---|---|---|---|
| A close back inside the ORB **exits an open trade** | Max V12 05:44 (verbatim: "Anytime we see a close back inside of orb anywhere, that's an invalidation and you can simply exit the trade") | EXPLICIT | post-entry |
| A close back inside the ORB **withdraws confirmation** | Max V12 08:49 | EXPLICIT | pre-entry |
| Confirmation can be re-earned by breaking back outside | Max V12 08:49 (direct implication of the wording) | EXPLICIT (wording) / INFERENCE (that it is unlimited) | pre-entry |
| Day-level time stop: still inside the ORB after six/seven **15-minute** candles (~11:30-noon) → stand down | Max V13/V14, U-04 resolved and independently confirmed by clock time | EXPLICIT, REPEATED | day |
| Any formal invalidation rule | CeeWilli | **UNKNOWN** — not stated in the four videos reviewed. Not filled by analogy. | — |

**Important interaction, and the crux of the audit.** Rules 1 and 2 are the *same
event* with *different consequences depending on whether you are in the trade*. Our
current model appears to treat a close back inside as globally fatal, which would
delete precisely the population that contains the taught entry. Max's own wording
separates the two cases. This must be encoded as two rules, not one.

---

# PART 8 — STOP AND TARGET CONSTRUCTION

## 8.1 Initial stop
| Source | Anchor | Class | Observed magnitudes |
|---|---|---|---|
| Max (behaviour) | beyond the **entry candle's extreme** | VISUAL, REPEATED | 6, 6, 9, 9, 9, 10, 16.5, 17 NQ points |
| Max (later teaching, R-050) | sized to the **recent wick distribution** | EXPLICIT (V13/V14) | ~25 NQ points |
| Max (R-031, corrected) | 80 ticks is a **trail**, not an initial stop | EXPLICIT | — |
| Max | a resting stop order **beyond the ORB edge** | **NOT FOUND in any video** | — |
| CeeWilli | beyond the **retest/pullback cluster extreme** | EXPLICIT + VISUAL | 5.75 ES points (one example) |

**Note the divergence, and that it is material.** Max anchors to the *entry bar*;
CeeWilli anchors to the *pullback structure*. These give systematically different R.
On Exhibit V-01 the CeeWilli stop is roughly twice the entry-bar-extreme distance.

**Note also what R-050 does to the cost argument.** Widening to ~25 NQ points gives
cost/R ≈ 0.053R against the ~0.046R reopening threshold — so on cost alone the
strategy would be borderline viable. But the Analyst's measured **gross** edge at
R>=20 is **-0.034R**. Widening destroys signal faster than it saves cost. This
**confirms** the closure against the "your stop was too tight" objection, and should
be stated as such rather than left as an open question.

## 8.2 Targets
| Source | Target | Class |
|---|---|---|
| Max | prior-day high/low, session extremes, liquidity pools | EXPLICIT |
| Max | fixed R multiple | NOT TAUGHT |
| CeeWilli | the named liquidity level being "targeted" (BSL/SSL) | EXPLICIT |
| CeeWilli | fixed R multiple | NOT TAUGHT (2.26R observed once, as an *outcome* of geometry, not a rule) |

Both sources produce **variable R by construction**. Any backtest that fixes a target
at a constant R multiple is testing a different trade from the one taught. Flagged for
Part 12.

## 8.3 Management
- Max: trail at 80 ticks (R-031, corrected classification). EXPLICIT.
- Max: exit on a close back inside the ORB. EXPLICIT.
- CeeWilli: not specified. UNKNOWN.

---

# PART 9 — VISUAL REFERENCE LIBRARY

Held as a separate file to keep the exhibits with the evidence tree:
`02_EVIDENCE/VISUAL_VERIFICATION/VISUAL_REFERENCE_LIBRARY.md`

Summary of what exists and what does not:
- **V-01 — CeeWilli C1 `_yr2oZhMPLM` t=308s.** ES1!, 1-minute, 28 May 2026, UTC-4,
  "ORB Ultimate+" indicator. Full bar-by-bar reading of break → six closes inside →
  wick-only bar → confirming close = entry; stop under the pullback cluster; on-screen
  labels `Stop: 5.75`, `Risk/reward ratio: 2.26`. **This is the decisive exhibit.**
- **V-02 — CeeWilli C1 t=292s.** Wider context frame. The apparent midline is recorded
  as PROVISIONAL INTERPRETATION only; its label was not legible.
- **Max exhibits: NOT CAPTURED this cycle.** V11 `0WddcphxAo8` ~514s and V10
  `NF0qHcXp50o` ~820s were scoped and not done. Max's side of the sequence question
  rests on explicit verbal evidence only. Recorded as a limitation, per the mandate —
  the quota is not padded with material that was not actually reviewed.

The file also carries the exact reproduction recipe, and the honest statement of the
method's resolution limits, so that no reader mistakes a geometric reading of an
800x475 render for a measurement.

---

# PART 10 — SPECIFICATION DIFF vs OUR CURRENT MODEL

| # | Element | Our current model | Max | CeeWilli | Verdict |
|---|---|---|---|---|---|
| D1 | Opening range | first 15m candle, wick to wick | same | same | **MATCH** |
| D2 | Midline used | plotted / available | plotted | plotted (provisional) | **MATCH** |
| D3 | Direction primitive | **confirming-block range ÷ ORB range** | structure & persistence ("no close, no close, close"; TRT) | displacement magnitude ("a lot of displacement") | **MISMATCH — our metric is used by neither** |
| D4 | Break = entry trigger? | treated as the start of an entry window | explicitly "get ready" only | explicitly "I don't enter just yet" | **PARTIAL MATCH** |
| D5 | Entry region | between confirmed direction and the ORB edge — i.e. price assumed to stay **outside** | price returns and may close **inside** | price returns and demonstrably closes **inside** (V-01, six bars) | **MISMATCH — material, primary** |
| D6 | Closes back inside between confirmation and entry | **0 of 2,370** | permitted; confirmation withdrawn then re-earned (V12 08:49) | permitted and typical (V-01) | **MISMATCH — primary** |
| D7 | Entry event | first touch / level cross | **the next body close after the rejection** (V13 x3) | **"another body stick candle closure"** (C1 04:41) | **MISMATCH — material** |
| D8 | Wick through the level | not distinguished from a close | body-close language throughout | explicitly excluded (C4 05:36) | **MISMATCH — material** |
| D9 | Rejection as a required, separate stage | absent | "we need to see printage" (V10 12:50) | listed as its own stage (C3 17:18; C4 07:39) | **MISMATCH — material** |
| D10 | Initial stop anchor | fixed-R / parameterised | entry-candle extreme (VISUAL), later wick-distribution ~25 pts (EXPLICIT) | pullback-cluster extreme | **PARTIAL MATCH** |
| D11 | Target | fixed R multiple | named structural level | named liquidity level | **MISMATCH — moderate** |
| D12 | Close back inside while **in** the trade | — | exit (V12 05:44) | not stated | **PARTIAL MATCH** |
| D13 | Day time stop | — | six/seven **15m** candles, ~11:30-noon | not stated | **PARTIAL MATCH** |
| D14 | Prospective continuation-vs-reversal selector | sought | **does not exist** — OCO pre-commitment to both branches | not offered | **MATCH (both absent)** |
| D15 | Prior-session liquidity context | not in D-038's ten features | not used | **CW-01**, used | **GAP — untested, not rejected** |

---

# PART 11 — MATERIAL MISMATCHES, RANKED

**M1 (primary, and sufficient on its own to invalidate the current test).**
Rows D5 + D6 + D7 + D9 are one mismatch seen four ways: our generator's entry region
presumes price stays outside the range, so the taught sequence — return, close inside,
reject, reclaim — **cannot occur in our sample at all**. The 0-of-2,370 figure is not
a finding about the market; it is a signature of the generator. Until this is fixed,
our result does not bear on what either source teaches.

**M2 (material).** D8 — wick vs body close. We do not distinguish them; CeeWilli
explicitly does, and Exhibit V-01 shows the rejection bar being declined precisely
because its close fell short. This changes which bar fills and therefore changes both
entry price and stop distance.

**M3 (material, but ours to own honestly).** D3 — our direction metric is not either
source's. It is a legitimate quantity; it is just not theirs. We should stop describing
the test as a test of "their" method on that axis.

**M4 (moderate).** D11 — fixed-R targets versus named structural targets. Both sources
produce variable R by construction. A fixed-R backtest truncates the right tail that
their geometry is designed to capture, which matters a great deal for a positive-skew,
low-hit-rate strategy.

**M5 (moderate).** D12/D7 interaction — treating a close back inside as globally fatal
conflates Max's two distinct rules and deletes the taught setup.

**M6 (gap, not a mismatch).** D15 — CW-01 has never been tested, is not covered by
D-038's ten features, and costs nothing to evaluate at 09:45.

## The user's standing question, answered directly
> "These are 2 very very successful ORB traders — this indicates that it is a valid
> working method."

It does not, and this audit does not change that. Two visible successful practitioners
is consistent with a valid method, and equally consistent with selection into
visibility, with income from teaching rather than trading, with undisclosed
discretion, and with survivorship among a large unobserved population of people using
the same rules unsuccessfully. Neither source has supplied a denominator: not a trade
count, not a period, not a sample. The single falsifiable number we found — CL-021's
"85 to 87%" — arrives with no sample and no definition of success, which makes it a
marketing claim rather than evidence.

What this audit **does** say is narrower and more useful: **we have not yet tested
what they teach.** Those are different statements, and only the second one is
actionable.

---

# PART 12 — MINIMUM SOURCE-FAITHFUL MECHANICAL SPECIFICATION

Design rule applied: **every field below is specifiable before the outcome is known**,
and every field is traceable to EXPLICIT source evidence from **both** sources, or is
marked as a declared assumption with its alternatives listed. No indicators. No
filters. No optimisation. Nothing added because it is common elsewhere.

## 12.1 Specification (SPEC-SF-1)

| # | Field | Value | Source |
|---|---|---|---|
| 1 | Instrument | as currently used (NQ / ES) | S1 |
| 2 | Range window | 09:30-09:45 ET, first 15m candle | S1, EXPLICIT both |
| 3 | Range boundaries | ORH = high, ORL = low, **wick to wick** | S1, EXPLICIT both |
| 4 | Execution timeframe | **1 minute** | S5, EXPLICIT both |
| 5 | Break | first 1m bar to **close** beyond ORH (long) or ORL (short) after 09:45 | S3, EXPLICIT both |
| 6 | Break is not an entry | no order is placed on the break bar | S4, EXPLICIT both |
| 7 | Return | after the break, price must trade back to the broken boundary. **A close back inside the range is permitted and does not cancel the setup.** | S6/S8, Max V12 08:49; V-01 |
| 8 | Rejection bar | the first bar after the return whose **close** is on the trade side of its own midpoint and which fails to close beyond the boundary | see 12.2 — DECLARED ASSUMPTION |
| 9 | Entry | at the **close of the first subsequent 1m bar that closes beyond the boundary** in the break direction (fill modelled at the next bar's open) | S7, EXPLICIT both (V13 x3; C1 04:41) |
| 10 | Initial stop — variant A | beyond the **entry bar's extreme** | Max, VISUAL REPEATED |
| 11 | Initial stop — variant B | beyond the **extreme of the return cluster** (lowest low / highest high between the break bar and the entry bar) | CeeWilli, EXPLICIT + V-01 |
| 12 | Target | the nearest **prior-session extreme** beyond the entry in the trade direction | S10, EXPLICIT both |
| 13 | Pre-entry invalidation | none, other than 15 below | Max V12 08:49 |
| 14 | Post-entry invalidation | exit at the first 1m **close back inside** the range | Max V12 05:44, EXPLICIT |
| 15 | Day time stop | abandon if no entry by **11:30 ET** | Max, EXPLICIT REPEATED (U-04 resolved) |
| 16 | Trades per day | one attempt per side; see U-14/U-15 | DECLARED ASSUMPTION |
| 17 | Costs | as currently modelled | — |

**Run variants A and B as two arms.** They are the actual disagreement between the two
sources (Part 8.1) and the difference is large enough to change R materially. Do not
average them, and do not pick the better one and call it the specification.

## 12.2 Declared assumptions (these are OURS, and are labelled)
The sources do not define these. They are set to the most conservative reading that
preserves the taught topology; each alternative is listed so the choice can be
revisited without re-reading the sources.

| ID | Assumption | Alternatives not chosen |
|---|---|---|
| A-01 | Return tolerance: price must **trade at or beyond** the boundary (touch), not merely approach it | (i) a fixed tick buffer; (ii) must close inside |
| A-02 | Rejection bar defined as in field 8 | (i) require an engulfing body; (ii) require a wick beyond the boundary; (iii) drop the rejection requirement and enter on the first reclaiming close |
| A-03 | One entry attempt per side per day | (i) unlimited re-arming; (ii) N attempts |
| A-04 | Direction may be re-earned on **either** side after a close back inside | (i) direction locks to the first side broken |
| A-05 | No maximum interval between break and entry, other than the 11:30 day stop | (i) an N-bar cap |

**A-02 is the one to be careful with.** Variant (iii) — drop the rejection requirement
and enter on the first reclaiming close — is arguably *more* source-faithful for Max,
whose language is about the reclaim rather than about a rejection bar, and it has the
advantage of adding nothing. **Recommend running A-02(iii) as the base case and
A-02 as written as a second arm.** If the two differ materially, the difference is
information; if they do not, we have removed a parameter.

## 12.3 What the re-run should and should not be allowed to conclude
- It **can** establish whether the taught entry sequence produces a different R
  distribution from the one we measured.
- It **cannot**, on its own, establish that the method is profitable, because the
  variable-R target (field 12) and the small number of qualifying days will make the
  estimate noisy. Report the R distribution, MFE/MAE, P(MFE>MAE) and effect size with
  intervals; do not report a single expectancy number as if it settled anything.
- Guard against the obvious failure mode: A-01 through A-05 are five free choices, and
  five free choices will find something. **Fix them before running, not after.**

---

# PART 13 — GENUINELY UNRESOLVED QUESTIONS

These are recorded as unresolved because the source material does not settle them —
**not** because more searching would obviously settle them. Where a resolution route
exists, it is stated.

| ID | Question | Why unresolved | Route, if any |
|---|---|---|---|
| U-11 | How much displacement is "a lot of displacement" (CeeWilli)? | Never quantified in any of the four videos | Measure his own worked examples; would give a distribution, not a rule. **Do not adopt a threshold from this.** |
| U-12 | How close must the return come to the boundary? | Neither source states a tolerance | None from the sources. A-01 is our choice. |
| U-13 | Maximum interval between break and entry? | Max caps the day, not the interval; CeeWilli caps nothing | None. A-05 is our choice. |
| U-14 | Are multiple retests permitted? Does each reset the sequence? | Not addressed | None. A-03 is our choice. |
| U-15 | May direction flip after one side has been broken? | Max's "no confirmations" wording implies yes but never says it | Watch further Max live sessions for a day where both sides break. **Not yet observed.** |
| U-16 | Does CeeWilli have any pre-entry invalidation rule? | Absent from the four videos reviewed | Review further CeeWilli material. Do **not** import Max's rule by analogy. |
| U-17 | Which stop anchor is the real one — entry bar (Max) or return cluster (CeeWilli)? | They genuinely differ | Not resolvable by more reading; it is a real disagreement between two practitioners. Test both (12.1 A/B). |
| U-18 | Is the "85-87%" claim (CL-021) about anything measurable? | No denominator, no sample, no period, no definition of success | Could be *independently* measured as a hypothesis (break of ORB and prior-day extreme simultaneously). It would be our measurement, not a verification of his claim. |
| U-19 | Does CW-01 (unswept liquidity predicts the fake-out side) carry information? | Never tested; not covered by D-038's ten features | **Cheapest open item in the programme.** Evaluable at 09:45 at zero extraction cost. |
| U-20 | Do either of them trade the midline? | Max plots and refers to it; CeeWilli's chart shows a mid-height level whose label was not legible (V-02) | Re-capture V-02 at a timestamp where the label is readable. |

---

# CLOSING NOTE ON SCOPE AND METHOD

- No course, indicator, membership or data was purchased.
- No paywall, login, bot check or technical restriction was bypassed. The
  youtubetotranscript.com Cloudflare challenge was encountered and **not** circumvented.
- Every quotation in this document comes from captions or audio of a video that was
  actually played. Nothing here rests on a title, a description, a search snippet or a
  third-party summary.
- Where a video or a frame could not be reviewed, that is recorded as a limitation
  (Part 9, Max exhibits) rather than filled with an assumption.
- No quantitative analysis or backtest was performed by the Research Agent. The
  measured figures cited (-0.034R gross at R>=20; the ~0.046R cost threshold; the
  0-of-2,370 count; D-038's ten features) are the Analyst's, reproduced for the purpose
  of comparison and not re-derived here.
