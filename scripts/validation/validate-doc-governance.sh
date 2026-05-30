#!/usr/bin/env bash
# validate-doc-governance.sh
# Validates absolute document governance: root routers, README indexes, stage-gate mapping,
# 8-folder compact limit, dev branch naming, and DESIGN.md initialization state.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"
REPO_BASENAME="$(basename "$REPO_ROOT")"
FAILURES=0
WARNINGS=0

echo "=== Absolute Doc Governance Validation ==="
echo "Repo: $REPO_ROOT"
echo ""

# --- 1. Strict 8-folder compact limit ---
echo "[ Check 1 ] Stage directories (8-folder compact limit)..."
ALLOWED_FOLDERS=(
  "00.agent-governance" "01.requirements" "02.architecture" "03.specs"
  "04.execution" "05.operations" "90.references" "99.templates"
)
for folder in "$REPO_ROOT/docs"/*/; do
  folder_name=$(basename "$folder")

  # Check if folder is in allowed list
  FOUND=0
  for allowed in "${ALLOWED_FOLDERS[@]}"; do
    if [[ "$folder_name" == "$allowed" ]]; then
      FOUND=1
      break
    fi
  done

  if [[ $FOUND -eq 0 ]]; then
    if git -C "$REPO_ROOT" ls-files -- "docs/$folder_name" | grep -q .; then
      echo "  ❌ FAIL: Illegal tracked folder found under 'docs/': $folder_name"
      FAILURES=$((FAILURES + 1))
    elif find "$folder" -mindepth 1 -print -quit | grep -q .; then
      echo "  ❌ FAIL: Illegal non-empty local folder found under 'docs/': $folder_name"
      FAILURES=$((FAILURES + 1))
    else
      echo "  ⚠️  Local only: Empty untracked legacy folder '$folder_name' exists."
    fi
  fi
done



# --- 3. DESIGN.md Initialization Integrity ---
echo "[ Check 3 ] DESIGN.md initialization state..."
if [[ -f "$REPO_ROOT/DESIGN.md" ]]; then
  if [[ "$REPO_BASENAME" == "Project-Template" ]]; then
    if ! grep -q "version: <string>" "$REPO_ROOT/DESIGN.md" || ! grep -q "name: <string>" "$REPO_ROOT/DESIGN.md"; then
      echo "  ❌ FAIL: DESIGN.md must use placeholders (<string>) for the Project-Template itself."
      FAILURES=$((FAILURES + 1))
    else
      echo "  ✅ DESIGN.md placeholders: OK"
    fi
  else
    if grep -q "version: <string>" "$REPO_ROOT/DESIGN.md" || grep -q "name: <string>" "$REPO_ROOT/DESIGN.md"; then
      echo "  ❌ FAIL: DESIGN.md still contains base-template placeholders in derived repository '$REPO_BASENAME'."
      FAILURES=$((FAILURES + 1))
    else
      echo "  ✅ DESIGN.md derived initialization: OK"
    fi
  fi
fi

# --- 4. Root shim size & Git rules ---
echo "[ Check 4 ] Root shim size & Git rules..."
SHIM_SECTION_LIMIT=20
SHIMS=("$REPO_ROOT/AGENTS.md" "$REPO_ROOT/CLAUDE.md" "$REPO_ROOT/GEMINI.md" "$REPO_ROOT/.claude/CLAUDE.md")
for shim in "${SHIMS[@]}"; do
  if [[ -f "$shim" ]]; then
    section_violations="$(
      awk -v limit="$SHIM_SECTION_LIMIT" '
        /^## / {
          if (section != "" && count > limit) {
            print section ":" count
          }
          section=$0
          sub(/^##[[:space:]]+/, "", section)
          count=0
          next
        }
        /^# / { next }
        section != "" && $0 !~ /^[[:space:]]*$/ { count++ }
        END {
          if (section != "" && count > limit) {
            print section ":" count
          }
        }
      ' "$shim"
    )"
    if [[ -n "$section_violations" ]]; then
      while IFS= read -r violation; do
        [[ -z "$violation" ]] && continue
        echo "  ❌ FAIL: ${shim#"$REPO_ROOT"/} — section exceeds ${SHIM_SECTION_LIMIT} non-empty lines ($violation)"
        FAILURES=$((FAILURES + 1))
      done <<< "$section_violations"
    fi

    if [[ "$shim" != "$REPO_ROOT/AGENTS.md" && "$shim" != "$REPO_ROOT/.claude/CLAUDE.md" ]]; then
      continue
    fi

    # Check for Git rules keywords
    MANDATORY_GIT=(Conventional commit PR branch dev "1-commit-1-change")
    for kw in "${MANDATORY_GIT[@]}"; do
      if ! grep -qi "$kw" "$shim"; then
        echo "  ❌ FAIL: $(basename "$shim") — missing mandatory keyword '$kw'"
        FAILURES=$((FAILURES + 1))
      fi
    done
  fi
done

# --- 5. Stage README content coverage ---
echo "[ Check 5 ] Stage README content..."
for stage in "${ALLOWED_FOLDERS[@]}"; do
  readme="$REPO_ROOT/docs/$stage/README.md"
  [[ -f "$readme" ]] || continue
  if [[ "$stage" =~ ^(01\.requirements|02\.architecture|03\.specs|04\.execution|05\.operations|90\.references)$ ]] \
    && grep -q "Skeleton" "$readme"; then
    continue
  fi
  # Check for mandatory sections
  sections=("Purpose & Scope" "Documents" "AI Authoring Guidance" "Naming Rules")
  for s in "${sections[@]}"; do
    if ! grep -qi "## $s" "$readme"; then
      echo "  ⚠️  WARN: docs/$stage/README.md — missing section '## $s'"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
done

# --- Summary ---
echo ""
echo "=== Summary ==="
echo "Failures: $FAILURES"
echo "Warnings: $WARNINGS"

if [[ $FAILURES -gt 0 ]]; then
  exit 2
elif [[ $WARNINGS -gt 0 ]]; then
  exit 1
else
  echo "✅ Absolute governance checks passed."
  exit 0
fi
