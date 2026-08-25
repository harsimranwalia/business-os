---
ticket: ENG-002
project: restaurant-portal
author: architect
created: 2026-08-25
adrs: []
one_way_doors: []
touches_data: false
touches_models: false
---

# Add a smoke-test harness to restaurant-portal — technical design

## Approach

`restaurant-portal` is a Vite + React + TypeScript app (`vite_react_shadcn_ts`)
with no test tooling of any kind — no `test` script, no `*.test.*` file, no
test runner in `package.json`. Add **Vitest** (not Jest, not Playwright) as the
dev dependency: it reuses the project's existing `vite.config.ts` directly, so
there is no second bundler/transform config to maintain, which is the cheapest
path to a *real* suite rather than a parallel one. Pair it with **React
Testing Library** for one smoke test that renders the app's real entry point
and asserts it mounts a known landmark — this is the test that fails when the
build breaks or the entry route stops rendering, which is the PRD's whole
acceptance bar.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `package.json` | add `vitest`, `@testing-library/react`, `@testing-library/jest-dom`, `jsdom` as devDependencies; add `"test": "vitest run"` | frontend |
| `vite.config.ts` | add a `test` block (`environment: 'jsdom'`, `globals: true`, setup file) | frontend |
| `src/test/setup.ts` | new — imports `@testing-library/jest-dom` matchers | frontend |
| `src/App.test.tsx` | new — renders `<App />` wrapped in whatever providers `main.tsx` wraps it in (router included), asserts a known landmark renders and nothing throws | frontend |
| `agents/eng-manager/config/projects.md` | Commands table, `restaurant-portal` Test cell → `npm run test` | eng-manager, at `ready-to-ship` |

## Data

Not applicable — `touches_data: false`.

## Interfaces

None. This is a dev-only addition; no runtime contract changes.

## Alternatives considered

- **Playwright (real-browser e2e).** Rejected for this ticket: needs a running
  dev/preview server plus a browser install in whatever runs the suite, which
  is real infrastructure for a "smoke" bar the PRD explicitly scopes down from
  ("comprehensive coverage" is a listed non-goal). Worth reconsidering if a
  later ticket wants true route-navigation coverage.
- **Jest.** Rejected: this is a Vite project: Jest needs its own transform
  config (`ts-jest`/`babel-jest`) that duplicates what Vite already does,
  and Vitest's API is a near-drop-in for Jest's if a future ticket ever wants
  to swap back.

## One-way doors

None. A test-runner choice is reversible — swapping Vitest for something else
later touches a handful of files, not a data model or a public contract. No
ADR, no G2.

## Risks

- **False negative from missing providers.** If `App.test.tsx` doesn't wrap
  `<App />` in the same providers `main.tsx` uses (router, any context
  providers), the smoke test can fail for a reason that has nothing to do with
  a real regression. Mitigation: the engineer at `building` reads `main.tsx`
  first and mirrors its provider tree exactly, rather than guessing.
- **jsdom vs. a real browser.** jsdom won't catch every rendering failure a
  real browser would. Accepted at smoke level — matches the PRD's own
  non-goal of comprehensive coverage; the Playwright alternative above is the
  upgrade path if that gap ever matters.

## Rollout

Dev dependency only — nothing deployed, nothing billed, no production surface
touched. Straight commit on a branch, PR per the project's L1 autonomy. No
rollback path needed beyond reverting the branch; `main` is never touched
directly.

## Out of scope

Comprehensive coverage, the other three frontends, `aiorders-api` — all named
in the PRD's own non-goals. This design does not touch any of them.
