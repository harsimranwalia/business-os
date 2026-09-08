# Acceptance — ENG-026 (FoodSwipe channel-visibility toggles and capability-based discovery — parent)

## Why this one is a from-scratch walk, not a rollup

`ENG-021`'s own acceptance notebook (`2026-09-07-eng021-acceptance.md`) found
both its children had already run `acceptance-check/SKILL.md` in full at
their own shipping point, so that parent check was "a rollup and a fresh
no-drift check, not a rediscovery." **This family is different.** All four
children (`ENG-044`, `ENG-045`, `ENG-046`, `ENG-047`) reached `shipped` via a
**control-center dashboard action**, not a build-loop pass — each one's own
board-file log says so explicitly ("Advanced from the dashboard rather than
by a build-loop pass"). A dashboard write never calls
`lib/eng-trigger.sh continue {ticket-id}`, so `continue` never fired for any
of the four individually, and `acceptance-check/SKILL.md`'s own trigger ("a
ticket enters state `shipped`") never got the chance to run at the child
level — not a shortcut version, none at all. Confirmed before writing
anything: no `agents/product-manager/notebook/` file exists for any of the
four (only `eng038`/`eng039`/`eng040`/`eng021`/`eng041` do), and unlike every
other settled family on this board (`ENG-031`/`033`/`034`, `ENG-038`/`039`,
`ENG-040`/`041` — all confirmed `state: verified` on their own children),
`ENG-044`–`047` sat at `state: shipped`, not `verified`, with no path back to
this check except this parent's own `ADR-003`-forced closing hop. Filed as a
proposal, not just noted here — see `ENG-026`'s own board-file log for this
date and the addendum to `proposals.md`'s 2026-09-07 dashboard-bypass row.

So this pass walks all five PRD criteria against the live, merged, deployed
code directly — the same standard `ENG-034`'s from-scratch run set
(`2026-09-04-acceptance.md`) when it was the first to break a similar streak
of skipped checks.

## Scope

All 5 acceptance criteria in the PRD
(`agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md`), per
the work-breakdown's own AC-mapping
(`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`):

| AC | Owner(s) | Repo |
|---|---|---|
| 1 (migration + defaults, no regression) | `ENG-044` | `aiorders-api` |
| 2 (staff view/set from admin-hub) | `ENG-046` | `aiorders-admin-hub` |
| 3 (Dine-In/Catering flag-gated, negative case) | `ENG-045` | `aiorders-api` |
| 4 (closed-but-enabled still shows; Open Now excludes) | `ENG-045` (logic) + `ENG-047` (UI) | `aiorders-api`, `restaurant-marketplace` |
| 5 (rollout/backfill answered on file) | `ENG-044` | `aiorders-api` |

No criterion is owned by a single ticket's diff alone for AC4 — same shape
`ENG-021`'s own AC3 split and `ENG-026`'s own work-breakdown notebook already
named; checked `ENG-045` and `ENG-047` together.

## Check against the live result — not the proxies

Fetched all three repos fresh in the department's own worktrees
(`~/Documents/projects/_eng/{project}`), read the merged code directly off
each default branch, and — since none of the four children's own build hops
had a CI file to lean on for `aiorders-api` — went one step further than a
git-ancestry check for that repo specifically:

```
$ (cd aiorders-api && git fetch origin main && git log -1 --oneline origin/main)
afc45cc Merge pull request #20 from harsimranwalia/feat/ENG-045-foodswipe-channel-visibility-discovery-handlers

$ (cd aiorders-admin-hub && git fetch origin main && git log -1 --oneline origin/main)
6d340c0 Merge pull request #10 from harsimranwalia/feat/ENG-046-foodswipe-channel-visibility-admin-toggles

$ (cd restaurant-marketplace && git fetch origin master && git log -1 --oneline origin/master)
0dc8af8 Merge pull request #1 from harsimranwalia/feat/ENG-047-foodswipe-open-now-and-channel-display
```

All four PRs independently confirmed `MERGED` via `gh pr view --json state`
(#19, #20 on `aiorders-api`; #10 on `aiorders-admin-hub`; #1 on
`restaurant-marketplace`).

**`aiorders-admin-hub` and `restaurant-marketplace` — deploy confirmed, not
assumed, via their own CI:**

```
$ gh run list --branch main --limit 1     # aiorders-admin-hub
completed  success  Merge pull request #10 ... Deploy to Cloudflare Pages  2026-09-07T20:25:28Z

$ gh run list --branch master --limit 1   # restaurant-marketplace
completed  success  Merge pull request #1 ...  Deploy to Cloudflare Pages  2026-09-07T20:37:57Z
```

Both `.github/workflows/deploy-cf.yml` trigger on push to the default
branch; both show a `success` run against the exact merge commit.

**`aiorders-api` has no CI workflow at all** (`config/projects.md` already
names this repo as having no test/build automation) — merge-to-`main` is not
provably deploy-to-Supabase from the repo alone, so this pass went to the
next-best live evidence rather than stopping at git ancestry:

```
$ supabase migration list --linked
... {"local":"20260907120000","remote":"20260907120000", ...}
... {"local":"20260907120001","remote":"20260907120001", ...}
```

Both of `ENG-044`'s migrations show `local == remote` — applied to the
**live, linked production database** (`bmnmnejwdxbcqinqkwko`), not just
present as files on a merged branch. For the edge function itself
(`ENG-045`'s handler code), `supabase functions list` shows the
`restaurant-marketplace` function's `updated_at` at `2026-09-07T20:21:33Z` —
**62 seconds after** PR #20's own `mergedAt` (`2026-09-07T20:20:31Z`, via
`gh pr view 20 --json mergedAt`). Named honestly rather than overclaimed:
this is a tight timing correlation, not a byte-for-byte diff against the
deployed bundle (no committed anon key or CI log was available to fetch the
live source directly) — but a 62-second gap between merge and redeploy,
matching the one function this ticket's diff touches, is strong evidence the
merged handler code is what's actually serving traffic, not merely evidence
it exists in git.

## Walk every criterion

| AC | Criterion | Result |
|---|---|---|
| 1 | Migration adds all three flags with stated defaults; `has_order_food` default doesn't regress current Order Food discovery | **Pass** — `20260907120000_add_channel_visibility_to_restaurants.sql` (live on `origin/main`, applied per `migration list --linked`): `has_order_food boolean not null default true`, `has_dine_in boolean not null default false`, `has_catering boolean not null default false`. No restaurant-level gate restricts Order Food today (confirmed in the design and unchanged by this migration) — defaulting every row `true` reproduces current behavior exactly, not a guess |
| 2 | Staff can view and set all three flags per merchant from `aiorders-admin-hub` | **Pass** — `RestaurantDetails.tsx` (live on `origin/main`): three `Switch` rows (`has_order_food`/`has_dine_in`/`has_catering`, lines 502-539) bound to `checked`/`onCheckedChange`, each with a Yes/No `Badge`. `handleSave` sends `JSON.stringify(restaurant)` (the whole object, including the three fields) via `PUT .../admin-portal/restaurants/:id` — the existing, unmodified write path. The old `dine_in`-bound Switch is gone, not duplicated: only `has_dine_in` appears now, confirming the design's "repoint, don't add" instruction was actually followed |
| 3 | Dine-In/Catering tabs show only flag-`true` merchants; a `false`-flagged merchant never appears regardless of Open Now (negative case) | **Pass** — both query paths gate on the flag independently of `open_now`. RPC (`20260907120001_...sql`): `p_channel is null or (p_channel='order_food' and has_order_food) or (p_channel='dine_in' and has_dine_in) or (p_channel='catering' and has_catering)`. Fallback (`restaurants.ts` line 202): `.eq(CHANNEL_COLUMN[channel], true)`. `open_now`'s filter (`evaluateOpenNow`) only ever *removes* rows from a set the channel gate already produced — it cannot re-add a flag-`false` row, so the negative case holds under every `open_now` value by construction, not by a separate check |
| 4 | A flag-enabled, currently-closed merchant still appears by default with a status string; excluded only when Open Now is explicitly on | **Pass, both halves.** Logic (`ENG-045`, `evaluateOpenNow` in `restaurants.ts`): `isOpen === false` → `include: openNow !== true` (closed rows survive unless the caller explicitly asked to exclude them) and `status` is always set to the parser's label on a confirmed-closed row, open or not; `isOpen === true \| null` → always included, `status: null` — fail-open for unknown hours, matching the PRD's "don't hide" principle. `validateQueryParams` (line 93-94) parses `open_now` strictly to `true`/`false`/`undefined`, so an absent query param is `undefined`, never coerced to `true` — default-off confirmed at the parsing boundary, not just at the call site. UI (`ENG-047`, live on `origin/master`): `FilterBar.tsx` renders the "Open Now" chip on all three modes, unchecked by default (`filters.openNow` starts falsy, toggled only by user click); `RestaurantCard.tsx` renders `restaurant.status` when present (line 397-400) |
| 5 | Rollout/backfill question answered with evidence on file, not silently defaulted | **Pass** — `20260907120000_...sql`'s own header comment records the actual live-schema numbers checked before the migration was written: "243 rows total, 7 with `live_catering = true`, 241 with `dine_in = true`." The design's own conditional instruction (Data section: check whether `dine_in` exists; if so, backfill from it) was followed with the real answer, not guessed either way — `has_dine_in` backfills from the pre-existing `dine_in` column (`update ... set has_dine_in = dine_in`), and `has_catering` backfills from `live_catering`. This also resolves the design's own **named risk** ("Dine-In tab can go near-empty the moment the gate deploys") as a non-event: 241 of 243 restaurants already carried `dine_in = true`, so the backfill recovers real data for nearly the entire table rather than starting everyone at the PRD's own `false` default |

**All 5 criteria: pass.** No criterion required rework; nothing routes back
to `building`.

## Check the non-goals

Read each child's own diff scope (Components table cross-referenced against
what actually shipped) rather than re-deriving from the PRD alone:

