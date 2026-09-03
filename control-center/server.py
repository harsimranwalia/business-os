#!/usr/bin/env python3
"""Business OS Control Center — http://localhost:6789

A standalone command center for business-os, with zero dependency on
life-os. Runs entirely off this repo: departments/, instances/, and this
repo's own .env (TWENTY_API_KEY etc).

Gated by email+PIN, and now by ROLE. See control-center/accounts.py for the
store: an admin has no restrictions, a partner sees only the business
instances assigned to them and must supply their own Claude OAuth token and
SMS gateway before any work runs on their behalf. CONTROL_CENTER_USERS in
.env is no longer the user model — it seeds users.json once, on first run,
and is then ignored.

Tabs:
  Marketing    The marketing department, per business instance. Four views
               under one tab: DECIDE (what is due for the approver's M2 —
               the only recurring human gate in the system), CONTENT (the
               library), REDDIT (the Twenty CRM community pipeline, folded in
               as one channel among several rather than owning the tab), and
               SETTINGS (the channel config, editable — every value read on
               the next run). See departments/marketing/docs/marketing-team.md.
  Sales        A generic CRM funnel — stage-folder leads per business
               instance, no channel coupling. No sales agent writes into it
               yet (Harry's call, 2026-08-28: build the agent later), so this
               tab also has to be the way leads get in: create, move, edit.
  Engineering  Ported from life-os's control-center essentially unchanged —
               same board/bugs/gates/decide surface, same instance-selector
               design, just re-rooted at this repo instead of reaching into
               a sibling one. See docs/engineering-team.md.
  Cost         Spend by agent/model/routine/business, off the same
               costs-*.jsonl ledger lib/run-stream.py already writes per
               instance.
  Logs         Cron job stdout/stderr from logs/*.log (listeners,
               content_loop, reddit_post, eng-loop-all runs). ADMIN ONLY —
               these are repo-wide cron logs with no instance scoping in
               them, so there is no honest way to show a partner their
               slice of one.
  Partners     ADMIN ONLY. The user store: who exists, what role they hold,
               and which instances each partner may work on.
  Config       Your own credentials — Claude OAuth token, HTTP SMS gateway,
               and which customer database your SMS segments read from.
"""

import hmac
import json
import os
import re
import secrets
import shutil
import subprocess
import threading
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import accounts
import sms

ROOT = Path(__file__).resolve().parent.parent  # business-os root
HTML_FILE = Path(__file__).parent / "index.html"
LOGIN_HTML_FILE = Path(__file__).parent / "login.html"
PORT = 6789


def load_env():
    """Minimal .env loader, same shape scripts/content_loop.py already uses
    (os.environ.setdefault, so a real exported env var always wins)."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))


load_env()


# ── Auth gate ────────────────────────────────────────────────────────────────
# Email+PIN, server-side session store — no external deps. A session token is
# an opaque random id (not a signed cookie): the only thing worth protecting
# is which requests are self-authenticated, and a server-side dict does that
# without needing HMAC signing at all. _AUTH_LOCK exists because
# ThreadingHTTPServer runs each request on its own thread now — it did not
# before this gate needed one — and SESSIONS/LOGIN_ATTEMPTS are shared state.
#
# What changed when roles arrived: the session still stores only an email, and
# the ROLE is looked up per request from accounts.py rather than captured at
# login. That is the point — an admin who demotes a partner or narrows their
# instances takes effect on that partner's very next request, with no logout
# and no session invalidation to remember.

SESSION_COOKIE = "cc_session"
SESSION_TTL = 30 * 24 * 3600  # 30 days
LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 15 * 60

_AUTH_LOCK = threading.Lock()
SESSIONS = {}         # token -> {"email": str, "expires": float}
LOGIN_ATTEMPTS = {}   # ip -> {"count": int, "locked_until": float}


def _new_session(email):
    token = secrets.token_urlsafe(32)
    with _AUTH_LOCK:
        SESSIONS[token] = {"email": email, "expires": time.time() + SESSION_TTL}
    return token


def _session_email(token):
    if not token:
        return None
    with _AUTH_LOCK:
        sess = SESSIONS.get(token)
        if not sess:
            return None
        if sess["expires"] < time.time():
            SESSIONS.pop(token, None)
            return None
        return sess["email"]


def _drop_session(token):
    with _AUTH_LOCK:
        SESSIONS.pop(token, None)


def _client_ip(handler):
    """The real client IP, not cloudflared's own loopback socket peer.
    cloudflared forwards it in this header for every tunneled request;
    direct localhost access has none, so the raw socket address is the
    honest fallback there."""
    fwd = handler.headers.get("CF-Connecting-IP")
    return (fwd or handler.client_address[0]).strip()


def _login_locked(ip):
    with _AUTH_LOCK:
        a = LOGIN_ATTEMPTS.get(ip)
        if not a or not a["locked_until"] or a["locked_until"] <= time.time():
            return False, 0
        return True, int(a["locked_until"] - time.time())


def _login_fail(ip):
    with _AUTH_LOCK:
        a = LOGIN_ATTEMPTS.setdefault(ip, {"count": 0, "locked_until": 0})
        a["count"] += 1
        if a["count"] >= LOGIN_MAX_ATTEMPTS:
            a["locked_until"] = time.time() + LOGIN_LOCKOUT_SECONDS
            a["count"] = 0


def _login_ok(ip):
    with _AUTH_LOCK:
        LOGIN_ATTEMPTS.pop(ip, None)


def _parse_cookies(handler):
    out = {}
    for part in handler.headers.get("Cookie", "").split(";"):
        if "=" in part:
            k, _, v = part.strip().partition("=")
            out[k] = v
    return out


def _cookie_header(token, clear=False):
    # Secure works fine even over plain http://localhost — Chrome and
    # Firefox both treat localhost as a secure context — and is required for
    # the cookie to survive the trip through the Cloudflare Tunnel, where the
    # browser only ever sees HTTPS.
    max_age = 0 if clear else SESSION_TTL
    return (f"{SESSION_COOKIE}={token if not clear else ''}; Path=/; HttpOnly; "
            f"Secure; SameSite=Lax; Max-Age={max_age}")


# ── Generic markdown/frontmatter helpers ────────────────────────────────────

def parse_frontmatter_keys(fm_text, keys):
    """Pull a handful of top-level `key: value` pairs out of a frontmatter
    block. Deliberately shallow (no YAML dep) — good enough for the flat
    string keys every view here needs. Strips quotes and trailing comments."""
    out = {}
    for key in keys:
        m = re.search(rf"^{re.escape(key)}:[ \t]*(.*)$", fm_text, re.MULTILINE)
        if not m:
            continue
        val = m.group(1).strip()
        val = re.sub(r"\s+#.*$", "", val).strip()
        val = val.strip('"').strip("'")
        if val:
            out[key] = val
    return out


def _split_pr_part(p):
    """One `repo: url` or bare `url` segment from a pipe-separated pr_url
    string. Guards on the http(s) prefix so a bare URL's own scheme colon
    (`https://...`) never gets mistaken for a `repo:` separator."""
    p = p.strip()
    if not p.startswith(("http://", "https://")):
        m = re.match(r"^([^:\s]+):\s*(https?://\S+)$", p)
        if m:
            return {"repo": m.group(1), "url": m.group(2)}
    return {"repo": "", "url": p}


def _parse_pr_links(fm_text):
    """PR link(s) out of a merge-request frontmatter block. No YAML dep
    (matching parse_frontmatter_keys above) — handles every format this
    board has used: a `pr_urls:` list of `{repo, url}` pairs (current,
    multi-repo), a quoted `pr_url: "repo: url | repo: url"` string
    (superseded), and a flat `pr_url:`/`pr:` single URL (single-repo)."""
    m = re.search(r"^[ \t]*pr_urls:[ \t]*\n((?:[ \t]+-.*\n(?:[ \t]+\S.*\n)*)+)",
                  fm_text, re.MULTILINE)
    if m:
        links = [{"repo": repo, "url": url} for repo, url in
                 re.findall(r"-\s*repo:\s*(\S+)\s*\n\s*url:\s*(\S+)", m.group(1))]
        if links:
            return links

    m = re.search(r"^[ \t]*pr_url:[ \t]*(.+)$", fm_text, re.MULTILINE)
    if not m:
        m = re.search(r"^[ \t]+pr:[ \t]*(\S+)[ \t]*$", fm_text, re.MULTILINE)
    if not m:
        return []
    val = m.group(1).strip().strip('"').strip("'")
    if not val:
        return []
    return [_split_pr_part(p) for p in val.split("|") if p.strip()]


def read_file_content(rel_path):
    """Read a file relative to ROOT. Returns {frontmatter, body, raw}."""
    path = ROOT / rel_path
    if not path.exists():
        return None
    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", raw, re.DOTALL)
    if m:
        return {"frontmatter": m.group(1).strip(), "body": m.group(2).strip(), "raw": raw}
    return {"frontmatter": "", "body": raw.strip(), "raw": raw}


def update_frontmatter_key(raw, key, value):
    """Replace `key: anything` in the frontmatter block with `key: value`,
    or insert it just inside the opening `---` if it isn't there yet."""
    pattern = re.compile(rf"^({re.escape(key)}:\s*).*$", re.MULTILINE)
    if pattern.search(raw):
        return pattern.sub(rf"\g<1>{value}", raw, count=1)
    return re.sub(r"^(---\n)", rf"\1{key}: {value}\n", raw, count=1)


def _read_frontmatter(path, keys):
    """Frontmatter + body for a ticket-shaped markdown file."""
    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", raw, re.DOTALL)
    fm_text, body = (m.group(1), m.group(2).strip()) if m else ("", raw.strip())
    return parse_frontmatter_keys(fm_text, keys), body


def _fm_set(fm, key, value):
    """Set a frontmatter key, replacing an existing (often blank) one in
    place rather than appending a duplicate."""
    pat = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    if pat.search(fm):
        return pat.sub(f"{key}: {value}", fm, count=1)
    return fm.rstrip() + f"\n{key}: {value}"


def _days_since(date_str, fallback_mtime=None):
    """Days elapsed since a YYYY-MM-DD string (found anywhere in the value —
    tolerates ISO timestamps). Falls back to a file mtime. None if neither."""
    ts = None
    if date_str:
        m = re.search(r"\d{4}-\d{2}-\d{2}", date_str)
        if m:
            try:
                ts = datetime.strptime(m.group(0), "%Y-%m-%d").timestamp()
            except ValueError:
                ts = None
    if ts is None and fallback_mtime:
        ts = fallback_mtime
    if ts is None:
        return None
    return max(0, int((time.time() - ts) / 86400))


# ── Business instances ──────────────────────────────────────────────────────
# business-os is a template + per-business instance system (docs at
# agents/architect/designs/business-os-engineering-department-carveout.md).
# Every business Harry runs shows up under instances/{id}/ — Engineering and
# Sales both select against this same roster, so onboarding a business once
# makes it available everywhere rather than per-tab.

INSTANCES_DIR = ROOT / "instances"


def _business_label(inst_dir):
    """The business's own name for itself, not a title-cased directory name.

    `knowledge/business-profile.md` opens with `**Business:** AIOrders (…)` —
    naive title-casing renders it "Aiorders", visibly wrong on the one
    control whose entire job is telling Harry which business he's looking
    at."""
    prof = inst_dir / "knowledge" / "business-profile.md"
    if prof.exists():
        try:
            m = re.search(r"^\*\*Business:\*\*\s*(.+?)(?:\s*\(|\s*—|$)",
                          prof.read_text(), re.MULTILINE)
            if m and m.group(1).strip():
                return m.group(1).strip()[:40]
        except Exception:
            pass  # an unreadable profile costs a nice label, not the tab
    return inst_dir.name.replace("-", " ").replace("_", " ").title()


def _instance_dirs():
    """Every instance directory the ACTING USER may see, in one place.

    Role scoping lives here rather than at each API handler on purpose. There
    are five instance rosters in this file and a partner-visible endpoint that
    forgot to filter would be a silent cross-tenant leak — the exact defect
    class the engineering board has spent three tickets closing in the product
    itself (ENG-015, ENG-022). One choke point, and every roster below is a
    caller of it. accounts.filter_instance_dirs returns everything for an
    admin, and only the assigned ids for a partner."""
    if not INSTANCES_DIR.is_dir():
        return []
    dirs = sorted(p for p in INSTANCES_DIR.iterdir() if p.is_dir())
    return accounts.filter_instance_dirs(dirs)


def business_instances():
    """Every business this control center knows about, rebuilt per request —
    onboarding one shouldn't need a server restart to show up."""
    return [{"id": d.name, "label": _business_label(d)} for d in _instance_dirs()]


def _resolve_instance_id(instance_id):
    known = business_instances()
    if instance_id:
        for i in known:
            if i["id"] == instance_id:
                return i["id"]
    return known[0]["id"] if known else None


# ── Engineering view ─────────────────────────────────────────────────────────
# Ported from life-os's control-center (which, post carve-out, already reads
# THIS repo's departments/instances directly). Re-rooted here so the same
# view works with no sibling repo to reach into. See docs/engineering-team.md
# for the pipeline and gates, unchanged by the port.

