---
title: <string>
version: <string>
owner: <string>
layer: cross
stage: 04
status: draft
last-updated: YYYY-MM-DD
---

# Task List

<!-- Target: docs/04.execution/tasks/YYYY-MM-DD-<slug>.md -->

## Usage Guidance

- **When to use**: To track granular execution of an implementation plan.
- **Mandatory sections**: Task Table, TDD Evidence, Verification Summary.
- **Naming rule**: `YYYY-MM-DD-<slug>.md`.
- **Hard Stops**: STOP if TDD evidence (RED/GREEN/REFACTOR) is missing for `impl` tasks. STOP if `tests.md` is missing for `impl` streams.
- **Generation rule**: For derived-project seeds, keep `status: draft`, replace bracketed prompts with project facts or `TODO:`, and do not copy Project-Template maintenance tasks as active execution evidence.
- **Lifecycle reference**: Apply `docs/00.agent-governance/rules/template-document-lifecycle.md` before reusing inherited documents.

## Purpose

The Task List provides traceability-first tracking of execution. It ensures every logical change is verified via TDD or documented evidence.

---

## Overview (KR)

이 문서는 [기능 또는 작업 흐름명]의 구현·검증 작업 목록이다. Spec과 Plan에서 파생된 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Parent Plan**: `[../plans/YYYY-MM-DD-<feature>.md]`
- **Test Strategy**: `[../../03.specs/<feature-id>/tests.md]` — required for `impl` tasks; must exist before task execution begins

## Working Rules

- Write failing tests first for core behavior (RED phase).
- Every task must define evidence. No task may be closed without it.
- Documentation-only work still needs validation evidence.
- If a feature-local `tasks.md` exists under `03.specs/`, this document remains the execution-tracking source of truth.
- For `impl` tasks: either follow RED→GREEN→REFACTOR or fill TDD Exemption with one of:
  `external-integration` | `ui-exploratory` | `infra-setup` | `legacy-modification` (reason required).
- `ops` and `doc` type tasks are exempt by default; leave TDD Exemption as `—`.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | TDD Status             | TDD Exemption | Lint Gate     | Kanban Column | WIP # | Owner  | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ---------------------- | ------------- | ------------- | ------------- | ----- | ------ | ------ |
| T-001   | [Action]    | impl | SPC-001 / §2          | Phase 1             | `pytest ...`          | RED / GREEN / REFACTOR | —             | pre-commit ✅ | In Progress   | —     | [Name] | Todo   |

- **TDD Status**: `RED` (failing test written) → `GREEN` (test passes) → `REFACTOR` (cleanup, test still passes)
- **Kanban Column**: Todo / In Progress / Review / Done — **WIP #**: Work-in-progress limit slot (— if no WIP limit applies)

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [ ] T-001 — [Description] — TDD: RED ✓ / GREEN ✓ / REFACTOR ✓

### Phase 2

- [ ] T-002 — [Description] — TDD: RED ✓ / GREEN ✓ / REFACTOR ✓

## Verification Summary

- **Test Commands**:
- **Eval Commands**:
- **Logs / Evidence Location**:

## TDD Evidence Protocol

Use this section for each `impl` task unless a documented exemption applies.

| Phase    | Required Evidence                                               | Example                                                                      |
| :------- | :-------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| RED      | Failing test, expected failure, or skipped scaffold with reason | `pytest tests/<feat>/test_<behavior>.py -q` fails for the expected assertion |
| GREEN    | Passing test or eval result for the implemented behavior        | `pytest tests/<feat>/test_<behavior>.py -q` passes                           |
| REFACTOR | Same checks pass after cleanup                                  | `pytest tests/<feat>/test_<behavior>.py -q` passes after refactor            |

### Exemption Rules

- Valid reasons: `external-integration`, `ui-exploratory`, `infra-setup`, `legacy-modification`.
- Every exemption must include owner, rationale, alternative evidence, and review status.
- Documentation, operations, and pure governance tasks may use validation evidence instead of TDD evidence.

## Target-Relative Link Guidance

Keep placeholder paths as code spans until a generated document links to an existing file.

| Target Location                                | Governance Example                                       | Common Upstream/Downstream                                                  |
| ---------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------- |
| `docs/04.execution/tasks/YYYY-MM-DD-<slug>.md` | `[../../00.agent-governance/rules/stage-gate-matrix.md]` | `[../plans/YYYY-MM-DD-<slug>.md]`, `[../../03.specs/<feature-id>/tests.md]` |

## AI Execution Checklist

### Entry Gate

- [ ] Approved Spec and Plan links exist; `tests.md` is linked for all `impl` task streams.
- [ ] Every `impl` task has a TDD Status field (`RED` / `GREEN` / `REFACTOR` or documented exemption).

### Exit Gate

- [ ] Each task has status, owner, evidence, and TDD evidence or approved exemption.
- [ ] Verification Summary is populated with runnable commands.
- [ ] Phase View is updated to reflect actual completion state.

### Hard Stop Conditions

- **STOP** if no approved Spec and Plan links exist for any task stream.
- **STOP** if any `impl` task lacks a TDD Status (`RED`/`GREEN`/`REFACTOR`) or a documented exemption with reason, owner, and alternate evidence.
- **STOP** if `tests.md` does not exist for any `impl` task stream.
- **STOP** if validation evidence is undefined for any task.

### Downstream Trigger

- [ ] Update guides, operations, or runbooks when completed behavior changes user or operator workflows.

### Evidence Rule

- [ ] `impl` tasks MUST capture specific, non-empty RED/GREEN/REFACTOR log traces or test-run IDs.
- [ ] `doc`/`ops` tasks MUST record specific command output or reviewer links.

## Related Documents

- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Test Strategy**: `[../../03.specs/<feature-id>/tests.md]`
- **Plan**: `[../plans/YYYY-MM-DD-<feature>.md]`
