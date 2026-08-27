---
ticket: ENG-003
project: config-site-builder
status: rejected
size: M
author: product-manager
created: 2026-08-25
decided: 2026-08-26
---

# Untrack `.env` from config-site-builder and close related env-hygiene gaps

## Readback

**You said:** "`.env` is tracked in config-site-builder and unignored in
aiorders-admin-hub... The Google Maps key is the one worth an actual look: it
is billable, and if it carries no HTTP-referrer restriction in Google Cloud
it can be lifted from the bundle and spent by anyone... What this asks for:
[1] Check whether the Google Maps key is referrer-restricted... [2] Get
`.env` out of tracking in config-site-builder and add `.env` to both repos'
`.gitignore`, with a committed `.env.example`... [3] Decide whether rotation
is warranted... Also minor, same family: `restaurant-marketplace/.claude/projects/`
is untracked Claude session data with no `.gitignore` entry."
(`inbox/requests/2026-08-23-aiorders-env-hygiene.md`, filed by Harry, 2026-08-23)

**Understood as:** Three separable pieces, in the priority order you gave
them. (1) The one item with a live dollar cost — whether the Google Maps key
can be spent by anyone who pulls it out of the public bundle — needs an
answer, but that answer lives in the Google Cloud Console, not in a git repo
the department can reach. (2) `config-site-builder`'s tracked `.env` stops
being tracked going forward, both repos get a real `.gitignore` entry, and a
committed `.env.example` replaces the tribal knowledge of what variables
exist. (3) Rotation is a decision that waits on (1)'s answer, and — like (1)
— is itself a console operation, not a code change.

Two independent readings were run on the raw request — this PM's and, blind
to it, the architect's (an independent subagent, given only the raw request,
the business profile, and the relevant registry rows — no PM interpretation).
They agreed on all three pieces and on the core structural point that decided
how this ticket is scoped: **checking or restricting the Maps key, and
rotating anything, both require Google Cloud / Supabase console access that
nothing in this department's configuration shows it has.** Nothing in
`config/projects.md`, `config/conventions.yaml`, or anywhere else names a GCP
credential, a service account, or any console-level access — every
registered project's autonomy (L1: branch, PR, human merge) describes *git*
access only. The architect's reading additionally sharpened two things this
PM's first pass under-weighted: that "get `.env` out of tracking" has two
very different possible meanings (removing it going forward vs. rewriting
history to remove it from every past commit) with very different blast
radius, and that the second of those is structurally incompatible with the
L1 branch-and-PR model this department actually operates under (a PR is a
diff against a stable base; it cannot rewrite the base itself). No material
divergence on scope or problem — that sharper framing is simply what this
PRD uses.

**Requirements, tagged by where they came from:**
1. `[stated]` Determine whether the Google Maps API key carries an
   HTTP-referrer restriction, and restrict it if not.
2. `[stated]` `config-site-builder/.env` stops being tracked in git; both
   `config-site-builder` and `aiorders-admin-hub` get a `.gitignore` entry
   for `.env`; each gets a committed `.env.example` naming its real
   variables.
3. `[stated]` Decide whether the Supabase anon key and/or the Maps key
   should be rotated, informed by (1)'s answer.
4. `[stated]` `restaurant-marketplace/.claude/projects/` gets a `.gitignore`
   entry for untracked Claude session data.
5. `[inferred]` "Get `.env` out of tracking" means stop tracking it at the
   tip going forward (`git rm --cached` + `.gitignore`), not rewrite git
   history — both readings agree the values are already public-by-design in
   the shipped Vite bundle regardless of git tracking, so a disruptive
   history rewrite buys little marginal safety for a real cost (force-push,
   every clone invalidated, incompatible with the L1 PR model). If literal
   history scrubbing is actually wanted, that's a materially different,
   larger, and riskier piece of work than what's scoped here.
6. `[proposed]` The uncommitted `VITE_BRAND_ID` repoint in
   `config-site-builder/.env` is left exactly as it is in the (now-ignored)
   working file — not committed, not reverted, not treated as a new default
   — since the request explicitly reads it as one developer's local target
   rather than a decision this ticket should make.

