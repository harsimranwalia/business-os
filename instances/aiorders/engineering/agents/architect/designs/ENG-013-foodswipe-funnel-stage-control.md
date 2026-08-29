---
ticket: ENG-013
project: aiorders-admin-hub
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Foodswipe funnel page — staff-settable pipeline stages — technical design

## Approach

Add one nullable override column on `profiles` that takes precedence over
`classifyStage()`'s automatic computation, rather than replacing the
automatic classification with a stored one everywhere — this keeps the
existing, already-correct derivation as the default and makes the manual
path additive only. Extend the existing `admin-portal/handlers/foodswipe.ts`
handler with one new write action, reusing its already-present
admin/sub-admin authorization gate rather than writing a new one. On the
frontend, add a per-card stage control to `FoodswipeListings.tsx`, styled
after the existing edit affordance `Leads.tsx` already established
elsewhere in this same admin panel (dropdown + dialog pattern via
`@/components/ui/dropdown-menu` and `@/components/ui/dialog`), rather than
inventing a new interaction pattern for one page.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `profiles` table (migration) | add — one nullable column, `foodswipe_stage_override` (six-value constrained), default `null` | database |
| `aiorders-api`: `admin-portal/handlers/foodswipe.ts` | modify — `classifyStage()` checks the override first, falls back to existing automatic logic; add a new write branch (e.g. `POST` with an explicit action field, since the handler already accepts `POST` for reads today — the path split is the building engineer's call) that sets or clears the override | backend |
| `aiorders-admin-hub`: `src/pages/FoodswipeListings.tsx` | modify — per-card stage control (set + reset-to-automatic) on `KanbanCard`; visual marker distinguishing a manual override from an automatic classification | frontend |

## Data

- **One new nullable column on `profiles`**, no new table. `profiles` is
  the one entity present at every stage (even the earliest two,
  `account_created`/`profile_updated`, have no `restaurants` row yet), so
  it's the only correct place to key an override that must work for all
  six stages — keying it on `restaurants.id` instead would leave the two
  earliest stages unable to be overridden at all.
- **`profiles`' own base table is not in this repo's tracked migration
  history** — confirmed by searching every migration under
  `supabase/migrations/` for `profiles`; the six hits are all RLS
  policies and later references, none a `CREATE TABLE`. Consistent with
  `observations.md`'s 2026-08-26 finding that this repo's schema history
  was reconstructed after the fact, not authored from the start. Not
  blocking — an `ALTER TABLE profiles ADD COLUMN ...` migration doesn't
  need the original `CREATE TABLE` on hand, only the table's confirmed
  existence and column set, both established from the live handler code
  cited above — but flagged here so the engineer who builds this writes
  the migration against the real production shape and doesn't go looking
  for a `profiles` migration that isn't there.
- No change to `restaurants` or `restaurant_listing_data`. No backfill —
  every existing row's override starts `null`, which is exactly "keep
  computing automatically," so nothing about current behavior changes
  until a staff member actually sets one.

## Interfaces

`admin-portal/handlers/foodswipe.ts` gains one write action alongside its
existing read, reusing the same `adminSupabase` (service-role) client and
the same `allowedRoles = ['admin', 'sub-admin']` gate already enforced
there today — no new authorization surface, an extension of one that's
already correct and already exercised in production (the same pattern
`leads.ts`'s `updateWebsiteLead` uses for its own write). Sets or clears
`profiles.foodswipe_stage_override` for one profile id. Response shape for
the existing `GET`/kanban read is unchanged except that a listing's `stage`
now reflects the override when one is set — no new field needed on the
read side, since "what stage is this in" should mean the same thing
whether it's automatic or manually set; the frontend distinguishes
*source* (manual vs. automatic) separately, not the stage value itself.

## Alternatives considered

- **Store stage as a plain column everywhere, drop the derivation
  entirely.** Rejected — throws away a working, correct, zero-maintenance
  automatic classification for every listing nobody has ever manually
  touched, and would need a backfill to populate six stages' worth of
  history from the same columns `classifyStage()` already reads. The
  override approach gets staff control only where they actually use it.
- **Key the override on `restaurants.id` instead of `profiles.id`.**
  Rejected — the two earliest stages (`account_created`, `profile_updated`)
  have no `restaurants` row yet, so this would leave exactly the listings
  newest to the funnel unable to be corrected, which is backwards from
  what staff need most.
- **A new dedicated `foodswipe_overrides` table instead of a column on
  `profiles`.** Rejected as unnecessary weight for a single nullable
  field with no history requirement in this ticket's own acceptance
  criteria — a column is the smaller, more reversible change; a table
  is available later if an audit trail is ever asked for.

## One-way doors

None. One new nullable column, additive only, `null` by default so every
existing listing's behavior is unchanged until a staff member acts;
reusing an existing, already-correct authorization gate rather than
adding a new one; no data migration, no backfill, fully reversible by
dropping the column and the one new write branch. Same shape `ENG-011`
used for its own additive fields. Moves straight through `designed`, no
G2.

## Risks

- **`profiles`' untracked migration origin** (see Data) — not a design
  risk, but a real gap the building engineer needs to know about before
  writing the `ALTER TABLE`, rather than discover mid-build.
- **The six-value constraint on the override column needs to stay in
  sync with `classifyStage()`'s own `Stage` union type** — if a future
  ticket changes the stage set (the standing pre-signup-leads question,
  if answered yes, would likely do exactly this), both the constraint and
  the union type need updating together, or an override could reference
  a stage that no longer classifies automatically. Worth a code comment
  at build time, not a blocker now.
- **No audit trail for who set an override or when**, beyond whatever
  `updated_at`-style tracking the building engineer chooses to add —
  this ticket's acceptance criteria don't ask for one; flagged in case
  that turns out to matter once staff actually use this.

## Rollout

Straight — additive column (defaults `null`, no behavior change until
used), additive write action, additive UI control. No flag needed.
Rollback is reverting the three components; nothing to backfill either
direction, since the column starts and stays `null` for every listing no
staff member has touched.

## Out of scope

A pre-signup / cold-lead pipeline (the standing question,
`inbox/2026-08-29-eng013-presignup-leads-question.md` — a new record type
with no `profiles` row to hang off of, not an extension of this design).
Editing a listing's underlying details. An audit/history trail of stage
changes. Renaming or restructuring the six existing stage values.
