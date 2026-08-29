---
ticket: ENG-011
project: aiorders-admin-hub
status: designed
size: M
author: product-manager
created: 2026-08-29
decided: 2026-08-29T11:14:54.862156+00:00
---

# Client stage & health visibility on the Brands admin page — plus stage filtering

## Readback

**You said:** "on the admin panel we are unable to see if the restaurant is
our client or what stage he is at on the brands page we have. the admin
staff should be able to filter according to the stage of the client so they
can prioritize the clients based on the stage they are at . also the health
of restaurant and maybe tickets"

**Understood as:** Staff working the admin panel's Brands page (confirmed —
`aiorders-admin-hub`'s `src/pages/Brands.tsx` — a real, existing page) can't
tell, per row, whether a listed restaurant is an actual AIOrders client or
what stage of the client relationship it's in, so they can't prioritize who
to work on. You want the stage shown and filterable. You also want a
restaurant "health" signal on the same page, and — hedged with "maybe,"
read as a real but lower-conviction ask — something about support tickets.

**Requirements for this ticket:**
1. `[stated]` Staff can see, per restaurant on the Brands page, whether it
   is a current AIOrders client and what stage it's in.
2. `[stated]` Staff can filter the Brands page by stage.
3. `[proposed]` "Is this restaurant our client" is answered by the stage
   itself, not a separate flag — see "Assumed" below.
4. `[stated]` Staff can see a restaurant-health signal on the same page.
5. `[proposed]` A minimal, zero-new-cost health signal for this ticket —
   see "Assumed" below; a fuller scored/weighted health model is not this
   ticket.

**Assumed, and worth correcting if wrong:**
- **"Is our client" is the same fact as "what stage,"** not a second field —
  a restaurant at an early stage (lead-adjacent, mid-onboarding) reads as
  not-yet-a-client, one at "Live/Active" reads as a client, one at
  "Inactive/Churned" reads as a former client. One field answers both
  questions in the raw request, and avoids a second, separately-maintained
  "is client" flag drifting out of sync with stage (a risk the architect's
  independent reading raised explicitly). Proposed, not stated — easy to
  split into two fields later if a case shows up where they diverge.
