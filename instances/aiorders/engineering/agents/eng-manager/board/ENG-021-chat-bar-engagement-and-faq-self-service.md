---
id: ENG-021
title: Website chat-bar engagement visibility — customer questions and self-service FAQ editing on the brand portal
project: restaurant-portal
type: feature
size: M
time_estimate: a day to a day and a half
time_spent:
time_remaining:
severity: P2
priority: now
state: verified
owner: eng-manager
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-09-07
branch:
depends_on: [ENG-022]
blocks: []
parent:
links:
  prd: agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md
  design: agents/architect/designs/ENG-021-chat-bar-engagement-and-faq-self-service.md
  adrs: [ADR-013, ADR-014]
  review:
  test_plan:
  security_review:
  release:
  pr:
touches_data: true
touches_models: false
---

## Problem

Restaurant owners can't see that customers are using the AI chat/search bar on
their website, and have no way to turn a real customer question into a better
FAQ answer — even though every question is already logged per-restaurant and
the database already grants the owner's own account read access to it. The
FAQ content the bot answers from is staff-only to edit today; the brand
portal has no editor for it at all.

## Outcome

A restaurant owner, on the brand portal, can see the real questions customers
asked their chat bar (their own restaurant only), and create or edit a
website FAQ entry directly from that view — writing to the same data the bot
already reads, so the fix takes effect on the next customer question, with no
staff involvement required.

## Notes

Grounded in a live-code investigation across four repos before writing the
PRD — see `agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`
Readback for the full comparison. The load-bearing facts for whoever designs
this next:

- The widget is `config-site-builder`'s `AISearchBar`/`ChatPanel`, rendered
  site-wide via `Layout.tsx` behind a per-restaurant `showAIChat` flag —
  live today, not hypothetical.
- Every turn is written by `aiorders-api`'s `ai-search-openrouter` edge
  function to `ai_conversations` (`session_id`, `restaurant_id`, `messages`
  jsonb, timestamps) — one row per session, full transcript in `messages`,
  not one row per question.
- `ai_conversations` already carries an RLS policy titled "Restaurant
  managers can view their restaurant conversations" (`restaurant-portal`
  migration `20250903152559_...sql`) — the read-access grant for this exact
  feature already exists and nothing reads it.
- The bot's FAQ source is `restaurant_website.faqs`, edited today only in
  `aiorders-admin-hub`'s `RestaurantAIWebsite.tsx` via direct Supabase
  `.from('restaurant_website')` calls — no edge function in the write path.
  `restaurant-portal` has a same-named but **unrelated** FAQ list
  (`CateringFaq`, in `CateringPageForm.tsx`) scoped to the catering landing
  page only — do not confuse the two or wire the new editor to the wrong
  field.
- `restaurant-portal` already reads/writes `restaurant_website` directly
  today for a different section (`src/pages/hiring/Index.tsx`, careers
  content) — that's the precedent pattern for the new FAQ editor, and
  evidence (not proof — the literal RLS policy on `restaurant_website` was
  not read) that the owner's account can already write to this table.
- No "answered / unanswered" or confidence signal is stored anywhere today —
  don't assume one exists when designing the questions view.
- A `cleanup_old_ai_conversations` DB function exists (referenced in
  generated Supabase types) but its definition/schedule isn't in any of the
  four repos' migrations — likely configured directly in the database.
  Retention isn't something this ticket controls either way.

## Breakdown

Decomposed 2026-09-05 (`work-breakdown/SKILL.md`) into two sub-tickets, one
per owning agent, sequenced by the design's own Rollout order (API before
portal):

| Sub-ticket | Surface | Repo | Depends on | State |
|---|---|---|---|---|
| `ENG-040` | backend | `aiorders-api` | — | `building` |
| `ENG-041` | frontend | `restaurant-portal` | `ENG-040` | `ready` |

No `database` sub-ticket — this design has no schema change; `database`'s
role (a read-only RLS/retention/volume check against the live project) is
folded into `ENG-041`'s own Notes as a required first build step instead of a
ticket of its own. This parent carries no diff of its own from here on — its
evidence is its children's (ADR-003-class exemption). It moves directly to
`shipped` once both children reach `shipped`/`verified`/`dropped` with at
least one `shipped`/`verified`, without itself passing through
`in-review`/`in-qa`/`in-security`. Full reasoning — the surface split, why no
`database` ticket, the sequencing call, the AC-ownership mapping, and every
field decided without an explicit rule — is in
`agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`.

