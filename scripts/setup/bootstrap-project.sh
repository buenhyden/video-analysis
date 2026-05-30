#!/usr/bin/env bash
# bootstrap-project.sh
# Personalizes the template for a new project and performs initial hygiene.

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
DRY_RUN=false
KEEP_TEMPLATE_HISTORY=false
PROJECT_NAME=""
PROJECT_SLUG=""
AUTHOR="Autonomous Agent"
DESCRIPTION="A new project initialized from Project-Template."
GITHUB_OWNER=""
GITHUB_REPO=""
GITHUB_URL=""
SECURITY_EMAIL=""
CODEOWNERS_PREFIX=""
MAINTAINERS_TEAM="maintainers"
ARCHITECTS_TEAM="architects"
PLANNERS_TEAM="planners"
DEVOPS_TEAM="devops"
SECURITY_TEAM="security"
INTAKE_FILE=""
PRODUCT_PURPOSE=""
TARGET_USERS=""
CORE_FEATURES=""
SUCCESS_CRITERIA=""
APP_TYPE=""
LANGUAGE_STACK=""
FRAMEWORK_STACK=""
RUNTIME_STACK=""
PACKAGE_MANAGER=""
DATABASE_STACK=""
DEPLOYMENT_TARGET=""
CI_TARGET=""
DATA_CONSTRAINTS=""
SECURITY_CONSTRAINTS=""
EXTERNAL_SERVICES=""
ENVIRONMENTS=""
OBSERVABILITY=""
SLO_NEEDED=""
RELEASE_MODEL=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run) DRY_RUN=true; shift ;;
    --keep-template-history) KEEP_TEMPLATE_HISTORY=true; shift ;;
    --name) PROJECT_NAME="$2"; shift 2 ;;
    --slug) PROJECT_SLUG="$2"; shift 2 ;;
    --author) AUTHOR="$2"; shift 2 ;;
    --desc) DESCRIPTION="$2"; shift 2 ;;
    --github-owner) GITHUB_OWNER="$2"; shift 2 ;;
    --github-repo) GITHUB_REPO="$2"; shift 2 ;;
    --github-url) GITHUB_URL="$2"; shift 2 ;;
    --security-email) SECURITY_EMAIL="$2"; shift 2 ;;
    --codeowners-prefix) CODEOWNERS_PREFIX="$2"; shift 2 ;;
    --maintainers-team) MAINTAINERS_TEAM="$2"; shift 2 ;;
    --architects-team) ARCHITECTS_TEAM="$2"; shift 2 ;;
    --planners-team) PLANNERS_TEAM="$2"; shift 2 ;;
    --devops-team) DEVOPS_TEAM="$2"; shift 2 ;;
    --security-team) SECURITY_TEAM="$2"; shift 2 ;;
    --intake-file) INTAKE_FILE="$2"; shift 2 ;;
    --product-purpose) PRODUCT_PURPOSE="$2"; shift 2 ;;
    --target-users) TARGET_USERS="$2"; shift 2 ;;
    --core-features) CORE_FEATURES="$2"; shift 2 ;;
    --success-criteria) SUCCESS_CRITERIA="$2"; shift 2 ;;
    --app-type) APP_TYPE="$2"; shift 2 ;;
    --language) LANGUAGE_STACK="$2"; shift 2 ;;
    --framework) FRAMEWORK_STACK="$2"; shift 2 ;;
    --runtime) RUNTIME_STACK="$2"; shift 2 ;;
    --package-manager) PACKAGE_MANAGER="$2"; shift 2 ;;
    --database) DATABASE_STACK="$2"; shift 2 ;;
    --deployment-target) DEPLOYMENT_TARGET="$2"; shift 2 ;;
    --ci-target) CI_TARGET="$2"; shift 2 ;;
    --data-constraints) DATA_CONSTRAINTS="$2"; shift 2 ;;
    --security-constraints) SECURITY_CONSTRAINTS="$2"; shift 2 ;;
    --external-services) EXTERNAL_SERVICES="$2"; shift 2 ;;
    --environments) ENVIRONMENTS="$2"; shift 2 ;;
    --observability) OBSERVABILITY="$2"; shift 2 ;;
    --slo-needed) SLO_NEEDED="$2"; shift 2 ;;
    --release-model) RELEASE_MODEL="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$PROJECT_NAME" ]]; then
  echo "Error: --name is required."
  exit 1