- **A proposed starting stage set**, grounded in evidence already on disk
  rather than invented: `Brands.tsx`'s own `Brand`/`Restaurant` interfaces
  already carry `onboarding_step: number` (used by a real onboarding
  wizard, per `restaurant-portal-onboarding/brands.ts`) and `is_active`
  (per `restaurant-claims/index.ts`'s brand-creation call). Neither is
  surfaced or labeled on the Brands list today. Proposed business-language
  stages: **Onboarding** (`is_active` false, `onboarding_step` in
  progress) → **Live/Active** (`is_active` true) → **Inactive/Churned**
  (was active, no longer). The exact taxonomy and how it maps to columns is
  the architect's call at design time; this is a starting point for you to
  correct at G1, not a spec.
- **Health, for this ticket, is a minimal activity-based signal** (e.g.
  derived from order recency/volume — data the platform already has, no
  new integration, no new stored pipeline) rather than a weighted score
  with thresholds or alerting. Proposed as the cheap, buildable-now default;
  a fuller health model is named as a non-goal below.
- **"Tickets" is not in this ticket.** See the standing question below —
  its answer swings cost by roughly an order of magnitude, the same shape
  as `ENG-008`'s "engagement" question.
- **Filtering is the one unhedged, must-have part of the raw request** —
  stated plainly, unlike health and tickets which read as added on.

**Second reading agreed / diverged on:** Two independent readings were run
— this PM's, and, blind to it, the architect's (a subagent given only the
raw request and the business profile, model `opus` per the skill). Both
converged on the core shape: a missing stage/client-status concept on the
Brands page, an explicit filter requirement, an undefined "health" concept,
and an undefined "tickets" concept. **No material divergence** — both
readings agree on scope and on what this is for; the difference was depth,
not direction. The architect's reading additionally named, unprompted, the
specific one-way-door risk of a manually-set "is client" field drifting out
of sync with stage if AIOrders ever derives client status from billing —
folded into the "Assumed" item above rather than treated as a fork, since
both readings still agree stage is the thing to build.

Both readings independently flagged the same three things as **genuinely
unresolvable from the text alone** — a joint gap, not a disagreement:
the stage taxonomy's exact names, what "health" is computed from, and
what "tickets" refers to. Per the skill, a joint gap this size (three
items) doesn't become three separate approver questions — the first two
are shaped here as evidence-grounded, cheap-to-correct `[proposed]`
defaults confirmable at this G1; the third ("tickets") is large enough in
its cost range, and hedged enough in the raw text ("maybe"), to be split
out as its own standing non-blocking question instead, the same move
`ENG-008` made for "engagement."

**Evidence checked, not assumed.** `aiorders-admin-hub`'s live worktree
(`src/pages/Brands.tsx`) confirms the Brands page exists and today filters
only on `'all'` vs `'website_created'` — no stage, client, health, or
ticket concept anywhere on it. `aiorders-api`'s migrations, edge functions,
and Brands.tsx's own interfaces were searched for `stage`, `lifecycle`,
`health`, `last_order`, `churn`, and `ticket`/`support` — no support-ticket
table or health signal exists anywhere in either repo today. This resolves
what would otherwise have been a guess about whether "tickets" means
extending something that exists (it doesn't) into a confirmed net-new
question for the approver, and confirms the proposed stage taxonomy is
grounded in real, already-present columns rather than invented.

## Problem

Staff running the admin panel's Brands page can't tell which restaurants
are actual paying clients versus earlier-stage or inactive ones, and can't
see how a client is doing, so everyone on the list gets worked in the same
order regardless of where they actually sit — no way to prioritize
onboarding-stuck restaurants, at-risk active ones, or deprioritize churned
ones.

## Why now

Approver-initiated; no stated deadline. Directly blocks staff from
triaging their own workload on the one page built for it.

## Users

AIOrders admin staff operating the Brands page. Not restaurant-facing, not
the separately-flagged agency/reseller admin view (a different, already
separately-raised request about scoping what agency/reseller staff can see
— untouched by this ticket).

## Proposed change

After this ships, staff opening the Brands page see each restaurant's
client stage and a simple health indicator, and can filter the list by
stage to work it in priority order.

## Acceptance criteria

1. `[stated]` Given the Brands page, when staff view the list, then each
   row shows the restaurant's current stage (from a defined, finite set).
2. `[proposed]` Given a restaurant's stage, staff can read from it alone
   whether the restaurant is a current client — no separate "is client"
   indicator needed.
3. `[stated]` Given the Brands page, when staff apply a stage filter, then
   only restaurants in the selected stage(s) are shown.
4. `[inferred]` Given an applied stage filter, when staff clear it, then
   the full, unfiltered list returns.
5. `[proposed]` Given a restaurant with order history, when staff view its
   row, then a minimal health indicator (derived from existing order
   activity — no new integration) is shown.
6. `[proposed]` Given a non-staff request to the Brands page or its filter,
   then it's rejected by the same authorization gate the rest of the admin
   portal already uses.

## Non-goals

- A support-ticket count or indicator of any kind — the standing question
  below; genuinely unscoped until answered, and no ticket/support system
  exists anywhere in either repo today.
- A weighted, threshold-driven, or alerting health score — this ticket is a
  minimal activity signal only.
- Any change to the separate agency/reseller data-scoping request already
  raised (a different admin surface, a different problem).
- A staff-configurable stage taxonomy — the stage set is fixed for this
  ticket; making it editable is future work if asked for.
- Leads / pre-brand records (`Leads.tsx`, `FranchiseeLeads.tsx`) — scoped to
  the Brands page and existing brand records only.

## Risks and unknowns

- **Stage taxonomy is proposed, not confirmed** — grounded in existing
  `onboarding_step`/`is_active` columns, but the exact names and count of
  stages are this PRD's proposal, correctable at G1.
- **"Health" could grow** — today's proposal is a minimal, free signal;
  if the real ask is closer to a scored/weighted model, that's materially
  more build, flagged now rather than discovered mid-build.
- **"Tickets" is a genuine unknown, confirmed unbuilt anywhere in either
  repo** — could be a small display field (if a source already exists
  outside AIOrders that you haven't told us about) or a new system
  entirely. Standing question open, not blocking this ticket.
- No stated deadline, no specific restaurant named as blocked on this
  today.

## Cost

- Build: `M` — spans `aiorders-api` (a stage-bearing column/mapping,
  reusing `onboarding_step`/`is_active` where possible) and
  `aiorders-admin-hub` (Brands page display + filter UI), each half
  simple on its own, same order of magnitude as `ENG-008`. Rough band:
  half a day to a couple of days.
- Run: `$0/month` for this ticket's scope — no new vendor, no new
  datastore. If "tickets" resolves to a new external integration, that's
  separate cost, assessed once scoped.

## Decision

Filled in by the approver.
