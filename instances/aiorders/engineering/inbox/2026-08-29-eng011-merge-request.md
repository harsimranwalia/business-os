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
decision:
---

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
