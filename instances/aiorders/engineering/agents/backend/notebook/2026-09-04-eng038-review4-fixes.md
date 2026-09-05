# ENG-038 round-4 fix — Gap 4 (AC5 write half): sendBroadcastMessage send-and-log coverage

Full reasoning behind the `building -> in-review` hop that follows review
round 4's combined verdict (review PASS, quality gate FAIL on Gap 4 only);
the board-file log entry carries only the pointer to this file per
`conventions.yaml`'s `ticket_log` rule.

## Scope

One gap, QA's round-4 quality-gate report (`agents/qa/test-plans/ENG-038.md`,
"Gap 4 — AC5 (write half)"): `outgoing-communications/actors/consumers.ts:
881-1020` (`sendBroadcastMessage`) had zero test coverage anywhere — not a
regression, present since the original build (round 1), surfaced only once
Gap 2 (the read half of the same AC) stopped masking it.

Worktree confirmed fresh before editing (not trusted from the trigger's
checkpoint): `~/Documents/projects/_eng/aiorders-api`,
`feat/ENG-038-broadcast-composer-dispatcher-unsubscribe@d13722a`, matching
round 4's own reviewed commit exactly; `git fetch origin main` showed no
drift.

## Fix — `outgoing-communications/actors/consumers.ts`

Same remedy QA specified, the same shape this ticket has used for every prior
gap (`computeRedemptions`/`buildDeliveryByChannel` in round 3,
`buildBroadcastSmsBody`/`buildBroadcastEmailBody` in round 2) and the shape
`engineering-standards.md`'s "Decision logic does not live trapped inside a
bare handler" rule now names by pattern rather than per-ticket rediscovery:

- `decideBroadcastChannelEligibility(input)` — the per-channel gate
  (`wantsEmail`/`wantsSms`), extracted verbatim from the two inline `const`
  expressions.
- `buildBroadcastEmailLogRow(args)` / `buildBroadcastSmsLogRow(args)` — the
  `communication_log` row shape each channel's insert built inline. Two
  functions, not one polymorphic one, matching the existing
  one-function-per-channel precedent (`buildBroadcastSmsBody`/
  `buildBroadcastEmailBody`) rather than introducing a new shape.

`sendBroadcastMessage` itself is now `export`ed (previously module-private,
which was part of why it had no test entry point) and takes a third,
optional `deps` parameter — `{ sendEmail, sendSMS, buildUnsubscribeUrl }`,
defaulting to the three real functions it already imported. This is the same
injectable-dependency shape `broadcast-dispatch/dispatch.ts`'s `sendFn`
already established for this exact problem (a function that must call a real
network/crypto boundary in production but must not touch either in a test).

**Why `buildUnsubscribeUrl` is injected too, not just `sendEmail`/`sendSMS`.**
QA's own cover list ("one channel succeeds and the other fails") requires
exercising `sendBroadcastMessage`'s real orchestration end-to-end with a fake
Supabase client, the same way `broadcasts.test.ts` already fakes
`supabase.from()` — the interesting bug surface (the `anySucceeded`
aggregation, per-row status independence) lives in the un-extracted
orchestration, not in either pure fragment alone. `buildUnsubscribeUrl` sits
on that same call path and throws from `hmacKey()` when
`BROADCAST_UNSUBSCRIBE_SECRET` isn't set (`_shared/broadcastUnsubscribe.ts`).
The alternative — setting that env var in this test the way
`_shared/broadcastUnsubscribe.test.ts` already does — would require adding
`--allow-env` to `outgoing-communications/`'s own suite_command entry too,
contradicting round 3's own recorded claim that `_shared/` is "the only file
in this repo that touches `Deno.env`" (`agents/qa/test-plans/ENG-038.md`'s
frontmatter). Injecting the dependency instead keeps that claim true and
needs no `suite_command` edit — confirmed by re-running the 6b grep below.

No change to the row shape itself, the eligibility logic, or the aggregate
return value — this is an extraction, not a behaviour change, same as every
prior gap's fix on this ticket. The call site in
`handleConsumerCommunications`'s switch statement is unchanged (the new
third parameter is optional).

## Tests added — `consumers.test.ts` (2 -> 16)

- `decideBroadcastChannelEligibility` — 5 tests: both channels eligible;
  email excluded on missing subject; email excluded on no address on file;
  sms excluded when the step turns it off despite content+phone both
  existing; sms excluded on no phone on file.
- `buildBroadcastEmailLogRow` / `buildBroadcastSmsLogRow` — 4 tests: a
  successful send marked `sent` with the campaign `reference_type`/
  `reference_id` and (email only) `provider_message_id`; a failed send
  marked `failed` with `error_message` preserved and `sent_at: null`.
