# Review log — 2026-09-02

## ENG-009 — Influencer engagement info (aiorders-api, aiorders-admin-hub)

**Round 1: FAIL — the branch predates a sibling ticket's own bug fix and
still carries the bug.**

- **Where:** both repos, `feat/ENG-009-influencer-engagement-info`.
  `aiorders-api@4eb4b1b` branches from `dc6972a`, one commit before
  `ENG-008`'s own fix `57f8c4b`. `aiorders-admin-hub@328db29` branches from
  `f2ea36c`, one commit before `ENG-008`'s own fix `63be255`. Confirmed by
  `git merge-base --is-ancestor {fix-commit} {ENG-009-tip}` on each repo —
  both return false.
- **What's wrong:** `Influencers.tsx:139-140` still reads
  `accepts_paid: influencer.accepts_paid ?? !influencer.barter_visit` (and
  the `accepts_barter` equivalent) — the exact null-coalescing bug
  `ENG-008`'s own round-1 review found on 2026-08-30 (see that date's entry
  in this notebook) and fixed on 2026-08-31. `Influencers.tsx:194-195`
  still sends both fields unconditionally on every save, the second half of
  the same bug. On `aiorders-api`, `influencers.ts`'s
  `hasInfluencerAdminAccess` still reads unguarded `userProfile.role`
  rather than the optional-chained version `ENG-008`'s fix put there, and
  the missing-profile/allowlist-strip tests that fix added are absent from
  `ENG-009`'s copy of the test file — lower severity (the missing-profile
  path is provably unreachable in production, per `ENG-008`'s own
  round-2 review of the same line), not the reason this round fails.
- **Why it matters:** this isn't a new bug — it's a previously-found,
  previously-fixed one, reappearing because `ENG-009` forked from `ENG-008`
  before the fix (2026-08-30 01:39, a day before the fix landed) and was
  never rebased. Four sweep passes since have checked this board without
  catching it, because merge detection diffs a ticket's branch against
  `main`, never against a sibling it was deliberately sequenced behind.
- **The fix:** rebase (or re-cut) `ENG-009`'s branch onto `ENG-008`'s
  current tip on both repos and re-apply `ENG-009`'s own changes on top.
  Not a clean auto-merge: `ENG-008`'s fix and `ENG-009`'s own diff both
  touch the same `body` object-literal in `handleSaveInfluencer` (one
  converts `accepts_paid`/`accepts_barter` to conditional omission, the
  other adds `social_stats_platform` as a new entry in the same block) —
  needs both changes applied by hand, not a side picked. Re-verify against
  `ENG-008`'s own round-2 receipt (`agents/principal-engineer/reviews/ENG-008.md`)
  before resubmitting.
- **Verdict:** fail, round 1. No receipt written
  (`agents/principal-engineer/reviews/ENG-009.md` stays absent). Routed to
  `building`, same ticket, no owner change. QA's hop not run this round —
  discarded per the combined-hop design.

First occurrence of this specific shape (branch stale against a sibling,
not against `main`) on this board — not a repeat of the 2026-08-30
null-coalescing finding itself, which was genuinely fixed; this is that
same fix failing to travel to a branch cut before it existed. Proposal
filed (`agents/eng-manager/proposals.md`) naming the general gap: nothing
in this board's merge-detection or code-review inputs checks a ticket's
branch against a sibling it was branched from, only against `main`.
