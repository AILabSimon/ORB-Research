# CEEWILLI PRIMARY DOCUMENT AUDIT — "THE ORB PLAYBOOK"
Research Agent · 2026-09-20 · source: *The ORB Playbook*, Mind Over Markets / @ceewillii,
10 pages, free PDF. Read in full (text + page images). All quotations verbatim.

**Status: this is the strongest CeeWilli source we have.** It is written by him, it is
structured as a specification rather than commentary, and it states rules the videos
only gestured at. It **materially changes** the CeeWilli specification.

Classification key: **EXPLICIT** · **STRONGLY IMPLIED** · **EXAMPLE-DEPENDENT** ·
**DISCRETIONARY** · **UNKNOWN**.

---

# 1. INDEPENDENT RECONSTRUCTION

## 1.1 Foundation
| Element | Content | Class |
|---|---|---|
| Session / open | New York, **09:30-09:45 EST** | EXPLICIT |
| ORB window | the **first 15-minute candle** | EXPLICIT |
| Construction | "The high of that candle = ORH. The low = ORL." | EXPLICIT — **high/low, i.e. wick to wick. "Body" is never used for the range.** |
| Midline | **absent from this document entirely** | UNKNOWN (video C4 04:05 marks one) |
| Instrument | **not stated.** "$50K funded account" implies prop futures | UNKNOWN |
| Core idea | break above ORH → buy; below ORL → sell | EXPLICIT |

## 1.2 Chart timeframes — a direct conflict with our current spec
| Where | Timeframe | Class |
|---|---|---|
| Backtest instruction, Day 2 | "Go back through the last 20 trading sessions **on a 5-min chart**. Find every valid setup" | **EXPLICIT** |
| Entry 02 Pro Tip | "a **1-min or 5-min** fair value gap at the ORB level" | EXPLICIT |
| Entry 03 step 1 | "obvious swing highs/lows **on the 15-min chart**" | EXPLICIT |
| VRC-01 (video) | ES1! **1-minute** | VISUAL |
**The playbook's own testing instruction is 5-minute. Our spec executes on 1-minute.**
Unresolved — see U-23.

## 1.3 Pre-market analysis — a real, mechanisable checklist
> "**What You Need Pre-Market** ✓ Previous session high & low marked ✓ New Week Opening
> Gap noted ✓ Key fair value gaps on 5m & 15m ✓ Overall market bias (bullish or bearish)"
> "**What You're Watching at Open** ✓ First 15-minute candle forming ✓ **Volume on the
> breakout candle** ✓ Where price is relative to liquidity ✓ Which ORB entry model is
> setting up"

| Item | Mechanisable? | Class |
|---|---|---|
| Previous session high/low | **yes** | EXPLICIT |
| New Week Opening Gap | **yes** | EXPLICIT |
| Key FVGs on 5m and 15m | **yes** (FVG has a standard 3-bar definition) | EXPLICIT |
| Overall market bias | **no method is given anywhere in the document** | DISCRETIONARY |
| Volume on the breakout candle | concept EXPLICIT, **threshold UNKNOWN** | EXPLICIT / UNKNOWN |

## 1.4 The four entry models — explicitly enumerated and risk-ranked
| # | Model | Risk | "Best used when" |
|---|---|---|---|
| 01 | Straight Break | **Very High** | "Strong momentum candle, high volume — **use sparingly**" |
| 02 | **Break & Retest** | **Low-Medium** | "Price breaks, pulls back to ORB level, rejects — **highest probability**" |
| 03 | Liquidity Sweep | Medium | "Price sweeps a session high/low before reversing in your direction" |
| 04 | Rejection Inside ORB | Medium | "Fake breakout of one side — fade it and target the opposite ORB level" |

