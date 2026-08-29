---
type: eng-decision
agent: product-manager
gate: intake-question
project: aiorders-admin-hub
ticket: ENG-008
recommendation: Answer when convenient — does not block ENG-008's G1 or build. Once answered, this becomes its own small ticket (likely sequenced after ENG-008).
raised: 2026-08-29
notified: 2026-08-29T09:07:09
decision: approved
decided: 2026-08-29T09:10:52.731201+00:00
---

# One open thing before "engagement" can be scoped — does not block ENG-008

**You said:** "...also information on the engagement is missing ." (from
the same request as `ENG-008`, `agents/eng-manager/board/ENG-008-influencer-profile-admin-management.md`)

Two independent readings of this request (this PM's and, separately and
blind to it, the architect's) both landed on the same gap: neither could
tell what "engagement" means here, and the two candidate readings are far
enough apart in cost that guessing either way risks either a wasted build
or an undersold recommendation.

**Reading A:** "Engagement" means the influencer's activity on our own
platform — campaigns applied to, collaborations completed, response rate,
that kind of thing. Data we can derive from what we already have (or will
have once `ENG-008`'s fields exist). No new vendor, no new cost.

**Reading B:** "Engagement" means the influencer's social-media stats —
follower count, engagement rate — pulled from Instagram/TikTok/etc. This
needs a new third-party integration, most likely OAuth on the influencer's
own account, and an ongoing per-month or per-call cost.

**Which one?** (Or something else — if it's a number you already track
somewhere outside AIOrders today, say where.)

This does not hold up `ENG-008`, which covers region/campaign-type
preference, rating, and collaboration count and has no dependency on this
answer. Once answered, "engagement" gets shaped into its own small ticket
— likely sequenced after `ENG-008` since it lands on the same admin board.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-29T09:10:52.731201+00:00

i mean both reading a and reading B. reading A is something we can start with now so we know how active the particular influencer is. reading B is something our staff can update or later we can connect using some api from meta.

---

**Processed 2026-08-29, same `intake` pass that raised this item.** The
approver answered by hand-edit while this pass was still running, ahead of
the `decision` event this answer will also independently queue —
consistent with this instance's established practice of whichever event
reaches a fact first doing the real work. Read as: both readings wanted,
not a choice between them — an internal activity signal (buildable now, no
cost) and a staff-entered social figure (buildable now, no cost), with a
live Meta API connection explicitly named as later work, not this round.
Shaped directly into `ENG-009` (`agents/eng-manager/board/ENG-009-influencer-engagement-info.md`),
its own PRD, and a fresh G1
(`inbox/2026-08-29-eng009-g1-scope.md`) in the same pass, per the same
step-6b-style reasoning `ENG-006`/`ENG-007` established: this item was
already named as the next thing to file once answered, so filing it is
finishing this same request, not new agent-invented scope. Journaled in
`agents/eng-manager/config/decision-journal.md`.
