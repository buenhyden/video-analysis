---
title: Operations Policies Skeleton
version: 1.0.0
owner: Operations Lead
layer: operations
stage: 05
status: active
last-updated: 2026-05-21
---

# Operations Policies Skeleton

> 새 프로젝트의 operational policy와 SLO를 작성하기 위한 release skeleton.

## Overview

`docs/05.operations/policies/`는 파생 프로젝트의 operational controls, SLO, release policy, resilience policy를 보관한다. `main` release branch에서는 video-analysis SLO나 운영 정책 이력을 보관하지 않는다.

파생 프로젝트에서는 operations intake, architecture decisions, deployment target, observability baseline에 맞게 정책 문서를 작성한다.

아래 정책 rows는 video-analysis 운영 기준과 evidence package history다. 새 프로젝트의 SLO나 resilience policy는 intake가 필요성을 선언한 뒤 새로 작성한다.

## Audience

이 README의 주요 독자:

- Operations leads
- SRE and platform engineers
- Security and compliance reviewers
- AI agents

## Scope

The Operations layer establishes the "Guardrails" for running the system in production. It focuses on reliability, security, and maintenance policies. Unlike runbooks (which are instructional), operation documents are policy-driven, defining the targets (e.g., 99.9% uptime) and the constraints (e.g., backup frequency).

This folder is stored under compact `docs/05.operations/`, but it represents
Stage 08 in the stage-gate workflow. The base template stays stack-neutral:
write policy or SLO documents only when a derived project has operational
requirements, controls, or service objectives to govern.

### In Scope

- Project-specific operational policies
- SLO and reliability controls when required by intake
- Release, observability, backup, escalation, resilience criteria

### Out of Scope

- Step-by-step runbooks
- Incident timelines or postmortems
- Product requirements
- Template repository SLO history

## Structure

```text
policies/
└── README.md    # Release skeleton guide for policy authoring
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- [operation.template.md](../../99.templates/operation.template.md) - Standard operations policy template.
- [slo.template.md](../../99.templates/slo.template.md) - Service level objective template for explicit SLI/SLO policy.

## Naming Rules

- Policies: `<slug>.md`
- Approved policy packages may exist only when registered in the documentation protocol.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- Policies start as `draft`.
- Policies become `active` after owner, controls, promotion criteria, and validation are clear.
- Superseded policies must link to replacements.

## Cross-Reference Rules

- Every Operation policy must be linked in the [Documents](#documents) table below.
- Every Operation policy must link to the relevant Stage 09 runbooks under `docs/05.operations/runbooks/` and SLI/SLO dashboards or monitoring evidence.

## Usage Examples

```bash
cp docs/99.templates/operation.template.md docs/05.operations/policies/YYYY-MM-DD-release-policy.md
cp docs/99.templates/slo.template.md docs/05.operations/policies/YYYY-MM-DD-service-slo.md
```

## How to Work in This Area

1. Confirm operations intake fields and ownership.
2. Choose operation or SLO template based on policy type.
3. Define controls, measurement, validation, and escalation.
4. Update this README when policy files are added, renamed, deprecated, or removed.

## AI Authoring Guidance

1. **Phase 0: Metric**: Identify the core metric (SLI) and target (SLO).
2. **Phase 1: Constraint**: Define the boundaries and guardrails for operation.
3. **Phase 2: Link**: Ensure the policy links to relevant Stage 09 runbooks under `docs/05.operations/runbooks/`.
4. **Phase 3: Finalize**: Update index and set `status: active`.

## AI Execution Checklist

- [ ] Operations baseline and owner are known.
- [ ] Policy uses the approved template.
- [ ] Controls and validation criteria are explicit.
- [ ] Related runbooks/incidents/tasks are linked.
- [ ] The `Documents` table reflects actual files in this folder.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [02.architecture/requirements](../../02.architecture/requirements/README.md) - Architecture Reference
- [05.operations/runbooks](../runbooks/README.md) - Operational Procedures
- [05.operations/incidents](../incidents/README.md) - Incident Records

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
