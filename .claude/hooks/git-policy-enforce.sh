#!/usr/bin/env bash
# Git Policy Enforcement Hook
# Called before Bash tool execution.
# Exit 1 to BLOCK the tool call; exit 0 to ALLOW.

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null || pwd)}"
COMMAND="${CLAUDE_TOOL_INPUT_COMMAND:-}"

[[ -z "$COMMAND" ]] && exit 0

COMPACT_COMMAND="$(printf '%s' "$COMMAND" | tr '\n' ' ' | sed -E 's/[[:space:]]+/ /g')"

block() {
  local title="$1"
  local detail="$2"
  echo "❌ PRE-TOOL BLOCK: $title" >&2
  echo "   $detail" >&2
  exit 1
}

# Enforce PR template usage for GitHub PR creation.
if echo "$COMPACT_COMMAND" | grep -qE '(^|[;&|[:space:]])gh[[:space:]]+pr[[:space:]]+create([[:space:]]|$)'; then
  if ! echo "$COMPACT_COMMAND" | grep -qE 'PULL_REQUEST_TEMPLATE'; then
    echo "❌ PRE-TOOL BLOCK: gh pr create requires .github/PULL_REQUEST_TEMPLATE.md as the PR body." >&2
    echo "   Policy: docs/00.agent-governance/rules/git-workflow.md §3 PR Template." >&2
    echo "" >&2
    echo "   Use this starting point:" >&2
    echo "   gh pr create --base dev \\" >&2
    echo '     --title "<type>(<scope>): <summary>" \' >&2
    echo '     --body "$(cat .github/PULL_REQUEST_TEMPLATE.md)"' >&2
    echo "" >&2
    echo "   Then fill every section of the template before submitting." >&2
    exit 1
  fi
fi

# Do not allow bypassing local hooks for commits.
if echo "$COMPACT_COMMAND" | grep -qE '(^|[;&|[:space:]])git[[:space:]]+commit([^;&|]*[[:space:]])--no-verify([[:space:]]|$)'; then
  block "git commit --no-verify is prohibited." \
    "Run the relevant hooks and validators instead of bypassing repository policy."
fi

# Destructive working-tree operations require explicit human approval outside the hook.
if echo "$COMPACT_COMMAND" | grep -qE '(^|[;&|[:space:]])git[[:space:]]+reset([^;&|]*[[:space:]])--hard([[:space:]]|$)'; then
  block "git reset --hard is prohibited through agent tooling." \
    "Inspect the diff and request explicit human approval before destructive cleanup."
fi

if echo "$COMPACT_COMMAND" | grep -qE '(^|[;&|[:space:]])git[[:space:]]+clean([[:space:]]|$)'; then
  block "git clean is prohibited through agent tooling." \
    "Untracked files may contain user work; classify them before deletion."
fi

# Git-flow protected branch safeguards.
if echo "$COMPACT_COMMAND" | grep -qE '(^|[;&|[:space:]])git[[:space:]]+push([[:space:]]|$)'; then
  if echo "$COMPACT_COMMAND" | grep -qE '(^|[[:space:]])(-f|--force|--force-with-lease)([[:space:]]|$)|[[:space:]]\+[^[:space:]]+'; then
    block "Force push is prohibited by workspace Git policy." \
      "Use reviewed PR flow and protected branch rules; do not force-push through agent tooling."
  fi

  if echo "$COMPACT_COMMAND" | grep -qE 'git[[:space:]]+push[^;&|]*(^|[[:space:]])(--delete|-d)[[:space:]]+[^[:space:]]+[[:space:]]+(main|dev)([[:space:]]|$)'; then
    block "Deleting protected branch main/dev is prohibited." \
      "Protected branches must be changed only through reviewed PR governance."
  fi

  if echo "$COMPACT_COMMAND" | grep -qE 'git[[:space:]]+push[^;&|]*[[:space:]](origin|upstream)?[[:space:]]*(main|dev)([[:space:]]|$)'; then
    block "Direct push to protected branch main/dev is prohibited." \
      "Create a feature/docs/fix branch from dev and open a reviewed PR instead."
  fi

  if echo "$COMPACT_COMMAND" | grep -qE 'git[[:space:]]+push[^;&|]*(HEAD|refs/heads/[^[:space:]]+):(refs/heads/)?(main|dev)([[:space:]]|$)'; then
    block "Direct refspec push to protected branch main/dev is prohibited." \
      "Protected branches must receive changes through reviewed PRs only."
  fi

  CURRENT_BRANCH="$(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null || true)"
  if [[ "$CURRENT_BRANCH" =~ ^(main|dev)$ ]] \
    && echo "$COMPACT_COMMAND" | grep -qE '(^|[;&|[:space:]])git[[:space:]]+push([[:space:]]+(origin|upstream))?[[:space:]]*($|[;&|])'; then
    block "Implicit git push from protected branch '$CURRENT_BRANCH' is prohibited." \
      "Push a feature/docs/fix branch and open a reviewed PR instead."
  fi
fi

exit 0
