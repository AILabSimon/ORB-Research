# STRATEGY FAMILY MAP

Max states himself that the ORB is the basis of **six** strategies, not one
(V8 40:06: "all of them use the orb but the orb is the primary basis"). The families below are
reconstructed from what is actually shown, not from that count.

Shared substrate for every ORB family (R-001 to R-005, all "explicit and repeated"):

| Element | Value |
|---|---|
| Range window | 09:30:00–09:44:59 US Eastern, regular session |
| Range high / low | wick extremes of that single 15-minute candle |
| Midline | (high + low) / 2 |
| Pre-market / overnight input | none |
| Levels on the chart | ORB high, ORB low, ORB midline, and (optionally) previous day high/low |

---

## F1 — Close-confirmed 15-minute breakout continuation
- **Market phenomenon claimed:** a 15-minute body close beyond the opening range marks the day's
  directional commitment; the move continues to the opposite side of the range and often to the close.
- **Range definition:** shared substrate.
- **Entry trigger:** close of the first 15-minute candle whose BODY closes outside the range (R-006).
  Optional additional condition from V8: that candle also takes out the day's high/low (R-008).
- **Confirmation:** the close itself is the confirmation. V8 enumerates it as the fourth of "four
  levels of candlestick confirmation".
- **Stop / invalidation:** break back inside the opening range (R-012). Alternatives exist (C-02).
- **Exit:** TP1 midline; TP2 opposite ORB edge; runners to 16:00 (R-016, R-017). Conflicts with the
  09:55 log-off (C-03).
- **Time window:** first signal can occur at 09:45; in practice most examples shown are 09:45–11:00.
- **Instruments:** NQ/MNQ demonstrated; ES/MES referenced; SPX/SPY/QQQ options referenced.
- **Evidence strength:** STRONGEST of all families. Entry, stop, both targets and the exit are each
  stated explicitly, and the construction has been stable from ~2024 (V3) to 2026 (V5).
- **Mechanical readiness:** READY for trade construction once the Analyst fixes three open choices
  (entry fill assumption, touch-vs-close on the stop, runner vs midline exit).
- **Missing definitions:** same-bar ambiguity (what if the breakout candle also reaches the midline);
  what happens if both sides are broken on different bars.
- **Conflicts with:** F4 (a breakout that fails becomes a reversal signal in the opposite direction —
  the two families will fire on the same bar sequence and must be tested separately).

---

## F2 — Close-confirmed break, lower-timeframe continuation entry ("print through")
- **Phenomenon:** same as F1, but the 15-minute close is only a *trigger to look*; the entry is taken
  on a 1- or 2-minute continuation.
- **Entry trigger:** "the continuation print through" (R-009) — NEVER DEFINED.
- **Everything else:** as F1.
- **Evidence strength:** the *procedure* is explicit and repeated (V1 22:56, 27:18); the *trigger* is not.
- **Mechanical readiness:** INCOMPLETE. The Analyst would have to invent "print through".
- **Conflicts with:** F1 on entry price and therefore on R multiple.

---

## F3 — Close-confirmed break, lower-timeframe break-and-retest entry ("one-two punch")
- **Phenomenon:** after the break, price returns to the broken ORB level, fails there, and resumes.
- **Entry trigger:** "the second retest candle that failed and closed outside of orb" (R-010, V8 11:50).
- **Stop:** not separately stated; presumably the retest extreme, but NOT STATED.
- **Evidence strength:** explicit but isolated (one source). Max separately names break-and-retest as
  one of only two patterns he trades (R-015) but declines to define it.
- **Mechanical readiness:** INCOMPLETE — no retest tolerance, no stop.
- **Conflicts with:** F2 (a retest entry and a continuation entry are mutually exclusive on the same break).

---

## F4 — Failed-breakout reversal
- **Phenomenon:** "nothing is more bearish than a failed bullish move" (R-022) — the most-repeated
  statement in the entire body of material.
- **F4a (simple, V8 17:04):** price breaks out of ORB, then breaks back inside → take the opposite
  direction, target the opposite ORB edge.
- **F4b (confirmed, V1 32:50):** the same, but additionally requiring a break-and-retest of ORB, a
  wick back up, and a market-structure break with a confirmed higher low / lower high.
