# Acceptance — ENG-020 (Marketing ROI reporting — acquisition-channel breakdown)

## Why this ran in full, not as receipt bookkeeping

`ENG-020` is a standalone ticket (not a work-breakdown child) and owns all 5
of its own PRD's acceptance criteria — no `ENG-031`/`ENG-037`-style
0-criteria schema-only carve-out applies. `acceptance-check/SKILL.md`'s
trigger ("a ticket enters state `shipped`") has no exemption here, and the
department's own standing proposal (filed `2026-09-04`, after ten ship
events ran receipt-bookkeeping only) is to actually run this skill when a
ticket has real criteria to check, not skip it by habit.

## Scope

All 5 acceptance criteria in the PRD
(`agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md`),
across both repos (`aiorders-api` backend RPC + handler, `restaurant-portal`
frontend page).

## Check against the live result — not the proxies

Both PRs (`aiorders-api` #17, `restaurant-portal` #4) merged directly on
GitHub with no written reply, 94 seconds apart
(`2026-09-06T00:41:23Z` / `00:42:57Z`) — landing together, as both PR bodies
required. Confirmed zero drift before trusting any upstream receipt:
`git diff {reviewed-tip} origin/main --stat` empty on both repos, and each
merge commit's own parents show the reviewed branch tip merged as-is (no
squash, no extra commits folded in) — `672dfa77` (`aiorders-api`) and
`8eea8f15` (`restaurant-portal`).

**Confirmed live, not just merged, on both sides:**
- `aiorders-api`: `supabase functions list` shows `brand-portal` redeployed
  at `2026-09-06T00:45:28Z`, ~4 minutes after the merge — no tracked
  workflow responsible, same by-hand-deploy pattern `ENG-037`/`ENG-038`
  already established for this repo. `supabase db query` against the linked
  project confirms `get_acquisition_breakdown(p_restaurant_id uuid, p_from
  timestamptz, p_to timestamptz)` exists with exactly the signature the
  design specifies.
- `restaurant-portal`: `gh run list` shows "Deploy to Cloudflare Pages" ran
  on the merge commit (`8eea8f15`) and completed `success` at
  `2026-09-06T00:43:01Z`, ~90 seconds after the merge — this repo's own
  push-triggered CI, not a by-hand action.

Read the merged source directly (`git show origin/main:{path}`) rather than
trusting any gate's own account of it, for the two files carrying the most
acceptance-relevant logic: `supabase/functions/brand-portal/acquisition.ts`
and `restaurant-portal/src/pages/acquisition/Index.tsx`. No test campaign or
write action taken against production — this is a read-only reporting
surface, so nothing here needed the "don't exercise a real send" boundary
`ENG-038`'s/`ENG-039`'s checks had to hold.

## Walk every criterion

| AC | Criterion | Checked against | Result |
|---|---|---|---|
| 1 | Owner sees own customers/orders/revenue by acquisition channel, scoped to own restaurant | `acquisition.ts` `get_acquisition_report`: `verifyRestaurantAccess(restaurant_id, supabase, user)` called before any query, `access.hasAccess` gated, `restaurant_id` passed straight to the RPC — the checked id and the queried id are the same variable, no confused-deputy gap. `Index.tsx` renders `StatsCard`×3 (customers/orders/revenue) plus `ChannelBreakdown` from the response | **Pass** |
| 2 | Changing the time range updates the figures | `Index.tsx`: `useQuery({ queryKey: ['acquisition-report', currentRestaurant?.id, preset], ... })`, `resolveRange(preset)` recomputes `from`/`to` on every `preset` change — a `preset` change is a `queryKey` change, so react-query refetches automatically | **Pass** |
| 3 | A customer with no attribution data shows as an explicit "unknown/direct" bucket, never silently dropped or miscounted | `acquisition.ts`: `byChannel.set('direct_unknown', {customers:0, orders:0, revenue:0})` seeded before the aggregation loop; the render filter (`key === 'direct_unknown' \|\| agg.customers > 0 \|\| agg.orders > 0`) keeps this bucket even at zero while every other channel is omitted once empty | **Pass** |
| 4 | Framing makes clear organic/direct traffic reflects the restaurant's whole web presence (AI SEO among other factors), not an isolated AI-SEO effect | `Index.tsx`: page subtitle ("not a claim about any single channel's effect on its own"), a coverage sentence (`{attributed_pct}% of orders... could be traced to a source`), a `low_volume` caveat, and — gated on `hasOrganicSearch` — "Organic reflects your whole web presence — listings, reviews, site content, and your AI-generated SEO together — and isolates none of them individually." All four mechanisms the design's own Risks section names are present verbatim, not just implied | **Pass** |
| 5 | A request for a restaurant the caller doesn't belong to is rejected server-side, not just hidden in the UI | `acquisition.ts`: `access.hasAccess` check returns `{success: false}` before the RPC is ever called — no data leaves the server on denial. Same `verifyRestaurantAccess` call shape as `menus.ts`/`catering.ts`/`restaurants.ts`/`onlineOrders.ts` (the correct shape), not the broken argument-order shape `feedback.ts`/`offers.ts` carry (`ENG-022`'s own fix scope) | **Pass** |

