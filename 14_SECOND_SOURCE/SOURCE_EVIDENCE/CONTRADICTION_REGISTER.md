# CONTRADICTION REGISTER

These are preserved, not resolved. Where the Analyst must pick a side to run a test, the pick is an
ANALYST DECISION and must be recorded as such — it is not a source rule.

---

## C-01 — Breakout qualification: 15-minute body close vs anything that moves
**Taught (V1 22:36, V8 06:11):** the signal is a 15-minute BODY CLOSE outside the opening range; a
candle that closes back inside is explicitly *not* a confirmation.
**Demonstrated (live):**
- V7 07:16 — "got triggered in without body closure. I just let it wick me in off a pending order."
- V7 13:18 — "I don't care about the wick, bro. I don't even care about the wick" on an ORB break.
- V2 16:37 — "I told my people to go long at 9:44", i.e. before the opening-range candle had closed.
- V6, V7 — repeated entries on 30-second and 1-minute charts with no 15-minute close at all.

**Status:** IRRECONCILABLE. The taught rule and the live behaviour are different methods.
**Handling:** test the taught rule. Do not import live behaviour into it. If the taught rule fails,
that is a finding about the *taught* method, not about Max's trading.

---

## C-02 — Stops: level-based stop vs no stop at all vs fixed platform stop
- V1 26:38 — offers an ORB-level stop (14 pts in the example) or a market-structure stop (30 pts),
  then says "you can use different orb as your stop loss criteria".
- V1 41:00 — **"There's no price targets for me. There's no stop losses for me. All there is is
  candlestick structure."** (Same video, 14 minutes later.)
- V8 14:52 — the stop is "the break back into orb".
- V2 42:24 — for the three-bar pattern, the stop is "right below candle 2's wick".
- V2 07:33 — live, an automated **80-tick** stop with a 70-tick trail and a 60-tick trail trigger.
- V4, V6, V7 — live, stops moved manually five or six times per trade to the prior candle's extreme.

**Status:** at least four mutually exclusive stop definitions, one of which is "no stop".
**Handling:** the Analyst must pre-register a stop. Recommended primary: **break back inside the
opening range** (V8 14:52) because it is the only one that is a level rather than a judgement, and
it is the one paired with the published targets. Recommended secondary: the fixed 80-tick stop
(V2 07:33) because it is the only number he has ever published and it is what his platform
actually executes.

---

## C-03 — Holding period: log off at 09:55 vs hold runners to the 16:00 close
- V1 41:18 — "I log off sometimes at 9:40, 9:45. Once the orb is formed to hit an orb trade, I'm
  going to log off at 9:55."
- V8 32:13 — "runners hold them ... hold your runners until the end of the day because we're most
  likely going to close with that fuller body candle." V8 09:47 — "you need to be able to hold this
  and really compound that gain ... if you held to 145 today, congratulations."
- V4, V6, V7 (live) — trades last 2–20 minutes and are scaled out aggressively; nothing is held to
  the close in any live session reviewed.

**Status:** IRRECONCILABLE.
**Relevance to this project's mandate:** the 09:55 / scale-out version fits the 180-minute
constraint comfortably; the runner-to-close version does not. They are different strategies with
different economics and must be separated, not averaged.

---

## C-04 — Trade count: "one and done" vs 3–6 trades plus re-entries and direction flips
- Taught: V1 40:36 and 41:38, V5 01:23 and 28:30, V2 35:43 and 37:08 — "one and done" is presented
  as a core discipline and as the reason for his consistency.
- Demonstrated: V4 has at least five entries, a re-entry after a stop-out, an explicit direction
  flip ("I don't like hitting the reverse button, Poppy, but I will", V4 04:46) and a separate
  "yolo" account run alongside. V7 15:25 — "I only took two trades ... well, three trades."
- And directly: V8 25:55 — "you should never ever ever have an issue re-entering."

**Status:** the stated rule is contradicted by the same person's demonstrated behaviour and by his
own re-entry teaching.
**Handling:** treat max-trades-per-session as a **parameter to discover**, not a constant to assume.

---

## C-05 — The reversal trigger: one condition (V8) vs four conditions (V1)
- V8 17:04 — reversal = broke out, then broke back inside the opening range → take the opposite
  side to the opposite ORB edge.
- V1 32:50 — the same idea but requiring: break back into ORB **+** break-and-retest of ORB **+**
  a wick back up **+** a market-structure break with a higher low confirmed.

**Status:** these are not the same trigger. V1's version will fire far less often and later.
**Handling:** test them as two separate candidates (F4a simple, F4b confirmed). Do not merge.

---

## C-06 — "No indicators" vs a proprietary indicator suite
- V1 07:03 — "This beautiful Wealth Chart is all I need ... I don't need any indicators. I don't
  want to trade with any indicators."
- V2 32:37 and V5 03:05, 39:16 — an MOT indicator suite (basic ORB, advanced ORB, Range Breaker,
  MVG/Max Value Gap, trend) is being launched commercially, and V2 25:59 shows the Range Breaker
  being used live to call a range ("Range breaker says we're done").
- V5 45:46 — "if I really wanted to get more fancy I would throw on my rangebreaker indicator."

