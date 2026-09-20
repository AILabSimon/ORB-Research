# Second source assessment — @tsugitrades "15Min ORB Trading Strategy"

**Assessed** 2026-09-17 · **Analyst Agent** · **Status** complete
**Source** 15-slide Instagram carousel, author @tsugitrades. Instruments shown: SPY/SPX, TSLA, NVDA.

> **This is not Max Options Trading.** It is a different author teaching a superficially similar
> method. It is filed separately, it does not enter the Max evidence pack, and it does not
> corroborate or contradict Track A. Agreement between two retail educators is not evidence.

## 1. What the carousel contains, mapped to the register

| Model taught | Family | Status in this programme |
|---|---|---|
| Retest Entry (bull / bear) | retest at the ORB edge | **This is CM-C1.** Already the live candidate |
| Momentum Entry / "entry during the Break of Structure" | print-through confirmation | **Falsified.** −0.16R across 5/5 instruments |
| Rejection Entry | retest with candle confirmation | Falsified as above; re-falsified here at −0.155R for one bar of delay |
| V-Shape Recovery (sweep the low, reverse up) | failed break then reverse | **Tested here — falsified.** TSUGI-02 |
| Inverse V-Shape Recovery | mirror of the above | Same test, same result |
| "Above VWAP = Bullish Confirmation" | directional filter | **Tested here — no signal.** TSUGI-01 |
| "Don't Trade" — indecision, range-bound, low volume into the level | day filter | Partially covered: the impulse filter (imp_R > 0.23R) is the established form |
| Risk 1% or less | position sizing | Not a claim about edge |

**Net new testable content: two models.** Everything else was already decided.

## 2. The contradiction worth naming

Both sources teach **confirmation before entry** — @tsugitrades explicitly ("bullish/bearish
candles, wicks, or a structure break" monitored on 5–15 min). This programme has now measured that
requirement four separate ways, and every one of them is negative:

| Form of confirmation | Cost to expectancy |
|---|---|
| Print-through of the previous candle's extreme | −0.16R (5/5 instruments) |
| Enter at the close of the retest bar (one bar) | **−0.1554R** pooled, 9,359 trades |
| …filtered to clean-bodied retest bars only | −0.065R, still negative |
| …filtered to in-and-out retest bars only | −0.136R |

The entry price *is* the ORB edge. Every mechanism that gives it up loses more than the information
it buys. This is the single most stable finding in the programme and two independent sources teach
against it.

## 3. TSUGI-01 — VWAP as directional confirmation: NO SIGNAL

Session-anchored VWAP sits inside the opening range by construction, so it agrees with the ORB
direction on 98.9% of trades and cannot filter. Re-tested fairly with an overnight anchor:

| | n | net | dev ≤2021 | holdout >2021 |
|---|---|---|---|---|
| Baseline CM-C1, pooled | 9,360 | +0.0780R | +0.041 | +0.127 |
| Price agrees with VWAP | 7,367 | +0.0801R | +0.046 | +0.124 |
| Price disagrees | 1,990 | +0.0706R | +0.020 | +0.138 |

Difference **+0.0094R, p=0.737**. Per-instrument: XAUUSD +0.165, GBPUSD −0.162 — the sign is not
stable. Discards 21% of trades for nothing. **Not adopted.**

*Caveat: VWAP is computed on Dukascopy tick volume, not exchange volume. A real-volume VWAP could
differ. Given a pooled effect of +0.009R at p=0.74, it would have to differ enormously to matter.*

## 4. TSUGI-02 — sweep / V-shape recovery: FALSIFIED

Break beyond an ORB edge by >0.05W, reclaimed inside within 30 minutes, traded in the opposite
direction. Target next-extreme floored 2R capped 4R, max hold 180 min, measured spreads.

| Stop construction | n | net | 95% CI | dev | holdout |
|---|---|---|---|---|---|
| R = 0.5 × W (comparable with CM-C1) | 10,870 | **−0.105R** | [−0.127, −0.084] | −0.106 | −0.104 |
| Stop beyond the sweep extreme (as taught) | 10,870 | **−0.130R** | [−0.152, −0.108] | −0.153 | −0.100 |

Negative on 5/5 instruments under the first construction. Twelve sub-cuts on NAS100 — sweep-depth
quintiles, decisive reclaim, fast vs slow reclaim, VWAP agreement — produced no positive subset that
held its sign across development and holdout. The deepest-sweep quintile came closest at +0.0005R
and flipped sign between dev (+0.048) and holdout (−0.059).

**Reversal at the opening range is not a viable family on this data.**

## 5. TSUGI-03 — edge interaction: the variable is real, the sign is reversed, and it cannot be used

See DECISION_LOG D-027. Summary:

| Version | Difference | p | Tradeable? |
|---|---|---|---|
| 20-bar window ending **at** the entry bar | +0.142R (clean over chop) | 0.0001 | **No — look-ahead** |
| Same window ending at ei−1 | +0.044R | 0.062 | Yes, but not established |
| Enter at retest-bar close, filter on its body | −0.071R (in-and-out under clean) | 0.015 | Yes — but the delay costs −0.155R |

Right variable, wrong sign, and the extraction cost is more than double the information content.

## 6. What remains open

- Neither new model changes CM-C1's status: still **PROVISIONALLY SUPPORTED / DATA-LIMITED**.
- Per D-022, CM-C1 is cited as **+0.115R (2013–2026)** and **+0.151R (2016–2026 canonical)** together.
- Futures 1m data now exists in the store but is ~30 days long. See D-029.
