---
ticket: ENG-017
project: aiorders-api
status: awaiting-scope
size: L
author: product-manager
created: 2026-08-29
decided:
---

# Autopilot nurture for the presignup sales lead pipeline — stage-triggered email/SMS

## Readback

**You said:** "no autopilot on admin panel for our sales staff/ resellers to
use . how can we demonstrate to a client what we sell if we dont have it
for us. have a proper fully demonstration account on how all aiorders work.
also autopilot nurturing for resellers/sales/admin staff on admin panel
which works based on stages update/ auto nurturing ."

**Understood as:** This one raw request bundles two separable asks (see
Second reading below) — this PRD covers only the "autopilot nurturing...
which works based on stages update" half. A website visitor who fills out
AIOrders' own "become a client" form lands in a flat `leads` table with no
stage and no follow-up mechanism — nothing chases them, and nothing tells
staff which ones are worth prioritizing. You want that lead to carry a
stage, and for a stage change to automatically fire an email/SMS nurture
message, the same way the platform already automates marketing for a
*restaurant's* customers — pointed at AIOrders' own sales pipeline instead.

**Assumed, and worth correcting if wrong:**
- **This ticket is scoped to the `leads` table only** — the presignup,
  not-yet-signed-up prospect a sales rep is trying to close. It does **not**
  extend nurture triggers to the Brands-page client stage (`ENG-011`,
  `ready`) or the Foodswipe funnel stage (`ENG-013`, `ready`) — those are
  different entities (already-signed-up restaurants), each with its own
  in-flight ticket, and wiring nurture into all three at once would
  materially change this ticket's size. Proposed as a rider: build the
  presignup pipeline now (below), extend nurture to the other two stage
  fields as a separate, later, evidence-sized item if wanted.
