# RESEARCH_CURRENT.md — SOURCE-FAITHFUL V2 SPECIFICATION
Research Agent · **v2.2** · 2026-09-20 · supersedes all earlier specification material
v2.1 incorporated the RR-003 rulings (retest/continuation split, MAX-S1 floor, Max
print-through trigger). **v2.2 rewrites the CeeWilli specification against his primary
document — *The ORB Playbook* (Mind Over Markets, 10pp).** Changes are marked **[v2.1]**
and **[v2.2]**. Full reasoning: RR-003 and CEEWILLI_PLAYBOOK_AUDIT.md.

**[v2.2] The four largest changes:** a hard **1:2 R:R gate** before every CeeWilli entry
("Never take a trade unless your target is at least 2x your stop loss distance"); the
**>= 2-candle retest rule is Max-only** and has left the shared core; **U-16 is closed**
— CeeWilli states his own invalidation; and the **HTF bias veto is removed**.
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

## A.1 [v2.1] TWO ENTRY MODELS, NOT ONE — the retest/continuation split

Max teaches **two** entry models and says so when asked directly. V2 v2.0 modelled only
one of them, and by letting a one-bar touch satisfy the return it was in fact producing
mostly the *other* one while scoring it as the first.

> Audience question — *what do you do if it breaks out and doesn't retest?*
> V12 36:39 — "if you're waiting for a **two candle close**, or you waiting for
> **retest**, or are you waiting for **market structure** — there's a couple different
> ways to do it … and they all have their own risk reward."
> V12 37:09 — "**you can enter right here on this close. You don't have to wait for
> this.** … **You can enter on any close outside of orb** … **There's no correct
> answer. Just make sure that you have your risk reward.**"
> V12 05:44 — two ways to long: "one, a **retracement back down to orb and then a
> bounce up**; or two … a **continuation right to the upside**."

| Arm | Return required | Source |
|---|---|---|
| **RETEST** | yes — S2 as redefined (>= 2 interacting bars) | V8 11:50, V8 14:52, V12 27:23, V12 06:46; CeeWilli C2 03:34, VRC-01 |
| **CONTINUATION** | **none** — enter on a close beyond the boundary after the break | V12 37:09, V12 05:44 branch two |

**Run them as separate arms, reported end to end. Pooled, the number describes
neither.** The continuation arm has never been tested as such and is, on the Analyst's
own figures, the majority of what V2 has been measuring.

This is R-037 on the record — *there is no single correct entry, stated by the source*.
It is the reason the answer to "what makes a retest qualify?" is **split the
population**, not **raise the threshold**. There is no threshold in the sources to
raise, and inventing one would be parameter mining.


---

# B. SHARED-CORE STATE SEQUENCE

Every state below is EXPLICIT in **both** sources. Variant-specific detail is in §C/§D.

