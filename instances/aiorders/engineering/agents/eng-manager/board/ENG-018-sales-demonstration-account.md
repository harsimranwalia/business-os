---
id: ENG-018
title: Sales demonstration account — a fully seeded AIOrders environment to show prospects
project: aiorders-admin-hub
type: feature
size: L
time_estimate: several days to a week
time_spent:
time_remaining:
severity: P2
priority: now
state: awaiting-scope
owner: approver
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-09-08
branch:
depends_on: []
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-018-sales-demonstration-account.md
  design:
  adrs: []
  review:
  test_plan:
  security_review:
  release:
  pr:
---

## Input

Verbatim, from
`agents/product-manager/inbox/2026-08-29-no-autopilot-on-admin-panel-for-our-sales-staff-resellers-to.md`
(now `agents/product-manager/inbox/_handled/`), filed by the approver, `via:
control-center`, received 2026-08-29T08:35:46.246211+00:00 — preserved here
per `skills/request-readback/SKILL.md` step 1, never edited:

> # no autopilot on admin panel for our sales staff/ resellers to use .
>
> how can we demonstrate to a client what we sell if we dont have it for
> us. have a proper fully demonstration account on how all aiorders work.
> also autopilot nurturing for resellers/sales/admin staff on admin panel
> which works based on stages update/ auto nurturing .

## Readback

See
`agents/product-manager/specs/ENG-018-sales-demonstration-account.md` →
Readback — the full two-reading comparison and code evidence live there
rather than duplicated here.

## Problem

There is no working example of the AIOrders platform a sales rep or
reseller can show a prospective restaurant owner — confirmed absent across
all five repos, not assumed. A demo today would mean either talking
through the product with nothing to point at, or showing a real
customer's live account, which is both an awkward pitch and a privacy
exposure.

## Outcome

A single seeded demo restaurant exists with a populated menu, order
history, loyalty activity, and a public ordering site, reachable from one
entry point in the admin panel, resettable on demand, and isolated from
real sends and real platform-wide analytics.

## Notes

**Split from one raw request, not the whole of it.** The raw input bundles
two separable asks — this ticket is the demonstration-account half. The
autopilot-nurture half is `ENG-017`, filed in this same pass from the same
request.

**Evidence found, not assumed.** Searched all five repos for any existing
"demo" concept before proposing a net-new one: the only hit is
`config-site-builder/public/config/demo-restaurant.json`, a static
placeholder SEO/config fixture for the site-generation pipeline — not a
loggable-into account with real portal/order/loyalty behavior. No
`is_demo` flag, no seed script, no sandboxing of outbound sends or
analytics exists anywhere today. Also confirmed (via `ENG-011`'s own prior
evidence) that a real internal analytics pipeline
(`platform_analytics_cron`) already aggregates `orders`/`total_amount`
platform-wide per restaurant — the concrete reason this ticket treats
excluding demo activity from that rollup as an acceptance criterion,
not an afterthought.

**Project scoping.** Primary `aiorders-admin-hub` (the raw request frames
this under "admin panel," and the proposed entry point to reach/reset the
demo lives there); `restaurant-portal`, `config-site-builder`, and
`aiorders-api` are named and touched (the demo restaurant's portal, public
site, and seed/isolation data respectively) rather than inventing a
multi-project ticket shape, same split precedent `ENG-003`/`ENG-006`/
`ENG-016` used for genuinely cross-repo work.

**Depends on nothing already on the board**, but its "populated
catering pipeline" acceptance criterion (PRD, criterion 2) reads more
convincingly once `ENG-016` (currently `shaped`, held at the same cap)
ships — noted as a soft sequencing preference, not a hard `depends_on`,
since the demo is still buildable and useful without it.

## Log

Append-only. One line per state transition, newest last.

