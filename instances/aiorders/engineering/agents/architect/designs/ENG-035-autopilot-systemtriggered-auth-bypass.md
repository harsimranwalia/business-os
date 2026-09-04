---
ticket: ENG-035
project: aiorders-api
author: architect
created: 2026-09-03
adrs: [ADR-016]
one_way_doors: []
touches_data: false
touches_models: false
---

# `autopilot`'s system-triggered marketing branch skips authentication — technical design

## Approach

`index.ts`'s `systemTriggered` branch needs a real trust check before it calls
`handleMarketing`. The check is extracted into a new file,
`autopilot/marketing/auth.ts`, exporting one function —
`authorizeSystemTrigger(req, responseHeaders)` — for the same reason
`ENG-030`'s `analytics/auth.ts` was extracted rather than inlined: `index.ts`
calls `serve(...)` at module scope, so importing it for a test starts a
listener (confirmed against every existing `*.test.ts` in this repo — none
imports a `serve`-wrapping `index.ts`). AC4 needs a regression test per
marketing action; that test can only exist if the gate is importable on its
own.

The check itself: the request's `Authorization` header must equal
`Bearer ${SUPABASE_SERVICE_ROLE_KEY}` — a secret this function already reads
from `Deno.env` to build its own Supabase client, never exposed to any
client anywhere in this codebase. **Why this value and not a new secret or
the existing `SB_PUBLISHABLE_KEY`: `ADR-016`.** In short — this repo's own
migration history shows two different conventions for a Postgres-side caller
invoking an edge function: a row-level Database Webhook
(`supabase_functions.http_request(...)`, confirmed via
`20260807000004_fix_restaurant_website_cache_invalidation_trigger.sql` to
carry an `Authorization` header copied from a sibling trigger) and a
headerless scheduled job (`20260217000001_platform_analytics_cron.sql`'s
`pg_cron` + raw `net.http_post`, `Content-Type` only). `welcome_offer`'s own
trigger fires on a row-level event — `welcome.ts`'s own comment: "Called by
database trigger when a new customer is created" — matching the
Database-Webhook group's shape, not the headerless cron group's. Supabase
Studio's own "send to Edge Function" webhook preset defaults to attaching
`Authorization: Bearer <service_role_key>`, consistent with what the
migration confirms the sibling triggers actually carry. This is the
best-supported guess available without live project access, not a certainty
— see Risks.

