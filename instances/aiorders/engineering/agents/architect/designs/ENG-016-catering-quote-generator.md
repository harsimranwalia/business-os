---
ticket: ENG-016
project: config-site-builder
author: architect
created: 2026-09-03
adrs: [ADR-008, ADR-009]
one_way_doors: []
touches_data: true
touches_models: false
---

# Catering page — structured order capture and automatic stage update (Piece 1) — technical design

## Approach

Piece 1 is additive everywhere. The public catering form keeps its existing
fields, its existing `delivery_method` control and its existing single-POST
submission to `catering-request`; it gains a category-grouped dish picker
between the fulfillment control and the submit row, a second submit action
("Skip & Have Someone Contact Me"), and two new optional fields on the payload.
`catering-request` gains two nullable columns to store them and one line of
server-derived `status`. `restaurant-portal` gains two strings in each of the
places its five status strings are already hardcoded, plus one read-only
rendering block in the detail modal.

Two things drive that shape rather than the more obvious one.

**No new datastore surface, because the read path already returns whatever we
add.** `brand-portal/catering.ts`'s `get_catering_requests` is a `select('*')`
behind `verifyRestaurantAccess`, and `public.catering` already carries real
row-scoped RLS policies (`20250729143357_initial_restaurant_rls.sql`). Two
nullable columns on that table are therefore visible to the owner, and refused
to everyone else, with **zero new authorization code and zero new endpoint** —
which is how AC-13 is satisfied here (see Interfaces). A child
`catering_selections` table would have needed its own policies, its own join,
and a change to that handler; it buys nothing, because selections are only ever
read with their parent row.

**The two new pipeline stages are the risky part, not the new data.** The
kanban builds its columns from a hardcoded `columns` array and groups requests
by filtering on it — a request whose `status` is not in that array is **not
rendered at all**, and the adjacent `statusConfig[status].borderColor` lookup is
unguarded, so a column string with no config entry throws and takes the board
down. That makes deploy order a correctness requirement, not a preference (see
Rollout), and it makes "both hardcoded copies in the same file, in the same
commit" a rule rather than a tidiness note.

