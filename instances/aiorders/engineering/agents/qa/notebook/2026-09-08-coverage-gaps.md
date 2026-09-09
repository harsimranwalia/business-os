# Coverage gaps — 2026-09-08

## ENG-053 — round discarded on a code-review fail, and this gate's own coverage lens independently lands on the same finding

`aiorders-api` mechanically isn't "no suite" for this file the way every
migration-only ticket on this project has been — `brand-portal/loyalty.ts`
has carried `loyalty.test.ts` since `ENG-049` (19 tests). Ran it fresh
against this ticket's branch rather than trusting the build hop's own "no
test suite exists for this project" line: `deno test --no-check` from
outside the repo tree, the same `npm:`-resolution workaround `ENG-049`'s
own round 2 and this ticket's own build hop both used for `deno check` —
**19/19, matching `ENG-049`'s round-2 count exactly, nothing regressed.**

**Acceptance coverage (this ticket's owned set — AC10 in full; the
handler-caller half of AC3, AC4, AC7, AC8, AC11):** every one of them
routes through `redeemPoints`, and none has a test. Confirmed by grep
(`redeemPoints\|redeem_points` against `loyalty.test.ts`: zero hits) before
letting the suite's own green run stand in for coverage of this ticket's
new code — 19/19 is real, but it's 19/19 of the *old* surface; it says
nothing about the ~50 new lines this ticket added to the same file.

**Failure paths — this gate's charter (`agents/qa/agent.md`, "How you
test") names "unauthorised caller" and "invalid input at the boundary"
specifically, and neither is exercised for this ticket's new action:**

| Scenario | Expected behaviour | Result |
|---|---|---|
| Staff without restaurant access calls `redeem_points` | Rejected before any RPC call (AC10) | Correct by inspection (`requireRestaurantAccess` runs first, same as its two siblings) — **but no test proves it**, unlike `record_dine_in_earn`'s own AC17 case three functions up in the same file |
| Missing `code` / `idempotency_key` / non-positive `points` | Rejected, zero RPC calls (design's own "no RPC call made") | Correct by inspection — **but no test proves the RPC is never reached**, the actual property the design calls load-bearing |
| Each of `invalid_code`/`not_enrolled`/`insufficient_balance`/`redeemed` | Distinct, correctly-shaped response per outcome | Correct by inspection, matches the design's Interfaces section exactly — **but no test pins any of the four branches**, so a future edit that swaps two `if` conditions would ship green |

Every row is "correct by inspection," the same conclusion code review's own
line-by-line trace reached — this isn't a logic defect. It's that
inspection is what this gate falls back to when nothing automated exists
to run, and here something automated *does* exist (this exact file's own
suite) and simply wasn't extended — a materially more avoidable gap than
the "genuinely no harness" position `ENG-046`/`ENG-047` were in.

**Not automated, and unlike most of this project's prior tickets, that's
not because there's nothing to add a case to** — `loyalty.test.ts` and
`acquisition.test.ts`'s stubbed-`.rpc()` extension are both real, present,
and directly reusable. No bug filed — this is a round-1 coverage finding on
a diff that's about to change, same treatment `ENG-048`'s round 1 gave its
own two findings.

**Not filed as a new proposal or observation on its own** — the missing
tests are this ticket's own fix to make, not a process gap needing the
approver's attention. The *adjacent* discovery that `config/projects.md`'s
"no test files" line is now stale for `aiorders-api` is filed once, in
`observations.md`, not duplicated here.

**Verdict: this round is discarded, not a recorded pass.** Review failed
(round 1, same diff — see
`agents/principal-engineer/notebook/2026-09-08-review-log.md`) on the
identical root cause this gate independently landed on, so per
`code-review-gate/SKILL.md` step 9 no `agents/qa/test-plans/ENG-053.md`
receipt is written this round.

## ENG-053 round 2 — the three failure-path gaps above, now closed

All three rows from round 1's table (unauthorised caller, boundary input, all
four RPC outcomes) have a test now — 15 new cases added to `loyalty.test.ts`
(34 total, up from 19), each asserting a call-count property
(`rpcCalls.length`/`ledger.queryCount()`) alongside the response shape rather
than just the absence of a thrown error. Re-ran fresh: 34/34 on the file,
119/119 on the full `brand-portal` suite. First non-discarded receipt for
this ticket: `agents/qa/test-plans/ENG-053.md`.
