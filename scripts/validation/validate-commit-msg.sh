#!/usr/bin/env bash
# validate-commit-msg.sh
# Enforces strictly Conventional Commits: <type>(<scope>): <summary>
# Wired by .git/hooks/commit-msg.
# Policy: docs/00.agent-governance/rules/git-workflow.md §Procedure.2 (Commit).

set -u

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")
SUBJECT=$(printf '%s' "$COMMIT_MSG" | head -n1)

# Skip merge / fixup / revert auto-generated commits (git creates these).
if [[ "$SUBJECT" =~ ^(Merge\ |Revert\ \"|fixup!|squash!|amend!) ]]; then
  echo "✅ Commit message: OK (auto-generated commit, skipped)"
  exit 0
fi

# 1. Conventional Commits format check.
# Types: feat, fix, docs, refactor, style, perf, test, build, ci, chore, deps, revert
TYPE_PATTERN="^(feat|fix|docs|refactor|style|perf|test|build|ci|chore|deps|revert)(\([a-z0-9._/-]+\))?!?: .+"
if [[ ! "$SUBJECT" =~ $TYPE_PATTERN ]]; then
  echo -e "\n❌ INVALID COMMIT MESSAGE: \"$SUBJECT\""
  echo -e "--------------------------------------------------"
  echo -e "Pattern: <type>(<scope>): <summary>"
  echo -e "Allowed Types: feat, fix, docs, refactor, style, perf, test, build, ci, chore, deps, revert"
  echo -e "Example: feat(web): add login page"
  echo -e "Policy:  docs/00.agent-governance/rules/git-workflow.md"
  echo -e "--------------------------------------------------"
  exit 1
fi

# 2. Issue IDs are optional. Include one when it is known or available.

# 3. Subject line length (hard fail at 72 chars per policy Constraints).
if [[ ${#SUBJECT} -gt 72 ]]; then
  echo -e "\n❌ SUBJECT TOO LONG: ${#SUBJECT} chars (limit 72)"
  echo -e "  \"$SUBJECT\""
  echo -e "Policy: docs/00.agent-governance/rules/git-workflow.md §Constraints"
  exit 1
fi

echo "✅ Commit message: OK"
exit 0
