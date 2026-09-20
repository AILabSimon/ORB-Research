# DATA ACQUISITION — status and corrected recommendation

**Date** 2026-09-13 · **Authorisation** SVP approved acquisition of the data needed to decide
candidate CM-C1, via Dukascopy, using a Python route rather than manual web access.
**Outcome** Not acquired. Two independent blockers, both verified rather than assumed.

---

## Blocker 1 — Dukascopy does not carry futures data at all

This is the material one, and it is a scope problem rather than a technical one.

The recommendation the SVP approved was for **NQ/MNQ futures** data (then GC/MGC). Dukascopy is
not a futures vendor. The full instrument catalogue in `dukascopy-python` 4.0.1 was enumerated:

> **1,380 instruments. Zero futures contracts.**

Every apparent match is a false positive:

| Symbol that looks like futures | What it actually is |
|---|---|
| `E_NQ-100` | NASDAQ-100 **index CFD** — this is the series we already hold and already measured |
| `CME.US/USD` | CME Group Inc **equity share** |
| `ES.US/USD` | Eversource Energy **stock** |
| `E_SandP-500` | S&P 500 **index CFD** — already held |
| `E_Futsee-100` | FTSE 100 **index CFD** |
| gold | only `XAU/USD` **spot**. There is no GC and no MGC. |

**Consequence.** Running this acquisition to completion would download more of the same index-CFD
data the candidate was already tested on, and would reproduce the **−0.001R** result already in the
record — because that figure *is* the Dukascopy CFD measurement. It cannot move the candidate off
DATA-LIMITED.

## Blocker 2 — the Dukascopy host is not on the network allowlist

Independently of the above, `freeserv.dukascopy.com` returns **HTTP 403 at the proxy CONNECT
stage** from both available shells — the cloud research container and the desktop Linux VM. The
agent-proxy status endpoint reports it explicitly:

```
kind:   connect_rejected
detail: gateway answered 403 to CONNECT (policy denial or upstream failure)
host:   freeserv.dukascopy.com:443
```

That is a policy denial, not a transient failure. Per project rules the endpoint was not retried
repeatedly, and the deprecated raw `datafeed.dukascopy.com/*.bi5` route was not rebuilt.

Note this blocker also applies to the *existing* shared store: refreshing it from this session is
not currently possible either.

---

## What is needed instead — corrected recommendation

### To decide CM-C1 (the only live candidate) — NQ or MNQ 1-minute futures history

Any of the following would settle it. All are futures vendors; none is Dukascopy.

| Route | Notes |
|---|---|
| **CME DataMine** | The exchange's own historical service — the authoritative source for NQ/MNQ |
| **Databento** | Per-instrument historical MBP/OHLCV, CME covered, API-first, pay-as-you-go |
| **Firstrate Data / Kibot** | Low-cost bulk 1-minute continuous-contract history |
| **An existing broker feed** | If the desk already holds a futures data subscription, that is the cheapest route by far — worth checking before buying anything |

**Minimum viable spec to decide the candidate:** NQ *or* MNQ, 1-minute OHLC, continuous front-month
with a documented roll convention, **2014 → present**, US cash session at minimum, timestamps
tz-aware or UTC with an exchange-timezone note. Bid/ask or tick would be better but is not required.

Once that exists, no new analysis is needed — the existing scripts re-run unchanged and the
candidate either survives on native data or does not.

### To decide gold — GC or MGC 1-minute futures history
Same vendors, same spec. Lower priority: gold is currently blocked by a 3.2-year sample as well as
by instrument, so it needs both more history and native data.

---

## What *can* still be done with Dukascopy, and why it is worth something

Tick data for the instruments we already hold is not futures data, but it is not worthless. It
removes two of the three remaining modelling assumptions in the cost model:

1. **Spread at the moment of entry.** Currently approximated from 1-minute closing quotes, which
   is a floor rather than an execution estimate.
2. **Same-bar stop/target sequencing.** Currently resolved by a conservative rule that charges the
   trade the worse outcome. This affects **11.3%** of trades. Ticks resolve the true order.

That would harden the −0.001R CFD figure and make the eventual futures comparison cleaner — but
it would **not change which instrument that figure describes**, and it does not decide CM-C1.

**Recommendation:** treat this as a low-priority follow-on, not a substitute. It needs Blocker 2
lifted regardless.

---

## Ready to execute

