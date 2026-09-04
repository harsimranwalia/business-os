---
id: ENG-032
title: Catering board — two new stages, itemized owner view, order-form enable switch
project: restaurant-portal
type: feature
size: M
time_estimate: ~1 day
time_spent: build (single session) + ~35m code review round 1 (fail — missing regression test) + fix (regression test, single session) + review round 2 + quality gate (combined hop, single session) + security gate (single session) + release-readiness (single session)
time_remaining: none — PR open, awaiting the approver's merge; two non-blocking review notes left unaddressed (optional, low-risk per review)
severity: P2
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-03
updated: 2026-09-03
branch: feat/ENG-032-catering-portal-stages-and-itemized-view (restaurant-portal@77631b0)
depends_on: [ENG-031]
blocks: [ENG-033]
parent: ENG-016
links:
  prd: agents/product-manager/specs/ENG-016-catering-quote-generator.md
  design: agents/architect/designs/ENG-016-catering-quote-generator.md
  adrs: [ADR-008, ADR-009]
  review: agents/principal-engineer/reviews/ENG-032.md
  test_plan: agents/qa/test-plans/ENG-032.md
  security_review: agents/security/reviews/ENG-032.md
  release: agents/devops/releases/2026-09-03-restaurant-portal-ENG-032.md
  pr: https://github.com/harsimranwalia/restaurant-portal/pull/2
---

## Problem

The catering board doesn't know about the two new outcomes Piece 1
introduces (`Quote Generated`, `Contact Requested`), and the owner's detail
modal has nowhere to show what a customer actually selected — today it's
five hardcoded stage strings duplicated across eight files, plus one
free-text `requirements` field. The owner also has no way to turn the new
order form on for their restaurant.

## Outcome

The two new stages are appended (immediately after `New Enquiry`) to every
hardcoded copy: `CateringKanban.tsx` (`columns` and `statusConfig`),
`CateringDetailModal.tsx` (`statusConfig` and `statusOptions`),
`StatusUpdateModal.tsx`, `ArchivedCateringModal.tsx`, `CateringForm.tsx`
(`statusOptions` only — its two `'New Enquiry'` literals are record defaults,
not a list, and stay untouched), `CateringCalendar.tsx`,
`CateringRequestCard.tsx`, `pages/catering/Index.tsx`, `index.css`. An
existing request in any of the five current stages is unaffected and stays
visible (AC-8).

`CateringDetailModal` gains a read-only itemized-selections block (AC-12) —
one line per selection (quantity, name, note), grouped by category, the raw
stored `name` rendered as-is and never re-resolved against the current menu.

The owner-side catering editor (`CateringPageForm.tsx`, `types/website.ts`)
gains the `orderFormEnabled` switch (default off, ADR-009) and a per-option
copy editor (`fulfillmentCopy`). `CateringPageForm`'s save path is fixed to
spread `...content` before its normalised fields, so keys outside its known
field list survive a save — without this fix the new switch would appear to
work once and then silently revert the next time the owner saves any other
catering-page edit.

## Notes

Design's `## Components` (the `restaurant-portal` rows) has the exact file
list; `## Risks` has the two correctness traps that matter most here: a
`columns` entry with no matching `statusConfig` entry throws on
`.borderColor` and takes the whole kanban down (both copies change in the
same commit, always), and the editor's current save path already silently
drops unknown keys (true today of the legacy `formFields` key) — this ticket
makes that newly consequential rather than newly created.

`depends_on: [ENG-031]` — the itemized block reads `action_type`/`selections`
via the existing `select('*')`, so the columns should exist first, and this
is also step 2 of the design's own Rollout order (must precede step 3 — see
Risks: a stage written before this ships is invisible on the board).
`ENG-033` depends on this ticket shipping. Full sequencing rationale:
`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`.

## Log

- `2026-09-03` `(created) → ready` (eng-manager, `work-breakdown`,
  `continue ENG-016` event pass) — sub-ticket of `ENG-016`, sequence 2 of 4.
  Held at `ready`: `depends_on: [ENG-031]` not yet `shipped`. `time_estimate`
  ~1 day. `chained: none` — waiting on a sibling's dependency, not agent-
  actionable yet; re-check is the scheduled sweep's or `ENG-031`'s own
  ship-triggered pass's job, not this one's to force.

