---
id: ENG-010
title: Influencer relationship notes — staff log for personality, preferences, and off-platform conversations
project: aiorders-admin-hub
type: feature
size: S
time_estimate: a few hours to half a day
time_spent: ~1h build (ready → building, not itemized by that pass — a pre-existing gap named here rather than backfilled with an invented figure) + ~45m code review round 1 (fail) + ~20m fix hop (guarded both async callbacks with a ref) + ~45m code review round 2 (fail — missing RLS) + ~20m fix hop (enabled RLS + policy) + ~45m code review + quality round 3 (pass) + ~30m security gate (pass) + ~20m release-readiness (both PRs opened, stacked on ENG-009's branch)
time_remaining: 0 machine time — release-readiness done, both PRs open. What's left is the approver's own merge, on their own schedule (L1).
severity: P3
priority:
state: blocked
owner: approver
lane: full
blocked_on: approver
blocked_from: ready-to-ship
source: approver
created: 2026-08-29
updated: 2026-09-02
branch: feat/ENG-010-influencer-relationship-notes (aiorders-api@486eec0, aiorders-admin-hub@8b90f0e)
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-010-influencer-relationship-notes.md
  design: agents/architect/designs/ENG-010-influencer-relationship-notes.md
  adrs: []
  review: agents/principal-engineer/reviews/ENG-010.md
  test_plan: agents/qa/test-plans/ENG-010.md
  security_review: agents/security/reviews/ENG-010.md
  release:
  pr:
    - repo: aiorders-api
      url: https://github.com/harsimranwalia/aiorders-api/pull/8
    - repo: aiorders-admin-hub
      url: https://github.com/harsimranwalia/aiorders-admin-hub/pull/7
---

## Input

Verbatim, from the approver's own reply to `ENG-009`'s G1 item
(`inbox/2026-08-29-eng009-g1-scope.md`, still open at the time this ticket
was filed — see that ticket), decided 2026-08-29T09:20:42.679606+00:00, a
rider appended after the plain "approved" answer rather than a separate
inbox item — preserved here per `skills/request-readback/SKILL.md` step 1,
never edited:

> potentially add notes by the staff to collaborate on the influencer and
> see how their personality is or what they want/like or what
> conversations have happened with them off the platform. we want our
> community mangers(staff) to be able to more easily use these influencers
> for our restaurant campaings.

## Readback

See
`agents/product-manager/specs/ENG-010-influencer-relationship-notes.md`
→ Readback — the full two-reading comparison lives there rather than
duplicated here.

## Problem

Community managers build up real knowledge about an influencer —
personality, preferences, what's been discussed off-platform — but today
that knowledge lives only in the individual manager's memory or private
messages, so it doesn't transfer when a different staff member (or the
same one, later) needs to activate that influencer for a restaurant
campaign.

## Outcome

Any staff member viewing an influencer's admin record can read every note
previously left about that influencer (who wrote it and when) and add a
new one. Nothing else on the influencer record changes; nothing an
influencer can see about themselves changes.

## Notes

**New scope arriving through a gate-reply channel, not the normal inbox —
treated as new business intake, not folded into `ENG-009`.** The approver
answered `ENG-009`'s G1 with a plain approval and then added this,
unprompted, in the same reply. It doesn't extend `ENG-009`'s own two
signals (internal activity, social figure) and isn't testable as part of
that ticket's acceptance criteria — it's a materially different capability
(a freeform, multi-author notes log) with its own risk profile
(influencer-visibility is the central concern here; neither of `ENG-009`'s
signals carries that risk). Per `definition-of-done.md`'s "scope
discovered outside G1 is never silently absorbed," shaped and filed as its
own ticket in the same pass rather than appended to `ENG-009`'s already-
approved scope.

**Full readback run, not skipped.** Unlike `ENG-009` (which reused the
divergence-check already run for `ENG-008`'s standing engagement question,
since the approver's answer there was itself already a spec), this
addendum had not been through any prior two-reading comparison — a plain
feature description, not an answer to a posed question. Ran it fresh: no
material divergence found. See the PRD's own Readback section.

**Sequencing.** No hard dependency on `ENG-008` or `ENG-009`, but all
three touch the same admin-UI file (`src/pages/Influencers.tsx`) and the
same influencer record — building them back to back rather than
concurrently avoids a needless merge conflict. Likely last of the three
given it was raised last and depends on nothing the other two produce;
the EM's call at `ready`, not decided here.

**The one risk this ticket cannot get wrong:** influencers hold real
AIOrders accounts (`user_id` on the influencer record, per `ENG-008`'s own
design evidence). Staff commentary about a person, readable by that same
person, is the concrete failure mode — flagged prominently in the PRD's
Risks section and carried into acceptance criterion 4 as an explicit
negative-authorization test, not left implicit for QA/security to catch
later.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager,
  `intake` event pass, context the original influencer-board request
  file — this ticket is downstream of that same request via `ENG-009`'s
  G1 reply, not a fresh unrelated card). Mode check clean (business-os
  `.env` → `MODE=` empty). Caps checked fresh before raising: at the point
  this G1 was written, `ENG-008` and `ENG-009` had both already cleared
  their own approver-facing states earlier in this same pass, so
  approver-facing WIP stood at 0/2 and approval cap at 0/3 — both fully
  free.

  **Ran the full request-readback** (`skills/request-readback/SKILL.md`):
  this PM's own reading plus a blind architect reading (a subagent given
  only the raw addendum text, `knowledge/business-profile.md`, and
  `agents/eng-manager/config/projects.md`, model `opus` per the skill,
  explicitly instructed not to read any existing ticket/PRD/design file
  about influencer work so the reading stayed genuinely blind). **No
  material divergence** — both converged on a multi-entry, authored/
  timestamped, staff-only, never-influencer-visible notes log attached to
  the influencer record. The architect's reading added technical texture
  (named the `user_id` mechanism behind the visibility risk, raised the
  open question of brand/agency/reseller admin-hub roles, flagged
  discoverability) rather than disagreement — per the skill's own
  classification table, "fine, proceed." No question put to the approver.

  **Sized `S`.** PRD written:
  `agents/product-manager/specs/ENG-010-influencer-relationship-notes.md`,
  acceptance criteria and non-goals naming the influencer-visibility
  boundary and the open brand/reseller-role question explicitly.

  **G1 required** — full lane, not XS/bug/chore. Wrote
  `inbox/2026-08-29-eng010-g1-scope.md` (`agent: product-manager`, `gate:
  scope`, `project: aiorders-admin-hub`, recommendation to build now, this
  ticket sequenced last of the three influencer tickets). Ran
  `departments/engineering/lib/eng-notify.sh raise`; see the item's own
  frontmatter for the result and `notified:` timestamp.

  **No dissent section** — `agents/critic/agent.md` doesn't exist at the
  department or instance level (confirmed absent again this pass); same
  already-open proposal (`proposals.md`, 2026-08-25 row), not refiled.

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver`. **Consequence:** approver-facing WIP
  0 → 1 (cap 2); approval cap 0 → 1 (this G1). `machine_wip` unaffected.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract — not run beyond this request's own lineage (`ENG-008`,
  `ENG-009`, this ticket).

  **Notify sweep:** this pass's own item raised and stamped above. Nothing
  else to nudge. Approval cap 1/3 (after this pass's net changes across
  all three tickets — see board index), not full — no stall.

  **Observations filed** (`observations.md`): a second data point (after
  `ENG-006`'s SMS-vendor rider) of this approver using a G1 reply to add
  new, unprompted content rather than only answering the question it
  asked.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human.

- `2026-08-29` `awaiting-scope → designed → ready` (architect, then
  eng-manager — `scheduled` event pass, context `schtasks`). Found this
  ticket's own G1 (`inbox/2026-08-29-eng010-g1-scope.md`) answered
  `decision: approved`, `decided: 2026-08-29T10:49:55.456343+00:00`,
  sitting unprocessed — part of the four-item answered-but-unprocessed
  backlog this board's header had flagged for five consecutive passes.
  Mode check clean (`MODE=` empty); pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Real design work done against the live repos. Also corrects an
  unverified citation in this ticket's own `## Notes`**, found while
  checking it rather than repeating it: the "one risk this ticket cannot
  get wrong" cited "`user_id` on the influencer record, per `ENG-008`'s
  own design evidence" — `ENG-008`'s design doc never says that. The risk
  is real regardless, confirmed by different, checked evidence: influencers
  authenticate as `profiles` rows with `role: 'influencer'`
  (`20250729143357_initial_restaurant_rls.sql`), and `admin-portal`'s own
  router-level `authenticate()` already excludes that role from every route
  under it — the new handler adds one further, narrower check on top
  (`admin`/`sub-admin` only, excluding `partner-admin`/`partner-user`,
  since this ticket's own G1 already defaulted brand/agency/reseller
  visibility to no). Full detail: `agents/architect/designs/
  ENG-010-influencer-relationship-notes.md`.

  **New table (`influencer_notes`), new dedicated handler** — not an
  extension of `ENG-008`/`ENG-009`'s shared `influencers.ts`, since notes
  are their own list/append sub-resource with a narrower authorization
  boundary than that file's base gate. No existing notes concept found
  anywhere in the repo (checked before designing one from scratch).

  **No one-way door** — a new, isolated table with no existing reader and
  no data migrated into it; reversible by `DROP TABLE` with zero blast
  radius elsewhere. No change to any existing table or to the shared
  router gate (the narrower check lives inside the new handler only).
  Moved straight through `designed` without a G2.

  Moved `inbox/2026-08-29-eng010-g1-scope.md` → `inbox/_handled/` with a
  processed footer. **Journaled** in `agents/eng-manager/config/
  decision-journal.md` (not previously recorded — unlike `ENG-009`'s G1,
  this one had not yet been journaled).

  **2 transitions** (`awaiting-scope → designed → ready`), well under the
  cap of 4. **Consequence:** machine WIP 5/6 → 6/6 (this ticket now inside
  the counted `ready`..`ready-to-ship` range, alongside `ENG-007`/
  `ENG-008`/`ENG-009`/`ENG-011`/`ENG-013` — **at cap, not over**; nothing
  further should start into this band until one clears); approver-facing
  WIP and approval cap unaffected (this G1 was already off both counts
  before this pass).

  **Dead-end sweep:** this ticket's own resolution is this entry; see the
  board index and `observations.md` for this pass's whole-board findings.

  `chained: none — held for sequencing.` Same reasoning as `ENG-009`,
  one step further down the same queue: this ticket's own G1 named it
  "last of the three influencer tickets," and its design reuses the same
  admin-auth pattern `ENG-008`/`ENG-009` establish first. `ENG-008`'s
  chain is being re-fired this same pass; re-check `ENG-009` and `ENG-010`
  once it's built. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: see board index.

