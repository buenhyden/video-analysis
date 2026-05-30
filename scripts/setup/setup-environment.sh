#!/usr/bin/env bash
# setup-environment.sh
# Reports local prerequisites for the minimal governance template.

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)

echo "=== Workspace Prerequisite Check ==="

check_tool() {
  local tool_name="$1"
  local required="$2"
  local note="${3:-}"

  if command -v "$tool_name" >/dev/null 2>&1; then
    echo "  [OK] $tool_name: $(command -v "$tool_name")"
  elif [[ "$required" == "required" ]]; then
    echo "  [MISSING] $tool_name: required for core governance workflows${note:+ - $note}"
  else
    echo "  [OPTIONAL] $tool_name: install only if the related task or declared stack needs it${note:+ - $note}"
  fi
}

check_python_module() {
  local module_name="$1"
  local required="$2"
  local note="${3:-}"

  if python3 -c "import ${module_name}" >/dev/null 2>&1; then
    echo "  [OK] python module ${module_name}"
  elif [[ "$required" == "required" ]]; then
    echo "  [MISSING] python module ${module_name}: required for core governance workflows${note:+ - $note}"
  else
    echo "  [OPTIONAL] python module ${module_name}: install only if the related task needs it${note:+ - $note}"
  fi
}

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

echo "[ Core ]"
check_tool "git" "required" "repository state, validation, and PR workflow"
check_tool "bash" "required" "workspace command router and shell validators"
check_tool "python3" "required" "governance validators and bootstrap helpers"
check_tool "rg" "required" "fast repository search and reference audits"
check_python_module "yaml" "required" "workflow and metadata validators"

echo "[ Review and publishing ]"
check_tool "gh" "optional" "local PR creation, PR inspection, and CI status review"

echo "[ Optional local lint tools ]"
check_tool "markdownlint-cli2" "optional" "Markdown linting"
check_tool "yamllint" "optional" "YAML linting"
check_tool "shellcheck" "optional" "shell script linting"
check_tool "mkdocs" "optional" "docs site build or serve"

echo "[ Optional security and stack tools ]"
check_tool "bandit" "optional" "Python security checks"
check_tool "pip-audit" "optional" "Python dependency audit"
check_tool "gitleaks" "optional" "focused secret scan"
check_tool "trivy" "optional" "container image scan"
check_tool "node" "optional" "derived JavaScript/TypeScript stacks"
check_tool "npm" "optional" "derived JavaScript/TypeScript dependency tasks"
check_tool "docker" "optional" "derived container tasks"

echo "[ Stack roots ]"
if has_active_stack_roots; then
  echo "  [NOTICE] Active implementation roots detected. Confirm they are intentional for this project."
else
  echo "  [OK] No active application stack roots in the minimal template."
fi

echo "[ Policy ]"
echo "  [INFO] ws setup is report-only; it must not install tools or mutate files."
echo "  [INFO] Read docs/00.agent-governance/rules/environment-readiness.md before changing prerequisite classes."

echo "=== Prerequisite check complete ==="
