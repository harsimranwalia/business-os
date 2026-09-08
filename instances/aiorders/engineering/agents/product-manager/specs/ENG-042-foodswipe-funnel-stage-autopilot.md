---
ticket: ENG-042
project: aiorders-api
status: awaiting-scope
size: L
author: product-manager
created: 2026-09-06
decided:
---

# Foodswipe funnel — stage-triggered autopilot email/SMS

## Readback

**Raw input** — the second half of the approver's `changed` answer on
`ENG-028`'s G1 (`inbox/_handled/2026-09-03-eng028-g1-scope.md`, decided
2026-09-06T09:09:08.947929+00:00), verbatim:

> "Can we have autopilot email/sms setup on admin panel like brand portal
> for each stage update"

**This PM's reading, grounded in the live repos.** An automation that,
when a Foodswipe listing's stage changes, sends a templated email and/or
SMS without a staff member composing or sending it by hand — configured
from a new admin-hub screen, modeled on `restaurant-portal`'s existing
`Autopilot` section (`src/pages/autopilot/{Automations,Broadcasts,
Templates}.tsx`, a trigger → message → review wizard) and backed by a
*parallel* trigger set on `aiorders-api`'s send layer, not the existing
`autopilot` function's own tables. Checked before assuming reuse was free:
`supabase/functions/autopilot/utils/triggers.ts`'s `TriggerType` is a
closed, hardcoded enum of restaurant/order-lifecycle events
(`order_completed`, `abandoned_cart`, `birthday`, `new_catering_lead`, six
more), each with its own hardcoded template variables
(`customer_name`, `restaurant_name`, `order_number`). None of it applies to
a Foodswipe listing, which has no restaurant at the early stages and never
has an order. Same finding `ENG-017`'s own design already made for the
presignup-leads pipeline: **the reusable part is the send layer
(`sendEmail`/`sendSMS`), not the trigger/template data model.**

**Blind reading** (subagent, raw request + `knowledge/business-profile.md`
only, no repo access, no exposure to this reading). Converged
independently on the same core mechanism — stage-change-triggered,
templated, admin-configured, modeled on an existing pattern. **No material
divergence on what's being asked.** It surfaced four specifics worth
carrying forward rather than silently deciding:

- **Recipient isn't stated** — the listing's own contact (external) vs. the
  staff member who owns it (an internal alert) vs. both. Read here as
  **external**, matching every other use of "autopilot" in this codebase
  (birthday/winback/welcome/order messages all go to the external
  customer, never to staff) — named because it's the one reading that
  would make this a different, smaller ticket if wrong.
- **Consent/compliance** — independently raised the same CASL-shaped
  exposure `ENG-017`'s own design already found and fenced off (a global
  off-by-default switch plus a per-contact consent flag) for the sibling
  presignup-leads pipeline. Treated as **confirmed**, not speculative, on
  that precedent — not re-derived from scratch.
- **Trigger semantics** — fire once when a listing enters a stage, or on
  every save (risk of a duplicate send if a listing bounces backward and
  forward between two stages, which this pipeline's own `On Hold` stage
  makes a real path, not a hypothetical one).
- **Contact-data quality at early stages** — a listing sitting in an early
  stage may have no verified email or phone at all. Grounded in
  `ENG-028`'s own evidence: the *current* `account_created` stage is
  defined as "doesn't yet have both a name and a phone" — the new pipeline's
  early stages (`Waitlisted`, `Contacted`) carry the same risk under a new
  name.

## Problem

Foodswipe listings move through a sales pipeline entirely by a staff
member's own memory and typing — nobody is told a stage changed, and no
follow-up message goes out unless a person writes and sends one by hand.
`restaurant-portal` already gives brand managers exactly this capability
for their own customer lifecycle (order completed, abandoned cart,
birthday, and more); the admin panel's sales staff have no equivalent for
the pipeline they work every day.

## Outcome

When an authorised staff member attaches a template and a channel to one
of `ENG-028`'s nine Foodswipe stages, a listing entering that stage
automatically sends that message to its own contact — no staff member
drafts or sends it by hand. Sending is off by default, per stage and per
listing, until both a template exists and consent is on file: nothing
sends silently on the day this ships.

## Users

AIOrders sales and onboarding staff working the Foodswipe funnel — the
same staff `ENG-013`/`ENG-028` serve — and, as the message's actual
recipient, the Foodswipe listing's own contact: a restaurant considering or
mid-onboarding, not yet a live `restaurant-portal` customer.

## Proposed change

A new admin-hub screen lets staff attach a template and a channel (email,
SMS, or both) to any of `ENG-028`'s nine stages, following the same
trigger → message → review shape as `restaurant-portal`'s `Autopilot`
wizard. A listing entering a configured stage sends that template once,
reusing the platform's existing `sendEmail`/`sendSMS` primitives directly
rather than the restaurant-scoped `autopilot` function's trigger/template
tables, which don't fit a Foodswipe listing (see Readback). Consent and a
global kill switch gate every send, both defaulted **off**, mirroring
`ENG-017`'s own unresolved-legal-question handling rather than deciding it
here.

## Acceptance criteria

1. `[stated]` Given a stage with a template and channel configured, when a
   listing enters that stage, then the configured message sends once to
   the listing's own contact.
2. `[stated]` Given a stage with no template configured, when a listing
   enters it, then nothing sends — silence is the default, not an error.
3. `[proposed]` Given a listing that re-enters a stage it already passed
   through, when that stage's automation is still configured, then it does
   not send a second time for the same listing — proposed: once per
   listing per stage, ever, not once per entry. A real design question, not
   resolved here (see Risks).
4. `[inferred]` Given a caller without admin access to this page, when they
   attempt to configure or view an automation, then it is rejected by the
   same authorisation gate the funnel's existing endpoints already use.
