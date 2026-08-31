# Skill: ship-content

**Owner:** shared — runs on its own routine; the campaign strategist does not
invoke it, it reads its output for the channel report
**Model:** small (selection and validation are rule checks, not judgment)
**Trigger:** a daily routine. The routine fires **every day**; step 1 gates it to
the channel's publishing days and no-ops otherwise. Also callable with an
explicit path by whatever component processes the approval surface, when a
piece is approved out of band.
**Suppressed when:** `MODE` is `sabbath`, `retreat` or `quiet`; publishing (only)
is suppressed when `MKT_PUBLISH_FREEZE` is set.

---

## Purpose

Publish exactly one approved piece to a long-form channel, verify it as strongly
as that channel allows, and move the piece into terminal truth.

This is the long-form path: a single body of text, optionally with one image,
several images, or a document deck (a carousel). The short-form thread path is
`ship-content-x` — see **Why this is not one skill** at the bottom.

---

## Paths

Bare paths are **instance-relative** (`$MKT_INSTANCE`). Paths prefixed
`$MKT_DEPT` are template-side and read-only at runtime.

---

## The gate: `status: approved`, and nothing else

**`status: approved` in the piece's frontmatter is the publishing gate. The
folder it sits in is not.** `content/approved/` is where a human finds a piece;
the frontmatter field is how a machine decides. Where they disagree, the field
wins — except in `content/shipped/`, which is terminal and is never re-read as
work.

The approver's M2 approval has already happened by the time this runs, through
whatever approval surface the instance uses. **That approval is the
confirmation.**

**Publish immediately. Never ask the approver to confirm again. Never pause with
"shall I go ahead?"** This skill runs unattended — nobody is present to answer,
and a question here means the piece silently does not ship. A run has exactly
two valid endings: it publishes, or it stops and logs one of the named stop
codes below. There is no third ending where it asks and waits.

This cuts both ways: do not publish a piece that is not `status: approved`, and
do not re-ask about one that is. Checking the field *is* checking for approval.

**Channel autonomy does not change the gate.** At C2 the approver sets
`approved` at M2; at C3 the review pass sets it with no human. Either way this
skill's condition is identical, so there is only ever one publish path and it is
the one that gets exercised every day. If the channel is registered C0 or C1, no
publishing path is supposed to exist: stop with `channel_autonomy_too_low`.

---

## Config keys read (every run, never cached, never hardcoded)

From the instance's `config/config.yaml`:

| Key | Use |
|---|---|
| `channels.{channel}.enabled` | false → `channel_disabled` |
| `channels.{channel}.autonomy` | `c0`/`c1` → `channel_autonomy_too_low` |
| `channels.{channel}.publishing_days` | the cadence — a list of weekday names |
| `channels.{channel}.method` | `api` \| `browser` \| `manual` (see `publishing` in `config/conventions.yaml`) |
| `channels.{channel}.publish_command` | instance-provided command implementing the method |
| `channels.{channel}.author_id_env` | **name** of the env var holding the author/account id |
| `channels.{channel}.credential_env` | **name** of the env var holding the token |
| `channels.{channel}.limits.body_chars` | hard body limit, revalidated here |
| `channels.{channel}.limits.images_max` | max images in one post |
| `approval_surface.close_command` | optional; see step 8 |

A credential is referenced **by env var name**. This skill reads the value out
of the environment at call time and never writes it anywhere — not to a trace,
not to frontmatter, not to a log line.

**Cadence lives in config, not in this file.** Never hardcode a day list here.
A scheduler that can only fire daily or on one fixed weekday cannot express
"Tuesday, Wednesday, Thursday", so the routine fires daily and step 1 is what
actually enforces the schedule. The four no-op days a week are the design
working, not a fault — log them quietly. The payoff: changing cadence is a
one-line config edit with nothing to reconfigure in the scheduler, which is what
keeps cadence changes off the approver's plate.

---

## Inputs

- The channel's queue: every file in `content/approved/`, `content/ready-to-send/`
  and `content/drafts/` (all three are scanned; the field is the gate, not the
  folder)
