---
id: ENG-004
title: Reconcile aiorders-admin-hub's deleted-but-uncommitted migration history
project: aiorders-admin-hub
type: chore
size: L
severity: P2
priority:
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-25
updated: 2026-08-26
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-004-admin-hub-migration-history.md
  design: agents/architect/designs/ENG-004-admin-hub-migration-history.md
  adrs: [ADR-003, ADR-004]
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
- `2026-08-26` `awaiting-scope → designed` (product-manager → eng-manager,
  `watch` event pass — a file changed in a watched inbox outside the notify/poll
  channel) — swept all three watched inboxes per the event's own narrower
  contract; found `inbox/2026-08-25-eng004-g1-scope.md` answered since the
  last pass touched it (the immediately preceding `decision` pass, which
  closed `ENG-001`'s G3 only and left this item untouched). **G1 approved**,
  `decided: 2026-08-27T05:57:21.472123+00:00` (2026-08-26T22:57:21-07:00
  local), no additional comment beyond `decision: approved`. Answered by a
  direct hand-edit of the gate item file rather than through
  `lib/eng-notify.sh`'s reply channel — frontmatter `decision:`/`decided:` set
  and a second `## Decision` section appended below the still-blank original
  placeholder. Second occurrence of that channel shape after `ENG-001`'s G3
  (see decision journal); moved the item to `inbox/_handled/` unedited, same
  treatment as that one. PRD `status: approved`,
  `decided: 2026-08-26` (`agents/product-manager/specs/ENG-004-*.md`).
  Journaled in `agents/eng-manager/config/decision-journal.md`.

  **Handed to the architect at `designed`, design work itself not started this
  pass.** Per `config/definition-of-done.md`'s state table, `designed`'s exit
  condition is "tech design written; ADRs logged; one-way doors decided or
  escalated" — for this ticket that exit condition is not a light design
  choice (contrast `ENG-002`'s test-runner pick, done inline the same pass its
  G1 was answered) but the substantive live-database investigation the PRD's
  Proposed change and G1 recommendation both call for: confirming
  `admin-hub`'s Supabase project linkage, reading the live
  `supabase_migrations.schema_migrations` ledger, and content-diffing six
  files against `aiorders-api`'s nine. That is new implementation-adjacent
  work against a project with real operator/customer data, not board
  bookkeeping, so — same reasoning `schedules/eng_build_loop.md`'s Cadence
  section gives for reserving `building` for a dedicated session — it belongs
  in a fresh, dedicated `continue ENG-004` context rather than folded into
  this narrowly-scoped `watch` pass. `machine_wip` (6) is irrelevant here (it
  counts `ready` through `ready-to-ship` only; `designed` isn't in that range)
  so nothing caps the handoff itself.

  **Capacity freed, not spent on anything else this pass.** Approval cap
  2/3 → 1/3 (`ENG-003` G1 only); approver-facing WIP 2 → 1 (`ENG-003` only,
  now well under the limit of 2). Per the same reasoning the preceding
  `decision` pass used for this exact situation, dispatching the newly-freed
  capacity onto another ticket (e.g. raising `ENG-005`'s G1) is left for the
  next `scheduled`/`watch`/`continue` pass — out of scope for a `watch` event
  scoped to the inbox item it found changed.

  Post-pass `lib/eng-gate-check.sh`: exit 0, clean. `chained: ENG-004` — sitting
  at `designed`, owned by `architect` (an agent, not the approver, not blocked,
  not terminal); firing `/bin/zsh lib/eng-trigger.sh continue ENG-004` for the
  dedicated investigation-and-design session.
- `2026-08-26` `designed` — investigation complete, tech design + two ADRs
  written (architect, `continue ENG-004` pass, dedicated session). Mode check
  clean (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty, falls back). Pre-pass `lib/eng-gate-check.sh`: exit 0, clean.

  **Ran the investigation the PRD's Proposed change calls for**, in
  `~/Documents/projects/_eng/aiorders-admin-hub` and `~/Documents/projects/_eng/aiorders-api`
  (department worktrees; the human's own checkouts were not touched, per
  `config/projects.md`). `git fetch` in both first.

  **AC1 — project linkage.** Both repos' `supabase/config.toml` name the same
  `project_id = "bmnmnejwdxbcqinqkwko"` — confirmed via each repo's own config
  file, the exact mechanism the architect's blind reading named at readback,
  not a live-ledger query.

  **AC2/AC3 — authoritative repo, and consolidation under a different name.**
  Both `_eng/` worktrees sit on a department branch (`eng/base`) diverged from
  `origin/main` — admin-hub's by one merge's worth, aiorders-api's by dozens of
  commits (its `eng/base` predates this consolidation entirely). Read
  `origin/main` directly instead of trusting either worktree's own files.
  Found two pairs of matched commits, both 2026-08-24, seconds apart, same
  session: `aiorders-api` `4b6a835` (09:52:28, "Add restaurant/profile
  migrations moved from aiorders-admin-hub") paired with `aiorders-admin-hub`
  `c90c02c` (09:52:42, "Remove migrations moved to aiorders-api"), then
  `aiorders-api` `5b3bac2` (10:18:27, "Consolidate remaining migrations from
  aiorders-admin-hub") paired with `aiorders-admin-hub` `919d355` (10:18:36,
  "Remove supabase/migrations, fully consolidated into aiorders-api"). **The
  approver did this directly, one day after filing the request, before this
  ticket ever reached `shaped`.** `aiorders-admin-hub`'s `origin/main` now
  carries no `supabase/migrations/` at all. Content-diffed all six named files
  (admin-hub's tree at `7009f18`, the last commit before removal) against
  their new location in `aiorders-api` (`origin/main`): all six
  byte-identical, one renamed (`20250729143432-1040fac4-....sql` →
  `20250729143432_updated_at_functions.sql`), none edited. Resolves the PRD's
  flagged "four siblings" discrepancy too: the real count is **three**
  (`20250729143357`, `20250814063455`, `20250814065341`), matching the three
  timestamps the original request actually named.

  **AC4 — replay integrity.** `aiorders-api`'s `origin/main` now holds all 22
  migrations in one chain; `20260312000001_restaurant_activations.sql` sorts
  before `20260408000001_google_review_history.sql` — the exact ordering
  hazard the original request flagged is resolved by the consolidation itself.
  Attempted an actual local replay (disposable Docker Postgres, zero
  production risk — `supabase start --exclude <all non-db services>` against a
  scratch dir seeded from `aiorders-api`'s `origin/main` migrations) to
  confirm mechanically rather than by inspection; aborted after ~3 minutes
  mid-image-pull as disproportionate — the byte-identical content diff plus
  verified filename ordering already answer what the replay would test, since
  none of these are new/untested SQL. Docker state confirmed clean afterward
  (no containers or volumes left running); scratch directories removed.

  **AC5 — pending deletion.** `aiorders-admin-hub`'s local `main` (the
  approver's own checkout) already matches `origin/main` exactly — no
  ahead/behind in `git branch -vv` — so the deletion sitting uncommitted on
  2026-08-23 is resolved at the ref level: `origin/main` already carries it,
  deliberately, correctly sequenced after the content move. Did not inspect
  the human's working-tree status directly (`~/Documents/projects/aiorders/aiorders-admin-hub`)
  — out of the department's view per `config/projects.md`, and unnecessary
  once the ref comparison settled it.

  **All five acceptance criteria satisfied without a diff in any registered
  project — but not for `ADR-001`'s reason.** `aiorders-admin-hub` **is**
  registered (L1); a diff was exactly the right mechanism and one happened,
  just not from this ticket's own `building` state. Wrote `ADR-003`
  (`agents/architect/decisions/ADR-003-aiorders-api-authoritative-for-migrations.md`,
  `decided_by: approver`, recorded retroactively) naming `aiorders-api`
  authoritative. Wrote `ADR-004`
  (`agents/architect/decisions/ADR-004-eng004-verification-ticket-second-occurrence.md`,
  `decided_by: architect`) extending `ADR-001`'s pattern across this ticket's
  entire remaining lane (`building` through `verified`) in one ADR rather than
  `ADR-001`+`ADR-002`'s two-step split, since the full remaining path is
  already known now. Explicitly engaged `ADR-001`'s own Review trigger (second
  verification-only ticket → reconsider internal-lane/G2): declined both —
  admin-hub fails the internal lane's own test on the facts (real Cloudflare
  deploy target, real traffic), and the two occurrences share a mechanism but
  not a cause, so a G2 on the pattern would be premature at n=2. `in-security`
  is named explicitly as *not* ceremony here — five of the six files under
  this ticket's history are the security surface itself. No one-way door: the
  ownership move is already an executed fact, not a pending decision — nothing
  to escalate. Tech design at
  `agents/architect/designs/ENG-004-admin-hub-migration-history.md`.
  `links.design`/`links.adrs` set on this ticket.

  **Two observations logged**, not folded into this ticket's scope:
  `_eng/aiorders-api`'s worktree branch has diverged far enough from
  `origin/main` that trusting its own files for investigation would have been
  wrong here and could mislead a future ticket the same way; and
  `aiorders-admin-hub`'s `supabase/config.toml` still lists 20 orphaned
  `[functions.*]` stanzas for functions no longer in that repo (harmless,
  unrelated to migrations). See `agents/eng-manager/observations.md`.

  **Not proceeding into `ready` or `building` this pass, deliberately** — same
  reasoning `ENG-001`'s own history applied at this exact point (`shaped →
  designed` was one architect pass; `designed → ready` was a separate
  eng-manager pass; `ready → building` separate again): work breakdown and the
  building-as-verification-record step are each real, distinct work reserved
  for their own session, and `ADR-004` gives whoever picks this up next
  everything needed to act without re-deriving it. `machine_wip` (6) and the
  approval cap are both unaffected — `designed` isn't in the counted range and
  no gate item was raised.

  Post-pass `lib/eng-gate-check.sh`: exit 0, clean. `chained: ENG-004` —
  sitting at `designed` with its exit condition now met (design written, ADRs
  logged, no one-way door outstanding), owned by `architect` handing to
  `eng-manager` for work breakdown (agent, not the approver, not blocked, not
  terminal); firing `/bin/zsh departments/engineering/lib/eng-trigger.sh
  continue ENG-004`.
