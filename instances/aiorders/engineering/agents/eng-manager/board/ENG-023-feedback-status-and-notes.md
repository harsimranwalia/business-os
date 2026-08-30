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
state: designed
owner: eng-manager
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
  design: agents/architect/designs/ENG-023-feedback-status-and-notes.md
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

- `2026-08-29` `awaiting-scope → designed` (approver → architect, `watch`
  event pass, context `schtasks`) — swept all three watched inboxes per this
  event's own contract; `inbox/2026-08-29-eng023-g1-scope.md` was the only
  item found changed (found answered, **approved**,
  `decided: 2026-08-29T23:38:32.834274+00:00`, no additional comment).
  `ENG-011`'s merge request, the only other live item in `inbox/`, still
  carries an empty `decision:` — left untouched. Mode check clean
  (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-023`) and whole-board: both exit 0, clean.

  Same procedure `ENG-025`'s identical transition used earlier today: PRD
  `status: draft → approved`, `decided:` stamped. Gate item moved to
  `inbox/_handled/` with a processed footer. Journaled in
  `agents/eng-manager/config/decision-journal.md`.

  **Handed to the architect at `designed`, design work itself not started
  this pass** — same reasoning `ENG-025`'s own G1 processing used:
  `designed`'s exit condition (tech design written) is the architect's own
  output, not board bookkeeping, so it belongs in a dedicated `continue
  ENG-023` session.

  **State:** `awaiting-scope → designed`, `owner` moves `approver →
  architect`. **Consequence:** approver-facing WIP 2/2 → 1/2; approval cap
  2/3 → 1/3. `ENG-011`'s merge request is now the only item occupying either
  cap.

  **Dead-end sweep (scoped to this event's three-inbox contract):**
  `agents/product-manager/inbox/` and `agents/eng-manager/inbox/` both held
  nothing beyond `.gitkeep` — no other unprocessed item found.

  **Notify sweep:** nothing to raise for this ticket itself (its own gate is
  now closed, not open). No item found with `notified:` older than 24h and
  no `decision:`/`nudged:` among the two live inbox items. Approval cap
  1/3, not full — no stall.

  **Observations filed** (`observations.md`): none beyond what's captured
  here.

  `chained: ENG-023` — `designed`, owned by `architect`, an agent-owned
  state; firing
  `/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-023`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.

- `2026-08-29` `designed → designed`, `owner: architect → eng-manager`
  (`continue` event pass, context `ENG-023`) — the dedicated design session
  the prior pass's own log named. Mode check clean (business-os `.env` →
  `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
  whole-board: both exit 0, clean.

  **Investigated before designing**: read `restaurant-portal`'s
  `pages/feedback/Index.tsx` and `services/brandPortalApi.ts` in full;
  `aiorders-api`'s `brand-portal/feedback.ts`, `catering.ts` (the PRD's
  named model), `utils.ts` (`verifyRestaurantAccess`'s real signature —
  confirmed `feedback.ts`'s own `getFeedback` calls it with arguments in the
  wrong order and treats its object return as a boolean, exactly `ENG-022`'s
  filed defect) and `index.ts` (confirmed service-role client, no RLS
  involved, and the outer error-envelope both handler styles fall through
  to). Queried the live schema directly (Supabase MCP, read-only,
  `bmnmnejwdxbcqinqkwko`): confirmed `restaurant_feedback` has no
  `status`/`notes` column today; confirmed its only existing trigger is
  `AFTER INSERT` only (the notification email), so an `UPDATE` this ticket
  adds cannot re-trigger it; confirmed `catering.status`'s live values and
  that it's plain `text` with no CHECK/enum; found `restaurant_feedback`
  already carries an unwired `updated_at` column and that this codebase has
  an existing, reusable `update_updated_at_column()` trigger already wired
  to six other tables.

  **Design written**:
  `agents/architect/designs/ENG-023-feedback-status-and-notes.md`. Two
  additive columns (`status text NOT NULL DEFAULT 'new'`, `notes text
  NULL`) plus wiring the existing `updated_at` trigger; one new
  `update_feedback` action modeled on `update_catering_request`'s
  access-check shape but **not** its payload shape — see next paragraph.
  No RLS change (service-role client, matching every sibling handler). Full
  reasoning, alternatives, and risks in the design doc itself.

  **One-way doors: none.** Purely additive, fully reversible. No G2.

  **Found and routed a defect in the ticket's own prescribed model,
  rather than copying it**: `catering.ts`'s `update_catering_request`
  spreads the client's raw `updateData` directly into `.update()` with no
  field allow-list — a caller who passes its own access check can
  overwrite any column on the row, including `restaurant_id`. This
  ticket's new action allow-lists `status`/`notes` explicitly instead
  (design doc, Alternatives #2). Not this ticket's surface to fix — filed
  as a proposal line (`agents/eng-manager/proposals.md`, `by: architect`,
  `project: aiorders-api`, `size: S`) per step 3, since it needs an
  already-authenticated actor's deliberate misuse rather than an open
  unauthenticated hole and so doesn't meet the P0 carve-out.

  **State: stays `designed`** — the exit condition (tech design written,
  ADRs logged [none needed], one-way doors decided [none found]) is now
  met, so `owner` moves `architect → eng-manager` per the state table
  (`ready` is the EM's). The state field itself does not advance because
  machine WIP is still capped. **Re-checked fresh from each ticket's own
  frontmatter, not the board header**: `ENG-008` `building`, `ENG-013`
  `building`, `ENG-009`/`ENG-010` both `ready` — still 4/1, over the
  1-ticket cap, unchanged since the last pass to check it. `ENG-023`
  joins `ENG-014`/`ENG-015`/`ENG-022`/`ENG-025` in the same held-at-
  `designed` position for the same reason.

  **Dead-end sweep:** nothing else to resume for this ticket specifically
  — narrow scope per this event's own contract.

  **Notify sweep:** nothing to raise (no gate opened this pass) or nudge.

  **Observations filed** (`observations.md`): none beyond the proposal
  above, which is itself the correct channel for what was found.

  `chained: none` — held by the machine WIP cap (4/1, over the 1-ticket
  limit; no new ticket enters `ready` until it drains). Re-check once
  `ENG-008`, `ENG-009`, `ENG-010`, or `ENG-013` reaches `shipped`. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
  whole-board: see pass notes in `agents/eng-manager/board/_index.md`.
