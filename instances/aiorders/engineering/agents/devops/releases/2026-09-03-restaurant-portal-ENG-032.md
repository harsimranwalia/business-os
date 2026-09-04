---
ticket: ENG-032
project: restaurant-portal
released: 2026-09-04T04:56:20Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 5276a53 (merge of 77631b0, PR #2)
environment: production (Cloudflare Pages, `deploy-cf.yml`). Merge confirmed on `origin/main`; the push-triggered workflow's own run status is not checked from this worktree — no CI dashboard access from this department. See Health note.
rollback_tested: false — reasoned, not drilled (no way to trigger/observe a GitHub Actions run from this host). Reasoning: no migration, pure UI plus an existing-jsonb-column save-path fix; reverting the merge commit on `main` re-triggers `deploy-cf.yml` and redeploys the prior build.
health_check: not checked — no dashboard/monitoring access to this Cloudflare Pages project from this department; see Health note
cost_delta_monthly: 0
---

# Release — Catering board: two new stages, itemized owner view, order-form enable switch (ENG-016 Piece 1, sub-ticket 2 of 4)

## What shipped

The catering board's two new outcomes from Piece 1 (`Quote Generated`,
`Contact Requested`) are now recognized everywhere the stage list was
hardcoded — `CateringKanban.tsx` (`columns` + `statusConfig`),
`CateringDetailModal.tsx`, `StatusUpdateModal.tsx`,
`ArchivedCateringModal.tsx`, `CateringForm.tsx`, `CateringCalendar.tsx`,
`CateringRequestCard.tsx`, `pages/catering/Index.tsx`, `index.css`. An
existing request in any of the five prior stages is unaffected (AC-8). The
owner's detail modal gains a read-only itemized-selections block, grouped by
category (AC-12, narrowed to this ticket's own slice). The owner-side
catering editor gains an `orderFormEnabled` switch (default off, `ADR-009`)
and a per-fulfillment-option copy editor, and its save path now spreads
`...content` before its normalised fields so keys outside the known field
list survive a save — fixing a real, live silent-revert bug in the same
commit.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-03-eng032-merge-request.md`, `decision:` still blank).
`restaurant-portal` PR #2 was merged directly on GitHub instead. Confirmed
independently via local git ancestry (`eng_build_loop.md` step 5), then
cross-checked with `gh pr view` on top of the local-git-only floor (not
required at this severity, done anyway since the check is cheap and this
sweep already had the tool open for `ENG-008`/`009`/`010`/`013`'s own
recheck):

```
$ git merge-base --is-ancestor origin/feat/ENG-032-catering-portal-stages-and-itemized-view origin/main && echo YES
YES
$ gh pr view 2 --repo harsimranwalia/restaurant-portal --json state,mergedAt,mergeCommit
{"mergeCommit":{"oid":"5276a53345527c2a59b426eaa8b74fbea6a9ca83"},"mergedAt":"2026-09-04T04:56:20Z","state":"MERGED"}
```

`origin/main`'s tip (`5276a53`) is exactly that merge commit. The branch tip
(`77631b0`) matches this ticket's own `ready-to-ship → blocked` log entry
with zero drift — `77631b0` is itself the merge-base of the branch and
`main`, i.e. the whole branch is cleanly contained. Single repo, no
cross-ticket branch dependency (`ENG-033` depends on this shipping, not the
reverse).

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass, round 2 (round 1 failed: missing regression test on the save-path fix, closed) | principal-engineer | 2026-09-03 |
| Quality (QA) | pass | qa | 2026-09-03 |
| Security | pass, one non-blocking finding routed to `proposals.md` | security | 2026-09-03 |
| Migration | n/a — no schema or data change | database | 2026-09-03 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-04 |

Re-read all three receipts directly before writing this record, not taken
from the ticket's own narrative: `agents/principal-engineer/reviews/ENG-032.md`
(`verdict: pass`), `agents/qa/test-plans/ENG-032.md` (`last_result: pass`),
`agents/security/reviews/ENG-032.md` (`verdict: pass`). No
`agents/database/migrations/ENG-032-*.md` — correct, confirmed no `*.sql` in
the diff.

## Deploy

- **Method:** merge to `main` triggers `.github/workflows/deploy-cf.yml`
  (push-triggered, `npm run deploy-cf`) — new since `ENG-002`'s own release
  on this repo (2026-08-26), which had no CI/CD at all. Confirmed present on
  `origin/main` by reading the workflow file directly.
- **Why this department didn't run it:** `restaurant-portal` is registered
  **L1** — a human merges; the workflow itself runs unattended on GitHub's
  side once merged, outside this department's own action.
- **What actually happened:** unknown from here — this worktree has no
  access to the Actions run log or Cloudflare Pages dashboard for this
  project.
- **Migration:** none.
- **Feature flag:** none — `orderFormEnabled` defaults off per-restaurant
  (`ADR-009`), not a global flag.
- **Duration:** n/a — no deploy run by this department.

## Verification

Re-verified directly against the merged tree, not just the receipts'
account: `git show origin/main:src/components/catering/CateringKanban.tsx`
confirms both `'Quote Generated'` and `'Contact Requested'` present in both
the `columns` and `statusConfig` structures; `git show
origin/main:src/components/catering/CateringDetailModal.tsx` confirms the
`CateringSelection` interface and the `selections`-driven render block are
present; `git show
origin/main:src/components/website/CateringPageForm.tsx` confirms the
`...content` spread precedes the normalised fields and the
`orderFormEnabled` switch is wired to `form.orderFormEnabled`/`set(...)`.
Health checks: not run — see `health_check` above.

## Acceptance criteria

Re-checked against `origin/main`
(`agents/architect/designs/ENG-016-catering-quote-generator.md`):

- **AC-8** (an existing request in any of the five current stages stays
  visible once the two new stages are added to every hardcoded list).
  **Pass** — QA's own mutation-verified test (`CateringKanban.test.tsx`)
  re-read directly (`last_result: pass`); the two new entries are additive
  appends confirmed on the merged tree, no existing key removed or
  reordered.
- **AC-12** (itemized selections render grouped by category in the owner's
  detail modal), narrowed per the design to this ticket's own
  `restaurant-portal` slice. **Pass** — QA's own mutation-verified test
  (`CateringDetailModal.test.tsx`) re-read directly; the render block's
  presence re-confirmed on `origin/main` per Verification above.

## Rollback

- **Path:** revert the single merge commit — no migration, no stored-state
  change; `deploy-cf.yml` re-triggers on the revert and redeploys the prior
  build.
- **Tested:** not drilled — see `rollback_tested` above.
- **Used:** no.

## Health note

No dashboard/monitoring access to this Cloudflare Pages project or its
GitHub Actions run history from this department's worktree, so whether the
deploy actually ran and is healthy is unknown from here — same boundary
`ENG-002`'s release already named, now with a real CI workflow in between
that this department still can't observe the result of.

## Observability

The one named throw risk (a `columns` entry with no matching `statusConfig`
entry) is mutation-tested pre-merge (QA's AC-8 test). No client-side runtime
error tracking exists anywhere in this repo — a pre-existing gap across this
whole instance, not introduced or worsened by this ticket, same posture
already accepted at this gate on `ENG-002`.

## Cost

$0/month delta — no new dependency, no new service; confirmed no
`package.json`/lockfile change in the diff (`git diff origin/main...HEAD
--stat` before merge carried none), reuses existing Cloudflare Pages
capacity and `ENG-031`'s existing `catering` columns.

## Follow-ups

Unblocks `ENG-033`'s sole remaining dependency (`depends_on: [ENG-031,
ENG-032]`, `ENG-031` already `verified`) — see that ticket's own board-file
log for this pass's dispatch decision. The security gate's one non-blocking
finding (QA's claim that `ENG-022`'s suite covers `brand-portal/catering.ts`
was overstated — it doesn't) is not re-derived here, already routed to
`agents/eng-manager/proposals.md` (2026-09-03, security, `aiorders-api`) and
`agents/security/notebook/2026-09-03-findings.md`. The `ENG-016` family
(parent plus `ENG-031`..`034`) is not itself `shipped`/`verified` — per
`ADR-003`, two siblings (`ENG-033`, `ENG-034`) remain unbuilt.