- **"Sales staff/admin staff" means the existing `admin`/`sub-admin`
  roles** — no distinct "sales" role exists anywhere in
  `aiorders-admin-hub` (`AuthContext.tsx`'s role union is `admin |
  sub-admin | influencer | restaurant | brand | partner-admin |
  partner-user`), and the Leads page + its backend handler already gate on
  exactly `admin`/`sub-admin` today.
- **"Resellers" means `partner-admin`/`partner-user`** (this codebase's
  existing name, confirmed at `ENG-015`) — **and reseller access to this
  lead-nurture tool is proposed OUT of this ticket**, not silently granted.
  There is no mechanism anywhere in `aiorders-api` that attributes a
  website lead to a specific reseller — no referral code, no `partner_id`
  on the `leads` table, nothing a reseller's own prospects could be scoped
  by. Giving partner roles access today would mean every reseller sees
  every lead platform-wide, the exact cross-tenant shape `ENG-015` is
  currently fixing on a *different* page. Building real attribution
  (how does a lead get credited to a reseller in the first place — a
  referral link? a dropdown at signup?) is separate, non-trivial scope.
  This ticket ships the nurture engine for internal `admin`/`sub-admin`
  staff now; reseller access is named as follow-up work, not built here.
- **Channels: email and SMS**, matching what the existing engine already
  sends and what's already commercially covered (`ENG-006` G1: an
  unlimited-SMS vendor at a fixed monthly cost is already in place).
  WhatsApp exists as a send service (`outgoing-communications/services/
  whatsapp.ts`) but isn't proposed as in-scope unless asked for.
- **This is a new, parallel trigger/template layer, not an extension of
  the existing restaurant-facing one** — see Evidence. The existing
  `communication_templates` table is hard-scoped to `restaurant_id` and
  `trigger_type` is a closed enum of restaurant-customer lifecycle events
  (`new_customer_welcome`, `abandoned_cart`, `birthday`, …); a presignup
  lead has no `restaurant_id` and isn't a customer of any restaurant, so
  it cannot be enrolled through that data model as-is. What *is* reusable:
  the underlying send services (`email.ts`, `sms.ts`, `template.ts`) and
  the `outgoing-communications` function's existing `actor: 'admin'` route
  — present in the router already, but its three handlers
  (`sendSystemAlert`, `sendUserSignupNotification`, `sendErrorNotification`)
  are all unimplemented `TODO` stubs today, not a working precedent to
  build on top of.
- **Consent is a real, unresolved gap, not a formality.** The website form
  that creates a `leads` row (`aiorders-website/index.ts`'s `saveLead`)
  captures name/email/phone/business details and nothing else — no
  consent flag of any kind, unlike the catering-request flow, which
  explicitly sets `consent_sms`/`consent_email: true` on the CRM customer
  it creates. AIOrders is a Canadian business; CASL (Canada's anti-spam
  law) governs automated commercial email/SMS to a person, and "they
  filled out a contact form" is a materially weaker consent basis than an
  explicit opt-in checkbox. Proposed as an acceptance criterion below
  (add a consent notice/checkbox to the lead form) rather than shipping
  automatic nurture sends on an undocumented consent basis.

**Second reading agreed / diverged on:** This PM's reading, grounded in the
live code cited throughout, plus a blind architect reading (subagent,
`opus`, raw request + `knowledge/business-profile.md` only — no repo
access, no exposure to this PM's own reading). **No material divergence**
— both independently read the raw request as **two** bundled asks (a
demonstration account, and stage-triggered nurture automation), both
independently identified "autopilot" as the existing customer-marketing
engine redirected at a second audience, and both independently flagged
reseller/sales-vs-admin scoping as a real, load-bearing prerequisite rather
than a detail. The architect's blind reading additionally, and
unprompted, raised CASL-style consent exposure for cold-lead messaging —
checked against the live form and confirmed real (see Assumed above) — and
flagged that a nurture message needs a send-as identity, throttling, and
an unsubscribe path, which this PRD folds into Risks and a proposed
acceptance criterion rather than treating as a new divergence to ask about.
The demonstration-account half of the architect's reading is carried into
`ENG-018`, filed alongside this ticket from the same request.

## Problem

A prospective restaurant owner who fills out AIOrders' own "become a
client" website form becomes a row in a `leads` table with no stage, no
priority, and no automated follow-up of any kind — confirmed in code, not
assumed: the table has no status/stage column, and nothing ever reads a
lead to decide whether or how to contact it again after the one-time
staff notification path. Whether a lead ever gets a second touch depends
entirely on a staff member remembering to chase it by hand. This is the
same gap `ENG-013`'s own standing question surfaced and the approver
already answered directly (see Notes) — this request restates and
broadens it.

## Why now

Approver-initiated, and answered twice: once narrowly, as a standing
question under `ENG-013` ("autopilot built to nurture these leads to next
stages automatically and send them emails/sms to nurture" — approved,
2026-08-29T11:46:34), and again here, more broadly, a few hours later. No
specific lost deal named; the underlying gap (no stage, no follow-up) is
concrete and code-confirmed rather than anticipated.

## Users

Internal `admin`/`sub-admin` staff working the Leads page — today they can
view and hand-edit a website lead, but have no way to signal "this one
needs a nurture touch" beyond doing it manually. Reseller (`partner-admin`
/`partner-user`) use is named in the raw request but proposed as
out-of-scope for this ticket — see Assumed.

## Proposed change

After this ships:
- Every website lead carries a stage — proposed taxonomy: **New → Contacted
  → Interested → Signed Up / Lost** (four working stages plus a terminal
  pair), staff-settable from the Leads page, defaulting to **New** for
  every existing and future lead.
- Moving a lead into a stage flagged for nurture (proposed: **Contacted**
  and **Interested**) automatically sends that lead a templated email
  and/or SMS, reusing the platform's existing send services rather than a
  new vendor integration.
- Every automated send is logged and visible to staff, the same
  auditability the restaurant-facing `autopilot` log already gives.
- A lead that converts (signs up for real, becoming a `profiles` row)
  stops receiving lead-nurture messages — no double-messaging a real user
  through two systems at once.
- The website lead form gains a consent notice/checkbox before this ships,
  so automated nurture sends rest on the same explicit-consent footing the
  catering flow already uses, not on an unexamined implied-consent
  assumption.

This ticket does not build reseller access, does not extend nurture
triggers to the Brands-page or Foodswipe-funnel stage fields, and does not
build a new outbound channel — see Non-goals.

## Acceptance criteria

1. `[confirmed]` Given a website lead, when a staff member (`admin`/
   `sub-admin`) views the Leads page, then they see a stage value,
   defaulting to "New" for leads that don't have one set yet.
2. `[confirmed]` Given a lead, when a staff member changes its stage, then
   the change saves and is reflected immediately on the page.
3. `[confirmed]` Given a lead's stage changes to a stage flagged for
   nurture (proposed: Contacted, Interested), then a templated email
   and/or SMS is sent to that lead automatically, reusing the existing
   send services rather than a new integration.
4. `[proposed]` Given an automated nurture send, then it is logged
   (recipient, template, channel, timestamp) and visible to staff from the
   admin panel.
5. `[inferred]` Given a lead that has since signed up for a real account,
   then it no longer receives lead-nurture messages.
6. `[proposed]` Given the website lead-capture form, when a visitor
   submits it, then they see a consent notice covering automated
   email/SMS follow-up, and that consent is what gates whether this
   ticket's automated sends may fire for that lead.
7. `[inferred]` Given a request to read or write lead-stage or nurture data
   made by a caller who isn't `admin`/`sub-admin`, then it's rejected —
   including `partner-admin`/`partner-user`, consistent with this ticket's
   proposed scope (see Non-goals).

## Non-goals

- **Reseller (`partner-admin`/`partner-user`) access to leads or the
  nurture tool** — no existing mechanism attributes a lead to a specific
  reseller; building that attribution is separate, materially different
  work. See Assumed.
- **Extending automated nurture to the Brands-page client stage (`ENG-011`)
  or the Foodswipe funnel stage (`ENG-013`)** — different entities,
  already-signed-up restaurants, each with its own in-flight ticket. A
  later item if wanted, not assumed into this one.
- **A new outbound channel** (WhatsApp, push, etc.) — email/SMS only,
  matching the already-contracted vendor.
- **Retroactively messaging every existing lead the moment this ships** —
  nurture fires on a *stage change* going forward; this ticket doesn't
  define a one-time backfill campaign against the current backlog of
  leads (a separate, marketing-owned decision, not an engineering default).
- **Extending the general restaurant-facing `communication_templates`/
  `trigger_type` model** to cover leads — this ticket builds a parallel,
  lead-shaped structure instead; see Evidence/Assumed for why the existing
  one doesn't fit.

## Risks and unknowns

- **Consent basis, named above rather than assumed away.** Adding the
  consent notice is proposed as part of this ticket (acceptance criterion
  6) specifically because shipping automated commercial messaging to cold
  leads without it is a real compliance exposure for a Canadian business,
  not a hypothetical one.
- **Send-as identity, throttling, and unsubscribe** — the architect's blind
  reading flagged all three as necessary for any outbound nurture system;
  this PRD treats them as implementation detail for the architect to
  design against rather than approver-facing forks, but they are real
  scope, not free.
- **Exact stage taxonomy and which stages trigger nurture** are proposed
  defaults above, correctable at G1.
- **This ticket's true cost depends on how much of the existing send
  plumbing (queueing, template storage, logging) can be reused versus
  needs a parallel implementation** — sized as `L` on the assumption that
  the *services* are reusable but the *data model* isn't; the architect
  may narrow this at design time.
- No specific lead or lost deal named as evidence; the gap is structural
  and code-confirmed rather than measured against a real loss.

## Cost

- Build: `L` — a new stage column and staff-facing control on an existing
  page (`aiorders-admin-hub`), a new lead-shaped trigger/enrollment/log
  data model reusing existing send services rather than
  `communication_templates` (`aiorders-api`), and a consent-capture
  addition to the public lead form. No new vendor. Rough band: several
  days to a week.
- Run: `$0/month` expected — reuses the already-contracted unlimited-SMS
  vendor and existing email send path; flag to devops/CFO only if design
  time surfaces a real new per-message cost.

## Decision

**Raised** 2026-08-29 (`scheduled` event pass, context `schtasks`) —
`ENG-014` and `ENG-015` have both since cleared their own G1s (both at
`designed`), freeing the approver-facing WIP cap (2) back to 0/2. G1 sent:
`inbox/2026-08-29-eng017-g1-scope.md`. Awaiting the approver's decision.
Filed alongside `ENG-018` (the demonstration-account half of the same raw
request) — see that PRD for the sibling scope.

- **The approver's answer:** —
- **Date:** —
- **Notes:** —
