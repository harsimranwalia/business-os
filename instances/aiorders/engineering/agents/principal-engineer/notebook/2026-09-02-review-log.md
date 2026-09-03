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

## ENG-010 — Influencer relationship notes (aiorders-api, aiorders-admin-hub)

**Round 1: FAIL — a stale-response race can display one influencer's notes
under a different influencer's open dialog.**

- **Where:** `aiorders-admin-hub`, `src/pages/Influencers.tsx`. `fetchNotes`
  (line 147) and `handleAddNote` (line 167), each newly added by this
  ticket.
- **What's wrong:** neither callback checks that its async response is
  still for the influencer currently open before applying it
  (`setNotes(payload.data)` line 159; `setNotes(prev => [payload.data,
  ...prev])` line 189). Every influencer row renders its own uncontrolled
  `<Dialog>`, all sharing one page component's state that never unmounts
  between selections — so opening influencer A, closing, then opening B
  while A's `GET`/`POST` is still in flight lets A's response land after
  B's dialog is already open and overwrite it with A's notes, mislabeled as
  B's. No exotic timing needed, ordinary click-through speed is enough.
- **Why it matters:** not the influencer-visibility risk this ticket's own
  PRD names as the one thing it can't get wrong (server-side the note is
  always written against the right `influencer_id`), and not a P0 — but the
  feature exists so staff act on the notes they're looking at, and this can
  silently show the wrong influencer's notes with no error. No test could
  have caught it: this project's frontend has no test harness at all
  (standing gap, `proposals.md` 2026-08-31).
- **The fix:** compare the id the response is *for* against
  `selectedInfluencer?.id` before applying it, in both callbacks. Small,
  mechanical, no new infrastructure.
- **Automatic-failure scan:** 0/10. Worth noting for the running `any`-typing
  watch (2026-08-31 entry above): `resolveAuthorNames(adminSupabase: any,
  ...)` is a **new function**, not a duplicated `AuthenticatedRequest`
  interface, and its `any` is the extraction of an already-`any`-typed value
  — same reasoning already applied to `ENG-013`'s `hasFoodswipeAccess`, not
  a fresh untyped surface and not a third occurrence of the interface-
  duplication pattern that section is tracking (this ticket imports
  `AuthenticatedRequest` from `influencers.ts` rather than copying it — the
  cleanest of the four tickets on this board that have touched this type).
- **Verified independently, not trusted from the ticket log:** `deno
  check`/`deno test` re-run in the worktree — `influencer-notes.test.ts`
  16/16, `influencers.test.ts` (sibling) 34/34, matching the build pass's
  own claim exactly. `npm run lint`/`build` (`aiorders-admin-hub`) at the
  established baseline, `Influencers.tsx` carrying its one pre-existing
  warning, zero new. Two of the diff's own comments spot-checked rather
  than trusted: the router substring-non-overlap claim, and the
  `influencer-invitations.ts` fetch-separately-map-by-id precedent citation
  — both confirmed accurate.
- **Verdict:** fail, round 1. No receipt written
  (`agents/principal-engineer/reviews/ENG-010.md` stays absent). Routed to
  `building`, same ticket, no owner change. QA's hop not run this round —
  discarded per the combined-hop design, same as `ENG-009`'s own round 1.

**Round 2: FAIL — the new `influencer_notes` table has no row-level security,
so the one risk this ticket cannot get wrong is still open through a second,
unmediated path the edge-function check never touches.**

- **Where:** `aiorders-api`,
  `supabase/migrations/20260902120000_create_influencer_notes.sql`. Round 1's
  finding is confirmed fixed (see below) — this is a new finding, not a
  reopening.
- **What's wrong:** the migration creates `influencer_notes` with no
  `ENABLE ROW LEVEL SECURITY` and no policy. `admin-portal/handlers/
  influencer-notes.ts` only ever reads/writes it through `auth.adminSupabase`,
  which `admin-portal/index.ts:51-58` constructs with
  `SUPABASE_SERVICE_ROLE_KEY` — a role that bypasses RLS by definition — so
  the handler's own `hasInfluencerAdminAccess` check (and the router's
  `authenticate()` allowlist beneath it) are the *only* gate on this data.
  Neither gate lives in the database, and both are specific to one call path
  into it. Supabase exposes every `public`-schema table over PostgREST by
  default; `src/pages/Influencers.tsx:102` (this exact file, unchanged by
  this ticket) already calls `supabase.from('influencers').select('*')`
  directly from the browser using the project's anon key — live proof this
  access path is real for the sibling table today, not a theoretical one this
  review is inventing. Nothing distinguishes `influencer_notes` from
  `influencers` at the database layer: no RLS on either blocks a request
  built the same way, bearer token swapped for an influencer's own valid
  session JWT instead of a staff member's.
