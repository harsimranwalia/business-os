---
ticket: ENG-011
project: aiorders-admin-hub
project_secondary: aiorders-api
released: 2026-08-30T01:43:13Z
released_by: devops
autonomy: L1 (both repos)
gate_g3: n/a — L1 merge, no G3 on this lane
commit: "aiorders-admin-hub: e12342d (merged via PR #3) | aiorders-api: eb2ed89 (merged via PR #3)"
environment: production. `aiorders-admin-hub` auto-deployed to Cloudflare Pages (GitHub Actions, confirmed by run status). `aiorders-api` has no CI/CD; its migration and the `admin-portal` edge function were pushed to the live Supabase project (`bmnmnejwdxbcqinqkwko`) out-of-band, outside this department's own L1 workflow — confirmed by reading live state via the Supabase MCP connection, not inferred. See Deploy note.
rollback_tested: "not live-drilled — no Docker/psql/supabase CLI on this build host. Reasoned pre-merge plus independently confirmed via a read-only Supabase MCP catalog check: `orders.created_at` is `timestamptz NOT NULL` as assumed, the live `calculate_platform_analytics` body (pre-migration) matched the rollback's restore target exactly, and neither `pg_depend` nor `cron.job` showed a dependent on the function's OID."
health_check: "not checked via a monitoring dashboard (no access — same standing gap as ENG-005/ENG-006) — but the deploy itself is independently confirmed, not assumed: see Verification."
cost_delta_monthly: 0
---

# Release — Client stage & health visibility on the Brands admin page (ENG-011)

## What shipped

Admin staff can see each restaurant's derived client stage and a minimal
health signal on the `aiorders-admin-hub` Brands page, and filter the list
by stage. `aiorders-api`'s `calculate_platform_analytics()` gained one
additive aggregate column (`last_order_at`); nothing else in its schema
changed. No new table, no new vendor, $0/month delta.

## Merge

Both PRs' own gate item (`inbox/_handled/2026-08-29-eng011-merge-request.md`)
carries `decision: approved`, `decided: 2026-08-30T01:43:13.118048+00:00`, and
a trailing "merged" note — a hand-edit, not a reply through
`lib/eng-notify.sh`'s channel, consistent with every gate on this instance but
`ENG-002`'s. **Not taken on the text alone** — independently re-derived via git
ancestry in this department's own worktrees, never the human's checkout:

```
$ cd _eng/aiorders-api && git fetch origin
$ git merge-base --is-ancestor origin/feat/ENG-011-client-stage-health-visibility origin/main
MERGED
$ git log --oneline -1 origin/main
93617c6 Merge pull request #4 from harsimranwalia/loyalty-system   # ENG-007, landed after ENG-011's own merge (eb2ed89), both ancestors

$ cd _eng/aiorders-admin-hub && git fetch origin
$ git merge-base --is-ancestor origin/feat/ENG-011-client-stage-health-visibility origin/main
MERGED
$ git log --oneline -1 origin/main
ceb9552 Scope deploy job to the Production environment
```

Both repos' branches confirmed merged. Per `eng_build_loop.md` step 5, a
multi-repo ticket ships only once every repo's branch has merged — both have.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Migration | pass, named gap (no live Postgres dry-run on this host) | database | 2026-08-29 |
| Code review | pass | principal-engineer | 2026-08-29 |
| Quality | pass, 12/12 tests | qa | 2026-08-29 |
| Security | pass | security | 2026-08-29 |
| Release readiness | pass | devops | 2026-08-29 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-08-29 |

## Deploy

- **`aiorders-admin-hub`:** a GitHub Actions Cloudflare Pages workflow did
  **not** exist at the moment PR #3 merged (`e12342d`) — it was added
  afterward, in two commits on top of it (`698b7c1`, then `ceb9552` fixing the
  `CLOUDFLARE_API_TOKEN` environment scoping). The first run (`698b7c1`)
  failed for that reason; the second (`ceb9552`) succeeded — confirmed via
  `gh run list`: `completed / success / "Scope deploy job to the Production
  environment" / Deploy to Cloudflare Pages / 57s`. Because `ceb9552` is a
  descendant of `e12342d`, that successful run built and deployed the full
  current `main`, which includes this ticket's `Brands.tsx` change — so the
  frontend is confirmed live despite never being deployed by a run of its own.
