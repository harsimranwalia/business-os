---
ticket: ENG-018
project: aiorders-admin-hub
status: draft
size: L
author: product-manager
created: 2026-08-29
decided:
---

# Sales demonstration account — a fully seeded AIOrders environment to show prospects

## Readback

**You said:** "no autopilot on admin panel for our sales staff/ resellers to
use . how can we demonstrate to a client what we sell if we dont have it
for us. have a proper fully demonstration account on how all aiorders work.
also autopilot nurturing for resellers/sales/admin staff on admin panel
which works based on stages update/ auto nurturing ."

**Understood as:** This one raw request bundles two separable asks (see
Second reading below) — this PRD covers only the "demonstration account"
half; the autopilot-nurture half is `ENG-017`. Today, when a sales rep or
reseller pitches a prospective restaurant owner, there is nothing to
actually show them — no seeded, working example of a restaurant's ordering
website, portal, loyalty, and marketing running end to end. "We don't have
it for us" reads as: AIOrders sells restaurants a working platform but has
no instance of its own product it can point to live. You want one
demonstration setup — a fake but fully-populated restaurant — that any
sales rep or reseller can pull up mid-pitch and click through as if it
were real.

**Assumed, and worth correcting if wrong:**
- **"What we sell" is the restaurant-facing product** — the branded
  ordering website (`config-site-builder`) and the owner's operating
  portal (`restaurant-portal`: orders, menu, loyalty, catering pipeline,
  marketing) — not the internal `aiorders-admin-hub`, which restaurants
  never see. The demo's job is to show a prospect what *their* restaurant
  would look and feel like on AIOrders, not to show them AIOrders' own
  back office.
- **One shared demonstration tenant, not a per-rep or per-reseller clone.**
  The raw text says "a proper fully demonstration account" (singular).
  Proposed default: one seeded demo restaurant, neutrally branded, usable
  by internal sales staff and resellers alike. A reseller-branded copy of
  the demo (so a reseller can show it under their own brand rather than
  AIOrders') is real and named in the raw text's "resellers... to use,"
  but is proposed as later work — see Non-goals — since it multiplies this
  ticket's scope (a brandable, cloneable demo rather than one fixed
  instance) without changing what a first prospect actually sees.
