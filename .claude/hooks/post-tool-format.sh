#!/usr/bin/env bash
# Post-Tool Format Hook — applies safe formatting after Write/Edit/MultiEdit.
# Non-blocking: formatting failures warn but do not stop the agent session.

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"
TARGET="${CLAUDE_TOOL_RESULT_FILE_PATH:-${CLAUDE_TOOL_INPUT_FILE_PATH:-}}"

[[ -z "$TARGET" ]] && exit 0
[[ -f "$TARGET" ]] || exit 0

cd "$PROJECT_DIR" || exit 0
REL="${TARGET#"$PROJECT_DIR/"}"

case "$REL" in
  .git/*|node_modules/*|dist/*|coverage/*|.venv/*|.claude/*.local.md)
    exit 0
    ;;
esac

# Keep text files clean even when optional language formatters are unavailable.
python3 - "$TARGET" <<'PY' || true
from __future__ import annotations

import sys
from pathlib import Path

path = Path(sys.argv[1])
data = path.read_bytes()
if b"\0" in data:
    raise SystemExit(0)

try:
    text = data.decode("utf-8")
except UnicodeDecodeError:
    raise SystemExit(0)

normalized = text.replace("\r\n", "\n").replace("\r", "\n")
normalized = "\n".join(line.rstrip(" \t") for line in normalized.split("\n"))
if normalized and not normalized.endswith("\n"):
    normalized += "\n"

if normalized != text:
    path.write_text(normalized, encoding="utf-8")
    print(f"post-tool-format: normalized whitespace in {path}")
PY

case "$REL" in
  *.json|*.yaml|*.yml|*.md|*.mdx|*.js|*.jsx|*.ts|*.tsx|*.css|*.scss|*.html)
    if command -v prettier >/dev/null 2>&1; then
      prettier --write "$TARGET" >/dev/null 2>&1 || {
        echo "⚠️  post-tool-format: prettier failed for '$REL'." >&2
      }
    fi
    ;;
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      ruff format "$TARGET" >/dev/null 2>&1 || {
        echo "⚠️  post-tool-format: ruff format failed for '$REL'." >&2
      }
    elif command -v black >/dev/null 2>&1; then
      black --quiet "$TARGET" >/dev/null 2>&1 || {
        echo "⚠️  post-tool-format: black failed for '$REL'." >&2
      }
    fi
    ;;
  *.sh|*.bash)
    if command -v shfmt >/dev/null 2>&1; then
      shfmt -w "$TARGET" >/dev/null 2>&1 || {
        echo "⚠️  post-tool-format: shfmt failed for '$REL'." >&2
      }
    fi
    ;;
esac

exit 0