- **`aiorders-api`:** no CI/CD exists on this repo (`.github/workflows/`
  absent from `origin/main`, unchanged from every prior release on this
  project). The department's own L1 autonomy stops at opening the PR — a human
  merges and, on this project, a human also deploys. Confirmed live anyway,
  read-only, via the Supabase MCP connection rather than assumed from the
  merge alone:
  - `list_migrations` on `bmnmnejwdxbcqinqkwko` shows
    `20260829190000_add_last_order_at_to_platform_analytics` applied.
  - `pg_get_functiondef('public.calculate_platform_analytics')` returns the
    live function with `last_order_at timestamp with time zone` in its
    `RETURNS TABLE` signature and `MAX(o.created_at) as last_order_at` in the
    body — byte-for-byte the shape this ticket's migration doc specified, not
    the pre-migration version.
  - The `admin-portal` edge function (the router serving the brands-list
    endpoint) shows `version: 115`, `updated_at` **2026-08-30T02:47:37Z** —
    after this ticket's own `decided:` timestamp — and its deployed bundle
    contains the `last_order_at`-driven derivation code. Deployed from
    `file:///Users/hwalia/Documents/projects/aiorders/aiorders-api/...`
    (the approver's own checkout, not this department's `_eng` worktree) —
    same out-of-band pattern `ENG-006`'s release record documented for
    `platform-customer-auth`.
- **Why this department didn't run either deploy itself:** both projects are
  **L1** (`agents/eng-manager/config/projects.md`) — writing on a branch and
  opening a PR is the department's full autonomy; a human merges and, where no
  CI/CD exists, a human also deploys.

## Verification

Re-confirmed against live state rather than trusted from the merge alone —
see the three Supabase MCP checks under Deploy above, plus the Cloudflare
Pages run status. All are read-only queries or a GitHub API read; no cost, no
write.

**Acceptance criteria — not yet formally walked.** This record establishes
that the merged code is deployed and live; `skills/acceptance-check/SKILL.md`
(triggered by this ticket entering `shipped`, owned by product-manager) is
where each criterion gets checked against the live result specifically, not
duplicated here. Given the confirmations above, both derived fields
(`stage`, `health`) should now be live and non-placeholder for restaurants
with order history — a fast thing for that pass to spot-check first.

## Rollback

- **Path:** migration — the doc's own `DROP FUNCTION`+`CREATE FUNCTION`
  restores the pre-migration 4-column signature (additive column only, no
  data loss). Frontend — the Stage/Health columns and filter are additive UI;
  reverting `Brands.tsx` removes them with no backend dependency either way
  (both directions already degrade gracefully to a `-` cell, per the code
  review).
- **Tested:** not live-drilled (see frontmatter). Reasoned pre-merge plus
  independently checked against live catalog data this pass (see
  `rollback_tested` above) — narrower gap than "unverified," not fully closed.
- **Used:** no.

## Observability

No new observability mechanism — errors in the `admin-portal` function log
server-side through Supabase's existing function-log mechanism, same as every
other route in this router. Not independently exercised against the live
deploy (no dashboard access from this department).

## Cost

$0/month delta — same Supabase project, one additive column, no new service.
Cloudflare Pages build/deploy is already-provisioned capacity.

## Follow-ups

- Unbatched per-brand KV read fan-out (named at `ready-to-ship`, non-blocking
  at today's scale) — carried forward, not fixed here.
- No live-app click-through of the Brands page performed by this department
  (no browser access from this host) — the next hop (acceptance-check) should
  treat this as the first real user-perspective check, not assume the API-level
  confirmation above already covers it.
- This is the first ticket on this board where the GitHub Actions Cloudflare
  Pages pipeline existed at deploy time (added mid-ticket, after `e12342d`
  merged, before this reconciliation) — future `aiorders-admin-hub` releases
  should expect an actual run tied to their own merge commit, not this
  ticket's coincidental "swept in by a later run" shape.
