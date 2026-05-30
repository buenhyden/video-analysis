---
title: Execution Tasks Skeleton
version: 1.0.0
owner: Delivery Lead
layer: execution
stage: 04
status: active
last-updated: 2026-05-21
---

# Execution Tasks Skeleton

> 새 프로젝트의 task execution과 validation evidence를 기록하기 위한 release skeleton.

## Overview

`docs/04.execution/tasks/`는 파생 프로젝트에서 실제 구현, 검증, evidence를 기록하는 위치이다. `main` release branch에서는 기존 Project-Template task history를 보관하지 않는다.

파생 프로젝트에서는 plan, spec, implementation change, validation output을 연결해 task 문서를 작성한다.

아래 task rows는 Project-Template 유지보수 evidence다. 새 프로젝트에서는 이 completed task evidence를 복사하지 않고 `task.template.md`에서 새 draft task record를 만든다.

## Audience

이 README의 주요 독자:

- Implementing engineers
- QA reviewers
- Delivery leads
- AI agents

## Scope

The Tasks layer is the active record of work being performed. It breaks down implementation into manageable units and provides a verifiable log of the TDD (Test-Driven Development) cycle (RED-GREEN-REFACTOR). This ensures that all code changes are backed by evidence of testing and quality assurance.

This folder represents Stage 06 in the stage-gate workflow even though it is stored under the compact `docs/04.execution/` folder. Implementation tasks require RED/GREEN/REFACTOR evidence; documentation, operations, and validation-only tasks record command evidence and explicit exemption rationale instead.

### In Scope

- Detailed task tracking for implementation and refactoring.
- TDD Execution Evidence (Test output, screenshots, recordings).
- RED-GREEN-REFACTOR cycle logs.
- Bug fix records and regression evidence.
- Documentation-only, operations, or validation task records with command evidence.

### Out of Scope

- High-level plans without execution evidence
- Product requirements or architecture decisions
- Long-lived runbooks
- Template repository task history

## Structure

```text
tasks/
└── README.md    # Release skeleton guide for task authoring
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- New task records must start from `docs/99.templates/task.template.md`.

## Naming Rules

- Use `YYYY-MM-DD-<task-slug>.md`.
- Keep task scope small enough to review independently.
- Do not mix unrelated implementation evidence in one task file.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- Tasks start as `draft`.
- Tasks become `completed` only when validation evidence is recorded.
- Blocked tasks must identify the blocker and next sync point.

## Cross-Reference Rules

- Every Task must be linked in the [Documents](#documents) table below.
- Every Task must have a `## Related Documents` section linking to parent Plans and relevant Specs, Tests, commits, or PRs when they exist.
- Task records own actual command output, validation summaries, and closure state; plans own sequencing and intended verification.

## Usage Examples

```bash
cp docs/99.templates/task.template.md docs/04.execution/tasks/YYYY-MM-DD-implementation-task.md
```

## How to Work in This Area

1. Confirm the owning plan exists or explain why the task is trivial.
2. Create the task from the approved template.
3. Record validation evidence before closure.
4. Update this README when task files are added, renamed, deprecated, or removed.

## AI Authoring Guidance

- Do not mark a task complete without evidence.
- Do not preserve Project-Template task history in a release skeleton.
- Keep task rows aligned with actual files.
- In a derived project, rewrite skeleton rows to match real project execution.

## AI Execution Checklist

- [ ] Owning plan or trivial-work rationale is linked.
- [ ] Task uses `docs/99.templates/task.template.md`.
- [ ] Validation evidence is recorded.
- [ ] Follow-up operations docs are linked when needed.
- [ ] The `Documents` table reflects actual files in this folder.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [04.execution/plans](../plans/README.md) - Execution Plans
- [03.specs](../../03.specs/README.md) - Technical Specifications
- [README.md](../../../README.md) - Root workspace overview

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