No `SupabaseClient` or database lookup is needed for this check (unlike
`ENG-029`/`ENG-030`'s ownership checks) — it is a pure header comparison,
which makes the regression test trivial with zero mocking.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/functions/autopilot/marketing/auth.ts` | new — `authorizeSystemTrigger(req, responseHeaders)`: reads the `Authorization` header, compares it to `` `Bearer ${Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')}` ``, logs a distinct, greppable message and returns a 401 `Response` on any mismatch or missing header; returns `null` on match. | backend |
| `supabase/functions/autopilot/index.ts` | modify — import `authorizeSystemTrigger`; inside the existing `if (systemTriggered && marketingActions.includes(action))` block, call the gate first and return its `Response` if non-null, before the `console.log`/`handleMarketing` call. No other line changes — the `apikey`/template/log branches below are untouched. | backend |
| `supabase/functions/autopilot/marketing/auth.test.ts` | new — `Deno.test` per case in the Interfaces table below, run for all three marketing actions per AC3 | backend |

## Interfaces

```ts
export function authorizeSystemTrigger(
  req: Request,
  responseHeaders: Record<string, string>,
): Response | null
```

| Case | Result |
|---|---|
| No `Authorization` header | 401 `{error: 'System credential required', source: 'autopilot-marketing'}`; `console.error('[autopilot] systemTriggered denied: missing Authorization header')` |
| `Authorization` present but not `Bearer ${SUPABASE_SERVICE_ROLE_KEY}` | same 401 body; `console.error('[autopilot] systemTriggered denied: invalid system credential')` |
| `Authorization` === `` `Bearer ${SUPABASE_SERVICE_ROLE_KEY}` `` | `null` — `index.ts` proceeds to `handleMarketing`, behavior unchanged (AC2) |

`index.ts`'s only new lines, inside the existing branch:

```ts
if (systemTriggered && marketingActions.includes(action)) {
  const denied = authorizeSystemTrigger(req, responseHeaders);
  if (denied) return denied;
  console.log(`Autopilot system-triggered action: ${action}`);
  const result = await handleMarketing(action, payload, supabase);
  return new Response(JSON.stringify(result), { status: 200, headers: responseHeaders });
}
```

Covers `welcome_offer`, `birthday_offer`, and `winback_offer` in one place —
satisfies AC3 (stubs gated the same way) without touching either stub file.

## Alternatives considered

1. **Reorder only** — move the `systemTriggered` branch below the existing
   `apikey` check, so a system call must present `SB_PUBLISHABLE_KEY` like
   every other action. The PRD's own second-named option, and the smallest
   possible diff. Rejected: that key is a *publishable* key by name and
   design — embedded client-side in all four frontends, so it is not secret
   from a moderately capable caller. The PRD rates this bug worse than
   `ENG-022`/`ENG-029`/`ENG-030` specifically because those three "require at
   least the committed publishable key"; matching this ticket's bar to
   theirs would erase the distinction the PRD itself draws. Full reasoning:
   `ADR-016`.
2. **A new dedicated secret**, with the DB trigger reconfigured to send it.
   Rejected — this session has no DB/CLI/MCP access to make or verify that
   reconfiguration, so it would guarantee breakage until a human does it by
   hand, versus the chosen approach's reasoned chance of already matching
   what the trigger sends today. `ADR-016`.
3. **Timing-safe string comparison** for the secret check. Rejected —
   inconsistent with this same function's own existing `apikey` check (plain
   `!==`), not a standard this codebase holds itself to anywhere else, and
   edge-function network jitter makes the attack impractical regardless.

## One-way doors

None. An additive header check ahead of existing, unchanged handler code — no
schema change, no new datastore or vendor, no contract change visible to the
legitimate caller if it already sends this header (Interfaces table, success
row). Decided here rather than escalated.

## Risks

- **Central, load-bearing risk: whether the live `welcome_offer` trigger
  actually sends `Authorization: Bearer <service_role_key>` cannot be
  confirmed from this repo** (no DB/CLI/MCP access this session; the
  trigger itself is not tracked in any migration — see `ADR-016`'s Context).
  The reasoning above is the best available evidence, not a certainty. This
  exact failure shape — a newly added header check silently rejecting a
  legitimate trigger — already happened once in this codebase:
  `20260807000004_fix_restaurant_website_cache_invalidation_trigger.sql`'s
  own commit message describes `get-brand-website` rejecting every
  invalidation call with 401 because its trigger had no `Authorization`
  header, "meaning edits to `restaurant_website` never purged the brand's KV
  cache... until the TTL expired" — a silent failure nobody caught until
  someone went looking. Mitigation: the denial path logs a distinct,
  greppable message (Interfaces table) specifically so a real trigger
  starting to fail is visible in Supabase function logs rather than only in
  a customer's absent welcome email; Rollout below adds a mandatory manual
  post-deploy check, since an automated test can only mock the header, never
  prove what the live trigger sends.
- **`outgoing-communications` has the identical-shaped bug** — its own
  `systemTriggered` check skips *all* authentication, for *any* `actor`
  (including `admin`), not just marketing. Confirmed live and reachable by
  reading `outgoing-communications/index.ts` and its `actors/*.ts` handlers
  in full (required reading for this design, since `marketing/utils.ts`
  calls this function directly) — `consumers.ts`'s `sendOrderFeedbackRequest`
  and `welcome_offer`/`every_order`/`first_order`, and `brands.ts`'s campaign
  notifications, are real, non-stub sends reachable the same way `ENG-035`'s
  own `welcome_offer` is. Filed separately as `ENG-036`, same reasoning
  `ENG-029`'s own design pass used to file `ENG-035` itself — a different
  file, a non-overlapping diff, out of scope for this ticket's own PRD
  (Non-goals).
- **No evidence of actual exploitation** (carried from the PRD). Customer
  notification is the approver/security's call, already surfaced via the P0
  incident notice.

## Rollout

Straight, no flag, no backfill — a logic-only addition ahead of existing,
unchanged handler code; no schema change, no migration. Branch → PR → gates
→ human merge (`aiorders-api` is L1) → deploy. Qualifies for
`definition-of-done.md`'s P0-hotfix exception to the release window, same as
`ENG-022`/`ENG-029`/`ENG-030`. Rollback: revert the merge commit — no
migration, so a revert fully restores prior (broken) behavior with nothing
further to clean up.

**Mandatory manual post-deploy verification (AC2), named explicitly because
automation cannot reach it:** an automated test can only mock the
`Authorization` header, never prove what the live database trigger actually
sends. After deploy, check Supabase function logs for `autopilot` in the
following welcome-offer window for the new `[autopilot] systemTriggered
denied` line; its absence on a real new-customer signup is the confirmation
AC2 holds. If it appears against a real trigger fire, this is the Risks
section's named failure materializing — revert immediately per the Review
trigger in `ADR-016`, don't leave it broken while investigating.

## Out of scope

- `birthday_offer`/`winback_offer`'s own unimplemented logic (PRD non-goal) —
  gated the same way, not implemented.
- `outgoing-communications`' identical-shaped check — filed as `ENG-036`.
- `ENG-029`'s own 8 template/log actions — separate ticket, already in
  flight, unrelated auth model.
- Reconciling the Studio-Database-Webhook and headerless-`pg_cron` trigger
  conventions across the wider migration history, or auditing whether
  `platform-analytics-hourly`'s own lack of any header is itself a problem —
  noticed while researching this design's own trigger-convention question,
  not required by this PRD; one-line observation filed instead of expanded
  into scope here.
