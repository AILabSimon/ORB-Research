# CROSS-MARKET DATA INVENTORY — ORB Programme, cross-market branch

Created 2026-09-12. Read-only reference to the shared store
`/Users/ailab/Documents/AI Lab/Data/Downloads/Dukascopy`. Nothing duplicated into this branch.

> **PLACEMENT NOTE.** This branch was created inside the connected folder
> `ORB Reserach Sub 2.0/13_CROSS_MARKET/` because access to the parent
> `.../Projects/Trading/` directory was not granted in this session, so the existing ORB
> Programme root could not be located. It is a **branch, not a new project**, and should be
> relocated under the Programme root once that folder is reachable. No separate per-instrument
> project has been created.

---

## 1. HEADLINE: no source-native futures data exists anywhere in the shared store

Every instrument below is a Dukascopy OTC CFD or spot series. **NQ, MNQ, ES, MES, GC and MGC are
not present**, and no futures feed is configured. Consequences, applied throughout this branch:

- Index and gold results are **explicitly labelled proxies**. They are never called futures results.
- **Proxy and futures evidence are never combined** (there is no futures evidence to combine).
- Each proxy carries a written statement of what it can and cannot support (§4).
- Acquisition of futures data is a separate, non-blocking workstream. Per the mandate, the markets
  whose data is already available proceed now.

## 2. Panel as at 2026-09-12

| # | Market | Source-native target | Dataset used | Representation | Side(s) | Coverage | Sessions | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Nasdaq | NQ / MNQ | `NAS100_1m.csv` | **INDEX_CFD_OTC proxy** | BID + **ASK** | 2013-08 → 2026-08 | 3,343 | VALIDATED |
| 2 | S&P 500 | ES / MES | `US500_1m.csv` | **INDEX_CFD_OTC proxy** | BID + **ASK** | 2013-08 → 2026-08 | 3,345 | VALIDATED |
| 3 | Gold | GC / MGC | `XAUUSD_1m.csv` | **SPOT proxy** | BID only | **2023-05 → 2026-08** | **825** | VALIDATED but **SAMPLE-LIMITED** and **COST-LIMITED** |
| 4 | EURUSD | — (spot is native) | `EURUSD_1M.csv` | SPOT | BID + **ASK** | 2014-06 → 2026-08 | 3,173 | VALIDATED |
| 5 | GBPUSD | — (spot is native) | `GBPUSD_1M.csv` | SPOT | BID + **ASK** | 2014-06 → 2026-08 | 3,170 | VALIDATED |

## 3. Validation detail

Integrity (all five): duplicate timestamps **0**; timestamps monotonic; non-positive prices **0**.
OHLC self-consistency violations: NAS100 338 of 4,137,277 (0.008%, excluded and counted); US500,
XAUUSD, EURUSD, GBPUSD **0**.

**XAUUSD (new to the programme), validated this cycle:**

| Window (America/New_York, weekdays) | Days | Completeness |
|---|---|---|
| 08:20–08:25 (COMEX open, 5-min range) | 825 | **100.00%** |
| 08:20–08:50 (COMEX open, 30-min range) | 825 | 99.76% |
| 09:30–09:35 (cash open, 5-min range) | 824 | 100.00% |
| 09:30–10:00 (cash open, 30-min range) | 825 | 99.76% |
| 08:20–16:00 full session | 825 | median 460 of 460 bars |

Years: 2023 (151) · 2024 (259) · 2025 (258) · 2026 (157).

Index and FX validation carried forward unchanged from `06_DATA/DATA_INVENTORY.md`: NAS100 09:30
ORB window 99.58% complete, US500 99.04%; EURUSD/GBPUSD full-day completeness 96.1%/96.7%.

## 4. What each proxy can and cannot support

| Proxy | CAN support | CANNOT support |
|---|---|---|
| NAS100 | Whether *Nasdaq index price behaviour* around the cash open is directionally informative; relative comparison across range lengths and events; a cost floor via measured BID/ASK | Any statement about NQ/MNQ tick economics, exchange fees, opening-auction print, order-book depth, or contract-specific execution |
| US500 | The same for S&P 500 index price behaviour | The same for ES/MES; and nothing at all about SPX options |
| XAUUSD | Whether *gold price behaviour* around the COMEX and cash opens is directionally informative | GC/MGC contract economics; **and crucially, gold execution cost — there is no ASK series, so spread must be assumed rather than measured** |
| EURUSD / GBPUSD | Spot FX is the native instrument here; measured BID/ASK gives a true spread floor | Broker-specific retail or FTMO execution, which is wider |

## 5. Known limitations carried into every result

1. **No futures data.** The three futures markets in the panel are represented by proxies only.
2. **Gold is sample-limited**: 825 sessions over 3.2 years, versus ~3,300 over 12–13 years for the
   other four. A development/holdout split on gold will be thin; this is stated wherever gold is
   reported and gold is not permitted to advance on a short-sample result alone.
3. **Gold is cost-limited**: no ASK series. XAUUSD spread will be *assumed* from published typical
   values and varied in sensitivity, never presented as measured. **XAUUSD spread must never be
   used as a GC/MGC commission figure.**
4. Volume fields are provider tick-volume, not exchange volume. Not used.
5. The shared cache is mutable — SHA256 frozen at each census run into `13_CROSS_MARKET/DATA/`.
6. Missing interior minutes exist on all series (no-tick minutes); counted per session, and
   sessions failing the opening-range completeness test are excluded and counted.

## 6. Acquisition status
**No download performed and none is blocking.** If source-native futures data is later obtained,
it enters as a separate panel and its results are reported separately from everything here.
