# campaign-strategist — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/campaign-strategist/`.

Append only. A reverted change is not deleted here; the rollback appends its
own entry.

<!-- The marketing department ships no versioning or rollback scripts of its
     own. `departments/engineering/lib/agent-version.sh` and
     `agent-rollback.sh` are the reference implementations if an instance wants
     them; until one is wired here, a version is a git tag on this directory
     and a rollback is a git revert. -->

## v1 — 2026-08-29 — ported out of life-os
Changed:  This agent exists. Ported from `life-os@2026-08-29` as the middle
          layer of the marketing department: CMO → campaign strategist →
          content writer.
Source:   port

**Its own history, for context.** In life-os this agent began as a single-channel
LinkedIn agent, was widened to a cross-channel strategist when a second channel
arrived, and had a content writer split out from underneath it at the same time.
Both moves survive the port intact and are the reason the shape is what it is:
strategy sits in one agent because it is cross-channel by nature, and craft sits
below it because craft is the same job whatever the channel.

**Depersonalized.** Gone: the named approver, the identity and voice stores, the
running content series and its stages, named clients, the publishing author URN
and account handle, and the integration connection identifiers. The series
*mechanism* stayed — `content/series/`, the total-pause rule, the checked resume
condition, and the trailing-series fall-through — because all four are general
and all four were learned the hard way. The particular series did not.

**The channel registry moved out of this agent.** In life-os this file held the
per-channel `enabled` flag, publishing credentials and cadence. Here it holds
**defaults only**; the live registry is the instance's `config/config.yaml` and
the mechanics are the playbook's. Three files could each plausibly hold "the
channel's cadence" and exactly one now does — duplicating a number to save a
file read is how two copies end up disagreeing and the wrong one wins.

**Autonomy tiers are explicit.** Channel autonomy is now C0–C3 and belongs to
the channel, never to the piece. This agent does not move a channel between
tiers — that is an M3 proposal from the CMO — but it does own the consequence:
not briefing into a tier that cannot receive it, and knowing that a channel with
a working ship path and an empty queue is C2 rather than C1.

**The interrupt got its honest name.** The "interrupt duty" here has never
interrupted a human: an outperforming piece produces two follow-up drafts, and
the approver hears about it in the weekly report. Stated plainly in the
frontmatter now, because "interrupt_rule" read like a line to the approver and
was not one.

**The voice asymmetry was kept and labelled rather than evened out.** The
long-form path runs a voice preflight; the short-form path deliberately does not,
because a new instance has no short-form corpus and the writer skill borrows
long-form exemplars for tone only. The consequence — M2 carries more weight on
that channel — is now written in both this agent's config and the playbook,
instead of being a property someone would have to infer by noticing an absence.
