# DECISION LOG — cross-market ORB branch

## 2026-09-12 — X-001: branch created inside the connected folder, not as a new project
Access to `.../Projects/Trading/` was not granted this session, so the ORB Programme root could not
be located. The branch lives at `ORB Reserach Sub 2.0/13_CROSS_MARKET/` and should be relocated
under the Programme root when that folder is reachable. **No separate per-instrument project was
created**, per the mandate.

## 2026-09-12 — X-002: no futures data exists; proxies labelled, work proceeds
NQ, MNQ, ES, MES, GC and MGC are absent from the shared store. Index and gold work proceeds on
explicitly labelled CFD/spot proxies; proxy and futures evidence are never combined; futures cost
figures are sizing estimates, never measurements. Acquisition is a separate, non-blocking workstream
— the available markets were not held up for it.

## 2026-09-12 — X-003: events and range lengths PRE-REGISTERED before measurement
09:30 NY for the indices; **08:20 NY COMEX and 09:30 NY for gold, reported separately and never
merged**; 08:00 London for FX, preserving the existing programme's anchor rather than forcing the
US cash-open construction onto FX. L ∈ {5,15,30} everywhere. The 60-minute range was excluded and
its inclusion made conditional on Phase A evidence; that evidence did not appear, so it stays out.

## 2026-09-12 — X-004: the retest family is the cross-market behavioural finding
Positive in 16 of 18 cells, significant in 9, strengthening with range length, and positive in gross
trade terms in all five markets. Recorded as BEHAVIOURAL EFFECT CONFIRMED.

## 2026-09-12 — X-005: the completed close destroys information — confirmed cross-market
Touch beats close in 13 of 18 cells. Independently reproduces, on four new markets, the result the
closed Max project found in FX. The two projects are not pooled; this is a separate replication.

## 2026-09-12 — X-006: the cost problem was the stop construction, not opening-range trading
Sizing the stop off the opening range rather than the entry candle moves cost/R from ~0.28 to
0.04–0.18 on the index and gold proxies. This does **not** reopen the closed Max project; it is a
new construction on a new branch, and it is the branch's most reusable finding.

## 2026-09-12 — X-007: CM-C1 does NOT advance — DATA-LIMITED
Nasdaq retest is +0.105R [+0.060,+0.151] under NQ sizing and **−0.001R [−0.046,+0.047]** on the
measured CFD cost that is the only basis this data supports. It fails to replicate on US500, EURUSD
and GBPUSD (all negative net, positive gross). Development is materially weaker than holdout. With
72 behavioural measurements and ~40 arms examined, one positive under an assumed cost model is a
reason to acquire data, not to advance a candidate.

## 2026-09-12 — X-008: gold PARKED, not rejected
Best 2R geometry in the panel and the cheapest cost/R, but 825 sessions over 3.2 years and every
CI includes zero. Parked pending GC/MGC data. A short-sample point estimate is not permitted to
advance or to kill it.

## 2026-09-12 — X-009: FX and S&P arms COST-DESTROYED — no filtering
Gross is positive in both; the shortfall is arithmetic. Adding filters to close it would be fitting
noise. Recorded so they cannot re-enter under a new construction without new economics.

## 2026-09-12 — X-010: existing FX ORB V1 control NOT modified
Compared conceptually only; results never pooled. The structural contrast supports V1's design.

## 2026-09-12 — X-011: highest-value action is DATA ACQUISITION, not more analysis
NQ/MNQ first, then GC/MGC. Do not extend the market panel. Do not filter the cost-destroyed arms.
