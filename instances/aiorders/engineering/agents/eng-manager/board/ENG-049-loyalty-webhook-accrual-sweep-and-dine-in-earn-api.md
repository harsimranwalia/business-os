---
id: ENG-049
title: Loyalty accrual — webhook handler, auto-complete sweep, and dine-in earn API
project: aiorders-api
type: feature
size: M
time_estimate: a day to a couple of days
time_spent:
time_remaining:
severity: P3
priority:
state: blocked
owner: approver
lane: full
blocked_on: approver
blocked_from: ready-to-ship
source: approver
created: 2026-09-07
updated: 2026-09-07
branch: feat/ENG-049-loyalty-webhook-accrual-sweep-and-dine-in-earn-api
depends_on: [ENG-048]
blocks: []
parent: ENG-027
links:
  prd: agents/product-manager/specs/ENG-027-loyalty-points-ledger-and-earn.md
  design: agents/architect/designs/ENG-027-loyalty-points-ledger-and-earn.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-049.md
  test_plan: agents/qa/test-plans/ENG-049.md
  security_review: agents/security/reviews/ENG-049.md
  release:
  pr: https://github.com/harsimranwalia/aiorders-api/pull/22
---

## Problem

`ENG-027`'s design un-ignores three CloudWaitress webhook events, adds a
cron-invoked sweep for orders nobody reports on, and adds a staff-facing
dine-in earn API — none of which exist yet, and none of which can be built
against real tables/functions until `ENG-048` (database) ships.

## Outcome

`external-integrations/handlers/cloudwaitress.ts`'s `createOrder()` persists
CloudWaitress's own order id (`data.order._id`, already read, never
currently stored) into `orders.cw_order_id`. `handleCloudWaitress()` stops
discarding `order_completed_updated`, `order_cancelled_updated`, and
`order_cancel`: it looks the order up by `cw_order_id`, and on a fulfilment
report calls `credit_order_if_eligible(order.id, 'reported')`; on either
cancellation event it unconditionally sets `status = 'cancelled'`. Both
branches return `200 {success:true}` regardless of credit outcome, same as
today's shape for an unrecognized order. A new edge function,
`loyalty-auto-complete`, authenticates as `ADR-016`–`018`'s internal/system
calls already do, selects the eligible batch, calls
`credit_order_if_eligible(id, 'window_elapsed')` per row inside a
catch-and-continue loop, and returns `{claimed, credited, skipped, errors}`.
Two new `brand-portal` actions exist — `record_dine_in_earn` and
`get_loyalty_balance` — both gated by `requireRestaurantAccess`, wired into
`brand-portal/index.ts`.

## Notes

Design: `agents/architect/designs/ENG-027-loyalty-points-ledger-and-earn.md`
— `## Interfaces` (all three: webhook, edge function, `brand-portal`
actions). The sweep's mechanism (`pg_cron` + `net.http_post`, structurally
identical to `ADR-018`'s `broadcast-dispatch-tick`) is `ADR-021`, decided and
logged, not escalated — this ticket's own edge function is an ordinary
authenticated HTTP handler regardless of what invokes it, so it does not
carry that ADR in its own `links` (`ENG-048` does); named here only so the
engineer has the context.

**Webhook response contract, exact (AC13, containment):** a credit or status
update that fails for any reason must never change the webhook's own
`200 {success:true}` response — order recording (a separate, untouched code
path) can never be blocked by a loyalty-side failure. Log the failure; don't
propagate it into the response.

**Not-found order (AC14):** a terminal-event report for an order the
platform has no record of (`cw_order_id` lookup misses) gets the same
`{success:true, message:'...ignored'}` shape the handler already returns for
an unrecognized event today — accepted and ignored, not an error.

