---
id: ADR-005
title: url-shortener trusts a per-action restaurant-scoped check, not only platform-admin, for one new action
project: aiorders-api
ticket: ENG-014
status: accepted
decided_by: architect
date: 2026-08-31
supersedes:
superseded_by:
---

# ADR-005: `url-shortener` trusts a per-action restaurant-scoped check, not only platform-admin, for one new action

## Context

`url-shortener`'s dispatcher enforces one blanket rule before its action
`switch`: every action requires `verifyAdminAccess` (`profile.role ===
'admin'` exactly), with a single existing carve-out for the fully public
`redirect` action (no auth at all, called by the Cloudflare Worker). `ENG-014`
needs a restaurant or brand manager — never a platform admin — to get or
create their own restaurant's QR code from the brand portal, so at least one
action on this function must now accept a caller who is not an admin.

## Decision

Add exactly one new action, `get_or_create_restaurant_qr`, that still requires
a real authenticated user (Bearer JWT, same as every other action) but checks
`verifyRestaurantAccess(restaurant_id, ...)` — from `_shared/restaurantAccess.ts`,
already duplicated there for the same reason (`api-key-auth` needing the same
check without cross-importing between independently-deployed functions) —
instead of `verifyAdminAccess`. Everything the action can read or write is
scoped to a `destination_url` it computes itself from that one restaurant's
own `website` column, never one supplied by the caller. Every other action on
this function keeps the existing admin-only gate, unchanged.

## Alternatives

| Option | Why not |
|---|---|
| Loosen the blanket `verifyAdminAccess` check for all actions | Every other action (`list`, `update`, `delete`, `analytics`) would then need its own re-scoping to avoid a cross-tenant leak — `list` alone returns every restaurant's shortened-URL rows. Far more surface than this ticket needs. |
| Accept a client-supplied `destination_url` on the new action | Would let a caller who passes `verifyRestaurantAccess` for their own restaurant still read or create a shortened link for an unrelated destination — the access check would gate the action but not what the action actually does. |

## Consequences

**Accepted:** `url-shortener` now has two trust levels instead of one —
platform-admin for six actions, restaurant-scoped for one. A future engineer
adding an action to this file needs to pick the right check deliberately
rather than assuming the file-wide admin gate still covers everything.

**Gained:** the brand portal gets a real, minimally-scoped write path onto
shared backend infrastructure without touching that infrastructure's existing
trust boundary for anything already built on it (the admin console).

**Reversibility:** removing the new action, or tightening it further, is a
code change with no data migration — the `shortened_urls` rows it creates are
indistinguishable from ones the admin console already creates today.

## Review trigger

If a second non-admin action is ever added to this function, revisit whether
the per-action pattern still reads cleanly or whether the file needs an
explicit action-to-required-check table instead of two ad hoc carve-outs
(`redirect`, `get_or_create_restaurant_qr`).
