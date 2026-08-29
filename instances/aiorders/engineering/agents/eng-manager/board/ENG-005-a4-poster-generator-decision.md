---
id: ENG-005
title: Decide and act on the orphaned A4PosterGenerator component
project: aiorders-admin-hub
type: chore
size: S
severity: P3
priority:
state: verified
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-25
updated: 2026-08-28
branch: chore/ENG-005-a4-poster-generator-wire-in
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md
  design: agents/architect/designs/ENG-005-a4-poster-generator-wire-in.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-005.md
  test_plan: agents/qa/test-plans/ENG-005.md
  security_review: agents/security/reviews/ENG-005.md
  release: agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md
---

## Input

Verbatim, from `inbox/requests/2026-08-23-a4-poster-generator-unwired.md`
(now `inbox/_handled/`), filed by the approver, received 2026-08-23 —
preserved here per `skills/request-readback/SKILL.md` step 1, never edited:

> A4PosterGenerator is committed but not reachable
>
> `src/components/A4PosterGenerator.tsx` was committed to `aiorders-admin-hub`
> on 2026-08-23 (`bfddffe`) so the work would be tracked rather than sitting
> loose in the working tree. Nothing imports it — a grep across `src/` finds
> no reference outside the file itself. It is in the repo and unreachable
> from the running app.
>
> **What this asks for:** First decide whether it is wanted, then act on the
> answer. If it is, wire it into a route or a surface in the admin hub and
> say which. If it is not, delete it — `bfddffe` is a single-file commit
> specifically so reverting it is clean.
>
> Small, and genuinely low stakes. Worth capturing only so a
> committed-but-dead component does not quietly become permanent.

Full text in the handled request file.

## Readback

See `agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md` →
Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

`A4PosterGenerator.tsx` is fully committed to `aiorders-admin-hub` but
unreachable from the running app — nothing imports it. Whether it's wanted
at all is the open question the request itself leads with.

## Outcome

Either the component is wired into a named, reachable surface in the admin
hub, or `bfddffe` is cleanly reverted — whichever the approver decides at
G1.

## Notes

