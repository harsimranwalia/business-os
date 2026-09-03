---
ticket: ENG-020
project: restaurant-portal
status: approved
size: M
author: product-manager
created: 2026-08-29
decided: 2026-09-03T15:53:14.495206+00:00
---

# Marketing ROI reporting — traffic source and revenue attribution on the brand dashboard

## Readback

**You said:** "AI SEO no way to track if its useful or working on brand dasboard.
no roi from AI SEO or tracking how and where the customers are coming from .

we have started to install microsoft clarity on restaurant website but can
demostrate how aiorders is helping their business with increasing sales or roi
or any other metrics"

**Understood as:** Restaurant owners — and AIOrders staff on their behalf —
have no way to see, anywhere in the product, whether the AI-generated SEO
applied to a restaurant's website is doing anything: no view of where
customers actually come from (organic search, direct, social, referral, QR,
etc.), and no link from that traffic to actual orders or revenue. Microsoft
Clarity has started being installed on restaurant websites as an attempt to
answer this, but Clarity is a behaviour-analytics tool (heatmaps, session
replay) — it was never going to answer "is this making us money," and today
nothing inside AIOrders itself does either.

**Assumed, and worth correcting if wrong:**
- **"AI SEO"** means the existing admin-hub "Generate with AI" SEO tab (title,
  description, keywords, Open Graph tags — `RestaurantAIWebsite.tsx`/
  `BrandAIWebsite.tsx`) applied to a restaurant's `config-site-builder`
  website — not paid ads, not Google Business Profile.
- **"but can demostrate" is read as "but [cannot] demonstrate"** — the
  sentence is missing a negation. Both readings (this PM's own and a blind
  architect reading) independently converged on this, so it's named as an
  assumption rather than raised as a standing question.
- **"Brand dashboard"** means the brand portal (`restaurant-portal`) that
  restaurant owners themselves log into — the same surface `ENG-014`/`ENG-015`/
  `ENG-019` already use that name for.
- **Primary audience is the restaurant owner.** AIOrders staff wanting the
  same story for retention/sales conversations is real but proposed as a
  follow-on (a staff-facing rollup across all restaurants on the admin hub),
  not built here — the raw text names the owner-facing "brand dashboard"
  specifically.
- **"ROI" is scoped down to revenue by traffic source/channel**, not a true
  return-on-investment ratio — a real ROI figure needs each restaurant's
  AIOrders subscription cost on the other side of the ledger, which no
  analytics surface has. Same narrowing this board already applied to
  `ENG-019` ("generate/track ROI" → coupon-redemption-only).
- **Microsoft Clarity itself is proposed out of scope** — see Non-goals.

