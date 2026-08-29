---
ticket: ENG-007
project: aiorders-api
status: draft
size: S
author: product-manager
created: 2026-08-28
decided:
---

# Per-restaurant loyalty configuration — earn rates and redemption value

## Readback

**You said:** "Per-restaurant loyalty configuration — earn % (online,
dine-in) and a redemption value, per restaurant, effective-dated so a later
rate change doesn't rewrite the meaning of past ledger entries. No
dependency on `ENG-006`; could build in parallel. Backend and migrations go
in `aiorders-api`, same as `ENG-006`. Frontend is out of scope for this
whole sequence, same as `ENG-006` — a separate, later discussion." (full
filed request preserved verbatim in the ticket's `## Input`, from
`inbox/_handled/2026-08-28-eng006-sequence-item-2.md`)

**Understood as:** Item 2 of the five-ticket loyalty sequence the approver
already reviewed the shape of at `ENG-006`'s G1. A per-restaurant
configuration surface holding three values — earn % for online orders, earn
% for dine-in, and one redemption value — each effective-dated so that a
rate changed tomorrow never alters what a transaction from last month meant
when read back later. Pure configuration data: no ledger, no points, no
identity dependency, no frontend. This unblocks ticket 3 (points
ledger/earn API) and ticket 4 (redemption/QR), both of which need a rate to
compute against and have none today.

**Requirements:**
1. `[stated]` Each restaurant has an online earn % and a dine-in earn %,
   configured independently.
2. `[stated]` Each restaurant has a redemption value — what a point is
   worth on redemption — configured per restaurant, not platform-wide.
3. `[stated]` All three values are effective-dated: a later rate change
   never rewrites what an earlier ledger entry's rate was.
4. `[stated]` No dependency on `ENG-006` — this ticket's data model is
   keyed on restaurant alone, not on the platform-customer identity.
5. `[stated]` Backend and migrations only, in `aiorders-api`. No frontend
   in any repo, in this ticket or anywhere else in the sequence.
6. `[inferred]` A rate change creates a new effective-dated record rather
   than editing the existing one, so any point-in-time read — including a
   future ledger entry — resolves against whichever record was actually in
   effect at that time.
7. `[inferred]` Redemption value is a single figure per restaurant, not
   split online/dine-in — the request lists it separately from the two
   earn rates.
8. `[inferred]` Downstream tickets need to look these values up
   programmatically, so this ticket exposes at least a read path ("the
   effective rate for restaurant X as of time T") even though nothing
   consumes it yet.
9. `[proposed]` A minimal internal write path (API or equivalent) to set a
   new effective-dated rate exists in this ticket — nothing in the
   sequence has a frontend to drive it otherwise, and the values have to
   enter the system somehow.
10. `[proposed]` A restaurant with no configured rate yet reads as "not
    enrolled" (earn/redeem inactive), not an error and not a silent
    platform-wide default.
11. `[proposed]` Basic validation — earn % and redemption value can't be
    negative — so a fat-fingered config can't produce nonsensical ledger
    math downstream.

**Assumed, and worth correcting if wrong:**
- The unit basis for earn % (percentage of what — order subtotal,
  presumably) and for redemption value (currency per point, a flat credit,
  something else) is unresolved by the request. Left for the architect to
  fix at design time, not guessed here.
- "Restaurant" means the same single-location entity `ENG-006`'s PRD
  assumed, not re-litigated in this ticket.
- Whether a rate change can be backdated (retroactively altering what "was"
  in effect) or only ever takes effect in the future is unresolved — it
  changes the write-path validation materially and is flagged for the
  architect rather than decided here.

**Second reading agreed / diverged on:** Two independent readings were run
— this PM's, and, blind to it, the architect's (an independent subagent
given only the raw request and the business profile, nothing else). They
converged tightly: a per-restaurant config table holding the two earn rates
and one redemption value, effective-dated so historical reads never change
meaning, backend/migrations only in `aiorders-api`, no dependency on
`ENG-006`'s identity model. **No material divergence** — nothing where one
reading included scope the other didn't, or where they disagreed about
what this is for. The architect's reading added technical texture a PM
lens wouldn't surface alone: the likely temporal table shape (restaurant,
effective-from, the three values, guarded against overlapping ranges), the
two candidate mechanisms for keeping a rate change non-retroactive (the
ledger snapshots the rate at write time, versus every historical read
pinning to whichever record was effective then — left to the architect's
design rather than fixed here), and a sharper framing of the open unit
question (dollars-per-point vs. percentage vs. flat credit, not just
"currency"). Notably, both readings independently proposed the same
default for an unconfigured restaurant — "not enrolled" rather than an
error or a platform-wide fallback — without seeing each other's answer.

