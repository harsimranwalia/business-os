---
id: ENG-043
title: Clarify which ticket "stage names" belongs to before shaping (ENG-011 or ENG-028)
project: aiorders-admin-hub
type: feature
size:
time_estimate:
time_spent:
time_remaining:
severity: P3
priority:
state: intake
owner: product-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-09-06
updated: 2026-09-06
branch:
depends_on: []
blocks: []
parent:
links:
  prd:
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

Cannot state this yet — that's the finding, not a gap to fill by guessing.
The raw request names an operation ("stage names... should be ed[itable]")
but the object is ambiguous between two live, unrelated tickets that both
have a "stage names" concept, and the request's own body carried no
recoverable content beyond a single, uninterpretable word. Per PM
agent.md ("if you can't write that paragraph, say so in the ticket and ask
the one question that would let you"), this ticket exists to hold that
question, not to force a problem statement the input doesn't support.

## Outcome

Not yet known. Once the approver answers the question in
`inbox/2026-09-06-eng043-stage-names-clarification.md`, this ticket either
(a) gets a real problem statement and proceeds to a PRD if it's genuinely
new scope, (b) gets folded into `ENG-028`'s own still-open G1 rescope reply
if that's what was meant, or (c) is dropped if the answer is "neither" /
the approver resends a clean version elsewhere.

## Notes

**Input, verbatim** (`agents/product-manager/inbox/2026-09-06-enhance-eng-011-stages-names-shoud-be-ed.md`,
now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-09-06T09:15:26.053364+00:00 — this is the
complete file body, nothing omitted:

> # Enhance ENG-011 stages names shoud be ed
>
> Healf

**Full request-readback run**, per `skills/request-readback/SKILL.md`, both
readings on `opus`, from the raw text plus `knowledge/business-profile.md`
only (no repo access, blind to each other) — the trigger for full-lane
intake, and no reason to skip it just because the text is short.

- **PM-lens reading:** reads the title as "stage names should be ed[itable
  /ited]," flags the body as unrecoverable ("Healf" — no honest candidate),
  and explicitly recommends not proceeding without a re-ask.
- **Architect-lens reading, independently blind:** converges on the same
  object ("stage names, from ENG-011") but is explicit that it can name the
  object and not the operation — rename-once vs. make-renameable is, in its
  own words, "materially different work."

**No material divergence between the two readings on the headline claim**
(both read "stage names should become editable") — by the skill's own
table that's "same picture, different words," which would normally mean
proceed. What makes this ambiguous enough to ask anyway is something
neither blind reading could see, because both were deliberately given only
the raw text and business-profile.md, never repo or board state (that's
the method — see `request-readback/SKILL.md` step 3). This PM's own
follow-up check against the live board is what surfaces the real fork:

**Checked, not assumed: two different tickets on this board both have a
"stage names" concept, and the title's "ENG-011" reference has already
been wrong once before in this exact shape.**

- `ENG-011` (`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`,
  `state: verified`, terminal) shows a restaurant's **client stage**
  (`live` / `onboarding` / `inactive`) on the Brands admin page, derived
  read-time from `is_active`/`onboarding_step`. Its own acceptance
  verification explicitly checked and passed a non-goal: "no configurable
  stage taxonomy (`ONBOARDING_FINAL_STEP` is a fixed constant)." A request
  to make these names editable is coherent — it would be reopening a
  named non-goal — but it's a *cold* ticket, shipped a week ago.
- `ENG-028` (`agents/eng-manager/board/ENG-028-foodswipe-custom-pipeline-stages.md`,
  `state: awaiting-scope`) is about the **FoodSwipe funnel's pipeline
  stage names** — a completely different concept (sales/onboarding
  progress, not client lifecycle). It is not cold: its G1 rescope answer,
  hardcoding nine literal stage names in place of a staff-configurable
  editor, was decided at **2026-09-06T09:09:08** — six minutes before this
  request arrived at 09:15:26. This ticket's own fresh G1
  (`inbox/2026-09-06-eng028-g1-rescope.md`) is sitting open, unanswered,
  right now.
- **Precedent that "ENG-011" in a title is not reliable evidence of
  intent**: `agents/product-manager/inbox/_handled/2026-09-01-eng-011-on-the-brand-portal-i-want-option-to-make-the-restau.md`
  cited "ENG-011" in its own title while describing work with no
  connection to it; that pass allocated a fresh id (`ENG-026`) rather than
  trusting the label. Same caution applies here, doubly so given how much
  more directly ENG-028 fits "stage names" than ENG-011 does.

**Reading this together: the six-minute gap is the load-bearing fact.**
This could be someone continuing to think about the FoodSwipe stage-name
decision they'd just made and mistyping the ticket id (`ENG-011` for
`ENG-028`) — in which case this isn't new scope at all, it's a follow-up
thought that belongs on `ENG-028`'s still-open G1, not a new ticket. Or it
could genuinely be about `ENG-011`'s own client-stage labels, unrelated to
the FoodSwipe decision, arriving minutes later by coincidence. Both are
live readings a single blind text-only pass could never distinguish, and
picking one to build would risk either reopening a shipped, verified
ticket's declared non-goal on a guess, or silently duplicating a decision
already awaiting the approver's own answer three lines away in the same
inbox.

