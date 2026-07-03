---
title: Operations Guides Skeleton
version: 1.0.0
owner: Operations Lead
layer: operations
stage: 05
status: active
last-updated: 2026-05-21
---

# Operations Guides Skeleton

> 새 프로젝트의 human-readable operations guide를 작성하기 위한 release skeleton.

## Overview

`docs/05.operations/guides/`는 파생 프로젝트의 사용자, 운영자, agent가 안정적인 절차와 사용법을 이해하도록 돕는 guide를 보관한다. `main` release branch에서는 video-analysis onboarding guide나 walkthrough history를 보관하지 않는다.

파생 프로젝트에서는 실제 product/software, stack, environments, release model에 맞게 guide 문서를 작성한다.

아래 onboarding guides는 video-analysis 사용법을 설명하는 `active-template-contract`다. 새 프로젝트에서는 product/operator guide가 필요할 때 `guide.template.md`에서 새 문서를 만든다.

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Support or onboarding owners
- AI agents

## Scope

The Guides layer is dedicated to accessibility and knowledge transfer. It transforms technical features into understandable workflows, tutorials, and references. This ensures that anyone—whether a new developer, an end-user, or a freshly initialized AI agent—can effectively interact with the system.

This folder is stored under compact `docs/05.operations/`, but it represents
Stage 07 in the stage-gate workflow. The base template does not create product
guides by default; write guides only after behavior is stable and linked to
specification or Stage 06 task evidence.

### In Scope

- Project-specific usage, onboarding, operations, and support guides
- Stable behavior and procedure explanations
- Links to runbooks, policies, plans, and tasks

### Out of Scope

- Executable incident response procedures
- Formal operational policies
- Task evidence logs
- Template repository walkthroughs

## Structure

```text
guides/
└── README.md    # Release skeleton guide for guide authoring
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- New guides must start from `docs/99.templates/guide.template.md`.

## Naming Rules

- Evergreen guides: `<slug>.md`
- Dated or historical guides and walkthroughs: `YYYY-MM-DD-<slug>.md`
- Do not rename existing guide files just to match a newer naming pattern.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- Guides start as `draft`.
- Guides become `active` after audience, prerequisites, and stable behavior are clear.
- Deprecated guides must link to replacements or explain removal.

## Cross-Reference Rules

- Every Guide must be linked in the [Documents](#documents) table below.
- Every Guide should link back to the relevant Stage 04 Spec under `docs/03.specs/` or Stage 06 task evidence under `docs/04.execution/tasks/`.

## Usage Examples

```bash
cp docs/99.templates/guide.template.md docs/05.operations/guides/YYYY-MM-DD-operator-guide.md
```

## How to Work in This Area

1. Confirm the guide belongs in operations rather than requirements/specs.
2. Create the guide from the approved template.
3. Keep instructions stable and project-specific.
4. Update this README when guide files are added, renamed, deprecated, or removed.

## AI Authoring Guidance

- Do not write generic template history as an operations guide.
- Do not describe missing project infrastructure as if it exists.
- In a derived project, rewrite skeleton wording to match real users, tools, and workflows.

## AI Execution Checklist

- **Entry Gate**: Feature implementation is complete with Stage 06 task evidence under `docs/04.execution/tasks/`, and the need for documentation is identified.
- **Exit Gate**: Document index is updated, and all links to specs/implementation are verified.
- **Hard Stop Conditions**: STOP if the document index cannot be reconciled with folder contents.
- **Evidence Rule**: Every guide must be verified against the actual implementation.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [03.specs](../../03.specs/README.md) - Technical Specifications
- [05.operations/runbooks](../runbooks/README.md) - Operational Procedures
- root `README.md` - Project Entry Point

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
