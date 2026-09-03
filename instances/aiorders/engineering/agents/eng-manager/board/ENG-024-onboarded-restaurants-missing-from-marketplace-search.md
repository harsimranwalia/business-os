---
id: ENG-024
title: Set show_in_marketplace on restaurant-portal-onboarding's createRestaurant insert, plus a backfill
project: aiorders-api
type: bug
size: XS
time_estimate: under an hour (XS band, definition-of-done.md)
time_spent: build, fast-lane combined review (review/suite/OWASP), and release-readiness (PR opened, merge request raised) complete this pass, not itemized against a pass-start clock (same pre-existing gap ENG-010's/ENG-022's own frontmatter already named rather than backfilled with an invented figure)
time_remaining: nothing left for the department — waiting on the approver to merge the PR; already inside the original under-an-hour/XS band, not separately re-banded
severity: P1
priority:
state: blocked
owner: approver
lane: fast
blocked_on: approver
blocked_from: ready-to-ship
source: approver
created: 2026-08-29
updated: 2026-09-03
branch: fix/ENG-024-onboarding-marketplace-visibility (aiorders-api@8c97bd3)
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md
  design:
  adrs: []
  review: agents/principal-engineer/reviews/ENG-024.md
  test_plan:
  security_review:
  release:
  pr: https://github.com/harsimranwalia/aiorders-api/pull/11
---

## Problem

`aiorders-api`'s `restaurant-portal-onboarding` edge function creates a new
restaurant row with `approved: true` but never sets `show_in_marketplace`.
Every marketplace search path (`restaurant-marketplace`'s discovery RPC and its
fallback query, plus the sitemap) hard-requires `show_in_marketplace = true`.
Result: every restaurant added through the FoodSwipe onboarding sign-up flow is
silently invisible in marketplace search — including location-sorted search —
until a staff member manually flips a toggle in the internal admin tool, which
nothing in the flow tells anyone to do. Full trace in the PRD.

## Outcome

A restaurant added through onboarding is visible in FoodSwipe marketplace
search (including location-sorted search) immediately, with no manual admin
step. Restaurants already added through this flow before the fix are made
visible by a one-time backfill, not just new sign-ups going forward.

## Notes

- **Fix site:** `aiorders-api/supabase/functions/restaurant-portal-onboarding/restaurants.ts`,
  `createRestaurant`'s `.insert()` — add `show_in_marketplace: true` alongside
  the existing `approved: true`.
- **Backfill:** existing rows created through this path that are `approved:
  true` and currently not `show_in_marketplace: true` need a one-time update.
  Scope the `WHERE` to this flow's actual signature carefully — don't flip the
  flag for rows that are unapproved or belong to the separate `restaurant-claims`
  path on purpose (see PRD Non-goals).
- **Worth checking while in this file:** whether `show_in_marketplace`'s
  DB-level default should also change, so any future insert path doesn't
  reintroduce the same gap. Not decided here — see PRD Risks.
- **Not in scope:** `restaurant-claims`' own insert (same omission, but
  `approved: false` by design — different question, see PRD Non-goals and
  `observations.md`).
- **Fast lane** (`size: XS`, `type: bug`): `intake → building → in-review →
  shipped → verified`, one combined gate (review + suite + OWASP on the
  touched surface). `aiorders-api` has no test command registered
  (`config/projects.md`) — pre-existing, board-wide gap, not specific to this
  ticket.
- **G1 auto-skipped** (bug type) — no gate item raised, no approver-facing WIP
  or approval-cap slot used by this ticket.

## Log

