---
id: ENG-053
title: Loyalty redemption — brand-portal redeem_points action
project: aiorders-api
type: feature
size: S
time_estimate: half a day
time_spent:
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
branch: feat/ENG-053-loyalty-redemption-brand-portal-api
depends_on: [ENG-052]
blocks: []
parent: ENG-051
links:
  prd: agents/product-manager/specs/ENG-051-redemption-api-and-qr-issuance-scanning.md
  design: agents/architect/designs/ENG-051-redemption-api-and-qr-issuance-scanning.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-053.md
  test_plan: agents/qa/test-plans/ENG-053.md
  security_review: agents/security/reviews/ENG-053.md
  release:
  pr: https://github.com/harsimranwalia/aiorders-api/pull/25
---

## Problem

`ENG-051`'s design adds a staff-facing redemption action, but nothing calls
`ENG-052`'s new `redeem_points_if_eligible` function yet — a restaurant staff
member has no way to actually redeem a diner's points at the point of sale
until this ships.

## Outcome

`brand-portal/loyalty.ts` gains a new `redeemPoints` handler, wired into
`handleLoyalty`'s switch and `brand-portal/index.ts`'s router (+1
`case 'redeem_points':` line, same pattern the two existing loyalty actions
already use). Payload `{restaurant_id, code, points, idempotency_key}`.
`requireRestaurantAccess(restaurant_id, supabase, user)` runs first — a
caller without access to that restaurant gets the same failure shape every
other `requireRestaurantAccess` denial in this file already produces (AC10).
`code`/`idempotency_key` missing, or `points` not a positive finite number →
a `400`-shaped rejection, no RPC call made. Otherwise calls
`supabase.rpc('redeem_points_if_eligible', {p_platform_customer_id: code,
p_restaurant_id: restaurant_id, p_points: points, p_idempotency_key:
idempotency_key, p_created_by: user.id})`. On `invalid_code` or
`not_enrolled`, returns `{success: true, result}` directly — a live, distinct
result, not a fabricated success. On `insufficient_balance` or `redeemed`,
also calls the existing, unchanged `readBalance(supabase, code,
restaurant_id)` and attaches the diner's current balance to the response.
`LoyaltyLedgerEntry`'s `source` union type widens to include `'redemption'`.

## Notes

Design: `agents/architect/designs/ENG-051-redemption-api-and-qr-issuance-scanning.md`
— `## Interfaces` (the `brand-portal` action's exact contract, argument
names, and per-status response shaping).

**Do not build or test against a live `redeem_points_if_eligible` call until
`ENG-052` has actually shipped and its grants are confirmed closed** —
calling it against an unprivileged role before the revoke/grant fix lands
would either fail for the wrong reason or (worse) succeed via the
`pg_default_acl` gap `ENG-048`'s own security gate found on
`credit_order_if_eligible`. `ENG-052`'s own Notes name the exact
verification query (`has_function_privilege('anon', ...)` → `false`) to
confirm before relying on the function being safe to call from an
authenticated context.

**Follow the same wiring shape every existing `brand-portal` action already
uses** (`requireRestaurantAccess` first, then the action body) — see
`record_dine_in_earn`/`get_loyalty_balance` (`ENG-027`/`ENG-049`) for the
closest existing example, both in the same file this ticket modifies.

**AC10's failure shape is `500`-shaped in practice, not `403`-shaped, despite
the PRD's own language** — `principal-engineer`'s 2026-09-07 finding
(`ENG-049`'s own security-gate history): every `requireRestaurantAccess`
denial in this file today is a thrown `Error`, caught by `index.ts`'s
top-level handler, returned as `500`. This ticket matches its siblings
exactly and is not the one to fix that mismatch — an unrelated,
already-flagged, project-wide inconsistency (`engineering-standards.md`
forbids the drive-by fix).

**Branch fresh off `origin/main`, not stacked off `ENG-052`.** `ENG-052`
(no dependency) is dispatched to `building` in the same pass this ticket was
created and is expected to reach an open PR well before this ticket's own
dependency check runs — same reasoning `ENG-049`'s own Notes used for
`ENG-048`. If `ENG-052`'s PR is still open when this ticket's `depends_on`
check runs, that pass branches from `ENG-052`'s own branch instead (a
stacked PR, per `eng_build_loop.md` Guards) and says so in this ticket's own
Log; not assumed here since it hasn't happened yet.

**AC ownership** (mapped in full in
`agents/eng-manager/notebook/2026-09-08-eng051-work-breakdown.md`): this
ticket owns AC10 in full, and half of AC3, AC4, AC7, AC8, and AC11 — the
handler-caller half; the guard/debit half belongs to `ENG-052`. No sub-ticket
proves AC3, AC4, AC7, AC8, or AC11 alone — check both together. Neither
sub-ticket owns AC1/AC2 (QR issuance) — already satisfied by `ENG-006`'s
shipped `platform_customers.id`.

## Log

- 2026-09-08 `(created) → ready` (eng-manager, `work-breakdown`, `continue
  ENG-051` event pass) — sub-ticket of `ENG-051`, sequence 2,
  `depends_on: [ENG-052]` unmet — stays `ready`, owner `eng-manager`, until
  `ENG-052` ships (an open PR is enough, per `eng_build_loop.md` Guards'
  2026-09-07 amendment — not full `verified`). `time_estimate` half a day, 0h
  spent. Machine WIP: part of `ENG-051`'s own family, not a second occupant
  of the `1/1` slot. Full reasoning:
  `agents/eng-manager/notebook/2026-09-08-eng051-work-breakdown.md`.
  `chained: none` — dependency unmet; resumes once `ENG-052` reaches a state
  that satisfies it.