ENG_DEPT_DIR = ROOT / "departments" / "engineering"
ENG_TRIGGER_SCRIPT = ENG_DEPT_DIR / "lib" / "eng-trigger.sh"

TICKET_KEYS = ["id", "title", "project", "type", "size", "severity", "state",
               "owner", "lane", "blocked_on", "source", "created", "updated",
               "branch", "priority", "time_estimate", "time_spent", "time_remaining"]

# Harry's ordering lever, and deliberately not `severity`. Severity is the
# agent's read of how bad a problem is; priority is his instruction about
# what to work first. Empty is the default and means the EM orders it.
ENG_PRIORITIES = ["now", "next", "hold"]
ENG_PRIORITY_WORKING_STATES = {"ready", "building", "in-review", "in-qa",
                               "in-security", "ready-to-ship"}

ENG_STATES = ["intake", "shaped", "awaiting-scope", "designed", "awaiting-decision",
              "ready", "building", "in-review", "in-qa", "in-security",
              "ready-to-ship", "awaiting-release", "shipped", "verified",
              "advised", "blocked", "dropped"]
ENG_WAITING_STATES = {"awaiting-scope", "awaiting-decision", "awaiting-release"}


def eng_instances():
    """Every engineering board this server can show — one per business that
    has actually been instantiated (`config/instantiated-from` is
    install.sh's marker). A dir without it is a half-made instance, not a
    board — listing it would offer a selector option whose every action
    then fails."""
    out = []
    for d in _instance_dirs():
        eng = d / "engineering"
        if not (eng / "config" / "instantiated-from").exists():
            continue
        out.append({
            "id": d.name,
            "label": _business_label(d),
            "root": ROOT,
            "board": eng / "agents" / "eng-manager" / "board",
            "bugs": eng / "agents" / "qa" / "bugs" / "_index.md",
            "pm_inbox": eng / "agents" / "product-manager" / "inbox",
            # The approver's decision inbox and the filer's intake queue —
            # an instance has both; a filer (a cofounder, via Telegram)
            # writes `inbox/requests/` directly.
            "inbox": eng / "inbox",
            "requests": eng / "inbox" / "requests",
            "config": eng / "config" / "config.yaml",
            "trigger": ENG_TRIGGER_SCRIPT,
            "env": {"ENG_DEPT": str(ENG_DEPT_DIR), "ENG_INSTANCE": str(eng)},
        })
    return out


def eng_instance(instance_id=None):
    """Resolve an instance id to its paths, falling back to the first known
    instance. An unknown id falls back rather than erroring — the id arrives
    from a value the browser remembered, so a business that was renamed or
    removed shouldn't leave the tab permanently broken."""
    known = eng_instances()
    if instance_id:
        for i in known:
            if i["id"] == instance_id:
                return i
    return known[0] if known else None


def list_engineering(instance_id=None):
    """Board tickets, open bugs, and every engineering decision waiting on
    Harry, for ONE business's engineering instance."""
    inst = eng_instance(instance_id)
    if not inst:
        return {"instance": None, "instances": [], "tickets": [], "by_state": {},
                "states": ENG_STATES, "bugs": [], "waiting": [], "blocked_on_harry": [],
                "deciding": [], "submitted": [],
                "stats": {"waiting_on_harry": 0, "in_flight": 0, "pending_apply": 0,
                          "machine_limit": 0, "open_bugs": 0, "shipped_recent": 0},
                "empty": "No engineering instance yet — run departments/engineering/install.sh "
                         "to onboard a business."}

    board_dir, bugs_index = inst["board"], inst["bugs"]
    pm_inbox, decisions_inbox = inst["pm_inbox"], inst["inbox"]
    inst_root = inst["root"]

    tickets = []
    if board_dir.exists():
        for f in sorted(board_dir.glob("*.md")):
            if f.name.startswith("_"):
                continue
            fm, body = _read_frontmatter(f, TICKET_KEYS)
            if not fm.get("id"):
                continue
            problem = ""
            pm = re.search(r"^##\s+Problem\s*\n+(.+?)(?=\n#|\Z)", body,
                           re.DOTALL | re.MULTILINE)
            if pm:
                problem = " ".join(pm.group(1).split())[:280]
            pr_m = re.search(r"^[ \t]+pr:[ \t]*(\S+)[ \t]*$", f.read_text(),
                             re.MULTILINE)
            tickets.append({
                "id": fm.get("id", ""),
                "title": fm.get("title", f.stem),
                "project": fm.get("project", ""),
                "type": fm.get("type", ""),
                "size": fm.get("size", ""),
                "severity": fm.get("severity", ""),
                "priority": fm.get("priority", ""),
                "state": fm.get("state", "intake"),
                "owner": fm.get("owner", ""),
                "lane": fm.get("lane", "full"),
                "blocked_on": fm.get("blocked_on", ""),
                "updated": fm.get("updated", ""),
                "branch": fm.get("branch", ""),
                "time_estimate": fm.get("time_estimate", ""),
                "time_spent": fm.get("time_spent", ""),
                "time_remaining": fm.get("time_remaining", ""),
                "problem": problem,
                "pr_url": pr_m.group(1) if pr_m else "",
                "path": str(f.relative_to(inst_root)),
            })

    bugs = []
    if bugs_index.exists():
        in_open = False
        for line in bugs_index.read_text().split("\n"):
            h = re.match(r"^##\s+(.+)$", line)
            if h:
                in_open = h.group(1).strip().lower() == "open"
                continue
            if not in_open or not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 6 or cells[0] in ("ID", "—") or set(cells[0]) <= {"-", ":"}:
                continue
            bugs.append({"id": cells[0], "title": cells[1], "project": cells[2],
                         "severity": cells[3], "owner": cells[4], "age": cells[5]})

    waiting = []
    deciding = []
    if decisions_inbox.exists():
        for f in sorted(decisions_inbox.glob("*.md")):
            fm, body = _read_frontmatter(
                f, ["type", "gate", "ticket", "project", "recommendation",
                    "raised", "pr_url", "decision", "decided",
                    "time_estimate", "time_impact"])
            if fm.get("type") != "eng-decision":
                continue
            # PR link(s) live in the frontmatter in one of three formats
            # (see _parse_pr_links) — read straight from the raw file since
            # parse_frontmatter_keys only pulls flat single-line values and
            # can't see the `pr_urls:` YAML-list form multi-repo tickets use.
            raw = f.read_text()
            fm_m = re.match(r"^---\n(.*?)\n---\n?", raw, re.DOTALL)
            pr_links = _parse_pr_links(fm_m.group(1) if fm_m else raw)
            if fm.get("decision"):
                deciding.append({
                    "file": f.name,
                    "gate": fm.get("gate", ""),
                    "ticket": fm.get("ticket", ""),
                    "project": fm.get("project", ""),
                    "decision": fm.get("decision", ""),
                    "decided": fm.get("decided", ""),
                    "recommendation": fm.get("recommendation", ""),
                    "pr_links": pr_links,
                    # The full readback/recommendation text — dropped from this
                    # payload before, which is exactly why the text you just
                    # approved became unreadable the moment it moved out of
                    # "Waiting on you": the API response never carried it.
                    "body": body,
                })
                continue
            waiting.append({
                "file": f.name,
                "gate": fm.get("gate", ""),
                "ticket": fm.get("ticket", ""),
                "project": fm.get("project", ""),
                "recommendation": fm.get("recommendation", ""),
                "raised": fm.get("raised", ""),
                "pr_links": pr_links,
                "time_estimate": fm.get("time_estimate", ""),
                "time_impact": fm.get("time_impact", ""),
                "body": body,
            })

    submitted = []
    for queue, origin in ((pm_inbox, "sent"), (inst.get("requests"), "filed")):
        if not queue or not queue.exists():
            continue
        for f in sorted(queue.glob("*.md")):
            fm, body = _read_frontmatter(f, ["source", "via", "received"])
            title_m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            submitted.append({
                "file": f.name,
                "title": title_m.group(1).strip() if title_m else f.stem,
                "received": fm.get("received", ""),
                "origin": origin,
                "source": fm.get("source", ""),
            })

    by_state = {}
    for t in tickets:
        by_state.setdefault(t["state"], []).append(t)

    in_flight = [t for t in tickets
                 if t["state"] in {"ready", "building", "in-review", "in-qa",
                                   "in-security", "ready-to-ship"}]
    # A ticket blocked on the approver (e.g. an L1 merge request) already has
    # its own inbox item — in `waiting` while undecided, in `deciding` once
    # answered but not yet cleared (merge not detected/marked yet). Either way
    # that item IS the decide card. Without this filter the same PR showed
    # twice: once here, once in the inbox-item list. Only show a ticket here
    # when it's blocked on the approver for something that never got an inbox
    # item (a risk acceptance, a direct question) — nothing else surfaces it.
    inbox_item_tickets = {w["ticket"] for w in waiting + deciding if w.get("ticket")}
    blocked_on_harry = [t for t in tickets
                        if t["state"] == "blocked" and t["blocked_on"] == "approver"
                        and t["id"] not in inbox_item_tickets]

    limits = eng_limits(inst)
    return {
        "instance": inst["id"],
        "instances": [{"id": i["id"], "label": i["label"]} for i in eng_instances()],
        "tickets": tickets,
        "by_state": by_state,
        "states": ENG_STATES,
        "bugs": bugs,
        "waiting": waiting,
        "blocked_on_harry": [
            {"id": t["id"], "title": t["title"], "project": t["project"],
             "updated": t["updated"], "pr_url": t["pr_url"], "path": t["path"]}
            for t in blocked_on_harry
        ],
        "deciding": deciding,
        "submitted": submitted,
        "activity": eng_activity(inst),
        "stats": {
            "waiting_on_harry": len(waiting) + len(blocked_on_harry),
            "in_flight": len(in_flight),
            "pending_apply": len(deciding),
            "machine_limit": limits["machine_limit"],
            "open_bugs": len(bugs),
            "shipped_recent": len(by_state.get("verified", [])),
        },
    }


def eng_intake(title, description, instance_id=None):
    """Write a business need to the Product Manager's inbox for one instance.
    The PM is the department's front door — it shapes the request into a
    ticket. Nothing here creates a ticket directly."""
    title = (title or "").strip()
    if not title:
        return None, "title required"
    inst = eng_instance(instance_id)
    if not inst:
        return None, "no engineering instance"
    pm_inbox = inst["pm_inbox"]
    pm_inbox.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or "request"
    stamp = datetime.now().strftime("%Y-%m-%d")
    path = pm_inbox / f"{stamp}-{slug}.md"
    n = 2
    while path.exists():
        path = pm_inbox / f"{stamp}-{slug}-{n}.md"
        n += 1
    path.write_text(
        "---\n"
        "source: approver\n"
        "via: control-center\n"
        f"received: {datetime.now(timezone.utc).isoformat()}\n"
        "---\n\n"
        f"# {title}\n\n"
        f"{(description or '').strip()}\n"
    )
    return str(path.relative_to(inst["root"])), None


def eng_priority(ticket_id, priority, instance_id=None):
    """Set Harry's ordering lever on a board ticket, in the ticket itself."""
    ticket_id = (ticket_id or "").strip().upper()
    if not re.fullmatch(r"ENG-\d+", ticket_id):
        return None, "invalid ticket id"
    priority = (priority or "").strip().lower()
    if priority and priority not in ENG_PRIORITIES:
        return None, f"priority must be empty or one of: {', '.join(ENG_PRIORITIES)}"

    inst = eng_instance(instance_id)
    if not inst:
        return None, "no engineering instance"
    matches = [f for f in inst["board"].glob(f"{ticket_id}-*.md")
               if not f.name.startswith("_")]
    if len(matches) != 1:
        return None, "ticket not found" if not matches else "ambiguous ticket id"
    path = matches[0]

    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", raw, re.DOTALL)
    if not m:
        return None, "ticket has no frontmatter"
    fm, body = m.group(1), m.group(2)

    state = ""
    sm = re.search(r"^state:[ \t]*(\S+)", fm, re.MULTILINE)
    if sm:
        state = sm.group(1)

    if priority == "hold" and state in ENG_PRIORITY_WORKING_STATES:
        return None, (f"{ticket_id} is at `{state}` — the machine is working it now. "
                      f"Holding it means stopping mid-flight; unwind it to a clean "
                      f"state first.")

    fm = _fm_set(fm, "priority", priority)
    fm = _fm_set(fm, "updated", datetime.now().strftime("%Y-%m-%d"))
    path.write_text(f"---\n{fm}\n---\n{body}")
    return {"ticket": ticket_id, "priority": priority,
            "path": str(path.relative_to(inst["root"]))}, None


ENG_WORKTREES = Path.home() / "Documents" / "projects" / "_eng"


