---
type: eng-decision
agent: eng-manager
gate: merge
project: restaurant-portal
ticket: ENG-039
time_estimate: ~1-1.5 days
recommendation: merge — code review (round 1), quality (round 1), and security (round 1) all passed; pure frontend addition over ENG-038's already-shipped, already-reviewed backend, no new dependency, no schema change; two non-blocking code-review findings named below, neither blocking; two pre-existing operational gaps (unsubscribe secret not provisioned; SMS delivery mocked) become reachable for the first time once this merges — named in full below and in the PR, neither is this diff's to fix
pr_url: https://github.com/harsimranwalia/restaurant-portal/pull/3
raised: 2026-09-05
notified: 2026-09-05T03:41:22
nudged:
decision:
---

# Merge request — Broadcasts tab, composer, drip editor, report UI (ENG-039)

Sub-ticket 3 of 3 under `ENG-019` (restaurant marketing broadcasts) — last of
the family. `ENG-037` (schema) and `ENG-038` (API) are both merged and
`verified`.

## What this does

A third "Broadcasts" tab on the Automations page: a paginated campaign list;
a composer for a one-time message or a 2+-step drip, with an audience picker
(all customers / inactive-for-N-days), per-step email and/or SMS content, an
optional existing-offer coupon attach, and send-now-or-schedule (locks to
read-only once a campaign starts sending, reflecting the server's own
`status`); row actions to pause/resume/cancel; a report view showing
recipient status counts, delivery-by-channel, and coupon redemptions/revenue.
Consumes `ENG-038`'s API exactly as it exists on `origin/main` — no new
backend route, no schema change, no new dependency.

## Gates passed

- **Code review: pass, round 1** — `agents/principal-engineer/reviews/ENG-039.md`.
  0/10 automatic failures.
- **Quality: pass, round 1** — `agents/qa/test-plans/ENG-039.md`. 14/14, all
  five owned acceptance criteria covered (two new test files added this hop).
- **Security: pass, round 1** — `agents/security/reviews/ENG-039.md`. 0
  findings — every one of the 7 API calls this diff makes independently
  re-verified as authz-checked and tenant-scoped on the live merged backend.

No migration — pure frontend diff.

## PR

- `restaurant-portal`: https://github.com/harsimranwalia/restaurant-portal/pull/3

This project is registered **L1** — merge whenever suits you on GitHub
directly; the next build-loop pass detects the merge itself (local git
ancestry, no reply needed from you) and advances the ticket once it's in.

## Named gaps, carried forward rather than hidden

- **F1, low-to-medium severity.** A newly-added drip step's default delay
  guess can land outside the preset dropdown's options, so the 4th+ step
  shows no visible label until manually reselected. Data stays valid,
  display-only.
- **F2, low severity.** `BroadcastComposer.tsx` is 526 lines at creation,
  past this repo's ~400-line smell threshold; two clean extraction points
  named in the review.
- **Observation, not a finding.** The reused, unmodified `EmailEditor`
  component's existing raw-HTML preview is now reachable by a feature that
  can fan one message out to an owner's entire customer list at once. The
  component itself is untouched by this diff.

## Before a real send — two pre-existing gaps this PR makes reachable

This is the ticket that gives an owner their first way to actually create
and send a broadcast. Two gaps that were correctly judged non-blocking at
`ENG-037`'s and `ENG-038`'s own release-readiness hops — because nothing
could reach them yet — stop being dormant the moment this merges and
deploys. Neither is in this diff; neither is this diff's to fix.

1. **`BROADCAST_UNSUBSCRIBE_SECRET` is not provisioned.** Checked live this
   pass against the project's actual edge function secrets (not the Vault
   secrets table, which is a different store and where `service_role_key`
   lives) — confirmed absent. Every real send throws while minting the
   unsubscribe link; the throw is caught, logged, and the recipient is
   marked `failed` with the error message (visible in this ticket's own
   Report view, not silent) — but it is guaranteed on the very first real
   send by any owner until fixed. One command closes it:
   `supabase secrets set BROADCAST_UNSUBSCRIBE_SECRET=<value> --project-ref bmnmnejwdxbcqinqkwko`.
2. **SMS delivery is entirely mocked**, codebase-wide, not just for
   broadcasts. `outgoing-communications/services/sms.ts`'s `createSMSService()`
   only ever returns a `MockSMSService` in production today — no
   `SMS_PROVIDER` secret is set, and the Twilio/MessageBird/Vonage branches
   are commented-out stubs that were never built. Any campaign step with SMS
   content will report `status: 'sent'` for every recipient while delivering
   nothing — a false-positive success, not a visible failure, and there is
   no config flag that fixes it the way the unsubscribe secret has one.
   Email is real and working (Brevo-backed, live `BREVO_API_KEY`) — only the
   SMS half of the channel matrix is fake. This is pre-existing, untouched
   by `ENG-037`/`ENG-038`/`ENG-039`, and was never caught at an earlier gate
   because no earlier ticket in this family exercised the send path itself.
   This ticket's own PRD assumed otherwise ("Sizing assumes the existing
   send services (email/SMS/template) are reusable as-is"; "reuses the
   already-contracted email/SMS delivery") — checked directly this pass and
   found false for SMS specifically. Already a tracked proposal, not a fresh
   one: `agents/eng-manager/proposals.md`'s 2026-09-03 (`architect`) row on
   this exact file was corrected this pass rather than duplicated — its own
   2026-09-04 correction had narrowed the exposure for the three
   *pre-existing* triggers (they hit a `body`-vs-`message` bug and fail
   loudly instead), but broadcasts call `sendSMS` with the correct field
   name and don't have that bug, so the original, uncorrected "silent false
   success" framing is exactly what a real broadcast SMS send hits. Not
   raised as a P0 — no security exposure, no production incident, and zero
   campaigns exist yet so nobody has been affected.

Full reasoning for both: `agents/devops/notebook/2026-09-05-release-readiness-log.md`.

Neither gap blocks this PR — both are pre-existing conditions in already-shipped,
unrelated code, not something this diff's own frontend code can fix. Named
here, and in the PR body, so a real test send isn't a surprise.

## Decision

No written reply — `restaurant-portal` PR #3 merged directly on GitHub
(`aeeb7b9`, `2026-09-05T17:05:41Z`), same standing pattern this approver has
used for every prior L1 merge on this board. Found by this `watch (launchd)`
event pass's own step-5 re-check. All three gate receipts re-read fresh and
confirmed `pass`; a full acceptance-check (all 5 owned criteria) run against
the merged tree — see the ticket's own board-file log and
`agents/devops/releases/2026-09-05-restaurant-portal-ENG-039.md`. Carried
`blocked → shipped → verified` this pass. Every child of `ENG-019` is now
settled; `continue ENG-019` fired the same pass.
