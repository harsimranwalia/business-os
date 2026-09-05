---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-api
ticket: ENG-038
time_estimate: ~2-3 days
recommendation: merge — code review (round 6), quality (round 6), security (round 2), and the migration gate all passed; closes a live gap (ENG-037's cron has been firing every 5 minutes against this function since it merged, currently failing since the function doesn't exist — harmless today, zero rows in any broadcast table); five non-blocking findings named below, none blocking
pr_url: https://github.com/harsimranwalia/aiorders-api/pull/16
raised: 2026-09-04
notified: 2026-09-04T21:06:41
nudged:
decision:
---

# Merge request — broadcast composer API, dispatch poller, unsubscribe function (ENG-038)

Sub-ticket 2 of 3 under `ENG-019` (restaurant marketing broadcasts). `ENG-037`
(schema + dispatch cron) already merged; `ENG-039` (frontend) waits on this
one.

## What this does

- `brand-portal/broadcasts.ts` — compose/edit/pause/resume/cancel/report on a
  broadcast campaign, audience capped at 10,000 recipients, minimum 24h
  between campaigns per restaurant.
- `broadcast-dispatch/index.ts` — the cron target `ENG-037`'s
  `broadcast-dispatch-tick` calls every 5 minutes: promotes due campaigns,
  enrolls audiences, atomically claims and dispatches due recipients.
- `outgoing-communications/actors/consumers.ts` — new `broadcast_message`
  case, locked to an already-claimed `recipientId`; no caller-supplied
  content or recipient.
- `broadcast-unsubscribe/index.ts` — public, signed-token unsubscribe
  endpoint.
- Migration — widens the recipient status check to add `'claimed'`, indexes
  `step_id`, constrains `scheduled_send_at`.

## Gates passed

- **Code review: pass, round 6** — `agents/principal-engineer/reviews/ENG-038.md`.
  0/10 automatic failures.
- **Quality: pass, round 6** — `agents/qa/test-plans/ENG-038.md`. 85/85, all
  seven PRD acceptance criteria covered.
- **Security: pass, round 2** — `agents/security/reviews/ENG-038.md`. Both
  round-1 blocking findings (unauthenticated arbitrary-content send; no
  audience/interval cap) verified closed against the code and schema, not
  just the fix notebook's account of them.
- **Migration: pass** — `agents/database/migrations/ENG-038-broadcast-recipients-claimed-status.md`.
  Additive-only; rollback actually executed against a disposable replica and
  behaviourally re-verified.

## PR

- `aiorders-api`: https://github.com/harsimranwalia/aiorders-api/pull/16

This project is registered **L1** — merge whenever suits you on GitHub
directly; the next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket once it's in.

## Named gaps, carried forward rather than hidden

- **TOCTOU race, low severity.** `tooSoonSinceLastCampaign` reads then later
  writes with no lock — two near-simultaneous `create_broadcast` calls for
  the same restaurant can both pass the 24h check. Bounded: the audience-size
  cap has no equivalent race; exploiting this needs an already-authenticated
  restaurant-owner credential.
- **A recipient row stuck at `status = 'claimed'`** if the process is killed
  mid-send. No automatic recovery sweep; self-diagnosable via one query
  (given in the migration file's own comment), bounded to a missed send.
- **`cancel_broadcast` doesn't flip already-claimed rows to `cancelled`** —
  narrow window, pre-existing since the original build.
- **`enrollAudience`'s restaurant-scoping has no dedicated cross-tenant
  regression test**, though no caller-supplied cross-tenant vector exists on
  this path.
- **`ENG-036`'s shared `systemTriggered` auth bypass on
  `outgoing-communications` is untouched** — every action other than
  `broadcast_message` stays exposed until `ENG-036` ships.

## Deploy-time note — time-sensitive once merged, not a reason to hold the PR

Checked directly against the linked project this pass (`supabase functions
list`, `cron.job`): `ENG-037`'s `broadcast-dispatch-tick` cron has been
`active` and firing every 5 minutes since that PR merged (~14:19 PDT today);
`broadcast-dispatch` isn't deployed yet, so every tick is currently failing
at the routing layer. Harmless right now — all three broadcast tables are
still empty, no campaign has ever been created, and nothing external reaches
this path before `ENG-039` ships. Two things for whoever deploys this
function:

1. Deploying it closes that window.
2. The cron's outbound call still needs the service-role bearer key
   available via Supabase Vault (`broadcast-dispatch/auth.ts`) — until
   `vault.create_secret(...)` runs once for it, calls will fail auth instead
   of 404. Already named on `ENG-037`'s own merge request; still
   outstanding, not this ticket's to close.

## Decision

No reply was written here. `aiorders-api` PR #16 was merged directly on
GitHub instead, base `main`, no stacking:

```
$ git merge-base --is-ancestor origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe origin/main
MERGED (is ancestor)
$ gh pr view 16 --json state,mergedAt,baseRefName,headRefName,mergeCommit
{"baseRefName":"main","headRefName":"feat/ENG-038-broadcast-composer-dispatcher-unsubscribe",
 "mergeCommit":{"oid":"89c6fdb180f85d4f23505eabbba4d064a3b22b7f"},
 "mergedAt":"2026-09-05T07:22:20Z","state":"MERGED"}
```

Found by this `scheduled` sweep's own step-5 merge detection
(2026-09-05, 02:00 PDT pass). All four gate receipts (review/quality/
security/migration) re-read fresh and confirmed `pass`; a full
acceptance-check (all 7 owned criteria) run against the live, deployed code
— not just the merged commit, since all four touched functions turned out
to already be deployed too (see the ticket's own board-file log and
`agents/devops/releases/2026-09-05-aiorders-api-ENG-038.md`). Carried
`blocked → shipped → verified` this pass. Unblocked `ENG-039`; `continue
ENG-039` fired the same pass.
