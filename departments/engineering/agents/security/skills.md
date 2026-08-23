# Security Expert — Skills

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/security-gate/SKILL.md` | ticket enters `in-security` | opus | OWASP + LLM + secrets + dependency review; the blocking verdict |

## Call graph

```
ticket → `in-security` (dispatched by eng-manager after the quality gate)
  └── security-gate
        ├── reads: agents/eng-manager/config/security-baseline.md (the standard)
        ├── reads: agents/architect/designs/{ENG-NNN}-{slug}.md (trust boundaries)
        ├── reads: the full diff, and the branch history for secrets
        ├── reads: agents/qa/test-plans/{ENG-NNN}.md (are the negative authz cases tested?)
        ├── walks: OWASP A01–A10, each applicable or n/a with a reason
        ├── walks: the LLM checklist if the change touches a model, agent, tool, MCP, or RAG
        ├── scans: secrets (diff + history), dependencies (CVE, licence, maintenance)
        └── pass → writes: agents/security/reviews/{ENG-NNN}.md — the receipt,
                     written on a `pass` verdict ONLY; sets links.security_review
                     in the same write. Then state `ready-to-ship`, owner devops
            fail → state `building`, owner the implementing engineer,
                   with category, severity, location, exploit path, and the exact
                   fix — into the ticket log and
                   agents/security/notebook/{date}-findings.md. NO receipt file
            risk acceptance → state `blocked`, owner eng-manager,
                   blocked_from: in-security. NO receipt file — an accepted risk
                   is an ADR plus a later `pass`, not a gate that cleared

eng_security_sweep (Sun 07:00)
  └── security
        ├── scans: dependency CVEs across every project in config/projects.md
        ├── scans: secrets across registered repos
        ├── checks: SOC 2 control drift, aged findings past SLA
        ├── files: findings as tickets → agents/eng-manager/inbox/   (no approver involvement)
        └── writes: agents/security/notebook/{date}-sweep.md

leaked credential found (any time)
  └── P0 → interrupt via eng-manager
        └── rotate, then remove from history, then write the incident up with devops

three occurrences of the same finding class
  └── proposes: addition to agents/eng-manager/config/engineering-standards.md
        └── enforced thereafter by principal-engineer at code review
```

## What a `fail` costs

The release waits. That is the intended cost and it is not negotiable by any
agent, including the EM. Only the approver can accept a risk — presented as
finding, exploit path, blast radius, cost to fix, cost to accept — and their
answer is recorded as an ADR, not as a passing verdict.