fi

validate_intake() {
  if [[ -n "$INTAKE_FILE" ]]; then
    if [[ ! -f "$INTAKE_FILE" ]]; then
      echo "Error: --intake-file does not exist: $INTAKE_FILE"
      exit 1
    fi
    return 0
  fi

  local missing=()
  [[ -n "$PRODUCT_PURPOSE" ]] || missing+=("--product-purpose")
  [[ -n "$TARGET_USERS" ]] || missing+=("--target-users")
  [[ -n "$CORE_FEATURES" ]] || missing+=("--core-features")
  [[ -n "$SUCCESS_CRITERIA" ]] || missing+=("--success-criteria")
  [[ -n "$APP_TYPE" ]] || missing+=("--app-type")
  [[ -n "$LANGUAGE_STACK" ]] || missing+=("--language")
  [[ -n "$FRAMEWORK_STACK" ]] || missing+=("--framework")
  [[ -n "$RUNTIME_STACK" ]] || missing+=("--runtime")
  [[ -n "$PACKAGE_MANAGER" ]] || missing+=("--package-manager")
  [[ -n "$DATABASE_STACK" ]] || missing+=("--database")
  [[ -n "$DEPLOYMENT_TARGET" ]] || missing+=("--deployment-target")
  [[ -n "$CI_TARGET" ]] || missing+=("--ci-target")
  [[ -n "$DATA_CONSTRAINTS" ]] || missing+=("--data-constraints")
  [[ -n "$SECURITY_CONSTRAINTS" ]] || missing+=("--security-constraints")
  [[ -n "$EXTERNAL_SERVICES" ]] || missing+=("--external-services")
  [[ -n "$ENVIRONMENTS" ]] || missing+=("--environments")
  [[ -n "$OBSERVABILITY" ]] || missing+=("--observability")
  [[ -n "$SLO_NEEDED" ]] || missing+=("--slo-needed")
  [[ -n "$RELEASE_MODEL" ]] || missing+=("--release-model")

  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Error: project initialization intake is required."
    echo "Provide --intake-file <path> or all intake flags:"
    printf '  %s\n' "${missing[@]}"
    exit 1
  fi
}

validate_intake

