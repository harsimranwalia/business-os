# Review log — 2026-09-05

## ENG-020 (round 1, aiorders-api + restaurant-portal) — REVIEW pass, QUALITY fail

Combined review+quality hop, first round, both repos in one session (`M`-sized
multi-repo ticket, `ENG-008`/`ENG-013` precedent — one hop, no work-breakdown
split). Ticket entered this hop at `building`, owner `eng-manager`, both
branches already pushed with no PR (`aiorders-api@cd82579`,
`restaurant-portal@2d3dc15`). `git fetch origin main` in both worktrees; `git
log HEAD..origin/main` / `git diff HEAD...origin/main --stat` both empty in
both — no drift since the build hop, no rebase needed.

**Automatic-failure scan: 0/10, both repos.** Full detail and per-item
reasoning: `agents/principal-engineer/reviews/ENG-020.md`. Nothing worth
repeating here beyond the one item that took real digging: #4 (`any`/untyped)
— `handleAcquisition`'s `payload: any, user: any` looked at first like a new
untyped surface, but `customers.ts`/`feedback.ts`/`offers.ts` already use the
identical signature shape, so this is the router's own dominant convention,
not a new departure. Worth remembering for the next `brand-portal` review:
this file family has two competing typed-`user` conventions already
(`catering.ts`/`broadcasts.ts` use `user: User`), so "reads like the code
around it" needs checking against more than one sibling before concluding
either way.

**AC5 (tenant isolation) mutation-tested, not read-and-trusted** — forced
`acquisition.ts`'s `!access.hasAccess` branch off (`if (false)`), re-ran
`acquisition.test.ts`: exactly the one denial test failed, the other 11 held.
Restored via backup (`/tmp/acquisition.ts.bak`), re-ran clean, `git status
--short` empty before continuing. Same discipline this board has applied to
every tenant-isolation claim since `ENG-015`.

**Independent re-run, both repos, matches the build hop's own account
exactly**: `aiorders-api` 40/40 (`channels.test.ts` 28 + `acquisition.test.ts`
12), `deno check` on both new files clean (3 pre-existing `utils.ts` errors
only, confirmed unchanged and outside this diff). `restaurant-portal` 14/14,
lint 0 new issues (the one flagged `any` is `brandPortalApi.ts`'s pre-existing
line-24 `RestaurantFeedback.meta`, not this diff's), build clean.

**Verified rather than assumed: the frontend/backend response-contract
claim.** `brandPortalApi.ts`'s new `getAcquisitionReport` casts `callApi`'s
result `as unknown as Promise<AcquisitionReportResponse>` — a flat shape,
unlike every other method's `{success, data}` envelope. Read `callApi`
itself: it returns `supabase.functions.invoke`'s `data` verbatim, no
re-wrapping; read `brand-portal/index.ts`'s response write: `JSON.stringify(result)`
straight from the handler, no envelope either. The cast is honest, not just
asserted — worth having checked, since a mismatch here is exactly the "seam
between two agents' work" class of bug `agents/qa/agent.md` names as the one
that reaches production most often.

**Three non-blocking findings** (full text, specific fixes:
`agents/principal-engineer/reviews/ENG-020.md`): F1, a single hardcoded error
heading shown for every query failure, not just the one it names; F2, the
organic-search honesty copy is a page footnote rather than attached to the
organic-search row the design's own wording implied (substance of AC4 still
met); F3, no cap on the number of distinct `other:<source>` buckets or on
label length, tracing back to unbounded public form input — low severity,
matches this ticket's own design reasoning about RPC-side cardinality being
accepted elsewhere on this exact function family.

**The quality gate found what review doesn't own — full account:
`agents/qa/test-plans/ENG-020.md`.** Worth naming here because it's a
different flavor from this board's usual "extract inline logic so it's
testable" finding: `acquisition.ts`/`channels.ts` are thoroughly unit-tested
(40/40) and this repo has no technical barrier to testing the frontend either
— `restaurant-portal` already has five component tests doing exactly this
shape of work (`BroadcastReport.test.tsx` especially, a report component
fetching data and asserting rendered totals/conditional sections). The gap
here is that the *new* page/component (`Index.tsx`, `ChannelBreakdown.tsx`)
shipped with zero test file despite that direct, repeated precedent — not a
missing capability, a missed application of an existing one. First time this
specific flavor (UI-rendering coverage gap despite in-repo precedent) has
been named this way on this board; not proposing a standards promotion off
one instance.

**Verdict: PASS on code review, round 1.** `links.review` set to this file's
sibling receipt. Quality gate FAILs on Gaps 1–3 (AC1/AC3 rendering, AC2, AC4)
— ticket returns to `building`, review's own pass stands and isn't
re-litigated next round.
