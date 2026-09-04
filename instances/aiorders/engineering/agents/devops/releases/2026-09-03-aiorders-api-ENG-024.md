---
ticket: ENG-024
project: aiorders-api
released: 2026-09-03T22:09:23Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 8c97bd3 (merged via b1265ac, PR #11)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). Merge confirmed on `origin/main`; whether the backfill migration has been pushed live is unknown from this worktree — no `SUPABASE_ACCESS_TOKEN`, not linked. See Health note.
rollback_tested: false — reasoned, not drilled (no Docker/psql/supabase CLI reachable from this host, same standing gap `ENG-007`'s release already named). Reasoning: single `UPDATE ... WHERE` backfill, non-destructive, effectively idempotent, reversible by an inverse `UPDATE` on the same `WHERE`; code side reverts with the one commit.
health_check: not checked — no dashboard/monitoring access to bmnmnejwdxbcqinqkwko from this department; see Health note
cost_delta_monthly: 0
---

# Release — Onboarded restaurants missing from marketplace search

## What shipped

`aiorders-api`'s `restaurant-portal-onboarding` function now sets
`show_in_marketplace: true` on `createRestaurant`'s insert, alongside the
existing `approved: true` — closing the gap where every restaurant onboarded
through the FoodSwipe sign-up flow was silently invisible in marketplace
search (including location-sorted search) until a staff member manually
flipped the flag. A one-time backfill migration
(`20260903120000_backfill_onboarding_show_in_marketplace.sql`) makes
already-onboarded restaurants visible too, scoped to exclude unapproved rows
and the separate `restaurant-claims` path on purpose. One new colocated test
file (`restaurants.test.ts`, 2 cases) covers the regression directly.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-03-eng024-merge-request.md`, `decision:` still blank).
`aiorders-api` PR #11 was merged directly on GitHub instead. Confirmed
independently via local git ancestry, not trusted from the ticket's own
account alone:

```
$ git merge-base --is-ancestor refs/remotes/origin/pr/11 origin/main
YES ancestor
$ git log -1 --format="%H %ci %s" b1265acffd8abe4ff6d98059c0d675163e3587c8
b1265acffd8abe4ff6d98059c0d675163e3587c8 2026-09-03 15:09:23 -0700 Merge pull request #11 from harsimranwalia/fix/ENG-024-onboarding-marketplace-visibility
```

`refs/remotes/origin/pr/11`'s head (`8c97bd3`) is exactly the commit this
ticket's own `ready-to-ship → blocked` log entry recorded — no drift, no
rebase. Single repo, no cross-ticket branch dependency. Per `eng_build_loop.md`
step 5, local git only — no `gh` call made for this detection.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Review + suite + OWASP (fast-lane combined) | pass | principal-engineer | 2026-09-03 |
| Migration | no dedicated verdict exists on this lane (named gap, not silently passed — see `agents/principal-engineer/reviews/ENG-024.md` and the open `proposals.md` row); assessed low-risk informally | principal-engineer / devops | 2026-09-03 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-03 |

## Deploy

- **Method:** merge to `main` only — no CI/CD auto-deploy exists on this repo
  (`.github/workflows/` absent from `origin/main`, confirmed same as every
  prior `aiorders-api` release on this board).
- **Why this department didn't run it:** `aiorders-api` is registered **L1**
  — a human merges, and running the deploy would exceed this department's
  own autonomy. This worktree also couldn't have run it: not linked, no
  `SUPABASE_ACCESS_TOKEN`.
- **What actually happened:** unknown from here — same open question every
  `aiorders-api` release on this board has recorded since `ENG-007`.
- **Migration:** additive/backfill only, present on `origin/main`; live-push
  status unknown.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

- `git diff refs/remotes/origin/pr/11 origin/main -- $(git diff --name-only refs/remotes/origin/pr/11^..refs/remotes/origin/pr/11)` shows no divergence beyond the merge itself — the merged tree matches the branch tip that passed review.
- `git ls-tree -r origin/main --name-only` confirms `restaurants.ts`,
  `restaurants.test.ts`, and the backfill migration are present under the
  reviewed paths.
- Health checks: not run — see `health_check` above.
- Acceptance criteria: 3 of 3 confirmed against the merged tree — see below.

## Acceptance criteria

Re-checked against `origin/main`
(`agents/product-manager/specs/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md`):

1. A restaurant onboarded through FoodSwipe is visible in marketplace search
   immediately. **Pass** — `show_in_marketplace: true` present on the
   merged `createRestaurant` insert, unchanged from the reviewed diff.
2. Restaurants onboarded before the fix become visible via the backfill.
   **Pass** — backfill migration present on `origin/main`; whether it has
   been applied to the live database is unknown (see Deploy).
3. `restaurant-claims` and unapproved rows are not affected. **Pass** —
   backfill `WHERE` clause (`approved = true AND claimed_by_user_id IS NULL`)
   unchanged from the reviewed diff.

## Rollback

- **Path:** revert the single commit (removes the insert field); inverse
  `UPDATE` on the same `WHERE` to undo the backfill.
- **Tested:** not drilled — see `rollback_tested` above.
- **Used:** no.

## Health note

Same boundary every `aiorders-api` release on this board has hit: no
dashboard/monitoring access to `bmnmnejwdxbcqinqkwko` from this department's
worktree, and no separate deploy evidence exists here either — so both
whether the migration is live *and* whether it's healthy are unknown from
this department.

## Observability

No new failure mode introduced — one literal field added to an
already-existing insert. The migration's own `RAISE NOTICE` reports its row
count on apply (not independently observed — no log/dashboard access).

## Cost

$0/month delta — same Supabase project, one new field on an existing insert,
one backfill migration, no new service.

## Follow-ups

Two open proposals reference this ticket's own gaps and are not re-filed
here: the fast-lane migration-gate mechanism gap (`proposals.md`,
2026-09-03, principal-engineer) and whether `show_in_marketplace`'s DB-level
default should change (`proposals.md`, 2026-09-03, eng-manager). Both stand
as already-open, unrelated to this release's own correctness.
