---
title: Runbooks Skeleton
version: 1.0.0
owner: Operations Lead
layer: operations
stage: 05
status: active
last-updated: 2026-05-21
---

# Runbooks Skeleton

> 새 프로젝트의 executable operations procedures를 작성하기 위한 release skeleton.

## Overview

`docs/05.operations/runbooks/`는 파생 프로젝트에서 반복 가능한 운영 절차를 보관한다. `main` release branch에서는 video-analysis-specific runbook history를 보관하지 않는다.

파생 프로젝트에서는 실제 environments, deployment target, observability tools, escalation path에 맞게 runbook 절차를 작성한다.

## Audience

이 README의 주요 독자:

- Operators
- SRE and platform engineers
- Incident responders
- AI agents

## Scope

Runbooks provide deterministic, repeatable steps for common operational tasks
such as scaling, patching, database maintenance, and incident response procedures.
Unlike operation policies (Stage 08, which define targets and constraints), runbooks
are instructional — they describe exactly _how_ to execute a task safely.

This folder is stored under compact `docs/05.operations/`, but it represents
Stage 09 in the stage-gate workflow. The base template does not require
runbooks until a derived project has a Stage 08 policy or Stage 10 incident
anchor that needs repeatable operator steps.

### In Scope

- Step-by-step execution procedures for recurring operational tasks.
- Runbooks linked to a Stage 08 policy under `docs/05.operations/policies/` or triggered by a Stage 10 incident under `docs/05.operations/incidents/`.
- Verification steps confirming the procedure succeeded.

### Out of Scope

- General onboarding guides
- Formal policy statements without procedure
- Incident postmortems
- Template repository runbook history

## Structure

```text
runbooks/
└── README.md    # Release skeleton guide for runbook authoring
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- New runbooks must start from `docs/99.templates/runbook.template.md`.

## Naming Rules

- Use stable kebab-case names for durable procedures.
- Use `YYYY-MM-DD-<runbook-slug>.md` only for time-bound temporary procedures.
- Do not store policies or incident records here.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- Runbooks start as `draft`.
- Runbooks become `active` after steps, rollback, validation, and escalation are testable.
- Deprecated runbooks must link to replacements or explain removal.

## Cross-Reference Rules

- Link related policies, alerts, deployment docs, tasks, and incidents.
- Link rollback and escalation references directly from the runbook.

## Usage Examples

```bash
cp docs/99.templates/runbook.template.md docs/05.operations/runbooks/deploy-service.md
```

## How to Work in This Area

1. Confirm the procedure is repeatable and operational.
2. Create the runbook from the approved template.
3. Keep commands, preconditions, rollback, and validation explicit.
4. Update this README when runbook files are added, renamed, deprecated, or removed.

## AI Authoring Guidance

- Do not invent tools, dashboards, or deployment targets before intake confirms them.
- Do not keep video-analysis runbook history on `main`.
- In a derived project, align runbook steps with real operational tooling.

## AI Execution Checklist

- **Entry Gate**: A Stage 08 policy under `docs/05.operations/policies/` or Stage 10 incident under `docs/05.operations/incidents/` requiring a runbook exists.
- **Exit Gate**: Document index updated; runbook links to upstream policy or incident.
- **Hard Stop Conditions**: STOP if no upstream anchor (policy or incident) exists for this runbook.
- **Evidence Rule**: Every runbook must include verification steps executable by an agent or operator.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [05.operations/policies](../policies/README.md) — Operational Policies
- [05.operations/incidents](../incidents/README.md) — Incident Records

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
