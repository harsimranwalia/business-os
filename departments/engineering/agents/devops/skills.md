# AI Ops + CloudOps Engineer — Skills

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/release-runner/SKILL.md` | ticket enters `ready-to-ship` | sonnet | Readiness gate, deploy per autonomy level, verify, write the release record |

## Call graph

```
ticket → `ready-to-ship` (dispatched by eng-manager after the security gate)
  └── release-runner
        ├── reads: agents/eng-manager/config/projects.md (autonomy level)
        ├── reads: MODE from .env (window check: sabbath/retreat) + ENG_RELEASE_FREEZE
        ├── checks the readiness gate:
        │     ├── rollback tested (not theorised)
        │     ├── observability on the new path
        │     ├── recurring cost known and CFO notified if above $0
        │     └── release window open
        ├── fail → state `building` or `blocked`, with the specific reason
        ├── pass + autonomy L1        → open PR, state `blocked` on the human merge
        │     pass + autonomy L2      → G3 to the approver via eng-manager → inbox/
        │     pass + autonomy L3      → deploy, notify the approver after
        ├── deploys, runs the migration (database's plan), verifies health
        ├── writes: agents/devops/releases/{YYYY-MM-DD}-{project}-{ENG-NNN}.md
        └── → state `shipped`, owner product-manager (acceptance verification)

incident (any time)
  └── devops
        ├── stabilise → assess → communicate once → diagnose
        ├── writes: agents/devops/incidents/{YYYY-MM-DD}-{slug}.md (same day)
        ├── files: follow-up tickets → agents/eng-manager/inbox/
        └── P0 (down / data loss / security exposure) → interrupt via eng-manager

model ops sweep (weekly, inside eng_weekly_report)
  └── devops
        ├── checks: latency, failure rate, malformed-output rate, token spend
        ├── runs: the eval sets for model-backed features
        └── writes: agents/devops/notebook/{date}-model-ops.md
```

## Cost reporting

Every release with a recurring cost above $0/month reaches the CFO through the
EM **before** it ships. The weekly report carries the running total per project.
The approver finding out about new spend from a bill is a system failure, and
this is the mechanism that prevents it.
