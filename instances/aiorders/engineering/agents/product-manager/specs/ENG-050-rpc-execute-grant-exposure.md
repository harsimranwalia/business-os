---
ticket: ENG-050
project: aiorders-api
status: draft
size: S
author: security
created: 2026-09-07
decided:
---

# Two production RPC functions grant `EXECUTE` to `anon`/`authenticated` — unauthenticated platform-analytics and acquisition-breakdown exposure

**Auto-approved type (`security`) — no readback, no G1.** Per
`skills/request-readback/SKILL.md`, agent-originated findings with their own
evidence skip the readback. Per
`agents/eng-manager/config/definition-of-done.md`'s ticket-states table,
`security`-typed tickets auto-skip `awaiting-scope` (G1). This PRD is
intentionally short — the evidence below, already independently confirmed
twice by security, stands in for a Problem/Users narrative.

**Filed directly, not via `agents/eng-manager/proposals.md`.** Per
`schedules/eng_build_loop.md` step 3's carve-out ("A P0 on a registered
project that is not on the internal lane... becomes a ticket immediately, no
proposal and no G1") and `templates/ticket.md`'s `source:` field note (a P0
on a non-internal project "keeps its agent source"). `aiorders-api` is
registered `L1`, not internal (`config/projects.md`) — "Highest blast radius
of the set."

**Discovered as a byproduct**, not an assigned sweep. `agents/eng-manager/
proposals.md`'s 2026-09-07 row (principal-engineer, found while reviewing
`ENG-048` round 1's own `credit_order_if_eligible` grant gap, then checked
project-wide) named these two functions as carrying the identical gap, live
— but explicitly left "is this actually exploitable enough to matter" as
security's own call, not re-derived by that finding. Security made that call
during `ENG-048`'s own security gate (`agents/security/reviews/ENG-048.md`,
`agents/security/notebook/2026-09-07-findings.md`): confirmed live, twice,
independently — once by direct catalog query against the actual production
project (`bmnmnejwdxbcqinqkwko`), once again by reproducing the mechanism
from scratch on a disposable replica — and filed to
`agents/eng-manager/inbox/2026-09-07-security-p0-rpc-execute-grant-exposure.md`.

## Problem (the evidence)

Two Postgres RPC functions in this project are directly, unauthenticatedly
callable via `supabase.rpc(...)` today:

- `calculate_platform_analytics()` —
  `supabase/migrations/20260217000001_platform_analytics_cron.sql`. Returns
  per-brand/per-restaurant/global order counts and order-value totals via
  `GROUPING SETS`. Intended caller: the `platform-analytics` edge function's
  hourly `pg_cron` job — confirmed directly, this pass, by reading the
  function itself: `platform-analytics/index.ts:53`
  (`supabase.rpc('calculate_platform_analytics')`) on a client built from
  `SUPABASE_SERVICE_ROLE_KEY` (`index.ts:230,236`).
- `get_acquisition_breakdown(p_restaurant_id uuid, p_from timestamptz, p_to
  timestamptz)` —
  `supabase/migrations/20260905190000_add_acquisition_breakdown_rpc.sql`.
  Returns per-channel customer/order/revenue aggregates for one restaurant.
  Intended caller: `brand-portal/acquisition.ts`'s `handleAcquisition`,
  which runs its own `verifyRestaurantAccess` check first — but only inside
  the edge function, itself built from `SUPABASE_SERVICE_ROLE_KEY` —
  confirmed directly, this pass: `brand-portal/index.ts:31,41` (client
  construction), `:192` (`handleAcquisition` called with that client).

Both migrations grant only `GRANT EXECUTE ON FUNCTION ... TO service_role`,
and neither one — nor any other migration in this repo's history — ever
revokes the Postgres default. Confirmed directly in both migration files
(read in full, this pass, against the department worktree): no `revoke`
statement of any kind exists for either function anywhere in
`supabase/migrations/`.

**Root cause, confirmed independently twice today** (once against this
exact production project's live catalog, once by reproducing the mechanism
from scratch on a disposable `supabase/postgres:15.8.1.073` replica —
`agents/security/reviews/ENG-048.md`): this project's `public` schema
carries a `pg_default_acl` entry (grantor `postgres`, object type `f`)
naming `anon`/`authenticated`/`service_role` directly with `EXECUTE` at
function-creation time. This is separate from the `PUBLIC` pseudo-role — a
bare `GRANT ... TO service_role` does nothing to restrict the other two
named roles, and `REVOKE ... FROM PUBLIC` alone does not close it either;
both roles must be named explicitly in the `REVOKE`.

Net effect: **any caller holding this project's public anon key —
intentionally public, shipped in every frontend bundle by Supabase's own
design — can call either function directly, today, in production,
bypassing both functions' own application-layer authorization entirely**
(the `verifyRestaurantAccess` check in `brand-portal/acquisition.ts`, and
the fact that `calculate_platform_analytics` is meant to be cron-only). No
exploit tooling needed, no valid login required.

## Impact — who is affected and how

