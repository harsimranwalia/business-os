# Skill: test-suite-run

**Owner:** qa
**Model:** haiku (run + parse — mechanical) escalating to sonnet only on failures
**Trigger:** after test-authoring; on demand; before any release
**Suppressed when:** sabbath, retreat

---

## Purpose

Run the suite, report what actually happened, and turn failures into filed bugs.
No interpretation, no rounding up, no "green except".

---

## Inputs

- `agents/qa/test-plans/{ENG-NNN}.md` — the plan and its `suite_command`
- The project's test command — from the plan, or from
  `agents/eng-manager/config/projects.md` if this is the first run
- `.env` → `MODE`

---

## Steps

### 1. Mode check

`sabbath` or `retreat`: exit.

### 2. Run the full suite

The exact command in the plan. Full suite, not the changed files — the point is
catching what this change broke elsewhere. Capture stdout and stderr.

Also run the project's lint, typecheck, and build. A green suite on code that
doesn't build is not a pass.

**Haiku handles steps 2–4.** Escalate to sonnet only if something failed.

### 3. Parse the result

Record the real numbers into the plan's `## Result` section: passed, failed,
skipped, and the wall-clock time.

**Skipped tests are counted and explained.** A suite quietly skipping forty
tests is a suite nobody is reading.

### 4. Green?

If passed with zero failures and zero unexplained skips: update the plan, set
`last_run` and `last_result: pass`, and return to the caller. Done.

### 5. Red — escalate to sonnet, then classify each failure

For each failing test, decide which of three it is:

| Kind | Signal | Action |
|---|---|---|
| **Real defect** | Fails consistently, traces to the change | `bug-triage` → file it |
| **Bad test** | The behaviour is correct; the test asserted implementation or a stale expectation | Fix the test, note it in the notebook |
| **Flaky** | Passes and fails on identical code | **P2 bug**, quarantine, never delete quietly |

Re-run a suspected flaky test at least three times before calling it flaky.
Guessing here is how flakiness becomes permanent.

### 6. Never make red green by removal

Deleting, skipping, or loosening a test to get a green run is forbidden. If a
test is genuinely wrong, fix it and record why in the notebook — the change must
be visible and reviewable, never silent.

### 7. File the bugs

Every real defect through `skills/bug-triage/SKILL.md`. Severity comes from the
definition, not from how inconvenient it is. Every bug gets an owner in the same
write.

### 8. Report

Update the plan's result block: numbers, bugs filed, verdict `pass` or `fail`.
Return the verdict to the caller — the quality gate reads it directly.

---

## Outputs

| File | Purpose |
|---|---|
| `agents/qa/test-plans/{ENG-NNN}.md` | Result block: numbers, bugs, verdict |
| `agents/qa/bugs/{BUG-NNN}-{slug}.md` | One per real defect |
| `agents/qa/bugs/_index.md` | Ledger updated, `next_id` incremented |
| `agents/qa/notebook/{date}-flaky.md` | Flaky findings, when any |

---

## Trace

`traces/qa-{run-id}.json` — command, passed/failed/skipped, duration, bugs
filed, verdict.

---

## Failure modes to avoid

- **"Green except the flaky one."** That's a fail and a P2 bug.
- **Running only the changed files.** The regression is the point.
- **Reporting a rounded result.** Exact numbers, always.
- **Silently fixing a test to get green.** Visible and reviewable, or not at all.
- **Calling a test flaky after one re-run.** Three, minimum.
