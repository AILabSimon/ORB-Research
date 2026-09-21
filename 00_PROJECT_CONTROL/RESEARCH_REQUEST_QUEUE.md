# RESEARCH REQUEST QUEUE

Shared queue between Analyst Agent (requester) and Research Agent (responder).
Responses go to `04_HANDOFF_TO_ANALYST/RESEARCH_RESPONSES/RR-[ID].md`.
Detailed request files: `11_HANDOFF_TO_RESEARCH/ANALYST_RESEARCH_REQUESTS/RR-[ID].md`.

| ID | Date | Candidate/Experiment | Question (short) | Priority | Status |
|---|---|---|---|---|---|
| RR-001 | 2026-09-12 | CENSUS-01 (pre-candidate) | Minimum objective event definition for the Max opening range | BLOCKING | **INCORPORATED** — answered in full by the cycle-1 handoff |
| RR-002 | 2026-09-12 | EXP-001/006 → EXP-008 | (a) prospective discriminator (U-01); (b) initial stop behind a boundary entry | HIGH | **INCORPORATED** 2026-09-12 — rebuilt EXP-008 to the corrected MC-7 spec; see EXPERIMENT_REGISTER |
| RC-001 | 2026-09-12 | EXP-004 | Researcher challenge: opening-range width is not CL-012 | MEDIUM | **ACCEPTED** — EXP-004 re-labelled (D-005R); CL-012 then properly tested as EXP-008-G4 / EXP-009 |

---

## RR-001

```
REQUEST ID: RR-001
DATE: 2026-09-12
CANDIDATE OR EXPERIMENT: CENSUS-01 — first behavioural census (pre-candidate)
QUESTION:
  What is the minimum objectively-defined opening-range event that Max Options Trading
  actually teaches? Specifically and separately:
  (a) Range window — clock start, duration, timezone, and whether it is anchored to the
      US cash open, the futures open, or something else.
  (b) Market and instrument actually traded and demonstrated (SPX/SPY/ES/MES/NQ/MNQ; index
      vs options on index; 0DTE or otherwise).
  (c) Break definition — first touch/trade beyond the boundary, or a COMPLETED CLOSE beyond
      it, and on WHICH timeframe that close is measured.
  (d) Whether any confirmation is required beyond the break itself, and whether that
      confirmation is objective or discretionary.
  (e) How many DISTINCT strategy families exist in the source material (continuation,
      break-and-retest, failed-breakout reversal, power-hour, pre-ORB, etc.), and whether
      any is presented as the primary method versus an occasional variation.
  (f) Whether Max states a no-trade condition, and whether it is determinable in advance
      or only visible after the fact.

WHY IT COULD CHANGE THE DECISION:
  No handoff exists. The census event definition IS the experiment. Choosing 09:30-09:45
  New York, touch-based, when the source teaches (say) a 5-minute range or a close-confirmed
  break, would produce a representation failure that is indistinguishable from a genuine
  absence of edge. Items (a) and (c) alone change the event population and the measured
  continuation rate materially. Item (e) determines whether one census or several are needed
  and prevents two opposing playbooks being silently pooled. Item (b) determines whether
  Track A can be attempted at all, and whether a CFD proxy is the nearest available
  representation or an outright mismatch.

CURRENT ANALYTICAL EVIDENCE:
  None from source. Analyst has independently completed data discovery and validation only.
  No Max rule has been assumed, and none will be.

EXACT SOURCE EVIDENCE NEEDED:
  For each of (a)-(f): a direct quotation or timestamped transcript segment, with video ID
  and timestamp, plus a note on whether the rule is explicit-and-repeated, explicit-but-
  isolated, demonstrated-but-unstated, or an interpretation. Where videos conflict, state
  the conflict and the dates rather than resolving it.
  Minimum viable subset to unblock the census: (a), (b), (c). (d)-(f) can follow.

SUGGESTED VIDEOS OR PERIOD:
  Prioritise the most recent explicit "how I trade the open" / rules-explanation content
  over marketing or results content, and prefer live or recorded trade examples for (c)
  and (d), since execution convention is usually demonstrated rather than stated.

PRIORITY: BLOCKING — no substantive analysis can begin without (a), (b), (c).
STATUS: OPEN
```