**Second reading agreed / diverged on:** No material divergence. This PM's
reading, grounded in live code across `aiorders-admin-hub`, `config-site-
builder`, `aiorders-api`, and `restaurant-portal` (see Problem below), plus a
blind architect reading (subagent, `opus`, raw request + `knowledge/business-
profile.md` only, no repo access, no exposure to this PM's own reading)
independently converged on the same core shape: a per-restaurant view, on the
brand portal, joining traffic source to order/revenue outcomes, with Clarity
named as the wrong tool for this specific question. The architect's blind
reading additionally, unprompted, raised several real risks — attribution
honesty, cross-domain cookie stitching, Canadian privacy-law exposure from
session recording, the lack of a pre-AI-SEO baseline, small-restaurant traffic
noise, and tenant isolation — folded into Risks below rather than treated as a
divergence to ask about.

## Problem

Restaurant owners cannot see, anywhere in the product, whether the AI-
generated SEO applied to their website is doing anything — no visibility into
where customers actually come from, and no link from that traffic to orders or
revenue. Confirmed in code, not assumed: the brand portal's `Dashboard`
(`restaurant-portal/src/pages/Dashboard.tsx`) and its only live analytics
service (`analyticsService.ts`, backed by `aiorders-api`'s `analytics` edge
function) report sales, orders, tips, dish counts, and repeat-customer
metrics — nothing about traffic source. The one page whose name suggests
otherwise, `pages/analytics/Index.tsx` ("Analytics"), is entirely mock data
about influencer-campaign performance (Instagram/TikTok/YouTube views,
applications, saves) — unrelated to website traffic or SEO, and worth not
confusing with this ticket (see Non-goals). Microsoft Clarity, the stopgap
already being installed, appears nowhere in any of the five repos — it isn't
integrated with AIOrders at all, and even fully integrated it only produces
behavioural analytics, never revenue attribution.

**The data this needs mostly already exists — this is a reporting gap, not a
capture gap.** Every customer-signup path this platform has — online order,
email signup, catering form, and a dedicated cross-subdomain tracking script
(`config-site-builder/public/tracking/user-tracking.js`) — already writes
`utm_source`, `utm_medium`, `utm_campaign`, `first_touch_source`,
`last_touch_source`, and `first_referrer` onto that customer's row
(`website-submissions/customer-signup.ts`, `email-signup.ts`,
`update-customer-tracking.ts`, `catering-request/index.ts`,
`crm/customers.ts`), and the marketing autopilot already reads
`first_touch_source` to branch its own welcome-email logic
(`autopilot/marketing/welcome.ts`). Nothing reads those columns back out to an
owner.

## Why now

Approver-relayed, from restaurant owners directly. This sits at the center of
what AIOrders sells — `knowledge/business-profile.md` names "AI-powered
marketing" and "owned customer relationships" as two of the three things
restaurants pay for, and an owner who can't see either working has no reason
to keep paying for them. The request is itself evidence: an owner installing a
third-party tool (Clarity) looking for this answer is telling AIOrders its own
product doesn't have it.

## Users

Restaurant owners and managers on the brand portal (`restaurant-portal`) — the
same audience `ENG-019`'s broadcast tools and the existing `Dashboard`/
`Offers` pages serve. AIOrders staff wanting the same numbers for account
management or sales conversations is real but named as a non-goal/follow-on
(see below) rather than bundled in.

## Proposed change

After this ships, from the brand portal a restaurant owner can see, for their
own restaurant:
- A breakdown of customers/orders/revenue by acquisition channel (organic
  search, direct, social, referral, paid, QR/in-store, marketplace-migrated,
  etc.), derived from the `utm_source`/`first_touch_source`/`first_referrer`
  data already captured on every customer.
- That breakdown over a selectable time range, so a trend (channel mix or
  channel revenue rising or falling) is visible, not just a single snapshot.
- Plain-language framing rather than a raw analytics dump — this is a trust
  artifact for a non-technical owner, not a BI tool.

This is additive: it extends the existing `analytics` edge function (already
queries both `orders` and `customers` for a restaurant —
`aiorders-api/supabase/functions/analytics/database.ts`) and the existing
Dashboard/Reports surfaces, rather than introducing a new subsystem.

## Acceptance criteria

1. `[stated]` Given a restaurant owner on the brand portal, when they view
   their traffic/revenue report, then they see their own customers, orders,
   and revenue broken down by acquisition channel, scoped strictly to their
   own restaurant.
2. `[inferred]` Given the breakdown, when the owner changes the time range,
   then the figures update to match, so a trend is visible rather than a
   single all-time snapshot.
3. `[inferred]` Given a customer record with no attribution data captured (a
   real, current possibility — see Risks), when it's included in the
   breakdown, then it's shown as an explicit "unknown/direct" bucket rather
   than silently dropped or miscounted into another channel.
4. `[proposed]` Given the channel breakdown, when organic-search/direct
   traffic is shown, then the report's framing makes clear this reflects the
   restaurant's overall web presence (including AI-generated SEO among other
   factors), not a number claiming to isolate AI SEO's effect alone — see
   Risks, attribution honesty.
5. `[inferred]` Given a request to read this data for a restaurant a caller
   doesn't belong to, then it's rejected server-side, not just hidden in the
   UI — same precedent `ENG-015`/`ENG-019` criterion 7 already established on
   this board.

## Non-goals

- **Microsoft Clarity integration.** Clarity is a session-recording/heatmap
  tool, not an attribution or revenue tool — pulling its data into AIOrders
  would not answer the "is this making money" question this ticket exists to
  answer, and nothing in this codebase talks to it today. If what's actually
  wanted is Clarity's own behavioural data (rage-clicks, scroll depth)
  surfaced inside AIOrders, that's a separate, real integration — worth asking
  for explicitly rather than assumed into this ticket.
- **A true ROI ratio (return over cost).** This ships revenue-by-channel;
  weighing it against each restaurant's AIOrders subscription cost is a
  separate calculation with a data source (billing) this analytics surface
  doesn't have.
