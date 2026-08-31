# Engineering Board — pass log archive

Dated pass entries moved out of `_index.md` once the live board holds more than
three, newest first. The live board keeps its table plus enough recent narrative
to resume a ticket; everything older lives here.

Nothing reads this file on a pass — it is the department's history, not its
state. `lib/eng-gate-check.sh` globs `ENG-*.md` and never sees it.

This exists because every pass reads `_index.md` in full, so an append-only log
there is a tax on every future pass.

---

## 2026-08-31 — continue ENG-015: design actually written — PASS, stays at designed (WIP-capped)

`continue` event pass, context `ENG-015`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
This is the design work three prior passes recorded chaining to and none of
them actually reached — confirmed at pass start: `ENG-015` absent from
`traces/.pending` (already drained to launch this session); no design file
existed at `agents/architect/designs/ENG-015-*.md`. Mode check clean.
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-015`) and whole-board: both exit 0, clean.

Read the real code across both repos this ticket touches — `aiorders-api`'s
`admin-portal/handlers/restaurants.ts` (all four functions, not only the one
the PRD's Evidence section named), `brands.ts`, `_shared/restaurantAccess.ts`,
`proxy-login/index.ts`, every migration touching `restaurants`'/`brands`'
RLS, and `admin-portal/index.ts`'s auth middleware; `aiorders-admin-hub`'s
`AddRestaurantModal.tsx`, `AuthContext.tsx`, `Brands.tsx`,
`PartnerBrandAssignment.tsx`, `Restaurants.tsx` — rather than trusting the
PRD's summary. Wrote
`agents/architect/designs/ENG-015-agency-reseller-brand-scoping.md`: one
local helper pair in `restaurants.ts` (`isStaff`, `getPartnerBrandIds`)
applied to `getRestaurants`/`getRestaurantById`/`updateRestaurant`; one new
`INSERT` policy migration on `restaurants` (brand-scoped, `WITH CHECK
(approved = false)`); one small `AddRestaurantModal.tsx` change.

**Tracing the RLS history changed the design from what the PRD proposed.**
The PRD suggested mirroring `brands.ts`'s client-branch pattern for the read
fix. Three migrations after the one the PRD cited already locked
`restaurants`' public SELECT down to `USING (false)` — that branch would
return zero rows for a partner today, not their own brand's rows. Separately
`brands` has zero RLS policies in tracked migration history at all, the same
untracked-schema-history gap the PRD already names for `profiles`/
`influencers`, now confirmed for a second table. Designed around both
findings — brand scoping enforced in code via the service-role client, not
by trusting either table's RLS. `ADR-006` records the decision; judged
reversible and not a one-way door, same precedent `ADR-004`/`ADR-005` set —
**no G2**.

**Extended the fix to two functions the PRD's Evidence section didn't
name** (`getRestaurantById`, `updateRestaurant` — same file, same defect,
reachable today by a partner via a direct call, squarely inside AC2's own
wording), logged as a deliberate scope decision rather than silently
expanded or silently left open. **Found a third, unrelated defect in the
same file** (`updateBrandOwner()` — no role/ownership check at all, any
partner can rewrite any brand owner's contact info) — different resource
than this PRD describes, not folded in; filed as a proposal in
`agents/eng-manager/proposals.md` (architect-originated finding, step 3)
instead.

**Stays at `designed` regardless — held by the machine WIP cap, not a
gate.** Re-verified fresh from each ticket's own frontmatter: `ENG-008`
(`in-qa`), `ENG-009`/`ENG-010` (`ready`), `ENG-013` (`ready-to-ship`) — four
tickets inside the counted `ready`..`ready-to-ship` range against a cap of
1, unchanged since this morning's `scheduled` sweep. Design work itself is
exempt from this cap; entering `ready` is not, so this pass does not
attempt it — no branch created in either worktree, no code written.

Closes the chain gap the `scheduled` sweep flagged this morning against
this ticket specifically: `ENG-015` was sitting at `designed`
*un-designed*, not cap-held-after-completion. As of this pass it's
genuinely the latter.

**0 transitions** — ticket stays at `designed`; the cap, not the hop
budget, is what stopped it. Machine WIP unaffected (still 4/1, `ENG-015`
was never inside the counted range). Approver-facing WIP and approval cap
both unaffected — no gate raised.

`chained: none` — held by the machine WIP cap (4/1:
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` occupying), one of the documented
no-chain conditions. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-015`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-014: design actually written — PASS, stays at designed (WIP-capped)

`continue` event pass, context `ENG-014`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
This is the dedicated `continue ENG-014` session three prior passes recorded
chaining to and none of them actually reached — confirmed at pass start:
`ENG-014` absent from `traces/.pending` (already drained to launch this
session). Mode check clean. Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-014`) and
whole-board: both exit 0, clean.

Read the real code across all three repos this ticket touches
(`aiorders-api`'s `url-shortener` and `brand-portal` functions,
`aiorders-admin-hub`'s three existing QR/media call sites, `restaurant-portal`'s
own context/API/nav) rather than trusting the PRD's summary. Wrote
`agents/architect/designs/ENG-014-restaurant-qr-media-self-service.md`: one
new restaurant-scoped action on `url-shortener` (`get_or_create_restaurant_qr`,
computing its own destination URL server-side rather than trusting the
caller's, which is what makes the restaurant-scoping actually binding), one
new read action on `brand-portal` (`get_restaurant_media_info`), and both
existing generator components ported into `restaurant-portal` (no shared
package exists across these four repos to import from instead). `ADR-005`
records the one real "why on earth" decision (narrowing `url-shortener`'s
trust boundary per-action); judged reversible and not a one-way door, so
decided and logged rather than escalated — **no G2**, same precedent
`ENG-011`/`ENG-013` set.

**Stays at `designed` regardless — held by the machine WIP cap, not a gate.**
Re-verified fresh from each ticket's own frontmatter: `ENG-008` (`in-qa`),
`ENG-009`/`ENG-010` (`ready`), `ENG-013` (`ready-to-ship`) — four tickets
inside the counted `ready`..`ready-to-ship` range against a cap of 1. Design
work itself is exempt from this cap; entering `ready` is not, so this pass
does not attempt it.

Closes the specific ambiguity the architect's own `ENG-023` observation and
the prior `scheduled` sweep both flagged against this ticket: `ENG-014` was
sitting at `designed` *un-designed*, not cap-held-after-completion. As of
this pass it's genuinely the latter. `ENG-015` is untouched (out of scope —
this event names `ENG-014` only) and remains un-designed.

**0 transitions** — ticket stays at `designed`; the cap, not the hop budget,
is what stopped it. Machine WIP unaffected (still 4/1, `ENG-014` was never
inside the counted range). Approver-facing WIP and approval cap both
unaffected — no gate raised.

`chained: none` — held by the machine WIP cap (4/1:
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` occupying), one of the documented
no-chain conditions. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-014`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-013: security gate — PASS, now ready-to-ship

`continue` event pass, context `ENG-013`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

Ran the security gate fresh — no receipt existed at pass start, a real
first execution. Threat-modelled the change (new input: `profileId`/`stage`
on two new POST routes, both behind the existing bearer-auth middleware and
the handler's existing admin/sub-admin gate; new capability: write access
to one enum field, granted only to the population that could already read
every row; blast radius on full compromise: integrity-only, reversible, no
new confidentiality or financial exposure). Walked OWASP A01–A10, 8 `n/a`
with reason, 2 reviewed in full. A01 clean — both new write routes reuse the
one existing gate call and additionally scope every write to
`source='foodswipe'`, the same tenant boundary the existing read already
enforced; independently re-verified the tenant-scoping test is
mutation-sensitive by construction, not just shape-checked. A05 found one
non-blocking item — both new actions return a raw `error.message` on a
500 — weighed (role-gated before either function runs, copied from this
file's own pre-existing `GET` catch, nothing secret in what it could
contain) and logged as the first tracked occurrence of this finding class
in `agents/security/notebook/2026-08-31-findings.md`, not escalated.
Checked all three of the baseline's negative-auth cases, not just the two
with dedicated tests — read `admin-portal/index.ts` fresh to confirm the
no-token case 401s upstream of this handler entirely, unmodified by this
diff. Secret-scanned the diff and all three unique commits across both
branches: zero matches. SOC 2 evidence trail confirmed complete. Full
detail: `agents/security/reviews/ENG-013.md`, and the ticket's own log.

**1 transition** (`in-qa → ready-to-ship`), well under the cap of 4 —
stopped deliberately, not by the cap: `release_readiness` is a separate
hop after `security` per `config.yaml`'s `sequential_after_quality`, and
this was a fresh security session with no receipt to recover. `machine_wip`
unaffected (`ENG-013` stays inside the counted `ready`..`ready-to-ship`
range, now at its far end). Approver-facing WIP and approval cap both
unaffected — `ready-to-ship` raises no gate for an L1 project; devops's
release-readiness hop is what opens the PR and raises the merge request.

`chained: ENG-013` — `ready-to-ship` is agent-owned (devops's
release-readiness hop next), not the approver, not blocked, not terminal,
not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-013`
before exiting — confirmed queued (not lost): the trigger's own log shows
it queued behind the still-active `scheduled launchd` fire's lock rather
than launching immediately, same FIFO shape every prior hop on this ticket
has used. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-008: review+quality combined hop, round 2 — PASS, now in-qa

`continue` event pass, context `ENG-008`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Ran the code-review-gate and quality gates fresh, re-deriving both diffs
from disk rather than trusting the prior pass's own account (clean diff
against each repo's own merge-base, no main-drift pollution). Automatic-
failure scan: 0/10 open — both round-1 findings independently re-verified:
hand-traced all 19 `Deno.test` cases in `influencers.test.ts` against
`influencers.ts` at HEAD (no `deno` on this host), and independently
re-confirmed the frontend null-coalescing fix by re-reading the migration's
additive backfill, not by trusting the fix-pass's own claim. One new,
non-blocking (P3) finding from this round's own full review — not a round-1
regression: `handleSaveInfluencer` can write a stale `min_visit_payment`
after `accepts_paid` is toggled off, since the two fields are sent
independently of each other. Named in the review receipt rather than filed,
per this board's practice for a single-occurrence, non-blocking finding at
this scale. Full detail: `agents/principal-engineer/reviews/ENG-008.md`,
`agents/qa/test-plans/ENG-008.md`, and the ticket's own log.

**2 transitions** (`building→in-review→in-qa`), well under the cap of 4 —
stopped deliberately, not by the cap: security is a separate hop by design
(`sequential_after_quality`), needing this pass's own just-written QA plan,
and a fresh session is what `eng_build_loop.md` calls for there. `machine_wip`
unaffected (`ENG-008` stays inside the counted `ready`..`ready-to-ship`
range — now at `in-qa`, alongside `ENG-013`). Approver-facing WIP and
approval cap both unaffected — no gate raised.

Also populated `time_estimate`/`time_spent`/`time_remaining` on this ticket
for the first time — round 1's own observation had flagged these as never
carried despite `definition-of-done.md` calling for them from `building`
onward; closed here rather than left for another pass to re-notice.

`chained: ENG-008` — `in-qa` is agent-owned (security next, fresh session),
not the approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — scheduled (launchd): three broken chains repaired (ENG-014/015/025), attempt 2/3 on this event

`scheduled` event pass, context `launchd` — the four-times-daily safety-net
sweep, whole-board per this event's own contract. This fire is attempt 2/3
of the `scheduled` event: attempt 1 (02:45–02:56) ran a real 647s
investigation, reached the same conclusion below, then died exit 1 on the
account's monthly spend limit at the moment it tried to act — correctly not
treated as "never started" (real output, real duration) and correctly
re-queued rather than dropped. This pass independently re-verified
everything from disk rather than trusting that narrative, per this
instance's own standing practice.

Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Gate returns:** `inbox/` holds one item, `2026-08-30-eng-events-dropped.md`
(incident, no `decision:` field) — already self-investigated same-day,
concluding the two causes (OAuth token revoked, transient DNS failure) were
host/network issues unrelated to `ENG-023`. Left in place, not archived:
every prior `eng-events-dropped` item on this board (`decision-journal.md`
rows 22, 35) moved to `_handled/` only once the approver actually answered
it; this one never has, and "never infer approval from silence" applies to
archiving an incident item as much as to advancing a ticket. Not blocking
anything — `gate: incident` items don't occupy the approver-facing WIP or
approval-cap counts. PM inbox and EM inbox both empty (only `_handled/`) —
nothing for business or technical intake this pass.

**Merge detection:** no ticket currently at `state: blocked` (confirmed by
grepping every ticket's own frontmatter, not the board header) — nothing to
check against `origin/main`.

**Dead-end sweep — the substantive finding.** Investigated
`agents/architect/designs/` directly after the `continue ENG-023` entry
above filed an observation that `ENG-014`/`ENG-015` were cited as
`designed`-by-WIP-cap precedent without actually having a design file.
Confirmed and extended: **`ENG-014`, `ENG-015`, and `ENG-025` all have no
design file, and none of them has ever had a `continue` pass actually run**
— grepped every `traces/eng-loop-*.log` this instance has ever written for
`pass start: continue (ENG-014|ENG-015|ENG-025)` (exact format confirmed
live against `ENG-008`'s and `ENG-013`'s own successful runs earlier today):
zero matches, for any of the three, ever. `ENG-014` and `ENG-015` each
carry a ticket-log entry from 2026-08-29 that already found and repaired
this once (the original `watch`-pass fire died before launching; a later
`decision` pass re-fired it and confirmed it landed in `traces/.pending`)
— so this is a *second*, different loss of the same two chains, this time
between a confirmed append and an actual drain, with no code read yet that
explains how. `ENG-025` never had that intermediate repair at all. None of
the three ever produced an `eng-events-dropped` incident, because that
mechanism only fires on a launch that fails or never-starts — this loss
happens earlier, between append and drain, so today's board-reading safety
net is currently the only thing that catches it, and it took two days on a
`P1` security ticket (`ENG-015`).

**Action taken.** `continue ENG-014` was already sitting in
`traces/.pending` at this pass's start — left alone rather than double-fired
(collapses harmlessly at worst; firing blind into a possibly-already-stuck
entry doesn't diagnose anything). `continue ENG-015` and `continue ENG-025`
were not queued — fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-015` and
`continue ENG-025` directly, each confirmed on `traces/.pending` afterward
rather than assumed. All three now queue behind `ENG-008`/`ENG-013`
(already queued, unrelated) and will drain one pass at a time once this
pass releases the lock. Full reasoning on each of the three tickets' own
logs.

**Filed, not fixed:** `agents/eng-manager/proposals.md` — the dispatch gap
itself (append confirmed, drain never happens, no drop-notice either) is
department machinery, not a ticket-shaped change, and this instance's own
rule reserves that class of fix for the approver's sign-off. Corroborating
row in `observations.md`, cross-referencing the architect's own `ENG-023`
observation this same day.

**Notify sweep:** nothing new to raise — no gate opened this pass, and the
one open incident item is well past any nudge threshold but explicitly
exempt (see Gate returns above; it isn't a decision awaiting an answer in
the G1/G2/G3/merge sense the nudge rule targets). Approval cap 0/3, not
full — no stall.

**Caps, re-verified fresh:** machine WIP still 4/1 (`ENG-008`/`ENG-013`
`building`, `ENG-009`/`ENG-010` `ready`) — unaffected by any action this
pass (all three repairs stay at `designed`, below the cap's own range).
Approver-facing WIP 0/2, approval cap 0/3 — both unaffected, no gate raised
or answered.

`chained: ENG-015`, `chained: ENG-025` — both fired and confirmed queued
this pass (see ticket logs). `chained: none` for `ENG-014` — already
queued; a second fire would not be a repair. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-013: review+quality combined hop, round 2 — PASS, now in-qa

`continue` event pass, context `ENG-013`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

Ran the code-review-gate and quality gates fresh — no receipt existed for
either at pass start, so unlike `ENG-007`'s/`ENG-011`'s own recovery passes
this was a real first execution, not a discovery of already-completed work.
Automatic-failure scan: 0/10 open — round 1's #10 (no failure-case test on
the new authz-gated write path) is closed by `foodswipe.test.ts`, with the
`source='foodswipe'` scoping test confirmed mutation-sensitive (a fake
client records every `.eq()` call, so removing that scoping line would fail
the test for the reason it exists, not incidentally). `npm run
lint`/`npm run build` (`aiorders-admin-hub`) reproduced fresh, both clean
against this ticket's own recorded baseline. `deno test` could not execute
on this host (deno absent, `aiorders-api` has no registered suite command)
— hand-traced all 17 cases against the code at HEAD instead, independently
of the prior pass's own trace, zero discrepancies, named plainly as
corroborating evidence rather than a green run. QA plan written covering
all five acceptance criteria. Full detail: `agents/principal-engineer/reviews/ENG-013.md`,
`agents/qa/test-plans/ENG-013.md`, and the ticket's own log.

**2 transitions** (`building→in-review→in-qa`), well under the cap of 4 —
stopped deliberately, not by the cap: `config.yaml`'s `combined_hop`
licenses exactly `[code_review, quality]` together; security is a
separate hop by design (`sequential_after_quality`), needing QA's just-
written plan, and a fresh session is what `eng_build_loop.md` calls for
there. `machine_wip` unaffected (`ENG-013` stays inside the counted
`ready`..`ready-to-ship` range). Approver-facing WIP and approval cap both
unaffected — no gate raised.

**Observation filed** (`observations.md`): the existing Supabase-MCP
substitute-verification proposal (2026-08-29) does not cover this ticket's
own deno-unavailable gap — different tool, no substitute execution path
exists; a prior pass's note conflated the two.

`chained: ENG-013` — `in-qa` is agent-owned (security next), not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-013`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-31 — continue ENG-008: round 1's findings fixed, chained for review round 2

`continue` event pass, context `ENG-008`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Found a second undocumented commit on `aiorders-api` (`dc6972a`, the missing
test file round 1 asked for) — same cross-host shape `ENG-013` hit
2026-08-30, but this time hand-tracing it against the review notebook (not
just against the handler) found it incomplete: covered three of four named
`hasInfluencerAdminAccess` cases and every field validation, but not the
"missing/undefined profile" case or a test proving `EDITABLE_FIELDS`
actually strips an unauthorized field from a mixed body. Closed both gaps:
`hasInfluencerAdminAccess` now null-safe (optional chaining; confirmed not
live-reachable today since `index.ts`'s router already 403s before any
handler runs on a missing profile, fixed anyway to match this repo's own
`loyalty-config.ts` precedent and close what round 1 explicitly asked for),
plus two new tests. Independently re-confirmed the CORS/`PATCH` fix from the
original build hop is still intact.

Fixed the real bug properly rather than patching the symptom:
`Influencers.tsx`'s `accepts_paid`/`accepts_barter` now pass through
`openInfluencer` as `null` (dropping the `barter_visit` fallback entirely —
hand-confirmed it never had a correct value to fall back to, since the
migration's additive backfill guarantees `barter_visit` is null in every row
where the new flags are also null), checkboxes render unchecked via
`?? false` without mutating the stored form state, and
`handleSaveInfluencer` now omits either field from the PATCH body while
still `null` — an untouched unset preference survives any number of saves
instead of getting overwritten with a guess. This is the stronger of the two
fixes the review offered ("or track which the user actually touched"),
required because the review's own regression-test wording ("neither is
written unless the user checks it") isn't satisfiable by a blanket
default alone. Also dropped the one cosmetic `Button variant="secondary"`
change round 1 flagged but didn't block on.

Self-tested with this repo's only available tools: `npm run build` clean,
`npm run lint` 150 errors / 1 warning, both figures identical to this
ticket's own recorded baseline, zero new. No automated frontend regression
test exists to add — confirmed fresh that `aiorders-admin-hub` has no test
framework, no `test` script, and zero test files anywhere in the repo;
proposal filed (`proposals.md`) rather than standing up a test harness
inside a bug-fix ticket. One observation filed (`observations.md`): a found
commit needs checking against the finding it was meant to close, not only
against the code.

Both branches committed (automation identity `businesspilotcare-gif`,
consistent with every prior commit on this ticket) and pushed:
`aiorders-api@57f8c4b`, `aiorders-admin-hub@63be255`. Frontmatter `branch:`
and `updated:` refreshed.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`building`/`eng-manager`): fixing a failed review's findings is build work,
and `in-review` is only reached by a fresh review-plus-quality session
actually passing it. `machine_wip` unaffected, still 4/1 (draining
naturally, unrelated to this pass). Approver-facing WIP and approval cap
both unaffected — no gate touched.

`chained: ENG-008` — `building` is agent-owned (the next hop is code review
+ quality, combined, round 2), not the approver, not blocked, not terminal,
not held by a cap. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: see below.

## 2026-08-31 — continue ENG-023: tech design written, held at `designed` by the WIP cap

`continue` event pass, context `ENG-023`. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
whole-board: both exit 0, clean.

Picked up the hand-off the 2026-08-29 `designed`-entry left for this exact
session: the tech design itself, not yet written. Investigated the live
code first (`restaurant-portal`'s feedback page and API client,
`aiorders-api`'s `feedback.ts`/`catering.ts`/`utils.ts`/`index.ts`, the
`restaurant_feedback` migration history and its closest sibling precedent)
and confirmed first-hand the `getFeedback` tenant-isolation bug `ENG-022`
already found (wrong argument order into `verifyRestaurantAccess`, plus a
truthy-object check that never actually denies). Wrote
`agents/architect/designs/ENG-023-feedback-status-and-notes.md`: two new
columns on `restaurant_feedback` (`status`, `notes`), a new `update_feedback`
action modeled on `catering.ts`'s fetch→verify→update→return shape while
keeping `feedback.ts`'s own throw convention for failures (reasoned
explicitly against an apparent PRD/`ENG-022` conflict that resolves cleanly
once shape and error-convention are treated as separate questions), and a
non-blocking sequencing note with `ENG-022` on the access-check helper's
live name. One-way doors: none — status vocabulary and the no-audit-log
choice both decided directly, both reversible. No ADR: no one-way door, no
standards deviation, no accepted risk. Full detail on the ticket's own log.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`designed`/`architect`). The exit condition for `designed` is now met, and
with no one-way door this ticket's next stop would be `ready` directly, no
G2 — **not taken this pass.** Machine WIP re-verified fresh from every
ticket file's own frontmatter, not the cached header: `ENG-008`/`ENG-013`
`building`, `ENG-009`/`ENG-010` `ready` — 4/1, still over cap, still
draining naturally. Same precedent already on record for `ENG-014`/`ENG-015`:
a clean, one-way-door-free design still holds at `designed` until the count
clears. `ENG-023` now joins `ENG-014`/`ENG-015`/`ENG-025` there.

**Notify sweep:** nothing raised — no gate opened this pass. **Dead-end
sweep** (scoped to this event's contract): no broken chain on this ticket's
own prior entries beyond the one this pass resumed.

`chained: none` — `designed`, held by the machine WIP cap (4/1, re-verified
above), not blocked and not waiting on a human specifically, but firing
`continue ENG-023` now would only re-discover the same cap with no new work
to do. Re-check once a `scheduled`/`watch`/`continue` pass drains
`ENG-008`/`ENG-009`/`ENG-010`/`ENG-013` below the cap. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-023`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-30 — continue ENG-013: the missing test already existed, found undocumented rather than written

`continue` event pass, context `ENG-013` — the re-fire from the `scheduled`
sweep above. Narrow scope per the event's own contract (resume this ticket
from its current state; no board-wide sweep). Mode check clean. Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

Went to write the Deno test file round 1's code review asked for and found
one already on the branch: `foodswipe.test.ts`, commit `c95b25b`, same
automation identity (`businesspilotcare-gif`) as the ticket's own recorded
build commit, already pushed. Nothing in tracked state knew about it — not
this ticket's own log, not `business-os`'s own `git log` (`main` confirmed
0/0 with `origin/main`), not either dated trace log on this host. Root
cause, per `proposals.md`'s existing 2026-08-29 row: this instance runs on
two hosts and `traces/` is host-local and `.gitignore`d, so a pass that ran
on the other host, did the work, and pushed it leaves nothing here if it
never reached (or never pushed) its own ticket-log update. `deno` isn't
installed on this Mac host at all, so verification was by hand: read both
files in full and traced all 17 new test cases against the live handler
logic, confirming they correctly cover the three gaps round 1 named
(access-gate negative case, stage validation, `source='foodswipe'`
tenant-scoping) with no bugs found. Accepted the existing commit rather than
duplicating it; added a short PR-body addendum on the ticket noting the
file and two small additive fixes it carries (exported types, a
`Boolean(...)` wrap with no behavior change). Full investigation and
verification detail on `ENG-013`'s own ticket log.

**0 net frontmatter transitions** — `state` was `building` at pass start and
remains `building`: the work was already complete before this pass began,
so there was no further machine-owned state to advance into within this
same session regardless (`eng_build_loop.md`'s "a pass stops after
`building` on purpose" is state-based, not effort-based). `machine_wip`,
approver-facing WIP, and approval cap all unaffected — no gate raised or
resolved.

**Proposal filed** (`proposals.md`): a build hop has no step that checks a
ticket's recorded commit hash(es) against its remote branch before assuming
code still needs writing — cheap to add (`git log {hash}..origin/{branch}`
per linked repo), and would have surfaced this in one command instead of a
multi-step investigation. Distinct from the existing 2026-08-29 row (that
one is about a dropped-event incident item lacking detail; this is about a
pass that finished correctly and left no incident at all).

`chained: ENG-013` — `building` is agent-owned (the review+quality combined
hop is next), not the approver, not blocked, not terminal, not held by a
cap. Fired `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
ENG-013` before exiting. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-30 — continue ENG-008: code review round 1 FAIL, bounced to building

`continue` event pass, context `ENG-008` — this fire's own turn at the front
of `traces/.pending`, re-fired by the `scheduled` sweep above after the
original 2026-08-29 fire never ran. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

Both branches were cut before `ENG-007`/`ENG-011` merged to `main` (this same
board's own `scheduled` entry above), so a raw two-dot diff against current
`main` shows spurious deletions of both tickets' shipped work. Read the
isolated single-commit patch on each branch instead (`git show --stat` /
merge-base diffing) to avoid reviewing noise that was never this ticket's.

Ran the code-review gate's automatic-failure scan: hit **#10** again —
`influencers.ts`'s new admin-gated `PATCH` path (`hasInfluencerAdminAccess`,
`updateInfluencer`) carries **zero test coverage**, identical shape to
`ENG-013`'s own round 1 failure one day earlier, same repo. Also found an
independent correctness bug: `Influencers.tsx`'s `openInfluencer` defaults
`accepts_paid`/`accepts_barter` via `null ?? !null`, which evaluates `true`
in JavaScript — so the 51/306 production rows where the preference is
genuinely unset get a fabricated "accepts paid" value written back on the
next save of *any* field, contradicting the migration's own deliberate
null-preserving backfill. Full detail on the ticket's own log. No receipt
written; findings logged on the ticket and in
`agents/principal-engineer/notebook/2026-08-30-review-log.md`. QA's hop not
run this round — discarded per the combined-hop design.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`building`/`eng-manager`); the gate was reached and immediately routed
back on the fail verdict. `machine_wip` unaffected, still 4/1.
Approver-facing WIP and approval cap both unaffected. Two observations filed
(`observations.md`): second occurrence of the automatic-failure-#10 shape in
two days (same repo, same handler family); `ENG-008`'s frontmatter missing
`time_estimate`/`time_spent`/`time_remaining` despite both
`definition-of-done.md` and the ticket template calling for them.

`chained: ENG-008` — `building` is agent-owned (both findings are the next
hop's work), not the approver, not blocked, not terminal, not held by a cap.
Fired `/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-008`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-30 — scheduled (launchd): two silent merges shipped, three broken chains resumed

`scheduled` event pass, context `launchd`, the 15:30 safety-net slot (fired
15:46, delayed by an in-flight `continue ENG-023` attempt that ran until
13:00 and a lock hand-off after). Mode check clean (business-os `.env` →
`MODE=active`). This pass's own transcript was interrupted once mid-run by
the host machine sleeping — resumed from the same session, nothing lost.

**Found a rough day on disk before touching anything.** `git status` showed
six files uncommitted from the 2026-08-29 `watch` pass that processed
`ENG-023`'s G1 (never committed before this pass started) — read in full via
`git diff` before proceeding, confirmed coherent and already fully described
by that pass's own ticket-log and journal entries, left as-is to commit
together with this pass's own work rather than committed prematurely
mid-investigation. `traces/eng-loop-2026-08-30.log` showed `continue ENG-023`
had failed twice today (`401 OAuth access token has been revoked` at 02:13;
`ENOTFOUND` at 09:31, after only 5 file reads) and been **dropped after 3
attempts total** (across both days) — `inbox/2026-08-30-eng-events-dropped.md`
raised automatically by the trigger script itself, unnotified (its own first
notify attempt hit the same `ENOTFOUND` class of failure).

**Merge detection (step 5) run against every ticket sitting on an L1 PR or
possible PR, not just the one named by the failed `continue`** — this is
what a `continue` event's own narrower contract can never do, and exactly
why today's two failed `ENG-023` attempts left this undetected for hours:

- `ENG-007` (`ready-to-ship`, no gate item ever raised — blocked by a
  Saturday window-hold the same-day L1 correction had already made moot):
  `git merge-base --is-ancestor` **MERGED**; independently confirmed via
  `gh pr view 4` (`mergedAt: 2026-08-30T02:38:08Z`, approver's own account).
  Receipts verified fresh from disk (all 4 present), `eng-gate-check.sh
  ENG-007` exit 0. Carried `ready-to-ship → shipped → verified`. Release
  record: `agents/devops/releases/2026-08-30-aiorders-api-ENG-007.md`.
- `ENG-011` (`blocked`, merge request raised 2026-08-29, never answered —
  its own text told the approver a reply wasn't required): both repos
  checked independently — `aiorders-api` PR #3 **MERGED** 00:12:50Z,
  `aiorders-admin-hub` PR #3 **MERGED** 00:13:30Z, git ancestry confirmed on
  both before treating the ticket as shippable (first two-repo merge
  detection on this board). Receipts verified (3 + migration, all present),
  `eng-gate-check.sh ENG-011` exit 0. Carried `blocked → shipped →
  verified`. Merge-request item closed to `inbox/_handled/`. Release record:
  `agents/devops/releases/2026-08-30-ENG-011-aiorders-api-and-admin-hub.md`.

Both close-outs done to the same standard `ENG-006` set two days ago:
receipts checked before advancing (never trusted from the PR body alone),
what an L1-with-no-CI/CD project can honestly attest to at `shipped`
(deploy status recorded as unknown where no evidence exists, rather than
inferred), and acceptance criteria re-confirmed against the merged tree with
any live-only gap named and carried forward, not hidden. Both PRDs' `status`
moved to `verified`. Both journaled in `decision-journal.md`.

**Dead-end sweep found three broken chains, not one.** `ENG-023`'s own
`continue` chain (fired correctly at the end of the 2026-08-29 `watch`
entry above) is the one this pass was triggered to investigate — root-caused
(both failures infra-level, neither implicating the ticket) and re-fired,
with the diagnosis recorded in `inbox/2026-08-30-eng-events-dropped.md`
before re-firing, per that item's own recommendation. Checking the rest of
the board for the same shape (a ticket ending its last log entry with
`chained: ENG-XXX` and no evidence the fire ever ran) surfaced two more:
`ENG-008` (`building`, chained at end of its 2026-08-29 build entry, waiting
on the combined review+quality hop) and `ENG-013` (`building`, chained at
end of its code-review-fail entry, waiting on the missing test). Neither
`continue (ENG-008)` nor `continue (ENG-013)` appears anywhere in
`traces/eng-loop-2026-08-29.log` or `-30.log` — only `ENG-023`'s two failed
attempts and this pass ever drained. All three re-fired; the trigger queue's
own duplicate-collapse rule makes this safe even where a fire is merely
still queued rather than genuinely lost, so no risk of double-running any
hop. `ENG-007`'s own former hold (the Saturday window note in its prior log
entry) resolved itself via the merge discovery above rather than needing a
fourth chain-fire.

**4 tickets touched, 5 net transitions** (`ENG-007` ×2, `ENG-011` ×2,
`ENG-023` dead-end resume with no state change), all within per-ticket caps.
`machine_wip` 5/1 → 4/1 (`ENG-007` left the counted range; still over cap,
still draining naturally — `ENG-009`/`ENG-010`/`ENG-008`/`ENG-013` remain).
Approver-facing WIP 1/2 → 0/2, fully clear. Approval cap 1/3 → 0/3, fully
clear — both caps clear at once for the first time recorded on this board.

**Notify sweep:** `inbox/2026-08-30-eng-events-dropped.md` raised and
notified this pass (its own automatic first attempt had failed on the same
network error it was reporting); `notified:` stamped. Nothing else new to
raise or nudge.

**Observations filed** (`observations.md`, two rows): merge detection's
`continue`-vs-`scheduled`/`watch` coverage gap made concrete by today's
timeline; fifth and sixth data points of this approver merging L1 PRs
directly on GitHub rather than through the tracked channel.

**Chained:** `ENG-007` — none, terminal (`verified`). `ENG-011` — none,
terminal (`verified`). `ENG-008` — `ENG-008`, re-fired
(`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-008`).
`ENG-013` — `ENG-013`, re-fired (`/bin/sh .../eng-trigger.sh continue
ENG-013`). `ENG-023` — `ENG-023`, re-fired (`/bin/zsh .../eng-trigger.sh
continue ENG-023`). All three fires happen after this board update and the
commit that follows it, per this pass's own closing instructions. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: run clean
before the fires below (see traces for the exact invocation and output).

## 2026-08-29 — watch (launchd): ENG-023's G1 answered and processed, awaiting-scope → designed

`watch` event pass, context `launchd`. Mode check clean (business-os `.env`
→ `MODE=active`; instance `config/config.yaml` → `mode:` not set, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-023`) and whole-board: both exit 0, clean — run fresh, not taken on
any prior pass's own account.

**Swept all three watched inboxes per this event's own contract.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` — nothing new. `inbox/` held exactly two live items:
`2026-08-29-eng023-g1-scope.md`, found answered (**approved**, `decided:
2026-08-29T23:38:32.834274+00:00`, no additional comment) since the last
pass touched it; and `2026-08-29-eng011-merge-request.md`, re-checked fresh
and still unanswered (`decision:` empty) — never inferring approval from
silence, nothing to act on there.

**Found the repo mid-recovery from an unrelated `git stash pop` conflict**
on `_index.md`/`_index-archive.md`/`observations.md`
(`stash@{0}: On main: local instance state before marketing port pull`),
resolved to a clean tree matching `HEAD` by something else between this
pass's first and second `git status` check, mid-sweep. Out of scope for
this event — not touched; the stash itself is untouched too. Full detail in
`observations.md` and on `ENG-023`'s own ticket log.

Processed `ENG-023`'s G1: PRD `status: approved`
(`agents/product-manager/specs/ENG-023-feedback-status-and-notes.md`), gate
item moved to `inbox/_handled/` with a processed footer, journaled in
`agents/eng-manager/config/decision-journal.md`. Ticket `awaiting-scope →
designed`, `owner: approver → architect`. **Design work itself not started
this pass** — same reasoning `ENG-014`'s own `watch`-event G1 processing
used: implementation-adjacent work against a project with real customer
data belongs in a dedicated `continue ENG-023` session, not this event's
inbox-sweep scope. Full detail on `ENG-023`'s own ticket log.

**1 transition** (`awaiting-scope → designed`), well under the cap of 4.
Approver-facing WIP 2/2 → 1/2 (`ENG-023` off the count; `ENG-011`'s merge
request the one remaining slot). Approval cap 2/3 → 1/3 (`ENG-023`'s gate
item now in `inbox/_handled/`). Machine WIP unaffected, still 5/1 —
`designed` isn't in the counted range, and the cap already holds
`ENG-014`/`ENG-015` at `designed` for the same reason, so `ENG-023` joining
them there (rather than `ready`) once its design lands is expected, not a
new constraint.

**Capacity freed, not spent on anything else this pass** — same precedent
`ENG-014`'s `watch` entry set: dispatching the freed approver-facing
WIP/approval-cap slot onto a different waiting ticket (`ENG-016` through
`ENG-021`, all G1-drafted) is left for a future `scheduled`/`watch`/
`continue` pass.

One observation filed (`observations.md`): the concurrent git-stash-conflict
recovery found mid-sweep, and the reminder that this instance's board files
can change under a pass from outside the build loop entirely, not just via
the approver answering a gate.

`chained: ENG-023` — `designed`, owned by `architect`, an agent-owned
state; not the approver, not blocked, not terminal, not held by a cap
(design/shaping work is exempt from the machine-WIP limit). Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-023`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-023`) and whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — continue ENG-013: code review round 1 FAIL, bounced to building

`continue` event pass, context `ENG-013` — this fire's own turn at the front
of `traces/.pending` finally reached. Narrow scope per the event's own
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

Read the actual diff fresh from both worktrees via `git diff`/`git show`
against the branch (`aiorders-api@ac4efba`, `aiorders-admin-hub@a1c3bdf`)
rather than checking either worktree out — both were sitting on `ENG-008`'s
branch, same as the building pass itself found. Ran the code-review gate's
automatic-failure scan before any deeper review: hit **#10** — the two new
authz-gated write actions (`setStageOverride`/`resetStageOverride` in
`foodswipe.ts`, tenant-scoped by `.eq('source', 'foodswipe')`, the diff's
own "review hardest" line) carry **zero test coverage**, against direct
precedent from `ENG-007`/`ENG-011` on this same repo. No receipt written;
verdict and finding logged on the ticket and in
`agents/principal-engineer/notebook/2026-08-29-review-log.md`. QA's hop not
run this round — discarded per the combined-hop design.

**0 net frontmatter transitions** — `state`/`owner` unchanged
(`building`/`eng-manager`); the gate was reached and immediately routed
back on the fail verdict. `machine_wip` unaffected, still 5/1.
Approver-facing WIP and approval cap both unaffected. One observation filed
(`observations.md`): first code-review failure recorded on this board.

`chained: ENG-013` — `building` is agent-owned (the missing test is the
next hop's work), not the approver, not blocked, not terminal, not held by
a cap. Fired `/bin/sh departments/engineering/lib/eng-trigger.sh continue
ENG-013` before exiting. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — continue ENG-011: both L1 PRs opened, ready-to-ship → blocked

`continue` event pass, context `ENG-011` — this fire's own turn at the front
of `traces/.pending`. Narrow scope per the event's own contract (resume this
ticket from its current state; no board-wide sweep). Mode check clean
(business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-011`) and whole-board: both exit 0, clean.

Read the current `skills/release-runner/SKILL.md` rather than the release-
window question this ticket's own prior log entry had left open: the skill
was corrected earlier today to state that the window check is L2/L3-only and
never applies to L1, and both of this ticket's projects are L1 — so no hold
applied. Verified all four upstream gates fresh from their own receipt files
(migration, code review, quality, security — all **pass**, one named
non-blocking gap on the missing live-Postgres run). Re-checked both `_eng`
worktrees before touching them (both were sitting on `ENG-008`'s branch, not
this ticket's — confirmed clean first so nothing of `ENG-008`'s was at risk),
checked out `feat/ENG-011-client-stage-health-visibility` in both, confirmed
commit hashes matched every receipt exactly, checked for an already-open PR
on each repo (none), then opened both: `aiorders-api`
https://github.com/harsimranwalia/aiorders-api/pull/3,
`aiorders-admin-hub` https://github.com/harsimranwalia/aiorders-admin-hub/pull/3.
Restored both worktrees to `ENG-008`'s branch afterward. Wrote the merge
request (`inbox/2026-08-29-eng011-merge-request.md`), ran `eng-notify.sh
raise` (hit the same standing `SLACK_WEBHOOK_URL unset` gap every gate item
today has hit — not new), stamped `notified:` by hand. Ticket →
`ready-to-ship → blocked`, `blocked_on: approver`, `blocked_from:
ready-to-ship`, owner `devops → approver`. Full detail on the ticket's own
log.

**1 transition**, well under the cap of 4. `machine_wip` 6/1 → 5/1 (`ENG-011`
now outside the counted range). Approver-facing WIP 1/2 → 2/2 (at the limit,
not over — an already-gated ticket reaching its next gate, not a new start,
same reasoning `ENG-005` used at this identical boundary). Approval cap
1/3 → 2/3.

One observation filed (`observations.md`): the skill correction and this
ticket's own prior log entry disagreed on an open policy question, and the
current skill file is what should win — worth a future pass trusting that
ordering rather than re-litigating a stale ticket-log note.

`chained: none` — `blocked`, `blocked_on: approver`; the human gate this hop
was driving toward. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-011`) and whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — continue ENG-024: shaped, held — machine WIP still 6/1 over cap, no slot free

`continue` event pass, context `ENG-024` — its own chain fire from the
`intake` pass that shaped it. Narrow scope per this event's own contract:
this ticket only. Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass gate check: exit
0, clean, both scoped (`ENG-024`) and whole-board.

Re-checked fresh rather than trusted the board's cached header: all six
machine-WIP tickets' own frontmatter (`ENG-007` ready-to-ship, `ENG-008`
building, `ENG-009` ready, `ENG-010` ready, `ENG-011` ready-to-ship,
`ENG-013` building) — count unchanged at 6/1, still over the cap of 1. Per
`eng_build_loop.md` step 6, the To-do column is the only place a new start
is drawn from, and "there is exactly one slot [that] does not free until
the ticket occupying it reaches `shipped`" — `ENG-024` (severity P1, fast
lane, `shaped`) cannot enter `building` this pass regardless of severity;
nothing in the loop's dispatch rule exempts P1 from the WIP cap. Only the
unrelated proposal-batching P0 carve-out (step 3) mentions P0 at all, and
that gate doesn't apply here since ENG-024 already has an approved ticket.
`agents/eng-manager/inbox/` empty — no technical-intake item for this
ticket; G1 was already correctly auto-skipped (bug type, fast lane), so
there is no gate item to check either. Ticket correctly stays at `shaped`.

