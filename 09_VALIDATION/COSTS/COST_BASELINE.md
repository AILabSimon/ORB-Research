# COST BASELINE — measured, not assumed

Created 2026-09-12 by Analyst Agent. Script: `12_CODE/measure_spread.py`.
Raw output: `09_VALIDATION/COSTS/SPREAD_*.json`.

Spread was **reconstructed** from the paired Dukascopy BID and ASK 1m series
(close-to-close, per minute), not taken from a broker schedule or assumed. ~4M paired
minutes per instrument, 2013/2014 → Aug 2026.

## Measured spread by session window (weekdays only, DST-aware)

### Index CFDs — index points — America/New_York

| Instrument | Window | n | Median | p75 | p90 | p99 | Recent 3y median |
|---|---|---|---|---|---|---|---|
| NAS100 | 09:30–09:45 (ORB) | 49,999 | 1.232 | 1.480 | 1.802 | 2.775 | **1.416** |
| NAS100 | 09:30–16:00 | 1,281,923 | 1.236 | 1.472 | 1.586 | 2.523 | — |
| NAS100 | 15:00–16:00 (power hour) | 193,719 | 1.236 | 1.472 | 1.590 | 2.436 | — |
| US500 | 09:30–09:45 (ORB) | 49,952 | 0.498 | 0.519 | 0.560 | 1.031 | **0.511** |
| US500 | 09:30–16:00 | 1,269,267 | 0.499 | 0.519 | 0.560 | 1.041 | — |
| US500 | 15:00–16:00 (power hour) | 191,883 | 0.500 | 0.520 | 0.561 | 1.064 | — |

### Spot FX — pips — Europe/London

| Instrument | Window | n | Median | p90 | p99 | Recent 3y median |
|---|---|---|---|---|---|---|
| EURUSD | 08:00–08:15 | 47,410 | 0.3 | 0.5 | 0.7 | **0.3** |
| EURUSD | 13:30–13:45 | 47,404 | 0.3 | 0.5 | 0.7 | — |
| EURUSD | 07:00–17:00 | 1,897,175 | 0.3 | 0.5 | 0.7 | — |
| GBPUSD | 08:00–08:15 | 47,410 | 0.8 | 1.2 | 1.7 | **0.7** |
| GBPUSD | 13:30–13:45 | 47,402 | 0.8 | 1.2 | 1.9 | — |
| GBPUSD | 07:00–17:00 | 1,896,890 | 0.8 | 1.1 | 1.8 | — |

## Findings

1. **Spread is essentially flat across the opening range, the cash session and the power
   hour** on both index series. There is no meaningful opening-spread penalty in this data
   at 1-minute resolution. This removes one common reason an opening-range effect appears
   untradable — but see limitation 1 below.
2. NAS100 spread has **widened over time**: full-history median 1.23 pts vs recent-3-year
   median 1.42 pts at the open. Any expectancy figure must therefore be reported on the
   recent regime as well as the full sample, not the full-sample average alone.
3. US500 spread is remarkably stable (~0.50 pts throughout, 0.51 recent).
4. EURUSD 0.3 pips and GBPUSD 0.7–0.8 pips are **raw institutional spreads**.

## Limitations that must be carried into every costed result

1. **These are 1-minute close spreads, not spreads at the moment of a breakout trade.**
   A stop or market order that fires on a breakout impulse will very often transact at a
   worse spread than the minute's closing quote. Slippage must be modelled separately and
   must not be conflated with the spread measured here. These figures are a **floor**.
2. **Dukascopy raw ≠ FTMO or retail execution.** An FTMO-style account will see wider
   spread plus commission. Cost sensitivity testing must span at least the measured median,
   2× the measured median, and the measured p99, plus commission.
3. Commission, entry latency and missed limit fills are not in these numbers.
4. Index CFD costs do not represent futures (tick value, exchange + clearing fees) and
   represent options not at all.

## Default cost assumptions for first-pass costed tests (to be varied in sensitivity)

| Instrument | Spread charged | Slippage | Commission |
|---|---|---|---|
| NAS100 | 1.5 pts (recent p90 ≈ 1.52) | 1 pt on market/stop entries and stop exits | modelled separately |
| US500 | 0.55 pts | 0.5 pt | modelled separately |
| EURUSD | 0.5 pips (p90) | 0.3 pips | ~$7/lot round turn (FTMO-style) |
| GBPUSD | 1.2 pips (p90) | 0.5 pips | ~$7/lot round turn (FTMO-style) |

These are deliberately conservative relative to the measured median. No candidate will be
advanced on median-spread economics alone.
