---
id: ENG-052
title: Loyalty redemption — widen loyalty_ledger_entries and add redeem_points_if_eligible
project: aiorders-api
type: feature
size: S
time_estimate: half a day
time_spent: ~45m build hop (live-schema/constraint/ACL verification, disposable-replica functional matrix including the rate_applied precision fix, two rollback runs)
time_remaining:
severity: P3
priority:
state: verified
owner: eng-manager
lane: full
blocked_on: 
blocked_from: 
source: approver
created: 2026-09-08
updated: 2026-09-09
branch: feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function
depends_on: []
blocks: [ENG-053]
parent: ENG-051
links:
  prd: agents/product-manager/specs/ENG-051-redemption-api-and-qr-issuance-scanning.md
  design: agents/architect/designs/ENG-051-redemption-api-and-qr-issuance-scanning.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-052.md
  test_plan: agents/qa/test-plans/ENG-052.md
  security_review: agents/security/reviews/ENG-052.md
  release:
  pr: https://github.com/harsimranwalia/aiorders-api/pull/24
---

## Problem

`ENG-051`'s design needs `loyalty_ledger_entries` (`ENG-027`) widened to carry
a redemption (debit) row and a guarded, idempotent function to write one
safely — neither exists yet. `ENG-053` (backend) has nothing to call until
this ships.

## Outcome

