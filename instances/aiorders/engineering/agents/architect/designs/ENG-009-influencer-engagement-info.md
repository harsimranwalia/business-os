---
ticket: ENG-009
project: aiorders-admin-hub
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Influencer engagement info — technical design

## Correction, stated plainly rather than buried

`ENG-008`'s design doc closed with a lead for this ticket: that
`engagement` / `followers` / `followers_growth` / `engagement_growth`
"already exist and are already displayed on this same page, same as
`city_preference` and `barter_visit` were" — implying `ENG-009` would
shrink the same way `ENG-008` did, into a pure edit-path gap.

**That lead is half right, and the wrong half matters.** The four columns
do exist and are displayed. But unlike `city_preference` and
`barter_visit`, they hold **no data at all**. Queried against live
production this pass: all **306** influencer rows have `followers = 0`,
`engagement = 0`, `followers_growth = 0`, `engagement_growth = 0` — not
null, but every single row sitting on its `DEFAULT 0`. Nothing in either
repo on this host writes them. The board's "Followers" and "Engagement"
columns render `0` and `0.0%` for all 306 influencers today, and the "Avg
Followers" / "Top Engagement" stat cards are showing `0` to staff right
now.

Two consequences, in opposite directions:

- **Reading B shrinks, but for a different reason than `ENG-008` gave.**
  These are not fields with real meaning that merely lack an edit control
  — they are empty, unwired columns of the right type and the right
  display path. That makes them a *better* reuse target, not a worse one:
  no backfill, no existing meaning to collide with, no display code to
  write. Adding new `social_followers` / `social_engagement` columns
  beside four zeroed ones would be the duplicate-column mistake this
  design exists to avoid.
- **The real follower data is in a column nobody on this page reads.**
  `influencers.follower_count` — a *separate*, `text` column — is
  populated for **229 of 306** rows, and it is the one the live
  restaurant-facing code actually selects
  (`restaurant-influencer-campaigns/handlers/influencer-invitations.ts:97`).
  It holds self-reported signup bands, not numbers: `1k-10k` (136),
  `10k-50k` (34), `2,000-10,000` (29), `10,000` (16), `Less Than 2000`
  (6), `50k-100k` (6), `100k-500k` (2) — two generations of dropdown
  vocabulary mixed together.

Reading A shrinks not at all: **no internal activity measure exists in any
form.** It is designed fresh below, from the one internal ledger that is
actually populated.

## Approach

Two readings, two different mechanisms, deliberately not merged.

**Reading B — staff-entered social figure.** Reuse the existing, empty
`followers` (`integer`) and `engagement` (`numeric`) columns rather than
adding new ones. They already have the right types, the right table
column, the right detail-dialog field, and the board's existing
`ORDER BY followers DESC` sort. The only genuinely new column is a
timestamp, `social_stats_updated_at`, because acceptance criterion 4 asks
when *the social figure* was last updated and the table-wide
`influencers.updated_at` cannot answer that — `ENG-008`'s edit form bumps
it too. Add the fields to the edit form `ENG-008` is already building.

**Reading A — internal activity signal.** Derived, computed on read,
never stored — the PRD's own non-goal. Source is
`influencer_invitations`, the only populated internal ledger:
809 rows across 138 distinct influencers, live from 2025-05-16 to
2026-08-22. It **must** be aggregated server-side with the service-role
client: `influencer_invitations` has no staff/admin `SELECT` policy (only
influencer-sees-own and restaurant-owner-sees-theirs), so the admin hub's
anon-key client would silently read **zero rows**. This is a hard
constraint, not a preference.

Both readings land on the `admin-portal/handlers/influencers.ts` endpoint
`ENG-008` is already creating, and on the edit form `ENG-008` is already
adding — this ticket extends both rather than building a second of either.

## Evidence read before designing

**Live production schema and data** (project `bmnmnejwdxbcqinqkwko`,
`foodswipe-love`, the ref matching the anon key in
`src/config/constants.ts`) — read-only queries, the credential gap
`ENG-008` recorded no longer applies:

- `influencers`: 306 rows. `followers integer DEFAULT 0`,
  `engagement numeric DEFAULT 0`, `followers_growth numeric DEFAULT 0`,
  `engagement_growth numeric DEFAULT 0` — **all four are non-null and
  zero on all 306 rows.** `follower_count text` (no default) is populated
  on 229. `updated_at timestamptz DEFAULT now()` exists but is table-wide.
  There is **no** activity, collaboration, rating, or response column of
  any kind.
- `influencer_invitations`: 809 rows, 138 distinct influencers.
  Status vocabulary is exactly `pending` (634 rows / 127 influencers),
  `scheduled` (173 / 71, all 173 carrying a `scheduled_visit`), `rejected`
  (2). There is **no `completed` status** — a finished collaboration is a
  `scheduled` row whose `scheduled_visit` has passed.
- Distribution across the 306 influencers: 168 with zero invitations, 83
  with 1–4, 49 with 5–19, 6 with 20+ (max 41, mean 2.64); 71 have at
  least one scheduled visit; 47 saw invitation activity in the last 90
  days. The signal genuinely discriminates rather than collapsing to one
  value.
- `influencer_campaigns` (196 rows) has **`restaurant_id` but no
  `influencer_id`** — campaigns are restaurant-owned postings.
  "Campaigns applied to" is therefore *not* directly representable; the
  influencer↔campaign link runs through `influencer_invitations`. The
  admin page's existing `influencer_campaigns` fetch can only ever produce
  the global count it already shows, never a per-influencer number.
- `matches`, `reviews`, `conversations` all carry an `influencer_id` and
  are all **empty (0 rows)** — and `matches.influencer_id` /
  `reviews.influencer_id` are FK'd to `profiles`, not `influencers`. Dead
  ends; a design sourcing activity from them would render nothing.
