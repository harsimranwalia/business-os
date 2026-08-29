#!/usr/bin/env python3
"""Business OS Control Center — http://localhost:7777

A standalone command center for business-os, with zero dependency on
life-os. Runs entirely off this repo: departments/, instances/, and this
repo's own .env (TWENTY_API_KEY etc). Local-only by default — no passcode
gate, no tunnel — because it is meant to run on Harry's business desktop,
not be reachable from the open internet. If that changes, add the gate
life-os's control-center already has rather than inventing a new one.

Tabs:
  Marketing    Twenty CRM "Marketing Content" lifecycle — approve/edit/skip
               drafts right here, the same lifecycle Telegram already drives
               (scripts/content_loop.py). Two approval surfaces, one system
               of record — Twenty's `status` field is the only truth either
               of them writes.
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
               content_loop, reddit_post, eng-loop-all runs).
"""

import json
import os
import re
import subprocess
import threading
import time
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent  # business-os root
HTML_FILE = Path(__file__).parent / "index.html"
PORT = 7777


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


def business_instances():
    """Every business this control center knows about, rebuilt per request —
    onboarding one shouldn't need a server restart to show up."""
    out = []
    if INSTANCES_DIR.is_dir():
        for d in sorted(p for p in INSTANCES_DIR.iterdir() if p.is_dir()):
            out.append({"id": d.name, "label": _business_label(d)})
    return out


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
               "branch", "priority"]

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
    if INSTANCES_DIR.is_dir():
        for d in sorted(p for p in INSTANCES_DIR.iterdir() if p.is_dir()):
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
                "stats": {"waiting_on_harry": 0, "approval_cap": 0, "in_flight": 0,
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
                    "raised", "pr_url", "decision", "decided"])
            if fm.get("type") != "eng-decision":
                continue
            if fm.get("decision"):
                deciding.append({
                    "file": f.name,
                    "gate": fm.get("gate", ""),
                    "ticket": fm.get("ticket", ""),
                    "project": fm.get("project", ""),
                    "decision": fm.get("decision", ""),
                    "decided": fm.get("decided", ""),
                })
                continue
            waiting.append({
                "file": f.name,
                "gate": fm.get("gate", ""),
                "ticket": fm.get("ticket", ""),
                "project": fm.get("project", ""),
                "recommendation": fm.get("recommendation", ""),
                "raised": fm.get("raised", ""),
                "pr_url": fm.get("pr_url", ""),
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
    blocked_on_harry = [t for t in tickets
                        if t["state"] == "blocked" and t["blocked_on"] == "approver"]

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
        "stats": {
            "waiting_on_harry": len(waiting) + len(blocked_on_harry),
            "approval_cap": limits["approval_cap"],
            "in_flight": len(in_flight),
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
           re.search(r"^gate:[ \t]*merge-request", t, re.MULTILINE):
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
    """Read the WIP and approval caps from this instance's config rather
    than hardcoding. business-os's own vocabulary (`approver_limit`,
    `approval_cap`) — "harry" isn't a word a shared template can use."""
    defaults = {"approver_limit": 2, "machine_limit": 6, "approval_cap": 3}
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


TRIGGER_SHELL = "bash" if os.name == "nt" else ("/bin/zsh" if os.uname().sysname == "Darwin" else "/bin/bash")


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


# ── Marketing view (Twenty CRM) ─────────────────────────────────────────────
# System of record is Twenty's "Marketing Content" object (see
# scripts/content_loop.py, which drives the same lifecycle over Telegram).
# This tab is a second surface over the SAME lifecycle — it only ever moves
# `status`, never invents a parallel one. No LLM in this path either.

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


def list_marketing(status_filter=None):
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


def marketing_action(rid, action, body=None, reason=None):
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
    from datetime import timedelta
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    rows = []
    if INSTANCES_DIR.is_dir():
        for traces_dir in INSTANCES_DIR.glob("*/engineering/traces"):
            business = traces_dir.parent.parent.name
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


# ── HTTP handler ─────────────────────────────────────────────────────────────

class ControlCenterHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send_json(self, code, data):
        body = json.dumps(data, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self):
        body = HTML_FILE.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

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
            try:
                self.send_json(200, list_marketing(qs.get("status", [None])[0]))
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

        if parsed.path == "/api/logs":
            self.send_json(200, list_logs())
            return

        if parsed.path == "/api/logs/view":
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

        if parsed.path == "/api/eng/intake":
            body = self.read_body()
            inst_id = body.get("instance")
            path, err = eng_intake(body.get("title"), body.get("description"), inst_id)
            if err:
                self.send_json(400, {"error": err})
                return
            fire_eng_trigger("intake", path, inst_id)
            self.send_json(201, {"path": path})
            return

        if parsed.path == "/api/eng/priority":
            body = self.read_body()
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
            body = self.read_body()
            result, err = eng_merge_check(body.get("ticket"), force=bool(body.get("force")),
                                          instance_id=body.get("instance"))
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(200, result)
            return

        if parsed.path == "/api/eng/decide":
            body = self.read_body()
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
            body = self.read_body()
            result, err = sales_create_lead(body.get("instance"), body)
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(201, result)
            return

        if parsed.path == "/api/sales/lead/update":
            body = self.read_body()
            result, err = sales_update_lead(body.get("instance"), body.get("slug"),
                                            body.get("fields") or {}, body.get("note"))
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(200, result)
            return

        if parsed.path == "/api/sales/move-lead":
            body = self.read_body()
            result, err = sales_move_lead(body.get("instance"), body.get("slug"),
                                          body.get("to_stage"))
            if err:
                self.send_json(400, {"error": err})
                return
            self.send_json(200, result)
            return

        if parsed.path == "/api/marketing/action":
            body = self.read_body()
            try:
                result, err = marketing_action(body.get("id"), body.get("action"),
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
    server = HTTPServer((HOST, PORT), ControlCenterHandler)
    print(f"Business OS Control Center → http://localhost:{PORT}")
    print(f"Root              → {ROOT}")
    print(f"Instances found   → {[i['id'] for i in business_instances()] or '(none yet)'}")
    print("Ctrl-C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
