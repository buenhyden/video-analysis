#!/usr/bin/env bash
# ws.sh (Workspace CLI)
# Unified entry point for all Project-Template operations.

set -euo pipefail

COMMAND="${1:-help}"
REPO_ROOT=$(git rev-parse --show-toplevel)

show_help() {
  echo "Usage: ws <command> [args]"
  echo ""
  echo "Commands:"
  echo "  setup      - Report local prerequisite status without installing tools"
  echo "  validate   - Run all governance, script, security, and structure checks"
  echo "  validate-derived - Run post-bootstrap derived-project validation"
  echo "  validate-distribution - Verify the main release-template skeleton"
  echo "  audit      - Run dependency and container audits when stack manifests exist"
  echo "  heal       - Detect and report workspace configuration issues"
  echo "  info       - Show workspace health and status summary"
  echo "  docs       - Build or serve the documentation site (ws docs <build|serve>)"
  echo "  hook       - Run configured agent hook by event (ws hook <event> [matcher])"
  echo "  sbom       - Generate Software Bill of Materials (SBOM)"
  echo "  intelligence - Generate repository intelligence graph"
  echo "  dispatch   - Create a transient governed subagent dispatch packet"
  echo "  swarm      - Orchestrate a multi-agent swarm mission (ws swarm <task_id> <command>)"
  echo "  bootstrap  - Personalize the template for a new project"
  echo "  help       - Show this help message"
}

case "$COMMAND" in
  setup)
    bash "$REPO_ROOT/scripts/setup/setup-environment.sh"
    ;;
  heal)
    bash "$REPO_ROOT/scripts/harness/self-heal.sh"
    ;;
  validate)
    bash "$REPO_ROOT/scripts/validation/validate-docs.sh"
    bash "$REPO_ROOT/scripts/validation/validate-doc-governance.sh"
    bash "$REPO_ROOT/scripts/validation/validate-folders.sh"
    bash "$REPO_ROOT/scripts/validation/validate-cross-links.sh"
    python3 "$REPO_ROOT/scripts/validation/validate-path-portability.py"
    bash "$REPO_ROOT/scripts/validation/validate-code-style.sh"
    python3 "$REPO_ROOT/scripts/validation/validate-script-inventory.py"
    python3 "$REPO_ROOT/scripts/validation/validate-github-workflows.py"
    python3 "$REPO_ROOT/scripts/validation/validate-github-metadata.py"
    python3 "$REPO_ROOT/scripts/validation/validate-runtime-contracts.py"
    bash "$REPO_ROOT/scripts/validation/validate-skill-quality.sh"
    bash "$REPO_ROOT/scripts/qa/summarize-tdd-coverage.sh" --fail-on-missing
    bash "$REPO_ROOT/scripts/validation/validate-architecture.sh"
    python3 "$REPO_ROOT/scripts/validation/validate-version-drift.py"
    bash "$REPO_ROOT/scripts/validation/audit-dependencies.sh"
    bash "$REPO_ROOT/scripts/validation/validate-containers.sh"
    if [[ "${TEMPLATE_DISTRIBUTION:-0}" == "1" ]]; then
      bash "$REPO_ROOT/scripts/validation/validate-template-distribution.sh"
    fi
    ;;
  validate-derived)
    bash "$REPO_ROOT/scripts/ws.sh" validate
    python3 "$REPO_ROOT/scripts/validation/validate-github-metadata.py" --strict-derived
    if grep -Eq "^version:[[:space:]]+<string>|^name:[[:space:]]+<string>" "$REPO_ROOT/DESIGN.md"; then
      echo "❌ DESIGN.md still has uninitialized version/name placeholders."
      exit 1
    fi
    echo "✅ Derived-project validation passed."
    ;;
  validate-distribution)
    bash "$REPO_ROOT/scripts/validation/validate-template-distribution.sh"
    ;;
  audit)
    bash "$REPO_ROOT/scripts/validation/audit-dependencies.sh"
    bash "$REPO_ROOT/scripts/validation/validate-containers.sh"
    ;;
  dispatch)
    bash "$REPO_ROOT/scripts/harness/dispatch-subagent.sh" "${@:2}"
    ;;
  intelligence)
    python3 "$REPO_ROOT/scripts/generation/generate-repo-intelligence.py"
    ;;
  swarm)
    bash "$REPO_ROOT/scripts/harness/swarm-dispatch.sh" "${@:2}"
    ;;
  bootstrap)
    bash "$REPO_ROOT/scripts/setup/bootstrap-project.sh" "${@:2}"
    ;;
  info)
    echo "=== Workspace Info ==="
    echo "Repository: $(git rev-parse --show-toplevel)"
    echo "Git Branch: $(git rev-parse --abbrev-ref HEAD)"
    echo "Architecture: $(bash scripts/validation/validate-architecture.sh | grep 'Architecture:' || echo 'N/A')"
    echo "Security Audit: $(bash scripts/validation/audit-dependencies.sh | tail -n 1 || echo 'N/A')"
    echo "Governance: $(bash scripts/validation/validate-doc-governance.sh | tail -n 1 || echo 'N/A')"
    ;;
  docs)
    bash "$REPO_ROOT/scripts/docs/build-docs.sh" "${2:-build}"
    ;;
  hook)
    python3 "$REPO_ROOT/scripts/harness/agent-hook-dispatch.py" "${@:2}"
    ;;
  sbom)
    bash "$REPO_ROOT/scripts/generation/generate-sbom.sh"
    ;;
  help|*)
    show_help
    ;;
esac
