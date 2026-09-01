# Review log — 2026-08-29

## ENG-013 — Foodswipe funnel stage control (aiorders-api, aiorders-admin-hub)

**Round 1: FAIL — automatic-failure #10** (auth/authorization path changed
with no failure-case test).

- **Where:** `supabase/functions/admin-portal/handlers/foodswipe.ts` @
  `feat/ENG-013-foodswipe-funnel-stage-control` (`ac4efba`). New actions
  `setStageOverride` (line 155) and `resetStageOverride` (line 203), routed
  at lines 69/72, gated by `hasFoodswipeAccess` (line 42), tenant-scoped by
  `.eq('source', 'foodswipe')` (lines 178, 219).
- **What's wrong:** zero test coverage — no test proves a non-admin/
  sub-admin caller is rejected, no test proves an invalid `stage` value is
  rejected, no test proves the `source='foodswipe'` scoping actually stops
  a write from landing on a non-Foodswipe profile. That last one is the
  single line the diff's own PR body calls "what to review hardest," and it
  has no regression protection at all.
- **Why it matters:** this repo already has direct precedent for exactly
  this situation — `ENG-007`'s `loyalty-config.test.ts` (44 tests, including
  a named non-admin-role → 403 case) and `ENG-011`'s `brands.test.ts` — both
  written despite the same "no `deno.json`" gap this repo has always had
  (`config/projects.md`). The absence here isn't this repo's baseline; it's
  a regression against this board's own two prior tickets.
- **The fix:** one colocated `foodswipe.test.ts` (same shape as
  `loyalty-config.test.ts`): `hasFoodswipeAccess` unit tests (admin,
  sub-admin, neither, the `additional_roles` variant); a `VALID_STAGES`
  rejection test for `setStageOverride`; a case proving the `source` filter
  is actually present in the query the handler builds (stub the Supabase
  client call args, same technique `loyalty-config.test.ts` uses for its
  DB-touching branches).
- **Verdict:** fail, round 1. No receipt written
  (`agents/principal-engineer/reviews/ENG-013.md` stays absent). Routed to
  `building`, same ticket, no owner change (`eng-manager` throughout this
  instance's machine-owned range). QA's hop not run this round — discarded
  per the combined-hop design (`config.yaml` → `machine_gates.combined_hop`).

This is the first code-review failure recorded on this board — no
third-occurrence pattern yet, so no `engineering-standards.md` promotion
from this entry alone.

### ENG-013 — round 2: PASS

- **Where:** `foodswipe.test.ts` (new, 239 lines) plus two additive exports
  in `foodswipe.ts` (`AuthenticatedRequest`, `hasFoodswipeAccess`), closing
  round 1's #10.
- **Automatic-failure scan:** 0/10. #10 closed — 5 access-check unit tests,
  a 403 test per new write route via a throwing-`Proxy` `adminSupabase`, a
  405-before-role test, 6 validation-rejection tests, and 4 tests on the
  write itself proving both `.eq('id', ...)` and `.eq('source',
  'foodswipe')` fire. #4 (`any`) has one new instance
  (`hasFoodswipeAccess(userProfile: any)`) — confirmed by diffing lint
  output against `origin/main` (13 vs. 12) that this is the extraction of
  an already-untyped value, not a fresh untyped surface; same call
  `ENG-008` already made for `hasInfluencerAdminAccess`.
- **Verified independently, not trusted from the ticket log:** `deno
  check`/`deno test` re-run in place (worktree already on this ticket's
  branch) — 19/19, matching the build pass's own claim exactly.
  **Mutation-tested the tenant-scoping assertion** — round 1's own "what to
  review hardest" line: removed `.eq('source', 'foodswipe')` from
  `setStageOverride` by hand, re-ran — the scoping test and its 404
  neighbor both failed (17/19) exactly as expected, `resetStageOverride`'s
  own pair correctly stayed green (only `setStageOverride` was mutated).
  Reverted, confirmed `git diff --stat` empty, re-ran clean. `npm run
  lint`/`npm run build` on `aiorders-admin-hub` (switched to this ticket's
  branch, switched back to `ENG-008`'s afterward) independently reproduced
  the build pass's exact counts (150 pre-existing lint errors, 0 new; clean
  build).
- **One correction to the ticket's own log, not a code finding:** the
  build/test-gap pass recorded the repo's 17 pre-existing `deno check`
  errors as "all in `users.ts`." Re-run fresh this round with each error's
  file location isolated rather than trusted: the actual split is
  `auth.ts` (4), `partners.ts` (4), `users.ts` (9). The count (17) and the
  load-bearing claim (zero in `foodswipe.ts`/`foodswipe.test.ts`) both
  still hold — doesn't change the verdict, corrected in the receipt for
  whoever reads that log entry next.
- **No new finding beyond what `ENG-008`'s round 2 already filed**: the
  `hasXAccess`/`AuthenticatedRequest` duplication proposal already named
  `foodswipe.ts` as one of its three files; this round re-confirms that
  fact rather than adding a new one.
- **Verdict:** pass, round 2. Receipt written:
  `agents/principal-engineer/reviews/ENG-013.md`. Full gap detail (narrow
  success-path value coverage, "set then reload" not exercised as one
  test, no live DB, no frontend test harness) in
  `agents/qa/test-plans/ENG-013.md` — none of it blocking, none of it
  inside automatic-failure #10's actual scope.

## ENG-008 — Influencer board admin management (aiorders-api, aiorders-admin-hub)

**Round 1: FAIL — automatic-failure #10** (auth path changed with no
failure-case test).

