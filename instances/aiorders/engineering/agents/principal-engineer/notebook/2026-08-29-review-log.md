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