**"Healf" carries no recoverable content.** Neither reading produced a
candidate; noted plainly rather than forced into a guess (e.g. "Health,"
`ENG-011`'s own other visible attribute, is a plausible completion but
unconfirmable and not built on).

**Filter check, done anyway despite holding at intake:** worth asking
rather than worth dropping. Both candidate tickets are real, live, and
this is a six-minute-old thought from the approver, not stale noise — the
"would not building it be fine" test doesn't even apply yet, because
nobody knows what "it" is.

**No PRD written** — per PM agent.md ("don't write a PRD around a problem
you can't state") and the request-readback chain itself (divergence found
→ ask → stop there), writing requirements or a brief before this answers
would be inventing scope.

**One observation filed** (`observations.md`): this is the first garbled/
truncated control-center submission seen on this board (distinct from
`ENG-026`'s case, which was a fully-formed request with a wrong id, not
truncated text) — one occurrence, not a pattern, not a proposal.

## Log

Append-only. One line per state transition, newest last.

- `2026-09-06` **held at `intake` — no transition** (product-manager,
  `intake` event pass, context
  `agents/product-manager/inbox/2026-09-06-enhance-eng-011-stages-names-shoud-be-ed.md`).
  Per this event's own narrower contract: act on this one request, don't
  sweep the board. Mode check clean (business-os `.env` → `MODE=active`;
  instance `config/config.yaml` → `mode:` empty, falls back). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
  clean.

  **Ran the full request-readback** (two `opus` subagents, PM lens and
  blind architect lens, raw text + `knowledge/business-profile.md` only —
  see Notes above for both readings in full). No material divergence
  between the two readings themselves, but both independently flagged the
  input as incomplete and recommended asking rather than guessing.

  **Went further than either blind reading could**, per this PM's own
  standing practice of checking live state before proposing defaults
  (`ENG-011`'s and `ENG-028`'s own precedent): checked both candidate
  tickets' board files fresh rather than trusting the title's own
  attribution. Found `ENG-011` verified/terminal with a matching non-goal
  ("no configurable stage taxonomy") and `ENG-028` awaiting-scope with a
  same-topic G1 rescope decided six minutes before this request arrived,
  still unanswered. Also checked this board's own history for a prior
  "ENG-011 cited wrong" incident and found one
  (`ENG-026`'s intake, 2026-09-01) — directly on point, not a coincidence
  worth ignoring.

  **Did not guess between the two.** Per `request-readback/SKILL.md` step
  4 ("a material divergence is not a failure to resolve internally... two
  careful readers disagreeing is the finding") — here the disagreement is
  between what the raw text says and what this PM's own investigation
  surfaces, which is the same category of finding the skill exists to
  catch, just discovered one layer later than the two-reading comparison
  itself. Wrote one question, framed as a choice between the two concrete
  readings plus an explicit "neither" escape hatch (same shape
  `ENG-011`'s own "tickets" question used), rather than an open "can you
  clarify."

  **No new ticket id spent on either candidate.** `ENG-043` (this ticket)
  exists to hold the question itself, not to pre-allocate scope under
  either `ENG-011` or `ENG-028` — allocating under one of the two live
  candidates before knowing which is right would itself be a guess, just
  a quieter one.

  Source card moved `agents/product-manager/inbox/` →
  `agents/product-manager/inbox/_handled/` with a processed footer
  pointing here. Gate item written:
  `inbox/2026-09-06-eng043-stage-names-clarification.md` (`gate:
  intake-question`, `agent: product-manager`, `project:
  aiorders-admin-hub`, `ticket: ENG-043`). Ran
  `departments/engineering/lib/eng-notify.sh raise` — see the item's own
  frontmatter for the result and `notified:` timestamp. One observation
  filed (`observations.md`): first garbled/truncated control-center
  submission seen on this board.

  **State: stays `intake`.** No project/size/one-line-problem-statement
  exit condition met, deliberately — `definition-of-done.md`'s own exit
  bar for this state ("shaped: project set, size set, type set, one-line
  problem statement") isn't met because the object of the request isn't
  known yet, not because shaping was skipped. `owner: product-manager` —
  `intake` is not one of the enumerated states where `owner: approver` is
  correct per `config/templates/ticket.md` (`awaiting-scope`,
  `awaiting-decision`, `awaiting-release`, or `blocked` with `blocked_on:
  approver`); the gate item in `inbox/`, not this field, is what actually
  surfaces this to the approver. **0 transitions.** No cap consequence —
  `intake` sits outside the counted `ready`..`ready-to-ship` machine-WIP
  range, and `wip.approver_limit` has been unlimited/visibility-only since
  2026-09-02.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract — no other ticket touched. `ENG-028`'s own still-open G1
  rescope item is left exactly as it is; this pass does not answer it or
  treat this new note as an answer to it, since that would be guessing
  Reading B without the approver having said so.

  **Notify sweep:** this pass's own gate item raised and stamped above.
  Nothing else to nudge for this ticket (nothing prior existed).

  `chained: none` — held at `intake`, the question just raised has no
  agent-owned next step; nothing machine-actionable exists on this ticket
  until the approver answers `inbox/2026-09-06-eng043-stage-names-clarification.md`.
  Firing `continue ENG-043` now would queue an event against a ticket with
  nothing for a machine to do. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board: see this
  pass's own final check.
