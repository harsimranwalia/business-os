---
ticket: ENG-038
project: aiorders-api
released: 2026-09-05T07:22:20Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 89c6fdb1 (merge of 63f5635, PR #16)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). **Confirmed
  deployed, not just merged** — `brand-portal` (v81), `broadcast-dispatch`
  (v1), `broadcast-unsubscribe` (v1), `outgoing-communications` (v70), all
  version-bumped `2026-09-05T07:25:20Z`-`07:25:55Z`, 3-8 minutes after merge.
  See Deploy below.
rollback_tested: true — disposable-container rehearsal at the migration gate
  (`supabase/postgres:15.8.1.073`), rollback executed and behaviourally
  re-verified (claim rejected again, index gone, constraint gone), not just
  asserted. Not re-drilled against production itself.
health_check: partial — schema/index/constraint existence and cron HTTP
  status confirmed live (read-only); no application-level health check
  exists; no real campaign has ever been created
cost_delta_monthly: 0
---

# Release — Broadcast composer API, dispatch poller, unsubscribe function (ENG-038)

## What shipped

`aiorders-api` gains the full backend surface for restaurant marketing
broadcasts: `brand-portal/broadcasts.ts` (8 actions — list/get/create/update/
pause/resume/cancel/report), `broadcast-dispatch` (cron target, atomic
per-recipient claim, drip scheduling), `broadcast-unsubscribe` (public,
signed-token opt-out), a new `outgoing-communications` `broadcast_message`
consumer case, and a migration widening `broadcast_campaign_recipients`'s
status check to add `'claimed'`, plus a `step_id` index and a
`scheduled_send_at` check constraint. Sub-ticket 2 of 3 under `ENG-019`
(restaurant marketing broadcasts) — `ENG-037` (schema/cron) already shipped;
`ENG-039` (frontend) unblocked by this release. Full detail: `ENG-038`'s own
board file, `agents/database/migrations/ENG-038-broadcast-recipients-claimed-status.md`.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-04-eng038-merge-request.md`, `decision:` still blank).
`aiorders-api` PR #16 was merged directly on GitHub instead, base `main`, no
stacking:

```
$ git merge-base --is-ancestor origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe origin/main
MERGED (is ancestor)
$ gh pr view 16 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-038-broadcast-composer-dispatcher-unsubscribe",
 "mergeCommit":{"oid":"89c6fdb180f85d4f23505eabbba4d064a3b22b7f"},
 "mergedAt":"2026-09-05T07:22:20Z","state":"MERGED"}