- **Isolating "AI-generated SEO" specifically from organic traffic
  generally.** The platform has no record today of which restaurants have
  AI-generated vs. manually-written SEO applied, and even with one, months of
  pre/post data would be needed before a causal claim is honest.
  Organic-channel revenue is a reasonable proxy and is what ships; a dedicated
  AI-SEO-attribution metric is real, later work if the approver wants to
  invest in tracking that split going forward.
- **A staff-facing, all-restaurants rollup on the admin hub.** Real and
  useful for account management/sales — proposed as a follow-on ticket once
  the per-restaurant version is live and proven, same sequencing this board
  already used for `ENG-014`'s two-item split and `ENG-016`'s deferred
  deeper-autopilot item.
- **Any change to the existing `Analytics` (influencer-campaign) or
  `Reports` (staff-curated external links) pages** — this is additive, and
  the influencer-analytics naming collision is worth naming explicitly
  (avoid it in whatever this ships as) rather than silently reused.

## Risks and unknowns

- **Attribution honesty, named by both readings independently.** A
  last-click/last-touch number will overstate what SEO specifically did.
  Acceptance criterion 4 exists because of this, not generic caution — the
  report must be able to show SEO isn't working, or it isn't honest.
- **Cross-domain attribution may be incomplete.** The existing
  `user-tracking.js` script shares cookies across subdomains of one domain,
  but its own `README.md` documents the online-ordering-side wiring as
  something each deployment still has to add, not something guaranteed live
  everywhere already — the architect should confirm actual coverage per
  restaurant before this report's numbers are presented as complete.
  Acceptance criterion 3's "unknown/direct" bucket exists partly to absorb
  this honestly rather than hide it.
- **Privacy/legal exposure**, raised by the blind architect reading and not
  previously flagged on this board: session-recording tools like Clarity, and
  even first-party UTM/referrer capture, touch PIPEDA and (for Quebec
  restaurants) Law 25. Worth a real check on consent and data-controller
  responsibilities between AIOrders and each restaurant — especially since
  Clarity's own installation, already underway outside this ticket, may not
  have had one.
- **No historical baseline for existing customers.** `first_touch_source` is
  only populated going forward from when each capture path started writing
  it; a restaurant onboarded earlier has incomplete history, which the
  "unknown/direct" bucket (criterion 3) makes honest rather than hidden.
- **Small-restaurant noise.** A single-location restaurant's weekly channel
  mix will swing on small numbers; the UI should avoid implying false
  precision — same instinct `ENG-019`'s Risks applied to campaign ROI.
- **Tenant isolation.** This codebase has a confirmed, real history of
  exactly this bug class (`ENG-015`) — acceptance criterion 5 exists because
  of that precedent, not generic caution.
- Sizing assumes the underlying attribution columns are reliable and complete
  enough to report on as-is (extending the existing `analytics` edge
  function, which already queries both `orders` and `customers` for a
  restaurant). If the architect finds the existing data materially sparse or
  inconsistent across the five repos' capture paths, this ticket's cost grows.

## Cost

- Build: `M` — no new data model (the attribution columns already exist and
  are already being written by multiple live paths), no new vendor. Extends
  an already-wired edge function plus a new report view on an existing page.
  Rough band: a day and a half to two days.
- Run: `$0/month` expected — no new vendor, reuses existing Supabase compute;
  flag to devops/CFO only if the architect's query design surfaces a real new
  cost.

## Decision

- **The approver's answer:** approved
- **Date:** 2026-09-03T15:53:14.495206+00:00
- **Notes:** Bare approval, no additional comment — read as accepting the
  recommendation exactly as scoped (per-restaurant traffic-source/revenue
  breakdown reusing already-captured attribution data; Clarity integration, a
  true ROI ratio, isolating AI-SEO specifically from organic traffic, and a
  staff-facing all-restaurants rollup all deferred as later, separate work),
  and every item in the readback's "Assumed, correctable here" list as
  proposed, same convention this journal already applies to an
  unremarked-on assumption (`ENG-019`'s row, `ENG-026`'s requirement 6,
  `ENG-016`'s unremarked riders). The Risks this PRD flagged — attribution
  honesty, cross-domain attribution completeness, PIPEDA/Law 25 exposure, no
  historical baseline, small-restaurant noise, and tenant isolation — are not
  resolved by this approval and stay open, inherited by the architect at
  `designed`.
