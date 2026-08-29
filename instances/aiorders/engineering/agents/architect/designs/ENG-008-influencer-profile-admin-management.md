---
ticket: ENG-008
project: aiorders-admin-hub
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Influencer board admin management — technical design

## Correction, stated plainly rather than buried

An earlier draft of this design (before `aiorders-admin-hub` had a
worktree on this host) assumed region and campaign-type preference needed
new columns, based only on `aiorders-api`'s edge-function code. Once the
worktree existed and `src/pages/Influencers.tsx` (the actual influencer
board) could be read directly, that assumption turned out wrong in a way
that shrinks this ticket, not grows it — see Evidence below. Corrected
before any migration was written; nothing built against the earlier
version.

## Approach

The entire Influencer Management page is **read-only today** — search and
a location filter, plus a detail dialog that displays fields but has no
save/edit path anywhere. Region preference (`city_preference`) and
campaign-type (`barter_visit` / `min_visit_payment`) already exist as real
columns and are already **displayed**, just not editable — so most of this
ticket's "region/campaign-type" requirements are a UI edit-capability gap,
not a schema gap. Only `staff_rating` and `collaboration_count` are
genuinely new columns. Add those two, extend the existing paid/barter
model from one boolean to two independent flags (so "both" is
representable, which the current single boolean cannot express), and add
an edit form to the existing detail dialog — through a new
`admin-portal/handlers/influencers.ts` endpoint, admin-auth gated, same
pattern `ENG-007` used.

## Evidence read before designing

**`aiorders-api`** (`origin/main`, worktree already existed): the backend
concept is real (`influencers`, `influencer_campaigns`,
`influencer_invitations`, an `outgoing-communications` actor, an
invitation-based access pattern gated by `brand_managers` for
restaurant-side campaign management — not the gate this ticket uses).
`admin-portal`'s existing `profiles.role`/`additional_roles` check
(`admin-portal/index.ts`) is the staff-facing gate this ticket reuses, same
as `ENG-007`. No `influencers`/`influencer_campaigns`/`influencer_invitations`
table appears in any tracked migration — same untracked-base-schema gap
`ENG-006` found elsewhere, not fully closed by `5b3bac2`. No DB credential
available from this environment to read the live schema directly.

**`aiorders-admin-hub`** (worktree created this pass — none existed on
this host before): `src/pages/Influencers.tsx` is the influencer board.
Its own `Influencer` interface (391 lines, read in full) already declares
— and the page already fetches with `select('*')` and renders —
`followers`, `engagement`, `followers_growth`, `engagement_growth`,
`barter_visit`, `min_visit_payment`, `city_preference: string[]`, and
`cuisine_preference: string[]`, alongside identity fields. Specifically:
- The table's "Engagement" column and the detail dialog's "Engagement
  Rate" field already render `engagement`/`engagement_growth`. Displayed,
  not editable — see `ENG-009` correction note below; that ticket's own
  premise needs revisiting for the same reason this one did.
- The table's "Payment Type" column and detail dialog already render
  `barter_visit` (as a Barter/Paid badge) and `min_visit_payment`.
  Displayed, not editable.
- The detail dialog's "Location Preferences" section already renders
  `city_preference` as read-only badges. Displayed, not editable.
- **Nothing on this entire page is editable.** No form, no save action,
  no write call anywhere in the file — `Contact` and `View Profile` are
  the only buttons, and neither writes anything. So "we are unable to
  see or edit... or update those" reads precisely now: staff can already
  *see* region and payment-type preference; what's actually missing
  across this whole ticket is the *edit* path, plus two genuinely new
  fields (rating, collaboration count).