- **Where:** `supabase/functions/admin-portal/handlers/influencers.ts` @
  `feat/ENG-008-influencer-admin-management` (`e240767`), new file. New
  `GET`/`PATCH /admin-portal/influencers/{id}`, gated by
  `hasInfluencerAdminAccess` (admin/sub-admin, line 20), routed from
  `index.ts`. Frontend caller: `handleSaveInfluencer` in
  `aiorders-admin-hub`'s `src/pages/Influencers.tsx` @ `f2ea36c`.
- **What's wrong:** zero test coverage anywhere in either diff — no test
  proves a non-admin/sub-admin caller gets 403, no test proves any of the
  six field-level validations in `updateInfluencer` (out-of-range
  `staff_rating`, negative `collaboration_count`, wrong types on
  `city_preference`/`accepts_paid`/`accepts_barter`/`min_visit_payment`)
  reject bad input with 400, no test proves a successful `PATCH` actually
  persists and returns the updated row. `git diff --stat` against both
  branches (`origin/main...HEAD`) shows only the handler, `index.ts`'s
  routing/CORS line, and the migration in `aiorders-api`, plus
  `Influencers.tsx` in `aiorders-admin-hub` — no `.test.ts` anywhere.
- **Why it matters:** same rule, same repo, same day as `ENG-013`'s own
  round-1 fail immediately above — this board already has two precedent
  test files for exactly this shape (`loyalty-config.test.ts` — `ENG-007`;
  `brands.test.ts` — `ENG-011`), so the absence here is a regression
  against this board's own established practice, not an unreasonable new
  bar invented at review time.
- **The fix:** one colocated `influencers.test.ts` (same shape as
  `loyalty-config.test.ts`): `hasInfluencerAdminAccess` unit tests (admin,
  sub-admin, neither, the `additional_roles` variant); a rejection test per
  validated field in `updateInfluencer`; a case proving a successful
  `PATCH` returns the updated row.
- **Verdict:** fail, round 1. No receipt written
  (`agents/principal-engineer/reviews/ENG-008.md` stays absent). Routed to
  `building`, same ticket, owner unchanged (`eng-manager`). QA's hop not
  run this round — discarded per the combined-hop design (`config.yaml` →
  `machine_gates.combined_hop`).

