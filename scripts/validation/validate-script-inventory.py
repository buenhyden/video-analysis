#!/usr/bin/env python3
"""Validate active workspace script and ws command inventory."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "scripts"
README = SCRIPTS_DIR / "README.md"
WS = SCRIPTS_DIR / "ws.sh"

EXPECTED_WS_COMMANDS = {
    "audit",
    "bootstrap",
    "dispatch",
    "docs",
    "heal",
    "help",
    "hook",
    "info",
    "intelligence",
    "sbom",
    "setup",
    "swarm",
    "validate",
    "validate-derived",
    "validate-distribution",
}
FORBIDDEN_ACTIVE_COMMANDS = {
    "architect",
    "autopilot",
    "compactor",
    "cost",
    "fix",
    "monitor",
    "package",
    "pipeline",
    "project-scaffold",
    "propose",
    "quality",
    "scaffold",
}
FORBIDDEN_SCRIPT_REFS = {
    "".join(parts)
    for parts in [
        ("project", "_architect.py"),
        ("pipeline", "_generator.py"),
        ("code_quality", "_analyzer.py"),
        ("fullstack", "_scaffolder.py"),
        ("project", "_scaffolder.py"),
        ("evolution", "-proposer.py"),
        ("evolution", "-fixer.py"),
        ("trash", "-compactor.py"),
    ]
}
REMOVED_SCRIPT_NAMES = {
    "".join(parts)
    for parts in [
        ("generate-llm-wiki", "-index.py"),
        ("index", "-knowledge.sh"),
        ("rename", "-project.sh"),
        ("validate-commit", "-messages.sh"),
    ]
}
SELF_HEAL_FORBIDDEN_PATTERNS = {
    r"\bcp\b[^\n]*\.env": "self-heal must not copy or create .env files",
    r">>\s*[^\n]*\.env": "self-heal must not append to .env files",
    r"(?<!>)>\s*[^\n]*\.env": "self-heal must not redirect output into .env files",
    r"\btee\b[^\n]*\.env": "self-heal must not write .env files through tee",
    r"\bsed\b[^\n]*-i[^\n]*\.env": "self-heal must not edit .env files in place",
    r"\bmv\b[^\n]*\.env": "self-heal must not move or replace .env files",
}
DOC_PATHS = [
    ROOT / "AGENTS.md",
    ROOT / "CLAUDE.md",
    ROOT / "GEMINI.md",
    ROOT / ".claude",
    ROOT / "docs/00.agent-governance",
    ROOT / "docs/LLM-WIKI.md",
    ROOT / "docs/05.operations/guides",
    ROOT / "docs/05.operations/policies",
    ROOT / "docs/90.references",
]
COMMAND_FIRST_SWARM_PATTERN = re.compile(
    r"\b(?:bash\s+scripts/ws\.sh\s+)?ws\s+swarm\s+"
    r"(start|status|handoff|suggest)(?=\s|`|$)",
    re.IGNORECASE,
)
NON_CANONICAL_SWARM_PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:bash\s+scripts/ws\.sh\s+)?ws\s+swarm\s+<task-id>\b|<next-role>\b",
    re.IGNORECASE,
)


def ws_help_commands(text: str) -> set[str]:
    return set(re.findall(r'echo "  ([a-z][a-z0-9-]*)\s+-', text))


def ws_case_commands(text: str) -> set[str]:
    commands = set(re.findall(r"^\s{2}([a-z][a-z0-9-]*)\)", text, re.MULTILINE))
    commands.add("help")
    return commands


VALID_STATUSES = {
    "active-ws",
    "active-ci",
    "active-direct",
    "reserved-direct",
    "optional-example",
}
RETENTION_MARKERS = {
    "ws consumer",
    "ci consumer",
    "documented direct governance use",
    "reserved direct use",
    "derived-project conditional value",
}
REQUIRED_STATUS_MARKERS = {
    "active-ws": "ws consumer",
    "active-ci": "ci consumer",
    "active-direct": "documented direct governance use",
    "reserved-direct": "reserved direct use",
}
DIRECT_PURPOSE_PATTERN = re.compile(r"\bdirect (command|helper)\b", re.IGNORECASE)


def inventory_rows(text: str) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for line in text.splitlines():
        match = re.match(r"\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|", line)
        if match:
            status = match.group(1).strip()
            script = match.group(2).strip()
            purpose = match.group(3).strip()
            if status in VALID_STATUSES:
                rows.append((status, script, purpose))
    return rows


def retention_markers(purpose: str) -> set[str]:
    purpose_lower = purpose.lower()
    return {marker for marker in RETENTION_MARKERS if marker in purpose_lower}


def direct_command_scripts(text: str) -> set[str]:
    match = re.search(r"^## Direct Commands\n(?P<body>.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        return set()
    return set(re.findall(r"`(?:bash|python3)\s+scripts/([^`\s]+)", match.group("body")))


def script_files() -> set[str]:
    return {
        child.relative_to(SCRIPTS_DIR).as_posix()
        for child in SCRIPTS_DIR.rglob("*")
        if child.is_file()
        and child.suffix in {".sh", ".py"}
        and "__pycache__" not in child.parts
    }


def iter_text_files(path: Path):
    if path.is_file():
        yield path
        return
    for child in path.rglob("*"):
        if child.is_file() and child.suffix in {".md", ".sh", ".py", ".json", ".yaml", ".yml"}:
            yield child


def main() -> int:
    errors: list[str] = []
    readme_text = README.read_text(encoding="utf-8")
    ws_text = WS.read_text(encoding="utf-8")
    dispatch_text = (SCRIPTS_DIR / "harness/dispatch-subagent.sh").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    self_heal_text = (SCRIPTS_DIR / "harness/self-heal.sh").read_text(
        encoding="utf-8",
        errors="ignore",
    )
    github_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in (ROOT / ".github").rglob("*")
        if path.is_file() and path.suffix in {".md", ".sh", ".py", ".json", ".yaml", ".yml", ""}
    )

    help_commands = ws_help_commands(ws_text)
    case_commands = ws_case_commands(ws_text)
    if help_commands != EXPECTED_WS_COMMANDS:
        errors.append(
            f"scripts/ws.sh help commands drift: expected {sorted(EXPECTED_WS_COMMANDS)}, got {sorted(help_commands)}"
        )
    if case_commands != EXPECTED_WS_COMMANDS:
        errors.append(
            f"scripts/ws.sh case commands drift: expected {sorted(EXPECTED_WS_COMMANDS)}, got {sorted(case_commands)}"
        )
    forbidden_exposed = (help_commands | case_commands) & FORBIDDEN_ACTIVE_COMMANDS
    if forbidden_exposed:
        errors.append(f"forbidden ws commands exposed: {sorted(forbidden_exposed)}")

    rows = inventory_rows(readme_text)
    direct_commands = direct_command_scripts(readme_text)
    if not rows:
        errors.append("scripts/README.md does not contain a validated script inventory")
    llm_wiki_text = (ROOT / "docs/LLM-WIKI.md").read_text(encoding="utf-8", errors="ignore")
    for status in sorted(VALID_STATUSES):
        if status not in readme_text:
            errors.append(f"scripts/README.md does not document `{status}` script retention")
        if status not in llm_wiki_text:
            errors.append(f"docs/LLM-WIKI.md does not document `{status}` script retention")

    direct_inventory = {script for status, script, _purpose in rows if status != "optional-example"}
    actual_scripts = script_files()
    missing_inventory = actual_scripts - direct_inventory
    stale_inventory = direct_inventory - actual_scripts
    unexpected_root_scripts = {
        script
        for script in actual_scripts
        if "/" not in script and script not in {"ws.sh"}
    }
    if missing_inventory:
        errors.append(f"scripts missing from scripts/README.md inventory: {sorted(missing_inventory)}")
    if stale_inventory:
        errors.append(f"scripts/README.md lists removed scripts: {sorted(stale_inventory)}")
    if unexpected_root_scripts:
        errors.append(
            "root scripts/ may contain only ws.sh and README.md; move these scripts into a purpose folder: "
            f"{sorted(unexpected_root_scripts)}"
        )

    nested_script_basenames = {
        Path(script).name
        for script in actual_scripts
        if "/" in script
    }

    seen_scripts: set[str] = set()
    for status, script, purpose in rows:
        if script in seen_scripts:
            errors.append(f"scripts/README.md lists duplicate script `{script}`")
        seen_scripts.add(script)

        markers = retention_markers(purpose)
        if status in REQUIRED_STATUS_MARKERS and not markers:
            errors.append(f"scripts/README.md lists `{script}` without a `Basis:` retention marker")
        required_marker = REQUIRED_STATUS_MARKERS.get(status)
        if required_marker and required_marker not in markers:
            errors.append(
                f"scripts/README.md lists `{script}` as {status} without `Basis: {required_marker}`"
            )
        if status == "active-direct" and not DIRECT_PURPOSE_PATTERN.search(purpose):
            errors.append(
                f"scripts/README.md lists `{script}` as active-direct without a concrete direct-command purpose"
            )

        script_path = SCRIPTS_DIR / script
        if status != "optional-example" and not script_path.exists():
            errors.append(f"scripts/README.md lists missing {status} script `{script}`")
            continue
        if status == "active-ws" and script != "ws.sh" and script not in ws_text:
            errors.append(f"scripts/README.md lists `{script}` as active-ws but scripts/ws.sh does not invoke it")
        if status == "active-ci" and script not in github_text:
            errors.append(f"scripts/README.md lists `{script}` as active-ci but .github/** does not invoke it")
        if status == "active-direct" and script not in direct_commands:
            errors.append(f"scripts/README.md lists `{script}` as active-direct without a Direct Commands entry")
        if status == "reserved-direct" and not purpose.startswith("Reserved"):
            errors.append(f"scripts/README.md lists `{script}` as reserved-direct without a Reserved purpose")
        if status == "optional-example":
            if script.startswith("examples/"):
                if not (ROOT / script).exists():
                    errors.append(f"optional example script `{script}` is missing")
                if script in ws_text or script in github_text:
                    errors.append(f"optional example script `{script}` is required by active automation")
            elif (SCRIPTS_DIR / script).exists():
                errors.append(f"optional-example `{script}` must not live in active scripts/")

    active_script_refs = []
    for path in [ROOT / ".github", ROOT / "scripts", ROOT / "README.md", *DOC_PATHS]:
        if not path.exists():
            continue
        for text_file in iter_text_files(path):
            if "examples/fullstack-starter" in str(text_file):
                continue
            if text_file == Path(__file__).resolve():
                continue
            text = text_file.read_text(encoding="utf-8", errors="ignore")
            if COMMAND_FIRST_SWARM_PATTERN.search(text):
                errors.append(
                    f"{text_file.relative_to(ROOT)} documents command-first `ws swarm <command>` syntax; "
                    "use `ws swarm <task_id> <command>` as canonical"
                )
            if NON_CANONICAL_SWARM_PLACEHOLDER_PATTERN.search(text):
                errors.append(
                    f"{text_file.relative_to(ROOT)} documents non-canonical `ws swarm` placeholders; "
                    "use `ws swarm <task_id> <start|status|handoff|suggest> [next_role]`"
                )
            for root_script_ref in re.findall(r"\bscripts/([A-Za-z0-9_.-]+\.(?:sh|py))", text):
                if root_script_ref in nested_script_basenames:
                    active_script_refs.append(
                        f"{text_file.relative_to(ROOT)} references stale root script path "
                        f"`scripts/{root_script_ref}`"
                    )
            for command in re.findall(r"\bws\s+([a-z][a-z0-9-]*)", text):
                if command not in EXPECTED_WS_COMMANDS and command not in {"command", "consumer"}:
                    errors.append(f"{text_file.relative_to(ROOT)} references inactive `ws {command}`")
            for script_ref in FORBIDDEN_SCRIPT_REFS:
                if script_ref in text:
                    active_script_refs.append(f"{text_file.relative_to(ROOT)} references `{script_ref}`")
            for removed_script in REMOVED_SCRIPT_NAMES:
                if removed_script in text:
                    active_script_refs.append(
                        f"{text_file.relative_to(ROOT)} references removed script `{removed_script}`"
                    )

    errors.extend(active_script_refs)

    forbidden_dispatch_patterns = {
        "git checkout -b": "dispatch must not create branches",
        "".join(("file", "://")): "dispatch must not emit machine-specific absolute links",
        "s/<string>": "dispatch must not broad-replace template placeholders",
        "sed -i": "dispatch must not mutate Stage 06 task files",
        "cp \"$TEMPLATE_FILE\"": "dispatch must not scaffold authoritative task documents",
    }
    for pattern, reason in forbidden_dispatch_patterns.items():
        if pattern in dispatch_text:
            errors.append(f"scripts/harness/dispatch-subagent.sh contains forbidden pattern `{pattern}` ({reason})")

    for pattern, reason in SELF_HEAL_FORBIDDEN_PATTERNS.items():
        if re.search(pattern, self_heal_text):
            errors.append(f"scripts/harness/self-heal.sh contains forbidden mutating pattern `{pattern}` ({reason})")

    if errors:
        print("Script inventory validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Script inventory validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
