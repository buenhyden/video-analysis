#!/usr/bin/env bash
# validate-architecture.sh
# Verifies architectural constraints without mutating generated graph artifacts.

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)

echo "=== Architecture Validation ==="

# 1. Optional Graphify posture
if command -v graphify >/dev/null 2>&1; then
  echo "Graphify available: optional local graph refresh can be run manually."
else
  echo "Graphify not found: optional graph validation skipped."
fi

# 2. Constraint Check: Layer Boundaries
echo "Verifying layer boundaries..."
FAILURES=0

# Check: Web should not directly import from Server
if [[ -d "$REPO_ROOT/web" ]] && grep -R "from '../../server" "$REPO_ROOT/web" \
  --include="*.ts" \
  --include="*.tsx" \
  --exclude-dir=node_modules \
  --exclude-dir=.next \
  --exclude-dir=dist \
  --exclude-dir=build \
  --exclude-dir=coverage \
  >/dev/null 2>&1; then
  echo "  ❌ FAIL: Illegal direct import from 'server' found in 'web/'. Use API calls instead."
  FAILURES=$((FAILURES + 1))
fi

# Check: Server should not directly import from Web
if [[ -d "$REPO_ROOT/server" ]] && grep -r "import .* from .*web" "$REPO_ROOT/server" --include="*.py" >/dev/null 2>&1; then
  echo "  ❌ FAIL: Illegal direct import from 'web' found in 'server/'."
  FAILURES=$((FAILURES + 1))
fi

if [[ ! -d "$REPO_ROOT/web" && ! -d "$REPO_ROOT/server" ]]; then
  echo "  ✅ No active application stack roots; layer-boundary checks are not required."
fi

# 3. Constraint Check: Folder READMEs
echo "Verifying README integrity..."
STAGES=("01.requirements" "02.architecture/requirements" "02.architecture/decisions" "03.specs" "04.execution/plans" "04.execution/tasks" "05.operations/guides" "05.operations/policies" "05.operations/runbooks" "05.operations/incidents")
for stage in "${STAGES[@]}"; do
  if [[ ! -f "$REPO_ROOT/docs/$stage/README.md" ]]; then
    echo "  ❌ FAIL: Missing README in docs/$stage"
    FAILURES=$((FAILURES + 1))
  fi
done

if [[ $FAILURES -eq 0 ]]; then
  echo -e "\n✅ Architecture: OK"
else
  echo -e "\n❌ Architecture: $FAILURES failures found."
  exit 1
fi
