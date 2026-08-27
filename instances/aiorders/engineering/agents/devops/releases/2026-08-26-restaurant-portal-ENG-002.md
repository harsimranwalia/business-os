---
ticket: ENG-002
project: restaurant-portal
released: 2026-08-26T15:40
released_by: devops
autonomy: L1
gate_g3: n/a — L1 merge, no G3 on this lane
commit: 2703add08 (merged via b3a81ef, PR #1)
environment: production (static site host; see Deploy note — nothing newly deployed)
rollback_tested: true
health_check: green
cost_delta_monthly: 0
---

# Release — Add a smoke-test harness to restaurant-portal

## What shipped

`restaurant-portal` now has a real, runnable test command (`npm run test` →
`vitest run`) and one smoke test that renders the actual app and fails if the
build breaks or the login route stops working. It's the first real test on
any AIOrders repo, and it means the department's quality gate on this repo
now proves something instead of producing an honest-but-empty "no suite"
receipt.

## Merge

The approver merged PR #1 directly on GitHub rather than replying in the
tracked gate item (`inbox/2026-08-26-eng002-merge-request.md`, `## Decision`
still literally unfilled) — recorded on the ticket by a direct dashboard
("control center") edit setting `state: shipped` ahead of any build-loop pass,
with ancestry explicitly not consulted at that time. This pass independently
verified the merge itself, from scratch, rather than trusting that edit:

```
$ git fetch origin
   33c5de6..b3a81ef  main -> origin/main
$ git merge-base --is-ancestor chore/ENG-002-smoke-test-harness origin/main
RESULT: MERGED
$ git log origin/main --oneline -3
b3a81ef Merge pull request #1 from harsimranwalia/chore/ENG-002-smoke-test-harness
2703add Add Vitest smoke-test harness
33c5de6 Add hidden flag to menu items
```

`origin/main`'s tip (`b3a81ef`) has no commits beyond this PR's own merge
since the branch was cut, so its tree is byte-identical to the branch tip —
confirmed via `git diff` between the two, empty. The control center's claim
checks out.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass | principal-engineer | 2026-08-26 |
| Migration | n/a — no schema change | database | — |
| Quality | pass (1/1 suite) | qa | 2026-08-26 |
| Security | pass | security | 2026-08-26 |
| Release readiness | pass | devops | 2026-08-26 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-08-26 |

## Deploy

- **Method:** merge to `main` only. `restaurant-portal` has no CI/CD wired to
  `main` (`.github/workflows/` doesn't exist; `wrangler.toml` + the
  repo's own `deploy-cf` script — `wrangler pages deploy dist
  --project-name=brand-portal` — is a manual, explicitly-invoked step, not a
  push-triggered one). Confirmed by reading both directly this pass, not
  assumed from the ticket's earlier framing.
- **Why no deploy run:** the entire change is a `devDependency`-only addition
  (`vitest`, React Testing Library) plus test files. Neither is imported by
  any file the app's entry point reaches, so Vite's build graph excludes them
  by construction — verified directly this pass by running `npm run build`
  against the merged tree and reading the output: `dist/index.html`,
  `dist/assets/index-*.css`, `dist/assets/index-*.js` only, same shape as
  before this ticket. There is no new production artifact to deploy, so
  `npm run deploy-cf` was deliberately not run — running it would push a
  production deploy that isn't part of this ticket's approved scope for no
  behavioural change.
- **Migration:** none.
- **Feature flag:** none — not applicable to a dev-tooling change.
- **Duration:** n/a — no deploy executed.

## Verification

Re-run independently against the actual merged tree in the department's own
worktree (`~/Documents/projects/_eng/restaurant-portal`, tree confirmed
identical to `origin/main` by empty `git diff` — the human's own checkout at
`~/Documents/projects/aiorders/restaurant-portal` was not touched):

- `npm test` → 1 passed, 0 failed, 0 skipped
- `npm run build` → succeeds, `dist/` shape unchanged (see Deploy note)
- Health checks: no live endpoint or runtime behaviour changed by this
  release, so "green" here means what the readiness gate already
  established — nothing that could go newly unhealthy. No production traffic
  was touched.
- Acceptance criteria: verified by product-manager on 2026-08-26 — see the
  ticket log and `agents/qa/test-plans/ENG-002.md` (AC3 updated from
  `pending` to `pass` this pass, now that `config/projects.md`'s Commands
  table edit is confirmed live on disk).
- Error rate / latency vs. the hour before: not applicable — no traffic-facing
  change, nothing was deployed to compare.

## Rollback

- **Path:** revert `2703add` on `main` (a single, self-contained commit —
  `package.json`, `package-lock.json`, `vite.config.ts`, `src/App.test.tsx`,
  `src/test/setup.ts`).
- **Tested:** the implementing pass verified the test goes red on a broken
  entry route and green again on revert, byte-identical, before ever
  committing (see the ticket's `building` log entry). A revert of the merge
  commit itself was not separately dry-run, since there is no deployed
  artifact a rollback needs to undo.
- **Used:** no.

## Observability

Nothing new is watched, because nothing new runs in production — the only
thing this release changes is what `skills/test-suite-run/SKILL.md` executes
on future `restaurant-portal` tickets. That skill's own pass/fail output *is*
the observability this ticket exists to create. If a future change to this
repo breaks silently, the suite going red on the next ticket's `in-qa` hop is
the mechanism, not a monitoring dashboard.

## Cost

$0/month — a dev-time test runner, no new runtime dependency, no new
infrastructure. No cost notice owed.

## Follow-ups

None committed by this ticket. `aiorders-api` (Deno, no `package.json`) and
the three other frontends still have no test command — each would need its
own ticket, not promised here (see the PRD's Non-goals).
