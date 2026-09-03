---
ticket: ENG-016
project: config-site-builder
status: approved
size: L
author: product-manager
created: 2026-08-29
decided: 2026-09-03T15:47:46.139489+00:00
---

# Catering page — self-serve quote generator, with automatic stage update

## Readback

**You said:** "for catering page need next step/quote generator page which
would have the menu selection for the customer can be sent as link via
sms/email and update the stage on restaurant portal for ones who fill the
quote form"

"restaurant owners can choose to have pricing generator work after the
client fill the form and get it sent to them and client also choose to have
generic message that someone from the restaurant will reach out to you.
also be able to edit the quote and resent on their end. the catering
pipeline section can overall be improved and more automated with autopilot's
use for stage updates/ quote sent etc."

**Understood as:** Today, a customer who fills out a restaurant's public
catering enquiry page gets nothing back but an on-screen "we'll contact
you" message — confirmed in code, not assumed (see Evidence below): the
restaurant is notified and a CRM record is created, but the customer has no
next step and no path to an actual price. You want a self-service "quote
generator" step where that customer picks menu items and sees a computed
price, reachable by a link sent over SMS/email, with the whole thing
opt-in per restaurant. Completing it should move the request's stage on
restaurant-portal's existing catering board automatically rather than
staff dragging the card by hand. Editing an already-sent quote and
resending it, and using the `autopilot` engine to automate more of the
pipeline generally, are both named but are explicitly later work, not this
ticket.

**Requirements:**
1. `[stated]` A customer who submits the catering enquiry form can reach a
   quote-builder step where they select menu items to build a priced
   order.
2. `[stated]` That quote-builder step is reachable via a link sent by
   SMS/email.
3. `[stated]` Restaurant owners can turn this on or off — when off, the
   customer's experience is unchanged from today.
4. `[stated]` When a customer completes the quote step (or opts out of it),
   the matching request's stage updates on restaurant-portal automatically.
5. `[stated, deferred to a later item]` Owners can edit an already-generated
   quote and resend it.
6. `[stated, deferred to a later item]` The broader catering pipeline should
   use the existing `autopilot` automation engine more generally for stage
   updates and messaging.

**Assumed, and worth correcting if wrong:**
- **"Catering page" is `config-site-builder`'s own per-restaurant public
  page** (`src/pages/Catering.tsx`, with its enquiry form component,
  `src/components/CateringForm.tsx`) — not `restaurant-marketplace`'s
  separate catering form, and not the CloudWaitress popup widget
  (`restaurant-portal/public/CW-popup.html`). Both of those have their own
  independent submission paths today (`restaurant-marketplace`'s own
  `catering.ts` handler is a different code path entirely) and are out of
  scope for this ticket. Correctable at G1; extending to those surfaces
  would be a separate, named follow-up.
- **"Restaurant portal" is the existing owner-facing `restaurant-portal`
  project's live Catering board** (`components/catering/CateringKanban.tsx`,
  `StatusUpdateModal.tsx`, `CateringDetailModal.tsx`) — a real, shipped
  5-stage pipeline (New Enquiry → Contacted → Not Interested → Finalized →
  Completed) on a `catering` Supabase table, today updated only by a staff
  member dragging a card or picking a dropdown value. Not the internal
  admin panel.
- **"Menu selection" means the restaurant's existing menu, at its existing
  per-item prices — à la carte, not a new catering-specific pricing
  model** (per-person tiers, minimums, package pricing). Reusing what's
  there is the smaller, buildable-now interpretation and nothing in the
  raw text specifically asks for tiered catering pricing; the blind
  architect reading flagged this as a real fork worth naming rather than
  silently assuming (see Second reading below). If the approver wants a
  genuine catering-specific pricing model, that is materially bigger and
  belongs in its own ticket, not this one.
- **The existing per-guest "catering income" figure already shown on the
  restaurant-portal dashboard (`number_of_guests * 34`, a flat estimate
  used nowhere else) is unrelated to this ticket** — it is a rough
  dashboard heuristic, not real menu-based pricing, and this ticket does
  not touch it.
