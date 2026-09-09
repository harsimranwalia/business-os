---
ticket: ENG-054
project: aiorders-api
status: awaiting-scope
size: M
author: product-manager
created: 2026-09-09
decided:
---

# Loyalty admin/support surfaces — cross-restaurant lookup and manual ledger adjustment/void

## Readback

**There is no raw request to quote this time, and inventing one would be
worse than saying so.** Same position `ENG-027` (item 3) and `ENG-051` (item
4) were both in: nobody wrote a new request for this ticket. It is item 5 —
the last one — of the five-item sequence the approver reviewed and approved
the shape of at `ENG-006`'s G1, and its scope is already stated precisely, by
this department, in a document the approver read and approved. So the
"request" being read back here is that text, quoted as what it is: **the
approved sequencing note, not a customer's words.**

**What was approved,** verbatim from
`agents/product-manager/specs/ENG-006-unified-customer-identity.md`, `##
Feature shape and sequencing`, item 5:

> **Admin/support surfaces** — internal lookup, cross-restaurant view for
> support, and manual ledger adjustment/void. Depends on ENG-006 and (3).

**And that it stands as a sequence,** verbatim from that PRD's `## Decision`
(the approver's own G1 answer, 2026-08-28): the identity slice proceeds "and
the proposed five-ticket sequence stands as shape to file incrementally, not
as four pre-approved tickets."

**And that this specific ticket is wanted now:** filed directly per
`skills/acceptance-check/SKILL.md` step 6b, the moment `ENG-051` (item 4)
reached `verified` in the same pass, on the authority of `ENG-006`'s own G1
already covering the whole shape — the same mechanism that filed `ENG-051`
itself once `ENG-027` verified. **This does not skip this ticket's own G1** —
this PRD still needs a fresh, specific approval before anything is built,
exactly as every prior ticket in this sequence did.

**This closes the sequence.** There is no item 6 on `ENG-006`'s sequencing
note — once this ticket's own G1 is answered, the five-item shape the
approver reviewed on 2026-08-28 is fully filed.

**Understood as:** The four tickets already shipped and verified
(`ENG-006`, `ENG-027`, `ENG-051`, and their sub-tickets `ENG-048`/`049`/`052`/
`053`) gave diners one identity, a growing points balance per restaurant, and
a way to spend it — but every one of those paths is diner- or
restaurant-staff-initiated, and none of them gives AIOrders' own support
staff a way to see across a diner's restaurants or fix a mistake once one
posts. This ticket is the internal-only correction and visibility layer on
top of everything already built: a staff member can look up a diner across
every restaurant they're linked to, see the ambiguous-match conflicts
`ENG-006`'s own linking logic already detects but has never surfaced
anywhere, and reverse a wrong ledger entry without altering the historical
record.

**Assumed, and worth correcting if wrong** (only the ones that change the
build, not its details):

- **"Internal lookup" and "cross-restaurant view for support" are the same
  capability**, not two — a `platform_customers`-centred read surface for
  AIOrders staff. Direct from the frontend-knowledge-capture doc's own
  framing (`agents/product-manager/specs/loyalty-program-frontend-understanding.md`):
  "the one legitimate cross-restaurant read the whole feature has, and it's
  internal-only."
- **The ambiguous-match review queue is in scope here, not a separate
  ticket.** `ENG-006`'s own design
  (`agents/architect/designs/ENG-006-unified-customer-identity.md`) added
  `needs_review`/`review_reason` to `platform_customer_legacy_links` for
  exactly this — two-plus legacy rows at the same restaurant sharing a
  phone, or a diverging name — and states outright that both still get
  linked, "just flagged for a human to look at later (**ticket 5's admin
  surface**, see the frontend knowledge-capture doc)." No other ticket in
  this sequence claims that field. If this ticket doesn't surface it,
  nothing does.
