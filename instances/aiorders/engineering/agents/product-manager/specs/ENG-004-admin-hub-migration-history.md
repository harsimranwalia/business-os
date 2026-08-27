---
ticket: ENG-004
project: aiorders-admin-hub
status: approved
size: L
author: product-manager
created: 2026-08-25
decided: 2026-08-26
---

# Reconcile aiorders-admin-hub's deleted-but-uncommitted migration history

## Readback

**You said:** "Six aiorders-admin-hub migrations are deleted from the working
tree and exist nowhere else... The deletion was not committed... Establish
what the real migration history is and make the repo match it. The
underlying question the department should answer first: is
`aiorders-admin-hub/supabase/migrations` still authoritative at all, or did
migrations move to `aiorders-api`... Nothing here is urgent. The deployed
database is unaffected either way; this is about whether the tracked history
can rebuild it." (`inbox/requests/2026-08-23-admin-hub-migration-history.md`,
filed by Harry, 2026-08-23)

**Understood as:** Before committing anything, find out — from the live
Supabase project itself, not from either repo's tracked files — what the
real migration history actually is: which repo (if either, cleanly) is the
source of truth for this database's schema today. Then make the tracked
history in that repo replay safely from empty to the live schema, without
silently dropping the five RLS/`search_path`-hardening migrations or leaving
the `restaurant_activations` chain broken (a later, already-committed
migration alters a table only one of the six deleted files creates).

Two independent readings were run on the raw request — this PM's and, blind
to it, the architect's (an independent subagent, given only the raw request,
the business profile, and the two relevant registry rows — no PM
interpretation). They agreed on the core ask and, notably, both
independently flagged the same gap without prompting each other: **neither
reading could confirm from anything in the department's configuration that
`aiorders-admin-hub` and `aiorders-api` even target the same Supabase
project** — `config/projects.md` names a project ref for `aiorders-api`
(`bmnmnejwdxbcqinqkwko`) but none for `admin-hub`. The architect's reading
went further and named the actual mechanism this investigation needs: the
live `supabase_migrations.schema_migrations` ledger inside the Postgres
instance itself, plus each repo's own `supabase/config.toml` linkage — not a
filename or content diff between the two repos' folders, which is what the
original sweep used and which cannot, on its own, settle "authoritative."
No material divergence on scope or problem — that sharper framing is simply
what this PRD uses.

**Requirements, tagged by where they came from:**
1. `[stated]` Establish the real migration history before committing the
   pending deletion — using the live Supabase project as ground truth, not
   either repo's tracked files.
2. `[stated]` Answer whether `aiorders-admin-hub/supabase/migrations` is
   still authoritative, or migrations moved to `aiorders-api` the way edge
   functions did (and only half-moved).
3. `[stated]` Make the repo (whichever is authoritative) match the real
   history, without breaking a from-scratch replay and without silently
   dropping the RLS/`search_path` hardening.
4. `[inferred]` "Match the real history" requires first confirming, via the
   live database's own migration ledger and each repo's Supabase project
   linkage, which Supabase project each repo actually targets — not
   assumable from either tree's contents.
5. `[proposed]` The investigation itself (confirming ground truth) is
   separable from, and must complete before, any remediation (restoring
   files, moving them, or documenting the split) — attempting both at once
   risks committing a fix to the wrong understanding of the problem, which is
   exactly the mistake the original request is warning against.

