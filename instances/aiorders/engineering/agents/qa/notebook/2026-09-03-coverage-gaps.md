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
