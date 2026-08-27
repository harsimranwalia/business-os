---
id: ENG-001
title: Register this business's repos and prove the loop runs end to end
project: aiorders
type: chore
size: S
severity: P3
priority: now
state: verified
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-23
updated: 2026-08-26
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-001-register-repos-and-prove-the-loop.md
  design: agents/architect/designs/ENG-001-register-repos-and-prove-the-loop.md
  adrs: [ADR-001, ADR-002]
  review: agents/principal-engineer/reviews/ENG-001.md
  test_plan: agents/qa/test-plans/ENG-001.md
  security_review: agents/security/reviews/ENG-001.md
  release:
---

# Register this business's repos and prove the loop runs end to end

The seed ticket every instance starts with. It exists for two reasons.

**First, a board with nothing on it is not a clean board.** `lib/eng-gate-check.sh`
fails closed on an empty board directory, deliberately — the riskiest failure in
this department is a root that resolves somewhere real and empty, which under a
permissive rule would print nothing and exit 0. This ticket is what makes a fresh
instance distinguishable from a misresolved one.

**Second, it is genuinely the first work.** Nothing can be built until the repos
are registered.

## Acceptance criteria

1. Every repo this business owns is registered in `config/projects.md` at **L1**,
   via `skills/repo-onboarder/SKILL.md`, and the approver has approved each.
2. A department-owned git worktree exists under `_eng/` for each registered repo.
3. `lib/eng-gate-check.sh` exits 0 against this instance.
4. One real ticket has moved `intake → shaped` and the board renders it.

## Notes

