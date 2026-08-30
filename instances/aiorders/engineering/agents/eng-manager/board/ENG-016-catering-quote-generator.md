---
id: ENG-016
title: Catering page — self-serve quote generator, with automatic stage update
project: config-site-builder
type: feature
size: L
time_estimate: several days to a week
time_spent:
time_remaining:
severity: P2
priority: next
state: shaped
owner: product-manager
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
  prd: agents/product-manager/specs/ENG-016-catering-quote-generator.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

A restaurant's catering leads dead-end at "thanks, we'll be in touch" —
the owner is notified and a CRM record is created, but every quote after
that is fully manual (staff price it and reply by phone/email), there's no
computed price, and the catering pipeline on restaurant-portal is only
ever updated by a staff member dragging a card by hand.

## Outcome

A restaurant owner can opt in to an automated quote flow: a customer who
submits the catering enquiry form gets a link (SMS/email) to a
self-service quote-builder page where they pick menu items and see a
computed price, or skip straight to today's generic message. Either way,
the matching request's stage on restaurant-portal's catering board updates
on its own. Owners who don't opt in see no change from today.

## Notes

Full grounding, evidence, and the two forks named in the request-readback
(who controls the "just contact me" fallback; reuse the existing menu's
prices vs. a new catering-specific pricing model) are in the PRD — see
`links.prd`. Spans three repos: `config-site-builder` (primary — the new
customer-facing quote page), `aiorders-api` (quote storage, link
generation, send — reusing the existing `outgoing-communications`/
`autopilot` engine), `restaurant-portal` (one additive status value plus a
small addition to the already-shipped `CateringDetailModal`).

Deliberately held at `shaped` rather than advanced to `awaiting-scope` —
see Log. Not a scope gap; the G1 content is fully drafted in the PRD and
ready to raise the moment a WIP slot frees.

## Log

- `2026-08-29` `intake → shaped` (product-manager) — event pass, context
  `agents/product-manager/inbox/2026-08-29-for-catering-page-need-next-step-quote-generator-page-which-.md`.
  Sized `L`, project `config-site-builder` (primary; `aiorders-api` and
  `restaurant-portal` also touched, named in the PRD per the `ENG-003`
  precedent for a multi-repo ticket under a singular `project:` field).
  Ran the full request-readback (`skills/request-readback/SKILL.md`): this
  PM's own reading, grounded in live code across all three repos, plus a
  blind architect reading (subagent, `opus`, raw request +
  `knowledge/business-profile.md` only, no repo access, no exposure to
  this PM's own reading). No material divergence on the core shape; two
  real forks surfaced (fallback-path control; menu/pricing reuse vs. a new
  catering-specific model) — both resolved with a stated, correctable
  default bundled into the PRD as a G1 rider, same bar `ENG-015`'s G1 used
  for its own small fork, rather than opening a separate blocking standing
  question.
  **Caps checked fresh, not from the cached board header, before deciding
  how far to carry this ticket:** `inbox/` re-listed directly this pass —
  `2026-08-29-eng014-g1-scope.md` and `2026-08-29-eng015-g1-scope.md` both
  still present, unanswered (`ENG-009`/`ENG-010`/`ENG-012`'s G1s and
  `ENG-013`'s standing question also still present but already answered
  per prior passes' own findings, off the count per this board's
  established convention). Approver-facing WIP therefore still
  substantively 2/2 — at cap — per `board/_index.md`'s own header, itself
  confirmed fresh this pass rather than trusted. Per
  `schedules/eng_build_loop.md`'s Guards section ("Approver WIP limit (2)
  ... At the limit, nothing new starts that will need them"), this ticket
  — full lane, `type: feature`, not on the G1-auto-skip list — was carried
  through readback and PRD-writing (agent-owned work, consumes nothing of
  the approver's queue) but **held at `shaped` rather than advanced to
  `awaiting-scope`**, since doing so would raise a third open G1 against a
  cap of two. The PRD's own G1 content (readback, recommendation, both
  forks named as riders) is fully drafted and ready — nothing further to
  shape once a slot frees.
  `chained: none` — held by the approver-facing WIP cap (2/2:
  `ENG-014`, `ENG-015` both still open, neither cleared during this pass);
  not blocked, not waiting on a human for *this* ticket specifically, but
  the chaining guard's cap exception applies all the same, since firing
  `continue ENG-016` now would only re-discover the same cap with no new
  work to do. Re-check on the next `decision`/`watch`/`scheduled` pass that
  clears `ENG-014` or `ENG-015`, or via a dedicated `continue ENG-016` once
  either does.