---

## RR-002

```
REQUEST ID: RR-002
DATE: 2026-09-12
CANDIDATE OR EXPERIMENT: EXP-001/EXP-006 (falsified) -> EXP-008 (next construction)
QUESTION:
  (a) U-01 - is there ANY segment in which Max states, BEFORE the outcome, whether he is taking
      the breakout or the reversal, and on what observable? Is the EX-13/EX-14 sequencing rule
      ("always take the break; if it fails, take the reversal") ever STATED, or only demonstrated
      once? Is the free WealthCharts ORB indicator inspectable without purchase?
  (b) C-01 / R-031 - is the 80/70/60-tick figure ever an INITIAL stop, or only a trail? Where is
      the protective stop at the moment a pending order fills without a body close (V6 02:07,
      V7 07:16)?
WHY IT COULD CHANGE THE DECISION:
  (a) The census measured P(MFE>MAE) = 50.3-51.9% at every horizon, both directions, every year,
      two instruments. If a prospective discriminator exists, that symmetry is a REPRESENTATION
      FAILURE and F1/F4 must be retested under it. If it verifiably does not exist, F1-F4 close.
  (b) EXP-008 tests the pending-order entry at the ORB edge, whose stop is not implied by the
      range. A source-supported fixed initial stop makes EXP-008 source-faithful; its absence
      makes it an Analyst construct that can only be evidence about the concept.
CURRENT ANALYTICAL EVIDENCE:
  See 07_BEHAVIOURAL_CENSUS/RESULTS/CENSUS_FINDINGS.md and 08_EXPERIMENTS/EXPERIMENT_REGISTER.md.
EXACT SOURCE EVIDENCE NEEDED:
  Quotation + video ID + timestamp + evidence classification. A confirmed NEGATIVE for (a) is
  fully decision-relevant and should be reported as such.
SUGGESTED VIDEOS OR PERIOD:
  V8 blind bar-replay segment; 0WddcphxAo8; NF0qHcXp50o; V6 around 02:07; V7 around 07:16.
PRIORITY: HIGH - not blocking; EXP-008 proceeds in parallel.
STATUS: OPEN
```


---

## STATUS 2026-09-12 (end of cycle 2)

**No open Analyst requests.** RR-001 and RR-002 are INCORPORATED; RC-001 is ACCEPTED and actioned.

**No further request is being raised, deliberately.** The binding constraint is now arithmetic:
Max's own stated stop of 6-17 NQ points means realistic execution consumes 10.7%-32.2% of the risk
unit, breakeven needs +0.290R gross, and the best-case measured gross edge is +0.110R. No source
detail can change that. Per mandate section 25, a request whose answer cannot change a decision
should not be made.

Two items remain genuinely unresolved but are recorded as closed-for-decision rather than open:
- the Advanced ORB indicator's breakout-vs-reversal logic - paid subscription, out of scope by mandate;
- the F3 retest tolerance (U-02) - the source itself declines to define it (C-09), and the F3 arm
  shares MC-7's small-R geometry, so it cannot escape the cost arithmetic above.

---

## STATUS 2026-09-18 — third source reviewed (@CeewilliTradez)

Reviewed at Simon's request, to test whether the approach complements Max. **It does not.**
Assessment: `14_SECOND_SOURCE/OUTPUTS/SOURCE_ASSESSMENT_CEEWILLITRADEZ.md`
(4 videos, ~81 min, full ASR transcripts, all quotations timestamped).

**Finding.** Same entry geometry as Max and as CM-C1 — 09:30–09:45, wick to wick, midline, break,
retest, rejection — with *more* confirmation stacked on top (body-close, engulfing, inverse FVG,
"a better retest"). Against the reopening criterion in DECISION_LOG (*a materially larger raw edge
from a different entry geometry, not a filter on this one*), **nothing in this source qualifies.**

**Carousel mapped to the register:**

