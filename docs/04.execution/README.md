---
title: Execution Skeleton
version: 1.0.0
owner: Delivery Lead
layer: execution
stage: 04
status: active
last-updated: 2026-05-21
---

# Execution Skeleton

> 새 프로젝트의 execution plans와 task evidence를 작성하기 위한 release skeleton.

## Overview

This hub owns execution planning and task-level validation evidence in the
compact docs model. It replaces the former separate top-level plan and task
folders. Although this path is `docs/04.execution/`, its subfolders preserve
the stage-gate workflow boundary: `plans/` stores Stage 05 execution plans and
`tasks/` stores Stage 06 task evidence.

`dev` may contain completed Project-Template plans and task evidence for
traceability. Those records are `template-maintenance`, not execution seeds for
new projects. `main` keeps only the README skeleton guides.

## Audience

- Delivery leads
- Engineers executing approved specs
- QA inspectors validating task evidence
- AI agents preparing plans or execution records

## Scope

### In Scope

- Stage 05 execution plans under `plans/`.
- Stage 06 execution, verification, and task evidence records under `tasks/`.

### Out of Scope

- Product requirements or architecture decisions
- Long-lived operations procedures
- Incident postmortems
- Project-Template development history

## Structure

```text
04.execution/
├── plans/      # Execution plan skeleton
├── tasks/      # Execution task evidence skeleton
└── README.md   # This file
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- Execution plans must start from `docs/99.templates/plan.template.md`.
- Execution tasks must start from `docs/99.templates/task.template.md`.

## Naming Rules

- Use `YYYY-MM-DD-<work-slug>.md` for plans and tasks.
- Keep planning documents in `plans/`.
- Keep task execution and validation evidence in `tasks/`.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- Plans and tasks start as `draft`.
- A task can be closed only when validation evidence is recorded.
- Completed work should keep links to the governing plan and upstream spec.
- On `main`, this folder remains a skeleton until a derived project creates project-specific execution records.

## Cross-Reference Rules

- Every plan must link to parent requirements, specs, or decisions and define runnable validation.
- Every task record must link to its parent plan, relevant spec or test strategy, and validation evidence.

## Usage Examples

```bash
cp docs/99.templates/plan.template.md docs/04.execution/plans/YYYY-MM-DD-implementation-plan.md
cp docs/99.templates/task.template.md docs/04.execution/tasks/YYYY-MM-DD-implementation-task.md
```

## How to Work in This Area

1. Confirm intake and upstream stage documents exist.
2. Create or update a plan before non-trivial implementation.
3. Record task evidence as work proceeds.
4. Update child README `Documents` tables when plan/task files change.
5. Run the relevant validation gate before closing work.

## AI Authoring Guidance

- Do not create execution records before intake and upstream context exist.
- Do not mark work complete without validation evidence.
- Do not keep Project-Template task history in the release skeleton.
- In a derived project, rewrite skeleton rows to match actual project work.

## AI Execution Checklist

- [ ] Upstream PRD/ARD/spec links are identified.
- [ ] Plan/task documents use approved templates.
- [ ] Validation commands and results are captured in tasks.
- [ ] Operations follow-up is linked when needed.
- [ ] The `Documents` table reflects actual child folders and files.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [plans](./plans/) | package | Execution plan seed guide plus dev-only template maintenance plans | project-seed | 2026-05-21 |
| [tasks](./tasks/) | package | Task evidence seed guide plus dev-only template maintenance tasks | project-seed | 2026-05-21 |

## Related Documents

- [01.requirements](../01.requirements/README.md) - Product requirements
- [02.architecture](../02.architecture/README.md) - Architecture requirements and decisions
- [03.specs](../03.specs/README.md) - Technical specifications

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