## Log

- 2026-08-29 `intake → shaped` (product-manager) — sized M, project
  `restaurant-portal`. Ran the full request-readback
  (`skills/request-readback/SKILL.md`): this PM's own reading, grounded in
  live code across `config-site-builder`, `aiorders-api`,
  `aiorders-admin-hub`, and `restaurant-portal` (all four worktrees already
  present on this host at `~/Documents/_eng/`, per `ENG_WORKTREES`
  resolution — no worktree creation needed this pass); a blind architect
  reading (subagent, opus, raw request + `knowledge/business-profile.md`
  only, no repo access, no exposure to this PM's own reading). **No material
  divergence** — both independently converged on the same core shape:
  capture → surface to the owner → act via FAQs, on the brand portal. Full
  comparison in the PRD's Readback section.
  **Caps checked fresh from `inbox/` directly, not the cached board header:**
  found `ENG-014`'s and `ENG-015`'s G1s (`inbox/2026-08-29-eng014-g1-scope.md`,
  `inbox/2026-08-29-eng015-g1-scope.md`) both now carry `decision: approved`
  (decided 15:54:50 and 16:12:24 respectively) — answered, but neither
  ticket's own frontmatter has been advanced past `state: awaiting-scope,
  owner: approver` yet by a `decision` pass. Per this event's own narrower
  contract (act on the intake card given, not the whole board) this pass
  does not process those two decisions itself — that's a `decision` event's
  job and appears to already be in flight independently. For this ticket's
  own purposes, treated conservatively as **still occupying both
  approver-facing WIP slots** (mechanical ticket state, not the answered-but
  -unprocessed G1 text) — logged as an observation for the dead-end/decision
  sweep rather than acted on here. Approver-facing WIP therefore read as
  2/2, at cap, going into this pass.
  **Held at `shaped`, not advanced to `awaiting-scope`** — same reason and
  same move as `ENG-020` earlier today: nothing new should start down a path
  that needs the approver until `ENG-014` or `ENG-015` actually clears.
  G1 content (readback, both readings, non-goals, recommendation) is fully
  drafted in the PRD's Decision section and ready to raise the moment a slot
  frees. 1 transition (`intake → shaped`), well under the 4-transition cap.
  No `inbox/` item raised this pass (no G1 yet), so no `lib/eng-notify.sh`
  call. `chained: none` — held by the approver-facing WIP cap, not blocked
  or waiting on a human for this ticket specifically; re-check once a
  `decision`/`watch`/`scheduled` pass actually clears `ENG-014` or `ENG-015`.

## 2026-09-03 — scheduled: G1 raised — `shaped → awaiting-scope`

Same stale premise as `ENG-019`/`ENG-020` (see `ENG-019`'s own dated entry
for the full derivation): the approver-facing WIP cap this ticket was held
behind no longer exists — this instance's own `config/config.yaml` raised
`approver_limit` to `unlimited` on 2026-09-02, by the approver's own
explicit decision, never checked by any pass that held this ticket at
`shaped`. Readback already converged (no material divergence), so straight
to G1.

Wrote `inbox/2026-09-03-eng021-g1-scope.md` (recommendation: build now,
scoped to surfacing chat-bar questions plus a self-service FAQ editor,
exactly as the PRD proposes). `lib/eng-notify.sh raise` called, exit 0
(logged `sent: active`, the already-tracked `MODE`-clobber bug, not
re-filed). Stamped `notified: 2026-09-03T11:56:44`.

**1 transition** (`shaped → awaiting-scope`). **Consequence:** no
machine-WIP change. Approver-facing WIP uncapped, so this adds to the queue
without displacing anything — `owner` moves `product-manager → approver`.

`chained: none` — `awaiting-scope` is one of the documented no-chain
conditions (waiting on the approver).

## 2026-09-03 — decision: G1 approved — `awaiting-scope → designed`

`decision` event pass, context `inbox/2026-09-03-eng021-g1-scope.md`. Reading
map for `decision`: steps 4 and 8c, plus step 6 (this answer advances the
ticket into a machine-owned state) and the not-negotiable set (step 1, 7, 8b,
9, 10; *Enforced vs instructed*, *The four lanes*, *Guards*). Mode check clean
(repo-root `.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-021`) and whole-board: both exit 0, clean.

**The answer:** `approved` (`decided: 2026-09-03T15:54:34.623417+00:00`). No
additional comment. Read as accepting the recommendation exactly as scoped —
customer questions surfaced on the brand portal plus a self-service FAQ editor
writing the same `restaurant_website.faqs` table the bot already reads from;
scoring answer quality, clustering questions, a staff-facing admin-hub mirror,
and any change to the chat bar's own runtime behavior all named as later,
separate work — and as accepting every item in the readback's "Assumed,
correctable here" list since none was corrected. Full reasoning on `ENG-021`'s
own PRD, not repeated here.

`ENG-021` moved `awaiting-scope → designed`, `owner: approver → architect`.
PRD `status: approved`
(`agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`).
Journaled (`decision-journal.md`). Gate item's `## Decision` footer filled in
and moved to `inbox/_handled/`.

**Risks named in the PRD stay open, inherited by the architect at `designed`,
not resolved by this approval:** PII in free-text customer questions (the
owner is arguably the right custodian of their own customers' data, but the
security gate should look at this plainly rather than it being an accident of
shipping a log viewer); RLS on `restaurant_website` assumed from a sibling
page's (`hiring`) behavior, not read literally — confirm the actual policy
before relying on it; retention window and per-restaurant query volume both
unknown, worth a quick check at design time rather than a guess here. Restated
here so the `continue ENG-021` hop below doesn't have to re-derive them from
the PRD alone.

Machine WIP re-checked fresh from every ticket's own frontmatter, not the
cached header: still `1/1`, occupied by `ENG-024` (`ready-to-ship`, not yet
`shipped`) — irrelevant to this transition, since `designed` sits outside the
counted `ready`..`ready-to-ship` range and shaping/design work is backlog
grooming regardless of who holds the slot. Handed to the architect for the
tech design itself (a `continue ENG-021` session) rather than attempted
inline, same precedent `ENG-020`'s, `ENG-019`'s, `ENG-026`'s and `ENG-016`'s
identical G1-approved hand-offs already set.

**1 transition** (`awaiting-scope → designed`), well under the cap of 4.
**Consequence:** approver-facing WIP drops by one item — this G1 drops off the
"Waiting on the approver" list, same shape `ENG-013`'s, `ENG-016`'s,
`ENG-026`'s, `ENG-019`'s and `ENG-020`'s closures already set. Machine WIP
unaffected (`designed` sits outside the counted range).

**Dead-end sweep (scoped to this event):** no other ticket touched, per this
event's own narrower contract (act on the answered gate item, advance only
the ticket it belongs to). **Two things noticed while in `inbox/`, filed to
`observations.md` rather than acted on here, since both belong to a different
ticket than this event's own:** `ENG-027`'s own G1
(`inbox/2026-09-03-eng027-g1-scope.md`) now carries `decision: changed`
(`decided: 2026-09-03T16:00:32`) — a separate ticket's gate, not this event's
to process. `inbox/2026-09-03-eng-loop-stalled.md` (incident, `ticket:
ENG-024`) carries no `notified:` stamp at all and no `## Decision` section,
timestamped 06:37 this morning — likely stale, since multiple passes have
clearly run since (this one included), but not re-derived or closed here,
out of this event's own scope.

