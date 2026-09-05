---
id: ENG-039
title: Broadcasts tab — composer, drip editor, and report UI
project: restaurant-portal
type: feature
size: M
time_estimate: ~1-1.5 days
time_spent: build (single session) + review/quality (combined hop, single session) + security (single session) + release-readiness (single session, pass — PR opened) + merge detection + acceptance-check (pass)
time_remaining: none — verified
severity: P2
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-04
updated: 2026-09-05
branch: feat/ENG-039-broadcasts-tab-composer-and-report-ui (restaurant-portal@2f438e0)
depends_on: [ENG-038]
blocks: []
parent: ENG-019
links:
  prd: agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md
  design: agents/architect/designs/ENG-019-restaurant-marketing-broadcasts.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-039.md
  test_plan: agents/qa/test-plans/ENG-039.md
  security_review: agents/security/reviews/ENG-039.md
  release: agents/devops/releases/2026-09-05-restaurant-portal-ENG-039.md
  pr: https://github.com/harsimranwalia/restaurant-portal/pull/3
---

## Problem

Once `ENG-038`'s API exists, owners still have no in-product surface to
compose a campaign, build a drip sequence, pick an audience, or see what a
past send produced.

## Outcome

- **`pages/autopilot/Automations.tsx`** — third `TabsTrigger`/`TabsContent`
  ("Broadcasts"), rendering the new page component. No change to the
  existing "Automation Flows"/"History" tabs.
- **`pages/autopilot/Broadcasts.tsx`** — campaign list + create/edit composer
  entry + per-campaign report view. Split into sub-components if any piece
  nears the ~400-line standards threshold.
