---
ticket: ENG-050
project: aiorders-api
author: architect
created: 2026-09-07
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Two production RPC functions grant `EXECUTE` to `anon`/`authenticated` — technical design

## Approach

Apply the exact statement already proven twice today on this project
(`ENG-048` round 2, `agents/security/reviews/ENG-048.md`): a new migration that
names `anon`/`authenticated` explicitly in the `REVOKE`, not `FROM PUBLIC`
alone — confirmed insufficient on this project's own `pg_default_acl` setup,
independently, twice. One new migration, both functions fixed together — same
root cause, same finding, same fix shape, no reason to split an S ticket into
two files or two PRs. Neither function's own body, signature, or return shape
changes; the exposure is the grant, not the aggregation.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/migrations/20260907140000_revoke_anon_authenticated_execute_platform_analytics_and_acquisition_breakdown.sql` | new | database |

## Data

Hand-off per `skills/schema-change/SKILL.md` — intent and constraints only,
`database` owns the migration itself.

Intent: close `pg_default_acl`'s function-object default grant (`EXECUTE` to
`anon`/`authenticated`/`service_role` at function-creation time on this
project's `public` schema — confirmed mechanism, `ENG-048` round 2 and this
ticket's own PRD) on two **existing** functions:
`calculate_platform_analytics()` and
`public.get_acquisition_breakdown(uuid, timestamptz, timestamptz)`. Cannot
edit the two original migration files — both already applied to production;
this is a new, additive migration, timestamped after the latest one on disk
(`20260907130000_...`).

Proven statement (PRD's own "Proposed change", identical to `ENG-048`'s
round-2 fix):

```sql
revoke execute on function public.calculate_platform_analytics() from public, anon, authenticated;
grant execute on function public.calculate_platform_analytics() to service_role;

