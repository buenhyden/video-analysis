#!/usr/bin/env bash
# Stop Completion Governance Hook — prevents silent handoff with dirty changes.

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"

cd "$PROJECT_DIR" || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

if [[ "${AGENT_ALLOW_DIRTY_STOP:-0}" == "1" ]]; then
  exit 0
fi

STATUS="$(git status --porcelain)"
[[ -z "$STATUS" ]] && exit 0

BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"

{
  echo "❌ STOP BLOCK: Uncommitted workspace changes remain on branch '$BRANCH'."
  echo ""
  echo "Before stopping, the AI agent must either:"
  echo "1. Group its own changes into logical units, run the relevant validation, stage only those files, and create Conventional Commit(s)."
  echo "2. If the user explicitly requested no commit or unrelated user changes are present, record the handoff clearly and set AGENT_ALLOW_DIRTY_STOP=1 only for that stop attempt."
  echo ""
  echo "Dirty paths:"
  printf '%s\n' "$STATUS"
} >&2

exit 2