PROJECT_SLUG=${PROJECT_SLUG:-$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')}
GITHUB_REPO=${GITHUB_REPO:-$PROJECT_SLUG}

if [[ -n "$GITHUB_URL" && -z "$GITHUB_OWNER" ]]; then
  GITHUB_PATH=${GITHUB_URL#git@github.com:}
  GITHUB_PATH=${GITHUB_PATH#https://github.com/}
  GITHUB_PATH=${GITHUB_PATH%.git}
  GITHUB_OWNER=${GITHUB_PATH%%/*}
  if [[ "$GITHUB_PATH" == */* && "$GITHUB_REPO" == "$PROJECT_SLUG" ]]; then
    GITHUB_REPO=${GITHUB_PATH#*/}
  fi
fi

if [[ -n "$GITHUB_OWNER" && -z "$CODEOWNERS_PREFIX" ]]; then
  CODEOWNERS_PREFIX="@$GITHUB_OWNER"
fi

echo "=== Project Bootstrapper ==="
echo "Name: $PROJECT_NAME"
echo "Slug: $PROJECT_SLUG"
echo "Author: $AUTHOR"
echo "Description: $DESCRIPTION"
if [[ -n "$GITHUB_OWNER" ]]; then
  echo "GitHub Repository: $GITHUB_OWNER/$GITHUB_REPO"
else
  echo "GitHub Repository: <unchanged template placeholders>"
fi
if [[ -n "$SECURITY_EMAIL" ]]; then
  echo "Security Email: $SECURITY_EMAIL"
else
  echo "Security Email: <unchanged template placeholder>"
fi
echo "Dry Run: $DRY_RUN"
echo "Keep Template History: $KEEP_TEMPLATE_HISTORY"
if [[ -n "$INTAKE_FILE" ]]; then
  echo "Intake File: $INTAKE_FILE"
else
  echo "Intake: explicit bootstrap flags"
fi
echo "============================"

# 1. Placeholder Replacement
replace_file_literal() {
  local target_file="$1"
  local pattern="$2"
  local replacement="$3"

  python3 - "$target_file" "$pattern" "$replacement" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
pattern = sys.argv[2]
replacement = sys.argv[3]

text = path.read_text(encoding="utf-8")
updated = text.replace(pattern, replacement)
if updated != text:
    path.write_text(updated, encoding="utf-8")
PY
}

replace_exact_line() {
  local target_file="$1"
  local pattern="$2"
  local replacement="$3"

  python3 - "$target_file" "$pattern" "$replacement" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
pattern = sys.argv[2]
replacement = sys.argv[3]

lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
changed = False
for index, line in enumerate(lines):
    newline = ""
    body = line
    if line.endswith("\r\n"):
        body = line[:-2]
        newline = "\r\n"
    elif line.endswith("\n"):
        body = line[:-1]
        newline = "\n"
    if body == pattern:
        lines[index] = f"{replacement}{newline}"
        changed = True

if changed:
    path.write_text("".join(lines), encoding="utf-8")
PY
}

yaml_string_literal() {
  local value="$1"

  python3 - "$value" <<'PY'
import json
import sys

print(json.dumps(sys.argv[1]))
PY
}

replace_project_name() {
  local target_file="$1"
  if ! grep -qF "Project-Template" "$target_file"; then
    return 0
  fi
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY] $target_file: Project-Template -> $PROJECT_NAME"
  else
    echo "  Processing $target_file"
    replace_file_literal "$target_file" "Project-Template" "$PROJECT_NAME"
  fi
}

initialize_design_file() {
  local design_file="$REPO_ROOT/DESIGN.md"
  if [[ ! -f "$design_file" ]]; then
    return 0
  fi

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY] DESIGN.md: initialize frontmatter version/name/description"
    return 0
  fi

  replace_exact_line "$design_file" "version: <string>" "version: \"alpha\""
  replace_exact_line "$design_file" "name: <string>" "name: $(yaml_string_literal "$PROJECT_NAME")"
  replace_exact_line "$design_file" "description: <string>" "description: $(yaml_string_literal "$DESCRIPTION")"
}

replace_literal() {
  local target_file="$1"
  local pattern="$2"
  local replacement="$3"
  if ! grep -qF "$pattern" "$target_file"; then
    return 0
  fi
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY] $target_file: $pattern -> $replacement"
  else
    replace_file_literal "$target_file" "$pattern" "$replacement"
  fi
}

codeowner_value() {
  local value="$1"
  if [[ "$value" == @* ]]; then
    printf '%s' "$value"
  else
    printf '%s/%s' "${CODEOWNERS_PREFIX%/}" "$value"
  fi
}

