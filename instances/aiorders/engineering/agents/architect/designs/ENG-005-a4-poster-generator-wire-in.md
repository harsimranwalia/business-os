---
ticket: ENG-005
project: aiorders-admin-hub
author: architect
created: 2026-08-27
adrs: []
one_way_doors: []
touches_data: false
touches_models: false
---

# Wire A4PosterGenerator into RestaurantDetails.tsx — technical design

## Approach

Investigated fresh against `origin/main` in the department worktree (`git fetch`
first, both `aiorders-admin-hub` and `aiorders-api`) rather than trusting the G1
follow-up's summary secondhand.

`src/components/A4PosterGenerator.tsx` (committed whole at `bfddffe`, untouched
since) is a self-contained, already-finished component: a canvas-rendered A4
poster preview plus a "Download A4 Poster PDF" button
(`jsPDF`), and a QR code pointing at `{websiteUrl}/links/{restaurantId}`, fetched
via the `url-shortener` Supabase edge function — **confirmed present** at
`supabase/functions/url-shortener/index.ts` in `aiorders-api`'s `origin/main`,
closing the one real risk the original readback flagged (a dependency on code
this department couldn't see). It takes its own Supabase session
(`supabase.auth.getSession()`) and degrades silently — no session, no token, the
QR fetch just returns early — so a stale/missing session cannot crash the page,
only leave the QR blank. `jspdf` (`^4.2.0`) is already in `package.json`: **no
new dependency**.

`src/pages/RestaurantDetails.tsx` (900 lines, route `/restaurants/:id/details`,
behind the app's existing `<ProtectedRoute>`) already fetches a `Restaurant`
record keyed by the route's `:id` param, with `id`, `name`, `website`, and
`logo_url` on it directly — four of the component's five props by name or
trivial rename. **The fifth, `primaryColor`, has nothing to read from.**
The `Restaurant` interface (52 fields, read in full) has no color/theme field
anywhere, on this page or in the fetched record itself. Pass
`primaryColor={null}`; the component's own fallback
(`const accent = primaryColor || '#E85C2A'`) is exactly the designed behavior
for "no brand color yet," not a workaround invented here.

The page's body is a `grid gap-6 md:grid-cols-2` of `<Card>` sections (Basic
Information, Brand Owner, Location, Restaurant Features, …). The change is one
more `<Card>` in that same grid — the page's own existing composition pattern,
not a new layout primitive — containing the `<A4PosterGenerator>` instance.
Reachable via the same navigation that already reaches this page (a
restaurant's row → Details), satisfying the ticket's "discoverable, not only a
direct URL" requirement with zero new nav wiring.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `src/pages/RestaurantDetails.tsx` | Add one `<Card>` to the existing grid (title: "Marketing Poster" or similar), rendering `<A4PosterGenerator restaurantName={restaurant.name} websiteUrl={restaurant.website} logoUrl={restaurant.logo_url} primaryColor={null} restaurantId={restaurant.id} />` | frontend |
| `src/components/A4PosterGenerator.tsx` | None — complete as committed at `bfddffe` | — |
| `package.json` | None — `jspdf` `^4.2.0` already present | — |
| `aiorders-api`'s `url-shortener` function | None — already deployed, reused as-is | — |

## Data

Not applicable — `touches_data: false`. No schema, table, or column change.

## Interfaces

None new. Reuses the existing `url-shortener` edge function's existing
contract as-is. No new endpoint, no new public contract, no change to who can
reach what — the surface is the admin hub's existing authenticated
`/restaurants/:id/details` route.

## Alternatives considered

- **Pass a real per-restaurant brand color instead of `null`.** Rejected for
  this ticket: no such field exists on `Restaurant` today, and adding one is a
  data-model change this ticket's own PRD excludes (non-goals: don't touch any
  of the admin-hub's other 64 uncommitted files, don't invent scope). Revisit
  if/when a brand-theming ticket exists.

## One-way doors

None. An additive UI section using an already-committed, self-contained
component and an already-deployed edge function is fully reversible — deleting
the one new `<Card>` block is a one-file revert, same as the PRD's own
"cleanly reverted" bar for the branch not taken. No ADR, no G2.

## Risks

- **QR code depends on the caller's live Supabase session at render time** —
  matches the component's own existing behavior (not introduced by this
  wiring); if the session is missing/stale, the poster still renders, just
  without a working QR.
- **No per-restaurant brand color** — the poster always uses the component's
  default accent (`#E85C2A`). Cosmetic only; out of scope here (see
  Alternatives).

## Rollout

Straight commit on a branch, PR per `aiorders-admin-hub`'s L1 autonomy. No
migration, no feature flag — additive, admin-only, reversible in one file. No
new recurring cost: the QR edge function is already deployed and billed under
existing usage.

## Out of scope

Per the PRD's own non-goals: no touch to any of `aiorders-admin-hub`'s other 64
uncommitted files, no comprehensive testing beyond smoke-level, no
per-restaurant brand color field.
