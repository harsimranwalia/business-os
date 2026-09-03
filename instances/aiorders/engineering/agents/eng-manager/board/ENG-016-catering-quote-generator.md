---
id: ENG-016
title: Catering page — self-serve quote generator, with automatic stage update
project: config-site-builder
type: feature
size: L
time_estimate: several days to a week
time_spent:
time_remaining:
severity: P2
priority: next
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-09-03
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-016-catering-quote-generator.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Problem

A restaurant's catering leads dead-end at "thanks, we'll be in touch" —
the owner is notified and a CRM record is created, but every quote after
that is fully manual (staff price it and reply by phone/email), there's no
computed price, and the catering pipeline on restaurant-portal is only
ever updated by a staff member dragging a card by hand.

## Outcome

**Rescoped 2026-09-03 after the approver's `changed` G1 answer — see PRD
for the full rewrite and the resulting split.** This ticket now covers
Piece 1 only: a customer on a restaurant's public catering page picks a
fulfillment option and guest count, selects menu items by category with
quantities and a note each (no price shown), and either submits or asks
for a callback instead. Either way the matching request lands on
restaurant-portal's catering board in the right stage automatically. A
restaurant with no structured menu data sees no change from today.
Displayed pricing (a package/price-book model) and owner-side quote
editing/resend are named as Piece 2 and Piece 3 in the PRD, not filed as
tickets yet.

## Notes

Full grounding, evidence, and the two forks named in the request-readback
(who controls the "just contact me" fallback; reuse the existing menu's
prices vs. a new catering-specific pricing model) are in the PRD — see
`links.prd`. Spans three repos: `config-site-builder` (primary — the new
customer-facing quote page), `aiorders-api` (quote storage, link
generation, send — reusing the existing `outgoing-communications`/
`autopilot` engine), `restaurant-portal` (one additive status value plus a
small addition to the already-shipped `CateringDetailModal`).

Deliberately held at `shaped` rather than advanced to `awaiting-scope` —
see Log. Not a scope gap; the G1 content is fully drafted in the PRD and
ready to raise the moment a WIP slot frees.

## Log

