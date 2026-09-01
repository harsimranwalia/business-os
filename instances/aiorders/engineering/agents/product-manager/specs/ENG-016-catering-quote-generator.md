---
ticket: ENG-016
project: config-site-builder
status: awaiting-scope
size: L
author: product-manager
created: 2026-08-29
decided:
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
pipeline section can overall be improved and more automated with
autopilot's use for stage updates/ quote sent etc."

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
   catalog?** Addressed above under "Assumed" — proposed as à la carte
   reuse of the existing menu, correctable at G1.

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
  modal) — five hardcoded status strings in three separate files (`New
  Enquiry`, `Contacted`, `Not Interested`, `Finalized`, `Completed`),
  no server-side enum, so adding a sixth ("Quote Sent") is an additive
  frontend change, not a schema migration.
- `aiorders-api/supabase/functions/brand-portal/catering.ts`: the backend
  behind that kanban — `get_catering_requests`, `update_catering_request`,
  and `get_catering_dashboard_stats` (the latter computing `cateringIncome`
  as `number_of_guests * 34`, a flat estimate unrelated to real menu
  pricing — see Assumed above). Also confirms `restaurants.live_catering`
  /`party_hall` are existing per-restaurant boolean settings, the same
  pattern a new "Auto-quote" setting would follow.
- `aiorders-api/supabase/functions/autopilot/` and
  `.../autopilot/marketing/README.md`: a real, mature, already-shipped
  automation engine — DB-trigger-initiated, queued through Cloudflare
  Queues, sent via the `outgoing-communications` edge function, with
  per-restaurant customizable templates (`communication_templates`,
  `trigger_type`, `email_enabled`/`sms_enabled`, templated variables) and a
  `communication_log`. Today it only fires on customer lifecycle events
  (welcome/first-order/every-order/birthday/winback) — nothing catering-
  related. This is the concrete "autopilot" the request names, and it is
  the natural engine to extend for deeper pipeline automation, not
  something this ticket needs to build from scratch — but wiring a new
  domain (catering) into it is real, separable work, not a one-line
  addition, hence its own later item rather than folded in here.
- `restaurant-marketplace/src/hooks/useCatering.tsx` and
  `aiorders-api/.../restaurant-marketplace/handlers/catering.ts`: confirm
  the marketplace's catering path is genuinely separate code, not a thin
  wrapper over the same function — supporting the "config-site-builder
  only" scoping above rather than assuming it.

## Problem

A restaurant's catering leads currently dead-end at "thanks, we'll be in
touch": the owner gets notified and a CRM record is created, but every
quote after that depends entirely on a staff member manually pricing the
order and replying by phone or email. There's no automated next step, no
computed price, and no record of a quote ever having existed — so a lead
that isn't followed up on quickly just goes cold, and the "catering
pipeline" a staff member sees is only ever updated by hand.

## Why now

Approver-initiated; no specific lead or restaurant named as lost, no
stated deadline. The underlying gap is concrete and code-confirmed (see
Evidence) rather than anticipated.

## Users

Two audiences on two different surfaces: the **customer**, on a
restaurant's public website, who wants a price without waiting for a
callback; and the **restaurant owner/staff**, on `restaurant-portal`, who
want the catering board to reflect what's actually happened without
updating it by hand for every enquiry.

## Proposed change

