#!/usr/bin/env bash
# Docs README Sync Hook
# Called after Write|Edit|MultiEdit. Keeps docs/* README Documents tables fresh.

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"
TARGET="${CLAUDE_TOOL_RESULT_FILE_PATH:-${CLAUDE_TOOL_INPUT_FILE_PATH:-}}"

[[ -z "$TARGET" ]] && exit 0

DOCS_DIR="$PROJECT_DIR/docs"
[[ "$TARGET" == "$DOCS_DIR"/* ]] || exit 0

TARGET_DIR="$(dirname "$TARGET")"
[[ "$TARGET_DIR" != "$DOCS_DIR" ]] || exit 0

REL_DIR="${TARGET_DIR#"$DOCS_DIR/"}"
[[ "$REL_DIR" != "$TARGET_DIR" ]] || exit 0

"$PROJECT_DIR/scripts/docs/update-doc-readme-index.sh" "$REL_DIR" 2>/dev/null || true

# Bubble up one level: if the changed file is inside a stage subfolder (e.g.
# docs/03.specs/<package>/), also sync the parent stage README so the parent
# Documents table stays current without a manual batch run.
PARENT_DIR="$(dirname "$TARGET_DIR")"
if [[ "$PARENT_DIR" != "$DOCS_DIR" ]]; then
  PARENT_REL="${PARENT_DIR#"$DOCS_DIR/"}"
  [[ "$PARENT_REL" != "$PARENT_DIR" ]] && \
    "$PROJECT_DIR/scripts/docs/update-doc-readme-index.sh" "$PARENT_REL" 2>/dev/null || true
fi

exit 0
