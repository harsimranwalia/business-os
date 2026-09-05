# Coverage gaps — 2026-09-05

## ENG-020 — backend fully tested, frontend rendering entirely untested, despite direct precedent for testing that exact shape

First quality-gate run on this ticket. `aiorders-api`'s new code
(`acquisition.ts`, `channels.ts`) is thoroughly covered — 40 tests, including
a mutation-verified tenant-isolation case. `restaurant-portal`'s new page
(`Index.tsx`) and component (`ChannelBreakdown.tsx`) have zero test coverage
of any kind — no new `*.test.tsx` file in the diff at all.

**Worth naming as its own pattern, distinct from this board's usual "extract
it so it's testable" finding.** There is no extraction problem here and no
missing test infrastructure — `restaurant-portal` already runs `vitest` and
already has five component tests doing exactly this shape of work
(`BroadcastReport.test.tsx` most directly: a report component that fetches
data via a mocked source and asserts specific numbers and conditional
sections render). The acquisition report page is architecturally the closest
thing on this board to `BroadcastReport.tsx`. The gap is that the new page
didn't follow the pattern already established next to it in the same
repo — not that the pattern doesn't exist or can't reach.

**Not filed as a proposal.** This closes within `ENG-020`'s own next fix hop,
same as every other first-quality-gate-run finding on this board has. Naming
it here in case a second instance of "new report/detail component ships with
no rendering test despite direct sibling precedent" shows up on a different
ticket — that would be worth a sharper rule (e.g., the quality gate checking
for a sibling `*.test.tsx` pattern whenever a new page/report component is
added on a project that already has one), not this one occurrence.

Full findings, the specific fix per gap, and the acceptance-coverage table:
`agents/qa/test-plans/ENG-020.md`.