After this ships:
- A restaurant owner can turn on "Auto-quote" for their catering page
  (default off — nothing changes for a restaurant that doesn't touch this).
- With it on, a customer who submits the existing catering enquiry form
  receives a link by SMS and/or email to a new quote-builder page. There
  they pick items and quantities from the restaurant's own menu and see a
  computed subtotal before submitting — or they can skip straight to
  today's plain "have someone contact me" option instead.
- With it off (the default), the customer's experience is exactly what it
  is today.
- Either way — quote submitted, or skipped — the matching request's stage
  on restaurant-portal's catering board updates on its own, and, if a quote
  was built, the owner can see exactly what was selected and its computed
  total from the existing request detail view.

This ticket does not cover editing/resending an already-sent quote, a
catering-specific pricing model, or wiring this into the general
`autopilot` trigger/template system — see Non-goals.

## Acceptance criteria

1. `[stated]` Given a restaurant with "Auto-quote" enabled, when a customer
   submits the catering enquiry form, then they receive a link to a
   quote-builder page by SMS and/or email.
2. `[stated]` Given the quote-builder page, when the customer selects menu
   items and quantities, then a computed subtotal is shown before they
   submit.
3. `[inferred]` Given the quote-builder page, when the customer doesn't
   want to build a quote themselves, then they can choose a plain
   alternative that behaves like today's "someone will reach out" message.
4. `[stated]` Given a restaurant with "Auto-quote" disabled (the default),
   when a customer submits the enquiry form, then nothing about their
   experience changes from today — no quote-builder link is sent.
5. `[inferred]` Given a customer completes the quote-builder page, or
   chooses the skip option, then the matching request's stage on
   restaurant-portal's catering board updates automatically, without a
   staff member setting it by hand.
6. `[inferred]` Given a submitted quote, then the restaurant owner can view
   the selected items, quantities, and computed subtotal from the existing
   catering request detail view.
7. `[proposed]` Given the quote-builder link, when it's opened, then it
   resolves to the correct restaurant and catering request without
   requiring the customer to log in, and cannot be used to view or modify
   a different customer's request.
8. `[inferred]` Given a request to read or write the new quote/settings
   data made by a non-owner/non-staff caller, then it's rejected by the
   same authorization pattern the existing catering endpoints already use.

## Non-goals

- **Owners editing an already-sent quote and resending it** — depends on
  this ticket's quote data existing first; a real, separate, later item
  (`stated, deferred` above).
- **A catering-specific pricing model** (per-person tiers, package
  minimums, delivery/service fees) — this ticket reuses the existing
  menu's own per-item prices, à la carte. See Assumed/Second reading above.
- **Wiring this into the general `autopilot` trigger/template engine** so
  restaurants can customize the quote-sent message or add follow-up
  reminders — real and explicitly named by the approver, but a separate
  piece of work extending an existing system into a new domain, not a
  one-line addition. A later item, not this one.
- **`restaurant-marketplace`'s and the CloudWaitress popup's own,
  separate catering-request paths** — out of scope; see Assumed above.
- **Payment, deposits, or booking/acceptance of the quote** — nothing in
  the request describes money changing hands through this flow.
- **Changing the meaning or order of the existing five catering statuses**
  — only additive (one new "Quote Sent"-style value); the other five are
  untouched.

## Risks and unknowns

- **The two named forks above** (who controls the fallback path; menu
  reuse vs. a catering-specific pricing model) — both resolved with a
  stated default in this PRD, correctable at G1 rather than blocking it.
- **Unauthenticated public link security.** The quote-builder link has to
  work without a login, scoped to exactly one catering request. `catering.id`
  is already a UUID, which is a reasonable base, but the exact
  token/expiry scheme is a design-time decision — flagged for the
  architect, possibly its own G2 if a materially new token mechanism turns
  out to be needed.
- **Consent scope.** The existing enquiry form's consent notice covers
  contacting the customer by email/SMS; this ticket assumes that already
  covers an automated quote-link message rather than only a human
  reaching out, worth the architect confirming rather than this PRD
  asserting it outright.
- No specific restaurant or lead named as affected today; no stated
  deadline.

## Cost

- Build: `L` — a new customer-facing page and flow (`config-site-builder`),
  a new backend surface for quote storage, link generation, and
  SMS/email send reusing the existing `outgoing-communications`/`autopilot`
  path (`aiorders-api`), and one additive status value plus a small
  detail-view addition on the already-shipped kanban (`restaurant-portal`).
  Three repos, one genuinely new data shape (a quote). Rough band: several
  days to a week.
- Run: `$0/month` expected — reuses the already-contracted unlimited-SMS
  vendor (`ENG-006` G1) and the existing outgoing-communications send
  path; flag to devops/CFO only if design time surfaces an actual new
  per-message cost.

## Decision

**Raised** 2026-08-29 (`scheduled` event pass, context `schtasks`) —
`ENG-014` and `ENG-015` have both since cleared their own G1s (both at
`designed`), freeing the approver-facing WIP cap (2) back to 0/2. G1 sent:
`inbox/2026-08-29-eng016-g1-scope.md`. Awaiting the approver's decision.

- **The approver's answer:** —
- **Date:** —
- **Notes:** —
