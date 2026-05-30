#!/usr/bin/env bash
# PostToolUseFailure Hook — logs tool failures to transient workspace diagnostics
# Non-blocking: always exits 0; does not block agent execution on write failure

set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"

DIAG="$PROJECT_DIR/_workspace/diagnostics"
mkdir -p "$DIAG" 2>/dev/null || true

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "unknown-time")
TOOL="${CLAUDE_TOOL_NAME:-unknown}"
FILE="${CLAUDE_TOOL_INPUT_FILE_PATH:-}"
ERROR="${CLAUDE_TOOL_ERROR:-}"

# Supplement env vars with stdin JSON (Claude Code sends error details via stdin)
if [ ! -t 0 ]; then
  STDIN_DATA=$(cat 2>/dev/null || true)
  if [[ -n "$STDIN_DATA" ]]; then
    PARSED=$(printf '%s' "$STDIN_DATA" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    tool = d.get('tool_name', '')
    tr = d.get('tool_response') or {}
    err = tr.get('error', '') if isinstance(tr, dict) else ''
    err = err or d.get('error', '')
    print(tool + '|' + str(err)[:200])
except Exception:
    print('|')
" 2>/dev/null || echo "|")
    IFS='|' read -r PARSED_TOOL PARSED_ERROR <<< "$PARSED"
    [[ -n "$PARSED_TOOL" && "$TOOL" == "unknown" ]] && TOOL="$PARSED_TOOL"
    [[ -n "$PARSED_ERROR" && -z "$ERROR" ]] && ERROR="$PARSED_ERROR"
  fi
fi

# Truncate error to avoid bloated log lines
TRUNCATED_ERROR="${ERROR:0:200}"
LOG_LINE="[$TIMESTAMP] FAIL tool=$TOOL file=${FILE:-none} error=${TRUNCATED_ERROR:-no-error-detail}"

printf '%s\n' "$LOG_LINE" >> "$DIAG/hook-errors.log" 2>/dev/null || true

exit 0
