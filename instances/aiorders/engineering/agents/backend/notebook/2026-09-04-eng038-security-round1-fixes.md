# ENG-038 security-gate round-1 fixes — Finding 1 (critical, auth bypass) and Finding 2 (medium, no rate limit)

Full reasoning behind the `building -> in-review` hop that follows security
gate round 1's `FAIL` verdict; the board-file log entry carries only the
pointer to this file per `conventions.yaml`'s `ticket_log` rule.

## Scope

Both blocking findings from `agents/security/notebook/2026-09-04-findings.md`
/ the ticket's own round-1 security-gate log entry. Security's own fix
instructions were specific enough to implement directly (`backend/agent.md`:
"their findings come back to you with an exact fix... you don't negotiate the
severity down") — no design ambiguity to escalate.

Worktree confirmed fresh before editing: `~/Documents/projects/_eng/aiorders-api`,
`feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`, up to date with
`origin` (round 5's own reviewed commit `125286f`), `git fetch origin` showed
no drift.

## Fix — Finding 1 (critical): `broadcast_message` trusted the request body

`outgoing-communications/actors/consumers.ts#sendBroadcastMessage` took
`campaignId`/`customerId`/`restaurantId`/`emailSubject`/`emailBody`/`smsBody`/
`sendEmail`/`sendSms` straight from the request body, on an action reachable
with `systemTriggered: true` and no credential at all
(`outgoing-communications/index.ts`, pre-existing, untouched). Changed the
call contract to a single `recipientId` — the `broadcast_campaign_recipients.id`
that `broadcast-dispatch/dispatch.ts#resolveRecipient` already claims
(`status = 'claimed'`) before ever calling this:

- `sendBroadcastMessage` now looks up that row, throws if not found or not
  `status === 'claimed'`, then derives `customer_id`/`restaurant_id`/
  `campaign_id`/`step_id` from it — fetches customer, restaurant, and step
  content (`email_subject`/`email_body`/`sms_body`) from the database, never
  from `data`. Consent (`consent_email`/`consent_sms`) is also re-derived from
  the freshly-fetched customer row rather than trusted as a `sendEmail`/
  `sendSms` boolean from the caller, closing the "no re-check of consent at
  all" half of the finding at this layer too (defense in depth — dispatch.ts's
  own pre-check still skips the network call entirely for an already
  opted-out customer, as an optimization, not the authoritative gate).
- `broadcast-dispatch/dispatch.ts`: `SendBroadcastFn`'s type narrowed to
  `{ recipientId: string }`; `resolveRecipient` no longer fetches step content
  itself (dead once `sendFn` stopped taking it) and calls
  `sendFn({ recipientId: recipient.id })`; the exported HTTP-calling
  `sendBroadcastMessage` const's request body narrowed to match.

Does **not** fix `ENG-036` itself (the shared `systemTriggered` gate stays
open for every other actor/action) — noted in both the function docstring and
`README.md` so a later reader doesn't assume more was closed than was.

## Fix — Finding 2 (medium): no bound on audience size or send frequency

`brand-portal/broadcasts.ts`, two new checks, both fail closed (a lookup
error blocks rather than silently skipping the check — this is now a
security control, not a display count):

- `audienceExceedsCap` — a `count: 'exact', head: true` query against
  `customers`, same filter shape `enrollAudience`'s own audience resolution
  uses (`restaurant_id` + the `inactive_days` `.or()` cutoff when that mode is
  selected), compared against `MAX_RECIPIENTS_PER_CAMPAIGN = 10000`. This
  necessarily runs *before* `enrollAudience`'s own per-channel consent filter
  (that filter reads `consent_email`/`consent_sms` per row, not a
  count-only query), so it's a conservative over-estimate: it can reject a
  borderline campaign that would have enrolled fewer consenting customers,
  never under-count. No precedent number exists anywhere in this codebase
  (`ENG-037`'s own migration notes: "No number available yet for typical
  restaurant customer-list size on this platform") — chosen generously enough
  not to block a legitimate large restaurant's own full list, named as a
  runtime constant, raisable without a schema change. Wired into both
  `createBroadcast` and `updateBroadcast` — `update` can change `audience`
  too, and nothing else re-checks it before a campaign leaves `scheduled` for
  dispatch, so gating only `create` would leave a one-call bypass of the very
  cap just added.
- `tooSoonSinceLastCampaign` — the restaurant's most recent non-`cancelled`
  campaign's `created_at`, rejecting a new one within
  `MIN_CAMPAIGN_INTERVAL_HOURS = 24`. This is the "repeatedly" half of the
  finding's own abuse scenario; the cap above bounds one campaign's size but
  not how often a new one starts. `createBroadcast` gets a hard-coded
  `status: 'scheduled'` and a `scheduled_send_at` that defaults to now, so
  gating creation frequency effectively gates send frequency — there's no
  meaningful "draft that never sends" state to worry about exempting.
  Not wired into `updateBroadcast`: editing doesn't create a new campaign row,
  so it doesn't touch the "how often" dimension at all. A cancelled campaign
  never sent anything, so it's excluded from the lookup (`.neq('status',
  'cancelled')`) — a restaurant that immediately cancels a mistake can retry
  without waiting out the full cooldown.

Both constants exported (`MAX_RECIPIENTS_PER_CAMPAIGN`, `MIN_CAMPAIGN_INTERVAL_HOURS`)
so the test file asserts against the same named value rather than a
duplicated magic number.

## Tests added

- `consumers.test.ts` (19 -> updated in place + 3 new, net still 19 since the
  six pre-existing `sendBroadcastMessage` tests were rewritten to the new
  `{recipientId}` contract rather than added alongside): the six orchestration
  tests now stub `broadcast_campaign_recipients`/`broadcast_campaign_steps`
  and call through `recipientId` instead of spreading raw fields. Three new:
  refuses a non-`claimed` recipient; derives customer/restaurant/content
  strictly from the claimed row while a spoofed `customerId`/`restaurantId`/
  `emailSubject`/`emailBody` sits alongside `recipientId` in the same payload
  (proves the old contract's fields are now inert); honors the customer's own
  DB consent with no caller override available.
- `dispatch.test.ts` (10 -> 11): rewrote the partial-batch-failure test's
  `sendFn` to match on `recipientId` instead of the no-longer-passed
  `customerId`; removed the now-dead `broadcast_campaign_steps` stub from two
  tests (`resolveRecipient` no longer queries that table). One new test
  asserts `sendFn` receives *exactly* `{ recipientId }` — `Object.keys(...)`
  equality, not just a value check — as the direct regression guard for
  Finding 1's own shape.
- `broadcasts.test.ts` (38 -> 42): extended the shared `fakeSupabase` fake
  with `.neq()`/`.limit()` (previously unsupported — nothing had called
  them). Updated the one existing `createBroadcast` success test to stub the
  two new checks. Four new: cap rejection on `create`, interval rejection on
  `create`, a cancelled prior campaign *not* blocking a new one (the fake
  handler implements the `neq` filter generically against a small fixture
  rather than hard-coding the expected outcome, so this test only passes if
  the real code actually calls `.neq('status', 'cancelled')` — verified by
  hand that removing that call would flip this test to fail), and cap
  rejection on `update`.

## Full regression, run fresh per directory (`deno test --no-check`, per
`agents/qa/test-plans/ENG-038.md`'s own recorded `suite_command`)

`brand-portal/` 42/42 (was 38/38), `broadcast-dispatch/` 11/11 (was 10/10),
`outgoing-communications/actors/consumers.test.ts` 19/19 (was 16/16),
`broadcast-unsubscribe/` 6/6, `_shared/broadcastUnsubscribe.test.ts`
(`--allow-env`) 7/7 — no regression anywhere. ENG-038-relevant total: 70/70
(62 pre-existing through round 4 + 8 this round).

Also ran `deno check` on all three touched source files as extra due
diligence (not this project's own `--no-check` `suite_command`):
`dispatch.ts` — zero errors. `broadcasts.ts` — 3 pre-existing errors, all in
`brand-portal/utils.ts` (2x `TS18046` on a `catch (error) { error.message }`
pattern repeated throughout this repo, 1x `TS7006` implicit-any in an
unrelated `.find()` callback), none in `broadcasts.ts` itself, none touched
by this diff. `consumers.ts` — pre-existing `TS18046`s in `services/email.ts`/
`sms.ts`/`whatsapp.ts`/`utils/formatters.ts` (imports, not this diff) plus two
in `consumers.ts` itself at its own `catch (error) { ...error.message }`
blocks (one is `sendBroadcastMessage`'s own, preserved verbatim from before
this diff, same as round 4 recorded for the same line). Same shape round 4
already logged for this exact repo-wide pattern — not filed (would be
automatic-failure #7, an unrelated bundled change).

## Step 6b

Grepped every artifact this hop's change touches or relies on:

- `sendBroadcastMessage` / `SendBroadcastFn` / `broadcast_message` — every
  hit outside the files this diff touches is either this ticket's own history
  (board log, prior notebooks, QA test plan — `location`, not re-litigated)
  or a literal string tag (`trigger_type: 'broadcast_message'` on
  `communication_log` rows, unrelated to the call contract). No other caller
  of `sendBroadcastMessage`/`SendBroadcastFn` exists anywhere else in this
  repo — the only two call sites are the ones this diff already updated
  (`handleConsumerCommunications`'s switch statement, `dispatch.ts`'s own
  `resolveRecipient`/`runDispatchTick`/`claimAndDispatchDueRecipients`
  defaults).
- `MAX_RECIPIENTS_PER_CAMPAIGN` / `MIN_CAMPAIGN_INTERVAL_HOURS` — new names,
  no prior hits anywhere, nothing to reconcile.
- `README.md` — updated in the same commit per this repo's own
  `CLAUDE.md` ("After changing a function, update that function's entry...
  in the same commit"): the `outgoing-communications` and `broadcast-dispatch`
  entries now describe the `recipientId`-only contract; the `brand-portal`
  entry now names both new checks and their constants.

## Commits

Two, each an independent finding (same split round 3 used for three
independent gaps), both pushed to
`origin/feat/ENG-038-broadcast-composer-dispatcher-unsubscribe`:

- `92d1bd4` — Require an already-claimed recipientId for broadcast_message,
  stop trusting the request body (ENG-038). 4 files.
- `63f5635` — Cap recipients per broadcast campaign, enforce a minimum
  interval between campaigns (ENG-038). 3 files (includes `README.md`).

Branch now 19 files vs round 5's 19 (no new file added this round, only
existing ones edited).

## `building`'s exit condition

Branch pushed, self-tested (70/70 across five suites, one new test asserting
the exact `sendFn` payload shape as a direct regression guard, one new test
whose pass/fail is load-bearing on the real `.neq()` call actually happening).
Both findings fixed as specified, neither severity negotiated down. No
externally-visible behavior change to any caller outside this codebase's own
`systemTriggered` path — the PR body from the original build hop
(`agents/backend/notebook/2026-09-04-eng038-build.md`) still describes the
same external surface; the recipientId contract change is internal to this
repo (`broadcast-dispatch` is the only real caller).
