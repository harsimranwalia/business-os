# Skill: test-authoring

**Owner:** qa (also invoked by backend and frontend alongside implementation)
**Model:** sonnet
**Trigger:** by an engineer while implementing; by qa when a ticket enters `in-qa`
**Suppressed when:** sabbath, retreat

---

## Purpose

Write tests that fail for the right reasons. Behaviour, not implementation;
failure paths, not just the happy one.

---

## Inputs

- `agents/product-manager/specs/{ENG-NNN}-{slug}.md` — the acceptance criteria (required)
- `agents/architect/designs/{ENG-NNN}-{slug}.md` — what can break
- `agents/qa/test-plans/{ENG-NNN}.md` — when qa is running this (written first)  <!-- eng-receipt-exception: QA's plan is written before the gate runs; the pass-verdict-only rule does not apply to it -->
- The project's existing test suite — its patterns, helpers, and fixtures
- `agents/qa/notebook/` — escaped defects, so the gaps get closed

---

## Steps

### 1. Mode check

`sabbath` or `retreat`: exit.

### 2. Match the project's test conventions

Read three existing tests before writing one. Match the framework, the naming,
the fixture style, the assertion style. A test suite with two conventions is a
suite people stop trusting.

### 3. When run by qa: write the test plan first

`agents/qa/test-plans/{ENG-NNN}.md` from the template — one row per acceptance
criterion, before authoring anything. A criterion you can't write a test for
goes back to the PM through the EM to be rewritten. Never quietly test something
adjacent instead.

### 4. One test per acceptance criterion

Named so the failure output says what broke in domain terms. `test_declines_
order_when_menu_item_unavailable`, not `test_order_2`.

Assert on observable behaviour — return values, state changes, emitted events,
what the user sees. Never on internal call counts or private structure. A test
that breaks on a refactor with no behaviour change is a bad test and will teach
the team to ignore red.

### 5. Then the failure paths — the part that matters

For every change, work through the ones that apply:

| Scenario | What to assert |
|---|---|
| Invalid input at the boundary | Rejected cleanly, nothing written |
| Missing or malformed field | Clear error, no partial state |
| Empty collection / zero / null | Handled, not crashed |
| Maximum or oversized input | Bounded, not unbounded work |
| Unauthorised caller | Denied — **and this case must exist**, per the security baseline |
| Wrong tenant or wrong role | Denied, no data leak |
| Downstream timeout or 500 | Bounded retry, then a clean failure |
| Duplicate or replayed request | Idempotent, no double effect |
| Concurrent write to one record | No lost update |
| Model returns malformed / empty / confidently wrong output | Defined, tested behaviour |

### 6. Regression tests

Every bug fix gets a test that **fails against the old code**. Write it, check
out the pre-fix code, watch it fail, then restore. QA verifies this
independently at the gate — the engineer's word is not the verification.

### 7. Keep the boundaries clean

No test touches production, sends real email, charges a real card, or calls a
real model endpoint. Mock at the boundary, not three layers in. Test data is
synthetic — never a production dump, never real PII.

### 8. Update the plan

Fill in the test name and status for each row. Rows still empty are the coverage
gap, and the gate reads this table.

---

## Outputs

| File | Purpose |
|---|---|
| Project test files | The tests |
| `agents/qa/test-plans/{ENG-NNN}.md` | Coverage table filled in |  <!-- eng-receipt-exception: QA's plan is written before the gate runs; the pass-verdict-only rule does not apply to it -->

---

## Trace

`traces/qa-{run-id}.json` — ticket, tests written by level, criteria covered,
gaps remaining.

---

## Failure modes to avoid

- **Testing implementation.** Mock counts and private-method assertions are
  future rework.
- **Happy path only.** The failure table above is the actual job.
- **A test that cannot fail.** Confirm it fails before you make it pass.
- **Skipping the negative authz case.** Proving the authorised user gets in
  proves nothing about the ones who shouldn't.
- **Inventing a criterion** because the PRD's was untestable. Send it back.
