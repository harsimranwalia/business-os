---
ticket: ENG-005
project: aiorders-admin-hub
status: verified
size: S
author: product-manager
created: 2026-08-25
decided: 2026-08-27T20:08:53.367622+00:00
---

# Decide and act on the orphaned A4PosterGenerator component

## Readback

**You said:** "`src/components/A4PosterGenerator.tsx` was committed to
`aiorders-admin-hub` on 2026-08-23 (`bfddffe`)... Nothing imports it... First
decide whether it is wanted, then act on the answer. If it is, wire it into a
route or a surface in the admin hub and say which. If it is not, delete it —
`bfddffe` is a single-file commit specifically so reverting it is clean.
Small, and genuinely low stakes." (`inbox/requests/2026-08-23-a4-poster-generator-unwired.md`,
filed by Harry, 2026-08-23)

**Understood as:** A component exists, fully committed, that nothing in the
running app can reach. You want a decision made on whether it's wanted at
all, then that decision executed cleanly in the same repo — wired into a
named route/surface if yes, reverted if no — so it doesn't sit in
committed-but-dead limbo indefinitely.

Two independent readings were run on the raw request — this PM's and, blind
to it, the architect's (an independent subagent, given only the raw request,
the business profile, and the admin-hub registry row — no PM
interpretation). They agreed completely on the ask and the fork; no material
divergence. The architect's reading went further on the technical texture —
inferring from the name and the AIOrders domain (commission-free direct
ordering) that "A4 poster" plausibly means printable, per-restaurant
collateral (a table poster or window cling driving customers to direct
ordering, possibly QR-coded) — a plausible guess this PRD notes but does not
treat as fact, since the request itself never says what the component does.
The architect's reading also caught something this PM's first pass hadn't
weighed: `aiorders-admin-hub` has **64 uncommitted files in the human
checkout** (`config/projects.md`), so this single committed file may share
dependencies with work the department cannot currently see — "wire it in"
could fail for reasons invisible to anyone building only from `main`. That
risk is carried into this PRD.

**This ticket cannot be fully shaped the way `ENG-002`/`ENG-003`/`ENG-004`
were, and that's deliberate, not an oversight:** the request's own first
line is "first decide whether it is wanted" — there is no PRD-writable
acceptance criterion for "wire it in" without knowing what surface, and none
for "delete it" that isn't already trivial. Rather than guess a direction
(which is exactly the thing the request asks *not* to do) or auto-skip G1 on
the size/type mechanics (`S` + `chore` would ordinarily skip it per
`config/definition-of-done.md`'s Size table), this ticket routes the fork
itself to G1: **G1 is being required here despite the mechanical auto-skip
eligibility**, because what's missing isn't ceremony, it's the one fact
(wanted or not) the rest of the ticket depends on. This is a deliberate,
logged judgement call, not a rule change — see the ticket log.

**Requirements, tagged by where they came from:**
1. `[stated]` A decision: is `A4PosterGenerator.tsx` wanted?
2. `[stated]` If yes: wire it into a named route or surface in
   `aiorders-admin-hub`.
3. `[stated]` If no: revert `bfddffe` (a clean, single-file revert).
4. `[inferred]` "Wired in" means reachable by a human via normal navigation,
   not merely present in the bundle.

**Assumed, and worth correcting if wrong:**
- That you (or whoever committed `bfddffe`) don't already have a specific
  surface in mind — the request explicitly leaves this open ("say which"),
  so this PRD doesn't propose one; naming one is exactly what G1 is being
  used to ask.
- That the component's own completeness (does it compile, does it depend on
  anything only present in the 64 uncommitted files) hasn't been checked yet
  — worth a quick look at `building`, whichever branch is chosen, before
  assuming it's finished code.

## Problem

A committed, fully-merged component in `aiorders-admin-hub` is unreachable
from the running app — nothing imports it. Re-verified this pass
(2026-08-25): still true, still the only reference to itself. Left as-is, a
committed-but-dead component reads as intentional to the next person who
finds it, when it's actually just unresolved.

## Why now

