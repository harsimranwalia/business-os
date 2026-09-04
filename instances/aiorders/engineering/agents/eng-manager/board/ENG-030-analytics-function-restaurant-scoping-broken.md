---
id: ENG-030
title: "`analytics` edge function has no authentication or authorization at all — cross-tenant revenue/order/customer exposure"
project: aiorders-api
type: security
size: S
time_estimate: a few hours to half a day
time_spent:
time_remaining:
severity: P0
priority:
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: architect
created: 2026-09-03
updated: 2026-09-03
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-030-analytics-function-restaurant-scoping-broken.md
  design: agents/architect/designs/ENG-030-analytics-function-restaurant-scoping-broken.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

`supabase/functions/analytics/index.ts` reads `restaurantId` from the
request body, builds a service-role Supabase client, and calls
`fetchDatabaseAnalytics(supabase, restaurantId)` — no `Authorization` header
read, no `auth.getUser`, no ownership check of any kind, anywhere in the
function. Full evidence, the exact code, and confirmation that the repo's
own `supabase/functions/README.md` lists `analytics` in neither its
consolidated "no auth check at all" list nor its own per-function notes are
in the PRD (link above) — not duplicated here.

Net effect: any caller holding the project's committed publishable key and a
restaurant UUID can read that restaurant's full yearly revenue, order count,
tip totals, and customer-count analytics. No exploit tooling needed, no
valid login required.

## Outcome

`analytics`'s one request path denies a caller who doesn't own the
requested restaurant, and denies a caller with no valid session at all —
verified by a negative-case test, not just the positive case. The brand
portal's existing `Dashboard.tsx` (the function's one known live consumer)
keeps working unchanged for a legitimate owner.

## Notes

**How this was found.** Not an assigned security sweep — a byproduct of
`ENG-020`'s own tech-design research (marketing ROI/traffic-source
reporting), which was pointed at this same function's `database.ts` as its
proposed extension point by the PRD. Reading the rest of the function —
`index.ts`, which the PRD, the ticket's Notes, and `observations.md` had
all named the file's neighbour without opening — found the gap. `ENG-020`'s
own design does not extend or touch `analytics` regardless of this ticket's
timeline; it ships as a new, already-authenticated `brand-portal` action
instead (`ADR-011`), specifically because this gap existed.

**Existing correct primitive to reuse.** `brand-portal/utils.ts`'s
`verifyRestaurantAccess` (and `ENG-022`'s promoted, throwing
`requireRestaurantAccess`, once that ticket ships) is already the
department's correct pattern for exactly this check — likely reusable here
directly, or via `_shared/restaurantAccess.ts` (already used by
`api-key-auth` for the same cross-function-directory reason); architect's
call at the design step. Retiring `analytics` in favour of `brand-portal`
entirely is also now a live option, since `ENG-020` puts a second,
authenticated analytics surface into `brand-portal` regardless.

**Relationship to `ENG-022` and `ENG-029`.** Third instance this week of the
same underlying bug class (missing/defeated restaurant-ownership check) on
this codebase, third different function, third different failure shape:
`ENG-022` — a correct check called with the wrong arguments or its result
discarded, in `brand-portal/`; `ENG-029` — a check fetched but never
threaded into any of `autopilot`'s 8 handlers; this one — no access-check
code of any kind, anywhere in `analytics`. `ENG-022`'s own PRD named
"auditing access checks outside `brand-portal/`" as an explicit non-goal;
this is now the second follow-on into that gap, after `ENG-029`. Worth the
EM's or approver's attention as a pattern, not just three unrelated tickets
— named in this PRD's Non-goals rather than expanded into a fourth PRD here.

## Log

