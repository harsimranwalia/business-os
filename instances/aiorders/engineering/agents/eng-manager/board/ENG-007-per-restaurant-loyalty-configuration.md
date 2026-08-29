---
id: ENG-007
title: Per-restaurant loyalty configuration — earn rates and redemption value
project: aiorders-api
type: feature
size: S
time_estimate: S (a few hours to half a day, per PRD Cost section)
time_spent: not separately clocked — build, review, QA and security all completed in an unrecorded prior pass (see Log); read as most of the estimate consumed
time_remaining: ~0 build time; PR-open, merge and verify remain as gate/administrative steps, not development work
severity: P3
priority:
state: ready-to-ship
owner: devops
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-28
updated: 2026-08-29
branch: loyalty-system
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-007-per-restaurant-loyalty-configuration.md
  design: agents/architect/designs/ENG-007-per-restaurant-loyalty-configuration.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-007.md
  test_plan: agents/qa/test-plans/ENG-007.md
  security_review: agents/security/reviews/ENG-007.md
  release:
  pr:
---

## Input

Verbatim, from `inbox/requests/2026-08-28-eng006-sequence-item-2.md` (now
`inbox/_handled/`), filed by the approver (`source: harry`), received
2026-08-29T04:30:00.000000+00:00 — preserved here per
`skills/request-readback/SKILL.md` step 1, never edited:

> # Continue the approved ENG-006 loyalty-identity sequence — file ticket 2
>
> `ENG-006` (unified cross-restaurant customer identity) is `verified` and
> its PRD (`agents/product-manager/specs/ENG-006-unified-customer-identity.md`,
> "Feature shape and sequencing") proposed a five-ticket sequence for the
> loyalty feature, of which `ENG-006` was item one. The G1 answer on that
> ticket explicitly affirmed proceeding with the whole shape: "the proposed
> five-ticket sequence stands as shape to file incrementally, not as four
> pre-approved tickets." Harry's own later clarification of what that
> meant: "we finish one ticket then you file next and seek approval then
> next then next till feature is complete" — and that filing the next item
> is not the department inventing work, since the shape was already
> reviewed once.
>
> This request exists because `skills/acceptance-check/SKILL.md` step 6b
> (the mechanism meant to do this automatically the moment a sequenced
> ticket verifies) didn't exist yet when `ENG-006` actually passed
> acceptance-check, so nothing fired. Filing this directly through the
> normal front door rather than trying to retroactively re-trigger a pass
> that already completed.
>
> Item 2, as `ENG-006`'s own PRD scoped it: "Per-restaurant loyalty
> configuration — earn % (online, dine-in) and a redemption value, per
> restaurant, effective-dated so a later rate change doesn't rewrite the
> meaning of past ledger entries. No dependency on `ENG-006`; could build
> in parallel." Backend and migrations go in `aiorders-api`, same as
> `ENG-006`. Frontend is out of scope for this whole sequence, same as
> `ENG-006` — a separate, later discussion.
>
> Shape this into its own ticket and PRD exactly as any fresh intake
> would — this note only carries forward the shape already agreed at
> `ENG-006`'s G1, not a pre-approval of this ticket's own scope,
> acceptance criteria, or size.

## Readback

See `agents/product-manager/specs/ENG-007-per-restaurant-loyalty-configuration.md`
→ Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

Tickets 3 and 4 of the approved loyalty sequence both need a per-restaurant
rate to compute against, and nothing in the system stores one today.

## Outcome

Every restaurant can have an online earn %, a dine-in earn %, and a
redemption value on file, effective-dated, with a full history of what was
true when — no later rate change can alter what an earlier ledger entry's
rate was. Nothing user-facing changes yet; no ledger, no points, no
redemption until tickets 3 and 4 ship.

## Notes

**Sized `S`, not `L` like `ENG-006`.** A single effective-dated config
table plus a minimal read/write surface — no auth, no session, no identity
mapping. Materially smaller than the ticket it follows.

**`severity: P3`, same reasoning as `ENG-006`.** Nothing is broken; this is
scoped opportunity work the approver already reviewed the shape of.
`priority` is left to the approver, per `definition-of-done.md`.

**No dependency on `ENG-006`**, per the request's own text — a candidate
for the EM to sequence in parallel with anything else in flight at
`ready`. Not decided here.

