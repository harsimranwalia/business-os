# Bug template

Written by `qa` at `agents/qa/bugs/{BUG-NNN}-{slug}.md`. Next ID lives in
`agents/qa/bugs/_index.md`, which is the ledger — every open bug appears there
with an owner and an age.

A bug with no owner is a dead end. The build loop flags any bug that has been
open past its severity's SLA.

```markdown
---
id: BUG-000
title: One line — the symptom, not the guess at the cause
project: <project>
severity: P2              # P0 | P1 | P2 | P3 — see definition-of-done.md
status: open              # open | assigned | fixed | verified | wontfix | duplicate
owner: backend            # the agent who will fix it — never empty while open
found_by: qa
found_in: ENG-000         # the ticket under test, or `production`
fix_ticket:               # the ticket that carries the fix
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## Symptom

What happens, observably. No theory.

## Reproduction

1. Exact steps
2. From a clean state
3. Every time, or {n} times in {m}

**Environment:** branch/commit, project, config that matters.

## Expected

What should happen instead, and where that expectation comes from — an
acceptance criterion, a standard, or a contract.

## Impact

Who is affected and how badly. This justifies the severity; a severity without
an impact statement is a guess.

## Evidence

Failing test name, log excerpt (secrets redacted), stack trace, screenshot path.

## Fix

Filled in by the engineer.

- **Cause:** the actual root cause, not the symptom
- **Change:** what was changed
- **Regression test:** the test that now fails against the old code
- **Verified by:** qa, on {date}
```

## Severity SLA

| Severity | Response | Escalates if open past |
|---|---|---|
| P0 | Immediately, interrupts everything | 0 — already interrupting |
| P1 | Next build-loop pass | 2 working days → weekly report |
| P2 | Within the week | 10 working days → weekly report |
| P3 | Backlog, no commitment | never — but reviewed quarterly and closed honestly |

## Rules

- **Symptom first, cause later.** A bug titled with a guess sends the fix in the
  wrong direction.
- **No fix without a regression test.** The test must fail against the old code —
  QA verifies that, not the engineer's word for it.
- **`wontfix` needs a reason and the approver's awareness** if it's P0/P1.
  Silent closure is not allowed.
- **Root cause, not symptom.** Three bugs with the same cause is a design
  problem: file the design ticket, don't patch it a fourth time.
- **Bugs found in production** are filed the same way, with `found_in:
  production` and a note in the release record they came from.
