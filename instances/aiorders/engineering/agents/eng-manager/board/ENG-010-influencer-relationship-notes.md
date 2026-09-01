---
id: ENG-010
title: Influencer relationship notes — staff log for personality, preferences, and off-platform conversations
project: aiorders-admin-hub
type: feature
size: S
severity: P3
priority:
state: ready
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-08-29
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-010-influencer-relationship-notes.md
  design: agents/architect/designs/ENG-010-influencer-relationship-notes.md
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
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
