---
title: Architecture Skeleton
version: 1.0.0
owner: System Architect
layer: architecture
stage: 02
status: active
last-updated: 2026-05-21
---

# Architecture Skeleton

> 새 프로젝트의 architecture requirements와 decision records를 작성하기 위한 release skeleton.

## Overview

This hub owns architecture requirement documents and architecture decision
records. Use it to answer architecture-level questions before a feature moves
into detailed specification or execution planning.

The Stage 02 split is intentional:

- `requirements/` stores Architecture Reference Documents (ARDs): system
  boundaries, quality attributes, context diagrams, and DDD strategy.
- `decisions/` stores Architecture Decision Records (ADRs): accepted or
  deprecated choices, alternatives, consequences, and rationale.
- Implementation design belongs in `docs/03.specs/`; work breakdown and
  validation evidence belong in `docs/04.execution/`.

`dev`의 ARD/ADR 문서는 Project-Template architecture contract 또는 archive/reference history다. 파생 프로젝트에서는 intake와 PRD가 준비된 뒤 matching template에서 새 ARD/ADR을 생성한다.

## Audience

- System architects
- Technical leads
- AI agents preparing architecture or decision records
- Reviewers validating downstream spec readiness

## Scope

### In Scope

- Architecture requirements under `requirements/`.
- Architecture decisions under `decisions/`.
- Research artifacts that support architecture requirements.
- Architecture-level routing guidance that helps agents choose ARD, ADR, Spec,
  Plan, or Task locations correctly.

### Out of Scope

- Product requirements, which belong in `docs/01.requirements/`.
- Feature specifications, which belong in `docs/03.specs/`.
- Execution plans and task evidence, which belong in `docs/04.execution/`.
- Runtime policy, which belongs in `docs/00.agent-governance/` and provider
  surfaces.

## Structure

```text
02.architecture/
├── decisions/      # Architecture Decision Records
├── requirements/   # Architecture Reference Documents
└── README.md       # This file
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- Architecture requirements must start from `docs/99.templates/ard.template.md`.
- Architecture decisions must start from `docs/99.templates/adr.template.md`.

## Naming Rules

- Use `####-<decision-slug>.md` for ADRs.
- Use `YYYY-MM-DD-<architecture-slug>.md` for time-bound ARD material.
- Keep architecture requirements in `requirements/` and decisions in `decisions/`.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- New ARD/ADR documents start as `draft`.
- Only reviewed architecture decisions may become `active` and guide downstream specs.
- Deprecated decisions must link to superseding ADRs.
- On `main`, this folder remains a skeleton until a derived project creates project-specific architecture documents.

## Cross-Reference Rules

- Every architecture requirement must link to upstream requirements when applicable.
- Every decision must link to the requirement, spec, plan, or issue that required it.
- Subfolder README indexes must be kept in sync after moves or metadata changes.
- Link only existing durable targets as Markdown links. Keep planned or purged
  historical targets as inline text with rationale.

## Usage Examples

- Use `requirements/` for reusable architecture requirements and reference models.
- Use `decisions/` for accepted ADRs and compact docs migration decisions.
- Use `docs/03.specs/` when the question is about implementation behavior,
  interfaces, data models, or test strategy.
- Use `docs/04.execution/` when the question is about work sequencing,
  validation logs, or task evidence.

## How to Work in This Area

1. Confirm product intake and PRD context exist.
2. Choose `requirements/` for ARDs or `decisions/` for ADRs.
3. Start from the matching template in `docs/99.templates/`.
4. Update this README and the relevant child README when files change.

## AI Authoring Guidance

1. Confirm the change requires architecture-level traceability.
2. Select the matching template from `docs/99.templates/`.
3. Link downstream specs or execution evidence.
4. Update this README and the relevant subfolder README.
5. STOP if the work is actually implementation detail or execution evidence and
   route it to Stage 03 or Stage 04 instead.

## AI Execution Checklist

- [ ] Intake and PRD inputs are available.
- [ ] ARD/ADR documents use the required templates.
- [ ] Stack and quality attribute assumptions are explicit.
- [ ] Downstream spec/plan links are maintained.
- [ ] The `Documents` table reflects actual child folders and files.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [decisions](./decisions/) | package | ADR seed guide plus dev-only template decision history | project-seed | 2026-05-21 |
| [requirements](./requirements/) | package | ARD seed guide plus dev-only template architecture history | project-seed | 2026-05-21 |

## Related Documents

- [01.requirements](../01.requirements/README.md) - Upstream product requirements
- [03.specs](../03.specs/README.md) - Technical specifications
- [04.execution](../04.execution/README.md) - Plans and task evidence
- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md) - Documentation governance

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
