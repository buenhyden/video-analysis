---
name: fullstack-webapp
description: Optional fullstack development pipeline for projects that explicitly choose a web application stack. This skill must not create or imply a default stack for the root minimal governance template.
---

# Fullstack Web App — Optional Development Pipeline

An agent team collaborates through the pipeline after a consuming project declares its implementation paths and technology choices. The root template remains language-agnostic and does not provide a default application stack.

## Execution Mode

**Agent Team** — agents communicate via SendMessage and cross-verify deliverables.

## Agent Composition

| Agent             | File                                  | Role                                                                    | Type            |
| ----------------- | ------------------------------------- | ----------------------------------------------------------------------- | --------------- |
| system-architect  | `.claude/agents/system-architect.md`  | Requirements analysis, architecture design, DB modeling, API design     | general-purpose |
| frontend-engineer | `.claude/agents/frontend-engineer.md` | Project-declared UI components, routing, state management, API integration | general-purpose |
| backend-engineer  | `.claude/agents/backend-engineer.md`  | API implementation, DB integration, auth, business logic                | general-purpose |
| qa-inspector      | `.claude/agents/qa-inspector.md`      | Test strategy, unit/integration/E2E tests, coverage analysis            | general-purpose |
| infra-devops      | `.claude/agents/infra-devops.md`      | CI/CD pipeline, infrastructure configuration, deployment, monitoring    | general-purpose |

## Workflow

### Phase 1: Preparation (Orchestrator)

1. Extract from user input:
   - **App Description**: Purpose and core features of the web app
   - **Technology Stack**: Required before implementation; do not assume a default.
   - **Scale** (optional): MVP/small/medium/large
   - **Existing Code** (optional): Existing project to extend
   - **Deployment Platform** (optional): project-selected target, if any.
2. Create `_workspace/` directory at the project root.
3. Save organized input to `_workspace/00_input.md`.
4. If existing code is provided, analyze it and adjust relevant phases.
5. Determine **execution mode** based on request scope.

### Phase 2: Team Assembly and Execution

| Order | Task                 | Owner             | Dependencies | Deliverables                                              |
| ----- | -------------------- | ----------------- | ------------ | --------------------------------------------------------- |
| 1     | Architecture Design  | system-architect  | None         | `docs/03.specs/<feature-id>/spec.md`, `docs/03.specs/<feature-id>/api-spec.md`, `docs/03.specs/<feature-id>/data-model.md` |
| 2a    | Frontend Development | frontend-engineer | Task 1       | project-declared frontend code path                      |
| 2b    | Backend Development  | backend-engineer  | Task 1       | project-declared backend code path                       |
| 2c    | Deployment Setup     | infra-devops      | Task 1       | `docs/05.operations/policies/<feature-id>/deployment-guide.md`, CI/CD config |
| 3     | Testing & Review     | qa-inspector      | Tasks 2a, 2b | `docs/03.specs/<feature-id>/tests.md`, `_workspace/06_review_report.md`, test code |

Tasks 2a, 2b, and 2c run **in parallel** — all depend only on Task 1.

**Inter-team Communication Flow:**

- system-architect completes → delivers component structure/routing to frontend-engineer; API/DB/auth spec to backend-engineer; infrastructure requirements to infra-devops; functional requirements to qa-inspector.
- frontend-engineer ↔ backend-engineer: Real-time communication during API integration.
- infra-devops completes → shares environment variables and deployment URLs with all agents.
- qa-inspector reviews all code and tests. On blocking finding: requests fix from relevant agent → rework → re-verify (max 2 rounds).

### Phase 3: Integration and Final Deliverables

1. Verify canonical docs in `docs/` plus transient coordination notes in `_workspace/`.
2. Confirm all blocking findings from the review have been addressed.
3. Report final summary to the user:
   - Architecture Design — `docs/03.specs/<feature-id>/spec.md`
   - API Specification — `docs/03.specs/<feature-id>/api-spec.md`
   - DB Schema — `docs/03.specs/<feature-id>/data-model.md`
   - Test Plan — `docs/03.specs/<feature-id>/tests.md`
   - Deployment Guide — `docs/05.operations/policies/<feature-id>/deployment-guide.md`
   - Review Report — `_workspace/06_review_report.md`
   - Source Code — project-declared implementation paths

## Execution Modes by Scale

| Request Pattern                               | Execution Mode       | Agents Deployed                                     |
| --------------------------------------------- | -------------------- | --------------------------------------------------- |
| "Build me a web app", "fullstack development" | **Full Pipeline**    | All 5                                               |
| "Just build the API"                          | **Backend Mode**     | system-architect + backend-engineer + qa-inspector  |
| "Just build the frontend" (API exists)        | **Frontend Mode**    | system-architect + frontend-engineer + qa-inspector |
| "Refactor this code"                          | **Refactoring Mode** | system-architect + relevant engineer + qa-inspector |
| "Just set up deployment"                      | **DevOps Mode**      | infra-devops only                                   |

**Leveraging Existing Code**: If existing code is provided, system-architect analyzes extension points and only necessary agents are deployed.

## Data Transfer Protocol

| Strategy      | Method                 | Purpose                                               |
| ------------- | ---------------------- | ----------------------------------------------------- |
| File-based    | `docs/` + `_workspace/` + project-declared implementation paths | canonical design docs + transient coordination + source code |
| Message-based | SendMessage            | API integration issues, review findings, fix requests |
| Task-based    | TaskCreate/TaskUpdate  | Progress tracking, dependency management              |

## Error Handling

| Error Type                 | Strategy                                                                  |
| -------------------------- | ------------------------------------------------------------------------- |
| Ambiguous requirements     | Stop and request project-specific requirements; do not infer CRUD scope    |
| Unspecified tech stack     | Stop and request a stack decision before implementation.                   |
| Build errors               | Analyze logs → relevant engineer fixes → qa-inspector re-verifies         |
| Agent failure              | Retry once → proceed without deliverable if still failing, note in review |
| Blocking finding in review | Request fix from relevant agent → rework → re-verify (max 2 rounds)       |

## Output Routing Rules

- Final architecture, API, data-model, and test-plan artifacts must be written under canonical `docs/03.specs/<feature-id>/`.
- Final deployment guidance must be written under canonical operations docs, not `_workspace/`.
- `_workspace/` is for transient input, review, and coordination files only.