- **`components/autopilot/BroadcastComposer.tsx`** — compose form: audience
  picker (all customers / inactive-for-N-days), one-time vs. drip step
  editor (owner-set delay per step, e.g. immediately / +3 days / +7 days),
  coupon attach (existing offers only — this ticket doesn't mint new ones).
- **`components/autopilot/BroadcastReport.tsx`** — sent/pending/failed by
  channel; redemptions + revenue when a coupon is attached; email
  open/click counts when present.
- **`services/brandPortalApi.ts`** — methods matching `ENG-038`'s
  `broadcasts_*` actions, same idiom as the existing `getOffers`/
  `createOffer` methods.
- **`types/broadcasts.ts`** — `BroadcastCampaign`, `BroadcastStep`,
  `BroadcastAudience`, `BroadcastReport`.
- **`hooks/use-broadcasts.ts`** — `useBroadcasts`, `useBroadcast`,
  `useBroadcastReport`, matching `use-autopilot.ts`'s existing hook shape.

**No change** to `pages/autopilot/Templates.tsx`, `types/autopilot.ts`, or
any reactive `Automations` flow — explicit non-goal, this ticket is additive
only.

## Notes

No ADR governs UI structure directly — this ticket consumes `ENG-038`'s
contract exactly as specified in the design's `## Interfaces` section,
nothing more (validation, audience resolution, and consent enforcement all
live server-side; this ticket doesn't duplicate any of it client-side beyond
ordinary form validation for UX).

`update_broadcast`'s active-or-later rejection (`ENG-038`) means the
composer needs a read-only/locked state once a campaign starts sending, not
a client-side guess about when to disable editing — reflect whatever
`get_broadcast`'s `status` says.

Surfaces AC1–AC5 (composer send-now/schedule, drip step editor, audience
picker, ROI report display, send-history view). AC6 (unsubscribe) and AC7
(server-side tenant rejection) are fully backend-enforced — nothing for this
ticket to add. Full surface-split and sizing reasoning:
`agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`.

## Log

- `2026-09-04` `(created) → ready` (eng-manager, `work-breakdown`, `continue
  ENG-019` event pass) — sub-ticket of `ENG-019`, sequence 3 of 3,
  `depends_on: [ENG-038]` unmet, held at `ready`. `time_estimate` ~1-1.5
  days. Owner `eng-manager` while waiting, reassigned to `frontend` once
  `ENG-038` ships. `chained: none` — waiting on an unmet `depends_on:
  [ENG-038]`, nothing agent-actionable until it clears.

- `2026-09-05` no state change (product-manager, `scheduled` event pass,
  02:00 PDT — step 5 merge detection). `ENG-038`'s `aiorders-api` PR #16
  confirmed merged this same pass via local git ancestry, cross-checked with
  `gh pr view`, then carried through a full acceptance-check (all 7 owned
  criteria pass) to `verified` (see `ENG-038`'s own board-file log) —
  `depends_on: [ENG-038]` is now satisfied, read literally as *shipped/
  verified* per the `ENG-016`/`ENG-019` work-breakdown precedent.

  **Not transitioned to `building` in this pass** — same precedent this
  board has set on every prior sub-ticket handoff (`ENG-032`, `ENG-034`,
  `ENG-038` itself): a `scheduled` sweep does not perform new implementation
  work. The next hop is a real code edit against `restaurant-portal` (the
  Broadcasts tab, composer, drip editor, report UI) and belongs in its own
  dedicated session. This is the family's last sub-ticket — no other member
  remains to pick, so there is no ordering choice to make. Machine WIP
  unaffected — still the `ENG-019` family's own slot (`1/1`).

  **0 transitions.** `chained: ENG-039` — fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-039` before this pass exits, so a dedicated session performs
  `ready → building`.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.

- `2026-09-05` `ready → building` (frontend, `continue` event pass, context
  `ENG-039` — this ticket's own turn, per the prior pass's own `chained:
  ENG-039`). Narrow scope per the event's own contract — this ticket only.
  Reading map for `continue`: steps 6 and 6b (design already complete, no
  mid-PRD checkpoint applies) plus the not-negotiable set (1, 7, 8b, 9, 10;
  *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check clean
  (repo-root `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-039`) and
  whole-board: both exit 0, clean.

  **WIP re-checked fresh off the board index and this ticket's own
  frontmatter**, not trusted from the checkpoint: still `1/1`, held by the
  `ENG-019` family (parent still `building`, this is its last sub-ticket).

  **Worktree branch set up clean.** `~/Documents/projects/_eng/restaurant-portal`
  was on `feat/ENG-032-catering-portal-stages-and-itemized-view` (that
  ticket's own already-merged, already-terminal branch; clean tree, nothing
  uncommitted, no prior pass died mid-work) — not the parent-slug slip
  `ENG-031`/`ENG-032` each hit, just a stale checkout left over from the last
  ticket built in this worktree. `git fetch origin`, confirmed local `main`
  already matched `origin/main` (`5276a53`, `ENG-032`'s own merge commit).
  `main` itself is checked out in the human's own working copy
  (`~/Documents/projects/aiorders/restaurant-portal`), so branched directly
  off `origin/main` — `git checkout -b feat/ENG-039-broadcasts-tab-composer-and-report-ui
  origin/main` — rather than checking out local `main` first in this
  worktree.

  **Read the actual merged `ENG-038` code before writing any frontend type**,
  not just the design's Interfaces prose — `brand-portal/broadcasts.ts`, its
  migration (`20260904140000_broadcast_campaigns.sql`), and `brand-portal/index.ts`'s
  routing, all on `origin/main`. Two places this diverged from the design/
  ticket's own wording, both resolved in favor of the live code: the
  `getOffers`/`createOffer` methods both cite as the idiom to match in
  `brandPortalApi.ts` don't exist there (that file's own `callApi(action,
  payload)` pattern, already used by `get_catering_requests`/`get_feedback`,
  is what the 8 new broadcast methods actually follow instead — same router,
  same idiom, just not the two names cited); and the report's real shape has
  no per-channel pending/failed breakdown (`broadcast_campaign_recipients`
  carries no `channel` column), so `BroadcastReport.tsx` renders
  `recipients_by_status` (no channel split) and `delivery_by_channel`
  (sent/opened/clicked only) as the two groupings the API actually returns,
  not the "sent/pending/failed by channel" phrasing read literally. Full
  reasoning: `agents/frontend/notebook/2026-09-05-eng039-broadcasts-tab-composer-and-report.md`.

  **Built all 7 `restaurant-portal` rows of the design's `## Components`
  table**, no more, no fewer: `types/broadcasts.ts` (new — wire types +
  `BROADCAST_DELAY_OPTIONS`/`BROADCAST_STATUS_LABELS`), `services/brandPortalApi.ts`
  (modify — 8 methods for `list/get/create/update/pause/resume/cancel_broadcast`
  + `get_broadcast_report`, `BrandPortalApiResponse` gains an optional
  `pagination` field matching `autopilotService.ts`'s own `AutopilotApiResponse`
  shape), `hooks/use-broadcasts.ts` (new — `useBroadcasts`/`useBroadcast`/
  `useBroadcastReport` query hooks plus create/update/pause/resume/cancel
  mutation hooks, matching `use-autopilot.ts`'s shape including its flat,
  unabstracted mutation-hook style rather than a generic factory), 
  `components/autopilot/BroadcastComposer.tsx` (new — name/type/audience-
  picker/coupon-attach/drip-step-editor/schedule form; fetches its own edit
  target via `useBroadcast(restaurantId, editCampaignId)` rather than
  requiring the caller to have the full record; locks to read-only via a
  single `<fieldset disabled>` once `editCampaign.status` is outside
  `draft`/`scheduled`, never a `scheduled_send_at`-vs-now guess per the
  ticket's own Notes), `components/autopilot/BroadcastReport.tsx` (new —
  recipient-status counts, delivery-by-channel, coupon redemptions/revenue
  when `offer_id` is set), `pages/autopilot/Broadcasts.tsx` (new — paginated
  list, new-broadcast entry point, per-row edit/pause-resume/cancel/report
  actions, cancel behind an `AlertDialog` confirm), `pages/autopilot/Automations.tsx`
  (modify — third `TabsTrigger`/`TabsContent`, existing "Automation Flows"/
  "History" tabs byte-for-byte unchanged otherwise). `types/autopilot.ts`,
  `pages/autopilot/Templates.tsx`, and every reactive `Automations` flow
  confirmed untouched (design's own explicit non-goal). Reused rather than
  rebuilt: `EmailEditor` (existing component, single-entry `customer_name`
  variable list) for step email bodies, `useOffers()` (existing hook) for
  the coupon-attach picker, the Popover+Calendar shape (not the Canadian-
  timezone logic) from `ScheduleVisitDialog.tsx` for the schedule picker.

  **Self-tested.** `npm run lint`: 96 problems, exact count and file set
  `ENG-032`'s own log already established as this repo's true baseline
  ("Lint 96/0-new... round 1's logged '63' was stale") — grepped the full
  output for every new/touched filename, zero hits, confirmed 0 new rather
  than assumed from the total staying flat. `npm run build`: clean; bundle
  delta measured directly (stash/build/pop, not assumed): `1,976.47 kB →
  2,003.65 kB` raw (+1.4%), gzip `552.63 kB → 558.85 kB` (+1.1%) — under the
  standards' 10%-growth-needs-justification line. `npm run test`: 5/5
  passed (4 files), all pre-existing and unchanged. **No new test file** —
  this is additive feature work with no bug being fixed, and this repo has
  no established per-component test convention for new UI beyond the one
  regression test `ENG-032` itself added for an actual bug; same position
  that ticket's own build hop was in, resolved the same way. QA's gate is
  where coverage for this ticket's owned criteria (AC1–AC5 per the
  work-breakdown's own AC-mapping) gets written next.

  **Committed and pushed**, single repo: `restaurant-portal@9a9ec86`
  (`feat/ENG-039-broadcasts-tab-composer-and-report-ui`, tracking
  `origin/feat/ENG-039-broadcasts-tab-composer-and-report-ui`); no PR opened
  yet — devops's own release-readiness hop, same precedent every prior
  building hop on this board has used. PR body drafted here:

  *restaurant-portal* — title: `Broadcasts tab: composer, drip step editor,
  and report view (ENG-039)`. Body: what's new (a third "Broadcasts" tab on
  the Automations page — a paginated campaign list; a composer for a
  one-time message or a 2+-step drip, with an audience picker (all customers
  / inactive-for-N-days), per-step email and/or SMS content, an optional
  existing-offer coupon attach, and send-now-or-schedule; the composer locks
  to read-only once a campaign has started sending, reflecting the server's
  own `status`; row actions to pause/resume/cancel a campaign; a report view
  showing recipient status counts, delivery-by-channel, and coupon
  redemptions/revenue when one is attached); self-test summary (lint
  96/0-new, build clean at +1.4% bundle, existing 5/5 suite green, no new
  test — reasoning above); out of scope (no change to `Templates.tsx`,
  `types/autopilot.ts`, or any reactive `Automations` flow — ticket's own
  non-goal; AC6 unsubscribe and AC7 tenant rejection are fully
  backend-enforced per the work-breakdown's own AC-mapping, nothing added
  here; the 10k-recipient cap and 24h campaign-interval cap are surfaced only
  as whatever error the server returns, never re-validated client-side).
  Depends on `ENG-038` (merged, verified) for the underlying API — sequencing
  note only, not a blocker for this PR merging on its own.

  **1 transition** (`ready → building`), under the cap of 4. Machine WIP
  unaffected — still `1/1`, `ENG-019` family (parent still `building`,
  waiting on this, its own last sub-ticket). Approver-facing WIP and
  approval cap unaffected — no gate touched this hop.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** the three open `inbox/` items' `notified:`/`nudged:`
  checked fresh against the 24h threshold (current
  `2026-09-05T09:46:35Z`) — `ENG-027`/`ENG-028` already carry their one-time
  `nudged:` (2026-09-04T14:48:03 / 2026-09-04T09:13:37); `ENG-016`'s
  continue-Piece-2 question (`notified: 2026-09-04T10:58:06`, no `nudged:`
  yet) is at ~22h48m, still under 24h. Nothing crossed, nothing raised this
  pass. **Observations filed:** none — the two contract discrepancies above
  were resolved inline, same-file, no process-level pattern to flag (unlike
  `ENG-032`'s worktree-branch-slip observation, which was a second
  occurrence of a cross-ticket mechanism gap).

  **Step 6b: not run** — nothing this hop writes is a rule about a
  business-os artifact path, state name, or config key; every new file is
  product code consuming an already-fixed backend contract, same reasoning
  `ENG-032`'s own build hop recorded for its status strings and jsonb keys.
  **Journal:** not applicable — no G1/G2/G3 or merge request answered this
  pass.

  `chained: ENG-039` — `building` is agent-owned (next hop `in-review`,
  owned by `principal-engineer` per `definition-of-done.md`'s state table,
  combined with the quality gate per `eng_build_loop.md` step 6); not the
  approver, not blocked, not terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-039` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-039`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-05` **review round 1: PASS / PASS** (principal-engineer + qa,
  `continue` event pass, context `ENG-039`, combined review+quality hop per
  `eng_build_loop.md` step 6). Reading map for `continue`: steps 6 and 6b
  plus the not-negotiable set (1, 7, 8b, 9, 10). Mode check clean
  (`MODE=active`). Pre-pass `eng-gate-check.sh`, scoped and whole-board:
  both exit 0. WIP re-checked fresh: still `1/1`, `ENG-019` family.

  Worktree (`~/Documents/projects/_eng/restaurant-portal`) fetched fresh:
  local `main` matches `origin/main` (`5276a53`) with no drift, branch on
  its own head (`9a9ec86` at pass start). Read the ticket, the `ENG-019`
  design and PRD, `engineering-standards.md`, both new-hop notebooks
  (`agents/frontend/notebook/2026-09-05-eng039-...md`,
  `agents/eng-manager/notebook/2026-09-04-eng019-work-breakdown.md`), and —
  rather than trusting either notebook's account of the backend contract —
  read `aiorders-api@63f5635`'s actual `brand-portal/broadcasts.ts` and its
  migration directly: every field on `types/broadcasts.ts` traced against
  the live DB columns and every handler's actual response shape
  (`listBroadcasts`, `getBroadcast`, `updateBroadcast`,
  `getBroadcastReport`/`buildDeliveryByChannel`) — exact match, no drift
  found this round.

  **Automatic-failure scan: 0/10** (secret, silent swallow, missing
  bug-fix test, `any`, unbounded query, new dependency, unrelated refactor,
  commented-out code/TODO, datastore bypass, auth/payment/deletion path —
  grepped all 7 build-hop files plus both new test files for the last few
  directly). Full reasoning, the AC-by-AC contract trace, and two
  non-blocking findings (`F1`: a newly-added drip step's default delay
  guess can land outside `BROADCAST_DELAY_OPTIONS`, so its `Select` shows
  no visible label until manually reselected — data stays valid, display
  only; `F2`: `BroadcastComposer.tsx` is 526 lines at creation, past the
  ~400-line smell threshold, with two natural extraction points named):
  `agents/principal-engineer/reviews/ENG-039.md`.

  **Quality gate: closed a real gap rather than accepting the build hop's
  own framing.** The build hop argued no per-component test convention
  exists on this repo beyond one bug-fix regression test — checked against
  `ENG-032`'s own test plan directly rather than taken on trust, and that
  claim is only half true: two of that ticket's three new tests were
  acceptance-criterion tests for new UI, not regressions. `restaurant-portal`
  has a real, working suite (unlike `ENG-034`'s `config-site-builder`,
  which genuinely has none) and this ticket owns 5 significant ACs, so
  wrote the missing coverage in this same hop rather than carrying the gap
  forward: `BroadcastComposer.test.tsx` (6 tests: locked-vs-editable state,
  audience-mode/inactive-days restore, schedule prefill, multi-step drip
  content, and a fresh-compose create-payload test) and
  `BroadcastReport.test.tsx` (3 tests: null-vs-zero coupon redemptions,
  recipient-status defaults, email-only open/click display) — mocking
  `@/hooks/use-broadcasts`/`@/hooks/use-offers` at the hook boundary (no
  existing precedent in this repo for a real `QueryClientProvider` in a
  test, and every assertion is about rendered output). Every assertion
  avoids Radix `Select`/`Switch` open-state interaction (no
  `@testing-library/user-event` dependency in this repo, and
  `fireEvent.click` doesn't reliably open a Radix trigger in jsdom) —
  coverage comes from native-element state, plain text, and, for the
  create path, the exact mutation payload. **Three mutations run live**
  (`isLocked` hardcoded `false`; `BroadcastReport`'s `!== null` changed to
  `!== undefined`; the create-payload's `email_subject` forced to `null`)
  — all three failed for the reason they exist, then reverted, then
  re-confirmed green. One coverage gap named rather than left implicit:
  the `scheduleLater` toggle's own click interaction isn't exercised
  (same Radix constraint), though both code paths it selects between are
  covered from other angles. Full detail, the AC-coverage table, and the
  Result block: `agents/qa/test-plans/ENG-039.md`.

  **Independently re-run this session:** `npm run lint` — 96 problems, 0
  new (grepped both new test filenames across the full output). `npm run
  build` — clean, bundle unchanged (`2,003.65 kB`, test files don't ship).
  `npx tsc --noEmit` — 0 errors. `npm run test` — **14 passed, 0 failed, 0
  skipped** (6 files: 4 pre-existing unchanged + 2 new). No open P0/P1
  against this ticket (`agents/qa/bugs/_index.md`).

  **Committed and pushed, two commits, same branch:** `b766b41` ("Add
  quality-gate coverage for the Broadcasts composer and report") and
  `2f438e0` ("Cover the fresh-compose send-immediately path in
  BroadcastComposer") — both on
  `feat/ENG-039-broadcasts-tab-composer-and-report-ui`, both pushed to
  `origin`. `branch`/frontmatter updated to the new head. `links.review`
  and `links.test_plan` set to the two receipts written this hop.

  **Observation filed** (`observations.md`): the reused, unmodified
  `EmailEditor` component's existing raw-HTML preview is now reachable by
  a feature that can fan a single message out to an owner's entire
  customer list, not just one triggered recipient at a time — not this
  ticket's to fix (the component itself is untouched by this diff), flagged
  for the department. **Step 6b: not run** — nothing this hop writes is a
  rule about a business-os artifact path, state name, or config key; every
  edit is product code (2 test files) plus 2 receipt files in this ticket's
  own directories, same reasoning the build hop recorded for its own diff.
  **Journal: not applicable** — no G1/G2/G3 or merge request answered this
  pass. **Notify sweep:** all three open `inbox/` items checked fresh
  against the 24h threshold (current `2026-09-05T10:12:28Z`) —
  `ENG-027`/`ENG-028` already carry their one-time `nudged:`; `ENG-016`'s
  continue-Piece-2 question (`notified: 2026-09-04T10:58:06`) sits at
  ~23h14m, still under 24h by roughly 46 minutes. Nothing crossed, nothing
  raised. **Dead-end sweep (scoped to this event):** no other ticket
  touched.

  **2 transitions** (`building → in-review → in-security`), under the cap
  of 4 — both gates passed round 1, so no `building` bounce. Machine WIP
  unaffected — still `1/1`, `ENG-019` family (parent still `building`,
  waiting on this, its own last sub-ticket). Approver-facing WIP and
  approval cap unaffected — no gate touched this hop.

  `chained: ENG-039` — `in-security` is agent-owned (`security`, per
  `definition-of-done.md`'s state table); not the approver, not blocked,
  not terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-039` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-039`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-05` **security round 1: PASS** (security, `continue` event pass,
  context `ENG-039`). Reading map for `continue`: steps 6 and 6b plus the
  not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*; *The four
  lanes*; *Guards*). Mode check clean (`MODE=active`). Pre-pass
  `eng-gate-check.sh`, scoped (`ENG-039`) and whole-board: both exit 0,
  clean. WIP re-checked fresh: still `1/1`, `ENG-019` family. Project
  confirmed `L1` (`config/projects.md`) — no L0 scanning restriction
  applies. `skills/security-gate/SKILL.md` followed step by step.

  Worktree (`~/Documents/projects/_eng/restaurant-portal`) fetched fresh: no
  drift, branch on its own head (`2f438e0`) matching the frontmatter and
  both prior gates' cited head.

  **Threat-modeled the change** (the skill's four questions) before the
  checklist: this is a pure frontend addition over `ENG-038`'s
  already-shipped, already-security-reviewed backend — no new endpoint, no
  new actor, no new data exposure, and a compromised client gains nothing a
  compromised session didn't already have.

  **Did not take either prior gate's account of the backend on trust** —
  read `aiorders-api`'s actual `brand-portal/broadcasts.ts` and `utils.ts`
  directly, at current `origin/main` (`89c6fdb`; confirmed `63f5635`, the
  commit both the build and review hops cited, is its ancestor and the file
  is byte-for-byte unchanged since). Confirmed all 7 actions this ticket's
  frontend calls (`list/get/create/update/pause/resume/cancel_broadcast`,
  `get_broadcast_report`) independently enforce `requireRestaurantAccess`
  plus row-level `.eq('id', ...).eq('restaurant_id', ...)` scoping together
  (not `id` alone) — no IDOR, no cross-tenant path. Confirmed `brand-portal`'s
  entry point requires a real user Bearer JWT for every one of the 7 (none
  are in the orders-only `API_KEY_ALLOWED_ACTIONS` list) — a structurally
  different, already-hardened path from `ENG-035`/`ENG-036`'s still-open
  `systemTriggered` bypass (a different function entirely). Confirmed
  `restaurantId` is sourced client-side from `useRestaurant()`'s
  session-derived context, never a URL/route param, matching every sibling
  autopilot page.

  **OWASP walk, all ten marked, none skipped silently:** A01 checked in
  full per above — clean. A03 clean (grepped the full diff for
  `dangerouslySetInnerHTML`/`innerHTML`/`eval(`/`new Function(`/
  `document.write`: zero hits; the one raw-HTML sink reachable from this
  feature, `EmailEditor`'s existing preview, is unmodified by this diff).
  A04 considered rather than n/a'd: the feature's own larger blast radius
  (one campaign reaching an owner's whole customer list through the reused,
  unmodified `EmailEditor`) is business-logic abuse by an already-vetted
  actor against their own opted-in list, capped by `ENG-037`/`ENG-038`'s
  own `MAX_RECIPIENTS_PER_CAMPAIGN`/`MIN_CAMPAIGN_INTERVAL_HOURS` (both
  re-confirmed live in the code this pass) — the feature's own intended
  capability, scoped through the full lane already, not an emergent gap.
  A06 clean (`git diff --stat -- '*.json' '*.lock'`: zero hits, no
  dependency touched). A09 clean (grepped all 4 new/modified source files
  for `console.*`: zero hits; server-side denial logging unchanged).
  A02/A05/A07/A08/A10 n/a, each with a reason (no crypto, no config/CORS,
  no session logic, no deserialization, no server-side fetch in a
  frontend-only diff). LLM checklist n/a in full — no model/agent/tool/MCP/
  RAG anywhere in this diff.

  **Secrets:** scanned the full diff and the branch's own history against
  `origin/main` (`git diff`/`git log -p`) for key/secret/password/token/
  bearer/PEM-shaped strings — one hit, a benign code comment, not a
  credential.

  **Negative-case test coverage:** this ticket adds no new backend route,
  so the wrong-tenant/wrong-role/no-token case is `ENG-038`'s own, already
  discharged at that gate — not re-tested here. What this ticket owns (can
  a user re-edit a campaign that's already sending) is tested: read
  `BroadcastComposer.test.tsx` directly rather than trusting the prior
  gates' account of it, confirmed the lock-state assertion disables the
  name input, hides Save, and shows the notice when `status: "active"`,
  mutation-verified by the review hop.

  **Zero new findings.** `F1`/`F2` (code review) and the `EmailEditor`
  observation are not security-category findings of this diff and are not
  duplicated into the receipt or the notebook — named and reasoned about
  instead (A03/A04 above). `ENG-038`'s own carried-forward items (TOCTOU
  race, `enrollAudience` scoping untested-in-isolation, `ENG-036`'s
  still-open bypass) are unreachable through, and unaffected by, this diff.
  No notebook entry written — nothing new to log.

  Receipt written: `agents/security/reviews/ENG-039.md`. `links.security_review`
  set. `time_spent`/`time_remaining` updated (security done; release-
  readiness remains).

  **1 transition** (`in-security → ready-to-ship`), under the cap of 4.
  Machine WIP unaffected — still `1/1`, `ENG-019` family (parent still
  `building`, waiting on this, its own last sub-ticket). Approver-facing
  WIP and approval cap unaffected — no gate touched this hop.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** all three open `inbox/` items checked fresh against the
  24h threshold (current `2026-09-05T10:24:07Z`) — `ENG-027`/`ENG-028`
  already carry their one-time `nudged:`; `ENG-016`'s continue-Piece-2
  question (`notified: 2026-09-04T10:58:06`) sits at ~23h26m, still under
  24h by about 34 minutes. Nothing crossed, nothing raised. **Observations:**
  none new — the one candidate (`EmailEditor`'s raised blast radius) was
  already filed by the code-review hop; not duplicated. No
  `exception-request:` found on this or any other ticket touched. **Step
  6b:** not run — this hop wrote a review receipt plus ticket/board
  updates, no rule about a business-os artifact path, state name, or config
  key. **Journal:** not applicable — no G1/G2/G3 or merge request answered
  this pass.

  `chained: ENG-039` — `ready-to-ship` is agent-owned (`devops`, per
  `definition-of-done.md`'s state table); not the approver, not blocked,
  not terminal, not held by a cap. Fired `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-039` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-039`) and
  whole-board: see board index.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.

- `2026-09-05` **release-readiness: PR opened, blocked on approver** (devops,
  `continue` event pass, context `ENG-039`). Entry kept short per
  `conventions.yaml` → `ticket_log.entry.cap_lines: 20`; full reasoning:
  `agents/devops/notebook/2026-09-05-release-readiness-log.md`.

  All three upstream gates re-verified fresh, still passing (review, QA,
  security — all round 1). No migration owed. Readiness gate held, no
  blocking failure — rollback fine (single-branch revert), cost $0/month;
  two pre-existing, out-of-scope gaps named in full rather than carried
  quietly: `BROADCAST_UNSUBSCRIBE_SECRET` not provisioned (every real send
  fails loudly, logged, until fixed), and SMS delivery entirely mocked
  (silent false-`'sent'` on any SMS step — corrected an existing
  `proposals.md` row rather than duplicating it). Neither blocks this PR.
  Opened `restaurant-portal` PR #3; raised
  `inbox/2026-09-05-eng039-merge-request.md`.

  **1 transition** — `ready-to-ship → blocked`, `blocked_on: approver`,
  `blocked_from: ready-to-ship`, owner `devops → approver`, `links.pr` set.
  WIP unaffected — still `1/1`, `ENG-019` family, last sub-ticket.
  `chained: none` — waiting on the approver, an L1 merge is a human gate.

  business-os left uncommitted — standing default, open.

- `2026-09-05` no state change (eng-manager, `watch (launchd)` event pass —
  step 5 merge detection, triggered by this ticket's own merge-request file
  landing in `inbox/`). Re-checked PR #3: local git (`git fetch` +
  `merge-base --is-ancestor` on the ticket's own recorded commit `2f438e0`,
  not the live branch tip, per the `ENG-008` lesson) says not merged —
  `origin/main` still at `5276a53`. `gh pr view 3` cross-check agrees:
  `state: OPEN`, `mergedAt: null`, no comments. Stays `blocked`.

  **Notify sweep:** all three open `inbox/` items checked fresh (current
  `2026-09-05T10:53:09Z`) — `ENG-027`/`ENG-028` already carry their
  one-time `nudged:`; `ENG-016`'s continue-Piece-2 question (`notified:
  2026-09-04T10:58:06`) sits at ~23h55m, still under 24h by ~5 minutes.
  Nothing crossed, nothing raised. **Dead-end sweep (scoped to this
  event):** no other ticket touched — the `watch` reading map (steps 2-4,
  plus 5 for a changed merge-request item) doesn't call for a full board
  sweep. No `exception-request:` found; no new observation.

  `chained: none` — still `blocked_on: approver`, unchanged by this pass.
  Pre/post `eng-gate-check.sh`, scoped (`ENG-039`) and whole-board: both
  exit 0, clean.

  business-os left uncommitted — standing default, open.

- `2026-09-05` no state change (eng-manager, `scheduled` event pass, 09:30
  PDT — whole-board sweep, the safety net, read in full per the reading
  map). Re-checked PR #3: git ancestry on `2f438e0` + `gh pr view 3` agree —
  `OPEN`, `mergedAt: null`, `origin/main` still `5276a53`. Stays `blocked`.

  **Notify sweep:** `ENG-016`'s continue-Piece-2 question crossed 24h
  (`notified: 2026-09-04T10:58:06`, no prior `nudged:`, ~29h33m old) —
  nudged this pass, `nudged:` stamped. Logged `sent: active` not `sent:
  nudge` — the known `$MODE`/`.env` clobber in `lib/eng-notify.sh`
  (`proposals.md` 2026-08-25 row, reconfirmed a third time this pass, not
  re-filed). `ENG-027`/`ENG-028` already past their one-time nudge; this
  ticket's own merge request (`notified: 2026-09-05T03:41:22`) is ~13h old,
  under threshold.

  **Whole-board dead-end sweep:** no ticket with no owner; no broken chain
  (no `*-eng-events-dropped.md` files exist, `traces/.pending` empty, this
  ticket's own last `chained: none` correctly matches `blocked_on:
  approver`). Machine WIP unchanged, `1/1`, `ENG-019` family. `exceptions.md`
  still empty; no `exception-request:` found on any ticket.

  `chained: none` — still `blocked_on: approver`, unchanged. Pre/post
  `eng-gate-check.sh`, scoped (`ENG-039`) and whole-board: both exit 0,
  clean.

  business-os left uncommitted — standing default, open.

- `2026-09-05` no state change (eng-manager, `watch (launchd)` event pass —
  step 5 merge detection; fired ~16:55 UTC, ~25 minutes after the
  immediately-preceding `scheduled` pass's own nudge-stamp write to
  `ENG-016`'s continue-Piece-2 question (09:31:45 PDT / 16:31:45 UTC) — a
  changed fingerprint in the watched inbox with zero unprocessed work
  behind it). Verified fresh rather than trusted: `git fetch` +
  `merge-base --is-ancestor` on the ticket's own recorded commit `2f438e0`
  — not merged, `origin/main` still `5276a53`; `gh pr view 3` agrees
  (`OPEN`, `mergedAt: null`). Stays `blocked`.

  **Notify sweep:** all four open `inbox/` items re-read fresh, none
  carries a `decision:`. `ENG-027`/`ENG-028` already past their one-time
  nudge; `ENG-016`'s continue-question already nudged by the preceding
  `scheduled` pass; this ticket's own merge request (`notified:
  2026-09-05T03:41:22`) still under the 24h threshold. Nothing crossed,
  nothing raised. `agents/product-manager/inbox/` and
  `agents/eng-manager/inbox/` hold only `.gitkeep`/processed folders — no
  new intake, no new technical finding.

  `chained: none` — still `blocked_on: approver`, unchanged by this pass.
  `traces/.pending` holds only the next `scheduled` auto-drain, no
  `continue ENG-039` or other queued event — no broken chain. Pre/post
  `eng-gate-check.sh`, scoped (`ENG-039`) and whole-board: both exit 0,
  clean.

  business-os left uncommitted — standing default, open.

- `2026-09-05` **step-5 merge re-check: MERGED — full acceptance-check —
  `blocked → shipped → verified`** (eng-manager + product-manager, `watch
  (launchd)` event pass — step 5, merge-request item unchanged on disk but
  its underlying PR state had not been re-checked in ~1h; re-verified fresh
  per this ticket's own standing practice rather than trusted from the last
  `watch` pass's "not merged" answer). Reading map for `watch`: steps 2-4
  plus 5 (changed/pending merge-request item) plus the not-negotiable set
  (1, 7, 8b, 9, 10). Mode check clean (`MODE=active`). Pre-pass
  `eng-gate-check.sh`, scoped (`ENG-039`) and whole-board: both exit 0,
  clean. WIP re-checked fresh: still `1/1`, `ENG-019` family.

  **Merge confirmed two ways.** `git fetch` +
  `git merge-base --is-ancestor 2f438e0 origin/main` → YES; `gh pr view 3`
  → `state: MERGED`, `baseRefName: main`, `mergeCommit: aeeb7b9`,
  `mergedAt: 2026-09-05T17:05:41Z`. `git diff 2f438e0 aeeb7b9 --stat`
  empty — zero drift from what all three gates reviewed.

  **All three gate receipts re-read fresh, all still `pass`:** code review
  round 1, quality round 1 (14/14), security round 1 (zero findings). Per
  step 5 ("a merge is not a gate"), verified before advancing rather than
  assumed from the merge request's own account. No migration —
  `agents/database/migrations/` has no `ENG-039-*` entry, confirmed against
  the diff (`git diff 5276a53 aeeb7b9 --stat`: 9 `src/**`/test files only).

  **Ran `acceptance-check/SKILL.md` in full**, this family's third
  consecutive full run (after `ENG-034`'s and `ENG-038`'s own, per the
  proposal on the ten-ticket gap that preceded them) — not the
  receipt-bookkeeping shortcut. This ticket owns AC1-AC5 of `ENG-019`'s 7
  per the work-breakdown's own AC-mapping. Read the merged tree directly
  (`origin/main` at `aeeb7b9`) rather than the diff, the PR description, or
  any gate's own summary — same standing practice. Unlike `ENG-038`'s own
  check, no live-deploy-timing surprise to chase: this is a static
  Cloudflare Pages frontend with no runtime state of its own, so the merge
  commit itself is the full source of truth. **All 5 owned criteria: pass.**
  No scope creep (`types/autopilot.ts`, `Templates.tsx`, every reactive
  `Automations` flow confirmed untouched via `git diff --stat`). Cost
  matches ($0/month — no dependency/lockfile change). Full walk:
  `agents/product-manager/notebook/2026-09-05-eng039-acceptance.md`.

  **Release record written:**
  `agents/devops/releases/2026-09-05-restaurant-portal-ENG-039.md` — same
  L1/`deploy-cf.yml`/no-dashboard-access posture `ENG-032`'s own record on
  this repo already set. `links.release` set in the same edit.

  **2 transitions** (`blocked → shipped`, `shipped → verified`), under the
  cap of 4. `state: verified`, `owner: approver → eng-manager`,
  `blocked_on`/`blocked_from` cleared, `time_remaining: none`.

  **Consequence for the family:** every child of `ENG-019` (`ENG-037`,
  `ENG-038`, this ticket) is now `shipped`/`verified` — the `ADR-003` parent
  exemption condition is satisfied (all children settled, at least one
  actually shipped). `ENG-019` itself is not touched in this pass — its own
  next hop belongs in its own dedicated session, same handoff shape
  `ENG-034`'s own shipping pass used for `ENG-016`.

  **Dead-end sweep (scoped to this event):** no other ticket touched — the
  `watch` reading map (steps 2-4, plus 5 for this changed merge-request
  item) doesn't call for a full board sweep. **Notify sweep:** merge-request
  item resolved this pass (moved to `inbox/_handled/`, `## Decision` filled
  in — no written reply was ever given, same standing pattern this approver
  has used for every prior L1 merge); `ENG-027`/`ENG-028` already past their
  one-time `nudged:`; `ENG-016`'s continue-Piece-2 question already nudged
  by an earlier `scheduled` pass today. Nothing new crossed 24h.
  **Observations:** none new — nothing surfaced beyond what `ENG-038`'s own
  acceptance-check already filed. No `exception-request:` found. **Step
  6b:** not run — this hop wrote a release record, an acceptance notebook,
  and board/inbox/journal updates; no rule about a business-os artifact
  path, state name, or config key. **Journal:** decision-journal entry
  added for the merge (see `decision-journal.md`).

  Post-pass `eng-gate-check.sh`, scoped (`ENG-039`) and whole-board: see
  board index.

  `chained: ENG-019` — not this ticket (`verified` is terminal, the
  chaining guard never fires on it), but the parent this ticket's own
  shipping now makes eligible for its own `ADR-003`-class exemption. Fired
  `/bin/zsh
  /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-019` before this pass exits.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains
  open, not re-decided here.