- **Why it matters:** this is precisely the failure this ticket's own PRD
  names as the one thing it cannot get wrong — an influencer reading staff
  commentary about themselves — reachable without going anywhere near the
  edge function this review already checked carefully. The new
  negative-authorization test (`rejects the influencer's own role with 403 --
  the one case this ticket can't get wrong`) calls `handleInfluencerNotes`
  directly; it proves the *handler* rejects that role, and says nothing about
  whether the *table* does, because a request that never reaches the handler
  was never in scope for that test. Round 1 and the database migration gate
  both passed this same file without asking the question — the migration
  doc's own verdict reads "no change to ... RLS policy," which is true only
  in the sense that a table which never had one still doesn't; the table is
  new, so "unchanged" reads as reassurance it isn't.
- **The fix:** this codebase already has the exact template, unused here.
  `supabase/migrations/20250926000000_proxy_sessions_audit_logs.sql` (an
  existing admin-only table, same shape: FKs into `profiles`/`auth.users`,
  read/written only via the service-role client) pairs
  `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` with a policy scoped to
  `profiles.role IN ('admin', 'sub-admin')` — the identical boundary this
  ticket's own handler already enforces in code. Add both lines to this
  migration before it merges:
  ```sql
  alter table influencer_notes enable row level security;

  create policy "Admins can manage influencer notes"
  on influencer_notes
  for all
  using (exists (
    select 1 from public.profiles
    where id = auth.uid() and role in ('admin', 'sub-admin')
  ))
  with check (exists (
    select 1 from public.profiles
    where id = auth.uid() and role in ('admin', 'sub-admin')
  ));
  ```
  Changes nothing about how the feature works — the handler's own client
  bypasses RLS regardless — it only closes the direct path. First occurrence
  of this specific shape (new sensitive table, no RLS) on this board; not
  promoted to `engineering-standards.md` off one instance, but worth watching
  for a second.
- **Round 1's own fix, re-verified, not re-trusted:** read
  `selectedInfluencerIdRef`'s full lifecycle in the current diff —
  set synchronously in `openInfluencer` before `setSelectedInfluencer`,
  compared in both `fetchNotes`'s and `handleAddNote`'s success branches
  before applying a response. Correct and complete for the race round 1
  named; this round's finding is unrelated to it.
- **Verified independently:** `deno check` clean on both new files;
  `deno test influencer-notes.test.ts` 16/16, `influencers.test.ts` (sibling)
  34/34, whole-tree `deno check handlers/*.ts` 17 pre-existing errors
  (`auth.ts`/`partners.ts`/`users.ts`), zero in either file this ticket
  touches — all matching the build hop's and round 1's own numbers exactly.
  `npm run lint` 150/31 baseline unchanged, `Influencers.tsx` one
  pre-existing warning, zero new. `npm run build` clean. Confirmed
  `hasInfluencerAdminAccess`'s actual body (`influencers.ts:27-33`) matches
  what this ticket's log claims (`role` or `additional_roles`, `admin`/
  `sub-admin` only). Confirmed `adminSupabase`'s construction
  (service-role key) directly rather than assuming it from the naming
  convention.
- **Verdict:** fail, round 2. No receipt written
  (`agents/principal-engineer/reviews/ENG-010.md` stays absent). Routed to
  `building`, same ticket, no owner change. QA's hop not run this round —
  discarded per the combined-hop design, same as round 1.

**Round 3: PASS — building → in-review → in-qa.**

