# Test plan template

Written by `qa` at `agents/qa/test-plans/{ENG-NNN}.md` before any test is  <!-- eng-receipt-exception: QA's plan is written before the gate runs; the pass-verdict-only rule does not apply to it -->
authored. The plan is what makes the QA gate objective — without it, "tested" is
an opinion.

```markdown
---
ticket: ENG-000
project: <project>
author: qa
created: YYYY-MM-DD
suite_command:            # exact command, e.g. `npm test`, `pytest -q`
last_run: YYYY-MM-DD
last_result: pass         # pass | fail
coverage_note:            # coverage on changed lines, if the project measures it
---

# Test plan — {Title}

## Acceptance coverage

One row per acceptance criterion from the PRD. Every criterion gets a test. A
criterion with no test means the ticket does not leave `in-qa`.

| AC | Criterion | Test | Level | Status |
|---|---|---|---|---|
| 1 | {from PRD} | `test_file::test_name` | unit / integration / e2e | pass |

## Failure paths

The tests that matter more than the happy path. One row per way this can break.

| Scenario | Expected behaviour | Test |
|---|---|---|
| Invalid input at the boundary | Rejected with a clear error, nothing written | |
| Downstream service times out | Bounded retry, then a clean failure | |
| Unauthorised caller | Denied, and the denial is logged | |
| Concurrent request on the same record | No lost update | |

## Regression risk

What existing behaviour could this break? Name the specific paths and the tests
that cover them. For a project with real transactional data, any change near
payments, orders, or other core business data requires an explicit regression
pass on that critical path.

## Not automated

Anything verified by hand, with the reason automation can't reach it and the
evidence that it was actually checked. This list should be short and shrinking.

## Result

- **Run:** `{command}` on `{date}`
- **Outcome:** {n} passed, {n} failed, {n} skipped
- **Bugs filed:** BUG-000, BUG-000
- **Verdict:** pass / fail
```

## Rules

- **Test behaviour, not implementation.** A test that breaks on a refactor with
  no behaviour change is a bad test and QA should say so at review.
- **Green means green.** "Passing except the flaky one" is a fail. A flaky test
  is filed as a P2 bug with its own ticket, and quarantined — never deleted
  quietly.
- **Every bug fix ships with the regression test that would have caught it.**
  QA verifies the test fails against the old code before accepting the fix.
- **No test hits production, sends real mail, charges a real card, or calls a
  real model endpoint.** Mock at the boundary.
- **Test data is synthetic.** Never a production dump, never real PII.
