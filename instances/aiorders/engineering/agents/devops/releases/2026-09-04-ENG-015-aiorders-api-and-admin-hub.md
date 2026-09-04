---
ticket: ENG-015
project: aiorders-admin-hub + aiorders-api (one ticket, two repos)
released: 2026-09-04T06:45:05Z (admin-hub) / 2026-09-04T06:44:33Z (api)
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1 (both)
gate_g3: n/a — L1 lane has no G3; the PR merges are the human gate
commit: aiorders-api PR #10 (MERGED, d9e0c6d) | aiorders-admin-hub PR #8 (MERGED, 2389790)
environment: production (Supabase bmnmnejwdxbcqinqkwko + Cloudflare Workers admin-hub). Merges confirmed; live-deploy status of either side is unknown from this worktree. See Health note.
rollback_tested: n/a — no destructive migration to drill; additive RLS policy plus a code-side branch, both cleanly revertible.
health_check: not checked — no dashboard/monitoring access to either Supabase or Cloudflare from this department; see Health note
cost_delta_monthly: 0
---

# Release — Agency/reseller (partner) brand-scoped locations and a working add-location path

## What shipped

Fixes a live P1 cross-tenant exposure: a partner-admin/partner-user could
previously see and act on **every** restaurant on the platform, not just
their own brand's, and could not successfully add a new restaurant at all
(the write silently failed). `getRestaurants`/`getRestaurantById`/
`updateRestaurant` in `aiorders-api` now scope a non-staff caller to their
own `brands.partner_id` set, enforced in code (service-role client, explicit
filter/check — not RLS, `ADR-006`). A new RLS `INSERT` policy lets a partner
add a restaurant under their own brand, held for staff review by default
(`approved = false`); `aiorders-admin-hub`'s `AddRestaurantModal.tsx` now
sends that `approved: false` for a partner caller instead of the
unconditional `true` every caller got before. Round 1 of code review also
caught and closed a real mass-assignment bug in the same diff (a partner
could self-approve their own new restaurant, or reassign it to a brand they
don't own, via `updateRestaurant`) before it ever shipped.

## Merge

No reply was ever written to this ticket's own merge-request item
(`inbox/2026-09-03-eng015-merge-request.md`, `decision:` stays blank). Both
PRs merged directly on GitHub instead, in the same batch-merge session as
`ENG-013`'s two PRs above (all four within about 90 seconds of each other),
and — as both PR bodies required — together rather than one at a time (32
seconds apart):

```
$ git merge-base --is-ancestor origin/fix/ENG-015-agency-reseller-brand-scoping origin/main   # aiorders-api
YES ancestor
$ gh pr view 10 --repo harsimranwalia/aiorders-api --json state,mergedAt,mergeCommit
{"state":"MERGED","mergedAt":"2026-09-04T06:44:33Z","mergeCommit":{"oid":"d9e0c6d94a8955046664e044bcb5459b438c519c"}}

$ git merge-base --is-ancestor origin/fix/ENG-015-agency-reseller-brand-scoping origin/main   # aiorders-admin-hub
YES ancestor
$ gh pr view 8 --repo harsimranwalia/aiorders-admin-hub --json state,mergedAt,mergeCommit
{"state":"MERGED","mergedAt":"2026-09-04T06:45:05Z","mergeCommit":{"oid":"23897905e14ae9ba574ede9a447ec9e7edefd0f5"}}
```

Branch tips (`aiorders-api@99ea353`, `aiorders-admin-hub@8c0db46`) match this
ticket's own frontmatter exactly — no drift between what passed every gate
and what merged. Both landing in the same session matters here specifically:
either PR alone would have left AC3/AC5 only half-satisfied (the backend's
`approved = false` INSERT policy is what makes the frontend's conditional
load-bearing rather than cosmetic) — confirmed both are in on the merged
tree, not just opened together.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Migration | pass — additive INSERT policy only, no backfill, no existing row touched | database | 2026-09-03 |
| Code review | pass, round 2 (round 1 failed: zero test coverage, third occurrence of this shape this week, plus a real mass-assignment bug — self-approve and brand-reassignment both possible via `updateRestaurant`; both closed with a strip-fields fix and 22 tests, mutation-verified) | principal-engineer | 2026-09-03 |
| Quality | pass — 22/22 new tests, 78/78 whole-directory (one unrelated pre-existing flake, not reproduced); `aiorders-admin-hub` side unchanged since round 1's own clean lint/build | qa | 2026-09-03 |
| Security | pass — one non-blocking finding (RLS activation on `public.restaurants` itself unverified from this repo — a layer beneath the policy-logic trace; folded into a staging-smoke-test recommendation, not gating) | security | 2026-09-03 |
| G3 | n/a — L1 lane has no G3; the PR merges are the human gate | approver | 2026-09-04 |

Re-read all four receipts directly before writing this record:
`agents/database/migrations/ENG-015-agency-reseller-brand-scoping.md`,
`agents/principal-engineer/reviews/ENG-015.md`,
`agents/qa/test-plans/ENG-015.md`, `agents/security/reviews/ENG-015.md` —
all `pass`.

## Deploy

- **Method:** merge to `main` on both repos. Neither repo has a confirmed
  push-triggered CI/deploy workflow on `origin/main`.
- **Why this department didn't run it:** both projects are registered
  **L1** — a human merges; this department has no deploy credentials for
  either.
- **What actually happened:** unknown from here — no Actions run log or
  Supabase/Cloudflare dashboard access from this worktree.
- **Migration:** additive (one new `INSERT` policy on `restaurants`) — not
  executed against a live Postgres by this department (no live DB/Supabase
  MCP session was available during the build hop this time); verified
  instead by reading every relevant tracked migration directly.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

`git show origin/main:supabase/functions/admin-portal/handlers/restaurants.ts`
confirms `isStaff`/`getPartnerBrandIds`/`stripPartnerRestrictedFields` all
present and wired into all three functions (`getRestaurants`,
`getRestaurantById`, `updateRestaurant`); `git show
origin/main:src/components/AddRestaurantModal.tsx` confirms the conditional
`approved` field for `partner-admin`/`partner-user`. Health checks: not
run — see `health_check` above.

## Acceptance criteria

Re-checked against both `origin/main`s
(`agents/product-manager/specs/ENG-015-agency-reseller-brand-scoping.md`): a
partner sees only their own brand's restaurants (pass, AC1/2), is denied a
restaurant outside their brand on the by-id and update paths (pass, AC2/4,
including the two round-1-found bypasses now closed), can add a restaurant
under their own brand held for staff review by default (pass, AC3/5), staff
(admin/sub-admin) behavior is unchanged (pass, AC6). Dashboard/Influencers/
Users pages were investigated at PRD stage and confirmed already
hard-blocking partner roles outright — not touched by this diff, not a
regression. Not verified live against a running frontend/Postgres session —
same named gap this instance's other releases already carry; the security
gate's own RLS-activation finding folds into the recommended staging smoke
test.

## Rollback

- **Path:** revert both merge commits. `aiorders-api` —
  `DROP POLICY IF EXISTS "Partners can add restaurants to their assigned
  brands" ON public.restaurants;` plus reverting the handler diff (no data
  migration, no backfill to unwind). `aiorders-admin-hub` — revert the
  modal diff.
- **Tested:** not drilled — no destructive migration exists to drill
  against a throwaway container, and no live Postgres was reachable from
  this host during the build hop either way.
- **Used:** no.

## Health note

No dashboard/monitoring access to either Supabase (`bmnmnejwdxbcqinqkwko`)
or the Cloudflare project behind `aiorders-admin-hub`, from this
department's worktrees — live-deploy status and runtime health are both
unknown here, same boundary this instance's other L1 releases already
carry.

## Observability

Both new/changed write paths propagate errors to each caller's existing
`catch` (`console.error`), consistent with this file's own pre-existing
convention (also the security gate's one named non-blocking finding: those
catches return `error.message` verbatim in a 500 body — pre-existing
posture, not introduced by this diff). New 403 denials use this codebase's
existing `_shared/restaurantAccess.ts` wording, not a fresh convention.

## Cost

$0/month delta — no new service or dependency; one additive RLS policy plus
a code branch and a one-field frontend conditional.

## Follow-ups

The security gate's own RLS-activation finding (no tracked migration
creates `public.restaurants` or enables RLS on it — a layer beneath the
policy-logic trace this ticket's own tests exercise) is folded into a
sharpened staging-smoke-test recommendation on `ENG-015`'s own security
review, not a new proposal — confirm a test partner's insert/update is
actually rejected or held, never unrestricted, next time this department or
the approver has a live session against either environment.
`updateBrandOwner()` (same file, a distinct unrelated finding — any partner
can rewrite any brand's owner contact info) remains open on
`agents/eng-manager/proposals.md`, out of this ticket's own scope.
