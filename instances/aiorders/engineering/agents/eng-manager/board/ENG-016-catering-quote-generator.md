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

- `2026-08-29` `shaped → awaiting-scope` (product-manager, `scheduled` event
  pass, context `schtasks`). This is exactly the re-check this ticket's own
  prior entry named: `ENG-014` and `ENG-015` have both since reached
  `designed` (past their own G1s), confirmed fresh from each ticket's own
  frontmatter rather than trusted from the board table — approver-facing
  WIP is 0/2, fully free. Mode check clean (business-os `.env` → `MODE=`
  empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-016`) and
  whole-board: both exit 0, clean.

  **Also corrected while re-checking the cap, not assumed from the board
  header:** `agents/eng-manager/config/config.yaml` records `approval_cap`
  as removed 2026-08-29 at the approver's request — the only real
  approver-side lever left is `wip.approver_limit` (2). The board index's
  repeated "Approval cap 3" framing is stale relative to that removal; fixed
  in this pass's board update rather than propagated further.

  No new readback needed — the G1 content was already fully drafted in the
  PRD at `shaped` time (see PRD's own Decision section, now updated to
  `status: awaiting-scope`). Raised
  `inbox/2026-08-29-eng016-g1-scope.md`, ran
  `departments/engineering/lib/eng-notify.sh raise` (logged
  `SLACK_WEBHOOK_URL unset — cannot notify`, non-fatal per the script's own
  design — the item still sits in `inbox/` and the control center), stamped
  `notified: 2026-08-29T23:13:49`.

  **Picked ahead of `ENG-017`/`ENG-019`/`ENG-020`/`ENG-021` per the board's
  own dispatch ordering** (`eng_build_loop.md` step 6): `priority: next`
  outranks the unset priority the other three carry; `ENG-018` excluded
  outright (`priority: hold`). Exactly two free approver-facing WIP slots
  and exactly two tickets ordered ahead of the rest (`ENG-016`, then
  `ENG-017`) — both raised this pass, filling the cap to 2/2 without
  exceeding it.

  **1 transition** (`shaped → awaiting-scope`), well under the cap of 4 —
  `awaiting-scope` is owned by the approver, this pass's own stopping
  point. **Consequence:** approver-facing WIP 0/2 → 1/2 (this G1); machine
  WIP unaffected (`awaiting-scope` sits outside the counted range).

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-016`) and
  whole-board: see board index.

- `2026-09-01` **no state change — `board/_index.md` corrected instead**
  (`watch` event pass, context `launchd`). Found this ticket's own file and
  PRD (both `awaiting-scope`, G1 raised and notified `2026-08-29T23:13:49`,
  never answered) disagreeing with `_index.md`'s In-flight table and
  "Waiting on the approver" section, both of which read `shaped` /
  `product-manager` / "G1-drafted, ready to raise" for this ticket. Root
  cause: the 09:30 pass's own `git pull` (`e281c71`, "reconcile 26 diverged
  engineering-board files") kept a rival host's account of the index
  wholesale for internal consistency with several other tickets that really
  were behind on that host — but that host had never learned this ticket's
  G1 was raised on 2026-08-29, so its narrative was not stale, it was
  genuinely missing an event. Checked `decision-journal.md` (no `ENG-016`
  row) and this ticket's own PRD `status:` before concluding staleness
  rather than a legitimate reset — neither shows one. Corrected `_index.md`
  in place (In-flight row, header WIP accounting, "Waiting on the approver"
  section) rather than this ticket's own file, which was already right.
  Also nudged the open G1 (`inbox/2026-08-29-eng016-g1-scope.md`,
  `nudged: 2026-09-01T10:20:06`) — notified 2.5 days ago, never nudged
  before, missed by every intervening pass because they all read the index
  rather than this file. Filed a proposal
  (`agents/eng-manager/proposals.md`) so a future cross-host reconciliation
  re-derives the In-flight table from each ticket's own frontmatter instead
  of keeping one side's board-index prose wholesale.
  `chained: none` — still `awaiting-scope`, owned by the approver; unchanged
  by this correction.
