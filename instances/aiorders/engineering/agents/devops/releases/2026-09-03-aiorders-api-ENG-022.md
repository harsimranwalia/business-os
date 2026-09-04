---
ticket: ENG-022
project: aiorders-api
released: 2026-09-04T02:03:48Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 78194da (merge of d5078c5, PR #9)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). Merge confirmed on `origin/main`; whether the deploy has actually pushed live is unknown from this worktree — no `SUPABASE_ACCESS_TOKEN`, not linked. See Health note.
rollback_tested: false — reasoned, not drilled (no Docker/psql/supabase CLI reachable from this host, same standing gap every prior `aiorders-api` release on this board has named). Reasoning: no migration, no stored-state change; a plain revert of the merge commit fully undoes the diff.
health_check: not checked — no dashboard/monitoring access to bmnmnejwdxbcqinqkwko from this department; see Health note
cost_delta_monthly: 0
---

# Release — Fix broken restaurant-scoped access check on 5 brand-portal handlers

## What shipped

`aiorders-api`'s `supabase/functions/brand-portal/` closed a cross-tenant
PII/write exposure across 5 of 9 handler files. `utils.ts`'s dead,
correctly-implemented `verifyRestaurantAccessLegacy` was promoted (renamed
`requireRestaurantAccess`, `@deprecated` dropped, A09 denial logging added)
and wired into `feedback.ts`/`customers.ts`/`hiring.ts`/`website.ts` (11
call sites, previously discarding the check's return value entirely);
`offers.ts` (8 call sites) was fixed in place — correct argument order and
`.hasAccess` check, matching its own already-correct siblings. 24 new
`Deno.test` cases (19 negative + 5 positive) across 5 colocated test files.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-03-eng022-merge-request.md`, `decision:` still blank).
`aiorders-api` PR #9 was merged directly on GitHub instead. Confirmed
independently via local git ancestry (`eng_build_loop.md` step 5), then
cross-checked against `gh pr view` given the severity (P0):

```
$ git merge-base --is-ancestor d5078c5 origin/main && echo YES
YES
$ gh pr view 9 --repo harsimranwalia/aiorders-api --json state,mergedAt,mergeCommit
{"mergeCommit":{"oid":"78194da85e8942429ae3d83c4ef3545ba6475e42"},"mergedAt":"2026-09-04T02:03:48Z","state":"MERGED"}
```

`origin/main`'s tip (`78194da8`) is exactly that merge commit. The branch
tip (`d5078c5`) matches this ticket's own `ready-to-ship → blocked` log
entry with zero drift: `git diff origin/fix/ENG-022-brand-portal-tenant-isolation origin/main -- <changed files>` is empty — the merged tree is
byte-identical to what passed all three gates. Single repo, no cross-ticket
branch dependency.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass | principal-engineer | 2026-09-03 |
| Quality (QA) | pass | qa | 2026-09-03 |
| Security | pass | security | 2026-09-03 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-04 |

Re-read all three receipts directly before writing this record (not taken
from the ticket's own narrative): `agents/principal-engineer/reviews/ENG-022.md`
(`verdict: pass`), `agents/qa/test-plans/ENG-022.md` (`last_result: pass`),
`agents/security/reviews/ENG-022.md` (`verdict: pass`). No migration — none
applies, confirmed no `*.sql` in the diff.

## Deploy

- **Method:** merge to `main` only — no CI/CD auto-deploy exists on this repo
  (`.github/workflows/` absent from `origin/main`, same as every prior
  `aiorders-api` release on this board).
- **Why this department didn't run it:** `aiorders-api` is registered **L1**
  — a human merges, and running the deploy would exceed this department's
  own autonomy.
- **What actually happened:** unknown from here — same open question every
  `aiorders-api` release on this board has recorded since `ENG-007`.
- **Migration:** none.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

Re-verified directly against the merged tree, not just the receipts'
account: all 5 fixed files (`feedback.ts`, `offers.ts`, `customers.ts`,
`hiring.ts`, `website.ts`) call the corrected function/pattern on
`origin/main` — `grep` confirmed per file, one-for-one against the design's
own table. `utils.ts` exports `requireRestaurantAccess` (promoted from the
dead legacy helper) at `origin/main`. Health checks: not run — see
`health_check` above.

## Acceptance criteria

Re-checked against `origin/main`
(`agents/product-manager/specs/ENG-022-brand-portal-tenant-isolation-broken.md`):

1. Cross-tenant call with another restaurant's id is denied, across every
   `verifyRestaurantAccess` call site in `brand-portal/`. **Pass** — all 19
   call sites across the 5 files independently re-confirmed on the merged
   tree calling `requireRestaurantAccess`/corrected `verifyRestaurantAccess`,
   matching the security gate's own one-for-one count.
2. Full audit of every call site, not just the ones first noticed.
   **Pass** — same 19-site re-check as AC1; the 4 already-correct files
   (`catering.ts`, `menus.ts`, `restaurants.ts`, and `onlineOrders.ts`) are
   unchanged in this diff, confirmed out of scope correctly.
3. Legitimate owner access for their own restaurant is unchanged.
   **Pass** — security gate's own mutation test (disabled the check at one
   throw-site and one return-site, confirmed exactly the matching negative
   tests went red, all other tests including positive cases stayed green);
   not re-run this hop, receipt re-read directly instead.
4. A regression test exists per fixed call site proving the negative case.
   **Pass** — 5 test files, 24 `Deno.test` cases (19 negative + 5 positive),
   `deno test --no-check`: 24 passed / 0 failed, confirmed by the security
   gate's own fresh run, receipt re-read directly.

## Rollback

- **Path:** revert the single merge commit — no migration, no stored-state
  change, fully undoes the diff.
- **Tested:** not drilled — see `rollback_tested` above.
- **Used:** no.

## Health note

Same boundary every `aiorders-api` release on this board has hit: no
dashboard/monitoring access to `bmnmnejwdxbcqinqkwko` from this
department's worktree, so whether the deploy is live and healthy is
unknown from here.

## Observability

Both fix paths (`requireRestaurantAccess`'s throw and `offers.ts`'s
in-place return) log via `console.warn` before denying
(`user=<id> restaurant=<id>`), surfaced through Supabase's existing
function logs — confirmed present on `origin/main`, no new mechanism
needed.

## Cost

$0/month delta — no new dependency, no new vendor, confirmed no
`package.json`/`deno.json`/lockfile change in the diff (the untracked
`deno.lock` in the department's worktree is a pre-existing local artifact,
not part of this diff).

## Follow-ups

Two non-blocking findings from the security gate are not re-derived here,
both already routed to their own channel: the verbose-error-message finding
on `verifyRestaurantAccess`'s catch-all (already three-struck, not
re-proposed) and the admin/sub-admin/partner-admin/partner-user bypass in
`utils.ts` (filed as a proposal, `agents/eng-manager/proposals.md`,
2026-09-03, security, `aiorders-api`) — both out of this diff's scope, not
this release's own gap.
