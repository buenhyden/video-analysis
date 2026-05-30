---
title: <string>
version: <string>
owner: <string>
layer: qa
stage: 03
status: draft
last-updated: YYYY-MM-DD
---

# Test & Evaluation Strategy

<!-- Target: docs/03.specs/<feature-id>/tests.md -->

## Usage Guidance

- **When to use**: To define how a feature will be verified, including TDD scope and agent evals.
- **Mandatory sections**: Overview, TDD Scope, Test Matrix, Agent Evals (if applicable).
- **Naming rule**: `tests.md` (within the feature directory).
- **Hard Stops**: STOP if no parent Spec exists. STOP if TDD targets are empty without exemptions.
- **Derived-project seed rule**: Create only after a parent spec exists; keep `status: draft` and TODOs until verification scope is reviewed.

## Purpose

The Test & Evaluation Strategy ensures that every feature is built on a foundation of verifiable behavior. It bridges the gap between design requirements and implementation evidence.

---

## Overview (KR)

단위, 통합, 계약, 성능 테스트 및 Agent Eval 기준을 정리한다.

## Parent Documents

- **Spec**: `[./spec.md]`
- **Domain Events**: `[./domain-events.md]`
- **API Spec**: `[./api-spec.md]`

## Verification Goals

- **What must be proven**:
- **What risks are targeted**:

## TDD Scope

### Red-Green-Refactor Targets

| Behavior | Test File | RED status | GREEN status | REFACTORED |
| :--- | :--- | :--- | :--- | :--- |
| [Core behavior 1] | `tests/<feat>/test_<name>.py` | ☐ | ☐ | ☐ |

### TDD Exemptions

| Scope | Reason | Approved by |
| :--- | :--- | :--- |
| [e.g., external API call] | [Integration boundary] | [Owner] |

### Coverage Target

- Minimum: 90% line coverage for every PR after the project has an active implementation stack
- Base-template exception: `Project-Template` may have no coverage artifact while no active stack manifest exists
- Critical paths: [e.g., 100%]
- Measurement command: `pytest --cov=src/<feat> tests/<feat>/`

## TDD Auto-Link

Use this section to connect test strategy to execution tasks in `docs/04.execution/tasks/`.

| Task ID | Behavior | RED Test File | GREEN Evidence | REFACTOR Evidence | Exemption |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-001 | [Core behavior] | `tests/<feat>/test_<behavior>.py` | [command/log] | [command/log] | — |

Rules:

- Every core behavior must map to at least one execution task.
- RED evidence may be a failing test log, skipped test with reason, or expected failure marker.
- GREEN evidence must be a passing command or eval result.
- REFACTOR evidence must show the same behavioral checks still pass after cleanup.

## Test Matrix

| Test ID | Layer | Purpose | Input / Fixture | Expected Result | Automation |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | unit | [Purpose] | [Input] | [Result] | yes |

## Contract & Integration Tests

- **API contract checks**:
- **Consumer compatibility checks**:
- **Dependency integration checks**:

## Non-Functional Tests

- **Performance / latency**:
- **Reliability / retry**:
- **Security / abuse**:

## Agent Evals (If Applicable)

| Eval ID | Type | Scenario | Dataset / Prompt Set | Metric | Threshold |
| --- | --- | --- | --- | --- | --- |
| EVAL-001 | offline | [Scenario] | [Dataset] | [Metric] | [Threshold] |

## Fixtures / Datasets

- **Test fixtures**:
- **Eval datasets**:
- **Golden outputs**:

## How to Run

```bash
pytest tests/
npm test
python evals/run_feature_eval.py
```

## Evidence & Reporting

- **Where results are stored**:
- **Failure triage rule**:
- **Linked execution tasks**: `[../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md]`

## Target-Relative Link Guidance

- This file lives at `docs/03.specs/<feature-id>/tests.md`; sibling links use `./`.
- Link parent spec and companion contracts as `[./spec.md]`, `[./api-spec.md]`, and `[./domain-events.md]`.
- Link execution evidence as `[../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

- **Entry Gate**: parent Spec defines core behavior and risk targets.
- **Exit Gate**: TDD targets, exemptions, test matrix, and run commands are complete.
- **Hard Stop Conditions**: STOP if no parent Spec exists or core behaviors are not yet defined. STOP if TDD targets are empty and no exemption reason is provided for every behavior listed in the Spec.
- **Downstream Trigger**: `docs/04.execution/tasks/` records must reference RED/GREEN/REFACTOR evidence from this strategy.
- **Evidence Rule**: every core behavior maps to a task ID and command/eval evidence.

## Related Documents

- **Spec**: `[./spec.md]`
- **Tasks**: `[../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md]`
- **Plan**: `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`
