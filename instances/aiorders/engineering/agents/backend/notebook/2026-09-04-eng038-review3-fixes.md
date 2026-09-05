# ENG-038 review round 3 fixes — redemption/revenue, delivery-by-channel, unsubscribe mechanism coverage

Full reasoning behind the `building -> in-review` hop that follows review
round 3's combined verdict (review PASS, quality gate FAIL); the board-file
log entry carries only the pointer to this file per `conventions.yaml`'s
`ticket_log` rule.

## Scope

All three gaps QA's round-3 quality-gate pass left fully specified as this
hop's work (`agents/qa/test-plans/ENG-038.md`), all three pre-existing since
the original build (round 1), none a regression from rounds 2-3:

1. **Gap 1 (blocking, AC4).** `getBroadcastReport`'s coupon-redemption/revenue
   matching (`broadcasts.ts:594-601` as of round 3) had zero test of its real
   branch — both existing tests set `offer_id: null`.
2. **Gap 2 (blocking, AC5 read half).** Same function's delivery-by-channel
   aggregation (`541-552`) was likewise only exercised via its empty-array
   branch.
3. **Gap 3 (blocking, AC6, highest stakes).** The unsubscribe token
   sign/verify pair and the `broadcast-unsubscribe` handler had no test
   anywhere — a public, unauthenticated, consent-mutating endpoint.

Worktree confirmed fresh before editing (not trusted from the trigger's
checkpoint): `~/Documents/projects/_eng/aiorders-api`,
`feat/ENG-038-broadcast-composer-dispatcher-unsubscribe@87f3f8c`, matching
round 3's own reviewed commit exactly; `git fetch origin main` showed no
drift.

## Fix 1 — `brand-portal/broadcasts.ts` (Gaps 1 + 2)

Extracted both branches QA named into pure, exported functions, matching
this ticket's own round-2 precedent (`buildBroadcastSmsBody`/
`buildBroadcastEmailBody`) and QA's own suggested signatures exactly:

- `computeRedemptions(orders, couponCode): {redemptions, revenue}` — the
  `promos` array-matching + `total_amount` summing that was inline in the
  `if (campaign.offer_id)` branch.
- `buildDeliveryByChannel(logRows): Record<string, {sent, opened, clicked}>`
  — the `communication_log` bucketing loop.

`getBroadcastReport` now just calls both; output is byte-identical (pure
extraction, no logic change).