`loyalty_ledger_entries`'s `source` check accepts `'redemption'` alongside
`'online_order'`/`'dine_in'`; its three existing per-source checks
(`order_id`, `fulfillment_reason`, `created_by`) each grow a third arm so a
redemption row shapes the same way `dine_in` does on the first two and
requires a non-null `created_by` (a debit needs an audit trail at least as
much as `dine_in`'s own unverifiable-amount case does); a new points-sign
check enforces `points < 0` for `redemption` and keeps the existing sources at
`points >= 0` (not `> 0` — a `0`-point earn is already a real, unconstrained
case via `credit_order_if_eligible`'s own floor and a legally-configurable
`0`% rate, and this ticket doesn't touch that path). A new nullable
`idempotency_key text` column, unique when present, lets a caller-supplied
key dedupe a retried redemption.

`redeem_points_if_eligible(p_platform_customer_id uuid, p_restaurant_id uuid,
p_points numeric, p_idempotency_key text, p_created_by uuid) → text` exists as
one Postgres function, `security definer`, doing (in order): reject
non-positive `p_points` or a missing key outright; take a per-`(diner,
restaurant)` advisory lock (`pg_advisory_xact_lock(hashtextextended(...), 1)`
— seed `1`, not `ENG-007`'s `0`, so the two locks can never collide);
check the idempotency key **before reading balance** (a matching replay
returns `'redeemed'` again with no new insert; a key reused for a different
`(diner, restaurant, points)` raises); resolve the restaurant's currently-
effective redemption rate (`ENG-007`'s read) — none → `'not_enrolled'`;
confirm the diner exists in `platform_customers` — missing →
`'invalid_code'`; sum the diner's balance at that restaurant — insufficient →
`'insufficient_balance'`; otherwise insert one negative-points row and return
`'redeemed'`. `revoke`n from `public`/`anon`/`authenticated` by name and
`grant`ed to `service_role` only.

## Notes

Design: `agents/architect/designs/ENG-051-redemption-api-and-qr-issuance-scanning.md`
— `## Data` (the exact constraint widening) and `## Interfaces` (the DB
function's full 7-step body, function signature, and the grant statements).

**The grant statements are not optional boilerplate — read `ENG-048`'s own
security-gate history before writing them, not just this design's summary
of it.** `ENG-048`'s round-1 review found `credit_order_if_eligible` shipped
with no grant/revoke at all, live-callable by `anon`; the fix that looked
right (`revoke ... from public`) still didn't close it, because this
project's `pg_default_acl` grants `EXECUTE` to `anon`/`authenticated` **by
name** at function-creation time — a separate ACL mechanism a `FROM PUBLIC`
revoke can't reach. The actual fix, confirmed by testing against a
disposable replica, not by reading the recommendation: `revoke execute on
function public.redeem_points_if_eligible(...) from public, anon,
authenticated; grant execute on function
public.redeem_points_if_eligible(...) to service_role;` — naming `anon`/
`authenticated` directly, both statements. Verify with
`has_function_privilege('anon', 'public.redeem_points_if_eligible(...)',
'EXECUTE')` returning `false` before calling this state done, the same way
`ENG-048`'s round-2 build hop did.

**Idempotency-key check must run before the balance read, not after — this
is load-bearing, not stylistic** (design's own Interfaces section, and
Alternatives considered / rejected). A genuine retry arrives after the
original request's own insert has already reduced the balance; checking
balance first would make a legitimate retry fail as `insufficient_balance`
instead of replaying `'redeemed'`.

**Query shapes:** the existing
`loyalty_ledger_entries_customer_restaurant_idx` on `(platform_customer_id,
restaurant_id)` already backs the balance-ceiling sum; the new
`idempotency_key` lookup is a point-lookup the `unique` constraint itself
already indexes — no new index needed beyond the constraint. Confirm both
against the live schema (`\d+ loyalty_ledger_entries`) before writing the
migration, same discipline `ENG-048`'s own build hop used, rather than
assuming the design's own best-reading of the auto-generated constraint
names.

**Rollback:** additive only — drop the new function, drop the
`idempotency_key` column and its constraint, restore the three widened
checks to their prior two-arm form. Test it against a disposable replica
before this ticket reaches `in-review`, same standard `ENG-048` set.

**Branch fresh off `origin/main`, not stacked.** Both prerequisite tickets
this design builds on (`ENG-048`, `ENG-049`) are already merged and verified
— confirmed fresh this pass (`git fetch origin main`; `ENG-048`'s merge
commit `2e5333a` and `ENG-049`'s merge commit `a36c0de` are both ancestors of
`origin/main` at `fb26921`); no open PR exists on `aiorders-api` to stack on.
Full reasoning: `agents/eng-manager/notebook/2026-09-08-eng051-work-breakdown.md`.

**AC ownership** (mapped in full in the work-breakdown notebook above): this
ticket owns AC5, AC6, and AC9 in full, and half of AC3, AC4, AC7, AC8, and
AC11 — the guard/debit half; the handler-caller half belongs to `ENG-053`. No
sub-ticket proves AC3, AC4, AC7, AC8, or AC11 alone — check both together.
Neither sub-ticket owns AC1/AC2 (QR issuance) — already satisfied by
`ENG-006`'s shipped `platform_customers.id`, per this design's own central
finding; nothing in either child issues a code.

## Log

- 2026-09-08 `(created) → building` (eng-manager, `work-breakdown`, `continue
  ENG-051` event pass) — sub-ticket of `ENG-051`, sequence 1, no dependency,
  dispatched straight to `building`, owner `database`. `time_estimate` half
  a day, 0h spent. Machine WIP: part of `ENG-051`'s own family, not a second
  occupant of the `1/1` slot — same reading `ENG-016`/`ENG-019`/`ENG-021`/
  `ENG-026`/`ENG-027` already established. Full reasoning:
  `agents/eng-manager/notebook/2026-09-08-eng051-work-breakdown.md`.
  `chained: ENG-052` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-052`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-052` appended behind one already-outstanding `watch
  launchd` event; no `*-eng-events-dropped.md` for today.

- 2026-09-08 `building → in-review`, `owner: database → principal-engineer`
  (database, `continue` event pass, context `ENG-052`). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*, *The four lanes*, *Guards*) — this ticket is not
  mid-PRD, so step 2's checkpoint note doesn't apply. Mode check clean
  (repo-root `.env` → `MODE=active`, no `ENG_RELEASE_FREEZE`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-052` and whole-board:
  both exit 0, clean.

  Ran `skills/schema-change/SKILL.md` in full.

  **The numbers (step 2), confirmed live before designing anything:**
  `loyalty_ledger_entries` — **0 rows** (`ENG-049` is deployed but nothing
  has yet exercised the webhook accrual, sweep, or dine-in earn in
  production); `restaurant_loyalty_configs` — also 0 rows, so there is no
  real `redemption_value_per_point` value to size the precision question
  against empirically (see below). Every constraint name this migration's
  `DROP CONSTRAINT` targets confirmed against live `pg_constraint` first,
  not assumed from the design's own "best reading" — all four matched the
  design's predicted names exactly. Confirmed no new index is needed beyond
  the `idempotency_key` unique constraint (existing composite index already
  backs the balance read; the unique constraint backs the key lookup).
  `pg_default_acl` for schema `public` (function objects) re-confirmed live:
  same by-name `anon`/`authenticated` grant `ENG-048`'s own round-2 review
  fix already found — applied the two-statement fix from the start rather
  than writing the insufficient `FROM PUBLIC`-only form first.

  **One real gap found and fixed, not present in the architect's design.**
  `rate_applied` was `numeric(5,2)` (sized for the earn side's percentage
  rates); `redemption_value_per_point` (what a redemption's `rate_applied`
  must snapshot) is `numeric(10,4)` on this project — a dollars-per-point
  ratio ENG-007 deliberately gave four decimal places. The design's own
  Interfaces section states `rate_applied = v_rate` without addressing that
  gap. Storing a sub-cent per-point value into `numeric(5,2)` would silently
  round it to `0.00`, defeating the column's own documented audit purpose.
  Widened `rate_applied` to `numeric(10,4)` in this same migration — same
  discipline `ENG-007`'s own pass set for a design-vs-repository mismatch,
  applied here to a design-vs-live-schema-type mismatch. Confirmed a pure,
  lossless widening (existing percentage-shaped values cast up losslessly;
  `credit_order_if_eligible`'s own `v_rate`, untouched, still inserts
  correctly) and confirmed the fix actually closes the regression — see
  Verification below. Full reasoning, both directions tested:
  `agents/database/migrations/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function.md`
  ("Constraint choice").

  **Runtime and locks:** every altered table confirmed at zero live rows
  this pass, so every `ACCESS EXCLUSIVE`-taking statement (five constraint
  changes plus the column-type widening) is sub-millisecond regardless of
  the table's steady-state traffic once `ENG-053` ships — no `CONCURRENTLY`
  strategy applicable the way `ENG-048`'s own live, ~21.9k-row `orders`
  index needed one. `ADD COLUMN idempotency_key` (no default): metadata-only.
  `CREATE OR REPLACE FUNCTION`: a genuinely new function name, not an
  argument-count change to an existing one — this project's own
  `ENG-044`-found `CREATE OR REPLACE` overload trap
  (`agents/database/notebook/2026-09-07-eng044-function-signature-overload-trap.md`)
  does not apply.

  **Expand/contract:** additive only, no backfill — `idempotency_key` starts
  null on zero existing rows; the `rate_applied` widening changes no stored
  value, only the column's representable range.

  **Rollback written, then run — twice, against a disposable replica**
  (`public.ecr.aws/supabase/postgres:15.8.1.073`, same image every prior
  pass on this sequence has used): once as the forward-then-functional-test
  run (below), once as a clean run against a zero-row copy specifically to
  prove the real rollback precondition ("safe any time before `ENG-053`
  ships"). All twelve statements succeed; schema shape restored
  character-for-character to `20260907130000`'s own originals, function
  gone from `pg_proc`, a fresh `redemption`-sourced insert rejected
  afterward. **Corrected the ticket's own rollback description while
  writing it** — the Notes list three items to unwind; this pass's own
  `rate_applied` widening and new sign check are two more, both included and
  tested. Full transcript:
  `agents/database/migrations/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function.md`
  ("Rollback").

  **Self-tested per this state's own exit condition — full functional
  matrix against a disposable replica**, a minimal stand-in for the five
  tables this migration references (column shapes taken from this pass's
  own live reads, `loyalty_ledger_entries` created exactly as `ENG-048`
  left it live) plus `auth.users` (pre-shipped in the image, one row
  inserted). One restaurant deliberately configured at
  `redemption_value_per_point 0.0025` — the exact sub-cent case that would
  silently round to `0.00` under the old column width. Every named function
  branch and every constraint confirmed by direct query, not by reading the
  SQL back: happy path (`redeemed`, `rate_applied 0.0025` not `0.00` —
  the regression this pass's own fix prevents); idempotent replay (same
  key, same triple → `redeemed` again, zero new rows); idempotency
  conflict (same key, different points → raises); insufficient balance (no
  insert); exact-balance boundary (`redeemed`, not insufficient — confirms
  "exceeds" is `<`, not `<=`); not enrolled; invalid code; both guards
  (non-positive points, missing key) raise; all four per-source `CHECK`s
  proven with real failing/succeeding inserts in both directions (including
  that the new sign check still binds `online_order`/`dine_in`, not just
  `redemption`); nullable-safe `idempotency_key` uniqueness (two nulls
  coexist); grant/revoke (`anon`/`authenticated → false`,
  `service_role → true`); `rate_applied` widening backward-compatible for
  an existing-style `online_order` row (`5.00` stores/reads as `5.0000`).
  Full transcript and every query: same migration plan doc, "Verification
  actually performed this pass". All containers removed after use; nothing
  left running (`docker ps -a --filter name=eng052` empty after cleanup).

  **Artifact enumeration (step 6b):**
  `grep -rln "redeem_points_if_eligible\|redeem_points\b"` and
  `grep -rln "idempotency_key\|loyalty_ledger_entries_points_sign_by_source\|rate_applied"`
  across `agents/` (instance) and `departments/engineering/`. The one hit
  that matters as an **instruction** — `ENG-053`'s own board file, the
  ticket that will actually write the calling code — already states the
  exact `supabase.rpc('redeem_points_if_eligible', {p_platform_customer_id:
  code, p_restaurant_id: restaurant_id, p_points: points,
  p_idempotency_key: idempotency_key, p_created_by: user.id})` shape, and
  every parameter name matches this function's real signature exactly — no
  drift, nothing to fix. `departments/engineering/agents/backend/config.yaml`
  matched on `idempotency_key_on_non_idempotent_writes: required` — a
  generic, business-agnostic department standard (read-only template, not
  edited) that this ticket's own design already follows; coincidental
  keyword match, not a conflict. Every other hit is this ticket's own new
  file, the parent's design/board files (already reconciled — this pass
  implemented against them directly), or historical closed-ticket records
  (`ENG-048`'s own migration plan/release/security-review, PM acceptance
  notebooks) that no future producer reads as an instruction.

  **PR body drafted** (`building`'s own exit condition; no PR opened yet —
  L1 opens it at release-readiness):
  - *What it does:* Widens `loyalty_ledger_entries`'s three per-source
    `CHECK`s to add a `redemption` arm; adds
    `loyalty_ledger_entries_points_sign_by_source`; adds nullable-unique
    `idempotency_key`; widens `rate_applied` `numeric(5,2)` →
    `numeric(10,4)` (a design-vs-live-schema gap found and fixed this pass).
    Adds `redeem_points_if_eligible(...)` — guarded, idempotent debit,
    structured like `credit_order_if_eligible`.
  - *What it deliberately does not do:* No caller yet (`ENG-053`, backend,
    wires `brand-portal`'s `redeem_points` action). No frontend, no QR
    issuance (already satisfied by `ENG-006`'s `platform_customers.id`, per
    the design's own central finding). No change to how points are earned.
    No backfill.
  - *Uncertainties:* none material — every claim tested against a
    disposable replica, including the boundary case. True multi-transaction
    concurrency (two simultaneous callers for the same diner+restaurant)
    was reasoned through, not literally executed concurrently — same
    verification depth `ENG-007`'s own advisory-lock pattern accepted as
    gate-passing for the identical mechanism.
  - *What to review hardest:* (1) the `rate_applied` widening — is
    widening the right minimal fix, or does it point at a deeper question
    about `redemption_value_per_point`'s own precision policy that should
    be raised rather than silently absorbed; (2) the four-way per-source
    `CHECK` matrix is exhaustive across all three `source` values now, not
    just the original two; (3) the idempotency-check-before-balance-read
    ordering, since retry correctness depends specifically on that order.

  Branch committed (`0a2f730`, 1 file) and pushed:
  `origin/feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function`.

  **1 transition this pass** (`building → in-review`), under the cap of 4 —
  `in-review` (principal-engineer, code review) is a fresh session's work
  per `eng_build_loop.md`'s "a pass stops after `building` on purpose."
  Machine WIP: still `1/1`, held by the `ENG-051` family (parent `ENG-051`
  still `building`, sibling `ENG-053` still `ready` on its unmet
  `depends_on: [ENG-052]`) — unaffected, since `in-review` is still inside
  the counted `ready..ready-to-ship` range.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract.

  **Notify sweep:** nothing raised this pass — `in-review` needs no
  approver gate. Nothing of this ticket's own to nudge (no open gate item
  on `ENG-052`); did not sweep the rest of `inbox/` for staleness, same
  scoping every prior `continue`-event hop on this board has used —
  that's the `scheduled`/`watch` sweep's job.

  **One observation filed** (`observations.md`, this date, `database`/
  `aiorders-api`): the `rate_applied` precision gap — an architect design's
  Interfaces section named an insert shape without checking the target
  column's own live type against the source value's type. One instance,
  caught and fixed in the same pass it was introduced; not filed as a
  proposal (no second instance found, nothing left undone). No
  `exception-request:`; no G1/G2/G3/merge-request answered this pass, so
  no decision-journal entry owed.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-052` and
  whole-board: both exit 0, clean.

  `chained: ENG-052` — `in-review` is agent-owned (principal-engineer, code
  review next), not the approver, not blocked, not terminal, not held by a
  cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-052`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-052` appended behind one already-outstanding `watch
  launchd` event; no `*-eng-events-dropped.md` for today. This pass still
  holds `traces/.loop.lock` at fire time, so the fire queues rather than
  launches; the drain runs the queue in order the moment this pass exits.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- 2026-09-08 `in-review → in-qa → in-security` (principal-engineer + qa,
  combined hop, `continue ENG-052` event pass, round 1). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*) — this ticket is not
  mid-PRD. Mode check clean (repo-root `.env` → `MODE=active`, no
  `ENG_RELEASE_FREEZE`). `sh departments/engineering/lib/eng-gate-check.sh
  ENG-052` and whole-board: both exit 0, clean.

  Ran `skills/code-review-gate/SKILL.md` and QA's own quality gate
  concurrently on the same diff (`0a2f730` vs `origin/main` `fb26921`, one
  file, 267 lines).

  **Review: pass, round 1.** 0/10 automatic failures. Design conformance
  confirmed line-by-line against `agents/architect/designs/ENG-051-....md`'s
  Interfaces section — exact match on signature, 7-step body order, and the
  grant/revoke shape. Two non-blocking notes (neither a standard — first
  occurrence of each): the insert omits `order_id`/`fulfillment_reason`
  rather than an explicit `null` (equivalent, no established precedent
  either way on this table); `amount` carries the redemption's positive
  dollar magnitude while `points` carries the signed delta, matching the
  design exactly but worth naming for a future reader. Receipt:
  `agents/principal-engineer/reviews/ENG-052.md`, `links.review` set.

  **QA: pass, round 1.** No suite exists for `aiorders-api` (no
  `package.json`, no `deno.json` — same position every prior migration-only
  ticket on this project has been in); recorded `no suite` per
  `test-suite-run/SKILL.md` step 8. This ticket's fully- and half-owned
  acceptance criteria (AC5, AC6, AC9 full; AC3, AC4, AC7, AC8, AC11 the
  guard/debit half) all confirmed covered. 0 open P0/P1. Receipt:
  `agents/qa/test-plans/ENG-052.md`, `links.test_plan` set.

  **Both gates independently re-ran the disposable-replica verification
  themselves rather than accepting the database agent's own build-hop
  write-up** — own fixture (not the one on file), own container
  (`public.ecr.aws/supabase/postgres:15.8.1.073`, same image every prior
  verification on this sequence has used), the real migration file applied
  unmodified. Same standard `ENG-048`'s own gates set for this project,
  given its specific history of a "looks right" grant/revoke fix that
  wasn't (B1). Reproduced, independently, every material claim in
  `agents/database/migrations/ENG-052-....md`: access control (a catalog
  read *and* an actual denied RPC call as both `anon` and `authenticated`
  via `set role`, not a catalog read alone); the sub-cent precision case
  (`redemption_value_per_point 0.0025` stored and read back as `0.0025`,
  not `0.00` — the exact regression this pass's own `rate_applied` widening
  prevents); idempotent replay (zero new rows); idempotency conflict (a
  real raise); insufficient balance; the exact-balance boundary (`<`, not
  `<=`); not-enrolled; invalid-code; both input guards; all four
  cross-field `CHECK`s proven in the failing direction; two null-
  `idempotency_key` redemption rows coexisting; and `rate_applied`
  backward-compatibility for the earn side. Every number matched the
  migration plan doc's own account exactly. Container removed immediately
  after; confirmed nothing left running.

  **2 transitions this pass** (`in-review → in-qa`, `in-qa → in-security`),
  under the cap of 4 — both gates cleared in this same combined hop, so the
  ticket lands directly at `in-security` rather than parking at `in-qa`
  (the `ENG-047` precedent this board already established for a clean
  combined-hop pass, not the bookkeeping gap `ENG-048`'s own round-2 entry
  had to correct). `state: in-security`, `owner: principal-engineer →
  security`. No WIP/cap change — still inside the counted
  `ready..ready-to-ship` range, still held by the `ENG-051` family, not a
  second occupant of the machine slot.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract.

  **Notify sweep (step 7):** nothing raised this pass — `in-security` needs
  no approver gate. Nothing of this ticket's own to nudge. Did not sweep
  the rest of `inbox/` for staleness — that's the `scheduled`/`watch`
  sweep's job, not a `continue` event's.

  **8b:** no observation beyond what's already recorded in the two receipts
  above; no `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-
  request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-052` and
  whole-board: both exit 0, clean.

  `chained: ENG-052` — `in-security` is agent-owned (security next), not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-052`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-052` appended behind one already-outstanding `watch
  launchd` event; no `*-eng-events-dropped.md` for today. This pass still
  holds `traces/.loop.lock` at fire time (this hop's own live PID), so the
  fire queues rather than launches; the drain runs the queue in order the
  moment this pass exits.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No project-repo commit
  this hop — read-only review, no application code changed; the disposable
  replica containers were removed, not committed anywhere.

- 2026-09-08 `in-security → ready-to-ship`, `owner: security → devops`
  (security, `continue ENG-052` event pass). Reading map for `continue`:
  steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*; *The four lanes*; *Guards*) — this ticket is not mid-PRD, so
  step 2's checkpoint note doesn't apply. Mode check clean (repo-root `.env`
  → `MODE=active`, no `ENG_RELEASE_FREEZE`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-052` and whole-board:
  both exit 0, clean.

  Ran `skills/security-gate/SKILL.md` in full. Project `aiorders-api` is L1,
  not L0 — scanning and probing permitted.

  **Threat model (step 2):** `EXECUTE` is `service_role`-only post-migration
  (verified below), so the only attacker-controlled input is one layer up,
  at `ENG-053`'s not-yet-built handler — out of this ticket's own scope,
  flagged forward. `service_role` gains one guarded debit capability; no new
  data exposure (`loyalty_ledger_entries` pre-exists, RLS unaffected); a
  compromised `service_role` is bounded by the function's own guards, same
  position `ENG-048`'s review took for the analogous credit function.

  **Independently re-verified from scratch, not accepted on the database
  agent's, code review's, or QA's own write-up** — own fixture (not the one
  on file), own disposable container
  (`public.ecr.aws/supabase/postgres:15.8.1.073`, same image every prior
  verification on this sequence used), all three real migration files
  applied unmodified in order (`20260829130000`, `20260907130000`,
  `20260908160000`). Confirmed the `pg_default_acl` by-name-grant mechanism
  itself before applying anything, not read off any prior account.
  **`has_function_privilege`:** `anon → false`, `authenticated → false`,
  `service_role → true`. **Went past the catalog read — attempted the
  actual RPC as both `anon` and `authenticated`:** both fail with a real
  `permission denied for function redeem_points_if_eligible`, not an
  inferred rejection; `service_role` executes normally. `search_path`
  pinning confirmed at the catalog level (`pg_proc.proconfig`), not just in
  the source text. RLS on `loyalty_ledger_entries` confirmed unaffected
  (`relrowsecurity = t`, zero policies). Reproduced the idempotency-before-
  balance-read ordering (replay → `redeemed` again, zero new rows; a key
  reused for a different amount raises), both input guards, the sub-cent
  precision fix (`0.0025` stored, not `0.00`), the exact-balance boundary,
  `not_enrolled`/`invalid_code`, all four per-source `CHECK`s in both
  directions (including the sign check binding `online_order` too, and the
  `created_by` audit-trail arm), nullable-safe `idempotency_key` uniqueness,
  and `rate_applied` backward compatibility (`5.00` reads back `5.0000`).
  Secrets: diff and full branch history (one commit, 267 insertions / 0
  deletions) grepped for credential patterns — zero matches, not even a
  constraint-name false positive. Container removed immediately after;
  confirmed nothing left running.

  **OWASP walk: A01–A10 all `reviewed`/`n/a` with a reason** — A01 the
  primary surface (access control, independently re-verified above, per
  the explicit checklist item this notebook flagged 2026-09-07 rather than
  just a catalog-read proof); A03 clean (no dynamic SQL, read in full); A04
  business-logic abuse considered and independently tested (double-
  redemption, negative/zero-amount, balance boundary); A05 the project's
  known `pg_default_acl` gotcha (`ENG-050`'s own P0) correctly closed from
  the start, not re-introduced — third gate-reviewed function to get this
  right, not a third miss; A09 every guard path visible, `created_by`
  audit trail enforced. A02/A06/A07/A08/A10 n/a, no surface in this diff.
  LLM checklist n/a — no model/agent/tool/MCP/RAG surface. No new or
  bumped dependency.

  **Findings: none blocking.** Three forward notes recorded in the receipt
  for `ENG-053`'s own gate (same mechanism `ENG-048`'s gate used for
  `ENG-049`): (1) the wrong-tenant case — `requireRestaurantAccess` at the
  handler, not this function, which trusts `p_restaurant_id` by design; (2)
  the redemption code's own bearer-credential shape, unchanged by design
  and carried from the PRD (`ADR-022`) — the handler shouldn't widen that
  exposure; (3) `loyalty_ledger_entries` still has no DB-level
  `UPDATE`/`DELETE` protection — pre-existing, already an open proposal
  (principal-engineer, 2026-09-07), not from this diff, not this ticket's
  scope.

  Receipt written: `agents/security/reviews/ENG-052.md`. `links.security_review`
  set in the same write. No new `agents/security/notebook/` entry — no
  blocking finding and no new pattern; the one pattern worth noting (A05
  correctly applied a third time, closing the loop the 2026-09-07 notebook
  entry left open) is a confirmation, not a fresh finding class, so it's
  recorded in the receipt itself rather than a new dated notebook file.

  **1 transition this pass** (`in-security → ready-to-ship`), under the cap
  of 4. `state: ready-to-ship`, `owner: security → devops`. Machine WIP:
  still `1/1`, held by the `ENG-051` family (parent `ENG-051` still
  `building`, sibling `ENG-053` still `ready` on its unmet
  `depends_on: [ENG-052]`) — `ready-to-ship` is still inside the counted
  `ready..ready-to-ship` range, so the family's slot is unaffected; per
  Guards, a slot only frees when every child is parked on the approver or
  verified, and `ENG-053` hasn't even started yet.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract.

  **Notify sweep (step 7):** nothing raised this pass — `ready-to-ship` is
  the release-readiness hop's own trigger, not an approver gate itself.
  Nothing of this ticket's own to nudge.

  **8b:** one observation filed (`observations.md`, this date,
  `security`/`aiorders-api`) — the A01 checklist gap the 2026-09-07 notebook
  entry flagged (verify a new/changed RPC function's own
  `has_function_privilege` independently of any application-layer wrapper)
  was applied here without needing to be re-derived, closing that loop in
  practice; worth folding into `security-baseline.md`'s own A01 row if the
  pattern holds on the next function-level ticket, not done this pass since
  editing the department-wide baseline is outside a `continue` event's own
  scope. No `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-
  request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-052` and
  whole-board: both exit 0, clean.

  `chained: ENG-052` — `ready-to-ship` is agent-owned (devops,
  release-readiness next), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-052`
  before this pass exits.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No project-repo commit
  this hop — read-only security review, no application code changed; the
  disposable replica containers were removed, not committed anywhere.

- 2026-09-08 `ready-to-ship → blocked` (devops, `continue ENG-052` event
  pass — release-readiness hop, `skills/release-runner/SKILL.md`). Reading
  map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
  9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*) — this ticket
  is not mid-PRD. Mode check clean (repo-root `.env` → `MODE=active`, no
  `ENG_RELEASE_FREEZE`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-052` and whole-board:
  both exit 0, clean.

  **Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`,
  re-confirmed directly) — no window check applies; steps 2-3's readiness
  content still runs, minus the window bullet.

  **Step 2 (upstream gates) — all four re-read fresh from the receipt files,
  not from the ticket log's own account, all passing:**
  `agents/principal-engineer/reviews/ENG-052.md` (pass, round 1),
  `agents/qa/test-plans/ENG-052.md` (pass, round 1),
  `agents/security/reviews/ENG-052.md` (pass, zero blocking findings),
  `agents/database/migrations/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function.md`
  (pass).

  **Step 3 (readiness gate):**
  - *Rollback:* tested, not reasoned — run twice against a disposable local
    replica (`supabase/postgres:15.8.1.073`), forward-then-functional and a
    clean run against a zero-row copy, both confirmed clean.
  - *Observability:* no gap. Unlike `ENG-048`'s own cron (unconditional
    `net.http_post` against a not-yet-existing endpoint), this migration adds
    no trigger, cron, or caller of any kind — `redeem_points_if_eligible` is
    unreachable by anything until `ENG-053` wires a caller in. Inert, not
    silently failing.
  - *Cost:* $0/month — same Supabase project; one nullable column and four
    widened/added `CHECK` constraints are storage-negligible at low row
    counts; no new compute.
  - *Window:* n/a, L1.

  No blocking readiness failure.

  **Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
  re-checked fresh: `git fetch origin main`; `git diff origin/main...HEAD
  --stat`: 1 file, 267 insertions, 0 deletions — matches every prior gate's
  own account, no drift. Only the same class of long-standing untracked
  `deno.lock` files present, unrelated to this branch. `gh pr list --head
  feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function --state
  all` — empty, confirmed no PR already existed for this branch.

  Opened `aiorders-api` PR #24
  (https://github.com/harsimranwalia/aiorders-api/pull/24). Body: what it
  does, all four gate receipts with paths, what to review hardest (the
  `rate_applied` widening; the four-way per-source `CHECK` matrix; the
  idempotency-before-balance-read ordering), rollback, cost, and the three
  forward notes for `ENG-053`'s own security gate.

  Wrote `inbox/2026-09-08-eng052-merge-request.md`, plain `pr_url:` string
  (single repo). `lib/eng-notify.sh raise` exit 0, confirmed sent from the
  log (`traces/eng-notify-2026-09-08.log`: `sent: active
  2026-09-08-eng052-merge-request.md`, `14:41:39`); stamped `notified:
  2026-09-08T14:41:39` on the item, copied verbatim from the log.

  Ticket set `blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, `owner: devops → approver`, `links.pr` set. No G3 — L1 has
  none; the PR merge is the human gate. No release record yet — L1's actual
  deploy and the release record both wait for merge detection on a future
  pass, per the skill's own step 4 L1 row / step 7 split.

  **Slot freed — chained the sibling, not the top of To-do or the `designed`
  pool (Guards, amended 2026-09-07).** `ENG-052` leaving the
  `ready..ready-to-ship` range frees the `ENG-051` family's machine slot.
  `ENG-053` (`parent: ENG-051`, `depends_on: [ENG-052]`, currently `ready`)
  is the next child of the same parent, and its dependency is satisfied
  **now** — this ticket has an open PR (`blocked_on: approver`), which per
  the 2026-09-07 reading is sufficient; `ENG-053` does not wait for
  `verified`. Confirmed `ENG-053` is actually startable, not just
  dependency-clear: `priority` unset (default order), not `hold`,
  `blocked_on` empty, `grep -rl "ENG-053" inbox/*.md` finds only this
  ticket's own new merge-request item (no unanswered scope/decision question
  against `ENG-053` itself). Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-053`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-053` appended behind two already-outstanding `watch
  launchd` events; no `*-eng-events-dropped.md` for today. `ENG-053`'s own
  frontmatter is untouched by this pass — dispatching it (branching off this
  ticket's own PR branch as a stacked PR, base set to it, merge request
  naming `ENG-052` as the PR that must merge first) is that fresh session's
  work, not this one's.

  `chained: ENG-053 — slot freed by ENG-052`.

  **Machine WIP:** unaffected in the sense that matters — the `ENG-051`
  family still holds the one slot, now via `ENG-053` rather than `ENG-052`;
  no second occupant, no new family dispatched.

  **A live, unrelated integrity question was found and deliberately not
  acted on.** Step 7's mandatory 24h-nudge check touched
  `inbox/IDLE-2026-09-07.md` and `inbox/2026-09-08-eng-loop-integrity-check.md`
  — both open P0-adjacent items about an unverified, uncommitted 2026-09-08
  self-edit to `eng_build_loop.md`/both `config.yaml`s/`proposals.md`
  claiming the approver authorized drawing new machine starts from the
  `designed` pool. **This pass's own `chained: ENG-053` decision does not
  rely on that disputed text at all** — it rests entirely on the earlier,
  uncontested 2026-09-07 amendment (an open PR satisfies `depends_on`; the
  dependent sibling starts in the same pass), the same rule the
  `ENG-048`→`ENG-049` handoff already used without dispute. Neither item was
  due for a nudge under a correctly-computed local-time 24h window (see 8b
  observation below on the timezone check itself): `IDLE-2026-09-07`
  notified `2026-09-07T18:44:54` local, ~19h55m elapsed against this pass's
  own local clock (`2026-09-08T14:40:04` PDT); `eng-loop-integrity-check`
  notified `2026-09-08T09:58:53` local, ~4h41m elapsed. Neither touched
  beyond this read; resolving the disputed text is the approver's call, not
  this pass's, and several prior passes have already correctly declined to
  act on it.

  **Dead-end sweep (scoped to this event):** no other ticket touched besides
  the hand-off above.

  **Notify sweep (step 7):** this pass's own new gate item raised
  immediately (above). Checked all other open `inbox/*.md` items for a 24h
  nudge using local time (matching how `eng-notify.sh` itself stamps
  `notified:`, via unqualified local `date`): all already-nudged items
  correctly skipped (exactly one nudge, ever); the two un-nudged items
  (`IDLE-2026-09-07`, `eng-loop-integrity-check`) are both still under 24h
  by local-clock math — see above. None nudged this pass.

  **8b:** no new observation filed — checked `observations.md` before
  writing one and found this exact pattern (`eng-notify.sh` stamps
  `notified:`/`nudged:` via unqualified local `date`, but at least one prior
  pass diffed that local string against a UTC "now" and nudged early,
  `ENG-050`'s own `notified: 2026-09-07T16:04:16` → `nudged:
  2026-09-08T09:52:23` being this pass's own instance of it) already
  tracked: `observations.md` carries the identical `ENG-050` timestamp
  discrepancy (2026-09-08 row, "30th consecutive... idle-check"), and
  `proposals.md` already holds an escalated, three-strike-plus proposal on
  this exact defect (2026-09-02 discovery, 2026-09-07 "third occurrence...
  crosses this repo's own three-strike line," with a concrete `S`-sized fix
  named — stamp `notified:`/`nudged:` with an explicit UTC offset, or
  document the local-time convention in step 7 itself). Filing a fresh
  observation for a fourth-plus confirmation of an already-escalated
  proposal would be noise, not signal; this pass's own contribution is
  simply that it used correct local-to-local math itself (above), so no
  fresh mistake to add to the count. No `exception-request:` found. **8c:**
  n/a — no G1/G2/G3/merge-request answered this pass; the merge request
  raised above is unanswered, nothing to journal yet.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-052` and
  whole-board: both exit 0, clean.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No project-repo commit
  this hop — release-readiness opens a PR against already-pushed commits,
  nothing new to commit in the `aiorders-api` worktree either.

- `2026-09-09` `blocked → shipped` (control center, merge detected) — `feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function` is an ancestor of `origin/main`. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree.

- `2026-09-09T07:33 PDT` `shipped → verified` (product-manager, acceptance-check,
  `continue ENG-051` event). AC5/6/9 (fully owned) + guard/debit half of
  AC3/4/7/8/11 (checked with `ENG-053`, per Notes) — all pass, verified live:
  migration `20260908160000` read in full, matches design; live
  `has_function_privilege` on production — anon/authenticated/service_role =
  false/false/true, closing the `ENG-048`-class grant gap. Non-goals clear,
  cost matches estimate. Full walk:
  `agents/product-manager/notebook/2026-09-09-eng052-eng053-acceptance.md`.
  `owner: approver → eng-manager`. Git ops this pass (read-only bar one
  harmless ff-only pull) logged once on `ENG-051`'s own entry.
  Post-pass gate-check: see `ENG-051`'s entry.
  `chained: n/a` — terminal (`verified`) this hop; nothing to chain for it
  specifically. See `ENG-051`'s own log for this pass's chain decision.
  business-os left uncommitted — standing default, not re-decided here.
