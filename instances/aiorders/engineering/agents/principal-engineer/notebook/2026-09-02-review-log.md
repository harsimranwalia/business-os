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

**Round 2: PASS, plus the quality gate — now in-qa.**

- **What changed:** the rebase-and-refix hop carried `ENG-008`'s fix
  commits onto this branch on both repos (`aiorders-api@d37e0c9`,
  `aiorders-admin-hub@92bcacd`); `git merge-base --is-ancestor` on both
  fix commits now returns true, reversing round 1's finding. One real
  test-file conflict on `aiorders-api` (two independent blocks appended
  after the same last test) hand-resolved; the flagged `aiorders-admin-hub`
  hunk auto-merged with zero conflicts. Both re-verified by reading the
  reconstructed result in full, not by trusting the merge's exit status —
  see the receipt for what was checked.
- **Automatic-failure scan:** 0/10 open, re-run fresh against the
  post-rebase diff (not carried forward from round 1). One accepted
  precedent (unbounded `influencer_invitations` query, 4th occurrence of
  this exact class on this board).
- **Verification:** `deno test` actually **executed** this round — `deno`
  2.9.6 installed on this host during the rebase hop — 34 passed, 0
  failed. First ticket on this board where `aiorders-api`'s suite runs
  rather than being hand-traced.
- **Quality gate (QA):** test plan written,
  `agents/qa/test-plans/ENG-009.md` — all 4 acceptance criteria covered
  (executed or inspected); no open P0/P1 bug.
- **Receipts:** `agents/principal-engineer/reviews/ENG-009.md` (verdict
  `pass`, round 2), `agents/qa/test-plans/ENG-009.md`. `links.review` /
  `links.test_plan` set on the ticket.
- **Verdict:** pass. State `building → in-review → in-qa`. Next hop:
  security (fresh session, per `eng_build_loop.md`'s sequencing — needs
  this round's own test plan).
