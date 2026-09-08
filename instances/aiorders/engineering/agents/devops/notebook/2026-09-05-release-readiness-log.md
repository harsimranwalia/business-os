# Release-readiness log — 2026-09-05

## ENG-039 — `ready-to-ship → blocked`, PR opened

`continue ENG-039` event pass. `skills/release-runner/SKILL.md` run step by
step, same L1 reading established on `2026-09-04-release-readiness-log.md`
(step 1 is the clock check only; steps 2-3's readiness content still run for
L1, minus the window bullet).

**Step 1 (window):** `restaurant-portal` is L1 (`config/projects.md`,
re-confirmed directly) — no window check applies.

**Step 2 (upstream gates) — all three re-read fresh from the receipt files,
not from the ticket log's own account, all passing:**

- `agents/principal-engineer/reviews/ENG-039.md` — round 1, `verdict: pass`,
  0/10 automatic failures.
- `agents/qa/test-plans/ENG-039.md` — round 1, `last_result: pass`, 14/14,
  all five owned acceptance criteria (AC1-AC5) covered.
- `agents/security/reviews/ENG-039.md` — round 1, `verdict: pass`, 0
  findings.

No migration owed — confirmed `agents/database/migrations/` has no
`ENG-039-*.md`, correct for a pure frontend diff (no `*.sql` anywhere in the
9-file diff).

**Step 3 (readiness gate):**

- *Rollback:* single branch, 3 commits (`9a9ec86` build, `b766b41`/`2f438e0`
  quality-gate coverage), no migration, no stored-state change of its own —
  reverting the merge (once merged) fully undoes it. `deploy-cf.yml`
  (push-to-`main`-triggered, confirmed by reading the workflow file directly)
  re-triggers on a revert and redeploys the prior build — same mechanism and
  same reasoning `ENG-032`'s own release-readiness hop already established
  for this exact repo. Not drilled — no CI dashboard or Cloudflare Pages
  access from this department, the same standing boundary every prior
  `restaurant-portal` release on this board has recorded.
- *Observability* — two points, both pre-existing and outside this diff's
  own code, both written up in full below rather than carried forward with
  the same "still dormant" framing `ENG-037`/`ENG-038` used, because this is
  the ticket that ends the dormancy.
- *Cost:* $0/month — no new dependency (`git diff --stat -- '*.json'
  '*.lock'` confirmed clean at the security gate, not re-run here), bundle
  +1.4% (under the 10%-growth-needs-justification line), no new
  infrastructure.
- *Window:* n/a, L1.

No blocking readiness failure for this ticket's own release — see the two
points below for why "no blocking failure" doesn't mean "nothing to say."

### Observability, in full — the two points worth writing up

**This ticket is the one that turns two previously-dormant gaps live**,
because it is the *only* path to actually create and send a broadcast
campaign. `ENG-037`'s own release-readiness hop and `ENG-038`'s (round 2)
both named risks here and judged them non-blocking specifically because
nothing could reach them yet — no UI existed. That precondition ends the
moment this PR merges and deploys. Both gaps are re-examined here on that
basis, not re-derived from scratch and not waved through on the strength of
the prior hops' own "still dormant" conclusion, which no longer applies to
either.

**1. `BROADCAST_UNSUBSCRIBE_SECRET` is not provisioned.** Checked live this
pass, and checked the *right* store on the second attempt: `select name from
vault.secrets` (`supabase db query --linked`) returns only `resend_api_key`
and `service_role_key` — but `vault.secrets` is the Postgres-side store
`ENG-037`'s cron job reads from, a different mechanism from Supabase Edge
Function secrets (`supabase secrets list --project-ref bmnmnejwdxbcqinqkwko`),
which is what `Deno.env.get('BROADCAST_UNSUBSCRIBE_SECRET')`
(`_shared/broadcastUnsubscribe.ts:39`) actually reads at runtime. The
function-secrets list was read directly (34 entries) — no
`BROADCAST_UNSUBSCRIBE_SECRET` anywhere in it. Confirmed absent at the
correct location, not assumed from checking the wrong one.

