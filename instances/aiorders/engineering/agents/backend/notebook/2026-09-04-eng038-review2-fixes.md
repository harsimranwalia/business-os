# ENG-038 review round 2 fixes — SMS/email body extraction, dispatch enrollment coverage

Full reasoning behind the `building -> in-review` hop that follows review
round 2's FAIL; the board-file log entry carries only the pointer to this
file per `conventions.yaml`'s `ticket_log` rule.

## Scope

Both items review round 2 left fully specified as this hop's work (no third
round needed for either):

1. **Blocking (automatic failure #3, missing test on a bug fix).** Round 1's
   SMS "Reply STOP" defect was fixed in `ede0e1e` with no regression test —
   `sendBroadcastMessage` wasn't exported and `outgoing-communications/` had
   zero test files.
2. **QA coverage gap, named as a real quality-gate risk for the next round.**
   `dispatch.test.ts` covered only the claim/resolve half of the dispatcher;
   `promoteDueCampaigns`/`enrollAudience` — three of the ticket's seven
   acceptance criteria (AC1 schedule/immediate promotion, AC2 per-step drip
   fan-out, AC3 audience-mode choice) — had zero coverage anywhere.

Worktree confirmed fresh before editing (not trusted from the trigger's
checkpoint): `~/Documents/projects/_eng/aiorders-api`,
`feat/ENG-038-broadcast-composer-dispatcher-unsubscribe@ede0e1e`, matching
round 2's own reviewed commit exactly.

## Fix 1 — `outgoing-communications/actors/consumers.ts`

Extracted both inline body-construction template literals out of
`sendBroadcastMessage` into pure, exported functions:
`buildBroadcastSmsBody(smsBody, templateVariables, unsubscribeUrl)` and, for
symmetry (round 2's own suggestion), `buildBroadcastEmailBody(emailBody,
templateVariables, unsubscribeUrl)`. `sendBroadcastMessage` now just calls
these instead of building the strings inline; the resulting SMS/email text is
byte-identical to before, this is a pure extraction plus a fix that was
already committed in `ede0e1e`.

Added `consumers.test.ts` (first test file for this directory) — two tests,
asserting the SMS/email output never contains `STOP`/`Reply`, and asserts the
exact `Visit {url} to unsubscribe.` / `Unsubscribe: {url}` sentences
byte-for-byte. Confirmed this directory needs no `deno.json` to run tests
(same as every sibling function directory): `deno test --no-check
actors/consumers.test.ts` from within `outgoing-communications/` resolved
and ran clean without one.

**Mutation-verified per `engineering-standards.md`'s rule:** reverted
`buildBroadcastSmsBody` to the exact old buggy text (`Reply STOP or visit
{url} to unsubscribe.`), re-ran — only the STOP/Reply assertion failed
(`AssertionError: Values are not equal: - true / + false`), the email test
still passed untouched. Restored via the pre-edit backup, re-ran clean (2/2).

**`deno check actors/consumers.ts` (informational, not enforced):** 8 errors,
none in the two new functions (they're one-line pure returns with no
`catch`). Traced each: 5 are the pre-existing untyped-`catch (error)` idiom
already used by every other handler in this file (`sendOrderFeedbackRequest`,
`sendWelcomeOffer`, `sendEveryOrderOffer`, `sendFirstOrderOffer`,
`sendBroadcastMessage` itself); 3 are the already-documented, already-
proposed `sendSMS({to, body})` vs. the real `{to, message}` signature
mismatch at the three lifecycle-offer call sites (see this ticket's own build
notebook, "Pre-existing bug found, not fixed here" — already has a proposal
row, not this hop's to fix). Confirmed via `grep -n "catch (error)"` and
reading each flagged line directly, not assumed from the error count alone.

## Fix 2 — `broadcast-dispatch/dispatch.test.ts`

Added a second, purpose-built fake (`makeQueryableTable` +
`makeEnrollmentSupabase`) rather than extending the existing
`makeRecipientsTable`/`combinedSupabase` pair above it in the same file —
`promoteDueCampaigns`/`enrollAudience` touch three additional tables
(`broadcast_campaigns`, `customers`, `broadcast_campaign_steps`) plus an
`INSERT` on `broadcast_campaign_recipients`, none of which the existing
claim/resolve fakes support, and extending them risked changing behavior the
four passing tests already depend on. The new fake supports
`select/update/insert/eq/lte/or/order` generically, including a minimal
`.or()` parser for the one clause shape `enrollAudience` actually builds
(`last_order_at.lt.<cutoff>,last_order_at.is.null`).

Six new tests, covering every property round 2 named "at minimum":

- `promoteDueCampaigns` promotes only the campaign whose `scheduled_send_at`
  has arrived; the not-yet-due one stays `scheduled`.
- `enrollAudience` with `audience_mode: 'all'` ignores `last_order_at`
  entirely.
- `enrollAudience` with `audience_mode: 'inactive_days'` excludes a customer
  who ordered inside the cutoff, includes one who ordered before it, and
  includes one who never ordered (`null` counts as inactive too).
- `enrollAudience` excludes a customer only when *both* `consent_email` and
  `consent_sms` are explicitly `false` — one channel opted out, the other
  not, still enrolls; no consent rows yet (`null`) still enrolls.
- `enrollAudience` fans out one recipient row per step, and the *gap*
  between two steps' `due_at` for the same customer equals exactly the
  difference in their `delay_hours` — asserted as a delta rather than an
  absolute value so the test isn't racing the real clock (both rows share
  one `enrolledAt = Date.now()` call inside the function, so the delta is
  exact by construction, not approximate).
- `enrollAudience` flips a campaign straight to `completed` when its
  audience resolves to zero contactable customers, and inserts no recipient
  rows.

**Mutation-verified the two highest-value properties** (not all six — same
proportionality round 1 used, picking the highest-stakes property rather
than mutating everything):

- Removed the `.lte('scheduled_send_at', nowIso)` line from
  `promoteDueCampaigns`: the not-yet-due campaign got promoted too,
  `promotedCount` came back `2` instead of `1`, and exactly the promotion
  test failed (`AssertionError: - 2 / + 1`). Restored via backup, re-ran
  clean.
- Changed `enrollAudience`'s `due_at` line to drop the
  `+ (step.delay_hours || 0) * 60 * 60 * 1000` term entirely: the fan-out
  test's delta assertion failed (`AssertionError: - 0 / + 86400000`) while
  every other test stayed green. Restored via backup, re-ran clean.

**Full regression, run fresh from within each function's own directory
(matching every prior round's practice — the shared `supabase/functions/`
root doesn't resolve `npm:@supabase/supabase-js@2`):** `dispatch.test.ts`
10/10 (4 pre-existing + 6 new), `brand-portal/broadcasts.test.ts` 6/6,
`brand-portal/offers.test.ts` 9/9, `consumers.test.ts` 2/2 — 27/27, no
regression anywhere.

## Step 6b

Neither fix writes or relies on a rule about an artifact (no new receipt
path, state name, config key, or file-another-agent-produces convention) —
both are internal extraction + test additions with no cross-file contract.
No grep run; noted here so the omission reads as considered, not skipped.

## Commits

Two, mirroring this ticket's own build-hop practice of one commit per
logically distinct change:

- `d9c98ff` — Extract broadcast SMS/email body builders and add regression
  test (ENG-038)
- `87f3f8c` — Add promoteDueCampaigns/enrollAudience test coverage (ENG-038)

Both pushed to `origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`.
Branch now 15 files, 2237/7 vs. `origin/main` (up from round 2's 14 files,
1946/7 — `consumers.test.ts` is a new file).

## `building`'s exit condition

Branch pushed, self-tested (27/27 across four suites, two mutation-verified
properties), PR body already written at build time
(`agents/backend/notebook/2026-09-04-eng038-build.md`) and still accurate —
neither fix changes the feature's externally-visible behavior, so the PR
body needs no revision, same reasoning the SMS-copy-fix hop used for the
same question.
