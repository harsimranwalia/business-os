---
id: ENG-010
title: Influencer relationship notes — staff log for personality, preferences, and off-platform conversations
project: aiorders-admin-hub
type: feature
size: S
severity: P3
priority:
state: awaiting-scope
owner: approver
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
  design:
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