Added 8 tests to `broadcasts.test.ts`: `computeRedemptions` — matching order
counted+summed, non-matching `promos` entry excluded, no-`promos`-array
excluded, multiple matches sum correctly, empty input → `{0, 0}` (not
null — that distinction is the caller's job one level up, unchanged);
`buildDeliveryByChannel` — two channels bucketed independently,
sent/delivered both count as sent but failed doesn't, opened/clicked
counted only when their timestamp is present.

**Mutation-verified the higher-stakes of the two** (money, not counting —
same proportionality every prior round used): changed the `promos` matching
predicate from `promo?.code === couponCode` to `!== couponCode`. Result:
exactly the three tests that depend on correct matching failed (`counts and
sums a matching order`, `excludes ... doesn't match`, `sums multiple
matching orders`); the no-`promos`-array and empty-input tests, which don't
depend on the comparison direction, stayed green. Restored via backup,
`git diff --stat` empty, re-ran clean.

## Fix 2 — `_shared/broadcastUnsubscribe.ts` (Gap 3a)

`signUnsubscribeToken`/`verifyUnsubscribeToken` needed no extraction (both
already exported, both pure aside from one env read) — added
`broadcastUnsubscribe.test.ts` directly: sign-then-verify round trip returns
the original `customerId`; wrong part count → null; malformed base64url →
null; tampered signature → null; missing token → null; missing
`BROADCAST_UNSUBSCRIBE_SECRET` throws from `signUnsubscribeToken` (not
swallowed, since it has no try/catch); the same missing-secret condition
resolves to `null`, not a throw, through `verifyUnsubscribeToken` (its
try/catch does swallow it) — asserted explicitly since that swallow is
deliberate per the design (caller never distinguishes cause).

**F1 closed in the same pass, per QA's own note that it was cheap to do
so here** (`_shared/broadcastUnsubscribe.ts`'s catch-all had no
distinguishing log line — carried non-blocking since round 1). Changed
`catch { return null }` to `catch (error) { console.error(...); return
null }`. No caller-visible behaviour change (still resolves to `null`
either way) — confirmed by keeping the missing-secret-via-verify test
above passing unchanged; only what an operator sees in logs changes,
distinguishing a real misconfiguration from an ordinary bad/tampered token.

**Requires `--allow-env` to run** — the only test file in this repo that
touches `Deno.env`, and Deno's permission model gates env reads and writes
identically with no per-test escalation above the CLI-level grant (verified
empirically: a `Deno.test({permissions: {env: true}})` override throws
`NotCapable: Can't escalate parent thread permissions` when the CLI itself
wasn't given `--allow-env`). Updated `agents/qa/test-plans/ENG-038.md`'s own
`suite_command` field (only that field — `last_run`/`last_result` stay
QA's own to set) to record the flag, per step 6b and this repo's own
per-ticket precedent for command peculiarities (ENG-008/ENG-010/ENG-011/
ENG-013 all recorded an ad hoc `--allow-net`/`--allow-env` the same way).
Ran the 6b grep for `suite_command` first — every other hit is either this
same ticket's own file, another ticket's own already-closed test plan, or
`test-suite-run/SKILL.md`'s generic "read the plan's exact command"
instruction, none of which this change conflicts with.

**Mutation-verified the single highest-stakes property in this whole
hop** (QA's own words: "the highest-stakes of the three gaps in this
report") — changed `verifyUnsubscribeToken`'s `const valid = await
crypto.subtle.verify(...)` to `const valid = true; await
crypto.subtle.verify(...)` (verify still runs, its result just isn't
used). Result: exactly `returns null for a tampered signature` failed,
all six other tests (including the round trip) stayed green. Restored via
backup, `git diff --stat` empty, re-ran clean (7/7).

## Fix 3 — `broadcast-unsubscribe/` (Gap 3b)

`index.ts`'s handler had the channel/token/consent/write branching that
picks the response trapped inside a bare `serve()` callback — the same
shape `broadcast-dispatch/dispatch.ts` already solved. Extracted to a new
`unsubscribe.ts` (never imported by a test through `index.ts`, so `serve()`
never starts during `deno test`):

- `decideUnsubscribePreCheck({channel, customerId, existingConsent})` —
  everything decidable before the database write; returns `null` when the
  caller must attempt the write.
- `decideUnsubscribeWriteResult(updateErrored)` — the post-write mapping.

`index.ts` is now a thin adapter: resolve `channel`/`token` →
`verifyUnsubscribeToken` → (if resolved) fetch the customer row → call
`decideUnsubscribePreCheck` → if it returns non-null, respond; otherwise
attempt the consent write and call `decideUnsubscribeWriteResult`. Verified
by hand against every original branch (channel invalid, token
invalid/missing, customer row missing, idempotent already-unsubscribed,
write error, write success) that the response for each is unchanged.

Added `unsubscribe.test.ts` — 6 tests covering all four named branches
(invalid channel, invalid/missing token, already-unsubscribed idempotent,
write-failure retry) plus the two ways `decideUnsubscribePreCheck` defers
to a write (never-unsubscribed, previously-opted-in) and the write-success
case.

## Full regression, run fresh from within each function's own directory

`brand-portal/` (whole directory, all files) 38/38, `broadcast-dispatch/`
10/10, `outgoing-communications/actors/consumers.test.ts` 2/2,
`broadcast-unsubscribe/` 6/6, `_shared/broadcastUnsubscribe.test.ts`
(`--allow-env`) 7/7. ENG-038-relevant total: 48/48 (27 pre-existing + 8 +
6 + 7 new), no regression anywhere.

## Step 6b

Ran the grep for every artifact this hop's changes touch or rely on:

- `suite_command` — see Fix 2 above; the one real instruction in conflict,
  fixed in this hop.
- `broadcast-unsubscribe`, `verifyUnsubscribeToken`, `signUnsubscribeToken`,
  `getBroadcastReport`, `BROADCAST_UNSUBSCRIBE_SECRET` — hits in the
  architect's design doc and ADR-020 describe the endpoint's *behaviour*
  (routes, response shapes, DB tables), which is unchanged; hits in
  `supabase/functions/README.md`'s house-format section are the same
  behavioural level. Both are `location` classifications per this step's
  taxonomy, not `instruction`, and need no edit — confirmed by reading both
  in full rather than assuming from the grep hit alone.

## Commits

Three, one per gap (Gap 3 split into its own (a)/(b) the way QA's own
report split it):

- `af3da30` — Extract getBroadcastReport's redemption/revenue and
  delivery-by-channel logic into pure functions, add tests (ENG-038)
- `8be42ec` — Add sign/verify round-trip tests for the broadcast
  unsubscribe token, log the misconfigured-secret case (ENG-038)
- `d13722a` — Extract broadcast-unsubscribe's response decision logic into
  pure functions, add tests (ENG-038)

All three pushed to
`origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`. Branch now
18 files, 2472/7 vs. `origin/main` (up from round 3's 15 files, 2237/7).

## `building`'s exit condition

Branch pushed, self-tested (48/48 across five suites, two mutation-verified
properties — the money-matching logic and the token tamper-detection, the
two highest-stakes properties across this hop's three gaps). PR body
written at build time (`agents/backend/notebook/2026-09-04-eng038-build.md`)
still accurate — none of these three fixes change the feature's
externally-visible behaviour, same reasoning the round-2 hop used for the
same question.