```

18 files, 3235 insertions / 7 deletions (`git show --stat` on the merge
commit) — matches this ticket's own recorded diff exactly. All files
confirmed present on `origin/main` directly (`git ls-tree`), not inferred
from the PR's own description.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass (round 6) | principal-engineer | 2026-09-04 |
| Quality (QA) | pass (round 6), 85/85 | qa | 2026-09-04 |
| Security | pass (round 2) | security | 2026-09-04 |
| Migration | pass | database | 2026-09-04 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-05 |

Re-read all four receipts directly before writing this record:
`agents/principal-engineer/reviews/ENG-038.md` (`verdict: pass`),
`agents/qa/test-plans/ENG-038.md` (`last_result: pass`, 85/85, all 7 ACs),
`agents/security/reviews/ENG-038.md` (`verdict: pass`, both round-1 findings
re-verified closed), `agents/database/migrations/ENG-038-broadcast-recipients-claimed-status.md`
(`Gate verdict: pass`). No migration owed beyond this ticket's own.

## Deploy

- **Method: unknown to this department, but confirmed to have happened.** No
  `.github/workflows/` on this repo, same as every prior `aiorders-api`
  release — this department did not run a deploy itself, and nothing here
  triggers one automatically.
- **What actually happened, checked live this pass, not left open:**
  `supabase functions list` shows `brand-portal` (v81), `broadcast-dispatch`
  (v1), `broadcast-unsubscribe` (v1), and `outgoing-communications` (v70) all
  version-bumped between `07:25:20Z` and `07:25:55Z` — 3 to 8 minutes after
  this PR's own `mergedAt` (`07:22:20Z`), and covering exactly the four
  functions this diff touches, no others. Reads as the approver deploying by
  hand immediately after merging (consistent with every other data point in
  `decision-journal.md` on how this approver operates), not an automated
  process — but the department has no direct visibility into who ran it,
  only that it happened and what it touched.
- **Migration:** live, confirmed by direct query — `broadcast_campaign_recipients_status_check`
  includes `'claimed'`; the new `step_id` index present alongside the
  pre-existing `campaign_id`/`status_due_at` ones.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

Read-only queries only, no write against production, no test campaign
created (would dispatch real email/SMS to real customers — out of bounds for
verification). `broadcast-dispatch-tick`'s last 30 minutes of HTTP calls
(`net._http_response`, project-wide, not scoped to this job alone): 9× `200`,
1× `401`, 3× `null` — reads as healthy for the current no-op case (zero
campaigns exist, tick returns fast); not chased further, ongoing traffic
health is devops's standing job, not this release record's.

**One config gap confirmed still open, not closed by this deploy:**
`BROADCAST_UNSUBSCRIBE_SECRET` is absent from `supabase secrets list` (name
checked, not value). `_shared/broadcastUnsubscribe.ts#hmacKey()` throws
without it — dormant today (no campaign has ever been created, and
`ENG-039`, the only UI path to create one, hasn't shipped), same
non-blocking shape as `ENG-037`'s own Vault `service_role_key` prerequisite
(confirmed present, by contrast). Already named in three notebooks (backend
build, review, QA); re-confirmed live here since it turned out to matter
sooner than assumed.

## Acceptance criteria

Full `acceptance-check/SKILL.md` walk run this pass (not the
receipt-bookkeeping shortcut) — this ticket owns all 7 of `ENG-019`'s
criteria per the work-breakdown's own AC-mapping. All 7: **pass**. Full
walk, non-goals check, and cost check:
`agents/product-manager/notebook/2026-09-05-eng038-acceptance.md`.

## Rollback

- **Path:** the migration's own trailing-comment rollback (drop the
  `'claimed'` check value, the `step_id` index, the `scheduled_send_at`
  constraint); the four functions redeploy to their prior version via
  `supabase functions deploy {name}` from the prior commit, or `git revert`
  the merge and redeploy.
- **Tested:** migration rollback yes, against a disposable replica at the
  migration gate (executed, not just asserted). Function-level rollback not
  drilled — no destructive action taken against the live project this pass.
- **Used:** no.

## Health note

Schema and cron-call health confirmed live and reachable. No
application-level health check exists because no restaurant can create a
real campaign yet (`ENG-039` unshipped) — this release has no live usage to
observe, only readiness.

## Observability

`ENG-037`'s named pre-`ENG-038` 404 window is now closed — `broadcast-dispatch`
is deployed and its recent calls return `200`. The `BROADCAST_UNSUBSCRIBE_SECRET`
gap above is the new standing non-blocking item until someone sets it;
self-closes the moment it's configured, same as the Vault secret did for
`ENG-037`.

## Cost

$0/month delta — no new vendor, no new dependency; matches the PRD's own
estimate, re-confirmed at release-readiness and again here.

## Follow-ups

**Unblocks `ENG-039`** (`depends_on: [ENG-038]`) — the family's last
sub-ticket, `restaurant-portal` frontend only. `continue ENG-039` fired this
same pass rather than building it inline. `ENG-019` (parent) still cannot
reach `shipped` until `ENG-039` is settled too (`ADR-003`). Two operational
items remain for whoever next touches deploy config: set
`BROADCAST_UNSUBSCRIBE_SECRET` (above) before any real campaign sends;
`ENG-036`'s shared `systemTriggered` auth bypass on `outgoing-communications`
remains open for every action other than `broadcast_message`.
