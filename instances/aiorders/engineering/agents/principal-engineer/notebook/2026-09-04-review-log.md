# Review log — 2026-09-04

## ENG-033 (round 2, aiorders-api) — FAIL

Combined review+quality hop. Worktree confirmed on
`feat/ENG-033-catering-request-order-capture-endpoint@b9a22a2`, clean aside
from the standing unrelated untracked `deno.lock`. `git fetch` first, then
`git diff origin/main...HEAD --stat`: still 2 files, 59 insertions/1
deletion — the same shape round 1 reviewed, now with `b9a22a2` folded in.
Checked whether `origin/main` moving in the meantime mattered rather than
assuming it didn't: `git log HEAD..origin/main` shows only `ENG-013`/
`ENG-015`'s merged commits since this branch's base, and
`git diff HEAD...origin/main --stat` confirms neither touches
`catering-request/` or `brand-portal/website.ts`. No rebase needed, no
stale-sibling risk.

**Automatic-failure scan: 1/10.** Re-run fresh against the full current
diff rather than carried forward from round 1's own 0/10 — a fix commit
changes what's on the branch, so the scan runs again in full:
secret/credential clean; no new try/catch; `isValidSelections(selections:
unknown)` still uses `unknown`, still unexported; no new query; no new
dependency; no drive-by refactor; no commented code/TODO; the insert still
goes through `supabase.from("catering").insert(...)`; no auth/payment/
deletion path touched. One hit, below.

**Blocking finding (automatic failure #3, "missing test on a bug fix").**
Round 1 found a real, confirmed, reachable defect: a present-but-non-string
`note` skipped `isValidSelections`'s length check entirely and reached
`restaurant-portal`'s `CateringDetailModal`, which renders it as a bare JSX
child with no error boundary anywhere in that app — throwing on render,
reachable by anyone through this unauthenticated public endpoint. `b9a22a2`
fixes the logic exactly as specified, re-verified against the current diff
rather than trusted from either the review-round or fix-round hop's own
account:

```
index.ts:176: if (note !== null && note !== undefined && (typeof note !== 'string' || note.length > MAX_NOTE_LENGTH)) return false;
```

That's the correct fix, symmetric with `name`'s strictness, cross-checked
again against the design's `## Data` section (`"note": string | null`). But
it ships with no regression test anywhere: `catering-request/` has zero
test files (`find . -iname "*.test.ts"` across the repo lists every other
function's coverage — `brand-portal/*.test.ts`,
`admin-portal/handlers/*.test.ts`, `platform-customer-auth/*.test.ts`,
`restaurant-portal-onboarding/*.test.ts` — and none for this one),
`isValidSelections` isn't exported, and nothing anywhere in the repo
asserts the note-rejection behaviour this fix adds.

`engineering-standards.md` states this with no qualifier: "Every bug fix
ships with the regression test that would have caught it. No exceptions —
this is the single highest-leverage rule in this document," restated
verbatim as automatic failure #3. There is no infrastructure excuse
available, either — checked empirically this round rather than assumed:
`deno test supabase/functions/platform-customer-auth/validation.test.ts`
ran clean, 13/13, with zero setup and no `deno.json` anywhere in the repo.
And this repo carries same-day, directly-on-point precedent for exactly
this shape of function: `platform-customer-auth/validation.ts` +
`validation.test.ts` unit-tests a pure, synchronous boundary-validation
function (`validatePhoneStrict`) with `Deno.test`/`assertEquals`, covering
exactly this edge-case class — null, undefined, wrong-type input.
`isValidSelections` is architecturally identical to `validatePhoneStrict`:
same repo, same day, same shape of pure predicate over untrusted input —
and is the only function like it on this board with zero coverage, despite
already having caused one confirmed defect.

Worth naming directly, because it's this board's own closest precedent and
points at the exact gap: `ENG-032`'s round 1 was also "bug fix, no test" (a
silent `...content`-spread ordering bug in `CateringPageForm.tsx` that wiped
`orderFormEnabled`/`fulfillmentCopy` on save) — and *that* ticket's own
round-2 fix hop closed it by adding `CateringPageForm.test.tsx`, mutation-
verified, same day, same board. `ENG-033`'s fix hop fixed the logic but
didn't take that same second step.

**Specific fix:** export `isValidSelections` from `catering-request/
index.ts` (or split it into its own `validation.ts` alongside `index.ts`,
mirroring `platform-customer-auth`'s own split — either shape is fine,
no preference), add `catering-request/index.test.ts`, and cover at
minimum:

- The round-1 regression itself: a `note` that's an object or a number is
  rejected.
- The design's own named boundaries: 200 elements accepted, 201 rejected;
  non-integer or non-positive `quantity` rejected; non-string `name`
  rejected; `note` at exactly 500 chars accepted, 501 rejected; `note:
  null` and `note` omitted both accepted.
- One fully-valid input returning `true`.

Per `engineering-standards.md`'s mutation-testing rule, at least the
note-rejection case needs to be seen red for the right reason before this
is evidence: revert `b9a22a2`'s one line, confirm that specific case fails
and no other case does, then restore.

**Two non-blocking notes, carried forward unchanged from round 1 —
independently re-checked against the current diff rather than assumed
still true, since neither line was touched by the fix:**

