---
name: cicd-pipeline
description: Full pipeline for CI/CD pipeline design, configuration generation, security integration, and monitoring. An agent team collaborates to perform stage design, YAML configuration, security scan integration, and monitoring/alert design. Use for 'create a CI/CD pipeline', 'GitHub Actions', 'GitLab CI', 'Jenkins pipeline', 'deployment automation', 'build pipeline', 'DevOps pipeline', 'auto deploy', 'CI setup', 'CD setup'. Also supports optimization and security hardening for existing pipelines. Actual infrastructure provisioning (cloud resource creation), server configuration, and cluster management are outside scope.
---

# CI/CD Pipeline — Pipeline Design, Build, Monitoring, and Optimization

An agent team collaborates to perform CI/CD pipeline design, configuration generation, security integration, and monitoring in a single pass.

## Execution Mode

**Agent Team** — agents communicate via SendMessage and cross-validate each other's work.

## Agent Composition

| Agent             | File                                  | Role                                                                                                   | Type            |
| ----------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------- |
| infra-devops      | `.claude/agents/infra-devops.md`      | Stage design, branch strategy, deployment strategy; runner/container/secrets/environment configuration | general-purpose |
| sre-ops           | `.claude/agents/sre-ops.md`           | Metrics, alerts, dashboards, DORA metrics                                                              | general-purpose |
| security-engineer | `.claude/agents/security-engineer.md` | SAST, SCA, container scanning, secret detection                                                        | general-purpose |
| code-reviewer     | `.claude/agents/code-reviewer.md`     | Efficiency, reliability, security, and alignment verification of the final pipeline                    | general-purpose |

## Workflow

### Phase 1: Preparation (Orchestrator)

1. Extract from user input:
   - **Project Type**: Language/framework (Node.js, Python, Go, Java, etc.)
   - **CI/CD Tool**: GitHub Actions / GitLab CI / Jenkins
   - **Deployment Target**: AWS / GCP / Azure / Kubernetes / Docker
   - **Branch Strategy** (optional): GitFlow, Trunk-based
   - **Existing Files** (optional): Existing CI/CD configuration, Dockerfile, etc.
2. Create `_workspace/` directory at the project root.
3. Save organized input to `_workspace/00_input.md`.
4. If existing files are provided, copy to `_workspace/` and skip the corresponding phase.
5. Determine **execution mode** based on request scope.

### Phase 2: Team Assembly and Execution

| Order | Task                  | Owner             | Dependencies    | Artifact                                               |
| ----- | --------------------- | ----------------- | --------------- | ------------------------------------------------------ |
| 1     | Pipeline Design       | infra-devops      | None            | `_workspace/01_pipeline_design.md`                     |
| 2a    | Infrastructure Config | infra-devops      | Task 1          | `_workspace/02_pipeline_config/`, `02_infra_config.md` |
| 2b    | Security Scan Design  | security-engineer | Task 1          | `_workspace/04_security_scan.md`                       |
| 3     | Monitoring Design     | sre-ops           | Tasks 1, 2a     | `_workspace/03_monitoring.md`                          |
| 4     | Pipeline Review       | code-reviewer     | Tasks 2a, 2b, 3 | `_workspace/05_review_report.md`                       |

Tasks 2a (infrastructure) and 2b (security) run **in parallel**.

**Inter-team Communication Flow:**

- infra-devops (design) → delivers stage requirements to infrastructure config phase, scan placement to security-engineer, deployment strategy to sre-ops.
- infra-devops (infra) → delivers log/metric endpoints to sre-ops, image/dependency paths to security-engineer.
- security-engineer → delivers security alert rules to sre-ops.
- code-reviewer cross-validates all artifacts. On blocking finding: requests revision from relevant agent → rework → re-verify (max 2 rounds).

### Phase 3: Integration and Final Artifacts

1. Verify transient coordination files in `_workspace/`.
2. Promote authoritative CI/CD policy, operations, and runbook outcomes to `docs/05.operations/policies/` and `docs/05.operations/runbooks/` before handoff.
3. Confirm all blocking items from the review report have been addressed.
4. Report final summary to the user.

## Execution Modes by Scope

| User Request Pattern                                       | Execution Mode      | Agents Deployed                   |
| ---------------------------------------------------------- | ------------------- | --------------------------------- |
| "Create a CI/CD pipeline", "full design"                   | **Full Pipeline**   | All 4 agents                      |
| "Just set up CI"                                           | **CI Mode**         | infra-devops + code-reviewer      |
| "Add security scanning to this pipeline" (existing config) | **Security Mode**   | security-engineer + code-reviewer |
| "Design pipeline monitoring" (existing config)             | **Monitoring Mode** | sre-ops + code-reviewer           |
| "Review this CI/CD config"                                 | **Review Mode**     | code-reviewer only                |

**Leveraging Existing Files**: If existing YAML, Dockerfile, or other config files are provided, skip the corresponding phases.

## Data Transfer Protocol

| Strategy      | Method                  | Purpose                                                  |
| ------------- | ----------------------- | -------------------------------------------------------- |
| File-based    | `_workspace/` directory | Store transient pipeline coordination artifacts           |
| Message-based | SendMessage             | Real-time delivery of key information, revision requests |
| Task-based    | TaskCreate/TaskUpdate   | Progress tracking, dependency management                 |

File naming convention: `{order}_{agent}_{artifact}.{extension}`

## Error Handling

| Error Type                      | Strategy                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| CI/CD tool not specified        | Stop and request the CI/CD target or use the value declared by project intake        |
| Deployment target not specified | Stop and request the deployment target or use the value declared by project intake   |
| Agent failure                   | Retry once → if still failing, proceed without that artifact, note in review report |
| Blocking finding in review      | Request revision from relevant agent → rework → re-verify (max 2 rounds)            |
| Existing YAML parsing failure   | Manually analyze and create new configuration files                                 |
