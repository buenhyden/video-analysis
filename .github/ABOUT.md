# GitHub Configuration Hub

This directory stores GitHub-specific metadata for the minimal, language-agnostic governance template. It must describe and validate repository governance without implying a default application stack.

## Content Mapping

- **`workflows/`**: CI/CD gates, security gates, release-note automation, diagnostics, and repository automation workflows.
- **`gates/`**: Quality-gate helpers, including the 90% test coverage gate with a stack-neutral base-template exception.
- **`scripts/`**: GitHub workflow helpers that keep generated workflow content out of YAML.
- **`ISSUE_TEMPLATE/`**: Structured bug and feature request forms.
- **`PULL_REQUEST_TEMPLATE.md`**: PR traceability, validation evidence, and risk checklist.
- **`CODEOWNERS`**: Placeholder ownership map for repositories that replace `@your-org/*` values before enabling enforcement.
- **`SECURITY.md`**: Vulnerability reporting policy.

## Workflow Inventory

| Workflow | Classification | Purpose |
| :--- | :--- | :--- |
| `ci-global.yml` | CI/CD gate | Runs pre-commit, canonical `bash scripts/ws.sh validate`, and conditional 90% test coverage enforcement for every PR. |
| `ci-security.yml` | Security gate | Runs secret/security checks, uploads the short-retention Gitleaks report artifact, and runs optional CodeQL analysis for GitHub Actions without stack-specific build steps. |
| `autopilot-intelligence.yml` | Repository intelligence | Generates repository intelligence artifacts on branch-filtered events. |
| `generate-changelog.yml` | Release automation | Generates changelog changes from release tags, pushes only a generated branch, and creates or updates a reviewed PR to `main`. |
| `ai-remediation.yml` | Diagnostics | Collects failure diagnostics after core validation workflows fail; it does not push fixes. |
| `greetings.yml` | Repository automation | Posts first-interaction issue and PR greetings; it is not a QA or merge gate. |
| `labeler.yml` | Repository automation | Applies labels to PRs using stack-neutral repository metadata. |
| `stale.yml` | Repository automation | Manages stale issues and PRs on a schedule; it is not a QA or merge gate. |

## Governance Rules

- Git flow uses `main` for production and `dev` for integration.
- Active workflows must validate PRs and pushes for `main` and `dev` without pushing directly to protected branches.
- Branch-filtered, `workflow_run`, scheduled, tag-triggered, and write-permission workflows must declare top-level `concurrency`.
- Active workflow names, job ids, job display names, actions, script references, and inventory classifications are governed by the role matrix in `scripts/validation/validate-github-workflows.py` and `scripts/validation/validate-github-metadata.py`.
- Active workflows must not require optional starter material under `examples/`.
- Test coverage is mandatory once an implementation stack exists: `.github/gates/check-coverage.sh` must receive a parseable coverage artifact, enforce at least 90% line coverage, and fail missing or below-threshold coverage after an active stack manifest is declared.
- In the stack-neutral base template, the PR coverage gate may skip only when no active stack manifest is present. Stack-specific lint, test, build, or deployment gates remain conditional until a derived project declares active implementation paths.
- Repository automation workflows are not required status checks unless a future governance update explicitly promotes them to QA gates.
- Issue IDs are referenced when known or available; they are not mandatory for template governance changes.

## Required References

- CI/CD and infrastructure: [`docs/00.agent-governance/scopes/infra.md`](../docs/00.agent-governance/scopes/infra.md)
- Git workflow and PR policy: [`docs/00.agent-governance/rules/git-workflow.md`](../docs/00.agent-governance/rules/git-workflow.md)
- GitHub repository governance: [`docs/00.agent-governance/rules/github-repository-governance.md`](../docs/00.agent-governance/rules/github-repository-governance.md)
