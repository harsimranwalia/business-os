---
ticket: ENG-005
project: aiorders-admin-hub
released: 2026-08-27T17:12
released_by: devops
autonomy: L1
gate_g3: n/a — L1 merge, no G3 on this lane
commit: 51cdb29 (merged via edf6947, PR #2)
environment: production target (Cloudflare Pages; deploy execution is outside L1 autonomy — see Deploy note, not run by this department)
rollback_tested: false
health_check: not checked — no monitoring/Cloudflare access from this department; see Health note
cost_delta_monthly: 0
---

# Release — Wire A4PosterGenerator into RestaurantDetails.tsx

## What shipped

`aiorders-admin-hub` gets one new card on `RestaurantDetails.tsx`
(`/restaurants/:id/details`), rendering the previously-orphaned
`A4PosterGenerator` component with the four real `Restaurant` fields
(`id`, `name`, `website`, `logo_url`) plus `primaryColor={null}` (the
`Restaurant` interface has no color field). No new route, no new nav entry —
discoverable via the page's existing navigation. Closes the fork
`inbox/requests/2026-08-23-a4-poster-generator-unwired.md` opened: the
component was wanted, not dead code.

## Merge

The approver answered the tracked gate item this time (`inbox/2026-08-27-eng005-merge-request.md`,
`decision: approved`, `decided: 2026-08-28T00:13:09.817494+00:00`, text
"merged") — the normal channel, unlike `ENG-002`'s direct-GitHub-merge/control-center
bypass. Not taken on the text alone; independently verified from scratch in
the department's own worktree (`~/Documents/projects/_eng/aiorders-admin-hub`,
never the human's checkout):

```
$ git fetch origin
   919d355..edf6947  main -> origin/main
$ git merge-base --is-ancestor chore/ENG-005-a4-poster-generator-wire-in origin/main
RESULT: MERGED
$ git log origin/main --oneline -3
edf6947 Merge pull request #2 from harsimranwalia/chore/ENG-005-a4-poster-generator-wire-in
51cdb29 Wire A4PosterGenerator into RestaurantDetails
919d355 Remove supabase/migrations, fully consolidated into aiorders-api
```

`origin/main`'s tip (`edf6947`) is the PR's own merge commit directly on top
of this ticket's commit (`51cdb29`) — `git diff` between the branch tip and
`origin/main` is empty, so no intervening commits landed alongside it. The
merge commit's own timestamp (`2026-08-27T17:12:49-07:00` = `2026-08-28T00:12:49Z`)
lands about 20 seconds before the gate item's `decided:` stamp — consistent
with the approver merging on GitHub and recording the decision in the same
sitting. The gate item's claim checks out.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass | principal-engineer | 2026-08-27 |
| Migration | n/a — no schema change | database | — |
| Quality | pass (structural/build; no suite exists) | qa | 2026-08-27 |
| Security | pass | security | 2026-08-27 |
| Release readiness | pass | devops | 2026-08-27 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-08-28 |

## Deploy

- **Method:** merge to `main` only. Re-confirmed directly this pass (not
  assumed from the ticket's earlier `ready-to-ship` note): `.github/workflows/`
  absent from `origin/main`; `package.json`'s `deploy-cf` script
  (`npm run build && ... wrangler pages deploy dist --project-name=admin-portal`)
  is a manual, explicitly-invoked command, not push-triggered.
- **Why no deploy run:** unlike `ENG-002`, this release genuinely has a new
  production-facing artifact (the poster card becomes reachable once live) —
  so this is a scope boundary, not a "nothing to deploy" call. `aiorders-admin-hub`
  is registered **L1**: the department writes on a branch and opens a PR: a
  human merges, and a human or their own process deploys. Running
  `deploy-cf` would push a production release the department has no autonomy
  to trigger, regardless of diff content. Whether/when the human's own
  process (Cloudflare Pages git integration, or a manual `wrangler` run)
  puts this live is outside this department's visibility — not confirmed
  live, not confirmed pending, genuinely unknown from here.
- **Migration:** none.
- **Feature flag:** none.
- **Duration:** n/a — no deploy executed by this department.

## Verification

Re-run independently against the actual merged tree, in the department's own
worktree (checked out `origin/main` detached, confirmed tree-identical to the
branch tip by empty `git diff` first; the human's own checkout at
`~/Documents/projects/aiorders/aiorders-admin-hub` was not touched):

- `npm run build` → succeeds; bundle now includes `html2canvas`/`purify.es`/
  `index.es` chunks not present in a build with the component unreachable —
  corroborates the component's code path is actually exercised now, not
  merely present in the tree.
- `grep -rn "A4PosterGenerator" src/pages/RestaurantDetails.tsx` → one import,
  one usage (line 904), matching the design.
- Health checks: not run — see `health_check` above. No monitoring or
  Cloudflare dashboard access from this department, and per the Deploy note
  above it isn't established that this is live yet. Nothing here contradicts
  the readiness gate's earlier finding that the component's own pre-existing
  failure paths (no/failed/non-admin session) degrade silently rather than
  crash (`agents/qa/test-plans/ENG-005.md`) — that reasoning is unchanged by
  the merge, just not independently re-observed against live traffic.
- Acceptance criteria: both confirmed against the live (merged) tree — see
  Acceptance criteria below.
- Error rate / latency vs. the hour before: not applicable — no access to
  compare, and not established that a new deploy has actually gone out yet.

## Acceptance criteria

Both re-confirmed against `origin/main` directly, not carried over from the
pre-merge numbers:

1. `A4PosterGenerator` renders without error in a new section on
   `RestaurantDetails.tsx` — `npm run build` succeeds on the merged tree
   (a broken import/prop/JSX in this block would fail the TS/JSX compile
   step); the new `<Card>` sits inside the same `restaurant &&`-guarded
   render branch as every other card on the page. **Pass.**
2. The poster section is reachable via the page's existing navigation, not
   only a direct URL — no new route or nav entry exists on `origin/main`;
   placement is a new `<Card>` on the already-linked-to
   `/restaurants/:id/details` route. **Pass.**

## Rollback

- **Path:** revert `51cdb29` on `main` (single commit, one file changed:
  `src/pages/RestaurantDetails.tsx`).
- **Tested:** no. `aiorders-admin-hub` has no test command
  (`config/projects.md`'s Commands table: lint + build only), so — unlike
  `ENG-002`, where a red/green test run against the revert was possible —
  there is nothing to drill-run a rollback against here. Named as a gap, not
  silently assumed clean.
- **Used:** no.

## Health note

This department has no Cloudflare dashboard access, no production monitoring,
and — per the Deploy section above — no confirmation that a production
deploy carrying this change has actually happened yet. `health_check` is
marked "not checked" rather than "green" deliberately: `ENG-002`'s "green"
meant "nothing that could go newly unhealthy" because nothing was deployed at
all; that reasoning doesn't transfer here, because this release does have a
real new production-facing artifact once whatever deploys `main` catches up
to it. Recorded honestly rather than inferring a status this department
cannot observe.

## Observability

Unchanged. No new endpoint, no new write path — the component's own existing
try/catch and optional-chaining around its edge-function calls
(`agents/security/reviews/ENG-005.md`, `agents/qa/test-plans/ENG-005.md`) is
the only failure path, and it predates this ticket. If it ever fails loudly,
that would show up wherever `aiorders-admin-hub`'s existing (unmonitored by
this department) frontend errors already surface, same as before this ticket.

## Cost

$0/month — reuses the already-deployed `url-shortener` edge function and the
already-installed `jspdf` dependency; no new infrastructure.

## Follow-ups

None committed by this ticket. Whether/when this actually reaches production
is worth a look outside this department's own visibility — nothing here
schedules that check, since the department has no way to run it.
