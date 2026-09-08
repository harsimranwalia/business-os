---
id: ENG-047
title: FoodSwipe Open Now filter and channel display — consumer marketplace
project: restaurant-marketplace
type: feature
size: S
time_estimate: a few hours to half a day
time_spent:
time_remaining:
severity: P3
priority:
state: verified
owner: eng-manager
lane: full
blocked_on: 
blocked_from: 
source: approver
created: 2026-09-07
updated: 2026-09-07
branch: feat/ENG-047-foodswipe-open-now-and-channel-display
depends_on: [ENG-045]
blocks: []
parent: ENG-026
links:
  prd: agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md
  design: agents/architect/designs/ENG-026-foodswipe-channel-visibility.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-047.md
  test_plan: agents/qa/test-plans/ENG-047.md
  security_review: agents/security/reviews/ENG-047.md
  release:
  pr: https://github.com/harsimranwalia/restaurant-marketplace/pull/1
---

## Problem

FoodSwipe's discovery UI has no way to filter to currently-open merchants and
no way to show a closed merchant's status — it can only render whatever the
API already returns, which today carries neither `open_now` nor a `status`
field.

## Outcome

A new "Open Now" filter chip is visible on all three channel tabs, default
off. Turning it on excludes merchants the backend reports as currently
closed, for that channel only. A merchant the backend reports as closed but
included still renders its `status` string. Nothing about today's default
(`open_now` off) behavior changes for a consumer who never touches the chip.

## Notes

Design: `agents/architect/designs/ENG-026-foodswipe-channel-visibility.md` —
`## Components` and `## Interfaces` (`FilterBar.tsx` section). Depends on
`ENG-045`: this ticket only threads and renders the `open_now` param and
`status` field the backend handler provides — it does not implement the
open/closed evaluation itself.

**`types/index.ts`**: add `has_order_food`, `has_dine_in`, `has_catering`,
`status?: string | null` to `RestaurantCard`. `show_in_marketplace` stays
server-only — no acceptance criterion needs it client-side, don't add it.

**`services/api.ts` / `hooks/useRestaurants.tsx`**: thread a new `openNow`
boolean param through to the `open_now` query param.

**`FilterBar.tsx`** — new "Open Now" chip, styled like the existing
"Offers"/"Rating 4+" chips (`FilterBar.tsx:186-220`), but **shown for all
three modes** — those two are gated to `order-food`/`dine-in` only (line
187), this one is not, since Catering restaurants close too.

- **`openNow` is not reset when the active tab changes**, unlike
  `hasOffers`/`rating4Plus` (`RestaurantList.tsx:112-119`). This is a
  deliberate divergence, not an oversight — "show me who's open right now"
  is a standing intent about the current moment, not scoped to one channel.
- Not persisted to `localStorage`, matching `hasOffers`/`rating4Plus`'s
  precedent — a time-sensitive filter shouldn't outlive the session.

**`RestaurantCard.tsx`**: render `restaurant.status` when present, near the
card's existing secondary info. No client-side hours parsing here — the
server already computed the label; this is a pure render.

**`MobileBottomNav.tsx`/`Header.tsx`: no change** — the three tabs
(`order-food`/`dine-in`/`catering`) already exist and already name exactly
the three channels this ticket's backend half gates.

**Pagination under `open_now=true` is approximate, by design** (`ADR-010`,
governing `ENG-045`, not this ticket — read it if page counts look off
during testing). A page can under-return relative to `limit`, and an exact
count can overstate what's actually visible once the filter applies. This is
an accepted, inherited trade-off; it is not a bug to chase down here.

**AC ownership** (mapped in
`agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`): this
ticket owns AC4's UI half (the chip and the `status` render). It does not
independently prove AC3/AC4's filtering guarantee — it inherits that from
`ENG-045`'s own diff.

Branch from `origin/master` (this repo's default branch is `master`, not
`main`) in the `restaurant-marketplace` worktree, off `ENG-045`'s
already-merged/verified tip.

## Log

- 2026-09-07 `(created) → ready` (eng-manager, `work-breakdown`, `continue
  ENG-026` event pass) — sub-ticket of `ENG-026`, sequence 3,
  `depends_on: [ENG-045]` unmet, held at `ready`. `time_estimate` a few
  hours to half a day. Owner `eng-manager` while waiting, reassigned to
  `frontend` once `ENG-045` ships. Full reasoning:
  `agents/eng-manager/notebook/2026-09-07-eng026-work-breakdown.md`.
  `chained: none` — waiting on an unmet `depends_on: [ENG-045]`, nothing
  agent-actionable until it clears.

