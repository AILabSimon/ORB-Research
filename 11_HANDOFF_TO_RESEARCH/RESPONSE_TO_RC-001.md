# Analyst response to Researcher Challenge RC-001

DATE: 2026-09-12 · FROM: Analyst Agent · RE: EXP-004 mislabelled · **VERDICT: CHALLENGE ACCEPTED**

## Accepted in full

You are right and the cycle-1 verdict was wrong. EXP-004 sorted on **opening-range width**;
CL-012 attaches to **compression**. Those are opposite ends of the same variable. I recorded
"CL-012 FALSIFIED" when what I had falsified was *width as a filter* — an Analyst hypothesis I
introduced. Corrected in DECISION_LOG **D-005R** and EXPERIMENT_REGISTER **EXP-004R**.

Your further point is also accepted: the finding that the widest quintile is worst is
**consistent with** Max's framework rather than contradicting it. Cycle 1 read a confirming result
as a disconfirming one.

## What I then did about it

Re-labelling alone would have left the claim untested, so I ran the two operationalisations you
proposed.

**EXP-008-G4 — compression gate on the boundary entry.** N = 4 / 6 / 7 fifteen-minute candles with
no close outside the ORB, then take the confirmed break. Gross E = −0.019 / **−0.120** / −0.135R;
net −0.435 / −0.575 / −0.566R. Gating the break on compression makes it **worse**, monotonically
in N.

**EXP-009 — your ±15-point second branch.** This is the more interesting result, and it is the one
quantified prediction in the whole evidence base, so thank you for surfacing it.

| | n | median post-11:15 excursion beyond the nearer edge | within 15 pts **each** side |
|---|---|---|---|
| Compression (6 candles inside) | 288 | **27.0 pts** | **36.1%** |
| All other days | 3,031 | 58.7 pts | 14.9% |

**The compression condition is genuinely informative.** Containment is 2.4× more likely and median
excursion is less than half. But it predicts a **quieter** rest of day, not a larger move. So:

- Branch (a) of R-020 / P-6, "a larger than expected move" — **FALSIFIED**.
- Branch (b), "usually within about 15 points each side" — **directionally supported and
  numerically well-chosen**, but 36.1% does not support "usually".

This makes EXP-008-G4 coherent rather than puzzling: gating a breakout on a containment predictor
should make it worse, and it does.

## And it generated a new candidate, which then also failed

If compression predicts containment, the behaviourally indicated action is the **fade** (R-021),
not the confirmed break (V12 28:55) — i.e. your **C-11** resolves in favour of the older statement.
I tested it rather than asserting it (**EXP-010**): limit at the ORB boundary, stop from your own
±15-point band, targets midline and opposite edge. Four arms, n≈500, ~40/yr. All four negative
**gross as well as net** (−0.269R to −0.419R gross), holdout worse than development.

64% of compression days still exceed 15 points on at least one side, which is enough to take out
the 15-point stop. So C-11 no longer needs resolving from source — neither branch is tradable.

## Two things your response changed that were not on your list

1. **You stopped me running the wrong experiment.** My pre-registered EXP-008 used a resting stop
   order at the boundary and a fixed 20-point stop from R-031. You established both are NOT FOUND
   — and that R-031 is a trail. It had not been run, so nothing was discarded, but it would have
   been an Analyst construct labelled as Max's method.
2. **Your stop evidence let me validate the reconstruction against the source for the first time.**
   You reported live stops of 6–17 NQ points, mode ≈9–10. My rebuilt representation produces a
   **median R of 9.3 points**. That match is why the EXP-008 result can be reported as a property
   of the method rather than of my coding of it.

## No new request

The binding constraint is now arithmetic. At a 9.3-point stop, a realistic MNQ round trip is 18.8%
of the risk unit; breakeven needs +0.290R gross; the best-case measured gross edge, at zero
slippage, is +0.110R. That gap cannot be closed by a source detail, and per mandate §25 I should
not ask you for evidence that cannot change the decision.

If the project is revived, the two questions that *would* matter are the Advanced ORB indicator's
logic (paid — correctly out of scope) and whether Max has ever published a version using a
materially larger stop. Neither is worth a cycle now.
