---
title: Specs Skeleton
version: 1.0.0
owner: System Architect
layer: specification
stage: 03
status: active
last-updated: 2026-05-21
---

# Specs Skeleton

> Feature-level technical specifications and test strategies for the compact docs model.

## Overview

This hub owns feature-level technical specification packages. `docs/03.specs/`
is folder 03 in the compact docs tree, while technical specifications are the
Stage 04 technical-spec gate in the 00-10 workflow matrix.

A spec translates approved product requirements, architecture requirements, and
architecture decisions into precise component contracts, sequence/state diagrams,
TDD readiness maps, and agent behavior contracts before execution planning begins.

The spec packages listed on `dev` are completed Project-Template remediation
specs. They are not examples or seed specs for derived projects; `main` keeps
this folder as a README skeleton until a derived project creates its own spec
package from `spec.template.md` and `tests.template.md`.

## Audience

- System architects
- Backend, frontend, and QA engineers
- AI agents preparing implementation-ready feature contracts
- Reviewers validating SDD, DDD, and TDD readiness

## Scope

### In Scope

- Feature specification packages under `<feature-id>/`.
- Primary package document: `<feature-id>/spec.md`.
- Required test strategy before execution planning: `<feature-id>/tests.md`.
- Template-backed companion artifacts when applicable: `api-spec.md`,
  `tactical-model.md`, `domain-model.md`, `domain-events.md`, and
  `contracts/*` machine-readable contracts.
- Agent role and IO contracts when AI agent behavior is in scope.

### Out of Scope

- PRD or ARD authoring
- Implementation task logs
- Operations runbooks or incidents
- Template repository history

## Structure

```text
03.specs/
└── README.md    # Release skeleton guide for project-specific specs
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- [spec.template.md](../99.templates/spec.template.md) - Package creation template for `spec.md`.
- [tests.template.md](../99.templates/tests.template.md) - Required before creating execution plans in `docs/04.execution/plans/`.

Optional companion templates are used only when the spec scope requires them:

- [api-spec.template.md](../99.templates/api-spec.template.md) - API contract companion.
- [Tactical DDD Model Template](../99.templates/expanded/tactical-model.template.md) - Tactical DDD companion.
- [Domain Model Template](../99.templates/expanded/domain-model.template.md) - Domain model companion.
- [Domain Events Template](../99.templates/expanded/domain-events.template.md) - Domain events companion.
- [openapi.template.yaml](../99.templates/openapi.template.yaml) - OpenAPI contract under `contracts/`.
- [GraphQL Schema Template](../99.templates/extended/schema.template.graphql) - GraphQL contract when the project adopts GraphQL.
- [gRPC/Proto Service Template](../99.templates/extended/service.template.proto) - gRPC/Proto contract when the project adopts gRPC.

## Naming Rules

- Feature spec directory: `<feature-id>/` (slug matching the upstream PRD or ARD).
- Primary spec file: `spec.md` within the feature directory.
- Required test strategy file before execution planning: `tests.md`.
- Companion files: `api-spec.md`, `tactical-model.md`, `domain-model.md`,
  `domain-events.md`, and `contracts/*` within the same feature directory.
- Do not create `data-model.md` as a default new-file target unless a future
  approved template or policy explicitly introduces it.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- New specs start as `draft`.
- Specs become `active` only when upstream requirements and architecture links are valid.
- Superseded specs must link to replacements or downstream migration plans.
- On `main`, this folder remains a skeleton until a derived project creates project-specific specs.

## Cross-Reference Rules

- Every spec must link to its upstream PRD in `docs/01.requirements/`.
- Every spec must link to relevant ARDs and ADRs in `docs/02.architecture/`.
- Every spec package must use target-relative links from the generated document
  location, not from the template source in `docs/99.templates/`.
- Every spec must be linked in the [Documents](#documents) table below.
- Subfolder README indexes must be kept in sync after moves or metadata changes.

## Usage Examples

- Create a feature directory and `spec.md` from `spec.template.md` after PRD approval.
- Fill SDD, DDD, and TDD readiness sections, or document explicit exemptions.
- Create and link `tests.md` from `tests.template.md` before creating plans in `docs/04.execution/plans/`.
- Add execution plan and task evidence in `docs/04.execution/` only after the spec package is ready.

## How to Work in This Area

1. Confirm intake, PRD, and architecture context exist or document the approved absence rationale.
2. Create a feature directory and start `spec.md` from `docs/99.templates/spec.template.md`.
3. Create `tests.md` from `docs/99.templates/tests.template.md` before execution planning.
4. Update this README when spec packages are added, renamed, deprecated, or removed.

## AI Authoring Guidance

1. Confirm the upstream PRD and ARD context exists before drafting a spec, or record the approved rationale for absence.
2. Select `spec.template.md` from `docs/99.templates/`.
3. Complete all mandatory sections: SDD, DDD, TDD Readiness, and Agent IO Contract if applicable.
4. Create and link `tests.md` from `tests.template.md` before execution planning.
5. Update this README and link downstream execution evidence.

## AI Execution Checklist

- [ ] **Entry Gate**: Upstream PRD and ARD links are identified or absence is rationale-documented.
- [ ] **Template Gate**: New spec documents use `spec.template.md`.
- [ ] **SDD Gate**: All flows with 3+ components include a Mermaid sequence diagram.
- [ ] **TDD Gate**: `tests.md` exists before execution planning, and all `impl` behaviors are mapped to test cases or have documented exemptions.
- [ ] **Index Gate**: This README Documents table is synchronized after any spec is added or changed.
- [ ] **Exit Gate**: Spec is marked `active` only after SDD and TDD gates pass.
- [ ] **Hard Stop**: STOP if a spec is marked `active` without upstream PRD/ARD links or rationale, target-relative links, and TDD mapping.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [01.requirements](../01.requirements/README.md) - Product requirements
- [02.architecture](../02.architecture/README.md) - Architecture requirements and decisions
- [04.execution](../04.execution/README.md) - Plans and task evidence
- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md) - Documentation governance

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