- `content/shipped/` — to enforce today's cap
- `config/config.yaml`, `config/channels/{channel}.md` — the playbook
- `.env` → `MODE`, `MKT_PUBLISH_FREEZE`
- Optionally, one explicit piece path from a caller

### Frontmatter this skill dispatches on

The contract is `$MKT_DEPT/skills/content-writer/SKILL.md` § Draft frontmatter.
This skill reads a subset of it and adds one state.

| Field | Required | Meaning |
|---|---|---|
| `kind` | yes | `content-draft` |
| `channel` | yes | scopes the queue. This skill touches only its own channel's pieces |
| `status` | yes | `approved` is the gate. The writer's enum is `draft \| ready-to-send \| approved \| shipped`; a piece parked at `needs_attention` by any skill is never selectable |
| `format` | yes | `post` \| `carousel` \| `article` \| `email` \| `dm` — only the publishable ones reach here |
| filename `{YYYY-MM-DD}` prefix | yes | the **planned** publish date — the selection key |
| `planned_date` | yes | already written by the writer, equal to the filename date. **Preserved, never recomputed** |
| `archetype` | yes | carried through to `performance/` |
| `series`, `series_position` | no | the carousel cover-title fallback |

The visual block is **exactly one** of these variants, checked in this order:

| Variant | Fields | Notes |
|---|---|---|
| carousel | `carousel_pdf` + `slide_paths` (ordered) + `image_path` (slide 1) + `image_format: carousel` | takes precedence over everything below |
| single image | `image_path` + `image_format` | the common case |
| declared text-only | `image: none` + `image_note` | **an explicit decision, not a missing field.** Publish text-only without a warning — the writer already recorded why |
| multi-image | `image_refs` (ordered) | instance-bound; the default writer does not emit it |
| external design ref | `image_ref` | instance-bound; the default writer does not emit it |

An absent visual block with no `image: none` declaration is a gap, not a
decision: publish text-only and log `image_undeclared` so the writer's asset
readiness gate gets the signal.

`carousel_title` is optional. When absent, fall back to `"{series} — {series_position}"`,
then to the humanized `slug`. Never publish a deck with an empty cover title.

Written back by this skill: `status: shipped`, `shipped_at`, `post_id`,
`post_url`, `publish_verified`, and `planned_date` **only if the writer somehow
omitted it**.

---

## Steps

### 1. Mode, freeze, day, cap — in that order, before touching the queue

1. **`MODE`.** `sabbath`, `retreat` or `quiet` → exit immediately and silently.
   Log `mode_halt`. The scheduler keeps firing; the component is what stops.
2. **`MKT_PUBLISH_FREEZE`.** Any non-empty value → stop with `publish_freeze`.
   The freeze blocks **publishing only**: planning, drafting, review and M2
   approval all keep running, so approved pieces simply queue in
   `content/approved/`. When the freeze lifts they drain oldest-first, one per
   publishing day — **never as a burst**.
3. **Day of week.** Compute it **fresh** — `date +%A`, lowercased. Never read a
   stored `scheduled_day` label off a piece or a plan; a stored label is a
   record of intent, and acting on it publishes on the wrong day the first time
   the two disagree. Compare against
   `channels.{channel}.publishing_days`. Not in the list → stop with
   `non_publishing_day`. The backlog does not advance on a non-publishing day
   and no slot is lost: the oldest-first sort resumes exactly where it left off.
4. **Today's cap.** Scan `content/shipped/` for any file with this `channel` and
   a `shipped_at` dated today (local date, `YYYY-MM-DD` prefix). One exists →
   stop with `already_shipped_today`. **The guard is the calendar day, not the
   run**: it holds however this run was invoked — cron, manual retry, a
   just-approved piece handed in by the approval surface. Caps are per channel
   and independent: a long-form post today does not block a thread today.

An explicit piece path from a caller does **not** skip 1–4. It skips only the
selection in step 2.

### 2. Select — the single oldest, never the batch

Scan the three queue folders for files with this `channel`, `status: approved`,
and a filename date of today or earlier. Sort by filename date **ascending** and
select **only the single oldest**. Log every other qualifying file as
`deferred_backlog` with its filename and take no action on it — the next
publishing day picks up the next-oldest, one per day. Never skip ahead in the
queue.

