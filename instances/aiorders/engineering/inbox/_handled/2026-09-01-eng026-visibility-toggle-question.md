---
type: eng-decision
agent: product-manager
gate: intake-question
project: restaurant-marketplace
ticket: ENG-026
recommendation: Answer to unblock shaping. Does not block anything currently in flight — answer when convenient.
raised: 2026-09-01
notified: 2026-09-01T10:03:26
nudged: 2026-09-02T15:37:50
decision: approved
decided: 2026-09-03T00:58:19.957907+00:00
---

# One thing before ENG-026 gets shaped further — is a channel-visibility toggle part of this?

**Context.** A new request arrived (via control-center) titled "on the brand
portal i want option to make the restaurant visible on order food, dine in
and catering separately," with a body specifying three enhancements:
operational time-clocks/cutoffs, consumer-facing filters for dine-in/
catering, and a promo-badge overlay — plus internal admin-form fields for
the first two.

**Why this is a question rather than an automatic shape.** Both the PM's own
reading and an independent, blind architect reading (raw request only, no
repo access, not shown the PM's reading) converged on the same gap without
being asked to look for it: none of the three body tasks actually adds a
per-channel on/off visibility toggle — the thing the title itself literally
asks for. Two careful readers landing on the same "the title and the body
don't match" finding is exactly the ambiguity this department's readback
process exists to catch before anything gets built from it.

**You said** (this ticket's own title): "i want option to make the
restaurant visible on order food, dine in and catering separately"

**But the body's three tasks** (operational time-clocks, smart filters,
promo badges) never add a per-channel on/off visibility toggle anywhere.

**Reading A:** the three body tasks are the whole ask — the title described
the goal loosely (a restaurant "being visible" for ordering, dine-in, and
catering distinctly, in the sense of having distinct hours/filters/promos
for each), not a literal missing toggle field.

**Reading B:** a real, independent per-channel visibility toggle is also
wanted, as a fourth piece alongside the three body tasks — e.g. a restaurant
could turn off "dine-in" on FoodSwipe entirely while keeping "order food" on.

**Which?**

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-09-03T00:58:19.957907+00:00

ENG-026 Scope Clarification: Channel Visibility, Toggles, and Open Now Filters

Team,

We have resolved the ambiguity regarding channel visibility across the Brand Portal, Admin, and consumer apps. The scope for ENG-026 is confirmed as follows:

1. MASTER CAPABILITY TOGGLES (SCHEMA, ADMIN & BRAND PORTAL)
Visibility must be driven by what services a restaurant actually offers, not operating hours alone.

* Add per-merchant boolean fields: has_order_food (default: true), has_dine_in (default: false), and has_catering (default: false).
* In the Brand Portal and Admin, channel-specific settings (operating hours, cutoffs, advance-notice rules) should only be visible/editable when that channel's master toggle is set to true.

2. CONSUMER DISCOVERY (CAPABILITY-BASED BY DEFAULT)

* Channel tabs or filters (Order Food, Dine-In, Catering) must display all merchants where the corresponding toggle is true.
* Do NOT automatically hide closed restaurants. Discovery stays wide by default so consumers can view menus or plan pre-orders.
* Merchants that are currently closed or past their order cutoff should still appear, marked with their current status (for example: Closed - Pre-order for tomorrow, or Opens at 5 PM).

3. "OPEN NOW" USER FILTER (OPT-IN ONLY)

* "Open Now" must be an explicit, optional filter chip selected manually by the user (default: off).
* Only filter out closed restaurants when the user explicitly checks or enables "Open Now".

4. API QUERY LOGIC

* Base filter: WHERE has_[channel] = true
* If open_now = true: evaluate operating hours and cutoffs for that channel against the current timestamp and exclude closed locations.
* If open_now = false (default): return all merchants where has_[channel] = true regardless of current open/closed status.

---

**Processed 2026-09-02**, `watch` event pass (context `launchd`) — read as an
approver-authored spec confirming Reading B, not a bare pick between the two
offered readings. Scoped down from the original four-capability request to
just this piece (the only one the answer actually specifies); the other
three (operational status engine, smart filters, promo badges) named as
deferred follow-on work in the ticket's own PRD rather than folded in or
dropped. PRD written
(`agents/product-manager/specs/ENG-026-foodswipe-channel-visibility.md`),
ticket moved `intake → shaped → awaiting-scope`, G1 raised
(`inbox/2026-09-02-eng026-g1-scope.md`). Journaled in
`agents/eng-manager/config/decision-journal.md`. Full trace: `ENG-026`'s own
board file.
