---
ticket: ENG-013
project: aiorders-admin-hub + aiorders-api (one ticket, two repos)
released: 2026-09-04T06:45:37Z (admin-hub) / 2026-09-04T06:45:54Z (api)
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1 (both)
gate_g3: n/a — L1 lane has no G3; the PR merges are the human gate
commit: aiorders-api PR #5 (MERGED, 1b0c504) | aiorders-admin-hub PR #4 (MERGED, 0583962)
environment: production (Supabase bmnmnejwdxbcqinqkwko + Cloudflare Workers admin-hub). Merges confirmed; live-deploy status of either side is unknown from this worktree. See Health note.
rollback_tested: false — reasoned, not drilled. One nullable additive column, no default, no backfill; frontend side is a UI addition only.
health_check: not checked — no dashboard/monitoring access to either Supabase or Cloudflare from this department; see Health note
cost_delta_monthly: 0
---

# Release — Foodswipe funnel: staff-settable pipeline stage override

## What shipped

Sales/onboarding staff can now set or correct a Foodswipe listing's pipeline
stage directly from the kanban card, with the manual choice sticking (a new
nullable `profiles.foodswipe_stage_override` column takes precedence over
the existing `classifyStage()` derivation) and a "Reset to automatic" path
back to the derived value. A "Manually set" badge marks an overridden card.

## Merge

No reply was ever written to this ticket's original merge-request item — the
approver's own `changed` answer (2026-09-01) asked a different, real
question first (whether custom pipeline-*stage-definitions*, not just
per-card overrides, were wanted), resolved 2026-09-03 as "Reading A": ship
this PR as built, file stage-taxonomy configuration separately (`ENG-028`).
That answer authorized the merge; it did not perform it. Both PRs then
merged directly on GitHub, in the same batch-merge session as `ENG-015`'s
two PRs below (all four within about 90 seconds of each other):

```
$ git merge-base --is-ancestor origin/feat/ENG-013-foodswipe-funnel-stage-control origin/main   # aiorders-api
YES ancestor
$ gh pr view 5 --repo harsimranwalia/aiorders-api --json state,mergedAt,mergeCommit
{"state":"MERGED","mergedAt":"2026-09-04T06:45:54Z","mergeCommit":{"oid":"1b0c504411676684cdb1f68544502e6269ecb695"}}

$ git merge-base --is-ancestor origin/feat/ENG-013-foodswipe-funnel-stage-control origin/main   # aiorders-admin-hub
YES ancestor
$ gh pr view 4 --repo harsimranwalia/aiorders-admin-hub --json state,mergedAt,mergeCommit
{"state":"MERGED","mergedAt":"2026-09-04T06:45:37Z","mergeCommit":{"oid":"058396299758af69def7c1870903a680e1baab2b"}}
```

Branch tips (`aiorders-api@c95b25b`, `aiorders-admin-hub@a1c3bdf`) match this
ticket's own frontmatter exactly — no drift between what passed every gate
and what merged.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Migration | pass — additive nullable column, no default, no backfill, no RLS change | database | 2026-08-29 |
| Code review | pass, round 2 (round 1 failed: zero test coverage on the new authz-gated write path, closed with 17 tests) | principal-engineer | 2026-08-31 |
| Quality | pass — all 5 ACs covered; `deno test` not executable on this host (no `deno` on PATH), hand-traced instead, 0 discrepancies | qa | 2026-08-31 |
| Security | pass — one non-blocking finding (raw `error.message` in a 500 body, first tracked occurrence) | security | 2026-08-31 |
| G3 | n/a — L1 lane has no G3; the PR merges are the human gate | approver | 2026-09-04 |

Re-read all four receipts directly before writing this record:
`agents/database/migrations/ENG-013-foodswipe-funnel-stage-control.md`,
`agents/principal-engineer/reviews/ENG-013.md`,
`agents/qa/test-plans/ENG-013.md`, `agents/security/reviews/ENG-013.md` —
all `pass`.

## Deploy

- **Method:** merge to `main` on both repos. Neither repo has a confirmed
  push-triggered CI/deploy workflow on `origin/main` (unlike
  `restaurant-portal`'s `deploy-cf.yml`).
- **Why this department didn't run it:** both projects are registered
  **L1** — a human merges; this department has no deploy credentials for
  either (no `SUPABASE_ACCESS_TOKEN`, no Cloudflare token).
- **What actually happened:** unknown from here — no Actions run log or
  Supabase/Cloudflare dashboard access from this worktree.
- **Migration:** additive (one nullable column, no default, no backfill) —
  not executed against a live Postgres by this department at any gate (no
  `docker`/`psql`/`supabase` CLI on this host); verified instead via
  read-only Supabase MCP against the real production schema at build time.
- **Feature flag:** none — the override column defaults to `null`
  (automatic) for every existing row.
- **Duration:** n/a — no deploy run by this department.

## Verification

`git show origin/main:supabase/functions/admin-portal/handlers/foodswipe.ts`
confirms `setStageOverride`/`resetStageOverride` both present, both still
scoped `.eq('source', 'foodswipe')` in addition to the id; `git show
origin/main:src/pages/FoodswipeListings.tsx` confirms the dropdown/dialog
and "Manually set" badge are present, unchanged from what code review
reviewed. Health checks: not run — see `health_check` above.

## Acceptance criteria

Re-checked against both `origin/main`s
(`agents/product-manager/specs/ENG-013-foodswipe-funnel-stage-control.md`):
staff can set a stage (pass), the manual choice sticks and beats the
automatic derivation (pass), a reset path returns to automatic (pass), the
write is scoped to the caller's existing admin/sub-admin gate and to
`source='foodswipe'` so no other profile can be touched (pass — the exact
line code review named "what to review hardest"), a kanban card shows which
listings are manually set (pass, the badge). Not verified live against a
running frontend session (no live Postgres/browser session available to
this department) — same named gap this instance's other releases already
carry.

## Rollback

- **Path:** revert both merge commits. `aiorders-api` — drop the nullable
  column (`ALTER TABLE profiles DROP COLUMN foodswipe_stage_override`), no
  data loss beyond the overrides themselves. `aiorders-admin-hub` — revert
  the UI diff; no schema or stored-state dependency.
- **Tested:** not drilled — no destructive migration to drill against, and
  no live Postgres reachable from this host either way.
- **Used:** no.

## Health note

No dashboard/monitoring access to either Supabase (`bmnmnejwdxbcqinqkwko`)
or the Cloudflare project behind `aiorders-admin-hub`, from this
department's worktrees — live-deploy status and runtime health are both
unknown here, same boundary this instance's other L1 releases already
carry.

## Observability

Errors on both new routes propagate to each caller's existing `catch`
(`console.error`), consistent with this handler's own pre-existing
convention — nothing new and silent. No audit trail of who set an override
or when — named as a future risk at design time, not an acceptance
criterion, not added here.

## Cost

$0/month delta — one additive nullable column, no new service or
dependency.

## Follow-ups

`ENG-028` (staff-configurable Foodswipe pipeline stage *set*, filed
2026-09-03 per the approver's own Reading A) names this ticket as its sole
dependency (`depends_on: [ENG-013]`) — now satisfied by this merge.
`ENG-028` itself is unaffected in state: its own G1
(`inbox/2026-09-03-eng028-g1-scope.md`) is still unanswered, so a satisfied
dependency doesn't advance it on its own. The raw `error.message` finding
from the security gate is tracked in
`agents/security/notebook/2026-08-31-findings.md` (first occurrence, not
yet a three-strike pattern) — not re-raised here.
