# Review log — 2026-09-03

## ENG-022 (round 1, aiorders-api) — pass

Findings by category:

- **Duplication (non-blocking, 1st occurrence).** `offers.ts`'s 8
  access-denial call sites repeat an identical two-line block
  (`console.warn(...)` + `return {success:false, error}`) that a small local
  helper could collapse. Not blocking — matches the file's own pre-existing
  level of per-action repetition, and `offers.ts` deliberately stayed off
  `requireRestaurantAccess` per its own return-style convention. Watching for
  a second occurrence of "repeated denial/error-response block in one file"
  anywhere on this board before treating it as a standards candidate.
- **Positive signal.** A mutation check was actually executed this round
  (not hand-traced): disabling the access check at one throw-convention site
  and one return-convention site turned exactly the two matching tests red,
  with every other test in both files — untouched call sites included —
  staying green. That's the shape every negative-authz test on this board
  should have; worth pointing to as an example for future test-authoring.

## ENG-015 (round 1, aiorders-api + aiorders-admin-hub) — FAIL

Findings by category:

- **Automatic-failure #3/#10 (blocking, 3rd occurrence this week).** Zero
  test coverage on `restaurants.ts`'s new brand-scoping logic
  (`isStaff`/`getPartnerBrandIds`, all three modified functions). Direct
  in-directory precedent (`brands.test.ts`, `loyalty-config.test.ts`) and
  today's own `ENG-022` (24 tests, identical class of fix) both establish
  this is expected, not this repo's baseline. Third occurrence of this
  exact shape this week (`ENG-013` round 1, `ENG-008` round 1 — both logged
  here as "not yet a third," waiting for exactly this) — crosses
  `code-review-gate/SKILL.md` step 10's promotion threshold. Flagged to
  `observations.md` rather than edited directly: `engineering-standards.md`
  lives in the read-only department tree, out of reach for an
  instance-scoped pass.
- **Authorization bug (blocking, found independent of the missing tests).**
  `updateRestaurant` (`restaurants.ts:207-232`) checks only the target
  restaurant's *existing* `brand_id` against the caller's owned brands, then
  writes every other body field unfiltered via the service-role client — no
  RLS backstop. A partner can `PUT` their own restaurant with
  `{approved: true}` and self-approve it (defeats this ticket's own AC5),
  or with `{brand_id: <unowned brand>}` and reassign it. The build hop's own
  PR-body claim that this can't happen is checked against the code and is
  wrong — the check never inspects the incoming body, only the existing
  row. Exactly the class of bug the missing negative test above exists to
  catch.
- **Verified independently:** `deno check` clean (typecheck can't catch
  either finding — both are authorization logic, not types); worktrees
  match the ticket's recorded commits exactly, no drift; error wording,
  `Profile['role']` literals, and `user.profile` shape all confirmed against
  the actual source rather than trusted from the design/build log.

**Verdict:** fail, round 1. No receipt written. QA's hop discarded, no
test-plan file.

## ENG-015 (round 2, aiorders-api + aiorders-admin-hub) — PASS

Findings by category:

- **Both round-1 findings verified fixed, independently re-derived.**
  `stripPartnerRestrictedFields` closes both the self-approve bypass and
  the brand-reassignment bypass. Re-ran the mutation check myself rather
  than trusting the fix hop's own account: reverted the strip, got exactly
  the three tests naming these findings red (19 others green), restored
  byte-identical, re-ran clean. Same result the fix hop reported — now
  confirmed independently, not merely repeated.
- **Automatic-failure scan:** all 10 clear (#3/#10 closed by the 22 new
  tests).
- **Test quality (positive signal):** assertions on recorded `.update()`
  payloads and on which tables get queried at all — proving behaviour at
  the boundary with the datastore, not implementation internals. The
  "empty brand list never queries `restaurants`" test uses a `from()`
  override that throws on any unstubbed table, so it can't pass vacuously.
- **Three non-blocking notes, none asked for a re-round** (full text in
  the receipt): an untested empty-`{}`-payload PostgREST edge case (low
  severity — either behaviour preserves the security property); a
  pre-existing (not this round's) read-then-write ownership check in
  `updateRestaurant`, theoretically non-atomic, no real trigger path in
  this codebase; and a missing log line on the two new 403s — checked
  against this ticket's own cited precedent (`_shared/restaurantAccess.ts`,
  which also logs nothing on denial) and let go as consistent with that
  convention rather than a deviation from it, rather than promoted off one
  data point on each side.
- **The one substantive gap this round surfaces isn't a code defect: it's
  that AC3/AC4/AC5 (the add-location write path) rest entirely on the new
  RLS policy plus a frontend conditional, and neither this repo
  (`aiorders-admin-hub`, zero test infra) nor this pass (no live Postgres)
  can execute either.** Spent real effort de-risking this via a full
  policy-history trace instead of waving it through — see QA's own test
  plan for the trace itself. Recorded here because it's the kind of gap a
  future review on this same handler family should recognise on sight: a
  security-relevant INSERT/UPDATE policy with no live execution anywhere
  in its own ticket's history is a pattern this board has now hit more
  than once (`ENG-007`/`ENG-011`/`ENG-013`'s migrations, this ticket's own
  migration doc, now the policy's actual *logic*) — worth a proposal if a
  live read-only DB connection is ever wired in, so this class of gap
  closes for every future ticket at once rather than being re-traced by
  hand each time.

**Verdict:** pass, round 2. Receipt written
(`agents/principal-engineer/reviews/ENG-015.md`). QA passed concurrently
with one named, non-blocking coverage gap (above). Ticket continues to
`in-security`.

## ENG-024 (round 1, aiorders-api, fast lane) — pass

Findings by category:

- **Process gap, first occurrence.** Fast lane has no trigger that routes a
  migration discovered at *build* time to `database`'s own gate
  (`schema-change/SKILL.md`'s trigger is `touches_data: true` on an
  architect design — fast lane skips design entirely). This ticket's
  backfill migration went straight from build to this review with no
  database sign-off. Assessed it informally against `schema-change`'s own
  7 failure conditions myself (outside my actual scope — migration is
  explicitly not mine to gate) and found it low-risk: one soft miss (no
  stated runtime estimate/batching), matching this repo's own only backfill
  precedent exactly. Not blocking this verdict; filed as a proposal
  (`proposals.md`, 2026-09-03) since the mechanism gap is general, not
  specific to this migration.
- **Process note (self-correction, worth flagging so it isn't repeated).**
  My first attempt to reproduce the pre-edit `deno check` baseline used
  `git stash -u`, which silently no-ops when the diff is already committed
  (nothing uncommitted to stash) — it re-checked the *already-fixed* file
  against itself and would have produced a false "identical" match had I
  not noticed the line numbers weren't shifting the way the diff implied.
  Correct approach for a committed diff: `git show origin/main:{path} >
  {path}`, check, then `git checkout -- {path}` to restore. Worth
  remembering for any future round that needs a true pre-edit baseline on a
  branch where the fix is already committed, not left as an uncommitted
  working-tree change.
- **Positive signal.** Mutation check executed directly (not hand-traced):
  removing the one-line fix turned exactly the test naming it red, the
  unrelated guard-clause test stayed green, restore was byte-identical
  (`git diff --stat` empty). Same shape `ENG-022`'s own round today already
  set as the example to point to.
