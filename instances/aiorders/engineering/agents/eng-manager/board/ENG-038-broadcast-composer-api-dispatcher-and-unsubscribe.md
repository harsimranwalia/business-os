---
id: ENG-038
title: Broadcast composer API, dispatch poller, and unsubscribe function
project: aiorders-api
type: feature
size: L
time_estimate: ~2-3 days
time_spent: ~1 day (backend build) + review round 1 (~3h) + SMS-copy fix (~20min) + review round 2 (~1.5h) + round-2 fixes (~1h) + review round 3 (~2h) + round-3 fixes (~1.5h) + review round 4 (~1.5h) + round-4 fixes (~1h) + review round 5 (~1.5h) + security gate round 1 (~2h) + security-fix round 1 (~1.5h) + review round 6 (~1.5h) + security gate round 2 (~1h) + release-readiness round 1 (~45min, returned — missing migration gate) + migration gate (~45min, pass — receipt written, rollback tested against a disposable replica) + release-readiness round 2 (~45min, pass — PR opened) + merge detection + acceptance-check (pass)
time_remaining: none — verified
severity: P2
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-04
updated: 2026-09-05
branch: feat/ENG-038-broadcast-composer-dispatcher-unsubscribe
depends_on: [ENG-037]
blocks: [ENG-039]
parent: ENG-019
links:
  prd: agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md
  design: agents/architect/designs/ENG-019-restaurant-marketing-broadcasts.md
  adrs: [ADR-018, ADR-019, ADR-020]
  review: agents/principal-engineer/reviews/ENG-038.md
  test_plan: agents/qa/test-plans/ENG-038.md
  security_review: agents/security/reviews/ENG-038.md
  release: agents/devops/releases/2026-09-05-aiorders-api-ENG-038.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/16
---

## Problem

Owners have no API to compose, edit, pause, or cancel a broadcast campaign;
nothing dispatches a scheduled or drip send once one exists; and no path
lets a recipient opt out of future campaign sends. `ENG-037`'s tables exist
but nothing reads or writes them yet.

## Outcome

**`brand-portal/broadcasts.ts`** — `handleBroadcasts(action, payload,
supabase, user)`, gated by `requireRestaurantAccess(restaurant_id, ...)` on
every action (`ADR-011`'s precedent, reconfirmed against `offers.ts`/
`catering.ts`), `{success, error}` response shape, never a thrown 500 for an
expected condition:

