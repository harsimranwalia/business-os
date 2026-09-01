---
ticket: ENG-023
project: restaurant-portal
author: architect
created: 2026-08-31
<!-- merge note: local claimed created 2026-08-29, remote claimed created 2026-08-31 (more recent), kept remote -->
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Feedback status and notes — technical design

## Approach

Two new columns on `restaurant_feedback` (`status`, `notes`), one new
`update_feedback` action in `brand-portal/feedback.ts` mirroring
`catering.ts`'s `update_catering_request` shape (fetch record → resolve the
owning `restaurant_id` → verify access → update → return), and a small edit
affordance added to the existing card in
`restaurant-portal/src/pages/feedback/Index.tsx`. No new table, no new page,
no new project.

**Resolving an apparent conflict between the PRD and `ENG-022`.** The PRD
says to model the new handler on `catering.ts`'s `update_catering_request`;
`ENG-022`'s design (same directory, filed the same day) classifies
`feedback.ts` as one of the four files that use the **throw** convention for
access failures, not `catering.ts`'s **return `{success:false}`** convention.
Read together rather than against each other: the PRD is asking for the
*data-access shape* (fetch → verify → update → return), not `catering.ts`'s
literal error-signaling mechanics — the PRD itself says the exact
implementation is the architect's call. Copying the return-idiom into
`feedback.ts` would leave this one file with two different failure
conventions (`getFeedback` throws, `updateFeedback` would return
`{success:false}`), which is the same inconsistency `ENG-022`'s own
Alternatives section rejects introducing *across* files — worse, here, done
*inside* one. So `updateFeedback` uses catering's shape with feedback's own
existing convention: it throws.

**Sequencing note with `ENG-022`, not a hard dependency (per the PRD).**
`feedback.ts`'s existing `getFeedback` calls `verifyRestaurantAccess` today
with the arguments in the wrong order and treats the returned object as a
boolean — always truthy, so access is never actually denied. That is
`ENG-022`'s bug to fix, not this ticket's, and `updateFeedback` below does not
reuse that call site. What this ticket *does* need is the correctly-ordered,
correctly-checked call — which exists today in `utils.ts` as
`verifyRestaurantAccessLegacy` (throws on denial, functionally correct,
currently unused and marked `@deprecated`). `ENG-022` renames this to
`requireRestaurantAccess` and drops the deprecation. Whichever of these two
tickets builds second should call `utils.ts` at build time to see which name
is live and use that one — a one-line detail, not a scheduling constraint on
either ticket.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/migrations/{ts}_restaurant_feedback_status_notes.sql` | new — two columns + `updated_at` trigger | database |
| `supabase/functions/brand-portal/feedback.ts` | modify — new `updateFeedback` function; new `update_feedback` case in `handleFeedback`'s switch | backend |
| `supabase/functions/brand-portal/index.ts` | modify — route `update_feedback` to `handleFeedback`, same pattern as the existing `get_feedback` line | backend |
| `restaurant-portal/src/services/brandPortalApi.ts` | modify — add `status`/`notes` to the `RestaurantFeedback` interface; add `updateFeedback(id, updateData)`, mirroring `updateCateringRequest` exactly | frontend |
| `restaurant-portal/src/pages/feedback/Index.tsx` | modify — a status `Select` and a notes field on each existing card, wired to a mutation that invalidates the `['restaurant-feedback', restaurantId]` query on success | frontend |

## Data

```sql
alter table public.restaurant_feedback
  add column if not exists status text not null default 'new',
  add column if not exists notes  text;

comment on column public.restaurant_feedback.status is
  'new | in_progress | resolved — restaurant-set workflow state';
comment on column public.restaurant_feedback.notes is
  'restaurant-internal notes; never shown to the customer';

drop trigger if exists set_updated_at on public.restaurant_feedback;
create trigger set_updated_at
  before update on public.restaurant_feedback
  for each row execute function public.update_updated_at_column();
