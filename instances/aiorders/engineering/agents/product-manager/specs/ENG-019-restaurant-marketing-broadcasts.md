---
ticket: ENG-019
project: restaurant-portal
status: approved
size: L
author: product-manager
created: 2026-08-29
decided: 2026-09-03T15:52:30.648626+00:00
---

# Restaurant marketing broadcasts — mass send and drip sequences for the brand portal

## Readback

**You said:** "client/brand page/portal  autopilot on brand portal does not
have mass/ drip campaign options for client/restraurant to use to send for
any new menu drop or holiday

they cant schedule or run any manual campaigns for their data and
generate/track roi of the campaigns"

**Understood as:** Restaurant owners on the brand portal want to message
their own customers on their own initiative — a one-time blast or a
multi-step drip, for an occasion they choose (a new menu item, a holiday) —
either sent right away or scheduled for later, and then see whether it
actually produced orders. Today the only customer-messaging system on the
brand portal (`Automations`) is entirely reactive: every send is triggered
automatically by a customer-lifecycle event, and nothing lets an owner act on
their own list on their own timing.

**Assumed, and worth correcting if wrong:**
- **"Campaign" here means a customer-facing marketing message/sequence — not
  the brand portal's existing "Campaigns" nav item**, which is a real,
  already-shipped, unrelated feature: inviting influencers to visit and post
  about the restaurant (`influencer_campaigns` table, `Create Campaign` →
  "Start promoting your restaurant by inviting influencers..."). Confirmed by
  reading the page and its service layer directly, not assumed from the
  name. This ticket does not touch that feature and proposes a different
  label for the new one (working name: "Broadcasts") to avoid the collision
  — correctable at G1.
- **Audience is the restaurant's own existing customer list** (already
  populated from orders, the same list the `Customers` page shows). Proposed
  v1: send to all customers, or narrow to customers who haven't ordered in a
  chosen number of days (the underlying `last_order` data already exists on
  every customer record). A fuller segment/list builder is proposed as later
  work, not built here — see Non-goals.
- **Channels: email and SMS**, matching every send path this platform
  already has. No new channel implied by the request.
- **"Generate/track ROI" is proposed as: a campaign can carry a coupon
  code**, reusing the exact mechanic the existing welcome/first-order/
  every-order offers already use (`offers.coupon_code`), and the campaign's
  own page shows redemptions and the revenue behind them. A deeper
  measurement layer — open/click tracking, attribution for a campaign with
  no code attached — is proposed as later work, not this ticket. See
  Non-goals.
- **Content is owner-authored**, not generated from the menu catalog. The
  business is positioned as "AI-powered marketing," which makes
  auto-drafted content a plausible future request, but the raw request's own
  verb is "send," not "write" — proposed out of scope for this ticket.
- **A drip is a sequence of owner-authored steps with owner-set spacing**
  (e.g., immediately, +3 days, +7 days), started once per customer at
  enrollment — a new, parallel mechanism, not a new trigger type bolted onto
  the existing reactive `Automations`, which keeps working exactly as it
  does today.

