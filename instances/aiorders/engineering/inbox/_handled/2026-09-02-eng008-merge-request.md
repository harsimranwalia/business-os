---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-008
recommendation: merge — migration, code review (round 3), quality, and security all passed on the revised diff (accepts_barter dropped, barter_visit reused directly, per your own correction on the original merge request); additive-only change (staff_rating, collaboration_count, accepts_paid — two new nullable/defaulted columns plus one backfilled boolean — one new admin-gated write route, no schema removal, no new dependency)
pr_urls:
  - repo: aiorders-api
    url: https://github.com/harsimranwalia/aiorders-api/pull/6
  - repo: aiorders-admin-hub
    url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/5
raised: 2026-09-02
notified: 2026-09-02T23:24:37
nudged: 2026-09-04T00:18:02
decision:
---

# Merge request — Influencer board admin management (ENG-008), revised

Same ticket as your `changed` reply on 2026-08-31 — both PRs stay open,
updated in place, not reopened.

## What changed since your last reply

You flagged the original diff's new `accepts_barter` column as redundant
with the existing `barter_visit` boolean. Fixed exactly as you described:
`accepts_barter` dropped everywhere (migration, handler, tests, frontend);
every read/write that targeted it now targets `barter_visit` directly,
using the same null-safe handling `accepts_paid` already had (an unset
preference stays unset — no fabricated value, nothing written until staff
actually check a box). `accepts_paid` is unchanged — it has no pre-existing
column, so it stays new.

## What this does (current shape)

Staff managing the admin panel's influencer board can now see and edit an
influencer's region and campaign-type (paid/barter) preferences, rate an
influencer, and track a collaboration count — the Influencer Management
page was previously 100% read-only with no save path anywhere.

- `aiorders-api`: adds `staff_rating` (1-5), `collaboration_count`, and
  `accepts_paid` columns on `influencers`, backfilled additively (null
  stays null). Barter preference is read/written on the existing
  `barter_visit` column — no new column for it. New `GET`/`PATCH
  admin-portal/influencers/{id}`, admin/sub-admin gated, field-allowlisted.
- `aiorders-admin-hub`: adds an edit form to the existing (previously
  read-only) influencer detail dialog — region, paid/barter + min payment,
  rating, collaboration count. Payment Type badge now reads
  `accepts_paid`/`barter_visit`.

## Gates passed (round 3, on the revised diff)

- Migration: **pass** — `agents/database/migrations/ENG-008-influencer-profile-admin-management.md`,
  amended in place to record your correction. Additive only; no live
  Postgres reachable from the build host, verified via read-only Supabase
  MCP against the real schema and live row distribution (306 rows:
  226/29/51 split on `barter_visit`).
- Code review: **pass, round 3** — `agents/principal-engineer/reviews/ENG-008.md`.
  Round 1 failed on a missing failure-case test plus a null-handling bug
  (both fixed in round 2); round 3 reviewed the `accepts_barter →
  barter_visit` rename specifically and mutation-tested the renamed
  validation by hand (reverted the guard, confirmed exactly one test goes
  red, reverted back clean).
- Quality: **pass** — `agents/qa/test-plans/ENG-008.md`. All 8 acceptance
  criteria covered. This host has `deno` on `PATH` for the first time on
  this ticket — `deno test` actually executed: 19/19 pass, not hand-traced.
- Security: **pass, round 3** — `agents/security/reviews/ENG-008.md`. The
  rename touches no auth-check function (confirmed by diff); `barter_visit`
  sits behind the same shared gate every other field on this allowlist
  already uses; negative-auth cases re-run for real (19/19, both
  auth-critical cases green); no secrets on either new commit.

## PRs (updated in place, same PR numbers as before)

- `aiorders-api` (schema + endpoint): https://github.com/harsimranwalia/aiorders-api/pull/6
- `aiorders-admin-hub` (edit form): https://github.com/harsimranwalia/aiorders-admin-hub/pull/5

Both projects are registered **L1** — merge whenever suits you on GitHub
directly, in either order; the next build-loop pass detects each merge
itself (local git ancestry, no reply needed from you) and advances the
ticket once both are in.

## Named gaps, carried forward rather than hidden

- **Raw `error.message` returned on a 500** (both new handler branches) —
  2nd tracked occurrence of this finding class at this gate; not yet
  three-strike.
- **No automated frontend test** on `aiorders-admin-hub` — no test
  framework, no `test` script, zero test files anywhere. Already proposed
  (`agents/eng-manager/proposals.md`).
- **`min_visit_payment` stale-value-on-uncheck** (P3, has a workaround) —
  named in code review and security, not fixed here (outside this ticket's
  acceptance criteria).
- **Architect's design doc still describes the pre-revision `accepts_barter`
  shape** — prose drift only, flagged for the architect; the running code
  and both PRs above are correct.

## Two related items intentionally not filed yet

Per this ticket's own PRD scope split: the influencer-facing region/
campaign-type gated opportunity visibility (item 4 of the original request)
depends on these preference fields existing and will be filed once this
ticket verifies. The "engagement" item is a separate, already-answered
standing question (see `ENG-009`), not part of this ticket.

## Decision

Filled in by you.