### 1.4.1 THE SOURCE NAMES ITS OWN PRIMARY MODEL, AND TELLS YOU TO TEST IT ALONE
> Entry 02 header: "**HIGHEST PROBABILITY** … **BEST ENTRY** … This is **the money
> entry**."
> 7-Day plan, Day 2: "**Backtest Entry 2 (Break & Retest) only.** Go back through the
> last 20 trading sessions … Find every valid setup, mark entry, stop, and target."
> Day 5-6: "**Focus on Entry 2 only. Master one entry before adding complexity** — this
> is the rule that separates consistent traders from everyone else."
> Day 7 / After: "**If your backtesting shows a consistent edge on Entry 2**, you're
> ready to start trading with small size."
Class: **EXPLICIT and repeated three times.** The source's own instruction is to isolate
Entry 02 and measure it alone. That is precisely what the programme should do.

## 1.5 Entry 01 — Straight Break (VERY HIGH RISK, "use rarely")
| Step | Rule | Class |
|---|---|---|
| 1 | ORB defined by the close of the first 15-min candle | EXPLICIT |
| 2 | "a **full-bodied, high-volume** breakout candle … **not a wick, not a slow grind.** You want to see conviction." | EXPLICIT (concept) / UNKNOWN (thresholds) |
| 3 | "Enter at market on the breakout candle **or next open**. … **Don't chase it more than one candle — the edge is gone.**" | **EXPLICIT — a hard latency cap of one candle** |
| 4 | "**Stop just below the ORB level**" | **EXPLICIT — the stop is the ORB edge, not a swing** |
| 4 | "**If price returns back inside the ORB, the setup is invalidated.**" | **EXPLICIT — this is CeeWilli's own invalidation rule** |
| 4 | "Target the previous session high/low or key fair value gap" | EXPLICIT |
| — | "This entry gets new traders in trouble. The market frequently fakes breakouts. … skip this entry until you are [experienced]" | EXPLICIT fence |

## 1.6 Entry 02 — Break & Retest (the primary model)
| Step | Verbatim | Class |
|---|---|---|
| 1 | "Let price break the ORH (bullish) or ORL (bearish). **You're not entering here — just watching and confirming the break is real.**" | EXPLICIT that the break is not an entry; **"real" is not defined in this model** |
| 2 | "Price breaks out and **pulls back to the level it just broke.** Institutions are re-accumulating before the next leg. You want to see this happen." | EXPLICIT — the pullback is **mandatory** |
| 3 | "**The critical step.** Price retests the level **and rejects it.** On a bullish setup, **the ORH now acts as support.** That rejection is your entry trigger." | EXPLICIT — rejection is a separate, required step; **and the geometry is a support flip, price on the correct side** |
| 4 | "**Stop just beyond the retest** — target the next liquidity level. Tighter stop, more conviction. … previous session high/low, new week opening gap, or the next key fair value gap." | EXPLICIT |
| Pro tip | "Pair the retest with a **1-min or 5-min fair value gap at the ORB level** … FVG + ORB retest at the same level is one of the strongest confluences" | EXPLICIT, but framed as **confluence, not a requirement** |

**No candle count is given for the pullback. None. Anywhere.**

## 1.7 Entry 03 — Liquidity Sweep
| Step | Verbatim | Class |
|---|---|---|
| 1 | "Previous session high/low, previous day high/low, obvious swing highs/lows on the 15-min chart. These are your liquidity targets." | EXPLICIT |
| 2 | "Price **wicks through** the key level — taking out stop losses. … It happens fast, **usually in 1-3 candles**." | EXPLICIT, with a **numeric bound from the source** |
| 3 | "After the sweep, a **strong reversal candle closes back on the correct side of the level.** That candle is your entry trigger." | **EXPLICIT — and this is the document's only mechanical definition of a rejection candle** |
| 4 | "Stop goes **just beyond the extreme of the wick.** If price continues past that point, the thesis is wrong. **Target the opposite ORB level** or next liquidity zone." | EXPLICIT |
| — | "**The sweep itself is not the entry — the rejection of the sweep is.**" | EXPLICIT |

