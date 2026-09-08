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
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-01
updated: 2026-09-07
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

## Breakdown

Decomposed 2026-09-07 (`work-breakdown/SKILL.md`) into four sub-tickets, one
per owning-agent/repo pair, sequenced as a DAG per the design's own Rollout
order (schema first; the two independent last steps — admin toggle, consumer
UI — each gated only on their own real prerequisite, not on each other):

| Sub-ticket | Surface | Repo | Depends on | State |
|---|---|---|---|---|
| `ENG-044` | database | `aiorders-api` | — | `building` |
| `ENG-045` | backend | `aiorders-api` | `ENG-044` | `ready` |
| `ENG-046` | frontend | `aiorders-admin-hub` | `ENG-044` | `ready` |
| `ENG-047` | frontend | `restaurant-marketplace` | `ENG-045` | `ready` |

No sub-ticket for `admin-portal/handlers/restaurants.ts` (no code change —
the existing write path already passes the three new fields through with
zero edits) or for `aiorders-admin-hub`'s generated `types.ts` (regenerated,
not hand-written, folded into `ENG-046`'s own build step). This parent
carries no diff of its own from here on — its evidence is its children's
(`ADR-003`-class exemption). It moves directly to `shipped` once all four
children reach `shipped`/`verified`/`dropped` with at least one
`shipped`/`verified`, without itself passing through
`in-review`/`in-qa`/`in-security`. Full reasoning — the surface split, the
DAG sequencing rationale (including why `ENG-046` does not wait on
`ENG-045`), the AC-ownership mapping, and every field decided without an
explicit rule — is in
`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`.

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

## 2026-09-07 — continue (`ENG-021`): slot freed, claimed the same pass — `designed → ready`

`continue` event pass, context `ENG-021` — `ENG-021` itself reached
`verified` this pass (`ADR-003`-class exemption, both children settled) and
freed the machine-WIP slot. Per `eng_build_loop.md` Guards → Machine WIP
limit, amended 2026-09-06 ("never idle"), the pass that frees a slot fills it
in the same pass rather than leaving it for the next dispatch-scoped sweep —
full reasoning on `ENG-021`'s own board-file log for this date.

To-do column (`intake`/`shaped`/`awaiting-scope`) had nothing
machine-actionable (`ENG-018`, `ENG-028`, `ENG-042`, `ENG-043` all genuinely
on an unanswered approver question, confirmed via `inbox/` directly — no item
carries a `decision:`), so the pick came from the held-for-slot pool, same
precedent this ticket's own 2026-09-03 entry already anticipated:
`designed` tickets with a completed design and no one-way door, deferred only
by the cap. `ENG-026` and `ENG-027` both carry `priority: now`; lowest id
decided.

Re-confirmed this ticket's own design output directly rather than trusting
the pool description: `agents/architect/designs/ENG-026-foodswipe-channel-visibility.md`
exists, this ticket's own 2026-09-03 design-pass log above states **No
one-way doors** plainly (checked against all six criteria in the design's own
table), `ADR-010` recorded with no G2 owed, `depends_on: []`. `tech-design/SKILL.md`
step 11 routes exactly that case to `ready`, owner `eng-manager`, no G2 —
matching what this ticket's own prior log already anticipated ("the next hop
... fires once ... a ... pass finds the slot free and this design already
complete — nothing to re-derive at that point, only the state/owner fields to
flip").

`ENG-026` moved `designed → ready`, `owner: architect → eng-manager`. **1
transition**, well under the cap of 4. **Consequence:** machine WIP
`0/1 → 1/1`. Stopped there — work-breakdown/building is new implementation
work, chained instead rather than attempted inline, same handoff shape every
prior dispatch on this board has used.

