# Infrastructure Layer Scope (March 2026)

`layer: infra`

This scope defines constraints for the Infra/DevOps persona.

## 1. Core Responsibilities

- **Stage 08 (Operations)**: define environment and deployment policy.
- **Stage 09 (Runbooks)**: define executable response procedures.
- **Stage 10 (Incidents/Postmortems)**: support operational evidence and prevention loops.
- **GitHub Workflow Permissions**: all `.github/workflows/` changes must declare `permissions:` at job level; default is `read-all`; `write-all` is prohibited.
- **OIDC**: cloud authentication in workflows must use OIDC token exchange; PAT-based cloud auth is prohibited.
- **Branch Protection Alignment**: when CI check names change, update branch protection required-check configuration accordingly.
- **CODEOWNERS + PR Template Alignment**: keep `.github/CODEOWNERS` paths and `.github/PULL_REQUEST_TEMPLATE.md` references consistent with current repo taxonomy; replace stale paths before merging.

See `rules/github-repository-governance.md` §3–§8 for the full workflow security and required-checks policy.

## 2. Canonical Paths

- Operations policy: `docs/05.operations/policies/`
- Runbooks: `docs/05.operations/runbooks/`
- Incident tracking: `docs/05.operations/incidents/`
- Postmortems: `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md`

## 3. Template Mapping

- `operation.template.md`
- `runbook.template.md`
- `incident.template.md`
- `postmortem.template.md`

## 4. Quality Focus

- deployment safety and rollback readiness
- operational observability and ownership clarity
- runbook executability by on-call engineers

## File Ownership

- **Allowed Write**: `infra/**` · `.github/**` · `docs/05.operations/policies/**` · `docs/05.operations/runbooks/**`
- **Forbidden Write**: implementation paths unless explicitly required by an approved infra plan · `docs/99.templates/**`
- **Pre-condition**: Approved Spec and operations policy exist before infra changes.
- **Post-condition**: Deployment procedure validated; rollback path documented in runbook.

## Subagent Definition

- **Trigger**: Pre-production infra change, CI/CD pipeline update, or runbook authoring.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/infra-devops.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