## 1.8 Entry 04 — Rejection Inside the ORB (fake breakout)
| Step | Verbatim | Class |
|---|---|---|
| 1 | "Price pushes toward the ORH or ORL but doesn't commit. **It wicks through and closes back inside the range.**" | EXPLICIT — the fake is defined as a **wick** through, then a close inside |
| 2 | "**The candle body must close back inside the range. A wick above with the body still outside is NOT a fake — wait for the close.**" | EXPLICIT |
| 3 | "Failed bullish = enter short, **target ORL.** Failed bearish = enter long, target ORH. Your stop sits **just beyond the fake breakout extreme.**" | EXPLICIT |
| — | "A liquidity sweep above the ORH that fails = fake breakout + liquidity sweep. **Entries 3 and 4 together = maximum confluence.**" | EXPLICIT |
| — | Common mistake: "Entering before the candle closes back inside the ORB. **Wait for the close.**" | EXPLICIT |
| — | "There's nothing more bullish than a failed bearish move. Nothing more bearish than a failed bullish move." | EXPLICIT — identical to Max R-022, independently stated |

## 1.9 Risk, targets and management — the largest single gap in our spec
| Rule | Verbatim | Class |
|---|---|---|
| **Minimum R:R** | "**Minimum 1:2 R:R. Never take a trade unless your target is at least 2x your stop loss distance.**" | **EXPLICIT — a hard pre-trade GATE, not a preference** |
| Position risk | "Never risk more than 1% … On a $50K funded account, that's $500 max per trade" | EXPLICIT |
| Stop defined first | "Define your stop before you enter. Know exactly where you're wrong before you're in the trade. **No exceptions.**" | EXPLICIT |
| **Break-even** | "**Move to break even once at 1:1.** When price moves your stop distance in profit, move your stop to entry." | **EXPLICIT and fully mechanical** |
| Partials | "**consider** locking in half at 2R and letting the rest run" if the target is 4R away | **DISCRETIONARY** ("consider") |
| Daily loss limit | "**Stop trading after two losses in a day.**" | EXPLICIT and mechanical |
| No averaging | "Never add to a losing trade … If your stop hits, the trade is done" | EXPLICIT |
| Trailing | **not mentioned anywhere** | UNKNOWN |

## 1.10 No-trade conditions in this document
> "You don't need to trade all four entries every day. … **One good trade beats four
> forced trades every time.**" · Entry 01 "use sparingly" / "skip this entry until you
> are [experienced]" · "Stop trading after two losses in a day."

**The document contains no market-state no-trade filter** — no "choppy", no "no clear
structure", no earnings-gap rule. Those came from the videos (C1 02:06, C2 11:18, C2
13:51) and are **not** corroborated here.

## 1.11 Worked examples
**There are none.** No dated trade, no instrument, no price, no outcome, no R achieved.
The four diagrams are **schematic illustrations drawn for the guide**, not screenshots
of real sessions. I have not counted bars off them and they are not evidence of bar
counts. Recorded as a limitation: this document supplies **rules**, not **examples**.
Our only real CeeWilli worked example remains VRC-01 (video, ES1! 1m, 28 May 2026).

---

# 2. DOES THE STATE MACHINE NEED CHANGING? — YES

Current shared core: `RANGE_SET → BREAK → RETEST → RECLAIM → ENTRY`.
The document requires **two additional states** and **one redefinition**.

### NEW STATE — `DRAW` (pre-market, before RANGE_SET)
The target level must be identified **before** the entry decision, because the 1:2 gate
(§1.9) cannot be evaluated without it. Marked pre-market: previous session high/low,
NWOG, key 5m/15m FVGs, previous day high/low, 15m swing highs/lows. This is a real
state, not decoration — it can veto the trade.