revoke execute on function public.get_acquisition_breakdown(uuid, timestamptz, timestamptz) from public, anon, authenticated;
grant execute on function public.get_acquisition_breakdown(uuid, timestamptz, timestamptz) to service_role;
```

No schema change — no table, column, or index — so no volume/query-pattern/
lock concern: this is a catalog-only privilege change, near-instant regardless
of table size, the same reasoning `ENG-048`'s own Runtime and locks section
already established for this exact class of statement.

## Interfaces

No interface change. Both functions' signatures and return shapes are
byte-for-byte unchanged. The only externally-visible change: an
`anon`/`authenticated` caller invoking either function directly now receives
Postgres's own `permission denied for function {name}` error instead of a
served response — that response *is* the fix, not a side effect of it.

## Alternatives considered

1. **`REVOKE ... FROM PUBLIC` alone**, no explicit `anon`/`authenticated`.
   Rejected — proven insufficient on this exact project, twice, today
   (`ENG-048` round 2; this ticket's own PRD independently reconfirmed it
   against production). This project's `pg_default_acl` names `anon`,
   `authenticated`, and `service_role` directly — a separate mechanism a bare
   `FROM PUBLIC` revoke doesn't touch.
2. **Fix `pg_default_acl` itself**
   (`ALTER DEFAULT PRIVILEGES ... REVOKE EXECUTE ON FUNCTIONS FROM anon,
   authenticated`), closing the root cause so every future function is safe
   by default. Rejected for *this* ticket: it's a standing, project-wide
   default-privilege change affecting every migration from here on —
   materially bigger and riskier than a P0 hotfix on two confirmed-live
   functions should carry, and exactly the systemic piece the PRD leaves open
   as a separate, sized follow-up (see Out of scope) rather than folded in
   here.
3. **An application-layer check** in the calling edge function instead of a
   database-level grant fix. Rejected — doesn't close the actual hole
   (`supabase.rpc(...)` reaches Postgres directly, bypassing any
   edge-function-side gate entirely), and contradicts this project's own
   established principle that access constraints belong in the database, not
   a wrapper (`ENG-048`'s own security review, OWASP A05).

## One-way doors

None. A privilege correction on two existing functions, reversible by
re-granting (see Rollback) — no schema change, no new datastore or vendor, no
contract change visible to either confirmed legitimate caller (both
`service_role`, re-verified this pass, see Risks). Decided here, not
escalated.

## Risks

- **Caller completeness re-verified independently, not taken on the PRD's own
  word.** Grepped all five registered repos (`aiorders-api`,
  `aiorders-admin-hub`, `config-site-builder`, `restaurant-marketplace`,
  `restaurant-portal`) for both function names. Exactly the two
  already-confirmed `service_role` callers exist
  (`platform-analytics/index.ts`, `brand-portal/acquisition.ts`, both
  `aiorders-api`); `aiorders-admin-hub` carries only generated type
  definitions (`src/integrations/supabase/types.ts`), never an actual call;
  the other three repos have zero references to either name. No hidden
  anon-key caller this fix would break.
- **The other ~10 functions in this repo likely share the same gap**
  (`agents/eng-manager/proposals.md`, 2026-09-07, principal-engineer —
  corrected in place this pass, see Out of scope). Deliberately not addressed
  here: security confirmed *these two* live-exploitable in production today;
  the rest are an unconfirmed, separate concern this P0 ticket's own scope
  (and its "an hour or two" estimate) was never meant to cover. Named plainly
  rather than silently narrowed — tracked as a sized follow-up, not dropped.
- **No evidence of actual exploitation** (carried from the PRD) — this closes
  a confirmed live *capability*, not a confirmed breach.

## Rollout

Straight, no flag, no backfill — a privilege-only migration ahead of
unchanged function bodies. Branch → PR → gates (including `database`'s own
migration doc and review) → human merge (`aiorders-api` is L1) → deploy.
Qualifies for `definition-of-done.md`'s P0-hotfix exception to the release
window, same as `ENG-022`/`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`.

**Verification, carried from the PRD's own AC5 — not a catalog read alone:**
apply against a disposable `supabase/postgres:15.8.1.073` replica (matching
every prior verification on this project), confirm `has_function_privilege`
is `false` for `anon`/`authenticated` and `true` for `service_role` on both
functions, then actually attempt `set role anon; select {function}(...)` and
confirm a real `permission denied` — the same method `ENG-048`'s own security
gate used a fourth independent time rather than trust three prior accounts.

**Rollback** (re-opens the exposure this migration closes — emergency use
only, e.g. if the fix is later found to break a caller this pass's grep
missed):

```sql
grant execute on function public.calculate_platform_analytics() to anon, authenticated;
grant execute on function public.get_acquisition_breakdown(uuid, timestamptz, timestamptz) to anon, authenticated;
```

## Out of scope

- **The project-wide sweep of this repo's other ~10 functions for the same
  missing-explicit-`REVOKE` pattern.** The PRD's own Non-goals leaves this as
  the architect's design-time call; sized here: **not** part of this P0
  ticket — scope stays the two functions security confirmed live-exploitable,
  matching this ticket's own AC1–5, Outcome, and S/"an hour or two" estimate.
  A repo-wide audit (confirming which of ~12 functions are meant to be public
  vs. internal-only, one by one) is a materially different, larger piece of
  work. Sized as its own follow-up in `agents/eng-manager/proposals.md`
  (2026-09-07 principal-engineer row, corrected in place this pass) rather
  than folded in here — per `eng_build_loop.md` step 3, a *suspected*,
  unconfirmed pattern on the remaining functions doesn't qualify for the P0
  carve-out the way these two, security-confirmed-live, do.
- **`pg_default_acl` itself** — see Alternatives #2. A standing
  default-privilege fix is the natural companion to the wider sweep above,
  not this hotfix; whoever picks up that follow-up should size the two
  together.
- Any change to either function's own query logic or return shape — the
  exposure is the grant, not the aggregation (PRD's own Non-goals).
- The security gate's own A01 checklist gap (verifying function-level grants
  independently of application-layer wrappers) — already named not this
  ticket's to fix, per the PRD.
