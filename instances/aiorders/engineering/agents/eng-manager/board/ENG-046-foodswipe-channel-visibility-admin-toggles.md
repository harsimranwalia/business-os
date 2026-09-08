---
id: ENG-046
title: FoodSwipe channel-visibility toggles — admin-hub restaurant details
project: aiorders-admin-hub
type: feature
size: XS
time_estimate: under an hour
time_spent: ~20m
time_remaining: none — waiting on the approver's merge
severity: P3
priority:
state: verified
owner: eng-manager
lane: full
blocked_on: 
blocked_from: 
source: approver
created: 2026-09-07
updated: 2026-09-07
branch: feat/ENG-046-foodswipe-channel-visibility-admin-toggles
depends_on: [ENG-044]
blocks: []
parent: ENG-026
links:
  prd: agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md
  design: agents/architect/designs/ENG-026-foodswipe-channel-visibility.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-046.md
  test_plan: agents/qa/test-plans/ENG-046.md
  security_review: agents/security/reviews/ENG-046.md
  release:
  pr: https://github.com/harsimranwalia/aiorders-admin-hub/pull/10
---

## Problem

Staff has no UI to set `has_order_food`, `has_dine_in`, or `has_catering` per
merchant. `RestaurantDetails.tsx`'s existing "Restaurant Features" card
already has a `dine_in` Switch, but it's bound to a column nothing on the
consumer side reads.

## Outcome

The "Restaurant Features" card gains two new Switch rows (`has_order_food`,
`has_catering`), matching the six existing rows' exact markup. The existing
Switch repoints to `has_dine_in` per `ENG-044`'s own live-schema resolution
(see Notes). `aiorders-admin-hub/src/integrations/supabase/types.ts` is
regenerated, not hand-edited.

## Notes

Design: `agents/architect/designs/ENG-026-foodswipe-channel-visibility.md` —
`## Components` and `## Interfaces` (`aiorders-admin-hub` — the toggle
surface). Depends on `ENG-044`'s migration: the three columns must exist
before this UI can read/write them.

**No new API call needed.** The existing `PUT /admin-portal/restaurants/:id`
already accepts and persists arbitrary keys.
`RestaurantDetails.tsx` sends its entire `restaurant` state object on save,
so the two new fields and the repointed field are included automatically
once added to the interface and the form — no frontend wiring beyond the
interface/JSX change itself.

**Read `ENG-044`'s own Log before touching the existing `dine_in` Switch —
its resolution decides what this edit actually is:**