Close this ticket once the first real ticket is on the board — not before, or the
board is empty again.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-24` note (eng-manager) — gate-check-unavailable incident
  (`inbox/2026-08-24-eng-gate-check-unavailable.md`, raised against this ticket
  because it was in flight when the pre-pass check found `lib/eng-gate-check.sh`
  absent/unreadable) resolved. Root cause fixed in business-os `9366b84` (nine
  `$ROOT/lib/` call sites repointed to `$ENG_DEPT/lib/` after the carve-out).
  Approver decision: **approved**, 2026-08-24T17:00:57Z. Independently re-ran
  `lib/eng-gate-check.sh` against this instance this pass: exit 0, clean. **AC3
  satisfied.** AC1/AC2/AC4 untouched by this pass.
- `2026-08-24` chained: ENG-001 (eng-manager) — this pass was scoped to the
  answered gate only; firing `continue` so the PM can pick up shaping at
  `intake` with a fresh pass.
- `2026-08-25` `intake → shaped` (product-manager) — PRD written at
  `agents/product-manager/specs/ENG-001-register-repos-and-prove-the-loop.md`.
  Read the ticket's own criteria back rather than running the full
  request-readback ceremony (already a spec — see PRD). **AC1/AC2/AC3
  confirmed already satisfied** on re-check this pass: `config/projects.md`
  carries all five repos at L1 (approved 2026-07-28, re-verified
  2026-08-23); all five worktrees present under `~/Documents/projects/_eng/`;
  `lib/eng-gate-check.sh` re-run clean, exit 0. **AC4 open** — no second
  ticket exists yet. `type: chore` auto-skips G1 per
  `config/templates/prd.md`, so no gate item raised; PRD status recorded as
  `approved` directly. Not proceeding to `designed` in this pass — see the
  next line.
- `2026-08-25` note (product-manager) — **AC4 satisfied.** Found a genuine
  approver-filed request already sitting in `inbox/requests/` since
  2026-08-23 (`test-harness.md`) — not a self-originated finding, so no
  conflict with the department's-own-work rule. Ran it through the full
  request-readback (this PM's reading + a blind architect reading; no
  material divergence) and shaped it into `ENG-002` (`intake → shaped →
  awaiting-scope`, `agents/eng-manager/board/ENG-002-*.md`), a smoke-test
  harness for `restaurant-portal`. `ENG-002` reached `shaped` en route to
  `awaiting-scope` (its `size: M` requires G1, unlike this ticket's
  auto-skipped chore), which satisfies this ticket's AC4 literally: "one
  real ticket has moved intake → shaped." All four acceptance criteria are
  now met. Source request moved to `inbox/_handled/2026-08-23-test-harness.md`.
- `2026-08-25` note (product-manager) — **Not advancing this ticket past
  `shaped` this pass, deliberately.** What "building" (branch pushed,
  self-tested, PR body written) means for a ticket whose own deliverable is
  config/registry verification and another ticket — not application code in
  any registered repo — is not addressed anywhere in this department's docs
  (checked `schedules/eng_build_loop.md`, `docs/engineering-team.md`,
  `config/definition-of-done.md`, both `agent.md` files for architect and
  eng-manager). All four ACs are satisfied, so nothing is actually blocked —
  but deciding how a config-only, no-code ticket earns its three enforced
  receipts (review/test-plan/security) is a real design call, arguably worth
  an ADR since it sets precedent for every future instance's own ENG-001.
  Leaving it for the architect with a fresh pass rather than guessing it here.
  `chained: ENG-001` — sitting at `shaped`, owned by the architect (agent,
  not approver, not blocked, not terminal).
- `2026-08-25` `shaped → designed` (architect) — resolved the open question
  the prior pass left: what "building" means, and how the three full-lane
  receipts apply, for a ticket whose four acceptance criteria are all
  satisfied without a diff in any registered project (two are pre-existing
  registry/worktree facts, one is a mechanical check, one is `ENG-002`'s own
  independent progress). Wrote `ADR-001`
  (`agents/architect/decisions/ADR-001-verification-ticket-building-and-receipts.md`):
  a **verification ticket** still passes through every state and owes every
  receipt its lane specifies, but `building` records exactly what was checked
  instead of a branch/PR, and `branch:` stays empty. Considered and rejected
  two alternatives — registering `aiorders` in `config/internal-projects`
  (that file reserves adding a line to the approver, "should be rare," and
  this is expected to be a one-time ticket on this instance; revisit via G2
  if the shape recurs) and delegating via `parent: ENG-001` on `ENG-002`
  (would misrepresent `ENG-002`'s real, independent provenance to borrow the
  ADR-003 exemption). No one-way door — fully reversible, decided directly,
  no G2 raised, approver untouched. Tech design at
  `agents/architect/designs/ENG-001-register-repos-and-prove-the-loop.md`.
- `2026-08-25` `designed → ready` (eng-manager) — work breakdown: zero
  implementation units (no code in any registered project, per ADR-001), so
  nothing to sequence or assign; the ticket proceeds directly to the
  building-as-verification-record step ADR-001 defines. `machine_wip` (6) at
  1/6 going in (`ENG-002`), 2/6 after. **Not proceeding into `building` this
  pass, deliberately** — writing the three receipts
  (`agents/principal-engineer/reviews/ENG-001.md`,
  `agents/qa/test-plans/ENG-001.md`, `agents/security/reviews/ENG-001.md`)
  is real, distinct gate work, and `schedules/eng_build_loop.md` reserves
  that for its own session rather than the tail end of an architect/EM pass —
  same reasoning as `ENG-002` earlier today. `chained: ENG-001` — sitting at
  `ready`, owned by eng-manager (agent, not approver, not blocked, not
  terminal).
- `2026-08-26` `ready → building` (eng-manager, `continue ENG-001` pass) —
  building-as-verification-record per ADR-001. Re-verified all four
  acceptance criteria against disk this pass rather than trusting the prior
  citations:
  - **AC1** — `agents/eng-manager/config/projects.md` → Registered projects:
    all five rows (`aiorders-api`, `aiorders-admin-hub`, `config-site-builder`,
    `restaurant-marketplace`, `restaurant-portal`) still carry **L1**,
    approved 2026-07-28, re-verified 2026-08-23.
  - **AC2** — `~/Documents/projects/_eng/` listed fresh this pass: all five
    worktrees present (`aiorders-admin-hub`, `aiorders-api`,
    `config-site-builder`, `restaurant-marketplace`, `restaurant-portal`).
  - **AC3** — `lib/eng-gate-check.sh` re-run fresh this pass against this
    instance: exit 0, no violation lines on stdout.
  - **AC4** — `ENG-002` (`agents/eng-manager/board/ENG-002-*.md`) now at
    `building`, branch `chore/ENG-002-smoke-test-harness` — already past
    `shaped`, the literal bar AC4 sets; satisfied a fortiori.

  `branch:` stays empty — no registered project carries a diff for this
  ticket; per ADR-001 this is the documented shape for a verification
  ticket, not an omission. `machine_wip` (6) unchanged at 2/6 (`ENG-001`,
  `ENG-002`) — both `ready` and `building` fall inside the counted range, so
  this transition crosses no cap boundary.

  **Not proceeding into `in-review` this pass, deliberately** — the
  principal-engineer/QA review of these verification claims
  (`agents/principal-engineer/reviews/ENG-001.md`,
  `agents/qa/test-plans/ENG-001.md`, per the architect's design's Components
  table) is real, distinct gate work reserved for its own session, same
  reasoning already applied at every earlier hop on this ticket and on
  `ENG-002`. `chained: ENG-001` — sitting at `building`, owned by eng-manager
  per ADR-001's override of the normal backend/frontend/database owner
  (agent, not approver, not blocked, not terminal).
- `2026-08-26` `building → in-review → in-security` (eng-manager, `continue
  ENG-001` pass — this session) — the combined review+quality hop, per
  `schedules/eng_build_loop.md` step 6, followed by security on the same
  pass (ENG-002's own hop earlier today did the same three roles in one
  session; nothing here is a departure from that). Pre-pass
  `lib/eng-gate-check.sh`: exit 0, clean. Fresh gate-return sweep of all
  three inboxes found nothing pending for `ENG-001` — its last open question
  (what `building`/receipts mean) was resolved directly by the architect via
  `ADR-001`, no approver gate ever raised for it.

  **`in-review` (code review + quality gate, combined hop).** Acted as
  principal-engineer: per `ADR-001`, there is no diff, so the review confirms
  the verification claims are actually true on disk rather than reviewing
  code. Independently re-derived all four ACs this round rather than citing
  the prior pass's numbers — re-read `config/projects.md` (AC1: five rows,
  all L1), re-listed `_eng/` and ran `git rev-parse --abbrev-ref HEAD` in
  each of the five worktrees to confirm they're real and resolvable, not
  just present directories (AC2), re-ran `lib/eng-gate-check.sh` fresh (AC3:
  exit 0), and re-read `ENG-002`'s own board file directly (AC4: now at
  `blocked` with an open PR, several states past the literal "reached
  `shaped`" bar). Verdict **pass** — receipt written to
  `agents/principal-engineer/reviews/ENG-001.md`, `links.review` set. Acted
  as qa: wrote the test plan this ticket never had
  (`agents/qa/test-plans/ENG-001.md`), one row per acceptance criterion,
  each a direct disk/registry check rather than an automated test — no
  suite exists to run, and none is owed (`ADR-001`). Verdict **pass**,
  `links.test_plan` set.

  **`in-security`.** Acted as security: threat-modelled the ticket's own
  evidence trail (no new input, capability, data exposure, or component to
  compromise — nothing here is a runtime artifact). Walked OWASP A01–A10:
  all ten `n/a`, since no code, dependency, endpoint, or config surface was
  produced. Secret-scanned every file in this ticket's paper trail
  (`grep -niE 'api[_-]?key|secret|password|token|bearer|-----BEGIN'` across
  `ADR-001`, the design doc, the PRD, this board file, and the two receipts
  written this pass): one hit, the prose word "secret" in the design doc's
  own component description — not a credential. SOC 2 evidence trail
  (ticket → PRD → ADR → design → review → test plan → this verdict)
  confirmed complete. Verdict **pass** — receipt at
  `agents/security/reviews/ENG-001.md`, `links.security_review` set.

  **2 transitions this pass** (`building→in-review`, `in-review→in-security`)
  — well inside the 4-transition cap.

  **Not proceeding into `ready-to-ship` this pass, deliberately, for two
  independent reasons.** First, what `ready-to-ship`/`awaiting-release`/
  `shipped` mean for a ticket with no deploy target is a genuinely open
  question `ADR-001` does not answer — its Decision section names
  `building`, `in-review`, `in-qa`, and `in-security` specifically, and both
  the PRD's own Risks section and this ticket's prior log entries flagged
  the ambiguous stretch as exactly that span, never further. The design
  doc's Rollout section ("not applicable — nothing is deployed... the
  ticket's own release is this instance's board correctly reflecting facts
  that are already true") reads as a reasonable answer but was never framed
  as a considered decision the way `ADR-001` was, with alternatives weighed
  — improvising past it here would repeat the exact failure this ticket's
  own meta-history exists to prevent (a state's meaning invented in passing
  rather than decided). Second, and independently sufficient on its own: the
  approval cap is **3/3 (full)** right now — checked fresh this pass, not
  from the board's own cached header: `inbox/2026-08-26-eng002-merge-request.md`
  (`## Decision` — "Filled in by the approver.", unanswered),
  `inbox/2026-08-25-eng003-g1-scope.md` and
  `inbox/2026-08-25-eng004-g1-scope.md` (both `## Decision` — "Filled in by
  the approver.", unanswered). Per the Guards section, "at the cap, nothing
  advances into a gate state" — reaching `awaiting-release` would need a G3
  item, and this instance's `aiorders` pseudo-project qualifies for neither
  of the table's auto-routes (L1's merge-request shortcut or L3's
  auto-approve), since it is not a registered project at any autonomy level.
  So even a settled answer to the first question could not be acted on this
  pass regardless.

  Same reasoning this ticket has applied at every earlier hop: do the
  well-scoped work fully, stop at the next genuinely undecided boundary, and
  hand off with a fresh context rather than guess. `chained: ENG-001` —
  sitting at `in-security`, owned by security (agent, not approver, not
  blocked, not terminal); the cap-full condition blocks the *next* hop's
  gate, not this ticket's own present state, so this is not "held by a cap"
  in the sense the chaining guard means.
