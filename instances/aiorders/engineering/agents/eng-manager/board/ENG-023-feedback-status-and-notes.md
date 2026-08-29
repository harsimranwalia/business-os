---
id: ENG-023
title: Add status and internal notes to each brand-portal feedback item
project: restaurant-portal
type: feature
size: S
time_estimate: a few hours to half a day
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
  prd: agents/product-manager/specs/ENG-023-feedback-status-and-notes.md
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
`agents/product-manager/inbox/2026-08-29-the-feedback-board-on-the-brand-portal-does-not-have-status-.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T09:17:39.295756+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # the feedback board on the brand portal does not have status or notes
>
> what to do with the feedback, any actions taken is this frequent what are
> the bottomline issue that need to be resolved by the restaurant location.

## Readback

See `agents/product-manager/specs/ENG-023-feedback-status-and-notes.md` →
Readback — the full two-reading comparison and the divergence live there
rather than duplicated here.

## Problem

The brand portal's Feedback page (`restaurant-portal/src/pages/feedback/Index.tsx`)
is read-only display over `restaurant_feedback`, which has no `status` or
`notes` column at all — confirmed in schema, not just missing from the UI.
Restaurants get a real-time email per new item but have no durable record
afterward of what was done about it.

## Outcome

A restaurant can set a status and write an internal note on each of their
own feedback items, both persisting and scoped to their own restaurant only.

## Notes

**Investigated before writing anything**, same practice this board has used
throughout: read `restaurant-portal`'s Feedback page, its `brandPortalApi`
client, `aiorders-api`'s `brand-portal/feedback.ts` handler (only action
today: `get_feedback`), the `restaurant_feedback` table's real schema (no
status/notes columns), and the `notifications-handler`'s per-submission email
(confirmed feedback isn't missed on arrival, only unrecorded afterward).

**Filed alongside `ENG-022`, not folded into it.** Tracing this request's
backend surfaced a confirmed, unrelated security defect in the same
directory (`feedback.ts`'s existing `getFeedback` has a broken tenant-
isolation check) — filed as its own ticket
(`agents/eng-manager/board/ENG-022-brand-portal-tenant-isolation-broken.md`)
per `agents/product-manager/agent.md`'s `never_touches` list (security
findings aren't the PM's to fix or fold into a feature PRD). Cross-referenced
in both tickets' Risks/Notes: this ticket's new write path must be modeled on
`catering.ts`'s confirmed-correct `update_catering_request`, not on this
file's own broken `getFeedback` neighbor.

**Non-blocking question raised alongside this ticket**, not held for it:
`inbox/2026-08-29-eng023-frequency-question.md` — whether "is this frequent"
/ "bottomline issues" also wants a built cross-item aggregation view, per the
architect's blind reading diverging from this PM's own on exactly that point.
Same shape as `ENG-013`'s presignup-leads question → `ENG-017`: this ticket
ships the confirmed core regardless of the answer.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
reads 2/2 (conservative — `ENG-014`/`ENG-015`'s G1s are answered but not yet
processed by a `decision` pass; treated as still holding their slots, same
convention `ENG-021` used). G1 content (readback, both readings, non-goals,
recommendation) is fully drafted in the PRD's own Decision section, ready to
raise the moment a slot clears.

**Recommendation, for whenever this G1 raises:** build it. The core (status +
notes) is a small, well-precedented change — the department has shipped this
exact shape (new column + restaurant-scoped edit) three times this week
(`ENG-007`, `ENG-009`, `ENG-010`) — and it directly answers a question the
approver asked in their own words ("any actions taken").

## Log

- `2026-08-29` `intake → shaped` (product-manager, `intake` event pass,
  context this exact request file). Per this event's own narrower contract,
  worked only this one request end to end — did not sweep the rest of
  `agents/product-manager/inbox/` (`fix-the-location-bug-on-foodswipe`
  untouched, its own `intake` event presumably already queued or pending).

  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Caps checked fresh from `inbox/` directly**: `ENG-014`'s and `ENG-015`'s
  G1s both still sit in `inbox/` (not yet moved to `_handled/`) with
  `decision: approved` — answered but unprocessed, held conservatively as
  still occupying their approver-facing WIP slots pending a `decision` pass,
  same reasoning the board index and `ENG-021` already used. Approver-facing
  WIP treated as 2/2 for this ticket's own purposes.

  **Ran the full request-readback**
  (`skills/request-readback/SKILL.md`): this PM's own reading, grounded in
  live code across `restaurant-portal` and `aiorders-api`, plus a blind
  architect reading (subagent, `opus`, raw request +
  `knowledge/business-profile.md` only, no repo access, no exposure to this
  PM's own reading). Strong convergence on the core (status + notes per
  item); one material divergence on the "is this frequent" /
  "bottomline issues" phrase — see PRD Readback. Not held up: confirmed core
  shaped now, divergence raised as its own non-blocking question, per the
  `ENG-013`/leads-question precedent.

  **Investigated all relevant code before proposing anything**: see Notes
  above.

  **Found and filed `ENG-022` as a separate ticket** — a confirmed P0
  security defect discovered while tracing this request's backend, out of
  scope for a PM to fix or fold in. Full reasoning on `ENG-022`'s own PRD and
  ticket log.

  **PRD written**:
  `agents/product-manager/specs/ENG-023-feedback-status-and-notes.md`.

  **No G1 raised this pass** — approver-facing WIP at cap (2/2, conservative
  count above). G1 content fully drafted in the PRD, ready the moment a slot
  clears.

  **Non-blocking question raised**:
  `inbox/2026-08-29-eng023-frequency-question.md` (`agent: product-manager`,
  `gate: intake-question`). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's own
  frontmatter for the result and `notified:` timestamp.

  **State:** `intake → shaped`. `owner` stays `product-manager` — nothing
  handed off yet, no gate open. **Consequence:** no cap numbers change —
  `shaped` counts toward neither approver-facing WIP nor machine WIP (still
  6/6).

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract beyond the fresh cap-verification above.

  **Observations filed** (`observations.md`): none beyond what's captured on
  `ENG-022` and this ticket directly.

  `chained: none` — `ENG-023` sits at `shaped`, held by the approver-facing
  WIP cap, not genuinely blocked or waiting on a human for this ticket
  specifically; firing `continue ENG-023` now would only re-discover the
  same cap with no new work to do. Re-check once a
  `decision`/`watch`/`scheduled` pass actually clears `ENG-014` or
  `ENG-015`. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-023`) and whole-board: see pass notes in
  `agents/eng-manager/board/_index.md`.

