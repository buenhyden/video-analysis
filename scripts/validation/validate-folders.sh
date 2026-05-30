#!/usr/bin/env bash
# validate-folders.sh
# Enforces the strict 8-folder compact limit under docs/ as per governance.

set -euo pipefail

ALLOWED_FOLDERS=(
  "00.agent-governance"
  "01.requirements"
  "02.architecture"
  "03.specs"
  "04.execution"
  "05.operations"
  "90.references"
  "99.templates"
)

echo "=== Documentation Folder Structure Validation ==="

VIOLATIONS=0
for folder in docs/*/; do
  folder_name=$(basename "$folder")

  # Skip non-directories (just in case)
  [[ ! -d "$folder" ]] && continue

  # Check if folder is in allowed list
  FOUND=0
  for allowed in "${ALLOWED_FOLDERS[@]}"; do
    if [[ "$folder_name" == "$allowed" ]]; then
      FOUND=1
      break
    fi
  done

  if [[ $FOUND -eq 0 ]]; then
    if git ls-files -- "$folder" | grep -q .; then
      echo "❌ Violation: Illegal tracked folder found under 'docs/': $folder_name"
      VIOLATIONS=$((VIOLATIONS + 1))
    elif find "$folder" -mindepth 1 -print -quit | grep -q .; then
      echo "❌ Violation: Illegal non-empty local folder found under 'docs/': $folder_name"
      VIOLATIONS=$((VIOLATIONS + 1))
    else
      echo "⚠️  Local Warning: Empty untracked legacy folder '$folder_name' exists. Remove it when the filesystem allows."
    fi
  fi
done

if [[ $VIOLATIONS -gt 0 ]]; then
  echo ""
  echo "❌ Failed: $VIOLATIONS illegal folders detected."
  echo "   Refer to AGENTS.md for the allowed 8-folder compact set."
  exit 1
else
  echo "✅ Success: All folders under 'docs/' comply with governance."
  exit 0
fi