Per `agents/eng-manager/config/security-baseline.md` ("An active security
incident (leaked credential, **live exploit**, exposed data) — P0") and
`agents/security/agent.md`'s own `interrupt_rule` ("P0 only — active
incident, leaked credential, or exposed data (via the EM)"): a confirmed,
reproducible, zero-authentication ability to invoke a privileged production
function is a live exploit on its own terms, independent of how sensitive
the returned data is. This was confirmed twice, by two different methods,
against the real production project — not a theoretical read.

**Data classification.** Both functions' own output is aggregate business
data — order/customer counts, order value, revenue, acquisition/channel
figures — no PII, no credentials, no payment-instrument data. Per
`security-baseline.md`'s classification table, revenue figures fall under
**Confidential** ("Client names, contracts, revenue, pipeline"), not
Internal as the originating finding card characterized it — noted here as a
correction, not left to stand uncorrected, though it does not change the
outcome: the carve-out and the P0 rating both already turn on the
live-exploit criterion, not on the data tier. `aiorders-api` is registered
"Highest blast radius of the set — shared backend for all four frontends"
(`config/projects.md`).

Rated **P0** — the originating inbox card's own frontmatter read `severity:
P1` while its title, its carve-out citation, and nearly all of its own body
reasoned in P0 terms throughout. This PRD resolves the inconsistency to P0,
matching the carve-out it invokes, security's own notebook entry ("Made
that call this pass... that is the build-loop's own step-3 carve-out"), and
the bar every prior ticket of this exact shape (`ENG-022`, `ENG-029`,
`ENG-030`, `ENG-035`, `ENG-036`) was rated at.

## Proposed change

Behavior, not implementation — the exact statement is already proven twice
today on this project (`ENG-048`'s `credit_order_if_eligible`,
`agents/security/reviews/ENG-048.md`):

```sql
revoke execute on function {name}({arg_types}) from public, anon, authenticated;
grant execute on function {name}({arg_types}) to service_role;
```

applied to both:
- `calculate_platform_analytics()` — no arguments.
- `public.get_acquisition_breakdown(uuid, timestamptz, timestamptz)`.

Naming `anon`/`authenticated` explicitly (not `... from public` alone) is
the operative part — confirmed insufficient otherwise on this project's
`pg_default_acl` setup, twice.

**Scope of a wider sweep is the architect's call at design time**, not
pre-decided here. The originating proposal's own text: "Likely the same gap
on every other function in this repo lacking an explicit `REVOKE`, i.e.
most of them — worth a project-wide sweep, not a two-function patch." At
minimum, the two confirmed-live functions above get the fix; whether this
ticket also runs a full-repo sweep (sizing how many of this repo's ~12
functions are meant to be public vs. internal-only) or a follow-up ticket
does is scoped at design.

## Acceptance criteria

1. `[stated]` Given an unauthenticated caller (the project's public anon
   key only, no session), when they call `calculate_platform_analytics`
   directly via `supabase.rpc(...)`, then the call is denied with a
   permission error, not served.
2. `[stated]` Given the same caller, when they call
   `get_acquisition_breakdown` directly via `supabase.rpc(...)` with any
   arguments, then the call is denied with a permission error, not served —
   closing the direct-RPC bypass regardless of what
   `brand-portal/acquisition.ts`'s own `verifyRestaurantAccess` check does.
3. `[stated]` Given the `platform-analytics` edge function's own hourly
   cron call (`service_role`, confirmed at `platform-analytics/index.ts`
   lines 53/230/236), behavior is unchanged — still returns data, unchanged
   shape.
4. `[stated]` Given `brand-portal/acquisition.ts`'s own call on behalf of a
   verified restaurant owner (`service_role`, confirmed at
   `brand-portal/index.ts` lines 31/41/192), behavior is unchanged — still
   returns data, unchanged shape.
5. `[proposed]` Verification method matches `ENG-048`'s own proven
   approach, not a catalog read alone: apply the fix against a disposable
   `supabase/postgres:15.8.1.073` replica, confirm `has_function_privilege`
   is `false` for `anon`/`authenticated` and `true` for `service_role` on
   both functions, then actually attempt `set role anon; select
   {function}(...)` and confirm a real `permission denied`, not just an
   inferred one.

## Non-goals

- The project-wide sweep of the repo's other ~12 functions for the same
  missing-`REVOKE` pattern — named as in-scope-to-decide above, not
  pre-committed to either way; the architect sizes it at design time.
- Any change to either function's own query logic or return shape — the
  exposure is the grant, not the aggregation.
- The security gate's own A01 checklist gap (verifying function-level
  grants independently of application-layer wrappers) —
  `agents/security/notebook/2026-09-07-findings.md` already named this
  explicitly as "one short of three-strike," not proposed to
  `engineering-standards.md` this pass, and not this ticket's to fix.

## Risks and unknowns

- **No evidence of actual exploitation** — confirmed live vulnerability
  (reachable, reproducible), not a confirmed breach. Customer notification,
  if any, is the approver's/security's call, not this PRD's.
- **Not exhaustively enumerated beyond these two functions** — this finding
  traced exactly the two functions principal-engineer's proposal named; it
  does not re-check the other ~10 functions in the repo (see Non-goals and
  Proposed change).

## Cost

- **Build:** `S` — two functions, statement already proven twice today on
  this exact project, no new data model, no application-code change. Does
  not displace machine-WIP on its own — starts once a slot is free and
  `priority` (approver-only) says to jump the queue, same as
  `ENG-022`/`ENG-029`/`ENG-030`.
- **Run:** $0/month.

## Decision

N/A — `security`-typed tickets auto-skip G1
(`agents/eng-manager/config/definition-of-done.md`). Filed directly per the
P0 carve-out. The approver is notified as an incident, not asked to approve
starting the fix.