- `2026-09-03` no state change (eng-manager, `scheduled` event pass —
  whole-board sweep, step 5 merge detection). This is exactly the re-check
  the entry above named as this pass's job. `ENG-031`'s `aiorders-api` PR
  #12 confirmed merged this same pass via local git ancestry (see `ENG-031`'s
  own board-file log) — `depends_on: [ENG-031]` is now satisfied.

  **Not transitioned to `building` in this pass.** Same precedent this
  board already set explicitly on `ENG-024` and `ENG-022` (a whole-board
  sweep does not perform new implementation work itself): the next hop is a
  real code edit against `restaurant-portal` (kanban columns/status config,
  the itemized-selections block, the owner-side switch) and belongs in its
  own dedicated session per `eng_build_loop.md`'s "each heavy step gets its
  own session with fresh context," not this sweep.

  Confirmed this is the correct next pick: `ENG-033` (`depends_on: [ENG-031,
  ENG-032]`) and `ENG-034` (`depends_on: [ENG-033]`) both remain blocked on
  this ticket specifically — no other member of the family is dispatchable
  yet, so there is no ordering choice to make. Machine WIP unaffected —
  this ticket was already inside the counted `ready..ready-to-ship` range as
  part of the `ENG-016` family's slot; moving it to `building` swaps which
  member is active, not how many.

  **0 transitions.** `chained: ENG-032` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-032` before this pass exits, so a dedicated session performs
  `ready → building` (transition and implementation together, the same
  shape every other building hop on this board has used).

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` `ready → building` (frontend, `continue` event pass, context
  `ENG-032` — this ticket's own turn, per the prior pass's own `chained:
  ENG-032`). Narrow scope per the event's own contract — this ticket only.
  Reading map for `continue`: steps 6 and 6b (design already complete, no
  mid-PRD checkpoint applies). Mode check clean (`MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-032`):
  exit 0, clean.

  **WIP re-checked fresh off every ticket's own frontmatter (all 33 board
  files), not trusted from the checkpoint.** Still 1/1, held by the
  `ENG-016` family (`ENG-016` building, `ENG-033`/`ENG-034` still `ready`);
  this transition swaps which family member is active, not the count.

  **Worktree branch fixed before use.**
  `~/Documents/projects/_eng/restaurant-portal` was on
  `feat/ENG-016-catering-quote-generator` (the parent ticket's slug, 0
  commits, clean tree) — the identical slip `ENG-031`'s own log and
  `observations.md` (2026-09-03) already caught once on `aiorders-api`.
  Renamed via `git branch -m` (lossless, nothing committed) to
  `feat/ENG-032-catering-portal-stages-and-itemized-view`. An unrelated
  pre-existing stash in the same worktree (stray debug line in
  `public/catering-form.js`, real ancestor commit, not blocking) left
  untouched.

  **Built all 11 `restaurant-portal` rows of the design's `## Components`
  table:** the two new stages (`Quote Generated`, `Contact Requested`)
  appended after `New Enquiry` in `CateringKanban.tsx` (`columns` +
  `statusConfig`, matched 7-for-7 against the design's named throw risk),
  `CateringDetailModal.tsx` (`statusConfig`, `statusOptions`, the
  itemized-selections block between Event Details and Requirements, a new
  `CateringSelection` type, two new `CateringRequest` fields),
  `StatusUpdateModal.tsx` (`statusOptions`), `ArchivedCateringModal.tsx`
  (`statusConfig`), `CateringForm.tsx` (`statusOptions` only, per design),
  `CateringCalendar.tsx` + `CateringRequestCard.tsx` +
  `pages/catering/Index.tsx` (two case arms each), `index.css` (two new
  `.status-*` classes). `CateringPageForm.tsx`: spread `...content` before
  the normalised fields (ADR-009's named fix), added the `orderFormEnabled`
  switch and a per-fulfillment-option `fulfillmentCopy` editor over the
  five known `delivery_method` values (ADR-008) — confirmed
  `pages/website/Index.tsx` passes the saved object through unnarrowed.
  `types/website.ts`: extended `CateringPageContent`. `Dashboard.tsx`
  confirmed untouched (design's explicit non-goal). Full reasoning, the
  Components-table/Data-section field-count discrepancy (table says three
  new interface fields, Data section names two columns — treated Data as
  authoritative, flagged rather than silently resolved), and the colour
  choices: first entry in
  `agents/frontend/notebook/2026-09-03-eng032-catering-stages-and-order-form-editor.md`.

  **Self-tested. No new automated test written — reason in the notebook**
  (design's own Risks section assigns `restaurant-portal` stage-change
  coverage to QA's plan; no per-component test convention exists yet in
  this repo to extend). `npm run lint`: 63 pre-existing problems, confirmed
  zero new via `git stash` diff against the pristine files. `npm run
  build`: clean. `npm run test`: 1/1 passed (`ENG-002`'s smoke test,
  unchanged).

  **Committed and pushed**, single repo: `restaurant-portal@ab3fa4e`
  (`feat/ENG-032-catering-portal-stages-and-itemized-view`, tracking
  `origin/feat/ENG-032-catering-portal-stages-and-itemized-view`); no PR
  opened yet — devops's own release-readiness hop, same precedent
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022`/`ENG-024` each set. PR body
  drafted here:

  *restaurant-portal* — title: `Catering board: two new stages, itemized
  owner view, order-form enable switch (ENG-032)`. Body: what's new (the
  two auto-set stages `Quote Generated`/`Contact Requested` from
  `ENG-033`'s upcoming server-side derivation, an existing request in any
  of the five current stages is unaffected — AC-8; the owner's detail modal
  now renders the itemized order snapshot when present — AC-12; a new
  Website → Catering switch turns the public order form on, off by default
  — ADR-009 — plus per-option copy); the fixed silent-revert bug in the
  catering editor's save path (ADR-009's Risks); self-test summary (lint
  zero-new, build clean, existing smoke suite green); out of scope (no
  price/pricing anywhere — Piece 2; no Edit Quote/resend — Piece 3; the
  twelve duplicated status literals and eight `CateringRequest`
  redeclarations stay duplicated — PRD's own non-goal, overlaps `ENG-013`).
  Depends on `ENG-031` (merged) landing before `ENG-033` starts writing the
  new statuses — sequencing note only, not a blocker for this PR merging on
  its own.

  **1 transition** (`ready → building`), under the cap of 4. Machine WIP
  unaffected — still 1/1, `ENG-016` family. Approver-facing WIP and
  approval cap unaffected — no gate touched this hop.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** every open inbox item's `notified:`/`nudged:` checked
  fresh against the 24h threshold (current time
  `2026-09-04T02:31:02Z`) — `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022` already
  used their one nudge each; `ENG-015`/`ENG-027`/`ENG-028` all under 24h;
  the three P0 incident notices (`ENG-029`/`ENG-030`/`ENG-035`) left as the
  prior pass left them. Nothing crossed, nothing raised this pass.
  **Observations filed** (`observations.md`): the parent-slug worktree-branch
  slip is now a confirmed second occurrence (`aiorders-api` then
  `restaurant-portal`), promoted from "watch for it" to "it happened
  again." **Step 6b: not run** — the new status strings and jsonb config
  keys are product data, not business-os process artifacts (same reasoning
  `ENG-024`'s `show_in_marketplace` hop already set). **Journal:** no
  G1/G2/G3 or merge request answered this pass — not applicable.

  `chained: ENG-032` — `building` is agent-owned (next hop `in-review`,
  owned by `principal-engineer` per `definition-of-done.md`'s state table);
  not the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-032` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-032`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` **code review round 1: FAIL — automatic-failure #3 (missing
  regression test on a real bug fix)** (principal-engineer, `continue` event
  pass, context `ENG-032` — this ticket's own turn, per the prior `continue
  ENG-032` (build) pass's own `chained: ENG-032`). Narrow scope per the
  event's own contract (resume this ticket only). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check clean
  (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

  **Combined review + quality hop, per `eng_build_loop.md` step 6** — QA not
  actually run this round (see Verdict below). Worktree
  (`~/Documents/projects/_eng/restaurant-portal`) confirmed on
  `feat/ENG-032-catering-portal-stages-and-itemized-view@ab3fa4e`, matching
  this ticket's own frontmatter, clean tree, tracking
  `origin/feat/ENG-032-...`, no drift after `git fetch origin main`. Diff
  reviewed: `git diff origin/main...HEAD`, 11 files, 207 insertions / 6
  deletions.

  **Automatic-failure scan (`engineering-standards.md`):**

  | # | Check | Result |
  |---|---|---|
  | 1 | Secret/credential/token/key committed | Clean |
  | 2 | Silent exception swallow | Clean — no new `try`/`catch` anywhere in this diff |
  | 3 | Missing test on a bug fix | **Hit** — see below |
  | 4 | Untyped public interface, undocumented | Clean — `CateringSelection`, `CateringFulfillmentCopy`, `FULFILLMENT_OPTIONS` all typed; no new `any` |
  | 5 | Unbounded query / missing pagination | Clean — no query in this diff (pure rendering/form state) |
  | 6 | New dependency, no justification | Clean — `Switch` from `@/components/ui/switch` is a pre-existing shadcn primitive, not touched/added by this diff |
  | 7 | Unrelated refactor bundled in | Clean — see non-blocking note below on trailing whitespace, not treated as a refactor |
  | 8 | Commented-out code / unowned `TODO` | Clean |
  | 9 | Datastore write bypassing the data layer | Clean — no new write path; `CateringPageForm`'s save still goes through the existing `saveMutation` unchanged |
  | 10 | Auth/payment/deletion path changed, no failure-case test | Clean — none touched |

  **#3 — the `...content`-spread-before-normalised-fields fix
  (`CateringPageForm.tsx:53-66`) ships with zero test coverage.** The
  ticket's own Outcome section, the design's own Risks section, and this
  commit's own message all describe this as fixing a real, live bug — an
  owner editing their catering copy silently wipes `orderFormEnabled`/
  `fulfillmentCopy` on save. Zero test files exist anywhere in this 11-file
  diff. `@testing-library/react`, `jsdom`, and `vitest` are already
  installed (`package.json`, `ENG-002`'s harness) — this isn't blocked by
  missing infrastructure, nobody has written the first component test yet.
  `engineering-standards.md`'s Tests section calls the regression-test rule
  "the single highest-leverage rule in this document. No exceptions."
  Verified the fix is otherwise correct before flagging only the missing
  test, not the fix itself: traced `useEffect` (line 55's `...content`
  spread is never re-overwritten by the explicit field list that follows —
  `orderFormEnabled`/`fulfillmentCopy` aren't in it), `handleSubmit`
  (`onSave({...form, ...})`, line 87-92, doesn't re-narrow either), and the
  call site (`pages/website/Index.tsx:125`, passes the typed object straight
  through unnarrowed). Fix shape for the next build hop:
  `CateringPageForm.test.tsx`, render with a `content` prop carrying
  `orderFormEnabled: true` and a populated `fulfillmentCopy` entry, submit
  without touching either, assert `onSave` receives both intact; confirm red
  against the pre-fix field ordering before calling it done (the mutation-check
  bar `ENG-022`/`ENG-024`/`ENG-015` already set on this board).

  **Two non-blocking notes, not the reason this round fails:**
  `CateringKanban.tsx` carries a few trailing-whitespace-only edits on
  pre-existing lines directly beside the new entries (e.g. `'New Enquiry': {
  ` → `{`) — not treated as automatic-failure #7: the file still carries the
  same trailing whitespace untouched elsewhere (lines 53/56/57/60/61/64/65),
  so this reads as incidental re-typing, not a cleanup pass. And
  `CateringDetailModal.tsx:337` keys the rendered selection list on array
  `index` — normally worth a note, low actual risk here since the list is a
  static, read-only, submission-time snapshot never reordered after render.

  **Good work, briefly:** the 8-file/12-literal status-list addition is
  clean and complete — `CateringKanban`'s 7 `columns` entries and 7
  `statusConfig` keys matched one-for-one (the design's own named throw
  risk), colors applied consistently and matching each file's own existing
  per-file shape rather than one copy-pasted pattern.

  **Verdict: FAIL, round 1.** No receipt written
  (`agents/principal-engineer/reviews/ENG-032.md` stays absent — a receipt
  is written on `pass` only). QA's hop not run this round — discarded per
  the combined-hop design, the code is about to change; no
  `agents/qa/test-plans/ENG-032.md` written. Full findings:
  `agents/principal-engineer/notebook/2026-09-03-review-log.md`.

  **0 net transitions** — `state`/`owner` unchanged (`building`/`frontend`),
  same precedent `ENG-008`/`ENG-013`/`ENG-015`'s own round-1 entries set.
  `machine_wip` unaffected, still 1/1 (`ENG-016` family). Approver-facing WIP
  and approval cap both unaffected — a review failure is not an
  approver-facing gate. `time_spent`/`time_remaining` updated in
  frontmatter.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** every open inbox item's `notified:`/`nudged:` checked
  fresh against the 24h threshold (current `2026-09-04T03:09:49Z`) —
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022` already used their one nudge each;
  `ENG-015`/`ENG-027`/`ENG-028` all under 24h; the four P0 incident notices
  (`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`) left as-is, same standing
  treatment this board has given them all day. Nothing crossed, nothing
  raised — and a review failure routes back to `building`, not to the
  approver, so this hop itself raised nothing new either.

  **Observations filed** (`observations.md`): `restaurant-portal` has
  `@testing-library/react`/`jsdom`/`vitest` installed (`ENG-002`) but zero
  per-component test files exist yet — today's missing test is the first
  time that gap has actually blocked a round, worth watching for a repeat.

  **Step 6b: not run** — this is a review hop, not a build hop; nothing this
  pass writes establishes a new rule about an artifact path, state name, or
  config key. **Journal:** not applicable — no G1/G2/G3 or merge request
  answered this pass.

  `chained: ENG-032` — `building` is agent-owned (round 1's one finding is
  the next hop's own work: add the missing regression test, optionally
  address the two non-blocking notes), not the approver, not blocked, not
  terminal, not held by a cap. Firing `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-032` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-032`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` no transition (`building`/`frontend` unchanged) (frontend,
  `continue ENG-032` event pass, per round 1's `chained: ENG-032`).
  Reading map: steps 6/6b + not-negotiable set. Mode clean, pre-pass
  gate-check exit 0.

  Built round 1's fix shape: added
  `restaurant-portal/src/components/website/CateringPageForm.test.tsx`,
  confirmed red against the pre-fix field ordering then green restored.
  Lint 96/0-new (round 1's logged "63" was stale, not a regression),
  build clean, test 2/2 — full detail in notebook. Two non-blocking notes
  left unaddressed, deliberately. Committed + pushed:
  `restaurant-portal@7950a93`. No gate run this hop; WIP/approval caps
  unaffected. Dead-end sweep: none. Notify sweep: nothing crossed 24h.
  Step 6b: not run — test file is product code, not a business-os
  artifact. Journal: n/a.

  Reasoning:
  `agents/frontend/notebook/2026-09-03-eng032-catering-stages-and-order-form-editor.md`.
  2 observations filed (`observations.md`).

  `chained: ENG-032` — `building` still agent-owned (review round 2 next,
  principal-engineer); not approver, not blocked, not terminal, not
  capped. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-032` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-032`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` `building → in-review → in-qa` (principal-engineer + qa,
  combined review+quality hop, `continue ENG-032` event pass, per prior
  pass's own `chained: ENG-032`). **Review: PASS, round 2** (round 1's only
  finding — missing regression test — closed; 0/10 automatic failures).
  **QA: PASS** (AC-8 UI slice + AC-12, narrowed per design — both covered
  by 2 new mutation-verified tests this pass wrote and committed; no open
  P0/P1). Receipts: `agents/principal-engineer/reviews/ENG-032.md`,
  `agents/qa/test-plans/ENG-032.md`; `links.review`/`links.test_plan` set.
  New tests committed+pushed: `restaurant-portal@77631b0`.
  2 transitions, under cap. No WIP/cap change — still inside the counted
  `ready..ready-to-ship` range.
  Reasoning: `agents/principal-engineer/notebook/2026-09-03-review-log.md`,
  `agents/qa/notebook/2026-09-03-coverage-gaps.md`. 3 observations filed
  (`observations.md`).
  `chained: ENG-032` — `in-qa` is agent-owned (security next), not the
  approver, not blocked, not terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-032` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-032`) and
  whole-board: see board index for result.

- `2026-09-03` `in-qa → in-security` (security, `continue ENG-032` event
  pass, per prior pass's own `chained: ENG-032`). Reading map: steps 6/6b +
  not-negotiable set. Mode clean (`MODE=active`), pre-pass gate-check exit 0.

  **Security: PASS.** Threat-modeled the diff (4 questions), walked OWASP
  A01–A10 (all n/a-with-reason except A01/A03, both checked substantively —
  see receipt), LLM checklist n/a (no model/agent/tool touched), secret scan
  clean over the diff and full 3-commit branch history, no new/bumped
  dependency, config untouched. Independently re-verified rather than taken
  on the design's account: `grep`-confirmed zero `supabase.from(` calls
  anywhere in this diff (the itemized block renders an already-fetched prop,
  adds no new query); read `aiorders-api`'s `brand-portal/catering.ts` on
  `origin/main` directly and confirmed `get_catering_requests` calls
  `verifyRestaurantAccess` before its `select('*')`, in the correct order.
  Checked the new `(acc[selection.category] ||= []).push(...)` grouping
  pattern for prototype pollution — not exploitable, `||=`'s short-circuit
  on any plain object's always-truthy inherited `__proto__`/`constructor`
  means the assignment branch never fires for those keys. No blocking
  findings. Receipt: `agents/security/reviews/ENG-032.md`;
  `links.security_review` set. 2 transitions (`in-qa → in-security →
  ready-to-ship`), under cap. No WIP/approval-cap
  change — still inside the counted `ready..ready-to-ship` range.

  **One non-blocking finding, routed out rather than held against this
  ticket:** verifying QA's test-plan claim that "`ENG-022`'s own suite
  already covers `brand-portal`'s access-check call sites generally" found
  the claim overstated — `ENG-022`'s 19 negative tests cover 5 of
  `brand-portal`'s 10 handler files (confirmed against `origin/main`'s
  tree), and `catering.ts` (the file this ticket's rendered data flows
  through) isn't one of them, though its own `verifyRestaurantAccess` calls
  are correctly written. Doesn't change ENG-032's own verdict — this diff
  adds no code to `aiorders-api` and no authz-relevant code to test either
  way — but the gap is real and now matters more than it did before this
  ticket (the data it guards is rendered to the owner for the first time).
  Filed as a proposal (`agents/eng-manager/proposals.md`, 2026-09-03,
  security, `aiorders-api`) per `eng_build_loop.md` step 3 — the department
  doesn't turn its own findings straight into tickets. Also logged in
  `agents/security/notebook/2026-09-03-findings.md`.

  Step 6b: not run — this hop writes no new rule about an artifact path,
  state name, or config key; it only reads existing code and writes a
  receipt. Dead-end sweep: none. Notify sweep: nothing crossed 24h.
  Journal: n/a — no G1/G2/G3 or merge request answered this pass, and this
  gate is machine-owned, not an approver decision.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

  `chained: ENG-032` — `ready-to-ship` is agent-owned (devops next,
  release-readiness), not the approver, not blocked, not terminal, not held
  by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-032` before this pass exits. Not combined with this hop
  (unlike review+quality, security and release-readiness aren't named as a
  combinable pair anywhere in `eng_build_loop.md`, and each heavy gate gets
  its own fresh-context session by design — "The chain" section). Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-032`) and
  whole-board: see board index for result.

- `2026-09-03` `ready-to-ship → blocked` (devops, `continue ENG-032` event
  pass, per prior pass's own `chained: ENG-032`). Reading map: steps 6/6b +
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
  lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-032`) and
  whole-board: both exit 0, clean.

  Ran `skills/release-runner/SKILL.md`. `restaurant-portal` registered
  **L1** (`config/projects.md`) — step 1's window check skipped entirely per
  the skill's own instruction (opening a PR is not a release).

  **Step 2 — verified every upstream gate passed, read directly rather than
  trusted from the ticket's own state:** `agents/principal-engineer/reviews/ENG-032.md`
  (`verdict: pass`, round 2), `agents/qa/test-plans/ENG-032.md`
  (`last_result: pass`), `agents/security/reviews/ENG-032.md`
  (`verdict: pass`) all read in full. No `agents/database/migrations/ENG-032-*.md`
  — correct, this ticket touches no schema.

  **Step 3 — held the readiness gate. PASS on all three:**
  - **Rollback:** no migration, so a revert is complete on its own — three
    commits (`ab3fa4e`/`7950a93`/`77631b0`), pure UI plus an
    existing-jsonb-column save-path fix, additive only. Newly verified this
    hop: `.github/workflows/deploy-cf.yml` now exists on `main`
    (push-triggered, `npm run deploy-cf`) — this repo had none of that as of
    `ENG-002`'s own release record (2026-08-26). A revert on `main`
    re-triggers that same workflow and redeploys the prior build
    automatically; not live-drilled (no merge has happened yet to drill
    against), reasoned from reading the workflow file directly rather than
    assumed. Observation filed (`observations.md`) — this is new since
    `ENG-002` and changes what a future release-readiness hop on this repo
    should check.
  - **Observability:** the one named throw risk (a `columns` entry with no
    matching `statusConfig` entry) is mutation-tested pre-merge (QA's AC-8
    test, confirmed by reading `agents/qa/test-plans/ENG-032.md` directly,
    not assumed from its verdict alone). No client-side runtime error
    tracking exists anywhere in this repo
    (`grep -rniE "sentry|errorboundary|componentDidCatch|bugsnag|rollbar" src/`
    — zero hits) — a pre-existing gap across this whole instance, not
    introduced or worsened by this ticket, same posture that already passed
    this identical gate on `ENG-002`. The new CI workflow's own run status is
    a real, checkable signal once a merge happens, same mechanism `ENG-011`
    used on `aiorders-admin-hub`.
  - **Cost:** $0/month — independently confirmed, not just taken on
    security's A06 finding: `git diff origin/main...HEAD --stat` in the
    worktree carries no `package.json`/lockfile; no new external service;
    reuses existing Cloudflare Pages capacity and `ENG-031`'s existing DB
    columns. No cost notice owed.
  - Window-closed criterion: n/a, L1.

  **Step 4 — routed by autonomy.** L1: opened the PR and wrote the merge
  request in the same step. PR:
  `https://github.com/harsimranwalia/restaurant-portal/pull/2` (base
  `main`, head `feat/ENG-032-catering-portal-stages-and-itemized-view`,
  opened from the department's own worktree,
  `~/Documents/projects/_eng/restaurant-portal`, confirmed clean and on the
  right branch/commit before opening, no drift after `git fetch origin`).
  Merge request written: `inbox/2026-09-03-eng032-merge-request.md`,
  `pr_url` set, `time_estimate` mirrored from the ticket's own frontmatter.
  Notified immediately: `lib/eng-notify.sh raise` — confirmed sent
  (`traces/eng-notify-2026-09-03.log`: `sent: active
  2026-09-03-eng032-merge-request.md`), `notified:` stamped in the item's
  own frontmatter.

  Ticket set `ready-to-ship → blocked`, `owner: devops → approver`,
  `blocked_on: approver`, `blocked_from: ready-to-ship` (the field's
  presence is enforced; `lib/eng-gate-check.sh` confirmed clean post-edit).
  `links.pr` set on the ticket in the same edit. `time_spent`/`time_remaining`
  updated in frontmatter.

  **1 transition** (`ready-to-ship → blocked`), under the cap of 4. Machine
  WIP unaffected — still 1/1, held by the `ENG-016` family via `ENG-016`
  itself (still `building`), not by this ticket's own row.
  **Approver-facing WIP: `wip.approver_limit: unlimited`** — verified
  directly against `config/config.yaml` this hop (line 36: "Raised to no-cap
  2026-09-02 by the approver"), not taken from the board index's own
  narrative of it. This gate item is added to the count for visibility
  only; nothing here gates a new start either way.

  **Dead-end sweep (scoped to this event):** no other ticket touched. While
  confirming the approver-WIP framing above, spot-checked every ticket
  currently `blocked`/`blocked_on: approver` (`ENG-008`/`009`/`010`/`013`/
  `015`/`022`, six) or `awaiting-scope` (`ENG-027`/`028`, two) against their
  own frontmatter fresh — all eight already correctly reflect the
  `unlimited` reading; nothing to correct. **Notify sweep:** every open
  `inbox/` item's `notified:`/`nudged:` checked fresh against the 24h
  threshold (current `2026-09-04T04:27:45Z`) — `ENG-008`/`ENG-009`/
  `ENG-010`/`ENG-022` already carry their one-time `nudged:`; `ENG-015`/
  `ENG-027`/`ENG-028` and the four P0 incident notices all still under 24h;
  this pass's own new item notified immediately, not yet due for anything
  further. **Observation filed** (`observations.md`): the newly-discovered
  `deploy-cf.yml` workflow, above. **Step 6b:** not run — this hop follows
  the already-established `blocked`/`blocked_on: approver`/`pr_url` pattern
  exactly as `ENG-008`/`ENG-009`/`ENG-010`/`ENG-013`/`ENG-015`/`ENG-022`
  already used it; nothing here writes a new rule about an artifact path,
  state name, or config key. **Journal:** n/a — this gate was raised, not
  answered, this pass.

  **Board update:** this entry appended to this ticket's own log; the
  oldest of the four now-live dated entries on the board index
  (`continue ENG-032: round-1 fix...`) rolled to `_index-archive.md` per
  the keep-three rule, and a fresh dated entry for this hop appended there
  too. In-flight table row for `ENG-032` updated (`ready-to-ship`/`devops`
  → `blocked`/`approver`). Approver-facing-WIP list and count updated
  (seven → eight items), `ENG-032`'s own paragraph added to "Waiting on the
  approver."

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-032`) and whole-board: both exit 0, clean.

  `chained: none` — **waiting on the approver** (`blocked`,
  `blocked_on: approver`; L1 merge request raised, PR #2 open). Per
  `eng_build_loop.md` step 9 / "The chain," a ticket waiting on the approver
  is never chained — the next build-loop pass to touch this ticket is
  whichever one processes the merge (a `decision` event on the
  merge-request item, or a future `scheduled` sweep's own step-5 merge
  detection finding the PR merged directly on GitHub).

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` no state change (eng-manager, `watch` event pass, context
  `launchd`). The file-watcher fired on this ticket's own merge-request file
  (`inbox/2026-09-03-eng032-merge-request.md`) appearing in `inbox/` —
  written directly by the prior `continue ENG-032` pass's release-runner
  hop, not through the notify/decision-poll channel, which is exactly the
  "gate item... not through the control center" shape `eng_build_loop.md`
  defines this event for. Reading map for `watch`: steps 2, 3, 4 (sweeps all
  three inboxes) and step 5, since the changed file is a merge-request item,
  plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*,
  *The four lanes*, *Guards*) — read in full (whole document). Mode check
  clean (`MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-032`) and
  whole-board: both exit 0, clean.

  **Steps 2–4:** swept all three watched inboxes.
  `agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold
  nothing but their own `_handled`/`_processed` folders, both untouched
  since 2026-09-01; `inbox/requests/` is empty. `inbox/` itself holds twelve
  open items — checked every one's frontmatter `decision:` field and its
  `## Decision` section body directly rather than trusting the field alone
  (the hand-edit case this event exists to catch): every `decision:` is
  blank and every `## Decision` section still reads its own unfilled
  boilerplate ("Filled in by the approver" / "Nothing to decide —
  informational"). Nothing answered, nothing new to act on under steps 2–4.

  **Step 5 — merge detection**, since this ticket's own merge request is
  the item that fired this event: `git fetch origin` in
  `~/Documents/projects/_eng/restaurant-portal` (clean, no drift), then
  `git merge-base --is-ancestor origin/feat/ENG-032-catering-portal-stages-and-itemized-view
  origin/main` — **not an ancestor**. PR #2 still open, not merged. No
  transition.

  **0 transitions.** `state`/`owner` unchanged (`blocked`/`approver`).
  Machine WIP unaffected — still 1/1 (`ENG-016` family). Approver-facing WIP
  unaffected — this item stays counted, same as before this pass.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** every open `inbox/` item's `notified:`/`nudged:`
  rechecked fresh against the 24h threshold (current
  `2026-09-03T21:37:47-07:00` / `2026-09-04T04:37:47Z`) —
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022` already carry their one-time
  `nudged:`; `ENG-015`/`ENG-027`/`ENG-028` all still under 24h (reading
  their own local-time-mislabeled timestamps at face value against local
  now, same standing convention prior passes on this board have used); the
  four P0 incident notices (`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`) left
  as-is, same standing treatment; this ticket's own item was notified at
  raise time (~14 minutes before this pass), nowhere near due. Nothing
  crossed, nothing raised this pass. **No observations filed** — this pass
  confirmed steady state, found nothing novel. **Step 6b:** not run — no
  artifact rule written or relied on this hop. **Journal:** n/a — no
  G1/G2/G3 or merge request answered this pass.

  **Board update:** this entry appended; board index's own dated-entry log
  updated to match (see board index).

  `chained: none` — **waiting on the approver**, unchanged (`blocked`,
  `blocked_on: approver`; PR #2 still open, no answer). Per
  `eng_build_loop.md` step 9, a ticket waiting on the approver is never
  chained.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` `blocked → shipped → verified` (eng-manager, `scheduled`
  event pass — whole-board sweep, step 5 merge detection). `git fetch
  origin` in `~/Documents/projects/_eng/restaurant-portal` (clean, no
  drift), then `git merge-base --is-ancestor
  origin/feat/ENG-032-catering-portal-stages-and-itemized-view origin/main`:
  **YES** — PR #2 merged. Cross-checked beyond the local-git-only floor with
  `gh pr view 2 --repo harsimranwalia/restaurant-portal`: `state: MERGED`,
  `mergedAt: 2026-09-04T04:56:20Z`, merge commit `5276a53` — exactly
  `origin/main`'s current tip. The branch's own tip (`77631b0`) is itself
  the merge-base of the branch and `main` — the whole branch is cleanly
  contained, no drift between what passed every gate and what merged.
  `decision:` on `inbox/2026-09-03-eng032-merge-request.md` stayed blank —
  merged directly on GitHub, same shape `ENG-007`/`ENG-011`/`ENG-022`/
  `ENG-024`/`ENG-031` already established for this approver.

  **Not advanced past a state that owes gates** (step 5's own "a merge is
  not a gate" clause): re-read all three receipts directly before writing
  `shipped` — `agents/principal-engineer/reviews/ENG-032.md` (`verdict:
  pass`, round 2), `agents/qa/test-plans/ENG-032.md` (`last_result: pass`),
  `agents/security/reviews/ENG-032.md` (`verdict: pass`); no migration
  applies (no `agents/database/migrations/ENG-032-*.md` exists, correctly —
  confirmed no `*.sql` in the diff). Independently re-verified the fix on
  the merged tree itself rather than trusting the receipts' word alone:
  `git show origin/main:src/components/catering/CateringKanban.tsx` and
  `.../CateringDetailModal.tsx` confirm the two new stages and the
  itemized-selections block are present; `git show
  origin/main:src/components/website/CateringPageForm.tsx` confirms the
  `...content` spread precedes the normalised fields and `orderFormEnabled`
  is wired through. Both acceptance criteria (AC-8, AC-12 narrowed)
  re-confirmed against `origin/main`. Release record written:
  `agents/devops/releases/2026-09-03-restaurant-portal-ENG-032.md`,
  `links.release` set in the same edit. `state: blocked → verified`,
  `owner: approver → eng-manager`, `blocked_on`/`blocked_from` cleared.

  Merge-request item moved to `inbox/_handled/`. Journal entry added
  (`decision-journal.md`) — silent GitHub merge, no written reply, same
  shape as `ENG-007`/`ENG-011`/`ENG-022`/`ENG-024`/`ENG-031`'s own rows.

  **This ticket's own shipping satisfies `ENG-033`'s last unmet dependency**
  (`depends_on: [ENG-031, ENG-032]` — `ENG-031` already `verified`). Same
  precedent this ticket's own `2026-09-03` "no state change... step 5 merge
  detection" entry above set when `ENG-031` shipped for it: not built inline
  by this sweep (new implementation work stays out of a `scheduled` pass),
  but dispatched via `continue` so a dedicated session performs
  `ENG-033`'s own `ready → building` — see `ENG-033`'s own board-file log
  and this pass's own board-index entry for the dispatch reasoning. `ENG-034`
  (`depends_on: [ENG-033]`) remains blocked on that ticket specifically.

  **2 transitions** (`blocked → shipped`, `shipped → verified`), well under
  the cap of 4 — pure receipt-confirmation and bookkeeping, no new
  implementation work, same precedent `ENG-022`'s and `ENG-024`'s identical
  scheduled-sweep discoveries already set. **Consequence:** ticket leaves
  the board's in-flight table entirely (terminal); does not affect machine
  WIP (already outside the counted `ready..ready-to-ship` range since its
  own `ready-to-ship → blocked` hop; the `ENG-016` family still holds the
  slot via `ENG-033`/`ENG-034`); drops off the approver-facing "Waiting on
  the approver" count (no open inbox item remains for it).

  `chained: none` on this ticket's own row — `verified` is terminal, the
  chaining guard never fires on a terminal ticket. (`continue ENG-033` is
  fired by this same pass, recorded on `ENG-033`'s own log and this pass's
  board-index entry, not here — chaining is recorded against the ticket it
  advances.)

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.