- RLS: `influencer_invitations` has `SELECT` policies only for
  influencer-sees-own and restaurant-owner/manager-sees-theirs — **no
  staff/admin policy.** `influencers` has `SELECT` `USING (true)` (so the
  board's read works) and, separately, `UPDATE` to `authenticated` with
  `USING (true)` — see Risks.
- `auth.users`: 242 of 306 influencers have a linked `user_id`, all 242
  have a `last_sign_in_at`, 27 signed in within 30 days.

**`aiorders-api`** (`origin/main`): `admin-portal/handlers/influencers.ts`
**does not exist yet** — it is still only `ENG-008`'s plan; the handler
directory holds `activation`, `auth`, `billing`, `brands`, `foodswipe`,
`leads`, `partners`, `restaurants`, `users`. `admin-portal/index.ts`
carries the `profiles.role`/`additional_roles` gate this ticket reuses
(allowed roles `admin`, `sub-admin`, `partner-admin`, `partner-user`) and
exposes both an anon-key `supabase` and a service-role `adminSupabase` to
every handler. Its CORS `Access-Control-Allow-Methods` is
`'GET, POST, PUT, DELETE, OPTIONS'` — **no `PATCH`** — and every existing
handler branches on `GET`/`POST`/`PUT`/`DELETE`. Grepping the whole
functions tree, **nothing reads or writes `influencers.followers` or
`influencers.engagement`**; the only `followers` hit is
`influencer_campaigns.min_followers`, a campaign eligibility threshold.
The one existing notion of influencer activity is
`outgoing-communications/actors/influencers.ts` →
`scheduled_inactivity_emails`, which defines inactive as
`auth.users.last_sign_in_at` older than 30 days and records sends in
`influencers.inactivity_reminders_sent`.

**`aiorders-admin-hub`**: `src/pages/Influencers.tsx` (394 lines, read in
full). Its `Influencer` interface declares the four fields verbatim as
`followers: number; engagement: number; followers_growth: number;
engagement_growth: number;`. The page fetches `select('*')` ordered by
`followers` descending, renders `followers` through a K/M `formatNumber`
in the table and dialog, renders `engagement` as
`{(influencer.engagement || 0).toFixed(1)}%` in both — i.e. `engagement`
is a **percentage rate**, not a count — and shows `*_growth` only when
`> 0`, so today they are invisible. `follower_count` is not referenced
anywhere in the admin hub outside the generated types. Confirming
`ENG-008`: nothing on the page is editable. The house pattern for calling
this API is a `fetch` to `${SUPABASE_CONFIG.URL}${API_ENDPOINTS...}` with
a `Bearer` session token (`FoodswipeListings.tsx:207-223`), paths
centralised in `src/config/constants.ts`.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/migrations/{ts}_influencer_social_stats.sql` | new — one required column (`social_stats_updated_at`), one optional (`social_stats_platform`); no change to `followers`/`engagement`/`follower_count` | database |
| `supabase/functions/admin-portal/handlers/influencers.ts` | **modify** — extend `ENG-008`'s handler: add the invitation aggregate to `GET`, accept the social fields on write and stamp the timestamp | backend |
| `supabase/functions/admin-portal/index.ts` | no change — `ENG-008` already routes `influencers` | backend |
| `src/pages/Influencers.tsx` | **modify** — extend `ENG-008`'s edit form with followers/engagement/platform; add an activity block to the detail dialog and an activity cell to the table; show "Not set" instead of `0`; show `follower_count` as read-only context | frontend |
| `src/config/constants.ts` | modify — add the `INFLUENCERS_*` endpoint paths if `ENG-008` has not | frontend |

**Component dependency on `ENG-008` (not a ticket `depends_on`).** Every
row above marked *modify* assumes `ENG-008` has landed: it creates
`handlers/influencers.ts`, its routing, and the detail-dialog edit form.
This ticket adds fields to that one form and that one handler — it must
not create a second edit form or a second endpoint. If the EM's
sequencing ever inverts, this ticket inherits `ENG-008`'s handler-and-form
creation and grows from `S` to roughly `ENG-008`'s own size; that is a
re-estimate, not a redesign.

**Cross-ticket finding for the EM, not a unilateral change.** `ENG-008`
plans a stored `collaboration_count integer NOT NULL DEFAULT 0` as a
staff-maintained field. This design derives a true collaboration count
from `influencer_invitations` exactly, on read, for free. Two numbers
called "collaborations" — one hand-typed, one computed, disagreeing — is
the duplicate-source-of-truth problem `ENG-008` itself rejected elsewhere.
Recommendation: drop `collaboration_count` from `ENG-008`, or keep it
only if it is explicitly relabelled an off-platform tally. **The EM's and
PM's call; this design does not assume either outcome** — nothing here
reads or writes that column.

## Data

**Reused, no schema change:**

- `followers` (`integer`, `DEFAULT 0`, all 306 rows zero) — becomes the
  staff-entered follower count. Already displayed, already sorted on.
- `engagement` (`numeric`, `DEFAULT 0`, all 306 rows zero) — becomes the
  staff-entered engagement rate, as a percentage, matching the existing
  `.toFixed(1)%` render.
- `follower_count` (`text`, 229 populated) — **read-only, never written
  by this ticket.** It is influencer self-reported signup data and the
  restaurant-facing invitation UI depends on it. Surfaced in the dialog
  as labelled context ("self-reported at signup") so staff entering a
  verified number can see what the influencer claimed.
- `followers_growth` / `engagement_growth` — untouched. Both are empty,
  neither is asked for by any acceptance criterion, and a growth figure
  is meaningless without the value history the PRD explicitly excludes.

**New:**

- `social_stats_updated_at` (`timestamptz`, nullable, no default) —
  required by AC4. Stamped by the handler on any write that changes
  `followers` or `engagement`. Also the authoritative "has staff ever set
  this?" marker: since all 306 rows are `0` rather than `NULL`, a zero
  alone cannot distinguish "not set" from "genuinely zero", and
  `NULL` here means never entered. The UI renders "Not set" in that case
  rather than a misleading `0` / `0.0%`.
- `social_stats_platform` (`text`, nullable) — satisfies the PRD's stated
  assumption that "staff can label which platform a figure refers to."
  **No acceptance criterion requires it**; it is one nullable column and
  one form control, included because four handle columns (`ig_handle`,
  `tiktok`, `youtube`, `x`) already exist and an unlabelled number
  between them is ambiguous. Cheap to drop if the PM would rather not
  have it — nothing else depends on it.

Both are additive and nullable. No backfill, no default, no existing
reader affected. The migration must be written idempotently
(`ADD COLUMN IF NOT EXISTS`) — `influencers` has no `CREATE TABLE` in any
tracked migration, so the migration file is the first tracked statement
that will ever touch this table.

**Derived, stored nowhere** (Reading A), per influencer, from
`influencer_invitations`:

- `invitations` — `count(*)`
- `visits` — `count(*) filter (where status = 'scheduled')`
- `completed_visits` — as above, additionally `scheduled_visit < now()`
- `responded` — `count(*) filter (where status <> 'pending')`, and the
  rate over `invitations`
- `last_activity_at` — `max(created)`

## Interfaces

`admin-portal`, extending `ENG-008`'s handler. **`PUT`, not `PATCH`** —
`PATCH` is absent from the function's `Access-Control-Allow-Methods`, so
a browser preflight would fail before the handler ever ran, and no
existing handler uses it. `ENG-008`'s design specifies `PATCH`; whichever
ticket lands first should settle on `PUT` or widen the CORS header, and
this design assumes `PUT`.

- `GET /admin-portal/influencers` — returns the influencer list, each
  record additionally carrying:

  ```
  activity: {
    invitations: number,
    visits: number,
    completed_visits: number,
    responded: number,
    response_rate: number | null,   // null when invitations === 0
    last_activity_at: string | null
  } | null
  ```

  Computed with the service-role `adminSupabase` client (RLS blocks the
  anon client entirely). Two queries, merged in memory — the influencer
  rows, and one grouped aggregate over `influencer_invitations` — never
  one query per influencer. At 306 influencers and 809 invitations this
  is trivial, and it matches the two-query-then-merge shape
  `influencer-invitations.ts` already uses.

- `PUT /admin-portal/influencers` — body `{ id, ...fields }`, id in the
  body to match the house pattern (`RESTAURANT_UPDATE` and
  `BILLING_UPDATE` are both bare paths). This ticket adds three accepted
  fields to `ENG-008`'s set: `followers` (`integer`, `0 ≤ n ≤ 1e9`),
  `engagement` (`numeric`, `0 ≤ n ≤ 100` — it is a percentage), and
  `social_stats_platform` (`text`, trimmed, max 32 chars, nullable).
  When either numeric field is present and changed, the handler sets
  `social_stats_updated_at = now()` server-side; the client never sends
  that timestamp. 400 with a field-specific message on failed
  validation; 401/403 via the existing `authenticate()` gate.

**Failure behaviour.** If the aggregate query fails, the handler returns
the influencer list with `activity: null` and logs — a broken activity
signal degrades one dialog block to "—", it does not blank the whole
board. If the influencer query fails, the request fails as it does today.
On write, the update is a single-row scalar write: last write wins,
which is acceptable for a hand-maintained figure, and
`social_stats_updated_at` makes a stale value visible rather than silent.
No retry, no idempotency key — the write is naturally idempotent.

## Alternatives considered

**Add new `social_followers` / `social_engagement` columns and leave the
zeroed ones alone.** Rejected. It would leave four dead columns wired to
the table's own "Followers" and "Engagement" columns and to both stat
cards, so the board would show a real number in one place and `0` in
another for the same influencer. Reusing the empty columns costs one
migration line less and makes the existing display and sort correct for
free.

**Overwrite `follower_count` with the staff-entered number.** Rejected.
It is `text`, holds self-reported bands in two vocabularies, is populated
on 229 rows, and is read by the restaurant-facing invitation UI in
another repo. Writing a precise staff figure into it would destroy the
influencer's own answer and change what restaurants see, to satisfy a
requirement that never asked for either.

**Backfill `followers` from `follower_count`'s bands.** Rejected as
fabrication. `1k-10k` does not carry an integer, and inventing one (a
midpoint, say) would produce 136 identical fake follower counts that
staff could not distinguish from entered values. Leave `followers` empty
until a human types a real number; `social_stats_updated_at IS NULL`
tells the UI exactly that.

**Reuse the existing table-wide `influencers.updated_at` for AC4.**
Rejected. `ENG-008`'s edit form writes `city_preference`, `staff_rating`
and payment flags to the same row, and any of those would bump
`updated_at` — the board would then claim the social figure was refreshed
on a day nobody touched it. AC4 needs a field-specific timestamp; that is
the one column here that genuinely cannot be avoided.

**Source Reading A from `matches` / `reviews` / `conversations`.**
Rejected on evidence: all three are empty, and two of them FK
`influencer_id` to `profiles` rather than `influencers`. The design would
have rendered nothing for all 306 influencers.

**Source Reading A from `auth.users.last_sign_in_at`,** reusing the
30-day definition the inactivity mailer already applies. Rejected as the
primary measure — a login says the influencer opened the app, not that
they are active *with restaurants*, and it covers only the 242 rows with
a linked `user_id`. `last_activity_at` from the invitation ledger answers
the same question with better fidelity and full coverage. Worth revisiting
only if staff ask for "last seen" specifically.

**Store the activity signal in a column, refreshed on a schedule.**
Rejected — the PRD names computed-on-read as sufficient, and at this data
volume a cron job would add a staleness window and a failure mode in
exchange for nothing.

**Reduce the activity counts to a single banded label (Active /
Occasional / Dormant).** Rejected. It is more scannable, but the
thresholds are a product judgment the PRD did not delegate — it delegated
*which underlying measure*, not *what counts as active*. Raw counts plus
a last-activity date satisfy AC1 without inventing a cutoff. If staff ask
for a band later, the thresholds should come from the PM.

## One-way doors

None. Two nullable additive columns, no backfill and no destructive
change to any populated column, a derived read stored nowhere, reuse of
the existing admin-auth gate and the existing handler, no new vendor, no
new datastore, no public contract change. Rollback is dropping two
columns and reverting the display; `follower_count`, `barter_visit` and
every current display path are untouched throughout.

## Risks

- **`influencers` is writable by any authenticated user.** The live
  policy is `UPDATE` to role `authenticated` with `USING (true)` — every
  logged-in influencer and restaurant user can update every influencer
  row, including these fields. **Pre-existing, not introduced here**, and
  not this ticket's to fix, but it means the staff-only edit path this
  design adds is staff-only by routing, not by enforcement. Filing as a
  tech-debt intake card with the EM separately; whoever builds this
  should not be surprised by it, and should not "fix" it inside this
  ticket.
- **Reused columns could acquire a second writer.** `followers` and
  `engagement` are unwritten by anything in either repo on this host, but
  the influencer-facing FoodSwipe client is not on this host and was not
  read. If it ever writes them, a staff-entered figure could be silently
  overwritten. Low likelihood given all 306 rows are still on their
  default after 16 months of data, and `social_stats_updated_at` would
  make the overwrite visible rather than silent. A five-minute grep of
  that client before building is worth it.
- **The invitation ledger under-describes finished work.** With no
  `completed` status, `completed_visits` infers completion from a past
  `scheduled_visit` — an influencer who no-showed still counts. Honest
  labelling in the UI ("visits scheduled", not "visits delivered") is the
  mitigation; a real completion state is a different ticket.
- **634 of 809 invitations are `pending`,** so response rate will read
  low across the board and mostly reflects restaurants inviting in bulk
  rather than influencers ignoring them. Display it next to the raw
  counts, never alone, so staff can see the denominator.
- **`follower_count`'s two dropdown vocabularies** (`Less Than 2000` vs
  `1k-10k`) will look inconsistent in the dialog. Displayed verbatim as
  self-reported context, not parsed, not normalised — cleaning it up is
  neither required here nor safe to do while restaurants read it.

## Rollout

Straight. Additive migration, extensions to a handler and a form
`ENG-008` has already created, no data migration and no backfill. Ship
behind no flag — the new fields render as "Not set" until a staff member
enters one, which is the correct empty state rather than a regression.
Rollback: drop the two new columns and revert the display; the board
returns to showing `0`, exactly as it does today.

## Out of scope

The Meta/Instagram/TikTok API connection, deferred in the approver's own
words — when it is built, it should write `followers`/`engagement` and
stamp `social_stats_updated_at` the same way a human does, so this
ticket's field is the thing it takes over rather than a field it
replaces. Any history or timeline of past social figures. OAuth or
influencer-side account connection. Normalising `follower_count`'s band
vocabulary, or migrating it into a numeric column. Tightening the
`USING (true)` update policy on `influencers` — filed separately with the
EM, named here so it is not lost. `followers_growth` and
`engagement_growth`, which stay empty and undisplayed. Resolving
`ENG-008`'s `collaboration_count` against the derived count above — flagged
for the EM under Components, decided by the EM and PM, not here.