- An empty `name: ""` still passes (neither "missing" nor "non-string" per
  the letter of the design's table) — renders as a blank list item, no
  crash, possibly intentional.
- An empty `selections: []` with `action_type: 'QUOTE_SUBMITTED'` still
  passes and yields `status: 'Quote Generated'` with zero items — the
  design's validation table doesn't name this invalid either.

**One style preference, still not blocking:** the selections-validation
block still sits after "Normalize data" rather than grouped with the other
two early boundary checks (`restaurant_id`, `source`). Letting this go,
same reasoning as round 1 — the check is genuinely coupled to the
`QUOTE_SUBMITTED` branch, not a universal gate like the other two.

**One new non-blocking traceability note.** `website.ts`'s own new comment
cites ADR-009 directly ("Owner opt-in for the structured online order form
(ADR-009). Off unless explicitly set true.") — confirmed correct this
round, not just claimed: read `restaurant-portal`'s already-shipped copy of
the same interface straight from `origin/main` in the department's own
`_eng` worktree (never the human's checkout), and it matches field-for-
field, including that exact comment text. But the ticket's own
`links.adrs` frontmatter still names only `ADR-008`. Not a code defect —
worth adding `ADR-009` to that list at the next frontmatter touch.

**Good work, unchanged from round 1 and now independently re-confirmed
rather than re-asserted:** the conditional spread
(`...(derivedStatus !== undefined ? { status: derivedStatus } : {})`) still
keeps "never touch status when action_type is absent" exactly right with no
extra branching; every boundary constant (`MAX_SELECTIONS = 200`,
`MAX_NOTE_LENGTH = 500`, the two `VALID_ACTION_TYPES` literals) matches the
design's table value-for-value, checked this round rather than assumed
unchanged from round 1.

**Verdict:** fail, round 2. No receipt written, `links.review` stays
untouched. QA's hop discarded this round too — a missing-test finding makes
a real quality-gate run premature, same precedent `ENG-032`'s own round 1
already set for this identical failure class. Ticket stays `building`,
next hop is the fix (add the test), then review round 3.

## ENG-033 (round 3, aiorders-api) — REVIEW pass, QUALITY fail

Combined review+quality hop — the first time on this ticket both halves
actually ran, since rounds 1 and 2 both failed at review and QA's result
was discarded both times per `code-review-gate/SKILL.md` step 9. `git
fetch`, `git diff origin/main...HEAD --stat`: 4 files, 138/1 — `index.ts`
and `website.ts` unchanged since round 2 (confirmed byte-identical on the
lines already reviewed), plus the two new files round 2 asked for:
`validation.ts` (the extracted `isValidSelections`) and `index.test.ts`
(12 cases).

**Automatic-failure scan: 0/10.** Round 2's sole finding — missing test on
the round-1 bug fix — is closed: `index.test.ts` covers the regression by
name plus every boundary the design names.

**Did not take the fix hop's "12/12 pass" on trust — mutation-tested it
myself.** Round 2 explicitly asked for this ("at least the note-rejection
case needs to be seen red for the right reason before this is evidence")
and the fix hop's own log didn't record having done it. Reverted
`validation.ts`'s note check to the exact round-1 buggy line, ran `deno
test`: 11 passed, 1 failed — only the note-rejection case, `+false/-true`,
the right test failing for the right reason. Restored via `git checkout
--`, re-ran clean. This is now real evidence, not an inference from the
diff reading correct.

**Lint reconciled across all four touched files for the first time this
round** (prior hops each checked 3 or 2 files at a time) — 11 problems, 0
new; the arithmetic across every prior hop's own count (10 at the two-file
stage, 6 across the three `catering-request` files post-split) sums to
exactly 11 once `website.ts` is added back in, so nothing was missed by
checking file subsets separately in earlier rounds.

**One new non-blocking note:** `validation.ts`'s header comment says it
"mirrors platform-customer-auth's own index.ts + handler.ts split" — checked
per the comment-accuracy standard rather than taken at face value.
`platform-customer-auth` does have that split and does call `Deno.serve()`
at module scope, so the stated *reason* is correct, but the file actually
mirrored (and the one round 2's own review named) is `platform-customer-auth/
validation.ts`, not `handler.ts` — `catering-request` has no handler.ts
equivalent; the whole handler stays inline in `index.ts`. Names the wrong
sibling as precedent, doesn't mislead about behaviour. Not blocking.

**Verdict: PASS on code review.** Full writeup:
`agents/principal-engineer/reviews/ENG-033.md`, `links.review` set.

**But the quality gate — run for the first time on this ticket this
round — found its own gap, unrelated to anything review checks.** AC-5/6/7
are implemented by the status-derivation branching in `index.ts:247-264`
(reads `action_type`, decides `derivedStatus`, decides whether `selections`
is stored or force-nulled) — and nothing tests that branching. `index.
test.ts` imports only `isValidSelections`; the derivation logic has no
exported entry point of its own, same reason `isValidSelections` needed
extracting in the first place. Traced it by hand against the design's own
table and it's correct — but per `agents/qa/agent.md`'s own refusal list,
"manually verified" doesn't stand in for a test when automation could
reach the thing, and this logic has no I/O of its own, so it can be
extracted and tested the same way `isValidSelections` just was. Full
finding and the specific fix: `agents/qa/test-plans/ENG-033.md`.

Ticket returns to `building` on the quality finding, not the review one —
review's own PASS stands and does not need re-litigating next round, only
re-confirming fresh against whatever diff the extraction produces, same as
every prior round's own practice on this ticket.

## ENG-038 (round 1, aiorders-api) — FAIL

Combined review+quality hop, first round — the backend build hop
(`continue ENG-038`, previous pass) stopped at `building` rather than
transitioning to `in-review` itself (a narrower reading of "a pass stops
after building" than `ENG-037`'s equivalent hop used, which transitioned as
it exited); this hop performs both that recognition and the review+quality
work itself, since nothing about that choice changes what a fresh session
reviewing the diff for the first time does. Worktree
(`~/Documents/projects/_eng/aiorders-api`) checked fresh, not trusted from
the trigger's checkpoint: `git fetch origin main`, branch
`feat/ENG-038-broadcast-composer-dispatcher-unsubscribe` at `4f0dccf`, two
commits ahead of `origin/main` (`64baabf`, `ENG-037`'s own merge), clean
except the three long-standing untracked `deno.lock` files (new instances
of the same class every recent pass on this repo has already noted — see
this pass's own proposal on `proposals.md`). `git diff origin/main...HEAD
--stat`: 14 files, 1946/7.

**Automatic-failure scan: 0/10.** No secret (grepped the diff and both
commit messages for key/token/secret/bearer/PEM patterns); no silent
exception swallow *of the automatic-failure kind* — see the non-blocking
finding below, which is a logging gap inside a deliberate catch-all, not an
empty catch; not a bug fix; no untyped public interface beyond the
project's own existing `data: any` idiom, matched consistently; `list_
broadcasts` paginates; `deno.json`s for the two new functions add no new
dependency, both mirror the existing `broadcast-dispatch`/`brand-portal`
import maps exactly; no unrelated refactor riding along (confirmed: every
touched file outside the four new function directories is an additive,
scoped change — `consumers.ts` adds one new `case`/function, `index.ts`
adds one new routing block, `README.md` documents exactly this diff); no
commented-out code or unowned TODO; no datastore write bypassing the
project's data layer (every write goes through the same `supabase.from()`
client every sibling handler uses); the one auth-adjacent path with no
failure-case test is examined below and judged not a hit on this item
specifically (the negative-consent path IS tested — see `dispatch.test.ts`).

**Read against the design and the three ADRs — this is where round 1
failed.** Read `agents/architect/designs/ENG-019-restaurant-marketing-
broadcasts.md`'s `## Interfaces` section and `ADR-018`/`ADR-019`/`ADR-020`
directly, not the ticket's paraphrase.

**Blocking finding — `consumers.ts`'s new `sendBroadcastMessage` puts
"Reply STOP" into the SMS body, which `ADR-020` explicitly decided this
codebase cannot honor.** `outgoing-communications/actors/consumers.ts`,
the new SMS branch:

```
const smsText = `${replaceTemplateVariables(data.smsBody!, templateVariables)} Reply STOP or visit ${unsubscribeUrl} to unsubscribe.`
```

`ADR-020`'s own Alternatives table considered and rejected exactly this:
*"SMS opt-out via inbound 'STOP' reply parsing — `outgoing-communications/
services/sms.ts` is fully mocked — no real provider, no inbound-message
path exists at all in this codebase. Building one is separate work the
PRD's own Non-goals already exclude... The same link, in the SMS body
text, covers SMS the same way it covers email."* Confirmed live, not
assumed: `services/sms.ts` is still `MockSMSService` only (`SMS_PROVIDER`
switch on `twilio`/`messagebird`/`vonage` all fall through to the mock,
with a `TODO` naming each as unimplemented) — there is no inbound path of
any kind, mocked or real, for a reply to reach. A customer who replies
STOP today gets nothing: no code anywhere in this diff or the existing
tree consumes an inbound SMS. The link-flip path (the actual chosen
mechanism) is correctly implemented and does work — this finding is
specifically about the extra promise the copy makes on top of it.

Why this is blocking rather than a copy nitpick: (1) it directly
contradicts an accepted ADR written for this exact ticket, the same day —
not a stale doc, not an inference; (2) it is a customer-facing promise the
system cannot keep today, in an anti-spam-sensitive feature the PRD's own
Risks section already flags for CASL exposure; (3) even under a future
real SMS provider, a carrier-level STOP intercept (where some aggregators
auto-block delivery) would still never flip this app's own `consent_sms`
source of truth, so the report and every other automation would keep
treating that customer as reachable — a second-order inconsistency the
ADR's reasoning implicitly heads off by choosing link-only. **Specific
fix:** drop `Reply STOP or ` from the SMS body, leaving `... visit
${unsubscribeUrl} to unsubscribe.` — the link alone is what `ADR-020`
actually specified and what the rest of this diff correctly builds.

**Two non-blocking findings, both specific and actionable:**

**F1 — `_shared/broadcastUnsubscribe.ts`'s `verifyUnsubscribeToken`
catches every exception identically, including a missing-configuration
one, with no log line.**

```
} catch {
    return null
}
```

This function's own `hmacKey()` throws `'BROADCAST_UNSUBSCRIBE_SECRET is
not configured'` when that env var is unset — which it currently is
(named as a manual prerequisite in `agents/backend/notebook/2026-09-04-
eng038-build.md`, not yet provisioned). Until it is, every single
unsubscribe click throws inside `hmacKey()`, is caught here identically to
a genuinely malformed/forged token, and returns `null` — `broadcast-
unsubscribe/index.ts` then serves the same "This link is no longer valid"
page to every customer, and nothing anywhere logs *why*. This is not the
automatic-failure #2 shape (an empty catch that discards a bug silently
while the surrounding code carries on as if nothing happened) — returning
null on a malformed token is the correct, deliberate fail-closed behaviour
for an untrusted public caller. The gap is narrower: the catch-all doesn't
distinguish "expected, no log needed" from "server misconfiguration,
should be loud." **Specific fix:** check
`Deno.env.get('BROADCAST_UNSUBSCRIBE_SECRET')` explicitly at the top of
`verifyUnsubscribeToken` (or let `hmacKey()`'s specific error propagate
past the catch) and `console.error` that case distinctly before returning
null — same shape `broadcast-dispatch/index.ts` already uses for its own
required env vars (`Deno.env.get(...)!`, fails loud at cold start rather
than masking).

**F2 — `dispatch.ts`'s `enrollAudience` has no failure path if the
recipient-row insert itself fails.** If `supabase.from('broadcast_
campaign_recipients').insert(recipientRows)` errors (transient DB issue,
etc.), the function `console.error`s and returns — but the campaign was
already flipped to `active` by the caller's own atomic promotion UPDATE,
and nothing rolls that back or retries. The campaign then sits at
`active` with zero recipient rows, indistinguishable in `get_broadcast_
report` from "still resolving" and — unlike the genuine-empty-audience
case, which explicitly sets `status: 'completed'` — with no terminal state
and no automatic retry, since `promoteDueCampaigns`'s own `WHERE status =
'scheduled'` can never match it again. Narrow (the insert only fails on a
genuine DB error, not a normal input shape) and not reachable by anything
this round's own tests exercise, so not blocking — named because it's the
one gap in an otherwise carefully-reasoned dispatcher, the same class of
"insert half of a two-step write can fail after the first half commits"
the design's own Risks section reasons about elsewhere (the `claimed`-
stuck-row gap). **Specific fix, if picked up:** either retry once, or set
a distinguishable state (e.g. write `error_detail`-equivalent on the
campaign row, or a dedicated `enrollment_failed` status) so this doesn't
read as a legitimate empty campaign forever.

**Test quality: independently re-run, not trusted from the build hop's
own report.** `deno test --no-check`, run fresh from within each
function's own directory (the shared `supabase/functions/` root fails to
resolve `npm:@supabase/supabase-js@2` — a resolver-mode quirk, not a code
issue): `brand-portal/broadcasts.test.ts` 6/6, `broadcast-dispatch/
dispatch.test.ts` 4/4, `brand-portal/offers.test.ts` 9/9 (no regression) —
matches the build hop's own account exactly. **Mutation-tested the claim-
idempotency test myself**, the single highest-stakes correctness property
on this ticket (the design's Risks call it load-bearing, not incidental):
temporarily removed `claimRecipients`'s `.eq('status', 'pending')` guard
(`dispatch.ts:182`), re-ran — `claimRecipients under a simulated
overlapping tick never claims the same row twice` failed exactly as
expected (tick B claimed all 3 rows instead of 0), confirming the test is
wired to the actual threat, not just to its own assertion; restored via
the backup, re-ran clean. Did not independently re-run the cross-tenant-
leak mutation in `broadcasts.test.ts` (build hop's own account already
describes doing this, and the fake's `restaurantFilterMatches` logic reads
correctly on inspection) — flagged here so a future round knows this one
specific claim was taken on the build hop's word, unlike the claim
idempotency one.

**Coverage gaps found (QA side of this hop, discarded with the rest of
this round — recorded so the next quality-gate round doesn't have to
re-derive them):** `pause_broadcast`/`resume_broadcast`/`cancel_broadcast`
have no test coverage in `broadcasts.test.ts` — matches what the ticket's
own Tests section scoped (it names five scenarios, none of which are
these three), so not a gap against this ticket's own stated commitment,
but worth a look given `cancel_broadcast`'s non-trivial recipient-row
mutation. `promoteDueCampaigns`/`enrollAudience` (the promotion+enrollment
half of the dispatcher — audience resolution, the `inactive_days` cutoff,
the enrollment-time consent OR-filter, the empty-audience-completes path)
have zero test coverage anywhere in `dispatch.test.ts`, which only
exercises the claim+resolve half. Traced the logic by hand against the
design and it reads correct, but per `agents/qa/agent.md`'s own refusal
list this doesn't stand in for a test where automation could reach it —
worth the next quality-gate round's attention regardless of how round 1's
own blocking finding gets fixed.

Live-schema cross-checks run this round (not re-derived from `ENG-037`'s
own account where that ticket already confirmed a fact — see its own
Notes): `communication_log.trigger_type` is `character varying(50)`, no
CHECK constraint — `'broadcast_message'` fits with room to spare, no
migration owed for the new value. `customers.email`/`.phone` (`text`),
`restaurants.name` (`text not null`), `orders.total_amount`
(`numeric(10,2)`) all match how the new code reads them. The new
migration's `alter table ... drop constraint ... add constraint` correctly
targets the live constraint's actual name and superset-extends its actual
value list (`broadcast_campaign_recipients_status_check`, confirmed via
`supabase db dump --linked --schema public`, this session) — no data-loss
risk, no stale name.

**Verdict: FAIL, round 1.** No receipt written (`agents/principal-
engineer/reviews/ENG-038.md` does not exist), `links.review` untouched —
per `code-review-gate/SKILL.md` step 8/9, a receipt is written on pass
only. QA's own result this round (the coverage gaps above, the
independent test re-run, the mutation test) is discarded with it, per the
same skill's step 9 — the code is changing, so a real quality-gate run
against the current diff would be premature; no `agents/qa/test-plans/
ENG-038.md` written either. Ticket returns to `building`, owner `backend`.
Next hop: drop `Reply STOP or ` from the SMS body (one line,
`consumers.ts`), then review round 2 — F1/F2 above are non-blocking and
don't need to be fixed to pass, though F1 in particular is cheap enough
that fixing it in the same pass as the blocking line would avoid a third
round for something already fully specified.

## ENG-038 (round 2, aiorders-api) — FAIL

Combined review+quality hop. Worktree (`~/Documents/projects/_eng/aiorders-api`)
re-checked fresh, not trusted from the trigger's checkpoint: `git fetch origin
main`, branch `feat/ENG-038-broadcast-composer-dispatcher-unsubscribe` at
`ede0e1e`. `git log HEAD..origin/main` empty and `git diff HEAD...origin/main
--stat` empty — no drift, nothing landed on `main` since round 1 that could
touch this branch. `git diff origin/main...HEAD --stat`: still 14 files,
1946/7 — the same shape round 1 reviewed. `git show --stat ede0e1e` confirms
the only change since round 1 is exactly what the ticket log claims: one
file (`outgoing-communications/actors/consumers.ts`), one insertion, one
deletion.

**Automatic-failure scan: 1/10.** Re-run fresh against the full current diff
rather than carried forward from round 1's own 0/10 — a fix commit changes
what's on the branch, so the scan runs again in full: secret/credential
clean (the one-line diff is a string literal edit, nothing else); no new
exception handling; `any`/untyped — unchanged; `list_broadcasts` still
paginates; no new dependency; no unrelated refactor (`git show --stat
ede0e1e` confirms exactly one file, one line changed); no commented code/
TODO; no datastore write bypassing the data layer; no new auth/payment/
deletion path. One hit, below.

**Blocking finding (automatic failure #3, "missing test on a bug fix").**
`ede0e1e`'s own commit message frames itself correctly: it is a fix for the
specific defect round 1 found blocking (the SMS text's false "Reply STOP"
claim, contradicting `ADR-020`). Read the corrected line directly rather
than trusted from the commit message: `consumers.ts`'s `sendBroadcastMessage`
now reads `` `${replaceTemplateVariables(data.smsBody!, templateVariables)}
Visit ${unsubscribeUrl} to unsubscribe.` `` — correct, matches the email
sibling's own `\n\nUnsubscribe: ${url}` treatment exactly. But this fix ships
with no regression test anywhere: `sendBroadcastMessage` is not exported,
`outgoing-communications/` has zero test files of any kind (confirmed:
`find supabase/functions/outgoing-communications -iname "*.test.ts"` returns
nothing), and nothing in this diff or the existing tree asserts the
corrected copy — or would fail against the old, buggy line.
`engineering-standards.md` states this with no qualifier: "Every bug fix
ships with the regression test that would have caught it. No exceptions —
this is the single highest-leverage rule in this document," restated
verbatim as automatic failure #3.

This is the same shape as this board's own `ENG-033` round 2 finding, same
day: a defect caught at review round 1, fixed at the next build hop without
a regression test, failed again at round 2 for exactly that omission. That
precedent also closes off the "no test infra exists here" reading as an
excuse — checked empirically this round rather than assumed, same as
`ENG-033`'s own round 2 did: `find supabase/functions -maxdepth 1 -iname
deno.json` returns **nothing at all**, anywhere in this repo, including
every directory that already has passing tests (`brand-portal`,
`platform-customer-auth`, `catering-request`, `admin-portal/handlers`,
`restaurant-portal-onboarding`) — `deno test` needs no per-directory config
to run here, confirmed by running it. A test file under
`outgoing-communications/` is exactly as turnkey as it was everywhere else
in this repo.

**Specific fix:** extract the SMS (and, for symmetry, email) body
construction out of the inline template literals in `sendBroadcastMessage`
into a small, pure, exported function — e.g. `buildBroadcastSmsBody(smsBody:
string, templateVariables: Record<string, string>, unsubscribeUrl: string):
string` — and add a test file (`consumers.test.ts`, first for this
directory) asserting: the output does not contain `STOP` or `Reply`, and
does contain the exact `Visit {url} to unsubscribe.` sentence. Per the
standards' mutation rule, see it red for the right reason first: revert
just the `Visit` line back to the old `Reply STOP or visit` text, confirm
only that assertion fails, then restore.

**Two non-blocking findings, carried forward from round 1, un-relitigated
since neither line is touched by `ede0e1e`** (confirmed via `git show
--stat` above — only `consumers.ts` changed, and F1/F2 are in
`_shared/broadcastUnsubscribe.ts` and `broadcast-dispatch/dispatch.ts`
respectively): F1, the `verifyUnsubscribeToken` catch-all with no log line
distinguishing a missing-config failure from a malformed token; F2,
`enrollAudience`'s no-rollback path if the recipient-insert itself errors
after the campaign is already flipped `active`. Both stand exactly as round
1 described them.

**Test quality: independently re-run, not trusted from the fix hop's own
report.** `deno test --no-check`, run fresh from within each function's own
directory: `brand-portal/broadcasts.test.ts` 6/6, `broadcast-dispatch/
dispatch.test.ts` 4/4, `brand-portal/offers.test.ts` 9/9 — matches exactly,
no regression.

**Coverage gap found (QA side of this hop, discarded with the rest of this
round per `code-review-gate/SKILL.md` step 9 — recorded sharply, not
softened, so the next quality-gate round doesn't treat it as optional).**
Read `dispatch.test.ts` directly this round rather than trusted from round
1's own account: its four tests (`claimRecipients` idempotency,
`resolveRecipient`'s opted-out exclusion, partial-batch-failure isolation,
`claimAndDispatchDueRecipients` on an empty batch) exercise only the
claim/resolve half of the dispatcher. `promoteDueCampaigns` and
`enrollAudience` — the scheduled-campaign promotion and audience-resolution
logic — have **zero** test coverage anywhere in this diff. This is not a
peripheral gap: `enrollAudience`'s `audience_mode === 'inactive_days'`
cutoff-vs-`'all'` branch is the literal implementation of AC3 (audience
selection), its per-`(customer, step)` fan-out with `due_at = enrolledAt +
delay_hours` is the literal implementation of AC2 (drip, once per customer,
each step at its own delay), and `promoteDueCampaigns`'s `WHERE status =
'scheduled' AND scheduled_send_at <= now()` promotion query is the literal
implementation of AC1's schedule/immediate distinction. Per `agents/qa/
agent.md`'s own quality-gate definition ("fails when...an acceptance
criterion has no passing test"), this is a real, load-bearing risk for the
next quality-gate round, not a nice-to-have — sharper framing than round
1's own "worth the next round's attention," because tracing it this round
shows it's three of the ticket's seven acceptance criteria, not a
peripheral corner. `pause_broadcast`/`resume_broadcast`/`cancel_broadcast`
remain untested in `broadcasts.test.ts` too, carried forward unchanged from
round 1 — still not blocking, no AC names them specifically, same judgment
as round 1.

**Notebook self-note.** This is the second time (after `ENG-033` round 2's
`isValidSelections`) a review round's fix has needed "extract private logic
into an exported, pure function so it can be unit-tested" as its specific
remedy. Not yet a third occurrence — no standards promotion this round —
but the next one anywhere on this board should go straight to
`engineering-standards.md` rather than being treated as ticket-specific
again.

**Verdict: FAIL, round 2.** No receipt written (`agents/principal-engineer/
reviews/ENG-038.md` does not exist), `links.review` untouched. QA's own
result this round (the coverage-gap finding above, the independent test
re-run) is discarded with it, per `code-review-gate/SKILL.md` step 9 — the
code is changing again, so a real quality-gate run against the current diff
would be premature; no `agents/qa/test-plans/ENG-038.md` written. Ticket
returns to `building`, owner `backend`. Next hop — both fully specified now
so a third round isn't needed for either: (1) extract and test the SMS/
email body construction as described above, (2) add coverage for
`promoteDueCampaigns`/`enrollAudience` in `dispatch.test.ts` — at minimum a
due-vs-not-yet-due promotion check, both audience-mode branches, the
enrollment-time consent OR-filter, the per-step fan-out's `due_at` math, and
the empty-audience-completes-immediately path.

## ENG-038 (round 3, aiorders-api) — REVIEW pass, QUALITY fail

Combined hop. Worktree re-checked fresh: `git fetch origin main`; `git log
HEAD..origin/main`/`git diff HEAD...origin/main --stat` both empty, no
drift. `git diff origin/main...HEAD --stat`: 15 files, 2237/7 (round 2 was
14 files, 1946/7). `git diff ede0e1e..HEAD` confirms the only change is
exactly what the ticket log claims: `consumers.ts` (+18/-2), the new
`consumers.test.ts` (24 lines), `dispatch.test.ts` (+251). `dispatch.ts`
itself is untouched — byte-identical to what round 1 reviewed.

**Automatic-failure scan: 0/10**, re-run fresh. Round 2's own finding
(missing test on the SMS-copy bug fix) is closed: `buildBroadcastSmsBody`/
`buildBroadcastEmailBody` extracted as pure exported functions (read the
full surrounding function, `consumers.ts:881-1020`, not just the diff
hunk — confirmed byte-identical output to round 2's fix, pure extraction,
no behaviour change), `consumers.test.ts` asserts the corrected copy and
the absence of "STOP"/"Reply".

**Independently re-ran the full suite fresh:** `broadcasts.test.ts` 6/6,
`offers.test.ts` 9/9, `dispatch.test.ts` 10/10, `consumers.test.ts` 2/2 —
27/27, matches the backend's own report exactly.

**Two independent mutation tests, deliberately different properties from
what the fix hop's own trace already covered** (they mutated the
promotion-date filter and the due_at delta — picking different ones gives
independent coverage instead of re-confirming the same two):

- Reverted `buildBroadcastSmsBody` to the round-1 buggy text via a scripted
  edit (`/tmp/consumers.ts.bak` backup, restored after) — exactly the SMS
  test failed (1 passed/1 failed), email test untouched. Restored, `git
  diff --stat` empty, re-ran clean.
- Flipped `enrollAudience`'s consent filter from default-contactable
  (`!== false || !== false`) to default-excluded (`=== true || === true`)
  — exactly the "excludes only when both explicitly opted out" test failed
  (9 passed/1 failed). This is the ticket's most compliance-sensitive
  property (CASL exposure named in the PRD's own Risks) and it's now proven
  test-covered under mutation, not just read-as-correct. Restored, `git
  diff --stat` empty, re-ran clean.

**F1/F2 carried forward unchanged** (neither file touched this round).
**F2 given a full line-trace for the first time** (rounds 1-2 both only
"traced by hand" at the "reads correct" level, never against failure
propagation): `promoteDueCampaigns` flips ALL due campaigns to `active` in
one batched `UPDATE...RETURNING` *before* the `for` loop over them starts.
Nothing between there and `broadcast-dispatch/index.ts`'s own outer
`try/catch` wraps the loop or `enrollAudience` itself — only
`resolveRecipient` has per-item isolation. A thrown exception (not a
returned `{error}` — narrowed by `create_broadcast`'s own input validation,
but not impossible on a genuine network fault) at campaign N of an
M-campaign tick aborts enrollment for N+1..M, which are already `active`
in the DB and will never be re-selected (`WHERE status = 'scheduled'` no
longer matches). Stuck forever, one generic log line for the whole tick,
no campaign IDs named. Same root cause as F2, same non-blocking
disposition (narrow, no current test reaches it), recorded so whoever picks
up F2 fixes the real blast radius.

**New, low-severity, test-only:** `dispatch.test.ts`'s new `matchesOrExpr`
fake helper splits an `.or()` clause on every literal `.`, including the
one inside an ISO-8601 millisecond suffix — `"...56.789Z".split(".")` is 4
parts, silently dropping `789Z` from the compared value via destructuring.
Doesn't change any assertion's outcome this round (fixture gaps are
day-scale), but would misbehave on a future sub-day-precision test.

**New, non-blocking, low-confidence-it-matters:** no fixture among the six
new dispatch tests uses more than one restaurant, so `enrollAudience`'s own
`restaurant_id` filter has no regression test proving it excludes another
tenant's customers. The design/ticket already reasoned explicitly that
there's no *caller-supplied* cross-tenant vector on this path — a real and
separate point about auth bypass, not about filter regression-safety under
a future refactor. Flagged for completeness, not pressed against a
deliberate design call.

**Still open:** round 1's flag that the `broadcasts.test.ts` cross-tenant
leak mutation was taken on the build hop's word, never independently
mutation-tested. Unchanged code, not picked up this round either — noted so
it doesn't quietly vanish a second time.

**Verdict: PASS on code review.** 0/10 automatic failures, round 2's finding
closed and independently mutation-verified. Full writeup:
`agents/principal-engineer/reviews/ENG-038.md`, `links.review` set.

**But the quality gate — run for the first time on this ticket this round,
since rounds 1–2 both failed at review first — found real gaps, and they're
sharper than anything either prior round named.** Went looking at
`getBroadcastReport` and `broadcast-unsubscribe/index.ts` for the first
time this round (neither appears anywhere in round 1 or round 2's own
coverage-gap paragraphs, both of which focused entirely on the dispatcher's
claim/promote/enroll path — now closed). Found three:

1. **AC4 (blocking).** `broadcasts.ts:560-603`'s redemption/revenue
   matching (offer's `coupon_code` against `orders.promos`, summing
   `total_amount`) — AC4's entire implementation, named as such by the
   code's own comment — has zero test coverage. Both existing report tests
   use `offer_id: null`, so neither ever enters this branch. Confirmed by
   reading both tests in full and grepping the whole repo's test files.
2. **AC5, read half (blocking).** Same function, the `delivery_by_channel`
   loop (`541-552`) — only ever exercised via the empty-array branch.
   Lower risk than (1) (counting, not money arithmetic), still zero real
   coverage.
3. **AC6 (blocking, highest-stakes of the three).** `_shared/
   broadcastUnsubscribe.ts`'s sign/verify pair and `broadcast-
   unsubscribe/index.ts`'s handler have no test anywhere — confirmed via a
   repo-wide grep whose only hit is a test-fixture URL string containing
   the path segment as flavor text, not an actual call into either file.
   This is a public, unauthenticated, consent-mutating endpoint on a
   CASL-flagged feature. Unlike (1)/(2), the sign/verify functions need no
   extraction (already exported, already pure other than one settable env
   var) — only the handler's own branching needs the same
   extract-to-pure-function treatment.

Full findings, exact fix specs, and the acceptance-coverage table:
`agents/qa/test-plans/ENG-038.md`.

**Standards promotion — third occurrence.** The "extract private/inline
logic into a pure exported function for testability" remedy has now been
written three times on this board: `ENG-033`'s `deriveActionStatus`, this
ticket's own SMS/email body extraction (round 2→3, just confirmed above),
and this round's own three new findings. Per `code-review-gate/SKILL.md`
step 10, edited `agents/eng-manager/config/engineering-standards.md`
directly (`## Naming and structure`, new bullet) rather than treating a
fourth occurrence as ticket-specific again.

Ticket returns to `building` on the quality finding, not the review one —
same precedent `ENG-033`'s own round 3 set for this identical shape (review
pass + quality fail → `building`; review's own pass stands, re-confirmed
fresh next round rather than re-litigated from scratch).

## ENG-038 (round 4, aiorders-api) — REVIEW pass, QUALITY fail

Combined review+quality hop, scoped to the diff since round 3's reviewed
commit (`87f3f8c..d13722a`, the three round-3-fix commits) per
`code-review-gate/SKILL.md` step 9 — round 3's own review pass on the base
diff stands, not re-litigated. Worktree fetched fresh, HEAD `d13722a`
matches the ticket log, no drift vs `origin/main`.

**Automatic-failure scan: 0/10**, re-run against this round's diff. F1 (the
`verifyUnsubscribeToken` catch-all) is now closed rather than merely
carried forward — it logs the underlying error before returning `null`.
Traced `broadcast-unsubscribe/index.ts`'s new control flow against the
pre-round-4 version line by line (not just the diff hunks) to confirm the
extraction into `unsubscribe.ts` is behaviour-preserving: same four
response outcomes, same status codes, the `resolvedCustomerId as string`
cast is safe because the pre-check only returns `null` when `customerId`
was already truthy. `brand-portal/broadcasts.ts`'s two extractions are
byte-for-byte copy-moves.

