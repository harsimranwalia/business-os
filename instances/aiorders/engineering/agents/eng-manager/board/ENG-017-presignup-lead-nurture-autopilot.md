---
id: ENG-017
title: Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS
project: aiorders-api
type: feature
size: L
time_estimate: several days to a week
time_spent:
time_remaining:
severity: P2
priority:
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-017-presignup-lead-nurture-autopilot.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-29-no-autopilot-on-admin-panel-for-our-sales-staff-resellers-to.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T08:35:46.246211+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # no autopilot on admin panel for our sales staff/ resellers to use .
>
> how can we demonstrate to a client what we sell if we dont have it for
> us. have a proper fully demonstration account on how all aiorders work.
> also autopilot nurturing for resellers/sales/admin staff on admin panel
> which works based on stages update/ auto nurturing .

## Readback

See
`agents/product-manager/specs/ENG-017-presignup-lead-nurture-autopilot.md`
→ Readback — the full two-reading comparison and code evidence live there
rather than duplicated here.

## Problem

A website visitor who fills out AIOrders' own "become a client" form
becomes a `leads` row with no stage and no automated follow-up of any
kind — confirmed in code: no status column exists, and nothing ever
re-reads a lead to decide whether to contact it again. Whether it gets a
second touch depends entirely on a staff member remembering to.

## Outcome

A website lead carries a staff-settable stage; moving it to a stage
flagged for nurture (proposed: Contacted, Interested) automatically sends
a templated email/SMS, reusing the platform's existing send services. A
lead that has since signed up for real stops receiving nurture messages.

## Notes

**This request restates and broadens an ask the approver already
answered, under a different ticket, sitting unprocessed.**
`inbox/2026-08-29-eng013-presignup-leads-question.md` — `ENG-013`'s own
standing, non-blocking question (raised when its blind architect reading
independently guessed a pre-signup lead layer might be wanted) — carries
`decision: approved`, `decided: 2026-08-29T11:46:34.557123+00:00`,
verbatim: "Reading B. autopilot built to nurture these leads to next
stages autpmatically and send them emails/sms to nurture." That is
materially the same mechanism this new, separate inbox request asks for a
few hours later, more broadly ("resellers/sales/admin staff"). Treated as
**confirmed** evidence for this ticket's core mechanism — several
acceptance criteria above are marked `[confirmed]` on that basis rather
than `[inferred]` — but this ticket still owes its own G1, since it
broadens scope beyond what that question covered (the stage taxonomy, the
reseller non-goal, the consent-gap finding, and which trigger stages fire
nurture were never asked there).

**Deliberately not touched this pass, and named so the next pass doesn't
duplicate work:** `ENG-013`'s own standing-question gate item was not
processed, moved to `_handled/`, or journaled as `ENG-013`'s decision by
this pass — that item belongs to `ENG-013`'s own lifecycle, and acting on
it is out of scope for an `intake` event scoped to this different request.
Flagged in `observations.md` so that whichever `decision`/dead-end-sweep
pass next reaches that item points it at this ticket (`ENG-017`) instead
of shaping a redundant one.

**Evidence found, not assumed** — full detail in the PRD's Assumed/Risks
sections. Confirmed the `leads` table has no stage/status column and its
capture form (`aiorders-website/index.ts`) records no consent flag at all,
unlike the catering-request flow's explicit `consent_sms`/`consent_email`.
Confirmed the existing `autopilot`/`outgoing-communications` engine's
`communication_templates`/`trigger_type` model is hard-scoped to
`restaurant_id` and a closed set of customer-lifecycle triggers, so a
presignup lead (no restaurant, not a customer) cannot be enrolled through
it as-is — the reusable part is the underlying send services, not the
trigger/template data model. Confirmed `outgoing-communications`'s
`actor: 'admin'` route exists in the router but its three handlers are
unimplemented `TODO` stubs, not working prior art. Confirmed no mechanism
anywhere attributes a `leads` row to a specific reseller (`partner_id`,
referral code — none exist), which is why reseller access is proposed out
of this ticket rather than assumed in.

**Split from one raw request, not the whole of it.** The raw input bundles
two separable asks — this ticket is the autopilot-nurture half. The
demonstration-account half is `ENG-018`, filed in this same pass from the
same request.