**This exists because a backlog draining all at once has actually happened.** On
2026-07-16 three backlogged approved posts went out in a single run; they had to
be deleted by hand from the live feed, keeping one. A burst on a public feed is
not a cosmetic problem — it is the one failure mode that is visible to every
reader at once and cannot be undone by the system. So: one per channel per
publishing day, oldest-first, however many are approved.

Nothing qualifies → stop with `no_eligible_piece`. Not an error; most days on a
low-cadence channel end here.

Read the selected piece. `status` is not `approved` → stop with
`status_not_approved`.

### 3. Extract the body and revalidate the hard limit

The body is everything below the closing frontmatter `---`.

Revalidate its length against `channels.{channel}.limits.body_chars` **here**, at
publish time, not on the writer's stored count. Over → stop with `over_length`,
carrying the measured count. **Do not truncate.** Cutting words is a content
edit, and content edits belong to the writer and to M2, never to an unattended
publisher.

### 4. Render inline emphasis the channel actually supports

Most feed composers render no markdown at all: `**bold**` posts as literal
asterisks. Where the channel's playbook says so, convert bold and italic spans to
the corresponding Unicode Mathematical Sans-Serif Bold / Mathematical Italic code
points, character by character, leaving punctuation, spaces and plain text
untouched. Use the department's converter —
`$MKT_DEPT/lib/unicode-format.py` — and use its output as the body for every
step from here on, including the length check above.

**Do not attempt the character mapping by hand.** The exact code points matter
and guessing produces garbage glyphs in a published post. On a body with no `**`
or `_` the converter is a no-op, so running it unconditionally is always safe.

**If the converter is not installed** and the body contains `**` or `_`, stop
with `converter_missing`. Publishing literal asterisks under the business's name
is worse than publishing a day late, and this is the one step where doing
nothing is not the safe failure.

Headings and `[text](url)` links have no clean Unicode equivalent — they are the
writer's and reviewer's problem, and reaching this step with one in the body
means an earlier gate leaked.

### 5. Prepare assets — validate everything before publishing anything

Checked in this precedence order. The first one present wins.

**5a. Document deck (`carousel_pdf` and/or `slide_paths`).** Two publish routes:
the PDF as a true document post (swipeable, the form the deck was designed as),
and the ordered PNGs as a multi-image post (the fallback). **Validate both asset
sets up front**, so the fallback is known-good *before* publishing starts:

- `carousel_pdf` — exists, non-zero, and begins with the `%PDF-` magic bytes.
  Check the bytes, not the extension.
- `slide_paths` — every path exists, non-zero, and is a real PNG/JPEG **by
  inspection** (`file`), not by extension.

PDF broken, slides good → go straight to the multi-image route. **Both broken →
stop with `carousel_assets_missing`**, naming the offending paths, and notify.
Do not ship the piece text-only: for a deck, the text is a caption and publishing
it alone guts the post.

**5b. `image_path` / `image_refs` — local rendered files.** Verify each exists
and is a non-zero real image by inspection. Any failure → treat as no image and
publish text-only. Never publish a broken or empty file. Count against
`limits.images_max`.

**5c. `image_ref` — an external design tool.** Only where the instance binds one.
The shape is always the same three calls and it is worth knowing: start an
export job, **poll** the job until it reports success, download the result to a
local path, then use that local absolute path exactly like 5b. Do not skip the
poll — an export id is not an exported file.

**5d. `image: none` — declared text-only.** A decision the writer already made and
recorded in `image_note`. Publish text-only, no warning, no stop code.

No visual block at all and no declaration → publish text-only and log
`image_undeclared`. Text-only is a normal outcome on this channel; an
*undeclared* one means an upstream asset gate did not run.

### 6. Publish

Call `channels.{channel}.publish_command` with a JSON payload:

```json
{
  "author": "<value of the env var named by author_id_env>",
  "body": "<the converted body>",
  "visibility": "public",
  "images": ["<absolute path>", "..."],
  "document": { "path": "<absolute pdf path>", "title": "<carousel_title>" }
}
```

