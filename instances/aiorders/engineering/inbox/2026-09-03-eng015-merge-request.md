---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-015
recommendation: merge — code review (round 2), quality, security, and migration
  all passed; P1 fix for a live cross-tenant restaurant-visibility/write
  exposure plus a broken add-location path; two repos, must land together
  (see Named gaps)
time_estimate: half a day to a day
pr_urls:
  - repo: aiorders-api
    url: https://github.com/harsimranwalia/aiorders-api/pull/10
  - repo: aiorders-admin-hub
    url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/8
raised: 2026-09-03
notified: 2026-09-03T10:03:53
nudged:
decision:
---

# Merge request — Agency/reseller (partner) users: brand-scoped locations and a working add-location path (ENG-015)

## What this does

A partner-admin/partner-user (this codebase's existing name for
agency/reseller) previously saw and could fetch/update **every** restaurant
on the platform — a live cross-tenant data exposure — and could not
successfully add a new restaurant under their own brand at all (the write
was silently rejected). This fixes both: a partner now sees and can add
only restaurants under brand(s) assigned to them (`brands.partner_id`),
enforced server-side, not just in the UI. A partner-created restaurant lands
held for staff review (`approved: false`), not auto-approved. Staff
(`admin`/`sub-admin`) visibility and workflow are byte-for-byte unchanged.

Two round-1 findings (a partner could self-approve their own held restaurant,
and could reassign it to a brand they don't own — both via unfiltered
mass-assignment on `updateRestaurant`) were found by code review, fixed, and
closed with mutation-verified regression tests before this request was
raised.

## Gates passed

- Code review: **pass, round 2** — `agents/principal-engineer/reviews/ENG-015.md` (round 1 failed on zero test coverage plus the mass-assignment bug above; both closed)
- Quality: **pass** — `agents/qa/test-plans/ENG-015.md` (AC1/AC2/AC6 covered by 22 automated tests; AC3/AC4/AC5 — the add-location write path — de-risked by a full static trace of the table's RLS history, not executed; no live Postgres reachable this pass)
- Security: **pass** — `agents/security/reviews/ENG-015.md` (OWASP A01–A10 walked, zero blocking findings; one non-blocking finding below)
- Migration: **pass** — `agents/database/migrations/ENG-015-agency-reseller-brand-scoping.md` (additive-only RLS `INSERT` policy, no schema change, no backfill, no coexistence window; rollback is a single `DROP POLICY`)

## PRs

- `aiorders-api` (opened first — the backend endpoints the frontend depends on): https://github.com/harsimranwalia/aiorders-api/pull/10
- `aiorders-admin-hub`: https://github.com/harsimranwalia/aiorders-admin-hub/pull/8

Both projects are registered **L1** — this department opens the PR, a human
merges. **These two must land together**, not independently — the backend
PR's new RLS policy is what makes the frontend PR's `approved: false` change
load-bearing rather than cosmetic; either one alone leaves a partner insert
either silently auto-approved (today's actual bug) or unconditionally
rejected. Merge whenever suits you on GitHub directly, but merge both before
either one is considered done; the next build-loop pass detects each merge
itself (local git ancestry check, no reply needed from you) and advances the
ticket once both are in.

## Named gaps, carried forward rather than hidden

- **No live Postgres reachable at any hop on this ticket** (build, fix,
  review, QA, security, migration) — this instance's standing host-tooling
  gap. Every claim about the new RLS policy's runtime behavior comes from
  reading tracked migration history directly, not execution.
- **Security review's one non-blocking finding:** whether row-level security
  is actually *enabled* on `public.restaurants` at all — one layer beneath
  the policy-logic trace QA already ran — is unverified from this repo; the
  table predates tracked migration history entirely (the same
  untracked-schema-history gap `ADR-006` already names for `brands`). Not
  fixed blind (a defensive RLS-enable would be an unbounded-blast-radius
  change across four frontends). **Recommended, not gating:** a manual
  staging smoke test before or immediately after merge — a test partner
  account attempts to add/update a restaurant, confirm the row is actually
  rejected or lands held, never unrestricted. That one check empirically
  proves the whole chain at once.
- **Verbose `error.message` in this file's catch blocks** (pre-existing,
  unchanged by this diff) — already tracked under `ENG-009`'s standing
  proposal, not re-proposed here.

## Decision

Filled in by the approver.
