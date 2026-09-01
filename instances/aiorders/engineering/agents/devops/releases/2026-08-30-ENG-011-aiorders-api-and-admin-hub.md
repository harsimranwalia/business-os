---
ticket: ENG-011
project: aiorders-api + aiorders-admin-hub (one ticket, two repos — first on this board)
released: 2026-08-30T00:12:50Z (api) / 2026-08-30T00:13:30Z (admin-hub)
released_by: devops
autonomy: L1 (both)
gate_g3: n/a — L1 merge, no G3 on this lane
commit: aiorders-api PR #3 (MERGED) | aiorders-admin-hub PR #3 (MERGED), branch `feat/ENG-011-client-stage-health-visibility` on both
environment: production (Supabase bmnmnejwdxbcqinqkwko + Cloudflare Pages admin-portal). Both merges confirmed; live-deploy status of either side is unknown from this worktree. See Health note.
rollback_tested: n/a — no schema rollback needed (one additive aggregate column via function replacement, no destructive migration); frontend side is a pure UI addition
health_check: not checked — no monitoring/dashboard access to either Supabase or Cloudflare from this department; see Health note
cost_delta_monthly: 0
---

# Release — Client stage & health visibility on the Brands admin page

## What shipped

Admin staff can see each restaurant's client stage and a minimal health
signal on the Brands page, and filter the list by stage.

- `aiorders-api`: derives `stage`/`health` on the existing admin brands-list
  response; extends `calculate_platform_analytics()` with one additional
  aggregate column (`last_order_at`). No new table, no new vendor.
- `aiorders-admin-hub`: adds a Stage column, a Health column, and a stage
  filter to `Brands.tsx`, following the page's existing filter pattern.

## Merge

The tracked merge-request item (`inbox/2026-08-29-eng011-merge-request.md`)
told the approver a reply wasn't required — "merge whenever suits you on
GitHub directly... the next build-loop pass detects each merge itself." None
came (`decision:` still empty); the approver merged both PRs directly
instead, 40 seconds apart. Confirmed independently on both repos before
treating the ticket as shippable — one repo merging alone would not have been
enough, this being the board's first multi-repo ticket:

```
$ git merge-base --is-ancestor origin/feat/ENG-011-client-stage-health-visibility origin/main   # aiorders-api
YES ancestor
$ gh pr view 3 --repo harsimranwalia/aiorders-api --json state,mergedAt
{"state":"MERGED","mergedAt":"2026-08-30T00:12:50Z"}

$ git merge-base --is-ancestor origin/feat/ENG-011-client-stage-health-visibility origin/main   # aiorders-admin-hub
YES ancestor
$ gh pr view 3 --repo harsimranwalia/aiorders-admin-hub --json state,mergedAt
{"state":"MERGED","mergedAt":"2026-08-30T00:13:30Z"}
```

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Migration | pass, named gap (no live Postgres; verified by reading + read-only live-catalog check) | database | 2026-08-29 |
| Code review | pass | principal-engineer | 2026-08-29 |
| Quality | pass (12/12 tests, clean builds both repos) | qa | 2026-08-29 |
| Security | pass | security | 2026-08-29 |
| G3 | n/a — L1 lane has no G3; the PR merges are the human gate | approver | 2026-08-30 |

## Deploy

- **Method:** merge to `main` only on both repos — no CI/CD auto-deploy
  exists on either (`.github/workflows/` absent from both `origin/main`s).
- **Why this department didn't run it:** both projects are registered **L1**
  — a human merges, and running either deploy would push a production release
  outside this department's own autonomy. Neither worktree has the
  credentials to do so anyway (no `SUPABASE_ACCESS_TOKEN`; no Cloudflare
  token — `deploy-cf` is a manual `wrangler` invocation, not push-triggered).
- **What actually happened:** unknown from here on both sides. No deploy
  evidence exists for either repo, unlike `ENG-006`'s confirmed separate
  Supabase push. Recorded as unknown, not inferred.
- **Migration:** additive (function signature extension only, no new table).
- **Feature flag:** none — both directions degrade gracefully to a `-` cell
  per the design, so nothing needs to stay dark.
- **Duration:** n/a — no deploy run by this department.

## Verification

- `git diff` against each reviewed branch tip vs. its own `origin/main`:
  empty on both repos — the merged trees are byte-identical to what passed
  review/QA/security, so the 12/12 test result and clean builds already
  documented at `in-review` still hold; not re-run against identical source.
- `git ls-tree` confirms the reviewed files (API handler extension,
  `Brands.tsx` changes) are present on both `origin/main`s under the
  reviewed paths.
- Health checks: not run — see `health_check` above.
- Acceptance criteria: 5 of 6 confirmed against the merged trees, 1 carries a
  pre-existing named gap — see below.

## Acceptance criteria

Re-checked against both `origin/main`s (`agents/product-manager/specs/ENG-011-client-stage-health-visibility.md`):

1. Each Brands row shows current stage. **Pass** — unit-tested, unchanged on
   merged tree.
2. Stage alone tells staff "is this a client." **Pass** — same field, no
   separate indicator needed by design.
3. Stage filter shows only matching restaurants. **Pass** — unit-tested.
4. Clearing the filter returns the full list. **Pass** — unit-tested.
5. Health indicator shown from existing order activity. **Not verified
   live** — no live Brands-page load or frontend session was exercised
   pre-merge (host has no Docker/psql/supabase CLI; admin-hub worktree has no
   `.env`), a gap QA and security both already named at their own gates, not
   newly discovered here and not closeable from this department post-merge.
6. Non-staff requests rejected by the existing admin-portal authz gate.
   **Pass** — security-reviewed, no new input surface.

**AC5 is the one open item, carried forward rather than hidden** — same
"named at the gate, not silently claimed" standard `ENG-006` applied to its
own OTP-dependent ACs. Worth a post-merge smoke check per the merge-request
item's own "Named gaps" section, whenever this department or the approver
next has a live session against either project.

## Rollback

- **Path:** `aiorders-api` — revert `calculate_platform_analytics()` to its
  prior signature (no data migration, function replacement only).
  `aiorders-admin-hub` — revert the `Brands.tsx` diff; no schema, no stored
  state introduced.
- **Tested:** n/a — no destructive or stateful migration exists to drill
  against a throwaway container.
- **Used:** no.

## Health note

No dashboard/monitoring access to either `bmnmnejwdxbcqinqkwko` (Supabase) or
the Cloudflare Pages project behind admin-portal, from this department's
worktrees. Unlike `ENG-006`, no separate deploy evidence exists for either
side — both live-deploy status and runtime health are unknown here, on both
repos.

## Observability

No new logging surface — `stage`/`health` are derived, read-only fields on an
existing response; failures degrade to a `-` cell per the design rather than
throwing. Not independently exercised against a live deploy.

## Cost

$0/month delta — no new tables, no new service, one additional aggregate
column and one additional UI column.

## Follow-ups

AC5 (health indicator) needs a live Brands-page smoke check once this
department or the approver has a session against either live environment —
the one gap this release carries forward, already named at QA/security and
not new here. KV read fan-out (one Cloudflare KV GET per brand row) is
unbatched, non-blocking, already named at code review.
