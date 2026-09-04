---
id: ADR-016
title: "`autopilot`'s `systemTriggered` marketing branch authenticates via the service-role key as a bearer credential, not a new secret or the existing publishable key"
project: aiorders-api
ticket: ENG-035
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-016: `autopilot`'s `systemTriggered` marketing branch authenticates via the service-role key as a bearer credential, not a new secret or the existing publishable key

## Context

`ENG-035`'s PRD leaves the mechanism open — "a shared-secret header compared
against a new dedicated env var, routing the trigger through a mechanism that
already carries a verifiable signature, or removing the early-auth-bypass and
giving the marketing actions their own service-level credential check is the
architect's call." Its own Risks section names the real blocker: the
legitimate caller's actual invocation (`welcome.ts`'s own comment: "Called by
database trigger when a new customer is created") is not tracked anywhere in
this repo — no migration defines it, and `supabase/config.toml` carries only a
`project_id`, no per-function `verify_jwt` override — so what the live trigger
actually sends cannot be read from source.

Two confirmed trigger-to-edge-function conventions exist elsewhere in this
repo's own migration history. `20260807000004_fix_restaurant_website_cache_invalidation_trigger.sql`
recreates a row-level webhook using Supabase's own `supabase_functions.http_request(...)`
trigger helper, copying its header set from a sibling `brand_website_cache_invalidation`
trigger — the migration itself `RAISE EXCEPTION`s if that sibling's headers
don't contain `Authorization`, proving the sibling carries one. This is
Supabase Studio's own "Database Webhook → Edge Function" preset shape, which
defaults to `Authorization: Bearer <service_role_key>`. A second, *headerless*
convention also exists (`20260217000001_platform_analytics_cron.sql`'s
`pg_cron` + raw `net.http_post` job — `headers := jsonb_build_object('Content-Type', ...)`
only, no `Authorization` at all) — but that one is a time-based scheduled job,
a structurally different mechanism from a row-level "on insert" trigger.
`welcome_offer`'s own trigger is row-level, matching the Studio-webhook
group's shape, not the headerless cron group's.

## Decision

The `systemTriggered` marketing branch in `autopilot/index.ts` requires
`Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}` before `handleMarketing`
runs (`marketing/auth.ts`'s `authorizeSystemTrigger`). No new secret is
provisioned, and `SB_PUBLISHABLE_KEY` — already known to be embedded in all
four public frontends — is not reused for this gate.

## Alternatives

| Option | Why not |
|---|---|
| Reuse `SB_PUBLISHABLE_KEY` (move the branch below the existing `apikey` check) | Smallest possible diff, but the key is designed to be embedded client-side in all four frontends — not secret from a moderately capable caller. The PRD rates this bug worse than `ENG-022`/`ENG-029`/`ENG-030` specifically because those three need at least this key; matching their bar here would erase that distinction. |
| New dedicated secret (e.g. `AUTOPILOT_SYSTEM_SECRET`) | Requires reconfiguring the live Supabase trigger to send it — an out-of-band change this session has no DB/CLI/MCP access to make or verify, guaranteeing breakage until someone does it by hand, versus a reasoned (not certain) chance the chosen approach already matches what the trigger sends today. |
| Route through a mechanism with a verifiable signature | This project's confirmed trigger convention (Studio's header-based Database Webhook) doesn't sign payloads — nothing to verify against. Switching the trigger to a signing mechanism is a live-project reconfiguration this session cannot make. |

## Consequences

**Accepted:** if the live `welcome_offer` trigger does *not* already send
`Authorization: Bearer <service_role_key>` — unverifiable from this repo —
this fix silently breaks the legitimate welcome-offer flow until someone
notices, the same failure shape `20260807000004`'s own commit message
describes happening to a sibling trigger for an unknown period. Named
plainly in `ENG-035`'s own design Risks, with a mandatory manual post-deploy
verification step as mitigation — not treated as a solved problem here.

**Gained:** no new secret to provision or rotate; the gate reuses a
credential every legitimate internal caller in this Supabase project already
has access to, and that no client has ever been given.

**Reversibility:** cheap — swapping the compared value (to a dedicated
secret, once one is provisioned and the trigger reconfigured) is a one-line
change in `marketing/auth.ts`, no data migration, no contract change visible
to any legitimate external caller.

## Review trigger

If the post-deploy verification (`ENG-035`'s own Rollout step) finds the real
trigger does *not* send this header, roll back to a safe state immediately
(or fast-follow with the dedicated-secret alternative above) rather than
leaving welcome offers silently broken — raise a fresh P0 if that happens,
don't quietly patch over it. Also worth reconciling with whichever mechanism
`ENG-036` (`outgoing-communications`' identical-shaped bug) settles on, so
this project ends up with one system-trust convention rather than two.