**Not doing:** the points ledger and earn/redeem transaction history
(ticket 3); redemption execution or QR generation/scanning (ticket 4);
admin/support surfaces (ticket 5); any frontend in any repo; deciding the
actual $/% numbers for any real restaurant.

## Problem

Tickets 3 and 4 of the approved loyalty sequence both need a per-restaurant
rate to compute against — an earn percentage and a redemption value — and
nothing in the system stores either today. Whatever gets added has to
survive a rate change later without corrupting the historical record of
what a past transaction actually earned or was worth.

## Why now

Item 2 of the five-ticket sequence the approver already reviewed and
approved the shape of at `ENG-006`'s G1 ("the proposed five-ticket
sequence stands as shape to file incrementally, not as four pre-approved
tickets"). No dependency on `ENG-006`, so it could have shipped in
parallel; filed now because `ENG-006` just verified and the approver's own
instruction is to continue the sequence one ticket at a time ("we finish
one ticket then you file next and seek approval then next then next till
feature is complete").

## Users

Not directly user-facing yet — invisible until the ledger (3) and
redemption (4) tickets land on top of it, same as `ENG-006`. Eventual
users: restaurant operators, who will set their own rates once a frontend
surface exists in the separate, later discussion; and indirectly diners,
once points start accruing against these rates.

## Proposed change

After this ships, every restaurant can have an online earn %, a dine-in
earn %, and a redemption value on file, effective-dated, with a full
history of what was true when. Nothing about the ordering or diner
experience changes yet — there's still no ledger, no points balance, and
no redemption until tickets 3 and 4 ship.

## Acceptance criteria

1. `[stated]` Given a restaurant with no configuration yet, when a new
   online earn %, dine-in earn %, and redemption value are set with an
   effective date, then those become the restaurant's current effective
   configuration.
2. `[stated]` Given a restaurant with an existing effective configuration,
   when a new rate is set with a later effective date, then the new record
   becomes current as of that date and the prior record's values remain
   readable, unchanged, for any point in time before it.
3. `[inferred]` Given a query for a restaurant's effective rate as of a
   specific past timestamp, when that timestamp falls before a later rate
   change, then the rate actually in effect at that timestamp is returned
   — never the current one.
4. `[inferred]` Given a restaurant that has never been configured, when its
   effective rate is queried, then the system reports it as not enrolled
   rather than returning a default numeric rate or an error.
5. `[proposed]` Given an attempt to set a negative earn % or a negative
   redemption value, when submitted, then it's rejected with a clear
   reason.
6. `[proposed]` Given two effective-dated records for the same restaurant
   with overlapping or conflicting date ranges, when a new one is
   submitted, then the conflict is rejected rather than silently creating
   an ambiguous history.

## Non-goals

- The points ledger, balances, and earn/redeem transaction history —
  ticket 3.
- Redemption execution or QR code generation/scanning — ticket 4.
- Admin/support surfaces — ticket 5.
- Any frontend work in any repo — deferred for the whole sequence, not
  just this ticket.
- Deciding the actual $/% numbers for any real restaurant — this ticket
  builds the capability to configure, not the initial data.

## Risks and unknowns

- **Retroactive vs. future-only rate changes** is unresolved and changes
  the write-path validation materially — flagged for the architect, not
  decided here.
- **Concurrent writes** — two config changes for the same restaurant
  submitted near-simultaneously — needs an explicit design answer (e.g. an
  overlapping-range constraint), not left to hope.
- No stated deadline and no committed launch restaurant, same as `ENG-006`
  — this is sequencing work the approver already scoped, not something a
  restaurant is asking for today.
- Genuinely independent of `ENG-006` per the request's own text — a
  candidate to build in parallel with anything else in flight; that's the
  EM's sequencing call at `ready`, not decided here.

## Cost

- Build: `S` — a single effective-dated config table plus a minimal
  read/write surface, materially smaller than `ENG-006` (no auth, no
  session, no identity mapping).
- Run: `$0` — runs inside the existing `aiorders-api` Supabase project, no
  new vendor, no new infrastructure.

## Decision

Filled in by the approver.
