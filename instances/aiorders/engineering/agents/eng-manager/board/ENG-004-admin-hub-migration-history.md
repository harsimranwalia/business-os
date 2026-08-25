---
id: ENG-004
title: Reconcile aiorders-admin-hub's deleted-but-uncommitted migration history
project: aiorders-admin-hub
type: chore
size: L
severity: P2
priority:
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-25
updated: 2026-08-25
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-004-admin-hub-migration-history.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
---

## Input

Verbatim, from `inbox/requests/2026-08-23-admin-hub-migration-history.md`
(now `inbox/_handled/`), filed by the approver, received 2026-08-23 —
preserved here per `skills/request-readback/SKILL.md` step 1, never edited:

> Six aiorders-admin-hub migrations are deleted from the working tree and
> exist nowhere else
>
> While committing the AIOrders working trees on 2026-08-23, six migration
> files were found deleted from `aiorders-admin-hub`'s working tree but
> still present in `HEAD`. The deletion was **not committed** [...]
>
> [six filenames: search_path hardening, RLS additions x2, restaurants_public
> view creation and SECURITY INVOKER recreation, restaurant_activations table
> creation]
>
> `20260408000001_google_review_history.sql`... runs `ALTER TABLE
> restaurant_activations`. The only migration that creates that table is
> `20260312000001_restaurant_activations.sql`, one of the six. Committing the
> deletion breaks a from-scratch replay [...]
>
> **What this asks for:** Establish what the real migration history is and
> make the repo match it. The underlying question the department should
> answer first: is `aiorders-admin-hub/supabase/migrations` still
> authoritative at all, or did migrations move to `aiorders-api`... and only
> get half-moved?
>
> Nothing here is urgent. The deployed database is unaffected either way;
> this is about whether the tracked history can rebuild it.

Full text, including all six filenames, in the handled request file.

## Readback

See `agents/product-manager/specs/ENG-004-admin-hub-migration-history.md` →
Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

Six migration files — five RLS/`search_path` security-hardening migrations
and the one that creates `restaurant_activations` — are deleted from
`admin-hub`'s working tree but uncommitted, and committing that deletion
as-is would break a from-scratch replay (a later, already-committed
migration alters the table one of the six creates). Whether `admin-hub` is
even still the authoritative source for this database's migrations, versus
`aiorders-api`, is unconfirmed.

## Outcome

It's established, from the live Supabase project rather than either repo's
tree, which repo is authoritative for this database's migration history.
That repo's tracked migrations replay cleanly from empty to the live schema,
including the RLS/`search_path` hardening. The pending uncommitted deletion
is resolved deliberately, not left sitting.

## Notes

**Not yet gated.** This ticket was shaped in the same `scheduled
manual-unblock` sweep pass as `ENG-003` and `ENG-005`, from the same batch of
requests that sat unprocessed in `inbox/requests/` since 2026-08-23. The
`wip.approver_limit` (2) had exactly one free slot going into this pass
(`ENG-002` held the other), and it went to `ENG-003` — see that ticket's log
for the severity-based reasoning. This ticket sits at `shaped`, fully ready,
for the next pass that finds a slot free to raise its G1.

Likely candidate for a G2 conversation later if design concludes migration
ownership should formally move from `admin-hub` to `aiorders-api` — see PRD
Risks.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-25` `intake → shaped` (product-manager) — shaped from
  `inbox/requests/2026-08-23-admin-hub-migration-history.md` (filed by the
  approver, received 2026-08-23, unprocessed for two days — a `scheduled
  manual-unblock` sweep pass's PM work, not a self-originated finding). Ran
  the full request-readback (`skills/request-readback/SKILL.md`): this PM's
  reading plus a blind architect reading (independent subagent, raw request +
  business profile + relevant registry rows only) — no material divergence;
  both readings independently flagged the same open question (whether
  `admin-hub` and `aiorders-api` share a Supabase project at all — the
  registry names a project ref for one and not the other), and the
  architect's reading named the actual verification mechanism (the live
  migration ledger and each repo's `supabase/config.toml`, not a filename
  sweep). See the PRD's Readback section. Sized `L` (cross-project,
  investigation-plus-remediation with real cost if gotten wrong), so **G1 is
  required** per `agents/eng-manager/config/definition-of-done.md` → Size
  table. PRD written at
  `agents/product-manager/specs/ENG-004-admin-hub-migration-history.md`.
  **G1 not raised this pass** — `wip.approver_limit` (2) had one free slot,
  which went to `ENG-003` (higher effective urgency: an ongoing,
  possibly-live cost exposure vs. this ticket's own "nothing here is
  urgent"). Holding at `shaped`, owner `product-manager`, for the next pass
  that finds a slot free. `chained: none` — held by the WIP cap, not by
  anything this ticket itself is waiting on; firing `continue` now would
  just re-discover the same cap and burn a hop, so the To-do-column pick-up
  at the next dispatch (per `schedules/eng_build_loop.md` step 6) is what
  advances this, not a chain fired from here.
- `2026-08-25` `shaped → awaiting-scope` (product-manager, `scheduled
  manual-unblock` pass, retry) — `ENG-002`'s G1 was approved this same pass,
  freeing the `wip.approver_limit` (2) slot `ENG-003` had been holding
  alongside it. Took the freed slot ahead of `ENG-005` on severity (`P2` vs
  `P3`) — both are still at `shaped` with no `priority` set, so severity is
  the tie-break per `config/definition-of-done.md`. PRD `status:
  awaiting-scope`. G1 item written to `inbox/2026-08-25-eng004-g1-scope.md`
  and notified. `chained: none` — sitting at `awaiting-scope`, owned by the
  approver.
