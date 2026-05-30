---
title: <string>
version: <string>
owner: <string>
layer: infra
stage: 05
status: draft
last-updated: YYYY-MM-DD
---

# Postmortem

<!-- Target: docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md -->

## Usage Guidance

- **When to use**: After an incident is resolved to analyze root causes and prevent recurrence.
- **Mandatory sections**: Overview, Summary, Root Cause Analysis, Action Items.
- **Naming rule**: `postmortem.md` (within an incident-specific directory).
- **Hard Stops**: STOP if the incident is not yet resolved. STOP if root cause analysis lacks evidence.
- **Derived-project seed rule**: Create only after a corresponding incident record exists and the incident is resolved or stabilized.

## Purpose

The Postmortem provides a blameless analysis of an incident. It identifies the systemic causes and the actions required to improve reliability and prevent future occurrences.

---

## Overview (KR)

이 문서는 사고의 구조적 원인과 재발 방지 조치를 분석하는 Postmortem 문서다. 비난 없는 분석과 시스템 개선에 집중한다.

## Incident Summary

| Field | Value |
| --- | --- |
| Incident ID | `INC-YYYYMMDD-XXX` |
| Incident Date | `YYYY-MM-DD` |
| Analysis Date | `YYYY-MM-DD` |
| Severity | `SEV-1 / SEV-2 / SEV-3` |
| Incident Document | `[./record.md]` |

## Agent Metadata (If Applicable)

- **Model Version**:
- **Prompt Version**:
- **Tool Set / Config**:
- **Guardrail State**:
- **Trace IDs**:
- **Eval Run IDs**:

## Impact

- **Affected Users or Systems**:
- **Operational Impact**:
- **Business / Maintenance Impact**:

## Timeline

| Time (UTC) | Event |
| --- | --- |
| HH:MM | [Detection / investigation / mitigation / resolved] |

## Root Cause Analysis

### Primary Root Cause

[Systemic cause.]

### Contributing Factors

- [Factor 1]
- [Factor 2]

### Detection Gaps

- [Gap 1]
- [Gap 2]

## What Went Well

- [Point 1]

## What Went Wrong

- [Point 1]

## Action Items

| Action | Owner | Priority | Ticket / Reference | Status |
| --- | --- | --- | --- | --- |
| [Action item] | [Name] | High | [Link] | Pending |

## Prevention and Verification

- [Prevention work]
- [Verification rule]

## Target-Relative Link Guidance

- This file lives at `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md`.
- Link the factual incident record as `[./record.md]`.
- Link runbooks and policies three levels up: `[../../../runbooks/####-<topic>.md]` and `[../../../policies/<policy-or-standard>.md]`.
- Keep corrective execution links target-relative, for example `[../../../../04.execution/tasks/YYYY-MM-DD-<follow-up>.md]` only if that target exists.
- Keep placeholder paths as code spans until the generated target exists.

## Required Documentation Feedback Loop

- **ADR updates**:
- **Spec updates**:
- **Operation updates**:
- **Runbook updates**:
- **Guardrail / Eval updates**:

## AI Execution Checklist

- **Entry Gate**: incident is resolved or stabilized and factual record exists.
- **Exit Gate**: root cause, contributing factors, impact, actions, owners, and due dates are complete.
- **Hard Stop Conditions**: STOP if no corresponding incident `record.md` exists or if the incident is not yet in `Resolved` or `Closed` state. STOP if root cause conclusion is stated as confirmed fact without supporting evidence from logs, metrics, or timeline.
- **Downstream Trigger**: update ADR/Spec/Operation/Runbook/Task artifacts for corrective actions.
- **Evidence Rule**: MUST cite specific incident logs, timeline artifacts, metric snapshots, or review meeting notes.

## Related Documents

- **Runbook**: `[../../../runbooks/####-<topic>.md]`
- **Operation**: `[../../../policies/<policy-or-standard>.md]`
- **Incident Record**: `[./record.md]`
