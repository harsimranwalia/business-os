---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-044
recommendation: merge — code review, quality, and security all passed (security: zero findings); migration gate passed, rollback for both migrations actually run and confirmed against a disposable replica; first sub-ticket of the ENG-026 family, unblocks ENG-045 and ENG-046
time_estimate: a few hours
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/19
raised: 2026-09-07
notified: 2026-09-07T03:48:06
nudged:
decision: merged
---

# Merge request — FoodSwipe channel-visibility columns and discovery-RPC channel gate (ENG-044)

Sub-ticket of `ENG-026` (FoodSwipe channel-visibility toggles and
capability-based discovery), sequence 1 of 4 — no dependency, first of the
family to build. `ENG-045` (backend) and `ENG-046` (frontend, admin-hub) both
depend on this ticket alone.

## What this does

- Three new `NOT NULL` boolean columns on `public.restaurants` —
  `has_order_food` (default `true`), `has_dine_in` (default `false`),
  `has_catering` (default `false`) — backfilled for every existing row from
  live data, not just defaulted (`has_catering` from `live_catering`;
  `has_dine_in` from the pre-existing, live `dine_in` column, confirmed
  present via a live-schema check rather than assumed dead).
- `get_restaurants_optimized` gains a `p_channel text default null` parameter
  and `opening_hours` in `RETURNS TABLE`; omitting the parameter reproduces
  today's exact behavior (tested, not just asserted by construction).
- Ports the function's full definition into `aiorders-api`'s own migration
  history — it previously lived only in `restaurant-marketplace`'s history,
  un-tracked from the repo where it actually runs (`ADR-003`'s
  migration-ownership call, completed here, not re-decided).

## Gates passed

- **Code review: pass** — `agents/principal-engineer/reviews/ENG-044.md`.
  Function port verified byte-for-byte against the real 2024 source; `DROP
  FUNCTION` signature confirmed against the true original; the one live
  caller traced and confirmed unaffected.
- **Quality: pass** — `agents/qa/test-plans/ENG-044.md`. AC1 and AC5 (this
  ticket's owned criteria) covered by inspection, live evidence, and
  call-site trace; no suite exists for `aiorders-api` (open proposal,
  unrelated to this ticket).
- **Security: pass, zero findings** — `agents/security/reviews/ENG-044.md`.
  Threat-modelled the diff; independently re-diffed the ported function
  against `restaurant-marketplace`'s real source; confirmed the channel
  predicate only narrows the pre-existing `approved`/`show_in_marketplace`
  gate, never widens it; re-confirmed the re-issued `grant execute` matches
  the original verbatim.
- **Migration: pass** — `agents/database/migrations/ENG-044-foodswipe-channel-visibility-schema.md`.
  Live-schema check run before writing the backfill (not guessed); a real
  Postgres overload-resolution defect caught by testing (a bare `CREATE OR
  REPLACE` with a changed arg count creates a silent second overload rather
  than erroring) and closed by a leading `DROP FUNCTION IF EXISTS`; both
  migrations verified end-to-end against a disposable replica, both
  rollbacks actually run and confirmed.

## Release readiness

- **Rollback:** tested, not just reasoned — both migrations' rollbacks
  actually run against a disposable local replica
  (`supabase/postgres:15.8.1.073`): the function reverts to exactly 13 args
  with the old call shape still working, and all three columns confirmed
  dropped.
- **Observability:** the one existing caller
  (`aiorders-api/supabase/functions/restaurant-marketplace/handlers/restaurants.ts`'s
  `handleRestaurantDiscovery`) already wraps this RPC call in error
  handling — logs via `console.error('Restaurant discovery error:', error)`
  and automatically falls back to a simpler query on a Postgres `42883`
  (undefined function) error, exactly the failure class a signature mismatch
  would raise. Pre-existing, not added by this ticket, but directly
  relevant: confirmed via disposable-replica testing that this migration
  doesn't trigger that path (old call shape still resolves to a single,
  correct function post-migration). No new reachable behavior yet either
  way — nothing calls with a non-null `p_channel` until `ENG-045` ships.
- **Cost:** $0/month — same Supabase project, three boolean columns and one
  function replacement, no new service, no index, matches the design's own
  "Recurring cost: None."
- **Window:** n/a — `aiorders-api` is registered L1; opening a PR is not a
  release.

## PR

https://github.com/harsimranwalia/aiorders-api/pull/19

This project is registered **L1** — this department opens the PR, a human
merges. The next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket.

## Non-blocking findings, named not fixed

None. Security review reported zero findings, blocking or non-blocking — the
free-text, unvalidated `p_channel` parameter matches this function's own
long-standing pattern (every other filter parameter has always been
unvalidated free text/array too) and degrades to zero rows on an
out-of-enum value, never an error.

## Out of scope

- `admin-portal/handlers/restaurants.ts` — already passes the three new
  fields through with zero code change, per the design.
- Any frontend — schema and RPC only.
- `restaurant-marketplace`'s own copy of the ported function — becomes
  historical, left in place, not deleted (design's own Risks).

First of `ENG-026`'s four sub-tickets. `ENG-045` and `ENG-046` both depend on
this one alone and stay `ready` until this ticket reaches `verified` — noted
so whichever pass finds the merge knows to check them next.
