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
state: designed
owner: architect
lane: full
blocked_on:
blocked_from:
source: approver
created: 2026-08-29
updated: 2026-09-03
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
