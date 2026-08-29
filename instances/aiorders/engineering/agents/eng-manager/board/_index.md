# Board

**Next ID: ENG-009** (`config/templates/ticket.md` — IDs are never reused;
this line is the counter it says lives here.)

**Machine WIP 6** (`config/config.yaml` → `wip.machine_limit`) — counts states
`ready` through `ready-to-ship`. **Currently 1/6** — `ENG-007` reached `ready`
in an earlier pass today, the first ticket on this instance's Windows host to
enter this range. `ENG-008` does not count here (`awaiting-scope`, short of
the counted range).
**Approver-facing WIP 2 — currently 1/2** — `ENG-008` reached `awaiting-scope`
this pass (its G1). One slot free.
**Approval cap 3 — currently 2/3** — `ENG-001`'s G3, `ENG-002`'s merge
request, `ENG-003`'s G1, `ENG-004`'s G1 **and** G3, `ENG-005`'s G1 — fork,
surface follow-up — **and** its merge request, `ENG-006`'s G1, G2, **and**
merge request, and `ENG-007`'s G1 **and** G2 are all answered and off the
board. Open now: `ENG-008`'s G1
(`inbox/2026-08-29-eng008-g1-scope.md`) and a standing, non-blocking
question about the same request's "engagement" item
(`inbox/2026-08-29-eng008-engagement-source-question.md`) — counted here
conservatively even though it names no ticket state and blocks nothing,
since it's functionally an open ask of the approver like any other. One
slot free.

`priority:` is a field on every ticket, and **only the approver sets it.** It is
not `severity`, which is the agent's read of how bad a problem is.

## In flight

| ID | Title | Project | State | Priority | Owner | Size | Updated |
|---|---|---|---|---|---|---|---|
| ENG-007 | Per-restaurant loyalty configuration — earn rates and redemption value | aiorders-api | ready | | eng-manager | S | 2026-08-29 |
| ENG-008 | Influencer board admin management — region/campaign-type preference, rating, collaboration count | aiorders-admin-hub | awaiting-scope | | approver | M | 2026-08-29 |

`ENG-002` shipped and reached `verified` in an earlier pass today — off the
In-flight table (terminal); see its own board file. `ENG-001` — this
instance's seed ticket — reached `verified` in an earlier pass today, its G3
answered **approved**; off the In-flight table (terminal); see its own board
file. `ENG-003` — its G1 answered **rejected** in an earlier pass today —
reached `dropped`; off the In-flight table (terminal); see its own board
file. `ENG-004` — its `ready-to-ship` confirmation and G3 were both raised
and answered **approved** in an earlier pass — reached `verified`; off the
In-flight table (terminal); see its own board file and the dated entry now
in `_index-archive.md` (rolled this pass, per the keep-three rule). `ENG-005`
— its L1 merge request answered **merged**, independently confirmed by git
ancestry — reached `verified`; off the In-flight table (terminal); see its
own board file and `agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md`.
`ENG-006` — a control-center dashboard action advanced `blocked → shipped`
ahead of this pass; its L1 merge request answered **approved** and
independently confirmed by git ancestry, then this pass carried it
`shipped → verified` — off the In-flight table (terminal); see its own board
file and `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`.

## Waiting on the approver

Cap: 3 across all gates. **Currently 2/3.** `ENG-007`'s G2 one-way-door (the
Walletly question) was answered in an earlier pass today: Walletly is being
retired/replaced, so the sequence proceeds as originally scoped — off this
list. Open now: `ENG-008`'s G1 scope
(`inbox/2026-08-29-eng008-g1-scope.md`, raised and notified this pass — see
its own frontmatter, the notify channel's known `SLACK_WEBHOOK_URL unset`
failure applies here too, `notified:` hand-stamped per established
practice) and a standing, non-blocking question about "engagement," the
one part of the same request neither independent reading could resolve
from the text
(`inbox/2026-08-29-eng008-engagement-source-question.md`) — does not block
`ENG-008` itself, counted here anyway out of caution.

## 2026-08-29 — intake: influencer-board admin-management request shaped to ENG-008, one non-blocking question raised separately

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-for-the-influencer-board-on-admin-panel-we-are-unable-to-see.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own
narrower contract, worked only this one request end to end rather than
sweeping the board — `ENG-007` and the other pending product-manager-inbox
requests untouched. Mode check clean (business-os `.env` → `MODE=` empty).
Caps checked fresh before raising: approver-facing WIP 0/2, approval cap
0/3, both fully free.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading plus a blind architect reading (subagent, `opus`,
raw request + `knowledge/business-profile.md` only). One material
divergence — whether an influencer-facing surface already exists at all —
resolved by checking `aiorders-api`'s live `origin/main` rather than by
guessing or asking: it already has `restaurant-influencer-campaigns`
(invitation-based), an `outgoing-communications` actor for influencers, and
`migrate-influencer-images`, so this extends a real existing concept.
Both readings independently flagged "engagement" as unresolvable from the
text — a joint gap, not a disagreement — and that's the one thing sent to
the approver as a question.

