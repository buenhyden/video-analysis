#!/usr/bin/env bash
# scaffold-tests-from-spec.sh
# Reads docs/03.specs/<feature-id>/spec.md and generates sibling tests.md.

set -euo pipefail

SPEC_FILE="${1:-}"

if [[ -z "$SPEC_FILE" ]]; then
  echo "Usage: ./scripts/qa/scaffold-tests-from-spec.sh docs/03.specs/<feature-id>/spec.md"
  exit 1
fi

if [[ ! -f "$SPEC_FILE" ]]; then
  echo "ERROR: File not found: $SPEC_FILE"
  exit 1
fi

NORMALIZED_SPEC="${SPEC_FILE#./}"
if [[ ! "$NORMALIZED_SPEC" =~ (^|/)docs/03\.specs/[^/]+/spec\.md$ ]]; then
  echo "ERROR: spec path must end with docs/03.specs/<feature-id>/spec.md" >&2
  exit 2
fi

SPEC_DIR=$(dirname "$SPEC_FILE")
TESTS_FILE="$SPEC_DIR/tests.md"
TEMPLATE="docs/99.templates/tests.template.md"

if [[ ! -f "$TEMPLATE" ]]; then
  echo "ERROR: Template not found: $TEMPLATE"
  exit 1
fi

if [[ -e "$TESTS_FILE" ]]; then
  echo "ERROR: tests.md already exists: $TESTS_FILE" >&2
  exit 3
fi

echo "Scaffolding tests from $SPEC_FILE..."

python3 - "$SPEC_FILE" "$TEMPLATE" "$TESTS_FILE" <<'EOF'
from __future__ import annotations

import datetime as dt
import getpass
import re
import sys
from pathlib import Path

spec_path = Path(sys.argv[1])
template_path = Path(sys.argv[2])
tests_path = Path(sys.argv[3])

DASH_VALUES = {"", "-", "—", "n/a", "N/A", "none", "None"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def spec_title(text: str) -> str:
    match = re.search(r"^title:\s*(.+)$", text, flags=re.M)
    if not match:
        return spec_path.parent.name
    return match.group(1).strip().strip('"').strip("'")


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def is_placeholder(cells: list[str]) -> bool:
    joined = " ".join(cells)
    markers = (
        "[Given/When/Then",
        "[Core behavior",
        "[Purpose]",
        "[Input]",
        "[Result]",
        "<feature>",
        "<name>",
    )
    return any(marker in joined for marker in markers)


def tdd_readiness_lines(text: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## TDD Readiness"):
            start = index + 1
            break
    if start is None:
        return []
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return lines[start:end]


def acceptance_mapping_rows(text: str) -> list[dict[str, str]]:
    lines = tdd_readiness_lines(text)
    heading_index = None
    for index, line in enumerate(lines):
        if line.startswith("### Acceptance Criteria ") and "Test Case Mapping" in line:
            heading_index = index
            break
    if heading_index is None:
        return []

    table_lines: list[str] = []
    table_started = False
    for line in lines[heading_index + 1 :]:
        if line.startswith("### "):
            break
        if line.strip().startswith("|"):
            table_started = True
            table_lines.append(line)
        elif table_started:
            break

    if len(table_lines) < 2:
        return []

    headers = [header.lower() for header in split_row(table_lines[0])]
    rows: list[dict[str, str]] = []
    for line in table_lines[1:]:
        cells = split_row(line)
        if is_separator(cells) or is_placeholder(cells):
            continue
        if len(cells) < len(headers):
            continue
        row = {headers[index]: cells[index] for index in range(len(headers))}
        rows.append(row)
    return rows


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|")


def code_cell(value: str) -> str:
    cleaned = value.strip()
    if cleaned in DASH_VALUES:
        return "—"
    if cleaned.startswith("`") and cleaned.endswith("`"):
        return cleaned
    return f"`{cleaned.strip('`')}`"


def is_exempt(row: dict[str, str]) -> bool:
    return row.get("tdd exemption", "").strip() not in DASH_VALUES


def behavior_label(row: dict[str, str]) -> str:
    ac_id = row.get("ac id", "").strip()
    criterion = row.get("acceptance criterion (from prd)", row.get("acceptance criterion", "")).strip()
    if ac_id and criterion:
        return f"{ac_id} - {criterion}"
    return ac_id or criterion or "Unmapped behavior"


def targets_table(rows: list[dict[str, str]], has_exemptions: bool) -> str:
    table = [
        "| Behavior | Test File | RED status | GREEN status | REFACTORED |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for row in rows:
        table.append(
            "| "
            + " | ".join(
                [
                    escape_cell(behavior_label(row)),
                    code_cell(row.get("test location", "")),
                    "☐",
                    "☐",
                    "☐",
                ]
            )
            + " |"
        )
    if not rows and has_exemptions:
        table.append("| _No non-exempt behaviors_ | — | — | — | — |")
    return "\n".join(table)


def exemptions_table(rows: list[dict[str, str]]) -> str:
    table = [
        "| Scope | Reason | Approved by |",
        "| :--- | :--- | :--- |",
    ]
    if not rows:
        table.append("| — | — | — |")
        return "\n".join(table)
    for row in rows:
        table.append(
            "| "
            + " | ".join(
                [
                    escape_cell(behavior_label(row)),
                    escape_cell(row.get("tdd exemption", "").strip()),
                    "Spec TDD Readiness",
                ]
            )
            + " |"
        )
    return "\n".join(table)


def replace_table_after_heading(content: str, heading: str, table: str) -> str:
    pattern = rf"({re.escape(heading)}\n\n)(?:\|[^\n]*\n)+"
    return re.sub(pattern, lambda match: match.group(1) + table + "\n", content, count=1)


spec_text = read_text(spec_path)
content = read_text(template_path)
title = spec_title(spec_text)

content = content.replace("title: <string>", f"title: Test Strategy for {title}")
content = content.replace("version: <string>", "version: alpha")
content = content.replace("owner: <string>", f"owner: {getpass.getuser()}")
content = content.replace("last-updated: YYYY-MM-DD", f"last-updated: {dt.date.today().isoformat()}")

rows = acceptance_mapping_rows(spec_text)
target_rows = [row for row in rows if not is_exempt(row)]
exempt_rows = [row for row in rows if is_exempt(row)]

if rows:
    content = replace_table_after_heading(
        content,
        "### Red-Green-Refactor Targets",
        targets_table(target_rows, bool(exempt_rows)),
    )
    content = replace_table_after_heading(
        content,
        "### TDD Exemptions",
        exemptions_table(exempt_rows),
    )

tests_path.write_text(content.rstrip() + "\n", encoding="utf-8")
EOF

echo "✅ Generated: $TESTS_FILE"
