#!/usr/bin/env bash
# Post-Tool Validate Hook — runs governance + cross-link validation after writes
# Called after Write|Edit|MultiEdit tool execution
# Non-blocking: always exits 0; prints warnings to stderr

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"

# PostToolUse with Write/Edit: Claude Code sets CLAUDE_TOOL_INPUT_FILE_PATH on the hook env;
# CLAUDE_TOOL_RESULT_FILE_PATH is populated only when replaying via ws hook dispatch.
TARGET="${CLAUDE_TOOL_RESULT_FILE_PATH:-${CLAUDE_TOOL_INPUT_FILE_PATH:-}}"
RUN_GLOBAL=0

cd "$PROJECT_DIR" || exit 0

# Post-write GitHub token scan (non-blocking: warns but does not exit 1)
# Repository-local files must not contain GitHub token literals.
if [[ -z "$TARGET" ]]; then
  RUN_GLOBAL=1
  REL_TARGET="<unspecified>"
else
  REL_TARGET="${TARGET#"$PROJECT_DIR/"}"
fi
GITHUB_TOKEN_PATTERN='(ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{82})'
if [[ -f "$TARGET" ]]; then
  if grep -qEe "$GITHUB_TOKEN_PATTERN" "$TARGET" 2>/dev/null; then
    echo "❌ POST-TOOL ALERT: GitHub token literal found in '$REL_TARGET' after write." >&2
    echo "   Revoke the exposed token immediately, then remove it from the file." >&2
    echo "   See docs/00.agent-governance/rules/github-repository-governance.md §5." >&2
  fi
fi

# Only run governance checks if the file is inside docs/, .github/, or .claude/.
# Provider-neutral replays through `ws hook` may not have Claude's target-file
# environment; in that case run repository-level document readiness checks.
if [[ "$RUN_GLOBAL" -ne 1 ]] && [[ "$TARGET" != */docs/* ]] && [[ "$TARGET" != */.github/* ]] && [[ "$TARGET" != */.claude/* ]]; then
  exit 0
fi

# Run governance validation (non-blocking)
if [[ -x "$PROJECT_DIR/scripts/validation/validate-doc-governance.sh" ]]; then
  bash "$PROJECT_DIR/scripts/validation/validate-doc-governance.sh" 2>&1 | grep -E "^(ERROR|WARN|❌|⚠️)" >&2 || true
fi

# Run template-readiness validation so stage documents preserve their docs/99.templates contract.
if [[ -f "$PROJECT_DIR/scripts/validation/validate-doc-readiness.py" ]]; then
  python3 "$PROJECT_DIR/scripts/validation/validate-doc-readiness.py" 2>&1 | grep -E "^(Template readiness validation failed:|- docs/|- README|- scripts/|- \.)" >&2 || true
fi

# Run cross-link validation on modified file's directory (non-blocking)
TARGET_DIR="$PROJECT_DIR/docs"
if [[ -n "$TARGET" ]]; then
  TARGET_DIR=$(dirname "$TARGET")
fi
if [[ -x "$PROJECT_DIR/scripts/validation/validate-cross-links.sh" ]]; then
  bash "$PROJECT_DIR/scripts/validation/validate-cross-links.sh" "$TARGET_DIR" 2>&1 | grep -E "^(ERROR|WARN|❌|⚠️)" >&2 || true
fi

exit 0
