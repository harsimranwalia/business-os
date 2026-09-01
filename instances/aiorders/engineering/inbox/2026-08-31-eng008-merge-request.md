---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-008
recommendation: merge — migration, code review (round 2), quality, and security all passed; additive-only change (two new nullable/defaulted columns, backward-compatible backfill, one new admin-gated write route, no schema removal, no new dependency)
pr_urls:
  - repo: aiorders-api
    url: https://github.com/harsimranwalia/aiorders-api/pull/6
  - repo: aiorders-admin-hub
    url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/5
raised: 2026-08-31
notified: 2026-08-31T11:15:29
nudged: 2026-09-01T22:41:10
decision:
---

# Merge request — Influencer board admin management (ENG-008)

Third two-repo ticket on this board (after `ENG-011`, `ENG-013`) — one ticket, two PRs, both opened this pass.

## What this does

Staff managing the admin panel's influencer board can now see and edit an
influencer's region and campaign-type (paid/barter) preferences, rate an
influencer, and track a collaboration count — the Influencer Management page
was previously 100% read-only with no save path anywhere.

- `aiorders-api`: adds `staff_rating` (1-5) and `collaboration_count` columns
  on `influencers`; splits the single `barter_visit` boolean into independent
  `accepts_paid`/`accepts_barter` flags so "both" is representable, backfilled
  additively (`barter_visit` itself untouched). New `GET`/`PATCH
  admin-portal/influencers/{id}`, admin/sub-admin gated, field-allowlisted.
- `aiorders-admin-hub`: adds an edit form to the existing (previously
  read-only) influencer detail dialog — region, paid/barter + min payment,
  rating, collaboration count. Payment Type badge now reads the two new flags.

## Gates passed

- Migration: **pass** — `agents/database/migrations/ENG-008-influencer-profile-admin-management.md`. Additive only (two new nullable/defaulted columns plus two backfilled flags), no RLS change (service-role client, same as every other admin write path). No live Postgres reachable from the build host; verified instead via a read-only Supabase MCP connection against the real production schema and live row distribution (306 rows: 226/29/51 split on `barter_visit`).
- Code review: **pass, round 2** — `agents/principal-engineer/reviews/ENG-008.md`. Round 1 failed on automatic-failure #10 (no failure-case test on the new authz-gated write path) plus a real null-handling bug (a null preference was silently fabricated to `accepts_paid: true` on open, and could be written on any unrelated save); both closed in round 2.
- Quality: **pass** — `agents/qa/test-plans/ENG-008.md`. All 8 acceptance criteria covered.
- Security: **pass** — `agents/security/reviews/ENG-008.md`. OWASP A01-A10 walked; all negative-auth cases (no-token, wrong-role, missing-profile) traced with mutation-sensitive assertions; no IDOR; no secrets; no new dependency; no privilege elevation — new write population is identical to the existing read population.

## PRs

- `aiorders-api` (schema + endpoint): https://github.com/harsimranwalia/aiorders-api/pull/6
- `aiorders-admin-hub` (edit form): https://github.com/harsimranwalia/aiorders-admin-hub/pull/5

Both projects are registered **L1** — this department opens the PR, a human
merges. Merge whenever suits you on GitHub directly, in either order if you'd
rather not sequence them (the frontend simply has nothing new to call until
the backend PR lands; the backend alone changes nothing observable to staff
until the frontend calls it); the next build-loop pass detects each merge
itself (local git ancestry check, no reply needed from you) and advances the
ticket once both are in.

## Named gaps, carried forward rather than hidden

- **Raw `error.message` returned on a 500** (both new handler branches) —
  2nd tracked occurrence of this finding class at this gate (security review,
  A05); not yet three-strike.
- **No automated frontend test** on `aiorders-admin-hub` — this repo has no
  test framework, no `test` script, and zero test files anywhere (confirmed
  fresh this ticket). A proposal sizing the fix is filed
  (`agents/eng-manager/proposals.md`).
- **`min_visit_payment` stale-value-on-uncheck** (P3, data-integrity, has a
  workaround) — named in both code review and security review, not fixed in
  this ticket (outside its 8 acceptance criteria).
- **No live Postgres or `deno test` run on this host** — same host-tooling
  gap `ENG-007`/`ENG-011`/`ENG-013` already recorded. All 19 backend test
  cases and the frontend fix were hand-traced against the code at HEAD
  instead of executed; zero discrepancies found across three independent
  passes (round 1 fix, round 2 review, security review).

## Two related items intentionally not filed yet

Per this ticket's own PRD scope split: the influencer-facing region/
campaign-type gated opportunity visibility (item 4 of the original request)
depends on these preference fields existing and will be filed once this
ticket verifies. The "engagement" item is a separate, already-answered
standing question (see `ENG-009`), not part of this ticket.

## Decision

Filled in by the approver.