replace_github_metadata() {
  local owner_repo=""
  local maintainers=""
  local architects=""
  local planners=""
  local devops=""
  local security=""

  if [[ -z "$GITHUB_OWNER" && -z "$SECURITY_EMAIL" && -z "$CODEOWNERS_PREFIX" ]]; then
    echo "GitHub metadata placeholders retained. Pass --github-owner and --security-email for derived projects."
    return 0
  fi

  echo "Replacing GitHub metadata placeholders..."
  if [[ -n "$GITHUB_OWNER" ]]; then
    owner_repo="$GITHUB_OWNER/$GITHUB_REPO"
  fi
  if [[ -n "$CODEOWNERS_PREFIX" ]]; then
    maintainers=$(codeowner_value "$MAINTAINERS_TEAM")
    architects=$(codeowner_value "$ARCHITECTS_TEAM")
    planners=$(codeowner_value "$PLANNERS_TEAM")
    devops=$(codeowner_value "$DEVOPS_TEAM")
    security=$(codeowner_value "$SECURITY_TEAM")
  fi

  while IFS= read -r f; do
    if [[ -n "$owner_repo" ]]; then
      replace_literal "$f" "OWNER/REPO" "$owner_repo"
      replace_literal "$f" "<owner>/<repo>" "$owner_repo"
      replace_literal "$f" "<org>/<repo>" "$owner_repo"
    fi
    if [[ -n "$SECURITY_EMAIL" ]]; then
      replace_literal "$f" "security@example.com" "$SECURITY_EMAIL"
    fi
    if [[ -n "$CODEOWNERS_PREFIX" ]]; then
      replace_literal "$f" "@your-org/maintainers" "$maintainers"
      replace_literal "$f" "@your-org/architects" "$architects"
      replace_literal "$f" "@your-org/planners" "$planners"
      replace_literal "$f" "@your-org/devops" "$devops"
      replace_literal "$f" "@your-org/security" "$security"
      replace_literal "$f" "@your-org/*" "${CODEOWNERS_PREFIX%/}/*"
      replace_literal "$f" "your-github-username-or-team" "${maintainers#@}"
    fi
  done < <(find "$REPO_ROOT/.github" -type f)
}

# Find all relevant files (ignoring .git, node_modules, .venv)
echo "Replacing project identity placeholders..."
while IFS= read -r -d '' f; do
  replace_project_name "$f"
