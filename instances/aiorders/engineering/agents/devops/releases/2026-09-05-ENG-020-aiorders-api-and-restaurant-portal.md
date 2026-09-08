---
ticket: ENG-020
project: aiorders-api + restaurant-portal (one ticket, two repos)
released: 2026-09-06T00:41:23Z (aiorders-api) / 2026-09-06T00:42:57Z (restaurant-portal)
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1 (both)
gate_g3: n/a — L1 lane has no G3; the PR merges are the human gate
commit: aiorders-api PR #17 (MERGED, 672dfa77) | restaurant-portal PR #4 (MERGED, 8eea8f15)
environment: production (Supabase bmnmnejwdxbcqinqkwko + Cloudflare Pages
  restaurant-portal). **Confirmed deployed, not just merged** — `brand-portal`
  function redeployed `2026-09-06T00:45:28Z` (~4 min after merge, by hand, no
  tracked workflow); `restaurant-portal`'s "Deploy to Cloudflare Pages" run
  completed `success` on the merge commit at `2026-09-06T00:43:01Z` (~90s
  after merge, this repo's own push-triggered CI). See Deploy below.
rollback_tested: true — the new `get_acquisition_breakdown` function's own
  `DROP FUNCTION IF EXISTS` was run against a disposable Postgres replica at
  the migration gate, followed by a `pg_proc` lookup confirming zero rows.
health_check: partial — RPC existence and signature confirmed live
  (read-only); no application-level health check exists, and none is needed
  for a read-only reporting page.
cost_delta_monthly: 0
---

# Release — Marketing ROI reporting, acquisition-channel breakdown (ENG-020)

## What shipped

A restaurant owner on the brand portal can now see their own customers,
orders, and revenue broken down by acquisition channel (organic search,
paid, email, social, marketplace, QR, referral, or an always-present
"direct / not tracked" bucket) over a selectable time range. `aiorders-api`
gains a new `brand-portal` action (`get_acquisition_report`) and a read-only
aggregate RPC (`get_acquisition_breakdown`); `restaurant-portal` gains a new
page (`/acquisition`, "Customer Sources" in the sidebar) with a channel
table and an explicit attribution-honesty framing (coverage %, low-volume
caveat, and an organic-search disclaimer distinguishing overall web presence
from AI-SEO's isolated effect). Full detail: `ENG-020`'s own board file,
`agents/architect/designs/ENG-020-marketing-roi-attribution-reporting.md`.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-05-eng020-merge-request.md`, `decision:` stays blank). Both
PRs merged directly on GitHub instead, 94 seconds apart — together, as both
PR bodies required (either alone would have left the portal rendering a
tested "not available yet" state, not a defect, but not the finished
feature either):

```
$ gh pr view 17 --repo harsimranwalia/aiorders-api --json state,mergedAt,baseRefName,mergeCommit
{"baseRefName":"main","mergeCommit":{"oid":"672dfa77ce33ac6ec1aa6918c21a2c563cbe3873"},"mergedAt":"2026-09-06T00:41:23Z","state":"MERGED"}
$ gh pr view 4 --repo harsimranwalia/restaurant-portal --json state,mergedAt,baseRefName,mergeCommit
{"baseRefName":"main","mergeCommit":{"oid":"8eea8f15bf49f570ded0fdd57b9cf4e5fce1798e"},"mergedAt":"2026-09-06T00:42:57Z","state":"MERGED"}
```

Zero drift confirmed on both sides: `git diff {reviewed-branch-tip}
origin/main --stat` empty on both repos, and each merge commit's own parents
(`git log -1 --format='%H %P'`) show the reviewed branch tip
(`cd82579`/`5783a2d`) merged in as-is — no squash, nothing folded in beyond
what every gate already reviewed.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Migration | pass — additive `SECURITY DEFINER` RPC only, no table/column change; rollback tested against a disposable replica | database | 2026-09-05 |
| Code review | pass, round 3 (round 1 and round 2 both passed too — this ticket's only rounds were on the quality gate, not review) | principal-engineer | 2026-09-05 |
| Quality | pass, round 3 (round 1 failed: zero frontend test coverage for AC1-4; round 2 failed narrower: AC4's coverage-sentence and low-volume-caveat mechanisms untested; round 3: all 5 acceptance criteria pass, 32/32 restaurant-portal tests, 40/40 aiorders-api tests) | qa | 2026-09-05 |
| Security | pass, round 1 — access control mutation-verified, not just read; one non-blocking finding (a pre-existing, shared restaurant-existence oracle, not introduced here) | security | 2026-09-05 |
| G3 | n/a — L1 lane has no G3; the PR merges are the human gate | approver | 2026-09-06 |

Re-read all four receipts directly before writing this record:
`agents/database/migrations/ENG-020-marketing-roi-attribution-reporting.md`
(`Gate verdict: pass`), `agents/principal-engineer/reviews/ENG-020.md`
(round 3, `pass`), `agents/qa/test-plans/ENG-020.md` (`last_result: pass`,
all 5 ACs), `agents/security/reviews/ENG-020.md` (`verdict: pass`) — all
current, none stale.

## Deploy

- **Method:** merge to `main` on both repos, each redeployed independently —
  `aiorders-api` by hand (no CI on this repo, same as every prior release
  here), `restaurant-portal` via its own existing push-triggered GitHub
  Actions workflow.
- **What actually happened, checked live this pass:** `supabase functions
  list` shows `brand-portal` version-bumped `2026-09-06T00:45:28Z`, ~4
  minutes after `aiorders-api` PR #17's own `mergedAt` — reads as the
  approver deploying by hand immediately after merging, the same pattern
  `decision-journal.md` already has multiple data points for. `gh run list`
  on `restaurant-portal` shows "Deploy to Cloudflare Pages" completed
  `success` on head `8eea8f15` (the merge commit itself) at
  `2026-09-06T00:43:01Z`, ~90 seconds after merge — this repo's own tracked
  CI, not a by-hand action.
- **Migration:** live, confirmed by direct query — `supabase db query
  --linked` against `bmnmnejwdxbcqinqkwko` returns `get_acquisition_breakdown(p_restaurant_id
  uuid, p_from timestamp with time zone, p_to timestamp with time zone)`,
  matching the design's signature exactly.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

Read `git show origin/main:supabase/functions/brand-portal/acquisition.ts`
and `git show origin/main:src/pages/acquisition/Index.tsx` directly (both
confirmed identical to the reviewed tips, no drift). Confirmed the
`verifyRestaurantAccess`/`access.hasAccess` gate precedes the RPC call, the
always-present `direct_unknown` bucket, the preset-driven `queryKey`
refetch, and all four AC4 framing mechanisms (subtitle, coverage sentence,
low-volume caveat, organic-search disclaimer) render from the response
verbatim. No test campaign or write action taken against production — this
is a read-only reporting surface with nothing to exercise destructively.

## Acceptance criteria

Full `acceptance-check/SKILL.md` walk run this pass (not the
receipt-bookkeeping shortcut) — this ticket owns all 5 of its own PRD's
criteria. All 5: **pass**. Full walk, non-goals check, and cost check:
`agents/product-manager/notebook/2026-09-05-eng020-acceptance.md`.

## Rollback

- **Path:** `DROP FUNCTION IF EXISTS public.get_acquisition_breakdown(...)`
  (the migration's own trailing rollback), then revert either merge commit
  — neither diff changes existing behavior, so reverting fully undoes it.
  `restaurant-portal`'s `deploy-cf.yml` redeploys the prior build
  automatically on a revert-and-push; `aiorders-api` has no CI, so a revert
  there needs the same by-hand redeploy the original merge got.
- **Tested:** migration rollback yes, against a disposable replica at the
  migration gate (executed and behaviourally re-verified, not just
  asserted). Function-level/frontend rollback not drilled — no destructive
  action taken against the live project this pass.
- **Used:** no.

## Health note

RPC existence and signature confirmed live and reachable; the frontend's own
deploy completed successfully. No application-level health check exists
because none is meaningful here — a read-only report page with no
background job, cron, or async delivery path to monitor.

## Observability

Both RPC failure branches (migration-not-yet-applied, generic error) log
server-side (`console.error`) before returning a fixed client message,
confirmed by reading `acquisition.ts` directly — the one scenario that could
otherwise be a silent gap (portal shipping ahead of backend) is an explicit,
tested case, not a dormant risk.

## Cost

$0/month delta — no new vendor, no new dependency (confirmed fresh via `git
diff origin/main...HEAD -- '*.json' '*.lock'`, empty on both repos); one new
Postgres function on already-running infrastructure. Matches the PRD's own
estimate.

## Follow-ups

`blocks: []` — nothing else on the board depends on this ticket; no chain
fired as a result of this release. The PRD's own non-goals (Clarity
integration, a true ROI ratio, isolating AI-SEO specifically, a staff-facing
all-restaurants rollup) remain unfiled — this ticket's G1 was a bare
approval, not an explicit sequence sign-off, so `acceptance-check/SKILL.md`
step 6b does not auto-file any of them (see the acceptance notebook entry).
The recurring quality-gate shape this ticket surfaced twice (a gap's own
prose naming more mechanisms than its "specific fix" bullet delivers) is
already tracked in `observations.md`, not repeated here.
