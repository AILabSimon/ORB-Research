# Note to the Market Data Engineer — from ORB Research Sub 2.0

Date 2026-09-17. We have migrated onto the canonical store. Three items: two defects worth
fixing, and one data request.

---

## 1. DEFECT — reading `Canonical/.../CURRENT/` directly returns a silent fraction of the data

The guide says *"you can read the Parquet files directly, but `load()` always picks the current,
validated version for you."* Read literally, that invites direct Parquet reads. Doing so is unsafe,
because a version directory is a **delta**, not a complete dataset.

`NAS100/BID/CURRENT` → `v2`. Its MANIFEST correctly declares 11 files and 3,366,965 rows spanning
2016-01-04 → 2026-09-15. The **directory contains one Parquet file** (2026 only). The other ten
years live in `v1`, reachable through `parent_version`.

| | rows | share |
|---|---|---|
| Naive read of everything in `CURRENT/` | 241,688 | **7.2%** |
| Correct read, walking `parent_version` | 3,366,965 | 100% |

**No error is raised.** A project doing the obvious thing gets 7.2% of NAS100 and a backtest that
appears to run fine. EURUSD is worse — its chain is six deep (`v6 ← v5 ← v4 ← v3 ← v2 ← v1`).

Suggested fixes, any one of which closes it:
- State explicitly in the guide that version directories are deltas and must be resolved through
  `parent_version` — and that direct Parquet reads are therefore **not** supported; or
- Have `build_canonical.py` write complete (not delta) version directories; or
- Ship a `CURRENT/` view — symlinks or a manifest-driven index — that resolves to the full set.

## 2. DEFECT — `mdlib` is not importable, so the safe path is unavailable to us

```
sys.path.insert(0, ".../Market Data/Scripts")
from mdlib.io import load, load_manifest
# ModuleNotFoundError: No module named 'mdlib'
```

There is no `mdlib` package under `Scripts/`. Since `load()` is the documented safe route and
item 1 makes the fallback unsafe, this is currently blocking correct use for anyone outside
whatever environment `mdlib` lives in. We have written a local resolver as a stopgap; we would
rather delete it and use yours.

## 3. Findings that may interest you (no action needed)

- **`USATECHIDXUSD` and the legacy `E_NQ-100` are the same series.** On 205,732 overlapping
  minutes: zero differences, 1-minute return correlation 1.000000, and the 09:30–10:00 opening
  range identical on **100%** of shared sessions. We had flagged a risk that the new symbol was a
  different product; it is not. Confidence in the migration is high.
- **Our strategy result reproduces on your store**, like-for-like over 2016→2026:
  canonical +0.1508R vs legacy +0.1534R (n = 2,143 vs 2,123). The small difference is your
  slightly better coverage, and it favours the canonical data.

---

## 4. DATA REQUEST

```
DATA REQUEST
Instrument: NAS100, US500, XAUUSD
Period: 2013-08-21 to 2016-01-03   (back-extension only; we already have 2016 onward)
Timeframes: 1m
Price: BID/ASK
Export: ORB Research Sub 2.0
```

**Why the back-extension matters more than it looks.** The canonical store begins 2016-01-04. Our
published result used 2013-08 onward, and the dropped 2.4 years contain our **worst** period. Same
frozen strategy, only the start date differing:

| Window | Net expectancy | Development ≤2021 | Max drawdown |
|---|---|---|---|
| 2013-08 → 2026 (published) | +0.1152R | +0.0491R | 54R |
| 2016-01 → 2026 (canonical) | **+0.1508R** | **+0.0917R** | 29R |

Migrating makes our numbers look **31% better and halves the drawdown — and none of that is
real.** It is the loss of 2014 (−0.19R, our worst year). We will report on the canonical window
because that is policy, but we will carry the longer-window figure alongside it so the improvement
is not mistaken for a finding. If the back-extension is cheap, it removes the caveat entirely.

**Also registering interest:** the free futures sources you mention (`YF_ES` and the Databento
check). Our one live candidate is blocked on **NQ or MNQ 1-minute history** — it is the single
dataset that decides it. We do not need tick, and daily is no use; 1-minute continuous front-month
with a documented roll convention is the requirement. Please flag when those land.

**Standing down our own downloader.** Per the guide we have retired `acquire_tick_data.py` and will
not build another. Future needs come to you as requests.