| Model | Status |
|---|---|
| Break → retest → rejection | This **is** CM-C1 |
| Liquidity sweep → reversal | TSUGI-02 — already falsified |
| Inside-ORB rejection / fade | Rejection entry — already falsified |
| Break-and-go (no retest) | He says it fails on futures — see the conflict below |
| Confirmation candles / IFVG | Confirmation family — closed four ways |
| 5-min ORB | Duplicate (Max R-044), and narrower R ⇒ **worse** cost/R |
| HTF 4H/1H bias gate + no-trade-if-unclear | Probably inside D-031; pre-open, cheap |
| **Unswept liquidity beyond the ORB edge ⇒ fake-out** | **Not in the register — CW-01** |
| Targets at external liquidity (1:2 to 3.75R) | Exit sweep covered it; noted, not proposed |
| Single-name equity options, 20–50% premium exits | **Untestable — no options data** |

**Net new testable content: one item (CW-01), and it is a filter, so it cannot reopen the family.**
It is offered as a *gap-closer in the discriminant search*, not as a candidate: a structural-context
feature evaluable at 09:45 with **zero extraction cost** (no bar close, no look-ahead — unlike
TSUGI-03, which cost −0.155R to extract). Screen on **gross only**; if gross is ~zero it joins D-031
and the discriminant search is closed on a broader basis than it is now.

**Checked against D-038 rather than assumed.** The ten screened features were *reached the edge ·
direction · W_rel · imp_R · cost/R · latency · W · day-of-week · straddle · outside-fraction*. All
are properties of the range, of the break's own path, or of the calendar. **None is prior-session
structural context.** `straddle` and `outside-fraction` describe behaviour around the edge after the
range forms — a different variable. D-038 also screened against *full-stop-versus-not* (a loss
predictor), whereas CW-01 predicts *which side resolves*. So the narrow closure does not cover it;
the broad one (D-031, patterns on gross → zero) probably does.
**No request is raised.** Under mandate section 25 the case is borderline and the Research Agent's
prior is that it returns zero. The Analyst decides whether the marginal certainty is worth one run.

**Recorded conflict.** The programme's hardest finding is that the entry price must be the ORB edge
because one minute of confirmation already costs more than the edge is worth. This author states the
opposite for futures — C2 13:20, of entering the break without waiting: *"Do not recommend doing
that on futures though because you will get [screwed] most likely."* He reserves the un-confirmed
entry for options, where the payoff is premium percentage rather than R against a price stop, and
the programme's cost arithmetic does not apply. Measured evidence (9,360 trades, reconstructed
spreads) outweighs asserted evidence (screenshots), so this changes nothing — but it is now the
third independent voice on the confirmation side and is logged rather than dissolved.

**Filed outside the Max evidence pack**, per the tsugitrades precedent.

---

## STATUS 2026-09-18 (b) — Max cycle 3: latest material reviewed

Two further Max videos read end to end — `vTnk9C8u5RQ` (12:02, published 2026-09-13, the only
ORB-relevant upload since cycle 2) and `umBODqRzLnQ` (37:36, published 2026-07-23, 47,750 views,
**missed in cycles 1–2**). Corpus now 14 videos, ~10h. Full detail with step-by-step markers,
instruments and timeframes: `.../Max Options Trading ORB/04_HANDOFF_TO_ANALYST/CYCLE3_LATEST_VIDEO_REVIEW.md`.

**Three items are Analyst-relevant. Only one is a possible test, and it is a filter.**

**1. The "your stop was too tight" objection is now answered from source — and it confirms the closure.**
R-050, new: Max teaches sizing the stop to the *recent wick distribution* —
> V13 05:57: *"The previous 20 candles had 15 to 20 point wicks, but you got a five-point stop-loss …
> you need to check your size and go down maybe to three or four micros instead of a mini and **allow
> that 25 point stop loss**."*

That implies **R ≈ 25 pts**, not the ~9 pts tested, which would put cost/R at ≈ **0.053R** — right at
the ~0.046R reopening threshold in the DECISION_LOG. **It does not rescue the family**, because
RESEARCH_STATE finding 3 already measured gross edge by R band: +0.110R (all) → +0.063R (R≥5) →
+0.031R (R≥10) → **−0.034R (R≥20)**. At the R this stop implies, the gross edge is already negative.
Widening buys down cost/R more slowly than it destroys the signal. **Recommend citing this explicitly
in the closeout** — it is precisely the challenge a reviewer would raise, and it is now pre-answered
with the source's own stop rule.

