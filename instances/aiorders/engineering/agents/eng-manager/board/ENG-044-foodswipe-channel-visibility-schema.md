---
id: ENG-044
title: FoodSwipe channel-visibility columns and discovery-RPC channel gate
project: aiorders-api
type: feature
size: S
time_estimate: a few hours
time_spent: ~2h build (live-schema check, both migrations, disposable-replica verification including rollback) plus one combined review+QA hop plus one release-readiness hop
time_remaining: none — waiting on the approver's merge
severity: P3
priority:
state: verified
owner: eng-manager
lane: full
blocked_on: 
blocked_from: 
source: approver
created: 2026-09-07
updated: 2026-09-07
branch: feat/ENG-044-foodswipe-channel-visibility-schema
depends_on: []
blocks: [ENG-045, ENG-046]
parent: ENG-026
links:
  prd: agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md
  design: agents/architect/designs/ENG-026-foodswipe-channel-visibility.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-044.md
  test_plan: agents/qa/test-plans/ENG-044.md
  security_review: agents/security/reviews/ENG-044.md
  release:
  pr: https://github.com/harsimranwalia/aiorders-api/pull/19
---

## Problem

`restaurants` has no per-channel visibility flags, so `get_restaurants_optimized`
cannot gate its result set by channel. The RPC's own defining migration also
never followed it when `restaurant-marketplace`'s `supabase/functions/*` was
deleted (`f733e68`, 2026-08-23) — it still lives only in that repo's migration
history, untracked from `aiorders-api`, which is where the function actually
runs today.

## Outcome

Three new `NOT NULL` boolean columns exist on `public.restaurants` —
`has_order_food` (default `true`), `has_dine_in` (default `false`),
`has_catering` (default `false`) — correctly backfilled for every existing
row, not just defaulted. `get_restaurants_optimized` accepts a new
`p_channel text DEFAULT NULL` parameter and returns `opening_hours`;
omitting the parameter reproduces today's exact behavior. The function's full
definition is now tracked in `aiorders-api`'s own migration history.

## Notes

Design: `agents/architect/designs/ENG-026-foodswipe-channel-visibility.md` —
`## Data` and `## Interfaces` (RPC section). Two migrations, per the design's
own `## Components` table. **Filenames actually used differ from the design's
own — see this ticket's own Log for why (a timestamp collision with `ENG-031`,
which shipped a migration under the exact `20260903130000` prefix the design
was written against):**

1. `supabase/migrations/20260907120000_add_channel_visibility_to_restaurants.sql`
   — the three columns, defaults, column comments (matching this table's
   existing comment convention), and the backfill below. No index — these are
   read via each tab's own already-indexed-or-not discovery query, never
   queried in isolation.
