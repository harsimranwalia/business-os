# Review log — 2026-08-31

## ENG-013 — Foodswipe funnel stage control, round 2 (aiorders-api, aiorders-admin-hub)

**Round 2: PASS.** Full detail: `agents/principal-engineer/reviews/ENG-013.md`.
Round 1's finding (automatic-failure #10, no failure-case test on the new
authz-gated write path) is closed by `foodswipe.test.ts` (17 cases),
already on the branch when this review started (cross-host provenance,
see the ticket's own log). Tenant-scoping test is mutation-sensitive by
construction (records every `.eq()` call rather than asserting only the
response shape) — worth citing as an example the next time a handler
needs the same kind of test.

**Watching, not yet promoting:** `export interface AuthenticatedRequest {
user: any; supabase: any; adminSupabase: any; }` now appears on two
`admin-portal` handlers — `influencers.ts` (`ENG-008`) and `foodswipe.ts`
(`ENG-013`). `loyalty-config.ts` (`ENG-007`) instead types this properly
(`AuthenticatedUser`, `SupabaseClient`). Two occurrences of the untyped
version, not three — engineering-standards.md's automatic-failure #4
already covers this in principle; what's missing is a house convention
for *which* of the two existing shapes new handlers should follow. Next
occurrence promotes this to `engineering-standards.md` directly rather
than being noted again.
