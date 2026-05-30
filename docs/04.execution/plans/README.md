---
title: Execution Plans Skeleton
version: 1.0.0
owner: Delivery Lead
layer: execution
stage: 04
status: active
last-updated: 2026-05-21
---

# Execution Plans Skeleton

> 새 프로젝트의 implementation plan을 작성하기 위한 release skeleton.

## Overview

`docs/04.execution/plans/`는 파생 프로젝트에서 non-trivial work를 시작하기 전 실행 계획을 보관하는 위치이다. `main` release branch에서는 Project-Template의 과거 plan 문서를 보관하지 않는다.

파생 프로젝트에서는 upstream PRD, ARD, spec, risk, validation command를 바탕으로 프로젝트별 plan을 작성한다.

아래 plan rows는 Project-Template 유지보수 이력이다. 새 프로젝트에서는 이 completed plan들을 복사하지 않고 `plan.template.md`에서 새 draft plan을 만든다.

## Audience

이 README의 주요 독자:

- Delivery leads
- Implementing engineers
- Reviewers
- AI agents

## Scope

The Plans layer bridges the gap between technical specification (Stage 04) and task-level execution (Stage 06). It represents Stage 05 in the stage-gate workflow even though it is stored under the compact `docs/04.execution/` folder. It defines the order of operations, dependency management, and verification strategies required to deliver a feature safely and efficiently.

### In Scope

- Project-specific execution plans
- Work breakdown, risks, validation plan, dependencies
- Links from plans to tasks and upstream specs

### Out of Scope

- Task execution logs
- Operations runbooks
- Incident records
- Template development plans

## Structure

```text
plans/
└── README.md    # Release skeleton guide for plan authoring
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- New plans must start from `docs/99.templates/plan.template.md`.

## Naming Rules

- Use `YYYY-MM-DD-<work-slug>.md`.
- Keep one cohesive work initiative per plan.
- Do not store task evidence in this folder.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- Plans start as `draft`.
- Plans become `active` only when scope, validation, risks, and dependencies are clear.
- Completed or abandoned plans must link to final tasks or closure notes.

## Cross-Reference Rules

- Every Plan must be linked in the [Documents](#documents) table below.
- Every Plan must have a `## Related Documents` section linking to parent Specs or Tests and downstream Tasks.
- Plans define what will be done and how it will be verified; task records own the actual evidence and closure state.

## Usage Examples

```bash
cp docs/99.templates/plan.template.md docs/04.execution/plans/YYYY-MM-DD-implementation-plan.md
```

## How to Work in This Area

1. Confirm upstream context and intake are complete.
2. Create the plan from the approved template.
3. Define validation before implementation begins.
4. Update this README when plan files are added, renamed, deprecated, or removed.

## AI Authoring Guidance

- Do not plan from missing requirements or unknown stack assumptions.
- Keep validation commands concrete and runnable.
- Do not keep Project-Template execution history on `main`.
- In a derived project, replace skeleton rows with real plan documents.

## AI Execution Checklist

- [ ] Upstream links are present.
- [ ] Plan uses `docs/99.templates/plan.template.md`.
- [ ] Validation and rollback criteria are explicit.
- [ ] Task links are added when execution starts.
- [ ] The `Documents` table reflects actual files in this folder.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [03.specs](../../03.specs/README.md) - Technical Specifications
- [04.execution/tasks](../tasks/README.md) - Implementation Tasks
- [05.operations/runbooks](../../05.operations/runbooks/README.md) - Operational Procedures

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
