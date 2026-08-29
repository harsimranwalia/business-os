---
ticket: ENG-009
project: aiorders-admin-hub
status: awaiting-scope
size: S
author: product-manager
created: 2026-08-29
decided:
---

# Influencer engagement info — internal activity signal plus a staff-editable social stat

## Readback

**You said:** "i mean both reading a and reading B. reading A is something
we can start with now so we know how active the particular influencer is.
reading B is something our staff can update or later we can connect using
some api from meta." (answering
`inbox/_handled/2026-08-29-eng008-engagement-source-question.md`, itself
carved out of the same request as `ENG-008`)

**Understood as:** Build both. An internal activity signal (how active an
influencer is on AIOrders, derived from data we already have or will have)
now, and a social-media engagement figure that staff enter and update by
hand for now — a live connection to a Meta API is explicitly future work,
not this ticket.

**Requirements:**
1. `[confirmed]` Staff can see an internally-derived indicator of how
   active an influencer is on AIOrders.
2. `[confirmed]` Staff can view and manually enter/update a social-media
   engagement figure for an influencer.
3. `[inferred]` The two are shown as distinct values, not merged.
4. `[proposed]` The manually-entered figure shows when it was last
   updated.

**Assumed, and worth correcting if wrong:**
- "How active" is a derived read (e.g. campaigns applied to,
  collaborations, response rate) — the architect picks the concrete
  measure from what already exists rather than this PRD inventing a
  formula.
- The social figure is one overwritable number per influencer, not a
  history of past values.
- No specific platform is hardcoded — staff can label which platform a
  figure refers to.

No second blind architect reading run for this ticket — the ambiguity it
would test for was already found and resolved by the approver's own
direct answer to the standing question raised while shaping `ENG-008`;
see that PRD's Readback section for the original two-reading comparison.

## Problem

Staff have no way to see how active an influencer is on AIOrders or to
record their social reach, even informally, so both signals are missing
from every matching or rating decision made on the admin board.

## Why now

Direct, immediate follow-on to `ENG-008` — the approver named this while
that ticket's own standing question was being answered, in the same
conversation.

## Users

AIOrders staff operating the admin panel. Not influencer-facing.

## Proposed change

An influencer's admin record shows an internally-derived activity signal
and a staff-editable social engagement figure. No external API call is
made.

## Acceptance criteria

1. `[confirmed]` Given an influencer with campaign/collaboration history,
   when staff view their admin record, then an activity signal derived
   from that history is displayed.
2. `[confirmed]` Given an influencer with no social figure set, when staff
   enter one, then the admin board displays it and it persists.
3. `[confirmed]` Given an influencer with a social figure already set,
   when staff update it, then the board reflects the new value.
4. `[proposed]` Given a social figure that has been set, then the board
   also shows when it was last updated.

## Non-goals

- Any live Meta/Instagram/TikTok API integration — explicitly deferred by
  the approver's own words ("later we can connect").
- OAuth or any influencer-side account connection.
- A history/timeline of past social figures — one current value only.
- Automated recalculation of the activity signal on a schedule — computed
  on read is sufficient unless the architect finds a reason otherwise.

## Risks and unknowns

- The exact internal measure behind "how active" is left to the
  architect — doesn't change the acceptance criteria above, only the
  underlying query.
- No dependency on `ENG-008`'s own fields, but both tickets touch the same
  admin UI file and the same influencer table — sequencing them back to
  back (not concurrently) avoids a needless merge conflict; the EM's call
  at `ready`.

## Cost

- Build: `S` — one or two new columns, a derived read, and a small admin
  UI addition to a screen `ENG-008` is already touching.
- Run: `$0/month` — no new vendor; the Meta API connection this ticket
  explicitly excludes is where a future cost would appear, not here.

## Decision

Filled in by the approver.
