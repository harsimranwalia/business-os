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