**Not yet gated, and for a different reason than `ENG-004`.** This ticket's
`size: S` + `type: chore` would ordinarily auto-skip G1 per
`config/definition-of-done.md`'s Size table — but the ticket's entire scope
depends on an unresolved fork (wire in vs. delete) that only the approver
can settle, so G1 is being required anyway as a deliberate judgement call,
not because the size/type mechanics demand it. See the PRD's Readback
section for the reasoning. Separately, and on top of that: even if G1 were
being raised this pass, `wip.approver_limit` (2) had exactly one free slot
and it went to `ENG-003` — see that ticket's log.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-25` `intake → shaped` (product-manager) — shaped from
  `inbox/requests/2026-08-23-a4-poster-generator-unwired.md` (filed by the
  approver, received 2026-08-23, unprocessed for two days — a `scheduled
  manual-unblock` sweep pass's PM work, not a self-originated finding). Ran
  the full request-readback (`skills/request-readback/SKILL.md`): this PM's
  reading plus a blind architect reading (independent subagent, raw request
  + business profile + the admin-hub registry row only) — no material
  divergence; the architect's reading added a plausible print/QR-poster
  hypothesis (not treated as fact) and flagged a real risk this PM's first
  pass missed: the component may depend on code that exists only in
  `admin-hub`'s 64 uncommitted human-checkout files, which could make
  "wire it in" fail for reasons invisible to this department. See the PRD.
  PRD written at
  `agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`,
  deliberately without committed acceptance criteria for either branch of
  the fork (see PRD step 5 note) — writing criteria for an unmade decision
  would be inventing scope, which `skills/prd-writer/SKILL.md`'s own
  failure-modes list warns against.

  **G1 required despite auto-skip eligibility — logged explicitly since this
  deviates from the mechanical rule.** `size: S` + `type: chore` ordinarily
  skips G1 per the Size table ("S: Yes, unless bug/chore"). Requiring it
  anyway is a judgement call: the skip exists for routine work whose shape
  is already understood, and this ticket's shape — wire in vs. delete — is
  exactly the thing G1 exists to settle, not a scope this PM can responsibly
  guess at just because the ticket is small. Treated as a shaping judgement
  call in the same spirit as the doc-inconsistency calls `ENG-002`'s pass
  made (logged, not hidden), not as a formal process exception under
  `agents/eng-manager/config/exceptions.md` — no established rule is being
  broken, since neither `config.yaml` nor `definition-of-done.md` addresses
  what to do when a ticket's own scope is the open question.

  **G1 not raised this pass regardless** — `wip.approver_limit` (2) had one
  free slot, which went to `ENG-003` (see that ticket's log for the
  ordering). Holding at `shaped`, owner `product-manager`. `chained: none`
  — held by the WIP cap; the next dispatch's To-do-column pick-up
  (`schedules/eng_build_loop.md` step 6) advances this, not a chain fired
  from here.
- `2026-08-27` `shaped → awaiting-scope` (product-manager, `scheduled`
  event pass — twice-daily safety-net sweep) — dispatch, board-wide per the
  event's own contract. `ENG-005` was the only ticket in the To-do column
  (`intake`/`shaped`/`awaiting-scope`) this pass found: `ENG-004` already
  sits past its own G1 at `ready`, and its dedicated `continue` session is
  separately queued (`traces/.pending`), so it wasn't competing for the same
  slot. Re-checked the caps fresh rather than trusting the board's cached
  header: `wip.approver_limit` (2) at 0, `wip.approval_cap` (3) at 0/3 — both
  fully free, so nothing blocks raising this ticket's G1 now. Wrote the gate
  item as the fork itself rather than a plan to approve, per this ticket's
  own PRD framing ("tell us which of two things you want," not "approve this
  plan") — `inbox/2026-08-27-eng005-g1-scope.md`, `agent: product-manager`,
  `recommendation:` states no build recommendation and asks the approver to
  choose wire-in-and-name-the-surface vs. revert. Ran
  `departments/engineering/lib/eng-notify.sh raise
  inbox/2026-08-27-eng005-g1-scope.md`; stamped `notified: 2026-08-27T09:59:41`
  in the gate item's own frontmatter. PRD `status: shaped → awaiting-scope`
  (`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`).

  **Consequence:** approver-facing WIP 0 → 1; approval cap 0/3 → 1/3.
  `owner` moves `product-manager → approver` per
  `config/definition-of-done.md`'s state table. `chained: none` — sitting at
  `awaiting-scope`, owned by the approver; the chaining guard never fires on
  a ticket waiting on a human.
- `2026-08-27` (still `awaiting-scope`, `watch` event pass — a hand-edited
  gate item in a watched inbox, not a channel reply) — swept all three
  watched inboxes per the event's own contract and found
  `inbox/2026-08-27-eng005-g1-scope.md` changed since the last pass touched
  it: `decision: approved`, `decided: 2026-08-27T18:03:50.514589+00:00`, a
  second `## Decision` section appended below the original placeholder —
  same hand-edit shape every gate on this instance but `ENG-002`'s merge has
  used. The answer's text is `wire it in`, with no route/surface named.

  **Read as a partial answer, not a complete one, and acted on as such.**
  This G1's own text asked for two things in one reply — "Wire it in — and
  name the route/surface it should appear on, so acceptance criteria can be
  written against it" — and only the first came back. The fork is genuinely
  settled: the component is wanted, the revert branch is closed, no reading
  of "wire it in" leaves that ambiguous. The surface is not — and this
  ticket's own PRD calls that out twice, in its Readback's "Assumed" section
  and again in Non-goals, as a decision the department does not get to make
  quietly. Treated the same way `skills/prd-writer/SKILL.md` treats any
  ambiguity that changes the work: one question back, not a guess.

  **Investigated before asking, rather than reflecting the question back
  unhelped.** `git fetch origin` in `_eng/aiorders-admin-hub`, then read
  `A4PosterGenerator.tsx` off `origin/main` directly: its props
  (`restaurantName`, `websiteUrl`, `logoUrl`, `primaryColor`,
  `restaurantId`) are a single restaurant's own detail context, not a
  picker. Listed all 19 pages under `src/pages/` and the sidebar
  (`AppSidebar.tsx`); exactly one page is shaped to hold that context —
  `RestaurantDetails.tsx`, which already loads `name`, `website`, `logo_url`
  and `id` for one restaurant (`Restaurants.tsx` is the list view). No
  existing poster/QR/marketing section there to slot into, so wiring it in
  means a new section, not enabling something half-built. This is offered as
  a recommendation in the follow-up, not adopted as the answer — the PRD's
  non-goal is explicit that naming the surface is the approver's call, and a
  well-evidenced guess is still a guess.

  **Ticket log and PRD updated, original gate item closed out, one narrow
  follow-up raised.** PRD `## Decision`
  (`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`)
  filled in with the approver's words and this interpretation, `status`
  left at `awaiting-scope`. `inbox/2026-08-27-eng005-g1-scope.md` moved to
  `inbox/_handled/` with one appended line pointing at the follow-up — it is
  fully read and acted on, not abandoned mid-file. Wrote
  `inbox/2026-08-27-eng005-g1-followup-surface.md` (`agent: product-manager`,
  `gate: scope`, `follow_up_to:` the closed item), ran
  `departments/engineering/lib/eng-notify.sh raise` on it (reproduced the
  already-filed `MODE`-collision bug — `sent: active`, not `sent: raise`,
  `traces/eng-notify-2026-08-27.log` 11:17:06 — corroborating, not new), and
  stamped `notified: 2026-08-27T18:16:48`. Journaled in
  `agents/eng-manager/config/decision-journal.md`: the sixth data point on
  hand-edited gate answers on this instance, and the first where a G1's own
  requested sub-detail went unanswered.

  **State held at `awaiting-scope` — did not advance to `designed`.**
  `definition-of-done.md` names `designed`'s owner as the architect, whose
  job is technical design, not naming a product surface the PRD explicitly
  reserved for the approver; sending this to `designed` without a surface
  would make the architect guess exactly what this ticket refuses to guess,
  one state later and with a technical-design label instead of a scope one.
  `owner` stays `approver`. No cap impact — still the same one open
  approver-facing item this ticket already held (approval cap unchanged at
  1/3, approver WIP unchanged at 1), just a narrower question on the same
  slot.

  **`chained: none`** — sitting at `awaiting-scope`, owned by the approver;
  the chaining guard never fires on a ticket waiting on a human.
- `2026-08-27` `awaiting-scope → designed → ready` (product-manager, then
  architect, then eng-manager — `decision` event pass, narrow scope per the
  event contract: act on the answered gate item and advance only this
  ticket). Mode check clean (`MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.

  **The follow-up's answer:** `decision: approved`, `decided:
  2026-08-27T20:08:53.367622+00:00`, text "lets do RestaurantDetails.tsx" —
  confirms the PM's recommendation as given, no different surface named.
  Both halves of the original G1 (fork, then surface) are now answered, so
  `awaiting-scope`'s own exit condition ("G1 approved in `inbox/`") is met.
  PRD updated
  (`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`):
  `status: designed`, `decided:` stamped, acceptance criteria filled in
  concretely now that the surface is known (route
  `/restaurants/:id/details`, discoverable via existing navigation — no new
  nav entry needed). Gate item moved to `inbox/_handled/` with a processed
  footer. Journaled in
  `agents/eng-manager/config/decision-journal.md`.

  **Design work done this pass, not deferred to a separate hop** — acted as
  architect per the same one-pass pattern `ENG-002` used at this identical
  boundary (`awaiting-scope → designed → ready` in one pass when no one-way
  door exists). Investigated fresh against `origin/main` in both
  `_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch origin` in
  both first) rather than trusting the follow-up's summary secondhand:
  confirmed the `url-shortener` edge function the component calls actually
  exists (`supabase/functions/url-shortener/index.ts`), confirmed `jspdf`
  `^4.2.0` is already a dependency in admin-hub's `package.json` (no new
  dependency), read `RestaurantDetails.tsx` in full (900 lines) and found its
  `Restaurant` interface has **no color field anywhere** — the follow-up's
  own investigation never claimed `primaryColor` was loaded (it listed only
  the four fields that are: `name`, `website`, `logo_url`, `id`), so this
  isn't a correction of that work, just the next question it didn't need to
  answer. The design passes `primaryColor={null}` and lets the component's
  own fallback accent apply. Confirmed the route (`/restaurants/:id/details`, behind the
  existing `<ProtectedRoute>`) satisfies the "discoverable, not just a direct
  URL" requirement with zero new nav wiring. Design written:
  `agents/architect/designs/ENG-005-a4-poster-generator-wire-in.md` —
  `one_way_doors: []`. **No one-way door** — additive UI section,
  self-contained already-committed component, already-deployed edge
  function, no schema change, no new dependency, one-file-revert reversible
  — so `awaiting-decision` (G2) is skipped entirely per
  `definition-of-done.md`'s own rule that G2 is "only entered when a
  one-way door exists." No ADR filed, matching the design's own conclusion.

  **`ready` reached the same pass** — acted as eng-manager: breakdown is one
  task (one `<Card>` added to `RestaurantDetails.tsx`'s existing grid,
  rendering `<A4PosterGenerator>` with the four real props plus
  `primaryColor={null}`), no sequencing needed, assigned to frontend.
  `machine_wip` (`ready` through `ready-to-ship`) 0/6 → 1/6 — slot was free.
  Approver-facing WIP 1 → 0; approval cap 1/3 → 0/3 (this ticket's G1 was the
  only open item on either count).

  **2 transitions this pass** (`awaiting-scope → designed`, `designed →
  ready`), well under the cap of 4. Did not proceed into `building` —
  writing the actual code is new implementation work, which per
  `schedules/eng_build_loop.md` step 6 is exactly where a pass stops and
  hands off to a fresh session instead of pushing through.

  **Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
  state with a chain record below. No other ticket is in flight to check —
  `ENG-004` is terminal (`verified`); out of scope for a `decision` event
  naming this ticket anyway.

  **Notify sweep:** nothing to raise this pass (`designed`/`ready` raise no
  gate item — no one-way door, no G2). Nothing to nudge. Approval cap now
  0/3, not full — no stall.

  `chained: ENG-005` — sitting at `ready`, owned by eng-manager (an agent,
  not the approver, not blocked, not terminal). Fired `/bin/zsh
  departments/engineering/lib/eng-trigger.sh continue ENG-005` for the
  dedicated `building` (frontend) session. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.
- `2026-08-27` `ready → building → in-review → in-security → ready-to-ship`
  (frontend, then principal-engineer + qa combined, then security, then
  devops — `continue ENG-005` event pass). Narrow scope per the event
  contract (resume this ticket from its current state; no board-wide sweep).
  Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.

  **Recovered an unrecorded build before doing anything else.** The dedicated
  `building` session the prior pass chained had already run: the worktree
  (`_eng/aiorders-admin-hub`) was on branch
  `chore/ENG-005-a4-poster-generator-wire-in`, up to date with `origin`, tree
  clean, carrying one commit (`51cdb29`, "Wire A4PosterGenerator into
  RestaurantDetails") this ticket's log had no record of — that session did
  real work and died before writing back, exactly `ENG-002`'s precedent for
  the same failure shape. `traces/.hops-2026-08-27-ENG-005` reads `2`,
  confirming this is the second dispatch of `continue ENG-005` today (the
  first produced the commit, this one is the recovery). Ruled out a live
  concurrent session before trusting any of it: walked the full process
  ancestry (`ps` + `ppid` chain) from this session's own `claude` pid up to
  the `eng-trigger.sh scheduled launchd` invocation holding `traces/.loop.lock`
  — that invocation is this pass's own top-of-chain orchestrator (it drained
  the already-queued `continue ENG-005` event ahead of its own `scheduled`
  event, oldest-first, per the queue's own rule), not a second instance; the
  `traces/.pass-out.*` file mirroring this session's own narration is that
  same orchestrator's cost-logging child (`run-stream.py`), not a competing
  session.

  **Independently verified the recovered commit rather than trusting it.**
  Read the full diff (`git show 51cdb29`): one file, 18 lines, exactly the
  architect's design — import plus one `<Card>` in the page's existing grid,
  the four real `Restaurant` fields (confirmed present by name:
  `id`/`name`/`website`/`logo_url`) plus `primaryColor={null}`, type-checked
  against the component's own `Props` (`primaryColor: string | null`).
  `grep -rn "A4PosterGenerator" src/`: exactly one import, one usage, no
  duplication. `npm run lint` on the branch: 181 problems (150 errors/31
  warnings); `git checkout origin/main --detach` and re-ran: identical count,
  identical last line — zero new lint findings, checked back out to the
  ticket's branch afterward (`git status` clean, same commit at the tip).
  `npm run build`: succeeds. No dependency added (`package.json`/lockfile
  absent from the diff), so no audit delta is possible. Full detail in
  `agents/principal-engineer/reviews/ENG-005.md`. `building`'s exit condition
  (`definition-of-done.md`: "branch pushed, self-tested") is met.

  **`in-review` (combined review + quality hop).** Acted as principal-engineer:
  automatic-failure scan clean (0/10), design conformance confirmed, verdict
  **pass** — `agents/principal-engineer/reviews/ENG-005.md`,
  `links.review` set. Acted as qa: wrote the test plan
  (`agents/qa/test-plans/ENG-005.md`) mapping both PRD acceptance criteria to
  the build/structural checks available on a project with no test command
  (`config/projects.md` confirms no `Test` cell for `aiorders-admin-hub`);
  traced the one real failure path (a caller with no/failed/non-admin
  session) through the component's own try/catch and optional-chaining to
  confirm it degrades silently rather than crashing. Verdict **pass**,
  `links.test_plan` set. Per `skills/code-review-gate/SKILL.md` step 9, both
  clearing together advances straight to `in-security` — no separate `in-qa`
  sit-state.

  **`in-security`.** Threat-modelled the diff: no new input, and the one new
  *capability reachability* question — does wiring in a dormant component
  quietly widen who can do what — traced to no. Read `aiorders-api`'s
  `url-shortener` edge function directly (`git fetch` first): every action
  the component calls (`list`, `create`) requires a Bearer token plus
  `profiles.role === 'admin'`, fail-closed, unchanged by this ticket; only
  the unrelated `redirect` action is intentionally public (the QR's own
  target, meant for customers scanning a printed poster). OWASP walk: A01 and
  A07 checked as real content, the rest `n/a` with reasons. No secrets. SOC 2
  trail complete. Verdict **pass** — `agents/security/reviews/ENG-005.md`,
  `links.security_review` set.

  **`ready-to-ship`.** Acted as devops: all three upstream receipts verified
  present and non-empty on disk (not assumed from frontmatter). No migration
  (`touches_data: false`). Rollback is reverting the one commit; observability
  is unchanged (no new failure path — the component's existing silent-degrade
  behavior is what QA/security both traced). Cost: $0/month — no new
  infrastructure, the QR edge function is already deployed and billed under
  existing usage. Release window: Thursday 2026-08-27, ~15:40 local,
  `MODE=active`, no `ENG_RELEASE_FREEZE` set — no freeze. Confirmed
  `aiorders-admin-hub` has no push-to-`main` CI/CD (`.github/workflows/`
  absent) and `deploy-cf` is a manual `wrangler pages deploy` script, same
  shape `ENG-002` found on `restaurant-portal` — deploying is outside L1
  autonomy regardless (a human merges; a human or their own process deploys),
  so nothing was run here beyond confirming that's still true.

  **Not opening the PR or moving to `blocked` this pass, deliberately — the
  4-transition cap.** Counting from this pass's own starting state (`ready`):
  `ready→building`, `building→in-review`, `in-review→in-security`,
  `in-security→ready-to-ship` is already 4 transitions, `eng_build_loop.md`
  step 6's stated cap. Opening the PR and entering `blocked` is real,
  distinct devops work (`ENG-002`'s own precedent bundles it with the
  transition *into* `blocked`, not before) — reserved for the next hop rather
  than pushed through over the cap. `machine_wip` unchanged at 1/6 —
  `ready-to-ship` is inside the counted range, same as `ready` was.
  Approval cap and approver-facing WIP both unchanged (0/3, 0) — none of
  this pass's four transitions raise a gate item.

  **Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
  state with a chain record below. No other ticket in flight to check —
  `ENG-006` (`awaiting-scope`, owner approver) is out of scope for a
  `continue` event naming this ticket.

  **Notify sweep:** nothing to raise this pass (none of `building`,
  `in-review`, `in-security`, `ready-to-ship` raise a gate item). Nothing to
  nudge. Approval cap unchanged at 0/3, not full — no stall.

  `chained: ENG-005` — sitting at `ready-to-ship`, owned by devops (an agent,
  not the approver, not blocked, not terminal). Fired `/bin/zsh
  departments/engineering/lib/eng-trigger.sh continue ENG-005` for the
  dedicated session to open the L1 PR and raise the merge-request gate.
  Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
  whole-board: both exit 0, clean.
- `2026-08-27` `ready-to-ship → blocked` (devops — `continue ENG-005` event
  pass, the dedicated session the preceding pass chained specifically to open
  the L1 PR). Narrow scope per the event contract (resume this ticket from
  its current state; no board-wide sweep). Mode check clean (business-os
  `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean. `traces/.hops-2026-08-27-ENG-005` read `3` — third
  dispatch of `continue ENG-005` today, well under `hops_per_ticket` (8,
  `plan.tier: pro`).

  **Checked for an already-opened PR before creating one** — the immediately
  preceding pass recovered one unrecorded build already today, so a duplicate
  PR was a real risk, not a formality. `gh pr list --head
  chore/ENG-005-a4-poster-generator-wire-in --state all`: empty. None existed.

  **Opened the real PR** (`gh pr create`, title "Wire A4PosterGenerator into
  RestaurantDetails"): https://github.com/harsimranwalia/aiorders-admin-hub/pull/2.
  Body states what changed, why, and the three gate verdicts. Wrote the L1
  merge-request item (`inbox/2026-08-27-eng005-merge-request.md`, `gate:
  merge`, `agent: eng-manager`) carrying the PR link and the three gate
  verdicts by file reference. Ran `departments/engineering/lib/eng-notify.sh
  raise` — reproduced the already-filed `MODE`-collision bug (`sent: active`,
  not `sent: raise`, `traces/eng-notify-2026-08-27.log` 16:03:58) — eighth-plus
  corroborating occurrence per the open `proposals.md` row, not a new finding.
  Stamped `notified: 2026-08-27T16:03:58` by hand, since the script never
  writes back to the item either way. State → `blocked`, `blocked_on:
  approver`, `blocked_from: ready-to-ship`, owner `devops → approver` — the
  same design `config.yaml`'s `gates.merge_request` describes, and the one
  `ENG-002` used at this identical boundary.

  **Cap check before this transition, read fresh rather than trusted from the
  board header.** `wip.approver_limit` (2) was at 1 (`ENG-006`'s G1);
  `wip.approval_cap`/`awaiting_approver_cap` (3) was at 1/3 (same item).
  `ENG-005` is an already-in-flight, already-fully-gated ticket reaching its
  own next gate, not a new start — `approver_limit`'s stated consequence
  ("nothing NEW starts") is untouched, matching `ENG-002`'s own reasoning at
  this exact boundary. Advancing brings `awaiting_approver_cap` to 2/3 (not
  over) and `approver_limit` to 2/2 (at the limit, not over) — proceeded on
  that basis.

  **1 transition this pass** (`ready-to-ship → blocked`), well under the
  cap of 4 — opening the PR and writing the gate item is itself the real work
  of this hop, same as `ENG-002`'s precedent. `machine_wip` 1/6 → 0/6
  (`blocked` sits outside the `ready`..`ready-to-ship` range). Approver-facing
  WIP 1 → 2; approval cap 1/3 → 2/3.

  **Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
  state with a chain record below. `ENG-006` (`awaiting-scope`, owner
  approver) untouched — out of scope for a `continue` event naming this
  ticket, and already correctly waiting on its own G1.

  **Notify sweep:** this pass's own gate item raised and stamped above.
  Nothing to nudge (brand new). Approval cap now 2/3, not full — no stall.

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
  the whole hop was driving toward; firing `continue ENG-005` again would just
  re-queue against a ticket with nothing left for a machine to do until the
  approver merges the PR or replies to the gate item. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.
- `2026-08-28` `blocked → shipped → verified` (devops, then product-manager —
  `decision` event pass, context `inbox/2026-08-27-eng005-merge-request.md`).
  Narrow scope per the event contract (act on the answered gate item, advance
  only this ticket). Mode check clean (business-os `.env` → `MODE=active`).
  Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
  whole-board: both exit 0, clean.

  **The gate item's answer:** `decision: approved`,
  `decided: 2026-08-28T00:13:09.817494+00:00`, text "merged" — the tracked
  channel this time, unlike `ENG-002`'s direct-GitHub/control-center bypass.
  **Not taken on the text alone** — ran the loop's own merge-detection check
  (`schedules/eng_build_loop.md` step 5) from scratch in the department's own
  worktree (`~/Documents/projects/_eng/aiorders-admin-hub`, never the human's
  checkout): `git fetch origin` showed `919d355..edf6947 main -> origin/main`;
  `git merge-base --is-ancestor chore/ENG-005-a4-poster-generator-wire-in
  origin/main` confirmed the branch head is an ancestor; `git log origin/main
  --oneline` showed `edf6947` (the PR's own merge commit) directly on top of
  `51cdb29` (this ticket's commit) on top of `919d355` — no intervening
  commits, `git diff` between the branch tip and `origin/main` empty. The
  merge commit's own timestamp (`2026-08-27T17:12:49-07:00` =
  `2026-08-28T00:12:49Z`) lands ~20s before the gate item's `decided:` stamp —
  consistent with the approver merging and recording the decision in the same
  sitting. The claim checks out.

  **Acted as devops, closing out `shipped`'s exit condition**
  (`config/definition-of-done.md`: "Deployed, health checks green, release
  record written") **for what an L1 project can actually attest to.**
  Re-confirmed directly rather than trusting the ticket's earlier
  `ready-to-ship` note: `.github/workflows/` absent from `origin/main`;
  `deploy-cf` is still a manual `wrangler pages deploy` script. Checked out
  `origin/main` detached in the worktree and ran `npm run build`: succeeds,
  and the emitted bundle now includes `html2canvas`/`purify.es`/`index.es`
  chunks absent from a build where the component is unreachable — corroborates
  it's genuinely wired in, not just present in the tree. `grep -rn
  "A4PosterGenerator" src/pages/RestaurantDetails.tsx` on the merged tree:
  one import, one usage (line 904). **Unlike `ENG-002`, did not write
  `health_check: green`** — this release has a real new production-facing
  artifact once deployed, deploying is outside L1 autonomy regardless of diff
  content (a human merges; a human or their own process deploys), and this
  department has no Cloudflare/monitoring access to confirm whether that's
  happened yet. Recorded `health_check: not checked` and `rollback_tested:
  false` honestly rather than inferring a status unavailable to observe. Wrote
  the release record from what was actually found:
  `agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md`,
  `links.release` set. Checked the worktree back onto its own branch afterward
  (`git status` clean, same commit at the tip) — never left detached.

  **Acted as product-manager, confirming both acceptance criteria against the
  live (merged) tree** (`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`):
  AC1 (renders without error in a new section) — `npm run build` above
  succeeding on the merged tree is the same proof QA's test plan used, now
  re-run against `origin/main` instead of the pre-merge branch; the new
  `<Card>` sits inside the same `restaurant &&`-guarded branch as every other
  card. AC2 (reachable via existing navigation, not just a direct URL) —
  confirmed no new route or nav entry exists on `origin/main`; the route
  itself (`src/pages/RestaurantDetails.tsx`) is unchanged, only its rendered
  content grew. Both hold. PRD `status: designed → verified`.

  **Gate item closed out.** `inbox/2026-08-27-eng005-merge-request.md` moved
  to `inbox/_handled/` with a processed footer. Journaled in
  `agents/eng-manager/config/decision-journal.md`.

  **2 transitions this pass** (`blocked → shipped`, `shipped → verified`),
  well under the cap of 4. **Approval cap:** `ENG-005` no longer counts (was
  one of 2/2 approver-facing, 2/3 approval cap, both as `blocked_on:
  approver`) — `verified` is terminal and owes nothing to either cap.
  Approver-facing WIP 2 → 1; approval cap 2/3 → 1/3 (`ENG-006`'s G1 is the
  one remaining item on both). `machine_wip` unchanged at 0/6 — neither
  `blocked` nor `verified` sits inside the counted `ready`..`ready-to-ship`
  range.

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in a
  valid, accounted-for terminal state. `ENG-006` (`awaiting-scope`, owner
  approver) untouched and out of scope for a `decision` event naming this
  ticket.

  **Notify sweep:** nothing to raise this pass (`verified` raises no gate
  item). Nothing to nudge — the merge-request item is now answered and closed,
  not sitting open. Approval cap now 1/3, not full — no stall.

  `chained: none` — `verified` is a terminal state. Nothing left for a machine
  or the approver to do on this ticket. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board:
  both exit 0, clean.
