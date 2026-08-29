---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-005
recommendation: merge — code review, quality, and security all passed; additive UI only, no schema change, no new dependency
pr_url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/2
raised: 2026-08-27
notified: 2026-08-27T16:03:58
decision: approved
decided: 2026-08-28T00:13:09.817494+00:00
---

# Merge request — Wire A4PosterGenerator into RestaurantDetails

## What this does

`aiorders-admin-hub` gets one new card on `RestaurantDetails.tsx`
(`/restaurants/:id/details`) rendering the previously-orphaned
`A4PosterGenerator` component — reachable through the same navigation that
already reaches this page, no new nav entry. No schema change, no new
dependency (`jspdf` already in `package.json`), no new endpoint (reuses the
already-deployed `url-shortener` edge function as-is).

## Gates passed

- Code review: **pass** — `agents/principal-engineer/reviews/ENG-005.md`
- Quality: **pass** — `agents/qa/test-plans/ENG-005.md`
- Security: **pass** — `agents/security/reviews/ENG-005.md` (the component's
  edge-function calls stay behind existing Bearer + admin-role gating; no new
  capability granted)

## PR

https://github.com/harsimranwalia/aiorders-admin-hub/pull/2

`aiorders-admin-hub` is registered **L1** — this department opens the PR, a
human merges. Merge whenever suits you on GitHub directly; the next
build-loop pass detects the merge itself (local git ancestry check, no action
needed from you beyond the merge) and advances the ticket to `shipped`.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-28T00:13:09.817494+00:00

merged

---

**Processed 2026-08-28 (`decision` event pass).** The "merged" answer was not
taken on its text alone — independently re-derived via the loop's own
merge-detection check (`schedules/eng_build_loop.md` step 5): `git fetch` in
the department's own worktree, then `git merge-base --is-ancestor
chore/ENG-005-a4-poster-generator-wire-in origin/main` confirmed MERGED,
`edf6947` (PR #2's own merge commit) directly on top of `51cdb29` with no
intervening commits. Ticket advanced `blocked → shipped → verified` in this
pass — see `agents/eng-manager/board/ENG-005-a4-poster-generator-decision.md`
for the full record and
`agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md` for the
release record (production deploy status not confirmed either way — outside
this department's visibility on an L1 project; see that record's Deploy and
Health notes). Journaled in `agents/eng-manager/config/decision-journal.md`.
