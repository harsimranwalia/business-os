---
ticket: ENG-009, ENG-010
project: aiorders-api, aiorders-admin-hub
released: 2026-09-04T15:40:31Z
released_by: approver (direct GitHub merge of a new consolidating PR on each repo, no written reply to either ticket's own merge-request item)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: "aiorders-api 5415ef0 (merge of #14, merge/ENG-009-ENG-010-to-main -> main); aiorders-admin-hub f5de339 (merge of #9, same branch name)"
environment: production (Supabase project bmnmnejwdxbcqinqkwko for aiorders-api; Cloudflare Workers for aiorders-admin-hub). Corrected 2026-09-04, post-release: `aiorders-api`'s edge function (`admin-portal`) and both migrations ARE confirmed deployed/applied — done by the approver directly (via this session's own Claude Code assistant), outside this department's pipeline. `aiorders-admin-hub`'s own deploy status is still unconfirmed from here. See the dated addendum below, not the Deploy section above it (left as originally written, per this board's own amend-don't-rewrite convention).
rollback_tested: false — reasoned, not drilled. Reasoning below is corrected 2026-09-04: this release DOES carry a migration on `aiorders-api` (two new nullable columns, one new isolated table) — see addendum. Reverting the merge commit alone would leave the schema in place, which is fine (both additions are inert without the code), but is no longer "fully undoes the diff" as originally reasoned.
health_check: not checked from this department (still true for `aiorders-admin-hub`). For `aiorders-api`: `supabase migration list` reconfirmed both migrations applied post-deploy — see addendum.
cost_delta_monthly: 0
---

# Release — Influencer engagement info (ENG-009) and influencer relationship notes (ENG-010)

## What shipped

Two tickets, landed by one action per repo:

- **ENG-009** (`aiorders-admin-hub`, primary): three new fields on the
  existing `PATCH /admin-portal/influencers/{id}` handler (`followers`,
  `engagement`, `social_stats_platform`) plus a new `GET
  /admin-portal/influencers/activity` route — an internal activity signal
  and a staff-editable social stat.
- **ENG-010** (`aiorders-admin-hub`, primary): a staff log for influencer
  personality, preferences, and off-platform conversation notes
  (`relationship_notes`, `getInfluencerNotes`), RLS-protected.

Both touch `aiorders-api` and `aiorders-admin-hub`. Both stacked their
branch on `ENG-008`'s (`ENG-009` on `feat/ENG-008-...`, `ENG-010` on
`feat/ENG-009-...` in turn) and each originally opened its own pair of PRs
against that stacked base, not `main`.

## Merge — two hops, not one

