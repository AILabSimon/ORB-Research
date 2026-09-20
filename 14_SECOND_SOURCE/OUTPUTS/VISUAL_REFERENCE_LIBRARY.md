# VISUAL REFERENCE LIBRARY — ENTRY-SEQUENCE VERIFICATION
Research Agent (Agent 1) · Cycle 4 · 2026-09-20
Purpose: Part 10 of the 20.1 Representation Audit. Establish, by direct observation
of the chart (not by transcript alone), where the entry bar sits relative to the
ORB edge, the retest and the rejection.

## METHOD AND ITS LIMITS (read before using any exhibit)

Method actually used: the video was played in the desktop browser pane, paused at a
stated timestamp, and the `<video>` element was drawn to an HTML canvas and screen-
shotted. This is necessary because the video element itself renders blank in ordinary
page screenshots.

Reproduction recipe (any agent with the browser pane can regenerate every exhibit):

```js
// 1. define helpers on the watch page
window.__seek = async t => { const v=document.querySelector('video'); v.pause();
  v.currentTime=t; await new Promise(r=>{const h=()=>{v.removeEventListener('seeked',h);r();};
  v.addEventListener('seeked',h); setTimeout(r,3000);}); await new Promise(r=>setTimeout(r,500)); };
window.__ov = () => { let c=document.getElementById('__ovc'); if(!c){ c=document.createElement('canvas');
  c.id='__ovc'; c.style.cssText='position:fixed;left:0;top:0;z-index:2147483647;background:#111';
  document.body.appendChild(c); c.width=1560; c.height=920; c.style.width='1560px'; c.style.height='920px'; }
  return c; };
window.__draw = (dx,dy,dw,dh,sx,sy,sw,sh) => { const v=document.querySelector('video');
  window.__ov().getContext('2d').drawImage(v,sx,sy,sw,sh,dx,dy,dw,dh); };
// 2. emulate viewport 1600x950, then: await __seek(308); __draw(0,0,1400,900, 760,620,280,180);
// 3. take an ordinary screenshot of the pane.
```

LIMITS, stated honestly:
- Maximum screenshot resolution available from the pane is 800x475 regardless of the
  requested scale. Magnification is obtained by cropping the 1920x1080 source frame
  before drawing, not by a higher-resolution capture.
