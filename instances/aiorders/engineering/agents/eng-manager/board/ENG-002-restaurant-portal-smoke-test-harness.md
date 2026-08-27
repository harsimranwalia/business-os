---
id: ENG-002
title: Add a smoke-test harness to restaurant-portal
project: restaurant-portal
type: chore
size: M
severity: P2
priority:
state: verified
owner: product-manager
lane: full
blocked_on: 
blocked_from: 
source: approver
created: 2026-08-25
updated: 2026-08-26
branch: chore/ENG-002-smoke-test-harness
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-002-restaurant-portal-smoke-test-harness.md
  design: agents/architect/designs/ENG-002-restaurant-portal-smoke-test-harness.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-002.md
  test_plan: agents/qa/test-plans/ENG-002.md
  security_review: agents/security/reviews/ENG-002.md
  release: agents/devops/releases/2026-08-26-restaurant-portal-ENG-002.md
  pr: https://github.com/harsimranwalia/restaurant-portal/pull/1
---

## Input

Verbatim, from `inbox/requests/2026-08-23-test-harness.md` (now
`inbox/_handled/`), filed by the approver, received 2026-08-23 — preserved
here per `skills/request-readback/SKILL.md` step 1, never edited:

> No registered AIOrders project has a single test. Verified 2026-08-23: none
> of the four `package.json` files defines a `test` script, `aiorders-api`
> has no `package.json` at all, and a filesystem sweep finds zero
> `*.test.*` or `*.spec.*` files outside `node_modules` anywhere in the five
> repos.
>
> That makes the quality gate unenforceable rather than merely weak. The
> `full` lane requires a QA test-plan receipt and
> `skills/test-suite-run/SKILL.md` needs something to execute; with no
> suite, the receipt exists and proves nothing — the exact failure
> `skills/code-review-gate/SKILL.md` names in its own receipt table, where a
> receipt written on a fail satisfies the check it was meant to prove.
>
> Verido-CRM was in this position and it was solved the same way, for the
> same stated reason: ENG-002 built a smoke test harness because the app had
> no CI to prove a change had not broken a route.
>
> **What this asks for:** Shape and scope this. The department decides the
> shape — this is a problem statement, not a design. Start with one repo,
> not five — `restaurant-portal` has a clean working tree and already
> builds. `aiorders-api` is the highest blast radius and the hardest case —
> it probably deserves its own ticket rather than being folded into a
> frontend harness.

Full text, including the "why it's worth building" close, in the handled
request file.

## Readback

See `agents/product-manager/specs/ENG-002-restaurant-portal-smoke-test-harness.md`
→ Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

None of the five registered AIOrders repos has a single test. That makes the
`full` lane's quality gate structurally unable to prove anything: a receipt
file is enough to satisfy `lib/eng-gate-check.sh`, and
`skills/test-suite-run/SKILL.md` writes an honest "no suite" result that
still produces a non-empty receipt. Filed by the approver
(`inbox/requests/2026-08-23-test-harness.md`) after verifying no
`package.json` defines a `test` script and no `*.test.*`/`*.spec.*` file
exists anywhere in the five repos.

## Outcome

`restaurant-portal` has a real test command and at least one test that fails
on a broken build or a route that stops rendering. The registry's Commands
table names the real command. `test-suite-run` executes it and produces a
real result instead of the "no suite" branch.

## Notes

Scoped to one repo deliberately — see the PRD's Non-goals. `aiorders-api`
(Deno, no `package.json`, highest blast radius) and the other three
frontends are out of scope; `aiorders-api` will likely need its own ticket
but that isn't committed here.

