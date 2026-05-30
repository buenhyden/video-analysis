---
title: Architecture Reference Documents Index
version: 1.0.0
owner: System Architect
layer: architecture
stage: 02
status: active
last-updated: 2026-05-21
---

# Architecture Requirements Skeleton

> 새 프로젝트의 ARD를 작성하기 위한 release skeleton.

## Overview

`docs/02.architecture/requirements/`는 파생 프로젝트의 architecture requirements document를 보관한다. `main` release branch에서는 실제 ARD가 없어야 하며, 이 README만 새 프로젝트 authoring guide로 남긴다.

파생 프로젝트에서는 intake, PRD, stack 결정을 바탕으로 quality attributes, C4 context, deployment baseline, data boundaries, security assumptions를 프로젝트에 맞게 작성한다.

아래 `Documents` 표의 existing ARD와 research package는 `dev` 유지용 Project-Template architecture history다. 새 프로젝트에서는 이 문서를 복사하지 않고 `ard.template.md`에서 새 draft ARD를 만든다.

## Audience

이 README의 주요 독자:

- System architects
- Engineering leads
- Security and operations reviewers
- AI agents

## Scope

The ARD layer establishes the technical foundation and constraints of the
system. It defines "How" product requirements will be structured at a high
level, covering system boundaries, component relationships, data flow, quality
attributes, C4 diagrams, and Domain-Driven Design (DDD) strategy.

Use an ARD when the durable question is "what are the system boundaries and
architecture requirements?" Use an ADR when the durable question is "which
architecture choice did we accept and why?"

### In Scope

- High-level architecture blueprints (C4 Model Level 1 & 2).
- DDD Strategic Modeling (Subdomains, Bounded Contexts, Context Maps).
- Quality Attribute Scenarios (Performance, Security, Scalability).
- System boundary definitions and external integrations.
- Repository-governance architecture when it defines durable workspace
  structure or validation boundaries.

### Out of Scope

- Specific tech stack decisions (see `docs/02.architecture/decisions/`).
- Component-level details and internal logic (see `docs/03.specs/`).
- Product vision (see `docs/01.requirements/`).
- Execution sequencing, validation logs, or task evidence (see
  `docs/04.execution/`).

## Structure

- `README.md` - Folder contract and index.
- Child files and folders listed in the Documents table.

## How to Work in This Area

1. Confirm the artifact is an ARD, not an ADR, Spec, Plan, or Task.
2. Use the matching template from `docs/99.templates/`.
3. Update this README after files change.
4. Run the relevant documentation validation gate.

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- New ARD documents must start from `docs/99.templates/ard.template.md`.

## Naming Rules

- Use `YYYY-MM-DD-<architecture-slug>.md`.
- Keep one coherent architecture baseline per document.
- Do not mix ADR decision records into this folder.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- New ARDs start as `draft`.
- ARDs become `active` only after intake, PRD, and stack assumptions are reviewable.
- Superseded ARDs must link to the newer architecture baseline.

## Cross-Reference Rules

- Every ARD must be linked in the [Documents](#documents) table below.
- Every ARD must have a `## Related Documents` section linking to parent PRDs and downstream Specs/ADRs.
- Strategic DDD documents should be linked in the ARD's `## Related Documents`.
- Missing planned downstream artifacts must be named as inline text with
  rationale, not linked as Markdown paths.

## Usage Examples

- Create a new architecture reference from `ard.template.md` after a PRD establishes product intent.
- Place supporting research in `research/` only when it is referenced by an ARD or downstream spec.
- Keep C4 Context and C4 Container diagrams in the ARD when the system has
  multiple durable components.

## AI Authoring Guidance

1. **Phase 0: Context**: Read the upstream PRD and existing ARDs.
2. **Phase 1: Blueprint**: Define system boundaries and core components.
3. **Phase 2: DDD**: If triggers fire, populate Bounded Context and Ubiquitous Language documents.
4. **Phase 3: Validation**: Ensure C4 diagrams are included for complex systems. Update index and set `status: active`.
5. **Routing Check**: Move implementation details to Stage 03 and evidence logs
   to Stage 04 before closing.

## AI Execution Checklist

- [ ] Intake and PRD links are available.
- [ ] ARD uses `docs/99.templates/ard.template.md`.
- [ ] Quality attributes and constraints are explicit.
- [ ] Related ADR/spec links are maintained.
- [ ] The `Documents` table reflects actual files in this folder.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [01.requirements](../../01.requirements/README.md) - Product Requirements
- [02.architecture/decisions](../decisions/README.md) - Architecture Decision Records
- [03.specs](../../03.specs/README.md) - Technical Specifications

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
