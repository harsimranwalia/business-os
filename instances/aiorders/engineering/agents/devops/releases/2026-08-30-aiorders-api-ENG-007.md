---
ticket: ENG-007
project: aiorders-api
released: 2026-08-30T02:38:08Z
released_by: devops
autonomy: L1
gate_g3: n/a — L1 merge, no G3 on this lane
commit: 2aec86f (merged via 93617c6, PR #4)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). Merge confirmed; whether the migration has been pushed live is unknown from this worktree — no `SUPABASE_ACCESS_TOKEN`, not linked. See Health note.
rollback_tested: true — migration rollback drilled pre-merge against a throwaway Postgres container (named as a weaker substitute for a live-Postgres run in the migration receipt, same gap class as ENG-011's below); not drilled against the live Supabase project (no access — see Health note).
health_check: not checked — no dashboard/monitoring access to bmnmnejwdxbcqinqkwko from this department; see Health note
cost_delta_monthly: 0
---

# Release — Per-restaurant loyalty configuration

## What shipped

`aiorders-api` gets one new additive table (`restaurant_loyalty_configs`,
RLS-enabled, service-role only) and a `BEFORE INSERT` trigger enforcing
strictly-increasing, future-only `effective_from` values per restaurant under
an advisory lock. New `GET`/`POST admin-portal/handlers/loyalty-config.ts`,
admin/sub-admin gated, 44 unit tests covering every DB-free decision (role
gate, input validation, "current as of T" derivation, trigger-error mapping).
No ledger, no points, no redemption, and no frontend caller exists anywhere in
this diff — purely additive config for tickets 3/4 of the loyalty sequence
(ENG-006's own follow-ons) to compute against later. Zero behavioral effect on
production until something calls it, same shape as ENG-006.

## Merge

No L1 merge request was ever raised by this department — the ticket sat at
`ready-to-ship` behind a Saturday `releases.block_weekends` hold that (per the
corrected `skills/release-runner/SKILL.md`, 2026-08-29) should never have
applied to an L1 project in the first place. PR #4 was opened and merged
directly on GitHub — `mergedBy` is the approver's own account — without the
department's own PR-open step ever running. Confirmed independently rather
than trusted from either signal alone:

```
$ git merge-base --is-ancestor origin/loyalty-system origin/main
YES ancestor
$ git log -1 --format="%H %P" origin/main
93617c6 eb2ed89 2aec86f
$ gh pr view 4 --json state,mergedAt,headRefName
{"state":"MERGED","mergedAt":"2026-08-30T02:38:08Z","headRefName":"loyalty-system"}
```

`origin/loyalty-system`'s head (`2aec86f`) is exactly the commit this
ticket's own `ready-to-ship` log entry recorded — no drift, no rebase.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass | principal-engineer | 2026-08-29 |
| Quality | pass (44/44 tests) | qa | 2026-08-29 |
| Security | pass | security | 2026-08-29 |
| Migration | pass, named gap (no live-Postgres run) | database | 2026-08-29 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-08-30 |

## Deploy

- **Method:** merge to `main` only — no CI/CD auto-deploy exists on this repo
  (`.github/workflows/` absent from `origin/main`).
- **Why this department didn't run it:** `aiorders-api` is registered **L1**
  — a human merges, and running the deploy would push a production release
  outside this department's own autonomy. This worktree also couldn't have
  run it: not linked, no `SUPABASE_ACCESS_TOKEN`.
- **What actually happened:** unknown from here. Unlike `ENG-006` (where the
  approver's own separate `supabase db push`/`functions deploy` runs were
  independently confirmed by their CLI output), no equivalent evidence exists
  for this migration yet. Recorded as unknown, not inferred either way.
- **Migration:** additive, present on `origin/main`; live-push status unknown.
- **Feature flag:** none — no live caller, so nothing to keep dark.
- **Duration:** n/a — no deploy run by this department.

## Verification

- `git diff origin/loyalty-system origin/main` → empty. The merged tree is
  byte-identical to the branch tip that passed review/QA/security, so the
  44/44 test result documented at `in-review` necessarily still holds against
  `origin/main`; not re-run against provably identical source.
- `git ls-tree -r origin/main --name-only` confirms `loyalty-config.ts` and
  its migration file are present under the reviewed paths.
- Health checks: not run — see `health_check` above.
- Acceptance criteria: 4 of 4 confirmed against the merged tree — see below.

## Acceptance criteria

Re-checked against `origin/main` (`agents/product-manager/specs/ENG-007-per-restaurant-loyalty-configuration.md`):

1. New config with an effective date becomes the restaurant's current
   configuration. **Pass** — direct unit coverage, unchanged on `origin/main`.
2. A later-dated rate becomes current as of its date; prior records remain
   readable for earlier points in time. **Pass** — same coverage.
3. An as-of query before a later rate change returns the rate actually in
   effect then, never the current one. **Pass** — same coverage.
4. An unconfigured restaurant reports not-enrolled, not an error. **Pass** —
   same coverage.

All four are pure, DB-free decision logic — unlike `ENG-006`'s OTP-provider
gap, nothing here depends on a live external call to exercise, so nothing is
carried forward as unverified.

## Rollback

- **Path:** drop `restaurant_loyalty_configs` and its trigger — purely
  additive, no FK from any existing table into it.
- **Tested:** drilled pre-merge against a throwaway Postgres container
  (`agents/database/migrations/ENG-007-per-restaurant-loyalty-configuration.md`).
  Not re-drilled against the live project — no access (see Health note).
- **Used:** no.

## Health note

Same boundary `ENG-006` hit two days ago on this same repo: no
dashboard/monitoring access to `bmnmnejwdxbcqinqkwko` from this department's
worktree. Unlike `ENG-006`, no separate deploy evidence exists here either —
so both whether the migration is live *and* whether it's healthy are unknown
from this department, not just the latter.

## Observability

New: `loyalty-config.ts` logs every trigger-error mapping server-side,
matching this repo's existing pattern. Not independently exercised against a
live deploy — no log/dashboard access.

## Cost

$0/month delta — same Supabase project, one new empty table, no new service.

## Follow-ups

Tickets 3/4 of the loyalty sequence (points ledger, redemption) are the
intended callers of this config and remain unscheduled. Whether this
migration has actually been pushed to the live Supabase project is the one
open question this release leaves behind — worth a direct check next time
this department (or the approver) has live access, not urgent given zero
current callers.
