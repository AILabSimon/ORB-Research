# ANALYST_CURRENT
**21 Sep 2026 · Analyst Agent · latest cycle built against RESEARCH_CURRENT v2.3, issue #3**

---
# CEEWILLI V2.3 — CURRENT (code rebuilt; execution blocked this cycle)

## What this cycle could and could not do
This cycle ran inside the GitHub Actions `claude-code-action` environment (a fresh
`ubuntu-latest` checkout of this repository only, triggered from issue #3). Every prior
Analyst cycle recorded in this file was produced somewhere with access to the canonical
market-data store that `13_CROSS_MARKET/CODE/mdload.py` reads from (mounted at
`~/mnt/Market Data`; underlying store `/Users/.../Data/Downloads/Dukascopy`, see
`13_CROSS_MARKET/DATA/CROSS_MARKET_DATA_INVENTORY.md`). **That store is not reachable
from this environment** — the harness hard-blocks any path outside the repository
working directory, and no such mount exists on the Actions runner. Consequently:
**no backtest was executed, no contingency counts or rates were produced, and no visual
pack was rendered this cycle.** Per programme discipline (gross before net, no invented
numbers), nothing below is presented as a result — only as code, ready to run, plus one
finding that is verifiable from the specification text alone (trend/bias, below).

## 1. CeeWilli Entry 02 — v2.3 draw-arm rebuild (`13_CROSS_MARKET/CODE/cw_entry02.py`)
[v2.2's ANALYST_CURRENT defect 1 — "§E.2 nearest contradicts §D.11 hierarchy"] is
superseded by the v2.3 ruling (§D.11.3), which withdraws both the old `nearest` and
`hierarchy` readings and replaces them with two source-defensible arms. The engine is
rebuilt accordingly:
- `select_draw()` now scans outward from entry by distance and takes the **first**
  permitted level that already satisfies `>= 2R`; a nearer non-qualifying level is
  skipped, never a veto — this directly targets **H28** ("a setup refused because a
  level closer than a qualifying one sat in the way is a defect").
- `DRAW-NQ`: all permitted types (§D.11 table, minus the opposite ORB level) — the full
  ~120-level set.
- `DRAW-SQ`: prior-session structural levels only (previous session H/L, previous day
  H/L, NWOG, 15m swing H/L) — FVGs excluded as targets.
- The reject reason collapses to a single `no_draw` bucket (no level anywhere above
  entry reaches 2R) — there is no longer an `rr_below_2` reason, because a level that
  fails the gate is simply skipped in favour of the next one out, not treated as a
  refusal. This is the intended effect of H19 + H28 together.
- All source-faithful mechanics carried over unchanged: 1m/5m execution, HOLD/DEEP U-22,
  BE-at-1R/no-BE, the hard >=2R gate, CW-S1 stop construction, next-bar-open fills, gross
  before costs, full unselected population. **16 cells** = {1m,5m} x {HOLD,DEEP} x
  {BE off,BE on} x {DRAW-NQ,DRAW-SQ}. Neither draw arm is selected; both are reported
  once run.
- **Not executed.** The code has not been run against real data in this environment and
  has not cleared H1-H29 on a sample. Do not trust a future run's numbers until it has.

## 2. External FVG / failed-break diagnostic — NEW (`13_CROSS_MARKET/CODE/fvg_diagnostic.py`)
Built to the issue's spec: causal 3-candle FVG registry (same gap definition already used
for pre-market draws — no new tolerance/size/distance parameter), evaluated continuously
so an FVG can be "known before the ORB completed" as the issue asks, not just from the
previous session. Implements:
- fields 1-2 (external FVG above ORH / below ORL present, live and unfilled, at break
  time);
- field 3 (first broken-side external FVG subsequently touched — wick overlap);
- field 4 (fill state: `full` / `partial` / `wick_only`, from a single exact-bounds test,
  no tolerance added);
- field 5-6 (opposite-ORB-boundary reached vs the Entry-02 continuation-side draw, and
  which comes first — continuation-side draw is only defined on days/sides that actually
  produced an Entry-02 trade; otherwise recorded as not applicable, never proxied);
- field 7 (order: break -> FVG touch -> return inside ORB -> opposite touch);
- formation-timing cohorts (pre_orb / during_orb / post_orb), descriptive only;
- `primary_counts()` — Entry-02 win/loss x broken-side-FVG-touch contingency + rates;
- `reversal_counts()` — FVG-touch x opposite-ORB-reached, over **all** eligible breaks,
  not only entered trades (the issue separates these two measurements deliberately);
- `visual_pack()` — renders the five requested example categories once a diagnostic
  table exists, extending the existing `v22_figs.py` candle-drawing conventions.

**Known caveat, unresolved pending a run:** the tf=5 bar grid in this module is resampled
continuously across the whole series, while `cw_entry02.run()` resamples per trading day
from 09:30. The two 5-minute bin boundaries are not guaranteed to align. Verify on a
sample day before trusting any tf=5 touch/order result, or rebuild the grid from
`cw_entry02.resample()` applied per day and concatenated.

**Not executed, not sanity-checked, not visually validated.** This is written code, not
a research finding. RESEARCH_CURRENT.md's own rule applies here as much as to the entry
engine: pass acceptance checks on a small sample before any count is quoted.

## 3. Overall trend / bias — answerable without execution
No fitted trend filter was created, per the mandate. Checked directly against the
specification text (no data run needed for this part): §D.3 states the HTF bias veto is
**removed** from v2.2 onward; §D.14 and §I U-24 confirm CeeWilli's "overall market bias"
is named once, in the pre-market checklist, with **no mechanical method given** and **no
gate on any of his four models**; `cw_entry02.py` computes no such field for exactly this
reason. **There is no objective trend/bias column in this research dataset to cross-tab
the FVG-touch/reversal counts against.** This is left for a Research ruling, as the issue
itself anticipates, rather than fitted from economics. See `trend_bias_note()`.

## Highest-value next action
Run `cw_entry02.py` (16 cells) and `fvg_diagnostic.py` in an environment with `mdload`
access to the canonical store; confirm H1-H29 (entry engine) and a small-sample sanity
check on the FVG module (touch/fill classification, causal-only FVGs, no lookahead)
before trusting any number; then produce the primary contingency counts, the reversal-
sequence counts (pooled + by direction + by instrument), the formation-timing cross-tab,
and the visual pack requested in issue #3, and append them here as a new dated entry.
Until that run happens, the population size and every rate implied by it is unknown —
this section deliberately contains no numbers.

---
# CEEWILLI V2.2 — PRIOR CYCLE (built against v2.2; draw rule now superseded by v2.3 above)

## Specification built (v2.2 §D / §E.2 / §F, Entry 02 only)
PRE-MARK DRAW → ORB 09:30–09:44:59 wick-to-wick → **BREAK** (body close beyond the edge; body/range
and volume/median-20 recorded, never filtered) → **PULLBACK** to the broken level (**no candle
count**) → **REJECTION** (bar with `low ≤ ORH ≤ high` **and** a close beyond the edge; a wick alone
is not enough) → **STOP** = beyond the retest cluster, `min(low)[break…rejection] − 1 tick` →
**RR_GATE** `dist(entry,draw)/dist(entry,stop) ≥ 2.0` else **NO TRADE** → **ENTRY** at the rejection
close, filled at the next bar's open → target = the qualifying draw; exit on stop, on the first close
back inside the ORB (his own rule), at 16:00 → 11:30 entry cut-off → **two-loss day stop**.
Entries 01/03/04 and Max's continuation model are not in this population. 8 cells; nothing selected.

## Representation gate — H19–H27 all PASS
H19 RR gate enforced, min rr = 2.000, **no-target bucket = 0** · H20 draws pre-marked and causal
(12 permitted types, prior sessions only) · H21 **no candle count** — the only `>=2` in the engine is
the two-loss stop; 83% of entries have a single-bar pullback and are kept · H22 HOLD and DEEP both
built, populations differ · H23 1m and 5m built end to end (stop and gate included) · H24 break
diagnostics on 100% of breaks, no threshold anywhere · H25 invalidation is CeeWilli's own · H26 BE
and no-BE arms · H27 zero trades after two losses. Retained: H1 ORB, H3 break ≠ entry (min gap
2 min), H4 real interaction, H6 wick-only ≠ rejection, H9 no lookahead, H13 day stop, honest fills
(next-bar open). **H14 VRC-01 FAILS under the literal §E.2 reading — see defect 1.**

## Visual validation — PASS for geometry, and it exposed the gate defect
Sampled 1m/5m × HOLD/DEEP, each a win, a loss and a gate reject. Break → rejection → fill are
properly separated and the trades read as Entry 02. **Stop realism is good:** median stop 0.087% of
price (NAS100 1m) against CeeWilli's on-screen 0.076%. Two reject panels show the defect plainly —
NAS100 2024-11-18 (R=58.0, preRR **0.0**) and 2022-08-24 (R=48.4, preRR **0.0**) were refused
because a 5-minute FVG sat on top of the entry, and price then ran hard in the trade's direction.

## Economics — 8 cells, gross first, full unselected population
Full table (candidates, gate passes/rejects, MFE/MAE, 1R/2R/3R, exit mix, year-by-year,
available_RR and draw-type distributions) is in `13_CROSS_MARKET/OUTPUTS/CW_ENTRY02_ECONOMICS.md`.
US500 headline:

| cell | cand | pass | rej (no draw / rr<2) | /yr | GROSS | 95% CI | win% | 2R | stop | inval | target | BE | NET |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1m HOLD BE0 | 2587 | 361 | 694 / 1532 | 34 | −0.0913 | [−0.289, +0.117] | 13.3 | 28% | 34% | 52% | 13% | — | −1.008 |
| 1m HOLD BE1 | 2587 | 361 | 694 / 1532 | 34 | −0.0453 | [−0.214, +0.153] | 9.7 | 23% | 25% | 36% | 9% | 29% | −0.962 |
| 1m DEEP BE0 | 2948 | 311 | 801 / 1836 | 29 | −0.1211 | [−0.291, +0.079] | 12.2 | 26% | 24% | 64% | 11% | — | −0.864 |
| 1m DEEP BE1 | 2948 | 311 | 801 / 1836 | 29 | −0.0315 | [−0.193, +0.149] | 10.0 | 23% | 17% | 47% | 9% | 27% | −0.775 |
| 5m HOLD BE0 | 1777 | 124 | 505 / 1148 | 12 | −0.3076 | [−0.513, −0.076] | 9.7 | 21% | 43% | 47% | 10% | — | −0.879 |
| 5m HOLD BE1 | 1777 | 124 | 505 / 1148 | 12 | −0.2808 | [−0.449, −0.097] | 5.6 | 15% | 35% | 28% | 6% | 31% | −0.852 |
| 5m DEEP BE0 | 2221 | 130 | 632 / 1459 | 12 | −0.2152 | [−0.414, +0.005] | 13.8 | 25% | 35% | 52% | 12% | — | −0.719 |
| 5m DEEP BE1 | 2221 | 130 | 632 / 1459 | 12 | −0.1918 | [−0.362, −0.004] | 9.2 | 20% | 29% | 32% | 8% | 30% | −0.696 |

NAS100 runs slightly positive gross on the same cells (1m DEEP +0.048, 1m HOLD +0.018); **the two
instruments do not agree in sign.** Mean winner +2.6 to +4.0R, mean loser −0.6 to −0.8R.
**DIAGNOSTIC, not selected:** the §D.11 hierarchy reading yields 146–150 trades/yr at gross −0.009
to +0.019, all intervals spanning zero.

## Material defects
1. **§E.2 "nearest" contradicts §D.11 "hierarchy" — blocks H14.** `available_RR` is below 0.5 on
   **61%** of gate evaluations and below 0.10 on **~33%** of the rr-rejects: with ~120 pre-marked
   levels the nearest one is usually adjacent to the entry. On 28 May 2026 that gives rr ≈ 0 and no
   trade; under the hierarchy the same day gives preRR 2.59 against CeeWilli's on-screen 2.26.
   Both built, both reported, **neither selected. Research must rule.**
2. **Fixed, mine:** a 15-minute swing **low** was admitted as an upside draw for a long (and a
   bearish FVG likewise). Draws are now direction-typed. Counts roughly doubled; conclusions unchanged.
3. **VRC-01's six inside closes are absent from every series we hold.** Native ES 1m begins
   2026-08-19, so the acceptance case can only be run on the US500 proxy, whose microstructure that
   day differs. H14 is therefore not fully demonstrable on available data.
4. **Cost, not signal, is what kills every cell.** cost/R median 0.30 (NAS100 1m), 0.53 (US500 1m).
   Every arm's gross is smaller than its own cost.

## What was learned
The setup is now represented credibly and the numbers are honest: stop distances match the source,
the gate is enforced with an empty no-target bucket, and 2R is naturally reached on 20–28% of trades.
Gross sits at or just below zero on every cell, on both instruments, in both U-22 readings and on
both timeframes — and the intervals span zero except where they are significantly **negative**.
BE-at-1R improves gross in all eight cells and leaves every one of them negative. The dominant exit
is **invalidation** (28–64%), i.e. his own close-back-inside rule cutting trades early.

## Is Entry 02 now represented credibly?
**Yes, with one caveat.** The state machine, stop construction, gate and management follow v2.2
exactly, and the visual sample reads as Entry 02. The caveat is defect 1: the draw-selection rule is
genuinely ambiguous in the source, and it changes trade count roughly five-fold (311 → 1,607 on
US500 1m). Until that is ruled on, the *population* is provisional even though the *mechanism* is right.

## Highest-value next action
**The §E.2 / §D.11 draw ruling.** It is the only open representation question, it is the blocker on
H14, and it moves the trade population by a factor of five. Everything else is measured.

---
# MAX V2.1 — PENDING SEPARATE CYCLE
Not run this cycle, per mandate. Existing results stand unchanged: RETEST S1 n=1,355, gross +0.1871
[+0.015, +0.361], net −0.238 — **with the caveat already on the record that the top 1% of trades is
100% of total R and removing the best 10 trades takes gross to +0.0330R.**

---
# V2.0 — SUPERSEDED REPRESENTATION
Diagnostic history only, not strategy evidence: +0.0528R pooled gross; the CFD net result; the 31.8%
no-target population; the rejection-arm result; the unfloored MAX stop-A failure.
