---
id: ENG-007
title: Per-restaurant loyalty configuration — earn rates and redemption value
project: aiorders-api
type: feature
size: S
severity: P3
priority:
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-28
updated: 2026-08-28
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-007-per-restaurant-loyalty-configuration.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
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