- **Both fixes re-verified, not re-trusted:** round 1's
  `selectedInfluencerIdRef` guard traced through its full lifecycle, correct
  and complete. Round 2's RLS policy compared character-by-character
  against `proxy_sessions_audit_logs`, then checked one level deeper than
  either prior round: `20250729143357_initial_restaurant_rls.sql` (this
  project's foundational RLS migration) already gates `restaurants` and
  `catering` with the identical `EXISTS`-against-`profiles` shape — this is
  the codebase's established house pattern, not a precedent copied a
  second time on faith.
- **Automatic-failure scan:** 0/10, re-run fresh against the full
  cumulative diff (all three commits, not just the delta since round 2).
- **Fresh scan for new issues** (not carried forward from either prior
  round) found one pre-existing, codebase-wide, non-blocking gap — the new
  RLS policy checks `profiles.role` only, not `additional_roles`, same as
  every other admin-gated RLS policy in this repo (grepped
  `additional_roles` across every migration: zero hits anywhere) — and two
  minor UX gaps in the same already-accepted class round 1 named
  (`fetchNotes`'s `!response.ok` silently degrades one step further than
  its own catch block; `handleAddNote`'s error toast isn't scoped to the
  influencer that actually failed). Also checked and ruled out as
  pre-existing, not this ticket's own: the `error.message`-in-500-body
  pattern in both new handlers (matches a dozen+ existing files, already a
  tracked three-strike proposal — see
  `2026-09-02-security-proposal-verbose-error-response.md` — named for
  security's own count, not re-filed); `req.json()` inside the outer `try`
  (matches every body-parsing handler in this directory); `deno check`
  failing on `index.ts` directly (confirmed via a disposable worktree at
  the pre-`ENG-010` base commit that this predates this ticket's own
  8-line addition).
- **Verified independently:** `deno check` clean on both new files; `deno
  test influencer-notes.test.ts` 16/16; `deno test influencers.test.ts`
  (sibling) 34/34; whole-tree `deno check handlers/*.ts` 17 pre-existing
  errors, zero new; `npm run lint` 150/31 baseline unchanged,
  `Influencers.tsx` one pre-existing warning, zero new; `npm run build`
  clean. All numbers match every prior hop's own claims exactly.
- **Receipts:** `agents/principal-engineer/reviews/ENG-010.md` (verdict
  `pass`, round 3), `agents/qa/test-plans/ENG-010.md` (all 4 ACs covered).
  `links.review` / `links.test_plan` set on the ticket.
- **Verdict:** pass. State `building → in-review → in-qa`. Next hop:
  security (fresh session, needs this round's own test plan).

## ENG-008 — Influencer board admin management (aiorders-api, aiorders-admin-hub)

**Round 3: PASS, plus the quality gate — now in-qa.**

- **What changed:** the approver's merge-request reply rejected the new
  `accepts_barter` column as redundant with the pre-existing `barter_visit`.
  Fix hop dropped it from the migration/handler/test/frontend, renaming every
  reference to `barter_visit` instead (`aiorders-api@7c6e4b8`,
  `aiorders-admin-hub@141f2eb`).
- **Automatic-failure scan:** 0/10, re-run against the full cumulative diff.
  Grepped `accepts_barter` across both repos' full tracked trees: zero
  remaining code references.
- **Verified independently:** `deno test` executed for real (19/19, 12ms) —
  this host has `deno` on `PATH`. **Mutation-tested the renamed validation**:
  reverted the `barter_visit` type guard by hand, re-ran — exactly
  `rejects a non-boolean barter_visit` went red (18/19), nothing else.
  `npm run lint`/`build` (`aiorders-admin-hub`) reproduced at the established
  150/31 baseline, `Influencers.tsx` one pre-existing warning, zero new.
- **New finding #1 (non-blocking, this role doesn't own the fix):** the
  architect's design doc
  (`agents/architect/designs/ENG-008-influencer-profile-admin-management.md`,
  lines 99–101/128–131) still specifies `accepts_barter` as a real column and
  valid PATCH field — stale since the approver's correction. Flagged rather
  than edited; `agents/architect/designs/` is the architect's owned artifact.
- **New finding #2 (non-blocking to this ticket, more consequential):
  `ENG-009`'s branch is stale against this fix.** `git merge-base
  --is-ancestor 7c6e4b8/141f2eb {ENG-009-tip}` returns false on both repos.
  **Not a new failure shape** — this is the *second* occurrence today of the
  exact gap `ENG-009`'s own round-1 review found a few hours earlier in this
  same notebook (above): `ENG-009` was rebased onto `ENG-008`'s round-2 tip
  specifically to fix that first occurrence, passed round 2, and then
  `ENG-008` moved again (this round's fix) after the rebase — so the same
  ticket pair drifted stale a second time in one day. The proposal already
  filed off the first occurrence (`proposals.md`, 2026-09-02,
  `principal-engineer`: check a ticket's branch against the sibling it
  forked from, not just `main`) would have caught this one too — this is
  reinforcing evidence, not a reason for a second proposal. `ENG-009` is
  `blocked`/`blocked_on: approver` with an open, unanswered merge request
  right now, and `origin/main` on both repos is still clean of
  `accepts_barter` — a live, catchable window. Cross-referenced into
  `ENG-009`'s own ticket log; not fixed here (rebasing a different ticket
  that's already at its own human gate is outside this event's contract).
- **Receipts:** `agents/principal-engineer/reviews/ENG-008.md` (verdict
  `pass`, round 3), `agents/qa/test-plans/ENG-008.md`. `links.review` /
  `links.test_plan` already pointed at these paths from round 2; content
  overwritten to describe this round's diff, per this file's own established
  convention (see either receipt's own "Prior pass (superseded)" section).
- **Verdict:** pass. State `building → in-review → in-qa`. Next hop:
  security (fresh session, needs this round's own test plan).

**Pattern note, now that the sibling-staleness gap has recurred within one
day on the same two tickets:** worth watching whether a third occurrence
happens before the existing proposal is ever acted on — this board's own
practice (`eng_build_loop.md` step 8b) is to stop granting case-by-case
fixes and force a process change at the third occurrence of the same kind.
Two so far, same day, same ticket pair.