**Notify sweep:** nothing raised this pass — no new gate item written.
Nothing nudged: `ENG-008` (~16h45m since `notified:`), `ENG-010` (~22h25m)
and `ENG-022` (~14h43m) are all still under the 24h threshold; `ENG-015`
(~6h6m) and the just-raised `ENG-028` are far under it; `ENG-009` already
carries its one-ever nudge.

**Observations/proposals filed:** the two items named in the dead-end sweep
note above.

**Board update** — In-flight table's `ENG-021` row (`state`, `owner`,
`updated`); header's approver-facing bullet, "unanswered items" paragraph and
count, "Waiting on the approver" section's `ENG-021` paragraph and item
count. Rolled the oldest of the four now-live dated entries (`decision
(ENG-026 G1)`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both
exit 0, clean.

`chained: ENG-021` — `designed` is agent-owned (`architect`, via
`tech-design/SKILL.md`, triggered by this exact state); not the approver, not
blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-021` before
this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

**Addendum, same date, resumed pass:** the paragraphs above were written by
this event's first attempt, which hit the session's rate limit immediately
after writing them (`traces/eng-loop-2026-09-03.log`, `pass FAILED (exit 1,
379s)`, re-queued) — this ticket's own frontmatter/log update landed on disk,
but nothing past it did: the gate item was still sitting unmoved in `inbox/`,
no `decision-journal.md` row existed, the PRD's frontmatter/`## Decision`
section were untouched, `_index.md` still showed `awaiting-scope`/`approver`,
and no `.hops-2026-09-03-ENG-021` trace existed — meaning `continue ENG-021`
had not actually been fired despite the paragraphs above already narrating it
as done. This resumption verified every claim above against the underlying
files before trusting it (all accurate), then completed what the crash
skipped: gate item processed-note appended and moved to `inbox/_handled/`,
`decision-journal.md` row added, PRD frontmatter/`## Decision` filled in,
`_index.md` synced, and `lib/eng-trigger.sh continue ENG-021` fired for
real. No re-derivation of the decision itself was needed — only completion of
the mechanical steps the first attempt narrated but didn't reach.

## 2026-09-03 — continue: design pass — stays `designed`, held by machine WIP + a new dependency

`continue` event pass, context `ENG-021`. Reading map: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped and whole-board: both exit 0.

Ran `tech-design/SKILL.md`: gathered evidence across all four repos myself,
then dispatched design judgment and write-up to an `opus` subagent per the
skill's own model header, same split `ENG-016`'s/`ENG-020`'s passes used.

**Design:** `agents/architect/designs/ENG-021-chat-bar-engagement-and-faq-self-service.md`.
**Two ADRs** (`ADR-013`, `ADR-014`, both `decided_by: architect`, `_index.md`
→ `ADR-015`). **No one-way doors.** `touches_data: true` (no schema change —
`database` does a read-only live-project RLS check), `touches_models: false`.
Corrects a wrong PRD assumption: the write goes through `brand-portal`'s
existing `update_website_content` action (widen `EDITABLE_PAGES` by one), not
a direct client write — so `restaurant_website`'s untracked RLS never becomes
load-bearing. Full reasoning, alternatives, failure modes: the design itself;
process notes and my own independent verification of the finding below:
`agents/architect/notebook/2026-09-03-eng021-design.md`.

**New finding, verified independently, not just taken from the subagent:**
this design edits `brand-portal/website.ts`, whose ownership check is
currently defeated (`ENG-022`, P0, `blocked`/`approver`, PR #9, confirmed via
`git merge-base --is-ancestor` **not** merged into `origin/main`) — and that
same branch rewrites the identical two call sites in `website.ts`. Set
`depends_on: [ENG-022]` on this ticket's frontmatter myself (architect's own
technical-sequencing call, not `priority`). One observation filed
(`observations.md`): `ENG-014`'s `owner: eng-manager`/`state: designed`
mismatch, found while confirming today's owner-stays-`architect` convention.