- 2026-09-03 `intake → shaped` (architect, `continue` event pass, context
  `ENG-020` — this finding is a byproduct of that pass's own tech-design
  research, not its assigned subject; see `ENG-020` for the assigned work).
  Mode check clean (repo-root `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean (run before this ticket existed; scoped re-run post-pass below).

  PRD written short-form (auto-skip type, no readback —
  agent-originated finding with its own evidence,
  `skills/request-readback/SKILL.md`'s "when this does NOT run" list).
  Evidence gathered by reading `supabase/functions/analytics/index.ts` in
  full against `origin/main`, independently (not taken on the design
  subagent's word alone) — confirmed no `Authorization` header read
  anywhere in the file, and cross-checked `supabase/functions/README.md`'s
  consolidated "no auth check at all" list and the `## analytics` section's
  own Notes, both silent on the gap. Cross-checked `proposals.md`,
  `observations.md`, `agents/security/reviews/`, `agents/security/notebook/`,
  and `decision-journal.md` for any prior mention of this specific gap
  before filing — none found; the closest prior art is `ENG-022`'s and
  `ENG-029`'s own "outside `brand-portal`"/"different function" non-goals,
  not a duplicate finding.

  Incident notice raised: `inbox/2026-09-03-eng030-p0-incident.md`
  (`gate: incident`, `agent: architect`). Ran
  `departments/engineering/lib/eng-notify.sh raise` on it; see the item's
  own frontmatter and `traces/eng-notify-2026-09-03.log` for the result.

  **State:** `intake → shaped`, `owner: product-manager → architect`.
  **Consequence:** does not consume approver-facing WIP or the approval cap
  — `security`-typed, auto-skip G1, nothing waiting at a gate. Machine WIP
  (1/1, `ENG-016`, `ready`) also unaffected — `shaped` is short of the
  counted range (`ready` through `ready-to-ship`).

  `chained: ENG-030` — `shaped`, owned by `architect`, an agent-owned state;
  firing `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
  ENG-030` before this pass exits so the design step starts without waiting
  for a scheduled sweep, given the severity — same precedent `ENG-022`'s and
  `ENG-029`'s own creation entries set. This is the primary subject ticket's
  own second, separate chain fire in a pass whose assigned subject is
  `ENG-020`; see that ticket's own log for its own chain record. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board and scoped
  `ENG-020`/`ENG-030`: see pass notes in `agents/eng-manager/board/_index.md`.

- 2026-09-03 `shaped → designed` (architect, `continue` event pass, context
  `ENG-030` — this ticket's own turn at the front of `traces/.pending`).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
  7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*) — not
  mid-PRD, so step 2's checkpoint note doesn't apply. Mode check clean
  (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-030`) and
  whole-board: both exit 0, clean.

  Read the real code before designing against it, via `git show origin/main:`
  in `~/Documents/projects/_eng/aiorders-api` (and `_eng/restaurant-portal`
  for the one known consumer) rather than trusting either worktree's checked
  -out state, same standing habit `ENG-021`'s and `ENG-029`'s own passes
  used. Read `analytics/index.ts` in full — confirmed the PRD's citation
  exactly, no access-check code anywhere in the request path. Read
  `_shared/restaurantAccess.ts`, `api-key-auth/index.ts` (the closest
  structural precedent: single-file `index.ts`, no `handlers/` split, already
  importing this same shared primitive), `brand-portal/utils.ts`,
  `autopilot/index.ts`, `ADR-015`, and the ADR index. Read
  `restaurant-portal/src/services/analyticsService.ts` and its
  `integrations/supabase/client.ts` to confirm `supabase.functions.invoke`
  already attaches the caller's session `Authorization` header automatically
  when one exists — so AC3 (existing consumer unchanged) needs no frontend
  edit — and `App.tsx` to confirm `Dashboard` sits behind this portal's
  private-route block today. Read every existing `*.test.ts` in the repo
  (`admin-portal/handlers/*.test.ts`, `platform-customer-auth/*.test.ts`,
  `restaurant-portal-onboarding/restaurants.test.ts`) to find the actual
  testable-unit convention: every one imports a plain exported function from
  a sibling module, none imports a `serve`-wrapping `index.ts` directly — and
  `platform-customer-auth/handler.test.ts`'s own comment names not having a
  mocked `SupabaseClient` as a "named, not silent, gap" on this repo today.

  **Design:** `agents/architect/designs/ENG-030-analytics-function-restaurant-scoping-broken.md`.
  New `analytics/auth.ts` exporting `authorizeAnalyticsRequest(req, supabase,
  restaurantId, corsHeaders)` — decodes the caller, 401s with no valid
  session, else calls `verifyRestaurantAccess` (`_shared/restaurantAccess.ts`,
  same primitive `ADR-015` already chose for `autopilot` and for the
  identical reason: `analytics` is outside `brand-portal/` too), 403s if
  denied, else returns `null`; `index.ts` calls it once and returns its
  response if non-null, with the existing `source`/switch/aggregation code
  otherwise untouched. **No new ADR** — `ADR-015`'s comparison (`_shared/
  restaurantAccess.ts` vs. `brand-portal/utils.ts`'s two variants) transfers
  to `analytics` unchanged, since it is in the identical "outside
  `brand-portal/`" position `autopilot` was in; the design cites `ADR-015`
  directly rather than minting a content-free restatement of it (`adrs: []`
  on both this design and the ticket frontmatter — no entry added to
  `decisions/_index.md`, `next_id` stays `ADR-016`). **No one-way door** —
  same conclusion as `ENG-022`/`ENG-029`: an additive import of an existing,
  already-deployed shared primitive, no schema change, no new datastore or
  vendor, no contract change visible to a legitimate caller. `touches_data:
  false` (no migration), `touches_models: false` (nothing in the diff calls a
  model). Test approach commits to the same not-yet-proven stubbed-
  `SupabaseClient` shape `ENG-029`'s design already planned, wider than
  `platform-customer-auth`'s own already-merged (but DB-branch-incomplete)
  precedent — required here because AC4 explicitly names the wrong-tenant
  case, which only a stub (or a live project) can exercise. Every acceptance
  criterion walked, full risk table (including the pre-existing
  "restaurant not found" vs. "access denied" distinction `access.error`
  surfaces, inherited unchanged from the shared primitive, same as
  `api-key-auth`'s and `ENG-029`'s own design already accept): the design
  itself.

  **One observation filed** (`observations.md`): `ENG-029` and this ticket
  are both about to independently write their own stubbed-`SupabaseClient`
  test helper, same shape, same day, in two different directories — worth
  consolidating into one shared stub once either actually lands, not before
  (neither has reached `building` yet, so nothing is duplicated on disk
  today).

  **State:** `shaped → designed`. **Owner stays `architect`** — see Routing
  below.

  **Routing (step 11): would be `ready` — held at `designed` instead.**
  Neither L0 nor a one-way door, so the skill's own routing reads `ready`,
  `owner: eng-manager`. Machine WIP re-checked fresh from every ticket's own
  frontmatter, not the board index table: `ENG-016`/`ENG-031` `building`,
  `ENG-032`/`ENG-033`/`ENG-034` `ready` — still `1/1`, the family reading
  `ENG-016`'s own work-breakdown pass established, none `shipped`. Same
  precedent `ENG-014`/`ENG-017`/`ENG-019`/`ENG-020`/`ENG-021`/`ENG-023`/
  `ENG-025`/`ENG-026`/`ENG-029` already set: held at `designed`, owner
  staying `architect`, rather than writing `ready` while the one slot is
  occupied. `ENG-030`'s own `depends_on: []` and empty `priority:` confirm
  the WIP cap is the only hold — the approver did not exercise the one lever
  the P0 incident notice offered.

  **Dead-end sweep:** out of scope for a `continue` event (narrower
  contract) — nothing surfaced unsought this pass (unlike `ENG-020`'s and
  `ENG-029`'s own design passes, this one found no new byproduct P0; the
  code read for this design was confined to `analytics/`, `_shared/`, and
  the two files already named in Notes, plus the one frontend consumer).
  **Notify sweep:** no new gate item this pass (no one-way door). Swept
  `inbox/` (`date -u`: `2026-09-04T00:31:57`) — nothing crosses the 24h
  no-nudge-no-decision threshold: closest is `ENG-022`'s merge request at
  ~23h05m, not yet due; `ENG-008`/`ENG-009`/`ENG-010` already carry their
  one-ever nudge; `ENG-015`/`ENG-024`/`ENG-027` rescope/`ENG-028` and the
  `ENG-029`/`ENG-030`/`ENG-035` P0 incidents are all well under and/or
  informational-only with nothing owed. **Journal:** no gate answered this
  pass (no G1/G2/G3, no merge request) — not applicable.

  **Board update** — In-flight row for `ENG-030` (`shaped → designed`,
  updated date unchanged, still 2026-09-03). See
  `agents/eng-manager/board/_index.md` for the full pass entry.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-030`) and whole-board: see board index.

  `chained: none` — held by the machine-WIP cap (`1/1`, the `ENG-016`
  family: `ENG-016`/`ENG-031` `building`, `ENG-032`–`034` `ready`, none
  `shipped`), one of the documented no-chain conditions; re-check once that
  family reaches `shipped`. Not blocked, not terminal, not waiting on the
  approver — only the cap.