**Branch:** `ENG-006`'s ticket recorded that the approver asked for the
whole loyalty sequence to share one branch, `loyalty-system`, in
`aiorders-api`, rather than the standard one-ticket-one-branch convention.
Carried forward here — whoever picks this ticket up at `building` should
branch from (and merge back into) `loyalty-system`, not cut a fresh
`feat/ENG-007-...` off `main`. Left blank in frontmatter per the
template's own lifecycle (set by the engineer at `building`).

**Model deviation, named rather than hidden.** `skills/request-readback/SKILL.md`
directs opus for both readings; `ENG-006`'s own precedent honored that
explicitly. This pass's blind architect reading was spawned without an
explicit `model: opus` override, under whatever this pass's default
subagent routing resolves to. Not redone: the output was thorough,
specific, and converged cleanly with this PM's independent reading down to
matching sub-details neither reading could have copied from the other (the
"not enrolled" default, the single non-channel-split redemption value) —
nothing about it reads as shallow or subtly wrong, the exact failure mode
the opus direction exists to guard against. Flagged for whoever automates
the readback dispatch next, not reopened here — and worth naming why it
happened: this same account had already hit its monthly spend limit once
today mid-pass on this exact ticket (see Log), so the lower-cost default
was the practical outcome of the environment this pass ran in, not a
considered substitution.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-28` `intake → shaped → awaiting-scope` (product-manager, `watch`
  event pass, context `launchd`). This is attempt 2/2 of this fire —
  attempt 1 (21:33–21:38) reached the same request file, ran the mode
  check and board sweep, spawned the blind architect-reading subagent, and
  then died mid-flight on the account's monthly spend limit
  (`traces/eng-loop-2026-08-28.log`: `pass end: watch (exit 1, 352s)`,
  classified a real failure — charged, not refunded, since the 352s run
  time clears the 60s never-started threshold despite the vendor-limit
  signature in its output). Verified fresh rather than trusted: no
  artifact from attempt 1 survived on disk (`agents/product-manager/specs/`
  and this board directory held nothing for this request; `ListAgents`
  showed no orphaned subagent), so this pass redid the work from scratch
  rather than resuming a partial state. Mode check clean (business-os
  `.env` → `MODE=active`).

  **Swept all three watched inboxes fresh**, per the `watch` event's own
  contract (act on whatever is new across all three, not just one
  ticket). `agents/product-manager/inbox/` and `agents/eng-manager/inbox/`
  held only `.gitkeep` plus already-`_handled/` items. `inbox/` held one
  already-notified, non-P0 item (`2026-08-28-eng-events-dropped.md`,
  unrelated to this ticket) and `inbox/requests/` held exactly one new
  file: `2026-08-28-eng006-sequence-item-2.md`. `traces/.pending` also
  carried a queued `1 intake 2026-08-28-eng006-sequence-item-2.md` line
  behind this pass, for the same file — matches this instance's
  well-documented duplicate-queued-event race
  (`agents/eng-manager/observations.md`), where a filesystem change fires
  both a `watch` and its own dedicated event and whichever drains first
  does the real work. Processed it here rather than leaving it for the
  queued `intake` event, since it's exactly what this `watch` sweep exists
  to act on; the `intake` event will very likely no-op when it drains
  next, per the established pattern.

  **Ran the full request-readback** (`skills/request-readback/SKILL.md`):
  this PM's independent reading plus a blind architect reading (a
  subagent given only the raw request verbatim and
  `../knowledge/business-profile.md`, no model override specified — see
  Notes above), neither seeing the other's reading. **Compared and found
  no material divergence** — both converged on the core shape (a
  per-restaurant, effective-dated config table holding two earn rates and
  one redemption value, backend/migrations only, no dependency on
  `ENG-006`'s identity model), including independently matching on two
  sub-details neither could have copied from the other. Differences were
  additive technical texture from the architect's lens (temporal table
  shape, the snapshot-vs-pinned-read mechanism choice, a sharper framing
  of the open unit question) rather than disagreement about scope or
  purpose — per the skill's own classification table, "fine, proceed," not
  a fork to ask about. No question put to the approver. Full comparison in
  the PRD's Readback section.

  **Sized `S`.** PRD written:
  `agents/product-manager/specs/ENG-007-per-restaurant-loyalty-configuration.md`,
  including acceptance criteria and non-goals naming the other three
  unfiled sequence items explicitly.

  **G1 required** — full lane, not XS/bug/chore, so G1 is not a judgement
  call here. Checked caps fresh before raising: approver-facing WIP (2) at
  0, approval cap (3) at 0 — both fully free, board fully terminal. Wrote
  `inbox/2026-08-28-eng007-g1-scope.md` (`agent: product-manager`,
  `gate: scope`, `project: aiorders-api`, recommendation to build now,
  readback first per the skill's own ordering). Ran
  `departments/engineering/lib/eng-notify.sh raise
  inbox/2026-08-28-eng007-g1-scope.md`; stamped `notified:` in the gate
  item's own frontmatter. PRD `status: draft → awaiting-scope`.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver` per `definition-of-done.md`'s state
  table. **Consequence:** approver-facing WIP 0 → 1 (cap 2, room for one
  more); approval cap 0/3 → 1/3. `machine_wip` unaffected — this ticket
  doesn't enter that range yet. **1 transition-worthy stop** (one gate
  reached); did not proceed further — `awaiting-scope` is a human stop by
  design.

  **Dead-end sweep:** no other ticket is in flight (board fully terminal
  before this pass) — nothing else to check.

  **Notify sweep:** this pass's own gate item was raised and stamped
  above. Nothing else to nudge (board otherwise empty); approval cap 1/3,
  not full — no stall.

  `chained: none` — sitting at `awaiting-scope`, owned by the approver;
  the chaining guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
  whole-board: both run clean.

