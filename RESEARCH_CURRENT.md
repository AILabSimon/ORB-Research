# RESEARCH_CURRENT.md — SOURCE-FAITHFUL V2 SPECIFICATION
Research Agent · v2.0 · 2026-09-20 · supersedes all earlier specification material
Sources: @MaxOptionsTrading (V1-V14) · @CeewilliTradez (C1-C4). Evidence IDs in §J.

Status of MODEL V1: retired as a representation of the source strategy.
This document is the specification the Analyst builds MODEL V2 from.

---

# A. CURRENT RESEARCH CONCLUSION

**The two sources describe the same five-state machine and differ in exactly two
places: what counts as the break, and how the entry fires.** Everything else in the
sequence is shared and explicit.

The reconstruction that closes the audit is this. Both authors place a candle
**between** the retest and the entry, and both say so in their own words:

- Max V8 11:50 — "the one-two punch is always going to be **the fail and the retest**
  … the second retest candle **that failed and closed outside of orb**, the second this
  candle made a newer low, **that's the retest confirmation and this was your entry**."
- Max V13 01:04 — "It's **not** the candle you think you should enter on. It's usually
  **the next one**."
- CeeWilli C1 04:41 — after the rejection, "I'm just waiting for **another body stick
  candle closure** … Boom, it's entered in here."

