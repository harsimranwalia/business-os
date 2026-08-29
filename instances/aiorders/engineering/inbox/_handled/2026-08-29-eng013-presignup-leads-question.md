---
type: eng-decision
agent: product-manager
gate: intake-question
project: aiorders-admin-hub
ticket: ENG-013
recommendation: Answer when convenient — does not block ENG-013's G1 or build. Once answered, "yes" becomes its own new ticket; "no" closes this with nothing further to do.
raised: 2026-08-29
notified: 2026-08-29T11:39:45
time_estimate:
decision: approved
decided: 2026-08-29T11:46:34.557123+00:00
---

# One open thing before "sales" can be fully scoped — does not block ENG-013

**You said:** "for the foodswipe **SALES** funnel page... sales, onboarding
staff..." (from the same request as `ENG-013`,
`agents/eng-manager/board/ENG-013-foodswipe-funnel-stage-control.md`)

Two independent readings of this request (this PM's, and, separately and
blind to it, the architect's) both noticed the same thing once checked
against the actual page: every stage on the Foodswipe funnel page today —
Account Created, Profile Updated, Listing Claimed, Menu Uploaded, GBP
Shared, Website Interest — describes a restaurant that has **already
signed up**. There is no stage, anywhere in the system, for a restaurant
that hasn't signed up yet — a cold lead, someone a sales rep is trying to
land. The architect's blind reading independently guessed that "sales"
staff might need exactly that: a phase before "Account Created" even
happens, with its own vocabulary (something like contacted → interested →
signed up).

`ENG-013` (this page's PRD) builds the confirmed, bounded fix regardless
of this answer: staff can set/correct a listing's stage among the six
that already exist. This question is about whether something bigger is
also wanted.

**Reading A:** No — "sales" just describes who uses this page alongside
onboarding staff, working restaurants that have already signed up. The
six existing stages are the whole picture; `ENG-013` alone covers it.

**Reading B:** Yes — sales staff also need to track prospects who
haven't signed up yet (cold leads, people they're actively trying to
close), and that's a genuinely separate, new pipeline this system has
nothing for today — a new record type with no `profiles` row to hang off
of, not an extension of the existing kanban.

**Which one — or is there a third thing "sales" means here?** If Reading
B, naming roughly how leads get into that pipeline today (a spreadsheet,
a CRM, memory, nothing yet) would help scope it.

This does not hold up `ENG-013`. Once answered, "yes" gets shaped into
its own ticket, sized properly once we know where leads come from today;
"no" just closes this question.

## Decision

Filled in by the approver.

## Decision

**approved** — 2026-08-29T11:46:34.557123+00:00

Reading B. autopilot built to nurture these leads to next stages autpmatically and send them emails/sms to nurture

---

**Processed 2026-08-29 (`scheduled` event pass, context `schtasks`).** Found
sitting answered-but-unprocessed. Per this item's own stated next step
("yes gets shaped into its own ticket"), checked for an existing ticket
before filing a new one first — and found one: a later `intake` event pass
this same day (context: the "no autopilot for sales staff/resellers"
request) independently reached the same conclusion from the approver's own
words and filed `ENG-017` (presignup lead nurture autopilot,
`agents/eng-manager/board/ENG-017-presignup-lead-nurture-autopilot.md`),
already `state: shaped`, already citing this exact answer as grounding
evidence in its own Notes. **No new ticket filed here** — doing so would
duplicate `ENG-017`, not extend it. This item's own job (get the question
in front of the approver and route "yes" to a ticket) is complete via that
ticket. `ENG-013` itself was never blocked by this question and needs no
further action from it. Journaled in
`agents/eng-manager/config/decision-journal.md`.