- **Read-only-feeling, not truly transactional.** A prospect should be able
  to see orders, a menu, loyalty activity, and the catering pipeline
  behaving as if real, without a real payment, a real SMS/email hitting
  someone's actual phone, or the demo's fake activity leaking into
  platform-wide analytics or revenue reporting. See Risks — this is a real
  constraint, not a nice-to-have, given a live internal analytics
  pipeline already aggregates `orders`/`total_amount` per restaurant
  platform-wide (`ENG-011`'s own evidence, `platform_analytics_cron`).
- **Resettable.** A demo gets clicked around and broken during a pitch;
  the proposed default is a way to reset it to a known-good state on
  demand rather than assuming it stays pristine.
- **Access is from the admin panel** — the raw request frames this under
  "admin panel," so the proposed entry point is a control inside
  `aiorders-admin-hub` that any `admin`/`sub-admin`/`partner-admin`/
  `partner-user` can use to reach or reset the demo, rather than handing
  out a separate set of raw credentials to remember.

**Second reading agreed / diverged on:** This PM's reading, grounded in the
live code cited throughout, plus a blind architect reading (subagent,
`opus`, raw request + `knowledge/business-profile.md` only — no repo
access, no exposure to this PM's own reading). **No material divergence**
— both independently split the raw request into the same two pieces, and
both independently arrived at "a seeded, fully working fake restaurant" as
the shape of the fix. The architect's reading additionally, and
unprompted, flagged that demo data must be isolated from real sends,
payments, and reporting rollups, and that a reseller's demo should show
their own brand rather than AIOrders' — both folded into Assumed/Non-goals
above rather than treated as new divergences requiring a question. The
autopilot-nurture half of the architect's reading is carried into
`ENG-017`.

**Evidence checked, not assumed.** Searched all five repos for any
existing "demo" concept before proposing a net-new one: the only hit
resembling a demo account is `config-site-builder/public/config/
demo-restaurant.json` — a static, placeholder SEO/config fixture used as a
template example for the site-generation pipeline, not a live, loggable-into
account with real portal/order/loyalty behavior. No `is_demo` flag, no demo
role, no seed script, and no sandboxing of outbound sends or analytics
exists anywhere today. This is a genuine, confirmed-net-new gap.

## Problem

There is no working example of the AIOrders platform that a sales rep or
reseller can show a prospective restaurant owner — confirmed absent across
all five repos, not assumed. Every demonstration today would have to
either talk through the product with no live artifact, or show a real
paying customer's actual account, which is both an awkward pitch and a
real privacy exposure (showing one restaurant's live orders/customers to
a different, prospective one).

## Why now

Approver-initiated; no specific lost deal named, no stated deadline. The
underlying gap — nothing to demo with — is structural and confirmed by a
full search of the codebase, not anticipated.

## Users

Internal sales/admin staff and resellers (`partner-admin`/`partner-user`)
who pitch prospective restaurant owners. The prospect themselves is a
secondary, indirect user — they see the demo's public ordering site during
the pitch but never log into anything.

## Proposed change

After this ships:
- A seeded, realistic demo restaurant exists with a populated menu, order
  history, an active loyalty configuration (per `ENG-007`'s per-restaurant
  loyalty setup), and a public ordering website
  (`config-site-builder`) that looks and functions like a real
  restaurant's.
- Sales staff and resellers can reach this demo restaurant's owner-facing
  portal (`restaurant-portal`) and its public site from a single, obvious
  entry point in the admin panel, without needing separate remembered
  credentials.
- Activity inside the demo (orders placed, loyalty points earned, catering
  requests submitted) behaves believably on-screen but never sends a real
  email/SMS to a real inbox/phone and never affects platform-wide
  analytics or revenue reporting.
- The demo can be reset to a known-good state on demand, so one rep's
  pitch doesn't leave it broken for the next.

This ticket does not build reseller-branded demo clones or a
prospect-facing shareable demo link — see Non-goals.

## Acceptance criteria

1. `[stated]` Given a sales staff member or reseller in the admin panel,
   when they look for a way to demonstrate the platform, then they can
   reach a working demo restaurant's portal and public ordering site from
   one clear entry point.
2. `[inferred]` Given the demo restaurant, then it has a populated menu,
   order history, an active loyalty configuration, and (once `ENG-016`
   ships) a catering pipeline with example entries — enough to show "how
   all aiorders work" rather than an empty shell.
3. `[proposed]` Given activity performed inside the demo (placing an
   order, triggering a loyalty event, submitting a catering enquiry),
   then no real email or SMS is sent to any real recipient.
4. `[proposed]` Given the demo restaurant's order/revenue activity, then
   it is excluded from platform-wide analytics and revenue aggregation
   (the existing `platform_analytics_cron` pipeline), so it never inflates
   real reporting.
5. `[proposed]` Given a demo that's been clicked through and left in a
   messy state, when staff want to reset it, then a reset path returns it
   to a known-good seeded state without a manual data cleanup.
6. `[inferred]` Given a caller who isn't `admin`/`sub-admin`/`partner-admin`
   /`partner-user`, then they cannot reach the demo's reset/management
   controls (viewing the public site itself stays open, same as any real
   restaurant's site today).

## Non-goals

- **Reseller-branded demo clones** — showing the demo under a specific
  reseller's own brand rather than AIOrders' neutral one. Real, named in
  the raw text, and proposed as later work once the single shared demo
  above is real. See Assumed.
- **A prospect-facing shareable link** usable without staff present (e.g.
  a self-serve demo a prospect clicks through alone) — not asked for in
  the raw text; this ticket's demo is something staff drive during a
  pitch, not a marketing asset distributed unsupervised.
- **A second, fully isolated database/environment.** Proposed as one
  flagged demo restaurant inside the existing platform (cheaper, matches
  every other restaurant's real code paths exactly) rather than a
  parallel deployment — the architect may revisit this if isolating sends
  and analytics turns out to need more separation than a flag allows.
- **Automatically keeping the demo's "order history" current or trending**
  — a static, periodically-reset seed is proposed; a live-simulated demo
  that generates fresh fake activity on its own is out of scope.

## Risks and unknowns

- **Isolation is the load-bearing requirement, not a detail.** A demo
  restaurant that accidentally sends a real SMS, or whose fake orders
  land in real revenue analytics, is worse than no demo at all. This PRD
  treats isolation as acceptance criteria (3, 4) rather than an
  implementation nicety so it can't be quietly dropped at build time.
- **Whether "one flagged restaurant" is enough isolation or whether the
  send/analytics pipelines need a structural change to safely exclude
  it** is a real open design question — flagged for the architect,
  possibly its own G2 if excluding demo activity turns out to require
  touching shared aggregation logic non-trivially.
- **Reseller-branded demo scope (Non-goals) may turn out to matter more
  than assumed** if resellers are a primary sales channel rather than a
  secondary one — worth the approver confirming the phased approach
  rather than this PRD asserting it's fine.
- No specific lost deal named as evidence; the gap is structural.

## Cost

- Build: `L` — seed data across multiple tables/repos (menu, orders,
  loyalty, catering) and a flag/mechanism to exclude that data from real
  sends and analytics (`aiorders-api`), an access/reset entry point
  (`aiorders-admin-hub`), and confirming the public site
  (`config-site-builder`) and portal (`restaurant-portal`) render
  correctly for a flagged demo restaurant. Four repos touched, no new
  data model beyond a demo flag and a reset mechanism. Rough band: several
  days to a week.
- Run: `$0/month` expected — reuses existing infrastructure; flag to
  devops/CFO only if a genuinely separate environment turns out to be
  needed.

## Decision

Not yet raised. **Held at `shaped`, not advanced to `awaiting-scope` this
pass** — the approver-facing WIP cap (2) is currently full (`ENG-014`,
`ENG-015`, both still open) per `eng_build_loop.md`'s Guards. Will raise G1
once a slot frees; see the ticket's own log for the fresh cap check made
before this decision. Filed alongside `ENG-017` (the autopilot-nurture half
of the same raw request) — see that PRD for the sibling scope.

- **The approver's answer:** —
- **Date:** —
- **Notes:** —
