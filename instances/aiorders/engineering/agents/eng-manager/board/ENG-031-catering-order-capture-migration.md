---
id: ENG-031
title: Add order-capture columns to catering — action_type + selections (migration)
project: aiorders-api
type: feature
size: S
time_estimate: ~1-2h
time_spent: ~1h build plus review/QA/security/release-readiness gate hops
  (all pass this pass), not itemized against a pass-start clock
time_remaining: none — merged and verified; already inside the original
  ~1-2h/S band
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
branch: feat/ENG-031-catering-order-capture-migration
depends_on: []
blocks: [ENG-032, ENG-033]
parent: ENG-016
links:
  prd: agents/product-manager/specs/ENG-016-catering-quote-generator.md
  design: agents/architect/designs/ENG-016-catering-quote-generator.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-031.md
  test_plan: agents/qa/test-plans/ENG-031.md
  security_review: agents/security/reviews/ENG-031.md
  release: agents/devops/releases/2026-09-03-aiorders-api-ENG-031.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/12
---

## Problem

`public.catering` has no columns to store what a customer actually selected,
or how they reached the request (a priced quote attempt vs. a plain
"contact me"). Piece 1 (ENG-016) needs somewhere to persist both before
either the backend endpoint or either frontend can do anything with them.

## Outcome

Two new nullable columns exist on `public.catering`:

- `action_type text` — `QUOTE_SUBMITTED` | `MANUAL_CONTACT_REQUESTED` | null.
- `selections jsonb` — array of `{category, item_id, name, quantity, note}`,
  null unless `action_type = QUOTE_SUBMITTED`.

No default, no `NOT NULL`, no `CHECK`, no enum type, no index. `add column if
not exists`, matching `20260807000001_add_heard_about_us_to_catering.sql` —
the only prior additive migration against this table, and this ticket's
template. Column comments on both, documenting `selections`' element shape,
the way `20260807000002_add_catering_to_restaurant_website.sql` documents its
own jsonb shape.

## Notes