**Routing:** would be `ready` — held at `designed`, `owner: architect`
(unchanged), per today's `ENG-020` convention. Machine WIP re-checked fresh:
`1/1`, `ENG-016` (`ready`). Even once that frees, `ENG-021` still can't enter
`ready` until `ENG-022` merges — both reasons now govern this ticket's hold,
not just the cap.

**Dead-end sweep:** out of scope for `continue` (narrower contract). **Notify
sweep:** nothing raised — no gate opened this pass.

**Board update** — header's Machine-WIP paragraph (`ENG-021` added to the
held-for-slot list, `depends_on: [ENG-022]` noted); In-flight row unchanged
(state/owner didn't move). Rolled the oldest of the four live dated entries
(`continue ENG-016`) to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped and whole-board: both exit 0.

`chained: none` — held by the machine-WIP cap (`1/1`, `ENG-016`, `ready`) and,
independently, by `depends_on: [ENG-022]` (unmerged P0); neither the approver
nor blocked nor terminal, but two of the documented no-chain conditions apply
at once. Re-check once `ENG-016` ships **and** `ENG-022` merges.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-04 — scheduled (whole-board sweep): stays `designed` — `depends_on: [ENG-022]` now satisfied, machine WIP the sole remaining hold

`scheduled` event pass, whole-board sweep. This ticket wasn't itself the
source of new work this pass (no gate answered, no merge for its own
branch — it has none yet), but the board index's own header paragraph
about it had gone stale: it still read `ENG-022`'s branch as "unmerged,"
when `ENG-022` shipped and reached `verified` in an earlier pass tonight.
Checked fresh against `ENG-022`'s own board file (`state: verified`) before
correcting the header text, rather than trusting either account on faith.

**No frontmatter change** — `depends_on: [ENG-022]` stays recorded as
history (the technical-sequencing call that was made, not undone now that
it's satisfied), and `state`/`owner` are unchanged: the machine-WIP cap
(`1/1`, held by the `ENG-016` family) was always this ticket's other,
independent hold, and remains the sole one now. This ticket does not enter
`ready` from this pass — that would be a fresh dispatch decision requiring
a free slot, which step 6 confirmed doesn't exist this pass.

`chained: none` — held by the machine-WIP cap alone now; re-check once the
`ENG-016` family reaches `shipped`.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-05 — scheduled: claimed the free machine-WIP slot — `designed → ready`

`scheduled` event pass, whole-board sweep. Reading map for `scheduled`: the
whole document (never narrowed). Mode check clean (repo-root `.env` →
`MODE=active`). Pre-pass `lib/eng-gate-check.sh`, whole-board: exit 0, clean.

Machine WIP re-checked fresh from every ticket's own frontmatter, not the
cached board header: `0/1`, free — `ENG-020` left the counted `ready`..
`ready-to-ship` range earlier today (`ready-to-ship → blocked` at its own
release-readiness hop) and no pass since picked a replacement. To-do column
(`intake`/`shaped`/`awaiting-scope`) swept fresh: `ENG-018` stays excluded
(`priority: hold`); `ENG-028` is the only other occupant and its G1
(`inbox/2026-09-03-eng028-g1-scope.md`) is still unanswered — genuinely
waiting on the approver, not machine-actionable. Nothing there to start.

Fell back to the held-for-slot pool, same precedent `ENG-019`'s and
`ENG-020`'s own dispatches already set today: `designed` tickets with a
completed design and no one-way door, deferred only by the cap. Candidates
carrying `priority: now`: this ticket, `ENG-026`, and `ENG-027`. **This
ticket's own `depends_on: [ENG-022]` is satisfied** (`ENG-022` verified,
re-confirmed fresh from its own board file, not assumed from this ticket's
2026-09-04 note) — no other hold recorded. Lowest id decided: `ENG-021`.

Re-confirmed this ticket's own design output directly rather than trusting
the pool description: `agents/architect/designs/ENG-021-chat-bar-engagement-and-faq-self-service.md`
exists, the 2026-09-03 design-pass log above states **No one-way doors**
plainly, and `tech-design/SKILL.md` step 11 routes exactly that case to
`ready`, owner `eng-manager`, no G2 — matching what this ticket's own prior
log already anticipated ("Routing: would be `ready`").

`ENG-021` moved `designed → ready`, `owner: architect → eng-manager`. **1
transition**, well under the cap of 4. **Consequence:** machine WIP
`0/1 → 1/1`. Stopped there — work-breakdown/building is new implementation
work, chained instead rather than attempted inline, same handoff shape
`ENG-019`'s and `ENG-020`'s own dispatch passes already used today.

**Dead-end sweep:** all three `inbox/` items re-read fresh — `ENG-028`'s G1
and `ENG-016`'s Piece-2 question both still carry no `decision:` and already
carry their one-ever `nudged:`; `ENG-020`'s merge request carries no
`decision:` and no `nudged:` yet, `notified: 2026-09-05T13:40:18`, well under
the 24h threshold. No broken chains found — the only ticket in an
agent-owned working state before this edit was `ENG-020` (`blocked`,
correctly un-chained), and no `*-eng-events-dropped.md` exists for today.
**Merge detection (step 5):** `ENG-020` re-checked fresh (`git fetch` +
`git merge-base --is-ancestor` on both `aiorders-api` and `restaurant-portal`
worktrees, cross-checked with `gh pr view`) — both PR #17 and PR #4 still
`OPEN`, not merged. No other ticket is `blocked` on an L1 PR. **Observations
filed:** two, to `agents/eng-manager/observations.md` — a stale
`priority:` field found on `ENG-028`'s In-flight table row (blank, should be
`now`, fixed in this pass's board update), and `_index.md`'s own dated-entry
block no longer reads newest-first against the ticket-log ground truth
(this file's own three live entries are physically ordered
release-readiness/round-3/security-round-1, but `ENG-020`'s own append-only
log shows round-3 before security-round-1 before release-readiness) —
noted for whoever next touches the rolling mechanics, not corrected here
since reordering existing entries isn't this pass's job. **Notify sweep:**
nothing raised this pass (no new gate item); no re-nudge (both nudge-eligible
items already spent their one-ever nudge).

**Board update:** In-flight row (`state`, `owner`, `updated`); header's
machine-WIP paragraph noting the new occupant; `ENG-028`'s stale `priority`
cell corrected. Live file held three dated entries before this one — the
chronologically oldest (`continue (ENG-020): review+quality combined hop,
round 3`, per `ENG-020`'s own log timestamps, not this file's physical
position) rolled to `_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both
exit 0, clean.

`chained: ENG-021` — `ready` is agent-owned (`eng-manager`, work-breakdown
next per `tech-design/SKILL.md` step 11); not the approver, not blocked, not
terminal, not held by a cap. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh
continue ENG-021` before this pass exits.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-05 — continue: work-breakdown — `ready → building`, two sub-tickets

`continue` event pass, context `ENG-021`. Reading map: steps 6 and 6b, plus the
not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs instructed*, *The four
lanes*, *Guards*). Mode check clean (`MODE=active`). Pre-pass
`lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both exit 0.

Ran `work-breakdown/SKILL.md`. Autonomy check: both `aiorders-api` and
`restaurant-portal` are L1 — proceeds. Machine WIP re-checked fresh from every
ticket's own frontmatter: `1/1`, held by `ENG-021` itself (only `ENG-020`,
`blocked`, and this ticket sit outside terminal/pre-ready states) — a
ticket's own family isn't a second occupant of its own slot, same reading
`ENG-016`/`ENG-019` already established, so work-breakdown proceeds.

Split by the design's own `## Components` table into two owning-agent
sub-tickets — `ENG-040` (backend, `aiorders-api`) and `ENG-041` (frontend,
`restaurant-portal`) — no `database` sub-ticket, since this design has no
schema change (see `## Breakdown` above and the notebook for why that
verification is folded into `ENG-041` instead of ticketed separately).
Sequenced per the design's own Rollout order: `ENG-040` first (no
dependency), `ENG-041` `depends_on: [ENG-040]`, read literally as
*shipped*, not merely built, same precedent `ENG-016`'s/`ENG-019`'s own
sub-ticket chains already set. Full reasoning, the AC1-AC6 ownership mapping,
and every field decided without an explicit rule:
`agents/eng-manager/notebook/2026-09-05-eng021-work-breakdown.md`.