**0 transitions.** `chained: none` — held by the machine WIP cap (6/1, no
free slot); one of the explicit do-not-chain conditions. Recorded on the
ticket's own log.

One observation filed (`observations.md`): the `intake` pass that shaped
this ticket fired its chain without checking the machine-WIP cap, which was
already known full at the time (six tickets already in flight) — this pass
is the cost of that gap, one hop spent to re-derive a hold the shaping pass
could have recognized itself.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-024`) and whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — continue ENG-022: architect's design written, shaped → designed

`continue` event pass, context `ENG-022` — this fire's own turn at the
front of `traces/.pending`, reached after the approver's plain "approved"
acknowledgement on the P0 incident notice (no priority change, nothing
else to act on). Narrow scope per this event's own contract — this ticket
only. Mode check clean. Pre-pass gate check: exit 0, clean, both scoped and
whole-board.

Read the live `aiorders-api` worktree before designing against it rather
than trusting the PRD's summary alone; confirmed all 19 broken call sites
and the 4 correct contrast files match exactly. Found one thing the PRD
didn't surface: `utils.ts` already contains a correct, unused throwing
wrapper (`verifyRestaurantAccessLegacy`, called from nowhere in the repo) —
promoted it (renamed, `@deprecated` dropped) instead of designing a new one.
Design written: `agents/architect/designs/ENG-022-brand-portal-tenant-isolation-broken.md`
— fixes each of the 5 broken files per its *own* pre-existing error
convention (throw vs. `{success:false}`) rather than unifying all 9, which
would be a refactor bundled into a P0 bug fix. Test plan: colocated
`Deno.test` files with a stubbed Supabase client, proving the negative case
per call site with no live project and no new CI wiring. No one-way door,
no ADR. Full detail on the ticket's own log.

**1 transition** (`shaped → designed`), well under the cap. `ENG-022` stays
short of the counted `ready..ready-to-ship` machine-WIP range (6/12
unaffected); `security`-typed, no G1/G2 raised, approver-facing WIP and
approval cap both unchanged (1/2, 1/3).

One observation filed (`observations.md`): `brand-portal/`'s two
pre-existing, unrelated error-response conventions, so a future pass
doesn't mistake the split for something this ticket introduced.

`chained: ENG-022` — `designed`, owned by `eng-manager` next (no one-way
door, so `awaiting-decision` does not apply), an agent-owned state; firing
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-022`
before this pass exits. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`) and
whole-board: exit 0, clean, no `WAIVED:` lines.

## 2026-08-29 — scheduled schtasks: safety-net sweep — processed ENG-025's G1, raised ENG-023's, recovered five passes of uncommitted work

`scheduled` event pass, context `schtasks` — the four-times-daily safety-net
sweep, drained immediately behind the `decision ENG-015` pass above in the
same held lock (`traces/.loop.lock/pid 1909`, confirmed alive throughout).
Whole-board sweep per this event's own contract, not one named ticket. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/`, and `inbox/requests/` all empty. Nothing to
shape, nothing to batch as a proposal.

**Gate returns:** `inbox/` held exactly one file,
`2026-08-29-eng025-g1-scope.md` (`decision: approved`,
`decided: 2026-08-29T22:22:18.827452+00:00`). Processed:
`ENG-025` `awaiting-scope → designed`, owner `approver → architect`; PRD
`status: approved`; gate item moved to `inbox/_handled/`; journaled
(`decision-journal.md`). That freed both the approver-facing WIP slot and
the approval-cap slot ENG-025 held — reused in this same pass, per
`_index.md`'s own standing note, to raise `ENG-023`'s G1 (fully drafted
already in its PRD's Decision section, nothing written fresh): `ENG-023`
`shaped → awaiting-scope`, owner `product-manager → approver`;
`inbox/2026-08-29-eng023-g1-scope.md` raised, `eng-notify.sh raise` run
(logged `SLACK_WEBHOOK_URL unset`, same open gap every gate item today has
hit), `notified:` stamped manually. Net: approver-facing WIP and approval
cap both end this pass exactly where they started (1/2, 1/3), now against
`ENG-023` instead of `ENG-025`. `ENG-016`–`ENG-021` (also G1-drafted)
deliberately left unraised — see `ENG-023`'s own log for why only the one
explicitly-earmarked ticket was raised rather than filling every free slot.

**Merge detection:** no ticket sits at `blocked` anywhere on the board — no
L1 PRs to check ancestry on this pass.

**Dispatch / dead-end sweep, whole board:** `ENG-007` (`ready-to-ship`)
re-confirmed correctly held — release window still closed (Saturday);
resumes naturally Monday. `ENG-009`/`ENG-010` (`ready`) re-confirmed
correctly held pending `ENG-008` reaching `in-review` or later — neither
worktree shows a branch or build started yet. `ENG-011`'s
`chained: ENG-011` already fired and sits genuinely queued in
`traces/.pending`, not stale. No broken chain found on any in-flight
ticket beyond the two already repaired by the two passes immediately
above. Removed `_index-archive.md.tmp.4632.31c9ee9459a2`, the stale
5,027-line crash-artifact temp file `observations.md`'s immediately
preceding row flagged as safe to clear on a dead-end sweep — verified
against that row's own description (size, mtime, stale content) before
deleting.

**Uncommitted-work recovery, the main substance of this pass.** Pre-pass
`git status` showed nothing committed since `a143d9b` despite the board's
own narrative recording five further passes' worth of real, verified work
since: `continue ENG-008` (built the influencer admin-edit path),
`continue ENG-013` (built the FoodSwipe stage-override path), the
`ENG-014`/`ENG-015` chain repairs, and the `ENG-022`/`ENG-023` incident/
question processing — including the `eng-loop-halted` repair pass's own
config-path fix for `read_plan_budget()` (the actual cause of today's
40-hop ceiling firing early). That repair pass's own log states it
committed three of those files "alongside this pass's own changes," but a
fresh `git status` at this pass's start showed all three still modified —
the commit most likely never ran. Verified each change against its own
ticket log before trusting it (per this instance's standing practice, and
the specific lesson `observations.md` names for exactly this shape of
mismatch) rather than committing blindly. Committed the accumulated,
verified work in this pass — see the commit itself for the exact file
list; the stray temp file above was deleted, not committed, and nothing
else in the tree looked suspicious (no secrets, no `.env`, no unrelated
files). Filed as its own `observations.md` row for the pattern (a pass's
own narrated git action not matching the filesystem — a new variant of an
already-seen lesson).

**Notify sweep:** `ENG-023`'s new item raised and stamped this pass (see
above). No item found with `notified:` older than 24h and no `decision:` —
nothing to nudge. Approval cap 1/3, not full — no stall.

**Journal:** `ENG-025`'s G1 answer added to `decision-journal.md`.

`chained: ENG-025` — fired this pass (see that ticket's own log);
`ENG-023` and all `ready`/`ready-to-ship` tickets correctly recorded
`chained: none` (approver-owned or deliberately held) and are not
re-chained here. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean, no `WAIVED:` lines.

## 2026-08-29 — decision ENG-015: G1 already processed by the same dying `watch` pass as ENG-014, its own recorded chain never fired either — repaired

`decision` event pass, context `2026-08-29-eng015-g1-scope.md` — this
event's own queued fire, drained behind the `decision ENG-014` repair pass
immediately before it (`pass end: decision (exit 0, 685s)` at 15:33:53 →
`draining queued event: decision (2026-08-29-eng015-g1-scope.md)`,
15:34:45, no gap, one duplicate collapsed). Mode check clean. Pre-pass gate
check: exit 0, clean, scoped (`ENG-015`) and whole-board.

Exactly the gap the immediately-preceding pass predicted and flagged in
`observations.md`: `ENG-015`'s G1 was genuinely fully processed (approved,
`awaiting-scope → designed`, owner `architect`, journaled — all verified
fresh against `inbox/_handled/`, the PRD, and `decision-journal.md` rather
than trusted), but its own recorded `chained: ENG-015` line never actually
fired — same dying `watch` pass (pid 36150), same absence from
`traces/eng-loop-2026-08-29.log` and from `traces/.pending` beforehand.

**Action:** re-fired `/bin/sh
departments/engineering/lib/eng-trigger.sh continue ENG-015` directly.
Confirmed on `traces/.pending` afterward (`1 continue ENG-015`) and via
`traces/.loop.lock/pid` (`1909`) confirmed alive with `ps -W` — queued
correctly behind this still-running pass rather than lost again. No ticket
state changed.

**0 transitions**, no cap impact — this was a chain repair, not new gate
or state movement. This closes out both halves of the pair `ENG-014`'s own
repair pass surfaced; no further tickets carry this shape as far as this
pass found.

`chained: ENG-015` — re-fired and confirmed queued this pass (see above).
Post-pass gate check: exit 0, clean, both scoped and whole-board. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-015-agency-reseller-brand-scoping.md`).

## 2026-08-29 — continue ENG-013: built the stage-override column, handler, and UI across both repos, ready → building

`continue` event pass, context `ENG-013`, its turn at the front of
`traces/.pending` finally reached. Narrow scope per the event's own
contract. Mode check clean.

Pre-pass gate check arrived flagged (exit 2, all of `ENG-013`..`ENG-024`
reported "not a regular file"). Investigated rather than trusted: `stat`
confirmed every file is a normal regular file, and a fresh re-run (scoped
and whole-board) returned exit 0 clean. Transient — the injected report was
captured mid-write during the prior pass's own commit
(`1a6fe83`). Nothing to fix.

Both `_eng` worktrees existed, sitting on `feat/ENG-011-...` (still owed —
`ENG-011` hasn't opened its PR yet). `aiorders-admin-hub` carried the same
benign `package-lock.json` `peer:true` drift `ENG-011`'s own recovery
already named — stashed, labeled, not discarded, not committed. Branched
both repos fresh off `origin/main` as `feat/ENG-013-foodswipe-funnel-stage-control`.

Built per the design: one nullable `foodswipe_stage_override` column on
`profiles` (six-value `CHECK`); `classifyStage()`'s caller now prefers it;
two new gated, source-scoped write actions
(`/foodswipe/stage/{set,reset}`) in `aiorders-api`. Per-card stage dropdown
+ dialog (styled after `Leads.tsx`) and a "Manually set" badge in
`aiorders-admin-hub`. Self-tested: `deno check` clean, `npm run lint`
(zero new issues — the repo's 150 pre-existing errors are all in files
this ticket didn't touch), `npm run build` clean. Live-verified read-only
via Supabase MCP against the real `aiorders-api` project
(`bmnmnejwdxbcqinqkwko`): schema assumptions, table scale (528 rows, 36
`source='foodswipe'`), and non-applied migration status all confirmed.
Database migration doc written
(`agents/database/migrations/ENG-013-foodswipe-funnel-stage-control.md`).
Both branches committed and pushed; PR bodies drafted in the ticket's own
log (no PR opened yet — that's devops's release step). Artifact-enumeration
grep for "foodswipe" across instance+department docs found no
instruction/map conflicts, only one harmless location-citation drift in
`ENG-009`'s design doc, left alone.

**1 transition** (`ready → building`), well under the cap — the next hop
(review + quality, combined) is a fresh session's work by design. No cap
change; `ENG-013` stays inside the counted `ready..ready-to-ship` range.

`chained: ENG-013` — `building` is agent-owned (principal-engineer + qa
next). Fired `continue ENG-013`. Post-pass gate check: exit 0, clean, both
scoped and whole-board. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — continue ENG-008: built the preference/rating/collaboration-count edit path across both repos, ready → building

`continue` event pass, context `ENG-008`, its turn at the front of
`traces/.pending` finally reached. Narrow scope per the event's own
contract. Mode check clean. Pre-pass gate check: exit 0, clean, both scoped
and whole-board.

Both `_eng` worktrees existed, clean, sitting on `ENG-013`'s own
still-in-flight branch — not touched. Fetched both; `origin/main` unchanged
since `ENG-013` last branched. Branched both fresh as
`feat/ENG-008-influencer-admin-management`, migration timestamp
`20260829220000` chosen deliberately clear of `ENG-013`'s unmerged
`20260829200000`.

Built per the design: `staff_rating`/`collaboration_count` plus
`accepts_paid`/`accepts_barter` (backfilled from `barter_visit`, which is
left untouched) on `influencers`; new `GET`/`PATCH
admin-portal/influencers/{id}` (admin/sub-admin gate, same narrower pattern
`ENG-007` and `ENG-013` both use); edit form added to `aiorders-admin-hub`'s
previously entirely-read-only influencer detail dialog. Self-tested: `deno
check` clean on the new handler in isolation, `npm run lint` zero new
issues (150 pre-existing, same count `ENG-013` recorded), `npm run build`
clean.

**Step 6b's artifact-enumeration grep caught a real bug before it shipped**:
`ENG-009`'s design doc (sibling ticket, same handler, sequenced to build
after this one) had already recorded `admin-portal/index.ts`'s CORS
`Access-Control-Allow-Methods` as missing `PATCH` — exactly the method this
ticket's design specifies. None of the three local self-tests would have
caught it (a CORS failure only shows up against a real browser preflight).
Fixed in this same hop by widening the allow-list in both files that carry
it. Full detail, plus the separate (deliberately not acted on)
`collaboration_count` naming-overlap flag from the same doc, on the
ticket's own log.

Both branches committed and pushed (`aiorders-api@e240767`,
`aiorders-admin-hub@f2ea36c`); no PR opened yet — devops's step. PR bodies
drafted on the ticket's own log. Database migration doc written
(`agents/database/migrations/ENG-008-influencer-profile-admin-management.md`).

**1 transition** (`ready → building`), well under the cap — the next hop
(review + quality, combined) is a fresh session's work by design. No cap
change; `ENG-008` stays inside the counted `ready..ready-to-ship` range.

`chained: ENG-008` — `building` is agent-owned (code review + quality
next). Fired `continue ENG-008`. Post-pass gate check: exit 0, clean, both
scoped and whole-board. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-008-influencer-profile-admin-management.md`).

## 2026-08-29 — decision ENG-014: G1 already processed by an earlier `watch` pass, but its own recorded chain never fired — repaired

`decision` event pass, context `2026-08-29-eng014-g1-scope.md` — this
event's own queued fire, drained behind a `watch`/`schtasks` fire that
reached the same gate item first. Mode check clean. Pre-pass gate check:
exit 0, clean, scoped (`ENG-014`) and whole-board.

Verified fresh rather than assumed stale: the gate item is genuinely
already in `inbox/_handled/` with a "Processed" footer, `ENG-014` is
genuinely at `designed`/`architect`, and `decision-journal.md` genuinely
carries the G1 row — the earlier `watch` pass's substantive work all
checks out. What doesn't check out is its own `chained: ENG-014` line:
`traces/eng-loop-2026-08-29.log` shows no `continue (ENG-014)` ever ran,
and it wasn't sitting in `traces/.pending` either. That `watch` pass's
process (pid 36150) died before exiting cleanly (`clearing stale lock
(2103s old, owner 36150 gone)`) — almost certainly right around writing
that log line, before the shell fire behind it ever executed. `ENG-015`
carries the identical shape from the same dying pass; out of scope for
this event (named ticket is `ENG-014` only), flagged in `observations.md`
instead.

**Action:** re-fired `/bin/sh
departments/engineering/lib/eng-trigger.sh continue ENG-014` directly.
Confirmed on `traces/.pending` afterward and via the trigger's own stderr
(queued correctly behind this still-running pass rather than lost again).
No ticket state changed — the architect's actual design work stays a
dedicated session's job, which the now-genuine chain will launch.

**0 transitions**, no cap impact — this was a chain repair, not new
gate or state movement.

`chained: ENG-014` — re-fired and confirmed queued this pass (see above).
Post-pass gate check: exit 0, clean, both scoped and whole-board. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-014-restaurant-qr-media-self-service.md`).

## 2026-08-29 — continue ENG-007: verified fresh, held at `ready-to-ship` — release window closed for the weekend

`continue` event pass, context `ENG-007`, the chain fire from the pass that
reached `ready-to-ship`. Narrow scope per the event's own contract. Mode
check clean. Pre-pass gate check: exit 0, clean, both scoped and
whole-board.

Verified fresh rather than trusted, given this ticket's two prior
unrecorded-build recoveries: the `aiorders-api` worktree confirms
`loyalty-system` unchanged at `2aec86f`, tree clean, not merged into
`origin/main`, and no PR open against it (`gh pr list` shows only `ENG-006`'s
own already-merged PR #2) — genuinely still `ready-to-ship`, not a third
unrecorded advance.

Release window re-checked fresh, as the prior entry explicitly asked the
next hop to do: Saturday 2026-08-29, 14:09 local, inside
`releases.block_weekends`. `ENG-006` hit this identical boundary on a Friday
before the 15:00 cutoff and proceeded to open its PR; this lands outside the
window. Consistent with that precedent — this department treats the PR-open
step itself, not just the eventual merge, as the release-window-gated
action — and with this pass's own prompt, which names "a closed release
window" as a chaining exclusion alongside the approver: no PR opened, no
state change.

**0 transitions.** No cap affected either way — what's holding this ticket
is the release window, not WIP or approval capacity.

`chained: none` — release window closed (weekend). Expected to clear on its
own: the next scheduled safety-net pass, or a fresh `continue ENG-007` fire,
landing once the window reopens Monday will find this same state and
proceed to open the PR — this is the guard's first real activation on this
instance (`observations.md`), not previously seen blocking anything. Post-pass
gate check: exit 0, clean, both scoped and whole-board. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).

## 2026-08-29 — decision ENG-013 (presignup-leads question): a third predicted twin no-op — arrived after the fact was already consumed by a scheduled sweep, not by the pass that raised it

`decision` event pass, context
`inbox/_handled/2026-08-29-eng013-presignup-leads-question.md` — same
twin-no-op shape as `ENG-013`'s own G1 logged directly above, and
`ENG-011`'s tickets-question twin before that. Per this event's own
narrower contract (act on the answered gate item, advance only the ticket
it belongs to), scoped to `ENG-013` only — no board-wide sweep. Mode check
clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean.

**Confirmed rather than assumed, and a different shape from the two twins
above.** `traces/eng-loop-2026-08-29.log`: `13:15:10 queue: collapsed 1
duplicate event(s)` fires immediately before `13:15:10 draining queued
event: decision (2026-08-29-eng013-presignup-leads-question.md)`, pass
start `13:15:11`, claude launched `13:16:05`. Unlike the G1 twin directly
above (caught live by the same pass that raised it), this question sat
answered-but-unprocessed until a separate `scheduled` event pass (context
`schtasks`, since rolled to `_index-archive.md`) swept it: read the answer
fresh from `inbox/` (`decision: approved`, "Reading B" — a genuine
pre-signup pipeline with autopilot nurture, `decided:
2026-08-29T11:46:34.557123+00:00`), checked for an existing ticket before
filing a new one per the item's own stated next step, and found one — an
independent `intake` pass the same day had already reached the same
conclusion from a different raw request (the "no autopilot for sales
staff/resellers" card) and filed `ENG-017` (presignup lead nurture
autopilot, `agents/eng-manager/board/ENG-017-presignup-lead-nurture-autopilot.md`,
`state: shaped`), already citing this exact verbatim answer as grounding
evidence in its own Notes. Checked fresh rather than trusted: the gate
item's own processed footer, `decision-journal.md` row 31, `ENG-013`'s own
Notes section (added by that scheduled pass), and `ENG-017`'s own Notes
section all agree — the question is closed against `ENG-017`, not
re-opened, and not filed twice. `ENG-013` itself was never blocked by this
question and needed no action from it either way, then or now.

**0 transitions.** No cap affected — `ENG-013` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
this standing question's approval-cap slot was already freed by the
scheduled pass that closed it — the board header's current cap accounting
(`ENG-014`/`ENG-015`'s G1s only) no longer carries it.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-013` —
fired when this ticket reached `ready` — still sitting in
`traces/.pending`, undrained, behind a longer backlog than either twin
above last saw. Not stuck — no documented sequencing hold against a
sibling ticket, purely FIFO position.

**Notify sweep:** nothing to raise (no new gate item this pass); nothing to
nudge (this question's `notified:`/`decision:` cycle closed same-day, hours
before this pass, well inside the 24h threshold).

Another corroborating occurrence of the open `proposals.md` race
(2026-08-27 row — `eng-trigger.sh` should skip the launch when a
`decision` event's named gate item is already in `_handled/`); not
re-filed or re-logged as its own observation — the existing proposal
already covers this exactly.

`chained: none` — no state change; `ENG-013`'s existing chain (`continue
ENG-013`) is already queued and will run on its own turn; firing a second
`continue ENG-013` now would only queue a duplicate for the collapse logic
to clean up later. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — decision ENG-013 (G1 scope): another predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng013-g1-scope.md`
— same shape as `ENG-011`'s own G1 twin logged above (and, before that,
`ENG-008`'s two gate items, `ENG-009`'s G1, `ENG-010`'s G1). Per this
event's own narrower contract (act on the answered gate item, advance only
the ticket it belongs to), scoped to `ENG-013` only — no board-wide sweep.
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`13:01:35 draining queued event: decision (2026-08-29-eng013-g1-scope.md)`
— no `queue: collapsed` line immediately above it this time, so this is a
single fire reaching its own turn late (raised/`notified:` 11:39:39), not a
duplicate-collapse; a long backlog (`ENG-014`..`ENG-024` work) simply sat
ahead of it in the FIFO. By the time it drained, the same `intake` pass
that raised this G1 had already caught the approver's hand-edit
(`decision: approved`, `decided: 2026-08-29T11:45:00.908943+00:00`, bare
approval, ~6 minutes after `notified:`) while still running: the ticket
carried `awaiting-scope → designed → ready`, journaled
(`agents/eng-manager/config/decision-journal.md`, row 28), and the gate
item moved to `inbox/_handled/` with its own processed footer. Checked
fresh rather than trusted: this ticket's own frontmatter (`state: ready`,
`owner: eng-manager`), the journal row, and the footer all agree. Nothing
left for this event to act on.

**0 transitions.** No cap affected — `ENG-013` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
this G1 was already off both the approver-facing WIP and approval-cap
counts.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-013` —
fired by the pass that closed this ticket's G1 — still sitting in
`traces/.pending`, undrained, third in line behind two older not-yet-drained
fires (`ENG-013`'s own presignup-leads question, `ENG-012`'s G1). Not a
broken chain, just not yet its turn in the FIFO queue.

**Notify sweep:** nothing to raise (no new gate item this pass); nothing to
nudge (this G1's `notified:`/`decision:` cycle closed same-day, hours
before this pass, well inside the 24h threshold).

Another corroborating occurrence of the open `proposals.md` race (2026-08-27
row, filed by hand — `eng-trigger.sh` should skip the launch when a
`decision` event's named gate item is already in `_handled/`); well past a
dozen occurrences instance-wide as of today, so not re-filed or re-logged as
its own observation — the existing proposal already covers this exactly and
stands unimplemented, waiting on the approver.

`chained: none` — no state change; `ENG-013`'s existing chain (`continue
ENG-013`) is already queued and will run on its own turn. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-013`) and
whole-board: both exit 0, clean. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`).

## 2026-08-29 — continue ENG-011: recovered an unrecorded build already through security, live-DB read verification closed part of the migration gap, ready → ready-to-ship

`continue` event pass, context `ENG-011`, its actual turn at the front of
`traces/.pending`. Narrow scope per the event's own contract. Mode check
clean; pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

Same recovery shape `ENG-007` hit earlier the same day, one occurrence
further: both `_eng` worktrees already carried a pushed
`feat/ENG-011-client-stage-health-visibility` branch, and all four gate
receipts (database migration, code review, QA test plan, security review)
already existed on disk with `pass` verdicts. Verified fresh rather than
trusted — git state, `deno test` (12/12), `npm run build` (clean) all
independently reproduced and matched. New this time: the Supabase MCP
connection reaches the real `aiorders-api` project read-only, used at zero
cost to independently confirm the migration's schema assumptions and rule
out catalog-level dependents — closing the "is it safe" half of the
long-standing no-live-Postgres gap without spending the approver's money
or writing DDL to production ahead of review (both declined as out of this
pass's own authority). Third occurrence of that host limitation crossed
the threshold `observations.md` set for a proposal; filed one
(`proposals.md`), not another observation.

State recorded to match reality: `ready → building → in-review →
in-security → ready-to-ship`, 4 transitions (cap). `machine_wip` and both
approver-facing counters unaffected — no gate raised this pass, the L1
merge request (both repos, this board's first two-repo release) is the
next hop's work. Release window independently reconfirmed closed (Saturday
2026-08-29, `releases.block_weekends`) — flagged for the next hop, not
acted on, same split `ENG-006`/`ENG-007` used at this boundary.

`chained: ENG-011` — `ready-to-ship` is agent-owned (devops opens the PR
next). Fired `continue ENG-011`. Post-pass gate check: see pass notes. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`).

## 2026-08-29 — decision ENG-011 (tickets-source question): a second predicted twin no-op, arrived after the fact was carried all the way to a closed thread

`decision` event pass, context
`inbox/_handled/2026-08-29-eng011-tickets-source-question.md` — the same
duplicate-queued-event shape as the entry directly above, but a different
gate item: `ENG-011`'s standing "tickets" question was queued as its own
independent `decision` event, separate from its G1. Sixth occurrence of
this shape today (`ENG-008`'s two gate items, `ENG-009`'s G1, `ENG-010`'s
G1, `ENG-011`'s own G1, now this). Per this event's own narrower contract
(act on the answered gate item, advance only the ticket it belongs to),
scoped to `ENG-011` only — no board-wide sweep. Mode check clean
(business-os `.env` → `MODE=` empty).  Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`11:13:54 queue: collapsed 3 duplicate event(s)` fires immediately before
`11:13:54 draining queued event: decision
(2026-08-29-eng011-tickets-source-question.md)`, pass start `11:13:55`,
claude launched `11:14:48`. By the time this pass reached the file, the
same `intake` pass that raised the question had already caught the
approver's hand-edit (`decision: rejected`, free text "Reading A",
`decided: 2026-08-29T11:16:32.000840+00:00`) while still running, read it
as a selection of Reading A rather than a flat rejection, shaped it
directly into `ENG-012` in that same pass, and journaled the read
(`decision-journal.md` row 27). Checked further than the last twin
required: `ENG-012`'s own board file shows the thread didn't stop at
"shaped" — a later `scheduled` pass found its G1 answered `rejected`
("later") and carried it to terminal `state: dropped`. Frontmatter,
footer, journal row, and `ENG-012`'s own log all agree — this thread is
not just consumed, it's closed end to end.

**0 transitions.** No cap affected — `ENG-011` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range before this pass, and
this standing question was already off both approver-facing WIP and the
approval cap (closed the same pass it was raised).

**Dead-end sweep (scoped to this event):** re-confirmed `continue
ENG-011` still sitting in `traces/.pending`, undrained, now behind a
considerably longer backlog than the entry above last saw (fires for
`ENG-013` through `ENG-024` have since queued). Still not stuck — no
documented sequencing hold against a sibling ticket, purely FIFO
position.

**Notify sweep:** nothing to raise or nudge.

`chained: none` — no state change; `ENG-011`'s existing chain (`continue
ENG-011`) is already queued and will run when it reaches the front.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-011`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`).

## 2026-08-29 — decision ENG-011 (G1 scope): the predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng011-g1-scope.md`
— the same duplicate-queued-event shape already logged for `ENG-008`'s two
gate items, `ENG-009`'s G1, and `ENG-010`'s G1 earlier today. Per this
event's own narrower contract (act on the answered gate item, advance only
the ticket it belongs to), scoped to `ENG-011` only — no board-wide sweep.
Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-011`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`10:59:40 queue: collapsed 2 duplicate event(s)` fires immediately before
`10:59:40 draining queued event: decision (2026-08-29-eng011-g1-scope.md)`
— duplicate copies of this event collapsed to the oldest, which is this
pass. This item's fact — the approver's G1 approval — was fully consumed by
the `intake` pass that raised it, which caught the hand-edit (`decided:
2026-08-29T11:14:54.862156+00:00`) while still running: architect design
work done (`stage`/`health` both derived at read time from existing
columns/pipelines, no new stored fields — closing the drift-risk the
readback itself flagged), the ticket carried `awaiting-scope → designed →
ready`, journaled (`agents/eng-manager/config/decision-journal.md`, row
26), and the gate item moved to `inbox/_handled/` with its own processed
footer. Checked fresh: the ticket's own frontmatter (`state: ready`,
`owner: eng-manager`), the journal row, and the footer all agree. Nothing
left for this event to act on.

**0 transitions.** No cap affected — `ENG-011` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before
this pass, and this G1 was already off both the approver-facing WIP and
approval cap counts.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-011` —
fired by the pass that closed this ticket's G1 — still queued and
undrained in `traces/.pending`, behind several older not-yet-drained
fires. Unlike `ENG-009`/`ENG-010`, `ENG-011` carries no documented
sequencing hold against a sibling ticket, so nothing here is deliberately
parked — it's simply not yet its turn in the FIFO queue.

**Notify sweep:** nothing to raise or nudge.

`chained: none` — no state change; `ENG-011`'s existing chain
(`continue ENG-011`) is already queued and will run when it reaches the
front. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-011`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-011-client-stage-health-visibility.md`).