**Status:** the "pure price action" framing is a teaching device, not a description of his screen.
**Relevance:** the **advanced ORB indicator "will show you the actual breakouts versus the
reversals"** (V2 33:18). That means the continuation-vs-reversal discriminator the Analyst most
needs is encoded in a closed-source commercial indicator. It is not in the public material.

---

## C-07 — Biography inconsistency
V1 35:45 and V8 49:54: "four years law enforcement", "six years military".
V5 07:42: "I am 10 years military, six years or 10 years law enforcement. I worked as a corrections
officer in a prison for 4 years."
**Status:** minor, but recorded because the project must not treat creator self-description as
reliable. It bears on how much weight to give unverifiable performance claims.

---

## C-08 — "28 of 28 accounts funded" vs "I'm on 45 Midgard accounts ... I'd be blowing accounts"
- V8 40:06 (≈2025) — "I have gotten 28 of my last 28 accounts funded using one strategy."
- V2 40:40 (≈2026) — "I think I'm on 45 Midgard accounts and at least 200 trade[s] ... don't get me
  wrong, I'd be blowing accounts like the [rest]. I'm one of us."
**Status:** the later, volunteered disclosure contradicts the earlier marketing claim.
**Handling:** CL-007 is treated as unsupported.

---

# CYCLE 2 ADDITIONS (from RR-002, 2026-09-12)

## C-09 — "There's no correct answer" vs any single mechanical entry
Asked directly, by an audience member, what to do when a break does not retest:

> **V12 37:09** — "you can enter right here on this close. You don't have to wait for this. It's not
> invalidated. You can enter on any close outside of orb … on the smaller time frames you can enter
> here, here, here, here. I mean, you can enter on all of these. **There's no there's no correct
> answer. Just make sure that you have your risk reward.**"
> **V12 36:39** — "if you're waiting for a two candle close, or you waiting for retest, or are you
> waiting for market structure — there's a couple different ways to do it … and they all have their
> own risk reward."

**Status:** this is the source explicitly declining to define the entry.
**Handling:** it outranks any inference the Analyst or the Research Agent could make. **No single
entry representation may be labelled "Max's rule."** Results must be reported as results about the
tested representation. This does not make the method untestable — it makes the *label* on the result
the thing that has to be careful.

---

## C-10 — A five-minute opening range is also in live use
- **V11 02:07** — "I'd love for NQ to break out of this **5minute orb**."
- **V11 04:17** — "broke out of the **fiveminute orb** already."
- **V11 09:50** — the 15-minute range completes later in the same session: "Orb right there. **945**."

Against **R-001** and **V1 07:23**, where the 15-minute range is the method and 5-minute is framed as
something other people do ("You can try the 5-minute … Remember, what I say is what I do").

**Status:** the taught construction is 15-minute. The live construction is both.
**Relevance:** this is the cleanest available explanation of the pre-09:45 entries that cycle 1 could
only record as undifferentiated "pre-ORB trading" (R-032), and unlike that, it is testable.

---

## C-11 — What to do when the range holds: fade it, or wait and trade the break?
- **R-021 (V3 01:47, V1 21:15)** — "that means this becomes a short every time you hit the top";
  "you got to go long at the bottom and short the top. That's how you play the chop."
- **V12 28:55** — the same six-candles-inside-the-range condition, opposite instruction:
  "one, you're either going to have a larger than expected move now, so **you definitely want to play
  the confirmed break of orb**; two, it is going to bounce around orb and stay close within it,
  usually within about 15 points on each side."

**Status:** two explicit, opposite actions attached to the same objective condition, roughly two
years apart. Not reconciled.
**Note:** the second branch is the only **quantified** prediction found anywhere in the material
(≈15 points either side of the ORB), and is worth measuring in its own right.

---

## C-12 — Stop discipline
- **V11 17:35** — "Definitely keep a stop loss, though."
- **V10 16:39** — a runner carried without one: "**Okay, no stop loss.** It's closed for minus $11 on
  one micro that I had running."
- **V1 41:00** — "There's no price targets for me. **There's no stop losses for me.**"

**Status:** extends C-02 with a live instance. The working reading: an initial stop is placed on
every sized entry, and runners are sometimes carried naked once the position is already banked.

---

## C-13 — "One and done", live and self-corrected within ten minutes
- **V10 15:48** — "**One and done, baby.**"
- **V10 16:00 onwards** — continues trading for a further 25 minutes, taking at least three more
  entries including a re-entry and a direction flip.
- **V10 25:10** — self-correction: "I think I'm **one and done or a two and three**."

**Status:** the clearest single instance of C-04. Trades-per-session remains a parameter to discover,
not a constant to assume.

---

## C-14 — Appeals to statistical work by someone who says he has never done any
- **V4 27:08** — "when you do the **large statistical data**, Orb works best on large move mornings."
- **V2 23:33** — "if you look at **20 years worth of data**, Fridays give the cleanest trends."
- **V10 10:42** — "**I've never back tested a day in my life. Ever.** I forward test."

**Status:** irreconcilable as stated. Either the data is someone else's or it is an impression
described as data.
**Handling:** CL-012 and CL-014 are downgraded to impressions. This does **not** make CL-012 not
worth testing — it makes it a hypothesis rather than a reported finding.