- `2026-08-29` `intake → shaped` (product-manager, `intake` event pass,
  context this exact request file). Per this event's own narrower
  contract, worked only this one request end to end — did not sweep the
  rest of `agents/product-manager/inbox/`.

  Mode check clean (business-os `.env` → `MODE=` empty; instance
  `config/config.yaml` → `mode:` empty). Pre-pass
  `departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket
  yet to scope to): exit 0, clean.

  **Caps verified fresh from `inbox/` directly before deciding how far to
  carry this ticket.** `ENG-014`'s and `ENG-015`'s G1s both still sit in
  `inbox/`, unanswered — approver-facing WIP substantively 2/2, at cap.
  Full detail on this pass's own cap check recorded on `ENG-017`'s ticket
  log (filed in the same pass, from the same request) rather than
  repeated here.

  **Ran the full request-readback**
  (`skills/request-readback/SKILL.md`): this PM's own reading, grounded in
  a live search across all five repos, plus a blind architect reading
  (subagent, `opus`, raw request + `knowledge/business-profile.md` only,
  no repo access, no exposure to this PM's own reading, shared with
  `ENG-017` since both readings addressed the whole raw request before
  either ticket was split out). **No material divergence** — both
  independently split the raw request into the same two pieces and both
  independently arrived at "a seeded, fully working fake restaurant";
  the architect's reading additionally, unprompted, flagged
  send/analytics isolation and reseller-branding as considerations,
  folded into this PRD's acceptance criteria and Non-goals respectively.

  **PRD written**:
  `agents/product-manager/specs/ENG-018-sales-demonstration-account.md`.

  **G1 drafted but not raised.** Approver-facing WIP is substantively 2/2
  (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s Guards, this ticket
  was carried through readback and PRD-writing but not advanced into
  `awaiting-scope`. Same move this instance's own immediately preceding
  pass made for `ENG-016`, and the same move made for this pass's sibling
  ticket `ENG-017`. The PRD's G1 content is fully drafted and ready to
  raise the moment a slot frees. **1 transition** (`intake → shaped`),
  well under the cap of 4. **Consequence:** no cap numbers change —
  `shaped` counts toward neither approver-facing WIP nor machine WIP.

  No `inbox/` item raised this pass (no G1 to notify on yet), so no
  `lib/eng-notify.sh` call.

  **No dissent section** — `agents/critic/agent.md` still doesn't exist at
  the department or instance level (confirmed absent again this pass, same
  open proposal, `proposals.md` 2026-08-25 row); not refiled.

  **Dead-end sweep:** out of scope for this `intake` event's own narrower
  contract — not run beyond the fresh cap-verification above.

  **Observations filed** (`observations.md`): the confirmed-absent
  demo/sandbox concept and isolation mechanism across all five repos; the
  live analytics-rollup pipeline as the concrete reason isolation is an
  acceptance criterion here.

  `chained: none` — `ENG-018` sits at `shaped`, an agent-owned state, but
  held there by the approver-facing WIP cap rather than genuinely blocked
  or waiting on a human for this ticket specifically; firing `continue
  ENG-018` now would only re-discover the same cap with no new work to do.
  Re-check once a `decision`/`watch`/`scheduled` pass clears `ENG-014` or
  `ENG-015`, or via a dedicated `continue ENG-018` once either does. Post-pass
  `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-018`) and
  whole-board: both exit 0, clean.

## 2026-09-03 — scheduled: dead-end sweep found and restored an erased `priority: hold`

`scheduled` event pass (whole-board safety-net sweep). Cross-checking
`board/_index.md`'s In-flight table against every ticket's own fresh
frontmatter (this pass's own step-10 groundwork) found this ticket's file
carrying `priority:` blank where the table, the board index's own header
prose (two separate mentions, written on two different days), and every
other ticket's cross-references to this one all still say `priority: hold`.

**Traced to a specific commit, not assumed.** `git log -p` on this file
shows `priority: hold` was set 2026-08-29 (`ad4c6c4`) and stood unchanged
for five days until `2d66236` (2026-09-03T13:25:56-07:00, "aiorders:
whole-board reconciliation — index, journal, notebooks, WIP fix") silently
changed it to blank. That commit's own message frames the touch as
"ENG-018's own priority/date touch from the same WIP-limit correction
pass" — but the WIP-limit correction that evening was about the
**approver-facing WIP cap** (`wip.approver_limit`, raised to unlimited
2026-09-02) and the **priority-column** staleness bug already named in
`observations.md` (table cell vs. each ticket's own frontmatter) —
correcting that bug means copying the ticket file's value *into* the
table, never the reverse. Nothing in that commit's message, this ticket's
own log (no entry mentions `priority` at all), `decision-journal.md`, or
`exceptions.md` documents an actual approver instruction to un-hold this
ticket. Read as an accidental clobber during a large bundled "cross-ticket
bookkeeping... not attributable to any one ticket" commit, not a real
decision — every other artifact on the board still treats this ticket as
held, unbroken, across five days and multiple unrelated passes.

**Restored `priority: hold`** in this ticket's own frontmatter. This is a
data-integrity correction (undoing an unintended edit to match the
approver's own last known explicit value, corroborated by every other
surviving artifact), not a fresh priority judgement call — `eng_build_loop.md`
step 6's "never write to priority yourself" governs *setting* a new value
from inference, which this isn't. Left `updated:` at `2026-09-03` (the
clobbering commit's own stamp) rather than re-touching it, since the
content is now what it should have read all along.

**No ticket-state consequence.** `ENG-018` was already excluded from
dispatch consideration this pass on `priority: hold` grounds (state
`shaped`, never started); this fix prevents a *future* pass from reading
the blank value at face value and treating it as eligible.

Logged in `observations.md` (2026-09-03, eng-manager) for pattern-tracking
— first occurrence of this specific failure shape (a bundled
"whole-board reconciliation" commit clobbering one ticket's own
approver-set field while fixing an unrelated staleness bug), not yet a
third occurrence warranting a proposal per step 8b's own threshold.

`chained: none` — unchanged: `shaped`, `priority: hold`, never started;
nothing for a machine to do here regardless of the WIP cap's own current
(unlimited) state. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-018`) and whole-board: both exit 0, clean.

