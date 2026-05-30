#!/usr/bin/env bash
# update-doc-readme-index.sh
# Auto-updates README.md index tables in docs/ directories.
# Preserves the required table shape from docs/00.agent-governance.
# Usage: ./scripts/docs/update-doc-readme-index.sh [docs-relative-dir]
# If docs-relative-dir is provided, updates only that directory. Otherwise updates top-level docs folders.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel 2>/dev/null || (cd "$SCRIPT_DIR/../.." && pwd))"
TARGET="${1:-}"

update_readme() {
  local stage_dir="$1"
  local readme="$stage_dir/README.md"

  if [[ ! -f "$readme" ]]; then
    return
  fi

  echo "  Updating: $stage_dir/README.md"

  python3 - "$stage_dir" "$readme" <<'EOF'
import re
import sys
from pathlib import Path

stage_dir = Path(sys.argv[1])
readme = Path(sys.argv[2])
INDEXED_SUFFIXES = {".md", ".yaml", ".yml", ".graphql", ".proto"}
PLACEHOLDER_VALUES = {"", "<string>", "YYYY-MM-DD"}
OWNERSHIP_LABELS = {
    "project-seed",
    "template-maintenance",
    "example",
    "archive/reference",
    "remove-candidate",
    "active-template-contract",
}
MACHINE_READABLE_TEMPLATE_SUMMARIES = {
    "openapi.template.yaml": "OpenAPI contract template for feature specs",
    "schema.template.graphql": "GraphQL schema contract template",
    "service.template.proto": "gRPC/Protocol Buffers service contract template",
}

def is_template_path(path: Path) -> bool:
    return "docs/99.templates" in path.as_posix()

def clean_meta_value(value, fallback="-"):
    if value is None:
        return fallback
    value = str(value).strip()
    if value in PLACEHOLDER_VALUES:
        return fallback
    return value

def first_h1(content: str, fallback: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            if title and title not in PLACEHOLDER_VALUES:
                return title
    return fallback

def first_purpose_sentence(content: str):
    match = re.search(r"^## Purpose\n(?P<body>.*?)(?=^## |\Z)", content, re.M | re.S)
    if not match:
        return None
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("<!--", "---")):
            continue
        line = re.sub(r"\s+", " ", line)
        sentence = re.split(r"(?<=[.!?])\s+", line, maxsplit=1)[0].strip()
        if sentence and sentence not in PLACEHOLDER_VALUES:
            return sentence
    return None

def parse_frontmatter(path: Path):
    if path.is_dir():
        candidate = path / "spec.md"
        if not candidate.exists():
            candidate = path / "README.md"
        if not candidate.exists():
            return {"title": path.name, "status": "active", "last-updated": "-"}
        path = candidate

    content = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)

    meta = {"title": path.name, "status": "active", "last-updated": "-"}

    # Simple regex parser for YAML frontmatter
    if match:
        fm_text = match.group(1)
        for line in fm_text.splitlines():
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    key, val = parts
                    meta[key.strip()] = val.strip().strip('"').strip("'")
    else:
        # Fallback to H1 search
        meta["title"] = first_h1(content, path.name)

    if is_template_path(path):
        fallback_title = first_h1(content, path.name)
        title = clean_meta_value(meta.get("title"), fallback_title)
        if path.name in MACHINE_READABLE_TEMPLATE_SUMMARIES:
            meta["title"] = MACHINE_READABLE_TEMPLATE_SUMMARIES[path.name]
        else:
            meta["title"] = first_purpose_sentence(content) or title
        meta["status"] = clean_meta_value(meta.get("status"), "active")
        meta["last-updated"] = clean_meta_value(meta.get("last-updated"), "-")
    else:
        meta["title"] = clean_meta_value(meta.get("title"), path.name)
        meta["status"] = clean_meta_value(meta.get("status"), "active")
        meta["last-updated"] = clean_meta_value(meta.get("last-updated"), "-")
    return meta

def doc_type(path: Path) -> str:
    if path.is_dir():
        return "package"
    suffix = path.suffix.lower().lstrip(".")
    return suffix or "file"

def normalize_link_target(value: str) -> str:
    value = value.strip()
    match = re.search(r"\[[^\]]+\]\(([^)]+)\)", value)
    if match:
        value = match.group(1)
    value = value.split("#", 1)[0].strip()
    if " " in value:
        value = value.split(" ", 1)[0].strip()
    return value

def existing_ownership_rows(content: str):
    match = re.search(r"^## Documents\n\n(?P<table>.*?)(?=\n## |\Z)", content, re.M | re.S)
    if not match:
        return {}

    rows = {}
    for line in match.group("table").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or stripped.startswith("| ---") or stripped.startswith("| File "):
            continue
        cols = [col.strip() for col in stripped.strip("|").split("|")]
        if len(cols) < 5:
            continue
        status = cols[3]
        if status not in OWNERSHIP_LABELS:
            continue
        target = normalize_link_target(cols[0])
        if target:
            rows[target] = {"summary": cols[2], "status": status}
    return rows

content = readme.read_text(encoding="utf-8")
preserved_ownership = existing_ownership_rows(content)

items = []
for child in sorted(stage_dir.iterdir(), key=lambda p: p.name):
    if child.name == "README.md" or child.name.startswith("."):
        continue
    if child.is_dir():
        if not any(child.iterdir()):
            continue
        link = f"./{child.name}/"
    elif child.suffix in INDEXED_SUFFIXES:
        link = f"./{child.name}"
    else:
        continue

    meta = parse_frontmatter(child)
    preserved = preserved_ownership.get(link)
    if preserved:
        meta["title"] = preserved["summary"]
        meta["status"] = preserved["status"]
    items.append((link, doc_type(child), meta.get("title", child.name), meta.get("status", "active"), meta.get("last-updated", "-")))

if not items:
    rows = ["| _No documents yet_ | — | This stage has been reset for new project use. | — | — |"]
else:
    rows = [
        f"| [{Path(link).name.rstrip('/')}]({link}) | {kind} | {summary} | {status} | {updated} |"
        for link, kind, summary, status, updated in items
    ]

table = "\n".join([
    "| File | Type | Summary | Status | Last Modified |",
    "| --- | --- | --- | --- | --- |",
    *rows,
])

section = "## Documents\n\n" + table + "\n"

if re.search(r"^## Documents\n", content, flags=re.M):
    content = re.sub(r"^## Documents\n.*?(?=\n## |\Z)", section, content, flags=re.M | re.S)
else:
    content = content.rstrip() + "\n\n" + section + "\n"

readme.write_text(content.rstrip() + "\n", encoding="utf-8")
EOF
}

if [[ -n "$TARGET" ]]; then
  if [[ -d "$REPO_ROOT/docs/$TARGET" ]]; then
    update_readme "$REPO_ROOT/docs/$TARGET"
  else
    echo "ERROR: docs/$TARGET not found"
    echo "Usage: $0 [docs-relative-dir]"
    exit 1
  fi
else
  echo "=== Updating README indexes ==="
  for stage_dir in "$REPO_ROOT"/docs/*/; do
    update_readme "$stage_dir"
  done
  echo "✅ Done."
fi