### NEW STATE — `RR_GATE` (at the entry decision, before the order)
`distance(entry → selected draw level) >= 2 × distance(entry → stop)`, else **NO TRADE**.
EXPLICIT, numeric, and it **reduces** trade count.

### REDEFINITION — `RECLAIM` is wrong for CeeWilli; the state is `REJECTION`
The document never describes a reclaim. Entry 02's geometry is a **support flip**: after
the break, "**the ORH now acts as support**" — price is on the correct side and rejects
*from* the level. The mechanical form is given explicitly in Entry 03 and carries over:
"a strong reversal candle **closes back on the correct side of the level**."
v2.1's S3 label "RECLAIM / REJECTION" conflates two different geometries.

### NOT required as separate states
`BIAS` (no method given — discretionary), `DISPLACEMENT` (a quality of the break
candle, not a state), `ACCEPTANCE` (the word never appears), `STRUCTURE` (only in the
Entry-03 liquidity sense).

**Revised CeeWilli machine:**
`DRAW (pre-market) → RANGE_SET → BREAK → PULLBACK → REJECTION → RR_GATE → ENTRY`

---

# 3. AUDIT OF THE 1-MINUTE BREAK RULE

**v2.1 says: CeeWilli BREAK = first 1-minute body close outside the ORB. This is only
half right, and the timeframe is contradicted.**

What the document actually requires:
- Entry 02 step 1 requires **"confirming the break is real"** — EXPLICIT that the break
  is qualified, but **the criterion is not stated in Entry 02**.
- The only stated break-quality criterion is in **Entry 01**: "**full-bodied,
  high-volume** … **not a wick, not a slow grind** … conviction", reinforced by the
  open checklist item "**Volume on the breakout candle**".
- Entry 04 supplies the negative case: a **wick** through with a close back inside is a
  **fake**, not a break.

**Ruling.** Body-close-outside is necessary (Entry 04 makes a wick explicitly
insufficient) but the document adds **body dominance** and **volume** as quality terms.
**Neither is quantified and I am not inventing a threshold.**
- Record `body/range` of the break candle and `volume / rolling-20-median volume` as
  **diagnostic columns**, no threshold, no filter.
- The timeframe is **unresolved**: the document's own backtest instruction is **5-min**
  (Day 2), the videos execute on **1-min**. Run both. See U-23.

---

# 4. AUDIT OF THE RETEST RULE — v2.1 IS WRONG HERE

**Question: does Max's ">= 2 interacting candles" apply to CeeWilli? NO.**
The document gives **no candle count for the pullback anywhere**. Max's ordinal rule was
derived from Max's words ("retest, retest", "the second retest candle", "retest, doji
retest") and there is **no CeeWilli equivalent**. Applying it to CeeWilli is
unsupported. **It must be moved out of the shared core into the Max variant only.**

Answers to the nine questions as asked:

| Question | Answer | Class |
|---|---|---|
| Is a retest mandatory? | **Yes, for Entry 02** — "Wait for the pullback… You want to see this happen." Not for Entry 01. | EXPLICIT |
| Can one candle qualify? | **The document does not exclude it.** No count is given. | UNKNOWN — do not impose a count |
| Must multiple candles interact? | **No such requirement exists for CeeWilli.** | UNKNOWN |
| Must price touch the exact ORB boundary? | "pulls back **to the level it just broke**"; the ORH then "**acts as support**" → interaction with the level is required; an exact-tick touch is not stated | STRONGLY IMPLIED |
| Can price close back inside? | **Not in Entry 02's described geometry** — the level acts as support, price stays on the correct side. And Entry 01 says a return inside **invalidates**; Entry 04 makes a body close inside the trigger for the **opposite** trade. | **See the contradiction below** |
| How deep may the pullback go? | **Not stated.** | UNKNOWN |
| Retest vs failed breakout? | Entry 04: a **wick** through + body close back inside = fake. Entry 02: body close outside first, then a pullback that **holds** the level. | EXPLICIT |
| What turns retest into rejection? | Entry 03's mechanical form: "a strong reversal candle **closes back on the correct side of the level**". Entry 02: "Price retests the level **and rejects it**." | EXPLICIT (03) / STRONGLY IMPLIED (02) |
| Is rejection separate from reclaim? | **There is no reclaim in this document.** Rejection is the entry trigger and it is a single candle. | EXPLICIT |

