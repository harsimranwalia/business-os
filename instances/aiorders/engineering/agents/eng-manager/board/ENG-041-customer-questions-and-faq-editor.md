---
id: ENG-041
title: Customer Questions page and self-service FAQ editor — brand portal
project: restaurant-portal
type: feature
size: M
time_estimate: ~1 to 1.5 days
time_spent:
time_remaining:
severity: P2
priority:
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-05
updated: 2026-09-07
branch: feat/ENG-041-customer-questions-and-faq-editor
depends_on: [ENG-040]
blocks: []
parent: ENG-021
links:
  prd: agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md
  design: agents/architect/designs/ENG-021-chat-bar-engagement-and-faq-self-service.md
  adrs: [ADR-013, ADR-014]
  review: agents/principal-engineer/reviews/ENG-041.md
  test_plan: agents/qa/test-plans/ENG-041.md
  security_review: agents/security/reviews/ENG-041.md
  release: agents/devops/releases/2026-09-07-restaurant-portal-ENG-041.md
  pr: https://github.com/harsimranwalia/restaurant-portal/pull/5
---

## Problem

Restaurant owners have no visibility into the chat-bar questions their own
customers ask, and no way to turn one into a website FAQ without staff —
even though the conversation log and the FAQ content are both already
reachable, per-restaurant, from this portal.

## Outcome

A new `/questions` page lists the restaurant's own chat-bar questions, newest
first, with a plain empty state and a distinct error state. A third "FAQs"
tab on the existing Website page adds/edits/removes entries against
`restaurant_website.faqs` through `ENG-040`'s widened action. A per-row "Add
to FAQs" button on the questions page carries the question text across and
pre-fills a new FAQ entry with it.

## Notes

**Depends on `ENG-040` shipping, not merely building.** The FAQ tab's save
path calls the widened `update_website_content` action, and the design's own
Rollout section sequences API before portal specifically so the FAQ tab never
saves against an un-widened handler in production. (The questions page half
has no such dependency — it never calls `ENG-040`'s action — but both ship as
one PR per the design's own component list, so this ticket waits as a whole
rather than splitting further. Reasoning:
`agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`.)

**Required first step of this ticket's build hop, before writing the
questions-page query — carried over from the design's own `## Data` section,
not run during work-breakdown (no live DB access from that pass):** confirm
directly against the live project (`bmnmnejwdxbcqinqkwko`):

