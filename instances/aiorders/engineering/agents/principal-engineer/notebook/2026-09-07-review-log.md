# 2026-09-07 — Review log

## ENG-044 (round 1, aiorders-api) — REVIEW pass

Two-file diff, `feat/ENG-044-foodswipe-channel-visibility-schema` (`81350d4`)
vs `origin/main`: `20260907120000_add_channel_visibility_to_restaurants.sql`
(57 lines) and `20260907120001_gate_get_restaurants_optimized_by_channel.sql`
(216 lines). No `.ts`, no frontend, pure DDL/DML plus one function
replacement. **0/10 automatic failures.**

**Independent verification, not taken on the ticket's or the database
agent's own account** — the migration doc
(`agents/database/migrations/ENG-044-foodswipe-channel-visibility-schema.md`)
already carries a thorough disposable-replica test writeup; this round's own
job was to check the claims that writeup makes, the same way `ENG-041`'s
round 2 re-derived a repro by hand rather than trusting "fixed":

1. **Port fidelity, checked byte-for-byte against the real source, not from
   memory.** `restaurant-marketplace`'s own
   `20240302_optimize_restaurant_discovery.sql` was deleted from that repo's
   working tree in `f733e68` (2026-08-23) but still lives in its git history
   — pulled it directly (`git show 2cac687:...`) and diffed manually against
   the ported function in migration 2. Aside from the lowercase-keyword
   convention (documented, matches this repo's post-2026-08-29 style) and
   the two stated additive changes (`p_channel` appended after `p_offset`;
   `opening_hours` appended to `RETURNS TABLE`), the port is exact — every
   CTE, the Haversine calculation, the offer/ordering-link filters,
   ordering, limit/offset, all unchanged.
2. **`DROP FUNCTION IF EXISTS` signature, checked against the true original
   13-arg list**, not against what the new file merely claims to drop:
   `double precision, double precision, text, text[], text[], text[], double
   precision, text, boolean, text, boolean, integer, integer` matches
   `p_lat..p_offset` in order, exactly. This is the line the ticket itself
   flags as "what to review hardest" (the overload-coexistence defect its
   own testing caught) — confirmed the fix actually targets the right
   signature rather than assuming the writeup's own account of it.
3. **Backfill math re-derived independently from the reported counts**, not
   copied: `has_catering`/`has_dine_in` both add at default `false`, so `SET
   has_catering = live_catering WHERE has_catering IS DISTINCT FROM
   live_catering` only touches rows where `live_catering = true` — exactly
   the 7 the migration doc reports, with the other 236 already correct at
   the default and correctly skipped by the guard. Same shape for
   `has_dine_in`/`dine_in` against the reported 241. Self-consistent; the
   guard and the numbers agree.
4. **Style precedents spot-checked against the actual cited files, not
   assumed accurate**: `add column if not exists` + `comment on column`
   confirmed real in `20260807000001_add_heard_about_us_to_catering.sql`;
   the `is distinct from` backfill guard confirmed real in
   `20260903120000_backfill_onboarding_show_in_marketplace.sql` (that file
   uses `GET DIAGNOSTICS ... ROW_COUNT` instead of a re-query count for its
   own single-column backfill — a reasonable adaptation here given this
   migration backfills two columns in one block, not a second, undocumented
   way of doing the same thing). `ADR-003` confirmed to exist under a title
   that matches the citation.
5. **The ticket's own premise — that `restaurant-marketplace`'s
   `supabase/functions/*` is gone, so this RPC's definition is untracked
   anywhere until this migration — checked against that repo's real default
   branch, not the department's local worktree.** The local
   `~/Documents/projects/_eng/restaurant-marketplace` worktree sits on a
   stale `eng/base` branch with no `supabase/functions/` deletion visible,
   which would have been a real problem if taken at face value. Fetched and
   checked `origin/master` (the actual default branch) directly:
   `f733e68` **is** an ancestor of `origin/master`, and `git ls-tree -r
   origin/master -- supabase/functions/` returns nothing. The worktree is
   simply behind (an ancestor of master, not diverged) — not a conflict,
   just stale, and not evidence of anything wrong with this ticket's claim.
6. **Traced the one real caller of this RPC**, rather than trusting
   "backward compatible" from the positional-arg replica test alone:
   `aiorders-api`'s own `supabase/functions/restaurant-marketplace/handlers/
   restaurants.ts` (`handleRestaurantDiscovery`) — the file `ENG-045` will
   build against next, confirmed untouched by this diff. It calls
   `supabase.rpc('get_restaurants_optimized', { p_lat: ..., ... })` with
   **named** parameters, no `p_channel` key. A named-parameter call is
   immune to an appended, defaulted parameter regardless of position — a
   stronger backward-compatibility guarantee than the positional-call test
   already run, and it means today's actual production traffic is
   unaffected by construction, not just by a replica test. The function's
   own fallback path (`handleRestaurantDiscoveryFallback`, triggered only on
   Postgres error `42883`, function-not-found) is never reached by this
   change since `CREATE OR REPLACE` guarantees the function exists
   afterward.
7. **Wider blast radius sanity check**: 30 files across `aiorders-api`
   query or write `restaurants`. Did not open all 30 — additive `NOT NULL`
   columns with defaults can't break an existing `INSERT` (Postgres fills
   the default), and every consumer here is `supabase-js`/PostgREST
   (JSON-keyed responses, not positional tuples), so an unreferenced new
   column is invisible to code that doesn't ask for it. No currently
   deployed `.ts` anywhere in this repo or its siblings references
   `has_order_food`/`has_dine_in`/`has_catering` yet (confirmed by grep) —
   there is nothing live for this migration to have broken, categorically,
   not just in the cases checked.

**Two non-blocking notes, neither promoted:**
- `catering_updated`/`dine_in_updated` in migration 1's closing diagnostic
  block are post-migration **match** counts (`has_catering = live_catering`),
  not literally counts of rows the `UPDATE` changed — the `RAISE NOTICE`
  text itself says "matches ... on % row(s)", which is accurate, so this is
  a variable-naming nit only. One occurrence, not a standard.
- No test (automated or replica) exercises `p_channel` set to a value
  outside `{NULL, 'order_food', 'dine_in', 'catering'}`. Safe by inspection
  — the three-branch `OR`, `AND`-ed together, is false on every branch for
  an unrecognized string, so the query returns zero rows, never an error —
  and it matches how every other free-text parameter on this function
  already behaves (`p_city`, `p_search`, `p_offer_context`: no enum
  validation, no error path, pre-existing). Not a new inconsistency this
  ticket introduces. Handed to QA as a cheap case worth adding once
  `aiorders-api` has any harness to add it to (open proposal,
  `proposals.md`, 2026-08-29).

**Verdict: PASS, round 1.** Receipt: `agents/principal-engineer/reviews/ENG-044.md`.
`links.review` set. Continues to `in-qa` — QA's own gate ran concurrently
on the same diff, see `agents/qa/test-plans/ENG-044.md` and
`agents/qa/notebook/2026-09-07-coverage-gaps.md`.

Ticket-log entry for this hop written under `conventions.yaml`'s
`ticket_log.entry.cap_lines: 20` — this drift is already tracked
(`observations.md`, six occurrences 2026-09-03 through 2026-09-06;
`proposals.md`, 2026-09-04, open) so not re-flagged here, just complied
with.

## ENG-045 (round 1, aiorders-api) — REVIEW pass

Five-file diff, `feat/ENG-045-foodswipe-channel-visibility-discovery-handlers`
(`b647508`) vs `origin/main`: new `_shared/openingHours.ts` (355 lines) +
`openingHours.test.ts` (68 lines), plus `restaurant-marketplace/handlers/
restaurants.ts`, `types/api.ts`, `utils/validation.ts`. **0/10 automatic
failures** — checked #2 closely given how many `try/catch`s the new shared
util carries: every one returns a defined sentinel (`{isOpen:null,label:null}`
or `null`), never an empty catch, so this isn't the automatic-failure shape;
noted separately below as a non-blocking observability gap instead.

**One blocking finding.** `restaurants.ts`'s new `channelForMode`/
`evaluateOpenNow` are small, pure, correctly-shaped extractions out of the
handler body — and then not exported. `engineering-standards.md`'s own
"Decision logic does not live trapped inside a bare request handler... or a
non-exported function with no test entry point" rule names this exact second
shape, not just the first (logic trapped in the handler with no extraction at
all). Promoted 2026-09-04 after three occurrences (`ENG-033`'s
`deriveActionStatus`, `ENG-038`'s `buildBroadcastSmsBody`/
`buildBroadcastEmailBody`) specifically to avoid a mocked-client workaround —
and this hop needed exactly that workaround (stubbing `supabase.rpc`/`.from`
in place, since this handler takes no injectable client, unlike `brand-portal`'s
`handleWebsite`) to reach AC3/AC4 at the quality gate at all. Fourth
occurrence, three days after promotion, in a brand-new file with no prior
debt to excuse it. Fix is two words (`export` on each declaration), zero
behavior risk — failed anyway rather than waved through, since the point of
promoting a standard is that it applies the next time, not just the third
time.

**One non-blocking note.** The new `_shared/openingHours.ts`'s exported
functions each wrap their body in `try/catch { return <sentinel> }` with no
log line on the caught-exception path. Given every already-handled
non-throwing branch (unrecognized shape, empty list, unparseable line)
already returns the identical sentinel, an actual thrown exception is
invisible — indistinguishable from the expected "can't parse this" case,
which is by design silent. Ported unchanged from the client-side original
(same silence there), so not a regression this ticket introduces; worth a
`console.error` the next time this file is touched, not a reason to hold an
otherwise-clean port.

**Good work:** the live-data shape check (`public.restaurants.opening_hours`
sampled directly, found storing `{day,open,close,isClosed?,h24?}` objects
rather than the `weekday_text` strings the ported parser expected) caught a
silent-no-op class of bug before shipping — the exact failure mode AC4 exists
to prevent, found by reading production data rather than trusting the source
file's own docstring.

**Verdict: FAIL, round 1.** No receipt (fail writes nothing, per
`code-review-gate/SKILL.md` step 8). `state: building`, owner `backend`
(unchanged — already the implementing engineer). QA's own gate ran
concurrently on the same diff and found a real, separate coverage gap of its
own — closed rather than merely flagged, see
`agents/qa/notebook/2026-09-07-coverage-gaps.md` — but writes no receipt
either, since this round is discarded and the diff is about to change.

## ENG-045 (round 2, aiorders-api) — REVIEW pass

One-file, two-line diff, `feat/ENG-045-foodswipe-channel-visibility-discovery-handlers`
(`5f35b92`, `a9693b6..5f35b92`) vs the round-1 diff already reviewed above.
**0/10 automatic failures**, re-scanned against the whole diff, not just the
delta.

**Round 1's fix, confirmed exact.** `git diff a9693b6..5f35b92`: `export`
added to `channelForMode` and `evaluateOpenNow` in `restaurants.ts`, nothing
else — matches round 1's own "two words, no other edit implied" precisely.
No new logic to trace; both bodies re-read anyway and remain correct against
`ADR-010`.

**One non-blocking note, not a new finding.** The two newly-exported
functions still have no direct unit test importing them — QA's own six
`restaurants.test.ts` tests (round 1) all reach them indirectly through the
handler with `supabase` stubbed. The export satisfies the standard's actual
requirement (the functions are now reachable without a client mock); real
behavioral coverage of both already exists through the handler tests. Not
holding a third round over a bar round 1 never set for this ticket.

**Independent re-verification, not trusted from the ticket log:** `deno
check` on all four touched/relevant files clean; `deno test --no-check` —
15/15 (9 `openingHours` + 6 handler); `deno lint` on `restaurants.ts` — 5,
unchanged, confirming the fix is purely additive. Full text:
`agents/principal-engineer/reviews/ENG-045.md`.

**Verdict: PASS, round 2.** Receipt: `agents/principal-engineer/reviews/ENG-045.md`.
`links.review` set. Continues to `in-security` — QA's own gate ran
concurrently on the same diff and also passed, its first non-discarded
receipt for this ticket: `agents/qa/test-plans/ENG-045.md`.

## ENG-046 (round 1, aiorders-admin-hub) — REVIEW pass

Two-file diff, `feat/ENG-046-foodswipe-channel-visibility-admin-toggles`
(`a2c51af`) vs `origin/main`: `RestaurantDetails.tsx` (44 lines) +
`types.ts` (1576 lines, generated, regenerated per the design's own
instruction — not hand-edited, confirmed by inspection). No drift. **0/10
automatic failures**, including #7 (unrelated refactor): the large
`types.ts` diff is entirely mechanical schema-drift catch-up from several
unrelated, already-shipped tickets that never regenerated this file, not
authored code.

**Design conformance, checked against `ENG-044`'s own board-file Log, not
assumed:** repoint confirmed correct (`dine_in` real/live/backfilled per
`ENG-044`), two new rows match the six pre-existing rows' exact markup, no
new API call needed (`handleSave` already sends the whole state object,
confirmed by reading it — line ~124 — not taken on the ticket's word; the
GET side already returns all fields too, per `ENG-045`'s own independent
confirmation that `admin-portal`'s handlers need no change).

**Line-level: each of the three rows traced individually** for `id`/
`htmlFor`/`checked`/`onCheckedChange` — all four reference the same field
name, consistently, per row. No cross-wiring from the three-times-copied
block.

**Independent re-verification, not trusted from the build hop's own
account:** `npm run build` clean (same pre-existing chunk-size notice
only); `npx tsc --noEmit -p tsconfig.app.json` — zero errors in either
touched file; `npx eslint` on both files — one warning, the pre-existing,
untouched `react-hooks/exhaustive-deps` at line 81; `types.ts` produces
zero lint output. All three match the notebook's own account exactly.

**One inaccurate citation found in the frontend's own build notebook,
not a code defect.** `agents/frontend/notebook/2026-09-07-eng046-build.md`
cites "the same shape `ENG-040`'s own admin-toggle work used" to justify
skipping a test. Checked both cited tickets directly: `ENG-040` is a
backend `EDITABLE_PAGES` allow-list widening on `aiorders-api`, `ENG-041`
is an FAQ editor — neither is an admin-hub toggle UI, and neither is about
a missing test harness for the reason implied. The underlying judgement
(no test added) is independently correct anyway — `aiorders-admin-hub` has
zero test infrastructure (open proposal, `proposals.md`, 2026-08-31) and
this is a pure prop-through change with no new logic branch, same as the
six sibling rows already in this file. Filed as an observation
(`observations.md`, this date), not a review finding — it's a citation in
a notebook, not a defect in the shipped diff.

**No test added, and none required.** `aiorders-admin-hub` carries zero
test infrastructure (no `test` script, no framework dependency, zero
`*.test.*`/`*.spec.*` files anywhere in `src/` — confirmed fresh this
pass), matching `config/projects.md`'s own empty Test cell for this
project and the open 2026-08-31 proposal. Full reasoning:
`agents/qa/notebook/2026-09-07-coverage-gaps.md`.

**Verdict: PASS, round 1.** Receipt: `agents/principal-engineer/reviews/ENG-046.md`.
`links.review` set. Continues to `in-security` — QA's own gate ran
concurrently on the same diff, also pass:
`agents/qa/test-plans/ENG-046.md`.

## ENG-047 (round 1, restaurant-marketplace) — REVIEW pass

Six-file diff, `feat/ENG-047-foodswipe-open-now-and-channel-display`
(`5dbb76c`) vs `origin/master`: `FilterBar.tsx`, `RestaurantCard.tsx`,
`RestaurantList.tsx`, `useRestaurants.tsx`, `api.ts`, `types/index.ts` (35
insertions, 2 deletions). No drift. **0/10 automatic failures.**

**Wire contract confirmed against `ENG-045`'s actual shipped code, not this
ticket's own Notes**: `aiorders-api`'s `utils/validation.ts` reads
`open_now` (snake_case); `handlers/restaurants.ts` returns `status` on
discovery-list rows only, never the three `has_*` flags (those are
detail-endpoint-only). This diff's `api.ts`/`RestaurantCard.status` match
exactly.

**Design conformance, three claims traced rather than taken on the ticket's
word:** the new chip sits outside the `mode === 'order-food' || 'dine-in'`
gate (all three modes, per design); the tab-reset effect
(`RestaurantList.tsx:213-221`, a merge) and `handleClearFilters` (a full
replacement) both correctly handle `openNow` by *not* naming it, in opposite
directions, exactly matching the design's "not reset on tab change, reset on
Clear All" divergence with zero new code in either function; `RestaurantCard`'s
new `status` clause correctly extends the existing four-field growing-separator
pattern.

**One non-blocking note, confirmed rather than taken on the frontend's own
flagged uncertainty**: `RestaurantCard`'s three new `has_*` fields have zero
producers today (grepped every consumer of the type — none is the detail
page, and `ENG-045`'s discovery/list handlers never populate them). Matches
the design's own explicit Components-row instruction and its "not required
by any AC but natural" framing for the detail endpoint — deliberate
forward-compat, not a slip in either the design or this diff. Not held.

**One inaccuracy found in this same build hop's own proposal filing, not a
code defect**: `proposals.md`'s 2026-09-07 `restaurant-marketplace` lint row
cited `ENG-032`/`ENG-034` as prior diffs on this repo — checked directly,
neither touches `restaurant-marketplace` (`restaurant-portal` and
`config-site-builder` respectively); `ENG-047` is in fact this repo's first
department ticket with a real diff. Corrected in place. **Second occurrence
of this general class** (first: `ENG-046`'s `ENG-040` mischaracterization) —
not yet a third, no standard promoted. Checked whether this round's own reuse
of `ENG-040` as a "thin, no new logic branch" precedent repeats that
inaccuracy: read `ENG-040`'s own ticket file directly — "the handler's
existing per-key loop makes this a pure addition, not a rewrite" — genuinely
accurate this time, not a repeat.

**Independent re-verification:** `npm run typecheck` clean; `npm run build`
clean, 1803 modules, matches the build hop's own account exactly. `npm run
lint` reproduced the identical pre-existing `.eslintrc.cjs:18` syntax error;
confirmed via `git diff origin/master...HEAD -- .eslintrc.cjs` (empty) that
this diff doesn't touch that file. Full text:
`agents/principal-engineer/reviews/ENG-047.md`.

**Verdict: PASS, round 1.** Receipt: `agents/principal-engineer/reviews/ENG-047.md`.
`links.review` set. Continues to `in-security` — QA's own gate ran
concurrently on the same diff, also pass:
`agents/qa/test-plans/ENG-047.md`.

## ENG-048 (round 1, aiorders-api) — REVIEW pass

One-file diff, `feat/ENG-048-loyalty-ledger-schema-credit-function-and-cron`
(`9fccdad`) vs `origin/main`:
`20260907130000_loyalty_ledger_schema_and_credit_function.sql`, 250 lines,
additive only — one new table, two new nullable `orders` columns, one new
function, one new `pg_cron` schedule. **0/10 automatic failures** — #1
(secrets) checked closely given the vault/cron block: `vault.decrypted_secrets`
looked up by name, never a literal value, matching the established
`broadcast-dispatch-tick` precedent byte-for-byte (confirmed below).

**Independent re-verification, not taken on the ticket's or the database
agent's own account** — the migration doc and board-file log already carry a
thorough disposable-replica writeup (rollback run twice, every named branch
queried, both double-credit guards proven); this round's own job was to
check the claims and the parts no replica test exercises:

1. **Cron block confirmed structurally identical to `ADR-018`'s own
   `broadcast-dispatch-tick`, not just cited as such** — diffed directly
   against `20260904140000_broadcast_campaigns.sql:123-136`. Same shape byte
   for byte apart from job name, interval, target URL, and empty body.
2. **The identity walk's load-bearing assumption — `orders.customer_id` IS
   `customers.id`, no join needed — independently traced through real
   application code, not accepted from the migration's own comment.**
   `platform_customer_legacy_links.legacy_customer_id references
   customers(id)` (`20260828120000_platform_customer_identity.sql:27`) and is
   populated from `customers.id` directly (`platform-customer-auth/linking.ts:75`,
   `handler.ts:148`). `orders.customer_id` is populated
   (`cloudwaitress.ts:193,330`) from the CRM's own `create-customer` response,
   which itself inserts into and returns an id from `customers`
   (`crm/customers.ts:335-371`). Both ends independently confirmed to be the
   same id space — this is the single highest-leverage correctness fact in
   the function (AC12), worth tracing rather than trusting.
3. **The rate-as-of-timestamp read confirmed against the real `ENG-007`
   precedent**, not just the design's citation of it:
   `admin-portal/handlers/loyalty-config.ts:101` (`.order('effective_from',
   {ascending:false})` then `history.find(row => row.effective_from <=
   asOfIso)`) is the same "latest row not after the timestamp" semantics as
   the function's `order by effective_from desc limit 1`. `restaurant_loyalty_configs`
   (`20260829130000_...sql`) also enforces strictly-increasing,
   never-backdated `effective_from` per restaurant via an advisory-locked
   trigger — independently confirms the function's read is race-free, not
   just plausible.
4. **`bill.cart`/`bill.discount` unit (dollars) independently re-derived,
   not just corroborated a second time**: the `CloudWaitressOrder` interface
   (`cloudwaitress.ts`) shows `cart`/`discount` as bare `number` fields with
   no `_cents` counterpart, and `createOrder()` stores `bill: orderData.bill`
   unmodified (line 198) — so the SQL's flat `bill->>'cart'` extraction path
   matches the actual stored shape, not a nested one. Same conclusion the
   migration doc reached, reached here independently from the source instead
   of trusting the citation.

**Two blocking findings.**

**B1 — `credit_order_if_eligible` carries no `GRANT`/`REVOKE` at all
(function definition ends line 212, `comment on function` line 214), and
Postgres/Supabase's default leaves a newly-created function executable by
`PUBLIC` unless explicitly restricted.** Checked live against this exact
project rather than assumed (`supabase db query --linked`, `pg_proc`/
`pg_roles`/`has_function_privilege` — system catalogs only, no row data):
`anon`, `authenticated`, and `service_role` **all** currently have `EXECUTE`
on `calculate_platform_analytics` and `get_acquisition_breakdown` — the two
functions in this repo whose own migrations add a `GRANT EXECUTE ... TO
service_role` specifically to look internal-only. That grant is not
restrictive on its own — nothing in this repo's history ever pairs it with a
`REVOKE ... FROM PUBLIC` — so on this live project it's a no-op against
`anon`/`authenticated`, who already have `PUBLIC`'s default. `ENG-048`
doesn't even carry that (insufficient) pattern: zero grant statements.

This function is `security definer`, so it bypasses `orders`' and
`loyalty_ledger_entries`' own RLS internally regardless of who calls it — the
design's own stated model ("every caller is a service-role edge function...
not through RLS keyed to the caller's own JWT") is not actually enforced at
the one place that would enforce it. Concrete, not hypothetical: once this
migration deploys, any already-`authenticated` caller of this live
production project (any diner with a `platform_customers` login — a real,
existing population, per `ENG-006`) can call
`supabase.rpc('credit_order_if_eligible', {p_order_id: <their own known
order id>, p_fulfillment_reason: 'reported'})` directly — no guessing
required, a diner already knows their own order ids — and force an immediate
credit before the restaurant ever reports completion or the 24h window
elapses, or mutate `orders.status`/`loyalty_processed_at` on that order
arbitrarily. This is live from the moment the migration ships, independent
of whether `ENG-049` (the intended-only caller) has been built yet — the
"inert until ENG-049 ships" framing in the migration's own Rollout note is
true for data eligibility, not for this function's own reachability.

Fix: `revoke execute on function public.credit_order_if_eligible(uuid, text)
from public; grant execute on function public.credit_order_if_eligible(uuid,
text) to service_role;` — the revoke is the operative half; copying only
this repo's existing (insufficient) grant-only pattern will not fix it, per
the live check above.

**B2 — `v_amount` (line 197) is not floored at zero, so a boundary input
this ticket's own schema comment explicitly disclaims can reach it through
the *automated* path.** `loyalty_ledger_entries`'s own comment (line 58):
"points is plain numeric rather than positive-only... even though this
ticket only ever writes positive values." If `bill.discount > bill.cart`
(a coupon/promo exceeding the subtotal — not exotic; "flat amount off" is a
common promo shape, and nothing upstream bounds discount by cart), `v_amount`
computes negative, `v_points` (line 198) inherits the sign
(`online_earn_pct` is always `>= 0`, so sign only ever comes from
`v_amount`), and the function returns `credited` with a negative ledger
entry — written by the webhook/sweep path, not the "ticket 5, human
correction" path the comment promises is the only source of a negative row.
`engineering-standards.md`'s own promoted rule ("a comment or doc that
asserts a property the code does not have is a defect... the sentence is
what the author meant") is directly on point — this isn't a nit, the code
and its own adjacent comment disagree.

Fix: `v_amount := greatest(coalesce((v_order.bill->>'cart')::numeric, 0) -
coalesce((v_order.bill->>'discount')::numeric, 0), 0);` — floors the earn
base at zero (a fully-discounted-or-more order earns 0 points, same
treatment as a $0 subtotal) and restores the comment's own invariant. Not
recommending a new return value or an exception — that would change the
function's documented four-outcome contract for a case the design never
separately named, and `greatest()` is a one-line, zero-risk fix consistent
with how the design already treats "still gets marked processed, just
without an entry" elsewhere.

**Two non-blocking notes:**

- Malformed/absent `bill.cart`/`bill.discount` (not merely `discount >
  cart`, but a non-numeric or missing value) raises an uncaught cast error,
  which rolls back the whole statement including the guard `UPDATE` —
  the order stays unprocessed and is retried every tick, forever, with no
  distinct signal. Same *shape* the design already accepts for any per-row
  sweep failure ("a failure on one order leaves it `loyalty_processed_at IS
  NULL`... no special-case recovery logic") — not a new gap this ticket
  introduces, and whether `ENG-049` logs it legibly is that ticket's own
  concern. Named for awareness, not blocking.
- `cloudwaitress.ts:332` already has an unrelated JSON response field named
  `cw_order_id` (`data.cw_order_id`, echoing `webhookData.data.order._id`
  back to the caller — dated 2026-07-07, untouched by this diff). Confirmed
  it's a naming coincidence, not a collision: an HTTP response key, never
  persisted, and this migration's own new `orders.cw_order_id` column is
  unrelated. The design's "never persisted" claim about `orderData._id`
  still holds. Worth knowing so a future `grep cw_order_id` isn't confused
  by two unrelated meanings.

**A systemic version of B1, out of scope for this ticket, filed as a
proposal rather than fixed here:** `calculate_platform_analytics` and
`get_acquisition_breakdown` (both pre-existing, unrelated to `ENG-048`)
share the same root gap — confirmed live, both currently callable by
`anon`/`authenticated` despite each one's own `GRANT ... TO service_role`
looking intentionally restrictive. See `proposals.md`, this date.

**Verdict: FAIL, round 1.** No receipt (fail writes nothing, per
`code-review-gate/SKILL.md` step 8). `state: building`, owner `database`
(unchanged — already the implementing agent). QA's own gate ran concurrently
on the same diff and reached the same two findings through its own
failure-path/AC lens — also discarded, no receipt, see
`agents/qa/notebook/2026-09-07-coverage-gaps.md`. `chained: ENG-048` fired —
`building` is agent-owned, not the approver, not blocked, not terminal.

## ENG-048 (round 2, aiorders-api) — REVIEW pass

`git diff 9fccdad 60fa06e -- supabase/migrations/20260907130000_....sql`
first, before reading anything else — confirms the second commit touches
only two spots: the `v_amount` line (B2) and a new `revoke`/`grant` block
after the function body (B1). Nothing else in the 265-line file moved, so
everything round 1 already cleared (automatic-failure scan, the identity
walk, the rate-as-of-timestamp read, the cron block, the guard clause) needs
no re-review — only regression-checking that neither fix disturbs it.

**Did not accept the database agent's own round-2 writeup on trust, even
though it's unusually thorough** (`agents/database/migrations/ENG-048-....md`,
"Round 2" — a fresh disposable-replica re-test of both fixes, including
catching that round 1's own literal B1 fix text doesn't actually work on this
project). The reason not to: that writeup exists precisely *because* a
"looks correct" fix already failed once on this exact ticket
(`revoke ... from public` read as sufficient, wasn't). Accepting a second
"looks correct, and I tested it" account without re-running it myself would
repeat the same trust failure one level up. Built a fresh container
(`supabase/postgres:15.8.1.073`), a fixture written from scratch (not copied
from the file on disk — six tables, shapes taken from the live-dump numbers
already cited in the migration doc), applied the real migration file
unmodified:

- `has_function_privilege` on `credit_order_if_eligible(uuid,text)`, all four
  roles: `anon → false`, `authenticated → false`, `service_role → true`,
  `postgres → true`. Matches the database agent's own claimed result exactly,
  now independently reproduced rather than read and believed. **B1 confirmed
  closed.**
- Fixture order, `bill = {"cart": 20, "discount": 35}` (the exact `discount >
  cart` boundary the design's own table comment disclaims): `credited`,
  `amount 0.00, points 0.0000`. Floored, not negative. **B2 confirmed
  closed.**
- Repeat call on the same order, other `fulfillment_reason`:
  `already_processed`, ledger count still `1` — the `loyalty_processed_at`
  guard (a different code path from either fix) still holds. No regression.
- Container removed after use.

**Design conformance re-checked on one specific point, not because either fix
touches it, but because it's the kind of ordering assumption a reviewer
should verify rather than inherit:** the cancellation-vs-credit race. Re-read
`agents/architect/designs/ENG-027-....md`'s Approach: cancellation updates
`orders.status` unconditionally and never touches `loyalty_processed_at`, so
(a) a cancellation that commits before any credit attempt is blocked by the
guard (AC5, "credited zero times"), and (b) a cancellation arriving *after* a
credit already committed does not retroactively void it (AC16, correction is
a manual opposite entry, ticket 5). At first read this looked like a possible
tension in AC5's own wording ("a cancellation anywhere in that sequence means
it was credited zero times") — resolved by the design's own explicit
statement that both ACs are true at once by construction, not by this
migration doing anything special. No new finding; worth having checked once,
given this ticket owns only the guard/crediting half of AC5 and the design's
resolution of the two ACs' apparent tension is exactly the kind of thing that
would be easy to take on faith.

**One systemic, pre-existing pattern, checked before filing anywhere:**
`loyalty_ledger_entries`'s own comment claims "append-only, never updated or
deleted," but this migration issues no `REVOKE UPDATE, DELETE` against
`service_role` (which bypasses this project's RLS by default, confirmed on
the replica above — `Bypass RLS` present on `service_role`, absent on
`anon`/`authenticated`), so the claim is enforced by convention only, not by
the schema. Checked whether this is a new gap or an existing one before
deciding how to route it: `create_influencer_notes.sql` makes the identical
"append-only" claim with the identical (non-)enforcement — a real, repo-wide
pattern, not something this ticket introduces or makes worse. Filing it as a
finding that blocks *this* ticket alone would itself be the "second way to do
what the project already does" failure mode this role's own standards warn
against — matching precedent (round 1's own systemic B1-sibling on
`calculate_platform_analytics`/`get_acquisition_breakdown` went to
`proposals.md`, not a fix). Filed there, this date, rather than fixed here or
silently dropped.

**Verdict: PASS, round 2.** Receipt: `agents/principal-engineer/reviews/ENG-048.md`.
`links.review` set. Continues to `in-qa` — QA's own gate ran concurrently on
the same diff, see `agents/qa/test-plans/ENG-048.md` and
`agents/qa/notebook/2026-09-07-coverage-gaps.md`.

## ENG-049 (round 1, aiorders-api) — REVIEW pass

Stacked-PR diff, `feat/ENG-049-...` (`4cd02f5`, `b72ce33`) vs `feat/ENG-048-...`
(re-confirmed `OPEN` via `gh pr view 21` before diffing against it, not
assumed from the ticket's own account) — 12 files, 1260/-31. **0/10 automatic
failures.**

**Method: re-derive, don't read-and-believe — same discipline `ENG-048`
round 2 used one hop ago, and for the same reason (a "looks correct" account
already failed once today).** Every claim in this ticket's own board-log that
was checkable was checked, not paraphrased:

- Read `external-integrations/index.ts` in full rather than trusting "the
  other four handlers unaffected" — confirmed the explicit re-export (lines
  73-74) actually covers the three siblings that still import from
  `../index.ts` (grepped for the import, not assumed).
- Ran all three new test files myself, in the same per-function-directory
  shape the ticket used: 8/8, 10/10, 19/19. `deno check`'s 4 errors
  independently traced to two pre-existing locations — pulled the *base*
  (`ENG-048` branch) copy of `cloudwaitress.ts` via `git show` and confirmed
  the untyped outer `catch` is already there, unchanged, at the tail of the
  345-line pre-ticket file. Not inferred from an error-count diff; read both
  copies.
- Cross-read `crm/utils.ts`'s `normalizePhone` against the new
  `normalizePhoneForIdentity` line by line — the claimed "local copy" is
  faithful (one legitimate branch-collapse, one dropped null-guard that's
  safe given both call sites already guard before calling it).
- Grepped for the migration comment ENG-049's own Notes quote
  ("Dine-in earn... does not call this function") to confirm it's a real
  citation, not a paraphrase drifting from the source.
- Read `ENG-048`'s `orders_loyalty_sweep_idx` `create index` statement
  directly and compared it column-by-column against `selectEligibleOrders`'s
  own `.not()/.is()/.neq()/.lte()` chain — genuine match, including
  confirming the one disclosed gap (`.neq()` vs. `IS DISTINCT FROM` on a
  null `status`) is theoretical given `CloudWaitressOrder.status: string`
  and `createOrder()`'s own pre-existing, unconditional read of it.
- Diffed `authorizeServiceRole` against `broadcast-dispatch/auth.ts`'s own
  copy byte-for-byte — identical, confirming the "local copy per ADR-015"
  claim rather than accepting the docstring's citation on its face.

**One design-language finding, chased to a real (if pre-existing) gap
instead of stopping at "the code does what the design says."** The design's
own AC17 text — "the same 403-shaped error every other brand-portal action
already returns" — reads at first as a spec the code should meet literally.
Grepped `403` across the whole `brand-portal` directory before accepting
either way: appears exactly once, at `index.ts:100`, for an unrelated
API-key-scope check. Every `requireRestaurantAccess` failure across all six
actions that call it (five pre-existing, plus this ticket's own) throws into
the same top-level `catch` and comes back as HTTP `500`. So "403-shaped" was
always describing "whatever the existing convention already does," per the
design's own words, not promising an actual `403` — the code matches its
design instruction exactly, and the design's own label is what's slightly
off. Systemic and repo-wide, not introduced by this ticket, not fixable for
one action alone without creating a second convention — filed as a proposal
rather than a blocking finding, same reasoning `ENG-048`'s own round-2 entry
above used for the append-only-table gap.

**One test-naming nit, preference not blocking.** `loyalty.test.ts`'s
7-value `INVALID_AMOUNTS` parameterisation labels each case with
`JSON.stringify(amount)`; `NaN`/`Infinity`/`null` all stringify to `"null"`,
so three of seven test names print identically even though each is a
distinct, independently-failing assertion (confirmed by reading the array
and the `assertRejects` call, not just the test-runner output). `String()`
instead of `JSON.stringify()` would disambiguate all three at no cost. Noted
in the receipt; not worth a round.

**Verdict: PASS, round 1.** Receipt: `agents/principal-engineer/reviews/ENG-049.md`.
`links.review` set. Continues to `in-security` — QA's own gate ran
concurrently on the same diff, see `agents/qa/test-plans/ENG-049.md`.

## ENG-049 (round 2, aiorders-api) — REVIEW pass, on the security-gate fix

Security gate round 1 found one critical finding (unauthenticated
CloudWaitress webhook — a live financial-fraud path, sweep credits real
loyalty points against a forged order 24h15m later) and sent the ticket to
`building`. The fix hop routed to `in-review` rather than straight to
`in-security` — same shape as `ENG-038`'s own round-5→round-6 precedent, a
gate finding fixed outside this reviewer's own round, reviewed fresh rather
than assumed. Scope: `0bec87c` only (2 files, 165/3), stacked on `ENG-048`'s
still-`OPEN` PR #21, re-confirmed live via `gh pr view 21` rather than
carried over from round 1's account.

**0/10 automatic failures**, re-scanned fresh. Full detail:
`agents/principal-engineer/reviews/ENG-049.md`.

**Read the fix against the finding's own requirement, not just against
green tests.** The finding specified "before any branching on
`webhookData.event`" precisely because a narrower gate (terminal events
only) would leave `order_new` — the actual fabrication path — open. Read
`handleCloudWaitress` directly: `verifyCloudWaitressSecret` sits
immediately after `request.json()`, strictly before structural validation,
the terminal-event branch, and the `order_new` branch. All three covered.
Fails closed (`if (!expected || !provided) return false`) — an unset env
var never matches an equally-missing webhook secret, confirmed by the
dedicated test rather than by reading the line alone.

**Unprompted standards conformance worth recording.** `verifyCloudWaitressSecret`
is exported as a pure function (webhook data in, boolean out, no client
inside it) — matches the "decision logic doesn't live trapped inside a bare
handler" rule (promoted 2026-09-04, three prior occurrences) exactly,
without anyone asking for it this round. Logs the denial (`event` name only)
without ever logging the secret or the expected value — satisfies the
observability standard's "no secrets in log lines" the same way.

**Independently re-ran all three suites, not accepted on the fix's own
count**: `cloudwaitress.test.ts` 16/16 (was 8/8 — 8 new), `sweep.test.ts`
10/10, `loyalty.test.ts` 19/19 — 45/45. `deno check` on the touched files:
same 4 pre-existing errors at the same three lines (447/448/451,
`kitchenhub-auth.ts:92`), compared line-for-line against round 1's own
baseline rather than just the count — zero new.

**Test shape check, not just the pass count.** The exploit-chain test
(`rejects order_new with no configured secret ... before ever touching
supabase`) asserts `tableCalls.length === 0` and `rpcCalls.length === 0`
alongside the `401`, which is the property the finding actually needed — an
unauthenticated caller can't get partway through order creation either, not
just "gets rejected eventually." A second rejection test covers a terminal
event with a wrong secret, closing the one gap a narrower fix would have
left. Two positive tests (a correctly-signed ignored event, a
correctly-signed terminal event reaching `credit_order_if_eligible` with the
same RPC args round 1 already asserted) prove the gate doesn't reject
legitimate traffic — without these a green suite would be equally
consistent with an over-broad fix.

Two non-blocking findings carried forward unchanged from round 1 (test-name
collision in `loyalty.test.ts`; the AC17 "403-shaped" design-language
mismatch, already a proposal) — neither file touched this round, so neither
re-verified fresh.

**Verdict: PASS, round 2.** Receipt: `agents/principal-engineer/reviews/ENG-049.md`
(`round: 2`). `links.review` re-set. Continues to `in-security` — QA's own
gate re-check ran concurrently on the same diff, see
`agents/qa/test-plans/ENG-049.md`.
