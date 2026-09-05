---
ticket: ENG-039
project: restaurant-portal
released: 2026-09-05T17:05:41Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: aeeb7b9 (merge of 2f438e0, PR #3)
environment: production (Cloudflare Pages, `deploy-cf.yml`). Merge confirmed on `origin/main`; the push-triggered workflow's own run status is not checked from this worktree — no CI dashboard access from this department. See Health note.
rollback_tested: false — reasoned, not drilled (no way to trigger/observe a GitHub Actions run from this host). Reasoning: no migration, pure additive frontend diff (9 new/modified files, 0 deletions); reverting the merge commit on `main` re-triggers `deploy-cf.yml` and redeploys the prior build.
health_check: not checked — no dashboard/monitoring access to this Cloudflare Pages project from this department; see Health note
cost_delta_monthly: 0
---

# Release — Broadcasts tab, composer, drip editor, report UI (ENG-039, sub-ticket 3 of 3 under ENG-019)

## What shipped

A third "Broadcasts" tab on the Automations page: a paginated campaign list
(`Broadcasts.tsx`); a composer (`BroadcastComposer.tsx`) for a one-time
message or a 2+-step drip, with an audience picker (all customers /
inactive-for-N-days), per-step email and/or SMS content, an optional
existing-offer coupon attach, and send-now-or-schedule, locking to read-only
once a campaign starts sending; row actions to pause/resume/cancel; a report
view (`BroadcastReport.tsx`) showing recipient status counts,
delivery-by-channel, and coupon redemptions/revenue. Consumes `ENG-038`'s
already-shipped, already-verified API exactly as it exists on `origin/main`
— no new backend route, no schema change, no new dependency. Last of
`ENG-019`'s three work-breakdown sub-tickets.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-05-eng039-merge-request.md`, `decision:` still blank).
`restaurant-portal` PR #3 was merged directly on GitHub instead. Confirmed
independently via local git ancestry (`eng_build_loop.md` step 5), then
cross-checked with `gh pr view`:

```
$ git merge-base --is-ancestor 2f438e0 origin/main && echo YES
YES
$ gh pr view 3 --json state,mergedAt,mergeCommit,baseRefName
{"baseRefName":"main","mergeCommit":{"oid":"aeeb7b9a4f3c97a26c2af1a2981053bd98f8656b"},
 "mergedAt":"2026-09-05T17:05:41Z","state":"MERGED"}
```

`origin/main`'s tip (`aeeb7b9`) is exactly that merge commit, with `5276a53`
(the pre-merge `main`, `ENG-032`'s own merge) and `2f438e0` (this ticket's
reviewed branch head) as its two parents. `git diff 2f438e0 aeeb7b9 --stat`
is empty — the merge introduced zero drift from the code all three gates
reviewed. Single repo, no cross-ticket branch dependency for this PR itself.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass, round 1 | principal-engineer | 2026-09-05 |
| Quality (QA) | pass, round 1 (14/14) | qa | 2026-09-05 |
| Security | pass, round 1, zero findings | security | 2026-09-05 |
| Migration | n/a — no schema or data change | — | — |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-05 |

Re-read all three receipts directly before writing this record, not taken
from the ticket's own narrative: `agents/principal-engineer/reviews/ENG-039.md`
(`verdict: pass`), `agents/qa/test-plans/ENG-039.md` (`last_result: pass`),
`agents/security/reviews/ENG-039.md` (`verdict: pass`). No
`agents/database/migrations/ENG-039-*.md` — correct, confirmed no `*.sql` in
the diff and `git diff 5276a53 aeeb7b9 --stat` touches only 9
`src/**`/test files.

## Deploy

- **Method:** merge to `main` triggers `.github/workflows/deploy-cf.yml`
  (push-triggered, `npm run deploy-cf`) — confirmed present on the merge
  commit directly (`git show aeeb7b9:.github/workflows/deploy-cf.yml`).
- **Why this department didn't run it:** `restaurant-portal` is registered
  **L1** — a human merges; the workflow itself runs unattended on GitHub's
  side once merged, outside this department's own action.
- **What actually happened:** unknown from here — this worktree has no
  access to the Actions run log or Cloudflare Pages dashboard for this
  project (same boundary `ENG-002`'s and `ENG-032`'s own releases on this
  repo already named).
- **Migration:** none.
- **Feature flag:** none — reachability is additive (a new tab); no
  restaurant is opted in or out.
- **Duration:** n/a — no deploy run by this department.

## Verification

Re-verified directly against the merged tree at `aeeb7b9`, not just the
receipts' account — see Acceptance criteria below for the specific
`git show` citations per criterion. Health checks: not run — see
`health_check` above.

## Acceptance criteria

This ticket owns AC1–AC5 of `ENG-019`'s 7 (per
`agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`'s own
AC-mapping; AC6/AC7 are fully backend-enforced, `ENG-038`'s own). Full walk:
`agents/product-manager/notebook/2026-09-05-eng039-acceptance.md`. Summary,
re-checked against `origin/main` directly:

- **AC1** (send immediately or schedule for a future date/time). **Pass** —
  `scheduleLater`/`scheduleDate`/`scheduleTime` state plus the
  `send_at`-omitted-means-immediate submit path
  (`BroadcastComposer.tsx:107-109,183-215`).
- **AC2** (drip sequence, 2+ steps, each with its own configured delay).
  **Pass** — per-step `delay_hours` editor bound to `BROADCAST_DELAY_OPTIONS`
  (`BroadcastComposer.tsx:167-169,363-385`); the delay mechanics themselves
  are `ENG-037`/`ENG-038`'s own, already verified.
- **AC3** (audience: all customers / inactive-for-N-days, scoped to the
  owner's own restaurant). **Pass** — `audience_mode`/`inactive_days` picker
  (`BroadcastComposer.tsx:127-128,206,302-305`); `restaurantId` sourced from
  `useRestaurant()`'s session-derived context, never a URL/route param —
  already independently confirmed by security round 1, re-cited rather than
  re-derived.
- **AC4** (coupon redemption count and revenue on the campaign's own page).
  **Pass** — `report.redemptions`/`report.revenue` rendered as "Redemptions"
  and "Revenue" cards, gated on `!== null` so no-coupon reads as absent, not
  zero (`BroadcastReport.tsx:101-122`).
- **AC5** (send logged and visible in the campaign's own history). **Pass**
  — `recipients_by_status`/`delivery_by_channel` rendered in the report
  dialog, reachable per-campaign from the list's "View report" action
  (`BroadcastReport.tsx:41,59`; `Broadcasts.tsx:202,276-281`); the
  underlying log write is `ENG-038`'s own, already verified.

No scope creep found: `types/autopilot.ts`, `Templates.tsx`, and every
reactive `Automations` flow confirmed untouched on `origin/main`
(`git diff 5276a53 aeeb7b9 --stat` names only the 9 files the ticket's own
Outcome section lists). Cost matches ($0/month).

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
`ENG-002`'s and `ENG-032`'s own releases on this repo already named.

## Observability

No client-side runtime error tracking exists anywhere in this repo — a
pre-existing gap across this whole instance, not introduced or worsened by
this ticket, same posture already accepted at this gate on `ENG-002`/`ENG-032`.

## Carried-forward gaps — not this release's to fix

Named in full in the merge request and devops's own release-readiness log
(`agents/devops/notebook/2026-09-05-release-readiness-log.md`), repeated
here because this is the release that makes both reachable for the first
time:

1. **`BROADCAST_UNSUBSCRIBE_SECRET` not provisioned** on the `aiorders-api`
   side — every real send throws minting the unsubscribe link; caught,
   logged, recipient marked `failed` (visible in this ticket's own Report
   view), not silent. One `supabase secrets set` command closes it. Not
   re-checked live this pass — it belongs to a different project
   (`aiorders-api`'s Supabase functions), not this frontend-only release.
2. **SMS delivery entirely mocked** codebase-wide
   (`outgoing-communications/services/sms.ts`) — any campaign step with SMS
   content reports `status: 'sent'` for every recipient while delivering
   nothing. Pre-existing, untouched by `ENG-037`/`ENG-038`/`ENG-039`.
   Already a tracked proposal (`agents/eng-manager/proposals.md`,
   2026-09-03/09-04 rows, `architect`).

Neither blocks this release — both are pre-existing conditions in
already-shipped, unrelated code.

## Cost

$0/month delta — no new dependency, no new service; confirmed no
`package.json`/lockfile change in the diff (code review's automatic-failure
scan #6, re-confirmed via `git diff 5276a53 aeeb7b9 --stat`: no `.json`/
`.lock` file touched), reuses existing Cloudflare Pages capacity.

## Follow-ups

This is the last of `ENG-019`'s three work-breakdown sub-tickets
(`ENG-037`, `ENG-038`, both already `verified`) — with this one now
`verified`, every child of `ENG-019` is settled and at least two shipped,
so the parent qualifies for its own `ADR-003`-class exemption. `continue
ENG-019` fired this same pass so the parent can advance on its own next
hop.