The design deliberately does **not** introduce a fulfillment-value remap or a
second fulfillment field (ADR-008), and gates the whole feature behind an
explicit owner opt-in that defaults off (ADR-009).

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api`: `supabase/migrations/<ts>_add_order_capture_to_catering.sql` | new — two nullable columns on `public.catering` (see Data) | database |
| `aiorders-api`: `supabase/functions/catering-request/index.ts` | modify — destructure + validate `action_type`/`selections`, derive `status` server-side, include both in the INSERT | backend |
| `aiorders-api`: `supabase/functions/brand-portal/website.ts` | modify — extend the `CateringPageContent` interface with the two new keys. **Type documentation only**: `updateWebsiteContent` writes `content[page]` opaquely, so no behaviour changes | backend |
| `aiorders-api`: `supabase/functions/brand-portal/catering.ts` | **no change** — `get_catering_requests` is `select('*')`; the new columns are returned already. Listed so nobody "adds" them | — |
| `config-site-builder`: `src/types/restaurant.ts` | modify — extend `CateringPageContent` with `orderFormEnabled` and `fulfillmentCopy` | frontend |
| `config-site-builder`: `src/components/CateringMenuSelector.tsx` | new — category-grouped dish picker (quantity + per-dish note), controlled, no fetch of its own | frontend |
| `config-site-builder`: `src/components/CateringForm.tsx` | modify — gate, per-option copy, conditional email requirement, selector mount, second submit action, payload fields | frontend |
| `restaurant-portal`: `src/components/catering/CateringKanban.tsx` | modify — **both** copies: `columns` and `statusConfig` | frontend |
| `restaurant-portal`: `src/components/catering/CateringDetailModal.tsx` | modify — **both** copies (`statusConfig`, `statusOptions`), plus the itemized-selections block and the three new interface fields (AC-12) | frontend |
| `restaurant-portal`: `src/components/catering/StatusUpdateModal.tsx` | modify — `statusOptions` | frontend |
| `restaurant-portal`: `src/components/catering/ArchivedCateringModal.tsx` | modify — `statusConfig` | frontend |
| `restaurant-portal`: `src/components/catering/CateringForm.tsx` | modify — `statusOptions` only. The two `'New Enquiry'` literals are *defaults for a new record*, not a list; they stay | frontend |
| `restaurant-portal`: `src/components/catering/CateringCalendar.tsx` | modify — two `case` arms on `getStatusBadgeColor` | frontend |
| `restaurant-portal`: `src/components/catering/CateringRequestCard.tsx` | modify — two `case` arms on `getStatusBadgeClass` | frontend |
| `restaurant-portal`: `src/pages/catering/Index.tsx` | modify — two `case` arms on `getStatusBadgeColor` | frontend |
| `restaurant-portal`: `src/index.css` | modify — two `.status-*` classes beside the existing five (~line 130) | frontend |
| `restaurant-portal`: `src/components/website/CateringPageForm.tsx` | modify — preserve unknown keys on save (see Risks), add the enable switch and the per-option copy editor | frontend |
| `restaurant-portal`: `src/types/website.ts` | modify — extend its own copy of `CateringPageContent` | frontend |
| `restaurant-portal`: `src/pages/Dashboard.tsx` | **no change** — it declares its own `CateringRequest` interface but renders no status column and needs none of the new fields. Explicitly out of scope | — |

`CateringRequest` is independently declared in **eight** `restaurant-portal`
files (the seven catering files above plus `Dashboard.tsx`); the five status
strings appear in **eight** files as **twelve** separate literals. Neither is
collapsed here — that is the PRD's own non-goal and it overlaps `ENG-013`'s open
stage-config question. Grep each file for its own local copies before editing
it; two of them have two each.

## Data

`touches_data: true`. `database` owns the migration; this section states intent
and constraints only.

**Two nullable columns on the existing `public.catering` table.** No new table,
no constraint on an existing column, no backfill, no change to any existing
column's type or nullability.

| Column | Type | Null | Purpose |
|---|---|---|---|
| `action_type` | `text` | yes | What the customer actually did: `QUOTE_SUBMITTED` or `MANUAL_CONTACT_REQUESTED`. Null for every row written before this ticket and for every caller that doesn't send it |
| `selections` | `jsonb` | yes | The itemized order. Null unless `action_type = 'QUOTE_SUBMITTED'` |

Constraints the migration must satisfy:

- **Nullable, no default, no `NOT NULL`, no `CHECK`, no enum type.** Existing
  rows and existing callers (`restaurant-marketplace`'s own direct insert, the
  GoHighLevel path) must remain valid without touching them — AC-8 and AC-10.
  `action_type` is validated in the edge function, not by the database; a
  `CHECK` constraint would turn a malformed third-party payload into a failed
  insert, which is the wrong failure direction for a public lead form.
- **`add column if not exists`**, matching
  `20260807000001_add_heard_about_us_to_catering.sql` — the only prior additive
  migration against this table, and the template for this one. That file's own
  header states the deploy-order rule this ticket inherits (migration before
  the edge function, or the INSERT fails on a missing column); repeat it.
- **Column comments on both**, same as `heard_about_us`. `selections`' comment
  should carry the element shape, the way
  `20260807000002_add_catering_to_restaurant_website.sql` documents its own
  jsonb shape — this table has no tracked `CREATE TABLE`, so comments are the
  only schema documentation that exists.
- **No index.** `selections` is only ever read via the parent row, and
  `get_catering_requests` already filters on `restaurant_id`/`archived`.
  `action_type` is not queried by anything in this ticket.

**Element shape for `selections`** (an array; AC-5's five fields, no more):

```
[{ "category": "Appetizers",        // category name as displayed at submission
   "item_id": "cQ1IIsOGt4" | null,  // item.id ?? item._id ?? null — both optional in the live type
   "name": "Butter Chicken",        // snapshot; the durable identifier
   "quantity": 2,                   // integer >= 1
   "note": "medium spice" | null }] // AC-4