- 2026-09-07 `ready → building → in-review` (frontend, `continue ENG-047`
  event pass, `chained: ENG-047 — slot freed by ENG-046` from `ENG-046`'s own
  release-readiness hop). Reading map for `continue`: steps 6 and 6b, plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*). Mode check clean (`MODE=active`, repo-root `.env`).

  **`depends_on: [ENG-045]` re-verified fresh, not trusted off the board's own
  summary:** `ENG-045` is `blocked`, `blocked_on: approver`, PR #20 open on
  `aiorders-api` — satisfied per the 2026-09-07 Guards amendment ("an open PR
  does satisfy `depends_on`"), not yet `shipped`. Confirmed the actual API
  contract by reading `ENG-045`'s own shipped branch directly
  (`aiorders-api@5f35b92`, `handlers/restaurants.ts` and `utils/validation.ts`)
  rather than trusting this ticket's own Notes: query key is `open_now`
  (snake_case, unlike every other camelCase param on this endpoint), response
  field is `status` on list rows only — the three `has_*` flags are consumed
  server-side as filter inputs and only echoed on `handleRestaurantDetail`'s
  single-record response, not on discovery/list rows.

  **Branching note:** the ticket's own Notes said to branch "off `ENG-045`'s
  already-merged/verified tip," which doesn't apply — `ENG-045` lives in
  `aiorders-api`, a different repo from this ticket's own
  `restaurant-marketplace`, so there is no such tip here. Branched fresh off
  this repo's own `origin/master` (`ed2272d`) instead; the dependency is
  functional, not git-level. Filed as an observation
  (`observations.md`, this date) — a work-breakdown Notes-drafting gap for
  cross-repo DAG edges, not a defect in this ticket.

  **Built**, per the design's own Components rows: `types/index.ts`
  (`RestaurantCard` gains `has_order_food?`/`has_dine_in?`/`has_catering?`/
  `status?: string | null`; `FilterState` gains `openNow?: boolean`),
  `services/api.ts` (`open_now` query param), `hooks/useRestaurants.tsx`
  (param threaded, added to the fetch-triggering effect's deps),
  `FilterBar.tsx` (new "Open Now" chip, shown on all three modes unlike
  Offers/Rating 4+, folded into `hasActiveFilters`/`activeFilterCount`),
  `RestaurantList.tsx` (`openNow` passed to `useRestaurants`, folded into
  `hasAnyFilter`), `RestaurantCard.tsx` (renders `restaurant.status` in the
  existing meta row). Confirmed by reading the existing reset/clear effects
  first: `openNow` is correctly *not* reset on tab change (the reset effect
  merges, so simply not naming it there was enough) and correctly *is* reset
  by "Clear All" (that handler fully replaces state, so likewise not naming
  it there was enough) — both needed opposite code shapes to get the design's
  documented behavior, and neither needed a new line. Full detail and PR
  body: `agents/frontend/notebook/2026-09-07-eng047-build.md`.

  **Self-tested.** No `node_modules` in this worktree (first build here) —
  `npm install` first (no lockfile; see below). `npm run typecheck`: clean.
  `npm run build`: clean, 1803 modules, no new warnings. `npm run lint`:
  **could not run** — `.eslintrc.cjs` has a pre-existing syntax error (stray
  `]`, line 18) confirmed present on `origin/master` since this repo's first
  commit and never exercised by CI (`deploy-cf.yml` never calls `lint`); not
  fixed here (unrelated file). No test command registered for this repo
  (`config/projects.md`); none added — a thin wiring change with no new logic
  branch of its own, same precedent `ENG-046` used. Proposal filed
  (`proposals.md`, this date) covering both the broken lint config and this
  repo's missing, `.gitignore`d `package-lock.json`.

  Branch `feat/ENG-047-foodswipe-open-now-and-channel-display` pushed fresh
  off `origin/master` (`restaurant-marketplace@5dbb76c`, 6 files, 35
  insertions, 2 deletions). No PR yet — devops's release-readiness step.
  Machine WIP unaffected — still `1/1`, held by the `ENG-026` family.

  **2 transitions this pass** (`ready → building`, `building → in-review`),
  under the cap of 4.

  **6b:** grepped `openingHours\.ts|open_now|has_order_food|has_dine_in|
  has_catering` across `agents/`. All hits are `ENG-044`/`ENG-045`'s own
  migration/review/test-plan files (map/location, consistent with what this
  ticket built against), the already-filed `openingHours.ts` parser-mismatch
  proposal (confirms this ticket's own diff correctly leaves that file
  untouched), and `ENG-026`'s own parent-ticket log. No instruction found in
  conflict; nothing to fix.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep:** nothing to raise this pass — `in-review` needs no
  approver gate. Checked open `inbox/` items per the not-negotiable step 7:
  all carry their one-ever `nudged:` already, none newly due.

  **Observations/exceptions/journal:** two lines filed (`observations.md`,
  this date — the cross-repo branching-note gap above) plus the proposal
  above; no `exception-request:`; no G1/G2/G3/merge-request answered this
  pass, so no decision-journal entry is owed.

  Pre-pass and post-pass `sh departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-047`) and whole-board: see board index for result.

  `chained: ENG-047` — `in-review` is agent-owned (principal-engineer + qa
  combined hop next), not the approver, not blocked, not terminal, not held
  by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-047`
  before this pass exits.

  business-os itself left uncommitted through this edit — standing default
  per the open commit-convention question, not re-decided here.

- 2026-09-07 `in-review → in-qa → in-security` (principal-engineer + qa
  combined hop, `continue ENG-047` event pass, `chained: ENG-047` from this
  ticket's own prior hop). Reading map: steps 6/6b + not-negotiable set.
  Mode check clean. Pre-pass `eng-gate-check.sh` (`ENG-047`, whole-board):
  both exit 0.

  **Review: PASS, round 1.** Receipt: `agents/principal-engineer/reviews/ENG-047.md`.
  0/10 automatic failures; wire contract (`open_now`/`status`) independently
  confirmed against `ENG-045`'s shipped code; reset/Clear-All effects traced,
  not assumed. **Quality gate: PASS.** Test plan:
  `agents/qa/test-plans/ENG-047.md` — owns AC4's UI half only, covered by
  inspection (no suite exists for this project; proposal filed, see below).
  Full reasoning: `agents/principal-engineer/notebook/2026-09-07-review-log.md`,
  `agents/qa/notebook/2026-09-07-coverage-gaps.md`.

  **2 transitions** (`in-review → in-qa`, `in-qa → in-security`), under cap
  of 4. `owner: principal-engineer → security`. Machine WIP unaffected —
  still `1/1`, held by the `ENG-026` family.

  One proposal filed (missing test harness, `restaurant-marketplace` —
  `proposals.md`, this date) and one same-day proposal row corrected in
  place (a wrong `ENG-032`/`ENG-034` citation on the lint-config row).

  `chained: ENG-047` — `in-security` is agent-owned (`security` next). Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-047`
  before this pass exits.

  business-os left uncommitted — standing default, not re-decided here.

- 2026-09-07 `in-security → ready-to-ship` (security, `continue ENG-047`
  event pass, `chained: ENG-047` from this ticket's own prior hop). Reading
  map for `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b,
  9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check
  clean (`MODE=active`, repo-root `.env`). Pre-pass `eng-gate-check.sh`
  (`ENG-047`, whole-board): both exit 0.

  **Ran `skills/security-gate/SKILL.md` in full.** Project autonomy: L1
  (`config/projects.md`), so no client-repo (L0) restriction applies. Fetched
  fresh (`ed2272d`); diff unchanged from review/QA's own account — six files,
  35/-2, one commit (`5dbb76c`), `0 1` ahead/behind, confirmed via
  `git rev-list --left-right --count`.

  **Threat model:** the only attacker-reachable input is a boolean
  (`openNow`), serialized via `URLSearchParams` — never free text; the only
  new inbound field (`restaurant.status`) is read-only, rendered as a plain
  JSX text node. No new route, no new capability, no session touched — this
  page is and remains unauthenticated. Data exposed (`status`, a
  closed/hours label) is intended business-status text, same classification
  `ENG-044`/`ENG-045`'s own gates already gave the underlying column/field.
  The three new `has_*` fields on `RestaurantCard` are confirmed dead weight
  today — re-verified directly against `aiorders-api`'s shipped `ENG-045`
  handler (discovery/list rows never populate them) and against every
  consumer of the type in this repo (none is the detail page).

  **Verified directly, not taken on the review's word:** grepped both touched
  render files for `dangerouslySetInnerHTML` (zero hits — `status` cannot
  become markup regardless of content); confirmed the `Check` icon import is
  pre-existing (`git blame` → `8fe3b8d3`, 2026-09-02), not a new dependency;
  scanned the diff and the branch's one commit for
  key/secret/password/token/bearer/AWS/PEM patterns (zero matches); confirmed
  no `package.json`/lockfile in the diffstat.

  **OWASP A01–A10:** nine `n/a` (each with its own reason — no route, no
  crypto, no config, no auth, no CI/CD, no logging surface, no SSRF anywhere
  in this diff), one checked (A03 Injection — clean: safe query-param
  encoding, React's automatic text-node escaping, no ORM/shell/SQL anywhere
  in a frontend-only diff). LLM checklist: n/a, no model/agent/tool/MCP
  surface touched. Negative-case testing (baseline step 6): n/a — no authz
  surface exists on this diff to exercise a wrong-tenant/role/token case
  against.

  **Verdict: PASS.** Zero findings, zero backlog notes, nothing inherited
  from a sibling ticket to re-flag (unlike `ENG-046`'s carried-forward
  `updateRestaurant` allow-list note — this diff has no write path at all).
  Receipt written: `agents/security/reviews/ENG-047.md`,
  `links.security_review` set in the same write. Full reasoning is the
  receipt itself; no separate notebook entry needed for a clean pass.

  **1 transition** (`in-security → ready-to-ship`), under the cap of 4.
  `owner: security → devops`. Machine WIP unaffected — still `1/1`, held by
  the `ENG-026` family.

  **6b:** not applicable — `links.security_review` follows the
  already-established receipt-path convention this board already uses; no
  new instruction, state name, or config key introduced.

  **Dead-end sweep (scoped to this event):** no other ticket touched.

  **Notify sweep (step 7):** nothing to raise — a `pass` security verdict is
  not itself approver-facing. Checked open `inbox/` items:
  `2026-09-07-eng045-merge-request.md` (notified ~10:58, well under 24h) and
  `2026-09-07-eng046-merge-request.md` (notified ~12:16, well under 24h) both
  need no nudge yet; every other open item already carries its one-ever
  `nudged:`.

  **8b:** no new observation — nothing surfaced this pass outside what the
  receipt itself already records. No `exception-request:` found. **8c:** n/a
  — no G1/G2/G3/merge-request answered this pass (the security verdict is
  this gate's own, not an approver decision), so no decision-journal entry is
  owed.

  **Board update:** this ticket's own row (`state`, `owner`) and
  `links.security_review`; this entry appended;
  `agents/eng-manager/board/_index.md`'s own dated-entry log updated the same
  way (see its own entry for this pass). Live file held three dated entries
  before this one; oldest (`continue (ENG-046)`: security gate — PASS retry)
  rolled to `_index-archive.md` per the keep-three rule, done before that
  entry was written so the count stays at three.

  Post-pass `eng-gate-check.sh`, scoped (`ENG-047`) and whole-board: both
  exit 0, clean.

  `chained: ENG-047` — `ready-to-ship` is agent-owned (`devops` next,
  release-readiness hop), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-047`
  before this pass exits — confirmed queued behind this still-in-flight pass
  (`traces/eng-loop-2026-09-07.log`, `13:11:24 continue — pass in flight,
  queued as pending`), not lost; will drain the moment this pass exits. (The
  same log also shows this pass's own launch needed one retry — an
  all-accounts-limited NEVER STARTED at 12:58:18, refunded, back-off armed
  300s, then the queued event drained and actually launched at 13:03:27 —
  self-healing per the documented retry mechanics, not a broken chain.)

  business-os itself left uncommitted through this pass's edits (ticket
  file, the new security review, this board index) — same standing default
  every pass on this board has used; the commit-convention question remains
  open, not re-decided here. No project-repo commit this hop — read-only
  review, no application code changed.

- 2026-09-07 `ready-to-ship → blocked` (devops, `continue ENG-047` event
  pass, `skills/release-runner/SKILL.md` run step by step). Reading map for
  `continue`: steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*; *The four lanes*; *Guards*). Mode check clean
  (`.env` → `MODE=active`). Pre-pass `eng-gate-check.sh`, scoped
  (`ENG-047`) and whole-board: both exit 0, clean.

  **Step 1 (window): skipped.** `restaurant-marketplace` is registered L1
  (`agents/eng-manager/config/projects.md`) — opening a PR is not a
  release, so the window check doesn't apply.

  **Step 2 (upstream gates), all three re-read fresh from the receipt
  files, not from this ticket log's own account:** review
  (`agents/principal-engineer/reviews/ENG-047.md`, pass, round 1, 0/10
  automatic failures), quality (`agents/qa/test-plans/ENG-047.md`, pass,
  AC4's UI half by inspection), security
  (`agents/security/reviews/ENG-047.md`, pass, zero findings). No migration
  owed — confirmed no `ENG-047-*.md` file under
  `agents/database/migrations/`, correct for a pure frontend diff.

  **Step 3 (readiness gate), no blocking failure:**
  - *Rollback:* no migration, no stored-state change of its own —
    reverting the merge (once merged) fully undoes this diff.
  - *Observability:* read `useRestaurants.tsx` directly rather than
    assuming — its existing fetch path already wraps every request in
    try/catch and sets a generic `error` state on failure, unconditional on
    which params are set; the new `openNow` param rides the same path,
    nothing new to instrument.
  - *Cost:* $0/month — no new dependency (`package.json`/lockfile absent
    from the diffstat), no new infrastructure.
  - *Window:* n/a, L1 (step 1).

  **Step 4 (route):** worktree
  (`~/Documents/projects/_eng/restaurant-marketplace`) re-checked fresh,
  not assumed unchanged since the security hop: clean at pass start, `git
  fetch origin master`, `HEAD` at `5dbb76c` matching every gate's cited
  head, `0 1` ahead/behind (`git rev-list --left-right --count
  origin/master...HEAD`), `git diff origin/master...HEAD --stat` still
  exactly the six files review/QA/security already characterized (35
  insertions/2 deletions) — no drift. `git ls-tree -r origin/master
  --name-only | grep -i workflow` → `deploy-cf.yml`, `on: push: branches:
  [master]` only, no `pull_request` trigger — opening this PR carries no
  auto-deploy risk. `gh pr list --head
  feat/ENG-047-foodswipe-open-now-and-channel-display --state all`
  confirmed no PR already existed for this branch.

  Opened `restaurant-marketplace` PR #1
  (https://github.com/harsimranwalia/restaurant-marketplace/pull/1) — this
  repo's first-ever PR from this department. Body: what changed, what it
  deliberately doesn't do, the three gate receipts with paths, the
  independent drift/build/typecheck re-check, safe merge-ordering relative
  to `ENG-045`, what to review hardest (the three dead-weight `has_*`
  fields), and the rollback/observability/cost/window reasoning above —
  built from the frontend build hop's own pre-drafted PR-body section
  (`agents/frontend/notebook/2026-09-07-eng047-build.md`) rather than
  written from scratch.

  Wrote `inbox/2026-09-07-eng047-merge-request.md`, plain `pr_url:` string
  (single repo). `time_estimate: a few hours to half a day` carried from
  this ticket's own frontmatter. `lib/eng-notify.sh raise` exited 0;
  confirmed sent from `traces/eng-notify-2026-09-07.log` (`sent: active
  2026-09-07-eng047-merge-request.md`, `13:16:15`); stamped `notified:
  2026-09-07T13:16:15` on the item by hand, copied verbatim from the log.

  State `ready-to-ship → blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, `owner: devops → approver`, `links.pr` set. No G3 — L1
  has none; the PR merge is the human gate. No release record yet — L1's
  actual deploy (merge triggers `deploy-cf.yml`) and the release record
  both wait for merge detection on a future pass, per the skill's own step
  4 L1 row / step 7 split.

  **1 transition** (`ready-to-ship → blocked`), well under the cap of 4.

  **Machine WIP / family slot — re-derived fresh, not carried forward from
  this ticket's own prior entries or `ENG-046`'s own board-file paragraph.**
  Read all three other `ENG-026` siblings directly: `ENG-044` — `shipped`.
  `ENG-045` — `blocked`, `blocked_on: approver`, PR #20 open
  (`aiorders-api`). `ENG-046` — `blocked`, `blocked_on: approver`, PR #10
  open (`aiorders-admin-hub`). Parent `ENG-026` itself: `building`.

  With this hop's own transition, **every `ENG-026` child is now either
  `shipped` or parked on the approver, and this ticket was the family's
  last undispatched child** — unlike `ENG-046`'s own hop, which could chain
  straight into this ticket as the next sibling, there is no sibling left
  here to fill the freed slot. Per `eng_build_loop.md` Guards (amended
  2026-09-07(b)): *"the next child with a satisfied dependency, else the
  top of To-do — same pass, `continue {NEXT-ID}` before exit."* Swept To-do
  fresh (`ENG-018`/`ENG-028`/`ENG-042`/`ENG-043`) and found nothing
  startable — same conclusion recent dispatch-scoped passes reached for the
  same four tickets — so fell back to the held-for-slot pool of `designed`
  tickets with a completed design and no one-way door, same precedent
  `ENG-019`/`ENG-020`/`ENG-021`/`ENG-026` each already set. `ENG-027` is the
  sole `now`-priority ticket in that pool (the three tickets that used to
  rank ahead of it by id — `ENG-020`, `ENG-021`, `ENG-026` — have all since
  shipped or, for `ENG-026`, dispatched their own last child this same
  pass), its `depends_on: [ENG-006, ENG-007]` re-confirmed `verified`/
  `verified`, and its one-way-door question was already closed at its own
  2026-09-05 tech-design pass. Dispatched: `designed → ready`, `owner:
  architect → eng-manager`, no G2 (reused, not re-derived). Full reasoning:
  `ENG-027`'s own board-file log and this same date's entry on
  `agents/eng-manager/board/_index.md`.

  **6b:** not applicable — the merge-request item follows this board's own
  established format exactly (`ENG-044`'s, `ENG-045`'s, `ENG-046`'s); no
  new receipt path, state name, config key, or cross-file artifact rule
  introduced.

  **Dead-end sweep (scoped to this event):** `ENG-044`/`ENG-045`/`ENG-046`/
  `ENG-026` read only, to derive the family-slot state above. `ENG-027` is
  the one other ticket actually written this pass — the slot-fill dispatch
  this same event's own chain obligation requires, not scope creep.

  **Notify sweep (step 7, whole inbox, not just this ticket):** this hop's
  own merge request raised and stamped above. Checked every other open
  `inbox/` item fresh: `ENG-016`'s continue-Piece-2 question, `ENG-018`'s
  G1, `ENG-028`'s rescope G1, `ENG-042`'s and `ENG-043`'s items, and
  `PROP-2026-W36` all already carry their one-ever `nudged:` — no action.
  `ENG-045`'s merge request (`notified: 10:57:56`, ~2h20m old) and
  `ENG-046`'s (`notified: 12:15:34`, ~1h old) are both well under the 24h
  threshold — no action.

  **8b:** no new observation filed — nothing surfaced this pass beyond what
  the merge-request item and the family/To-do derivation above already
  record. No `exception-request:` found. **8c:** n/a — no G1/G2/G3/
  merge-request *answered* this pass (one merge request was raised), so no
  decision-journal entry is owed.

  Post-pass `eng-gate-check.sh`, scoped (`ENG-047`), scoped (`ENG-027`), and
  whole-board: all three exit 0, clean.

  `chained: ENG-027` — slot freed by `ENG-047`, and this ticket was the
  `ENG-026` family's last undispatched child, so the fill drew from the
  held-for-slot pool rather than a sibling. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-027`
  before this pass exits. This ticket itself is not re-chained — it is
  parked on the approver (`blocked_on: approver`), which step 9 never
  chains.

  business-os itself left uncommitted through this pass's edits (this
  ticket file, `ENG-027`'s own board file, `_index.md`, the new merge-
  request item) — same standing default every pass on this board has used;
  the commit-convention question remains open, not re-decided here. No
  `restaurant-marketplace` code commit this hop beyond the PR open itself —
  the code commit (`5dbb76c`) was already made and pushed in the build
  hop.

- `2026-09-07` `blocked → shipped` (control center, merge detected) — `feat/ENG-047-foodswipe-open-now-and-channel-display` is an ancestor of `origin/master`. Advanced from the dashboard rather than by a build-loop pass; the loop's own ancestry check on its next pass will agree.
- `2026-09-07` `shipped → verified` — this dashboard flip never fired `continue ENG-047`, so `acceptance-check/SKILL.md` never ran on this ticket individually (unlike every sibling family's children — see `proposals.md`'s 2026-09-07 dashboard-bypass row, addendum (4)). Closed as part of `ENG-026`'s own parent-level closing pass instead: this ticket's own AC slice (PRD AC4's UI half — the "Open Now" chip, default off, shown on all three modes; `restaurant.status` rendered on the card when present) walked directly against `FilterBar.tsx`/`RestaurantCard.tsx` on `origin/master`, plus `services/api.ts`/`useRestaurants.tsx` correctly threading `open_now` to match the backend's own param name. Deploy confirmed via this repo's own Cloudflare Pages run (`success`, `2026-09-07T20:37:57Z`, against the exact merge commit). Pass. Full walk: `agents/product-manager/notebook/2026-09-07-eng026-acceptance.md`. `owner` stays `eng-manager`.