def _default_branch(worktree):
    """The remote's own default branch, asked rather than assumed —
    restaurant-marketplace uses `master` where the rest use `main`."""
    r = subprocess.run(["git", "-C", str(worktree), "symbolic-ref",
                        "refs/remotes/origin/HEAD"],
                       capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip().rsplit("/", 1)[-1]
    for cand in ("main", "master"):
        probe = subprocess.run(["git", "-C", str(worktree), "rev-parse",
                                "--verify", f"origin/{cand}"],
                               capture_output=True, text=True)
        if probe.returncode == 0:
            return cand
    return None


def eng_merge_check(ticket_id, force=False, instance_id=None):
    """Has this ticket's PR landed? Advance it to `shipped` if so. Local git
    ancestry only — no API call, no token."""
    ticket_id = (ticket_id or "").strip().upper()
    if not re.fullmatch(r"ENG-\d+", ticket_id):
        return None, "invalid ticket id"

    inst = eng_instance(instance_id)
    if not inst:
        return None, "no engineering instance"
    matches = [f for f in inst["board"].glob(f"{ticket_id}-*.md")
               if not f.name.startswith("_")]
    if len(matches) != 1:
        return None, "ticket not found" if not matches else "ambiguous ticket id"
    path = matches[0]
    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", raw, re.DOTALL)
    if not m:
        return None, "ticket has no frontmatter"
    fm, body = m.group(1), m.group(2)

    def fld(k):
        mm = re.search(rf"^{k}:[ \t]*(.*)$", fm, re.MULTILINE)
        return re.sub(r"\s+#.*$", "", mm.group(1)).strip() if mm else ""

    state, project, branch = fld("state"), fld("project"), fld("branch")
    if state != "blocked":
        return None, f"{ticket_id} is at `{state}`, not blocked on a PR"
    if not branch:
        return None, f"{ticket_id} has no `branch:` — nothing to check"

    merged, detail = False, ""
    if force:
        detail = "recorded on Harry's say-so; ancestry not consulted"
    else:
        worktree = ENG_WORKTREES / project
        if not worktree.exists():
            return None, f"no worktree at {worktree} — cannot check, use 'mark merged'"
        base = _default_branch(worktree)
        if not base:
            return None, "could not resolve the remote's default branch"
        subprocess.run(["git", "-C", str(worktree), "fetch", "origin", "--quiet"],
                       capture_output=True, text=True, timeout=60)
        anc = subprocess.run(
            ["git", "-C", str(worktree), "merge-base", "--is-ancestor",
             branch, f"origin/{base}"], capture_output=True, text=True)
        merged = anc.returncode == 0
        detail = f"`{branch}` {'is' if merged else 'is not'} an ancestor of `origin/{base}`"
        if not merged:
            return {"ticket": ticket_id, "merged": False, "detail": detail,
                    "hint": "If you merged with squash or rebase the branch head "
                            "will never become an ancestor — use 'mark merged'."}, None

    fm = _fm_set(fm, "state", "shipped")
    fm = _fm_set(fm, "blocked_on", "")
    fm = _fm_set(fm, "blocked_from", "")
    fm = _fm_set(fm, "updated", datetime.now().strftime("%Y-%m-%d"))
    stamp = datetime.now().strftime("%Y-%m-%d")
    body = body.rstrip() + (
        f"\n\n- `{stamp}` `blocked → shipped` (control center, merge detected) — "
        f"{detail}. Advanced from the dashboard rather than by a build-loop pass; "
        f"the loop's own ancestry check on its next pass will agree.\n")
    path.write_text(f"---\n{fm}\n---\n{body}")

    handled = inst["inbox"] / "_handled"
    for f in inst["inbox"].glob("*.md"):
        t = f.read_text()
        if re.search(rf"^ticket:[ \t]*{ticket_id}\s*$", t, re.MULTILINE) and \
           re.search(r"^gate:[ \t]*merge\s*$", t, re.MULTILINE):
            handled.mkdir(parents=True, exist_ok=True)
            f.write_text(re.sub(r"^decision:[ \t]*$", "decision: merged", t,
                                count=1, flags=re.MULTILINE))
            f.rename(handled / f.name)
            break

    return {"ticket": ticket_id, "merged": True, "detail": detail,
            "state": "shipped"}, None


def eng_decide(filename, decision, note, instance_id=None):
    """Record Harry's answer on a gate item, in the item itself. `changed`
    requires a note — a scope Harry wants to *adjust*, not kill."""
    if decision not in ("approved", "rejected", "changed"):
        return None, "decision must be approved, rejected, or changed"
    note = (note or "").strip()
    if decision == "changed" and not note:
        return None, "note required when requesting changes"
    if not filename or "/" in filename or not filename.endswith(".md"):
        return None, "invalid file"
    inst = eng_instance(instance_id)
    if not inst:
        return None, "no engineering instance"
    path = inst["inbox"] / filename
    if not path.exists():
        return None, "item not found"
    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)", raw, re.DOTALL)
    if not m:
        return None, "item is not a decision file"
    fm, body = m.group(1), m.group(2)
    if re.search(r"^decision:[ \t]*\S", fm, re.MULTILINE):
        return None, "already decided"
    stamp = datetime.now(timezone.utc).isoformat()
    fm = _fm_set(fm, "decision", decision)
    fm = _fm_set(fm, "decided", stamp)
    body = body.rstrip() + f"\n\n## Decision\n\n**{decision}** — {stamp}\n"
    if note:
        body += f"\n{note}\n"
    path.write_text(f"---\n{fm}\n---\n{body}")
    return {"file": filename, "decision": decision}, None


def eng_limits(inst):
    """Read the WIP limits from this instance's config rather than
    hardcoding. business-os's own vocabulary (`approver_limit`) — "harry"
    isn't a word a shared template can use. There is deliberately no cap on
    how many decisions may be waiting at once (the awaiting-approver queue
    cap was a life-os holdover business-os doesn't use, removed 2026-08-29) —
    `approver_limit` is the one WIP lever on the approver's side, and it's a
    limit on tickets in flight, not on decisions queued."""
    defaults = {"approver_limit": 2, "machine_limit": 6}
    cfg = inst["config"]
    if not cfg.exists():
        return defaults
    try:
        text = cfg.read_text()
        block = re.search(r"^wip:\n(.*?)(?=^\S)", text, re.MULTILINE | re.DOTALL)
        scope = block.group(1) if block else text
        for key in defaults:
            m = re.search(rf"^\s+{key}:\s*(\d+)", scope, re.MULTILINE)
            if m:
                defaults[key] = int(m.group(1))
    except Exception:
        pass  # a malformed config must not take the dashboard down
    return defaults


def _pid_alive(pid):
    """Ask the SAME check `lib/eng-trigger.sh`'s own `acquire()` uses
    (`kill -0` under Git Bash), not a Windows-native tool. The PID in
    `.loop.lock/pid` is bash's own `$$` — under Git Bash that is an
    MSYS-namespace PID, which `tasklist` cannot reliably resolve, so a
    `tasklist`-based check can disagree with the script that actually holds
    the lock and report a live pass as dead. That's a worse failure than a
    slow status readout: it's the same false-status problem the WSL bug
    caused, one layer up. On error, assume alive rather than falsely tell
    the approver a live pass has died — this only feeds a status readout,
    never a decision that deletes or steals anything."""
    if os.name == "nt":
        try:
            bash = _resolve_windows_bash()
            r = subprocess.run([bash, "-c", f"kill -0 {int(pid)} 2>/dev/null"], timeout=5)
            return r.returncode == 0
        except Exception:
            return True
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except Exception:
        return True


