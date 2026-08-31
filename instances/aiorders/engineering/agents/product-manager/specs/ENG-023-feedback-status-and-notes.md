---
ticket: ENG-023
project: restaurant-portal
status: approved
size: S
author: product-manager
created: 2026-08-29
decided: 2026-08-29T23:38:32.834274+00:00
---

# Feedback board: status and notes per item, so the restaurant can act on feedback and show it did

## Readback

**You said:** "the feedback board on the brand portal does not have status or notes

what to do with the feedback, any actions taken is this frequent what are the bottomline issue that need to be resolved by the restaurant location."

**Understood as:** The brand portal's Feedback page shows customer feedback
but is pure read-only display — a restaurant can see a complaint or review
but has no way to mark what's being done about it or record what the actual
issue was. This ticket adds a status and an internal notes field to each
feedback item so a restaurant can track it item-by-item: where it stands,
what action was taken, what the real underlying issue was.

**Assumed, and worth correcting if wrong:**
- Status/notes are set by the restaurant's own staff on the brand portal
  (`restaurant-portal`) — not something only AIOrders' internal admin tool
  shows. Confirmed `aiorders-admin-hub` has no feedback view of its own today
  (one bullet mention in `Brands.tsx`, no page), so this couldn't be an
  admin-hub feature read back into brand-portal language.
- Notes are internal — for the restaurant's own tracking — not a reply
  channel back to the customer. Nothing in the request or the existing page
  implies a customer-facing response.
- The exact status vocabulary (e.g. new / in progress / resolved) is a design
  decision, not dictated by the literal request — naming it here would cross
  into the architect's lane.

**Second reading agreed / diverged on:** Ran the request-readback — this PM's
own reading grounded in the live `restaurant-portal`/`aiorders-api` code, plus
a blind architect reading (subagent, opus, raw request + business profile
only, no repo access). **Strong convergence on the core**: both independently
landed on "each feedback item needs a workflow status and an internal note,"
unprompted — the architect's phrase was "the feedback board is a dead-end
inbox... turning raw feedback into an operating loop: triage, act, record."
**One material divergence**: the architect's blind reading treated "is this
frequent" and "bottomline issues" as asking for a built cross-item
aggregation layer — counts, recurring-issue detection, possibly AI-assisted
categorization ("this complaint came up 14 times this month"). This PM's own
first read leaned the other way — that a restaurant could answer "is this
frequent" for itself once notes exist to look back through — which is a
materially smaller build. Per `skills/request-readback/SKILL.md`'s
divergence table this is "different scope, one includes something the other
doesn't" — genuinely ambiguous, not resolved internally. **Not held up for
it**: same shape as `ENG-013`'s presignup-leads question, the confirmed core
below ships regardless of the answer, and a separate non-blocking question is
raised (`inbox/2026-08-29-eng023-frequency-question.md`) — "yes" becomes its
own ticket once scoped against what aggregation would actually need.

## Problem

The `restaurant_feedback` table (confirmed in schema) has no `status` or
`notes` column at all — this isn't a hidden field the UI just doesn't show,
the data has nowhere to live yet. Every new item does trigger a real-time
email to the restaurant (`notifications-handler`'s
`restaurant_feedback` handler, confirmed), so nothing is missed on arrival —
but there's no durable record afterward of what happened to it. The
approver's own question — "any actions taken" — can't currently be answered
by anyone, restaurant or AIOrders staff, without digging back through old
emails one at a time.

## Why now

The approver noticed this directly while looking at the feedback board — no
deeper trigger found or claimed.

## Users

Restaurant owners/managers on the brand portal (`restaurant-portal`) — the
people the approver names directly ("resolved by the restaurant location").

## Proposed change

On the brand portal's Feedback page, a restaurant can:
1. See and set a status on each feedback item (where it stands).
2. Write and save an internal note on each feedback item (what the issue
   was, what was done) — visible only to the restaurant's own staff, never
   the customer.

## Acceptance criteria

1. `[stated]` Given a restaurant viewing their feedback list, when they open
   a feedback item, then they can set a status on it, and it persists and
   displays correctly on return.
2. `[stated]` Given a restaurant viewing a feedback item, when they write a
   note about it, then the note saves and persists, and displays on return.
3. `[inferred]` Given restaurant A sets status/notes on their own feedback,
   when restaurant B views their own feedback list, then none of restaurant
   A's items, statuses, or notes are visible to B — same tenant scoping
   already required for reading feedback at all (see Risks — this depends on
   `ENG-022`'s fix landing correctly, not a new requirement invented here).
4. `[inferred]` Given a feedback item that existed before this ships, when a
   restaurant views it, then it shows a plain default/empty status rather
   than an error or a blank crash.
5. `[proposed]` Status is a small fixed set of values rather than free text
   (e.g. new / in progress / resolved), so a future list can filter or count
   by it — exact values are a design decision, not fixed by this PRD.

## Non-goals

- **Cross-item frequency or pattern analysis** — "is this frequent," "what
  are the bottomline issues" read as a built aggregation/analytics feature
  (counts, recurring-issue detection, AI-assisted categorization). Real
  question, not dropped — see the separate, non-blocking intake-question
  raised alongside this ticket. Becomes its own ticket if the answer is yes,
  same shape as `ENG-013` → `ENG-017`.
- Any customer-facing reply channel — notes are internal only.
- A staff-facing (admin-hub) mirror of this same status/notes view —
  plausible future value, not what was asked, and admin-hub has no feedback
  view to extend today.
- AI-generated summarization or categorization of feedback content.

## Risks and unknowns

- **Do not copy this file's existing broken pattern.** The only existing
  write-shaped precedent in `supabase/functions/brand-portal/feedback.ts` is
  its own `getFeedback`, which has a confirmed broken tenant-isolation check
  (`ENG-022`, filed this same pass, same file). The new `update_feedback`
  handler this ticket needs must be modeled on `catering.ts`'s
  `update_catering_request` (confirmed correct: fetch record → verify access
  via the properly-ordered call, checking `.hasAccess` → update → return),
  not on its own file's neighbor. Not a formal `depends_on` — this ticket
  doesn't need `ENG-022` to ship first, only to not repeat its mistake.
- Status vocabulary and whether a who/when audit trail on changes is
  warranted are open design questions. The architect's blind reading assumed
  multi-staff attribution matters (several staff sharing one portal login
  set); this PM found no confirmed precedent either way in the sibling
  `catering`/`offers` status fields to settle it — left to design rather than
  guessed here.

## Cost

- **Build:** `S` — two new columns (`status`, `notes`) on `restaurant_feedback`,
  one new edge-function action closely modeled on an existing same-file-
  directory precedent, and a small addition (status control + notes field)
  to the existing Feedback page's card layout. No new data model, single
  project pairing (`restaurant-portal` primary, `aiorders-api` for the write
  path) — same split precedent as `ENG-007`/`ENG-011`/`ENG-015`. A few hours
  to half a day. Displaces one slot on an already-full board (machine WIP
  6/6); sequencing against `ENG-022` in the same file is the EM's call at
  `ready`, not decided here.
- **Run:** $0/month. No new infrastructure.

## Decision

Filled in after G1.

- **The approver's answer:** approved
- **Date:** 2026-08-29T23:38:32.834274+00:00
- **Notes:** No additional comment recorded beyond the bare approval.
