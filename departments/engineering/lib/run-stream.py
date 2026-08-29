#!/usr/bin/env python3
"""
lib/run-stream.py — stdout filter for `claude -p --output-format stream-json --verbose`.

Sits in the pipe between the `claude` process and the routine's log. Two jobs:

  1. Emit human-readable text to stdout, so traces/cron-{name}.log and
     Coolify's execution log stay readable AND stay live. This is the entire
     reason vps-cron.sh does not use `--output-format json`: that form buffers
     everything to the end of the run, so a routine that hangs shows nothing at
     all. Given this host's history of failures that were invisible for days
     (the root guard, the missing Composio CLI), losing live output to gain
     cost data would have been a bad trade. stream-json gives both.

  2. Capture the final `result` event and append ONE cost record per run to
     traces/costs-{host}.jsonl — model, tokens, dollars, duration, plus the
     agent version that produced it.

This filter must never fail the run it is watching:
  - any line that will not parse is passed through raw,
  - a missing or malformed result event writes no record rather than a wrong one,
  - it always exits 0. The routine's real exit code comes from PIPESTATUS[0]
    in vps-cron.sh, and nothing here may shadow it.

`python3` and not `jq` on purpose: the VPS image (node:22-slim + python3, git,
bash, curl, unzip) has no jq, and adding a package to the image to parse JSON
that python3 already parses is not worth the layer.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


def emit(text):
    """Write to stdout unbuffered-ish. Broken pipe is not our problem to report."""
    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except BrokenPipeError:
        pass


def human_line(obj):
    """Render one stream event as the prose a person reads in the log."""
    etype = obj.get("type")

    if etype == "assistant":
        content = (obj.get("message") or {}).get("content") or []
        out = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                out.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                out.append("\n· %s\n" % block.get("name", "tool"))
        return "".join(out)

    if etype == "result" and obj.get("is_error"):
        # Surface the failure in the log even when no assistant text was produced.
        return "\n!! %s: %s\n" % (
            obj.get("subtype", "error"),
            obj.get("result") or obj.get("api_error_status") or "no detail",
        )

    if etype == "rate_limit_event":
        info = obj.get("rate_limit_info") or {}
        status = info.get("status")
        # Only worth a log line when it is actually constraining the run.
        if status and status != "allowed":
            return "\n·· rate limit: %s\n" % status

    return ""


def cost_record(result, args, printed_any):
    """Flatten a result event into the one-line record written to costs jsonl."""
    usage = result.get("usage") or {}
    model_usage = result.get("modelUsage") or {}

    # modelUsage is keyed by concrete model id and is the only place the actual
    # model that ran is reported. A run can legitimately touch more than one
    # (a subagent on a different tier), so keep the breakdown and derive the
    # headline model as the one that cost the most.
    primary = ""
    if model_usage:
        primary = max(model_usage, key=lambda m: (model_usage[m] or {}).get("costUSD", 0))

    return {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "routine": args.routine,
        "agent": args.agent,
        "agent_version": args.agent_version,
        "repo_sha": args.repo_sha,
        "host": args.host,
        "model_tier": args.model_tier,
        "model_requested": args.model_requested,
        "model": primary,
        # Requested vs actual. A run asked for sonnet and billed opus is a
        # routing failure that otherwise looks exactly like a normal run — the
        # shape of silent failure this host keeps producing. Recorded rather
        # than alerted: one row proves nothing, a column in the report does.
        "model_drift": bool(
            primary
            and args.model_requested not in ("default", "")
            and args.model_requested.split("-")[0] not in primary
        ),
        "cost_usd": result.get("total_cost_usd"),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cache_read_tokens": usage.get("cache_read_input_tokens"),
        "cache_creation_tokens": usage.get("cache_creation_input_tokens"),
        "duration_ms": result.get("duration_ms"),
        "num_turns": result.get("num_turns"),
        "session_id": result.get("session_id"),
        "is_error": bool(result.get("is_error")),
        "subtype": result.get("subtype"),
        "printed_output": printed_any,
        "models": {
            m: {
                "cost_usd": (v or {}).get("costUSD"),
                "input_tokens": (v or {}).get("inputTokens"),
                "output_tokens": (v or {}).get("outputTokens"),
                "cache_read_tokens": (v or {}).get("cacheReadInputTokens"),
                "cache_creation_tokens": (v or {}).get("cacheCreationInputTokens"),
            }
            for m, v in model_usage.items()
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--routine", default="unknown")
    p.add_argument("--agent", default="unmapped")
    p.add_argument("--agent-version", default="unknown")
    p.add_argument("--repo-sha", default="unknown")
    p.add_argument("--host", default="unknown")
    p.add_argument("--model-tier", default="unmapped")
    p.add_argument("--model-requested", default="default")
    p.add_argument("--out", required=True, help="path to costs jsonl")
    args = p.parse_args()

    # Undecodable bytes must not kill the filter. Default stdin raises
    # UnicodeDecodeError on invalid UTF-8, which would end the process
    # mid-stream and silently truncate the routine's log. Caught by
    # lib/tests/run-cost-accounting.test.sh ("binary garbage: exits 0").
    try:
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    # Same problem, the write side. Default stdout on Windows is the console's
    # ANSI codepage (cp1252 here), not UTF-8, unless the interpreter is launched
    # with -X utf8/PYTHONUTF8=1 — which `python3 lib/run-stream.py` in
    # lib/eng-trigger.sh's pipeline is not. Claude's own assistant text is full
    # of exactly the characters that break this (arrows, em-dashes, checkmarks):
    # 2026-08-29 hit `UnicodeEncodeError: 'charmap' codec can't encode
    # character '→'` mid-stream, which killed this filter's stdin loop
    # early. The filter itself degrades safely (the outer try/except in
    # __main__ catches it and exits 0, per this file's own contract) — but the
    # `claude` process upstream in the pipe does not: it kept writing into a
    # pipe nothing was reading any more, and the pass sat orphaned for ~89
    # minutes until a stale-lock check eventually noticed and recovered it.
    # Reconfiguring here, the same way stdin already is, closes the actual hole
    # rather than only containing its symptom.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    result = None
    printed_any = False

    for raw in sys.stdin:
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except (ValueError, TypeError):
            # Not an event. Could be a pre-flight error from the CLI itself
            # (the root-guard message, an auth failure) — exactly the output
            # that must not be swallowed.
            emit(raw)
            printed_any = True
            continue

        if obj.get("type") == "result":
            result = obj

        text = human_line(obj)
        if text:
            emit(text)
            printed_any = True

    # Guarantee the log carries the outcome even if nothing streamed as text.
    if result is not None and not printed_any:
        final = result.get("result")
        if final:
            emit(str(final) + "\n")
            printed_any = True

    emit("\n")

    if result is None:
        # No result event: the process died before finishing. Write nothing —
        # a cost row invented from a partial run is worse than a missing one,
        # and vps-cron.sh's exit-code trailer already records that it failed.
        return 0

    try:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(cost_record(result, args, printed_any)) + "\n")
    except OSError as exc:
        # Losing a cost row must never cost us the run.
        sys.stderr.write("run-stream: could not write cost record: %s\n" % exc)

    return 0


if __name__ == "__main__":
    # Belt and braces. This filter sits in the pipe of eighteen production
    # routines; there is no failure of ITS OWN worth failing a routine over.
    # vps-cron.sh reads PIPESTATUS[0] (the claude process) for the real status,
    # so exiting non-zero here would only ever corrupt an unrelated signal.
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:  # noqa: BLE001 - deliberate catch-all, see above
        sys.stderr.write("run-stream: %s: %s\n" % (type(exc).__name__, exc))
        sys.exit(0)