def eng_activity(inst):
    """What `lib/eng-trigger.sh` is actually doing right now, for one
    instance — not what the board says, which only updates once a pass
    finishes. Reads the same `traces/` state the trigger script itself reads
    (`.loop.lock`, `.pending`, `.hops-*`, `.backoff`), so this is a live
    readout, not a derived guess. Every field is read straight off disk and
    every read is wrapped — a missing or half-written file (a pass is
    writing it right now) must not take the dashboard down; it just shows as
    "unknown" for that one field rather than a 500."""
    root = Path(inst["env"]["ENG_INSTANCE"])
    state = root / "traces"
    today = datetime.now().strftime("%Y-%m-%d")
    # Same resolution eng-env.sh's ENG_MODE uses: this instance's own
    # config/config.yaml `mode:` wins if set, else the business-os-wide
    # .env MODE is the default. Reading only the global var here (as this
    # used to) shows the wrong value once an instance sets its own override.
    eng_mode = ""
    try:
        cfg_text = (root / "config" / "config.yaml").read_text()
        m = re.search(r"^mode:[ \t]*([^\s#]*)", cfg_text, re.MULTILINE)
        if m:
            eng_mode = m.group(1)
    except Exception:
        pass
    if not eng_mode:
        eng_mode = os.environ.get("MODE", "")
    out = {
        "mode": eng_mode,
        # Only sabbath/retreat/quiet actually halt anything (eng_mode_halts
        # in eng-env.sh) — every other value, "active" included, is normal
        # operation. The dashboard used to warn on ANY non-empty MODE, which
        # made "active" (the normal, running value) look like an outage.
        "mode_halting": eng_mode in ("sabbath", "retreat", "quiet"),
        "running": False, "pid": None, "running_seconds": None, "current_event": "",
        "current_ticket": None, "current_activity": "",
        "pending_count": 0, "pending_preview": [],
        "hops_today": 0, "hops_budget": None, "refunds_today": 0,
        "backoff_active": False, "backoff_seconds": None,
        "recent_log": [],
    }
    if not state.is_dir():
        return out

    lock = state / ".loop.lock"
    if lock.is_dir():
        try:
            out["pid"] = int((lock / "pid").read_text(encoding="utf-8").strip())
            out["running"] = _pid_alive(out["pid"])
            out["running_seconds"] = max(0, int(time.time() - lock.stat().st_mtime))
        except Exception:
            pass

    pending = state / ".pending"
    if pending.exists():
        try:
            lines = [l for l in pending.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
            out["pending_count"] = len(lines)
            for l in lines[:8]:
                parts = l.split(" ", 2)
                out["pending_preview"].append({
                    "event": parts[1] if len(parts) > 1 else l,
                    "context": (parts[2][:80] if len(parts) > 2 else ""),
                })
        except Exception:
            pass

    try:
        out["hops_today"] = int((state / f".hops-{today}").read_text(encoding="utf-8").strip() or 0)
    except Exception:
        pass
    try:
        out["refunds_today"] = int((state / f".refunds-{today}").read_text(encoding="utf-8").strip() or 0)
    except Exception:
        pass

    try:
        cfg_text = (ENG_DEPT_DIR / "agents" / "eng-manager" / "config.yaml").read_text(encoding="utf-8")
        tier_m = re.search(r"^\s*tier:\s*(\S+)", cfg_text, re.MULTILINE)
        if tier_m:
            # Capture only the lines directly under `    <tier>:` that are
            # indented one level deeper (6 spaces) — stops at the next sibling
            # tier or any less-indented line, wherever this tier falls in the
            # file, without relying on DOTALL reaching a lookahead that may
            # never match (e.g. the last tier in the block).
            block = re.search(rf"^    {re.escape(tier_m.group(1))}:\n((?:^ {{6}}.*\n?)*)",
                              cfg_text, re.MULTILINE)
            if block:
                hpd = re.search(r"hops_per_day:\s*(\d+)", block.group(1))
                if hpd:
                    out["hops_budget"] = int(hpd.group(1))
    except Exception:
        pass

    backoff = state / ".backoff"
    if backoff.exists():
        try:
            until = int(backoff.read_text(encoding="utf-8").split()[0])
            if until > time.time():
                out["backoff_active"] = True
                out["backoff_seconds"] = int(until - time.time())
        except Exception:
            pass

    log_f = state / f"eng-loop-{today}.log"
    if log_f.exists():
        try:
            lines = log_f.read_text(encoding="utf-8", errors="replace").splitlines()
            timestamped = [l for l in lines if re.match(r"^\[\d{4}-\d{2}-\d{2}", l)]
            out["recent_log"] = timestamped[-6:]
            for l in reversed(timestamped):
                # 2026-08-29: was `(\S+)` — captured only the event TYPE
                # ("continue", "decision", "scheduled"...) and silently
                # dropped the context in parens right next to it, which is
                # the one thing that actually names a ticket ("continue
                # (ENG-011)") or a gate file ("decision
                # (2026-08-29-eng008-g1-scope.md)"). Every line ends
                # " [day N/40 charged..." (added by ENG-005's hop-accounting
                # work), so that is the real stop point, not the first space.
                m = re.search(r"pass start: (.+?)(?:\s*\[day\b|\s*$)", l)
                if m:
                    out["current_event"] = m.group(1)
                    tm = re.search(r"ENG-\d+", out["current_event"])
                    if tm:
                        out["current_ticket"] = tm.group(0)
                    break
        except Exception:
            pass

    if out["running"] and out["pid"]:
        out["current_activity"] = _activity_snippet(state, out["pid"])

    return out


def _activity_snippet(state, pid):
    """Last human-readable line of the currently running pass's own
    transcript (`traces/.pass-out.<pid>`, written by `lib/run-stream.py`) —
    the closest thing to a live "is it building, testing, reviewing..."
    readout that exists, short of teaching the trigger a separate phase/role
    field it does not track today: one Claude session does design, code, and
    test verification all in the same pass, guided by the ticket's own state
    rather than a labelled hand-off between roles. Tool-call markers
    ("· Bash", "· Read", ...) and rate-limit markers ("·· ...") carry no
    information on their own, so the last non-marker line of prose is what
    gets surfaced. Wrapped like every other read in this function: a pass
    writing this same file right now must not take the dashboard down."""
    f = state / f".pass-out.{pid}"
    if not f.is_file():
        return ""
    try:
        with open(f, "rb") as fh:
            fh.seek(0, os.SEEK_END)
            size = fh.tell()
            fh.seek(max(0, size - 4000))
            tail = fh.read().decode("utf-8", errors="replace")
    except Exception:
        return ""
    for line in reversed(tail.splitlines()):
        s = line.strip()
        if not s or s.startswith("·"):
            continue
        # Generous cap — just a DOM-size guard against one freak unwrapped
        # line, not the visual boundary. The frontend's own 2-line CSS clamp
        # (.now-line) is what decides where this actually gets cut, so it
        # ends at a real line edge with an ellipsis instead of mid-word at a
        # fixed offset that had no relationship to the rendered width.
        return s[:600]
    return ""


def _resolve_windows_bash():
    """Git Bash's bash.exe, resolved explicitly rather than left as a bare
    "bash" string. subprocess.run(["bash", ...]) hands that to Windows'
    CreateProcess, which searches C:\\Windows\\System32 BEFORE consulting
    PATH for a bare command name — and System32\\bash.exe is the WSL launcher
    stub, not a shell. A trigger fired through it dies instantly with "Windows
    Subsystem for Linux has no installed distributions" (this is what an
    approved decision — e.g. ENG-007 — hit). lib/eng-schedule-win.sh fought
    the identical landmine on the Task Scheduler side; same fix here: never
    hand Windows a bare "bash" and hope PATH order saves you.
    """
    candidates = [os.environ.get("ENG_BASH_BIN", "")]
    for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")):
        if base:
            candidates.append(os.path.join(base, "Git", "bin", "bash.exe"))
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    # shutil.which walks PATH in order (unlike CreateProcess, it does not
    # special-case System32), so it normally finds Git's bash.exe first — but
    # reject it anyway if PATH somehow put the WSL stub ahead of Git.
    found = shutil.which("bash")
    if found and "system32" not in found.lower():
        return found
    return "bash"  # nothing found; let it fail loudly rather than silently


TRIGGER_SHELL = _resolve_windows_bash() if os.name == "nt" else ("/bin/zsh" if os.uname().sysname == "Darwin" else "/bin/bash")


def _spawn_trigger(script, args, label, env=None):
    """Run a repo trigger script in the background, loudly — a trigger that
    silently fails to start is indistinguishable from a quiet day."""
    def _run():
        try:
            child_env = {**os.environ, **env} if env else None
            proc = subprocess.run([TRIGGER_SHELL, str(script), *args],
                                  check=False, env=child_env)
            if proc.returncode != 0:
                print(f"[control-center] {label} exited {proc.returncode}")
        except Exception as e:
            print(f"[control-center] {label} FAILED TO START: {e}")
    threading.Thread(target=_run, daemon=True).start()


def fire_eng_trigger(event, context="", instance_id=None):
    """Run an engineering build-loop pass now instead of waiting for the next
    scheduled one. The script holds a single-flight lock, so firing this
    while a pass is running is a safe no-op."""
    inst = eng_instance(instance_id)
    if not inst:
        return
    script = inst["trigger"]
    if not script.exists():
        print(f"[control-center] eng {event}: no trigger at {script}")
        return
    _spawn_trigger(script, [event, context], f"eng {event} [{inst['id']}]",
                   env=inst["env"])


# ── Sales pipeline view ─────────────────────────────────────────────────────
# A generic stage-folder CRM funnel, per business instance. No channel
# coupling — a lead's `source` field is freeform text, not a fixed vocabulary.
# No sales agent writes into this yet (Harry, 2026-08-28: build the agent
# later) — until one exists, this tab is also the only way leads get in, so
# create/edit live here alongside move.

PIPELINE_STAGES = ["1-signal", "2-qualified", "3-contacted", "4-engaged",
                   "5-proposal-sent", "6-negotiating", "7-closed/won", "7-closed/lost"]
LEAD_KEYS = ["lead_id", "contact", "company", "stage", "source", "status_note",
             "estimated_value", "last_touch", "next_action_due", "icp_segment",
             "contract_end_date", "custom_cadence"]
ACTIVE_VALUE_STAGES = {"2-qualified", "3-contacted", "4-engaged",
                       "5-proposal-sent", "6-negotiating"}


def sales_pipeline_dir(instance_id):
    return INSTANCES_DIR / instance_id / "sales" / "pipeline"


def _list_funnel(pipeline_dir, stages, keys, value_field, active_value_stages):
    """Generic stage-column funnel reader — a directory of stage subfolders
    holding frontmatter'd markdown leads."""
    today = datetime.now().strftime("%Y-%m-%d")
    stage_list = []
    total_value = 0
    for stage in stages:
        stage_dir = pipeline_dir / stage
        items = []
        if stage_dir.exists():
            for f in sorted(stage_dir.glob("*.md")):
                raw = f.read_text()
                m = re.match(r"^---\n(.*?)\n---\n?(.*)", raw, re.DOTALL)
                fm_text, body = (m.group(1), m.group(2).strip()) if m else ("", raw.strip())
                fm = parse_frontmatter_keys(fm_text, keys)
                value = 0
                if fm.get(value_field):
                    vm = re.search(r"\d[\d,]*", fm[value_field])
                    if vm:
                        value = int(vm.group(0).replace(",", ""))
                if stage in active_value_stages:
                    total_value += value
                due = fm.get("next_action_due", "")
                items.append({
                    "path": str(f.relative_to(ROOT)),
                    "slug": f.stem,
                    "contact": fm.get("contact", ""),
                    "company": fm.get("company", ""),
                    "status_note": fm.get("status_note", ""),
                    "source": fm.get("source", ""),
                    "value": value,
                    "days_since_touch": _days_since(fm.get("last_touch"), f.stat().st_mtime),
                    "next_action_due": due,
                    "action_overdue": bool(due) and (due == "today" or due <= today),
                    "icp_segment": fm.get("icp_segment", ""),
                    "last_touch": fm.get("last_touch", ""),
                    "contract_end_date": fm.get("contract_end_date", ""),
                    "custom_cadence": fm.get("custom_cadence", ""),
                    "body": body,
                })
        stage_list.append({"name": stage, "leads": items})
    return stage_list, total_value


def list_sales(instance_id=None):
    inst_id = _resolve_instance_id(instance_id)
    if not inst_id:
        return {"instance": None, "instances": [], "stages": [], "total_value": 0,
                "empty": "No business instance yet."}
    stages, total_value = _list_funnel(
        sales_pipeline_dir(inst_id), PIPELINE_STAGES, LEAD_KEYS,
        "estimated_value", ACTIVE_VALUE_STAGES)
    return {"instance": inst_id,
            "instances": business_instances(),
            "stages": stages, "total_value": total_value}


def sales_create_lead(instance_id, fields):
    inst_id = _resolve_instance_id(instance_id)
    if not inst_id:
        return None, "no business instance"
    contact = (fields.get("contact") or "").strip()
    company = (fields.get("company") or "").strip()
    if not contact and not company:
        return None, "contact or company required"
    slug_src = contact or company
    slug = re.sub(r"[^a-z0-9]+", "-", slug_src.lower()).strip("-")[:60] or "lead"
    stage_dir = sales_pipeline_dir(inst_id) / "1-signal"
    stage_dir.mkdir(parents=True, exist_ok=True)
    path = stage_dir / f"{slug}.md"
    n = 2
    while path.exists():
        path = stage_dir / f"{slug}-{n}.md"
        n += 1
    lead_id = path.stem
    today = datetime.now().strftime("%Y-%m-%d")
    fm_lines = [
        "---",
        f"lead_id: {lead_id}",
        f"contact: {contact}",
        f"company: {company}",
        "stage: 1-signal",
        f"source: {(fields.get('source') or '').strip()}",
        f"status_note: {(fields.get('status_note') or '').strip()}",
        f"estimated_value: {(fields.get('estimated_value') or '').strip()}",
        f"last_touch: {today}",
        "next_action_due:",
        f"icp_segment: {(fields.get('icp_segment') or '').strip()}",
        "contract_end_date:",
        "custom_cadence:",
        "---",
        "",
        f"### {today} — created",
        "Added by Harry in the control center.",
        "",
    ]
    path.write_text("\n".join(fm_lines))
    return {"slug": lead_id, "instance": inst_id}, None


def sales_update_lead(instance_id, slug, fields, note):
    inst_id = _resolve_instance_id(instance_id)
    if not inst_id:
        return None, "no business instance"
    if not re.match(r"^[\w-]+$", slug or ""):
        return None, "bad slug"
    base_dir = sales_pipeline_dir(inst_id)
    matches = list(base_dir.glob(f"*/{slug}.md")) + list(base_dir.glob(f"*/*/{slug}.md"))
    if not matches:
        return None, "lead not found"
    path = matches[0]
    raw = path.read_text()
    EDITABLE = ("contact", "company", "source", "status_note", "estimated_value",
                "next_action_due", "icp_segment", "contract_end_date", "custom_cadence")
    for key, value in (fields or {}).items():
        if key in EDITABLE:
            raw = update_frontmatter_key(raw, key, (value or "").strip())
    if note and note.strip():
        raw = update_frontmatter_key(raw, "last_touch", datetime.now().strftime("%Y-%m-%d"))
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        raw = raw.rstrip("\n") + f"\n\n### {stamp} — note\n{note.strip()}\n"
    path.write_text(raw)
    return {"slug": slug}, None


def sales_move_lead(instance_id, slug, to_stage):
    inst_id = _resolve_instance_id(instance_id)
    if not inst_id:
        return None, "no business instance"
    if not re.match(r"^[\w-]+$", slug or ""):
        return None, "bad slug"
    if to_stage not in PIPELINE_STAGES:
        return None, f"unknown stage {to_stage}"
    base_dir = sales_pipeline_dir(inst_id)
    matches = list(base_dir.glob(f"*/{slug}.md")) + list(base_dir.glob(f"*/*/{slug}.md"))
    if not matches:
        return None, "lead not found"
    lead_path = matches[0]
    from_stage = str(lead_path.parent.relative_to(base_dir))
    if from_stage == to_stage:
        return {"moved": False, "stage": to_stage}, None
    raw = update_frontmatter_key(lead_path.read_text(), "stage", to_stage)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    raw = raw.rstrip("\n") + f"\n\n### {stamp} — moved {from_stage} → {to_stage}\nMoved by Harry in the control center.\n"
    dest_dir = base_dir / to_stage
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / lead_path.name).write_text(raw)
    lead_path.unlink()
    return {"moved": True, "from": from_stage, "stage": to_stage}, None


# ── Marketing view (the marketing department) ────────────────────────────────
# Ported from life-os's control-center, re-rooted onto business-os's two-root
# department shape: MKT_DEPT is the read-only template, MKT_INSTANCE is the one
# thing written. See departments/marketing/config/conventions.yaml.
#
# Three views under one tab, and the split is deliberate. DECIDE is the only
# recurring human gate the whole system has (M2 — every piece, before it
# publishes), so it shows what is actually due and nothing else. CONTENT is the
# library, for looking rather than deciding. SETTINGS is the channel config,
# which sat as its own tab in life-os for a day and was wrong there: everything
# in it is a channel setting, and a channel picked in the dropdown should scope
# its settings exactly as it scopes its work.
#
# The channel roster is read out of the instance's config rather than hardcoded.
# life-os could name LinkedIn and X in a constant because life-os is one
# business; a department that ships to any business cannot.

MKT_DEPT_DIR = ROOT / "departments" / "marketing"

# A week. Long enough that nothing is a surprise, short enough that "due"
# still means due — a fortnight of pieces is a library, not a decision.
MKT_DUE_WINDOW_DAYS = 7

WEEKDAY_INDEX = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                 "friday": 4, "saturday": 5, "sunday": 6}
WEEKDAY_NAMES = ["monday", "tuesday", "wednesday", "thursday", "friday",
                 "saturday", "sunday"]

# The four stage folders, in lifecycle order. A stage folder is a location,
# not a gate — `status` is the gate — but shipped/ is terminal either way.
MKT_STAGES = ["drafts", "ready-to-send", "approved", "shipped"]

MKT_KEYS = ["status", "channel", "register", "kind", "archetype", "series",
            "stage", "planned_date", "scheduled_day", "image_format",
            "carousel_pdf", "format", "tweet_count", "shipped_at", "title"]

# What the Settings view may write. Anything outside this list is rendered
# read-only, because set_channel_field() would refuse it and a control that
# fails when clicked is worse than one that was never offered.
SETTINGS_WRITABLE = {
    "enabled":         "bool",
    "post_count":      "int",
    "publishing_days": "days",
    "publishing_time": "time",
}


