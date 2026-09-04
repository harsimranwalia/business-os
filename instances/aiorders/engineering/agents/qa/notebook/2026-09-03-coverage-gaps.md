# Coverage gaps — 2026-09-03

## ENG-015 — AC3/AC4/AC5 untestable this pass, root cause is two compounding infra gaps

The add-location write path (partner INSERT under their own brand, held
for review) is enforced by a new RLS policy on `aiorders-api` plus a
5-line conditional in `aiorders-admin-hub`'s `AddRestaurantModal.tsx`.
Neither has any automated or live-executed coverage as of this ticket's
`in-security` handoff:

- No live Postgres/Supabase connection reachable this pass (or any prior
  hop on this ticket — build, round-1-fix, migration doc all named the
  same gap independently).
- `aiorders-admin-hub` has zero test infrastructure at all — confirmed
  fresh again this pass (no `vitest`/`jest`/`@testing-library`, no `test`
  script, no `*.test.*` file anywhere). Standing open proposal,
  `proposals.md` 2026-08-31 (eng-manager) — this is the **second** ticket
  this same gap has blocked full coverage on since that proposal was
  filed (`ENG-008`'s round-1 regression test was the first, same
  proposal's own row already cites it).

Closed the gap as far as static reasoning can this pass (full RLS
policy-history trace — see `test-plans/ENG-015.md`'s "Not automated"
section for the trace itself) rather than either silently passing it as
covered or hard-failing a gate that can't be fixed by another build hop.
Recommended a manual staging smoke test as the actual close-out step.

**Pattern worth watching:** this is the second acceptance criterion on
this board (after `ENG-013`'s frontend criteria) closed by hand-trace
rather than execution specifically because of `aiorders-admin-hub`'s
missing test harness, and the first where the untestable piece is also a
security enforcement boundary (an RLS `WITH CHECK`) rather than a
read-path UI behaviour. If a third ticket hits this, the standing
proposal's severity argument gets stronger — worth a line in whoever
next reviews the batched proposal G1.

**For future coverage-gap entries on this ticket family:** the fastest
way to close this permanently isn't more hand-tracing per ticket, it's
either (a) the open `aiorders-admin-hub` test-harness proposal landing, or
(b) a working read-only DB connection being wired back in for build-loop
sessions — `ENG-007`/`ENG-011`/`ENG-013` all had one at various points
and this ticket's entire history did not. Either would have turned this
pass's several hours of static tracing into one executed test.

## ENG-031 — not a coverage gap in the usual sense: zero ACs apply, zero suite exists

Distinct from the ENG-015 entry above, worth telling apart. That gap was
"criterion real, execution blocked." This one is "no criterion from the
parent PRD applies to this diff at all": `ENG-016`'s 13 acceptance
criteria all require `ENG-032`/`ENG-033`/`ENG-034`, none of which exist yet
— this ticket adds two nullable columns nothing reads or writes. On top of
that, `aiorders-api` has no test infrastructure whatsoever for *any*
ticket: no `package.json`, no `deno.json`, config/projects.md's Commands
row is empty across Test/Lint/Typecheck/Build. Unlike `ENG-022`/`ENG-024`
(same project, same day), this diff has zero `.ts` files, so there wasn't
even an ad-hoc `deno check`/`deno test` to run informally.

Verdict was still `pass`: none of the quality gate's own fail conditions
(red suite, uncovered AC, unregressed bug fix, open P0/P1) are met when
none apply. Full reasoning: `agents/qa/test-plans/ENG-031.md`.

**Filed as a proposal, not just this note** (`proposals.md`, 2026-09-03):
`aiorders-api` has never had a `deno.json`/test command registered, unlike
`aiorders-admin-hub` (proposed 2026-08-31) and `restaurant-portal`
(`ENG-002`, already shipped). This is the first ticket on this project with
*zero* code to informally check either way — worth closing before a ticket
that actually needs the harness hits the same wall with higher stakes.

## ENG-032 — first component-test coverage for CateringKanban / CateringDetailModal, both zero before this round

The design assigned AC-8's UI slice and AC-12 (narrowed — see the test plan's
own Scope note) to QA's plan rather than the build hop, and neither component
had ever had a test file. Wrote both this round:
`CateringKanban.test.tsx` and `CateringDetailModal.test.tsx`, colocated,
matching the two-file convention `CateringPageForm.test.tsx` already set this
same day. Both components turned out to be far cheaper to test than
`CateringPageForm` risked being — `requests`/`request` both arrive as props,
no internal fetch, no context provider needed — so the "needs supabase
mocking" worry (both files import it transitively, one directly) resolved to
a one-line `vi.mock` with an empty stub, never actually exercised since
nothing in a read-only render path calls it.

Mutation-verified both, not just written and left green: removed one
`statusConfig` entry (`CateringKanban`) and reproduced the design's own
named risk verbatim — `Cannot read properties of undefined (reading
'borderColor')` — then restored. Forced the itemized block to always render
(`CateringDetailModal`) and got `Cannot read properties of null (reading
'reduce')` on the omit-block test, confirming that test independently
catches the opposite mistake from the render test. Same discipline
`engineering-standards.md`'s mutation rule asks for on regression tests,
applied here to new coverage rather than a bug fix — worth treating as the
default for any new test on this board, not just ones tied to a fix.

One item named by the design but deliberately not automated: the
brand-level-catering-content precedence override (ADR-009's Consequences,
"worth a line in QA's test plan and worth an observation"). Both written —
see the test plan's own Not-automated section and `observations.md`.

Full reasoning: `agents/qa/test-plans/ENG-032.md`.
