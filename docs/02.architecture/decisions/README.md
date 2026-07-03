---
title: Architecture Decision Records Index
version: 1.0.0
owner: System Architect
layer: architecture
stage: 02
status: active
last-updated: 2026-05-21
---

# Architecture Decisions Skeleton

> 새 프로젝트의 ADR을 작성하기 위한 release skeleton.

## Overview

`docs/02.architecture/decisions/`는 파생 프로젝트에서 durable architecture decisions를 기록하는 위치이다. `main` release branch에서는 이전 video-analysis ADR이나 decision history를 보관하지 않는다.

파생 프로젝트에서는 approved requirements, ARD, stack intake를 바탕으로 decision context, alternatives, chosen option, consequences를 프로젝트에 맞게 작성한다.

아래 ADR rows는 video-analysis의 template/runtime decision history다. 새 프로젝트에서는 번호를 재사용하거나 복사하지 않고, 실제 decision trigger가 있을 때 새 ADR을 생성한다.

## Audience

이 README의 주요 독자:

- System architects
- Tech leads
- Reviewers evaluating tradeoffs
- AI agents

## Scope

The ADR layer provides a historical log of technical decisions. It answers the
"why this choice" question after an ARD, spec, plan, issue, or governance
change creates a real decision point.

Use an ADR when alternatives were considered and one path is accepted,
deprecated, or superseded. Use an ARD when the document should define system
boundaries, quality attributes, or DDD strategy.

### In Scope

- Strategic technical decisions (e.g., choice of database, framework, or architecture pattern).
- High-impact tactical decisions (e.g., API design philosophy, state management).
- Rationale, trade-offs, and rejected alternatives.
- Positive and negative consequences of the decision.
- Deprecation records for decisions that remain useful as historical context.

### Out of Scope

- Low-level implementation details (see `docs/03.specs/`).
- Transient notes or scratch ideas.
- Project management or operational policies.
- Execution plans, task evidence, validation logs, or closure notes (see
  `docs/04.execution/`).

## Structure

- `README.md` - Folder contract and index.
- Child files and folders listed in the Documents table.

## How to Work in This Area

1. Confirm the artifact records a durable decision, not a reference
   architecture, implementation spec, or execution log.
2. Use the matching template from `docs/99.templates/`.
3. Update this README after files change.
4. Run the relevant documentation validation gate.

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- New ADR documents must start from `docs/99.templates/adr.template.md`.

## Naming Rules

- Use `####-<decision-slug>.md`.
- Keep numbering monotonic within the derived project.
- Do not reuse numbers for replaced or removed decisions.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- New ADRs start as `draft`.
- Accepted decisions become `active`.
- Replaced or invalid decisions become `deprecated` and link to the superseding ADR.

## Cross-Reference Rules

- Every ADR must be linked in the [Documents](#documents) table below.
- Every ADR must have a `## Related Documents` section linking to parent PRDs/ARDs and affected Specs.
- Link only existing durable targets as Markdown links. Keep purged archives or
  planned downstream artifacts as inline text with rationale.

## Usage Examples

- Create an ADR from `adr.template.md` when a decision changes architecture, workflow, runtime, or governance policy.
- Mark an ADR as superseded only after the replacement ADR or governance document is linked.
- Deprecate an ADR when its decision no longer applies to the base template but
  still explains a historical trade-off.

## AI Authoring Guidance

1. **Phase 0: Problem**: Identify a technical challenge requiring a decision.
2. **Phase 1: Alternatives**: Research and document at least two alternatives.
3. **Phase 2: Decision**: Select the path and document trade-offs/consequences.
4. **Phase 3: Finalize**: Update the index and set status (`accepted`, `deprecated`, etc.).
5. **Routing Check**: Move system boundaries to ARDs, behavior details to Specs,
   and validation evidence to Stage 04.

## AI Execution Checklist

- [ ] Intake and architecture context are linked.
- [ ] ADR uses `docs/99.templates/adr.template.md`.
- [ ] Alternatives and consequences are explicit.
- [ ] Superseded decisions link to replacements.
- [ ] The `Documents` table reflects actual files in this folder.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [02.architecture/requirements](../requirements/README.md) - Architecture Reference Models
- [03.specs](../../03.specs/README.md) - Technical Specifications
- [AGENTS.md](../../../AGENTS.md) - Agent Governance Root

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