5. `[proposed]` Given a listing with no consent on file, when it enters a
   configured stage, then no message sends regardless of configuration —
   consent gates every send, not only the global switch.
6. `[proposed]` Given the global autopilot switch for this funnel is off,
   when any listing enters any configured stage, then nothing sends —
   checked at send time, not only at configuration time.
7. `[inferred]` Given a listing's contact has no email or phone on file for
   the channel a template uses, when it enters that stage, then the send
   is skipped and logged — never retried indefinitely, never thrown as an
   error that blocks the stage change itself.

## Non-goals

Building this into the existing `autopilot` Supabase function or its
`TriggerType`/template tables — the data model doesn't fit (Readback).
A rules engine beyond "stage X triggers message Y" — no branching, no
delays, no multi-step sequences (`ENG-017` may want this too, someday, as
its own ticket). Resolving whether Foodswipe listings have standing
consent to be messaged at all — the same open legal question `ENG-017`
already carries for a sibling pipeline, fenced off here the same way
(default off) rather than answered twice independently. An audit/reporting
screen (`restaurant-portal`'s `BroadcastReport.tsx` equivalent) — a real
feature if wanted later, not asked for. Internal staff notifications on
stage change — a different, smaller feature, and not what "autopilot"
means anywhere else in this codebase (flagged as a risk below, not
assumed). Which nine stages exist or what they're named — that's
`ENG-028`; this ticket's trigger vocabulary is whatever that ticket ships
with.

## Risks and unknowns

- **Recipient assumed external, not confirmed.** Read as the listing's own
  contact, matching every existing use of "autopilot" in this codebase. If
  the approver meant an internal alert to the staff member who owns the
  listing instead, this is a different, smaller ticket (a notification,
  not a nurture message) — worth confirming at this gate rather than
  building the wrong one.
- **Consent is unresolved, not just unbuilt.** Same CASL-shaped gap
  `ENG-017`'s design already named for presignup leads: nothing confirms a
  Foodswipe contact agreed to be emailed or texted. Shipping with a global
  switch and a per-contact flag, both defaulted off, ships the mechanism
  without deciding the legal question — consistent with how `ENG-017`
  handled the identical gap, not a new call invented here.
- **Fire-once semantics are a real design question, not a detail.** A
  listing bouncing between two stages (e.g. `On Hold` back to
  `Follow Up`) could otherwise re-trigger the same message repeatedly.
  Criterion 3 proposes "once per listing per stage, ever" as the safer
  default; the architect's call at `designed`.
- **Contact-data completeness at early stages.** `Waitlisted`/`Contacted`
  listings may have no verified email or phone yet. A channel with no
  destination has to skip cleanly, not error.
- **Depends on `ENG-028`'s final stage list, not just its shipping.** This
  ticket's own trigger vocabulary is keyed on stage names `ENG-028` hasn't
  finished confirming — its own fresh G1 is still open as of this ticket's
  filing. `depends_on: [ENG-028]` covers build order; a stage rename after
  this ticket starts building would still require a matching rename here.
- **No dissent section** — `agents/critic/agent.md` still doesn't exist at
  department or instance level, same gap every G1 on this board has
  recorded; not refiled, the open proposal (`proposals.md`, 2026-08-25 row)
  covers it.

## Cost

- **Build: `L`** — several days to a week, sized against `ENG-017`'s own
  near-identical shape (a new admin-hub UI section modeled on the same
  `Autopilot` wizard, a parallel trigger/template data model, consent/
  kill-switch plumbing) rather than estimated fresh. Cross-project
  (`aiorders-api` for the trigger/send logic, `aiorders-admin-hub` for the
  configuration screen) and a new data model each independently trigger
  `L` on this board's own size table.
- **What it displaces:** nothing at build time. `depends_on: [ENG-028]`
  means it cannot enter `building` until that ticket ships, so it sits at
  `designed` or earlier without holding the machine WIP slot.
- **Run: `$0`/month** — reuses the existing `sendEmail`/`sendSMS`
  primitives and their already-contracted vendor; no new vendor, no new
  metered call.

## Recommendation

**Shape and size now; build after `ENG-028` ships.** The ask is real,
well-precedented by `restaurant-portal`'s own `Autopilot` section, and —
per the blind reading above — not materially ambiguous about what's
wanted, only about four specifics worth confirming rather than guessing:
recipient (proposed: the listing's own contact, external), consent
handling (proposed: off by default, same as `ENG-017`), fire-once
semantics (proposed: once per listing per stage), and contact-data gaps
(proposed: skip and log, never error). None of the four changes whether to
build; the first two would change what gets built if the proposed default
is wrong.

## The 5-question filter, answered honestly

1. **Off the plate or onto it?** Onto it — a new automation someone has to
   configure, template, and eventually debug when a send doesn't fire.
   Removes a manual-follow-up tax from sales staff.
2. **Freedom created or removed?** Creates freedom (staff stop needing to
   remember to follow up); removes none — every send stays off until
   explicitly configured, and consent gates every one on top of that.
3. **Current or anticipated?** Current — asked directly, the same pass
   `ENG-028`'s own scope was answered, not speculative.
4. **What does it displace?** Nothing today (blocked on `ENG-028` for build
   order); at `designed` it sits alongside this board's other already-
   `designed` tickets, none of which it jumps ahead of.
5. **Would not building it be fine?** For now, yes — a workaround exists
   (staff message contacts manually, same as today) — but the approver
   asked for it directly and it is well-precedented elsewhere in the
   product, so deferring it is a sequencing choice, not a rejection.

**Filter verdict: shape it now (this PRD), gate it now (G1), build it once
`ENG-028` ships.**

## Decision

Filled in by the approver.