## 4.1 ⚠ THE MATERIAL CONTRADICTION — playbook vs VRC-01
| | Playbook (written) | VRC-01 (his own video, ES1! 1m, 28 May 2026) |
|---|---|---|
| Pullback geometry | ORH **acts as support**; price holds outside | **six consecutive 1m closes back inside the ORB** |
| A close back inside after a real break | Entry 01: "**the setup is invalidated**"; Entry 04: trigger to trade the **opposite** way | followed by a long entry on the reclaim |

Two readings, and **the document does not settle which is right**:
- **(i)** Entry 04's fake is defined as a **wick** through — "It **wicks through** and
  closes back inside" — so it may not cover the case where a genuine **body close
  outside** happened first. VRC-01 had that body close first. Under this reading the two
  are compatible and VRC-01 is a deep Entry-02 retest.
- **(ii)** Entry 01's invalidation is unconditional — "If price returns back inside the
  ORB, the setup is invalidated" — in which case VRC-01 contradicts the playbook.

**I am not choosing.** This is **U-22**, and it is the single highest-value open
question for CeeWilli because it decides whether the VRC-01 population exists at all.
**Run it as two arms** (§10). One worked example must not silently become the rule, and
neither must one sentence of a free PDF.

---

# 5. ENTRY — confirmed, with one addition

| Element | Document | vs v2.1 |
|---|---|---|
| Signal event | the **rejection candle** — "a strong reversal candle closes back on the correct side of the level" (03); "that rejection is your entry trigger" (02) | **CONFIRMED** |
| Decision time | that candle's **close** | **CONFIRMED** |
| Is a further candle required? | **No.** Nothing in the document requires a candle after the rejection. | **CONFIRMED** — CeeWilli has no print-through; that is Max's |
| Order type | "Enter **at market**" (stated for Entry 01; nothing contrary elsewhere) | CONFIRMED |
| Execution price | close of the rejection candle; model at the next bar's open | CONFIRMED (fill convention is ours) |
| Can the next candle invalidate the signal? | **Yes** — a close back inside the ORB invalidates (Entry 01), with no grace period stated | CONFIRMED |
| **New** | **the RR_GATE must pass before the order is sent** | **MISSING from v2.1** |

---

# 6. STOP AND INVALIDATION — U-16 IS CLOSED

**They are separate concepts and the document treats them separately.**

| Model | Stop | Class |
|---|---|---|
| 01 Straight Break | "just below the **ORB level**" | EXPLICIT — **the ORB edge**, contradicting v2.1's claim that CeeWilli never uses it |
| 02 Break & Retest | "just beyond the **retest**" | EXPLICIT — **confirms CW-S1** |
| 03 Liquidity Sweep | "just beyond the **extreme of the wick**" | EXPLICIT |
| 04 Rejection Inside | "just beyond the **fake breakout extreme**" | EXPLICIT |

**Invalidation — CeeWilli's own, no longer imported from Max:**
> Entry 01: "**If price returns back inside the ORB, the setup is invalidated.**"
> Entry 04: "**The candle body must close back inside the range.**" (close, not touch)
> Entry 03: "If price continues past that point, **the thesis is wrong**." (stop = thesis)

**U-16 is CLOSED.** CeeWilli's invalidation is a **close back inside the ORB** — the same
event as Max's, arrived at independently. v2.1's note "apply Max's rule and label it as
ours" must be deleted; it is now CeeWilli's own rule, EXPLICIT.

---