| State | Name | Entered when | Notes |
|---|---|---|---|
| **S0** | RANGE_SET | 09:45:00 ET | ORH = max(high), ORL = min(low) over 09:30:00-09:44:59, **wick to wick**. Midline = (ORH+ORL)/2. Pre-market excluded. (R-001, R-002, R-003, R-004, R-005; C1 02:33, C4 04:05) |
| **S0-pre** | **[v2.2] DRAW** (CeeWilli only) | pre-market | Mark previous session H/L, previous day H/L, New Week Opening Gap, key 5m/15m FVGs. A real state: it can veto the trade through the RR_GATE. EXPLICIT (playbook pre-market checklist). |
| **S1** | BREAK | first completed candle whose **close** is beyond ORH (long bias) or ORL (short bias) | **Candle length is variant-specific** (§C.1 / §D.1). Establishes a **candidate direction**; does **NOT** authorise entry. (R-006, R-049; C1 08:59) |
| **S2** | RETEST | **[v2.2] MAX ONLY:** the boundary is interacted with on **at least two separate 1-minute candles** — `low_i <= ORH <= high_i` (long) — after the break candle and before the qualifying close. They need not be consecutive. | **[v2.1]** A one-bar wick to the boundary is **not** a retest: "retest, **retest**" (V8 14:52), "the **second** retest candle" (V8 11:50), "retest, **doji retest**" (V12 27:23), "**pulls back**" (C2 03:34), V-01's 8 bars. Ordinal, not numeric — there is no threshold to search. **[v2.2] CeeWilli gives no candle count anywhere in his playbook — this rule does NOT apply to him** (§D.4). Price **may** close back inside the ORB for Max (V12 08:49); for CeeWilli this is **U-22, run as two arms** (§D.5). |
| **S3** | **[v2.2]** RECLAIM (Max) / **REJECTION** (CeeWilli — there is no reclaim in his playbook, §D.6) | first 1-minute candle after S2 whose **close** is again beyond the broken edge in the S1 direction | This is the object Max calls "the retest candle that failed and closed outside of orb" (V8 11:50) and the candle CeeWilli's "body stick candle closure" refers to. **A wick beyond the edge is NOT sufficient** (C4 05:36; visually verified, V-01 bar 10). |
| **S3b** | **[v2.2] RR_GATE** (CeeWilli only) | at the entry decision | `dist(entry→draw) >= 2 x dist(entry→stop)` else **NO TRADE**. EXPLICIT and numeric: "Never take a trade unless your target is at least 2x your stop loss distance." |
| **S4** | ENTRY | **variant-specific** — see §C.3 / §D.7 | Max: next candle prints through S3's extreme. CeeWilli: at S3's close. |
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
| **MAX-S1** (base) **[v2.1: FLOORED by MAX-S2 — see R3 below]** | beyond the **S3 (reclaim) candle's opposite extreme** | EXPLICIT, REPEATED (R-040): V10 14:08 "Just that previous stop loss at candle low… Risking a total of nine points"; V11 39:05 "Stop loss goes under the candle" | NQ 6, 6, 9, 9, 9, 10, 16.5, 17 pts |
| **MAX-S2** (alt) | sized to the **recent wick distribution** — if the last ~20 candles carry 15-20 pt wicks, use ~25 pts and size down to micros | EXPLICIT but ISOLATED (R-050, V13 05:57) | ~25 pts NQ |
| — | entry back to the broken ORB edge | EXPLICIT but belongs to a **different entry** (the boundary entry, R-041/V12 31:58). Do **not** attach it to the print-through entry. | — |
| — | 80 ticks | this is a **trail**, not an initial stop (R-031/R-053, corrected) | — |
**Which of MAX-S1 / MAX-S2 is "the" rule is UNRESOLVED (§I, U-17).** Run both.

**[v2.1] R3 — MAX-S1 is floored, never raw.** `stop_distance = max(|entry − reclaim
extreme|, wick_floor)`. Max prescribes this floor himself, for exactly the
degeneracy the Analyst found (R < 0.0002 x price on 20-26% of trades): V13 05:57 —
"The previous 20 candles had 15 to 20 point wicks, but you got a five-point
stop-loss … allow that 25 point stop loss." An unfloored MAX-S1 is **half of Max's
stop rule**, not Max's stop rule.

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
**[v2.2] Rewritten against the primary document — *The ORB Playbook*, Mind Over Markets
/ @ceewillii, 10pp.** That document is rule-rich and example-free; the videos are the
reverse. Where they conflict, both readings are carried. Full audit:
`14_SECOND_SOURCE/OUTPUTS/CEEWILLI_PLAYBOOK_AUDIT.md`.

## D.0 [v2.2] FOUR models, and the source names its own primary
| # | Model | Risk (his) | In V2? |
|---|---|---|---|
| 01 | Straight Break | Very High — "use sparingly", "skip this entry" | no |
| **02** | **Break & Retest** | **Low-Medium — "the money entry", "HIGHEST PROBABILITY", "BEST ENTRY"** | **yes — the CeeWilli arm** |
| 03 | Liquidity Sweep | Medium | no (TSUGI-02 measured −0.105R, 5/5 negative) |
| 04 | Rejection Inside ORB (fake breakout) | Medium | no |

