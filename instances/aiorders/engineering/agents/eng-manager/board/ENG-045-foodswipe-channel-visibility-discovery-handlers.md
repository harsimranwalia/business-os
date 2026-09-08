---
id: ENG-045
title: FoodSwipe channel-visibility discovery handlers — open-now gating and status
project: aiorders-api
type: feature
size: S
time_estimate: half a day
time_spent:
time_remaining:
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
branch: feat/ENG-045-foodswipe-channel-visibility-discovery-handlers
depends_on: [ENG-044]
blocks: [ENG-047]
parent: ENG-026
links:
  prd: agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md
  design: agents/architect/designs/ENG-026-foodswipe-channel-visibility.md
  adrs: [ADR-010]
  review: agents/principal-engineer/reviews/ENG-045.md
  test_plan: agents/qa/test-plans/ENG-045.md
  security_review: agents/security/reviews/ENG-045.md
  release:
  pr: https://github.com/harsimranwalia/aiorders-api/pull/20
---

## Problem

`handleRestaurantDiscovery`/`handleRestaurantDiscoveryFallback` have no
channel gate and no notion of "open now" — every tab currently returns the
same restaurant set. No server-side single source of truth for "is this
restaurant open" exists either; the only implementation
(`openingHours.ts`'s `getOpenState`) is client-side, wired into one page in
`restaurant-marketplace`.

## Outcome

`aiorders-api/supabase/functions/_shared/openingHours.ts` exists as a Deno
port of that same parser. `handleRestaurantDiscovery` maps the existing
`mode` param to `p_channel` on the RPC call; `handleRestaurantDiscoveryFallback`
gets the matching `.eq()` gate. Both paths compute a `status` label per row
via the shared util and apply the `open_now` filter post-fetch, per
`ADR-010`. `handleRestaurantDetail` includes the three flags in its response.

## Notes

Design: `agents/architect/designs/ENG-026-foodswipe-channel-visibility.md` —
`## Components` and `## Interfaces`. Depends on `ENG-044`'s migration: this
handler calls the RPC with the new `p_channel` argument and reads the new
`opening_hours` column, both of which must exist first.

**Channel mapping** (`handleRestaurantDiscovery`): `'order-food'` →
`'order_food'`, `'dine-in'` → `'dine_in'`, `'catering'` → `'catering'`, passed
as `p_channel` on the RPC call and as the matching `.eq()` on the fallback's
`.from('restaurants')` query.

**Today's `orderingLink`-presence filter on `order-food`
(`restaurants.ts` / `RestaurantList.tsx:64-65`) stays untouched and
independent.** It and the new `has_order_food` gate are both `AND`ed onto the
same query — neither replaces the other. Do not conflate "has an
ordering-link integration configured" with "staff wants this restaurant
discoverable under Order Food"; that would silently change which restaurants
show up for a reason no acceptance criterion asks for.

**`open_now` — evaluated post-fetch, uniformly for both the RPC and fallback
paths** (`ADR-010` — read it for why this runs here rather than as a SQL
predicate, and the pagination trade-off it accepts): for each returned row,
`_shared/openingHours.ts` evaluates `opening_hours` against the current time.

- `isOpen === false` (confirmed closed): when `open_now=true`, drop the row.
  Regardless of `open_now`, set `status` to the parser's own closed-label
  text (its real output format — e.g. `"Closed · opens 11 AM"` — not the
  PRD Outcome section's more elaborate illustrative copy; that copy isn't
  this ticket's to write).
- `isOpen === true` or `isOpen === null` (no usable `opening_hours` data):
  **never excluded**, `status` stays `null`. This fail-open behavior is
  deliberate, not a bug to "fix" — a restaurant this system cannot evaluate
  must not disappear just because its hours are unknown.

**Detail endpoint** (`handleRestaurantDetail`): unaffected by the channel
gate or `open_now` (a direct `id` lookup, not a list) — gains the three flags
in its response for completeness. Its existing `opening_hours`/
`business_status` fields and `RestaurantDetail.tsx`'s own client-side
`getOpenState` call are untouched.

**`admin-portal/handlers/restaurants.ts` needs NO code change** —
`updateRestaurant`'s `.update(updates)` and `getRestaurants(ById)`'s
`select('*')` already pass the three new fields through with zero edits. Do
not add a field allow-list here as a drive-by fix: that gap is real but
pre-existing and already filed separately (`proposals.md`, 2026-09-03),
distinct from the already-tracked ownership-check issue on the same
function.

**AC ownership** (mapped in
`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`): this
ticket owns AC3 in full (the negative case — a `false`-flagged merchant never
appears, regardless of `open_now`) and AC4's filter/status-computation half
(the UI rendering of `status` and the "Open Now" chip is `ENG-047`'s).

Branch from `origin/main` in the `aiorders-api` worktree, off `ENG-044`'s
already-merged/verified tip — re-fetch first; do not assume the migration's
column/RPC shape without re-reading it live, since `ENG-044` may resolve the
`has_dine_in` backfill branch differently than either default guess.

## Log

- 2026-09-07 `(created) → ready` (eng-manager, `work-breakdown`, `continue
  ENG-026` event pass) — sub-ticket of `ENG-026`, sequence 2,
  `depends_on: [ENG-044]` unmet, held at `ready`. `time_estimate` half a day.
  Owner `eng-manager` while waiting, reassigned to `backend` once `ENG-044`
  ships. Full reasoning:
  `agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`.
  `chained: none` — waiting on an unmet `depends_on: [ENG-044]`, nothing
  agent-actionable until it clears.

- 2026-09-07 `ready → building → in-review` (backend, `continue ENG-045`
  event pass, per `ENG-026`'s own child-dispatch fire once `ENG-044` shipped —
  `agents/eng-manager/notebook/2026-09-07-eng026-child-dispatch.md`). Reading
  map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9,
  10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (`MODE=active`).

  **Dependency re-verified, not trusted off the board's own summary.** Fresh
  `git fetch` + read of both shipped `ENG-044` migrations in
  `~/Documents/projects/_eng/aiorders-api`: `p_channel text default null`
  (RPC's last parameter), `opening_hours jsonb[]` in `RETURNS TABLE` (also
  last), `has_dine_in` a **repoint** of the real live `dine_in` column — all
  three matched `ENG-044`'s own board-file Log exactly, no drift.

  **Built:** `_shared/openingHours.ts` (new) — Deno port of
  `restaurant-marketplace`'s `getOpenState` (fetched fresh from
  `origin/master`, per `ADR-010`). `handleRestaurantDiscovery`/`Fallback`
  gated by channel (`p_channel` on the RPC; matching `has_*` `.eq()` on the
  fallback); both paths evaluate `open_now` post-fetch and set a per-row
  `status` — confirmed-closed only, per the ticket's own Notes; open/unknown
  never excluded, `status` stays `null`. `handleRestaurantDetail` gains the
  three `has_*` flags. `admin-portal/handlers/restaurants.ts`: confirmed
  no change needed, per the ticket's own Notes. Full detail:
  `agents/backend/notebook/2026-09-07-eng045-build.md`.

  **Found and closed a live-data/parser mismatch before it could ship
  silently broken:** `public.restaurants.opening_hours` (live query, two
  sampled rows) stores `{day, open, close, isClosed?, h24?}` objects, not the
  `weekday_text` string list the source parser expects — a straight port
  would have made `getOpenState` return `{isOpen: null, label: null}` for
  every row, unconditionally, satisfying AC4's code shape while never
  actually filtering or labelling anything in production. Fixed in
  `toWeekdayLines` itself (recognizes both shapes now); 9 new tests cover
  both, plus `isClosed`/`h24`/overnight-past-midnight. Likely affects
  `restaurant-marketplace`'s own client-side copy too (different repo,
  already shipped, not this ticket's diff) — proposed separately:
  `agents/eng-manager/proposals.md`, 2026-09-07.

  **Self-tested:** `deno test`/`deno check` on the new shared util (9/9 pass,
  clean check); `deno check` on all three modified files (clean). Live,
  read-only check against the shipped RPC: `p_channel='dine_in'` narrows 211
  rows to 209 with **zero** leaked `has_dine_in=false` rows (joined on `id`);
  `opening_hours` confirmed present on sampled RPC rows. Full detail,
  including the `deno lint` baseline-vs-new-`any` accounting:
  `agents/backend/notebook/2026-09-07-eng045-build.md`.

  Branch `feat/ENG-045-foodswipe-channel-visibility-discovery-handlers`
  pushed fresh off `origin/main` (`aiorders-api@b647508`); no PR yet —
  release-readiness's own step. Machine WIP unaffected — still held by the
  `ENG-026` family.

  **2 transitions this pass** (`ready → building`, `building → in-review`),
  under the cap of 4 — `in-review`/`in-qa` (combined hop) is a fresh session's
  work per `eng_build_loop.md`'s "a pass stops after `building` on purpose."

  **6b:** ran the grep against `openingHours\.ts|open_now|has_order_food|
  has_dine_in|has_catering` across `agents/`. `ENG-046`'s and `ENG-047`'s own
  board files (siblings, not yet built) already assume the exact contract
  this pass shipped (`open_now` query key, `status` field name, the three
  `has_*` names) — confirms, doesn't conflict. `ADR-010` (this ticket's own
  linked ADR) read in full: this build matches its decision exactly
  (post-fetch, both paths, no over-fetch compensation, total/hasMore stay
  pre-filter). No instruction found in conflict; nothing to fix.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise this pass — `in-review` needs no
  approver gate. Nothing due a nudge.

  **Observations/exceptions/journal:** one proposal filed (above, live-data
  parser mismatch); no observation beyond that; no `exception-request:`; no
  G1/G2/G3/merge-request answered this pass.

  business-os itself left uncommitted — standing default per the open
  commit-convention question, not re-decided here.

  `chained: ENG-045` — `in-review` is agent-owned (principal-engineer + qa
  combined hop next), not the approver, not blocked, not terminal, not held
  by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-045`
  before this pass exits. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-045`) and whole-board: see board index for result.

