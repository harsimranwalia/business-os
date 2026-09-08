---
id: ENG-040
title: Brand-portal FAQ write path — widen `EDITABLE_PAGES` to accept `faqs`
project: aiorders-api
type: feature
size: XS
time_estimate: under an hour
time_spent: ~35m
time_remaining: none — verified
severity: P2
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-05
updated: 2026-09-06
branch: feat/ENG-040-brand-portal-faq-write-path
depends_on: []
blocks: [ENG-041]
parent: ENG-021
links:
  prd: agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md
  design: agents/architect/designs/ENG-021-chat-bar-engagement-and-faq-self-service.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-040.md
  test_plan: agents/qa/test-plans/ENG-040.md
  security_review: agents/security/reviews/ENG-040.md
  release: agents/devops/releases/2026-09-06-aiorders-api-ENG-040.md
  pr: https://github.com/harsimranwalia/aiorders-api/pull/18
---

## Problem

`brand-portal`'s `website.ts` handler allow-lists exactly two keys
(`catering`, `careers`) in `EDITABLE_PAGES`. There is no write path for
`restaurant_website.faqs` through the edge function an owner's own JWT is
already authorised to call, so `ENG-041`'s FAQ editor has nothing to save to.

## Outcome

`update_website_content` accepts a third key, `faqs`, and persists it to
`restaurant_website.faqs` unchanged. `get_website_content` returns it in the
response `content` object. `catering`/`careers` behaviour is unaffected — the
handler's existing per-key loop makes this a pure addition, not a rewrite.

## Notes

Design: `agents/architect/designs/ENG-021-chat-bar-engagement-and-faq-self-service.md`
— `## Components` (first two rows) and `## Interfaces` (`update_website_content`
widened payload; `get_website_content` widened response). Exact diff:

- `aiorders-api/supabase/functions/brand-portal/website.ts` — add `'faqs'` to
  `EDITABLE_PAGES`; add `faqs: data?.faqs ?? null` to `getWebsiteContent`'s
  returned `content`; export `interface WebsiteFaq { question: string; answer:
  string }`. Widen the array's own comment (it currently says "pages"; the
  array now holds columns too). **No other edit to this file** — in
  particular, do not touch `verifyRestaurantAccess` or the ownership check.
  That's `ENG-022`'s fix (already merged and verified); re-touching it here
  is a bundled fix, automatic review failure #7.
- `aiorders-api/supabase/functions/README.md` — add `faqs` to `brand-portal`'s
  DB-columns note. Required in the same commit per this repo's own
  `CLAUDE.md` ("After changing a function").

Branch from `origin/main` — `ENG-022` is already merged and verified, so the
design's named sibling-branch-staleness risk no longer applies. Re-read
`website.ts`/`utils.ts` at build time rather than trusting the design's quoted
source, since the design itself flagged this file as recently and separately
touched.

`content.faqs = []` must persist as `[]`, not be dropped — `?? null` only
nulls on `null`/`undefined`. That's what "the owner deleted every FAQ" looks
like on disk; get it right here, since `ENG-041`'s save-empty-list path
depends on it round-tripping correctly.

