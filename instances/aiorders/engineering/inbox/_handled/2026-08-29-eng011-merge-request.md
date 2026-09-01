---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-011
recommendation: merge — migration, code review, quality, and security all passed; no schema change beyond one additive column, no new endpoint, no new dependency
pr_url: "aiorders-api: https://github.com/harsimranwalia/aiorders-api/pull/3 | aiorders-admin-hub: https://github.com/harsimranwalia/aiorders-admin-hub/pull/3"
raised: 2026-08-29
notified: 2026-08-29T17:04:29
decision: approved
decided: 2026-08-30T01:43:13.118048+00:00
---

---

**Processed 2026-08-30**, `scheduled` event pass (context `launchd`). Never
answered — `decision:` stays empty on record. This item's own text told the
approver a reply wasn't required ("merge whenever suits you on GitHub
directly"), and they took exactly that path: both PRs merged directly,
confirmed independently via git ancestry and `gh pr view` on both repos
(`aiorders-api` PR #3 merged 2026-08-30T00:12:50Z, `aiorders-admin-hub` PR #3
merged 2026-08-30T00:13:30Z). `ENG-011` advanced `blocked → shipped →
verified` this same pass. Full detail on the ticket's own log and
`agents/devops/releases/2026-08-30-ENG-011-aiorders-api-and-admin-hub.md`.
Journaled in `decision-journal.md`.

# Merge request — Client stage & health visibility on the Brands admin page (ENG-011)

First two-repo ticket on this board — one ticket, two PRs, both opened this pass.

## What this does

Admin staff can now see each restaurant's client stage and a minimal health
signal on the Brands page, and filter the list by stage.

- `aiorders-api`: derives `stage`/`health` on the existing admin brands-list
  response; extends `calculate_platform_analytics()` with one additional
  aggregate column (`last_order_at`). No new table, no new vendor.
- `aiorders-admin-hub`: adds a Stage column, a Health column, and a stage
  filter to `Brands.tsx`, following the page's existing filter pattern.

## Gates passed

- Migration: **pass, with a named non-blocking gap** — `agents/database/migrations/ENG-011-client-stage-health-visibility.md`. No live Postgres reachable from the build host (no Docker/psql/supabase CLI); the corrected `DROP FUNCTION`+`CREATE FUNCTION` statement (an earlier `CREATE OR REPLACE` draft was caught and fixed pre-merge — Postgres rejects changing a `RETURNS TABLE` function's columns that way) is verified by reading plus a read-only live-catalog check via Supabase MCP, not by a container dry-run.
- Code review: **pass** — `agents/principal-engineer/reviews/ENG-011.md`
- Quality: **pass**, 12/12 unit tests plus clean builds on both repos — `agents/qa/test-plans/ENG-011.md`
- Security: **pass** — `agents/security/reviews/ENG-011.md`. No new endpoint, no new input surface, no new capability; `stage`/`health` are additive read-only fields behind the existing admin/sub-admin/partner gate.

## PRs

- `aiorders-api` (open **first**, per the code review's recommended deploy order — both directions degrade gracefully to a `-` cell, so this is a preference, not a hard requirement): https://github.com/harsimranwalia/aiorders-api/pull/3
- `aiorders-admin-hub`: https://github.com/harsimranwalia/aiorders-admin-hub/pull/3

Both projects are registered **L1** — this department opens the PR, a human
merges. Merge whenever suits you on GitHub directly, in either order if you'd
rather not sequence them; the next build-loop pass detects each merge itself
(local git ancestry check, no action needed from you beyond merging) and
advances the ticket once both are in.

## Named gaps, carried forward rather than hidden

- No live Postgres or live frontend session was exercised this pass (host has
  no Docker/psql/supabase CLI, and the admin-hub worktree has no `.env`) — the
  decision logic has full unit coverage, but a real Brands-page load has not
  been observed. Worth a post-merge smoke check given this is the first ticket
  to ship to two repos at once.
- KV read fan-out (one Cloudflare KV GET per brand row, per page load) is
  unbatched — fine at today's scale, worth a bulk-read path if brand count
  grows an order of magnitude. Non-blocking, already carried in the code
  review and security review.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-30T01:43:13.118048+00:00

merged

---

**Processed 2026-08-29**, `watch` event pass (context `schtasks`) — found
this item still sitting in `inbox/` well after its own `decided:` timestamp;
earlier same-day passes on `ENG-007` and `ENG-025` had each noticed it in
passing and correctly left it for a pass whose own scope covered it. Not
taken on the "merged" text alone: independently re-derived via `git
merge-base --is-ancestor` in this department's own worktrees for **both**
repos (`aiorders-api`, `aiorders-admin-hub`) against their respective
`origin/main` — both confirmed merged. Deploy itself further confirmed live
(not just merged) via the Supabase MCP connection (migration applied,
`admin-portal` function redeployed and carrying the merged code) and GitHub
Actions run status (`aiorders-admin-hub`'s Cloudflare Pages deploy). Ticket
advanced `blocked → shipped`; full detail on the ticket's own log and
`agents/devops/releases/2026-08-29-aiorders-admin-hub-ENG-011.md`. Journaled
in `agents/eng-manager/config/decision-journal.md`.
