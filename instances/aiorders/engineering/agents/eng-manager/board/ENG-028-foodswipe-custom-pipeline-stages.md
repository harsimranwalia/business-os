---
id: ENG-028
title: Foodswipe funnel — staff-configurable pipeline stage set
project: aiorders-admin-hub
type: feature
size: L
time_estimate: several days to a week+
time_spent:
time_remaining:
severity: P2
priority:
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-03
updated: 2026-09-03
branch:
depends_on: [ENG-013]
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-028-foodswipe-custom-pipeline-stages.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

Sales and onboarding staff can now move a Foodswipe listing between stages
(`ENG-013`), but the stages themselves are fixed in code — six names, bound
in four separate places across two repositories — so changing the pipeline
the team works, in any way at all, is an engineering ticket and two
deploys. The approver has said twice that this set is not the right one:
obliquely in `ENG-013`'s original request ("not able to update or have
proper peipleine stages") and explicitly in its merge-request reply
("custom pipeline stages for the whole foodswipe funnel").

## Outcome

Staff can define the Foodswipe funnel's stage set themselves — add a
stage, rename one, change their order, remove one — and the funnel page
reflects that set for every staff member, with no engineering change and
no deploy. The six stages that exist today survive intact: same names,
same order, same listings sitting in them, each still assigned
automatically by the same signal as before. A stage staff add beyond those
six is reachable by setting a listing's stage by hand, using the control
`ENG-013` already built. No listing is ever left referencing a stage that
is not on the board.

## Notes

**Filed off an approved decision, not a fresh request.** The approver's
reply to `ENG-013`'s merge request
(`inbox/_handled/2026-08-31-eng013-merge-request.md`, `decision: changed`,
2026-09-01T17:13:54), verbatim:

> "You added manual update of stage to the card what about the funnel
> stages itself on the page, if I want custom pipeline flow stages not
> just per card. This ticket was meant to allow custom pipeline stages for
> the whole foodswipe funnel, the stage updates per card can be manual or
> automatic."

