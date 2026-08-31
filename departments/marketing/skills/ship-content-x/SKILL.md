# Skill: ship-content-x

**Owner:** shared — runs on its own routine; the campaign strategist does not
invoke it, it reads its output for the channel report
**Model:** small for selection and validation (rule checks) — escalating to
reasoning for the composer drive and the read-back, which are judgment
**Trigger:** a daily routine on a machine with a live logged-in browser session.
It fires **every day**; step 1 gates it to the channel's publishing days and
no-ops otherwise. Also callable with an explicit path when a piece is approved
out of band.
**Suppressed when:** `MODE` is `sabbath`, `retreat` or `quiet`; publishing (only)
is suppressed when `MKT_PUBLISH_FREEZE` is set.

---

## Paths

Bare paths are **instance-relative** (`$MKT_INSTANCE`). Paths prefixed
`$MKT_DEPT` are template-side and read-only at runtime.

---

## Why this is a separate skill, not an extension of `ship-content`

The obvious move — teach `ship-content` a second channel — was considered and
rejected. `ship-content` is several hundred lines of long-form machinery: design
tool export/poll/download, markdown→Unicode conversion, a document-post route
with a multi-image fallback, and a channel on which read-back is impossible.
This channel uses none of it, and needs machinery the long-form path has no
analogue for: a native thread composer driven through a real browser, weighted
per-tweet character revalidation, quarantine on partial publication, and a
genuine read-back of the rendered timeline. Folding both into one file would make
the shared quarter unreadable and the divergent three-quarters
conditional-heavy.

**What the two share is the stance, not the code**: the approval gate, the daily
cap, oldest-first backlog drain, and the never-re-ask rule are duplicated here
deliberately and must stay in sync in spirit. Neither skill touches the other's
queue — not to ship, not to defer, not to count against the other's cap. The
caps are independent: a long-form post today does not block a thread today.

---

## Purpose

Publish one approved short-form piece per eligible day — a single tweet or a
thread — through an authenticated browser session, and verify it by looking at
the result.

Media is out of scope: this path ships text-only, matching the writer skill
upstream, which produces no image pass.

---

## The publishing path is a browser session, not an API

This is **this instance's binding of the `publishing.methods.browser` seam** in
`config/conventions.yaml`, not a universal fact about the platform. It is
recorded here because the reasoning transfers to any channel whose API turns out
to be entitlement-gated.

The API path was checked, on 2026-08-29, against a live connection whose OAuth
token was valid and whose status read ACTIVE: reads returned 401, writes returned
401 *before* the platform even evaluated the content, and search returned **402
Payment Required**. The token was real; the app behind it carried no API
entitlement, and under the platform's pay-per-use pricing that is a **billing
gate, not a scope problem**. Re-linking does not change it. An instance whose
account does hold the entitlement should bind `publishing.methods.api` instead
and can delete most of steps 4 and 6 — but should keep step 3.

What the browser path gives instead, and it is not a consolation prize:

- **Atomic threads.** The native composer takes every tweet of the thread in one
  modal and publishes the chain in a single action. A thread either lands whole
  or not at all.
- **Real verification.** Publication is confirmed by reading the rendered
  timeline, not by trusting a returned identifier. Stronger than any API check
  available on any channel in this department.
- **No metered spend.** Zero per-post cost.

**The honest cost, and it is real:** this cannot run headless. It needs a live,
logged-in browser session on a machine that is awake, which makes it materially
less robust than a container cron — if the machine is asleep or the session has
dropped, the run silently does not happen. That belongs in the channel's
playbook, not discovered on the first missed day. The trade was not a choice
between two working options: the API returned 401/402 on every call.

---

## Why a thread must publish atomically

**Use the native thread composer. Do not chain replies.**

