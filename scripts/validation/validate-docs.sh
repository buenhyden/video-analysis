#!/usr/bin/env bash
set -e

echo "Running Docs Validation..."

ERROR=0
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
REPO_BASENAME="$(basename "$REPO_ROOT")"

echo "Checking template readiness invariants..."
python3 scripts/validation/validate-doc-readiness.py || ERROR=1

# Validate Template Frontmatter
echo "Checking docs/99.templates/ for required frontmatter..."
for file in docs/99.templates/*.md docs/99.templates/expanded/*.md; do
  if [ -f "$file" ]; then
    # Skip if it's the README itself
    if [[ "$file" == "docs/99.templates/README.md" ]]; then
      continue
    fi

    MISSING=""
    grep -q "title:" "$file" || MISSING="$MISSING title"
    grep -q "version:" "$file" || MISSING="$MISSING version"
    grep -q "owner:" "$file" || MISSING="$MISSING owner"
    grep -q "layer:" "$file" || MISSING="$MISSING layer"
    grep -q "stage:" "$file" || MISSING="$MISSING stage"
    grep -q "status:" "$file" || MISSING="$MISSING status"
    grep -q "last-updated:" "$file" || MISSING="$MISSING last-updated"

    if [ -n "$MISSING" ]; then
      echo "❌ $file is missing frontmatter fields:$MISSING"
      ERROR=1
    fi
  fi
done

if [ $ERROR -eq 0 ]; then
  echo "✅ All templates have required frontmatter."
fi

# Validate Folder READMEs for Lifecycle Rules
echo "Checking docs folder READMEs for lifecycle rules..."
for dir in docs/0[1-5]*/ docs/90*/; do
  readme="${dir}README.md"
  if [ -f "$readme" ]; then
    if ! grep -qi "## Lifecycle Rules" "$readme"; then
      echo "❌ $readme is missing '## Lifecycle Rules' section."
      ERROR=1
    fi
  fi
done

# Validate Agent Instructions 4-part structure
echo "Checking agent instructions for 4-part structure..."
for file in .claude/agents/*.md docs/00.agent-governance/rules/*.md; do
  if [ -f "$file" ]; then
    MISSING=""
    grep -qi "^## Role definition" "$file" || MISSING="$MISSING 'Role definition'"
    grep -qi "^## Procedure" "$file" || MISSING="$MISSING 'Procedure'"
    grep -qi "^## Constraints" "$file" || MISSING="$MISSING 'Constraints'"
    grep -qi "^## File references" "$file" || MISSING="$MISSING 'File references'"

    if [ -n "$MISSING" ]; then
      echo "❌ $file is missing required sections:$MISSING"
      ERROR=1
    fi
  fi
done

# Validate DESIGN.md placeholders
echo "Checking DESIGN.md for initialization placeholders..."
if [ -f "$REPO_ROOT/DESIGN.md" ]; then
  if [ "$REPO_BASENAME" = "Project-Template" ]; then
    if ! grep -q "version: <string>" "$REPO_ROOT/DESIGN.md" || ! grep -q "name: <string>" "$REPO_ROOT/DESIGN.md"; then
      echo "❌ DESIGN.md does not contain required placeholders for 'version' and 'name'. It might have been initialized prematurely."
      ERROR=1
    fi
  else
    if grep -q "version: <string>" "$REPO_ROOT/DESIGN.md" || grep -q "name: <string>" "$REPO_ROOT/DESIGN.md"; then
      echo "❌ DESIGN.md still contains base-template placeholders in derived repository '$REPO_BASENAME'."
      ERROR=1
    else
      echo "✅ DESIGN.md is initialized for derived repository '$REPO_BASENAME'."
    fi
  fi
fi

# Validate Formatting and Linting
echo "Running format and linting checks..."

if command -v markdownlint-cli2 >/dev/null 2>&1; then
  echo "Running markdownlint..."
  markdownlint-cli2 "**/*.md" "#node_modules" || ERROR=1
else
  echo "⚠️ markdownlint-cli2 not installed, skipping markdown linting."
fi

if command -v yamllint >/dev/null 2>&1; then
  echo "Running yamllint..."
  yamllint . || ERROR=1
else
  echo "⚠️ yamllint not installed, skipping YAML linting."
fi

if command -v shellcheck >/dev/null 2>&1; then
  echo "Running shellcheck..."
  find scripts/ -type f -name "*.sh" -exec shellcheck {} + || ERROR=1
else
  echo "⚠️ shellcheck not installed, skipping bash script linting."
fi

if [ $ERROR -ne 0 ]; then
  echo "Validation failed."
  exit 1
fi

echo "Validation passed."
exit 0