- `barter_visit` is a single boolean — the current UI shows Barter XOR
  Paid, never both. This ticket's own acceptance criteria (3/4) ask for
  "paid, barter, or both," which a single boolean cannot represent — see
  Data below for the fix.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/migrations/{ts}_influencer_admin_fields.sql` | new — 2 new columns (`staff_rating`, `collaboration_count`) plus the `barter_visit` → two-flag migration | database |
| `supabase/functions/admin-portal/handlers/influencers.ts` | new — GET/PATCH, admin-auth gated | backend |
| `supabase/functions/admin-portal/index.ts` | modify — route `influencers` to the new handler | backend |
| `src/pages/Influencers.tsx` | modify — add an edit form to the existing detail dialog (city_preference, paid/barter flags, staff_rating, collaboration_count); update the Payment Type badge to read the two new flags instead of `barter_visit` | frontend |

## Data

- `staff_rating` — `smallint`, nullable, `CHECK` 1–5. Genuinely new.
- `collaboration_count` — `integer`, `NOT NULL DEFAULT 0`. Genuinely new
  — "no collaborations yet" and "not yet answered" are the same state, so
  a default is correct here (unlike the fields below, where null must stay
  distinguishable from a real value).
- `accepts_paid` / `accepts_barter` — two new `boolean` columns,
  **backfilled from the existing `barter_visit`** in the same migration
  (`accepts_barter = barter_visit`, `accepts_paid = NOT barter_visit`),
  preserving every existing row's current meaning exactly. `barter_visit`
  itself is left in place, unused by new code, rather than dropped in the
  same migration — dropping a column every other caller might still read
  is exactly the kind of change to make separately, once every reader is
  confirmed migrated (this repo's own `Influencers.tsx` is the only
  in-repo reader found; `restaurant-influencer-campaigns` in `aiorders-api`
  was not found to read it, but that's a different repo and worth the
  engineer's own check before any drop, not this ticket's problem to
  solve). This ticket's frontend change reads the two new flags; nothing
  new reads `barter_visit`.
- `city_preference` and `min_visit_payment` — **no schema change.** Both
  already exist and already hold real meaning; this ticket only adds a
  write path (via the new handler) and an edit control on the existing
  display.

All four new/changed columns are additive or backward-compatible
backfills — no existing reader breaks, since `barter_visit` itself is
untouched.

## Interfaces

`admin-portal` (existing router, new handler file):

- `GET /admin-portal/influencers/{id}` — returns the influencer record.
  404 if missing; 401/403 via the existing `authenticate()` gate for
  non-staff.
- `PATCH /admin-portal/influencers/{id}` — body may include any subset of
  `city_preference` (`string[]`), `accepts_paid` (`boolean`),
  `accepts_barter` (`boolean`), `min_visit_payment` (`number`),
  `staff_rating` (`1`–`5`), `collaboration_count` (`integer >= 0`).
  400 with a field-specific message on a failed validation (rating out of
  range, negative count); 401/403 same as GET.

## Alternatives considered

**Add a third `text[]` column (`preferred_campaign_types`) instead of
extending the existing boolean.** This was the original (pre-correction)
plan. Rejected once `Influencers.tsx` was read: it would create two
sources of truth for the same concept (`barter_visit` and a new array),
and every existing reader of `barter_visit` would need to either be
migrated anyway or left silently inconsistent with the new field —
strictly worse than extending the one that's already live everywhere this
concept is used.

**Drop `barter_visit` in this same migration.** Rejected — this repo's
usage is fully accounted for, but `aiorders-api` (a separate repo, not
re-checked exhaustively for this specific column) might still read it;
confirming that is a five-minute check for whoever builds this, not worth
blocking or guessing on here.

## One-way doors

None. Two new nullable/defaulted columns, a backward-compatible backfill
of a third, reuse of an existing auth gate, no new vendor, no new
datastore, no public contract change.

## Risks

- **Untracked base schema** for `influencers` (no `CREATE TABLE` in any
  migration) — mitigated the same way as the original draft: verify the
  live schema (`supabase db pull` or dashboard) before writing the
  migration, don't assume this design's column list is exhaustive of
  what's already there.
- **`barter_visit` may have other readers outside this repo** — flagged
  above; the fix (leave the old column in place, additive-only) makes this
  low-severity even if an unchecked reader exists, since nothing here
  changes what `barter_visit` returns.
- **`city_preference` free-text entries may already be inconsistently
  cased/spelled** in production data (e.g. "Vancouver" vs "vancouver") —
  this ticket doesn't need to clean that up (it's an edit control on an
  existing field, not a matching engine), but item 2 (influencer-facing
  region matching) will need to normalize before comparing, same risk the
  pre-correction draft already flagged.

## Rollout

Straight. Additive migration + backward-compatible backfill, new handler,
edit form added to an existing dialog. Rollback: drop the three new
columns; `barter_visit` and every existing display path are untouched
throughout, so rollback risk is limited to the new edit capability itself.

## Out of scope

Item 2 (influencer-facing gating) and `ENG-009` (engagement) — separate
tickets. `ENG-009`'s own premise should be revisited the same way this
one was before its design is written: `engagement`/`followers`/
`*_growth` already exist and are already displayed on this same page,
same as `city_preference` and `barter_visit` were — see the note left on
`ENG-009`'s own ticket file. Dropping the legacy `barter_visit` column
once every reader is confirmed — not this ticket's problem to solve, named
above so it isn't lost.
