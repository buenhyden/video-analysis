---
title: <string>
version: <string>
owner: <string>
layer: infra
stage: 05
status: draft
last-updated: YYYY-MM-DD
---

# Incident Record

<!-- Target: docs/05.operations/incidents/YYYY/INC-###-<incident-title>/record.md -->

## Usage Guidance

- **When to use**: To record facts, status, and response state during and after an incident.
- **Mandatory sections**: Overview, Metadata, Timeline, Impact, Follow-up Actions.
- **Naming rule**: `record.md` (within an incident-specific directory).
- **Hard Stops**: STOP if severity or primary service is undefined. STOP if closing without impact assessment.
- **Derived-project seed rule**: Create only for a real declared incident or drill; do not include placeholder incidents in a fresh project.

## Purpose

The Incident Record documents the detection, investigation, and resolution of an operational event. It focuses on facts and the timeline to support eventual postmortem analysis.

---

## Overview (KR)

이 문서는 사고의 영향, 현재 상태, 주요 대응 흐름을 기록하는 Incident 문서다. 사실 기록과 대응 로그에 집중한다.

## Incident Metadata

| Field | Value |
| --- | --- |
| Incident ID | `INC-YYYYMMDD-XXX` |
| Severity | `SEV-1 / SEV-2 / SEV-3` |
| Status | `Investigating / Mitigating / Monitoring / Resolved / Closed` |
| Detection Time | `YYYY-MM-DD HH:MM UTC` |
| Primary Service | [Affected service] |
| Evidence Source | [Log / dashboard / report] |
| Runbook Link | `[../../../runbooks/####-<topic>.md]` |

## Agent Metadata (If Applicable)

- **Model Version**:
- **Prompt Version**:
- **Tool Set / Config**:
- **Guardrail State**:
- **Trace IDs**:
- **Eval Run IDs**:

## Incident Summary

[Short summary.]

## Impact

- [Impact 1]
- [Impact 2]

## Timeline

| Time (UTC) | Actor | Detail |
| --- | --- | --- |
| HH:MM | [Name] | [What happened] |

## Current Hypothesis / Response State

- **Current Hypothesis**:
- **Mitigation Actions**:
- **Resolution State**:

## Evidence

- [Evidence 1]
- [Evidence 2]

## Target-Relative Link Guidance

- This file lives at `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/record.md`.
- Link runbooks and policies three levels up: `[../../../runbooks/####-<topic>.md]` and `[../../../policies/<policy-or-standard>.md]`.
- Link the companion postmortem as `[./postmortem.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

- **Entry Gate**: incident is detected or declared with severity and primary service.
- **Exit Gate**: impact, timeline, response state, evidence, and follow-up actions are complete.
- **Hard Stop Conditions**: STOP if incident severity and primary service are undefined. STOP if closing the record without confirmed impact assessment or at least one follow-up action assigned.
- **Downstream Trigger**: create `postmortem.md` for severity threshold or recurring incident patterns.
- **Evidence Rule**: MUST link specific logs, traces, or metric snapshots that distinguish confirmed facts from hypotheses.

## Follow-up Actions

- [ ] [Action] — Owner: [Name]

## Postmortem Link

- `[./postmortem.md]`

## Related Documents

- **Runbook**: `[../../../runbooks/####-<topic>.md]`
- **Operation**: `[../../../policies/<policy-or-standard>.md]`
- **Postmortem**: `[./postmortem.md]`