`images` and `document` are mutually exclusive and both are optional. Paths are
**absolute** — a relative path is unverified and resolves against whatever
directory the routine happened to start in.

**Route the deck to the document route first.** A document post is a different
media type from an image post, not a PDF-shaped image; the fallback is used only
when the document route fails.

> **Never put a PDF into an images array.** Until 2026-08-13 the source of this
> skill claimed the image field accepted `application/pdf`, "verified against the
> tool schema". It never did. Because the field took any file path without
> validating its type, the call returned success **and a well-formed media id**,
> and the platform then silently dropped the post when the PDF failed as an image
> asset. The piece read as shipped in every log and artifact while nothing was
> live, and a human found it, not the system.
>
> The lesson that generalizes past that one field: **a non-erroring call is not a
> published post.** That is why step 7 exists, and why the document route is
> required to read its post id out of a response header rather than a body field.

**Verify the call's real contract before assuming a flag exists.** The same
integration was called with a `--file` flag for months; it has no such flag, and
a live publish rejected it with `images: Expected array, received string`
(2026-07-10). Where the instance's binding offers a schema-dump command, read it
rather than inferring the shape from an older example.

**Document-route fallback.** If the document route fails for *any* reason —
non-zero exit, unparseable result, an explicit failure — fall back **in the same
run** to the multi-image route with `slide_paths`. Record the document route's
failure reason in the trace so a persistent regression is visible rather than
quietly absorbed every day.

Failure of both routes → stop with `publish_failed`. **Do not retry beyond the
one documented fallback**, and do not mark the piece shipped. Leaving it in place
at `status: approved` is exactly what lets the next run retry it cleanly.

### 7. Record how strongly the publish was verified

A returned id is not proof of publication (2026-08-13, above). On this channel a
genuine read-back is **not available** — every route to fetch one's own post back
was checked on 2026-08-13 and each is gated behind a partner-tier API, returning
403 even for posts known to be live. A 403 there carries no information in either
direction, so do not add a read-back call and do not treat its absence as a
signal. Instead record the *strength* of what was actually confirmed, and never
let a weak signal read as a strong one:

| `publish_verified` | Means |
|---|---|
| `asset_available_and_id_header` | the document route succeeded: the asset was polled to available before posting (the exact thing that failed on 2026-08-13), and the post id came from a response header |
| `id_returned_only` | the image or text route succeeded: an id came back, with no asset-state check behind it. **This is the confidence level that once proved wrong** — record it as the weak signal it is |
| `false` | the publish failed. Do **not** mark shipped, do **not** move the file |

Write `publish_verified` to both the trace and the shipped frontmatter. The point
is that confidence is *recorded*, not assumed: if a post goes missing again, the
trace should say exactly how much was ever known.

**The one real check on this channel is a human eye on the feed.** Do not put
that step in this skill — it is unattended, and an instruction to "eyeball it" in
a cron job is how the 2026-08-13 verification never ran. Where the channel's
playbook says read-back is impossible, it says so explicitly and says what is
checked instead; that is the `publishing.verification` rule in
`config/conventions.yaml`.

### 8. Move to terminal truth

Move the file to `content/shipped/`, **renaming it to the actual ship date.** The
filename date must mean "when this went out", not "when it was planned" — the
planned date is only useful for post-mortem and belongs in frontmatter. It is
what keeps `content/shipped/` readable as a history rather than a list of
intentions.

- shipped filename: `{today}-{rest-of-original-name}.md`
- rename any single image to match the new slug and update `image_path`
- **leave `planned_date` exactly as the writer wrote it.** It already holds the
  original planned date; recomputing it from the new filename would erase the
  only record of what was planned, which is the entire reason the field exists

```yaml
status: shipped
shipped_at: {ISO timestamp}
planned_date: {unchanged — the original planned date}
post_id: {returned id}
post_url: {live url, where the channel gives one}
publish_verified: asset_available_and_id_header | id_returned_only
```

Selection in step 2 still reads the *planned* filename date on unshipped pieces —
correct, because the rename happens only on the way into `content/shipped/`.

### 9. Notify, log, and close the loop