Everything else scanned clean: no secret, no silent catch (`console.error`
before every error response, both new handler functions), no unbounded
query (`GET` is single-row by id, no collection endpoint), no new
dependency (`Checkbox` and `@radix-ui/react-checkbox` both already in
`aiorders-admin-hub`'s `package.json` before this diff), no commented-out
code or unowned `TODO`, no drive-by refactor (the CORS
`Access-Control-Allow-Methods` widening is required by the new `PATCH`
route itself, not unrelated cleanup), no datastore-layer bypass
(`adminSupabase.from(...)` matches `loyalty-config.ts`/`foodswipe.ts`'s own
established pattern). The `AuthenticatedRequest` interface's `any` fields
are copied verbatim from `foodswipe.ts` — matches surrounding code exactly,
not a fresh violation of the no-`any` standard.

Second occurrence of automatic-failure #10 in one day, same repo, same
untested-write-path shape as `ENG-013` directly above — both of today's new
`admin-portal` write handlers shipped without their own test file. Not yet
a third occurrence (the promotion threshold in `engineering-standards.md`
step 10), but one more of this exact shape is worth promoting to an
explicit standing item ("every new handler file needs a colocated
`.test.ts` before code review") rather than continuing to catch it after
the fact each time.

### ENG-008 — round 2: PASS

- **Where:** `influencers.test.ts` (new, 161 lines) plus a one-expression
  fix in `influencers.ts` (`Boolean(...)` wrap on `hasInfluencerAdminAccess`'s
  return), closing round 1's #10.
- **Automatic-failure scan:** 0/10. #10 closed — 5 access-check unit tests,
  a 403 and a 405 test through `handleInfluencers` itself via a
  throwing-`Proxy` `adminSupabase` (fails loudly if a rejected branch ever
  reached the datastore), one rejection test per `EDITABLE_FIELDS` entry (8
  cases), one success case. #4 (`any`) unchanged from round 1, re-confirmed
  rather than re-litigated: `foodswipe.ts`'s `AuthenticatedRequest` diffed
  directly this round — byte-for-byte identical, so this is the same
  already-adjudicated finding, not a new one.
- **Verified independently, not trusted from the ticket log:** `deno
  check`/`deno test` re-run from an isolated copy (the shared
  `_eng/aiorders-api` worktree was mid-flight on `ENG-013`'s branch at
  review time) — 17/17, matching the build pass's own claim exactly.
  **Mutation-tested the regression fix**: reverted `Boolean(...)` by hand,
  re-ran — `hasInfluencerAdminAccess rejects an unrelated role` failed
  exactly as expected (16/17), confirming the test is evidence and not
  just present, per the standards' mutation-testing bar. `npm run
  lint`/`npm run build` on `aiorders-admin-hub` (already on this ticket's
  branch) independently reproduced the build pass's exact counts (150
  pre-existing lint errors, 0 new; clean build).
- **New finding, not blocking:** the `hasXAccess`/`AuthenticatedRequest`
  shape is now duplicated across three handler files
  (`foodswipe.ts`/`influencers.ts`/`loyalty-config.ts`), two incompatible
  conventions (crash-on-null-profile vs. null-safe), written on three
  different tickets the same day. This ticket correctly matched its
  nearest same-day sibling (`foodswipe.ts`) rather than inventing a fourth
  shape — the right per-ticket call — but the fork itself predates this
  ticket and isn't this ticket's to fix. Filed as a proposal
  (`proposals.md`, `by: principal-engineer`) rather than fixed inline.
- **Verdict:** pass, round 2. Receipt written:
  `agents/principal-engineer/reviews/ENG-008.md`. Full gap detail (narrow
  success-path field coverage, two untested branches, no live DB) in
  `agents/qa/test-plans/ENG-008.md` — none of it blocking, none of it
  inside automatic-failure #10's actual scope.
