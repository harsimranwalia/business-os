---
id: ENG-048
title: Loyalty ledger schema, credit function, and auto-complete cron
project: aiorders-api
type: feature
size: S
time_estimate: half a day
time_spent: ~1h build hop (recovering and verifying an uncommitted prior attempt, live-schema + vault verification, disposable-replica verification including two full rollback runs and one CONCURRENTLY fix) + ~1h round-1 review/quality hop (failed — see Log) + ~45m round-2 build hop (both fixes, disposable-replica re-verification, one rollback re-run) + ~30m round-2 review/quality hop (pass — independent disposable-replica re-test of both fixes) + ~30m security gate (fourth independent re-verification of B1, disposable replica built from scratch) + ~20m release-readiness hop (gate re-verification, observability/cost analysis, PR + merge request, slot-freed chain to ENG-049) + ~25m merge-detection/release/acceptance hop (found merged mid-pass, migration-live verification, release record, full acceptance walk)
time_remaining:
severity: P3
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-07
updated: 2026-09-08
branch: feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron
depends_on: []
blocks: [ENG-049]
parent: ENG-027
links:
  prd: agents/product-manager/specs/ENG-027-loyalty-points-ledger-and-earn.md
  design: agents/architect/designs/ENG-027-loyalty-points-ledger-and-earn.md
  adrs: ["ADR-021"]
  review: agents/principal-engineer/reviews/ENG-048.md
  test_plan: agents/qa/test-plans/ENG-048.md
  security_review: agents/security/reviews/ENG-048.md
  release: agents/devops/releases/2026-09-08-aiorders-api-ENG-048.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/21
---

## Problem

`ENG-027`'s design needs a permanent per-credit ledger, two additive columns
on `orders` closing the CloudWaitress-order join-key gap, a database-side
crediting function with real idempotency guarantees, and a cron schedule for
the auto-complete sweep — none of which exist yet. `ENG-049` (backend) has
nothing to call or write to until this ships.

## Outcome

`loyalty_ledger_entries` exists — append-only, `order_id` unique when
present — indexed on `(platform_customer_id, restaurant_id)` for the
balance/history read. `orders` carries two new nullable columns,
`cw_order_id` (unique when present) and `loyalty_processed_at`, populated
only for orders inserted after this ships. `credit_order_if_eligible(order_id
uuid, fulfillment_reason text)` exists as one Postgres function doing guard,
identity resolution, rate resolution, ledger insert, and the `orders` update
in a single transaction — the one code path both the webhook and the sweep
call. `loyalty-auto-complete-tick` is scheduled via `pg_cron`/`net.http_post`,
calling `ENG-049`'s edge function on an interval (see Notes — no measured
number exists yet).

## Notes

Design: `agents/architect/designs/ENG-027-loyalty-points-ledger-and-earn.md`
— `## Data`, `## Interfaces` (DB function + cron sections), `## Approach`
(idempotency, the cancellation-vs-credit race). `ADR-021` (reuses `ADR-018`'s
`pg_cron` + `net.http_post` poller shape rather than a per-order Cloudflare
Queue delay) governs this ticket's own cron schedule. It does not govern
`ENG-049`'s edge function — that's an ordinary authenticated HTTP handler
regardless of what calls it, same attribution logic `ENG-026`'s own
work-breakdown used for `ADR-010`.

**One question the design explicitly leaves for build time, not guessed
here:** whether `bill.cart`/`bill.discount` (jsonb, already stored by
`createOrder()`) are dollars or integer cents — the TS interface doesn't
settle it, and getting it wrong makes every balance wrong by a consistent,
invisible factor. Verify against a real captured payload, or CloudWaitress's
own API docs, before writing the points computation inside this function.

**Batch size and tick interval have no measured numbers behind them** — the
design offers `ADR-018`'s own 200-rows/5-minutes only as a starting point,
sized for a different table and a different load. Pick a reasonable default
and say so plainly in the migration's own comment rather than treating
either number as load-bearing; nothing here depends on the exact values.

**Guard clause, exact, from the design:** `WHERE loyalty_processed_at IS NULL
AND status IS DISTINCT FROM 'cancelled'` on the `orders` row. Ordinary
Postgres row-level locking is what makes two concurrent callers (webhook and
sweep) resolve safely — no advisory lock needed, unlike `ENG-007`'s
cross-row race. The `loyalty_ledger_entries.order_id` unique constraint
(nullable-safe) is a second, independent guard against ever double-crediting
one order — this department's first money-adjacent write path, worth
over-enforcing per the PRD's own framing.

**This function never updates or deletes a ledger row, and never will** —
correction is ticket 5's own surface (a new, opposite-signed entry), not
this one's. Keep the schema able to carry a negative `points` value later
even though nothing here ever writes one.

