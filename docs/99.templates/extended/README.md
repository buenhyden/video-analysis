---
title: Extended Templates
version: 1.0.0
owner: Governance Architect
layer: common
stage: 99
status: active
last-updated: 2026-05-21
---

# Extended Templates

> Optional machine-readable contract templates for adopted GraphQL and gRPC technologies.

## Overview

This folder contains optional machine-readable contract templates for projects that explicitly adopt GraphQL or gRPC.

## Audience

This README is for spec authors, backend implementers, API reviewers, and agents selecting optional contract templates.

## Scope

This folder contains optional contract templates for technologies that are not mandatory in the language-agnostic workspace template. Use them only when the target project explicitly adopts the matching technology.

### In Scope

- GraphQL schema template.
- gRPC/Protocol Buffers service template.
- README indexing for optional machine-readable templates.

### Out of Scope

- Required SDLC templates.
- Generated feature contracts.
- Technology choices for projects that have not adopted GraphQL or gRPC.

## Mandatory Templates

- None. These templates are optional and technology-specific.

## Structure

| Template | Purpose |
| :--- | :--- |
| `schema.template.graphql` | Optional GraphQL schema contract starter. |
| `service.template.proto` | Optional gRPC/Protocol Buffers service starter. |

## Naming Rules

- GraphQL: `schema.template.graphql`
- gRPC/Proto: `service.template.proto`
- Generated contracts must live under the relevant feature spec package.
- Path portability: keep template path segments <= 80 chars and avoid spaces or Windows-reserved characters.

## Lifecycle Rules

Documents in this folder follow the standard lifecycle: `draft`, `active`, `completed`, `deprecated`.

## Cross-Reference Rules

- Every extended template must be listed in the [Documents](#documents) table.
- Generated contracts must be linked from the parent `spec.md`.
- Link examples inside machine-readable templates are written from the generated contract target location, `docs/03.specs/<feature-id>/contracts/`.
- From that generated location, parent references use `../spec.md`, `../tests.md`, and `../api-spec.md`.

## AI Authoring Guidance

1. Confirm the target project uses the technology before selecting a template.
2. Keep generated contracts in `docs/03.specs/<feature-id>/contracts/`.
3. Do not make GraphQL or gRPC mandatory for the template repository.
4. Convert template comments into live parent links in the generated parent `spec.md`; do not leave pseudo-links in generated Markdown.
5. For derived-project seeds, do not generate GraphQL or gRPC contracts until intake and parent spec explicitly adopt that technology.

## How to Work in This Area

1. Confirm the adopted technology is in the parent Stage 04 spec.
2. Select the matching contract template and generate project-specific contracts outside `docs/99.templates/`.
3. Link generated contracts from the parent `spec.md` and feature README.
4. Keep this README `Documents` table synchronized with local contract templates.

## AI Execution Checklist

- **Entry Gate**: A parent Spec requires a machine-readable GraphQL or gRPC contract.
- **Exit Gate**: Generated contract is linked from the parent Spec and feature README.
- **Hard Stop Conditions**: STOP if the target technology is not in scope.
- **Downstream Trigger**: Update parent specs, API specs, and generated contract links when an extended template changes.
- **Evidence Rule**: Cite the Spec section requiring the contract.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [schema.template.graphql](./schema.template.graphql) | graphql | GraphQL schema contract template | active | - |
| [service.template.proto](./service.template.proto) | proto | gRPC/Protocol Buffers service contract template | active | - |

## Related Documents

- [Template Index](../README.md)
- [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- [Stage Gate Matrix](../../00.agent-governance/rules/stage-gate-matrix.md)

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
