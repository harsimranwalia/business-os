# The Marketing Team

Three agents that run a business's distribution end-to-end so the approver
doesn't have to. Ported out of `life-os` on 2026-08-29, a week after the
engineering department. This is the map — read it before touching any agent in
the department.

**Reading the paths in this document.** `agents/{name}/agent.md`, `skills/`,
`lib/` and `config/conventions.yaml` are **department**-relative (`$MKT_DEPT`,
read-only at runtime). Everything else — `content/`, `voice/`, `inbox/`,
`performance/`, `proof/`, `reports/`, `config/config.yaml`,
`agents/{name}/notebook/` — is **instance**-relative (`$MKT_INSTANCE`, the only
thing ever written). An agent directory exists in both roots and holds
different things in each: the definition in the template, the memory in the
instance.

## Why it exists

A business's credibility is usually real and usually invisible. What turns one
into the other is publishing, consistently, for longer than anyone feels like
doing it. Left to one person that means: pick a topic, write the piece,
second-guess the hook, make the image, remember to publish, check the numbers,
forget to check the numbers, repeat weekly forever. That is a part-time job
bolted onto a full-time one, and it is the first thing dropped in a busy week —
which is exactly the week the compounding breaks.

The department replaces all of it. Agents mine the topics, write the drafts in
the business's voice, critique them, review them against real engagement data,
render the assets, queue the publishing, ship on schedule, collect the numbers,
and fold what they learn into next week's plan. The approver's recurring role
is one thing: approving or rejecting pieces. Everything else — strategy
included — is *proposed* to them, never *operated* by them.

**The measure:** if a change to this department adds a recurring manual step to
the approver's week — a number to paste, a file to edit, an upload to do —
it's designed wrong. Automate it or drop it.

## The roster

| Agent | Role | Owns | Talks to the approver? |
|---|---|---|---|
| `cmo` | CMO | Positioning, ICP, the channel portfolio, the weekly allocation, the narrative arc, the funnel read, the unified weekly report | **Yes** — strategy proposals (M1/M3) and one weekly report |
| `campaign-strategist` | Cross-channel strategist | Which channel each beat serves, in what format, in what order. Archetype/CTA rotation, repurposing, the topic bank, engagement analysis, inbound-signal routing, publishing oversight | **Only through the work** — pieces reach the approval surface; the agent never messages the approver |
| `content-writer` | Craft specialist | Turning a per-piece brief into a reviewed, voice-correct draft plus its assets | **Never** |

**The CMO is the front door for strategy, and the only agent that initiates a
conversation with the approver.** One unified weekly report, and inbox
proposals when positioning, the ICP, or the channel portfolio should change.
The **campaign strategist** raises pieces for approval — but a piece is raised
by *being a draft on the approval surface*, not by an agent deciding to speak.
The **content writer** never talks to the approver at all.

This is deliberate, and it is the same reasoning engineering uses for keeping
eight of its ten agents silent: three agents each pinging one human is worse
than no department at all. The whole value proposition is *fewer* inbound
threads, not three well-organised ones.

The hierarchy is strict about who decides what, and each boundary is written as
a `never_touches` list in the agent's own file:

- The **CMO** decides *whether a channel exists* and how much of the week's
  content capacity each one gets. It never writes a piece and never executes a
  channel.
- The **campaign strategist** decides *which channel each beat serves, in what
  format, in what order*. It never proposes a new channel and never writes a
  word.
- The **content writer** decides *how well the piece is written*. It forms no
  opinion about what to write, when, or where.

Crossing one of those lines in either direction is a contract violation, not
initiative.

## The pipeline

Every artifact has an owner, a next step, and a mechanism that advances it.
Nothing here is allowed to be produced with no path forward. Traced end to end:

