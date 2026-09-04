---
id: ADR-020
title: "Broadcast opt-out reuses `customers.consent_email`/`consent_sms` via a new public unsubscribe function, not a new column or an `outgoing-communications` action"
project: aiorders-api
ticket: ENG-019
status: accepted
decided_by: architect
date: 2026-09-03
supersedes:
superseded_by:
---

# ADR-020: Broadcast opt-out reuses `customers.consent_email`/`consent_sms` via a new public unsubscribe function, not a new column or an `outgoing-communications` action

## Context

AC6 requires a working unsubscribe path on every campaign send and durable
exclusion from every future send. No opt-out mechanism exists anywhere in
this codebase today — `git grep -i "unsubscribe|opted_out|opt_out"` across
`aiorders-api` finds only Brevo's own webhook event names
(`external-integrations/handlers/brevo.ts`), which update a *per-message*
`communication_log.status` to `unsubscribed`, not a durable per-customer
exclusion any future send would check.

Separately, `crm/customers.ts` already reads and writes `consent_email`/
`consent_sms` — JSONB columns shaped `{consent: boolean, consent_at,
channel?, source?, method?}` — already populated on **every** customer at
creation: `external-integrations/handlers/cloudwaitress.ts`'s
`findOrCreateCustomer` sets `consent_email: {method: 'website', source:
'online-order', consent: true, consent_at: now}` (and the SMS equivalent) for
every order-created customer. That is the exact CASL "implied consent from an
existing order relationship" reasoning the PRD's own Risks section already
argues in prose — already captured as a live, per-channel field, not
something this ticket needs to invent.

## Decision

Unsubscribing sets `consent_email.consent = false` (email link) or
`consent_sms.consent = false` (SMS link) on the customer's own row, via the
same update shape `crm/customers.ts` already accepts. Every campaign email
and SMS carries a link to a new, small, public, unauthenticated edge function
(`broadcast-unsubscribe`) keyed by an opaque per-customer token; visiting it
flips the relevant consent field and returns a plain confirmation page. The
broadcast audience-resolution query excludes any customer whose relevant
channel's `consent.consent` is `false` — checked once at campaign-start
snapshot, and again by the dispatcher immediately before every individual
send (per this design's Interfaces/Risks), so a customer who unsubscribes
between enrollment and a later drip step is still excluded from that later
step.

## Alternatives

| Option | Why not |
|---|---|
| A new dedicated `broadcast_opt_out` column or table | `consent_email`/`consent_sms` already exist, are already channel-scoped (matching CASL's own channel-level consent concept), and are already wired into `crm/customers.ts`'s update path. A new column would duplicate a field that already means exactly this. |
| Add the unsubscribe action to `outgoing-communications` | That function's router requires either `systemTriggered: true` or a real user Bearer JWT for *every* action — a customer clicking a link from their inbox has neither. Retrofitting a public, unauthenticated exception into a gate this project just finished tightening (`ADR-016`/`ADR-017`, the `ENG-022`/`ENG-029`/`ENG-035`/`ENG-036` cross-tenant/auth cascade, same evening) reopens exactly the class of hole that work closed, for one narrow new purpose. |
| SMS opt-out via inbound "STOP" reply parsing | `outgoing-communications/services/sms.ts` is fully mocked — no real provider, no inbound-message path exists at all in this codebase. Building one is separate work the PRD's own Non-goals already exclude ("no new outbound channel" implies no new inbound one either). The same link, in the SMS body text, covers SMS the same way it covers email. |

## Consequences

**Accepted:** `consent_email.consent_at`/`consent_sms.consent_at` stop
meaning only "when the customer first consented" once a customer
unsubscribes — it becomes "when consent was last set, in either direction."
Nothing in this codebase today reads either field as an immutable historical
fact, so this is safe, but worth naming for whoever next touches it.

**Accepted:** the reactive `Automations` (welcome/birthday/winback) do not
check either consent field before sending, today or after this ticket — this
design does not change that, per the PRD's own non-goal ("any change to the
existing reactive Automations" is out of scope). Broadcasts becomes the
first sender on this platform to actually honor the field it's named for.

**Gained:** zero schema change to `customers`. The only new object is one
small public function plus its token-verification logic.

## Review trigger

If `Automations` is ever revisited and made to respect `consent_email`/
`consent_sms` too — closing the gap this ADR deliberately leaves open — no
change is needed here; the fields already mean the same thing to both.