This ticket is also what satisfies AC4 of `ENG-001` (the seed ticket needs
one real ticket to reach `shaped`) — see that ticket's log.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-25` `intake → shaped → awaiting-scope` (product-manager) — shaped
  from `inbox/requests/2026-08-23-test-harness.md` (filed by the approver,
  received 2026-08-23, unprocessed for two days — this pass's PM work, not a
  self-originated finding). Ran the full request-readback
  (`skills/request-readback/SKILL.md`): this PM's reading plus a blind
  architect reading, no material divergence — see the PRD's Readback
  section. `size: M` chore, so **G1 is required** per
  `agents/eng-manager/config/definition-of-done.md` → Size table (only `S`
  bug/chore auto-skips; `prd-writer/SKILL.md`'s coarser "bug/chore skips G1"
  reading was not used here — flagged as a doc inconsistency, not resolved
  in this pass). PRD written at
  `agents/product-manager/specs/ENG-002-restaurant-portal-smoke-test-harness.md`.
  No `## Dissent` — `agents/critic/agent.md` doesn't exist on this instance
  or the department template; filed as a proposal instead of worked around.
  G1 item written to `inbox/2026-08-25-eng002-g1-scope.md` and notified.
- `2026-08-25` `awaiting-scope → designed → ready` (eng-manager, `scheduled
  manual-unblock` pass) — G1 **approved** by the approver, 2026-08-25T21:43:57Z,
  no additional comment. Gate item moved to `inbox/_handled/`; PRD `status:
  approved`; journaled in `agents/eng-manager/config/decision-journal.md`.
  **Designed:** architect design written at
  `agents/architect/designs/ENG-002-restaurant-portal-smoke-test-harness.md` —
  Vitest + React Testing Library (reuses the project's own `vite.config.ts`,
  no second transform config), one smoke test rendering the real app entry
  point with its actual provider tree, asserting a known landmark renders.
  Playwright and Jest considered and rejected — see design's Alternatives.
  No one-way door (a test-runner choice is reversible); no ADR, no G2. **Ready:**
  work is a single unit (one repo, one test file, one config change) — no
  further breakdown needed; `machine_wip` (6) had 0/6 in flight, well within
  cap. **Not proceeding into `building` this pass, deliberately** — this pass
  is a `scheduled manual-unblock` sweep recovering from an earlier timeout
  (see this ticket's board-index entry), not a fresh, dedicated context, and
  `schedules/eng_build_loop.md` names `building` as the pass's own stopping
  point precisely because writing the actual code deserves a clean session
  ("an engineer writing code is the pass's real unit of work"). `chained:
  ENG-002` — sitting at `ready`, owned by eng-manager (agent, not approver,
  not blocked, not terminal) — firing `continue` for a dedicated building hop.
- `2026-08-26` `ready` (no state change — eng-manager, `decision` event,
  attempt 2/2 of the 2026-08-25T15:30:09Z attempt that failed mid-pass — the
  org hit its monthly Claude spend limit 236s in, per
  `traces/eng-loop-2026-08-25.log`; the event was re-queued rather than
  consumed) — re-checked `inbox/_handled/2026-08-25-eng002-g1-scope.md`: the
  G1 decision this event exists to act on was already fully processed by the
  intervening `scheduled (manual-unblock)` retry pass logged directly above,
  which reached the same answered gate item through its own step-4 inbox
  sweep before this event's retry got a turn. All four receipts independently
  verified rather than trusted: gate item in `inbox/_handled/`, ticket at
  `ready`, PRD `status: approved`, decision journaled in
  `agents/eng-manager/config/decision-journal.md`. Nothing left to act on;
  redid none of it. `chained: none` — `continue ENG-002` is already the front
  line of `traces/.pending` from that earlier pass, and this pass's own
  parent `eng-trigger.sh scheduled launchd` invocation (pid 37779) currently
  holds `traces/.loop.lock`, so firing `eng-trigger.sh continue ENG-002`
  again here would both duplicate a queued line and contend a lock its own
  ancestor holds. The next fire drains it.
- `2026-08-26` `ready → building` (eng-manager, `scheduled` sweep) — a
  dedicated `continue ENG-002` build hop ran this morning
  (`traces/eng-loop-2026-08-26.log`, 09:36–09:56, 1195s, under the same
  launchd-fired `eng-trigger.sh scheduled launchd` lock as this pass) and
  implemented the smoke test per the architect's design: Vitest + React
  Testing Library wiring in `package.json`/`vite.config.ts`,
  `src/test/setup.ts` (jsdom shims for `matchMedia`/`ResizeObserver`/
  `IntersectionObserver`), and `src/App.test.tsx` rendering the real
  `<App/>` and asserting a signed-out visitor lands on Login. Per its own
  account: verified red by mutating the `/login` route out of `App.tsx` and
  confirming the suite failed, then reverted (byte-identical); confirmed
  zero new lint errors (96 before/after) and zero new `npm audit` findings
  from the added dependencies. Also found `restaurant-portal/.env` tracked
  and un-gitignored (same class as `ENG-003`) and was mid-way through filing
  it as a proposal.

  **That pass then stopped itself, uncommitted, citing what it believed was
  a second concurrent instance of this automation touching the same
  ticket** — `EPERM` errors on the board file and the worktree, and a live
  `eng-trigger.sh scheduled launchd` process (pid 37779) plus a `claude`
  child (pid 48189) found via `ps`. It asked the approver, inline in its own
  session only (no inbox item, no durable record), whether to wait or
  intervene, then exited 0 having committed and pushed nothing.

  **Independently re-verified this pass, before touching anything:** pid
  37779 is this exact chain's own launchd-fired orchestrator, still holding
  `traces/.loop.lock` throughout — it drained `continue ENG-002` at ~09:36,
  ran it to completion at 09:56:41 (exit 0), and immediately drained the
  next queued event (this `scheduled` pass) at 09:56:42. `ps` right now
  shows no other `claude`/`eng-trigger`/`run-claude`/`run-stream` process
  touching this instance or the `restaurant-portal` worktree — the four
  other long-running `claude` processes on this machine are unrelated
  interactive sessions from Monday, none scoped to this repo. The worktree
  (`~/Documents/projects/_eng/restaurant-portal`) matches the stopped
  pass's own description exactly: branch `chore/ENG-002-smoke-test-harness`,
  modified `package.json`/`package-lock.json`/`vite.config.ts`, untracked
  `src/App.test.tsx` and `src/test/`; `package.json` really does carry
  `"test": "vitest run"` and both new test files are on disk. **Conclusion:
  no real collision — the stopped pass almost certainly mistook its own
  parent/orchestrator process (or a transient TCC/EPERM permission blip, the
  documented recurring macOS failure class named in
  `schedules/eng_build_loop.md`) for a competing instance.**

  Per `config/projects.md` → "Working copies" ("uncommitted changes in the
  worktree at the start of a pass means a previous pass died mid-work. Stop
  and flag it. Never discard, never stash blindly"), left the worktree
  exactly as found rather than touching it. Filed the `.env` finding the
  stopped pass didn't get to (`agents/eng-manager/proposals.md`).

  Set `state: building` and `branch: chore/ENG-002-smoke-test-harness` to
  match reality — the prior pass did real, verified implementation work and
  simply never updated the board before stopping. **Not finishing the
  build (commit, push, PR) in this pass, deliberately** — that's
  implementation follow-through work this department consistently reserves
  for a dedicated `continue` session (same reasoning applied to
  `ENG-001`/`ENG-002`'s own `ready`→`building` transitions earlier), not a
  broad board sweep. `chained: ENG-002` — fired `/bin/zsh eng-trigger.sh
  continue ENG-002` (queued; this pass's own lock is held by its ancestor,
  so the fire appends to `traces/.pending` and exits rather than launching
  immediately — the next drain runs it).
- `2026-08-26` `building → in-review → in-security → ready-to-ship → blocked`
  (eng-manager, dedicated `continue ENG-002` pass — this session) — the
  session `schedules/eng_build_loop.md`'s Cadence section describes as
  reserved for finishing a build; confirmed via `traces/.pending`/lock state
  and the trigger log that this pass is exactly the queued continuation the
  two passes above deferred to, not a duplicate. Pre-pass `lib/eng-gate-check.sh`
  (whole board and `ENG-002` scoped): exit 0, clean.

  **Finished `building`.** Did not take the prior pass's self-tested claim on
  faith — re-verified independently before committing: read the actual diff
  against `agents/architect/designs/ENG-002-*.md` (matches exactly, no
  deviation); traced `src/App.test.tsx`'s Supabase mock through
  `src/context/auth/supabaseAuth.ts` and `AuthContext.tsx` to confirm it
  mocks the real boundary the code actually calls; traced the "Login" tab
  landmark to `src/pages/Login.tsx`'s literal `TabsTrigger` text. Ran
  `npm test` myself: 1 passed, 0 failed, 0 skipped. Ran `npm run lint` on
  this branch and, separately, on a clean `origin/main` checkout
  (`git stash -u`): 96 problems (62 errors/34 warnings) on both — zero new,
  independently confirmed rather than trusting the prior pass's count. Ran
  `npm run build`: succeeds. Ran `npm audit` both branches: 37 total (this
  branch) vs. 39 (`main`) — no new vulnerabilities; two pre-existing highs
  incidentally resolved by the lockfile re-resolution. Committed exactly the
  five relevant files (`package.json`, `package-lock.json`, `vite.config.ts`,
  `src/App.test.tsx`, `src/test/setup.ts` — staged by name, not `-A`, since
  the repo also carries the unrelated already-proposed tracked-`.env`
  finding) as `2703add`, pushed `chore/ENG-002-smoke-test-harness` to
  `origin`.

  **`in-review` (code review + quality gate, combined hop).** Acted as
  principal-engineer: automatic-failure scan clean (0/10 hit), diff-shape and
  line-level review clean, test-quality check confirmed the assertion is
  real rather than tautological. Verdict **pass** — receipt written to
  `agents/principal-engineer/reviews/ENG-002.md`, `links.review` set.
  Acted as qa: wrote the test plan this ticket never had
  (`agents/qa/test-plans/ENG-002.md`, one row per PRD acceptance criterion —
  AC1/AC2/AC4 map to the actual test and pass, AC3 is a `ready-to-ship`
  registry edit, not a test) and ran the suite for the record. Verdict
  **pass**, `links.test_plan` set. Per `skills/code-review-gate/SKILL.md`
  step 9, a review+quality pass on this combined hop advances straight to
  `in-security` — `in-qa` is not a separate sit-state when both clear
  together.

  **`in-security`.** Acted as security: threat-modelled the diff (no new
  input, capability, data exposure, or production blast radius — dev-only
  tooling, confirmed the built `dist/` bundle is unchanged in shape). Walked
  OWASP A01–A10 per `security-baseline.md`: nine `n/a` with reasons, A06
  (Vulnerable Components) checked directly against the `npm audit` numbers
  above. Secret-scanned the diff and the new commit: none. SOC 2 evidence
  trail (ticket → PRD → design → review → test plan → this verdict)
  confirmed complete. Verdict **pass** — receipt at
  `agents/security/reviews/ENG-002.md`, `links.security_review` set.

  **`ready-to-ship`.** Acted as devops: all three upstream gates verified
  present and non-empty on disk (not assumed from the frontmatter — read
  each file). No migration (`touches_data: false`). Readiness: rollback is
  "revert the branch," nothing deployed to roll back from a dev-only
  dependency; observability is `test-suite-run` itself, which now has a real
  command to execute on every future `restaurant-portal` ticket instead of
  the vacuous "no suite" branch; cost $0/month per the PRD, no cost notice
  owed. Window check: 2026-08-26 is a Wednesday, ~11:00am local, `MODE=active`
  — no freeze. Updated `config/projects.md`'s Commands table (`restaurant-portal`
  Test cell: `npm run test`) per the design's own Components table, which
  assigns this specific edit to this specific hop. **Autonomy is L1** —
  opened the real PR (`gh pr create`, title "Add Vitest smoke-test harness"):
  https://github.com/harsimranwalia/restaurant-portal/pull/1. Wrote the L1
  merge-request item (`inbox/2026-08-26-eng002-merge-request.md`, `gate:
  merge` — matching the literal value `lib/eng-notify.sh`'s case statement
  checks for, not the config key `merge_request`) carrying the PR link and
  the three gate verdicts, and raised it (`lib/eng-notify.sh raise`, sent
  per `traces/eng-notify-2026-08-26.log`, `notified: 2026-08-26T11:01:46`
  stamped by hand since the script itself never writes back to the item —
  confirmed by reading it rather than assumed). State → `blocked`,
  `blocked_on: approver`, `blocked_from: ready-to-ship`, owner `approver` —
  the same design `config.yaml`'s `gates.merge_request` describes, and the
  one L1 releases have used since 2026-07-27 specifically so a PR awaiting
  merge counts against the approval cap instead of sitting invisible.

  **Approval-cap check before this transition, since the board was already
  at 2/3 with the approver-facing WIP guard also at 2/2 (full).** Read both
  guards' actual definitions in `config/config.yaml` (`wip.approver_limit`,
  `wip.awaiting_approver_cap`) rather than trusting the board header's
  prose alone: `approver_limit`'s own stated consequence is "nothing NEW
  starts," and `awaiting_approver_cap` (3, the guard `config.yaml` names
  explicitly as covering "an L1 PR waiting to be merged") was at 2/3 with
  one slot free. `ENG-002` is an already-in-flight, already-G1-approved
  ticket reaching its own next gate, not a new start — advancing it to
  `blocked` brings `awaiting_approver_cap` to exactly 3/3 (at the cap, not
  over it) and leaves `approver_limit`'s "new starts" rule untouched, since
  nothing new started. Proceeded on that basis.

  **4 transitions this pass** (`building→in-review`, `in-review→in-security`,
  `in-security→ready-to-ship`, `ready-to-ship→blocked`) — exactly the
  per-ticket cap, and it lands exactly on the human gate, which is the
  designed stopping point anyway.

  This pass's own `lib/eng-notify.sh raise` call (above) reproduced the
  `MODE`-variable-collision bug (`sent: active`, not `sent: raise`, in
  `traces/eng-notify-2026-08-26.log`) already filed as an open proposal
  2026-08-25 (`proposals.md`, row 2) — same symptom the ENG-003 raise hit
  first. No new proposal written; this is corroborating evidence for an
  existing one, not a fresh finding. Confirmed manually stamping `notified:`
  on the merge-request item was still necessary regardless of the bug, since
  the script never writes back to the item file either way.

  Post-pass `lib/eng-gate-check.sh`: exit 0, clean. `chained: none` —
  `blocked`, `blocked_on: approver`. This is the human gate the whole hop
  was driving toward; firing `continue ENG-002` again would just re-queue
  against a ticket with nothing left for a machine to do until the approver
  merges or replies.

