#!/usr/bin/env python3
"""Validate incoming stage-document write content against template contracts.

This helper is intentionally narrow: it runs during PreToolUse and validates
only the content supplied with the pending write. Existing files remain covered
by validate-doc-readiness.py on PostToolUse, Stop, and ws validate.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
READINESS = ROOT / "scripts/validation/validate-doc-readiness.py"


def load_readiness() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_doc_readiness", READINESS)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load validate-doc-readiness.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_hook_json() -> dict[str, Any]:
    if sys.stdin.isatty():
        return {}
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def rel_path_for(target: str) -> str:
    path = Path(target)
    if path.is_absolute():
        try:
            return path.relative_to(ROOT).as_posix()
        except ValueError:
            return path.as_posix()
    return path.as_posix()


def first_text(*values: object) -> str:
    for value in values:
        if isinstance(value, str) and value:
            return value
    return ""


def tool_input_from_hook() -> tuple[str, str]:
    hook_json = read_hook_json()
    tool_input = hook_json.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}

    target = first_text(
        os.environ.get("CLAUDE_TOOL_INPUT_FILE_PATH"),
        os.environ.get("CLAUDE_TOOL_INPUT_PATH"),
        tool_input.get("file_path"),
        tool_input.get("path"),
    )
    content = first_text(
        os.environ.get("CLAUDE_TOOL_INPUT_CONTENT"),
        os.environ.get("CLAUDE_TOOL_INPUT_NEW_TEXT"),
        os.environ.get("CLAUDE_TOOL_INPUT_NEW_STRING"),
        tool_input.get("content"),
        tool_input.get("new_text"),
        tool_input.get("new_string"),
    )
    return target, content


def is_target_markdown_stage_doc(rel: str) -> bool:
    path = Path(rel)
    if path.suffix != ".md" or path.name == "README.md":
        return False
    return any(
        rel.startswith(f"docs/{stage}/")
        for stage in (
            "01.requirements",
            "02.architecture",
            "03.specs",
            "04.execution",
            "05.operations",
            "90.references",
        )
    )


def machine_readable_issues(rel: str, content: str) -> list[str]:
    path = Path(rel)
    if not rel.startswith("docs/03.specs/") or path.suffix not in {
        ".yaml",
        ".yml",
        ".graphql",
        ".proto",
    }:
        return []

    if path.name in {"openapi.yaml", "openapi.yml"}:
        required = ["openapi:", "info:", "paths:"]
        template = "openapi.template.yaml"
    elif path.name == "schema.graphql":
        required = ["schema", "type "]
        template = "extended/schema.template.graphql"
    elif path.name == "service.proto":
        required = ['syntax = "proto3";', "service "]
        template = "extended/service.template.proto"
    else:
        return [
            "machine-readable spec contract must use an approved docs/99.templates "
            "target name: openapi.yaml, schema.graphql, or service.proto"
        ]

    missing = [marker for marker in required if marker not in content]
    if missing:
        return [f"does not match {template}; missing markers {missing}"]
    return []


def main() -> int:
    target, content = tool_input_from_hook()
    if not target or not content:
        return 0

    rel = rel_path_for(target)
    issues: list[str] = []

    if is_target_markdown_stage_doc(rel):
        readiness = load_readiness()
        issues.extend(readiness.canonical_template_conformance_issues(content))
        issues.extend(readiness.stage_template_contract_issues(rel, content))
    else:
        issues.extend(machine_readable_issues(rel, content))

    if not issues:
        return 0

    print(
        f"PRE-TOOL BLOCK: {rel} does not satisfy its docs/99.templates contract.",
        file=sys.stderr,
    )
    for issue in issues:
        print(f"- {issue}", file=sys.stderr)
    print(
        "Start from the matching template and preserve required frontmatter, "
        "AI Execution Checklist, Related Documents, and stage-specific sections.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