**Assumed, and worth correcting if wrong:**
- That the department genuinely has no Google Cloud Console / Supabase
  dashboard access — this PRD couldn't find any credential or connection for
  either anywhere in the department's config. If that's wrong and the
  department does have a way to check/restrict/rotate these, say so and this
  ticket's scope grows to include it directly instead of handing it back.
- That "get `.env` out of tracking" means tip-only, not a history rewrite
  (see requirement 5). This is the single biggest scope fork in this ticket
  — if the history should be scrubbed, that needs to be said explicitly,
  because it changes this from a one-PR chore into a coordinated, disruptive
  operation.
- That `aiorders-admin-hub/.env`'s actual variable names (needed for its
  `.env.example`) can be read directly off that untracked file when this
  ticket is built — the request never lists them, and no reading here can
  see an untracked file's contents in advance.
- That rotation, if warranted, is a decision to make here but not
  necessarily to execute in the same ticket — executing it is another
  console operation this department may not be able to reach either.

## Problem

Two AIOrders repos have live credentials sitting somewhere they shouldn't be
by convention: `config-site-builder/.env` (holding a Supabase URL, a Supabase
anon key, and a Google Maps API key) is committed to git history, and neither
repo's `.gitignore` mentions `.env` at all, so `aiorders-admin-hub`'s own
untracked `.env` is one `git add -A` away from joining it. Separately, and
not really a git problem at all: the Google Maps key is billable, and if
Google Cloud has no HTTP-referrer restriction on it, anyone who opens the
browser bundle (trivial — these are public-by-design client-side variables)
can lift it and run up a bill on Harry's account. Found by Harry while
committing the AIOrders working trees on 2026-08-23, not by any systematic
audit — no AIOrders repo has been swept for this pattern beyond the three
named here.

## Why now

The Maps key exposure, if real, is a live and ongoing cost risk that doesn't
improve by waiting — every day it's unrestricted is another day it's
spendable by whoever finds it. The git-tracking issue doesn't get worse by
waiting in the same way (the values are already public in the shipped bundle
regardless), but it is an active footgun: `config-site-builder/.env`
currently has an uncommitted edit sitting in the same file, one accidental
`git add -A` away from becoming the new tracked default for everyone.

## Users

Not user-facing. This protects AIOrders' own cloud billing and repo hygiene,
and the `.env.example`s specifically help whoever next sets up either repo's
local environment.

## Proposed change

For `config-site-builder`: remove `.env` from git tracking going forward (not
from history), add `.env` to `.gitignore`, and add a committed `.env.example`
listing its real variable names with placeholder values. For
`aiorders-admin-hub`: add `.env` to `.gitignore` (it's already untracked) and
add its own `.env.example` once its real variable names are confirmed by
reading the file directly. For `restaurant-marketplace`: add a `.gitignore`
entry for `.claude/projects/`. Separately, and explicitly flagged back to
Harry rather than attempted: check the Google Maps key's HTTP-referrer
restriction in Google Cloud Console, restrict it if it's open, and decide on
rotation once that's known — none of which this ticket's execution can do
without console access this department doesn't have.

## Acceptance criteria

1. `[stated]` Given `config-site-builder`'s repo after this ships, when
   `git ls-files` is run, then `.env` is not among the tracked files, and
   `.gitignore` lists `.env`.
2. `[stated]` Given `config-site-builder` after this ships, when a fresh
   clone is set up, then a committed `.env.example` names every real
   variable the app needs (at minimum `VITE_SUPABASE_URL`,
   `VITE_SUPABASE_ANON_KEY`, `VITE_GOOGLE_MAPS_API_KEY`, `VITE_BRAND_ID`)
   with placeholder values, not live ones.
3. `[stated]` Given `aiorders-admin-hub` after this ships, when `.gitignore`
   is read, then it lists `.env`, and a committed `.env.example` names that
   repo's real variables (read from the actual file at build time, not
   guessed here).
4. `[stated]` Given `restaurant-marketplace` after this ships, when
   `.gitignore` is read, then it lists `.claude/projects/`.
5. `[stated]` Given this ticket reaches the approver again (at `verified` or
   sooner), then the readback above — "check the Maps key restriction,
   decide on rotation" — has been put back in front of them as an explicit
   action item they need to take themselves, not silently dropped.
