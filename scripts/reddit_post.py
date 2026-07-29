#!/usr/bin/env python3
"""
reddit_post.py (v2, CRM-backed) — posts APPROVED Marketing Contents to Reddit.
The only component in business-os with Reddit write access.

Source of truth is Twenty: records with channel=reddit, status=approved
(set only by a human reply over Telegram via content_loop.py). This script
posts them and writes the outcome back:

  approved -> posted  (postedUrl set)
  approved -> failed  (error in notes)

Design guarantees (unchanged from v1):
  - No LLM in the send path. Approval is a human Telegram reply; the send
    is a dumb deterministic apply.
  - At most ONE comment per run + a minimum gap between posts.
  - Refuses to run in quiet (sabbath/retreat) mode.
  - Refuses to double-post to a thread already posted to.
  - Verifies the thread is not locked/archived/removed before posting.

Env: TWENTY_API_KEY, TWENTY_BASE_URL, plus Reddit creds
(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, and either
REDDIT_REFRESH_TOKEN or REDDIT_USERNAME + REDDIT_PASSWORD).
Keep these separate from the read-only listener's creds.

Quiet mode: set MODE=sabbath|retreat|quiet in .env and the poster exits silently.

Cron:  */30 * * * *  cd /path/to/business-os && python scripts/reddit_post.py
Requires: pip install praw
"""

import json
import os
import re
import sys
import time
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import praw
import prawcore

BASE_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = BASE_DIR / "memory" / "marketing" / ".post_state.json"
ENGAGEMENT_LOG = BASE_DIR / "memory" / "marketing" / "engagement-log.md"
TELEGRAM = Path(__file__).resolve().parent / "telegram.py"

MIN_GAP_MINUTES = 45
MAX_POSTS_PER_RUN = 1
MAX_BODY_CHARS = 2500

# ---------------------------------------------------------------- helpers

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


def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_post_ts": 0, "posted_thread_ids": []}


def save_state(state: dict) -> None:
    state["posted_thread_ids"] = state["posted_thread_ids"][-2000:]
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def log_engagement(line: str) -> None:
    ENGAGEMENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with ENGAGEMENT_LOG.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def tg_send(text: str) -> None:
    """Best-effort Telegram notice; never fails the run."""
    if not TELEGRAM.exists():
        return
    subprocess.run([sys.executable, str(TELEGRAM), "send", text],
                   capture_output=True, text=True)

# ---------------------------------------------------------------- twenty

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


FIELDS = "id title key channel status community permalink externalId notes"
# body is RICH_TEXT — a composite {markdown, blocknote} object in Twenty's
# GraphQL schema, so it needs a sub-selection rather than a bare field name.
SELECTION = f"{FIELDS} body {{ markdown }}"


def approved_reddit_records() -> list:
    q = f"""query($f: MarketingContentFilterInput) {{
      marketingContents(filter: $f, first: 20) {{
        edges {{ node {{ {SELECTION} }} }} }} }}"""
    data = gql(q, {"f": {"and": [{"status": {"eq": "APPROVED"}},
                                 {"channel": {"eq": "REDDIT"}}]}})
    return [e["node"] for e in data["marketingContents"]["edges"]]


def update_record(rid: str, fields: dict) -> None:
    q = """mutation($id: UUID!, $d: MarketingContentUpdateInput!) {
      updateMarketingContent(id: $id, data: $d) { id } }"""
    gql(q, {"id": rid, "d": fields})

# ---------------------------------------------------------------- reddit

def reddit_client() -> praw.Reddit:
    base = {
        "client_id": os.environ.get("REDDIT_CLIENT_ID", ""),
        "client_secret": os.environ.get("REDDIT_CLIENT_SECRET", ""),
        "user_agent": os.environ.get("REDDIT_USER_AGENT", ""),
    }
    if not all(base.values()):
        sys.exit("Missing REDDIT_CLIENT_ID / REDDIT_CLIENT_SECRET / REDDIT_USER_AGENT")
    if os.environ.get("REDDIT_REFRESH_TOKEN"):
        base["refresh_token"] = os.environ["REDDIT_REFRESH_TOKEN"]
    elif os.environ.get("REDDIT_USERNAME") and os.environ.get("REDDIT_PASSWORD"):
        base["username"] = os.environ["REDDIT_USERNAME"]
        base["password"] = os.environ["REDDIT_PASSWORD"]
    else:
        sys.exit("Need REDDIT_REFRESH_TOKEN, or REDDIT_USERNAME + REDDIT_PASSWORD")
    r = praw.Reddit(**base)
    print(f"authenticated as u/{r.user.me()}")
    return r


def thread_id_of(rec: dict) -> str:
    if rec.get("externalId"):
        return rec["externalId"]
    m = re.search(r"/comments/([a-z0-9]+)/", rec.get("permalink") or "")
    if not m:
        raise ValueError("cannot determine thread id from externalId or permalink")
    return m.group(1)

# ---------------------------------------------------------------- main

def run() -> None:
    load_env()
    if quiet_mode():
        print("quiet mode — poster exiting silently")
        return

    queue = approved_reddit_records()
    if not queue:
        print("queue empty")
        return

    state = load_state()
    gap_s = time.time() - state["last_post_ts"]
    if gap_s < MIN_GAP_MINUTES * 60:
        print(f"rate limit: next post eligible in "
              f"~{int((MIN_GAP_MINUTES * 60 - gap_s) / 60) + 1}m "
              f"({len(queue)} approved in queue)")
        return

    reddit = reddit_client()
    posted = 0

    for rec in queue:
        if posted >= MAX_POSTS_PER_RUN:
            print(f"per-run cap reached; {len(queue) - posted} remain approved")
            break
        try:
            body = ((rec.get("body") or {}).get("markdown") or "").strip()
            if not body:
                raise ValueError("empty body")
            if len(body) > MAX_BODY_CHARS:
                raise ValueError(f"body {len(body)} chars over ceiling")

            tid = thread_id_of(rec)
            if tid in state["posted_thread_ids"]:
                raise ValueError("already commented on this thread")

            submission = reddit.submission(id=tid)
            if submission.locked:
                raise ValueError("thread is locked")
            if submission.archived:
                raise ValueError("thread is archived")
            if getattr(submission, "removed_by_category", None):
                raise ValueError("thread was removed")

            comment = submission.reply(body)
            url = f"https://reddit.com{comment.permalink}"

            state["last_post_ts"] = time.time()
            state["posted_thread_ids"].append(tid)
            save_state(state)
            posted += 1

            update_record(rec["id"], {"status": "POSTED", "postedUrl": url})
            log_engagement(f"{datetime.now(timezone.utc).date()} | "
                           f"{rec['community']} | {tid} | POSTED | {url}")
            tg_send(f"{rec['key']} posted: {url}")
            print(f"posted {rec['key']}: {url}")

        except (ValueError, prawcore.exceptions.PrawcoreException,
                praw.exceptions.RedditAPIException) as e:
            update_record(rec["id"], {
                "status": "FAILED",
                "notes": f"failed {datetime.now(timezone.utc).isoformat()}: {e}",
            })
            log_engagement(f"{datetime.now(timezone.utc).date()} | "
                           f"{rec.get('community')} | {rec.get('key')} | FAILED | {e}")
            tg_send(f"{rec.get('key')} failed to post: {e}")
            print(f"failed {rec.get('key')}: {e}", file=sys.stderr)


if __name__ == "__main__":
    run()