Chaining — publish tweet 1, then reply to it with tweet 2, and so on — fails
catastrophically in the middle. A rejection at tweet 5 of 8 leaves a **truncated
thread live on a public timeline** with no clean recovery: the system does not
delete published content (that is the approver's call and the approver's hands),
and re-running duplicates tweets 1–4. A validation bug becomes a visible incident
requiring human cleanup.

The composer takes the whole thread in one modal and publishes it in one action,
so there is no half-published state to clean up. That single property is why this
skill's failure handling is short and why almost all of it lives *before* the
publish click.

---

## The gate: `status: approved`, and nothing else

Same rule as `ship-content`, verbatim in intent. **`status: approved` in the
frontmatter is the gate; the folder is not.** The approver's M2 approval already
happened; that approval *is* the confirmation.

**Publish immediately. Never re-ask.** This runs unattended and a question means
the piece silently does not ship. Two valid endings only: publish, or stop with a
named stop code.

**One approval covers the whole thread.** Per-tweet re-confirmation does not exist
and must not be invented.

`status: needs_attention` is the other side of the same gate — see step 6.

---

## Config keys read (every run, never cached, never hardcoded)

From the instance's `config/config.yaml`:

| Key | Use |
|---|---|
| `channels.{channel}.enabled` | false → `channel_disabled` |
| `channels.{channel}.autonomy` | `c0`/`c1` → `channel_autonomy_too_low` |
| `channels.{channel}.publishing_days` | the cadence — a list of weekday names |
| `channels.{channel}.method` | expected `browser` for this binding |
| `channels.{channel}.handle` | the account this must be logged in as, and the URL base for read-back |
| `channels.{channel}.limits.weighted_chars` | the per-tweet hard limit (280 on the source platform) |
| `channels.{channel}.limits.url_weight` | fixed weight of any URL (23 on the source platform) |
| `approval_surface.close_command` | optional; step 9 |

The session credential is the browser profile itself and never appears in config.
Any token-based key is referenced **by env var name**; values are never written to
a trace, frontmatter, or log line.

**Cadence lives in config.** Never hardcode a day list here. The source instance
publishes Tue/Wed/Thu, on the finding that two independent large-scale datasets
(one ~2B engagements across 307K profiles, one 8.7M posts) both put mid-week
mornings at the top and Friday/Saturday at the bottom — but that is *evidence for
a config value*, recorded in the channel playbook, not a rule to bake into a
skill. The scheduler cannot express three specific weekdays: it offers "daily" or
one fixed weekday. So the routine fires daily and **step 1 is the schedule**. The
four no-op days a week are the design working. The payoff is that changing
cadence — adding a day, dropping to two — is a one-line config edit with nothing
to reconfigure in the scheduler.

A channel with no engagement history of its own has no account-specific baseline
to override a general finding. When it has one, revisit the config with the
approver; do not let the cadence drift silently.

---

## Inputs

- The channel's queue: `content/approved/`, `content/ready-to-send/`,
  `content/drafts/`
- `content/shipped/` — to enforce today's cap
- `config/config.yaml`, `config/channels/{channel}.md`
- `.env` → `MODE`, `MKT_PUBLISH_FREEZE`
- Optionally, one explicit piece path from a caller

### Frontmatter this skill dispatches on

The contract is `$MKT_DEPT/skills/x-content-writer/SKILL.md` § Draft
frontmatter. This skill reads a subset of it and adds one state.

| Field | Required | Meaning |
|---|---|---|
| `kind` | yes | `content-draft` |
| `channel` | yes | scopes the queue. This skill touches only its own channel's pieces |
| `status` | yes | `approved` is the gate. The writer's enum is `draft \| ready-to-send \| approved \| shipped`; **this skill adds `needs_attention`**, which is never selectable |
| `format` | yes | `tweet` (a single standalone tweet) \| `thread` |
| filename `{YYYY-MM-DD}` prefix | yes | the **planned** publish date — the selection key |
| `planned_date` | yes | already written by the writer, equal to the filename date. Preserved, not recomputed |
| `tweet_count` | no | cross-checked against the parsed list; a mismatch is `draft_unparseable` |
| `weighted_chars` | no | the writer's per-tweet counts. **Informational here** — step 3 recomputes |