def mkt_instances():
    """Every marketing instance this server can show — one per business that
    has actually been instantiated (`config/instantiated-from` is install.sh's
    marker, same test the engineering roster uses). A directory without it is
    a half-made instance, not a department."""
    out = []
    for d in _instance_dirs():
        mkt = d / "marketing"
        if not (mkt / "config" / "instantiated-from").exists():
            continue
        out.append({
            "id": d.name,
            "label": _business_label(d),
            "root": mkt,
            "config": mkt / "config" / "config.yaml",
            "content": mkt / "content",
            "topic_bank": mkt / "content" / "topic-bank.md",
        })
    return out


def mkt_instance(instance_id=None):
    """Resolve an instance id to its paths, falling back to the first known
    one. An unknown id falls back rather than erroring — it arrives from a
    value the browser remembered, so a business that was renamed shouldn't
    leave the tab permanently broken."""
    known = mkt_instances()
    if instance_id:
        for i in known:
            if i["id"] == instance_id:
                return i
    return known[0] if known else None


def _mkt_channel_blocks(cfg_path):
    """channel id -> the raw YAML lines under it in the instance config.

    Line scan, no YAML dependency — the same call eng_limits() makes, for the
    same reason: this server has none and shouldn't grow one to read a dozen
    scalars. It also means a config with a syntax error still renders the tab
    with whatever it could read, instead of 500ing the dashboard."""
    blocks, cur = {}, None
    if not cfg_path or not cfg_path.exists():
        return blocks
    try:
        lines = cfg_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return blocks
    in_channels = False
    for line in lines:
        if re.match(r"^channels:\s*$", line):
            in_channels = True
            continue
        if not in_channels:
            continue
        if line.strip() and not line.startswith(" "):
            break  # a new top-level key — the channels block is over
        m = re.match(r"^  ([a-z0-9_-]+):\s*$", line)
        if m:
            cur = m.group(1)
            blocks[cur] = []
            continue
        if cur is not None:
            blocks[cur].append(line)
    return {k: "\n".join(v) for k, v in blocks.items()}


def _mkt_scalar(block, key, default=""):
    """One scalar out of a channel block, comment and quotes stripped.

    Anchored on `key:` preceded only by whitespace, so a commented-out line can
    never be read as live config — which matters more here than usual, because
    these blocks carry long explanatory comments and some of them name a key
    precisely to say it is deliberately absent."""
    m = re.search(rf"^\s+{re.escape(key)}:[ \t]*([^#\n]*)", block, re.MULTILINE)
    if not m:
        return default
    return m.group(1).strip().strip('"').strip("'") or default


def _mkt_list(block, key):
    """An inline YAML list (`[a, b, c]`) out of a channel block."""
    raw = _mkt_scalar(block, key)
    if not raw.startswith("["):
        return []
    return [v.strip().strip('"').strip("'").lower()
            for v in raw.strip("[]").split(",") if v.strip()]


def _mkt_has(block, key):
    """Is this key actually SET on this channel, live (not in a comment)?

    The distinction between "absent" and "absent, so we defaulted it" is the
    whole point. `_mkt_scalar(block, 'publishing_time', '08:00')` returns
    '08:00' for a channel whose config never mentions a publishing time — fine
    for computing a next slot, wrong for telling someone what their config
    says, and actively misleading rendered as an editable field."""
    return re.search(rf"^\s+{re.escape(key)}:[ \t]", block, re.MULTILINE) is not None


def _mkt_label(cid):
    """A channel's display name. Config may carry one; otherwise the id,
    title-cased, with the two whose casing everyone already knows kept."""
    fixed = {"linkedin": "LinkedIn", "x": "X", "youtube": "YouTube",
             "tiktok": "TikTok", "reddit": "Reddit"}
    return fixed.get(cid, cid.replace("-", " ").replace("_", " ").title())


def _mkt_next_slot(days, hhmm):
    """The next date this channel can publish on, as (iso_date, human).

    An empty `days` means every weekday — a channel whose cadence lives in its
    ship routine's own schedule rather than in this config."""
    try:
        hour, minute = [int(x) for x in (hhmm or "08:00").split(":")[:2]]
    except Exception:
        hour, minute = 8, 0
    idx = sorted({WEEKDAY_INDEX[d] for d in days if d in WEEKDAY_INDEX})
    if not idx:
        idx = [0, 1, 2, 3, 4]
    now = datetime.now()
    for ahead in range(0, 14):
        day = now + timedelta(days=ahead)
        if day.weekday() not in idx:
            continue
        if ahead == 0 and (now.hour, now.minute) >= (hour, minute):
            continue  # today's slot has already passed
        label = "today" if ahead == 0 else ("tomorrow" if ahead == 1
                                            else day.strftime("%a %d %b"))
        return day.strftime("%Y-%m-%d"), f"{label} {hhmm or '08:00'}"
    return "", ""


def _mkt_channel_of(fm, known):
    """Which channel a piece belongs to.

    The `channel:` field decides. The register/format fallback below it exists
    because pieces written before a channel's field was introduced predate it
    entirely, and inferring `thread`/`tweet` avoids backfilling historical
    files to teach this tab one thing it can already derive. A piece that
    resolves to nothing keeps an empty channel rather than being assigned to
    whichever channel happens to be first — guessing here would put a piece on
    the wrong channel's approval list."""
    ch = (fm.get("channel") or "").strip().lower()
    if ch in known:
        return ch
    reg = (fm.get("register") or "").strip().lower()
    fmt = (fm.get("format") or "").strip().lower()
    if ("x" in known) and (reg in ("tweet", "thread") or fmt in ("tweet", "thread")):
        return "x"
    return ch


def _mkt_phase(stage, status):
    """Where a piece sits in the pipeline.

    Status leads and the folder is the fallback, matching the department's own
    rule that `status` is the gate and the folder is not — except for shipped/,
    which is terminal truth: a published piece whose frontmatter went stale
    must never reappear as work."""
    if stage == "shipped" or status == "shipped":
        return "shipped"
    if status == "approved":
        return "queued"
    if status in ("ready-to-send", "ready_to_send", "final", "reviewed"):
        return "awaiting"
    if stage == "approved":
        return "queued"
    if stage == "ready-to-send":
        return "awaiting"
    return "drafting"


def _mkt_title(slug, fm):
    """A readable title for a piece. The frontmatter's if it has one, else the
    slug with its leading date stripped."""
    if fm.get("title"):
        return fm["title"]
    m = re.match(r"^(\d{4}-\d{2}-\d{2})[-_](.*)$", slug)
    rest = m.group(2) if m else slug
    return rest.replace("-", " ").replace("_", " ").strip().capitalize() or slug


