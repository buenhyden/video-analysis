---
title: Incidents Skeleton
version: 1.0.0
owner: Operations Lead
layer: operations
stage: 05
status: active
last-updated: 2026-05-21
---

# Incidents Skeleton

> 새 프로젝트의 incident record와 postmortem을 작성하기 위한 release skeleton.

## Overview

`docs/05.operations/incidents/`는 파생 프로젝트에서 incident records와 postmortems를 보관한다. `main` release branch에서는 Project-Template incident history나 retrospective 자료를 보관하지 않는다.

파생 프로젝트에서는 실제 영향, timeline, response, root cause, corrective actions, follow-up ownership을 프로젝트 맥락에 맞게 기록한다.

## Audience

이 README의 주요 독자:

- Incident commanders
- Operators
- Engineering and reliability reviewers
- AI agents

## Scope

The Incidents layer is the system's "Black Box". It records what went wrong, how the system was restored, and why it failed. It is divided into active Incident Records (the "What") and Postmortems (the "Why").

This folder is stored under compact `docs/05.operations/`, but it represents
Stage 10 in the stage-gate workflow. Incident records capture operational
facts and learning; follow-up prevention work routes back into Stage 05
execution plans under `docs/04.execution/plans/` and Stage 06 task evidence
under `docs/04.execution/tasks/`.

### In Scope

- Project-specific incident records
- Postmortems, timelines, impact, action items, follow-up ownership
- Links to runbooks, policies, tasks, and affected specs

### Out of Scope

- General operations guides
- Runbook procedure definitions
- Product requirements
- Template repository incident history

## Structure

```text
incidents/
└── README.md    # Release skeleton guide for incident authoring
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- Incident records use `docs/99.templates/incident.template.md`.
- Postmortems use `docs/99.templates/postmortem.template.md`.

## Naming Rules

- Use `YYYY-MM-DD-<incident-slug>.md`.
- Keep one incident or postmortem per file.
- Do not store runbooks or policies here.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- Incident records start as `draft`.
- Incident records become `completed` only after impact, timeline, response, action items, and ownership are recorded.
- Follow-up items must link to execution tasks or policy/runbook updates.

## Cross-Reference Rules

- Every Incident must be linked in the [Documents](#documents) table below.
- Every Incident Record must link to the relevant Stage 09 runbook under `docs/05.operations/runbooks/`.
- Every Postmortem must link to follow-up Stage 06 task evidence under `docs/04.execution/tasks/`.

## Usage Examples

```bash
cp docs/99.templates/incident.template.md docs/05.operations/incidents/YYYY-MM-DD-service-outage.md
cp docs/99.templates/postmortem.template.md docs/05.operations/incidents/YYYY-MM-DD-service-outage-postmortem.md
```

## How to Work in This Area

1. Confirm an incident or learning record belongs here.
2. Create the record from the approved template.
3. Capture facts, timeline, impact, response, and follow-up ownership.
4. Update this README when incident files are added, renamed, deprecated, or removed.

## AI Authoring Guidance

1. **Phase 0: Triage**: Create `record.md` immediately. Document facts and timeline.
2. **Phase 1: Recovery**: Record exact remediation steps taken.
3. **Phase 2: RCA**: Conduct a blameless Postmortem (`postmortem.md`).
4. **Phase 3: Prevention**: Map action items to Stage 05 execution plans under `docs/04.execution/plans/` or Stage 06 task evidence under `docs/04.execution/tasks/`.

## AI Execution Checklist

- **Entry Gate**: A system anomaly or disruption is detected and confirmed.
- **Exit Gate**: Document index is updated, and all follow-up plans or tasks are initialized under `docs/04.execution/`.
- **Hard Stop Conditions**: STOP if the document index cannot be reconciled with folder contents.
- **Evidence Rule**: Every postmortem must be based on the facts recorded in the incident record.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [05.operations/runbooks](../runbooks/README.md) - Operational Procedures
- [05.operations/policies](../policies/README.md) - Operational Policies
- [00.agent-governance/memory/](../../00.agent-governance/memory/) - Technical Insights

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
