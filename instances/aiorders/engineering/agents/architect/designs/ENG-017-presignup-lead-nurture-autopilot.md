---
ticket: ENG-017
project: aiorders-api
author: architect
created: 2026-09-01
adrs: []
one_way_doors: []
touches_data: true
touches_models: false
---

# Autopilot nurture for the presignup sales lead pipeline — technical design

## Approach

Reuse the exact shape `ENG-013` already established for `profiles.foodswipe_stage_override`
(nullable text column + CHECK constraint, admin-gated set/reset semantics, kanban-style
read preferring the override), applied to `leads` instead of `profiles`. Do **not** route
through the restaurant-scoped `autopilot`/`communication_templates` system — it cannot
represent a presignup lead (no `restaurant_id`, not a customer) and adapting it would be
the bigger, riskier change. Instead, call the two actor-agnostic send primitives
(`sendEmail`, `sendSMS`) directly from a new, small lead-nurture code path with its own
hardcoded per-stage template content. Extend the *existing* `admin-portal/handlers/leads.ts`
update route rather than inventing parallel endpoints, since it already does what a stage
change needs (an authenticated, admin/sub-admin-gated write to a `leads` row) — the only
new behavior is a side effect when `stage` changes to a nurture-flagged value.

**Correction to this ticket's own PRD, found during this design:** `ENG-013` — named in the
PRD as "the same mechanism, already approved" — is not on `origin/main`. It ships on its own
unmerged branch (`feat/ENG-013-foodswipe-funnel-stage-control`), currently `blocked` awaiting
the approver's merge. This design mirrors ENG-013's *pattern* (there is nothing wrong with
that; the pattern is sound and already reviewed once), but cannot literally share code with
it — this ticket's migration and handler are new files, not an extension of ENG-013's. The
two tickets touch different tables (`leads` vs `profiles`) and can build, review, and merge
in either order with no file conflict.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `aiorders-api/supabase/migrations/{ts}_add_leads_stage_and_nurture.sql` | new | database |
| `aiorders-api/supabase/functions/admin-portal/handlers/leads.ts` | modify — `stage` becomes an updatable field on the existing update route; side-effect hook on stage change | backend |
| `aiorders-api/supabase/functions/admin-portal/handlers/leads.ts` (or a small new sibling module) | new — `sendLeadNurtureMessage(lead, newStage)` | backend |
| `aiorders-admin-hub/src/pages/Leads.tsx` | modify — stage control on each row (mirrors ENG-013's inline dropdown pattern already used on `FoodswipeListings.tsx`); new "Autopilot Nurture" section (global enable/disable + sent-log) | frontend |

## Data

New migration on `leads` — **the first migration this table has ever had**; it was created
outside the migration system (same known pattern as `clover` and others, per the functions
README). Confirmed current columns via the intake/read code, not a migration file: `id,
name, email, phone, restaurant_name, business_type, country, num_of_locations, revenue,
work_title, created_at`. No stage/status column, no consent column, today.

Add, all nullable/defaulted (additive only):
- `stage text default 'new'` — CHECK constraint, closed set: `('new', 'contacted',
  'interested', 'converted', 'not_interested')`. `contacted`/`interested` are the
  nurture-flagged stages (per the PRD's own proposal); `converted`/`not_interested` are
  terminal, non-nurturing.
- `nurture_consent boolean default false` — see Risks. Ships in this migration either way
  (free, additive, avoids a second migration later); whether the lead-capture *form* actually
  collects it (PRD requirement 5) is a separate, unconfirmed piece of scope — see below.
- `last_nurture_sent_at timestamptz` — so a lead is never double-sent on a rapid stage
  bounce (set→reset→set), and so requirement 3 (send log visible to staff) has a cheap
  per-lead answer without joining a log table for the common case.

Open question this design does not resolve (flagged for whoever builds it, not decided
here): the PRD's requirement 4 ("a lead that has since signed up for real stops receiving
nurture") assumes some existing signal for "this lead converted to a real account." The
investigation did not find one — `leads` carries no `restaurant_id` or any other link to a
`profiles`/`restaurants` row. Two options: (a) treat `stage = 'converted'` as that signal,
staff-set, no automatic detection — simplest, matches this ticket's own size; (b) add real
detection (e.g. match on email against `profiles`) — materially more work, not sized into
this ticket. Recommendation: (a) for this ticket, name (b) as a follow-up if staff find
themselves forgetting to flip the stage.

## Interfaces

`PUT /admin-portal/leads/website/update` (existing route, `leads.ts`, admin/sub-admin gate
already in place at the file's own access check) — request body gains an optional `stage`
field alongside whatever it already accepts.

Side effect, inside the same handler, after a successful DB update: if the update changed
`stage` to `'contacted'` or `'interested'` (compare old vs new value; a same-stage no-op
update does not re-send), call:

```ts
async function sendLeadNurtureMessage(lead: Lead, newStage: string): Promise<void>
```

- No-ops (logs, does not throw) if `lead.nurture_consent` is not `true`.
- No-ops if `last_nurture_sent_at` is inside a minimum cooldown (recommend 24h, prevents a
  staff member toggling a stage back and forth from spamming the lead).
- Picks a hardcoded template per stage (no new template-authoring system — out of scope,
  matches the PRD's own non-goal). Calls `sendEmail()`/`sendSMS()` (`services/email.ts`,
  `services/sms.ts`) directly — both are actor-agnostic and already return
  `Promise<{success, messageId?, error?}>`; on `success: false`, log and continue (never
  block the stage-update response on a send failure — the stage change is the source of
  truth, the message is best-effort).
- Updates `last_nurture_sent_at` on send.
- Writes one row to a new minimal `lead_nurture_log` table (lead_id, stage, channel,
  success, sent_at) — this is requirement 3's "every send is logged," and is what the new
  admin-hub UI section reads.

New admin-hub UI: extend the existing `Leads.tsx` "website" tab with a stage control per
row (dropdown, same interaction shape as `FoodswipeListings.tsx`'s "Set stage"/"Reset to
automatic"). Separately, a small new "Autopilot Nurture" card/section on the same page: a
global on/off toggle (see Risks — recommend default **off**) and a table reading
`lead_nurture_log`. No per-stage template editor in this ticket (non-goal, both PRD and
this design).

## Alternatives considered

**Extend the restaurant-scoped `autopilot`/`communication_templates` system to allow a null
`restaurant_id`.** Rejected: that system's `trigger_type` enum, template model, and (per the
investigation) the unimplemented `actor: 'admin'` stub in `outgoing-communications` are all
shaped around a customer-of-a-restaurant, not a presignup lead. Bending it to fit would touch
more shared surface for a narrower, lead-specific need, and would still need new code in the
stub either way. Rejected in the PRD already; this design confirms the investigation was
accurate rather than re-opening it.

**Dedicated `stage/set` and `stage/reset` endpoints, mirroring ENG-013 exactly.** Considered,
since it's the proven, already-reviewed pattern. Rejected in favor of extending the existing
generic update route: `leads.ts` (unlike `profiles` for foodswipe) already has a working,
gated update endpoint, so adding parallel stage-specific routes would be two ways to write
the same field for no real benefit. The side-effect hook lives in one place either way.

## One-way doors

None. Two new nullable/defaulted columns plus one new small table, all additive; no existing
column changes meaning, no existing route's behavior changes for a lead that stays at
`stage = 'new'` (the default), no new vendor, no auth-model change — same reversibility
class as `ENG-009`/`ENG-010`/`ENG-013`. Reversible by dropping the two columns and the new
table with zero blast radius elsewhere.

## Risks

**Consent (the one this ticket cannot get wrong).** Sending real, unsolicited marketing
email/SMS to a person who never opted in is a CASL exposure (AIOrders is Canadian), not just
a UX concern — the PRD already flagged this (requirement 5, `[proposed]`, not yet confirmed
by the approver) and the investigation confirmed the lead-capture form collects no consent
signal today. **Recommendation: `nurture_consent` defaults to `false` and the global
"Autopilot Nurture" toggle (above) also defaults to off.** This ships the full mechanism
(schema, send path, UI) in this ticket, but nothing actually sends until a human deliberately
flips both — which decouples "build the feature" from "resolve the consent-capture gap,"
rather than making this design silently decide a legal question. If the approver wants sends
enabled before requirement 5's form change ships, that's a decision for them to make
explicitly, not a default this design should pick.

**Send failures are silent by design (best-effort).** Acceptable because a lead's stage is
the real system-of-record signal (matches requirement 1); a failed nurture send degrades to
"staff still has to follow up manually," which is where every lead already sits today.

## Rollout

Straight — migration first (additive, no backfill needed since `stage` defaults `'new'` for
every existing row, which is the correct behavior: nothing should suddenly nurture-fire for
the entire existing backlog on deploy). No flag needed beyond the "Autopilot Nurture" on/off
toggle already in the design, which doubles as the rollout control. Rollback: drop the new
columns/table; no other code path reads them.

## Out of scope

Reseller/partner access (no lead-to-reseller attribution mechanism exists — PRD non-goal).
A per-stage template-editing UI (hardcoded templates only, this ticket). Extending
`communication_templates` to leads. A new outbound channel beyond email/SMS. Retroactively
messaging the existing lead backlog (the default-`'new'` migration behavior above is
deliberate). Automatic "converted" detection beyond a staff-set stage (see Data section).