## 2026-08-29 — intake: FoodSwipe location-search bug traced to onboarding's missing `show_in_marketplace`, shaped to ENG-024, fast lane, G1 auto-skipped

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-fix-the-location-bug-on-foodswipe.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end — did not sweep the rest of
the board. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` not re-checked separately this pass, no signal it
changed). No pre-pass `lib/eng-gate-check.sh` run through the trigger this
session either (started directly, same known gap prior entries have already
named) — ran it post-pass instead, scoped and whole-board (below).

**No worktree existed on this host for any of the five registered projects**
(`~/Documents/projects/_eng/` itself was absent, not just missing entries) —
none created; `git worktree add` felt like more than an `intake` pass should
reach for on its own initiative when the investigation could be done
read-only. Investigated by reading the human's own checkout directly
(`~/Documents/projects/aiorders/*`), strictly read-only — no git command run
there, no file written there. Whoever next needs to actually build against
`aiorders-api` for this ticket still needs a real worktree
(`config/projects.md`'s by-hand `git worktree add -b eng/base` command, or a
full `lib/eng-setup.sh --apply`); not created here.

**Traced the report to a full, confirmed root cause across two repos before
sizing anything** — skipped `skills/request-readback/SKILL.md`'s dual-reading
ceremony by design (fast lane, see below), and used the saved budget to chase
the actual code instead: `aiorders-api/supabase/functions/restaurant-portal-onboarding/restaurants.ts`'s
`createRestaurant` inserts a new restaurant with `approved: true` but never
sets `show_in_marketplace`; the same file's `updateRestaurantDetails`, called
immediately after in the same onboarding action
(`restaurant-portal/src/components/onboarding/steps/AddLocationsStep.tsx` →
`addLocationFromPlace`), writes Google Places data through
`mapPlaceToRestaurantRow` (`_shared/googlePlaces.ts`) — confirmed its own
`RESTAURANT_PLACE_COLUMNS` whitelist also excludes `show_in_marketplace`, so
nothing anywhere in the sign-up path ever sets it. Every marketplace search
path hard-requires it: `restaurant-marketplace/handlers/restaurants.ts`'s
primary `get_restaurants_optimized` RPC and its own fallback query both filter
`.eq('approved', true).eq('show_in_marketplace', true)`, matching the RPC's
own definition
(`restaurant-marketplace/supabase/migrations/20240302_optimize_restaurant_discovery.sql`);
`sitemap.ts` carries the same requirement. The only place in the codebase that
ever sets the flag `true` is a manual checkbox on an internal admin page
(`aiorders-admin-hub/src/pages/RestaurantDetails.tsx`). `geo` itself **is**
set correctly by `updateRestaurantDetails` — this is specifically a
visibility-flag gap, not a geocoding one, confirmed rather than assumed from
the report's "search by location" wording.

**Sized XS, lane `fast`** — single-file code fix (one field on one existing
insert) plus a one-time backfill `UPDATE` for rows already stuck invisible;
no schema change (column exists already), no new interface, touches none of
the fast-lane exclusion list (auth, payments, data deletion, schema,
dependencies, model calls, public contracts, PII). `type: bug` — G1
auto-skipped per `definition-of-done.md`'s state table, so no gate item
raised and neither approver-facing WIP nor the approval cap is touched by
this ticket at all.

**Filed `ENG-024`** (project `aiorders-api`; severity `P1` — the sign-up
flow's entire point silently fails with no error and no signal to anyone,
though a manual admin workaround exists so it falls short of P0). PRD:
`agents/product-manager/specs/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md`.
Named two things explicitly out of scope rather than silently narrowing: a
second insert site with the identical omission
(`aiorders-api/supabase/functions/restaurant-claims/index.ts`, the separate
"claim your restaurant" flow) sets `approved: false` by design, so whether
*its* eventual approval step also needs to set the flag is a different,
unverified question, not pulled into this ticket; and the column's actual
DB-level default isn't defined in any tracked migration in any of the five
repos, left for whoever builds this to confirm on the way past.

**Held at `shaped` only long enough to write this entry, not blocked by any
cap** — machine WIP counts `ready`..`ready-to-ship` only, and G1 being
auto-skipped means this ticket never touched approver-facing WIP or the
approval cap either. Owner handed to `eng-manager` immediately: per
`agents/product-manager/agent.md`, sequencing/WIP/assignment is the EM's job
even for an auto-approved bug, never the PM's, so this pass deliberately
stopped short of pushing the ticket into `ready`/`building` itself — the
latter is new implementation work, which is this `intake` event's own named
stopping condition regardless of lane. **1 transition**
(`intake → shaped`), well under the cap of 4.

**Rolled the board index this pass** — one more dated entry than the
keep-three rule allows before this one landed; moved the oldest
(`ENG-021`'s chat-bar entry) to the top of `_index-archive.md`'s list,
verified by direct before/after line comparison rather than assumed clean.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract beyond the fresh work above. `ENG-007` through `ENG-023` otherwise
untouched.

**Observations filed** (`observations.md`): the `restaurant-claims` sibling
gap named above, as a suspicion worth a follow-up look rather than a
confirmed second bug — not escalated to a proposal since it's unverified
whether the claims-approval step already closes it downstream.

`chained: ENG-024` — fired `lib/eng-trigger.sh continue ENG-024` before this
pass exits: `shaped`, owner `eng-manager`, an agent-owned state with no gate
to wait at (G1 auto-skipped), nothing about this ticket waiting on a human.
Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-024-onboarded-restaurants-missing-from-marketplace-search.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-024`)
and whole-board: both exit 0, clean.

## 2026-08-29 — decision ENG-009 (G1 scope): the predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng009-g1-scope.md`
— the same duplicate-queued-event shape already logged twice on this board
for `ENG-008`'s own two gate items (now both archived). Per this event's own
narrower contract (act on the answered gate item, advance only the ticket it
belongs to), scoped to `ENG-009` only — no board-wide sweep. Mode check
clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-009`) and whole-board: both exit 0, clean.

**Confirmed rather than assumed.** `traces/eng-loop-2026-08-29.log`:
`10:18:40 queue: collapsed 3 duplicate event(s)` fires immediately before
`10:18:40 draining queued event: decision (2026-08-29-eng009-g1-scope.md)`
— three legitimately-queued copies of this event collapsed to the oldest,
which is this pass. This item's fact — the approver's G1 approval, plus an
unprompted staff-notes addendum already shaped into `ENG-010` — was fully
consumed by the `scheduled` pass (context `schtasks`) that found it sitting
answered-but-unprocessed: shaped, journaled (`decision-journal.md` row 25),
moved to `inbox/_handled/` with its own processed footer, and `ENG-009`
itself carried `awaiting-scope → designed → ready` in that same pass.
Checked fresh: this item's frontmatter (`decision: approved`, `decided:
2026-08-29T09:20:42.679606+00:00`), the journal row, and `ENG-009`'s own
`state: ready` all agree — nothing left for this event to act on.

**0 transitions.** No cap affected — `ENG-009` was already inside the
counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before this
pass, and this G1 was already off both the approver-facing WIP and approval
cap counts.

**Dead-end sweep (scoped to this event):** confirmed `continue ENG-008`
still queued and undrained in `traces/.pending`, behind several other
not-yet-drained fires — consistent with `ENG-008` still sitting at `ready`
with no branch or build started. `ENG-009`'s existing sequencing hold
(re-check once `ENG-008` reaches `in-review` or later) therefore still
applies unchanged. Nothing to resume.

**Notify sweep:** nothing to raise or nudge.

`chained: none` — no state change; `ENG-009` remains held at `ready` pending
`ENG-008`. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-009`) and whole-board: both exit 0, clean. Full detail on the ticket's
own log
(`agents/eng-manager/board/ENG-009-influencer-engagement-info.md`).

## 2026-08-29 — intake: feedback-board status/notes shaped to ENG-023, held at `shaped` — and a P0 tenant-isolation bug found along the way, filed as ENG-022

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-the-feedback-board-on-the-brand-portal-does-not-have-status-.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end — did not sweep the rest
of `agents/product-manager/inbox/` (`fix-the-location-bug-on-foodswipe`
untouched). Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Caps checked fresh from `inbox/` directly**: `ENG-014`'s and `ENG-015`'s
G1s both still sit in `inbox/`, both `decision: approved`, neither
frontmatter advanced — same answered-but-unprocessed state as every pass
today since `ENG-021`'s. Treated conservatively as still 2/2 approver-facing
WIP, 2/3 approval cap.

**Traced the request to its backend before proposing anything**: brand
portal's Feedback page → `brandPortalApi.getFeedback` →
`aiorders-api`'s `brand-portal/feedback.ts` → `restaurant_feedback` schema
(no `status`/`notes` columns at all, confirmed). That trace surfaced a
second thing: `feedback.ts`'s own access check,
`verifyRestaurantAccess(supabase, user.id, restaurant_id)`, has its
arguments in the wrong order against the real signature
(`restaurantId, supabase, user, options`) *and* checks the returned
`{hasAccess, error}` object's truthiness instead of its `.hasAccess` field
— so the check can never deny access, for anyone, to any restaurant's
feedback. Grepped every `verifyRestaurantAccess` call site in
`brand-portal/` (9 files) rather than assuming this was isolated: found the
identical wrong-order-plus-truthiness bug in all 8 call sites of
`offers.ts`, and a second, different mistake — the check called but its
return value discarded entirely, so it does nothing regardless of argument
order — in `customers.ts` (5 sites), `hiring.ts` (3), `website.ts` (2).
Confirmed correct, for contrast: `catering.ts`, `restaurants.ts`, `menus.ts`
(7 sites), `onlineOrders.ts`. Net: any authenticated brand-portal user can
read or write any other restaurant's customer feedback, customer list,
offers, or website content by supplying a different `restaurant_id` — no
exploit tooling needed. `aiorders-api` is documented in `config/projects.md`
as "Highest blast radius of the set — shared backend for all four
frontends."

**Filed as its own ticket, not folded into the feedback ticket and not
routed through `agents/eng-manager/proposals.md`.** Per
`agents/product-manager/agent.md`'s `never_touches` list, a security finding
isn't the PM's to fix or fold into a feature PRD — but per
`schedules/eng_build_loop.md` step 3's explicit bypass and
`templates/ticket.md`'s `source:` note, **a P0 on a registered non-internal
project "keeps its agent source"** and is filed directly rather than queued
for a weekly batched G1: "a live security hole must not wait for a weekly
batch." Rated **P0** rather than P1 on the merits (weighed directly against
this board's other confirmed cross-tenant finding, `ENG-015`, itself P1):
`agents/eng-manager/config/security-baseline.md` names "exposed data" as an
active-security-incident example on par with a leaked credential, and
`agents/security/agent.md`'s own `interrupt_rule` is "P0 only — active
incident, leaked credential, or exposed data." This exposes live customer
PII (not just listings, as `ENG-015` did) and grants unauthorized
cross-tenant *writes* (offers, website content), across five files rather
than one.

**Filed `ENG-022`** (`type: security`, `severity: P0`, `project:
aiorders-api`). PRD (short-form — auto-skip type, no readback needed for an
agent-originated finding with its own evidence):
`agents/product-manager/specs/ENG-022-brand-portal-tenant-isolation-broken.md`.
Landed at `state: shaped, owner: architect` rather than attempting
`designed` myself — that state's exit condition (tech design, ADRs) is the
architect's own output. **Per `security-baseline.md`, "only two things reach
the approver directly... an active security incident — P0,"** so this also
raised an incident notice rather than only a ticket:
`inbox/2026-08-29-eng022-p0-incident.md` (`gate: incident`). Ran
`departments/engineering/lib/eng-notify.sh raise` on it — **exit 0, but
confirmed via `traces/eng-notify-2026-08-29.log` that this is the
already-known, already-proposed no-op** (`proposals.md`, 2026-08-25 row:
`SLACK_WEBHOOK_URL` unset, and this instance's own `config/config.yaml`
sets `approver.notify: telegram`, which the script has no branch for
regardless). The item is on disk in `inbox/` and will surface via the
control center and the next daily brief/weekly report even though the push
did not fire — noted here rather than silently trusted, same practice this
board used the first time this exact gap was caught (2026-08-25). Did not
attempt a fix — that script's channel-dispatch logic is already a queued
proposal and touching its core dispatch path outside that review felt like
larger scope than this pass should take unilaterally.

**Then completed the assigned intake work.** Ran the full request-readback
(`skills/request-readback/SKILL.md`): this PM's own reading plus a blind
architect reading (subagent, `opus`, raw request +
`knowledge/business-profile.md` only, no repo access, no exposure to this
PM's own reading, no exposure to the `ENG-022` investigation either — kept
genuinely blind). **Strong convergence on the core** — both independently
landed on "each feedback item needs a status and an internal note,"
unprompted. **One material divergence**: the architect's reading treated
"is this frequent" / "bottomline issues" as asking for a built cross-item
aggregation/analytics layer (counts, recurring-issue detection, possibly
AI-assisted categorization); this PM's own reading leaned toward "a
restaurant can judge that for itself once notes exist," a materially
smaller build. Per the skill's divergence table this is genuine — different
scope, not different wording — so not resolved internally.

**Did not hold the ticket for it**, same shape as `ENG-013`'s
presignup-leads question → `ENG-017`: the confirmed core (status + notes)
ships regardless, and the divergence became its own non-blocking question,
`inbox/2026-08-29-eng023-frequency-question.md` (`gate: intake-question`) —
"yes" becomes its own ticket once scoped; "no" just closes it. Ran
`lib/eng-notify.sh raise` on it too (same known no-op logged above).

**Filed `ENG-023`** (`type: feature`, `size: S`, `project:
restaurant-portal`). PRD:
`agents/product-manager/specs/ENG-023-feedback-status-and-notes.md`.
**Cross-referenced both new tickets explicitly**: `ENG-023`'s new write path
touches the same file as `ENG-022`'s fix
(`brand-portal/feedback.ts`) — flagged on both that the new
`update_feedback` handler must be modeled on `catering.ts`'s confirmed-
correct `update_catering_request`, not on this file's own (until `ENG-022`
lands) broken `getFeedback`. Not a formal `depends_on` — sequencing between
them is the EM's call at `ready`.

**Held `ENG-023` at `shaped`, not advanced to `awaiting-scope`** —
approver-facing WIP 2/2 per the fresh check above. G1 content fully drafted
in the PRD's Decision section, ready to raise the moment a slot clears.
**Consequence for both tickets:** no cap numbers change — `shaped` counts
toward neither approver-facing WIP nor machine WIP (still 6/6). **2
transitions total** (`ENG-022` and `ENG-023` each `intake → shaped`), well
under the per-ticket cap of 4.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract beyond the fresh cap-verification above. `ENG-007` through
`ENG-021` otherwise untouched.

**Observations filed** (`observations.md`): none beyond what both new
tickets already carry directly — the `ENG-014`/`ENG-015`
answered-but-unprocessed backlog is now six consecutive passes old without
a `decision` event picking it up, re-flagged again; added one line noting
`eng-notify.sh`'s channel-dispatch gap (`proposals.md`, 2026-08-25) was
confirmed a second time this pass, this time on a P0's own incident notice,
strengthening rather than duplicating that existing proposal.

`chained: ENG-022` — `shaped`, owned by `architect`, an agent-owned state;
fired `lib/eng-trigger.sh continue ENG-022` before this pass exits given the
severity, rather than waiting for a scheduled sweep. Confirmed via
`traces/.pending` and `traces/eng-loop-2026-08-29.log` that this queued
correctly rather than launching immediately — this session has held
`traces/.loop.lock` since this pass's own start (09:46:13; the log's last
entry, 10:11:36, already shows two `watch` fires and one `continue` fire
queuing behind it rather than stealing it, "PID 89985 is alive"), so
`continue ENG-022` joined 15 other fires already queued behind the same
lock. Not a stuck lock — it releases the moment this pass exits, and
whatever fires next drains the queue oldest-first; several of the queued
`decision` items look, from their own filenames, like they'll resolve as the
same already-consumed-before-the-fire-arrived no-ops this board has logged
twice already today. Left alone rather than manually drained — outside this
event's scope and not this pass's concurrency state to hand-edit. `chained:
none` for
`ENG-023` — `shaped`, held by the approver-facing WIP cap, not genuinely
blocked for this ticket specifically; re-check once a
`decision`/`watch`/`scheduled` pass clears `ENG-014` or `ENG-015`. Full
detail on each ticket's own log
(`agents/eng-manager/board/ENG-022-brand-portal-tenant-isolation-broken.md`,
`agents/eng-manager/board/ENG-023-feedback-status-and-notes.md`). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-022`,
`ENG-023`) and whole-board: all three exit 0, clean.

## 2026-08-29 — intake: website chat-bar engagement gap shaped to ENG-021 — customer-questions view plus brand-portal FAQ editor, held at `shaped`

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-the-search-chat-bar-engagement-on-website-is-not-displayed-v.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — two other unshaped `agents/product-manager/inbox/` requests
untouched (`fix-the-location-bug-on-foodswipe`,
`the-feedback-board-on-the-brand-portal-does-not-have-status-`), each with
its own `intake` event presumably already queued or pending. Mode check
clean (business-os `.env` → `MODE=` empty; instance `config/config.yaml` →
`mode:` empty). No genuine pre-pass gate-check this time either — same gap
`ENG-019`'s own archived entry already named: this session started
directly rather than through `lib/eng-trigger.sh`'s own pre-pass injection.
Ran `departments/engineering/lib/eng-gate-check.sh` for real after
finishing this ticket's edits instead (below) — the only verdict this entry
can honestly report.

**Caps checked fresh from `inbox/` directly, not the cached header.** Found
`ENG-014`'s and `ENG-015`'s G1s both now `decision: approved` (decided
15:54:50 and 16:12:24) — a genuine change since the header was last
written, which claimed both "unanswered." Neither ticket's own frontmatter
has moved past `state: awaiting-scope, owner: approver` yet, so both
mechanically still hold their approver-facing WIP slot until a `decision`
pass processes them — treated conservatively as still 2/2, at cap, for
this pass's own G1 decision below. Processing those two decisions is out of
this event's scope (a `decision` event's job, apparently already in flight
independently for each); corrected the board header and the "Waiting on
the approver" section to say so plainly instead of repeating the
now-stale "both unanswered," and filed an observation
(`observations.md`) rather than acting on them directly.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in live code across `config-site-builder`,
`aiorders-api`, `aiorders-admin-hub`, and `restaurant-portal` (all four
worktrees already present on this host at `$ENG_WORKTREES`, no creation
needed this pass), plus a blind architect reading (subagent, `opus`, raw
request + `knowledge/business-profile.md` only, no repo access, no exposure
to this PM's own reading). **No material divergence** — both independently
converged on the same core shape: capture real customer questions from the
chat bar, surface them to the owner, and let the owner act on them via
FAQs, as one closed loop on the brand portal. The architect's blind
reading, reasoning with no code access, correctly flagged as open questions
several things this PM's code-grounded reading confirmed directly instead:
whether queries are even captured today (yes, durably), whether the owner
already has backend read access to that data (yes, via an existing but
entirely unused RLS policy), and who authors the FAQ content today (staff
only, in the internal admin tool). None of these changed the shape of the
request, only its cost. The architect's PII and "answered vs. unanswered"
signal concerns were carried into the PRD's Risks/Non-goals rather than the
acceptance criteria, since neither is what the literal request asks for.

**Investigated all four repos before proposing anything.** Traced the
"search/chat bar" to `config-site-builder`'s `AISearchBar`/`ChatPanel`,
rendered site-wide via `Layout.tsx` behind a per-restaurant `showAIChat`
flag — live today, not hypothetical. Every turn is written by
`aiorders-api`'s `ai-search-openrouter` edge function to `ai_conversations`
(`session_id`, `restaurant_id`, `messages` jsonb, timestamps) — confirmed
this table already carries an RLS policy titled "Restaurant managers can
view their restaurant conversations" (`restaurant-portal` migration
`20250903152559_...sql`), granting the exact access this request needs,
entirely unused by any UI in either `restaurant-portal` or
`aiorders-admin-hub` (grepped both for `ai_conversations` usage beyond
generated types — zero hits). The bot's FAQ source is
`restaurant_website.faqs`, editable today only in `aiorders-admin-hub`'s
`RestaurantAIWebsite.tsx` via direct Supabase calls, no edge function in
the path. Confirmed `restaurant-portal` has a same-named but **unrelated**
FAQ list (`CateringFaq`, catering-page-specific) that does not touch this
data — flagged in the ticket so the next agent doesn't wire the new editor
to the wrong field. Confirmed `restaurant-portal` already reads/writes
`restaurant_website` directly today for a different section
(`src/pages/hiring/Index.tsx`, careers content) — the precedent pattern for
the new editor, and evidence (not proof — the literal RLS policy text on
`restaurant_website` was not read) that the owner's account can likely
already write to this table.

**Filed `ENG-021`** (project `restaurant-portal`; size `M` — two coordinated
frontend pieces in one repo, reusing existing tables/RLS on both sides, no
new backend endpoint anticipated; severity `P2`, same "real capability gap,
real manual workaround" calibration as `ENG-020` earlier today). PRD:
`agents/product-manager/specs/ENG-021-chat-bar-engagement-and-faq-self-service.md`.
Scoped as a real-questions log plus a working FAQ write path, not a
quality/gap-analysis dashboard: "answered vs. unanswered" scoring and
cross-session question clustering are named Non-goals/follow-on work, same
"ship the coherent core, name the harder measurement layer as follow-on"
shape `ENG-016`/`ENG-019`/`ENG-020` already used on this board. A
staff-facing (admin-hub) mirror of the same view is named a Non-goal too —
plausible future value, not what was asked.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
reads 2/2 per the fresh-but-conservative check above. G1 content (readback,
both readings' comparison, non-goals, recommendation) is fully drafted in
the PRD's own Decision section and ready to raise the moment a slot
actually clears. **1 transition** (`intake → shaped`), well under the cap
of 4. **Consequence:** no cap numbers change — `shaped` counts toward
neither approver-facing WIP nor machine WIP (still 6/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract beyond the fresh cap-verification above. `ENG-007` through
`ENG-020` otherwise untouched.

**Observations filed** (`observations.md`): the `ENG-014`/`ENG-015`
answered-but-unprocessed finding above; a pre-existing dangling
`"scheduled sweep below"` cross-reference in this file's `ENG-012`
narrative, left unfixed as out of this event's scope.

`chained: none` — `ENG-021` sits at `shaped`, held by the approver-facing
WIP cap, not genuinely blocked or waiting on a human for this ticket
specifically; firing `continue ENG-021` now would only re-discover the same
cap with no new work to do. Re-check once a `decision`/`watch`/`scheduled`
pass actually clears `ENG-014` or `ENG-015`. Full detail on the ticket's
own log
(`agents/eng-manager/board/ENG-021-chat-bar-engagement-and-faq-self-service.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-021`) and whole-board: both exit 0, clean.

## 2026-08-29 — decision ENG-008 (G1 scope): the predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng008-g1-scope.md`
— this is the exact item the immediately preceding entry's own
`observations.md` note predicted would be the same no-op. Per this event's
own narrower contract (act on the answered gate item, advance only the
ticket it belongs to), scoped to `ENG-008` only — no board-wide sweep. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, no
output — clean, including for `ENG-008` specifically (grepped the output
for it directly rather than trusting a clean exit code alone).

**Confirmed the prediction rather than trusting it.** This item's fact —
the approver's G1 approval of the admin-side scope — was already fully
consumed by the `intake` pass that raised it: shaped, journaled
(`decision-journal.md` row 23, "ENG-008 | G1 scope | approved"), moved to
`inbox/_handled/` with its own processed footer, and `ENG-008` itself
carried `awaiting-scope → designed → ready` in that same pass. Checked
fresh rather than assumed: this item's own frontmatter (`decision:
approved`, `decided: 2026-08-29T09:12:46.283064+00:00`) and processed
footer; the journal row; `ENG-008`'s own frontmatter (`state: ready`) and
log. All agree — nothing left for this event to act on. Same
duplicate-queued-event race as its sibling (the engagement-source
question, immediately above): both this G1 and that question were answered
and consumed inside the same live `intake` pass, and the two standalone
`decision` events each independently queued arrived afterward to find
their own facts already closed.

**0 transitions.** No cap affected — this item was already off every count
before this pass (per this file's own header, which already excludes it
from "Waiting on the approver" and the approval cap).

**Dead-end sweep (scoped to this event):** `ENG-008` already carries a
correct, reasoned chain decision from the preceding `scheduled` sweep
(re-fired `continue ENG-008`) — confirmed still queued and undrained in
`traces/.pending` as of this pass, so nothing to resume or fix.

**Notify sweep:** nothing to raise (no new gate item); nothing to nudge
(this item's `notified:`/`decision:` cycle closed same-day, hours before
this pass).

`chained: none` — no state change. `continue ENG-008` remains queued in
`traces/.pending` from the earlier `scheduled` sweep; firing it again would
only collapse into that existing copy at pop time, per the queue's own
dedup rule. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-008`) and whole-board: both exit 0, clean.

## 2026-08-29 — decision ENG-008 (engagement-source question): arrived after the fact was already consumed — no-op

`decision` event pass, context
`inbox/_handled/2026-08-29-eng008-engagement-source-question.md`. Per this
event's own narrower contract (act on the answered gate item, advance only
the ticket it belongs to), scoped to `ENG-008`/`ENG-009` only — no
board-wide sweep. Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean.

**Nothing to act on.** This item's fact — the approver's "both readings"
answer — was already fully consumed by the `intake` pass that raised it,
reading the hand-edit live while still running: shaped into `ENG-009`,
journaled (`decision-journal.md`, "intake-question (engagement source)"
row), moved to `inbox/_handled/`, and `ENG-009` itself carried all the way
to `ready` by the `scheduled` sweep archived immediately above this entry.
Re-confirmed fresh rather than trusted: this item's own frontmatter/footer,
`ENG-009`'s ticket file, `ENG-008`'s own log, and the journal row all
agree.

**Fits the instance's well-documented duplicate-queued-event race
exactly** — confirmed directly from `traces/eng-loop-2026-08-29.log`
(`08:45:06 queue: collapsed 1 duplicate event(s)` immediately before
draining this one): two copies of the same event were legitimately queued
for the same underlying fact, and the live `intake` pass reached it first.
Contrast the `continue ENG-006` no-op (2026-08-28, archived), which did
*not* fit this pattern — that one came from a fire outside the chain
mechanism entirely; this one is the ordinary race.

**0 transitions.** No cap affected — this item was already off every count
before this pass.

**Observation filed** (`observations.md`): the next item in
`traces/.pending` (`decision 2026-08-29-eng008-g1-scope.md`) is the same
shape and will likely be the same no-op — that G1 was also already closed
in the same pass that advanced `ENG-008` to `ready`.

`chained: none` — no state change on either ticket; `continue ENG-008` is
already queued from the preceding `scheduled` sweep, and firing it again
here would only collapse into that existing copy at pop time. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-008`) and
whole-board: both exit 0, clean.

## 2026-08-29 — intake: "AI SEO has no ROI tracking" shaped to ENG-020 — traffic-source/revenue attribution report, Clarity named out of scope

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-ai-seo-no-way-to-track-if-its-useful-or-working-on-brand-das.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — three other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
to scope to): exit 0, clean.

**Caps checked fresh from `inbox/` directly, not the cached header, twice —
once before starting and again immediately before deciding whether to raise
G1.** Both checks agreed: `ENG-014`'s and `ENG-015`'s G1s both still read
`decision:` empty — approver-facing WIP substantively 2/2, at cap,
unchanged from the header going into this pass.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in live code read across
`aiorders-admin-hub`, `config-site-builder` (created this host's missing
worktree to do so — the same per-host worktree gap this board has flagged
repeatedly this session, now also hit for this project), `aiorders-api`,
and `restaurant-portal`, plus a blind architect reading (subagent, `opus`,
raw request + `knowledge/business-profile.md` only, no repo access, no
exposure to this PM's own reading). **No material divergence** — both
independently converged on the same core shape: a per-restaurant view on
the brand portal joining traffic source to order/revenue outcomes, with
Microsoft Clarity named as the wrong tool for the actual question being
asked (behavioural analytics, not attribution or revenue). The architect's
blind reading additionally, unprompted, caught a real ambiguity in the raw
text itself — "but can demostrate" reads as missing a negation ("but
[cannot] demonstrate") — resolved without a standing question since both
readings independently landed on the same resolution, and raised several
risks folded into the PRD's Risks section: attribution honesty (a
last-touch number will overstate what SEO specifically did), cross-domain
cookie-stitching coverage, PIPEDA/Quebec Law 25 exposure from session
recording, no historical baseline for existing customers, small-restaurant
traffic noise, and tenant isolation.

**Investigated all four touched repos before proposing anything.** Traced
"AI SEO" to a real, specific, already-shipped feature — not a vague
marketing term: `aiorders-admin-hub`'s `RestaurantAIWebsite.tsx`/
`BrandAIWebsite.tsx` has a staff-only "SEO Settings" tab with a "Generate
with AI" button that writes `seo.title`/`description`/`keywords`/OG tags,
consumed by `config-site-builder`'s `buildSeo.ts` when building each
restaurant's public site. The restaurant owner never sees this feature or
its output's performance anywhere today. Confirmed Microsoft Clarity
appears nowhere in any of the five repos (case-insensitive search, zero
hits) — not a first-class integration; if installed at all, it's via the
generic custom-code head/body injection (`config-site-builder`'s
`useCustomCode.ts`) or entirely outside AIOrders. **The core finding that
shapes this ticket's low cost:** this is a reporting gap, not a capture
gap. Every customer-signup path this platform has — online order, email
signup, catering form, and a dedicated cross-subdomain tracking script
(`config-site-builder/public/tracking/user-tracking.js`) — already writes
`utm_source`/`utm_medium`/`utm_campaign`/`first_touch_source`/
`last_touch_source`/`first_referrer` onto the `customers` row
(`website-submissions/customer-signup.ts`, `email-signup.ts`,
`update-customer-tracking.ts`, `catering-request/index.ts`,
`crm/customers.ts`), and `autopilot/marketing/welcome.ts` already branches
its own logic on `first_touch_source` — real, wired, already-populated
columns that nothing reads back out to an owner. Confirmed the extension
point: `aiorders-api`'s `analytics` edge function
(`supabase/functions/analytics/database.ts`) already queries both `orders`
and `customers` for a restaurant, so the join this needs already exists at
that seam. Also confirmed `restaurant-portal`'s existing "Analytics" nav
item (`pages/analytics/Index.tsx`) is entirely mock data about
influencer-campaign performance — unrelated to website traffic, and
flagged in the PRD/ticket so it isn't confused with or reused for this
ticket.

**Filed `ENG-020`** (project `restaurant-portal` — primary; `aiorders-api`
also touched and named explicitly in the PRD, same multi-repo/singular-
`project:`-field precedent this board has used since `ENG-003`; size `M`
— no new data model, extends an already-wired edge function plus a new
report view; severity `P2`, calibrated against this board's now-standard
"real capability gap, real manual workaround" shape). PRD:
`agents/product-manager/specs/ENG-020-marketing-roi-attribution-reporting.md`.
Scoped deliberately smaller than the raw request's full framing: ships
revenue-by-channel, not a true ROI ratio (no billing-cost data exists to
weigh against), and organic-traffic revenue as the proxy for "is AI SEO
working" rather than a dedicated AI-SEO-specific attribution flag (nothing
records which restaurants have AI-generated vs. manual SEO applied today)
— both named as Non-goals/follow-on work rather than built now, same
"ship the coherent core, name the harder measurement layer as follow-on"
shape `ENG-016`/`ENG-019` already used on this board. Microsoft Clarity
integration itself is a Non-goal, with the reasoning stated plainly in the
PRD rather than quietly dropped.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
is substantively 2/2 (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s
Guards, same move this instance's four immediately preceding intake passes
all made. G1 content (readback, both readings' comparison, non-goals,
recommendation) is fully drafted in the PRD's own Decision section and
ready to raise the moment a slot frees. **1 transition**
(`intake → shaped`), well under the cap of 4. **Consequence:** no cap
numbers change — `shaped` counts toward neither approver-facing WIP nor
machine WIP (still 4/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-019` otherwise untouched.

**Observations filed** (`observations.md`): the confirmed staff-only
scope of the "AI SEO" feature and the restaurant owner's total lack of
visibility into it; the confirmed-real attribution data already captured
and wired across five different entry points with nothing reading it back
out; the existing `analytics` edge function as the natural extension
point; the confirmed-mock-data state of the existing "Analytics" nav item,
worth a look in its own right since it presents as live to an owner who
has no way to know otherwise; the confirmed absence of Microsoft Clarity
anywhere in code; the fourth occurrence of this host's stale-worktree-
registry gap, this time for `config-site-builder`.

`chained: none` — `ENG-020` sits at `shaped`, held by the approver-facing
WIP cap rather than genuinely blocked or waiting on a human for this ticket
specifically; firing `continue ENG-020` now would only re-discover the same
cap with no new work to do. Re-check once a `decision`/`watch`/`scheduled`
pass clears `ENG-014` or `ENG-015`, or via a dedicated `continue ENG-020`
once either does. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-020-marketing-roi-attribution-reporting.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-020`) and whole-board: both exit 0, clean.

## 2026-08-29 — intake: brand-portal autopilot campaign gap shaped to ENG-019 (mass send + drip, ROI via coupon redemption), held at `shaped` — approver-facing WIP cap still full

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-client-brand-page-portal-autopilot-on-brand-portal-does-not-.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — four other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). No genuine pre-pass gate-check this
time either — this session also started directly rather than through
`lib/eng-trigger.sh`'s own pre-pass injection, same gap the immediately
preceding `ENG-016` entry already flagged; ran
`departments/engineering/lib/eng-gate-check.sh` for real after finishing
this ticket's edits instead (see below), the only verdict this entry can
honestly report.

**Caps checked fresh from `inbox/` directly, not the cached header, twice —
once before starting and again immediately before deciding whether to
raise G1.** Both checks agreed: `ENG-014`'s and `ENG-015`'s G1s both still
read `decision:` empty — approver-facing WIP substantively 2/2, at cap,
unchanged from the header going into this pass. The
`ENG-009`/`ENG-010`/`ENG-012`/`ENG-013`-question backlog remains answered
but unprocessed (unchanged, still off the count per this board's
established convention) — a further consecutive pass without a `decision`
event or dead-end sweep clearing it; re-flagged in `observations.md`, not
fixed here, out of scope for this `intake` event.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in live code read across `restaurant-portal`
and `aiorders-api` (created this host's missing `restaurant-portal`
worktree to do it — see below), plus a blind architect reading (subagent,
`opus`, raw request + `knowledge/business-profile.md` only, no repo access,
no exposure to this PM's own reading). **No material divergence** — both
independently converged on the same core shape: a self-service send
capability layered beside the existing reactive `Automations` engine, a new
campaign/audience/scheduling data model, and an ROI mechanism that doesn't
exist today. The architect's blind reading additionally, unprompted, raised
CASL consent exposure, cross-tenant scoping, durable scheduling
infrastructure, and whether a restaurant-initiated send needs its own
approval step — the last resolved as a non-issue (this repo's own
human-approval constitution governs business-os's own outbound content, not
a feature the AIOrders product exposes to its own paying customers) rather
than a real fork. Full comparison in the PRD's own Readback section.

**Investigated both touched repos before proposing anything.** This host's
`$ENG_WORKTREES` held `aiorders-api` and `aiorders-admin-hub` but not
`restaurant-portal` — third occurrence of the gap the architect first
flagged 2026-08-29 for `aiorders-api` (`config/projects.md`'s "all five
already exist" is a stale, Mac-only verification); created it with the same
`git worktree add -b eng/base` command `lib/eng-setup.sh` runs, one project
rather than the full script, same as that occurrence. Confirmed a real,
load-bearing naming collision before writing anything: the brand portal
already has a nav item called "Campaigns" (`pages/campaigns/*`,
`services/campaignService.ts`, the `influencer_campaigns` table) that is
entirely about inviting influencers to visit and post — unrelated to this
request, and this PRD proposes a different label ("Broadcasts") for the new
capability specifically to avoid it. Confirmed the brand portal's
`Automations` page (`pages/autopilot/Automations.tsx`) is real,
restaurant-facing self-service already, but every one of its trigger types
(`TriggerType` in `types/autopilot.ts`) is reactive — tied to a customer
lifecycle event — with no manual, scheduled, mass, or drip concept
anywhere. Confirmed `offers.coupon_code` is already wired into three
existing offer-based automations, the reuse target this PRD's proposed ROI
mechanism (acceptance criterion 4) is built on rather than new tracking.
Confirmed `outgoing-communications/actors/brands.ts`'s own
`sendPerformanceReport`/`sendMonthlySummary` actions are unimplemented
`TODO` stubs — the platform already intended owner-facing reporting once
and never finished it, worth knowing before assuming either function does
anything today. Also confirmed `pg_cron` is already live in this database
(`platform_analytics_cron`), useful precedent for the scheduled-send/drip
dispatch mechanism this ticket's architect will need to design.

**Filed `ENG-019`** (project `restaurant-portal` — primary; `aiorders-api`
also touched and named explicitly in the PRD, same multi-repo/singular-
`project:`-field precedent `ENG-003`/`ENG-016` set; size `L`; severity
`P2`, calibrated against `ENG-013`/`ENG-016`/`ENG-017`'s same "real
capability gap, real manual workaround" shape). PRD:
`agents/product-manager/specs/ENG-019-restaurant-marketing-broadcasts.md`.
Scoped deliberately smaller than the raw request's full ask: ROI ships as
coupon-redemption tracking only (reusing existing `offers` plumbing), with
open/click attribution and richer segmentation named as Non-goals /
proposed later work rather than built now — same "ship the coherent core,
name the harder measurement layer as follow-on" shape `ENG-014`'s two-item
split and `ENG-016`'s deferred deeper-autopilot item both already used on
this board.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
is substantively 2/2 (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s
Guards, same move this instance's three immediately preceding intake passes
all made. G1 content (readback, both readings' comparison, non-goals,
recommendation) is fully drafted in the PRD's own Decision section and
ready to raise the moment a slot frees. **1 transition**
(`intake → shaped`), well under the cap of 4. **Consequence:** no cap
numbers change — `shaped` counts toward neither approver-facing WIP nor
machine WIP (still 4/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-018` otherwise untouched.

**Observations filed** (`observations.md`): the confirmed "Campaigns"
naming collision (influencer outreach, not customer messaging) and the
label chosen to avoid it; the confirmed reactive-only shape of every
existing `Automations` trigger type; the reusable `offers.coupon_code` and
`pg_cron` prior art; the unimplemented brand performance-report/monthly-
summary stubs; the third occurrence of this host's stale-worktree-registry
gap.

`chained: none` — `ENG-019` sits at `shaped`, held by the approver-facing
WIP cap rather than genuinely blocked or waiting on a human for this ticket
specifically; firing `continue ENG-019` now would only re-discover the same
cap with no new work to do. Re-check once a `decision`/`watch`/`scheduled`
pass clears `ENG-014` or `ENG-015`, or via a dedicated `continue ENG-019`
once either does. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-019-restaurant-marketing-broadcasts.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-019`) and whole-board: both exit 0, clean.

## 2026-08-29 — scheduled: whole-board safety-net sweep clears the four-item answered-gate backlog, finds and re-fires ENG-008's broken chain

`scheduled` event pass, context `schtasks` — the four-times-daily safety
net, not a single-ticket event, so this entry covers the whole board
rather than one request. Mode check clean (business-os `.env` → `MODE=`
empty); pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

**Cleared the answered-but-unprocessed backlog this board's own header had
flagged for five consecutive passes.** `ENG-009` and `ENG-010`'s G1s
(approved), `ENG-012`'s G1 (rejected), and `ENG-013`'s presignup-leads
standing question (approved) were each read fresh from `inbox/`, acted on,
journaled, and moved to `_handled/`:
- `ENG-009` — design work corrected the ticket's own premise before
  writing it (`followers`/`engagement`/growth fields already exist and are
  already displayed, same edit-capability-gap shape `ENG-008` already
  found for region/campaign-type — the note `ENG-008`'s design doc claimed
  it had left here didn't actually exist; caught and corrected, see
  `observations.md`). No one-way door. `awaiting-scope → designed →
  ready`.
- `ENG-010` — new `influencer_notes` table and a dedicated handler with a
  narrower authorization check than `admin-portal`'s shared gate (excludes
  `partner-admin`/`partner-user`, matching this ticket's own G1 default).
  Also corrects an unverified citation in the ticket's own risk section
  (see `observations.md`). No one-way door. `awaiting-scope → designed →
  ready`.
- `ENG-012` — G1 read as a plain rejection ("later"), not the
  reading-under-rejection shape `ENG-011`'s tickets-question had.
  `awaiting-scope → dropped`.
- `ENG-013`'s presignup question — "yes" (Reading B) already had its own
  ticket: an independent `intake` pass the same day had already filed
  `ENG-017` from a different raw request and cited this same answer as
  grounding. Closed against `ENG-017` rather than filed twice.

Full reasoning on each ticket's own log; design docs at
`agents/architect/designs/ENG-009-influencer-engagement-info.md` and
`agents/architect/designs/ENG-010-influencer-relationship-notes.md`. Both
G1s not previously journaled now are (`decision-journal.md`); `ENG-009`'s
own G1 was already journaled at approval time.

**Dead-end sweep found a broken chain, not just a slow queue.** `ENG-008`'s
own log claims `chained: ENG-008` with the trigger fired, but no
`continue (ENG-008)` pass ever ran — absent from `traces/.pending` and
from every `pass start:` line in today's full loop log; no branch exists
in either worktree. Re-fired `/bin/sh
departments/engineering/lib/eng-trigger.sh continue ENG-008` this pass
(queued cleanly behind this pass's own held lock — confirmed via the
trigger's own "pass in flight" log line, no race). Full reasoning on
`ENG-008`'s own log and `observations.md`. `ENG-009` and `ENG-010` are
deliberately **not** chained yet — both extend/reuse code `ENG-008` builds
first, and three tickets' own notes all flagged the same same-file
concurrent-edit risk; re-check once `ENG-008` reaches `in-review` or
later.

**Merge detection:** no ticket sits at `blocked` — nothing to reconcile
against git ancestry this pass.

**No new gate item raised this pass** (only closures), so no
`lib/eng-notify.sh raise` call. Approval cap and approver-facing WIP are
now mechanically clean, not just substantively — both counts agree with
`inbox/`'s actual contents for the first time in six passes; see the
header above.

**Consequence:** machine WIP 4/6 → 6/6 (**at cap** — `ENG-007`
ready-to-ship; `ENG-008`/`ENG-009`/`ENG-010`/`ENG-011`/`ENG-013` ready;
nothing further can enter `ready` until one clears). Approver-facing WIP
and approval cap unchanged in substance (still `ENG-014`+`ENG-015` only)
but now mechanically exact.

**Observations filed** (`observations.md`, six rows this pass): the
backlog clearing itself; two unverified-citation catches in the same
design pass; the partner-admin/partner-user authorization question left
open on `ENG-008`/`ENG-009`; `ENG-008`'s broken-chain finding; the
machine-WIP-at-cap note above.

`chained: none` for this entry itself — a whole-board sweep, not a
single-ticket `continue`; each ticket's own chain decision is recorded on
its own log (`ENG-008` re-fired; `ENG-009`/`ENG-010` deliberately held;
`ENG-007`/`ENG-011`/`ENG-013` already correctly chained and untouched;
`ENG-014`–`ENG-020` genuinely waiting on the approver or the
approver-facing WIP cap, also untouched). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0,
clean.

## 2026-08-29 — intake: "no autopilot for sales staff/resellers" split into ENG-017 (presignup lead nurture) and ENG-018 (demo account), both held at `shaped` — approver-facing WIP cap still full

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-no-autopilot-on-admin-panel-for-our-sales-staff-resellers-to.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own
narrower contract, worked only this one request end to end rather than
sweeping the board — five other unshaped `agents/product-manager/inbox/`
requests untouched, each with its own `intake` event already queued or
pending. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
to scope to): exit 0, clean.

**Caps checked fresh from `inbox/` directly, not the cached header.**
`ENG-014`'s and `ENG-015`'s G1s both still sit in `inbox/`, unanswered —
approver-facing WIP substantively 2/2, at cap, exactly as the header
already read. The `ENG-009`/`ENG-010`/`ENG-012`/`ENG-013`-question backlog
remains answered but unprocessed (unchanged, still off the count per this
board's established convention) — now a further consecutive pass without a
`decision` event or dead-end sweep clearing it; re-flagged in
`observations.md`, not fixed here, out of scope for this `intake` event.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in a live search across all five repos,
plus a blind architect reading (subagent, `opus`, raw request +
`knowledge/business-profile.md` only, no repo access, no exposure to
this PM's own reading). **No material divergence** — both independently
read the raw request as **two** bundled asks (a demonstration account; and
stage-triggered nurture automation for the sales/admin lead pipeline), both
independently named "autopilot" as the existing customer-marketing engine
redirected at a second audience, and both independently flagged
reseller-vs-internal-staff scoping as a real, load-bearing prerequisite
rather than a detail. The architect's blind reading additionally,
unprompted, raised CASL-style consent exposure for cold-lead messaging and
demo-data isolation from real sends/analytics — both checked against live
code (see below) and confirmed real, not speculative.

**A significant cross-reference surfaced during investigation, used as
evidence but deliberately not acted on beyond that.** This request
substantially restates `ENG-013`'s own presignup-leads standing question
(`inbox/2026-08-29-eng013-presignup-leads-question.md`), already
`decision: approved` with explicit verbatim direction — "autopilot built
to nurture these leads to next stages autpmatically and send them
emails/sms to nurture" — but still sitting unprocessed, part of the same
backlog flagged every pass this session. Treated as **confirmed** grounding
evidence for `ENG-017`'s core mechanism rather than re-derived from
scratch; that gate item itself was **not** touched, moved, or journaled by
this pass — it belongs to `ENG-013`'s own lifecycle, out of scope for an
`intake` event about a different request. Flagged plainly in both tickets'
Notes and in `observations.md` so a future `decision`/dead-end-sweep pass
points that item at `ENG-017` instead of shaping a duplicate.

**Investigated all five repos before proposing anything.** Confirmed the
`leads` (website "become a client") table has no stage column and no
consent flag at all, unlike the catering-request flow's explicit
`consent_sms`/`consent_email`. Confirmed the existing `autopilot`/
`outgoing-communications` engine's `communication_templates`/`trigger_type`
model is hard-scoped to `restaurant_id` and a closed set of
customer-lifecycle triggers — a presignup lead fits neither, so a
lead-nurture engine reuses the underlying send services but needs a
parallel trigger/template layer, not a drop-in extension; the router's
`actor: 'admin'` path exists but all three of its handlers are
unimplemented `TODO` stubs. Confirmed no mechanism anywhere attributes a
website lead to a specific reseller (no referral code, no `partner_id` on
`leads`). Separately, searched all five repos for any existing demo/sandbox
concept: the only hit, `config-site-builder/public/config/
demo-restaurant.json`, is a static SEO/config fixture, not a working
account — confirmed genuinely net-new, and, combined with `ENG-011`'s
prior finding of a live platform-wide analytics rollup
(`platform_analytics_cron`), grounds why demo-activity isolation is written
as an acceptance criterion rather than an implementation detail.

**Filed two tickets, not one** — the raw request bundles two independently
shippable pieces with different acceptance criteria and different primary
surfaces, same split precedent this instance has applied all session
(`ENG-009`/`ENG-010`, `ENG-011`/`ENG-012`, `ENG-014`'s two-item split):
- `ENG-017` — Autopilot nurture for the presignup sales lead pipeline
  (project `aiorders-api`; `aiorders-admin-hub` touched; size `L`;
  severity `P2`). PRD:
  `agents/product-manager/specs/ENG-017-presignup-lead-nurture-autopilot.md`.
  Reseller access, and extending nurture to the Brands-page/Foodswipe-
  funnel stage fields, both proposed as non-goals/follow-on work rather
  than assumed in.
- `ENG-018` — Sales demonstration account (project `aiorders-admin-hub`;
  `restaurant-portal`, `config-site-builder`, `aiorders-api` touched; size
  `L`; severity `P2`). PRD:
  `agents/product-manager/specs/ENG-018-sales-demonstration-account.md`.
  Reseller-branded demo clones proposed as a non-goal/follow-on; one
  shared, neutrally-branded demo tenant proposed as the buildable-now
  default.

**Both held at `shaped`, not advanced to `awaiting-scope`.**
Approver-facing WIP is substantively 2/2 (`ENG-014`, `ENG-015`) — per
`eng_build_loop.md`'s Guards ("Approver WIP limit (2)... at the limit,
nothing new starts that will need them"), same move this instance's own
immediately preceding pass made for `ENG-016`. Both PRDs' G1 content
(readback, non-goals, recommendation) is fully drafted and ready to raise
the moment a slot frees. **1 transition each** (`intake → shaped`), well
under the cap of 4. **Consequence:** no cap numbers change — `shaped`
counts toward neither approver-facing WIP nor machine WIP (still 4/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-016` otherwise untouched.

**Observations filed** (`observations.md`): the `ENG-013`
standing-question cross-reference and the recommendation against
duplicating it; the confirmed-absent stage/consent concepts and the
restaurant-scoped shape of the existing autopilot data model; the
confirmed-absent demo/sandbox concept across all five repos and the live
analytics rollup that makes isolation load-bearing.

`chained: none` — both `ENG-017` and `ENG-018` sit at `shaped`, held by the
approver-facing WIP cap rather than genuinely blocked or waiting on a human
for either ticket specifically; firing `continue` on either now would only
re-discover the same cap with no new work to do. Re-check once a
`decision`/`watch`/`scheduled` pass clears `ENG-014` or `ENG-015`, or via a
dedicated `continue ENG-017`/`continue ENG-018` once either does. Full
detail on each ticket's own log
(`agents/eng-manager/board/ENG-017-presignup-lead-nurture-autopilot.md`,
`agents/eng-manager/board/ENG-018-sales-demonstration-account.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-017`, `ENG-018`) and whole-board: all three exit 0, clean.

## 2026-08-29 — intake: catering page self-serve quote generator shaped to ENG-016, held at `shaped` — approver-facing WIP cap full

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-for-catering-page-need-next-step-quote-generator-page-which-.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — six other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty). **No genuine pre-pass
gate-check this time** — this session started directly rather than through
`lib/eng-trigger.sh`'s own pre-pass injection, so there is no baseline
verdict from before this pass's edits began; noted plainly rather than
claimed. Ran `departments/engineering/lib/eng-gate-check.sh` for real after
finishing this ticket's edits instead (see below), which is the only
verdict this entry can honestly report.

**Caps checked fresh from `inbox/` directly, not the cached header, before
deciding how far to carry this ticket.** `ENG-014`'s and `ENG-015`'s G1s
both still sit in `inbox/`, unanswered — approver-facing WIP substantively
2/2, at cap, exactly as the header already read. `ENG-009`/`ENG-010`/
`ENG-012`'s G1s and `ENG-013`'s standing question remain answered but
unprocessed (unchanged, still off the count per this board's established
convention) — now six consecutive passes without a dead-end sweep or
`decision` event clearing them; re-flagged in `observations.md`, not fixed
here, out of scope for this `intake` event.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading, grounded in live code read across all three repos
this touches, plus a blind architect reading (subagent, `opus`, raw
request + `knowledge/business-profile.md` only, no repo access, no
exposure to this PM's own reading). **No material divergence on the core
shape** — both independently converged on: a catering lead flow that
dead-ends today without an automated path to a price; a self-serve quote
builder with menu selection delivered as an SMS/email link; an
owner-configurable toggle between real pricing and a generic
acknowledgement; automatic stage progression; and owner edit/resend plus
deeper `autopilot` use as separable, later work. **Two real forks
surfaced**, neither assumed away: (1) whether the "generic message"
fallback is the restaurant owner's site-wide setting or the customer's own
per-visit choice — resolved by proposing both, the same "cheap either way"
resolution the approver preferred at `ENG-008`; (2) whether "menu
selection" reuses the existing menu's own per-item prices or implies a new
catering-specific pricing model — resolved by proposing reuse, correctable
at G1. Both bundled into the PRD as G1 riders rather than a separate
blocking standing question, the same bar `ENG-015`'s G1 used for its own
small fork.

**Investigated all three touched repos before proposing anything.**
Confirmed in `config-site-builder`: a live public `Catering.tsx` page whose
own "How It Works" copy already promises a step ("Customize Your Menu")
that doesn't exist anywhere in the code; its `CateringForm.tsx` posts to
`aiorders-api`'s `catering-request` function, which inserts into the
`catering` table, creates a CRM customer record, and notifies the
**restaurant owner only** — nothing is ever sent back to the customer
beyond an on-page "we'll contact you" message, confirming the exact gap
named in the request. Confirmed in `restaurant-portal`: a real, shipped
5-status kanban (`CateringKanban`/`StatusUpdateModal`/
`CateringDetailModal`) with all five status strings hardcoded across three
files and no server-side enum, so a sixth ("Quote Sent"-style) value is
additive, not a migration. Confirmed in `aiorders-api`: a mature, already-
shipped `autopilot`/`outgoing-communications` engine (DB-trigger-initiated,
queued, per-restaurant customizable templates, already sending customer
email/SMS) that today only fires on customer-lifecycle events, never
catering — the concrete system the request's own "autopilot" mention
names, and the natural target for the deeper-automation item named as
future work rather than built now. Also confirmed `restaurant-marketplace`
and the CloudWaitress popup widget each have their own, separate catering-
submission code paths — grounding the PRD's scoping to `config-site-
builder`'s own catering page only, the one surface the raw text actually
names.

**Filed `ENG-016`** (project `config-site-builder` — primary; `aiorders-api`
and `restaurant-portal` also touched and named explicitly in the PRD,
following the multi-repo/singular-`project:`-field precedent `ENG-003`
set; size `L`; severity `P2`, calibrated against `ENG-013`'s same
"real capability gap, real manual workaround" shape rather than `ENG-011`'s
lighter `P3`). PRD:
`agents/product-manager/specs/ENG-016-catering-quote-generator.md`.

**Held at `shaped`, not advanced to `awaiting-scope`.** Approver-facing WIP
is substantively 2/2 (`ENG-014`, `ENG-015`) — per `eng_build_loop.md`'s
Guards ("Approver WIP limit (2)... at the limit, nothing new starts that
will need them"), this ticket was carried through readback and PRD-writing
(agent-owned work, costs the approver's queue nothing) but not advanced
into a state that would raise a third open G1 against a cap of two. The
PRD's G1 content (readback, both forks named as riders, recommendation) is
fully drafted and ready to raise the moment a slot frees — nothing further
to shape. **1 transition** (`intake → shaped`), well under the cap of 4.
**Consequence:** no cap numbers change — `shaped` counts toward neither
approver-facing WIP nor machine WIP. Machine WIP unaffected (4/6).

No `inbox/` item raised this pass (no G1 to notify on yet), so no
`lib/eng-notify.sh` call.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-015` otherwise untouched.

**Observations filed** (`observations.md`): the confirmed customer-side
notification gap on catering submission; the additive (no-migration)
shape of the existing hardcoded status lists; the already-shipped
`autopilot`/`outgoing-communications` engine as the concrete target for
the request's own deeper-automation ask; the answered-but-unprocessed
inbox backlog, still unresolved, now six consecutive passes old.

`chained: none` — `ENG-016` sits at `shaped`, an agent-owned state, but
held there by the approver-facing WIP cap rather than genuinely blocked or
waiting on a human for this ticket specifically; firing `continue
ENG-016` now would only re-discover the same cap with no new work to do.
Re-check once a `decision`/`watch`/`scheduled` pass clears `ENG-014` or
`ENG-015`, or via a dedicated `continue ENG-016` once either does. Full
detail on the ticket's own log
(`agents/eng-manager/board/ENG-016-catering-quote-generator.md`). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-016`) and
whole-board: both exit 0, clean.

## 2026-08-29 — intake: agency/reseller brand-scoping shaped to ENG-015 — two of four reported symptoms confirmed and traced to exact code, two found already fixed

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-admin-portal-is-not-optimized-for-new-agency-users-resellers.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — seven other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
to scope to): exit 0, clean.

**Caps verified fresh from `inbox/` directly before raising**, same practice
every pass today has used: `ENG-009`'s and `ENG-010`'s G1s and `ENG-013`'s
standing question all read `decision: approved` but sit unprocessed;
`ENG-012`'s G1 reads `decision: rejected`, also unprocessed — all four
treated as closed for cap arithmetic per this board's established
convention. Only `ENG-014`'s G1 was genuinely open before this pass:
approver-facing WIP 1/2, approval cap 1/3, one WIP slot and two approval
slots free.

**This request carried real severity, flagged in advance.** A `watch`
pass earlier today (`observations.md`, 2026-08-29) had already read the raw
request closely enough to note it reads as "a cross-tenant authorization
boundary gap... not a UI polish item" and to ask whoever shaped it to give
it real severity rather than routine `P3`. Treated that as a pointer to
verify, not a conclusion to inherit untested — see Investigation below.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading plus a blind architect reading (subagent, `opus`, raw
request + `knowledge/business-profile.md` only, no repo access, no exposure
to this PM's own reading). **No material divergence on intent** — both
converged on a systemic, data-layer tenancy-scoping gap rather than
isolated page bugs, and the architect's reading independently guessed that
an agency→brand→location ownership relationship would have to already
exist for the request to make sense — confirmed true against the live
schema before writing anything (see below).

**Investigated both live repos in depth before proposing anything**, same
practice every ticket today has used, deeper here because the raw request
names four separate symptoms across four pages. Confirmed the
`partner-admin`/`partner-user` role pair already exists and already has a
real brand-ownership relationship (`brands.partner_id`, backing a working
`/partners/:id/assign-brands` screen) — this is a propagation gap in an
existing model, not a greenfield access-control build. Traced the two
symptoms that are genuinely real to exact code: `admin-portal/handlers/
restaurants.ts`'s `getRestaurants()` always uses the service-role client
with no role check at all (unlike its sibling `brands.ts`, which already
branches service-role-only-for-`admin`), and the `restaurants` table's only
`INSERT`-capable RLS policy names `admin`/`sub-admin` only, which is why the
existing "Add Restaurant" modal's direct client-side insert silently fails
for a partner caller. Also traced the other two named symptoms
(Dashboard, Influencers) to exact code and found them **already blocked
outright** for partner roles today — not leaking, not scoped, just denied
— and resolved the raw text's ambiguous "or user" by checking `/users`
directly rather than asking the approver to pick a reading: also already
admin-only, both frontend and backend. Caught and corrected one of my own
mid-investigation misreads before it reached the PRD (an `AppSidebar.tsx`
conditional read in isolation, which looked like partner access but on
reading its actual branch body and `ProtectedRoute.tsx` in full turned out
to be a hide/deny) — logged in the ticket rather than silently fixed, same
practice this instance applies to any other artifact's claim.

**Filed `ENG-015`** (`awaiting-scope`, size `M`, project
`aiorders-admin-hub`, `type: security`, severity `P1` — real, live,
code-confirmed cross-tenant data exposure on a reachable admin page, for
real onboarded users, today; short of P0 since this is a latent access-control
gap rather than an active incident). PRD:
`agents/product-manager/specs/ENG-015-agency-reseller-brand-scoping.md`. G1:
`inbox/2026-08-29-eng015-g1-scope.md` — raised despite `security` being on
`definition-of-done.md`'s G1-auto-skip list, a deliberate departure logged
in the ticket's own Notes: a real (if small) policy fork exists that the
raw request doesn't address (should a partner-created restaurant
auto-approve like an admin-created one, or hold for review — proposed
default: hold), and two of the four reported symptoms don't reproduce on
this branch, both worth a one-tap confirm-or-correct rather than silently
deciding either way. No separate standing-question item this time, unlike
`ENG-011`/`ENG-013` — the auto-approve fork is a single default, not a
scope fork that could roughly 10x the ticket's cost, so it's bundled into
this same G1 rather than given its own gate.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stops here by
design. **Consequence:** approver-facing WIP 1/2 → 2/2 (at cap, not over);
approval cap 1/3 → 2/3 (one slot free); machine WIP unaffected (4/6).

Ran `departments/engineering/lib/eng-notify.sh raise` on the new `inbox/`
item — logged the already-open `SLACK_WEBHOOK_URL unset` failure
(`traces/eng-notify-2026-08-29.log`, 13:26:06 local), consistent with every
gate raised on this instance today; `notified:` hand-stamped per
established practice (the field was first written with a stale timestamp
copied from `ENG-014`'s own example by mistake, caught and corrected before
the raise, not after). No dissent section on the G1 — `agents/critic/
agent.md` still doesn't exist (open proposal, `proposals.md` 2026-08-25
row), confirmed absent again rather than assumed.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-014` otherwise untouched. The answered-but-unprocessed backlog
(`ENG-009`/`ENG-010`/`ENG-012`/`ENG-013`-question) is now five consecutive
`intake` passes old without a `decision` event or dead-end sweep picking
any of them up — re-flagged in `observations.md`, not fixed here, same as
every pass before this one.

**Observations filed** (`observations.md`): the precise root-cause trace for
both confirmed defects; the page-by-page "deny outright rather than scope"
pattern the three already-blocked pages share; the corrected mid-investigation
misread.

**Board:** rolled the oldest of three live dated entries (`intake: foodswipe
funnel page shaped...`) into `_index-archive.md`, newest-first per that
file's own convention, before adding this entry — net three entries live
after this one, matching the keep-three rule. Extracted and moved
programmatically (exact line range, not retyped) to avoid transcription
drift on a ~150-line entry.

`chained: none` — `ENG-015` sits at `awaiting-scope`, owned by the
approver; the chaining guard never fires on a ticket waiting on a human.
Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-015-agency-reseller-brand-scoping.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-015`) and whole-board: see pass notes.

## 2026-08-29 — continue ENG-007: recovered an unrecorded build already through security, real ready-to-ship devops work done fresh

`continue` event pass, context `ENG-007`. Per this event's own narrower
contract, resumed only this ticket from its current state — no board-wide
sweep. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-007`) and
whole-board: both exit 0, clean.

**Found the ticket's own board file still reading `ready` while four
complete, dated, mutually-consistent gate receipts already sat on disk**
(migration, code review, QA, security — all citing commit `2aec86f` on
`loyalty-system`). Verified fresh rather than trusted: confirmed the commit
is real, pushed, and unmerged (`git merge-base --is-ancestor` → not an
ancestor of `origin/main`); confirmed no PR is open yet (`gh pr list --head
loyalty-system --state all` shows only `ENG-006`'s already-merged one);
independently re-ran `deno test`/`check`/`lint` against the live worktree
rather than trusting the receipts' own claims — 44/44 passing, clean check,
clean lint, matching every receipt exactly. Recorded the recovered state
machine (`ready → building → in-review → in-security`, 3 transitions) and
then did the genuinely new work `ready-to-ship` still owed — release plan,
rollback, observability, and a $0/month cost delta, none of which any prior
receipt covered — reaching `ready-to-ship` (4th transition, at this pass's
cap). Release window checked fresh and found closed (Saturday,
`block_weekends`) but deliberately left for the next hop to act on, same
split `ENG-006` used at this identical boundary. Full detail, every command
run, and every citation on the ticket's own log
(`agents/eng-manager/board/ENG-007-per-restaurant-loyalty-configuration.md`).

**Consequence:** `machine_wip` unaffected (`ENG-007` was already inside the
counted `ready..ready-to-ship` range at `ready`, stays inside it at
`ready-to-ship`, still 4/6). Approver-facing WIP and approval cap both
unaffected — no gate raised this pass; opening the PR (the merge request) is
the next hop's distinct work.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below. No sweep of the rest
of the board — out of scope for a `continue` event naming this ticket
specifically.

**Board:** rolled the `ENG-011` dated entry (the oldest of the four this
pass's own new entry would otherwise leave live) into `_index-archive.md`,
newest-first per that file's own convention — net three entries live after
this one, matching the keep-three rule.

**Observations filed** (`observations.md`): the recovered-unrecorded-build
shape, a third and furthest-progressed data point in the
partially-updated-artifact family `ENG-006` first named; `deno` now working
for real on this Windows host, closing the migration doc's own open fallback
attempt; Docker Desktop still not coming up within a bounded wait, second
occurrence.

`chained: ENG-007` — `ready-to-ship` is a devops-owned state, not the
approver, not blocked, not terminal, not held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-007`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-007`) and whole-board: both run clean.

## 2026-08-29 — intake: brand-portal restaurant self-service (QR codes & marketing media) shaped to ENG-014, website-settings half named for later

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-on-the-brand-portal-restaurant-is-not-able-to-see-or-generea.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own narrower
contract, worked only this one request end to end rather than sweeping the
board — the other unshaped `agents/product-manager/inbox/` requests
untouched, each with its own `intake` event already queued or pending. Mode
check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Caps re-verified fresh from ground truth, not the cached header —
and the ground truth had moved.** All four items the header carried as
"open" or "answered-but-unprocessed" turned out, on a fresh read of
`inbox/`, to be **answered**: `ENG-009`'s and `ENG-010`'s G1s (unchanged from
prior passes, still unprocessed), `ENG-012`'s G1 (**rejected**), and
`ENG-013`'s presignup-leads question (approved) — the latter two newly
answered since the immediately preceding pass. Read as closed, not open,
for this pass's own cap arithmetic per this board's established convention
(an answered gate item is off the count immediately rather than waiting on
the mechanical `state:` field). Approver-facing WIP and approval cap both
fully free (0/2, 0/3) before this ticket's own G1 — not "one slot free" as
the pre-pass header read.

**Identified the exact repos before proposing anything.** "Brand portal" is
`restaurant-portal` (confirmed via its own `brandPortalApi.ts`), not
`aiorders-admin-hub` (the staff-only "admin portal" the request explicitly
names as inaccessible to owners). Read `restaurant-portal`'s `Website` and
`Settings` pages (only `catering`/`careers` content and an unimplemented
stub, respectively — zero QR/media/hours surface anywhere), `aiorders-admin-hub`'s
`Activation.tsx` (a "Share Bag Insert & QR with Owner" step names today's
manual workaround exactly) and `RestaurantAIWebsite.tsx` (where hours
actually live, staff-only), and `aiorders-api`'s `url-shortener` function —
confirmed it checks `profile.role === 'admin'` exactly, so the gap is a real
backend authorization boundary, not only a missing frontend screen. QR
images come from a free public API (`api.qrserver.com`) — $0/month.

**Split the request into a two-item shape, filed the first, named the
second** — same pattern `ENG-006`/`ENG-007`/`ENG-008` established.
`ENG-014` (this pass, `awaiting-scope`, project `restaurant-portal`, size
`M`) covers QR codes and marketing-media downloads only — the more tightly
bounded half (two already-live generators, restricted to the caller's own
restaurant). Item 2 (website settings, including hours) is named in the PRD
as proposed, to be filed once `ENG-014` verifies; its own scoping question
(how far "anythings related to their website" extends) is deferred to when
item 2 is actually shaped, since it doesn't gate this ticket. No separate
standing-question inbox item this time — unlike `ENG-008`/`ENG-011`/
`ENG-013`, the open gap lives entirely inside item 2's future scope and
doesn't need an approver answer to move `ENG-014` forward.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stops here by
design. Consequence: approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 1/3.
Machine WIP unaffected.

Ran `departments/engineering/lib/eng-notify.sh raise` on the new `inbox/`
item — logged the already-open `SLACK_WEBHOOK_URL unset` failure
(`traces/eng-notify-2026-08-29.log`, 05:08:45 local / 12:08:45 UTC),
consistent with every gate raised on this instance recently; `notified:`
hand-stamped per established practice. No dissent section on the G1 —
`agents/critic/agent.md` still doesn't exist (open proposal,
`proposals.md` 2026-08-25 row), confirmed absent again rather than assumed.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the fresh cap-verification above. `ENG-007`
through `ENG-013` otherwise untouched.

**Observations filed** (`observations.md`): the confirmed admin-only
`url-shortener` gate and the free-QR-provider cost finding grounding this
PRD; and — flagged more pointedly this time — the answered-but-unprocessed
inbox backlog is now **four items deep and four consecutive passes old**
(`ENG-009`, `ENG-010`, `ENG-012`, `ENG-013`'s question), with no pass yet
picking it up. Worth a dead-end sweep or a `decision` event rather than a
fifth re-verification.

`chained: none` — `ENG-014` sits at `awaiting-scope`, owned by the approver;
the chaining guard never fires on a ticket waiting on a human. Full detail
on the ticket's own log
(`agents/eng-manager/board/ENG-014-restaurant-qr-media-self-service.md`).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-014`) and whole-board: see pass notes.

---

## 2026-08-29 — decision ENG-010 (G1 scope): the predicted twin no-op — arrived after the fact was already consumed

`decision` event pass, context `inbox/_handled/2026-08-29-eng010-g1-scope.md`
— the same duplicate-queued-event shape already logged three times on this
board today (`ENG-008`'s two gate items, then `ENG-009`'s G1, all now
archived). Per this event's own narrower contract (act on the answered gate
item, advance only the ticket it belongs to), scoped to `ENG-010` only — no
board-wide sweep. Mode check clean (business-os `.env` → `MODE=` empty;
instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-010`) and
whole-board: both exit 0, clean.

**Confirmed rather than assumed.** This item's own frontmatter
(`decision: approved`, `decided: 2026-08-29T10:49:55.456343+00:00`) already
carries a processed footer — "Processed 2026-08-29 (`scheduled` event pass,
context `schtasks`)" — naming the exact pass that consumed it: design work
done (new `influencer_notes` table, dedicated handler), the ticket moved
`awaiting-scope → designed → ready`, journaled
(`agents/eng-manager/config/decision-journal.md`), and the gate item itself
already relocated to `inbox/_handled/`. Checked fresh rather than trusted:
the ticket's own frontmatter (`state: ready`, `owner: eng-manager`) and its
own log entry for that same pass agree with the footer. Nothing left for
this event to act on.

**0 transitions.** No cap affected — this ticket was already inside the
counted `ready`..`ready-to-ship` machine-WIP range (6/6, at cap) before this
pass, and this G1 was already off both the approver-facing WIP and
approval-cap counts.

**Dead-end sweep (scoped to this event):** `ENG-008` — the ticket this
one's own sequencing hold depends on — still sits at `ready` with no branch
or build started. This ticket's existing sequencing hold (re-check once
`ENG-008` reaches `in-review` or later) therefore still applies unchanged.
Nothing to resume.

**Notify sweep:** nothing to raise (no new gate item); nothing to nudge
(this item's `notified:`/`decision:` cycle closed same-day, hours before
this pass).

`chained: none` — no state change; `ENG-010` remains held at `ready`
pending `ENG-008`. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-010`) and whole-board: both exit 0, clean. Full detail on the
ticket's own log
(`agents/eng-manager/board/ENG-010-influencer-relationship-notes.md`).

---

## 2026-08-29 — intake: foodswipe funnel page shaped, designed and readied same-pass after a mid-flight G1 approval; a pre-signup-leads question raised separately

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-for-the-foodswipe-sales-funnel-page-we-are-not-able-to-or-th.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own
narrower contract, worked only this one request end to end rather than
sweeping the board — nine other unshaped `agents/product-manager/inbox/`
requests untouched, each with its own `intake` event already queued or
pending. Mode check clean (business-os `.env` → `MODE=` empty; instance
`config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (no ticket yet
to scope to): exit 0, clean.

**Caps verified fresh from ground truth before raising.** `ENG-009`'s and
`ENG-010`'s G1s (`inbox/2026-08-29-eng009-g1-scope.md`,
`inbox/2026-08-29-eng010-g1-scope.md`) still sit answered-but-unprocessed —
the same pair the immediately preceding `ENG-011` pass found (see
`observations.md`, 2026-08-29). Treated as closed for cap arithmetic per
this board's established convention. Only `ENG-012`'s G1 was genuinely
open before this pass: approver-facing WIP 1/2, approval cap 1/3, both
with room for one more.

**Identified the exact page before writing anything.** "Funnel" as a
keyword matches exactly one file in `aiorders-admin-hub`:
`src/pages/FoodswipeListings.tsx` ("Foodswipe Listings" — a six-column
kanban already tracking "restaurant onboarding progress across stages,"
plus a funnel-conversion summary). Read it and its backend handler
(`aiorders-api`'s `admin-portal/handlers/foodswipe.ts`) in full before
proposing anything: **confirmed zero write path anywhere** — no
click/drag/edit affordance in the frontend, no mutation branch in the
handler despite it technically accepting `POST`, `classifyStage()` a pure
function over existing columns. Searched the whole API repo for any
staff-assignable status concept (`assigned_to`, `lead_status`,
`crm_stage`, `sales_stage`, `contact_status`, `owner_id`) — none exist;
confirmed net-new, same shape `ENG-011` found for "tickets." Ruled out
`Leads.tsx` (real edit UI, but for an unrelated record type — website-
interest-form leads, not Foodswipe profiles) and found `claim_status`
(the one plausible existing status field) is dead — written once to a
constant, read nowhere.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading plus a blind architect reading (subagent, `opus`,
raw request + `knowledge/business-profile.md` only, no repo access, no
exposure to this PM's own reading). **No material divergence on
direction** — both converged on an existing, currently non-functional
admin page that should let staff act on a pipeline; both independently
flagged "update" as ambiguous between move-stage and edit-details. The
architect's reading went one step further, unprompted: it guessed "sales"
and "onboarding" might need two different stage vocabularies for two
different phases, and that the current stages might only cover one.
Checked against the code rather than accepted or dismissed on guess
alone — **true**: all six existing stages are post-signup; nothing in
this system tracks a restaurant before it signs up. That turned a
speculative guess into a confirmed, live fork worth asking about, not
something to silently build either way.

**Filed `ENG-013`** (`awaiting-scope`, size `M`, project
`aiorders-admin-hub`, severity `P2` — calibrated against `ENG-011`'s
`P3`: this is missing *all* interactivity, confirmed in code, versus
`ENG-011`'s missing visibility+filter; still non-emergency with a
workaround, so short of P1). PRD:
`agents/product-manager/specs/ENG-013-foodswipe-funnel-stage-control.md`.
G1: `inbox/2026-08-29-eng013-g1-scope.md`. Standing question (pre-signup
leads): `inbox/2026-08-29-eng013-presignup-leads-question.md`. Both
raised via `lib/eng-notify.sh raise`, both logged the already-open
`SLACK_WEBHOOK_URL unset` failure (`traces/eng-notify-2026-08-29.log`,
04:39:39 and 04:39:45 local), `notified:` hand-stamped on both (converted
to UTC) per established practice.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stopped here by
design, momentarily. **Consequence at that point:** approver-facing WIP
1/2 → 2/2; approval cap 1/3 → 3/3 (at cap) — this pass's own G1 plus
standing question, counted conservatively, same convention
`ENG-008`/`ENG-011` used. Machine WIP unaffected (3/6). Superseded within
the same pass — see "Continued" below.

**Board:** found `_index.md` sitting at exactly three dated entries before
this pass's own — at the keep-three limit already. Rolled the oldest
(`2026-08-29 — watch (schtasks): no ticket touched...`) into
`_index-archive.md`, newest-first per that file's own convention. Checked
for the already-documented duplicate-archive failure mode
(`observations.md`, 2026-08-29) before touching anything — not present
this time, a clean roll.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the cap verification above. `ENG-007`,
`ENG-008`, `ENG-009`, `ENG-010`, `ENG-011`, `ENG-012` otherwise untouched.
`ENG-009`/`ENG-010` still due a sweep — found and correctly left again
this pass (see `observations.md`, 2026-08-29, and `ENG-011`'s own board
entry).

**Notify sweep:** both of this pass's own items raised and stamped above.
Nothing else to nudge. Approval cap briefly touched 3/3 (full) at this
point in the pass — see "Continued" below for where it settled; no
`lib/eng-notify.sh stall` fired either way, since the cap was reached (and
then relieved) by this pass's own work rather than discovered stuck.

**Observations filed** (`observations.md`): the confirmed-zero write path
and the confirmed-absent staff-status concept grounding this PRD's
defaults; the "foodswipe" brand-name overload between this ticket's
restaurant-onboarding funnel and `ENG-006`'s already-shipped
cross-restaurant consumer loyalty identity; the architect's blind-reading
guess about a pre-signup sales layer turning out to be live once checked
against code.

**Continued, same pass — `ENG-013`'s own G1 came back answered by
hand-edit while this pass was still running.** Processed inline rather
than left for a separately-queued `decision` event, per this instance's
established practice (`ENG-007`, `ENG-008`, `ENG-011` all set the same
precedent earlier today). **G1: approved, bare, no rider.** Real design
work done against the live repos before advancing: searched every
migration in `aiorders-api` for `profiles` before proposing to alter it —
none is its `CREATE TABLE`, corroborating the 2026-08-26 finding that this
repo's schema history was reconstructed after the fact and evidently still
doesn't cover `profiles`' own origin (not blocking; an `ALTER TABLE`
doesn't need it). Checked `admin-portal/index.ts`'s routing and
`leads.ts`'s existing `updateWebsiteLead` write path so the design reuses
a pattern already proven in this codebase. Design:
`agents/architect/designs/ENG-013-foodswipe-funnel-stage-control.md` — one
nullable override column on `profiles` (the only entity present at every
one of the six stages), taking precedence over the existing
`classifyStage()` derivation; new write action reuses the handler's
already-present admin/sub-admin gate. **No one-way door** — additive
column, `null` default, no backfill, no new authorization surface. Moved
straight through `designed → ready`, no G2. Moved the G1 to
`inbox/_handled/`; journaled.

**2 more transitions on `ENG-013`** (`awaiting-scope → designed → ready`),
4 total this pass on that one ticket — at the cap of 4, stopping here by
design (`building` is new implementation work, a different owning role).
**Final consequence this pass:** machine WIP 3/6 → 4/6 (`ENG-007`,
`ENG-008`, `ENG-011` unaffected, `ENG-013` newly in range); approver-facing
WIP 2/2 → 1/2 (`ENG-013`'s own path no longer runs through the approver —
its still-open standing question doesn't hold a WIP slot, since it doesn't
block the ticket); approval cap 3/3 → 2/3 (`ENG-013`'s G1 closed; its
standing question stays open, `ENG-012`'s G1 unaffected) — one slot free
again, not full.

**Observations filed** (`observations.md`): the corroborating
`profiles`-untracked-migration finding.

`chained: ENG-013` — `ready` is eng-manager-owned (a backend/database
engineer builds next), not the approver, not blocked, not terminal, not
held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-013`
before exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-013`) and whole-board: see pass notes.

## 2026-08-29 — intake: ENG-011 shaped, designed and readied same-pass after a mid-flight G1 approval; its tickets question answered and filed as ENG-012

`intake` event pass, context the product-manager inbox request itself
(`agents/product-manager/inbox/2026-08-29-on-the-admin-panel-we-are-unable-to-see-if-the-restaurant-is.md`,
now `agents/product-manager/inbox/_handled/`). Per this event's own
narrower contract, worked only this one request end to end rather than
sweeping the board. Mode check clean (business-os `.env` → `MODE=` empty).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board (no
ticket yet to scope to): exit 0, clean.

**Caps verified fresh from ground truth, not the (stale) cached header** —
found `inbox/2026-08-29-eng009-g1-scope.md` and
`inbox/2026-08-29-eng010-g1-scope.md` both answered (`decision: approved`,
09:20:42 and 10:49:55) but still sitting in `inbox/`, unprocessed; their
tickets still read `state: awaiting-scope` on disk. Left both untouched
(dead-end-sweep/decision-event work, out of scope for an `intake` event on
an unrelated request) but read as closed, not open, for this pass's own
cap arithmetic — see the header note above and `observations.md` for the
full reasoning. Approver-facing WIP and approval cap both fully free by
that reading (0/2, 0/3) before this pass's own G1.

**Ran the full request-readback** (`skills/request-readback/SKILL.md`):
this PM's own reading plus a blind architect reading (subagent, `opus`,
raw request + `knowledge/business-profile.md` only). **No material
divergence** — both converged on the same shape: a missing stage/client
concept on the Brands page, an explicit filter requirement, undefined
health, undefined tickets. Checked both live repos before proposing
defaults, same practice `ENG-005`/`ENG-008` established: `Brands.tsx`
exists with no stage/health/ticket concept today; `onboarding_step` and
`is_active` already exist as raw, unsurfaced signals to ground a proposed
stage taxonomy; no ticket/support system exists anywhere in either repo.
Turned what could have been three guesses into two evidence-grounded
`[proposed]` defaults (stage taxonomy, minimal health signal) plus one
genuine standing question (tickets) — same move `ENG-008` made for its own
"engagement" item.

**Filed `ENG-011`** (`awaiting-scope`, size `M`, project
`aiorders-admin-hub`). PRD:
`agents/product-manager/specs/ENG-011-client-stage-health-visibility.md`.
G1: `inbox/2026-08-29-eng011-g1-scope.md`. Standing question:
`inbox/2026-08-29-eng011-tickets-source-question.md`. Both raised via
`lib/eng-notify.sh raise` — both logged the already-open
`SLACK_WEBHOOK_URL unset` failure (`traces/eng-notify-2026-08-29.log`),
`notified:` hand-stamped on both per established practice.

**2 transitions** (`intake → shaped → awaiting-scope`), well under the cap
of 4 — the next state needs the approver, so this pass stops here by
design. Consequence: approver-facing WIP 0/2 → 1/2; approval cap 0/3 → 2/3
(this pass's own reading — see header for the mechanical count, which
reads over-cap if `ENG-009`/`ENG-010` are counted literally by their
on-disk state instead).

**Board:** found `_index.md` already four dated entries deep (one over the
keep-three limit) even before this pass's own entry — and found the oldest
of those four **already duplicated verbatim in `_index-archive.md`**,
apparently left behind by an earlier roll that completed the copy but never
removed the source. Verified by direct text comparison before touching
anything, not assumed from the matching headings alone. Same general
failure family as the single already-documented "partially-updated,
self-contradictory artifact" occurrence (`observations.md`, 2026-08-28 — a
pass crashing mid-sequence between writes), though a different specific
artifact (a board roll, not a PRD/ticket edit) — noted as corroborating,
not identical. Fixed here: moved the next-oldest entry (`ENG-007`'s G2
answered) into the archive for real, and dropped the already-archived
duplicate from the live file rather than archiving it a second time. Net:
three entries now live (this one plus the two next-newest), matching the
rule.

**Dead-end sweep:** out of scope for this `intake` event's own narrower
contract — not run beyond the cap verification and the board-duplicate fix
above. `ENG-007`, `ENG-008`, `ENG-009`, `ENG-010` otherwise untouched.

**Notify sweep:** both of this pass's own items raised and stamped above.
Nothing else to nudge. Approval cap 2/3 (this pass's own reading), not
full — no stall.

**Observations filed** (`observations.md`): the confirmed-absent
stage/health/ticket concepts and the evidence grounding the proposed
taxonomy; the `ENG-009`/`ENG-010` answered-but-unprocessed gate items; the
duplicated archive entry.

`chained: none` — `ENG-011` sits at `awaiting-scope`, owned by the
approver; the chaining guard never fires on a ticket waiting on a human.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-011`) and whole-board: both exit 0, clean.

**Continued, same pass — both of `ENG-011`'s own gate items came back
answered by hand-edit while this pass was still running.** Processed both
rather than leaving them for a separately-queued `decision` event, per
this instance's established practice.

**G1: approved, bare, no rider.** Did real architect-hat design work
against the live repos before advancing: checked whether cheap internal
order data actually exists for the health signal (it does — a real
internal `orders` table plus an existing hourly
`calculate_platform_analytics()` cron already aggregating per-restaurant
order totals into Cloudflare KV, `20260217000001_platform_analytics_cron.sql` —
checking paid off by confirming feasibility this time, not by finding a
landmine). Design: `agents/architect/designs/ENG-011-client-stage-health-visibility.md` —
`stage` and `health` both derived at read time from columns/pipelines that
already exist, no new table, no new vendor. **No one-way door** — moved
straight through `designed → ready`. Moved the gate item to
`inbox/_handled/`; journaled.

**Standing "tickets" question: `decision: rejected`, free-text "Reading
A."** Read together rather than the field alone — a flat rejection
doesn't usually come with a specific named option underneath it; taken as
"build Reading A" (a minimal from-scratch ticket system), not as killing
the idea. Flagged as an interpretation, not a certainty, on the gate
item's own processed footer and in `decision-journal.md` — first
occurrence of a `decision:`/free-text mismatch on this instance, worth
asking the approver directly if it recurs rather than continuing to
infer. **Filed `ENG-012`** (`awaiting-scope`, size `L` — a genuine new
data model/CRUD surface, materially bigger than `ENG-011`'s derived-field
approach) directly from the selected reading, no fresh blind-readback
subagent run (the question itself already fully specified both options —
same light treatment `ENG-009` used answering `ENG-008`'s "engagement"
question). PRD: `agents/product-manager/specs/ENG-012-restaurant-support-tickets.md`.
G1 raised and notified: `inbox/2026-08-29-eng012-g1-scope.md`.

**2 more transitions on `ENG-011`** (`awaiting-scope → designed → ready`),
4 total this pass on that one ticket — at the cap of 4, stopping here by
design (`building` is new implementation work, a different owning role).
`ENG-012` adds its own 2 (`intake → shaped → awaiting-scope`), well under
its own cap. **Final consequence this pass:** machine WIP 1/6 → 3/6
(`ENG-007` unaffected, `ENG-008` unaffected, `ENG-011` newly in range);
approver-facing WIP and approval cap both net to substantively 1/2 and
1/3 (`ENG-012` alone) — see header for the full mechanical-vs-substantive
figures and the still-open `ENG-009`/`ENG-010` gap this pass did not
touch.

**Observations filed** (`observations.md`): the confirmed-live internal
orders/analytics pipeline `ENG-011`'s health signal now reuses; the
`decision:`-vs-free-text mismatch on the tickets question.

`chained: ENG-011` — `ready` is eng-manager-owned (a
backend/frontend/database engineer builds next), not the approver, not
blocked, not terminal, not held by a cap. Fired
`/bin/sh departments/engineering/lib/eng-trigger.sh continue ENG-011`
before exiting. `chained: none` for `ENG-012` — `awaiting-scope`, owned by
the approver. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-011`), scoped (`ENG-012`), and whole-board: all exit 0,
clean.

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

## 2026-08-28 — scheduled (manualtest): safety-net sweep — board fully terminal except ENG-007, nothing to act on; first pass run on Windows

`scheduled` event pass, context `manualtest` — the first fire this instance
has run through the Windows port (`168cb89`, committed 23:34:44 by the human
operator, one minute before this pass's own drain). `traces/eng-loop-2026-08-28.log`:
a `watch (schtasks)` fire arrived first at 23:33:59 while `MODE=quiet`, and
the trigger's pre-lock pause switch (`eng-trigger.sh`, "the pause switch")
queued it without launching — the quiet-mode gate firing correctly on this
host for the first time. This pass's own fire reached the lock at 23:34:36
once `MODE` had cleared, collapsed 3 duplicate queued event(s), and drained
`scheduled (manualtest)` — launched 23:34:53 via
`/c/Users/jerryai/AppData/Local/Microsoft/WinGet/Links/claude` (the
`$ENG_CLAUDE_BIN`/PATH fallback the same commit added, resolving correctly).
Mode check re-confirmed clean in-session (business-os `.env` → `MODE=`
empty; instance `config/config.yaml` → `mode:` empty). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Business intake:** `agents/product-manager/inbox/` and `inbox/requests/`
hold only `.gitkeep`. Nothing to shape.

**Technical intake:** `agents/eng-manager/inbox/` holds only `.gitkeep`.
Nothing to batch into `proposals.md`.

**Gate returns:** `inbox/` holds the same two live items as the preceding
pass — `2026-08-28-eng007-g1-scope.md` (`notified: 22:15:21`,
`decision:`/`decided:` both still empty, ~1h20m old, well under the 24h
nudge threshold) and `2026-08-28-eng-events-dropped.md` (still no
`decision:`, still non-P0, still never successfully notified — the known
`eng-notify.sh` `MODE`-collision bug, `proposals.md` 2026-08-25 row).
Nothing new, nothing to act on.

**Merge detection:** no ticket is `blocked` on an L1 PR — `ENG-007` sits at
`awaiting-scope`; all six others terminal. Nothing to check.

**Dispatch:** To-do is `ENG-007` alone, and it's waiting on its own G1
answer, not free to dispatch regardless of slot. No other ticket in flight.
Machine WIP 0/6, unaffected.

**Dead-end sweep:** `ENG-007`'s own log ends `chained: none`, owner
`approver` — a valid human-wait. All six terminal tickets' logs already end
`chained: none` in accounted-for terminal states (confirmed on the two
immediately preceding passes; unchanged since). No ticket without an owner.
No broken chain.

**Notify sweep:** nothing raised this pass. Nothing to nudge (`ENG-007`'s G1
well under 24h; the events-dropped item deliberately not retried, per
established precedent — a corroborated open proposal, not this pass's
bug to fix). Approval cap 1/3, not full — no stall.

**Observations filed** (`observations.md`) — this is the first confirmed
end-to-end run of the Windows scheduler port: the pre-lock quiet-mode queue
gate, duplicate-event collapse, and claude-binary resolution all worked as
designed on this host. Also noted: further `watch (schtasks)` fires queued
behind this pass while it held the lock (23:35:40, 23:42:05 so far — roughly
the documented 5-minute poll cadence, not a busy loop), plus one `scheduled
(schtasks)` fire; left for the next pass to drain, per design.

**Board:** rolled the oldest dated entry (`scheduled (launchd): safety-net
sweep`, 20:30:05) to `_index-archive.md` per the keep-three rule — this
entry is the fourth.

No ticket state changed, no gate item was written. `chained: none` — this
pass advanced no ticket, so there is no hop of its own to fire. All
WIP/approval-cap figures unchanged (machine 0/6, approver 1/2, approval cap
1/3). Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board:
exit 0, clean.

## 2026-08-28 — watch: filed ENG-007, item 2 of the approved loyalty sequence — G1 raised

`watch` event pass, context `launchd`, attempt 2/2 of this fire — attempt 1
(21:33–21:38) reached the same request and died mid-flight on the account's
monthly spend limit right after spawning the blind architect-reading
subagent (`traces/eng-loop-2026-08-28.log`: `pass end: watch (exit 1,
352s)`, charged not refunded — 352s clears the 60s never-started
threshold). No artifact from attempt 1 survived on disk or as a live
subagent, so this pass redid the work from scratch. Mode check clean
(business-os `.env` → `MODE=active`).

**Swept all three watched inboxes fresh**, per the `watch` event's own
contract. `agents/product-manager/inbox/` and `agents/eng-manager/inbox/`
held only `.gitkeep` plus already-`_handled/` items; `inbox/` held one
already-notified, non-P0 item (`2026-08-28-eng-events-dropped.md`,
untouched, out of scope). `inbox/requests/` held exactly one new file,
`2026-08-28-eng006-sequence-item-2.md` — the approver continuing the
`ENG-006` loyalty sequence by hand, since `skills/acceptance-check/SKILL.md`
step 6b (the automation meant to do this the moment a sequenced ticket
verifies) didn't exist yet when `ENG-006` itself verified. A queued `intake`
event for the same file sat behind this pass in `traces/.pending` —
matches this instance's well-documented duplicate-queued-event race; that
event will very likely no-op when it drains next, since this pass processed
the file fully.

**Ran the full request-readback** (this PM's reading plus a blind architect
subagent, neither seeing the other) and found no material divergence — both
converged on a per-restaurant, effective-dated config table (two earn
rates, one redemption value), no dependency on `ENG-006`'s identity work.
Full comparison on the ticket's own log and PRD. Sized `S`. `size: L`'s G1
requirement doesn't apply here, but full lane always requires G1 regardless
of size, and caps were fully free (0/2, 0/3) before raising. Wrote and
notified `inbox/2026-08-28-eng007-g1-scope.md`. Filed the intake request to
`inbox/_handled/`.

**1 transition-worthy stop.** `ENG-007`: `intake → shaped → awaiting-scope`
in one pass, `owner` moving `product-manager → approver`. Approver-facing
WIP 0 → 1/2; approval cap 0 → 1/3; machine WIP unaffected (0/6).

**Dead-end sweep:** no other ticket was in flight before this pass — nothing
else to check. **Notify sweep:** this pass's own gate item raised and
stamped; nothing else to nudge; cap 1/3, not full — no stall. **Observation
filed** (`observations.md`) — a second monthly-spend-limit death today,
worth watching as a pattern.

`chained: none` — `ENG-007` sits at `awaiting-scope`, owned by the
approver; the chaining guard never fires on a ticket waiting on a human.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-007`) and whole-board: both run clean.

## 2026-08-28 — watch (schtasks): swept all three inboxes, nothing new — first confirmed watch drain on the Windows port

`watch` event pass, context `schtasks`. Per the event's own narrower
contract, swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`,
and `inbox/` (including `inbox/requests/`) only, acting on whatever is new —
not a board-wide sweep. `traces/eng-loop-2026-08-28.log`: drained
immediately behind the `scheduled (manualtest)` pass directly below (`pass
end: scheduled (exit 0, 554s)` at 23:44:08 → collapsed 2 duplicate event(s)
→ `draining queued event: watch (schtasks)` → `pass start: watch (schtasks)`
23:44:24, launched 23:44:38). Mode check clean (business-os `.env` →
`MODE=` empty; instance `config/config.yaml` → `mode:` empty, both fall
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board (this event names no ticket to scope to): exit 0, clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entry); `inbox/requests/`
is empty. `inbox/` holds exactly the same two live items the immediately
preceding `scheduled (manualtest)` pass already read fresh and accounted
for — read directly again rather than trusted from that account:
`2026-08-28-eng007-g1-scope.md` (`notified: 22:15:21`, `decision:`/
`decided:` both still empty, well under the 24h nudge threshold) and
`2026-08-28-eng-events-dropped.md` (still no `decision:`, still non-P0,
still never successfully notified — the known `eng-notify.sh`
`MODE`-collision bug, `proposals.md` 2026-08-25 row). Nothing new anywhere.

**Merge detection:** no ticket is `blocked` on an L1 PR — `ENG-007` sits at
`awaiting-scope`; nothing else in flight. Nothing to check.

**Dispatch:** To-do is `ENG-007` alone, and it's waiting on its own G1
answer, not free to dispatch regardless of slot. Machine WIP 0/6,
unaffected.

**Dead-end sweep:** `ENG-007`'s own log ends `chained: none`, owner
`approver` — a valid human-wait, unchanged since the preceding pass. No
ticket without an owner. No broken chain.

**Notify sweep:** nothing raised this pass. Nothing to nudge (`ENG-007`'s G1
well under 24h; the events-dropped item deliberately not retried, per
established precedent). Approval cap 1/3, not full — no stall.

**Observation filed** (`observations.md`) — this is the first confirmed
end-to-end completion of a `watch (schtasks)` fire on the Windows port
(the immediately preceding pass confirmed `scheduled (manualtest)`; this is
the first time the 5-minute poll path itself has been seen through to a
clean finish). `traces/.pending` still holds one `scheduled schtasks` and
one `watch schtasks` fire, queued behind this pass while it ran — left for
the next pass to drain, per design.

**Board:** rolled the oldest dated entry (`continue ENG-006: fired
externally...`) to `_index-archive.md` per the keep-three rule — this entry
is the fourth.

No ticket state changed, no gate item was written. `chained: none` — this
pass advanced no ticket, so there is no hop of its own to fire. All
WIP/approval-cap figures unchanged (machine 0/6, approver 1/2, approval cap
1/3). Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

## 2026-08-28 — continue ENG-006: fired externally against an already-terminal ticket — no-op

`continue` event pass, context `ENG-006`. Per the event's own contract
(resume the named ticket from its current state), scoped to this ticket
only — no board-wide sweep. Mode check clean (business-os `.env` →
`MODE=active`; instance `config/config.yaml` → `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

**Nothing to resume.** `ENG-006` has been `state: verified` — terminal —
since the `decision` pass at 20:12:38, confirmed independently twice more
since (the `watch` and `scheduled` passes immediately below). Re-confirmed
fresh rather than trusted from the board's own account: the ticket's own
frontmatter and log, this file's header/In-flight table, and
`decision-journal.md` (all three of its gates — G1, G2, L1 merge — already
journaled) all agree. `traces/.pending` empty; all three watched inboxes
hold only `.gitkeep` and the already-notified, non-P0
`2026-08-28-eng-events-dropped.md`. Nothing anywhere for a machine to act on.

**This fire does not fit the instance's well-documented duplicate-queued-event
race** (`observations.md`, eleven-plus prior rows) — that pattern is always
two events the loop itself legitimately queued for the same underlying
change, racing each other. This one doesn't: `traces/eng-loop-2026-08-28.log`
shows no `continue — queued as pending` line and no pass since the
`ready-to-ship → blocked` transition (14:38:21, its own chain already
consumed) ever recording `chained: ENG-006` — the `decision`, `watch`, and
`scheduled` passes since all correctly logged `chained: none`. This fire
lands at 21:02:49, 27 minutes after the `scheduled` pass's own `pass end`
line, with nothing queued between them — meaning it reached the lock and
drained its own freshly-appended line, not an older one left waiting. That
shape means the fire itself came from outside the loop's own chain
mechanism — a direct invocation of `eng-trigger.sh continue ENG-006` — not
from two internally-queued events racing. Filed as its own,
differently-shaped observation rather than folded into the existing race
count.

**A concrete, plausible source surfaced mid-pass, while re-checking the
working tree.** Commit `3c3dcd0` ("ENG-006: verify against production —
migration and function confirmed deployed") landed at
2026-08-28T21:09:07-07:00, authored by Harsimran — inside this pass's own
window. Its message: the approver ran `supabase db push` and `supabase
functions deploy platform-customer-auth` directly against production,
confirmed by CLI output, and updated the release record's `environment`/
`health_check` frontmatter accordingly — all "outside this department's own
L1 workflow, which still only opens PRs." That's a plausible source for an
external trigger fire landing on this exact ticket in this exact window,
though nothing ties the commit to the fire directly (no log line names a
cause), so it's recorded as circumstantial, not confirmed. Checking that
commit's diff also surfaced a second thing, unrelated to the fire itself:
its frontmatter update to `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`
wasn't matched by an update to that file's own prose body, which still reads
the opposite (`## Deploy`/`## Health note`: "not established that a live
Supabase deploy has happened yet"). Not fixed here — see the observation
below for why.

**0 transitions.** No cap affected — machine WIP 0/6, approver WIP 0/2,
approval cap 0/3, all unchanged; `ENG-006` sits outside every counted range.

**Dead-end sweep (scoped to this event):** `ENG-006`'s own log already ended
in a valid, terminal, accounted-for state before this pass started, and this
pass added one line confirming that rather than reopening it. No other
ticket is in flight to check.

**Notify sweep:** nothing to raise, nothing to nudge. Approval cap 0/3 — no
stall.

**Observation filed** (`observations.md`) — this fire's shape, distinct from
the duplicate-event race.

No ticket state changed, no gate item was written. `chained: none` —
`verified` is terminal; firing `continue ENG-006` again would just repeat
this same no-op. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped (`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — scheduled (launchd): safety-net sweep — board fully terminal, nothing to act on

`scheduled` event pass, context `launchd`, the four-times-daily safety net
(20:30 firing). `traces/eng-loop-2026-08-28.log`: queued behind the `watch`
pass that ended at 20:24:32 (exit 0, 714s); this fire drained at 20:30:05 —
the scheduled calendar time itself, not an immediate queue-drain artifact.
Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean — run fresh myself, not taken on
the preceding passes' own recorded claim.

**Found the working tree already carrying the preceding `decision
ENG-006` + `watch` passes' edits, uncommitted.** Verified rather than
trusted before relying on any of it: independently re-ran the whole-board
gate-check (above); independently grepped every board file's own
`state`/`owner`/`blocked_on` frontmatter directly rather than reading the
index's summary (`ENG-001`, `ENG-002`, `ENG-004`, `ENG-005`, `ENG-006` all
`state: verified`; `ENG-003` `state: dropped`; none `blocked_on` anything);
independently grepped every ticket log's last `chained:` line (all six read
`chained: none`) — no broken chain anywhere on the board. `lib/eng-env.sh:14`
confirms committing this bookkeeping repo is "a deliberate git commit
against business-os, not something a run does," matching this instance's
already-established convention (the immediately preceding passes' own
entries) — left the tree uncommitted, did not commit on this pass's behalf.

**Business intake:** `agents/product-manager/inbox/` and `inbox/requests/`
hold only `.gitkeep`. Nothing to shape.

**Technical intake:** `agents/eng-manager/inbox/` holds only `.gitkeep`.
Nothing to batch into `proposals.md`.

**Gate returns:** `inbox/` holds exactly one live item,
`2026-08-28-eng-events-dropped.md` — read fresh: still no `decision:` field,
still not P0, still no `notified:` stamp (the earlier raise attempt failed on
the already-filed `MODE`-collision bug, not compelling a retry for a non-P0
item). Nothing new, nothing to act on. `2026-08-28-eng006-merge-request.md`
is no longer live — already moved to `_handled/` by the preceding `decision`
pass.

**Merge detection:** no ticket is `blocked` on an L1 PR — all six terminal
(confirmed above). Nothing to check.

**Dispatch:** To-do (`intake`/`shaped`/`awaiting-scope`) is empty; no free
slot to fill regardless (machine WIP 0/6).

**Dead-end sweep:** all six ticket logs end in a valid, accounted-for
terminal state with `chained: none` on record (confirmed above). No ticket
without an owner. No broken chain.

**Notify sweep:** nothing to raise, nothing to nudge (one nudge is the limit
and the events-dropped item never even got a first successful notify —
out of this pass's scope, already a corroborated open proposal), no stall
(approval cap 0/3, not full).

**Observations/exceptions/journal:** nothing new — no gate answered this
pass, no exception request open on any (terminal) ticket log.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire. All WIP/approval-cap figures unchanged (0/6, 0/2, 0/3). Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes, nothing new — board already fully terminal

`watch` event pass, context `launchd`. Per the event's own narrower contract,
swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` (including `inbox/requests/`) only — not a board-wide sweep. Mode
check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean.

**Drained immediately behind the `decision ENG-006` pass directly below, in
the same lock hold, not a separate concurrent invocation.**
`traces/eng-loop-2026-08-28.log`: that pass ended at 20:12:38 (785s, exit
0), the queue then collapsed 2 duplicate event(s), and this `watch` fire was
drained next and launched in the same breath. Verified rather than assumed:
process ancestry (`traces/.loop.lock`, pid 33561, `eng-trigger.sh decision
...`) traces to this session's own `claude` process via `lib/run-claude.sh`
— the same wrapper invocation working through its queue, not a second live
pass touching the same files.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entries); `inbox/requests/`
is empty. `inbox/` holds exactly one live item,
`2026-08-28-eng-events-dropped.md` — read directly: still no `decision:`
field, still not P0, already notified once (10:42:17), and already fully
accounted for both in `ENG-006`'s own ticket log and the immediately
preceding `decision` pass's addendum. `2026-08-28-eng006-merge-request.md`
is no longer a live inbox item at all — that same preceding pass closed it
out and moved it to `_handled/`. Nothing new anywhere.

**Board already fully terminal by the time this pass ran** — confirmed
against the header the preceding pass already updated, not re-derived:
`ENG-001`–`ENG-006` all terminal (`verified` ×5, `dropped` ×1); machine WIP
0/6, approver-facing WIP 0/2, approval cap 0/3. No ticket to dispatch, no
free slot to fill from an empty To-do regardless.

**Dead-end sweep:** nothing beyond the inboxes to check — no ticket in
flight, so no chain to verify.

**Notify sweep:** nothing to raise, nothing to nudge, approval cap 0/3 —
no stall.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire. All WIP/approval-cap figures unchanged. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

## 2026-08-28 — decision ENG-006: merge-request gate closed, control-center jump reconciled — shipped → verified

`decision` event pass, context `inbox/2026-08-28-eng006-merge-request.md`.
Narrow scope per the event contract (act on the answered gate item, advance
only this ticket). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`)
and whole-board: both exit 0, clean.

**Found the ticket already past the gate item it was meant to act on.** The
tracked item carried `decision: approved` (`decided: 2026-08-29T02:59:33Z`,
text "approved"), but `ENG-006`'s own `state:` was already `shipped` — a
"control center" dashboard action had advanced `blocked → shipped` ahead of
any build-loop pass (the one-liner immediately above this entry, in the
ticket's own log). Second occurrence of the gap `ENG-002` first hit
(`proposals.md`, 2026-08-26 row), this time hybrid: unlike `ENG-002` (no
reply at all, item left open), the tracked item *was* answered — just
minutes after the merge rather than instead of it. Addendum filed in
`observations.md` rather than a new proposal row; journaled in
`decision-journal.md`.

**Neither signal trusted on its own text.** Re-ran the loop's own
merge-detection check from scratch in the department's own worktree: `git
fetch` + `git merge-base --is-ancestor origin/loyalty-system origin/main` →
MERGED, `40d7c36` (PR #2's merge commit) directly on `c3ab50c` with no
intervening commits; cross-checked via `gh pr view 2` → `MERGED`,
`2026-08-29T02:57:05Z`, ~2m28s before the gate item's `decided:` stamp — same
"merge, then record" shape as `ENG-005`. The control center's `shipped` call
checks out; not redone.

**Closed out `shipped → verified` in one hop.** Acted as devops: confirmed
the migration and all 7 edge-function files present on `origin/main`
(branch-to-main diff empty, so the already-passing 27/27 Deno suite still
holds — not re-run for zero new information); confirmed no CI/CD exists;
confirmed this worktree has no linked Supabase session
(`supabase migration list --linked` → "Cannot find project ref"), so
`health_check: not checked` recorded honestly rather than inferred. Release
record: `agents/devops/releases/2026-08-28-aiorders-api-ENG-006.md`. Acted as
product-manager: AC3/4/7 confirmed directly against the merged tree
(unit-test-covered linking/validation logic, no live OTP needed); AC1/2/5/6
remain **not verified live**, unchanged from the already-named, already
approver-seen gap (Supabase phone-auth + SMS vendor not yet configured) —
carried forward, not new, not blocking, same standard applied at every gate
on this ticket. PRD `status: designed → verified`. Full reasoning on the
ticket's own log.

**1 transition this pass** (`shipped → verified`), well under the cap of 4.
Approver-facing WIP 1 → 0; approval cap 1/3 → 0/3 — `ENG-006` was the only
item on either. `machine_wip` unaffected (0/6).

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for terminal state. No other ticket in flight.

**Notify sweep:** nothing to raise (`verified` raises no gate item); nothing
to nudge (item now closed, not open). Approval cap 0/3 — no stall.

`chained: none` — `verified` is terminal. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-28 — scheduled (launchd): safety-net sweep — merge check confirms PR #2 still open

`scheduled` event pass, context `launchd`, the four-times-daily safety net.
Queued directly behind, and drained immediately after, the `watch` pass that
finished at 15:37:45 (`traces/eng-loop-2026-08-28.log`) — not the
decision/watch race documented on this instance: no hand-edited gate item is
in play here, and the `watch` pass's own narrower contract explicitly left
merge detection, dispatch, and the full dead-end sweep out of scope. Those
are exactly this event's job, so this is the late-safety-net case, not the
race — and unlike that case's usual "found nothing" shape, this pass had one
real check of its own to run. Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board (this event
names no ticket to scope to): exit 0, clean.

**Business intake:** `agents/product-manager/inbox/` and `inbox/requests/`
hold only `.gitkeep` (plus the former's `_handled/`). Nothing to shape.

**Technical intake:** `agents/eng-manager/inbox/` holds only `.gitkeep`.
Nothing to batch into `proposals.md`.

**Gate returns:** `inbox/` holds the same two live items the immediately
preceding `watch` pass already read fresh and accounted for —
`2026-08-28-eng006-merge-request.md` (still the unfilled "Filled in by the
approver." placeholder, no `decision:`) and `2026-08-28-eng-events-dropped.md`
(no `decision:`, not P0). Re-read both directly rather than trusted from the
board's own account: unchanged, neither new. Nothing to act on.

**Merge detection — the one check this event contributes that the prior pass
didn't.** `ENG-006` is `blocked` on its L1 PR
(https://github.com/harsimranwalia/aiorders-api/pull/2). In the worktree
(`~/Documents/projects/_eng/aiorders-api`, clean): `git fetch origin`, then
`git merge-base --is-ancestor c3ab50c origin/main` — **not an ancestor**;
`origin/main` is still at `5b3bac2`. Cross-checked independently via `gh pr
view 2 --json state,mergedAt`: `state: OPEN`, `mergedAt: null`. Both routes
agree: **not merged.** `ENG-006` stays `blocked`, `blocked_on: approver`,
unchanged — PR opened today (`notified: 2026-08-28T21:42:08`, well under an
hour before this pass), nowhere near the 3-day resurface threshold.

**Dispatch:** nothing to start — `ENG-006` is the only in-flight ticket and
it's `blocked`, not in To-do; no free slot to fill regardless.

**Dead-end sweep:** `ENG-006`'s own ticket log ends validly, `chained: none`
with the blocked-on-approver reason, matching the board. No ticket lacks an
owner; no broken chain.

**Notify sweep:** nothing to raise (no new gate item), nothing to nudge (the
merge-request item is under an hour old), no stall (approval cap 1/3, not
full).

**Observations/exceptions/journal:** none. No gate was answered this pass,
and the two open `inbox/` items plus the `eng_stamp()` fingerprint bug were
already fully accounted for by the `watch` pass that drained immediately
before this one — nothing new to add on top of that.

`chained: none` — `ENG-006` stays `blocked`, `blocked_on: approver`; nothing
for a machine to do until the approver merges the PR or answers the gate
item directly. Post-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board: exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes, nothing new; found the deeper cause of the watch-fingerprint bug

`watch` event pass, context `launchd`. Per the event's own narrower contract,
swept `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` (including `inbox/requests/`) only, acting on whatever is new — not
a board-wide sweep. Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board (this
event names no ticket to scope to): exit 0, clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entry); `inbox/requests/`
is empty. `inbox/` holds exactly two live items, both read directly rather
than trusted from the board's own summary:
`2026-08-28-eng006-merge-request.md` (`ENG-006`'s own L1 merge-request gate,
raised and notified by the immediately preceding `continue ENG-006` pass at
`21:42:08`) still carries the unfilled "Filled in by the approver."
placeholder — no decision yet; and `2026-08-28-eng-events-dropped.md` (the
day's dropped-event incident notice) still carries no `decision:` field and
is still not P0. Both predate this fire and are already accounted for on the
board's own log — nothing new in any of the three inboxes.

**Chased down the incident notice's "already notified" claim rather than
taking it at face value.** `traces/eng-notify-2026-08-28.log` shows the
10:42:17 raise attempt for that file returned `FAILED: active ... — item
still in inbox and in the tab` — the same already-filed `MODE`-collision bug
every other gate item on this instance has hit (`sent: active`, not `sent:
raise`), not a successful notification. The file's frontmatter carries no
`notified:` field, consistent with the failure. Not re-raised here: it's an
already-corroborated, already-proposed bug in shared department code
(`lib/eng-notify.sh`), out of a `watch` pass's narrow scope to fix, and the
item isn't P0, so nothing compels a retry — it stays visible in `inbox/`
regardless, per the constitution's own design.

**Found a deeper cause underneath the open `.watch-seen` proposal
(`proposals.md`, 2026-08-26 row) rather than just logging another
corroboration of its already-known symptom.** Read `watch_fingerprint()`
(`lib/eng-trigger.sh:366`) and the `eng_stamp()` helper it calls per file
(`lib/eng-env.sh:185`): `eng_stamp()` is `date '+%Y-%m-%dT%H:%M:%S%z'` and
ignores its `$1` argument completely, returning wall-clock time rather than
anything derived from the file it's supposedly stamping (contrast
`eng_mtime()` immediately above it, which correctly `stat`s `$1`). Verified
empirically, not just read: called the real function twice, 2s apart,
against these same two unchanged files — two different SHA-1s
(`cba0b32b...` vs `55b6fbd9...`). So the open proposal's own fix (commit the
fingerprint after every event type, not only `watch`) would not close this —
any two fingerprint computations of a genuinely unchanged, non-empty inbox
more than about a second apart already differ, because the hash is a
function of call-time and file *count*, never file identity. Filed as an
addendum in `observations.md` (2026-08-28, last row) pointing back at the
open proposal rather than as a new row — same shape the 2026-08-26
self-modifying-pass addendum used for the same proposal.

**Merge detection, dispatch, and the full dead-end sweep are out of scope
for this event** — no ticket sits in a startable state regardless; `ENG-006`
is the only in-flight ticket, still `blocked`/`blocked_on: approver` on its
L1 PR. Its own ticket log already ends in a valid, accounted-for state with
`chained: none` from the pass that opened the PR — spot-checked directly
against the file rather than trusted from the board's account: matches.

**Notify sweep:** nothing new to raise. `ENG-006`'s merge-request item is
well under 24h old (raised `21:42:08` today). The incident notice has no
`notified:` to measure a nudge threshold against, and isn't P0 — left as is,
per this pass's own instruction not to surface anything but a P0.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its
own to fire; `ENG-006` stays `blocked`, `blocked_on: approver`, exactly as
the pass before this one left it. All WIP/approval-cap figures in the header
are unchanged (machine WIP 0/6, approver-facing WIP 1/2, approval cap 1/3).
Post-pass `departments/engineering/lib/eng-gate-check.sh`, whole-board: exit
0, clean.

## 2026-08-28 — continue ENG-006: L1 PR opened, merge-request gate raised — ready-to-ship → blocked

`continue ENG-006` event pass, the dedicated session the preceding pass
chained specifically to open the L1 PR. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**Release window re-checked fresh**, as the preceding pass explicitly asked
the session that opens the PR to do: Friday 2026-08-28, 14:40 PDT (before the
15:00 cutoff), `MODE=active`, no `ENG_RELEASE_FREEZE`. Inside the window.
Checked for an already-opened PR first (`gh pr list --head loyalty-system`:
empty) and confirmed the worktree (`_eng/aiorders-api`, clean, `loyalty-system`
at `c3ab50c`, not yet merged) before creating one, same discipline `ENG-005`
used at this identical boundary.

**Opened the PR**: https://github.com/harsimranwalia/aiorders-api/pull/2.
Wrote the L1 merge-request item (`inbox/2026-08-28-eng006-merge-request.md`,
`gate: merge`) carrying the PR link and all four gate verdicts (review,
quality, security, migration) by file reference, plus the three
already-designed-around items (SMS/phone-provider config, consent capture,
phone-recycling mitigation) so the approver sees them at the merge decision
itself. Ran `lib/eng-notify.sh raise` — reproduced the already-filed `MODE`-
collision bug (`sent: active`, not `sent: raise`) — corroborating, not new.
Stamped `notified: 2026-08-28T21:42:08` by hand. State → `blocked`,
`blocked_on: approver`, `blocked_from: ready-to-ship`, owner `devops →
approver`, `links.pr` set — same design `ENG-002`/`ENG-005` used at this
boundary.

**1 transition this pass** (`ready-to-ship → blocked`), well under the cap of
4. `machine_wip` 1/6 → 0/6 (`blocked` sits outside the counted range).
Approver-facing WIP 0 → 1; approval cap 0/3 → 1/3.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below. No other ticket in
flight.

**Notify sweep:** this pass's own gate item raised and stamped above. Nothing
to nudge (brand new). Approval cap 1/3, not full — no stall.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; nothing left for a machine to do until the
approver merges the PR or replies to the gate item. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-28 — continue ENG-006: building through ready-to-ship, recovered from a timeout

`continue` event pass, context `ENG-006`, attempt 2/2 after the first
dispatch timed out at 1800s. Narrow scope per the event contract (resume
this ticket from its current state; no board-wide sweep). Mode check clean
(`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**Recovered an unrecorded build** (same shape as `ENG-002`/`ENG-005`'s own
precedent): the dead first attempt had already branched `loyalty-system` in
`_eng/aiorders-api`, written and DB-verified the migration, written the
`platform-customer-auth` edge function plus tests, and fixed a real bug in
its own phone validator — all uncommitted when it hit the timeout mid
re-verification. Ruled out a live concurrent session before trusting any of
it (lock pid, running `claude` pid, and `.pass-out.*` all traced to this
exact invocation). Independently re-verified rather than trusted: deno
test/check/lint re-run fresh via Docker (deno isn't installed on this host)
— 27/27 tests, clean check, clean lint. Full detail on the ticket's own log.

**Ran the full arc in one session, same stopping point as `ENG-005`'s
precedent:** committed and pushed (`building` done) → code review + quality
combined hop (`agents/principal-engineer/reviews/ENG-006.md`,
`agents/qa/test-plans/ENG-006.md`, both **pass**) → security
(`agents/security/reviews/ENG-006.md`, **pass**) → `ready-to-ship` (devops:
migration gate already cleared, $0/month cost, rollback tested, no live
caller yet so zero production blast radius). 4 transitions, at the cap —
stopped before opening the PR (`blocked`), deliberately, same as `ENG-005`.

**Three pre-existing, already-designed-around items carried forward rather
than re-derived by the next reader:** Supabase phone-provider/SMS-vendor
configuration still open (this ticket's OTP-dependent ACs are unreachable
until it lands), consent capture for the new cross-restaurant correlation
not yet wired (approver's/counsel's call per the design), and the
phone-recycling mitigation deliberately deferred as a build-time refinement.
None block this verdict — all three were named in the design doc before
this code was written, not discovered here. Full detail, including the
independent-verification narrative and the per-gate reasoning, is on the
ticket's own log (`agents/eng-manager/board/ENG-006-unified-customer-identity.md`).

**Consequence:** `machine_wip` stays 1/6 — same ticket, later state in the
same counted range. Approver-facing WIP and approval cap both unaffected —
no gate raised this pass (the merge request, which will need the approver,
is the next hop's work).

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with the chain record below.

**Notify sweep:** nothing raised this pass. Approval cap 0/3, not full — no
stall.

**Observations/exceptions:** none filed — the recovered-unrecorded-build
shape corroborates `ENG-002`/`ENG-005`'s precedent rather than adding a new
one.

`chained: ENG-006` — `ready-to-ship` is devops-owned, not the approver, not
blocked, not terminal. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-006` before
exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — scheduled: ENG-006's G2 caught mid-sweep — awaiting-decision → ready

`scheduled` event pass, context `launchd` — the four-times-daily safety net.
Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, whole-board: exit 0, clean.

**Full board swept, not just the one ticket.** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/`, and `inbox/requests/` all empty (bar
`.gitkeep`/already-`_handled/` entries) — no PM or EM intake waiting. No
ticket sits `blocked` on an L1 PR — merge detection had nothing to check.
`ENG-006` was the only in-flight ticket, and its `inbox/` gate item
(`2026-08-28-eng006-g2-oneway-door.md`) had already been answered
(`decided: 2026-08-28T20:09:06`) by the time this pass read it — caught here
precisely because this is what a scheduled sweep is for: neither `watch`
(unwired on this instance) nor a tracked-channel reply (this approver
hand-edits gate files directly, every time so far) had a live path to act on
it sooner. `traces/.pending` held a `decision` event for the same file
queued behind this pass — the already-documented duplicate-event race
(`observations.md`), not new; that queued fire will find the item already in
`_handled/` and no-op.

**Acted on the answer as eng-manager (G2 is the EM's gate).** Approved, with
the approver's own reversibility criterion restated in full rather than a
bare yes — read in full on `inbox/_handled/2026-08-28-eng006-g2-oneway-door.md`
and the ticket's own log. Confirms rather than changes the design's approach:
legacy `customers` stays untouched, the two flows run side by side, and a
unified cross-restaurant order view is explicitly later-ticket scope. Ticket
advanced `awaiting-decision → ready` — one transition, well under the cap of
4, stopping there because `building` is new implementation work and this
event's dispatch step leaves that for a fresh chained session by design.
Journaled in `agents/eng-manager/config/decision-journal.md`. Full detail,
including the cap arithmetic and the design's own breakdown this ticket's
`ready` state relies on, is on the ticket's own log
(`agents/eng-manager/board/ENG-006-unified-customer-identity.md`).

**Consequence:** `machine_wip` 0/6 → 1/6 (`ENG-006` now inside the counted
`ready`..`ready-to-ship` range for the first time). Approver-facing WIP 1/2 →
0/2; approval cap 1/3 → 0/3 — both now clear.

**Dead-end sweep (whole-board):** `ENG-001`–`ENG-005` all terminal with valid
closing log lines. `ENG-006` now ends in a valid state with a chain record
below. `inbox/2026-08-28-eng-events-dropped.md` (incident notice, `ticket:
unknown`) has no `decision:` yet and isn't P0 — left waiting on the approver,
already notified once at creation; not re-surfaced per the constitution's
P0-only rule for this pass.

**Notify sweep:** nothing raised this pass (one gate closed, none opened).
Nothing past 24h with no `nudged:`/`decision:`. Approval cap 0/3, not full —
no stall.

**Observations/exceptions:** none filed — the queued-duplicate race behind
this pass corroborates an already-open pattern rather than adding a new one.

`chained: ENG-006` — `ready` is eng-manager-owned, not the approver, not
blocked, not terminal. Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-006` before
exiting. Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped
(`ENG-006`) and whole-board: both exit 0, clean.

## 2026-08-28 — decision ENG-006: G1 approved, design done, one-way door escalated — awaiting-scope → designed → awaiting-decision

`decision` event pass, context `inbox/2026-08-27-eng006-g1-scope.md`. Narrow
scope per the event contract (act on the answered gate item, advance only
this ticket). Mode check clean (`MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**Not a clean unanswered gate — found mid-recovery.** An earlier `watch` pass
today (08:35–08:44) had already started processing this exact answer: it
edited the PRD's `## Decision` section and flipped its status to `designed`,
then crashed on the account's monthly spend limit before touching the ticket,
the board, or the gate item. Its retry failed on a network error and the
event was dropped after two attempts
(`inbox/2026-08-28-eng-events-dropped.md`). This pass verified the PRD's
claims against the filesystem rather than trusting them — the frontend
knowledge-capture doc it claimed was "Done" did not exist — and completed the
work for real. Full detail on the ticket's own log
(`agents/eng-manager/board/ENG-006-unified-customer-identity.md`); one
observation filed on the general pattern
(`agents/eng-manager/observations.md`).

**Design done fresh against the live `aiorders-api` repo** (no schema in
version control there at all — read the edge functions that query
`customers` instead of trusting the PRD's inferences). Corrected one PRD
assumption in the process: legacy customer records are already scoped by
`restaurant_id` **or** `brand_id`, not restaurant-only. Full design:
`agents/architect/designs/ENG-006-unified-customer-identity.md` — Supabase's
native phone/OTP auth, two new additive tables, `customers` untouched.

**One-way door escalated rather than decided** — the PRD flagged this twice
for the architect to evaluate at G2; given the stakes (largest new subsystem
on this board) and no G2 precedent yet, put the actual question to the
approver instead of deciding unilaterally. Raised
`inbox/2026-08-28-eng006-g2-oneway-door.md`.

**Both G1 riders honored:** wrote
`agents/product-manager/specs/loyalty-program-frontend-understanding.md`
(knowledge capture only, not scheduled); carried the resolved SMS-vendor-cost
note into the design's Risks, with the caveat that delivery still isn't
wired to any real vendor in code.

**2 transitions this pass** (`awaiting-scope → designed → awaiting-decision`),
under the cap of 4. `machine_wip` unaffected. Approver-facing WIP and
approval cap both net unchanged at 1/2 and 1/3 — G1 closed, G2 opened, same
ticket.

**Dead-end sweep (scoped to this event):** this ticket's log now ends in a
valid, accounted-for state with a chain record below.

**Notify sweep:** this pass's own gate item raised and stamped. Nothing to
nudge. Approval cap 1/3, not full — no stall.

`chained: none` — `awaiting-decision`, owned by the approver; the chaining
guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
whole-board: both exit 0, clean.

## 2026-08-28 — watch: swept all three inboxes again, nothing new

`watch` event pass, context `launchd`. Per the event's own narrower contract,
this sweeps `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`, and
`inbox/` only, acting on whatever is new — not a board-wide sweep. Mode check
clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh` (`ENG_ROOT` pinned to this
instance — the default root resolves against the script's own department
location, which has no `board/`; see `observations.md`), whole-board: exit 0,
clean.

**Swept all three inboxes fresh; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` hold only
`.gitkeep` (plus the former's already-`_handled/` entry); `inbox/requests/`
is empty. `inbox/` itself holds exactly one live item,
`2026-08-28-eng-events-dropped.md` (the incident notice for today's dropped
build-loop event) — read directly rather than assumed from the board: still
no `decision:` field, still not P0 (an incident notice, not production-down
or an exploitable vuln), still under 24h since its one `raised:` notification
(10:42:17). The immediately-preceding `scheduled` pass already accounted for
this exact file on identical grounds. Nothing else in any of the three
inboxes postdates that pass.

**Another occurrence of the open `.watch-seen` fingerprint-timing race**
(`proposals.md`, 2026-08-26 row; corroborated repeatedly in
`observations.md`). The preceding `scheduled` pass processed this same inbox
state but — being `scheduled`-typed, not `watch`-typed — never called
`commit_watch_fingerprint()`, so `traces/.watch-seen` stayed stamped at
whatever it held before today's `eng-events-dropped.md` arrived. This fire's
recomputed fingerprint still differed from that stale value, cleared the
above-the-lock de-noise check, and spent a full session confirming the
`scheduled` pass had already left nothing behind. Not re-diagnosed at length
here — the mechanism is already on record; this is a data point, not a new
finding. One line added to `observations.md`.

**Merge detection, dispatch, and the full dead-end sweep are out of scope for
this event** — no ticket sits `blocked` on an L1 PR regardless (`ENG-006` is
the only in-flight ticket, at `ready`). `ENG-006`'s own ticket log already
ends in a valid, accounted-for state with `chained: ENG-006`, spot-checked
directly against the file rather than trusted from the board's own account —
matches. That chain's `continue ENG-006` sits queued in `traces/.pending`
behind this pass, unaffected and not duplicated here — also queued behind it,
`1 decision 2026-08-28-eng006-g2-oneway-door.md`, which the prior pass already
predicted will find its file in `_handled/` and no-op.

**Notify sweep:** nothing new to raise. Today's incident notice is under the
24h nudge threshold. Approval cap 0/3, not full — no stall.

**Nothing to journal** — no gate was answered this pass.

No ticket was touched, no ticket state changed, no gate item was written.
`chained: none` — this pass advanced no ticket, so there is no hop of its own
to fire; `ENG-006`'s separately-queued `continue` (from the preceding pass)
runs on its own regardless, once this pass exits. All WIP/approval-cap
figures in the header are unchanged. Post-pass
`departments/engineering/lib/eng-gate-check.sh` (`ENG_ROOT` pinned as above):
exit 0, unchanged.

## 2026-08-28 — decision ENG-005: merge confirmed by git ancestry — blocked → shipped → verified

`decision` event pass, context `inbox/2026-08-27-eng005-merge-request.md`.
Narrow scope per the event contract (act on the answered gate item, advance
only this ticket). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`)
and whole-board: both exit 0, clean.

**The gate item's answer:** `decision: approved`, `decided:
2026-08-28T00:13:09.817494+00:00`, text "merged" — the tracked channel this
time, unlike `ENG-002`'s direct-GitHub/control-center bypass. **Not taken on
the text alone** — re-ran the loop's own merge-detection check
(`schedules/eng_build_loop.md` step 5) from scratch in the department's own
worktree (`~/Documents/projects/_eng/aiorders-admin-hub`): `git fetch origin`
showed `919d355..edf6947 main -> origin/main`; `git merge-base
--is-ancestor chore/ENG-005-a4-poster-generator-wire-in origin/main`
confirmed MERGED; `edf6947` (PR #2's own merge commit) sits directly on
`51cdb29` (this ticket's commit) with no intervening commits, `git diff`
between the branch tip and `origin/main` empty. The merge commit's own
timestamp lands ~20s before the gate item's `decided:` stamp — consistent
with merging and recording the decision in one sitting.

**Acted as devops for `shipped`, then product-manager for `verified`, both
this pass.** Checked out `origin/main` in the worktree, ran `npm run build`
(succeeds; bundle now pulls in the component's own chunks, corroborating it's
genuinely reachable, not just present) and confirmed the wiring directly
(`grep -rn "A4PosterGenerator" src/pages/RestaurantDetails.tsx`). Both PRD
acceptance criteria re-confirmed against the merged tree. **Recorded
`health_check: not checked` and `rollback_tested: false` rather than
`green`/`true`** — unlike `ENG-002`, this release has a real new
production-facing artifact once deployed, and deploying is outside L1
autonomy regardless of diff content (a human merges; a human or their own
process deploys) — this department has no Cloudflare/monitoring access to
confirm live status either way, and said so plainly rather than inferring a
number it can't observe. Release record:
`agents/devops/releases/2026-08-28-aiorders-admin-hub-ENG-005.md`. Gate item
moved to `inbox/_handled/` with a processed footer; journaled in
`agents/eng-manager/config/decision-journal.md`. Full detail on the ticket's
own log.

**2 transitions this pass** (`blocked → shipped`, `shipped → verified`), well
under the cap of 4. Approver-facing WIP 2 → 1; approval cap 2/3 → 1/3
(`ENG-005` no longer counts — `verified` is terminal). `machine_wip`
unchanged at 0/6 (neither `blocked` nor `verified` is in the counted range).

**Dead-end sweep (scoped to this event):** `ENG-005`'s log now ends in a
valid, accounted-for terminal state. `ENG-006` (`awaiting-scope`, owner
approver) untouched — out of scope for a `decision` event naming this
ticket.

**Notify sweep:** nothing to raise (`verified` raises no gate item). Nothing
to nudge — the merge-request item is answered and closed. Approval cap now
1/3, not full — no stall.

**Observation filed, not acted on:** the per-ticket hop-budget file is named
`.hops-{today's date}-{TICKET-ID}` (`lib/eng-trigger.sh`), which resets to a
fresh file every midnight — but this document's own cadence section states
"the day's counter clears at midnight where a ticket's does not." The two
disagree; not investigated further here since it's outside this event's
scope and didn't block this ticket (today's `.hops-2026-08-28-ENG-005` file
didn't exist before this pass, well under the 8/day cap regardless). See
`agents/eng-manager/observations.md`.

`chained: none` — `verified` is a terminal state; nothing left for a machine
or the approver to do on this ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`) and
whole-board: both exit 0, clean.

## 2026-08-27 — continue ENG-005: L1 PR opened, merge-request gate raised — ready-to-ship → blocked

`continue ENG-005` event pass — the dedicated session the preceding pass
chained specifically to open the L1 PR. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean. `traces/.hops-2026-08-27-ENG-005`
read `3` — third dispatch today, well under `hops_per_ticket` (8, `pro` tier).

**Checked for an already-opened PR first** — the immediately preceding pass
recovered one unrecorded build today already, so a duplicate PR was a real
risk. `gh pr list --head chore/ENG-005-a4-poster-generator-wire-in --state
all`: empty. None existed.

**Opened the PR** (`gh pr create`):
https://github.com/harsimranwalia/aiorders-admin-hub/pull/2. Wrote the L1
merge-request item (`inbox/2026-08-27-eng005-merge-request.md`, `gate:
merge`) carrying the PR link and the three gate verdicts by file reference.
Ran `lib/eng-notify.sh raise` — reproduced the already-filed `MODE`-collision
bug (`sent: active`, not `sent: raise`) — corroborating, not new. Stamped
`notified: 2026-08-27T16:03:58` by hand. State → `blocked`, `blocked_on:
approver`, `blocked_from: ready-to-ship`, owner `devops → approver` — same
design `ENG-002` used at this identical boundary.

**Cap check before advancing, read fresh:** `wip.approver_limit` (2) was at 1
(`ENG-006`'s G1); `awaiting_approver_cap` (3) was at 1/3. `ENG-005` is an
already-in-flight, already-fully-gated ticket reaching its own next gate, not
a new start, so `approver_limit`'s "nothing new starts" consequence is
untouched. Advancing brings `approver_limit` to 2/2 (at the limit, not over)
and `awaiting_approver_cap` to 2/3 (not over) — proceeded on that basis.

**1 transition this pass** (`ready-to-ship → blocked`), well under the cap of
4 — opening the PR and raising the gate is the real work of this hop.
`machine_wip` 1/6 → 0/6 (`blocked` sits outside the counted range).
Approver-facing WIP 1 → 2; approval cap 1/3 → 2/3.

**Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
state with a chain record below. `ENG-006` (`awaiting-scope`, owner
approver) untouched — out of scope for a `continue` event naming this
ticket.

**Notify sweep:** this pass's own gate item raised and stamped above.
Nothing to nudge (brand new). Approval cap 2/3, not full — no stall.

`chained: none` — `blocked`, `blocked_on: approver`. This is the human gate
the whole hop was driving toward; firing `continue ENG-005` again would just
re-queue against a ticket with nothing left for a machine to do until the
approver merges the PR or replies. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — continue ENG-005: recovered an unrecorded build, then ready → ready-to-ship in one hop

`continue ENG-005` event pass — the dedicated `building` (frontend) session
the preceding `decision` pass chained. Narrow scope per the event contract
(resume this ticket from its current state; no board-wide sweep). Mode check
clean (`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**The chained `building` session had already run and died before recording
anything.** The worktree carried a clean, pushed commit
(`51cdb29`, "Wire A4PosterGenerator into RestaurantDetails") this ticket's log
had no record of — `traces/.hops-2026-08-27-ENG-005` (`2`) confirms this is
the second dispatch of `continue ENG-005` today. Ruled out a live competing
session first (full `ps`/`ppid` ancestry walk: the process holding
`traces/.loop.lock` is this pass's own top-of-chain orchestrator, not a
second instance), then independently verified the recovered commit rather
than trusting it — diff matches the architect's design exactly, lint
identical to a clean `origin/main` checkout (181 problems, zero new), build
succeeds, no dependency added. Full detail on the ticket's own log.

**Four transitions this pass, at the cap:** `ready → building → in-review →
in-security → ready-to-ship`. Principal-engineer + qa combined hop both
verdict **pass** (`agents/principal-engineer/reviews/ENG-005.md`,
`agents/qa/test-plans/ENG-005.md`); security verdict **pass**
(`agents/security/reviews/ENG-005.md`, confirmed the component's own
edge-function calls stay behind existing Bearer+admin-role gating, no new
capability granted); devops confirmed release readiness (rollback = revert
commit, $0/month, no freeze, no CI/CD to run). **Deliberately stopped at
`ready-to-ship`** rather than also opening the L1 PR and entering `blocked` —
that would be a 5th transition, over the per-pass cap — reserving the PR-open
for its own hop, same as `ENG-002`'s precedent bundles it with the transition
*into* `blocked` rather than before. `machine_wip` unchanged at 1/6
(`ready-to-ship` is inside the counted range); approval cap and approver WIP
both unchanged — none of this pass's transitions raise a gate item.

**Dead-end sweep:** this ticket's log now ends in a valid, accounted-for
state with a chain record below. `ENG-006` (`awaiting-scope`, owner approver)
out of scope for a `continue` event naming this ticket.

**Notify sweep:** nothing to raise (none of this pass's four states raise a
gate item). Nothing to nudge. Approval cap unchanged at 0/3, not full — no
stall.

`chained: ENG-005` — sitting at `ready-to-ship`, owned by devops (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-005` for the
dedicated session to open the L1 PR and raise the merge-request gate.
Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
whole-board: both exit 0, clean.

## 2026-08-27 — intake ENG-006: loyalty-points request shaped and split — one foundational ticket raised at G1, four more proposed but not filed

`intake` event pass — a new approver request in
`agents/product-manager/inbox/` (via control center): a cross-restaurant
loyalty points program, backend only for now. Narrow scope per the event
contract (shape the new request and carry it as far as it goes; the board was
not swept). Mode check clean (`MODE=active`; instance `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
whole-board (nothing to scope to yet): exit 0, clean.

**Confirmed this was the right event to act on it under.** An earlier
`watch` pass the same day had already found this file and correctly left it
alone — it arrived `via: control-center` with a matching `intake` event
already queued, so shaping it under `watch`'s contract would have both used
the wrong contract and starved the queued `intake` fire of any work to find
(`agents/eng-manager/observations.md`, 2026-08-27). This pass is that queued
fire.

**Full request-readback run** (`skills/request-readback/SKILL.md`): this PM's
reading and a blind architect reading, both independent opus subagents, each
given only the raw request and `knowledge/business-profile.md` — no material
divergence found between them (see `ENG-006`'s own log and PRD for the full
comparison). No question went to the approver as a result; the request is
detailed enough that every load-bearing gap either reading flagged alone was
resolved by proposing a requirement rather than guessing or asking.

**Sized `XL` as a single ticket — split before leaving intake**, per
`config/definition-of-done.md`'s size table. Shaped the identity/OTP-auth/
session/legacy-mapping slice as **`ENG-006`** (`L`, `aiorders-api`, full
lane), the one piece every other slice depends on. PRD written
(`agents/product-manager/specs/ENG-006-unified-customer-identity.md`)
defining the whole proposed five-ticket shape — the other four are
**proposed sequencing only, no IDs allocated, nothing filed** — so this pass
manufactures one ticket's worth of board presence, not five, ahead of the
approver seeing the shape.

**G1 raised** (`size: L` always requires it) — checked caps fresh first:
`wip.approver_limit` (2) at 0, `wip.approval_cap` (3) at 0/3, both free.
`inbox/2026-08-27-eng006-g1-scope.md` written, readback first, then the
recommendation (build `ENG-006` now; the four follow-on slices are open to
correction at this same G1). `lib/eng-notify.sh raise` run (exit 0;
`sent: active` not `sent: raise` — the known `MODE`-collision bug, eighth
corroborating occurrence, still the open `proposals.md` row); `notified:
2026-08-27T13:47:31` stamped. Original request moved
`agents/product-manager/inbox/` → `agents/product-manager/inbox/_handled/`
(new folder — no prior handled-folder existed under the PM's own inbox; this
mirrors the top-level `inbox/_handled/` convention).

**State: `intake → shaped → awaiting-scope`, all in one pass.** `owner`
`product-manager → approver`. Approver-facing WIP 0 → 1; approval cap
0/3 → 1/3. `machine_wip` unchanged at 1/6 — `awaiting-scope` sits outside
that range.

**Dead-end sweep (scoped to this event):** `ENG-006`'s log ends in a valid,
accounted-for state with a chain record. `ENG-005` untouched and out of
scope for this event — it already carries its own valid `chained: ENG-005`
from the immediately preceding pass.

**Notify sweep:** this pass's own gate item raised and stamped above.
Nothing to nudge (brand new). Approval cap 1/3, not full — no stall.

`chained: none` — `ENG-006` sits at `awaiting-scope`, owned by the approver;
the chaining guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-006`) and
whole-board: both exit 0, clean.

## 2026-08-27 — decision ENG-005: surface follow-up answered — designed → ready in the same pass, no one-way door, chained to building

`decision` event pass — the approver answered `ENG-005`'s G1 follow-up
(`inbox/2026-08-27-eng005-g1-followup-surface.md`). Narrow scope per the
event contract (act on the answered gate item, advance only this ticket).
Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**The answer:** `decision: approved`, `decided:
2026-08-27T20:08:53.367622+00:00`, text "lets do RestaurantDetails.tsx" —
confirms the PM's recommendation exactly as offered. Both halves of the
original G1 (fork, then surface) are now answered, so `awaiting-scope`'s exit
condition is met. PRD updated (`status: designed`, acceptance criteria filled
in concretely); gate item moved to `inbox/_handled/` with a processed
footer; journaled in `agents/eng-manager/config/decision-journal.md`.

**Design done this pass** (architect), same one-pass pattern `ENG-002` used
at this boundary. Investigated fresh against `origin/main` in both
`_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch` first):
confirmed the component's `url-shortener` edge-function dependency exists,
confirmed `jspdf` is already in `package.json` (no new dependency), and
read `RestaurantDetails.tsx` in full to find `Restaurant` has no color field
anywhere — not a correction of the follow-up's own investigation, which
never claimed `primaryColor` was loaded (it named only the four fields that
are), just the next question design had to answer that scope selection
didn't. The design passes `null` and relies on the component's own fallback
accent.
Design written:
`agents/architect/designs/ENG-005-a4-poster-generator-wire-in.md` —
`one_way_doors: []`. No one-way door (additive, reversible, no schema, no
new dependency) → `awaiting-decision` (G2) skipped entirely per
`definition-of-done.md`.

**`ready` reached the same pass** (eng-manager): one task, no sequencing,
assigned to frontend. `machine_wip` 0/6 → 1/6. Approver-facing WIP 1 → 0;
approval cap 1/3 → 0/3. **2 transitions this pass**
(`awaiting-scope → designed`, `designed → ready`), under the cap of 4. Did
not proceed into `building` — new implementation work, which is where a pass
stops and hands off instead of pushing through (`schedules/eng_build_loop.md`
step 6).

**Dead-end sweep:** this ticket's log ends in a valid, accounted-for state
with a chain record below. No other ticket in flight — `ENG-004` is terminal.

**Notify sweep:** nothing to raise (no G2 this pass). Nothing to nudge.
Approval cap 0/3, not full — no stall.

`chained: ENG-005` — sitting at `ready`, owned by eng-manager (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-005` for the
dedicated `building` (frontend) session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — watch: ENG-005's G1 answered only half its own question — fork resolved, surface carried forward as one follow-up

`watch` (launchd) pass — a file changed in a watched inbox outside the
notify/poll channel. Mode check clean (business-os `.env` → `MODE=active`;
instance `config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped (`ENG-005`) and
whole-board: both exit 0, clean.

**Swept all three watched inboxes**, per the event's own contract.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` held one
item directly: `2026-08-27-eng005-g1-scope.md`, changed since the archived
`watch` pass a few entries back confirmed it still blank — now carrying
`decision: approved`, `decided: 2026-08-27T18:03:50.514589+00:00`, a second
`## Decision` section appended below the original placeholder. Answered by
direct file edit, not through `lib/eng-notify.sh`'s reply channel — sixth
such occurrence on this instance (decision journal).

**The answer settles the fork and nothing past it.** Verbatim: "wire it in."
This G1's own text asked for two things at once — decide wire-in vs. revert,
and if wire-in, name the route/surface, "so acceptance criteria can be
written against it." Only the fork came back. Read the two halves
separately rather than treating a partial answer as a complete one: "wire it
in" leaves no real ambiguity about the fork (the revert branch is closed,
the component stays); it says nothing about the surface, which this
ticket's own PRD had already flagged twice (Readback's Assumed section,
Non-goals) as the approver's call, not a default the department infers from
silence or convenience.

**Investigated before asking a second time, rather than bouncing the
question back unhelped.** `git fetch origin` in `_eng/aiorders-admin-hub`
(worktree predated `bfddffe`), then read `A4PosterGenerator.tsx` off
`origin/main`: props are `restaurantName`, `websiteUrl`, `logoUrl`,
`primaryColor`, `restaurantId` — one restaurant's own detail context. Of the
admin hub's 19 pages (`src/pages/*.tsx`) and its sidebar
(`AppSidebar.tsx`), exactly one is shaped to hold that context:
`RestaurantDetails.tsx`, which already loads `name`, `website`, `logo_url`
and `id` for a single restaurant (`Restaurants.tsx` is the list view, not a
detail context). No existing poster/QR/marketing section there — wiring in
means a new section, not flipping on something half-built. Offered as a
recommendation in the follow-up, not adopted as the answer: a well-evidenced
guess is still a guess, and this PRD's non-goal is specifically about not
making this one.

**Closed out the answered item, raised one narrow follow-up, left the fork
resolved on the record.** PRD `## Decision`
(`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`)
filled in with the approver's words and this interpretation; `status` stays
`awaiting-scope`. `inbox/2026-08-27-eng005-g1-scope.md` moved to
`inbox/_handled/` with one appended line pointing at the follow-up, so the
closed item is traceable rather than just gone. Wrote
`inbox/2026-08-27-eng005-g1-followup-surface.md` (`agent: product-manager`,
`gate: scope`, `follow_up_to:` the closed item, `recommendation:
RestaurantDetails.tsx`), ran `departments/engineering/lib/eng-notify.sh
raise` on it (reproduced the already-filed `MODE`-collision bug — `sent:
active`, not `sent: raise` — corroborating, not new), stamped `notified:
2026-08-27T18:16:48`. Journaled in
`agents/eng-manager/config/decision-journal.md` — first data point on this
instance of a G1 answer settling part of its own question and leaving a
named, requested sub-detail open.

**Held at `awaiting-scope`, did not advance to `designed`.**
`definition-of-done.md` gives `designed` to the architect for technical
design — not for naming a product surface this PRD explicitly reserved for
the approver. Advancing without the surface would just move the guess one
state later and relabel it a design decision instead of a scope one. `owner`
stays `approver`. No cap or WIP change — still the same one approver-facing
slot this ticket already held (approval cap unchanged at 1/3, approver WIP
unchanged at 1), narrowed to one question on it.

**Dead-end sweep:** `ENG-005`'s log now ends in a valid, accounted-for state
with a chain record below. No other ticket is in flight to check — `ENG-004`
reached `verified` (terminal) in the pass immediately before this one; see
its own board file and the dated entry below.

**Notify sweep:** this pass's own follow-up was raised and stamped above —
nothing else to raise. Nothing to nudge (`ENG-005`'s original G1 is now
answered and closed, its follow-up is minutes old). Approval cap unchanged
at 1/3, not full — no stall.

`chained: none` — sitting at `awaiting-scope`, owned by the approver; the
chaining guard never fires on a ticket waiting on a human. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — continue ENG-004: ready-to-ship through verified in one pass — G3 answered in ~92 seconds, ticket now terminal

`continue ENG-004` event pass — the dedicated `ready-to-ship` (devops)
session the preceding `in-security` hop chained. Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean. Pre-pass `departments/engineering/lib/eng-gate-check.sh`,
scoped and whole-board: both exit 0, clean.

**`in-security → ready-to-ship`, 1 transition.** Acted as devops per
`ADR-004`: confirmed no release, rollback, or observability plan is owed —
the change already reached `origin/main` on 2026-08-24, before this ticket
existed. Re-checked `config/projects.md` (L1, worktree present), release
window (Thursday, no `ENG_RELEASE_FREEZE`), and cost (`$0/month`) fresh.
`machine_wip` 1/6 → 0/6.

**Continued into `awaiting-release` the same pass** — unlike `ENG-001`'s
split at this identical boundary, which its own log names as cap-driven; the
approval cap here had room (checked fresh: 1/3, only `ENG-005`'s G1), so
nothing forced a stop. No ADR or schedule rule names a fresh-context
requirement between these two states, unlike security-after-quality. Wrote
and raised `inbox/2026-08-27-eng004-g3-verification.md` (`lib/eng-notify.sh
raise`) — reproduced the already-filed `MODE`-collision/Slack-not-Telegram
bugs (`proposals.md`, 2026-08-25), not a new finding. Cap 1/3 → 2/3; approver
WIP 1 → 2. **2nd transition.**

**The G3 was answered before this pass exited** — `decision: approved`, no
comment, ~92 seconds after `notified:` was stamped, by the same hand-edit
shape every gate on this instance but `ENG-002`'s merge has used. Fifth data
point on that pattern; the turnaround itself journaled as consistent with,
not proof of, the open notify-channel proposal
(`agents/eng-manager/config/decision-journal.md`). Item moved to
`inbox/_handled/`.

**`awaiting-release → shipped`, 3rd transition.** Devops recorded the G3
confirmation in place of a deploy — no release record fabricated at
`agents/devops/releases/`, `links.release` stays empty (`ADR-004`).

**`shipped → verified`, 4th transition — 4 total this pass, at the cap.**
Product-manager re-confirmed all five acceptance criteria fresh against
disk/git (project linkage, admin-hub's empty `supabase/` tree, two re-sampled
blob-SHA matches, the 22-file ordering, `0`/`0` ahead-behind) and re-opened
all three receipts — all hold. Full citations on the ticket's own log.

**This ticket is now terminal.** `machine_wip` stays 0/6; approval cap
2/3 → 1/3 (`ENG-005`'s G1 only); approver WIP 2 → 1 — noted for the next
pass's arithmetic, not acted on here.

**Dead-end sweep (scoped to `ENG-004`):** ends in a valid, terminal state.
`ENG-005` untouched — out of scope for this event.

**Notify sweep:** the pass's own gate item was raised and is already
answered above; nothing else to raise or nudge.

Post-pass `departments/engineering/lib/eng-gate-check.sh`, scoped and
whole-board: both exit 0, clean. `chained: none` — `verified`, terminal;
never re-fired.

## 2026-08-27 — continue ENG-004: in-security verdict pass — content-reviewed, not just hash-checked; chained to ready-to-ship

`continue ENG-004` event pass — the dedicated `in-security` session the
preceding combined review+quality hop chained. Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Dispatch: `in-qa → in-security`, 1 transition.** Acted as security per
`ADR-004` — the one gate on this ticket with real content, not ceremony.
Independently re-derived AC1/presence/AC4 fresh against disk/git in
`_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch origin` in both
first); re-confirmed AC3 (unmodified) by a second, independent mechanism
(git's own blob SHA, not review/QA's SHA-256) — all six files identical
pairwise across both repos. Then read the six files' actual content, the
substantive check neither review nor QA did: coherent, complete
RLS/`search_path` hardening across `profiles`, `restaurants`, and the new
`restaurant_activations` table. Verdict **pass** —
`agents/security/reviews/ENG-004.md` written, `links.security_review` set.
Full citations on the ticket's own log. `machine_wip` unchanged at 1/6 —
`in-security` falls inside the counted range.

**One observation filed, not a finding** (`observations.md`): a migration
comment about view security semantics that reads backwards against actual
Postgres defaults (`restaurants_public`'s recreate, item 5 of the six) —
explicitly out of this ticket's scope per the PRD's own non-goal ("whether
that policy is still the right policy today"), since the reconciliation
itself is confirmed intact by an independent hash method.

**Not proceeding into `ready-to-ship` this pass, deliberately** — same
discipline this ticket has used at every prior hop; devops's own
confirmation (no release/rollback/observability plan owed, per `ADR-004`) is
real, distinct work reserved for its own session.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`in-security` raises no gate item).
Nothing new to nudge — `ENG-005`'s G1 still under 24h old; approval cap
unchanged at 1/3.

`chained: ENG-004` — sitting at `in-security`, owned by `security` (agent,
not the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
dedicated `ready-to-ship` (devops) session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — continue ENG-004: combined review+quality hop — building → in-review → in-qa, security deferred to its own session

`continue ENG-004` event pass — the dedicated combined review+quality session
the preceding `ready → building` pass chained (queued behind one intervening
no-op `watch` fire, drained immediately after). Narrow scope per the event
contract (resume this ticket from its current state; no board-wide sweep).
Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

**Dispatch: `building → in-review → in-qa`, 2 transitions.** Acted as
principal-engineer and qa on the combined hop (`schedules/eng_build_loop.md`
step 6): independently re-derived all five acceptance criteria fresh against
disk/git in `_eng/aiorders-admin-hub` and `_eng/aiorders-api` (`git fetch
origin` in both first) rather than citing the design's or `building`'s own
numbers — project linkage, the still-empty `supabase/migrations` on
admin-hub's `origin/main`, both consolidation commit pairs, a fresh
`shasum -a 256` re-hash of all six named files (all identical), the 22-file
migration count/ordering, and the ref-level `0`/`0` ahead-behind on admin-hub's
local `main`. Verdict **pass** on both:
`agents/principal-engineer/reviews/ENG-004.md` and
`agents/qa/test-plans/ENG-004.md` written, `links.review`/`links.test_plan`
set. Full citations on the ticket's own log. `machine_wip` unchanged at 1/6 —
both states fall inside the counted range.

**Not proceeding into `in-security` this pass, deliberately** — sharper than
the "own session" discipline this ticket has used at every prior hop:
`ADR-004` names this ticket's security gate as real, substantive content
(five of six files under review are the RLS/`search_path` hardening surface
itself) and warns explicitly against waving it through as ceremony, unlike
`ENG-001`'s all-`n/a` security pass (the one case here where review, quality
and security were combined into a single session). Reserved for its own
dedicated pass with fresh context.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`in-qa` raises no gate item). Nothing new
to nudge — `ENG-005`'s G1 is still well under 24h old; approval cap unchanged
at 1/3.

`chained: ENG-004` — sitting at `in-qa`, owned by `qa` (agent, not the
approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the dedicated
`in-security` session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`, scoped and whole-board: both
exit 0, clean.

## 2026-08-27 — watch: swept all three inboxes again, nothing new — seventh occurrence, ENG-005's G1 fingerprint-stale exactly as diagnosed

`watch` (launchd) pass, drained immediately behind the `continue ENG-004`
(`ready → building`) pass that ended 10:13:51 (`traces/eng-loop-2026-08-27.log`,
549s, exit 0) — day 5/40 hops charged, 0 refunded today. Per the event's own
narrower contract, swept only `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/` (including `inbox/requests/`),
acting on whatever is new. Mode check clean (business-os `.env` →
`MODE=active`; instance `config/config.yaml` → `mode:` empty, falls
through). Pre-pass `departments/engineering/lib/eng-gate-check.sh` (`env
ENG_ROOT=<instance> sh eng-gate-check.sh`): exit 0, clean.

**Swept all three inboxes; found nothing to act on.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly one file directly — `2026-08-27-eng005-g1-scope.md` — which is
`ENG-005`'s own G1, raised and notified by the `scheduled` pass earlier this
same day (see that entry below); `inbox/_handled/`'s ten items are all
already accounted for, none new. Read the gate item itself and the PRD's own
`## Decision` section
(`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`)
directly rather than trusting the board's characterization of it: both still
carry the unfilled template placeholder ("Filled in by the approver." / "The
approver's answer:" blank) — no decision recorded anywhere. Nothing new to
act on for `ENG-005`; it stays exactly at `awaiting-scope`, owner `approver`.

**Seventh occurrence of the already-diagnosed `.watch-seen` staleness
pattern** (`observations.md` and `proposals.md`'s open 2026-08-26 row carry
the first six; the sixth is this board's own archived entry from earlier
today). Confirmed the mechanism live rather than assuming it still applies:
`traces/.watch-seen` currently holds
`da39a3ee5e6b4b0d3255bfef95601890afd80709` — the SHA-1 of an empty input —
meaning the last `watch`-typed pass to commit a fingerprint saw all three
inboxes empty, and every non-`watch` pass since (today's `continue ENG-004`
×2 and the `scheduled` sweep) changed `inbox/`'s top-level contents without
ever being able to update it, per `commit_watch_fingerprint`'s own `[
"$EVENT" = "watch" ]` guard (`lib/eng-trigger.sh`). Exactly the fix the open
proposal already names. **Not filing a new proposal or observation** — a
seventh data point on an already-diagnosed, already-proposed issue is
corroboration, same restraint every occurrence since the fourth has applied.

**Queue backlog, unchanged from the entry above.** `traces/.pending` still
holds `1 continue ENG-004` — appended by the `ready → building` pass's own
chain fire for the combined `in-review`/`in-qa` session, queued behind this
`watch` fire only because `watch` was older in the queue (the file-watcher
fired on `inbox/2026-08-27-eng005-g1-scope.md`'s creation before that chain
fire ever ran). Not re-fired here: `continue ENG-004` was queued by its own
originating pass, and re-firing it would only duplicate a line the queue's
own dedup collapses back down.

**Dead-end sweep:** out of scope for this event beyond the inboxes it
unblocks. `ENG-004` (`building`, owner `eng-manager`) and `ENG-005`
(`awaiting-scope`, owner `approver`) both already carry valid chain records
from their own last passes, untouched here.

**Notify sweep:** nothing to raise (no gate item written this pass); nothing
to nudge (`ENG-005`'s G1 is under an hour old, no `nudged:` due); approval
cap unchanged at 1/3, not full, no stall.

No ticket was touched this pass, so no ticket log carries a chain record —
the record lives here instead, same convention every no-op `watch` entry on
this board has used. `chained: none` — nothing this pass owns to chain;
`continue ENG-004` is already queued from its own originating pass, not
re-fired. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean, unchanged.

## 2026-08-27 — continue ENG-004: building-as-verification-record written per ADR-004

`continue ENG-004` event pass — the dedicated session the preceding
`designed → ready` pass chained. Narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
`mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Dispatch: `ready → building`, 1 transition.** Re-verified all five
acceptance criteria fresh against disk/git in `_eng/aiorders-admin-hub` and
`_eng/aiorders-api` (`git fetch origin` in both first) rather than trusting
`designed`'s prior citations — project linkage, the absence of any
`supabase/migrations`/`functions` directory on admin-hub's `origin/main`,
both consolidation commit pairs, a fresh `sha256` re-hash of all six named
files against their new home in `aiorders-api` (all identical — a stronger
check than the design's own byte-diff), the 22-file migration count and
ordering, and a ref-level (not working-tree) confirmation that admin-hub's
local `main` is 0 ahead/0 behind `origin/main`. All five held exactly as
`designed` recorded them a day earlier — nothing drifted. `branch:` stays
empty per `ADR-004` (the diff this ticket investigated already exists on
`origin/main`, produced by the approver directly on 2026-08-24, not by this
ticket). `machine_wip` unchanged at 1/6 — both `ready` and `building` fall
inside the counted range. Full citations on the ticket's own log.

**Not proceeding into `in-review`/`in-qa` this pass, deliberately** — per
`schedules/eng_build_loop.md` step 6 those are one combined hop, and each
still owes its own independent re-derivation against disk/git per `ADR-004`
— real, distinct gate work reserved for its own session, same discipline
this ticket has applied at every earlier hop.

**Dead-end sweep (scoped to `ENG-004`):** its log now ends in a valid,
accounted-for state with a chain record below. `ENG-005` (`awaiting-scope`,
owner approver) untouched — out of scope for a `continue` event naming one
ticket.

**Notify sweep:** nothing to raise (`building` raises no gate item). Nothing
new to nudge — approval cap unchanged at 1/3 (`ENG-005`'s G1 only).

`chained: ENG-004` — sitting at `building`, owned by `eng-manager` per
`ADR-001`'s owner override as extended by `ADR-004` (agent, not the
approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
combined `in-review`/`in-qa` session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — scheduled: safety-net sweep — ENG-005's G1 raised, ENG-004 left mid-chain

`scheduled` (launchd) pass — the twice-daily safety-net sweep. Mode check
clean (business-os `.env` → `MODE=active`; instance `config/config.yaml` →
`mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty (`.gitkeep`
only) — nothing new to shape or propose.

**Gate returns:** `inbox/` holds nothing outside `_handled/` — no answered
item to act on. Cross-checked `inbox/_handled/` (ten items) against the
board and the decision journal; all already reflected.

**Merge detection:** no in-flight ticket is `blocked` on anything — no-op.

**Dispatch (priority order `now` → empty; neither in-flight ticket has a
`priority` set):** reviewed both in-flight tickets.

- `ENG-004` (`ready`, owner `eng-manager`) — left untouched, deliberately.
  Its own last log entry already chained a dedicated `continue ENG-004`
  session for the building-as-verification-record step, and
  `traces/.pending` confirms it (`1 continue ENG-004`), still undrained.
  Re-firing it here would only duplicate an already-queued line, and
  attempting `ready → building` inline would break the same discipline this
  exact hop has followed at every prior occurrence on this board — reserved
  for its own dedicated session.
- `ENG-005` (`shaped`, owner `product-manager`) — the only ticket in the
  To-do column (`intake`/`shaped`/`awaiting-scope`), so it's what this
  step's ordering picks up. Re-checked the caps fresh rather than trusting
  the board's cached header: `wip.approver_limit` (2) at 0, `wip.approval_cap`
  (3) at 0/3, both fully free. Raised its G1 —
  `inbox/2026-08-27-eng005-g1-scope.md` — framed as the fork itself rather
  than a plan to approve (wire `A4PosterGenerator.tsx` into a named surface,
  or revert `bfddffe`), matching this ticket's own PRD, which deliberately
  never proposed a direction. Advanced `shaped → awaiting-scope`, `owner`
  `product-manager → approver`. Full reasoning on the ticket's own log.

**Notify sweep.** Ran `departments/engineering/lib/eng-notify.sh raise
inbox/2026-08-27-eng005-g1-scope.md`; stamped `notified: 2026-08-27T09:59:41`
on the gate item. Reproduced the already-filed `MODE`-collision bug
(`traces/eng-notify-2026-08-27.log`: `sent: active`, not `sent: raise`) —
corroborating the open 2026-08-25 proposal, not a new finding. No nudge due
— `ENG-005`'s G1 is minutes old and nothing else is open. Approval cap
0/3 → 1/3, not full — no stall alert.

**Dead-end sweep.** `ENG-004`'s log ends in a valid, accounted-for state
with its own chain record (`continue ENG-004`, already queued, untouched
here). `ENG-005`'s log now ends in a valid state too, written this pass.
`config/exceptions.md` is empty — nothing at a third occurrence.
`proposals.md`'s five open rows are all 0–2 days old, none near the 30-day
expiry.

**One observation filed** (`observations.md`): uncommitted modifications
found in the department's own (shared, read-only-to-an-instance) tree at
this pass's start — `lib/eng-schedule.sh` and
`schedules/eng_weekly_report.md` modified, `lib/eng-report.sh` untracked.
None of the three is a file this loop reads (`eng-gate-check.sh`,
`eng-trigger.sh`, and `eng_build_loop.md` itself are all untouched), so out
of scope to act on from inside this pass; flagged since the department
directory is meant to be read-only from an instance's perspective.

**Chain.** `ENG-005` — `chained: none`, written on the ticket's own log:
sitting at `awaiting-scope`, owned by the approver. `ENG-004` — not touched
this pass, so the record lives here instead: `chained: none — continue
ENG-004` already queued from its own prior pass; re-firing here would only
duplicate a line the queue's own dedup collapses back to one, spending a
fire for no additional effect.

Approver-facing WIP 0 → 1, approval cap 0/3 → 1/3, machine WIP unchanged at
1/6. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean.

## 2026-08-27 — continue ENG-004: work breakdown done, zero implementation units — advanced to ready

`continue ENG-004` event pass — the dedicated work-breakdown session the
`designed → ready` hand-off named. Narrow scope per the event contract
(resume the named ticket from its current state; no board-wide sweep). Mode
check clean (business-os `.env` → `MODE=active`; instance `config/config.yaml`
→ `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Work breakdown: zero implementation units.** Per `ADR-003`/`ADR-004`, the
remediation this ticket investigated was already executed by the approver
directly on 2026-08-24 — nothing to sequence, nothing to assign. Advanced
`ENG-004` `designed → ready`, owner `architect → eng-manager` per
`definition-of-done.md`. `machine_wip` 0/6 → 1/6. No approver-facing WIP or
approval-cap impact — `ready` raises no gate. Full reasoning on the ticket's
own log.

**Not proceeding into `building` this pass, deliberately** — same split
`ENG-001`'s history applied at this identical hop, already flagged by this
ticket's own prior log entry: `ready → building` is reserved for its own
session.

**Dead-end sweep (scoped to `ENG-004`):** log ends in a valid state with a
chain record. `ENG-005` untouched — out of scope for a `continue` event
naming one ticket.

**Notify sweep:** nothing to raise (no gate at `ready`); nothing to nudge
(approval cap 0/3).

`chained: ENG-004` — sitting at `ready`, owned by `eng-manager` (agent, not
the approver, not blocked, not terminal). Fired `/bin/zsh
departments/engineering/lib/eng-trigger.sh continue ENG-004` for the
building-as-verification-record session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-27 — watch: swept all three inboxes again, nothing new — sixth occurrence, queue backlog sitting behind it

`watch` (launchd) pass, `traces/.pass-out.24282`: `pass start: watch (launchd)
[day 1/40 charged, 0 refunded today]`, after the queue collapsed 1 duplicate
`watch launchd` event into one. Per the event's own narrower contract, swept
only `agents/product-manager/inbox/`, `agents/eng-manager/inbox/` and
`inbox/`, plus `inbox/requests/`, acting on whatever is new. Mode check clean
(business-os `.env` → `MODE=active`; instance `config/config.yaml` → `mode:`
empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh` (`env ENG_ROOT=<instance> sh
eng-gate-check.sh`): exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` itself
holds no files directly — everything that has ever landed there has already
moved to `inbox/_handled/` (ten items, spanning the original approver
requests through `ENG-003`'s G1), none new. Sixth recorded instance of a
`watch` fire finding nothing (`observations.md`'s rows, `proposals.md`'s open
row, and this board's archived/live entries carry the first five).

**Queue backlog, noted rather than freshly diagnosed.** `traces/.pending`
currently holds `1 continue ENG-004` and `1 scheduled launchd`, both still
undrained as this pass runs — today's own 09:30 safety-net sweep queued
behind an older event rather than running. Consistent with
`eng_build_loop.md`'s description of the queue (a fire drains the front only
when it reaches the lock; an idle stretch leaves whatever's queued sitting
untouched) rather than a new mechanism traced through the code this pass —
unlike the fifth occurrence's addendum, this isn't offered as a sharpened
root cause, just an honest note of what's on disk right now. Not re-fired:
`continue ENG-004` was queued by its own originating pass (`2026-08-26 —
continue ENG-004`, this board), and re-firing it here would only duplicate a
line the queue's own dedup collapses back down — same restraint every
occurrence since the fourth has applied. `scheduled launchd` is likewise left
for the next fire to drain; forcing a board-wide sweep from inside a
`watch`-scoped pass would be exactly the job this event's own narrower
contract reserves for `scheduled` itself.

**Not filing a new proposal or observation.** No new mechanism was traced
here beyond what `proposals.md`'s open row and `observations.md`'s addendum
already cover; a sixth data point on an already-diagnosed, already-proposed
issue is corroboration, same reasoning the fourth occurrence gave for
declining to refile.

**Dead-end sweep:** out of scope for this event beyond the inboxes it
unblocks. `ENG-004` (`designed`, owner `architect`) and `ENG-005` (`shaped`,
owner `product-manager`) both already carry valid chain records from their
own last passes, untouched here.

**Notify sweep:** nothing to raise (no gate item written this pass). Nothing
open to nudge — approval cap is 0/3, nothing waiting on the approver.

No ticket was touched this pass, so no ticket log carries a chain record —
the record lives here instead, same convention every no-op `watch` entry on
this board has used. `chained: none` — nothing this pass owns to chain;
`continue ENG-004` is already queued from its own originating pass, not
re-fired. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean, unchanged.

## 2026-08-26 — watch: swept all three inboxes again, nothing new — fifth occurrence, a distinct mechanism from the open proposal

`watch` (launchd) pass — drained immediately behind the `decision` no-op
directly above: that pass ended 23:16:55 and this one began draining the
same second (`traces/eng-loop-2026-08-26.log`). Per the event's own narrower
contract, swept only the three watched inboxes plus `inbox/requests/`,
acting on whatever is new. Mode check clean (business-os `.env` →
`MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly one item, `2026-08-25-eng003-g1-scope.md` — checked against its last
committed version (`git diff`), the only change is the
`nudged: 2026-08-26T15:43:45` stamp already recorded on this board's
"Waiting on the approver" list; still no `decision:`. `inbox/_handled/`
matches the board exactly (`ENG-001`'s G3, `ENG-002`'s merge request,
`ENG-004`'s G1), all already reflected in ticket state and the decision
journal. Nothing to act on.

**Root cause, read from the code rather than assumed.** Fifth recorded
`watch`-fires-for-nothing occurrence (`observations.md`'s two rows and the
open proposal's row, `proposals.md` 2026-08-26, carry the first four) — but
a different mechanism from the one that proposal diagnoses, which blames
non-`watch` event types never committing `.watch-seen`. Read
`lib/eng-trigger.sh` directly: `WATCH_FP` is computed **before the pass
launches** (line 1583), deliberately — its own comment says anything that
arrives *during* a pass must still look new to the next fire — and
`commit_watch_fingerprint` (line 424) writes that unchanged pre-launch value
to `.watch-seen` **only on a clean exit** (`if [ "$STATUS" -eq 0 ]`, line
1892-1893). The immediately-preceding `watch` pass (pid 73496, `pass end:
watch (exit 0, 669s)` at 23:08:31) exited 0 and so committed — but it had
just moved `2026-08-25-eng004-g1-scope.md` out of `inbox/` into `_handled/`
as part of processing `ENG-004`'s G1, so the fingerprint it committed
reflects `inbox/`'s state *before* that move, not after. Any `watch` pass
that actually processes a gate item modifies a watched inbox this same way,
so this isn't a one-off: it guarantees the next `watch` fire sees a diff and
relaunches for zero new work, every time a `watch` pass does real work. The
open proposal's fix ("commit after every event type") doesn't cover this —
the pass that caused it *was* `watch`-typed and *did* commit. Filed as an
addendum in `observations.md` rather than a second proposal — it sharpens
the existing one's required fix scope, it doesn't ask for a new ticket.

**Dead-end sweep:** `ENG-003` (`awaiting-scope`), `ENG-004` (`designed`) and
`ENG-005` (`shaped`) ticket logs each already end in a valid, accounted-for
state with their own chain record — none touched by this pass, none a dead
end. `traces/.pending` still holds exactly `1 continue ENG-004`, queued by
the preceding `watch` pass and not yet drained; not re-fired here, same
reasoning the preceding `decision` pass gave for the identical situation.

**Notify sweep:** nothing to raise (no gate item written this pass); no
nudge due (`ENG-003` already nudged once, 2026-08-26). Approval cap
unchanged at 1/3 — not full, no stall alert.

No ticket was touched this pass, so no ticket log carries a chain record —
same as the `decision` no-op two entries above; the record lives here
instead. `chained: none` — nothing this pass owns to chain; `continue
ENG-004` is already correctly queued from the prior pass. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean, unchanged.

## 2026-08-26 — continue ENG-004: investigation found the consolidation already done — design + ADR-003 + ADR-004 written

`continue ENG-004` event pass — the dedicated investigation-and-design
session the preceding `watch` pass chained. Narrow scope per the event
contract (resume the named ticket from its current state; no board-wide
sweep). Mode check clean (business-os `.env` → `MODE=active`; instance
`config/config.yaml` → `mode:` empty, falls through). Pre-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Investigated in the department's own worktrees** (`_eng/aiorders-admin-hub`,
`_eng/aiorders-api`; the human's checkouts were never touched), `git fetch`
first in both. Found both `_eng/` branches diverged from `origin/main` —
admin-hub's mildly, aiorders-api's by dozens of commits predating this
consolidation entirely — so read `origin/main` directly rather than trusting
either worktree's files (logged as an observation, see below).

**The investigation this ticket asked for turned out to already be answered.**
`aiorders-api` is authoritative: two paired same-session commits, both
2026-08-24 (`4b6a835`/`c90c02c` at ~09:52, `5b3bac2`/`919d355` at ~10:18,
seconds apart each pair) moved every migration from `aiorders-admin-hub` to
`aiorders-api` and removed admin-hub's `supabase/migrations` entirely — **the
approver did this directly, one day after filing the request, before the
ticket ever reached `shaped`.** Content-diffed all six named files
byte-for-byte against their new home: all six identical, one renamed
(UUID-suffixed filename → descriptive name), none edited — confirming the
"renamed consolidation" the architect's blind reading flagged as unruled-out
by a filename sweep. `20260312000001_restaurant_activations.sql` now sorts
before `20260408000001_google_review_history.sql` in the same repo, resolving
the replay-order hazard the original request named. The PRD's flagged "four
siblings" discrepancy is resolved too — the real count is three, matching the
three timestamps actually named. `aiorders-admin-hub`'s local `main` already
matches `origin/main` exactly (no ahead/behind), so the pending uncommitted
deletion the request opened with is resolved at the ref level. Attempted an
actual local Docker replay for extra confidence beyond the static diff;
aborted mid-image-pull as disproportionate once it was clear the static
evidence already answered the question — Docker left clean, scratch dirs
removed. Full citations (commit hashes, timestamps, diff results) on the
design doc and the ticket's own log.

**All five acceptance criteria satisfied without a diff — a second
verification-only ticket on this instance, but not `ADR-001`'s reason.**
`aiorders-admin-hub` **is** registered (L1); a diff was the right mechanism
and one happened, just not from this ticket's own `building` state. Wrote
`ADR-003` (`aiorders-api` authoritative, `decided_by: approver`, recorded
retroactively) and `ADR-004` (extends `ADR-001`'s verification-ticket pattern
across this ticket's entire remaining lane in one ADR, `decided_by:
architect`) — explicitly engaging `ADR-001`'s own Review trigger for a second
occurrence and declining both alternatives it raises (internal-lane: admin-hub
fails the lane's own no-deploy-target test on the facts; G2 on the pattern:
premature at two occurrences with different causes). `in-security` is named
explicitly as real work here, not ceremony — five of the six files under this
ticket's history are the security surface itself. No one-way door — the
ownership move is an executed fact, not a pending decision; nothing to
escalate. Tech design at
`agents/architect/designs/ENG-004-admin-hub-migration-history.md`.
`agents/architect/decisions/_index.md` updated, Next ID now `ADR-005`.

**Three observations filed** (`agents/eng-manager/observations.md`), none
folded into this ticket's scope: `_eng/aiorders-api`'s worktree divergence
from `origin/main` (a future investigation trusting that worktree's files for
this repo would be wrong); admin-hub's `supabase/config.toml` still lists 20
orphaned `[functions.*]` stanzas for functions no longer in that repo;
and this ticket's whole subject having been resolved by the approver directly
mid-flight, named in `ADR-004`'s Review trigger as a pattern worth watching
for a second occurrence.

**Not proceeding into `ready` or `building` this pass, deliberately** — same
discipline `ENG-001`'s own history applied at this exact point (each of
`shaped→designed`, `designed→ready`, `ready→building` was its own separate
pass): work breakdown and the building-as-verification-record step are real,
distinct work reserved for their own sessions, and `ADR-004` leaves whoever
picks this up next everything needed to act without re-deriving it.
`machine_wip` (6) and the approval cap are both unaffected — `designed` isn't
in the counted range, no gate item was raised.

**Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
log now ends in a valid, accounted-for state with a chain record below.
`ENG-003` (`awaiting-scope`) and `ENG-005` (`shaped`) untouched this pass —
out of scope for a `continue` event naming one ticket.

**Notify sweep:** no gate item written this pass — nothing to raise. No nudge
due (`ENG-003` already nudged once, 2026-08-26). Approval cap unchanged at
1/3 — not full, no stall alert.

`chained: ENG-004` — `designed`'s exit condition now met (design written,
ADRs logged, no one-way door outstanding), owned by `architect` handing to
`eng-manager` for work breakdown (agent, not the approver, not blocked, not
terminal). Fired `/bin/zsh departments/engineering/lib/eng-trigger.sh continue
ENG-004`. Post-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0,
clean.

## 2026-08-26 — decision: ENG-003's G1 rejected — dropped

`decision` event pass, context `2026-08-25-eng003-g1-scope.md` — narrow scope
per the event contract (act on the answered gate item and advance only the
ticket it belongs to; no board-wide sweep). Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Gate return: `ENG-003`'s G1 answered — rejected.** Hand-edited directly
(frontmatter `decision:`/`decided:` set, a second `## Decision` section
appended below the still-blank original placeholder) rather than through
`lib/eng-notify.sh`'s reply channel — fourth such occurrence today,
after `ENG-002`'s GitHub merge, `ENG-001`'s G3, and `ENG-004`'s G1 (decision
journal). `decided: 2026-08-27T06:38:51.515614+00:00`
(2026-08-26T23:38:51.515614-07:00 local). Verbatim answer, the only reason
given: "Drop this ticket do not  need to be done." **First outright G1
rejection this department has recorded** — every prior G1 (`ENG-002`,
`ENG-004`) was approved as scoped.

**Advanced `ENG-003` `awaiting-scope → dropped`, owner `eng-manager` — no
other transition is available at a killed G1.** PRD `status: rejected`
(`agents/product-manager/specs/ENG-003-aiorders-env-hygiene.md`, `##
Decision` filled in). Gate item moved to
`inbox/_handled/2026-08-25-eng003-g1-scope.md` unedited. Journaled in
`agents/eng-manager/config/decision-journal.md`, including a
grounded-but-labelled-as-interpretation read: the PRD's own Problem section
already noted the tracked `.env` values are public-by-design in the shipped
bundle regardless of git tracking, so the git-hygiene fix may have read as
low-value on its own once separated from the Maps-key question it couldn't
resolve anyway — not confirmed, not asked. Flagged there as a relevant prior
data point for the still-open `restaurant-portal` `.env` proposal
(`proposals.md`, 2026-08-26 row, same fix family) whenever that batch reaches
the approver — not acted on now, since an unapproved proposal is a separate
decision on its own timeline. `depends_on`/`blocks` both empty on `ENG-003`
— no other ticket affected by the drop.

**Consequence:** approval cap 1/3 → 0/3; approver-facing WIP 1 → 0. Nothing
dispatched onto the freed capacity this pass — out of scope for a `decision`
event scoped to the one gate item it answers, same restraint prior passes
applied to the same situation.

**Notify sweep:** no gate item written this pass (one was consumed, none
raised) — nothing to `raise`. No nudge due — the only open item was this one,
now answered. Approval cap dropped, not filled — no stall alert.

**Dead-end sweep (scoped to `ENG-003`, the ticket this event names):** its
log now ends in a valid, accounted-for state (`chained: none — dropped,
terminal`), written this pass. `ENG-004` and `ENG-005` untouched, out of
scope for this event.

`chained: none` — `ENG-003` is `dropped`, a terminal state; the chaining
guard never re-fires a terminal ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-26 — decision: ENG-004's G1 already resolved by the preceding watch pass — no-op

`decision` event pass, context `2026-08-25-eng004-g1-scope.md` — narrow scope
per the event contract (act on the answered gate item and advance only the
ticket it belongs to; no board-wide sweep). Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `departments/engineering/lib/eng-gate-check.sh`:
exit 0, clean.

**Gate return: already handled.** The named item was gone from `inbox/`
before this pass opened it — already at `inbox/_handled/2026-08-25-eng004-g1-scope.md`,
`decision: approved`, `decided: 2026-08-27T05:57:21.472123+00:00`. Per
`traces/eng-loop-2026-08-26.log`, the immediately preceding `watch` pass drained
in the same sequence with no gap (`pass end: watch (exit 0, 669s)` →
`draining queued event: decision (2026-08-25-eng004-g1-scope.md)`, same
second) and had already found this same hand-edited gate item and fully
processed it — see the entry directly above. Verified fresh rather than
trusted from that entry: PRD `status: approved` (`agents/product-manager/specs/ENG-004-*.md`),
the decision-journal row present, the ticket at `designed` owned by
`architect`, and the board's own In-flight row already correct. All four
consistent — nothing left to act on.

**Why both fired for one edit.** The approver answered by hand-editing the
gate item file directly — third such bypass of `lib/eng-notify.sh`'s reply
channel in two days (decision journal) — which changes a file inside a
watched `inbox/`. That one edit is visible to both the poll-detected
`decision` path and the raw file-watch `watch` path, and
`schedules/eng_build_loop.md`'s queue dedup only collapses identical
`<event> <context>` lines, so `decision (2026-08-25-eng004-g1-scope.md)` and
`watch (launchd)` never recognize each other as the same work. Whichever
drains first does it; the loser — this pass — finds nothing. Logged as one
data point in `agents/eng-manager/observations.md` rather than proposed: a
first occurrence of this specific race, and distinct from the already-open
`.watch-seen` staleness proposal (that one is watch-after-non-watch; this is
decision-vs-watch on the same edit).

**Dead-end sweep (scoped to `ENG-004`, the ticket this event names):** its
log already ends in a valid, accounted-for state (`chained: ENG-004`,
written by the preceding pass) — not a dead end, nothing to resume.
`ENG-003` and `ENG-005` untouched, out of scope for this event.

**Notify sweep:** nothing to raise (no gate item written this pass); no
nudge due (`ENG-003` already nudged once, 2026-08-26). Approval cap and WIP
unchanged — no stall alert.

No ticket transition made this pass, so no new entry on `ENG-004`'s own log —
its log already ends in a correct, unbroken chain record and this pass added
no new fact beyond confirming that record still holds. Approver-facing WIP
unchanged at 1 (`ENG-003` only), approval cap unchanged at 1/3, machine WIP
unchanged at 0/6. `chained: none` — `continue ENG-004` is already queued
(`traces/.pending`: `1 watch launchd` / `1 continue ENG-004`) from the
preceding pass's own chain fire; re-firing it here would only append a
duplicate line that the queue's own dedup collapses back to one at its next
pop, spending a fire for no additional effect. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean, unchanged.

## 2026-08-26 — watch: ENG-004's G1 answered by direct file edit — handed to the architect

`watch` (launchd) pass — a file changed in a watched inbox outside the
notify/poll channel. Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three watched inboxes**, per the event's own narrower contract.
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` empty
(`.gitkeep` only); `inbox/requests/` empty. `inbox/` held two items:
`2026-08-25-eng003-g1-scope.md` — read fresh, still blank, still just the
2026-08-26 nudge from a prior pass, nothing new — and
`2026-08-25-eng004-g1-scope.md` — **answered** since the last pass touched
it (the `decision` pass immediately above this entry closed `ENG-001`'s G3
only and left this item untouched).

**Gate return: `ENG-004`'s G1 approved**, `decided:
2026-08-27T05:57:21.472123+00:00` (2026-08-26T22:57:21-07:00 local), no
additional comment. Answered by directly hand-editing the gate item file —
frontmatter `decision:`/`decided:` set and a second `## Decision` section
appended below the still-blank original placeholder — rather than through
`lib/eng-notify.sh`'s reply channel; third such occurrence in two days after
`ENG-002`'s GitHub merge and `ENG-001`'s G3 (decision journal). PRD `status:
approved`; gate item moved to `inbox/_handled/` unedited, same treatment as
`ENG-001`'s G3; journaled in `agents/eng-manager/config/decision-journal.md`.

**Advanced `ENG-004` `awaiting-scope → designed`, owner `architect` —
handoff only, design work not started this pass.** `designed`'s exit
condition for this ticket is a live-database investigation (confirm
`admin-hub`'s Supabase project linkage, read the live migration ledger,
content-diff six files against `aiorders-api`'s nine), not a light design
choice — real work against a project with live operator/customer data,
same class of thing `schedules/eng_build_loop.md`'s Cadence section reserves
`building` for. Left it for a dedicated `continue ENG-004` session rather
than folding it into this narrowly-scoped `watch` pass. Full reasoning on
the ticket's own log.

**Consequence:** approval cap 2/3 → 1/3 (`ENG-003` G1 only); approver-facing
WIP 2 → 1. Not spent on anything else this pass — dispatching the freed
capacity onto another ticket (e.g. raising `ENG-005`'s G1) is left for the
next `scheduled`/`watch`/`continue` pass, same restraint the preceding
`decision` pass applied to this exact situation.

**Notify sweep:** no gate item written this pass (one was consumed, none
raised) — nothing to `raise`. No nudge due: `ENG-003` was already nudged
once, 2026-08-26, and a nudge fires at most once per item. Approval cap
dropped, not filled — no stall alert.

**Dead-end sweep (scoped to `ENG-004`, the ticket this event unblocked):**
its log now ends in a valid, accounted-for state with a chain record below.
`ENG-003` (`awaiting-scope`) and `ENG-005` (`shaped`) untouched this pass —
both already correctly waiting on the approver or the next `scheduled`/`watch`
sweep, neither a dead end.

`chained: ENG-004` — sitting at `designed`, owned by `architect` (an agent,
not the approver, not blocked, not terminal). Fired
`/bin/zsh departments/engineering/lib/eng-trigger.sh continue ENG-004` for
the dedicated investigation-and-design session. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean.

## 2026-08-26 — decision: ENG-001's G3 approved — the seed ticket reaches `verified`

`decision` event pass — narrow scope per the event contract (act on the
answered gate item in `inbox/` and advance only the ticket it belongs to; no
board-wide sweep). Mode check clean (business-os `.env` → `MODE=active`).
Pre-pass `departments/engineering/lib/eng-gate-check.sh` (whole board and
`ENG-001`-scoped): exit 0, clean.

**Gate return: `ENG-001`'s G3**
(`inbox/2026-08-26-eng001-g3-verification.md`) **answered — approved**, no
additional comment, `decided: 2026-08-27T05:05:01.598404+00:00`. Per
`ADR-002`, advanced `awaiting-release → shipped → verified`, 2 transitions.
Acted as devops at `shipped`: recorded the G3 confirmation in place of a
deploy, logged on the ticket; no release record fabricated at
`agents/devops/releases/` for a deploy that never happened, per `ADR-002`'s
own instruction. Acted as product-manager at `verified`: re-confirmed all
four acceptance criteria fresh against disk (registry, worktrees, gate-check,
`ENG-002`'s own `verified` state) and re-opened all three existing receipts
(`agents/principal-engineer/reviews/ENG-001.md`,
`agents/qa/test-plans/ENG-001.md`, `agents/security/reviews/ENG-001.md`) to
confirm each still reads `pass` rather than citing the prior hop's numbers.
Full detail on the ticket's own log. Gate item moved to
`inbox/_handled/2026-08-26-eng001-g3-verification.md` unedited — the approver
filled in `## Decision` directly this time. Journaled in
`agents/eng-manager/config/decision-journal.md`.

**This closes the seed ticket.** All four acceptance criteria hold, every
lane receipt is on file and independently re-verified more than once,
`ADR-001`/`ADR-002` stay on record for the next instance's own seed ticket.
`ENG-001` is off the In-flight table, terminal.

**Consequence, not an action this pass:** approval cap drops 3/3 → 2/3
(`ENG-003`+`ENG-004` G1s only); approver-facing WIP drops 3 → 2, back at the
soft limit rather than over it. Dispatching any newly-freed capacity onto
another ticket (e.g. a G1 slot for `ENG-005`) is left for the next
`scheduled`/`watch`/`continue` pass — out of scope for a `decision` event
scoped to the one gate item it answers.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: none — verified, terminal`). Other in-flight tickets untouched.

`chained: none` — `ENG-001` is `verified`, a terminal state; the chaining
guard never re-fires a terminal ticket. Post-pass
`departments/engineering/lib/eng-gate-check.sh`: exit 0, clean (whole board).

## 2026-08-26 — watch: swept all three inboxes again, nothing new — fourth occurrence of the self-inflicted no-op pattern

`watch` (launchd) pass — drained immediately behind the `scheduled`
safety-net sweep directly above: that pass ended 15:48:00 and this one began
draining the same second, after the queue collapsed 2 duplicate `watch`
events into one (`traces/eng-loop-2026-08-26.log`). Per the event's own
narrower contract, swept only `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/`, acting on whatever is new. Mode
check clean (business-os `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` holds
exactly the three items already on the board's "Waiting on the approver"
list, and all three are exactly as the immediately-preceding `scheduled`
pass left them seconds earlier — read fresh, not trusted from the board
header: `2026-08-26-eng001-g3-verification.md` (`## Decision` blank,
raised/notified `2026-08-26T15:43:11`), `2026-08-25-eng003-g1-scope.md` and
`2026-08-25-eng004-g1-scope.md` (both `## Decision` blank, both `nudged:
2026-08-26T15:43:45`). Nothing new to act on.

**Notify sweep:** no nudge due — `ENG-001`'s G3 is minutes old; `ENG-003`/
`ENG-004` were each nudged exactly once, seconds ago, by the pass
immediately before this one, and a nudge fires at most once per item.
Approval cap unchanged at 3/3, same composition the `scheduled` pass already
reasoned about (not a fresh stall) — no new stall alert.

**Fourth occurrence of the pattern `proposals.md` already carries a full
root-cause diagnosis for** — filed as a proposal by the `watch` pass two
entries above this one (itself the third occurrence, after two
`observations.md` rows on 2026-08-25 and 2026-08-26 10:13). Mechanism
unchanged from that proposal's own account: `commit_watch_fingerprint()` in
`lib/eng-trigger.sh` only stamps `.watch-seen` on an `$EVENT=watch` pass, so
the G3 raise and the two nudges the `scheduled` pass just wrote to `inbox/`
changed the three watched inboxes' fingerprint without updating
`.watch-seen` — guaranteeing this fire would see "something changed" and
find nothing left to do, exactly as it did. Not refiled as a new proposal or
observation: a fifth data point on an already-diagnosed, already-proposed
issue is corroboration, not a new finding, and refiling it risks the
"proposal batch becomes unreadable" failure mode `schedules/eng_build_loop.md`
step 8b warns against. Left for the approver's existing G1 batch to resolve.

No ticket was touched this pass, no ticket state changed, no gate item was
written, nothing to journal. `chained: none` — this pass advanced no
ticket, so there is no hop of its own to fire, and every in-flight ticket
(`ENG-001` awaiting-release, `ENG-003`/`ENG-004` awaiting-scope, `ENG-005`
shaped) is already correctly waiting on the approver or a WIP/approval cap,
none of which a machine can clear. Approver-facing WIP unchanged (3, still
over the 2 soft limit, still harmless per the header note), approval cap
unchanged at 3/3, machine WIP unchanged at 0/6. Post-pass
`lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — scheduled: safety-net sweep — ENG-002's out-of-band merge reconciled, ENG-001's G3 raised, two G1s nudged

`scheduled` (launchd) pass — the twice-daily safety-net sweep. Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Pre-pass `lib/eng-gate-check.sh`: exit 0, clean.
Confirmed this pass's own lock (`traces/.loop.lock`, pid of this chain's
`eng-trigger.sh scheduled launchd` invocation) is legitimately its own, not a
collision.

**Business/technical intake:** `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty — nothing new to
shape or propose.

**Gate returns / merge detection, combined — `ENG-002` found already marked
`shipped` by a direct "control center" edit, ancestry not yet consulted.**
The ticket's own log said so explicitly. Independently re-ran the loop's own
merge-detection check from scratch in the department's worktree
(`~/Documents/projects/_eng/restaurant-portal`, never the human's checkout):
`git fetch origin` → `33c5de6..b3a81ef main -> origin/main`;
`git merge-base --is-ancestor chore/ENG-002-smoke-test-harness origin/main` →
merged; `git diff` between the branch tip and `origin/main` → empty (no
intervening commits on `main`). The control center's claim held up.
`inbox/2026-08-26-eng002-merge-request.md`'s `## Decision` was never actually
filled in — the approver merged directly on GitHub instead, an alternative
the item's own text offered. Treated the merge as the answer: filled the
item's Decision with what happened, moved it to `inbox/_handled/`, and
journaled it (`agents/eng-manager/config/decision-journal.md`) — flagging
that the tracked channel was bypassed, worth watching for a repeat.

**Closed out `ENG-002` (`shipped → verified`).** Acted as devops for the
`shipped` exit condition the control-center edit had skipped: confirmed
`restaurant-portal` has no push-to-`main` CI/CD (`deploy-cf` is a manual
`wrangler pages deploy` script; no `.github/workflows/`), and this ticket's
diff (`devDependency`s + test files) never reaches Vite's build graph —
re-ran `npm run build` on the merged tree and confirmed the `dist/` output is
unchanged in shape. Nothing to deploy, so `npm run deploy-cf` was
deliberately not run. Wrote the release record from what was actually found
(`agents/devops/releases/2026-08-26-restaurant-portal-ENG-002.md`). Then
acted as product-manager: re-ran `npm test` on the merged tree (1 passed),
re-checked `config/projects.md`'s Commands table on disk (present), and
updated `agents/qa/test-plans/ENG-002.md`'s AC3 from `pending` to `pass` —
all four acceptance criteria now confirmed against the live, merged thing.
Full detail on the ticket's own log. **`ENG-002` no longer counts against the
approval cap** — the third of 3/3 is now open.

**Dispatch: `ENG-001` `ready-to-ship → awaiting-release`, 1 transition.**
With the cap at 2/3 (`ENG-003`+`ENG-004` G1s only), raising `ENG-001`'s G3 —
an already-in-flight ticket reaching its own next gate, not a new start — is
legal per the Guards section, the same reasoning `ENG-002`'s own history used
at 2/3→3/3 earlier. Wrote the G3 item per `ADR-002`'s framing (confirm the
record, not "ship to production" — nothing is being deployed) at
`inbox/2026-08-26-eng001-g3-verification.md` and raised it. Approval cap is
back to 3/3 (full) — `ENG-003`, `ENG-004`, and this G3 — a different
composition than before, not a fresh stall (the board was never observed as
anything but full/near-full by any pass boundary in between, so no new stall
alert sent; one was already sent for the ongoing episode and is the known
no-op `MODE`-collision bug). Machine WIP now 0/6 — nothing left in the
`ready`..`ready-to-ship` range.

**Notify sweep — two nudges due.** `ENG-003` (notified 2026-08-25T13:55:41)
and `ENG-004` (notified 2026-08-25T14:55:55) had both crossed the 24h
threshold as of this pass (15:43 local) — the immediately-preceding passes checked
this correctly and found both still under 24h at the time; time alone closed
the gap, which is exactly what a `scheduled` safety-net sweep exists to
catch between local events. Ran `lib/eng-notify.sh nudge` on both, stamped
`nudged:` on each by hand (the script's known `MODE`-collision bug means its
own log line reads `sent: active` rather than `sent: nudge` — reproduced
here too, corroborating the existing proposal, not a new finding).

**One proposal filed** (`proposals.md`): the general gap this pass's
`ENG-002` reconciliation exposed — a ticket's `state:` can move out from
under an open gate item via the control center, and nothing currently
cross-checks the two automatically; this pass only caught it by chance while
re-deriving `ENG-002`'s status for other reasons. Sized `S` — the check
itself (for every open gate item, confirm the ticket it names is still
actually at the state the item implies) is cheap; a repeat occurrence would
make this worth acting on.

**Dead-end sweep:** every in-flight ticket's log now ends in a valid,
accounted-for state. `ENG-001` — `chained: none`, `awaiting-release`, owner
`approver`. `ENG-002` — `chained: none`, `verified`, terminal. `ENG-003`/
`ENG-004` — unchanged, waiting on the approver, both now nudged.
`ENG-005` — unchanged, `chained: none — held by the WIP cap`
(`wip.approver_limit` 2/2, `ENG-003`+`ENG-004` still open; freeing the
approval cap doesn't free this one, since it's a distinct, smaller cap that
was already full before `ENG-002` ever blocked on it). No broken chains
found; `agents/eng-manager/config/exceptions.md` empty; nothing past the
30-day proposal expiry.

Post-pass `lib/eng-gate-check.sh`: exit 0, clean (checked after each of the
`ENG-002` and `ENG-001` edits individually, and once more for the whole
board at the end).

## 2026-08-26 — watch: swept all three inboxes, nothing new to act on

`watch` (launchd) pass — fired by the file-watcher on a change to one of the
three watched inboxes. Per the event's own narrower contract, this sweeps
`agents/product-manager/inbox/`, `agents/eng-manager/inbox/` and `inbox/`
only, acting on whatever is new; the board-wide version of dispatch/merge-
detection/dead-end-sweep is the twice-daily `scheduled` pass's job, not
this one's. Mode check clean (business-os `.env` → `MODE=active`). Pre-pass
`lib/eng-gate-check.sh`: exit 0, clean.

**Swept all three inboxes; found nothing unprocessed.**
`agents/product-manager/inbox/` and `agents/eng-manager/inbox/` are both
empty (`.gitkeep` only); `inbox/requests/` is empty too. `inbox/` itself
holds exactly the three items already on the board's "Waiting on the
approver" list, and all three still read `## Decision` / "Filled in by the
approver," unanswered — `2026-08-26-eng002-merge-request.md`,
`2026-08-25-eng003-g1-scope.md`, `2026-08-25-eng004-g1-scope.md`. The
merge-request file is the one genuinely new artifact since the last board
entry (written 11:01 by the immediately-preceding `continue ENG-002`
pass), but that same pass had already raised it (`notified:
2026-08-26T11:01:46`) and reflected it on the board — nothing was left
unprocessed for this pass to act on. Cross-checked against
`traces/.watch-seen` (fingerprint last stamped 10:20, before the file's
11:01 creation) and `traces/eng-loop-2026-08-26.log`: this `watch` fire is
that same write being independently observed by the file-watcher, not a
second, unhandled change — consistent with the fingerprint changing and
the fire not being deduplicated above the lock.

**Notify sweep:** neither `ENG-003` nor `ENG-004`'s G1 has crossed the 24h
nudge threshold (notified 2026-08-25T13:55:41 / T14:55:55, both still under
24h as of this pass). The approval cap reached 3/3 (full) during the
immediately-preceding `continue ENG-002` pass and no stall alert had been
sent for that stall, so ran `lib/eng-notify.sh stall` per step 7 — it is
still the known-broken no-op filed 2026-08-25 (`proposals.md` row 2, the
`MODE`-variable collision with the sourced business-os `.env`): logged
`no such item:` and sent nothing. Corroborating evidence for the existing
proposal, not a new finding.

**Merge detection, board-wide dispatch, and the full dead-end sweep are out
of scope for this event** — `watch` only unblocks the inbox sweep above.
Spot-checked only what bears on the one new file: `ENG-001`'s own
`continue` chain, fired by its own immediately-preceding pass, is intact
and queued at the front of `traces/.pending`, unaffected by this pass.

**One proposal filed** (`proposals.md`): this is the third occurrence of
the no-op-`watch` pattern `observations.md` flagged twice already
(2026-08-25, 2026-08-26 10:13) and explicitly deferred to a proposal "if it
recurs." Traced the actual mechanism this time, in `lib/eng-trigger.sh`:
`commit_watch_fingerprint()` and the `WATCH_FP` capture both key off
`$EVENT = "watch"` specifically, so a gate item raised by a `continue` or
`scheduled` pass changes the watched inboxes' fingerprint but never updates
`.watch-seen` — guaranteeing the next `watch` fire sees "something changed"
and spends a full pass finding nothing, exactly what happened here
(`.watch-seen` stamped 10:20; `continue ENG-002` raised its merge request
at 11:01; this pass is the predictable result). Not fixed inline — it's
department machinery, self-discovered, so `schedules/eng_build_loop.md`
step 3 routes it to the proposal list, not a drive-by patch.

No ticket was touched this pass, no ticket state changed, no gate item was
written, nothing to journal. `chained: none` — this pass advanced no
ticket, so there is no hop of its own to fire; `ENG-001`'s separately-queued
`continue` (from its own prior pass) runs next regardless, once this pass
exits. Approver-facing WIP unchanged (3, still over the 2 soft limit, still
harmless per the header note), approval cap unchanged at 3/3, machine WIP
unchanged at 1/6. Post-pass `lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — continue ENG-001: ADR-002 resolved the release/G3 question, reached ready-to-ship, held there by the approval cap

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh`
(whole board and `ENG-001`-scoped): exit 0, clean. Fresh sweep of all three
inboxes found nothing pending for `ENG-001`.

**Resolved the boundary the immediately-preceding pass named and stopped
at.** That pass reached `in-security` with a **pass** verdict already on
record, but declined to guess what `ready-to-ship`/`awaiting-release`/
`shipped` mean for a no-deploy verification ticket, since `ADR-001`'s
Decision text names `building` through `in-security` specifically and never
further. Acting as architect, wrote `ADR-002`
(`agents/architect/decisions/ADR-002-verification-ticket-release-and-g3.md`):
a verification ticket owes every remaining full-lane state exactly as any
other ticket — `ready-to-ship`, G3, `shipped`, and `verified` are none of
them skipped or auto-routed by inventing an autonomy level `aiorders` was
never granted (re-confirmed fresh: `config/projects.md` still only the five
app repos at **L1**, `config/internal-projects` still empty). Only the
*content* of each state changes, continuing `ADR-001`'s own pattern —
`ready-to-ship` records devops confirming nothing to release; G3 asks the
approver to confirm the ticket's record rather than approve a deploy that
doesn't exist; `shipped` records that confirmation, not a fabricated
release. G3 is deliberately **not** waived or downgraded to L3's
notify-after treatment: `docs/engineering-team.md` reserves "say yes to
production" to the approver, department-wide, and unlike `building`'s empty
`branch:` field, removing a human checkpoint isn't a reversible logging
convention — see the ADR's own reasoning for why this isn't the same kind of
call `ADR-001` made. No G2 raised. `agents/architect/decisions/_index.md`
updated, Next ID now `ADR-003`.

**Dispatch: `in-security → ready-to-ship`, 1 transition.** Acted as devops
per `ADR-002`: confirmed and logged, not skipped, that no release plan,
rollback, or observability plan exists because no registered project carries
a diff for this ticket — re-verified `config/projects.md` (five rows, all
L1) and `_eng/` (all five worktrees present) fresh rather than citing the
`in-security` hop's numbers. Release window checked for consistency with
today's `ENG-002` hop even though nothing deploys: Wednesday, no
`ENG_RELEASE_FREEZE` — clean, moot either way.

**Not proceeding into `awaiting-release`.** The approval cap is **3/3
(full)** — re-checked fresh, not from this board's cached header:
`inbox/2026-08-26-eng002-merge-request.md`,
`inbox/2026-08-25-eng003-g1-scope.md`, and
`inbox/2026-08-25-eng004-g1-scope.md` all still read "Filled in by the
approver.", unanswered, and `config/config.yaml` confirms `wip.approval_cap:
3` rather than assuming the board header is current. Per the Guards section,
"at the cap, nothing advances into a gate state" — `awaiting-release` is
exactly that, so the G3 item `ADR-002` calls for is not raised this pass.

**`chained: none` — held by the approval cap (3/3, full), not by anything
left for this ticket to decide.** Unlike every earlier stop on this ticket,
this one isn't an undecided question a fresh pass could resolve: all four
acceptance criteria are satisfied, `ADR-002` has settled what every
remaining state means, and devops's own confirmation is done. Nothing
machine-ownable remains until a slot frees. Re-firing `continue ENG-001` now
would only re-derive this same conclusion at the cost of a full pass — the
chaining guard's own list names this condition directly ("held by a cap
(WIP or approvals)"). Resumes at the next `scheduled` safety-net sweep, or a
direct re-fire once the approver clears one of the other three open items.

No gate item raised this pass; nothing to notify. Machine WIP unchanged at
1/6 (`ready-to-ship` is still inside the counted `ready`..`ready-to-ship`
range). Approval cap unchanged at 3/3 — this pass created no new gate item.
**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: none`, reason given). Other in-flight tickets untouched. Post-pass
`lib/eng-gate-check.sh`: exit 0, unchanged.

## 2026-08-26 — continue ENG-001: combined review+quality+security hop, stopped short of ready-to-ship

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Pre-pass `lib/eng-gate-check.sh`: exit 0, clean.
Fresh sweep of all three inboxes found nothing pending for `ENG-001`.

**Dispatch: `building → in-review → in-security`, 2 transitions.** Acted as
principal-engineer and qa on the combined review+quality hop (step 6):
independently re-derived all four acceptance criteria against disk this
round rather than citing prior numbers — `config/projects.md` (AC1),
`_eng/` worktrees plus `git rev-parse` in each to confirm they're real,
resolvable checkouts (AC2), a fresh `lib/eng-gate-check.sh` run (AC3), and
`ENG-002`'s own board file, now at `blocked` with an open PR — several
states past AC4's literal bar (AC4). Verdict **pass**;
`agents/principal-engineer/reviews/ENG-001.md` and
`agents/qa/test-plans/ENG-001.md` written, `links.review`/`links.test_plan`
set. Acted as security: threat model, full OWASP walk (all ten `n/a` — no
code, dependency, endpoint, or config surface exists), secret-scanned this
ticket's entire paper trail (one prose hit, not a credential). Verdict
**pass**; `agents/security/reviews/ENG-001.md` written, `links.security_review`
set. Full detail on the ticket's own log.

**Not proceeding into `ready-to-ship`, for two independent reasons.** What
`ready-to-ship`/`awaiting-release`/`shipped` mean for a no-deploy
verification ticket is a real open question `ADR-001` does not cover — its
Decision text names `building` through `in-security` specifically, never
further, and the design doc's brief Rollout note was never weighed as a
considered decision the way the ADR was. Improvising it here would repeat
the exact failure this ticket exists to prevent. Independently: the
approval cap is **3/3 (full)** right now — checked fresh this pass by reading each
of the three open items' `## Decision` sections directly (all still "Filled
in by the approver," unanswered) rather than trusted from this board's own
cached header — so reaching `awaiting-release` (a G3 this pseudo-project
cannot auto-route, being registered at no autonomy level) could not be
acted on regardless.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: ENG-001`). Other in-flight tickets untouched — out of scope for a
`continue` event naming one ticket.

No gate item raised this pass; nothing to notify. Machine WIP unchanged at
1/6 (`in-security` is still inside the `ready`..`ready-to-ship` counted
range). Approval cap unchanged at 3/3 — this pass created no new gate item.
`chained: ENG-001` — sitting at `in-security`, owned by security (agent, not
approver, not blocked, not terminal); the full cap blocks the *next* hop's
gate, not this ticket's present state.

## 2026-08-26 — continue ENG-002: building finished, all three machine gates passed, PR open

`continue ENG-002` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Confirmed via
the trigger log this is exactly the dedicated continuation the safety-net
sweep directly below deferred, not a duplicate: that pass ended 10:44:34 and
this one began draining immediately after. Mode check clean (business-os
`.env` → `MODE=active`). Pre-pass `lib/eng-gate-check.sh` (whole board and
`ENG-002` scoped): exit 0, clean.

**`building → in-review → in-security → ready-to-ship → blocked`, 4
transitions (the per-ticket cap), landing exactly on the human gate.** Did
not take the prior pass's "self-tested" claim on faith: independently re-ran
`npm test` (1 passed), `npm run lint` (96 problems, identical on a clean
`origin/main` checkout via `git stash -u` — zero new), `npm run build`
(succeeds), and `npm audit` (37 vs. 39 on `main` — no new vulnerabilities);
traced the test's Supabase mock and its "Login" tab landmark through the
actual component chain rather than trusting the description. Committed the
five relevant files as `2703add`, pushed the branch. Acted as
principal-engineer (review pass, `agents/principal-engineer/reviews/ENG-002.md`)
and qa (wrote the test plan this ticket never had, `agents/qa/test-plans/ENG-002.md`,
suite green) on the combined review+quality hop; acted as security
(`agents/security/reviews/ENG-002.md`, OWASP walk mostly `n/a` for a dev-only
harness, dependency check clean); acted as devops at `ready-to-ship`
(upstream gates verified on disk, readiness held, `config/projects.md`'s
Commands table updated per the design's own assignment, window check clean —
Wednesday, no freeze). Opened the real PR
(https://github.com/harsimranwalia/restaurant-portal/pull/1) since
`restaurant-portal` is **L1**, wrote and raised the merge-request item
(`inbox/2026-08-26-eng002-merge-request.md`), landed at `blocked`,
`blocked_on: approver`. Full detail, including the approval-cap arithmetic
that justified proceeding while the board was already at 2/3, on the
ticket's own log.

**Approval cap now 3/3 (full)** — checked `config/config.yaml`'s actual
`wip.approver_limit`/`wip.awaiting_approver_cap` definitions rather than the
board header's prose: `approver_limit`'s only enforcement is blocking *new*
starts (already true at 2, still true at 3), and `awaiting_approver_cap` —
the guard `config.yaml` names explicitly for "an L1 PR waiting to be
merged" — had exactly one slot free. Machine WIP now 1/6 (`ENG-001` only).

This pass's own `lib/eng-notify.sh raise` call reproduced the already-filed
`MODE`-collision bug (`sent: active`, not `sent: raise`) — corroborating
evidence for the open 2026-08-25 proposal, not a new one.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-002`'s log now ends `chained: none` with the waiting-on-
approver reason. Other in-flight tickets untouched.

`chained: none` — `ENG-002` is `blocked`, `blocked_on: approver`. The whole
point of this hop was to reach that gate; nothing left for a machine to do
until the approver merges the PR or replies to the inbox item.

## 2026-08-26 — scheduled: safety-net sweep, board already mid-chain — nothing to dispatch

`scheduled` (launchd) pass. Mode check clean (business-os `.env` →
`MODE=active`; instance `config.yaml` → `mode:` empty, falls through).
Pre-pass `lib/eng-gate-check.sh`: exit 0, no violations.

Business intake: `agents/product-manager/inbox/`, `agents/eng-manager/inbox/`
and `inbox/requests/` all empty — nothing new to shape or propose. Gate
returns: `ENG-003`/`ENG-004` G1s both still unanswered (`## Decision` blank
in both; notified 2026-08-25T13:55:41/T14:55:55, still under 24h as of this
pass [10:41] — no nudge due). Merge detection: no ticket `blocked` on an L1
PR, no-op.

**Dispatch — reviewed all five in-flight tickets, advanced none.** `ENG-001`
and `ENG-002` are both already mid-chain from the two dedicated `continue`
passes that ran in the hour before this one (`ENG-001` `ready→building` at
10:20–10:33; `ENG-002`'s uncommitted `building` work found and corrected at
09:56). Each ticket's own chain is already queued: `cat traces/.pending`
shows `continue ENG-002` then `continue ENG-001`, both appended by those
passes themselves, not by this one. Re-firing either here would duplicate an
already-queued line and, since this pass's own parent `eng-trigger.sh
scheduled launchd` (pid 37779, alive since 09:30) holds `traces/.loop.lock`
throughout, would contend a lock its own ancestor holds — the exact
situation two earlier passes today already hit and correctly avoided. Left
both untouched. `ENG-003`/`ENG-004` stay `awaiting-scope` — approver WIP
2/2 (full), both G1s unanswered. `ENG-005` stays `shaped`, held by the same
cap — no slot freed this pass.

**Notify sweep:** no gate item raised this pass, nothing to notify; neither
`ENG-003` nor `ENG-004` has crossed the 24h nudge threshold yet; approval cap
is 2/3, not full, so no stall alert.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`); no
broken chain. `agents/eng-manager/config/exceptions.md` is empty (nothing at
a third occurrence); `proposals.md`'s three open items and
`observations.md`'s ledger are all within days of filing, none past the
30-day proposal expiry.

Approver-facing WIP unchanged at 2/2 (full), approval cap 2/3, machine WIP
unchanged at 2/6. `chained: none` on all five tickets — `ENG-001`/`ENG-002`
because a dedicated continuation is already queued for each (see above);
`ENG-003`/`ENG-004` because they wait on the approver; `ENG-005` because it's
held by the approver-WIP cap. Post-pass `lib/eng-gate-check.sh`: exit 0,
unchanged.

## 2026-08-26 — continue ENG-001: building-as-verification record written

`continue ENG-001` event pass — narrow scope per the event contract (resume
the named ticket from its current state; no board-wide sweep). Mode check
clean (business-os `.env` → `MODE=active`; instance `config.yaml` → `mode:`
empty, falls through). Confirmed no pending gate item for `ENG-001` in any of
the three inboxes before dispatching — none exists; its last judgement call
(what `building`/receipts mean for a diffless ticket) was decided directly by
the architect via ADR-001, no approver gate raised. Merge detection:
`ENG-001` carries no branch, no-op.

**Dispatch:** `ENG-001` advanced `ready → building` — the
building-as-verification-record step ADR-001 defines. Re-verified all four
acceptance criteria against disk rather than trusting prior citations: AC1
(`config/projects.md`, five rows, all **L1**), AC2 (`_eng/` worktrees, all
five present), AC3 (`lib/eng-gate-check.sh` re-run, exit 0), AC4 (`ENG-002`
now at `building`, already past `shaped`). Full citations on the ticket's
own log. `branch:` stays empty per ADR-001; `machine_wip` (6) unchanged at
2/6 (`ENG-001`, `ENG-002` — both already inside the counted range). **Not
proceeding into `in-review` this pass, deliberately** — the
principal-engineer/QA review of the verification claims is real, distinct
gate work reserved for its own session, same reasoning applied at every
earlier hop on this ticket. `chained: ENG-001`.

**Dead-end sweep (scoped to this ticket, per the event's own narrower
contract):** `ENG-001`'s log now ends in a valid, accounted-for state
(`chained: ENG-001`). Other in-flight tickets untouched — out of scope for a
`continue` event naming one ticket.

No gate item raised this pass; nothing to notify; nothing new to observe or
propose.

## 2026-08-26 — scheduled: safety-net sweep, ENG-002's building state corrected

`scheduled` (launchd) pass — twice-daily safety-net sweep, drained
immediately behind this morning's `continue ENG-002` build hop under the
same lock (pid 37779, 09:30 launchd fire). Mode check clean (business-os
`.env` → `MODE=active`; this instance's own `config.yaml` → `mode:` empty,
falls through). Business intake: `agents/product-manager/inbox/`,
`agents/eng-manager/inbox/` and `inbox/requests/` all empty — nothing new to
shape or propose. Gate returns: `ENG-003`/`ENG-004` G1s both still
unanswered (`## Decision` blank in both inbox items; notified
2026-08-25T13:55/14:55, both under 24h as of this pass — no nudge due yet).
Merge detection: no ticket `blocked` on an L1 PR, no-op.

**Dispatch (priority order `now` → empty):** `ENG-001` reviewed and left
unchanged — still `ready`, its `continue` already queued
(`traces/.pending`) from an earlier pass, nothing to redo. `ENG-002`
reviewed and found mid-flight: the `continue ENG-002` hop that ran
09:36–09:56 just before this pass implemented the smoke test for real
(Vitest + RTL, per the architect's design) but stopped itself uncommitted,
citing a suspected concurrent instance of this automation — which this pass
independently re-checked via `ps` and the lock file and found to be false
(pid 37779 is this exact chain's own orchestrator; no other process
touches this instance or the `restaurant-portal` worktree). Full forensics
on that ticket's own log. Corrected the board to `state: building` and
`branch: chore/ENG-002-smoke-test-harness` to match the real, verified,
on-disk work; left the worktree exactly as found per `config/projects.md`'s
own rule against touching a previous pass's uncommitted state; filed the
`.env`-tracked finding that pass discovered but didn't get to
(`proposals.md`); did not commit/push/finish the build myself — that stays
reserved for a dedicated `continue` session, same reasoning already applied
to every other `ready`→`building` transition on this board. `ENG-003`/
`ENG-004` stay `awaiting-scope` (approver WIP 2/2, both gates unanswered);
`ENG-005` stays `shaped`, held by the same cap — no slot freed this pass.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`) —
`ENG-002`'s is the one this pass brought current; `ENG-001`, `ENG-003`,
`ENG-004`, `ENG-005` were already correct and untouched. One observation
filed (`observations.md`): a second occurrence of the `scheduled`-event-
with-a-ticket-path-context oddity first seen 2026-08-25, with a correction
to that earlier note — it does charge a ticket's hop counter (`ENG-001`
this time), not ticket-less as previously assumed.

Approver-facing WIP unchanged at 2/2 (full), approval cap 2/3, machine WIP
unchanged at 2/6. `chained: ENG-002` (fired `/bin/zsh eng-trigger.sh
continue ENG-002` — queued behind this pass's own lock, next drain runs
it). `ENG-001`/`ENG-003`/`ENG-004`/`ENG-005`: `chained: none`, all for
reasons unchanged from their own last log entries.

## 2026-08-25 — continue ENG-001: architect resolved the building/receipts gap

`continue ENG-001` pass — the dedicated hop chained by the earlier PM-shaping
pass; the intervening `scheduled (manual-unblock)` sweep and its retry (both
below/archived) deliberately left this ticket alone because this `continue`
was already queued for it.

Architect resolved the question the PM pass raised: what `building` and the
three full-lane receipts mean for a ticket with no application-code
deliverable. Wrote `ADR-001`
(`agents/architect/decisions/ADR-001-verification-ticket-building-and-receipts.md`)
and a short tech design
(`agents/architect/designs/ENG-001-register-repos-and-prove-the-loop.md`): a
**verification ticket** — every acceptance criterion satisfied with no diff
in any registered project — still owes every state and every receipt its
lane specifies, but `building` records what was checked instead of a
branch/PR. Considered and rejected registering `aiorders` in
`config/internal-projects` (reserved to the approver by that file's own
header, and premature for what's expected to be a one-time ticket) and
delegating via `parent:` to `ENG-002` (would misrepresent its real,
independent provenance). No one-way door; decided directly, no G2, no
approver touch — `ENG-003`/`ENG-004` keep both approver-WIP slots
undisturbed.

**Dispatch:** `ENG-001` advanced `shaped → designed → ready`. EM work
breakdown found zero implementation units (no code in any registered
project), so nothing to sequence; `machine_wip` (6) now 2/6 (`ENG-002`,
`ENG-001`). **Stopped before `building`, deliberately** — writing the three
receipts against the verification evidence is real, distinct gate work that
`schedules/eng_build_loop.md` reserves for its own session, same reasoning as
`ENG-002` earlier today. `chained: ENG-001`.

**Merge detection:** no ticket is `blocked` on an L1 PR. No-op.

**Dead-end sweep:** every in-flight ticket's log ends in a valid,
accounted-for state (`chained: <id>` or `chained: none — <reason>`); no
broken chain found.

## 2026-08-25 — scheduled (manual-unblock), retry: ENG-002 gate processed, ENG-004 G1 raised

**This pass is the retry (attempt 2/2) of the `scheduled (manual-unblock)`
event below** — the first attempt timed out at the 1800s pass ceiling while
finishing the board-index edit for the entry directly below this one (see
`traces/eng-loop-2026-08-25.log`: `pass TIMED OUT after 1800s`, re-queued as
attempt 2/2). Before doing anything new, verified the first attempt's
substantive work — `ENG-003`/`ENG-004`/`ENG-005` shaped, `ENG-003`'s G1
raised, two proposals and three observations filed — was complete and
internally consistent on disk; the only gap found was this table missing rows
for the three new tickets, now fixed. Filed one further observation on the
timeout itself (`agents/eng-manager/observations.md`).

**Gate returns:** `ENG-002`'s G1 was answered — **approved**, no additional
comment — while this retry was starting (`decided: 2026-08-25T21:43:57Z`).
Processed it: gate item moved to `inbox/_handled/`, PRD `status: approved`,
entry added to `agents/eng-manager/config/decision-journal.md`. A dedicated
`decision 2026-08-25-eng002-g1-scope.md` event is separately queued
(`traces/.pending`) from the control center's own fire — when it eventually
drains it will find the gate already resolved and be a harmless no-op.
`ENG-003`'s G1 remains unanswered; left as-is.

**Dispatch:** `ENG-001` left alone, same reasoning as the pass below — its
`continue` is still independently queued (`traces/.pending`), so re-opening
the architect's deferred judgement call here would race a pass already
in flight for it. `ENG-002` advanced `awaiting-scope → designed → ready`:
architect design written
(`agents/architect/designs/ENG-002-restaurant-portal-smoke-test-harness.md`
— Vitest + React Testing Library, one smoke test on the real app entry
point; no one-way door, no ADR, no G2); EM sequencing found a single unit of
work and `machine_wip` (6) at 0/6 going in. **Stopped before `building`,
deliberately** — this pass is a recovery/sweep context, not the clean session
`schedules/eng_build_loop.md` reserves for "an engineer writing code," so the
actual implementation is left for a dedicated `continue` hop. `chained:
ENG-002`.

Resolving `ENG-002`'s gate freed the `wip.approver_limit` (2) slot it had
been holding alongside `ENG-003`. Took the freed slot for `ENG-004` over
`ENG-005` — both still `shaped` with no `priority` set, so severity is the
tie-break (`P2` vs `P3`), per `config/definition-of-done.md`. `ENG-004`'s G1
raised and notified; PRD `status: awaiting-scope`. `ENG-005` holds at
`shaped` — approver WIP is 2/2 (full) again with `ENG-003` + `ENG-004`.

**Merge detection:** no ticket is `blocked` on an L1 PR. No-op.

**Dead-end sweep:** every in-flight ticket's log ends in a valid, accounted-for
state (`chained: <id>` or `chained: none — <reason>`); no broken chain found.

## 2026-08-25 — scheduled (manual-unblock), attempt 1: swept the three unshaped requests

`scheduled (manual-unblock)` pass — the safety-net sweep queued behind the
`continue ENG-001` pass earlier today. Per the event's own scope ("sweep the
whole board: everything a local event cannot see"), left `ENG-001` alone —
its `continue` was already queued (`traces/.pending`) from that earlier
pass's own chain, so redoing its architect-judgement question here would
have raced a pass already in flight for it. Confirmed nothing is `blocked`
on an L1 PR (merge detection: no-op this pass) and no ticket's chain
silently broke (`ENG-001`'s and `ENG-002`'s logs both end in a valid,
accounted-for state).

Business intake: found and shaped all three approver-filed requests that had
sat unprocessed in `inbox/requests/` since 2026-08-23 (flagged as an
observation by the prior pass). Ran the full request-readback on each — this
PM's reading plus a blind architect reading via an independent subagent per
request, so the second reading genuinely couldn't see the first. No material
divergence on any of the three; all three architect readings sharpened the
technical picture without disagreeing on scope or problem — see each
ticket's PRD.

- **ENG-003** (`aiorders-env-hygiene`, `config-site-builder`, size M, P2) —
  shaped straight through to `awaiting-scope`. `wip.approver_limit` (2) had
  exactly one free slot (`ENG-002` held the other); this one took it, on
  severity grounds — an ongoing, possibly-live cost exposure (an
  unrestricted Google Maps key) outranks the other two's own "nothing here
  is urgent" framing. G1 raised and notified.
- **ENG-004** (`admin-hub-migration-history`, `aiorders-admin-hub`, size L,
  P2) — shaped to `shaped`, PRD complete, G1 held for the next free slot.
- **ENG-005** (`a4-poster-generator-decision`, `aiorders-admin-hub`, size S,
  P3) — shaped to `shaped`, PRD complete, G1 held for the next free slot. G1
  will be required despite `S`+`chore` auto-skip eligibility — the ticket's
  scope is an unresolved approver decision, not routine work; see its own
  log.

All three source requests moved to `inbox/_handled/`. Two items filed rather
than fixed: a proposal (`agents/eng-manager/proposals.md`) that
`lib/eng-notify.sh` has two real bugs — no channel dispatch (posts to Slack
regardless of this instance's `approver.notify: telegram`), and a `MODE`
variable collision with the sourced business-os `.env` that silently breaks
the `stall` alert and the `nudge` prefix (confirmed live: this pass's own
`raise` call logged `sent: active`, not `sent: raise`); and two observations
(`agents/eng-manager/observations.md`) — a ticket-schema gap (`project:`/
`branch:` are singular, `ENG-003` genuinely spans three repos) and a
registry gap (`config/projects.md` doesn't record which Supabase project
`aiorders-admin-hub` is linked to, which `ENG-004` needs to answer).

Approver-facing WIP now 2/2 (full), approval cap 2/3. `chained: none` on all
three new tickets — `ENG-003` waits on the approver, `ENG-004`/`ENG-005`
wait on a WIP slot freeing; see each ticket's log for the reasoning.

## 2026-08-25 — continue ENG-001: PM shaping + ENG-002 opened

`continue ENG-001` pass. Shaped `ENG-001` (`intake → shaped`): wrote its PRD,
re-confirmed AC1 (five repos registered at L1, approved 2026-07-28,
re-verified 2026-08-23), AC2 (all five worktrees present under `_eng/`), and
AC3 (`lib/eng-gate-check.sh` exit 0) as already satisfied.  `type: chore`
auto-skips G1, so no gate item for `ENG-001` itself.

AC4 (one real ticket to `shaped`) was still open. Found a genuine, already-filed
approver request sitting unprocessed in `inbox/requests/` since 2026-08-23
(`2026-08-23-test-harness.md`) — not a self-originated finding, so shaping it
didn't touch the department's-own-work rule (`schedules/eng_build_loop.md`
step 3). Ran the full request-readback on it (this PM's reading + a blind
architect reading, no material divergence) and shaped it into `ENG-002`
(`intake → shaped → awaiting-scope`) — a smoke-test harness for
`restaurant-portal`, since none of the five AIOrders repos has a single test
and the QA gate is currently unable to prove anything ran. `size: M`, so
(unlike `ENG-001`) **G1 is required** — item raised and notified, see
"Waiting on the approver" above. `ENG-001`'s AC4 is satisfied by `ENG-002`
having reached `shaped` en route to `awaiting-scope`.

Did not push `ENG-001` past `shaped` this pass — what "building" means for a
ticket with no application-code deliverable (config/registry verification,
another ticket) isn't addressed anywhere in the department's docs, and a
snap judgement call on that shouldn't be buried in a PM pass. Left for the
architect on the next `continue`. `chained: ENG-001`.

Two things filed rather than fixed in this pass: a proposal
(`agents/eng-manager/proposals.md`) noting `agents/critic/agent.md` doesn't
exist on this instance or the department template, though
`skills/prd-writer/SKILL.md` step 8b calls for it before every G1 (ENG-002's
G1 went out with no `## Dissent` as a result); and an observation
(`agents/eng-manager/observations.md`) that three other approver requests in
`inbox/requests/` (`a4-poster-generator-unwired`, `admin-hub-migration-history`,
`aiorders-env-hygiene`) are still unshaped, out of scope for this
ticket-scoped pass. The `scheduled manual-unblock` event already queued
behind this one should sweep them.

## 2026-08-24 — decision: gate-check-unavailable resolved

Acted on the answered incident gate `2026-08-24-eng-gate-check-unavailable.md`
(`gate: incident`, tied to ENG-001 because it was the ticket in flight when the
pre-pass check found `lib/eng-gate-check.sh` unreadable). Its `project: life-os`
was stale — a leftover of the pre-carve-out hardcoding bug fixed in business-os
`ed8dd56`/`58ae148`/`9366b84`; `ticket: ENG-001` was correct. Approver had
already recorded `decision: approved`. Independently re-ran
`lib/eng-gate-check.sh` against this instance this pass: exit 0, clean — ENG-001
AC3 satisfied. Logged on ENG-001, moved the gate item to `inbox/_handled/`.
Did not shape ENG-001 further — a decision pass is scoped to the gate it
answers, not PM intake work — so `chained: ENG-001` to hand the ticket to a
fresh `continue` pass.