- `2026-08-26` `in-security → ready-to-ship` (architect, then eng-manager
  acting as devops — `continue ENG-001` pass, this session) — resolved the
  boundary the prior pass named and stopped at, then acted on it in the same
  pass, same combined-hop shape `ENG-002` used earlier today for its own
  review+quality+security+ready-to-ship run.

  **Architect: `ADR-002`**
  (`agents/architect/decisions/ADR-002-verification-ticket-release-and-g3.md`)
  — extends `ADR-001` past `in-security`, which is as far as its Decision text
  ever named. Re-checked fresh rather than trusted from `ADR-001`'s own
  citation: `config/projects.md` still lists only the five app repos (all
  **L1**), `config/internal-projects` is still empty — so `aiorders` qualifies
  for neither of the state table's auto-routes (L1's merge-request shortcut,
  L3's auto-approve). Decision: a verification ticket owes `ready-to-ship`,
  `awaiting-release` (G3), `shipped`, and `verified` exactly as any other
  full-lane ticket — none skipped, none auto-routed by inventing an autonomy
  level this instance's registry never granted. Only the *content* changes,
  continuing `ADR-001`'s pattern: `ready-to-ship` records devops confirming
  there is nothing to release rather than a real plan; G3 asks the approver to
  confirm the ticket's record is accurate rather than to approve a deploy that
  doesn't exist; `shipped` records that confirmation rather than a
  fabricated release. G3 itself is deliberately **not** waived or downgraded
  to L3's notify-after treatment — `docs/engineering-team.md` names "say yes
  to production" as one of exactly three things this department reserves for
  the approver, department-wide, and that is a different kind of call from
  `ADR-001`'s own (recording `building`'s absence honestly costs nothing and
  sets no precedent about who decides what; skipping a whole class of ticket's
  G3 would). No G2 raised — reversible on the recording half, and the G3 half
  is a decision *not* to remove a human checkpoint, which needs no escalation.
  Logged in `agents/architect/decisions/_index.md`, Next ID now `ADR-003`.

  **Eng-manager acting as devops: `ready-to-ship`.** Per `ADR-002`, confirmed
  and logged rather than skipped: no release plan, rollback, or observability
  plan exists because no registered project carries a diff for this ticket —
  re-checked `config/projects.md` and `_eng/` fresh this pass (still all five
  repos **L1**, still all five worktrees present:
  `aiorders-admin-hub`, `aiorders-api`, `config-site-builder`,
  `restaurant-marketplace`, `restaurant-portal`) rather than citing the
  `in-security` hop's numbers. Release window checked for consistency with
  today's `ENG-002` hop even though nothing deploys: 2026-08-26 is a
  Wednesday, no `ENG_RELEASE_FREEZE` set — clean, moot either way. Pre-pass
  `lib/eng-gate-check.sh` (whole board and `ENG-001`-scoped): exit 0, clean,
  both re-run fresh this pass.

  **1 transition this pass** (`in-security → ready-to-ship`) — well inside the
  4-transition cap.

  **Not proceeding into `awaiting-release` this pass — the approval cap is
  3/3 (full), checked fresh, not from the board's cached header.**
  Independently re-read all three open items' `## Decision` sections directly:
  `inbox/2026-08-26-eng002-merge-request.md`,
  `inbox/2026-08-25-eng003-g1-scope.md`, and
  `inbox/2026-08-25-eng004-g1-scope.md` all still read "Filled in by the
  approver.", unanswered. Also confirmed the cap itself is genuinely 3 from
  `config/config.yaml` (`wip.approval_cap: 3`) rather than assumed. Per the
  Guards section, "at the cap, nothing advances into a gate state" —
  `awaiting-release` is exactly that, so the G3 item `ADR-002` calls for is
  not raised this pass. This is different from every earlier stop on this
  ticket: those were blocked by an undecided question this pass could answer
  itself; this one is blocked by a department-wide resource limit that a
  single ticket's own pass has no authority to override.

  **`chained: none` — held by the approval cap (3/3, full), not by anything
  left for this ticket to decide.** Every acceptance criterion is satisfied,
  `ADR-002` has resolved what every remaining state means, and devops's own
  `ready-to-ship` confirmation is complete — there is no more machine-ownable
  work on `ENG-001` until a slot frees. Re-firing `continue ENG-001` now would
  re-derive this identical conclusion at the cost of a full pass with nothing
  new to show for it, which is exactly the "burning usage" the chaining guard
  exists to prevent, and the guard's own list names this condition by name
  ("held by a cap (WIP or approvals)"). This resumes when the cap clears —
  either the next `scheduled` safety-net sweep re-checks it after the
  approver answers one of the other three open items, or a fresh `continue
  ENG-001` is fired directly once a slot is known free. Not a broken chain:
  the dead-end sweep should read this entry, not flag it.
