---
id: ADR-001
title: Verification tickets satisfy `building` and receipts without a diff
project: aiorders
ticket: ENG-001
status: accepted
decided_by: architect
date: 2026-08-25
supersedes:
superseded_by:
---

# ADR-001: Verification tickets satisfy `building` and receipts without a diff

## Context

ENG-001 is this instance's seed ticket. All four of its acceptance criteria are
satisfied without a diff in any registered project: two are pre-existing
registry/worktree facts established through the project-card mechanism
(approved 2026-07-28, re-verified 2026-08-23), one is a mechanical check
(`lib/eng-gate-check.sh` exit 0), and the fourth is satisfied by `ENG-002`'s
own, independent progress (it reached `shaped`). `project: aiorders` names
this instance's own engineering substrate, not a row in
`agents/eng-manager/config/projects.md` (which lists only the five app repos)
and not an entry in `config/internal-projects` (empty).

`building`'s documented exit condition — "branch pushed, self-tested, PR body
written" (`definition-of-done.md`) — assumes a registered project with a
worktree to branch in. ENG-001 will never have one. Full lane's three
receipts are otherwise unconditional at `shipped`/`verified`
(`lib/eng-gate-check.sh`'s receipt table), and the only exemption the checker
recognises is `parent:`-based delegation to a settled, shipped child
(ADR-003, from this department's history prior to the business-os port).
Checked and confirmed silent on this exact gap: `schedules/eng_build_loop.md`,
`docs/engineering-team.md`, `definition-of-done.md`, and both the architect's
and eng-manager's `agent.md` — see this ticket's PRD (Risks and unknowns) and
its PM-shaping log entry.

## Decision

A **verification ticket** — one whose acceptance criteria are all satisfied
without producing a diff in any registered project, either because they check
pre-existing state or because they're satisfied by another ticket's
independent progress — still passes through every state in its lane's normal
path, including `building`, `in-review`, `in-qa`, and `in-security`, and still
owes every receipt its lane specifies. What changes is only what `building`
records and what the gates review: instead of a branch and a PR, `building`'s
log entry names exactly which files and commands were checked and what each
showed, `branch:` stays empty with a one-line note explaining why, and
principal-engineer/QA/security each review that verification work directly —
confirming the claims are actually true on disk, not that a diff is
well-written — rather than reviewing code that does not exist.

## Alternatives

| Option | Why not |
|---|---|
| Register `aiorders` in `config/internal-projects`, move to `lane: internal` (drops the QA and security receipts) | That file's own header reserves adding a line to "the approver's call... and should be rare." Spending it isn't this architect's decision to make alone, and ENG-001 is expected to be a one-time seed ticket on this instance — there is nothing yet to amortise the cost of asking against. Revisit via G2 if a second ticket of this exact shape appears (see Review trigger). |
| Delegate via `parent: ENG-001` on `ENG-002`, using the ADR-003 parent exemption | `ENG-002` is a real, independent, `restaurant-portal`-scoped ticket with its own PRD and G1 — it was never split out of ENG-001's work. Setting `parent:` on it to borrow the exemption would misrepresent that provenance to every future reader of the board. |
| Leave the gap undocumented and let a future pass improvise a state mapping on arrival at `building` | This is exactly the failure `schedules/eng_build_loop.md` step 6b names — an instruction fixed in whichever file a future pass happens to think of, while the enforced checker still expects a branch it will never see. `lib/eng-gate-check.sh` cannot be edited from this instance, so an improvised, undocumented rule is not a bad idea to avoid — it is the same failure ENG-001's own history (reaching `main` "shipped" while owing all three gates) exists to prevent. |

## Consequences

**Accepted:** principal-engineer, QA, and security each spend a short pass
reviewing verification claims instead of a diff — a small, real cost, not
skipped.

**Gained:** the full lane's receipts stay meaningful and unconditional for
this ticket; no lever reserved for the approver is spent on a ticket that
doesn't need it; the pattern is documented for whichever future ticket turns
out to be verification-only rather than code-bearing.

**Reversibility:** cheap. This decision binds only how a diff-less ticket is
reviewed on this instance; it changes no project's autonomy and no registered
repo. Superseding it later costs one new ADR and touches no code.

## Review trigger

If a second verification-only ticket appears on this instance, revisit
whether the internal-lane registration rejected above (premature for a single
occurrence) is now worth raising to the approver as a G2 — two occurrences is
the pattern threshold this department already uses elsewhere (e.g. promoting
a recurring correction to a standard).
