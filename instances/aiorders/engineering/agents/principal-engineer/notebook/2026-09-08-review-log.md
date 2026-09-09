# 2026-09-08 — Review log

## ENG-052 (round 1, aiorders-api) — REVIEW pass

One-file diff, `feat/ENG-052-loyalty-redemption-ledger-widening-and-redeem-function`
(`0a2f730`) vs `origin/main`: pure SQL migration, 267 lines, widening
`loyalty_ledger_entries` for a redemption row and adding
`redeem_points_if_eligible`. **0/10 automatic failures.**

Design conformance confirmed line-by-line against
`agents/architect/designs/ENG-051-....md`'s Interfaces section — signature,
7-step body order, idempotency-match condition, grant/revoke shape, all
exact. One design gap (`rate_applied` sized for the earn side's percentages,
too narrow for `redemption_value_per_point`'s own 4-decimal precision) was
found and fixed by the database agent within the same build hop, not left
for this gate to catch.

**Independent verification, own fixture and own container, not the database
agent's** — same standard `ENG-044`'s and `ENG-048`'s own rounds applied,
given this project's specific history of a "looks right" grant/revoke fix
that wasn't (`ENG-048` B1). Reproduced every material claim in the migration
plan doc: access control (catalog read *and* an actual denied `set role anon`
/ `authenticated` call), the sub-cent precision case (`0.0025` stored and
read back exactly, not `0.00`), idempotent replay (zero new rows),
idempotency conflict (real raise), insufficient balance, the exact-balance
boundary (`<` not `<=`), not-enrolled, invalid-code, both guards, all four
cross-field `CHECK`s in the failing direction, and `rate_applied`
backward-compatibility for the earn side. Every number matched the writeup
exactly — first ENG-052 review round to independently re-derive the whole
matrix from scratch rather than spot-checking a subset, given the
money-adjacent surface (the department's first debit-shaped write path
against a real balance).

Two non-blocking notes, neither a standard (first occurrence of each): the
insert omits `order_id`/`fulfillment_reason` rather than passing explicit
`null` (equivalent, no prior SQL-level precedent on this table either way);
`amount` stores the redemption's positive dollar magnitude while `points`
stores the signed delta — matches the design exactly, worth naming so a
future reader isn't surprised the two columns use different sign
conventions.

**Verdict: PASS, round 1.** Full writeup:
`agents/principal-engineer/reviews/ENG-052.md`.

## ENG-053 (round 1, aiorders-api) — REVIEW pass

Diff: `fff72f0` vs `0a2f730` (`ENG-052`'s own commit, this ticket's stacked
base) — 2 files, 70 insertions / 1 deletion. **0/10 automatic failures** on
the standard scan.

Design conformance confirmed line-by-line against
`agents/architect/designs/ENG-051-....md`'s Interfaces section: payload
shape, `requireRestaurantAccess`-then-validation order, the exact
`supabase.rpc('redeem_points_if_eligible', {...})` argument names,
`invalid_code`/`not_enrolled` returned directly, `insufficient_balance`/
`redeemed` attaching `readBalance`'s own unchanged output, `source` union
widened to add `'redemption'`. All exact. The 500-vs-400 judgment call this
ticket names in its own Log is real but not new — a second instance of the
already-escalated 2026-09-07 proposal (found on `ENG-049`'s AC17 language),
correctly not re-filed as a fresh one.

**One blocking finding, not on the automatic-10 list but squarely "review
what isn't there" (step 6): `redeemPoints` shipped with zero test
coverage, in a file that already has a real, passing suite covering its
two sibling functions.**

`brand-portal/loyalty.ts` has carried `loyalty.test.ts` since `ENG-049`
(2026-09-07, `4cd02f5`) — 19 tests, covering `recordDineInEarn`,
`getLoyaltyBalance`, `readBalance`, and `handleLoyalty`'s routing. Ran it
myself against this ticket's branch rather than trusting the build hop's
own account (`deno test --no-check`, from outside the repo tree — the same
`npm:`-resolution workaround the build hop used for `deno check`): **19
passed, 0 failed**, nothing regressed. But zero of the 19 touch
`redeem_points`/`redeemPoints` (`grep -n "redeemPoints\|redeem_points"
loyalty.test.ts` — no hits). This ticket added ~50 lines of new branching
logic to the exact file that suite exists for (3 validation branches —
missing `code`, missing `idempotency_key`, non-positive `points` — and 4
RPC-outcome branches — `invalid_code`, `not_enrolled`,
`insufficient_balance`, `redeemed`) and extended none of it.

**The ticket's own board-log Notes and this pass's build-hop entry both
state "no test suite exists for this project" — true for the SQL migration
side (no `deno.json`, verified by disposable replica instead, same as
`ENG-048`/`ENG-052`) but false for this specific file.** `loyalty.test.ts`
is real, `deno test`-runnable in this exact environment (`/opt/homebrew/
bin/deno` present), and was written by this ticket's own immediate
predecessor on the same file three days ago. This isn't a project-wide gap
this ticket inherited — it's a same-file regression in a practice `ENG-049`
itself established. `handleLoyalty routes both actions to their own
handler` (line 270) is now also a stale test name — the switch gained a
third case this ticket doesn't know about.

**Not the 500-vs-400 shape (a systemic, already-flagged, disproportionate-
to-fix-here gap) — this is sized exactly to this ticket.** The fake-
`SupabaseClient` harness `loyalty.test.ts` already uses for
`recordDineInEarn` (stub the access-check dependency chain, assert a
thrown `Error` on denial) covers `redeemPoints`'s own access check with no
new pattern needed, and `acquisition.test.ts` (2026-09-05) already
extended the identical harness with a stubbed `.rpc()` for its own one
aggregate call — the exact shape `redeemPoints`'s
`redeem_points_if_eligible` call needs. Nothing to invent.

**Specific fix, round 2 — add to `loyalty.test.ts`:**
1. `restaurant_id`/`code`/`idempotency_key` missing, and `points`
   non-positive/non-finite/wrong-type → rejects, **and the stubbed
   `.rpc()` is never called** (the design's own load-bearing "no RPC call
   made" claim — assert call count, not just the throw).
2. Access denied (`requireRestaurantAccess` throws) → propagates, RPC
   never called.
3. Each of the four RPC outcomes (`invalid_code`, `not_enrolled`,
   `insufficient_balance`, `redeemed`) via a stubbed `.rpc()` returning
   each in turn — the first two return without calling `readBalance`, the
   last two attach it.
4. Update (or rename) `handleLoyalty routes both actions to their own
   handler` — it no longer covers everything the name claims.

**Non-blocking note, not a standard (first occurrence):** `redeemPoints`'s
own docstring says "AC10 in full" and "half of AC3, AC4, AC7, AC8, and
AC11" — `ENG-051`'s own AC numbers. `getLoyaltyBalance`'s existing
docstring three functions up also says "AC10," and `recordDineInEarn`'s
says "AC11" — both `ENG-049`'s own numbers, for unrelated requirements.
Four AC-numbered comments in one file now resolve to two different PRDs
depending on which function they're attached to, with nothing in the text
itself signalling that. Worth a `(ENG-051)`/`(ENG-049)` suffix next time
either file's touched; not blocking on its own.

**Verdict: FAIL, round 1.** No receipt — round discarded, per
`code-review-gate/SKILL.md` step 9. QA's own quality gate ran concurrently
on the same diff and independently landed on the same root cause (missing
coverage, not a design or logic defect) — see
`agents/qa/notebook/2026-09-08-coverage-gaps.md`.

## ENG-053 (round 2, aiorders-api) — REVIEW pass, on the missing-coverage fix

`git diff fff72f0 ec5e099 --stat` first: one file, `loyalty.test.ts`, 141/-4
— no change to `loyalty.ts` or `index.ts` this round, so round 1's clean
automatic-failure scan and design-conformance walk on the implementation
itself need no re-review, only regression-checking that the new tests don't
disturb anything. **0/10 automatic failures**, re-scanned fresh against this
round's diff.

**Read each of round 1's four fix-list items against the actual new tests,
not against the ticket's own account of them** — same discipline `ENG-049`'s
own round 2 applied to its security-fix tests. All four present and each
proves the specific property named: the eleven negative-input tests assert
both the rejection message and `rpcCalls.length === 0`; the four RPC-outcome
tests assert `ledger.queryCount() === 0` on the two no-balance branches and
the correct summed value on the two balance-attaching branches (a real,
mutation-sensitive property — swapping which branches attach balance would
fail it); `handleLoyalty`'s renamed test now dispatches `redeem_points`
through the switch and confirms exactly one `.rpc()` call reaches
`redeem_points_if_eligible`.

**Independently re-verified, not accepted on the fix hop's own account:**
`deno test --no-check` on `loyalty.test.ts` alone — 34/34 (was 19, +15 new,
matching exactly); full `brand-portal/*.test.ts` — 119/119, nothing
regressed. `deno check` on `loyalty.test.ts` alone — same 3 pre-existing
`utils.ts` errors as round 1, zero new; on the three-file set including
`index.ts` — 24 pre-existing errors across `profiles.ts`/`restaurants.ts`/
`utils.ts`/`website.ts` (a broader check than the ticket's own scope, since
`index.ts` transitively pulls in every sibling handler), none in the files
this ticket touches.

One non-blocking note carried forward unchanged (the AC-number collision
across `ENG-049`'s and `ENG-051`'s own numbering in this file) — neither
docstring touched this round, not re-verified fresh.

**Verdict: PASS, round 2.** Receipt: `agents/principal-engineer/reviews/ENG-053.md`.
`links.review` set. Continues to `in-security` — QA's own gate ran
concurrently on the same diff and also passed, its first non-discarded
receipt for this ticket: `agents/qa/test-plans/ENG-053.md`.
