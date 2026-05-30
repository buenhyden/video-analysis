#!/usr/bin/env python3
"""Validate shared agent runtime settings and hook contract boundaries."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETTINGS = ROOT / ".claude/settings.json"
HOOK_DISPATCHER = ROOT / "scripts/harness/agent-hook-dispatch.py"

EXPECTED_HOOK_EVENTS = {
    "SessionStart",
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "PreCompact",
    "Stop",
}

REQUIRED_HOOK_COMMAND_MARKERS = {
    "PreToolUse": (
        "pre-tool-validate.sh",
    ),
    "PostToolUse": (
        "docs-readme-sync.sh",
        "post-tool-format.sh",
        "post-tool-validate.sh",
    ),
    "Stop": (
        "validate-doc-governance.sh",
        "validate-doc-readiness.py",
        "stop-completion-governance.sh",
    ),
}

FORBIDDEN_SURFACES = [
    ".codex/hooks.json",
    ".codex/hooks",
    ".agents/skills",
    ".gemini",
    ".github/copilot-instructions.md",
    ".github/instructions",
]

ALLOWED_LEGACY_AGENTS_FILES = {
    ".agents/README.md",
    ".agents/rules/graphify.md",
    ".agents/workflows/graphify.md",
}

REQUIRED_SCRIPT_CONTENT_MARKERS = {
    ".claude/hooks/pre-tool-validate.sh": (
        "validate-stage-template-write.py",
        ".codex/hooks.json",
        ".codex/agents/*.toml",
        ".agents/skills",
        "pull_request_target",
        "permissions: write-all",
    ),
    ".claude/hooks/post-tool-validate.sh": (
        "validate-doc-readiness.py",
    ),
    ".claude/hooks/post-tool-format.sh": (
        "prettier",
        "ruff format",
        "shfmt",
    ),
    ".claude/hooks/stop-completion-governance.sh": (
        "git status --porcelain",
        "AGENT_ALLOW_DIRTY_STOP",
        "Conventional Commit",
    ),
}

REQUIRED_DISPATCHER_MARKERS = (
    ".claude/settings.json",
    "CODEX_TOOL_INPUT_",
    "CLAUDE_TOOL_INPUT_FILE_PATH",
    "CLAUDE_TOOL_INPUT_CONTENT",
    "CLAUDE_TOOL_RESULT_FILE_PATH",
    "input=raw_input",
    "hydrate_portable_tool_env",
)

LOCAL_PATH_PATTERNS = [
    re.compile(r"\$CLAUDE_PROJECT_DIR/([A-Za-z0-9_./-]+)"),
    re.compile(r"\bbash\s+(scripts/[A-Za-z0-9_./-]+)"),
    re.compile(r"\bpython3\s+(scripts/[A-Za-z0-9_./-]+)"),
]


def load_settings(errors: list[str]) -> dict:
    try:
        data = json.loads(SETTINGS.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(".claude/settings.json is missing")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f".claude/settings.json is invalid JSON: {exc}")
        return {}

    if not isinstance(data, dict):
        errors.append(".claude/settings.json must contain a JSON object")
        return {}
    return data


def validate_permissions(settings: dict, errors: list[str]) -> None:
    permissions = settings.get("permissions")
    if not isinstance(permissions, dict):
        errors.append("permissions must be an object")
        return

    for key in ("allow", "deny"):
        values = permissions.get(key)
        if not isinstance(values, list) or not all(
            isinstance(value, str) and value for value in values
        ):
            errors.append(f"permissions.{key} must be a list of non-empty strings")


def referenced_local_paths(command: str) -> set[Path]:
    paths: set[Path] = set()
    for pattern in LOCAL_PATH_PATTERNS:
        for match in pattern.findall(command):
            paths.add(ROOT / match)
    return paths


def event_commands(hooks: dict, event: str) -> list[str]:
    commands: list[str] = []
    entries = hooks.get(event)
    if not isinstance(entries, list):
        return commands

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        entry_hooks = entry.get("hooks")
        if not isinstance(entry_hooks, list):
            continue
        for hook in entry_hooks:
            if not isinstance(hook, dict):
                continue
            command = hook.get("command")
            if isinstance(command, str) and command:
                commands.append(command)
    return commands


def validate_required_hook_commands(hooks: dict, errors: list[str]) -> None:
    for event, markers in REQUIRED_HOOK_COMMAND_MARKERS.items():
        commands = event_commands(hooks, event)
        for marker in markers:
            if not any(marker in command for command in commands):
                errors.append(f"hooks.{event} must invoke {marker}")


def validate_required_script_markers(errors: list[str]) -> None:
    for rel_path, markers in REQUIRED_SCRIPT_CONTENT_MARKERS.items():
        path = ROOT / rel_path
        if not path.exists():
            errors.append(f"required hook helper is missing: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel_path} must reference {marker}")


def validate_provider_neutral_dispatcher(errors: list[str]) -> None:
    if not HOOK_DISPATCHER.exists():
        errors.append(
            "provider-neutral hook dispatcher is missing: scripts/harness/agent-hook-dispatch.py"
        )
        return
    text = HOOK_DISPATCHER.read_text(encoding="utf-8", errors="ignore")
    for marker in REQUIRED_DISPATCHER_MARKERS:
        if marker not in text:
            errors.append(
                f"scripts/harness/agent-hook-dispatch.py must contain `{marker}`"
            )


def validate_hooks(settings: dict, errors: list[str]) -> None:
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        errors.append("hooks must be an object")
        return

    configured_events = set(hooks)
    unexpected = sorted(configured_events - EXPECTED_HOOK_EVENTS)
    missing = sorted(EXPECTED_HOOK_EVENTS - configured_events)
    if unexpected:
        errors.append(f"unexpected hook events configured: {unexpected}")
    if missing:
        errors.append(f"expected hook events missing: {missing}")

    for event, entries in hooks.items():
        if not isinstance(entries, list) or not entries:
            errors.append(f"hooks.{event} must be a non-empty list")
            continue

        for entry_index, entry in enumerate(entries):
            location = f"hooks.{event}[{entry_index}]"
            if not isinstance(entry, dict):
                errors.append(f"{location} must be an object")
                continue

            matcher = entry.get("matcher")
            if not isinstance(matcher, str) or not matcher:
                errors.append(f"{location}.matcher must be a non-empty string")

            entry_hooks = entry.get("hooks")
            if not isinstance(entry_hooks, list) or not entry_hooks:
                errors.append(f"{location}.hooks must be a non-empty list")
                continue

            for hook_index, hook in enumerate(entry_hooks):
                hook_location = f"{location}.hooks[{hook_index}]"
                if not isinstance(hook, dict):
                    errors.append(f"{hook_location} must be an object")
                    continue

                if hook.get("type") != "command":
                    errors.append(f"{hook_location}.type must be 'command'")

                command = hook.get("command")
                if not isinstance(command, str) or not command:
                    errors.append(f"{hook_location}.command must be a non-empty string")
                    continue

                timeout = hook.get("timeout")
                if not isinstance(timeout, int) or timeout <= 0:
                    errors.append(f"{hook_location}.timeout must be a positive integer")

                for local_path in sorted(referenced_local_paths(command)):
                    if not local_path.exists():
                        rel = local_path.relative_to(ROOT)
                        errors.append(f"{hook_location}.command references missing {rel}")

    validate_required_hook_commands(hooks, errors)


def validate_forbidden_surfaces(errors: list[str]) -> None:
    for rel_path in FORBIDDEN_SURFACES:
        path = ROOT / rel_path
        if path.exists():
            errors.append(f"forbidden runtime policy surface exists: {rel_path}")


def validate_legacy_agents_surface(errors: list[str]) -> None:
    legacy_root = ROOT / ".agents"
    if not legacy_root.exists():
        return

    for path in legacy_root.rglob("*"):
        if path.is_dir():
            continue
        rel_path = path.relative_to(ROOT).as_posix()
        if rel_path not in ALLOWED_LEGACY_AGENTS_FILES:
            errors.append(
                ".agents/** is legacy/helper-only; unexpected tracked-like surface "
                f"exists: {rel_path}"
            )


def validate_local_settings_separation(errors: list[str]) -> None:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", ".claude/settings.local.json"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result.returncode == 0:
        errors.append(".claude/settings.local.json must not be tracked")


def main() -> int:
    errors: list[str] = []
    settings = load_settings(errors)
    if settings:
        validate_permissions(settings, errors)
        validate_hooks(settings, errors)
        validate_required_script_markers(errors)
    validate_provider_neutral_dispatcher(errors)
    validate_forbidden_surfaces(errors)
    validate_legacy_agents_surface(errors)
    validate_local_settings_separation(errors)

    if errors:
        print("Runtime contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Runtime contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
