---
id: ENG-034
title: Public catering form — category-grouped dish picker, gated by owner opt-in
project: config-site-builder
type: feature
size: M
time_estimate: ~1.5-2 days
time_spent: build (single session)
time_remaining: review + quality + security + release-readiness rounds (not yet started)
severity: P2
priority:
state: building
owner: frontend
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-03
updated: 2026-09-04
branch: feat/ENG-034-catering-menu-selector-public-form (config-site-builder@62b3ca0)
depends_on: [ENG-033]
blocks: []
parent: ENG-016
links:
  prd: agents/product-manager/specs/ENG-016-catering-quote-generator.md
  design: agents/architect/designs/ENG-016-catering-quote-generator.md
  adrs: [ADR-008, ADR-009]
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

The public catering form has no way for a customer to select menu items —
`Catering.tsx`'s own "How It Works" copy already promises "2. Customize Your
Menu," a step that exists nowhere in the code today.

## Outcome

A new `CateringMenuSelector` component (category-grouped dish picker,
quantity + per-dish note, controlled, no fetch or config read of its own)
mounts on `CateringForm` when the gate is open:

```
orderFormEnabled =
     config.catering?.orderFormEnabled === true          // ADR-009
  && effectiveHasMenu === 'page'
  && effectiveMenu.length > 0
```

resolved per selected location, reusing `CateringForm`'s existing
`selectedLocation` derivation. Gate closed → the form renders exactly what it
renders today, byte for byte (AC-9). Gate open: fulfillment option labels and
descriptions come from `config.catering.fulfillmentCopy[value]` when present
(ADR-008 — no new fulfillment values, no remap), `requirements` loses its
`required` attribute and becomes general notes, `email` becomes required
(AC-11, a deliberate behaviour change on this branch only), and two submit
actions replace one — "Submit Quote Request" (needs ≥1 selection) and "Skip &
Have Someone Contact Me" — both validating the same required-field set
client-side. Changing `restaurant_id` mid-form resets selections (visibly),
matching the existing `delivery_method` reset behaviour.

`src/types/restaurant.ts` gains the two new `CateringPageContent` keys.

## Notes

Design's `## Interfaces` → "`config-site-builder` — the gate, and what it
gates" and "`CateringMenuSelector` — new component" have the exact gate
expression, prop shape (`{ menu, value, onChange }`), the menu-reading
pattern to match (`MenuList.tsx`'s own `(menu.categories||[]).map` over
`(category.items||category.dishes)`, both field names live), and the
selection-identity rule — composite `${menuIndex}-${categoryIndex}-
${itemIndex}` key, never dish name (repeats across categories) or `item.id`
(optional, can be absent). Called out in the design's own `## Risks` as the
largest single piece of new logic in this ticket.

`depends_on: [ENG-033]` — last in the design's Rollout order; the picker
POSTs `action_type`/`selections`, which only `ENG-033` makes the endpoint
understand. Full sequencing rationale:
`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`.

## Log

- `2026-09-03` `(created) → ready` (eng-manager, `work-breakdown`,
  `continue ENG-016` event pass) — sub-ticket of `ENG-016`, sequence 4 of 4,
  last in the chain. Held at `ready`: `depends_on: [ENG-033]` not yet
  `shipped`. `time_estimate` ~1.5-2 days. `chained: none` — waiting on a
  sibling, not agent-actionable yet.

- `2026-09-04` `ready → building` (frontend, `continue ENG-034` event pass,
  per the prior `watch (launchd)` pass's own `chained: ENG-034` — `ENG-033`
  shipped, satisfying this ticket's sole dependency). Mode clean
  (`MODE=active`). Pre-pass `eng-gate-check.sh`, scoped + whole-board: both
  exit 0.

  Built all three files the design's `## Components` table names for this
  surface (`src/types/restaurant.ts`, new `CateringMenuSelector.tsx`,
  `CateringForm.tsx`). No gate this hop, no receipt written. Self-tested:
  `npm install` (first ever in this worktree), `npm run lint` (both
  touched/new files clean; `restaurant.ts`'s 4 hits confirmed pre-existing
  via `git stash`), `npm run build` clean, `npx tsc --noEmit` clean (beyond
  this project's own defined check surface, run for extra rigor). Committed
  `config-site-builder@62b3ca0`
  (`feat/ENG-034-catering-menu-selector-public-form`, branched fresh off
  `origin/main` — the worktree's prior branch was `ENG-016`'s own, never
  diverged), pushed. Full reasoning and every interpretation call:
  `agents/eng-manager/notebook/2026-09-04-eng034-build.md`.

  **1 transition**, under the cap of 4. Machine WIP unaffected — still 1/1,
  `ENG-016` family, its last sibling now dispatched. Dead-end sweep (scoped
  to this event): no other ticket touched. Notify sweep (current
  `2026-09-04T16:13:26Z`): `ENG-028`'s G1 crossed 24h with no `nudged:`/
  `decision:` (`notified: 2026-09-03T16:10:27`) — nudged
  (`lib/eng-notify.sh nudge`), stamped `nudged: 2026-09-04T09:13:37`
  (copied verbatim from the trace log, same standing local-time-labeled-as-
  UTC convention this board already uses). `ENG-027`/`ENG-030` already
  carry their one-time nudge. One observation filed (`observations.md` —
  ticket-log length convention). Step 6b: not run — product code internal
  to one repo, no receipt path/state name/config key/cross-agent artifact
  involved. Journal: n/a — no gate answered this hop.

  `chained: ENG-034` — `building` is agent-owned (next hop: code review,
  principal-engineer); not the approver, not blocked, not terminal, not held
  by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-034` before this pass exits. Post-pass `eng-gate-check.sh`,
  scoped + whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass has
  used; the commit-convention question remains open, not re-decided here.