- `2026-08-26` `blocked → shipped` (control center, merge detected) — recorded on Harry's say-so; ancestry not consulted. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree. The release record and `verified` still belong to a pass — this marks the merge, not the verification.
- `2026-08-26` `shipped → verified` (eng-manager acting as devops then
  product-manager — `scheduled` safety-net pass) — this is the pass the line
  directly above was waiting for. Did not take the control center's `shipped`
  write on faith: independently ran the loop's own merge-detection check
  (`schedules/eng_build_loop.md` step 5) from scratch before doing anything
  else. `git fetch origin` in the department's own worktree
  (`~/Documents/projects/_eng/restaurant-portal`, never the human's checkout)
  showed `33c5de6..b3a81ef main -> origin/main`;
  `git merge-base --is-ancestor chore/ENG-002-smoke-test-harness origin/main`
  confirmed the branch head is an ancestor; `git log origin/main --oneline`
  showed `b3a81ef` (the merge) directly on top of `2703add` (this ticket's
  commit) on top of `33c5de6` (`main`'s pre-PR tip) — no intervening commits,
  so `git diff` between the worktree's checked-out branch tip and
  `origin/main` is empty. The control center's claim checks out; the merge is
  real.

  **Acted as devops, closing out `shipped`'s exit condition** (`config/definition-of-done.md`:
  "Deployed, health checks green, release record written") **which the
  control center's direct edit skipped.** `restaurant-portal` has no
  push-to-`main` CI/CD (`.github/workflows/` absent; `deploy-cf` is a manual
  `wrangler pages deploy` script, confirmed by reading both, not assumed) and
  this ticket's entire diff is `devDependency` + test files that Vite's build
  graph never reaches from the app entry point — re-verified by running
  `npm run build` against the actual merged tree (worktree tree-identical to
  `origin/main`, confirmed above) and reading the output: same three
  artifacts (`index.html`, one CSS bundle, one JS bundle) as any other build.
  So there is no new production artifact this release needs to deploy, and
  `npm run deploy-cf` was deliberately not run — unlike `ENG-001`'s
  no-deploy-ever shape (`ADR-001`/`ADR-002`), this is an ordinary ticket that
  simply has nothing to deploy *this time*, not a ticket type exempted from
  deploying. Re-ran `npm test` on the merged tree independently rather than
  trusting the pre-merge numbers: 1 passed, 0 failed, 0 skipped. Wrote the
  release record from what was actually found, not copied from any plan:
  `agents/devops/releases/2026-08-26-restaurant-portal-ENG-002.md`,
  `links.release` set.

  **Acted as product-manager, confirming all four acceptance criteria against
  the live (merged) thing** (`agents/qa/test-plans/ENG-002.md`): AC1/AC2/AC4
  re-confirmed by the fresh `npm test` run above; AC3 (`config/projects.md`'s
  Commands table names `npm run test`) read directly off disk and confirmed
  present — updated the test plan's AC3 row from `pending` to `pass`, since
  the registry edit that made it true was completed at this ticket's own
  `ready-to-ship` hop and simply hadn't been re-checked against the live file
  until now. All four criteria hold.

  **The gate item this ticket was blocked on
  (`inbox/2026-08-26-eng002-merge-request.md`) was never filled in** — the
  approver merged directly on GitHub rather than replying with a decision, an
  alternative the item's own text explicitly offered ("Merge whenever suits
  you on GitHub directly... the next build-loop pass detects the merge
  itself"). Treated the merge itself as the answer: moved the item to
  `inbox/_handled/`, filled its `## Decision` with what actually happened
  (merged directly, no written reply), and added an entry to
  `agents/eng-manager/config/decision-journal.md` recording that this
  channel was bypassed — worth knowing if it recurs. Filed a proposal
  (`agents/eng-manager/proposals.md`) about the general gap this exposes: a
  ticket's own state can move out from under an open gate item via a channel
  (`control center`) this system doesn't watch, and nothing currently
  cross-checks the two automatically outside a sweep that happens to compare
  them by hand, as this pass just did.

  **Approval cap:** `ENG-002` no longer counts (was the third of 3/3, as
  `blocked_on: approver` — `verified` is terminal and owes nothing to any
  cap). Cap drops to 2/3 (`ENG-003`, `ENG-004` G1s) — see the board index for
  what this pass did with the freed slot.

  `chained: none` — `verified` is a terminal state. Nothing left for a
  machine or the approver to do on this ticket.
