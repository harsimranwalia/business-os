---
ticket: ENG-031
project: aiorders-api
released: 2026-09-04T01:51:41Z
released_by: approver (direct GitHub merge, no written reply)
autonomy: L1
gate_g3: n/a — L1 lane has no G3; the PR merge is the human gate
commit: 06e8e84 (merged via 3cf5607, PR #12)
environment: production (Supabase project bmnmnejwdxbcqinqkwko). Merge confirmed on `origin/main`; whether the statement has actually executed against the live database is unknown from this worktree — no `SUPABASE_ACCESS_TOKEN`, not linked, no Postgres/Supabase MCP reachable this session. See Health note.
rollback_tested: false — reasoned, not drilled (no Docker/psql/supabase CLI or MCP reachable from any build host on this instance, same standing gap `ENG-007`'s release already named). Reasoning: two nullable `ADD COLUMN IF NOT EXISTS` statements, no default, no backfill, no code path reads either column yet — dropping both columns is a complete, risk-free rollback.
health_check: not checked — no dashboard/monitoring access to bmnmnejwdxbcqinqkwko from this department; see Health note
cost_delta_monthly: 0
---

# Release — Catering order-capture columns (ENG-016 Piece 1, sub-ticket 1 of 4)

## What shipped

`public.catering` gets two new nullable columns —
`action_type text` (`QUOTE_SUBMITTED` | `MANUAL_CONTACT_REQUESTED` | null) and
`selections jsonb` (array of `{category, item_id, name, quantity, note}`,
null unless `action_type = QUOTE_SUBMITTED`) — via
`ADD COLUMN IF NOT EXISTS`, each with a documenting column comment. No
default, no `NOT NULL`, no `CHECK`, no enum type, no index, no backfill, no
code path reads or writes either column yet. This is step 1 of `ENG-016`'s
own Rollout order (schema before backend before either frontend) — inert
until `ENG-033` starts writing to it.

## Merge

No reply was ever written to this department's own merge-request item
(`inbox/2026-09-03-eng031-merge-request.md`, `decision:` still blank).
`aiorders-api` PR #12 was merged directly on GitHub instead. Confirmed
independently via local git ancestry, not trusted from the ticket's own
account alone:

```
$ git merge-base --is-ancestor refs/remotes/origin/pr/12 origin/main
YES ancestor
$ git log -1 --format="%H %ci %s" 3cf5607b9b8837b68cad7a4435ba1fc163570e8b
3cf5607b9b8837b68cad7a4435ba1fc163570e8b 2026-09-03 18:51:41 -0700 Merge pull request #12 from harsimranwalia/feat/ENG-031-catering-order-capture-migration
```

`refs/remotes/origin/pr/12`'s head (`06e8e84`) is exactly the commit this
ticket's own `ready-to-ship → blocked` log entry recorded — no drift, no
rebase. Single repo, no cross-ticket branch dependency. Per `eng_build_loop.md`
step 5, local git only — no `gh` call made for this detection.

## Gates

| Gate | Verdict | By | Date |
|---|---|---|---|
| Code review | pass | principal-engineer | 2026-09-03 |
| Quality | pass (no suite applies — pure DDL, no `.ts` touched) | qa | 2026-09-03 |
| Security | pass, one non-blocking finding (RLS activation on `public.catering` unverified from the repo, pre-existing, routed to `ENG-033`'s own future gate) | security | 2026-09-03 |
| Migration | pass | database | 2026-09-03 |
| G3 | n/a — L1 lane has no G3; the PR merge is the human gate | approver | 2026-09-03 |

## Deploy

- **Method:** merge to `main` only — no CI/CD auto-deploy exists on this repo
  (`.github/workflows/` absent from `origin/main`, confirmed same as every
  prior `aiorders-api` release on this board).
- **Why this department didn't run it:** `aiorders-api` is registered **L1**
  — a human merges, and running the deploy would exceed this department's
  own autonomy. This worktree also couldn't have run it: not linked, no
  `SUPABASE_ACCESS_TOKEN`.
- **What actually happened:** unknown from here — same open question every
  `aiorders-api` release on this board has recorded since `ENG-007`.
- **Migration:** additive-only, present on `origin/main`; live-push status
  unknown.
- **Feature flag:** none — no live caller of either column exists yet.
- **Duration:** n/a — no deploy run by this department.

## Verification

- `git ls-tree -r origin/main --name-only` confirms
  `supabase/migrations/20260903130000_add_order_capture_to_catering.sql` is
  present under the reviewed path, byte-identical to what review/QA/security
  each verified (single-file diff, `06e8e84`).
- Health checks: not run — see `health_check` above.
- Acceptance criteria: this ticket's own single criterion confirmed against
  the merged tree — see below.

## Acceptance criteria

Re-checked against `origin/main`
(`agents/architect/designs/ENG-016-catering-quote-generator.md`'s `## Data`
section): the two columns exist exactly as designed, with no default, no
`NOT NULL`, no `CHECK`, no enum, no index. **Pass.** None of `ENG-016`'s 13
feature-level acceptance criteria apply to this ticket's own diff — all
require `ENG-032`/`ENG-033`/`ENG-034`, none of which are built yet.

## Rollback

- **Path:** drop both columns — purely additive, no FK, no code path
  references either yet.
- **Tested:** not drilled — see `rollback_tested` above.
- **Used:** no.

## Health note

Same boundary every `aiorders-api` release on this board has hit: no
dashboard/monitoring access to `bmnmnejwdxbcqinqkwko` from this department's
worktree, and no separate deploy evidence exists here either — so both
whether the migration is live *and* whether it's healthy are unknown from
this department.

## Observability

N/a — no reachable runtime path exists anywhere yet (inert until `ENG-033`).

## Cost

$0/month delta — same Supabase project, two nullable columns, no new
service, no index.

## Follow-ups

This ticket's own `blocks: [ENG-032, ENG-033]` — `ENG-032`'s sole dependency
(`depends_on: [ENG-031]`) is now satisfied by this merge; `ENG-033` still
also depends on `ENG-032`, unaffected by this release alone. The security
gate's non-blocking RLS-verification finding on `public.catering` is
routed to `ENG-033`'s own future security gate, not re-opened here. The
`ENG-016` family (parent plus `ENG-031`..`034`) is not itself `shipped`/
`verified` — per `ADR-003`, the parent's own terminal state requires every
child `shipped`, `verified`, or `dropped`, with at least one having actually
shipped; three siblings remain unbuilt.
