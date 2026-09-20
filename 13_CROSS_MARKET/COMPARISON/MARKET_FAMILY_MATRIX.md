# MARKET × FAMILY COMPARISON MATRIX

Phase A/B, 2026-09-12. Behaviour only — no trades. Robust screen: W ≥ 0.5 × lagged 20-session
median W (removes the near-zero-range pathology; share removed is 0.1%–9.8%, tabulated in the
Phase B-1 output). Entry at the ORB edge with an **opposite-edge stop makes R = W exactly**, so
MFE measured in W *is* MFE in R. Effect = mean(MFE − MAE) in W, with a 2,000-sample bootstrap CI.

## 1. Directional effect by family, 180-minute horizon (effect in W; **bold** = CI excludes zero)

| Market / event | L | touch | close | **retest** | fail-reversal |
|---|---|---|---|---|---|
| NAS100 CASH0930 | 5 | +0.080 | −0.021 | +0.039 | **+0.104** |
| NAS100 CASH0930 | 15 | +0.045 | +0.023 | **+0.104** | **+0.086** |
| NAS100 CASH0930 | 30 | +0.034 | +0.023 | **+0.124** | **+0.064** |
| US500 CASH0930 | 5 | **+0.137** | +0.067 | **+0.159** | −0.027 |
| US500 CASH0930 | 15 | +0.036 | +0.049 | **+0.101** | **+0.070** |
| US500 CASH0930 | 30 | +0.035 | +0.010 | **+0.072** | **+0.070** |
| XAUUSD COMEX0820 | 5 | +0.263 | −0.204 | −0.020 | +0.003 |
| XAUUSD COMEX0820 | 15 | −0.037 | −0.031 | +0.119 | +0.100 |
| XAUUSD COMEX0820 | 30 | −0.099 | +0.044 | +0.143 | +0.017 |
| XAUUSD CASH0930 | 5 | −0.084 | +0.004 | +0.001 | +0.180 |
| XAUUSD CASH0930 | 15 | −0.011 | +0.015 | +0.085 | +0.052 |
| XAUUSD CASH0930 | 30 | +0.052 | **+0.097** | **+0.219** | **−0.103** |
| EURUSD LON0800 | 5 | **+0.176** | −0.013 | +0.029 | +0.098 |
| EURUSD LON0800 | 15 | **+0.135** | +0.066 | **+0.151** | −0.018 |
| EURUSD LON0800 | 30 | **+0.117** | +0.019 | **+0.179** | +0.022 |
| GBPUSD LON0800 | 5 | +0.075 | −0.043 | +0.070 | +0.113 |
| GBPUSD LON0800 | 15 | **+0.098** | +0.022 | **+0.187** | +0.009 |
| GBPUSD LON0800 | 30 | **+0.087** | +0.017 | **+0.149** | **+0.093** |

**Three findings, each consistent across markets:**

1. **The RETEST family is the strongest everywhere.** Significant in 9 of 18 cells and positive in
   16 of 18 — the only family with that consistency. It also **strengthens with range length**
   (NAS100 +0.039 → +0.104 → +0.124; EURUSD +0.029 → +0.151 → +0.179).
2. **The COMPLETED CLOSE destroys information.** Its effect is the weakest of the four families in
   almost every cell, and significant in only one. A touch qualification beats a close qualification
   in 13 of 18 cells. This reproduces, on four new markets and three range lengths, the same result
   the closed Max project found in FX — and it is now a cross-market fact rather than a one-off.
3. **No market shows strong raw continuation.** P(MFE>MAE) spans 42.8%–59.9% across all 72
   measurements; nothing resembles a large directional asymmetry on a touch or a close.

## 2. The central tension: direction improves with L, 2R geometry collapses with L

P2R = P(MFE₁₈₀ ≥ 2W) = the probability a 2R target is reachable under an opposite-edge stop.

| Market | family | P2R L5 | P2R L15 | P2R L30 | eff L5 | eff L15 | eff L30 |
|---|---|---|---|---|---|---|---|
| NAS100 | retest | 32.3% | 11.1% | 4.4% | +0.039 | +0.104 | +0.124 |
| US500 | retest | 38.2% | 16.1% | 6.6% | +0.159 | +0.101 | +0.072 |
| XAUUSD COMEX | retest | **59.0%** | 29.0% | 17.0% | −0.020 | +0.119 | +0.143 |
| XAUUSD CASH | retest | 42.3% | 15.8% | 5.8% | +0.001 | +0.085 | +0.219 |
| EURUSD | retest | 46.7% | 27.2% | 17.0% | +0.029 | +0.151 | +0.179 |
| GBPUSD | retest | 50.7% | 31.0% | 18.4% | +0.070 | +0.187 | +0.149 |

Short ranges give abundant 2R geometry but no measurable direction; long ranges give direction but
little 2R headroom **under a full-width stop**. This is what motivated testing a fractional stop in
Phase C, and it is why 2R attainability must be read jointly with the stop construction rather than
treated as a property of the market.

**Gold at the COMEX open has the best 2R geometry in the panel** (P2R 59–63% at L=5), which is a
genuinely new observation: gold's opening range is unusually small relative to its subsequent
travel. Its directional effect at that length is not significant on 3.2 years of data.

## 3. X-1 control — does the opening event add information?
The 12:00 non-opening range of equal duration gives P(MFE>MAE) of 47.8%–50.5% in every market —
consistently *below* 50 — whereas the opening ranges give 48.1%–53.2%. The opening event therefore
adds a small amount of information in most cells (delta in effect +0.04 to +0.22W, excluding the
pathological NAS100 L5 cell). The margin is real but modest, and on its own is not tradable.

## 4. X-2 unconditional baseline
Recorded per session (`unc_*` columns) and used to keep effect sizes readable against what the
session offers regardless of the event. No opening-range effect in the panel approaches the scale
of unconditional session movement.