- Price values cannot be read off most crops. Where a number is quoted below it was
  read from on-screen text (the position tool's own labels), not inferred from pixels.
- Candle-by-candle readings are geometric readings of a rendered chart. They are
  recorded below as OBSERVED, and are classified as REPEATED VISUAL BEHAVIOUR only
  where the same structure was seen in more than one example.
- No claim in this file should be promoted to a mechanical rule on the strength of a
  single exhibit. Where an exhibit corroborates an explicit verbal statement, the
  verbal statement remains the primary evidence and the exhibit is corroboration.

## EXHIBIT V-01 — CeeWilli C1, entry bar is NOT the touch bar
Source: CeeWilli "The 15min ORB Strategy is a CHEATCODE for Scalping (Full Strategy)"
  video id `_yr2oZhMPLM`, 24:18 total.
Frame: t = 308 s. Also examined t = 286 s and t = 292 s.
On-screen identification (crisp text, read directly):
- Instrument: **ES1!** — "S&P 500 E-mini Futures · CME"
- Timeframe: **1 minute** (toolbar shows 30s 1m 2m 3m 5m 15m 30m 1h 2h 4h D W; chart
  header reads `1`; watermark reads `ES1! (1m)`)
- Session date in replay: **Thu 28 May 2026**; clock **UTC-4**; TradingView **Replay** mode
- Indicator watermark: **"ORB Ultimate+ | CeeWilli x Taking Prophets"**
- Plotted levels seen and labelled by the indicator: **ORH** (opening-range high, drawn
  as a horizontal line with the range box shaded below it and projected forward),
  **BSL** (buy-side liquidity, above), **SMT w/ NQ** markers on two swing highs.
- Position tool labels: `Stop: 5.75 (0.076%)`, `Risk/reward ratio: 2.26`, `Qty: 3.478`,
  `Open PnL: 0.00`.

OBSERVED bar sequence (1-minute bars, left to right, relative to the ORH line):

| # | bar | position of the CLOSE relative to ORH |
|---|-----|----------------------------------------|
| 1-2 | two small bars | inside the range (below ORH) |
| 3 | large green bar | **closes well above ORH — the break** |
| 4 | red bar | closes above ORH (still outside) |
| 5 | red bar | **closes back INSIDE the range** |
| 6 | red bar | inside |
| 7 | green bar | inside |
| 8 | red bar | inside |
| 9 | green bar | inside |
| 10 | green bar, long upper wick piercing ORH | **wick above ORH, close still INSIDE** |
| 11 | large green bar | **closes above ORH — ENTRY anchored here** |

The position tool's entry anchor sits at the close of bar 11. The stop anchor sits
below the low of the pullback cluster (bars 5-10), **not** below bar 11's own low.
Stop distance is stated on screen as 5.75 ES points.

WHAT THIS EXHIBIT ESTABLISHES (OBSERVED, single example):
1. The entry bar is not the bar that first returns to the level. Six bars closed
   inside the range between the break and the entry.
2. A wick back through the ORB edge is explicitly not an entry (bar 10). The entry
   requires a body close beyond the edge.
3. The retest is not a shallow touch of the edge from outside. In this example price
   re-entered the range and closed inside it repeatedly.
4. The initial stop is anchored to the pullback structure's extreme, not to the entry
   bar's extreme.

CORROBORATING VERBAL EVIDENCE (primary; already in the ledger):
- CeeWilli C1 04:41 — "we see the buyers come in, nice bullish engulfing candlestick …
  I'm just really right here, I'm just waiting for another body stick candle closure.
  Okay, so I get a body stick candle closure right here. Boom, it's entered in here,
  put our stop loss under this low." → bar 10 is the engulfing bar; bar 11 is the
  "another body stick candle closure"; the exhibit matches the words bar for bar.
- CeeWilli C1 08:59 — "the indicator is telling us to enter. I don't enter just yet.
  I want a little bit more of a better break and a better retest."
- CeeWilli C4 05:36 — "We don't just want a wick. We want a lot of displacement
  outside of the orb." → bar 10 vs bar 11.
- CeeWilli C3 17:18 — "we just wait for a 1-minute candle closure above or below. We
  wait for price to retest. We get a rejection, and then we enter our trade."
- Max V13 (x3 within 12 minutes) — "It's not the candle you think you should enter on.
  It's usually the next one."
- Max V10 12:50 — "I'm going to be looking for the next candle to just retest the orb…
  We need to see printage, though. If I don't see printage, I'm not a fan."

## EXHIBIT V-02 — CeeWilli C1, wider frame (context for V-01)
Frame: t = 292 s, full chart.
Visible: the opening-range box shaded and projected forward to the right of the last
bar; a horizontal ORH line extending both left and right; a dashed level at
approximately the mid-height of the box (consistent with an ORB midline, NOT verified
as such by an on-screen label); a second dotted level above; swing-high and swing-low
annotations produced by the indicator, one labelled with a sweep marker.
Status: CONTEXT ONLY. The midline reading is a **provisional interpretation**; the
label was not legible. Do not use it as evidence that CeeWilli trades a midline.

## NOT CAPTURED — recorded as a limitation, not as an absence of evidence
- Max V11 `0WddcphxAo8` ~514 s (print-through entry) and Max V10 `NF0qHcXp50o` ~820 s
  were scoped for the same treatment and were NOT captured in this cycle. The
  equivalent bar-by-bar visual confirmation for Max therefore does not yet exist.
  Max's side of the sequence question currently rests on explicit verbal evidence only
  (V1 22:36, V1 27:18, V10 12:50, V12 05:44, V12 08:49, V13 x3).
- No attempt was made to obtain material behind any paywall, login or bot check.
  youtubetotranscript.com remains behind a Cloudflare challenge and was NOT bypassed.
