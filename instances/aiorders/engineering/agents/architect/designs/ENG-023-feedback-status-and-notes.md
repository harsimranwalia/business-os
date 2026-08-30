---
ticket: ENG-023
project: restaurant-portal
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Add status and internal notes to each brand-portal feedback item — technical design

## Approach

Two new columns on `restaurant_feedback` (`status`, `notes`), one new
edge-function action (`update_feedback`) on `brand-portal`, modeled on
`catering.ts`'s `update_catering_request` per the PRD's own instruction — with
one deliberate deviation from that model (an explicit field allow-list instead
of a blind spread; see Alternatives #2 and Risks). One new UI section on each
feedback `Card` in `Index.tsx`: a status `Select` and a notes `Textarea`, one
`Save` button per item persisting both fields together in one request.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/migrations/{ts}_add_status_notes_to_restaurant_feedback.sql` (`aiorders-api`) | new — two columns plus one trigger, see Data | database |
| `supabase/functions/brand-portal/feedback.ts` (`aiorders-api`) | modify — add `updateFeedback`, wired into the existing `handleFeedback` switch | backend |
| `supabase/functions/brand-portal/index.ts` (`aiorders-api`) | modify — route `update_feedback` to `handleFeedback`, alongside the existing `get_feedback` case | backend |
| `src/services/brandPortalApi.ts` (`restaurant-portal`) | modify — add `updateFeedback(id, updateData)`, extend `RestaurantFeedback` with `status`/`notes` | frontend |
| `src/pages/feedback/Index.tsx` (`restaurant-portal`) | modify — per-item status/notes editing UI | frontend |

## Data

- **`status text NOT NULL DEFAULT 'new'`.** Matches `catering.status`'s
  `NOT NULL` + default-text convention (confirmed live: `'New Enquiry'`, plain
  `text`, no enum, no CHECK constraint). The `ALTER ... ADD COLUMN ... DEFAULT`
  backfills every existing row in the same statement, so AC4 (pre-existing
  items show a plain default rather than an error) needs no separate backfill
  step. Fixed vocabulary: `new` / `in_progress` / `resolved` — lowercase
  snake_case, deliberately matching *this file's own* `nature`/`type`
  convention (`Index.tsx` already lowercases and switches on both) rather than
  `catering`'s Title-Case free text. Both precedents exist in this codebase and
  disagree, so this is a real choice: same-file consistency wins because the
  new field lives and is read in this exact file.
- **`notes text NULL`**, no default — absence (never written) stays
  distinguishable from an explicitly cleared note.
- **`updated_at`** already exists on this table (confirmed live: `timestamptz`,
  nullable, no default) but carries no trigger today. Attach the codebase's
  existing `public.update_updated_at_column()` `BEFORE UPDATE` trigger
  (already defined, already wired to `offers`, `restaurant_managers`, `ai`,
  `ai_conversations`, `influencer_campaigns`, `influencer_invitations` —
  confirmed live; `restaurant_feedback` simply never got wired to it). Answers
  the "when" half of the PRD's open who/when question for zero new code.
- **No RLS change.** `brand-portal`'s Supabase client is service-role
  (confirmed, `index.ts`), same as every other handler in this function —
  access is enforced entirely in-handler, not by RLS, matching both `catering`
  and `feedback`'s existing pattern.
- **Confirmed non-risk**: `restaurant_feedback`'s only existing trigger fires
  on `AFTER INSERT` only (`on_website_feedback_submit`, the new-feedback email
  to the restaurant via `notifications-handler`). An `UPDATE` from this
  ticket's new action cannot re-trigger that email. Checked directly against
  live trigger metadata rather than assumed, since a duplicate-notification
  regression would have been a real risk if this table's INSERT/UPDATE
  triggers weren't split the way they are.

## Interfaces

`brand-portal`, new action `update_feedback`:

```
Request:  { action: 'update_feedback', id: string,
            updateData: { status?: 'new' | 'in_progress' | 'resolved', notes?: string } }
Response: { success: true, data: RestaurantFeedback }
        | { success: false, error: string }
```

Client: `brandPortalApi.updateFeedback(id, updateData)`, same shape as
`updateCateringRequest(id, updateData)`.

Handler (`feedback.ts`, new `updateFeedback`, added to `handleFeedback`'s
switch alongside `get_feedback`):

1. Require `id` → `{success:false, error:'id is required'}` if missing.
2. Fetch `restaurant_id` for that row
   (`.from('restaurant_feedback').select('restaurant_id').eq('id', id).single()`)
   → `{success:false, error:'Feedback item not found'}` if missing — mirrors
   `update_catering_request` exactly.
3. `verifyRestaurantAccess(restaurant_id, supabase, user)` — correct argument
   order, checking `.hasAccess`, matching `catering.ts` and deliberately *not*
   `feedback.ts`'s own neighboring `getFeedback` (confirmed broken tenant-
   isolation check, `ENG-022`, same file). `{success:false, error: access.error
   || 'Access denied'}` on failure.
4. **Allow-list, not spread**: build the update payload by picking only
   `status` (if present — validated server-side against the 3-value set,
   rejecting anything else, since there is no DB CHECK to catch a bad write)
   and `notes` (if present, no length cap, matching every other free-text
   column on this table). The raw `updateData` object is never passed to
   `.update()` directly — see Alternatives #2 for why this departs from the
   model function's own body shape.
5. `.from('restaurant_feedback').update(payload).eq('id', id).select().single()`
   → `{success:true, data}` / `{success:false, error}`.

This handler returns `{success:false, ...}` on every failure path rather than
throwing, matching `catering.ts` (per the PRD's explicit instruction) and
*not* this same file's own `getFeedback`, which throws and is caught by
`index.ts`'s outer handler as an undifferentiated `500`. The frontend's
existing `if (!response.success)` handling already expects the return-based
shape, so failures here surface as a normal toast, not a generic
"Internal server error."

Frontend: `Index.tsx` gains local per-item editable state (`status`, `notes`)
seeded from each `feedback` row, a `Select` (3 fixed options, `@/components/ui/select`,
already present in this repo) and a `Textarea` (`@/components/ui/textarea`,
already present), and one `Save` `Button` per card. Save calls
`brandPortalApi.updateFeedback(feedback.id, {status, notes})` and, on success,
invalidates the `['restaurant-feedback', currentRestaurant?.id]` query
(react-query — this page already uses `useQuery` for its fetch, so
invalidation is the file's own idiom; `catering/Index.tsx`'s manual
refresh-counter pattern doesn't apply here since that page doesn't use
react-query at all). Toast on success/error, matching this file's existing
`useToast` usage.

## Alternatives considered

1. **Auto-save `status` on change, keep `notes` on an explicit Save.**
   Rejected for a ticket this size — two independent save paths on one card
   roughly doubles the state and error-handling surface for a few hours of
   estimated work. One combined save satisfies both stated acceptance
   criteria with one request, one loading state, one error path.
2. **Spread `updateData` directly into `.update()`, exactly mirroring
   `update_catering_request`'s body.** Rejected on inspection. `catering.ts`'s
   own `update_catering_request` passes the client's raw `updateData` straight
   into `.update()` with no field allow-list — a caller who already passed the
   access check can overwrite *any* column on the row, including
   `restaurant_id` itself. The PRD asks this design to copy that function's
   *access-check shape* (confirmed correct — fetch, verify, then write), not
   its *payload shape* (never audited, not confirmed correct); copying the
   latter would import a mass-assignment gap into new code with eyes open for
   the sake of literal symmetry. Two extra lines instead. See Risks for where
   the original gap is being flagged.
3. **Postgres enum type or a CHECK constraint for `status`.** Rejected in
   favor of plain `text`, matching `catering.status`'s convention — no status-
   shaped column anywhere in this schema uses an enum or a CHECK constraint.
   An enum is more correct in isolation but is new machinery this codebase
   doesn't otherwise use, for a 3-value set the handler already validates
   server-side.
4. **A separate `restaurant_feedback_status_history` audit table** (who/when
   per change), answering the PRD's open multi-staff-attribution question
   directly. Rejected as speculative generality: no sibling status field in
   this schema (`catering`, the only precedent) carries per-change
   attribution either, the PRD leaves this explicitly open rather than
   required, and a meaningful "who" needs distinct per-staff portal logins —
   not confirmed to exist by anything read for this design. The cheap half,
   "when," is answered by wiring the existing `updated_at` trigger. If "who"
   turns out to matter, it's a new ticket once staff-level accounts are
   confirmed.

## One-way doors

None. Two additive columns (one defaulted/backfilled by the `ALTER` itself,
one nullable), one new handler action following an existing in-file pattern,
one new UI section. Fully reversible: drop the two columns, delete the action
and its switch case, revert the UI commit. No new datastore, vendor, auth
model, or public contract — `brand-portal` already accepts arbitrary `action`
values in the same request envelope.

## Risks

- **`catering.ts`'s `update_catering_request` has its own, unrelated
  mass-assignment gap** (blind `updateData` spread — Alternatives #2),
  discovered while reading it as this ticket's prescribed model. Not this
  ticket's surface, not fixed here — different file, no shared code path.
  Filing one line to `agents/eng-manager/proposals.md` so it isn't lost, per
  this department's rule that an agent's own findings become proposals, not
  tickets, outside the P0 carve-out. This doesn't meet that carve-out: it
  requires an already-authenticated actor's deliberate misuse, not an open
  unauthenticated hole, on a project that (being `restaurant-portal`/
  `aiorders-api`, not internal-lane) would otherwise need the P0 bar to
  bypass the proposal queue.
- **Inherits none of `feedback.ts`'s existing `getFeedback` access-check
  defect** (`ENG-022`) — this design's own `verifyRestaurantAccess` call is
  independently correct (Interfaces, step 3); `getFeedback` and the new
  `updateFeedback` share a file, not code.
- **Status vocabulary is enforced in two places that must be kept in sync**:
  the frontend `Select`'s fixed options and the handler's server-side
  allow-list. Three values, low drift risk, named so a future 4th status
  remembers both.
- **No migration needed for historical rows beyond the column default** —
  `notes` is genuinely absent for every pre-existing row (`NULL`, correctly
  distinct from "cleared"), and `status` is backfilled to `'new'` by the
  column default in the same DDL statement that adds it.

## Rollout

Straight, no flag. Branch → PR → gates → human merge (both `restaurant-portal`
and `aiorders-api` are L1, same split precedent as `ENG-007`/`ENG-011`/
`ENG-015`). `restaurant-portal`: `npm run lint` + `npm run build` +
`npm run test` — new/extended `Index.test.tsx` cases: status update persists,
notes update persists, a pre-existing item renders its default status rather
than crashing, an access-denied response surfaces as a toast. `aiorders-api`
has no test command (a registered gap, `ENG-002`'s own scope, not this
ticket's to fill).

Rollback: revert both repos' commits. Dropping the two columns in a follow-up
migration is safe at any point after rollback — nothing else reads them.

## Out of scope

- Cross-item frequency/aggregation (PRD non-goal; `ENG-025`, same page,
  additive alongside — no shared code path, confirmed in `ENG-025`'s own
  design).
- Any customer-facing reply channel (PRD non-goal).
- An admin-hub mirror of this view (PRD non-goal).
- Per-change (who/when) audit trail (Alternatives #4).
- Fixing `feedback.ts`'s `getFeedback` access-check defect (`ENG-022`'s
  scope).
- Fixing `catering.ts`'s `update_catering_request` mass-assignment gap (new
  finding, routed via `proposals.md`, a separate ticket if approved).