- `2026-08-29` `intake → shaped` (product-manager) — event pass, context
  `agents/product-manager/inbox/2026-08-29-for-catering-page-need-next-step-quote-generator-page-which-.md`.
  Sized `L`, project `config-site-builder` (primary; `aiorders-api` and
  `restaurant-portal` also touched, named in the PRD per the `ENG-003`
  precedent for a multi-repo ticket under a singular `project:` field).
  Ran the full request-readback (`skills/request-readback/SKILL.md`): this
  PM's own reading, grounded in live code across all three repos, plus a
  blind architect reading (subagent, `opus`, raw request +
  `knowledge/business-profile.md` only, no repo access, no exposure to
  this PM's own reading). No material divergence on the core shape; two
  real forks surfaced (fallback-path control; menu/pricing reuse vs. a new
  catering-specific model) — both resolved with a stated, correctable
  default bundled into the PRD as a G1 rider, same bar `ENG-015`'s G1 used
  for its own small fork, rather than opening a separate blocking standing
  question.
  **Caps checked fresh, not from the cached board header, before deciding
  how far to carry this ticket:** `inbox/` re-listed directly this pass —
  `2026-08-29-eng014-g1-scope.md` and `2026-08-29-eng015-g1-scope.md` both
  still present, unanswered (`ENG-009`/`ENG-010`/`ENG-012`'s G1s and
  `ENG-013`'s standing question also still present but already answered
  per prior passes' own findings, off the count per this board's
  established convention). Approver-facing WIP therefore still
  substantively 2/2 — at cap — per `board/_index.md`'s own header, itself
  confirmed fresh this pass rather than trusted. Per
  `schedules/eng_build_loop.md`'s Guards section ("Approver WIP limit (2)
  ... At the limit, nothing new starts that will need them"), this ticket
  — full lane, `type: feature`, not on the G1-auto-skip list — was carried
  through readback and PRD-writing (agent-owned work, consumes nothing of
  the approver's queue) but **held at `shaped` rather than advanced to
  `awaiting-scope`**, since doing so would raise a third open G1 against a
  cap of two. The PRD's own G1 content (readback, recommendation, both
  forks named as riders) is fully drafted and ready — nothing further to
  shape once a slot frees.
  `chained: none` — held by the approver-facing WIP cap (2/2:
  `ENG-014`, `ENG-015` both still open, neither cleared during this pass);
  not blocked, not waiting on a human for *this* ticket specifically, but
  the chaining guard's cap exception applies all the same, since firing
  `continue ENG-016` now would only re-discover the same cap with no new
  work to do. Re-check on the next `decision`/`watch`/`scheduled` pass that
  clears `ENG-014` or `ENG-015`, or via a dedicated `continue ENG-016` once
  either does.

- `2026-08-29` `shaped → awaiting-scope` (product-manager, `scheduled` event
  pass, context `schtasks`). This is exactly the re-check this ticket's own
  prior entry named: `ENG-014` and `ENG-015` have both since reached
  `designed` (past their own G1s), confirmed fresh from each ticket's own
  frontmatter rather than trusted from the board table — approver-facing
  WIP is 0/2, fully free. Mode check clean (business-os `.env` → `MODE=`
  empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-016`) and
  whole-board: both exit 0, clean.

  **Also corrected while re-checking the cap, not assumed from the board
  header:** `agents/eng-manager/config/config.yaml` records `approval_cap`
  as removed 2026-08-29 at the approver's request — the only real
  approver-side lever left is `wip.approver_limit` (2). The board index's
  repeated "Approval cap 3" framing is stale relative to that removal; fixed
  in this pass's board update rather than propagated further.

  No new readback needed — the G1 content was already fully drafted in the
  PRD at `shaped` time (see PRD's own Decision section, now updated to
  `status: awaiting-scope`). Raised
  `inbox/2026-08-29-eng016-g1-scope.md`, ran
  `departments/engineering/lib/eng-notify.sh raise` (logged
  `SLACK_WEBHOOK_URL unset — cannot notify`, non-fatal per the script's own
  design — the item still sits in `inbox/` and the control center), stamped
  `notified: 2026-08-29T23:13:49`.

  **Picked ahead of `ENG-017`/`ENG-019`/`ENG-020`/`ENG-021` per the board's
  own dispatch ordering** (`eng_build_loop.md` step 6): `priority: next`
  outranks the unset priority the other three carry; `ENG-018` excluded
  outright (`priority: hold`). Exactly two free approver-facing WIP slots
  and exactly two tickets ordered ahead of the rest (`ENG-016`, then
  `ENG-017`) — both raised this pass, filling the cap to 2/2 without
  exceeding it.

  **1 transition** (`shaped → awaiting-scope`), well under the cap of 4 —
  `awaiting-scope` is owned by the approver, this pass's own stopping
  point. **Consequence:** approver-facing WIP 0/2 → 1/2 (this G1); machine
  WIP unaffected (`awaiting-scope` sits outside the counted range).

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard never fires on a ticket waiting on a human. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-016`) and
  whole-board: see board index.

- `2026-09-01` **no state change — `board/_index.md` corrected instead**
  (`watch` event pass, context `launchd`). Found this ticket's own file and
  PRD (both `awaiting-scope`, G1 raised and notified `2026-08-29T23:13:49`,
  never answered) disagreeing with `_index.md`'s In-flight table and
  "Waiting on the approver" section, both of which read `shaped` /
  `product-manager` / "G1-drafted, ready to raise" for this ticket. Root
  cause: the 09:30 pass's own `git pull` (`e281c71`, "reconcile 26 diverged
  engineering-board files") kept a rival host's account of the index
  wholesale for internal consistency with several other tickets that really
  were behind on that host — but that host had never learned this ticket's
  G1 was raised on 2026-08-29, so its narrative was not stale, it was
  genuinely missing an event. Checked `decision-journal.md` (no `ENG-016`
  row) and this ticket's own PRD `status:` before concluding staleness
  rather than a legitimate reset — neither shows one. Corrected `_index.md`
  in place (In-flight row, header WIP accounting, "Waiting on the approver"
  section) rather than this ticket's own file, which was already right.
  Also nudged the open G1 (`inbox/2026-08-29-eng016-g1-scope.md`,
  `nudged: 2026-09-01T10:20:06`) — notified 2.5 days ago, never nudged
  before, missed by every intervening pass because they all read the index
  rather than this file. Filed a proposal
  (`agents/eng-manager/proposals.md`) so a future cross-host reconciliation
  re-derives the In-flight table from each ticket's own frontmatter instead
  of keeping one side's board-index prose wholesale.
  `chained: none` — still `awaiting-scope`, owned by the approver; unchanged
  by this correction.

- `2026-09-03` **no state change — G1 answered `changed`, PRD rewritten,
  fresh G1 raised** (`scheduled` event pass, context `manual`; this is the
  gate-return step of a whole-board sweep, not a `continue` on this ticket
  specifically). Mode check clean (`MODE=active`). Pre-pass
  `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

  The G1 raised 2026-08-29 came back `decision: changed` (decided
  2026-09-03T00:53:17Z) with a complete replacement engineering spec, not
  an edit — reproduced in full in `inbox/2026-08-29-eng016-g1-scope.md`.
  Delegated the actual PM judgment (sizing, the filter, the PRD rewrite) to
  an `opus` subagent per `prd-writer/SKILL.md`'s own model designation,
  after gathering fresh codebase evidence via a separate `sonnet` research
  subagent — kept the two apart deliberately: fact-finding doesn't need
  opus, the sizing/split call does.

  **Verdict: the rewrite is `XL`, not `L`.** It reintroduces the
  catering-specific tiered pricing model the original PRD named as a
  non-goal, plus the owner-side quote editing it deferred, plus a new
  view-tracking mechanism this codebase has no equivalent of today (SMS
  delivery has no open-tracking at all; email's is partial and unrelated
  to catering). Per `prd-writer/SKILL.md` step 7 ("XL goes back to the EM
  to be split"), split into three pieces, build order 1→2→3: **Piece 1
  (this ticket, rescoped, `L`)** — structured order capture, itemized
  owner view, two automatic stages, no pricing shown; proceeds now. **Piece
  2** (package/price-book + tiered pricing, `L`, depends on Piece 1) and
  **Piece 3** (owner edit/resend + view tracking, `M`–`L`, depends on
  Pieces 1–2) are named in the PRD's Recommendation section but
  deliberately **not filed** — they're the approver's to confirm via this
  G1 before either gets a ticket id, and Piece 2 specifically waits on a
  named answer for who maintains each restaurant's price book. Not filing
  them now isn't scope-timidity: `next_id` stays `ENG-027`, unclaimed,
  until the approver has actually seen the split.

  Also resolved, as a rider rather than a blocking question: the rewrite's
  own stage matrix names three target stages but its enum-update
  instruction names only two — evidence-resolvable, not a 50/50 pick, since
  the rewrite also deletes the tokenized link the third stage
  (`Quote Viewed`) depends on. Building the two the rewrite's own enum
  instruction names; `Quote Viewed` moves to Piece 3, named plainly as a
  rider on the fresh G1 rather than silently dropped or silently guessed —
  did not meet this board's bar for a blocking question (`ENG-013`'s
  precedent) since the evidence, not a coin flip, decides it.

  PRD rewritten in place (`agents/product-manager/specs/ENG-016-catering-
  quote-generator.md`) — original Readback/Evidence kept as history, a new
  "Approver's `changed` response" section added with the four load-bearing
  code corrections the rewrite's own assumptions don't hold up against, and
  Problem-through-Decision replaced with Piece 1's scope. Fresh G1 raised:
  `inbox/2026-09-02-eng016-g1-rescope.md`. **No dissent section** —
  `agents/critic/agent.md` still doesn't exist at department or instance
  level, same gap `ENG-017`'s G1 already logged; not re-filed as a second
  proposal, the open one (`proposals.md`, 2026-08-25) already covers it.
  Notified and stamped (see `traces/eng-notify-2026-09-02.log`).
  Decision-journal entry written for the `changed` verdict.

  **0 transitions** — `awaiting-scope → awaiting-scope`, still owned by the
  approver throughout; this pass answered the gate return, it didn't move
  the ticket. `machine_wip` unaffected. Approver-facing WIP: this ticket's
  G1 rejoins the count (it was flagged "answered, not counted" while
  unactioned; now unanswered again) — same precedent tonight's
  `ENG-008`/`ENG-009`/`ENG-010` merge-request re-raises already set: a
  ticket's own gate cycle continuing is not a fresh To-do-column start, so
  it isn't blocked by the WIP-2 cap being over, but it does count once
  raised.

  `chained: none` — `awaiting-scope`, owned by the approver; the chaining
  guard doesn't fire on a ticket waiting on a human. Post-pass
  `lib/eng-gate-check.sh`, whole-board: see below.

- `2026-09-03` **`awaiting-scope → designed`, `owner: approver → architect`**
  (`decision` event pass, context
  `inbox/2026-09-02-eng016-g1-rescope.md`). Reading map for `decision`:
  steps 4 and 8c, plus step 6 (this answer advances the ticket into a
  machine-owned state) and the not-negotiable set (step 1, 7, 8b, 9, 10;
  *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check clean
  (repo-root `.env` → `MODE=active`; instance `config/config.yaml` →
  `mode:` empty, falls back to the global switch). Pre-pass
  `lib/eng-gate-check.sh`, scoped (`ENG-016`) and whole-board: both exit 0,
  clean.

  **The answer:** `approved` (`decided: 2026-09-03T15:47:46.139489+00:00`).
  Full text: "Lets start with piece 1" (sic). No comment on either rider
  this G1 carried (the 3-vs-2 stage-count resolution; the fulfillment-value
  remap question) — read as silence, not objection, so both stand as
  proposed. Read as confirming the recommended build order, not as
  pre-authorizing Pieces 2 or 3 — neither is filed by this answer, and
  Piece 2 still waits on a named answer for who maintains each
  restaurant's price book.

  PRD `status: approved`, `decided:` stamped
  (`agents/product-manager/specs/ENG-016-catering-quote-generator.md`, `##
  Decision` section filled in). Journal entry written
  (`agents/eng-manager/config/decision-journal.md`). Gate item's own `##
  Decision` footer filled in and the file moved
  `inbox/2026-09-02-eng016-g1-rescope.md` →
  `inbox/_handled/2026-09-02-eng016-g1-rescope.md`.

  **Machine WIP re-checked fresh from every ticket's own frontmatter, not
  the cached board header:** `1/1`, occupied by `ENG-024`
  (`ready-to-ship`, not yet `shipped`). Irrelevant to this transition —
  `designed` sits outside the counted `ready`..`ready-to-ship` range;
  shaping/design work is backlog grooming regardless of who holds the
  slot (`eng_build_loop.md` step 6). The architect's own tech-design pass
  will hit that same cap if it reaches step 11's "otherwise → `ready`"
  route before `ENG-024` ships — not pre-empted here, since the design
  work itself (steps 1–10) isn't gated, only entry to `ready` is.

  **1 transition** (`awaiting-scope → designed`), well under the cap of 4
  — the actual design work is the architect's own next hop, not attempted
  inline here, same precedent `ENG-015`'s identical G1-approved hand-off
  already set. **Consequence:** ticket now owned by `architect`, outside
  both the machine-WIP and approver-WIP counted ranges. Approver-facing
  WIP uncapped (`wip.approver_limit: unlimited`); this G1 drops off the
  "Waiting on the approver" list — same shape `ENG-013`'s question closing
  already set.

  **Dead-end sweep (scoped to this event):** no other ticket touched, per
  this event's own narrower contract (act on the answered gate item,
  advance only the ticket it belongs to).

  **Notify sweep:** nothing raised this pass — no new gate item written
  (Pieces 2/3 remain unfiled by the approver's own answer, Piece 2
  explicitly held). Nothing else nudged — out of this event's own scope.

  **Observations/proposals filed:** two observations (`observations.md`).
  First — the board index's cached priority column disagrees with several
  other tickets' own frontmatter (`ENG-019`/`ENG-020`/`ENG-021`/`ENG-026`/
  `ENG-027`, all actually `priority: now` on disk), noticed while
  re-checking dispatch order for this ticket. Same root cause the open
  2026-09-01 proposal on this file already names (the In-flight table
  needs regenerating from each ticket's own frontmatter, not hand-kept);
  not re-filed as a new proposal, and not corrected in `_index.md` by this
  pass — out of this event's own "advance only the ticket it belongs to"
  contract. Second — firing this pass's own `continue ENG-016` chain (see
  below) found `traces/.pending` 16 events deep; not investigated, queue
  depth is reference territory, not a normal pass's job, full detail on
  the observation itself.

  Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-016`) and whole-board:
  both exit 0, clean.

  `chained: ENG-016` — `designed` is agent-owned (`architect`, via
  `tech-design/SKILL.md`, triggered by this exact state); not the
  approver, not blocked, not terminal, not held by a cap (design work is
  backlog grooming, exempt from the machine-WIP slot `ENG-024` still
  occupies). Fired
  `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-016`
  before this pass exits.

  business-os itself left uncommitted — same standing default every pass
  has used; the commit-convention question remains open, not re-decided
  here.
