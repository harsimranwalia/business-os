---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-013
recommendation: merge — migration, code review (round 2), quality, and security all passed; additive-only change (one nullable column, two new gate-reuse write routes, no schema removal, no new dependency)
pr_urls:
  - repo: aiorders-api
    url: https://github.com/harsimranwalia/aiorders-api/pull/5
  - repo: aiorders-admin-hub
    url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/4
raised: 2026-08-31
notified: 2026-08-31T11:05:16
nudged: 2026-09-01T22:41:10
decision: changed
decided: 2026-09-01T17:13:54.293916+00:00
---

# Merge request — Foodswipe funnel page, staff-settable pipeline stages (ENG-013)

Second two-repo ticket on this board (after `ENG-011`) — one ticket, two PRs, both opened this pass.

## What this does

Sales/onboarding staff can now set (and reset) a Foodswipe listing's pipeline
stage directly on the admin funnel page, instead of the page being 100%
read-only.

- `aiorders-api`: adds a nullable `foodswipe_stage_override` column on
  `profiles`, and two new write routes (`stage/set`, `stage/reset`) behind
  the handler's existing admin/sub-admin gate, scoped to
  `source = 'foodswipe'`. The existing kanban read now prefers the override
  over the automatic `classifyStage()` derivation when one is set.
- `aiorders-admin-hub`: adds a "Set stage" / "Reset to automatic" dropdown
  and a "Manually set" badge to each kanban card on the Foodswipe funnel
  page.

## Gates passed

- Migration: **pass** — `agents/database/migrations/ENG-013-foodswipe-funnel-stage-control.md`. Additive nullable column, no default, no backfill, no RLS change (writes go through the service-role client, same as every other admin write path). No live Postgres reachable from the build host; verified instead via a read-only Supabase MCP connection against the real production schema.
- Code review: **pass, round 2** — `agents/principal-engineer/reviews/ENG-013.md`. Round 1 failed on automatic-failure #10 (no failure-case test on the new authz-gated write path); closed in round 2 with 17 test cases including a mutation-sensitive test on the tenant-scoping line.
- Quality: **pass** — `agents/qa/test-plans/ENG-013.md`. All 5 acceptance criteria covered; 8 failure-path scenarios documented (2 intentionally untested — idempotent reset, concurrent-write-last-wins-by-design).
- Security: **pass** — `agents/security/reviews/ENG-013.md`. OWASP A01–A10 walked (2 reviewed in full, 8 n/a with reason); all three negative-auth cases (no-token, wrong-role, wrong-tenant) traced; no secrets; no privilege elevation — the new write population is identical to the existing read population.

## PRs

- `aiorders-api` (opened first — the backend endpoints the frontend depends on): https://github.com/harsimranwalia/aiorders-api/pull/5
- `aiorders-admin-hub`: https://github.com/harsimranwalia/aiorders-admin-hub/pull/4

Both projects are registered **L1** — this department opens the PR, a human
merges. Merge whenever suits you on GitHub directly, in either order if
you'd rather not sequence them (both directions degrade gracefully — the
frontend simply has nothing to call until the backend PR lands, and the
backend alone changes nothing observable to staff); the next build-loop pass
detects each merge itself (local git ancestry check, no reply needed from
you) and advances the ticket once both are in.

## Named gaps, carried forward rather than hidden

- **Raw `error.message` returned on a 500** (both new write actions) — first
  tracked occurrence of this finding class (security review, A05); not
  blocking, not yet a three-strike pattern.
- **No audit trail** for who set an override or when — already named and
  accepted as out-of-scope by the architect's own design.
- **No live Postgres or live frontend session exercised this pass** — same
  host-tooling gap `ENG-007`/`ENG-011` already recorded. All 17 backend test
  cases and the frontend's interaction logic were hand-traced against the
  code at HEAD instead of executed; zero discrepancies found by three
  independent passes (round 1 fix, round 2 review, security review).

## Decision

Filled in by the approver.

## Decision

**changed** — 2026-09-01T17:13:54.293916+00:00

You added manual update of stage to the card what about the funnel stages itself on the page, if I want custom pipeline flow stages not just per card. This ticket was meant to allow custom pipeline stages for the whole foodswipe funnel, the stage updates per card can be manual or automatic

---

**Processed 2026-09-02**, `watch` event pass (context `launchd`) — recorded
on a different host/checkout, only reached this Mac via tonight's `1b72b26`
merge. This reply's own scope question (ship what's built and file the
larger ask separately, or hold and fold it in) is genuinely ambiguous —
asked rather than guessed:
`inbox/2026-09-02-eng013-stage-config-question.md`. Full reasoning on
`ENG-013`'s own board file. Journaled in
`agents/eng-manager/config/decision-journal.md`.