1. RLS is `ENABLED` on `public.ai_conversations` and the SELECT policy
   `"Restaurant managers can view their restaurant conversations"` exists and
   matches `restaurant-portal`'s own tracked migration
   (`20250903152559_*.sql`). **If this is not true, stop and report back
   rather than building the direct-read design** — the named contingency (a
   new `brand-portal` action with an explicit `.hasAccess` check; see the
   design's Alternatives table) is a different design, not a build-time
   judgement call, and needs to go back through the architect.
2. Retention window / `cleanup_old_ai_conversations` schedule, and
   per-restaurant session-count distribution (sanity-checks the 100-session
   page bound). Informational only — doesn't gate the build. Note whatever is
   found in this ticket's own log; if the confirmed max sessions per
   restaurant is under ~20, the design's own Risks section says "Load older"
   is dead weight and should be dropped.

Design: `agents/architect/designs/ENG-021-chat-bar-engagement-and-faq-self-service.md`
— `## Components` (rows 4-9), `## Interfaces` (questions query, keyset
pagination via `.lt('updated_at', ...)`, questions→FAQ hand-off through
react-router location state — never a URL parameter), `## Failure behaviour`
(the full table — every empty/error/malformed case is already specified;
build to it rather than improvising).

Explicitly **do not touch** `CateringPageForm.tsx` / `CateringFaq` — a
different, unrelated FAQ list scoped to the catering landing page only. Mirror
its add/edit/remove idiom in the new `WebsiteFaqForm.tsx`; don't wire into it.

**AC ownership** (mapped in
`agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`): this
ticket owns AC1, AC2, AC6 in full, and the UI half of AC3 (the editor itself
and the "Add to FAQs" hand-off — the stronger reading of the parent's own
Outcome, "directly from that view"). AC4/AC5 are satisfied by construction of
`ENG-040`'s shared column; nothing in this ticket's own diff proves them
independently — don't re-derive them here.

## Log

- 2026-09-05 `(created) → ready` (eng-manager, `work-breakdown`, `continue
  ENG-021` event pass) — sub-ticket of `ENG-021`, sequence 2 of 2,
  `depends_on: [ENG-040]` unmet, held at `ready`. `time_estimate` ~1 to 1.5
  days. Owner `eng-manager` while waiting, reassigned to `frontend` once
  `ENG-040` ships. Full reasoning:
  `agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`.
  `chained: none` — waiting on an unmet `depends_on: [ENG-040]`, nothing
  agent-actionable until it clears.

- 2026-09-06 no state change (eng-manager, `scheduled` event pass —
  whole-board sweep, step 5 merge detection). `ENG-040`'s `aiorders-api` PR
  #18 confirmed merged this same pass via local git ancestry, cross-checked
  with `gh pr view`, and carried through a full acceptance-check to
  `verified` (see `ENG-040`'s own board-file log) —
  `depends_on: [ENG-040]` is now satisfied.

  **Not transitioned to `building` in this pass.** Same precedent this board
  already set explicitly on `ENG-032`/`ENG-038`/`ENG-039` (a whole-board
  sweep does not perform new implementation work itself): the next hop is a
  real code edit against `restaurant-portal` (the questions page, the FAQ
  tab, `WebsiteFaqForm.tsx`) plus the required live-RLS confirmation named in
  this ticket's own Notes, and belongs in its own dedicated session per
  `eng_build_loop.md`'s "each heavy step gets its own session with fresh
  context," not this sweep.

  Confirmed this is the correct next pick: this is the only remaining member
  of the `ENG-021` family — no ordering choice to make. Machine WIP
  unaffected — this ticket was already inside the counted
  `ready`..`ready-to-ship` range as part of `ENG-021`'s family slot; moving
  it to `building` swaps which member is active, not how many. Owner stays
  `eng-manager` on this entry — reassignment to `frontend` happens at the
  `continue ENG-041` build hop itself, when the ticket actually starts, per
  this ticket's own `(created) → ready` entry above.

  **0 transitions.** `chained: ENG-041` — fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-041` before this pass exits, so a dedicated session performs
  `ready → building` (transition and implementation together, the same shape
  every other building hop on this board has used).

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.

- 2026-09-06 `ready → building → in-review` (frontend, `continue ENG-041`
  event pass). Owner `eng-manager → frontend` per the earlier entry's own
  standing instruction.

  **Required first step run before the query was written**, per this
  ticket's own Notes: live-project verification against `bmnmnejwdxbcqinqkwko`
  via `supabase db query --linked`. RLS is `ENABLED` on
  `public.ai_conversations` and the SELECT policy matches the tracked
  migration verbatim — **the load-bearing gate passes**, direct-read design
  proceeded. Informational: no `cleanup_old_ai_conversations` cron job
  actually exists (retention is unbounded in practice); session volume tops
  out at 585/restaurant (median 30), confirming "Load older" is not dead
  weight; a 100-row page is ~87.6 KB, well under the design's narrowing
  trigger. Full numbers: `agents/frontend/notebook/2026-09-06-eng041-build.md`.

  Built per design's Components rows 4-9: `types/website.ts` gains
  `WebsiteFaq`/`WebsiteContent.faqs`; new `WebsiteFaqForm.tsx` (mirrors
  `CateringPageForm.tsx`'s add/edit/remove idiom, seeds one entry from a
  `faqDraft` prop exactly once via a ref guard); `pages/website/Index.tsx`
  gains the third FAQs tab and the one-time `location.state.faqDraft`
  capture/clear; new `pages/questions/Index.tsx` (`useInfiniteQuery`
  keyset pagination, the design's own normaliser table implemented
  verbatim, throws from `queryFn` rather than swallowing errors into an
  empty state); `App.tsx`/`Sidebar.tsx` wire the route and nav entry
  (`MessageCircleQuestion`, immediately above Feedback). Did not touch
  `CateringPageForm.tsx`/`CateringFaq` or the admin-hub staff editor, per
  the design's explicit instruction. Added test coverage for the one
  genuinely new piece of logic (the draft-seed-once behaviour) plus the
  questions page's flattening/sort/error/empty states and the hand-off
  contract. Full detail: `agents/frontend/notebook/2026-09-06-eng041-build.md`.

  **Self-test, all clean against the `origin/main` baseline** (confirmed via
  `git stash -u`, not assumed): `npm run build` succeeds; `npm run lint` —
  96 problems, identical to baseline, zero in touched files; `npx tsc
  --noEmit -p tsconfig.app.json` — 12 pre-existing errors, identical to
  baseline, zero in touched files; `npm run test` — 40/40 pass (32
  pre-existing + 8 new).

  Branch `feat/ENG-041-customer-questions-and-faq-editor`, off
  `origin/main` (`8eea8f1`, post-`ENG-020`). Two commits pushed:
  `restaurant-portal@6be78ef` (feature),
  `restaurant-portal@81b00b1` (tests). No PR opened — devops's
  release-readiness step, not this hop's.

  **6b:** the artifact this ticket relies on (`update_website_content`'s
  widened `EDITABLE_PAGES`, `restaurant_website.faqs`) is application code
  already cross-referenced by the design's own "blast radius" section (bot,
  public site, schema.org) and by `ENG-040`'s own build hop; no new rule
  about a receipt path, state name, config key, or business-os process file
  was written or relied on by this hop, so no grep sweep was run.

  **2 transitions** (`ready → building`, `building → in-review`), under the
  cap of 4. Machine WIP unaffected — still `1/1`, held by the `ENG-021`
  family, and this is the family's last child.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract. **Notify sweep:** no new gate
  item this pass; checked the five open `inbox/` items fresh per the
  not-negotiable step 7 (`ENG-016`'s question, `ENG-018`/`ENG-028`/`ENG-042`'s
  G1s, `ENG-043`'s clarification question) against current time
  (`2026-09-06T17:06:56Z`) — `ENG-016`'s already carries its one-ever
  `nudged:` (2026-09-05); the other four are all `notified:` 02:28-03:13 the
  same day, ~14-15h old, under the 24h threshold. No nudge due on any.
  **Observations:** none beyond what's already in `observations.md`.
  **Exceptions/journal:** n/a — no `exception-request:`, no
  G1/G2/G3/merge-request answered this pass.

  Pre-pass state inherited clean from the prior pass's own post-pass run
  (recorded on its entry above); this pass's own post-pass `lib/eng-gate-check.sh`,
  scoped (`ENG-041`) and whole-board: both exit 0, clean.

  `chained: ENG-041` — `in-review` is agent-owned (`principal-engineer`/`qa`
  next, the combined review+quality hop, per `definition-of-done.md`'s state
  table), not the approver, not blocked, not terminal, not held by a cap.
  Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-041` before this pass exits.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.

- 2026-09-06 **code review round 1: FAIL — a real cross-restaurant data
  leak, not a style finding** (principal-engineer, `continue ENG-041` event
  pass). Mode check clean (repo-root `.env` → `MODE=active`). Pre-pass
  `lib/eng-gate-check.sh`, scoped (`ENG-041`) and whole-board: both exit 0,
  clean. Reviewed the branch tip (`restaurant-portal@81b00b1`) against
  `origin/main@8eea8f1` — diff matches the prior pass's own account exactly
  (578 insertions / 2 deletions, 8 files). **0/10 automatic failures.**
  Independently re-ran rather than trusted: `npm run test` (40/40),
  `npm run build` (clean), `npm run lint` (96 problems, identical to
  baseline, zero in touched files).

  **The finding.** `faqDraft` — the customer question carried from the
  Questions page's "Add to FAQs" hand-off — is captured once in `Website`'s
  own component state (`pages/website/Index.tsx` lines 24-30) with no
  restaurant id attached. `WebsiteFaqForm`'s guard against re-appending it a
  second time is a `useRef` (`draftConsumedRef`), which resets on every
  fresh *mount* of that component. `Website`'s own `content` query is keyed
  on `currentRestaurant?.id` with no `placeholderData`/`keepPreviousData`
  (grepped the repo — no page uses either), so switching restaurants flips
  `isLoading` back to `true` for a render, and the `if (isLoading) return`
  guard (line 111) — sitting above the `<Tabs>` return — unmounts and
  remounts `<Tabs>` and `WebsiteFaqForm` with it on every switch. `Website`
  the component does not itself unmount (same route, same instance), so
  `faqDraft` survives the switch untouched while the guard against reusing
  it does not. Net: an owner who manages 2+ restaurants — explicitly a
  supported case, the query's own `.eq('restaurant_id', ...)` filter exists
  because of it — can open Restaurant A's Customer Questions page, click
  "Add to FAQs," land on `/website` with the FAQ tab pre-filled and unsaved,
  switch to Restaurant B via the always-mounted `Sidebar` restaurant
  selector without saving, and have Restaurant A's customer's question
  silently re-appended — pre-filled, focused — onto Restaurant B's FAQ
  editor. If saved, that text is published to Restaurant B's public website
  and schema.org markup and fed into Restaurant B's bot context (this
  ticket's own design doc, "The FAQ column's blast radius is wider than the
  PRD knew") — a different restaurant's customer's free-text question,
  potentially containing PII per this ticket's own ADR-014, persisted
  somewhere ADR-014 assumed nothing gets copied to. **Blocking.** No test
  exercises this path — both `WebsiteFaqForm.test.tsx` cases `rerender()`
  one already-mounted instance rather than unmount/remount with different
  `content`, which is the correct test for the case they cover (post-save
  refetch, same restaurant) and not this one.

  **The fix:** scope the draft to the restaurant it was created for and
  drop it on mismatch — carry `restaurantId: currentRestaurant.id` alongside
  the question in `questions/Index.tsx`'s `handleAddToFaqs` navigation
  state, and have `Website`'s `faqDraft` capture (or `WebsiteFaqForm`'s
  consuming effect) discard the draft instead of applying it when
  `currentRestaurant.id` doesn't match. Bundle in the same round: the
  `{ question: string }` draft shape is currently declared inline in three
  files — export one `FaqDraft` type from `types/website.ts` while adding
  the id, rather than a fourth inline literal. Add a test: mount with a
  `faqDraft` scoped to a different restaurant than `currentRestaurant` and
  confirm it does not appear.

  Full trace of how each supporting fact was confirmed (RestaurantContext
  as a top-level provider, Sidebar's always-mounted selector, the
  no-`placeholderData` grep, the test-coverage check), one non-blocking
  type-sharing note, and one acknowledgment of good work:
  `agents/principal-engineer/notebook/2026-09-06-review-log.md`.

  No receipt written (`agents/principal-engineer/reviews/ENG-041.md` stays
  absent — pass-only, per `code-review-gate/SKILL.md` step 8). QA's side of
  this combined hop discarded per step 9; no
  `agents/qa/test-plans/ENG-041.md` written.

  **1 transition** — `in-review → building`, owner `principal-engineer →
  frontend` (this ticket's own frontmatter read `frontend` straight through
  the `in-review` hop rather than `principal-engineer` — same
  no-functional-consequence drift this board already corrected on
  `ENG-014`/`ENG-025`; a `continue` fire routes off `state:`, not `owner:`,
  so not re-flagged as a separate finding, just noted). Machine WIP
  unaffected — still `1/1`, held by the `ENG-021` family, this ticket its
  last child. One observation filed (`agents/eng-manager/observations.md`)
  — first occurrence on this board of transient hand-off state surviving a
  route-level remount unscoped to the entity it depends on.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract. **Notify sweep:** no new gate
  item this pass — a review fail is internal, not approver-facing; checked
  the four open `inbox/` items fresh against current time
  (`2026-09-06T17:21:16Z`): `ENG-016`'s question already carries its
  one-ever `nudged:`; `ENG-018`, `ENG-028`'s rescope, `ENG-042` and `ENG-043`
  are all `notified:` 02:28–03:13 the same day, ~14-15h old, under the 24h
  threshold. No nudge due on any. **Exceptions/journal:** n/a — no
  `exception-request:`, no G1/G2/G3/merge-request answered this pass.

  Pre-pass state inherited clean from the prior pass's own post-pass run;
  this pass's own post-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`) and
  whole-board: both exit 0, clean.

  `chained: ENG-041` — `building`/`frontend` is agent-owned, not the
  approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-041` before this pass exits.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.

- 2026-09-06 `building → in-review` — **review round 1's blocking finding
  fixed** (frontend, `continue ENG-041` event pass). Mode check clean
  (repo-root `.env` → `MODE=active`). Read the finding from this ticket's
  own log above plus the full trace in
  `agents/principal-engineer/notebook/2026-09-06-review-log.md` rather than
  re-deriving it.

  **The fix, exactly as specified by the review, nothing beyond it:**
  `src/types/website.ts` gains one exported `FaqDraft { question,
  restaurantId }`, replacing the `{ question: string }` shape that was
  declared inline in `WebsiteFaqForm.tsx`'s prop type and twice in
  `pages/website/Index.tsx` (the `FaqDraftState` interface and the
  `useState` type argument). `pages/questions/Index.tsx`'s
  `handleAddToFaqs` now carries `restaurantId: currentRestaurant.id`
  alongside the question in the navigation state (guarded by an explicit
  `if (!currentRestaurant) return` — the handler closure captures
  `currentRestaurant` from the outer scope, which TS does not narrow across
  even though the only caller, the "Add to FAQs" button, can't render before
  the component's own `!currentRestaurant` early return). `WebsiteFaqForm`
  takes the new prop `currentRestaurantId: string` (`Website` passes
  `currentRestaurant.id`, safe there — same function scope, after the
  narrowing check, not a separate closure) and its consuming effect now
  computes `faqDraft?.restaurantId === currentRestaurantId ? faqDraft :
  null` before checking `.question`, discarding a draft scoped to a
  different restaurant instead of applying it. Chose this location (the
  review's own "or" — `Website`'s capture, or `WebsiteFaqForm`'s consuming
  effect) over filtering in `Website` because it keeps the existing
  `WebsiteFaqForm.test.tsx` file's own established idiom — direct
  prop-driven unit tests, no router/query/context mounting — usable for the
  new case too.

  **Test added, per the review's own ask:**
  `WebsiteFaqForm.test.tsx` — "does not surface a draft scoped to a
  different restaurant": content `[{question: "Do you cater?", ...}]`,
  `faqDraft` scoped to `restaurant-1`, `currentRestaurantId="restaurant-2"`;
  asserts the draft question is absent and the FAQ count stays at the
  pre-existing one. The two existing `WebsiteFaqForm.test.tsx` cases and
  `pages/questions/Index.test.tsx`'s hand-off assertion updated for the new
  required prop / new field rather than left to bit-rot — not new coverage,
  the same behavior re-expressed against the new shape.

  **Self-test, all clean against the `origin/main` baseline** (same
  comparison method this ticket's first build hop used): `npm run test` —
  41/41 pass (40 prior + 1 new); `npm run build` — succeeds, same
  >500 kB chunk-size notice as baseline; `npm run lint` — 96 problems (62
  errors, 34 warnings), identical count to baseline, zero in touched files;
  `npx tsc --noEmit -p tsconfig.app.json` — 12 pre-existing errors,
  identical set to baseline, zero in touched files.

  Commit `restaurant-portal@64f9e82` on the existing branch
  `feat/ENG-041-customer-questions-and-faq-editor`, pushed. One commit, not
  split — type export, the two call-site fixes, and their tests are one
  indivisible change (the type change is what the call-site fixes and the
  new test compile against).

  **6b:** the artifact this hop relies on (`FaqDraft`, `restaurantId`) is
  application code introduced by this same ticket, not an existing rule
  another agent or process file already depends on — no grep sweep run, same
  conclusion as this ticket's first build hop for the same reason.

  **1 transition** (`building → in-review`), under the cap of 4. Machine WIP
  unaffected — still `1/1`, held by the `ENG-021` family, this ticket its
  last child.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract. **Notify sweep:** no new gate
  item this pass — a review fix is internal, not approver-facing; checked
  the five open `inbox/` items fresh against current time
  (`2026-09-06T17:33:40Z`): `ENG-016` already carries its one-ever
  `nudged:` (2026-09-05); `ENG-018` (~14h20m), `ENG-028` (~15h05m), `ENG-042`
  (~15h05m) and `ENG-043` (~14h46m) are all under the 24h threshold. No
  nudge due on any. **Observations:** none beyond what's already in
  `observations.md`. **Exceptions/journal:** n/a — no `exception-request:`,
  no G1/G2/G3/merge-request answered this pass.

  Pre-pass state inherited clean from the prior pass's own post-pass run;
  this pass's own post-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`) and
  whole-board: both exit 0, clean.

  `chained: ENG-041` — `in-review` is agent-owned (`principal-engineer`/`qa`
  next, the combined review+quality hop, review round 2), not the approver,
  not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-041` before this pass exits.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.

- 2026-09-06 `in-review → in-qa → in-security` — **round 2: review PASS,
  quality gate PASS** (principal-engineer + qa, combined hop, `continue
  ENG-041` event pass). Mode check clean (repo-root `.env` →
  `MODE=active`). Pre-pass state inherited clean from the prior pass's own
  post-pass run (recorded on its entry above).

  **Code review, round 2.** Diff: fix-only delta `81b00b1..64f9e82`, 6
  files, +79/-16 (round 1's own `81b00b1` diff already reviewed; not
  re-litigated). 0/10 automatic failures. Traced the fix against round 1's
  own repro by hand rather than trusting "restaurantId now flows through":
  A → add-to-FAQs → land on `/website` scoped to A → switch to B →
  `WebsiteFaqForm` remounts against B with a fresh `draftConsumedRef` →
  `faqDraft.restaurantId ('A') !== currentRestaurantId ('B')` → discarded.
  Also confirmed the fix's one undictated design choice (scoping the
  discard inside `WebsiteFaqForm`'s own effect rather than filtering in
  `Website`) against the review's own stated "or," and that the
  `{question}` triplication round 1 flagged non-blocking is now a single
  `FaqDraft` export used everywhere. **Verified the regression test, not
  assumed:** swapped in the pre-fix `WebsiteFaqForm.tsx` (`git show
  81b00b1:...` over the working copy), reran `WebsiteFaqForm.test.tsx`
  alone — the new "does not surface a draft scoped to a different
  restaurant" case fails, for the leak, and only that case; the other
  three stay green. Restored via `git checkout --`, worktree confirmed
  clean before continuing. Independent re-verification, not trusted from
  the log: `npm run test` 41/41, `npm run build` clean, `npm run lint` 96
  problems / zero in any touched file (grepped full output, not just the
  count), `npx tsc --noEmit` 12 pre-existing / zero in any touched file —
  all match exactly. **Verdict: PASS.** Receipt:
  `agents/principal-engineer/reviews/ENG-041.md`; `links.review` set.
  Full trace: `agents/principal-engineer/notebook/2026-09-06-review-log.md`.

  **Quality gate.** One coverage gap found on this ticket's owned ACs
  (AC1, AC2, AC6, UI-half AC3): AC1's "never another restaurant's" half
  had no test of its own — only live RLS, which authorises a
  multi-restaurant owner for *every* restaurant they manage, not just the
  one currently selected, so a dropped client-side filter would not be
  caught by RLS for that explicitly-supported case. The same ticket's
  round-1 finding was this identical shape on the FAQ-write side.
  **Closed directly** (QA's own "extend where coverage is thin," not
  bounced back to `building`): added
  `pages/questions/Index.test.tsx :: "scopes the query to the currently
  selected restaurant (AC1)"`, asserting `.eq('restaurant_id', 'rest-1')`
  on the query itself. Mutation-verified: removed the `.eq(...)` call from
  `questions/Index.tsx`, confirmed only the new test went red, restored via
  `git checkout --`, full suite green again after. Committed
  (`restaurant-portal@01c6ddb`) and **pushed** to the existing branch — the
  one write this hop makes to the project repo (business-os's own tracking
  below is separate; see closing note). All 4 owned ACs now covered;
  suite 42/42 (41 + this hop's 1); lint/build/typecheck re-confirmed clean
  in touched files including the new test; no open P0/P1 against this
  ticket (`agents/qa/bugs/_index.md`'s one entry, `BUG-001`, is
  `aiorders-api`, unrelated). **Verdict: PASS.** Test plan:
  `agents/qa/test-plans/ENG-041.md`. Coverage-gap note:
  `agents/qa/notebook/2026-09-06-coverage-gaps.md`.

  One observation filed (`agents/eng-manager/observations.md`) — two
  occurrences now, on this one ticket, of a multi-tenant scoping guarantee
  that was correct but rested on a single unreinforced mechanism (round
  1's hand-off state, this gate's missing regression test); named as worth
  promoting to a standard on a third occurrence anywhere on the board, not
  yet on two data points from one ticket.

  **2 transitions** (`in-review → in-qa`, `in-qa → in-security`), under
  the cap of 4. Owner `frontend → security` per `definition-of-done.md`'s
  state table. Machine WIP unaffected — still `1/1`, held by the
  `ENG-021` family, this ticket its last child.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract. **Notify sweep:** no new gate
  item this pass — an internal review/QA verdict isn't approver-facing;
  checked the five open `inbox/` items fresh against current time
  (`2026-09-06T17:53:04Z`): `ENG-016` already carries its one-ever
  `nudged:` (2026-09-05); `ENG-018` (~14h40m), `ENG-028` (~15h25m),
  `ENG-042` (~15h25m) and `ENG-043` (~15h05m) are all under the 24h
  threshold. No nudge due on any. **Exceptions/journal:** n/a — no
  `exception-request:`, no G1/G2/G3/merge-request answered this pass.

  Pre-pass state inherited clean from the prior pass's own post-pass run;
  this pass's own post-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`)
  and whole-board: both exit 0, clean.

  `chained: ENG-041` — `in-security` is agent-owned (`security` next), not
  the approver, not blocked, not terminal, not held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-041` before this pass exits.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains
  open, not re-decided here. (Distinct from `restaurant-portal`, the
  project repo, which this hop did commit and push to — that repo's own
  convention is that finished work ships on its branch regardless of
  business-os's own tracking state.)

- 2026-09-06 `in-security → ready-to-ship` — **security gate: PASS**
  (security, `continue ENG-041` event pass). Reading map for `continue`:
  steps 6 and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
  instructed*; *The four lanes*; *Guards*). Mode check clean (repo-root
  `.env` → `MODE=active`). Project autonomy re-confirmed directly
  (`config/projects.md`): `restaurant-portal` is L1, not L0 — full scanning
  permitted. Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`) and
  whole-board: both exit 0, clean.

  **Threat-modelled the change** (four questions, full answers in the
  receipt): no new unauthenticated input, no new capability class, no new
  audience for the data exposed, no cross-tenant escalation on full
  compromise — both enforcement points (RLS, `requireRestaurantAccess`)
  independently re-confirmed live, not assumed.

  **Cross-repo dependency re-verified live, not taken on any ticket's
  word.** The design's own Risks section names the real precondition: this
  ticket's parent widens a write path whose ownership check was, before
  `ENG-022`, discarded rather than enforced. `git fetch` +
  `git log -1 --oneline origin/main` against `aiorders-api` (not
  `ENG-040`'s branch tip — `origin/main` is what this ticket's frontend
  actually calls) → HEAD is `5e36648`, `ENG-040`'s own merge commit; grepped
  `website.ts` at that tip — both call sites use `requireRestaurantAccess`
  (`ENG-022`'s throwing fix), not the pre-fix `verifyRestaurantAccess`. The
  design's Rollout step 0 precondition holds today, on the actual code path.

  **OWASP walk, all ten, each marked applicable-and-clean or `n/a` with a
  reason** — full table in the receipt. A01 (this ticket's real risk)
  reviewed in depth: independently re-confirmed round 1's fix (the
  FAQ-draft cross-restaurant leak) by reading the actual diff — not
  trusting the review log — and grepping both regression tests directly
  out of their test files rather than inferring them from the test plan's
  prose. A03: grepped the full diff for `dangerouslySetInnerHTML`/
  `innerHTML`/`eval(`/`new Function`/`document.write` — zero hits; customer
  free text renders through plain JSX, React's default escaping intact. A04
  (write-payload shape/size validation): traced to `ENG-040`'s own diff and
  already-logged non-blocking finding, not a fresh occurrence on this
  ticket's surface — not re-logged. A06: confirmed no manifest/lockfile in
  the 8-file diff.

  **Secrets:** `git diff` and `git log -p` across all four commits vs
  `origin/main`, grepped for key/secret/token/password/bearer/service-role/
  PEM patterns — no hits, diff or history. **Dependencies:** none new or
  bumped.

  **PII handling (`ADR-014`) checked control-by-control against the shipped
  code, not the design doc's claims:** never in a URL (confirmed —
  `react-router` state only), never in a log line (confirmed — only
  `error.code` logged), only the customer's own turns ever rendered
  (confirmed — `role !== 'user'` filter read directly), no export path
  (confirmed absent), nothing persisted until the owner explicitly saves
  (the hand-off is in-memory state, cleared on consume). Classified
  **Restricted** per `security-baseline.md`.

  **RLS on `ai_conversations`:** corroborated the tracked migration text
  directly (`20250903152559_*.sql`) against the design's and the build
  hop's quoted policy — verbatim match. Its live-enabled state was
  confirmed by this same ticket's own build hop, same day, via a direct
  `supabase db query --linked` — not redundantly re-queried here; nothing
  plausibly changed between that check and this one, and re-running an
  identical live query minutes later would be re-deriving evidence already
  fresh on record, not verifying anything new.

  **Negative-case coverage:** both tenant-boundary tests this ticket's own
  history required exist and were read directly out of the test files
  (`WebsiteFaqForm.test.tsx`'s cross-restaurant-draft case,
  `pages/questions/Index.test.tsx`'s AC1 scoping case); both were already
  mutation-verified by earlier hops in this same pipeline (guard/filter
  removed, only the intended test went red, restored clean) — not re-run
  mechanically since that evidence is fresh and on record. Server-side
  enforcement (RLS denial, `requireRestaurantAccess` denial) is exercised
  by `aiorders-api`'s own negative tests, already confirmed present at
  `ENG-040`'s gate; this diff adds no server-side code to re-test.

  **SOC 2 trail:** ticket → PRD → design → review (round 2 pass) → QA
  (pass) → this verdict → release record (pending). No gap.

  **Verdict: PASS. Zero blocking findings, zero new non-blocking
  findings** — the one candidate (A04) traces to an already-logged
  `ENG-040` finding, not a fresh instance, so nothing new was written to
  `agents/security/notebook/`. Receipt: `agents/security/reviews/ENG-041.md`;
  `links.security_review` set on the ticket in the same edit.

  **1 transition** (`in-security → ready-to-ship`), owner `security →
  devops`, under the cap of 4. Machine WIP unaffected — still `1/1`, held
  by the `ENG-021` family, this ticket its last child.

  **Dead-end sweep (scoped to this event):** no other ticket touched — a
  `continue` event's own narrower contract. **Notify sweep:** no new gate
  item this pass — a security pass verdict isn't approver-facing (only a
  fail or a risk-acceptance escalation would be); checked the five open
  `inbox/` items fresh against current time (`2026-09-06T18:05:55Z`):
  `ENG-016` already carries its one-ever `nudged:` (2026-09-05); `ENG-018`
  (~14h52m), `ENG-028` (~15h37m), `ENG-042` (~15h37m) and `ENG-043`
  (~15h18m) are all under the 24h threshold. No nudge due on any.
  **Observations:** none beyond what's already in `observations.md` — no
  new process pattern surfaced this pass. **Exceptions/journal:** n/a — no
  `exception-request:`, no G1/G2/G3/merge-request answered this pass.

  Pre-pass state inherited clean from the prior pass's own post-pass run;
  this pass's own post-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`) and
  whole-board: both exit 0, clean.

  `chained: ENG-041` — `ready-to-ship` is agent-owned (`devops` next, the
  release-readiness hop), not the approver, not blocked, not terminal, not
  held by a cap. Fired
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-041` before this pass exits.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here. No write to `restaurant-portal` this hop — a
  read-only review of its existing branch.

- 2026-09-06 **release-readiness: PR opened, blocked on approver** (devops,
  `continue ENG-041` event pass). Entry kept short per `conventions.yaml` →
  `ticket_log.entry.cap_lines: 20`; full reasoning:
  `agents/devops/notebook/2026-09-06-release-readiness-log.md`.

  All three upstream gates re-verified fresh, still passing (review round 2,
  QA, security). No migration owed. Readiness gate held, no blocking
  failure — rollback fine (single-branch revert, near-fully-additive diff,
  not drilled — no CI dashboard access), cost $0/month; no client-side error
  tracking exists anywhere in this repo, a pre-existing gap already accepted
  at this gate on `ENG-002`/`ENG-032`/`ENG-039`, not introduced here. Opened
  `restaurant-portal` PR #5; raised `inbox/2026-09-06-eng041-merge-request.md`.

  **1 transition** — `ready-to-ship → blocked`, `blocked_on: approver`,
  `blocked_from: ready-to-ship`, owner `devops → approver`, `links.pr` set.
  WIP unaffected — still `1/1`, `ENG-021` family, this ticket its last
  child. `chained: none` — waiting on the approver, an L1 merge is a human
  gate.

  This is `ENG-021`'s last sub-ticket — once this PR merges and ships, the
  parent qualifies for its own `ADR-003`-class exemption.

  business-os left uncommitted — standing default, open.

- 2026-09-06 no state change (eng-manager, `watch` event pass, context
  `launchd`). File-watcher fired on this ticket's own merge-request file
  appearing in `inbox/`. Reading map for `watch`: steps 2-4 (sweep all
  three inboxes) and step 5 (changed file is a merge-request item), plus
  the not-negotiable set. Mode check clean; pre/post-pass
  `lib/eng-gate-check.sh` scoped+whole-board both exit 0.

  Swept all three inboxes: nothing answered, nothing new to act on. Step 5:
  `git fetch` + `git merge-base --is-ancestor` on `restaurant-portal` — PR
  #5 still open, not merged (`gh pr view 5` confirms `state: OPEN`,
  `mergedAt: null`). No transition. Full reasoning, the notify-sweep
  timestamp table, and the timezone-basis check:
  `agents/eng-manager/notebook/2026-09-06-eng041-watch-recheck.md`.

  **0 transitions.** `chained: none` — waiting on the approver, unchanged
  (`blocked`, `blocked_on: approver`).

  business-os left uncommitted — standing default, open.

- 2026-09-06 no state change (eng-manager, `scheduled` event pass, context
  `launchd`, ~15:30 PDT). Whole-board safety-net sweep, reading map: whole
  document. Mode check clean; pre/post-pass `lib/eng-gate-check.sh`
  scoped+whole-board both exit 0.

  Step 5: `git fetch` + `git merge-base --is-ancestor` on `restaurant-portal`
  — PR #5 still open, not merged; cross-checked with `gh pr view 5`
  (`state: OPEN`, `mergedAt: null`). No transition.

  **0 transitions.** `chained: none` — waiting on the approver, unchanged
  (`blocked`, `blocked_on: approver`).

  business-os left uncommitted — standing default, open.

- 2026-09-06 no state change (eng-manager, `scheduled` event pass, context
  `auto-drain`, ~19:12 PDT). Whole-board safety-net sweep, reading map: whole
  document, never narrowed. Mode check clean; pre/post-pass
  `lib/eng-gate-check.sh` scoped+whole-board both exit 0.

  Step 5: `git fetch` + `git merge-base --is-ancestor` on `restaurant-portal`
  — PR #5 still open, not merged; cross-checked with `gh pr view 5`
  (`state: OPEN`, `mergedAt: null`). The immediately preceding `watch` pass
  (19:02–19:10) had skipped this check — its own trigger file wasn't a
  merge-request item — so this is the first fresh re-check since ~15:30;
  nothing changed in the interim.

  **0 transitions.** `chained: none` — waiting on the approver, unchanged
  (`blocked`, `blocked_on: approver`).

  business-os left uncommitted — standing default, open.

- 2026-09-06 no state change (eng-manager, `scheduled` event pass, context
  `launchd`, ~20:30 PDT). Whole-board safety-net sweep, reading map: whole
  document, never narrowed. Mode check clean; pre/post-pass
  `lib/eng-gate-check.sh` scoped+whole-board both exit 0.

  Step 5: `git fetch` + `git merge-base --is-ancestor` on `restaurant-portal`
  — PR #5 still open, not merged; cross-checked with `gh pr view 5`
  (`state: OPEN`, `mergedAt: null`). ~1h20m since the last fresh check
  (19:10 `auto-drain` pass); nothing changed in the interim.

  **0 transitions.** `chained: none` — waiting on the approver, unchanged
  (`blocked`, `blocked_on: approver`).

  business-os left uncommitted — standing default, open.

- 2026-09-07 `blocked → shipped → verified` (eng-manager, `scheduled` event
  pass, context `launchd`, ~02:00 PDT). Whole-board safety-net sweep, reading
  map: whole document, never narrowed. Mode check clean (repo-root `.env` →
  `MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`) and
  whole-board: both exit 0, clean.

  **Step 5:** `git fetch` + `git merge-base --is-ancestor` on
  `restaurant-portal` — **now an ancestor of `origin/main`**, the first
  change since the 11:16 PDT open. Cross-checked with `gh pr view 5`:
  `state: MERGED`, `mergedAt: 2026-09-07T06:18:50Z`, base `main`, head this
  ticket's own branch, no stacking.

  **"A merge is not a gate" — receipts re-verified fresh before advancing.**
  All three: `agents/principal-engineer/reviews/ENG-041.md` (`Verdict: PASS`,
  round 2), `agents/qa/test-plans/ENG-041.md` (`last_result: pass`, 4/4 owned
  ACs), `agents/security/reviews/ENG-041.md` (`verdict: pass`, zero blocking
  findings) — all still read `pass` today, unchanged since raised. No
  migration owed (confirmed again: no schema/data-model change in the diff).

  **Zero drift.** `git diff 01c6ddb origin/main --stat` (the QA-reviewed
  tip vs. the merged tree) is empty. Merge commit `f649583`'s own two
  parents are `8eea8f1` (`main`'s tip at merge time) and `01c6ddb` (this
  ticket's own reviewed tip) — a plain merge, nothing else rode in on it.

  **Confirmed actually deployed, not just merged:** `gh run list --branch
  main` on `restaurant-portal` shows a "Deploy to Cloudflare Pages" run at
  `head_sha f649583`, `createdAt: 2026-09-07T06:18:53Z` (3 seconds after the
  merge), `status: completed`, `conclusion: success`.

  **Full `acceptance-check/SKILL.md` walk run**, not the receipt-bookkeeping
  shortcut — this ticket owns real, checkable behaviour (AC1, AC2, AC6 in
  full, AC3's UI half), not a 0-criteria schema-only shape. Independently
  re-verified beyond the ticket's own claims by reading the merged source
  directly: the questions query's `.eq('restaurant_id', ...)` scoping
  (AC1); the distinct empty-state card vs. the distinct error-state card
  (AC2); `flattenSession`'s `role === 'user'`-only filter plus
  `sortNewestFirst` (AC6); and, for AC3's UI half, both the
  `handleAddToFaqs` hand-off (react-router state, never a URL parameter,
  carrying `restaurantId`) and `WebsiteFaqForm`'s
  `faqDraft?.restaurantId === currentRestaurantId ? faqDraft : null` guard
  — the round-1 cross-restaurant-leak fix, confirmed present in the actual
  shipped code, not just claimed in the review log — and the `Save FAQs`
  submit wired to the same `update_website_content` write path `ENG-040`
  already verified. All 4 owned criteria: **pass**. No non-goal built
  (`CateringPageForm.tsx`/`CateringFaq`/admin-hub editor all absent from the
  8-file merge diff). Cost: `$0/month`, no manifest/lockfile touched,
  matches estimate. Full walk:
  `agents/product-manager/notebook/2026-09-07-eng041-acceptance.md`; release
  record: `agents/devops/releases/2026-09-07-restaurant-portal-ENG-041.md`.

  Merge-request item's `## Decision` filled with a plain-language resolution
  note and moved to `inbox/_handled/2026-09-06-eng041-merge-request.md` —
  `decision:` frontmatter field itself left blank, same convention every
  prior silent-merge item on this board has used.

  **2 transitions** (`blocked → shipped`, `shipped → verified`), well under
  the cap of 4 — receipt re-confirmation, live-deploy check, and a full
  acceptance-check, no new implementation work.

  **This was `ENG-021`'s last sub-ticket.** Both children (`ENG-040`,
  `ENG-041`) are now `shipped`/`verified` — the parent's own `ADR-003`-class
  exemption (all children settled, at least one shipped — here, both) is
  now satisfied. `ENG-021` itself is not touched in this pass — same
  precedent `ENG-016`'s/`ENG-019`'s own closing passes already set: the
  parent's no-diff shipped transition gets its own dedicated hop rather
  than being processed inline by a whole-board sweep. Machine WIP
  unaffected throughout — this ticket left the counted `ready`..
  `ready-to-ship` range at its own prior `ready-to-ship → blocked` hop; the
  slot has been held by the `ENG-021` family the whole time (`ENG-021`
  still `building` until its own chained pass carries it to `shipped`).

  **6b:** not applicable — no build hop ran this pass; the artifacts this
  ticket relies on were already checked for cross-file mentions at their
  own build hops.

  **Dead-end sweep:** see the board index's own whole-board sweep notes for
  this pass. **Notify sweep:** this ticket's own merge-request item is now
  resolved and archived — nothing to nudge on it. The six other open
  `inbox/` items checked fresh (see the board index's own entry for this
  pass) — none past the 24h threshold yet. **Observations:** none new.
  **Exceptions/journal:** n/a — no `exception-request:` found; the
  merge-request item was resolved by silent GitHub merge, not an answered
  gate, so no decision-journal entry is owed (same disposition every prior
  silent merge on this board has used).

  Pre-pass and post-pass `lib/eng-gate-check.sh`, scoped (`ENG-041`) and
  whole-board: all four runs exit 0, clean.

  `chained: none` — `verified` is terminal; the chaining guard never fires
  on a terminal ticket. `chained: ENG-021` fired instead — recorded on
  `ENG-021`'s own consequence, see the board index's entry for this pass:
  `/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
  continue ENG-021`.

  business-os itself left uncommitted through this edit — same standing
  default every pass has used; the commit-convention question remains open,
  not re-decided here.
