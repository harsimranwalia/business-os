---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-009
recommendation: hold — was "merge" when raised; a fact discovered since changes that. All four gates below still pass on the diff they were run against, but ENG-008 has since moved a second time (round 3, ~22:48 on 2026-09-02) and this branch was never re-synced to it — see "Update, 2026-09-03" under Sequencing before merging.
pr_urls:
  - repo: aiorders-api
    url: https://github.com/harsimranwalia/aiorders-api/pull/7
  - repo: aiorders-admin-hub
    url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/6
raised: 2026-09-02
notified: 2026-09-02T10:51:07
nudged: 2026-09-03T11:34:08
decision:
---

# Merge request — Influencer engagement info (ENG-009)

Fourth two-repo ticket on this board (after `ENG-011`, `ENG-013`, `ENG-008`)
— one ticket, two PRs, both opened this pass.

## What this does

Staff can now see an internally-derived signal of how active an influencer
is on AIOrders, and can manually enter/update a social-media engagement
figure — both were the standing answer to the question raised while shaping
`ENG-008` ("both reading A and reading B", the approver's own words).

- `aiorders-api`: two new nullable columns on `influencers`
  (`social_stats_updated_at`, `social_stats_platform`); a write path on the
  existing, previously-unwritten `followers`/`engagement` columns via
  `PATCH admin-portal/influencers/{id}` (extends `ENG-008`'s handler); new
  `GET admin-portal/influencers/activity` (admin/sub-admin gated,
  service-role client) returns a per-influencer activity aggregate derived
  from invitation history — no external API call, no stored derived data.
- `aiorders-admin-hub`: edit form gains followers/engagement/platform
  inputs; table gains an Activity column, dialog gains an Activity block;
  Followers/Engagement now show "Not set" instead of a fabricated `0`/`0.0%`
  before staff enter a value.

**Not the Meta API integration** — the approver's own words defer that
("later we can connect"); this ticket ships the staff-manual version only.

## Sequencing — read before merging

**Both PRs are based on `feat/ENG-008-influencer-admin-management`, not
`main`**, because this ticket extends the exact handler file and edit form
`ENG-008` adds, and its round-1 code review failed specifically because this
branch had forked *before* `ENG-008`'s own bug fix landed (see Gates
passed). The diff on each PR is ENG-009's own change only — `ENG-008`'s
commits are not duplicated into these PRs' review surface.

`ENG-008`'s own merge request (`inbox/2026-08-31-eng008-merge-request.md`)
is still open and unanswered. Two ways to sequence:
- Merge `ENG-008`'s two PRs first. If you delete its branch on merge (GitHub's
  default prompt), GitHub auto-retargets these PRs to `main`, and they
  merge cleanly from there.
- Or merge these first — GitHub allows merging into a non-default base
  branch directly; `ENG-008`'s own PRs are unaffected either way. Its
  branch keeps carrying these commits until `ENG-008` itself merges.

No functional dependency forces one order — this is purely a review-surface
choice already made at build time, not a new constraint from this pass.