**Live-schema check before finalizing the migration** (same discipline
`ENG-044`'s own build hop used for `has_dine_in`): confirm `bill.cart`/
`bill.discount`'s actual shape against a live payload rather than the TS
interface alone (above), and confirm no existing index already covers
`(platform_customer_id, restaurant_id)` before adding a new one.

**Branch from `origin/main`, not `loyalty-system`.** This ticket's own
parent (`ENG-027`) Notes name a shared branch for the whole five-ticket
sequence — true when written (2026-09-03), before `ENG-006`/`ENG-007` had
merged. Checked fresh this pass: `origin/loyalty-system` is now an ancestor
of `origin/main` with zero unique commits, and `main` has moved 59 commits
ahead since. Branch fresh, same as every other work-breakdown sub-ticket on
this board. Full reasoning: `ENG-027`'s own board-file log and
`agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`.

**AC ownership** (mapped in full in
`agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`): this
ticket owns AC4, AC5, AC8, AC9, and AC12 in full, and half of AC1, AC2, AC3,
AC7, AC11, AC15, and AC16 — the guard/crediting half; the webhook/sweep-caller
half belongs to `ENG-049`. No sub-ticket proves AC1, AC2, AC3, AC7, AC11,
AC15, or AC16 alone — check both together.

## Log

- 2026-09-07 `(created) → building` (eng-manager, `work-breakdown`, `continue
  ENG-027` event pass) — sub-ticket of `ENG-027`, sequence 1, no dependency,
  dispatched straight to `building`, owner `database`. `time_estimate` half
  a day, 0h spent. Machine WIP: part of `ENG-027`'s own family, not a second
  occupant of the `1/1` slot — same reading `ENG-016`/`ENG-019`/`ENG-021`/
  `ENG-026` already established. Full reasoning:
  `agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`.
  `chained: ENG-048` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-048`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-048` appended behind five already-outstanding
  events. This pass (`continue ENG-027`) itself still holds
  `traces/.loop.lock` (pid `75800`) at fire time, so the fire queues rather
  than launches; the drain runs the queue in order the moment this pass
  exits.

- 2026-09-07 `building → in-review` (database, `continue` event pass, context
  `ENG-048`). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
  lanes*, *Guards*). Mode check clean (`.env` → `MODE=active`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-048`: exit 0, clean.

  **Worktree not started fresh — found mid-work from an uncommitted prior
  attempt, per `config/projects.md`'s own instruction for exactly this case.**
  `~/Documents/projects/_eng/aiorders-api` was on
  `feat/ENG-045-foodswipe-channel-visibility-discovery-handlers` (unrelated,
  already-pushed ticket) with this ticket's own migration file already
  present, complete, and **untracked** — no branch, no commit, no log entry
  on this ticket, no plan doc, `traces/.hops-2026-09-07-ENG-048` already `2`.
  Not discarded, not blindly trusted either: independently re-verified this
  pass (below) rather than assumed correct because it looked finished.
  Separately, an **orphaned Docker container** from that same earlier
  attempt (`eng048-pgtest`, running since `20:54:54Z` with the migration
  already applied and two synthetic test rows matching the inherited file's
  own cited arithmetic) was found and removed as routine disposable-test
  cleanup once this pass's own independent replica test superseded it — not
  treated as work to preserve, since a test fixture is rebuildable by
  construction. Full provenance write-up:
  `agents/database/migrations/ENG-048-loyalty-ledger-schema-credit-function-and-cron.md`
  ("Provenance"). `git fetch origin main` then `git switch -c
  feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron origin/main` —
  no work lost, nothing stashed, same remediation `ENG-044`'s own pass used
  for the same class of finding.

  **Live-schema and Vault verification, re-run fresh rather than trusted
  from the inherited file's own comments:** `supabase db dump --linked
  --schema public` plus two narrowly-scoped `supabase db query --linked`
  aggregates (row-count/size estimate, one secret-name existence check —
  never a row-level read of order/customer data). Every FK target and
  column the function reads confirmed against the live dump; no existing
  index anywhere on the project overlaps the new `(platform_customer_id,
  restaurant_id)` composite; `vault.secrets` now carries `service_role_key`
  (did not exist as of `ENG-037`'s own check four days ago — completed
  since). The one claim this pass could not independently re-run live (no
  query path to real order rows in this environment): `bill.cart`/
  `bill.discount` are dollars, not cents — corroborated instead via
  `createOrder()`'s own use of `bill.total` (not `bill.total_cents`) for the
  dollar `total_amount` column, plus the inherited file's own cited example
  reconciling exactly to the cent across four figures. Full numbers:
  `agents/database/migrations/ENG-048-loyalty-ledger-schema-credit-function-and-cron.md`.

  **One real gap found and fixed — not present in the inherited file.**
  `orders` is a live, continuously-written table (~21,905 rows, 140MB,
  confirmed this pass), and the migration's one index on it
  (`orders_loyalty_sweep_idx`) was a plain `CREATE INDEX` — a `SHARE` lock
  for the full scan-and-build, blocking the webhook's own order inserts for
  that window, exactly the "blocking lock on a hot table with no online
  strategy" condition this role's own migration gate names explicitly.
  Changed to `CREATE INDEX CONCURRENTLY IF NOT EXISTS` (rollback's matching
  `DROP INDEX CONCURRENTLY`), confirmed executable under this file's own
  no-explicit-transaction execution shape, and the full amended file
  re-verified end to end afterward. Full reasoning and the measured lock
  time on the one constraint left as a single blocking statement
  (`orders_cw_order_id_key`, 6.6ms against a replica sized to the live row
  count — accepted as-is): same plan doc, "Runtime and locks".

  **Self-tested per this state's own exit condition — against a disposable
  local replica** (`supabase/postgres:15.8.1.073`, same image `ENG-037`'s
  and `ENG-044`'s own passes used), stand-in tables sized from the live
  dump above. Every named function branch exercised and confirmed by direct
  query: `credited` (points computed correctly, `4.5000` on a `cart 100 -
  discount 10` order at 5%), repeat call → `already_processed` with no
  second ledger row, `skipped_no_identity`, `skipped_not_enrolled`,
  cancelled-order guard (blocks, status untouched, zero ledger rows),
  invalid `fulfillment_reason` raises. Both independent double-credit
  guards proven separately: the function's own `loyalty_processed_at` guard,
  and a raw insert bypassing the function entirely rejected by
  `loyalty_ledger_entries_order_id_key`. Both cross-field `CHECK`
  constraints proven with an actual failing insert each. Nullable-safe
  uniqueness on `cw_order_id` proven both ways (two nulls coexist, two
  equal values collide). **Rollback actually run, twice** (pre- and
  post-`CONCURRENTLY`), both confirmed clean — zero relations, zero cron
  jobs, columns confirmed dropped. All containers removed after; nothing
  left running. Full detail:
  `agents/database/migrations/ENG-048-loyalty-ledger-schema-credit-function-and-cron.md`.

  **Artifact enumeration (step 6b):** `grep -rln
  "credit_order_if_eligible\|loyalty_ledger_entries\|cw_order_id\|
  loyalty_processed_at\|loyalty-auto-complete-tick"` across `agents/`
  (instance) and `departments/engineering/`. Hits: `ENG-027` (parent,
  historical), `ENG-049` (sibling, not yet built — every name and call
  signature it uses, e.g. `credit_order_if_eligible(order.id, 'reported')`,
  matches exactly what was built here, no drift), `ADR-021` (governs the
  cron mechanism, consistent), `_index-archive.md` (historical allocation
  note). No conflicting instruction found; nothing to fix.

  **PR body drafted** (`building`'s own exit condition; no PR opened yet —
  L1 opens it at release-readiness):
  - *What it does:* Adds `loyalty_ledger_entries` (append-only, unique
    `order_id`, three cross-field `CHECK`s tying shape to `source`) and two
    nullable `orders` columns (`cw_order_id` unique, `loyalty_processed_at`).
    Adds `credit_order_if_eligible(order_id, fulfillment_reason)` — one
    transaction, guard + identity/rate resolution + ledger insert + order
    update — the single code path `ENG-049`'s webhook handler and sweep will
    both call. Schedules `loyalty-auto-complete-tick` (`*/15 * * * *`,
    `pg_cron`/`net.http_post`, per `ADR-021`).
  - *What it deliberately does not do:* No backfill (both `orders` columns
    populate only going forward). No update/delete path on
    `loyalty_ledger_entries`, ever — a correction is ticket 5's own new,
    opposite-signed entry. Doesn't touch the webhook handler or the sweep
    itself — that's `ENG-049`, which this ticket only unblocks.
  - *Uncertainties:* One inherited claim corroborated rather than freshly
    re-run live (`bill.cart`/`discount` unit — see Verification above);
    non-blocking either way per the gate verdict's own reasoning.
  - *What to review hardest:* the three-way `CHECK` constraints tying
    `source` to `order_id`/`fulfillment_reason`/`created_by` — confirm the
    matrix is actually exhaustive for both `source` values (it is: each
    constraint's own two branches cover `online_order`/`dine_in`
    completely, tested both ways per branch). Second: the `CONCURRENTLY`
    index addition — confirm it doesn't collide with how this project's own
    hosted migration push actually executes (this pass could only confirm
    the local execution model, named as a residual in the plan doc).

  Branch committed (`9fccdad`, 1 file, includes the `CONCURRENTLY` fix
  folded into the same commit before push) and pushed:
  `origin/feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`.

  **1 transition this pass** (`building → in-review`), under the cap of 4 —
  `in-review`/`in-qa` (combined hop, principal-engineer + qa) is a fresh
  session's work per `eng_build_loop.md`'s "a pass stops after `building` on
  purpose." No WIP-cap change: this ticket was already inside the counted
  `ready..ready-to-ship` range at `building`; `in-review` is still inside
  it. Machine WIP still held by the `ENG-027` family, unaffected.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `in-review` needs no approver gate.
  Nothing to nudge.

  **One observation filed** (`observations.md`, this date): the earlier
  uncommitted attempt left more than the untracked file `config/projects.md`
  already anticipates — an orphaned Docker container from its own
  disposable-replica test was still running hours later. `docker ps` isn't
  part of the documented recovery check today, only `git status`; worth a
  proposal if a second orphaned container turns up the same way. The
  `CONCURRENTLY` finding itself stays in this ticket's own log and the
  migration plan doc — reusable schema-review knowledge, not a
  department-process gap.

  `chained: ENG-048` — `in-review` is agent-owned (principal-engineer + qa
  combined hop next), not the approver, not blocked, not terminal, not held
  by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-048`
  before this pass exits (exit 0) — confirmed queued, not dropped:
  `traces/.pending` shows `1 continue ENG-048` appended behind three
  already-outstanding events (`watch launchd`, `scheduled launchd`,
  `scheduled auto-drain`). This pass still holds `traces/.loop.lock` (pid
  `78771`) at fire time, so the fire queues rather than launches; the drain
  runs the queue in order the moment this pass exits. Post-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-048` and whole-board:
  both exit 0, clean.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- 2026-09-07 `in-review → building` (principal-engineer then qa, `continue
  ENG-048` event pass — combined review/quality hop, round 1). Reading map
  for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9,
  10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check
  clean. Pre-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-048`:
  exit 0.

  **Review: FAIL, round 1.** 0/10 automatic failures. Design conformance
  otherwise clean — the identity walk (`orders.customer_id` = `customers.id`,
  AC12), the rate-as-of-timestamp read (AC8), and the `bill.cart`/`discount`
  dollar-unit claim were each independently re-traced through real
  application code rather than accepted from the migration's or the
  inherited file's own comments; all three hold. Two blocking findings, full
  text and fixes in
  `agents/principal-engineer/notebook/2026-09-07-review-log.md` (ENG-048
  round 1) and `agents/qa/notebook/2026-09-07-coverage-gaps.md` (same date,
  QA's own failure-path/AC lens on the same diff — independently landed on
  the same two root causes):

  - **B1 (function has no `GRANT`/`REVOKE` at all — line 214 area).**
    Confirmed live (system-catalog query only, no row data) that this
    project's `PUBLIC`-execute default is genuinely in effect —
    `calculate_platform_analytics`/`get_acquisition_breakdown`, this repo's
    only two precedent "internal-only" functions, are themselves currently
    callable by `anon`/`authenticated` despite each carrying a `GRANT ... TO
    service_role` (never paired with a `REVOKE ... FROM PUBLIC`, repo-wide).
    `credit_order_if_eligible` is `security definer` and bypasses
    `orders`/`loyalty_ledger_entries`'s own RLS internally — with no grant
    restriction at all, any already-`authenticated` caller of this live
    project can call it directly today, on their own known order ids, live
    from the moment this migration deploys (independent of whether `ENG-049`
    exists yet). Fix: explicit `revoke ... from public` + `grant ... to
    service_role` — the revoke is the operative half; this repo's existing
    grant-only pattern on the other two functions does not actually work,
    confirmed by the same live check.
  - **B2 (`v_amount`, line 197, not floored at zero).** `bill.discount >
    bill.cart` (a plausible promo shape) produces a negative `points`/
    `amount` row through the automated path, contradicting the table's own
    comment (line 58: "this ticket only ever writes positive values") —
    `engineering-standards.md`'s own promoted comment-is-authoritative rule
    is directly on point. Fix: `greatest(cart - discount, 0)`.

  Two non-blocking notes (not gating): a malformed/absent `bill.cart`/
  `discount` retries forever, same accepted shape the design already names
  for any sweep failure; a pre-existing, unrelated `cw_order_id` JSON
  response field in `cloudwaitress.ts:332` (2026-07-07, untouched) is a
  naming coincidence, not a collision.

  No receipt written for either agent (fail discards the round, per
  `code-review-gate/SKILL.md` step 8 and the same rule for QA). `links.review`/
  `links.test_plan` stay unset. **1 transition this pass** (`in-review →
  building`), under the cap of 4. `state: building`, `owner:
  principal-engineer → database` (the implementing agent, unchanged from
  before `in-review`). Machine WIP unaffected — still `1/1`, held by the
  `ENG-027` family.

  **A systemic version of B1, out of scope for this ticket:** the same
  live-check found `calculate_platform_analytics`/`get_acquisition_breakdown`
  (pre-existing, unrelated) share the identical gap. Filed as a proposal, not
  fixed here — `proposals.md`, this date.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing to raise — a fail returns to `building`, not the
  approver. **8b:** the systemic-grant proposal above is the only filing this
  pass; no separate observation (would fragment tracking of the same finding
  across two files). **8c:** n/a — no gate answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-048` and
  whole-board: both exit 0, clean.

  `chained: ENG-048` — `building` is agent-owned (`database`, to apply both
  fixes next), not the approver, not blocked, not terminal, not held by a
  cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-048`
  before this pass exits.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- 2026-09-07 `building → in-review` (database, `continue` event pass, context
  `ENG-048` — round 2, applying round 1's two fixes). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (`.env` → `MODE=active`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-048`: exit 0.

  **B2 fixed as recommended** — `v_amount := greatest(coalesce((v_order.bill
  ->>'cart')::numeric, 0) - coalesce((v_order.bill->>'discount')::numeric,
  0), 0)`, floors the earn base at zero.

  **B1 — review's own literal fix text does not close the hole on this
  project; found by testing the fix, not by applying it on trust.** Applied
  `revoke execute ... from public; grant execute ... to service_role;`
  exactly as round 1 recommended, against a fresh disposable replica of this
  project's own image (`supabase/postgres:15.8.1.073`, matching the image
  every prior verification on this ticket has used) seeded from this
  migration file. `has_function_privilege('anon', ...,
  'EXECUTE')` still returned `true` afterward. Root cause one layer under
  "PUBLIC's default is in effect" (what round 1 named): this project's
  `pg_default_acl` for schema `public` carries an explicit default-privileges
  entry granting `EXECUTE` to `anon`/`authenticated`/`service_role` **by
  name** at function-creation time — confirmed by querying `pg_default_acl`
  directly on the replica, not inferred — a separate ACL mechanism from the
  `PUBLIC` pseudo-grant that a `REVOKE ... FROM PUBLIC` cannot reach.
  Reproduced independently with a throwaway function carrying only `GRANT
  ... TO service_role` (round 1's own two precedent functions' exact shape,
  no revoke at all): `anon` could still execute it on the same replica —
  matching round 1's live finding on `calculate_platform_analytics`/
  `get_acquisition_breakdown` byte for byte, which also confirms this
  replica's default-privileges behavior matches the live project's rather
  than being a local-image idiosyncrasy. Fix applied instead and verified to
  actually close it: `revoke execute on function
  public.credit_order_if_eligible(uuid, text) from public, anon,
  authenticated; grant execute on function
  public.credit_order_if_eligible(uuid, text) to service_role;` — naming
  `anon`/`authenticated` directly. Re-checked all four roles on the
  corrected file: `anon` → `false`, `authenticated` → `false`, `service_role`
  → `true`, `postgres` → `true` (superuser, expected).

  **Full regression matrix re-run on the corrected file, same disposable
  replica, by direct query:** happy path (`cart 100 - discount 10` at 5% →
  `credited`, `amount 90.00`, `points 4.5000`, `rate_applied 5.00`, matching
  round 1's own numbers exactly — no drift from the B1/B2 edits);
  idempotent repeat call → `already_processed`, ledger count still 1;
  `skipped_no_identity`; `skipped_not_enrolled`; cancelled order →
  `already_processed`, `status` untouched at `cancelled`; invalid
  `fulfillment_reason` → raises. **Rollback re-run and confirmed clean** —
  via `psql -f` (matching this repo's own no-single-transaction-per-file
  execution shape, same as every prior verification on this ticket): zero
  `loyalty_ledger_entries` table, zero `orders_loyalty_sweep_idx` index,
  zero matching `cron.job` row, both `orders` columns gone, function gone
  from `pg_proc`. An earlier attempt through `psql -c` (all seven statements
  as one implicit multi-statement transaction) errored on `DROP INDEX
  CONCURRENTLY cannot run inside a transaction block` and rolled back the
  whole batch — an artifact of `-c`'s own batching, not a finding about the
  migration; noted so it isn't mistaken for one on a later read. Container
  removed after use; nothing left running. Full write-up: `agents/database/
  migrations/ENG-048-loyalty-ledger-schema-credit-function-and-cron.md`,
  "Round 2".

  **Proposal correction (8b):** `agents/eng-manager/proposals.md`'s
  2026-09-07 systemic-grant row (principal-engineer, filed off this ticket's
  own round-1 finding) recommended the same insufficient `from public`-only
  fix for `calculate_platform_analytics`/`get_acquisition_breakdown`.
  Corrected in place this round — both the diagnosis (named the
  `pg_default_acl` mechanism) and the Fix column (now names `anon`,
  `authenticated` explicitly) — rather than left to mislead whoever picks it
  up, same convention the restaurant-marketplace row on that file already
  used for its own correction. No separate observation filed (would
  fragment the same finding across two files).

  **New commit on top of `9fccdad`, not an amend** — already pushed to
  `origin/feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`
  (round 1's own build hop), so amending would need a force-push to a
  shared remote to rewrite already-public history. A second, additive
  commit avoids that and matches this project's own precedent of more than
  one commit per ticket branch (`ENG-045`: `b647508`/`a9693b6`/`5f35b92`,
  three commits, one PR). Committed (`60fa06e`, 1 file, 16
  insertions/1 deletion) and pushed:
  `origin/feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`.

  **1 transition this pass** (`building → in-review`), under the cap of 4.
  `state: in-review`, `owner: database → principal-engineer` (next hop:
  review + QA combined, round 2). Machine WIP unaffected — still held by the
  `ENG-027` family.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `in-review` needs no approver gate.
  Nothing to nudge.

  **8c:** n/a — no gate answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-048` and
  whole-board: both exit 0, clean.

  `chained: ENG-048` — `in-review` is agent-owned (principal-engineer + qa
  combined hop next), not the approver, not blocked, not terminal, not held
  by a cap. Firing
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-048`
  before this pass exits.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- 2026-09-07 `in-review → in-qa` (principal-engineer + qa, combined hop,
  `continue ENG-048` event pass, round 2). **Review: pass** — both round-1
  blocking findings (B1 grants, B2 negative amount) independently
  re-verified against a freshly built disposable replica, not accepted on
  the database agent's own writeup. **QA: pass** — both round-1 failing
  rows re-tested the same way; AC4/5/8/9/12 unaffected by this round's
  diff, still hold; 0 open P0/P1. Receipts:
  `agents/principal-engineer/reviews/ENG-048.md`,
  `agents/qa/test-plans/ENG-048.md`; `links.review`/`links.test_plan` set.
  One non-blocking systemic finding (append-only table, no DB-enforced
  revoke) filed as a proposal, not fixed here. No WIP/cap change — still
  inside `ready..ready-to-ship`. Reasoning:
  `agents/principal-engineer/notebook/2026-09-07-review-log.md`,
  `agents/qa/notebook/2026-09-07-coverage-gaps.md`.
  `chained: ENG-048` — `in-qa` is agent-owned (security next), not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-048`
  before this pass exits.

- 2026-09-07 `in-qa → in-security → ready-to-ship` (security, `continue
  ENG-048` event pass, `chained: ENG-048` from this ticket's own prior
  hop). Reading map for `continue`: steps 6 and 6b, plus the not-negotiable
  set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*;
  *Guards*). Mode check clean (`.env` → `MODE=active`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-048`: exit 0.

  **Bookkeeping correction, first.** The prior hop's own review (pass) and
  QA (pass) both cleared in the same combined round-2 hop, which per this
  same board's `ENG-047` precedent (same day: "**2 transitions**
  (`in-review → in-qa`, `in-qa → in-security`)... `in-security` is
  agent-owned (`security` next)") should have landed this ticket at
  `in-security`, not `in-qa` — the prior entry's own closing line ("`in-qa`
  is agent-owned (security next)") already said as much in prose but only
  recorded one transition instead of two, leaving frontmatter one state
  behind its own narrative. Not a re-review: both receipts
  (`agents/principal-engineer/reviews/ENG-048.md`,
  `agents/qa/test-plans/ENG-048.md`) were already on disk and unchanged: the
  ticket was already functionally ready for the security gate. Completing
  the missed transition here rather than treating it as a fresh anomaly.

  **Ran `skills/security-gate/SKILL.md` in full.** Project autonomy: L1
  (`config/projects.md`), so no client-repo (L0) restriction applies.
  Fetched fresh (`origin/main`, `origin/feat/ENG-048-...`); diff unchanged
  from every prior gate's own account — one file, 265 insertions/0
  deletions, two commits (`9fccdad`, `60fa06e`), confirmed via `git diff
  origin/main..HEAD --stat` and per-commit diffstats.

  **Threat model, OWASP A01–A10, LLM checklist (n/a), secrets (clean),
  dependencies (none), negative-case testing, SOC 2 trail — full detail in
  the receipt.** The one finding this ticket owned (B1, access control) was
  independently re-proven a **fourth** time rather than accepted on three
  matching prior accounts: built a fresh disposable replica
  (`supabase/postgres:15.8.1.073`, own from-scratch fixture), independently
  reproduced the `pg_default_acl` mechanism itself *before* applying the
  migration, applied the real migration file unmodified, then went past a
  catalog read — actually called the RPC `set role anon` /
  `set role authenticated` and got a real `permission denied for function
  credit_order_if_eligible` back from both, then confirmed `service_role`
  still gets `credited` with the exact same numbers every prior party
  measured (`amount 90.00, points 4.5000` on the same fixture shape).
  Container removed immediately after; nothing left running (this pass's
  own build-hop log already carries one observation about a prior
  orphaned-container miss — not repeated here).

  **Verdict: PASS.** Zero blocking findings. Two forward-looking notes for
  `ENG-049`'s own gate (webhook signature verification; the wrong-tenant
  negative case, which lives at the handler layer, not this function's).
  Receipt written: `agents/security/reviews/ENG-048.md`,
  `links.security_review` set in the same write.

  **2 transitions this pass** (`in-qa → in-security`, `in-security →
  ready-to-ship`), under the cap of 4 — the first completes the correction
  above, the second is this gate's own routing on a `pass` verdict.
  `state: ready-to-ship`, `owner: qa → devops`. No WIP-cap change — still
  inside the counted `ready..ready-to-ship` range, still held by the
  `ENG-027` family, not a second occupant of the machine slot.

  **Adjacent finding, not part of this ticket's own verdict.**
  Re-deriving the `pg_default_acl` mechanism surfaced that two *pre-existing,
  unrelated* functions on this project (`calculate_platform_analytics`,
  `get_acquisition_breakdown`) carry the identical gap **live, in
  production, with `anon` — fully unauthenticated — confirmed able to
  execute both** (`proposals.md`, 2026-09-07, principal-engineer). That
  proposal explicitly deferred "is this actually exploitable enough to
  matter" to security. Judged this pass: yes — confirmed live, zero auth
  required, real production project, cheap proven fix. This is the step-3
  P0 carve-out (registered, non-internal-lane project, actively
  exploitable), not a finding that should ride the weekly batch. Filed to
  `agents/eng-manager/inbox/2026-09-07-security-p0-rpc-execute-grant-exposure.md`
  (`source: security` per the ticket template's own carve-out exception)
  and fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh finding rpc-execute-grant-exposure`
  — confirmed queued (`traces/.pending`: `1 finding
  rpc-execute-grant-exposure`, behind five already-outstanding events), not
  dropped. Full writeup: `agents/security/notebook/2026-09-07-findings.md`
  (also carries a related but separate three-strike note about the security
  gate's own A01 checklist — not blocking, not this ticket's).

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep (step 7):** the P0 finding above is the only new item this
  pass wrote to `inbox/`, and it was raised immediately (`lib/eng-notify.sh`
  is invoked by the EM's own step-3 handling of a `finding` event, not by
  this gate directly — this gate's job ends at filing and firing). A `pass`
  security verdict is not itself approver-facing, nothing to raise for
  `ENG-048` on its own account. Checked other open `inbox/` items for a
  24h-nudge: none due yet.

  **8b:** the three-strike A01-checklist note (above) is recorded in the
  security notebook, not filed as a standards proposal this pass —
  `engineering-standards.md` is principal-engineer's own code-review
  checklist and this is specifically a security-gate-checklist gap, one
  short of three-strike by gate-reviewed-occurrence count. No
  `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-048` and
  whole-board: both exit 0, clean.

  `chained: ENG-048` — `ready-to-ship` is agent-owned (`devops` next,
  release-readiness hop via `skills/release-runner/SKILL.md`), not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-048`
  before this pass exits — confirmed queued (`traces/.pending` shows `1
  continue ENG-048` appended behind six already-outstanding events,
  including this pass's own `finding` fire above), not dropped. This pass
  still holds `traces/.loop.lock` (pid `78771`, a concurrently-running
  `scheduled auto-drain`) at fire time, so both fires queue rather than
  launch; the drain runs the queue in order the moment the lock frees.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No project-repo commit
  this hop — read-only review, no application code changed; the disposable
  replica container was removed, not committed anywhere.

- 2026-09-07 `ready-to-ship → blocked` (devops, `continue ENG-048` event
  pass — release-readiness hop, `skills/release-runner/SKILL.md`). Reading
  map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
  9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check
  clean (`.env` → `MODE=active`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-048`: exit 0.

  **Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`,
  re-confirmed directly) — no window check applies; steps 2-3's readiness
  content still runs, minus the window bullet, same reading this board has
  used since `ENG-037`/`ENG-039`/`ENG-040`/`ENG-041`/`ENG-044`.

  **Step 2 (upstream gates) — all four re-read fresh from the receipt
  files, not from the ticket log's own account, all passing:**
  `agents/principal-engineer/reviews/ENG-048.md` (pass, round 2),
  `agents/qa/test-plans/ENG-048.md` (pass, round 2),
  `agents/security/reviews/ENG-048.md` (pass, zero blocking findings),
  `agents/database/migrations/ENG-048-loyalty-ledger-schema-credit-function-and-cron.md`
  (pass).

  **Step 3 (readiness gate):**
  - *Rollback:* tested, not reasoned — run twice against a disposable local
    replica (`supabase/postgres:15.8.1.073`), pre- and post-`CONCURRENTLY`
    fix, both confirmed clean.
  - *Observability — read the actual cron body, not the ticket's own
    "no-op-by-construction" framing.* `loyalty-auto-complete-tick` calls
    `net.http_post` **unconditionally** on every 15-minute fire — the
    migration's cron body does not check for eligible rows first (that's
    `ENG-049`'s own claim-query responsibility). Until `ENG-049` deploys the
    `loyalty-auto-complete` edge function, every tick 404s at Supabase's
    edge-routing layer. Not observable today: `net.http_post` is
    fire-and-forget (`pg_net` queues it, response lands in
    `net._http_response`, which nothing reads), and `cron.job_run_details`
    records the tick as succeeded regardless of the HTTP outcome — the same
    mechanism `ENG-037`'s own `broadcast-dispatch-tick` has. Unlike that
    ticket, there is exactly **one** failure window here, not two: the
    `service_role_key` Vault secret this job authenticates with already
    exists live (confirmed this pass), so only the endpoint itself is
    missing, not the secret too. **Judged non-blocking**, same three-part
    reasoning this log's own `ENG-037`/`ENG-038` entries (2026-09-04)
    already established: (a) `aiorders-api` carries no CI/CD auto-deploy —
    confirmed fresh (`find .github` in the worktree: no
    `.github/workflows/`) — so merging this PR does not itself push the
    migration live, that's a separate `supabase db push` outside this
    hop's scope; (b) nothing external reads or writes `loyalty_ledger_entries`
    or either new `orders` column yet, so no user can be affected; (c) the
    gap is bounded and already tracked — it closes the moment `ENG-049`
    ships (this ticket's own `blocks: [ENG-049]`, next in this exact
    sequence). Named precisely in the PR body and the merge-request item so
    whoever pushes this live isn't confused by 404 noise, and so `ENG-049`'s
    own gates inherit the accurate picture.
  - *Cost:* $0/month — same Supabase project; `pg_cron`/`pg_net` and Vault
    already in live use elsewhere on this project; one new table, two
    nullable columns, and four indexes are storage-negligible at low row
    counts; a 404'd `net.http_post` call invokes no billable compute.
  - *Window:* n/a, L1.

  No blocking readiness failure.

  **Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
  re-checked fresh: `git fetch origin main` current; `git diff
  origin/main...HEAD --stat`: 1 file, 265 insertions, 0 deletions — matches
  every prior gate's own account, no drift. Only the same two long-standing
  untracked `deno.lock` files present (`brand-portal`,
  `restaurant-marketplace`), belonging to unrelated pre-existing work, not
  this branch. `gh pr list --head
  feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron --state all`
  — empty, confirmed no PR already existed for this branch.

  Opened `aiorders-api` PR #21
  (https://github.com/harsimranwalia/aiorders-api/pull/21). Body: what it
  does, the round-1→round-2 fix history (B1 access control, B2 negative
  amount), all four gate receipts with paths, the one uncorroborated-live
  claim (`bill.cart`/`discount` unit), what to review hardest (the
  three-way `CHECK` constraints; the `CONCURRENTLY` index add against this
  project's hosted push execution model), the observability finding above
  in full, and cost.

  Wrote `inbox/2026-09-07-eng048-merge-request.md`, plain `pr_url:` string
  (single repo). `time_estimate: half a day` set on the item, mirroring the
  ticket's own field. `lib/eng-notify.sh raise` exit 0, confirmed sent from
  the log (`traces/eng-notify-2026-09-07.log`: `sent: active
  2026-09-07-eng048-merge-request.md`, `16:18:23`); stamped `notified:
  2026-09-07T16:18:23` on the item, copied verbatim from the log. Checked
  the five other open `inbox/` items for a 24h nudge: all five already
  carry a `nudged:` timestamp from a prior pass — exactly one nudge, ever,
  per step 7 — so none nudged again.

  Ticket set `blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, `owner: devops → approver`, `links.pr` set. No G3 — L1 has
  none; the PR merge is the human gate. No release record yet — L1's actual
  deploy (a manual `supabase db push`/migration apply after merge, same
  by-hand pattern every prior `aiorders-api` release on this board has
  shown) and the release record both wait for merge detection on a future
  pass, per the skill's own step 4 L1 row / step 7 split.

  **Slot freed — chained the sibling, not the top of To-do (Guards, amended
  2026-09-07).** `ENG-048` leaving the `ready..ready-to-ship` range frees the
  `ENG-027` family's machine slot. `ENG-049` (`parent: ENG-027`, `depends_on:
  [ENG-048]`, currently `ready`) is the next child of the same parent, and
  its dependency is satisfied **now** — this ticket has an open PR
  (`blocked_on: approver`), which per the corrected 2026-09-07 reading is
  sufficient; `ENG-049` does not wait for `verified`. This is deliberately
  not the ENG-044/045/046 misreading this same guard amendment names: that
  pass logged "ENG-045/046 wait on ENG-044 reaching `verified`" and sat idle
  from 04:02 to the next calendar sweep with three `ready` sub-tickets on
  the board. Confirmed `ENG-049` is actually startable, not just dependency-
  clear: `priority` unset (default order), not `hold`, `blocked_on` empty,
  no unanswered scope/decision question against it. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-049`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-049` appended behind six already-outstanding events
  (`watch launchd` ×2, `scheduled launchd`, `scheduled auto-drain`,
  `continue ENG-050`). `traces/.loop.lock/pid` shows `78771`, a
  concurrently-running `scheduled auto-drain`, so this fire queues rather
  than launches; the drain runs the queue in order the moment the lock
  frees. `ENG-049`'s own frontmatter is untouched by this pass — dispatching
  it (branching off this ticket's own PR branch as a stacked PR, base set to
  it, merge request naming `ENG-048` as the PR that must merge first) is
  that fresh session's work, not this one's.

  `chained: ENG-049 — slot freed by ENG-048`.

  **Machine WIP:** unaffected in the sense that matters — the `ENG-027`
  family still holds the one slot, now via `ENG-049` rather than `ENG-048`;
  no second occupant, no new family dispatched.

  **Dead-end sweep (scoped to this event):** no other ticket touched besides
  the hand-off above.

  **8b:** nothing new to observe or propose this hop — the observability
  and cost reasoning above reuses an already-established pattern
  (`ENG-037`/`ENG-038`) rather than surfacing a new one. No
  `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  answered this pass; the merge request raised above is unanswered, nothing
  to journal yet.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-048` and
  whole-board: both exit 0, clean.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- `2026-09-08` **`blocked → shipped → verified`** (eng-manager, mid-`continue
  ENG-027` event pass — merge detected incidentally while re-checking this
  ticket's own PR state to evaluate the parent container's dispatch options,
  not from a dedicated `continue ENG-048` event). Reading map used: step 6
  (dispatch — this is exactly the "consecutive machine-owned states" case),
  plus `skills/release-runner/SKILL.md` and `skills/acceptance-check/SKILL.md`
  in full, since advancing through them is what this hop actually did.

  **Merge detection.** The checkpoint this pass started from (copied from the
  prior hop's own log) read PR #21 as `OPEN`. Re-verified fresh via `gh pr
  view 21 --json state,mergedAt,baseRefName` from the isolated
  `_eng/aiorders-api` worktree: `MERGED`, `mergedAt: 2026-09-08T18:05:03Z`,
  base `main` — merged directly on GitHub with no written reply to the
  merge-request item. Single-repo ticket, so step 5's ancestry question is
  moot beyond the `gh` state itself.

  **Gates re-verified before advancing, not assumed from the frontmatter's
  populated `links`:** `agents/principal-engineer/reviews/ENG-048.md`
  (`verdict: pass`), `agents/qa/test-plans/ENG-048.md` (`Verdict: pass`),
  `agents/security/reviews/ENG-048.md` (`verdict: pass`) — all read directly
  this pass. No gate owed → advances to `shipped` per step 5 ("a merge is not
  a gate... if the ticket's receipts are not on disk, it goes to the state of
  the first gate it still owes" — they were on disk).

  **Deploy verification (release-runner step 6), not skipped as "L1 doesn't
  release":** `supabase migration list --linked` shows `20260907130000`
  matched on both `local` and `remote` — the migration actually executed
  against the live production database, not just merged to `main`. Full
  detail, including the closed observability gap and the one still-open
  follow-up (first live cron tick not yet observed): release record below.

  **Release record written:**
  `agents/devops/releases/2026-09-08-aiorders-api-ENG-048.md`. No release
  record, no `shipped` state (release-runner step 7) — written before the
  state field below changed.

  **Acceptance-check run in full** (not receipt bookkeeping — this ticket has
  real, checkable behaviour): `agents/product-manager/notebook/2026-09-08-eng048-acceptance.md`.
  All 5 fully-owned criteria (AC4, AC5, AC8, AC9, AC12) verified directly
  against the live-matching migration file, cross-checked against
  independently re-tested QA evidence rather than accepted on the receipt's
  own account — **pass**. The guard/crediting half of the seven shared
  criteria (AC1, AC2, AC3, AC7, AC11, AC15, AC16) is real but not provable by
  this ticket alone; `ENG-049`'s own half completes each (processed the same
  pass — see that ticket's own log and acceptance notebook entry). State →
  `verified`, owner → `eng-manager`, per acceptance-check step 6.

  **Two transitions this hop** (`blocked → shipped → verified`), within the
  4-per-pass cap.

  **8b:** two observations filed — the newly-present GitHub Actions
  auto-deploy workflow on `aiorders-api` (undocumented in
  `config/projects.md`, which still reads "no `.github/workflows/`"), and the
  migration file's own rollback comment ("safe any time before `ENG-049`
  ships") now being stale now that both tickets are live. No
  `exception-request:` found. **8c:** n/a — no G1/G2/G3 answered this hop; the
  PR merge itself is the L1 human gate, already the `released_by` field on
  the release record, not a separate inbox item to journal.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-048` and
  whole-board: both exit 0, clean.

  This settles one of `ENG-027`'s two children. See `ENG-027`'s own log,
  same pass, for the container-level consequence.

  `chained:` n/a — this ticket reached a terminal state (`verified`) this
  hop; nothing to chain for it specifically. See `ENG-027`'s own log for
  this pass's overall chain decision.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.