6. `[inferred]` Given `config-site-builder`'s uncommitted `VITE_BRAND_ID`
   change, when this ticket's changes are made, then that local edit is
   neither committed nor discarded by this work.

## Non-goals

- Does not check, restrict, or rotate the Google Maps API key, the Supabase
  anon key, or any other cloud-console-side credential — this department has
  no evidence of Google Cloud Console or Supabase dashboard access anywhere
  in its configuration. That work is named explicitly as the approver's own
  action item, not silently dropped.
- Does not rewrite `config-site-builder`'s git history to remove the secret
  values from old commits. The values are already public-by-design in every
  shipped bundle regardless of git tracking, so a history rewrite
  (force-push, every clone invalidated) buys little marginal safety for real
  disruption, and it's structurally awkward under this department's L1
  branch-and-PR model. If literal history scrubbing is actually wanted,
  that's a separate, explicitly-scoped decision, not an assumed part of this
  ticket.
- Does not touch the uncommitted `VITE_BRAND_ID` repoint in
  `config-site-builder/.env` — left exactly as-is.
- Does not add any `.env`/secret hygiene to `aiorders-api` or
  `restaurant-portal` — not flagged in the source request, and out of scope
  here.
- Does not add pre-commit secret-scanning or any preventative tooling — this
  ticket is remedial for the three repos named, not a systemic fix for the
  underlying gap that let this happen unnoticed.

## Risks and unknowns

- Whether Cloudflare's own build/deploy configuration for `config-site-builder`
  and `aiorders-admin-hub` already sources these variables independently of
  the committed `.env` file, or will need Cloudflare-side environment
  variables configured as a prerequisite to safely untracking. Worth checking
  at `building`, before the untrack lands, so a deploy doesn't silently lose
  its config.
- `aiorders-admin-hub/.env`'s real variable list is unknown until read
  directly — this PRD can't name it.
- Whether this ticket's three-repo scope needs three separate branches/PRs
  under one ticket ID, since `config/templates/ticket.md` models
  `branch:`/`links.pr` as singular — flagged as an observation
  (`agents/eng-manager/observations.md`, 2026-08-25) for whoever picks this
  up at `building` to resolve, not decided here.
- Whether the Maps key is, in fact, unrestricted — genuinely unknown; this
  PRD can't check it, which is exactly why it's named as an approver action
  item rather than an assumption either way.

## Cost

- Build: M — three repos touched (one with an actual `git rm --cached` +
  history-tip change, two with a one-line `.gitignore` addition each), two
  new `.env.example` files, no new runtime dependency.
- Run: $0/month — a `.gitignore` and an example file are dev-time only. (The
  Maps key's *existing* cost exposure, if any, isn't created by this ticket
  — it already exists and isn't resolved by this ticket either, since that
  piece is out of the department's reach.)

## Decision

G1 raised 2026-08-25, notified 2026-08-25T13:55:41, nudged 2026-08-26T15:43:45
(24h with no reply) — see `inbox/2026-08-25-eng003-g1-scope.md`, now
`inbox/_handled/`.

- **The approver's answer:** rejected — killed at G1, nothing built.
- **Date:** 2026-08-26T23:38:51.515614-07:00 (2026-08-27T06:38:51.515614+00:00)
- **Notes:** "Drop this ticket do not  need to be done" — verbatim, the only
  reason given. Answered by directly hand-editing the gate item file
  (frontmatter `decision:`/`decided:` set, a second `## Decision` section
  appended below the still-blank original placeholder) rather than through
  `lib/eng-notify.sh`'s reply channel — fourth such occurrence today,
  after `ENG-002`'s GitHub merge, `ENG-001`'s G3, and `ENG-004`'s G1 (all in
  `agents/eng-manager/config/decision-journal.md`). First outright G1
  rejection this department has recorded — every prior G1 (`ENG-002`,
  `ENG-004`) was approved as scoped. No `## Dissent` section —
  `agents/critic/agent.md`, which `skills/prd-writer/SKILL.md` step 8b calls
  for before every G1, doesn't exist at the department or instance level.
  Already filed as a proposal (`agents/eng-manager/proposals.md`, 2026-08-25,
  from `ENG-002`'s pass) — not refiled here.
