# Project Registry — AIOrders

Every repo this instance's engineering team is allowed to touch, and how far it
may go. **If a repo is not in this table, the team does not touch it.** Adding
one is the approver's call — run `skills/repo-onboarder/SKILL.md`.

## Autonomy levels

| Level | Means |
|---|---|
| **L0** observe | Read and propose only. Never writes code, never opens a PR. |
| **L1** branch | Writes on a branch, opens a PR after all machine gates pass. A human merges. |
| **L2** merge | Merges to main once all machine gates pass. The approver approves releases (G3). |
| **L3** ship | Deploys to production after gates. The approver is notified after, not asked before. |

Autonomy belongs to the project, never the ticket. **New projects register at L1,
never higher.** Only the approver raises a level.

## Registered projects

All five carried over from the life-os registry where they were approved
2026-07-28, and **re-verified against the working trees on 2026-08-23** — branch,
remote, and available npm scripts were read from disk rather than trusted from
the old table.

| Project | Repo path | Stack | Deploy target | Autonomy | Notes |
|---|---|---|---|---|---|
| `aiorders-api` | `~/Documents/projects/aiorders/aiorders-api` | Supabase edge functions (Deno/TS) | Supabase (`bmnmnejwdxbcqinqkwko`) | **L1** | **Highest blast radius of the set** — shared backend for all four frontends. No `package.json`, so no npm test target exists. Default branch `main`. |
| `aiorders-admin-hub` | `~/Documents/projects/aiorders/aiorders-admin-hub` | Vite + Cloudflare Workers | Cloudflare (`deploy-cf`) | **L1** | Default branch `main`. **64 uncommitted files in the human checkout as of 2026-08-23** — active WIP the department cannot see. Expect merge friction. |
| `config-site-builder` | `~/Documents/projects/aiorders/config-site-builder` | Vite + Cloudflare Workers | Cloudflare (`deploy-cf`, `deploy-all`) | **L1** | Default branch `main`. |
| `restaurant-marketplace` | `~/Documents/projects/aiorders/restaurant-marketplace` | Vite + Cloudflare Workers | Cloudflare (`deploy-cf`) | **L1** | **Default branch is `master`, not `main`.** The only repo here with a `typecheck` script. 18 uncommitted files in the human checkout as of 2026-08-23. |
| `restaurant-portal` | `~/Documents/projects/aiorders/restaurant-portal` | Vite + Cloudflare Workers | Cloudflare (`deploy-cf`) | **L1** | Default branch `main`. Clean tree. |

All five remotes are under `harsimranwalia/`, so pull requests land in repos the
approver owns.

**Not registered, deliberately:** `GoogleMaps-Scraper`, `OpenWA`, `ringcentral`,
`twenty-crm` and anything else under `~/Documents/projects/aiorders/`. They sit in
the same parent directory but were never onboarded. The team does not touch them.

## Commands

How each project is verified. `skills/test-suite-run/SKILL.md` reads this when a
test plan carries no `suite_command` of its own. Read from each repo's own
`package.json` on 2026-08-23 — never guessed. An empty cell means the command
does not exist.

| Project | Test | Lint | Typecheck | Build |
|---|---|---|---|---|
| `aiorders-api` | — | — | — | — |
| `aiorders-admin-hub` | — | `npm run lint` | — | `npm run build` |
| `config-site-builder` | — | `npm run lint` | — | `npm run build` |
| `restaurant-marketplace` | — | `npm run lint` | `npm run typecheck` | `npm run build` |
| `restaurant-portal` | — | `npm run lint` | — | `npm run build` |

`aiorders-api` is empty across the board because it has no `package.json` at
all — it is Deno (Supabase edge functions), so whatever verification it gets
will be `deno test` / `deno lint` / `deno check` against a `deno.json` that does
not exist yet. That is a ticket, not a blank to fill in.

Four of the five have a working `build` and `lint`, which is more than nothing:
`skills/test-suite-run/SKILL.md` already treats lint, typecheck and build as
part of a run ("a green suite on code that doesn't build is not a pass"), so
those columns give the quality gate something real to enforce on day one even
before any test exists.

## No test command exists on any registered project

Verified 2026-08-23: none of the four `package.json` files defines a `test`
script, `aiorders-api` has no `package.json` at all, and a filesystem sweep finds
zero `*.test.*` or `*.spec.*` files outside `node_modules` in any of them.

This matters more than it looks. The `full` lane requires a QA test-plan receipt
and `skills/test-suite-run/SKILL.md` needs something to execute. A ticket that
reaches the quality gate here would produce a receipt file that proves nothing —
exactly the failure `skills/code-review-gate/SKILL.md` names in its own receipt
table, where a receipt written on a fail satisfies the check it was meant to
prove.

**So the first real ticket on this instance is a test harness**, not a feature.
This is the same position Verido-CRM was in, and it was solved there the same way
(ENG-002, smoke test harness) for the same stated reason: the app had no CI to
prove a change had not broken a route.

**Filed as `ENG-002` on this instance too, 2026-08-25** — shaped from the
approver's own request (`inbox/requests/2026-08-23-test-harness.md`, now
`inbox/_handled/`), scoped to `restaurant-portal`, awaiting G1. This
paragraph is now history, not an open gap — see the ticket rather than
re-deriving this note.

## Working copies — the department never touches a human's directories

```
~/Documents/projects/aiorders/{project}/   # the human's. Never touched by an agent.
~/Documents/projects/_eng/{project}/       # the department's worktree.
```

**All five worktrees already exist** under `~/Documents/projects/_eng/`, created
at the 2026-07-28 registration. Verified present 2026-08-23.

- The build loop refuses to run against a path that isn't under `_eng/`.
- Before any work: `git fetch`, then create the branch in the worktree.
- Uncommitted changes in the worktree at the start of a pass means a previous
  pass died mid-work. Stop and flag it. Never discard, never stash blindly.