- 2026-09-08 `ready → building → in-review`, `owner: eng-manager → backend →
  principal-engineer` (backend, `continue ENG-053` event pass — fired by
  `ENG-052`'s own `ready-to-ship → blocked` hop, "slot freed by `ENG-052`").
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
  7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*) — this
  ticket is not mid-PRD, so step 2's checkpoint note doesn't apply. Mode
  check clean (repo-root `.env` → `MODE=active`, no `ENG_RELEASE_FREEZE`).
  Pre-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and
  whole-board: both exit 0, clean.

  **Startability re-confirmed fresh, not trusted off `ENG-052`'s own account:**
  `gh pr view 24 --repo harsimranwalia/aiorders-api` — `state: OPEN`,
  `baseRefName: main`, `mergedAt: null`. Per Guards' 2026-09-07 amendment, an
  open PR satisfies `depends_on` — `ENG-053` does not wait for `verified`.
  `priority` unset, not `hold`; `blocked_on` empty; `grep -rl "ENG-053"
  inbox/*.md` finds only `ENG-052`'s own merge-request item naming it, no
  unanswered scope/decision question against `ENG-053` itself.

  **Stacked PR, per this ticket's own Notes** ("If `ENG-052`'s PR is still
  open when this ticket's `depends_on` check runs, that pass branches from
  `ENG-052`'s own branch instead... and says so in this ticket's own Log").
  `ENG-052`'s PR is still open (above), so branched from
  `feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function`
  (worktree already sitting on it, in sync with `origin`, no stray
  uncommitted state) rather than `origin/main`. New branch
  `feat/ENG-053-loyalty-redemption-brand-portal-api`. This ticket's own
  eventual merge request will name `ENG-052` as the PR that must merge
  first (step 5).

  **Artifact enumeration (step 6b), before writing anything:**
  `grep -rn "redeem_points\b\|redeemPoints\|RedeemPointsPayload"` across
  `agents/` (instance) and `agents/ skills/ lib/ docs/` (department, zero
  hits). Every instance hit is this same ticket family's own already-
  reconciled plan (`ENG-051`/`ENG-052`/`ENG-053` board files, the
  work-breakdown notebook, the design, `ADR-022`) — no conflicting
  instruction anywhere else.

  **Built per the Outcome section and the design's own Interfaces.**
  `brand-portal/loyalty.ts`: new `RedeemPointsPayload` interface; new
  `redeemPoints(data, supabase, user)` — `restaurant_id` presence, then
  `requireRestaurantAccess` (AC10), then `code`/`idempotency_key` presence
  and `points` positive-finite check, then
  `supabase.rpc('redeem_points_if_eligible', {p_platform_customer_id: code,
  p_restaurant_id, p_points: points, p_idempotency_key: idempotency_key,
  p_created_by: user.id})`; `invalid_code`/`not_enrolled` return directly;
  `insufficient_balance`/`redeemed` attach balance via the existing,
  unchanged `readBalance(supabase, code, restaurant_id)`. `handleLoyalty`'s
  switch gains `case 'redeem_points'`. `LoyaltyLedgerEntry.source` widened
  to add `'redemption'`. `brand-portal/index.ts`: exactly the `+1 case
  'redeem_points':` line the Components table calls for, alongside the two
  existing loyalty actions.

  **One judgment call, not resolved silently — the design's own "400-shaped
  rejection" language for missing `code`/`idempotency_key`/invalid `points`
  cannot be built literally without exceeding this ticket's own scope.**
  `index.ts`'s top-level `catch` is a single hardcoded `status: 500` with no
  mechanism today for a handler to signal a different code, and the design's
  own Components table caps this ticket's `index.ts` change at the one
  router-case line — no catch-block change is in scope. Checked
  `proposals.md` before deciding: the 2026-09-07 `principal-engineer` row
  (found on `ENG-049`) is this exact mechanism gap, one instance of it
  (`record_dine_in_earn`'s AC17 "403-shaped" language, actually 500), with
  the fix explicitly scoped as its own S–M ticket ("a caller-visible
  behavior change across all six actions in this file"). `ENG-051`'s design
  is a **second, independent** design doc making the same category of claim
  ("400-shaped") the current router cannot literally produce — reinforcing
  that proposal, not a new defect of this ticket's own making. Resolution:
  validation failures `throw new Error(...)`, same mechanism and depth as
  `recordDineInEarn`'s own `phone`/`amount` checks (which also just throw),
  surfacing as `500` via the existing generic catch — consistent with every
  other rejection in this file, this ticket's own AC10 included. Not filed
  as a fresh observation or proposal — a fourth-plus confirmation of an
  already-escalated proposal is noise, not signal, same call `ENG-052`'s own
  release-readiness hop made for the notify-timestamp discrepancy. Named
  here, and in the PR body below, so review/security can weigh in if they'd
  read the design's instruction more literally.

  **Self-checked, no test suite exists for this project to run.**
  `config/projects.md`: `aiorders-api` has no `package.json` and no
  `deno.json` — an already-recorded gap, not this ticket's to fill; neither
  `record_dine_in_earn` nor `get_loyalty_balance` (`ENG-027`/`ENG-049`)
  shipped with a test file either. Ran `deno check` against both changed
  files from outside the repo tree (avoids the `npm:` specifier resolution
  failure `deno check` hits when run from inside, with no local
  `deno.json`/`node_modules` to anchor it): zero errors in `loyalty.ts` or
  `index.ts` or in the new code itself; the pre-existing errors surfaced
  (`utils.ts`, `profiles.ts`, `restaurants.ts`, `website.ts` — all untyped
  `catch (error)` bindings, one unrelated `website.ts` typing gap) are in
  files this ticket doesn't touch, confirmed by line/file, not assumed.

  **PR body drafted** (`building`'s own exit condition; no PR opened yet —
  L1 opens it at release-readiness, base set to `ENG-052`'s branch per the
  stacking decision above):
  - *What it does:* Adds the `redeem_points` brand-portal action —
    `redeemPoints` handler, wired into `handleLoyalty` and `index.ts`'s
    router. Validates access then input, calls `ENG-052`'s
    `redeem_points_if_eligible`, returns its live result, attaches balance
    on `insufficient_balance`/`redeemed`. Widens `LoyaltyLedgerEntry.source`.
  - *What it deliberately does not do:* No frontend, no QR rendering (whole
    sequence's own non-goal). No new balance-read endpoint — AC11's own
    handler-caller half is satisfied by the type widening alone, per the
    work-breakdown notebook's own AC-mapping. Does not fix the pre-existing,
    already-flagged 500-vs-"error-code-shaped" language gap on
    `requireRestaurantAccess` denials or on this ticket's own new validation
    path — named below, not fixed, per `engineering-standards.md`'s
    drive-by-fix prohibition.
  - *Uncertainties:* the 500-vs-400 judgment call above is the one thing in
    this diff that isn't a mechanical application of an existing pattern —
    flagged in case the design's intent was a literal wire-level `400`,
    which would need its own, separately-scoped change to `index.ts`'s catch
    block (already proposed, unactioned, `proposals.md` 2026-09-07 row).
  - *What to review hardest:* (1) the 500-vs-400 call; (2) `code` needs no
    resolution step before reaching the RPC — it's `platform_customers.id`
    verbatim, the design's own central finding; (3) validation order (access
    → field checks → RPC → balance attach) matches the design's Interfaces
    section exactly, field checks strictly before any RPC call.

  Branch committed (`fff72f0`, 2 files, 70 insertions/1 deletion) and
  pushed: `origin/feat/ENG-053-loyalty-redemption-brand-portal-api`, base
  `feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function`.

  **2 transitions this pass** (`ready → building`, `building → in-review`),
  under the cap of 4 — `in-review` (principal-engineer, code review) is a
  fresh session's work per `eng_build_loop.md`'s "a pass stops after
  `building` on purpose"; this pass performed the build itself (the
  dispatch-only precedent `ENG-020`/`ENG-021`'s own "stopped there, chained
  instead" applies to a *new machine start* off the `designed` pool, not to
  a same-family sibling whose own dependency just cleared — the closest
  precedent is `ENG-052`'s own `building → in-review` hop, which also
  performed its full build inside the pass that held `building`). Machine
  WIP: still `1/1`, held by the `ENG-051` family (parent `ENG-051` still
  `building`) — unaffected, `in-review` is still inside the counted
  `ready..ready-to-ship` range.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract.

  **Notify sweep (step 7):** nothing raised this pass — `in-review` needs no
  approver gate. Nothing of this ticket's own to nudge (no open gate item on
  `ENG-053` itself). Did not sweep the rest of `inbox/` for staleness — same
  scoping every prior `continue`-event hop on this exact ticket family has
  used (`ENG-052`'s own `building → in-review` and `in-review → in-security`
  hops both declined this for the same stated reason: that's the
  `scheduled`/`watch` sweep's job); the one prior hop that did sweep fully
  was itself raising a new gate item at the same time, which this hop is
  not.

  **8b:** one judgment call recorded above (500-vs-400), not filed as a
  fresh observation or proposal — reinforces the existing 2026-09-07
  `proposals.md` row rather than adding a new one (reasoning above). No
  `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and
  whole-board: both exit 0, clean.

  `chained: ENG-053` — `in-review` is agent-owned (principal-engineer, code
  review next), not the approver, not blocked, not terminal, not held by a
  cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-053`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-053` appended behind one already-outstanding `watch
  launchd` event; no `*-eng-events-dropped.md` for today.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. `aiorders-api` commit
  `fff72f0` is on the ticket's own feature branch, pushed to `origin`, not to
  `main` — the L1 boundary this whole lane runs inside.

- 2026-09-08 `in-review → building`, `owner: principal-engineer → backend`
  (principal-engineer + qa, combined hop, `continue ENG-053` event pass,
  round 1). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*) — this ticket is not mid-PRD. Mode check clean
  (repo-root `.env` → `MODE=active`, no `ENG_RELEASE_FREEZE`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and whole-board:
  both exit 0, clean.

  Ran `skills/code-review-gate/SKILL.md` and QA's own quality gate
  concurrently on the same diff (`fff72f0` vs `0a2f730` — `ENG-052`'s own
  commit, this ticket's stacked base — 2 files, 70 insertions/1 deletion).

  **Review: FAIL, round 1.** 0/10 automatic failures. Design conformance
  otherwise clean — confirmed line-by-line against
  `agents/architect/designs/ENG-051-....md`'s Interfaces section (payload
  shape, access-then-validation order, the RPC call's exact argument names,
  all four outcome branches, `source` union widening) — no drift. The
  500-vs-400 judgment call named in the prior Log entry is real but not new,
  a second instance of the already-escalated 2026-09-07 proposal.

  **One blocking finding: `redeemPoints` shipped with zero test coverage, in
  a file that already has a real, passing suite covering its two sibling
  functions.** `brand-portal/loyalty.ts` has carried `loyalty.test.ts` since
  `ENG-049` (2026-09-07) — 19 tests, `recordDineInEarn`/`getLoyaltyBalance`/
  `readBalance`/`handleLoyalty`'s routing. Re-ran it fresh against this
  ticket's own branch rather than trusting the prior Log entry's own account
  (`deno test --no-check`, from outside the repo tree — the same
  `npm:`-resolution workaround that entry used for `deno check`): **19
  passed, 0 failed**, nothing regressed by this diff — but zero of the 19
  touch `redeem_points`/`redeemPoints` (`grep -n "redeemPoints\|redeem_points"
  loyalty.test.ts`: no hits). This ticket added ~50 lines of new branching
  logic (3 validation branches, 4 RPC-outcome branches) to the exact file
  that suite exists for and extended none of it.

  **The prior Log entry's own "no test suite exists for this project"
  claim is false for this specific file** — true only for the SQL/migration
  side (no `deno.json`, verified by disposable replica instead, same as
  `ENG-048`/`ENG-052`). `loyalty.test.ts` is real and `deno test`-runnable in
  this exact environment, written by this ticket's own immediate predecessor
  on the same file three days ago — this is a same-file regression in a
  practice `ENG-049` itself established, not an inherited project-wide gap.
  Full findings, the specific round-2 fix list (four items — including that
  the fix must assert the RPC is *never called* on a validation rejection,
  the design's own load-bearing claim), and a non-blocking note on an
  AC-number collision across `ENG-049`'s and `ENG-051`'s own numbering in
  this same file: `agents/principal-engineer/notebook/2026-09-08-review-log.md`.

  **QA: gate ran concurrently on the same diff, independently landed on the
  identical root cause** (missing coverage, not a design/logic defect) —
  acceptance coverage (AC10 full, handler-caller half of AC3/AC4/AC7/AC8/
  AC11) confirmed correct by inspection but unproven by test; failure-path
  table (unauthorised caller, boundary input, all four RPC outcomes) same
  verdict. No suite/bug filed — round discarded. Full:
  `agents/qa/notebook/2026-09-08-coverage-gaps.md`.

  **No receipt written for either agent** — fail discards the round, per
  `code-review-gate/SKILL.md` step 8/9 and the same rule for QA. `links.review`/
  `links.test_plan` stay unset.

  **1 transition this pass** (`in-review → building`), under the cap of 4.
  `state: building`, `owner: principal-engineer → backend` (the implementing
  agent, unchanged from before `in-review`). Machine WIP unaffected — still
  `1/1`, held by the `ENG-051` family.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep (step 7):** nothing raised — a fail returns to `building`,
  not the approver. Nothing of this ticket's own to nudge. Did not sweep the
  rest of `inbox/` for staleness, same scoping every prior `continue`-event
  hop on this exact ticket family has used.

  **8b:** one observation filed (`observations.md`, this date,
  `principal-engineer`/`aiorders-api`) — `config/projects.md`'s "no test
  files" claim is stale for `aiorders-api` (nine `.test.ts` files now exist
  under `brand-portal/` alone); not corrected in that file this pass, out of
  a code-review hop's own scope. No `exception-request:` found. **8c:** n/a
  — no G1/G2/G3/merge-request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and
  whole-board: both exit 0, clean.

  `chained: ENG-053` — `building` is agent-owned (`backend`, to apply the
  fix next), not the approver, not blocked, not terminal, not held by a cap.
  Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-053`
  before this pass exits.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No project-repo commit
  this hop — read-only review, no application code changed.

- 2026-09-08 `building → in-review`, `owner: backend → principal-engineer`
  (backend, `continue ENG-053` event pass, applying round-2's fix list).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set
  (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*) —
  this ticket is not mid-PRD. Mode check clean (repo-root `.env` →
  `MODE=active`, no `ENG_RELEASE_FREEZE`). Pre-pass
  `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and whole-board:
  both exit 0, clean.

  **Read the round-1 findings before touching anything**
  (`agents/principal-engineer/notebook/2026-09-08-review-log.md`'s own
  `ENG-053` section) rather than re-deriving the gap — one blocking finding,
  a specific 4-item round-2 fix list against `loyalty.test.ts`, all sized to
  this ticket (explicitly not the systemic 500-vs-400 gap).

  **6b:** no new artifact/rule introduced by this hop — it adds test
  coverage for an action (`redeem_points`) and RPC (`redeem_points_if_eligible`)
  already enumerated and reconciled in the ticket's own first build hop; the
  grep sweep is not repeated for a hop that instructs no producer and adds no
  state name, receipt path, or config key.

  **Fix, in the worktree
  (`~/Documents/projects/_eng/aiorders-api`, branch unchanged):** extended
  `loyalty.test.ts`'s existing `makeSupabase`/`makeLedgerTable` harness —
  the same fake-`SupabaseClient` pattern `recordDineInEarn`'s own tests
  already use, plus an `.rpc()` stub shaped like `acquisition.test.ts`'s own
  (records each call, resolves a configurable `{data, error}`) — and a
  `queryCount()` counter on the ledger stub (mirrors the file's own existing
  `insertedRows.length` side-effect-proof idiom) to prove `readBalance`
  (which only ever touches `loyalty_ledger_entries`) was not reached, rather
  than inferring it from response shape alone. All four round-2 items
  covered: (1) `restaurant_id`/`code`/`idempotency_key` missing and 7
  invalid-`points` values (0, -5, `NaN`, `Infinity`, string, `null`,
  `undefined`, matching `record_dine_in_earn`'s own `INVALID_AMOUNTS`
  pattern) — each asserts the rejection message and `rpcCalls.length === 0`;
  (2) access denied via `requireRestaurantAccess` — propagates, RPC never
  called; (3) all four RPC outcomes via a stubbed `.rpc()` result each —
  `invalid_code`/`not_enrolled` assert the exact response shape (no
  `balance` key) and `ledger.queryCount() === 0`,
  `insufficient_balance`/`redeemed` assert the correct summed balance
  attached; (4) `handleLoyalty routes both actions...` renamed to `routes
  all three actions...` and extended to dispatch `redeem_points` through the
  switch, asserting one `.rpc()` call reaches
  `redeem_points_if_eligible`. No changes to `loyalty.ts` or `index.ts` —
  round 1 found no defect in the implementation itself, only the missing
  coverage.

  **Self-checked, same workaround prior hops on this ticket used.**
  `deno test --no-check` against the full `brand-portal/*.test.ts` set from
  outside the repo tree: **119 passed, 0 failed** (34 in `loyalty.test.ts`
  alone, up from 19 — 15 new), nothing regressed. `deno check` against
  `loyalty.test.ts`: 3 pre-existing errors, all in `utils.ts` (untyped
  `catch (error)` bindings and an implicit-`any` callback param — the same
  file/class of gap the first build hop's own account named), zero in
  `loyalty.ts`, `loyalty.test.ts`, or `index.ts` — confirmed by filtering
  the check output for those three filenames, not assumed.

  Branch committed (`ec5e099`, 1 file, 141 insertions/4 deletions) and
  pushed to `origin/feat/ENG-053-loyalty-redemption-brand-portal-api` — no
  change to the base (`ENG-052`'s branch, still open, per the stacking
  decision already on this ticket's own Log).

  **1 transition this pass** (`building → in-review`), under the cap of 4.
  Sent straight back to `in-review` rather than stopping at `building` —
  same precedent this ticket's own first hop recorded (a same-family
  build-and-advance is not a new machine start off the `designed` pool) and
  the review session gets a fresh context to re-run round 2 independently,
  not this same session grading its own fix. Machine WIP unaffected — still
  `1/1`, held by the `ENG-051` family.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep (step 7):** nothing raised — `in-review` needs no approver
  gate. Nothing of this ticket's own to nudge. Did not sweep the rest of
  `inbox/` for staleness, same scoping every prior `continue`-event hop on
  this exact ticket family has used.

  **8b:** no new observation or proposal — this hop closes an already-filed
  finding rather than surfacing a new one. No `exception-request:` found.
  **8c:** n/a — no G1/G2/G3/merge-request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and
  whole-board: both exit 0, clean.

  `chained: ENG-053` — `in-review` is agent-owned (principal-engineer +
  QA, round 2, next), not the approver, not blocked, not terminal, not held
  by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-053`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-053` appended behind three already-outstanding
  events (`watch launchd`, `scheduled auto-drain`, `scheduled launchd`); no
  `*-eng-events-dropped.md` for today.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. `aiorders-api` commit
  `ec5e099` is on the ticket's own feature branch, pushed to `origin`, not
  to `main`.

- 2026-09-08 **review+quality combined hop, round 2** `in-review → in-qa →
  in-security`, `owner: principal-engineer → qa → security` (principal-engineer
  + qa, `continue ENG-053` event pass, per prior hop's `chained: ENG-053`).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
  7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*) — this
  ticket is not mid-PRD. Mode check clean (repo-root `.env` → `MODE=active`,
  no `ENG_RELEASE_FREEZE`). Pre-pass `sh
  departments/engineering/lib/eng-gate-check.sh ENG-053` and whole-board: both
  exit 0, clean.

  **Scope.** Round 1 failed on one blocking finding (zero test coverage for
  `redeemPoints`); the fix hop (`ec5e099`) extended `loyalty.test.ts` only —
  no change to `loyalty.ts`/`index.ts` this round. Worktree re-checked fresh:
  `~/Documents/projects/_eng/aiorders-api`, `git fetch origin`, HEAD `ec5e099`,
  branch up to date with origin, only the three already-known untracked
  `deno.lock` files present. `ENG-052`'s own PR #24 re-confirmed live
  (`gh pr view 24 --json state,baseRefName,mergedAt`): still `OPEN`, base
  `main` — correctly still stacked, not rebased.

  **Review: PASS, round 2.** 0/10 automatic failures, re-scanned fresh. Read
  each of round 1's four fix-list items against the actual new tests, not the
  ticket's own account: all eleven negative-input tests assert both the
  rejection message and `rpcCalls.length === 0`; the four RPC-outcome tests
  assert `ledger.queryCount()` (zero on `invalid_code`/`not_enrolled`, nonzero
  on `insufficient_balance`/`redeemed`) alongside the correctly-summed balance
  — a mutation-sensitive property, not a tautology; `handleLoyalty`'s renamed
  test now dispatches `redeem_points` end to end and confirms exactly one
  `.rpc()` call reaches `redeem_points_if_eligible`. Receipt:
  `agents/principal-engineer/reviews/ENG-053.md`.

  **Quality gate: PASS, round 2 (first non-discarded receipt for this
  ticket).** Test plan: `agents/qa/test-plans/ENG-053.md`. Fresh acceptance
  re-check: AC10 in full, the handler-caller half of AC3/AC4/AC7/AC8/AC11 —
  all pass, each now backed by a test rather than "correct by inspection."
  The three failure-path rows round 1's own coverage-gaps entry found
  unexercised (unauthorised caller, boundary input, all four RPC outcomes)
  are all closed. 0 open P0/P1 (`agents/qa/bugs/_index.md` unchanged — one
  open item, `BUG-001`, P2, unrelated project area).

  **Independently re-verified, not accepted on the fix hop's own account:**
  `deno test --no-check` on `loyalty.test.ts` alone — 34/34 (was 19, +15
  new, matching exactly); full `brand-portal/*.test.ts` — 119/119, nothing
  regressed. `deno check` on `loyalty.test.ts` alone — same 3 pre-existing
  `utils.ts` errors as round 1, zero new; on the three-file set including
  `index.ts` (pulls in every sibling handler transitively) — 24 pre-existing
  errors across `profiles.ts`/`restaurants.ts`/`utils.ts`/`website.ts`, none
  in the files this ticket touches.

  **2 transitions this pass** (`in-review → in-qa`, `in-qa → in-security`),
  under the cap of 4. `state: in-security`, `owner: principal-engineer → qa →
  security`. Machine WIP unaffected — still `1/1`, held by the `ENG-051`
  family.

  **Non-blocking findings:** none new. One carried forward unchanged from
  round 1 (the AC-number collision across `ENG-049`'s and `ENG-051`'s own
  numbering in this file) — neither docstring touched this round, not
  re-verified fresh.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep (step 7) — full inbox check this hop, not scoped to this
  ticket alone**, per the reading map's own "every event, not negotiable"
  listing for step 7 (no ticket-scoping language anywhere in that step's
  text, unlike step 8's dead-end sweep). Nothing of `ENG-053`'s own to raise
  — `in-security` needs no approver gate. Checked all 10 open `inbox/` items
  against the 24h-nudge condition (current local time `2026-09-08T16:10`):
  `inbox/IDLE-2026-09-07.md` — `notified: 2026-09-07T18:44:54`, no `nudged:`,
  no `decision:`, ~28h old — **nudged this pass**
  (`lib/eng-notify.sh nudge`, confirmed sent in
  `traces/eng-notify-2026-09-08.log`, stamped `nudged: 2026-09-08T16:10:48`).
  `inbox/2026-09-08-eng-loop-integrity-check.md` (`notified: 09:58:53`,
  ~13h old) and `inbox/2026-09-08-eng052-merge-request.md` (`notified:
  14:41:39`, ~1h29m old) both still under 24h. Every other open item already
  carries a one-time `nudged:` stamp. Full reasoning for why this hop swept
  the whole inbox where this ticket's own two prior hops didn't:
  `observations.md`, this date.

  **8b:** one observation filed (`observations.md`, this date,
  `eng-manager`/`aiorders`) — the notify-sweep scoping correction above, plus
  a live reconfirmation (not re-filed) of the already-proposed
  `lib/eng-notify.sh` `MODE`-clobber bug (`proposals.md`, 2026-08-25 row):
  this pass's own nudge call logged `sent: active`, not `sent: nudge`, same
  as every prior occurrence. No `exception-request:` found. **8c:** n/a — no
  G1/G2/G3/merge-request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and
  whole-board: both exit 0, clean.

  `chained: ENG-053` — `in-security` is agent-owned (`security` next), not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-053`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-053` appended behind four already-outstanding events
  (`watch launchd` ×2, `scheduled auto-drain`, `scheduled launchd`), lock
  held by pid `98802`; no `*-eng-events-dropped.md` for today.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No commit in the
  `aiorders-api` worktree this hop — read-only review plus test runs, no
  application code changed.

- 2026-09-08 `in-security → ready-to-ship`, `owner: security → devops`
  (security, `continue ENG-053` event pass — fired by the prior hop's own
  `chained: ENG-053`). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*) — this ticket is not mid-PRD, so step 2's checkpoint note
  doesn't apply. Mode check clean (repo-root `.env` → `MODE=active`, no
  `ENG_RELEASE_FREEZE`). Pre-pass `sh
  departments/engineering/lib/eng-gate-check.sh ENG-053` and whole-board:
  both exit 0, clean. No active row in `agents/eng-manager/config/gate-waivers.md`.

  **Ran `skills/security-gate/SKILL.md` in full**, not the receipt-bookkeeping
  shortcut. Inputs read fresh: `agents/eng-manager/config/security-baseline.md`
  (department copy — this instance has no per-instance override, same
  precedent every prior gate on this project has used),
  `agents/architect/designs/ENG-051-....md` + `ADR-022` (trust boundaries —
  the redemption code is a bearer credential by design, deferred, not this
  ticket's to fix), `agents/qa/test-plans/ENG-053.md` (PASS, round 2),
  `agents/eng-manager/config/projects.md` (`aiorders-api`, **L1** — no L0
  boundary restrictions apply), and `agents/security/notebook/` (scanned all
  six dated files for `loyalty`/`brand-portal` clustering — nothing new
  beyond two already-tracked, low-severity A05 patterns, below).

  **Worktree re-verified fresh, not trusted off the ticket's own account:**
  `~/Documents/projects/_eng/aiorders-api`, `git fetch origin`, HEAD
  `ec5e099`, only the three already-known untracked `deno.lock` files
  present. `ENG-052`'s own PR #24 re-confirmed `OPEN`, base `main`,
  `mergedAt: null` — correctly still stacked. Read the actual diff
  (`git diff 0a2f730..ec5e099`, 3 files, 211 insertions/5 deletions) rather
  than the ticket's summary of it — matches exactly.

  **Threat-modelled the change (4 questions), then walked OWASP A01–A10 in
  full** — every category marked applicable or `n/a` with a reason. Full
  writeup: `agents/security/reviews/ENG-053.md`. Highlights, not a
  restatement of the receipt:
  - **A01, and both items `ENG-052`'s own gate flagged forward — closed,
    independently confirmed rather than taken on trust.** Read
    `requireRestaurantAccess`/`verifyRestaurantAccess` (`utils.ts`) directly:
    a real `brand_id`-scoped ownership check runs before `code`/`points`/
    `idempotency_key` are read at all, and its denial log
    (`` `Restaurant access denied: user=${user.id} restaurant=${restaurantId}` ``)
    carries no diner `code` — confirms the wrong-tenant gate is real and the
    bearer-credential exposure isn't widened by this diff (the two things
    flagged forward). Negative-case test re-read directly, not summarized:
    asserts both the rejection and `rpcCalls.length === 0`.
  - **A07/"no-token"**, the leg `ENG-052`'s own gate explicitly deferred to
    this layer: confirmed by reading `index.ts`'s auth resolution (unchanged,
    pre-existing) that a missing/invalid Bearer token gets `401` via a real
    `supabase.auth.getUser` call before any dispatch, and that `redeem_points`
    is absent from `API_KEY_ALLOWED_ACTIONS` — a static `x-api-key` cannot
    reach this action, only a full user JWT can.
  - **A03/A06/A08/A02/A10:** n/a, confirmed by reading the diff directly —
    parameterised `.rpc()` call, no new import, no deserialization/webhook/
    crypto/outbound-fetch code anywhere in it.
  - **A04:** reviewed — race/double-redemption protection lives in
    `redeem_points_if_eligible` itself (`ENG-052`'s own advisory lock +
    idempotency ordering, independently verified there, unchanged here);
    `points` validated `number && finite && > 0` before any RPC call, all 7
    boundary cases re-run (below). No new rate limit on the action itself —
    same posture as its two siblings and the PRD's own deferred
    bearer-credential tradeoff, not new or worsened here.
  - **A05 — two pre-existing, already-tracked patterns named, neither new to
    this diff, neither re-proposed:** (1) `details: error.message` on the
    generic `500` catch (`index.ts`, unchanged, predates this ticket) is a
    **6th+ occurrence** of the pattern `agents/security/notebook/
    2026-09-03-findings.md` (`ENG-022`) already tracks — this ticket's own
    throw messages checked individually, none carry a secret or the diner
    `code`. (2) Repo-wide `Access-Control-Allow-Origin: '*'` (`index.ts`,
    unchanged) is the same class `2026-09-02-findings.md` already named for
    `admin-portal` (low severity there: Bearer-token auth, not
    cookie-based) — **first time named for `brand-portal` specifically**,
    same reasoning applies verbatim, not filed as a fresh proposal, same
    "one repo-wide fact restated" call the 2026-09-02 entry made for its own
    directory. Not written to a fresh `agents/security/notebook/` entry
    either — matches `ENG-052`'s own precedent (no notebook entry on a clean
    pass whose findings are fully captured in the receipt itself).
  - **A09:** reviewed, pass — every path is a real, visible outcome, no
    silent no-op; access denial logged without the diner code (above).

  **LLM checklist:** n/a, confirmed directly — no model/agent/tool/MCP/RAG
  surface anywhere in this diff.

  **Secrets — this ticket's own two commits, diff and full history**
  (`git log -p 0a2f730..ec5e099`; the stacked base `0a2f730` already scanned
  clean by `ENG-052`'s own gate): grepped
  `key|secret|password|token|bearer|AKIA|BEGIN (RSA|EC|PGP|OPENSSH)|api[_-]?key`,
  excluding the expected `idempotency_key`/`x-api-key`/
  `SUPABASE_SERVICE_ROLE_KEY` identifier names — zero matches.

  **Dependencies:** none new or bumped — no new import anywhere in the diff.

  **Negative-case testing (baseline step 6) — independently re-run, not
  accepted on QA's or the build hop's own counts.** `deno test --no-check`
  from outside the repo tree: `loyalty.test.ts` alone — **34 passed, 0
  failed** (matches QA's own count exactly); full `brand-portal/*.test.ts` —
  **119 passed, 0 failed**, nothing regressed. Re-read each of the 11
  boundary/missing-field tests and all four RPC-outcome tests individually:
  every rejection asserts `rpcCalls.length === 0`, every outcome asserts
  exact response shape plus `ledger.queryCount()` — mutation-sensitive, not
  cosmetic, confirmed by reading the assertions themselves rather than
  trusting the test plan's own description of them.

  **PII handling:** no new PII. `code` is a Supabase Auth subject id, not
  independently PII per `ADR-022`'s own Consequences; handling here doesn't
  widen exposure beyond what `ENG-006`'s shipped QR-issuance groundwork
  already established (confirmed above: not logged, not returned beyond the
  same shape `get_loyalty_balance` already returns). Data classification
  unchanged: **Internal**.

  **SOC 2 evidence trail — confirmed present and non-empty on disk, not
  assumed:** ticket → PRD
  (`agents/product-manager/specs/ENG-051-....md`) → design + ADR
  (`agents/architect/designs/ENG-051-....md`, `ADR-022`) → code review
  (`agents/principal-engineer/reviews/ENG-053.md`, PASS round 2) → test run
  (`agents/qa/test-plans/ENG-053.md`, PASS round 2) → this verdict → release
  record (pending — correct, no PR opened yet; opens at release-readiness,
  base `ENG-052`'s branch per the stacking decision already on this ticket's
  own Log). No gap.

  **Verdict: PASS.** No blocking finding. Both items `ENG-052`'s own gate
  flagged forward closed, independently confirmed. Two pre-existing,
  already-tracked, non-blocking A05 patterns named, neither new, neither
  re-proposed. Receipt written: `agents/security/reviews/ENG-053.md`.
  `links.security_review` set on this ticket in the same write (frontmatter,
  above). Per `skills/security-gate/SKILL.md` step 9 — write only on `pass`,
  which this is.

  **1 transition this pass** (`in-security → ready-to-ship`), under the cap
  of 4. `state: ready-to-ship`, `owner: security → devops`. Machine WIP
  unaffected — still `1/1`, held by the `ENG-051` family; `ready-to-ship` is
  still inside the counted `ready..ready-to-ship` range, so no slot frees
  yet (that happens on the next hop, once a PR is actually open and the
  ticket parks on the approver).

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep (step 7) — full inbox check this hop, not scoped to this
  ticket alone**, per the reading map's own "every event, not negotiable"
  listing for step 7 and the prior hop's own established reading (no
  ticket-scoping language anywhere in step 7's text, unlike step 8's
  dead-end sweep). Checked all 10 open `inbox/` items (current local time
  `2026-09-08T16:23`) against the 24h-nudge condition: none crossed it since
  the prior hop's own check 13 minutes earlier —
  `inbox/2026-09-08-eng-loop-integrity-check.md` (~6h25m old) and
  `inbox/2026-09-08-eng052-merge-request.md` (~1h42m old) both still under
  24h with no `nudged:` yet; every other open item already carries a
  one-time `nudged:` stamp. No item carries an unprocessed `decision:`
  field. Nothing raised or nudged this pass.

  **8b:** no new observation — the one tracking-worthy note (CORS wildcard
  now confirmed in `brand-portal`, not just `admin-portal`) is fully
  captured in the review receipt itself; duplicating it into
  `observations.md` would be redundant, and it doesn't clear the "would be
  disappointed if nobody acted on it" bar for a proposal (matches the
  already-established non-proposal disposition for the identical pattern in
  `admin-portal`, 2026-09-02). No `exception-request:` found. **8c:** n/a —
  no G1/G2/G3/merge-request answered this pass.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and
  whole-board: both exit 0, clean.

  `chained: ENG-053` — `ready-to-ship` is agent-owned (`devops`,
  release-readiness next — `skills/release-runner/SKILL.md`, same next step
  `ENG-052`'s own identical transition took), not the approver, not blocked,
  not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-053`
  before this pass exits — confirmed queued, not dropped: `traces/.pending`
  shows `1 continue ENG-053` appended behind three already-outstanding
  events (`watch launchd`, `scheduled auto-drain`, `scheduled launchd`); no
  `*-eng-events-dropped.md` for today.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. No commit in the
  `aiorders-api` worktree this hop — read-only review plus test runs, no
  application code changed.

- 2026-09-08 `ready-to-ship → blocked` (devops, `continue ENG-053` event
  pass — release-readiness hop, `skills/release-runner/SKILL.md`, fired by
  the prior hop's own `chained: ENG-053`). Reading map for `continue`: steps
  6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*; *The four lanes*; *Guards*) — this ticket is not mid-PRD.
  Mode check clean (repo-root `.env` → `MODE=active`, no
  `ENG_RELEASE_FREEZE`). Pre-pass `sh
  departments/engineering/lib/eng-gate-check.sh ENG-053` and whole-board:
  both exit 0, clean.

  **Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`,
  re-confirmed directly) — no window check applies; steps 2-3's readiness
  content still runs, minus the window bullet.

  **Step 2 (upstream gates) — all three re-read fresh from the receipt
  files, not from the ticket log's own account, all passing:**
  `agents/principal-engineer/reviews/ENG-053.md` (`verdict: pass`, round 2),
  `agents/qa/test-plans/ENG-053.md` (`Verdict: pass, round 2`),
  `agents/security/reviews/ENG-053.md` (`verdict: pass`). Migration: n/a —
  no schema/data-model change; `ENG-052` owns the function this ticket
  calls.

  **Step 3 (readiness gate):**
  - *Rollback:* reasoned, not drilled — no migration in this diff, nothing
    destructive to rehearse (same shape `ENG-049`'s own release-readiness
    hop used for its own handler-only diff). Reverting the merge removes the
    `redeem_points` code path going forward; a redemption already recorded
    in the ledger before a revert stands — no undo mechanism exists in
    either direction, same accepted design `ENG-049`'s own crediting-side
    record carries.
  - *Observability:* no gap. Read `index.ts` directly
    (`grep -n "catch\|console\." supabase/functions/brand-portal/index.ts`):
    the generic top-level `catch` (`console.error('Error in brand-portal
    function:', error)`, pre-existing, unchanged) already covers every
    failure this action can produce; security's own review already
    confirmed the access-denial log carries no diner code.
  - *Cost:* $0/month — same Supabase project and edge function
    (`brand-portal`), no new infrastructure, no new compute.
  - *Window:* n/a, L1.

  No blocking readiness failure.

  **Step 4 (route):** worktree
  (`~/Documents/projects/_eng/aiorders-api`) re-checked fresh: `git fetch
  origin`; branch `feat/ENG-053-loyalty-redemption-brand-portal-api` up to
  date with origin at `ec5e099`, no drift; only the three already-known
  untracked `deno.lock` files present — no prior pass died mid-work.
  `ENG-052`'s own PR #24 re-confirmed live (`gh pr view 24 --repo
  harsimranwalia/aiorders-api --json state,baseRefName,mergedAt`): still
  `OPEN`, base `main`, `mergedAt: null` — this ticket's branch correctly
  still stacks on it. `gh pr list --head
  feat/ENG-053-loyalty-redemption-brand-portal-api --state all` — empty,
  confirmed no PR already existed for this branch. `git diff
  origin/feat/ENG-052-...​...HEAD --stat`: 3 files, 211 insertions/5
  deletions — matches every prior gate's own account, no drift.

  Opened `aiorders-api` PR #25
  (https://github.com/harsimranwalia/aiorders-api/pull/25), base
  `feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function` (the
  stacking decision recorded on this ticket's own first build hop). Body:
  what it does, what it deliberately does not do, all three gate receipts
  with paths, the 500-vs-400 judgment call, what to review hardest,
  rollback, observability, cost, and the stacked-base note naming `ENG-052`
  as the PR that must merge first.

  Wrote `inbox/2026-09-08-eng053-merge-request.md`, plain `pr_url:` string
  (single repo). `lib/eng-notify.sh raise` exit 0, confirmed sent from the
  log (`traces/eng-notify-2026-09-08.log`: `sent: active
  2026-09-08-eng053-merge-request.md`, `16:35:41`); stamped `notified:
  2026-09-08T16:35:41` on the item, copied verbatim from the log.

  Ticket set `blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, `owner: devops → approver`, `links.pr` set. No G3 — L1 has
  none; the PR merge is the human gate. No release record yet — L1's actual
  deploy and the release record both wait for merge detection on a future
  pass, per the skill's own step 4 L1 row / step 7 split, same precedent
  `ENG-052`'s own identical hop set.

  **Slot freed — and this is the family's last child, not just another
  sibling hand-off.** `ENG-051` has exactly two children (`ENG-052`,
  `ENG-053` — confirmed against `ENG-051`'s own board file, "two sub-tickets
  ... both `aiorders-api`"). With this hop, **both** are now `blocked`,
  `blocked_on: approver` — per Guards' 2026-09-07 amendment (b), a
  `building` parent with every child parked or verified has a free slot,
  filled "the next child with a satisfied dependency, else the top of the
  designed pool ('the top of To-do' until 2026-09-08) — same pass." `ENG-051`
  has no remaining child to dispatch.

  **Did not fill it — the only route to a new dispatch relies on the
  disputed, unconfirmed 2026-09-08 text, and this pass will not spend that
  authority.** Checked fresh, not carried over from memory of the
  situation: `grep -rn "^decision:" inbox/*.md` — zero hits, across all 11
  currently-open items including this pass's own new one.
  `grep -n "2026-09-08" agents/eng-manager/config/decision-journal.md` —
  only the routine `ENG-048`/`ENG-049` merge rows and `ENG-051`'s own G1
  approval, none mentioning a designed-pool decision. `git status` on the
  four disputed files (`departments/engineering/schedules/eng_build_loop.md`,
  both `config.yaml`s, `agents/eng-manager/proposals.md`) — all four still
  modified, uncommitted, exactly as `inbox/2026-09-08-eng-loop-integrity-check.md`
  describes. This is the same fork two independent passes already hit today
  (the `continue ENG-029` pass and a `scheduled` pass, per that item's own
  17:09Z and 19:29Z updates) and both declined for the same reason — this
  pass is a third, arriving via a different route (a family's last child
  parking, not an idle-check re-fire), and reaches the same conclusion
  independently rather than assuming the prior declines still hold.

  **Checked whether the pre-2026-09-08 rule offers an uncontested
  alternative before concluding there's nothing to chain — it doesn't.**
  The 2026-09-07 text this amendment replaced read "the top of **To-do**"
  for this exact fallback. Swept the board's own In-flight table
  fresh (`agents/eng-manager/board/_index.md`): no ticket anywhere is
  currently at `ready` — every non-`ENG-051`-family ticket is either
  `designed` (`ENG-014`, `ENG-017`, `ENG-023`, `ENG-025`, `ENG-029`,
  `ENG-030`, `ENG-035`, `ENG-036`, `ENG-050`) or on an unanswered approver
  question at `awaiting-scope`/`intake` (`ENG-018`, `ENG-028`, `ENG-042`,
  `ENG-043`). A To-do ticket cannot enter `ready` without first being
  shaped, passing G1, and being designed — none of that is machine-startable
  within this pass regardless of which fallback text is authoritative, so
  "top of To-do" is not a live alternative here either; the only path to an
  actual new start is the disputed `designed`-pool draw itself. Not
  substituting `ENG-050` (the P0) or any other `designed` ticket in
  `ENG-051`'s place — that would rely on exactly the unverified authority
  the open incident item is asking the approver to confirm or reject, the
  same reasoning both prior declines used.

  **`chained: none — idle: designed-pool dispatch policy still unconfirmed
  (`inbox/2026-09-08-eng-loop-integrity-check.md`), and the pre-amendment
  fallback (To-do) has nothing machine-startable either — no ticket
  anywhere on the board is at `ready``.** Not raising a fresh "Nothing I can
  start" item — `inbox/IDLE-2026-09-07.md` (open, `gate: intake-question`)
  and `inbox/2026-09-08-eng-loop-integrity-check.md` (open, `gate:
  incident`) already cover this exact question from two angles; a third
  item while both sit undecided would violate "never a second while one is
  still undecided." Added a short corroborating update to the incident item
  instead (below) rather than treating this as a silent no-op, since a
  future pass checking that file's own history should see that a third,
  differently-triggered pass independently hit the same fork.

  **Machine WIP:** `ENG-051` family now holds zero rows in the counted
  `ready..ready-to-ship` range (both children parked) — the slot is free
  but unoccupied, not reassigned. No second family dispatched.

  **Dead-end sweep (scoped to this event):** no other ticket's board file
  touched. `agents/eng-manager/board/_index.md`'s own "Waiting on the
  approver" section still stops at `ENG-018`'s G1 (2026-09-06) and lists
  neither `ENG-050`'s P0, `ENG-028`'s/`ENG-042`'s G1s, nor `ENG-052`'s or
  this ticket's own merge requests — a continuation of the exact drift
  `observations.md`'s 2026-09-07 row already named and flagged "worth a
  proposal ... if a second family is found the same way." Noted below
  (8b), not fixed here — reconciling that whole section is beyond a single
  ticket's release-readiness hop.

  **Notify sweep (step 7) — full inbox check this hop, not scoped to this
  ticket alone**, since this hop raises a new gate item (same reading this
  ticket's own `in-security` and prior release-readiness-shaped hops
  already established for step 7's no-scoping text). Checked all 11 open
  `inbox/*.md` items (current local time `2026-09-08T16:34`) against the
  24h-nudge condition: `inbox/2026-09-08-eng-loop-integrity-check.md`
  (`notified: 2026-09-08T09:58:53`, no `nudged:`, ~6h36m old) and this
  pass's own new `2026-09-08-eng053-merge-request.md` (just raised) are
  both under 24h. Every other open item already carries its one-time
  `nudged:` stamp (confirmed via `grep -E "^notified:|^nudged:|^decision:"`
  across all 11 files). Nothing nudged this pass.

  **8b:** two items —
  (1) Added a short update to `inbox/2026-09-08-eng-loop-integrity-check.md`
  recording that this pass independently re-hit the same unconfirmed
  designed-pool question via a new trigger (a family's last child parking,
  not an idle-check re-fire) and declined the same way — see that file's
  own new update block. Not a fresh incident item; the existing one already
  covers it.
  (2) One-line addition to `observations.md` (this date,
  `eng-manager`/`aiorders-api`): `board/_index.md`'s "Waiting on the
  approver" section is stale since 2026-09-06 across at least four items
  now (`ENG-050`, `ENG-028`, `ENG-042`, `ENG-052`'s and this ticket's own
  merge requests) — third-plus occurrence of the pattern the 2026-09-07 row
  already flagged as proposal-worthy; not raised as a proposal itself here,
  left for whichever pass next does a board-wide reconciliation sweep to
  judge against the three-strike bar.
  No `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  answered this pass; the merge request raised above is unanswered, nothing
  to journal yet.

  Post-pass `sh departments/engineering/lib/eng-gate-check.sh ENG-053` and
  whole-board: both exit 0, clean.

  `chained: none — idle:` (reasoning above — the freed slot has no
  uncontested candidate; see the two updated inbox items for what would
  close this). Did **not** fire `lib/eng-trigger.sh continue` for any other
  ticket this pass.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here. `aiorders-api` commit
  history unchanged this hop; PR #25 opened against already-pushed commits,
  to `feat/ENG-052-...`, not to `main` — the L1 boundary this whole lane
  runs inside.

- `2026-09-09` `blocked → shipped` (control center, merge detected) — `feat/ENG-053-loyalty-redemption-brand-portal-api` is an ancestor of `origin/main`. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree.

- `2026-09-09T07:33 PDT` `shipped → verified` (product-manager, acceptance-check,
  `continue ENG-051` event). AC10 (fully owned) + caller half of AC3/4/7/8/11
  (checked with `ENG-052`, per Notes) — all pass, verified live:
  `brand-portal` redeployed `v87` at `2026-09-09T14:16:53Z`, after both PR
  merges — read `loyalty.ts`/`utils.ts`/`index.ts` directly: `redeemPoints`
  calls `requireRestaurantAccess` first, denial → thrown `Error` → `500`,
  same shape every sibling action in this file uses; `readBalance`'s
  `entries` query is source-agnostic, so a `redemption` row surfaces
  automatically. Non-goals clear, cost matches estimate. Full walk:
  `agents/product-manager/notebook/2026-09-09-eng052-eng053-acceptance.md`.
  `owner: approver → eng-manager`. Git ops and post-pass gate-check: see
  `ENG-051`'s own entry.
  `chained: n/a` — terminal (`verified`) this hop; nothing to chain for it
  specifically. See `ENG-051`'s own log for this pass's chain decision.
  business-os left uncommitted — standing default, not re-decided here.
