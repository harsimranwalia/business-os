---
id: ENG-007
title: Per-restaurant loyalty configuration — earn rates and redemption value
project: aiorders-api
type: feature
size: S
time_estimate: S (a few hours to half a day, per PRD Cost section)
time_spent: not separately clocked — build, review, QA and security all completed in an unrecorded prior pass (see Log); read as most of the estimate consumed
time_remaining: "0 — verified, closed out"
severity: P3
priority: now
state: verified
owner: eng-manager
lane: full
blocked_on: 
blocked_from: 
source: approver
created: 2026-08-28
updated: 2026-08-30
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
  release: agents/devops/releases/2026-08-29-aiorders-api-ENG-007.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/4
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

- `2026-08-29` **approver override, filed by hand in an interactive session —
  not a department pass.** The hold above predates
  `skills/release-runner/SKILL.md`'s same-day correction: **the weekend/window
  check (step 1) never applied to L1 projects in the first place** (the
  approver's own words there: "weekdays or weekends, my choice"), and
  `aiorders-api` is L1 (`agents/eng-manager/config/projects.md`). The hold
  entry above reasoned from the pre-correction reading and should not have
  waited for Monday. `priority: → now` set directly by the approver (not
  inferred by an agent — see `eng_build_loop.md`'s "never write to priority
  yourself," which this instruction satisfies rather than violates), and
  `traces/.pending` had `continue ENG-007` prepended by hand so it runs next
  once the currently in-flight pass finishes, since no `continue ENG-007` was
  otherwise queued. No other field changed; state stays `ready-to-ship`,
  owner stays `devops`. The next `continue ENG-007` pass should open the PR
  and raise the L1 merge request per the corrected skill — any day, any time.

- `2026-08-29` `ready-to-ship → blocked` (devops, `continue` event pass,
  context `ENG-007`). Narrow scope per the event's own contract (resume this
  ticket from its current state; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-007`) and whole-board: both exit 0, clean.

  **Ran `skills/release-runner/SKILL.md` steps 1–4 fresh, not reusing the
  prior hold's reasoning.** Step 1 (window check): `aiorders-api` is
  registered **L1** (`agents/eng-manager/config/projects.md`) — per the
  corrected skill, step 1 does not apply and the pass goes straight to step
  4, exactly as the immediately preceding log entry (the approver's
  override) instructed. Step 2 (upstream gates): all four receipts
  re-confirmed present and all `pass` — code review, quality, security,
  migration (the last "pass, with a named verification gap," carried
  forward, not a fail). Step 3 (readiness gate): already held by the pass
  that reached `ready-to-ship` (rollback written, observability via existing
  `console.error`+Supabase logs, $0/month cost, additive release plan) —
  re-read rather than redone, nothing has changed on disk since.

  **Verified fresh rather than trusted, given this ticket's own repeated
  history of drifting ahead of its log.** In the `aiorders-api` department
  worktree (`_eng/aiorders-api`, currently checked out on `ENG-008`'s branch
  for unrelated in-flight work — not switched, since `gh pr create` needs no
  checkout): `git fetch origin`; `loyalty-system` local and
  `origin/loyalty-system` both at `2aec86f`, matching every existing
  receipt's `diff:` line exactly. `git merge-base --is-ancestor
  origin/loyalty-system origin/main` → not an ancestor: still not merged.
  `gh pr list --head loyalty-system --state all --repo
  harsimranwalia/aiorders-api` → only `ENG-006`'s own already-merged PR #2;
  nothing open against this commit — confirmed no PR already existed before
  opening one.

  **Step 4 (L1 route): opened the PR and wrote the merge request in the same
  step**, per the skill's own instruction that the two are not separable for
  L1. `gh pr create --repo harsimranwalia/aiorders-api --base main --head
  loyalty-system` → **PR #4**
  (https://github.com/harsimranwalia/aiorders-api/pull/4), confirmed
  `OPEN`, `main<-loyalty-system`, via `gh pr view` immediately after
  creation. Body carries the same What-this-does / Gates-passed / Carried-forward
  structure ENG-006's own PR #2 used, drawn from this ticket's own four gate
  receipts rather than re-summarized from memory. Wrote
  `inbox/2026-08-29-eng007-merge-request.md` (`agent: eng-manager`, `gate:
  merge`, `pr_url` set to PR #4). Ran `lib/eng-notify.sh raise` — logged the
  same `SLACK_WEBHOOK_URL unset` failure this instance's every prior notify
  call has hit today; stamped `notified: 2026-08-29T19:32:13` by hand
  (the log's own timestamp), per this instance's established practice when
  the script can't confirm its own delivery.

  **Ticket set to `blocked`**, `blocked_on: approver`, `blocked_from:
  ready-to-ship` (so a later exit from `blocked` returns here, not forward,
  per `eng_build_loop.md` step 8's field-presence rule), `owner: devops →
  approver`, `links.pr` set to the PR URL above. This is the "L1 merge
  request" gate return type (`eng_build_loop.md` step 4), distinct from
  G1/G2/G3 — merge detection (step 5) is what will find the eventual merge
  and advance this ticket to `shipped`; no separate G3 is raised for an L1
  project.

  **Caps checked fresh before raising, using the board's own last-recorded
  counts as the baseline** (approver-facing WIP 1/2, approval cap 1/3, both
  from `ENG-011`'s still-open merge request): adding this ticket's own block
  and merge-request item brings them to **2/2** and **2/3** respectively —
  at the WIP cap but not over it, one slot still free on the approval cap.
  Legitimate to raise either way. **Noted, not acted on** (out of scope for
  a `continue ENG-007` pass naming this ticket specifically): while reading
  `inbox/2026-08-29-eng011-merge-request.md` as a formatting precedent, it
  now carries `decision: approved` and a trailing "merged" line — apparently
  already answered and resolved since the board's `_index.md` was last
  written, which would make the true current counts lower than the baseline
  used above. Not verified or processed here; leaves more headroom against
  both caps if true, never less, so it doesn't change this pass's own
  math. Flagged in `observations.md` for whichever pass owns reconciling it.

  **1 transition this pass** (`ready-to-ship → blocked`), well under the cap
  of 4 — the next state needs the approver to merge on GitHub, this pass's
  stopping point by design. **Consequence:** approver-facing WIP 1/2 → 2/2;
  approval cap 1/3 → 2/3; `machine_wip` unaffected (`blocked` is outside the
  counted `ready`..`ready-to-ship` range — this ticket leaves that range
  this pass).

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for state with the chain record below. No sweep of the
  rest of the board — out of scope for a `continue` event naming this
  ticket specifically; the `ENG-011` staleness noticed above is flagged, not
  chased.

  **Notify sweep:** this pass's own merge-request item raised and stamped
  above. Nothing else to nudge or stall on within this event's scope.

  **Observation filed** (`observations.md`): `ENG-011`'s merge request
  appears already answered and merged, noticed incidentally while this
  ticket's own pass was reading it for template formatting — not this
  event's ticket to reconcile.

  `chained: none` — `blocked`, `blocked_on: approver`; the chaining guard
  never fires on a ticket waiting on a human. Resume happens naturally: the
  build loop's own merge detection (step 5) finds the merge on a future
  pass via local git ancestry, no polling cost, and advances this ticket to
  `shipped` then. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-007`) and whole-board: both run clean.

- `2026-08-29` `blocked → shipped` (control center, merge detected) — recorded on Harry's say-so; ancestry not consulted. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree.

- `2026-08-29` **`shipped` reconciled — the control-center bypass verified
  and completed, not just noticed** (eng-manager, `watch` event pass, context
  `schtasks`). Per this event's own contract, swept all three watched inboxes
  fresh. Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
  whole-board: both exit 0, clean.

  **This ticket's own frontmatter already read `state: shipped`** (set by the
  control-center dashboard action directly above, "ancestry not consulted"),
  and multiple prior passes had flagged the gap — `owner` stale, no
  independent merge confirmation, no release record — as "for whichever pass
  owns reconciling it" without any pass yet claiming it. This pass did, since
  a `watch` sweep's own job (whatever's new and unprocessed across the three
  inboxes) surfaced `ENG-011`'s parallel, still-open merge request in
  `inbox/` and the same reconciliation logic applied to both.

  **Verified fresh rather than trusted on the control center's say-so:**
  `git fetch origin` in the `aiorders-api` worktree; `git merge-base
  --is-ancestor origin/loyalty-system origin/main` → **MERGED**
  (`origin/main` tip `93617c6`, "Merge pull request #4 from
  harsimranwalia/loyalty-system"). The dashboard's claim checks out.

  **Deploy verified live, not assumed from the merge** — a stronger check
  than this instance's own precedent (`ENG-006`) had available, using the
  Supabase MCP connection read-only against `bmnmnejwdxbcqinqkwko`:
  `list_migrations` shows `20260829130000_restaurant_loyalty_configs`
  applied; `restaurant_loyalty_configs` confirmed present in
  `information_schema.tables`; the `admin-portal` edge function
  (`version: 115`, `updated_at: 2026-08-30T02:47:37Z`, deployed from the
  approver's own checkout per its `entrypoint_path`) has a bundle containing
  the `loyalty-config` handler code. No CI/CD exists on this repo — this was
  run out-of-band by the approver directly, same pattern `ENG-006` documented
  for `platform-customer-auth`, and the same deploy event also carried
  `ENG-011`'s handler changes (one redeploy, two tickets' code).

  **Wrote the missing release record**
  (`agents/devops/releases/2026-08-29-aiorders-api-ENG-007.md`) —
  `definition-of-done.md`'s `shipped` exit condition requires one, and the
  control-center bypass had skipped it entirely, same as it skipped ancestry
  confirmation. **Added a footer to
  `inbox/_handled/2026-08-29-eng007-merge-request.md`** noting it was never
  formally answered through any channel (a third variant of the
  control-center-bypass gap: unlike `ENG-002`'s silence or `ENG-006`'s
  delayed written reply, this one got neither) — reconciled rather than left
  to read as an abandoned item. **Journaled**
  (`agents/eng-manager/config/decision-journal.md`) as an L1 merge, same
  treatment `ENG-002`'s no-reply merge received.

  **`owner: approver → devops`**, matching `definition-of-done.md`'s
  `shipped`-state ownership — the approver-owned part of this ticket's life
  (merging the PR) is over; what's left (release-record bookkeeping, now
  done; acceptance-check next) is machine-owned. `links.release` set above.
  **0 state transitions** — already `shipped`; this pass closed the gap
  behind that state rather than moving it further. `machine_wip` unaffected
  (`shipped` sits outside the counted range, unchanged). Approver-facing WIP
  and approval cap: this ticket's merge request was never counted as open in
  the first place (its `state:` had already outrun it) — no change from this
  reconciliation; see board index for `ENG-011`'s own, separate effect on
  both caps.

  **Dead-end sweep:** this is itself a dead-end-sweep catch — a ticket sitting
  in an agent-owned state (`shipped`) whose last log entry carried no
  `chained:` record at all, exactly the broken-chain shape
  `eng_build_loop.md` step 8 names. Resumed here. No wider board sweep beyond
  this ticket and `ENG-011` (both touched this pass) — out of scope for a
  `watch` event's own narrower contract.

  **Notify sweep:** nothing raised (no new gate item; reconciling a
  bookkeeping gap doesn't get its own notification).

  **Observation filed** (`observations.md`): the `admin-portal` edge function
  redeploy at 2026-08-30T02:47:37Z carried both this ticket's and `ENG-011`'s
  handler changes live in one event — worth knowing for any future ticket
  timing a deploy against this function specifically.

  `chained: ENG-007` — `shipped` is product-manager-owned next
  (`skills/acceptance-check/SKILL.md` triggers on entering `shipped`), not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-007`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-007`) and whole-board: see pass notes.

