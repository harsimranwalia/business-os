# Database Expert — Skills

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/schema-change/SKILL.md` | design has `touches_data: true` | opus | Schema design, migration plan, rollback, and the migration gate |

## Call graph

```
design has touches_data: true
  └── schema-change (design phase — runs with the architect)
        ├── reads: agents/architect/designs/{ENG-NNN}-{slug}.md (intent + constraints)
        ├── asks: row count, growth, query frequency, read/write ratio, cardinality
        ├── reads: the project's existing schema and migration history
        ├── writes: agents/database/migrations/{ENG-NNN}-{slug}.md
        │     — schema change, indexes, expand/contract sequence,
        │       runtime estimate, lock profile, backfill batching, rollback
        └── → the migration file in the project's own migration directory

sub-ticket → `building` (schema work)
  └── database
        ├── writes the migration in the project's migration dir
        ├── tests forward and rollback against synthetic data at realistic volume
        └── → state `in-review`, owner principal-engineer

migration gate (before release, dispatched by eng-manager)
  └── database
        ├── verifies: backup taken and verified (destructive changes)
        ├── verifies: rollback tested, runtime estimated, locks acceptable
        ├── verifies: schema and code can coexist across the deploy
        └── pass → continues to `in-security` / `ready-to-ship`
            fail → state `building`, owner database, with the specific failure named

restore verification (every 90 days, surfaced in the weekly report)
  └── database
        └── writes: agents/database/notebook/{date}-restore-verification.md
```

## Contract with backend

Backend requests a data change; it never writes one. The request carries what to
store, how it will be queried, expected volume, and growth rate. This agent
designs the schema, owns the migration, and owns the gate — including the
authority to say the request should be satisfied a different way.