From the body:

| Key | Required | Meaning |
|---|---|---|
| `tweets` | yes | the ordered list: `{ n, text, weighted_chars }`. `format: tweet` has exactly one entry. **This is what gets posted** |
| `hook_tweet` | yes | identical to `tweets[0].text`; used for read-back matching |
| `full_text` | no | the thread rendered with `n/total` numbering, **for human review only**. **Never post `full_text`.** It carries numbering the tweets deliberately do not, and posting it would publish the review artifact instead of the piece |

Written back: `status: shipped`, `shipped_at`, `post_ids` (ordered), `post_url`,
`publish_verified`. On quarantine: `status: needs_attention`,
`attention_reason`, `attempted_at`, and whatever `post_ids` were confirmed live.

---

## Steps

### 1. Mode, freeze, day, cap, selection

1. **`MODE`** is `sabbath`/`retreat`/`quiet` → exit silently, `mode_halt`.
2. **`MKT_PUBLISH_FREEZE`** set → stop, `publish_freeze`. Blocks publishing only:
   drafting, review and M2 keep running, approved pieces queue in
   `content/approved/` and drain oldest-first when the freeze lifts, one per
   publishing day, **never as a burst**.
3. **Day of week, computed fresh** — `date +%A`, lowercased. **Never trust a
   stored label.** Not in `channels.{channel}.publishing_days` → stop,
   `non_publishing_day`, logged quietly. The backlog does not advance on a
   non-publishing day and no slot is lost.
4. **Today's cap.** Scan `content/shipped/` for a file with this `channel` and
   `shipped_at` dated today → stop, `already_shipped_today`. The guard is the
   calendar day, not the run: it holds for a manual retry, a second cron fire, or
   a hand-off from the approval surface. **A thread is ONE piece** regardless of
   how many tweets it contains — an 8-tweet thread does not consume 8 days of
   quota, and shipping a thread does not permit shipping a standalone tweet the
   same day.
5. **Select.** Files with this `channel`, `status: approved`, filename date today
   or earlier. Sort ascending by filename date, take **the single oldest**, log
   the rest as `deferred_backlog`. Never skip ahead.

   **Selection reads `status: approved` only.** A piece at
   `status: needs_attention` is deliberately unselectable — some or all of its
   tweets may already be live, and re-selecting it would re-post the thread from
   tweet 1, duplicating live posts on a public timeline. The queue moves past it
   to the next-oldest. Only the approver clears it.

   This oldest-first rule is inherited, not rediscovered: on the long-form
   channel, 2026-07-16, three backlogged approved posts went out in one run and
   had to be deleted by hand. This channel gets the rule on day one instead of
   learning it the same way.

An explicit path from a caller skips step 5 only — 1 through 4 still run. A
just-approved piece must not ship on a non-publishing day or after something
already went out today.

`status` not `approved` → stop, `status_not_approved`.

### 2. Parse the piece

Read the ordered `tweets` list from the body — `n`, `text`, `weighted_chars` for
each. `format: tweet` has exactly one entry. Cross-check the count against
`tweet_count` where the writer supplied it.

**Post `tweets[]`, never `full_text`.** `full_text` exists so a human can read the
thread as one document before approving; it carries `n/total` numbering that the
tweets deliberately do not.

**A malformed or unparseable list is a hard stop.** Log `draft_unparseable` with
what specifically failed, notify, publish nothing. **Never "post what we could
parse"** — a half-thread on a public timeline is worse than no thread, and unlike
a failed run there is no clean recovery from it. If the parse is broken the fix
happens in the piece file, not in a best-effort publish.

### 3. Pre-flight: weighted length of every tweet, before any tweet posts

