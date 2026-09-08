# Coverage gaps — 2026-09-07

## ENG-044 — a live RPC changed, not an inert one, and that changes what "no suite" is allowed to mean

`aiorders-api` has no test harness (no `package.json`, no `deno.json` — open
proposal, `proposals.md`, 2026-08-29), so the mechanical result here is the
same as every prior migration-only ticket on this project: `no suite`, not a
pass or a fail. What's different from the closest precedent (`ENG-031`, also
aiorders-api, also migration-only) is that `ENG-031`'s diff was genuinely
inert — zero application code reachable it yet, confirmed by grep, deferred
entirely to a future ticket. `ENG-044` changes `get_restaurants_optimized`, a
function with a real, live, currently-called caller today. "No suite" cannot
mean "nothing to check" here the way it correctly did for `ENG-031` — it
means the checking has to happen by inspection and by tracing the one real
caller, not by running anything.

Traced `handlers/restaurants.ts`'s `handleRestaurantDiscovery` (the file
`ENG-045` builds against next) rather than trusting the migration doc's own
"backward compatible" claim: it calls the RPC with named parameters, doesn't
send `p_channel`, and isn't touched by this diff. A named-parameter call
without the new key receives the function's own `DEFAULT NULL` regardless of
argument position — which sidesteps the positional-argument question the
database agent's own replica test was built around, and is a strictly
stronger compatibility guarantee than what was tested. Recorded in the plan's
own Acceptance coverage row for AC1 rather than left as a review-only
finding, since this is exactly the kind of "seam between two agents' work"
this role exists to check.

**One real coverage gap, closed by inspection rather than by test, and named
rather than silently accepted:** no case (replica or otherwise) exercises
`p_channel` outside `{NULL, 'order_food', 'dine_in', 'catering'}`. Verified
by inspection that this is safe (three `OR` branches, all false on an
unrecognized string, zero rows returned, no error path) and that it isn't a
new gap this ticket introduces — every other free-text parameter on this
function (`p_city`, `p_search`, `p_offer_context`) has always worked this
way, unvalidated, and none of them are enum-shaped either. Not blocking:
there is nothing to add this test *to* until `aiorders-api` has a harness
(same open proposal). Worth remembering as the first item on that harness's
own list, not re-filed as a second proposal.

**Not filed as a new proposal or observation on its own** — both the missing
harness and this specific function's now-larger blast radius are already
visible from the open harness proposal and this ticket's own record; a
second note would fragment tracking rather than add information.

Full acceptance-coverage table and result: `agents/qa/test-plans/ENG-044.md`.

## ENG-045 — a handler with zero prior tests, and the two owned ACs had none either

