#!/usr/bin/env bash
# validate-design-initialization.sh
# Verifies that DESIGN.md is initialized (version/name not <string>)
# if any frontend-related specs are detected.
# Usage: ./scripts/validation/validate-design-initialization.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"
FAILURES=0

echo "=== Design Initialization Validation ==="
echo "Repo: $REPO_ROOT"
echo ""

# 1. Check if DESIGN.md exists
if [[ ! -f "$REPO_ROOT/DESIGN.md" ]]; then
  echo "❌ FAIL: DESIGN.md missing from root"
  exit 2
fi

# 2. Skip validation if this is the Project-Template repository itself
if [[ "$(basename "$REPO_ROOT")" == "Project-Template" ]]; then
  echo "✅ Skipping DESIGN.md initialization check for Project-Template repository."
  exit 0
fi

# 3. Find specs that claim to have frontend design contracts
FRONTEND_SPECS=$(grep -rl "## Frontend Design Contract" "$REPO_ROOT/docs/03.specs" --include="*.md" || true)

if [[ -z "$FRONTEND_SPECS" ]]; then
  echo "✅ No frontend specs detected. Skipping DESIGN.md initialization check."
  exit 0
fi

echo "Detected frontend specs:"
while IFS= read -r spec; do
  echo "  - $spec"
done <<< "$FRONTEND_SPECS"
echo ""

# 3. Check DESIGN.md for placeholder values
DESIGN_CONTENT=$(cat "$REPO_ROOT/DESIGN.md")

# Simple check for YAML frontmatter placeholders (must be at start of line)
if echo "$DESIGN_CONTENT" | grep -Eq "^version:[[:space:]]+<string>"; then
  echo "❌ FAIL: DESIGN.md is NOT initialized (version is still <string>)"
  FAILURES=$((FAILURES + 1))
fi

if echo "$DESIGN_CONTENT" | grep -Eq "^name:[[:space:]]+<string>"; then
  echo "❌ FAIL: DESIGN.md is NOT initialized (name is still <string>)"
  FAILURES=$((FAILURES + 1))
fi

if [[ $FAILURES -gt 0 ]]; then
  echo ""
  echo "❌ Error: Frontend work detected but DESIGN.md is in placeholder state."
  echo "Please initialize DESIGN.md with actual project name and version."
  exit 2
else
  echo "✅ DESIGN.md is initialized or no frontend specs require it."
  exit 0
fi