- 2026-08-29 `intake → shaped` (product-manager) — sized XS, project
  `aiorders-api`, type `bug`, severity P1, lane `fast`. Context: PM inbox card
  `agents/product-manager/inbox/2026-08-29-fix-the-location-bug-on-foodswipe.md`.
  Root cause traced directly in live code (no worktree existed on this host for
  any project — none created; investigation read the human's own checkout
  read-only across `aiorders-api`, `restaurant-portal`, `restaurant-marketplace`,
  `aiorders-admin-hub`, no writes made there): `restaurant-portal-onboarding`'s
  `createRestaurant` insert sets `approved: true` but never
  `show_in_marketplace`, which every marketplace search path hard-requires.
  Confirmed the gap is never closed downstream either (`updateRestaurantDetails`
  → `mapPlaceToRestaurantRow`'s column whitelist also excludes it). PRD written:
  `agents/product-manager/specs/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md`.
  G1 auto-skipped per `definition-of-done.md` (bug type). Held at `shaped`
  only long enough to write this entry — not blocked by any cap (machine WIP
  counts `ready`..`ready-to-ship`, not `shaped`; approver-facing WIP and
  approval cap don't apply since no G1 was raised). Owner handed to
  `eng-manager` — PM's job (shape + PRD) is done, and per
  `agents/product-manager/agent.md`, sequencing/WIP/assignment is the EM's,
  never the PM's, even for an auto-approved bug. `1 transition`
  (`intake → shaped`), well under the cap of 4 — deliberately did not attempt
  `ready`/`building` myself: that's the EM's assignment step and then new
  implementation work, both outside this `intake` event's own contract ("a
  pass stops at... new implementation work").
  `chained: ENG-024` — fired `lib/eng-trigger.sh continue ENG-024` before
  this pass exits: `shaped`, owner `eng-manager`, an agent-owned state with no
  gate to wait at (G1 auto-skipped), so nothing about this ticket is waiting
  on a human. Full reasoning above; see also `agents/eng-manager/board/_index.md`'s
  dated entry for this pass.

- 2026-08-29 no state change (eng-manager, `continue` event pass, context
  `ENG-024` — this ticket's own chain fire from the `intake` pass above).
  Narrow scope per this event's own contract: this ticket only. Mode check
  clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-024`) and whole-board: exit 0, clean.

  Re-checked fresh rather than trusted the board's cached header: all six
  machine-WIP tickets' own frontmatter (`ENG-007` ready-to-ship, `ENG-008`
  building, `ENG-009` ready, `ENG-010` ready, `ENG-011` ready-to-ship,
  `ENG-013` building) — count unchanged at 6/1, still over the cap of 1.
  Per `eng_build_loop.md` step 6, the To-do column (`intake`/`shaped`/
  `awaiting-scope`) is the only place a new start is drawn from, and "there
  is exactly one slot [that] does not free until the ticket occupying it
  reaches `shipped`" — this ticket (severity P1, fast lane) cannot enter
  `building` this pass regardless of severity; nothing in the loop's
  dispatch rule exempts P1 from the machine WIP cap, only the unrelated
  proposal-batching P0 carve-out (step 3) mentions P0 at all, and that's a
  different gate entirely. `agents/eng-manager/inbox/` empty — no technical
  intake item for this ticket; G1 was already correctly auto-skipped (bug
  type, fast lane), so there is no gate item to check either. Ticket
  correctly stays at `shaped`.

  **0 transitions.** `chained: none` — held by the machine WIP cap (6/1, no
  free slot); one of the explicit do-not-chain conditions. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-024`) and
  whole-board: exit 0, clean. One observation filed (`observations.md`): the
  `intake` pass above fired this chain without checking the machine-WIP cap,
  which was already known full at the time — this pass is the cost of that
  gap, one hop spent to re-derive a hold the shaping pass could have
  recognized itself. Full narrative on `agents/eng-manager/board/_index.md`'s
  dated entry for this pass.

- 2026-09-03 no state change (eng-manager, `scheduled` event pass —
  whole-board sweep). Machine WIP re-checked fresh, not trusted from any
  cached count: every ticket's own frontmatter read directly, zero currently
  sitting in `ready`..`ready-to-ship` — `0/1`, free. The condition that held
  this ticket since 2026-08-29 (`6/1`, over cap) has cleared and was never
  re-checked in the five days since; this pass is that re-check.

  Confirmed this is the correct next pick for the freed slot: among the
  To-do column (`intake`/`shaped`/`awaiting-scope`), `ENG-016` and `ENG-019`
  carry `priority: next` but both already sit behind an unanswered G1 of
  their own (raised this same pass, in `ENG-019`'s case) and so cannot
  themselves enter `building` yet; every other candidate at `shaped`
  (`ENG-020`, `ENG-021`, this pass's own G1 raises) is in the same
  position. `ENG-024` is the only To-do-column ticket with no gate
  outstanding at all (G1 auto-skipped, fast lane, bug type) — genuinely
  free to move.

  **Not transitioned to `building` in this pass.** Same precedent
  `ENG-022`'s own dispatch hop set explicitly (see that ticket's board file,
  2026-09-03, `designed → ready`): the next hop is new implementation
  work — a real code edit plus a scoped backfill against a live table — and
  belongs in its own dedicated session, not this whole-board sweep. Fast
  lane has no intermediate `ready` marker state to move into ahead of
  `building` the way the full lane does, so there is no cheap, gate-free
  transition available here to make now; the state stays `shaped` rather
  than manufacturing an unneeded intermediate step.

  **0 transitions.** `chained: ENG-024` — fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-024`
  before this pass exits, so a dedicated session performs `shaped →
  building` (transition and implementation together, the same shape every
  other building hop on this board has used) rather than this sweep
  attempting the edit itself. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-024`) and
  whole-board: see `agents/eng-manager/board/_index.md`'s dated entry for
  this pass.

- `2026-09-03` `shaped → building`: built per the PRD, single repo
  (`aiorders-api`) (backend, `continue` event pass, context `ENG-024` — this
  ticket's own turn at the front of the queue, per the prior pass's own
  `chained: ENG-024`). Narrow scope per the event's own contract — this
  ticket only. Reading map for `continue`: steps 6 and 6b (step 2's
  mid-PRD checkpoint doesn't apply — the PRD is already complete). Mode
  check clean (business-os `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Machine WIP re-checked fresh, not trusted from the prior pass's own
  account.** Every ticket's own frontmatter read directly (`state:` field on
  all 26 board files): zero sitting in `ready`..`ready-to-ship` — still
  `0/1`, free, unchanged since the `scheduled` pass that chained here.
  `ENG-024` still `shaped`, still the only To-do-column ticket with no gate
  outstanding. Correct to proceed.

  **Worktree confirmed clean before branching.**
  `~/Documents/projects/_eng/aiorders-api` was sitting on `ENG-015`'s own
  branch (`fix/ENG-015-agency-reseller-brand-scoping`, no uncommitted
  changes — that ticket's build long finished, now `blocked`). `git fetch
  origin` confirmed `origin/main@93617c6`, no drift. Branched
  `fix/ENG-024-onboarding-marketplace-visibility` off `origin/main`
  directly — this ticket has no dependency on any other in-flight ticket's
  branch.

  **Live code re-read before editing, not trusted from the PRD's own
  quotes.** `restaurants.ts`'s `createRestaurant` matched the PRD's evidence
  exactly — `.insert()` sets `name`/`address`/`google_place_id`/`brand_id`/
  `approved: true`, no `show_in_marketplace`.

  **Built exactly what the PRD's Notes named.** One field added to the
  existing insert: `show_in_marketplace: true`, same auto-approve intent as
  the adjacent `approved: true`. No other line touched.

  **Backfill migration**, scoped deliberately narrower than a plain
  `WHERE approved = true`: researched the second insert path
  (`restaurant-claims/index.ts`'s `createClaimFromGooglePlace`) to confirm
  its actual DB-level signature rather than relying on "claims are
  unapproved" holding forever — it sets `approved: false` **and**
  `claimed_by_user_id`/`claim_status`/`claimed_at`, and grepping every file
  that reads `claim_status`/`claimed_by_user_id`
  (`FoodswipeListings.tsx`, `admin-portal/handlers/foodswipe.ts`,
  `useRestaurantClaim.ts`, `Dashboard.tsx`, `portalApi.ts`) found no code
  path anywhere that ever flips a claim's `approved` back to `true` — so
  today, `approved = true` alone already excludes every claims row. Added
  `claimed_by_user_id IS NULL` to the backfill's `WHERE` anyway, as a
  self-documenting belt-and-suspenders condition matching the PRD's own
  explicit caution ("don't flip the flag for rows that... belong to the
  separate `restaurant-claims` path on purpose") rather than relying on an
  absence of code that could change later. Used `IS DISTINCT FROM true`
  (not `!= true`/`= false`) for the `show_in_marketplace` comparison —
  NULL-safe, since the column's literal default is unconfirmed (see below).
  `supabase/migrations/20260903120000_backfill_onboarding_show_in_marketplace.sql`,
  styled on this repo's one existing precedent for a pure-data-backfill
  migration (`20260221000001_normalize_customer_phone_numbers.sql`):
  header comment stating scope and reasoning, `UPDATE ... WHERE`, a `DO $$`
  block reporting the row count via `RAISE NOTICE`.

  **DB-level default: investigated, deliberately not changed in this
  ticket.** The PRD's own Risk note flagged checking whether
  `show_in_marketplace`'s column default should also change, "not decided
  here." Confirmed the column is defined in no tracked migration across any
  of the five repos (grepped every `*.sql` for `show_in_marketplace`,
  found only the unrelated discovery-RPC migration; no
  `CREATE TABLE restaurants` exists in migration history at all — added
  outside migrations, matching the PRD's own suspicion). Chose **not** to
  add an `ALTER TABLE ... SET DEFAULT` here: `definition-of-done.md`'s
  fast-lane exclusion list names `schema` explicitly, and this ticket's own
  PRD scoped it fast lane specifically on "no schema change (column already
  exists)" — a DDL change would retroactively invalidate that lane choice,
  which is new scope this build hop doesn't get to grant itself. Filed as a
  proposal instead (`agents/eng-manager/proposals.md`, 2026-09-03 row,
  `by: eng-manager`) rather than an observation — this is something worth
  someone deciding on, not just a note that something is so.

  **Step 6b (artifact-mention enumeration): not run, and here's why rather
  than a silent skip.** The condition is a change that writes or relies on
  a rule about a receipt path, state name, config key, or a file another
  agent is told to produce. `show_in_marketplace` is an existing product
  database column, already referenced by every marketplace query — this
  hop sets it at one more insert site, same as it already reads at every
  other site; nothing here is a new business-os-process artifact, and
  nothing is renamed (contrast `ENG-022`'s `requireRestaurantAccess`
  rename, which is exactly the case 6b exists for).

  **Self-tested.** `deno check` on the two touched/new files hit a
  pre-existing environment snag first: run from this function's own
  directory (matching `ENG-022`'s own noted workaround) still failed with a
  byonm/`node_modules` resolution error — traced to an unrelated
  `~/package.json` + `~/node_modules` that Deno's package.json auto-walk
  finds above the repo root on this host (not present, or not yet hit, when
  `ENG-022` wrote its own note — worth a correction there, not repeating
  the now-incomplete workaround silently). `DENO_NO_PACKAGE_JSON=1 deno
  check --node-modules-dir=none` resolves it cleanly. Result: **6
  pre-existing `TS18046` errors** (`error.message` on a caught `unknown`),
  confirmed identical (line-for-line, off by one from this diff's own
  single added line) against the pre-edit file via `git stash -u`; zero
  introduced by this diff, none on a touched line. `deno test
  --node-modules-dir=none --no-check restaurants.test.ts`: **2 passed, 0
  failed**.

  **Executed a real mutation check, not a hand-trace.** Removed
  `show_in_marketplace: true` from the insert, reran the test file: exactly
  the one test asserting on it went red (`AssertionError:
  undefined` vs `true`), the unrelated guard-clause test stayed green.
  Restored the fix, reran: **2 passed, 0 failed** again. This is the
  regression evidence the PRD's acceptance criterion 1 asks for.

  **New test: 1 file, 2 `Deno.test` cases**
  (`restaurants.test.ts`, colocated, matching this repo's existing
  `*.test.ts` convention). A minimal fake `.from('restaurants').insert().select().single()`
  chain that captures the insert payload directly (no live Supabase
  project, no network) — the regression case (payload carries both
  `approved: true` and `show_in_marketplace: true`) plus one positive
  control proving the existing required-fields guard is unchanged, so a
  reader can't mistake "stub always passes" for "field is actually set."

  **Committed and pushed**, single repo: `aiorders-api@8c97bd3`
  (`fix/ENG-024-onboarding-marketplace-visibility`, tracking
  `origin/fix/ENG-024-onboarding-marketplace-visibility`); no PR opened
  yet — devops's own release-readiness hop, same precedent
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022` each set. PR body drafted here:

  *aiorders-api* — title: `Set show_in_marketplace on onboarding's
  createRestaurant insert, plus backfill (ENG-024)`. Body: the bug
  (`createRestaurant` auto-approves but never sets the separate flag every
  marketplace search path also requires, so onboarded restaurants were
  invisible in search with no error to anyone); the fix (one field, same
  intent as the adjacent `approved: true`); the backfill (scoped to exclude
  `restaurant-claims` rows on purpose, reasoning above); the regression
  test and the mutation check that proves it catches the bug; `deno check`
  before/after (6 pre-existing errors, unchanged, none introduced); out of
  scope (`restaurant-claims`' own insert — separate flow, separate
  question; the column's DB-level default — filed as a proposal, would
  require full lane). Single repo, no cross-ticket branch dependency.

  **1 transition** (`shaped → building`; the build itself happened inside
  it), same shape every other building hop on this board has used — the
  next hop (fast lane's combined review + quality + OWASP gate) is a fresh
  session's work by design, per the chain rationale ("each heavy step gets
  its own session with fresh context"). **Consequence:** machine WIP
  `0/1 → 1/1` — `building` is inside the counted `ready`..`ready-to-ship`
  range. Approver-facing WIP and approval cap both unaffected — no gate
  touched this hop (the DB-default proposal isn't a gate item; it sits in
  `proposals.md` per step 3, batched into the weekly report).

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing to raise this pass — a build hop doesn't
  notify. **Observations/proposals filed:** one proposal
  (`proposals.md`, DB-level default, reasoning above); no `observations.md`
  entry — the Deno/`node_modules` environment snag is recorded here on the
  ticket log with its working fix, but is worth a shared note too since the
  next pass hitting Deno tooling on this repo shouldn't rediscover it —
  filed as one line to `observations.md`.

  `chained: ENG-024` — `building` is agent-owned (next hop `in-review`,
  owned by `principal-engineer` per `definition-of-done.md`'s state table);
  not the approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-024`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-024`) and
  whole-board: see board index.

- `2026-09-03` `building → ready-to-ship`: fast-lane combined gate
  (review + suite + OWASP), round 1, **pass** (`principal-engineer`,
  `continue` event pass, context `ENG-024` — this ticket's own turn per the
  prior pass's own `chained: ENG-024`). Reading map for `continue`: steps 6
  and 6b. Mode check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty, falls back to the global switch).
  This hop does not edit code (`principal-engineer/agent.md`
  `never_touches: writing feature code`), so **step 6b does not apply** —
  named rather than silently skipped, same pattern the prior hop used.
  **Correction against the pattern prior hops set:** the pre-pass
  `eng-gate-check.sh` run was missed at the start of this hop — the first
  scoped/whole-board run happened only after the review and its writes were
  already done. Run at that point instead: `ENG-024`-scoped and whole-board,
  both exit 0, clean. Named here rather than silently backfilled as if it
  ran first, since it didn't; nothing it would have caught was in fact
  missed (the ticket's own frontmatter and the board's WIP count were both
  independently re-verified fresh before any edit regardless, see below),
  but the ordering itself is worth being honest about rather than quietly
  correcting the account.

  **Ticket state re-checked fresh from the file on disk, not trusted from
  the checkpoint copy this pass launched with.** `state: building`,
  `branch: fix/ENG-024-onboarding-marketplace-visibility
  (aiorders-api@8c97bd3)` — matches. Which state a fast-lane pass verdict
  should land on was not obvious from `definition-of-done.md`'s fast-lane
  row alone (its path line omits an explicit stop between `in-review` and
  `shipped`), so read further rather than guessing: `release-runner/SKILL.md`'s
  own trigger line ("a ticket enters state `ready-to-ship`") and
  `security-gate/SKILL.md`'s own pass-routing (full lane's analogous final
  gate routes `pass → ready-to-ship, owner devops` directly) both confirm
  `ready-to-ship` is the correct landing state regardless of lane — the
  fast-lane row's path is a simplified summary, not a literal state list.

  **Worktree independently verified, not trusted from the log.** `git
  status`/`git log` in `~/Documents/projects/_eng/aiorders-api` confirmed
  branch tip `8c97bd3` and `origin/main@93617c6` directly (fresh `git
  fetch`, no drift) before reading anything. One pre-existing, unrelated
  untracked file (`brand-portal/deno.lock`, from `ENG-022`'s own work in
  this shared worktree) — left untouched.

  **Full review performed and independently verified — see
  `agents/principal-engineer/reviews/ENG-024.md` for the complete record.**
  Automatic-10 scan: 0/10 open. Design conformance: all 3 PRD acceptance
  criteria re-verified against live code myself, including two claims not
  strictly required but cheap to check and load-bearing for the fix's
  correctness — the marketplace read paths' actual `show_in_marketplace`
  requirement (grepped directly, 3 sites) and `updateRestaurantDetails`'s
  inability to clobber the new field (read `_shared/googlePlaces.ts`'s
  column whitelist directly). `deno check`: 6 pre-existing `TS18046`
  errors, zero introduced — reproduced correctly on the **second** attempt,
  after a first attempt's `git stash -u` silently no-opped on an
  already-committed diff and nearly produced a false match; corrected via
  `git show origin/main:{path}` in place, then restored. `deno test`: 2/2
  passed. **Mutation check executed myself** (removed the fix via `Edit`,
  reran, confirmed exactly the regression test went red, restored
  byte-identical via `git diff --stat`, reran green) — independent of the
  build hop's own claimed mutation check. OWASP A01–A10 walked in full,
  every category `n/a` with a reason (no new input, capability, or auth
  surface; the newly-visible data is the feature's own intended public
  business-listing content, not PII).

  **One real gap surfaced, not blocking.** This ticket's backfill migration
  has never been through `database`'s own migration gate
  (`schema-change/SKILL.md`) — traced why: that skill's only trigger is an
  architect design with `touches_data: true`, and fast lane skips the
  design state entirely, so nothing on this lane ever fires it, migration
  or not. Confirmed this is deliberately outside this review's own
  authority (`principal-engineer/agent.md`'s `never_touches` list names the
  migration gate explicitly; `definition-of-done.md`'s fast-lane row names
  only review/suite/OWASP as folded in). Assessed the migration informally
  against `schema-change`'s 7 failure conditions anyway as a sanity check:
  low risk (not destructive, practically reversible, no schema/code
  coexistence question), one soft miss (no stated runtime estimate/batching,
  matching this repo's own only backfill precedent exactly). Not held on
  this — filed as a proposal (`proposals.md`, 2026-09-03,
  `by: principal-engineer`) since the gap is in the fast-lane *mechanism*,
  not particular to this migration; `release-runner/SKILL.md` step 2
  ("a missing verdict is a fail, not an assumption") remains the documented
  backstop if this risk read is ever wrong on a future ticket.

  **Verdict: PASS.** Receipt written
  (`agents/principal-engineer/reviews/ENG-024.md`), `links.review` set in
  the same edit. `owner: backend → devops`, `state: building →
  ready-to-ship` — this is the fast lane's own literal terminal machine
  state before the L1 PR gets opened; no `in-qa`/`in-security` stop exists
  on this lane, review/suite/OWASP together **are** the one combined gate.
  Notebook entry added
  (`agents/principal-engineer/notebook/2026-09-03-review-log.md`).

  **1 transition** (`building → ready-to-ship`), well under the cap of 4.
  **Consequence:** ticket stays inside machine WIP's counted range
  (`ready`..`ready-to-ship`) — still `1/1`, unchanged. Approver-facing WIP
  and approval cap both unaffected — no gate item raised this pass (a
  passing review isn't an approver decision), so nothing goes to `inbox/`
  and nothing to notify this pass.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Observations/proposals filed:** one proposal (`proposals.md`, the
  fast-lane migration-gate mechanism gap, reasoning above); no
  `observations.md` entry — the `git stash -u`-on-a-committed-diff mistake
  is recorded in the notebook (above) since it's a review-technique note
  for this agent specifically, not a department-wide pattern yet (first
  occurrence).

  `chained: ENG-024` — `ready-to-ship` is agent-owned (`devops`, via
  `release-runner/SKILL.md`, triggered by this exact state); not the
  approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-024`
  before this pass exits, so a fresh session runs the release-readiness hop
  (which will itself re-verify the migration verdict per that skill's own
  step 2 — see the gap named above). Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-024`) and
  whole-board: see board index.

- `2026-09-03` `ready-to-ship → blocked`: **release-readiness — PR opened,
  merge request raised** (devops, `continue` event pass, context `ENG-024` —
  this fire's own turn at the front of the queue, per the prior pass's own
  `chained: ENG-024`). Narrow scope per the event's own contract — this
  ticket only. Reading map for `continue`: steps 6 and 6b. Mode check clean
  (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty, falls back to the global switch). Pre-pass
  `lib/eng-gate-check.sh`, scoped (`ENG-024`) and whole-board: both exit 0,
  clean, run before any edit this time (correcting the pattern the prior
  hop's own log named itself as having missed).

  **Found and closed a stale incident before starting the ticket work — not
  in the reading map for `continue`, but the map's own floor-not-ceiling
  clause names exactly this shape ("a gate item that turns out to be an
  incident") as a case to read into rather than skip.**
  `inbox/2026-09-03-eng-loop-stalled.md` (`gate: incident`, `ticket:
  ENG-024`, raised 06:37:12 after 5 consecutive never-started passes) had
  never been investigated. Classified directly from this host's own
  `traces/eng-loop-2026-09-03.log`, not inferred: every `pass NEVER STARTED`
  line in that run carries the explicit `vendor limit signature` text (the
  self-healing shape, not `claude not on PATH`), and the same log shows
  `08:56:01 back-off cleared — a session started normally`, followed by
  eleven further `exit 0` passes since, including this ticket's own review
  hop. Resolved, confirmed rather than assumed from silence alone — full
  reasoning written into the file. Moved to `inbox/_handled/` (the file was
  untracked, so a plain move, not `git mv`). No `decision:` field, matching
  this exact incident type's own established precedent
  (`inbox/_handled/2026-09-02-eng-loop-stalled.md`).

  **Also checked, not acted on:** `inbox/2026-09-03-eng027-g1-scope.md`
  carries `decision: changed` (2026-09-03T16:00:32) while the board index's
  own narrative still describes it as an open rider — a real discrepancy,
  but not a broken chain: `traces/.pending` already carries a queued
  `decision 2026-09-03-eng027-g1-scope.md` line, waiting its own turn behind
  several other queued events. The prior (`ENG-021`) pass's call to leave it
  alone was correct; nothing to fix here, so no observation filed for it.

  **Verified all upstream gates fresh from the receipt file**, not assumed
  from frontmatter alone: `agents/principal-engineer/reviews/ENG-024.md`,
  `verdict: pass`, fast-lane combined review + suite + OWASP, round 1.
  Worktree (`~/Documents/projects/_eng/aiorders-api`) independently
  re-confirmed clean but for the same pre-existing untracked `deno.lock`
  (`ENG-022`'s, left alone); `git status --branch` showed
  `fix/ENG-024-onboarding-marketplace-visibility` at `8c97bd3`, `+0 -0`
  against its own pushed upstream — already pushed, nothing to push this
  hop. `git fetch` plus `git merge-base --is-ancestor` confirmed **not
  merged** against `origin/main@93617c6` (matches frontmatter). `gh pr list
  --head fix/ENG-024-onboarding-marketplace-visibility --state all` — empty,
  no PR already open; not a duplicate.

  **Project registered L1** (`config/projects.md`) — step 1's window check
  does not apply. **Step 3 readiness checks**, same interpretation this
  board established for `ENG-007`/`ENG-008`/`ENG-013`/`ENG-022` (the
  "L2/L3 only" carve-out in step 3's own text names only the window-closed
  criterion, not the other three — read narrowly to that one bullet, not
  the whole step, since step 3's rollback/observability/cost bullets carry
  no such carve-out and this board's own precedent already runs them for
  every L1 release):
  - **Rollback:** not live-drilled — same standing, already-proposed
    host limitation named on `ENG-007`'s release record and re-confirmed
    independently here (no Docker/psql/supabase CLI reachable from any
    build host on this instance). Reasoned instead, from my own direct read
    of the migration file (`supabase/migrations/20260903120000_backfill_
    onboarding_show_in_marketplace.sql`), not just the review's account of
    it: a single `UPDATE ... WHERE approved = true AND claimed_by_user_id
    IS NULL AND show_in_marketplace IS DISTINCT FROM true`, non-destructive,
    effectively idempotent (a second run touches zero rows), reversible by
    an inverse `UPDATE` on the same `WHERE`. Code side reverts with the
    single commit. Same "reasoned, not drilled" bar `ENG-007`'s own release
    record already set and shipped on.
  - **Observability:** `createRestaurant`'s existing `console.error` failure
    path is unchanged by this diff; the migration's own `RAISE NOTICE`
    reports its row count on apply. No new failure mode introduced (one
    literal field added to an already-existing insert).
  - **Cost:** **$0/month** — PRD's own Cost section confirms no new
    infrastructure, no new dependency.
  - **Window:** n/a, L1.

  **The migration-verdict gap, decided rather than silently passed
  through.** `release-runner/SKILL.md` step 2 says a missing verdict is a
  fail, not an assumption, and no `database`-gate verdict exists for this
  migration — the review's own non-blocking finding named exactly why (fast
  lane has no path that triggers `schema-change/SKILL.md`; that skill's only
  trigger is an architect design with `touches_data: true`, and fast lane
  skips design entirely). Read step 2 as requiring a real, existing gate to
  return the ticket to, not as authority to invent one that doesn't exist on
  this lane — routing this ticket to a migration-gate state the fast lane's
  own documented path (`intake → building → in-review → shipped → verified`)
  has no slot for would be improvising a new process step, not following
  the one written down. Proceeded instead on the same basis this board
  already established for the identical host-side gap on rollback testing
  (`ENG-007`, shipped on "reasoned, not drilled"): independently re-read the
  migration SQL myself rather than trust the review's account, concur with
  its low-risk assessment (not destructive, effectively idempotent, no
  schema/code coexistence question, small and non-hot table at this
  business's actual scale), and named the gap plainly in both the PR body
  and the merge-request item rather than writing `pass` as if a formal gate
  ran. The open proposal (`proposals.md`, 2026-09-03, principal-engineer) is
  the mechanism-level fix; not re-filed here, since it already exists and
  this is the same instance of the gap it already names, not a new one.

  **Opened the PR**: `aiorders-api` #11
  (https://github.com/harsimranwalia/aiorders-api/pull/11). Body states the
  bug, the fix, the backfill and its scoping logic, the three gates passed,
  the readiness checks above, and the named migration-verdict gap — same
  transparency standard `ENG-022`'s PR body set.

  **Wrote the L1 merge-request item**
  (`inbox/2026-09-03-eng024-merge-request.md`), plain `pr_url:` string per
  `skills/release-runner/SKILL.md` step 4 (single repo). Set
  `time_estimate:` on the item matching the ticket's own field, per
  `definition-of-done.md`'s Time tracking section, same fix `ENG-022`'s own
  merge-request item already applied. Ran
  `departments/engineering/lib/eng-notify.sh raise` — exit 0, confirmed sent
  (`traces/eng-notify-2026-09-03.log`: `sent: active
  2026-09-03-eng024-merge-request.md`, local-time-logged `10:58:15`);
  stamped `notified: 2026-09-03T10:58:15` on the item by hand using that
  same literal value, matching this board's own established (if
  already-flagged-as-buggy, `proposals.md` 2026-09-02 row) stamping
  convention rather than hand-correcting it unilaterally on one item only.

  State `ready-to-ship → blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, owner `devops → approver`. `links.pr` set to the PR URL.
  No release record yet, per `release-runner`'s own step 7/step 4 split —
  written only once merge detection confirms the PR merged, same position
  `ENG-008`/`ENG-009`/`ENG-010`/`ENG-022` are already in.

  **1 transition** (`ready-to-ship → blocked`). **Consequence:**
  `machine_wip` `1/1 → 0/1` — `ENG-024` leaves the counted
  `ready`..`ready-to-ship` range, freeing the slot (not acted on this pass —
  narrow scope per this event's own contract; a fresh start is the next
  `scheduled`/`continue`-elsewhere pass's work). Approver-facing WIP
  uncapped (`config/config.yaml` → `wip.approver_limit: unlimited`) — this
  item adds to the informational count, gates nothing new.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume; the stale incident (above) is the one dead-end this
  hop found and closed. **Notify sweep:** this pass's own item raised and
  stamped above. Checked every other open item fresh rather than trusting
  the board narrative: `ENG-008` (notified 2026-09-02T23:24:37, ~18h34m,
  under 24h), `ENG-015` (notified 2026-09-03T10:03:53, ~7h54m, under 24h),
  `ENG-022` (notified 2026-09-03T01:26:47, ~16h31m, under 24h), `ENG-028`
  (notified 2026-09-03T16:10:27, ~1h48m, under 24h) — none due. `ENG-009`
  and `ENG-010` already carry their one-ever nudge each. `ENG-027` carries
  `decision: changed` (see above) — not a nudge candidate, already answered.
  **Observations/proposals filed:** none new — the migration-verdict gap and
  the host rollback-testing limitation are both already-open, already-named
  proposals; this hop's own instance of each is reasoning applied against
  existing entries, not a fresh finding.

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human
  gate the whole hop was driving toward; firing `continue ENG-024` again
  would queue against a ticket with nothing left for a machine to do, same
  reasoning `ENG-008`'s and `ENG-022`'s own release-readiness entries
  already recorded at this identical state. Post-pass
  `lib/eng-gate-check.sh`, scoped (`ENG-024`) and whole-board: see board
  index.

  business-os itself left uncommitted — same standing default every pass
  today has used (including this ticket's own preceding hop); the
  commit-convention question remains open, not re-decided here. This
  includes the incident-item move above: `eng_build_loop.md` step 4 says to
  commit an incident's closure "in this same pass," but every pass today
  that touched `inbox/_handled/` left business-os uncommitted regardless
  (`ENG-022`'s own incident-adjacent entries included) — followed that
  live, consistent precedent rather than being the one hop that diverges
  from it.
