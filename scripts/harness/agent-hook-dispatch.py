#!/usr/bin/env python3
"""Dispatch canonical workspace hooks by event for local agent runtimes.

The canonical hook configuration lives in `.claude/settings.json`. Claude Code
uses it directly; other agents can call this script through `ws hook` to execute
the same command hooks, including document-readiness gates, without introducing
a second policy surface.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SETTINGS = ROOT / ".claude/settings.json"


def load_hooks() -> dict:
    try:
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(
            f"ERROR: hook settings missing: {SETTINGS.relative_to(ROOT)}",
            file=sys.stderr,
        )
        return {}
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid hook settings JSON: {exc}", file=sys.stderr)
        return {}
    return settings.get("hooks", {})


def matcher_applies(pattern: str | None, requested: str) -> bool:
    if not pattern or pattern == "*":
        return True
    allowed = {part.strip() for part in pattern.split("|") if part.strip()}
    return requested in allowed


def read_hook_input() -> str:
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read()


def parse_hook_input(raw_input: str) -> dict[str, Any]:
    if not raw_input.strip():
        return {}
    try:
        data = json.loads(raw_input)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def first_text(*values: object) -> str:
    for value in values:
        if isinstance(value, str) and value:
            return value
    return ""


def set_default_env(env: dict[str, str], key: str, value: str) -> None:
    if value and not env.get(key):
        env[key] = value


def hydrate_portable_tool_env(env: dict[str, str], hook_input: dict[str, Any]) -> None:
    """Translate provider-neutral or Codex hook inputs into Claude hook env names."""
    # Codex/local runtimes may provide CODEX_TOOL_INPUT_* and CODEX_TOOL_RESULT_* env vars.
    for suffix in (
        "TOOL_INPUT_FILE_PATH",
        "TOOL_INPUT_PATH",
        "TOOL_INPUT_CONTENT",
        "TOOL_INPUT_NEW_TEXT",
        "TOOL_INPUT_NEW_STRING",
        "TOOL_INPUT_COMMAND",
        "TOOL_RESULT_FILE_PATH",
    ):
        set_default_env(
            env,
            f"CLAUDE_{suffix}",
            first_text(env.get(f"CODEX_{suffix}"), env.get(f"AGENT_{suffix}")),
        )

    tool_input = hook_input.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
    tool_result = hook_input.get("tool_result")
    if not isinstance(tool_result, dict):
        tool_result = {}

    set_default_env(
        env,
        "CLAUDE_TOOL_INPUT_FILE_PATH",
        first_text(tool_input.get("file_path"), tool_input.get("path")),
    )
    set_default_env(env, "CLAUDE_TOOL_INPUT_PATH", first_text(tool_input.get("path")))
    set_default_env(
        env,
        "CLAUDE_TOOL_INPUT_CONTENT",
        first_text(
            tool_input.get("content"),
            tool_input.get("new_text"),
            tool_input.get("new_string"),
        ),
    )
    set_default_env(env, "CLAUDE_TOOL_INPUT_NEW_TEXT", first_text(tool_input.get("new_text")))
    set_default_env(
        env,
        "CLAUDE_TOOL_INPUT_NEW_STRING",
        first_text(tool_input.get("new_string")),
    )
    set_default_env(env, "CLAUDE_TOOL_INPUT_COMMAND", first_text(tool_input.get("command")))
    set_default_env(
        env,
        "CLAUDE_TOOL_RESULT_FILE_PATH",
        first_text(tool_result.get("file_path"), tool_result.get("path")),
    )


def dispatch(event: str, matcher: str, raw_input: str = "") -> int:
    event_entries = load_hooks().get(event)
    if not event_entries:
        print(f"No hooks configured for event {event}.")
        return 0

    hook_input = parse_hook_input(raw_input)
    matched = 0
    env = os.environ.copy()
    env.setdefault("CLAUDE_PROJECT_DIR", str(ROOT))
    env["AGENT_HOOK_EVENT"] = event
    env["AGENT_HOOK_MATCHER"] = matcher
    hydrate_portable_tool_env(env, hook_input)

    for entry in event_entries:
        if not matcher_applies(entry.get("matcher"), matcher):
            continue
        matched += 1
        for hook in entry.get("hooks", []):
            hook_type = hook.get("type")
            if hook_type != "command":
                print(
                    f"WARNING: skipping unsupported {hook_type!r} hook for {event}/{matcher}; "
                    "only command hooks are portable through ws hook.",
                    file=sys.stderr,
                )
                continue

            command = hook.get("command")
            if not command:
                print(
                    f"WARNING: skipping empty command hook for {event}/{matcher}.",
                    file=sys.stderr,
                )
                continue

            timeout = int(hook.get("timeout", 60))
            try:
                result = subprocess.run(
                    command,
                    cwd=ROOT,
                    env=env,
                    shell=True,
                    input=raw_input if raw_input else None,
                    timeout=timeout,
                    text=True,
                )
            except subprocess.TimeoutExpired:
                print(
                    f"ERROR: hook timed out after {timeout}s: {command}",
                    file=sys.stderr,
                )
                return 124

            if result.returncode != 0:
                return result.returncode

    if matched == 0:
        print(f"No hooks matched event {event} with matcher {matcher}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run canonical `.claude/settings.json` hooks by event and matcher."
    )
    parser.add_argument(
        "event",
        help=(
            "Hook event name. Active wired events: "
            "SessionStart, PreToolUse, PostToolUse, PostToolUseFailure, PreCompact, Stop"
        ),
    )
    parser.add_argument(
        "matcher",
        nargs="?",
        default="*",
        help="Hook matcher, for example Bash, Read, Write",
    )
    args = parser.parse_args()
    return dispatch(args.event, args.matcher, read_hook_input())


if __name__ == "__main__":
    raise SystemExit(main())