Unlike `ENG-040`'s `website.test.ts` (existing harness, extended), `restaurant-
marketplace/handlers/restaurants.ts` had no test file at all before this hop.
The build hop's own 9 new tests are all against `_shared/openingHours.ts`'s
`getOpenState` in isolation — real, and independently re-run clean this
round, but they prove the parser works, not that the handler wires it in
correctly. Neither AC3 (channel gate, owned in full) nor AC4's backend half
(open_now, owned in part) had a test that could fail if the wiring regressed
— the ticket's own build note offers a live, read-only RPC check
(`p_channel='dine_in'` narrowing 211→209 rows) as evidence, which is real but
manual, and "manually verified" for something automation can reach is exactly
what this role refuses to sign off on.

**Closed it, not just flagged it.** `handlers/restaurants.test.ts` (new, 6
tests): the RPC path's channel gate (stubbing `get_restaurants_optimized` to
apply the same `p_channel`/`has_*` predicate the live function documents, so
a wrong mode→channel mapping shows up here the same way it would against the
real function); the fallback path's own independent `.eq()` gate (forced via
a simulated `42883`); the open_now include/exclude boundary using
all-`h24`/all-`isClosed` fixtures so the assertion doesn't depend on which
day or hour the suite happens to run; and the three `has_*` flags reaching
`handleRestaurantDetail`'s response. No dependency-injection seam exists on
this handler (`supabase` is imported as a singleton, not passed in, unlike
`brand-portal`'s `handleWebsite`) — stubbed `.rpc`/`.from` on the singleton
directly, save-and-restore around each test, the same shape principle as
`website.test.ts`'s injected fake but forced into place rather than passed
in. Flagged to review as the finding it actually is: the two functions this
gap centers on, `channelForMode`/`evaluateOpenNow`, are exactly the kind of
decision logic `engineering-standards.md` says should be extracted **and
exported** for direct testing — they're extracted, not exported, which is
why a client-stub was necessary here at all.

**Mutation-checked, both directions.** Reverted `channelForMode` to always
return `null`: the 3 tests that assert on channel exclusion went red, the
other 3 (catering-tab, both open_now, detail) held. Reverted
`evaluateOpenNow`'s `include: openNow !== true` to `include: true`
unconditionally: exactly the 1 test asserting the exclusion boundary went
red, the inclusion-by-default test held. Both reverted to the real code
before committing; `git diff` confirmed empty.

**`deno lint` re-derived independently, not trusted from the backend
notebook:** baseline (`origin/main`) `restaurants.ts` carries 4
`no-explicit-any` hits; this diff's 5th (`visibleRestaurants.map`) confirmed
load-bearing by testing the alternative first — dropping the annotation is a
`TS7006` `deno check` **failure**, not a lint-only warning, because the RPC
result's inferred type isn't bare `any`. Matches the build hop's own account
exactly (4→5).

**Verdict: this round is discarded, not a recorded pass.** Review failed
(round 1, see `agents/principal-engineer/notebook/2026-09-07-review-log.md`)
on an unrelated finding in the same diff, so per `code-review-gate/SKILL.md`
step 9 no `agents/qa/test-plans/ENG-045.md` receipt is written this round —
the diff is about to change (two `export` keywords) and re-reviewing a
verdict against code that's already different would be worthless. The test
file itself is real, passing, and committed (`aiorders-api@a9693b6`) — round
2 builds on it rather than redoing it, same asymmetry
`ENG-040`'s own write-path test drew between "the verdict is provisional" and
"the artifact is not."

## ENG-046 — a genuinely test-infrastructure-free repo, and confirming that rather than assuming it

`aiorders-admin-hub`'s missing test harness is already a tracked, open
proposal (`proposals.md`, 2026-08-31) — re-confirmed fresh this pass rather
than cited from memory: no `test` script or test-framework dependency in
`package.json`, zero `*.test.*`/`*.spec.*` files anywhere under `src/`,
`config/projects.md`'s Commands table carries an empty Test cell for this
project. Unlike `ENG-045` (a handler with no test file but a live `deno
test` runtime available to write one into), there is no harness here to add
a test *to* at all — the 2026-08-31 proposal's own scope (installing
`vitest` + `@testing-library/react`) is exactly the missing piece, and it is
still open.

**This ticket's own diff is a pure prop-through UI change** — three Switch/
Badge rows bound directly to state fields, no computed value, no
conditional beyond the same binary-toggle pattern the six pre-existing rows
in this same card already use, none of which have a test either. So the gap
here isn't a new hole this ticket opens; it's the same, already-proposed
repo-wide gap, applied to one more row in a file that already had eight
untested ones.

**Coverage confirmed by inspection instead:** traced all three rows'
`id`/`checked`/`onCheckedChange`/`htmlFor` individually against the diff —
each references its own field consistently, no crossed wiring from the
copy-pasted block (the actual failure mode a test would exist to catch
here). Confirmed the read (`admin-portal`'s `getRestaurantById`,
`select('*')`) and write (`updateRestaurant`, whole-object `PUT`) paths both
already pass all three fields through with zero backend change — cross-
checked against `ENG-045`'s own board-file Log rather than re-derived, since
that ticket already confirmed this exact handler needs no edit.

**Also checked, not assumed: whether the repointed `dine_in` field is read
anywhere else in the repo.** One hit outside `has_dine_in`:
`RestaurantAIWebsite.tsx:802`'s `conditions.location.dine_in` — read
directly, a CSV-menu-import feature's per-dish availability flag, unrelated
domain concept, not this table or this ticket's local `Restaurant`
interface. Not a regression.

**Not filed as a new proposal** — the 2026-08-31 one already covers this
exact gap for this exact project; a second entry would fragment tracking,
not add information.

**Verdict: pass.** No suite exists, none is required (see above), the one
owned criterion (AC2) is covered by inspection against the actual diff, no
bug filed. Full acceptance-coverage table: `agents/qa/test-plans/ENG-046.md`.

## ENG-047 — a fourth test-infrastructure-free repo, and the first one with no proposal already open for it

`restaurant-marketplace` has the identical shape to `ENG-044`'s/`ENG-045`'s/
`ENG-046`'s own projects — confirmed fresh: `config/projects.md`'s Commands
table carries an empty `Test` cell (only Lint/Typecheck/Build are
registered), no `test` script or test-framework dependency in
`package.json`, zero `*.test.*`/`*.spec.*` files anywhere under `src/`. **The
difference from all three siblings: nobody had filed the proposal for this
project yet.** `aiorders-admin-hub` (2026-08-31), `aiorders-api`
(2026-09-03), and `config-site-builder` (2026-09-04) all already have one;
`restaurant-marketplace` — a registered L1 project carrying real, currently
serving traffic — did not, until this pass. Filed: `proposals.md`,
2026-09-07.

**This ticket's own diff is thinner than the sibling that triggered
`config-site-builder`'s proposal** (`ENG-034`'s "largest single piece of new
logic" framing doesn't apply here) **but isn't the pure prop-through
boilerplate `ENG-046`'s toggle rows were either** — `RestaurantCard.tsx`'s
new `status` clause is a real conditional (a fourth OR'd separator check),
the kind of thing a copy-paste mutation could silently break. Coverage
confirmed by inspection instead: traced the clause against the three
pre-existing separator checks it extends and found the pattern applied
consistently (see `agents/principal-engineer/reviews/ENG-047.md` for the
full trace); traced `filters.openNow`'s default (unset/falsy everywhere it's
initialized) to confirm the chip is genuinely default-off, matching AC4's
own "explicit, user-initiated... default off" language.

**Also checked, not assumed: whether the tab-reset and Clear-All effects
this ticket depends on actually do what its own build notebook claims.**
Read both directly — `RestaurantList.tsx`'s tab-change effect is a merge
that never names `openNow` (correctly leaves it alone across tabs);
`handleClearFilters` is a full-replacement literal that also never names it
(correctly zeroes it on Clear All). Both already correct before this
ticket's diff touched either function — confirmed rather than taken on the
notebook's word, since a wrong claim here would have meant a real,
user-visible regression risk (a filter that doesn't clear, or a filter that
resets when it shouldn't) shipping on an unverified assertion.

**One inaccuracy found in this same build hop's own proposal filing** — not
this ticket's acceptance coverage, but adjacent enough to record here rather
than only in the review: the 2026-09-07 lint-config proposal row this same
build hop filed cited `ENG-032`/`ENG-034` as prior `restaurant-marketplace`
diffs; neither ticket touches this repo. Corrected in place
(`proposals.md`); full reasoning in
`agents/principal-engineer/reviews/ENG-047.md`.

**Verdict: pass.** No suite exists, none is required (see above), the one
owned criterion (AC4's UI half) is covered by inspection against the actual
diff, no bug filed. Full acceptance-coverage table:
`agents/qa/test-plans/ENG-047.md`.

## ENG-048 — round discarded on a code-review fail, but this gate's own two lenses (unauthorised caller, boundary input) independently landed on the same root causes

`aiorders-api` has no test harness (open proposal, 2026-08-29), so the
mechanical result would again be `no suite`, not a pass or a fail — moot
this round since code review failed on the same diff and this round is
discarded regardless (`code-review-gate/SKILL.md` step 9: "QA writes no
receipt for a discarded round either"). Ran the acceptance-coverage and
failure-path passes anyway, on this ticket's own owned criteria, since the
next round needs to know whether the fix closes everything or only what
principal-engineer named.

**Acceptance coverage (AC4, AC5, AC8, AC9, AC12 — this ticket's full-owned
set):** all five hold up under inspection plus the disposable-replica
evidence already on file (`agents/database/migrations/ENG-048-....md`) —
AC12 specifically re-traced independently this round (see the review log's
own point 2) rather than accepted, since it's the one criterion a wrong
`customer_id`/`customers.id` assumption would silently break for every
online order, not just an edge case.

**Failure paths — this gate's own explicit charter includes "unauthorised
caller" (`agents/qa/agent.md`, "How you test") and "invalid input at the
boundary," and both produced a real finding, not a clean pass:**

| Scenario | Expected behaviour | Result |
|---|---|---|
| Direct RPC call bypassing the webhook/sweep (`supabase.rpc('credit_order_if_eligible', ...)` from an `authenticated` or `anon` client) | Rejected — design's own model is service-role-only | **Fails.** No `GRANT`/`REVOKE` on the function at all; confirmed live (system-catalog query, no row data) that this project's `PUBLIC` default leaves comparable functions executable by `anon`/`authenticated` regardless of an intended-restrictive `GRANT ... TO service_role`. Same finding as review's B1 — an unauthorised caller isn't merely untested here, the control itself is missing. |
| `bill.discount > bill.cart` (over-discounted order) | Some defined, non-negative outcome | **Fails.** No floor at zero; produces a negative `points`/`amount` row through the automated path. Same finding as review's B1→B2 numbering, review's own B2. |
| Cancelled order, credit attempted | Blocked, zero ledger rows, `already_processed` | Pass — disposable-replica evidence on file, independently re-derived from the guard clause's own `IS DISTINCT FROM` semantics against a null status. |
| Two concurrent callers (webhook + sweep) on the same order | Exactly one credit, no double-write | Pass — single-row `UPDATE ... WHERE loyalty_processed_at IS NULL` guard is standard Postgres row-locking; traced the "first caller rolls back" sub-case too (second waiter re-evaluates against reverted state, proceeds normally) — correct by construction, not just by the happy-path test already on file. |
| Malformed/non-numeric `bill.cart`/`bill.discount` | Some defined outcome, ideally distinguishable from a real credit/skip | Not clean, but not new: raises, rolls back the guard `UPDATE` too, retried every tick forever. Same accepted shape the design already names for any per-row sweep failure — not filed as a separate gap. |

**Not automated**, same two reasons every prior `aiorders-api` ticket has
recorded (no suite exists; no harness to add a case to) — irrelevant to the
verdict here since inspection is what found both blocking issues, not what
missed them.

**Verdict: FAIL, round 1 (discarded).** No receipt — this round's diff is
about to change. Both findings above are the same B1/B2 code review already
named; nothing QA-only to add to the fix list beyond confirming the fix
actually closes the "unauthorised caller" and "boundary input" rows above,
not just the letter of review's two findings, when round 2 runs.

## ENG-048 (round 2) — both round-1 failing rows re-tested, not re-read

Round 1 set the bar exactly: confirm the fix actually closes "unauthorised
caller" and "boundary input," not just the letter of review's two findings.
The database agent's own round-2 writeup already claims both are closed, with
its own disposable-replica evidence — but that evidence is precisely what
proved insufficient once already on this ticket (round 1's literal `revoke
... from public` read as closing B1 and didn't). Re-tested both from scratch
this round rather than reading the writeup and marking the table `pass`:

- Built a fresh replica (`supabase/postgres:15.8.1.073`), fixture written
  independently (not the file already on disk), applied the real migration
  unmodified.
- **Unauthorised caller:** `has_function_privilege('anon', ..., 'EXECUTE')`
  and the same for `authenticated` both return `false`; `service_role` and
  `postgres` both `true`. The corrected fix (naming `anon`/`authenticated`
  directly) is what's actually in the file — confirmed by reading the diff
  before testing it, not assumed from round 1's own recommendation text,
  which this project's `pg_default_acl` setup would have defeated.
- **Boundary input:** fixture order `bill = {"cart": 20, "discount": 35}` —
  `credited`, `amount 0.00, points 0.0000`. Floored, not negative, on the
  exact shape (discount exceeding cart) round 1 named.
- **Regression, not in round 1's own table:** repeat call on the same order
  with the other `fulfillment_reason` still returns `already_processed`, the
  ledger still holds exactly one row. The idempotency guard is a different
  code path from both fixes (confirmed via `git diff 9fccdad 60fa06e` before
  testing anything — only the amount line and the grant/revoke block
  changed), so this is a non-regression check, not a new area of risk.

**Acceptance coverage (AC4, AC5, AC8, AC9, AC12) — not re-derived.** Neither
fix touches the guard clause, the identity walk, or the rate lookup, so
round 1's own basis for all five (inspection plus the disposable-replica
evidence, AC12 independently traced through source) still holds without
re-running it.

**Not filed as a new observation or proposal on its own** — the one systemic
finding worth surfacing this round (append-only enforced by convention only,
repo-wide) belongs to code review's own notebook entry and `proposals.md`;
a second QA-side note would fragment tracking of the same finding.

**Verdict: PASS, round 2.** Receipt: `agents/qa/test-plans/ENG-048.md`. 0 open
P0/P1 (`agents/qa/bugs/_index.md`: one open item, `BUG-001`, P2, unrelated
project area). Continues to `in-qa` — code review passed concurrently on the
same diff (`agents/principal-engineer/reviews/ENG-048.md`).

## ENG-049 — the first `aiorders-api` ticket with real, independently-runnable tests

Every prior ticket on this project this board has seen (`ENG-031`, `ENG-044`,
`ENG-048`, ...) was pure SQL or inspection-only — this is the first with
actual `.test.ts` files to run rather than read. Ran all three myself rather
than trusting the ticket's own counts: `cloudwaitress.test.ts` 8/8,
`sweep.test.ts` 10/10, `loyalty.test.ts` 19/19 — matched exactly.

**Coverage cross-check, both halves at once.** This ticket owns AC6, AC10,
AC13, AC14, AC17, AC18 in full and the webhook/sweep-caller/dine-in half of
AC1, AC2, AC3, AC7, AC11, AC15, AC16 — `ENG-048` owns the guard/crediting
half of the latter seven. Checked both test plans side by side rather than
grading this ticket's half in isolation: no gap on either side for any of
the seven shared criteria (`ENG-048`'s own idempotency/guard tests cover the
half this ticket doesn't touch).

**The balance-summing regression test actually distinguishes the fix from
the bug, not just asserts a number.** Read `makeLedgerTable`'s own fake
before trusting the 505-row test: `.limit(n)` is captured per query-chain
instance (a fresh closure per `.from()` call), so the unbounded sum query
and the capped display query genuinely see different row counts inside the
fake — this test would go red if `readBalance` ever went back to summing
from the capped list, the same way a real Postgres query would catch it.
Worth checking, since a fake that ignores `.limit()` entirely would make
this "regression test" pass against the reverted bug too and prove nothing.

**Test-infrastructure gap: strengthened an existing proposal rather than
filing a new one.** `proposals.md`'s 2026-09-03 row (`qa`, `aiorders-api`)
already names "three individual functions... carry their own [deno.json],
undiscoverable from the repo root and unregistered anywhere." This ticket
adds a fourth (`loyalty-auto-complete/deno.json`) with three of its four
touched functions now carrying real, passing tests in exactly that
undiscoverable shape — new evidence for the same already-open ask, not a
new gap. Appended a note to that row rather than duplicating it.

**Verdict: PASS, round 1.** Receipt: `agents/qa/test-plans/ENG-049.md`. 0
open P0/P1 (`agents/qa/bugs/_index.md`: one open item, `BUG-001`, P2,
unrelated project area). Continues to `in-security` — code review passed
concurrently on the same diff (`agents/principal-engineer/reviews/ENG-049.md`).

## ENG-049 round 2 — the webhook-secret fix, graded as a regression suite, not a new AC

Security gate round 1 blocked on one critical finding (CloudWaitress webhook
accepted any caller) and sent the ticket to `building`; the fix hop added
`verifyCloudWaitressSecret` plus 8 tests and returned it to `in-review`.
Checked the PRD first, same as `ENG-038`'s round 6 precedent: neither the AC
list nor the Risks section names webhook authentication anywhere — the
design's own Approach text ("no auth-model change") was answering a
different question, not asserting the inbound payload trustworthy — so this
finding owes suite-green and a verified regression suite, not a new AC row.

Ran all three suites myself rather than trusting the fix's own counts:
`cloudwaitress.test.ts` **16/16** (was 8/8), `sweep.test.ts` 10/10
(unchanged), `loyalty.test.ts` 19/19 (unchanged) — **45/45**, matching
exactly.

**Fresh re-check of every AC this ticket owns, full or half — not just the
fixed finding.** All thirteen (6, 10, 13, 14, 17, 18 in full; 1, 2, 3, 7, 11,
15, 16 by half) still pass; nothing in this round's two-file diff touches
any of them, confirmed by reading the diff rather than assuming an
unrelated-looking fix stayed unrelated.

**Graded the 8 new tests as a security regression suite.** The two that
matter most: `rejects order_new with no configured secret ... before ever
touching supabase` and its terminal-event sibling both assert zero
`tableCalls`/`rpcCalls`, not just a `401` — proving an unauthenticated
caller can't get partway through order creation, which is the actual shape
of the fraud path the finding traced. The two positive tests (correctly-
signed traffic still passes, still reaches `credit_order_if_eligible` with
the same RPC args round 1 asserted) are what stop this from being gradeable
as "any 401 would do" — an over-broad fix that also rejected legitimate
webhooks would fail these two and nothing else would have caught it.

0 open P0/P1, unchanged (`BUG-001` still the only open item, still
unrelated). No new bug filed — the finding was a security-gate item with its
own fix hop, not a QA-discovered defect.

**Verdict: PASS, round 2.** Receipt: `agents/qa/test-plans/ENG-049.md`.
Continues to `in-security` — code review round 2 passed concurrently on the
same diff (`agents/principal-engineer/reviews/ENG-049.md`).