- If `ENG-044` found a real, pre-existing `dine_in` column and backfilled
  `has_dine_in` from it: this is a **repoint** — change the Switch's bound
  field from `dine_in` to `has_dine_in` in both the local `Restaurant`
  interface and the JSX. The old `dine_in` column stays in the database,
  unused, until a follow-up ticket drops it (per `ENG-044`'s own Notes) —
  this ticket does not touch the database.
- If `ENG-044` found no such column: `has_dine_in` never existed as a real
  toggle before — this is a **fresh addition**, and whatever the current
  `dine_in` Switch is bound to (if anything real) is unrelated and stays as
  is.

Either way, extend the local `Restaurant` interface with `has_order_food`,
`has_catering` (and `has_dine_in` if not already present under that name),
and regenerate `types.ts` via `supabase gen types typescript` after
`ENG-044`'s migration is live — not hand-edited.

**AC ownership** (mapped in
`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`): this
ticket owns AC2 in full (staff can view and set all three flags).

Branch from `origin/main` in the `aiorders-admin-hub` worktree.

## Log

- 2026-09-07 `(created) → ready` (eng-manager, `work-breakdown`, `continue
  ENG-026` event pass) — sub-ticket of `ENG-026`, sequence 2 (parallel with
  `ENG-045`, both gated only on `ENG-044`), `depends_on: [ENG-044]` unmet,
  held at `ready`. `time_estimate` under an hour. Owner `eng-manager` while
  waiting, reassigned to `frontend` once `ENG-044` ships. Full reasoning:
  `agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`.
  `chained: none` — waiting on an unmet `depends_on: [ENG-044]`, nothing
  agent-actionable until it clears.

- 2026-09-07 `ready → building → in-review` (frontend, `continue ENG-046`
  event pass). `depends_on: [ENG-044]` satisfied (`shipped`). Owner
  `eng-manager → frontend` per this ticket's own creation note. Mode clean;
  pre-pass `eng-gate-check.sh ENG-046` exit 0.

  Repoint confirmed via `ENG-044`'s own Log (`dine_in` real, live,
  backfilled) — repoint, not fresh addition. Built: `RestaurantDetails.tsx`
  gains `has_order_food`/`has_catering` rows, Dine In repointed to
  `has_dine_in`; `types.ts` regenerated, not hand-edited (diff larger than
  this ticket alone — see notebook and `observations.md`, this date).
  Self-test clean: build passes, lint/`tsc --noEmit` zero new issues in
  either touched file. Full detail and PR body:
  `agents/frontend/notebook/2026-09-07-eng046-build.md`.

  Branch `feat/ENG-046-foodswipe-channel-visibility-admin-toggles`,
  committed `a2c51af`, pushed. No PR yet (devops's release-readiness step).

  `chained: ENG-046` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-046`
  before this pass exits.

- 2026-09-07 `in-review → in-qa → in-security` (principal-engineer + qa,
  combined hop, `continue ENG-046` event pass). No drift since the build hop
  (`a2c51af`). **Review: pass** — 0/10 automatic failures; design/`ENG-044`
  live-schema conformance confirmed; all three rows' field-wiring traced
  individually, no cross-wiring. **QA: pass** — AC2 covered by inspection
  against the diff; no suite exists for `aiorders-admin-hub` (open
  proposal, 2026-08-31), same as eight already-untested sibling rows in
  this file; 0 open P0/P1. One notebook-citation inaccuracy found and
  corrected, not a code defect (`observations.md`, this date). Receipts:
  `agents/principal-engineer/reviews/ENG-046.md`,
  `agents/qa/test-plans/ENG-046.md`; `links.review`/`links.test_plan` set.
  No WIP/cap change — still `1/1`, held by the `ENG-026` family. Reasoning:
  `agents/principal-engineer/notebook/2026-09-07-review-log.md`,
  `agents/qa/notebook/2026-09-07-coverage-gaps.md`.

  `chained: ENG-046` — `in-security` is agent-owned (security next), not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-046`
  before this pass exits. Post-pass `eng-gate-check.sh`, scoped (`ENG-046`)
  and whole-board: see board index for result.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- 2026-09-07 `in-security → ready-to-ship` (security, `continue ENG-046`
  event pass). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*). Mode check clean (`MODE=active`). Pre-pass
  `eng-gate-check.sh ENG-046`: exit 0.

  **Found `agents/security/reviews/ENG-046.md` already on disk, verdict
  `pass`, dated this same day** — written by the immediately preceding fire
  of this exact event (`traces/eng-loop-2026-09-07.log`: `11:41:25 pass
  start: continue (ENG-046)`, then `11:47:04 pass FAILED (exit 1) — event
  're-queued as attempt 2/3, NOT consumed`, file mtime `11:47`). That pass
  ran `security-gate/SKILL.md` to completion, wrote the receipt, and then
  **hit its own session usage limit** — the log's own line, verbatim:
  "You've hit your session limit · resets 12:50pm (America/Vancouver)",
  logged directly after that pass's `Write` of the receipt — before writing
  back to this ticket's own frontmatter/log or the board index, and before
  chaining. A capacity cutoff, not an application error. The next two fires
  (`11:52:07`/`11:57:15`) are this same re-queued event, the first a
  never-started account-limit rotation (refunded, no life spent), this one
  the actual retry.

  **Treated the same way step 4 treats an incident file with a finished
  investigation already on it: verified current, did not re-derive.**
  Independently re-read the live diff before opening the receipt (not
  after, so this wasn't confirmation bias) — `git diff
  origin/main...HEAD --stat` still exactly `RestaurantDetails.tsx` (44
  lines) and `types.ts` (1576 lines, generated), `origin/main` still at
  `f5de339` (no drift), single commit `a2c51af` unchanged — then read the
  receipt and confirmed its threat model, OWASP walk, and secret/dependency
  scan match what the diff actually contains: no new route, `handleSave`'s
  Bearer-token auth path byte-for-byte unchanged, the two new fields ride
  the same already-open `PUT /admin-portal/restaurants/:id` path the six
  sibling toggles already use, zero secrets (the `cw_token`/`api_keys` hits
  in `types.ts` are generated column-name strings, not values), zero new
  dependencies. The one pre-existing gap named (`updateRestaurant`'s
  missing field allow-list) is the design's own already-filed proposal
  (`proposals.md`, 2026-09-03), not reopened here. **Verdict confirmed:
  PASS.** `links.security_review` set to the existing receipt path.

  **1 transition** (`in-security → ready-to-ship`), under the cap of 4.
  Owner `security → devops` per `definition-of-done.md`'s state table
  (devops's release-readiness hop next). Machine WIP unaffected — still
  `1/1`, held by the `ENG-026` family.

  **6b:** not applicable — `links.security_review` follows the same
  already-established receipt-path convention ten prior tickets on this
  board already use; no new instruction introduced.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep.** All open `inbox/` items with a `nudged:` already carry
  their one-ever nudge — no action.
  `inbox/2026-09-07-eng045-merge-request.md` (`notified: 10:57:56`, ~1h
  old) and `PROP-2026-W36` (`notified:` 2026-09-06T18:57:12, ~17h old) are
  both well under the 24h threshold. A `pass` security verdict is not
  itself approver-facing, so no new item raised this pass.

  **8b:** one line filed to `observations.md` — a pass can finish its real
  work (the receipt, written and correct) and still fail before writing
  that back to the ticket/board, which the existing "broken chain" check
  does not catch (the chain *was* fired and *did* run); worth watching as
  its own failure shape rather than folding into "Broken and dropped
  chains", which is about a chain never firing at all. No
  `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  answered this pass, so no decision-journal entry is owed.

  Post-pass `eng-gate-check.sh`, scoped (`ENG-046`) and whole-board: see
  board index for result.

  `chained: ENG-046` — `ready-to-ship` is agent-owned (`devops` next,
  release-readiness hop), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-046`
  before this pass exits.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains
  open, not re-decided here. No project-repo commit this hop — read-only
  verification, no code changed.

- 2026-09-07 `ready-to-ship → blocked` (devops, `continue ENG-046` event
  pass, `skills/release-runner/SKILL.md` run step by step). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (`.env` → `MODE=active`). Pre-pass `eng-gate-check.sh ENG-046`: exit 0,
  clean.

  **Step 1 (window): skipped.** `aiorders-admin-hub` is registered L1
  (`agents/eng-manager/config/projects.md`) — opening a PR is not a
  release, so the window check doesn't apply.

  **Step 2 (upstream gates), all three re-read fresh from the receipt
  files, not from the ticket log's own account:** review
  (`agents/principal-engineer/reviews/ENG-046.md`, pass, 0/10 automatic
  failures), quality (`agents/qa/test-plans/ENG-046.md`, pass, AC2 by
  inspection), security (`agents/security/reviews/ENG-046.md`, pass, zero
  findings). No migration owed — confirmed no `ENG-046-*.md` file under
  `agents/database/migrations/`, correct for a pure frontend diff.

  **Step 3 (readiness gate), no blocking failure:**
  - *Rollback:* no migration, no stored-state change of its own —
    reverting the merge (once merged) fully undoes this diff.
  - *Observability:* read `handleSave` directly rather than assuming —
    already wraps the save in try/catch, logs `console.error`, and shows a
    destructive toast on failure, generic over every field on the
    `restaurant` object including the three new ones. Pre-existing,
    unchanged by this diff.
  - *Cost:* $0/month — no new dependency (`package.json`/lockfile absent
    from the diffstat), no new infrastructure.
  - *Window:* n/a, L1 (step 1).

  **Step 4 (route):** worktree
  (`~/Documents/projects/_eng/aiorders-admin-hub`) re-checked fresh, not
  assumed unchanged since the security hop: `git fetch origin main`, `HEAD`
  at `a2c51af` matching every gate's cited head, `0 1` ahead/behind
  (`git rev-list --left-right --count origin/main...HEAD`), `git diff
  origin/main...HEAD --stat` still exactly `RestaurantDetails.tsx` (44
  lines) and `types.ts` (1576 lines, generated) — no drift. `git ls-tree
  -r origin/main --name-only | grep -i workflow` → `deploy-cf.yml`,
  `on: push: branches: [main]` only, no `pull_request` trigger — opening
  this PR carries no auto-deploy risk. `gh pr list --head
  feat/ENG-046-foodswipe-channel-visibility-admin-toggles --state all`
  confirmed no PR already existed for this branch.

  Opened `aiorders-admin-hub` PR #10
  (https://github.com/harsimranwalia/aiorders-admin-hub/pull/10). Body:
  what changed, what it deliberately doesn't do, the three gate receipts
  with paths, the independent build/lint/typecheck re-run summary, what to
  review hardest (the three rows' field-wiring), and the rollback/CI
  reasoning above.

  Wrote `inbox/2026-09-07-eng046-merge-request.md`, plain `pr_url:` string
  (single repo). `time_estimate: under an hour` carried from the ticket's
  own frontmatter. `lib/eng-notify.sh raise` exited 0; confirmed sent from
  `traces/eng-notify-2026-09-07.log` (`sent: active
  2026-09-07-eng046-merge-request.md`, `12:15:34`); stamped `notified:
  2026-09-07T12:15:34` on the item by hand, copied verbatim from the log.

  State `ready-to-ship → blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, `owner: devops → approver`, `links.pr` set. No G3 — L1
  has none; the PR merge is the human gate. No release record yet — L1's
  actual deploy (merge triggers `deploy-cf.yml`, no manual step needed on
  this repo, unlike `aiorders-api`) and the release record both wait for
  merge detection on a future pass, per the skill's own step 4 L1 row /
  step 7 split.

  **1 transition** (`ready-to-ship → blocked`), well under the cap of 4.

  **Machine WIP / family slot — re-derived fresh, not carried forward from
  this ticket's own prior entries.** Read all three other `ENG-026`
  siblings directly rather than assuming their state from memory:
  `ENG-044` — `shipped` (merged, per its own board-file Log). `ENG-045` —
  `blocked`, `blocked_on: approver`, PR #20 open (`aiorders-api`),
  `depends_on: [ENG-045]`'s own dependent is `ENG-047`. `ENG-047` — `ready`,
  `depends_on: [ENG-045]`, not yet dispatched. Parent `ENG-026` itself:
  `building`.

  With this hop's own transition, **every `ENG-026` child is now either
  shipped or parked on the approver except `ENG-047`** — and `ENG-047`'s
  own dependency is satisfied: `ENG-045`'s PR is open, `blocked_on:
  approver`, which per `eng_build_loop.md` Guards (amended 2026-09-07, "an
  open PR does satisfy `depends_on`") clears it without waiting for
  `verified`. This is exactly the family-container case the same
  amendment's part (b) describes: *"A `building` parent with every child
  parked or `verified` has a free slot, and the pass fills it — the next
  child with a satisfied dependency, else the top of To-do — same pass,
  `continue {NEXT-ID}` before exit."* `ENG-047` is that next child, so this
  hop chains into it directly rather than drawing a fresh ticket from
  To-do or leaving the family idle. (`ENG-047` is cross-repo from `ENG-045`
  — `restaurant-marketplace` vs. `aiorders-api` — so no git-level PR
  stacking applies to it, unlike `ENG-045`/`ENG-046`'s own shared-repo
  case; that's for the pass that actually builds `ENG-047` to work from its
  own ticket Notes, not decided here.)

  **6b:** not applicable — the merge-request item follows this board's own
  established format exactly (`ENG-044`'s, `ENG-045`'s); no new receipt
  path, state name, config key, or cross-file artifact rule was introduced.

  **Dead-end sweep (scoped to this event):** no other ticket's file
  touched — `ENG-044`/`ENG-045`/`ENG-047`/`ENG-026` were read to derive the
  family-slot state above, not written to.

  **Notify sweep (step 7, whole inbox, not just this ticket):** this hop's
  own merge request raised and stamped above. Checked every other open
  `inbox/` item: `ENG-016`'s continue-Piece-2 question, `ENG-018`'s G1,
  `ENG-028`'s rescope G1, and `ENG-042`'s/`ENG-043`'s items all already
  carry their one-ever `nudged:` — no action.
  `inbox/2026-09-07-eng045-merge-request.md` (`notified: 10:57:56`, ~1h15m
  old) is well under the 24h threshold — no action. **`PROP-2026-W36`
  (`notified: 2026-09-06T18:57:12`) had crossed 24h with no `nudged:` and
  no `decision:`** — fired `lib/eng-notify.sh nudge` (confirmed `sent:
  active PROP-2026-W36.md`, `12:12:11` in the log), stamped `nudged:
  2026-09-07T12:12:11` on the item by hand. Exactly its one-ever nudge; it
  now rides the daily brief and weekly report.

  **8b:** one line filed to `observations.md` — `ENG-045`'s own
  merge-request item carries a closing note ("`ENG-047` ... stays `ready`
  until this ticket reaches `verified`") that the same-day Guards amendment
  supersedes; harmless (not re-read as a live instruction) but could
  mislead a human skimming it, not fixed here since editing another
  ticket's already-raised gate item is outside this event's scope. No
  `exception-request:` found. **8c:** n/a — no G1/G2/G3/merge-request
  *answered* this pass (one was raised), so no decision-journal entry is
  owed.

  Post-pass `eng-gate-check.sh`, scoped (`ENG-046`) and whole-board: both
  exit 0, clean.

  `chained: ENG-047` — slot freed by `ENG-046`. `ready-to-ship → blocked`
  moved this ticket off the machine-counted range, and the `ENG-026` family
  slot passes to `ENG-047`, its only remaining child with a satisfied
  dependency and not yet dispatched. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-047`
  before this pass exits (confirmed queued: `traces/eng-loop-2026-09-07.log`
  shows it accepted at `12:15:58` behind this still-in-flight pass, to
  drain once this pass ends — the standard "queued, not launched while the
  lock is held" shape, not a failure). `ENG-046` itself is not
  re-chained — it is parked on the approver (`blocked_on: approver`), which
  step 9 never chains.

  business-os itself left uncommitted through this hop's edits (ticket
  file, `inbox/2026-09-07-eng046-merge-request.md`,
  `inbox/PROP-2026-W36.md`'s `nudged:` stamp, `observations.md`) — same
  standing default every pass on this board has used; the commit-convention
  question remains open, not re-decided here. The project-repo commit
  (`a2c51af`) was already made and pushed in the build hop, before this
  pass began; this hop only opened the PR on top of it, no new commit.

- `2026-09-07` `blocked → shipped` (control center, merge detected) — `feat/ENG-046-foodswipe-channel-visibility-admin-toggles` is an ancestor of `origin/main`. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree.
- `2026-09-07` `shipped → verified` — this dashboard flip never fired `continue ENG-046`, so `acceptance-check/SKILL.md` never ran on this ticket individually (unlike every sibling family's children — see `proposals.md`'s 2026-09-07 dashboard-bypass row, addendum (4)). Closed as part of `ENG-026`'s own parent-level closing pass instead: this ticket's own AC slice (PRD AC2 — staff can view and set all three flags from `aiorders-admin-hub`) walked directly against `RestaurantDetails.tsx` on `origin/main` (three `Switch` rows wired to state, `handleSave` posting the whole object through the existing `PUT` path) and the merge's own Cloudflare Pages deploy run (`success`, `2026-09-07T20:25:28Z`). Pass. Full walk: `agents/product-manager/notebook/2026-09-07-eng026-acceptance.md`. `owner` stays `eng-manager`.
