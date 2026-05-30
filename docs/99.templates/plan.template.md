---
title: <string>
version: <string>
owner: <string>
layer: product
stage: 04
status: draft
last-updated: YYYY-MM-DD
methodology: scrum
---

<!-- methodology: scrum | lean | kanban | hybrid -->

# Implementation Plan

<!-- Target: docs/04.execution/plans/YYYY-MM-DD-<slug>.md -->

## Usage Guidance

- **When to use**: Before starting complex multi-step execution.
- **Mandatory sections**: Work Breakdown, Verification Plan, Risks.
- **Naming rule**: `YYYY-MM-DD-<slug>.md`.
- **Hard Stops**: STOP if success criteria or rollback triggers are undefined. STOP if TDD requirements are missing.
- **Generation rule**: For derived-project seeds, keep `status: draft`, replace bracketed prompts with project facts or `TODO:`, and do not copy Project-Template maintenance plans as active implementation plans.
- **Lifecycle reference**: Apply `docs/00.agent-governance/rules/template-document-lifecycle.md` before reusing inherited documents.

## Purpose

The Implementation Plan defines the execution order, risk control, and rollout strategy for a specific feature or set of tasks.

---

## Overview (KR)

이 문서는 [기능 또는 컴포넌트명]의 실행 계획서다. 작업 분해, 검증, 롤아웃, 위험 관리, 완료 기준을 정의한다.

## Context

[Why this work exists.]

## Goals & In-Scope

- **Goals**:
- **In Scope**:

## Non-Goals & Out-of-Scope

- **Non-goals**:
- **Out of Scope**:

## Work Breakdown

| Task    | Description | Files / Docs Affected | Target REQ | Agent               | TDD Requirement | Validation Criteria |
| ------- | ----------- | --------------------- | ---------- | ------------------- | --------------- | ------------------- |
| PLN-001 | [Action]    | `path/to/file`        | REQ-001    | [Persona or `lead`] | [Yes/Exempt]    | [Evidence]          |

## Verification Plan

| ID          | Level      | Description | Command / How to Run | Pass Criteria |
| ----------- | ---------- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Structural | [Check]     | [Command]            | [Pass]        |

## Risks & Mitigations

| Risk   | Impact | Mitigation   |
| ------ | ------ | ------------ |
| [Risk] | High   | [Mitigation] |

## Methodology Overlay (Sprint / Kanban)

> Use this section when executing under SCRUM or KANBAN methodologies to replace standalone sprint/review templates.

### Sprint Iteration (If SCRUM)

- **Sprint Goal**:
- **Capacity/Velocity**:
- **Sprint Backlog**:

### Sprint Review & Retrospective (Post-Execution)

- **What went well**:
- **What could be improved**:
- **Action items for next sprint**:

### Kanban Board (If KANBAN)

#### WIP Limits

| Column      | WIP Limit | Rationale                        |
| :---------- | :-------: | :------------------------------- |
| In Progress |     3     | [Why this limit — team capacity] |
| Review      |     2     | [Why this limit — reviewer load] |

#### Active Items

| ID    | Description | Type | TDD Status | Assignee | Column  | Blocked By | Started | Cycle Time |
| :---- | :---------- | :--- | :--------- | :------- | :------ | :--------- | :------ | :--------- |
| T-001 | [Task]      | impl | Required   | —        | Backlog | —          | —       | —          |

#### Flow Metrics

| Week     | Throughput | Avg Cycle Time | Avg Lead Time | WIP Count |
| :------- | :--------: | :------------: | :-----------: | :-------: |
| YYYY-WXX |     0      |       —        |       —       |     0     |

#### Blocker Log

| Date       | Item  | Blocker Description | Resolved | Resolution |
| :--------- | :---- | :------------------ | :------- | :--------- |
| YYYY-MM-DD | T-001 | [Blocker]           | —        | —          |

#### Definition of Done

- [ ] Implementation matches acceptance criteria in the linked Spec.
- [ ] Tests pass (unit + integration where required).
- [ ] Code review approved (if `impl` type).
- [ ] Documentation updated if behavior changed.

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**:
- **Sandbox / Canary Rollout**:
- **Human Approval Gate**:
- **Rollback Trigger**:
- **Prompt / Model Promotion Criteria**:

## Completion Criteria

- [ ] Scoped work completed
- [ ] Verification passed
- [ ] Required docs updated

## Target-Relative Link Guidance

Keep placeholder paths as code spans until a generated document links to an existing file.

| Target Location                                | Governance Example                                       | Common Upstream/Downstream                                                 |
| ---------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------- |
| `docs/04.execution/plans/YYYY-MM-DD-<slug>.md` | `[../../00.agent-governance/rules/stage-gate-matrix.md]` | `[../../03.specs/<feature-id>/spec.md]`, `[../tasks/YYYY-MM-DD-<slug>.md]` |

## AI Execution Checklist

### Entry Gate

- [ ] PRD, ARD/ADR, and Spec anchors are approved or explicitly waived with rationale.
- [ ] `tests.md` exists or is scheduled for creation before execution task start for all `impl` work streams.
- [ ] TDD Requirement column is filled for every `impl` task in the Work Breakdown.

### Exit Gate

- [ ] Work breakdown, risks, validation commands, and rollback criteria are complete.
- [ ] Verification Plan maps every planned validation to a specific runnable command.
- [ ] Definition of Done checklist is complete if KANBAN methodology is active.

### Hard Stop Conditions

- **STOP** if no approved Spec exists for any planned work stream.
- **STOP** if PRD acceptance criteria are not reflected in the Verification Plan.
- **STOP** if rollback or success criteria are undefined.
- **STOP** if TDD Requirement is missing or blank for any `impl` task.
- **STOP** if `tests.md` does not exist and there is no plan to create it before execution tasking starts.
- **STOP** if any Verification Plan command is not a specific, runnable CLI command or executable script path.

### Downstream Trigger

- [ ] Create `docs/04.execution/tasks/` records before implementation starts.
- [ ] Ensure `tests.md` is created or linked for all `impl` task streams before `docs/04.execution/tasks/`.

### Evidence Rule

- [ ] Every planned validation MUST map to a specific execution command, log snippet, or review artifact link.

## Related Documents

- **PRD**: `[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`
- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **ADR**: `[../../02.architecture/decisions/####-<short-title>.md]`