**Routing:** `ready → building`, owner stays `eng-manager` — no engineer
builds a two-surface parent with no diff of its own (`ready`'s exit condition,
`definition-of-done.md`, is satisfied by the breakdown itself). `ENG-040`
dispatched straight to `building` (no dependency); `ENG-041` stays `ready`
(unmet `depends_on: [ENG-040]`).

**1 transition** on this ticket (`ready → building`). Machine WIP: still
`1/1`, same family (`ENG-021` + `ENG-040`/`ENG-041`), not `2/1` — see
notebook. No gate raised, no G1/G2/G3, no one-way door.

**Dead-end sweep:** out of scope for `continue` (narrower contract — act on
the ticket this event names). **Notify sweep:** nothing raised this pass (no
new gate item written).

**Board update** — In-flight table: `ENG-021`'s own row (`state: building`,
`updated`); new rows added for `ENG-040` and `ENG-041`; `next_id` advanced
`ENG-040 → ENG-042`; header's machine-WIP paragraph noted. Live file held
three dated entries before this one — the chronologically oldest rolled to
`_index-archive.md` per the keep-three rule.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both
exit 0, clean.

`chained: ENG-040` — the only child with a met dependency and something
agent-actionable now. Fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-040`
before this pass exits. `chained: none` on `ENG-021` itself (parent has no
action until a child reports back) and on `ENG-041` (waiting on its unmet
sibling dependency) — recorded on each ticket's own log.

business-os itself left uncommitted — same standing default every pass has
used; the commit-convention question remains open, not re-decided here.

## 2026-09-07 — continue: parent settled — `building → shipped → verified`, slot freed and re-filled same pass

`continue` event pass, context `ENG-021`. Reading map for `continue`: steps 6
and 6b, plus the not-negotiable set (1, 7, 8b, 9, 10; *Enforced vs
instructed*, *The four lanes*, *Guards*) — step 2's mid-PRD checkpoint
doesn't apply, the PRD has been `approved` since 2026-09-03. Mode check clean
(repo-root `.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`, scoped
(`ENG-021`) and whole-board: both exit 0, clean.

**Both children re-checked fresh off their own frontmatter, not this
ticket's own cached narrative:** `ENG-040` and `ENG-041` both `state:
verified`, both `parent: ENG-021`, neither dropped. `ADR-003`-class exemption
met (both children settled, both actually shipped — well past the "at least
one" floor). `building → shipped`, no diff, review, QA, or security hop of
its own — same handoff shape `ENG-016`'s and `ENG-019`'s own parent
transitions used.

**Ran `acceptance-check/SKILL.md` in full despite the exemption** — the
skill's trigger has no parent carve-out. Re-fetched both repos fresh rather
than trusting either child's own notebook date: `aiorders-api` `origin/main`
→ `5e36648`, `restaurant-portal` `origin/main` → `f649583` — both identical
to the commits `ENG-040`'s and `ENG-041`'s own acceptance-checks already
walked, zero drift. Both children already ran `acceptance-check` in full at
their own shipping point (neither took the `ENG-031`/`ENG-037`-style
receipt-bookkeeping shortcut — neither is schema-only), so this pass is a
rollup and a fresh no-drift confirmation, not a gap-fill, same shape
`ENG-019`'s own closing check found for its family. All 6 PRD criteria pass
(AC1/AC2/AC6/AC3-UI cross-referenced from `ENG-041`'s own notebook; AC4/AC5/
AC3-write cross-referenced from `ENG-040`'s own notebook); no scope creep
found in a whole-family non-goals sweep (explicitly checked: no admin-hub
mirror, no answered/unanswered signal, no retention change, no PII
redaction — the security gate's Restricted classification is access control,
not redaction, matching the PRD's own framing); cost `$0/month` as estimated,
confirmed independently on both children's own release records. `shipped →
verified`. Full reasoning:
`agents/product-manager/notebook/2026-09-07-eng021-acceptance.md`.

**2 transitions** (`building → shipped`, `shipped → verified`), well under
the cap of 4. **Machine WIP: `1/1 → 0/1`, free** — the whole `ENG-021` family
(parent plus `ENG-040`/`ENG-041`) is now terminal.

**Step 6b: neither condition met** — same shape `ENG-019`'s own check gave
its identically-bare G1: the PRD's Non-goals section names deferred ideas in
prose (an answered/unanswered signal, clustering, a staff-facing admin-hub
mirror) but no "Feature shape and sequencing" section naming a specific next
ticket, and the G1 answer was a bare "approved" with no sequence sign-off.
Nothing filed.

**SLOT FREED — not left for the next dispatch-scoped pass.** `eng_build_loop.md`
Guards → Machine WIP limit, amended 2026-09-06 ("never idle"): the department
does not sit on a freed slot until a `scheduled`/`decision`/`watch` pass
happens to notice it — this is a live departure from the precedent
`ENG-016`'s and `ENG-019`'s own closing passes set (both logged `chained:
none` and left the pick to "the next dispatch-scoped pass," under the
pre-amendment reading). Applying the amended rule in this same pass rather
than the stale precedent, since the amendment post-dates both of those
closures and this event's own instructions restate it directly.

To-do column (`intake`/`shaped`/`awaiting-scope`) swept fresh, not from the
cached board header: `ENG-018`, `ENG-028`, `ENG-042` and `ENG-043` are the
only occupants. All four checked against `inbox/` directly —
`grep -l "^decision:" inbox/*.md` returns nothing, so all six open items
(including these four tickets' own G1s/clarification question) are
genuinely unanswered. **Nothing in To-do is startable** — every candidate is
on an unanswered scope/decision question (`ENG-042` additionally blocked on
`ENG-028`, itself unanswered). Not written up as a "Nothing I can start" gate
item — the held-for-slot pool below has a startable candidate, so the
machine isn't actually idle; that gate item is for when nothing anywhere
qualifies.

Fell back to the held-for-slot pool, same precedent `ENG-019`'s, `ENG-020`'s
and this ticket's own prior dispatch already set: `designed` tickets with a
completed design and no one-way door, deferred only by the cap. Candidates
carrying `priority: now`: `ENG-026`, `ENG-027`. Lowest id decided: `ENG-026`.
Re-confirmed its own design output directly rather than trusting the pool
description: `agents/architect/designs/ENG-026-foodswipe-channel-visibility.md`
exists, its own 2026-09-03 design-pass log states **No one-way doors**
plainly (checked against all six criteria in the design's own table), one
ADR (`ADR-010`) recorded with no G2 owed, `depends_on: []`, `blocked_on:`
empty. `tech-design/SKILL.md` step 11 routes exactly that case to `ready`,
owner `eng-manager`, no G2 — matching what `ENG-026`'s own prior log already
anticipated.

`ENG-026` moved `designed → ready`, `owner: architect → eng-manager` (logged
on its own board file). **Consequence:** machine WIP `0/1 → 1/1`. Stopped
there — work-breakdown/building is new implementation work, chained instead
of run inline, same handoff shape every prior dispatch on this board has
used (`ENG-021`'s own 2026-09-05 pick included).

**Dead-end sweep:** the To-do sweep above and the held-for-slot pick double
as this pass's own dead-end sweep — no other ticket touched beyond what
picking the next occupant required. **Notify sweep:** no new gate item this
pass (no G1/G2/G3, no merge request, no one-way door). Checked the six open
`inbox/` items fresh regardless, per the not-negotiable step 7, ages
computed on the local-wall-clock basis `notified:`/`nudged:` are actually
stamped in (per `2026-09-06-eng041-watch-recheck.md`'s own timezone-basis
finding, not the UTC-`Z` misread some earlier passes today used). Current
local time at check: `2026-09-07T02:27:24` PDT.

| Item | `notified:` (local) | Age |
|---|---|---|
| `ENG-016` continue-piece2 | 2026-09-04T10:58:06, `nudged:` 2026-09-05T09:31:45 | already carries its one-ever nudge |
| `ENG-018` G1 | 2026-09-06T03:13:31 | ~23h14m |
| `ENG-028` rescope G1 | 2026-09-06T02:28:29 | ~23h59m |
| `ENG-042` G1 | 2026-09-06T02:28:29 | ~23h59m |
| `ENG-043` clarification | 2026-09-06T02:47:56 | ~23h39m |
| `PROP-2026-W36` | 2026-09-06T18:57:12 | ~7h30m |

None carries a `decision:` (re-confirmed: `grep -l "^decision:" inbox/*.md`
returns nothing), so none is nudge-eligible on that basis either. `ENG-028`
and `ENG-042` are within about a minute of the 24h threshold — genuinely
under it at this check, not rounded, and very likely to cross it on
whichever pass runs next. No nudge due on any this pass.
**Observations filed** (`observations.md`, two): the notify-sweep above as a
concrete near-miss on the 2026-09-06 timezone-basis risk (`ENG-028`/`ENG-042`
sat ~65s under the 24h threshold — a wrong-basis read would have nudged both
a full day early); and this pass itself as the first application of the
2026-09-06 "never idle" amendment to a parent's own no-diff closing hop,
departing from `ENG-016`'s and `ENG-019`'s own precedent (correct at the
time, pre-amendment). **Exceptions/journal:** n/a — no
`exception-request:`, no G1/G2/G3/merge-request answered this pass (the
merge-request items resolved silently by GitHub merge on `ENG-021`'s own
children were already journaled — or correctly not — at each child's own
closing pass).

**Board update** — In-flight table: `ENG-021` row removed (terminal,
folded into the closing narrative below); `ENG-026` row (`state: ready`,
`owner: eng-manager`, `updated`); header's machine-WIP paragraph rewritten
for the new occupant. Live file's dated-entry rolling handled in the board
index's own edit for this pass.

Post-pass `lib/eng-gate-check.sh`, scoped (`ENG-021`) and whole-board: both
exit 0, clean.

`chained: ENG-026 — slot freed by ENG-021`. `ENG-021` itself is terminal
(`verified`) — the chaining guard never fires on a terminal ticket, so there
is no self-chain to record. But per the amended Guards rule, a freed machine
slot is not left idle: this pass drew the top of the held-for-slot pool
(To-do itself had nothing startable), dispatched `ENG-026` to `ready`, and
fired
`/bin/zsh /Users/hwalia/Documents/projects/personal/business-os/departments/engineering/lib/eng-trigger.sh continue ENG-026`
before this pass exits — recorded here, on the ticket whose transition freed
the slot, per the amendment's own worked example. Confirmed queued, not
dropped or silently failed: `traces/eng-loop-2026-09-07.log`'s `02:30:13
continue — pass in flight, queued as pending` line and `traces/.pending`
(`1 watch launchd` then `1 continue ENG-026`, oldest first) both show it
queued behind this same pass's own single-flight lock — expected, since
this pass itself still holds the lock — to drain the moment this pass
exits.

business-os itself left uncommitted through this edit — same standing
default every pass has used; the commit-convention question remains open,
not re-decided here.