**Project scoping.** Primary `aiorders-api` (the trigger/send engine is
the real build surface); `aiorders-admin-hub` is named and touched (the
stage control on the Leads page) rather than inventing a multi-project
ticket shape, same split precedent `ENG-003`/`ENG-008`/`ENG-011`/`ENG-013`/
`ENG-015` used.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped` (product-manager, `intake` event pass,
  context this exact request file). Per this event's own narrower
  contract, worked only this one request end to end — did not sweep the
  rest of `agents/product-manager/inbox/`.

  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket
  yet to scope to): exit 0, clean.

  **Caps verified fresh from `inbox/` directly before deciding how far to
  carry this ticket.** `ENG-014`'s and `ENG-015`'s G1s both still sit in
  `inbox/`, unanswered — approver-facing WIP substantively 2/2, at cap.
  `ENG-009`/`ENG-010`/`ENG-012`'s G1s and `ENG-013`'s presignup-leads
  question remain answered but unprocessed (unchanged, off the count per
  this board's established convention) — now a further consecutive pass
  without a `decision` event or dead-end sweep clearing them; re-flagged
  in `observations.md`, not fixed here, out of scope for this `intake`
  event.

  **Ran the full request-readback**
  (`skills/request-readback/SKILL.md`): this PM's own reading, grounded in
  live code across `aiorders-admin-hub` and `aiorders-api`, plus a blind
  architect reading (subagent, `opus`, raw request +
  `knowledge/business-profile.md` only, no repo access, no exposure to
  this PM's own reading). **No material divergence** — both independently
  read the raw request as two bundled asks and both independently named
  reseller/sales scoping as a real prerequisite; the architect's reading
  additionally, unprompted, raised CASL-style consent exposure, checked
  against the live lead-capture form and confirmed real (see PRD Assumed).

  **Investigated both live repos in depth before proposing anything** —
  full trace in the PRD's Assumed/Evidence. Also found, while checking
  `agents/eng-manager/config/decision-journal.md` and `inbox/` per the
  readback skill's own required inputs, that this request substantially
  overlaps an already-approved, still-unprocessed standing question under
  `ENG-013` (see Notes above) — used as confirming evidence for this
  ticket's core mechanism rather than re-derived from scratch, without
  touching that item's own gate lifecycle.

  **PRD written**:
  `agents/product-manager/specs/ENG-017-presignup-lead-nurture-autopilot.md`.

  **G1 drafted but not raised.** Approver-facing WIP is substantively 2/2
  (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s Guards ("Approver WIP
  limit (2)... at the limit, nothing new starts that will need them"),
  this ticket was carried through readback and PRD-writing (agent-owned
  work, costs the approver's queue nothing) but not advanced into
  `awaiting-scope`, which would raise a third open G1 against a cap of
  two. Same move this instance's own immediately preceding pass made for
  `ENG-016`. The PRD's G1 content (readback, non-goals, recommendation) is
  fully drafted and ready to raise the moment a slot frees. **1
  transition** (`intake → shaped`), well under the cap of 4.
  **Consequence:** no cap numbers change — `shaped` counts toward neither
  approver-facing WIP nor machine WIP.

  No `inbox/` item raised this pass (no G1 to notify on yet), so no
  `lib/eng-notify.sh` call.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist at
  the department or instance level (confirmed absent again this pass, same
  open proposal, `proposals.md` 2026-08-25 row); not refiled.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract — not run beyond the fresh cap-verification above.

  **Observations filed** (`observations.md`): the confirmed-absent
  stage/consent concepts on the `leads` table; the restaurant-scoped shape
  of the existing autopilot data model and why it doesn't directly fit a
  presignup lead; the cross-reference to `ENG-013`'s answered-but-
  unprocessed standing question and the recommendation to point that
  item's eventual processing at this ticket rather than duplicating it.

  `chained: none` — `ENG-017` sits at `shaped`, an agent-owned state, but
  held there by the approver-facing WIP cap rather than genuinely blocked
  or waiting on a human for this ticket specifically; firing `continue
  ENG-017` now would only re-discover the same cap with no new work to do.
  Re-check once a `decision`/`watch`/`scheduled` pass clears `ENG-014` or
  `ENG-015`, or via a dedicated `continue ENG-017` once either does. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-017`) and
  whole-board: both exit 0, clean.

- `2026-08-29` `shaped → awaiting-scope` (product-manager, `scheduled` event
  pass, context `schtasks`). The re-check this ticket's own prior entry
  named: `ENG-014` and `ENG-015` have both since reached `designed` (past
  their own G1s), confirmed fresh from each ticket's own frontmatter —
  approver-facing WIP is 0/2 before this pass's own two raises. Mode check
  clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml`
  → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-017`) and
  whole-board: both exit 0, clean.

  G1 content already fully drafted in the PRD at `shaped` time; no new
  readback needed. Raised `inbox/2026-08-29-eng017-g1-scope.md` immediately
  after `ENG-016`'s (this pass's other raise — `ENG-016`'s `priority: next`
  outranks this ticket's unset priority, so it went first; among the
  remaining unset-priority backlog this ticket has the lowest id, per
  `eng_build_loop.md` step 6's dispatch ordering). Ran
  `departments/engineering/lib/eng-notify.sh raise` (logged
  `SLACK_WEBHOOK_URL unset — cannot notify`, non-fatal — item still sits in
  `inbox/` and the control center), stamped `notified:
  2026-08-29T23:13:50`.

  **1 transition** (`shaped → awaiting-scope`), well under the cap of 4.
  **Consequence:** approver-facing WIP 1/2 → 2/2 (this G1, after `ENG-016`'s
  in the same pass) — now at cap; nothing further should start into an
  approver-facing state until one of these two clears. Machine WIP
  unaffected.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-017`) and
  whole-board: see board index.
