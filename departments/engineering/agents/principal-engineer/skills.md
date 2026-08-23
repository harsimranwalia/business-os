# Principal Engineer — Skills

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/code-review-gate/SKILL.md` | ticket enters `in-review` | opus | The blocking code review — correctness, simplicity, standards |

## Call graph

```
ticket → `in-review` (dispatched by eng-manager after `building`)
  └── code-review-gate
        ├── reads: board/{ENG-NNN}-{slug}.md (ticket + design links)
        ├── reads: agents/architect/designs/{ENG-NNN}-{slug}.md
        ├── reads: agents/eng-manager/config/engineering-standards.md
        ├── reads: the project's own conventions (CLAUDE.md / AGENTS.md / style config)
        ├── reads: the full diff on the branch
        ├── scans: automatic-failure list first — any hit fails immediately
        ├── writes: verdict + findings into the ticket's `review:` block
        └── pass → writes: agents/principal-engineer/reviews/{ENG-NNN}.md — the
                     receipt, written on a `pass` verdict ONLY; sets links.review
                     in the same write. Then state `in-qa`, owner qa
            fail → state `building`, owner the implementing engineer.
                   NO receipt file — the `review:` block and the reviewer's
                   notebook are the whole record
                   (3 failed rounds → back to architect via EM)

three occurrences of the same correction
  └── edits: agents/eng-manager/config/engineering-standards.md
        └── notifies eng-manager → noted in the weekly report
```

## What this gate does not do

- It does not check coverage — `qa` owns that.
- It does not run the test suite — `qa` runs it.
- It does not do the security review — `security` owns that, and a `pass` here
  says nothing about a security verdict.
- It does not check the migration — `database` owns that gate.

Four separate gates, four separate owners, no agent overriding another. A change
that passes review and fails security is a normal outcome, not a contradiction.
