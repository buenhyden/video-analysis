#!/usr/bin/env bash
# PreCompact Hook — saves workspace state snapshot before context compaction
# Non-blocking: always exits 0; transient output goes to _workspace/diagnostics/

set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"

DIAG="$PROJECT_DIR/_workspace/diagnostics"
mkdir -p "$DIAG" 2>/dev/null || true

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "unknown-time")
BRANCH=$(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null || echo "unknown")
CHANGED=$(git -C "$PROJECT_DIR" status --short 2>/dev/null | head -20 || echo "none")
LAST_COMMITS=$(git -C "$PROJECT_DIR" log -5 --format="%h %s" 2>/dev/null || echo "none")

PROGRESS_SNIPPET=""
PROGRESS_FILE="$PROJECT_DIR/docs/00.agent-governance/memory/progress.md"
if [[ -f "$PROGRESS_FILE" ]]; then
  PROGRESS_SNIPPET=$(grep -E "Task ID|Status|Description" "$PROGRESS_FILE" 2>/dev/null | head -6 || echo "")
fi

{
  printf '# Pre-Compact Context Snapshot\n'
  printf '# Saved: %s\n\n' "$TIMESTAMP"
  printf '## Branch\n%s\n\n' "$BRANCH"
  printf '## Changed Files (up to 20)\n%s\n\n' "${CHANGED:-none}"
  printf '## Last 5 Commits\n%s\n\n' "$LAST_COMMITS"
  printf '## Active Task (from memory/progress.md)\n%s\n' "${PROGRESS_SNIPPET:-not available}"
} > "$DIAG/pre-compact-context.txt" 2>/dev/null || true

exit 0
