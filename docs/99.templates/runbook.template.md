---
title: <string>
version: <string>
owner: <string>
layer: infra
stage: 05
status: draft
last-updated: YYYY-MM-DD
---

# Runbook

<!-- Target: docs/05.operations/runbooks/####-<topic>.md -->

## Usage Guidance

- **When to use**: For immediate execution of operational tasks, recovery, or maintenance.
- **Mandatory sections**: Overview, Procedure or Checklist, Verification, Rollback.
- **Naming rule**: `####-<topic>.md`.
- **Hard Stops**: STOP if rollback steps are missing. STOP if no operations policy exists for this scope.
- **Generation rule**: For derived-project seeds, keep `status: draft`, replace bracketed prompts with project facts or `TODO:`, and do not copy Project-Template maintenance runbooks as active operational procedures.
- **Lifecycle reference**: Apply `docs/00.agent-governance/rules/template-document-lifecycle.md` before reusing inherited documents.

## Purpose

The Runbook provides exact, step-by-step procedures for operational tasks. It is designed for reliability and speed during execution.

---

## Overview (KR)

이 런북은 [서비스 또는 워크플로명]에 대한 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공한다.

## Objectives

[What operational problem this runbook addresses.]

## Canonical References

- `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- `[../../02.architecture/decisions/####-<short-title>.md]`
- `[../../03.specs/<feature-id>/spec.md]`
- `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`

## When to Use

- [Use case 1]
- [Use case 2]

## Procedure or Checklist

### Checklist

- [ ] [Check 1]
- [ ] [Check 2]

### Procedure

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Verification Steps

- [ ] [Verification command or manual check]

## Observability and Evidence Sources

- **Signals**:
- **Evidence to Capture**:

## Safe Rollback or Recovery Procedure

- [ ] [Recovery step 1]
- [ ] [Recovery step 2]

## Agent Operations (If Applicable)

- **Prompt Rollback**:
- **Model Fallback**:
- **Tool Disable / Revoke**:
- **Eval Re-run**:
- **Trace Capture**:

## Escalation Path

| Condition | Action | Contact |
| --- | --- | --- |
| [Condition 1, e.g., recovery fails after 2 retries] | [Action, e.g., page on-call lead] | [Contact, e.g., #ops-oncall] |
| [Condition 2, e.g., data loss suspected] | [Action, e.g., halt and escalate] | [Contact, e.g., eng-lead + security] |

## Related Operational Documents

- **Incident examples**: `[../incidents/YYYY/INC-###-<incident-title>/record.md]`
- **Postmortem examples**: `[../incidents/YYYY/INC-###-<incident-title>/postmortem.md]`

## Target-Relative Link Guidance

- This file lives under `docs/05.operations/runbooks/`; sibling operations links use `../`.
- Link upstream architecture/spec/plan context as `[../../02.architecture/requirements/####-<system-or-domain>.md]`, `[../../03.specs/<feature-id>/spec.md]`, and `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`.
- Link policies and incidents as `[../policies/<policy-or-standard>.md]` and `[../incidents/YYYY/INC-###-<incident-title>/record.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

- **Entry Gate**: operation policy or known risk requires executable recovery steps.
- **Exit Gate**: diagnostics, mitigation, rollback, escalation, and verification steps are complete.
- **Hard Stop Conditions**: STOP if no operations policy document (`docs/05.operations/policies/`) exists for the scope this runbook executes. STOP if rollback or recovery steps reference undocumented or unverified system behavior.
- **Downstream Trigger**: link from incident records and update after postmortem actions.
- **Evidence Rule**: MUST capture specific dry-run output, command transcript logs, or reviewer sign-off artifacts.

## Related Documents

- **Operation**: `[../policies/<policy-or-standard>.md]`
- **Incident Record**: `[../incidents/YYYY/INC-###-<incident-title>/record.md]`
- **Postmortem**: `[../incidents/YYYY/INC-###-<incident-title>/postmortem.md]`
