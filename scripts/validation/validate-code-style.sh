#!/usr/bin/env bash
# Validate code and document style without introducing a default app stack.

set -euo pipefail

echo "=== Code Style Validation ==="

ERROR=0

if ! git diff --check; then
  ERROR=1
fi

if command -v pre-commit >/dev/null 2>&1; then
  echo "Running pre-commit style checks..."
  STYLE_HOOKS=(
    end-of-file-fixer
    mixed-line-ending
    trailing-whitespace
    yamllint
    markdownlint-cli2
    shellcheck
    prettier
  )
  for hook in "${STYLE_HOOKS[@]}"; do
    pre-commit run "$hook" --all-files --show-diff-on-failure || ERROR=1
  done
else
  echo "⚠️ pre-commit not installed, skipping repository style hooks."
  echo "   CI still runs pre-commit through .github/workflows/ci-global.yml."
fi

if [[ "$ERROR" -ne 0 ]]; then
  echo "❌ Code style validation failed."
  exit 1
fi

echo "✅ Code style validation passed."