done < <(find "$REPO_ROOT" -type f \
  -not -path "*/.git/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/.next/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.venv/*" \
  -not -path "*/_workspace/*" \
  -not -path "*/graphify-out/*" \
  -not -path "*/.agent/*" \
  -not -path "*/.agent-work/*" \
  -not -path "*/.agents/*" \
  -not -path "*/.claude/*" \
  -not -path "*/docs/99.templates/*" \
  -not -path "*/bootstrap-project.sh" \
  \( -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.toml" -o -name "*.py" -o -name "*.dart" -o -name "Dockerfile" \) \
  -print0)

initialize_design_file
replace_github_metadata

reset_stage_history() {
  if [[ "$KEEP_TEMPLATE_HISTORY" == "true" ]]; then
    echo "Template stage history retained by --keep-template-history."
    return 0
  fi

  echo "Resetting template stage history for derived project..."
  local stages=(
    "01.requirements" "02.architecture/requirements" "02.architecture/decisions"
    "03.specs" "04.execution/plans" "04.execution/tasks"
    "05.operations/guides" "05.operations/policies" "05.operations/runbooks"
    "05.operations/incidents" "90.references"
  )

  for stage in "${stages[@]}"; do
    local stage_dir="$REPO_ROOT/docs/$stage"
    [[ -d "$stage_dir" ]] || continue

    if [[ "$DRY_RUN" == "true" ]]; then
      echo "  [DRY] Reset docs/$stage to README-only stage state"
      continue
    fi

    while IFS= read -r -d '' file_path; do
      rel_path="${file_path#"$REPO_ROOT"/}"
      if [[ "$rel_path" == "docs/$stage/README.md" ]]; then
        continue
      fi
      rm -f "$file_path"
    done < <(find "$stage_dir" -type f -print0)

    find "$stage_dir" -depth -type d -empty ! -path "$stage_dir" -delete
    bash "$REPO_ROOT/scripts/docs/update-doc-readme-index.sh" "$stage"
  done
}

reset_stage_history

write_intake_document() {
  local intake_doc
  intake_doc="$REPO_ROOT/docs/01.requirements/$(date +%Y-%m-%d)-project-intake-prd.md"

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY] Create docs/01.requirements/$(date +%Y-%m-%d)-project-intake-prd.md from initialization intake"
    return 0
  fi

  mkdir -p "$REPO_ROOT/docs/01.requirements"
  local seed_product_purpose="${PRODUCT_PURPOSE:-TODO: Extract product purpose from Source Intake.}"
  local seed_target_users="${TARGET_USERS:-TODO: Extract target users from Source Intake.}"
  local seed_core_features="${CORE_FEATURES:-TODO: Extract core features from Source Intake.}"
  local seed_success_criteria="${SUCCESS_CRITERIA:-TODO: Extract success criteria from Source Intake.}"
  local seed_security_constraints="${SECURITY_CONSTRAINTS:-TODO: Extract security constraints from Source Intake.}"
  local seed_slo_needed="${SLO_NEEDED:-TODO: Extract SLO need from Source Intake.}"

  {
    cat <<EOF
---
title: Project Initialization Intake
version: 1.0.0
owner: Product Manager
layer: product
stage: 01
status: draft
last-updated: $(date +%Y-%m-%d)
methodology: HYBRID
---

# Product Requirements Document (PRD)

<!-- Target: docs/01.requirements/YYYY-MM-DD-project-intake-prd.md -->

## Usage Guidance

- **When to use**: This is the first draft requirements seed for a derived project after bootstrap intake.
- **Mandatory sections**: Purpose, Vision, Functional Requirements, Acceptance Criteria, Scope and Non-goals, AI Execution Checklist, Related Documents.
- **Naming rule**: `YYYY-MM-DD-project-intake-prd.md` under `docs/01.requirements/`.
- **Hard Stops**: STOP if TODOs are treated as approved requirements or if downstream documents are created before intake review.

## Purpose

This PRD seed captures the first required input for the derived project
workspace. It is intentionally draft-only. Replace TODO rows with reviewed
project requirements before creating downstream ARD, ADR, spec, plan, task,
operations, or reference documents.

## Overview (KR)

이 문서는 파생 프로젝트의 초기 intake를 PRD 계약에 맞게 보관하는 seed 문서다.
아래 TODO 항목은 완료된 요구사항이나 승인된 결정이 아니며, 실제 프로젝트 검토 후
구체적인 요구사항으로 교체해야 한다.

## Vision

TODO: Confirm the durable user or business outcome for $PROJECT_NAME.

## Problem Statement

TODO: Validate the problem statement from the intake before treating it as an approved requirement.

## Personas

| Persona | Role | Primary Need | Pain Point |
| :--- | :--- | :--- | :--- |
| TODO | Target user from intake | $seed_target_users | TODO: Confirm pain point through discovery. |

## Key Use Cases

- **STORY-01**: TODO: As a target user, I want the project to solve the validated core problem so that $seed_success_criteria.

## Epics & Story Breakdown (SCRUM / HYBRID)

| Epic ID | Epic Name | Stories | Priority |
| :--- | :--- | :--- | :--- |
| EPIC-01 | Initial project intake validation | STORY-01 | Must-have |

## Priority Matrix (MoSCoW)

| Priority | Items |
| :--- | :--- |
| **Must-have** | Validate product purpose, target users, core features, success criteria, and stack choices. |
| **Should-have** | Convert intake into reviewed PRD, ARD, spec, execution, and operations documents as needed. |
| **Could-have** | Add examples only after they are clearly marked non-authoritative. |
| **Won't-have (this release)** | Treat Project-Template maintenance history as active project requirements. |

## Functional Requirements

- **REQ-PRD-FUN-01**: The derived project must preserve the reviewed project intake before downstream stage authoring.
- **REQ-PRD-FUN-02**: The derived project must replace template skeleton guidance with project-specific requirements before implementation starts.
- **REQ-PRD-FUN-03**: The derived project must use approved `docs/99.templates/` contracts for downstream governed documents.

## Non-Functional Requirements

- **Performance**: TODO: Define target performance only after the stack and usage model are confirmed.
- **Security**: $seed_security_constraints
- **Scalability**: TODO: Define scale targets after real traffic or workload assumptions are reviewed.
- **Reliability**: TODO: Define SLOs only if intake confirms SLO need: $seed_slo_needed.
- **Accessibility**: TODO: Define accessibility targets when UI scope exists.

## Acceptance Criteria

| ID | Given | When | Then | Story Ref |
| :--- | :--- | :--- | :--- | :--- |
| AC-001 | A maintainer has completed project intake | Bootstrap creates the derived workspace | A draft PRD seed exists in `docs/01.requirements/` and links to governance rules | STORY-01 |
| AC-002 | A downstream stage document is needed | An agent or maintainer creates it | The matching `docs/99.templates/` contract is used | STORY-01 |

## Success Criteria & Metrics

| ID | Metric | Baseline | Target | Measurement Method |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PRD-MET-01 | Bootstrap readiness | Template clone | Derived validation passes | `bash scripts/ws.sh validate-derived` |
| REQ-PRD-MET-02 | Product success | TODO | $seed_success_criteria | TODO: Confirm measurement method |

## Scope and Non-goals

- **In Scope**: $seed_product_purpose; $seed_core_features
- **Out of Scope**: Project-Template maintenance history and completed template remediation records.
- **Non-goals**: Pretending architecture, specs, plans, SLOs, or runbooks are approved before their stage gates.

## Risks, Dependencies, and Assumptions

| Type | Description | Validation / Owner |
| :--- | :--- | :--- |
| Risk | Intake values may be too broad for implementation. | Product Manager reviews before Stage 02/03. |
| Dependency | Stack choices must be confirmed before stack-specific rules are added. | System Architect validates intake. |
| Assumption | Bootstrap input represents the first project direction, not final approval. | Replace TODOs during PRD review. |

## SDLC Governance Triggers (TDD / SDD / DDD)

| Type | Trigger Condition | Status | Target Doc |
| :--- | :--- | :--- | :--- |
| **DDD** | Multiple domain collaboration or complex business logic? | TODO | `docs/02.architecture/requirements/` |
| **SDD** | Flow involves 3+ components/services? | TODO | `docs/03.specs/` |
| **TDD** | Core business logic requiring high reliability? | Always evaluate | `docs/03.specs/` then `docs/04.execution/tasks/` |

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: TODO: Define after project-specific AI scope is known.
- **Disallowed Actions**: Do not use Project-Template maintenance history as active product scope.
- **Human-in-the-loop Requirement**: Required for stack, security, data, and deployment commitments.
- **Evaluation Expectation**: TODO: Define project-specific evals if AI features exist.
- **Safety / Guardrail Notes**: $seed_security_constraints

## Lean Canvas (If Applicable)

### Problem

- **Top 3 Problems**:
  1. TODO: Validate primary problem.
  2. TODO: Validate secondary problem.
  3. TODO: Validate operational or adoption problem.
- **Existing Alternatives**: TODO: Document how target users solve this today.

### Customer Segments

- **Target Customers**: $seed_target_users
- **Early Adopters**: TODO: Identify early adopter segment.

### Unique Value Proposition

- **Single clear message**: TODO: Write after discovery.
- **High-Level Concept**: TODO: Define only after product positioning is reviewed.

### Solution

- **Top 3 Features**:
  1. $seed_core_features
  2. TODO: Split features into independently testable requirements.
  3. TODO: Defer speculative features.

### Channels

- **Path to Customers**: TODO: Define if this is a product with external users.

### Revenue Streams

- **Revenue Model**: TODO: Define if relevant.

### Cost Structure

- **Customer Acquisition Cost (CAC)**: TODO
- **Infrastructure / Hosting**: TODO

### Key Metrics

| Metric | Definition | Target | How to Measure |
| :--- | :--- | :--- | :--- |
| Activation | TODO | TODO | TODO |
| Retention | TODO | TODO | TODO |

## Intake Snapshot

| Field | Value |
| --- | --- |
| Name | $PROJECT_NAME |
| Slug | $PROJECT_SLUG |
| Description | $DESCRIPTION |
EOF

    if [[ -n "$INTAKE_FILE" ]]; then
      cat <<EOF
| Intake Source | $INTAKE_FILE |

## Source Intake

EOF
      sed 's/^/> /' "$INTAKE_FILE"
    else
      cat <<EOF
| Purpose | $PRODUCT_PURPOSE |
| Target users | $TARGET_USERS |
| Core features | $CORE_FEATURES |
| Success criteria | $SUCCESS_CRITERIA |

## Application And Stack

| Field | Value |
| --- | --- |
| Application type | $APP_TYPE |
| Language | $LANGUAGE_STACK |
| Framework | $FRAMEWORK_STACK |
| Runtime | $RUNTIME_STACK |
| Package manager | $PACKAGE_MANAGER |
| Database | $DATABASE_STACK |
| Deployment target | $DEPLOYMENT_TARGET |
| CI/CD target | $CI_TARGET |

## Security, Data, And Operations

| Field | Value |
| --- | --- |
| Data constraints | $DATA_CONSTRAINTS |
| Security constraints | $SECURITY_CONSTRAINTS |
| External services | $EXTERNAL_SERVICES |
| Environments | $ENVIRONMENTS |
| Observability | $OBSERVABILITY |
| SLO needed | $SLO_NEEDED |
| Release model | $RELEASE_MODEL |
EOF
    fi

    cat <<EOF

## AI Execution Checklist

- [ ] **Entry Gate**: Intake exists and is reviewed before ARD, ADR, spec, plan, task, operations, or reference authoring.
- [ ] **Procedure**: Replace TODOs with reviewed project requirements using `docs/99.templates/prd.template.md`.
- [ ] **Exit Gate**: Downstream documents link to this PRD seed until a more specific PRD supersedes it.
- [ ] **Hard Stop**: Stop if stack-specific assumptions are missing, contradicted, or absent from intake.
- [ ] **Downstream Trigger**: Create ARD/ADR/spec/plan/task documents only when their stage gates are reached.
- [ ] **Evidence Rule**: Keep validation output from `bash scripts/ws.sh validate-derived`.

## Related Documents

- [Requirements Guide](./README.md)
- [Project Initialization Intake Rule](../00.agent-governance/rules/project-initialization-intake.md)
- [Template Document Lifecycle](../00.agent-governance/rules/template-document-lifecycle.md)
- [PRD Template](../99.templates/prd.template.md)
EOF
  } > "$intake_doc"

  bash "$REPO_ROOT/scripts/docs/update-doc-readme-index.sh" "01.requirements"
}

write_intake_document

# 2. Hygiene: Reset Change Log
CHANGELOG_FILE="$REPO_ROOT/docs/00.agent-governance/policy-change-log.md"
if [[ "$DRY_RUN" == "false" ]]; then
  echo "Resetting policy-change-log.md..."
  cat > "$CHANGELOG_FILE" <<EOF
# Policy Change Log

---
title: Policy Change Log
version: 1.0.0
owner: Project Architect
layer: governance
stage: 00
status: active
last-updated: $(date +%Y-%m-%d)
---

## Overview

This log tracks all changes to the workspace governance, SDLC policies, and Git workflows.

## Change History

### [1.0.0] - $(date +%Y-%m-%d)
- **Action**: Project initialized from Project-Template.
- **Scope**: Workspace-wide.
- **Reference**: N/A.

---
EOF
fi

if [[ "$KEEP_TEMPLATE_HISTORY" == "true" ]]; then
  echo "Template stage history retained; no archive subfolder will be created."
else
  echo "Template stage history reset to README-driven stage folders."
fi

echo -e "\n✅ Bootstrapping complete."
if [[ "$DRY_RUN" == "true" ]]; then
  echo "NOTE: This was a dry run. No files were modified."
else
  echo "Next Steps: Replace PRD TODOs, initialize project metadata/design as needed, then run 'bash scripts/ws.sh validate-derived'."
fi