**This is the single most important rule in this file.** Recompute each tweet's
**weighted** length from scratch:

- Any `http(s)://` URL substring counts as exactly **`limits.url_weight`** (23 on
  the source platform), **regardless of its literal length** — the platform wraps
  every link through a fixed-length shortener, so a 200-character URL and a
  30-character URL cost the same.
- **Emoji and CJK characters weigh 2 each.**
- Everything else — Latin text, digits, common punctuation — weighs 1.
- When unsure whether a character is light or heavy, **count it as 2.** An
  undercount publishes a broken thread; an overcount blocks a valid one, which is
  recoverable.

**Recompute; do not read `weighted_chars` off the draft.** The writer computes the
same weighted count, so this is usually a confirmation rather than a correction —
that is the point. A stored count is a record of the text *at the moment it was
written*, and between then and now the piece passed a reviewer, possibly a
revision pass, and a human at M2, any of which can edit the text without
recomputing the number. **This is the last gate before an irreversible public
action**, so it measures the bytes that are about to be posted, not a number
someone recorded about an earlier version. A mismatch between the stored count
and this one is worth recording in the trace: it means something edited the text
downstream of the writer.

Any tweet over `limits.weighted_chars` → **stop and publish nothing.** Log
`tweet_over_limit` with the offending index, its stored count, and its recomputed
count. Notify. Do not truncate, do not cut words, do not skip the offending tweet
and post the rest.

Why validate everything up front rather than letting the platform catch it: the
alternative is discovering the problem at tweet 5 of 8. Even with an atomic
composer, a rejection surfaced late costs a run; with any non-atomic path it
converts a validation bug into a public, human-cleanup incident. Validate the
whole thread on the ground.

### 4. Drive the composer

**Preflight the session.** Open the composer and confirm it is logged in **as the
handle in `channels.{channel}.handle`**. Session absent → stop, `not_logged_in`.
Logged in as anything else → stop, `wrong_account`. **Publishing as the wrong
account is not recoverable** and it is the one mistake here that cannot be
undone by anyone.

The composer's elements are identified by stable test ids on the source platform
— composer URL, the box for tweet *n*, the "add another box" control, the publish
button, and the account indicator used for the logged-in check. Record the exact
selectors in `config/channels/{channel}.md`, not here: they are the instance's
binding and they change when the platform's UI does. Verified working 2026-08-29
against the live composer.

**Text insertion — two traps, both hit during verification, both must be
handled:**

- **The editor is rich-text and ignores synthetic keystrokes.** A plain "type"
  action does nothing to it. The reliable method is to focus the box and use
  `document.execCommand('insertText', false, text)`.
- **Insert APPENDS, it does not replace.** Collapsing the range to the end and
  inserting produced `TEXT ONETEXT ONE` on a re-run. **Clear the box first** —
  select its full contents and `execCommand('delete')` — *then* insert, then read
  the box back and assert it equals the intended text exactly. Never trust the
  insert blind.
- **An empty box gets silently deleted.** A box that is added but not filled
  disappears on its own. So **fill each box immediately after adding it**, and
  re-count the boxes before publishing.

**Procedure.** Fill box 0. For each remaining tweet, click "add" and fill the new
box immediately. When every box is filled, read all boxes back and assert two
things: the box count equals the tweet count, and each box's text matches its tweet
exactly. **Only then** click publish. Any mismatch at this point → stop **without
publishing**; the piece is untouched and the next run retries cleanly, which is
the whole benefit of the composer being atomic.

### 5. Failure handling

Short, because atomicity does most of the work.

- **Anything fails before the publish click** — not logged in, wrong account, a
  box that will not take text, a read-back mismatch across boxes: stop, publish
  nothing, leave the piece exactly as it is at `status: approved`. Log the
  specific reason. The next run retries from scratch with no residue, because
  nothing reached the timeline.
