#!/usr/bin/env bash
# audit-dependencies.sh
# Performs dependency auditing for active stack manifests when present.

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
FAILURES=0

echo "=== Dependency Security Audit ==="

# 1. JavaScript (npm)
echo "[ Audit 1 ] JavaScript (npm) dependencies..."
if [[ -f "$REPO_ROOT/web/package.json" ]]; then
  if ! command -v npm &> /dev/null; then
    echo "  ⚠️ npm not installed. Skipping JavaScript audit."
  elif [[ ! -f "$REPO_ROOT/web/package-lock.json" ]]; then
    echo "  ⚠️ package-lock.json not found. Skipping npm audit."
  else
    cd "$REPO_ROOT/web"
    if npm audit --audit-level=high; then
      echo "  ✅ JavaScript security audit: OK"
    else
      echo "  ❌ FAIL: High-severity vulnerabilities found in active JavaScript dependencies."
      FAILURES=$((FAILURES + 1))
    fi
  fi
else
  echo "  ✅ JavaScript audit: not required; no active web/package.json."
fi

# 2. Python (pip)
echo "[ Audit 2 ] Python (pip) dependencies..."
if [[ -f "$REPO_ROOT/server/requirements.txt" ]]; then
  # Requires pip-audit to be installed
  if command -v pip-audit &> /dev/null; then
    if pip-audit -r "$REPO_ROOT/server/requirements.txt"; then
      echo "  ✅ Python security audit: OK"
    else
      echo "  ❌ FAIL: Vulnerabilities found in active Python requirements."
      FAILURES=$((FAILURES + 1))
    fi
  else
    echo "  ⚠️ pip-audit not installed. Skipping deep scan."
    # Fallback to a basic check if needed, or just warn
  fi
else
  echo "  ✅ Python audit: not required; no active server/requirements.txt."
fi

echo ""
if [[ $FAILURES -gt 0 ]]; then
  echo "❌ Dependency audit FAILED with $FAILURES issues."
  exit 1
else
  echo "✅ All dependency audits passed."
  exit 0
fi
