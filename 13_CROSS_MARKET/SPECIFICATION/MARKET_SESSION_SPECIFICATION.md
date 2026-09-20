# MARKET AND SESSION SPECIFICATION — cross-market branch

Pre-registered 2026-09-12, **before any census was run**. Fixed for Phase A. Any later change is
a new specification with a new version number, not an edit.

## 1. Opening events — pre-registered, not searched

| Market | Dataset | Event | Clock | Timezone | Session end | Rationale |
|---|---|---|---|---|---|---|
| Nasdaq | NAS100 (proxy) | US cash-equity open | **09:30** | `America/New_York` | 16:00 | Primary price-discovery event |
| S&P 500 | US500 (proxy) | US cash-equity open | **09:30** | `America/New_York` | 16:00 | Primary price-discovery event |
| Gold | XAUUSD (proxy) | **COMEX open** | **08:20** | `America/New_York` | 16:00 | Primary gold price-discovery event |
| Gold | XAUUSD (proxy) | US cash-equity open | **09:30** | `America/New_York` | 16:00 | Secondary **structural comparison** only |
| EURUSD | EURUSD spot | London open | **08:00** | `Europe/London` | 17:00 | Existing programme's FX session anchor |
| GBPUSD | GBPUSD spot | London open | **08:00** | `Europe/London` | 17:00 | Existing programme's FX session anchor |

**Gold's two anchors are reported separately throughout and are never merged.** Neither is chosen
retrospectively; both were fixed here before measurement, and both will be reported whatever the
result, including if one is clearly worse.

**FX:** the US cash-open construction is **not** forced onto FX. The FX anchor is the existing
programme's London open. The existing FX ORB V1 control (00:00–08:00 range, 0.10×ATR14 buffer,
opposite-side stop, 16:00 exit, ≈ +0.049R) uses a **different, 8-hour range** and is **preserved
unchanged**. V1 results are never pooled with this branch; comparison is conceptual only and is
deferred to Phase E.

## 2. Opening-range lengths — pre-registered

**L ∈ {5, 15, 30} minutes** for every market and every event.

A 60-minute range is **not** included in Phase A. Per the mandate it may be added only if Phase A
evidence indicates delayed price discovery, or if source research supports it. If added it will be
recorded as a specification amendment with the triggering evidence cited.

Range extremes are **wick to wick**. Range is built from 1-minute bars; a session is included only
if all L one-minute bars of its range window are present. Excluded sessions are counted.

## 3. Timezone handling
All timestamps tz-aware. `America/New_York` and `Europe/London` are applied via the tz database, so
US and UK daylight-saving transitions — including the two periods each year when they are
misaligned — are handled by conversion, never by a fixed UTC offset. Verified: both the 300-minute
and 240-minute London-minus-New-York wall-clock offsets are present in the data.

## 4. Controls — minimum useful set, three only

| ID | Control | Identification problem it addresses |
|---|---|---|
| **X-1** | **Time-matched non-opening range of equal duration**, built at **12:00** local in the same session, same L, identical machinery | Does the *opening* event add information, or would any range of the same length at a quiet hour behave the same? |
| **X-2** | **Unconditional movement from the same decision time** — excursion measured from range completion with no event conditioning, in both directions | Sets the baseline excursion scale, so effect sizes are read against what the session offers anyway |
| **X-3** | **Touch versus completed-close qualification** — both measured on every session from their own event times | Does requiring a completed close add or destroy information? Built into the measurement, costs nothing extra |

No further controls. Volatility- or width-matched non-opening ranges are held in reserve and will
be added **only** if X-1 shows a difference that could plausibly be a width artefact.

## 5. Prohibited in this branch
Higher-timeframe bias · EMA · VWAP · FVG · day-of-week filters · news filters · arbitrary
volatility screens · multi-indicator combinations · retesting the closed Max constructions on the
same proxy datasets without a material reason · searching across opening times.

## 6. Phase discipline
Phase A is **behaviour only**: no stop, no target, no R-multiple, no trade, no equity curve.
Excursions are normalised by **opening-range width W** and by **lagged 20-session median W**
(shifted, no look-ahead) — both behavioural scalings, not risk units. Instrument points are
reported alongside so that Phase-C cost work has an absolute scale.
