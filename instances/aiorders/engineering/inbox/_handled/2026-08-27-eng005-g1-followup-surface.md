---
type: eng-decision
agent: product-manager
gate: scope
project: aiorders-admin-hub
ticket: ENG-005
follow_up_to: inbox/_handled/2026-08-27-eng005-g1-scope.md
recommendation: RestaurantDetails.tsx — the only admin-hub page shaped to receive the component's required props (restaurantId, restaurantName, websiteUrl, logoUrl, primaryColor)
raised: 2026-08-27
notified: 2026-08-27T18:16:48
decision: approved
decided: 2026-08-27T20:08:53.367622+00:00
---

# G1 follow-up — which surface for A4PosterGenerator?

## Where this left off

You answered the original G1 (`inbox/_handled/2026-08-27-eng005-g1-scope.md`):
**"wire it in."** That settles the fork this ticket opened with — the
component is wanted, and the revert branch is closed. It did not answer the
other half of that G1's own question: *"Wire it in — and name the
route/surface it should appear on, so acceptance criteria can be written
against it."* This ticket's own PRD treats guessing that surface as a
non-goal rather than something to invent quietly, so this is one narrow
question, not a new G1 — answer it and this moves straight to `designed`.

## What the code says

Investigated fresh against `origin/main` (worktree fetched first) rather than
guessing from the component's name:

- `A4PosterGenerator`'s props are `restaurantName`, `websiteUrl`, `logoUrl`,
  `primaryColor`, `restaurantId` — one restaurant's own detail context, not a
  picker across many.
- Of the admin hub's 19 pages, exactly one is shaped that way:
  `src/pages/RestaurantDetails.tsx` — it already loads `name`, `website`,
  `logo_url`, and `id` for a single restaurant. `Restaurants.tsx` is the list
  view; nothing else on the sidebar (`AppSidebar.tsx`) carries a single
  restaurant's identity this way.
- No existing poster/QR/marketing section on `RestaurantDetails.tsx` to slot
  into — wiring it in means a new section on that page, not enabling
  something half-built.

## Recommendation

**`RestaurantDetails.tsx`** — matches the original request's "wire it into a
route or surface in the admin hub" and is the only page that can receive the
component's props without inventing a new data-fetch. Not treated as
decided: this is the naming this G1 exists to get from you, not a default the
department is quietly adopting.

## Decision

**Confirm `RestaurantDetails.tsx`**, or **name a different surface** — either
answer is enough to write acceptance criteria and move `ENG-005` to
`designed`.

## Decision

**approved** — 2026-08-27T20:08:53.367622+00:00

lets do RestaurantDetails.tsx

---

**Processed 2026-08-27 (`decision` event pass).** Confirms the recommendation
as given — no different surface named. PRD acceptance criteria filled in
(`agents/product-manager/specs/ENG-005-a4-poster-generator-decision.md`);
ticket moved `awaiting-scope → designed → ready` in the same pass (no
one-way door — additive, reversible, no schema, no new dependency, so no G2;
see `agents/architect/designs/ENG-005-a4-poster-generator-wire-in.md`).
Journaled in `agents/eng-manager/config/decision-journal.md`. See the
ticket's own log for the full transition record.