```

`name` and `category` are snapshots taken at submission. That is the mitigation
for the PRD's dangling-`item_id` risk: `MenuItem.id` and `_id` are *both*
optional in the live type and the menu is a hand-edited JSONB blob, so an owner
who renames or removes a dish after a quote was built must still be able to read
what was ordered. **No price is snapshotted.** Piece 1 shows no price anywhere;
a price column would be the first pricing field in the catering data model and
belongs with Piece 2, where it becomes meaningful. It is cheap to add later —
another nullable key on the same jsonb — and adding it now would be the
speculative half of a decision that hasn't been made.

**Volume and growth.** Bounded by catering submissions per restaurant, which is
a low-hundreds-per-year lead volume, not an event stream. `selections` is capped
at 200 items and 500 characters per note at the boundary (see Interfaces), so
the column's worst case is single-digit KB per row. No partitioning, no
archival, no retention change.

**Not stored anywhere new:** the customer's own free-text notes. AC-5's "and the
customer's own notes" is the existing `requirements` column, which the form
already collects and the detail modal already renders. Adding a second free-text
column beside it would give the owner two boxes to read.

## Interfaces

### `catering-request` — additive request fields

The function is a public, unauthenticated POST (anon key only) and remains so.
It destructures a fixed field list from the body and ignores everything else, so
**every existing caller is unaffected by construction** — the GoHighLevel
`customData` branch and `restaurant-marketplace` (which never calls this
function at all; it does its own direct insert) both keep working with no
change. This is what makes AC-10 structural rather than a promise.

Two new optional body fields:

- `action_type?: 'QUOTE_SUBMITTED' | 'MANUAL_CONTACT_REQUESTED'`
- `selections?: Array<{ category, item_id, name, quantity, note }>`

**Validation, at the boundary, failing closed toward today's behaviour:**

| Input | Behaviour |
|---|---|
| `action_type` absent | Store `null`, omit `status` from the INSERT — the column default (`'New Enquiry'`) applies, exactly as today |
| `action_type` present but not one of the two literals | Same as absent. Store `null`, ignore `selections`, default status. A malformed field never costs a customer their submission |
| `action_type = 'MANUAL_CONTACT_REQUESTED'` | Store it, store `selections` as `null` regardless of what was sent, `status = 'Contact Requested'` |
| `action_type = 'QUOTE_SUBMITTED'`, `selections` valid | Store both, `status = 'Quote Generated'` |
| `selections` not an array, > 200 elements, or any element with a non-positive/non-integer `quantity`, a missing/non-string `name`, or a `note` over 500 chars | **400** `{ error: "Invalid selections" }` with `...corsHeaders` |

Two rules that are load-bearing rather than stylistic:

1. **`status` is derived server-side from `action_type` and is never read from
   the request body.** This endpoint is unauthenticated: a client-supplied
   status would let anyone drop a request straight into `Finalized` or
   `Completed`, skewing the owner's board and the dashboard's `cateringIncome`
   figure. The function does not destructure `status` today, so this preserves
   an existing property rather than adding a guard — but it is the one place
   this ticket lets external input influence a field the owner acts on, so it is
   stated explicitly.
2. **The `if (source == "form" && ...)` required-field branch is not touched.**
   `config-site-builder`'s form sends `source: 'website'`, so that branch does
   not fire for the path this ticket changes; `restaurant-marketplace` sends
   `source: 'form'` but never reaches this function. What the GoHighLevel
   workflow sends is not determinable from the repo. Leaving the branch alone
   makes AC-10 hold regardless of which of those is true, and AC-11's field-level
   blocking is a client-side concern in any case (below).

The new 400 path carries `...corsHeaders`. The function's two **pre-existing**
error returns (invalid restaurant id, insert failure) do not, so a browser sees
a network error rather than the body — a real defect, but pre-existing on every
error path of this function and not created here. Fix what this ticket adds;
file the rest, don't bundle it.

### `config-site-builder` — the gate, and what it gates

```
orderFormEnabled =
     config.catering?.orderFormEnabled === true          // explicit owner opt-in, ADR-009
  && effectiveHasMenu === 'page'                          // structured menu exists
  && effectiveMenu.length > 0
