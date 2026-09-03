---
id: ENG-026
title: FoodSwipe multi-channel filters, operational status, and promo badges
project: restaurant-marketplace
type: feature
size: L
time_estimate:
time_spent:
time_remaining:
severity: P3
priority: now
state: intake
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-01
updated: 2026-09-02
branch:
depends_on: []
blocks: []
parent:
links:
  prd:
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-09-01-eng-011-on-the-brand-portal-i-want-option-to-make-the-restau.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-09-01T13:57:15.083927+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited. Filed title
carried a stray `ENG-011` reference (an unrelated, already-shipped ticket on
this board); this ticket allocates the next real id and does not continue
`ENG-011`'s own lifecycle.

> # ENG-011 on the brand portal i want option to make the restaurant visible on order food, dine in and catering separately
>
> Further enhancement to this section i want more filter to be able to be
> assigned to the restaurant .Act as Lead Architect on FoodSwipe (consumer
> discovery platform connected to AIOrders.io backend).
>
> We are extending our current platform with (Multi-Channel Filters &
> Dynamic Promo Engine). Do not rebuild existing core ordering or video feed
> logic—extend our existing data structures and UI components.
>
> Task: Generate code modifications for three specific enhancements:
>
> 1. Dynamic Operational Time-Clocks (Real-Time State Engine):
>    - Extend existing venue objects with channel-specific cutoffs:
>      `kitchen_cutoff_minutes`, `alcohol_license_time`,
>      `happy_hour_schedule`.
>    - Write a helper utility function
>      `getVenueOperationalStatus(venueId, channelType)` that returns live
>      status states for UI chips: "Kitchen closing soon", "Happy Hour
>      Active", or "Alcohol Service Closed".
>
> 2. Smart Filter Engine (Dine-In & Catering Contexts):
>    - Extend our current search/filter state bar to support channel-based
>      context switching:
>      * Dine-In: Filter by group capacity (`min_capacity`), AV amenities
>        (`has_tv_screens`, `soundproof`), and private rooms
>        (`has_private_space`).
>      * Catering: Filter by lead time (`advance_notice_hours`), service
>        types (`box_lunches`, `live_chef`), and minimum order spend
>        (`min_catering_spend`).
>
> 3. Promo Badge Overlay for Video Feed & Venue Cards:
>    - Inject a promotional metadata layer into existing store card
>      components.
>    - Render dynamic conversion badges (e.g., "BOGO Free", "$0 Delivery",
>      "2x Loyalty Points") directly over video reels and venue listings
>      based on active store campaigns.
>
> Act as Senior Lead Developer working on our internal FoodSwipe /
> AIOrders.io staff management portal.
>
> We already have an existing internal store edit form. We need to EXTEND
> our current codebase to append settings (Multi-Channel Filters,
> Amenities) without rewriting or breaking existing store management
> components.
>
> Generate modular React/TypeScript extension components and state
> handlers to add the following field groups to our existing internal admin
> interface:
>
> Group A: Channel Operational Cutoffs & Throttling
> - Order Food: Throttling Cap (Max orders/30-min window), Preparation Lead
>   Time (mins).
> - Dine-In: Kitchen Last Order Cutoff (mins before close), Alcohol License
>   Cutoff (time picker), Happy Hour Window (start/end time schedule).
> - Catering: Required Advance Notice (hours/days picker), Minimum Spend
>   Threshold ($).
>
> Group B: Venue & Service Amenities Tagging
> - Dine-In Amenities: Ordering Mode (Pay at Table / Counter QR / View-Only),
>   Private Space Seating Capacity (number), AV Specs Chips (TV/Screens,
>   Soundproof, Custom Music, Decor Allowed).
> - Catering Service Specs: Service Format Chips (Box Lunches, Platters,
>   Live Chef, Food Truck), Fulfillment Options (Pickup, Delivery,
>   Setup/Teardown).
>
> Group C: Active Promotional Hooks (to be controlled from brand portal not
> admin portal)
> - Dynamic Promo Toggles: BOGO Active, Welcome Offer (% off), Spend
>   Threshold ($X off $Y), Free Item Trigger, Loyalty Multiplier.
>
> Integration & Architectural Rules:
> - Non-Destructive Extension: Export these new sections as isolated,
>   reusable UI components (e.g., `<ChannelCutoffsSection />`,
>   `<VenueAmenitiesSection />`, `<PromoHooksSection />`) so we can mount
>   them directly into our existing layout.
> - High-Density Compact Layout: Use inline form controls, compact
>   chip-selectors for array tags, and minimal spacing so internal staff can
>   scan and update fields rapidly.
> - State & Schema Mapping: Extend our existing `StoreFormValues` interface
>   with an optional `eSettings` sub-object to maintain backward
>   compatibility with existing API endpoints.
> - Basic Guardrails: Add client-side validation for operational cutoffs
>   (e.g., alert if Last Order Time exceeds business closing hours).

