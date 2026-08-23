# Lead Backend Engineer — Skills

This agent implements. Most of its work is direct code authoring against the
architect's design rather than a named skill.

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/test-authoring/SKILL.md` | alongside every implementation | sonnet | Write the tests that cover the code just written |

## Call graph

```
sub-ticket → `building` (assigned by eng-manager after work-breakdown)
  └── backend
        ├── reads: agents/architect/designs/{ENG-NNN}-{slug}.md   (what to build)
        ├── reads: agents/product-manager/specs/{ENG-NNN}-{slug}.md (why)
        ├── reads: agents/eng-manager/config/engineering-standards.md (how)
        ├── reads: the project's own conventions and surrounding code
        ├── branches: {type}/{ENG-NNN}-{slug}   (except an internal-lane project
        │     — in-tree on `main`, rollback named as a commit range; see projects.md)
        ├── implements + test-authoring (tests written with the code, not after)
        ├── runs: lint, typecheck, build, and the suite locally
        ├── writes: PR description (what / what not / uncertainties / review focus)
        └── → state `in-review`, owner principal-engineer

review or security or qa returns the ticket
  └── backend fixes the named finding, re-runs the suite, returns it to the
      gate that failed it — never to a later gate
```

## Requests out

| Need | Goes to | With |
|---|---|---|
| Schema or migration | `database` | What to store, query patterns, volume, growth |
| API contract agreement | `frontend` | Request/response/error shape, status codes |
| Design is wrong or silent on something material | `eng-manager` → `architect` | The specific question, not a guess |
| New dependency | `security` (via the gate) | Justification: what it does, why not stdlib, maintenance status |
