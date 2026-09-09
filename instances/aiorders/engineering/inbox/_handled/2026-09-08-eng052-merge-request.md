---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-052
recommendation: merge — code review, quality, and security all passed (security zero blocking findings, three forward notes filed for ENG-053's own gate); migration gate passed, rollback actually run twice against a disposable replica; sequence 1 of 2 in the ENG-051 (redemption) family — unblocks ENG-053, which this pass has already dispatched as a stacked PR off this branch
time_estimate: half a day
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/24
raised: 2026-09-08
notified: 2026-09-08T14:41:39
nudged:
---

# Merge request — Loyalty redemption ledger widening and redeem_points_if_eligible (ENG-052)

Sub-ticket of `ENG-051` (redemption API and QR issuance/scanning), sequence 1
of 2, no dependency of its own; `ENG-053` (brand-portal `redeem_points`
action) depends on this ticket alone and cannot call a real function until
this ships.

## What this does

- Widens `loyalty_ledger_entries`'s three per-source `CHECK`s to add a
  `redemption` arm; adds `loyalty_ledger_entries_points_sign_by_source`
  (`points < 0` for `redemption`, `points >= 0` for the existing sources);
  adds a nullable-unique `idempotency_key`; widens `rate_applied`
  `numeric(5,2)` → `numeric(10,4)` — a design-vs-live-schema gap found and
  fixed in this same migration (`redemption_value_per_point` is
  `numeric(10,4)`; the old width would have silently truncated a sub-cent
  rate to `0.00`).
- Adds `redeem_points_if_eligible(p_platform_customer_id uuid,
  p_restaurant_id uuid, p_points numeric, p_idempotency_key text,
  p_created_by uuid) returns text` — one guarded, idempotent Postgres
  function structured like `credit_order_if_eligible` (`ENG-048`): rejects
  non-positive points or a missing idempotency key, takes a per-`(diner,
  restaurant)` advisory lock, checks the idempotency key **before** reading
  balance (load-bearing — a genuine retry must replay, not bounce as
  `insufficient_balance`), resolves the effective redemption rate, validates
  the diner exists, checks sufficient balance, inserts one negative-points
  row. `revoke`n from `public`/`anon`/`authenticated` by name, `grant`ed to
  `service_role` only — this project's `pg_default_acl` grants `EXECUTE` to
  `anon`/`authenticated` by name at function-creation time, so a bare
  `revoke ... from public` alone would not have closed it (`ENG-048`'s
  round-1 review found exactly this gap on `credit_order_if_eligible`).

## Gates passed

- **Code review: pass, round 1** — `agents/principal-engineer/reviews/ENG-052.md`.
  0/10 automatic failures. Design conformance confirmed line-by-line. Two
  non-blocking style notes, neither a standard.
- **Quality: pass, round 1** — `agents/qa/test-plans/ENG-052.md`. This
  ticket's fully-owned criteria (AC5, AC6, AC9) and the guard/debit half of
  five others (AC3, AC4, AC7, AC8, AC11) all covered against an
  independently-run disposable-replica matrix. 0 open P0/P1.
- **Security: pass, zero blocking findings** — `agents/security/reviews/ENG-052.md`.
  Full OWASP walk, threat model, secrets scan clean, no new dependencies.
  Access control independently re-verified past the catalog read — an actual
  denied RPC call as both `anon` and `authenticated`. Three forward notes for
  `ENG-053`'s own gate (wrong-tenant case belongs at the handler; the
  redemption code's own bearer-credential shape is unchanged by design; the
  table's pre-existing lack of DB-level `UPDATE`/`DELETE` protection) — none
  of the three from this diff, none blocking here.
- **Migration: pass** — `agents/database/migrations/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function.md`.
  Live-schema checks re-confirmed fresh; every function branch exercised
  against a disposable replica by direct query; rollback actually run twice.

All four gates independently re-verified the same core claims from scratch
(own fixture, own container) rather than accepting a prior gate's write-up —
same standard this project has held since `ENG-048`'s own B1 finding.

## Release readiness

- **Rollback:** tested, not reasoned — run twice against a disposable local
  replica (`supabase/postgres:15.8.1.073`): once forward-then-functional,
  once as a clean rollback run against a zero-row copy to prove the real
  precondition. All twelve statements succeed; schema restored
  character-for-character.
- **Observability:** no gap. Unlike `ENG-048`'s cron (which fired
  unconditionally against a not-yet-existing endpoint), this function has no
  caller of any kind — no cron, no trigger, nothing invokes it — until
  `ENG-053`'s handler is wired in. It is inert, not silently failing.
- **Cost:** $0/month — same Supabase project, no new infrastructure; one
  nullable column and four widened/added `CHECK` constraints are
  storage-negligible at low row counts; no new compute.
- **Window:** n/a — `aiorders-api` is registered L1; opening a PR is not a
  release.

## PR

https://github.com/harsimranwalia/aiorders-api/pull/24

This project is registered **L1** — this department opens the PR, a human
merges. The next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket.

## Out of scope

- The `brand-portal` handler itself, and QR issuance (already satisfied by
  `ENG-006`'s shipped `platform_customers.id`) — both `ENG-053`.
- Any frontend — schema and RPC only, per the design's own non-goals.
- Any change to how points are earned.

Sequence 1 of `ENG-051`'s two sub-tickets. `ENG-053` depends on this ticket
alone; per Guards' 2026-09-07 amendment (an open PR satisfies `depends_on`,
not full `verified`), that dependency is satisfied now that this PR is open.
Dispatched in this same pass as a stacked PR off this ticket's own branch —
see `ENG-053`'s own board-file log once its build hop runs.
