---
type: eng-decision
agent: eng-manager
gate: G3
project: aiorders-admin-hub
ticket: ENG-004
recommendation: confirm — all five acceptance criteria are satisfied and independently re-verified three times over (review, QA, security); the reconciliation this ticket investigated was already executed by you directly on 2026-08-24, so there is nothing new to deploy — this is a record check, not a production go/no-go
raised: 2026-08-27
notified: 2026-08-27T11:01:34
decision: approved
decided: 2026-08-27T18:03:06.296846+00:00
---

# G3 — Reconcile aiorders-admin-hub's deleted-but-uncommitted migration history

## Not the usual G3

This ticket has a real deploy target — `aiorders-admin-hub` is registered at
**L1**, with a real Cloudflare deploy and real production traffic — but no
diff of its own. `ADR-003` and `ADR-004` (`agents/architect/decisions/`)
found that the reconciliation this ticket investigated was already executed
by you directly, on `origin/main`, on 2026-08-24 — two days before this
ticket even reached `designed`. So the question here is not "ship this to
production" (nothing is being shipped by this ticket); it's **"is this
ticket's record accurate, and is it actually done?"**

## What this asks you to confirm

1. `aiorders-api` is now the authoritative repo for this database's migration
   history, not `aiorders-admin-hub` — both share Supabase project
   `bmnmnejwdxbcqinqkwko`; `aiorders-admin-hub`'s `origin/main` carries no
   `supabase/migrations/` at all; the six files in question exist,
   byte-identical (one renamed), on `aiorders-api`'s `origin/main`.
2. The replay-ordering hazard the original request flagged is resolved:
   `aiorders-api`'s 22 migrations sort with `restaurant_activations`
   immediately before `google_review_history`.
3. The pending uncommitted deletion from 2026-08-23 is resolved at the ref
   level — `aiorders-admin-hub`'s local `main` (your own checkout) already
   matches `origin/main` exactly, 0 ahead / 0 behind.
4. The RLS/`search_path` hardening in the six files survived the move
   intact — confirmed by reading the content, not just matching a hash
   (`agents/security/reviews/ENG-004.md`).
5. Review, QA, and security have each independently re-derived all five
   acceptance criteria against disk/git, fresh, at every hop since design —
   all three verdicts are **pass**
   (`agents/principal-engineer/reviews/ENG-004.md`,
   `agents/qa/test-plans/ENG-004.md`, `agents/security/reviews/ENG-004.md`).

None of this was cited from an earlier hop's numbers without re-checking:
`aiorders-admin-hub`'s registration (L1) and worktree were both re-read fresh
this pass, and the release window and `ENG_RELEASE_FREEZE` were checked for
consistency even though nothing deploys. Full citations (commit SHAs, blob
hashes, `git ls-tree` output) are on the ticket's own log.

## Recommendation

**Confirm.** There is no release to weigh: `aiorders-admin-hub`'s Cloudflare
deploy is unaffected by this ticket either way, exactly as the original
request said ("the deployed database is unaffected either way; this is about
whether the tracked history can rebuild it"). No rollback, no observability
change, no recurring cost — devops confirms none of the three apply, because
none is triggered by a diff this ticket produced. This gate exists because
`docs/engineering-team.md` reserves "say yes to production" to you
specifically, department-wide, and `ADR-004` deliberately didn't invent an
exception for a ticket shaped like this one — see the ADR's Review trigger if
this framing feels like it asked something it didn't need to.

## PRD / design / ADRs

- `agents/product-manager/specs/ENG-004-admin-hub-migration-history.md`
- `agents/architect/designs/ENG-004-admin-hub-migration-history.md`
- `agents/architect/decisions/ADR-003-aiorders-api-authoritative-for-migrations.md`
- `agents/architect/decisions/ADR-004-eng004-verification-ticket-second-occurrence.md`

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-27T18:03:06.296846+00:00