`acquire_tick_data.py` (delivered alongside this note) is the complete acquisition, written and
ready. It downloads bid **and** ask ticks for NAS100 and XAUUSD, restricted to the session windows
the candidate actually trades, resumable per month, with provenance written in the same schema the
existing shared store uses — including an explicit proxy warning in every provenance record so the
files can never be mistaken for futures.

It runs unchanged in either of two situations:

- `freeserv.dukascopy.com` is added to the egress allowlist → run it from this session; or
- it is run from any machine with unrestricted outbound HTTPS.

Verify access first with `python3 acquire_tick_data.py --probe`, which makes one small request and
reports clearly whether the network path is open.

---

## Effect on the research position

**None.** CM-C1 remains **PROVISIONALLY SUPPORTED / DATA-LIMITED** and does not advance. The
programme position is unchanged from the SVP brief: the candidate sits between **+0.105R** under
assumed futures costs and **−0.001R** on measured CFD costs, and that gap is still a missing
dataset — one that Dukascopy cannot supply.

**Two decisions for the SVP:**
1. Approve a **futures data vendor** (or confirm an existing desk subscription can be used).
2. Optionally, request that `freeserv.dukascopy.com` be allowlisted — needed for the tick
   follow-on and for any future refresh of the existing shared store.

---

# UPDATE — 2026-09-13, after SVP approved both options

## Status of the two approvals

| Approved | Status | Who must act |
|---|---|---|
| 1. Futures data vendor | **Not yet actionable by the research session.** Approval to spend is not the same as access. I hold no vendor credentials, and the project's operating rules prohibit me from purchasing data or market services. | Desk/IT: provision credentials, or deliver the files, or confirm an existing futures subscription |
| 2. Allowlist `freeserv.dukascopy.com` | **Not yet in effect.** Re-tested from both shells after approval: still HTTP 403 at proxy CONNECT (latest failure logged 2026-09-13T16:27Z). | Network/IT: add the host to the egress allowlist |

Neither is a research blocker I can clear myself. No further retries will be made until one of
them changes — retrying a policy denial produces nothing.

## What was built instead — and self-validated

`13_CROSS_MARKET/CODE/futures_pipeline.py`. Two subcommands:

- **`ingest`** — normalises a vendor file (Databento, CME DataMine, Firstrate, Kibot, or generic
  OHLC) into the store schema, with full validation (duplicates, monotonicity, OHLC integrity,
  opening-range completeness by year) and provenance including SHA256 and the roll convention.
  It **refuses to guess** a naive timestamp's timezone, because getting that wrong silently
  shifts every session.
- **`decide`** — runs the **frozen** CM-C1 construction with true contract economics and prints
  the verdict plus the full battery: temporal split, per-year, parameter neighbourhood,
  execution delay, cost sensitivity, and a direct comparison against the proxy baseline.

**Self-test passed.** Run against the existing NAS100 index-CFD data with NQ economics, the
pipeline reproduces the recorded proxy result:

| | recorded (cross-market branch) | pipeline self-test |
|---|---|---|
| net expectancy | +0.1052R | +0.1152R |
| n | 2,578 | 2,581 |
| development ≤2021 | +0.035R | +0.049R |
| holdout >2021 | +0.229R | +0.232R |
| stop neighbourhood | monotone, all positive | monotone, all positive |
| worst year | 2014 negative | 2014 −0.170R |

Two small, explained differences: the pipeline charges **exit-reason-dependent** cost (1.25 pts on
a stop exit, 1.00 otherwise) where the original charged a flat 1.25 — the newer treatment is the
more correct one and accounts for the +0.010R gap; and the standalone loader retains the 338
OHLC-violating bars the original dropped, which accounts for the 3-trade difference. Neither
changes any conclusion.

**Consequence:** the moment data arrives, deciding CM-C1 is two commands and no new analysis.

## What is still needed, precisely

**For the futures decision — any ONE of:**
1. Vendor credentials (API key / login) for Databento, CME DataMine or similar, supplied to this
   session; or
2. The data file itself — NQ *or* MNQ, 1-minute OHLC, continuous front-month with a stated roll
   convention, 2014→present, dropped into the shared store or attached; or
3. Confirmation that an existing desk subscription can be used, plus how to reach it.

Option 2 is the fastest and needs no credentials to change hands.

**For the Dukascopy tick follow-on:** confirmation from network/IT that
`freeserv.dukascopy.com:443` has actually been added to the egress allowlist. I will re-probe on
request rather than polling.

## Research position — unchanged
CM-C1 remains **PROVISIONALLY SUPPORTED / DATA-LIMITED**. Nothing in this update alters the
evidence; it removes the latency between data arriving and the decision being made.