> Day 2: "**Backtest Entry 2 (Break & Retest) only.**" Day 5-6: "**Focus on Entry 2
> only. Master one entry before adding complexity.**" Day 7: "If your backtesting shows
> a consistent edge on Entry 2, you're ready to start trading."
The source's own instruction is to isolate Entry 02 and measure it alone. **The
CeeWilli arm is Entry 02 and nothing else.** EXPLICIT, stated three times.

## D.1 Timeframes — UNRESOLVED, run both
| Source | Timeframe |
|---|---|
| Playbook, Day 2 backtest instruction | "on a **5-min chart**" |
| Playbook, Entry 02 pro tip | "a **1-min or 5-min** fair value gap" |
| Video VRC-01 | ES1! **1-minute** |
**U-23. Run 1m and 5m arms.** Do not pick one. Bar size changes stop distance, and
stop distance drives the RR_GATE, so this choice is not cosmetic.

## D.2 Break — body close outside, quality unquantified
Entry 02 step 1: "Let price break the ORH (bullish) or ORL (bearish). **You're not
entering here — just watching and confirming the break is real.**" EXPLICIT that the
break is not an entry; **"real" is not defined in Entry 02.**
The only stated quality terms are in Entry 01 — "**full-bodied, high-volume** … **not a
wick, not a slow grind** … conviction" — plus the open checklist item "**Volume on the
breakout candle**". Entry 04 gives the negative case: a wick through with a body close
back inside is a **fake**, not a break.
**Implementation: body close beyond the edge is the trigger. Record `body/range` and
`volume / rolling-20-median volume` as DIAGNOSTIC COLUMNS. No threshold. No filter.**
(U-11 stays open.)

## D.3 Direction — displacement; **no HTF bias veto**
"Full-bodied … not a wick, not a slow grind" (Entry 01); "a lot of displacement outside
of the orb" (video C4 05:36). Unquantified in both. **U-11.**
**[v2.2] The HTF bias veto is REMOVED from the specification.** The playbook lists
"Overall market bias (bullish or bearish)" once, in the pre-market checklist, gives no
method for forming it, and **never gates any of the four models on it**. The veto is
video-only (C4 07:08). Test bias-free and record that the live trader is therefore
*more* selective than the arm we measure. See §I U-24 for exactly what stays
discretionary.

## D.4 Pullback — mandatory, but **no candle count**
> Entry 02 step 2: "Price breaks out and **pulls back to the level it just broke.**
> Institutions are re-accumulating before the next leg. **You want to see this happen.**"
Mandatory for Entry 02. **No count, no depth, no time limit is given anywhere in the
document.**
**[v2.2] Max's ">= 2 interacting candles" rule does NOT apply to CeeWilli** and has been
moved out of the shared core into the Max variant. It was derived from Max's words
("retest, retest"; "the second retest candle"; "retest, doji retest") and CeeWilli has
no equivalent. Imposing it on him would be our invention.

## D.5 [v2.2] ⚠ May price close back inside the ORB? — **U-22, the decisive open question**
| | Playbook | VRC-01 (his own video) |
|---|---|---|
| geometry | "the ORH **now acts as support**" — price holds on the correct side | **six consecutive 1m closes back inside** |
| a return inside | Entry 01: "**the setup is invalidated**"; Entry 04: a body close inside = trade the **opposite** way | followed by a long on the reclaim |

Two readings, and the document does not settle it:
- **(i) compatible** — Entry 04's fake is defined as a **wick** through ("It **wicks
  through** and closes back inside"), so it may not cover a case where a genuine body
  close outside came first. VRC-01 had that. Then VRC-01 is a deep Entry-02 retest.
- **(ii) contradictory** — Entry 01's invalidation is unconditional, and VRC-01
  contradicts the playbook.
**Run both arms (§E.2). Do not choose.** One worked example must not become the rule;
neither must one sentence of a free PDF.

