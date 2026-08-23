# Release record template

Written by `devops` at `agents/devops/releases/{YYYY-MM-DD}-{project}-{ENG-NNN}.md`,
after the deploy, not before. This is the change-management evidence a SOC 2
control wants, and the first thing anyone reads during an incident.

```markdown
---
ticket: ENG-000
project: <project>
released: YYYY-MM-DDTHH:MM
released_by: devops
autonomy: L1              # the project's level at release time
gate_g3: auto             # auto (L3) | approver-approved YYYY-MM-DD
commit:                   # the deployed SHA
environment: production
rollback_tested: true
health_check: green       # green | degraded | rolled-back
cost_delta_monthly: 0     # $/month this release adds. Non-zero → CFO notified
---

# Release — {Title}

## What shipped

One paragraph, in terms a non-engineer understands. This is the line that ends
up in the weekly report.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass | principal-engineer | |
| Migration | pass / n/a | database | |
| Quality | pass | qa | |
| Security | pass | security | |
| Release readiness | pass | devops | |
| G3 | approved / auto | approver / — | |

## Deploy

- **Method:** {how — push to main, Vercel deploy, cron install, migration run}
- **Migration:** applied / none. Runtime: {n}s. Rows touched: {n}
- **Feature flag:** on / off / none
- **Duration:** start → healthy

## Verification

- Health checks: {what was checked, and the result}
- Acceptance criteria: verified by product-manager on {date}
- Error rate and latency vs. the hour before: {delta}

## Rollback

- **Path:** the exact command or steps
- **Tested:** how and when — before the deploy, not theoretically
- **Used:** no / yes, at {time}, because {reason}

## Observability

What is now watched on this path, and where a failure shows up. If the answer is
"nothing", this release should not have passed the readiness gate.

## Cost

Recurring delta in $/month and what drives it. Anything above zero goes to CFO
before the release, not after.

## Follow-ups

Anything deliberately deferred, as ticket IDs. Empty is a valid and good answer.
```

## Rules

- **Written after the deploy, from what actually happened** — not copied from
  the plan. A record that matches the plan exactly, every time, is not being
  written honestly.
- **A rollback that was never tested is not a rollback.** The readiness gate
  fails without one.
- **No release record, no `shipped` state.** The ticket cannot advance.
- **Non-zero recurring cost reaches CFO before release.** The approver
  finding out about new spend from a bill is a system failure.
- **On a project registered internal, "released" means merged to main *and*
  the routine actually fired.** A cron that never runs is a failed deploy —
  verify the first fire.
