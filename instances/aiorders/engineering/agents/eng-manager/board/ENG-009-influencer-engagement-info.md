---
id: ENG-009
title: Influencer engagement info — internal activity signal plus a staff-editable social stat
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
  prd: agents/product-manager/specs/ENG-009-influencer-engagement-info.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

This ticket is the direct, approver-answered resolution of the standing
question raised while shaping `ENG-008`
(`inbox/_handled/2026-08-29-eng008-engagement-source-question.md`), itself
carved out of the same original request as `ENG-008`
(`agents/product-manager/inbox/_handled/2026-08-29-for-the-influencer-board-on-admin-panel-we-are-unable-to-see.md`).
Verbatim answer, given as a hand-edit to the question item while this
pass was still running:

> i mean both reading a and reading B. reading A is something we can start
> with now so we know how active the particular influencer is. reading B
> is something our staff can update or later we can connect using some api
> from meta.

## Readback

**Understood as:** Both candidate readings of "engagement" are wanted, not
one instead of the other:
- **Reading A** — an internal signal showing how active a given influencer
  is on AIOrders (derived from existing/adjacent data — campaigns,
  collaborations, responses). Build now.
- **Reading B** — a social-media engagement figure (e.g. follower count or
  engagement rate). For now this is **staff-entered by hand**, not pulled
  from any platform. A live Meta API connection is explicitly named as
  future work, not this ticket — "later we can connect."

No second blind reading run for this ticket: the standing question this
answers already went through the full request-readback comparison (both
independent readings flagged the same gap; see `ENG-008`'s PRD), and the
approver's own reply directly resolves it with concrete instructions
rather than reopening any ambiguity a second reading could usefully test.

**Requirements:**
1. `[confirmed]` Staff can see an internally-derived indicator of how
   active an influencer is on AIOrders.
2. `[confirmed]` Staff can view and manually enter/update a social-media
   engagement figure for an influencer.
3. `[inferred]` The two figures are shown distinctly, not merged into one
   number — they answer different questions (platform activity vs.
   external social reach).
4. `[proposed]` The manually-entered social figure shows when it was last
   updated, since nothing keeps it fresh automatically.

**Assumed, and worth correcting if wrong:**
- "How active" (reading A) is a derived read, not a new field staff types
  in — the architect picks the concrete measure (e.g. campaigns applied
  to, collaborations count, response rate) from what already exists,
  rather than this PRD inventing a formula.
- The social figure (reading B) is a single number (e.g. a follower count
  or a percentage) staff overwrite each time they check, not a
  history/timeline of past values — a timeline is a bigger feature nobody
  asked for.
- No specific platform (Instagram vs. TikTok vs. both) is named for the
  manual figure — staff can label or choose per influencer; this ticket
  doesn't hardcode one platform.

## Problem

Staff have no way to judge how active an influencer actually is on
AIOrders, or to record what their social reach looks like, even
informally — both are needed to make a sensible match/rating decision, and
today neither exists anywhere on the admin board.

## Outcome

An influencer's admin record shows an internally-derived activity signal
and a staff-editable social engagement figure. No external API call is
made by this ticket.

## Notes

**No hard dependency on `ENG-008`**, but sequenced after it in practice:
both tickets touch the same influencer-detail admin UI (`aiorders-admin-hub`)
and the same influencer table (`aiorders-api`), and building them
concurrently risks a merge conflict on the same files for no real benefit
— not a data dependency, an engineering-sequencing one. The EM's call at
`ready`, not decided here.

**Explicitly not the Meta API integration.** The approver's own words defer
that ("later we can connect") — this ticket delivers the staff-manual
version now. Whoever files the future API-connected version should treat
this ticket's manual field as the thing it eventually replaces or
augments, not something to redesign from zero.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped → awaiting-scope` (product-manager, same
  `intake` event pass as `ENG-008`, continued after the standing question
  it depended on was answered mid-pass). Caps checked fresh: approver-facing
  WIP 1/2 (from `ENG-008` this same pass) → this ticket would take the
  second and last free slot; approval cap 2/3 → closing the now-answered
  question and opening this G1 nets to 2/3 (unchanged count, different
  contents).

  **Shaped directly from the approver's own answer** rather than running a
  fresh two-reading comparison — the ambiguity that comparison exists to
  catch was already found and is now resolved by direct instruction; a
  second blind reading here would be ceremony over an approver-authored
  spec, per `skills/request-readback/SKILL.md`'s own exemption for a
  request that's already effectively a spec.

  PRD written:
  `agents/product-manager/specs/ENG-009-influencer-engagement-info.md`. G1
  raised: `inbox/2026-08-29-eng009-g1-scope.md`. Ran
  `departments/engineering/lib/eng-notify.sh raise`; see the item's own
  frontmatter for the result.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist
  (same open proposal, not refiled).

  **State:** `intake → shaped → awaiting-scope`, all in this pass. `owner`
  moves `product-manager → approver`. **Consequence:** approver-facing WIP
  1/2 → 2/2 (cap reached, not exceeded — no further approver-dependent
  work starts until one of these two clears). Approval cap stays 2/3 (the
  answered question closed, this G1 opened). Machine WIP unaffected.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human.