- `2026-08-26` `ready-to-ship → awaiting-release` (eng-manager — `scheduled`
  safety-net pass) — the cap that held this ticket at the entry directly
  above cleared during this same pass, not by the approver answering one of
  the three items it was waiting on: `ENG-002` independently reached
  `verified` this pass (its own merge, detected fresh via local git
  ancestry — see that ticket's log), which no longer counts against
  `wip.approval_cap` now that it's terminal. Re-read `config/config.yaml`
  directly rather than assuming: cap is 3, and with `ENG-002` off it, only
  `ENG-003`'s and `ENG-004`'s G1s remain open (2/3) — room for one more.

  Raising this ticket's G3 is advancing an already-in-flight ticket into its
  own next gate, not a new start — the same reasoning `ENG-002`'s own history
  used when it reached `blocked` at 2/3→3/3 earlier — so `wip.approver_limit`
  (2, already held by `ENG-003`+`ENG-004`)'s "nothing new starts" rule
  doesn't apply here; only `approval_cap` (which gates advancing into a gate
  state) does, and it has room.

  Wrote the G3 item per `ADR-002`'s own framing — not "ship this to
  production" (nothing is shipping), but "is this ticket's record accurate,
  and is it done" — at `inbox/2026-08-26-eng001-g3-verification.md`, and
  raised it (`lib/eng-notify.sh raise`; reproduced the already-filed
  `MODE`-collision bug, log line read `sent: active` rather than `sent:
  raise`, not a new finding; `notified:` stamped by hand since the script
  never writes back). Approval cap now 3/3 (full) again — `ENG-003`, `ENG-004`,
  and this ticket's own G3 — a different composition than before, not a new
  stall episode (the board never actually cleared to "not full" where anyone
  outside this pass could observe it; see the board index for the stall-alert
  reasoning).

  `chained: none` — `awaiting-release`, owner `approver`. This is the human
  gate `ADR-002` decided this ticket still owes; nothing machine-ownable
  remains until it's answered.