## Check the non-goals

Diff scanned against the 5 non-goals (Clarity integration, a true ROI ratio,
isolating AI-SEO specifically, a staff-facing all-restaurants rollup, any
change to the existing `Analytics`/`Reports` pages) — none present. The only
two non-`acquisition`/`brand-portal` files touched are `App.tsx` (+2: one
import, one route) and `Sidebar.tsx` (+2: one icon import, one nav entry) —
purely additive registration, no existing page's behavior touched. No
Clarity reference anywhere in the diff.

## Check the cost

PRD: `$0/month` expected (no new vendor, extends already-wired edge function
and Supabase compute). `git diff origin/main...HEAD -- '*.json' '*.lock'`
empty on both repos (re-run fresh this pass) — no new dependency. Matches.

## Route

**All 5 criteria: pass**, verified directly against the exact merged and
now-live source (`aiorders-api@672dfa77`, `restaurant-portal@8eea8f15`), not
against the test suite or any gate's own summary. State → `verified`, owner
→ `eng-manager`.

## Step 6b — continue an approved sequence?

Does not apply. The PRD's Non-goals list names four deferred ideas (Clarity
integration, a true ROI ratio, AI-SEO isolation, a staff-facing rollup), but
none carries the shape `acceptance-check/SKILL.md` step 6b requires — a
named next item with real shape, plus a G1 answer that explicitly signed off
on continuing a sequence. This ticket's own G1 was answered **approved**
with no additional comment (2026-09-03T15:53:14) — a bare approval, same bar
`ENG-019`'s own closing entry already held to. Nothing auto-filed.

## What the estimate got right, and what it missed

`time_estimate: a day and a half to two days` (build only) held for the
build hop itself, but undercounted total elapsed pipeline time: three
review+quality rounds (round 1 quality-failed on missing frontend test
coverage entirely — no `*.test.tsx` existed for this page at intake despite
`BroadcastReport.test.tsx` being a direct in-repo precedent; round 2
quality-failed narrower, on two of AC4's four mechanisms going untested
despite the gap's own narrative naming all four; round 3 passed clean) before
one security round and release-readiness. The recurring shape across both
quality failures — a gap's own prose naming more than its "specific fix"
bullet actually closes — is already flagged as an observation
(`observations.md`, filed at round 2, second occurrence after `ENG-038`'s
round-3→4 finding); not re-filed here. Worth carrying forward for the next
report-page PRD: budget an explicit frontend test-coverage line item for any
new page-level component, the same way this repo already has a tested
precedent (`BroadcastReport`) that this ticket's own intake didn't reference.

## Also worth recording

`blocks: []` — nothing else on the board depends on this ticket; shipping it
does not unblock or chain anything further. Machine WIP unaffected — this
ticket left the counted `ready`..`ready-to-ship` range at its own prior
`ready-to-ship → blocked` hop; the slot has been held by the `ENG-021`
family (still `building`) throughout.
