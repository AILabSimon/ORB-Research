# Claude scheduled instruction check (fallback poller)

## Why this isn't already live

The Claude GitHub App/action used in this repo cannot modify files under
`.github/workflows/` — that permission is withheld by design (a GitHub App
without the `workflows` OAuth scope cannot push changes there, and this one
doesn't have it). So the scheduled-check workflow is staged here instead of
being installed directly.

**To activate it:** move (not copy, so this stays out of `.github/workflows/`
in git history going forward) the workflow file into place and commit it:

```
git mv .github/claude-scheduler/scheduled-check.workflow.yml .github/workflows/claude-scheduled-check.yml
git commit -m "Enable Claude scheduled instruction check"
git push
```

That's the one manual step required — everything else (detection logic,
state tracking, invocation) is already implemented in that file.

## What it does

- Runs on a cron schedule (every 3 hours, see the `on.schedule` cron in the
  workflow) plus `workflow_dispatch` for manual testing.
- Each run makes a single `gh api` call listing recent issue/PR comments
  repo-wide and checks, for the newest non-bot comment containing `@claude`
  on each thread, whether a `claude[bot]` comment already exists later in
  that same thread. If so, the live event trigger (`.github/workflows/claude.yml`)
  already handled it and the run exits — no Claude invocation, no commit.
- If an `@claude` comment has no later bot reply, it's treated as missed by
  the live trigger. The workflow invokes `anthropics/claude-code-action`
  directly with a `prompt` (this repo's own `claude.yml`/`claude-code-review.yml`
  already document `prompt` as the supported override input) pointing Claude at
  that specific comment/issue, so it's processed through the normal repository
  workflow rather than the live event path.
- After firing, it records the fired comment's id in `state.json` and commits
  that file, so a second scheduled run inside the same window (e.g. while the
  first Claude job is still running) won't fire again on the same comment.

## UNVERIFIED: whether the trigger step actually works end-to-end

This is the one part of the design I could not validate, and it is the most
important limitation to know about before trusting this unattended.

`anthropics/claude-code-action`'s normal flow is: a live event (issue_comment,
issues, pull_request_review*) arrives with `github.event.issue` / `.pull_request`
populated, and the action creates/updates a tracking comment on that object
automatically. A `schedule` (or manually-run `workflow_dispatch`) trigger has
**no such event context** — there is no issue or PR attached to the workflow
run itself. This workflow works around that by telling Claude, in the `prompt`
text, which issue to fetch and which issue to comment back on, relying on
Claude's own `gh`/GitHub-comment tool access (already granted via the
`issues: write` permission above) to act on it directly rather than relying on
the action's automatic event-bound comment tracking.

I could not confirm this actually works, for two compounding reasons:
1. This sandbox has no network access to fetch `anthropics/claude-code-action`'s
   docs/source and confirm how it behaves with no native event context, or
   whether `prompt` alone is sufficient vs. requiring something like a synthetic
   event payload.
2. This sandbox cannot execute GitHub Actions workflows (only `claude-code-action`
   invocations wrapped around a live issue/PR event can be observed this way) —
   so there's no way to dry-run this workflow to see what actually happens.

**Before relying on this unattended:** once the workflow is moved into
`.github/workflows/`, trigger it once manually with `workflow_dispatch` against
a known-missed comment (or a synthetic one) and confirm Claude actually posts a
reply to the right issue. If it doesn't, the fallback trigger step needs a
different mechanism than a bare `prompt` override — do not assume it works
just because the file is in place and the cron fires.

## Scope limitation

Detection only reads the `issues/comments` REST endpoint (issue comments and
PR conversation comments — this covers how every instruction in this repo so
far, including this one, has actually been sent). It does **not** see inline
PR review comments (`pull_request_review_comment`) or whole-PR reviews
(`pull_request_review`), even though `.github/workflows/claude.yml` does
listen for `@claude` in those. If an instruction only ever arrives that way
and the live trigger misses it, this fallback will not catch it.

## What it deliberately does NOT do

- It does not invent research tasks. If nothing is missed, it does nothing.
- It does not replace or duplicate `.github/workflows/claude.yml` — that stays
  the primary, instant trigger. This is a fallback only.
- It does not guarantee zero overlap with a live-triggered run: GitHub Actions
  concurrency groups only serialize workflows that share the same `group`
  name, and `claude.yml` cannot be edited (same restriction as above) to add
  a matching group. In practice this is a narrow race — the bot-reply check
  above already prevents firing on anything the live trigger has finished (or
  even just started replying to) — but a scheduled run that starts in the
  few-second gap between a live trigger firing and Claude's first comment
  appearing could theoretically fire twice for the same instruction. This is
  a real, acknowledged limitation, not something this design fully closes.

## Cost when there's nothing new

One `actions/checkout` (shallow) + one `gh api` call + some `jq` parsing.
No LLM/Claude invocation, no commit, no comment. This is the "low-usage"
path requested.