- **Stop:** NOT STATED anywhere. The natural candidate (the failed breakout's extreme) is never named.
- **Exit:** midline, then opposite ORB edge.
- **Evidence strength:** the axiom is explicit and repeated across four sources over a year; the
  operational trigger is explicit but isolated and given two incompatible ways (C-05).
- **Mechanical readiness:** F4a READY for behavioural discovery (the event is objective).
  F4b INCOMPLETE. Neither has a stop.
- **Conflicts with:** F1 directly. Max offers no *prospective* ORB-based discriminator between
  "this breakout will continue" and "this breakout will fail"; the only discriminator he gives is a
  1-minute market-structure break (R-024, R-025) and, tellingly, a closed-source indicator (C-06).

---

## F5 — Inside-range mean reversion (chop fade)
- **Phenomenon:** on a day that stays inside the range, the ORB high and low are reliable reaction levels.
- **Gate:** the six-or-seven candle rule (R-020).
- **Entry trigger:** long at the ORB low, short at the ORB high (R-021). Reaction/rejection at the
  level is implied but the rejection is not defined.
- **Exit:** midline, or the opposite edge.
- **Evidence strength:** explicit and repeated as an instruction ("go long at the bottom and short
  the top, that's how you play the chop"), never demonstrated as a numbered trade.
- **Mechanical readiness:** PARTIALLY READY. Levels are objective; the gate does not discriminate;
  "rejection" is undefined.
- **Conflicts with:** F1 and F4 (fading an edge is the opposite of trading a break of it). The gate is
  what is meant to separate them, and the gate is disjunctive.

---

## F6 — Delayed afternoon expansion
- **Phenomenon:** the same compressed-morning condition that produces chop can instead produce a
  larger-than-expected move late in the afternoon (R-020, the "A" branch).
- **Entry trigger:** NONE GIVEN. Max never shows how he trades the afternoon expansion.
- **Evidence strength:** stated once as an expectation, never operationalised.
- **Mechanical readiness:** INCOMPLETE — there is no entry rule at all.
- **Note:** this is nonetheless a clean **behavioural** question the Analyst can measure without any
  trade construction: conditional on N candles inside the range, what is the distribution of
  afternoon range expansion versus an unconditional day?

---

## F7 — Pre-ORB trading (NOT an ORB family)
- Trades taken before 09:45 using an undisclosed paid strategy ("Futures Two" / the Mastermind's five
  strategies) plus the three-bar pattern and his MVG imbalance indicator (R-032).
- Max is explicit that the criteria are paid content (V6 06:46, 14:00).
- **Mechanical readiness:** NOT RESEARCHABLE FROM PUBLIC EVIDENCE.
- **Must not be merged into any ORB family.** The video title "How to Find Profits Before ORB Has
  Formed" is the clearest example in the channel of ORB-branded content that is not ORB.

---

## F8 — Non-US-session ORB
- Claimed for the 18:00 ET futures open, the London 03:00–03:15 ET open, and an Asia open stated three
  different ways in one sentence (R-029).
- Only the 18:00 ET futures open is ever shown on a chart (EX-02), and only as a picture.
- **Mechanical readiness:** construction is READY for London and the 18:00 futures open; INCOMPLETE
  for Asia. No entry/exit evidence exists for any of them beyond the US-session rules by assertion.
- **Do not assume transfer.** All FX support is third-party anecdote (V3 09:18).

---

## F9 — "Power hour ORB" — PROVISIONALLY REJECTED
Phase 0 listed a power-hour ORB as a distinct family. On the evidence:
- The "Power Hour Special" is a separate show hosted by Vlady, Logan and Havi; **Max is not present**.
- Across the whole of the sampled episode (V9, 1h47m, 240 caption blocks) the words "orb" and
  "opening range" do not occur once.
- The levels used are a proprietary "sauce box" (which has its own midline), "Quantum Shift" and
  "Pivot Hunter Pro".

**Status:** REJECTED on a sample of 1 of 29+ episodes. A second sample would settle it. Until then,
there is no evidence that a second, afternoon opening range is defined anywhere in Max's material.

---

## Family conflict summary

| | F1 | F4 | F5 |
|---|---|---|---|
| **F1 breakout continuation** | — | fires on the same bar sequence, opposite direction | opposite action at the same level |
| **F4 failed-breakout reversal** | requires F1 to have failed | — | compatible (both fade the break) |
| **F5 chop fade** | opposite action | compatible | — |

There is no published rule that decides between F1 and F4 in advance. That is the single most
important structural finding of this research cycle.