- `list_broadcasts` — paginated (pagination is not optional — engineering-
  standards' automatic review failure #5).
- `get_broadcast` — full campaign + step list.
- `create_broadcast` — validates: at least one step, at least one channel
  per step, `offer_id` (if given) belongs to this restaurant, `inactive_days`
  is a positive integer when that audience mode is chosen. `send_at`
  omitted/past = due immediately (unified-dispatch decision, `ENG-037`'s own
  row shape).
- `update_broadcast` — rejected once `status` is `active` or later:
  `{success: false, error: 'Cannot edit a campaign that has started sending'}`.
- `pause_broadcast` / `resume_broadcast` — flips `active`/`paused`; the
  dispatcher's claim query filters on campaign status.
- `cancel_broadcast` — terminal; marks every remaining `pending` recipient
  row `cancelled`. Already-sent rows untouched.
- `get_broadcast_report` — counts by status/channel; when `offer_id` is set,
  redemption count + revenue per `ADR-019`'s query against `orders.promos`
  (use `ENG-037`'s confirmed key shape — don't re-derive it here); email
  open/click counts from `communication_log` when present.

**`brand-portal/index.ts`** — routes `broadcasts_*` actions to the new
handler, same shape as the existing `offers`/`catering` lines.

**`broadcast-dispatch/index.ts`** — service-role-bearer-gated (matches
`ADR-016`/`ADR-017`; local `auth.ts` in this function's own directory, not
`_shared/` — this is only the second consumer, `ADR-017`'s "third consumer"
extraction bar isn't crossed). Per tick: (1) promote due campaigns
(`scheduled` → `active` where `scheduled_send_at <= now()`), resolve each
one's audience (consent-filtered) and bulk-insert recipient rows; (2) claim
up to 200 due rows atomically (not a plain `SELECT` then `UPDATE` —
idempotency under an overlapping tick is load-bearing per the design's own
Risks, not a nice-to-have), **re-check consent at claim time** (not the
enrollment-time snapshot — a customer may unsubscribe between drip steps),
call `outgoing-communications` (`broadcast_message`, `systemTriggered:
true`, service-role bearer), write the resulting status. One recipient's
failure never aborts the batch — isolated per-item try/catch, matching
`sendCampaignCreatedNotification`'s existing `Promise.all` pattern.

**`broadcast-unsubscribe/index.ts`** — public, unauthenticated, `GET,
OPTIONS` only. Token is an opaque, non-enumerable HMAC-signed customer_id.
Response table from the design:

| Condition | Response |
|---|---|
| Token missing/invalid/expired | 400, plain-text "This link is no longer valid." |
| Token valid, already unsubscribed | 200, same confirmation copy (idempotent) |
| Token valid | 200, flips the matching consent field, confirmation page |

**`outgoing-communications/actors/consumers.ts`** — new `broadcast_message`
case alongside `welcome_offer`/`every_order`/`first_order`: sends the step's
pre-composed subject/body (`replaceTemplateVariables`'s existing
`{{customer_name}}`, reused not rebuilt), appends the unsubscribe link,
writes `communication_log` with `reference_type: 'broadcast_campaign'`,
`reference_id: campaign.id`.

**Tests:** `broadcasts.test.ts` (access-denied, cross-tenant audience leak,
empty-audience no-op, malformed step delay, edit-after-active rejected).
`dispatch.test.ts` (claim idempotency under a simulated overlapping tick,
opted-out-between-enrollment-and-send exclusion, partial-batch-failure
isolation).

**`supabase/functions/README.md`** — `brand-portal` DB-tables list gains the
three new tables; two new function sections (`broadcast-dispatch`,
`broadcast-unsubscribe`) in the house format.

## Notes

Cross-tenant scoping is named explicitly in the design's Risks because this
codebase has a confirmed history of exactly this bug class (`ENG-015`,
`ENG-022`) — every action here needs both `requireRestaurantAccess` *and* a
`restaurant_id` filter on every query (defense in depth, `ADR-006`'s
pattern), read `ENG-015`'s review before writing the audience-query code.
The dispatcher path carries no caller-supplied `restaurant_id` at all (each
recipient row already carries its own), so there's no cross-tenant vector to
guard there specifically — don't add a check that doesn't apply.

Don't re-verify `orders.promos`'/`communication_log`'s shape from scratch —
`ENG-037` already did that and the finding lives on its own board file/log;
read it fresh before writing `get_broadcast_report` and the dispatcher's
log-write, per step 6b.

Serves AC1–AC7 (all seven — every criterion in the PRD is backend-enforced;
`ENG-039` only surfaces what this ticket returns). Full surface-split,
ADR-mapping and sizing reasoning:
`agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`.

## Log

- `2026-09-04` `(created) → ready` (eng-manager, `work-breakdown`, `continue
  ENG-019` event pass) — sub-ticket of `ENG-019`, sequence 2 of 3,
  `depends_on: [ENG-037]` unmet (not yet `shipped`), so held at `ready`
  rather than dispatched. `time_estimate` ~2-3 days. Owner `eng-manager`
  while waiting, per the state table's documented owner for `ready`
  generally — reassigned to `backend` once `ENG-037` ships and this ticket
  actually starts. `chained: none` — waiting on an unmet `depends_on:
  [ENG-037]`, nothing agent-actionable on this ticket yet; the merge-
  detection/dispatch step that advances `ENG-037` will pick this ticket up
  on its own once it ships.

- `2026-09-04` no state change (eng-manager, `scheduled` event pass —
  whole-board sweep, step 5 merge detection). This is exactly the re-check
  the entry above named as this pass's job. `ENG-037`'s `aiorders-api` PR
  #15 confirmed merged this same pass via local git ancestry, cross-checked
  with `gh pr view` (see `ENG-037`'s own board-file log) —
  `depends_on: [ENG-037]` is now satisfied.

  **Not transitioned to `building` in this pass.** Same precedent this
  board already set explicitly on `ENG-032`/`ENG-024`/`ENG-022` (a
  whole-board sweep does not perform new implementation work itself): the
  next hop is a real code edit against `aiorders-api` (the broadcasts
  handler, dispatch poller, unsubscribe function) and belongs in its own
  dedicated session per `eng_build_loop.md`'s "each heavy step gets its own
  session with fresh context," not this sweep.

  Confirmed this is the correct next pick: `ENG-039` (`depends_on:
  [ENG-038]`) remains blocked on this ticket specifically — no other member
  of the family is dispatchable yet, so there is no ordering choice to
  make. Machine WIP unaffected — this ticket was already inside the
  counted `ready..ready-to-ship` range as part of `ENG-019`'s family slot;
  moving it to `building` swaps which member is active, not how many.

  **0 transitions.** `chained: ENG-038` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-038` before this pass exits, so a dedicated session performs
  `ready → building` (transition and implementation together, the same
  shape every other building hop on this board has used).

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.

- `2026-09-04` `ready → building` (backend, `continue ENG-038` event pass) —
  built the full backend surface: `brand-portal/broadcasts.ts` (8 actions),
  `broadcast-dispatch` (new function, atomic per-recipient claim), `broadcast-
  unsubscribe` (new function), `outgoing-communications`'s new
  `broadcast_message` action, and a new migration (`broadcast_campaign_
  recipients` gains a `claimed` status — ENG-037's schema deliberately left
  this to this ticket). Self-tested: `deno test --no-check` 6/6 + 4/4, no
  regression on `offers.test.ts` (9/9); claim-idempotency and cross-tenant
  tests mutation-verified. Branch pushed:
  `feat/ENG-038-broadcast-composer-dispatcher-unsubscribe` (`aiorders-
  api@c1d55df`). PR body drafted. Full reasoning (access-check synthesis, the
  schema addition, a pre-existing SMS bug found+corrected+proposed
  separately, live-schema verification): `agents/backend/notebook/2026-09-04-
  eng038-build.md`. WIP unaffected (still `ENG-019`'s own slot). Needs a
  manual `BROADCAST_UNSUBSCRIBE_SECRET` env var before real sends.
  Step 6b's grep also surfaced `ENG-037`'s own review naming two findings
  (missing index, missing check constraint) as safe to land here — folded
  into the same migration, second commit `4f0dccf`, pushed.
  **Not carried further this pass** — review/quality is its own session per
  `eng_build_loop.md`. `chained: ENG-038` — fired `continue ENG-038` before
  this pass exits.

- `2026-09-04` **review round 1: FAIL** (principal-engineer, combined
  review+quality hop, `continue ENG-038` event pass, per prior pass's own
  `chained: ENG-038`). Reading map for `continue`: steps 6 and 6b (design
  already complete, not mid-PRD), plus the not-negotiable set (1, 7, 8b, 9,
  10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check
  clean (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh ENG-038`: exit 0, clean.
  Worktree re-checked fresh (not trusted from the trigger's checkpoint):
  `feat/ENG-038-broadcast-composer-dispatcher-unsubscribe@4f0dccf`, 14
  files, 1946/7 vs `origin/main`. 0/10 automatic failures.

  **Blocking:** `outgoing-communications/actors/consumers.ts`'s new
  `sendBroadcastMessage` puts "Reply STOP or visit {link} to unsubscribe."
  in every campaign SMS — but `ADR-020`'s own Alternatives table explicitly
  rejected STOP-reply opt-out for this exact ticket ("no inbound-message
  path exists at all in this codebase... The same link... covers SMS the
  same way it covers email"), and confirmed still true this round:
  `services/sms.ts` is still mock-only, no inbound path of any kind. A
  customer who replies STOP today is not unsubscribed by anything in this
  codebase — a customer-facing promise the system can't keep, on a feature
  the PRD's own Risks section already flags for CASL exposure. The link
  itself is correctly implemented; only the extra "Reply STOP or " text is
  wrong. Fix: delete that phrase, keep the link-only sentence `ADR-020`
  actually specified. Two non-blocking findings (a logging gap in
  `_shared/broadcastUnsubscribe.ts`'s catch-all when the not-yet-configured
  `BROADCAST_UNSUBSCRIBE_SECRET` is missing; `dispatch.ts`'s
  `enrollAudience` has no failure path if the recipient-insert itself
  errors, leaving a campaign stuck `active` with 0 recipients) and two QA
  coverage gaps (pause/resume/cancel untested — matches what this ticket's
  own Tests section scoped, not a new gap; `promoteDueCampaigns`/
  `enrollAudience` untested anywhere). Independently re-ran both test
  suites fresh (not trusted from the build hop's report): `broadcasts.test.ts`
  6/6, `dispatch.test.ts` 4/4, `offers.test.ts` 9/9 no regression — matches
  exactly. Mutation-tested the claim-idempotency test myself (removed
  `claimRecipients`'s `.eq('status','pending')` guard, confirmed it fails
  for the right reason, restored) since it's this ticket's single
  highest-stakes correctness property. Full trace, live-schema
  cross-checks, and every finding in full: `agents/principal-engineer/
  notebook/2026-09-04-review-log.md`.

  No receipt written, `links.review` untouched. QA's hop result this round
  (coverage gaps, independent test re-run, mutation test) discarded with
  it, per `code-review-gate/SKILL.md` step 9 — the code is about to change;
  no `agents/qa/test-plans/ENG-038.md` written. **0 net transitions** —
  `state`/`owner` unchanged (`building`/`backend`), same precedent
  `ENG-033`'s own round-1 fail set. WIP/approval caps unaffected.
  `time_spent`/`time_remaining` updated in frontmatter.

  Dead-end sweep: no other ticket touched. Notify sweep: nothing to raise
  or nudge — a review fail isn't approver-facing, and no open inbox item
  crossed a threshold this pass. Step 8b: one proposal filed
  (`proposals.md`) — the untracked `deno.lock` files in all three new
  function directories this round, a recurrence of the same pattern
  `ENG-029`/`ENG-031`/`ENG-037` already noticed independently with zero
  action taken; no `exception-request:` found. Step 8c: n/a, no gate
  answered this pass.

  `chained: ENG-038` — `building` is agent-owned (round 1's one blocking
  finding is the next hop's own work), not the approver, not blocked, not
  terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-038` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh ENG-038` and whole-board:
  see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` `building → in-review` (backend, `continue ENG-038` event
  pass, per prior pass's own `chained: ENG-038`) — the one blocking finding
  from review round 1, and nothing else: reading map for `continue` (design
  already complete, not mid-PRD): steps 6 and 6b, plus the not-negotiable
  set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*;
  *Guards*). Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
  `eng-gate-check.sh ENG-038`: exit 0, clean. Worktree re-checked fresh (not
  trusted from the trigger's checkpoint): `feat/ENG-038-broadcast-composer-
  dispatcher-unsubscribe@4f0dccf`, matching the reviewed commit exactly.

  **Fix:** `outgoing-communications/actors/consumers.ts`'s `sendBroadcastMessage`
  — deleted `"Reply STOP or "` from the SMS unsubscribe sentence, leaving
  `` `${body} Visit ${unsubscribeUrl} to unsubscribe.` ``, mirroring the email
  path's own `\n\nUnsubscribe: ${url}` treatment. Confirmed against both
  named sources before editing, not just the reviewer's say-so: `ADR-020`'s
  Alternatives table ("no inbound-message path exists at all... the same
  link... covers SMS the same way it covers email") and the design's own
  Non-goals ("SMS opt-out via inbound `STOP` reply parsing — link-based for
  both channels instead"). Step 6b: `grep -rn "STOP" supabase/functions/`
  across the whole `aiorders-api` functions tree returns exactly the one hit
  that was just fixed — no second call site, no test asserting the old copy,
  nothing in the PRD or design specifying literal SMS text that would now
  disagree with the code. One-line diff, nothing else touched.

  Self-tested: re-ran all three suites review round 1 ran, fresh — `deno
  test --no-check`: `broadcasts.test.ts` 6/6, `dispatch.test.ts` 4/4,
  `offers.test.ts` 9/9, no regression, matches exactly. None of the three
  exercises `consumers.ts`'s SMS branch directly (no test file exists under
  `outgoing-communications/`, unchanged by this fix), so the gate that
  actually re-checks this line is review round 2, next. Committed
  (`ede0e1e`, "Remove STOP-reply claim from broadcast SMS unsubscribe text")
  and pushed to `origin/feat/ENG-038-broadcast-composer-dispatcher-
  unsubscribe`. The three untracked `deno.lock` files noted last round are
  untouched and still deliberately unstaged — already filed, no new
  occurrence this round, nothing to re-propose.

  `building`'s exit condition (branch pushed, self-tested, PR body written)
  is met again — the PR body drafted at initial build time
  (`agents/backend/notebook/2026-09-04-eng038-build.md`) describes the
  feature, not this line, and needs no revision. **1 transition** —
  `building → in-review`, owner `backend → principal-engineer` per
  `definition-of-done.md`'s state table. `links.review` still unset — round
  1 failed with no receipt per `code-review-gate/SKILL.md` step 8, and
  round 2 hasn't run yet. `time_spent`/`time_remaining` updated in
  frontmatter (fix took ~20 min; remaining estimate unchanged in substance,
  just drops the now-done SMS-copy item from its own parenthetical).

  Dead-end sweep: no other ticket touched. Notify sweep: nothing to raise
  or nudge — no gate item written this pass, nothing crossed the 24h mark.
  Step 8b: nothing new to observe or propose beyond what's already on
  `proposals.md`/`observations.md` from round 1. Step 8c: n/a, no gate
  answered this pass.

  `chained: ENG-038` — `in-review` is agent-owned (principal-engineer's
  round 2), not the approver, not blocked, not terminal, not held by a cap.
  Fired `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/
  departments/engineering/lib/eng-trigger.sh continue ENG-038` before this
  pass exits. Post-pass `eng-gate-check.sh ENG-038`: exit 0, clean.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` **review round 2: FAIL** (principal-engineer, combined
  review+quality hop, `continue ENG-038` event pass, per prior pass's own
  `chained: ENG-038`). Reading map for `continue`: steps 6 and 6b (design
  already complete, not mid-PRD), plus the not-negotiable set (1, 7, 8b, 9,
  10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check
  clean (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh ENG-038`: exit 0, clean.
  Worktree re-checked fresh (not trusted from the trigger's checkpoint):
  `feat/ENG-038-broadcast-composer-dispatcher-unsubscribe@ede0e1e`, matching
  the checkpoint exactly. `git log HEAD..origin/main` and `git diff
  HEAD...origin/main --stat` both empty — no drift since round 1. `git diff
  origin/main...HEAD --stat`: still 14 files, 1946/7. `git show --stat
  ede0e1e`: confirms the only change since round 1 is exactly the one file,
  one line the prior pass's own log claims.

  **Automatic-failure scan: 1/10**, re-run fresh against the full current
  diff rather than carried forward from round 1's own 0/10. **Blocking:
  automatic failure #3, "missing test on a bug fix."** `ede0e1e` is a fix
  for round 1's own blocking finding (the SMS "Reply STOP" claim) — read
  directly, the corrected line is right, matches the email path's
  treatment. But it ships with no regression test: `sendBroadcastMessage`
  isn't exported, `outgoing-communications/` has zero test files of any
  kind, and nothing anywhere asserts the corrected copy or would fail
  against the old buggy line. Same shape as this board's own `ENG-033`
  round 2 (a round-1-caught defect, fixed without a test, failed again at
  round 2 for exactly that), which also already closed off "no test infra
  here" as an excuse — re-confirmed empirically this round: no directory in
  this repo has its own `deno.json`, including every one that already has
  passing tests, so a test file under `outgoing-communications/` needs no
  new scaffolding. **Specific fix:** extract the SMS (and, for symmetry,
  email) body construction into a small pure exported function and add
  `consumers.test.ts` (first for this directory) asserting the output
  excludes `STOP`/`Reply` and contains the exact `Visit {url} to
  unsubscribe.` sentence — mutation-verified (revert the line, confirm only
  that assertion fails, restore) per the standards' own rule. Two
  non-blocking findings (F1 logging gap, F2 `enrollAudience` no-rollback)
  carried forward unchanged from round 1 — confirmed via `git show --stat`
  that neither touched file changed this round.

  Independently re-ran all three suites fresh: `broadcasts.test.ts` 6/6,
  `dispatch.test.ts` 4/4, `offers.test.ts` 9/9 — matches exactly, no
  regression. **QA side of this combined hop, discarded with the rest of
  this round:** read `dispatch.test.ts` directly (not trusted from round
  1's own account) — its four tests cover only the claim/resolve half of
  the dispatcher; `promoteDueCampaigns` and `enrollAudience` (the
  promotion/audience-resolution logic implementing AC1's schedule/immediate
  distinction, AC2's per-step drip fan-out, and AC3's audience-mode choice)
  have zero coverage anywhere. Named sharply this round, not softened — a
  real quality-gate risk for the next round covering three of seven
  acceptance criteria, not a nice-to-have. Full trace, precedent citation,
  and both fully-specified fixes:
  `agents/principal-engineer/notebook/2026-09-04-review-log.md`.

  No receipt written, `links.review` untouched. QA's own result this round
  (the coverage-gap finding, the independent test re-run) discarded with it,
  per `code-review-gate/SKILL.md` step 9 — the code is changing again; no
  `agents/qa/test-plans/ENG-038.md` written. **1 transition** —
  `in-review → building`, owner `principal-engineer → backend`. This is the
  ticket's second consecutive failed review round (round 1 fail, round 2
  fail) — not yet the third-round escalation to `blocked`/architect, but
  worth naming plainly so a third round doesn't need to recount it.
  `time_spent`/`time_remaining` updated in frontmatter (review round 2 took
  ~1.5h; remaining estimate now names both fixes explicitly rather than
  carrying the old "review round 2, QA, security, release-readiness" band
  forward unchanged).

  Dead-end sweep: no other ticket touched. Notify sweep: nothing to raise —
  a review fail isn't approver-facing. Checked all three open `inbox/`
  items for the 24h-nudge condition regardless: `ENG-027`/`ENG-028`'s G1s
  already carry a `nudged:` stamp (one nudge, ever — nothing more owed);
  `ENG-016`'s Piece-2 question (`notified: 2026-09-04T10:58:06`) is ~6h old
  against a current time of `2026-09-04T17:04:17`, well under the 24h
  threshold — nothing nudged this pass. Step 8b: one observation filed
  (`observations.md`) — the immediately prior pass (the SMS-copy fix hop,
  `building → in-review`) does not appear to have appended its own dated
  entry to `board/_index.md`, unlike every other pass on this ticket; not
  re-derived or fixed retroactively, just flagged. No `exception-request:`
  found. Step 8c: n/a, no gate answered this pass.

  `chained: ENG-038` — `building` is agent-owned (both fixes are the next
  hop's own work), not the approver, not blocked, not terminal, not held by
  a cap. Fired `/bin/zsh /Users/hwalia/Documents/projects/personal/
  business-os/departments/engineering/lib/eng-trigger.sh continue ENG-038`
  before this pass exits. Post-pass `eng-gate-check.sh ENG-038` and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` `building → in-review` (backend, `continue ENG-038` event pass,
  per prior pass's `chained: ENG-038`) — closed both items round 2 fully
  specified: extracted `buildBroadcastSmsBody`/`buildBroadcastEmailBody`
  (pure, exported) + new `consumers.test.ts`, mutation-verified; added 6
  tests for `promoteDueCampaigns`/`enrollAudience` in `dispatch.test.ts` on a
  new fake, 2 mutation-verified. Full regression 27/27 (10+6+9+2), no
  regression. Commits `d9c98ff`/`87f3f8c`, pushed. `building`'s exit
  condition met (pushed, self-tested, PR body unchanged/still accurate). No
  gate ran — no receipt, `links.review` untouched. **1 transition** — owner
  `backend → principal-engineer`. WIP/caps unaffected; `time_spent`/
  `time_remaining` updated. Dead-end/notify/8b/8c: nothing to report. Full
  reasoning + both mutation traces: `agents/backend/notebook/2026-09-04-
  eng038-review2-fixes.md`.

  `chained: ENG-038` — agent-owned (principal-engineer's round 3), not
  approver/blocked/terminal/capped. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/
  engineering/lib/eng-trigger.sh continue ENG-038` before exit.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **review round 3: REVIEW pass, QUALITY fail** (principal-engineer,
  combined review+quality hop, `continue ENG-038` event pass, per prior
  pass's `chained: ENG-038`). Reading map for `continue`: steps 6 and 6b,
  plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*;
  *The four lanes*; *Guards*). Mode check clean (`MODE=active`). Pre-pass
  `eng-gate-check.sh ENG-038`: exit 0, clean. Worktree re-checked fresh:
  `@87f3f8c`, matching the checkpoint exactly; no drift vs `origin/main`.
  `git diff origin/main...HEAD --stat`: 15 files, 2237/7 (round 2 was 14
  files, 1946/7 — `consumers.test.ts` is new).

  **Automatic-failure scan: 0/10**, re-run fresh. Round 2's blocking finding
  (missing test on the SMS-copy bug fix) is closed: `buildBroadcastSmsBody`/
  `buildBroadcastEmailBody` extracted as pure exported functions,
  `consumers.test.ts` covers the corrected copy. Independently re-ran the
  full suite fresh: 27/27 (6+9+10+2), matches the backend's own report.
  Independently mutation-tested two properties the fix hop's own trace
  hadn't already covered (the SMS-copy regression and, most notably, the
  consent-inclusion default — flipping it from default-contactable to
  default-excluded failed exactly the one test built to catch it). Both
  restored clean. **Verdict: PASS on code review.** Full writeup:
  `agents/principal-engineer/reviews/ENG-038.md`, `links.review` set.

  **Quality gate — its first real verdict on this ticket (rounds 1–2 both
  failed at review first, discarding QA's result both times) — FAIL.**
  Went looking at `getBroadcastReport` and `broadcast-unsubscribe/index.ts`
  for the first time this round; neither appears in either prior round's
  own coverage notes. Found three gaps, all pre-existing since the original
  build (not introduced by anything in rounds 2–3): **(1)** AC4 — the
  redemption/revenue matching in `getBroadcastReport` (`broadcasts.ts:
  560-603`) has zero test of its actual logic, only the no-offer-attached
  null case is covered. **(2)** AC5 (read half) — the same function's
  delivery-by-channel aggregation (`541-552`) is likewise only exercised
  via its empty-array branch. **(3)** AC6, the highest-stakes of the
  three — the unsubscribe token sign/verify pair and the
  `broadcast-unsubscribe` handler have no test anywhere; this is a public,
  unauthenticated, consent-mutating endpoint on a CASL-flagged feature.
  Full findings, exact fix specs, and the acceptance-coverage table:
  `agents/qa/test-plans/ENG-038.md`, `links.test_plan` set. No bugs filed —
  each gap is a coverage miss, not a confirmed wrong answer.

  **Standards promotion.** The "extract inline/private logic into a pure
  exported function for testability" remedy has now been written a third
  time on this board (`ENG-033`'s `deriveActionStatus`; this ticket's own
  round-2→3 SMS/email extraction; this round's three new findings). Per
  `code-review-gate/SKILL.md` step 10, added a rule to
  `agents/eng-manager/config/engineering-standards.md` (`## Naming and
  structure`) rather than treating a fourth occurrence as ticket-specific
  again. Telling the EM here, in the board's own audit trail, since no
  separate approval or channel is specified for this step.

  Per `code-review-gate/SKILL.md` step 9 and the `ENG-033` round-3 precedent
  (review pass + quality fail → `building` on the quality finding; review's
  own pass stands, re-confirmed rather than re-litigated next round): **1
  transition** — `in-review → building`, owner `principal-engineer →
  backend`. WIP/approval caps unaffected. `time_spent`/`time_remaining`
  updated in frontmatter — three fixes now fully specified (no fourth
  review round should be needed for any of them). Full reasoning, every
  independent verification, and both mutation traces:
  `agents/principal-engineer/notebook/2026-09-04-review-log.md`.

  Dead-end sweep: no other ticket touched this pass. Notify sweep: nothing
  to raise — a quality-gate fail isn't approver-facing; no open `inbox/`
  item crossed the 24h-nudge threshold this pass (checked all three:
  `ENG-027`/`ENG-028` already nudged once, `ENG-016`'s Piece-2 item still
  under 24h). Step 8b: no new observation or proposal beyond the standards
  promotion above (which is a direct edit, not a proposal — no gate needed
  per that skill step); no `exception-request:` found. Step 8c: n/a, no
  gate answered this pass.

  `chained: ENG-038` — `building` is agent-owned (the three fixes are the
  next hop's own work), not the approver, not blocked, not terminal, not
  held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/projects/personal/
  business-os/departments/engineering/lib/eng-trigger.sh continue ENG-038`
  before this pass exits. Post-pass `eng-gate-check.sh ENG-038` and
  whole-board: see board index.

  business-os left uncommitted — standing default, convention still open
  (this pass also touched the department-shared `engineering-standards.md`
  for the promotion above; same standing default applies to it).

- `2026-09-04` **round-3 fixes: all three quality-gate gaps closed**
  (backend, `continue ENG-038` event pass, per prior pass's `chained:
  ENG-038`). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*). Mode check clean (`MODE=active`). Pre-pass
  `eng-gate-check.sh ENG-038`: exit 0, clean. Worktree re-checked fresh:
  `@87f3f8c`, matching the checkpoint exactly; no drift vs `origin/main`.

  Fixed all three gaps QA's round-3 quality-gate report specified
  (`agents/qa/test-plans/ENG-038.md`): **(1)** extracted
  `getBroadcastReport`'s coupon-redemption/revenue matching into
  `computeRedemptions`, **(2)** its delivery-by-channel aggregation into
  `buildDeliveryByChannel`, both in `brand-portal/broadcasts.ts`, with 8 new
  tests between them; **(3)** added `_shared/broadcastUnsubscribe.test.ts`
  covering `signUnsubscribeToken`/`verifyUnsubscribeToken` directly (round
  trip, malformed token, tampered signature, missing-secret throw/swallow),
  and extracted `broadcast-unsubscribe/index.ts`'s response-decision logic
  into a new `unsubscribe.ts` (`decideUnsubscribePreCheck`,
  `decideUnsubscribeWriteResult`) with 6 more tests — same
  serve()-stays-thin shape `broadcast-dispatch/dispatch.ts` already uses, so
  no test ever imports `index.ts` and starts a server. Also closed F1
  (non-blocking since round 1) in the same pass, per QA's own note that it
  was cheap to do so here: `verifyUnsubscribeToken`'s catch-all now logs the
  underlying error instead of swallowing it silently — no caller-visible
  behaviour change.

  Full regression, run fresh per directory: `brand-portal/` (whole
  directory) 38/38, `broadcast-dispatch/` 10/10,
  `outgoing-communications/actors/consumers.test.ts` 2/2,
  `broadcast-unsubscribe/` 6/6, `_shared/broadcastUnsubscribe.test.ts`
  (needs `--allow-env`, the only file in this repo that touches `Deno.env`)
  7/7 — ENG-038-relevant total 48/48 (27 pre-existing + 21 new), no
  regression anywhere. **Mutation-verified the two highest-stakes
  properties across this hop** (proportional to round 1–3's own practice,
  not every branch): the coupon-matching predicate (money; flipping `===`
  to `!==` failed exactly the three matching-dependent tests) and the
  token-signature check (QA's own words, "the highest-stakes of the three
  gaps"; bypassing `crypto.subtle.verify`'s result failed exactly the
  tampered-signature test). Both restored via backup, re-ran clean. Full
  reasoning: `agents/backend/notebook/2026-09-04-eng038-review3-fixes.md`.

  **Step 6b.** Grepped `suite_command` (this ticket's own field is the only
  one it touches) before editing: `_shared/`'s new test file needs
  `--allow-env` to exercise the missing-secret case — Deno gates env reads
  and writes under one permission with no per-test escalation above the CLI
  grant, confirmed empirically. Updated only that field in
  `agents/qa/test-plans/ENG-038.md`'s frontmatter (not `last_run`/
  `last_result`, which stay QA's own to set), matching this repo's own
  per-ticket precedent for command peculiarities (ENG-008/010/011/013 each
  recorded their own ad hoc permission flag the same way). Also grepped
  `broadcast-unsubscribe`/`verifyUnsubscribeToken`/`signUnsubscribeToken`/
  `getBroadcastReport`: hits in the architect's design doc, ADR-020, and
  `supabase/functions/README.md` all describe endpoint *behaviour*
  (routes, response shapes), unchanged by an internal-only extraction —
  `location` classification, no edit needed.

  Three commits, one per gap (Gap 3 split into its own (a)/(b) the way QA's
  own report split it): `af3da30` (redemption/revenue +
  delivery-by-channel), `8be42ec` (unsubscribe token tests + F1),
  `d13722a` (unsubscribe handler decision extraction). All pushed to
  `origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe` — 18
  files, 2472/7 vs `origin/main` (round 3 was 15 files, 2237/7).

  Per `code-review-gate/SKILL.md`'s normal build-hop exit and this ticket's
  own round-2 precedent: **1 transition** — `building → in-review`, owner
  `backend → principal-engineer`. WIP/approval caps unaffected.
  `time_spent`/`time_remaining` updated in frontmatter.

  Dead-end sweep: no other ticket touched this pass. Notify sweep: nothing
  to raise — no gate item written this pass, and no open `inbox/` item
  crossed the 24h-nudge threshold (same three checked last pass, none newly
  eligible: `ENG-027`/`ENG-028` already nudged once, `ENG-016`'s Piece-2
  item still under 24h). Step 8b: no new observation or proposal — nothing
  noticed outside this ticket's own scope this pass; no `exception-request:`
  found. Step 8c: n/a, no gate answered this pass.

  `chained: ENG-038` — `in-review` is agent-owned (review round 4 is the
  next hop's own work), not the approver, not blocked, not terminal, not
  held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/projects/personal/
  business-os/departments/engineering/lib/eng-trigger.sh continue ENG-038`
  before this pass exits. Post-pass `eng-gate-check.sh ENG-038` and
  whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **round 4: REVIEW pass, QUALITY fail — one gap remains, Gap
  4 (AC5 write half)** (principal-engineer, `continue ENG-038` event pass,
  per prior pass's `chained: ENG-038`). Reading map for `continue`: steps 6
  and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*; *The four lanes*; *Guards*). Mode check clean
  (`MODE=active`). Pre-pass `eng-gate-check.sh ENG-038`: exit 0, clean.
  Worktree re-checked fresh: fetched `origin main
  feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`; HEAD `d13722a`,
  matching the checkpoint exactly; `git log HEAD..origin/main` / `git diff
  HEAD...origin/main --stat` both empty, no drift.

  Ran the combined review+quality hop, scoped to the diff since round 3's
  reviewed commit (`87f3f8c..d13722a`, 7 files, 282/47 — the three
  round-3-fix commits) per `code-review-gate/SKILL.md` step 9: round 3's
  own review pass on the base diff stands, not re-litigated.

  **Code review: PASS, 0/10 automatic failures**, second consecutive pass.
  Traced `broadcast-unsubscribe/index.ts`'s new control flow against the
  pre-round-4 version line by line (not just diff hunks) and confirmed the
  `unsubscribe.ts` extraction is behaviour-preserving: same four response
  outcomes, same status codes; the `resolvedCustomerId as string` cast is
  safe since the pre-check only returns `null` when `customerId` was
  already truthy. `brand-portal/broadcasts.ts`'s two extractions
  (`computeRedemptions`, `buildDeliveryByChannel`) are byte-for-byte
  copy-moves. F1 is now closed outright (logs the underlying error) rather
  than merely carried forward. Independently re-ran the full regression
  fresh, per directory: `brand-portal/` (whole dir) 38/38,
  `broadcast-dispatch/` 10/10, `outgoing-communications/actors/
  consumers.test.ts` 2/2, `broadcast-unsubscribe/` 6/6, `_shared/
  broadcastUnsubscribe.test.ts` (`--allow-env`) 7/7 — matches the backend's
  own report exactly; reconciled its "48/48 (27 pre-existing + 21 new)" by
  counting `Deno.test` blocks per file rather than trusting the sum (checks
  out). **Two mutation tests on this round's one genuinely new decision
  shape** (`decideUnsubscribePreCheck` — round 3 already mutation-verified
  the coupon-matching and signature-check logic *before* extraction, so
  re-mutating the relocated code would be repetition): the idempotency
  check (`=== false` → `!== false`) failed exactly the 2 dependent tests;
  the missing-customer-id gate (`!input.customerId` → `input.customerId`)
  failed exactly the 3 dependent tests, including the one wired to a
  request with no verified token reaching the write path. Both restored via
  backup, `git diff --stat` empty, re-ran clean. Also ran `deno check` on
  every file this round's diff touches (extra due diligence, not this
  project's own `--no-check` `suite_command` — no `deno.json` exists yet,
  a standing gap in `projects.md`, not this ticket's to fix): the
  unsubscribe/shared files check clean; `brand-portal/broadcasts.ts`
  surfaces 9 pre-existing errors, all in code this round doesn't touch —
  not filed (fixing it here would itself be automatic-failure #7).
  `links.review` re-set to `agents/principal-engineer/reviews/ENG-038.md`
  (round 4).

  **Quality gate: FAIL, second consecutive fail.** Gaps 1–3 (AC4,
  AC5-read, AC6) closed and independently confirmed via the same
  regression run and mutation tests above. **One gap remains, and it isn't
  new:** round 3's own test-plan already named it, in the "Not automated"
  section under AC5 (write) — `sendBroadcastMessage`
  (`outgoing-communications/actors/consumers.ts:881-1020`)'s own
  `communication_log` insert has zero test coverage anywhere. Round 3
  deliberately left it unnumbered "because the read half (Gap 2) already
  fails the gate for this AC" — a reporting-efficiency call, not a
  substantive judgement that the write path is safe untested (unlike AC3's
  restaurant-scoping note in the same section, which rests on an actual
  design reasoning about there being no caller-supplied cross-tenant
  vector, and stays non-blocking, unchanged, this round). The round-3 fix
  hop closed the three *numbered* gaps and didn't pick up the
  parenthetical. Confirmed by grep this is still genuinely untested:
  `dispatch.ts` exports an unrelated function of the same name (the
  injectable HTTP wrapper `dispatch.test.ts` fakes at the network
  boundary), so that suite's 10/10 never reaches the real handler, and
  `consumers.test.ts` covers only the two pure body-builder helpers this
  handler calls, never the handler itself. Filed as Gap 4, blocking, with a
  specific fix (extract the per-channel gate and the `communication_log`
  row shape into testable pieces, same remedy as Gaps 1–3):
  `agents/qa/test-plans/ENG-038.md`. Read the handler itself line-by-line
  looking for a confirmed defect, not just a coverage hole — found none;
  same "reads correct, never proven" status Gaps 1–3 had before their own
  tests existed.

  Filed one observation (`agents/eng-manager/observations.md`) on the
  process shape that let this ride: a gap folded into a sibling gap's
  blocking status for reporting efficiency needs its own re-check once the
  sibling closes, or it can silently disappear. Not a proposal — one
  occurrence, not a pattern across tickets yet.

  Per `code-review-gate/SKILL.md` step 9 and this ticket's own round-3
  precedent (review pass + quality fail → `building` on the quality
  finding, review's own pass stands and is not re-litigated): **1
  transition** — `in-review → building`, owner `principal-engineer →
  backend`. Not a "third failed round" escalation: that clause
  (`code-review-gate/SKILL.md` step 9) is code review's own failure count,
  and review has now passed twice running (rounds 3–4); the quality gate
  carries no equivalent three-strike rule anywhere in this department's
  docs. WIP/approval caps unaffected. `time_spent`/`time_remaining`
  updated in frontmatter.

  Dead-end sweep: no other ticket touched this pass. Notify sweep: nothing
  to raise — a quality-gate fail isn't approver-facing; checked all three
  open `inbox/` items for the 24h-nudge condition anyway (current time
  `2026-09-04T18:20:59` PDT): `ENG-027`/`ENG-028` already carry a one-time
  `nudged:` stamp, nothing more owed; `ENG-016`'s Piece-2 item
  (`notified: 2026-09-04T10:58:06`) is ~7h23m old, still well under the 24h
  threshold. Nothing nudged. Step 8b: one observation filed (above); no
  `exception-request:` found. Step 8c: n/a, no gate answered this pass.

  `chained: ENG-038` — `building` is agent-owned (the Gap 4 fix is the next
  hop's own work), not the approver, not blocked, not terminal, not held by
  a cap. Fired `/bin/zsh /Users/hwalia/Documents/projects/personal/
  business-os/departments/engineering/lib/eng-trigger.sh continue ENG-038`
  before this pass exits. Post-pass `eng-gate-check.sh ENG-038` and
  whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **round-4 fixes: Gap 4 (AC5 write half) closed** (backend,
  `continue ENG-038` event pass, per prior pass's `chained: ENG-038`).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set
  (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*).
  Mode check clean (`MODE=active`). Pre-pass `eng-gate-check.sh ENG-038`:
  exit 0, clean. Worktree re-checked fresh: `@d13722a`, matching the
  checkpoint exactly; no drift vs `origin/main`.

  Fixed the one gap QA's round-4 report specified
  (`agents/qa/test-plans/ENG-038.md`): extracted `sendBroadcastMessage`'s
  (`outgoing-communications/actors/consumers.ts`) per-channel gate into
  `decideBroadcastChannelEligibility` and its `communication_log` row shape
  into `buildBroadcastEmailLogRow`/`buildBroadcastSmsLogRow`; exported
  `sendBroadcastMessage` itself (was module-private) with a new optional
  `deps` param (`sendEmail`/`sendSMS`/`buildUnsubscribeUrl`, all defaulting
  to the real functions) — same injectable shape
  `broadcast-dispatch/dispatch.ts`'s `sendFn` already uses, so the whole
  orchestration is testable against a fake Supabase client with no network
  or `BROADCAST_UNSUBSCRIBE_SECRET` touched. 14 new tests in
  `consumers.test.ts` (2 → 16), covering exactly QA's list: email-only,
  sms-only, both, the skip path (asserts zero inserts/zero send calls), and
  one channel succeeding while the other fails (asserts `anySucceeded` and
  each row's own status independently). **Mutation-verified** the property
  QA named directly: flipping the `anySucceeded` `||` to `&&` failed exactly
  3 of 6 orchestration tests (email-only, sms-only, one-succeeds-one-fails);
  restored via backup, re-ran clean. Full reasoning:
  `agents/backend/notebook/2026-09-04-eng038-review4-fixes.md`.

  Full regression, run fresh per directory: `brand-portal/` 38/38,
  `broadcast-dispatch/` 10/10, `outgoing-communications/actors/
  consumers.test.ts` 16/16, `broadcast-unsubscribe/` 6/6, `_shared/
  broadcastUnsubscribe.test.ts` (`--allow-env`) 7/7 — ENG-038-relevant total
  62/62 (27 pre-existing + 21 rounds 1–4 + 14 this round), no regression
  anywhere. Also ran `deno check` on both touched files: `consumers.ts`'s 8
  in-file errors are all the pre-existing repo-wide `catch (error) {
  error.message }` TS18046 pattern (untouched by this diff, same call round
  4 made on `brand-portal/utils.ts`); `consumers.test.ts` needed its
  `SupabaseClient` type import switched from `npm:@supabase/supabase-js@2`
  to the `esm.sh` URL `consumers.ts` itself already uses (the `npm:`
  specifier doesn't resolve from this directory) — zero errors after.

  **Step 6b.** Grepped `sendBroadcastMessage`/`decideBroadcastChannelEligibility`/
  `buildBroadcastEmailLogRow`/`buildBroadcastSmsLogRow`/`communication_log`:
  all hits are this ticket's own history (board log, QA plan, prior
  notebooks — `location`, not re-litigated) plus one precedent-citing
  mention in the department's `engineering-standards.md` (read-only from
  this instance regardless). Confirmed `suite_command` was **not** touched
  this round — the injectable-`deps` approach was chosen specifically so
  this hop wouldn't need to add `--allow-env` to this directory and
  contradict round 3's recorded claim that `_shared/` is the only file here
  touching `Deno.env`.

  One commit, pushed to
  `origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`:
  `125286f` — Extract sendBroadcastMessage's channel gate and
  communication_log row shape into pure, tested functions; make
  send/unsubscribe-url deps injectable (ENG-038). Branch now 19 files vs
  round 4's 18.

  Per this ticket's own round-2/round-3-fix precedent (normal build-hop
  exit, branch pushed and self-tested): **1 transition** —
  `building → in-review`, owner `backend → principal-engineer`. WIP/approval
  caps unaffected. `time_spent`/`time_remaining` updated in frontmatter.

  Dead-end sweep: no other ticket touched this pass. Notify sweep: nothing
  to raise — no gate item written this pass; checked all three open
  `inbox/` items for the 24h-nudge condition (current time
  `2026-09-04T18:45:02` PDT): `ENG-027`/`ENG-028` already nudged once,
  nothing more owed; `ENG-016`'s Piece-2 item
  (`notified: 2026-09-04T10:58:06`) is ~7h47m old, still under 24h. Nothing
  nudged. Step 8b: no new observation or proposal — nothing noticed outside
  this ticket's own scope; no `exception-request:` found. Step 8c: n/a, no
  gate answered this pass.

  `chained: ENG-038` — `in-review` is agent-owned (review round 5 is the
  next hop's own work), not the approver, not blocked, not terminal, not
  held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/projects/personal/
  business-os/departments/engineering/lib/eng-trigger.sh continue ENG-038`
  before this pass exits. Post-pass `eng-gate-check.sh ENG-038` and
  whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **review round 5: PASS / PASS — first round both halves of
  the combined gate pass together** (principal-engineer + qa, `continue
  ENG-038` event pass). Scope: diff since round 4's reviewed commit
  (`d13722a..125286f`, `consumers.ts` + its test file only). Code review
  0/10 automatic failures, extraction confirmed behaviour-preserving.
  Quality gate: Gap 4 (AC5 write half) closed, all five of QA's cover cases
  present; fresh re-check of the full acceptance table surfaced nothing
  new. Independently re-ran the full regression (77 passed/0 failed, 62
  ENG-038-relevant) and two mutation tests of my own choosing on this
  round's new logic, both caught cleanly. One new non-blocking finding
  (low severity): `sendBroadcastMessage`'s fetch-failure branches still
  untested, doesn't fail any AC. Receipts:
  `agents/principal-engineer/reviews/ENG-038.md` (round 5),
  `agents/qa/test-plans/ENG-038.md` (updated in place). Full reasoning:
  `agents/principal-engineer/notebook/2026-09-04-review-log.md`.

  Per `code-review-gate/SKILL.md` step 9: **1 transition** —
  `in-review → in-security`, owner `principal-engineer → security`.
  WIP/approval caps unaffected. `time_spent`/`time_remaining` updated.

  Dead-end sweep: no other ticket touched. Notify sweep: nothing to raise;
  checked all three open `inbox/` items for the 24h-nudge condition
  (`2026-09-04T18:54:44` PDT): `ENG-027`/`ENG-028` already nudged once;
  `ENG-016`'s Piece-2 item (`notified: 2026-09-04T10:58:06`) ~7h56m old,
  still under 24h. Nothing nudged. Step 8b: no new observation/proposal
  beyond the notebook finding above; no `exception-request:` found. Step
  8c: n/a, no gate answered this pass.

  `chained: ENG-038` — `in-security` is agent-owned (security's own gate is
  the next hop's work), not the approver, not blocked, not terminal, not
  held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/projects/personal/
  business-os/departments/engineering/lib/eng-trigger.sh continue ENG-038`
  before this pass exits. Post-pass `eng-gate-check.sh ENG-038` and
  whole-board: see board index.

- `2026-09-04` **security gate round 1: FAIL — two blocking findings, one
  critical** (`continue ENG-038` event pass). Scope: full diff
  `origin/main...HEAD` (9 commits, `c1d55df..125286f`, 18 files, worktree
  `~/Documents/projects/_eng/aiorders-api`) plus branch history
  (`git log origin/main..HEAD -p`) for secrets.

  **Finding 1 — Critical, blocking (A01 Broken Access Control / A04
  spam-relay / Restricted-data misuse).** The new `broadcast_message` action
  this ticket adds to `outgoing-communications/actors/consumers.ts`
  (`sendBroadcastMessage`) is reachable **fully unauthenticated**, because
  `outgoing-communications/index.ts` (pre-existing, untouched by this diff)
  skips its entire auth block whenever the caller's own JSON body sets
  `systemTriggered: true` — a plain boolean the caller supplies themselves,
  not a credential (`if (!systemTriggered) { ...require Bearer JWT... }`,
  `user = null` otherwise, no check at all). `sendBroadcastMessage` then
  trusts `data.customerId`, `data.restaurantId`, `data.emailSubject`,
  `data.emailBody`, `data.smsBody` verbatim — no lookup against a real
  campaign/step, and no re-check of the customer's
  `consent_email`/`consent_sms` at all (that check exists only in
  `broadcast-dispatch/dispatch.ts#resolveRecipient`, which this path
  bypasses entirely by calling `outgoing-communications` directly).
  **Exploit:** `POST {SUPABASE_URL}/functions/v1/outgoing-communications`
  with `{"actor":"consumer","action":"broadcast_message",
  "systemTriggered":true,"data":{"customerId":"<any>","restaurantId":"<any>",
  "campaignId":"x","emailSubject":"<anything>","emailBody":"<anything>",
  "sendEmail":true}}` — zero credentials required. Sends as
  `noreply@aiorders.io` / `fromName: restaurant.name`, i.e. impersonating
  any restaurant on the platform to any customer in the database, bypassing
  consent entirely, with no rate limit. This is the exact bug class
  `ENG-036` (P0, confirmed on the board at `state: designed`, owner
  `architect`, not yet built) already tracks for this same function's
  shared gate — but `ENG-036`'s own PRD predates this ticket (filed
  2026-09-03) and never named `broadcast_message`, since it didn't exist
  yet. Not "wait for ENG-036": `ENG-036` sitting unbuilt, with no owner
  currently building it, is exactly why this ticket must not ship a new,
  more dangerous instance riding the same hole today. **Fix (scoped to this
  ticket, independent of ENG-036's own timeline):** stop trusting the
  request body for recipient/content. Change the call contract to a
  `recipientId` — the already-claimed `broadcast_campaign_recipients.id`
  that `dispatch.ts#resolveRecipient` already holds at its call site —
  instead of raw `customerId`/`restaurantId`/`emailSubject`/`emailBody`/
  `smsBody`/`sendEmail`/`sendSms`. `sendBroadcastMessage` looks up that row,
  requires `status = 'claimed'`, and derives customer, restaurant and step
  content from the database, never from the request body.
  `broadcast-dispatch/dispatch.ts`'s own `sendBroadcastMessage` (the
  HTTP-calling `const`) needs the matching change to pass `recipientId:
  recipient.id`. A caller can no longer supply arbitrary recipient/content
  this way — they'd need an already-`claimed`, short-lived, unguessable row
  id, immediately consumed once used. This does **not** fix `ENG-036`
  itself (the shared gate stays broken for every other actor/action) — that
  remains `ENG-036`'s own scope, untouched here.

  **Finding 2 — Medium, blocking (A04 Insecure Design — no rate limit,
  quota, or audience-size cap).** Confirmed by reading
  `validateBroadcastInput`/`createBroadcast` (`brand-portal/broadcasts.ts`)
  and `enrollAudience` (`broadcast-dispatch/dispatch.ts`) in full: zero
  bound anywhere on recipients per campaign, campaigns per restaurant per
  day, or minimum interval between sends. `BATCH_SIZE = 200` throttles
  per-5-minute-tick throughput only, not total campaign size or send
  frequency. This is `ENG-037`'s own security review's routed-forward
  finding (`agents/security/notebook/2026-09-04-findings.md`), which asked
  this gate specifically to confirm a bound exists **or** record its
  absence as a deliberate decision before passing. Neither is true: no
  bound exists, and no ADR or design text accepts this specific abuse
  angle (the design's own Risks section frames the unbounded case as a
  throughput/latency trade-off, not an abuse-prevention one). A legitimate
  or compromised restaurant-owner credential can mass-message that
  restaurant's full customer list repeatedly with nothing to stop it —
  CASL/CAN-SPAM exposure for that tenant, and a deliverability/reputation
  risk for every other tenant sharing the same send infrastructure
  (`noreply@aiorders.io`, the shared SMS provider). Accepting this gap is
  the approver's call, not this gate's, so it can't pass silently a second
  time. **Fix:** a hard cap on recipients per campaign and/or a minimum
  interval between two campaigns from the same restaurant, checked in
  `createBroadcast`. Small, additive, no schema change. If the team wants
  no cap for v1, that needs an explicit approver risk-acceptance (finding,
  exploit path, blast radius, cost to fix/accept) recorded as an ADR, not
  silence.

  **OWASP walk, remaining categories, all clear:** A02 n/a (unsubscribe
  token is HMAC-SHA256 via `crypto.subtle`, constant-time verify built in,
  non-enumerable per design — verified directly in
  `_shared/broadcastUnsubscribe.ts`). A03 n/a (no raw SQL anywhere in the
  diff; the one `.or()` PostgREST filter in `enrollAudience` interpolates a
  server-computed ISO-date `cutoff`, never attacker text). A05 n/a (no
  config/CORS/header change beyond `broadcast-dispatch`'s service-role
  bearer header, matching existing convention). A06 clear (the new
  `deno.json`s pin the exact same `deno.land/std@0.177.0` +
  `npm:@supabase/supabase-js@2` versions `brand-portal`'s own `deno.json`
  already uses — no new dependency, no lockfile drift). A07 clear on the
  intended path (`broadcast-dispatch/auth.ts` checks a real `Bearer
  ${SUPABASE_SERVICE_ROLE_KEY}` comparison, matching `ADR-016`/`ADR-017` —
  correctly the "callee" side `ENG-037`'s own review deferred to this
  ticket). A08 n/a (no CI/CD input, no deserialization, no new webhook).
  A09 clear (`requireRestaurantAccess` logs every denial with
  user/restaurant ids; no secret or token ever logged —
  `verifyUnsubscribeToken`'s catch logs the JS error only, never the
  token/secret). A10 n/a (the one outbound `fetch`, in `dispatch.ts`,
  targets `Deno.env.get('SUPABASE_URL')`, never a caller-supplied URL).
  Cross-tenant authz on the owner-facing surface
  (`brand-portal/broadcasts.ts`) verified directly, not just trusted from
  QA's account: all 7 action handlers call `requireRestaurantAccess`
  (grep-counted), every query additionally filters by `restaurant_id`, and
  `broadcasts.test.ts`'s two cross-tenant tests (`getBroadcast`/
  `getBroadcastReport`) genuinely construct a row owned by a different
  restaurant rather than a tautology. `enrollAudience`'s audience query is
  scoped by `campaign.restaurant_id` (DB-sourced, never caller input) — no
  cross-tenant vector on the dispatch path, confirmed by reading the code
  myself, matching AC3's own non-blocking "not automated" note in QA's test
  plan. Secrets: `git diff origin/main...HEAD -p` and
  `git log origin/main..HEAD -p` both scanned — zero hits beyond the
  deliberately-labeled test fixture
  (`test-only-hmac-secret-do-not-use-in-prod`). LLM checklist: n/a in full,
  no model/agent/tool/MCP/RAG anywhere in this diff.

  **Two non-blocking notes, for completeness, neither acted on:** (a)
  `broadcast-dispatch/auth.ts`'s `authHeader === \`Bearer ${expected}\``
  is a non-constant-time comparison of the service-role key — matches the
  already-established `ADR-016`/`ADR-017` convention verbatim (not a
  pattern this ticket invented) and isn't practically exploitable over a
  network round trip against a high-entropy secret. (b)
  `broadcast-dispatch/index.ts` doesn't log a failed `authorizeServiceRole`
  check server-side, unlike `brand-portal`'s denial logging — same shape as
  other systemTriggered-style gates already in this codebase, not a
  regression this ticket introduces.

  SOC 2 evidence trail: ticket → PRD → design → review verdict (5 rounds,
  pass) → test run (pass, 77/0) → this verdict → release record. Complete;
  this verdict is the first gap in the trail, which is what the gate is
  for. Data classification: the customer contact fields Finding 1 exposes
  (email, phone, consent state) are Restricted-tier per
  `security-baseline.md` — the reason Finding 1 is Critical rather than
  merely High.

  **No receipt written** — `agents/security/reviews/ENG-038.md` does not
  exist and is not created on a fail (`skills/security-gate/SKILL.md` step
  9). Full findings also logged: `agents/security/notebook/
  2026-09-04-findings.md`.

  Per `skills/security-gate/SKILL.md` step 9: **1 transition** —
  `in-security → building`, owner `security → backend`. WIP/approval caps
  unaffected — still the one machine-WIP ticket (the `ENG-019` family's
  slot, `1/1`), `building` is within the counted range.
  `time_spent`/`time_remaining` updated in frontmatter.

  Dead-end sweep: no other ticket touched this pass. Notify sweep: nothing
  to raise — a security-gate fail is fixed, not escalated, so no gate item
  was written this pass; checked all three open `inbox/` items for the
  24h-nudge condition anyway (current time `2026-09-04T19:14:05` PDT):
  `ENG-027`/`ENG-028` already carry a one-time `nudged:` stamp, nothing
  more owed; `ENG-016`'s Piece-2 item (`notified: 2026-09-04T10:58:06`) is
  ~8h16m old, still under the 24h threshold. Nothing nudged. Step 8b: one
  observation filed (`agents/eng-manager/observations.md`) on a systemic
  pattern this finding surfaced; no `exception-request:` found. Step 8c:
  n/a, no gate answered this pass.

  `chained: ENG-038` — `building` is agent-owned (the two fixes are the
  next hop's own work, owner `backend`), not the approver, not blocked,
  not terminal, not held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/
  projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-038` before this pass exits. Post-pass `eng-gate-check.sh
  ENG-038` and whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **security-fix round 1: both blocking findings fixed**
  (backend, `continue ENG-038` event pass, per prior pass's `chained:
  ENG-038`). No gate ran this hop. Finding 1 (critical) and Finding 2
  (medium) from security-gate round 1 both fixed as specified, in the
  `aiorders-api` worktree, re-confirmed fresh against `origin` before
  editing. 8 new/rewritten tests across three suites; full regression
  70/70 (62 pre-existing + 8 this round), no regression; `deno check` on
  all three touched files surfaced no new errors. No receipt (fixing a
  finding isn't a gate). Full reasoning:
  `agents/backend/notebook/2026-09-04-eng038-security-round1-fixes.md`.

  Two commits, pushed to
  `origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`:
  `92d1bd4` (Finding 1) and `63f5635` (Finding 2 + `README.md`).

  Per this ticket's own round-2/3/4-fix precedent (normal build-hop exit,
  branch pushed and self-tested): **1 transition** — `building →
  in-review`, owner `backend → principal-engineer`. WIP/approval caps
  unaffected — still the `ENG-019` family's `1/1` slot. `time_spent`/
  `time_remaining` updated in frontmatter.

  Dead-end sweep: no other ticket touched this pass. Notify sweep: nothing
  to raise — no gate item written this pass; checked all three open
  `inbox/` items for the 24h-nudge condition (current time
  `2026-09-04T19:39:44` PDT): `ENG-027`/`ENG-028` already carry a one-time
  `nudged:` stamp, decision still empty, nothing more owed; `ENG-016`'s
  Piece-2 item (`notified: 2026-09-04T10:58:06`) is ~8h41m old, still
  under 24h. Nothing nudged. Step 8b: no new observation or proposal
  beyond this ticket's own scope; no `exception-request:` found. Step 8c:
  n/a, no gate answered this pass.

  `chained: ENG-038` — `in-review` is agent-owned (review round 6 is the
  next hop's own work), not the approver, not blocked, not terminal, not
  held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/projects/personal/
  business-os/departments/engineering/lib/eng-trigger.sh continue ENG-038`
  before this pass exits. Post-pass `eng-gate-check.sh ENG-038` and
  whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **review round 6: PASS / PASS** (principal-engineer + qa,
  `continue ENG-038` event pass). Scope: diff since round 5's reviewed
  commit (`125286f..63f5635`, the two security-fix commits — 7 files, 474
  insertions/106 deletions). Worktree re-checked fresh against `origin`
  before reviewing anything: HEAD `63f5635`, no drift.

  The prior hop's own `building → in-review` transition cited "this
  ticket's own round-2/3/4-fix precedent" — that citation doesn't quite
  fit (those precedents were fixes for findings raised *inside* the
  in-review combined hop; these two were security-gate findings, raised
  after review had already passed), but the destination is right on
  independent grounds: the two fix commits are new code principal-engineer
  has never reviewed, and code-review-gate's own job (correctness, shape,
  test quality) is distinct from what security already checked. Recorded
  so the next reader doesn't take the prior citation at face value the way
  this hop almost did.

  Code review 0/10 automatic failures. Traced both fixes against the
  design: Finding 1's `recipientId`/claimed-row contract confirmed against
  the actual migration (`broadcast_campaign_recipients.restaurant_id` is a
  real, denormalized column; `status = 'claimed'` is a legal value per
  `20260904150000_broadcast_recipients_claimed_status.sql`, added in the
  *original* build commit, not new this round). Checked the new consent
  re-check's object-shape assumption
  (`customer.consent_email?.consent !== false`) against every read/write
  site in the repo — real, established idiom, not a defect; recording the
  check since a shape mismatch here would have made the "defense in
  depth" consent gate silently inert. Finding 2's audience/interval caps
  run after `requireRestaurantAccess`, fail closed on a lookup error, and
  `updateBroadcast` correctly omits the interval check (an edit creates no
  new campaign row).

  Independently re-ran the full regression fresh (85 passed/0 failed
  across five suites — round 5's 77 plus 8 new, reconciling exactly
  against the backend's own count) and `deno check` from each function's
  own directory (`dispatch.ts` 0 errors, `broadcasts.ts` 3 pre-existing in
  `utils.ts`, `consumers.ts` 8 in-file + 5 imported = 13 total, matching
  round 5's own baseline exactly — one line shifted 1091→1120 from the new
  code above it, same pre-existing catch block, not a new condition).

  Two new non-blocking findings: (1) low severity — a recipient row
  already `claimed` when `cancel_broadcast` runs isn't among the rows that
  action cancels (pre-existing behaviour, narrow window, never surfaced in
  five prior rounds); (2) very-low-severity test-quality nit — the new
  cap/interval-rejection tests don't independently verify
  `restaurant_id`-scoping the way the cancelled-campaign test verifies its
  own filter. Carried forward unchanged: F2 + its round-3 extension,
  `matchesOrExpr`'s truncation bug, `enrollAudience`'s untested
  restaurant-scoping, round 1's unclaimed cross-tenant mutation. Round 5's
  own non-blocking finding (`sendBroadcastMessage`'s untested DB-fetch
  failure branches) is broadened, not repeated: this round's two new
  lookups (recipient, step) add two more untested throw sites to the same
  class, now four instead of two — still non-blocking, same reasoning.
  Good work named: the "derives customer, restaurant, and content strictly
  from the claimed recipient row" test, which replays the actual pre-fix
  attack shape against the new code rather than just exercising the new
  contract. Receipts: `agents/principal-engineer/reviews/ENG-038.md`
  (round 6), `agents/qa/test-plans/ENG-038.md` (updated in place). Full
  reasoning: `agents/principal-engineer/notebook/2026-09-04-review-log.md`.

  **Quality gate: PASS.** Neither finding maps to a PRD acceptance
  criterion (the PRD names no rate/audience cap or recipient-identity
  contract anywhere), so this round owned suite-green, a verified
  regression test per finding, and no open P0/P1
  (`agents/qa/bugs/_index.md` has no ENG-038 entry) — all three satisfied.
  Fresh re-check of AC1–7: all still pass, none touch this round's changed
  logic (audience *resolution*, redemption/revenue, and unsubscribe are
  all untouched files this round).

  Per `code-review-gate/SKILL.md` step 9: **1 transition** —
  `in-review → in-security`, owner `principal-engineer → security` — back
  to security to confirm its own two findings are actually closed, not a
  fresh code-review lap. WIP/approval caps unaffected — still the
  `ENG-019` family's `1/1` slot. `time_spent`/`time_remaining` updated in
  frontmatter.

  Dead-end sweep: no other ticket touched this pass. Notify sweep: nothing
  to raise — a gate pass isn't approver-facing, no gate item written this
  pass; checked all three open `inbox/` items for the 24h-nudge condition
  anyway (current time `2026-09-04T19:54:00` PDT): `ENG-027`/`ENG-028`
  already carry a one-time `nudged:` stamp, decisions still empty, nothing
  more owed; `ENG-016`'s Piece-2 item (`notified: 2026-09-04T10:58:06`) is
  ~8h56m old, still under 24h. Nothing nudged. Step 8b: no new observation
  or proposal beyond the two non-blocking findings already recorded above
  (ticket-specific, not a systemic pattern); no `exception-request:`
  found. Step 8c: n/a, no gate answered this pass.

  `chained: ENG-038` — `in-security` is agent-owned (security's own gate
  is the next hop's work), not the approver, not blocked, not terminal,
  not held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/projects/
  personal/business-os/departments/engineering/lib/eng-trigger.sh continue
  ENG-038` before this pass exits. Post-pass `eng-gate-check.sh ENG-038`
  and whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **security gate round 2: PASS** (security, `continue ENG-038`
  event pass). Re-verified both round-1 findings against the fix commits
  (`92d1bd4`/`63f5635`) and the live code/schema directly, not either
  agent's account. Finding 1: `sendBroadcastMessage` takes only
  `{recipientId}`, requires `status = 'claimed'` on an unguessable,
  single-claim, single-use row; the removed fields are read nowhere —
  closed. Finding 2: audience cap + interval check run after authz, fail
  closed, tested against real returned error strings — closed. Fresh
  regression 85/85, reconciling exactly against round 6. One new
  non-blocking finding: a narrow TOCTOU race on the interval check (bounded
  — the size cap has no equivalent race); not proposed, ticket-specific.
  Receipt: `agents/security/reviews/ENG-038.md`. Notebook:
  `agents/security/notebook/2026-09-04-findings.md`.

  **1 transition** — `in-security → ready-to-ship`, owner `security →
  devops`. WIP unaffected (`ENG-019` family's `1/1` slot).
  `time_spent`/`time_remaining` updated.

  Dead-end sweep: no other ticket touched. Notify sweep: nothing to raise —
  a gate pass isn't approver-facing; checked all three open inbox items for
  the 24h-nudge condition (current time ~20:17 PDT, `notified:`/`nudged:`
  read as local per `proposals.md`'s 2026-09-02 correction, not UTC):
  `ENG-027`/`ENG-028` already carry their one-time nudge; `ENG-016` Piece-2
  (~9h19m old) still under 24h. Nothing nudged. Step 8b: nothing beyond the
  one ticket-specific finding logged above; no `exception-request:` found.
  Step 8c: n/a, no gate answered this pass.

  `chained: ENG-038` — `ready-to-ship` is agent-owned (devops's own
  release-readiness hop is next), not the approver, not blocked, not
  terminal, not held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/
  projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-038` before this pass exits. Post-pass `eng-gate-check.sh
  ENG-038` and whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **release-readiness: RETURNED — migration gate never ran**
  (devops, `continue ENG-038` event pass). `skills/release-runner/SKILL.md`
  step by step; L1 window check skipped per this project's own established
  reading (clock check only — steps 2-3's readiness content still runs).

  **Step 2 (upstream gates).** Code review (round 6), quality (round 6),
  and security (round 2) all re-verified fresh from their own receipts —
  genuinely `pass`. But this ticket also owes a migration verdict, and none
  exists: `building` (owner `backend`, per this ticket's own log) wrote
  `supabase/migrations/20260904150000_broadcast_recipients_claimed_status.sql`
  directly — a real schema change (adds `'claimed'` to a check constraint,
  a new index on `step_id`, a new check constraint on
  `broadcast_campaigns.scheduled_send_at`), read in full this pass. No
  `agents/database/migrations/ENG-038-*.md` exists; no log entry anywhere
  on this ticket attributes a hop to `database`; the rollback exists only
  as a SQL comment, never executed — unlike `ENG-037`'s and `ENG-031`'s own
  migrations, both drilled against a disposable Postgres replica first.
  `agents/backend/agent.md`'s own `never_touches` names exactly this:
  "schema design or migrations (database owns those — you request, they
  design)." `conventions.yaml` lists migration as one of five separate
  blocking machine gates, and `database/agent.md` names "the migration
  gate" as its own exclusive scope — code review's and security's
  incidental scrutiny of the same file (constraint legality; whether
  `'claimed'` closes their own finding) is not that gate. Per
  `release-runner/SKILL.md` step 2, verbatim: "A missing verdict is a fail,
  not an assumption — return the ticket to the gate that never ran."

  **Step 3, checked anyway.** Read `dispatch.ts` in full: every reachable
  failure path already logs (`console.error`) and marks a terminal status;
  the one named gap (a row stuck `claimed` on a hard process kill between
  claim and resolve) is self-diagnosable via the migration's own comment,
  bounded, non-blocking — not why this ticket is returned, named for
  completeness. Cost $0/month either way. Window n/a, L1. Step 4 not
  reached — no PR opened.

  **1 transition** — `ready-to-ship → building`, owner `devops →
  database`. Not `blocked`: no ticket on this board uses `blocked` for an
  unmet gate verdict, and `building` is exactly where `ENG-037`'s/
  `ENG-031`'s own `database` work already happened, before their own
  `in-review` hop. WIP unaffected (`ENG-019` family's own `1/1` slot).
  `time_spent`/`time_remaining` updated. Full reasoning, evidence, and the
  `dispatch.ts` read: `agents/devops/notebook/2026-09-04-release-readiness-log.md`.

  Dead-end sweep: no other ticket touched. Notify sweep: nothing to raise —
  a gate fail isn't approver-facing (no production exposure; `ENG-037`'s
  own tables are still unread/unwritten); checked all three open `inbox/`
  items for the 24h-nudge condition (current time `2026-09-04T20:33` PDT):
  `ENG-027`/`ENG-028` already carry their one-time nudge; `ENG-016`'s
  Piece-2 (~9h35m old) still under 24h. Nothing nudged. Step 8b: proposal
  filed (`proposals.md`, this date) — no mechanical check anywhere catches
  a migration file with no matching `agents/database/migrations/` receipt;
  both this hop's own pre-pass `eng-gate-check.sh` runs (scoped and
  whole-board) exited 0 clean despite the gap. Related to, distinct
  mechanism from, the existing 2026-09-03 principal-engineer proposal on
  the same file. No `exception-request:` found. Step 8c: n/a, no gate
  answered this pass.

  `chained: ENG-038` — `building` is agent-owned (database's own migration
  gate is the next hop's work), not the approver, not blocked, not
  terminal, not held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/
  projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-038` before this pass exits. Post-pass `eng-gate-check.sh
  ENG-038` and whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **migration gate: PASS** (database, `continue ENG-038` event
  pass, per prior pass's `chained: ENG-038`). Wrote the missing receipt and
  ran the gate against the migration `backend` committed directly at
  `building` (`20260904150000_broadcast_recipients_claimed_status.sql`) —
  the specific gap release-readiness returned the ticket for. Additive-only
  (widened status check, new `step_id` index, new `scheduled_send_at`
  check); both affected tables confirmed empty on the live, linked project
  (0 rows) — `20260904140000` (ENG-037's base schema) is already applied
  remotely, this migration is not. Rollback **actually executed** against a
  disposable Postgres replica (`public.ecr.aws/supabase/postgres:15.8.1.073`,
  same image/method as `ENG-037`'s own gate) and behaviourally re-verified
  (claim rejected again, index gone, constraint gone — not just "ran clean")
  — closing the one gap named at return. Schema/code coexistence confirmed
  by reading every write path to `broadcast_campaigns.status`
  (`brand-portal/broadcasts.ts`'s `createBroadcast`/`updateBroadcast`/
  `setBroadcastStatus`/`cancelBroadcast`, `broadcast-dispatch/dispatch.ts`'s
  `promoteDueCampaigns`) directly: none can produce a row the new
  constraint would reject. No edit to the migration file itself, so no new
  diff for principal-engineer to re-review. Receipt:
  `agents/database/migrations/ENG-038-broadcast-recipients-claimed-status.md`
  (full verification trace there).

  Per `skills/schema-change/SKILL.md` step 10 ("pass → continue the
  pipeline") and this ticket's own upstream gates (review round 6, quality
  round 6, security round 2) already passing: **1 transition** —
  `building → ready-to-ship`, owner `database → devops`, for
  release-readiness to re-run with all four gate receipts now present. WIP
  unaffected (`ENG-019` family's `1/1` slot). `time_spent`/`time_remaining`
  updated in frontmatter.

  Dead-end sweep: no other ticket touched. Notify sweep: nothing to raise —
  a gate pass isn't approver-facing; checked all three open `inbox/` items
  for the 24h-nudge condition (current time `2026-09-04T20:53:20` PDT):
  `ENG-027`/`ENG-028` G1s each already carry their one-time `nudged:`
  stamp, decisions still empty, nothing more owed; `ENG-016`'s Piece-2 item
  (`notified: 2026-09-04T10:58:06`) is ~9h55m old, still under the 24h
  threshold. Nothing nudged. Step 8b: nothing new to observe or propose —
  the process gap that made this receipt retroactive (`backend` writing a
  migration directly instead of routing it to `database`) is already
  proposed (`proposals.md`, 2026-09-04); no `exception-request:` found.
  Step 8c: n/a, no gate answered this pass.

  `chained: ENG-038` — `ready-to-ship` is agent-owned (devops's
  release-readiness re-run is next), not the approver, not blocked, not
  terminal, not held by a cap. Fired `/bin/zsh /Users/hwalia/Documents/
  projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-038` before this pass exits. Post-pass `eng-gate-check.sh
  ENG-038` and whole-board: see board index.

  business-os left uncommitted — standing default, convention still open.

- `2026-09-04` **release-readiness round 2: PASS** (devops, `continue
  ENG-038`). Entry kept short per `conventions.yaml` →
  `ticket_log.entry.cap_lines: 20`; full reasoning:
  `agents/devops/notebook/2026-09-04-release-readiness-log.md`.

  All four upstream gates re-verified fresh, still passing (review round
  6, QA round 6, security round 2, migration gate). Readiness gate held,
  no blocking failure — migration rollback already tested; two
  non-blocking observability gaps named (claimed-row-stuck edge case;
  `ENG-037`'s cron confirmed live, 404ing every 5min against this
  not-yet-deployed function, harmless — 0 rows anywhere); cost $0/month.
  Opened `aiorders-api` PR #16; raised L1 merge request
  (`inbox/2026-09-04-eng038-merge-request.md`).

  **1 transition** — `ready-to-ship → blocked`, `blocked_on: approver`,
  `blocked_from: ready-to-ship`, owner `devops → approver`, `links.pr`
  set. WIP unaffected. `chained: none` — waiting on the approver, an L1
  merge is a human gate.

  business-os left uncommitted — standing default, open.

- `2026-09-04` **step-5 merge re-check: still open** (eng-manager, `watch
  (launchd)` event — new `inbox/2026-09-04-eng038-merge-request.md`
  triggered the sweep). `git fetch` + ancestry check against
  `~/Documents/projects/_eng/aiorders-api`: branch
  `feat/ENG-038-broadcast-composer-dispatcher-unsubscribe` (`63f5635`) is
  not an ancestor of `origin/main` (`64baabf`) — PR #16 still open.

  **No transition** — stays `blocked`, `blocked_on: approver`. `chained:
  none` — waiting on the approver, an L1 merge is a human gate (unchanged
  from last hop).

  business-os left uncommitted — standing default, open.

- `2026-09-05` **step-5 merge re-check: MERGED — full acceptance-check —
  `blocked → shipped → verified`** (product-manager, `scheduled` event pass,
  02:00 PDT). Pre-pass `eng-gate-check.sh`, scoped (`ENG-038`) and
  whole-board: both exit 0, clean.

  **Merge confirmed two ways.** `git fetch` + `git merge-base --is-ancestor
  origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe origin/main`
  → merged; cross-checked `gh pr view 16` → `state: MERGED`, `baseRefName:
  main`, `mergeCommit: 89c6fdb1`, `mergedAt: 2026-09-05T07:22:20Z`. No
  stacking. `git show --stat` on the merge commit: 18 files, 3235/7, all
  present on `origin/main` directly (`git ls-tree`) — no drift from this
  ticket's own recorded diff. No written reply to
  `inbox/2026-09-04-eng038-merge-request.md` — same standing pattern this
  approver has used for every prior L1 merge on this board.

  **All four gate receipts re-read fresh, all still `pass`:** code review
  round 6, quality round 6 (85/85), security round 2, migration gate. Per
  step 5 ("a merge is not a gate"), verified before advancing rather than
  assumed from the merge request's own account.

  **Ran `acceptance-check/SKILL.md` in full, not the receipt-bookkeeping
  shortcut** — this ticket owns all 7 of `ENG-019`'s acceptance criteria per
  `2026-09-04-eng019-work-breakdown.md`'s own AC-mapping ("every criterion is
  backend-enforced... mapped here so a later gate doesn't have to re-derive
  it"), unlike `ENG-037`'s 0-criteria schema-only shape. Read every touched
  file directly from `origin/main` at the merge commit and traced each
  criterion against it, not against the diff, the PR description, or any
  gate's own summary. **Discovered mid-check: release-readiness's own
  "not deployed" snapshot (the pass immediately before this one) was already
  stale** — `supabase functions list` now shows all four touched functions
  (`brand-portal`, `broadcast-dispatch`, `broadcast-unsubscribe`,
  `outgoing-communications`) deployed, version-bumped 3-8 minutes after the
  merge, no tracked workflow responsible (reads as the approver deploying by
  hand). Re-verified live, read-only: the migration's `'claimed'` check value
  and `step_id` index are live; the Vault `service_role_key` `ENG-037`'s
  cron needs is present; `BROADCAST_UNSUBSCRIBE_SECRET` is **not** in
  `supabase secrets list` (name only, no value read) — `hmacKey()` will
  throw the moment this path is actually exercised, dormant today (zero
  campaigns exist, and `ENG-039` — the only way to create one — hasn't
  shipped), same non-blocking shape as `ENG-037`'s own Vault-secret
  prerequisite, already named in three other notebooks. Did not create a
  test campaign or exercise a real send — that would dispatch actual
  email/SMS to real customers against `bmnmnejwdxbcqinqkwko`, out of bounds
  for verification. **All 7 criteria: pass.** No scope creep (one adjacent-
  but-not-violating non-goal noted: the report's open/click counters read
  pre-existing, universally-populated `communication_log` columns, adding no
  new tracking instrumentation of their own). Cost matches ($0/month). Full
  walk: `agents/product-manager/notebook/2026-09-05-eng038-acceptance.md`.
  Release record: `agents/devops/releases/2026-09-05-aiorders-api-ENG-038.md`,
  `links.release` set in the same edit.

  **2 transitions** (`blocked → shipped`, `shipped → verified`), under the
  cap of 4. `state: verified`, `owner: approver → eng-manager`,
  `blocked_on`/`blocked_from` cleared, `time_remaining: none`.

  **Consequence for the family:** this ticket's `blocks: [ENG-039]` — its
  sole dependency is now satisfied. `ENG-019` (parent) still cannot reach
  `shipped` until `ENG-039` is settled too (`ADR-003`); machine WIP
  unaffected (`1/1`, still held by the `ENG-019` family).

  **Dead-end sweep (whole board, this is a `scheduled` pass):** no broken
  chains found (no `*-eng-events-dropped.md` for today; `traces/.pending`
  empty). No WIP violations, no `priority: hold` ticket in a working state,
  no `blocked` ticket past its 3-day resurface threshold. See the board
  index's own closing notes for this pass.

  **Notify sweep:** nothing to raise — a ship isn't approver-facing.
  `ENG-027`/`ENG-028` already past their one-time `nudged:`; `ENG-016`'s
  Piece-2 question (~15h old) still under the 24h threshold. This ticket's
  own merge-request item moved to `inbox/_handled/`, `## Decision` filled in
  with the plain-language merge note.

  **Step 8b:** one observation filed (`observations.md`) — a gate's own
  "not deployed" snapshot went stale within the same evening once a human
  started merging and deploying by hand outside any tracked workflow; worth
  re-verifying live deploy state at each gate that depends on it rather than
  trusting the last pass's own answer. No `exception-request:` found.

  **Step 8c:** decision-journal entry added (see `decision-journal.md`).

  Post-pass `eng-gate-check.sh`, scoped (`ENG-038`) and whole-board: both
  exit 0, clean.

  `chained: none` — `verified` is terminal; the chaining guard never fires
  on a terminal ticket. `chained: ENG-039` fired instead, recorded on
  `ENG-039`'s own log — see that ticket's file.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.