**Dead-end sweep:** out of scope for `continue` (narrower contract — the
event's own To-do/held-for-slot sweep, recorded on `ENG-021`'s own log,
covers this). **Notify sweep:** nothing raised this pass (no G2, no gate item
— routing per step 11 needed none). **Observations/proposals:** none new.
**Exceptions/journal:** n/a.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`) and whole-board: both
exit 0, clean.

`chained: ENG-026` — `ready` is agent-owned (`eng-manager`, work-breakdown
next per `tech-design/SKILL.md` step 11); not the approver, not blocked, not
terminal, not held by a cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-026`
before this pass exits — confirmed queued, not dropped:
`traces/eng-loop-2026-09-07.log`'s `02:30:13 continue — pass in flight,
queued as pending` line and `traces/.pending` (`1 watch launchd` then `1
continue ENG-026`) both show it queued behind this pass's own single-flight
lock, to drain the moment this pass exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-07 — continue: work-breakdown — `ready → building`, four sub-tickets

`continue` event pass, context `ENG-026`. Reading map for `continue`: steps 6
and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
instructed*, *The four lanes*, *Guards*). Mode check clean (`MODE=active`).
Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`) and whole-board: both
exit 0.

Ran `work-breakdown/SKILL.md`. Autonomy check: `aiorders-api`,
`aiorders-admin-hub`, and `restaurant-marketplace` are all L1 — proceeds.
Machine WIP re-checked fresh from every ticket's own frontmatter: `1/1`, held
by `ENG-026` itself (the only ticket outside terminal/pre-ready states) — a
ticket's own family isn't a second occupant of its own slot, same reading
`ENG-016`/`ENG-019`/`ENG-021` already established, so work-breakdown proceeds.

Split by the design's own `## Components` table into four owning-agent/repo
sub-tickets — `ENG-044` (database, `aiorders-api`), `ENG-045` (backend,
`aiorders-api`), `ENG-046` (frontend, `aiorders-admin-hub`), `ENG-047`
(frontend, `restaurant-marketplace`) — the first time `frontend` has split
into two sub-tickets on the same parent since `ENG-016`'s own family (two
repos, one surface each). No `admin-portal` or `types.ts` sub-ticket — both
no-diff (see `## Breakdown` above). Sequenced as a DAG, not a single chain:
`ENG-044` first (no dependency); `ENG-045` and `ENG-046` both
`depends_on: [ENG-044]` only, independent of each other; `ENG-047`
`depends_on: [ENG-045]`. Read literally per the `ENG-016`/`ENG-019`/`ENG-021`
precedent — "a sub-ticket whose dependency isn't shipped doesn't start" means
*shipped*, not merely built. Full reasoning, the AC1-AC5 ownership mapping,
and every field decided without an explicit rule:
`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`.

**Routing:** `ready → building`, owner stays `eng-manager` — no engineer
builds a four-surface parent with no diff of its own (`ready`'s exit
condition, `definition-of-done.md`, is satisfied by the breakdown itself).
`ENG-044` dispatched straight to `building` (no dependency); `ENG-045`,
`ENG-046`, and `ENG-047` all stay `ready` (unmet `depends_on`).

**1 transition** on this ticket (`ready → building`). Machine WIP: still
`1/1`, same family (`ENG-026` + `ENG-044`..`047`), not `2/1` — see notebook.
No gate raised, no G1/G2/G3, no one-way door.

