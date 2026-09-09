---
ticket: ENG-018
project: aiorders-admin-hub
status: awaiting-scope
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

## Approver's `changed` response (2026-09-09T02:03:59Z) — fast-simulated timeline, one session-scoped run

**The answer** (`decision: changed`): *"It has to be fast simulated like
show the autopilot 90 day process in 15 minutes. And 1 complete experience
per session."*

Two clauses. The first redirects the demo's core mechanic away from this
PRD's original "believable, not transactional" static seed (Assumed,
above) and toward a scripted, time-compressed playback: what a
restaurant's real customer-lifecycle automation does over roughly 90 real
days, compressed into about a 15-minute session. The second scopes how
that plays out when more than one person is looking at the demo at once:
each session gets its own single, complete, start-to-finish run — not a
shared clock every rep and prospect watches the same slice of.

**Checked against live code before rescoping, not assumed.**
`restaurant-portal`'s `Autopilot` section (`src/pages/autopilot/
Automations.tsx`, `src/pages/autopilot/Broadcasts.tsx`) is real, live, and
backed by `aiorders-api`'s `autopilot` function — this is the actual thing
AIOrders sells restaurants: automated customer-lifecycle messaging. Its
`TriggerType` enum (`supabase/functions/autopilot/utils/triggers.ts`) is
ten hardcoded events — `new_customer_welcome`, `first_order`,
`welcome_offer`, `every_order`, `order_completed`, `abandoned_cart`,
`order_feedback`, `feedback_received`, `birthday`, `new_catering_lead` —
each with its own `email_delay_minutes`/`sms_delay_minutes` on the
template row. There is no single documented "90-day sequence" anywhere in
the code; "90 day" is read as the approver's own approximate framing of
what a realistic run through this trigger set looks like across a new
customer's first few months (welcome, first order, repeat/abandoned-cart
nudges, eventually a birthday or win-back message) — not a literal spec to
reproduce move-for-move. Named as interpretation, correctable here, same
convention this department already applies to a supplied mechanism that
isn't literally in the code (`ENG-027`'s "autocompleted after x hours").

**Mechanism proposed, and the one explicitly rejected.** There are two
ways to make ~90 real days visible in ~15 real minutes: (a) give the live
`autopilot` function a virtual clock it reads instead of `now()`, so the
real trigger/delay pipeline actually fires early on the demo restaurant;
or (b) a demo-only scripted timeline — a fixed, ordered set of pre-written
rows (communications "sent," orders placed, loyalty points earned, a
catering enquiry) tagged to the demo restaurant with backdated timestamps
spanning ~90 days, revealed to the viewer on a compressed schedule during
the session.

**(b) is proposed.** It's cheaper, and (a) is the one mechanism this PRD's
own isolation criteria (3, 4, both already in the original acceptance
criteria) exist to rule out — the real trigger/delay pipeline is the thing
real restaurants' real customers receive real messages from. Isolation was
already this PRD's load-bearing requirement, not a detail; this rescope
makes the same call again rather than loosening it for the
more-impressive-looking option.

**"One complete experience per session," read together with the above:**
the compressed playback is a single guided run — one demo restaurant
identity (still shared, still neutrally branded, per the original Assumed
section), but the *playback state* is scoped to the session watching it,
not a global clock the whole account shares. Two reps demoing at the same
time, or one rep restarting mid-pitch, never see or affect each other's
progress. This resolves, in a specific direction, the open question the
original PRD's Risks section left open ("whether 'one flagged restaurant'
is enough isolation") — the answer is yes for the restaurant *identity*, no
for the *playback state*, which needs its own session-scoped mechanism.
Read literally alongside the first clause, not as two unrelated
instructions: "1 complete experience" is the same single scripted run
"fast simulated... in 15 minutes" describes, seen from the concurrency side
rather than the content side.

**Sizing verdict: stays `L`.** What would have pushed this to `XL` —
virtualizing time inside the real send/trigger engine (mechanism (a)) — is
exactly what's rejected. What's added instead is a bounded, demo-only
asset: a scripted set of backdated seed rows plus a playback/reveal UI,
still inside the four repos already named, still no new vendor, still
$0/month. Flagged as a risk below: if the architect finds session-scoped
playback state needs a real cross-repo session-identity mechanism (not
just a client-side timer over static seed data), that is a bigger,
structural decision and may earn its own G2 — same fork this PRD already
named once for isolation generally.

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

## Proposed change (rescoped)

After this ships:
- A seeded, realistic demo restaurant exists (unchanged from the original
  scope) with a populated menu, order history, an active loyalty
  configuration (per `ENG-007`'s per-restaurant loyalty setup), and, once
  `ENG-016`'s catering pipeline is available, a catering pipeline — all
  backdated to support one full scripted run.
- Starting a demo session plays a single, complete, guided run of the demo
  restaurant's Autopilot customer-lifecycle sequence — welcome, first
  order, a repeat/abandoned-cart nudge, eventually a birthday or win-back
  message — on a compressed timeline that reads as roughly 90 days of real
  activity, completing in around 15 minutes. This is a demo-only scripted
  reveal of pre-seeded, backdated activity; it never invokes the real
  `autopilot` trigger/delay pipeline (see Non-goals).
- Sales staff and resellers can reach this demo restaurant's owner-facing
  portal (`restaurant-portal`) and its public site
  (`config-site-builder`) from a single, obvious entry point in the admin
  panel, without needing separate remembered credentials.
- Each session's playback is its own: starting a new session (or
  restarting mid-pitch) always begins one fresh, complete run, and two
  sessions running at the same time never see or affect each other's
  progress.
- Nothing in the playback sends a real email/SMS to a real inbox/phone,
  and none of it affects platform-wide analytics or revenue reporting
  (unchanged from the original scope, now explicitly covering the
  playback mechanism too — see Acceptance criteria 3, 4).

This ticket still does not build reseller-branded demo clones or a
prospect-facing shareable demo link — see Non-goals.

## Acceptance criteria (rescoped)

1. `[stated]` Unchanged. Given a sales staff member or reseller in the
   admin panel, when they look for a way to demonstrate the platform,
   then they can reach a working demo restaurant's portal and public
   ordering site from one clear entry point.
2. `[stated]` Rewritten — was `[inferred]`, now the approver's own explicit
   instruction. Given a rep starts a demo session, then it plays one
   complete, scripted run of the demo restaurant's Autopilot
   customer-lifecycle sequence (drawn from the live `TriggerType` set:
   welcome, first order, a repeat or abandoned-cart nudge, a birthday/
   win-back message) on a compressed timeline reading as roughly 90 days
   of activity, finishing in roughly 15 minutes — backed by seeded menu,
   order, loyalty and (once `ENG-016` ships) catering data, not an empty
   shell.
3. `[proposed]` Unchanged, now explicitly covering the new mechanism too.
   Given activity shown inside the demo (placing an order, an Autopilot
   message in the playback, a loyalty event, a catering enquiry), then no
   real email or SMS is ever sent to a real recipient, at any point,
   including during the compressed playback.
4. `[proposed]` Unchanged. Given the demo restaurant's order/revenue
   activity (seeded or played back), then it is excluded from
   platform-wide analytics and revenue aggregation (the existing
   `platform_analytics_cron` pipeline), so it never inflates real
   reporting.
5. `[proposed]` Rewritten. Given a rep opens the demo, then a fresh,
   complete run starts on its own — no separate manual "reset" step is
   needed between pitches — and given two sessions open at the same time
   (two reps, or one rep restarting), then neither sees or affects the
   other's progress.
6. `[inferred]` Unchanged. Given a caller who isn't `admin`/`sub-admin`/
   `partner-admin`/`partner-user`, then they cannot reach the demo's
   session/management controls (viewing the public site itself stays
   open, same as any real restaurant's site today).

**The one most worth correcting if wrong:** criterion 5 now treats "start
a new session" as replacing the original manual reset action entirely,
rather than sitting alongside it. If staff still want a manual
"reset everything" control independent of starting a new session (e.g. to
clear a botched multi-rep state), say so — it's a small addition, not a
rescope.

## Non-goals (rescoped)

- **Superseded by this answer:** "automatically keeping the demo's order
  history current or trending... a live-simulated demo that generates
  fresh fake activity on its own" is no longer entirely out of scope — the
  compressed playback *is* a form of that, scoped to an active session
  (the original wording read too broadly against this instruction). What's
  still out: a live, ever-running simulation with no session behind it —
  there is no 24/7 background clock advancing a shared demo state between
  pitches; the playback exists only while a session is open.
- **New, naming the rejected mechanism plainly:** virtualizing time inside
  the real `autopilot` function so its actual trigger/delay pipeline fires
  early. The playback is a demo-only scripted reveal of pre-seeded,
  backdated rows; it does not touch the real send pipeline real
  restaurants depend on.
- **Reseller-branded demo clones** — unchanged. Showing the demo under a
  specific reseller's own brand rather than AIOrders' neutral one. Real,
  named in the raw text, and proposed as later work once the single
  shared demo above is real. See Assumed.
- **A prospect-facing shareable link** — unchanged. Usable without staff
  present (e.g. a self-serve demo a prospect clicks through alone) — not
  asked for in the raw text; this ticket's demo is something staff drive
  during a pitch, not a marketing asset distributed unsupervised.
- **A second, fully isolated database/environment** — unchanged, and
  reinforced rather than reopened by the mechanism chosen above: one
  flagged demo restaurant inside the existing platform, no new deploy
  target needed.

## Risks and unknowns (rescoped)

- **Isolation is still the load-bearing requirement, not a detail.**
  Unchanged from the original PRD, now re-affirmed against a more
  tempting alternative: mechanism (a), a virtual clock inside the real
  automation, was available and is explicitly rejected in favour of (b),
  a scripted, pre-seeded reveal, for exactly this reason.
- **Resolved by this answer:** whether "one flagged restaurant" is enough
  isolation. Yes for the restaurant's identity/seed data; the *playback
  state* additionally needs to be session-scoped, which is new, specific
  scope this rescope adds (see Cost).
- **Open for the architect, possibly its own G2:** how cheaply
  "session-scoped" can be built. If a client-side timer replaying static,
  pre-ordered seed data is enough, this stays a UI-layer addition. If it
  needs a real session-identity mechanism threaded through the admin
  panel, portal, and public site (e.g. so a reset/restart on one screen
  doesn't leave another screen mid-playback), that's a bigger, structural
  call and may need its own gate before building.
- **"90 day" and the specific trigger sequence shown are the approver's
  approximate framing, not a literal spec** (see the rescope section
  above) — the exact events, order, and apparent day-spacing in the
  playback are a content/scripting decision for design or a follow-up
  pass, not fixed by this PRD.
- Carried forward, unchanged: reseller-branded demo scope (Non-goals) may
  turn out to matter more than assumed if resellers are a primary sales
  channel rather than a secondary one. No specific lost deal named as
  evidence; the gap is structural.

## Cost (rescoped)

- Build: still `L` — several days to a week. On top of the original scope
  (seed data across menu/orders/loyalty/catering, the send/analytics
  exclusion flag (`aiorders-api`), the admin-hub entry point
  (`aiorders-admin-hub`), and portal/public-site rendering
  (`restaurant-portal`, `config-site-builder`)), this rescope adds a
  backdated, ordered set of scripted "communication sent" rows spanning
  the demo's ~90-day narrative, and a compressed playback/reveal UI
  scoped to one session at a time. Still four repos, no new vendor, no
  new deploy target. **Fork named explicitly, not absorbed silently:** if
  the architect finds a client-side/static-seed approach to
  session-scoping insufficient and a real cross-repo session mechanism is
  needed, this ticket's size and shape both change — flagged above as a
  possible G2, same as the original PRD's own isolation question was
  flagged.
- Run: `$0/month` expected, unchanged — reuses existing infrastructure;
  flag to devops/CFO only if a genuinely separate environment turns out to
  be needed.

## Decision

Filled in by the approver.
