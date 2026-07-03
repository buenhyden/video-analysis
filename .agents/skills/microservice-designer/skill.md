---
name: microservice-designer
description: Full pipeline for designing, decomposing, and documenting microservice architectures. An agent team collaborates on domain analysis, service design, communication patterns, and observability. Use for 'design a microservice architecture', 'decompose services', 'MSA design', 'domain analysis', 'event-driven architecture', 'inter-service communication design', 'distributed system design', 'API gateway design'. Also supports monolith-to-MSA transitions. Actual infrastructure setup, Kubernetes deployment, and code implementation are outside scope.
---

# Microservice Designer — Architecture Design Pipeline

An agent team collaborates through: domain analysis → service design → communication design → observability design.

## Execution Mode

**Agent Team** — agents communicate via SendMessage and cross-validate deliverables.

## Agent Composition

| Agent            | File                                 | Role                                                                                                                                                          | Type            |
| ---------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| system-architect | `.Codex/agents/system-architect.md` | Domain analysis (bounded contexts, event storming); service design (API contracts, data ownership); communication design (sync/async, Saga); cross-validation | general-purpose |
| sre-ops          | `.Codex/agents/sre-ops.md`          | Observability design — SLI/SLO, metrics, logging, distributed tracing, alerting                                                                               | general-purpose |
| code-reviewer    | `.Codex/agents/code-reviewer.md`    | Architecture review — anti-pattern detection, consistency across all deliverables                                                                             | general-purpose |

## Workflow

### Phase 1: Preparation (Orchestrator)

1. Extract from user input:
   - **Business Domain**: System or service being designed
   - **Current State** (optional): Monolith migration or greenfield
   - **Scale/Constraints** (optional): Expected traffic, team size, tech stack constraints
   - **Existing Documentation** (optional): ERD, architecture docs, API docs
2. Create `_workspace/` at the project root.
3. Save organized input to `_workspace/00_input.md`.
4. If existing files are available, skip corresponding phases.

### Phase 2: Team Assembly and Execution

| Order | Task                 | Owner            | Dependencies | Deliverable                             |
| ----- | -------------------- | ---------------- | ------------ | --------------------------------------- |
| 1     | Domain Analysis      | system-architect | None         | `_workspace/01_domain_analysis.md`      |
| 2     | Service Design       | system-architect | Task 1       | `_workspace/02_service_design.md`       |
| 3a    | Communication Design | system-architect | Tasks 1, 2   | `_workspace/03_communication_design.md` |
| 3b    | Observability Design | sre-ops          | Task 2       | `_workspace/04_observability_design.md` |
| 4     | Architecture Review  | code-reviewer    | Tasks 1–3b   | `_workspace/05_review_report.md`        |

Tasks 3a and 3b can run **in parallel**.

**Inter-team Communication Flow:**

- Domain analysis completes → delivers bounded contexts and aggregates to service design; delivers domain events to communication design.
- Service design completes → delivers service catalog and API contracts to communication design; delivers service list and dependencies to sre-ops.
- Communication design completes → delivers communication matrix and Saga flows to sre-ops.
- code-reviewer cross-validates all deliverables. On blocking finding: requests fix → rework → re-verify (max 2 rounds).

### Phase 3: Integration and Final Deliverables

1. Verify transient coordination files in `_workspace/`.
2. Promote authoritative architecture outcomes to `docs/02.architecture/requirements/`, `docs/02.architecture/decisions/`, or `docs/03.specs/` before handoff when the design is accepted.
3. Confirm all blocking findings from the review have been addressed.
4. Report final summary to the user.

## Execution Modes by Scope

| User Request Pattern                          | Execution Mode         | Agents Deployed                  |
| --------------------------------------------- | ---------------------- | -------------------------------- |
| "Design a microservice architecture"          | **Full Pipeline**      | All 3 agents                     |
| "Analyze the domain", "Event storming"        | **Domain Mode**        | system-architect + code-reviewer |
| "Decompose services" (domain analysis exists) | **Service Mode**       | system-architect + code-reviewer |
| "Design inter-service communication"          | **Communication Mode** | system-architect + code-reviewer |
| "Design monitoring/observability"             | **Observability Mode** | sre-ops + code-reviewer          |

## Data Transfer Protocol

| Strategy      | Method                  | Purpose                                          |
| ------------- | ----------------------- | ------------------------------------------------ |
| File-based    | `_workspace/` directory | Store transient design coordination artifacts    |
| Message-based | SendMessage             | Real-time key information delivery, fix requests |
| Task-based    | TaskCreate/TaskUpdate   | Progress tracking, dependency management         |

## Error Handling

| Error Type                      | Strategy                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| Insufficient domain information | Draft using similar domain reference patterns; request user validation              |
| Too many services               | Recommend modular monolith first; provide gradual decomposition roadmap             |
| Agent failure                   | Retry once → if still failing, proceed without deliverable, note omission in review |
| Blocking finding in review      | Request fix from relevant agent → rework → re-verify (max 2 rounds)                 |
| Distributed monolith signs      | Request service boundary readjustment from system-architect                         |
