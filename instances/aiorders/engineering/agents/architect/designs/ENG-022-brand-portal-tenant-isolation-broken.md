---
ticket: ENG-022
project: aiorders-api
author: architect
created: 2026-08-29
adrs: []
one_way_doors: []
touches_data: false
touches_models: false
---

# Brand-portal restaurant-scoped access check — technical design

## Approach

The nine files in `supabase/functions/brand-portal/` already split into two
families by how they signal failure: five files (`feedback.ts`, `customers.ts`,
`hiring.ts`, `website.ts`, and — for its *other* errors only —
`offers.ts`'s siblings `catering.ts`/`menus.ts`/`restaurants.ts`) throw plain
`Error`s for validation failures; four (`catering.ts`, `menus.ts`,
`restaurants.ts`, `onlineOrders.ts`'s `checkAccess()`) return `{success:false,
error}` for *access* failures specifically. The fix follows each broken file's
own existing convention rather than introducing a third shape or unifying the
two — unifying is a directory-wide refactor, not a bug fix (see Alternatives).

`utils.ts` already contains an unused, correctly-implemented throwing wrapper —
`verifyRestaurantAccessLegacy` (line 116), called from nowhere in the repo
(confirmed by grep across the whole `aiorders-api` worktree). Promoting it
(rename, drop `@deprecated`) gives the four throw-convention files
(`feedback.ts`, `customers.ts`, `hiring.ts`, `website.ts`) a one-line fix that
is structurally hard to get wrong the same way twice: nothing is returned to
forget to check. `offers.ts` — the one broken file whose own surrounding code
already returns `{success:false}` — is fixed in place, matching its own
correct siblings exactly; no new helper needed there.

## Components

| Component | Change | Owner agent |
|---|---|---|
| `supabase/functions/brand-portal/utils.ts` | modify — rename `verifyRestaurantAccessLegacy` → `requireRestaurantAccess`, drop the `@deprecated` doc comment, same behavior (throws `Error(result.error \|\| 'Access denied to this restaurant')` on denial, otherwise returns). Add one `console.warn` denial log line (user id + restaurant id) before the throw — `security-baseline.md` A09 requires authz denials to be logged and none of the 9 files currently log one. | backend |
| `supabase/functions/brand-portal/feedback.ts` | modify — 1 call site, `getFeedback` (~line 46) | backend |
| `supabase/functions/brand-portal/customers.ts` | modify — 5 call sites: `getCustomers`, `getCustomer`, `createCustomer`, `updateCustomer`, `deleteCustomer` (~lines 73, 124, 155, 186, 224) | backend |
| `supabase/functions/brand-portal/hiring.ts` | modify — 3 call sites: `getJobs`, `updateJobs`, `getCandidates` (~lines 37, 66, 115) | backend |
| `supabase/functions/brand-portal/website.ts` | modify — 2 call sites: `getWebsiteContent`, `updateWebsiteContent` (~lines 84, 120) | backend |
| `supabase/functions/brand-portal/offers.ts` | modify — 8 call sites, fixed in place (correct argument order + `.hasAccess` check), no new helper: `getOffers`, `createOffer`, `updateOffer`, `deleteOffer`, `toggleOfferStatus`, `createSpecial`, `updateSpecial`, `deleteSpecial` (lines 79, 146, 186, 224, 264, 304, 366, 424) | backend |
| `supabase/functions/brand-portal/*_test.ts` (new, one per fixed source file) | new — `Deno.test` negative-case per call site, per acceptance criterion 4 | backend |

**Test approach**, since `aiorders-api` has no test runner registered
(`config/projects.md`) and this ticket should not block on building one: Deno
ships a test runner with no config file required (`deno test path/to/file`
picks up the existing `brand-portal/deno.json` import map automatically). Each
new `*_test.ts` stubs a minimal `SupabaseClient`-shaped object — just the
`.from().select().eq().single()` chain each handler actually calls — returning
canned rows for "user manages restaurant A" and asserting the call for
restaurant B is denied (throws, for the four throw-convention files;
`success:false` for `offers.ts`). No network call, no live Supabase project, no
secrets. This is a real automated regression test per acceptance criterion 4,
not a manual-verification substitute, and it does not require the repo-wide
test harness `config/projects.md` frames as its own ticket — that framing was
about `restaurant-portal` (Vite/Vitest, zero existing scaffolding); Deno's
built-in runner has no equivalent gap.

## Interfaces

`utils.ts`, renamed export (signature unchanged from the existing dead helper):

```ts
export async function requireRestaurantAccess(
  restaurantId: string,
  supabase: SupabaseClient,
  user: User,
  options: RestaurantAccessOptions = {}
): Promise<true>   // throws on denial, never returns false
```

**Two call idioms, one per pre-existing file convention — deliberately not
unified:**

- **Throw idiom** (`feedback.ts`, `customers.ts`, `hiring.ts`, `website.ts`):
  ```ts
  await requireRestaurantAccess(restaurant_id, supabase, user)
  ```
  `customers.ts` and `feedback.ts` have no local `try/catch` around these call
  sites today — the throw reaches `index.ts`'s existing top-level catch
  unchanged: HTTP 500, `{error: 'Internal server error', details: message}`.
  That is this ticket's only place a legitimate denial produces a 500 instead
  of a clean 4xx — pre-existing for every other thrown validation error in
  both files (e.g. `customers.ts`'s `'Restaurant ID is required'`), not
  introduced by this fix (see Risks). `hiring.ts` and `website.ts` already
  wrap each call site in a local `try/catch` that converts any thrown error to
  `{success:false, error: error.message}` at HTTP 200 — the throw is caught
  one layer earlier, no index.ts involvement.

- **Return idiom** (`offers.ts` only):
  ```ts
  const access = await verifyRestaurantAccess(restaurant_id, supabase, user)
  if (!access.hasAccess) {
    return { success: false, error: access.error || 'Access denied to this restaurant' }
  }
  ```
  Identical to the already-correct idiom in `catering.ts`/`menus.ts`/
  `restaurants.ts` in the same directory.

Failure response as seen by `restaurant-portal`: either HTTP 200 with
`{success:false, error}` or HTTP 500 with `{error, details}`, depending on
which file — a split that already exists today for reasons unrelated to this
bug and that this ticket does not change.

## Alternatives considered

1. **Unify all 9 files on one convention (always throw, or always
   `{success:false}`).** Rejected — larger diff across files that are not
   broken today, changes response shape for call sites `restaurant-portal`
   may special-case on, and bundles a refactor into a P0 bug fix
   (`agents/architect/agent.md`: "Refactors bundled into feature work. They're
   separate tickets, always"). Worth a follow-on proposal, not this ticket.
2. **Fix each of the 19 broken call sites inline, no shared helper.** Rejected
   for the 11 throw-convention sites — satisfies the letter of the acceptance
   criteria but not the PRD's explicit ask ("structurally hard to repeat a
   sixth time"): a bare `if (!result.hasAccess) throw ...` inline is exactly
   as easy to omit as today's bug. A named helper makes the safe path the only
   path.
3. **Write a new throwing wrapper from scratch.** Rejected once
   `verifyRestaurantAccessLegacy` turned up already doing this, unused —
   promoting it costs a rename, not new code.

## One-way doors

None. Renaming an internal function with zero external callers (confirmed by
repo-wide grep), correcting call sites to use an existing primitive properly,
and adding colocated unit tests are all reversible and carry no recurring
cost, new dependency, or contract change.

## Risks

- **`offers.ts`'s fix does not use the new helper**, so the same
  wrong-order-and-bare-boolean mistake is still structurally possible there in
  the future. Accepted: `offers.ts` now has 8 freshly-corrected sites plus 3
  sibling files to copy from; the actual failure mode being closed is "copied
  from the one broken file in the directory," which no helper can fully
  prevent against a bad copy either way.
- **This ticket does not unify the two response shapes** (500-with-details vs.
  200-with-`success:false`) already present across these 9 files (see
  Alternatives #1). Whoever builds this should spot-check `restaurant-portal`'s
  call site for `get_feedback` in particular — its denial path is currently
  dead code (the bug always granted access) and is about to become live with a
  500 response; confirm the frontend doesn't assume every `brand-portal`
  response is 200 with a `success` field before shipping.
- **No CI wiring runs `deno test`/`deno check`** (`config/projects.md` — no
  `deno.json` at repo root). This ticket's tests run manually as part of
  `building`'s self-test step and QA's verification. Wiring a repo-wide CI
  wasn't needed to write real tests here (see Components), and remains out of
  scope beyond that.
- **No evidence of actual exploitation** (carried from the PRD). Customer
  notification is a business/legal call, not an engineering one, and has
  already been surfaced to the approver via the P0 incident notice
  (`inbox/_handled/2026-08-29-eng022-p0-incident.md`, acknowledged, no further
  action requested).

## Rollout

Straight, no flag, no backfill — a logic-only fix on existing endpoints, no
schema change. Branch → PR → gates → human merge (`aiorders-api` is L1) →
deploy to the Supabase project (`bmnmnejwdxbcqinqkwko`). Qualifies for
`definition-of-done.md`'s P0-hotfix exception to the release window
(no-Friday-afternoon / no-weekend) if it reaches `ready-to-ship` inside one —
the exception waives the calendar, not the security gate, which still runs.
Rollback: revert the merge commit. No migration, so a revert fully restores
prior (broken) behavior with nothing further to clean up.

## Out of scope

- The 4 already-correct files (`catering.ts`, `restaurants.ts`, `menus.ts`,
  `onlineOrders.ts`) — not touched, not broken.
- Unifying the two response conventions across the directory (Alternatives
  #1) — a separate refactor ticket if wanted.
- Auditing access checks outside `supabase/functions/brand-portal/` (PRD
  non-goal).
- Wiring `deno test`/`deno check` into CI — this ticket's tests run manually;
  a repo-wide harness is its own ticket if the pattern proves worth extending
  past this one directory.
- Changing HTTP status codes for denial (e.g. 403 instead of 200/500) — touches
  frontend error handling, a bigger and separate change.
