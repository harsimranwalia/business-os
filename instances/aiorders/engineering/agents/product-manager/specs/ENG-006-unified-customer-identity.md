---
ticket: ENG-006
project: aiorders-api
status: designed
size: L
author: product-manager
created: 2026-08-27
decided: 2026-08-28T00:20:57.797718+00:00
---

# Unified cross-restaurant customer identity, phone/OTP auth, and legacy-customer mapping

## Readback

**You said:** "I want to be able to give the customers points for online
ordering and dine in they do at a restaurant and the points would be
restaurant specific only but all of them would have the same naming in the
frontend. For now we are just going to build the backend to support this. ...
We are also introducing the concept of a foodswipe customer who will be
identified by a unique phone number and they will be authenticated through an
sms otp and session would be maintained. Currently each restaurant has its own
customer even though its the same physical human being which will now be
identified in the system as a xxx customer (do no use the name xxx anywhere in
db and code thats more for branding). We can map the new foodswipe customer to
the legacy restaurant customer but for loyalty it will be one user but
collecting and redeeming points for multiple restaurants and see all of them
on one ui. and one qr code of the user would be scanned by all restaurants to
add and redeem points. Define the feature and we may have to split this into
multiple tickets... Also create this int a separate branch of loyalty-system
and backend and supabase migrations go in aiorders-api. Frontend stories/tasks
can be written but they will be done later on in a separate discussion." (full
text preserved verbatim in the ticket's `## Input`, from
`agents/product-manager/inbox/2026-08-27-i-want-to-be-able-to-give-the-customers-points-for-online-or.md`)

**Understood as:** A cross-restaurant loyalty program, backend only for now.
Today every restaurant has its own siloed customer record, so the same diner
is a stranger at each one and nothing earned anywhere carries anywhere else.
You want a single platform-level identity per human — phone number + SMS OTP
+ a maintained session — that maps onto the existing per-restaurant customer
records without replacing them, so a diner has one account and one QR code
across every AIOrders restaurant, while the points themselves stay
restaurant-specific (earned and spent only where they were earned) under one
shared display name. This is genuinely too large for one ticket, and you asked
for it to be split into a sequence — this PRD defines the whole shape and
scopes **this ticket to the identity/auth/mapping foundation only**; see
"Feature shape and sequencing" below for the rest.

**Requirements for this ticket** (identity, auth, session, legacy mapping —
not points, config, redemption, or QR):

1. `[stated]` A customer identifies themselves by phone number and
   authenticates via SMS OTP.
2. `[stated]` A session is maintained afterward — no repeat OTP on every
   visit.
3. `[stated]` One physical person is represented by one identity across every
   restaurant, replacing today's one-record-per-restaurant model for loyalty
   purposes.
4. `[stated]` The new identity maps to the existing legacy per-restaurant
   customer records rather than replacing them.
5. `[inferred]` The mapping is many-to-one: one unified identity can link to
   several legacy per-restaurant customer records, one per restaurant the
   person has ordered from before.
6. `[inferred]` Phone numbers are normalized to one canonical form before
   being used as the matching/uniqueness key — otherwise the same human
   re-entering their number slightly differently creates a second identity.
7. `[proposed]` OTP attempts are rate-limited and the code expires, so cost
   and abuse both stay bounded.
8. `[inferred]` The technical name for this identity avoids the branding word
   entirely, per your own instruction. This PRD refers to it as the
   **platform customer** — a neutral placeholder, not a naming decision. The
   architect picks the real schema-level name at design time; whatever it is,
   it must not be a brand word.
9. `[proposed]` Where a phone number matches legacy records at more than one
   restaurant, all of them link to the same identity automatically. Where a
   match looks ambiguous (e.g. conflicting name on the same phone, or a
   number shared by more than one legacy record at the same restaurant), the
   case is surfaced rather than guessed — this ticket does not silently
   resolve conflicts.

**Assumed, and worth correcting if wrong** (the ones that would change the
build, not just its details):

- **Dine-in spend has no existing record to hang points off.** AIOrders is an
  online-ordering platform; nothing here suggests a POS integration exists.
  Both independent readings of your request inferred the same thing: dine-in
  points come from an amount a restaurant staff member enters by hand at the
  point of the QR scan, not from an integrated bill. If a POS integration is
  actually expected, the ledger ticket downstream is considerably bigger than
  currently scoped.
- **Redemption needs its own configured value, not just an earn rate.** You
  specified how much to *give* (a percentage) but not what a point is *worth*
  when spent. The proposed fix is to make redemption value a second
  per-restaurant config field, symmetric with the earn-rate config — not a
  fixed platform-wide number — but that's a proposal, not something you
  stated.
- **Points never move between restaurants.** Earned at Restaurant A, spent
  only at Restaurant A. The "one UI" is a shared view over separate balances,
  never a shared balance or a transfer path.
- **Legacy customer records are kept, not merged or deleted.** This is
  additive only; every existing order flow keyed on the old per-restaurant
  customer keeps working untouched.
- **No points expiry in this phase.** Not mentioned either way, and worth
  saying out loud since it's a real liability lever, not just a detail.