```

`effectiveHasMenu` / `effectiveMenu` resolve **per selected location**:
`selectedLocation?.hasMenu ?? config.hasMenu` and `selectedLocation?.menu ??
config.menu`. `CateringForm` already computes `selectedLocation` from
`formData.restaurant_id` for its `delivery_method` flags; reuse that. This
matters — a multi-location brand can have one location on a page menu and
another on an embedded ordering widget, and `get-brand-website` defaults
`hasMenu` to `'embedded'` when unset, so the qualifying population is narrow
and deliberate.

When the gate is closed, `CateringForm` renders **exactly** what it renders
today: same fields, same required set (email optional, `requirements`
required), same single submit button, same payload with no new keys. AC-9 is
satisfied by not entering the new branch at all, not by a parallel
implementation of the old one.

When the gate is open:

- The `delivery_method` `<select>` is unchanged in values and flag-gating; each
  option's **label** and its **description** come from
  `config.catering.fulfillmentCopy[value]` when present, falling back to
  today's hardcoded labels (ADR-008 explains why this is copy rather than new
  values).
- `number_of_guests` stays visible and required, as today. Its per-option
  **helper note** (`fulfillmentCopy[value].guestCountNote`) appears when the
  selected option has one configured. See "AC-1, read narrowly" below.
- `CateringMenuSelector` renders below the fulfillment row.
- `requirements` loses its `required` attribute — the itemized selections are
  now where order detail goes — and its label becomes general notes. It is
  still sent, still stored in the same column, still rendered in the same place
  in the owner's detail modal.
- `email` becomes required (AC-11). This is a deliberate behaviour change,
  named in the PRD's Risks, and it applies **only** on this branch — a
  not-enabled restaurant keeps accepting phone-only submissions.
- Two submit actions replace one. Both run the same client-side validation over
  `full_name`, `phone`, `email`, `event_date` (plus the fields already
  `required` today) and both block with a field-level message — AC-11's "either
  bottom action" is explicit that the skip path is not a validation bypass.
  "Submit Quote Request" additionally requires at least one selection, with the
  message pointing at the skip action rather than just refusing.

### `CateringMenuSelector` — new component

Props: `{ menu: Menu[]; value: Selection[]; onChange(next: Selection[]): void }`.
No data fetching, no config reads, no submission logic — the menu is already in
the page config, exactly as it is on the menu page.

Reads the menu the way this repo already reads it, in `MenuList.tsx`:
`(menu.categories || []).map(...)` over `((category.items || category.dishes) ||
[])` — **both** field names exist in the live `Menu` type and both occur — with
`isDishHidden` from `src/utils/menuItems.ts` as the visibility filter. A
`no-stock` dish stays selectable, because `MenuList` already lists it and a
catering order is placed weeks ahead; matching the existing rule beats inventing
a second one.

Selection identity is `${menuIndex}-${categoryIndex}-${itemIndex}`, the same
composite key `MenuList` uses for its own keys — **not** the dish name and not
`item.id`. Names repeat across categories and ids are optional; either would
silently merge two different dishes into one line.

### `restaurant-portal` — the two new stages

`'Quote Generated'` and `'Contact Requested'`, appended after `'New Enquiry'`
in the kanban's `columns` (so a new lead sits next to the other new leads) and
added to every `statusConfig` / `statusOptions` / `switch` copy listed in
Components. `catering.status` is plain `text` with a default and no enum,
constraint, or server-side validation — confirmed in
`restaurant-marketplace/README.md` (`status (text, default: 'New Enquiry')`) —
so this is a frontend-only, additive change, and `CateringRequest.status` is
already typed `string` everywhere, so no type changes.

`ArchivedCateringModal` and `CateringDetailModal` index `statusConfig` directly
and render `undefined` as a className if a status is missing; `CateringKanban`
dereferences `.borderColor` off the same lookup and **throws**. Update every
copy in a file together.

The detail modal's itemized block (AC-12) is read-only and additive: a new
conditional section following the same `{request.requirements && (<><Separator
/>…</>)}` shape already used for Requirements, placed between "Event Details"
and "Requirements". One line per selection — quantity, name, note — grouped by
`category`, with the raw stored `name` rendered as-is (never re-resolved against
the current menu, which is the whole point of the snapshot). Fulfillment option
and guest count are already rendered by that modal today and need no work.

**No new write path.** Piece 1's owner side is read-only: there is no "Edit
Quote" (Piece 3). The kanban's drag handler and `StatusUpdateModal` keep sending
only `{ status }` through `brandPortalApi.updateCateringRequest`, and
`CateringDetailModal` keeps writing `{ status }` directly via RLS. Nothing new
is routed through `update_catering_request`.

### AC-13, and why it needs no code

Every read of the new data goes through paths that already exist and are already
scoped:

- `brand-portal/catering.ts` → `verifyRestaurantAccess(restaurant_id, …)` then
  `select('*').eq('restaurant_id', …)`. New columns ride along; a caller without
  access gets `{ success: false, error: 'Access denied' }` before any row is
  read.
- `CateringDetailModal`'s direct `supabase.from('catering')` calls run as the
  authenticated user against the RLS policies in
  `20250729143357_initial_restaurant_rls.sql`, which are **row**-scoped
  (`user_has_restaurant_access(auth.uid(), restaurant_id)`), not column-scoped —
  so they cover columns added after they were written, automatically.

No new table, no new endpoint, no new action, no new write path, no widened
gate. AC-13 is satisfied by construction, and the QA test for it is the existing
cross-tenant read attempt against a row that now carries `selections`.

### AC-1, read narrowly — flagged, not silently absorbed

AC-1 says selecting a per-person/on-site option "reveals a guest-count input
with its helper note." This design keeps `number_of_guests` **always visible and
required**, as it is today, and treats the per-option **helper note** as the
thing that appears.

Reason: `number_of_guests` is required on today's form and is read by the
owner's board and by `get_catering_dashboard_stats`' `cateringIncome`
(`number_of_guests * 34`). Hiding it for pickup/delivery orders would drop that
data for a whole class of requests to satisfy a clause inherited from the
approver's rewrite, where guest count drove per-person *pricing* — and Piece 1
shows no pricing at all, so the per-person framing has no consequence here. The
conditional-reveal version is also strictly more code.

This is a narrowing of AC-1's literal wording, named here so QA tests the right
behaviour and the PM can push back before code rather than after. Everything
else in AC-1 (the fulfillment control, per-option copy, the helper note) is met
as written.

## Alternatives considered

- **A `catering_selections` child table instead of a jsonb column.** Rejected:
  selections are never queried across rows, never aggregated, and never read
  apart from their parent. A table would need its own RLS policies (the one
  thing this design otherwise needs none of), a join in `get_catering_requests`,
  and a second write in a function whose insert is currently a single statement
  with no transaction around it. Every menu-shaped structure in this codebase
  is already jsonb (`restaurant_website.menu`, `.catering`, `.option_sets`);
  this matches it.
- **Remap `catering.delivery_method`'s five values to the rewrite's three, or
  add a second `fulfillment_option` column beside it.** Both rejected — ADR-008.
- **Default the order form on for every restaurant with a structured menu**,
  with an opt-out. Rejected — ADR-009.
- **A structured option-set / modifier picker per dish.** Dishes carry
  `option_sets: string[]` referencing modifier groups in
  `restaurant_website.option_sets`, and a group can be
  `conditions.required: true`. Rejected: no acceptance criterion asks for it;
  AC-4's per-dish free-text note already covers the case, and its own worked
  example ("spice level, dry vs. gravy") is precisely the ubiquitous option set
  `MenuList.tsx` singles out by name today. Building it properly means
  enforcing required groups, min/max option counts, and the per-option `price`
  surcharges those groups carry — which is pricing, i.e. Piece 2. This was not
  in the PRD's evidence; it is named here rather than quietly skipped, and
  carried into Out of scope and Risks.
- **Store a price snapshot alongside each selection**, as the PRD's Risks
  section suggests. Rejected for Piece 1: the dangling-reference risk it names
  is closed by the `name`/`category` snapshot alone (the owner reads a name, not
  an id), price adds nothing to it, and a price field here would be the first
  pricing data in the catering model — Piece 2's territory, and cheap to add
  then.
- **Fix `brand-portal/catering.ts`'s `update_catering_request` allow-list gap**
  while in the file. Rejected: an open, architect-filed proposal already covers
  it (`agents/eng-manager/proposals.md`, 2026-08-29) and it is not approved.
  This design adds no new write through that action, so it does not make the gap
  worse; the new columns do join the set of columns it can overwrite, which is
  noted in Risks.
- **Collapse the twelve hardcoded status literals into one shared constant.**
  Rejected — the PRD's explicit non-goal, overlapping `ENG-013`'s open
  stage-config question. Adding two duplicated strings to a file that already
  duplicates five is matching the codebase, not laziness. No speculative shared
  config layer is introduced in anticipation of that ticket either.

## One-way doors

**None.** Each criterion, checked rather than asserted:

| Criterion | Verdict |
|---|---|
| New datastore | No — two columns on an existing Postgres table |
| New vendor | No — nothing is sent. Run cost stays `$0/month`; no SMS, email, or third-party call is added |
| Auth model change | No — zero new authorization code; existing RLS plus `verifyRestaurantAccess`, both row-scoped and already covering the new columns |
| Public contract break | No — `catering-request` gains two optional fields; the function already ignores undestructured input, so existing callers are unaffected by construction. AC-10 is an acceptance criterion, verified against `restaurant-marketplace`'s and GoHighLevel's actual code paths |
| Data model painful to migrate | No — two nullable columns via `add column if not exists`; reversing is dropping two columns nothing else reads |
| Recurring cost | None |

The closest call is the two new `status` strings becoming live data. Reversing
them costs more than dropping a column — orphaned rows would fall out of the
kanban's `columns` filter and become invisible — but `catering.status` has no
enum or constraint behind it, every list/calendar/card consumer has a `default:`
arm, and the unwind is removing two strings plus a one-line `UPDATE ... SET
status = 'New Enquiry' WHERE status IN (…)`. Moderate, not one-way.

Two reversible decisions are recorded because a future engineer will ask why:
**ADR-008** (fulfillment values) and **ADR-009** (the enablement gate). Neither
is escalated — escalating a reversible decision spends the resource this
department exists to protect. **Route: `ready`, no G2.**

## Risks

- **Deploy order is a correctness requirement, not a preference.**
  `CateringKanban` renders only the statuses in its hardcoded `columns` array,
  so if `catering-request` starts writing `Quote Generated` before
  `restaurant-portal` ships, every new catering lead is invisible on the owner's
  board — the exact opposite of the ticket's purpose, and silent. Closed by the
  ordering in Rollout, which is also the ordering
  `20260807000001_add_heard_about_us_to_catering.sql` already documents for this
  same pair of components.
- **`CateringKanban`'s `statusConfig` lookup is unguarded.** A `columns` entry
  with no `statusConfig` entry throws on `.borderColor` and takes the whole
  board down. Both copies change in the same commit; a partial edit is a P1, not
  a cosmetic miss.
- **`restaurant-portal`'s catering editor replaces the whole `catering` jsonb
  object on save.** `CateringPageForm` re-initialises its state from an explicit
  field list and `updateWebsiteContent` does `.update({ catering: <whole
  object> })` — a column replace, not a merge. Any key not in that field list is
  destroyed on the owner's next save. This is already true of the legacy
  `formFields` key today; if `orderFormEnabled` and `fulfillmentCopy` are added
  without touching that initialiser, **an owner editing their catering copy
  silently turns the feature off**. Fixed by spreading `...content` before the
  normalised fields, which makes every present and future key round-trip; the
  enable switch and copy editor then make them owner-settable rather than
  merely preserved.
- **Brand-level catering content overrides the restaurant-level column.**
  `get-brand-website` resolves `catering: brand.metadata?.catering ||
  restaurantData.catering || null` — deliberately, per its own comment — while
  the portal's editor writes `restaurant_website.catering`. For a brand with
  `brand.metadata.catering` set, an owner can flip the switch and see no change
  on the public site. Pre-existing precedence (it affects `heardAboutUsOptions`
  the same way today) but newly consequential now that the object carries a
  functional switch rather than only copy. Enablement for those brands is a
  staff edit at brand level. Worth a line in QA's test plan and worth an
  observation; not fixed here, because changing that precedence would change
  what every brand's published catering page renders.
- **The seven-column board scrolls; it does not break.** The kanban is `flex
  gap-3 overflow-x-auto` with `w-56` columns, so two more columns extend an
  already-scrolling row — the PRD's "a layout change, not just a string
  addition" overstates it. Real consequence: at seven columns roughly the last
  two sit off-screen on a 1440px display, so the two new stages must be
  positioned where a new lead is actually looked for (immediately after `New
  Enquiry`), not appended at the end.
- **No structured option/modifier capture.** A restaurant whose dishes carry a
  `conditions.required: true` option set (serving size, portion) will receive
  "2 × Butter Chicken" with the modifier expressed — if at all — in the dish's
  free-text note. That is a real gap against how those dishes are ordered
  elsewhere in the product, and it is the most likely source of a "the owner
  still had to phone back" complaint after this ships. Accepted for Piece 1 (no
  AC requires it; building it correctly is pricing-adjacent, i.e. Piece 2), and
  named so that if it does happen it reads as a known limitation with a home
  rather than a design miss.
- **The new columns are writable through the known `update_catering_request`
  gap.** An authenticated staff member with legitimate access to a row can
  overwrite `selections`/`action_type` via that unconstrained `.update(
  updateData)`. No new cross-tenant exposure (the access check itself is
  correct) and no new write path is added by this ticket; the new columns simply
  join the set the existing 2026-08-29 proposal already covers. Not fixed here,
  not re-filed.
- **Changing location mid-form invalidates the selections.** A multi-location
  brand's locations have different menus, and the form already resets
  `delivery_method` when `restaurant_id` changes. Selections must reset too, and
  visibly — a silent wipe of a half-built order is worse than the stale
  references it prevents.
- **Duplicate submissions on retry.** The endpoint has no idempotency key, so a
  timeout-then-retry creates two rows. True today; not introduced here, and not
  worth building for a lead form where a duplicate is visible and deletable.
  Named so it isn't rediscovered as new.
- **`config-site-builder` has no test target** — `npm run lint` and `npm run
  build` only, per `projects.md`. The largest single piece of new logic in this
  ticket (the selector and the gate) therefore gets no automated coverage. That
  is `ENG-002`'s tracked gap, not this ticket's to fix; QA's plan should lean on
  `restaurant-portal`'s `vitest` for the stage changes and on manual
  verification for the public form.
- **Size.** This is an honest `L` and it is at the top of the range: three
  repos, one new component, twelve status literals across eight files, plus the
  catering-editor addition ADR-009 makes mandatory. The editor section (`~100`
  lines across three files) is the piece most exposed if the ticket runs long —
  but it cannot be cut without leaving the feature unenableable, so if pressure
  appears, the honest response is to say so, not to trim it.

## Rollout

**Phased by deploy order, gated off by default.** No feature flag is added —
`orderFormEnabled` is the flag, and it is per-restaurant, owner-settable, and
already off everywhere.

1. **`aiorders-api` migration.** Two nullable columns. Inert — nothing reads or
   writes them.
2. **`restaurant-portal`.** Two new stages everywhere, the itemized block, the
   editor addition. Inert — the two new columns render empty and no row carries
   the new statuses yet. **Must precede step 3**; see Risks.
3. **`aiorders-api` `catering-request`.** Now able to store the new fields and
   derive the new statuses. Still inert — no caller sends them.
4. **`config-site-builder`.** The picker ships. Still inert for every
   restaurant, because `orderFormEnabled` defaults off.
5. **Enablement, one restaurant at a time**, by its owner in Website →
   Catering, or by staff for a brand whose `brand.metadata.catering` overrides
   the restaurant-level column.

**Rollback:** revert step 4 and no new-status rows are produced; step 2 stays
deployed so any rows already created keep rendering on the board. If steps 1–3
must also come out, move orphaned rows back first (`UPDATE catering SET status
= 'New Enquiry' WHERE status IN ('Quote Generated','Contact Requested')`) — the
columns themselves can be dropped safely, since nothing outside this ticket
reads them.

## Out of scope

- **Any price, tier, package, upcharge, or price snapshot** — Piece 2. Nothing
  in this design stores or displays a price.
- **"Edit Quote", resend, a customer-facing quote, `Quote Viewed`, and any
  tokenized quote URL** — Piece 3. Piece 1 adds no new write path into
  `catering` from the owner side at all.
- **A structured dish option-set / modifier picker** — see Alternatives. If it
  proves necessary, it belongs with Piece 2, where the option surcharges become
  meaningful.
- **Itemizing the owner notification email.** `catering-request` builds its
  owner email by interpolating the flat fields into HTML; it stays as-is. The
  itemized order lives in the portal, which the email already links to.
- **Collapsing the duplicated status lists or `CateringRequest` interfaces** —
  the PRD's non-goal; overlaps `ENG-013`.
- **`src/pages/Dashboard.tsx`** — declares its own `CateringRequest` but needs
  none of the new fields and renders no status column. A mechanical "add the
  fields everywhere" pass should not pull it in.
- **Fixing `update_catering_request`'s missing field allow-list** — open
  proposal, 2026-08-29, not approved.
- **Fixing the two pre-existing `catering-request` error responses that omit
  CORS headers** — real, but not created here. The one error path this ticket
  adds carries them.
- **Changing `get-brand-website`'s brand-over-restaurant catering precedence** —
  deliberate, documented, and load-bearing for every brand's published page.
- **`restaurant-marketplace`'s and the CloudWaitress popup's own catering
  paths**, and wiring catering into the `autopilot` trigger engine — the PRD's
  non-goals, unchanged.