- `2026-08-29` `shaped → awaiting-scope` (product-manager → approver,
  `scheduled` event pass, context `schtasks`) — the four-times-daily
  safety-net sweep. Mode check clean (business-os `.env` → `MODE=` empty;
  instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Re-check from the top, not trusted from the cached header.** Processing
  `ENG-025`'s answered G1 this same pass (see that ticket's own log) freed
  both the approver-facing WIP slot and the approval-cap slot this ticket's
  own prior log entry was waiting on. `_index.md`'s own "Waiting on the
  approver" section names this exact ticket by id as the one to raise "the
  moment a `scheduled`/`watch`/`continue` pass picks it up" — this is that
  pass.

  **No new drafting needed** — G1 content (readback, both readings,
  evidence, non-goals, recommendation) was already fully drafted in the
  PRD's own Decision section at `shaped` time. Wrote
  `inbox/2026-08-29-eng023-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: restaurant-portal`, recommendation to build now) from
  that drafted content, not written fresh. Ran
  `departments/engineering/lib/eng-notify.sh raise` on it — logged
  `SLACK_WEBHOOK_URL unset — cannot notify` (`traces/eng-notify-2026-08-29.log`,
  15:55:43), same open, already-tracked notify-channel gap every gate item
  today has hit; stamped `notified: 2026-08-29T15:55:43` into the item's
  frontmatter directly, per this instance's established practice of
  stamping regardless of whether the push itself succeeds.

  **State:** `shaped → awaiting-scope`, `owner` moves `product-manager →
  approver`. **Consequence:** approver-facing WIP 0/2 → 1/2 (after
  `ENG-025`'s own G1 freed it earlier this same pass); approval cap 0/3 →
  1/3. Two approver-facing slots and two approval-cap slots remain free —
  `ENG-016` through `ENG-021` (also G1-drafted) deliberately left for a
  future pass; see `ENG-025`'s own log entry for why only this one ticket's
  freed capacity was reused rather than filling every open slot.

  **Dead-end sweep:** no other action needed on `ENG-023` itself; the
  broader whole-board sweep this event ran is recorded on `ENG-025`'s own
  log entry and the board index, not repeated here.

  **Notify sweep:** this pass's own new item raised and stamped above.
  Nothing else to nudge.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.