## D.6 Rejection — a single candle, mechanically defined
Entry 02 step 3: "**The critical step.** Price retests the level **and rejects it.** On
a bullish setup, **the ORH now acts as support.** That rejection is your entry trigger."
The mechanical form is given explicitly in Entry 03 and carries over:
> "a strong reversal candle **closes back on the correct side of the level.** That
> candle is your entry trigger."
**REJECTION candle (long) = a candle that interacts with ORH (`low <= ORH <= high`) and
closes above ORH.** EXPLICIT (03) / STRONGLY IMPLIED (02).
**There is no "reclaim" in this document.** v2.1's combined "RECLAIM / REJECTION" state
conflated two geometries; the state is **REJECTION**.
*Confluence, not requirement:* "Pair the retest with a 1-min or 5-min **fair value gap**
at the ORB level for even higher conviction." Record FVG-at-level as a diagnostic flag.

## D.7 Entry — at the rejection candle's close, **after the R:R gate**
"That rejection is your entry trigger" (02); "That candle is your entry trigger" (03);
"Enter at market" (01). **No further candle is required** — CeeWilli has no
print-through; that is Max's. Fill modelled at the next bar's open (our convention).

## D.8 [v2.2] RR_GATE — a hard pre-trade filter, and the largest single change
> "**Minimum 1:2 R:R. Never take a trade unless your target is at least 2x your stop
> loss distance.**"
> "**Define your stop before you enter.** Know exactly where you're wrong before you're
> in the trade. **No exceptions.**"
`distance(entry → selected draw level) >= 2 × distance(entry → stop)` **else NO TRADE.**
EXPLICIT and numeric. It **cuts** trade count, which is the direction the programme
should be biased toward.
**It also disposes of RR-003 K3.** The Analyst's "no target on 31.8% of trades, and that
subset carries all the gross" cannot arise: those are not trades.

## D.9 Stop — per model, all explicit
| Model | Stop |
|---|---|
| 01 Straight Break | "just below the **ORB level**" |
| **02 Break & Retest** | "**just beyond the retest**" → **CW-S1 CONFIRMED** |
| 03 Liquidity Sweep | "just beyond the **extreme of the wick**" |
| 04 Rejection Inside | "just beyond the **fake breakout extreme**" |
**[v2.2] Correction:** v2.1 said CeeWilli never uses the ORB edge as a stop. False for
Entry 01. True for Entry 02, which is our arm.

## D.10 [v2.2] Invalidation — CeeWilli's own. **U-16 CLOSED.**
> Entry 01: "**If price returns back inside the ORB, the setup is invalidated.**"
> Entry 04: "**The candle body must close back inside the range**" — close, not touch.
> Entry 03: "If price continues past that point, **the thesis is wrong.**"
Exit at the first close back inside the ORB. **This is no longer Max's rule applied to
his arm for comparability — it is his own, EXPLICIT, arrived at independently.** Delete
the v2.1 note that labelled it as ours.

## D.11 Target hierarchy — explicit, and one v2.1 claim was false
1. Previous session high / low · 2. Previous day high / low · 3. **New Week Opening
Gap** · 4. Key fair value gaps, **5m and 15m** · 5. 15-minute swing highs/lows ·
6. **The opposite ORB level** (Entries 03 and 04 only).
**[v2.2] v2.1 said CeeWilli's targets are "never ORB-derived". CONTRADICTED** — true for
01/02, false for 03/04. For our Entry-02 arm, targets are external liquidity, selected
**before** entry so the RR_GATE can be evaluated.

## D.12 [v2.2] Management — new, and mechanical
| Rule | Verbatim | Class |
|---|---|---|
| **Break-even at 1:1** | "**Move to break even once at 1:1.** When price moves your stop distance in profit, move your stop to entry." | EXPLICIT, mechanical — **run as an arm** |
| Partials | "**consider** locking in half at 2R and letting the rest run" (on a 4R target) | **DISCRETIONARY** — not implemented |
| **Two-loss day stop** | "**Stop trading after two losses in a day.**" | EXPLICIT, mechanical |
| Position risk | 1% of account; "$50K funded … $500 max per trade" | EXPLICIT, not needed for R-space |
| Trailing | **absent from the document** | UNKNOWN |

