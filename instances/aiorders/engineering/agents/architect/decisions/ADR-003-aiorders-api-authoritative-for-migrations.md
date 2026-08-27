---
id: ADR-003
title: aiorders-api is authoritative for AIOrders' Supabase migration history, not aiorders-admin-hub
project: aiorders-admin-hub
ticket: ENG-004
status: accepted
decided_by: approver
date: 2026-08-26
supersedes:
superseded_by:
---

# ADR-003: `aiorders-api` is authoritative for AIOrders' Supabase migration history, not `aiorders-admin-hub`

## Context

`ENG-004` was filed 2026-08-23 to answer, using the live Supabase project as
ground truth, whether `aiorders-admin-hub/supabase/migrations` was still
authoritative or whether migration ownership had moved to `aiorders-api` "the
way the edge functions did, and only got half-moved."

Investigating this at `designed` (2026-08-26) found the question had already
been answered — not by this ticket, and not by a live-ledger query, but by two
pairs of matched commits the approver pushed directly to both repos' `main` on
**2026-08-24**, one day after filing the request:

- `aiorders-api`: `4b6a835` "Add restaurant/profile migrations moved from
  aiorders-admin-hub" (09:52:28), `5b3bac2` "Consolidate remaining migrations
  from aiorders-admin-hub" (10:18:27).
- `aiorders-admin-hub`: `c90c02c` "Remove migrations moved to aiorders-api"
  (09:52:42, 14s after its pair), `919d355` "Remove supabase/migrations, fully
  consolidated into aiorders-api" (10:18:36, 9s after its pair).

Both repos' `supabase/config.toml` already confirmed the same live project
(`project_id = "bmnmnejwdxbcqinqkwko"`). Content-diffing all six of the
files the original request named against their new location in `aiorders-api`
(`origin/main`) found every one byte-identical to admin-hub's last committed
version before removal (`7009f18`) — one renamed from a UUID-suffixed
filename to a descriptive one, none edited. `aiorders-admin-hub`'s
`origin/main` now carries no `supabase/migrations/` directory at all.

This ADR is written retroactively — the decision was the approver's and was
already executed on disk two days before this record exists — because a
future engineer opening `aiorders-admin-hub` and finding no
`supabase/migrations/` directory needs the same answer this investigation
needed and had to reconstruct from git history.

## Decision

`aiorders-api` is the authoritative source for this database's tracked
migration history. `aiorders-admin-hub`'s `supabase/migrations` and
`supabase/functions` directories are intentionally empty — not an
in-progress move, not an accident — as of the approver's 2026-08-24 commits.
Any future migration for tables or policies this database uses belongs in
`aiorders-api`, not `aiorders-admin-hub`. `aiorders-admin-hub`'s
`supabase/config.toml` retains `project_id` (the repo's frontend code still
talks to this Supabase project directly for reads) but should not be read as
implying the repo owns any part of the tracked schema history.

## Alternatives

| Option | Why not |
|---|---|
| Treat this as still unsettled pending a live-ledger query | The file-level evidence is first-party (the account owner's own commits), dated, paired across both repos within seconds, and content-verified byte-for-byte — stronger for this specific question than a ledger row would add, given these are pre-existing already-applied migrations rather than new schema under test. Named as a residual gap in the ticket's design rather than treated as blocking. |
| Leave the fact undocumented, since the commits speak for themselves | This is exactly the failure this department's own ADR discipline exists to prevent — a fact a future reader has to reconstruct from git archaeology instead of finding in one place. `ADR-001`'s Alternatives table made the same point about an undocumented state gap; the same reasoning applies to an undocumented repo-ownership fact. |

## Consequences

**Accepted:** nothing new — this ADR changes no code and no running system. It
records a fact.

**Gained:** the next engineer or agent who opens `aiorders-admin-hub` and
wonders where its migrations went has an answer in one file instead of a git
archaeology exercise; `ENG-004`'s investigation doesn't have to be
re-performed if the same question is asked again.

**Reversibility:** the record itself is cheap to supersede if migration
ownership ever moves again. The underlying fact it records — the actual
consolidation on disk — was already a completed action before this ADR
existed; this ADR does not itself decide or reverse anything.

## Review trigger

If `aiorders-admin-hub` ever regains a `supabase/migrations` directory, or a
future change reintroduces schema ownership split across both repos, this ADR
is stale and should be superseded rather than trusted.