**Cancellation never touches the ledger (AC16, this ticket's own half):**
the cancellation branch updates `orders.status` only. It must not delete,
rewrite, or otherwise touch any `loyalty_ledger_entries` row — if points were
already credited before the cancellation arrives, the entry stands; a human
correction is ticket 5's own surface.

**Dine-in never creates a platform identity, only credits an existing one**
(per the design's own Approach): `record_dine_in_earn` resolves
`platform_customers` by normalized phone; no row → a distinct
`no_platform_identity` result, no entry, nothing fabricated.

**Two live, distinct non-success results `get_loyalty_balance`'s sibling
handler must return, not silent successes:** `not_enrolled` (no configured
dine-in rate — AC11's dine-in half) and the 403-shaped access-check failure
(AC17). Input validation on `amount` (AC18) — not a positive finite number →
`400` with a clear reason, no entry.

**`brand-portal/loyalty.ts` and `index.ts` wiring** follow the same pattern
every existing `brand-portal` action already uses (`requireRestaurantAccess`
first, then the action body) — see `feedback.ts` for the closest existing
example the design itself cites.

**Branch from `origin/main`, not `loyalty-system`.** Same correction as
`ENG-048`'s own Notes — the parent ticket's 2026-09-03 shared-branch
instruction predates `ENG-006`/`ENG-007` merging it away; `origin/main` is
59 commits ahead of that branch now. Full reasoning: `ENG-027`'s own
board-file log and
`agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`. Also
branch from `origin/main` directly rather than stacking on `ENG-048`'s own
branch: `ENG-048` is dispatched to `building` this same pass and is expected
to merge (open its PR) well before this ticket's own `depends_on` clears, so
there's ordinarily no need to stack — if `ENG-048`'s PR is still open when
this ticket's dependency check runs, that pass branches from `ENG-048`'s own
branch instead (a stacked PR, per `eng_build_loop.md` Guards) and says so in
this ticket's own Log; not assumed here since it hasn't happened yet.

**AC ownership** (mapped in full in
`agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`): this
ticket owns AC6, AC10, AC13, AC14, AC17, and AC18 in full, and half of AC1,
AC2, AC3, AC7, AC11, AC15, and AC16 — the webhook/sweep-caller and
dine-in-population half; the guard/crediting half belongs to `ENG-048`. No
sub-ticket proves AC1, AC2, AC3, AC7, AC11, AC15, or AC16 alone — check both
together.

## Log

- 2026-09-07 `(created) → ready` (eng-manager, `work-breakdown`, `continue
  ENG-027` event pass) — sub-ticket of `ENG-027`, sequence 2,
  `depends_on: [ENG-048]` unmet — stays `ready`, owner `eng-manager`, until
  `ENG-048` ships. `time_estimate` a day to a couple of days, 0h spent.
  Machine WIP: part of `ENG-027`'s own family, not a second occupant of the
  `1/1` slot. Full reasoning:
  `agents/eng-manager/notebook/2026-09-07-eng027-work-breakdown.md`.
  `chained: none` — dependency unmet; resumes once `ENG-048` reaches a state
  that satisfies it (an open PR is enough, per `eng_build_loop.md` Guards'
  2026-09-07 amendment — not full `verified`).

- 2026-09-07 `ready → building → in-review` (backend, `continue ENG-049`
  event pass — slot freed by `ENG-048` parking on the approver with PR #21
  open). Reading map for `continue`: steps 6 and 6b, plus the not-negotiable
  set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*;
  *Guards*). Mode check clean (`.env` → `MODE=active`).

  **Dependency re-verified live, not assumed from the ticket's own text:**
  `git fetch origin`, `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`
  local HEAD matched `origin/...` exactly (`60fa06e`), `gh pr view 21
  --json state,baseRefName,headRefName,mergedAt` — `OPEN`, base `main`.
  Branches from `ENG-048`'s own branch as a stacked PR, per this ticket's
  own Notes and Guards' 2026-09-07 amendment, not from `origin/main`.

  **Built:** `cloudwaitress.ts` — `createOrder()` persists `cw_order_id`;
  new exported `handleTerminalOrderEvent` un-ignores `order_completed_updated`
  (calls `credit_order_if_eligible(order.id, 'reported')`),
  `order_cancelled_updated`/`order_cancel` (unconditional `status='cancelled'`,
  never touches the ledger — AC16). Every branch, including an RPC or
  update error, still returns `200 {success:true}` (AC13 containment).
  New edge function `loyalty-auto-complete` (service-role gated, local copy
  of `broadcast-dispatch/auth.ts`'s own pattern) selects the eligible batch
  (`BATCH_SIZE 200`, no measured number yet, same order of magnitude as
  `ADR-018`'s own starting point) and calls `credit_order_if_eligible(id,
  'window_elapsed')` per row in a catch-and-continue loop (AC15). New
  `brand-portal/loyalty.ts` — `record_dine_in_earn` (`requireRestaurantAccess`
  first per AC17, `amount` validated per AC18, `not_enrolled`/
  `no_platform_identity` both live distinct results per AC11, inserts the
  ledger row directly per the migration's own comment that dine-in never
  calls `credit_order_if_eligible`) and `get_loyalty_balance` (AC10), wired
  into `index.ts` (+2 case lines). Split `external-integrations/index.ts`'s
  response helpers into a new `responses.ts` so a handler can be
  unit-tested without importing `index.ts`'s own top-level `Deno.serve(...)`
  as a side effect — confirmed the other four handlers unaffected by
  diffing `deno check index.ts`'s error count before/after (24, both times,
  all pre-existing, none in a file this ticket touches).

  **One correctness bug caught and fixed before it shipped:** `readBalance`'s
  first draft summed from the same capped, ordered `entries` list it
  returns for display — correct today (zero rows) but silently wrong the
  moment a diner/restaurant pair ever exceeded the 500-row display cap,
  since AC10 requires the exact sum of *every* entry. Split into two
  queries (an unbounded narrow sum query, a bounded wide display query).
  Regression test seeds 505 rows and asserts the sum is 505 while the
  display list stays ≤500. Full writeup:
  `agents/backend/notebook/2026-09-07-eng049-build.md`.

  **Acted on both of `ENG-048`'s own security-gate forward-notes** (read
  the actual receipt, `agents/security/reviews/ENG-048.md`, not just the
  board-log summary): (1) webhook signature verification — confirmed
  pre-existing on every event this handler processes (the `secret` field
  has never been checked, including for `order_new`), and explicitly out of
  this ticket's scope per the design's own "no auth-model change" — named
  plainly here and in the PR body rather than silently deferred. (2)
  wrong-tenant/ownership case — addressable in-scope without a new auth
  mechanism: confirmed `handleTerminalOrderEvent` never reads
  `webhookData.restaurant_id` for anything security-relevant (the lookup is
  keyed solely by `cw_order_id`, everything downstream comes from the
  matched row), and added a direct test proving it (second commit, below).

  **Self-tested, three new `.test.ts` files, each run from its own function
  directory** (no top-level test command exists for this project —
  `config/projects.md`'s own Commands table): `cloudwaitress.test.ts` 8/8,
  `loyalty-auto-complete/sweep.test.ts` 10/10, `brand-portal/loyalty.test.ts`
  19/19 — 37 tests total, all green. `deno check` on every touched/new file:
  zero new errors (baseline noise in `cloudwaitress.ts`'s outer catch,
  `kitchenhub-auth.ts`, and `brand-portal/utils.ts` confirmed pre-existing
  by diffing error counts via `git stash`/`deno check`/stash-pop before
  writing any code, not assumed).

  **Branch, two commits** (the second additive, not an amend — the first
  was already pushed before the wrong-tenant test was added, same reasoning
  `ENG-048`'s own round 2 used to avoid a force-push to a shared remote):
  `4cd02f5` (the full feature) and `b72ce33` (the wrong-tenant regression
  test). Pushed:
  `origin/feat/ENG-049-loyalty-webhook-accrual-sweep-and-dine-in-earn-api`.
  The two pre-existing untracked `deno.lock` files plus this ticket's own
  fresh `loyalty-auto-complete/deno.lock` all left untracked — checked
  `git ls-files` first and confirmed neither `broadcast-dispatch/deno.lock`
  nor `brand-portal/deno.lock` is tracked in this repo, so untracked is this
  project's own actual convention, not `engineering-standards.md`'s generic
  "lockfiles are committed" line (that document's own first rule: project
  conventions win).

  **Artifact enumeration (step 6b):** `grep -rln
  "loyalty-auto-complete\|record_dine_in_earn\|get_loyalty_balance\|cw_order_id"`
  across `agents/` and `departments/engineering/`. Hits: `ADR-021`, `ENG-027`
  design and board file, `ENG-048` migration/board/security-review,
  `eng027-work-breakdown` notebook, `devops`'s release-readiness log (its
  own already-known 404-until-this-ships observation, unaffected),
  `_index-archive.md` (historical). No conflicting instruction found beyond
  the security-note test already added.

  **2 transitions this pass** (`ready → building`, `building → in-review`),
  under the cap of 4. `state: in-review`, `owner: eng-manager → backend →
  principal-engineer` (next hop: review + QA combined). Machine WIP: this
  ticket is `ENG-027`'s own family, occupying the slot `ENG-048` vacated
  when it parked on the approver — not a second occupant.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `in-review` needs no approver gate.
  Nothing due for a 24h nudge among the open `inbox/` items.

  **8b:** nothing new to observe or propose — the `responses.ts` split and
  the balance-summing fix are both recorded here and in the backend
  notebook, not fragmented into a separate filing. No `exception-request:`
  found. **8c:** n/a — no G1/G2/G3/merge-request answered this pass.

  Full build writeup: `agents/backend/notebook/2026-09-07-eng049-build.md`
  (dependency re-verification, every file changed, the correctness bug and
  its fix, the security forward-notes, full test inventory, PR body draft).

  `chained: ENG-049` — `in-review` is agent-owned (principal-engineer + qa
  combined hop next), not the approver, not blocked, not terminal, not held
  by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-049`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-049` appended behind three already-outstanding
  events (`watch launchd`, `scheduled launchd`, `scheduled auto-drain`).
  `traces/.loop.lock/pid` shows `78771`, a concurrently-held lock, so this
  fire queues rather than launches; the drain runs the queue in order the
  moment the lock frees.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- 2026-09-07 `in-review → in-qa → in-security` (principal-engineer + qa,
  combined hop, `continue ENG-049` event pass, `chained: ENG-049` from this
  ticket's own prior hop). Reading map for `continue`: steps 6 and 6b, plus
  the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The
  four lanes*; *Guards*). Mode check clean (`.env` → `MODE=active`).
  Pre-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-049` and
  whole-board: both exit 0.

  **Review: PASS, round 1.** 0/10 automatic failures. Receipt:
  `agents/principal-engineer/reviews/ENG-049.md`. Independently re-verified
  rather than accepted on the ticket's own account — ran all three new test
  files myself (8/8, 10/10, 19/19, matching exactly), traced the 4 `deno
  check` errors to two pre-existing locations by reading the base
  (`ENG-048`-branch) file directly, cross-read `normalizePhoneForIdentity`
  against `crm/utils.ts`'s own `normalizePhone` line by line, confirmed
  `selectEligibleOrders`'s filter matches `ENG-048`'s own partial-index
  predicate column for column, and confirmed the `responses.ts` split leaves
  the other three `external-integrations` handlers' imports intact via
  `index.ts`'s own re-export (grepped, not assumed).

  **Quality gate: PASS.** Test plan: `agents/qa/test-plans/ENG-049.md` — all
  six fully-owned ACs (6, 10, 13, 14, 17, 18) and all seven half-owned ACs
  (1, 2, 3, 7, 11, 15, 16) covered, cross-checked against `ENG-048`'s own
  test plan for the other half of each; 0 open P0/P1. First `aiorders-api`
  ticket with real, independently-runnable tests rather than inspection or
  SQL-only evidence. The `readBalance` sum-vs-cap bug fix ships with a
  regression test confirmed (by reading the fake's own `.limit()` handling)
  to actually distinguish the fix from the reverted bug, not just assert a
  number.

  Full reasoning: `agents/principal-engineer/notebook/2026-09-07-review-log.md`,
  `agents/qa/notebook/2026-09-07-coverage-gaps.md`.

  **2 transitions this pass** (`in-review → in-qa`, `in-qa → in-security`),
  under the cap of 4. `state: in-security`, `owner: principal-engineer →
  security`. Machine WIP unaffected — still `1/1`, held by the `ENG-027`
  family.

  **Two non-blocking findings, neither holding up this pass:** (1) a
  cosmetic test-naming collision in `loyalty.test.ts`'s `INVALID_AMOUNTS`
  parameterisation (`JSON.stringify` collapses `NaN`/`Infinity`/`null` to
  the same printed name; coverage itself is real) — noted in the review
  receipt, not worth a round. (2) the design's own AC17 language ("the same
  403-shaped error every other brand-portal action already returns") turns
  out not to be literally true anywhere in `brand-portal` — every access
  denial in this file, old and new, actually returns HTTP `500`, not `403`.
  This ticket matches its five siblings exactly and is not the one to fix
  it alone. Filed as a new proposal (`proposals.md`, this date,
  principal-engineer).

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `in-security` needs no approver gate.
  Checked open `inbox/` items for a 24h nudge: none newly due.

  **8b:** one new proposal filed (AC17/403-shaped label, above); one
  existing proposal strengthened in place rather than duplicated
  (`proposals.md`'s 2026-09-03 `aiorders-api` test-harness row — this
  ticket's fourth per-function `deno.json` and 37 real passing tests are new
  evidence for the same already-open ask). No separate observation — both
  findings are fully tracked in the notebooks and `proposals.md` already; a
  third filing would fragment, not clarify. No `exception-request:` found.
  **8c:** n/a — no G1/G2/G3/merge-request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-049` and
  whole-board: both exit 0, clean.

  `chained: ENG-049` — `in-security` is agent-owned (`security` next), not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-049`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-049` appended behind three already-outstanding
  events (`watch launchd`, `scheduled launchd`, `scheduled auto-drain`).
  `traces/.loop.lock/pid` shows `78771`, a concurrently-held lock, so this
  fire queues rather than launches; the drain runs the queue in order the
  moment the lock frees.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No project-repo commit
  this hop — read-only review plus test runs, no application code changed.

- 2026-09-07 **security gate round 1: FAIL — one critical blocking finding**
  (security, `continue ENG-049` event pass, per prior pass's `chained:
  ENG-049`). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*). Also read `skills/security-gate/SKILL.md` in full and
  `agents/eng-manager/config/security-baseline.md` (department copy — not
  carried into this instance's own `config/`). Mode check clean (`.env` →
  `MODE=active`). Pre-pass `sh departments/engineering/lib/eng-gate-check.sh
  ENG-049` and whole-board: both exit 0, clean.

  **Scope.** Same stacked-PR diff round 1 review/QA graded: `feat/ENG-049-...`
  (`4cd02f5`, `b72ce33`) vs `feat/ENG-048-...cron` (`ENG-048`'s own PR #21
  re-confirmed `OPEN`, base `main`, via `gh pr view 21
  --json state,baseRefName,headRefName,mergedAt` this pass — not assumed
  from the prior hop's account). 12 files, 1260/31, matching the review's
  own diffstat exactly (`git diff origin/feat/ENG-048-...cron..HEAD --stat`,
  re-run independently).

  **Threat model (baseline step 2), answered before the checklist:** (1)
  What new input can an attacker control? — every field CloudWaitress's own
  webhook payload carries, because nothing on this route verifies the
  caller is actually CloudWaitress (below). (2) What new capability does
  this grant, and to whom? — this is the finding: an anonymous caller gains
  the ability to mint arbitrary `loyalty_ledger_entries` value. (3) What new
  data does this expose? — none newly read-exposed; the issue is a write,
  not a leak. (4) What breaks if this component is fully compromised? —
  already fully "compromised" by design, since no compromise is required to
  reach it.

  **Finding 1 — Critical, blocking (A08 Software & Data Integrity ×
  A04 Insecure Design, business-logic abuse).** `external-integrations`'s
  CloudWaitress route has never verified the inbound webhook is actually
  from CloudWaitress. Verified directly, not inherited from the ticket's own
  "confirmed pre-existing... explicitly out of this ticket's scope" account
  (board log, build hop, above) or from principal-engineer's round-1 review,
  neither of which treated this as blocking:

  - `CloudWaitressWebhook.secret` (`cloudwaitress.ts:7`) is declared on the
    interface and never once read anywhere in the file — grepped
    (`grep -n secret cloudwaitress.ts`), one hit, the declaration itself.
  - `external-integrations/index.ts`'s router (`Deno.serve`, unchanged by
    this diff) does no auth of its own — confirmed by reading the full
    file; this project's own `supabase/functions/README.md` names the same
    conclusion independently, in its own per-function notes: "No JWT/auth
    check at the top-level router — relies on webhook secrets/service-role
    trust" (`README.md:294`).
  - That reliance is not actually wired up, and the missing half is a live
    value, not a hypothetical: `cloudwaitress-middleware/handlers/
    restaurant.ts:6-7` hardcodes the exact webhook registration CloudWaitress
    is configured with for every restaurant —
    `AIORDERS_WEBHOOK = { _id: 'TI8WLaFR3', secret:
    'e713df50-7251-4998-9be7-2529a531263a', ... }` — the same `secret` field
    `cloudwaitress.ts`'s own interface anticipates and never checks. The
    mechanism this project intended is real and already in the codebase;
    the consuming side simply never compares against it. (The hardcoded
    literal itself is pre-existing, already-tracked debt —
    `README.md`'s own "Known issues" bullet on hardcoded credentials — not
    new and not this finding; named only because it's the proof the check
    is missing, not decorative.)

  **Exploit chain, traced end to end against this diff's own new code, not
  asserted:** (1) POST a forged `order_new` webhook to `{SUPABASE_URL}/
  functions/v1/external-integrations/cloudwaitress` — no credential of any
  kind required — with attacker-chosen `data.order._id` (becomes
  `cw_order_id`), attacker-chosen `data.order.bill.cart` (e.g. `999999`),
  `bill.discount: 0`, and `data.customer` fields matching the attacker's own
  real phone/email (any past legitimate order already resolves one).
  `createOrder()` (`cloudwaitress.ts:185-215`, unchanged by this ticket
  except for the new `cw_order_id` line) persists `bill: orderData.bill`
  verbatim — confirmed by reading the insert directly. (2) Do nothing
  further. `loyalty-auto-complete`'s cron tick (every 15 min,
  `ADR-021`/`ENG-048`'s migration) calls `selectEligibleOrders`
  (`sweep.ts:41-58`, this ticket's own new code, read directly) whose only
  predicate is `cw_order_id is not null AND loyalty_processed_at is null AND
  status != 'cancelled' AND created_at <= now()-24h` — nothing checks the
  order was ever legitimately reported complete by CloudWaitress. Within 24h
  15m of the forged POST, `credit_order_if_eligible` (`ENG-048`'s function,
  confirmed by reading the migration's own SQL) computes
  `v_amount := bill.cart - bill.discount` **from the attacker's own forged
  payload** and inserts a real `loyalty_ledger_entries` row at the
  restaurant's real, legitimately-configured rate. No step of this requires
  guessing a secret, a race, or a privileged credential — one unauthenticated
  HTTP POST, repeatable without bound (a fresh `cw_order_id` per attempt),
  is financial fraud with no cap. **Secondary, lower-confidence consequence
  of the identical root cause, same fix closes it:** if a real order's
  `cw_order_id` is ever guessed or leaked (the migration's own comment
  argues CloudWaitress's Mongo-style ObjectIds make this "practically
  impossible," not independently verified here), the same missing check
  lets an anonymous caller force early completion or wrongful cancellation
  of *that* real order via `handleTerminalOrderEvent` — bounded, unlike the
  fabrication path above, but the same gap.

  **Why this blocks now rather than riding the ticket's own "out of scope,
  no auth-model change" framing.** The design's Risks section (`ENG-027`
  design doc) never once discusses the webhook's own trust boundary — its
  "nothing here...introduces an auth-model change" line (Approach) was
  answering a different question (no new user-facing login flow), not
  asserting the inbound payload is trustworthy. `ENG-048`'s own security gate
  forward-noted exactly this ("confirm the CloudWaitress webhook signature
  is verified before any code path calls `credit_order_if_eligible` with a
  caller-supplied order id... only true if `ENG-049`'s handler actually
  authenticates the inbound webhook") precisely because it could not verify
  the answer from its own diff. The honest answer, now that this ticket's
  diff is what's in front of the gate: no, it does not. Baseline A08 is
  explicit and does not carve out an exception for "the design didn't ask
  for it": **"Webhook signatures verified — always, no 'we'll add it
  later'."** This is also the second time this exact shape has reached this
  gate — a pre-existing, already-known bypass (there: `outgoing-
  communications`'s `systemTriggered` flag; here: this route's never-wired
  `secret` check) that a *new* ticket's own capability turns from a
  standing nuisance into a live, unbounded abuse path (`ENG-038` security
  gate round 1, Finding 1, `2026-09-04`: same reasoning, blocked the same
  way, fixed in the very next hop). Consistent with that precedent and with
  this gate's own refusal to accept risk itself: fixed now, not silently
  passed and not escalated as a risk-acceptance ask — there's a small,
  scoped, mechanical fix on hand, not a disproportionate one.

  **Fix, specified exactly.** Gate `handleCloudWaitress` on the shared
  secret **before any branching on `webhookData.event`** — covering
  `order_new` too, not only the three terminal events this ticket adds:
  gating only the terminal branch leaves the fabrication path above fully
  open, since the sweep credits any inserted order 24h later regardless of
  which webhook event created it. Compare `webhookData.secret` against the
  same value `cloudwaitress-middleware/handlers/restaurant.ts`'s
  `AIORDERS_WEBHOOK.secret` already registers with CloudWaitress for every
  restaurant (one shared constant, not per-restaurant — confirmed by reading
  that file, so a single equality check is complete, no per-restaurant
  lookup needed); reject a mismatch with a 401 and a logged denial (A09),
  matching `loyalty-auto-complete/index.ts`'s own `authorizeServiceRole`
  shape from this same ticket rather than inventing a new one. Source the
  expected value from an env var (e.g. `CLOUDWAITRESS_WEBHOOK_SECRET`) —
  suggested name, not load-bearing — rather than a second hardcoded literal;
  migrating the *existing* hardcoded one in `cloudwaitress-middleware` is
  the separate, already-tracked cleanup item (`README.md`'s "Known issues"),
  not blocking here. No schema change, no interface change, additive guard
  clause only.

  **OWASP walk, remaining categories.** A01 **reviewed, pass** —
  `record_dine_in_earn`/`get_loyalty_balance` both require a real Bearer JWT
  (`brand-portal/index.ts`'s router, confirmed neither is in
  `API_KEY_ALLOWED_ACTIONS`) then `requireRestaurantAccess` with the correct
  argument order (`restaurant_id, supabase, user`, confirmed by reading
  `utils.ts:117-131` directly — not the `feedback.ts`/`offers.ts`
  wrong-order bug the README's own "Known issues" already names). The
  wrong-tenant forward-note is independently confirmed closed:
  `handleTerminalOrderEvent` never reads `webhookData.restaurant_id` for
  anything (read the full function; only `cw_order_id` drives the lookup),
  and `b72ce33`'s own test asserts that affirmatively, re-run here (8/8
  green). A02 n/a — no crypto/session code. A03 clean — no dynamic SQL, no
  shell interpolation, confirmed reading every new file. A05 n/a — no
  config/CORS change beyond the existing `corsHeaders` convention. A06
  clear — `loyalty-auto-complete/deno.json`'s two entries
  (`deno.land/std@0.177.0`, `npm:@supabase/supabase-js@2`) match versions
  already in use elsewhere on this project; no lockfile drift. A07 n/a on
  the parts this ticket owns (`loyalty-auto-complete`'s own service-role
  gate is a direct, correct copy of `ADR-016`-`018`'s established pattern,
  confirmed by reading `auth.ts`). A09 the one gap is the finding above
  (a missing check can't log its own denial); everything else that already
  exists (every catch in `handleTerminalOrderEvent`, `requireRestaurantAccess`'s
  own denial log) is visible, not silent. A10 n/a — no caller-supplied URL
  anywhere in this diff.

  **LLM checklist:** n/a, confirmed directly — no model, agent, tool, MCP,
  or RAG surface anywhere in this diff.

  **Secrets scan:** clean over this diff and its two commits individually
  (`git diff`/`git log -p` vs `ENG-048`'s branch tip) — the one real secret
  literal found this pass (`cloudwaitress-middleware`'s `AIORDERS_WEBHOOK.
  secret`) lives outside this diff, pre-existing, already tracked; not a
  fresh leak.

  **Dependencies:** none new or bumped (A06, above).

  **Negative-case testing (baseline step 6) — the gap.** All 37 tests
  independently re-run (8/10/19 across the three suites, `--no-check`,
  matching round 1's own counts exactly; the same 4 pre-existing `deno
  check` errors confirmed pre-existing by reading the `ENG-048`-branch copy
  of `cloudwaitress.ts` and `kitchenhub-auth.ts` directly). None exercises
  "no valid webhook credential" for this route, because no credential check
  exists to exercise — exactly the "no-token case" this step asks after,
  and precisely why this is a gate finding rather than a QA gap: QA's own
  test plan correctly named the webhook signature check as "out of this
  ticket's scope," which was true of QA's job, not of this gate's.

  **SOC 2 evidence trail:** ticket → PRD → design → code review (pass, round
  1) → test run (pass, round 1) → this verdict. Complete up to here; this
  verdict is the trail's own first gap, which is what this gate is for
  (baseline step 7).

  **No receipt written** — `agents/security/reviews/ENG-049.md` does not
  exist and is not created on a fail (`skills/security-gate/SKILL.md` step
  9; `security-baseline.md` "When the gate fails" §1). `links.security_review`
  left unset. Full findings also logged:
  `agents/security/notebook/2026-09-07-findings.md`.

  Per `skills/security-gate/SKILL.md` step 9: **1 transition** —
  `in-security → building`, owner `security → backend`. WIP/approval caps
  unaffected — still the `ENG-027` family's `1/1` slot, `building` is within
  the counted range.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — a security-gate fail is fixed, not
  escalated, so no gate item was written this pass. Checked all open
  `inbox/` items for the 24h-nudge condition anyway (current time
  `2026-09-08T00:46:46Z`): the two newest (`2026-09-07-eng048-merge-request.md`,
  `notified: 16:18:23`; `2026-09-07-eng050-p0-incident.md`, `notified:
  16:04:16`) are both ~8.5h old, under threshold; every older open item
  already carries a one-time `nudged:` stamp. Nothing nudged.

  **8b:** no new observation or proposal — this finding is fully handled by
  the fail → fix-next-hop cycle, not left for a batch nobody acts on (8b's
  own observation-vs-proposal test). No `exception-request:` found. **8c:**
  n/a — no G1/G2/G3/merge-request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-049` and
  whole-board: both exit 0, clean.

  `chained: ENG-049` — `building` is agent-owned (backend's own fix is the
  next hop), not the approver, not blocked, not terminal, not held by a cap.
  Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-049`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-049` appended behind three already-outstanding
  events (`watch launchd`, `scheduled launchd`, `scheduled auto-drain`).
  `traces/.loop.lock/pid` shows `78771`, a concurrently-held lock, so this
  fire queues rather than launches; the drain runs the queue in order the
  moment the lock frees.

  business-os itself left uncommitted through this pass's edits (the
  ticket's own board file, this board index and its archive, the security
  notebook entry) — same standing default every pass on this board has
  used; the commit-convention question remains open, not re-decided here.
  No project-repo commit this hop — read-only review, no application code
  changed (the fix is the next hop's own work).

- 2026-09-07 **security-fix round 1** `building → in-review` (backend,
  `continue ENG-049` event pass, per prior pass's `chained: ENG-049`).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set
  (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*).
  Mode check clean (`.env` → `MODE=active`). Pre-pass `sh
  departments/engineering/lib/eng-gate-check.sh ENG-049` and whole-board:
  both exit 0, clean. Worktree re-checked fresh before editing:
  `~/Documents/projects/_eng/aiorders-api` on `feat/ENG-049-...`, HEAD
  `b72ce33` (matching where round 1's security hop left it), only the
  three already-known untracked `deno.lock` files present — no prior pass
  died mid-work here. `ENG-048`'s own PR #21 re-confirmed live
  (`gh pr view 21 --json state,baseRefName,headRefName,mergedAt`): still
  `OPEN`, base `main`, not merged — this branch correctly keeps stacking on
  it, not `origin/main`.

  **Fixed exactly what the security gate specified, nothing broader.**
  `cloudwaitress.ts` gains an exported `verifyCloudWaitressSecret(webhookData)`
  — reads `CLOUDWAITRESS_WEBHOOK_SECRET` from env, fails closed if either
  side is unset/empty (an unconfigured deployment can't be satisfied by an
  equally-missing `webhookData.secret`), plain equality otherwise, same
  shape as `loyalty-auto-complete/auth.ts`'s own `authorizeServiceRole`.
  `handleCloudWaitress` calls it immediately after parsing the body and
  before the existing structural-validation check — covering `order_new`
  as well as the three terminal events, per the finding's own requirement
  ("before any branching on webhookData.event"). A mismatch logs
  `console.warn` (event name only, never the secret value) and returns
  `createErrorResponse('Unauthorized', 401)` — `{success:false,
  error:'Unauthorized'}`, matching `loyalty-auto-complete/index.ts`'s own
  401 shape rather than inventing a new one. Left the pre-existing
  hardcoded literal in `cloudwaitress-middleware/handlers/restaurant.ts`
  untouched — that migration is the separate, already-tracked cleanup item
  the finding itself named as out of scope here.

  **Verified the fix actually closes the exploit chain, not just that the
  code compiles.** Added to `cloudwaitress.test.ts`: 4 unit tests on
  `verifyCloudWaitressSecret` directly (match / mismatch / missing
  webhook-side secret / fails-closed when unconfigured even against an
  equally-missing webhook secret) and 4 through `handleCloudWaitress`
  itself — an unauthenticated `order_new` and a wrong-secret terminal event
  both now return `401 {success:false, error:'Unauthorized'}` **and never
  touch `supabase`** (asserted via the existing `tableCalls`/`rpcCalls`
  spies, not just the response shape) — the direct regression test for the
  finding's own traced exploit chain; a correctly-signed ignored event and
  a correctly-signed terminal event both still pass straight through
  unchanged, proving the gate doesn't block legitimate traffic. 16/16
  green (was 8/8 before this round). Re-ran the other two suites this
  ticket owns, untouched by this diff, to confirm no regression:
  `loyalty-auto-complete/sweep.test.ts` 10/10, `brand-portal/loyalty.test.ts`
  19/19 — unchanged counts. `deno check cloudwaitress.ts
  cloudwaitress.test.ts`: the same 4 pre-existing errors at the same
  locations (447/448/451's `error.message` accesses in the outer catch,
  `kitchenhub-auth.ts:92`) — compared line-for-line against round 1's own
  baseline, not just the count; zero new errors from either the fix or the
  new tests.

  **Artifact enumeration (step 6b) for the new artifacts this hop
  introduces:** `grep -rn "CLOUDWAITRESS_WEBHOOK_SECRET\|verifyCloudWaitressSecret"
  --include="*.md" --include="*.sh" --include="*.yaml" agents/ skills/ lib/
  docs/` (department + this instance) — no hits beyond this ticket's own
  board file, so no existing instruction or map needs to be brought into
  agreement. Checked whether a required-secrets doc already exists for
  this project the way `agents/devops/notebook/2026-09-05-release-readiness-log.md`
  tracks `BROADCAST_UNSUBSCRIBE_SECRET` for `ENG-038` — same pattern
  applies here: provisioning `CLOUDWAITRESS_WEBHOOK_SECRET` in the live
  Supabase Function secrets store is a release-readiness/devops check when
  this ticket reaches that gate, not a build-hop concern now. Named here
  so that hop doesn't have to rediscover it.

  **1 transition** (`building → in-review`), well under the cap of 4 —
  deliberately not more: this diff is new code principal-engineer hasn't
  reviewed yet, so it goes back through review + QA combined before
  security re-checks it, same shape as this exact gate's own precedent
  (`ENG-038`: security round 1 → fix → `building → in-review` → a fresh
  combined review+QA pass → security round 2 — read directly from
  `agents/eng-manager/board/ENG-038-broadcast-composer-api-dispatcher-and-unsubscribe.md`
  rather than assumed). `state: in-review`, `owner: security → backend →
  principal-engineer`. Machine WIP unaffected — still `1/1`, held by the
  `ENG-027` family.

  One commit, additive (round 1's two commits already pushed, same
  no-force-push convention this ticket already established): `0bec87c`.
  Pushed: `origin/feat/ENG-049-loyalty-webhook-accrual-sweep-and-dine-in-earn-api`.
  No PR opened for `ENG-049` itself yet — round 1's own build hop didn't
  open one either; that's release-runner's job at `ready-to-ship`, still
  ahead.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — a security-driven code fix isn't a
  gate event. Checked all open `inbox/` items for the 24h-nudge condition
  (current time `2026-09-08T01:04:19Z`): the same two un-nudged items from
  the prior pass (`2026-09-07-eng048-merge-request.md`, `notified:
  16:18:23`; `2026-09-07-eng050-p0-incident.md`, `notified: 16:04:16`) are
  now ~8h46m/~9h00m old — still under 24h. Nothing nudged.

  **8b:** no new observation or proposal — this hop is a scoped fix to an
  already-filed, already-fully-described finding, not new territory. The
  provisioning note above is recorded here for the release-readiness hop
  to find, not a separate filing. No `exception-request:` found. **8c:**
  n/a — no G1/G2/G3/merge-request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-049` and
  whole-board: both exit 0, clean.

  `chained: ENG-049` — `in-review` is agent-owned (review + QA combined is
  the next hop), not the approver, not blocked, not terminal, not held by
  a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-049`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  showed `1 continue ENG-049` appended behind three already-outstanding
  events (`watch launchd`, `scheduled launchd`, `scheduled auto-drain`).
  `traces/.loop.lock/pid` shows `78771`, the same concurrently-held lock
  every prior hop in this pass chain has seen, so this fire queues rather
  than launches; the drain runs the queue in order the moment the lock
  frees.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- 2026-09-07 **review+quality combined hop, round 2** `in-review → in-qa →
  in-security` (principal-engineer + qa, `continue ENG-049` event pass, per
  prior pass's `chained: ENG-049`). Reading map for `continue`: steps 6 and
  6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*; *The four lanes*; *Guards*). Mode check clean (`.env` →
  `MODE=active`). Pre-pass `sh departments/engineering/lib/eng-gate-check.sh
  ENG-049` and whole-board: both exit 0, clean.

  **Scope.** Round 1 passed; security gate round 1 blocked on one critical
  finding (unauthenticated CloudWaitress webhook) and sent the ticket to
  `building`; the fix hop (`0bec87c`) returned it here rather than straight
  to `in-security` — same shape as this exact gate's own `ENG-038`
  round-5→round-6 precedent, read directly from that ticket's own board
  file rather than assumed. Worktree re-checked fresh:
  `~/Documents/projects/_eng/aiorders-api`, HEAD `0bec87c`, branch up to
  date with origin, only the three already-known untracked `deno.lock`
  files present — no prior pass died mid-work. `ENG-048`'s own PR #21
  re-confirmed live (`gh pr view 21 --json state,baseRefName,headRefName,mergedAt`):
  still `OPEN`, base `main` — correctly still stacked, not rebased onto
  `origin/main`. `git show --stat 0bec87c`: 2 files, 165/3, matching the
  prior hop's own account exactly.

  **Review: PASS, round 2.** 0/10 automatic failures, re-scanned fresh.
  Read the fix against the finding's own requirement rather than trusting
  the tests alone: `verifyCloudWaitressSecret` sits immediately after
  `request.json()`, strictly before structural validation and both the
  terminal-event and `order_new` branches, so all three paths the finding
  named are covered, not only the three this ticket originally added.
  Fails closed on its own misconfiguration (confirmed via its own dedicated
  test, not just by reading the line). Exported as a pure, directly-testable
  function — matches `engineering-standards.md`'s "decision logic doesn't
  live trapped inside a bare handler" rule unprompted. Logs the denial
  without ever logging the secret. Receipt:
  `agents/principal-engineer/reviews/ENG-049.md` (`round: 2`).

  **Quality gate: PASS, round 2.** Test plan:
  `agents/qa/test-plans/ENG-049.md`. Graded the 8 new tests as a security
  regression suite rather than a new AC row — neither the PRD's AC list nor
  its Risks section names webhook authentication, consistent with
  `ENG-038`'s own round-6 precedent for a security-gate-originated fix.
  Fresh re-check of all thirteen ACs this ticket owns (six in full, seven by
  half): all still pass, nothing in this round's two-file diff touches any
  of them. 0 open P0/P1.

  **Independently re-verified, not accepted on the fix hop's own account:**
  ran all three suites myself — `cloudwaitress.test.ts` 16/16 (was 8/8, +8
  new), `sweep.test.ts` 10/10, `loyalty.test.ts` 19/19 — 45/45, matching
  exactly. `deno check` on the touched files: the same 4 pre-existing
  errors at the same three lines (447/448/451's `error.message` accesses,
  `kitchenhub-auth.ts:92`), compared line-for-line against round 1's own
  baseline — zero new. The exploit-chain test asserts zero `tableCalls`/
  `rpcCalls` alongside the `401`, proving an unauthenticated caller can't
  get partway through order creation, not just that it eventually gets
  rejected; two positive tests confirm correctly-signed traffic still
  passes and still reaches `credit_order_if_eligible` with the same RPC
  args round 1 already asserted — without them a green suite would be
  equally consistent with an over-broad fix.

  **2 transitions this pass** (`in-review → in-qa`, `in-qa → in-security`),
  under the cap of 4. `state: in-security`, `owner: principal-engineer → qa
  → security`. Machine WIP unaffected — still `1/1`, held by the `ENG-027`
  family.

  **Non-blocking findings:** none new. Two carried forward unchanged from
  round 1 (test-name collision in `loyalty.test.ts`; the AC17 "403-shaped"
  design-language mismatch, already filed as a proposal) — neither file
  touched this round, so neither re-verified fresh.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `in-security` needs no approver
  gate. Checked all open `inbox/` items for the 24h-nudge condition
  (current time `2026-09-08T01:15:39Z`): `2026-09-07-eng048-merge-request.md`
  (`notified: 16:18:23`, ~8h57m old) and `2026-09-07-eng050-p0-incident.md`
  (`notified: 16:04:16`, ~9h11m old) are both still under 24h; every older
  open item already carries a one-time `nudged:` stamp. Nothing nudged.

  **8b:** no new observation or proposal — nothing surfaced this round
  beyond what round 1 already filed. No `exception-request:` found. **8c:**
  n/a — no G1/G2/G3/merge-request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-049` and
  whole-board: both exit 0, clean.

  `chained: ENG-049` — `in-security` is agent-owned (`security` next), not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-049`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-049` appended behind the same three
  already-outstanding events every hop in this pass chain has seen
  (`watch launchd`, `scheduled launchd`, `scheduled auto-drain`).
  `traces/.loop.lock/pid` still shows `78771` at the same `0:00.26` CPU
  time as every prior check this chain has made — the same held lock, not
  a new one — so this fire queues rather than launches; the drain runs the
  queue in order the moment the lock frees.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No commit in the
  `aiorders-api` worktree this hop — read-only review plus test runs, no
  application code changed.

- 2026-09-07 **security gate round 2: PASS** `in-security → ready-to-ship`
  (security, `continue ENG-049` event pass, per prior pass's `chained:
  ENG-049`). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*). Also read `skills/security-gate/SKILL.md` in full and
  `agents/eng-manager/config/security-baseline.md` (department copy — not
  carried into this instance's own `config/`). Mode check clean (`.env` →
  `MODE=active`). Pre-pass `sh departments/engineering/lib/eng-gate-check.sh
  ENG-049` and whole-board: both exit 0, clean.

  **Scope.** Round 1 (this same date) failed on one critical, blocking
  finding — the CloudWaitress webhook route never verified the caller, so an
  unauthenticated POST could fabricate an order the auto-complete sweep
  would credit real loyalty points against 24h15m later — and sent the
  ticket to `building`. The fix (`0bec87c`) went through a fresh combined
  review+QA pass (round 2, PASS, above) before returning here rather than
  straight to a re-check, same shape as this exact gate's own `ENG-038`
  round-1→round-2 precedent, read directly from that ticket's own security
  receipt rather than assumed.

  **Worktree re-checked fresh, not trusted from any prior hop's account:**
  `~/Documents/projects/_eng/aiorders-api`, `git fetch origin`, HEAD
  `0bec87c`, branch up to date with
  `origin/feat/ENG-049-loyalty-webhook-accrual-sweep-and-dine-in-earn-api`,
  only the three already-known untracked `deno.lock` files present — no
  prior pass died mid-work here. `ENG-048`'s own PR #21 re-confirmed live
  (`gh pr view 21 --json state,baseRefName,headRefName,mergedAt`): still
  `OPEN`, base `main`, not merged — this branch correctly still stacks on it
  rather than `origin/main`. `git show --stat 0bec87c`: 2 files, 165
  insertions / 3 deletions, matching every prior hop's account exactly.

  **Threat model, re-run against this round's diff only:** (1) attacker-
  controlled input is now *less* than before this fix, not more — the same
  payload fields exist but are unreachable without the shared secret. (2)
  new capability granted — none; this is a capability removal. (3) new data
  exposed — none. (4) what breaks under full compromise — unchanged in kind:
  if `CLOUDWAITRESS_WEBHOOK_SECRET` itself leaks, the same exploit chain
  round 1 traced still runs; that residual is inherent to CloudWaitress's
  own in-band shared-secret webhook design (confirmed by reading
  `cloudwaitress-middleware/handlers/restaurant.ts`'s registration shape,
  unchanged and out of this ticket's scope to redesign), not a gap in this
  fix.

  **Read the fix against the finding's own requirement directly, not
  accepted on the backend's, principal-engineer's, or QA's account of it.**
  `verifyCloudWaitressSecret` sits immediately after `request.json()` and
  strictly before the structural-validation check, the terminal-event
  branch, and the `order_new` branch — all three paths the finding named are
  covered, not only the three this ticket originally added. Fails closed:
  `if (!expected || !provided) return false` — an unset
  `CLOUDWAITRESS_WEBHOOK_SECRET` never matches an equally-missing
  `webhookData.secret`. Sourced from an env var, not a second hardcoded
  literal — grepped `git show 0bec87c` for the real registered secret
  literal, zero hits. `console.warn` on a mismatch logs the event name only,
  never the secret value, in either direction — closes round 1's own named
  A09 gap (no visible denial where none existed before).

  **Independently re-verified, not accepted on any prior hop's counts.** Ran
  all three suites myself from each function's own directory:
  `cloudwaitress.test.ts` **16/16** (was 8/8 at round 1, +8 new),
  `sweep.test.ts` **10/10** (unchanged), `loyalty.test.ts` **19/19**
  (unchanged) — **45/45, 0 failed**. `deno check cloudwaitress.ts
  cloudwaitress.test.ts`: 4 errors at lines 447/448/451 (outer `catch`
  block's untyped `error.message` accesses) plus `kitchenhub-auth.ts:92` —
  confirmed pre-existing *this round*, not just re-counted, by reading
  `git show 60fa06e:supabase/functions/external-integrations/handlers/
  cloudwaitress.ts` (the `ENG-048`-branch tip, before any `ENG-049` commit)
  directly: the identical three `error.message` accesses already exist there
  at lines 340/341/344, shifted down by this ticket's own earlier code.
  **Zero new errors.** Secrets scan: `git log -p 4cd02f5..0bec87c` over both
  touched files — the only removed literal is the pre-existing non-sensitive
  test fixture default (`secret: "x"`), every new test fixture value is
  synthetic, the real registered secret does not appear anywhere in this
  diff.

  **Read the four new unit tests and four new handler tests directly, not
  just their names.** The exploit-chain test
  (`rejects order_new with no configured secret... before ever touching
  supabase`) asserts `res.status === 401` **and** `tableCalls.length === 0`
  **and** `rpcCalls.length === 0` — proving the request never reaches
  Supabase at all, the exact property the finding needed, not a generic 401
  check. A second rejection test covers a terminal event with a wrong
  secret, closing the one gap a narrower fix (gating only the three new
  terminal events) would have left open. Two positive tests confirm the gate
  doesn't block legitimate traffic. This closes round 1's own named gap
  exactly (the "no-token case" QA correctly scoped out of its own job).

  **Both of `ENG-048`'s own forward notes for this gate now closed:** (1)
  webhook signature verification — closed by this round's fix. (2)
  wrong-tenant/ownership case — independently re-confirmed already closed by
  round 1's own test (`handleTerminalOrderEvent` never reads
  `webhookData.restaurant_id`), unaffected by this round's diff.

  **One new non-blocking finding: A02/A07-adjacent, low severity.**
  `verifyCloudWaitressSecret`'s `provided === expected` is a standard JS
  string equality check, not constant-time — in principle a timing side
  channel on the secret. Not blocking: the real secret is a full UUID
  (`cloudwaitress-middleware`'s `AIORDERS_WEBHOOK.secret`, ~122 bits) checked
  over a public HTTP round trip, where network jitter dwarfs a
  single-character V8 string-compare delta, and CloudWaitress's own webhook
  contract already sends the secret in-band in the body rather than as an
  HMAC-signed header — this fix authenticates against the mechanism the
  integration actually has; a constant-time compare would narrow an
  already-impractical channel, not close an open one. Fix, if picked up next
  time this function is touched: a constant-time comparison (fixed-length
  HMAC or byte-by-byte with no early return). Not filed as a proposal —
  specific to this one function, not a systemic pattern across the project.
  Logged in `agents/security/reviews/ENG-049.md` and
  `agents/security/notebook/2026-09-07-findings.md`. Two findings carried
  forward unchanged from review round 2 (test-naming nit in
  `loyalty.test.ts`; AC17's "403-shaped" design language vs. this file's
  actual `500`, already filed as a proposal round 1) — neither file touched
  this round.

  **SOC 2 evidence trail:** ticket → PRD → design → code review (round 2,
  pass) → QA (round 2, pass) → this verdict → release record (pending,
  devops next). Round 1 left this trail's one gap open by design (a fail
  writes no receipt); this pass closes it.

  **Receipt written:** `agents/security/reviews/ENG-049.md`.
  `links.security_review` set on the ticket in this same write.

  **1 transition** (`in-security → ready-to-ship`), under the cap of 4.
  `state: ready-to-ship`, `owner: security → devops`. Machine WIP unaffected
  — still `1/1`, held by the `ENG-027` family (`ready-to-ship` is within the
  counted `ready`..`ready-to-ship` range).

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `ready-to-ship` needs no approver
  gate at this hop; release-runner raises its own merge-request item once
  devops opens the PR, not this one. Checked all open `inbox/` items for the
  24h-nudge condition (current time `2026-09-08T01:26:32Z`):
  `2026-09-07-eng048-merge-request.md` (`notified: 16:18:23`, ~9h08m old)
  and `2026-09-07-eng050-p0-incident.md` (`notified: 16:04:16`, ~9h22m old)
  are both still under 24h; every older open item already carries a
  one-time `nudged:` stamp. Nothing nudged.

  **8b:** no new observation or proposal — the timing-comparison finding is
  fully tracked in the security receipt and notebook, scoped to one
  function, not a systemic pattern (8b's own observation-vs-proposal test).
  No `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-049` and
  whole-board: both exit 0, clean.

  `chained: ENG-049` — `ready-to-ship` is agent-owned (`devops`/
  release-runner next), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-049`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-049` appended behind the same three
  already-outstanding events every hop in this pass chain has seen (`watch
  launchd`, `scheduled launchd`, `scheduled auto-drain`). `traces/.loop.lock/pid`
  still shows `78771`, now at `4:25:19` elapsed — the same held lock, not a
  new one — so this fire queues rather than launches; the drain runs the
  queue in order the moment the lock frees.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No commit in the
  `aiorders-api` worktree this hop — read-only review plus test runs, no
  application code changed.

- 2026-09-07 **release-readiness** `ready-to-ship → blocked` (devops,
  `continue ENG-049` event pass, per prior pass's `chained: ENG-049`).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set
  (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*).
  Also read `skills/release-runner/SKILL.md` in full. Mode check clean
  (`.env` → `MODE=active`). Pre-pass `sh
  departments/engineering/lib/eng-gate-check.sh ENG-049` and whole-board:
  both exit 0, clean.

  **Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`,
  re-confirmed) — no window check applies, straight to step 4's readiness
  content.

  **Step 2 — all three gates re-read fresh from the receipt files:**
  `agents/principal-engineer/reviews/ENG-049.md` (pass, round 2),
  `agents/qa/test-plans/ENG-049.md` (pass, round 2, 45/45), `agents/security/reviews/ENG-049.md`
  (pass, round 2). No migration owed — confirmed no
  `agents/database/migrations/ENG-049-*.md` exists, correct for a Deno/TS-only
  diff (schema is `ENG-048`'s).

  **Step 3 (readiness gate) — the one that mattered this time:**
  `CLOUDWAITRESS_WEBHOOK_SECRET` is not provisioned in the live Supabase
  Function secrets store, checked directly (`supabase secrets list
  --project-ref bmnmnejwdxbcqinqkwko`, 34 entries, none matching) rather
  than assumed from the security receipt's own note. Read
  `cloudwaitress.ts` myself before characterizing the risk: the secret
  check (line 325) runs before every branch on `webhookData.event`,
  including plain `order_new` — so an unset secret doesn't just leave
  loyalty crediting open, it 401s **all** CloudWaitress traffic the moment
  this deploys, stopping order intake entirely. Materially worse than
  `ENG-039`'s own `BROADCAST_UNSUBSCRIBE_SECRET` gap (per-message, loud,
  logged) — this one is total and silent from the caller's side. Judged
  non-blocking for *opening this PR* only (no CI/CD on this repo; merging
  doesn't deploy; the actual `supabase functions deploy` is a separate,
  future, manual act) but flagged as a **hard pre-deploy requirement**, at
  maximum prominence, in the PR body, the merge-request item, and
  `agents/devops/notebook/2026-09-07-release-readiness-log.md` — not a
  "known limitation to live with" the way the unsubscribe gap was. The
  actual secret value is never reproduced in any of those three places
  (referenced by file path — `cloudwaitress-middleware/handlers/
  restaurant.ts`'s own `AIORDERS_WEBHOOK.secret` — instead), since a PR on
  a real GitHub repo is a more exposed surface than this internal
  notebook. This department does not provision production secrets
  unilaterally (same boundary `ENG-039` already established) — named for
  whoever runs the eventual deploy, not fixed here.

  Rollback: reasoned (no migration in this diff; reverting removes these
  code paths going forward; a loyalty entry already credited before a
  revert stands, per this ticket's own already-accepted design, not a
  fresh gap). Cost: $0/month, no new infrastructure. Window: n/a, L1. No
  blocking readiness failure for the PR itself. Full reasoning:
  `agents/devops/notebook/2026-09-07-release-readiness-log.md`.

  **Step 4 (route):** worktree re-checked fresh (`git fetch origin`, HEAD
  `0bec87c`, only the three known untracked `deno.lock` files, no prior
  pass died mid-work). `ENG-048`'s PR #21 re-confirmed `OPEN`, base `main`
  — opened this PR stacked on it rather than `main`, per this ticket's own
  Notes. **Opened `aiorders-api` PR #22**
  (https://github.com/harsimranwalia/aiorders-api/pull/22, base
  `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`). Wrote
  `inbox/2026-09-07-eng049-merge-request.md`, plain `pr_url:` string
  (single repo), the webhook-secret requirement repeated at the top of the
  item. `lib/eng-notify.sh raise` exited 0, confirmed sent
  (`traces/eng-notify-2026-09-07.log`: `18:44:54`); stamped `notified:
  2026-09-07T18:44:54` by hand, copied verbatim from the log.

  Ticket set `blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, `owner: devops → approver`, `links.pr` set to PR #22. No
  G3 — L1 has none. No release record yet — L1's actual deploy and the
  release record both wait for merge detection on a future pass, per the
  skill's own step 4 L1 row / step 7 split; that future hop must not skip
  the webhook-secret check above (named in the devops notebook so it isn't
  rediscovered from the PR alone).

  **Slot freed, and nothing filled it — checked, not assumed.** `ENG-049`
  was the last of `ENG-027`'s two sub-tickets (a strict chain, no third
  child per the board's own `Next ID` note) — with `ENG-048` and now
  `ENG-049` both `blocked_on: approver`, the family holds no ticket in the
  counted `ready..ready-to-ship` range, so per `eng_build_loop.md` Guards
  (amended 2026-09-07, part (b)) the slot is free with no next sibling to
  fill it. Checked the top of To-do (the only place a new start is drawn
  from, step 6, read literally): `ENG-018`, `ENG-028`, `ENG-042`
  (`awaiting-scope`) and `ENG-043` (`intake`) are the only occupants;
  grepped each item's own inbox file for a `decision:` field — none
  present, all four genuinely still unanswered. Nothing startable.
  **Deliberately did not fall back to the `designed`-state "held-for-slot
  pool"** `ENG-019`'s/`ENG-020`'s/`ENG-021`'s/`ENG-026`'s own dispatches
  used in this exact situation on four earlier passes — `eng_build_loop.md`
  step 6 states plainly that `intake`/`shaped`/`awaiting-scope` "is the
  only place a new start is drawn from," and nothing in the document
  (read in full this pass) sanctions that pool; filed as a proposal
  (`proposals.md`, this date, devops) rather than a fifth quiet repetition
  or an uninstructed unilateral reversal of established board practice.
  Wrote the one permitted item: `inbox/IDLE-2026-09-07.md` — no other
  "nothing I can start" item was already open. `lib/eng-notify.sh raise`
  exited 0, confirmed sent (`18:44:54`, same log), stamped by hand.

  **Dead-end sweep (scoped to this event):** no other ticket touched
  beyond the To-do check above, which the slot-freed guard itself
  requires.

  **Notify sweep:** the two new items raised above. Checked every other
  open `inbox/` item for the 24h-nudge condition (current time
  `2026-09-08T01:43:37Z`): `2026-09-07-eng048-merge-request.md` (`notified:
  16:18:23`, ~9h25m old) and `2026-09-07-eng050-p0-incident.md` (`notified:
  16:04:16`, ~9h39m old) both still under 24h; every older open item
  already carries its one-time `nudged:` stamp. Nothing nudged.

  **8b:** one new proposal filed (the To-do-vs-`designed`-pool discrepancy,
  above) — this is a proposal, not an observation, because leaving it
  unfiled means the same tension gets silently re-decided by pattern-match
  on the next idle episode rather than by a rule anyone actually chose.
  No `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-049` and
  whole-board: both exit 0, clean.

  **Board update:** ticket frontmatter (`state`, `owner`, `blocked_on`,
  `blocked_from`, `links.pr`) and this entry; In-flight table's `ENG-049`
  row updated to `blocked`/`approver`; `IDLE-2026-09-07.md` and this
  ticket's own new merge-request paragraph added to "Waiting on the
  approver"; count line updated. Live file held three dated entries before
  this one; oldest (`continue (ENG-049)`: security-fix round 1 —
  `building → in-review`) rolled to `_index-archive.md` per the keep-three
  rule, done before this entry was written so the count stays at three.

  `chained: none — idle: nothing startable` — `ENG-027`'s family fully
  parked (both children `blocked_on: approver`, no more children), and
  every To-do occupant is genuinely blocked on an unanswered approver item.
  This is not `chained: none — blocked_on: approver`, which this step may
  not write per the Guards amendment — the reason logged is the idle
  condition the slot-freed check actually found, with the one permitted
  "Nothing I can start" item raised to match.

  business-os itself left uncommitted through this pass's edits (this
  ticket's own board file, the board index and its archive, the devops
  notebook, `proposals.md`, the two new inbox items) — same standing
  default every pass on this board has used; the commit-convention
  question remains open, not re-decided here. `aiorders-api`'s own commit
  history is unchanged this hop — release-readiness and PR-opening only,
  no application code touched.
