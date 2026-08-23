# Skill: code-review-gate

**Owner:** principal-engineer
**Model:** opus (correctness reasoning over a whole diff)
**Trigger:** a ticket enters state `in-review` — **runs concurrently with the quality gate**
**Suppressed when:** sabbath, retreat

---

## Purpose

The blocking code review. Verdict is `pass` or `fail` — there is no "pass with
comments." Every finding is specific enough to act on without a follow-up
question.

---

## Inputs

- `agents/eng-manager/board/{ENG-NNN}-{slug}.md` — the ticket and its links (required)
- `agents/architect/designs/{ENG-NNN}-{slug}.md` — what this was supposed to do
- `agents/eng-manager/config/engineering-standards.md` — the bar
- The project's own conventions — its `CLAUDE.md`/`AGENTS.md`, style config, and
  the code surrounding the change
- The full diff on the branch
- `agents/principal-engineer/notebook/` — this agent's repeated findings

---

## Steps

### 1. Mode check

`sabbath` or `retreat`: exit without writing.

### 2. Scan for automatic failures first

Ten items in `engineering-standards.md`. Any hit → **fail immediately**, one
line per hit, and stop. Do not conduct a thorough review of a change with a
credential in it.

1. Secret, credential, token, or key committed
2. Silent exception swallow
3. Missing test on a bug fix
4. Untyped public interface with no documented reason
5. Unbounded query or missing pagination
6. New dependency with no justification
7. Unrelated refactor bundled in
8. Commented-out code or an unowned `TODO`
9. Datastore write bypassing the project's data layer
10. Auth, payment, or deletion path changed with no failure-case test

### 3. Read the ticket and design

What was this supposed to do? A change that works but doesn't do what the design
said is a fail — either the code is wrong or the design is, and both need
resolving before merge.

### 4. Review the whole diff for shape

Right change, right places, right size? Specifically:
- Is this one concern, or several wearing one branch?
- Is there an abstraction here for a use case that doesn't exist?
- Is there duplication that should be shared, or sharing that should be split?
- Could this be smaller? Deleting code is a valid and often best outcome.
- Does it read like the code around it? A second way to do what the project
  already does is a fail, even when the new way is better — better goes in its
  own ticket, applied everywhere.

### 5. Review the lines

Correctness first: concurrency, partial failure, empty and boundary inputs,
error paths, idempotency, ordering assumptions, off-by-one, timezone, null
handling. Then naming, then standards conformance.

### 6. Review what isn't there

The step most reviews skip and most bugs live in:
- The missing test — especially the failure case
- The unhandled input
- The log line that would make this debuggable at 2am
- The migration that should accompany a model change
- The rollback consideration

### 7. Assess test quality (shape, not coverage)

QA owns coverage; you own whether the tests are worth anything. Fail on: tests
asserting implementation details, tests that cannot fail, a bug fix with no
regression test, or a test that mocks the thing it claims to verify.

### 8. Write the verdict

Into the ticket's `review:` block. Every finding: **file and line, what's wrong,
why it matters, the specific fix.** State whether each is blocking or a
preference — and if it's only your taste, either let it go or make it a standard.

Acknowledge genuinely good work in one line. The engineer agents learn from
their notebooks, and precise positive signal is as useful as precise negative.

**On `pass` — and only on `pass` — write the receipt.**
`agents/principal-engineer/reviews/{ENG-NNN}.md`, then set `links.review` on the
ticket to that path. Same file on the fast lane, where the combined gate's
verdict already exists and this only asks that it land somewhere with a
predictable name. It carries the verdict, the round number, the diff reviewed,
and what was checked — the same content that used to live only in the ticket
body, in a file the ticket does not own.

**On `fail`, write nothing here.** The verdict goes in the ticket log and your
notebook, which is where it already goes. This is not tidiness: `lib/eng-gate-check.sh`
tests that the receipt file exists and is non-empty, and it cannot read the
verdict inside. A receipt written on the way through regardless of outcome would
satisfy the exact check it exists to prove, and a ticket could reach `shipped`
holding three receipts that all say "failed" — which is ENG-004's bug arriving
back through the fix for it.

### 9. Route

QA runs its gate **concurrently with this one** on the same diff — the two don't
depend on each other, and running them back to back cost a wall-clock step for
nothing.

- **pass** → the receipt from step 8 is on disk and `links.review` is set; the
  ticket continues to `in-security` once QA has also passed
- **fail** → state `building`, owner the implementing engineer, **and no receipt
  file** — see step 8. **QA's result for this round is discarded**, whatever it
  was: the code is changing. Wasted compute, saved wall-clock — and compute isn't
  the scarce resource here. QA writes no receipt for a discarded round either.
- **third failed round** → state `blocked`, owner `eng-manager`, escalate to the
  architect. Rising rounds mean the design or the brief is wrong, not the engineer.

Log the round number. First-pass rate is tracked at the department level
(`agents/eng-manager/config.yaml` → `speed`); a rate below 70% means engineers
are being sent to write code without knowing what this gate will ask, and the
fix is upstream in the brief — **never in reviewing more leniently.**

### 10. Check for standards promotion

If this is the third time you've written the same correction (check your
notebook), edit `agents/eng-manager/config/engineering-standards.md` to add it,
and tell the EM. That's how the department stops repeating itself.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/principal-engineer/reviews/{ENG-NNN}.md` | **The receipt — written on a `pass` verdict ONLY, never on a fail.** The check that reads it (`lib/eng-gate-check.sh`) tests that the file exists and is non-empty; it cannot read the verdict inside. So a receipt written on a fail satisfies the exact check it is meant to prove. Set `links.review` on the ticket in the same write. Applies on the fast lane too — no new artifact, no extra hop, no new gate: the combined gate's verdict simply lands in a file with a predictable name. |
| ticket `review:` block | Verdict and findings |
| ticket log | One line: verdict, round number |
| `agents/principal-engineer/notebook/{date}-review-log.md` | Findings by category and agent |
| `agents/eng-manager/config/engineering-standards.md` | Edited on a third occurrence |

---

## Trace

`traces/principal-engineer-{run-id}.json` — ticket, verdict, finding count by
category, round number, automatic-failure hits.

---

## Failure modes to avoid

- **Passing under time pressure.** A gate that bends isn't a gate.
- **Vague findings.** "Consider refactoring" wastes a whole round.
- **Reviewing the author.** No "you always." The pattern goes in the notebook and
  becomes a standard.
- **Approving what you don't understand.** If the diff is unreadable, that's the
  finding: split it.
- **Doing QA's or security's job.** Four gates, four owners. Passing here says
  nothing about the other three.
