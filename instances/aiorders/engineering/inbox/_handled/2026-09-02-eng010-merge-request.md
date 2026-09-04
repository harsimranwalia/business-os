---
type: eng-decision
agent: eng-manager
gate: merge
project: aiorders-admin-hub
ticket: ENG-010
recommendation: merge — migration, code review (round 3), quality, and security all passed; additive-only change (one new isolated table with RLS, two new admin-gated routes reusing the existing auth check, one new UI section, no schema removal, no new dependency). Both PRs are stacked on ENG-009's still-open branch, not main — see Sequencing below before merging.
pr_urls:
  - repo: aiorders-api
    url: https://github.com/harsimranwalia/aiorders-api/pull/8
  - repo: aiorders-admin-hub
    url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/7
raised: 2026-09-02
notified: 2026-09-02T17:45:02
nudged: 2026-09-03T17:46:05
decision:
---

# Merge request — Influencer relationship notes (ENG-010)

Fifth two-repo ticket on this board (after `ENG-011`, `ENG-013`, `ENG-008`,
`ENG-009`) — one ticket, two PRs, both opened this pass.

## What this does

Any staff member viewing an influencer's admin record can now read every
note previously left about that influencer (who wrote it and when) and add
a new one — this ticket's own PRD's stated Outcome. Nothing else on the
influencer record changes; nothing an influencer can see about themselves
changes.

- `aiorders-api`: new, isolated `influencer_notes` table (FKs into
  `influencers`/`profiles`, no edit/delete path, RLS scoped to
  admin/sub-admin); new `GET admin-portal/influencer-notes?influencer_id={id}`
  (list, newest first, resolved author name) and
  `POST admin-portal/influencer-notes` (create; `author_id` always from the
  session), both gated via the same `hasInfluencerAdminAccess` check
  `ENG-008`/`ENG-009` established.
- `aiorders-admin-hub`: a Notes block added to the existing influencer
  detail dialog — chronological list (author + timestamp) plus an add-note
  form, fetched per-influencer on dialog open.

## Sequencing — read before merging

Same shape as `ENG-009`'s own merge request. Both PRs are based on
`feat/ENG-009-influencer-engagement-info`, not `main`, because this ticket
branched off that tip (all three influencer tickets touch the same
admin-UI file, `src/pages/Influencers.tsx`, and were sequenced back to back
to avoid a needless merge conflict). The diff on each PR is `ENG-010`'s own
change only — `ENG-009`'s commits are not duplicated into these PRs' review
surface.

`ENG-009`'s own merge request (`inbox/2026-09-02-eng009-merge-request.md`)
and `ENG-008`'s (`inbox/2026-08-31-eng008-merge-request.md`) are both still
open and unanswered. Two ways to sequence:
- Merge `ENG-008`'s PRs, then `ENG-009`'s, then these — each auto-retargets
  to the next once its own base merges and its branch is deleted (GitHub's
  default prompt).
- Or merge any of the three out of order — GitHub allows merging into a
  non-default base branch directly; each ticket's own PRs are unaffected
  either way.

No functional dependency forces one order — this is purely a review-surface
choice already made at build time, not a new constraint from this pass.

**Update, 2026-09-03 (`scheduled auto-drain` sweep) — read `ENG-009`'s own
merge request before acting on this one.** `ENG-009`'s `aiorders-admin-hub`
branch (this ticket's own base) is stale against `ENG-008`'s round-3 fix
and will conflict on `src/pages/Influencers.tsx` once that sequencing plays
out — full detail in `inbox/2026-09-02-eng009-merge-request.md`'s own
"Update, 2026-09-03." This ticket's own diff is unaffected directly
(confirmed fresh this pass: no `accepts_barter`/`barter_visit` lines
anywhere in `ENG-010`'s own diff on either repo, on top of `ENG-009`'s
tip) — but it inherits `ENG-009`'s branch wholesale, so once `ENG-009` is
rebased to fix its own conflict, this branch will need the same
rebase-onto-new-base treatment before it, in turn, is safe to merge toward
`main`. Merging this PR into `ENG-009`'s branch directly (not `main`) is
unaffected by any of this and can proceed independently of when `ENG-009`
gets fixed.

## Update, 2026-09-04 (`scheduled` sweep) — what actually happened when these merged

Both PRs now show `MERGED` on GitHub. **Neither shipped** — both merged into
`feat/ENG-009-influencer-engagement-info` (this ticket's own configured
base, per Sequencing above), which itself still hasn't reached `main` (see
`ENG-009`'s own merge-request item and board-file log — same date). This
ticket's own content was never in question (round 3 passed clean, no hold
recommendation), only the delivery path, which it inherits from `ENG-009`.
No reply needed here — resolving `ENG-009`'s path to `main` resolves this
ticket's too. Full mechanics: this ticket's own board-file log, 2026-09-04
entry.