- **"Restaurant" means one location, not a multi-location brand.** AIOrders'
  own positioning (independent restaurants, not chains) makes this the likely
  reading, but the architect should confirm it against the live schema rather
  than this PRD asserting it as fact.
- **Frontend is out of scope everywhere in this sequence, not just here.**
  restaurant-marketplace, restaurant-portal, and admin-hub all get their
  stories written later, in the separate discussion you named — none of the
  tickets in this sequence build UI.

**Second reading agreed / diverged on:** Two independent readings were run —
this PM's, and, blind to it, the architect's (an independent subagent given
only the raw request and the business profile, nothing else). They converged
on the core shape: platform-level phone identity, additive mapping to legacy
customers, restaurant-scoped balances under shared naming, manual dine-in
entry, restaurant-scoped QR authorization, and a near-identical proposed
ticket sequence. **No material divergence** — nothing where one reading
included scope the other didn't, or where they disagreed about what this is
for. The architect's reading added technical texture a PM lens wouldn't
surface on its own (ledger/balance duality and reconciliation, redemption
needing to be race-safe against concurrent scans, the percentage's base —
pre-tax vs. total — needing to be fixed and stored, RLS/tenant isolation with
exactly one necessary cross-restaurant read). This PM's reading surfaced
something the architect's lens didn't name as sharply: a single identity
shared across competing independent restaurants sits structurally closer to
what a marketplace owns than to the "you own your customer" pitch AIOrders
sells restaurants against UberEats/DoorDash. That's not a build question, so
it isn't a fork to ask about — it's a positioning fact worth having on the
record, and it's in Risks below rather than blocking this PRD.

## Feature shape and sequencing

You asked to "define the feature" and split it into tickets delivered one
after another. Here's the whole proposed shape — **only the first item is
this ticket; the rest are `[proposed]` sequencing, not yet filed, not yet
sized, and open to correction at this G1** before any of them exist:

1. **This ticket (ENG-006) — identity, OTP auth, session, legacy mapping.**
   Foundational; everything else keys off it.
2. **Per-restaurant loyalty configuration** — earn % (online, dine-in) and a
   redemption value, per restaurant, effective-dated so a later rate change
   doesn't rewrite the meaning of past ledger entries. No dependency on
   ENG-006; could build in parallel.
3. **Points ledger, balances, and earn API** — the points-per-customer-per-restaurant
   record, an earn/redeem transaction history, online-order-triggered
   accrual, and manually-entered dine-in spend and its accrual. Depends on
   ENG-006 (needs an identity to award to) and on (2) (needs a rate).
4. **Redemption API and QR issuance/scanning** — generates the customer's QR
   code, enforces that a scan only ever touches the scanning restaurant's own
   balance for that customer, and performs the redemption. Depends on
   ENG-006 and (3).
5. **Admin/support surfaces** — internal lookup, cross-restaurant view for
   support, and manual ledger adjustment/void. Depends on ENG-006 and (3).

Frontend (restaurant-marketplace, restaurant-portal, admin-hub) is
deliberately not sequenced here — you were explicit that it's a separate,
later discussion, and none of the above is customer- or staff-visible without
it.

**Recommendation: build ENG-006 now.** It's the one piece every later ticket
depends on, it's cleanly scoped on its own, and it's invisible to restaurants
and diners until later work lands on top of it — so shipping it first carries
no half-built user-facing risk. If the shape or order above is wrong, say so
in this G1 rather than after (2)–(5) start getting filed.

## Problem

Every restaurant on AIOrders has its own customer record for the same diner,
so the platform has no way to recognize one human across restaurants — and
therefore no way to run any reward program broader than a single restaurant,
and no visibility at all into dine-in spend, which today is entirely outside
the system. This also means AIOrders' core pitch to restaurants — "own your
customer relationship instead of renting it from a marketplace" — currently
has no identity layer behind it; it's an order record, not a relationship.

## Why now

No stated deadline and no committed launch restaurant named in the request.
This is foundational, approver-initiated work to start building the identity
layer the rest of the loyalty program depends on — said plainly since "no
particular reason beyond wanting to start" is a fair basis for building
something, not a gap to paper over.

## Users

Not directly user-facing yet. This ticket alone changes nothing any diner,
restaurant, or admin sees — it becomes visible only once the ledger, config,
redemption, and eventually frontend work land on top of it. The eventual
users are: diners (one identity and one QR instead of being re-created at
every restaurant), restaurant operators (a retention tool they configure and
fund themselves, with no visibility into a customer's activity at other
restaurants), and AIOrders' own support staff via admin-hub.

## Proposed change

After this ships, a diner who verifies a phone number once via SMS code is
recognized as the same person at every AIOrders restaurant, including ones
where they already have order history under the old per-restaurant model —
that history is linked, not lost or duplicated. Nothing about the ordering
experience changes yet; there is no points balance, no QR code, and no
redemption until the follow-on tickets above ship.

## Acceptance criteria

1. `[stated]` Given a phone number with no existing platform customer, when
   the person requests and correctly submits an SMS OTP, then a platform
   customer is created and a session is issued.