That was genuinely ambiguous on *how* it should ship, so it was asked
rather than guessed:
`inbox/2026-09-02-eng013-stage-config-question.md`, answered **approved /
"Reading a approved"** (2026-09-03T15:23:36) — ship `ENG-013`'s two PRs
as-is and file stage-taxonomy configuration as a new, separate ticket
built on top. This is that ticket. The question's own closing note
explicitly deferred the design ("a new admin screen, ordering, whether
stages can be deleted once in use, etc.") to this ticket's own next design
round, so the PRD deliberately stops at capability and leaves all of that
to `designed`.

**No fresh request-readback run**, per this board's own precedent for
exactly this situation (`ENG-027`, filed off an approved decision rather
than raw ambiguous input): there is no new raw input to have two readers
disagree about. The approver's words above are the grounding, and the
scope was already narrowed to one named reading by an explicit question
the approver answered. The PRD carries a **readback-equivalent** section
citing those exact words and that resolution instead of a two-reading
comparison.

**Code grounding, verified against the live
`feat/ENG-013-foodswipe-funnel-stage-control` branches** (condensed; full
account in the PRD):
- `aiorders-api` / `admin-portal/handlers/foodswipe.ts` — a `Stage`
  TypeScript union and a `VALID_STAGES` array, both the same six literals;
  `classifyStage()` is a **fixed if/else chain over specific columns**
  (name+phone present, a `restaurants` row exists, menus present,
  `google_business_shared`, `website_interest`), not a table-driven
  engine. There is no generic "rule" concept anywhere.
- `supabase/migrations/20260829200000_add_foodswipe_stage_override.sql` —
  `profiles.foodswipe_stage_override text CHECK (... IN (the same six
  literals))`. Its own comment already names this ticket's central risk:
  *"If a future ticket changes that stage set, this constraint needs
  updating in the same change or an override could reference a stage that
  no longer classifies automatically."*
- `aiorders-admin-hub` / `src/pages/FoodswipeListings.tsx` — a `STAGES`
  array of six entries drives the kanban columns, each carrying `key`,
  `label`, `icon` and four separate colour/style fields. Display metadata
  is hand-authored per stage, not derived.

**The material open question, named not resolved:** a staff-*defined*
stage has no signal in `classifyStage()` — there is no mechanism by which
a made-up stage name could ever be assigned automatically. The approver's
"the stage updates per card can be manual or automatic" reads most
plausibly as: the original six keep their automatic classification,
anything staff add beyond those is manual-only. That is a proposed
default carried as `[proposed]` in the acceptance criteria, not a
confirmed requirement — put to the approver directly in the G1's own
Readback section as the one thing most worth correcting if wrong.

**Depends on `ENG-013`, which is not merged yet.** `ENG-013` is `state:
blocked` / `blocked_on: approver` with two open PRs (`aiorders-api#5`,
`aiorders-admin-hub#4`) that Reading A authorised merging. Whoever picks
this up at `building` must confirm those PRs actually landed on `main`
first — building this on top of an unmerged sibling branch is a known
review blind spot on this loop (merge detection diffs against `main`,
never against the sibling a ticket actually branched from).

**Sized `L`, not `M`.** New data model plus cross-project, two of the size
table's own `L` triggers, and a genuinely new admin surface where
`ENG-013` extended an existing screen. What would push it to `XL` (and
therefore back to the EM to split rather than build): making the
automatic classifier itself rule-configurable; requiring a data-migration
path for existing `foodswipe_stage_override` values on stage deletion; or
requiring the built-in six to be fully severable from their automatic
signals. Full reasoning in the PRD's Cost section.

**Full lane, checked against the exclusion list rather than assumed.**
`type: feature` at `L` fails the fast-lane size bar outright, and it
independently trips schema (a new stored taxonomy plus altering a live
CHECK constraint) and public contracts (new authenticated admin endpoints
plus a change to the shape the existing funnel read returns).

**Project field is a judgment call.** The work spans `aiorders-api`
(taxonomy storage, the constraint, the classifier's output type,
management endpoints) and `aiorders-admin-hub` (data-driven columns plus
the management screen). Recorded as `aiorders-admin-hub` following
`ENG-013`'s precedent for the same two-repo split and because the
user-facing surface is there; both repos named here so the architect
doesn't scope to one.

**Flagged for the EM's own sequencing judgement, not resolved here:**
`ENG-017` (presignup lead nurture autopilot, `designed`) nurtures leads
"to next stages automatically" — an editable taxonomy means a stage its
rules point at could be renamed or deleted out from under it. Whichever
of the two builds second inherits the coupling.

**Not the most urgent item on the board.** `ENG-022` (`type: security`,
`severity: P0`, cross-tenant PII/write exposure on five live handlers) is
already `designed`, owing only a G2, and outranks this if the approver's
attention is scarce — said in the G1 itself rather than left for them to
notice.

**No dissent section** — `agents/critic/agent.md` still doesn't exist at
department or instance level, confirmed fresh this pass. Same gap
`ENG-016`, `ENG-017` and `ENG-027`'s G1s already logged; not re-filed, the
open proposal (`proposals.md`, 2026-08-25) covers it.

## Log

Append-only. One line per state transition, newest last.

- `2026-09-03` `intake → shaped → awaiting-scope` (product-manager,
  `decision` event pass, context
  `inbox/2026-09-02-eng013-stage-config-question.md` — filed as a direct
  consequence of that decision, not a fresh board sweep). Mode check clean
  (business-os `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean (no `ENG-028` yet to scope to).

  Not agent-invented scope: the approved decision's own text directs
  "file stage-taxonomy configuration as ENG-0XX, a new ticket, built on
  top of this" — the same carve-out `eng_build_loop.md` step 3 already
  established for `ENG-027` (an approver-affirmed continuation is the
  approver's own request, already reviewed once, not the department
  inventing work about its own machinery).

  **Delegated PM judgment (filter, sizing, PRD/G1 drafting) to an `opus`
  subagent**, per `prd-writer/SKILL.md`'s own model designation, grounded
  in a fresh read of `knowledge/business-profile.md`, `ENG-013`'s own PRD
  and merge-request reply, `decision-journal.md`, `observations.md`
  (grepped for "foodswipe"/"stage" — no standing observation pre-flags
  this specific problem), and the live code on
  `origin/feat/ENG-013-foodswipe-funnel-stage-control` (`classifyStage()`,
  `VALID_STAGES`, the override column's `CHECK` constraint and its own
  prescient comment, the frontend `STAGES` display array) — read fresh by
  this pass before delegating, not asserted secondhand.

  **Filter check: build it.** Current, approver-evidenced problem (raised
  twice); real but bounded displacement (the one machine WIP slot, for
  longer than any ticket on this board has held it); the honest
  counter-pressure (nobody has named *which* stages are wrong, so a
  config screen may be a slow answer) carried into the PRD's Risks rather
  than argued away.

  **PRD written**:
  `agents/product-manager/specs/ENG-028-foodswipe-custom-pipeline-stages.md`
  — readback-equivalent (the approver's verbatim words plus the
  stage-config decision that resolved them, per the no-fresh-readback
  precedent below), acceptance criteria naming the manual-only assumption
  as the one thing most worth the approver correcting, non-goals
  explicitly excluding a configurable classifier, `ENG-017`'s pre-signup
  pipeline, and per-card stage setting (unchanged, `ENG-013`'s).

  **No fresh two-reader readback run** — per `ENG-027`'s own precedent for
  a ticket filed off an approved decision rather than raw ambiguous input:
  there is no new raw request for a blind architect reading to diverge
  against. The scope was already narrowed to one reading by the stage-
  config question the approver already answered.

  **G1 required** — full lane (`L`, new data model, cross-project; fails
  fast-lane's size and schema/public-contract exclusions independently).
  Wrote `inbox/2026-09-03-eng028-g1-scope.md` (`agent: product-manager`,
  `gate: scope`, `project: aiorders-admin-hub`, recommendation: build now,
  one ticket, expect a G2 on deletion semantics). Ran
  `departments/engineering/lib/eng-notify.sh raise`; see the item's own
  frontmatter for the result and `notified:` timestamp.

  **No dissent section** — `agents/critic/agent.md` confirmed absent
  again this pass (department and instance level); not refiled, the open
  proposal already covers it.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  `product-manager → approver`. **Consequence:** `machine_wip` unaffected
  (`awaiting-scope` sits outside the counted `ready`..`ready-to-ship`
  range — shaping is backlog grooming, not gated by the WIP-1 slot).
  Approver-facing WIP: joins the uncapped list (`wip.approver_limit:
  unlimited` since 2026-09-02) — visibility only, gates nothing.

  **Dead-end sweep:** out of scope for this `decision` event's own
  contract (act on the answered gate item; advance only the ticket it
  belongs to, `ENG-013`, plus this direct consequence of that decision).
  No other ticket touched.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-028`) and
  whole-board: see this pass's own entry on `ENG-013`'s board file and
  `_index.md`.