## Gates passed

- Migration: **pass** — `agents/database/migrations/ENG-010-influencer-relationship-notes.md`.
  Additive only: one new table, two `not null` FKs into already-live
  tables, one composite index, no backfill. Addendum: round-2 review found
  the table shipped with no row-level security — fixed in the same
  migration file (`ENABLE ROW LEVEL SECURITY` plus an admin/sub-admin
  policy matching the existing `proxy_sessions` precedent).
- Code review: **pass, round 3** — `agents/principal-engineer/reviews/ENG-010.md`.
  Round 1 failed on a stale-response race in the frontend notes UI (closing
  one influencer's dialog and opening another while a request was in
  flight could misattribute notes between them) — fixed with a ref-based
  guard. Round 2 failed on the missing-RLS gap above — fixed. Round 3: both
  fixes re-verified independently, 0/10 automatic failures, all 4
  acceptance criteria covered.
- Quality: **pass** — `agents/qa/test-plans/ENG-010.md`. All 4 acceptance
  criteria covered. `deno test` actually executed: 16 passed, 0 failed
  (new), 34 passed, 0 failed (sibling `influencers.test.ts`, unaffected).
- Security: **pass** — `agents/security/reviews/ENG-010.md`. OWASP A01–A10
  walked, 0 blocking. Every route sits behind two independent authorization
  layers (router allowlist, reused `hasInfluencerAdminAccess`) plus, as of
  the RLS fix, a third at the database layer — closing the one risk this
  ticket's PRD names as the thing it cannot get wrong (an influencer
  reading staff commentary about themselves). No secrets, no new
  dependency, no injection surface.

## Named gaps, carried forward rather than hidden

- **Raw `error.message` returned on a 500**, both new handlers — 4th and
  5th tracked occurrence of this finding class (after `ENG-013`, `ENG-008`,
  `ENG-009`). Not blocking. Already proposed to principal-engineer as a
  three-strike standards question:
  `agents/principal-engineer/notebook/2026-09-02-security-proposal-verbose-error-response.md`
  — not re-proposed here.
- **`Access-Control-Allow-Origin: '*'`** on both new routes — confirmed
  identical to all eleven existing handler files in this directory, not a
  decision this ticket made; lower severity given this app's bearer-token
  (not cookie) auth model.
- **RLS policy checks `profiles.role` only, not `additional_roles`** —
  matches every other admin-gated RLS policy in this codebase; not
  exploitable through this feature's own code path (the only reader is the
  service-role client, which bypasses RLS and applies the wider check).
- **No automated frontend test framework exists on `aiorders-admin-hub`**
  (standing gap, tracked as a proposal since `ENG-008`, now a third/fourth
  data point from this ticket's own two review rounds) — round 1's
  race-condition fix has no regression test as a result; verified instead
  by principal-engineer reading the full ref lifecycle against the code
  directly.
- `fetchNotes`'s `if (!response.ok) return` degrades silently to "No notes
  yet.", indistinguishable from a genuinely empty list; `handleAddNote`'s
  error toast isn't scoped to the influencer that actually failed. Both
  named, both non-blocking, same class of gap this file's existing
  `fetchActivity` already carries.
- No live Postgres reachable from the build host — the new `alter
  table`/`create policy` statements have not been executed anywhere;
  verified instead by direct, character-level comparison against two
  already-running policies of the identical shape in this same codebase
  (`proxy_sessions_audit_logs`, and the foundational RLS migration gating
  `restaurants`/`catering`).

## Update, 2026-09-04 (`watch (launchd)` event pass) — resolved, shipped

Same resolution as `ENG-009`'s own item, same action: a new PR on each
repo, `merge/ENG-009-ENG-010-to-main` (`aiorders-api` #14,
`aiorders-admin-hub` #9), base `main`, head the stacked branch's current
tip, opened and merged directly on GitHub at `2026-09-04T15:39:16Z` /
`15:40:31Z`, carrying this ticket's commits along with `ENG-009`'s (already
stacked on each other). Confirmed via `git merge-base --is-ancestor` on
this ticket's own recorded commits (`486eec0`, `8b90f0e`) against fresh
`origin/main` on both repos. All three gate receipts re-read fresh, still
`pass`; no migration owed. Ticket carried `blocked → shipped → verified`.
Full detail: `ENG-010`'s own board-file log, 2026-09-04 entry, and
`agents/devops/releases/2026-09-04-ENG-009-ENG-010-aiorders-api-and-admin-hub.md`.

No reply was ever written to this item in the tracked channel — resolved
entirely by direct action on GitHub.

## Decision

Filled in by the approver. (None given — resolved by direct GitHub action;
see the update immediately above.)