Put together with the reclaim requirement (Max V12 08:49 "Until it breaks back outside
of orb there's no confirmations"), the shared machine is:

**BREAK → RETEST (may close back inside the ORB) → RECLAIM candle (closes back
beyond the edge) → ENTRY.**

The two divergences:

| | MAX | CEEWILLI |
|---|---|---|
| **Break** | a **15-minute** body close outside the ORB (R-006) | a **1-minute** body close outside the ORB, with visible displacement (C3 17:18, C4 05:36) |
| **Entry fires** | on the **next** candle trading **through the reclaim candle's extreme** — an intrabar stop-order trigger ("print through", R-009, V11 08:34) | at the **close of the reclaim candle itself** — an end-of-bar trigger (C1 04:41) |

They are **one bar apart**, and Max's "it's usually the next one" is exactly that one
bar. This is not a hybrid; it is two variants of one machine, and they must be tested
as two arms.

**Corrections I am making to my own earlier record.** In the 20.1 Representation Audit
I wrote that the R-band result "confirms the closure against the *your stop was too
tight* objection." The Analyst is right in IMPLEMENTATION_AUDIT_20_1 §7 and I withdraw
it: that result varied R by **selecting days with wider ranges** (a change of
population), whereas changing the stop **rule** changes the payoff on the **same**
population. They are different experiments and the first does not answer the second.
**The stop question is open.** Separately, the Analyst's uncertainty map row 7 records
"Max ~1R"; that is not supported — see §F.2.

**What this does not claim.** Nothing here says the trade works. Max's own falsifiable
number (R-027 / CL-021, "85 to 87%") arrives with no sample, no period and no
definition of success. Neither author has ever published a denominator.

---

# B. SHARED-CORE STATE SEQUENCE

Every state below is EXPLICIT in **both** sources. Variant-specific detail is in §C/§D.

| State | Name | Entered when | Notes |
|---|---|---|---|
| **S0** | RANGE_SET | 09:45:00 ET | ORH = max(high), ORL = min(low) over 09:30:00-09:44:59, **wick to wick**. Midline = (ORH+ORL)/2. Pre-market excluded. (R-001, R-002, R-003, R-004, R-005; C1 02:33, C4 04:05) |
| **S1** | BREAK | first completed candle whose **close** is beyond ORH (long bias) or ORL (short bias) | **Candle length is variant-specific** (§C.1 / §D.1). Establishes a **candidate direction**; does **NOT** authorise entry. (R-006, R-049; C1 08:59) |
| **S2** | RETEST | after S1, price trades back to the broken edge | Price **may** close back inside the ORB, and **may do so repeatedly**. This does **not** cancel the setup. (Max V12 08:49; CeeWilli V-01: six consecutive 1m closes inside) |
| **S3** | RECLAIM / REJECTION | first 1-minute candle after S2 whose **close** is again beyond the broken edge in the S1 direction | This is the object Max calls "the retest candle that failed and closed outside of orb" (V8 11:50) and the candle CeeWilli's "body stick candle closure" refers to. **A wick beyond the edge is NOT sufficient** (C4 05:36; visually verified, V-01 bar 10). |
| **S4** | ENTRY | **variant-specific** — see §C.3 / §D.3 | Max: next candle prints through S3's extreme. CeeWilli: at S3's close. |
| **X** | INVALIDATION (pre-entry) | see §B.1 | Reachable before S4 in both variants — this is the property V1 lacked. |

## B.1 Pre-entry invalidation — the rule that makes V2 testable
A close back inside the ORB **withdraws confirmation**; it does not end the day. The
machine returns to a state where a further reclaim can re-arm it.
> Max V12 08:49 — "**Until it breaks back outside of orb there's no confirmations.**"

Mechanically: while in S2, a 1-minute close back inside the ORB resets S3-eligibility;
the setup remains live and S3 can occur later. The **day** ends per §B.2.

This is distinct from the **post-entry** rule (§F.3), which exits an open trade. They
are the same event with different consequences and **must be coded as two rules**.

## B.2 Day-level stop
Abandon the day if no entry has occurred by **11:30 ET** — six to seven 15-minute
candles from 09:45. (R-020; timeframe resolved in cycle 3 and independently confirmed
by a clock-time statement in V14 18:07.) EXPLICIT, REPEATED.

## B.3 Direction bias gate — CeeWilli only, do NOT apply to Max
CeeWilli vetoes trades whose break direction disagrees with a pre-open 4h/1h bias
(C2 02:02, C4 07:08 "We **did** have a break to the downside, but we did not have it
break in the direction of our bias. **So we do not take this trade.**"). Max has no
equivalent. See §D.2 — it is carried as a flag, not as a filter, in the first run.

---

# C. MAX SPECIFICATION

Instrument NQ/MNQ. Chart timezone ET (note: V14 charts are Central, 08:30 open).

## C.1 Break (S1) — 15-minute close
A completed **15-minute** candle whose body closes outside ORH/ORL.
> V1 22:36 — "We have a candle closure outside of the orb low or a candle closure
> outside of the orb high **on the 15-minute chart. That's your signal.**"
> V8 06:11 — "once your candle closed **inside** of orb then that is **not** a
> confirmation for entrance for you."
Class: EXPLICIT, REPEATED, stable 2024→2026 (R-006).
**It is a signal to prepare, not to enter** — V1 22:36 calls it "the casting the bat
signal. **Get ready.**" (R-049.)
*Known divergence from live behaviour:* V6 07:16 and V2 16:37 show wick-triggered and
pre-09:45 entries. That is Max's discretion, not his rule; it is NOT specified here
(C-01 in the contradiction register).

## C.2 Direction — structure and persistence, NOT magnitude
Max's direction primitive is that the level is **repeatedly defended and then closed
through**, and it is **withdrawn** by a close back inside.
- "no close, no close, no close, **close**"
- TRT three-bar: bar 2 ranges **inside** bar 1's body, then bar 3 resolves (R-013, R-051)
- withdrawal: V12 08:49 (§B.1)
There is **no magnitude term anywhere** in Max's direction language. NOT FOUND.
**Do not use confirming-block magnitude here.** The Analyst's own decomposition shows
that variable is ~0.78 correlated with block **body ÷ W**, i.e. it is a *displacement*
composite — which is CeeWilli's concept, not Max's, and it moved gross by nothing.

## C.3 Entry (S4) — print through the reclaim candle's extreme
Once S3 has occurred, place a **stop order** at the S3 candle's extreme in the trade
direction (its high for a long, its low for a short). Entry occurs when the **next**
candle trades through that level.
> V10 24:18 — "as soon as I see a candle **flip up or print through the previous
> candle**, I'm going long."
> V11 08:34 — "there was my entry … I want to see the print through — **the next
> candle's wick hit 308 and then go**."
> V8 11:50 — "the second retest candle that failed and closed outside of orb, the
> second this candle made a newer low, **that's the retest confirmation and this was
> your entry**."
Class: EXPLICIT, REPEATED (R-009, R-010).
Execution timeframe: **1-minute** (V1 22:56 permits 1/2/3/4/5m — "who cares" — so the
timeframe is a free parameter; fix it at 1m and do not search it).
**Model non-fills.** If the following candle does not trade through the level, there is
no entry. Max demonstrably misses fills (R-039: V11 39:30 "you're making me get in
eight points away from [where] I wanted it").

## C.4 Stop
| ID | Rule | Class | Observed |
|---|---|---|---|
| **MAX-S1** (base) | beyond the **S3 (reclaim) candle's opposite extreme** | EXPLICIT, REPEATED (R-040): V10 14:08 "Just that previous stop loss at candle low… Risking a total of nine points"; V11 39:05 "Stop loss goes under the candle" | NQ 6, 6, 9, 9, 9, 10, 16.5, 17 pts |
| **MAX-S2** (alt) | sized to the **recent wick distribution** — if the last ~20 candles carry 15-20 pt wicks, use ~25 pts and size down to micros | EXPLICIT but ISOLATED (R-050, V13 05:57) | ~25 pts NQ |
| — | entry back to the broken ORB edge | EXPLICIT but belongs to a **different entry** (the boundary entry, R-041/V12 31:58). Do **not** attach it to the print-through entry. | — |
| — | 80 ticks | this is a **trail**, not an initial stop (R-031/R-053, corrected) | — |
**Which of MAX-S1 / MAX-S2 is "the" rule is UNRESOLVED (§I, U-17).** Run both.

## C.5 Target — no fixed multiple; two different trade families
**Do not impose 1R. Max does not teach 1R.**
- **Continuation family (this spec):** no price target. Hold until invalidation,
  trimming at each counter-structure point, full exit on the second.
  > V12 29:25 — "Here's your trim, here's your exit. **You ride it until the
  > invalidation.**" (R-045, EXPLICIT REPEATED)
  Named liquidity beyond the entry: **previous day's high/low** (R-027, V8 08:15).
- **Failed-break / reversal family (NOT this spec):** midline first, then the
  **opposite** ORB edge, then runners (R-016, R-017, R-023). These are the ORB-derived
  targets, and they belong to the fade, not the continuation. Recorded so they are not
  mis-assigned.
Consequence for the Analyst: **R is variable by construction. Measure natural MFE
first; do not fix a target in the first run.**

---

# D. CEEWILLI SPECIFICATION

Instrument in the full-strategy video: **ES1!** (CME). Execution chart **1-minute**,
timezone UTC-4, his own "ORB Ultimate+" indicator plotting ORH/ORL, projected range
box, liquidity levels (BSL/SSL) and SMT-vs-NQ markers.

## D.1 Break (S1) — 1-minute close, with displacement
> C3 17:18 — "we just wait for a **1-minute candle closure** above or below."
> C4 05:36 — "**We don't just want a wick. We want a lot of displacement** outside of
> the orb."
Class: EXPLICIT. **The displacement magnitude is never quantified** (§I, U-11).
**For the first run, do not implement a displacement threshold.** Record displacement
(close-beyond-edge ÷ W, and body ÷ W) as a **diagnostic column** so a threshold can be
examined later without having been chosen in advance.

## D.2 Direction — displacement, plus an HTF bias veto
Two components, both his:
1. **Break quality** = displacement magnitude (C4 05:36). Unquantified.
2. **Bias veto** — a pre-open 4h/1h directional bias; a break against it is not taken.
   > C4 07:08 — "We **did** have a break to the downside, but we did not have it break
   > in the direction of our bias. **So we do not take this trade.**" (C2 02:02.)
The bias is discretionary and not mechanisable from the source. **Do not implement it.**
It is recorded because it means the CeeWilli arm as tested is *less* selective than
what he trades, and results should be read with that in mind.
No-trade conditions he states (all evaluable at or before 09:45): no clear HTF
structure (C2 02:02, C1 02:06), choppy (C2 11:18), overnight earnings gap (C2 13:51).

## D.3 Entry (S4) — at the close of the reclaim candle
> C1 04:41 — "nice bullish engulfing candlestick … I'm just waiting for **another body
> stick candle closure**. Okay, so I get a body stick candle closure right here.
> **Boom, it's entered in here**, put our stop loss under this low."
> C2 03:34 — the whole frame in one line: "**Wait, confirmation, execute.**"
> C1 08:59 — "the indicator is telling us to enter. **I don't enter just yet.**"
Class: EXPLICIT + VISUALLY VERIFIED (§G, case VRC-01).
Fill convention: entry at the S3 candle's close, modelled at the **next candle's open**.

**His other two entry models are excluded, on his own instruction and on our evidence:**
- *Break-and-go* (no retest): C2 13:20 — "**Do not recommend doing that on futures
  though because you will get [screwed] most likely.**" Options only.
- *Fake-out / sweep → reversal from inside the ORB* (C3 17:18): a distinct strategy,
  and the closest object we have already measured (TSUGI-02) came in at **−0.105R,
  negative 5/5**. Not part of V2.

## D.4 Stop — beyond the swing formed by the retest
> C1 05:07 "put our stop loss **under this low**"; C1 10:16 "just under the low";
> C3 11:42 "above this high"; C4 07:39 "below a fair value gap or **below a lower high
> or a higher low**."
> C1 10:42, the reasoning — "price needs some room to breathe … if we sweep this, then
> we're probably just most likely just completely wrong about the trade."
**CW-S1:** stop beyond the **extreme of the retest cluster** — the lowest low (long) /
highest high (short) between the S1 break candle and the S3 reclaim candle inclusive.
Class: EXPLICIT + VISUAL. Observed once at **5.75 ES points** (V-01 on-screen label).
Note this is systematically **wider** than MAX-S1 and therefore a different R.

## D.5 Target — external liquidity, never ORB-derived
> C1 05:07 — "target either Asian high or … the 15-minute liquidity … or all the way
> to the previous day high." C1 16:18 — an unfilled new-week opening gap as "very good
> drawing liquidity." C4 07:39 — "target draw on liquidity … **at least a 1:2 or 1.5**."
Reported R on his worked examples: **2.75R** (C1 09:51), **3.75R** (C1 12:53), ~3R
(C1 22:21), 1:3-1:5 (C4 07:08); V-01 on-screen **2.26**.
Implementation: nearest **prior-session extreme** (prior-day high/low; overnight/Asian
extreme) beyond the entry in the trade direction. **Do not impose a fixed multiple.**
(Options exits are a premium percentage, C2 08:10 — not applicable to futures.)

---

# E. LONG / SHORT ENTRY SEQUENCE (implementation-grade)

Notation: `ORH`, `ORL` from §B S0. `W = ORH − ORL`. All candles **completed**. No
lookahead: every condition is evaluated only on bars at or before the decision bar.

## E.1 LONG — MAX variant
```
1  at 09:45 compute ORH, ORL, mid
2  S1  first completed 15m candle with close > ORH            → dir = LONG, t_break
3  S2  after t_break, on 1m: wait for low <= ORH              (touch of the edge)
       closes back below ORH are PERMITTED and are counted, not fatal
4  S3  first 1m candle after S2 with close > ORH              → reclaim candle r
5  S4  arm a BUY STOP at high(r) + 1 tick
       if the next 1m candle trades >= that level  → FILL at that level
       if it does not                              → no trade this attempt; return to 3
6  stop  MAX-S1: low(r) − 1 tick      |  MAX-S2: entry − wick_size(last 20 candles)
7  exit  no fixed target. Trail/trim at counter-structure; hard exit on the first 1m
         close back below ORH (§F.3). Day stop 11:30 ET. Flat at session close.
```
SHORT is the exact mirror: `close < ORL`, `high >= ORL`, `close < ORL`, SELL STOP at
`low(r) − 1 tick`, stop at `high(r) + 1 tick`.

## E.2 LONG — CEEWILLI variant
```
1  at 09:45 compute ORH, ORL, mid
2  S1  first completed 1m candle with close > ORH             → dir = LONG, t_break
       record displacement diagnostics (close-beyond/W, body/W) — no threshold applied
3  S2  after t_break, on 1m: wait for low <= ORH
       closes back below ORH are PERMITTED and are counted, not fatal
4  S3  first 1m candle after S2 with close > ORH              → reclaim candle r
5  S4  ENTER at close(r); model the fill at open(r+1)
6  stop  CW-S1: min(low) over [t_break … r] − 1 tick
7  exit  no fixed target; nearest prior-session extreme above entry as the reference
         level for MFE measurement. Hard exit on a 1m close back below ORH (§F.3).
         Day stop 11:30 ET. Flat at session close.
```
SHORT is the exact mirror.

**The two variants share S0, S2, S3, the invalidation and the day stop. They differ
only at S1 (15m vs 1m), S4 (stop order on the next bar vs close of the reclaim bar)
and the stop anchor. Run them as two arms. Do not blend them.**

---

# F. STOP / TARGET SPECIFICATION

## F.1 Stop — four constructions exist in the corpus; three are attached to different entries
| ID | Construction | Attached to | Class | Use in V2 |
|---|---|---|---|---|
| MAX-S1 | beyond the reclaim candle's opposite extreme | the print-through entry | EXPLICIT, REPEATED (R-040) | **base, Max arm** |
| MAX-S2 | recent wick distribution (~25 pts NQ) | the print-through entry | EXPLICIT, ISOLATED (R-050) | **second Max arm** |
| CW-S1 | beyond the retest-cluster extreme | CeeWilli's close entry | EXPLICIT + VISUAL | **base, CeeWilli arm** |
| — | entry back to the broken ORB edge | the **boundary** entry (R-041) | EXPLICIT | **not used** — different trade |
| — | 0.5·W / the midline | nothing in the source | **our invention (V1)** | **retired** |
| — | 80 ticks | a **trail** | demonstrated (R-053) | not an initial stop |

**UNRESOLVED, and I will not invent a resolution (§I U-17):** MAX-S1 and MAX-S2 are
both explicit, both from Max, and materially different (≈9 pts vs ≈25 pts). Max also
says outright, in the same corpus, "There's no price targets for me. There's no stop
losses for me. All there is is candlestick structure" (V1 41:00). Test both; report
both; do not pick the better one and call it the specification.

## F.2 Target
**No fixed R multiple is taught by either author for the continuation trade.**
- Max, continuation: hold to invalidation, trim at counter-structure (R-045). The
  ORB-derived targets (midline → opposite edge) belong to the **failed-break/fade**
  family and must not be attached here (R-016/R-017/R-023).
- CeeWilli: external liquidity; stated floor "at least a 1:2 or 1.5" (C4 07:39);
  worked examples 2.26R-3.75R.
- **Correction to IMPLEMENTATION_AUDIT_20_1 row 7:** "Max ~1R" is not supported by any
  rule in the ledger. It should read *"no fixed target; hold to invalidation"*.
- The programme needs credible 2R+ economics. That is a **programme requirement**, not
  a source rule. Measure natural MFE first, unselected, gross, both variants.

## F.3 Post-entry invalidation (distinct from §B.1)
> Max V12 05:44 — "**Anytime we see a close back inside of orb anywhere, that's an
> invalidation and you can simply exit the trade.**" (Also V8 14:52.)
Implement as: exit at the close of the first 1-minute candle that closes back inside
the range. CeeWilli states **no** post-entry invalidation rule (§I, U-16) — apply the
same rule to his arm for comparability and **label it as ours**, not his.
*Ambiguity on the record:* V8 14:52 mixes "break back in" with "close in this zone" —
touch vs close is not settled by the source. We use **close**. Declared assumption.

## F.4 Re-entry
Explicitly permitted and encouraged after a stop-out (R-019, V8 25:55; V4 19:01).
**Not implemented in the first run** — one attempt per side per day — because
unlimited re-entry is a free parameter. Recorded so it is not mistaken for absent.

---

# G. VISUAL REFERENCE CASES

Full library and the reproducible capture recipe:
`14_SECOND_SOURCE/OUTPUTS/VISUAL_REFERENCE_LIBRARY.md`.

| ID | Source | What it establishes | Strength |
|---|---|---|---|
| **VRC-01** (mandatory) | CeeWilli C1 `_yr2oZhMPLM` t=308s · **ES1! 1-minute, 28 May 2026, UTC-4** | Break above ORH → **six consecutive 1m closes back inside the range** → a bar whose **wick** pierces ORH and closes back inside is **NOT** taken → the **next** bar closes above ORH and **IS** taken. Stop under the retest cluster; on-screen `Stop: 5.75`, `R:R 2.26`. | **Strong.** Directly read from the chart; matches C1 04:41 bar for bar. |
| VRC-02 | CeeWilli C1 t=292s, wider frame | Context: range box projected forward, ORH line, BSL above. The apparent midline is **PROVISIONAL** — the label was not legible. | Context only. |
| VRC-03 | Max V8 11:50-12:20 | The "one-two punch": fail → retest → the candle that closed outside → new extreme = entry. | **Verbal only.** No chart capture. |
| VRC-04 | Max V11 08:34 / V10 24:18 | Print-through entry, stated live and pre-announced. | **Verbal only.** No chart capture. |

**Max's visual evidence is weaker and I am not going to pretend otherwise.** V11
`0WddcphxAo8` ~514s and V10 `NF0qHcXp50o` ~820s were scoped for bar-by-bar capture and
**were not captured**. Max's side of the sequence rests on explicit, repeated *verbal*
evidence. That is good evidence; it is not visual confirmation, and it is not recorded
as such.

Stage 8 visual validation should check V2's generated entries against **VRC-01 first**:
if the model cannot reproduce that sequence, it is still not the source strategy.

---

# H. ANALYST ACCEPTANCE TESTS
Behavioural checklist. **V2 must pass all of these on a small sample before any
historical economics are computed.** Each is source-supported; the source is named.

| # | Test | Pass condition | Source |
|---|---|---|---|
| H1 | **Range** | ORH/ORL come from 09:30:00-09:44:59 only, wick to wick, pre-market excluded. A 30-minute range anywhere in the code fails the test. | R-001/002/003/004; C1 02:33 |
| H2 | **Break stored independently** | `t_break` exists as its own field on every candidate and is never equal to the entry bar by construction. | audit §1 T2 |
| H3 | **Break ≠ entry** | Fraction of entries on the break bar itself = **0%**. (V1 was 52.1%.) | R-049; C1 08:59 |
| H4 | **Real touch** | 100% of entries have `low <= ORH` (long) / `high >= ORL` (short) at some bar in [t_break, entry). Proximity bands are removed entirely. (V1 was 26.1%.) | §B S2 |
| H5 | **Inside closes occur and do not force entry** | The count of 1m closes back inside the ORB in [t_break, entry) is **> 0 on a non-trivial share of days**, and days with such closes still produce entries. If this is 0 everywhere, the generator is still wrong. | Max V12 08:49; VRC-01 (six) |
| H6 | **Wick-only interaction is NOT an entry** | Construct the VRC-01 pattern (wick beyond edge, close inside, next bar closes beyond): the model must skip the wick bar and take the next. | C4 05:36; VRC-01 |
| H7 | **Reclaim precedes entry** | Every entry has an S3 candle with `close` beyond the edge, at or before the entry bar. | V8 11:50; C1 04:41 |
| H8 | **Pre-entry invalidation is reachable** | There exist candidates that reach S2/S3 and are **reset** by an inside close before any entry, and some days end with no trade for that reason. If this set is empty, invalidation is still dominated by entry and V2 has repeated V1's error. | audit §3 |
| H9 | **No lookahead** | Every decision at bar *i* uses only bars <= *i*. Entry fills use the next bar's open (CeeWilli arm) or an intrabar stop level (Max arm), never the same bar's close. | method |
| H10 | **Max arm models non-fills** | A non-zero count of armed-but-unfilled print-through orders. If every armed order fills, the trigger is being evaluated wrongly. | R-039 |
| H11 | **Stop is decoupled from W** | No stop in V2 is a function of `W`. MAX-S1/CW-S1 are candle/swing extremes; MAX-S2 is a wick statistic. | §F.1 |
| H12 | **Variants are separate** | Max and CeeWilli arms are reported separately end to end. No blended arm exists in the output. | §A |
| H13 | **Day stop** | No entry after 11:30 ET. | R-020 |
| H14 | **VRC-01 reproduction** | Replay the 28 May 2026 ES session (or the nearest equivalent in our data) and confirm the CeeWilli arm produces an entry at the reclaim bar, not earlier. | §G |

**Reporting discipline for the first run** (restating what is already programme method,
because it is easy to lose in a re-build): gross before net; full unselected
population; continuation and failed-break reported separately; natural MFE/MAE
distributions before any target is imposed; no parameter search.

---

# I. GENUINE UNRESOLVED QUESTIONS
Recorded because the **source** does not settle them — not as a to-do list.
**Do not fill any of these silently.** Where V2 needs a value, §I marks it DECLARED.

| ID | Question | Status | Handling in V2 |
|---|---|---|---|
| U-11 | How much displacement is "a lot of displacement" (CeeWilli)? | Never quantified in C1-C4 | **No threshold.** Recorded as a diagnostic column only. |
| U-12 | How close must the retest come to the edge? | Neither author states a tolerance | **DECLARED:** touch of the exact edge (`low <= ORH`). The alternative (a tick buffer) is rejected because it reintroduces V1's proximity error. |
| U-13 | Maximum interval between break and entry? | Max caps the **day** (11:30), not the interval; CeeWilli caps nothing | **DECLARED:** none, other than the day stop. |
| U-14 | Are multiple retests permitted? Does each re-arm? | Not addressed by either | **DECLARED:** yes, re-arming is permitted within the day; one **filled** entry per side per day. |
| U-15 | May direction flip after one side has broken? | Max's "no confirmations" wording implies yes; he never says it | **DECLARED:** yes — both sides remain eligible. Flagged as the choice most likely to matter. |
| U-16 | Does CeeWilli have any invalidation rule? | Absent from C1-C4 | Max's rule is applied to his arm **and labelled as ours**. Not imported as his. |
| U-17 | MAX-S1 (≈9 pts) or MAX-S2 (≈25 pts)? | Both explicit, both Max, materially different; V1 41:00 says he uses neither | **Two arms.** Not resolvable by more reading. |
| U-18 | Is CL-021 / R-027 ("85-87% if you break ORB and prior-day H/L at the same time") about anything measurable? | No sample, no period, no definition of success | Testable as **our** hypothesis; would not verify his claim. Not in V2. |
| U-19 | CW-01 — does unswept liquidity beyond the edge predict which side fakes out? | Never tested; **not** covered by D-038's ten features; predicts *which side resolves*, not stop-vs-not | **Cheapest open item in the programme.** Evaluable at 09:45, zero extraction cost. Analyst's call. |
| U-20 | Does CeeWilli trade the midline? | C4 04:05 marks it; VRC-02's mid-height level was not legible | Not in V2. Re-capture needed. |
| U-21 | Is Max's reclaim candle the stop anchor, or the entry candle? | V11 39:05 "stop loss goes under the candle" — which candle is ambiguous | **DECLARED:** the reclaim (S3) candle. They are adjacent; the difference is small but real. |

**Not researchable from public evidence:** Max's pre-ORB entries (R-032) — he states
they are undisclosed.

---

# J. SOURCE / EVIDENCE REFERENCES

**Primary corpus.** Max V1-V14 (14 videos); CeeWilli C1-C4 (4 videos). Every quotation
in this document comes from captions or audio of a video that was actually played.
Nothing rests on a title, description, search snippet or third-party summary. No
course, indicator, membership or data was purchased; no paywall, login or bot check was
bypassed (the youtubetotranscript.com Cloudflare challenge was encountered and **not**
circumvented).

**Detailed evidence lives elsewhere and is not duplicated here:**
- `Trading/Max Options Trading ORB/02_EVIDENCE/RULE_EVIDENCE_LEDGER.csv` — 56 rules
  with classification, source, timestamp, contradictions, mechanical readiness.
- `.../02_EVIDENCE/CONTRADICTION_REGISTER.md` — C-01…C-14.
- `.../02_EVIDENCE/CLAIMS_REGISTER.csv` — 26 claims, none with a denominator.
- `.../02_EVIDENCE/EXAMPLE_TRADE_REGISTER.csv` — 22 worked examples.
- `.../01_SOURCES/TRANSCRIPTS/` — V1-V12 evidence extracts; V13/V14 in
  `04_HANDOFF_TO_ANALYST/CYCLE3_LATEST_VIDEO_REVIEW.md`.
- `14_SECOND_SOURCE/OUTPUTS/SOURCE_ASSESSMENT_CEEWILLITRADEZ.md` — C1-C4.
- `14_SECOND_SOURCE/OUTPUTS/REPRESENTATION_AUDIT_20.1.md` — the 13-part audit.
- `14_SECOND_SOURCE/OUTPUTS/VISUAL_REFERENCE_LIBRARY.md` — VRC cases + capture recipe.

**Rule IDs cited in this document:** R-001 R-002 R-003 R-004 R-005 R-006 R-009 R-010
R-013 R-016 R-017 R-019 R-020 R-023 R-027 R-031 R-039 R-040 R-041 R-045 R-049 R-050
R-051 R-053. **CeeWilli timestamps cited:** C1 02:33 04:41 05:07 08:59 09:51 10:16
10:42 12:53 16:18 22:21 · C2 02:02 03:34 08:10 11:18 13:20 13:51 · C3 02:34 11:42
17:18 · C4 04:05 05:36 07:08 07:39.

**Core rule.** This specification is not an attempt to make ORB work. It exists so the
Analyst tests the trade the sources actually teach.