def _mkt_date(slug, fm):
    """The date a piece is planned for. The filename's date is the one every
    ship skill selects on, so it leads; `planned_date` is the fallback."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", slug)
    return (m.group(1) if m else "") or fm.get("planned_date", "")


def _mkt_pieces(inst, known):
    """Every content piece in the instance, tagged with channel and phase."""
    items = []
    content = inst["content"]
    if not content.exists():
        return items
    for stage in MKT_STAGES:
        stage_dir = content / stage
        if not stage_dir.exists():
            continue
        for f in sorted(stage_dir.glob("*.md")):
            try:
                raw = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            m = re.match(r"^---\n(.*?)\n---\n?(.*)", raw, re.DOTALL)
            fm_text, body = (m.group(1), m.group(2).strip()) if m else ("", raw.strip())
            fm = parse_frontmatter_keys(fm_text, MKT_KEYS)
            slug = f.stem
            items.append({
                "path": str(f.relative_to(ROOT)),
                "slug": slug,
                "title": _mkt_title(slug, fm),
                "channel": _mkt_channel_of(fm, known),
                "phase": _mkt_phase(stage, (fm.get("status") or "").strip().lower()),
                "stage": stage,
                "date": _mkt_date(slug, fm),
                "archetype": fm.get("archetype", ""),
                "register": fm.get("register", ""),
                "series": fm.get("series", ""),
                "series_stage": fm.get("stage", ""),
                "format": fm.get("image_format") or fm.get("format", ""),
                "has_carousel": bool(fm.get("carousel_pdf")),
                "body": body,
            })
    return items


def _mkt_channel_cards(blocks):
    """One derived card per configured channel, in config order."""
    cards = []
    for cid, block in blocks.items():
        enabled = _mkt_scalar(block, "enabled").lower() == "true"
        days = _mkt_list(block, "publishing_days")
        time_str = _mkt_scalar(block, "publishing_time", "08:00")
        method = _mkt_scalar(block, "method")
        cred = _mkt_scalar(block, "credential_env")
        declared = _mkt_scalar(block, "autonomy").upper()

        # Autonomy is DECLARED here, unlike in life-os where it had to be
        # inferred: `autonomy: c2` is the recorded output of gate M3, so it is
        # authoritative about what the approver granted. What it is not is
        # authoritative about what the channel can currently do — a config can
        # say C2 while its publishing path is empty. So both are computed and
        # the view shows the grant, flagging it when reality is behind it.
        # A tier that keeps claiming a channel can publish, for exactly as long
        # as it took someone to notice, is the failure this guards against.
        if not enabled:
            capable, why = "C0", "not enabled — nothing drafted, nothing published"
        elif method and method != "manual" and cred:
            capable, why = "C2", "drafts and publishes, one approval per piece"
        elif method == "manual":
            capable, why = "C1", "drafts; publishing is a manual step, not a path"
        else:
            capable, why = "C1", "drafts, but no publishing path is configured"

        if not enabled:
            # Off is off. The grant is what it would resume at, not a gap to
            # close — framing it as one turns every parked channel into a
            # to-do.
            tier = "C0"
            if re.match(r"^C[1-3]$", declared):
                why += f" · config grants {declared} when switched back on"
        else:
            tier = declared if re.match(r"^C[0-3]$", declared) else capable
            if tier != capable:
                why = f"config grants {tier}, but it can only do {capable} today — {why}"
        nxt_iso, nxt_human = _mkt_next_slot(days, time_str) if enabled else ("", "")
        cards.append({
            "id": cid,
            "label": _mkt_scalar(block, "label") or _mkt_label(cid),
            "enabled": enabled,
            "tier": tier,
            "tier_why": why,
            "days": days,
            "time": time_str,
            "next_slot": nxt_human,
            "next_iso": nxt_iso,
            "post_count": _mkt_scalar(block, "post_count", "0"),
            "paused_for": _mkt_scalar(block, "paused_for"),
            # The credential's NAME, never its value — the config stores a
            # variable name on purpose and this view must not be the thing
            # that resolves it.
            "publish_path": ("the approver's logged-in browser session"
                             if method == "browser" else
                             (f"{method} · {cred}" if method and cred else
                              (method or "none configured"))),
            "require_approval": _mkt_scalar(block, "require_approval").lower() != "false",
            "voice_have": _mkt_scalar(block, "current_samples", "0"),
            "voice_need": _mkt_scalar(block, "floor", "0"),
            "playbook": _mkt_scalar(block, "playbook"),
        })
    return cards


MKT_EMPTY_HINT = ("No marketing instance yet — run departments/marketing/install.sh "
                  "to onboard a business.")


def list_marketing(instance_id=None):
    """Channel health, the pipeline per channel, and the pieces actually due
    for the approver's M2.

    `due` is the section that earns this view: without it, approving the next
    piece means finding it among everything staged in a flat library."""
    inst = mkt_instance(instance_id)
    instances = [{"id": i["id"], "label": i["label"]} for i in mkt_instances()]
    if not inst:
        return {"instance": None, "instances": [], "channels": [], "due": [],
                "queued": [], "later_count": 0, "later_first": "",
                "today": datetime.now().strftime("%Y-%m-%d"),
                "window_days": MKT_DUE_WINDOW_DAYS,
                "stats": {"due": 0, "queued": 0, "shipped_30d": 0, "channels_live": 0},
                "empty": MKT_EMPTY_HINT}

    blocks = _mkt_channel_blocks(inst["config"])
    cards = _mkt_channel_cards(blocks)
    items = _mkt_pieces(inst, set(blocks))

    today = datetime.now().strftime("%Y-%m-%d")
    horizon = (datetime.now() + timedelta(days=MKT_DUE_WINDOW_DAYS)).strftime("%Y-%m-%d")

    def of(ch, phase):
        return [i for i in items if i["channel"] == ch and i["phase"] == phase]

    for c in cards:
        awaiting = of(c["id"], "awaiting")
        queued = of(c["id"], "queued")
        # Of the unapproved pieces, how many are actually due. Both numbers are
        # kept because they answer different questions: "how much is written" is
        # planning, "how much needs you this week" is a call on someone's time.
        c["due"] = len([i for i in awaiting if not i["date"] or i["date"] <= horizon])
        c["pipeline"] = {
            "drafting": len(of(c["id"], "drafting")),
            "awaiting": len(awaiting),
            "due": c["due"],
            "queued": len(queued),
            "shipped": len(of(c["id"], "shipped")),
        }

    awaiting_all = sorted([i for i in items if i["phase"] == "awaiting"],
                          key=lambda i: i["date"] or "9999")
    due = [i for i in awaiting_all if not i["date"] or i["date"] <= horizon]
    later = [i for i in awaiting_all if i not in due]
    queued_all = sorted([i for i in items if i["phase"] == "queued"],
                        key=lambda i: i["date"] or "9999")

    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    shipped_recent = [i for i in items if i["phase"] == "shipped" and i["date"] >= cutoff]

    return {
        "instance": inst["id"],
        "instances": instances,
        "today": today,
        "window_days": MKT_DUE_WINDOW_DAYS,
        # Just enough for the channel dropdown. Everything else about a channel
        # — cadence, publishing path, voice corpus — is under Settings, because
        # it is configuration rather than work.
        "channels": [{"id": c["id"], "label": c["label"], "enabled": c["enabled"],
                      "due": c["due"], "next_slot": c["next_slot"]} for c in cards],
        "due": due,
        # A count, not a list. The whole point of the window is that these stay
        # out of the way until they come due; the Content view has them.
        "later_count": len(later),
        "later_first": later[0]["date"] if later else "",
        "queued": queued_all,
        "stats": {
            "due": len(due),
            "queued": len(queued_all),
            "shipped_30d": len(shipped_recent),
            "channels_live": len([c for c in cards if c["enabled"]]),
        },
    }


def list_content(instance_id=None):
    """The whole library, every phase. Looking, not deciding."""
    inst = mkt_instance(instance_id)
    if not inst:
        return {"instance": None, "items": [], "empty": MKT_EMPTY_HINT}
    blocks = _mkt_channel_blocks(inst["config"])
    items = _mkt_pieces(inst, set(blocks))
    items.sort(key=lambda i: i["date"] or "0000", reverse=True)
    return {"instance": inst["id"], "items": items}


# ── Marketing settings — the channel config, editable ────────────────────────
# Everything here was previously a hand edit to a YAML file, which is exactly
# the recurring manual step this system exists to remove. The writes are
# line-targeted rather than a YAML round-trip: that config is mostly comments
# explaining WHY each number is what it is, and a dump-and-reload would delete
# all of them — a far larger loss than this endpoint saves.

def _mkt_channel_line_span(lines, channel):
    """(start, end) line indices of one channel's block in the config.

    Returns the lines UNDER `  {channel}:`, exclusive of the header itself, so
    a write can never touch the key that names the block."""
    in_channels, start = False, None
    for i, line in enumerate(lines):
        if re.match(r"^channels:\s*$", line):
            in_channels = True
            continue
        if not in_channels:
            continue
        if line.strip() and not line.startswith(" "):
            return (start, i) if start is not None else (None, None)
        m = re.match(r"^  ([a-z0-9_-]+):\s*$", line)
        if m:
            if start is not None:
                return start, i          # the next channel begins
            if m.group(1) == channel:
                start = i + 1
    return (start, len(lines)) if start is not None else (None, None)


def _settings_coerce(kind, value):
    """Validate and normalise one incoming value. Returns (yaml_text, error)."""
    if kind == "bool":
        if isinstance(value, str):
            value = value.lower() in ("true", "1", "yes", "on")
        return ("true" if value else "false"), None
    if kind == "int":
        try:
            n = int(value)
        except (TypeError, ValueError):
            return None, "must be a whole number"
        if not 0 <= n <= 50:
            return None, "must be between 0 and 50"
        return str(n), None
    if kind == "days":
        if isinstance(value, str):
            value = [v.strip() for v in value.split(",") if v.strip()]
        if not isinstance(value, list):
            return None, "must be a list of weekday names"
        days = [str(d).strip().lower() for d in value]
        bad = [d for d in days if d not in WEEKDAY_NAMES]
        if bad:
            return None, f"not weekday names: {', '.join(bad)}"
        # Ordered Monday-first and deduplicated. A list reading
        # [thursday, tuesday] is the same schedule and a worse thing to read.
        days = [d for d in WEEKDAY_NAMES if d in days]
        return "[" + ", ".join(days) + "]", None
    if kind == "time":
        s = str(value).strip().strip('"').strip("'")
        if not re.match(r"^([01]?\d|2[0-3]):[0-5]\d$", s):
            return None, "must be HH:MM, 24-hour"
        return f'"{s}"', None
    return None, "unknown field type"


def set_channel_field(channel, field, value, instance_id=None):
    """Write one channel field back to the instance's marketing config.

    The write is atomic and verified: the candidate text has to round-trip to
    the value we intended before it replaces the file. A settings view that can
    corrupt the config governing what gets published is worse than no settings
    view — so on any doubt it refuses and the file is left alone."""
    inst = mkt_instance(instance_id)
    if not inst:
        return None, "no marketing instance"
    kind = SETTINGS_WRITABLE.get(field)
    if not kind:
        return None, f"'{field}' is not editable here"
    cfg = inst["config"]
    if not cfg.exists():
        return None, "marketing config not found"

    text = cfg.read_text(encoding="utf-8")
    lines = text.splitlines()
    start, end = _mkt_channel_line_span(lines, channel)
    if start is None:
        return None, f"no channel '{channel}' in the config"

    new_val, err = _settings_coerce(kind, value)
    if err:
        return None, f"{field}: {err}"

    hit = None
    for i in range(start, end):
        m = re.match(rf"^(\s+){re.escape(field)}:([ \t]*)([^#\n]*)(#.*)?$", lines[i])
        if m:
            hit = i
            indent, comment = m.group(1), (m.group(4) or "")
            # Keep the comment and its spacing. These carry the reasoning for
            # the value; losing them on edit would strip the config of the only
            # record of why it is what it is.
            spacer = "   " if comment else ""
            lines[i] = f"{indent}{field}: {new_val}{spacer}{comment}".rstrip()
            break
    if hit is None:
        return None, f"'{field}' is not set on channel '{channel}' — add it to the file first"

    candidate = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

    try:
        import yaml as _yaml
        parsed = _yaml.safe_load(candidate)
        got = (((parsed or {}).get("channels") or {}).get(channel) or {})

        # Walk to the field wherever it landed — it may be nested under
        # weekly_plan or publishing, and this check must not assume which.
        def _find(d):
            if not isinstance(d, dict):
                return None, False
            if field in d:
                return d[field], True
            for v in d.values():
                got_v, ok = _find(v)
                if ok:
                    return got_v, True
            return None, False

        actual, found = _find(got)
        if not found:
            return None, "write produced a config the value disappeared from — not saved"
        if actual != _yaml.safe_load(new_val):
            return None, f"write did not round-trip ({actual!r}) — not saved"
    except ImportError:
        # No yaml module here. Fall back to the shallow reader this file
        # already uses: weaker, but it still catches a mangled line, and it
        # beats writing blind.
        probe = _mkt_scalar("\n".join(lines[start:end]), field)
        if probe.strip() != new_val.strip():
            return None, "write did not round-trip — not saved"
    except Exception as e:
        return None, f"result would not parse as YAML ({e}) — not saved"

    tmp = cfg.with_suffix(".yaml.tmp")
    tmp.write_text(candidate, encoding="utf-8")
    tmp.replace(cfg)
    return {"channel": channel, "field": field, "value": new_val}, None


def _mkt_ship_schedule(channel):
    """The department schedule that actually publishes a channel — a pointer,
    never a copy, so this view cannot drift from the thing that really fires.

    It has to exist because channels answer "when does this publish?" from two
    different places. A channel with `publishing_days` answers from the config,
    and its ship skill reads that list every run. A channel without one answers
    from its schedule's own cron, and a day list written here would be a
    setting nobody reads."""
    for name in (f"ship_content_{channel}.md", "ship_content.md"):
        p = MKT_DEPT_DIR / "schedules" / name
        if p.exists():
            return str(p.relative_to(ROOT))
    return ""


SCHEDULE_CADENCE_FIELDS = ("Schedule \\(human\\)", "Trigger")


def _schedule_human(rel):
    """The cadence sentence out of a schedules/ file.

    Two field names, because the two departments head it differently:
    engineering writes `**Schedule (human):**`, marketing writes `**Trigger:**`.
    Reading only one would leave this row blank for a whole department, which
    is how a settings view starts quietly lying about when things publish.

    Continuation lines are joined until the blank line — these files hard-wrap
    prose, so reading one line would truncate the sentence mid-clause."""
    if not rel:
        return ""
    p = ROOT / rel
    if not p.exists():
        return ""
    try:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return ""
    pat = re.compile(r"^\*\*(?:" + "|".join(SCHEDULE_CADENCE_FIELDS) + r"):\*\*\s*(.*)$")
    out = []
    for i, line in enumerate(lines):
        m = pat.match(line)
        if not m:
            continue
        out.append(m.group(1).strip())
        for nxt in lines[i + 1:]:
            if not nxt.strip():
                break
            out.append(nxt.strip())
        break
    return re.sub(r"[*`]", "", " ".join(out)).strip()


def list_settings(instance_id=None):
    """Everything editable, grouped into sections."""
    inst = mkt_instance(instance_id)
    if not inst:
        return {"instance": None, "sections": [], "empty": MKT_EMPTY_HINT}
    blocks = _mkt_channel_blocks(inst["config"])
    channels = []
    for c in _mkt_channel_cards(blocks):
        block = blocks.get(c["id"], "")
        # The literal config value, blank when the key is absent — as opposed
        # to the assumption used to compute a next slot. Keeping them apart is
        # what stops a default being rendered as if someone had chosen it.
        time_str = _mkt_scalar(block, "publishing_time") if _mkt_has(block, "publishing_time") else ""
        sched_rel = _mkt_ship_schedule(c["id"])
        channels.append({
            "id": c["id"],
            "label": c["label"],
            "tier": c["tier"],
            "tier_why": c["tier_why"],
            "enabled": c["enabled"],
            # Offer exactly what can be written. set_channel_field() refuses
            # any key not already in the file, so anything outside this list
            # would be a control that fails when clicked.
            "editable": [f for f in SETTINGS_WRITABLE if _mkt_has(block, f)],
            "post_count": c["post_count"],
            "publishing_days": c["days"],
            # Where the cadence really lives. `config` means this list is read
            # every run and editing it changes what publishes. `schedule` means
            # the ship routine's own cron decides and this config has no day
            # list to read.
            "cadence_source": "config" if c["days"] else "schedule",
            "schedule_file": sched_rel,
            "schedule_human": "" if c["days"] else _schedule_human(sched_rel),
            "publishing_time": time_str,
            "next_slot": c["next_slot"],
            "paused_for": c["paused_for"],
            "publish_path": c["publish_path"],
            "require_approval": c["require_approval"],
            "voice_have": c["voice_have"],
            "voice_need": c["voice_need"],
            "playbook": c["playbook"],
        })
    try:
        source = str(inst["config"].relative_to(ROOT))
    except ValueError:
        source = str(inst["config"])
    return {
        "instance": inst["id"],
        "sections": [{
            "id": "channels",
            "label": "Marketing channels",
            "note": "Every editable value here is read on the next run, so a "
                    "change is a change to what actually publishes. Where a row "
                    "is read-only, the reason is on the row — usually that the "
                    "real setting lives somewhere else.",
            "source": source,
            "channels": channels,
            "weekdays": WEEKDAY_NAMES,
            "writable": sorted(SETTINGS_WRITABLE),
        }],
    }


def mkt_topic(topic, note, instance_id=None):
    """Append an idea to the instance's topic bank.

    Not a new mechanism — the CMO already drains this file on every planning
    run. What it removes is the manual step of opening a markdown file to
    record a thought, the same reason the engineering tab has an intake box.

    The archetype is left unset deliberately. Asking someone to classify an
    idea before they can write it down puts a taxonomy between them and the
    thought, and the CMO picks the archetype anyway."""
    inst = mkt_instance(instance_id)
    if not inst:
        return None, "no marketing instance"
    topic = (topic or "").strip()
    if not topic:
        return None, "topic required"
    bank = inst["topic_bank"]
    bank.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d")
    entry = f"- **{topic}** — archetype: unset · added {stamp}"
    if (note or "").strip():
        entry += f"\n  - {note.strip()}"
    if not bank.exists():
        bank.write_text(
            "# Topic bank\n\n"
            "Topics waiting for a planning run. The CMO reads this file on "
            "every run and picks the archetype.\n\n"
            "## Queued topics\n\n" + entry + "\n", encoding="utf-8")
        return {"added": topic}, None
    raw = bank.read_text(encoding="utf-8")
    # `[ \t]*`, never `\s*`: \s matches newlines, so a greedy tail would eat the
    # blank line after the heading and land the insert below the first bullet.
    m = re.search(r"^##+[ \t]*Queued topics[ \t]*$", raw, re.MULTILINE | re.IGNORECASE)
    if m:
        cut = raw.find("\n", m.end())
        cut = len(raw) if cut == -1 else cut + 1
        raw = raw[:cut] + "\n" + entry + "\n" + raw[cut:].lstrip("\n")
    else:
        raw = raw.rstrip("\n") + "\n\n## Queued topics\n\n" + entry + "\n"
    bank.write_text(raw, encoding="utf-8")
    return {"added": topic}, None


def mkt_approve(rel_path, instance_id=None):
    """The approver's M2, executed: `status: approved`, and the file moved into
    content/approved/ so the folder agrees with the field.

    This never publishes. A ship skill picks the piece up on its channel's next
    slot, one per day, oldest first — which is the whole reason approving here
    is safe to do in one click."""
    inst = mkt_instance(instance_id)
    if not inst:
        return None, "no marketing instance"
    if not rel_path:
        return None, "path required"
    src = (ROOT / rel_path).resolve()
    content = inst["content"].resolve()
    # A path arrives from the browser. It must land inside this instance's
    # content tree or it is not a piece, whatever it is named.
    try:
        src.relative_to(content)
    except ValueError:
        return None, "not a piece in this instance's content"
    if not src.exists():
        return None, "piece not found"
    if src.parent.name == "shipped":
        return None, "already shipped — shipped is terminal"

    raw = src.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", raw, re.DOTALL)
    fm = parse_frontmatter_keys(m.group(1) if m else "", ["status"])
    if (fm.get("status") or "").strip().lower() == "approved":
        return {"approved": False, "reason": "already approved"}, None

    dest_dir = inst["content"] / "approved"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    dest.write_text(update_frontmatter_key(raw, "status", "approved"), encoding="utf-8")
    if dest != src:
        src.unlink()
    return {"approved": True, "path": str(dest.relative_to(ROOT))}, None


# ── Reddit view (Twenty CRM) ────────────────────────────────────────────────
# NOT INSTANCE-SCOPED, and the only view here that is not. Twenty's Marketing
# Content records carry a community, not a business — this pipeline predates
# the instance model (see CLAUDE.md) and reads the repo-root knowledge/ files
# rather than any instance's. So role scoping cannot reach it: every signed-in
# user sees every record. That is correct today, with one business whose Reddit
# account is the only one, and it is a cross-tenant leak the day a second
# business gets a pipeline. The fix when that day comes is a business field on
# the Twenty object, filtered here through accounts.visible_instances() the way
# _instance_dirs does everywhere else — not an admin-only gate, which would
# take the view away from the partner whose business it actually is.
#
# The Reddit community pipeline, and a view UNDER Marketing rather than a tab
# of its own. It was the whole Marketing tab until the marketing department
# landed; that made it one channel among several rather than the surface, so
# it folded in where a channel belongs. Nothing about the pipeline changed —
# only what it is called and where it is reached.
#
# System of record is Twenty's "Marketing Content" object (see
# scripts/content_loop.py, which drives the same lifecycle over Telegram).
# This view is a second surface over the SAME lifecycle — it only ever moves
# `status`, never invents a parallel one. No LLM in this path either.
#
# It reads Twenty over the network, which is why it is not folded into
# /api/marketing: the department view has to render with no credentials and no
# reachable CRM, and one endpoint that can fail for two unrelated reasons is
# an endpoint that reports neither honestly.

MC_FIELDS = ("id title key channel status community permalink externalId "
             "rationale postedUrl notes telegramMessageId notifiedAt")
MC_SELECTION = f"{MC_FIELDS} body {{ markdown }}"


def _twenty_gql(query, variables):
    base = os.environ.get("TWENTY_BASE_URL", "").rstrip("/")
    key = os.environ.get("TWENTY_API_KEY", "")
    if not base or not key:
        raise RuntimeError("TWENTY_BASE_URL / TWENTY_API_KEY not set in .env")
    req = urllib.request.Request(
        f"{base}/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise RuntimeError(f"twenty graphql: {payload['errors']}")
    return payload["data"]


def _mc_find(filter_obj, limit=100):
    q = f"""query($f: MarketingContentFilterInput, $l: Int) {{
      marketingContents(filter: $f, first: $l, orderBy: {{createdAt: DescNullsLast}}) {{
        edges {{ node {{ {MC_SELECTION} }} }} }} }}"""
    data = _twenty_gql(q, {"f": filter_obj, "l": limit})
    return [e["node"] for e in data["marketingContents"]["edges"]]


def _mc_update(rid, fields):
    q = f"""mutation($id: UUID!, $d: MarketingContentUpdateInput!) {{
      updateMarketingContent(id: $id, data: $d) {{ {MC_SELECTION} }} }}"""
    return _twenty_gql(q, {"id": rid, "d": fields})["updateMarketingContent"]


def list_reddit(status_filter=None):
    filt = {"status": {"eq": status_filter.upper()}} if status_filter else None
    records = _mc_find(filt)
    items = []
    for r in records:
        items.append({
            "id": r["id"], "key": r.get("key", ""), "title": r.get("title", ""),
            "channel": r.get("channel", ""), "status": r.get("status", ""),
            "community": r.get("community", ""), "permalink": r.get("permalink", ""),
            "body": (r.get("body") or {}).get("markdown") or "",
            "rationale": r.get("rationale", ""), "notes": r.get("notes", ""),
            "posted_url": r.get("postedUrl", ""),
            "notified_at": r.get("notifiedAt", ""),
        })
    return {"items": items}


def reddit_action(rid, action, body=None, reason=None):
    if not rid:
        return None, "id required"
    recs = _mc_find({"id": {"eq": rid}}, limit=1)
    if not recs:
        return None, "record not found"
    rec = recs[0]
    if rec["status"] != "PENDING":
        return None, f"already {rec['status']} — no change"

    if action == "approve":
        _mc_update(rid, {"status": "APPROVED"})
    elif action == "edit_approve":
        if body is None:
            return None, "body required"
        _mc_update(rid, {"body": {"markdown": body}, "status": "APPROVED"})
    elif action == "save":
        if body is None:
            return None, "body required"
        _mc_update(rid, {"body": {"markdown": body}})
    elif action == "skip":
        _mc_update(rid, {"status": "DISCARDED",
                         "notes": f"skip: {(reason or 'no reason').strip()}"})
    else:
        return None, f"unknown action {action}"
    return {"id": rid, "action": action}, None


# ── Cost and usage ───────────────────────────────────────────────────────────
# lib/run-stream.py writes one record per `claude -p` run to
# instances/{business}/engineering/traces/costs-{host}.jsonl — model, tier,
# tokens, dollars, duration. Scanned across every instance so this tab is one
# view of spend across every business, not per-business bookkeeping.

MODEL_TIERS = {"classification": "haiku", "reasoning": "sonnet", "complex": "opus"}


def list_costs(days=30):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    rows = []
    # Through _instance_dirs, not a glob of INSTANCES_DIR — spend is per
    # business, and a partner reading another business's token burn is the
    # same leak as reading its board.
    for inst_dir in _instance_dirs():
        traces_dir = inst_dir / "engineering" / "traces"
        if traces_dir.is_dir():
            business = inst_dir.name
            for f in sorted(traces_dir.glob("costs-*.jsonl")):
                try:
                    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                        except ValueError:
                            continue
                        ts = rec.get("ts")
                        if ts:
                            try:
                                when = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
                                    tzinfo=timezone.utc)
                                if when < cutoff:
                                    continue
                            except ValueError:
                                pass
                        rec["_business"] = business
                        rows.append(rec)
                except OSError:
                    continue

    def bucket(store, key, rec):
        b = store.setdefault(key, {"runs": 0, "cost": 0.0, "errors": 0,
                                   "tokens": 0, "ms": 0, "drift": 0})
        b["runs"] += 1
        b["cost"] += rec.get("cost_usd") or 0.0
        b["errors"] += 1 if rec.get("is_error") else 0
        b["drift"] += 1 if rec.get("model_drift") else 0
        b["tokens"] += ((rec.get("input_tokens") or 0) + (rec.get("output_tokens") or 0)
                        + (rec.get("cache_read_tokens") or 0))
        b["ms"] += rec.get("duration_ms") or 0
        return b

    by_agent, by_model, by_routine, by_version, by_business = {}, {}, {}, {}, {}
    for rec in rows:
        bucket(by_agent, rec.get("agent") or "unmapped", rec)
        bucket(by_model, rec.get("model") or "unknown", rec)
        b = bucket(by_routine, rec.get("routine") or "unknown", rec)
        b["tier"] = rec.get("model_tier") or "unmapped"
        b["model"] = MODEL_TIERS.get(b["tier"], rec.get("model") or "")
        bucket(by_version, "%s %s" % (rec.get("agent") or "unmapped",
                                      rec.get("agent_version") or "?"), rec)
        bucket(by_business, rec.get("_business") or "unknown", rec)

    def listify(store, label):
        out = []
        for k, v in store.items():
            item = {label: k, "runs": v["runs"], "cost": round(v["cost"], 4),
                    "errors": v["errors"], "drift": v["drift"],
                    "tokens": v["tokens"],
                    "avg_s": round((v["ms"] / v["runs"]) / 1000.0, 1) if v["runs"] else 0,
                    "avg_cost": round(v["cost"] / v["runs"], 4) if v["runs"] else 0}
            for extra in ("tier", "model"):
                if extra in v:
                    item[extra] = v[extra]
            out.append(item)
        return sorted(out, key=lambda r: -r["cost"])

    total = round(sum(r.get("cost_usd") or 0.0 for r in rows), 4)
    return {
        "days": days,
        "total_cost": total,
        "runs": len(rows),
        "errors": sum(1 for r in rows if r.get("is_error")),
        "drift": sum(1 for r in rows if r.get("model_drift")),
        "avg_cost": round(total / len(rows), 4) if rows else 0,
        "tiers": MODEL_TIERS,
        "by_agent": listify(by_agent, "agent"),
        "by_model": listify(by_model, "model"),
        "by_routine": listify(by_routine, "routine"),
        "by_version": listify(by_version, "version"),
        "by_business": listify(by_business, "business"),
        "note": "API-equivalent pricing, not subscription billing — right for "
                "comparing agents against each other, wrong as an invoice.",
    }


# ── Logs ─────────────────────────────────────────────────────────────────────
# Cron job stdout/stderr — logs/*.log, written by install_cron.sh's crontab
# entries and departments/engineering/lib/eng-loop-all.sh.

LOGS_DIR = ROOT / "logs"
LOG_TAIL_LINES = 500


def list_logs():
    if not LOGS_DIR.is_dir():
        return {"files": []}
    files = []
    for f in sorted(LOGS_DIR.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True):
        st = f.stat()
        files.append({"name": f.name, "size": st.st_size, "mtime": st.st_mtime})
    return {"files": files}


def read_log(name):
    if not name or not re.match(r"^[\w.-]+\.log$", name):
        return None
    path = LOGS_DIR / name
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    tail = lines[-LOG_TAIL_LINES:]
    return {"name": name, "total_lines": len(lines), "shown": len(tail),
            "text": "\n".join(tail)}


# ── SMS — the fifth marketing channel ────────────────────────────────────────
# A view under Marketing rather than a tab, for the same reason Reddit is one:
# it is one channel, not the department. Two halves under it — CAMPAIGNS (bulk,
# human-gated) and SMART REACTIVATION (autonomous, no copy and no segment to
# choose). Everything that decides what either can do lives in the acting
# user's own config: their SMS gateway, their Claude OAuth token, and which
# customer database their segments read from. See control-center/sms.py.


def list_sms(instance_id=None, email=None):
    """Everything the SMS view renders, in one request.

    Deliberately does NOT go through mkt_instance(): SMS works whether or not
    the marketing department has been installed for this business, the same
    way the Reddit view does. Its instance roster is the plain business list.
    """
    inst_id = _resolve_instance_id(instance_id)
    cfg = accounts.read_config(email)
    missing = accounts.config_missing(email)
    if not inst_id:
        return {"instance": None, "instances": [], "segments": [],
                "campaigns": [], "reactivations": [], "config_missing": missing,
                "empty": "No business instance yet."}
    return {
        "instance": inst_id,
        "instances": business_instances(),
        "customer_source": cfg.get("customer_source") or "",
        "segments": sms.segments_for(cfg),
        "campaigns": sms.list_campaigns(inst_id),
        "reactivations": sms.list_reactivations(inst_id),
        "config_missing": missing,
        "quiet_mode": sms.quiet_mode(),
        "max_chars": sms.MAX_SMS_CHARS,
        "reactivation": {
            "cap": sms.REACTIVATION_MAX_RECIPIENTS,
            "cooldown_days": sms.REACTIVATION_COOLDOWN_DAYS,
            "lapsed_days": sms.REACTIVATION_LAPSED_DAYS,
        },
    }


def sms_action(path, body, email):
    """One dispatcher for every SMS write. The instance was already checked
    against the actor's assignments in do_POST, so these only have to be
    correct about SMS."""
    inst_id = _resolve_instance_id(body.get("instance"))
    if not inst_id:
        return None, "no business instance"
    cfg = accounts.read_config(email)
    campaign_id = body.get("id")

    if path == "/api/sms/campaign":
        return sms.create_campaign(inst_id, cfg, body, email)
    if path == "/api/sms/campaign/update":
        return sms.update_campaign(inst_id, campaign_id, body)
    if path == "/api/sms/campaign/approve":
        return sms.approve_campaign(inst_id, campaign_id, email)
    if path == "/api/sms/campaign/discard":
        return sms.discard_campaign(inst_id, campaign_id)
    if path == "/api/sms/campaign/send":
        # The gateway is the only part of the config a campaign needs. A
        # partner with no Claude token can still run campaigns — refusing
        # them for a credential this path never touches would be theatre.
        if not cfg.get("sms_url"):
            return None, "add your SMS server in Config first"
        return sms.send_campaign(inst_id, campaign_id, cfg)
    if path == "/api/sms/reactivate":
        missing = accounts.config_missing(email)
        if missing:
            return None, "finish your configuration first — missing: " + ", ".join(missing)
        return sms.run_reactivation(inst_id, cfg, email)
    return None, "unknown SMS action"


# ── HTTP handler ─────────────────────────────────────────────────────────────

class ControlCenterHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send_json(self, code, data, extra_headers=None):
        body = json.dumps(data, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, path=HTML_FILE):
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ── Auth ─────────────────────────────────────────────────────────────
    # Everything under /api/auth/ is reachable without a session (login has
    # to be, and logout/me are harmless to ask without one); GET /login is
    # the page that gets you one. Every other route — page or API — is
    # gated below, in do_GET/do_POST.

    def current_email(self):
        return _session_email(_parse_cookies(self).get(SESSION_COOKIE))

    def current_user(self):
        """The full account record behind this request's session, or None.

        Resolved fresh every time rather than cached on the session, so a role
        change or an instance reassignment lands on the next request instead of
        the next login."""
        return accounts.get_user(self.current_email())

    def require_auth(self, is_api):
        """True if the request may proceed. False means a response (redirect
        for a page, 401 for an API call) has already been sent.

        Also publishes the acting user to accounts, which is where every
        instance roster in this file reads its scope from. A deleted account
        with a live session cookie resolves to None here and is treated as
        signed out — deleting a partner takes their access away immediately,
        not whenever their cookie happens to expire."""
        user = self.current_user()
        if user:
            accounts.set_current(user)
            return True
        accounts.set_current(None)
        if is_api:
            self.send_json(401, {"error": "unauthenticated"})
        else:
            self.send_response(302)
            self.send_header("Location", "/login")
            self.end_headers()
        return False

    def require_admin(self):
        """The Partners page and the Logs tab. 403, not 404 — a partner who
        pokes at this URL should learn that it exists and is not theirs,
        rather than that the server is broken."""
        if accounts.is_admin():
            return True
        self.send_json(403, {"error": "admins only"})
        return False

    def require_instance(self, instance_id):
        """Guard for every write that names an instance. The read path is
        already scoped by _instance_dirs, but a POST resolves its instance by
        falling back to the first known one when the id is unknown — which for
        a partner naming someone else's business would silently redirect the
        write into their own. Reject it instead."""
        if instance_id and not accounts.can_see_instance(instance_id):
            self.send_json(403, {"error": "that business is not assigned to you"})
            return False
        return True

    def handle_login(self):
        body = self.read_body()
        ip = _client_ip(self)
        locked, retry_after = _login_locked(ip)
        if locked:
            self.send_json(429, {"error": f"too many attempts — try again in {retry_after}s"})
            return
        email = (body.get("email") or "").strip().lower()
        pin = (body.get("pin") or "").strip()
        user = accounts.get_user(email)
        expected = (user or {}).get("pin")
        # constant-time compare so a valid email can't be timed out of an
        # invalid one — the whole point of a PIN gate is that the PIN, not
        # the email, is the secret.
        if not expected or not hmac.compare_digest(expected, pin):
            _login_fail(ip)
            time.sleep(0.4)  # a small brake on brute-forcing a 4-digit PIN
            self.send_json(401, {"error": "wrong email or PIN"})
            return
        _login_ok(ip)
        accounts.touch_login(email)
        token = _new_session(email)
        self.send_json(200, {"ok": True, "email": email, "role": user["role"]},
                       extra_headers={"Set-Cookie": _cookie_header(token)})

    def handle_logout(self):
        _drop_session(_parse_cookies(self).get(SESSION_COOKIE))
        self.send_json(200, {"ok": True},
                       extra_headers={"Set-Cookie": _cookie_header(None, clear=True)})

    def handle_me(self):
        """What the browser needs to draw the right tabs. Advisory only — the
        server re-checks the role on every request that matters, so hiding the
        Partners tab is a courtesy, not the access control."""
        user = self.current_user()
        if not user:
            self.send_json(200, {"email": None})
            return
        self.send_json(200, {
            "email": user["email"],
            "name": user.get("name", ""),
            "role": user.get("role", "partner"),
            "instances": list(user.get("instances", [])),
            "config_ready": accounts.config_ready(user["email"]),
            "config_missing": accounts.config_missing(user["email"]),
        })

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # ── GET ──────────────────────────────────────────────────────────────

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)

        if parsed.path == "/login":
            self.send_html(LOGIN_HTML_FILE)
            return

        if parsed.path == "/api/auth/me":
            self.handle_me()
            return

        if not self.require_auth(is_api=parsed.path.startswith("/api/")):
            return

        if parsed.path in ("/", "/index.html"):
            self.send_html()
            return

        if parsed.path == "/api/engineering":
            self.send_json(200, list_engineering(qs.get("instance", [None])[0]))
            return

        if parsed.path == "/api/sales":
            self.send_json(200, list_sales(qs.get("instance", [None])[0]))
            return

        if parsed.path == "/api/marketing":
            self.send_json(200, list_marketing(qs.get("instance", [None])[0]))
            return

        if parsed.path == "/api/content":
            self.send_json(200, list_content(qs.get("instance", [None])[0]))
            return

        if parsed.path == "/api/settings":
            self.send_json(200, list_settings(qs.get("instance", [None])[0]))
            return

        if parsed.path == "/api/reddit":
            try:
                self.send_json(200, list_reddit(qs.get("status", [None])[0]))
            except Exception as e:
                self.send_json(502, {"error": str(e)})
            return

        if parsed.path == "/api/costs":
            try:
                days = int(qs.get("days", ["30"])[0])
            except (TypeError, ValueError):
                days = 30
            self.send_json(200, list_costs(max(1, min(days, 365))))
            return

        if parsed.path == "/api/partners":
            if not self.require_admin():
                return
            self.send_json(200, {
                "users": [accounts.public_user(u) for u in accounts.all_users()],
                "instances": business_instances(),
                "roles": list(accounts.ROLES),
            })
            return

        if parsed.path == "/api/config":
            # An admin may read anyone's config (redacted, like everyone
            # else's); a partner may read only their own.
            who = (qs.get("email", [None])[0] or "").strip().lower()
            if who and who != self.current_email():
                if not self.require_admin():
                    return
                if not accounts.get_user(who):
                    self.send_json(404, {"error": "no such user"})
                    return
            else:
                who = self.current_email()
            self.send_json(200, accounts.read_config_public(who))
            return

        if parsed.path == "/api/sms":
            inst_id = qs.get("instance", [None])[0]
            if not self.require_instance(inst_id):
                return
            self.send_json(200, list_sms(inst_id, self.current_email()))
            return

        if parsed.path == "/api/logs":
            # Repo-wide cron logs. Nothing in logs/*.log is scoped by
            # business, so there is no partner-safe subset to show.
            if not self.require_admin():
                return
            self.send_json(200, list_logs())
            return

        if parsed.path == "/api/logs/view":
            if not self.require_admin():
                return
            name = qs.get("name", [None])[0]
            result = read_log(name)
            if result is None:
                self.send_json(404, {"error": "log not found"})
                return
            self.send_json(200, result)
            return

        self.send_json(404, {"error": "not found"})

    # ── POST ─────────────────────────────────────────────────────────────

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/auth/login":
            self.handle_login()
            return

        if parsed.path == "/api/auth/logout":
            self.handle_logout()
            return

        if not self.require_auth(is_api=True):
            return

        # Every write that names a business is checked against the actor's
        # assignments before it reaches a handler, once, here — rather than
        # trusting a dozen handlers to each remember.
        if parsed.path.startswith("/api/") and self.headers.get("Content-Length"):
            self._body = self.read_body()
            if not self.require_instance(self._body.get("instance")):
                return
        else:
            self._body = {}

        if parsed.path == "/api/partners/create":
            if not self.require_admin():
                return
            result, err = accounts.create_user(self._body)
            self.send_json(400 if err else 201, {"error": err} if err else result)
            return

        if parsed.path == "/api/partners/update":
            if not self.require_admin():
                return
            result, err = accounts.update_user(self._body.get("email"), self._body)
            self.send_json(400 if err else 200, {"error": err} if err else result)
            return

        if parsed.path == "/api/partners/delete":
            if not self.require_admin():
                return
            result, err = accounts.delete_user(self._body.get("email"),
                                               acting_email=self.current_email())
            self.send_json(400 if err else 200, {"error": err} if err else result)
            return

        if parsed.path == "/api/config":
            # Same rule as the GET: your own, or anyone's if you are an admin.
            who = (self._body.get("email") or "").strip().lower()
            if who and who != self.current_email():
                if not self.require_admin():
                    return
                if not accounts.get_user(who):
                    self.send_json(404, {"error": "no such user"})
                    return
            else:
                who = self.current_email()
            result, err = accounts.write_config(who, self._body)
            self.send_json(400 if err else 200, {"error": err} if err else result)
            return

        if parsed.path.startswith("/api/sms/"):
            result, err = sms_action(parsed.path, self._body, self.current_email())
            self.send_json(400 if err else 200, {"error": err} if err else result)
            return

        if parsed.path == "/api/eng/intake":
            body = self._body
            inst_id = body.get("instance")
            path, err = eng_intake(body.get("title"), body.get("description"), inst_id)
            if err:
                self.send_json(400, {"error": err})
                return
            fire_eng_trigger("intake", path, inst_id)
            self.send_json(201, {"path": path})
            return

        if parsed.path == "/api/eng/priority":
            body = self._body
            inst_id = body.get("instance")
            result, err = eng_priority(body.get("ticket"), body.get("priority"), inst_id)
            if err:
                self.send_json(400, {"error": err})
                return
            if result["priority"] == "now":
                fire_eng_trigger("scheduled", result["path"], inst_id)
            self.send_json(200, result)
            return

        if parsed.path == "/api/eng/merge-check":
            body = self._body
            result, err = eng_merge_check(body.get("ticket"), force=bool(body.get("force")),
                                          instance_id=body.get("instance"))
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(200, result)
            return

        if parsed.path == "/api/eng/decide":
            body = self._body
            inst_id = body.get("instance")
            result, err = eng_decide(body.get("file"), body.get("decision"),
                                     body.get("note"), inst_id)
            if err:
                self.send_json(400, {"error": err})
                return
            fire_eng_trigger("decision", result["file"], inst_id)
            self.send_json(200, result)
            return

        if parsed.path == "/api/sales/lead":
            body = self._body
            result, err = sales_create_lead(body.get("instance"), body)
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(201, result)
            return

        if parsed.path == "/api/sales/lead/update":
            body = self._body
            result, err = sales_update_lead(body.get("instance"), body.get("slug"),
                                            body.get("fields") or {}, body.get("note"))
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(200, result)
            return

        if parsed.path == "/api/sales/move-lead":
            body = self._body
            result, err = sales_move_lead(body.get("instance"), body.get("slug"),
                                          body.get("to_stage"))
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(200, result)
            return

        if parsed.path == "/api/mkt/approve":
            body = self._body
            result, err = mkt_approve(body.get("path"), body.get("instance"))
            self.send_json(400 if err else 200, {"error": err} if err else result)
            return

        if parsed.path == "/api/mkt/topic":
            body = self._body
            result, err = mkt_topic(body.get("topic"), body.get("note"),
                                    body.get("instance"))
            self.send_json(400 if err else 200, {"error": err} if err else result)
            return

        if parsed.path == "/api/settings/channel":
            body = self._body
            result, err = set_channel_field(body.get("channel"), body.get("field"),
                                            body.get("value"), body.get("instance"))
            self.send_json(400 if err else 200, {"error": err} if err else result)
            return

        if parsed.path == "/api/reddit/action":
            body = self._body
            try:
                result, err = reddit_action(body.get("id"), body.get("action"),
                                            body.get("body"), body.get("reason"))
            except Exception as e:
                self.send_json(502, {"error": str(e)})
                return
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(200, result)
            return

        self.send_json(404, {"error": "not found"})


if __name__ == "__main__":
    HOST = os.environ.get("BUSINESS_OS_HOST", "127.0.0.1")
    PORT = int(os.environ.get("BUSINESS_OS_PORT", PORT))
    # Threading, not the plain HTTPServer this was before the auth gate: the
    # 0.4s brake on a failed login (see handle_login) would otherwise stall
    # every other tab on the dashboard for whoever is mistyping their PIN,
    # and once this is reachable over the internet concurrent requests are
    # the normal case, not the exception.
    server = ThreadingHTTPServer((HOST, PORT), ControlCenterHandler)
    if not accounts.any_users():
        print("WARNING: no users — nobody can log in.")
        print("  Set CONTROL_CENTER_USERS=you@example.com:1234 in .env and restart;")
        print(f"  it seeds {accounts.USERS_FILE.name} once, and the Partners tab owns it after that.\n")
    else:
        admins = [u["email"] for u in accounts.all_users() if u["role"] == "admin"]
        print(f"Users             → {len(accounts.all_users())} ({len(admins)} admin: {', '.join(admins)})")
    print(f"Business OS Control Center → http://localhost:{PORT}")
    print(f"Root              → {ROOT}")
    print(f"Instances found   → {[i['id'] for i in business_instances()] or '(none yet)'}")
    print("Ctrl-C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
