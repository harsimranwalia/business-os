---
ticket: ENG-051
project: aiorders-api
author: architect
created: 2026-09-08
adrs: ["ADR-022"]
one_way_doors: []
touches_data: true
touches_models: false
---

# Redemption API and QR issuance/scanning — technical design

## Approach

Investigated against `origin/main` (`fb26921`, 2026-09-08) via `git fetch` +
`git show`/`git grep` — the department worktree (`_eng/aiorders-api`)
currently sits on `ENG-049`'s own branch (a separate, already-shipped ticket's
checkout left in place), so reading through git avoided touching it, same
practice `ENG-027`'s own design used when it hit the identical situation.

**Half this ticket's own name is already built.** "QR issuance" (AC1/AC2)
needs a value that identifies a diner uniquely and consistently across every
restaurant, issued only once they have a verified platform identity, never
expiring or rotating (PRD Readback/`## Decision` — both defaults confirmed by
the G1 answer, not open to re-litigate here). `platform_customers.id`
(`references auth.users(id)`, `20260828120000_platform_customer_identity.sql`)
already satisfies all three exactly: one row per verified phone identity,
shared across every restaurant, permanent. It is also **already returned to
the diner's own client** — `platform-customer-auth/verify`
(`ENG-006`'s own Interfaces) returns the platform customer as part of
completing phone/OTP verification, and separately the row is independently
`select`-able by its own owner today via the live
`platform_customers_select_own` RLS policy (`auth.uid() = id`, same
migration). A diner's client already holds `auth.uid()` the moment a Supabase
session exists — which **is** this value. **No new issuance endpoint, table,
or column is needed for AC1/AC2** — the code is `platform_customers.id`,
submitted verbatim as `redeem_points`'s `code` field. See `ADR-022` for the
alternative shapes considered and rejected, and Risks for what accepting the
PRD's own bearer-credential framing at face value costs.

**Redemption reuses three established patterns rather than inventing a
fourth write path on this table.** `record_dine_in_earn`/`get_loyalty_balance`
(`brand-portal/loyalty.ts`, `ENG-027`/`ENG-049`) already established: staff
access is `requireRestaurantAccess(restaurant_id, supabase, user)`
(`brand-portal/utils.ts:117`) checked before anything else (AC10); a rate is
resolved by the same effective-dated read `ENG-007` established
(`restaurant_loyalty_configs` ordered by `effective_from desc`, here read
`redemption_value_per_point` as of `now()` — redemption, like dine-in, has no
order to anchor a past timestamp to); balance is `SUM(points)` on read, never
a maintained counter (`ENG-027`'s own choice, unchanged, AC8 is automatic as
a result); and `loyalty_ledger_entries` is append-only, one row per credit
*or* debit, RLS deny-by-default/service-role-only (`20260907130000...sql`).
The table's own comment already anticipated this ticket: "`points` is plain
numeric rather than positive-only so that entry type can exist later even
though this ticket only ever writes positive ones" (`ENG-027`'s migration,
referring to exactly the negative-entry case this ticket now writes).