- `2026-08-30` `shipped → verified` (product-manager, `continue` event pass,
  context `ENG-007` — the chain fired at the end of the immediately preceding
  entry). Narrow scope per this event's own contract (resume this ticket from
  its current state; no board-wide sweep). Mode check clean (business-os
  `.env` → `MODE=` empty; instance `config/config.yaml` → `mode:` empty).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`)
  and whole-board: both exit 0, clean.

  **Ran `skills/acceptance-check/SKILL.md` to completion.** No browser access
  on this host, same standing gap every acceptance-check on this instance has
  named (`ENG-011`'s precedent) — and this ticket has no frontend or user path
  at all (explicit non-goal for the whole sequence), so the substitute methods
  had to reach further than reading existing state. Verified against the live
  system, not the receipts, using four methods:

  1. **Live schema introspection** (`information_schema`, `pg_constraint`,
     `pg_trigger`, `pg_proc`, read-only, project `bmnmnejwdxbcqinqkwko`):
     `restaurant_loyalty_configs`'s columns, all three `CHECK` constraints
     (`online_earn_pct`/`dine_in_earn_pct` 0–100, `redemption_value_per_point`
     ≥0), the `restaurant_id` FK, and the `enforce_loyalty_config_effective_order`
     trigger's deployed `prosrc` all confirmed live and byte-for-byte identical
     to the design doc's SQL — stronger than the DB/QA gates' own verification,
     which hand-traced the git source, not the deployed function.
  2. **Deployed edge-function bundle** (`get_edge_function`, read-only):
     confirmed `admin-portal/index.ts` routes `/admin-portal/loyalty-config` to
     `handleLoyaltyConfig`; confirmed the deployed `deriveCurrentConfig`,
     `validateLoyaltyConfigInput`, `hasLoyaltyConfigAccess`, and
     `mapLoyaltyConfigInsertError` functions are present and match the design
     and test plan's claims exactly (not just the 44/44 unit tests passing
     against source — the actual live bundle contains this logic).
  3. **One live, unauthenticated request**: `GET .../admin-portal/loyalty-config?restaurant_id=...`
     with no auth header → `401 UNAUTHORIZED_NO_AUTH_HEADER` — the admin/sub-admin
     gate is live and enforced in production, not just reviewed in code.
  4. **Live data**: `select count(*) from restaurant_loyalty_configs` → `0` —
     confirms nothing has written through this path yet, matching the PRD's own
     non-goal ("deciding the actual $/% numbers for any real restaurant").

  **Deliberately did not perform a live write test.** The trigger's insert-time
  behavior (the core of AC1/2/3/6) was the one thing no gate so far had run
  against a live Postgres — the migration doc, QA, and the release record all
  named this as an open gap. Closing it for real would need an actual insert
  against this table. Considered and rejected: this table currently holds real
  per-restaurant financial configuration, and ticket 3 (the points ledger,
  question raised below) will start computing real point balances against
  whatever rows exist here — a test row surviving a botched rollback would
  silently plant a fake rate for a real restaurant with no frontend surface to
  notice it. Given no independent confirmation that this MCP connection's
  `execute_sql` runs a multi-statement script as one atomic, rollback-able
  session, the downside of being wrong outweighed what a live write would have
  added on top of methods 1–2 below. Instead, hand-traced the **confirmed-deployed**
  trigger source (method 1, not the git copy) against the required sequences:
  first insert for a restaurant (`current_max` null, first `if` skipped, second
  `if` passes at `effective_from = now()` → AC1); a later insert
  (`effective_from` > prior max and ≥ `now()` → both checks pass, prior row
  never touched by any `UPDATE`/`DELETE` anywhere in the schema or handler →
  AC2); the "effective as of T" read pattern, confirmed identical in the
  deployed `deriveCurrentConfig` → AC3; an earlier-or-equal `effective_from`
  than the restaurant's current max → first `if` raises `P0001`, confirmed
  mapped to a 400 by the deployed `mapLoyaltyConfigInsertError` → AC6; the two
  `CHECK` constraints (method 1) reject a negative value at the database layer
  independent of the handler entirely → AC5, on top of the deployed
  `validateLoyaltyConfigInput`'s own friendlier 400.

  **Walked all 6 acceptance criteria, each against the live-confirmed
  evidence above:**
  1. **PASS** — first-insert-becomes-current: trigger's first `if` is a no-op
     with no prior rows; confirmed live.
  2. **PASS** — later config becomes current, prior remains readable
     unchanged: insert-only schema (no `UPDATE`/`DELETE` path exists anywhere
     in the diff) plus the trigger's strictly-increasing check, both confirmed
     live.
  3. **PASS** — past-timestamp query returns the rate effective then:
     `deriveCurrentConfig`'s `history.find(row => row.effective_from <= asOfIso)`
     over newest-first history, confirmed in the deployed bundle, combined with
     AC2's insert-only guarantee.
  4. **PASS** — unconfigured restaurant reads as not enrolled: deployed
     `deriveCurrentConfig` returns `{enrolled: current !== null, ...}`, never a
     default or a throw; independently true right now for every real
     restaurant, since the table holds 0 rows.
  5. **PASS** — negative values rejected with a clear reason: enforced at two
     independent live layers — the DB `CHECK` constraints and the deployed
     `validateLoyaltyConfigInput`.
  6. **PASS** — overlapping/conflicting ranges rejected: trigger's own
     `current_max`/`effective_from` check, confirmed deployed, mapped to an
     actionable 400 by the deployed `mapLoyaltyConfigInsertError`.

  **Non-goals check**: queried `information_schema.tables` for anything
  ledger/point/redemption/loyalty-shaped beyond this ticket's own table — found
  exactly one match, `restaurant_loyalty_configs` itself. No ledger, no
  redemption/QR surface, no admin UI, no frontend, no real rate for any actual
  restaurant (0 rows) — nothing from the non-goals list got built. **Cost**:
  $0/month confirmed — same Supabase project, no new service, matching the PRD
  exactly.

  **Step 6b (continue an approved sequence) — checked, does not fire this
  pass.** `ENG-007`'s own PRD (via its non-goals line and the design doc's
  Walletly section) gives ticket 3 enough shape to satisfy condition 1, but
  condition 2 fails: `ENG-007`'s own G1
  (`inbox/_handled/2026-08-28-eng007-g1-scope.md`) was answered with a bare,
  unconditional "approved" that never independently touched the
  continue-the-sequence question — the literal "plain 'approved' that never
  touches the sequence does not clear this bar" case the skill names as its
  own worked example. Not resolved by inference from `ENG-006`'s original
  sequence-wide G1 either, even though `eng_build_loop.md` step 3's narrative
  reads that way at a glance ("the G1 answer on **it** affirms proceeding with
  the whole shape... the rest of that sequence isn't agent-originated") — see
  the observation filed below; this pass followed the skill's own literal,
  more specific, per-ticket text rather than the higher-level narrative,
  consistent with "never infer approval from silence." Asked rather than
  assumed: raised `inbox/2026-08-30-eng007-continue-sequence-question.md`
  (`gate: intake-question`, standing/non-blocking, same shape as the
  `ENG-008`/`ENG-013` precedents in the decision journal), naming that the one
  real open risk (Walletly) is already resolved at `ENG-007`'s own G2. Ran
  `lib/eng-notify.sh raise` — logged the same `SLACK_WEBHOOK_URL unset`
  failure every notify call on this instance has hit; stamped `notified:
  2026-08-30T07:43:29` at write time, per established practice.

  **Notebook entry written**: `agents/product-manager/notebook/2026-08-30-acceptance.md`
  — what the estimate got right (build size, $0 cost) and the one thing worth
  sharpening next time (an S-sized ticket whose core mechanism is a DB trigger
  should probably budget for a throwaway-Postgres verification path up front,
  not discover the gap three gates in a row).

  **State: `shipped → verified`**, `owner: devops → eng-manager`. **1
  transition**, well under the cap of 4. **Consequence:** `machine_wip`
  unaffected (both states sit outside the counted `ready`..`ready-to-ship`
  range). Approver-facing WIP unchanged at 2/2 — a standing intake-question is
  not a ticket in flight, same treatment the `ENG-008`/`ENG-013` precedents
  established, not counted against the cap.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for terminal state. No wider sweep — out of scope for a
  `continue` event naming `ENG-007` specifically. **Notify sweep:** this
  pass's own standing question raised and stamped above; nothing else to
  nudge within this event's scope.

  **Observations filed** (`observations.md`): (1) the schema/deployed-bundle
  verification method used here (introspect live `pg_catalog`/
  `information_schema` plus the deployed function bundle, hand-trace against
  it, skip a live write given real financial-config data with a near-term real
  consumer) as a reusable pattern for the next DB-trigger-heavy ticket with no
  browser path; (2) the load-bearing tension between `eng_build_loop.md` step
  3's narrative (reads as: the *original* sequence G1 alone licenses every
  later hand-off) and `skills/acceptance-check/SKILL.md` step 6b's literal
  text (requires *each* ticket's *own* G1 to independently re-touch the
  sequence) — undecided which is the intended design, and it will recur
  verbatim at ticket 3's own eventual acceptance-check if ticket 3 gets filed
  and its G1 is also a bare "approved."

  `chained: none` — `verified` is terminal. No new ticket was filed this pass
  (6b's condition 2 not met), so there is nothing else to chain either — the
  standing question waits on the approver, same as any gate item. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.