**2. CL-021 — the first falsifiable number Max has ever given.**
> V14 18:58: *"There's an **85 to 87% chance of success** if you break orb **and previous day highs or
> lows at the same time**."*

Objective, pre-entry, zero extraction cost, one pass. It is a **filter**, so by the stated criterion it
cannot reopen the family. But 85–87% against a measured ~51% base rate is a large gap, and closing it
on the record is cheap. **Gross first.** Alongside CW-01 from the CeeWilli review, that is two
zero-cost structural screens if the Analyst wants to close the discriminant search on a broader basis.
**No request raised** — under mandate section 25 neither can change the decision on its own.

**3. U-04 is now confirmed rather than inferred.** V14 18:07 gives the containment rule a clock time —
*"if we're still within orb by **11:30, noon**"* — which is exactly where six to seven 15-minute candles
from 09:45 land. Two independent statements ~2 years apart agree. The compression work (H-01) rests on
a correctly specified trigger.

**Not Analyst-relevant but recorded:** R-056 — the MVG mechanism is stated for the first time and is
technically wrong (a missing wick is an ordinary price gap, not a CME data-feed lag); the originality
claim is not supportable. CL-023 — *"I made $15,000 last month"*, volunteered, and materially below
every headline figure in the corpus. And V14's charts are on **Central** time (08:30 open).

---

## 2026-09-20 — RESEARCH AGENT: 20.1 REPRESENTATION AUDIT DELIVERED

**Files:** `14_SECOND_SOURCE/OUTPUTS/REPRESENTATION_AUDIT_20.1.md` and
`14_SECOND_SOURCE/OUTPUTS/VISUAL_REFERENCE_LIBRARY.md`.

**Headline for the Analyst: the 0-of-2,370 result is a property of the candidate
generator, not of the market.** Both sources teach a sequence in which price returns
into the range — closing back **inside** it, repeatedly — and the entry is the bar that
closes back **outside**. Our generator places the entry region between confirmed
direction and the ORB edge, which makes that population unreachable by construction.

**Newly verified (first direct chart verification in the programme).** Exhibit V-01,
CeeWilli C1 `_yr2oZhMPLM` t=308s, ES1! 1-minute, 28 May 2026: **six consecutive
1-minute bars close inside the range** between the break and the entry; the bar before
the entry pierces the ORB high with its **wick** and closes back inside and is **not**
taken; the next bar closes above and **is** taken; the stop sits under the pullback
cluster, on-screen label `Stop: 5.75`, `Risk/reward ratio: 2.26`. Method and its
resolution limits are documented; the capture recipe is reproducible.

**Three challenges to current model assumptions (RC-004 to RC-006).**
- **RC-004** — Entry is not the touch and not the rejection bar. It is the **next body
  close** beyond the boundary after the rejection (Max V13 x3; CeeWilli C1 04:41).
  Three-bar minimum structure, not one-bar.
- **RC-005** — A close back inside the ORB is **two different rules**, not one. Max
  V12 05:44 exits an **open** trade; V12 08:49 merely **withdraws confirmation**
  pre-entry, which can then be re-earned. Treating it as globally fatal deletes the
  taught setup.
- **RC-006** — Our direction metric (confirming-block range ÷ ORB range) is used by
  **neither** source. Max uses structure/persistence; CeeWilli uses displacement
  magnitude (unquantified). Legitimate as our own quantity — but the test should stop
  being described as a test of their method on that axis.

**Requested action: one re-run, SPEC-SF-1 (Part 12), two arms on the stop anchor
(Max = entry-bar extreme; CeeWilli = return-cluster extreme), and A-02(iii) as the
base case.** Fix assumptions A-01 to A-05 **before** running. Change nothing else — no
indicators, no filters, no optimisation.

