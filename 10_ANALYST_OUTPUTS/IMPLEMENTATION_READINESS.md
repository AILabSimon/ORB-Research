# IMPLEMENTATION READINESS

Date 2026-09-12 · **Assessment: NO CANDIDATE IS IMPLEMENTATION-READY. Nothing proceeds.**

This document exists to record *why* nothing advances, and what would have to change.

| Dimension | Assessment |
|---|---|
| **Mechanical completeness** | **Achieved, and this is the project's one clean success.** MC-7 has a source-supported entry (print-through, R-009/P-2), initial stop (entry candle's extreme, R-040) and exit (close back inside the ORB, R-045) — all classified explicit-and-repeated. The reconstruction was validated against the source's own numbers: median R 9.3 pts against a stated 6–17, mode 9–10. Mechanical completeness was never the blocker. |
| **Data requirements** | 1-minute OHLC minimum; 30-second is what the source actually watches. Available for proxies. **Source-native futures data is NOT available** and **no options data exists anywhere in the shared store.** |
| **Execution feasibility** | Poor. Entry is a manual market order during a breakout impulse, which the source himself complains fills badly. A single tick (0.25 pt) of entry slippage removes statistical significance from the best-case estimate. |
| **Cost modelling** | Complete and audited — `09_VALIDATION/COSTS/COST_RECONCILIATION.md`. **This is the blocker.** Median risk $17.62/contract against a $2.67 realistic round trip: breakeven needs +0.2806R, observed raw gross is +0.1100R (2.55× short), and that figure is itself not robust. |
| **Automation complexity** | Low — the rules are codeable and were coded. Irrelevant given the economics. |
| **Monitoring requirements** | N/A. |
| **Remaining validation** | N/A — nothing reached a state where further validation would be warranted. |
| **Live deployment blockers** | (1) No positive costs-adjusted expectancy in any representation on either track. (2) The apparent gross edge declines with tradability and is negative at R≥20 pts. (3) Holdout CI includes zero. (4) One tick of slippage removes significance. (5) Source-native futures unvalidated; options untestable. |

## What would have to change for this to be revisited

1. **A materially larger risk unit.** At the measured gross edge, the stop would have to exceed
   ~16–88 points for MNQ costs to be recoverable. The source's own stop is 6–17 points. A published
   Max variant using a substantially wider stop would be a genuine reason to re-open — nothing else
   found in twelve videos is.
2. **Source-native futures data** would sharpen but not reverse the conclusion: the zero-cost upper
   bound (+0.1100R) already sits below the optimistic-scenario breakeven (+0.1749R), so even
   perfect futures execution does not close the gap.
3. **Historical options contract data** would make the marketed options implementation testable for
   the first time. Nothing in this project is evidence for or against it.

## FTMO-style compatibility
Not assessed, deliberately. FTMO constraints must never be allowed to manufacture an edge, and
there is no underlying edge for them to be applied to.
