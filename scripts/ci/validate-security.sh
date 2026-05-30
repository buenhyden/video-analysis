#!/usr/bin/env bash
# validate-security.sh
# Local security gate for Project-Template.
# Fails on enforced security findings. Optional tool skips are reported as warnings/N/A.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"
FAILURES=0
WEB_MANIFEST="$REPO_ROOT/web/package.json"
SERVER_REQUIREMENTS="$REPO_ROOT/server/requirements.txt"
SERVER_PYPROJECT="$REPO_ROOT/server/pyproject.toml"
SECRET_SCAN_RESULTS="$(mktemp)"
CHANGED_SECRET_SCAN_RESULTS="$(mktemp)"

trap 'rm -f "$SECRET_SCAN_RESULTS" "$CHANGED_SECRET_SCAN_RESULTS"' EXIT

summarize_secret_matches() {
  local result_file="$1"
  local match_count

  match_count="$(wc -l < "$result_file" | tr -d ' ')"
  echo "  Match count: $match_count"
  awk -F: -v root="$REPO_ROOT/" '{ sub("^" root, "", $1); print "    - " $1 ":" $2 }' "$result_file" | head -n 5
}

echo -e "\n=== Security Validation ==="

# 0. Dependency Lock-file Check
echo "[ Check 0 ] Dependency Lock-files..."
MISSING_LOCKS=0
if [ -f "$WEB_MANIFEST" ] && [ ! -f "$REPO_ROOT/web/package-lock.json" ]; then
  echo "  ❌ FAIL: web/package-lock.json missing for active web/package.json."
  MISSING_LOCKS=$((MISSING_LOCKS + 1))
fi
if [ -d "$REPO_ROOT/server" ] \
  && [ ! -f "$SERVER_REQUIREMENTS" ] \
  && [ ! -f "$SERVER_PYPROJECT" ] \
  && find "$REPO_ROOT/server" -type f -name "*.py" -print -quit | grep -q .; then
  echo "  ❌ FAIL: server Python source exists without requirements.txt or pyproject.toml."
  MISSING_LOCKS=$((MISSING_LOCKS + 1))
fi

if [ $MISSING_LOCKS -eq 0 ]; then
  echo "  ✅ Lock-file policy: OK or not required for minimal template"
else
  FAILURES=$((FAILURES + MISSING_LOCKS))
fi

# 1. Secret Scanning (Focused on source directories)
echo "[ Check 1 ] Secret Scanning..."
# Match likely secret assignments instead of raw keywords. Policy validators need
# to mention names like GITHUB_TOKEN, so keyword-only scanning creates false positives.
SECRET_PATTERNS=(
  '(^|[^A-Za-z0-9_])AWS_SECRET_ACCESS_KEY[[:space:]]*[:=][[:space:]]*['\''"]?[A-Za-z0-9/+=_.-]{12,}'
  '(^|[^A-Za-z0-9_])[A-Za-z0-9_]*(SECRET_KEY|PASSWORD|API_KEY|TOKEN|GH_TOKEN|GITHUB_TOKEN)[[:space:]]*[:=][[:space:]]*['\''"]?[A-Za-z0-9/+=_.-]{12,}'
)
# Focus scan on active automation paths to avoid optional examples and docs false positives.
SCAN_DIRS=("scripts" ".github")

for dir in "${SCAN_DIRS[@]}"; do
  if [ -d "$REPO_ROOT/$dir" ]; then
    for pattern in "${SECRET_PATTERNS[@]}"; do
      if grep -rEIn "$pattern" "$REPO_ROOT/$dir" \
        --exclude-dir=".git" \
        --exclude-dir=".next" \
        --exclude-dir=".venv" \
        --exclude-dir="build" \
        --exclude-dir="coverage" \
        --exclude-dir="dist" \
        --exclude-dir="node_modules" \
        --exclude="*.template.md" \
        --exclude="package-lock.json" \
        --exclude="package.json" \
        --exclude="validate-security.sh" \
        --exclude="*.example" \
        | grep -v "REPLACE_ME" \
        | grep -v "EXAMPLE" \
        | grep -v "sample" \
        | grep -vE "secrets\.[A-Z0-9_]+|\$\{\{[[:space:]]*secrets\." \
        | grep -v "pragma: allowlist secret" > "$SECRET_SCAN_RESULTS"; then
        echo "  ❌ FAIL: Potential hardcoded secret assignment found in '$dir/'."
        summarize_secret_matches "$SECRET_SCAN_RESULTS"
        FAILURES=$((FAILURES + 1))
      fi
    done
  fi