Small and explicitly low-stakes per the request — this isn't time-pressured.
Worth resolving before it's forgotten and the context for *why* it was
committed (rather than just left in a working tree) is lost entirely.

## Users

Not directly user-facing yet — becomes user-facing (for restaurant operators
using the admin hub, and indirectly their customers if the poster is meant
to drive them to direct ordering) only if the decision is "wire it in."

## Proposed change

Not proposed here — this is the one ticket of the three shaped this pass
where the department is not recommending a build, because the build itself
depends on an answer only the approver can give. The G1 item asks the
question as a choice, per `skills/request-readback/SKILL.md` step 5.

## Acceptance criteria

Both halves of the fork are now answered — wired in, on
`RestaurantDetails.tsx` (`inbox/_handled/2026-08-27-eng005-g1-followup-surface.md`).
Only the wire-in branch's criteria apply; the revert branch is closed and its
criteria are dropped rather than kept as dead weight.

- `[stated]` Given the admin hub after this ships, when a human navigates to
  a restaurant's detail page (`/restaurants/:id/details`,
  `src/pages/RestaurantDetails.tsx`), then `A4PosterGenerator` renders without
  error in a new section on that page.
- `[stated]` Given the same, then the poster section is reachable via the
  page's existing navigation (a restaurant's row → Details), not only by a
  direct URL — satisfied by placement on an already-discoverable page, no new
  nav entry needed.

## Non-goals

- Does not guess which surface the component belongs on — that's the
  question this ticket's G1 asks, not something this PRD invents to avoid
  asking.
- Does not touch any of `aiorders-admin-hub`'s other 64 uncommitted files,
  regardless of whether they turn out to be related.
- Does not pursue comprehensive testing of the component either way — this
  is sized `S`, smoke-level at most, matching the request's own "small,
  genuinely low stakes."

## Risks and unknowns

- Whether the component actually compiles and is functionally complete, or
  is a rough checkpoint — unknown until opened.
- Whether it depends on anything that exists only in the 64 uncommitted
  files in the human's checkout — if so, "wire it in" could fail for
  reasons invisible to a department session working only from `main`
  (architect's reading; see above).
- If "wire it in" is chosen, the actual size may exceed this ticket's
  provisional `S` — e.g., if it needs new data-fetching, a QR-code
  dependency, or a permissions gate not yet in the admin hub. Flagged for
  the EM/architect to resize after the decision, not fixed here.

## Cost

- Build: `S`, provisional — genuinely uncertain until the decision is made;
  see Risks. The delete branch is trivially `XS`; the wire-in branch is the
  one that could grow.
- Run: $0/month either way — no new infrastructure implied by either branch
  as currently understood.

## Decision

- **The approver's answer (fork):** approved — "wire it in" (`inbox/_handled/2026-08-27-eng005-g1-scope.md`)
- **Date:** 2026-08-27T18:03:50.514589+00:00
- **The approver's answer (surface follow-up):** approved — "lets do
  RestaurantDetails.tsx" (`inbox/_handled/2026-08-27-eng005-g1-followup-surface.md`),
  confirming the PM's evidence-backed recommendation rather than naming a
  different surface.
- **Date:** 2026-08-27T20:08:53.367622+00:00
- **Notes:** Both halves of the G1 fork are now settled — the component
  stays, wired into `RestaurantDetails.tsx`, revert branch closed. Acceptance
  criteria filled in above now that the surface is known. `status` moves to
  `designed`; see the ticket log and
  `agents/architect/designs/ENG-005-a4-poster-generator-wire-in.md` for the
  technical design (no one-way doors — additive, reversible, no schema, no
  new dependency — so no G2). No `## Dissent` section — same
  `agents/critic/agent.md` gap as the other two shaped this pass.
- **Size resolved at design: stays `S`, not resized.** Closes the open
  question this PRD's own Risks section flagged — design confirmed no new
  data-fetching (four of five props come from the page's existing fetch) and
  no new dependency (the QR flow's `url-shortener` function and `jspdf` both
  already exist/are already installed). The fifth prop, `primaryColor`, has
  nothing to read from and is passed `null`.
