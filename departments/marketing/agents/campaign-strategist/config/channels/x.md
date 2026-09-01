# X — channel playbook

**Mechanics only.** Strategy lives in `agents/campaign-strategist/agent.md` and
the instance's channel registry. This file is the reference for *how X works*.

**This is the shipped starting playbook.** `install` copies it to
`$MKT_INSTANCE/config/channels/x.md`; from then on the instance's copy is the
live one. Everything marked _[instance]_ must be filled in before the first
publish.

## Autonomy

Registers at **C1**, moves to C2 at gate M3 once the publishing path is real.

Note the distinction that matters most on this channel: **a channel with a
working ship path and an empty queue is C2, not C1.** C1 means *no publishing
path exists*, and briefing into it produces drafts with nowhere to go. In the
ported instance this channel sat at C1 for exactly one day — not as a designed
staging period, but because the publishing path broke under it (see below) and
had to be rebuilt. **A tier is a statement about what a channel can actually do**,
and it moves the moment that becomes true, not when a plan said it should.

## Publishing path — and why this instance's is not an API

**Method: `browser`** in the instance this was ported from
(`config/conventions.yaml` → `publishing.methods`). That is unusual enough to
explain, because it is the clearest worked example of the publishing seam and of
why a playbook records the path rather than assuming it.

The original design published through an integration's X tool. With the
connection **ACTIVE**, that API turned out to be unusable: reads 401, writes 401,
search **402 Payment Required**. The token was valid and the *entitlement* was
absent — X moved to pay-per-use API access with no free tier for new developers,
so this was a **billing state**, not a scope problem, and re-linking or
re-authorizing could not move it. No agent can fix a billing gate.

Publishing moved to an **authenticated browser session** driving X's native
composer. Two things improved in the swap, and one got worse:

- **Multi-part pieces publish atomically.** The composer posts the whole chain in
  one action, so a half-published thread cannot strand on a public timeline the
  way sequential reply-chaining can.
- **It costs nothing.** No metered API spend.
- **It cannot run headless.** It needs a live, logged-in browser on a machine
  someone is signed into, which makes it dependent on a session in a way no API
  channel is. That is a real operational cost and it belongs here rather than
  being discovered on the first failed run.

_[instance: state which method your X channel actually uses. If your account has
API entitlement, use `api` — this section is an example of the seam, not a
universal fact about the platform. If it is `browser`, record which machine and
which session, because that is the thing that breaks.]_

Two mechanics a browser path on this platform depends on, verified the hard way
and worth recording wherever a browser path exists:

- X's rich-text editor **ignores synthetic keystrokes.** Text goes in via
  `execCommand('insertText')` after clearing the box — it appends otherwise.
- X **silently deletes empty compose boxes.** Each box is filled immediately
  after it is added, and every box is read back before publishing.

`require_approval: true` is not negotiable. `skills/ship-content-x/SKILL.md`
publishes only a draft carrying `status: approved`, set exclusively by the
approver's explicit action.

**Verification is visual read-back:** the run reads the rendered timeline and
confirms the piece is live with the expected part count. That is a *stronger*
check than the long-form channel gets, where read-back routes can be blocked
behind a partner API entirely — see `config/channels/linkedin.md`.

## Format limits

- **280 weighted characters per unit, hard limit.** The platform counts a
  *weighted* length, not raw characters: most characters weigh 1, emoji and CJK
  characters weigh 2, and **every URL counts a fixed 23** regardless of its
  actual length. `skills/ship-content-x/SKILL.md` recomputes the weighted length
  of every unit before posting anything.
- A multi-part piece is a numbered sequence, each part individually under the
  weighted limit. **The whole piece is validated before the first part goes
  out**, so a limit failure can never leave half of it live.

## Thread mechanics

- **A standalone hook.** The first part must work on its own — someone seeing
  only part 1 in their timeline, with no thread indicator visible yet, needs a
  reason to tap in. Never open with "a thread 🧵" and nothing else.
- **Each part self-contained.** A reader landing on part 4 out of context should
  get a complete thought, not a fragment that only parses next to part 3.
- **The arc earns the length.** Each part adds something the previous one did
  not. A thread that restates its hook in smaller pieces should have been one
  post.
- **CTA on the last part only**, never mid-thread, and only when the brief says
  `include_cta`.

## What works here — general, not measured on this account

Reply velocity in the first 15–30 minutes and quote pickup are the two signals
that most influence whether a piece escapes its existing follower graph.
Structurally similar to the long-form channel's early-velocity signal, but the
window is **shorter** and **replies matter more than reactions**.

This is general platform knowledge, not an account baseline. Do not let it
harden into one.

## Cadence

- _[instance: the publishing days and time, with an explicit timezone.]_ At most
  one piece per calendar day; a multi-part piece counts as **one**, however many
  units it chains.
- **The cadence lives in the channel registry, and the ship skill reads that list
  every run**, stopping on any day not in it. In the ported instance the
  scheduler could only express "every day" or one fixed weekday, so the routine
  fired daily and the *skill's own day check* was the real cadence. Keep that
  property wherever you can: it makes changing the cadence a one-line config edit
  with no scheduler to re-create.
