# Skill: bug-triage

**Owner:** qa
**Model:** sonnet (severity and root-cause judgment)
**Trigger:** a test failure, a defect found in review, or a production issue
**Suppressed when:** sabbath, retreat — except a P0, which always surfaces

---

## Purpose

File a bug precisely enough that the fix is obvious, with a severity taken from
the definition and an owner who will actually fix it.

---

## Inputs

- The failure: test output, reproduction, or the report
- `agents/eng-manager/config/definition-of-done.md` — the severity definitions
- `agents/qa/bugs/_index.md` — `next_id` and the open ledger
- `agents/eng-manager/config/templates/bug.md`
- The ticket under test, when there is one

---

## Steps

### 1. Reproduce from a clean state

Before filing anything. A bug that can't be reproduced gets filed anyway, with
that fact stated and the conditions under which it appeared — but a reproduction
attempt comes first, always.

Record: exact steps, branch/commit, project, and any config that matters.

### 2. Check for a duplicate

Scan the open ledger. A duplicate gets `status: duplicate` with a link, not a
second file. Three bugs with the same root cause is not three bugs — it's a
design problem, and that gets filed as an intake card with the EM instead of a
fourth patch.

### 3. Write the symptom, not the guess

The title is what happens, observably. `Order total excludes tax when the cart
has one item`, not `Tax calculator broken`. A title carrying a guess sends the
fix in the wrong direction, and titles are sticky.

### 4. Set the severity from the definition

| Severity | Definition |
|---|---|
| **P0** | Production down, data loss in progress, or an active security incident |
| **P1** | Core function broken for real users, no workaround |
| **P2** | Broken with a workaround, or degraded experience |
| **P3** | Cosmetic or minor |

**Severity is not negotiable and not a signalling device.** Escalating a P1 to a
P0 to get attention is a correction that goes in your own notebook. Every
severity needs an impact statement — who is affected and how badly — because a
severity with no impact statement is a guess.

### 5. Assign an owner

Always, while the bug is open. Route by surface: server → `backend`, UI →
`frontend`, schema or query → `database`, infrastructure or deploy → `devops`,
a security finding → back to the engineer who owns the code, with `security`
holding the verdict.

**A bug with no owner is a dead end.** Don't create one.

### 6. Write the file

`agents/qa/bugs/{BUG-NNN}-{slug}.md` from the template. Increment `next_id` and
add the ledger row in the same write. Evidence goes in: failing test name, log
excerpt with secrets redacted, stack trace, screenshot path.

### 7. Route by severity

- **P0** → interrupt the approver through the EM immediately. This is one of
  the very few interrupts the whole department has. Also notify `devops` — a
  P0 is an incident and gets an incident record.
- **P1** → the next build-loop pass. Sets the owning ticket back to `building`.
- **P2 / P3** → the ledger, picked up in sequence by the EM.

### 8. Track to closed

A bug is closed only when: root cause identified (not symptom), fix merged,
regression test written **and verified to fail against the old code**, and QA
has confirmed it. `wontfix` needs a stated reason, and for P0/P1 it needs the
approver's awareness through the EM.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/qa/bugs/{BUG-NNN}-{slug}.md` | The bug |
| `agents/qa/bugs/_index.md` | Ledger row, `next_id` incremented |
| ticket log | One line when a bug sends a ticket back to `building` |
| `agents/eng-manager/inbox/` | An intake card when three bugs share a root cause |

---

## Trace

`traces/qa-{run-id}.json` — bug IDs filed, severities, owners, duplicates found.

---

## Failure modes to avoid

- **A guess in the title.**
- **Severity inflation** to get attention, or deflation to unblock a release.
- **No owner.**
- **Closing on the symptom.** The same bug will return with a new number.
- **Silent closure.** Every close has a reason in the file.
