# ANALYST_CURRENT
**20 Sep 2026 · Analyst Agent · MODEL V2 built to SPEC-SF-1 · compact current state**

## A. Current programme status
MODEL V1 retired (representation, not economics). MODEL V2 built to SPEC-SF-1 and run.
**Representation gate: PARTIAL PASS — passes the named acceptance case, fails the population check.**
**Economic test: cannot be completed on available data.** One Research ruling and one dataset needed.

## B. Exact V2 specification tested
15-minute ORB 09:30–09:45 ET wick-to-wick → 1m execution → **BREAK** = first 1m close beyond ORH/ORL
after 09:45 (no order) → **RETURN** = price trades back to the boundary; a close back inside is
permitted → **[REJ arm only]** a rejection bar → **ENTRY SIGNAL** = first later 1m close beyond the
boundary → **FILL at the next bar's open** → stop **A** beyond the entry bar's extreme (Max) or **B**
beyond the return-cluster extreme (CeeWilli) → target = nearest prior-session extreme beyond entry →
post-entry invalidation = first 1m close back inside the ORB → abandon if no fill by 11:30 → one
attempt per side per day. Four arms: BASE-A, BASE-B, REJ-A, REJ-B. BASE = A-02(iii).
Instruments: NAS100, US500 (10.7y); YF_NQ, YF_ES (21 sessions).

## C. Representation acceptance results
**Acceptance case V-01 (CeeWilli ES1! 28 May 2026 1m): PASS.** Native ES 1m starts 2026-08-19, so the
case was run on US500, the closest available series — flagged as a proxy. The state machine produced
exactly the taught sequence: break 10:00 (close above ORH) → close back inside 10:02 → **wick above
ORH with close inside at 10:02 and 10:05 correctly produced NO ENTRY** → qualifying body close 10:07 →
fill 10:08 at the next bar's open. Bar-for-bar match to the exhibit.

## D. Visual-validation result — the gate
**FAIL on the population.** The reference case is an 8-bar pullback with six closes back inside. Ours:

| break → fill | share |
|---|---|
| 3 minutes (the mechanical minimum) | **31.1%** |
| ≤ 5 minutes | 51.4% |
| median | **5 minutes** |

58.0% return on the very next bar after the break; 54.4% signal on the very next bar after the return.
**The "return" is satisfied by a one-bar wick to the boundary.** This is V1's "proximity became entry"
failure arriving by a different route. The 7–12-minute bucket — the only one that looks like V-01 — is
17.8% of trades and its gross is **−0.0016R**.

## E. Material defects discovered
1. **Stop variant A is not mechanisable on 1-minute bars.** "Beyond the entry bar's extreme" gives
   R→0 when that bar is small: R < 0.0002 × price on 20.5% (NAS100) and 26.2% (US500) of trades, with
   unbounded R-multiples (max **699R** on US500). Reported, not patched. **Variant B carried forward.**
2. **SPEC-9 fill collides with SPEC-14 invalidation.** The fill is the next bar's open, which can be
   back inside the range, so the invalidation can fire at once: 49.4% of invalidation exits occur
   within one bar of the fill. Not silently resolved — flagged for a Research ruling.
3. **SPEC-12 yields no target on 31.8% of trades** (prior-session extreme already behind entry).
   Those trades carry **all** the apparent gross: +0.2016R without a target against −0.0166R with one.
4. Stop realism, for the record: variant B gives a median stop of 0.085–0.129% of price against the
   sources' 0.076% (CeeWilli, on-screen) and ~0.10% (Max). **Variant B is faithful; variant A is not.**

## F. Gross headline economics — full unselected population, BASE-B
| | n | /yr | gross | 95% CI | win% | mean W | mean L | med target |
|---|---|---|---|---|---|---|---|---|
| NAS100 | 2,813 | 263 | +0.0654R | [−0.014, +0.149] | 15.3% | — | — | — |
| US500 | 2,876 | 269 | +0.0406R | [−0.046, +0.134] | 14.0% | — | — | — |
| **POOLED** | **5,689** | **532** | **+0.0528R** | **[−0.008, +0.113]** | 14.6% | +3.72R | −0.58R | 5.28R |

MFE reach: 1R 34.5%, **2R 20.2%**, 3R 13.5%, 4R 9.9%.
Exits: invalidation 3,725 (65.5%, −0.442R, mean MFE 0.81R); stop 1,145 (−0.997R); target 522 (+2.615R);
eod 296 (+5.819R). Other arms, gross: BASE-A +0.10/+0.36 (degenerate, see E1), REJ-A +0.01/+0.13,
REJ-B +0.017/+0.059.

**Gross is not distinguishable from zero on any mechanisable arm.**

## G. Cost-adjusted economics
**cost/R median 0.277 pooled → NET −0.8645R.** The source-faithful stop is ~0.1% of price; the measured
CFD round trip is 0.025–0.04% of price. **SPEC-SF-1 cannot be afforded on CFD proxies.**

Native futures, 21 sessions — plumbing only, not economics:

| | median stop | cost/R |
|---|---|---|
| NAS100 CFD BASE-B | 0.129% | 0.188 |
| US500 CFD BASE-B | 0.085% | 0.382 |
| **YF_NQ BASE-B** | 0.184% | **0.023** |
| **YF_ES BASE-B** | 0.111% | **0.129** |

**cost/R on native NQ is ~8× better than on the CFD proxy.** This is the first result in the programme
where instrument choice is decisive rather than cosmetic.

## H. Robustness summary
NAS100 dev(≤2021) +0.071 / val(>2021) +0.059 — stable. US500 dev **−0.066** / val **+0.167** — the old
asymmetry, and it is the larger part of the pooled figure. Pooled dev **+0.002** vs val **+0.114**.
Per-year gross swings from −0.23 to +0.38. No subset is headlined.

## I. Validated
- The V2 state machine reproduces the taught sequence exactly on the one available acceptance case.
- Wick-only interaction correctly refuses entry; a close back inside correctly does not cancel.
- Variant B stop distances match the sources to within a factor of ~1.3.
- Fills are next-bar opens throughout: prices that certainly traded (D-035 discipline carried over).

## J. Falsified
- **Stop variant A (Max's "entry bar extreme") is not mechanisable on 1-minute data.**
- V2 gross on CFD proxies is not distinguishable from zero on any arm.
- The rejection-bar requirement (REJ) does not help: it removes ~29% of trades and lowers gross.
- The apparent gross edge sits entirely in the no-target subset, i.e. in trades with no exit rule.

## K. Unresolved
1. **What makes a return a retest?** A one-bar wick to the boundary currently qualifies. The sources
   show a multi-bar pullback. Setting a threshold ourselves would be parameter mining. **Research
   ruling required.**
2. **Fill-vs-invalidation collision** (E2) — does the source exit on a close inside when the entry
   itself filled inside?
3. **Target when no prior-session extreme lies beyond entry** (31.8% of trades).
4. **Native futures economics** — needs 1m NQ/ES **bid+ask**, 2016→present, documented roll. Have 21
   sessions, TRADE only.

## L. Highest-value next action
**Do not tune the return definition.** Two requests, in order:
1. **Research:** the qualifying-return question (K1) — what, in the sources, distinguishes a retest
   from a one-bar touch. This is the single blocker on the representation gate.
2. **Data:** 1-minute NQ (and ES) bid+ask, 2016→present. Section G shows cost/R falls ~8× on native
   futures, which is the only change measured so far that could make a ~0.05R gross edge tradeable.

Until K1 is answered, V2's economics describe a 5-minute compression around the boundary, not the
taught setup, and should not be quoted as a test of the source method.