- `sh "$MKT_DEPT/lib/mkt-notify.sh" shipped content/shipped/{filename}` — the
  department never formats for a specific channel; the instance decides where
  that goes.
- Append one line to `agents/campaign-strategist/notebook/{YYYY-MM-DD}-content-log.md`:
  `- shipped: {filename} | {channel} | post: {post_id} | verified: {publish_verified} | {timestamp}`
- Write `traces/mkt-ship-content-{YYYY-MM-DD}.log`.
- **Close the open review card, best-effort.** Where the instance sets
  `approval_surface.close_command`, call it with the piece's **original**
  pre-rename slug. Cards created during review reference the draft path, not the
  shipped path, so matching on the new filename finds nothing. This step must
  never fail or block a ship — unreachable surface, non-200, anything: skip
  silently and log `card_close_skipped`. (Added because review cards piled up
  stale in a board's review column when nothing closed them at ship time, and
  had to be hand-cleared: 2026-07-28.)

---

## Outputs

| Path | Contents |
|---|---|
| `content/shipped/{YYYY-MM-DD}-{rest}.md` | the piece, terminal, with `post_id` and `publish_verified` |
| `agents/campaign-strategist/notebook/{YYYY-MM-DD}-content-log.md` | one line per ship |
| `traces/mkt-ship-content-{YYYY-MM-DD}.log` | selection, deferrals, verification strength, stop code |
| `inbox/` (via notify) | anything that needs the approver: assets missing, over length, publish failed |

---

## Stop codes

Every run ends with exactly one of these, and the trace carries it.

| Code | Meaning |
|---|---|
| `published` | the only success |
| `mode_halt` | `MODE` is sabbath / retreat / quiet |
| `publish_freeze` | `MKT_PUBLISH_FREEZE` set — the queue holds and drains later |
| `non_publishing_day` | today is not in the channel's `publishing_days` |
| `already_shipped_today` | the per-channel daily cap |
| `channel_disabled` | `channels.{channel}.enabled` is false |
| `channel_autonomy_too_low` | channel is C0/C1 — no publishing path should exist |
| `no_eligible_piece` | nothing approved and due |
| `status_not_approved` | the named piece has not passed M2 |
| `over_length` | body exceeds the channel's hard limit |
| `converter_missing` | emphasis markers present and no converter installed |
| `image_invalid` | an asset failed inspection; published text-only |
| `image_undeclared` | no visual block and no `image: none` declaration; published text-only |
| `carousel_assets_missing` | both deck routes' assets are broken — nothing published |
| `publish_failed` | the call failed; the piece stays approved for the next run |
| `deferred_backlog` | informational, one per skipped queue entry |
| `card_close_skipped` | informational, never fatal |

---

## Why this is not one skill with `ship-content-x`

They share the *stance* — the approval gate, the daily cap, oldest-first drain,
the never-re-ask rule — and almost none of the machinery. This skill carries
design-tool export/poll/download, markdown→Unicode conversion, the document-post
route with its multi-image fallback, and a channel where read-back is impossible.
`ship-content-x` carries composer-driven atomic thread posting, per-unit weighted
revalidation, and a genuine rendered read-back. Folding them together would make
the shared quarter unreadable and the divergent three-quarters
conditional-heavy. Keep the stance in sync deliberately; keep the code apart.

Neither skill may touch the other's queue — not to ship, not to defer, not to
count against the other's cap.

---

## Failure modes to avoid

- **Asking for confirmation.** Unattended run; the question is never answered and
  the piece never ships.
- **Shipping the backlog.** One per channel per publishing day, oldest-first, no
  exceptions (2026-07-16).
- **Hardcoding the day list** instead of reading `publishing_days` — it turns a
  one-line config edit into a skill edit plus a scheduler edit.
- **Trusting a stored weekday label** instead of computing the day fresh.
- **Trusting a returned id as proof of publication** (2026-08-13).
- **Truncating an over-length body** rather than stopping.
- **Shipping a deck text-only** when its assets are broken.
- **Validating assets after the first publish call** instead of before.
- **Writing a credential value anywhere** — traces, frontmatter, logs. Env var
  names travel; values do not.
