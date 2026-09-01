---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-007
recommendation: merge — code review, quality, security, and migration all passed; additive migration plus one new admin-portal route with no live caller anywhere, so merging and deploying has zero production behavioral effect until tickets 3/4 of the loyalty sequence call it
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/4
raised: 2026-08-29
notified: 2026-08-29T19:32:13
---

# Merge request — Per-restaurant loyalty configuration (ENG-007)

## What this does

Every restaurant can now have an online earn %, a dine-in earn %, and a
redemption value on file, effective-dated, with a full history of what was
true when — no later rate change can alter what an earlier ledger entry's
rate was.

- New table: `restaurant_loyalty_configs` (additive, RLS-enabled, no
  policies — service-role only, same shape as ENG-006's
  `platform_customer_legacy_links`).
- `enforce_loyalty_config_effective_order`: a `BEFORE INSERT` trigger,
  per-restaurant advisory-locked, enforcing strictly-increasing, future-only
  `effective_from` values at the database.
- New `admin-portal/handlers/loyalty-config.ts` (`GET`/`POST`), admin/sub-admin
  only, reusing the router's existing auth. Every decision (role gate, input
  validation, "current as of T" derivation, trigger-error mapping) is pure
  and DB-free — 44 tests.

This is purely additive config for tickets 3/4 of the loyalty sequence
(points ledger, redemption) to compute against. No ledger, no points, no
redemption, and no frontend caller exists anywhere in this diff — same "zero
blast radius until something calls it" shape as ENG-006.

## Gates passed

- Code review: **pass** — `agents/principal-engineer/reviews/ENG-007.md`
- Quality: **pass** — `agents/qa/test-plans/ENG-007.md` (44/44 tests; every
  DB-free decision has direct coverage)
- Security: **pass** — `agents/security/reviews/ENG-007.md` (server-side
  admin/sub-admin gate, negative case tested; no new access-control gap
  beyond this router's own already-accepted model)
- Migration: **pass, with a named verification gap** —
  `agents/database/migrations/ENG-007-per-restaurant-loyalty-configuration.md`
  (additive, rollback written, not live-tested — see below)

## PR

https://github.com/harsimranwalia/aiorders-api/pull/4

`aiorders-api` is registered **L1** — this department opens the PR, a human
merges. Merge whenever suits you on GitHub directly; the next build-loop
pass detects the merge itself (local git ancestry check, no action needed
from you beyond the merge) and advances the ticket to `shipped`.

## Named gaps, carried forward rather than hidden

- **No live/throwaway-Postgres run this pass** — Docker Desktop didn't come
  up in time on the build host. Substituted with a hand-traced verification
  of the trigger's transaction semantics plus direct comparison against
  three already-applied precedents in this exact repo. Materially weaker
  than ENG-006's own container-verified migration.
- **Unbounded history query** (`GET`, no `limit()`) — accepted given the
  domain's real cardinality (a rate change is a rare, deliberate admin
  action, not a per-order event).
- **No rate limit on the write path** (A04) — low risk today since no live
  ledger reads this data yet; worth revisiting once tickets 3/4 exist.

## Decision

Filled in by the approver.

---

**Never formally answered — reconciled 2026-08-29 by a `watch` build-loop
pass, not left standing.** The ticket's own `state:` moved `blocked → shipped`
via a "control center" dashboard action before any reply landed here (same
bypass shape `ENG-002`/`ENG-006` hit); this item was moved to `_handled/` to
match, but `decision:`/`decided:` were never set because no reply ever came
through any channel — unlike `ENG-002` (bypassed, then quiet) or `ENG-006`
(bypassed, then a written "approved" landed minutes later), this one stayed
silent, a third variant of the same gap. Independently confirmed via git
ancestry rather than taken on the control center's say-so: `loyalty-system`
is a merged ancestor of `aiorders-api`'s `origin/main` (commit `93617c6`).
Full reconciliation, release record, and decision-journal entry:
`agents/devops/releases/2026-08-29-aiorders-api-ENG-007.md`,
`agents/eng-manager/config/decision-journal.md`.
