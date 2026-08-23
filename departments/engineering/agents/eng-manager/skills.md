# Engineering Manager — Skills

Skills this agent invokes directly. Specialist skills are invoked by the agent
that owns the state — see each agent's `skills.md`.

| Skill | Trigger | Model | Purpose |
|---|---|---|---|
| `skills/work-breakdown/SKILL.md` | ticket enters `ready` | sonnet | Tech design → sub-tickets, sequence, assignments |
| `skills/repo-onboarder/SKILL.md` | the approver names a new repo | sonnet | Scan a repo, draft its project card, propose an autonomy level |

## Call graph

```
eng_build_loop (weekdays 09:30 + 15:30)
  ├── product-manager — business intake (the front door)
  │     └── agents/product-manager/inbox/ + requests filed in inbox/requests/ tagged `eng`
  │           └── prd-writer → ticket at `intake` → PRD → G1 → hands to the EM
  │
  └── eng-manager (this agent) — delivery
        ├── reads: MODE from .env → exit on sabbath/retreat
        ├── reads: config/projects.md, config/definition-of-done.md
        ├── technical intake sweep — agents/eng-manager/inbox/
        │     (qa bugs, security findings, devops incidents, architect debt →
        │      one line in proposals.md, NOT a ticket. Batched G1 in the weekly
        │      report; only what the approver approves is built. Exception: a
        │      P0 on a project outside the internal lane tickets immediately.)
        ├── gate returns: reads inbox/ for answered items
        │     ├── G1 answered → the PM's ticket enters delivery here
        │     ├── G2 / G3 → advances or kills the ticket
        │     ├── L1 merge request → see merge detection below
        │     └── approved project card → appended to config/projects.md
        ├── merge detection: for tickets blocked on an L1 PR, `git fetch` then
        │     check branch-head ancestry against the default branch. Merged →
        │     `shipped`. Local git only, no API call.
        └── dispatch — each ticket runs forward through consecutive machine
              states, stopping at a human, new implementation work, or a failed
              gate (max 4 transitions per ticket per pass):
              ├── designed      → architect        (tech-design)
              ├── ready         → work-breakdown → backend / frontend / database
              ├── building      → backend / frontend / database   ← pass stops here
              ├── in-review     → principal-engineer (code-review-gate)
              ├── in-qa         → qa               (test-authoring, bug-triage)
              ├── in-security   → security         (security-gate)
              ├── ready-to-ship → devops           (release-runner)
              ├── shipped       → product-manager  (acceptance-check)
              ├── verified      → eng-manager: close, notebook, proof entry
              └── advised       → L0 terminal: advisory package → inbox/

eng_weekly_report (Sun 18:30)
  └── eng-manager
        ├── reads: board/, agents/qa/bugs/_index.md, agents/devops/releases/
        ├── reads: every department notebook (this week's entries only)
        └── writes: reports/engineering-{YYYY-WXX}.md   # terminal for now — the approver reads it or doesn't

repo onboarding (approver-triggered, never scheduled)
  └── repo-onboarder
        ├── scans: the named repo — stack, test/lint/build commands, CI, conventions
        └── writes: project card → inbox/ for the approver's approval
              └── on approval: appended to config/projects.md at L1
```

## Handoff contract

Every dispatch hands the receiving agent exactly three things: the ticket file,
the artifacts linked in its frontmatter, and the state it must reach. The
receiving agent writes its own artifact, updates `state` and `owner` on the
ticket, and appends one line to the ticket log. Nothing is handed off verbally,
and nothing is handed back without a written verdict.