done

echo "[ Check 1b ] Changed governance/runtime secret scan..."
mapfile -t CHANGED_FILES < <(
  {
    git -C "$REPO_ROOT" diff --name-only --diff-filter=ACMRT HEAD -- 2>/dev/null || true
    git -C "$REPO_ROOT" diff --cached --name-only --diff-filter=ACMRT -- 2>/dev/null || true
    git -C "$REPO_ROOT" ls-files --others --exclude-standard 2>/dev/null || true
  } | sort -u
)

CHANGED_SCANNED=0
for rel in "${CHANGED_FILES[@]}"; do
  [ -n "$rel" ] || continue
  [ "$rel" != "scripts/ci/validate-security.sh" ] || continue
  case "$rel" in
    AGENTS.md|CLAUDE.md|GEMINI.md|README.md|scripts/*|.github/*|.claude/*|.codex/*|docs/*) ;;
    *) continue ;;
  esac
  case "$rel" in
    *.md|*.toml|*.json|*.yaml|*.yml|*.sh|*.py|*.mjs) ;;
    *) continue ;;
  esac
  file_path="$REPO_ROOT/$rel"
  [ -f "$file_path" ] || continue
  CHANGED_SCANNED=$((CHANGED_SCANNED + 1))
  for pattern in "${SECRET_PATTERNS[@]}"; do
    if grep -EIn "$pattern" "$file_path" \
      | grep -v "REPLACE_ME" \
      | grep -v "EXAMPLE" \
      | grep -v "sample" \
      | grep -vE "secrets\.[A-Z0-9_]+|\$\{\{[[:space:]]*secrets\." \
      | grep -v "pragma: allowlist secret" > "$CHANGED_SECRET_SCAN_RESULTS"; then
      echo "  ❌ FAIL: Potential hardcoded secret assignment found in changed file '$rel'."
      summarize_secret_matches "$CHANGED_SECRET_SCAN_RESULTS"
      FAILURES=$((FAILURES + 1))
    fi
  done
done

if [ "$CHANGED_SCANNED" -eq 0 ]; then
  echo "  ✅ Changed-file secret scan: not required; no matching changed governance/runtime files."
else
  echo "  ✅ Changed-file secret scan: checked $CHANGED_SCANNED file(s)."
fi

if [ $FAILURES -eq 0 ]; then
  echo "  ✅ Secret scanning: OK"
fi

# 2. SAST (Python/Bandit)
echo "[ Check 2 ] SAST: Python (Bandit)..."
if [ ! -d "$REPO_ROOT/server" ] || ! find "$REPO_ROOT/server" -type f -name "*.py" -print -quit | grep -q .; then
  echo "  ✅ Python SAST: not required; no active server Python source."
elif command -v bandit >/dev/null 2>&1; then
  if ! bandit -r "$REPO_ROOT/server" -ll -ii > /tmp/bandit_out.txt 2>&1; then
    echo "  ❌ FAIL: Bandit found security issues in 'server/'."
    cat /tmp/bandit_out.txt
    FAILURES=$((FAILURES + 1))
  else
    echo "  ✅ Bandit: OK"
  fi
else
  echo "  ⚠️ WARNING: Bandit not installed, skipping Python SAST."
fi

# 3. SAST (JavaScript)
echo "[ Check 3 ] SAST: JavaScript..."
if [ ! -f "$WEB_MANIFEST" ]; then
  echo "  ✅ JS SAST: not required; no active web/package.json."
elif command -v npm >/dev/null 2>&1 && [ -d "$REPO_ROOT/web/node_modules" ]; then
  cd "$REPO_ROOT/web" || exit 1
  if ! npm run lint > /tmp/eslint_out.txt 2>&1; then
    echo "  ❌ FAIL: ESLint found issues in 'web/'."
    cat /tmp/eslint_out.txt
    FAILURES=$((FAILURES + 1))
  else
    echo "  ✅ ESLint: OK"
  fi
  cd "$REPO_ROOT" || exit 1
else
  echo "  ⚠️ WARNING: npm/node_modules not found in 'web/', skipping JS SAST."
fi

# Final Result
if [ "$FAILURES" -gt 0 ]; then
  echo -e "\n❌ Security validation FAILED with $FAILURES failure(s)."
  exit 1
else
  echo -e "\n✅ Security validation PASSED for enforced local checks."
  exit 0
fi
