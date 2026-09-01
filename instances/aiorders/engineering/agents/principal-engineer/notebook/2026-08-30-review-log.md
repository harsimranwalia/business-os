# Review log — 2026-08-30

## ENG-008 — Influencer board admin management (aiorders-api, aiorders-admin-hub)

**Round 1: FAIL — automatic-failure #10, plus a real correctness bug.**

- **Where (finding 1):** `supabase/functions/admin-portal/handlers/influencers.ts`
  @ `feat/ENG-008-influencer-admin-management` (`e240767`). New
  `hasInfluencerAdminAccess` (line 22) and the `PATCH` path in
  `updateInfluencer` (line 97), field allowlist `EDITABLE_FIELDS` (line 13).
- **What's wrong:** zero test coverage — no test proves a non-admin/
  sub-admin caller is rejected (PRD acceptance criterion 8, explicit), no
  test proves `staff_rating` outside 1–5 or a negative `collaboration_count`
  is rejected, no test proves the field allowlist actually restricts what a
  caller can write.
- **Why it matters:** identical shape to `ENG-013`'s round 1 failure one
  cycle earlier, same repo, same day (see the 2026-08-29 entry in this
  notebook). Direct precedent already exists here too:
  `loyalty-config.test.ts` (44 tests, the same access-check shape — admin,
  sub-admin, wrong role, missing profile) and `brands.test.ts`. Two
  occurrences of the same failure class on this board now, both this week.
- **Where (finding 2):** `src/pages/Influencers.tsx` @
  `feat/ENG-008-influencer-admin-management`
  (`aiorders-admin-hub@f2ea36c`), `openInfluencer` lines 96–97.
- **What's wrong:** `accepts_paid: influencer.accepts_paid ?? !influencer.barter_visit`
  and the `accepts_barter` equivalent. For the 51/306 production rows where
  `barter_visit` (and therefore the backfilled `accepts_paid`/
  `accepts_barter`) is genuinely `null`, `null ?? !null` evaluates to
  `true` (`!null === true` in JS) — the dialog silently presents a fabricated
  "accepts paid" default for an influencer whose preference was never set.
  `handleSaveInfluencer` sends both fields unconditionally on every save, so
  editing any unrelated field on one of these rows writes that fabricated
  value to the database.
- **Why it matters:** this directly contradicts the ticket's own migration
  and design intent — the backfill was deliberately written to keep a null
  `barter_visit` mapped to null on both new flags rather than guessing, and
  the frontend discards that guarantee the moment the record is opened for
  editing. Reachable today, not hypothetical: 51 real rows.
- **The fix:** one colocated `influencers.test.ts` (same shape as
  `loyalty-config.test.ts`) covering `hasInfluencerAdminAccess` (admin,
  sub-admin, wrong role, missing/undefined profile) and input validation on
  `updateInfluencer`; on the frontend, default both flags to `false` (not a
  negation of a possibly-null source) when the influencer's own value is
  null, plus a regression test opening the dialog on an all-null row and
  asserting neither checkbox pre-checks and neither field is written unless
  the user touches it.
- **Verdict:** fail, round 1. No receipt written
  (`agents/principal-engineer/reviews/ENG-008.md` stays absent). Routed to
  `building`, same ticket, no owner change (`eng-manager` throughout this
  instance's machine-owned range). QA's hop not run this round — discarded
  per the combined-hop design.

Second occurrence of the automatic-failure-#10 shape in two days, both on
`aiorders-api`'s `admin-portal` handlers (see 2026-08-29 entry, `ENG-013`).
Not yet a third occurrence — no `engineering-standards.md` promotion from
this entry alone — but one more of the same shape on this file family is
the trigger per `skills/code-review-gate/SKILL.md` step 10.
