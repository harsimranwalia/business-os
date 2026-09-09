---
id: ADR-022
title: "Redemption's diner code is `platform_customers.id` itself, not a new opaque or rotatable token"
project: aiorders-api
ticket: ENG-051
status: accepted
decided_by: architect
date: 2026-09-08
supersedes:
superseded_by:
---

# ADR-022: Redemption's diner code is `platform_customers.id` itself, not a new opaque or rotatable token

## Context

`ENG-051`'s PRD leaves the code's shape open at design time: "whether the
diner's code needs to be stored/revocable (a new table) rather than a
stateless derived value — left for the architect to size." It also names the
bearer-credential risk explicitly — "a stable, long-lived code is a bearer
credential... anyone holding it... can trigger a redemption... indistinguishable
from the diner presenting it themself" — and offers that deferring a
mitigation "may be reasonable... given a restaurant staff member is
physically present for every redemption today, the same... shape `ENG-027`
already accepted for dine-in earn." The ticket's own G1 answer pre-registered
silence on this exact question as accepting that deferred default, not as
leaving it open (`decision-journal.md`, 2026-09-08 row).

`platform_customers.id` (`references auth.users(id)`,
`20260828120000_platform_customer_identity.sql`) is already a random UUID,
one per verified phone identity, shared across every restaurant, permanent —
matching AC1/AC2 exactly. It is already known to the diner's own client
(`auth.uid()`, the moment a Supabase session exists) and already independently
`select`-able by its own owner under the live `platform_customers_select_own`
RLS policy. No new issuance write path exists anywhere in this ticket's
design as a result (main design, Approach).

## Decision

The redemption code IS `platform_customers.id`, submitted verbatim as the
`code` field on the new `redeem_points` brand-portal action. No new table, no
derived or signed token, no issuance endpoint.

## Alternatives

| Option | Why not |
|---|---|
| New table mapping an opaque, revocable token to `platform_customer_id` | Buys rotation/per-code revocation, which nothing in the approved PRD asks for — the G1 answer explicitly carried the no-expiry default forward rather than leaving it open. Additive and cheap to introduce later if a real need shows up; choosing the raw id now forecloses nothing. |
| HMAC-derived opaque token (stateless, no new table, but not the raw internal id) | No behavioral gain over the raw id: `ENG-051`'s central requirement (a redemption only ever touches the scanning restaurant's own balance for that diner) is enforced by `(platform_customer_id, restaurant_id)`-scoped queries inside `redeem_points_if_eligible`, not by anything about the code's own format. UUIDv4 is already non-enumerable; a derived token adds a secret to manage and an encode/decode step for indirection nothing here requires. |

## Consequences

**Accepted:** the value that eventually appears on a diner's QR code is also
their Supabase Auth subject id. This does not by itself grant any
authentication capability to whoever holds it — a valid session still
requires a signed JWT, which knowing `auth.uid()` alone cannot produce — so
its only exposure is the redemption capability the PRD already named and
accepted, not a broader account compromise.

**Gained:** issuance costs zero new code, and the value never expires or
rotates by construction — it matches the G1 default exactly rather than
approximating it.

**Reversibility:** cheap in one direction, real in the other. Adding a
stored/revocable token later is a pure addition (a new table, one new
resolution step inside `redeem_points_if_eligible`) that touches nothing
this migration does. Revoking one specific diner's already-issued code
without moving every diner to a new scheme is not possible under this
decision — a single compromised code cannot be individually invalidated
today, only accepted as a live risk, exactly as the PRD's own Risks section
already frames it.

## Review trigger

If a real fraud incident or an operational demand for per-code revocation
shows up once a frontend actually issues these to diners, revisit — the
stored-token alternative above is the concrete fallback, not a redesign.
