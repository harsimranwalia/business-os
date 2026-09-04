# 2026-09-03 — ENG-016 Piece 1, design pass

Design: `agents/architect/designs/ENG-016-catering-quote-generator.md`.
ADRs: `ADR-008` (fulfillment values), `ADR-009` (enablement gate).
The design carries the Alternatives, Risks and Out-of-scope reasoning; this is
process, dead ends, and the things that don't have a home in the template.

## Where the handed-over research was wrong, and how

The pass that dispatched this design supplied a full evidence packet and asked
for it to be checked rather than trusted. Four corrections came out of reading
`origin/main` directly, three of which changed the design.

- **`catering-request`'s required-field validation is dead for the path this
  ticket changes.** The branch is `if (source == "form" && …)`;
  `config-site-builder`'s form sends `source: 'website'`, and the only caller in
  the repos that sends `'form'` is `restaurant-marketplace`, which never calls
  this function at all — it does its own direct insert. So AC-11 was never going
  to be satisfiable server-side on this path, and the branch is best left
  untouched (AC-10 then holds regardless of what GoHighLevel sends, which is not
  determinable from the repo). This reframed AC-11 as entirely client-side.
- **The insert omits `status` and relies on a column default.** Confirmed in
  `restaurant-marketplace/README.md` (`status (text, default: 'New Enquiry')`),
  which is the only place the untracked `catering` table's DDL is documented at
  all. AC-7 therefore needs an explicit `status` on the insert, not a database
  change — and, because the endpoint is unauthenticated, that status must be
  derived server-side rather than accepted from the body.
- **`restaurant-portal` already has an owner-facing editor for
  `restaurant_website.catering`** (Website → Catering tab). The research
  packet — and the PRD, which described the `EDITABLE_PAGES` pattern as existing
  while "the shape and editor don't" — treated this surface as absent. It is
  live, and its existence is the single fact that flipped the enablement gate
  from default-on to default-off (ADR-009): a default-off toggle only ships dark
  if nobody can turn it on.
- **The board doesn't need a layout change.** The PRD's risk ("five columns
  becoming seven is a board-layout change, not just a string addition") reads
  worse than it is: `CateringKanban` is `flex overflow-x-auto` with fixed-width
  columns and already scrolls. What is real, and what the PRD didn't have, is
  that `columns` is also the render filter — a status outside it is invisible —
  and that `statusConfig[status].borderColor` is an unguarded dereference. The
  risk is deploy ordering and paired edits, not CSS.

Minor: the packet said `interface CateringRequest` is duplicated in 9 files; it
is 8 (`git grep -ln` over `origin/main`). Twelve status-string literals across 8
files, not one per file.

## Two dead ends worth remembering

**A `restaurants.catering_order_form_enabled` column.** This was the better
answer on the technical merits — per-location rather than brand-wide, immune to
`get-brand-website`'s brand-over-restaurant precedence, and sitting directly
beside the three flags (`live_catering` / `party_hall` / `food_truck`) that are
already the established per-restaurant catering capability switches. It lost on
one thing: nothing in `restaurant-portal` lets an owner set those flags, so
every enablement would be a staff action, forever, one restaurant at a time.
That is the exact cost the PRD's own 5-question filter says Piece 1 exists to
avoid. Recorded in ADR-009 because it is the alternative most likely to be
proposed again by someone reading only the code.

**Snapshotting the item price alongside each selection.** The PRD's Risks
section proposes it as the mitigation for dangling `item_id`s. It isn't — the
`name`/`category` snapshot is what closes that risk, because the owner reads a
name, not an id. Price would only serve Piece 2. Nearly absorbed it on the PRD's
authority before working out that the stated risk and the stated mitigation
don't actually connect; worth remembering that "the PRD suggested it" is not the
same as "the PRD's own reasoning requires it."

## The thing I expect to be wrong

ADR-008 answers a G1 rider that came back as silence. The G1 named the
fulfillment fork and proposed no default; the approver replied "Lets start with
piece 1" and this board's convention reads silence on a rider as acceptance of
what was proposed — except nothing *was* proposed here, so the decision fell to
this design. Reading the thirteen ACs, none of them names the three fulfillment
values, so the smallest thing that satisfies them keeps `delivery_method`
untouched and makes the labels per-restaurant copy. That is defensible against
the approved criteria, but it does mean the approver's own three names
("On-site Catering", "Pickup & Delivery", "Drop-off Trays") ship nowhere by
default. If the approver wanted a platform vocabulary rather than per-restaurant
copy, this is the decision they'll correct, and ADR-008's review trigger says so
in as many words.

Second candidate: AC-1's "reveals a guest-count input" was deliberately read
narrowly (the input stays visible and required; the per-option *helper note* is
what appears), because hiding a field the owner's board and the dashboard's
income estimate both read would lose data to satisfy a clause inherited from the
pricing model Piece 1 doesn't build. Named in the design rather than absorbed,
so QA tests the right behaviour and the PM can push back before code.

## Pattern, not yet a standard

Third ticket in a row where the load-bearing find was a **write path that
replaces rather than merges**: `ENG-023`'s `update_feedback` allow-list,
`brand-portal/catering.ts`'s unconstrained `update_catering_request` (open
proposal, 2026-08-29), and now `updateWebsiteContent`'s whole-column
`.update({ catering: … })` paired with a form that re-initialises from an
explicit field list — which already silently eats the legacy `formFields` key on
every save. All three are the same shape: a correct access check in front of an
unconstrained write. The department's standards cover fail-closed *validation*
but say nothing about write breadth. If a fourth turns up, that's a standards
entry ("a write is scoped to the fields it means to change") rather than a
per-ticket finding. Not filing it as a proposal yet — three occurrences, but two
are already covered by the open 2026-08-29 proposal, and the third is fixed
inside this ticket.

## Not done

No trace file written (`traces/architect-{run-id}.json`) — no run id was issued
for this pass and no prior architect pass on this instance has written one; the
convention exists in `tech-design/SKILL.md` but not on disk. Noting rather than
inventing a run id.

Ticket frontmatter, `_index.md`, the decision journal and routing to `ready` are
the dispatching pass's, not this one's.
