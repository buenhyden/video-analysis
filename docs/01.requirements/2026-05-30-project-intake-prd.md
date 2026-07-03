---
title: Project Initialization Intake
version: 1.0.0
owner: Product Manager
layer: product
stage: 01
status: draft
last-updated: 2026-05-30
methodology: HYBRID
---

# Product Requirements Document (PRD)

<!-- Target: docs/01.requirements/YYYY-MM-DD-project-intake-prd.md -->

## Usage Guidance

- **When to use**: This is the first draft requirements seed for a derived project after bootstrap intake.
- **Mandatory sections**: Purpose, Vision, Functional Requirements, Acceptance Criteria, Scope and Non-goals, AI Execution Checklist, Related Documents.
- **Naming rule**:  under .
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

TODO: Confirm the durable user or business outcome for video-analysis.

## Problem Statement

TODO: Validate the problem statement from the intake before treating it as an approved requirement.

## Personas

| Persona | Role | Primary Need | Pain Point |
| :--- | :--- | :--- | :--- |
| TODO | Target user from intake | Internal users or external clients needing video processing | TODO: Confirm pain point through discovery. |

## Key Use Cases

- **STORY-01**: TODO: As a target user, I want the project to solve the validated core problem so that Stable, scalable microservices with React frontend.

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
- **REQ-PRD-FUN-03**: The derived project must use approved  contracts for downstream governed documents.

## Non-Functional Requirements

- **Performance**: TODO: Define target performance only after the stack and usage model are confirmed.
- **Security**: TBD
- **Scalability**: TODO: Define scale targets after real traffic or workload assumptions are reviewed.
- **Reliability**: TODO: Define SLOs only if intake confirms SLO need: TBD.
- **Accessibility**: TODO: Define accessibility targets when UI scope exists.

## Acceptance Criteria

| ID | Given | When | Then | Story Ref |
| :--- | :--- | :--- | :--- | :--- |
| AC-001 | A maintainer has completed project intake | Bootstrap creates the derived workspace | A draft PRD seed exists in  and links to governance rules | STORY-01 |
| AC-002 | A downstream stage document is needed | An agent or maintainer creates it | The matching  contract is used | STORY-01 |

## Success Criteria & Metrics

