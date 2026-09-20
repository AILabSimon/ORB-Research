# Reusable prompt — "Build the SVP research-standing brief"

Paste everything below the line into any research project's session. It is deliberately
project-agnostic: it describes the *structure, rules and format*, and takes its content from
whatever that project has actually measured.

Tested on the ORB Programme, 13 Sep 2026. Produces a single self-contained HTML page (publishable
as an artifact, or saved and emailed as a file).

---

## PROMPT — copy from here

You are preparing a research-standing brief for an SVP. Build it as a **single self-contained HTML
page**. Follow the rules below exactly; they matter more than the prose.

### RULE 0 — HONESTY GATES (non-negotiable, apply before anything else)

These exist because a senior reader will spot a fabrication instantly, and one fabrication
discredits the whole brief.

1. **Never draw a visual for something you have not measured.** If I ask for a chart of a concept,
   framework, or metric this project has not tested, say so in a panel at the top of the brief,
   name the thing explicitly, and state plainly that no data exists. Do not substitute a
   plausible-looking diagram.
2. **Open with what is missing, not with what is impressive.** If there are things the reader may
   expect that are absent, they go in a bordered callout **before** the headline numbers — never
   buried in limitations at the end.
3. **Separate "tested and failed" from "never tested".** These are different verdicts. If the test
   ran on a proxy instrument or a substitute dataset, say what it can and cannot support. Never
   write "falsified" about something you only tested by proxy.
4. **Label every number with its cost/assumption basis.** If a result flips sign depending on an
   assumption, show *both* values side by side, not the favourable one.
5. **State whether any of it is live.** If everything is historical simulation, say "no live or
   forward-tested trades exist" in the opening panel.
6. **Surface the number you would least like to be asked about**, and annotate it yourself. If
   out-of-sample is stronger than in-sample, if the sample is short, if a result rests on one
   period — put it in a caption in your own words before the reader finds it.
7. **Own errors in the first person, with the correction.** Not "an adjustment was made" —
   "I quoted X as Y; that was wrong; here is the corrected figure; it is now used throughout."

### SECTION STRUCTURE — eight sections, numbered, in this order

| # | Section | Contains |
|---|---|---|
| 00 | Honesty panel | Rule 0 items 1, 2, 5. Bordered, before everything. |
| 01 | The headline | 3 stat tiles + one callout naming the single most important finding |
| 02 | The mechanism | Diagram of the thing actually tested, plus numbered stage cards |
| 03 | Where we were | "Before" performance table, per session |
| 04 | Errors & corrections | One card per error: what was wrong, what it is now |
| 05 | Adjustments | Before→after per component, + a chart of the impact |
| 06 | Where we are now | "After" performance table, per session, + 2 charts |
| 07 | Confidence split | Three columns: Settled / Still to clarify / Unknown |
| 08 | Direction | Recommendation + what is explicitly NOT recommended |

Close with a sources line naming the underlying files, and a one-line data-provenance statement.

### PERFORMANCE TABLES — exact schema

Both the "before" (§03) and "after" (§06) tables use the same columns so they can be read
against each other. **One row per market-and-session combination**, never pooled:

```
Market & session | Trades | W | L | BE | Win % | Total R | R / trade | R / yr | Max DD
```

- **Session** is a labelled pill next to the market name (e.g. `US 09:30`, `London 08:00`),
  because results from different sessions must never be summed.
- **BE** (break-even) is a real column, not folded into wins. Define the threshold and state it
  (e.g. |net R| < 0.05).
- Where the same row has two cost bases, give it **two rows**, the second visibly marked as the
  measured/conservative one. Highlight the headline row with a tinted background.
- Under the table, a small-print line giving sample length per row and flagging any row whose
  confidence interval includes zero.

### CHARTS — three, no more

Each must earn its place. Load the data-visualisation guidance before writing chart code.

1. **Impact on the trade distribution** — two 100% stacked horizontal bars, before vs after, split
   Win / Break-even / Loss. Semantic colour only (good / neutral / critical), legend present,
   percentages direct-labelled inside the bars.
2. **Expectancy per trade by market and session** — horizontal diverging bars around a labelled
   zero line. Sort best to worst. Fade any bar whose interval includes zero and say why in the
   caption. Direct-label every value.
3. **The candidate's result by year** — vertical bars around zero, with a dashed rule separating
   development from holdout and both periods labelled. **The caption is where you flag the
   weakness in this chart yourself.**

Chart rules: one scale per chart, never a dual axis. Text takes theme tokens, never the series
colour. Every axis label names a value the chart actually reaches. Leave room in the viewBox for
outermost labels. Give every drawn shape an explicit fill.

### DESIGN SPEC

- **Layout**: single column, max-width ~1080px, 20px side gutters, sections separated by a rule
  with a monospace section number in the accent colour. Must work at 400px wide.
- **Type**: three roles — a grotesque for headings (e.g. Archivo), a humanist sans for body
  (e.g. Source Sans 3), a monospace for **all figures** (e.g. JetBrains Mono) with
  `font-variant-numeric: tabular-nums` so columns align. Google Fonts only, with real fallback
  stacks.
- **Colour**: cool-biased neutrals (not pure grey), one accent used sparingly, and a **separate**
  semantic set for good / warning / critical that is never reused as a series colour.
- **Both themes**: define the complete light palette on bare `:root`; redefine only the tokens
  under `@media (prefers-color-scheme: dark)` guarded as `:root:not([data-theme="light"])`, and
  again under `:root[data-theme="dark"]`. Give `body` an explicit token background.
- **Not everything is a card.** Spend border/fill/shadow by role. Tables are tables.
- **Title**: a short specific noun phrase, two to four words. No explainer after a dash or colon.

### TONE

Write for someone who will interrogate one number and move on. Lead every section with the
conclusion. No hedging adverbs, no "it should be noted". Say "I" for errors. Where the honest
answer is "we don't know", write exactly that and give the reason.

### WHAT I WILL GIVE YOU

Point me at the project's results files and I will produce the page. If a required number is
missing I will tell you which one and stop, rather than estimate it.

## PROMPT — copy to here

---

## Notes for whoever adapts this

- The eight-section spine is the load-bearing part. Sections 04 (errors) and 07 (confidence split)
  are the two most often dropped and the two that most build credibility — keep them.
- If a project has no "before" state, replace §03/§05 with a single "what we tested and why"
  section and keep the numbering.
- If the project genuinely has live results, add a ninth section for them and keep simulated and
  live figures in separate tables. Never merge them.
- The brief is a *standing* document. Re-running it after each research cycle and republishing to
  the same URL is more useful than producing a new deck each time.