**Update, 2026-09-03 (`scheduled auto-drain` sweep) — the "merge cleanly"
claim above is no longer true.** `ENG-008`'s own round-3 code review
(2026-09-02 ~22:48, after this item was raised at 10:51) fixed a duplicate
column the approver's own merge-request reply objected to: dropped
`accepts_barter`, reusing the existing `barter_visit` boolean instead
(`aiorders-api@7c6e4b8`, `aiorders-admin-hub@141f2eb`). This branch was
never re-synced to that fix — confirmed fresh this pass,
`git merge-base --is-ancestor 7c6e4b8/141f2eb` against this branch's tip
(`d37e0c9`/`92bcacd`) returns **false** on both repos (`ENG-009`'s own
board log already recorded this as an informational cross-reference,
2026-09-02, found by that same `ENG-008` round-3 review — this update
propagates it to the gate item itself, which hadn't been touched).

Checked what that actually means for each repo, not just the ancestry
fact: **`aiorders-api` is unaffected** — this branch's own diff never
references `accepts_barter` (grepped directly). **`aiorders-admin-hub`
will conflict** — `src/pages/Influencers.tsx` on this branch still carries
the complete pre-round-3 `accepts_barter` UI (interface fields, edit-form
state, the checkbox, the table badge — 11 lines, untouched by this
ticket's own diff, just inherited from the stale base) that `ENG-008`'s
fix deleted/renamed to `barter_visit`. Merging `ENG-008` first will
**not** let this PR "merge cleanly" the way the paragraph above describes
— GitHub will show a real conflict on that file, not a silent problem,
but the resolution isn't a mechanical pick-a-side: `accepts_barter` needs
to become `barter_visit` throughout this ticket's own additions too,
same rename `ENG-008` already applied everywhere else.

**Recommendation:** hold this request; have the department rebase this
branch (`aiorders-admin-hub` only) onto `ENG-008`'s current tip and re-run
review/quality/security on the delta before treating this as safe to
merge — the same repair its own round-1→round-2 rebase already did once
today for an earlier ENG-008 fix. If you'd rather resolve the GitHub
conflict by hand instead of waiting, do the same rename in ENG-009's
added lines, not just accept whichever side the merge UI defaults to.

## Update, 2026-09-04 (`scheduled` sweep) — what actually happened when these merged

Both PRs now show `MERGED` on GitHub. **Neither shipped** — both merged into
`feat/ENG-008-influencer-admin-management` (this ticket's own configured
base, per Sequencing above), not `main`. `ENG-008`'s own separate PR (base
`main`) had already merged to `main` minutes earlier; merging into a
feature branch after that doesn't retroactively reach `main` on its own.
Confirmed by content, not just ancestry: this ticket's own distinguishing
code exists only on the stacked branch, not on either repo's `main`.

**The specific risk this section warned about did not materialize** — the
merged branch carries zero `accepts_barter` references and the correct
`ENG-008` round-3 rename throughout, confirmed by direct inspection. Taking
the "resolve by hand" path this section offered appears to be exactly what
happened, and it came out clean.

**Still open: how this actually reaches `main`.** There's no longer an open
PR anywhere targeting `main` that carries this ticket's changes —
`ENG-008`'s own main-bound PR already closed. This needs a real decision
(fresh PR from the current stacked tip, or extracting this ticket's commits
onto a clean branch off current `main`) by whoever next builds on this
ticket — not a re-click. No reply needed here; full mechanics on this
ticket's own board-file log, 2026-09-04 entry.

## Gates passed

- Migration: **pass** — `agents/database/migrations/ENG-009-influencer-engagement-info.md`. Two nullable columns, no default, no backfill.
- Code review: **pass, round 2** — `agents/principal-engineer/reviews/ENG-009.md`. Round 1 failed: this branch forked before `ENG-008`'s own fix landed on both repos and still shipped an already-fixed bug (a defensive auth gap on `aiorders-api`; a real null-coalescing bug on `aiorders-admin-hub` that fabricated `accepts_paid`/`accepts_barter` on an unset preference). Closed by rebasing onto `ENG-008`'s current tip — one real test-file conflict resolved by hand on `aiorders-api`, zero-conflict clean auto-merge on `aiorders-admin-hub`, both independently re-verified by reading the merged result in full.
- Quality: **pass** — `agents/qa/test-plans/ENG-009.md`. All 4 acceptance criteria covered. `deno test` actually executed for the first time on this repo: 34 passed, 0 failed.
- Security: **pass** — `agents/security/reviews/ENG-009.md`. OWASP A01–A10 walked; negative-auth cases (missing profile, wrong role, allowlist enforcement) independently re-verified, not taken on the review's word; no secrets, no new dependency, no PII in the new activity aggregate.

## Named gaps, carried forward rather than hidden

- **Raw `error.message` returned on a 500** in the new activity-endpoint catch block — **3rd tracked occurrence** of this finding class at the security gate (after `ENG-013`, `ENG-008`). Not blocking. Proposed to principal-engineer as a three-strike standards question rather than fixed here: `agents/principal-engineer/notebook/2026-09-02-security-proposal-verbose-error-response.md`.
- `getInfluencerActivity`'s query carries no `.limit()` — 4th occurrence of this accepted class on this board (cardinality bounded by real row counts today, architect-evaluated).
- `social_stats_updated_at` stamps on "present," not "present and changed" as the design literally worded it — a deliberate, tested simplification (avoids a read-modify-write race nothing else in this handler has).
- Setting `social_stats_platform` alone (no `followers`/`engagement`) persists but doesn't render anywhere yet. P3, has a workaround (enter a number too).
- No live Postgres reachable from the build host — verified instead via read-only Supabase MCP against the real production schema, same standing gap every prior migration on this board carries.

## Update, 2026-09-04 (`watch (launchd)` event pass) — resolved, shipped

The "still open: how this actually reaches `main`" question immediately
above is now closed. A new PR on each repo, `merge/ENG-009-ENG-010-to-main`
(`aiorders-api` #14, `aiorders-admin-hub` #9), base `main`, head the
stacked branch's current tip, was opened and merged directly on GitHub at
`2026-09-04T15:39:16Z` / `15:40:31Z` — the "fresh PR from the current
stacked-branch tip" option named above, taken by hand. Both this ticket's
and `ENG-010`'s commits landed together (they were already stacked on each
other). Confirmed via `git merge-base --is-ancestor` on this ticket's own
recorded commits (`d37e0c9`, `92bcacd`) against fresh `origin/main` on both
repos, and cross-checked with `gh pr view` on both new PRs. All three gate
receipts re-read fresh, still `pass`; no migration owed. Ticket carried
`blocked → shipped → verified`. Full detail: `ENG-009`'s own board-file
log, 2026-09-04 entry, and
`agents/devops/releases/2026-09-04-ENG-009-ENG-010-aiorders-api-and-admin-hub.md`.

No reply was ever written to this item in the tracked channel — resolved
entirely by direct action on GitHub, same as every other silent-merge
ticket on this board.

## Decision

Filled in by the approver. (None given — resolved by direct GitHub action;
see the update immediately above.)