```

Same shape as the most recent precedent in this repo,
`20260807000006_restaurant_claim_documents.sql`
(`status TEXT NOT NULL DEFAULT '...'` with the fixed set named in a comment,
plus a plain nullable `notes TEXT`) — matching the codebase's own convention
rather than introducing a Postgres enum type or a check constraint, neither
of which any sibling status column here uses.

`restaurant_feedback` already has `updated_at`, referenced by the 2026-08-07
dedupe migration's `ORDER BY updated_at DESC NULLS LAST` — the trigger
creation above is idempotent (`drop ... if exists` then `create`) in case it
isn't already wired to this table; `database` confirms against the live
schema at build time and can drop the trigger block entirely if it turns out
to already be present.

No separate backfill pass: `default 'new'` fills every existing row in the
same `alter table`, and AC4 asks for exactly that default rather than any
inferred value. `notes` stays `null` for existing rows, which the UI already
has to treat as "no note yet."

## Interfaces

```
action: 'update_feedback'
payload: { id: string, status?: string, notes?: string }
```

```ts
async function updateFeedback(data: any, supabase: SupabaseClient, user: any) {
  const { id, status, notes } = data
  if (!id) throw new Error('id is required')
  if (status === undefined && notes === undefined) {
    throw new Error('status or notes is required')
  }

  const { data: existing, error: fetchError } = await supabase
    .from('restaurant_feedback')
    .select('restaurant_id')
    .eq('id', id)
    .single()
  if (fetchError || !existing) {
    throw new Error('Feedback item not found')
  }

  // requireRestaurantAccess post-ENG-022, verifyRestaurantAccessLegacy before —
  // see Approach. Throws on denial.
  await requireRestaurantAccess(existing.restaurant_id, supabase, user)

  const updateData: Record<string, unknown> = {}
  if (status !== undefined) updateData.status = status
  if (notes !== undefined) updateData.notes = notes

  const { data: updated, error } = await supabase
    .from('restaurant_feedback')
    .update(updateData)
    .eq('id', id)
    .select()
    .single()
  if (error) throw new Error(`Failed to update feedback: ${error.message}`)

  return { success: true, data: updated }
}
```

No server-side check that `status` is one of the three values — the same
level of enforcement `catering.ts`'s own `update_catering_request` applies to
its own `status` field today (none; the client's own option list is the only
fence). Named here as a deliberate match to existing precedent, not an
oversight.

Failure responses (all thrown, all surfacing through `index.ts`'s existing
top-level catch as HTTP 500, `{error: 'Internal server error', details:
message}` — identical to `getFeedback`'s current failure shape in this same
file, not introduced by this ticket): `id is required`, `status or notes is
required`, `Feedback item not found`, `Access denied to this restaurant`.

Frontend: `brandPortalApi.updateFeedback(id, updateData):
Promise<BrandPortalApiResponse<RestaurantFeedback>>` →
`callApi('update_feedback', { id, updateData })`, exactly mirroring
`updateCateringRequest`.

## Alternatives considered

1. **Use `catering.ts`'s literal return-idiom** (`{success:false, error}`) for
   `updateFeedback`, reading the PRD's "model it on catering.ts" as literally
   as possible. Rejected — see Approach: leaves `feedback.ts` with two
   conventions for its two functions, which is the inconsistency `ENG-022`
   is in the middle of closing in the other direction for this exact file.
2. **A separate `restaurant_feedback_status_log` table** recording who changed
   what and when, addressing the architect's blind-reading assumption
   (readback divergence, PRD Risks) that multi-staff attribution matters.
   Rejected for now — no sibling status field in this codebase
   (`catering`, `restaurant_claim_documents`) has this, the PRD leaves it
   explicitly open rather than required, and it's a pure addition later
   (new table, no shape change to `status`/`notes`) if it turns out to
   matter. Revisit if the approver asks once the plain version is in use.

## One-way doors

None. Two columns added to an existing table (one defaulted, one nullable),
one new handler action following the file's own two-function pattern, one new
UI control on an existing card. Fully reversible: `restaurant_feedback` is
read only by `getFeedback`'s own `select('*')` today, so dropping both
columns after the fact leaves that query unaffected; removing the route case
and the UI control removes the rest.

## Risks

- **Sequencing/naming coupling with `ENG-022`** on the access-check helper's
  name — see Approach. Whichever ticket builds second checks `utils.ts` for
  the live name. Not a `depends_on`; both tickets are independently correct.
- **No format validation on `status`** beyond the client's option list (see
  Interfaces) — matches existing precedent (`catering.ts`), so a bad value
  written by anything other than this one client would show up as an
  unstyled badge, not break anything.
- **Existing rows backfill to `status: 'new'`** (AC4) regardless of their real
  history — unavoidable, since no historical status data exists anywhere to
  infer from (confirmed in the PRD). Worth naming so it isn't mistaken for a
  bug later: an old, already-resolved complaint will show as "new" until a
  restaurant re-touches it.
- **AC3's tenant-isolation guarantee still depends on `ENG-022` landing
  correctly** for the *existing* `getFeedback` read path — carried from the
  PRD, not re-decided here. This ticket's own new `updateFeedback` path is
  correct regardless of `ENG-022`'s build order (see Approach); `getFeedback`
  itself stays broken until `ENG-022` ships, independent of this ticket.

## Rollout

Straight, no flag, no phased rollout. Branch → PR → gates → human merge
(`restaurant-portal` and `aiorders-api` are both L1) → deploy (Cloudflare for
the frontend, the Supabase project for the edge function). Two-repo ticket,
same split precedent as `ENG-007`/`ENG-011`/`ENG-015` — both branches must
merge before this ships. Rollback: revert both merge commits; the schema
change is additive, so leaving the two columns in place after a code-only
revert is harmless and does not need its own rollback step.

## Out of scope

Cross-item frequency/aggregation analysis (PRD non-goal; separate
non-blocking question already raised, `inbox/2026-08-29-eng023-frequency-question.md`).
Any customer-facing reply channel. An admin-hub mirror of this view.
AI-generated summarization or categorization. A status-change audit log (see
Alternatives #2). Server-side enum validation beyond the client's own option
list (see Interfaces).

## Prior pass (superseded)

An earlier pass (2026-08-29, titled "Add status and internal notes to each
brand-portal feedback item") reached a similar overall shape (two new
columns, one new `update_feedback` action modeled on
`update_catering_request`, one new UI section per feedback `Card`) but
differed in two substantive, deliberate ways not carried forward into the
pass above:

- **Chose `catering.ts`'s literal return-based failure convention**
  (`{success:false, error}` on every failure path) for `updateFeedback`,
  rather than the throw-based convention `feedback.ts`'s own `getFeedback`
  already uses. The newer pass explicitly rejects this (Alternatives #1)
  because it would leave `feedback.ts` with two different failure
  conventions across its two functions — the earlier pass instead reasoned
  that matching failures shape to the frontend's existing
  `if (!response.success)` handling meant fewer changes on the client side.
- **Added explicit server-side validation of `status`** against the
  three-value allow-list (`new`/`in_progress`/`resolved`), rejecting any
  other value, on the grounds that there is no DB CHECK constraint to catch
  a bad write. The newer pass deliberately omits this, matching
  `catering.ts`'s own precedent of leaving `status` unvalidated server-side
  (Interfaces, "Named here as a deliberate match to existing precedent, not
  an oversight").

It also independently found and flagged `catering.ts`'s own
`update_catering_request` mass-assignment gap (a blind `updateData` spread
with no field allow-list, discovered while reading it as this ticket's
prescribed model) and routed it as a one-line finding to
`agents/eng-manager/proposals.md` rather than fixing it in this ticket's
scope — a finding the newer pass's own allow-list-shaped `updateData`
construction sidesteps but does not itself call out separately.