Traced the actual failure path rather than asserting one: `hmacKey()`
(`broadcastUnsubscribe.ts:38-50`) throws `BROADCAST_UNSUBSCRIBE_SECRET is not
configured` when the env var is unset. `signUnsubscribeToken` calls it with
no local catch, and `buildUnsubscribeUrl` is called unguarded at the top of
both the email and SMS branches in `sendBroadcastMessage`
(`outgoing-communications/actors/consumers.ts:1045,1076`) — but
`sendBroadcastMessage` itself wraps its whole body in one `try`/`catch`
(`:975`, `:1116-1122`) that logs the error and returns
`{success: false, error: error.message}`. Its caller, `resolveRecipient`
(`broadcast-dispatch/dispatch.ts:209-253`), treats that as any other send
failure: `markRecipient(supabase, recipient.id, 'failed', sendResult.error)`
(`:242`). So the failure is real but **not silent** — it's logged
server-side and persisted as a `failed` recipient row with the exact error
message, which is directly visible in this ticket's own `BroadcastReport.tsx`
recipient-status-counts view. Bounded and self-diagnosable, same shape
`ENG-038`'s own claimed-row-stuck gap already had — but unlike that one,
this is not an edge case: it fires on **every single send**, guaranteed,
until the secret exists. One command closes it (named in the PR and the
merge request); this department does not run it unilaterally — matches
`ENG-037`'s own precedent of leaving the analogous `service_role_key`
provisioning as "a named, out-of-band manual step," not something a
release-readiness hop performs itself on a live production secret store with
no reviewed process for generating the value.

**2. SMS delivery is entirely mocked — new finding, not previously surfaced
at any gate on this family.** Grepped every ENG-037/ENG-038 review, security,
and QA receipt for `mock`/`Mock`/`SMS_PROVIDER`: one hit, unrelated (a test
mocking-convention note). Read `outgoing-communications/services/sms.ts`
directly: `createSMSService()` (`:36-55`) switches on
`Deno.env.get('SMS_PROVIDER')`, but the `twilio`/`messagebird`/`vonage`
branches all log a "not implemented yet" warning and fall through to
`MockSMSService` regardless — those provider classes are commented-out
stubs (`// class TwilioSMSService implements SMSService { ... }`), never
built. `supabase secrets list` confirms no `SMS_PROVIDER` secret is even set
today, so the `default` branch (also `MockSMSService`) is what runs
regardless. `MockSMSService.sendSMS` (`:12-29`) logs to console, waits
100ms, and unconditionally returns `{success: true, messageId: 'sms_mock_...'}`
— every SMS "send" reports success and delivers nothing.

This is materially different from the unsubscribe-secret gap: that one fails
*loudly* (logged, `status: 'failed'`, visible in the report). This one fails
*silently* — `resolveRecipient` sees `sendResult.success === true` and calls
`markRecipient(..., 'sent')` (`dispatch.ts:246`), so `BroadcastReport.tsx`
will show a real "Sent" count for a channel that delivered nothing. There is
no config flag or one-line fix the way the unsubscribe gap has one — this
needs an actual SMS provider integration.