**Split the request into a two-item shape, filed the first, named the
second.** `ENG-008` (this pass, `awaiting-scope`) covers the admin-side
data only — region/campaign-type preference view+edit, rating,
collaboration count, project `aiorders-admin-hub`, size `M`. Item 2
(influencer-facing opportunity visibility gated by region/campaign-type)
depends on `ENG-008`'s fields and is named in the PRD as proposed, to be
filed once `ENG-008` verifies, per the `ENG-006`/`ENG-007`
sequence-continuation precedent (`skills/acceptance-check/SKILL.md` step
6b) — this is the same request's other half, not agent-invented work.
"Engagement" is deliberately in neither ticket: a standing, non-blocking
question is with the approver instead
(`inbox/2026-08-29-eng008-engagement-source-question.md`), since its
answer swings scope roughly an order of magnitude (a display field vs. a
paid third-party social-platform integration) and neither reading could
settle it from the text.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stops here by
design. Consequence: approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 2/3
(the G1 plus the standing question, the latter counted conservatively per
the header note above). Machine WIP unaffected.

Ran `departments/engineering/lib/eng-notify.sh raise` on both new `inbox/`
items — both logged the already-open `SLACK_WEBHOOK_URL unset` failure
(`traces/eng-notify-2026-08-29.log`), consistent with every gate raised on
this instance recently; `notified:` hand-stamped on both per established
practice. No dissent section on the G1 — `agents/critic/agent.md` still
doesn't exist (open proposal, `proposals.md` 2026-08-25 row), confirmed
absent again rather than assumed.

**Dead-end sweep:** out of scope for `intake`'s own narrower contract — not
run; `ENG-007` untouched. **Observations filed** (`observations.md`): the
confirmed-live influencer/campaign backend and its invitation-shaped
implication for item 2.

