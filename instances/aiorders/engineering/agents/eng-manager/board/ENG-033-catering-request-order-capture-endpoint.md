---
id: ENG-033
title: catering-request — accept, validate and derive status for order-capture fields
project: aiorders-api
type: feature
size: M
time_estimate: ~half a day
time_spent: build (single session) + review round 1 + fix round 1 finding + review round 2 + fix round 2 finding + review round 3 (pass) + quality gate round 1 (fail) + quality-gate finding fixed (extract + test status-derivation logic) + review round 4 (pass) + quality gate round 2 (pass) + security gate (pass) + release-readiness (PR opened, merge request raised)
time_remaining: 0 machine time — shipped.
severity: P2
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-03
updated: 2026-09-04
branch: feat/ENG-033-catering-request-order-capture-endpoint (aiorders-api@697df79)
depends_on: [ENG-031, ENG-032]
blocks: [ENG-034]
parent: ENG-016
links:
  prd: agents/product-manager/specs/ENG-016-catering-quote-generator.md
  design: agents/architect/designs/ENG-016-catering-quote-generator.md
  adrs: [ADR-008, ADR-009]
  review: agents/principal-engineer/reviews/ENG-033.md
  test_plan: agents/qa/test-plans/ENG-033.md
  security_review: agents/security/reviews/ENG-033.md
  release: agents/devops/releases/2026-09-04-aiorders-api-ENG-033.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/13
---

## Problem

`catering-request`'s handler has no way to accept or validate a customer's
dish selections, no way to record how they reached the request, and nothing
derives the two new board stages server-side — that has to happen before
`config-site-builder` has anything to POST to.

## Outcome

`catering-request/index.ts` destructures two new optional body fields,
validates them at the boundary, and derives `status` server-side (never from
the request body — this endpoint is unauthenticated, and a client-supplied
status would let anyone drop a request straight into a late-pipeline stage):

| Input | Behaviour |
|---|---|
| `action_type` absent | Store `null`, omit `status` from the INSERT — today's default (`'New Enquiry'`) applies, unchanged |
| `action_type` present but not one of the two literals | Same as absent |
| `action_type = MANUAL_CONTACT_REQUESTED` | Store it, store `selections` as `null` regardless of what was sent, `status = 'Contact Requested'` |
| `action_type = QUOTE_SUBMITTED`, `selections` valid | Store both, `status = 'Quote Generated'` |
| `selections` not an array, > 200 elements, or any element with non-positive/non-integer `quantity`, missing/non-string `name`, or `note` over 500 chars | 400 `{ error: "Invalid selections" }` with `...corsHeaders` |

