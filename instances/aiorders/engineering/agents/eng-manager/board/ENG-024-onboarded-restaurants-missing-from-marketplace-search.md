---
id: ENG-024
title: Set show_in_marketplace on restaurant-portal-onboarding's createRestaurant insert, plus a backfill
project: aiorders-api
type: bug
size: XS
time_estimate: under an hour (XS band, definition-of-done.md)
time_spent:
time_remaining:
severity: P1
priority:
state: shaped
owner: eng-manager
lane: fast
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

`aiorders-api`'s `restaurant-portal-onboarding` edge function creates a new
restaurant row with `approved: true` but never sets `show_in_marketplace`.
Every marketplace search path (`restaurant-marketplace`'s discovery RPC and its
fallback query, plus the sitemap) hard-requires `show_in_marketplace = true`.
Result: every restaurant added through the FoodSwipe onboarding sign-up flow is
silently invisible in marketplace search — including location-sorted search —
until a staff member manually flips a toggle in the internal admin tool, which
nothing in the flow tells anyone to do. Full trace in the PRD.

## Outcome

A restaurant added through onboarding is visible in FoodSwipe marketplace
search (including location-sorted search) immediately, with no manual admin
step. Restaurants already added through this flow before the fix are made
visible by a one-time backfill, not just new sign-ups going forward.

## Notes

- **Fix site:** `aiorders-api/supabase/functions/restaurant-portal-onboarding/restaurants.ts`,
  `createRestaurant`'s `.insert()` — add `show_in_marketplace: true` alongside
  the existing `approved: true`.
- **Backfill:** existing rows created through this path that are `approved:
  true` and currently not `show_in_marketplace: true` need a one-time update.
  Scope the `WHERE` to this flow's actual signature carefully — don't flip the
  flag for rows that are unapproved or belong to the separate `restaurant-claims`
  path on purpose (see PRD Non-goals).
- **Worth checking while in this file:** whether `show_in_marketplace`'s
  DB-level default should also change, so any future insert path doesn't
  reintroduce the same gap. Not decided here — see PRD Risks.
- **Not in scope:** `restaurant-claims`' own insert (same omission, but
  `approved: false` by design — different question, see PRD Non-goals and
  `observations.md`).
- **Fast lane** (`size: XS`, `type: bug`): `intake → building → in-review →
  shipped → verified`, one combined gate (review + suite + OWASP on the
  touched surface). `aiorders-api` has no test command registered
  (`config/projects.md`) — pre-existing, board-wide gap, not specific to this
  ticket.
- **G1 auto-skipped** (bug type) — no gate item raised, no approver-facing WIP
  or approval-cap slot used by this ticket.

## Log

- 2026-08-29 `intake → shaped` (product-manager) — sized XS, project
  `aiorders-api`, type `bug`, severity P1, lane `fast`. Context: PM inbox card
  `agents/product-manager/inbox/2026-08-29-fix-the-location-bug-on-foodswipe.md`.
  Root cause traced directly in live code (no worktree existed on this host for
  any project — none created; investigation read the human's own checkout
  read-only across `aiorders-api`, `restaurant-portal`, `restaurant-marketplace`,
  `aiorders-admin-hub`, no writes made there): `restaurant-portal-onboarding`'s
  `createRestaurant` insert sets `approved: true` but never
  `show_in_marketplace`, which every marketplace search path hard-requires.
  Confirmed the gap is never closed downstream either (`updateRestaurantDetails`
  → `mapPlaceToRestaurantRow`'s column whitelist also excludes it). PRD written:
  `agents/product-manager/specs/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md`.
  G1 auto-skipped per `definition-of-done.md` (bug type). Held at `shaped`
  only long enough to write this entry — not blocked by any cap (machine WIP
  counts `ready`..`ready-to-ship`, not `shaped`; approver-facing WIP and
  approval cap don't apply since no G1 was raised). Owner handed to
  `eng-manager` — PM's job (shape + PRD) is done, and per
  `agents/product-manager/agent.md`, sequencing/WIP/assignment is the EM's,
  never the PM's, even for an auto-approved bug. `1 transition`
  (`intake → shaped`), well under the cap of 4 — deliberately did not attempt
  `ready`/`building` myself: that's the EM's assignment step and then new
  implementation work, both outside this `intake` event's own contract ("a
  pass stops at... new implementation work").
  `chained: ENG-024` — fired `lib/eng-trigger.sh continue ENG-024` before
  this pass exits: `shaped`, owner `eng-manager`, an agent-owned state with no
  gate to wait at (G1 auto-skipped), so nothing about this ticket is waiting
  on a human. Full reasoning above; see also `agents/eng-manager/board/_index.md`'s
  dated entry for this pass.
