#!/usr/bin/env bash
# self-heal.sh
# Reports common workspace configuration issues without mutating repository files.

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)

echo "=== Workspace Heal Diagnostics ==="

has_active_stack_roots() {
  local root_name
  for root_name in web server app desktop monitoring tests; do
    if [[ -d "$REPO_ROOT/$root_name" ]]; then
      if git -C "$REPO_ROOT" ls-files -- "$root_name" | grep -q .; then
        return 0
      fi
      if find "$REPO_ROOT/$root_name" -type f -print -quit | grep -q .; then
        return 0
      fi
    fi
  done
  return 1
}

# 1. Environment Variable Diagnostics
echo "[ Heal 1 ] Checking .env state..."
if [[ ! -f "$REPO_ROOT/.env.example" ]]; then
  echo "  ⚠️ .env.example missing. Cannot compare local environment keys."
elif [[ ! -f "$REPO_ROOT/.env" ]]; then
  echo "  ⚠️ .env missing. Create it manually from .env.example if this project needs local secrets."
else
  MISSING_KEYS=$(comm -23 <(grep -v '^#' "$REPO_ROOT/.env.example" | cut -d= -f1 | sort) <(grep -v '^#' "$REPO_ROOT/.env" | cut -d= -f1 | sort))
  if [[ -n "$MISSING_KEYS" ]]; then
    echo "  ⚠️ Found missing keys in .env:"
    for key in $MISSING_KEYS; do
      echo "    - $key"
    done
    echo "  ℹ️ Add missing keys manually if this local environment requires them."
  else
    echo "  ✅ .env key set matches .env.example"
  fi
fi

# 2. Optional Stack Diagnostic
echo "[ Heal 2 ] Checking optional stack roots..."
if has_active_stack_roots; then
  echo "  ⚠️ Active application stack roots detected. Confirm they are intentional for this project."
else
  echo "  ✅ No active application stack roots; minimal governance template is clean."
fi

# 3. Tool Diagnostics
echo "[ Heal 3 ] Diagnosing governance tools..."
tools=("git")
for tool in "${tools[@]}"; do
  if ! command -v "$tool" &> /dev/null; then
    echo "  ⚠️ Missing tool: $tool"
  else
    echo "  ✅ Tool found: $tool ($(command -v "$tool"))"
  fi
done

echo ""
echo "✅ Heal diagnostics complete. No files were modified."
exit 0