Every existing caller (GoHighLevel's `customData` branch, `restaurant-
marketplace`'s own direct insert) is unaffected by construction — the
function already ignores any field it doesn't destructure (AC-10).

`brand-portal/website.ts`'s `CateringPageContent` interface gains the two new
keys (`orderFormEnabled`, `fulfillmentCopy`) — type documentation only;
`updateWebsiteContent` already writes `content[page]` opaquely, so this is a
no-behaviour-change edit.

## Notes

Design's `## Interfaces` → "`catering-request` — additive request fields"
has this validation table verbatim plus the two load-bearing rules (status
never read from the body; the existing `source == "form"` required-field
branch stays untouched) — build against it directly. ADR-008 is why no
fulfillment-value remap happens anywhere in this diff.

`depends_on: [ENG-031, ENG-032]` — per the design's Rollout order and its own
stated Risk, this must not deploy before the columns exist and
restaurant-portal can render the new stages, or new leads become invisible
on the owner's board the moment this ships. `ENG-034` depends on this
ticket shipping. Full sequencing rationale:
`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`.

## Log

- `2026-09-03` `(created) → ready` (eng-manager, `work-breakdown`,
  `continue ENG-016` event pass) — sub-ticket of `ENG-016`, sequence 3 of 4.
  Held at `ready`: `depends_on: [ENG-031, ENG-032]`, neither yet `shipped`.
  `time_estimate` ~half a day. `chained: none` — waiting on two siblings,
  not agent-actionable yet.

- `2026-09-03` no state change (eng-manager, `scheduled` event pass —
  whole-board sweep, step 5 merge detection). This same pass's own step 5
  found `restaurant-portal` PR #2 (`ENG-032`) merged directly on GitHub —
  see `ENG-032`'s own board-file log — and carried it `blocked → shipped →
  verified`. `ENG-031` was already `verified` (an earlier pass tonight).
  Both entries in `depends_on: [ENG-031, ENG-032]` are now satisfied.

  **Not transitioned to `building` in this pass.** Same precedent this
  board already set explicitly on `ENG-032` itself when `ENG-031` shipped
  for it (and on `ENG-024`/`ENG-022` before that): a whole-board sweep does
  not perform new implementation work itself. The next hop is a real code
  edit against `aiorders-api` (`catering-request/index.ts`'s new
  destructure/validate/derive-status logic, `brand-portal/website.ts`'s
  interface addition) and belongs in its own dedicated session per
  `eng_build_loop.md`'s "each heavy step gets its own session with fresh
  context," not this sweep.

  Confirmed this is the correct next pick: `ENG-034` (`depends_on:
  [ENG-033]`) remains blocked on this ticket specifically — no other member
  of the `ENG-016` family is dispatchable yet, so there is no ordering
  choice to make. Machine WIP unaffected — this ticket was already inside
  the counted `ready..ready-to-ship` range as part of the `ENG-016` family's
  slot; moving it to `building` swaps which member is active, not how many.

  **0 transitions.** `chained: ENG-033` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits, so a dedicated session performs
  `ready → building` (transition and implementation together, the same
  shape every other building hop on this board has used).

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` `ready → building` (backend, `continue` event pass, context
  `ENG-033` — this ticket's own turn, per the prior `scheduled` sweep's own
  `chained: ENG-033`). Narrow scope per the event's own contract — this
  ticket only. Reading map for `continue`: steps 6 and 6b (design already
  complete, no mid-PRD checkpoint applies), plus the not-negotiable set (1,
  7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode
  check clean (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: both exit 0, clean.

  **WIP re-checked fresh off every ticket's own frontmatter** (`ENG-016`
  `building`; `ENG-031`/`ENG-032` `verified`; `ENG-034` still `ready`), not
  trusted from the checkpoint: still 1/1, held by the `ENG-016` family. This
  transition swaps which family member is active, not the count — same
  precedent `ENG-031`'s and `ENG-032`'s own building hops already set.

  **Worktree branch fixed before use.**
  `~/Documents/projects/_eng/aiorders-api` was still on
  `feat/ENG-031-catering-order-capture-migration` (that ticket's own
  now-merged branch) — the identical slip `ENG-031`'s and `ENG-032`'s own
  logs and `observations.md` already caught twice. `git fetch origin`
  confirmed the branch's tip (`06e8e84`) was already an ancestor of
  `origin/main`, but `origin/main` had moved further ahead (`ENG-022`'s
  merge and others) — a `git branch -m` rename in place would have
  understated the real diff against current main, so branched fresh
  instead: `git checkout -B
  feat/ENG-033-catering-request-order-capture-endpoint origin/main`. The
  pre-existing untracked `supabase/functions/brand-portal/deno.lock`
  survived the switch, confirmed unrelated to this ticket's own diff —
  fourth independent pass to notice it still sitting there
  (`ENG-029`/`ENG-031`'s design and building passes, `ENG-031`'s
  release-readiness hop, now this one); left alone again, no new
  observation filed for it — the standing notice already asked for someone
  to pick it up rather than have it re-derived again.

  **Built both `aiorders-api` rows of the design's `## Components` table.**
  `catering-request/index.ts`: destructured `action_type`/`selections`
  alongside the existing fields (`status` deliberately not destructured,
  preserving the existing property exactly as the design's load-bearing
  rule requires); added `isValidSelections` (array, ≤200 elements, each
  element a positive integer `quantity`, a string `name`, and — when
  present — a `note` ≤500 chars); derived `status` server-side from
  `action_type` (`MANUAL_CONTACT_REQUESTED` → `'Contact Requested'`,
  `selections` forced `null`; `QUOTE_SUBMITTED` with valid `selections` →
  `'Quote Generated'`, both stored; absent or unrecognised `action_type` →
  both `null`, `status` omitted from the INSERT via a conditional spread so
  the column default applies unchanged). The `if (source == "form" && ...)`
  required-field branch, and the fact that `status` is not destructured
  from the body at all, both left untouched exactly as the design names.
  `brand-portal/website.ts`: added `CateringFulfillmentCopy` and the two
  new `CateringPageContent` keys (`orderFormEnabled`, `fulfillmentCopy`),
  mirrored field-for-field off `restaurant-portal`'s own already-shipped
  copy of this same interface (`types/website.ts@77631b0`) rather than
  reinventing the shape — `updateWebsiteContent` confirmed still opaque
  (`content[page]` written whole, no field list to narrow), so no
  behaviour change.

  **One interpretation call, flagged rather than silently resolved:** the
  validation table names only "`note` over 500 chars" as invalid and says
  nothing about a present-but-non-string `note`. Chose the narrow reading —
  check `note`'s length only when it is a `string`; a present non-string
  `note` is neither named as invalid by the table nor type-enforced
  anywhere else on this same public endpoint today (`full_name`/`phone`/
  `requirements` all pass through with zero type validation) — over the
  wider, `name`-symmetric reading (reject any non-string `note`), to avoid
  inventing a rejection condition the design never states.

  **Self-tested. No live Postgres to insert against this session** (no CLI,
  no MCP) — same standing limitation `ENG-031`'s own migration hop
  recorded. `deno check`: fails identically before and after this diff
  (`Could not find a matching package for 'npm:...'` — no
  `deno.json`/`node_modules` anywhere in this repo, the pre-existing gap
  `config/projects.md` already names as its own future ticket, not
  something this diff introduces or could fix). `deno lint`: 10 problems
  before this diff and 10 after (`git stash` diff against the pristine
  files) — zero new. The diff's own one new lint hit (`no-explicit-any` on
  the validator's callback parameter) fixed by dropping the redundant type
  annotation rather than casting.

  **Committed and pushed**, single repo: `aiorders-api@e3ef26a`
  (`feat/ENG-033-catering-request-order-capture-endpoint`, tracking
  `origin/feat/ENG-033-catering-request-order-capture-endpoint`); no PR
  opened yet — devops's own release-readiness hop, same precedent
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022`/`ENG-024`/`ENG-032` each set.

  **1 transition** (`ready → building`), under the cap of 4. Machine WIP
  unaffected — still 1/1, `ENG-016` family. Approver-facing WIP and
  approval cap unaffected — no gate touched this hop.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** every open `inbox/` item's `notified:`/`nudged:`
  checked fresh against the 24h threshold (current
  `2026-09-04T06:21:56Z`) — `ENG-008`/`ENG-009`/`ENG-010` already carry
  their one-time `nudged:`; `ENG-015` (~20h18m), `ENG-027` rescope
  (~17h06m), `ENG-028` (~14h11m) all still under 24h; the four P0 incident
  notices (`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`) left as-is, same
  standing informational treatment this board has given them all day.
  Nothing crossed, nothing raised this pass. **No observations filed** —
  the `deno.lock` re-sighting is a fourth confirmation of an
  already-three-times-noticed item, not a new finding; the `note`-typing
  interpretation call is recorded above, in this ticket's own log, same
  precedent `ENG-032`'s table/Data-section discrepancy set for its own
  judgement calls. **Step 6b:** not run — the new `action_type`/`selections`
  columns and the two new `status` strings are product data, not
  business-os process artifacts, and the two new `CateringPageContent`
  interface keys are the same kind of product-level type documentation
  `ENG-032`'s own hop already exempted on this identical interface (same
  reasoning, both citing `ENG-024`'s `show_in_marketplace` precedent).
  **Journal:** n/a — no G1/G2/G3 or merge request answered this pass.

  `chained: ENG-033` — `building` is agent-owned (next hop `in-review`,
  owned by `principal-engineer`); not the approver, not blocked, not
  terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` **review round 1: FAIL** (principal-engineer, combined
  review+quality hop, `continue ENG-033` event pass, per prior pass's own
  `chained: ENG-033`). Mode clean, pre-pass gate-check exit 0 (scoped +
  whole-board). 0/10 automatic failures.

  **Blocking:** `isValidSelections` (`catering-request/index.ts`) checks
  `note`'s length only when it's a string, so a present non-string `note`
  (e.g. an object) passes validation. Verified downstream:
  `CateringDetailModal.tsx:342` renders it as a bare JSX child with no
  error boundary anywhere in `restaurant-portal` — an object there throws
  on render, reachable by anyone since this endpoint is unauthenticated.
  Cites `engineering-standards.md`'s existing "failure direction is
  uniform" rule directly: `quantity`/`name` fail closed, `note` doesn't.
  Fix: reject any present non-string `note`, symmetric with `name`.
  Two non-blocking notes and one style preference, not blocking this
  round. Full trace, the interpretation-call reasoning, and the
  `category`/`item_id` safety check: `agents/principal-engineer/notebook/
  2026-09-03-review-log.md`.

  No receipt written, `links.review` untouched. QA's hop not run this
  round (discarded — the flagged code is about to change), no test-plan
  file. **0 net transitions** — `state`/`owner` unchanged
  (`building`/`eng-manager`), same precedent this board's other round-1
  fails set. WIP/approval caps unaffected. `time_spent`/`time_remaining`
  updated in frontmatter.

  Dead-end sweep: no other ticket touched. Notify sweep: current
  `2026-09-04T06:48:23Z` — every open inbox item still under 24h or
  already carrying its one nudge; nothing crossed, nothing raised (a
  review fail isn't approver-facing). No new observations — the
  cap_lines/notebook-routing gap is already tracked
  (`observations.md`, this same date). Step 6b: not run, review hop not a
  build hop. Journal: n/a.

  `chained: ENG-033` — `building` is agent-owned (round 1's one finding is
  the next hop's own work), not the approver, not blocked, not terminal,
  not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-03` **fix round 1 finding, no state change** (backend, `continue`
  event pass, context `ENG-033`, per prior hop's own `chained: ENG-033`).
  Reading map for `continue`: steps 6 and 6b (design already complete, not
  mid-PRD), plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*, *The four lanes*, *Guards*). Mode check clean (repo-root
  `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`, scoped (`ENG-033`)
  and whole-board: both exit 0.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint — matches it verbatim (`building`/`eng-manager`, round 1 FAIL,
  one blocking finding). Worktree (`~/Documents/projects/_eng/aiorders-api`)
  confirmed already on the right branch, clean aside from the standing
  unrelated untracked `deno.lock`; no branch-fix needed this time.

  **Applied the exact fix the review specified.**
  `isValidSelections` (`catering-request/index.ts:176`) checked `note`'s
  length only when it was already a `string`, so a present non-string
  `note` skipped validation and could reach `restaurant-portal`'s unguarded
  render. Changed to reject any present `note` that isn't a string,
  symmetric with `name`: `if (note !== null && note !== undefined &&
  (typeof note !== 'string' || note.length > MAX_NOTE_LENGTH)) return
  false;`. Cross-checked against the design's own `## Data` section, which
  types the element's `note` as `"note": string | null` — the fix enforces
  exactly that contract, nothing wider. Left the two non-blocking notes and
  the style preference alone; round 1 was explicit neither blocks, and
  fixing unrequested scope isn't this hop's job.

  **Step 6b: not run.** One-line logic fix inside a validation function
  already built this ticket — no receipt path, state name, config key, or
  cross-agent-referenced artifact involved, so there's no artifact rule to
  enumerate mentions for.

  **Self-tested, same method the build hop used.** `deno check` fails
  identically before and after (pre-existing `npm:openai` resolution gap,
  unrelated to this file, already tracked as its own future ticket).
  `deno lint` on both files this ticket has touched: 10 problems at the
  committed baseline (`e3ef26a`, via `git stash`) and 10 after this fix —
  zero new.

  **Committed and pushed**, single repo: `aiorders-api@b9a22a2` (same
  branch, `feat/ENG-033-catering-request-order-capture-endpoint`).

  **0 transitions** — state/owner left at `building`/`eng-manager`, same
  shape round 1 itself used: a review *pass* is what moves this ticket
  forward, not the fix that precedes it. `time_spent`/`time_remaining` and
  `branch` updated in frontmatter.

  Dead-end sweep: no other ticket touched. Notify sweep: current
  `2026-09-04T06:55:55Z` — `ENG-008`/`ENG-009`/`ENG-010` already carry
  their one-time `nudged:`; `ENG-015` (~20h52m), `ENG-027` (~17h40m),
  `ENG-028` (~14h45m), and all four P0 incident notices (`ENG-029`/
  `ENG-030`/`ENG-035`/`ENG-036`, oldest ~16h18m) still under 24h. Nothing
  crossed, nothing raised. No new observations — the untracked `deno.lock`
  is unchanged and already four-times noted; nothing else novel in a
  one-line fix. Journal: n/a — no G1/G2/G3 or merge request answered this
  pass.

  `chained: ENG-033` — `building` is agent-owned (next hop is review round
  2, owned by principal-engineer); not the approver, not blocked, not
  terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` **review round 2: FAIL** (principal-engineer, combined
  review+quality hop, `continue ENG-033` event pass, per prior hop's own
  `chained: ENG-033`). Reading map for `continue`: steps 6 and 6b (design
  already complete, not mid-PRD), plus the not-negotiable set (1, 7, 8b, 9,
  10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check
  clean (repo-root `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`,
  scoped (`ENG-033`) and whole-board: both exit 0.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint — matches it verbatim (`building`/`eng-manager`, round 1 FAIL
  fixed, next hop review round 2). Worktree
  (`~/Documents/projects/_eng/aiorders-api`) confirmed on
  `feat/ENG-033-catering-request-order-capture-endpoint@b9a22a2`, clean
  aside from the standing untracked `deno.lock`. `git fetch` +
  `git diff origin/main...HEAD --stat`: still 2 files, 59/1 — merge-base
  against `origin/main` unchanged since round 1 (the only new commits on
  `origin/main` since this branch's base are `ENG-013`/`ENG-015`, checked
  via `git log HEAD..origin/main` and `git diff HEAD...origin/main --stat`
  rather than assumed harmless: neither touches `catering-request/` or
  `brand-portal/website.ts`).

  **Automatic-failure scan: 1/10** — re-run fresh against the full current
  diff, not carried forward from round 1's 0/10. One hit: **missing test on
  a bug fix.** Round 1's finding was a confirmed, reachable defect (a
  present-but-non-string `note` skipping validation and reaching
  `restaurant-portal`'s unguarded render on an unauthenticated public
  endpoint); `b9a22a2` fixes the logic exactly as specified — re-verified
  against the current diff, not trusted from either prior hop's account
  (`index.ts:176`: `if (note !== null && note !== undefined && (typeof note
  !== 'string' || note.length > MAX_NOTE_LENGTH)) return false;`) — but adds
  no regression test anywhere. `catering-request/` has no test file at all,
  `isValidSelections` isn't exported, and `engineering-standards.md`'s rule
  here carries no qualifier: "Every bug fix ships with the regression test
  that would have caught it. No exceptions."

  Checked for an infrastructure excuse rather than assuming one either way:
  none exists. `deno test` against an existing file in this exact repo
  (`platform-customer-auth/validation.test.ts`) ran clean with zero setup,
  no `deno.json` needed. Same-day, directly-on-point precedent already sits
  in this repo: `platform-customer-auth/validation.ts` +
  `validation.test.ts` unit-tests a pure boundary-validation function
  (`validatePhoneStrict`) with `Deno.test`/`assertEquals` over exactly this
  edge-case class (null/undefined/wrong-type input) — `isValidSelections` is
  the same shape and is the only function like it on this board with zero
  coverage. Also worth naming: this board's own closest precedent,
  `ENG-032`'s round 1 (also "bug fix, no test" — a silent field-wipe), had
  its own round-2 fix hop close the gap by adding
  `CateringPageForm.test.tsx`, same day, mutation-verified. This ticket's
  own fix hop fixed the logic but didn't take that same second step.

  Fix specified: export `isValidSelections` (or split it into its own
  `validation.ts`, mirroring `platform-customer-auth`'s own split — either
  shape is fine), add `catering-request/index.test.ts` covering the round-1
  regression itself plus the design's named boundaries (200/201-element
  cap, non-integer/non-positive `quantity`, non-string `name`, `note` at
  500/501 chars, `note: null`/omitted, one fully-valid case). Full
  citation-by-citation detail:
  `agents/principal-engineer/notebook/2026-09-04-review-log.md`.

  Two non-blocking notes and one style preference carried forward from
  round 1 unchanged, independently re-checked against the current diff
  rather than assumed still true (empty `name: ""`; empty `selections: []`
  yielding `Quote Generated`; validation-block placement) — none touched by
  the fix, none blocking. One new non-blocking note: `website.ts`'s own
  comment cites ADR-009, confirmed correct this round against
  `restaurant-portal`'s shipped interface (read from `origin/main` in the
  department's own `_eng` worktree, not the human's checkout — field-for-
  field identical, including the comment text) — but the ticket's own
  `links.adrs` still names only `ADR-008`. Worth fixing at the next
  frontmatter touch; not blocking.

  No receipt written, `links.review` untouched. QA's hop discarded this
  round too — a missing-test finding makes a real quality-gate run
  premature, same precedent `ENG-032`'s own round 1 already set. **0 net
  transitions** — `state`/`owner` unchanged (`building`/`eng-manager`), same
  shape round 1 used. WIP/approval caps unaffected. `time_spent`/
  `time_remaining` updated in frontmatter.

  Dead-end sweep: no other ticket touched. Notify sweep: current
  `2026-09-04T07:07:55Z`, timestamps re-read fresh from each inbox file
  rather than trusted from the prior pass's own account —
  `ENG-008`/`ENG-009`/`ENG-010` already carry their one-time `nudged:`;
  `ENG-015` (~21h4m), `ENG-027` (~17h52m), `ENG-028` (~14h57m), and all four
  P0 incident notices (`ENG-029`/`ENG-030`/`ENG-035`/`ENG-036`, oldest
  ~16h30m) still under 24h. Nothing crossed, nothing raised — a review fail
  isn't approver-facing. No new observations — the missing-test finding is
  this round's own review verdict, not a process gap; the already-open
  proposal on `aiorders-api`'s unregistered test command (`proposals.md`,
  2026-09-03, filed against `ENG-031`) covers the adjacent config-staleness
  point and isn't restated here. Step 6b: not run — review hop, not a build
  hop. Journal: n/a — no G1/G2/G3 or merge request answered this pass.

  `chained: ENG-033` — `building` is agent-owned (next hop is fix round 2:
  add the missing test, then review round 3); not the approver, not
  blocked, not terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` **fix round 2 finding: exported `isValidSelections`, added
  regression coverage** (backend, `continue` event pass, context `ENG-033`,
  per prior hop's own `chained: ENG-033`). Reading map for `continue`: steps
  6 and 6b (design already complete, not mid-PRD), plus the not-negotiable
  set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four lanes*,
  *Guards*). Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
  `eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both exit 0.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint — matches it verbatim (`building`/`eng-manager`, round 2 FAIL,
  next hop fix round 2).

  **Worktree was not clean — investigated rather than assumed.**
  `~/Documents/projects/_eng/aiorders-api` carried a modified
  `catering-request/index.ts` plus two untracked files, `validation.ts` and
  `index.test.ts`, none of it committed and none of it mentioned anywhere in
  this ticket's own log. Traced rather than guessed at:
  `traces/eng-loop-2026-09-04.log` shows a `continue (ENG-033)` fire at
  `00:22:14` that never-started on an account session-limit (correctly
  refunded, re-queued at the same attempt, rotated to account 2 of 3), then
  a second fire at `00:27:22` that launched a real session on that rotated
  account (`00:27:23`) — and the log **ends there, 18 lines total, no
  `pass end` ever written for that launch.** `traces/.hops-2026-09-04-
  ENG-033` reads `2`, matching the count already present at *both* the
  00:22 and 00:27 pass-start lines — the crashed session never reached the
  point where the wrapper increments it. The three files' mtimes
  (`00:30:11`–`00:30:59`) sit squarely inside that session's run: it
  launched, worked just over three minutes, produced exactly fix round 2's
  own spec, and died before the wrapper could log a pass end, commit, write
  the ticket log, or fire a chain — not an agent forgetting a step, the
  orchestration layer itself never reached its own bookkeeping. Distinct
  from every previously-recorded instance of this failure family
  (`observations.md`, 2026-08-27, `ENG-005`: committed but unlogged;
  `proposals.md`, 2026-08-30, `ENG-013`: committed and pushed but unlogged):
  this one never reached a commit at all, so that open proposal's own fix
  (compare the ticket's recorded commit hash against `git log
  {hash}..origin/{branch}`) would not have caught it — there was no hash
  yet to compare. Widened the open proposal rather than filing a new one:
  `proposals.md`, 2026-08-30 row, with this pass's own trace-log/hop-budget/
  mtime evidence attached.

  **Verified rather than trusted before building on it.** Read the full
  diff and both new files. The split matches review round 2's own suggested
  shape exactly — `isValidSelections` moved into `catering-request/
  validation.ts` (mirroring `platform-customer-auth`'s own split, named in
  the review as the precedent to copy), `index.ts` now imports it, and
  `index.test.ts` carries 12 cases. Cross-checked every case against the
  design's own validation table (`agents/architect/designs/ENG-016-
  catering-quote-generator.md`, the `selections` row) rather than trusting
  the test file's own docstring-style names: fully-valid selections, the
  round-1 regression (non-string `note`) by name, `note: null`, `note`
  omitted, `note` at the 500-char boundary (valid) and 501 (invalid),
  exactly 200 selections (valid) and 201 (invalid), non-integer `quantity`,
  non-positive `quantity`, non-string `name`, and `selections` not an array
  — every boundary the design names, one case each, nothing missing and
  nothing invented beyond it.

  **Self-tested before committing.** `deno test` on the new file: 12/12
  pass. `deno lint` on all three touched files found 7 problems; isolated
  which were pre-existing rather than assuming either way — `git stash push
  -u` (scoped to just these three files) plus an in-place lint of the
  stashed-out baseline (this ticket's own established method; a `/tmp`-copy
  shortcut tried first gave a different, invalid result, since import-map
  resolution depends on the file's real path inside the repo tree) showed
  the committed `index.ts` alone already carrying 5 of those 7, unchanged
  line-for-line (`no-import-prefix`/`no-unversioned-import` on the
  pre-existing `jsr:`/`https:` imports, `no-prototype-builtins` on the
  untouched `hasOwnProperty` check — same finding, shifted from line 201 to
  183 only because 18 lines moved out to `validation.ts`). A 6th
  (`no-import-prefix` on `index.test.ts`'s own `assertEquals` import)
  matches, byte for byte, the same rule already firing on `platform-
  customer-auth/validation.test.ts` — the identical import style already
  merged on `main` — confirming it's this repo's standing no-`deno.json`
  gap (the same one `proposals.md`'s 2026-09-03 row already names against
  `ENG-031`) rather than anything this diff introduces. The 7th,
  `no-unused-vars` on a destructured `note` in `index.test.ts`'s
  omitted-note case, was real and new — fixed by renaming the binding to
  `_note` per the linter's own hint, re-ran clean (6 pre-existing, 0 new).
  `deno check` fails identically before and after (the same pre-existing
  `npm:openai` resolution gap named as its own future ticket in `config/
  projects.md`). Grepped the whole repo for
  `isValidSelections`/`MAX_SELECTIONS`/`MAX_NOTE_LENGTH` outside
  `catering-request/` to confirm the extraction broke no other reference:
  none found.

  **Step 6b: not run.** Splitting a validation function into a sibling file
  and adding its test is product code internal to one repo — no receipt
  path, state name, config key, or cross-agent-referenced artifact
  involved, same reasoning round 1's fix hop already gave for its own
  smaller change to this same function.

  **Committed and pushed**, single repo: `aiorders-api@b319a82` (same
  branch, `feat/ENG-033-catering-request-order-capture-endpoint`), covering
  exactly the recovered files plus the one lint fix — the standing
  untracked `brand-portal/deno.lock` left alone again, same as every prior
  hop.

  **0 transitions** — state/owner left at `building`/`eng-manager`, same
  shape every fix hop on this ticket has used: a review pass moves the
  ticket, not the fix that precedes it. `time_spent`/`time_remaining` and
  `branch` updated in frontmatter. Also applied round 2's own deferred,
  non-blocking note here, since this is the next frontmatter touch it named:
  `links.adrs` now reads `[ADR-008, ADR-009]` — confirmed `ADR-009`
  (`agents/architect/decisions/ADR-009-catering-order-form-opt-in-gate.md`)
  is in fact the ADR `website.ts`'s own comment cites, before adding it.

  Dead-end sweep: no other ticket touched. Notify sweep: current
  `2026-09-04T07:31:47Z`, every open `inbox/` item's `notified:`/`nudged:`
  re-read fresh from disk rather than carried from the checkpoint —
  `ENG-008`/`ENG-009`/`ENG-010` already carry their one-time `nudged:`;
  `ENG-015` (~21h28m), `ENG-027` (~18h16m), `ENG-028` (~15h21m), and all
  four P0 incident notices (oldest, `ENG-029`, ~16h54m) still under 24h.
  Nothing crossed, nothing raised. **One proposal widened** (not filed
  fresh): `proposals.md`, 2026-08-30 row, `aiorders-api` — added this
  pass's own concrete evidence (trace-log line count, hop-budget file, file
  mtimes) as a third, materially different variant its current proposed
  fix doesn't cover. No new observations beyond that. Journal: n/a — no
  G1/G2/G3 or merge request answered this pass.

  `chained: ENG-033` — `building` is agent-owned (next hop is review round
  3, principal-engineer); not the approver, not blocked, not terminal, not
  held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` **review round 3: PASS. Quality gate (first real run on this
  ticket): FAIL** (principal-engineer + qa, combined review+quality hop,
  `continue ENG-033` event pass, per prior hop's own `chained: ENG-033`).
  Reading map for `continue`: steps 6 and 6b (design already complete, not
  mid-PRD), plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*, *The four lanes*, *Guards*). Mode check clean (repo-root
  `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`, scoped (`ENG-033`)
  and whole-board: both exit 0.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint — matches it verbatim (`building`/`eng-manager`, round 2 FAIL
  fixed, next hop review round 3). Worktree
  (`~/Documents/projects/_eng/aiorders-api`) confirmed on
  `feat/ENG-033-catering-request-order-capture-endpoint@b319a82`, clean
  aside from the standing untracked `deno.lock`. `git fetch` +
  `git diff origin/main...HEAD --stat`: 4 files, 138/1 — no new commits on
  `origin/main` since round 2's own check.

  **Code review: PASS.** 0/10 automatic failures. Round 2's sole finding
  (missing test on the round-1 `note` bug fix) closed: `index.test.ts`
  covers the regression by name plus every design-named boundary.
  **Mutation-tested the regression test directly this round** rather than
  trusting the fix hop's own "12/12 pass" — round 2 had explicitly asked
  for this and the fix hop's log didn't record doing it. Reverted
  `validation.ts`'s note check to the exact round-1 buggy line
  (`git checkout --` after), reran: 11 passed, 1 failed — only the
  note-rejection case, failing for the right reason
  (`AssertionError: -true/+false`). Lint re-run across all four touched
  files together for the first time this round (11 problems, arithmetic
  reconciles exactly against every prior hop's own file-subset counts — 0
  new). One new non-blocking note: `validation.ts`'s header comment cites
  "platform-customer-auth's own index.ts + handler.ts split" as precedent,
  but the file actually mirrored (and the one round 2 itself named) is
  `platform-customer-auth/validation.ts`, not `handler.ts` — wrong sibling
  named, reasoning still correct, not blocking. Full writeup:
  `agents/principal-engineer/reviews/ENG-033.md`, `links.review` set.

  **Quality gate: FAIL — first time it has actually run on this ticket**
  (rounds 1 and 2 both failed at review, so QA's result was discarded both
  times per `code-review-gate/SKILL.md` step 9). This ticket's own ACs
  (5, 6, 7, 10, 13 — per `ENG-032`'s own scope note) are owned here.
  AC-5/6/7 are implemented by the status-derivation branching in
  `index.ts:247-264` — reads `action_type`, decides `derivedStatus`, decides
  whether `selections` is stored or force-nulled — and **nothing tests that
  branching.** `index.test.ts` imports only `isValidSelections`; the
  derivation logic has no exported entry point, same reason
  `isValidSelections` needed extracting in the first place (`index.ts`
  calls `serve()` at module scope). Traced it by hand against the design's
  own validation table and confirmed it's correct — but per
  `agents/qa/agent.md`'s own refusal list ("Signing off on 'manually
  verified' for something automation could reach"), a hand trace doesn't
  substitute for a test when the logic has no I/O of its own and can be
  extracted the same way `isValidSelections` just was. AC-10 and AC-13
  assessed and recorded as **not automated, with reasons** (no integration
  harness exists for this function at all, same repo-wide gap
  `platform-customer-auth/handler.test.ts` already names; AC-13's actual
  mechanism has zero lines touched by this diff, same call `ENG-032`'s own
  test plan made for its half of this AC) — not blocking, per
  `definition-of-done.md`'s own "Manual verification note where automation
  genuinely can't reach" allowance. **Specific fix:** extract the
  derivation block into a small, pure, exported function alongside
  `isValidSelections` (shape is the engineer's call), test the four
  branches named in full in the test plan — the
  `MANUAL_CONTACT_REQUESTED`-with-selections-sent case most pointedly,
  since it's a discard-on-purpose behaviour the same shape as round 1's own
  bug. No bug filed — not a functional defect, a coverage gap; the traced
  logic is correct. Full finding: `agents/qa/test-plans/ENG-033.md`.

  No security gate run — quality did not pass, so per step 6 ("Security
  stays strictly after quality") there is nothing yet for it to check.

  **0 transitions** — state/owner unchanged (`building`/`eng-manager`),
  same shape every review-outcome entry on this ticket has used: the
  ticket returns to `building` on the quality finding, not the review one;
  review's own PASS stands and will be re-confirmed fresh against the next
  diff, not re-litigated. `time_spent`/`time_remaining` updated in
  frontmatter; `links.review` and `links.test_plan` both set for the first
  time this ticket.

  Dead-end sweep: no other ticket touched. Notify sweep: current
  `2026-09-04T07:53:12Z`, every open `inbox/` item's `notified:`/`nudged:`
  re-read fresh from disk — `ENG-008`/`ENG-009`/`ENG-010` already carry
  their one-time `nudged:`; `ENG-015` (~21h49m), `ENG-027` (~18h38m),
  `ENG-028` (~15h43m), and all four P0 incident notices (oldest, `ENG-029`,
  ~17h16m) still under 24h. Nothing crossed, nothing raised — a quality-gate
  fail isn't approver-facing. No new proposal or observation filed: the
  finding closes within this ticket's own next hop, doesn't need a ticket
  or approval of its own — recorded instead in
  `agents/qa/notebook/2026-09-04-coverage-gaps.md`, named there as a
  pattern to watch (this is the second time this diff family turned out
  untestable only because logic stayed inline in `index.ts`'s `serve()`
  callback rather than being extracted) without filing a proposal over a
  two-instance pattern — `engineering-standards.md`'s own promotion
  mechanism is three. Step 6b: not run — this hop wrote review/test-plan
  receipts and ticket frontmatter/log only, no receipt path, state name,
  config key, or cross-agent artifact rule was touched. Journal: n/a — no
  G1/G2/G3 or merge request answered this pass.

  `chained: ENG-033` — `building` is agent-owned (next hop is the fix:
  extract and test the derivation logic, then review+quality round 4); not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` **fix: quality-gate finding fixed — extracted and tested the
  status-derivation logic. Stays `building`** (`continue ENG-033` event
  pass, per prior hop's own `chained: ENG-033`). Reading map for
  `continue`: steps 6 and 6b (design already complete, not mid-PRD), plus
  the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The
  four lanes*, *Guards*). Mode check clean (repo-root `.env` →
  `MODE=active`). Pre-pass `eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: both exit 0.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint — matches it verbatim (`building`/`eng-manager`, round 3
  review PASS, quality gate round 1 FAIL, next hop the extraction fix).
  Worktree (`~/Documents/projects/_eng/aiorders-api`) confirmed on
  `feat/ENG-033-catering-request-order-capture-endpoint@b319a82`, clean
  aside from the standing untracked `brand-portal/deno.lock`. `git fetch` +
  `git diff origin/main...HEAD --stat`: 4 files, 138/1 — no new commits on
  `origin/main` since round 3's own check.

  **Applied the specific fix quality gate named, no more.** Extracted the
  status-derivation block (`index.ts:247-264`) into `deriveActionStatus()`
  in `validation.ts`, alongside `isValidSelections` — same file, using the
  latitude round 2's own export was given ("shape is the implementing
  engineer's call"). The function is pure (no `Response`, no I/O): it
  returns `{ actionType, selections, status, selectionsInvalid }`, and
  `index.ts` destructures that result and turns `selectionsInvalid` into
  the existing 400 — the insert-object code right below it needed no edit
  at all, since it already read `normalizedActionType`/
  `normalizedSelections`/`derivedStatus` by name. `VALID_ACTION_TYPES`
  moved into `validation.ts` with it (its only caller, so nothing left
  behind in `index.ts`). Also applied round 3's own deferred, non-blocking
  note while touching this exact file for the first time since it was
  raised: the header comment named the wrong `platform-customer-auth`
  sibling (`handler.ts`) as precedent — corrected to `validation.ts`, the
  file round 3 confirmed is actually mirrored.

  **Tests: added the five cases quality gate's finding named**, in
  `index.test.ts`, importing `deriveActionStatus` alongside
  `isValidSelections`: `action_type` absent; an unrecognized `action_type`
  (`"bogus"`) treated the same as absent; `MANUAL_CONTACT_REQUESTED` with a
  non-empty `selections` still forcing `null` (the discard-on-purpose case
  named as most likely to silently regress — same shape as round 1's own
  bug); `QUOTE_SUBMITTED` with valid selections stored as-is; and
  `QUOTE_SUBMITTED` with invalid selections signalling `selectionsInvalid`.
  17/17 pass (`deno test --no-check index.test.ts`, the QA test plan's own
  `suite_command`).

  **Self-mutation-tested the discard-on-purpose case before trusting the
  green run** — the same verification rounds 2/3 have each done, done here
  pre-emptively since this is exactly the bug shape (a value present in the
  payload that must not survive into storage) this ticket has already
  regressed on once. Removed the force-null from the
  `MANUAL_CONTACT_REQUESTED` branch: 16 passed, 1 failed — only the new
  discard test, for the right reason (`null` expected, the array received
  instead). **One error during this step, corrected in the same hop, named
  here rather than smoothed over:** restored the file with
  `git checkout --`, which — unlike round 3's own use of that command
  against an already-*committed* baseline — discarded this hop's entire
  uncommitted extraction rather than just the mutation on top of it, since
  none of it had been committed yet. Caught immediately (the next read
  showed the pre-extraction file), redid the extraction identically, and
  re-ran clean: 17/17. Worth naming so a future hop doesn't reach for
  `git checkout --` to undo a self-mutation against a diff that isn't
  committed yet — it only safely restores a committed baseline.

  **Lint:** `deno lint` on the three touched files → 6 problems,
  reconciling exactly against round 3's own combined count (6 across these
  three files + 5 on `website.ts`, not touched this round, = 11) — 0 new.
  **`deno check`:** fails identically before/after, same pre-existing
  `npm:openai` resolution gap named every prior round; unrelated to this
  diff. Committed and pushed: `aiorders-api@697df79`.

  **0 transitions** — state/owner left at `building`/`eng-manager`, same
  shape every fix hop on this ticket has used: a review pass moves the
  ticket, not the fix that precedes it. `time_spent`/`time_remaining` and
  `branch` updated in frontmatter.

  Dead-end sweep: no other ticket touched. Notify sweep: current
  `2026-09-04T08:05:05Z`, every open `inbox/` item's `notified:`/`nudged:`
  re-read fresh from disk — `ENG-008`/`ENG-009`/`ENG-010` already carry
  their one-time `nudged:`; `ENG-015` (~22h1m), `ENG-027` (~18h50m),
  `ENG-028` (~15h55m), and all four P0 incident notices (oldest, `ENG-029`,
  ~17h28m) still under 24h. Nothing crossed, nothing raised — a build/fix
  hop isn't approver-facing. No new proposal or observation filed: nothing
  surfaced this hop beyond the `git checkout --` note above, which is
  recorded in this log rather than filed separately since it cost this hop
  one redo and nothing downstream. Step 6b: not run — this hop touched only
  product code internal to one repo, no receipt path, state name, config
  key, or cross-agent artifact rule was involved. Journal: n/a — no
  G1/G2/G3 or merge request answered this pass.

  `chained: ENG-033` — `building` is agent-owned (next hop is review+quality
  round 4, against the fresh diff); not the approver, not blocked, not
  terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: both exit 0, see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` **`building → in-review → in-qa`** (principal-engineer + qa,
  combined review+quality hop, `continue ENG-033` event pass, per prior
  hop's own `chained: ENG-033`). Reading map for `continue`: steps 6 and 6b
  (design already complete, not mid-PRD), plus the not-negotiable set (1, 7,
  8b, 9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode
  check clean (repo-root `.env` → `MODE=active`). Pre-pass
  `eng-gate-check.sh`, scoped (`ENG-033`) and whole-board: both exit 0.

  Ticket file read directly rather than trusted from the trigger's
  checkpoint — matches it verbatim (`building`/`eng-manager`, round 3 review
  PASS, quality gate round 1 FAIL fixed, next hop review+quality round 4).
  Worktree (`~/Documents/projects/_eng/aiorders-api`) confirmed on
  `feat/ENG-033-catering-request-order-capture-endpoint@697df79`, clean
  aside from the standing untracked `brand-portal/deno.lock`. `git fetch` +
  `git diff origin/main...HEAD --stat`: 4 files, 201/1. `git log
  HEAD..origin/main` showed two new merges since round 3's check
  (`ENG-013`, `ENG-015`); `git diff HEAD...origin/main --stat` confirmed
  neither touches `catering-request/` or `brand-portal/website.ts`
  (`admin-portal/` handlers and two migrations only).

  **Review: PASS, round 4.** Isolated the actual change since round 3's own
  reviewed commit (`git diff b319a82..697df79 --stat`: 3 files) rather than
  re-reviewing the full cumulative diff. Automatic-failure scan re-run fresh:
  0/10. Traced the extraction against the pre-extraction code branch by
  branch and confirmed it's behaviour-preserving — same stored values, same
  400 body/headers/status on every path. Full writeup:
  `agents/principal-engineer/reviews/ENG-033.md`, `links.review` unchanged
  (same path, content replaced).

  **QA: PASS, quality-gate round 2.** AC-5(storage), AC-6 and AC-7 — the
  three criteria round 1 of this gate found untested — now each have a
  passing test against `deriveActionStatus`. AC-10/AC-13 unchanged,
  not-automated-with-reasons, neither touched by this round's diff, both
  accepted under `definition-of-done.md`'s manual-verification allowance.
  No open P0/P1 (`BUG-001` open but unrelated function, same project). Full
  writeup: `agents/qa/test-plans/ENG-033.md`, `links.test_plan` unchanged
  (same path, content updated in place with round 1 kept as history).

  **Independent verification, not trusted from the fix hop's own account —
  this round's central activity.** Ran the suite fresh (17/17). Mutation-
  tested two branches of `deriveActionStatus` directly, each restored via
  `git checkout --` against the committed `697df79` baseline (safe here,
  unlike the fix hop's own noted mistake against an uncommitted diff):
  removing the `MANUAL_CONTACT_REQUESTED` force-null flipped exactly the
  discard-on-purpose test (16 passed, 1 failed, right reason); corrupting
  the absent/unrecognised fallback's `status` flipped exactly the two tests
  exercising that branch (15 passed, 2 failed). Both restores confirmed
  clean via `git diff --stat` before re-confirming 17/17. Lint on all four
  touched files: 11 problems, reconciling exactly against round 3's own
  count, attributed file-by-file this time — 0 new, and `validation.ts`
  itself (this hop's only changed logic file) carries zero lint issues.
  `deno check` fails identically (pre-existing `npm:openai` gap). Grepped
  for other callers of the moved symbols (`VALID_ACTION_TYPES`/
  `isValidSelections`/`deriveActionStatus`): none outside `catering-request/`.
  Verified round 3's deferred header-comment correction against the actual
  `platform-customer-auth/validation.ts` file rather than accepting it:
  accurate.

  No security gate run this hop — per step 6 ("Security stays strictly
  after quality"), it starts once quality has passed, which is this hop's
  own result; it belongs to the next session.

  **2 transitions** (`building → in-review → in-qa`), under the cap of 4.
  Machine WIP unaffected — still 1/1, `ENG-016` family. No approver-facing
  WIP or approval-cap change — no gate answered this hop.
  `time_spent`/`time_remaining` updated in frontmatter.

  Dead-end sweep: no other ticket touched. Notify sweep: current
  `2026-09-04T08:18:28Z`, every open `inbox/` item's `notified:`/`nudged:`
  re-read fresh from disk — `ENG-008`/`ENG-009`/`ENG-010` already carry
  their one-time `nudged:`; `ENG-015` (~22h15m), `ENG-027` (~19h3m),
  `ENG-028` (~16h8m), and all four P0 incident notices (oldest, `ENG-029`,
  ~17h41m) still under 24h. Nothing crossed, nothing raised — a review/
  quality pass isn't approver-facing on its own. No new proposal or
  observation filed: round 3's own prose approximated the lint
  reconciliation as "two pre-existing `no-explicit-any`/`no-prototype-
  builtins` items" when the actual file-by-file count is four
  `no-explicit-any` plus one `no-prototype-builtins` — noted here because
  it's this hop's own finding, not filed further, since the total (11, 0
  new) was and remains correct and no verdict anywhere depended on the
  finer breakdown. Step 6b: not run — this hop wrote review/test-plan
  receipts and ticket frontmatter/log only, same reasoning round 3 gave.
  Journal: n/a — no G1/G2/G3 or merge request answered this pass.

  `chained: ENG-033` — `in-qa` is agent-owned (security next); not the
  approver, not blocked, not terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-033` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: see board index for result.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` **`in-qa → ready-to-ship`: security gate — PASS** (security,
  `continue ENG-033` event pass, per prior hop's own `chained: ENG-033`).
  Reading map for `continue`: steps 6 and 6b (design already complete, not
  mid-PRD), plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*; *The four lanes*; *Guards*). Mode check clean (repo-root
  `.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`, scoped (`ENG-033`)
  and whole-board: both exit 0.

  Ticket file read directly, not trusted from the trigger's checkpoint —
  matched verbatim (`in-qa`/`eng-manager`, round 4 review PASS, quality gate
  round 2 PASS, security next). Worktree
  (`~/Documents/projects/_eng/aiorders-api`) confirmed on
  `feat/ENG-033-catering-request-order-capture-endpoint@697df79`, clean
  aside from the standing untracked `brand-portal/deno.lock`; `git fetch`
  showed no new commits since round 4's own check.

  **Security gate: PASS.** Full threat model, OWASP walk (all ten marked,
  most `n/a` with reasons — no new route, no auth/session/crypto/config/
  dependency/logging/SSRF surface anywhere in this diff), LLM checklist n/a
  (no model/agent/tool/MCP anywhere in this diff), secrets scan clean (diff
  and all four branch commits). Read `restaurant-portal/CateringDetailModal.tsx`
  directly to confirm the two new fields' only render path escapes by
  construction (JSX interpolation, no `dangerouslySetInnerHTML`) rather than
  assuming it from `ENG-032`'s own already-passed review. Read the full
  `catering-request/index.ts` (not just this diff's hunk) for trust-boundary
  context per the design's own framing of `status` as "the one place this
  ticket lets external input influence a field the owner acts on" — confirmed
  `deriveActionStatus` never sources it from the request body.

  **Two non-blocking findings, both pre-existing and outside this diff, found
  while reading the full function rather than just the diff hunk.** (1) A
  real HTML-injection gap in the owner-notification email
  (`index.ts:348-378`, unchanged by this diff, forwarded verbatim to a
  third-party webhook via `send-notification/index.ts:142-162`) — Medium
  severity, filed as a proposal (`proposals.md`, security, `aiorders-api`)
  and logged (`agents/security/notebook/2026-09-04-findings.md`); this
  ticket's own two new fields are not included in either template, so it
  neither creates nor worsens it. (2) `selections[].name` carries no length
  cap unlike sibling field `note` — Low severity, logged as an observation
  only (`observations.md`), not filed as a proposal — the design's own spec
  doesn't call for one either. Full writeup, including the exact
  category/severity/location/exploit-path/fix for each:
  `agents/security/reviews/ENG-033.md`, `links.security_review` set.

  **RLS-verification gap named for this exact gate by
  `agents/security/notebook/2026-09-03-findings.md`, independently
  re-checked rather than carried forward on trust — still open.** Searched
  for a Supabase/Postgres MCP tool this session; none available (same
  standing tooling gap `ENG-015`'s and `ENG-031`'s own hops already named,
  not new). Re-derived the static evidence myself: `grep`-confirmed no
  tracked migration runs `ENABLE ROW LEVEL SECURITY` on `catering` or
  `restaurants` (other tables do, in tracked history), and read
  `20250729143357_initial_restaurant_rls.sql` in full — its own framing
  ("Phase 1: Critical Database Security Fixes", removing "dangerous
  policies" that were "exposing all restaurant data") only makes sense if
  RLS was already enforced, slightly stronger evidence than the prior hops'
  "policies existed" argument alone. Same non-blocking conclusion, reached
  independently. Not re-routed to a future ticket this time (`ENG-034`
  doesn't touch reads of this table either, and a third silent punt would
  just be a fourth occurrence waiting to happen) — instead surfaced as a
  direct, ten-second ask to the approver in this pass's own L1 merge-request
  item, since only they have the live dashboard access this pipeline lacks.
  Full detail: `agents/security/reviews/ENG-033.md`, RLS verification
  section, and this notebook's own 2026-09-04 entry.

  **1 transition** (`in-qa → ready-to-ship`) — security-gate's own SKILL.md
  step 9 writes `ready-to-ship` directly on a pass; `in-security` is never
  itself persisted, same shape `ENG-022`'s own security hop used. Under the
  cap of 4. Machine WIP unaffected — still 1/1, `ENG-016` family (`ENG-034`
  still `ready`, dependent on this ticket). No approver-facing WIP change —
  `wip.approver_limit` is uncapped since 2026-09-02; no gate answered this
  hop regardless. `time_spent`/`time_remaining` updated in frontmatter.

  Dead-end sweep (scoped to this event): no other ticket touched. Notify
  sweep: current `2026-09-04T08:36:57Z`, every open `inbox/` item's
  `notified:`/`nudged:` re-read fresh from disk — `ENG-008`/`ENG-009`/
  `ENG-010` already carry their one-time `nudged:`; `ENG-015` (~22h33m),
  `ENG-027` (~19h21m), `ENG-028` (~16h26m), and all four P0 incident notices
  (oldest, `ENG-029`, ~17h59m) still under 24h. Nothing crossed, nothing
  raised this pass on its own — a security-gate pass isn't approver-facing
  by itself, though the two findings above are routed to their own channels
  (proposal, observation) rather than held silently. Step 6b: not run — this
  hop wrote a review receipt and ticket frontmatter/log only, no artifact
  rule involved. Journal: n/a — no G1/G2/G3 or merge request answered this
  pass (one is about to be raised, by the same pass, immediately below —
  journaled only once it's answered).

  Continuing in the same pass as devops for `ready-to-ship`, per dispatch's
  "consecutive machine-owned states" rule — see the next log entry rather
  than chaining a fresh hop for a state this session can finish itself.

- `2026-09-04` **`ready-to-ship → blocked`: release-readiness — PR opened,
  merge request raised** (devops, same `continue ENG-033` event pass,
  continuing forward from this pass's own `in-qa → ready-to-ship` hop
  immediately above per dispatch's "consecutive machine-owned states" rule —
  not a fresh chain).

  **Verified all three upstream gates fresh from the receipt files**, not
  assumed from frontmatter: code review
  (`agents/principal-engineer/reviews/ENG-033.md`, `verdict: pass`, round 4),
  quality (`agents/qa/test-plans/ENG-033.md`, `last_result: pass`, round 2),
  security (`agents/security/reviews/ENG-033.md`, `verdict: pass`, this same
  pass). No migration applies to this diff — the two nullable columns
  shipped separately under `ENG-031`, already merged and verified. Worktree
  (`~/Documents/projects/_eng/aiorders-api`) reconfirmed clean on
  `feat/ENG-033-catering-request-order-capture-endpoint@697df79`; `git
  fetch` plus an ahead/behind check against `origin/main` showed 4 ahead, 0
  behind — no drift since the security hop's own check minutes earlier.
  `gh pr list --head feat/ENG-033-catering-request-order-capture-endpoint
  --state all` confirmed no PR already existed for this branch.

  **Project registered L1** (`config/projects.md`) — step 1's window check
  does not apply. **Step 3 readiness checks**, same interpretation this
  board already established for `ENG-007`/`ENG-008`/`ENG-013`/`ENG-022`:
  - Rollback: no migration and no stored-state change in this diff —
    reverting the single PR (or the merge, once merged) fully and safely
    undoes it. The two columns it writes into are independently rollback-safe
    (nullable, added by `ENG-031`, already accounted for in that ticket's own
    release record).
  - Observability: the one new failure path (invalid `selections`) returns a
    synchronous 400 directly to the caller — visible immediately to whoever
    submits the form, not a silent background failure; the pre-existing DB
    insert-error path already logs (`console.log(error)`, unchanged).
  - Cost: **$0/month delta** — no new dependency, no new vendor (security
    review's own Dependencies section, re-confirmed here).
  - Window: n/a, L1.

  **Opened the PR**: `aiorders-api` #13
  (https://github.com/harsimranwalia/aiorders-api/pull/13). Body states what
  the endpoint now accepts, why `status` is server-derived and never
  client-supplied, the three gates passed, and the same two non-blocking
  findings plus the RLS ask named below — written out in full rather than
  left as a draft.

  **Wrote the L1 merge-request item**
  (`inbox/2026-09-04-eng033-merge-request.md`), plain `pr_url:` string per
  `skills/release-runner/SKILL.md` step 4 (single repo, no `pr_urls:` list
  needed). Set `time_estimate: ~half a day` on the item, mirroring the
  ticket's own field, per `definition-of-done.md`'s Time tracking section.
  Surfaced this pass's own two non-blocking security findings in the item's
  own "Named gaps" section, same as `ENG-008`'s precedent — including a
  direct, low-cost ask (confirm RLS is on for `catering`/`restaurants` via
  the Supabase dashboard) rather than leaving it buried in a notebook file a
  fourth time. Ran `departments/engineering/lib/eng-notify.sh raise` —
  logged `sent: active 2026-09-04-eng033-merge-request.md` in today's notify
  trace; stamped `notified: 2026-09-04T01:43:02` on the item by hand
  (copied verbatim from the log, matching this board's own already-flagged
  local-time-labeled-as-UTC convention — `proposals.md`, 2026-09-02 — rather
  than hand-correcting one item out of step with every other timestamp on
  this board).

  State `ready-to-ship → blocked`, `blocked_on: approver`,
  `blocked_from: ready-to-ship`, owner `devops → approver`. `links.pr` set
  to the PR URL. No release record yet, per `release-runner`'s own step
  7/step 4 split — written only once the build loop's merge-detection
  confirms the PR merged.

  **1 transition** (`ready-to-ship → blocked`), bringing this pass's total
  to **2** (`in-qa → ready-to-ship → blocked`), under the cap of 4.
  **Consequence:** `ENG-033` leaves the counted `ready`..`ready-to-ship`
  range, but the `ENG-016` family's machine-WIP slot stays occupied —
  `ENG-034` (`depends_on: [ENG-033]`) is still `ready`, unshipped, and the
  parent itself is still `building`; per this board's own first-precedent
  reading (`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`),
  the slot is held by the family, not freed by one child's own exit from the
  counted range. No approver-facing WIP change to report —
  `wip.approver_limit` is uncapped since 2026-09-02.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume. **Notify sweep:** this pass's own item raised and
  stamped above (see the `in-qa → ready-to-ship` entry immediately above for
  the full open-inbox age check — nothing else crossed 24h). **Observations/
  proposals filed:** both already routed at the security gate, one entry
  back — nothing new this hop.

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human
  gate the whole pass was driving toward; firing `continue ENG-033` again
  would only queue against a ticket with nothing left for a machine to do,
  same reasoning `ENG-008`'s and `ENG-022`'s own release-readiness entries
  already recorded at this identical state. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-033`) and
  whole-board: see board index for result.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-04` `blocked → shipped → verified` (eng-manager, `watch
  (launchd)` event pass — step 5, run because open merge-request items
  exist for every currently-`blocked` ticket). `git fetch origin` fresh on
  `~/Documents/projects/_eng/aiorders-api`, then `git merge-base
  --is-ancestor` on this ticket's own recorded commit (`697df79`) against
  `origin/main`: **YES**. Cross-checked with `gh pr view 13 --repo
  harsimranwalia/aiorders-api`: `state: MERGED`, `mergedAt:
  2026-09-04T15:25:13Z`, merge commit `cd40bbf` — exactly `origin/main`'s
  tip two commits back (the `ENG-009`/`ENG-010` consolidating merge landed
  on top of it ~14 minutes later, unrelated). `decision:` on
  `inbox/2026-09-04-eng033-merge-request.md` stayed blank — merged directly
  on GitHub, same shape every prior silent merge on this board.

  **Not advanced past a state that owes gates.** Re-read all three receipts
  directly: `agents/principal-engineer/reviews/ENG-033.md` (`verdict:
  pass`, round 4), `agents/qa/test-plans/ENG-033.md` (`last_result: pass`),
  `agents/security/reviews/ENG-033.md` (`verdict: pass`); no migration
  applies to this ticket (`ENG-031` owned the schema). Branch tip matches
  this ticket's own frontmatter exactly (`697df79`), no drift between what
  was reviewed and what merged. Release record written:
  `agents/devops/releases/2026-09-04-aiorders-api-ENG-033.md`,
  `links.release` set in the same edit. `state: blocked → verified`,
  `owner: approver → eng-manager`, `blocked_on`/`blocked_from` cleared.

  Merge-request item moved to `inbox/_handled/`. Journal entry added
  (`decision-journal.md`) — silent GitHub merge, no written reply, same
  shape as this board's prior occurrences.

  **2 transitions** (`blocked → shipped`, `shipped → verified`), well under
  the cap of 4 — receipt-confirmation and bookkeeping only, no new
  implementation work. **Consequence:** no machine-WIP change of its own —
  `ENG-033` was already outside the counted `ready..ready-to-ship` range
  while `blocked`, same as `ENG-032`'s own shipping pass recorded. But
  `depends_on: [ENG-033]` on `ENG-034` (the last `ENG-016` sub-ticket, sole
  remaining member of the family not yet `shipped`) is now satisfied —
  `ENG-034` sits `ready`, `owner: eng-manager`, held only by that
  dependency per its own log ("not yet agent-actionable"). Per this
  family's own first-precedent reading
  (`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`), the
  machine-WIP slot is held by the family as a whole, not freed by one
  child's exit — dispatching `ENG-034` needs no fresh slot. **Fired
  `continue ENG-034`** rather than building it inline (new implementation
  work stays out of a `watch` event's contract), same handoff shape
  `ENG-031`'s and `ENG-032`'s own shipping passes already used for their
  own successors.

  `chained: ENG-034` — not this ticket (`verified` is terminal, the
  chaining guard never fires on it), but the sibling its own shipping
  unblocked. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-033`) and whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.