- **"Manual ledger adjustment/void" must preserve `loyalty_ledger_entries`'s
  append-only invariant, not break it.** Every existing consumer (`ENG-027`,
  `ENG-051`) reads the balance as `SUM(points)` over every row for a
  customer at a restaurant — nothing computes or stores a running total.
  A correction has to be a new, clearly-labelled entry that offsets the
  mistake, never an edit or removal of the original row. See Risks: this
  is not a hypothetical concern, it's a named one.
- **This is a new authority tier, not the existing restaurant-staff one.**
  `ENG-027`'s and `ENG-051`'s write paths all authorize on restaurant-scoped
  staff access. This ticket's three capabilities are all about seeing or
  changing data *across* restaurants — restaurant-scoped access is not
  sufficient for any of them, even a restaurant's own staff over their own
  slice of a diner's history. See Risks for what already exists on this
  project that the architect may be able to reuse here.
- **Still backend only.** No frontend, in any repo, same deferral every
  ticket in this sequence has carried. Whatever admin-hub screen eventually
  calls this is separate, later, undesigned work.

**Second reading:** none run, same reasoning `ENG-027` and `ENG-051` both
recorded — `skills/request-readback/SKILL.md` exists to catch two careful
readers disagreeing about ambiguous *raw* input, and there is no raw input
here to diverge on. The reading that matters ran once, at `ENG-006`, and
converged with no material divergence there. It has since been independently
corroborated by every ticket downstream of it: `ENG-007` and `ENG-027`'s own
PRDs named "admin/support surfaces... manual ledger adjustment/void" as
ticket 5's boundary in their own non-goals, and `ENG-051`'s PRD did too, in
the same words, at three different times, by the same author drafting three
different tickets.

## Problem

Support has no way to see a diner's loyalty activity across the restaurants
they're linked to, no way to see the phone-match conflicts `ENG-006`'s own
identity-linking logic already detects and defers (`needs_review`), and no
way to correct a bad ledger entry once one exists — a double-scan, a
redemption processed against the wrong amount. Every write path built so far
(`ENG-027`/`ENG-048`/`ENG-049`/`ENG-051`/`ENG-052`/`ENG-053`) is
restaurant-scoped and diner- or staff-initiated; nothing today can see or fix
something that spans restaurants. A support agent facing a customer dispute
right now has no tool for this at all — the only way to look would be a
direct database query.

## Why now

Item 5, the last one, of the sequence the approver already reviewed and
approved the shape of at `ENG-006`'s G1. Filed the moment item 4 (`ENG-051`)
reached `verified`, per that same G1's standing authorization to continue
without asking again each time — the same position every prior ticket in
this sequence was filed from.

Said plainly rather than dressed up: this is anticipated, not measured. No
support ticket or customer complaint has been logged against the loyalty
program, because nothing customer-facing exists yet for anyone to complain
about. But the diner-facing balance has been earnable and (since `ENG-051`/
`ENG-052`/`ENG-053`) spendable and live in production since this same day —
the exposure to an uncorrectable mistake starts accruing with usage, not with
this PRD, and today there is no way to fix one when it happens.

## Users

AIOrders' own internal support/admin staff — not diners, not restaurant
staff. Not directly reachable yet: no frontend calls this, same invisible-
until-wired-in position every ticket in this sequence has shipped in (see
Risks). Indirect beneficiaries: diners and restaurants whose disputes
eventually get resolved once a staff member has a tool to use.

## Proposed change

After this ships, an authenticated AIOrders staff member can look up a
platform customer (most likely by phone) and see their identity together
with every restaurant they're linked to and their combined earn/redeem
history across all of them — a single view no existing surface provides.
They can also see any legacy-customer match `ENG-006`'s own linking logic
flagged as ambiguous and record a decision on it. And they can void or adjust
a specific ledger entry that turns out to be wrong, which posts as a new,
attributed, reason-carrying entry rather than altering what already
happened. Nothing about how points are earned or redeemed by diners or
restaurants changes; this only adds an internal visibility and correction
layer on top of what already exists.

## Acceptance criteria

1. `[stated]` Given an authenticated internal staff caller and a phone
   number, when they look up a platform customer, then they see that
   customer's platform identity together with every restaurant it's linked
   to — the one cross-restaurant read this whole feature has (extends
   `ENG-006` AC4 to a support-facing surface).
