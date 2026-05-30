# CI/CD Workflow Governance (May 2026)

> This document defines the branch-based CI/CD policy for the `Project-Template` workspace.

## Role definition

All AI agents and human contributors MUST treat GitHub Actions as governed infrastructure. Workflow changes require infra ownership, explicit branch filters, least-privilege permissions, and alignment with `git-flow`.

## Procedure

1. **Feature and fix validation**
   - Pull requests targeting `dev` MUST run template governance, lint/test/build checks that are available for the changed platform, and security checks where configured.
   - Every pull request targeting `dev` or `main` MUST pass a mandatory 90% line test coverage gate once an active implementation stack exists. The base `Project-Template` release skeleton may skip coverage when no stack manifest is present. Missing, unparseable, or below-threshold coverage artifacts block the PR after a stack is declared.
   - Feature branches SHOULD NOT deploy to shared environments.
2. **Development integration**
   - Pushes to `dev` represent integration state and MUST run release-readiness checks.
   - `dev` is the source branch for release promotion to `main`.
3. **Release promotion**
   - Promotion from `dev` to `main` MUST happen through a PR targeting `main`.
   - Automated workflows MAY create a release PR only after quality, security, build, and staging gates pass.
   - Workflows MUST NOT auto-merge the release PR.
   - Workflow-created PRs MUST use the repository PR template structure and fill all sections before review.
4. **Production validation**
   - Pushes to `main` MUST run production validation and release/tag automation when configured.
   - Production deploy steps MUST use GitHub environments or an equivalent approval gate before performing real deployment actions.
5. **Workflow security**
   - Declare minimal job-level `permissions:` for every job. Workflow-level `permissions:` is prohibited.
   - Every job MUST declare `timeout-minutes`.
   - Branch-filtered, `workflow_run`, scheduled, tag-triggered, and write-permission workflows MUST declare `concurrency` to avoid duplicate or conflicting runs.
   - Use OIDC for cloud authentication. PAT-based cloud credentials are prohibited.
   - Pin all third-party actions by full-length commit SHA. First-party `actions/*` may use tags only when policy allows, but known SHAs are preferred.
   - Checkout credentials MUST be disabled with `persist-credentials: false` except for explicitly documented generated-branch automation.
6. **Workflow validation gate**
   - Run canonical workspace validation before commit, push, or PR: `ws validate`, or `bash scripts/ws.sh validate` when the `ws` binary is not on PATH.
   - Canonical validation includes docs validation, docs governance, folder policy, cross-link validation, script inventory, GitHub workflow validation, GitHub metadata validation, skill quality, architecture validation, and conditional dependency/container audits.
   - CI/QA evidence must distinguish `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, and `chore` changes so reviewers can apply the correct validation expectations.
   - Incomplete but valuable checkpoints must record WIP state in the governed task/progress surface or PR body and must not be promoted to `dev` or `main` as completed work.
   - Run `bash scripts/ci/validate-security.sh` separately for security-sensitive changes or when validating the `ci-security.yml` gate locally.
   - Run `.github/gates/check-coverage.sh <coverage-report>` for every PR validation path; the default report path is `coverage/coverage.xml`. In the stack-neutral base template, the gate reports a skip only when no active stack manifest exists.
   - Run `bash scripts/ws.sh intelligence` after workflow, architecture, or intelligence generator changes.
   - Stack-specific lint/build/deploy gates remain conditional. The test coverage gate is conditional only for the base template before any active stack manifest exists; derived projects with a declared stack must provide coverage evidence.
   - Optional starter material under `examples/` MUST NOT be required by active CI.
   - The GitHub workflow validator enforces the active role matrix: workflow names, job ids, job display names, allowed actions, script refs, and required role markers must stay aligned with the maps below.

## Workflow Map

| Workflow | Event | Branches | Purpose |
| :--- | :--- | :--- | :--- |
| `ci-global.yml` | `push`, `pull_request` | `main`, `dev` | Run pre-commit, canonical workspace validation through `bash scripts/ws.sh validate`, and conditional 90% test coverage enforcement. |
| `ci-security.yml` | `push`, `pull_request`, schedule | `main`, `dev` | Run local security/secret checks, upload the short-retention Gitleaks report artifact, and run optional CodeQL analysis for GitHub Actions without stack-specific build steps. |
| `autopilot-intelligence.yml` | `push`, `pull_request` | `main`, `dev` | Generate and upload repository intelligence artifacts after branch-filtered events. |
| `generate-changelog.yml` | `push` tags | `v*.*.*` | Generate changelog changes on a non-protected branch, render PR body through `.github/scripts/render-changelog-pr-body.mjs`, and create or update a reviewed PR targeting `main`. |
| `ai-remediation.yml` | `workflow_run` | `main`, `dev` CI workflow completions | Collect diagnostics when validation workflows fail; does not push fixes automatically. |

## Repository Automation Map

These workflows are active GitHub automation but are not QA, release, deployment, or merge gates.

| Workflow | Event | Branches | Purpose |
| :--- | :--- | :--- | :--- |
| `greetings.yml` | `pull_request`, `issues` | `main`, `dev` for PRs | Post first-interaction comments. |
| `labeler.yml` | `pull_request` | `main`, `dev` | Apply stack-neutral PR labels. |
| `stale.yml` | schedule | default branch | Mark and close stale issues/PRs according to repository maintenance policy. |

## Constraints

- **HARD STOP**: HALT if a workflow can push directly to `main` or `dev` outside the PR policy.
- **HARD STOP**: HALT if a workflow creates and merges its own PR without human review.
- **HARD STOP**: HALT if a production workflow performs real deployment without environment approval or equivalent explicit gate.
- **HARD STOP**: HALT if workflow syntax cannot be parsed.
- **HARD STOP**: HALT if a workflow job lacks job-level `permissions` or `timeout-minutes`.
- **HARD STOP**: HALT if a third-party action is not pinned to a full-length commit SHA.
- **HARD STOP**: HALT if a branch-filtered, `workflow_run`, scheduled, tag-triggered, or write-permission workflow lacks concurrency control.
- **HARD STOP**: HALT if a workflow uses `pull_request_target` without a future ADR explicitly approving the trust boundary.
- **HARD STOP**: HALT if any PR validation path omits the 90% test coverage gate or allows missing coverage evidence to pass after an implementation stack is declared.
- Workflows must remain language-neutral unless a platform folder already exists and owns that technology.
- Active workflows must not reference stack paths moved under `examples/`.

## File references

- [AGENTS.md](../../../AGENTS.md) - Root Governance Router
- [git-workflow.md](./git-workflow.md) - Branching and PR policy
- [github-repository-governance.md](./github-repository-governance.md) - Repository and workflow security policy
- [documentation-protocol.md](./documentation-protocol.md) - Documentation standards