- `sendBroadcastMessage`, orchestration-level, fake Supabase (local
  `fakeSupabase`, trimmed from `broadcasts.test.ts`'s own to the
  `select().eq().single()` / `.insert()` chains this handler actually calls)
  plus injected `fakeDeps` — 5 tests covering exactly QA's cover list:
  email-only (no `smsBody` authored), sms-only (no email content authored),
  both channels, the neither-eligible skip path (asserts zero inserts and
  zero calls to either send function), and one channel succeeding while the
  other fails (asserts `anySucceeded`/overall `success: true`, and each row's
  own `status`/`error_message` independently).

**Mutation-verified the property QA specifically named** ("confirms
`anySucceeded`... independently"): flipped
`Boolean(emailResult?.success) || Boolean(smsResult?.success)` to `&&`.
Result: exactly 3 of the 6 orchestration tests failed — email-only, sms-only,
and the one-succeeds-one-fails case (the other channel's result defaults to
`null` when that channel isn't attempted, so `&&` against a `null`-derived
`false` breaks every case except "both succeed" and the skip path, which
never reaches this line). Restored via backup, `git diff --stat` empty
against the backup, re-ran clean (16/16).

## Full regression, run fresh from within each function's own directory

`brand-portal/` (whole directory) 38/38, `broadcast-dispatch/` 10/10,
`outgoing-communications/actors/consumers.test.ts` 16/16 (was 2/2),
`broadcast-unsubscribe/` 6/6, `_shared/broadcastUnsubscribe.test.ts`
(`--allow-env`) 7/7 — no regression anywhere. ENG-038-relevant total: 62/62
(27 pre-existing + 21 rounds 1-4 + 14 this round).

Also ran `deno check` on both touched files (extra due diligence, not this
project's own `--no-check` `suite_command`): `consumers.ts` surfaces 8
in-file errors, all `TS18046 'error' is of type 'unknown'` on the
pre-existing `catch (error) { ...error.message }` pattern this file already
repeats in every other handler (lines 174/356/419/566/629/795/858, none
touched by this diff) plus the one instance inside `sendBroadcastMessage`'s
own catch block, which this fix preserved verbatim — not a new condition,
not filed (fixing it here would be automatic-failure #7, an unrelated
bundled change, the same call round 4 made on `brand-portal/utils.ts`'s 9
pre-existing errors). `consumers.test.ts` initially failed to resolve types
at all via the `npm:@supabase/supabase-js@2` specifier (the same specifier
`broadcasts.test.ts` uses) — switched to the `https://esm.sh/
@supabase/supabase-js@2.45.0` URL `consumers.ts` itself already imports
`SupabaseClient` from, which resolves cleanly in this directory; re-ran
clean, zero errors in the test file itself.

## Step 6b

Grepped every artifact this hop's change touches or relies on:

- `sendBroadcastMessage`, `decideBroadcastChannelEligibility`,
  `buildBroadcastEmailLogRow`, `buildBroadcastSmsLogRow` — hits are all in
  this ticket's own board log, QA test plan, and prior review/notebook
  entries, all narrating history at the time they were written (`location`,
  not `instruction` — a round's own log doesn't get rewritten by a later
  round any more than round 3's did). One hit in
  `departments/engineering/agents/eng-manager/config/engineering-standards.md`
  cites this exact ticket as precedent for the extraction pattern; it is
  department-owned (read-only from this instance regardless) and
  precedent-citing prose, not a claim this hop makes newly stale.
- `communication_log` — hits in the architect's design doc and ADR-020
  describe the table's role/shape at the design level; the row shape
  written is byte-identical to before (extraction, not a change), so both
  stay accurate. `location`, no edit needed.
- `suite_command` — confirmed **not** touched this round (see "Why
  `buildUnsubscribeUrl` is injected too" above) — the one thing that would
  have required an edit here didn't happen, by design.

## Commits

One commit, this gap being a single cohesive extraction+test unit (unlike
round 3's three independent gaps):

- Extract sendBroadcastMessage's channel gate and communication_log row
  shape into pure, tested functions; make send/unsubscribe-url deps
  injectable (ENG-038)

Pushed to `origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`.

## `building`'s exit condition

Branch pushed, self-tested (62/62 across five suites, one mutation-verified
property — the `anySucceeded` OR-aggregation QA named directly). No
externally-visible behaviour change (same reasoning every prior fix hop on
this ticket has used for the same question) — PR body from the original
build hop (`agents/backend/notebook/2026-09-04-eng038-build.md`) still
accurate.
