---
id: ADR-017
title: "`outgoing-communications`' `systemTriggered` gate reuses `ADR-016`'s service-role-bearer mechanism, as its own per-function file, not a shared one"
project: aiorders-api
ticket: ENG-036
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-017: `outgoing-communications`' `systemTriggered` gate reuses `ADR-016`'s service-role-bearer mechanism, as its own per-function file, not a shared one

## Context

`ENG-036`'s PRD leaves the mechanism open, the same way `ENG-035`'s did:
"the same mechanism may transfer directly — the design step confirms this
against this function's actual callers rather than assuming it." `ADR-016`'s
own Review trigger asks for the two tickets to be reconciled "so this
project ends up with one system-trust convention rather than two."

Unlike `ENG-035`, where the legitimate caller was an untracked DB trigger,
this function's callers are all HTTP call sites this session could read in
full: grepping `outgoing-communications` across all five of this instance's
registered repos (not `aiorders-api` alone) found three callers that set
`systemTriggered: true` — `autopilot/marketing/utils.ts`'s
`scheduleWithQStash` and `sendViaOutgoingComms` (both `aiorders-api`), and
`aiorders-admin-hub`'s `cloudflare-workers/queue-consumer/index.ts` — and
three that don't (forwarded or ambient user sessions, unaffected either way).
All three `systemTriggered: true` callers already send
`Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}` today, confirmed by
reading each call site directly.

A second, separate question this ADR also settles: `_shared/` already holds
genuinely cross-function code in this repo (`restaurantAccess.ts`, per
`ADR-015`; `apiKeys.ts`) — so extracting the gate there, once, instead of
`ADR-016` and this ticket each writing their own copy, is a real option, not
a hypothetical.

## Decision

The `systemTriggered` branch in `outgoing-communications/index.ts` requires
`Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}`, checked in a new
`outgoing-communications/auth.ts` — the same credential, the same comparison,
and the same function signature `ADR-016` used for `autopilot`, but its own
file, not an import from `_shared/` or from `autopilot/marketing/`.

## Alternatives

| Option | Why not |
|---|---|
| Extract `authorizeSystemTrigger` into `_shared/`, imported by both `autopilot` and `outgoing-communications` | `ADR-016`'s own file doesn't exist in the tree yet — `ENG-035` is still `designed`, not `building` — so there is nothing to import from today. Doing this now would make `ENG-036`'s build depend on `ENG-035`'s branch for a ~20-line, zero-behavioral-cost duplicate, coupling two independently-shippable P0 security fixes for a marginal DRY win. `_shared/restaurantAccess.ts` is a substantially larger, genuinely shared lookup — not a precedent for sharing every small check. |
| A new dedicated secret, or a distinct secret per caller | Three live callers across two repos (`aiorders-api`, `aiorders-admin-hub`) would need coordinated reconfiguration this session cannot make or verify — against one header all three already send correctly today, per the caller table in the design doc. |
| Keep this function's own 400-via-catch-all for the new gate too | Would leave two different "denied" shapes for the same conceptual failure across the project's two `systemTriggered` gates, the opposite of what `ADR-016`'s Review trigger asked for. No caller (all six read in full) branches on status code, so there is no functional cost to preferring 401 here — named as a deliberate, narrow inconsistency with this same function's *other*, untouched auth path, not left implicit. |

## Consequences

**Accepted:** the codebase now has two files (`autopilot/marketing/auth.ts`,
once `ENG-035` builds, and `outgoing-communications/auth.ts`) implementing
the identical ~20-line check. A future pass may consolidate them into
`_shared/` once both exist — filed as an observation, not a proposal, since
nothing is lost by leaving two small identical files as-is indefinitely.

**Gained:** `ENG-036` ships independently of `ENG-035`'s own build order —
neither ticket's branch depends on the other's — while still converging on
the one system-trust convention `ADR-016`'s Review trigger asked for (same
credential, same comparison, same signature, same 401 shape).

**Reversibility:** cheap in both directions — extracting to `_shared/` later
is a pure refactor (move the function, update two imports, delete two
files), and swapping the compared credential (to a dedicated secret, if ever
provisioned) is a one-line change in each copy independently.

## Review trigger

If a third function ever needs this same check, extract to `_shared/` at
that point rather than writing a third copy — three is the line this
project already draws elsewhere (`eng_build_loop.md`'s own "third exception
of the same kind" rule), not a rule this ADR invents fresh.