**What this does NOT overturn.** The Analyst's cost analysis stands and is
strengthened: R-050 (Max sizes the stop to the recent wick distribution, ~25 NQ points)
gives cost/R ≈ 0.053R against the ~0.046R threshold, but measured **gross** edge at
R>=20 is **-0.034R** — widening destroys signal faster than it saves cost. The closure
survives the "your stop was too tight" objection. It has simply not yet been tested
against the correct entry sequence.

**Cheapest open item: CW-01 / U-19.** Unswept liquidity resting beyond the ORB edge as
a predictor of which side fakes out. Evaluable at 09:45 at zero extraction cost, not
covered by D-038's ten features, and predicts *which side resolves* rather than
full-stop-or-not.

---

## 2026-09-20(b) — RESEARCH AGENT: V2 SPECIFICATION DELIVERED → `RESEARCH_CURRENT.md`

**Location: `RESEARCH_CURRENT.md` at the root of this tree.** It is the single current
specification document; earlier specification material is superseded.

**One thing to change in your V2 sketch before you build.** Your recommendation reads
"15-minute close outside → **wait one further 15-minute candle**". The wait is **not**
a 15-minute candle. Max's own sequence is: 15m close = signal → **drop to 1-minute** →
retest → the candle that closes back outside → entry on the **next 1m candle printing
through its extreme** (V1 22:56, V8 11:50, V10 24:18, V11 08:34, V13 01:04). A 15-minute
wait would put entry up to 30 minutes after the signal and would re-create exactly the
staleness your figures A/B already diagnose (median break→confirm 28 min).

**Two divergences to run as separate arms, not a blend.**
- **Break:** Max = 15m close outside. CeeWilli = 1m close outside.
- **Entry fire:** Max = BUY/SELL STOP at the reclaim candle's extreme, filled by the
  next candle (**model non-fills — R-039**). CeeWilli = at the reclaim candle's close.
They are **one bar apart**; that one bar is what Max means by "it's usually the next one".

**Stop:** MAX-S1 = reclaim candle's opposite extreme (≈6-17 NQ pts, EXPLICIT REPEATED);
MAX-S2 = recent-wick-sized ≈25 pts (EXPLICIT ISOLATED); CW-S1 = retest-cluster extreme
(5.75 ES pts observed). **No stop in V2 is a function of W.** U-17 stays open — run both
Max arms, report both, do not pick the better one.

**Target:** no fixed multiple from either author for the continuation trade. Max holds
to invalidation and trims at counter-structure (R-045); the midline→opposite-edge targets
belong to the **fade** family and must not be attached here. **Row 7 of your uncertainty
map ("Max ~1R") is not supported by any rule in the ledger** — please amend to "no fixed
target; hold to invalidation".

**Two corrections I owe you.**
1. You are right in §7 and I withdraw my earlier claim that the R-band result settles
   the stop question. Selecting wider-range days changes the population; changing the
   stop rule changes the payoff on the same population. Different experiments. **The
   stop question is open.**
2. Your §4 concession is accepted and it cuts both ways: `block_range_W` correlating
   +0.776 with block body ÷ W means it is a *displacement* composite — which is
   **CeeWilli's** direction concept, not Max's. So the V1 variable was not meaningless;
   it was **the wrong author's primitive, applied to a 30-minute range, with no retest
   and no rejection**. It is still retired from V2 per your instruction.

**Acceptance tests: §H, fourteen of them.** H5 and H8 are the ones that matter — if the
count of inside closes between break and entry is zero everywhere, or if no candidate is
ever reset by a pre-entry invalidation, V2 has repeated V1's structural error and the
economics should not be run.

**Mandatory visual check before Stage 9: VRC-01** (CeeWilli C1, ES1! 1m, 28 May 2026).

---

## 2026-09-20(c) — RESEARCH AGENT: RR-003 — ANSWER TO ANALYST_CURRENT §K1-K3, §E1

**Files: `14_SECOND_SOURCE/OUTPUTS/RR-003.md`; `RESEARCH_CURRENT.md` is now v2.1.**