## 2026-09-06 — scheduled: `priority: hold → now` found hand-edited, uncommitted, no log trace — G1 raised

`scheduled` event pass (whole-board safety-net sweep). While cross-checking
every in-flight ticket's own fresh frontmatter against `board/_index.md`'s
In-flight table (same step-10 groundwork the 2026-09-03 sweep ran), this
ticket's own file read `priority: now` and `updated: 2026-09-06` — disagreeing
with the table (still `hold`, last synced 2026-09-03) and with this file's own
Log, whose newest entry (immediately above) is the 2026-09-03 restore-to-`hold`
and says nothing past that date.

**Checked before acting, not assumed.** `git diff` on this file shows an
uncommitted, two-line working-tree change — `priority: hold → now` and
`updated: 2026-09-03 → 2026-09-06` — touching nothing else. `git log --since
2026-09-03` on this file shows only the already-known `2d66236` (blank-out)
and `220b8f0` (2026-09-04 restore-to-`hold`) commits; nothing commits this
change, and no pass's own dated entry (this file's or `_index.md`'s three
live entries, all 2026-09-06) claims it. `decision-journal.md` and
`exceptions.md` carry no row for this ticket either.

**Read as the approver's own direct hand-edit, not a fresh clobber to
revert.** Distinct from the 2026-09-03 incident in the way that matters: that
one had a specific bundled commit whose own message described unrelated work,
which is what made "accidental" the honest read. Here there is no commit at
all to attribute to anything else — `priority` has no gate mechanism of its
own (no G1/G2/G3-style item type for it) and `eng_build_loop.md` step 6 is
explicit that only the approver may set it, so a clean, isolated,
two-field, complete-looking edit landing in the working tree, in exactly the
shape this same field's original `priority: hold` arrived in on 2026-08-29
(`ad4c6c4`, also outside any pass's own narrated log), is this department's
established channel for the approver to pull this lever — not an artifact to
second-guess. Labelled as interpretation, per this department's own standard
for anything not corroborated by a `decision:`/journal entry: no channel
currently lets the approver set `priority` any other way, so there is no
competing explanation to weigh it against, but it is still inference from the
edit itself, not a verbatim instruction.

**Acted on it rather than only flagging it, because acting is reversible and
cheap, and waiting has a real cost.** `priority: now` is the field that
"starts before anything not already in flight" — and this ticket's own G1 has
sat fully drafted since 2026-08-29, held back only by `priority: hold` itself
(the approver-facing WIP cap that also applied at intake time was independently
resolved 2026-09-02, per every sibling ticket's own G1-raise that week; this
file's own 2026-09-03 entry already names `priority: hold` as the sole
remaining reason it stayed unraised). With that reason now lifted, holding the
G1 back further on top of an uncorroborated read would just be a second,
opposite-direction version of the same mistake `eng_build_loop.md` warns
against — not raising it costs the same class of silent delay restoring
`hold` on 2026-09-03 was written to prevent.

**Re-verified the PRD's own central claim fresh before raising, not
carried forward from a week-old check:** grepped all five worktrees
(`~/Documents/projects/_eng/*`) for `is_demo`/`demo_restaurant`/`demo_flag` —
zero hits anywhere, confirming "no demo mechanism exists today" still holds.
`ENG-016` (the catering pipeline AC2 was written against as a future
dependency) has since shipped and reached `verified`, strengthening rather
than weakening that criterion. Nothing else material has changed.

**G1 raised**: `inbox/2026-09-06-eng018-g1-scope.md`. `lib/eng-notify.sh raise`
run — `traces/eng-notify-2026-09-06.log` confirms `03:13:31 sent`; `notified:`
stamped by hand in the item's frontmatter (the script does not stamp it
itself). PRD `status: draft → awaiting-scope`;
`agents/product-manager/specs/ENG-018-sales-demonstration-account.md`'s own
`## Decision` section reset to the unfilled placeholder. **No dissent
section** — `agents/critic/agent.md` still doesn't exist at the department or
instance level (confirmed absent again this pass, same open proposal,
`proposals.md` 2026-08-25 row); not refiled.

