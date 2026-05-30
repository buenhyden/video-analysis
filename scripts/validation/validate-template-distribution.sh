#!/usr/bin/env bash
# validate-template-distribution.sh
# Ensures the main release-template surface has only skeleton README guides in project-content folders.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"

echo "=== Template Distribution Validation ==="

# Branch-aware mode: on non-main branches, forbidden-file checks warn only.
CURRENT_BRANCH=$(git -C "$REPO_ROOT" branch --show-current 2>/dev/null || echo "")
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "ℹ️  Branch: '$CURRENT_BRANCH' (not 'main'). Forbidden-file check runs in warn-only mode."
  echo "ℹ️  Skeleton README checks still enforced. Forbidden files will be listed but will not fail."
  echo ""
  WARN_ONLY=true
else
  WARN_ONLY=false
fi

ALLOWED_FILES=(
  "docs/01.requirements/README.md"
  "docs/02.architecture/README.md"
  "docs/02.architecture/requirements/README.md"
  "docs/02.architecture/decisions/README.md"
  "docs/03.specs/README.md"
  "docs/04.execution/README.md"
  "docs/04.execution/plans/README.md"
  "docs/04.execution/tasks/README.md"
  "docs/05.operations/README.md"
  "docs/05.operations/guides/README.md"
  "docs/05.operations/policies/README.md"
  "docs/05.operations/runbooks/README.md"
  "docs/05.operations/incidents/README.md"
  "docs/90.references/README.md"
)

REQUIRED_README_SECTIONS=(
  "## Overview"
  "## Audience"
  "## Scope"
  "### In Scope"
  "### Out of Scope"
  "## Structure"
  "## Mandatory Templates"
  "## Naming Rules"
  "## Lifecycle Rules"
  "## Cross-Reference Rules"
  "## Usage Examples"
  "## How to Work in This Area"
  "## AI Authoring Guidance"
  "## AI Execution Checklist"
  "## Documents"
  "## Related Documents"
)

is_allowed() {
  local rel="$1"
  for allowed in "${ALLOWED_FILES[@]}"; do
    [[ "$rel" == "$allowed" ]] && return 0
  done
  return 1
}

failures=0
for allowed in "${ALLOWED_FILES[@]}"; do
  readme_path="$REPO_ROOT/$allowed"
  if [[ ! -f "$readme_path" ]]; then
    echo "  ❌ Missing release skeleton README: $allowed"
    failures=$((failures + 1))
    continue
  fi

  for section in "${REQUIRED_README_SECTIONS[@]}"; do
    if ! grep -Fq -- "$section" "$readme_path"; then
      echo "  ❌ Release skeleton README missing section '$section': $allowed"
      failures=$((failures + 1))
    fi
  done

  if ! grep -Fq "docs/99.templates/readme.template.md" "$readme_path"; then
    echo "  ❌ Release skeleton README must cite docs/99.templates/readme.template.md: $allowed"
    failures=$((failures + 1))
  fi

  if ! grep -Eq "Project-Template|새 프로젝트|derived project|파생 프로젝트" "$readme_path"; then
    echo "  ❌ Release skeleton README must identify new-project template usage: $allowed"
    failures=$((failures + 1))
  fi
done

forbidden_count=0
while IFS= read -r -d '' file_path; do
  rel="${file_path#"$REPO_ROOT"/}"
  if ! is_allowed "$rel"; then
    if [[ "$WARN_ONLY" == "true" ]]; then
      echo "  ⚠️  Would be forbidden on main: $rel"
      forbidden_count=$((forbidden_count + 1))
    else
      echo "  ❌ Forbidden project-content document in release skeleton: $rel"
      failures=$((failures + 1))
    fi
  fi
done < <(
  find \
    "$REPO_ROOT/docs/01.requirements" \
    "$REPO_ROOT/docs/02.architecture" \
    "$REPO_ROOT/docs/03.specs" \
    "$REPO_ROOT/docs/04.execution" \
    "$REPO_ROOT/docs/05.operations" \
    "$REPO_ROOT/docs/90.references" \
    -type f -print0
)

if [[ "$WARN_ONLY" == "true" && $forbidden_count -gt 0 ]]; then
  echo ""
  echo "⚠️  $forbidden_count file(s) would be forbidden on 'main'. These are expected on '$CURRENT_BRANCH'."
fi

if [[ $failures -gt 0 ]]; then
  echo "❌ Template distribution validation failed."
  exit 1
fi

if [[ "$WARN_ONLY" == "true" ]]; then
  echo "✅ Skeleton README checks passed (warn-only mode; run on 'main' for full enforcement)."
else
  echo "✅ Release skeleton contains only allowed README guides."
fi