```
  topic  (the topic bank | inbox/requests/ from a filer | a proof entry |
     │    an outperformer follow-up)
     ▼
  [cmo]  weekly. Reads ../knowledge/business-profile.md, last week's
     │   performance, the topic bank, and inbox/requests/.
     │   Writes the ALLOCATION BRIEF: how many pieces, any emphasis, any
     │   trades, and the current narrative arc in one line.
     ▼
  [campaign-strategist]  splits the allocation across live channels.
     │   Per piece, a BRIEF: {channel, archetype/format, source_material,
     │   register, include_cta, notes}
     │                                    ◀── MACHINE GATE: brief completeness
     ▼
  [content-writer]  dispatches on the brief's `channel` to that channel's
     │   writer skill. Draft + critique pass + image/carousel, one run.
     │                                    ◀── MACHINE GATES: voice, format limits
     ▼
  [content-writer]  review loop against the anti-patterns and real
     │   engagement data. Max 2 revision rounds; after round 2 unresolved
     │   concerns are ATTACHED to the draft, visibly, never suppressed.
     ▼
  content/drafts/ → content/ready-to-send/, status: draft
     │   This IS the approval surface. No second inbox is ever created for
     │   content, on any channel.
     │                                    ── GATE M2: the approver approves,
     ▼                                       edits, or rejects
  status: approved → content/approved/
     │   Set by the approver's explicit action and by nothing else. The
     │   frontmatter field is the gate; the folder is only where a human
     │   finds it.
     ▼
  [ship skill]  per channel. At most one piece per channel per publishing
     │   day, oldest approved first, never a burst.
     │                                    ◀── MACHINE GATES: cadence,
     ▼                                         asset readiness
  published → content/shipped/ → read-back verification
     │
     ├──→ voice/samples/{register}.md — the corpus grows by exactly one
     ├──→ proof/ — `used_in` recorded on whatever evidence the piece drew on
     ├──→ performance/ — metrics vs the rolling baseline
     │        ├── outperformer? → follow-up briefs, re-entering at the brief step
     │        └── ICP-matching inbound? → a signal item in inbox/
     ▼
  [campaign-strategist]  channel section
     ▼
  [cmo]  unified weekly report → and next week's allocation brief reads
         exactly this data. The loop closes by construction: nothing the
         pipeline produces terminates without feeding the approver, an
         adjacent department, or the next plan.
```

**Rejections and edits are signal, not noise.** They feed the agents'
notebooks, and an edit *is* the approval — the approver's edited version is
what ships. Weight rejections and edits above approvals when learning from
them; a wave-through says far less than a rewrite.

## Artifacts — every one has a next step

| Artifact | Written by | Lives at | Next step | Advanced by |
|---|---|---|---|---|
| Topic request | a filer | `inbox/requests/` | Drained at planning like any topic-bank entry | The weekly plan run |
| Topic bank entry | campaign-strategist | `content/topic-bank.md` | Selected into a weekly plan, or ages out | The weekly plan run |
| Allocation brief | cmo | the week's plan file, `plan-{YYYY}-W{WW}.md` | Split into per-piece briefs | campaign-strategist, same run |
| Per-piece brief | campaign-strategist | handed to content-writer in-run | A draft | content-writer |
| Draft | content-writer | `content/drafts/` → `content/ready-to-send/` | M2 | The approver, on the approval surface |
| Review verdict | content-writer | the draft's `review:` frontmatter | Travels with the draft to M2 | — (read at M2) |
| Assets | content-writer | `content/images/`, `content/carousels/{slug}/` | Referenced by the draft, revalidated at publish | The ship skill's asset-readiness gate |
| Approved piece | the approver | `content/approved/`, `status: approved` | Published | The channel's ship routine |
| Shipped piece | the ship skill | `content/shipped/` | Terminal as work; becomes a voice sample and a performance row | — |
| Voice sample | the ship skill | `voice/samples/{register}.md` | Read by every future draft in that register | content-writer |
| Performance row | engagement analysis | `performance/` | Feeds the baseline, the channel report, and outperformer detection | campaign-strategist |
| Inbound signal | campaign-strategist | `inbox/` | Read by the approver | — (terminal for now; rewires to a sales department if business-os grows one) |
| Strategy proposal | cmo | `inbox/` | M1 or M3 | The approver |
| Weekly report | cmo | `reports/marketing-{YYYY}-W{WW}.md` | The approver reads it, or doesn't | — (terminal by design) |
| Proof entry | anyone who solved something real | `proof/case-studies/`, `proof/internal/` | Source material for a future piece; `used_in` recorded on use | campaign-strategist at planning |

Two of those are deliberately terminal and one is deliberately a stub. The
weekly report is terminal because a report that generates follow-up work is not
a report. The **inbound signal** is a stub: in the system this was ported from,
ICP-matching replies and DMs routed to a sales agent's inbox and the CMO read
the outcomes back to close the funnel loop. business-os has no sales
department, so the signal lands in the instance inbox where the approver sees
it, and the wiring is one line away if one ever exists. Naming it as a stub is
the honest version; pretending the funnel ends at the DM is not.

