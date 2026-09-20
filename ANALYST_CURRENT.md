# ANALYST_CURRENT
**20 Sep 2026 · Analyst Agent · built against RESEARCH_CURRENT v2.2 · compact current state**
Three sections, deliberately separated: **CEEWILLI V2.2** · **MAX V2.1** · **SUPERSEDED V2.0**.

## A. Programme status
Both corrected implementations are built and pass their representation gates. Economics are
measured, unselected, gross first. **No candidate is cleared.** Every arm is negative after
measured CFD costs, and the only arm with a gross interval excluding zero (Max RETEST S1) is
carried by ten trades out of 1,355. One specification contradiction blocks the mandatory
acceptance case and needs a Research ruling.

---

# CEEWILLI V2.2 — Entry 02 (Break & Retest) only

## Specification built
v2.2 §D/§E.2 exactly. Pre-market DRAW → ORB 09:30–09:45 wick-to-wick → BREAK (body close
beyond the edge, diagnostics recorded not filtered) → PULLBACK (**no candle count**) →
REJECTION (bar interacts with the level AND closes beyond it) → **RR_GATE ≥ 2:1** → ENTRY at
the rejection close, filled at the next bar's open → exit on target / stop beyond the retest
cluster / first close back inside the ORB → 11:30 day stop → two-loss day stop.
**8 cells** = {1m, 5m} × {U22-DEEP, U22-HOLD} × {BE off, BE on}. Instruments NAS100, US500.

## Representation — H19–H27 all PASS
| Test | Result |
|---|---|
| H19 RR gate enforced | **PASS** — min rr = 2.000; **no-target bucket = 0** |
| H20 draws pre-marked, legal, no lookahead | **PASS** — 12 permitted types, all from prior sessions |
| H21 no ≥2-candle rule on CeeWilli | **PASS** — 83% of entries have a single-bar pullback and are kept |
| H22 U-22 two arms | **PASS** — DEEP n=458, HOLD n=494 (populations differ) |
| H23 timeframe two arms | **PASS** — 1m and 5m built end to end |
| H24 break diagnostics, not filtered | **PASS** — body/range and volume/median20 on 100% of breaks, no threshold |
| H25 invalidation is CeeWilli's own | **PASS** — §D.10, U-16 closed |
| H26 BE-at-1R arm | **PASS** |
| H27 two-loss day stop | **PASS** — 0 trades taken after two losses |
| H3 / H13 / H11 | **PASS** — break ≠ entry (min gap 2 min); no entry after 11:30; stop never a function of W |
| **H14 VRC-01** | **FAIL under the literal §E.2 reading; PASS structurally under §D.11** — see defect 1 |

## Headline — gross first, full unselected population, US500
**PRIMARY (§E.2 literal: nearest direction-correct draw)**

| cell | n | /yr | gross | 95% CI | win | 2R MFE | inval | net |
|---|---|---|---|---|---|---|---|---|
| 1m DEEP BE0 | 311 | 29 | −0.1211 | [−0.296, +0.081] | 12.2% | 26.0% | 64.3% | −0.864 |
| 1m DEEP BE1 | 311 | 29 | −0.0315 | [−0.190, +0.157] | 10.0% | 23.2% | 46.9% | −0.775 |
| 1m HOLD BE0 | 361 | 34 | −0.0913 | [−0.278, +0.117] | 13.3% | 28.3% | 52.4% | −1.008 |
| 1m HOLD BE1 | 361 | 34 | −0.0453 | [−0.213, +0.145] | 9.7% | 23.0% | 36.3% | −0.962 |
| 5m DEEP BE0 | 130 | 12 | −0.2152 | [−0.420, +0.003] | 13.8% | 24.6% | 51.5% | −0.719 |
| 5m DEEP BE1 | 130 | 12 | −0.1918 | [−0.367, −0.004] | 9.2% | 20.0% | 31.5% | −0.696 |
| 5m HOLD BE0 | 124 | 12 | −0.3076 | [−0.503, −0.079] | 9.7% | 21.0% | 46.8% | −0.879 |
| 5m HOLD BE1 | 124 | 12 | −0.2808 | [−0.453, −0.100] | 5.6% | 15.3% | 28.2% | −0.852 |

**DIAGNOSTIC (§D.11 hierarchy reading — reported to size the defect, NOT selected):** 1m cells
run 146–150 trades/yr at gross −0.009 to +0.019, all intervals spanning zero; 5m −0.035 to
−0.047. NAS100 mirrors this: nearest 1m DEEP +0.048, hierarchy 1m DEEP +0.051, all ≈ zero.
**No cell is selected. Instrument agreement is absent** (US500 mildly negative, NAS100 mildly
positive, both within noise).

---

# MAX V2.1

## Specification built
v2.2 §C/§E.1. ORB 09:30–09:45 → **15-minute** body close outside → RETEST (**≥2 separate 1m
bars** interacting with the edge; inside closes permitted and counted) → RECLAIM (1m close
beyond the edge) → **BUY/SELL STOP at the reclaim candle's extreme ±1 tick, filled only if the
next bar trades through it** → stop **MAX-S1 floored** by the 20-bar wick maximum, or **MAX-S2**
(the floor alone) → **no fixed target**; exit on the first close back inside the ORB, else the
close → 11:30 day stop. **CONTINUATION** run as a separate arm (no return required).
None of CeeWilli's RR gate, rejection definition, BE rule, two-loss stop or draw targets is used.

