#!/usr/bin/env bash

# Quality Gate: Conditional Test Coverage Enforcement

set -euo pipefail

# Every pull request with an active implementation stack must provide a
# parseable coverage artifact and meet the repository minimum. The base
# Project-Template may have no application stack yet; in that case, no coverage
# artifact is expected.

MIN_COVERAGE="${MIN_COVERAGE:-90}"
COVERAGE_FILE="${1:-${COVERAGE_FILE:-coverage/coverage.xml}}"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

has_active_stack_manifest() {
  local manifest
  local manifests=(
    "package.json"
    "pnpm-lock.yaml"
    "yarn.lock"
    "package-lock.json"
    "pyproject.toml"
    "requirements.txt"
    "poetry.lock"
    "Pipfile"
    "go.mod"
    "Cargo.toml"
    "pom.xml"
    "build.gradle"
    "build.gradle.kts"
    "Gemfile"
    "composer.json"
    "mix.exs"
  )

  for manifest in "${manifests[@]}"; do
    if find "$REPO_ROOT" \
      -path "$REPO_ROOT/.git" -prune -o \
      -path "$REPO_ROOT/node_modules" -prune -o \
      -path "$REPO_ROOT/.venv" -prune -o \
      -path "$REPO_ROOT/venv" -prune -o \
      -path "$REPO_ROOT/docs/99.templates" -prune -o \
      -path "$REPO_ROOT/examples" -prune -o \
      -name "$manifest" -type f -print -quit | grep -q .; then
      return 0
    fi
  done

  return 1
}

if [[ ! -f "$COVERAGE_FILE" ]]; then
  if ! has_active_stack_manifest; then
    echo "QUALITY GATE SKIPPED: no active stack manifest found; coverage artifact is not required for the base template."
    echo "When a derived project declares an implementation stack, provide '$COVERAGE_FILE' and meet ${MIN_COVERAGE}% line coverage."
    exit 0
  fi

  echo "QUALITY GATE FAILED: mandatory coverage report '$COVERAGE_FILE' was not found."
  exit 1
fi

ACTUAL_COVERAGE=$(
  python3 - "$COVERAGE_FILE" <<'PY'
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="ignore")


def emit(value: float) -> None:
    print(f"{value:.2f}")
    raise SystemExit(0)


# coverage.py XML and Cobertura XML expose line-rate as a 0..1 value.
try:
    root = ET.fromstring(text)
    line_rate = root.attrib.get("line-rate")
    if line_rate is not None:
        emit(float(line_rate) * 100)
except ET.ParseError:
    pass

# lcov.info exposes lines found/hit as LF/LH records.
lines_found = sum(int(value) for value in re.findall(r"^LF:(\d+)$", text, re.MULTILINE))
lines_hit = sum(int(value) for value in re.findall(r"^LH:(\d+)$", text, re.MULTILINE))
if lines_found:
    emit(lines_hit * 100 / lines_found)

# Simple summaries may contain "Lines: 90%" or "Line coverage: 90.5%".
match = re.search(r"(?im)\bline(?:s| coverage)?\s*:\s*([0-9]+(?:\.[0-9]+)?)\s*%", text)
if match:
    emit(float(match.group(1)))

raise SystemExit("Unable to parse line coverage from the provided coverage report.")
PY
)

echo "Required Coverage: ${MIN_COVERAGE}%"
echo "Actual Coverage:   ${ACTUAL_COVERAGE}%"

python3 - "$MIN_COVERAGE" "$ACTUAL_COVERAGE" <<'PY'
from __future__ import annotations

import sys

minimum = float(sys.argv[1])
actual = float(sys.argv[2])
if actual < minimum:
    print(f"QUALITY GATE FAILED: Code coverage is below the {minimum:g}% minimum threshold.")
    raise SystemExit(1)

print("QUALITY GATE PASSED: Code coverage meets the required standard.")
PY