## The gates

Marketing has fewer gates than engineering, and that is correct rather than a
gap. Engineering ships code that runs unattended against other people's data; a
bad merge is expensive and quiet. Marketing ships words in public under a name
the business cannot take back; the blast radius is real but singular, and one
human gate per piece covers it completely. More would be ceremony.

**Three human gates. That is the whole ask on the approver's time.**

| Gate | What they're deciding | Raised by | How often |
|---|---|---|---|
| **M1 — Strategy** | Positioning, the ICP, the channel portfolio, adding or retiring a channel | `cmo`, as an inbox proposal with the cost named in the approver's hours | Rare — quarterly, or when evidence demands |
| **M2 — The piece** | Every single piece, before it publishes | The draft itself, on the approval surface | **Recurring — the only gate that is** |
| **M3 — Channel autonomy** | Moving a channel up an autonomy tier | `cmo`, as a proposal. Nobody moves it but the approver | Rare |

**Why M2 is per-piece, stated plainly, because it is the department's largest
single cost in human attention.** An engineering ticket that ships a day late
costs a day. A wrong piece published under the business's own name costs the
credibility the entire department exists to compound — and unlike a bad deploy
there is no rollback, only a deletion that a screenshot outlives. Content is
the one place in this system where speed is worth less than control. Everything
else here is optimised for the approver's absence; this one gate is the reason
that absence is safe.

The CMO **proposes** at M1 and never adopts its own proposal — the same
principle as engineering's "the department cannot commission itself." A channel
is never built silently, and the bar for proposing one is written into the
CMO's config: a distinct format, voice and memory, **and** fully automatable
end to end.

**Five machine gates. The approver is never involved.**

| Gate | Enforced at | Blocks on |
|---|---|---|
| **Brief completeness** | the hand-off from campaign-strategist to content-writer | A missing field in `{channel, archetype/format, source_material, register, include_cta}`. A piece is not drafted from an incomplete brief — a writer that guesses the register produces something plausible and wrong |
| **Voice** | inside the writer skill, before and after drafting | A draft that does not match `voice/guide.md`'s fingerprint. Also where the corpus floor is read: below `voice.floor` samples in the brief's register, the run records the gap on the draft rather than pretending it drafted from evidence |
| **Format limits** | draft time **and again** at publish time | A piece over the channel's hard limit. Revalidated at publish because a limit checked once, hours earlier, against a file since edited, is not a check. On a multi-part format the **whole** piece is validated before the first part goes out, so a limit failure never leaves half a thread live |
| **Cadence** | the ship skill | More than one piece per channel per publishing day, publishing on a non-publishing day, skipping ahead in the queue, or draining a backlog as a burst |
| **Asset readiness** | the ship skill, immediately before publishing | A draft referencing an image, carousel or document that is not on disk. Publishing a text-only version of a piece designed around its visual is a silent quality failure, and the file is either there or it isn't — a machine question |

A machine gate failing means the piece does not publish. **No agent may
override another agent's machine gate.** Only the approver overrides, in a
session, explicitly, and the override is recorded in the instance's decision
log with what was accepted and why.

Two constraints sit *inside* the review pass rather than beside it as gates,
and it's worth knowing which is which. **Naming rules** — which clients, if
any, may be named, and how — are instance config, checked as a critical
failure rather than a style flag. **The critique loop** is craft, capped at two
rounds, with anything unresolved travelling visibly with the draft. Neither is
one of the five, because both are judgements the review pass makes rather than
facts a script can compute, and calling a judgement a machine gate is how gates
become hollow.

**`require_approval` is not a config default that could drift.** The only
publish trigger anywhere in this department is `status: approved` in a piece's
frontmatter, set exclusively by the approver's explicit action. Silence is not
approval, anywhere, ever.

## Channel autonomy tiers

The marketing analogue of engineering's L0–L3 project autonomy. **Autonomy
belongs to the channel, never to the piece.**

- **C0 — observe.** Metrics collected. Nothing drafted, nothing published.
- **C1 — draft.** Drafts generated; no publishing path exists.
- **C2 — approve-to-ship.** Drafts generated and published, one approval per
  piece (M2).
- **C3 — autoship.** Published with no per-piece approval.