- No operational-status engine (kitchen cutoffs, alcohol-license time,
  happy-hour scheduling, `getVenueOperationalStatus`) — `open_now` reuses the
  existing `openingHours.ts` parser as-is, ported not extended.
- No smart dine-in/catering filters (capacity, amenities, lead time, minimum
  spend) — none of the four diffs touch anything beyond the three boolean
  flags and the open-now/status pipeline.
- No promo badge overlay — untouched.
- No `restaurant-portal` changes anywhere in this family — confirmed by
  project field on all four children (`aiorders-api` ×2,
  `aiorders-admin-hub`, `restaurant-marketplace`); requirement 6's
  staff-only default (via `aiorders-admin-hub`, not self-service) held
  exactly as scoped.
- `admin-portal/handlers/restaurants.ts` (`updateRestaurant`) — confirmed
  genuinely untouched (design's own "no change" call, honored): the three
  new flags ride the pre-existing unconstrained `.update(updates)` path,
  which is a **known, separately-proposed** gap (`proposals.md`, 2026-08-29,
  corrected 2026-09-03), not something this family's diffs made worse or
  attempted to fix as a drive-by.

**None of the PRD's excluded scope present anywhere in the family.**

## Check the cost

PRD: "No new infrastructure, no new dependency expected." All four children
independently recorded `$0/month` at their own release-readiness hop
(`ENG-044` line 429, `ENG-045` line 595, `ENG-046` line 252, `ENG-047` line
365 of their own board files) — same Supabase project, no new vendor, no
`package.json`/lockfile touched in any of the three frontend/backend diffs.
Matches.

## Route

**All 5 criteria pass.** State → `verified`, owner → `eng-manager` on the
parent. See `ENG-026`'s own board-file log for the `building → shipped →
verified` transition (the `ADR-003`-class exemption for the `shipped` half).

**Also routed all four children `shipped → verified` in this same pass** —
not a separate acceptance-check run per child (the walk above already covers
each one's own AC slice directly against its own merged code), but each
child's own board file gets a short log line attributing its slice and
pointing back here, bringing all four back in line with every other settled
family on this board (see "Why this one is a from-scratch walk" above for
why they weren't already there).

## Step 6b — continue an approved sequence?

**Neither condition holds**, same reading `ENG-021`'s own check gave its
identically-bare G1. The PRD's own "Why this ticket is narrower than the
original request" section names three deferred items (operational-status
engine, smart filters, promo badge) in prose, explicitly framed as "a future
intake pass can pick them up individually" — not a "Feature shape and
sequencing" section naming a specific next ticket with real shape the way
`ENG-006`'s PRD did. Condition 1 (enough shape to draft from) isn't met.
Condition 2 fails independently regardless: the G1 decision was "Bare
approval, no comment" (PRD's own `## Decision` section) — no sequence
sign-off clearing `ENG-006`'s own bar. Nothing filed.

## What the estimate got right, and what it missed

`time_estimate: half a day to a day` (`M`). The work-breakdown notebook
already flagged this as likely to run past band once split into four
sub-tickets (per-ticket review/QA/security overhead the single-continuous-
build estimate didn't price in) — confirmed: `ENG-044` alone logged `~2h`
build plus a combined review+QA hop plus release-readiness; `ENG-046` `~20m`
build. Raw build time across all four stayed small: this is overhead from
ticket count, not from any single piece being harder than scoped, exactly as
the work-breakdown notebook predicted before any code was written — worth
noting as a case where the estimate-review loop worked as intended, not just
as a miss.

**What it missed, at the criteria level: nothing** — all five pass exactly
as scoped. **What's worth restating because this is the point the family
goes terminal:** the design's own single biggest named risk — the Dine-In
tab going near-empty the instant the channel gate deployed, before staff
could opt restaurants back in — did not materialize, and the reason is
traceable to a specific build-time decision rather than luck: `ENG-044`'s
own live-schema check (required by the design, not optional) found a real,
populated `dine_in` signal (241/243 rows) and backfilled from it instead of
leaving the PRD's own `false` default to stand. The next PRD with a
similarly-flagged "does real data exist for this backfill" risk: naming the
live check as a required build-time step, the way this design already did,
is what turned a plausible outage-shaped risk into a non-event.

## Also worth recording

**First family on this board where the parent's own acceptance-check found
real backfill work already owed and already done** — unlike `ENG-019`'s and
`ENG-021`'s families (both found "zero backfill work" specifically because
their children had already run this check individually), this family's gap
wasn't in the product criteria at all; it was in the department's own
bookkeeping. The dashboard-driven `shipped` transitions are efficient for
the approver (one click, all four children move at once) but invisible to
the chain — see the proposals.md addendum filed alongside this notebook.
Worth flagging plainly: this pass's own from-scratch walk is what closes the
gap for *this* family, but the mechanism that created the gap is still open,
and a same-shaped standalone ticket (no parent to force a recheck) would
have no equivalent safety net at all.
