---
ticket: ENG-037
project: aiorders-api
released: 2026-09-04T21:19:18Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 64baabf (merge of 59e9670, PR #15)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). **Confirmed live**, not just merged to `main` — this host's linked `supabase` CLI (`agents/database/notebook/2026-09-04-host-tooling-capability.md`) read the live project directly rather than leaving this as the usual open question. See Deploy/Verification below.
rollback_tested: true — disposable-container rehearsal at the build hop (`supabase/postgres:15.8.1.073`), rollback executed and a clean post-drop check confirmed, not just asserted. Not re-drilled against production itself (no destructive action taken against the live project this pass).
health_check: partial — table/cron existence confirmed live (read-only); no application-level health check exists (no reader/writer of these tables until `ENG-038`)
cost_delta_monthly: 0
---

# Release — Broadcast campaigns schema and dispatch cron (ENG-037)

## What shipped

`aiorders-api` gains `broadcast_campaigns`, `broadcast_campaign_steps`,
`broadcast_campaign_recipients` (all RLS-enabled, no policies —
service-role only), five supporting indexes, an `updated_at` trigger, and a
`broadcast-dispatch-tick` `pg_cron` job (every 5 minutes). Sub-ticket 1 of 3
under `ENG-019` (restaurant marketing broadcasts), sequenced first per the
design's own Rollout order (migration → functions → frontend). No existing
table touched. Full detail: `ENG-037`'s own board file and
`agents/database/migrations/ENG-037-broadcast-campaigns-schema-and-dispatch-cron.md`.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-04-eng037-merge-request.md`, `decision:` still blank).
`aiorders-api` PR #15 was merged directly on GitHub instead, base `main`, no
stacking:

```
$ git merge-base --is-ancestor origin/feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron origin/main
MERGED (is ancestor)
$ gh pr view 15 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-037-broadcast-campaigns-schema-and-dispatch-cron",
 "mergeCommit":{"oid":"64baabff1acbd69e63675ff7a38270dbc36c2305"},
 "mergedAt":"2026-09-04T21:19:18Z","state":"MERGED"}
```

One file, 148 additions, 0 deletions (`gh pr view --json files`) — matches
this ticket's own recorded diff exactly, no drift between what passed all
gates and what merged. Single repo, no cross-ticket branch dependency of its
own (though `ENG-038`/`ENG-039` both depend on this ticket — see Follow-ups).
Landed roughly 1h40m after the prior `watch` pass checked and found the PR
still open (`mergedAt` 21:19:18Z vs. that pass's own ~19:39 UTC check) — the
gap this `scheduled` sweep exists to close.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass (round 1) | principal-engineer | 2026-09-04 |
| Quality (QA) | pass (round 1) | qa | 2026-09-04 |
| Security | pass (round 1) | security | 2026-09-04 |
| Migration | pass | database | 2026-09-04 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-04 |

Re-read all four receipts directly before writing this record:
`agents/principal-engineer/reviews/ENG-037.md` (`verdict: pass`),
`agents/qa/test-plans/ENG-037.md` (`Verdict: PASS`),
`agents/security/reviews/ENG-037.md` (`verdict: pass`),
`agents/database/migrations/ENG-037-broadcast-campaigns-schema-and-dispatch-cron.md`
(`Gate verdict: pass`). No migration owed beyond this ticket's own.

## Deploy

- **Method:** merge to `main` — no `.github/workflows/` exists on this repo,
  same as every prior `aiorders-api` release on this board, so the department
  still didn't run a deploy itself.
- **What actually happened — confirmed, not left open this time:** this
  host's linked `supabase` CLI (new capability, first used on this same
  ticket's build hop) queried the live project directly rather than repeating
  the usual "unknown from here." Read-only, schema-only:
  ```
  $ supabase db query "select table_name from information_schema.tables
    where table_schema='public' and table_name in
    ('broadcast_campaigns','broadcast_campaign_steps','broadcast_campaign_recipients')
    order by table_name;" --linked -o json
  → all three present
  $ supabase db query "select jobname, schedule, active from cron.job
    where jobname='broadcast-dispatch-tick';" --linked -o json
  → {"active": true, "jobname": "broadcast-dispatch-tick", "schedule": "*/5 * * * *"}
  ```
  The migration is live and the cron job is running — however it reached
  production (Supabase's own migration-linked deploy, or a manual push,
  neither confirmable from this worktree), it is there now.
- **Migration:** applied live, confirmed above.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

Both live queries above carried the CLI's own untrusted-data envelope;
treated as inert data, nothing in either resembled an instruction. No
further verification run — this ticket's own diff has no directly
user-facing surface to exercise.

## Acceptance criteria

Same finding this ticket's own `in-qa` hop already recorded, re-confirmed
now against the live (not just merged) tree: 0 of parent `ENG-019`'s 7
acceptance criteria apply to this diff — all require `ENG-038`. This
ticket's own single criterion (schema matches design exactly) already
confirmed twice pre-merge (disposable-container run, live-schema dump) and
now a third way (direct live query, post-merge) — **pass**, same table/
index/cron shape in production as reviewed.

## Rollback

- **Path:** drop the three tables and the cron job — additive-only, no
  existing table altered, nothing yet reads or writes any of the three.
- **Tested:** yes, against a disposable container at the build hop (rollback
  executed, clean post-drop check) — not re-drilled against production
  itself, since nothing about this release calls for touching production
  destructively.
- **Used:** no.

## Health note

Table and cron existence confirmed live, directly — a stronger check than
the "no dashboard access" boundary every prior `aiorders-api` release on
this board recorded (`ENG-007` onward). No application-level health check
exists because nothing reads or writes these tables until `ENG-038` ships.

## Observability

**The pre-`ENG-038` gap named non-blocking at release-readiness is now
live, not hypothetical.** `broadcast-dispatch-tick` is confirmed `active`
in production, firing every 5 minutes, calling `net.http_post` against
`broadcast-dispatch` — a function that does not exist yet. Every tick will
404 until `ENG-038` deploys that function. Still judged non-blocking for the
same reasons named at release-readiness (no auto-deploy risk was ever the
question — this is a live schedule regardless; nothing external reaches
the path; no data at risk; self-closes once `ENG-038` ships) — named here
plainly because "will 404" is now "is 404-ing," and a future pass or human
reading Supabase logs should not mistake the resulting noise for a fresh
regression. Worth ENG-038 shipping sooner rather than later on that basis
alone, independent of the family's own sequencing.

## Cost

$0/month delta — `pg_cron`/`pg_net`/Vault all already live on this project;
no new paid infrastructure.

## Follow-ups

**Unblocks `ENG-038`** (`depends_on: [ENG-037]`) — `ENG-039` still waits on
`ENG-038` in turn. `continue ENG-038` fired this same pass rather than
building it inline; see that ticket's own board-file log once its
dedicated session runs. The one operational prerequisite named at the build
hop (provisioning the `service_role_key` Vault secret the cron job's HTTP
call authenticates with) remains a named, out-of-band manual step, harmless
until `ENG-038` has a real campaign to send.