Design's `## Data` section has the full column spec, the `selections`
element shape, and why validation lives in the edge function rather than the
database (a malformed third-party payload must never fail a public lead
form's insert). This is step 1 of the design's own Rollout order — inert
until `ENG-033` (backend) starts writing to it. Both `ENG-032` and `ENG-033`
`depends_on` this ticket; full sequencing rationale in
`agents/eng-manager/notebook/2026-09-03-eng016-work-breakdown.md`.

## Log

- `2026-09-03` `(created) → building` (eng-manager, `work-breakdown`,
  `continue ENG-016` event pass) — sub-ticket of `ENG-016`, sequence 1 of 4,
  no dependency, so dispatched straight to `building`. `time_estimate`
  ~1-2h, 0h spent. Machine WIP: this ticket is part of `ENG-016`'s own
  family, not a second occupant of the 1/1 slot — reasoning in the notebook
  above. `chained: ENG-031` — fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-031`
  before this pass exits.

- `2026-09-03` `building → in-review` (database/principal-engineer-adjacent,
  `continue` event pass, context `ENG-031`). Narrow scope per this event's
  own contract (resume this ticket from its current state only). Reading
  map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
  9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check
  clean (repo-root `.env` -> `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-031`): exit
  0, clean.

  **Worktree found mid-build, not started fresh.** `~/Documents/projects/_eng/aiorders-api`
  was on branch `feat/ENG-016-catering-quote-generator` with two uncommitted
  files: this ticket's own migration
  (`supabase/migrations/20260903130000_add_order_capture_to_catering.sql`,
  complete) and a pre-existing untracked `supabase/functions/brand-portal/deno.lock`
  (timestamped ~7.5h before the migration file - unrelated to this ticket,
  already independently noticed and left alone by `ENG-029`'s design pass
  the same day). Per `config/projects.md`'s own guard ("uncommitted changes
  at the start of a pass means a previous pass died mid-work - stop and
  flag it, never discard, never stash blindly"): investigated rather than
  either trusted blindly or discarded. The migration file's content was
  verified line-by-line against the design's `## Data` section and both
  cited template migrations (`20260807000001_add_heard_about_us_to_catering.sql`,
  `20260807000002_add_catering_to_restaurant_website.sql`) - exact match,
  no defects found. Confirmed via `git log origin/main..HEAD` that zero
  commits existed on the branch (the file was purely an uncommitted
  working-tree artifact) and via `agents/database/migrations/` that no
  `ENG-031-*.md` plan doc existed yet. Conclusion: the prior `continue
  ENG-031` pass this ticket's own `chained:` line fired did the real build
  work and died before committing or updating this log - recovered and
  completed here rather than re-derived from scratch or discarded.

  **Branch name did not match convention** (`engineering-standards.md` ->
  `Branch: {type}/{ENG-NNN}-{slug}`) - it was named after the parent
  (`ENG-016`) rather than this ticket. No evidence anywhere (this ticket,
  the design, or `2026-09-03-eng016-work-breakdown.md`) that a shared
  parent-family branch was a deliberate call - and one wouldn't make sense
  here regardless, since `ENG-033` `depends_on: [ENG-031]` read as *shipped*
  per the work-breakdown notebook, meaning `ENG-031` must merge to `main`
  before `ENG-033` even starts building. Read as a naming slip by the pass
  that died, not a decision to preserve. Safe to fix: `git log
  origin/main..HEAD` confirmed zero commits on the branch, so `git branch -m`
  to `feat/ENG-031-catering-order-capture-migration` cost nothing and lost
  no history. Filed as an observation (below) rather than silently corrected
  with no record.

  **Self-tested, per this state's own exit condition:** no live Postgres or
  Supabase MCP connection available this session (no MCP server of that
  name configured - confirmed via `ListMcpResourcesTool` and a `ToolSearch`
  for a Supabase/Postgres tool, both empty - a strictly worse position than
  `ENG-007`/`ENG-011`/`ENG-013`'s passes, which had the MCP fallback).
  Repo-level checks performed instead: grep confirmed no prior migration
  already defines `action_type`/`selections` on `public.catering` (no
  collision); grep confirmed nothing in `supabase/functions/` references
  either column yet (matches the design's "inert until `ENG-033`" claim);
  timestamp ordering confirmed against the latest on-disk migration. Full
  detail and the gate verdict:
  `agents/database/migrations/ENG-031-catering-order-capture-migration.md`
  (written this pass).

  **Artifact enumeration (step 6b):** `grep -rn "action_type\|selections"`
  and `grep -rln "ENG-031"` across both department and instance roots.
  Every hit for the two column names agrees on shape and semantics
  (`ENG-016`'s design, `ENG-032`, `ENG-033`, `ENG-034`, two superseded
  `inbox/_handled/` G1 drafts) - no instruction or map in conflict. `ENG-031`
  mentions in `ENG-029`/`ENG-030`'s own logs are machine-WIP-family status
  references, not conflicting claims about this ticket.

  **PR body written** (`building`'s own exit condition; no PR opened yet -
  L1 autonomy opens the PR at release-readiness per
  `skills/release-runner/SKILL.md` step 4, not at `building`):
  - *What it does:* Adds two nullable columns to `public.catering` -
    `action_type text` and `selections jsonb` - via `add column if not
    exists`, with a column comment on each documenting purpose and, for
    `selections`, the element shape.
  - *What it deliberately does not do:* No default, no `NOT NULL`, no
    `CHECK`, no enum type, no index, no backfill. Doesn't touch
    `catering-request` or any frontend - this ticket is schema-only.
  - *Uncertainties:* The statement has not executed against any live or
    staging Postgres (no CLI, no MCP this session) - see Self-tested above.
    Low risk: two nullable `ADD COLUMN` statements with no default is close
    to the smallest possible schema change.
  - *What to review hardest:* Nothing structurally risky here - the
    honest review target is whether the column comments' documented
    `selections` shape stays byte-for-byte consistent with what `ENG-033`
    actually implements, since the comment is this table's only schema
    documentation.

  Branch committed (`06e8e84`, 1 file) and pushed:
  `origin/feat/ENG-031-catering-order-capture-migration`.

  **1 transition this pass** (`building → in-review`), under the cap of 4 -
  `in-review`/`in-qa` (combined hop, principal-engineer + qa) is a fresh
  session's work per `eng_build_loop.md`'s "a pass stops after `building` on
  purpose." No WIP-cap change: this ticket was already inside the counted
  `ready`..`ready-to-ship` range at `building`; `in-review` is still inside
  it.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise - `in-review` needs no approver gate.
  Nothing to nudge.

  **Observations filed:** (1) the wrongly-named branch this pass found and
  fixed - worth a look if a second parent/child decomposition ever produces
  the same slip, since this is the first ticket-family this board has run
  through `building`. (2) the stray `supabase/functions/brand-portal/deno.lock`,
  still sitting untracked in the `aiorders-api` worktree, now independently
  noticed by two passes (`ENG-029`'s and this one) without being cleaned up
  or explained - worth someone's attention before a third pass has to
  re-derive the same "not mine, leave it" conclusion.

  `chained: ENG-031` - `in-review` is agent-owned (principal-engineer +
  qa combined hop next), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-031`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-031`) and
  whole-board: see board index for result.

- `2026-09-03` `in-review → in-qa` (principal-engineer + qa, combined hop,
  `continue ENG-031` event pass). Found `reviews/ENG-031.md` already
  written by a prior pass - uncommitted, untraced in this log - verified
  fresh against the design; matches, accepted rather than redone.
  **Review: pass** (0/10 automatic failures, no design divergence).
  **QA: pass** (no suite applies, no `.ts` in this diff; 0 of `ENG-016`'s
  13 ACs apply to this diff; this ticket's own criterion - schema matches
  design - verified by inspection; 0 open P0/P1).
  Receipts: `agents/principal-engineer/reviews/ENG-031.md`,
  `agents/qa/test-plans/ENG-031.md`; `links.review`/`links.test_plan` set.
  No WIP/cap change - still inside the counted `ready..ready-to-ship`
  range.
  Reasoning: `agents/principal-engineer/notebook/2026-09-03-review-log.md`,
  `agents/qa/notebook/2026-09-03-coverage-gaps.md`.
  Proposal filed (`proposals.md`): `aiorders-api` has no registered test
  harness.
  `chained: ENG-031` - `in-qa` is agent-owned (security next), not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-031`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-031`) and
  whole-board: see board index for result.

- `2026-09-03` `in-qa → ready-to-ship` (security, `continue ENG-031` event
  pass). `skills/security-gate/SKILL.md` run in full against the one-file
  diff (`06e8e84`, 26 lines, pure DDL, no reachable code path yet - grep
  of `supabase/functions/` for both column names re-confirmed zero hits,
  not taken on trust from QA's/review's own accounts).
  **Verdict: PASS**, 0 blocking findings. One non-blocking finding: RLS
  activation on `public.catering` unverified from the repo - 2nd
  occurrence today (1st: `ENG-015`, `public.restaurants`); pre-existing,
  not worsened by this diff, not fixable blind, routed to `ENG-033`'s own
  future gate rather than filed as a proposal. Reasoning and finding in
  full: `agents/security/notebook/2026-09-03-findings.md`.
  Receipt: `agents/security/reviews/ENG-031.md`; `links.security_review`
  set in the same edit. No WIP/cap change - still inside the counted
  `ready..ready-to-ship` range.
  Observation filed (`observations.md`): this hop and the prior one both
  logged an `eng-trigger.sh` chain command whose relative path does not
  resolve from the instance cwd; fired the absolute path instead, per
  this event's own instructions.
  `chained: ENG-031` - `ready-to-ship` is agent-owned (devops's
  release-readiness hop next), not the approver, not blocked, not
  terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-031` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-031`) and
  whole-board: see board index for result.

- `2026-09-03` `ready-to-ship → blocked` (devops, `continue ENG-031` event
  pass). `skills/release-runner/SKILL.md`: L1 skips the window check; all
  four upstream gates re-confirmed **pass** (review, QA, security,
  migration — receipts already linked). Readiness gate held: rollback
  written not live-drilled (standing host gap, same bar `ENG-007` cleared),
  no reachable runtime path yet to observe (inert until `ENG-033`), $0/month
  cost. Opened `aiorders-api` PR #12, wrote
  `inbox/2026-09-03-eng031-merge-request.md`, notified (stamped by hand —
  script gave no delivery confirmation). Full reasoning:
  `agents/devops/notebook/2026-09-03-release-readiness-log.md`.
  `blocked_on: approver`, `blocked_from: ready-to-ship`, `owner: approver`,
  `links.pr` set. Approver-facing WIP uncapped; machine WIP unaffected —
  `blocked` leaves the counted range. Observation filed (stray
  `deno.lock`, third notice).
  `chained: none` — blocked on the approver; merge detection (step 5)
  resumes it on a future pass.

- `2026-09-03` `blocked → shipped → verified` (eng-manager, `scheduled`
  event pass — whole-board sweep, step 5 merge detection, exactly the
  resume this ticket's own prior entry predicted). Local git only, per
  `eng_build_loop.md` step 5 — no `gh` call made. `aiorders-api` worktree:
  `git fetch origin main` (`origin/main@3cf5607`, fresh), then `git fetch
  origin pull/12/head` and `git merge-base --is-ancestor` against
  `origin/main`: **YES ancestor** — PR #12 merged (`3cf5607`, 2026-09-03
  18:51:41 -0700 / 2026-09-04T01:51:41Z), head `06e8e84` matching this
  ticket's own `ready-to-ship → blocked` log entry exactly, no drift.
  `decision:` on `inbox/2026-09-03-eng031-merge-request.md` stayed blank —
  merged directly on GitHub, same shape `ENG-007`'s and `ENG-011`'s own
  releases already established for this approver.

  **Not advanced past a state that owes gates:** re-read all four upstream
  receipts directly (`agents/principal-engineer/reviews/ENG-031.md`,
  `agents/qa/test-plans/ENG-031.md`, `agents/security/reviews/ENG-031.md`,
  `agents/database/migrations/ENG-031-catering-order-capture-migration.md`)
  — all four `pass` (security's one non-blocking RLS finding already routed
  to `ENG-033`, not re-litigated here). Release record written:
  `agents/devops/releases/2026-09-03-aiorders-api-ENG-031.md`, `links.release`
  set in the same edit. `state: blocked → verified`, `owner: approver →
  eng-manager`, `blocked_on`/`blocked_from` cleared.

  Merge-request item moved to `inbox/_handled/`. Journal entry added
  (`decision-journal.md`) — silent GitHub merge, no written reply, same
  shape as `ENG-007`'s and `ENG-011`'s own rows.

  **Consequence for the family:** this ticket's `blocks: [ENG-032, ENG-033]`
  — `ENG-032`'s sole dependency (`depends_on: [ENG-031]`) is now satisfied.
  `ENG-033` still also depends on `ENG-032` (`depends_on: [ENG-031,
  ENG-032]`), unaffected by this merge alone. See `ENG-032`'s own log for
  this pass's dispatch note. Machine WIP unaffected by this ticket's own
  shipping — it already left the counted `ready..ready-to-ship` range at its
  prior `ready-to-ship → blocked` hop; the family's slot is held by
  `ENG-032`/`ENG-033`/`ENG-034` regardless. Per `ADR-003`, the parent
  (`ENG-016`) still cannot reach `shipped`/`verified` until every child is
  settled — three siblings remain unbuilt.

  **2 transitions** (`blocked → shipped`, `shipped → verified`), well under
  the cap of 4 — pure receipt-confirmation and bookkeeping, no new
  implementation work, same precedent `ENG-007`'s and this same pass's own
  `ENG-024` discovery already set.

  `chained: none` — `verified` is terminal; the chaining guard never fires
  on a terminal ticket.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.
