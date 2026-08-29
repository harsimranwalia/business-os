---
ticket: ENG-013
project: aiorders-admin-hub
status: designed
size: M
author: product-manager
created: 2026-08-29
decided: 2026-08-29T11:45:00.908943+00:00
---

# Foodswipe funnel page — staff-settable pipeline stages

## Readback

**You said:** "for the foodswipe SALES funnel page we are not able to or the
sales staff is not able to update or have proper peipleine stages / sales,
onboarding staff is not able to do anything with the funnel page of
foodswipe on admin panel"

**Understood as:** The admin panel's Foodswipe funnel page (confirmed —
`aiorders-admin-hub`'s `src/pages/FoodswipeListings.tsx`, a real, existing
page titled "Foodswipe Listings" that tracks "restaurant onboarding
progress across stages") is entirely read-only today — sales and
onboarding staff can look at it but cannot act on it in any way. You want
staff to be able to set/correct a listing's pipeline stage, and you're
also questioning whether the stages it shows are the right ("proper")
ones for how the team actually works.

**Requirements:**
1. `[stated]` Staff can update a listing's pipeline stage on the Foodswipe
   funnel page — today there is no way to do this at all.
2. `[inferred]` Both "sales" and "onboarding" staff use this one page and
   both need this capability — not two separate tools.
3. `[proposed]` This is a missing capability, not a regression — nothing
   in the text or the code suggests it ever worked and broke. See
   "Evidence checked" below.
4. `[proposed]` The existing six-stage set (Account Created → Profile
   Updated → Listing Claimed → Menu Uploaded → GBP Shared → Website
   Interest) stays as this ticket's stage taxonomy — it already reflects
   real onboarding milestones. Making it staff-**settable** is this
   ticket; whether the stage *names* themselves are wrong is the standing
   question below.

**Assumed, and worth correcting if wrong:**
- **"Update" means staff can set/override which stage a listing sits in**,
  not edit the underlying lead/restaurant details (name, phone, email,
  etc.) — the literal text ties "update" to "pipeline stages"
  specifically. Editing record details is named as a non-goal below;
  cheap to add later if wrong.
- **A manual stage-set should stick** — once staff set a stage by hand, an
  automatic reclassification on next page load shouldn't silently
  overwrite it, and staff should be able to reset a listing back to
  automatic. The exact mechanism is the architect's call; this is the
  observable behavior the fix needs.
- **No new "sales" stages before the ones that already exist** — the
  current six all describe a restaurant that has already signed up via
  Foodswipe. Whether staff also want to track prospects who haven't
  signed up yet is the standing question below, not assumed into this
  ticket.