**Dead-end sweep:** out of scope for `continue` (narrower contract — act on
the ticket this event names). **Notify sweep (not-negotiable step 7, run
against every open `inbox/` item, not just this ticket's) — done wrong at
first, corrected here rather than left standing.** Initial check read
"current time" via `date -u` (UTC, `2026-09-07T09:37:33`) and diffed it
directly against four items' `notified:` frontmatter, reading all four as
30-31h old and nudging all four (`lib/eng-notify.sh nudge`, all exit 0,
`traces/eng-notify-2026-09-07.log`). **That math was wrong** — cross-checking
`traces/eng-notify-2026-09-06.log` proves `notified:` stamps are local PDT
wall-clock, not UTC (`ENG-018`'s `notified: 2026-09-06T03:13:31` matches that
log's own `[03:13:31] sent: active ...eng018...` line exactly), the same
skew `observations.md` already flagged twice (2026-09-06, 2026-09-07 rows).
Corrected, local-to-local (nudges actually sent ~02:37:56-58 PDT this pass):
`ENG-028`/`ENG-042` (`notified: 2026-09-06T02:28:29`) were genuinely
~24h09m — correctly due. `ENG-018` (`notified: 2026-09-06T03:13:31`, true
age ~23h24m) and `ENG-043` (`notified: 2026-09-06T02:47:56`, true age
~23h50m) were **not yet due** — both nudged 10-36 minutes early. Not
reverted: the Telegram sends already happened and `nudged:` accurately
records when, so the honest fix is this corrected account, not a rewritten
frontmatter timestamp. **Exactly one nudge, ever** — none of the four had a
prior `nudged:`, so all four are now spent, two of them slightly ahead of
schedule. Third occurrence of this exact skew — filed as a proposal rather
than a third observation (`proposals.md`, this date), per this repo's own
three-strike convention. `PROP-2026-W36` (`notified: 2026-09-06T18:57:12`,
~14h40m by either convention — well clear of the boundary either way) is
correctly under 24h — no action. `ENG-016`'s continue-to-Piece-2 question
already carries its one-ever `nudged:` — no action.

**Board update** — In-flight table: `ENG-026`'s own row (`state: building`,
`updated`); new rows added for `ENG-044`, `ENG-045`, `ENG-046`, `ENG-047`;
`next_id` advanced `ENG-044 → ENG-048`; header's machine-WIP paragraph noted.
Live file held three dated entries — under the keep-three threshold, so
nothing rolled to `_index-archive.md` this pass (no new dated `## {date} —`
entry was added; this dispatch is recorded as a header paragraph, same
convention `ENG-016`'s/`ENG-019`'s/`ENG-021`'s own work-breakdown dispatches
already used).

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`) and whole-board: both
exit 0, clean.

`chained: ENG-044` — the only child with a met dependency and something
agent-actionable now. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-044`
before this pass exits — confirmed queued, not dropped: `traces/.pending`
shows `1 continue ENG-044` appended behind three already-outstanding `watch
launchd` events. This pass (`continue ENG-026`) itself still holds the
single-flight lock at fire time, so the fire queues rather than launches, and
the drain will run the three queued `watch` events first, then this one, the
moment this pass exits. `chained: none` on `ENG-026` itself (parent has no
action until a child reports back) and on `ENG-045`/`ENG-046`/`ENG-047`
(each waiting on its own unmet dependency) — recorded on each ticket's own
log.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.

## 2026-09-07 — continue: child dispatched — no state change on ENG-026 itself

`continue` event pass, context `ENG-026` (eng-manager). `ENG-044` →
`shipped`, confirmed via `gh pr view 19` (`MERGED`) and `git merge-base
--is-ancestor` against `origin/main`, not trusted off frontmatter alone
(which changed `blocked → shipped` mid-pass — control center, live).
Clears `depends_on: [ENG-044]` for `ENG-045`/`ENG-046` both (Guards, "two
readings closed" (a)). Dispatches one, per this ticket's own
work-breakdown-notebook precedent: `ENG-045` (lower id, unblocks
`ENG-047`). `ENG-046` stays `ready`, turn deferred; `ENG-047` stays
blocked (`depends_on: [ENG-045]` unmet). No gate ran. Machine WIP
unaffected, `1/1`, family-held. Notify sweep: nothing due. One observation
filed (`observations.md`, this date). Full reasoning:
`agents/eng-manager/notebook/2026-09-07-eng026-child-dispatch.md`.

Post-pass `lib/eng-gate-check.sh`, scoped and whole-board: exit 0, clean.

`chained: ENG-045` — fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-045`,
confirmed queued (`traces/.pending`). `chained: none` on `ENG-026` (parent,
no action) and `ENG-046`/`ENG-047` (not this pass's turn / unmet
dependency).

business-os left uncommitted — standing default, commit-convention
question still open.

## 2026-09-07 — scheduled: all four children now shipped — ADR-003 exemption met, closing hop chained rather than run inline

`scheduled (launchd)` safety-net sweep, 19:0x PDT. Reading map: whole
document, not narrowed (never narrowed for `scheduled`). Mode check clean
(`.env` → `MODE=active`).

This ticket's own last entry above left `ENG-045` dispatched and
`ENG-046`/`ENG-047` waiting their turn. Since then all three reached
`shipped` **via the control center dashboard, not a build-loop pass** —
each one's own board file says so explicitly ("Advanced from the dashboard
rather than by a build-loop pass; the loop's own ancestry check on its next
pass will agree"). No dashboard flip fires `continue ENG-026`, so the
parent's own closing hop was never triggered — exactly the class of gap a
`scheduled` sweep exists to catch, since the intervening `continue ENG-049`
pass was correctly scoped only to `ENG-049` and had no reason to re-check
this family.

**Re-verified fresh, not trusted off frontmatter or the dashboard's own
say-so** — same bar every prior merge-detection on this board has held to:

- `ENG-044`: `origin/feat/ENG-044-foodswipe-channel-visibility-schema` is an
  ancestor of `origin/main` (`aiorders-api`, fetched fresh). Review `pass`,
  security `pass`, QA `no suite` (no `.ts` touched — same shape
  `ENG-031`/`ENG-037` already established).
- `ENG-045`: `origin/feat/ENG-045-foodswipe-channel-visibility-discovery-handlers`
  is an ancestor of `origin/main`. Review `pass` (round 2), security
  `pass`, QA `pass`.
- `ENG-046`: `origin/feat/ENG-046-foodswipe-channel-visibility-admin-toggles`
  is an ancestor of `origin/main` (`aiorders-admin-hub`, fetched fresh).
  Review `pass`, security `pass`, QA `no suite`.
- `ENG-047`: `origin/feat/ENG-047-foodswipe-open-now-and-channel-display` is
  an ancestor of `origin/master` (`restaurant-marketplace` — default branch
  is `master`, not `main`, per `config/projects.md`; fetched fresh). Review
  `pass`, security `pass`, QA `no suite`.

All four children `shipped`, at least one actually shipped — the `ADR-003`
parent exemption (*Enforced vs instructed* → "Enforced, and stated at no
step above") is satisfied. **Not processed inline this pass** — same
precedent `ENG-016`'s, `ENG-019`'s, and `ENG-021`'s own closures already
set: the parent's own `building → shipped → verified` transition, with a
full `acceptance-check` run (the trigger has no parent carve-out), gets its
own dedicated session rather than riding this board-wide sweep.

**Also fixed while here, same class as the `ENG-014`/`ENG-025` stale-owner
precedent:** all four children still carried `owner: approver` from their
prior `blocked` state; the dashboard's merge-detected flip to `shipped`
didn't update it, and every already-`verified` sibling on this board
(`ENG-038`, `ENG-040`, `ENG-041`) carries `owner: eng-manager` at this
stage instead. Corrected all four to `owner: eng-manager`. No functional
consequence — routing reads `state:`, not `owner:` — but left wrong it
misleads a reader about whose desk the ticket is on.

**Also checked while sweeping:** `ENG-048`/`ENG-049` (the only other family
in flight) — both PRs (`aiorders-api` #21, #22) confirmed still `OPEN`,
unmerged, via fresh `gh pr view`; no state change. `grep -l "^state:
blocked" agents/eng-manager/board/ENG-*.md` returns only those two — no
other ticket on the board is `blocked`. Machine WIP: `0/1` before and after
this entry — `ENG-026` and `ENG-027` are both containers holding zero slots
(Guards, 2026-09-07(b)); this entry frees nothing and fills nothing.
`IDLE-2026-09-07.md` (still open, unanswered) already covers the current
idle condition accurately — not reissued.

**1 transition on this ticket: none** — `ENG-026` itself stays `building`;
only its children's `owner` fields and this log entry changed.

Post-pass `lib/eng-gate-check.sh ENG-026` and whole-board: exit 0, clean.

`chained: ENG-026` — fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-026`
before this pass exits, for the dedicated closing hop (building → shipped →
verified, full acceptance-check).

business-os left uncommitted through this edit (this ticket file, the four
children's `owner:` fields) — standing default per the open
commit-convention question, not re-decided here.

## 2026-09-07 — continue: parent settled — `building → shipped → verified`, full acceptance-check from scratch, all four children closed with it

`continue` event pass, context `ENG-026`, per the prior `scheduled` sweep's
own `chained: ENG-026` (its dated entry, `_index.md`, this date — "the
dedicated closing hop"). Reading map for `continue`: steps 6 and 6b, plus
the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
lanes*; *Guards*) — step 2's mid-PRD checkpoint doesn't apply, the PRD has
been `approved` since 2026-09-03. Mode check clean (repo-root `.env` →
`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`) and
whole-board: both exit 0, clean.

**All four children re-checked fresh off their own frontmatter and, for the
first time on this board, against live production state directly — not
just git ancestry.** `ENG-044`/`045`/`046`/`047` all `state: shipped`,
`parent: ENG-026`, none dropped. `ADR-003`-class exemption met (all four
settled, all four actually shipped, well past the "at least one" floor).
`building → shipped`, no diff/review/QA/security hop of its own — same
handoff shape `ENG-016`'s/`ENG-019`'s/`ENG-021`'s own parent transitions
used.

**Ran `acceptance-check/SKILL.md` in full — a from-scratch walk, not a
rollup.** Unlike `ENG-021`'s family (both children had already run this
skill individually at their own shipping point), none of `ENG-044`–`047`
had: all four reached `shipped` via a **control-center dashboard action**,
which never fires `continue {ticket-id}`, so the skill's own trigger ("a
ticket enters state `shipped`") never ran on any of them. Confirmed before
concluding that: no `agents/product-manager/notebook/` file exists for any
of the four, and — checked against every other settled family on this board
(`ENG-031`/`033`/`034`, `ENG-038`/`039`, `ENG-040`/`041`) — every one of
those children's own frontmatter reads `state: verified`, not `shipped`.
This family's four did not. Real, not cosmetic: it means the PRD's own
promise had never actually been checked against the live-shipped thing for
any of these four, only against upstream review/QA/security proxies.

Walked all 5 PRD criteria directly against the merged, deployed code across
all three repos (fetched fresh: `aiorders-api` `origin/main` → `afc45cc`,
`aiorders-admin-hub` `origin/main` → `6d340c0`, `restaurant-marketplace`
`origin/master` → `0dc8af8`; all four PRs independently confirmed `MERGED`
via `gh pr view`). Went past git ancestry into actual deploy confirmation:
`aiorders-admin-hub`/`restaurant-marketplace` both show a `success`
Cloudflare Pages run against the exact merge commit (`gh run list`);
`aiorders-api` has no CI workflow at all, so used `supabase migration list
--linked` (both of `ENG-044`'s migrations show `local == remote` — applied
to the live production database, not just present on a merged branch) and
`supabase functions list`'s `updated_at` for the `restaurant-marketplace`
function (62 seconds after PR #20's own `mergedAt` — named honestly as
timing correlation, not a byte-for-byte diff, no committed anon key
available to call the live endpoint directly). **All 5 criteria pass** —
AC1 (migration/defaults, no regression), AC2 (staff view/set from
admin-hub), AC3 (flag-gated tabs, negative case holds under any `open_now`
value by construction), AC4 (closed-but-enabled still shows with a status
string, excluded only when `open_now` is explicitly true — both the
handler logic and the consumer UI), AC5 (rollout/backfill answered with
real live-schema evidence: 243 rows checked, 241 already `dine_in = true`,
backfilled from it — which also means the design's own single biggest
named risk, the Dine-In tab going near-empty at deploy, did not
materialize). No non-goal scope crept in (checked each child's actual diff
against the PRD's four deferred items and requirement 6's staff-only
default); cost `$0/month` as estimated, confirmed independently on all four
children's own release-readiness records. `shipped → verified`. Full
walk: `agents/product-manager/notebook/2026-09-07-eng026-acceptance.md`.

**Also flipped all four children `shipped → verified` in this same pass** —
not a second, separate acceptance-check per child, but each one's own AC
slice (already walked above) attributed on its own board file with a
pointer back here, closing the specific gap this pass's own investigation
found (see notebook's "Why this one is a from-scratch walk") and bringing
all four back in line with every other settled family on this board. Each
child's `owner` stays `eng-manager` (already corrected from a stale
`approver` by the prior `scheduled` sweep).

**2 transitions on the parent** (`building → shipped`, `shipped →
verified`), well under the cap of 4. **Machine WIP: unaffected, `0/1`
before and after** — per Guards (2026-09-07(b)), a parent holds no machine
slot in any state, and neither `ENG-026` nor its children were ever inside
the counted `ready`..`ready-to-ship` range at this point; this pass closes
out a family that was already outside it, not one that frees new capacity.

**Step 6b: neither condition met**, same reading `ENG-021`'s own check gave
its identically-bare G1. The PRD names three deferred items in prose ("a
future intake pass can pick them up individually") — not a "Feature shape
and sequencing" section naming a specific next ticket. The G1 answer was a
bare "approved," no sequence sign-off. Nothing filed.

**Nothing chained for a next ticket — deliberately, and this needs stating
plainly since drawing from the `designed`-state pool is exactly what put
`ENG-026` itself into `ready` on 2026-09-05.** That "held-for-slot pool"
practice is, as of today, an open, filed, unresolved tension:
`continue ENG-049` (same day, earlier) hit the identical fork — To-do empty,
only the `designed` pool available — read `eng_build_loop.md` step 6 fresh
in full rather than pattern-matching four prior board entries, found
nothing in the written document that actually authorizes drawing from
`designed`, and chose the literal reading: raised `IDLE-2026-09-07.md`
instead, and filed a proposal naming the tension
(`proposals.md`, 2026-09-07, devops). The `scheduled` sweep immediately
before this pass hit the same fork again and explicitly declined to
relitigate a same-day, considered call with no new information. This pass
makes the same choice a third time today, for the same reason: re-deciding
it now, with nothing new to inform the decision, would be relitigating, not
correcting. Independently re-confirmed rather than trusted off that sweep's
account: `grep -l "^decision:" inbox/*.md` returns nothing (still ten open
items, none answered); `ENG-018`/`ENG-028`/`ENG-042`/`ENG-043` (To-do) all
still genuinely blocked on their own unanswered G1/clarification;
`IDLE-2026-09-07.md` still open, still accurately describing this exact
condition (it already names `ENG-026`'s own family as not-yet-startable
work and reasons through the identical `designed`-pool tension for
`ENG-050`). Not reissued — "never raises a second while one is still
undecided."

**Dead-end sweep:** out of scope for `continue` (narrower contract — act on
the ticket this event names); this pass's own closing work already covers
its whole family. **Notify sweep:** every open `inbox/` item checked fresh
against local wall-clock `2026-09-07T19:33` PDT. Five items
(`ENG-016`-piece2, `ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`,
`PROP-2026-W36`) already carry their one-ever `nudged:` stamp — no action.
Four newer items (`ENG-048`, `ENG-049`, `ENG-050`, `IDLE-2026-09-07`) are
all well under 24h old (oldest ~3h29m) — no action. Nothing raised, nothing
nudged.

**8b:** one observation filed (`observations.md`, this date) — the
`supabase migration list --linked` / `functions list` substitute for a
missing CI run, worth reusing on future `aiorders-api` acceptance-checks.
One proposal **addended**, not filed fresh (`proposals.md`, this date,
appending point (4) to the existing 2026-09-07 dashboard-bypass row): none
of the four children had individually reached `verified`, unlike every
sibling family, because the dashboard flip skipped `acceptance-check`'s own
trigger entirely — closed for this family by this pass, but a
non-parent ticket dashboard-flipped to `shipped` has no equivalent forcing
function and would sit unchecked indefinitely. No `exception-request:`
found. **8c:** n/a — no G1/G2/G3/merge-request answered this pass.

**Board update, this pass:** `ENG-026`'s and all four children's frontmatter
(`state`, and `ENG-026`'s alone); `_index.md`'s In-flight table — all five
rows removed (all terminal now, nothing to replace them with). Live
`_index.md` held three dated entries before this edit; oldest (`continue
(ENG-049)`: security gate round 2) rolled to `_index-archive.md` per the
keep-three rule, done before this index's own new entry was written so the
count stays at three.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-026`, `ENG-044`, `ENG-045`,
`ENG-046`, `ENG-047`) and whole-board: all six runs exit 0, clean.

`chained: none — idle: nothing startable`. Machine WIP is `0/1`, genuinely free, but
nothing on the board can take it: To-do is empty of anything answered, and
the only other candidate pool (`designed`-state tickets, including the P0
`ENG-050`) is exactly the fallback this same day's own `continue ENG-049`
pass and the following `scheduled` sweep both declined to draw from,
pending the approver's read of the proposal naming that tension. Not a new
idle episode — `IDLE-2026-09-07.md` already open and accurate, not
reissued.

business-os itself left uncommitted through this pass's edits (this
ticket's own file; all four children's board files;
`agents/product-manager/notebook/2026-09-07-eng026-acceptance.md`;
`proposals.md`; `observations.md`; `_index.md` and `_index-archive.md`) —
same standing default every pass on this board has used; the
commit-convention question remains open, not re-decided here.