Known pre-existing `deno check` noise on `.select(EDITABLE_PAGES.join(', '))`
(already catalogued, `observations.md` 2026-09-03, found during `ENG-022`'s
own build). Do not "fix" it in passing (automatic review failure #7); add no
new errors to the known 10.

**AC ownership** (design didn't map ACs to components; mapped in
`agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`): this
ticket owns AC4 and AC5 in full, and the write-capability half of AC3. AC1,
AC2, AC6, and the UI half of AC3 are `ENG-041`'s.

## Log

- 2026-09-05 `(created) → building` (eng-manager, `work-breakdown`, `continue
  ENG-021` event pass) — sub-ticket of `ENG-021`, sequence 1 of 2, no
  dependency, dispatched straight to `building`. `time_estimate` under an
  hour, 0h spent. Machine WIP: this ticket is part of `ENG-021`'s own family,
  not a second occupant of the `1/1` slot — same reading `ENG-016`/`ENG-019`
  already established. Full reasoning:
  `agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`.
  `chained: ENG-040` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-040`
  before this pass exits.

- 2026-09-05 `building → in-review` (backend, `continue ENG-040` event pass).
  Built per design: `EDITABLE_PAGES` gains `faqs`; `getWebsiteContent`
  returns `faqs: data?.faqs ?? null`; new `WebsiteFaq` export; README
  DB-tables note widened. No other edit to `website.ts` — comment already
  said "Columns," nothing to widen there; re-confirmed `ENG-022`'s ownership
  fix live on both actions. Added 2 tests (empty-array and populated-array
  read path); 5/5 pass (`--no-check` — repo-wide `deno check` has failed
  outright pre-existing this ticket). `deno check website.ts`: 7→8, one new
  same-shape `GenericStringError` instance, not fixed in passing. Full
  detail, branch-switch note, and a correction to the design's own "count
  unchanged" claim: `agents/backend/notebook/2026-09-05-eng040-build.md`.
  Branch `feat/ENG-040-brand-portal-faq-write-path` pushed fresh off
  `origin/main` (`aiorders-api@7fa83b3`); no PR yet — release-readiness's own
  step. Machine WIP unaffected — still held by the `ENG-021` family.
  `chained: ENG-040` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-040`
  before this pass exits.

- 2026-09-05 `in-review → in-qa` (principal-engineer then qa, `continue
  ENG-040` event pass — combined review+quality hop, one session, per
  `eng_build_loop.md` step 6's "one combined hop" note). `git fetch` +
  `git diff origin/main...HEAD --stat` confirmed no drift since the build
  hop (`aiorders-api@7fa83b3`, unchanged at review time).

  **Review: PASS, round 1.** 0/10 automatic failures — checked #8 closely
  (the new `WebsiteFaq` export is unused in-file) and confirmed it matches
  its two neighbors' identical established convention rather than being a
  new departure; design names it explicitly. One non-blocking finding: the
  design/ticket's own stated reason for `faqs: data?.faqs ?? null` (vs. the
  siblings' `|| null`) doesn't hold — `[] || null` is `[]` in JS, arrays are
  always truthy, so either operator behaves identically here. Code is
  correct regardless; not blocking. Full text:
  `agents/principal-engineer/reviews/ENG-040.md`. `links.review` set.

  **Quality gate: PASS.** Test plan written first:
  `agents/qa/test-plans/ENG-040.md`, one row per owned AC (4 in full, 3's
  write half; AC5 confirmed structural, no code path to test). Found a real
  gap while writing it: `website.test.ts`'s fake Supabase client had never
  mocked `.update()`/`.insert()`, for any key, so the write side of AC3/AC4
  had zero test evidence despite the ticket claiming both in full. Closed it
  for this ticket's own scope only — extended the fake to capture its write
  payload, added one test proving `update_website_content` with `{faqs}`
  persists exactly `{restaurant_id, faqs}` via the insert branch. Mutation
  check: temporarily dropped `'faqs'` from `EDITABLE_PAGES`, re-ran — exactly
  the new test went red (`success: true → false`), the other 5 held;
  reverted, re-ran clean (6/6), confirmed `git status --short` showed only
  the intended test-file diff before committing. `deno check website.ts`
  independently re-derived: 8 errors, matches the build hop's own 7→8
  account. Committed and pushed as a separate commit,
  `aiorders-api@104b057` (`git log`: `7fa83b3..104b057`) — the review verdict
  above was written against `7fa83b3`, before this commit existed, so the
  code review and the QA-added test are on record against two different
  points on the branch, deliberately: re-reviewing a test-only addition that
  doesn't touch `website.ts` would not change round 1's verdict on the
  source diff. **Did not fix catering/careers' identical pre-existing
  write-path gap** — filed as a proposal instead
  (`agents/eng-manager/proposals.md`, 2026-09-05 row), since fixing
  department-wide test debt isn't this XS ticket's scope. `links.test_plan`
  set.

  **1 transition** (`in-review → in-qa`), well under the cap of 4. Machine
  WIP unaffected — `in-qa` is still inside the counted
  `ready`..`ready-to-ship` range, still `1/1`, held by the `ENG-021` family.

  **6b:** not applicable this hop — the only edit was a local test-harness
  extension inside `website.test.ts` itself; no receipt path, state name,
  config key, or cross-file artifact rule was written or relied on.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract. **Notify sweep:** nothing raised
  this pass (no new gate item; review/quality verdicts aren't gate items).
  Checked the three open `inbox/` items anyway per the not-negotiable step
  7: `ENG-028`'s G1 and `ENG-016`'s Piece-2 question already carry their
  one-ever `nudged:`; `ENG-020`'s merge request (`notified:
  2026-09-05T13:40:18`) is well under 24h. No action. **Observations:** none
  beyond the proposal filed above. **Exceptions/journal:** n/a — no
  `exception-request:`, no G1/G2/G3/merge-request answered this pass.

  Pre-pass and post-pass `lib/eng-gate-check.sh`, scoped (`ENG-040`) and
  whole-board: all four runs exit 0, clean.

  `chained: ENG-040` — `in-qa` is agent-owned (`security` next, per
  `definition-of-done.md`'s state table), not the approver, not blocked, not
  terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-040`
  before this pass exits.

- 2026-09-05 `in-qa → ready-to-ship` (security, `continue ENG-040` event
  pass, per `skills/security-gate/SKILL.md`). `git fetch` + `git diff
  origin/main...HEAD --stat` confirmed no drift since the QA hop
  (`aiorders-api@104b057` unchanged, `origin/main@89c6fdb`).

  **Verdict: PASS.** Threat-modelled the diff (4 questions), then did not
  take the ticket's own "`ENG-022` already merged" claim on trust: confirmed
  `78194da` (ENG-022's merge commit) is an ancestor of this branch, confirmed
  both `website.ts` call sites use the throwing `requireRestaurantAccess`
  (not the pre-`ENG-022` `verifyRestaurantAccess`), confirmed the checked
  `restaurant_id` and the written `restaurant_id` are the same variable at
  both the update and insert branch (no confused-deputy gap), and read both
  negative-authz tests directly rather than trusting the test plan's prose.
  Full OWASP A01–A10 walk, LLM checklist (n/a, confirmed no model/tool/agent
  code in the diff), secret scan (clean) and dependency check (none new; the
  untracked `deno.lock` re-confirmed as the same benign local artifact
  `ENG-022`'s review already characterised) in
  `agents/security/reviews/ENG-040.md`. `links.security_review` set.

  **2 non-blocking findings, neither blocking, logged to
  `agents/security/notebook/2026-09-05-findings.md`:** (1) A04 — no shape/size
  validation on `EDITABLE_PAGES` payload values, `faqs` inheriting a gap
  `catering`/`careers` already had rather than introducing a new one;
  tenant-confined, first occurrence of this specific class, not a
  three-strike, not proposed on its own. (2) A05 — the pre-existing verbose-
  error catch-all in `requireRestaurantAccess` (`utils.ts`, untouched by this
  diff), already three-struck and proposed at `ENG-009`, carried again at
  `ENG-010`/`ENG-022`; not re-proposed, logged as another occurrence per the
  same disposition `ENG-022`'s review already established.

  **1 transition** (`in-qa → ready-to-ship`), well under the cap of 4.
  Machine WIP unaffected — `ready-to-ship` is still inside the counted
  `ready`..`ready-to-ship` range, still `1/1`, held by the `ENG-021` family.

  **6b:** not applicable this hop — no receipt path, state name, config key,
  or cross-file artifact rule was written or relied on; `links.security_review`
  is a per-ticket frontmatter field, not a shared artifact another file
  references by path.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract. **Notify sweep:** nothing raised
  this pass (a `pass` verdict isn't a gate item). Checked the three open
  `inbox/` items per the not-negotiable step 7: `ENG-028`'s G1 and
  `ENG-016`'s Piece-2 question already carry their one-ever `nudged:`;
  `ENG-020`'s merge request still well under 24h. No action.
  **Observations:** none beyond the two findings logged above (both routed
  as findings/notebook entries, not observations — each asked something of a
  future reader, so neither belonged in `observations.md`).
  **Exceptions/journal:** n/a — no `exception-request:`, no G1/G2/G3/merge-
  request answered this pass.

  Pre-pass and post-pass `lib/eng-gate-check.sh`, scoped (`ENG-040`) and
  whole-board: all four runs exit 0, clean.

  `chained: ENG-040` — `ready-to-ship` is agent-owned (`devops` next, per
  `definition-of-done.md`'s state table), not the approver, not blocked, not
  terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-040`
  before this pass exits.

- 2026-09-05 `ready-to-ship → blocked` (devops, `continue ENG-040` event
  pass, `skills/release-runner/SKILL.md` run step by step). Full reasoning:
  `agents/devops/notebook/2026-09-05-release-readiness-log.md`.

  **Step 2 (upstream gates), all three re-read fresh from the receipt
  files:** review (`agents/principal-engineer/reviews/ENG-040.md`, round 1,
  pass), quality (`agents/qa/test-plans/ENG-040.md`, round 1, pass, 6/6),
  security (`agents/security/reviews/ENG-040.md`, round 1, pass). No
  migration owed — confirmed `agents/database/migrations/` has no
  `ENG-040-*.md`.

  **Step 3 (readiness gate), no blocking failure:** rollback — no migration,
  no stored-state change, reverting the merge fully undoes this diff.
  Observability — both handler paths already log via `console.error` before
  returning failure, generic over every `EDITABLE_PAGES` key including the
  new one; confirmed by reading `website.ts` directly. Cost — $0/month, no
  new dependency, no new infrastructure. Window — n/a, L1.

  **Step 4 (route):** worktree re-checked fresh — `git fetch`, `HEAD` at
  `104b057` matching every gate's cited head, not merged, no drift (`git
  diff origin/main...HEAD --stat`: 3 files, 87/-5, matches the security
  gate's own account exactly). `gh pr list` confirmed no PR already existed.
  Opened `aiorders-api` PR #18
  (https://github.com/harsimranwalia/aiorders-api/pull/18). Wrote
  `inbox/2026-09-05-eng040-merge-request.md`, plain `pr_url:` string (single
  repo), `time_estimate: under an hour`. `lib/eng-notify.sh raise` exited 0;
  confirmed sent from `traces/eng-notify-2026-09-05.log`
  (`16:51:18`); stamped `notified: 2026-09-05T16:51:18` on the item by hand.

  State `ready-to-ship → blocked`, `blocked_on: approver`,
  `blocked_from: ready-to-ship`, `owner: devops → approver`, `links.pr` set.
  No G3 — L1 has none; the PR merge is the human gate. No release record
  yet — L1's actual deploy (a manual `supabase functions deploy` after
  merge) and the release record both wait for merge detection on a future
  pass.

  **1 transition** (`ready-to-ship → blocked`), well under the cap of 4.
  **Machine WIP unaffected** — still `1/1`, held by the `ENG-021` family
  (`ENG-021` itself still `building`; `ENG-041` still `ready`, waiting on
  this ticket's own `depends_on`, unresolved by a merge request — that
  clears only on `verified`).

  **6b:** not applicable this hop — the merge-request item follows this
  board's own established format exactly; no new receipt path, state name,
  config key, or cross-file artifact rule was introduced.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract; `ENG-041` correctly left
  untouched at `ready`. **Notify sweep:** this pass's own merge request
  raised and stamped above. Checked the other open `inbox/` items per the
  not-negotiable step 7: `ENG-028`'s G1 and `ENG-016`'s Piece-2 question
  already carry their one-ever `nudged:`; `ENG-020`'s merge request
  (`notified: 2026-09-05T13:40:18`) still well under 24h. No action.
  **Observations:** none — both non-blocking findings carried forward were
  already logged to the security notebook at that gate, not newly found
  here. **Exceptions/journal:** n/a — no `exception-request:`, and nothing
  was *answered* this pass (a merge request was raised, not resolved), so
  no decision-journal entry is owed yet.

  Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-040`) and whole-board: both
  exit 0, clean. (Pre-pass state inherited clean from the immediately
  preceding hop's own post-pass check on this same ticket, above — no
  intervening pass.)

  `chained: none — blocked_on: approver`. Per `eng_build_loop.md` step 9 and
  the Guards section, a ticket waiting on the approver is never chained; the
  PR merge is the next event, and the build loop's own step-5 merge
  detection (or a `watch`/`scheduled` sweep) picks it up without a fired
  hop.

- 2026-09-06 `blocked → shipped → verified` (eng-manager then product-manager,
  `scheduled` event pass, four-times-daily safety net). Step 5 merge
  detection: `git fetch` in the department's own `aiorders-api` worktree,
  then `git merge-base --is-ancestor
  origin/feat/ENG-040-brand-portal-faq-write-path origin/main` →
  **is an ancestor**. Cross-checked directly, not inferred from ancestry
  alone: `gh pr view 18 --json state,mergedAt,baseRefName,headRefName,mergeCommit`
  → `state: MERGED`, `baseRefName: main` (no stacking), `mergedAt:
  2026-09-06T16:11:40Z`, merge commit `5e36648b`. No written reply on
  `inbox/2026-09-05-eng040-merge-request.md` (`decision:` still blank).

  **Receipts re-read fresh before advancing** (step 5's "a merge is not a
  gate" clause): review (round 1, pass), quality (round 1, pass, 6/6),
  security (round 1, pass) — all three still on disk exactly as the prior
  hops left them. No migration owed (confirmed: no
  `agents/database/migrations/ENG-040-*.md`).

  **Zero drift confirmed, not assumed:** `git diff 104b057 origin/main --stat`
  shows one file beyond the reviewed tip, `supabase/functions/README.md`
  (+2/-1) — read the actual diff rather than treating any beyond-tip change
  as suspect: it's `ENG-020`'s own already-verified `get_acquisition_report`
  line landing in the same shared file via `main`'s other parent
  (`672dfa77`), not this ticket's. `website.ts` itself merged byte-identical
  to what every gate reviewed.

  **Confirmed actually deployed, not just merged:** `supabase functions list`
  shows `brand-portal` at version 84, `UPDATED_AT 2026-09-06T16:29:25Z`, ~18
  minutes after the merge — no tracked workflow on this repo, by-hand deploy,
  same pattern every prior `aiorders-api` release has shown.

  **Full `acceptance-check/SKILL.md` walk run**, not the receipt-bookkeeping
  shortcut — this ticket owns real, checkable behaviour (AC4/AC5 in full,
  AC3's write half), not a 0-criteria schema-only shape. Independently
  re-verified beyond the ticket's own claims: read `website.ts` directly for
  the `EDITABLE_PAGES`/persist-loop/`requireRestaurantAccess` behaviour;
  grepped every `aiorders-api` chat-bot search function
  (`ai-search`/`ai-search-intelligent`/`ai-search-openrouter`) and confirmed
  each reads `restaurant_website.faqs` directly (AC4 — same column the bot
  reads and this ticket writes, no second store); read
  `aiorders-admin-hub/src/pages/RestaurantAIWebsite.tsx` directly and
  confirmed its own staff-editor save path writes the same
  `restaurant_website.faqs` column via a direct upsert (AC5 — two editors,
  one source of truth). All 3 owned criteria: **pass**. Full walk:
  `agents/product-manager/notebook/2026-09-06-eng040-acceptance.md`;
  release record:
  `agents/devops/releases/2026-09-06-aiorders-api-ENG-040.md`.

  Merge-request item's `## Decision` filled with a plain-language resolution
  note and moved to `inbox/_handled/2026-09-05-eng040-merge-request.md` —
  `decision:` frontmatter field itself left blank, same convention every
  prior silent-merge item on this board has used (the prose in the body is
  the record, not the field).

  **2 transitions** (`blocked → shipped`, `shipped → verified`), well under
  the cap of 4 — receipt re-confirmation, live-deploy check, and a full
  acceptance-check, no new implementation work.

  **Consequence for the family:** this ticket's `blocks: [ENG-041]` — that
  ticket's sole `depends_on: [ENG-040]` is now satisfied. `ENG-041` was
  already `ready` (dispatched as part of this work-breakdown family, not a
  fresh WIP slot) — its own dependency clearing doesn't start a second
  occupant of the `1/1` machine-WIP slot. `ENG-021` (parent) still cannot
  reach `shipped`/`verified` until `ENG-041` is settled too (`ADR-003`) — one
  child down, one to go. Machine WIP unaffected throughout — this ticket left
  the counted `ready`..`ready-to-ship` range at its own prior
  `ready-to-ship → blocked` hop; the slot has been held by the `ENG-021`
  family the whole time (`ENG-021` still `building`).

  **6b:** not applicable — no build hop ran this pass; the artifact this
  ticket wrote (`EDITABLE_PAGES` gaining `faqs`) was already checked for
  cross-file mentions at its own build hop.

  **Dead-end sweep:** see the board index's own whole-board sweep notes for
  this pass. **Notify sweep:** this ticket's own merge-request item is now
  resolved and archived — nothing to nudge on it. The five other open
  `inbox/` items checked fresh (see the board index's own entry for this
  pass) — none due. **Observations:** none new beyond what the board index's
  own entry records. **Exceptions/journal:** n/a — no `exception-request:`
  found; the merge-request item was resolved by silent GitHub merge, not an
  answered gate, so no decision-journal entry is owed (silence says nothing
  about what the approver wants, same disposition every prior silent merge
  on this board has used).

  Pre-pass and post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-040`) and whole-board: all four runs exit 0, clean.

  `chained: none` — `verified` is terminal; the chaining guard never fires on
  a terminal ticket. `chained: ENG-041` fired instead, recorded on
  `ENG-041`'s own log — see that ticket's file.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.
