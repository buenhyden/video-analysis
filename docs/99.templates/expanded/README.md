---
title: Expanded Templates
version: 1.0.0
owner: Governance Architect
layer: common
stage: 99
status: active
last-updated: 2026-05-21
---

# Expanded Templates

> Optional expanded Markdown templates for DDD and Stage 04 companion documents.

## Overview

This folder contains optional expanded Markdown templates used when a parent ARD or Spec needs companion DDD or domain-modeling detail.

## Audience

This README is for architects, spec authors, and agents selecting optional companion templates.

## Scope

This folder contains expanded templates used when the primary ARD or Spec template needs a separate companion document. These templates remain optional and must only be used when the parent stage gate or feature complexity requires the extra detail.

### In Scope

- Bounded context and ubiquitous language templates for Stage 02.
- Domain model, tactical model, and domain event templates for Stage 04.
- README indexing for expanded template inventory.

### Out of Scope

- Active architecture or specification documents.
- Machine-readable contract templates; use `../extended/` for those.

## Mandatory Templates

- None. All templates in this folder are optional companions selected by `docs/00.agent-governance/rules/stage-gate-matrix.md`.

## Structure

| Template Family | Purpose |
| :--- | :--- |
| Bounded context and ubiquitous language | Stage 02 DDD discovery companions. |
| Domain model, tactical model, and domain events | Stage 04 specification companions. |

## Naming Rules

- Pattern: `<slug>.template.md`
- Do not place generated stage documents in this folder.
- Path portability: keep template path segments <= 80 chars and avoid spaces or Windows-reserved characters.

## Lifecycle Rules

Documents in this folder follow the standard lifecycle: `draft`, `active`, `completed`, `deprecated`.

## Cross-Reference Rules

- Every template must be listed in the [Documents](#documents) table.
- Parent stage documents must link to any generated companion document.

## AI Authoring Guidance

1. Read the parent stage template first.
2. Use expanded templates only when the stage gate or feature complexity requires them.
3. Keep generated documents in their canonical stage folder, not in `docs/99.templates/`.
4. For derived-project seeds, keep expanded companion documents draft-only and create them only after parent ARD or Spec evidence exists.

## How to Work in This Area

1. Confirm a parent ARD or Spec requires an expanded companion.
2. Select only the template that matches the needed modeling artifact.
3. Link the generated document from the parent stage document and folder README.
4. Keep this README `Documents` table synchronized with local template files.

## AI Execution Checklist

- **Entry Gate**: A parent ARD or Spec requires a companion document.
- **Exit Gate**: The generated document is linked from the parent stage document and folder README.
- **Hard Stop Conditions**: STOP if no parent stage document exists.
- **Downstream Trigger**: Update the parent ARD/Spec, folder README, and generated companion links when an expanded template changes.
- **Evidence Rule**: Cite the parent ARD or Spec that required the expanded document.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [bounded-context.template.md](./bounded-context.template.md) | md | The Bounded Context document defines a linguistic and functional boundary within a domain. | draft | - |
| [domain-events.template.md](./domain-events.template.md) | md | The Domain Event Catalog defines the asynchronous contracts between contexts. | draft | - |
| [domain-model.template.md](./domain-model.template.md) | md | The Domain Model provides a technical blueprint of the domain logic. | draft | - |
| [tactical-model.template.md](./tactical-model.template.md) | md | The Tactical Model bridges the gap between high-level domain design and physical implementation. | draft | - |
| [ubiquitous-language.template.md](./ubiquitous-language.template.md) | md | The Ubiquitous Language Glossary ensures that every person (and agent) working in a domain uses the same terms for the same concepts. | draft | - |

## Related Documents

- [Template Index](../README.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage Gate Matrix](../../00.agent-governance/rules/stage-gate-matrix.md)

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