**A new channel registers at C1 and moves only when the approver says so
(M3).** C1 is not a resting place: a draft with nowhere to go is the dead-end
pattern this system exists to avoid, so a channel sitting at C1 needs a live
reason and a date.

**The C1/C2 line is capability, not activity.** A channel with a working ship
path whose queue happens to be empty is C2. A channel whose drafts have no
destination is C1. In the port's own history one channel spent exactly one day
at C1 — not as a designed staging period, but because its publishing path broke
underneath it — and moved to C2 the moment the path existed, not when a plan
said it should. A tier is a statement about what a channel can actually do.

**Nothing reaches C3 by accumulating good behaviour.** There is no probation
period that ends in autoship, no streak of clean approvals that earns it.
Moving a channel to C3 is a decision the approver makes explicitly, in the
knowledge that they are giving up the per-piece read — and a department where
no channel ever reaches C3 is a department working exactly as designed.

## A channel is a playbook, not an agent

The department's load-bearing design rule. Adding a channel means:

1. A **playbook file** — `config/channels/{name}.md` in the instance —
   carrying the mechanics: format limits, cadence and the evidence for it, the
   publishing path, what works on this platform, hashtag and mention
   conventions, current baselines.
2. A **registry entry** — `config/config.yaml` → `channels`: the tier, the
   publishing method, the credential's env var name, the weekly numbers.
3. A **writer skill, only if the craft genuinely differs.**

It is **not** a new agent and **not** a new strategy skill.

Strategy is cross-channel by nature. "This quarter's narrative gets three
long-form beats and beat two becomes a thread" is one judgement that no
per-channel component can see. Split strategy per channel and that judgement is
duplicated N times, after which the channels drift out of one narrative — which
is the exact failure a CMO exists to prevent.

**Craft can fork; strategy does not.** The port carries one fork, and it proves
the rule rather than breaking it: thread construction is *procedurally*
different from long-form, not merely stylistically — a hard per-part character
limit that must be counted mechanically, a hook that has to earn a tap rather
than open something already fully visible, and a multi-part arc instead of a
single body. So it is a second writer skill. Both skills take the **same brief
shape**, and the content writer dispatches on the brief's `channel` field. The
strategy layer never knows or cares which skill ran.

The playbook holds mechanics. It never holds what to say, the positioning, or
the week's plan — those live upstream, once.

## The two publishing seams

The port shipped with two live channels, and they are worth keeping in this
document as **examples of the two publishing seams**, because a business
adopting this department will land on one or the other and the operational
costs are completely different.

**Seam one — an API integration.** A published integration called with a token
from the environment. Headless, schedulable anywhere, verifiable by reading the
result back. This is the seam you want, and the one to check for first when
adding a channel. Its constraint is entitlement: the account needs the API
access tier the endpoint requires, and access tiers quietly determine which
metrics come back afterwards.

**Seam two — an authenticated browser session.** The department drives a
logged-in browser the way a person would. In the port this was not a
preference: that platform's API was entitlement-blocked behind pay-per-use
billing on the account in question — an ACTIVE connection returning 401 on
reads and writes and 402 on search, a billing gate no agent can move and no
re-link fixes. Publishing moved to the browser because there was no second
working option.

**The honest cost of the browser seam, stated up front so it isn't discovered
on the first failed run:**

- **No headless path.** It needs a real machine with a real logged-in session.
- **It silently does not run if the machine is asleep.** No error, no alert,
  no partial output — just a publishing day that quietly passes.
- **It cannot re-authenticate.** A dropped session means the run stops and logs
  `not_logged_in` rather than guessing.
- **It cannot live on a server** alongside the department's other scheduled
  work, which means one channel's publishing is on a different host from the
  rest of the department, and that split has to be written down somewhere
  someone will read.

What it buys is a zero-cost, non-metered publishing path, and — for multi-part
formats — genuine atomicity plus a read-back check stronger than the API's,
because it confirms the piece as *rendered* rather than as a returned
identifier. That is a real trade, not a workaround. Just make it knowingly, and
put the costs in the channel's playbook.

**Verification is read-back, never the absence of an error.** Where read-back
is genuinely impossible, the playbook says so explicitly and says what is
checked instead, and the publish is recorded as unverified. A publish nobody
confirmed is not a publish that happened.

## The voice seam

Everything this department publishes goes out in the *business's* voice,
calibrated from two files: `voice/guide.md` (words to use, words never to use,
the fingerprint) and `voice/samples/{register}.md` (real published pieces, one
file per register).