## D.13 No-trade conditions in the playbook
"You don't need to trade all four entries every day … **One good trade beats four
forced trades**"; Entry 01 "use sparingly"/"skip this entry"; two-loss day stop.
**The document contains no market-state filter** — no "choppy", no "no clear structure",
no earnings-gap rule. Those are video-only (C1 02:06, C2 11:18, C2 13:51) and are **not
corroborated** here. Not implemented.

## D.14 Not in the document
Instrument (UNKNOWN — "$50K funded account" implies prop futures; videos show ES1!);
the ORB **midline** (absent entirely); any **worked example** — no dated trade, no
prices, no outcome, no R achieved, no win rate, no sample. The four diagrams are
schematics drawn for the guide and were **not** treated as chart evidence.

---

# E. LONG / SHORT ENTRY SEQUENCE (implementation-grade)

Notation: `ORH`, `ORL` from §B S0. `W = ORH − ORL`. All candles **completed**. No
lookahead: every condition is evaluated only on bars at or before the decision bar.

## E.1 LONG — MAX variant
```
1  at 09:45 compute ORH, ORL, mid
2  S1  first completed 15m candle with close > ORH            → dir = LONG, t_break
3  S2  after t_break, on 1m: require >= 2 SEPARATE bars with low <= ORH <= high
       [v2.1] two interactions, not one touch. Need not be consecutive.
       closes back below ORH are PERMITTED and are counted, not fatal
4  S3  first 1m candle after S2 with close > ORH              → reclaim candle r
5  S4  arm a BUY STOP at high(r) + 1 tick
       if the next 1m candle trades >= that level  → FILL at that level
       if it does not                              → no trade this attempt; return to 3
6  stop  MAX-S1 [v2.1, FLOORED]: entry − max( entry − (low(r) − 1 tick) , wick_floor )
         wick_floor = max wick length over the previous 20 1m candles (R-050)
         MAX-S2: entry − wick_floor  (the floor alone)
7  exit  no fixed target. Trail/trim at counter-structure; hard exit on the first 1m
         close back below ORH (§F.3). Day stop 11:30 ET. Flat at session close.
```
SHORT is the exact mirror: `close < ORL`, `high >= ORL`, `close < ORL`, SELL STOP at
`low(r) − 1 tick`, stop at `high(r) + 1 tick`.

## E.2 LONG — CEEWILLI variant  [v2.2: Entry 02 only]
```
0  PRE-MARKET (DRAW): mark previous session H/L, previous day H/L, New Week Opening
       Gap, key 5m and 15m FVGs. These are the only permitted targets.
1  at 09:45 compute ORH, ORL  (midline not used by this source)
2  S1  BREAK: first completed bar with close > ORH            → dir = LONG, t_break
       record body/range and volume/median20 as DIAGNOSTICS — no threshold applied
       no order is placed here ("you're not entering here")
3  S2  PULLBACK: price trades back to ORH (low <= ORH)
       [v2.2] NO candle count. NO depth rule. The >=2 rule is MAX-ONLY.
       U-22 ARM (a) "holds": any bar closing back inside the ORB ABORTS the setup
       U-22 ARM (b) "deep" : closes back inside are permitted (the VRC-01 reading)
4  S3  REJECTION: first bar with low <= ORH <= high AND close > ORH   → bar r
5  RR_GATE: stop = min(low) over [t_break … r] − 1 tick   (CW-S1)
            entry_px = close(r)   [fill modelled at open(r+1)]
            draw = nearest pre-marked level above entry_px
            REQUIRE (draw − entry_px) >= 2 * (entry_px − stop)   ELSE **NO TRADE**
6  S4  ENTER at market; fill at open(r+1)
7  manage  BE arm: move stop to entry once price reaches entry + 1R
8  exit    target = draw; hard exit on the first close back inside the ORB (D.10);
           day stop 11:30 ET; flat at session close; stop trading after 2 losses today
```
SHORT is the exact mirror: `close < ORL`, `high >= ORL`, rejection bar with
`low <= ORL <= high AND close < ORL`, stop `max(high)[t_break…r] + 1 tick`, draw below.

