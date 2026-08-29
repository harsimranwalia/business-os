---
id: ENG-004
title: Reconcile aiorders-admin-hub's deleted-but-uncommitted migration history
project: aiorders-admin-hub
type: chore
size: L
severity: P2
priority:
state: verified
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-25
updated: 2026-08-27
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-004-admin-hub-migration-history.md
  design: agents/architect/designs/ENG-004-admin-hub-migration-history.md
  adrs: [ADR-003, ADR-004]
  review: agents/principal-engineer/reviews/ENG-004.md
  test_plan: agents/qa/test-plans/ENG-004.md
  security_review: agents/security/reviews/ENG-004.md
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
- `2026-08-27` `designed → ready` (eng-manager, `continue ENG-004` event pass)
  — work breakdown, narrow scope per the event's own contract (resume this
  ticket from its current state; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

  **Work breakdown: zero implementation units.** Per `ADR-003` and `ADR-004`,
  the remediation this ticket investigated was already executed by the
  approver directly, on `origin/main`, on 2026-08-24 — no code, migration, or
  config change is owed by this ticket in either registered project. There is
  nothing to sequence and nothing to assign; the ticket proceeds directly to
  the building-as-verification-record step `ADR-004` defines (record the
  exact commits/files/diffs already checked at design time, `branch:` stays
  empty with a one-line note, per `ADR-001`'s pattern). `owner` moves from
  `architect` to `eng-manager` per `definition-of-done.md`'s state table.

  `machine_wip` (6, `config/config.yaml` → `wip.machine_limit`, re-checked
  fresh this pass) at 0/6 going in — nothing else on the board sits in
  `ready`..`ready-to-ship` (`ENG-005` is still at `shaped`, not in the counted
  range) — 1/6 after this ticket enters `ready`. No approver-facing WIP or
  approval-cap impact: `ready` raises no gate.

  **Not proceeding into `building` this pass, deliberately** — same reasoning
  `ENG-001`'s own history applied at this identical hop
  (`designed → ready` was one eng-manager pass, `ready → building` a separate
  one) and the same split this ticket's own prior log entry already flagged
  for this exact point. The building-as-verification-record write is real,
  distinct work reserved for its own session rather than the tail end of this
  one.

  **Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
  log now ends in a valid, accounted-for state with a chain record below.
  `ENG-005` (`shaped`, owner `product-manager`) untouched this pass — out of
  scope for a `continue` event naming one ticket.

  **Notify sweep:** nothing to raise (`ready` raises no gate item this pass).
  Nothing open to nudge — approval cap 0/3, nothing waiting on the approver.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.
  `chained: ENG-004` — sitting at `ready`, owned by `eng-manager` (agent, not
  the approver, not blocked, not terminal); firing `/bin/zsh
  departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
  building-as-verification-record session.
- `2026-08-27` `ready → building` (eng-manager, `continue ENG-004` event pass)
  — building-as-verification-record per `ADR-004`. Narrow scope per the
  event contract (resume this ticket from its current state; no board-wide
  sweep). Mode check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

  **Re-verified all five acceptance criteria against disk/git this pass**,
  fresh in `_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch
  origin` in both first), rather than trusting the design's prior citations:
  - **AC1** — both repos' `supabase/config.toml` still name `project_id =
    "bmnmnejwdxbcqinqkwko"`, read fresh off disk this pass.
  - **AC2/AC3** — `git ls-tree -r origin/main -- supabase` on
    `aiorders-admin-hub` returns exactly one entry, `supabase/config.toml` —
    no `migrations/` or `functions/` directory exists on `origin/main`. Both
    matched consolidation commit pairs (`4b6a835`/`c90c02c`,
    `5b3bac2`/`919d355`) are still present, unchanged, on their respective
    `origin/main`s (`git show --stat` on all four). Re-hashed all six named
    files with `sha256` — admin-hub's tree at `7009f18` against
    `aiorders-api`'s current `origin/main` — a stronger check than the
    design's own byte-diff: all six **identical**.
  - **AC4** — `git ls-tree -r --name-only origin/main -- supabase/migrations`
    on `aiorders-api` lists **22** files; sorted, `20260312000001_restaurant_activations.sql`
    (line 12) immediately precedes `20260408000001_google_review_history.sql`
    (line 13).
  - **AC5** — `git branch -vv` in `_eng/aiorders-admin-hub` shows local
    `main` marked `+` (checked out in the linked worktree at the human's own
    `~/Documents/projects/aiorders/aiorders-admin-hub`) at `919d355`,
    `[origin/main]`; `git rev-list --left-right --count main...origin/main`
    returns `0	0`. Ref-level only — no working-tree file in the human's
    checkout was read, per `config/projects.md`'s repo isolation.

  All five hold exactly as `designed` recorded them on 2026-08-26 — nothing
  drifted in the one day between design and this pass.

  `branch:` stays empty — this ticket produces no diff of its own; the diff
  it investigated already exists on `origin/main` in both repos, produced by
  the approver directly on 2026-08-24, two days before this ticket reached
  `designed`. Per `ADR-004`, this is the documented shape for this ticket's
  entire remaining lane, not an omission. `machine_wip` (6) unchanged at
  1/6 — `ready` and `building` both fall inside the counted range, so this
  transition crosses no cap boundary. No approver-facing WIP or
  approval-cap impact — `building` raises no gate.

  **Not proceeding into `in-review`/`in-qa` this pass, deliberately.** Per
  `schedules/eng_build_loop.md` step 6 those two are one combined hop, and
  per `ADR-004` each still owes its own independent re-derivation of the
  acceptance criteria against disk/git rather than a rubber-stamp of this
  pass's numbers — real, distinct gate work reserved for its own session,
  the same discipline this ticket has applied at every earlier hop
  (`intake→shaped`, `shaped→awaiting-scope`, `awaiting-scope→designed`,
  the `designed` investigation itself, and `designed→ready` were each their
  own pass).

  **Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
  log now ends in a valid, accounted-for state with a chain record below.
  `ENG-005` (`awaiting-scope`, owner approver) untouched this pass — out of
  scope for a `continue` event naming one ticket.

  **Notify sweep:** nothing to raise (`building` raises no gate item).
  Nothing new to nudge — approval cap unchanged at 1/3 (`ENG-005`'s G1
  only).

  Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.
  `chained: ENG-004` — sitting at `building`, owned by `eng-manager` per
  `ADR-001`'s owner override as extended by `ADR-004` (agent, not the
  approver, not blocked, not terminal); firing `/bin/zsh
  departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
  combined `in-review`/`in-qa` session.
- `2026-08-27` `building → in-review → in-qa` (eng-manager acting as
  principal-engineer and qa, `continue ENG-004` event pass — the dedicated
  combined session the preceding hop chained). Narrow scope per the event
  contract (resume this ticket from its current state; no board-wide sweep).
  Mode check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean. Fresh sweep found nothing pending for `ENG-004`
  specifically (the only open inbox item is `ENG-005`'s G1, untouched by this
  event).

  **The combined review+quality hop, per `schedules/eng_build_loop.md` step
  6.** Per `ADR-004`, neither role reviews a diff — both independently
  re-derive all five acceptance criteria against disk and git, fresh, not
  cited from the design's or the `building` pass's own numbers. Re-ran `git
  fetch origin` in both `_eng/aiorders-admin-hub` and `_eng/aiorders-api`
  first.

  **Acted as principal-engineer (`in-review`).** Re-confirmed: both repos'
  `supabase/config.toml` still name `project_id = "bmnmnejwdxbcqinqkwko"`
  (AC1); `git ls-tree -r origin/main -- supabase` on admin-hub still returns
  only `config.toml`, both consolidation commit pairs (`4b6a835`/`c90c02c`,
  `5b3bac2`/`919d355`) still present and unchanged on their respective
  `origin/main`s (AC2/AC3 provenance); re-hashed all six named files with
  `shasum -a 256`, admin-hub's tree at `7009f18` against `aiorders-api`'s
  current `origin/main` — all six **identical** (AC3 content); `aiorders-api`
  `origin/main` still lists 22 migrations with `restaurant_activations`
  immediately preceding `google_review_history` (AC4); admin-hub's local
  `main` still `0`/`0` ahead/behind `origin/main`, at `919d355` (AC5).
  Verdict **pass** — `agents/principal-engineer/reviews/ENG-004.md` written,
  `links.review` set.

  **Acted as qa (`in-qa`).** Wrote the test plan this ticket never had
  (`agents/qa/test-plans/ENG-004.md`), one row per acceptance criterion, each
  a direct git/disk check rather than an automated test — no suite exists to
  run and none is owed, per `ADR-001`/`ADR-004`. Failure-paths table names the
  design's own residual risk explicitly (a future pass trusting a worktree's
  stale branch instead of `origin/main`) and records that both this pass's
  receipts read `origin/main` directly, never the `_eng/` worktree's own
  checked-out files. Verdict **pass**, `links.test_plan` set.

  **2 transitions this pass** (`building→in-review`, `in-review→in-qa`) —
  well inside the 4-transition cap. `machine_wip` (6) unchanged at 1/6 — both
  states fall inside the counted `ready`..`ready-to-ship` range. No
  approver-facing WIP or approval-cap impact — neither state raises a gate.

  **Not proceeding into `in-security` this pass, deliberately.** Same
  discipline this ticket has applied at every earlier hop — each real,
  distinct piece of gate work gets its own session rather than the tail end of
  this one — but here the reason is sharper than "same discipline": `ADR-004`
  says explicitly that this ticket's security gate has real content (five of
  the six files under review **are** the RLS/`search_path` hardening surface)
  and "must not be waved through as if it were" ceremony, unlike `ENG-001`'s
  own security pass (ten OWASP categories `n/a`), which is the one case on
  this instance where review+quality+security were combined into a single
  pass. Folding a substantive security review onto the end of an
  already-complete review+quality hop risks exactly the rubber-stamp `ADR-004`
  warns against. `in-security`'s own dedicated pass gets a fresh context to
  confirm the hardening's *content*, not just its byte-identity.

  **Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
  log now ends in a valid, accounted-for state with a chain record below.
  `ENG-005` (`awaiting-scope`, owner approver) untouched this pass — out of
  scope for a `continue` event naming one ticket.

  **Notify sweep:** nothing to raise (`in-qa` raises no gate item). Nothing
  new to nudge — `ENG-005`'s G1 (raised 09:59:41) is well under the 24h
  threshold; approval cap unchanged at 1/3, not full, no stall.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
  whole-board: both exit 0, clean. `chained: ENG-004` — sitting at `in-qa`,
  owned by `qa` (agent, not the approver, not blocked, not terminal); firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-004` for
  the dedicated `in-security` session.
- `2026-08-27` `in-qa → in-security` (eng-manager acting as security,
  `continue ENG-004` event pass — the dedicated session the preceding
  combined review+quality hop chained). Narrow scope per the event contract
  (resume this ticket from its current state; no board-wide sweep). Mode
  check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`
  (`ENG_ROOT=instances/aiorders/engineering`): exit 0, clean.

  **The one gate on this ticket with real content, per `ADR-004` — not waved
  through as ceremony.** Threat-modelled first: no new input, capability, or
  data exposure exists anywhere in this ticket's own evidence (no diff, no
  new component); the equivalent question for a reconciliation ticket is
  whether the *tracked history* is trustworthy, which AC3/AC4 already speak
  to. Re-ran `git fetch origin` fresh in both `_eng/aiorders-admin-hub` and
  `_eng/aiorders-api` and independently re-derived, not cited from any prior
  hop's numbers:
  - **AC1** — both `supabase/config.toml` still name `project_id =
    "bmnmnejwdxbcqinqkwko"`.
  - **Presence** — all six files (one renamed) found on `aiorders-api`
    `origin/main`; `admin-hub`'s `origin/main` still carries no
    `supabase/migrations/`.
  - **AC3 (unmodified)** — checked by a **different mechanism** than
    review's and QA's SHA-256 hash: compared git's own blob SHA for each of
    the six files, content-addressed and independent of path/filename. All
    six identical pairwise, `admin-hub@7009f18` vs. `aiorders-api`
    `origin/main` (`204ccb6f…`, `11d8407a…`, `366dab7e…`, `2b441662…`,
    `431a7324…`, `8657b0c8…`). Confirmed by a second, independent method, not
    a re-run of the first.
  - **AC4 (ordering)** — 22 files on `aiorders-api` `origin/main`;
    `restaurant_activations` (line 12) immediately precedes
    `google_review_history` (line 13).

  **Read the six files' actual content — the substantive check neither
  review nor QA did (review's own words: "does not re-audit what they
  say").** All six are coherent, complete hardening: pinned `search_path` on
  two `SECURITY DEFINER` trigger functions; the `profiles` table's
  public-read policies replaced with owner-only + role-gated admin access
  (via a `SECURITY DEFINER` helper added specifically to break an
  infinite-recursion defect the first fix introduced); `restaurants`'
  unconditional public read blocked (`USING (false)`) and replaced with a
  `restaurants_public` view exposing an explicit safe-column allowlist
  filtered to `approved = true`; `restaurant_activations` created with RLS
  enabled and a `service_role`-only policy, correctly not granted to
  `anon`/`authenticated`. Full per-file breakdown in
  `agents/security/reviews/ENG-004.md`.

  **One observation, explicitly not filed as a finding against this
  ticket.** Migration 5's own comment ("recreate the view without SECURITY
  DEFINER — default is SECURITY INVOKER") is likely backwards — Postgres's
  actual default for a plain `CREATE VIEW` is owner-rights execution unless
  `WITH (security_invoker = true)` is set, which neither version of the view
  sets — so the drop-and-recreate may not have changed `restaurants_public`'s
  RLS-bypass posture at all. Not a finding here: the PRD's own non-goals
  exclude "whether that policy is still the right policy today," and this is
  exactly that question, not a question about whether this ticket's
  reconciliation preserved the content (it did, confirmed above by an
  independent hash method). No DB credential is available to check
  Supabase's advisor output live either (design, Risks). Logged in
  `agents/eng-manager/observations.md` rather than escalated or held against
  this gate.

  **OWASP walk, secrets, SOC 2 trail** — full table in the receipt file. A01
  engaged as content (not `n/a`) since access control on
  `profiles`/`restaurants` is exactly what these six files are; A02–A10 all
  `n/a` with reasons (no crypto, no dynamic SQL, no new feature, no new
  config surface, no dependency, no auth path change, no build artifact, no
  new logged event, no server-side fetch). Secret-shaped-string scan
  (`grep -niE 'api[_-]?key|secret|password|token|bearer|-----BEGIN'`) over
  the six files' content and this ticket's entire paper trail (PRD, design,
  both ADRs, board, review, test plan): zero hits in either sweep. SOC 2
  trail complete: ticket → PRD → `ADR-003`/`ADR-004` → design → review → test
  plan → this verdict, no gap.

  **Verdict: PASS.** `agents/security/reviews/ENG-004.md` written,
  `links.security_review` set. `machine_wip` (6) unchanged at 1/6 —
  `in-security` still falls inside the counted `ready`..`ready-to-ship`
  range. No approver-facing WIP or approval-cap impact — `in-security` raises
  no gate.

  **Not proceeding into `ready-to-ship` this pass, deliberately** — same
  discipline this ticket has applied at every earlier hop. Devops's own
  confirmation (per `ADR-004`: that no release plan, rollback, or
  observability plan exists, because the change already shipped outside this
  ticket on 2026-08-24) is real, distinct work reserved for its own session,
  not the tail end of an already-complete security hop.

  **Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
  log now ends in a valid, accounted-for state with a chain record below.
  `ENG-005` (`awaiting-scope`, owner approver) untouched this pass — out of
  scope for a `continue` event naming one ticket.

  **Notify sweep:** nothing to raise (`in-security` raises no gate item).
  Nothing new to nudge — `ENG-005`'s G1 (raised 09:59:41) is well under the
  24h threshold; approval cap unchanged at 1/3, not full, no stall.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
  whole-board: both exit 0, clean. `chained: ENG-004` — sitting at
  `in-security`, owned by `security` (agent, not the approver, not blocked,
  not terminal); firing `/bin/zsh departments/engineering/lib/eng-trigger.sh
  continue ENG-004` for the dedicated `ready-to-ship` (devops) session.
- `2026-08-27` `in-security → ready-to-ship → awaiting-release → shipped →
  verified` (eng-manager acting as devops, then product-manager —
  `continue ENG-004` event pass, the dedicated session the preceding
  `in-security` hop chained; this ticket reached terminal within the same
  pass because the G3 it raised was answered while the pass was still
  running). Narrow scope per the event contract (resume this ticket from its
  current state; no board-wide sweep). Mode check clean (business-os `.env`
  → `MODE=active`; instance `config/config.yaml` → `mode:` empty, falls
  through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  and whole-board: both exit 0, clean.

  **Acted as devops at `ready-to-ship`, per `ADR-004`.** Confirmed and
  logged rather than skipped: no release, rollback, or observability plan is
  owed, because the change this ticket concerns already reached
  `origin/main` on 2026-08-24, two days before this ticket reached
  `designed` — a different reason than `ADR-002`'s (no registered project
  carried a diff at all), same honest-recording shape. Re-checked fresh
  rather than cited: `config/projects.md` still lists `aiorders-admin-hub`
  at **L1** with a real Cloudflare deploy target; its `_eng/` worktree is
  present. Release window checked for consistency even though nothing
  deploys: 2026-08-27 is a Thursday, `ENG_RELEASE_FREEZE` unset — clean,
  moot either way. Recurring cost: `$0/month`, no CFO escalation owed — no
  diff, no new infrastructure. `machine_wip` (6) drops from 1/6 to 0/6 —
  `ready-to-ship` is the last state in the counted `ready`..`ready-to-ship`
  range; nothing else on the board sits inside it.

  **1 transition** (`in-security → ready-to-ship`).

  **Continued into `awaiting-release` the same pass, deliberately, unlike
  `ENG-001`'s split at this identical boundary.** Re-checked the approval
  cap and approver-facing WIP fresh from `inbox/` directly (one open item,
  `ENG-005`'s G1) rather than from the board's cached header: cap 1/3, room
  for two more; approver WIP 1, room for one more. Per the Guards section,
  raising this ticket's G3 is advancing an already-in-flight ticket into its
  own next gate, not a new start — the same reasoning `ENG-001`'s own history
  used at 2/3 approval cap with `wip.approver_limit` already held — so
  nothing caps it. This differs from `ENG-001`'s `ready-to-ship`/
  `awaiting-release` split, which its own log names as cap-driven and
  "independently sufficient on its own"; that condition doesn't hold here.
  No schedule rule or ADR names a fresh-context requirement between these two
  states the way step 6 names one for security-after-quality, and neither
  `ADR-002` nor `ADR-004` distinguishes a session boundary here — unlike
  `building`/`in-review`/`in-qa`/`in-security`, `awaiting-release`'s own
  "work" is writing and raising the gate item this state's exit condition
  already requires, not a fresh independent re-derivation. Per the schedule's
  own top-line description ("runs every in-flight ticket forward until it
  hits a human"), `ready-to-ship` is machine-owned and `awaiting-release` is
  exactly that human stop, so continuing into it is the literal dispatch
  rule, not a departure from it.

  Wrote the G3 item per `ADR-004`'s own framing — not "ship this to
  production" (nothing is shipping), but "is this ticket's record accurate,
  and is it done" — at `inbox/2026-08-27-eng004-g3-verification.md`, and
  raised it (`lib/eng-notify.sh raise`). Reproduced the already-filed,
  already-proposed `eng-notify.sh` bugs (`proposals.md`, 2026-08-25 row): log
  line read `sent: active`, not `sent: raise` (the `MODE` variable
  collision), and the message went to Slack rather than the Telegram
  `config/config.yaml` names as this instance's actual channel — not a new
  finding, not re-filed. `notified:` stamped by hand (`11:01:34` local) since
  the script never writes back. Approval cap 1/3 → 2/3 (`ENG-005`'s G1 +
  this ticket's G3); approver-facing WIP 1 → 2 (at the limit, not over it).

  **2nd transition** (`ready-to-ship → awaiting-release`).

  **The G3 was answered before this pass exited.** `decision: approved`,
  `decided: 2026-08-27T18:03:06.296846+00:00` (`11:03:06` local) — roughly
  92 seconds after `notified:` was stamped, by a direct hand-edit of the gate
  item's frontmatter plus a second `## Decision` section below the original
  placeholder, same shape as every gate answer on this instance except
  `ENG-002`'s GitHub merge. No additional comment beyond the decision itself.
  Journaled in `agents/eng-manager/config/decision-journal.md` (fifth data
  point on the hand-edit pattern; the turnaround itself flagged there as
  consistent with, not proof of, the open notify-channel proposal). Moved
  as-is to `inbox/_handled/2026-08-27-eng004-g3-verification.md`, no edit
  needed.

  **Acted as devops at `shipped`, per `ADR-004`.** Recorded the G3
  confirmation in place of a deploy. **No release record is fabricated** at
  `agents/devops/releases/` for a deploy that never happened — this log
  entry is the record, same as `ADR-002` decided for `ENG-001`. `links.release`
  stays empty, same shape as `branch:` staying empty under `ADR-001`.

  **3rd transition** (`awaiting-release → shipped`).

  **Acted as product-manager at `verified`.** Re-confirmed all five
  acceptance criteria against disk/git fresh this pass, not cited from any
  prior hop's numbers — `git fetch origin` in both `_eng/aiorders-admin-hub`
  and `_eng/aiorders-api` first:
  - **AC1** — both `supabase/config.toml` still name `project_id =
    "bmnmnejwdxbcqinqkwko"`.
  - **AC2/AC3** — `aiorders-admin-hub`'s `origin/main` still carries only
    `supabase/config.toml` (no `migrations/`); re-sampled two of the six
    files' git blob SHAs on `aiorders-api`'s `origin/main` —
    `20250729143432_updated_at_functions.sql` → `204ccb6f…`,
    `20260312000001_restaurant_activations.sql` → `8657b0c8…` — both match
    every prior gate's recorded values exactly.
  - **AC4** — `aiorders-api`'s `origin/main` still lists 22 migrations,
    sorted; `restaurant_activations` (line 12) still immediately precedes
    `google_review_history` (line 13).
  - **AC5** — `git rev-list --left-right --count main...origin/main` in
    `_eng/aiorders-admin-hub` still returns `0	0`.

  All five hold exactly as every earlier gate recorded them — nothing
  drifted across the two days since `designed`. Also re-opened and read (not
  just cited) all three receipts this pass:
  `agents/principal-engineer/reviews/ENG-004.md` (`verdict: pass`),
  `agents/qa/test-plans/ENG-004.md` (`last_result: pass`, all five AC rows
  `pass`), `agents/security/reviews/ENG-004.md` (`verdict: pass`, content
  read confirmed coherent, all ten OWASP categories addressed, secret scan
  clean). All three hold.

  **4th transition** (`shipped → verified`) — **4 transitions this pass**
  in total, at the 4-transition cap, not over it.

  **This ticket is now terminal.** All five acceptance criteria hold, every
  receipt this lane requires is on file and independently re-verified at
  least four times over (design, building, review+QA, security, this
  pass), and `aiorders-api` is confirmed, on record, as the authoritative
  migration history for this database. `ADR-003` and `ADR-004` stay on
  record for whichever future ticket needs the same pattern.

  As a side effect of this ticket closing, `machine_wip` stays 0/6 (it left
  the counted range at `ready-to-ship`, one transition ago); the approval cap
  drops from 2/3 back to 1/3 (`ENG-005`'s G1 only) and approver-facing WIP
  drops from 2 back to 1 — noted here for the next pass's arithmetic, not
  acted on: dispatching any newly-freed capacity onto another ticket is out
  of scope for a `continue ENG-004` pass scoped to this ticket.

  **Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
  log now ends in a valid, terminal state. `ENG-005` (`awaiting-scope`, owner
  approver) untouched this pass — out of scope for a `continue` event naming
  one ticket.

  **Notify sweep:** nothing to raise this pass beyond the G3 item already
  raised and now answered above; nothing to nudge (`ENG-005`'s G1 is well
  under 24h old); approval cap not full, no stall.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
  whole-board: both exit 0, clean. `chained: none` — `verified`, a terminal
  state. Per the chaining guard, a terminal ticket is never re-fired.