**Hop 1 (2026-09-04, ~06:06–06:10 UTC):** this department's own four PRs
(`aiorders-api` #7 `ENG-009`, `aiorders-admin-hub` #6 `ENG-009`,
`aiorders-api` #8 `ENG-010`, `aiorders-admin-hub` #7 `ENG-010`) were merged
directly on GitHub, each into its configured stacked base — not `main`.
Neither ticket shipped. This department's own `scheduled` sweep found and
recorded this first ("merged, but did not ship") the same morning; both
merge-request items were amended in place; see `decision-journal.md`'s
`2026-09-04 | ENG-009 / ENG-010` row.

**Hop 2 (2026-09-04, 15:39:16Z / 15:40:31Z):** a **new** PR on each repo,
`merge/ENG-009-ENG-010-to-main` (`aiorders-api` #14, `aiorders-admin-hub`
#9), base `main`, head the stacked branch's own current tip — carrying both
tickets' commits in one shot (they were stacked on each other already) —
opened and merged directly on GitHub. This is the resolution `ENG-009`'s
own board log had left as an open question ("a fresh PR from the current
stacked-branch tip, or extracting this ticket's own commits onto a clean
branch off current `main`"); the approver took the first option, by hand.
No reply was written to either ticket's own tracked merge-request item at
any point in either hop.

```
$ git fetch origin   # both worktrees
$ git merge-base --is-ancestor d37e0c9 origin/main && echo YES   # ENG-009, aiorders-api
YES
$ git merge-base --is-ancestor 92bcacd origin/main && echo YES   # ENG-009, aiorders-admin-hub
YES
$ git merge-base --is-ancestor 486eec0 origin/main && echo YES   # ENG-010, aiorders-api
YES
$ git merge-base --is-ancestor 8b90f0e origin/main && echo YES   # ENG-010, aiorders-admin-hub
YES
$ gh pr view 14 --repo harsimranwalia/aiorders-api --json state,mergedAt,mergeCommit
{"state":"MERGED","mergedAt":"2026-09-04T15:39:16Z","mergeCommit":{"oid":"5415ef054dab27071951d1ff7dc034abc9394036"}}
$ gh pr view 9 --repo harsimranwalia/aiorders-admin-hub --json state,mergedAt,mergeCommit
{"state":"MERGED","mergedAt":"2026-09-04T15:40:31Z","mergeCommit":{"oid":"f5de3395c0f88ac13cc13b709d45dde2d84c2fcb"}}
```

Checked against each ticket's own **recorded** commit (frontmatter
`branch:`), not a live branch tip — the check this board adopted after
`ENG-008`'s branch-tip-contamination false-negative, and doubly relevant
here since both original stacked branches are still live and still not
ancestors of `main` on their own.

## Gates

Both tickets, full lane, all three receipts re-read directly (not taken
from either ticket's own narrative):

| Ticket | Code review | QA | Security |
|---|---|---|---|
| ENG-009 | pass (`agents/principal-engineer/reviews/ENG-009.md`) | pass (`agents/qa/test-plans/ENG-009.md`) | pass (`agents/security/reviews/ENG-009.md`) |
| ENG-010 | pass (`agents/principal-engineer/reviews/ENG-010.md`) | pass (`agents/qa/test-plans/ENG-010.md`) | pass (`agents/security/reviews/ENG-010.md`) |

No migration on either ticket — no `*.sql` in either diff, either repo.
G3: n/a, L1 lane.

## Deploy

- **Method:** merge to `main` only — no CI/CD auto-deploy exists on either
  repo (`.github/workflows/` absent from `origin/main` on both, same as
  every prior release on this board).
- **Why this department didn't run it:** both repos are registered **L1** —
  a human merges; running the deploy would exceed this department's
  autonomy.
- **What actually happened:** unknown from here — same open question every
  prior release on this board has recorded.
- **Migration:** none, either repo.
- **Feature flag:** none.
- **Duration:** n/a — no deploy run by this department.

## Verification

Recorded commits (`d37e0c9`, `92bcacd`, `486eec0`, `8b90f0e`) confirmed
present on `origin/main` by exact SHA on both repos, via the consolidating
merge commits above — not re-diffed against a live branch tip, since both
original stacked branches remain in their pre-consolidation shape and are
no longer representative of what shipped.

## Acceptance criteria

Not re-walked line-by-line this hop — both tickets' own security-gate
mutation tests and QA acceptance runs already confirmed every AC on the
exact commits now on `origin/main` (same SHAs, unmodified since); re-citing
the receipts here rather than re-deriving them, per this board's own
"don't re-derive a finished investigation" convention.

## Rollback

- **Path:** revert each repo's own consolidating merge commit (`5415ef0` /
  `f5de339`) — no migration, no stored-state change on either repo, fully
  undoes both tickets' diffs together (they cannot be reverted
  independently, since `ENG-010`'s commits sit on top of `ENG-009`'s in the
  same stack).
- **Tested:** not drilled — see `rollback_tested` above.
- **Used:** no.

## Health note

Same boundary every prior `aiorders-api`/`aiorders-admin-hub` release on
this board has hit: no dashboard/monitoring access to either deploy target
from this department's worktree, so whether either deploy is live and
healthy is unknown from here.

## Observability

Unchanged from each ticket's own security-gate findings — no new logging
mechanism needed or added by either ticket.

## Cost

$0/month delta — no new dependency, no new vendor, confirmed no
`package.json`/lockfile change attributable to either ticket's diff.

## Follow-ups

None new. The stacked-branch delivery-path question both tickets' own logs
flagged as open is now closed by this release; no residual gap.

## Update, 2026-09-04T16:xx (post-release addendum — corrects the record above, does not replace it)

**"No migration on either ticket" (Gates section, and the original
`rollback_tested` reasoning above) was wrong.** The consolidating merge
(`5415ef0`) does carry two migrations, confirmed by direct inspection:
`supabase/migrations/20260830100000_add_influencer_social_stats.sql`
(ENG-009 — two nullable columns, `social_stats_updated_at`/
`social_stats_platform`, on `influencers`) and
`supabase/migrations/20260902120000_create_influencer_notes.sql` (ENG-010 —
new `influencer_notes` table, RLS enabled, one FK-backed policy). Both were
present in the original PR diffs all along; this board's own prior passes
missed them (checked `*.diff` files, apparently not the migrations
directory) rather than them being newly introduced.

**Deploy, actually performed** — outside this department's own pipeline.
`aiorders-api` is registered L1 (a human deploys); the approver directed
this session's own Claude Code assistant to run it rather than doing it by
hand or asking the eng-loop, which would have declined per its own
autonomy limit:

1. `supabase functions deploy admin-portal --project-ref bmnmnejwdxbcqinqkwko`
   — ran first (sequencing mistake, caught immediately, not silently
   left). Live window with the new code but not yet the new schema:
   `GET`/`POST /admin-portal/influencer-notes` hard-failed (relation didn't
   exist) and any `PATCH` touching `social_stats_platform`/`followers`/
   `engagement` hard-failed (columns didn't exist). Checked against the
   handler's own code before assuming scope: every other route on this
   function, including `ENG-009`'s pre-existing PATCH fields, was
   unaffected — reads use `select('*')` (degrades to live schema, no
   error) and the new-column write path is reached only when a caller
   sends those specific new fields.
2. `supabase db push --project-ref bmnmnejwdxbcqinqkwko` — run by the
   approver directly, closing the gap. Reconfirmed via
   `supabase migration list`: both `20260830100000` and `20260902120000`
   now show applied on Remote, matching Local. Window between step 1 and
   this step: well under an hour, same conversation.

**`aiorders-admin-hub` deploy status: also confirmed, and also a correction
to the Deploy section above.** That section's "no CI/CD auto-deploy exists
on either repo (`.github/workflows/` absent from `origin/main` on both)"
is wrong for this repo — `.github/workflows/deploy-cf.yml` has existed
since 2026-08-30 (`698b7c1`), triggers on every push to `main`, and ran
successfully for this exact merge: `gh run list` shows "Deploy to
Cloudflare Pages" completed `success` at `2026-09-04T15:40:34Z`, 3 seconds
after PR #9 merged. (The claim was accurate for `aiorders-api`, which has
no workflow — only `aiorders-admin-hub` auto-deploys.)

**Net result: both repos are now fully live** — `aiorders-api`'s edge
function and schema, and `aiorders-admin-hub`'s frontend, all confirmed
deployed with no known gap remaining.

No reply needed — recorded for the release's own accuracy, not a new gate.
