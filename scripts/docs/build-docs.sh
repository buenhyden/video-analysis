#!/usr/bin/env bash
# build-docs.sh
# Builds or serves the MkDocs documentation site.

set -euo pipefail

COMMAND="${1:-build}"

if [[ ! -f "mkdocs.yml" && ! -f "mkdocs.yaml" ]]; then
  echo "Docs site not configured: no mkdocs.yml or mkdocs.yaml found."
  echo "Stage documentation remains available under docs/."
  exit 0
fi

if ! command -v mkdocs &> /dev/null; then
  echo "Docs site configured, but mkdocs is not installed."
  echo "Install mkdocs-material to build or serve the site."
  exit 0
fi

case "$COMMAND" in
  serve)
    echo "🚀 Serving documentation on http://localhost:8000..."
    mkdocs serve
    ;;
  build)
    echo "🔨 Building documentation site..."
    mkdocs build
    echo "✅ Documentation built in site/ directory."
    ;;
  *)
    echo "Usage: $0 {build|serve}"
    exit 1
    ;;
esac