## Representation — PASS
H15 **PASS** (min touches = 2; single-bar returns 0.0%) · H16 **PASS** (CONTINUATION separate,
never pooled) · H17 **PASS** (stop-order trigger, not a next-open fill) · H10 **PASS** (800 and
2,811 armed-but-unfilled orders) · H18 **PASS** (no R below the wick floor; max |gross| 50R,
against 699R in V2.0) · H11/H3/H13/H12 **PASS**.

## Headline — NAS100, full unselected population
| arm | n | /yr | gross | 95% CI | median | win | 2R MFE | dev/val | net |
|---|---|---|---|---|---|---|---|---|---|
| **RETEST S1** | 1,355 | 127 | **+0.1871** | **[+0.015, +0.361]** | −0.761 | 10.9% | 31.4% | +0.246 / +0.116 | −0.238 |
| RETEST S2 | 1,355 | 127 | +0.2547 | [+0.042, +0.473] | −1.000 | 8.9% | 32.8% | +0.377 / +0.105 | −0.359 |
| CONTINUATION S1 | 2,406 | 225 | +0.1280 | [−0.014, +0.285] | −1.000 | 11.1% | 31.4% | +0.165 / +0.083 | −0.319 |
| CONTINUATION S2 | 2,406 | 225 | +0.0531 | [−0.102, +0.212] | −1.000 | 8.2% | 30.0% | +0.073 / +0.028 | −0.538 |

**The interval on RETEST S1 excludes zero and should not be believed.** The top 1% of trades is
100.0% of total R. Removing the best **10** trades (0.7% of the sample) takes gross from
**+0.1871R to +0.0330R**. Five of eleven years are negative or flat; 2018 (+0.85) and 2023
(+0.88) carry the record. A bootstrap mean on a distribution this skewed is the wrong statistic
and I am not relying on it.

---

# SUPERSEDED V2.0
Retained as diagnostic history, **not** as strategy evidence: +0.0528R pooled gross; the CFD net
result; the 31.8% no-target population; the rejection-arm result; the raw unfloored MAX stop-A
failure. Generated by a representation now known to differ materially from the source.

---

## Material defects found
1. **§E.2 "nearest" contradicts §D.11 "hierarchy" — blocks H14.** On 28 May 2026 the draw
   universe holds 124 levels; the nearest above entry is 0.18 points away, giving rr ≈ 0 and
   **NO TRADE**. Across all gate evaluations, rr < 0.25 on **46%**. Under the hierarchy reading
   the same day yields prev_session_H at 9.80 points, preRR **2.59** against CeeWilli's on-screen
   **2.26**. Both readings are built and reported; **neither is selected. Research must rule.**
2. **My own implementation defect, fixed:** a 15-minute swing **low** was admitted as an upside
   draw for a long, and a bearish FVG likewise. Draws are now direction-typed. Trade counts
   roughly doubled; conclusions unchanged.
3. **VRC-01's structure is absent from the proxy.** Under the hierarchy reading the model enters
   on 28 May, but with `inside_closes = 0` — the US500 proxy's microstructure that day does not
   contain the six inside closes ES1! shows. H14 is therefore **not** fully demonstrated on any
   series we hold. Native ES 1m begins 2026-08-19.
4. **The compression is structural for CeeWilli, not a bug.** 46.5% of 1m entries sit at the
   mechanical 2-minute minimum (V2.0 was 31.1% at its 3-minute minimum). This is §D.4 working as
   written — he specifies no candle count — so it is faithful, and it is also why his arm and
   Max's RETEST arm are different populations.
5. **The no-target rule gives back large winners.** 24% of Max's stop-outs had already reached
   **≥2R** (mean MFE 4.34R) and exited at −1.00R. 45% of invalidation exits fire below 0.5R MFE.
6. A diagnostic column I printed earlier ("1%-trimmed mean") was meaningless here — the 1st
   percentile is exactly −1.00R, so a strict inequality dropped every full stop-out. Discarded.

## Validated
Both state machines are causal and inspectable; no lookahead. Break ≠ entry everywhere. Max's
print-through trigger is built and genuinely misses fills. Stops are decoupled from W. The RR
gate is enforced and the no-target bucket is empty. Natural 2R MFE is reached on ~31% of Max
trades and ~22–26% of CeeWilli trades.

## Falsified
No CeeWilli cell has a gross interval excluding zero on the primary reading, and none is
positive after cost. Max's apparent edge does not survive removal of ten trades. Neither
instrument agrees with the other in sign. BE-at-1R improves CeeWilli gross in every cell and
still leaves it negative.

## Unresolved
1. **§E.2 vs §D.11 draw selection** — the blocker on H14. Research ruling required.
2. Native futures: 21 sessions of 1m NQ/ES, TRADE-only, undocumented roll. cost/R on the CFD
   proxies is 0.13–0.36; every arm's gross is smaller than its cost. **The economics cannot be
   settled on the instruments we hold.**
3. U-11 displacement/volume thresholds remain unquantified and are recorded, never filtered.

## Highest-value next action
**Get the §E.2/§D.11 ruling.** It changes CeeWilli trade count by a factor of five (311 → 1,607
on US500 1m) and is the only thing standing between the build and a completed acceptance gate.
Second, and unchanged: **1-minute NQ/ES bid+ask, 2016→present, documented roll** — every arm
here dies on cost, not on signal.
