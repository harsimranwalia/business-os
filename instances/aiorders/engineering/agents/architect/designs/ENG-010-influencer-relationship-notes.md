---
ticket: ENG-010
project: aiorders-admin-hub
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Influencer relationship notes — technical design

## Correction, stated plainly rather than buried

This ticket's own file (`## Notes`) names the central risk as "influencers
hold real AIOrders accounts (`user_id` on the influencer record, per
`ENG-008`'s own design evidence)." Checked directly: `ENG-008`'s design doc
never mentions `user_id`, and `influencers` has no such column in any
evidence read for either ticket. The risk itself is real, confirmed by
different evidence than cited: `supabase/migrations/
20250729143357_initial_restaurant_rls.sql` shows `role = 'influencer'` is
a real value the new-user trigger assigns on `profiles` ("default to
influencer for security"), and `admin-portal/handlers/users.ts` separately
filters "pure influencers (`role='influencer'`... )" out of a staff
listing — so influencers authenticate as ordinary `profiles` rows with
`role: 'influencer'`, the same table and mechanism staff use, not a
separate column on `influencers` itself. Same underlying conclusion the
ticket already reached (a real authenticated influencer identity exists,
so this must never be influencer-readable), reached here from evidence
that actually checks out. Recorded in `observations.md` as a second
unverified-citation finding this pass, alongside `ENG-009`'s missing
cross-reference note.

## Approach

New, isolated table (`influencer_notes`) and a new, dedicated handler —
not an extension of `ENG-008`/`ENG-009`'s planned `influencers.ts`, since
notes are an independently-growing sub-resource (list + append, no
field-level PATCH) with their own authorization boundary, not another
field on the influencer record itself.

**The authorization boundary is narrower than "reuse the existing
admin-portal gate" by itself would give you, and that gap is the one
finding worth designing around.** `admin-portal`'s router-level
`authenticate()` allowlists `admin`, `sub-admin`, `partner-admin`,
`partner-user` for *every* route under it (`admin-portal/index.ts` line
94) — `partner-admin`/`partner-user` read as agency/reseller roles (the
same roles `ENG-015`, elsewhere on this board, is about scoping). This
ticket's own PRD already decided brand/agency/reseller visibility
defaults to **no** ("Assumed... Defaults to AIOrders-staff-only until you
say otherwise") — a decision already made at G1, not reopened here. Simply
reusing the router's blanket gate would silently grant `partner-admin`/
`partner-user` read/write access to internal staff commentary about a
person, contradicting that default. So the new handler adds a **second,
narrower check inside itself**, on top of the router's base
authentication: `profile.role` (or any `additional_roles` entry) must be
`admin` or `sub-admin` specifically. This is defense-in-depth, not a
change to the shared gate — every other route under `admin-portal` is
unaffected.

**Negative case, stated as a concrete rule rather than left implicit:**
`influencer` is not in the router's own allowlist at all (confirmed,
`admin-portal/index.ts` line 94), so an influencer's own authenticated
session is rejected before reaching *any* handler under this function,
including this one — the central risk this ticket names is closed by the
router itself, before this ticket's own extra `admin`/`sub-admin` check
ever runs. Both layers are still specified explicitly below rather than
assumed, since a future change to the router's allowlist should not
silently reopen this.

## Evidence read before designing

`aiorders-api`: `admin-portal/index.ts` — `authenticate()` (lines 27–115)
reads `profiles.role, additional_roles` (line 78), allowlists exactly
`['admin', 'sub-admin', 'partner-admin', 'partner-user']` (line 94),
applied once for the whole router (line 216) before any handler runs.
`admin-portal/handlers/users.ts` — confirms `profiles` carries `id, email,
name, first_name, last_name, role, additional_roles, phone, location,
created_at` (lines 183–194), giving a real display-name field for note
authorship. No existing `notes`, `influencer_notes`, or generic
polymorphic notes table found anywhere in `aiorders-api` (grepped
migrations and function directories for "notes" — no hit). No migration
creates `influencers` itself (same untracked-base-schema gap every other
ticket on this board touching this table has already found) — not
blocking, since this design only adds a new table with a foreign key
into it, which needs the referenced table to exist live, not to have a
tracked `CREATE TABLE`.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/migrations/{ts}_influencer_notes.sql` | new — `influencer_notes` table | database |
| `supabase/functions/admin-portal/handlers/influencer-notes.ts` | new — GET (list) / POST (create), admin/sub-admin only | backend |
| `supabase/functions/admin-portal/index.ts` | modify — route `influencer-notes` to the new handler (same pattern as `handleLoyaltyConfig`, `handleFoodswipe`) | backend |
| `src/pages/Influencers.tsx` | modify — add a "Notes" section to the existing detail dialog: chronological list (newest first, author + timestamp) and an add-note form | frontend |

## Data

```sql
create table influencer_notes (
  id uuid primary key default gen_random_uuid(),
  influencer_id uuid not null references influencers(id),
  author_id uuid not null references profiles(id),
  body text not null,
  created_at timestamptz not null default now()
);

create index influencer_notes_influencer_id_idx on influencer_notes(influencer_id, created_at desc);
```

No `updated_at`, no soft-delete column — the product requirement is
strictly append-only (AC3: "nothing is overwritten or removed"); adding
edit/delete plumbing that the acceptance criteria explicitly excludes
would be building past the spec. `author_id` is a hard foreign key, never
a free-text name — the display name is resolved at read time by joining
`profiles`, same "fetch separately, map by id" pattern
`influencer-invitations.ts` already uses for its own influencer join,
rather than denormalizing a name that could drift from a later profile
edit.

## Interfaces

New handler, same router, same base `authenticate()` plus the
narrower in-handler check described in Approach:

- `GET /admin-portal/influencer-notes?influencer_id={id}` — 403 unless
  `profile.role`/`additional_roles` includes `admin` or `sub-admin`.
  Returns every note for that influencer, newest first, each with
  `body`, `created_at`, and the author's resolved `name` (falling back to
  `first_name`/`last_name` if `name` is null — verify which is
  authoritative at build time). 404 if `influencer_id` doesn't exist.
- `POST /admin-portal/influencer-notes` — same authorization. Body:
  `{ influencer_id, body }`. `author_id` is **always** taken from the
  authenticated session (`authResult.user.id`), never accepted from the
  request body — the negative case worth stating explicitly: a
  client-supplied author id would let one staff member post a note
  attributed to another. 400 if `body` is empty or `influencer_id` is
  missing/doesn't exist.

No PATCH, no DELETE — not a gap, the acceptance criteria and non-goals
both rule them out (see Data).

## Alternatives considered

**A generic, polymorphic `notes` table** (`target_type`/`target_id`,
reusable for restaurants, campaigns, etc. later). Rejected for this
ticket — nothing else in this codebase has a notes concept yet (confirmed
absent, see Evidence), so a generic shape would be designed against
guessed future callers rather than the one real one; `ENG-010`'s own PRD
scopes this to influencers only. A generic table is a reasonable future
refactor once a second caller actually exists, not a reason to
over-generalize the first one.

**Reuse the router's blanket `authenticate()` alone, no extra check.**
Rejected — see Approach; would grant `partner-admin`/`partner-user` access
the PRD's own default explicitly excludes.

## One-way doors

None. A new, isolated table with no existing reader and no data migrated
into it — reversible by `DROP TABLE` with zero blast radius on anything
else. No change to any existing table, endpoint, or the router's own
shared gate (the narrower check lives inside the new handler only).

## Risks

- **The one this ticket can't get wrong, closed by two independent
  layers** (see Approach) — worth a negative-authorization test at QA
  specifically simulating a `role: 'influencer'` session against both
  `GET` and `POST`, not just a staff-happy-path test.
- **`partner-admin`/`partner-user` visibility** — resolved to "no" here
  per the PRD's own stated default; if the approver actually wants
  agency/reseller staff to see these notes, that's a scope change to this
  already-approved ticket, not something to silently widen later.
- **Note content is freeform text about a real, identifiable person** —
  no deletion path exists in this design (see Data — intentional, matches
  the accumulate-only requirement). If a legal/privacy deletion request
  ever applies to a specific note, that's a manual DB operation today, not
  a product feature; worth flagging to the approver only if it actually
  comes up, not designed for speculatively.

## Rollout

Straight. One new table, one new handler, one new route registration, one
new UI section. Rollback: drop the table and the route; nothing else in
the codebase reads or writes it.

## Out of scope

Editing/deleting any note (including your own); structured/typed
categories; brand/agency/reseller visibility (defaults to no); search over
note contents; notifications or mentions.