- **The publish click fails, or the page errors:** **do not click publish a second
  time** on the assumption it did not land. Go to step 6 and *look* first. A
  second click after a slow-but-successful publish posts the thread twice, and
  duplicate threads on a public timeline are the approver's to clean up, not the
  system's.
- **Never delete a published tweet.** Not to fix a duplicate, not to fix a typo.
  The system does not delete published content — that is the approver's call and
  the approver's hands. Flag it instead.

### 6. Read-back — by looking at the rendered timeline

Navigate to the account's own timeline (`handle` from config) and read the top of
it. This confirms the thread as **rendered**, not as a returned identifier — a
genuinely stronger check than any API offered here.

Confirm the hook's text appears as the most recent post and that the thread shows
the expected number of parts. Capture each part's status URL/id.

| `publish_verified` | Condition | Action |
|---|---|---|
| `timeline_confirmed` | visibly live, expected part count | the only value that ever reaches `content/shipped/` |
| `timeline_partial` | live, but the visible part count is wrong | **quarantine** (below) |
| `timeline_absent` | nothing new on the timeline | treat as **not published**: leave at `status: approved` so the next run retries. Do not mark shipped |
| `readback_failed` | the timeline could not be read at all — page error, session dropped | the publish may or may not have landed. Do **not** retry and do **not** mark shipped: **quarantine.** Guessing in either direction is worse than stopping |

Why this step is not optional: on the long-form channel, 2026-08-13, a publish
returned a well-formed id for a post that never existed, and the piece read as
shipped in every log while nothing was live. A human found it, not the system.
**A non-erroring call is not a published post.** Here the result can actually be
looked at, so look, every time.

**Quarantine.** On `timeline_partial` or `readback_failed`: set
`status: needs_attention` in the piece's frontmatter with `attention_reason`,
whatever `post_ids` were confirmed live, and `attempted_at`. **Leave the file
where it is** — do not move it to `content/shipped/`. Step 1 selects only
`status: approved`, so a quarantined piece is never re-selected and never
re-published. Notify with the thread URL if known and the **full text of every
tweet**, so the approver can resolve it without reconstructing anything.

**Only the approver clears `needs_attention`; the system never promotes it back
to `approved`.** Clearing it requires knowing what is already live on the
timeline and deciding what to do about it — finish the thread by hand, delete the
live tweets, or re-plan the piece — and every one of those is a human call about
published content.

### 7. Move to terminal truth

Runs only on `timeline_confirmed`. `timeline_partial`, `timeline_absent` and
`readback_failed` all exit at step 6 and never reach here.

Move the file to `content/shipped/`, **renaming it to the actual ship date** —
the filename date means "when this went out", not "when it was planned"; the
planned date is post-mortem material and lives in frontmatter. That convention is
what keeps `content/shipped/` readable as a history.

```yaml
status: shipped
shipped_at: {ISO timestamp}
planned_date: {unchanged — the original planned date the writer set}
post_ids:                                # ordered — hook first, then every tweet
  - "{hook_id}"
  - "{tweet_2_id}"
post_url: https://{host}/{handle}/status/{hook_id}
publish_verified: timeline_confirmed     # the only value that reaches shipped/
```

`{handle}` comes from config. If it is not recorded there, use the platform's
handle-independent status URL form rather than guessing a handle into a URL.

Selection in step 1 still reads the *planned* filename date on unshipped pieces —
correct, because the rename happens only on the way into `content/shipped/`.

### 8. Notify, log

- `sh "$MKT_DEPT/lib/mkt-notify.sh" shipped content/shipped/{filename}`
- Append to `agents/campaign-strategist/notebook/{YYYY-MM-DD}-content-log.md`:
  `- shipped: {filename} | {channel} | {tweet_count} tweet(s) | hook: {hook_id} | verified: {publish_verified} | {timestamp}`