2. `[inferred]` Given a looked-up platform customer, when their activity is
   viewed, then earn and redemption entries from every linked restaurant
   appear together in one ordered history — extending `ENG-051`'s own
   restaurant-scoped version (AC11) to the cross-restaurant case this ticket
   exists to add.
3. `[inferred]` Given a legacy-customer link `ENG-006`'s matching logic
   flagged `needs_review`, when the lookup is viewed, then the flag and its
   `review_reason` are visible — the field has existed since `ENG-006`
   shipped (2026-08-28) and nothing has surfaced it since.
4. `[proposed]` Given a flagged link, when staff record a decision on it
   (confirm or reject the match), then that resolution is recorded and the
   link no longer shows as outstanding.
5. `[stated]` Given a ledger entry staff determine was wrong (a double-scan,
   a mis-processed redemption), when they void or adjust it, then a new
   ledger entry is appended recording the correction — attributed to the
   acting staff member and carrying a reason — and the original entry is
   left unmodified.
6. `[inferred]` Given a posted void/adjustment, when the customer's balance
   at that restaurant is read afterward, then it reflects the correction
   immediately — the same sum-on-read balance every existing ledger consumer
   (`ENG-027`, `ENG-051`) already relies on.
7. `[inferred]` Given any void/adjustment, when it's reviewed later, then who
   performed it, when, and why are all recorded — the minimum audit trail
   for a support action on a money-equivalent balance.
8. `[inferred]` Given a caller without internal staff authority — a diner, a
   restaurant staff member acting through their own restaurant-scoped
   access, or an unauthenticated request — when any of this ticket's
   endpoints are called, then access is rejected. Restaurant-scoped access
   is explicitly not sufficient for any of these three capabilities, even
   over a restaurant's own slice of a diner's history.
9. `[proposed]` Given the same void/adjustment request submitted twice in
   immediate succession (e.g. a network retry), when the second copy
   arrives, then it does not post a second correction — the same
   idempotency shape `ENG-051` already established for redemption.
10. `[inferred]` Given a phone number with no matching platform customer,
    when looked up, then the result is a clear "not found," not an error —
    no identity is fabricated, same meaning `ENG-006`/`ENG-027`/`ENG-051`
    already established for "no match."

## Non-goals

- Any frontend, in any repo — deferred for the whole sequence per `ENG-006`'s
  own sequencing note. No admin-hub screen renders any of this yet.
- Rendering a UI for the `needs_review` queue — this ticket surfaces the
  data; a queue screen is frontend work, not this ticket's.
- Migrating or honoring existing Walletly point balances — an unresolved
  business/goodwill call carried forward from `ENG-027`, not this ticket's
  to make.
- Any change to how points are earned or redeemed by diners or restaurants —
  `ENG-027`'s and `ENG-051`'s paths are untouched.
- Point expiry, pooled or cross-restaurant balances — excluded platform-wide
  since `ENG-006`.
- Automatically resolving a `needs_review` match — staff decide; nothing
  here auto-merges or auto-rejects a flagged link (`ENG-006`'s own non-goal,
  "doesn't guess," still holds).
- Restaurant- or diner-facing dispute tools — this is strictly an internal
  support tool; a restaurant operator or diner still has no self-service way
  to raise or see a dispute.
- Database-level protection against `UPDATE`/`DELETE` on
  `loyalty_ledger_entries` — real, and named in Risks, but a schema-hardening
  question that predates this ticket and already has its own open proposal;
  not this ticket's to fix.
- Bulk or batch adjustment tooling — one entry at a time, matching the shape
  of every other write path in this sequence.
- Rate-limiting or abuse detection on these internal endpoints themselves —
  not asked for anywhere in the sequence; internal-staff-only access is the
  boundary this ticket relies on.

## Risks and unknowns