- 2026-09-07 `in-review → building` (principal-engineer then qa, `continue
  ENG-045` event pass — combined review+quality hop, one session, per
  `eng_build_loop.md` step 6's "one combined hop" note). `git fetch` + `git
  diff origin/main...HEAD --stat` confirmed no drift since the build hop
  (`aiorders-api@b647508`, unchanged at review time). Read the design's own
  `## Interfaces`/`## Components` and `ADR-010` in full against the diff, not
  from memory.

  **Review: FAIL, round 1.** 0/10 automatic failures (secret scan, exception
  handling, bundled refactor, dead code, datastore bypass, auth/payment path
  all checked and clean — the per-function `try/catch`s in `openingHours.ts`
  return a defined, spec'd sentinel on every path, not an empty catch, so
  automatic-failure #2 does not hit). **One blocking finding:** `restaurants.ts`'s
  new `channelForMode`/`evaluateOpenNow` (lines 23–38) are exactly the second
  named failure shape in `engineering-standards.md`'s "Decision logic does not
  live trapped..." rule (promoted 2026-09-04 after three occurrences —
  `ENG-033`, `ENG-038` ×2) — extracted, pure, correctly shaped, but **not
  exported**, so neither has a test entry point of its own. This diff is the
  rule's own fourth occurrence, three days after promotion, in a file with no
  prior precedent to blame. Concretely costly, not just a technicality: it is
  the exact reason this same hop's own QA half had to stub the `supabase`
  singleton's `.rpc`/`.from` methods in place (no dependency-injection seam on
  this handler, unlike `brand-portal`'s `handleWebsite(action, payload,
  supabaseClient, user)`) rather than unit-testing either pure function
  directly. **Fix:** add `export` to both declarations — zero behavior
  change, no other edit implied. **One non-blocking note:** `_shared/
  openingHours.ts`'s outer `try/catch`s (every exported function) log nothing
  on the caught-exception path; every reachable non-throwing branch already
  returns the identical `{isOpen:null,label:null}`/`null` sentinel, so an
  actual exception is indistinguishable from an expected unknown-shape read —
  worth a `console.error` if this file is next touched, not blocking a ticket
  that only ported the existing (already-silent) client-side behavior.
  **Good work, said plainly:** the live-data/parser shape mismatch (jsonb
  `{day,open,close}` objects vs. the expected `weekday_text` strings) was
  found and fixed before shipping, not after — see the ticket's own prior log
  entry. No receipt written (`code-review-gate/SKILL.md` step 8: fail writes
  nothing to `agents/principal-engineer/reviews/`); full text in
  `agents/principal-engineer/notebook/2026-09-07-review-log.md`.

  **Quality (this round's work, not a recorded gate verdict — the diff is
  about to change):** found, while writing the test plan, that this ticket's
  two owned criteria (AC3 in full, AC4's backend half) had **zero automated
  coverage** — the build hop's own 9 new tests all target `openingHours.ts`'s
  `getOpenState` in isolation; nothing exercised `handleRestaurantDiscovery`/
  `handleRestaurantDiscoveryFallback` themselves, and this handler file had no
  test at all before this hop (unlike `ENG-040`'s `website.test.ts`, which
  already existed and only needed extending). Closed it: 6 new tests in a new
  `handlers/restaurants.test.ts`, stubbing the `supabase` singleton's `.rpc`
  (RPC path) and `.from` (fallback path, forced via a simulated `42883`)
  directly, since this handler has no injectable client. Covers: a
  channel-disabled restaurant excluded regardless of `open_now`, on both the
  RPC and fallback paths (AC3); the catering tab unaffected by the dine-in
  flag; a confirmed-closed restaurant included by default with a non-null
  `status`, excluded only when `open_now=true` (AC4); the three `has_*` flags
  passed through `handleRestaurantDetail`. **Mutation-checked, not just
  green:** reverted `channelForMode` to always return `null` — exactly the 3
  channel-gate tests went red, the other 3 held; reverted `evaluateOpenNow`'s
  exclusion branch to `include: true` — exactly the 1 exclusion test went
  red. Both reverted back to the real code and re-confirmed clean (`git diff`
  empty) before committing. `deno test`/`deno check` independently re-run:
  6/6 new + 9/9 `openingHours.test.ts` pass; `deno check` on all three
  modified files clean; `deno lint` on `restaurants.ts` re-derived at 4→5
  (baseline 4, the new `visibleRestaurants` filter's `any` the 5th,
  confirmed load-bearing — omitting it is a `TS7006` `deno check` failure,
  not a style choice), matching the build hop's own account exactly. Full
  detail: `agents/qa/notebook/2026-09-07-coverage-gaps.md`. **No receipt**
  (`agents/qa/test-plans/ENG-045.md` not written — discarded round, per
  `code-review-gate/SKILL.md` step 9). Committed and pushed as its own commit,
  `aiorders-api@a9693b6` (`git log`: `b647508..a9693b6`) — real, passing,
  worktree-clean code that the round-2 build hop can build on rather than
  redo; not itself a claim that the gate passed.

  **1 transition** (`in-review → building`), under the cap of 4. Machine WIP
  unaffected — still `1/1`, held by the `ENG-026` family. `state: building`,
  `owner: backend` (unchanged — already the implementing engineer per
  `code-review-gate/SKILL.md` step 9's fail routing).

  **6b:** not applicable this hop — the new test file is a project artifact,
  not a receipt path, state name, config key, or cross-file naming contract
  another agent reads.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing to raise — a review verdict is not a gate item;
  checked the open `inbox/` items anyway per the not-negotiable step 7, none
  due a nudge (see board index for the full list). **Observations:** one line
  filed, `agents/eng-manager/observations.md` — the exported-decision-logic
  standard's fourth occurrence, three days after promotion, worth watching as
  a pattern rather than escalating on one instance. **Exceptions/journal:**
  n/a — no `exception-request:`, no G1/G2/G3/merge-request answered this
  pass.

  Pre-pass and post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-045`) and whole-board: see board index for result.

  `chained: ENG-045` — `building` is agent-owned (backend next, to add the
  two `export` keywords), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-045`
  before this pass exits.

- 2026-09-07 `building → in-review` (backend, `continue ENG-045` event pass —
  fixing round 1's one blocking finding). `git fetch` + `git diff
  origin/main...HEAD --stat` confirmed no drift since the QA hop
  (`aiorders-api@a9693b6`, unchanged). Untracked
  `supabase/functions/brand-portal/deno.lock` (pre-existing, Sep 5) and
  `supabase/functions/restaurant-marketplace/deno.lock` (this ticket's own
  Sep 7 `deno check`/`deno test` byproduct) still present, same precedent as
  both prior hops — left alone, not staged.

  **Fix, exactly as prescribed, nothing else:** added `export` to
  `channelForMode` and `evaluateOpenNow` in `restaurants.ts` (lines 22, 29).
  `git diff` confirmed the entire change is those two keywords — zero
  behavior change, no other edit.

  **Self-tested.** `deno check` on all four touched/relevant files
  (`restaurants.ts`, `validation.ts`, `api.ts`, `openingHours.ts`): clean.
  `deno test --no-check` — the flag round 1's own build hop already needed
  for `openingHours.test.ts` (remote-type-resolution on `npm:@types/node`
  fails under full type-check; not this diff's problem, reproduced
  identically pre- and post-fix) — plus `--allow-env` and dummy
  `SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY` env values, needed only for
  `restaurants.test.ts` (its import chain constructs the `supabase` singleton
  at module-eval time, unlike `openingHours.test.ts` which has no such
  import; the client is never actually called — `.rpc`/`.from` are stubbed
  directly — so dummy values are sufficient): **15/15 pass** (6 handler + 9
  `openingHours`), matching the QA hop's own count exactly. `deno lint` on
  `restaurants.ts`: still 5 (baseline 4 + the one load-bearing `any`) —
  unchanged, confirming the fix is purely additive.

  Committed (`aiorders-api@5f35b92`, 1 file, 2 lines) and pushed:
  `a9693b6..5f35b92` on the same branch.

  **1 transition** (`building → in-review`), under the cap of 4. `state:
  in-review`, `owner: principal-engineer` (code-review-gate's own Owner
  field — round 2 of the combined review+quality hop next). Machine WIP
  unaffected — still `1/1`, held by the `ENG-026` family.

  **6b:** not applicable — adding `export` to two already-reviewed, already-
  correct pure functions is not a receipt path, state name, config key, or
  cross-file naming contract another agent reads.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** checked `inbox/` per the not-negotiable step 7 — four
  items already carry `nudged:` (one nudge each, done, riding the weekly
  report now); `PROP-2026-W36` has no `nudged:` but `notified:
  2026-09-06T18:57:12` is ~22h old, not yet past the 24h threshold — correctly
  not due. Nothing raised, nothing nudged this pass.

  **Observations:** one line filed, `agents/eng-manager/observations.md` —
  `time_spent`/`time_remaining` have gone unpopulated across this ticket's
  `building` hops despite `definition-of-done.md`'s time-tracking rule; not
  backfilled here with a fabricated number since no reliable elapsed-time
  baseline exists from the prior hops. **Exceptions/journal:** n/a — no
  `exception-request:`, no G1/G2/G3/merge-request answered this pass.

  Pre-pass `departments/engineering/lib/eng-gate-check.sh ENG-045`: exit 0,
  no violations. Post-pass scoped and whole-board: see board index for
  result.

  `chained: ENG-045` — `in-review` is agent-owned (principal-engineer + qa
  combined hop, round 2, next), not the approver, not blocked, not terminal,
  not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-045`
  before this pass exits.