2. `supabase/migrations/20260907120001_gate_get_restaurants_optimized_by_channel.sql`
   — `CREATE OR REPLACE FUNCTION get_restaurants_optimized`, porting the
   existing definition forward from `restaurant-marketplace`'s
   `20240302_optimize_restaurant_discovery.sql` (read it directly — do not
   reconstruct the function from memory or from the fallback handler) plus the
   channel gate and `opening_hours` in `RETURNS TABLE`. This also completes
   `ADR-003`'s migration-ownership call (consolidating this function's
   canonical definition into `aiorders-api`) — not a new decision, cite it,
   don't re-litigate. `restaurant-marketplace`'s own copy becomes historical;
   leave it in place, do not delete it (out of scope, design's own Risks).

**Backfill — requirement 7 / AC5, this ticket's own load-bearing piece, not
optional cleanup:**

- `has_order_food`: the column default (`true`) *is* the backfill. No
  existing gate restricts this tab today, so every row defaulting to visible
  reproduces current behavior exactly.
- `has_catering`: `UPDATE restaurants SET has_catering = live_catering` in the
  same migration. `live_catering` is `NOT NULL` and already populated on
  every row today.
- `has_dine_in`: **cannot be resolved from the repo alone — check the live
  schema before writing this migration.** Query
  `information_schema.columns` (or the Supabase dashboard) for an existing
  `dine_in` boolean on `restaurants`.
  - **If it exists:** backfill `has_dine_in` from its value in the same
    migration, exactly like `has_catering` above, and leave `dine_in` in
    place — do not drop it this migration (reversibility during rollout; a
    follow-up cleanup ticket drops it once `ENG-046`'s repoint has shipped
    and nothing reads the old name).
  - **If it does not exist:** `has_dine_in` starts `false` for every row
    exactly as the approver's own spec defaults it — this is the approver
    having already made this call explicitly, not this ticket guessing.
  - Record which branch applied, in this ticket's own Log — `ENG-046`
    depends on knowing which one before it can decide whether its own
    `dine_in`-bound Switch is a repoint or a fresh addition.

**RPC gate — exact `WHERE` clause addition** (design's own `## Interfaces`):

```sql
AND (
  p_channel IS NULL
  OR (p_channel = 'order_food' AND has_order_food)
  OR (p_channel = 'dine_in'    AND has_dine_in)
  OR (p_channel = 'catering'   AND has_catering)
)
```

`DEFAULT NULL` plus the `IS NULL` branch is what makes this backward
compatible by construction — an existing caller that omits the parameter
must see exactly today's unfiltered behavior. Explicit `CASE`-shaped
predicate over three named values, not dynamic SQL — matches this function's
existing style (`p_cuisines`, `p_services`, `p_price_levels`, …).

**AC ownership** (mapped in
`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`): this
ticket owns AC1 in full and AC5 in full (the backfill decision, evidence-based
per the live-schema check above, not silently defaulted).

Branch from `origin/main` in the `aiorders-api` worktree.

## Log

- 2026-09-07 `(created) → building` (eng-manager, `work-breakdown`, `continue
  ENG-026` event pass) — sub-ticket of `ENG-026`, sequence 1, no dependency,
  dispatched straight to `building`. `time_estimate` a few hours, 0h spent.
  Machine WIP: this ticket is part of `ENG-026`'s own family, not a second
  occupant of the `1/1` slot — same reading `ENG-016`/`ENG-019`/`ENG-021`
  already established. Full reasoning:
  `agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`.
  `chained: ENG-044` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-044`
  before this pass exits.

- 2026-09-07 `building → in-review` (database, `continue` event pass, context
  `ENG-044`). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
  lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh ENG-044`: exit 0, clean.

  **Worktree found on a stale but harmless branch, not started fresh.**
  `~/Documents/projects/_eng/aiorders-api` was on `feat/ENG-040-...` (already
  `verified`, per the board) with zero uncommitted modifications — only the
  same long-standing, already-independently-noticed
  `supabase/functions/brand-portal/deno.lock` untracked file (`ENG-029`,
  `ENG-031`, `ENG-037` have each already left it alone; not re-observed
  again here). `git fetch origin main` then a fresh
  `git switch -c feat/ENG-044-foodswipe-channel-visibility-schema
  origin/main` — no work lost, nothing stashed.

  **Live-schema check run (this ticket's own load-bearing piece, AC5).**
  `supabase link --project-ref bmnmnejwdxbcqinqkwko` (not already linked this
  session, unlike `ENG-037`'s finding — non-interactive, no password
  prompt), then `supabase db dump --linked --schema public` (schema only) and
  one narrowly-scoped `supabase db query --linked` aggregate (single row,
  counts only, no per-row data). Findings: 243 restaurants total; `dine_in`
  **is** a real, live, `NOT NULL DEFAULT true` boolean (241/243 true, 2
  differ) — not a dead form field. Branch taken per the design's own
  conditional: backfill `has_dine_in` from `dine_in`'s per-row value, leave
  `dine_in` in place. **Recorded here explicitly for `ENG-046`:** this is a
  **repoint**, not a fresh addition — its own Notes' conditional branch A
  applies. Also confirmed `opening_hours` is `jsonb[]` (Postgres array), not
  plain `jsonb` — `RETURNS TABLE` typed to match. Full numbers and reasoning:
  `agents/database/migrations/ENG-044-foodswipe-channel-visibility-schema.md`.

  **Migration filenames changed from the design — a real collision, not a
  style choice.** The design's own `20260903130000_...` prefix was claimed
  four days ago by `ENG-031`'s already-shipped migration (different suffix,
  same thirteen digits). Renamed both files to `20260907120000`/`...0001`
  (today's date, after every existing migration) and corrected the two
  mentions (this ticket's own Notes, the design's Components table) rather
  than leaving a future reader to trip over stale filenames. Observation
  filed (`observations.md`) — first occurrence of a work-breakdown
  decomposition's baked-in filename colliding with a sibling family's
  already-shipped migration.

  **A real Postgres defect caught by testing, not by inspection.** Changing
  `get_restaurants_optimized`'s `RETURNS TABLE` shape while adding a
  parameter required verifying `CREATE OR REPLACE FUNCTION` would actually
  replace the live 13-arg function rather than silently coexist with it as a
  second overload — tested directly (disposable container) and confirmed a
  bare `CREATE OR REPLACE` with the changed arg count does **not** error, it
  creates a duplicate overload, and Postgres's overload resolution would keep
  routing old-shaped calls to the stale, ungated function forever. The
  migration's leading `DROP FUNCTION IF EXISTS` (exact old 13-arg type list)
  is what closes this — verified by re-running the real migration file
  against the two-overload state and confirming exactly one function
  remained. Full writeup, since this is reusable knowledge for any future
  parameter-count change on an existing function:
  `agents/database/notebook/2026-09-07-eng044-function-signature-overload-trap.md`.

  **Self-tested, per this state's own exit condition — against a disposable
  local replica** (`public.ecr.aws/supabase/postgres:15.8.1.073`, cached from
  `ENG-037`'s own pass; the bare `supabase/postgres:...` tag misses that
  cache and re-pulls from Docker Hub — hit this, killed it, redone against
  the cached tag, corrected in the notebook entry above). Seeded a minimal
  `restaurants`/`brands`/`offers` stand-in, five rows chosen to exercise
  every branch (catering-only, the 241-of-243 default case, unapproved,
  hidden-from-marketplace, order-food-only). Applied both migrations,
  confirmed by direct query: column shapes exact; `has_catering`/
  `has_dine_in` backfill matches `live_catering`/`dine_in` on every row, zero
  mismatches; `p_channel` NULL/`order_food`/`dine_in`/`catering` each return
  exactly the expected row set; unapproved/hidden rows excluded under every
  channel including NULL; `total_count` reflects the post-filter count; the
  historical 13-positional-argument call shape still executes and returns
  the same 3 rows (backward compatibility proven, not just asserted);
  `opening_hours` and the pre-existing, untouched `orderingLink` filter both
  still function correctly. **Rollback for both migrations actually run**,
  not asserted — function reverts to exactly 13 args and the old call shape
  still works; all three columns confirmed dropped. Container removed after.
  Full detail:
  `agents/database/migrations/ENG-044-foodswipe-channel-visibility-schema.md`.

  **Artifact enumeration (step 6b):** `grep -rln
  "has_order_food\|has_dine_in\|has_catering"` and a separate check for the
  two migration filenames, across `agents/` (instance) and
  `departments/engineering/`. Ten files hit; the PRD, the parent's own board
  file, the work-breakdown notebook, `proposals.md`, and the archive are
  historical/spec references, not in conflict. `ENG-045`/`ENG-046`/`ENG-047`
  (siblings, not yet built) all reference `p_channel`, `opening_hours`, and
  the three column names consistently with what was actually built — no
  drift, nothing to fix. The two real conflicts (design's Components table,
  this ticket's own Notes, both naming the now-collided filenames) are the
  rename above.

  **PR body written** (`building`'s own exit condition; no PR opened yet —
  L1 autonomy opens it at release-readiness):
  - *What it does:* Adds `has_order_food`/`has_dine_in`/`has_catering`
    (all `boolean not null`) to `public.restaurants`, backfilled from
    `live_catering`/pre-existing `dine_in` (confirmed live, not assumed) —
    `has_order_food` relies on its own `true` default as the entire
    backfill. Ports `get_restaurants_optimized` into this repo's own
    migration history (`ADR-003`), adding `p_channel text default null`
    (appended last) and `opening_hours jsonb[]` in `RETURNS TABLE`
    (appended last) — both additive and backward compatible by
    construction, proven against a disposable replica including the old
    13-arg call shape.
  - *What it deliberately does not do:* No index (existing discovery
    queries already cover these columns). No `CHECK`/enum. Doesn't touch
    `admin-portal/handlers/restaurants.ts` (already passes new fields
    through with zero code) or any frontend — schema and RPC only.
  - *Uncertainties:* None load-bearing — this is the one sub-ticket in the
    `ENG-026` family with live database access available, so every claim
    here (numbers, backfill correctness, RPC behavior, backward
    compatibility, the overload trap) was tested directly rather than
    inferred.
  - *What to review hardest:* The `DROP FUNCTION IF EXISTS` line in
    migration 2 — it looks like copied boilerplate from the 2024 source
    file but is doing real, load-bearing work here (see the overload-trap
    writeup); confirm the dropped type list still matches `pg_proc`'s live
    signature at review time, in case anything else touches this function
    between now and then.

  Branch committed (`81350d4`, 2 files) and pushed:
  `origin/feat/ENG-044-foodswipe-channel-visibility-schema`.

  **1 transition this pass** (`building → in-review`), under the cap of 4 —
  `in-review`/`in-qa` (combined hop, principal-engineer + qa) is a fresh
  session's work per `eng_build_loop.md`'s "a pass stops after `building` on
  purpose." No WIP-cap change: this ticket was already inside the counted
  `ready..ready-to-ship` range at `building`; `in-review` is still inside it.
  Machine WIP still held by the `ENG-026` family, unaffected.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise — `in-review` needs no approver gate.
  Nothing to nudge.

  **Observations filed:** (1) the migration-filename collision pattern —
  `observations.md`, this date. (2) the Postgres function-overload trap and
  two small tooling corrections — database agent's own notebook, not
  `observations.md`, since this is reusable technical knowledge for the
  agent's own future work, not a department-process gap.

  `chained: ENG-044` — `in-review` is agent-owned (principal-engineer + qa
  combined hop next), not the approver, not blocked, not terminal, not held
  by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-044`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-044`) and
  whole-board: see board index for result.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

- 2026-09-07 `in-review → in-qa` (principal-engineer + qa, combined hop,
  `continue ENG-044` event pass). **Review: pass** — 0/10 automatic
  failures; port verified byte-for-byte against real source history; `DROP
  FUNCTION` signature confirmed against the true original; the one live
  caller traced and confirmed unaffected. **QA: pass** — this ticket's own
  AC1 and AC5 covered by inspection/live evidence/call-site trace; no suite
  exists for `aiorders-api` (open proposal, unrelated to this ticket); 0
  open P0/P1. Receipts: `agents/principal-engineer/reviews/ENG-044.md`,
  `agents/qa/test-plans/ENG-044.md`; `links.review`/`links.test_plan` set.
  No WIP/cap change — still inside the counted `ready..ready-to-ship` range.
  Reasoning: `agents/principal-engineer/notebook/2026-09-07-review-log.md`,
  `agents/qa/notebook/2026-09-07-coverage-gaps.md`.
  `chained: ENG-044` — `in-qa` is agent-owned (security next), not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-044`
  before this pass exits.

- 2026-09-07 `continue (ENG-044)`: security gate — PASS — `in-qa →
  ready-to-ship`. `continue` event pass, context `ENG-044`, per prior pass's
  own `chained: ENG-044`. Reading map for `continue`: steps 6 and 6b, plus
  the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The
  four lanes*; *Guards*). Mode check clean (`MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh ENG-044`: exit 0, clean.
  `git fetch` + `git diff origin/main...HEAD --stat` on the worktree
  confirmed no drift since the QA hop (`aiorders-api@81350d4`,
  `origin/main@5e36648`).

  Acted as `security` on this hop, per `skills/security-gate/SKILL.md`.

  **Verdict: PASS.** Threat-modelled the diff (4 questions) before the
  checklist. Read the actual `WHERE` clause rather than trusting the
  ticket's/review's account of it: the new `p_channel` predicate is `AND`-ed
  onto the pre-existing `approved`/`show_in_marketplace` gate, so it can only
  narrow visibility, never widen it. Independently re-diffed the ported
  function against `restaurant-marketplace`'s real
  `20240302_optimize_restaurant_discovery.sql` (pulled fresh from that repo's
  own worktree, not trusted from the review's "byte-for-byte" claim) —
  identical apart from the two stated additive changes. Re-confirmed the
  `DROP FUNCTION IF EXISTS` signature (13 types) against that same source and
  confirmed the re-issued `grant execute ... to anon, authenticated,
  service_role` matches the original grant verbatim (a `DROP` clears grants,
  so re-granting is load-bearing, not defensive copy-paste). Full OWASP
  A01–A10 walk, LLM checklist (n/a, confirmed no model/agent/tool/MCP code in
  either changed file), secret scan (clean — `git diff origin/main...HEAD`
  and `git log -p origin/main..HEAD` on the one commit), dependency check
  (none — `git diff origin/main...HEAD --stat -- '*.json' '*.lock'` empty)
  and PII check (none — `opening_hours` is Public-classified, already
  client-visible elsewhere; the three new columns are staff-set flags, not
  user data) in `agents/security/reviews/ENG-044.md`. `links.security_review`
  set in the same write.

  **Zero findings** — blocking or non-blocking. Reported as a clean gate
  rather than manufacturing a finding to match the shape of recent reviews:
  the free-text, unvalidated `p_channel` parameter matches this function's
  own long-standing pattern (every other filter parameter has always been
  unvalidated free text/array too) and degrades to zero rows on an
  out-of-enum value, never an error or a distinguishable code path — not a
  new gap this diff introduces.

  **SOC 2 evidence trail** — all five upstream artifacts (PRD, design,
  review, test plan) confirmed present on disk this pass: ticket → PRD
  (`agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md`) →
  design (`agents/architect/designs/ENG-026-foodswipe-channel-visibility.md`)
  → review (`agents/principal-engineer/reviews/ENG-044.md`, pass) → test run
  (`agents/qa/test-plans/ENG-044.md`, pass) → this verdict → release record
  (pending, devops next). No gap.

  **1 transition** (`in-qa → ready-to-ship`), well under the cap of 4.
  Machine WIP unaffected — `ready-to-ship` is still inside the counted
  `ready`..`ready-to-ship` range, still `1/1`, held by the `ENG-026` family.

  **6b:** not applicable — no receipt path, state name, config key, or
  cross-file artifact rule was written or relied on this hop;
  `links.security_review` is a per-ticket frontmatter field, not a shared
  artifact another file references by path.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise this pass — a `pass` verdict isn't a
  gate item. Nothing to nudge.

  **Observations/exceptions/journal:** none — no observation worth filing
  beyond the review already written; no `exception-request:`; no
  G1/G2/G3/merge-request answered this pass.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

  `chained: ENG-044` — `ready-to-ship` is agent-owned (`devops` next, release
  readiness), not the approver, not blocked, not terminal, not held by a
  cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-044`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-044`) and
  whole-board: see board index for result.

- 2026-09-07 `ready-to-ship → blocked` (devops, `continue ENG-044` event
  pass, `skills/release-runner/SKILL.md` run step by step). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh
  ENG-044`: exit 0, clean.

  **Step 1 (window check): skipped.** `aiorders-api` is registered L1
  (`agents/eng-manager/config/projects.md`) — opening a PR is not a
  release, so the window check doesn't apply (per the approver's own
  2026-08-29 correction).

  **Step 2 (upstream gates), all four re-read fresh from the receipt
  files:** review (`agents/principal-engineer/reviews/ENG-044.md`, pass),
  quality (`agents/qa/test-plans/ENG-044.md`, pass), security
  (`agents/security/reviews/ENG-044.md`, pass, zero findings), migration
  (`agents/database/migrations/ENG-044-foodswipe-channel-visibility-schema.md`,
  pass).

  **Step 3 (readiness gate), no blocking failure:**
  - *Rollback:* tested, not reasoned — both migrations' rollbacks actually
    run against a disposable local replica during the `building` hop
    (`supabase/postgres:15.8.1.073`): function reverts to exactly 13 args
    with the old call shape still working; all three columns confirmed
    dropped after migration 1's rollback.
  - *Observability:* read the actual caller rather than assuming one
    exists. `aiorders-api/supabase/functions/restaurant-marketplace/handlers/restaurants.ts`'s
    `handleRestaurantDiscovery` — the one live caller of this RPC today —
    already wraps the call in error handling: logs
    `console.error('Restaurant discovery error:', error)` and automatically
    falls back to `handleRestaurantDiscoveryFallback` on Postgres error code
    `42883` (undefined function), exactly the failure class a signature
    mismatch would raise. Pre-existing, not added by this ticket, but
    directly on point given this migration's own tested defect class (the
    overload trap named in the migration file). Confirmed via the
    disposable-replica testing already done that this migration doesn't
    trigger that path — old call shape still resolves to exactly one,
    correct function post-migration. No new reachable behavior exists yet
    either way: nothing calls with a non-null `p_channel` until `ENG-045`
    ships, same "inert until the sibling ships" shape `ENG-031`'s own
    release used.
  - *Cost:* $0/month — same Supabase project, three boolean columns plus one
    function replacement, no new service, no new dependency, no index.
    Matches the design's own "Recurring cost: None" (`## One-way doors`
    table).
  - *Window:* n/a, L1 (step 1).

  **Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
  re-checked fresh, not assumed unchanged — `git fetch origin main`, `HEAD`
  at `81350d4` matching every gate's cited head, no drift (`git diff
  origin/main...HEAD --stat`: 2 files, 273/-0, exactly the two migration
  files). Only the same long-standing untracked
  `supabase/functions/brand-portal/deno.lock` present, left alone per every
  prior pass's own precedent. `gh pr list` confirmed no PR already existed
  for this branch. Opened `aiorders-api` PR #19
  (https://github.com/harsimranwalia/aiorders-api/pull/19). Wrote
  `inbox/2026-09-07-eng044-merge-request.md`, plain `pr_url:` string
  (single repo), `time_estimate: a few hours` carried from the ticket's own
  frontmatter. `lib/eng-notify.sh raise` exited 0; confirmed sent from
  `traces/eng-notify-2026-09-07.log` (`03:48:06`); stamped `notified:
  2026-09-07T03:48:06` on the item by hand.

  State `ready-to-ship → blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, `owner: devops → approver`, `links.pr` set. No G3 — L1 has
  none; the PR merge is the human gate. No release record yet — L1's actual
  deploy (a manual `supabase functions deploy`/migration push after merge,
  same by-hand pattern every prior `aiorders-api` release on this board has
  shown) and the release record both wait for merge detection on a future
  pass.

  **1 transition** (`ready-to-ship → blocked`), well under the cap of 4.
  **Machine WIP unaffected — still `1/1`, held by the `ENG-026` family.**
  This is the family-slot reading `ENG-016`'s/`ENG-019`'s/`ENG-021`'s own
  decompositions already established, not a per-row count: `ENG-026` itself
  is still `building`, and `ENG-045`/`ENG-046` (both `depends_on: [ENG-044]`)
  stay `ready` — that dependency clears only on `verified`, same bar
  `ENG-031→ENG-032` and this ticket's own siblings' precedents already set,
  not on `blocked_on: approver`. So the "never idle" slot-freed provision
  (`eng_build_loop.md` Guards, amended 2026-09-06) does not apply to this
  hop: it frees a slot held by a *single* ticket parking on the approver,
  and this slot is still occupied by three other family members inside the
  counted `ready..ready-to-ship` range. Nothing new dispatched this pass.

  **6b:** not applicable this hop — the merge-request item follows this
  board's own established format exactly (`ENG-040`'s, `ENG-041`'s); no new
  receipt path, state name, config key, or cross-file artifact rule was
  introduced.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract; `ENG-045`/`ENG-046`/`ENG-047`
  correctly left untouched at `ready`.

  **Notify sweep:** this pass's own merge request raised and stamped above.
  Checked every other open `inbox/` item per the not-negotiable step 7:
  `ENG-016`'s continue-Piece-2 question, `ENG-018`'s G1, `ENG-028`'s
  rescope G1, `ENG-042`'s G1, and `ENG-043`'s clarification all already
  carry their one-ever `nudged:` — no action. `PROP-2026-W36` (`notified:
  2026-09-06T18:57:12`) is under 24h old — no action.

  **Observations/exceptions/journal:** none — no observation worth filing
  beyond the readiness reasoning already written above; no
  `exception-request:`; nothing was *answered* this pass (a merge request
  was raised, not resolved), so no decision-journal entry is owed yet.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-044`) and whole-board: both exit 0, clean.

  `chained: none — blocked_on: approver`. Per `eng_build_loop.md` step 9 and
  the Guards section, a ticket waiting on the approver is never chained;
  the PR merge is the next event, and the build loop's own step-5 merge
  detection (or a `watch`/`scheduled` sweep) picks it up without a fired
  hop.

  ---

  **`watch (launchd)` event pass, ~03:56 PDT.** Fired by this ticket's own
  merge-request file landing in `inbox/` (the file-watcher observing the
  same write the immediately preceding pass made); per the event's reading
  map, step 5 applies since the changed file is a merge-request item.
  Re-checked in the department's own worktree
  (`~/Documents/projects/_eng/aiorders-api`): `git fetch origin`, then
  `git merge-base --is-ancestor
  origin/feat/ENG-044-foodswipe-channel-visibility-schema origin/main` — not
  an ancestor. Cross-checked directly against the PR: `gh pr view 19 --json
  state,baseRefName,mergedAt,mergeCommit,headRefName` → `state: OPEN`,
  `mergedAt: null`. PR opened ~8 minutes before this check — no realistic
  window for the approver to have acted yet. **No change** — ticket
  correctly stays `blocked`, `blocked_on: approver`. Notify sweep: this
  item is ~8 minutes past its own `notified:` stamp, nowhere near the 24h
  nudge threshold — no action. `chained: none — blocked_on: approver`. Full
  pass detail: `agents/eng-manager/board/_index.md`'s own dated entry,
  2026-09-07 "watch (launchd): inbox sweep — `ENG-044`'s merge request
  re-checked, still open."

- `2026-09-07` `blocked → shipped` (control center, merge detected) — `feat/ENG-044-foodswipe-channel-visibility-schema` is an ancestor of `origin/main`. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree.
- `2026-09-07` `shipped → verified` — this dashboard flip never fired `continue ENG-044`, so `acceptance-check/SKILL.md` never ran on this ticket individually (unlike every sibling family's children — see `proposals.md`'s 2026-09-07 dashboard-bypass row, addendum (4)). Closed as part of `ENG-026`'s own parent-level closing pass instead: this ticket's own AC slice (PRD AC1 — migration adds all three flags with stated defaults, no regression to `has_order_food`; AC5 — rollout/backfill answered with live-schema evidence, not defaulted) walked directly against the merged migration on `origin/main`, confirmed applied to the live database via `supabase migration list --linked`. Both pass. Full walk: `agents/product-manager/notebook/2026-09-07-eng026-acceptance.md`. `owner` stays `eng-manager`.
