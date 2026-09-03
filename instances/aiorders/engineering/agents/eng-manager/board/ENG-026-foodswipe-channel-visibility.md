---
id: ENG-026
title: FoodSwipe channel-visibility toggles and capability-based discovery
project: restaurant-marketplace
type: feature
size: M
time_estimate: half a day to a day
time_spent:
time_remaining:
severity: P3
priority:
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-01
updated: 2026-09-02
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

FoodSwipe (the consumer discovery app) and the tools that manage what appears
on it have no way to say a merchant participates in one ordering channel
(order food) but not another (dine-in, catering). Every merchant is
implicitly "in" everywhere.

## Outcome

A merchant's participation in each of three channels is an explicit,
staff-set flag. FoodSwipe's channel tabs/filters show exactly the merchants
enabled for that channel — including ones currently closed, marked with
status — unless a consumer explicitly opts into "Open Now".

## Notes

**Filed title referenced the wrong ticket.** The raw request (`agents/
product-manager/inbox/_handled/2026-09-01-eng-011-on-the-brand-portal-i-want-
option-to-make-the-restau.md`) titled itself "ENG-011", an unrelated,
already-shipped ticket — allocated `ENG-026` instead at intake.

**Raw request bundled four capabilities behind one title; this ticket is
scoped to one of them.** See the PRD's own "Why this ticket is narrower"
section for the full reasoning. The other three (operational status engine,
smart dine-in/catering filters, promo badge overlay) are named as deferred
follow-on work, not dropped — a future intake pass files them individually
once this foundation ships.

**Likely this board's first three-repo ticket** (`aiorders-api`, `aiorders-
admin-hub`, `restaurant-marketplace`) — one more than `ENG-011`'s two. Named
here so the build hop doesn't discover it mid-branch.

**One proposed default not yet confirmed by the approver:** requirement 6 in
the PRD assumes the three flags are staff-set via `aiorders-admin-hub`, not
restaurant-owner self-service via `restaurant-portal`. If G1 comes back
correcting this, the scope changes materially (a new self-service form,
restaurant-scoped write access), not just an implementation detail.

**One risk deliberately left unresolved at this stage, not silently
defaulted:** the rollout/backfill question for existing merchants (PRD
Risks). Real design work against the live schema is needed before this
reaches `building` — flagged explicitly so it isn't found the way `ENG-010`'s
missing RLS was, mid-review rather than at design.

## Log

Append-only. One line per state transition, newest last.

- `2026-09-01` `(none) → intake`, held (product-manager, `scheduled` event
  pass, context `launchd`). Raw request arrived via control-center, filed
  under a stale `ENG-011` reference — reallocated `ENG-026`. Ran the full
  request-readback (PM reading + blind architect reading, both against the
  raw input only): one material divergence found — the title's own
  per-channel visibility ask is not delivered by any of the body's three
  tasks (time-clocks, smart filters, promo badges). Raised as a standing
  question rather than guessed
  (`inbox/2026-09-01-eng026-visibility-toggle-question.md`), two readings
  offered. Held at `intake` pending the answer, per
  `skills/request-readback/SKILL.md` step 5 — no PRD, no sizing, no G1 yet;
  none of those are legitimate before the ambiguity clears. `chained: none`
  — waiting on the approver.

- `2026-09-02` `intake → shaped → awaiting-scope` (product-manager, `watch`
  event pass, context `launchd` — the hand-edited answer on
  `inbox/2026-09-01-eng026-visibility-toggle-question.md` is what this event
  caught). Mode check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty, falls through).

  **Answer confirmed Reading B and went well beyond it** — an exact schema
  (three booleans, exact defaults), exact discovery semantics
  (capability-gated, not availability-gated), and exact query logic. Read as
  an approver-authored spec, not a plain description — per the same
  precedent `ENG-009` set reusing `ENG-008`'s already-a-spec answer, no
  second blind reading run on top of it.

  **Scoped down from the original four-capability request to this one
  piece** — the only one the answer actually specifies. Same reasoning
  `ENG-008`/`ENG-009`/`ENG-010` used splitting one influencer-board request
  into three tickets by risk profile and dependency shape, applied here to a
  request that bundled visibility, operational status, smart filters, and
  promo badges under one title. Full reasoning: PRD, "Why this ticket is
  narrower than the original request".

  **Sized `M`** (revised down from the original intake's provisional `L`,
  which was sized against the full, unscoped four-capability request). A
  three-boolean migration and query-shape change, a small admin toggle UI,
  and a consumer-facing filter-chip change — smaller than `L` once the other
  three capabilities are deferred, but three repos keeps it above `S`.

  **PRD written**: `agents/product-manager/specs/
  ENG-026-foodswipe-channel-visibility.md` — requirements tagged by
  provenance (5 Confirmed directly off the approver's answer, 1 Proposed
  default flagged for G1 to confirm or correct, 1 Inferred risk named and
  deliberately not resolved at this stage).

  **G1 required** — full lane, `L`-adjacent multi-repo scope, not XS/bug/
  chore. Wrote `inbox/2026-09-02-eng026-g1-scope.md` (`agent:
  product-manager`, `gate: scope`, `project: restaurant-marketplace`,
  readback at the top per `request-readback/SKILL.md` step 8, recommendation
  to build as scoped). Ran `departments/engineering/lib/eng-notify.sh raise`
  — see the item's own frontmatter for the result and `notified:` timestamp.

  Moved `inbox/2026-09-01-eng026-visibility-toggle-question.md` →
  `inbox/_handled/` with a processed footer. Journaled in
  `agents/eng-manager/config/decision-journal.md`.

  **2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
  of 4. **Consequence:** approver-facing WIP 5/2 → **6/2**, further over
  cap — `ENG-016` is the board's own precedent that an `awaiting-scope`
  ticket with a raised G1 counts toward this cap exactly like a merge
  request does (both are "tickets whose path still runs through the
  approver," per `eng_build_loop.md`'s Guards section), so this ticket's own
  G1 is no exception. Not held back by that cap anyway: the guard blocks
  *starting new work that will need the approver*, and this shaping was
  already underway (readback run, question raised 2026-09-01) before
  tonight — finishing it is completing in-flight work, not starting fresh
  work while over cap. `machine_wip` unaffected — shaping is not gated by
  that slot either way.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** this pass's own item raised and stamped above.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-026`) and
  whole-board: see board index.