- **SMS/email consent is already captured on the existing enquiry form**
  ("By submitting this form, you consent to us contacting you via email
  and SMS," `config-site-builder`'s `CateringForm.tsx`) — this ticket
  relies on that existing consent covering the automated quote-link
  message too. Worth the architect confirming that reading rather than
  this PRD asserting it as settled.
- **The SMS/email send itself has $0 new vendor cost** — the approver
  already confirmed an unlimited-SMS vendor at a fixed monthly cost is in
  place (`ENG-006` G1 decision, 2026-08-28), and `aiorders-api`'s existing
  `outgoing-communications`/`autopilot` system already sends templated
  email and SMS to customers (see Evidence). This ticket is expected to
  reuse that path, not add a new one.
- **This is additive only** — a restaurant that never touches the new
  setting keeps today's exact behaviour (enquiry → owner notified →
  generic on-page "we'll contact you" message). Nothing about this ticket
  changes what happens for a restaurant that doesn't opt in.

**Second reading agreed / diverged on:** Two independent readings were
run — this PM's, grounded in the live code below, and, blind to it and to
this PM's own reading, the architect's (subagent, `opus`, raw request +
`knowledge/business-profile.md` only, no repo access). **No material
divergence on the core shape** — both independently converged on: a
catering lead flow that dead-ends today without an automated path to a
price; a self-serve quote builder with menu selection, delivered as an
SMS/email link; an owner-configurable toggle between real pricing and a
generic acknowledgement; automatic stage progression; and owner
edit/resend plus deeper `autopilot` use as separable, later work. Both
independently treated the request as fusing at least two shippable pieces
rather than one.

**Two real forks the architect's reading surfaced, neither assumed away:**
1. **Who controls the "generic message" fallback — the restaurant owner
   (a site-wide setting), or the customer (a per-visit choice)?** The raw
   text's "restaurant owners can choose... and client also choose" reads
   as the same owner-level choice restated (this PM's first-pass reading);
   the architect read "client also choose" as a second, genuinely
   customer-facing choice layered on top. These are not mutually
   exclusive and both are cheap, so this PRD proposes building both,
   the same resolution the approver preferred the one other time this
   instance offered a similar "A or B" choice that turned out cheap
   either way (`ENG-008`'s engagement-source question, `decision-journal.md`
   2026-08-29): an owner-level "Auto-quote" setting (default **off**,
   preserving today's behaviour) gates whether the automated SMS/email
   quote-link fires at all; independently, the quote-builder page itself
   carries a plain "Skip — just have someone contact me" option, so a
   customer who doesn't want to build a quote is never forced to. Named
   here as a rider for the approver to confirm or correct at G1, not
   raised as a separate blocking question — the cost difference between
   readings is small either way, the same bar `ENG-015`'s G1 used to bundle
   its own small fork rather than open a second gate for it.
2. **Same menu/pricing as online ordering, or a new catering-specific
   catalog?** Addressed above under "Assumed," and now settled by the
   approver's own rewrite below — see "Approver's `changed` response."

**Evidence checked, not assumed.** Read the live code across all three
repos this touches before proposing anything:
- `config-site-builder/src/pages/Catering.tsx` (304 lines): a real, live
  public page — hero, authored venues/FAQs, a "How It Works" explainer that
  already promises a step it doesn't deliver ("1. Request a Quote, 2.
  Customize Your Menu, 3. Enjoy Your Event" — step 2 does not exist
  anywhere in the code), and `<CateringForm config={config}
  preselectedLocationId={preselectedId} />`.
- `config-site-builder/src/components/CateringForm.tsx` (420 lines): posts
  directly to `https://…supabase.co/functions/v1/catering-request` with
  `full_name, phone, email, event_type, event_location, event_date,
  event_timings, number_of_guests, delivery_method, requirements,
  heard_about_us, source: 'website'`. No menu field of any kind exists on
  this form today.
- `aiorders-api/supabase/functions/catering-request/index.ts` (364 lines):
  on submit, inserts into the `catering` table, then (best-effort, does not
  fail the request) creates/updates a CRM customer record via
  `crm/customers/create-customer` with `consent_sms`/`consent_email` both
  `true`, then calls `send-notification` to alert the **restaurant owner**
  only — subject "New Catering Request on AI Orders," with a login link.
  **Nothing is ever sent back to the customer** beyond the form's own
  on-page success text ("We will contact you soon"). This is the exact gap
  named in the request.
- `restaurant-portal/src/components/catering/{CateringKanban,
  StatusUpdateModal, CateringRequestCard, CateringDetailModal}.tsx`: a
  real, shipped kanban with drag-and-drop and a status dropdown, both
  writing straight to `catering.status` via `brandPortalApi
  .updateCateringRequest` (kanban) or a direct Supabase update (detail
  modal) — five hardcoded status strings, no server-side enum.
- `aiorders-api/supabase/functions/brand-portal/catering.ts`: the backend
  behind that kanban — `get_catering_requests`, `update_catering_request`,
  and `get_catering_dashboard_stats` (the latter computing `cateringIncome`
  as `number_of_guests * 34`, a flat estimate unrelated to real menu
  pricing — see Assumed above). Also confirms `restaurants.live_catering`
  /`party_hall` are existing per-restaurant boolean settings.
- `aiorders-api/supabase/functions/autopilot/` and
  `.../autopilot/marketing/README.md`: a real, mature, already-shipped
  automation engine — DB-trigger-initiated, queued through Cloudflare
  Queues, sent via the `outgoing-communications` edge function. Today it
  only fires on customer lifecycle events — nothing catering-related.
- `restaurant-marketplace/src/hooks/useCatering.tsx` and
  `aiorders-api/.../restaurant-marketplace/handlers/catering.ts`: confirm
  the marketplace's catering path is genuinely separate code, supporting
  the "config-site-builder only" scoping above.

## Problem (original scope, superseded — see "Approver's `changed` response" below)

A restaurant's catering leads dead-end at "thanks, we'll be in touch" —
the owner is notified and a CRM record is created, but every quote after
that is fully manual (staff price it and reply by phone/email), there's no
computed price, and the catering pipeline on restaurant-portal is only
ever updated by a staff member dragging a card by hand.

## Outcome (original scope, superseded below)

The line above described the original, un-rewritten scope. See
"Approver's `changed` response" and everything from "## Problem (Piece 1,
rescoped)" onward for what actually proceeds.