**Second reading agreed / diverged on:** This PM's reading, grounded in the
brand portal, admin hub, and `aiorders-api` code read directly (see Assumed
above), plus a blind architect reading (subagent, `opus`, raw request +
`knowledge/business-profile.md` only — no repo access, no exposure to this
PM's own reading). **No material divergence** — both independently converged
on the same core shape: a self-service send capability layered beside the
existing reactive automation engine, a new campaign/audience/scheduling data
model, and an ROI mechanism that doesn't exist today. The architect's blind
reading additionally, unprompted, raised several real risks, folded into
Risks below rather than treated as a divergence to ask about: CASL consent
exposure (real, but lower-stakes here than `ENG-017`'s cold leads, since this
audience already has a prior order relationship with the restaurant);
cross-tenant scoping (this codebase has a confirmed history of exactly this
bug class — `ENG-015`); the need for durable scheduling infrastructure
rather than an in-process timer; and whether a restaurant-initiated send
needs an extra approval step. That last one resolves cleanly, not as a real
fork: this repo's own human-approval constitution governs business-os's own
outbound content (the Reddit bot), not features the AIOrders product exposes
to its own paying restaurant customers — a restaurant sending to its own
list is the product's normal function, no different from an owner activating
an existing Offer today.

## Problem

Restaurant owners on the brand portal cannot message their own customers
except when the platform's automatic triggers fire (welcome, order,
abandoned cart, birthday, feedback). An owner who wants to tell customers
about a new menu item or a holiday promotion — on their own timing, for their
own reason — has no in-product way to do it, and no way to see whether a past
send earned anything back. No specific lost-revenue figure is attached to
this; the gap itself is confirmed in code (see Assumed) and reaches this
ticket as a direct complaint from a restaurant owner, relayed by the
approver.

## Why now

Approver-initiated. The gap sits close to the center of this business's own
positioning: `knowledge/business-profile.md` names "AI-powered marketing"
and "owned customer relationships" alongside commission-free ordering as the
three things AIOrders sells restaurants. Today the product delivers
automated triggers but nothing an owner can point at their own list on their
own terms — the "owned" half of "owned customer relationships" is
incomplete without it.

## Users

Restaurant owners and managers on the brand portal (`restaurant-portal`) —
the same roles who already use `Automations` and `Offers` today. Not
`partner-admin`/`partner-user` (agency/reseller) — proposed out of scope,
same reasoning `ENG-017` used: nothing today scopes a reseller to only their
own brands' sends, and `ENG-015` is already fixing a related cross-tenant
gap on a different page. Extending broadcast access to resellers is separate,
later work once that lands.

## Proposed change

After this ships, from the brand portal an owner can:
- Compose a one-time message (email and/or SMS) and send it immediately, or
  schedule it for a future date and time.
- Compose a drip sequence — two or more owner-authored steps, each with its
  own delay (e.g., immediately, +3 days, +7 days) — and start it for a
  chosen audience; each customer moves through the sequence once, from when
  they're enrolled.
- Choose the audience: all of the restaurant's own customers, or narrowed to
  those who haven't ordered in a chosen number of days.
- Attach a coupon code to a campaign, reusing the mechanic the existing
  offers already use, so redemptions and their order value show up on that
  campaign's own page.
- See, per campaign: how many customers it reached, delivery status per
  channel (reusing the existing send-log pattern from `Automations`), and —
  where a code is attached — redemptions and revenue.

This is additive. The existing reactive `Automations` are untouched and keep
firing exactly as they do today; this gives owners a second, self-initiated
path that reuses the same underlying email/SMS delivery.

## Acceptance criteria

1. `[stated]` Given a restaurant owner composing a one-time message, when
   they choose to send it, then they can send immediately or schedule it for
   a future date and time.
2. `[stated]` Given a restaurant owner composing a drip sequence of two or
   more steps, when it starts, then each step sends at its own configured
   delay after a customer's enrollment, once per customer.
3. `[inferred]` Given a campaign being composed, when the owner picks an
   audience, then they can choose "all customers" or "customers inactive for
   N days," scoped strictly to that owner's own restaurant — never another
   restaurant's customers.
4. `[proposed]` Given a campaign with a coupon code attached, when a
   customer redeems it, then the campaign's own page shows the redemption
   count and total order value attributed to it.
5. `[inferred]` Given any campaign send, when it goes out, then it's logged
   the same way existing automation sends are (channel, recipient, status,
   timestamp) and visible in that campaign's own history.
6. `[proposed]` Given any campaign email or SMS, when a customer receives
   it, then it includes a working unsubscribe/opt-out path, and an
   opted-out customer is excluded from every future campaign send
   regardless of audience selection.
7. `[inferred]` Given a request to read or send campaign data for a
   restaurant a caller doesn't belong to, then it's rejected server-side,
   not just hidden in the UI.

