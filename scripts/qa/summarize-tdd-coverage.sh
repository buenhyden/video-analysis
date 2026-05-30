#!/usr/bin/env bash
set -euo pipefail

# summarize-tdd-coverage.sh
# Scans execution task files for rows marked 'impl' and summarizes TDD status.

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")"
TASKS_DIR="$REPO_ROOT/docs/04.execution/tasks"
FAIL_ON_MISSING=false

usage() {
  echo "Usage: bash scripts/qa/summarize-tdd-coverage.sh [--fail-on-missing] [--tasks-dir <path>]" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --fail-on-missing)
      FAIL_ON_MISSING=true
      shift
      ;;
    --tasks-dir)
      if [[ -z "${2:-}" ]]; then
        usage
        exit 2
      fi
      TASKS_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unsupported option '$1'." >&2
      usage
      exit 2
      ;;
  esac
done

if [[ ! -d "$TASKS_DIR" ]]; then
  echo "Tasks directory not found: $TASKS_DIR"
  exit 1
fi

echo "=== TDD Coverage Summary ==="
if [[ "$FAIL_ON_MISSING" == "true" ]]; then
  echo "Mode: fail on missing implementation TDD evidence"
fi
echo ""

python3 - "$TASKS_DIR" "$FAIL_ON_MISSING" <<'PY'
from __future__ import annotations

import re
import sys
from pathlib import Path

tasks_dir = Path(sys.argv[1])
fail_on_missing = sys.argv[2] == "true"
total = 0
with_evidence = 0


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def meaningful(value: str) -> bool:
    stripped = value.strip().lower()
    if not stripped or stripped in {"-", "—", "n/a", "todo", "[action]"}:
        return False
    return bool(re.search(r"[a-z0-9가-힣]", stripped))


def task_table_rows(text: str) -> list[tuple[dict[str, int], list[str]]]:
    lines = text.splitlines()
    rows: list[tuple[dict[str, int], list[str]]] = []
    for index, line in enumerate(lines):
        if line.strip().lower() != "## task table":
            continue
        table_lines: list[str] = []
        for candidate in lines[index + 1 :]:
            if candidate.startswith("## "):
                break
            if candidate.strip().startswith("|"):
                table_lines.append(candidate)
            elif table_lines:
                break
        if len(table_lines) < 2:
            continue
        headers = [header.lower() for header in split_row(table_lines[0])]
        header_index = {header: position for position, header in enumerate(headers)}
        for row in table_lines[2:]:
            cells = split_row(row)
            if len(cells) >= len(headers):
                rows.append((header_index, cells))
    return rows


for task_file in sorted(tasks_dir.glob("*.md")):
    if task_file.name == "README.md":
        continue
    text = task_file.read_text(encoding="utf-8")
    file_impl_count = 0
    file_evidence_count = 0

    for headers, cells in task_table_rows(text):
        type_index = headers.get("type")
        if type_index is None or type_index >= len(cells):
            continue
        if cells[type_index].strip().lower() != "impl":
            continue

        total += 1
        file_impl_count += 1
        task_id = cells[headers.get("task id", 0)] if headers.get("task id", 0) < len(cells) else "unknown"
        status = cells[headers["tdd status"]] if "tdd status" in headers and headers["tdd status"] < len(cells) else ""
        exemption = cells[headers["tdd exemption"]] if "tdd exemption" in headers and headers["tdd exemption"] < len(cells) else ""
        validation = cells[headers["validation / evidence"]] if "validation / evidence" in headers and headers["validation / evidence"] < len(cells) else ""

        has_tdd_status = meaningful(status) and bool(re.search(r"red|green|refactor|pass|fail", status, re.IGNORECASE))
        has_exemption = meaningful(exemption)
        has_validation = meaningful(validation)
        has_evidence = has_tdd_status or has_exemption or has_validation

        if has_evidence:
            with_evidence += 1
            file_evidence_count += 1
            print(f"✅ {task_file.name} {task_id}")
        else:
            print(f"❌ {task_file.name} {task_id}")

    if file_impl_count == 0 and re.search(r"^- Type:.*impl", text, re.MULTILINE):
        total += 1
        file_impl_count += 1
        has_evidence = bool(
            re.search(r"^## TDD Evidence[\s\S]*?[A-Za-z0-9가-힣]", text, re.MULTILINE)
        )
        if has_evidence:
            with_evidence += 1
            file_evidence_count += 1
            print(f"✅ {task_file.name} legacy-type")
        else:
            print(f"❌ {task_file.name} legacy-type")

missing = total - with_evidence
print()
print(f"Total 'impl' tasks: {total}")
print(f"Tasks with TDD Evidence: {with_evidence}")
print(f"Tasks missing TDD Evidence: {missing}")
if total:
    print(f"TDD Coverage: {with_evidence * 100 // total}%")
else:
    print("TDD Coverage: N/A (no 'impl' tasks found)")

if fail_on_missing and missing:
    print("ERROR: implementation tasks are missing TDD evidence.", file=sys.stderr)
    sys.exit(1)
PY