**A fresh instance starts with an empty corpus, and that is not a failure
state.** It is the honest starting position for a business that has not
published yet, and the department is designed around it rather than blocked by
it. This is the one place the port could not simply carry the original across:
`life-os` read one person's identity store for every draft, and a person is not
a business.

**The corpus grows by publishing.** Every piece the approver approves and
publishes is, by definition, a piece in the business's voice — so it becomes a
sample in its register. That is the intended path from empty to calibrated, and
it has a useful property: the corpus can only ever contain material the
approver already stood behind.

**The floor is 10 samples per register.** Below it, drafting still happens —
the department does not refuse to work because a business is new. What changes
is where the weight sits: the review pass and M2 carry more of it, the gap is
recorded on the draft rather than discovered later, and the instance config
makes the number visible. Raising the floor, or gating on it outright, is the
approver's call.

**Seed from real published material, never from a description.** Posts,
articles, talks, anything already public and already approved of. And seed
*per register* — a channel's samples must be that channel's register, because
what is being calibrated is rhythm and shape, not opinions. Long-form samples
teach a thread nothing except how to be too long.

## The proof seam

The department does not invent things to say. Its source material is evidence,
split by one question: **is there a client on the other end of it?**

- **`proof/case-studies/`** — a named or anonymised client, a real business
  problem, and a **measured** outcome. All three required. Missing any one, it
  is not a case study.
- **`proof/internal/`** — the same shape with no client: the business's own
  technical or strategic work. Still real proof of capability.
- **`../engineering/reports/proof/`** — **read-only here.** The engineering
  department writes a proof entry when it ships something genuinely
  interesting.

That third source is a loose end this port ties off.
`departments/engineering/config/conventions.yaml` declared `reports/proof/`
with the note that it "rewires to a marketing department if one exists." One
now does. The direction is one-way and stays that way: **engineering owns what
it built; marketing owns what gets said about it.** A marketing pass that
edited an engineering proof entry would be editing another department's record
of its own work.

Getting the case-study/internal split wrong is what turns an evidence library
into a claims library, so when in doubt it is internal proof.

**When a proof entry is used in a published piece, record it on the entry.**
Proof reused silently across three pieces reads as one story told three times —
which is the failure the `used_in` field exists to prevent, and the reason it
is a field rather than a convention.

## Rhythm

| Routine | Cadence | What |
|---|---|---|
| `mkt_weekly_plan` | Weekly, plus a catch-up fire the next day | The engine. CMO allocation → per-piece briefs → drafts → reviewed drafts on the approval surface → the unified weekly report |
| `ship_content` | **Daily**, publishes on the channel's publishing days | Publishes the single oldest approved piece for the API-seam channel |
| `ship_content_x` | **Daily**, publishes on the channel's publishing days | The same, for the browser-seam channel |
| engagement collection | Daily | Reads the numbers back for shipped pieces and writes `performance/`. **No routine ported** — every platform's collection path differs, and the port's ran behind an authenticated browser session |
| outperformer interrupt | Designed, unwired | Watches for a piece well above baseline early and briefs follow-ups |
| positioning audit | Designed, unwired | Scores recent shipped pieces against the positioning statement |

**What never runs on its own:** the content writer (it is invoked, never
scheduled), any strategy change (M1 is a proposal, not a routine), any autonomy
change (M3, same), and anything at all while `MODE` is set to a halt value.

**The ship routines fire daily and the skill gates the days.** Both of them,
whatever the channel's cadence is. The reasoning is in
`schedules/ship_content_x.md` and it is the more useful half of that file:
cadence becomes a **config value** rather than scheduler configuration, so
changing it is a one-line edit with nothing to reconfigure — and one prompt
cannot drift the way three copies of it can. Four quiet no-ops in a week is the
design working, not a routine misfiring.

**The weekly plan's catch-up is a backstop, not a second run.** The primary run
can silently die — a halt mode, a sleeping machine, a crash partway through the
chain — and without a backstop there is no recovery for a full week. The
catch-up fires the same routine a day later and the *agent* decides whether the
primary actually completed. Cron fires things on a timer; agents decide. The
completion check is drafts-based and looks in both `content/drafts/` and
`content/shipped/`, because a one-piece week's only draft may have already
published before the check runs — checking `drafts/` alone would false-negative
and double the week's output.

