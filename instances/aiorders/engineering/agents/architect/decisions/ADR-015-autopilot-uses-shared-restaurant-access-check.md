---
id: ADR-015
title: "`autopilot`'s ownership check imports `_shared/restaurantAccess.ts`, not `brand-portal/utils.ts`'s"
project: aiorders-api
ticket: ENG-029
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-015: `autopilot`'s ownership check imports `_shared/restaurantAccess.ts`, not `brand-portal/utils.ts`'s

## Context

`ENG-029`'s PRD names `brand-portal/utils.ts`'s `verifyRestaurantAccess` (and
`ENG-022`'s promoted, throwing `requireRestaurantAccess`, "once that ticket
ships") as the likely primitive to reuse, leaving the exact source as "the
architect's call at the design step." `requireRestaurantAccess` exists only on
`ENG-022`'s own unmerged branch (`fix/ENG-022-brand-portal-tenant-isolation`,
confirmed via `git merge-base --is-ancestor` against `origin/main`: not
merged) — not on `main`, where `ENG-029`'s own branch will start from.
Separately, `supabase/functions/_shared/restaurantAccess.ts` already exists on
`main`, exports a `verifyRestaurantAccess` with the identical access rule
(platform-admin bypass, then `brand_managers`, then `restaurant_managers`),
already returns `{hasAccess, error?}` rather than throwing, and its own doc
comment states it exists specifically so a function outside `brand-portal/`
can reuse the check "without importing across function directories" — already
proven in exactly that role by `api-key-auth`.

## Decision

`autopilot`'s new ownership check imports `verifyRestaurantAccess` from
`_shared/restaurantAccess.ts`, not from `brand-portal/utils.ts`.

## Alternatives

| Option | Why not |
|---|---|
| Import `brand-portal/utils.ts`'s `requireRestaurantAccess` (throwing) | Exists only on `ENG-022`'s unmerged branch — would force `ENG-029` to either wait on that merge or duplicate an unmerged rename, for a variant that also doesn't match `autopilot`'s own return-based (never-throw) convention. |
| Import `brand-portal/utils.ts`'s `verifyRestaurantAccess` (return-based, on `main` today) | Works today, but reaches into a sibling function's own `utils.ts` rather than the module built for exactly this cross-directory case — an undocumented pattern next to a documented one that does the same job. |
| Write a new, `autopilot`-local copy of the check | Needless duplication of a primitive that already exists, is already correct, and is already designed to be shared this way. |

## Consequences

**Accepted:** `autopilot` now depends on `_shared/restaurantAccess.ts` staying
stable — already true of `api-key-auth`, so this adds a second consumer to an
existing contract rather than creating a new one.
**Gained:** `ENG-029` ships independently of `ENG-022`'s merge order — no
`depends_on` needed between the two tickets.
**Reversibility:** cheap — a single import source, swappable in one line per
call site if `_shared/restaurantAccess.ts` is ever retired in favor of
`brand-portal/utils.ts`'s version (e.g. once `ENG-022` merges and the two
implementations are reconciled).

## Review trigger

If `brand-portal/utils.ts`'s `verifyRestaurantAccess`/`requireRestaurantAccess`
and `_shared/restaurantAccess.ts`'s copy ever diverge in behavior (they are
two independent implementations of the same rule today, not one shared by
reference), reconcile them into one — worth a proposal once `ENG-022` merges,
not blocking this ticket.