### K1 — the qualifying return. **Do not tighten the threshold. Split the population.**
Max teaches **two** entry models and says so when asked the exact question you are
stuck on. Audience question, verbatim: *what do you do if it breaks out and doesn't
retest?* → V12 36:39 "if you're waiting for a two candle close, or you waiting for
retest, or are you waiting for market structure — there's a couple different ways to do
it"; V12 37:09 "**you can enter on any close outside of orb** … **There's no correct
answer.**"

Your 58%-return-on-the-next-bar population is not the retest model failing a threshold.
It is the **continuation model**, scored as if it were the retest model. Neither is
being measured.

- **R1 — RETEST arm.** The boundary must be interacted with on **>= 2 separate 1m
  candles** (`low_i <= ORH <= high_i`) after the break and before the qualifying close.
  Source-worded and **ordinal, not numeric**: "retest, **retest**" (V8 14:52), "the
  **second** retest candle" (V8 11:50), "retest, **doji retest**" (V12 27:23), "pulls
  back" (C2 03:34), VRC-01's 8 bars. A one-bar wick is never called a retest anywhere
  in either corpus. There is no free number to search; the one-bar population is
  excluded by construction.
- **R2 — CONTINUATION arm.** No return required; enter on a close beyond the boundary
  (V12 37:09, V12 05:44). Legitimate, explicitly taught, and **never tested as such**.
Report R1 and R2 separately end to end. I am **not** ruling that R1 is "Max's rule" —
he says outright there is no single correct entry. Anything beyond the >= 2 count (a
depth of pullback, a time window, a higher bar count) has **no source support**.

### K2 — fill/invalidation collision: **not a collision. Faithful. Do not patch.**
V12 05:44 "**Anytime** we see a close back inside of orb **anywhere**, that's an
invalidation." No grace period exists in the corpus. Your 49.4%-within-one-bar is a
**finding about the setup**, and it is exactly what R1 predicts when the "retest" was a
one-bar wick — **re-measure it under R1 before drawing anything from it.** A secondary
arm starting invalidation at the bar after the fill is defensible (R-049); base case
stays as built.

### K3 — no prior-session extreme beyond entry: **no target, hold to invalidation.**
That is Max's continuation rule, not a fallback — V12 29:25 "**You ride it until the
invalidation**" (R-045, EXPLICIT REPEATED). CeeWilli's target menu is also wider than
prior-session extremes (Asian high, 15-minute liquidity, unfilled weekly gap — C1
05:07, C1 16:18); SPEC-12 implemented its narrowest member.
**⚠ Treat this ruling with suspicion.** You report the no-target subset carries all the
apparent gross (+0.2016R vs −0.0166R), so the faithful ruling and the profitable subset
coincide — the shape a motivated reading takes. I am ruling on R-045's wording alone,
which predates these numbers. Report that arm with its interval; do not headline it.

### E1 — stop variant A: **the source supplies the fix you were missing.**
R-050 was not implemented. Max prescribes a floor for exactly the degeneracy you found:
V13 05:57 "The previous 20 candles had 15 to 20 point wicks, but you got a five-point
stop-loss … **allow that 25 point stop loss**."
**R3:** `stop_distance = max(|entry − reclaim extreme|, wick_floor)`, `wick_floor` = max
wick over the previous 20 1m candles. Unfloored variant A is **half of Max's stop
rule**. Please withdraw "not mechanisable" as a conclusion about the source and re-test
with the floor. If it is still degenerate, that is a finding about Max.

### One thing V2 did not build
All four arms used *ENTRY SIGNAL = first later 1m close beyond the boundary → FILL at
the next bar's open*. That is **CeeWilli's** trigger. **Max's was not built.** Max arms
a **stop order at the reclaim candle's extreme** and fills only if the next bar trades
through it (V10 24:18 "print through the previous candle"; V11 08:34 "the next candle's
wick hit 308 and then go"). It is an extra filter, it produces **non-fills** (R-039 —
so H10 cannot have passed), and it changes the fill price. Arms A and B differ only in
the stop, so **the Max entry model is still untested.**

### Priority for the re-run
1. R1/R2 split — this is the representation gate. 2. R3 floor; re-test variant A.
3. Build Max's print-through trigger (H10 must show non-fills). 4. K3 arm reported
separately, not headlined. 5. K2 — leave; re-measure under R1.

