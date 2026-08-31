# content-writer — changelog

Behavioural changes to this agent, newest last. Versions are derived from git
history scoped to `agents/content-writer/`.

Append only. A reverted change is not deleted here; the rollback appends its
own entry.

<!-- The marketing department ships no versioning or rollback scripts of its
     own. `departments/engineering/lib/agent-version.sh` and
     `agent-rollback.sh` are the reference implementations if an instance wants
     them; until one is wired here, a version is a git tag on this directory
     and a rollback is a git revert. -->

## v1 — 2026-08-29 — ported out of life-os
Changed:  This agent exists. Ported from `life-os@2026-08-29` as the craft
          layer of the marketing department: CMO → campaign strategist →
          content writer.
Source:   port

**Its own history, for context.** In life-os this agent was split out on
2026-07-31 from under what was then a single-channel agent, when a second
channel arrived: drafting discipline — voice fidelity, hook craft, the
critique and review loop — is one job regardless of channel, while the
strategy call (what, when, which channel) is a different job that must not be
re-litigated per format. A second life-os entry (2026-08-10) made the
carousel archetype actually renderable. Both survive the port; the reasoning
behind the split is the reason this agent exists at all. The name collision
survives too — `agents/content-writer/` and `skills/content-writer/SKILL.md`
share a name and nothing else — and is now explained once, in `agent.md`,
rather than left for every reader to untangle.

**Depersonalized.** Gone: the named approver, the personal identity and voice
stores (replaced by the per-instance voice seam — `voice/guide.md`,
`voice/samples/{register}.md`), named clients and their fixed euphemisms, the
running content series, and model product names (each pass now names a
`generation` or `reasoning` tier that the instance binds to a model). One
rule was deliberately kept when its example was cut: **never name a client
without confirmed permission.** The instance's `naming_rules` decides who
that protects, and an instance that declares none gets every named client
anonymized by default — the guardrail was never about one client.

**Two skills this agent used to invoke no longer exist, deliberately.**
`draft-critique` is gone — critique is Pass 2 inside each writer skill, so
the criteria live in one place, next to the writing they judge, and cannot
drift from the skill that must satisfy them. `render-infographic` is gone —
a single image now renders through whatever the channel's playbook names in
`image_renderer`, and a channel with none registered writes `image: none`
plus an `image_note` instead of silently shipping textless. This agent's
files describe those mechanisms, not the originals.

**The voice floor stopped being a refusal, and the tally left the config.**
The life-os config's `min_samples_to_run: 10` gated real runs; here, below
the floor, the writer skill drafts anyway, stamps `voice_sample_count` and
`below_voice_floor`, and the piece leans harder on review and on M2 — a
fresh instance always starts below the floor, and the full reasoning is in
the CMO's changelog. The per-register sample tally the old config carried is
gone too: it was instance state pretending to be template config, and the
corpus itself is the count. The short-form path's missing preflight was kept
and labelled rather than evened out — borrowed long-form samples calibrate
tone only, and the critique pass and M2 carry more weight on that channel.

**The review loop's driver is stated honestly.** The life-os agent file said
this agent re-called the drafting skill on a `revise` verdict; the ported
`content-reviewer` drives its own loop — it calls the writer's
`revision_target` path, re-reviews, and stops at 2 rounds. This agent
invokes the reviewer once per piece and honours the outcome, including
`unresolved`, which attaches the concerns visibly and moves the piece to the
approver anyway. Where the old prose and the ported skills disagreed, the
skills won.

**The channel gate changed shape.** life-os held drafts back from the second
channel with an `enabled: false` flag; here the same protection is the
autonomy tier — `c0` drafts nothing, and `c1` drafts only against a live
reason and a date, because a draft with no publishing path is a dead end,
not a draft. Same intent, expressed in the vocabulary the whole department
now shares.
