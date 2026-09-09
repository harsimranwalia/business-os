---
ticket: ENG-051
project: aiorders-api
status: approved
size: M
author: product-manager
created: 2026-09-08
decided: 2026-09-08T19:53:32.308503+00:00
---

# Redemption API and QR issuance/scanning — spend loyalty points at the earning restaurant

## Readback

**There is no raw request to quote this time, and inventing one would be
worse than saying so.** Same position `ENG-027` (item 3) was in: nobody wrote
a new request for this ticket. It is item 4 of the five-item sequence the
approver reviewed and approved the shape of at `ENG-006`'s G1, and its scope
is already stated precisely — by this department, in a document the approver
read and approved. So the "request" being read back is that text, quoted as
what it is: **the approved sequencing note, not a customer's words.**

**What was approved,** verbatim from
`agents/product-manager/specs/ENG-006-unified-customer-identity.md`,
`## Feature shape and sequencing`, item 4:

> **Redemption API and QR issuance/scanning** — generates the customer's QR
> code, enforces that a scan only ever touches the scanning restaurant's own
> balance for that customer, and performs the redemption. Depends on ENG-006
> and (3).

**And that it stands as a sequence,** verbatim from that PRD's `## Decision`
(the approver's own G1 answer, 2026-08-28): the identity slice proceeds "and
the proposed five-ticket sequence stands as shape to file incrementally, not
as four pre-approved tickets."

**And that this specific ticket is wanted now:** unlike item 3, there is no
separate "continue the sequence?" question and answer to cite here — this
ticket was filed directly per `skills/acceptance-check/SKILL.md` step 6b, the
moment item 3 (`ENG-027`) reached `verified` in the same pass, on the
authority of `ENG-006`'s own G1 already covering the whole shape (the
approver, clarifying against `ENG-006`, 2026-08-28: continuing an
already-approved sequence "isn't agent-originated — it's the approver's own
request, already reviewed once"). That is the current, direct reading of
step 6b; `ENG-027` itself predates the department settling on filing
directly without an intermediate question. **This does not skip this
ticket's own G1** — this PRD still needs a fresh, specific approval before
anything is built, exactly as `ENG-027` did.

**Understood as:** Both of this ticket's dependencies are shipped and
verified and neither does anything about spending on its own. `ENG-006` gave
diners one identity across every restaurant. `ENG-007` gave every restaurant
an effective-dated redemption value — what a point is worth — that nothing
has read since it shipped. `ENG-027` gave diners a growing, append-only
points balance per restaurant that nothing can reduce. This ticket is the
piece that lets a balance actually be spent: a diner is issued something
that identifies them platform-wide, a restaurant resolves it and a points
amount at the point of sale, and the system debits that diner's balance at
**that restaurant only**, converting the points to value at that
restaurant's own rate.

**Assumed, and worth correcting if wrong** (only the ones that change the
build, not its details):

- **The code identifies the diner platform-wide — one code, not one per
  restaurant.** Direct from `ENG-006`'s own framing of the eventual user
  benefit: "diners (one identity and one QR instead of being re-created at
  every restaurant)."
- **This ticket issues the underlying scannable data (a code/token), not a
  rendered QR image.** Frontend is explicitly deferred for the whole
  sequence (`ENG-006`'s sequencing note, restated on this ticket's own board
  file) — turning a code into a displayed QR image is presentational work
  for whichever frontend eventually calls this, not this ticket's. If this
  is wrong and an actual image needs generating now with nothing to show it
  to, say so.
- **The code does not expire or rotate.** It behaves like a standing loyalty
  card, not a one-time-use token. Flagged as a risk below rather than solved
  here — see Risks.
- **Redemption is restaurant-initiated, not diner-initiated** — a staff
  member enters/scans the code plus an amount, the same shape `ENG-027`
  already used for dine-in earn (`record_dine_in_earn`), because no diner
  app or session-driven checkout exists to initiate it from the other side.
- **Redemption writes to the same `loyalty_ledger_entries` table `ENG-027`
  built, as a negative-points entry — not a new ledger.** `ENG-027`'s own
  design already reserved this: "the schema should not prevent a negative
  value later even though this ticket only ever writes positive ones."
- **A diner can only ever redeem against their own balance at the specific
  restaurant doing the redemption** — never a pooled or cross-restaurant
  balance (excluded platform-wide since `ENG-006`), and never another
  diner's balance. This is this ticket's central requirement, not an edge
  case — see Risks.