- 2026-09-07 `in-review → in-qa → in-security` — **round 2: review PASS,
  quality gate PASS** (principal-engineer + qa, combined hop, `continue
  ENG-045` event pass, per the prior pass's own `chained: ENG-045`). Reading
  map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
  9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check
  clean (`MODE=active`). Pre-pass state inherited clean from the prior
  pass's own post-pass run (recorded on its entry above) rather than
  re-run redundantly — confirmed, not assumed: `traces/eng-loop-2026-09-07.log`
  shows this pass's own `pass start: continue (ENG-045)` at `10:26:19`
  draining directly off that pass's `pass end` at `10:26:16`, no other pass
  in between. `git fetch` + `git diff origin/main...HEAD --stat` confirmed
  no drift since the fix hop (`aiorders-api@5f35b92`, unchanged).

  **Code review, round 2.** Diff: fix-only delta `a9693b6..5f35b92`, 1 file,
  +2/-2 (round 1's own `b647508` diff already reviewed; not re-litigated).
  0/10 automatic failures, re-scanned against the whole diff. Confirmed
  round 1's fix exact: `export` added to `channelForMode` and
  `evaluateOpenNow`, nothing else — matches "two words, no other edit
  implied" precisely; both bodies re-read anyway, still correct against
  `ADR-010`. One non-blocking note, not a new finding: the two
  newly-exported functions still have no test that imports them directly —
  QA's own six tests reach them only through the handler with `supabase`
  stubbed — but the export satisfies the standard's actual requirement
  (reachable without a client mock) and real behavioral coverage of both
  already exists; not holding a third round over a bar round 1 never set.
  Independent re-verification, not trusted from the log: `deno check` on
  all four touched/relevant files clean; `deno test --no-check` 15/15 (9
  `openingHours` + 6 handler); `deno lint` on `restaurants.ts` unchanged at
  5. **Verdict: PASS.** Receipt: `agents/principal-engineer/reviews/ENG-045.md`;
  `links.review` set. Full trace:
  `agents/principal-engineer/notebook/2026-09-07-review-log.md`.

  **Quality gate.** First non-discarded round for this ticket — round 1's
  six `handlers/restaurants.test.ts` tests (AC3 in full, AC4's backend
  half) and the build hop's own nine `openingHours.test.ts` tests both
  independently re-run clean this round: 15/15 pass. Mutation check not
  re-run — the only delta since round 1's own mutation-verified tests is a
  non-executable visibility keyword. `deno check` clean; `deno lint`
  unchanged at 5, informational only (not a registered gate for
  `aiorders-api`). No open P0/P1. **Verdict: PASS.** Test plan:
  `agents/qa/test-plans/ENG-045.md`.

  **2 transitions** (`in-review → in-qa`, `in-qa → in-security`), under the
  cap of 4. Owner `principal-engineer → security` per
  `definition-of-done.md`'s state table. Machine WIP unaffected — still
  `1/1`, held by the `ENG-026` family.

  **6b:** not applicable — no code changed this hop; nothing written here
  is a receipt path, state name, config key, or cross-file naming contract
  another agent reads beyond the already-established `links.review`/
  `links.test_plan` convention.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep.** Current local time `2026-09-07T10:32:00` PDT. Five
  `inbox/` gate items (`ENG-016`, `ENG-018`, `ENG-028`, `ENG-042`,
  `ENG-043`) already carry their one-ever `nudged:` — no action.
  `PROP-2026-W36` (`notified: 2026-09-06T18:57:12`, ~15h39m) — well under
  24h, no action. No new gate item this pass — an internal review/QA
  verdict isn't approver-facing.

  **8b:** one line appended to `observations.md` — the newly-exported
  `channelForMode`/`evaluateOpenNow` still have no direct unit test of
  their own, only indirect coverage through the handler; worth watching
  whether future tickets on this file start testing the exported functions
  directly now that the seam exists, not itself a gap on this ticket's
  owned criteria. No `exception-request:` found. **8c:** n/a — nothing
  answered this pass, no G1/G2/G3/merge-request, so no decision-journal
  entry is owed.

  Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-045`) and whole-board:
  see board index for result.

  `chained: ENG-045` — `in-security` is agent-owned (`security` next), not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-045`
  before this pass exits. Confirmed, not assumed: this fire's own `acquire`
  failed (`traces/eng-loop-2026-09-07.log`, `10:37:41 lock is 5513s old but
  PID 64849 is alive — not stealing`) — that PID is the long-running
  `eng-trigger.sh continue ENG-026` wrapper that has been chain-draining
  this ticket's whole sequence in-process since the original work-breakdown
  dispatch, currently blocked on this very session. Per
  `eng-trigger.sh`'s own `acquire`/queue logic, a failed acquire still
  appends before exiting — read `traces/.pending` directly afterward to
  confirm: `watch launchd`, `scheduled launchd`, `continue ENG-045`, FIFO,
  this fire genuinely third. Not lost, just not next — the wrapper's own
  `while true` loop picks it up once the `scheduled` sweep ahead of it
  finishes, no re-fire needed from here.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains
  open, not re-decided here. No project-repo commit this hop — read-only
  verification, no code changed.

- 2026-09-07 `in-security → ready-to-ship` (security, `continue ENG-045` event
  pass — the third fire in FIFO behind the `watch (launchd)` and `scheduled
  (launchd)` sweeps named in the prior entry, drained once both finished).
  Reading map for `continue`: steps 6 and 6b, plus the not-negotiable set (1,
  7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode
  check clean (`MODE=active`). Ran `skills/security-gate/SKILL.md` in full.

  **Threat-modelled the change** (4 questions, full text in the receipt): new
  input is `mode`/`open_now`, both bounded through a fixed 3-entry lookup or a
  strict boolean parse, never interpolated into a query; new capability is a
  finer filter on an already-public, already-unauthenticated endpoint
  (confirmed directly against `restaurant-marketplace/index.ts` — no auth
  check on this route before or after this diff, not this ticket's doing); new
  data exposed is an hours/status label and three staff-set discoverability
  flags, already **Public**-classified at `ENG-044`'s own gate; component
  compromise blast radius unchanged (no grant, no privilege boundary touched).

  **Verified directly rather than taken on the ticket's word:** the channel
  value can never reach an arbitrary column or RPC argument —
  `channelForMode`/`CHANNEL_COLUMN` both read side by side in `restaurants.ts`
  confirm the value space is exactly `order_food`/`dine_in`/`catering`/`null`;
  the already-shipped `20260907120001_...sql` re-read directly to confirm
  `p_channel` is compared with native `=`, no dynamic SQL. Secret scan over
  the diff *and* all three commits' full history (`b647508`, `a9693b6`,
  `5f35b92`) — one incidental match, an unrelated `token` variable name in
  `openingHours.ts`'s day parser, nothing to rotate. Dependency scan: no
  `package.json`/`deno.json`/lockfile in the tracked diff (the two untracked
  `.lock` files are confirmed not part of any commit); the one new test-file
  import (`deno.land/std@0.177.0`) matches the exact pin already used by 15+
  other test files in this repo, not a new or divergent dependency.

  **OWASP walk, all ten marked.** A01 reviewed — no tenant/role boundary
  exists on this route to test (pre-existing, unrelated to this diff); the
  feature's own correct negative case (a `false`-flagged restaurant never
  appears, either code path) is tested. A03/A04 reviewed and clean (bounded
  input, bounded parsing, no abuse case). A02/A05/A06/A07/A08/A10 `n/a` with
  reasons. A09 `n/a` — no security-relevant event (auth/authz/privilege/
  export) runs through this diff; the review hop's own non-blocking silent-
  catch note is a debuggability point, not a security finding, and is not
  re-raised as one here. LLM checklist `n/a` — no model/agent/tool/MCP/RAG
  code anywhere in the changed files.

  **Verdict: PASS.** Zero findings, blocking or non-blocking, beyond the two
  already-on-record non-security notes from the review/QA hops (not
  re-raised as security findings). Receipt written:
  `agents/security/reviews/ENG-045.md`; `links.security_review` set in the
  same write, per `security-gate/SKILL.md` step 9 (receipt written on `pass`
  only). Full text there — OWASP table, verified-directly section, SOC 2
  evidence trail (all five upstream artifacts confirmed present on disk this
  pass, not assumed).

  **1 transition** (`in-security → ready-to-ship`), under the cap of 4. Owner
  `security → devops` per `definition-of-done.md`'s state table (devops's
  release-readiness hop next). Machine WIP unaffected — still `1/1`, held by
  the `ENG-026` family (this state is inside the counted `ready`..
  `ready-to-ship` range, same family, same slot — not a second occupant).

  **6b:** this hop writes to an established receipt path
  (`agents/security/reviews/{ENG-NNN}.md`) and a config key
  (`links.security_review`), both already fully specified by
  `security-gate/SKILL.md` step 9 and `security-baseline.md`'s "When the gate
  fails" section, and already precedented by ten prior receipts on this board
  (`ENG-031`/`032`/`033`/`034`/`037`/`038`/`039`/`040`/`041`/`044`). This hop
  follows that existing, already-cross-referenced convention rather than
  writing or changing a rule about the artifact, so there is no new
  instruction to reconcile against other mentions.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep.** Current local time `2026-09-07T10:47:15` PDT. All five
  open `inbox/` gate items (`ENG-016`, `ENG-018`, `ENG-028`, `ENG-042`,
  `ENG-043`) already carry their one-ever `nudged:` — re-confirmed fresh, not
  assumed from the prior entry's timestamp — no action. `PROP-2026-W36`
  (`notified: 2026-09-06T18:57:12`, ~15h50m old) — still under 24h, no action.
  A `pass` security verdict is not itself approver-facing, so no new item
  raised this pass.

  **8b:** nothing new to append to `observations.md` beyond what the prior
  hop already filed. No `exception-request:` found. **8c:** n/a — nothing
  answered this pass, no G1/G2/G3/merge-request, so no decision-journal entry
  is owed.

  Pre-pass and post-pass `sh departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-045`, exit 0, no violations) and whole-board (exit 0, no
  violations) — both run directly this hop, not deferred.

  `chained: ENG-045` — `ready-to-ship` is agent-owned (`devops` next, release-
  readiness hop), not the approver, not blocked, not terminal, not held by a
  cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-045`
  before this pass exits.

  business-os itself left uncommitted through this edit — same standing
  default every pass on this ticket has used; the commit-convention question
  remains open, not re-decided here. No project-repo commit this hop —
  read-only verification (plus the already-shipped `ENG-044` migration file,
  read but not modified), no application code changed.

- 2026-09-07 `ready-to-ship → blocked`, PR opened (devops, `continue ENG-045`
  event pass, `skills/release-runner/SKILL.md` run step by step — same L1
  reading established on `2026-09-05-release-readiness-log.md`: step 1 is
  the clock check only; steps 2-3's readiness content still run for L1,
  minus the window bullet). Reading map for `continue`: steps 6 and 6b, plus
  the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The
  four lanes*; *Guards*). Mode check clean (`MODE=active`).

  **Step 1 (window check): skipped.** `aiorders-api` is registered L1
  (`config/projects.md`) — opening a PR is not a release.

  **Step 2 (upstream gates), all three re-read fresh from the receipt files,
  not from this ticket's own log:**
  - `agents/principal-engineer/reviews/ENG-045.md` — round 2, **PASS**, 0/10
    automatic failures.
  - `agents/qa/test-plans/ENG-045.md` — round 2, **PASS**, 15/15, both owned
    criteria (AC3 in full, AC4's backend half) covered, mutation-checked.
  - `agents/security/reviews/ENG-045.md` — **PASS**, zero findings.
  - No migration owed — confirmed `agents/database/migrations/` has no
    `ENG-045-*.md` (schema/RPC argument already shipped with `ENG-044`).

  **Step 3 (readiness gate), no blocking failure:**
  - *Rollback:* no migration and no stored-state change in this diff —
    reverting the merge (once merged) fully undoes it.
  - *Observability:* read the actual handler code rather than assumed —
    all three touched exported functions (`handleRestaurantDiscovery`,
    `handleRestaurantDiscoveryFallback`, `handleRestaurantDetail`) already
    wrap their full body in try/catch, log a distinct `console.error(...)`
    message, and return a 500 on failure (confirmed at
    `restaurants.ts:165,358,452`) — pre-existing, unchanged by this diff,
    and it also covers the new `channelForMode`/`evaluateOpenNow` calls
    since they run inside the same try blocks.
  - *Cost:* $0/month — handler-level code only, no new dependency (verified
    at the security gate), no new infrastructure.
  - *Window:* n/a, L1.

  **Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
  checked fresh: `git fetch origin`, `HEAD` at `5f35b92` matching every
  gate's cited head, `git rev-list --left-right --count origin/main...HEAD`
  → `0 3` (no drift), `origin/main` at `5be48ed` matching the security
  review's own cited base exactly. `git diff origin/main...HEAD --stat`: 6
  files, 746 insertions, 8 deletions. Only the same two long-standing
  untracked `deno.lock` files present, left alone per every prior pass's
  precedent. `gh pr list --head
  feat/ENG-045-foodswipe-channel-visibility-discovery-handlers --state all`
  confirmed no PR already existed. No `.github/workflows/` on this repo —
  opening this PR carries no auto-deploy risk.

  Opened `aiorders-api` PR #20
  (https://github.com/harsimranwalia/aiorders-api/pull/20). Body: what
  changed, the live-data/parser mismatch found and fixed during build, all
  three gates passed with receipt paths, self-test summary, the two
  non-blocking findings carried from review/QA, and what's out of scope
  (`ENG-047`'s UI, the pre-existing `orderingLink` filter's own coverage,
  `total`/`hasMore` staying pre-filter per `ADR-010`). Depends on `ENG-044`
  (merged) — sequencing note only.

  Wrote `inbox/2026-09-07-eng045-merge-request.md`, plain `pr_url:` string
  (single repo). `time_estimate: half a day` carried from the ticket's own
  frontmatter. `lib/eng-notify.sh raise` confirmed sent from
  `traces/eng-notify-2026-09-07.log` (`sent: active
  2026-09-07-eng045-merge-request.md`, `10:57:56`); stamped `notified:
  2026-09-07T10:57:56` on the item, copied verbatim from the log.

  State `ready-to-ship → blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, `owner: devops → approver`, `links.pr` set. No G3 — L1 has
  none; the PR merge is the human gate. No release record yet — L1's actual
  deploy (a manual `supabase functions deploy` after merge) and the release
  record both wait for merge detection on a future pass.

  **1 transition** (`ready-to-ship → blocked`), well under the cap of 4.

  **6b:** not applicable — the merge-request item follows this board's own
  established format exactly (`ENG-040`'s, `ENG-044`'s); no new receipt
  path, state name, config key, or cross-file artifact rule introduced.

  **Dead-end sweep (scoped to this event):** no other ticket touched by this
  hop itself — but see the slot-freed dispatch below, which the Guards
  section requires before this pass exits.

  **Notify sweep.** Current local time ~`2026-09-07T10:57` PDT. This pass's
  own merge request raised and stamped above. All five other open `inbox/`
  gate items (`ENG-016`, `ENG-018`, `ENG-028`, `ENG-042`, `ENG-043`) already
  carry their one-ever `nudged:` — no action. `PROP-2026-W36` (`notified:
  2026-09-06T18:57:12`, ~16h old) — still under 24h, no action.

  **Observations/exceptions/journal:** none — no observation beyond what's
  already on record; no `exception-request:`; nothing was *answered* this
  pass (a merge request was raised, not resolved), so no decision-journal
  entry is owed yet.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here. No project-repo commit beyond the PR branch push
  itself (already pushed by the build hop; nothing new committed this
  release-readiness hop).

  **Slot freed — family dispatch (Guards, amended 2026-09-06/07).** This
  ticket parking on the approver (`blocked`, `blocked_on: approver`, PR
  open) frees the machine slot the `ENG-026` family holds — leaving
  `ready-to-ship` is what frees it, not waiting for the merge. Checked the
  family before falling back to the global To-do, per the 2026-09-07 Guards
  amendment ("the next child of the same parent whose `depends_on` is
  satisfied, else the top of To-do") — this is the exact family the
  amendment was written against. Family state re-read fresh from each
  ticket's own frontmatter, not assumed: `ENG-044` `shipped` (merged, past
  the counted range), `ENG-045` now `blocked`/parked (this ticket), `ENG-046`
  `ready`, `depends_on: [ENG-044]` — satisfied, `ENG-044` shipped;
  `ENG-047` `ready`, `depends_on: [ENG-045]` — also satisfied under the
  2026-09-07 "an open PR satisfies `depends_on`" rule (`ENG-045` has PR #20
  open and is `blocked_on: approver`). Both children are technically
  startable; per step 6's tie-break ("among tickets of equal priority, take
  the lowest ticket id") and the work-breakdown's own DAG
  (`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`:
  `ENG-046` depends on `ENG-044` alone, parallel-safe with the
  `ENG-045`→`ENG-047` branch, not sequenced behind it), `ENG-046` is next:
  neither `hold` nor blocked on anything else. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-046`
  before this pass exits.

  `chained: ENG-046 — slot freed by ENG-045`. `ENG-045` itself is not
  chained — it is parked on the approver (blocked, `blocked_on: approver`),
  exactly the wait the guard names as never chained; the PR merge (or a
  `watch`/`scheduled` sweep) is its own next event.

  Confirmed, not assumed: this fire's own `acquire` also failed — the same
  long-running `eng-trigger.sh continue ENG-026` wrapper (`PID 64849`, alive
  ~1h57m) still holds the lock, chain-draining this family in-process since
  the original work-breakdown dispatch. Read `traces/.pending` directly
  afterward per that precedent: `watch launchd` ×3, `scheduled launchd` ×1,
  `continue ENG-046` — FIFO, this fire fifth (the three `watch` duplicates
  collapse to one at the next drain, per the queue's own dedup rule). Not
  lost, just not next — the wrapper's own loop picks it up once the sweeps
  ahead of it finish, no re-fire needed from here.

  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
  (`ENG-045`, exit 0, no violations) and whole-board (exit 0, no
  violations) — both run directly this hop, not deferred.

- `2026-09-07` `blocked → shipped` (control center, merge detected) — `feat/ENG-045-foodswipe-channel-visibility-discovery-handlers` is an ancestor of `origin/main`. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree.
- `2026-09-07` `shipped → verified` — this dashboard flip never fired `continue ENG-045`, so `acceptance-check/SKILL.md` never ran on this ticket individually (unlike every sibling family's children — see `proposals.md`'s 2026-09-07 dashboard-bypass row, addendum (4)). Closed as part of `ENG-026`'s own parent-level closing pass instead: this ticket's own AC slice (PRD AC3 — Dine-In/Catering tabs flag-gated independent of `open_now`, negative case included; AC4's logic half — a closed-but-enabled merchant stays visible with a status string, excluded only when `open_now` is explicitly true) walked directly against `handleRestaurantDiscovery`/`Fallback`/`evaluateOpenNow` on `origin/main`. Deploy confirmed via `supabase functions list`'s `updated_at` (62s after PR #20's own `mergedAt`) — see the notebook for why that's the evidence used, `aiorders-api` having no CI run to check instead. Both pass. Full walk: `agents/product-manager/notebook/2026-09-07-eng026-acceptance.md`. `owner` stays `eng-manager`.