- `2026-08-29` `awaiting-scope → designed → awaiting-decision` (architect,
  then eng-manager — `watch` event pass, context `schtasks`). Per the
  event's own contract, swept all three watched inboxes fresh rather than
  sweeping the whole board. Mode check clean (business-os `.env` → `MODE=`
  empty; instance `config/config.yaml` → `mode:` empty, both fall through).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-007`) and whole-board: both exit 0, clean.

  **Third attempt at tonight's fire, confirmed rather than assumed.**
  `traces/eng-loop-2026-08-29.log` and `traces/.loop.lock/pid` (`1067`,
  matching `traces/.pass-out.1067`, this session's own narration mirrored
  live — read directly, not inferred): two earlier launches for the same
  underlying `watch (schtasks)` event went stale and were force-cleared by
  the trigger (pid `3199`, started 23:51 the prior day; pid `1301`, started
  00:05:07 this morning) before this one (pid `1067`, 00:38:56) reached the
  lock. Checked both dead attempts' own output before trusting a clean
  slate: neither reached a `Write`/`Edit` call — both died mid-investigation
  (`.pass-out.3199` last mid-`Grep`; `.pass-out.1301` mid-checking the first
  attempt's own stale lock) — so nothing was silently half-written to
  reconcile, unlike `ENG-006`'s build-recovery precedent. `.hops-2026-08-29`
  reads `2` (this is the day's second charged launch), nowhere near the
  40/day ceiling.

  **This ticket's own G1 is what the sweep found new**: `inbox/2026-08-28-eng007-g1-scope.md`
  carried `decision: approved`, `decided: 2026-08-29T07:15:41.687445+00:00`
  — a hand-edit, not a reply through `lib/eng-notify.sh`'s channel (unsurprising:
  this pass's own live call to it, raising the G2 below, logged
  `traces/eng-notify-2026-08-29.log`: `SLACK_WEBHOOK_URL unset — cannot
  notify` — the plain-failure face of the already-open `proposals.md`
  2026-08-25 channel-dispatch bug, not a new finding). No rider, no
  correction to the readback or recommendation — read as a full,
  unconditional approval. Moved to `inbox/_handled/` with a processed
  footer; journaled in `agents/eng-manager/config/decision-journal.md`.

  **Found the PRD's own `status`/`decided` fields stale** — still `draft`/
  empty, despite this ticket's own frontmatter and log already showing
  `awaiting-scope` reached in the prior pass. Same class of gap `ENG-006`
  caught once already (a crash-and-recover pass leaving on-disk artifacts
  partially updated) — this ticket's own log records exactly that shape
  (attempt 1 died on the account's spend limit, attempt 2 redid the work
  from scratch) two entries up. Fixed rather than left standing: PRD
  `status: draft → designed`, `decided:` stamped to the G1 timestamp.

  **No project worktree existed on this host to design against.**
  `agents/eng-manager/config/projects.md` states "all five worktrees
  already exist," true only for the 2026-08-23 Mac verification — this is
  the first pass on the Windows port to actually need one.
  `$ENG_WORKTREES` (`C:/Users/jerryai/Documents/_eng`, per `lib/eng-env.sh`)
  existed as a bare directory but held none of the five. Created
  `aiorders-api`'s with the same commands `lib/eng-setup.sh` itself runs
  (`git worktree add -b eng/base`, from the human's clean, up-to-date
  `main` checkout — never touched that checkout directly) rather than
  running the full setup script, since only this one project was needed
  this pass. Observation filed.

  **Design work done fresh against the live repo, not inferred from the
  PRD alone** — same discipline `ENG-006` set at this identical state.
  `git fetch origin`; worktree clean. Found this repo's schema is now
  actually tracked in git (`supabase/migrations/`, 21 files) — corrects
  `ENG-006`'s own design doc, which found none; that gap closed with
  commit `5b3bac2` ("Consolidate remaining migrations from
  aiorders-admin-hub"), one commit before `ENG-006`'s own, so `ENG-006`'s
  finding was accurate when written and is now stale. Read the real
  migrations rather than reverse-engineering from edge-function code:
  confirmed `restaurants.id` is `uuid`, found the existing shared
  `update_updated_at_column()` trigger and the `restaurant_activations`
  table as the closest structural precedent (service-role-only RLS,
  trigger-maintained `updated_at`, one index on `restaurant_id`) — this
  design follows the same shape. Confirmed `admin-portal`'s existing
  role-gated auth middleware and path-router as the natural home for
  requirement 9's internal write path, avoiding new auth machinery for a
  ticket with no frontend, same reasoning `ENG-006` used to prefer native
  OTP over hand-rolling one.

  **Significant unplanned finding: a live third-party loyalty vendor
  (Walletly) is already integrated** — `external-integrations/handlers/walletly.ts`,
  catalogued in the repo's own `README.md`, last touched 2026-07-07 (seven
  weeks before this sequence was requested, not dead code). Neither the
  approver's original request nor `knowledge/business-profile.md` mentions
  it. Full reasoning on the design doc's own One-way doors section — in
  short: `ENG-007` itself carries no risk from this (additive, nothing
  calls it, trivially dropped), but ticket 3 (the points ledger) is where a
  second real points-tracking system would start running in production
  alongside Walletly's, and unwinding that after adoption is a data-migration
  problem, not a schema change. Deliberately not guessed at — three
  materially different readings (legacy/mid-deprecation, per-brand add-on
  coexisting fine, or the thing the approver actually meant) are all
  consistent with what's on disk, and nothing here resolves which.
  **Escalated rather than decided**, same bar `ENG-006`'s own G2 set (real
  stakes, no way to resolve it from the repo alone): raised
  `inbox/2026-08-29-eng007-g2-walletly-conflict.md` (`agent: eng-manager`,
  `gate: one-way-door`), recommending proceeding with `ENG-007` itself now
  (no dependency on the answer) while holding ticket 3 until it's
  answered. Ran `lib/eng-notify.sh raise` (logged the plain
  `SLACK_WEBHOOK_URL unset` failure noted above); stamped `notified:
  2026-08-29T07:53:00` by hand, per this instance's established practice
  when the script can't confirm its own delivery.

  **The rest of the design is fully specified and ready to build the
  moment this is answered** — one new table
  (`restaurant_loyalty_configs`), open-ended effective-dating (no
  `effective_to` column, so a rate change stays a pure insert per PRD
  requirement 6), a `before insert` trigger using a per-restaurant advisory
  lock to enforce future-only, strictly-increasing `effective_from` values
  — closing the PRD's own "concurrent writes" risk at the database rather
  than the application — and a new `admin-portal/handlers/loyalty-config.ts`
  reusing the existing admin/sub-admin auth gate. Full detail:
  `agents/architect/designs/ENG-007-per-restaurant-loyalty-configuration.md`.

  **2 transitions this pass** (`awaiting-scope → designed → awaiting-decision`),
  well under the cap of 4 — the next state needs the approver, so this
  pass stops here by design. `machine_wip` unaffected (neither state sits
  in the counted `ready`..`ready-to-ship` range). Approver-facing WIP and
  approval cap both net unchanged at 1/2 and 1/3 — this ticket's G1 closed
  and its G2 opened in the same pass, same shape as `ENG-006`'s identical
  transition.

  **Caps checked fresh before raising the G2**, not trusted from the board
  header: `wip.approver_limit` (2) was 1/2 (this ticket's own now-closed
  G1); `wip.approval_cap` (3) was 1/3 (same). Raising G2 on the same
  ticket as its G1 closes is a net-zero move on both, confirmed rather
  than assumed.

  **Dead-end sweep (scoped to this event, per its own contract):** this
  ticket's log now ends in a valid, accounted-for state with the chain
  record below. No other ticket is in flight to check —
  `agents/product-manager/inbox/` and `agents/eng-manager/inbox/` held only
  `.gitkeep`/already-`_handled/` entries; `inbox/requests/` was empty;
  `inbox/`'s only other item (`2026-08-28-eng-events-dropped.md`) is
  unchanged, still non-P0, still deliberately not retried per established
  precedent.

  **Notify sweep:** this pass's own G2 raised and stamped above. Nothing
  else to nudge — the events-dropped item carries no `notified:` at all
  (never successfully sent, same established gap) so the 24h-since-notified
  nudge rule doesn't apply to it. Approval cap 1/3, not full — no stall.

  **Observations filed** (`observations.md`): the missing Windows-host
  worktree and the fix; the now-tracked migration history correcting
  `ENG-006`'s design doc; the Walletly discovery, cross-referenced for
  whoever files ticket 3 next; today's `eng-notify.sh` failure signature
  (`SLACK_WEBHOOK_URL unset`) as the plain face of the already-open
  channel-dispatch proposal, not a new bug.

  **Correction filed** (`agents/eng-manager/config/projects.md`): the
  "all five worktrees already exist" claim is host-specific and was going
  stale silently; added a note rather than rewriting the table.

  `chained: none` — `awaiting-decision` (G2), waiting on the approver; the
  chaining guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
  whole-board: both run clean.

- `2026-08-29` `awaiting-decision → ready` (eng-manager, `watch` event pass,
  context `schtasks`). A second, distinct `watch (schtasks)` fire from the one
  that reached `designed → awaiting-decision` above — day's hop counter read
  `4` at pass start (`traces/.hops-2026-08-29`), and `traces/eng-loop-2026-08-29.log`
  shows this fire queued behind, and launched immediately after, a separate
  `decision` pass (for this ticket's own G1 file, already fully processed —
  that pass correctly no-op'd and logged itself in `observations.md`). Mode
  check clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml`
  → `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-007`) and whole-board: both exit 0, clean.

  **Swept all three watched inboxes fresh, per the event's own contract.**
  `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
  `inbox/requests/` held nothing new. `inbox/`'s other item
  (`2026-08-28-eng-events-dropped.md`) is unchanged, still non-P0, still the
  established never-successfully-notified gap — not acted on, per precedent.

  **`inbox/2026-08-29-eng007-g2-walletly-conflict.md` had been answered since
  the previous pass raised it** — `decision: approved`, `decided:
  2026-08-29T08:10:30.599034+00:00`, a hand-edit rather than a reply through
  `lib/eng-notify.sh` (consistent with every gate answer on this instance but
  `ENG-002`'s merge). Verified fresh rather than trusted at face value: re-read
  the file directly during this pass rather than relying on the earlier read
  from minutes prior, confirmed `traces/.pending` held a `decision
  2026-08-29-eng007-g2-walletly-conflict.md` line still queued behind this
  fire (not yet drained), and confirmed no second live process was mutating
  the same file concurrently. Processed here, in this `watch` pass, rather
  than left for that queued `decision` event — this is exactly the class of
  thing this event's own contract exists to catch ("a gate item edited by
  hand"), and per this instance's established practice the fact gets handled
  by whichever event reaches it first; the queued `decision` event will very
  likely no-op when it drains next, the mirror image of this same ticket's G1
  a few minutes earlier where `decision` drained first and the trailing
  `watch` found nothing left to do.

  **Read as answering option 1 of the three the gate offered**: "Walletly is
  being retired/replaced" — the native loyalty sequence is the intended
  replacement, proceed exactly as originally scoped. No boundary-setting
  reply needed (that was only called for under option 2), and no rider beyond
  the one-line answer. This settles the question before ticket 3 (the points
  ledger) is filed: no dual-system conflict to design around, so ticket 3
  proceeds as `ENG-006`'s G1 already scoped it once the sequence's
  auto-continuation (`skills/acceptance-check/SKILL.md` step 6b) files it
  after this ticket verifies. Moved
  `inbox/2026-08-29-eng007-g2-walletly-conflict.md` → `inbox/_handled/` with a
  processed footer; journaled in
  `agents/eng-manager/config/decision-journal.md`.

  **Architect's design doc left as-is, deliberately** — same precedent
  `ENG-006`'s own design doc set (its `one_way_doors` note still reads
  "escalated rather than decided here" today, unedited after that gate
  resolved). The design doc is a point-in-time artifact from the `designed`
  state; the resolution lives in this ticket's own log and the decision
  journal, which is what the next hop and any future ticket-3 design work
  actually read.

  **1 transition this pass** (`awaiting-decision → ready`), well under the cap
  of 4 — `ready`'s own exit condition (work broken down, sequenced, assigned;
  WIP slot available) is satisfied by this gate closing with nothing else in
  flight to sequence against, but `building` needs a different owning role
  (backend/database, per `definition-of-done.md`) actually writing code, which
  is new implementation work and this pass's stopping point by design
  (`config.yaml` → `build_loop.stop_at`). **Consequence:** approver-facing WIP
  1/2 → 0/2; approval cap 1/3 → 0/3 (this was the cap's only open item); machine
  WIP 0/6 → 1/6 — `ready` is the first state in the counted range, so this is
  the first ticket to enter it on this instance's Windows host.

  **Dead-end sweep:** no other ticket in flight. **Inbox sweep was not
  actually clean, corrected here rather than left standing:** five new files
  landed in `agents/product-manager/inbox/` mid-pass (`source: approver`,
  `via: control-center`, received 08:14–08:22) — after this pass's own
  initial three-inbox sweep had already found that directory empty. Read all
  five (UX/functionality gaps: admin-panel influencer board and brand
  stage/health filtering, the FoodSwipe sales-funnel pipeline stages, brand
  portal QR/media/site-timing self-service, admin-portal readiness for
  agency/reseller users) before deciding not to act — none meets the P0 bar,
  so none interrupts. Left for their own dedicated `intake` events (four
  already visible queued in `traces/.pending`; the fifth landed after that
  read and will get its own fire) rather than shaped here — full PM readback
  and G1 for five unrelated requests is `intake`'s own job under this
  pass-type's narrower contract, not `watch`'s, and would also blow past the
  approver-facing WIP cap of 2 if attempted in one pass regardless. Observation
  filed (`observations.md`). **Notify sweep:** nothing raised this pass (a
  gate closing doesn't get re-notified); nothing to nudge; approval cap just
  cleared to 0/3 — no stall.

  `chained: ENG-007` — `ready` is an agent-owned state (eng-manager sequenced
  it; the next hop is a backend/database engineer actually building), not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-007`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-007`) and whole-board: both run clean.

- `2026-08-29` `ready → building → in-review → in-security → ready-to-ship`
  (backend/database, then principal-engineer + qa combined, then security,
  then devops — `continue` event pass, context `ENG-007`). Narrow scope per
  the event's own contract (resume this ticket from its current state; no
  board-wide sweep). Mode check clean (business-os `.env` → `MODE=` empty;
  instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
  whole-board: both exit 0, clean.

  **Recovered a fully unrecorded build — the same failure family `ENG-006`
  named first, one step further along.** This ticket's own frontmatter and
  log still read `ready` at pass start, but four complete, dated,
  cross-consistent gate artifacts already existed on disk, all referencing
  the same commit:
  `agents/database/migrations/ENG-007-per-restaurant-loyalty-configuration.md`
  (verdict: pass, named gap),
  `agents/principal-engineer/reviews/ENG-007.md` (verdict: PASS, `diff:
  loyalty-system (2aec86f) vs origin/main`), `agents/qa/test-plans/ENG-007.md`
  (verdict: pass, 44/44), `agents/security/reviews/ENG-007.md` (verdict:
  PASS, same diff reference). Unlike `ENG-006`'s own recovery (uncommitted
  code, no receipts written yet), here the code was committed, pushed, and
  every downstream gate had already run to completion and written its
  receipt — only this ticket's own state/log bookkeeping hadn't caught up.
  Consistent with a pass that did the real work and crashed or was cut off
  after the last receipt write but before touching the board file.

  **Verified fresh rather than trusted, before recording anything.** `git
  branch -vv` in the `aiorders-api` worktree: `loyalty-system` at `2aec86f`,
  `[origin/loyalty-system]`, tree clean — matches every receipt's own
  `diff:` line exactly. `git merge-base --is-ancestor 2aec86f origin/main` →
  not an ancestor: not yet merged. `gh pr list --head loyalty-system --state
  all` (run inside the `aiorders-api` worktree) → only `ENG-006`'s own
  already-merged PR #2; nothing open for this commit — confirms no L1 merge
  request has been raised yet, so `ready-to-ship` (not `blocked`) is
  genuinely where this pass stops. Independently re-ran the verification the
  receipts claim rather than taking the documents' word for it: `deno test
  --allow-env loyalty-config.test.ts` → 44 passed, 0 failed; `deno check
  loyalty-config.ts loyalty-config.test.ts` → clean; `deno lint` → clean, 0
  problems — matches both the code review's and the QA plan's own claimed
  results exactly, a third independent reproduction of the same result.
  `deno` itself is now real on this host (`2.9.6`, `npm`-installed) — the
  database doc's own "attempted `npm install -g deno` as a fallback...
  outcome recorded alongside whatever it produced" resolved successfully;
  observation filed below. Docker Desktop still does not come up (`docker
  info`, bounded 8s wait, timed out) — the same gap the migration doc
  already named, not re-litigated, no further budget spent chasing it.

  **State recorded to match the verified reality**, `building → in-review`
  folding in `in-qa` per `config.yaml`'s own `combined_hop: [code_review,
  quality]` (no separate sit-state, same as `ENG-005`/`ENG-006`): `branch:
  loyalty-system`; `links.review`, `links.test_plan`, `links.security_review`
  all set to the receipts above.

  **`ready-to-ship` (devops role) — genuine new work this pass, not just
  bookkeeping**, since none of the four existing receipts is release-readiness
  itself:
  - **Migration gate**: already cleared — the database doc's own verdict
    ("pass, with a named verification gap") stands, re-confirmed above rather
    than re-derived.
  - **Release plan**: purely additive — one new table, one new `admin-portal`
    route. No frontend anywhere in this sequence calls it (explicit PRD
    non-goal, same as `ENG-006`), so merging and deploying has no live
    behavioral effect until a caller exists — the same "zero blast radius
    until something calls it" shape `ENG-006`'s own `ready-to-ship` used.
  - **Rollback**: migration rollback SQL written and reasoned through (not
    live-tested — the named gap, carried forward, not closed here); the route
    itself reverts trivially — the 2-line `index.ts` addition and the new
    handler/test files, nothing else touched.
  - **Observability**: every unexpected-error branch logs server-side via
    `console.error` before responding (confirmed directly in the code
    review's automatic-failure #2 disposition), surfaced through Supabase's
    existing function logs — no new observability mechanism needed, same one
    every other function in this repo already relies on.
  - **Cost**: **$0/month delta** — same Supabase project, one new empty
    table, no new service, no new vendor.
  - **Release window checked for completeness, deliberately not acted on
    this pass** — the same split `ENG-006` used at this identical boundary
    ("re-checked fresh by whichever session actually opens the PR, since
    that's a later hop"): `date` → Saturday 2026-08-29, 05:56 local, inside
    `releases.block_weekends`; no `ENG_RELEASE_FREEZE` in business-os
    `.env`; instance `config/config.yaml` carries no override. Flagged here
    so the next hop doesn't have to rediscover it, not decided here —
    opening the PR is real, distinct devops work for that hop, same as
    `ENG-006`'s own precedent at this exact boundary.

  **4 transitions this pass** (`ready→building`, `building→in-review`,
  `in-review→in-security`, `in-security→ready-to-ship`), at the cap of 4 —
  same count, same stopping point as `ENG-006`'s own recovery pass through
  this identical sequence. `machine_wip` unaffected — `ENG-007` was already
  inside the counted `ready..ready-to-ship` range at `ready`, stays inside it
  at `ready-to-ship` (still 4/6). Approver-facing WIP and approval cap both
  unaffected — no gate raised this pass; the merge request is the next hop's
  work.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for state with the chain record below. No sweep of the
  rest of the board — out of scope for a `continue` event naming this ticket
  specifically.

  **Notify sweep:** nothing raised this pass — a state recorded to match
  already-completed work doesn't get its own notification, and the merge
  request (next hop) is what will actually need the approver's attention.

  **Observations filed** (`observations.md`): (1) this recovery's own
  shape — a full receipt set (build, review, QA, security) written and
  internally consistent while only the board ticket's own state/log lagged,
  a further-along variant of the partially-updated-artifact family `ENG-006`
  first named; (2) `deno` is now genuinely installed and working on this
  Windows host (`2.9.6`, via `npm install -g deno`), closing a gap the
  database migration doc left open as an in-progress attempt — future passes
  on this host can use it directly rather than reaching for Docker first;
  (3) Docker Desktop still does not come up within a bounded wait, second
  occurrence.

  `chained: ENG-007` — `ready-to-ship` is a devops-owned state, not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-007`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-007`) and whole-board: both run clean.

- `2026-08-29` (no-op — held at `ready-to-ship`) `continue ENG-007` event
  pass, context `ENG-007` — the chain fire from the immediately preceding
  entry. Narrow scope per the event's own contract (resume this ticket from
  its current state; no board-wide sweep). Mode check clean (business-os
  `.env` → `MODE=` empty; instance `config/config.yaml` → `mode:` empty,
  both fall through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-007`) and whole-board: both exit 0, clean.

  **Verified fresh rather than trusted, given this ticket's own history of
  being further along than its log** (both prior recoveries, above). In the
  `aiorders-api` worktree: `git fetch origin`; `git branch -vv` shows
  `loyalty-system` at `2aec86f`, `[origin/loyalty-system]`, tree clean —
  matches every existing gate receipt exactly, nothing moved since the last
  entry. `git merge-base --is-ancestor origin/loyalty-system origin/main` →
  not an ancestor: still not merged. `gh pr list --head loyalty-system
  --state all` → only `ENG-006`'s own already-merged PR #2; nothing open
  against this commit — no L1 merge request exists yet, confirming
  `ready-to-ship` (not `blocked`) is genuinely still where this sits, not a
  third unrecorded advance.

  **Release window re-checked fresh, as this ticket's own prior entry
  explicitly asked the next hop to do, same boundary `ENG-006` hit once
  already.** `date` → **Saturday 2026-08-29, 14:09 local** —
  `config.yaml` → `releases.block_weekends: true`. Unlike `ENG-006`'s
  identical check (Friday, 14:40 PDT, *before* the 15:00 cutoff — inside the
  window, proceeded), this lands squarely inside a blocked weekend. This
  department's own established reading of this boundary, set by `ENG-006`'s
  precedent and restated by this ticket's own preceding log entry, treats
  **opening the PR itself** as the release-window-gated action, not just the
  eventual merge — so the fact that `aiorders-api` has no CI/CD and a human
  merge is required regardless does not exempt the PR-open step. This
  pass's own prompt independently confirms the same reading, naming "a
  closed release window" alongside "the approver" as a condition under which
  the next hop must not be chained.

  **No PR opened, no state change.** The only remaining action at
  `ready-to-ship` — raising the L1 merge request — is exactly the action the
  window blocks; nothing else is available to do here without either
  crossing that guard or inventing work. Ticket holds at `ready-to-ship`,
  `owner: devops`, unchanged.

  **0 transitions.** No cap affected either way. `board/_index.md`'s cached
  header still reads "Machine WIP 6... 6/6, at cap" (`ENG-007`/`ENG-011` at
  `ready-to-ship`, `ENG-008`/`ENG-009`/`ENG-010` at `ready`, `ENG-013` at
  `building`), but per this instance's own observations.md (`continue
  ENG-013` row, same day) the real limit on disk is already `12`
  (`instances/aiorders/engineering/config/config.yaml`'s uncommitted
  `wip.machine_limit: 6 → 12`, matching the corrected `max_5x` tier) — so the
  honest count is **6/12**, not at cap, though still uncommitted and not
  this ticket's own change to make. Not load-bearing for this ticket either
  way, since what's holding it is the release window, not machine WIP.
  Approver-facing WIP and approval cap both unaffected — no gate raised.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for state with the chain record below. No sweep of the
  rest of the board — out of scope for a `continue` event naming this ticket
  specifically.

  **Notify sweep:** nothing raised this pass — a hold with nothing new to
  decide doesn't get a notification of its own; the merge request (still
  pending) is what will actually need the approver, once it can legally be
  raised.

  **Observation filed** (`observations.md`): this is the first time
  `releases.block_weekends` has actually held a ticket back on this
  instance — every prior `ready-to-ship`→PR-open on this board (`ENG-002`,
  `ENG-004`, `ENG-005`, `ENG-006`) landed inside the window on a weekday.
  Worth a record as the guard's first real activation, not its first
  mention.

  `chained: none` — release window closed (Saturday; `releases.block_weekends`),
  per this pass's own instructions naming "a closed release window" as a
  chaining exclusion alongside the approver. Resume is expected to happen
  naturally: the next scheduled safety-net pass (or a fresh `continue
  ENG-007` fire) that lands once the window reopens Monday will find this
  same state and proceed to open the PR, per `eng_build_loop.md`'s own "the
  Friday 15:30 pass therefore never releases; it advances everything else
  and leaves the release for Monday." Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
  whole-board: both run clean.