# 7. TARGETS — HIERARCHY NOW EXPLICIT, AND ONE v2.1 CLAIM IS FALSE

**Draw-on-liquidity hierarchy (all EXPLICIT):**
1. Previous session high / low (01, 02, 03)
2. Previous day high / low (03)
3. New Week Opening Gap (02, pre-market checklist)
4. Key fair value gaps, 5m and 15m (01, 02, pre-market checklist)
5. Obvious swing highs/lows on the 15-min chart (03)
6. **The opposite ORB level** — Entry 04 "target the other ORB level"; Entry 03 "Target the opposite ORB level or next liquidity zone"

> **v2.1 states CeeWilli's targets are "not ORB-derived, never". That is CONTRADICTED.**
> It is true for Entries 01 and 02; it is **false** for Entries 03 and 04, where the
> opposite ORB level is the stated target.

**The 1:2 gate changes what a "no target" case means.** The Analyst reports SPEC-12
yields no target on 31.8% of trades, and that this subset carries all the apparent
gross. Under the document those are **not trades at all** — "Never take a trade unless
your target is at least 2x your stop loss distance." **This disposes of RR-003's K3
motivated-reasoning risk**: the suspicious subset should never have been generated.

**Management, both new:** break-even at 1:1 (EXPLICIT, mechanical); partials at 2R of a
4R target (DISCRETIONARY — "consider"); no trailing rule anywhere.

---

# 8. HTF BIAS — investigated aggressively, and the answer is negative

The pre-market checklist contains "**Overall market bias (bullish or bearish)**" and the
document then **never mentions it again**. It is not a step in any of the four models.
No method is given: not structure, not highs/lows, not closes, not liquidity, not FVG,
not trend, not premium/discount, not previous-session behaviour. Ten pages, one bullet.

**Ruling: HTF bias remains DISCRETIONARY and is NOT mechanisable from this document.**
What remains discretionary, precisely: *the single binary judgement "am I bullish or
bearish overall today", formed before the open by an unstated method.*