- `traces/mkt-ship-content-x-{YYYY-MM-DD}.log` — written **incrementally during
  posting**, not only at the end: if the run dies mid-step, what was already live
  must still be recoverable from the trace. Finalize with the selection decision,
  deferred backlog, per-tweet ids, and `publish_verified`.

### 9. Close the loop, best-effort

Where the instance sets `approval_surface.close_command`, call it with the
piece's **original pre-rename slug** — review cards reference the draft path, not
the shipped path. Never fatal: unreachable, non-200, anything → skip silently and
log `card_close_skipped`.

---

## Cost

Zero per post: the browser path uses an existing logged-in session, so there is
no per-call charge and no metered line item. Worth stating plainly because the
alternative was not — the source platform moved to pay-per-use pricing in
February 2026 and closed its free tier to new developers. At this cadence the API
would have cost a few dollars a month. Small in absolute terms, and still the
wrong shape: metered spend has no natural ceiling where a subscription does. The
browser path sidesteps the question rather than asking anyone to approve crossing
that line for a few dollars.

The one rule that survives from the API-era design: **links belong on the final
tweet only.** That was a style rule first — the hook has to earn the tap, not read
as an ad — briefly a cost rule too, and is a style rule again. Do not relax it on
the grounds that links are free again.

---

## Outputs

| Path | Contents |
|---|---|
| `content/shipped/{YYYY-MM-DD}-{rest}.md` | the piece, terminal, with ordered `post_ids`, `post_url`, `publish_verified` |
| the piece, in place | on quarantine: `status: needs_attention`, `attention_reason`, live `post_ids`, `attempted_at` — never re-selectable, waiting on the approver |
| `agents/campaign-strategist/notebook/{YYYY-MM-DD}-content-log.md` | one line per ship |
| `traces/mkt-ship-content-x-{YYYY-MM-DD}.log` | incremental during posting, finalized at the end |
| `inbox/` (via notify) | anything that needs the approver: over-limit tweet, unparseable piece, quarantine |

---

## Stop codes

| Code | Meaning |
|---|---|
| `published` | the only success |
| `mode_halt` | `MODE` is sabbath / retreat / quiet |
| `publish_freeze` | `MKT_PUBLISH_FREEZE` set — the queue holds and drains later |
| `non_publishing_day` | today is not in the channel's `publishing_days` |
| `already_shipped_today` | the per-channel daily cap; a thread is one piece |
| `channel_disabled` | `channels.{channel}.enabled` is false |
| `channel_autonomy_too_low` | channel is C0/C1 — no publishing path should exist |
| `no_eligible_piece` | nothing approved and due |
| `status_not_approved` | the named piece has not passed M2 |
| `draft_unparseable` | the `tweets` list did not parse, or disagreed with `tweet_count` — nothing published |
| `tweet_over_limit` | a tweet exceeds the weighted limit — nothing published |
| `not_logged_in` | no live session |
| `wrong_account` | logged in as someone else — never publish |
| `composer_readback_mismatch` | box count or text mismatch before publishing |
| `timeline_partial` | live but wrong part count — quarantined |
| `timeline_absent` | nothing live — left approved, retried next run |
| `readback_failed` | could not read the timeline — quarantined |
| `deferred_backlog` | informational, one per skipped queue entry |
| `card_close_skipped` | informational, never fatal |

---

## Failure modes to avoid

- **Chaining replies instead of using the composer.** A stranded half-thread is
  public and unrecoverable.
- **Reading `weighted_chars` off the draft** instead of recomputing at publish time.
- **Inserting text without clearing the box first** — the result is doubled text
  in a live post.
- **Adding a box and filling it later** — the empty box is deleted and the thread
  loses a tweet.
- **Clicking publish twice** after an ambiguous result. Look first.
- **Promoting a quarantined piece back to `approved`** on the system's own
  authority.
- **Hardcoding the day list** instead of reading `publishing_days`.
- **Asking for confirmation** in an unattended run.