**Second reading:** none run for this ticket, for the same reason `ENG-027`
recorded none — `skills/request-readback/SKILL.md` exists to catch two
careful readers disagreeing about ambiguous raw input, and there is no raw
input here to diverge on. The reading that matters was already run once, at
`ENG-006`, and converged with no material divergence there. It has since
been independently corroborated twice without prompting: `ENG-007`'s own PRD
(written after `ENG-006`, by the same PM, checked against a different
ticket's boundary) named "redemption execution or QR code generation/
scanning" as ticket 4's scope in its own non-goals, unprompted and in the
same words; `ENG-027`'s own PRD did the same. Three independent write-ups of
this sequence, at three different times, drew this ticket's boundary in the
same place.

## Problem

Diners accumulate points at a restaurant once they've verified a platform
identity (`ENG-006`), and every restaurant already has a redemption value on
file for what a point is worth (`ENG-007`, shipped 2026-08-30, never read by
anything since) — but nothing lets a diner spend what they've earned. A
balance that can only go up is not a loyalty program a restaurant can point
to; it's a number nobody can act on. Every restaurant counting on this
program for a repeat-visit incentive currently cannot honor it at the point
of sale.

## Why now

Item 4 of the five-ticket sequence the approver already reviewed and
approved the shape of at `ENG-006`'s G1. Filed the moment item 3 (`ENG-027`)
reached `verified`, per that same G1's standing authorization to continue
the sequence without asking again each time. No stated deadline and no
committed launch restaurant — this is sequencing work the approver already
scoped, the same position every prior ticket in this sequence was in.

## Users

Not directly user-facing yet — invisible until a frontend lands on top of
it, same as `ENG-006`/`ENG-007`/`ENG-027`. Eventual users: diners (spending
points at a participating restaurant) and restaurant staff (processing the
redemption at the point of sale, the same role `ENG-027` already gave them
for recording a dine-in earn).

## Proposed change

After this ships, a diner with a verified platform identity can be issued a
single code that identifies them, the same code at every restaurant. A
restaurant staff member can submit that code together with a points amount
at the point of sale, and the system redeems exactly that many points from
the diner's balance **at that restaurant only**, converting them to value at
that restaurant's own configured redemption rate — provided the diner has
enough balance there. Nothing about how points are earned changes; this
ticket only adds a way to spend them.

## Acceptance criteria

1. `[stated]` Given a diner with a verified platform identity, when they are
   issued their code, then it identifies them uniquely and consistently
   across every restaurant on the platform — one code, not one per
   restaurant.
2. `[inferred]` Given a diner with no verified platform identity, when a code
   is requested for them, then none is issued — no identity is fabricated,
   same meaning `ENG-006`/`ENG-027` already established for "no platform
   identity."
3. `[stated]` Given a restaurant staff member with access to a restaurant,
   when they submit a diner's code together with a points amount to redeem,
   then the system resolves the code to exactly one diner.
4. `[stated]` Given a resolved diner and the restaurant submitting the
   redemption, when it is processed, then only that diner's balance **at
   that specific restaurant** is affected — never their balance at any other
   restaurant, and never another diner's balance anywhere. This is the
   ticket's central requirement, not an edge case.
5. `[inferred]` Given a redemption amount greater than the diner's current
   balance at that restaurant, when submitted, then it is rejected with a
   clear reason and no ledger entry is written.
6. `[inferred]` Given a restaurant with no configured redemption value, when
   a redemption is attempted there, then it is rejected as "not enrolled" —
   same meaning `ENG-007` already established for a missing rate.
7. `[stated]` Given a valid redemption within balance, when it is processed,
   then it converts the redeemed points to a dollar value using that
   restaurant's own currently-effective redemption value (`ENG-007`) and
   writes one permanent, append-only ledger entry recording the debit —
   mirroring `ENG-027`'s own append-only earn entries.
8. `[inferred]` Given a successful redemption, when the diner's balance at
   that restaurant is read afterward, then it reflects the debit
   immediately (the same sum-on-read balance `ENG-027` already established).
9. `[proposed]` Given the same redemption request submitted twice in
   immediate succession (e.g. a network retry), when the second copy
   arrives, then it does not debit the balance a second time.
10. `[stated]` Given a diner's code and a restaurant staff member without
    access to that restaurant, when a redemption is attempted, then it is
    rejected the same way every other restaurant-scoped action already
    rejects an unauthorized caller (`ENG-027`'s `requireRestaurantAccess`
    pattern).
11. `[proposed]` Given a diner's balance history at one restaurant, when it's
    read, then earns and redemptions are both visible in one ordered
    history — extending `ENG-027`'s existing read surface rather than
    replacing it.

## Non-goals

- Any frontend, in any repo — deferred for the whole sequence per `ENG-006`'s
  own sequencing note. No UI renders a QR image and no camera-based scanning
  exists yet.
- Rendering the code as an actual QR image/bitmap — proposed as this
  ticket's own boundary (Readback); the code itself is this ticket's output,
  not an image of it.
- Admin/support surfaces, internal cross-restaurant lookup, and manual
  ledger adjustment or void of a bad redemption — ticket 5.
- Migrating or honoring existing Walletly point balances — an unresolved
  business/goodwill call carried forward from `ENG-027`, not this ticket's
  to make.
- Any change to how points are earned — `ENG-027`'s accrual paths are
  untouched.
- Point expiry, pooled or cross-restaurant balances — excluded platform-wide
  since `ENG-006`.
- Rate-limiting or fraud/abuse detection on redemption attempts beyond the
  restaurant-scoping itself — named in Risks, not built here.
- Rotating or expiring the diner's code — named in Risks, not solved here.

## Risks and unknowns

- **This is the department's first debit-shaped write path against real
  point balances, on the project with this instance's entire history of
  missing-authorization P0s** — `ENG-022` (cross-tenant PII/write exposure),
  `ENG-029` (autopilot's 8 actions with no restaurant-ownership check),
  `ENG-030` (analytics function with no auth at all), `ENG-035`/`ENG-036`
  (system-triggered auth bypasses), `ENG-050` (RPC functions grantable to
  `anon`) — all on this same `aiorders-api` project. This ticket's own
  defining requirement, "a scan only ever touches the scanning restaurant's
  own balance," is exactly the class of check this project has repeatedly
  shipped without. Named plainly so the architect treats it as the
  load-bearing design question it is, not a formality, and has a
  already-proven pattern to reuse rather than invent: `ENG-027`'s
  `requireRestaurantAccess()`.
- **A stable, long-lived code is a bearer credential.** Anyone holding it —
  a screenshot, a photo — can trigger a redemption against the diner's
  balance at any restaurant, indistinguishable from the diner presenting it
  themself. Flagged, not solved: the mitigation (rotation, a second factor,
  a per-redemption cap) is the architect's call, and may be reasonable to
  defer given a restaurant staff member is physically present for every
  redemption today — the same "unverifiable, but a human is there" shape
  `ENG-027` already accepted for dine-in earn.
- **Walletly's existing point balances remain unreachable once its contract
  lapses** (carried forward from `ENG-027`, still unresolved, still not this
  ticket's to decide) — a diner who held points under the old vendor starts
  this system at zero.
- **No frontend exists to present a QR image or scan one**, so nothing here
  is reachable by a real diner or restaurant yet — the same
  invisible-until-the-frontend-lands position every ticket in this sequence
  has been in.

## Cost

- Build: `M` — reuses `ENG-006`'s identity/session, `ENG-007`'s
  effective-dated redemption-value lookup, and `ENG-027`'s append-only
  ledger plus its restaurant-scoped-action pattern
  (`requireRestaurantAccess`, the `record_dine_in_earn` shape); no new
  external integration, no cron, no new vendor. Provisional stub guess was
  `L`; narrowed down on the analysis above, the same direction `ENG-027`'s
  own size moved the other way after its own G1 found real added scope. The
  one open question that could push this back to `L`: whether the diner's
  code needs to be stored/revocable (a new table) rather than a stateless
  derived value — left for the architect to size at design time.
- Run: `$0`/month — runs inside the existing `aiorders-api` Supabase
  project, no new vendor.

## Decision

**approved** — `decided: 2026-09-08T19:53:32.308503+00:00`
(`inbox/_handled/2026-09-08-eng051-g1-scope.md`). No additional comment. Read
per the G1 item's own stated default: both "worth confirming, not blocking"
questions — the code is issued as data, not a rendered image; the code
doesn't expire or rotate — resolve to the smaller, already-deferred-frontend-
consistent reading, since the approver said nothing to redirect either one.
Carried into design as defaults, not left open for the architect to guess
at.