**Arms to run on the CeeWilli side:** {1m, 5m} x {U-22 (a), U-22 (b)} x {BE on, BE off}.
That is 8 cells, and every dimension is a **documented disagreement in the sources**,
not a parameter sweep. Report all 8; do not select among them.

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
| CW-S1 | beyond the retest-cluster extreme | CeeWilli's close entry | **[v2.2] EXPLICIT in the playbook** — Entry 02: "stop just beyond the retest" | **base, CeeWilli arm** |
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
- CeeWilli: external liquidity, selected **before** entry. **[v2.2] The floor is not a
  preference — it is a hard pre-trade gate:** "**Minimum 1:2 R:R. Never take a trade
  unless your target is at least 2x your stop loss distance.**" See §D.8. Note the
  **opposite ORB level** IS a target for his Entries 03/04 (not our arm) — v2.1's
  "never ORB-derived" was wrong.
- **Correction to IMPLEMENTATION_AUDIT_20_1 row 7:** "Max ~1R" is not supported by any
  rule in the ledger. It should read *"no fixed target; hold to invalidation"*.
- The programme needs credible 2R+ economics. That is a **programme requirement**, not
  a source rule. Measure natural MFE first, unselected, gross, both variants.

## F.3 Post-entry invalidation (distinct from §B.1)
> Max V12 05:44 — "**Anytime we see a close back inside of orb anywhere, that's an
> invalidation and you can simply exit the trade.**" (Also V8 14:52.)
Implement as: exit at the close of the first 1-minute candle that closes back inside
the range. **[v2.2] CeeWilli states his own, and it is the same event — U-16 is CLOSED:**
"**If price returns back inside the ORB, the setup is invalidated**" (Entry 01), and
the close-not-touch reading is confirmed by Entry 04 ("the candle body must close back
inside the range"). It is no longer labelled as ours.
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
| **H15** | **[v2.1] Retest is multi-bar** | In the RETEST arm, 100% of entries have **>= 2 separate bars** with `low <= ORH <= high` in `[t_break, entry)`. Share of entries whose entire return was a single bar = **0%**. (v2.0 run: 58% returned on the very next bar.) | RR-003 R1 |
| **H16** | **[v2.1] Continuation arm exists and is separate** | A CONTINUATION arm is built, run and reported with its own n, gross and interval. No arm pools retest and continuation trades. | RR-003 R2; V12 37:09 |
| **H17** | **[v2.1] Max's entry trigger is built** | The Max arm arms a **stop order at the reclaim candle's extreme** and fills only when the next bar trades through it — not "fill at the next bar's open". H10 must then show a non-zero non-fill count. In the v2.0 run all four arms used CeeWilli's close trigger, so **the Max entry model is still untested.** | R-009, R-039; V10 24:18, V11 08:34 |
| **H18** | **[v2.1] MAX-S1 is floored** | No trade has `R < wick_floor`. Trades with `R -> 0` and unbounded R-multiples (max 699R in the v2.0 run) must disappear. | RR-003 R3; V13 05:57 |
| **H19** | **[v2.2] RR gate is enforced** | Every CeeWilli entry satisfies `dist(entry→draw) >= 2 x dist(entry→stop)` at the moment of entry. Trades with no qualifying draw are **NO-TRADES, not no-target trades**: the "no target" bucket must be **empty**. (v2.0 run: 31.8% had no target, and carried all the apparent gross.) | Playbook §Risk: "Never take a trade unless your target is at least 2x your stop loss distance" |
| **H20** | **[v2.2] Draw is pre-marked, no lookahead** | Every target level used by the gate is one of: previous session H/L, previous day H/L, New Week Opening Gap, 5m/15m FVG, 15m swing H/L — all computable **before 09:30**. No level derived from post-entry data. | Playbook pre-market checklist |
| **H21** | **[v2.2] >=2-candle retest is Max-only** | The CeeWilli arm applies **no** candle count to the pullback. If the CeeWilli generator enforces >=2 interacting bars, it is running Max's rule on the wrong author. | §D.4 |
| **H22** | **[v2.2] U-22 runs as two arms** | Arm (a) aborts the setup on any close back inside the ORB; arm (b) permits them. Both are built and reported. Neither is selected. | §D.5 |
| **H23** | **[v2.2] Timeframe runs as two arms** | 1-minute and 5-minute CeeWilli arms both built and reported. | §D.1, U-23 |
| **H24** | **[v2.2] Break diagnostics recorded, not filtered** | `body/range` and `volume / rolling-20-median volume` are present as columns on every break. **No threshold is applied to either.** If either appears in a filter, that is parameter mining. | §D.2 |
| **H25** | **[v2.2] CeeWilli invalidation is his own** | The close-back-inside exit is labelled as CeeWilli's own rule, not Max's imported. | §D.10, U-16 closed |
| **H26** | **[v2.2] BE-at-1R runs as an arm** | A break-even arm exists ("Move to break even once at 1:1") and is reported alongside the no-BE arm. | §D.12 |
| **H27** | **[v2.2] Two-loss day stop** | No third trade is taken on a day after two losses. | §D.12 |

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
| U-11 | How much displacement / volume makes a break "real" (CeeWilli)? | **[v2.2] Still unquantified in the playbook too** — "full-bodied, high-volume … not a wick, not a slow grind"; "confirming the break is real" is never defined. | **No threshold.** Recorded as a diagnostic column only. |
| U-12 | How close must the retest come to the edge, and for how long? | **[v2.1] RESOLVED on the count, still open on depth.** The count is source-worded (>= 2 interacting candles — RR-003 R1). No author states a **depth** of pullback or a tick tolerance. | **DECLARED:** exact-edge interaction (`low <= ORH <= high`), >= 2 bars. No tick buffer (reintroduces V1's proximity error). **No depth rule** — adding one would be parameter mining. |
| U-13 | Maximum interval between break and entry? | Max caps the **day** (11:30), not the interval; CeeWilli caps nothing | **DECLARED:** none, other than the day stop. |
| U-14 | Are multiple retests permitted? Does each re-arm? | Not addressed by either | **DECLARED:** yes, re-arming is permitted within the day; one **filled** entry per side per day. |
| U-15 | May direction flip after one side has broken? | Max's "no confirmations" wording implies yes; he never says it | **DECLARED:** yes — both sides remain eligible. Flagged as the choice most likely to matter. |
| ~~U-16~~ | ~~Does CeeWilli have any invalidation rule?~~ | **[v2.2] CLOSED.** Playbook Entry 01: "If price returns back inside the ORB, the setup is invalidated"; Entry 04 confirms close-not-touch. | His own rule, EXPLICIT. Same event as Max's, arrived at independently. |
| **U-22** | **[v2.2] After a genuine body close outside, may price close back INSIDE the ORB and still be an Entry-02 retest?** | Playbook Entry 01 says a return inside **invalidates**, and Entry 04 makes a body close inside the trigger for the **opposite** trade — but Entry 04's fake is defined as a **wick** through, which may not cover a prior body close outside. VRC-01 shows six inside closes then a long. | **Two arms (a) holds / (b) deep.** The single highest-value CeeWilli question: it decides whether the VRC-01 population exists. Do not choose. |
| **U-23** | **[v2.2] 1-minute or 5-minute execution for CeeWilli?** | His own backtest instruction says "**on a 5-min chart**" (Day 2); his pro tip says "1-min or 5-min"; VRC-01 is 1-minute. | **Run both.** Bar size drives stop distance, which drives the RR_GATE — not cosmetic. |
| **U-24** | **[v2.2] Can CeeWilli's HTF bias be mechanised?** | **No.** Ten pages; "Overall market bias (bullish or bearish)" appears once, in the pre-market checklist, with **no method**, and **gates none of the four models**. | Precisely what stays discretionary: *a single binary pre-open judgement formed by an unstated method.* Test bias-free; record that the live trader is therefore more selective than the arm we measure. |
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