**Assumed, and worth correcting if wrong:**
- "Nothing here is urgent... the deployed database is unaffected either way"
  is your own assessment, stated plainly rather than independently verified
  against the live ledger — this PRD treats it as the working assumption for
  sequencing (this doesn't jump the queue), but the investigation step
  should confirm it rather than simply inherit it, since it's one of the
  things the investigation is for.
- That you want this investigated and a recommendation brought back, not
  investigated-and-executed autonomously given the security-hardening
  content and the fact that both repos are `Autonomy L1` (a human merges
  either way). If you want it executed as far as the department's autonomy
  allows once the facts are in, say so; this PRD doesn't assume that.
- That the six files, if restored, would be restored as historical record
  (to make the chain replay) rather than necessarily re-applied as-is
  against today's live schema without review — five of six are
  security-relevant, and a blind restore is only safe if nothing since their
  deletion re-implemented equivalent policy differently.

## Problem

Six migration files were deleted from `aiorders-admin-hub`'s working tree
(uncommitted, deliberately held back by Harry pending this decision) while
still present in `HEAD` — five RLS/`search_path` security-hardening
migrations plus the one that creates `restaurant_activations`, a table an
already-committed later migration (`20260408000001_google_review_history.sql`)
alters. Committing the deletion as-is would break a from-scratch replay of
this repo's migration chain and would drop tracked security hardening from
the history. A filename sweep across all nine `projects/aiorders/` repos
found none of the six anywhere else, but — per the architect's reading — a
filename sweep can't rule out a renamed-and-edited consolidation, and
neither repo's Supabase project linkage has been confirmed, so it's not yet
established which repo's migration history is the one that matters for this
database.

## Why now

Explicitly not urgent per the request — the deployed database isn't at risk
either way. What does compound by waiting is ambiguity: every migration
either repo adds while this is unresolved (four were added to `admin-hub` on
2026-08-23 alone) makes the eventual reconciliation larger and the "which
repo is authoritative" question more entangled.

## Users

Not user-facing directly. This protects the integrity of the tracked schema
history for `restaurants` and `profiles` — tables holding real AIOrders
operator and customer data — against a disaster-recovery scenario where a
from-scratch replay would matter.

## Proposed change

Investigate first, using the live Supabase project (`bmnmnejwdxbcqinqkwko`,
confirmed for `aiorders-api`; `admin-hub`'s linkage needs confirming) as
ground truth: check the live migration ledger and each repo's
`supabase/config.toml`, and diff the six deleted files against
`aiorders-api`'s nine by content, not just filename, to rule out a renamed
consolidation. Bring the answer back — which repo is authoritative, and what
"match the real history" concretely requires — before touching the pending
deletion. Once that's settled, make the authoritative repo's tracked
migrations replay cleanly from empty to the live schema, preserving the
RLS/`search_path` hardening.

## Acceptance criteria

1. `[stated]` Given the live Supabase project(s) `aiorders-admin-hub` and
   `aiorders-api` connect to, when their linkage is checked (not assumed),
   then it's confirmed whether both target the same project.
2. `[stated]` Given the live migration ledger for that project, when
   compared against both repos' tracked migration files, then it's
   established which repo's `supabase/migrations` (if either cleanly) is
   authoritative today.
3. `[stated]` Given the six deleted files, when content-diffed (not just
   filename-diffed) against `aiorders-api`'s nine migrations, then it's
   confirmed whether any were in fact consolidated there under a different
   name.
4. `[stated]` Given the authoritative repo's migration chain after this
   ships, when replayed from an empty database, then it completes without
   error and without omitting the RLS/`search_path` hardening the six
   original files provided.
5. `[inferred]` Given the pending uncommitted deletion in `admin-hub`'s
   working tree, when this ticket ships, then that deletion has been
   resolved deliberately (restored, formally moved, or documented) — not
   left sitting uncommitted indefinitely.

## Non-goals

- Does not assume the answer to "which repo is authoritative" going in —
  that's the investigation's job, not a premise of this ticket.
- Does not touch `aiorders-api`'s own nine migrations beyond what's needed
  to confirm or complete a consolidation, if one turns out to be real.
- Does not re-verify or change RLS policy *logic* itself beyond restoring
  what the six files specify — auditing whether that policy is still the
  right policy today is a separate question this ticket doesn't take on.
- Does not touch any of the other 64 uncommitted files sitting in
  `admin-hub`'s human checkout — explicitly out of the department's view and
  out of scope here.
- Does not commit to executing a full migration-ownership move (admin-hub →
  aiorders-api) as part of this ticket, even if the investigation finds
  that's the right direction — that's plausibly a one-way-door design
  decision for the architect to size and possibly escalate via G2, not
  something decided in this PRD.

## Risks and unknowns

- Whether `aiorders-admin-hub` is even linked to the same Supabase project
  as `aiorders-api` — unconfirmed, and the investigation's first real
  question.
- Whether the six files' effects are currently live on production at all, or
  already superseded by something else done since their deletion — a blind
  restore is only safe once this is known.
- The source request itself has an internal inconsistency worth checking at
  execution: it says "four sibling migrations from the same minute... were
  kept" but names only three timestamps. Worth confirming the real count
  rather than carrying the discrepancy forward.
- This may surface a genuine one-way door (formally moving migration
  ownership between repos) — if the architect's design reaches that
  conclusion, this ticket may need a G2 conversation with the approver
  before proceeding past design, per `config/definition-of-done.md`.

## Cost

- Build: L — live-database investigation across two repos, a content-level
  diff, and a history reconciliation that has to preserve security-relevant
  migrations. Sized L on the Size table ("cross-project"), not because any
  single step is large, but because getting it wrong has real cost (a broken
  replay, or silently dropped RLS hardening) and it touches two repos'
  relationship to each other and to a live database none of the other
  AIOrders tickets have needed to reason about yet.
- Run: $0/month — no new infrastructure; this is entirely about the tracked
  history of infrastructure that already exists and is already paid for.

## Decision

G1 raised 2026-08-25 — `ENG-002`'s G1 was answered (approved) that pass,
freeing the `wip.approver_limit` (2) slot `ENG-003` had been holding
alongside it; this ticket took the freed slot on severity grounds (`P2`, the
higher of the two remaining To-do tickets — `ENG-005` is `P3`). See
`inbox/2026-08-25-eng004-g1-scope.md`, now `inbox/_handled/`.

- **The approver's answer:** approved
- **Date:** 2026-08-26T22:57:21-07:00 (2026-08-27T05:57:21.472123+00:00)
- **Notes:** Answered by directly editing the gate item file — `decision:`/
  `decided:` set in its frontmatter and a second `## Decision` section
  appended below the original unedited placeholder — rather than through
  `lib/eng-notify.sh`'s reply channel. Second such occurrence after `ENG-001`'s
  G3 (`agents/eng-manager/config/decision-journal.md`, 2026-08-26 row); moved
  the item to `_handled/` unedited, same as that one, rather than normalizing
  it. No `## Dissent` section — `agents/critic/agent.md` still doesn't exist
  at the department or instance level (open proposal, `agents/eng-manager/proposals.md`,
  2026-08-25).