New acceptance tests **H15-H18** in `RESEARCH_CURRENT.md` §H cover all of the above.

**Nothing in your §G is disputed.** Instrument choice looks decisive and no
representation work changes that. The 1m NQ/ES bid+ask request is supported.

---

## 2026-09-20(d) — RESEARCH AGENT: CEEWILLI PRIMARY DOCUMENT AUDIT → RESEARCH_CURRENT v2.2

**Files:** `14_SECOND_SOURCE/OUTPUTS/CEEWILLI_PLAYBOOK_AUDIT.md`; `RESEARCH_CURRENT.md`
is now **v2.2**. Source: *The ORB Playbook*, Mind Over Markets / @ceewillii, 10pp,
read in full. **Do not rebuild against v2.1.**

### The one finding that matters most
> "**Minimum 1:2 R:R. Never take a trade unless your target is at least 2x your stop
> loss distance.**"

That is a **hard pre-trade gate**, stated as a rule, on a page headed "Never take a
trade unless". V2 has no such gate, so **V2 has been generating trades the author's own
written rule forbids.** It also disposes of RR-003 K3 entirely: your "no target on
31.8% of trades, and that subset carries all the apparent gross" cannot arise — under
the source those are **not trades**. The motivated-reasoning risk I flagged is gone,
because the suspicious population should never have been generated.

### The source names its own primary model and tells you to test it alone
Entry 02 (Break & Retest) is labelled "**the money entry**", "**HIGHEST PROBABILITY**",
"**BEST ENTRY**". Day 2: "**Backtest Entry 2 (Break & Retest) only.**" Day 5-6:
"**Focus on Entry 2 only.**" **The CeeWilli arm is Entry 02 and nothing else.**
He has **four** models, not three: 01 Straight Break, 02 Break & Retest, 03 Liquidity
Sweep, 04 Rejection Inside ORB. We had 03 and 04 conflated.

### What I got wrong in v2.1, corrected
1. **The >= 2-candle retest rule is MAX-ONLY.** CeeWilli gives **no candle count
   anywhere**. I derived it from Max's words and let it sit in the shared core. Removed.
   His selectivity comes from the **R:R gate**, not from counting bars.
2. **U-16 is CLOSED.** CeeWilli has his own invalidation: "**If price returns back
   inside the ORB, the setup is invalidated**" (Entry 01), close-not-touch confirmed by
   Entry 04. Stop applying Max's rule "labelled as ours" — it is his.
3. **"Targets never ORB-derived" was false.** True for Entries 01/02; Entries 03/04
   explicitly target the **opposite ORB level**.
4. **"CeeWilli never stops at the ORB edge" was false.** Entry 01: "stop just below the
   ORB level". (Entry 02 — our arm — is unchanged: "just beyond the retest". CW-S1 is
   now EXPLICIT, not just visual.)
5. **The HTF bias veto is REMOVED.** Ten pages; bias appears once, in the pre-market
   checklist, with no method, and gates **none** of the four models. It is video-only.

### New states
`DRAW (pre-market) → RANGE_SET → BREAK → PULLBACK → REJECTION → RR_GATE → ENTRY`
DRAW and RR_GATE are real states — the target must be identified before entry because
the gate cannot be evaluated without it. And **there is no "reclaim" in his playbook**;
the state is REJECTION, defined mechanically by Entry 03: "a strong reversal candle
**closes back on the correct side of the level**."

### Two unresolved questions, both to be run as ARMS — do not choose
- **U-22 (decisive).** After a genuine body close outside, may price close back **inside**
  the ORB and still be an Entry-02 retest? Playbook: the ORH "**now acts as support**",
  and a return inside **invalidates** (01) or flips you to the opposite trade (04). But
  Entry 04's fake is defined as a **wick** through, which may not cover a prior body
  close outside — and VRC-01 shows six inside closes then a long. **Arm (a) holds /
  arm (b) deep.** This decides whether the VRC-01 population exists at all.
- **U-23.** His own backtest instruction is "**on a 5-min chart**" (Day 2); VRC-01 is
  1-minute. **Run both.** Bar size drives stop distance, which drives the gate.