| ID | Metric | Baseline | Target | Measurement Method |
| :--- | :--- | :--- | :--- | :--- |
| REQ-PRD-MET-01 | Bootstrap readiness | Template clone | Derived validation passes | Running Docs Validation...
Checking template readiness invariants...
Template readiness validation failed:
- docs/01.requirements/2026-05-30-project-intake-prd.md: canonical docs must start with YAML frontmatter
- docs/01.requirements/2026-05-30-project-intake-prd.md: template conformance failed (missing YAML frontmatter; missing required section `## AI Execution Checklist`; missing required section `## Related Documents`; does not match required docs/99.templates contract for its path; expected one of: prd.template.md)
- docs/01.requirements/README.md: missing Documents rows for ['./2026-05-30-project-intake-prd.md']
Checking docs/99.templates/ for required frontmatter...
Checking docs folder READMEs for lifecycle rules...
Checking agent instructions for 4-part structure...
Checking DESIGN.md for initialization placeholders...
❌ DESIGN.md still contains base-template placeholders in derived repository 'video-analysis'.
Running format and linting checks...
Running markdownlint...
markdownlint-cli2 v0.22.1 (markdownlint v0.40.0)
Finding: **/*.md !node_modules !.claude/ !.codex/ !.git/ !.history/ !.mypy_cache/ !.vscode/ !node_modules/ !.sisyphus/ !dist/ !coverage/ !storybook-static/ !AGENTS.md !CLAUDE.md !GEMINI.md !docs/00.agent-governance/memory/template.md !docs/99.templates/readme.template.md !.agent-work/ !.agent/ !.agents/ !graphify-out/ !docs/00.agent-governance/memory/progress.md !docs/04.execution/plans/2026-05-18-template-purpose-generated-doc-sync.md
Linting: 367 file(s)
Summary: 160 error(s)
Running yamllint...
./tmp/hy-home.service-1/.pre-commit-config.yaml
  1:7       error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-1/docker-compose.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-1/docker-compose.test.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-1/tests/load/docker-compose.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.frontend/docker-compose.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-2/.pre-commit-config.yaml
  1:7       error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-2/docker-compose.test.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-2/tests/load/docker-compose.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

Running shellcheck...
Validation failed. |
| REQ-PRD-MET-02 | Product success | TODO | Stable, scalable microservices with React frontend | TODO: Confirm measurement method |

## Scope and Non-goals

- **In Scope**: Video analysis and processing monorepo containing frontend and Python microservices; Video processing (OpenCV), async message handling (Kafka), search (OpenSearch)
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
| **DDD** | Multiple domain collaboration or complex business logic? | TODO |  |
| **SDD** | Flow involves 3+ components/services? | TODO |  |
| **TDD** | Core business logic requiring high reliability? | Always evaluate |  then  |

## AI Agent Requirements (If Applicable)

- **Allowed Actions**: TODO: Define after project-specific AI scope is known.
- **Disallowed Actions**: Do not use Project-Template maintenance history as active product scope.
- **Human-in-the-loop Requirement**: Required for stack, security, data, and deployment commitments.
- **Evaluation Expectation**: TODO: Define project-specific evals if AI features exist.
- **Safety / Guardrail Notes**: TBD

## Lean Canvas (If Applicable)

### Problem

- **Top 3 Problems**:
  1. TODO: Validate primary problem.
  2. TODO: Validate secondary problem.
  3. TODO: Validate operational or adoption problem.
- **Existing Alternatives**: TODO: Document how target users solve this today.

### Customer Segments

- **Target Customers**: Internal users or external clients needing video processing
- **Early Adopters**: TODO: Identify early adopter segment.

### Unique Value Proposition

- **Single clear message**: TODO: Write after discovery.
- **High-Level Concept**: TODO: Define only after product positioning is reviewed.

### Solution

- **Top 3 Features**:
  1. Video processing (OpenCV), async message handling (Kafka), search (OpenSearch)
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
| Name | video-analysis |
| Slug | video-analysis |
| Description | A new project initialized from Project-Template. |
| Purpose | Video analysis and processing monorepo containing frontend and Python microservices |
| Target users | Internal users or external clients needing video processing |
| Core features | Video processing (OpenCV), async message handling (Kafka), search (OpenSearch) |
| Success criteria | Stable, scalable microservices with React frontend |

## Application And Stack

| Field | Value |
| --- | --- |
| Application type | polyglot-monorepo |
| Language | TypeScript, Python 3.13 |
| Framework | React, FastAPI |
| Runtime | Node.js, uv |
| Package manager | npm, uv |
| Database | PostgreSQL, Redis, OpenSearch |
| Deployment target | Docker |
| CI/CD target | GitHub Actions |

## Security, Data, And Operations

| Field | Value |
| --- | --- |
| Data constraints | TBD |
| Security constraints | TBD |
| External services | TBD |
| Environments | dev, prod |
| Observability | OpenTelemetry, Loki |
| SLO needed | TBD |
| Release model | TBD |

## AI Execution Checklist

- [ ] **Entry Gate**: Intake exists and is reviewed before ARD, ADR, spec, plan, task, operations, or reference authoring.
- [ ] **Procedure**: Replace TODOs with reviewed project requirements using .
- [ ] **Exit Gate**: Downstream documents link to this PRD seed until a more specific PRD supersedes it.
- [ ] **Hard Stop**: Stop if stack-specific assumptions are missing, contradicted, or absent from intake.
- [ ] **Downstream Trigger**: Create ARD/ADR/spec/plan/task documents only when their stage gates are reached.
- [ ] **Evidence Rule**: Keep validation output from Running Docs Validation...
Checking template readiness invariants...
Template readiness validation failed:
- docs/01.requirements/2026-05-30-project-intake-prd.md: template conformance failed (missing required section `## AI Execution Checklist`; missing required section `## Related Documents`)
- docs/01.requirements/README.md: missing Documents rows for ['./2026-05-30-project-intake-prd.md']
Checking docs/99.templates/ for required frontmatter...
Checking docs folder READMEs for lifecycle rules...
Checking agent instructions for 4-part structure...
Checking DESIGN.md for initialization placeholders...
❌ DESIGN.md still contains base-template placeholders in derived repository 'video-analysis'.
Running format and linting checks...
Running markdownlint...
markdownlint-cli2 v0.22.1 (markdownlint v0.40.0)
Finding: **/*.md !node_modules !.claude/ !.codex/ !.git/ !.history/ !.mypy_cache/ !.vscode/ !node_modules/ !.sisyphus/ !dist/ !coverage/ !storybook-static/ !AGENTS.md !CLAUDE.md !GEMINI.md !docs/00.agent-governance/memory/template.md !docs/99.templates/readme.template.md !.agent-work/ !.agent/ !.agents/ !graphify-out/ !docs/00.agent-governance/memory/progress.md !docs/04.execution/plans/2026-05-18-template-purpose-generated-doc-sync.md
Linting: 367 file(s)
Summary: 166 error(s)
Running yamllint...
./tmp/hy-home.service-1/.pre-commit-config.yaml
  1:7       error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-1/docker-compose.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-1/docker-compose.test.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-1/tests/load/docker-compose.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.frontend/docker-compose.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-2/.pre-commit-config.yaml
  1:7       error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-2/docker-compose.test.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

./tmp/hy-home.service-2/tests/load/docker-compose.yml
  1:10      error    wrong new line character: expected \n  (new-lines)

Running shellcheck...
Validation failed..

## Related Documents

- [Requirements Guide](./README.md)
- [Project Initialization Intake Rule](../00.agent-governance/rules/project-initialization-intake.md)
- [Template Document Lifecycle](../00.agent-governance/rules/template-document-lifecycle.md)
- [PRD Template](../99.templates/prd.template.md)
