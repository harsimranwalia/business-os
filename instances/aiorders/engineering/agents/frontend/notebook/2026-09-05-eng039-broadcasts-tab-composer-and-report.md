# ENG-039 build notes — Broadcasts tab, composer, drip editor, report UI

`continue ENG-039` landed with the ticket at `ready`, `depends_on: [ENG-038]`
satisfied (verified 2026-09-05). Built against `restaurant-portal`'s
`origin/main` at `5276a53` (post-ENG-032 merge), branch
`feat/ENG-039-broadcasts-tab-composer-and-report-ui`.

## Contract grounding: design prose vs. the merged code

The design's Interfaces section and the ticket's own Outcome bullet were
read as the starting point, but the actual `aiorders-api` diff (merged,
`brand-portal/broadcasts.ts` + `20260904140000_broadcast_campaigns.sql`) was
read directly before writing any frontend type, per this board's own
standing practice of trusting the live/merged tree over design-time prose
where they could drift (`ADR-019`, `ENG-032`'s Components/Data discrepancy).
Two places this actually mattered:

- **`getOffers`/`createOffer`, cited by both the ticket and design as the
  idiom to match in `brandPortalApi.ts`, don't exist in that file.** Grepped
  the whole frontend repo — `createOfferMutation` lives in `pages/offers/Index.tsx`
  via a `use-offers.ts` hook that calls `supabase.functions.invoke('brand-portal',
  {action: 'get_offers', ...})` directly, not through `brandPortalApi`. Likely a
  stale reference from whenever the design was written, not a real conflict:
  `brandPortalApi.ts` already has its own live `callApi(action, payload)` idiom
  (used by `get_catering_requests`/`get_feedback`/etc.), and `broadcasts.ts` is a
  same-router sibling to `catering.ts`/`feedback.ts` in the exact same way — so
  the 8 new methods follow the file's own present pattern instead of chasing a
  reference that isn't there. Not filed as a proposal or observation — this is
  the kind of one-file, no-ambiguity drift a build hop just resolves and moves
  on from, not a process-level finding.
- **The report's actual shape is narrower than "sent/pending/failed by
  channel" reads.** `broadcast_campaign_recipients` carries no `channel`
  column (Data section: one row can cover more than one channel per step), so
  `recipients_by_status` (pending/sent/failed/skipped_opted_out/cancelled) has
  no per-channel breakdown, and `delivery_by_channel` (from `communication_log`)
  only carries `sent`/`opened`/`clicked` per channel — there is no
  "pending-by-channel" or "failed-by-channel" anywhere in the actual response.
  `BroadcastReport.tsx` renders exactly these two groupings side by side rather
  than inventing a channel-scoped pending/failed split the backend can't
  produce.

## Business rules deliberately not duplicated client-side

Per the ticket's own Notes ("this ticket doesn't duplicate any of it
client-side beyond ordinary form validation for UX"): the 10,000-recipient
cap and the 24h per-restaurant campaign-interval cap
(`MAX_RECIPIENTS_PER_CAMPAIGN`/`MIN_CAMPAIGN_INTERVAL_HOURS`,
`brand-portal/broadcasts.ts`) are not read, mirrored, or re-validated in the
composer. A rejection surfaces as whatever `error` string the action
returns, shown via the same toast path as any other failed mutation. Two
repos, no shared type package between them — hardcoding either number here
would be a silent-drift risk the ticket's own wording is warning against.

## The locked/read-only state

`update_broadcast` rejects anything not `draft`/`scheduled`
(`brand-portal/broadcasts.ts`'s own comment: "'active or later' ... draft/
scheduled are the only pre-send states"). The composer's `isLocked` reads
`editCampaign.status` (fetched fresh via `useBroadcast`, not the list row's
possibly-stale summary) against `EDITABLE_BROADCAST_STATUSES`, never a
`scheduled_send_at`-vs-`now()` comparison — the dispatcher poll can lag that
comparison by up to 5 minutes (`ADR-018`), so a wall-clock guess would show
the wrong lock state right around every send. A `<fieldset disabled>` wraps
the whole form when locked, which is enough to disable every Radix control
inside it (they all render real `<button>` elements) with no per-field
plumbing.

## Full campaign fetched by the composer itself, not passed in

The list only has `BroadcastCampaignSummary` (no `steps`) from
`list_broadcasts`. Rather than have `Broadcasts.tsx` fetch the full record
before opening the dialog, `BroadcastComposer` takes `editCampaignId` and
calls `useBroadcast` itself, showing a skeleton until the detail arrives.
Keeps the caller down to "which id," and means the same loading state covers
both a slow network and a cold cache.

The form-population `useEffect` keys on `[open, isEditing, editCampaign?.id,
editCampaign?.updated_at]`, not the whole `editCampaign` object — react-query
hands back a new object reference on every fetch, and keying on the object
itself would re-clobber in-progress typing on any background refetch
(window refocus, an invalidation from elsewhere). Keying on `updated_at`
specifically means a *real* server-side change (e.g. the dispatcher flipping
`scheduled → active` while the owner has the edit dialog open) still
re-populates and re-locks the form live — which is the behavior the ticket's
own locking note asks for, not a bug to guard against.

## Reused rather than rebuilt

- `EmailEditor` (existing autopilot component) for each step's email body,
  passed a single-entry `variables` list (`customer_name` only) instead of
  the reactive wizard's per-trigger variable sets — matches the design's own
  "`replaceTemplateVariables`'s existing `{{customer_name}}` — reused, not
  rebuilt."
- `useOffers()` (existing hook, already fetches active offers via
  `brand-portal`'s `get_offers`) powers the coupon-attach picker, filtered to
  `is_active && !is_template && coupon_code`. No new offers-fetching path.
- Popover+Calendar date picker copied in shape (not logic) from
  `ScheduleVisitDialog.tsx`, minus its Canadian-city timezone selector —
  that component picks a timezone because an influencer visit happens at a
  specific city; a broadcast is scheduled by the owner in their own current
  browser timezone, so a plain local `Date` + native `<input type="time">`
  is both simpler and more correct here, not a shortcut.

## Self-test

- `npm run lint`: 96 problems, identical count and file set to the baseline
  `ENG-032` already confirmed (`git log`'s own note: "Lint 96/0-new... round
  1's logged '63' was stale, not a regression") — grepped the full output for
  every new/touched filename, zero matches. 0 new.
- `npm run build`: clean. Bundle-size delta measured directly (stash/build/
  pop), not assumed: `1,976.47 kB → 2,003.65 kB` raw (+1.4%), gzip `552.63 kB
  → 558.85 kB` (+1.1%) — under the standards' 10%-growth-needs-justification
  line, so none written.
- `npm run test`: 5/5 passed (4 files) — all pre-existing, unchanged.
- **No new test file added.** No bug is being fixed (this is additive
  feature work, not a fix), and this repo has no established per-component
  test convention for new UI beyond the one regression test `ENG-032` itself
  added for an actual bug — same position that ticket's own build hop was in
  and resolved the same way. QA's own gate is the next place coverage for
  this ticket's 5 owned acceptance criteria (AC1–AC5, per the work-breakdown's
  own AC-mapping) gets written.

## Committed and pushed

`restaurant-portal@9a9ec86` (`feat/ENG-039-broadcasts-tab-composer-and-report-ui`,
tracking `origin/feat/ENG-039-broadcasts-tab-composer-and-report-ui`). No PR
opened yet — devops's own release-readiness hop, same precedent every prior
building hop on this board has used.