Two things follow, and I am not dropping it just because it is hard to code:
1. The videos use it as a **veto** (C4 07:08 "we did not have it break in the direction
   of our bias. So we do not take this trade."). The **playbook does not** — none of the
   four models gates on it. So the veto is video-only, and the documented method is
   bias-free. **Test bias-free**, and record that the live trader is therefore *more*
   selective than the arm we measure.
2. The mechanisable parts of his pre-market work are the **liquidity levels**, not the
   bias — and those now do real work through the RR_GATE, which is a far stronger
   constraint than a direction veto.

---

# 9. WORKED EXAMPLES AND NO-TRADE EXAMPLES

**None exist in this document.** No dated trade, no instrument, no entry/stop/target
prices, no outcome, no R achieved, and no no-trade example. The four diagrams are
schematics drawn for the guide; I have not treated them as chart evidence and have not
counted bars from them.

This matters for §10: the document is **rule-rich and example-poor**, the exact inverse
of the video corpus. Our only CeeWilli worked example is still **VRC-01**, and §4.1 is
now the open question about whether it is even the same model.

---

# 10. DELTA TABLE vs RESEARCH_CURRENT v2.1

| # | v2.1 rule | Document evidence | Verdict | Required change |
|---|---|---|---|---|
| 1 | ORB = first 15m candle, wick to wick | "first 15-minute candle … high = ORH, low = ORL" | **CONFIRMED** | none |
| 2 | Session 09:30-09:45 ET | "9:30-9:45 AM EST" | **CONFIRMED** | none |
| 3 | Execution on 1-minute | Day 2: "**on a 5-min chart**"; Pro tip "1-min or 5-min" | **CONTRADICTED** | run **1m and 5m** arms (U-23) |
| 4 | Break = 1m body close outside | body close necessary (04), plus "full-bodied, high-volume", "confirming the break is real" | **MODIFIED** | add body/range and relative-volume **diagnostics**; **no threshold** |
| 5 | Direction = displacement magnitude | "full-bodied … not a wick, not a slow grind" | **CONFIRMED, still unquantified** | keep U-11 open |
| 6 | HTF bias veto, non-mechanisable | one checklist bullet; **not a step in any model**; no method | **MODIFIED** | **remove the veto**; test bias-free; record §8 |
| 7 | Retest = >= 2 interacting candles (shared core) | **no count given anywhere** | **CONTRADICTED** | **move the >=2 rule to the MAX variant only** |
| 8 | Closes back inside permitted and not fatal | Entry 01 "**invalidated**"; Entry 04 body close inside = trade the **opposite** way; Entry 02 = support flip | **CONTRADICTED / UNRESOLVED** | **U-22 — two arms** (§4.1) |
| 9 | S3 = RECLAIM / REJECTION | no reclaim exists; rejection = "closes back on the correct side of the level" | **MODIFIED** | rename state to **REJECTION**; use the Entry-03 form |
| 10 | Entry at rejection-candle close | "that rejection is your entry trigger"; "that candle is your entry trigger" | **CONFIRMED** | none |
| 11 | No further candle after rejection | nothing requires one | **CONFIRMED** | none |
| 12 | Stop beyond the retest-cluster extreme | Entry 02: "**just beyond the retest**" | **CONFIRMED** | none |
| 13 | CeeWilli stops are never the ORB edge | Entry 01: "just below the **ORB level**" | **CONTRADICTED** | correct the text (Entry 01 only) |
| 14 | CeeWilli invalidation UNKNOWN; Max's imported | "**If price returns back inside the ORB, the setup is invalidated**" | **RESOLVED** | **close U-16**; relabel as CeeWilli's own |
| 15 | Targets never ORB-derived | Entries 03/04 target the **opposite ORB level** | **CONTRADICTED** | qualify: true for 01/02, false for 03/04 |
| 16 | No fixed R minimum | "**Minimum 1:2 R:R. Never take a trade unless…**" | **CONTRADICTED** | **add the RR_GATE** — hard pre-trade filter |
| 17 | No management rules | "**Move to break even once at 1:1**" | **MODIFIED** | add BE-at-1R as an arm |
| 18 | One attempt per side per day | "**Stop trading after two losses in a day**" | **MODIFIED** | add the two-loss day stop |
| 19 | Three CeeWilli models; sweep-reversal excluded | **four** models; 03 and 04 are **distinct** | **MODIFIED** | four models; 02 is primary |
| 20 | Straight-break excluded for futures (C2 13:20) | "Very High" risk, "use sparingly", "skip this entry" — fenced but **not excluded** | **MODIFIED** | keep excluded from the primary arm; note the fence is softer here |

**Bias check, as the brief requires.** Of the twenty deltas, the ones that change trade
count are #7 (removes an unsupported *restriction* → raises count), #8 (unresolved,
either way), #16 (**cuts** count, hard), #18 (**cuts** count). The net direction is
**more selective**, and the single largest change (#16) is the one that cuts hardest.
Nothing here was adopted because it removes losses; #16 was adopted because it is a
numbered rule on a page headed "Never take a trade unless".

---

# 11. KNOWN-WORKING-STRATEGY PREMISE — what this document does and does not license

It licenses re-testing, because a **material representation defect is now proven from
primary source**: the programme has been generating trades the author's own written rule
forbids (R:R < 1:2), and measuring a model (Entry 02) mixed with populations the author
separates into three other models.

It does **not** license any claim that the method works. The document contains **no
performance data at all** — no win rate, no sample, no period, no equity curve, not one
dated trade. It is a free lead-generation guide ending in a mentorship offer, and it
says so: "This guide is for educational purposes only." The "highest probability" label
on Entry 02 is the author's assertion, unevidenced.

Every change proposed above is justified by a verbatim rule from the document. None is
justified by its effect on results, and none has been tested.
