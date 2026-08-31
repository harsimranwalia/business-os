# cmo — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/cmo/`.

Append only. A reverted change is not deleted here; the rollback appends its
own entry.

<!-- The marketing department ships no versioning or rollback scripts of its
     own. `departments/engineering/lib/agent-version.sh` and
     `agent-rollback.sh` are the reference implementations if an instance wants
     them; until one is wired here, a version is a git tag on this directory
     and a rollback is a git revert. Stated rather than implied — a changelog
     that references tooling which does not exist is worse than one that
     admits the tooling is manual. -->

## v1 — 2026-08-29 — ported out of life-os
Changed:  This agent exists. Ported from `life-os@2026-08-29` as the head of
          the reusable marketing department, alongside the campaign strategist
          and the content writer, to the same contract shape the engineering
          department was ported to on 2026-08-22.
Source:   port

**Renamed `marketing` → `cmo`.** In life-os the agent and the department shared
the name `marketing`, which worked while there was exactly one of each. Here
`marketing` is the department and `cmo` is the agent inside it. Role, scope and
reporting line are unchanged; the department is now installed per business, so
the agent needed a name that survives living inside a directory called
`marketing/`.

**Depersonalized.** Gone: the named approver, the `clone/` identity and voice
stores, personal aims and values, named clients, the offer ladder and its
prices, the running content series, the publishing author URN, and the
subscription-tier reasoning. Replaced by the seams in
`config/conventions.yaml` — the `approver` role, the per-instance voice corpus,
`../knowledge/business-profile.md`, and `instance_configured` keys in
`config.yaml`. The judgment in these files transfers; the person does not, and
a template that ships one business's positioning produces content that sounds
like that business for everyone who installs it.

**The gates and tiers got names.** The three human gates are now **M1 strategy
/ M2 the piece / M3 channel autonomy**, and channel autonomy is **C0–C3**. Both
progressions already governed behaviour in life-os without having handles,
which meant they could only be referred to by describing them. A gate nobody can
name is a gate nobody can point at in a review.

**The positioning audit stopped being a skill.** `positioning-auditor` is gone;
the biweekly audit is now the CMO's own read of the last eight shipped pieces.
The audit's useful output is a judgment about drift across a run of pieces —
the one thing a per-piece scoring skill is worst at. It produced eight scores
and no conclusion.

**The voice floor stopped being a refusal.** Below ten samples in a register,
drafting now continues and leans harder on the review pass and on M2, with the
gap recorded in config. In life-os the long-form path refused. Every new
instance starts with an empty corpus, so a refusal at the floor means a freshly
installed department produces nothing and the operator's first experience of it
is a block — while the risk it guarded against, an under-calibrated draft going
out, is already covered by M2, which is per-piece and unskippable. Turning the
floor back into a refusal is the approver's call, per instance.