2. `[stated]` Given a phone number that already has a platform customer, when
   that person completes OTP verification again (a new device, a cleared
   session), then the existing platform customer is reused — no duplicate is
   created — and a new session is issued.
3. `[inferred]` Given a platform customer's verified phone number matches one
   or more existing legacy per-restaurant customer records, when the platform
   customer is created or first logs in, then those legacy records are
   linked to it without modifying or deleting the legacy records themselves.
4. `[inferred]` Given two legacy customer records at different restaurants
   share the same normalized phone number, when both are linked, then they
   resolve to the same single platform customer, and that platform customer
   can be read back together with the restaurants it's linked to.
5. `[inferred]` Given a valid session, when a subsequent API call is made,
   then the platform customer is identified from the session alone — no OTP
   is required again.
6. `[proposed]` Given a wrong or expired OTP code, when it's submitted, then
   the attempt is rejected, no customer record is created or linked, and
   repeated failures against the same phone number are rate-limited.
7. `[proposed]` Given a phone number that can't be normalized to a single
   canonical form, when OTP is requested, then the request is rejected with a
   clear reason rather than silently creating an inconsistent identity.

## Non-goals

- Points balances, the earn/redeem ledger, and redemption or spend history —
  ticket (3) above, not this one.
- Per-restaurant earn-rate or redemption-value configuration — ticket (2).
- QR code generation or scanning — ticket (4); this ticket has no QR surface
  at all.
- Admin-hub lookup/adjustment endpoints — ticket (5).
- Any frontend work in any of the three repos — explicitly deferred by you to
  a later, separate discussion; not even stories are written yet.
- Automatically merging or deduplicating legacy customer records that
  conflict on the same phone number — this ticket links what it can
  confidently link and surfaces the rest; it doesn't guess.
- Deciding the customer-facing brand name for the identity or the points
  currency — out of this department's lane regardless of ticket.

## Risks and unknowns

- **Positioning tension, named plainly rather than assumed away:** a single
  identity shared across competing independent restaurants is structurally
  closer to what a marketplace owns than to "you own your customer" — worth
  being a deliberate choice on the record, not a side effect discovered
  later by a restaurant operator asking why a competitor's customer looks
  familiar to the platform.
- **Phone number recycling.** Carriers reassign numbers. Whoever holds a
  number next inherits the previous holder's identity and history unless the
  design accounts for it — flagged for the architect, not solved here.
- **Legacy phone data is probably messy** — missing, unnormalized, or shared
  across a family — so the mapping in this ticket is a best-effort claim, not
  a guaranteed-correct backfill.
- **SMS OTP has a real recurring cost** via a third-party vendor not yet
  chosen — see Cost.
- **PIPEDA (Canada)** applies to storing phone numbers and building a
  cross-merchant profile of where someone eats — consent and opt-out aren't
  detailed in the raw request and need to be designed in, not bolted on.
- **This may be a one-way door.** A new auth/identity model, once diners
  start using it, is expensive to change later. Flagged for the architect to
  evaluate for G2 — not decided here.

## Cost

- Build: `L` — the largest single ticket in the sequence, since it's the
  foundation everything else depends on.
- Run: SMS OTP requires a third-party vendor with a real per-message cost
  that scales with signups and logins — vendor and exact $/month are the
  architect's to price at design time; flagged now so it isn't a surprise at
  G3. Everything else in this ticket runs inside the existing `aiorders-api`
  Supabase project — no new infrastructure spend beyond the SMS vendor.

## Decision

- **The approver's answer:** approved — the identity/auth/mapping slice (this
  ticket) proceeds as scoped, and the proposed five-ticket sequence stands as
  shape to file incrementally, not as four pre-approved tickets.
- **Date:** 2026-08-28T00:20:57.797718+00:00
- **Notes, verbatim:** "Do create a PRD for the understanding you got for the
  frontend work in different portals so that the knowledge is not lost. We
  will discuss and execute later doesnt mean lose the knowledge and findings
  and learnings while building the backend. We do have a vendor with
  unlimited sms at a monthly fixed cost so thats managed."
- **Read as two instructions, not one:** (1) capture the frontend
  understanding this readback already surfaced — restaurant-marketplace,
  restaurant-portal, and admin-hub implications across the proposed
  sequence — in its own document now, separate from this backend-only PRD, so
  the "separate discussion, later" the approver named earlier doesn't also
  mean losing what's already been figured out. Not a change of scope: frontend
  stays out of every ticket in this sequence, including this one; only the
  knowledge is being preserved, not scheduled. Done as
  `agents/product-manager/specs/loyalty-program-frontend-understanding.md`.
  (2) The SMS OTP vendor risk this PRD's Cost/Risks sections flagged as
  "not yet chosen" is resolved — an existing vendor relationship at a fixed
  monthly cost, unlimited volume, already in place. No dollar figure given and
  no vendor named; carried into the design as a closed cost question but an
  open integration one (which vendor's API, concretely, is for the architect/
  engineer at build time — see the design's Risks).