**Second reading agreed / diverged on:** Two independent readings were
run — this PM's, and, blind to it, the architect's (subagent, `opus`,
raw request + `knowledge/business-profile.md` only, no repo access, no
exposure to this PM's own reading). **No material divergence on
direction** — both readings converged on the same core shape: an
existing admin page, effectively non-functional for staff today, that
should let them act on a pipeline ("give sales and onboarding staff a
working funnel/pipeline view... where a staff member can move a record
from one stage to the next"); both independently flagged "update" as
collapsing two possible meanings (move-stage vs. edit-details) without
the text settling which; both read this as a missing capability rather
than a regression. The architect's reading went further than this PM's
on one point, unprompted: it hypothesized that "sales" and "onboarding"
might be **two different phases with two different stage vocabularies**,
and that the current stage set (which this PM's reading, before checking
code, had not examined) might only cover one of them — "built-in stages
likely stop at 'closed'." Checked against the actual code (below): the
current six stages are all *post-signup* — there is no pre-signup
"lead"/"prospect" stage anywhere in this system. That confirms the
architect's hypothesis is live rather than speculative, which is why it's
carried forward as the standing question rather than folded silently into
either reading.

**Evidence checked, not assumed.** `aiorders-admin-hub`'s live worktree
confirms `FoodswipeListings.tsx` (339 lines): a kanban board with six
columns, fed by one `GET` call, rendering `KanbanCard`s with **no click
handler, no drag handler, no edit affordance, and no mutation call
anywhere in the file.** `aiorders-api`'s handler
(`admin-portal/handlers/foodswipe.ts`) confirms the same on the backend:
`classifyStage()` is a pure function computing the stage entirely from
existing `profiles`/`restaurants`/`restaurant_listing_data` columns
(name+phone presence, claim status, menus, Google Business Profile share,
website interest) — there is no stored stage field, no manual-override
column, and no write branch in the handler at all (it accepts `POST` but
runs the identical read-only logic regardless of method). Searched the
whole `aiorders-api` repo for `assigned_to`, `lead_status`, `crm_stage`,
`sales_stage`, `contact_status`, `owner_id` — none exist anywhere; this
is genuinely new ground, not an extension of something already there,
same shape as `ENG-011`'s "tickets" finding. Also checked `claim_status`
(present on `restaurants`, fetched by this same handler): it is written
once, always to the literal string `'pending'`, and never read by
`classifyStage()` or anywhere else — a dead field, not a usable existing
status concept. Separately confirmed `Leads.tsx` (a different page, with
real edit/delete UI already) only edits **website-interest-form leads**,
an unrelated record type — its existing update endpoint
(`/leads/website/update`) does not touch Foodswipe profiles and isn't
reusable here.

**One naming note, not part of this ticket's scope but worth recording:**
"Foodswipe" is used for two distinct concepts across the two live
requests this instance is currently holding — this page's self-serve
*restaurant* onboarding funnel (`profiles.source = 'foodswipe'`), and, per
`ENG-006`'s already-shipped design, a cross-restaurant *consumer* loyalty
identity also branded "foodswipe customer." They share a name and nothing
else technically. Flagged so nobody downstream conflates the two.

## Problem

Sales and onboarding staff have no way to act on the one page built to
track a restaurant's progress through Foodswipe signup — they can see a
kanban board but cannot correct it, advance it, or otherwise do anything
with it, so the page can't actually be used to run day-to-day follow-up
work. Confirmed in code, not just reported: there is no write path
anywhere in the stack for this page today.

## Why now

Approver-initiated; no stated deadline, no specific restaurant named as
stuck. Read together with `ENG-011` (filed the same day, same "staff
can't act on an admin list" shape for a different page), this is the
second instance of the same underlying gap on this admin panel — worth
the EM's attention as a pattern, not escalated here since neither ticket
individually rises above its own stated severity.

## Users

AIOrders sales and onboarding staff working Foodswipe-sourced restaurant
signups on the admin panel. Not the restaurant/consumer side, and not the
separately-raised agency/reseller admin-scoping request.

## Proposed change

After this ships, staff opening the Foodswipe funnel page can set or
correct a listing's stage by hand, and that choice sticks (with a way to
reset back to automatic) rather than the page being pure, unactionable
read-only output.

## Acceptance criteria

1. `[stated]` Given the Foodswipe funnel page, when a staff member acts on
   a listing, then they can set its stage to any of the six existing
   values, regardless of what the automatic classification would compute.
2. `[inferred]` Given a manually-set stage, when the underlying data is
   later reloaded, then the manual value is what's shown — it is not
   silently overwritten by a fresh automatic classification.
3. `[inferred]` Given a manually-set stage, staff can reset the listing
   back to automatic classification.
4. `[proposed]` Given the funnel page, staff can visually tell which
   listings are manually set versus automatically classified.
5. `[inferred]` Given a non-admin/sub-admin request to the new stage-set
   capability, then it's rejected by the same authorization gate the
   page's existing read endpoint already uses.

## Non-goals

- Editing a listing's underlying details (name, phone, email, restaurant
  info) — this ticket is stage control only. See "Assumed" above.
- Notes, comments, or a contact/activity log per listing — not asked for
  in the text; a real feature if wanted, same shape as `ENG-010`'s
  influencer notes log, but for a different object and not yet requested
  here.
- A pre-signup / cold-lead pipeline for restaurants that haven't signed up
  via Foodswipe yet — the standing question below; genuinely unscoped
  until answered.
- Renaming, reordering, adding, or removing stages from the existing
  six-value set — kept as-is for this ticket; correctable at G1 if wrong.
- Drag-and-drop specifically as the interaction — this PRD states staff
  can set a stage; whether that's a dropdown, a button, or a drag gesture
  is the architect's/frontend's call.

## Risks and unknowns

- **"Proper pipeline stages" might mean the six-value set itself is wrong
  for how staff work**, not just that it's uneditable — if the approver
  means "different stages," this ticket's minimal fix (make the existing
  set staff-settable) would need revisiting once that's known. Flagged
  here rather than discovered mid-build.
- **Whether "sales" implies tracking pre-signup prospects is unresolved**
  — see the standing question. If yes, that is a materially larger,
  separate ticket (a new record type with no `profiles` row to hang off
  of), not an extension of this one.
- No specific restaurant or deal named as blocked today; no stated
  deadline.

## Cost

- Build: `M` — spans `aiorders-api` (a new authenticated write path plus
  wherever the manual override is stored) and `aiorders-admin-hub`
  (stage-set control on each kanban card), each half comparable to
  `ENG-011`'s two-repo split. Slightly more than a pure-derive ticket like
  `ENG-011` since this needs a genuine new write endpoint, not only
  additional read fields. Rough band: half a day to a couple of days.
- Run: `$0/month` — no new vendor, and the architect's own read of the
  data shape suggests one additive column at most, same pattern
  `ENG-011` used for its own derived fields.

## Decision

- **The approver's answer:** approved — bare, no rider.
- **Date:** 2026-08-29T11:45:00.908943+00:00
- **Notes:** No pushback on the readback, the proposed six-stage default,
  or the split-out standing question. Design found no one-way door
  (additive column, reused authorization) — moved straight through
  `designed → ready`, no G2.