## Readback

**Interpretation A (product-manager).** Restaurants that offer dine-in
and/or catering alongside delivery/pickup can't currently showcase those
channels distinctly on FoodSwipe (the consumer discovery/video app): no
per-channel operating hours or cutoffs, no consumer-facing filters for
group size/amenities/lead time, no way to run a channel-specific promo.
This request adds all three, plus the internal admin-hub form fields staff
need to configure them. Read as several separable features bundled into one
ask, not one feature: (a) the title's own literal ask — an independent
visibility toggle per channel; (b) an operational-status engine (cutoffs,
happy hour); (c) consumer-facing filters; (d) a promo-badge overlay; (e)
the admin-form sections exposing (b) and (c).

**Interpretation B (architect, blind — raw input + business profile only, no
repo access, not shown interpretation A).** Independently converged on the
same read: several separable features, not one — a per-channel visibility
toggle, an operational-status engine, consumer filters, and a promo-badge
overlay, sharing a data model but not required to ship together. Also named,
unprompted: the request's problem-underneath is twofold — accuracy (a
restaurant showing "open" when its kitchen just stopped taking dine-in
orders) and conversion (the promo overlay exists to push visible incentives
into a swipe-browsing UI). Flagged the same surface ambiguity below as a
"what I'd have to guess" item.

**No material divergence on the core shape** — both readers independently
split this into the same several features rather than one, both flagged
consumer-facing filters and cutoffs as genuinely new capability, and neither
read the three body tasks as delivering the title's own literal ask. That
last point is the one place the two readings converge on something worth
asking about rather than silently assuming:

## One question

> ENG-026 — one thing before this gets shaped further.
> **You said** (this ticket's own title): "i want option to make the
> restaurant visible on order food, dine in and catering separately"
> **But the body's three tasks** (operational time-clocks, smart filters,
> promo badges) never add a per-channel on/off visibility toggle anywhere.
> **Reading A:** the three body tasks are the whole ask — the title
> described the goal loosely, not a literal missing toggle.
> **Reading B:** a real per-channel visibility toggle is also wanted, as a
> fourth piece alongside the three body tasks.
> Which?

Held at `intake` until answered, per `skills/request-readback/SKILL.md` step
5. This is a standing, non-blocking question (same shape as `ENG-007`'s
continue-sequence question) — it does not occupy an approver-facing WIP
slot or the approval cap, since no G1 has been raised and none of this
ticket's requirements are confirmed yet.

