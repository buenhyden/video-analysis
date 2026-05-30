#!/usr/bin/env bash
# validate-cross-links.sh
# Checks all markdown internal links ([text](path)) in docs/ resolve to real files.
# Usage: ./scripts/validation/validate-cross-links.sh
# Exit: 0=pass, 1=broken links found

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"
BROKEN=0

echo "=== Cross-Link Validation ==="

extract_markdown_links() {
  python3 - "$1" <<'PY'
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8", errors="ignore")
visible_lines = []
in_fence = False

for line in text.splitlines():
    if re.match(r"^[ \t]*```", line):
        in_fence = not in_fence
        continue
    if not in_fence:
        visible_lines.append(line)

visible_text = "\n".join(visible_lines)
for match in re.finditer(r"(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)", visible_text):
    target = match.group(1).strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    elif " " in target:
        target = target.split()[0]
    print(target)
PY
}

while IFS= read -r -d '' file; do
  # Extract markdown links: [text](target)
  while IFS= read -r link; do
    # Skip external URLs, anchors-only, and empty
    if [[ "$link" =~ ^https?:// ]] || [[ "$link" =~ ^# ]] || [[ -z "$link" ]]; then
      continue
    fi

    # Strip anchor fragment
    path_part="${link%%#*}"
    [[ -z "$path_part" ]] && continue

    # Resolve relative to file's directory
    file_dir="$(dirname "$file")"
    if [[ "$path_part" = /* ]]; then
      resolved="$REPO_ROOT$path_part"
    else
      resolved="$file_dir/$path_part"
    fi

    # Normalize path
    resolved="$(cd "$(dirname "$resolved")" 2>/dev/null && pwd)/$(basename "$resolved")" || true

    if [[ ! -f "$resolved" && ! -d "$resolved" ]]; then
      echo "  ❌ BROKEN: $file"
      echo "     → $link"
      BROKEN=$((BROKEN + 1))
    fi
  done < <(extract_markdown_links "$file")
done < <(find "$REPO_ROOT/docs" -name "*.md" \
  -not -path "*/99.templates/*" \
  -print0 2>/dev/null)

echo ""
echo "=== Template Checklist Coverage ==="
while IFS= read -r -d '' template_file; do
  template_rel="${template_file#"$REPO_ROOT"/}"
  if ! grep -q "Target:" "$template_file"; then
    echo "  ❌ MISSING: $template_rel — Target"
    BROKEN=$((BROKEN + 1))
  fi

  if ! grep -q "^## AI Execution Checklist" "$template_file"; then
    echo "  ❌ MISSING: $template_rel — AI Execution Checklist"
    BROKEN=$((BROKEN + 1))
    continue
  fi

  for marker in "Entry Gate" "Exit Gate" "Hard Stop" "Downstream Trigger" "Evidence Rule"; do
    if ! grep -q "$marker" "$template_file"; then
      echo "  ❌ MISSING: $template_rel — $marker"
      BROKEN=$((BROKEN + 1))
    fi
  done
done < <(find "$REPO_ROOT/docs/99.templates" -name "*.template.md" \
  -not -name "memory.template.md" \
  -not -name "progress.template.md" \
  -print0 2>/dev/null)

echo ""
if [[ $BROKEN -gt 0 ]]; then
  echo "❌ $BROKEN broken link(s) found."
  exit 1
else
  echo "✅ All internal links valid."
  exit 0
fi