- Evidence for choosing days and times belongs **here**, not in config: the
  registry says *which* days, this file says *why those days*. In the ported
  instance the slots came from two independent large-sample analyses that both
  ranked mid-week highest and late-week lowest, cross-checked against the
  audience's timezone rather than the business's own — and set an hour offset
  from the long-form channel so the two never fire together. _[instance: record
  your own evidence, or record that you guessed. Both are useful; an unexplained
  cadence is not.]_
- A backlog drains oldest-first, one per publishing day. Never a burst.
- **Widening the cadence raises the real publishing rate.** Before adding a day,
  check that the queue can actually feed it — a series-driven queue that runs dry
  falls through to standalone pieces, which is designed, but a diet of them was
  not the plan.

## Hashtag and mention conventions

X has no meaningful hashtag-driven reach comparable to the long-form channel's.
**0–1 hashtags maximum**, and only when tied to a specific real event or
community. Never as a discovery tactic.

**Do not port the long-form channel's 3–5 hashtag convention here.** It reads as
spam on this platform. This is the single most common cross-channel mistake a
repurposing pipeline makes, because the text carries over cleanly and the
conventions do not.

## Current performance baselines

**All unknown until this account has shipped.** After `engagement-analyzer` has
logged enough real pieces, a measured baseline replaces this section.

Until then the performance thresholds in the channel registry are the long-form
channel's values **carried over as a starting guess** — explicitly labelled as
such, and not an X baseline. Do not invent a number here, and do not reason from
the carried-over ones as though they were measured.

## Formats

The writer skill takes `format: tweet | thread` rather than the long-form
channel's archetype list; `skills/x-content-writer/SKILL.md` holds the exact
input contract. The same source-material and voice rules apply as on any channel.
A thread is the natural home for a case-study or frame-shift beat; a standalone
piece for a sharp take or a data point repurposed from a long-form piece.

Where the queue is **series-driven** — pieces repurposed from another channel's
shipped run — the queue rule lives in that series' own file under
`content/series/`, not here. A slot with nothing queued falls through to a
standalone piece rather than going empty.

## Voice — the deliberate asymmetry

Registers: `tweet`, `thread`. Samples: `$MKT_INSTANCE/voice/samples/tweet.md`
and `.../thread.md`.

**This channel's writer skill carries no voice-sample preflight**, where the
long-form channel's does. That is deliberate, not an oversight:

- A new instance has **no** short-form corpus, and typically will not have one
  for months.
- `skills/x-content-writer/SKILL.md`'s voice frame borrows a few long-form
  exemplars for **tone and fingerprint only** — explicitly *not* for shape,
  because the shapes are unrelated ("compress hard into 280-character units" is
  not a long-form instruction).

**What it costs:** the first pieces on this channel are calibrated against a
register nobody has validated here, so they lean harder on the critique pass and
on the approver's per-piece approval than the long-form ones do. **The channel
with the least voice data has the least voice protection**, which means gate M2
is doing more work on this channel than anywhere else. Read the early pieces
closely; treat the first few publishes as verification, not routine.

**Do not close the gap by seeding the corpus from an existing personal
account.** This was investigated and rejected in the ported instance, with the
searches logged so it would not be re-proposed each quarter: the account had
hundreds of posts, of which the professional subset was a handful of stale link
shares, and its live register was personal. Using it as exemplars would have
pulled drafts *away* from the business's professional voice, not toward it.
**A corpus in the wrong register is worse than an empty one** — an empty corpus
produces cautious generic drafts that review catches; a wrong-register corpus
produces confident drafts in the wrong voice that review approves.

The corpus seeds from the front instead: approved, shipped pieces become the
exemplars.

## Enable checklist — kept as history

The gate list for turning this channel on in the ported instance. Kept rather
than deleted, because **an overruled checklist item deserves a written reason,
not a silent edit** — and because the pattern generalizes to any new channel.

1. ✅ **The connection exists.** The account was linked and the handle recorded.
   Note what "connected" turned out to mean — see item 2.
2. ⚠️ **Failed, and the design changed because of it.** The plan was to verify
   the integration's publishing tool. The tool existed and the connection went
   ACTIVE, but every call failed: 401 on reads and writes, 402 on search. Valid
   token, absent entitlement, a billing gate no agent can move. **Publishing
   moved to an authenticated browser session.** That trade was not chosen over a
   working alternative — the API returned an error on every call.
3. ✅ **Done, with a deviation, recorded.** This item said "extend the existing
   ship skill to handle the second channel." It was overridden in favour of a
   **separate** `skills/ship-content-x/SKILL.md`: the long-form ship skill is
   mostly machinery this channel never uses, while this channel needs machinery
   the long-form one has no analogue for — composer-driven multi-part posting,
   per-unit weighted-limit revalidation, timeline read-back, a different cadence.
   Same reasoning that split the writer skills.
4. ✅ **Registered** in the channel registry with a real weekly plan.

The original item 3 also asked whether this channel should inherit the long-form
channel's cadence or get its own. Answered: **its own**, on the evidence in
"Cadence" above. A channel that inherits another channel's cadence has not been
thought about.
