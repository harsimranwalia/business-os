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

- 2026-08-29 no state change (eng-manager, `continue` event pass, context
  `ENG-024` — this ticket's own chain fire from the `intake` pass above).
  Narrow scope per this event's own contract: this ticket only. Mode check
  clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-024`) and whole-board: exit 0, clean.

  Re-checked fresh rather than trusted the board's cached header: all six
  machine-WIP tickets' own frontmatter (`ENG-007` ready-to-ship, `ENG-008`
  building, `ENG-009` ready, `ENG-010` ready, `ENG-011` ready-to-ship,
  `ENG-013` building) — count unchanged at 6/1, still over the cap of 1.
  Per `eng_build_loop.md` step 6, the To-do column (`intake`/`shaped`/
  `awaiting-scope`) is the only place a new start is drawn from, and "there
  is exactly one slot [that] does not free until the ticket occupying it
  reaches `shipped`" — this ticket (severity P1, fast lane) cannot enter
  `building` this pass regardless of severity; nothing in the loop's
  dispatch rule exempts P1 from the machine WIP cap, only the unrelated
  proposal-batching P0 carve-out (step 3) mentions P0 at all, and that's a
  different gate entirely. `agents/eng-manager/inbox/` empty — no technical
  intake item for this ticket; G1 was already correctly auto-skipped (bug
  type, fast lane), so there is no gate item to check either. Ticket
  correctly stays at `shaped`.

  **0 transitions.** `chained: none` — held by the machine WIP cap (6/1, no
  free slot); one of the explicit do-not-chain conditions. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-024`) and
  whole-board: exit 0, clean. One observation filed (`observations.md`): the
  `intake` pass above fired this chain without checking the machine-WIP cap,
  which was already known full at the time — this pass is the cost of that
  gap, one hop spent to re-derive a hold the shaping pass could have
  recognized itself. Full narrative on `agents/eng-manager/board/_index.md`'s
  dated entry for this pass.