## Non-goals

- **Deeper ROI/attribution** — open/click tracking, attribution for
  campaigns that carry no coupon code, or any cost-basis/ROI-ratio
  calculation. This ticket ships redemption-and-revenue-by-coupon-code only,
  the mechanism the platform already has; a richer measurement layer is
  proposed as a later, separate ticket once this one is in use.
- **A segment/list builder beyond "all" or "inactive for N days."** A saved,
  multi-condition segment (spend tier, order frequency, items ordered) is
  real, later work.
- **AI-generated or menu-driven campaign content.** Composing is manual for
  this ticket; auto-drafting from the menu catalog is a natural follow-on,
  not assumed in.
- **Reseller (`partner-admin`/`partner-user`) access to broadcast tools** —
  same reasoning as `ENG-017`.
- **A new outbound channel.** Email and SMS only, matching every other send
  path on this platform today.
- **Any change to the existing reactive `Automations`** — this is additive
  only.

## Risks and unknowns

- **CASL consent**, named rather than assumed away. Unlike `ENG-017`'s cold
  leads, this audience is existing customers with a prior order — Canada's
  anti-spam law generally treats an existing business relationship as
  implied consent for a bounded period, materially better footing than a
  cold contact-form fill. Still worth a real legal check before relying on
  that reading; this PRD treats an unsubscribe path (acceptance criterion 6)
  as the baseline regardless of how that check lands.
- **Cross-tenant scoping.** This codebase has a confirmed, real history of
  exactly this bug class (`ENG-015` — a handler missing the role/brand check
  its sibling handler had). Acceptance criterion 7 exists because of that
  precedent, not generic caution.
- **Scheduling and drip delivery need a durable job, not an in-process
  timer** — the platform already runs a cron job for analytics
  (`platform_analytics_cron`) and per-message delays for automation sends,
  so the primitive isn't new to this codebase, but a multi-day drip on top
  of it is real design work, left to the architect.
- **Sizing assumes the existing send services (email/SMS/template) are
  reusable as-is**, and only the campaign/audience/scheduling data model is
  new — the same shape `ENG-017` used for lead nurture. If the architect
  finds the send layer needs changes to support a chosen-audience fan-out
  (versus today's single-recipient trigger sends), this ticket's cost grows.
- No specific restaurant or lost-opportunity named as evidence — the gap is
  structural and code-confirmed (see Assumed), not measured against a
  specific complaint beyond the raw request itself.

## Cost

- Build: `L` — a new campaign/audience/scheduling data model, an
  owner-facing composer and reporting UI (`restaurant-portal`), and a
  fan-out send path plus drip scheduler reusing existing send services
  (`aiorders-api`). No new vendor. Rough band: several days to a week+.
- Run: `$0/month` expected — reuses the already-contracted email/SMS
  delivery; flag to devops/CFO only if design time surfaces a real new
  per-message or per-job cost (e.g., a queue/cron tier change).

## Decision

- **The approver's answer:** approved
- **Date:** 2026-09-03T15:52:30.648626+00:00
- **Notes:** Bare approval, no comment — read as accepting every item in the
  Readback's "Assumed, correctable here" list as proposed (the "Broadcasts"
  working name, all/inactive-N-days audience only, email/SMS only, the
  coupon-code ROI mechanic, owner-authored content, owner/manager-only
  access), same convention this journal already applies to an unremarked-on
  rider or assumption (`ENG-013`'s stage-count assumption, `ENG-016`'s
  unremarked riders, `ENG-026`'s requirement 6). The Risks this PRD flagged
  as the architect's to resolve — durable scheduling/drip infrastructure,
  whether the existing send services need changes for a chosen-audience
  fan-out, and the CASL consent posture (better footing than `ENG-017`'s
  cold leads, but still worth a real check) — are not resolved by this
  approval and stay open, inherited at `designed`.
