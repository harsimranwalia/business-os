# Approver QA Engineer — Skills

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/test-authoring/SKILL.md` | ticket enters `in-qa` | sonnet | Write the plan's missing tests — integration, e2e, failure paths |
| `skills/test-suite-run/SKILL.md` | after authoring, and on demand | haiku → sonnet | Run the suite, parse results, escalate to sonnet only on failures |
| `skills/bug-triage/SKILL.md` | any failure or reported defect | sonnet | File the bug, set severity from the definition, assign an owner |

## Call graph

```
ticket → `in-qa` (dispatched by eng-manager — runs CONCURRENTLY with code review,
                  since both read the same diff and neither depends on the other.
                  If review fails, this round's result is discarded: the code is
                  about to change anyway.)
  └── qa
        ├── reads: agents/product-manager/specs/{ENG-NNN}-{slug}.md (acceptance criteria)
        ├── reads: agents/architect/designs/{ENG-NNN}-{slug}.md (what can break)
        ├── writes: agents/qa/test-plans/{ENG-NNN}.md   ← before authoring anything  <!-- eng-receipt-exception: QA's plan is written before the gate runs; the pass-verdict-only rule does not apply to it -->
        ├── reviews: the engineer's own tests (behaviour vs implementation)
        ├── test-authoring → the plan's missing tests
        ├── test-suite-run → full suite, real numbers into the plan
        ├── failures?
        │     └── bug-triage → agents/qa/bugs/{BUG-NNN}-{slug}.md
        │           ├── severity from definition-of-done.md, never negotiated
        │           ├── owner assigned (never empty while open)
        │           └── → state `building`, owner the assigned engineer
        └── pass → state `in-security`, owner security

bug fix returns
  └── qa verifies the regression test fails against the OLD code, then re-runs

production defect reported (from devops or the approver)
  └── bug-triage → filed with found_in: production
        └── P0 → interrupt via eng-manager; everything else → next build-loop pass
```

## The gate

`pass` requires all four: suite green, every acceptance criterion covered by a
passing test, every bug fix carrying a verified regression test, and no open
P0/P1 on the ticket. Three out of four is a fail.