- `2026-08-29` **the predicted twin no-op: G1 scope decision event arrived
  after its own fact was already consumed** (eng-manager, `decision` event
  pass, context `inbox/_handled/2026-08-29-eng010-g1-scope.md`). Per this
  event's own narrower contract, scoped to `ENG-010` only — no board-wide
  sweep. Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean.

  **Confirmed rather than assumed.** This item's own frontmatter carries a
  processed footer naming the exact pass that consumed it — "Processed
  2026-08-29 (`scheduled` event pass, context `schtasks`)": design work
  done (new `influencer_notes` table, dedicated handler), the ticket moved
  `awaiting-scope → designed → ready` in the log entry directly above,
  journaled (`agents/eng-manager/config/decision-journal.md`), and the gate
  item itself already moved to `inbox/_handled/`. Checked fresh rather than
  trusted: this ticket's own frontmatter (`state: ready`, `owner:
  eng-manager`) agrees with the footer. Nothing left for this event to act
  on.

  **0 transitions.** No cap affected — this ticket was already inside the
  counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before
  this pass, and this G1 was already off both the approver-facing WIP and
  approval-cap counts.

  **Dead-end sweep (scoped to this event):** `ENG-008` — the ticket this
  one's own sequencing hold depends on — still sits at `ready` with no
  branch or build started in either worktree. This ticket's existing
  sequencing hold (re-check once `ENG-008` reaches `in-review` or later)
  therefore still applies unchanged. Nothing to resume or fix.

  **Notify sweep:** nothing to raise (no new gate item); nothing to nudge
  (this item's `notified:`/`decision:` cycle closed same-day, hours before
  this pass).

  `chained: none` — no state change; this ticket remains deliberately held
  at `ready` pending `ENG-008` reaching `in-review` or later, per the
  reasoning already recorded above. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean. Also recorded on the board index
  (`_index.md`, matching dated entry).

- `2026-08-29` **approver override, filed by hand in an interactive session —
  not a department pass.** Same instruction and reasoning as the matching
  entry just added to `ENG-009`'s log this same moment: run `ENG-009` and
  `ENG-010` next, ahead of `ENG-008` finishing its `in-review` gate, instead
  of letting `.pending` work through several unrelated fires queued ahead
  of all four tickets first. `priority: → next` set directly by the
  approver. `traces/.pending` reordered by hand to `continue ENG-009,
  continue ENG-010, continue ENG-008, continue ENG-013` at the front, rest
  of the prior queue preserved behind them.

  **Known risk, same as ENG-009's:** this ticket's own design also extends
  the same not-yet-created handler file `ENG-008` (still `building`, not
  yet `in-review`) is building against — the conflict the sequencing hold
  exists to prevent hasn't actually cleared. Approver's call to accept that
  risk; if it surfaces, it's a rebase, not a bug. No other field changed;
  state stays `ready`, owner stays `eng-manager`.

- `2026-08-29` **approver reversal, same interactive session, minutes
  later.** Matching `ENG-009`'s own entry just added: new instruction is to
  clear the `building`/`in-review` queue (`ENG-008`, `ENG-013`) before
  going to `ready` tickets, superseding (not deleting) the override just
  above. `priority: next → ` (empty), reverted to match the original
  sequencing hold's own logic. `traces/.pending` reordered by hand to
  `continue ENG-008, continue ENG-013, continue ENG-009, continue ENG-010`.
  State stays `ready`, owner stays `eng-manager` — back to simply waiting
  behind `ENG-008`.

- `2026-08-29` `continue ENG-010`: sequencing hold re-checked, still unmet,
  `ready → ready` (no chain) (eng-manager, `continue` event pass, context
  `ENG-010` — draining the approver's hand-reordered queue, last of the four
  (`ENG-008`, `ENG-013`, `ENG-009` already worked this pass sequence)).
  Narrow scope per this event's own contract (resume this ticket from its
  current state; no board-wide sweep). Mode check clean (business-os `.env`
  → `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean.

  **Re-checked the sequencing hold's own condition rather than assuming it
  still holds — same check just run for `ENG-009`, same result.** This
  ticket sits at `ready`, held pending `ENG-008` reaching `in-review` or
  later — both tickets' designs extend the same not-yet-created
  `admin-portal/handlers/influencers.ts`. Read `ENG-008`'s own frontmatter
  and ticket-log tail directly rather than trusting this board's In-flight
  table: `state: building`, latest entry confirms round-1's test gap was
  closed this same pass sequence (`aiorders-api@dc6972a`) and round-2 code
  review is next, but it has not yet reached `in-review`. The hold's
  condition is therefore still unmet. Checked `agents/eng-manager/inbox/`,
  `agents/product-manager/inbox/` and `inbox/` for anything newly filed
  against `ENG-010` specifically — none found (the one item sitting in
  `agents/eng-manager/inbox/`, `2026-08-29-restaurant-detail-write-partner-
  exposure.md`, is unrelated to this ticket, out of scope for this event).

  **0 transitions.** State stays `ready`, owner stays `eng-manager`,
  `priority` stays empty (per the approver's own reversal recorded above).
  **Consequence:** machine WIP unaffected — verified fresh from each
  counted ticket's own `state:` field: `ENG-008` `building`, `ENG-009`/
  `ENG-010` `ready`, `ENG-013` `building` — still 4/1, over the new cap,
  draining naturally per the board header. Approver-facing WIP and approval
  cap both unaffected — no gate touched.

  **Dead-end sweep (scoped to this event):** nothing to resume — this is a
  deliberate wait with a re-verified condition, not a stall. `ENG-008`
  (the dependency) is already chained and progressing under its own event.
  **Notify sweep:** nothing to raise (no new gate item); nothing to nudge.

  `chained: none` — held for sequencing, unchanged from the prior entry:
  `ENG-008` has not yet reached `in-review`. Re-check once it does. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

- `2026-08-29` sequencing hold re-checked, still correctly held — the
  ticket ahead of it changed, not the outcome (eng-manager, `scheduled`
  event pass, context `schtasks`, whole-board sweep). `ENG-008` itself has
  now reached `in-qa` (past `in-review`), so the letter of this ticket's
  own stated condition is technically met — but this ticket's own `## Notes`
  names it explicitly as **last of the three** influencer tickets,
  sequenced behind `ENG-009` as well as `ENG-008` (same admin-UI file,
  `src/pages/Influencers.tsx`). `ENG-009`'s hold was lifted this same pass
  (see its own log) but it has not built yet — `state: ready`, no branch.
  This ticket's hold therefore still applies, now keyed on `ENG-009`
  reaching `in-review` or later rather than `ENG-008`.

  **0 transitions.** State stays `ready`, owner stays `eng-manager`.
  **Consequence:** machine WIP unaffected — already inside the counted
  range.

  `chained: none` — held for sequencing: re-check once `ENG-009` reaches
  `in-review` or later. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.
- `2026-08-31` **stale hold reason corrected, no state change** (eng-manager,
  `scheduled` event pass, context `launchd` — whole-board sweep). Same
  correction as `ENG-009`'s own log this same pass: this ticket's hold
  reason, "pending `ENG-008` reaching `in-review` or later," has been
  satisfied for hours (`ENG-008` passed round 2 review, quality, and
  security today, and now sits `blocked` on the approver's own merge).
  Re-verified before touching anything: machine WIP is still 2/1 — only this
  ticket and `ENG-009` occupy the counted `ready`..`ready-to-ship` range now
  that `ENG-008`/`ENG-013` both left it for `blocked` — still over the cap
  the approver set 2026-08-29, and that cap, not the original sequencing
  reason, is what now holds this ticket at `ready`. **Conclusion unchanged
  (stay at `ready`, do not start `building`); reason corrected** so a future
  pass doesn't mistake the stale text for a lapsed hold. Git ancestry
  independently confirms neither `ENG-008` nor `ENG-013` has merged yet (see
  the board index's own dated entry for this pass).

  **0 transitions.** No cap change.

  `chained: none` — still held by the machine-WIP cap (2/1, over), not by
  the sequencing reason this ticket's log previously cited. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean, no `WAIVED:` lines.

- `2026-09-02` **both hold reasons cleared, dispatched — chain fired for the
  build hop** (eng-manager, `scheduled` event pass, context `launchd`,
  15:30 — whole-board sweep). Re-checked this ticket's own two hold reasons
  directly rather than carrying forward either the board index or this
  log's own last entry, same ticket-file-over-table discipline `ENG-009`'s
  2026-09-02 09:30 entry established for the identical class of drift.

  **Sequencing hold:** last stated as waiting on `ENG-009` reaching
  `in-review` or later (this ticket's `## Notes` names it last of three
  sequenced against the same file, `src/pages/Influencers.tsx`). `ENG-009`'s
  own board file now reads `state: blocked`, `blocked_from: ready-to-ship`
  as of today — past `in-review`, `in-qa`, and `in-security` entirely;
  `ENG-008` (the earlier dependency) is at the identical point. Both
  tickets' PRs on both repos re-confirmed still open via `gh pr view` this
  pass (not merged, so no conflict has landed yet), but the risk the hold
  existed to prevent — building against a design either dependency might
  still change — is over: neither diff changes further from here, only
  merges. Condition satisfied.

  **Machine-WIP hold:** this log's own last entry cited "2/1, over" as of
  2026-08-31. Re-derived fresh from each counted ticket's own frontmatter
  rather than trusted forward: `ENG-008`/`ENG-013` (`blocked`,
  `blocked_from: ready-to-ship` since 2026-08-31) and now `ENG-009`
  (`blocked`, `blocked_from: ready-to-ship`, today's 09:02 devops hop) have
  all three left the counted `ready`..`ready-to-ship` range — matching
  `ENG-009`'s own log and this pass's board-index update. `ENG-010` is the
  sole remaining occupant: **1/1, exactly at cap, not over.** It is the
  ticket the slot belongs to, not one waiting behind it — the cap bars a
  *new* ticket from entering `ready`, not this one from proceeding.

  **Both hold reasons this ticket's log has ever cited are now satisfied.**
  No branch exists yet (`branch:` empty in frontmatter) — the actual build
  has not started. Per this loop's own design ("a pass stops after
  `building`... each heavy step gets its own session with fresh context"),
  this whole-board sweep does not start the implementation itself; it hands
  off to a dedicated hop instead.

  **0 transitions this pass** — state stays `ready`; `building` gets written
  by the session that actually opens the branch, not by a detection pass.
  **Consequence:** none yet — machine WIP stays 1/1 until that hop starts.

  `chained: ENG-010` — sole occupant of the machine-WIP-1 slot, agent-owned
  (`eng-manager`), not the approver, not blocked, not terminal, no cap left
  actually holding it. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean, no `WAIVED:` lines.

- `2026-09-02` `ready → building`: built per the design, both repos
  (eng-manager, `continue` event pass, context `ENG-010`, this ticket's turn
  at the front of `traces/.pending`). Narrow scope per the event's own
  contract (resume this ticket from its current state; no board-wide sweep).
  Mode check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean.

  **Both `_eng` worktrees already sat on `ENG-009`'s own tip, clean** —
  convenient rather than assumed: `git status` showed a clean tree on both
  before touching anything, `git fetch origin` confirmed neither
  `feat/ENG-009-influencer-engagement-info` branch had moved
  (`aiorders-api@d37e0c9`, `aiorders-admin-hub@92bcacd`, both matching this
  ticket's own prior-read evidence exactly). Branched
  `feat/ENG-010-influencer-relationship-notes` off that tip in **both**
  repos — this ticket's own `## Notes` already named it last of the three
  influencer tickets, sequenced behind `ENG-009` as well as `ENG-008`, and
  the frontend dependency is a hard one (`src/pages/Influencers.tsx` carries
  every field `ENG-008`/`ENG-009` added; branching off a stale copy would
  create exactly the merge conflict the sequencing hold existed to avoid).
  Neither `ENG-008`'s nor `ENG-009`'s own branch refs were disturbed —
  reconfirmed after branching (`57f8c4b`/`63be255` and `d37e0c9`/`92bcacd`
  respectively, both unchanged).

  **No Supabase MCP tool available this session** — checked via `ToolSearch`
  before writing the migration, unlike `ENG-008`'s and `ENG-009`'s own build
  hops, which both re-verified live schema state through it. Filed as an
  observation (`observations.md`) rather than assumed to be a permanent
  capability change — it may be this session's own tool configuration.
  Relied on static evidence instead (migrations-directory listing, a
  repo-wide grep for any colliding name, and the architect design's own
  same-week live-schema reading of `influencers`/`profiles`) — full
  reasoning and the resulting narrower gate verdict in
  `agents/database/migrations/ENG-010-influencer-relationship-notes.md`,
  which says plainly that its evidence is weaker than `ENG-008`'s/`ENG-009`'s
  rather than presenting it as equivalent.

  **Resolved the design's one open question with evidence, not a guess.**
  The design's Interfaces section left "verify which is authoritative at
  build time" between `profiles.name` and `first_name`/`last_name` for
  author-name resolution. Checked `handle_new_user()`
  (`20250729143357_initial_restaurant_rls.sql`): every signup branch
  (influencer, restaurant, and the else-branch admin/staff accounts fall
  into before a role is manually reassigned) inserts `name` from
  `raw_user_meta_data`; none inserts `first_name`/`last_name` at all. Those
  two columns are read elsewhere in this function family
  (`activation.ts`, `foodswipe.ts`, `users.ts`) but nothing in this codebase
  was found populating them for an admin/sub-admin account specifically.
  Implemented `name` as primary, `first_name`/`last_name` as fallback,
  matching the design's literal wording and the stronger evidence, in both
  the new handler's `resolveAuthorNames` and consistently for the POST
  response's own author.

  **Built exactly what the design named, reusing rather than duplicating
  the existing narrower check.** New table (`influencer_notes`, migration
  `20260902120000_create_influencer_notes.sql` — doc above); new handler
  `admin-portal/handlers/influencer-notes.ts` (`GET
  ?influencer_id={id}` list, `POST` create) importing
  `hasInfluencerAdminAccess` from `influencers.ts` rather than
  reimplementing the admin/sub-admin-only check, so the two handlers can
  never drift apart on who's allowed through; `author_id` always taken from
  `auth.user.id`, never the request body (tested explicitly). Routed in
  `index.ts` ahead of the existing `/influencers` branch — the two path
  prefixes don't actually overlap (`"influencer-notes"` is not a substring
  of `"influencers"`), but the ordering is defensive and cheap, matching
  this router's own existing ordering discipline for the unrelated
  `activity` sub-route. Frontend: `src/pages/Influencers.tsx` gains a Notes
  block in the existing detail dialog (chronological list, author +
  timestamp, add-note form), fetched per-influencer on dialog open
  (`fetchNotes`, mirroring `ENG-009`'s own `fetchActivity` lazy-fetch
  pattern) rather than preloaded for the whole list. No PATCH/DELETE
  anywhere, matching the PRD's strictly-accumulate-only requirement.

  **Found and fixed a real gap while touching this function, not a new
  one this ticket introduced.** `aiorders-api/CLAUDE.md` requires updating
  `supabase/functions/README.md`'s entry for a function "in the same
  commit" whenever it changes. `admin-portal`'s own entry never documented
  the `influencers`/`influencers/activity` routes `ENG-008`/`ENG-009` added
  — confirmed absent, not misremembered. Since this ticket is already
  changing `admin-portal` and already has full, current knowledge of what's
  missing, brought the whole entry up to date in one edit (routes, DB
  tables, and a Notes line on the narrower role check) rather than adding
  only this ticket's own route and leaving the pre-existing gap for a
  future pass to rediscover. Filed as an observation, not a proposal —
  already fixed, nothing left to decide.

  **Step 6b artifact-enumeration grep run before closing this hop.** Grepped
  `influencer_notes`, `influencer-notes`, `handleInfluencerNotes`, and
  `resolveAuthorNames` across `instances/`/`departments/`: every hit is this
  ticket's own design doc, its G1, its board file, or the migration doc just
  written this pass — no other department *instruction* or *map* file
  assumes a different shape, so nothing else needed fixing.

  **Self-tested, both repos.** `aiorders-api`: `deno check` on the new
  handler and test file — clean. `deno test influencer-notes.test.ts` —
  **16 passed, 0 failed**, including the explicit `role: 'influencer'`
  negative-authorization case (AC4) and the author-id-from-session case.
  `deno test influencers.test.ts` (unaffected sibling) — still **34 passed,
  0 failed**. Whole-tree `deno check handlers/*.ts` — 17 errors, matching
  the exact count every prior ticket on this board has recorded, all in
  `auth.ts`/`partners.ts`/`users.ts`; confirmed zero in
  `influencer-notes.ts` or `influencers.ts`. `aiorders-admin-hub`: `npm run
  lint` — 150 pre-existing errors (unchanged count), 31 warnings; grepped
  for `Influencers.tsx` specifically — the same one pre-existing
  `react-hooks/exhaustive-deps` warning every prior pass on this file
  recorded, zero new. `npm run build` — clean, same pre-existing chunk-size
  notice as every other ticket on this board.

  **Database migration doc written**
  (`agents/database/migrations/ENG-010-influencer-relationship-notes.md`) —
  static verification only (no MCP this pass, see above), gate verdict
  **pass**, evidence narrower than precedent and said so explicitly rather
  than dressed up as equivalent.

  **Both branches committed and pushed**
  (`aiorders-api@d79d963`, `aiorders-admin-hub@f7d8fd7`, both based on
  `ENG-009`'s still-unmerged tip); no PR opened yet — devops's release step,
  same as `ENG-008`/`ENG-009`. PR bodies drafted here:

  *aiorders-api* — title: `Add staff relationship notes for influencers
  (ENG-010)`. Body: new, isolated `influencer_notes` table (FK into
  `influencers`/`profiles`, no edit/delete path); new `GET
  admin-portal/influencer-notes?influencer_id={id}` (list, newest first,
  resolved author name) and `POST admin-portal/influencer-notes` (create;
  `author_id` always from the session), both admin/sub-admin gated via the
  same `hasInfluencerAdminAccess` check `ENG-008`/`ENG-009` established.
  Also brings `supabase/functions/README.md`'s `admin-portal` entry up to
  date (previously missing the `influencers` routes entirely). Depends on
  `ENG-009`'s branch (based off it, not `main`). Migration doc:
  `agents/database/migrations/ENG-010-influencer-relationship-notes.md`.

  *aiorders-admin-hub* — title: `Add staff notes section to influencer
  detail dialog (ENG-010)`. Body: adds a Notes block to the existing
  detail dialog — chronological list (author + timestamp) plus an add-note
  form, sourced from the new `aiorders-api` endpoints above, fetched
  per-influencer when the dialog opens. Depends on `ENG-009`'s branch
  (based off it, not `main`).

  **1 transition** (`ready → building`; the build itself happened inside
  it), well under the cap of 4 — the next hop (review + quality, combined)
  is a fresh session's work by design, same as every other ticket at this
  state on this board. **Consequence:** machine WIP unaffected — `building`
  is still inside the counted `ready`..`ready-to-ship` range, so the slot
  `ENG-010` already held is unchanged (1/1). Approver-facing WIP and cap
  both unaffected — no gate touched this hop.

  **Dead-end sweep (scoped to this event):** no other ticket touched.
  **Notify sweep:** nothing raised this pass (no gate item — a build hop
  doesn't notify); nothing to nudge. **Observations filed**
  (`observations.md`): the missing-MCP-tool finding and the
  README-documentation-gap finding, both above.

  `chained: ENG-010` — ticket sits at `building`, agent-owned (the build
  itself is done; the next hop is code review + quality, combined, per this
  loop's own design for why that isn't done in the same session) — not the
  approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-010`) and whole-board: see board index.

- `2026-09-02` **code review round 1: FAIL — a stale-response race can
  display one influencer's notes under a different influencer's open
  dialog** (principal-engineer, `continue` event pass, context `ENG-010` —
  the chain fired by the 16:02 build hop above). Narrow scope per the
  event's own contract (resume this ticket only; no board-wide sweep). Mode
  check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty, falls through). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines. Ticket hop count
  (`traces/.hops-2026-09-02-ENG-010`) at 2 coming in, well inside the
  per-ticket ceiling.

  **Re-derived the diff from disk rather than trusting the build hop's own
  account, against this ticket's actual base rather than `main`** (per
  `ENG-009`'s own round-1 precedent on this identical class of check). Both
  worktrees fetched, confirmed clean, at the commits this ticket's own
  frontmatter records (`aiorders-api@d79d963`, `aiorders-admin-hub@f7d8fd7`).
  `git merge-base --is-ancestor origin/feat/ENG-009-influencer-engagement-info
  {this branch}` → true on both repos, and `git merge-base` returns exactly
  `ENG-009`'s own current tip on both — so, unlike `ENG-009`'s own round 1,
  the sibling this ticket branched from has not moved since, and the diff
  reviewed (`d37e0c9..d79d963`, `92bcacd..f7d8fd7`) is exactly and only what
  `ENG-010` itself added.

  **Automatic-failure scan** (`engineering-standards.md`), fresh against
  this diff:

  | # | Check | Result |
  |---|---|---|
  | 1 | Secret/credential/token/key committed | Clean |
  | 2 | Silent exception swallow | Clean — both new backend catches `console.error` before returning 500; the frontend write path surfaces a toast on failure |
  | 3 | Missing test on a bug fix | N/a — feature ticket |
  | 4 | `any`/untyped public interface, undocumented | Clean, not a new instance. `resolveAuthorNames(adminSupabase: any, ...)`'s parameter is the extraction of an already-`any`-typed value (`AuthenticatedRequest.adminSupabase`, imported unchanged from `influencers.ts`), not a fresh untyped surface — same call this notebook's `ENG-013` entry already made for `hasFoodswipeAccess(userProfile: any)`. Every sibling handler in this directory (`auth.ts`, `billing.ts`, `brands.ts`, `activation.ts`, `foodswipe.ts`, `partners.ts`) types its own client/body params `any` the same way; matching that, not `users.ts`'s lone typed exception, reads like the code actually around it |
  | 5 | Unbounded query / missing pagination | Clean — `influencer_notes` is queried scoped to one `influencer_id`, not a cross-entity scan; no realistic per-influencer note volume approaches the concern the board's accepted `influencer_invitations`/`getAllBrands` precedents are about |
  | 6 | New dependency | Clean |
  | 7 | Unrelated refactor bundled in | Clean — the `supabase/functions/README.md` edit is required by `aiorders-api/CLAUDE.md` ("Update that function's entry ... in the same commit," line 16), and the gap it closes is real: `git show d37e0c9:supabase/functions/README.md` confirms the `admin-portal` entry never mentioned the `influencers`/`influencer-notes` routes at all before this commit. Required documentation, not a drive-by |
  | 8 | Commented-out code / unowned `TODO` | Clean |
  | 9 | Datastore write bypassing the data layer | N/a — `auth.adminSupabase` used directly, matching this handler family's own house style |
  | 10 | Auth/payment/deletion path changed, no failure-case test | Clean — both new routes carry an explicit `role: 'influencer'` 403 test, the exact case this ticket's own G1 named as the one it can't get wrong |

  **0/10 automatic failures. This round fails on a correctness finding
  outside that list** — `code-review-gate/SKILL.md` step 5 (concurrency,
  ordering assumptions), "the step most reviews skip and most bugs live
  in."

  **The finding.** `src/pages/Influencers.tsx`'s new `fetchNotes` (line 147)
  and `handleAddNote` (line 167) each apply their async result
  unconditionally — `if (payload?.data) setNotes(payload.data)` (line 159)
  and `setNotes(prev => [payload.data, ...prev])` (line 189) — with no check
  that the response just received is still for the influencer currently
  open. Every row renders its own uncontrolled `<Dialog>` (confirmed by
  reading the JSX: no shared controlled `open`/`onOpenChange`), all sharing
  the one `Influencers` page component's state, which never unmounts
  between selections. So: staff opens influencer A's dialog (`fetchNotes('A')`
  starts) → closes it and opens influencer B's (`openInfluencer`, line 208,
  resets `setNotes([])` then starts `fetchNotes('B')`) → if A's response
  lands after B's, `setNotes(A's data)` overwrites the screen with A's notes
  while B's dialog is what's on screen, under B's name. The same shape
  applies to `handleAddNote`: nothing stops closing A's dialog and opening
  B's while A's `POST` is still in flight, so a landing response can prepend
  A's just-written note onto whatever list is currently rendered for B. No
  exotic timing is needed — an ordinary network round-trip is enough if
  staff click through a couple of influencers quickly, which is exactly this
  feature's own stated workflow ("more easily use these influencers for our
  restaurant campaigns").

  **Why it matters.** Server-side the note is written against the correct
  `influencer_id` either way (`selectedInfluencer.id` is read synchronously
  at click time) — this is not the influencer-visibility risk the PRD names
  as the one thing this ticket can't get wrong, and it is not a P0. But the
  entire point of this feature is that a staff member acts on the notes
  they're looking at; a UI that can silently attribute influencer A's
  personality/preference notes to influencer B, with no error and no visual
  indication anything went wrong, produces exactly the "influencer gets
  mishandled" the PRD's own Problem statement was written to fix — arguably
  worse than the no-notes status quo, since a wrong note reads as
  authoritative. No test catches this: backend tests are the only
  automation this project has, and there is no frontend harness on this
  repo at all (a standing gap, already a proposal — see below). Review is
  the only gate that could have caught it.

  **The fix**, small and mechanical, no new infrastructure needed: compare
  the id the response is *for* against the currently-selected influencer
  before applying it — e.g. `if (payload?.data && selectedInfluencer?.id
  === influencerId) setNotes(payload.data)` in `fetchNotes`, and the
  equivalent guard on `handleAddNote`'s own success branch (capture the
  target id at call time, compare before the `setNotes(prev => ...)`
  prepend). An `AbortController` would also work but isn't necessary for a
  fix this contained, and nothing elsewhere in this codebase already
  establishes that pattern to match instead.

  **Also found this round, secondary, would not have blocked alone:**
  - `fetchNotes`'s own catch block only `console.error`s — a failed notes
    load renders as "No notes yet." (line 700), indistinguishable from an
    influencer that genuinely has none. Same class of gap `ENG-009`'s own
    accepted `fetchActivity` failure-isolation already carries on this file
    (degrade without blanking the page, no user-facing error) — not new,
    not blocking, named so QA's eventual test-plan coverage note doesn't
    silently repeat it as a fresh finding later.
  - `resolveAuthorNames`'s `row.name || [row.first_name, row.last_name]...`
    fallback treats a present-but-empty-string `name` the same as null —
    matches the design's literal wording and has no live counter-evidence
    (`handle_new_user` always inserts a non-empty `raw_user_meta_data` name
    or none at all) — not a real gap, named only so the next reader doesn't
    re-open the same question.

  **Verification reproduced this review, not taken on the build hop's
  word:** `deno check` on `influencer-notes.ts`/`influencer-notes.test.ts`:
  clean. `deno test --allow-net influencer-notes.test.ts`: **16 passed, 0
  failed** (`deno` 2.9.6). `deno test influencers.test.ts` (unaffected
  sibling): **34 passed, 0 failed**. Whole-tree `deno check handlers/*.ts`:
  **17 errors**, same count and same three pre-existing files
  (`auth.ts`/`partners.ts`/`users.ts`) every prior ticket on this board has
  recorded, zero in either file this ticket touched. `npm run lint`
  (`aiorders-admin-hub`): **150 errors / 31 warnings**, unchanged baseline;
  `Influencers.tsx` specifically carries exactly its one pre-existing
  `react-hooks/exhaustive-deps` warning (line 206), zero new. `npm run
  build`: clean, 3340 modules, same pre-existing chunk-size notice. Also
  independently checked two claims this diff's own comments make rather
  than trusting them: the router-ordering comment's substring-non-overlap
  claim (`"influencer-notes"` contains no `"influencers"` substring and vice
  versa — confirmed character-by-character, true either order) and the
  `influencer-invitations.ts` "fetch separately, map by id" precedent
  citation (confirmed present and matching,
  `restaurant-influencer-campaigns/handlers/influencer-invitations.ts:93-110`,
  same `Set` → `.in()` → `Map` shape `resolveAuthorNames` uses).

  **No open P0/P1 bug** (`agents/qa/bugs/_index.md`: one open item,
  `BUG-001`, `P2`, unrelated project area) — not the reason for this
  verdict, checked for completeness before QA's own hop was skipped.

  **No receipt written** (`agents/principal-engineer/reviews/ENG-010.md`
  stays absent — `code-review-gate/SKILL.md` step 8) and **QA's hop not run
  this round** — discarded per the combined-hop design, same precedent
  `ENG-009`'s own round-1 fail set on this board; no
  `agents/qa/test-plans/ENG-010.md` written either.

  **Observation filed** (`observations.md`): a second concrete data point
  for the standing `aiorders-admin-hub`-has-no-frontend-test-harness
  proposal (`proposals.md`, 2026-08-31) — this round's own finding is
  exactly the category of bug that proposal argues ships unguarded on this
  repo today.

  **Time tracking.** `time_estimate`/`time_spent`/`time_remaining` had never
  been populated on this ticket (a gap from its own `ready → building`
  entry, which didn't itemize hours) — added in this edit rather than
  carried forward blank, per `definition-of-done.md`'s time-tracking rule
  ("or back in it after a review round"). Backfilling an exact figure for
  the build hop itself would be inventing precision that pass didn't
  record; named as a gap instead of guessed.

  **0 net transitions** — `state`/`owner` unchanged (`building`/
  `eng-manager`), same precedent `ENG-008`'s and `ENG-009`'s own round-1
  fails set on this board: a review failure routes back to `building`
  without a persisted `in-review` frontmatter state. `machine_wip`
  unaffected (still 1/1, `ENG-010` the sole occupant). No approver-facing or
  approval-cap change — a review failure is not an approver-facing gate.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume — this finding *is* this pass's dead-end-sweep
  result. **Notify sweep:** nothing to raise (a review failure isn't a gate
  item to the approver); nothing to nudge.

  `chained: ENG-010` — `building` is agent-owned (the fix above is the next
  hop's work, a fresh frontend session per this loop's own design), not the
  approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-010`) and whole-board: see board index.

- `2026-09-02` **fix hop — round 1's stale-response race closed** (the fixing
  engineer, `continue` event pass, context `ENG-010` — the chain fired by the
  round-1-FAIL pass above). Narrow scope per this event's own contract (this
  ticket only; no board-wide sweep). Mode check clean (business-os `.env` →
  `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:` lines.
  Ticket hop count (`traces/.hops-2026-09-02-ENG-010`) at 3 coming in, well
  inside the per-ticket ceiling. `aiorders-admin-hub` worktree fetched,
  confirmed clean and at `f7d8fd7` (matching this ticket's own frontmatter)
  before touching anything; `aiorders-api` untouched this hop — the finding
  was frontend-only, so its own worktree was not re-verified.

  **Did not implement round 1's own example line verbatim, and named why.**
  The finding's suggested fix read `if (payload?.data && selectedInfluencer?.id
  === influencerId) setNotes(payload.data)`. Traced the actual timing before
  writing anything: `fetchNotes`/`handleAddNote` are plain `const` closures
  redefined every render, and `openInfluencer` calls `fetchNotes(influencer.id)`
  synchronously in the same event-handler tick as `setSelectedInfluencer`,
  before React applies that update — so the `selectedInfluencer` a given
  `fetchNotes` call closes over is always the *previous* selection, never the
  one it was just invoked for. Implementing the suggested line verbatim would
  have made the id comparison fail on every normal open, not just the race
  (`selectedInfluencer` would read `null`/the prior influencer while
  `influencerId` is the new target) — a regression disguised as the fix. Used
  a `useRef<string | null>`, set synchronously inside `openInfluencer` at
  click time instead: a ref's `.current` is read live regardless of which
  render's closure is doing the reading, so it correctly reflects "whichever
  influencer is currently open" at the moment each async response lands. Same
  intent the finding asked for ("compare the id the response is for against
  the currently-selected influencer"), correct mechanism for React's
  render-timing model.

  **The fix, `src/pages/Influencers.tsx` only:**
  - New `selectedInfluencerIdRef` (`useRef<string | null>(null)`), added to
    the existing `react` import rather than a new dependency, matching the
    finding's own "no new infrastructure needed."
  - `openInfluencer` sets `selectedInfluencerIdRef.current = influencer.id`
    synchronously, before `setSelectedInfluencer` — the one write that keeps
    the ref truthful.
  - `fetchNotes`: `setNotes(payload.data)` now gated on
    `selectedInfluencerIdRef.current === influencerId` (the argument it was
    called with), closing the finding's primary case.
  - `handleAddNote`: captures `targetInfluencerId = selectedInfluencer.id`
    before the first `await` (this closure's own `selectedInfluencer` read
    *is* correct at call time — it's bound to whichever dialog's "Add Note"
    button was actually clicked, not a second, different argument the way
    `fetchNotes` has), then gates the success branch (`setNotes` prepend
    *and* `setNewNoteBody('')`) on `selectedInfluencerIdRef.current ===
    targetInfluencerId`. Clearing the input was included in the guard, not
    just the prepend — a stale add-note response completing after staff
    switched dialogs must not wipe out whatever they've since started typing
    for the influencer now open, a second failure mode the finding didn't
    spell out but the same race produces.
  - Deliberately left unguarded: `notesLoading`/`savingNote`. A stale
    response can still flip these to `false` slightly early, a minor spinner
    flicker — not the silent-wrong-data failure the finding named, and out
    of this hop's scope (`minimal_scope`: fix what was asked, not every
    theoretical timing edge the same shared state could produce).

  **No test added** — `aiorders-admin-hub` has no frontend test harness at
  all, the standing gap round 1's own entry already logged a second data
  point for (`proposals.md`, 2026-08-31); a third data point isn't filed
  again here since it would just repeat the same open proposal. Verification
  is lint/build plus the render-timing trace above, not an automated
  regression test.

  **Self-tested.** `npm run lint`: **150 errors / 31 warnings**, unchanged
  baseline; `Influencers.tsx` carries exactly its one pre-existing
  `react-hooks/exhaustive-deps` warning (now line 211, shifted by the added
  lines, not new — confirmed by reading the surrounding line, still the
  mount `useEffect`), zero new. `npm run build`: clean, 3340 modules, same
  pre-existing chunk-size notice as every other ticket on this board.
  `aiorders-api` not re-run — untouched this hop, round 1's own backend
  verification (16/16, 34/34, 17 pre-existing `deno check` errors) still
  stands unchanged.

  **No new artifact or cross-file rule introduced this hop** — step 6b's
  enumeration is for a change that writes or relies on a rule about an
  artifact; this hop only touches existing state inside one component's own
  closures, nothing another file or department instruction assumes a shape
  for. Nothing to enumerate.

  Committed `aiorders-admin-hub@8b90f0e` ("Fix stale-response race in
  influencer notes dialog (ENG-010)"), pushed to the existing branch (no
  rebase needed — `ENG-009`'s tip this branch was built on has not moved).
  `time_spent`/`time_remaining` updated in frontmatter in the same edit as
  this entry.

  **0 net transitions** — `state`/`owner` unchanged (`building`/
  `eng-manager`); the next transition (`building → in-review`) is the review
  + quality hop's own write, not this one's. `machine_wip` unaffected (still
  1/1, `ENG-010` the sole occupant). No approver-facing or approval-cap
  change.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume — the fix round 1 asked for is this pass's entire
  result. **Notify sweep:** nothing to raise (a fix hop doesn't notify);
  nothing to nudge. **1 observation filed** (`observations.md`): a review
  finding's own suggested example fix can carry the same class of bug it's
  fixing when the example touches async-closure timing — worth a second
  look before pasting, not just before trusting the diagnosis.

  `chained: ENG-010` — `building` is agent-owned (review + quality round 2 is
  the next hop's work, a fresh session per this loop's own design), not the
  approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

  **Checked the fire's actual outcome rather than assuming "fired" meant
  "launched."** `traces/eng-loop-2026-09-02.log` tail: `lock is 3934s old but
  PID 17776 is alive — not stealing`, then `continue — pass in flight, queued
  as pending`. `ps -p 17776` confirms it's still running:
  `/bin/zsh .../eng-trigger.sh scheduled launchd`, elapsed `01:07:34` — the
  15:30 `scheduled` sweep's own orchestrating process, which is what launched
  this very fix-hop session as its claude subprocess and has held the
  single-flight lock the whole time since. `traces/.pending` confirms the
  event landed rather than dropped: `1 continue ENG-010`. Not a broken chain
  — the queued event is drained by "the next fire of any kind" per this
  loop's own design, and the most likely next fire is that same
  still-running orchestrating process checking `.pending` again once this
  session exits and returns control to it. No manual re-fire attempted: doing
  so would race the single-flight lock this mechanism exists to respect.

- `2026-09-02` **code review round 2: FAIL — the new table has no row-level
  security, so the risk this ticket names as the one thing it cannot get
  wrong is still open through a path the edge-function check never
  touches** (principal-engineer, `continue` event pass, context `ENG-010` —
  the chain fired by the fix-hop pass above). Narrow scope per the event's
  own contract (resume this ticket only; no board-wide sweep). Mode check
  clean (business-os `.env` → `MODE=active`; instance `config/config.yaml`
  → `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:`
  lines. Ticket hop count (`traces/.hops-2026-09-02-ENG-010`) at 4 coming
  in, well inside the `max_5x` tier's 20/ticket ceiling.

  **Re-derived both diffs from disk rather than trusting the fix hop's own
  account.** Both worktrees fetched, confirmed clean, at the commits this
  ticket's own frontmatter records (`aiorders-api@d79d963`,
  `aiorders-admin-hub@8b90f0e`). `git merge-base --is-ancestor
  origin/feat/ENG-009-influencer-engagement-info {this branch}` → true on
  both repos, and `git merge-base` returns exactly `ENG-009`'s own current
  tip (`d37e0c9`/`92bcacd`, both unchanged since round 1) on both — the
  sibling this ticket depends on still hasn't moved, so the diff reviewed
  (`d37e0c9..d79d963`, `92bcacd..8b90f0e`) is exactly and only what
  `ENG-010` itself has ever added.

  **Automatic-failure scan** (`engineering-standards.md`), fresh against
  this diff:

  | # | Check | Result |
  |---|---|---|
  | 1 | Secret/credential/token/key committed | Clean |
  | 2 | Silent exception swallow | Clean — unchanged from round 1 |
  | 3 | Missing test on a bug fix | N/a — feature ticket. Round 1's own frontend fix added no test, but that was already reasoned through and accepted at the fix hop (no test harness exists on this repo, standing proposal); not relitigated here |
  | 4 | `any`/untyped public interface, undocumented | Clean, not a new instance — same reasoning round 1 already recorded for `resolveAuthorNames` |
  | 5 | Unbounded query / missing pagination | Clean — same accepted class as round 1 (`influencer_notes` scoped to one `influencer_id`, no cross-entity scan) |
  | 6 | New dependency | Clean — `Textarea` (`src/components/ui/textarea.tsx`) is pre-existing, from this project's original shadcn scaffold, not new this ticket |
  | 7 | Unrelated refactor bundled in | Clean — same `README.md` reasoning as round 1 |
  | 8 | Commented-out code / unowned `TODO` | Clean |
  | 9 | Datastore write bypassing the data layer | N/a — same house style as round 1 |
  | 10 | Auth/payment/deletion path changed, no failure-case test | **This is where the real finding lives, not outside the list this time.** A failure-case test exists (`rejects the influencer's own role with 403`) and passes — but it calls `handleInfluencerNotes` directly, so it can only prove the *handler* rejects that role. It cannot and does not prove the *table* rejects a request that never reaches the handler. See below |

  **0/10 strictly "automatic," but item 10's own test doesn't cover the
  actual attack surface — this round fails on that gap, not on a fresh
  correctness finding outside the list the way round 1 did.**

  **The finding.**
  `supabase/migrations/20260902120000_create_influencer_notes.sql` creates
  `influencer_notes` with no `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
  and no policy. `admin-portal/handlers/influencer-notes.ts` only ever
  touches this table through `auth.adminSupabase`, and
  `admin-portal/index.ts:51-58` constructs that client with
  `SUPABASE_SERVICE_ROLE_KEY` — a role that bypasses RLS by definition —
  so the handler's own `hasInfluencerAdminAccess` check (confirmed at
  `influencers.ts:27-33`: `role` or `additional_roles`, `admin`/`sub-admin`
  only) and the router's `authenticate()` allowlist beneath it are the
  *only* gate on this data, and both gate exactly one call path into it.
  Supabase exposes every `public`-schema table over PostgREST by default,
  and this is not a hypothetical for this codebase: `src/pages/
  Influencers.tsx:102`, the very file this ticket modifies, already calls
  `supabase.from('influencers').select('*')` directly from the browser
  using the project's public anon key, for the sibling table — live,
  present-tense proof that a client bypassing the edge function entirely
  and hitting the table directly is a real, already-used access pattern on
  this project, not a theoretical one invented for this review. Nothing at
  the database layer distinguishes `influencer_notes` from `influencers`:
  the same request shape, with an influencer's own valid session JWT
  instead of a staff member's, reaches the table either way.

  **Why it matters.** This ticket's own PRD names exactly one thing it
  cannot get wrong: an influencer reading staff commentary about
  themselves. That failure is reachable today, on this branch, without
  going anywhere near the code this review and round 1's review both
  checked carefully — it requires only a direct PostgREST call, which this
  admin panel's own codebase already demonstrates is a normal way to reach
  these tables. The new negative-authorization test doesn't catch it
  because it was never able to: a unit test that calls a handler function
  directly cannot observe a request that skips the handler. The database
  migration gate's own verdict (`agents/database/migrations/
  ENG-010-influencer-relationship-notes.md`) reads "no change to any
  existing table, column, or RLS policy" — true in the narrow sense that a
  table which never had a policy still doesn't have one, but the table is
  brand new, so "unchanged" reads as reassurance where none was earned.
  Not a P0: nothing has merged or deployed, this sits on an unreviewed
  branch with no open PR, which is exactly what this gate exists to catch
  before either happens.

  **The fix, and it's already sitting in this same codebase, unused.**
  `supabase/migrations/20250926000000_proxy_sessions_audit_logs.sql`
  creates `proxy_sessions` — an existing admin-only table, same shape:
  foreign keys into `profiles`/`auth.users`, read and written only through
  the service-role client — and pairs `ALTER TABLE ... ENABLE ROW LEVEL
  SECURITY` with a policy scoped to `profiles.role IN ('admin',
  'sub-admin')`, the identical boundary this ticket's own handler already
  enforces in application code. Add the same two statements to this
  ticket's migration before it merges:
  ```sql
  alter table influencer_notes enable row level security;

  create policy "Admins can manage influencer notes"
  on influencer_notes
  for all
  using (exists (
    select 1 from public.profiles
    where id = auth.uid() and role in ('admin', 'sub-admin')
  ))
  with check (exists (
    select 1 from public.profiles
    where id = auth.uid() and role in ('admin', 'sub-admin')
  ));
  ```
  This changes nothing about how the shipped feature behaves — the
  handler's own client bypasses RLS regardless of whether it's enabled —
  it only closes the direct path nothing else in this design considered.

  **Round 1's own fix, re-verified rather than re-trusted.** Read
  `selectedInfluencerIdRef`'s full lifecycle in the current diff: set
  synchronously in `openInfluencer` before `setSelectedInfluencer` runs,
  compared against the call's own target id in both `fetchNotes`'s and
  `handleAddNote`'s success branches before either applies a response.
  Traced both call sites by hand against the race round 1 described —
  correct and complete; this round's finding is unrelated to it and does
  not reopen it.

  **No open P0/P1 bug** (`agents/qa/bugs/_index.md`: one open item,
  `BUG-001`, `P2`, unrelated project area) — not the reason for this
  verdict, checked for completeness before QA's own hop was skipped.

  **Verified independently, not taken on any prior hop's word:** `deno
  check` on `influencer-notes.ts`/`influencer-notes.test.ts`: clean. `deno
  test --allow-net influencer-notes.test.ts`: **16 passed, 0 failed**
  (`deno` 2.9.6). `deno test influencers.test.ts` (unaffected sibling):
  **34 passed, 0 failed**. Whole-tree `deno check handlers/*.ts`: **17
  errors**, same count and same three pre-existing files
  (`auth.ts`/`partners.ts`/`users.ts`) every prior ticket on this board has
  recorded, zero in either file this ticket touches. `npm run lint`
  (`aiorders-admin-hub`): **150 errors / 31 warnings**, unchanged baseline;
  `Influencers.tsx` carries exactly its one pre-existing
  `react-hooks/exhaustive-deps` warning, zero new. `npm run build`: clean,
  same pre-existing chunk-size notice. All numbers match the fix hop's own
  account exactly. Also independently confirmed rather than assumed:
  `hasInfluencerAdminAccess`'s actual body (`influencers.ts:27-33`), and
  `adminSupabase`'s construction with `SUPABASE_SERVICE_ROLE_KEY`
  (`admin-portal/index.ts:51-58`) — the fact the RLS finding turns on.

  **No receipt written** (`agents/principal-engineer/reviews/ENG-010.md`
  stays absent — `code-review-gate/SKILL.md` step 8) and **QA's hop not
  run this round** — discarded per the combined-hop design, same
  precedent this ticket's own round 1 and `ENG-009`'s round 1 both set; no
  `agents/qa/test-plans/ENG-010.md` written either.

  **Observation filed** (`observations.md`): the general pattern — a
  brand-new table whose only reader uses a service-role client had no RLS,
  and neither the design, the database migration gate, nor round 1's
  review asked the question, despite an exact working precedent
  (`proxy_sessions`) already in the same repo. First occurrence on this
  board; not promoted to `engineering-standards.md`'s automatic-failure
  list off one instance.

  **Time tracking** updated in frontmatter in this same edit
  (`time_spent`/`time_remaining`).

  **0 net transitions** — `state`/`owner` unchanged (`building`/
  `eng-manager`), same precedent every review-round fail on this board has
  set: a review failure routes back to `building` without a persisted
  `in-review` frontmatter state. `machine_wip` unaffected (still 1/1,
  `ENG-010` the sole occupant). No approver-facing or approval-cap
  change — a review failure is not an approver-facing gate.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume — this finding *is* this pass's dead-end-sweep
  result. **Notify sweep:** nothing to raise (a review failure isn't a
  gate item to the approver); nothing to nudge.

  `chained: ENG-010` — `building` is agent-owned (the fix above is the
  next hop's work, a fresh session per this loop's own design), not the
  approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
  before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-010`) and whole-board: see board index.

  **Checked the fire's actual outcome, same discipline the fix hop above
  established, rather than assuming this one behaved differently.**
  `traces/eng-loop-2026-09-02.log` tail: `lock is 4910s old but PID 17776 is
  alive — not stealing`, then `continue — pass in flight, queued as
  pending`. `ps -p 17776` confirms the same 15:30 `scheduled launchd`
  orchestrating process is still alive (elapsed `01:22:16` now) — it drained
  the fix hop's own queued event at `16:38:32`, launched this very
  round-2-review session as its claude subprocess, and has held the
  single-flight lock across both without releasing it. `traces/.pending`
  confirms this pass's own fire landed rather than dropped: `1 continue
  ENG-010`. Not a broken chain — the same "next fire of any kind drains the
  oldest queued event" mechanism applies, and the most likely next fire is
  that same orchestrator checking `.pending` again once this session exits.
  No manual re-fire attempted, for the same reason the fix hop gave: it
  would race the single-flight lock this mechanism exists to respect.

- `2026-09-02` **fix hop — round 2's missing-RLS gap closed** (the fixing
  engineer, `continue` event pass, context `ENG-010` — the chain fired by
  the round-2-FAIL pass above, drained once the 15:30 `scheduled` sweep's
  orchestrating process released the single-flight lock: `traces/
  eng-loop-2026-09-02.log` records `draining queued event: continue
  (ENG-010)` then `pass start: continue (ENG-010) [... ENG-010 5/20]`, well
  inside the per-ticket ceiling). Narrow scope per this event's own contract
  (this ticket only; no board-wide sweep). Mode check clean (business-os
  `.env` → `MODE=active`). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines. `aiorders-api`
  worktree fetched, confirmed clean and at `d79d963` (matching this
  ticket's own frontmatter) before touching anything; `aiorders-admin-hub`
  untouched this hop — the finding was migration-only.

  **Applied the fix round 2 named, not a substitute.** Added to
  `supabase/migrations/20260902120000_create_influencer_notes.sql`, after
  the existing `create table`/`create index` statements: `alter table
  influencer_notes enable row level security`, then a `for all` policy
  named `"Admins can manage influencer notes"` scoped to `profiles.role in
  ('admin', 'sub-admin')` for both `using` and `with check` — the exact
  shape the review cited from `supabase/migrations/
  20250926000000_proxy_sessions_audit_logs.sql`, matched to this file's own
  lowercase statement style rather than that precedent's uppercase one (the
  file being edited already established its own convention; the precedent
  is the policy shape, not the casing). This changes nothing about the
  shipped feature's own behavior — the handler's `auth.adminSupabase` client
  still uses the service-role key and still bypasses RLS regardless of
  whether it's enabled — it only closes the direct-PostgREST path the
  original design, the database migration gate, and round 1's review all
  missed.

  **Updated the migration doc's own gate verdict rather than leaving it
  stale.** `agents/database/migrations/
  ENG-010-influencer-relationship-notes.md`'s original verdict read "no
  change to any existing table, column, or RLS policy" — true narrowly (no
  *existing* policy changed) but read as reassurance on a question it never
  actually checked, per the review's own point. Added an Addendum section
  recording the gap, the fix, and that it changes no runtime behavior,
  rather than silently rewriting the original verdict text out from under
  its own history. Did not touch the architect design doc's own illustrative
  SQL snippet (`agents/architect/designs/
  ENG-010-influencer-relationship-notes.md`) — it's a pre-implementation
  sketch, not a producer instruction this fix contradicts, and no other
  ticket on this board has retroactively patched its own design doc for an
  implementation-stage fix; out of this hop's scope
  (`minimal_scope`).

  **No Supabase MCP tool available this session either** — checked via
  `ToolSearch` before concluding, same absence the build hop already filed
  as an observation; not re-filed as a second instance of the identical
  finding, since one data point already stands and this session's own
  absence doesn't confirm a pattern by itself.

  **Verified independently.** `deno check` on
  `influencer-notes.ts`/`influencer-notes.test.ts` (unchanged by this hop,
  re-run for confidence, not because the SQL-only edit could plausibly
  break TypeScript): clean. `deno test --allow-net
  influencer-notes.test.ts`: **16 passed, 0 failed**, matching every prior
  hop's count exactly. `deno test influencers.test.ts` (unaffected
  sibling): **34 passed, 0 failed**. Whole-tree `deno check handlers/*.ts`:
  **17 errors**, same count and same three pre-existing files
  (`auth.ts`/`partners.ts`/`users.ts`) every prior ticket on this board has
  recorded, zero in either file this ticket touches. No live Postgres
  reachable from this host (no `docker`, no `psql`, no `supabase` CLI,
  same standing gap the migration doc already named) — the new `alter
  table`/`create policy` statements have not been executed anywhere, named
  rather than assumed passing. `aiorders-admin-hub` not re-run — untouched
  this hop, round 2's own frontend-adjacent verification (150/31 lint
  baseline, clean build) still stands unchanged.

  Committed `aiorders-api@486eec0` ("Enable RLS on influencer_notes
  (ENG-010)"), pushed to the existing branch (no rebase needed — `ENG-009`'s
  tip this branch was built on has still not moved).
  `time_spent`/`time_remaining` updated in frontmatter in the same edit as
  this entry; `branch:` frontmatter's `aiorders-api` commit hash updated to
  `486eec0`.

  **0 net transitions** — `state`/`owner` unchanged (`building`/
  `eng-manager`); the next transition (`building → in-review`) is the
  review + quality hop's own write, not this one's. `machine_wip`
  unaffected (still 1/1, `ENG-010` the sole occupant). No approver-facing or
  approval-cap change.

  **Dead-end sweep (scoped to this event):** nothing else on this ticket's
  own lineage to resume — the fix round 2 asked for is this pass's entire
  result. **Notify sweep:** nothing to raise (a fix hop doesn't notify);
  nothing to nudge. **No new observation filed** — the missing-RLS pattern
  and the missing-MCP-tool gap were both already filed by the round-2-FAIL
  and build-hop entries respectively; this hop confirmed rather than
  duplicated them.

  `chained: ENG-010` — `building` is agent-owned (review + quality round 3
  is the next hop's work, a fresh session per this loop's own design), not
  the approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
  before exiting. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

  **Checked the fire's actual outcome, same discipline the last two hops
  established, rather than assuming it launched.** `traces/
  eng-loop-2026-09-02.log` tail: `lock is 5346s old but PID 17776 is alive —
  not stealing`, then `continue — pass in flight, queued as pending`.
  `ps -p 17776` confirms the same 15:30 `scheduled launchd` orchestrating
  process is still alive (now ~89 minutes elapsed) — it has held the
  single-flight lock across the build hop, both review rounds, and both fix
  hops without releasing it, launching each as its own claude subprocess in
  turn. `traces/.pending` confirms this pass's own fire landed rather than
  dropped: `1 continue ENG-010`. Not a broken chain — the same "next fire of
  any kind drains the oldest queued event" mechanism applies; the most
  likely next fire is that same orchestrator checking `.pending` again once
  this session exits. No manual re-fire attempted, for the same reason the
  last two hops gave: it would race the single-flight lock this mechanism
  exists to respect.

- `2026-09-02` **code review + quality round 3: PASS — building → in-review →
  in-qa** (principal-engineer then qa, `continue` event pass, context
  `ENG-010` — the chain fired by fix-hop-2 above). **Confirmed this session
  actually is the queued fire, not a second concurrent one, by walking its
  own process ancestry** rather than assuming: this shell's parent chain
  resolves `claude` → `run-claude.sh` (wrapped in `timeout 3600`) →
  `eng-trigger.sh continue ENG-010` → `eng-trigger.sh scheduled launchd`
  (`17776`, the same PID every hop this evening has cited as the
  single-flight-lock holder) → `eng-loop-all.sh scheduled launchd` →
  `launchd` — one continuous lineage, not two independent invocations of the
  same prompt. Narrow scope per the event's own contract (this ticket only;
  no board-wide sweep). Mode check clean (business-os `.env` →
  `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:`
  lines. Ticket hop count (`traces/.hops-2026-09-02-ENG-010`) at 6 coming
  in, well inside the `max_5x` tier's 20/ticket ceiling.

  **Re-derived the full cumulative diff from disk**, not just the delta
  since round 2 — a fix hop can introduce as easily as it closes. Both
  worktrees (`aiorders-api@486eec0`, `aiorders-admin-hub@8b90f0e`) fetched,
  confirmed clean, matching this ticket's own frontmatter exactly.
  `git merge-base --is-ancestor origin/feat/ENG-009-influencer-engagement-info
  {branch}` → true on both repos, merge-base unchanged at `ENG-009`'s own
  tip (`d37e0c9`/`92bcacd`) — the diff reviewed is exactly and only what
  `ENG-010` has ever added, across all three of its own commits.

  **Both prior fixes re-verified independently, not re-trusted from the
  log.** Round 1's `selectedInfluencerIdRef` guard traced through its whole
  lifecycle in the current diff — set synchronously in `openInfluencer`
  before `setSelectedInfluencer`, compared in both `fetchNotes`'s and
  `handleAddNote`'s success branches before applying a response — correct
  and complete. Round 2's RLS policy compared character-by-character
  against `proxy_sessions_audit_logs`'s own policy (same `EXISTS (SELECT 1
  FROM public.profiles WHERE id = auth.uid() AND role IN (...))` shape,
  casing only differs), then checked one level deeper than either prior
  round did: grepped `20250729143357_initial_restaurant_rls.sql`, this
  project's *foundational* RLS migration, and found the identical pattern
  already gating `restaurants` and `catering` — this is the codebase's own
  established house pattern for admin-only RLS, not a precedent being
  copied a second time on faith.

  **Automatic-failure scan: 0/10**, re-run fresh against the full
  cumulative diff. **A fresh scan for new issues, not carried forward from
  either prior round**, found: one pre-existing, codebase-wide gap worth
  naming but not blocking (the new RLS policy checks `profiles.role` only,
  not `additional_roles`, same as every other admin-gated RLS policy in
  this repo — grepped `additional_roles` across every migration in the
  repo, zero hits anywhere, so this isn't a gap this ticket introduced);
  two minor UX gaps in the same already-accepted class round 1 named and
  explicitly scoped out (`fetchNotes`'s `!response.ok` branch degrades one
  step more silently than its own catch block; `handleAddNote`'s error
  toast isn't scoped to the influencer that actually failed). Also checked
  and ruled out as pre-existing rather than this ticket's own: both new
  handlers' `error.message`-in-500-body pattern (matches a dozen+ existing
  files in this directory, already tracked as a non-blocking three-strike
  proposal at `agents/principal-engineer/notebook/
  2026-09-02-security-proposal-verbose-error-response.md` — named here for
  security's own eventual count at this ticket's own security gate, not
  re-filed as a new proposal); `req.json()` parsing inside the outer `try`
  (matches every other body-parsing handler in this directory);
  `deno check` failing on `index.ts` directly (confirmed via a disposable
  worktree at the pre-`ENG-010` base commit, removed immediately after,
  that this is a pre-existing environment condition on the file's
  pre-existing line-2 npm import, unrelated to this ticket's 8-line
  addition — main worktree confirmed unaffected afterward). None of the
  above rise to a third fail. Full reasoning for each:
  `agents/principal-engineer/reviews/ENG-010.md`.

  **Design and PRD conformance** — all 4 acceptance criteria covered:
  author identity + timestamp on write; newest-first list with author and
  timestamp on read; structurally accumulate-only (no PATCH/DELETE route
  or column exists to violate it, not merely a convention); the
  influencer-role rejection now closed at both the handler and, as of
  round 2's fix, the database layer. No divergence from the design's
  stated approach or non-goals.

  **Verified independently, not taken on any prior hop's word:** `deno
  check` on `influencer-notes.ts`/`influencer-notes.test.ts`: clean. `deno
  test --allow-net influencer-notes.test.ts`: **16 passed, 0 failed**.
  `deno test influencers.test.ts` (sibling): **34 passed, 0 failed**.
  Whole-tree `deno check handlers/*.ts`: **17 errors**, same three
  pre-existing files every prior round on this ticket has recorded, zero
  new. `npm run lint` (`aiorders-admin-hub`): **150 errors / 31 warnings**,
  unchanged baseline, `Influencers.tsx` one pre-existing warning, zero new.
  `npm run build`: clean, 3340 modules, same pre-existing chunk-size
  notice. Every number matches every prior hop's own claim exactly.

  **Receipts written** (first receipts on this ticket — rounds 1 and 2
  wrote none, per the pass-verdict-only rule):
  `agents/principal-engineer/reviews/ENG-010.md` (verdict `pass`, round 3)
  and `agents/qa/test-plans/ENG-010.md` (all 4 ACs covered, failure-path
  table, real suite numbers). `links.review` / `links.test_plan` set on the
  ticket in the same edit as this entry. QA's quality gate: suite green on
  both repos, every acceptance criterion covered, no open P0/P1 bug
  anywhere on this board (`agents/qa/bugs/_index.md`: only `BUG-001`, P2,
  unrelated project area) — gate passes. Appended to
  `agents/principal-engineer/notebook/2026-09-02-review-log.md` under this
  ticket's existing section.

  **2 transitions** (`building → in-review → in-qa`, both in this combined
  hop per this loop's own design), within the cap of 4. **Consequence:**
  machine WIP unaffected — `in-qa` is still inside the counted
  `ready`..`ready-to-ship` range, so `ENG-010`'s slot is unchanged (1/1).
  Approver-facing WIP and cap both unaffected — no gate in this hop reaches
  the approver.

  **Dead-end sweep (scoped to this event):** checked all three inboxes
  (`agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, `inbox/`)
  for anything newly filed against `ENG-010` specifically — none found.
  Nothing else on this ticket's own lineage to resume. **Notify sweep:**
  nothing to raise (a gate pass between two machine-owned states isn't an
  approver-facing item); nothing to nudge. **No new observation or
  proposal filed** — the one repo-wide pattern surfaced this round (RLS
  policies not accounting for `additional_roles`) has no live access path
  that exercises it (the only reader is the service-role client, which
  bypasses RLS and applies the wider check) and isn't new to this ticket —
  named in the receipt for the record rather than filed as a proposal
  nobody would act on differently.

  `chained: ENG-010` — `in-qa` is agent-owned (security is the next hop, a
  fresh session per this loop's own sequencing: security runs strictly
  after quality because it needs QA's finished test plan), not the
  approver, not blocked, not terminal, not held by a cap. Firing
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-010`
  before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

  **Checked the fire's actual outcome, same discipline every hop this
  evening has followed, rather than assuming it launched.**
  `traces/eng-loop-2026-09-02.log` tail: `lock is 6595s old but PID 17776
  is alive — not stealing`, then `continue — pass in flight, queued as
  pending`. `ps -p 17776` confirms the same 15:30 `scheduled launchd`
  orchestrating process is still alive (now ~110 minutes elapsed) — it has
  held the single-flight lock across the build hop, both review rounds,
  both fix hops, and this round-3 pass without releasing it once.
  `traces/.pending` confirms this pass's own fire landed rather than
  dropped: `1 continue ENG-010`. Not a broken chain — the security hop
  drains on the next fire of any kind, most likely that same orchestrator
  checking `.pending` again once this session exits. No manual re-fire
  attempted, for the same reason every prior hop gave: it would race the
  single-flight lock this mechanism exists to respect.

- `2026-09-02` **security gate: PASS — in-qa → in-security → ready-to-ship**
  (security, `continue` event pass, context `ENG-010` — the chain fired by
  round 3 above). **Confirmed this session is that queued fire, not a second
  concurrent one, by walking its own process ancestry** before touching
  anything: `claude -p "...Event: continue Context: ENG-010..."` →
  `run-claude.sh` (`timeout 3600`) → `eng-trigger.sh continue ENG-010` →
  `eng-trigger.sh scheduled launchd` (`17776`, the same PID every hop this
  evening has cited as the single-flight-lock holder, now elapsed ~1:54:16)
  → `eng-loop-all.sh scheduled launchd` → `launchd` — one continuous lineage,
  and `traces/.pending` reads empty (drained for this launch). Narrow scope
  per the event's own contract (this ticket only; no board-wide sweep). Mode
  check clean (business-os `.env` → `MODE=active`; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean. Ticket hop count
  (`traces/.hops-2026-09-02-ENG-010`) at 7 coming in; department daily count
  at 17. Both read against the tier's real budget, not the stale figure a
  department config file's own comment carries — see Observations below —
  and both well inside it (`plan.tier: max_5x` → 20/ticket, 200/day, verified
  by reading `lib/eng-trigger.sh`'s `read_plan_budget()` directly rather than
  trusting either the comment or this ticket's own prior citations of "20").

  **Found six consecutive passes' worth of uncommitted work in business-os
  (build hop through round 3) and independently re-verified all of it against
  the live repos before relying on any of it** — not assumed correct because
  the prose was thorough. Matches the open, previously-flagged gap
  (`[[project-buildloop-instance-repo-commit-gap]]`, this session's own
  memory): no durable instruction anywhere authorizes a pass to `git commit`
  the business-os instance repo itself, unlike the explicit L1
  branch/PR authorization `projects.md` grants for the product repos, and a
  prior pass already asked the approver once rather than deciding unilaterally
  — not re-asked here. Per that entry's own recorded safe default, left
  business-os uncommitted and kept working normally; did **not** run `git
  add`/`git commit` against it this pass either. Independent re-verification
  performed rather than skipped: fetched and read both worktrees directly
  (`aiorders-api@486eec0` vs merge-base `d37e0c9`, `aiorders-admin-hub@8b90f0e`
  vs merge-base `92bcacd`, both confirmed exactly matching this ticket's own
  frontmatter and both merge-bases confirmed unchanged at `ENG-009`'s own
  tip); read the full cumulative diff on both repos directly (not from the
  ticket log's account); re-ran `deno test --allow-net
  influencer-notes.test.ts` (16/16, matching every prior hop's own number);
  read `hasInfluencerAdminAccess`, the router's `authenticate()` allowlist,
  `adminSupabase`'s service-role construction, the RLS migration, and both
  cited precedents (`proxy_sessions_audit_logs.sql`,
  `20250729143357_initial_restaurant_rls.sql`) directly from disk. Every
  claim checked matched the ticket log's own account exactly — nothing
  fabricated or drifted found. Full verification detail, findings, and
  citations: `agents/security/reviews/ENG-010.md` (this gate's own receipt,
  first and only draft, written on this `pass` verdict per
  `skills/security-gate/SKILL.md` step 9).

  **Threat model, OWASP walk (0/10 blocking), negative-auth cases, secrets
  scan, and the SOC 2 evidence trail** — full detail in the receipt above,
  summarized here: every new route sits behind two independent, layered
  authorization checks (the router's unmodified allowlist, which already
  excludes `influencer`; this ticket's own reused `hasInfluencerAdminAccess`),
  plus, as of round 2's fix, a third at the database layer (RLS, verified by
  reading the migration file and both its cited precedents directly, not
  from the ticket log's account). No IDOR, no injection surface (Supabase
  query builder throughout, no raw SQL, note body renders as auto-escaped
  JSX text), no secret or credential in either diff or in the four commits
  this ticket added, no new dependency, no elevation of privilege, no new
  data-classification tier (freeform staff commentary about a named person
  classified **Internal** per `security-baseline.md`, correctly treated as
  higher-stakes than `ENG-009`'s own aggregate data by both the PRD and the
  design's second authorization layer). LLM checklist n/a — confirmed
  `touches_models: false` against both diffs directly.

  **Two non-blocking findings, both named, neither introduced fresh by this
  ticket.** (1) Both new handler functions carry the same raw
  `error.message`-in-500 pattern already tracked at three prior occurrences
  (`ENG-013`, `ENG-008`, `ENG-009`) and already proposed for promotion to a
  standard — a 4th and 5th occurrence, recorded in
  `agents/security/notebook/2026-09-02-findings.md` but **not re-proposed**,
  since the open `ENG-009` proposal already covers this exact class and a
  second one would just duplicate work for `principal-engineer` to
  reconcile. (2) `Access-Control-Allow-Origin: '*'` on both new routes —
  confirmed, by grepping every handler file in this directory, to be the
  identical pre-existing convention on all eleven files here, not a decision
  this ticket made; named explicitly for the first time on this board (no
  prior security review here mentioned it), read as lower-severity than the
  baseline's flat framing given this app's bearer-token (not cookie) auth
  model — an attacker would already need the token itself, at which point
  the wildcard isn't the control standing between them and the data. Not
  filed as a three-strike candidate (one repo-wide fact restated by every
  ticket touching this directory, not a new per-ticket recurrence) and not
  blocking.

  **No open P0/P1 bug** (`agents/qa/bugs/_index.md`: one open item,
  `BUG-001`, `P2`, unrelated project area) — checked fresh, not carried
  forward.

  **Verified independently, not taken on any prior hop's word:** `deno test
  --allow-net influencer-notes.test.ts`: **16 passed, 0 failed** (`deno`
  2.9.6). Every file this review's findings cite (`influencers.ts`,
  `admin-portal/index.ts`, the migration, both RLS precedents, every handler
  file's own CORS header) was read directly from disk this pass.

  **Receipt written** (`agents/security/reviews/ENG-010.md`, first and only
  draft — a security-gate receipt is written on a `pass` verdict only, per
  `skills/security-gate/SKILL.md` step 9 and `security-baseline.md`'s own
  "When the gate fails" section). `links.security_review` set on the ticket
  in the same edit as this entry.

  **2 transitions** (`in-qa → in-security → ready-to-ship`, both in this
  hop, matching round 3's own precedent for naming each lane state passed
  through even within one session), within the cap of 4. **Consequence:**
  machine WIP unaffected — `ready-to-ship` is still inside the counted
  `ready`..`ready-to-ship` range (the machine-WIP-1 slot frees only once
  devops's own hop moves this ticket to `blocked`, same precedent
  `ENG-008`/`ENG-009`/`ENG-013` each already set), so `ENG-010`'s slot stays
  1/1 unchanged. Approver-facing WIP and cap both unaffected — a security
  pass between two machine-owned states isn't an approver-facing gate.

  **Dead-end sweep (scoped to this event):** all three inboxes swept fresh
  (`agents/product-manager/inbox/`: only `.gitkeep` + `_handled/`;
  `agents/eng-manager/inbox/`: only `.gitkeep` + `_processed/`; `inbox/`:
  every live item already accounted for in the board index's own "Waiting on
  the approver" section — `ENG-013`/`ENG-008` merge requests, `ENG-016` G1,
  `ENG-009` merge request, `ENG-026`'s non-blocking intake-question) — nothing
  new against `ENG-010` specifically. **Notify sweep:** nothing to raise (a
  gate pass between two machine-owned states isn't an approver-facing item);
  nothing to nudge.

  **Observations filed** (`observations.md`): (1) `departments/engineering/
  agents/eng-manager/config.yaml` lines 488–489 (`max_hops_per_ticket: 8`,
  `max_hops_per_day: 40`, commented as mirrors of `plan.budgets[plan.tier]`)
  are stale — `plan.tier` reads `max_5x` (line 416, corrected 2026-08-29),
  whose real budget is 20/200, and `lib/eng-trigger.sh`'s
  `read_plan_budget()` correctly resolves through the tier dynamically
  (confirmed by reading the function), so the stale comment has zero runtime
  effect — but it contradicts the live value it claims to mirror, the exact
  comment-vs-code class `engineering-standards.md` already names as a
  defect. Department file, out of reach for a same-day fix from this
  instance-scoped pass; worth a Fable-authored correction next time someone
  is in that file for another reason. (2) The six-consecutive-pass
  uncommitted-business-os gap (`[[project-buildloop-instance-repo-commit-gap]]`)
  now extends through this hop too — recorded here for the count, per that
  entry's own "if a future pass finds a large uncommitted diff... don't
  assume silently" guidance; not re-asked to the approver a second time.

  `chained: ENG-010` — `ready-to-ship` is agent-owned (release readiness is
  next, a fresh session per this loop's own "each heavy step gets its own
  session" design — this pass stayed scoped to the security gate specifically,
  matching round 3's own framing of "security is next" as one dedicated hop
  rather than also taking on devops's own release-readiness work in the same
  session), not the approver, not blocked, not terminal, not held by a cap.
  Firing `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
  ENG-010` before this pass exits. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: both exit 0, clean, no `WAIVED:` lines.

  **Checked the fire's actual outcome, same discipline every hop tonight has
  followed, rather than assuming it launched.**
  `traces/eng-loop-2026-09-02.log` tail: this session's own `pass start:
  continue (ENG-010) [day 17/200 charged, 0 refunded today, ENG-010 7/20]` at
  17:21:45, then, for the chain fire just above, `lock is 7707s old but PID
  17776 is alive — not stealing` followed by `continue — pass in flight,
  queued as pending`. `ps -p 17776` confirms the same orchestrating process
  every hop tonight has cited is still alive (`eng-trigger.sh scheduled
  launchd`, elapsed `02:08:31`) — it launched this very security-gate session
  as its own subprocess and still holds the single-flight lock. `traces/
  .pending` confirms the fire landed rather than dropped: `1 continue
  ENG-010`. Not a broken chain — the release-readiness hop drains on the next
  fire of any kind, most likely that same orchestrator checking `.pending`
  again once this session exits. No manual re-fire attempted, for the same
  reason every prior hop gave: it would race the single-flight lock this
  mechanism exists to respect.

- `2026-09-02` **release-readiness: both PRs opened, now `blocked` on the
  approver** (devops, `continue` event pass, context `ENG-010` — the chain
  fired by the security-gate-PASS pass above, drained once the same
  orchestrating process this evening's every hop has cited checked
  `.pending` again). Confirmed this session is that queued fire, not a
  second concurrent one, by walking its own process ancestry: `claude -p
  "...Event: continue Context: ENG-010..."` → `run-claude.sh` →
  `eng-trigger.sh continue ENG-010` → `eng-trigger.sh scheduled launchd`
  (`17776`, the same PID every hop this evening has cited, elapsed
  `02:15:43` at time of check) → `eng-loop-all.sh scheduled launchd` →
  `launchd` — one continuous lineage. Narrow scope per the event's own
  contract (resume this ticket only; no board-wide sweep). Mode check clean
  (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
  scoped (`ENG-010`) and whole-board: both exit 0, clean, no `WAIVED:`
  lines. Ticket hop count (`traces/.hops-2026-09-02-ENG-010`) at 8 coming
  in (department daily 18/200) — well inside the `max_5x` tier's 20/ticket
  ceiling.

  **Read `skills/release-runner/SKILL.md` fresh before acting.** Both
  `aiorders-api` and `aiorders-admin-hub` are registered **L1**
  (`config/projects.md`) — step 1's window check does not apply; went
  straight to step 4.

  **Verified all four upstream gates fresh from the receipt files
  themselves**, not from this ticket's own log summary:
  `agents/database/migrations/ENG-010-influencer-relationship-notes.md`
  (**pass**, plus the round-2 RLS addendum),
  `agents/principal-engineer/reviews/ENG-010.md` (**pass**, round 3),
  `agents/qa/test-plans/ENG-010.md` (all 4 ACs covered, **pass**),
  `agents/security/reviews/ENG-010.md` (**pass**, 0/10 OWASP blocking). All
  four opened and read in full, not grepped for a verdict line alone.

  **Worktrees clean, on this ticket's own branch already.** Both
  `~/Documents/projects/_eng/{aiorders-api, aiorders-admin-hub}` fetched and
  confirmed sitting on `feat/ENG-010-influencer-relationship-notes` at the
  exact commits this ticket's frontmatter records (`486eec0`, `8b90f0e`), no
  ahead/behind against `origin`. Checked for an already-opened PR before
  creating one: `gh pr list --head feat/ENG-010-influencer-relationship-notes
  --state all` on both repos — empty on both. None existed.

  **Base-branch decision, re-verified rather than assumed from the design's
  own note.** This ticket's branch was built on `ENG-009`'s tip, not `main`
  (same reasoning `ENG-009`'s own release-readiness hop applied against
  `ENG-008`). Confirmed fresh: `git merge-base --is-ancestor
  origin/feat/ENG-009-influencer-engagement-info HEAD` → true on both repos;
  `git merge-base HEAD origin/feat/ENG-009-influencer-engagement-info`
  returns exactly `ENG-009`'s own current tip (`d37e0c9`/`92bcacd`,
  unchanged) on both. `gh pr list --head
  feat/ENG-009-influencer-engagement-info --state all` confirms `ENG-009`'s
  own two PRs (`aiorders-api#7`, `aiorders-admin-hub#6`) are still `OPEN`,
  not merged — opening this ticket's PRs against `main` would have pulled
  `ENG-009`'s own still-unreviewed-by-GitHub commits into this diff too,
  duplicating a PR already open and awaiting merge. Opened both PRs with
  `--base feat/ENG-009-influencer-engagement-info` instead — confirmed by
  diffing this ticket's branch against that base directly before creating
  anything (`aiorders-api`: 5 files, 538 insertions, 3 deletions;
  `aiorders-admin-hub`: 1 file, 115 insertions, 1 deletion) that this
  produces exactly `ENG-010`'s own change and nothing of `ENG-009`'s.

  **Step 3 readiness checks**, same interpretation this board already
  established for `ENG-007`/`ENG-008`/`ENG-013` given no live Postgres CLI
  reachable from this host:
  - Rollback: SQL written and reasoned through in the migration doc (`drop
    table if exists influencer_notes`, updated in the round-2 addendum to
    cover the added RLS policy too — dropping the table drops its policies
    with it) — not live-tested, the named, carried-forward gap every
    migration on this instance shares — paired with reverting the new
    handler file, its route registration, and the frontend Notes section in
    the same rollback, same three-way shape `ENG-008`'s/`ENG-009`'s own
    rollback notes already established for this file pair.
  - Observability: both new backend catches log via `console.error` before
    responding (confirmed directly in the security review's A09 line),
    surfaced through Supabase's existing function logs; the frontend write
    path surfaces a toast on failure — no new mechanism needed.
  - Cost: **$0/month delta** — no new vendor, no new dependency on either
    repo (security review's own Dependencies section, re-confirmed here via
    `git diff --stat` on both isolated diffs).
  - Window: n/a, L1.

  **Opened both PRs** (`aiorders-api` first, since `aiorders-admin-hub`'s
  Notes UI depends on its endpoints, same ordering `ENG-008`'s hop used):
  `aiorders-api` PR #8
  (https://github.com/harsimranwalia/aiorders-api/pull/8),
  `aiorders-admin-hub` PR #7
  (https://github.com/harsimranwalia/aiorders-admin-hub/pull/7). Verified
  both via `gh pr view` immediately after (`baseRefName`/`headRefName`/
  `state`) rather than trusting the create command's own stdout — both
  `OPEN`, based on `feat/ENG-009-influencer-engagement-info`, head
  `feat/ENG-010-influencer-relationship-notes`. Each PR body states what it
  does, the base-branch sequencing choice and both ways to resolve it, all
  four gate verdicts by file reference, and the named non-blocking gaps
  carried forward from review/security (the two tracked, pre-existing
  patterns — raw `error.message` in a 500, the repo-wide CORS wildcard — the
  RLS policy's `role`-only scope, and, admin-hub side, the standing
  no-frontend-test-harness gap plus two minor UX gaps named at round 3).
  Neither worktree left dirty; both still sit cleanly on this ticket's own
  branch (no other ticket had a claim on either worktree this pass).

  **Wrote the L1 merge-request item**
  (`inbox/2026-09-02-eng010-merge-request.md`, `gate: merge`, `agent:
  eng-manager`), `pr_urls:` as a YAML list of `{repo, url}` pairs per
  `skills/release-runner/SKILL.md` step 4 (one item covering both repos,
  never one per repo), carrying both PR links, all four gate verdicts by
  file reference, an explicit Sequencing section (this ticket's PRs stack
  behind both `ENG-009`'s and `ENG-008`'s still-open ones; any merge order
  among the three is legal), and the named non-blocking gaps. Ran
  `departments/engineering/lib/eng-notify.sh raise`: sent cleanly
  (`traces/eng-notify-2026-09-02.log`: `[17:45:02] sent: active
  2026-09-02-eng010-merge-request.md`). Stamped `notified: 2026-09-02T17:45:02`
  on the item by hand from that trace line, matching this board's own
  established (and, per `ENG-009`'s own re-check, verified-correct)
  convention of a bare local-clock ISO string with no UTC offset.

  **Cap check before this transition, read fresh from `inbox/`'s actual
  top-level contents**: ten items present besides this pass's own new one —
  `ENG-008`'s and `ENG-013`'s merge requests, `ENG-016`'s G1, `ENG-009`'s
  merge request (all four already counted), plus two `eng-events-dropped`
  notices, an `eng-loop-halted` notice, a gate-violation-watch notice,
  `ENG-007`'s own continue-sequence-question, and `ENG-026`'s
  intake-question — none of the latter five hold an approver-facing WIP
  slot (system-level notices and non-blocking intake questions, not
  G1/G2/G3/merge gates on a ticket). Approver-facing WIP was already `4/2`,
  over cap, going in. This transition adds a fifth. Same reasoning
  `ENG-008`'s and `ENG-009`'s own release-readiness hops already
  established at this identical point: the cap gates **new** work from
  starting that will need the approver — it does not hold a ticket that has
  already earned `ready-to-ship` back from reaching its required,
  non-discretionary L1 conclusion. Not treated as a reason to hold this hop.

  State `ready-to-ship → blocked`, `blocked_on: approver`, `blocked_from:
  ready-to-ship`, owner `devops → approver`. `links.pr` set to both PR URLs
  (`pr:` as a YAML list of `{repo, url}` pairs, matching `ENG-008`'s/
  `ENG-009`'s corrected convention). `time_spent`/`time_remaining` updated
  in frontmatter in the same edit as this entry. No release record yet, per
  `release-runner`'s own step 7/step 4 split — written only once the build
  loop's merge-detection confirms both PRs merged.

  **1 transition** (`ready-to-ship → blocked`), well under the cap of 4 —
  opening two PRs and writing the gate item is itself the real work of this
  hop. **Consequence:** `machine_wip` 1/1 → 0/1 (`blocked` sits outside the
  counted `ready`..`ready-to-ship` range; `ENG-010` was the sole occupant,
  so the range is now empty — a new ticket may enter `ready` on a future
  pass, not decided by this one, whose own contract stays scoped to
  `ENG-010`). Approver-facing WIP `4/2 → 5/2`; no separate approval cap
  exists to update (removed 2026-08-29).

  **Dead-end sweep (scoped to this event):** this ticket's log now ends in
  a valid, accounted-for state with the chain record below. `ENG-009` (the
  ticket this branch stacks on) untouched beyond the read-only `gh pr
  view`/ancestry checks above. One item outside this ticket's own scope
  noted rather than acted on: `traces/.pending` holds `1 watch launchd`,
  queued at 17:44:59 while this pass was already running (`traces/
  eng-loop-2026-09-02.log`: `lock is 8094s old but PID 17776 is alive — not
  stealing`, `watch — pass in flight, queued as pending`) — out of this
  `continue ENG-010` event's own narrower contract, and not a broken chain:
  it drains on the next fire of any kind, most likely the same
  still-running orchestrator checking `.pending` again once this session
  exits. Not manually processed, for the same reason no hop tonight has
  manually re-fired: doing so would race the single-flight lock this
  mechanism exists to respect.

  **Notify sweep:** this pass's own item raised and stamped above. Nothing
  else newly eligible to nudge — `ENG-008`/`ENG-013`/`ENG-016` already spent
  their one nudge each; `ENG-009`'s merge request is ~7h old, under the 24h
  threshold; this new item is 0h old.

  **No new proposals filed** — every named gap in this hop's PR bodies and
  gate item is already tracked elsewhere (the frontend-test-harness
  proposal, the verbose-error-response proposal, the CORS-wildcard and
  RLS-scope notes already recorded in the security review). **One
  observation filed** (`observations.md`): `skills/release-runner/SKILL.md`'s
  own Trace section calls for a `traces/devops-{run-id}.json` per release
  hop; `find traces -iname "*devops*"` returns nothing, and neither
  `ENG-008`'s nor `ENG-009`'s own release-readiness hops produced one
  either — not written here either, matching rather than breaking that
  precedent. Checked `agents/qa/bugs/_index.md` fresh: still only `BUG-001`
  (P2, unrelated project area) — no open P0/P1 anywhere on the board.

  `chained: none` — `blocked`, `blocked_on: approver`. This is the human
  gate the whole hop was driving toward; firing `continue ENG-010` again
  would only queue against a ticket with nothing left for a machine to do
  until the approver merges one or both PRs (in either sequencing order,
  per the item's own Sequencing section) or replies to the gate item. Same
  precedent `ENG-008`'s and `ENG-009`'s own release-readiness entries
  already set at this identical state. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
  whole-board: see board index.

- `2026-09-03` **informational cross-reference only — no state change, this
  ticket's own code not touched** (eng-manager, `scheduled` event pass,
  context `auto-drain` — whole-board sweep). `ENG-009`'s branch (this
  ticket's own base) is stale against `ENG-008`'s round-3 fix — full
  finding on `ENG-009`'s own board file, same date. Checked whether this
  ticket adds anything of its own to the conflict: `git diff` of this
  ticket's tip against `ENG-009`'s tip, both repos, for
  `accepts_barter`/`barter_visit` — empty on both. This ticket inherits the
  conflict wholesale rather than contributing to it.

  `inbox/2026-09-02-eng010-merge-request.md` corrected with a short pointer
  to `ENG-009`'s own (corrected) merge request rather than duplicating the
  full finding — this ticket's own `recommendation:` left as `merge`
  unchanged, since merging this PR into `ENG-009`'s branch (not `main`,
  per this item's own Sequencing section) is unaffected either way; only
  the eventual `main`-ward path is where `ENG-009`'s fix has to land
  first. Not re-notified, same reasoning as `ENG-009`'s own entry
  (one-raise-one-nudge budget already spent, not yet 24h old, correction
  lives in the file itself).

  `chained: none` — `blocked`, `blocked_on: approver`, unchanged.