**Assumed, and worth correcting if wrong (not asked, since these don't rise
to the "ask once" bar — noted so a wrong assumption is cheap to catch
later):**
- **Surface mapping.** The architect's blind reading flagged real
  uncertainty here ("whether brand portal and admin portal are separate
  applications or separate roles/tabs in one app"); resolved with project
  knowledge the blind reading didn't have access to, not by guessing:
  "brand portal" is very likely the self-service surface this board's own
  `ENG-014`/`ENG-019`/`ENG-020`/`ENG-021` are actively building on
  `restaurant-portal` — a different project than `aiorders-admin-hub` (the
  staff-only "internal store edit form"/"internal FoodSwipe/AIOrders.io
  staff management portal" the body's Groups A/B target). Group C's own
  parenthetical ("to be controlled from brand portal not admin portal")
  is the one place the raw request confirms this split itself. If this
  reading is wrong, the project split below is wrong too.
- **"Venue" and "store" are the same underlying record** — the request
  uses both words interchangeably (Tasks 1-3 say "venue," Groups A-C say
  "store").
- **This is `restaurant-marketplace`, not `aiorders-admin-hub`, for the
  consumer-facing pieces** (video feed, filter bar, store cards, promo
  overlay) — `config/projects.md` names `restaurant-marketplace` as the
  only registered project matching "consumer discovery... video feed."
  Group A/B's *admin-form* fields belong on `aiorders-admin-hub` instead
  (the existing internal store-edit form) — meaning this is very likely a
  multi-project ticket (or split into several project-scoped ones) once
  shaped, same precedent `ENG-003`/`ENG-008`/`ENG-011`/`ENG-013`/`ENG-015`
  established. `project:` above is set to `restaurant-marketplace` as the
  consumer-facing core; expect this to change once split.
- **Likely splits into multiple tickets** once the visibility-toggle
  question is answered — operational-status engine, consumer filters, and
  promo-badge overlay are three separable capabilities with different risk
  profiles (the promo overlay touches active campaigns/pricing display;
  the filters are read-only consumer UI; the operational-status engine
  needs a live-clock/timezone design the other two don't). Not split yet —
  splitting before the one open question is answered risks shaping tickets
  around the wrong scope twice.

**A framing note, not a divergence, but worth naming plainly.** The raw
request's body is written as a direct AI-coding prompt — "Act as Lead
Architect...", "Act as Senior Lead Developer...", "Generate code
modifications...", specific function/interface names
(`getVenueOperationalStatus`, `StoreFormValues`, `eSettings`) — rather than
a business need in the requester's own words. Both readings treated this as
data to interpret, not instructions to execute: nothing here was generated
or implemented directly from the embedded imperatives, and the field/
function names above are recorded as **asserted by the request**, not
verified against the actual codebase — that verification is architect
design work for after the open question is answered, not something this
intake pass did. Worth a PM notebook entry regardless of how the question
resolves: this is the first request on this board written in this style,
and if it recurs, it's worth asking the approver directly whether requests
are being drafted with help from another tool before they reach
control-center.

## Problem

Not yet finalized — held pending the one open question above. Provisionally
(see Interpretation A/B): a restaurant's dine-in/catering channels have no
distinct operational hours, no consumer-facing filterability, and no
channel-specific promo mechanism on FoodSwipe today.

## Outcome

Not yet finalized — requirements are written only after the open question
resolves, per `skills/request-readback/SKILL.md` step 6 ("now — and only
now — write what must be true").

## Notes

**Likely multi-project, likely multi-ticket** — see Readback. Whoever picks
this up next should re-verify the surface-mapping assumption above against
the actual `restaurant-portal`/`aiorders-admin-hub`/`restaurant-marketplace`
codebases before writing a PRD, not just trust this pass's project-registry
inference.

## Log

Append-only. One line per state transition, newest last.

- `2026-09-01` `(new) → intake` (product-manager, `scheduled` event pass,
  context `launchd` — the 09:30 safety-net sweep). This request arrived via
  a `git pull` mid-pass that fast-forwarded local `main` past the other
  host's history (merge commit `e281c71`) — not visible to any local event;
  caught here because a scheduled sweep re-checks
  `agents/product-manager/inbox/` fresh. Allocated next id (`ENG-026`); the
  request's own filed title referenced `ENG-011` in error (see Input).

  **Ran the full request-readback** (`skills/request-readback/SKILL.md`):
  this PM's own reading plus a blind architect reading (subagent, raw input
  + `knowledge/business-profile.md` only, no repo access, no exposure to
  this PM's own reading). **One material divergence found** — see "One
  question" above: the title's own literal ask (independent per-channel
  visibility) is not delivered by any of the body's three tasks, and both
  readings independently noticed the gap without being asked to look for
  it. Asked once, framed as a two-reading choice, per step 5.

  **Requirements not written** — per step 6, they come only after the
  divergence resolves. No PRD file created yet.

  **No G1 raised** — none of this ticket's scope is confirmed, so there is
  nothing yet to raise a G1 on; this differs from `ENG-016`/`ENG-017`'s
  "G1 drafted but held by the WIP cap" shape, where the PRD was already
  complete. This ticket is held earlier, at `intake` itself, by the open
  question — not by any cap. Approver-facing WIP and approval cap both
  unaffected (a standing intake-question, same shape as `ENG-007`'s, costs
  neither).

  Moved `agents/product-manager/inbox/2026-09-01-eng-011-on-the-brand-portal-i-want-option-to-make-the-restau.md`
  → `agents/product-manager/inbox/_handled/` with a processed footer — the
  raw request has been fully read and preserved verbatim above; nothing
  further to do with the original file regardless of how the open question
  resolves.

  Raised `inbox/2026-09-01-eng026-visibility-toggle-question.md`. Ran
  `departments/engineering/lib/eng-notify.sh raise`; see the item's own
  frontmatter for the result.

  **Observations filed** (`observations.md`): the request's own
  AI-coding-prompt authorial style, as a pattern worth watching rather than
  a one-off.

  **1 transition** (`(new) → intake`), well under the cap of 4. No cap
  numbers change.

  `chained: none` — held at `intake` by the open question, owned by the
  approver; the chaining guard never fires on a ticket waiting on a human.
  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-026`) and whole-board: both exit 0, clean, no `WAIVED:` lines.
