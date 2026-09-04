---
ticket: ENG-008
project: aiorders-admin-hub + aiorders-api (one ticket, two repos)
released: 2026-09-04T06:04:41Z (api) / 2026-09-04T06:07:37Z (admin-hub)
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1 (both)
gate_g3: n/a — L1 lane has no G3; the PR merges are the human gate
commit: aiorders-api PR #6 (MERGED, bd67e86) | aiorders-admin-hub PR #5 (MERGED, 39f6918)
environment: production (Supabase bmnmnejwdxbcqinqkwko + Cloudflare Workers admin-hub). Merges confirmed on `origin/main` on both repos; live-deploy status of either side is unknown from this worktree. See Health note.
rollback_tested: false — reasoned, not drilled (no Docker/psql/supabase CLI reachable from this host, same standing gap every prior `aiorders-api`/`aiorders-admin-hub` release on this board has named). Reasoning: additive migration only (two new nullable/defaulted columns, a backfill), a plain revert of both merge commits fully undoes the diff.
health_check: not checked — no dashboard/monitoring access to either Supabase or Cloudflare from this department; see Health note
cost_delta_monthly: 0
---

# Release — Influencer board admin management (region/campaign-type preference, rating, collaboration count)

## What shipped

Staff on the admin panel's Influencer board can now view and edit an
influencer's region preference and paid/barter campaign-type preference
(independent `accepts_paid`/`barter_visit` flags, the `accepts_barter`
column dropped per the approver's own round-3 correction — "no need for a
new column when we already have one to signify the same intent"), rate an
influencer 1–5, and track a staff-edited collaboration count. New
`GET`/`PATCH admin-portal/influencers/{id}` endpoint (`aiorders-api`,
admin/sub-admin gated); CORS `Access-Control-Allow-Methods` widened to
include `PATCH` (caught by this ticket's own build-hop artifact-enumeration
grep, before it ever reached review). A round-1 review found and a round-2
fix closed a real null-handling bug (`accepts_paid`/`accepts_barter`
fabricating `true`/`false` for the 51 influencers whose `barter_visit` was
genuinely unknown) with proper dirty-tracking rather than a blanket default.

## Merge

No reply was ever written to this ticket's own merge-request item
(`inbox/2026-09-02-eng008-merge-request.md`, `decision:` stays empty). Both
PRs merged directly on GitHub instead, base `main` on both repos, about 3
minutes apart:

```
$ git merge-base --is-ancestor 7c6e4b8 origin/main   # aiorders-api, PR #6's tip
YES ancestor — bd67e86 "Merge pull request #6 from .../feat/ENG-008-influencer-admin-management" is in origin/main's first-parent history
$ gh pr view 6 --repo harsimranwalia/aiorders-api --json state,mergedAt,mergeCommit,baseRefName
{"baseRefName":"main","state":"MERGED","mergedAt":"2026-09-04T06:04:41Z","mergeCommit":{"oid":"bd67e86..."}}

$ git merge-base --is-ancestor 141f2eb origin/main   # aiorders-admin-hub, PR #5's tip
YES ancestor — 39f6918 "Merge pull request #5 from .../feat/ENG-008-influencer-admin-management" is in origin/main's first-parent history
$ gh pr view 5 --repo harsimranwalia/aiorders-admin-hub --json state,mergedAt,mergeCommit,baseRefName
{"baseRefName":"main","state":"MERGED","mergedAt":"2026-09-04T06:07:37Z","mergeCommit":{"oid":"39f6918..."}}
```

**Why this took until now to catch, worth recording plainly.** Three
`scheduled`/`watch` sweeps between 09:37 and 09:57 UTC today reported
`aiorders-api` as "not merged" for this ticket — wrong, for roughly 3.5
hours, from 06:04:41Z on. The naive check (`git merge-base --is-ancestor
origin/feat/ENG-008-influencer-admin-management origin/main`, i.e. the
**current branch tip**) returns false on both repos even now, because
`ENG-009`'s and `ENG-010`'s PRs — stacked on this branch by design — merged
into it *after* this ticket's own PR had already separately merged to
`main`, moving the branch tip past what shipped. Checking the branch-tip
against `main` is the wrong test once a branch has downstream stacked
tickets still merging into it post-ship; checking the ticket's own recorded
commit (`branch:` frontmatter, `7c6e4b8`/`141f2eb`) or the PR object directly
via `gh` is what actually answers "did *this ticket's* diff reach `main`."
Full detail, including the same finding's consequence for `ENG-009`/`ENG-010`
themselves (their own merges did **not** ship, for the mirror-image reason):
this ticket's own log, `ENG-009`'s and `ENG-010`'s own logs, and a new row
filed in `proposals.md` this pass.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Migration | additive only — two nullable/defaulted columns (`staff_rating`, `collaboration_count`), `accepts_paid` backfilled from `barter_visit`; no destructive change | database | 2026-08-29 |
| Code review | pass, round 3 (round 1 failed: zero test coverage plus a null-coalescing bug fabricating preferences for 51 influencers with unknown `barter_visit`; round 2 closed both; round 3 re-reviewed the `accepts_barter → barter_visit` rename after the approver's own merge-request correction) | principal-engineer | 2026-09-02 |
| Quality | pass — `deno test` 19/19 (real execution), `aiorders-admin-hub` clean build, 1 pre-existing lint warning unrelated to this diff | qa | 2026-09-02 |
| Security | pass — two non-blocking findings (architect design-doc drift describing the dropped `accepts_barter` column; `ENG-009`'s branch staleness, cross-referenced above) | security | 2026-09-02 |
| G3 | n/a — L1 lane has no G3; the PR merges are the human gate | approver | 2026-09-04 |

Re-read all four receipts directly before writing this record:
`agents/database/migrations/ENG-008-influencer-profile-admin-management.md`,
`agents/principal-engineer/reviews/ENG-008.md`,
`agents/qa/test-plans/ENG-008.md`, `agents/security/reviews/ENG-008.md` — all
`pass`, all against the round-3 (`7c6e4b8`/`141f2eb`) diff that's actually on
`main` now — no drift between what was gated and what shipped.

## Deploy

- **Method:** merge to `main` on both repos. Neither repo has a confirmed
  push-triggered CI/deploy workflow on `origin/main`.
- **Why this department didn't run it:** both projects are registered
  **L1** — a human merges; this department has no deploy credentials for
  either.
- **What actually happened:** unknown from here — no Actions run log or
  Supabase/Cloudflare dashboard access from this worktree.
- **Migration:** additive, not executed against a live Postgres by this
  department (no live DB/Supabase MCP session during this hop) — verified
  instead by reading the tracked migration directly.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

`git show origin/main:supabase/functions/admin-portal/handlers/influencers.ts`
confirms `hasInfluencerAdminAccess`/`updateInfluencer`/`EDITABLE_FIELDS` all
present, zero references to `accepts_barter` anywhere in the tracked tree on
either repo (`git grep accepts_barter origin/main` — no hits, both repos).
`git show origin/main:src/pages/Influencers.tsx` confirms the fixed
dirty-tracked `accepts_paid` handling (no coalescing fallback) survives on
`main` unchanged. Health checks: not run — see `health_check` above.

## Acceptance criteria

Re-checked against `origin/main` on both repos
(`agents/product-manager/specs/ENG-008-influencer-profile-admin-management.md`):
region/campaign-type preference viewable and editable (pass), independent
paid/barter flags representable including "both" (pass), 1–5 rating
editable (pass), collaboration count viewable/editable (pass), non-admin
write rejected (pass, round-1-added tests). Item 4 (influencer-facing gated
visibility) and the "engagement" item remain explicitly out of this
ticket's scope, per its own PRD non-goals. Not verified live against a
running frontend/Postgres session — same named gap this instance's other
releases already carry.

## Rollback

- **Path:** revert both merge commits (`bd67e86` on `aiorders-api`, `39f6918`
  on `aiorders-admin-hub`). Migration rollback:
  `ALTER TABLE influencers DROP COLUMN staff_rating, DROP COLUMN
  collaboration_count;` — `barter_visit` itself was never touched, no
  backfill to unwind on that column.
- **Tested:** not drilled — no live Postgres reachable from this host.
- **Used:** no.

## Health note

No dashboard/monitoring access to either Supabase (`bmnmnejwdxbcqinqkwko`)
or the Cloudflare project behind `aiorders-admin-hub` from this
department's worktrees — live-deploy status and runtime health are both
unknown here, same boundary this instance's other L1 releases already
carry.

## Observability

Both new/changed write paths propagate errors via `console.error`,
consistent with this repo's existing convention — unchanged by this ticket.

## Cost

$0/month delta — no new service or dependency; two additive columns and one
gated CRUD endpoint.

## Follow-ups

**Not this ticket's own defect, but discovered while closing it out:**
`ENG-009`'s and `ENG-010`'s PRs also show `MERGED` on GitHub (into this
ticket's own branch, which was their configured stacked base) but neither
repo's `main` actually contains their commits — confirmed by content diff,
not just ancestry (`git grep`/`git show` against both the stale branch tip
and `main`). The specific regression risk this ticket's own round-3 review
flagged (`ENG-009` shipping the just-rejected `accepts_barter` shape) did
**not** materialize — the merged branch carries the correct post-round-3
code, byte-for-byte matching `main` past the `ENG-009`/`ENG-010` line-number
shift. But the operational fact stands regardless of content correctness:
neither ticket's code has reached `main`, despite both showing `MERGED`.
Full writeup: `ENG-009`'s and `ENG-010`'s own board-file logs, and a new
proposal row filed this pass (`proposals.md`) naming the general failure
shape (a stacked PR's merge can satisfy GitHub's UI without ever reaching
the default branch) so it's checked mechanically rather than caught by
chance, as it was here.