**Two mutation tests on this round's one genuinely new decision shape**
(round 3 already mutation-verified the coupon-matching predicate and the
signature check on this logic *before* extraction — re-mutating the
identical relocated code would be repetition, not new signal):
`decideUnsubscribePreCheck`'s idempotency check (`=== false` → `!== false`)
failed exactly the 2 dependent tests; the missing-customer-id gate
(`!input.customerId` → `input.customerId`) failed exactly the 3 dependent
tests, including the one wired to the actual threat (a request with no
verified token reaching the write path). Both restored via backup, re-ran
clean.

Also ran `deno check` on every file this round's diff touches (not this
project's own `suite_command`, which is `--no-check` — no `deno.json`
exists yet, a standing gap in `projects.md`, not this ticket's to fix, and
not filed again here). `broadcast-unsubscribe/*` and
`_shared/broadcastUnsubscribe.*` check clean; `brand-portal/broadcasts.ts`
surfaces 9 pre-existing errors, all in code this round doesn't touch
(`utils.ts`, test blocks before line 227) — not a new condition, not filed
as a finding (fixing it here would itself be automatic-failure #7).

**Verdict: PASS on code review**, second consecutive pass (rounds 3–4).
`links.review` re-set to `agents/principal-engineer/reviews/ENG-038.md`
(round 4).

**Verdict: FAIL on the quality gate, second consecutive fail** (round 3's
own first verdict on this ticket also failed). Gaps 1–3 (AC4, AC5-read,
AC6) are closed and independently re-verified. **One gap remains, and it
isn't new** — round 3's own report already named it, in the "Not automated"
section under AC5 (write): `sendBroadcastMessage`
(`outgoing-communications/actors/consumers.ts:881-1020`)'s own
`communication_log` insert has zero test coverage anywhere. Round 3 chose
not to number it "because the read half (Gap 2) already fails the gate for
this AC" — a reporting-efficiency call, not a substantive judgement that
the write path is safe untested (unlike AC3's restaurant-scoping note in
the same section, which rests on an actual design reasoning about there
being no caller-supplied cross-tenant vector). The round-3 fix hop closed
the three *numbered* gaps and didn't pick up the parenthetical. Confirmed
by grep that no test anywhere calls this function: `dispatch.ts` exports an
unrelated function of the same name (the injectable HTTP wrapper
`dispatch.test.ts` fakes), so that suite's 10/10 never reaches it, and
`consumers.test.ts` covers only the two pure body-builder helpers this
handler calls, not the handler itself. Filed as Gap 4:
`agents/qa/test-plans/ENG-038.md`.

**Process note, not a ticket finding.** A test-plan report that folds one
still-real gap into another gap's "blocking" status for reporting
efficiency creates a re-emergence risk: the next round can read "3 gaps,
all closed" and stop looking, rather than re-deriving the acceptance table
fresh. Worth QA carrying a harder rule — every acceptance-criterion row
that has zero test gets its own numbered gap even when another row on the
same AC is already failing — but this is a one-off noticing, not a pattern
across three tickets yet, so an observation
(`agents/eng-manager/observations.md`), not a proposal.

Per `code-review-gate/SKILL.md` step 9 and this ticket's own round-3
precedent: **1 transition** — `in-review → building`, owner
`principal-engineer → backend`. Not a "third failed round" escalation:
that clause is code review's own failure count, and review has now passed
twice running (rounds 3–4); the quality gate has no equivalent
three-strike rule written anywhere in this department's docs.

## ENG-038 (round 5, aiorders-api) — PASS / PASS

First round on this ticket where both halves of the combined hop pass
together. Scope: diff since round 4's reviewed commit only
(`d13722a..125286f`, `outgoing-communications/actors/consumers.ts` + its
test file). Worktree re-checked fresh: HEAD `125286f`, no drift either
direction vs `origin/main`.

**Code review: 0/10 automatic failures.** The backend's round-4 fix
(`decideBroadcastChannelEligibility`, `buildBroadcastEmailLogRow`/
`buildBroadcastSmsLogRow`, `sendBroadcastMessage` exported with an
injectable `deps`) traced line-by-line against the pre-extraction version —
behaviour-preserving, no field dropped or renamed in the move, call site
unaffected since `deps` defaults to the real functions. Confirmed the one
`any` in the diff (`consumers.test.ts`'s fake-client chain) matches
`brand-portal/broadcasts.test.ts`'s own established pattern by reading that
file directly, not by trusting the backend's citation.

**Quality gate: PASS, first time on this ticket.** Gap 4 (AC5 write half)
closed — all five of QA's round-4 cover cases present and mapped 1:1 to a
test. Fresh re-check of the full acceptance table surfaced nothing new.

**Independent verification, not trusted from the backend's own account:**
full regression re-run fresh per directory (77 passed, 0 failed across five
suites, 62 ENG-038-relevant — arithmetic reconciled by counting `Deno.test`
blocks directly); two mutation tests of my own choosing, different from the
backend's own (`anySucceeded` OR/AND) and from round 4's own
(`decideUnsubscribePreCheck`) — dropped the `customerEmail` requirement
from the email-eligibility gate (caught by exactly 1 of 16 tests) and
flipped the skip-path `&&` to `||` (caught by exactly 2 of 16, the two
single-channel tests). Both restored clean, `git diff --stat` empty before
re-running. `deno check` on the full import graph: 8 pre-existing errors in
`consumers.ts` at the same lines every prior round has named (including
line 1091, `sendBroadcastMessage`'s own catch block, preserved verbatim),
plus 5 more in files this round's diff doesn't touch (`services/{email,sms,
whatsapp}.ts`, `utils/formatters.ts`) surfaced only because `deno check`
follows the import graph — not filed, not this round's diff.

**One new non-blocking finding, low severity / medium confidence:**
`sendBroadcastMessage`'s own customer-fetch/restaurant-fetch failure
branches (the function's top-level `catch`) have zero test coverage in any
round — all five orchestration tests stub both lookups as successful. Not
filed as a blocking gap: this path writes no `communication_log` row at
all, so it sits upstream of what AC5 governs, and QA's own Gap 4 cover list
never asked for it. Recorded now specifically so it doesn't repeat Gap 4's
own history — visible-but-unnumbered in one round's report, then dropped —
on a future ticket. Full finding and suggested fix:
`agents/principal-engineer/reviews/ENG-038.md`.

**Good work worth naming:** the `deps` injection point was scoped to
exactly the three calls crossing a network/crypto boundary, leaving
`supabase` a plain argument faked at `.from()` — kept `suite_command`
untouched and round 3's "`_shared/` is the only file here touching
`Deno.env`" claim true, and the backend's own notebook reasoned this
explicitly rather than leaving it implicit.

Per `code-review-gate/SKILL.md` step 9 ("pass → the ticket continues to
`in-security` once QA has also passed"): **1 transition** —
`in-review → in-security`, owner `principal-engineer → security`.

## ENG-038 (round 6, aiorders-api) — PASS / PASS

Scope: diff since round 5's reviewed commit (`125286f..63f5635`), the two
security-fix commits from security-gate round 1's findings. The prior
build hop that fixed those findings routed the ticket to `in-review` on
the strength of "this ticket's own round-2/3/4-fix precedent" — worth
flagging on its own terms even though the destination turned out right:
that precedent was fixes for findings raised *inside* the in-review
combined hop; these were security-gate findings, raised after review had
already passed once. The destination stands anyway because the two fix
commits are new code this gate has never seen, which is reason enough on
its own.

0/10 automatic failures. Verified both fixes against the actual system
rather than just the diff: `broadcast_campaign_recipients.restaurant_id`
is a real column (migration, line 101, denormalized on purpose) and
`'claimed'` is a legal status value (added in the *original* build commit,
not something this round introduced or needs to worry about). Chased down
one thing that looked like it might be a bug and wasn't: the new consent
re-check (`customer.consent_email?.consent !== false`) only works if
`consent_email` is an object, not a plain boolean — grepped every read/
write site in the repo and confirmed the object shape is real and already
used identically twice elsewhere. Recording the check, not a finding.

**Independent verification:** full regression re-run fresh per directory
(85 passed, 0 failed — round 5's 77 plus 8 new, reconciling exactly) and
`deno check` from each function's own directory rather than the shared
root (which still doesn't resolve the npm import): `dispatch.ts` zero
errors, `broadcasts.ts` 3 pre-existing in `utils.ts`, `consumers.ts` 8
in-file + 5 imported = 13 total — matches round 5's own baseline exactly,
one line shifted 1091→1120 by this round's own added code, same
pre-existing catch block.

**Two new non-blocking findings:** (1) a recipient row already `claimed`
when `cancel_broadcast` runs isn't among the rows that action cancels —
narrow window, pre-existing since the original build, missed by five
rounds of review including this one until now; (2) the new cap/interval
tests don't independently verify `restaurant_id`-scoping the way the
cancelled-campaign test verifies its own filter — very low severity, the
scoping pattern itself is well-established elsewhere in this file. Round
5's own finding on `sendBroadcastMessage`'s untested DB-fetch failure
branches is broadened rather than repeated: two new lookups this round
(recipient, step) add two more untested throw sites to the same class,
now four instead of two. Full detail:
`agents/principal-engineer/reviews/ENG-038.md`.

**Good work worth naming:** the "derives customer, restaurant, and content
strictly from the claimed recipient row" test replays the actual pre-fix
attack shape (a full spoofed payload) against the new code and asserts the
spoofed fields were never read — a meaningfully stronger guarantee than
just testing the new contract in isolation.

Per `code-review-gate/SKILL.md` step 9: **1 transition** —
`in-review → in-security`, owner `principal-engineer → security` — back to
security to confirm its own two findings are closed, not a fresh review
lap.