`chained: none` — `ENG-008` sits at `awaiting-scope`, owned by the
approver; the chaining guard never fires on a ticket waiting on a human.
Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-008-influencer-profile-admin-management.md`).

## 2026-08-29 — watch (schtasks): no ticket touched — resolved the standing events-dropped incident, deferred a sixth new business request

`watch` event pass, context `schtasks` — day 5/40 charged, drained immediately
behind the `watch (schtasks)` pass below (`pass end: watch (exit 0, 973s)` at
01:25:17 → `queue: collapsed 3 duplicate event(s)` → `draining queued event:
watch (schtasks)` at 01:25:33), the 5-minute poll cadence backlogging while
that long pass held the lock, already-confirmed-working design (2026-08-28
Windows-port observations), not a bug. Mode check clean (business-os `.env`
→ `MODE=` empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket to
scope to): exit 0, clean.

**Swept all three watched inboxes fresh rather than trusting the pass
below's own read.** `agents/eng-manager/inbox/` holds only `.gitkeep`.
`inbox/requests/` empty. `ENG-007` unchanged at `ready`, its own log still
ending in a valid `chained: ENG-007` — nothing broken to resume. The five
`agents/product-manager/inbox/` items the immediately preceding pass found
and correctly deferred are all still exactly that: unshaped, their dedicated
`intake` events still sitting in `traces/.pending` — re-confirmed rather than
assumed, since shaping any of them is `intake`'s job under this event's
narrower contract, not `watch`'s, same reasoning the last two passes already
established. **Four more landed mid-sweep, checked at the end of this pass
rather than assumed unchanged from the top of it** — catering/quote-generator
(08:32:55), AI SEO ROI tracking (08:39:27), brand-portal drip/mass campaigns
(08:37:36), and admin-panel autopilot/demo account for resellers (08:35:46),
all `via: control-center`, nine total now landed 08:14–08:39. Read all four
before leaving them: routine feature requests, no security or urgency
language in any. Left untouched for their own `intake` events, same as the
first five; not worth a further `observations.md` entry, it's the same
batch-arrival pattern already recorded there, just a larger batch than first
seen.

**`inbox/2026-08-28-eng-events-dropped.md` came back answered since the last
pass to read it** — `decision: approved`, `decided:
2026-08-29T08:27:47.038600+00:00`, a hand-edit, not a reply through
`lib/eng-notify.sh` (unsurprising: this item was never successfully notified
in the first place, the known `MODE`-collision bug, `proposals.md`
2026-08-25 row — the approver found it by reading `inbox/` directly).
Verbatim: "recheck the request and report back how to fix. fix if you can."
This is exactly the class of thing `watch`'s own contract exists to catch (a
gate item edited by hand), and unlike the five business requests above,
answering it doesn't require `intake`-style PRD shaping — it required an
investigation, which this pass did rather than deferring further (this item
had already sat unanswered through several earlier passes; deferring an
*answered* incident again would just repeat that).

**Investigated as far as this instance's architecture allows, and said so
plainly rather than guessing at a false confirmation.** `traces/` is
`.gitignore`d and host-local; this instance now runs on two hosts (the Mac
that raised this incident at 10:42:17 that morning, and Windows since
`168cb89`); this Windows checkout's own trace history starts at 23:33:59
that night. The actual failure log is on the Mac's disk and unreachable from
here — full detail and the reasoned-not-confirmed TCC/EPERM-over-spend-limit
hypothesis (from `observations.md`'s same-day entries, since the log itself
isn't available) on the item's own file. Filed a proposal
(`agents/eng-manager/proposals.md`, 2026-08-29 row) for the fixable half:
dropped-event items should carry their own failure excerpt instead of a
`traces/` pointer that only resolves on the host that failed. Moved to
`inbox/_handled/`; journaled in
`agents/eng-manager/config/decision-journal.md` as a new data point (an
incident response, not a ticket gate) rather than skipped for not fitting
the G1/G2/G3 shape.

**No ticket transition** — `ticket: unknown` on the incident, and nothing
else was new. WIP/approval-cap figures unchanged (machine 1/6, approver
0/2, approval cap 0/3) — the incident was never counted against the approval
cap (not a G1/G2/G3 or merge request), so resolving it doesn't move any of
the three numbers.

**Dead-end sweep:** `ENG-007` is the only ticket in flight; its chain is
valid, nothing to resume. **Notify sweep:** nothing raised this pass (the
proposal rides the weekly report, not `lib/eng-notify.sh`); nothing to
nudge; approval cap 0/3, not full — no stall. **Observations filed**
(`observations.md`): sharpened, not overturned, the prior pass's "all
non-emergency" read of the five-item batch — the admin-portal/agency-reseller
item is the approver's own words, "security issue," a cross-tenant data
exposure on a registered **L1** project, worth real severity when its
`intake` event shapes it rather than routine `P3`.

`chained: none` — no ticket was touched this pass (the incident carries no
ticket to advance), so there is no hop of its own to fire. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

## 2026-08-29 — watch (schtasks): ENG-007's G2 came back answered — Walletly is retiring, ticket advanced to ready and chained

`watch` event pass, context `schtasks` — a second, distinct fire from the one
immediately below, queued behind (and launched right after) an unrelated
`decision` pass that drained first and correctly no-op'd on this ticket's
already-processed G1. Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean.

**Swept all three watched inboxes fresh; found `ENG-007`'s G2 answered**
since the previous pass raised it — `decision: approved`, verbatim
"Walletly is being retired/replaced," a hand-edit to
`inbox/2026-08-29-eng007-g2-walletly-conflict.md` rather than a reply through
`lib/eng-notify.sh`. Re-verified fresh rather than trusted (re-read the file,
checked `traces/.pending` for a live race) before acting. Picks option 1 of
the three the gate offered: the native loyalty sequence is Walletly's
intended replacement, proceed exactly as scoped — settling the boundary
question before ticket 3 (the points ledger) is ever filed.

**Processed here rather than left for a `decision` event already queued
behind this one for the same file** — the mirror image of this ticket's own
G1 a few minutes earlier, where `decision` drained first and `watch` found
nothing left to do; whichever event reaches a fact first does the real work,
per this instance's established practice. Moved the gate item to
`inbox/_handled/` with a processed footer; journaled in
`agents/eng-manager/config/decision-journal.md`. Architect's design doc left
unedited, same precedent `ENG-006`'s own G2 resolution set.

**1 transition** (`awaiting-decision → ready`), well under the cap of 4 —
`building` needs a different owning role (backend/database) actually writing
code, which is new implementation work and this pass's stop point by design.
Approver-facing WIP 1/2 → 0/2; approval cap 1/3 → 0/3 (now empty); machine WIP
0/6 → 1/6 — the first ticket into that range on this host.

**Dead-end sweep:** no other ticket in flight. **Not a clean sweep on the
inboxes, corrected here rather than left standing:** five new files landed in
`agents/product-manager/inbox/` mid-pass (`source: approver`, `via:
control-center`, received 08:14–08:22), after this pass's own initial sweep
had found that directory empty. Read all five before deciding not to act:
UX/functionality gaps on the admin panel (influencer board, brand
stage/health filtering), the FoodSwipe sales-funnel pipeline stages, the
brand portal (QR codes, media downloads, site-timing self-service), and
admin-portal readiness for agency/reseller users — none meets the P0 bar
(production down, data loss, active security incident), so none interrupts.
Left untouched for their own dedicated `intake` events, already visible
queued in `traces/.pending` for four of the five (the fifth landed after that
read and will get its own `watch` or `intake` fire) — shaping five requests'
worth of readback and G1s is `intake`'s own job per this event's narrower
contract, not this `watch` pass's. Observation filed. **Notify sweep:**
nothing to raise or nudge; cap just cleared to 0/3 — no stall.

`chained: ENG-007` — `ready` is agent-owned (eng-manager sequenced it; a
backend/database engineer builds next), not the approver, not blocked, not
terminal, not capped. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-007` before
exiting. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`)
and whole-board: both run clean.

## 2026-08-29 — watch (schtasks): ENG-007's G1 came back approved — designed, then a new G2 raised over an unplanned Walletly finding

`watch` event pass, context `schtasks`. Per the event's own narrower
contract, swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`,
and `inbox/` (including `inbox/requests/`) only, acting on whatever is new.
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty, both fall through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean.