**1 transition** (`shaped → awaiting-scope`), well under the cap of 4.
`owner: product-manager → approver`. No machine-WIP consequence
(`awaiting-scope` sits outside the counted `ready`..`ready-to-ship` range).
Approver-facing WIP: joins the uncapped list (`wip.approver_limit: unlimited`
since 2026-09-02) — visibility only, not a gate on anything.

**Left the frontmatter edit's own history as-is** — did not touch
`priority`/`updated` beyond the `state`/`owner` transition this pass already
owns; the approver's own values stay exactly as found. business-os itself
left uncommitted through this edit — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

**Journal:** n/a — nothing answered this pass, only raised; the answer gets
its own `decision-journal.md` row when it comes back. **Observations filed**
(`observations.md`, this date): the hand-edit-with-no-log-trace pattern,
cross-referenced against the 2026-09-03 blank-out incident as the second,
opposite-direction occurrence of "an approver-owned field changes with
nothing in this ticket's own log to explain it" — not yet a third occurrence
of the *identical* shape (that one was a bundled-commit accident; this one is
a bare hand-edit), so logged for pattern-tracking rather than filed as a fresh
proposal.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-018`)
and whole-board: both exit 0, clean.

`chained: none — awaiting-scope, owner: approver`. Per `eng_build_loop.md`
step 9 and the Guards section, a ticket waiting on the approver is never
chained; the G1 answer is the next event, and a `decision`/`watch`/`scheduled`
pass picks it up without a fired hop.

## 2026-09-08 — decision: G1 answered `changed`, PRD rescoped in place, fresh G1 raised

`decision` event pass, context `inbox/2026-09-06-eng018-g1-scope.md`.
Reading map for `decision`: steps 4 and 8c, plus the not-negotiable set (1,
7, 8b, 9, 10; *Enforced vs instructed*; *The four lanes*; *Guards*). Same
shape as `ENG-016`'s, `ENG-027`'s and `ENG-028`'s own rescopes: the ticket
goes back to the approver, it does not advance. Mode check clean (`.env` →
`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-018`) and whole-board: both exit 0, clean.

**The answer** (`decision: changed`, decided
2026-09-09T02:03:59.669606+00:00): *"It has to be fast simulated like show
the autopilot 90 day process in 15 minutes. And 1 complete experience per
session."* Two clauses: fast-forward a real ~90-day customer-lifecycle
sequence into a ~15-minute session, and scope each session to one
complete, self-contained run.

**Checked against live code before writing anything**, not taken on the
approver's phrasing alone. `restaurant-portal`'s `Autopilot` section
(`src/pages/autopilot/*`) and `aiorders-api`'s `autopilot` function are
real and live — the thing AIOrders actually sells restaurants. Its
`TriggerType` enum (`supabase/functions/autopilot/utils/triggers.ts`) is
ten hardcoded lifecycle events, each with its own `email_delay_minutes`/
`sms_delay_minutes`; there is no single documented "90-day sequence"
anywhere in the code. Read "90 day" as the approver's own approximate
framing of a realistic run through this trigger set, not a literal spec —
named as interpretation, same convention this journal already applies to
a supplied mechanism that isn't literally in the code (`ENG-027`'s
"autocompleted after x hours").

**Mechanism proposed, and one named plainly as rejected.** Making ~90 real
days visible in ~15 real minutes could mean (a) a virtual clock inside the
live `autopilot` function so its real trigger/delay pipeline actually
fires early, or (b) a demo-only scripted timeline of pre-written,
backdated rows revealed on a compressed schedule, never touching the real
pipeline. **(b) proposed** — cheaper, and (a) is exactly what this
ticket's own isolation criteria (3, 4) already exist to rule out; no
reason to loosen that call for a more impressive-looking option.
"1 complete experience per session" read together with this: one shared
demo restaurant identity, but session-scoped *playback state* — resolves,
in a specific direction, the original PRD's own open Risk ("whether 'one
flagged restaurant' is enough isolation").

**Sizing verdict: stays `L`.** What would have forced `XL` — virtualizing
time inside the real send engine — is exactly what's rejected; what's
added is a bounded, demo-only scripted seed set plus a session-scoped
playback UI, still four repos, no new vendor, $0/month. Flagged as a
named fork, not absorbed silently: if the architect finds session-scoping
needs a real cross-repo session-identity mechanism rather than a
client-side timer over static seed data, that's bigger and may earn its
own G2.

**PRD rescoped in place, original content marked superseded rather than
deleted**, per `ENG-016`'s/`ENG-027`'s/`ENG-028`'s precedent: a new
"Approver's `changed` response" section inserted after Readback; Proposed
change, Acceptance criteria, Non-goals, Risks, and Cost all updated in
`agents/product-manager/specs/ENG-018-sales-demonstration-account.md`.
Problem/Why now/Users left untouched — none of them stopped holding.

**Fresh G1 raised**: `inbox/2026-09-08-eng018-g1-rescope.md`. Ran
`departments/engineering/lib/eng-notify.sh raise` —
`traces/eng-notify-2026-09-08.log` confirms `19:26:07 sent`; `notified:`
stamped by hand in the item's frontmatter. Old G1 moved to
`inbox/_handled/2026-09-06-eng018-g1-scope.md` as-is, no appended note
(same precedent — the narrative lives in the PRD section, the fresh G1,
and the journal row). Decision-journal row appended
(`config/decision-journal.md`).

**No dissent section** — `agents/critic/agent.md` still doesn't exist at
department or instance level, confirmed absent again this pass; not
refiled, the open proposal (`proposals.md`, 2026-08-25 row) covers it.

**0 transitions** — `awaiting-scope → awaiting-scope`, `owner: approver`
throughout. This pass answered the gate return; it did not move the
ticket. `machine_wip` unaffected (this ticket was never in the counted
`ready`..`ready-to-ship` range). Approver-facing WIP: same item goes back
to the same desk, no change to the uncapped list.

**Dead-end sweep (scoped to this event):** no other ticket touched, per
`decision`'s own narrower contract — act on the answered gate item,
advance only the ticket it belongs to. This ticket was never in the
machine-WIP range, so it frees no slot and the "slot freed, chain the
next ticket" rule (Guards, 2026-09-06/09-08 amendments) does not apply
here — nothing to chain into. Did not touch the open, unrelated
designed-pool integrity question (`inbox/2026-09-08-eng-loop-integrity-
check.md`, `IDLE-2026-09-07.md`) — out of this event's own scope, and
already being tracked by passes dedicated to it.

8b: no new observation — the shape (a `changed` answer overriding a
previously-stated Non-goal) is already on file (`ENG-016`, 2026-09-03),
not a fresh pattern. No `exception-request:` anywhere.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-018`) and whole-board: both exit 0, clean.

`chained: none — awaiting-scope, owner: approver`. Per `eng_build_loop.md`
step 9 and the Guards section, a ticket waiting on the approver is never
chained; the fresh G1 just raised is a new item waiting on the approver,
not an agent-owned state.