Checked whether this was a known, accepted limitation rather than a genuine
gap before treating it as a finding: `ENG-019`'s own PRD, "Assumed" section —
*"Sizing assumes the existing send services (email/SMS/template) are
reusable as-is"* and, under Cost, *"Run: $0/month expected — reuses the
already-contracted email/SMS delivery."* Checked email against the same
bar for contrast, not just asserted as fine: `createEmailService()`
(`services/email.ts:122-145`) picks `BrevoEmailService` whenever
`BREVO_API_KEY` is set, and it is (confirmed in the live secrets list) — email
is real and working. The PRD's assumption holds for email and does not hold
for SMS; nobody checked the SMS side specifically before this hop, because no
earlier ticket in this family exercised the actual send implementation
(`ENG-037` is schema-only; `ENG-038`'s own gates verified the *code it wrote*
— authz, scoping, the claim/dispatch cycle — not the pre-existing service
implementations it calls into; `ENG-039` is frontend-only and has no reason
to open `services/sms.ts` on its own). The mock scaffolding itself
(`MockSMSService`, the commented-out provider classes, the "TODO: Replace
with actual SMS service implementations" comment) reads as pre-existing
boilerplate, not something written by any ticket on this board — not chased
further than that; the fix is the same regardless of exactly when it landed.

**Disposition: named, not fixed, not blocking.** Neither gap is in this
ticket's own 9-file diff, and neither has a code path in this diff that
could address it — the unsubscribe secret is a production credential this
department does not provision unilaterally, and the SMS mock is a
completely separate function (`outgoing-communications`, last touched by
`ENG-038`, already `verified`) that would need its own scoped ticket to
close. Both are named prominently and in full in the PR body and the merge
request (not just here) so a real test send after merge isn't a surprise,
and both are carried into this file so a future hop doesn't have to
re-derive them.

**The SMS-mock point is not a fresh proposal — checked before filing one,
and an existing row already covers it.** `agents/eng-manager/proposals.md`
already carries a 2026-09-03 (`architect`) row on this exact file, found
while designing this same `ENG-019` family, and a 2026-09-04 correction from
`ENG-038`'s own build hop narrowing it: the three *pre-existing* trigger
call sites (`sendWelcomeOffer`/`sendEveryOrderOffer`/`sendFirstOrderOffer`)
pass `body` where `SMSData` expects `message`, so they throw, get caught,
and log `status: 'failed'` — loud, not silent. That correction also noted,
without spelling out the consequence, that `ENG-038`'s own new
`broadcast_message` action calls `sendSMS` with the correct field and
"does not have this defect." Corrected the row a third time this pass with
the consequence made explicit: not having that bug is exactly what makes
broadcasts the one path where the mock's silent `success: true` is actually
reachable — confirmed by reading both `sendBroadcastMessage` call sites
directly (`consumers.ts:1079`, `{to, message: smsText}`, correct field) and
by tracing the return value through `resolveRecipient` to
`markRecipient(..., 'sent')`. **Not raised as a P0** — no security exposure,
no production incident, and zero campaigns exist yet (`select count(*) from
broadcast_campaigns` / `broadcast_campaign_recipients`, both 0, checked live
this pass), so nobody has been affected by either gap yet. The PRD's own
"assumed reusable as-is" claim being wrong for SMS specifically is already
what the existing 2026-09-03 proposal row is about — not re-filed as its own
observation, since the row corrected above already carries it. One
observation filed instead (`observations.md`, 2026-09-05) on a narrower,
distinct point: that row surviving two corrections across three different
hops without either correction rewriting its own "Why it matters" cell to
match is most of why this hop nearly filed a duplicate proposal instead of
finding and correcting the existing one — worth a habit of restating (or
explicitly reaffirming) "Why it matters" against the corrected facts
whenever a proposal row is corrected a second time, not just appending
another caveat to "What."

**Step 4 (route):** worktree (`~/Documents/projects/_eng/restaurant-portal`)
checked fresh: `git fetch origin` current, `git rev-list --left-right --count
origin/main...HEAD` → `0 3` (0 behind, 3 ahead — no drift), `HEAD` at
`2f438e0` matching the ticket's own frontmatter and all three prior gates'
cited head. `git diff origin/main...HEAD --stat`: 9 files, 1,571 insertions,
0 deletions — matches the security gate's own account exactly. `gh pr list
--head feat/ENG-039-broadcasts-tab-composer-and-report-ui --state all`
confirmed no PR already existed for this branch. `git ls-tree -r origin/main
--name-only | grep -i workflow` found `.github/workflows/deploy-cf.yml` —
**unlike `aiorders-api`/`config-site-builder`, this repo does have CI**, read
directly rather than assumed absent: `on: push: branches: [main]` only, no
`pull_request` trigger. Opening this PR carries no auto-deploy risk;
merging it is what triggers the Cloudflare Pages deploy, same fact
`ENG-032`'s own release-readiness hop already established for this exact
repo, re-confirmed rather than re-cited from memory.

Opened `restaurant-portal` PR #3
(https://github.com/harsimranwalia/restaurant-portal/pull/3). Body: what's
new, all three gates passed with receipt paths, self-test summary, the two
non-blocking code-review findings plus the `EmailEditor` observation, a
prominent "Known limitations at merge time" section covering both gaps
above in full, and out-of-scope items. Depends on `ENG-038` (merged,
verified) — sequencing note only.

Wrote `inbox/2026-09-05-eng039-merge-request.md`, plain `pr_url:` string
(single repo). `time_estimate: ~1-1.5 days` set on the item, mirroring the
ticket's own field. `lib/eng-notify.sh raise` run — `sent: active
2026-09-05-eng039-merge-request.md` at `03:41:22`,
`traces/eng-notify-2026-09-05.log`; stamped `notified: 2026-09-05T03:41:22`
on the item by hand, copied verbatim from the log (this board's own
already-flagged local-time-labeled-as-UTC convention, unchanged here).

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy and the
release record both wait for merge detection on a future pass, per the
skill's own step 4 L1 row / step 7 split.

**This is the `ENG-019` family's last sub-ticket.** Once this PR merges, a
future pass's step-5 merge detection carries `ENG-039` to `shipped`, which —
per the family's own `ADR-003`-class exemption, already used for `ENG-016`
— makes the parent `ENG-019` itself eligible to move `building → shipped`
directly, without its own review/QA/security hops. Not this hop's to
process; noted so the next hop that finds `ENG-039` merged isn't surprised
by the parent also being ready to close out the same pass.

## ENG-040 — `ready-to-ship → blocked`, PR opened

`continue ENG-040` event pass. `skills/release-runner/SKILL.md` run step by
step, same L1 reading established on this project's own file above (step 1
is the clock check only; steps 2-3's readiness content still runs for L1,
minus the window bullet).

**Step 1 (window):** `aiorders-api` is L1 (`config/projects.md`,
re-confirmed directly) — no window check applies.

**Step 2 (upstream gates) — all three re-read fresh from the receipt files,
not from the ticket log's own account, all passing:**

- `agents/principal-engineer/reviews/ENG-040.md` — round 1, `verdict: pass`,
  0/10 automatic failures. One non-blocking finding (the `??`-vs-`||`
  rationale doesn't hold in JS; code correct regardless).
- `agents/qa/test-plans/ENG-040.md` — round 1, `last_result: pass`, 6/6,
  both owned criteria (AC4 in full, AC3's write half) covered; AC5 confirmed
  structural.
- `agents/security/reviews/ENG-040.md` — round 1, `verdict: pass`, 0
  blocking findings; `ENG-022`'s ownership-check dependency independently
  re-derived, not taken on trust.

No migration owed — confirmed `agents/database/migrations/` has no
`ENG-040-*.md`, correct for a diff with zero `*.sql` files (matches the
ticket's own work-breakdown note: this design has no schema change).

**Step 3 (readiness gate):**

- *Rollback:* no migration, no stored-state change of any kind — reverting
  the merge (once merged) fully and safely undoes this diff. Same shape
  `ENG-022`'s own hop on this exact file already established, simpler still
  since this diff doesn't even change existing behaviour (pure addition to
  the `EDITABLE_PAGES` allow-list).
- *Observability:* read `website.ts` directly rather than assuming — both
  `getWebsiteContent` and `updateWebsiteContent` already wrap their full body
  in a try/catch that logs via `console.error` before returning
  `{success: false, error: ...}`, generic over every key in `EDITABLE_PAGES`
  including the new `faqs` one. No new logging mechanism needed; confirmed
  by reading the code, not inferred from the pattern `catering`/`careers`
  established.
- *Cost:* $0/month — diff is `website.ts` + its test file + one README line;
  no manifest touched, no new dependency, no new infrastructure.
- *Window:* n/a, L1.

No blocking readiness failure.

**Step 4 (route):** worktree (`~/Documents/projects/_eng/aiorders-api`)
re-checked fresh, not assumed unchanged since the security hop: `git fetch
origin` current, `HEAD` at `104b057` matching the ticket's own frontmatter
and the security gate's own cited head, `git merge-base --is-ancestor
feat/ENG-040-brand-portal-faq-write-path origin/main` → not merged, no
drift. `git diff origin/main...HEAD --stat`: 3 files, 87 insertions, 5
deletions — matches the security gate's own account exactly. `git status`
clean but for the same long-standing untracked
`supabase/functions/brand-portal/deno.lock` every `aiorders-api` release on
this board has already characterised as benign. `gh pr list --head
feat/ENG-040-brand-portal-faq-write-path --state all` confirmed no PR
already existed for this branch. No `.github/workflows/` on this repo
(re-confirmed) — opening this PR carries no auto-deploy risk.

Opened `aiorders-api` PR #18
(https://github.com/harsimranwalia/aiorders-api/pull/18). Body: what
changed, the known dependency on `ENG-022` verified independently, all three
gates passed with receipt paths, the `deno check`/`deno test` self-test
numbers, the two non-blocking findings (review's rationale note, security's
A04/A05), and what's out of scope (`ENG-041`'s UI, the bot's own read side,
the `catering`/`careers` test-coverage proposal).

Wrote `inbox/2026-09-05-eng040-merge-request.md`, plain `pr_url:` string
(single repo). `time_estimate: under an hour` set on the item, mirroring the
ticket's own field. `lib/eng-notify.sh raise` exited 0, no output; confirmed
sent from the log (`traces/eng-notify-2026-09-05.log`: `sent: active
2026-09-05-eng040-merge-request.md`, `16:51:18`); stamped `notified:
2026-09-05T16:51:18` on the item by hand, copied verbatim from the log,
same standing practice this file's own prior entries use.

Ticket set `blocked`, `blocked_on: approver`, `blocked_from: ready-to-ship`,
`owner: devops → approver`, `links.pr` set. No G3 — L1 has none; the PR
merge is the human gate. No release record yet — L1's actual deploy (a
manual `supabase functions deploy` after merge, same as every prior
`aiorders-api` release on this board) and the release record both wait for
merge detection on a future pass, per the skill's own step 4 L1 row / step 7
split.

**This is `ENG-021`'s first sub-ticket.** `ENG-041` (frontend, the FAQ
editor UI) stays `ready`, still waiting on this ticket per its own
`depends_on: [ENG-040]` — this hop doesn't clear that dependency, since
`depends_on` resolves on `verified`, not on a merge request being raised.
Not this hop's to process; noted so the next hop isn't surprised `ENG-041`
is still sitting at `ready`.