**Third attempt at tonight's fire** — two earlier launches for the same
event (pid `3199`, `1301`) went stale and were cleared by the trigger
before this one (pid `1067`) reached the lock; both died mid-investigation
with no write ever made, confirmed from their own output before trusting a
clean slate. `.hops-2026-08-29` reads `2`, nowhere near the daily ceiling.
Full detail on the ticket's own log.

**Found `ENG-007`'s G1 answered** (`decision: approved`,
`decided: 2026-08-29T07:15:41.687445+00:00`) — a hand-edit to the gate item
directly, not a reply through `lib/eng-notify.sh`. Moved to
`inbox/_handled/`, journaled. Also fixed the PRD's own stale
`status`/`decided` fields, left unset by an earlier crash-and-recover pass.

**No project worktree existed on this host** — `config/projects.md`'s "all
five worktrees already exist" was true only for the earlier Mac
verification. Created `aiorders-api`'s the same way `lib/eng-setup.sh`
would, then did real design work against the live repo (fresh `git fetch`,
read the now-actually-tracked migrations rather than inferring from
edge-function code). Full design: `restaurant_loyalty_configs`, open-ended
effective-dating, a per-restaurant-advisory-lock trigger closing the PRD's
own concurrent-write risk at the database, and an `admin-portal` handler
reusing the existing admin/sub-admin auth gate — complete and ready to
build. `agents/architect/designs/ENG-007-per-restaurant-loyalty-configuration.md`.

**Significant unplanned finding: a live, documented, actively-maintained
third-party loyalty vendor (Walletly) already runs in this codebase**,
unmentioned in the original request or either PRD. `ENG-007` itself carries
no risk from it, but ticket 3 (the points ledger) would start a second,
competing points system in production alongside it — expensive to unwind
after adoption, not before. Escalated via a new G2 rather than decided
unilaterally or silently carried forward:
`inbox/2026-08-29-eng007-g2-walletly-conflict.md`, recommending `ENG-007`
proceed now (no dependency on the answer) while ticket 3 waits for it.
Raised and notified (`lib/eng-notify.sh raise` logged
`SLACK_WEBHOOK_URL unset — cannot notify` — the plain-failure face of the
already-open channel-dispatch proposal, not a new bug); stamped `notified:`
by hand.

**2 transitions** (`awaiting-scope → designed → awaiting-decision`), well
under the cap of 4 — the next state needs the approver. Approver-facing WIP
and approval cap both net unchanged at 1/2 and 1/3 (this ticket's G1 closed,
its G2 opened). Machine WIP unaffected (0/6).

**Dead-end sweep:** no other ticket in flight; nothing else new across all
three inboxes. **Notify sweep:** this pass's own G2 raised and stamped;
nothing else to nudge; cap 1/3, not full — no stall. **Observations filed**
(`observations.md`): the missing Windows worktree, the now-tracked
migration history correcting `ENG-006`'s design doc, the Walletly
discovery, and today's plainer `eng-notify.sh` failure signature — all
corroborating existing gaps, none new. **Correction filed**
(`config/projects.md`): the worktree-existence claim is host-specific.

`chained: none` — `awaiting-decision` (G2), waiting on the approver. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-007`) and whole-board: both run clean.

