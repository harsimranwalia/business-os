# Lead Frontend Engineer — Skills

This agent implements. Most of its work is direct code authoring against the
architect's design rather than a named skill.

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/test-authoring/SKILL.md` | alongside every implementation | sonnet | Component and interaction tests for the code just written |

## Call graph

```
sub-ticket → `building` (assigned by eng-manager after work-breakdown)
  └── frontend
        ├── reads: agents/architect/designs/{ENG-NNN}-{slug}.md
        ├── reads: agents/product-manager/specs/{ENG-NNN}-{slug}.md (acceptance criteria)
        ├── reads: agents/eng-manager/config/engineering-standards.md
        ├── reads: the project's component patterns and existing conventions
        ├── confirms: the API contract with backend (agreed in the design)
        ├── branches: {type}/{ENG-NNN}-{slug}   (except an internal-lane project
        │     — in-tree on `main`, rollback named as a commit range; see projects.md)
        ├── implements every required state + test-authoring
        ├── runs: lint, typecheck, build, suite, and an accessibility pass
        ├── writes: PR description (states covered, perf delta, review focus)
        └── → state `in-review`, owner principal-engineer

review or security or qa returns the ticket
  └── frontend fixes the named finding and returns it to the gate that failed it
```

## Requests out

| Need | Goes to | With |
|---|---|---|
| API contract change | `backend` via the design | The shape needed and why the current one doesn't work |
| Copy for a user-facing surface | `eng-manager` → the project's brand owner | Where it appears and the constraint (length, tone) |
| Design silent on a state | `eng-manager` → `architect` | The specific state and the question |
