---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-046
recommendation: merge — code review, quality, and security all passed (security: zero findings); no migration owed (frontend-only, columns already shipped with ENG-044); third sub-ticket of the ENG-026 family, closes the family's UI half for AC2
time_estimate: under an hour
pr_url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/10
raised: 2026-09-07
notified: 2026-09-07T12:15:34
nudged:
decision: merged
---

# Merge request — FoodSwipe channel-visibility toggles — admin-hub restaurant details (ENG-046)

Sub-ticket of `ENG-026` (FoodSwipe channel-visibility toggles and
capability-based discovery), sequence 2 of 4 (parallel with `ENG-045`) —
depended on `ENG-044` alone (merged).

## What this does

- `RestaurantDetails.tsx`'s "Restaurant Features" card gains two new toggle
  rows (`has_order_food`, `has_catering`), markup identical to the six
  pre-existing rows in the same card.
- The existing Dine In `Switch` is repointed from `dine_in` to
  `has_dine_in` — `ENG-044`'s own live-schema check found `dine_in` real,
  live, and backfilled forward, so this is a repoint, not a fresh addition.
- `types.ts` regenerated (`supabase gen types typescript`), not hand-edited
  — most of this diff's line count is generated-output drift from several
  unrelated, already-shipped tickets that never regenerated this file.
- No new API call — `handleSave` already sends the entire `restaurant`
  state object to the existing `PUT /admin-portal/restaurants/:id`.

## Gates passed

- **Code review: pass** — `agents/principal-engineer/reviews/ENG-046.md`.
  0/10 automatic failures, no divergence from design, all three rows'
  field-wiring independently traced with no cross-wiring.
- **Quality: pass** — `agents/qa/test-plans/ENG-046.md`. AC2 (staff can
  view and set all three flags) covered by inspection against the diff; no
  suite exists for `aiorders-admin-hub` (open, unexpired proposal,
  `proposals.md` 2026-08-31), same as eight already-untested sibling rows
  in this file.
- **Security: pass, zero findings** — `agents/security/reviews/ENG-046.md`.
  No new route, no new dependency, no secret, no PII. The two new fields
  ride the same already-open write path the six sibling toggles already
  use; the one pre-existing gap (`updateRestaurant`'s missing field
  allow-list) is already tracked (`proposals.md`, 2026-09-03), not
  introduced or widened by this diff.
- No migration owed — confirmed no `ENG-046-*.md` migration file exists;
  correct for a pure frontend diff.

## Release readiness

- **Rollback:** no migration, no stored-state change of its own —
  reverting the merge (once merged) fully undoes this diff.
- **Observability:** read `handleSave` directly — already wraps the save
  in try/catch, logs `console.error`, and shows a destructive toast on
  failure, generic over every field on the `restaurant` object including
  the three new ones. Pre-existing, unchanged by this diff.
- **Cost:** $0/month — no new dependency (`package.json`/lockfile absent
  from the diffstat), no new infrastructure.
- **Window:** n/a — `aiorders-admin-hub` is registered L1; opening a PR is
  not a release. This repo's `deploy-cf.yml` triggers on push to `main`
  only (no `pull_request` trigger), so opening this PR carries no
  auto-deploy risk.

## PR

https://github.com/harsimranwalia/aiorders-admin-hub/pull/10

This project is registered **L1** — this department opens the PR, a human
merges. The next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket.

## Out of scope

- The Open Now filter and status display (`ENG-047`).
- The `updateRestaurant` field allow-list gap (already an open proposal,
  not this diff's to fix).
- Dropping the old `dine_in` column (follow-up ticket, per `ENG-044`'s own
  Notes).

Third of `ENG-026`'s four sub-tickets, and — with `ENG-044` shipped and
`ENG-045` also now parked on you (PR #20, `aiorders-api`) — every child
except `ENG-047` is now off the machine's own queue. `ENG-047`'s
`depends_on: [ENG-045]` is satisfied by `ENG-045`'s PR being open (does not
wait for merge, per `eng_build_loop.md` Guards, amended 2026-09-07), so
this pass is chaining straight into it rather than sitting idle — noted so
this isn't a surprise if you check the board before merging anything here.
