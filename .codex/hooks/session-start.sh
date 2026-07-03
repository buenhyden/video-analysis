#!/usr/bin/env bash
# Session Start Hook — injects governance context at session open
# Outputs to stdout so Claude Code picks it up as session context

set -uo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"

cd "$PROJECT_DIR" || exit 0

# Git context
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
LAST_COMMIT=$(git log -1 --format="%h %s" 2>/dev/null || echo "none")
CHANGED_FILES=$(git status --short 2>/dev/null | wc -l | tr -d ' ')

# Governance summary (existence checks only — fast)
AGENT_CATALOG="✅"
SUBAGENT_PROTO="✅"
SCOPES_COUNT=$(find "$PROJECT_DIR/docs/00.agent-governance/scopes" -maxdepth 1 -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ' || echo "0")
SETTINGS_LOCAL_STATE="✅ gitignored"

[[ ! -f "$PROJECT_DIR/AGENTS.md" ]] && AGENT_CATALOG="❌ MISSING"
[[ ! -f "$PROJECT_DIR/docs/00.agent-governance/rules/subagent-protocol.md" ]] && SUBAGENT_PROTO="❌ MISSING"
git ls-files "$PROJECT_DIR/.claude/settings.local.json" | grep -q . && SETTINGS_LOCAL_STATE="❌ tracked"

cat <<EOF
─── SESSION CONTEXT ────────────────────────────────────────
Branch:        $BRANCH
Last commit:   $LAST_COMMIT
Changed files: $CHANGED_FILES
────────────────────────────────────────────────────────────
Governance:
  AGENTS.md (SSOT):     $AGENT_CATALOG
  subagent-protocol:    $SUBAGENT_PROTO
  Scopes available:     $SCOPES_COUNT
  settings.local.json:  $SETTINGS_LOCAL_STATE
────────────────────────────────────────────────────────────
Active rules:  AGENTS.md Non-Negotiable Rules and Runtime Entrypoints
Docs 3 Rules:  HALT conditions in docs/00.agent-governance/rules/documentation-protocol.md
Lint:          .pre-commit-config.yaml (CI gate; local reproduction optional)
─────────────────────────────────────────────────────────────
EOF
