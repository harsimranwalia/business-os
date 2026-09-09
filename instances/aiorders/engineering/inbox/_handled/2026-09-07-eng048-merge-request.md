---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-048
recommendation: merge — code review, quality, and security all passed (security: zero blocking findings, one adjacent P0 filed separately as ENG-050); migration gate passed, rollback actually run twice against a disposable replica; first sub-ticket of the ENG-027 family, unblocks ENG-049
time_estimate: half a day
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/21
raised: 2026-09-07
notified: 2026-09-07T16:18:23
nudged: 2026-09-08T09:52:23
---

# Merge request — Loyalty ledger schema, credit function, and auto-complete cron (ENG-048)

Sub-ticket of `ENG-027` (loyalty points ledger and earn), sequence 1 of 2, a
strict chain — no dependency of its own; `ENG-049` (webhook, sweep, dine-in
earn API) depends on this ticket alone and cannot be built against real
tables/functions until this ships.

## What this does

- Adds `loyalty_ledger_entries` — append-only, unique `order_id`
  (nullable-safe), three cross-field `CHECK`s tying shape to `source`,
  indexed on `(platform_customer_id, restaurant_id)` for the balance/history
  read.
- Adds two nullable `orders` columns: `cw_order_id` (unique when present,
  closes the CloudWaitress-order join-key gap) and `loyalty_processed_at`.
  Both populate only going forward — no backfill.
- Adds `credit_order_if_eligible(order_id, fulfillment_reason)` — one
  Postgres transaction doing guard, identity resolution, rate resolution,
  ledger insert, and the `orders` update. The single code path `ENG-049`'s
  webhook handler and sweep will both call.
- Schedules `loyalty-auto-complete-tick` (`*/15 * * * *`, `pg_cron`/
  `net.http_post`, per `ADR-021` — reuses `ADR-018`'s own poller shape).

## Gates passed

- **Code review: pass, round 2** — `agents/principal-engineer/reviews/ENG-048.md`.
  Round 1 found two blocking issues (below); both fixed and independently
  re-verified against a fresh disposable replica.
- **Quality: pass, round 2** — `agents/qa/test-plans/ENG-048.md`. This
  ticket's fully-owned criteria (AC4, AC5, AC8, AC9, AC12) and the
  guard/crediting half of seven others covered; both round-1 failing rows
  re-tested and now pass.
- **Security: pass** — `agents/security/reviews/ENG-048.md`. Zero blocking
  findings. Full OWASP walk, threat model, secrets scan clean, no new
  dependencies. Two forward-looking notes for `ENG-049`'s own gate (webhook
  signature verification; wrong-tenant case at the handler layer) — not this
  ticket's to close.
- **Migration: pass** — `agents/database/migrations/ENG-048-loyalty-ledger-schema-credit-function-and-cron.md`.
  Live-schema and Vault checks run fresh; every function branch exercised
  against a disposable replica by direct query; rollback actually run twice.

## Fix history (round 1 → round 2)

- **B1 — access control.** Shipped with no `GRANT`/`REVOKE` at all;
  `anon`/`authenticated` could call the function directly. Review's own
  literal fix (`revoke ... from public`) was tested, not trusted, and found
  **not** to close the hole on this project — `pg_default_acl` grants
  `EXECUTE` to `anon`/`authenticated` **by name** at function-creation time,
  a separate mechanism a `PUBLIC`-only revoke can't reach. Fixed by naming
  the roles directly; re-verified four independent times, including an
  actual `set role anon` call returning `permission denied`.
- **B2 — negative amount.** `bill.discount > bill.cart` produced a negative
  ledger row. Fixed with `greatest(cart - discount, 0)`.

**Adjacent finding, filed separately as `ENG-050` (P0, not part of this PR):**
re-deriving the `pg_default_acl` mechanism surfaced that two pre-existing,
unrelated functions on this same live project (`calculate_platform_analytics`,
`get_acquisition_breakdown`) carry the identical gap today, callable by
`anon` with no login. Already in `inbox/` as its own P0 — no action needed
here beyond awareness.

## Release readiness

- **Rollback:** tested, not reasoned — run twice against a disposable local
  replica (`supabase/postgres:15.8.1.073`), pre- and post-`CONCURRENTLY` fix,
  both confirmed clean: zero relations, zero cron jobs, both `orders` columns
  dropped, function removed from `pg_proc`.
- **Observability:** the cron body calls `net.http_post` unconditionally on
  every 15-minute fire — it does not check for eligible rows first. Until
  `ENG-049` deploys the `loyalty-auto-complete` edge function, every tick
  will 404 at Supabase's edge-routing layer, and this is not observable
  today (`net.http_post` is fire-and-forget; `cron.job_run_details` records
  the tick, not the HTTP outcome). Unlike `ENG-037`'s own
  `broadcast-dispatch-tick`, there is only one failure window here, not two
  — the `service_role_key` Vault secret this job needs already exists live.
  Judged non-blocking, same reasoning already established on `ENG-037`/
  `ENG-038`: no CI/CD auto-deploy on this repo (merging this PR does not
  push the migration live — that's a separate, deliberate `supabase db push`),
  nothing external reads or writes this path yet, and the gap closes the
  moment `ENG-049` ships.
- **Cost:** $0/month — same Supabase project, `pg_cron`/`pg_net`/Vault
  already in live use elsewhere, one new table and two nullable columns are
  storage-negligible, a 404'd call invokes no billable compute.
- **Window:** n/a — `aiorders-api` is registered L1; opening a PR is not a
  release.

## PR

https://github.com/harsimranwalia/aiorders-api/pull/21

This project is registered **L1** — this department opens the PR, a human
merges. The next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket.

## Non-blocking findings, named not fixed

- Append-only table has no DB-enforced `REVOKE` of `UPDATE`/`DELETE` from
  `service_role` (comment-only enforcement, same pre-existing pattern this
  project's other "append-only" table already has) — filed as a proposal,
  not fixed here; introducing that lockdown on this ticket alone would be an
  unprecedented pattern on this project.
- A malformed/non-numeric `bill.cart`/`bill.discount` retries forever — an
  accepted shape the design already names for any sweep failure, not a gap.

## Out of scope

- The webhook handler, the sweep itself, and the dine-in earn API — all
  `ENG-049`.
- Any frontend — schema and RPC only, per the design's own non-goals.

First of `ENG-027`'s two sub-tickets, a strict chain. `ENG-049` depends on
this ticket alone; per the corrected reading of the never-idle guard
(`eng_build_loop.md`, amended 2026-09-07), that dependency is satisfied now
that this PR is open — `ENG-049` does not wait for `verified`. Chained in
the same pass this item was raised, as a stacked PR off this ticket's own
branch.