## Notes

Full grounding, evidence, and the two forks named in the request-readback
are above. Spans three repos: `config-site-builder` (primary — the new
customer-facing quote page), `aiorders-api` (quote storage), `restaurant-
portal` (the catering board).

---

## Approver's `changed` response (2026-09-03T00:53:17Z) — full rewrite, not an edit

The approver's G1 answer (`decision: changed`, full text in
`inbox/2026-08-29-eng016-g1-scope.md`'s `## Decision` section) replaced this
PRD's small, buildable-now interpretation with a complete engineering task
spec: a packaging/fulfillment model (On-site Catering / Pickup & Delivery /
Drop-off Trays, guest-count-driven), categorized menu selection with a
**tiered "included vs. charged" pricing model** (exactly the catering-
specific pricing model the original PRD named as a non-goal), per-item
portion/variant notes, an owner-side "Edit Quote" action (the original
PRD's other deferred item), and three target pipeline stages ("Quote
Generated"/"Quote Received", "Contact Requested", "Quote Viewed") — though
the rewrite's own "Kanban Status Enum" bullet names only two of the three.

**Four load-bearing facts, verified against live code before writing
anything below — none of these were in the original evidence, because none
were true of the original scope:**

1. **The rewrite deletes the SMS/email link and moves the selector onto
   the public catering page itself.** Its own §2 heading is "Frontend:
   Public Catering Form," and its opening line is "Upgrade the *existing
   public catering page* … from a static enquiry form into an interactive
   catering menu selector." SMS/email now appears only as an outbound
   *summary after submission*. This removes the original PRD's
   unauthenticated-token design outright, and it is why "Quote Viewed" (a
   token-link-opened event) is unbuildable as specified — see the
   accompanying G1's rider.
2. **The fulfillment dropdown and guest-count field already exist**, and
   are already flag-driven, not flat: `CateringForm.tsx`'s
   `delivery_method` options are `pickup`, `delivery`, plus
   `live_catering`/`party_hall`/`food_truck` gated on per-restaurant flags;
   `number_of_guests` and `event_date` are already required fields. The
   rewrite's three proposed values don't map onto today's five, which is a
   data-compatibility question for existing `catering.delivery_method`
   rows, not a greenfield build.
3. **The catering board's five status strings are hardcoded in eight
   files**, not the three the original evidence found:
   `CateringKanban.tsx` (two copies — `statusConfig` and `columns`),
   `CateringDetailModal.tsx` (two copies), `StatusUpdateModal.tsx`,
   `CateringForm.tsx` (list plus two defaults), `ArchivedCateringModal.tsx`,
   `CateringCalendar.tsx`, `CateringRequestCard.tsx`, and
   `pages/catering/Index.tsx`. Every new stage is an eight-file edit, and
   five columns becoming seven is a board-layout change.
4. **The menu is a hand-authored JSON blob** (`restaurant_website.menu`,
   via `brand-portal/menus.ts`'s `get_digital_menu`), not a normalized
   table — `aiorders-api` has no first-party menu table at all. It's
   already available client-side on the public catering page (no new
   fetch needed), **but only when a restaurant's `hasMenu === 'page'`**;
   restaurants on `'file'` (PDF) or `'embedded'` (iframe ordering) have no
   structured menu and cannot render a selector. Item ids are optional
   (`id?`/`_id?`) and at least two price shapes exist across the two
   frontends — the rewrite's `selections[].item_id` rests on a field
   that isn't guaranteed to exist.

**Sizing verdict: the full rewrite is `XL`, not `L`, and does not proceed
as one ticket** (`prd-writer/SKILL.md` step 7: "XL goes back to the EM to
be split"). It contains two genuinely new data models (a package/price-book
definition; stored order selections), one new owner-facing authoring
surface (the price book), one new tokenized public surface deferred out of
this rewrite by the rewrite itself, and one new tracking mechanism —
several times over what "a new subsystem, a new data model, or
cross-project" (the `L` bar) describes. Honest total across the whole
rewrite: roughly three `L`s, several weeks — most of it (the tiered
package/pricing authoring surface) for a capability no restaurant is on
record requesting; the rewrite's own Implementation Checklist has zero
items for *authoring* a package, only for *rendering* one.

**Split, in build order — only the first piece is scoped and proceeding
now:**

- **Piece 1 — this ticket, rescoped, `L`.** Structured catering order
  capture and stage automation, minus any displayed pricing. See "Problem
  (Piece 1, rescoped)" onward.
- **Piece 2 — catering package & price book, `L`, depends on Piece 1.**
  Not filed. An owner authors packages (base rate, included-selection
  counts per category, per-extra upcharge); the public form renders
  included-vs-charged labels and a running estimate from that
  authored package. Natural home: `restaurant_website.catering`, alongside
  the existing `EDITABLE_PAGES` pattern in `restaurant-portal`'s website
  editor — the pattern exists, the shape and editor don't. **Held
  deliberately**, pending the approver naming who maintains each
  restaurant's price book — an authoring/maintenance cost the rewrite
  never named and assigns to nobody today.
- **Piece 3 — owner quote edit, resend, and view tracking, `M`–`L`,
  depends on Pieces 1 and 2.** Not filed. This is where "Edit Quote," a
  resend, and a per-record tokenized quote link — and therefore a real,
  implementable "Quote Viewed" — belong: the record and its price exist by
  then, so the token finally has something to point at.

**Why pricing isn't first, even though the approver's rewrite centers it:**
it can't be — "Choose 2 appetizers, +$3.00/person" cannot render before a
restaurant can author "2" and "$3.00," and nothing in the product can
author either today. Piece 1 is what ships while that authoring surface
gets designed, not a detour around it.

**Not filed as a piece:** collapsing the eight hardcoded status-string
copies into one source of truth. Real, and it would make Pieces 1 and 3
cheaper, but it overlaps `ENG-013`'s own open, unrelated stage-configuration
question (`inbox/2026-09-02-eng013-stage-config-question.md`) on a
different board — filing it here risks two tickets building the same
capability. Named as a risk below instead.

---

## Problem (Piece 1, rescoped)

A restaurant's catering leads dead-end at "thanks, we'll be in touch."
`aiorders-api`'s `catering-request` handler inserts the row,
best-effort-creates a CRM customer, and notifies **the restaurant owner
only** — the customer receives nothing beyond static success text. The
owner receives contact details, a guest count, and one free-text
`requirements` field; every quote after that is a staff member phoning
back to ask what the customer actually wants, then pricing it by hand.
`Catering.tsx`'s own "How It Works" copy already promises "2. Customize
Your Menu" — a step that exists nowhere in the code. The catering board
only ever moves when someone drags a card.

No count of lost catering leads exists — there is no measurement, and none
is invented here. The gap itself is code-confirmed.

## Why now

Approver-initiated, and now approver-rewritten: a complete replacement
spec is a stronger signal of intent than the original request. The
underlying gap (Piece 1) is current and code-confirmed; the tiered-pricing
half (Piece 2) is anticipated — no restaurant is on record asking for
per-person package tiers — which is part of why the work is split rather
than taken whole.

## Users

The **customer** on a restaurant's public catering page, who today can
only describe an order in prose. The **restaurant owner/staff** in
`restaurant-portal`, who today get prose and a board updated by hand.

## Proposed change

After this ships, a customer on a restaurant's public catering page picks
a fulfillment option, and — for restaurants whose menu is structured data
— chooses dishes by category with quantities and a short note per dish
(spice level, dry vs. gravy). They either submit that order for a quote,
or skip the picker entirely and ask for a callback. Either way the request
lands on the catering board already in the right column, and the owner
opens it to an itemized list of exactly what was chosen instead of a
paragraph.

No prices are shown to the customer in this ticket, and no quote is sent
back to them. The owner prices it — as they do today, but from an exact
order rather than a phone call.

## Acceptance criteria

1. `[stated]` Given a restaurant with the catering order form enabled,
   when a customer opens the public catering page, then a fulfillment
   option control is shown, and selecting a per-person/on-site option
   reveals a guest-count input with its helper note.
2. `[stated]` Given the form, when a fulfillment option is selected, then
   the instructional copy shown for that option comes from that
   restaurant's own configuration — no copy is hardcoded to one
   restaurant.
3. `[stated]` Given a restaurant whose menu is structured data, when the
   customer reaches the selection step, then dishes are shown grouped by
   that restaurant's own menu categories, each selectable with a quantity.
4. `[stated]` Given a selected dish, when the customer opens its note
   field, then they can attach a short free-text note to that dish, and
   that note is stored with that dish's selection.
5. `[stated]` Given selections and required contact fields, when the
   customer chooses "Submit Quote Request," then the request is stored
   with `action_type = QUOTE_SUBMITTED` and its selections (category, item
   reference, name, quantity, note), and the customer's own notes.
6. `[stated]` Given the form, when the customer chooses "Skip & Have
   Someone Contact Me," then the request is stored with `action_type =
   MANUAL_CONTACT_REQUESTED` and no selections, and the customer is not
   required to pick any dish.
7. `[stated]` Given a `QUOTE_SUBMITTED` request, when it is created, then
   it appears on the `restaurant-portal` catering board in **`Quote
   Generated`**; given `MANUAL_CONTACT_REQUESTED`, then in **`Contact
   Requested`** — in both cases without a staff member setting it.
8. `[stated]` Given an existing catering request in any of the five
   current stages, when the two new stages are added, then that request's
   stage and card are unchanged and it remains visible on the board.
9. `[proposed]` Given a restaurant that has not enabled the catering order
   form — including any restaurant with no structured menu data (`hasMenu`
   of `file` or `embedded`) — when a customer opens its catering page,
   then the form behaves exactly as it does today.
10. `[proposed]` Given an existing caller of `catering-request` that sends
    today's payload and no new fields — including the GoHighLevel path and
    `restaurant-marketplace`'s own submission — when it posts, then the
    request succeeds unchanged and the row is stored as it is today.
11. `[stated]` Given the customer has not filled name, phone, email and
    event date, when they attempt either bottom action, then submission is
    blocked with a field-level reason. Email is currently optional and
    nullable on this form — this is a deliberate behaviour change, see
    Risks.
12. `[inferred]` Given a `QUOTE_SUBMITTED` request open in the owner's
    detail modal, then the fulfillment option, guest count, and the
    itemized selections with quantities and notes are rendered readably.
13. `[proposed]` Given any read or write of the new selection data by a
    caller who is not the owning restaurant's staff, then it is refused by
    the same authorization path the existing catering endpoints already
    use.

## Non-goals

- **Any price shown to the customer, and any package/tier/upcharge
  model** — Piece 2. The "first N included, extras at +$X" behaviour is
  deliberately absent here; nothing in the product can author "N" or "$X"
  yet.
- **"Edit Quote," resending, and any quote sent back to the customer** —
  Piece 3.
- **`Quote Viewed`, per-quote tokens, and any tokenized public quote
  URL** — Piece 3; see the rider in the re-raised G1.
- **The SMS/email link *to* the builder**, from the original scope of this
  ticket — removed by the rewrite itself, which puts the selector on the
  public page.
- **Wiring catering into the general `autopilot` trigger/template
  engine** — unchanged from the original PRD; a separate domain extension.
- **Collapsing the eight hardcoded copies of the status list** — real, but
  overlaps `ENG-013`'s open stage-config question; not claimed here.
- **`restaurant-marketplace`'s and the CloudWaitress popup's own catering
  paths.**
- **Payment, deposits, or accepting a quote.**
- **Changing the meaning or order of the five existing stages** —
  additive only.

## Risks and unknowns

- **Restaurants with no structured menu are excluded, permanently and
  silently**, unless AC-9 gates it explicitly. `hasMenu` of `'file'`
  (PDF) or `'embedded'` (iframe ordering) restaurants can't render a
  selector — "which restaurants can turn this on" becomes something the
  department tracks going forward.
- **`item_id` may not exist.** Menu item ids are optional in the live
  type, and the menu is a hand-editable JSON blob. Stored selections can
  dangle or mismatch when an owner edits their menu after a quote was
  built. Storing the item's name and price *snapshot* alongside its id is
  the likely mitigation; exact mechanism is the architect's call.
- **The rewrite's payload is a rename-and-drop of a live contract.** Taken
  literally it renames several fields and omits others the GoHighLevel
  path and `restaurant-marketplace` still send. AC-10 forces this to be
  additive, not a breaking replacement.
- **The three proposed fulfillment values don't match the five live,
  flag-gated ones.** Existing `catering.delivery_method` rows and any
  board filtering on them depend on today's values; a mapping or migration
  decision is needed, not just a UI relabel.
- **Making email required is a deliberate behaviour change** and will
  lose phone-only submissions that succeed today — a real, small trade the
  approver's rewrite implies but doesn't name explicitly.
- **Two new columns make a seven-column board across eight files** — a
  layout change, not just a string addition — and it will collide with
  whatever `ENG-013`'s stage-config question resolves to; sequencing that
  overlap is worth naming to the approver, not silently risked.
- **The board is over its approver-facing cap.** `board/_index.md` records
  5/2 before this G1 (`ENG-008`, `ENG-009`, `ENG-010` merge requests;
  `ENG-013`'s question; `ENG-026`'s G1); re-raising this G1 makes it a
  sixth. This is the ticket's own continuing gate cycle, not a fresh
  To-do-column start, so it proceeds per this evening's `ENG-008`/`ENG-009`
  precedent — sequencing beyond that is the EM's call, not this PRD's.

## Cost

- **Build: `L`.** Three repos (`config-site-builder` primary,
  `aiorders-api`, `restaurant-portal`), one new stored data shape, no new
  subsystem. Several days to a week. **Displaces:** the near-term backlog
  (`ENG-014`, `ENG-015`, `ENG-017`, `ENG-019`–`ENG-025`, all backlog-
  grooming only right now) for roughly that window. Taking the full
  rewrite whole (all three pieces) would displace essentially all of it
  for two to three weeks instead.
- **Run: `$0/month`.** No customer-facing send in this piece at all — no
  SMS, no email, no new vendor surface. The `ENG-006`-contracted
  unlimited-SMS vendor isn't even called on until Piece 3.
- **Unpriced recurring cost, named rather than hidden:** Piece 2 creates a
  per-restaurant price book someone must author and keep in sync with the
  menu — operator time, not dollars, and permanent. Worth the approver
  deciding ownership of that before Piece 2 is filed, not after it ships.

## Recommendation

**Split it; build Piece 1 now.** The approver's full rewrite is `XL` and
does not proceed as one ticket per this department's own sizing rule.
Piece 1 — structured order capture, an itemized owner view, and two
automatic stages — is `L`, `$0/month`, and independently removes real
manual work (an exact itemized order replacing a phone-call guessing
game; a board that stops needing to be dragged) without waiting on a
pricing model whose ongoing maintenance owner isn't named yet. Pieces 2
and 3 are named above, not filed, and Piece 2 specifically should hold
until the approver answers who maintains each restaurant's package price
book.

## The 5-question filter, answered against `knowledge/business-profile.md`

AIOrders sells commission-free direct ordering and owned customer
relationships to independent restaurants, reducing marketplace
dependency — the operator's time is the product, and operator burden
created here is a cost the approver carries across every tenant, forever.

1. **Work off the approver's plate, or onto it?** Split-dependent, and
   this is the core of the argument. Piece 1 removes real work — an
   itemized order replaces a callback to ask what the customer wants, and
   the board stops needing manual drags. Piece 2 **adds** permanent
   work — a price book that must be authored and kept in sync with the
   menu, with zero authoring step anywhere in the approver's own
   checklist and no named owner. Taken whole, the rewrite is a net loss
   on this question; split, Piece 1 alone is a clear net gain.
2. **Freedom created or removed?** Piece 1 runs off menu data restaurants
   already maintain for ordering — freedom. Piece 2 is a second pricing
   surface that must stay consistent with the first, plus a permanent
   "which restaurants qualify" answer this department now owns.
3. **Current problem, or anticipated?** The dead-end is current and
   code-confirmed. The tiered-package pricing model is anticipated — it
   reads as transcribed from one restaurant's own existing catering form,
   and no lead, ticket, or observation on this board names a restaurant
   asking for per-person package tiers.
4. **What does it displace?** Approver-facing WIP is already 5/2, over
   cap, before this G1. One `L` (Piece 1) displaces the backlog-grooming
   queue for about a week; all three `L`s would displace it for two to
   three weeks while `ENG-008`/`ENG-009`/`ENG-010`'s merge requests still
   sit unanswered.
5. **Would not building it be fine?** Building nothing is not fine — the
   page already promises a step it doesn't deliver, and catering is
   exactly the high-ticket, owned-customer lead type this business exists
   to keep off marketplaces. Building Piece 2 specifically could wait
   indefinitely and be fine: an owner holding an exact itemized order can
   quote it by phone in a minute, which already beats today's prose blob.

**Filter verdict:** build Piece 1. Defer Piece 2 behind an explicit
answer on price-book ownership. Piece 3 follows Piece 2.

## Decision

**Original G1** raised 2026-08-29, answered **`changed`**
2026-09-03T00:53:17Z — full rewrite, reproduced and analyzed above.

**Revised G1** (Piece 1, rescoped, this PRD) raised 2026-09-03 —
`inbox/2026-09-02-eng016-g1-rescope.md`. No dissent section: `agents/
critic/agent.md` does not exist at department or instance level (open
proposal `agents/eng-manager/proposals.md`, filed 2026-08-25, already
covers this — not re-filed), same as `ENG-017`'s G1.

- **The approver's answer:** approved
- **Date:** 2026-09-03T15:47:46.139489+00:00
- **Notes:** Full text: "Lets start with piece 1" (sic). Read plainly as
  approving Piece 1 exactly as scoped — structured order capture, itemized
  owner view, two automatic stages, no pricing shown — with no comment on
  the two riders this G1 carried (the 3-vs-2 stage-count resolution, the
  fulfillment-value remap question). Silence on a rider is not an
  objection to it; both stand as proposed. Pieces 2 and 3 remain named,
  not filed — "start with" reads as confirming the build order the
  recommendation proposed, not as authorizing them now. Piece 2 still
  waits on a named answer for who maintains each restaurant's price book.