## What the department will not do

- **Publish without per-piece approval,** on any channel below C3. `status:
  approved`, set by the approver's explicit action, is the only publish trigger
  in existence. Silence is never approval.
- **Commission its own strategy.** The CMO proposes portfolio and positioning
  changes with the cost named in the approver's hours; it never adopts its own
  proposal. The campaign strategist executes greenlit channels and proposes
  none. The content writer has no opinions about strategy at all, on purpose.
- **Invent a metric.** A baseline that has not been measured says "unknown" and
  means it. A case study without a measured outcome is `status: pending`, not
  proof. Inventing a plausible number is the single fastest way to make an
  evidence library worthless.
- **Manufacture urgency about content.** A missed slot is a missed slot. The
  allocation brief and the default mixes are ceilings shaped by judgement, not
  quotas — nobody fills the calendar because it is planning day, and a quiet
  week with one right piece beats a loud week of motion.
- **Add a recurring manual step for the approver.** Written into all three
  agent files independently, because it is the constraint most likely to be
  eroded one convenience at a time.
- **Chase engagement over positioning.** Impressions are a proxy. Forty
  impressions from three buyers in the ICP beats four thousand from peers.
- **Delete published content.** Not to fix a duplicate, not to fix a typo. That
  is the approver's call and the approver's hands. The department flags it.

## What genuinely isn't there yet

Honest, because a department that can't say this isn't trustworthy.

- **A new instance has no voice corpus and no baselines.** Both are unavoidable
  — they are earned by publishing — but they mean the first several weeks are
  calibration, not optimisation. Treat early pieces as ones that deserve a
  closer read at M2, and resist the urge to fill the baseline fields with
  platform-wide averages, which is exactly how a benchmark hardens into a
  "fact" about an account that has never posted.
- **The browser publishing seam has no headless path and no failure alarm.** It
  needs a live session on a machine that is awake. If either is false it does
  not run and does not say so — the first signal is a publishing day that
  passed with an approved piece still sitting in the queue. That gap is real,
  it is called out in `schedules/ship_content_x.md`, and closing it needs
  something outside this department watching for the silence.
- **Attribution from content to pipeline is thin, everywhere.** Platform APIs
  ration metrics by access tier; some do not expose impressions at all, some
  return untrustworthy zeros. The CMO's job is to *name* the gap in the report
  rather than pretend the funnel ends at the reply — but naming a gap is not
  closing it.
- **There is no destination for an inbound signal.** It lands in `inbox/` for
  the approver. If business-os grows a sales department, this rewires in one
  line; until then the funnel loop's second half is a human reading an inbox.
- **No engagement collection routine shipped with this port.** The pipeline
  depends on it — baselines, outperformer detection, the review pass's
  evidence and the CMO's weekly read all consume `performance/` — and nothing
  writes to it until an instance builds a collector for its own channels.
  Until then the baselines stay `unknown`, which is correct behaviour rather
  than a to-do someone forgot, and the review pass runs on the voice guide and
  the anti-patterns alone.
- **The interrupt check and the positioning audit are designed, not wired.**
  They run when invoked. Outperformer detection and positioning drift currently
  happen when a run happens to look, which on a quiet week is not at all.
- **No paid, no performance marketing, no SEO.** Deliberately scoped out in the
  original and not added here. The department is organic-only, and that is a
  decision rather than an oversight — but it means "marketing" here means
  "publishing", and a business whose growth genuinely depends on paid
  acquisition needs something this department is not.

## Relationship to the rest of business-os

- **Engineering** feeds the proof seam. Shipped tickets that were genuinely
  interesting become entries in `../engineering/reports/proof/`, which this
  department reads at planning time and never writes to. The two departments
  meet at exactly that directory and at
  `../knowledge/business-profile.md` — one description of the business, shared,
  rather than two that drift.
- **The approver** appears in exactly two places: the weekly report, and M2 on
  each piece. M1 and M3 exist but are rare by construction.
- **The notify seam** (`lib/mkt-notify.sh`) is how anything reaches the
  approver. The department never formats for a specific channel — it hands the
  script a mode and an item path, and the instance's config decides where that
  goes and how a reply comes back. Same seam, same script contract, as
  engineering's.
- **Approvals arrive wherever the approver is.** However many surfaces an
  instance wires up, they all set the same `status: approved` on the same file.
  One approval surface with several doors — never several surfaces.
