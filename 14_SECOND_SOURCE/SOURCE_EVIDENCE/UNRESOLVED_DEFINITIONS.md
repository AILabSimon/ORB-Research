# UNRESOLVED DEFINITIONS
Ranked by whether the answer could materially change the Analyst's next decision.

## TIER 1 — could change which candidate is tested first, or invalidate a result

### U-01 — Is there ANY prospective discriminator between continuation and reversal?
Max poses this exact question himself (V2 13:26: "How do I know if it's a reversal versus a
breakout?") and answers it with 1-minute market structure (R-024, R-025), not with anything
ORB-derived. He also sells an "advanced ORB indicator [that] will show you the actual breakouts
versus the reversals" (V2 33:18) — i.e. the discriminator is closed-source.
**Why it matters:** F1 and F4 fire on the same bar sequence in opposite directions. If there is no
discriminator, they cannot both be "the strategy", and testing either in isolation risks reporting
an artefact of which one happened to be tested.
**What would resolve it:** a video in which Max, *before* the outcome, states which of the two he is
taking and why. V8's blind bar-replay segment (EX-13/EX-14) is the closest: there he takes the
breakout first, books it as a loss, and only then takes the reversal. That sequencing is itself a
candidate rule — *always take the break; if it fails, take the reversal* — and it is testable.
**Status:** PARTIALLY RESOLVED by inference from EX-13/EX-14. Flagged as inference, not as a rule.

### U-02 — What is a "retest"?
Named as one of only two patterns he trades (R-015) and used as the entry in F3 and in the confirmed
reversal F4b, but explicitly never defined ("Very, very tough to understand break and retests. I
could give you an entire class", V2 43:29).
**Missing:** proximity tolerance to the level, whether a wick touch counts, whether a close beyond
is required to resume, and the maximum number of bars between the break and the retest.
**Why it matters:** it is the difference between a fill at the ORB level and a fill many points away.

### U-03 — Touch or close, at the stop?
V8 14:52 says both in one sentence: "the break back into orb is where you close your trade. If we
break back in **and we close** in this zone..."
**Why it matters:** on a 15-minute chart this is the difference between being stopped on a wick and
surviving the bar. It will dominate the measured expectancy of MC-1.

### U-04 — The six-or-seven-candle rule: which timeframe, and what is "really broken"?
"My rule of thumb is six or seven candles ... if we haven't really broken outside of orb" (R-020).
The timeframe is **inferred** from the fact that he is on the 15-minute chart. The phrase "really
broken" is never defined — wick breach, body close, or a subjective "meaningful" break.
**Why it matters:** at 15 minutes, 6–7 candles takes the clock to roughly 11:15–11:30 ET; at 1
minute it is 09:51. Those are completely different hypotheses.

### U-05 — Does the failed breakout's extreme become the stop on the reversal?
**Never stated anywhere.** It is the obvious choice and it is exactly the kind of "common ORB
convention" this project forbids importing silently. The Analyst must invent it and label it.

## TIER 2 — needed for a clean test but unlikely to change the direction of the finding

### U-06 — Daylight saving and session templates
No evidence at all. Max works in US Eastern wall-clock time and never discusses DST, half-days,
holidays, or CME session templates. The Analyst must define these and record them as Analyst decisions.

### U-07 — Order type
Never stated in any teaching video. Live, both market orders and resting pending/stop orders are used
(V6 02:07, V7 07:16), and the pending orders are what cause entries without a body close (C-01).

### U-08 — Scale-out fractions
TP1 / TP2 / runners are named (R-016, R-017) but the size split is never given. Live he trims
"one con" at a time from variable position sizes.

### U-09 — What is a "confirmation candle" / "does the candle confirm the previous candle"?
V3 05:16 lists this as one of his confirmations and never defines it. The only enumeration anywhere
is V8's "four levels of candlestick confirmation" (R-008), which is a *sequence* (lower low, lower
high, lower low, full-bodied close outside ORB), not a single-candle test.

### U-10 — "Perfect candle"
The Phase 0 report listed "perfect candle" as a term requiring definition. **In the nine videos
reviewed, "perfect candle" is never used as a defined term.** He says "perfect three bar", "perfect
bounce", "perfect entry", "a perfect looking one". Recorded as NOT CONFIRMED rather than unresolved.

### U-11 — The Asia session anchor
Given three incompatible ways in one sentence (R-029). Not definable from the evidence.

### U-12 — Can the range ever be redrawn?
No evidence that it is. Different sessions get their own range (18:00 ET futures, 03:00 ET London),
but within a session the range appears fixed once drawn. Recorded as "no evidence of redrawing"
rather than "never redrawn".

## TIER 3 — noted, low decision value

### U-13 — 5-minute and 30-minute variants
Acknowledged as things other people do (V1 07:23), never used. Not a Max variant.

### U-14 — Options-specific mechanics
Strike selection, DTE, and premium behaviour are never discussed in any ORB context. He sells puts
on Robinhood, separately from the futures work (V2 34:20). No options ORB execution detail exists.

### U-15 — Whether favourable examples require holding through drawdown Max would not tolerate live
Strong indication that they do: V8's runner-to-the-close examples sit alongside live sessions where
he trails a stop five or six times in ten minutes and is repeatedly "edged out" (EX-08: "I got edged
four times"). The taught examples and the live risk behaviour are not compatible.
**Testable:** measure maximum adverse excursion after entry for the EOD-exit variant of MC-1 and
compare it with the ~20-point (80-tick) stop he actually runs (R-031).

---

# CYCLE 2 STATUS CHANGES (RR-002, 2026-09-12)

- **U-01 — prospective continuation-vs-reversal discriminator: CLOSED AS A CONFIRMED NEGATIVE.**
  No *selector* exists in the public material. What exists is a **conditional pre-commitment**
  covering both branches (R-036, P-1), gated by an objective print-through (P-2) and an objective
  invalidation (P-3), with an asymmetric latency rule for counter-trend trades (R-043). The source
  forecloses the question himself: "There's no there's no correct answer" (V12 37:09). The one
  artefact that claims to make the distinction — the Advanced ORB indicator — publishes no logic and
  is a paid subscription; it was not purchased (CL-020).
- **U-02 — "print through": RESOLVED** (R-009, P-2). **"Retest": still UNRESOLVED**, and V12 36:39
  shows why — Max lists the retest as one of several equally valid entries rather than defining it.
- **U-04 — six-or-seven-candle timeframe: RESOLVED as 15-minute** (V12 19:37 + 28:24). The rule also
  gains a quantified second branch (≈15 points either side, V12 28:55) and an action instruction
  ("play the confirmed break") that contradicts R-021 — see C-11.
- **U-05 — does the failed breakout's extreme become the stop on a reversal: still NOT STATED.**
  However the question is now largely superseded for boundary entries: R-040 gives a source-supported
  stop (beyond the entry candle's extreme) that does not require this invention.
- **U-07 — order type: PARTIALLY RESOLVED.** Live entries are market, by hand (R-038). Limits are
  used on retests and fill badly (R-039). Exactly one resting entry order is set anywhere in twelve
  videos, at a non-ORB level, with its type unstated (EX-21). A pre-placed stop order beyond the ORB
  boundary was **NOT FOUND**.
- **U-08 — scale-out fractions: PARTIALLY RESOLVED.** "You should be at least 80% of your position
  gone already" (V10 24:18) — isolated, but it is the only number ever given.
- **U-16 (new) — the level rule behind cross-instrument confirmation (R-042).** The *structure*
  (gate NQ on the paired index) is repeated; the levels are hand-chosen each day. The Analyst must
  supply a level rule and label it as an Analyst construct.
- **U-17 (new) — Fibonacci 78.6% as a target (R-048).** Appears in one session only. Flagged so it
  cannot enter a specification quietly.