- **`loyalty_ledger_entries`'s append-only rule is enforced by comment and
  convention only, not by the database.** An open proposal
  (`principal-engineer`, `proposals.md`, 2026-09-07) found that no migration
  on this project revokes `UPDATE`/`DELETE` on the table from `service_role`
  — which bypasses RLS by default on this project — and named this exact
  ticket by number as the scenario it's worried about: "a mis-written
  correction on **ticket 5** of this same sequence... could mutate or delete
  a ledger row with no database-level guardrail." This ticket is the first
  one to hand a human the power that proposal warns about. Fixing the
  constraint itself is out of this ticket's scope (Non-goals), but the
  architect should treat safe-by-construction design here (append-only at
  the code path this ticket adds, regardless of what the database allows)
  as a live requirement, not a nice-to-have.
- **This needs a new authority tier, not the existing restaurant-staff
  check.** Every existing loyalty write path (`ENG-027`, `ENG-051`)
  authorizes on restaurant-scoped staff access
  (`requireRestaurantAccess()`). This ticket's three capabilities are all
  explicitly cross-restaurant. This project already has a live internal-
  staff role in production — `admin`/`sub-admin`, checked via
  `admin-portal`'s router-level `authenticate()` gate, already used for
  e.g. influencer relationship notes (`ENG-010`) — the natural fit, not a
  new concept to invent. But that same router's allowlist also grants
  `partner-admin`/`partner-user` (external agency/reseller roles), and
  `ENG-010` already found that reusing the blanket gate as-is would
  over-grant those external roles access to data meant AIOrders-staff-only,
  and added a narrower in-handler check on top of it instead of changing
  the shared gate. The same shape of over-grant risk applies here to
  cross-restaurant loyalty and ledger-adjustment data — flagged for the
  architect to evaluate and reuse the same pattern, not assume "internal
  auth" is automatically solved by the existing router alone.
- **This project's own history of missing or wrong authorization checks on
  `aiorders-api`** — `ENG-022`, `ENG-029`, `ENG-030`, `ENG-035`, `ENG-036`,
  `ENG-050`, all on this same project — is why the point above is named
  explicitly rather than assumed away, the same citation `ENG-051`'s own PRD
  used for the same reason.
- **A void that reverses an earn could take a balance negative** if the
  diner already redeemed part of the now-reversed points elsewhere at that
  restaurant. No stated business rule yet for whether that should be
  allowed, capped at zero, or blocked outright — named, not resolved; left
  for the architect or approver.
- **No frontend exists yet, so "support has no tool today" is only partly
  solved by a backend-only ticket.** Same invisible-until-wired-in position
  every ticket in this sequence has shipped in — an `admin`/`sub-admin`-
  equivalent caller can reach this directly once built, but a support agent
  with no client calling it still has nothing to click. Said plainly rather
  than overclaiming the Problem above is fully solved here.
- **How many `needs_review` links have accumulated since `ENG-006` shipped
  (2026-08-28) is unknown** — nothing has read the field yet, so this ticket
  doesn't know today whether the queue is empty or large. Worth a quick live
  count at design or build time rather than assuming either way.

## Cost

- Build: `M` — reuses `ENG-006`'s `platform_customers`/
  `platform_customer_legacy_links` tables (including the
  `needs_review`/`review_reason` fields nothing has read since), and
  `ENG-027`'s/`ENG-051`'s/`ENG-052`'s `loyalty_ledger_entries` table and its
  append-only, sum-on-read pattern directly; no new external integration, no
  cron, no new vendor. The new surface is a small set of internal-only
  read/write endpoints plus, most likely, a narrower authorization check
  layered on this project's existing `admin-portal` gate — multiple files/
  surfaces and a new interface, but no new architecture or data model.
  Two things could push this to `L`, both flagged above and left for the
  architect to resolve at design time: whether the negative-balance question
  needs more than a straightforward compensating entry, and whether the
  database-level ledger-hardening proposal gets folded into this ticket's
  own build rather than handled as its own separate item.
- Run: `$0`/month — runs inside the existing `aiorders-api` Supabase
  project, no new vendor.

## Decision

Filled in after G1.

- **The approver's answer:**
- **Date:**
- **Notes:**
