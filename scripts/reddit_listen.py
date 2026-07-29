#!/usr/bin/env python3
"""
reddit_listen.py — read-only Reddit listener for business-os.

Sweeps target subreddits for threads matching AIOrders-relevant signals and
writes candidate JSON to inbox/listeners/reddit/ for the community-builder
agent to triage. This script NEVER writes to Reddit. It authenticates
read-only and contains no code paths that submit, vote, or comment.

Setup:
  1. Create a Reddit "script" app at https://www.reddit.com/prefs/apps
  2. pip install praw
  3. Set env vars in repo-root .env: REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET,
     REDDIT_USER_AGENT. User agent format Reddit requires:
     "linux:business-os-listener:v1.0 (by /u/aiorders-io)"
  4. cron example (weekdays, 3x daily, skips Saturday for sabbath — adjust to yours):
       0 8,13,18 * * 0-5  cd /path/to/business-os && python scripts/reddit_listen.py

State: seen thread IDs are tracked in crm-adjacent local state
(inbox/listeners/reddit/.seen_ids.json) so the same thread is never
surfaced twice.

Quiet mode: set MODE=sabbath|retreat|quiet in repo-root .env and every
component in the pipeline (this listener included) goes silent.
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import praw

# ---------------------------------------------------------------- config

BASE_DIR = Path(__file__).resolve().parent.parent  # business-os/
OUT_DIR = BASE_DIR / "inbox" / "listeners" / "reddit"
SEEN_FILE = OUT_DIR / ".seen_ids.json"

# sub -> per-sub config. Keep in sync with memory/marketing/subreddit-map.md.
# The agent enforces the map; this list just controls what gets swept.
SUBREDDITS = {
    "restaurateur":        {"limit": 40},
    "smallbusiness":       {"limit": 40},
    "restaurantowners":    {"limit": 30},
    "KitchenConfidential": {"limit": 25},   # observe-only: swept for learning, agent won't pass
    "vancouver":           {"limit": 25},
    "askTO":               {"limit": 25},
}

# Signal terms. A thread qualifies if title+body matches >= MIN_SIGNALS,
# or matches one STRONG term. Case-insensitive, word-ish boundaries.
STRONG_TERMS = [
    r"door\s?dash\s+(fee|commission|30%)",
    r"uber\s?eats\s+(fee|commission|30%)",
    r"commission[-\s]free",
    r"direct\s+ordering",
    r"own\s+(my|our|your)\s+(ordering|website|customers?)",
    r"third[-\s]party\s+delivery",
    r"online\s+ordering\s+(system|platform|site)",
]
WEAK_TERMS = [
    r"door\s?dash", r"uber\s?eats", r"skip\s?the\s?dishes", r"grubhub",
    r"delivery\s+app", r"commission", r"pos\b", r"toast\b", r"square\b",
    r"clover\b", r"loyalty", r"repeat\s+customers?", r"google\s+business",
    r"restaurant\s+website", r"qr\s+(code\s+)?(menu|ordering)",
    r"delivery\s+fees?", r"marketplace\s+fees?",
]
MIN_WEAK_SIGNALS = 2

# Only surface threads that look like questions / requests for help.
QUESTION_HINTS = [
    r"\?", r"^how\b", r"\bhow do i\b", r"\bshould i\b", r"\bis it worth\b",
    r"\banyone (else|use|using|tried)\b", r"\bwhat (do|does|is|are)\b",
    r"\brecommend", r"\badvice\b", r"\bhelp\b", r"\bworth it\b",
]

MAX_AGE_HOURS = 24
MAX_COMMENTS = 30          # past this the agent rejects as STALE anyway
TOP_COMMENTS_TO_CAPTURE = 5
SEEN_CAP = 5000            # keep seen-id file bounded

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


def sabbath_mode() -> bool:
    """Respect sabbath/retreat mode: the listener itself goes silent."""
    return os.environ.get("MODE", "").strip().lower() in ("sabbath", "retreat", "quiet")


def load_seen() -> set:
    try:
        return set(json.loads(SEEN_FILE.read_text(encoding="utf-8")))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_seen(seen: set) -> None:
    ids = list(seen)[-SEEN_CAP:]
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(ids), encoding="utf-8")


def matches(text: str) -> tuple[bool, list[str]]:
    """Return (qualifies, matched_terms)."""
    t = text.lower()
    hits = []
    for pat in STRONG_TERMS:
        if re.search(pat, t):
            hits.append(f"strong:{pat}")
    if hits:
        return True, hits
    weak_hits = [f"weak:{p}" for p in WEAK_TERMS if re.search(p, t)]
    return len(weak_hits) >= MIN_WEAK_SIGNALS, weak_hits


def looks_like_question(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in QUESTION_HINTS)


def reddit_client() -> praw.Reddit:
    missing = [k for k in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT")
               if not os.environ.get(k)]
    if missing:
        sys.exit(f"Missing env vars: {', '.join(missing)}")
    r = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
    )
    r.read_only = True  # hard guarantee: no write capability on this client
    return r

# ---------------------------------------------------------------- sweep

def sweep() -> None:
    load_env()
    if sabbath_mode():
        print("mode: sabbath/retreat — listener exiting silently")
        return

    reddit = reddit_client()
    seen = load_seen()
    now = datetime.now(timezone.utc)
    candidates = []

    for sub_name, cfg in SUBREDDITS.items():
        try:
            sub = reddit.subreddit(sub_name)
            for post in sub.new(limit=cfg["limit"]):
                if post.id in seen:
                    continue
                seen.add(post.id)

                age_h = (now.timestamp() - post.created_utc) / 3600
                if age_h > MAX_AGE_HOURS:
                    continue
                if post.num_comments > MAX_COMMENTS:
                    continue
                if getattr(post, "stickied", False) or getattr(post, "locked", False):
                    continue

                text = f"{post.title}\n{post.selftext or ''}"
                ok, hits = matches(text)
                if not ok:
                    continue
                if not looks_like_question(text):
                    continue

                # capture top comments so triage/writer can judge saturation
                post.comment_sort = "top"
                post.comments.replace_more(limit=0)
                top_comments = [
                    c.body[:600] for c in post.comments[:TOP_COMMENTS_TO_CAPTURE]
                    if hasattr(c, "body")
                ]

                candidates.append({
                    "subreddit": sub_name,
                    "thread_id": post.id,
                    "thread_title": post.title,
                    "thread_body": (post.selftext or "")[:4000],
                    "top_comments": top_comments,
                    "permalink": f"https://reddit.com{post.permalink}",
                    "num_comments": post.num_comments,
                    "score": post.score,
                    "age_hours": round(age_h, 1),
                    "signals": hits,
                    "swept_at": now.isoformat(),
                })
            time.sleep(2)  # be polite between subs
        except Exception as e:  # one sub failing shouldn't kill the sweep
            print(f"warn: r/{sub_name} sweep failed: {e}", file=sys.stderr)

    save_seen(seen)

    if not candidates:
        print("sweep complete: 0 candidates")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"sweep-{now.strftime('%Y%m%d-%H%M')}.json"
    out_path.write_text(json.dumps(candidates, indent=2), encoding="utf-8")
    print(f"sweep complete: {len(candidates)} candidates -> {out_path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    sweep()
