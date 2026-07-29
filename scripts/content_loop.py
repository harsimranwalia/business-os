#!/usr/bin/env python3
"""
content_loop.py — Marketing Contents lifecycle between Twenty CRM and Telegram.

The CRM is the system of record. Telegram is the approval channel. This script
is deterministic glue — no LLM anywhere in the approval or send path.

Lifecycle (status field on the Marketing Content record):
  pending   -> created by an agent (via `create`), awaiting notification
  pending   -> notified over Telegram with a key like MC-123
  approved  -> human replied "approve" (or "edit: <new text>", which also
               updates the body) — reddit_post.py picks these up
  discarded -> human replied "skip" (optionally "skip: reason")
  posted / failed -> set by reddit_post.py after the send attempt

Subcommands:
  create   Read JSON on stdin, create a record at status=pending.
           Fields: title, channel, community, permalink, external_id,
           body, rationale
  notify   Send every un-notified pending record to Telegram via
           scripts/telegram.py (vendored from singlas/dev-workflow),
           tagged with its MC-<n> key for reply matching.
  poll     Poll Telegram replies via telegram.py and apply them:
           approve | skip[: reason] | edit: <replacement body>
  list     Print records, optionally --community <sub> --status <s>
           (used by the triage agent for PENDING-COLLISION checks).

Twenty setup (already provisioned via the metadata API — kept here as reference):
  Object "Marketing Content" (plural "Marketing Contents",
  API name marketingContent/marketingContents) with fields:
    title (text, default)        -- the record's title/name field
    key (text, unique)           -- MC-<n>, assigned here at create
    channel (select: REDDIT, INSTAGRAM, X)
    status (select: PENDING, APPROVED, DISCARDED, POSTED, FAILED)
    community (text)             -- e.g. subreddit
    permalink (text)             -- target thread URL
    externalId (text)            -- e.g. reddit thread id
    body (rich text)             -- the draft. RICH_TEXT is a composite
                                     {markdown, blocknote} field in Twenty's
                                     GraphQL schema, not a plain string — this
                                     script always reads/writes body.markdown.
    rationale (text)
    postedUrl (text)
    notes (text)
    telegramMessageId (number)
    notifiedAt (datetime)

  SELECT option values must be UPPER_CASE snake_case (Twenty enforces this).
  `create`'s channel input is lower-case for ergonomics (e.g. "reddit") and
  is upper-cased before being written.

Env (or repo-root .env): TWENTY_API_KEY, TWENTY_BASE_URL
(e.g. https://crm.example.com — no trailing slash), plus telegram.py's
TELEGRAM_BOT_TOKEN and AGENT_TELEGRAM_CHAT_ID.

Quiet mode: set MODE=sabbath|retreat|quiet in .env and `notify` goes silent.

Cron:
  */10 * * * *  cd /path/to/business-os && python scripts/content_loop.py notify
  */10 * * * *  cd /path/to/business-os && python scripts/content_loop.py poll

Stdlib only.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TELEGRAM = Path(__file__).resolve().parent / "telegram.py"

KEY_PREFIX = "MC"
APPROVE_RE = re.compile(r"^\s*(approve|yes|ok|lgtm)\s*$", re.IGNORECASE)
SKIP_RE = re.compile(r"^\s*skip\s*:?\s*(.*)$", re.IGNORECASE)
EDIT_RE = re.compile(r"^\s*edit\s*:\s*(.+)$", re.IGNORECASE | re.DOTALL)

# ---------------------------------------------------------------- env / mode

def load_env() -> None:
    env = BASE_DIR / ".env"
    if not env.exists():
        return
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def quiet_mode() -> bool:
    return os.environ.get("MODE", "").strip().lower() in ("sabbath", "retreat", "quiet")

# ---------------------------------------------------------------- twenty api

def gql(query: str, variables: dict) -> dict:
    base = os.environ.get("TWENTY_BASE_URL", "").rstrip("/")
    key = os.environ.get("TWENTY_API_KEY", "")
    if not base or not key:
        sys.exit("error: TWENTY_BASE_URL / TWENTY_API_KEY not set")
    req = urllib.request.Request(
        f"{base}/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        sys.exit(f"error: twenty graphql: {payload['errors']}")
    return payload["data"]


FIELDS = ("id title key channel status community permalink externalId "
          "rationale postedUrl notes telegramMessageId notifiedAt")
# body is RICH_TEXT — a composite {markdown, blocknote} object in Twenty's
# GraphQL schema, so it needs a sub-selection rather than a bare field name.
SELECTION = f"{FIELDS} body {{ markdown }}"


def find_records(filter_obj: dict, limit: int = 50) -> list:
    q = f"""query($f: MarketingContentFilterInput, $l: Int) {{
      marketingContents(filter: $f, first: $l) {{
        edges {{ node {{ {SELECTION} }} }} }} }}"""
    data = gql(q, {"f": filter_obj, "l": limit})
    return [e["node"] for e in data["marketingContents"]["edges"]]


def create_record(fields: dict) -> dict:
    q = f"""mutation($d: MarketingContentCreateInput!) {{
      createMarketingContent(data: $d) {{ {SELECTION} }} }}"""
    return gql(q, {"d": fields})["createMarketingContent"]


def update_record(rid: str, fields: dict) -> dict:
    q = f"""mutation($id: UUID!, $d: MarketingContentUpdateInput!) {{
      updateMarketingContent(id: $id, data: $d) {{ {SELECTION} }} }}"""
    return gql(q, {"id": rid, "d": fields})["updateMarketingContent"]


def body_text(rec: dict) -> str:
    return ((rec.get("body") or {}).get("markdown") or "")


def next_key() -> str:
    """MC-<n> from the current max. Fine at this scale (single writer)."""
    records = find_records({"key": {"startsWith": f"{KEY_PREFIX}-"}}, limit=500)
    nums = [int(m.group(1)) for r in records
            if (m := re.match(rf"{KEY_PREFIX}-(\d+)$", r.get("key") or ""))]
    return f"{KEY_PREFIX}-{max(nums, default=0) + 1}"

# ---------------------------------------------------------------- telegram

def tg(*args: str) -> str:
    """Shell out to the vendored telegram.py; returns stdout."""
    if not TELEGRAM.exists():
        sys.exit(f"error: {TELEGRAM} missing — vendor it from "
                 "github.com/singlas/dev-workflow skills/ticket-loop/telegram.py")
    r = subprocess.run([sys.executable, str(TELEGRAM), *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"error: telegram.py {args[0]}: {r.stderr.strip()}")
    return r.stdout

# ---------------------------------------------------------------- commands

def cmd_create(_a) -> None:
    payload = json.loads(sys.stdin.read())
    required = ("title", "channel", "community", "permalink", "body")
    missing = [k for k in required if not payload.get(k)]
    if missing:
        sys.exit(f"error: missing fields: {', '.join(missing)}")
    rec = create_record({
        "title": payload["title"][:120],
        "key": next_key(),
        "channel": payload["channel"].strip().upper(),
        "status": "PENDING",
        "community": payload["community"],
        "permalink": payload["permalink"],
        "externalId": payload.get("external_id", ""),
        "body": {"markdown": payload["body"]},
        "rationale": payload.get("rationale", ""),
    })
    print(json.dumps({"id": rec["id"], "key": rec["key"]}))


def cmd_notify(_a) -> None:
    if quiet_mode():
        print("quiet mode — not notifying")
        return
    pending = [r for r in find_records({"status": {"eq": "PENDING"}})
               if not r.get("notifiedAt")]
    for r in pending:
        text = (f"{r['key']} | r/{r['community']}\n{r['title']}\n{r['permalink']}\n\n"
                f"{body_text(r)}\n\n"
                f"why: {r.get('rationale') or '-'}\n\n"
                f"reply to THIS message: approve / skip[: reason] / edit: <new text>")
        out = tg("send", "--ticket", r["key"], text)
        msg_id = json.loads(out.strip().splitlines()[-1])["message_id"]
        update_record(r["id"], {
            "telegramMessageId": msg_id,
            "notifiedAt": datetime.now(timezone.utc).isoformat(),
        })
        print(f"notified {r['key']} (tg message {msg_id})")
    if not pending:
        print("nothing to notify")


def cmd_poll(_a) -> None:
    out = tg("poll", "--timeout", "10")
    for line in out.strip().splitlines():
        if not line.strip():
            continue
        msg = json.loads(line)
        key, text = msg.get("ticket"), (msg.get("text") or "").strip()
        if not key:
            continue
        matches = find_records({"key": {"eq": key}}, limit=1)
        if not matches:
            print(f"warn: reply for unknown key {key}", file=sys.stderr)
            continue
        rec = matches[0]
        if rec["status"] != "PENDING":
            tg("send", f"{key} is already {rec['status']} — no change")
            continue

        if APPROVE_RE.match(text):
            update_record(rec["id"], {"status": "APPROVED"})
            tg("send", f"{key} approved — will post on next cycle")
        elif (m := EDIT_RE.match(text)):
            update_record(rec["id"], {"body": {"markdown": m.group(1).strip()},
                                      "status": "APPROVED"})
            tg("send", f"{key} body replaced and approved")
        elif (m := SKIP_RE.match(text)):
            update_record(rec["id"], {"status": "DISCARDED",
                                      "notes": f"skip: {m.group(1) or 'no reason'}"})
            tg("send", f"{key} discarded")
        else:
            tg("send", f"{key}: didn't understand. reply to the draft with "
                       "approve / skip[: reason] / edit: <new text>")


def cmd_list(a) -> None:
    f = {}
    if a.community:
        f["community"] = {"eq": a.community}
    if a.status:
        f["status"] = {"eq": a.status.strip().upper()}
    for r in find_records(f or {"status": {"in": ["PENDING", "APPROVED"]}}):
        print(json.dumps({k: r.get(k) for k in
                          ("key", "status", "channel", "community",
                           "title", "permalink")}, ensure_ascii=False))


def main() -> None:
    load_env()
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("create").set_defaults(func=cmd_create)
    sub.add_parser("notify").set_defaults(func=cmd_notify)
    sub.add_parser("poll").set_defaults(func=cmd_poll)
    pl = sub.add_parser("list")
    pl.add_argument("--community")
    pl.add_argument("--status")
    pl.set_defaults(func=cmd_list)
    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