**The one genuinely new mechanism is a guarded, idempotent debit function,**
`redeem_points_if_eligible`, structured the same way `credit_order_if_eligible`
already is: one `security definer` Postgres function, one transaction, a
status-text return (`invalid_code` | `not_enrolled` | `insufficient_balance`
| `redeemed`), called via `supabase.rpc(...)` from the brand-portal handler.
Unlike the earn path, redemption has no `orders` row to guard a retry against
via row-level locking, and balance is computed by summing many rows rather
than reading one — so the idempotency mechanism has to be different: a
caller-supplied `idempotency_key`, unique when present (same "unique when
present" shape `order_id` already uses on this table), checked **first,
inside a per-`(diner, restaurant)` advisory lock**, before the balance is
even read. Checking it first is load-bearing, not stylistic: a genuine retry
arrives *after* the original request's own insert has already reduced the
balance, so recomputing the balance before checking the key would make a
legitimate retry fail as `insufficient_balance` — see Interfaces.

**Not to be confused with the *other* "redemption" on this same project.**
`ADR-019`/`ENG-019` (`orders.promos` matched against a marketing coupon code,
for campaign ROI) is a completely unrelated concept that happens to share the
word — noted so a future reader searching this codebase for "redemption"
isn't misled the way `observations.md`'s 2026-08-29 "Foodswipe" entry already
flagged for a different pair of terms on this same instance.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `loyalty_ledger_entries` | Alter — widen the `source` check to add `'redemption'`; widen the three existing per-source checks (`order_id`, `fulfillment_reason`, `created_by`) to cover it; add a new points-sign-by-source check; add nullable `idempotency_key text`, unique when present | database |
| New DB function `redeem_points_if_eligible(...)` | New | database |
| `brand-portal/loyalty.ts` | Modify — new `redeemPoints` handler; extend `handleLoyalty`'s switch; widen `LoyaltyLedgerEntry.source`'s union type | backend |
| `brand-portal/index.ts` | Modify — +1 `case 'redeem_points':` line, same pattern the two existing loyalty actions already use | backend |
| `platform_customers`, `platform_customer_legacy_links`, `restaurant_loyalty_configs`, `restaurants` | None — read-only from this ticket | — |

## Data

Intent and constraints only — `database` owns the migration
(`skills/schema-change/SKILL.md`); exact constraint names below are this
design's best reading of Postgres's auto-generated names on the live table
and should be confirmed (`\d+ loyalty_ledger_entries`) rather than assumed
before writing the `DROP CONSTRAINT`.

**`loyalty_ledger_entries`, widened, not replaced.** A redemption is a
negative-points row on the same table `ENG-027` built, not a new table —
per this ticket's own PRD Readback ("writes to the same `loyalty_ledger_entries`
table... not a new ledger").

- `source` check: add `'redemption'` to the allowed set.
- `order_id` / `fulfillment_reason` / `created_by` per-source checks: each
  currently reads `(source = 'online_order' and X) or (source = 'dine_in' and
  not-X)`. Each gets a third arm — `redemption` behaves like `dine_in` for
  `order_id` (null: no order exists) and `fulfillment_reason` (null: no
  fulfilment window exists), and *also* like `dine_in` for `created_by`
  (not null: a staff member submitted it, and this is the department's first
  **debit**-shaped write against a real balance — an audit trail matters at
  least as much here as it does for dine-in's own unverifiable-amount risk).
- **New:** a points-sign-by-source check —
  `(source in ('online_order','dine_in') and points >= 0) or (source =
  'redemption' and points < 0)`. **`>= 0`, not `> 0`, for the earn sources** —
  `credit_order_if_eligible`'s own `greatest(cart - discount, 0)` floor and a
  legally-configurable `0`-percent rate both already make a `0`-point earn
  entry a real, unconstrained-today case; a strict `> 0` here would be a
  behavior change to a path this ticket doesn't touch, not a tightening. A
  redemption entry can never legitimately be `0` — the handler rejects a
  non-positive `points` input before it ever reaches this function (mirrors
  `record_dine_in_earn`'s own `amount` validation).
- **New:** nullable `idempotency_key text`, `unique` when present — same
  nullable-safe shape `order_id`'s own constraint already uses on this table
  (Postgres treats every `NULL` as distinct under a plain `UNIQUE`, so this
  needs no partial index either).

No change to RLS (still zero policies, deny-by-default, service-role only —
every caller is this ticket's own new function, `security definer`, same as
every other write to this table) and no change to any other table.

**Query shapes this needs**, for `database` to confirm indexing is
sufficient rather than guessed here: the existing
`loyalty_ledger_entries_customer_restaurant_idx` on `(platform_customer_id,
restaurant_id)` already backs both the balance-ceiling check and the
restaurant's rate lookup already has its own index (`ENG-007`); the new
`idempotency_key` lookup is a point-lookup on a column the `unique`
constraint above already indexes, so no new index is needed beyond the
constraint itself.

## Interfaces

**`brand-portal` action (new): `redeem_points`.** Payload `{restaurant_id,
code, points, idempotency_key}`. `requireRestaurantAccess(restaurant_id,
supabase, user)` first — failure → the same uniform failure shape every
other `requireRestaurantAccess` denial in this file already produces today: a
thrown `Error`, caught by `index.ts`'s top-level handler, returned as an
HTTP `500` with `{error: 'Internal server error', details: ...}` (AC10 says
"the same way every other restaurant-scoped action already rejects" — that
way is, as of `principal-engineer`'s 2026-09-07 finding, `500`-shaped
despite every design template in this sequence calling it "403-shaped." This
design does not repeat that mislabel, and does not fix the mismatch either —
an unrelated, already-flagged, project-wide inconsistency; fixing it here
would be exactly the drive-by refactor `engineering-standards.md` forbids).
`code`/`idempotency_key` missing, or `points` not a positive finite number →
`400`-shaped rejection (same validation depth `record_dine_in_earn` already
applies to its own `phone`/`amount`), no RPC call made.

Calls `supabase.rpc('redeem_points_if_eligible', {p_platform_customer_id:
code, p_restaurant_id: restaurant_id, p_points: points, p_idempotency_key:
idempotency_key, p_created_by: user.id})`. On `invalid_code` or
`not_enrolled`, returns `{success: true, result}` directly — a live,
distinct, non-fabricated response, same reasoning `record_dine_in_earn`'s own
`not_enrolled`/`no_platform_identity` responses already use (AC6, and AC3's
"resolves to exactly one diner" by construction: `code` is a primary key, so
resolution is always exactly one row or none, never ambiguous). On
`insufficient_balance` or `redeemed`, calls the existing, **unchanged**
`readBalance(supabase, code, restaurant_id)` to attach the diner's current
balance to the response — cheap (already the query the function itself just
ran once inside its own transaction) and immediately useful to whichever
future frontend calls this (staff seeing "only 340 points available" without
a second round trip).

**DB function (new): `redeem_points_if_eligible(p_platform_customer_id uuid,
p_restaurant_id uuid, p_points numeric, p_idempotency_key text, p_created_by
uuid) → text`.** One transaction, `security definer`, `set search_path =
'public'`, `revoke`n from `public`/`anon`/`authenticated` and `grant`ed to
`service_role` only — the identical two-statement grant `database` already
had to apply to `credit_order_if_eligible`, for the identical reason
(Supabase's own default privileges grant `EXECUTE` to `anon`/`authenticated`
directly at function-creation time; a bare `REVOKE ... FROM PUBLIC` does not
touch that).

1. Reject `p_points <= 0` or a missing `p_idempotency_key` outright
   (`raise exception` — a caller/programmer error, not a business outcome;
   the handler already checks both, this is the same defense-in-depth
   `credit_order_if_eligible` applies to its own `p_fulfillment_reason`).
2. `pg_advisory_xact_lock(hashtextextended(p_platform_customer_id::text ||
   ':' || p_restaurant_id::text, 1))` — serializes concurrent redemption
   attempts for the *same diner at the same restaurant* (the actual race:
   two near-simultaneous submissions both reading a balance that supports
   each individually but not both together) without serializing anything
   for a different diner or a different restaurant. **Seed `1`, not
   `ENG-007`'s `0`** — same function, deliberately namespaced so this lock
   and the loyalty-config ordering lock can never coincide on the same
   64-bit key, cheap to do since both already share the mechanism.
3. **Idempotency check, before anything else is read.** Look up
   `loyalty_ledger_entries` by `idempotency_key`. Found, and its
   `(platform_customer_id, restaurant_id, points)` all match this
   request (`points = -p_points`) → return `'redeemed'` again, insert
   nothing (a replay reports success again, the same "idempotent, not an
   error" convention `broadcast-unsubscribe/unsubscribe.ts` already
   documents for its own re-submission case). Found, and any of the three
   don't match → `raise exception` — a reused key for a genuinely different
   request is a caller bug or a replay attack, and must never be reported as
   a silent success for the *new* amount. **This check must run before the
   balance read below**, not after: a genuine retry arrives once the
   original request's own insert has already reduced the balance, so
   checking balance first would make a legitimate retry fail as
   `insufficient_balance`.
4. Resolve the restaurant's redemption value as of now
   (`restaurant_loyalty_configs`, `effective_from <= now()`, `ENG-007`'s
   read). None → `'not_enrolled'` (AC6).
5. Confirm `p_platform_customer_id` exists in `platform_customers`. Missing →
   `'invalid_code'` (AC3) — checked explicitly rather than left to the
   table's own foreign key, which would otherwise surface as a raw
   constraint-violation error instead of this function's own clean sentinel
   contract.
6. Sum `points` for `(p_platform_customer_id, p_restaurant_id)`. Requested
   `p_points` exceeds it → `'insufficient_balance'`, no insert (AC5).
7. Insert one row: `points = -p_points`, `source = 'redemption'`, `amount =
   p_points * v_rate`, `rate_applied = v_rate`, `earned_at = now()`,
   `created_by = p_created_by`, `idempotency_key = p_idempotency_key`,
   `order_id = null`, `fulfillment_reason = null`. Return `'redeemed'`
   (AC4, AC7).

**RLS:** unchanged — `loyalty_ledger_entries` stays deny-by-default,
service-role only. This function is the only new way in.

## Alternatives considered

- **A stored, revocable code (a new table mapping an opaque token to
  `platform_customer_id`) instead of reusing `platform_customers.id`
  directly.** Rejected — see `ADR-022`. Nothing in the approved PRD asks for
  rotation or per-code revocation; the G1 answer explicitly carried the
  no-expiry default forward as a default, not an open question.
- **An HMAC-derived opaque token, stateless like the chosen option but not
  the raw internal id.** Rejected — see `ADR-022`. AC4's restaurant-scoping
  guarantee comes from `(platform_customer_id, restaurant_id)`-scoped
  queries, not from the code's own format; a derived token buys indirection
  nothing here needs, at the cost of a secret to manage.
- **Checking the balance before the idempotency key.** Rejected — explained
  in Interfaces: a legitimate retry would read a balance the original
  request already reduced and incorrectly bounce as `insufficient_balance`.
  The correctness of retries depends on this specific ordering, not just on
  the key existing at all.
- **One advisory lock per restaurant (`ENG-007`'s own granularity) instead
  of per `(diner, restaurant)`.** Rejected — would serialize every diner's
  redemption at a busy restaurant behind one lock for no correctness
  benefit; the only race that actually needs closing is two writes touching
  the *same* diner's balance at the *same* restaurant.
- **A dedicated new edge function for redemption, instead of a `brand-portal`
  action.** Rejected — same reasoning `ENG-027`/`ENG-007` already used for
  their own new actions: `brand-portal` already has `requireRestaurantAccess`
  and this concern's existing home (`loyalty.ts`); a new function would
  duplicate that machinery for a caller that needs exactly the same access
  model as its two siblings.

## One-way doors

**None escalated.** The one decision shaped like a one-way door here — the
diner code's format, and by extension whether it can ever be individually
revoked — was already decided at this ticket's own G1: the PRD named it
explicitly ("the architect's call... may be reasonable to defer") and the
approver's silence on it was pre-registered by the G1 item itself to mean
accepting the deferred default (`decision-journal.md`, 2026-09-08 row). This
design implements that default (`ADR-022`); it does not reopen it. Nothing
else here introduces a new datastore, a new vendor, an auth-model change, or
a public contract — no frontend or external caller exists for this ticket
either, same "invisible until wired in" position every prior ticket in this
sequence has been in.

## Risks

- **The bearer-credential risk is unchanged by this design, not solved by
  it** (carried from the PRD). An opaque derived token would carry the
  identical exposure, since the point of failure is *possession* of the
  value, not its format — see `ADR-022`. Still deferred on the same
  reasoning the PRD itself offered: a restaurant staff member is physically
  present for every redemption today.
- **A caller that never supplies an `idempotency_key` gets no server-side
  safety net.** Deliberate, not an oversight — `engineering-standards.md`
  places that responsibility on the caller, and a synthesized key on the
  server's side (e.g. derived from request contents) would silently paper
  over a distinct bug (a client that can't tell "retry" from "new request"
  apart) rather than surfacing it as the `400` it already gets today.
- **`amount = points * redemption_value_per_point` rounds to `numeric(10,2)`
  (cents) at insert.** At real-world point values this is immaterial;
  worth naming so a future reader doesn't mistake deterministic rounding for
  a bug.
- **`loyalty_ledger_entries` still has no database-level protection against
  `UPDATE`/`DELETE` by a future `service_role` code path** (open proposal,
  `principal-engineer`, 2026-09-07 — found on this same table before this
  ticket existed). This design adds a second write path to that same table
  rather than the first, which strengthens the case for that proposal but
  isn't this ticket's own scope to fix — named, not fixed, same as the
  `500`-vs-"403-shaped" note above.
- **A 36-character UUID is impractical to hand-type.** Out of this ticket's
  own scope (no frontend, no image rendering, per the whole sequence's
  deferral), but worth naming for whoever eventually builds the consuming
  frontend: this value reads as scan-first (an actual QR/barcode rendering
  of the raw code), and a shorter operator-facing fallback, if ever wanted,
  is a presentation-layer decision layered on top of this value, not a
  reason to mint a second identifier now.

## Rollout

Additive only: three widened check constraints (each strictly adding a
third, previously-impossible arm — no existing `online_order`/`dine_in` row
or write path is affected), one new nullable column, one new function. No
existing table is altered destructively and no existing caller's behavior
changes. Deploy order matches `ENG-048`/`ENG-049`'s own precedent: this
migration lands before `brand-portal`'s new `redeem_points` case deploys.
Until a frontend calls it (none does yet, per this whole sequence's own
non-goal), the new action is reachable only by an authenticated caller with
real restaurant access deliberately exercising it — same "invisible until
wired in" position `record_dine_in_earn`/`get_loyalty_balance` shipped in.
Rollback: drop the new function, drop the `idempotency_key` column and its
constraint, and restore the three widened checks to their prior two-arm
form — safe any time before a frontend ticket starts calling `redeem_points`,
same caveat `ENG-027`'s own migration plan recorded for its columns.

## Out of scope

Per the PRD's own non-goals: any frontend or QR image rendering in any repo;
admin/support surfaces and manual ledger correction (ticket 5); migrating
Walletly balances; any change to how points are earned; point expiry,
pooling, or cross-restaurant balances; rate-limiting or fraud detection
beyond the restaurant-scoping itself; rotating or expiring the diner's code.
This design also does not add a code-based variant of `get_loyalty_balance`
(no acceptance criterion asks for one — `redeem_points`'s own response
already carries the post-redemption balance) and does not touch the
already-flagged, unrelated `loyalty_ledger_entries` UPDATE/DELETE-revocation
gap (Risks).