- `2026-08-26` `awaiting-release → shipped → verified` (eng-manager acting as
  devops, then product-manager — `decision` event pass, `inbox/2026-08-26-eng001-g3-verification.md`)
  — the G3 this ticket was waiting on was answered: **approved**, no
  additional comment recorded beyond the decision itself, `decided:
  2026-08-27T05:05:01.598404+00:00`. Per this event's own narrower contract
  ("act on the answered gate item in inbox/ and advance only the ticket it
  belongs to"), only this ticket was touched this pass.

  **Acted as devops at `shipped`, per `ADR-002`.** Recorded the G3
  confirmation in place of a deploy rather than skipping the step: no release
  plan, rollback, or observability plan exists because no registered project
  carries a diff for this ticket, re-confirmed fresh (see below). Per
  `ADR-002`'s own Decision text, **no release record is fabricated at
  `agents/devops/releases/`** for a deploy that never happened — this log
  entry is the record. `links.release` stays empty, same shape as
  `branch:` staying empty under `ADR-001`.

  **Acted as product-manager at `verified`.** Re-confirmed all four
  acceptance criteria against disk fresh this pass, not cited from any prior
  hop's numbers:
  - **AC1** — `agents/eng-manager/config/projects.md` → Registered projects:
    read directly this pass, all five rows (`aiorders-api`,
    `aiorders-admin-hub`, `config-site-builder`, `restaurant-marketplace`,
    `restaurant-portal`) still carry **L1**.
  - **AC2** — `~/Documents/projects/_eng/` listed fresh this pass: all five
    worktrees present.
  - **AC3** — `departments/engineering/lib/eng-gate-check.sh` re-run fresh
    this pass, both whole-board and `ENG-001`-scoped: exit 0, no violation or
    parse-error lines, both runs.
  - **AC4** — `agents/eng-manager/board/ENG-002-restaurant-portal-smoke-test-harness.md`
    read directly this pass: `state: verified` — `ENG-002` reached the board,
    passed `shaped`, and has since shipped and been confirmed live. AC4's
    literal bar ("moved `intake → shaped`") satisfied a fortiori.

  Also re-opened and read (not just cited) the three existing receipts this
  pass: `agents/principal-engineer/reviews/ENG-001.md` (`verdict: pass`),
  `agents/qa/test-plans/ENG-001.md` (`last_result: pass`, all four AC rows
  `pass`), `agents/security/reviews/ENG-001.md` (`verdict: pass`, all ten
  OWASP categories `n/a`, secret scan clean). All three hold.

  **2 transitions this pass** (`awaiting-release→shipped`,
  `shipped→verified`) — well inside the 4-transition cap.

  Gate item's `## Decision` was already filled in by the approver (unlike
  `ENG-002`'s merge request, which the pass had to fill in from GitHub
  ancestry) — moved as-is to `inbox/_handled/2026-08-26-eng001-g3-verification.md`,
  no edit needed. Journaled in `agents/eng-manager/config/decision-journal.md`.

  **This ticket is now terminal.** The seed ticket is done: all four
  acceptance criteria hold, every receipt this lane requires is on file and
  independently re-verified at least twice, and the department's board is no
  longer "empty by construction" — `ENG-002` through `ENG-005` exist as real,
  independent tickets. `ADR-001` and `ADR-002` stay on record for whichever
  future instance's own seed ticket needs the same pattern.

  As a side effect of this ticket closing, the approval cap drops from 3/3 to
  2/3 (`ENG-003`+`ENG-004` G1s only) and approver-facing WIP drops from 3 to
  2 (no longer over the soft limit) — noted here for the next pass's
  arithmetic, not acted on: dispatching any newly-freed capacity on another
  ticket is out of scope for a `decision` event pass scoped to the gate item
  it answers.

  `chained: none` — `verified`, a terminal state. Per the chaining guard,
  a terminal ticket is never re-fired.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean
  (whole board).
