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
priority: now
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-01
updated: 2026-09-03
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md
  design: agents/architect/designs/ENG-026-foodswipe-channel-visibility.md
  adrs: [ADR-010]
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

- `2026-09-03` no state change — duplicate board file for this same ticket
  found and retired (eng-manager, `scheduled` event pass, context
  `manual-drain`, whole-board dead-end sweep). The rescope logged directly
  above was written to a **new** file (this one) instead of editing
  `ENG-026-foodswipe-multichannel-filters-and-promo-engine.md` — the
  original ticket file — in place, unlike `ENG-016`'s Piece 1, which kept
  its original file and id through an equivalent rescope. The old file was
  never deleted or marked superseded, so two board files carried
  `id: ENG-026` at once: this one (live, gated, cross-referenced
  everywhere) and the original (frozen at `state: intake` since
  2026-09-01, `priority: now`, never touched again). Confirmed
  `lib/eng-gate-check.sh` has no id-uniqueness check across board files —
  nothing mechanical would ever have caught this.

  **One real signal was stranded on the orphaned file, not just stale
  prose.** Commit `a862607` (2026-09-02 21:18:16, "capture uncommitted
  gate-answer bookkeeping before switching hosts") stamped `priority: now`
  on the old file as partial bookkeeping ahead of full gate processing —
  the same commit parked `ENG-016`'s `changed` G1 answer the same way
  ahead of its own full processing later that night. The 23:56 pass that
  did this ticket's full processing wrote the new file from the approver's
  answer directly and never carried that `priority: now` stamp forward.
  Not applied here: whether `now` was meant for the toggle piece
  specifically (already in-flight on its own G1 regardless of priority) or
  for the three deferred capabilities (not filed as tickets yet, by
  design — see Notes above) is genuinely unclear from the commit message
  alone, and priority is the approver's field to set, never this pass's to
  infer (`eng_build_loop.md` step 6, "never write to priority yourself").
  **Flagged so it isn't lost twice: when the deferred operational-status/
  filters/promo-badge work is eventually filed as its own ticket(s), check
  this entry and ask whether `now` still applies.**

  The old file's fuller four-way readback split (A: visibility toggle: B:
  operational-status engine; C: consumer filters; D: promo-badge overlay —
  more detail than this ticket's own Notes restate) is preserved in git
  history, last live at commit `a862607`:
  `git log --follow -- agents/eng-manager/board/ENG-026-foodswipe-multichannel-filters-and-promo-engine.md`.
  Removed the file from the live board directory (`git rm`) now that its
  content is folded in here and its continued presence was the actual
  hazard, not the history itself. Observation and a proposal filed
  (`observations.md`, `proposals.md`): the systemic gap is that rescoping
  a ticket by writing a new file loses non-prose frontmatter (`priority`,
  and anything else the prose doesn't restate) silently — the fix is to
  always rescope a ticket in place, same file and id, per `ENG-016`'s own
  precedent, never fork a new file for an id that already exists.

  **0 transitions** — `state`/`owner` unchanged (`awaiting-scope`/
  `approver`). Approver-facing WIP unaffected — no gate touched, no new
  item raised.

  `chained: none` — `awaiting-scope`, owned by the approver; unaffected by
  this bookkeeping fix. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  whole-board: see board index.

- `2026-09-03` **`awaiting-scope → designed`, `owner: approver →
  architect`** (`decision` event pass, context
  `inbox/2026-09-02-eng026-g1-scope.md`). Reading map for `decision`: steps
  4 and 8c, plus step 6 (this answer advances the ticket into a
  machine-owned state) and the not-negotiable set (step 1, 7, 8b, 9, 10;
  *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check clean
  (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-026`) and
  whole-board: both exit 0, clean.

  **The answer:** `approved` (`decided: 2026-09-03T15:51:04.400168+00:00`).
  No additional comment. Read as accepting the recommendation exactly as
  scoped — this piece only, the other three bundled capabilities deferred
  as separate future tickets — and as accepting requirement 6's proposed
  default (staff-set via `aiorders-admin-hub`, not restaurant self-service)
  since the readback's explicit "correct this if wrong" went uncorrected.

  **One gap found and fixed while processing this decision:** the PRD
  (`agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md`)
  had neither the frontmatter block nor the `## Decision` section every
  sibling PRD carries — added both per `templates/prd.md` (`status:
  approved`, `decided:` stamped, a `## Decision` section naming requirement
  7's rollout/backfill question as still open). Not a proposal — a
  one-document authoring gap, fixed in the same edit this decision already
  required.

  Journal entry written (`agents/eng-manager/config/decision-journal.md`).
  Gate item's own `## Decision` footer already carried the answer;
  appended a processed note and moved the file
  `inbox/2026-09-02-eng026-g1-scope.md` →
  `inbox/_handled/2026-09-02-eng026-g1-scope.md`.

  **Requirement 7 (rollout/backfill for existing merchants) stays open,
  inherited here at `designed` — not resolved by this approval and not
  silently defaulted.** A straight column-default migration would set
  every existing merchant to `has_order_food: true, has_dine_in: false,
  has_catering: false`, silently dropping any merchant that already does
  dine-in/catering today out of those tabs. This needs a real look at live
  data (does any existing column/tag carry a usable signal to backfill
  from, or does every merchant genuinely start blank and wait for staff to
  opt them in) before this reaches `building` — PRD Risks, and the
  ticket's own Notes above, both already flag it; restated here so this
  hop doesn't have to re-derive it.

  **Machine WIP re-checked fresh from every ticket's own frontmatter, not
  the cached board header:** `1/1`, occupied by `ENG-024`
  (`ready-to-ship`, not yet `shipped`). Irrelevant to this transition —
  `designed` sits outside the counted `ready`..`ready-to-ship` range;
  shaping/design work is backlog grooming regardless of who holds the
  slot (`eng_build_loop.md` step 6).

  **1 transition** (`awaiting-scope → designed`), well under the cap of 4
  — the actual design work is the architect's own next hop, not attempted
  inline here, same precedent `ENG-016`'s and `ENG-015`'s identical
  G1-approved hand-offs already set. **Consequence:** ticket now owned by
  `architect`, outside both the machine-WIP and approver-WIP counted
  ranges. Approver-facing WIP uncapped; this G1 drops off the "Waiting on
  the approver" list — same shape `ENG-013`'s and `ENG-016`'s closures
  already set.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract. **Notify sweep:** nothing raised
  this pass — no new gate item written. **Observations/proposals filed:**
  none — the PRD-template gap above was fixed inline, not filed, as a
  one-document miss rather than a recurring mechanism gap.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-026`) and whole-board: both exit 0, clean.

  `chained: ENG-026` — `designed` is agent-owned (`architect`, via
  `tech-design/SKILL.md`, triggered by this exact state); not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-026`
  before this pass exits — confirmed queued (`traces/.pending`, appended
  behind four already-outstanding events).

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` no state change — **tech design written** (architect,
  `continue` event pass, context `ENG-026`). Reading map for `continue`:
  steps 6 and 6b (step 2's mid-PRD checkpoint doesn't apply — the PRD is
  already complete/approved) plus the not-negotiable set (steps 1, 7, 8b, 9,
  10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check
  clean (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-026`) and
  whole-board: both exit 0, clean.

  **Read the live codebase across all three touched repos before designing**
  (`aiorders-api`, `aiorders-admin-hub`, `restaurant-marketplace`) rather
  than trusting the PRD's own framing — surfaced two facts the PRD couldn't
  have known and one the ticket's own Notes flagged as needing exactly this
  look:

  1. `restaurant-marketplace`'s own `supabase/functions/*` was deleted
     2026-08-23 (`f733e68`, "now owned by aiorders-api") — its 16-commits-
     behind worktree (`eng/base`) still showed the old handler code, which
     would have misdirected every backend change in this design had it not
     been checked against `origin/master`/`origin/main` directly. The
     discovery RPC (`get_restaurants_optimized`) and its handler live in
     `aiorders-api` today; `restaurant-marketplace` is frontend-only for
     this ticket.
  2. `has_dine_in` collides with a real, pre-existing, currently-dead
     `dine_in` column — staff-editable today from the exact admin surface
     requirement 6 names, read by nothing on the consumer side, and absent
     from `aiorders-admin-hub`'s own generated Supabase types (consistent
     with either "real column, stale typegen" or "never real, dead form
     field" — not resolvable from static analysis alone). Design hands
     `database` a concrete, conditional instruction rather than guessing
     either way (design doc, Data section).
  3. **Requirement 7 (rollout/backfill), open since PRD stage, resolved as
     far as static analysis permits:** `has_order_food` defaulting `true`
     for every row reproduces today's actual behavior exactly (no existing
     gate restricts that tab at all today). `has_catering` backfills from
     `live_catering` — `NOT NULL`, already populated, already this
     codebase's working stand-in for "does this restaurant do catering"
     per `brand-portal/catering.ts`. `has_dine_in` is the one piece that
     stays genuinely open, conditional on the live-schema check in (2) —
     named plainly rather than defaulted silently, per the ticket's and
     PRD's own explicit flag.

  **Design written:**
  `agents/architect/designs/ENG-026-foodswipe-channel-visibility.md`. Three
  repos, `touches_data: true`, `touches_models: false`. Full template used
  (M-sized but genuinely three-repo with a real schema collision to resolve
  — sized to the change's actual complexity, not just its estimate band).

  **One ADR, no G2.** `ADR-010` records evaluating "Open Now" post-query in
  TypeScript (a ported, not re-derived, existing client-side parser) rather
  than as a SQL predicate — reversible, no data migration either way, but a
  real trade-off (approximate pagination under `open_now=true`) a future
  engineer would otherwise have to re-derive from behavior alone. Consolidating
  `get_restaurants_optimized`'s orphaned migration into `aiorders-api`
  (finding 1, above) is **not** a new ADR — it completes `ADR-003`'s own
  migration-ownership call rather than making a new one, cited in the design
  instead.

  **No one-way doors** — checked against all six criteria in the design's
  own table, none apply. New columns, new RPC parameter (`DEFAULT NULL`,
  backward-compatible), new shared util — all reversible, none change auth,
  vendor, or public-contract shape.

  **One proposal filed, not fixed inline:** `admin-portal/handlers/
  restaurants.ts`'s `updateRestaurant()` has no field allow-list at all —
  found while confirming how the new flags reach the database, distinct
  from the already-tracked ownership-check finding on this same function
  (`proposals.md`, 2026-08-29, corrected 2026-09-03 now that `ENG-015`
  fixed the ownership half). This ticket's own three new fields ride the
  already-open surface; not this ticket's to fix, per `eng_build_loop.md`
  step 3 — filed to `proposals.md` instead of fixed as a drive-by.

  **Step 6b (artifact-mention enumeration): not run, and here's why rather
  than a silent skip.** Nothing in this design renames or introduces a rule
  about a business-os-process artifact (a receipt path, a state name, a
  config key, a file another agent is told to produce) — `links.design`/
  `links.adrs` are filled per the existing, unchanged convention, and the
  design/ADR file-path patterns are unchanged. Same reasoning `ENG-024`'s
  own `building` hop already recorded for the identical question.

  **Machine WIP re-checked fresh from every ticket's own frontmatter, not
  cached:** `1/1`, occupied by `ENG-016` at `ready` (not yet `building`) —
  every other ticket on the board sits at `designed`, `blocked`, `shaped`,
  `awaiting-scope`, `verified`, or `dropped`; none in `building`..
  `ready-to-ship`. **Ticket stays at `designed` regardless — held by the
  machine WIP cap, not a gate.** `eng_build_loop.md`'s Guards section is
  explicit: "nothing new enters `ready` until the one ticket in flight
  reaches `shipped`" — `ENG-016` sitting at `ready` (not even started
  building) is squarely "in flight" by that rule. Design work itself is
  exempt from the cap (`designed` is in the cap-exempt set); entering
  `ready` is not, so this pass does not attempt that transition — no
  branch created in any of the three worktrees, no code written. Same
  precedent `ENG-014`/`ENG-017`/`ENG-019`/`ENG-020`/`ENG-021`/`ENG-023`/
  `ENG-025` already set, all currently parked at `designed` for the
  identical reason.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract. **Notify sweep:** nothing raised
  this pass — no G2, no gate item written, nothing to notify or nudge.
  Approval cap and approver-facing WIP both unaffected.

  **0 transitions** — `state`/`owner` unchanged (`designed`/`architect`);
  the cap, not the hop budget, is what stopped it. Machine WIP unaffected
  (still `1/1`, `ENG-026` was never inside the counted range and still
  isn't). Approver-facing WIP and approval cap both unaffected — no gate
  raised.

  `chained: none` — held by the machine WIP cap (`1/1`: `ENG-016`
  occupying), one of the documented no-chain conditions ("held by a cap
  (WIP or approvals)"), not waiting on the approver and not blocked. The
  next hop (`ready`, work-breakdown) fires once `ENG-016` reaches `shipped`
  and a `scheduled`/`continue`-elsewhere pass finds the slot free and this
  design already complete — nothing to re-derive at that point, only the
  state/owner fields to flip. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-026`) and
  whole-board: both exit 0, clean.

  business-os itself left uncommitted — same standing default every pass
  today has used; the commit-convention question remains open, not
  re-decided here.