### Also new and mechanical
"**Move to break even once at 1:1**" (run as an arm); "**Stop trading after two losses
in a day**". Partials are hedged ("consider") — DISCRETIONARY, not implemented.
Break quality adds "**full-bodied, high-volume**" — record `body/range` and
`volume/median20` as **diagnostics only. No threshold. No filter.**

### Arms on the CeeWilli side
{1m, 5m} x {U-22 (a), (b)} x {BE on, off} = 8 cells. **Every dimension is a documented
disagreement in the sources, not a parameter sweep. Report all 8; select none.**

### Acceptance tests H19-H27 added. H19 and H21 are the gates.
H19: the "no target" bucket must be **empty**. H21: if the CeeWilli generator enforces
a candle count on the pullback, it is running Max's rule on the wrong author.

### What this document does NOT contain
**No worked examples. None.** No dated trade, no instrument, no prices, no outcome, no
R achieved, no win rate, no sample, no period. The four diagrams are schematics drawn
for the guide and I have not counted bars off them. It is a free lead-generation guide
ending in a mentorship offer. "Highest probability" is his assertion, unevidenced.
**Nothing here is evidence that the method works.** It is evidence about what the
method *is* — which is all we asked it for.

### Analyst is CLEARED to rebuild, against v2.2, Max and CeeWilli separately.

---

## 2026-09-21 — RESEARCH: DRAW-SELECTION RULING (RESEARCH_CURRENT v2.3)

**Classification D — the source does not resolve draw selection. Strict-nearest is
WITHDRAWN and must not be run as a cell.**

**Both sides of the contradiction were mine.** §E.2's "nearest pre-marked level" was my
simplification of "target the next liquidity level"; §D.11's numbered list implied a
priority the playbook never states. Corrected in v2.3.

**What the source does settle — a nearer level NEVER vetoes:**
- "Take partial profits at key levels. If your target is 4R away, consider locking in
  half at 2R" — presupposes levels **between** entry and target.
- Entry 02 step 4, same four lines as "target the next liquidity level": "**You can hold
  for bigger targets.**"
- The pro tip: a **1m/5m FVG at the ORB level** is "one of the strongest confluences" —
  an **entry** positive. Under nearest it becomes the target and refuses the trade. Your
  two reject panels (5m FVG on top of entry) are that inversion, and they must now pass.
- The gate's own words are conditional on **your** target, not on the nearest thing above.
- C1 05:07: "either Asian high or … or **all the way to** the previous day high."

**Mechanical rule:** scan outward from entry; the draw is the **first permitted level
that already satisfies >= 2R**. Non-qualifying nearer levels are partial-profit levels and
are skipped. No qualifying level anywhere above entry → NO TRADE.

**Two arms (16 cells total). Report both, select neither.**
- **DRAW-NQ** — all permitted types (minus the opposite ORB level).
- **DRAW-SQ** — prior-session structural only (prev session H/L, prev day H/L, NWOG, 15m
  swing H/L); **FVGs excluded as targets**, because the only FVG the playbook places at a
  specific price is the entry confluence, and the only one named as a target is "the next
  **key** fair value gap" with "key" undefined.

**New: H28** (the `rr<2` bucket may contain only setups where **nothing** above entry
reaches 2R) and **H29** (both arms built; strict-nearest is not a cell). U-25 opened.

**VRC-01:** his target is the level his indicator labels **BSL**; whether nearer
structure existed is **NOT determinable** from the capture. Used only as falsification —
strict-nearest predicts the trade is refused and he took it. It does **not** choose
between NQ and SQ; 2.59R is the engine's construction from our level set, not his.

**§D.11.4, and please weigh it:** his chart carries a handful of drawn levels and **no
FVGs at all**; the engine holds ~120 across 12 types. Part of the "nearest" pathology is
**level-set density**, not the selection rule. DRAW-SQ is the sparser reading. Recorded,
not turned into a filter.

**Your economics had no influence on this ruling** and I have not used them. Noted only
so it is on the record: the §D.11 diagnostic you ran is not the same object as either arm
above, so please rebuild rather than reusing it.
