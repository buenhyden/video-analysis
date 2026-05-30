# 99.templates

> Templates provide standardized markdown and YAML contracts for SDLC stages.

## Purpose & Scope

The Templates layer ensures consistency and professional standards across all documentation in the workspace. It provides the base schemas and required sections (including AI Execution Checklists) for every stage of the SDLC.

### In Scope

- SDLC Stage Templates (PRD, ARD, ADR, Spec, Plan, Task).
- Specialized Templates (API, Operation, Guide, Runbook, Incident).
- Data/Contract Templates (OpenAPI — technology-agnostic).
- Metadata and Frontmatter standards.
- `expanded/`: Optional expanded Markdown templates for DDD and companion Stage 04 documents.
- `extended/`: Optional technology-specific templates (GraphQL, gRPC/Proto). Use only when the target project adopts that technology.

### Out of Scope

- Active documentation (see `docs/01.requirements/` through `docs/05.operations/` and supporting Stage 90 references).
- Execution records (see `docs/04.execution/tasks/`).

## Mandatory Templates

- [readme.template.md](./readme.template.md) - Required for folder-level READMEs.

Stage-specific mandatory templates are selected by [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md) and [Stage Gate Matrix](../00.agent-governance/rules/stage-gate-matrix.md). This catalog lists the reusable sources; it does not make every optional companion mandatory.

## Template Classification

- **Core templates**: Markdown templates directly mapped to compact stage documents, Stage 00 memory, and Stage 90 references. These are the default starting point for governed work.
- **Optional expanded templates**: DDD and companion Markdown templates under `expanded/`. Use them only when the active stage requires additional modeling detail.
- **Optional technology-specific templates**: GraphQL and gRPC/Proto contracts under `extended/`. Use them only after the target project adopts that technology.
- **Machine-readable templates**: YAML, GraphQL, and Proto templates. Keep them stack-neutral in the base template and reference them from a Stage 04 spec before use.

## Generated Document Boundary

- Seed documents generated for a derived project must keep `status: draft` until reviewed.
- Markdown templates that generate stage documents use `status: draft` in their
  own frontmatter so copied seeds do not start as approved source of truth.
- Replace bracketed placeholders with project facts or explicit `TODO:` statements before using a generated document as an upstream stage gate.
- Do not copy Project-Template maintenance specs, plans, tasks, SLOs, generated intelligence, or reference history into a derived project unless `template-document-lifecycle.md` classifies the content and the maintainer intentionally keeps it.
- Treat target-relative links in template source as examples. Generated documents must convert them into live relative links only when the target exists.

## Naming Rules

- Pattern: `<slug>.template.<ext>`
- Path portability: keep generated reusable template paths <= 140 relative chars where practical, segments <= 80 chars, and avoid spaces or Windows-reserved characters.

## Lifecycle Rules

Generated documents created from these templates follow the standard lifecycle:

1. **draft**: Initial creation from template. Not yet for implementation.
2. **active**: Reviewed and approved. Source of truth for downstream stages.
3. **completed**: Implementation finished and verified.
4. **deprecated**: Replaced by a newer version or no longer relevant.

## Cross-Reference Rules

- Every Template must be linked in the [Documents](#documents) table below.
- Template catalog README files link back to the root `AGENTS.md`, `documentation-protocol.md`, or the stage-gate matrix as appropriate.
- Template cross-link examples are authored from the generated **Target** location, not from `docs/99.templates/`.
- Placeholder paths in template source stay as code spans unless the generated document points to an existing repository file.
- Generated documents must convert template pseudo-links into live Markdown links when the target exists.

### Target-Relative Link Quick Reference

| Generated target | Link back to governance | Common upstream/downstream examples |
| :--- | :--- | :--- |
| `docs/01.requirements/YYYY-MM-DD-<slug>.md` | `../00.agent-governance/rules/project-initialization-intake.md` | `../02.architecture/requirements/####-<slug>.md`, `../03.specs/<feature-id>/spec.md` |
| `docs/02.architecture/requirements/####-<slug>.md` | `../../00.agent-governance/rules/stage-gate-matrix.md` | `../../01.requirements/YYYY-MM-DD-<slug>.md`, `../decisions/####-<slug>.md`, `../../03.specs/<feature-id>/spec.md` |
| `docs/02.architecture/decisions/####-<slug>.md` | `../../00.agent-governance/rules/stage-gate-matrix.md` | `../requirements/####-<slug>.md`, `../../03.specs/<feature-id>/spec.md` |
| `docs/03.specs/<feature-id>/spec.md` | `../../00.agent-governance/rules/stage-gate-matrix.md` | `../../01.requirements/YYYY-MM-DD-<slug>.md`, `./tests.md`, `../../04.execution/plans/YYYY-MM-DD-<slug>.md` |
| `docs/03.specs/<feature-id>/api-spec.md` | `../../00.agent-governance/rules/stage-gate-matrix.md` | `./spec.md`, `./tests.md`, `./contracts/openapi.yaml`, `../../04.execution/tasks/YYYY-MM-DD-<slug>.md` |
| `docs/03.specs/<feature-id>/tests.md` | `../../00.agent-governance/rules/stage-gate-matrix.md` | `./spec.md`, `./api-spec.md`, `../../04.execution/tasks/YYYY-MM-DD-<slug>.md` |
| `docs/04.execution/plans/YYYY-MM-DD-<slug>.md` | `../../00.agent-governance/rules/stage-gate-matrix.md` | `../../03.specs/<feature-id>/spec.md`, `../tasks/YYYY-MM-DD-<slug>.md` |
| `docs/04.execution/tasks/YYYY-MM-DD-<slug>.md` | `../../00.agent-governance/rules/stage-gate-matrix.md` | `../plans/YYYY-MM-DD-<slug>.md`, `../../03.specs/<feature-id>/tests.md` |
| `docs/05.operations/**/<slug>.md` | `../../00.agent-governance/rules/stage-gate-matrix.md` or deeper as needed | `../../03.specs/<feature-id>/spec.md`, `../runbooks/<topic>.md`, `../policies/<policy>.md` |
| `docs/05.operations/incidents/YYYY/INC-###-<title>/{record.md,postmortem.md}` | `../../../../00.agent-governance/rules/stage-gate-matrix.md` | `../../../runbooks/####-<topic>.md`, `../../../policies/<policy>.md`, `./record.md`, `./postmortem.md` |
| `docs/00.agent-governance/memory/{methodology.md,progress.md,YYYY-MM-DD-<slug>.md}` | `../rules/bootstrap.md` | `./README.md`, `./progress.md`, `../../04.execution/tasks/YYYY-MM-DD-<slug>.md` |
| `docs/90.references/<slug>.md` | `../00.agent-governance/rules/reference-integrity.md` | `../01.requirements/YYYY-MM-DD-<slug>.md`, `./knowledge/<slug>.md` |

## Usage Examples

- Start a new Stage 04 spec from `spec.template.md`; add expanded DDD templates only when the ARD or spec triggers them.
- Start an API contract from `openapi.template.yaml`; use GraphQL or Proto templates only after the chosen project stack requires them.
- Start a new folder README from `readme.template.md`, then refresh the target index with `bash scripts/docs/update-doc-readme-index.sh <docs-relative-dir>`.
- When generating machine-readable contracts under `docs/03.specs/<feature-id>/contracts/`, parent document references must use target-relative paths such as `../spec.md`, `../tests.md`, and `../api-spec.md`.
- For derived-project seeds, generate only the next stage-gated document that has real intake/upstream evidence. Do not prefill ARD, ADR, spec, plan, task, SLO, runbook, incident, postmortem, or reference seeds during bootstrap.

## AI Authoring Guidance

1. **Phase 0: Selection**: Identify the correct template for the current SDLC stage.
2. **Phase 1: Hydration**: Fill all mandatory sections and YAML frontmatter.
3. **Phase 2: Validation**: Ensure no `<placeholder>` text remains.
4. **Phase 3: Linking**: Establish relative links to upstream/downstream documents.

## AI Execution Checklist

- **Entry Gate**: Stage boundary is crossed, and new documentation is required.
- **Exit Gate**: Document is created from template and added to the folder index.
- **Hard Stop Conditions**: STOP if a required template is missing or outdated.
- **Downstream Trigger**: refresh this catalog and affected generated documents when template contracts change.
- **Evidence Rule**: Every new document must prove it originated from the current version of the template.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [adr.template.md](./adr.template.md) | md | The ADR captures the rationale for a specific architectural decision, including the context and the trade-offs considered. | draft | - |
| [api-spec.template.md](./api-spec.template.md) | md | The API Specification defines the technical contract for communication between systems. | draft | - |
| [ard.template.md](./ard.template.md) | md | The ARD acts as the architectural blueprint for a system or domain. | draft | - |
| [expanded](./expanded/) | package | Expanded Templates | active | 2026-05-21 |
| [extended](./extended/) | package | Extended Templates | active | 2026-05-21 |
| [guide.template.md](./guide.template.md) | md | The Guide provides educational and procedural information for developers or operators to successfully interact with a system or feature. | draft | - |
| [incident.template.md](./incident.template.md) | md | The Incident Record documents the detection, investigation, and resolution of an operational event. | draft | - |
| [methodology.template.md](./methodology.template.md) | md | The Methodology Selection document defines the active process selection and run-state memory for the current project run. | active | - |
| [openapi.template.yaml](./openapi.template.yaml) | yaml | OpenAPI contract template for feature specs | active | - |
| [operation.template.md](./operation.template.md) | md | The Operations Policy defines the standards and constraints for operating a system. | draft | - |
| [plan.template.md](./plan.template.md) | md | The Implementation Plan defines the execution order, risk control, and rollout strategy for a specific feature or set of tasks. | draft | - |
| [postmortem.template.md](./postmortem.template.md) | md | The Postmortem provides a blameless analysis of an incident. | draft | - |
| [prd.template.md](./prd.template.md) | md | The PRD defines the product intent, scope, and success criteria. | draft | - |
| [progress.template.md](./progress.template.md) | md | `progress.md` is the canonical tracked progress surface for the current governed AI-agent run. | active | - |
| [readme.template.md](./readme.template.md) | md | README Template — Repository-wide Usage Guide | draft | - |
| [reference.template.md](./reference.template.md) | md | The Reference document provides a stable citation point for domain terms, standards, factual matrices, and static facts used across the workspace. | draft | - |
| [runbook.template.md](./runbook.template.md) | md | The Runbook provides exact, step-by-step procedures for operational tasks. | draft | - |
| [session-memory.template.md](./session-memory.template.md) | md | Durable Session Memory records technical knowledge gained during development. | draft | - |
| [slo.template.md](./slo.template.md) | md | The SLO Specification defines measurable service quality targets, how they are monitored, and what operational action follows when the error budget is exhausted. | draft | - |
| [spec.template.md](./spec.template.md) | md | The Spec provides the technical blueprint for a feature. | draft | - |
| [task.template.md](./task.template.md) | md | The Task List provides traceability-first tracking of execution. | draft | - |
| [tests.template.md](./tests.template.md) | md | The Test & Evaluation Strategy ensures that every feature is built on a foundation of verifiable behavior. | draft | - |

## Expanded Templates (Optional Markdown Companions)

Use these when a stage requires a more detailed DDD or companion document than the primary template can hold.

| File | Type | Summary | Status | Last Modified |
| :--- | :--- | :--- | :--- | :--- |
| [expanded/bounded-context.template.md](./expanded/bounded-context.template.md) | md | Bounded Context Template | draft | - |
| [expanded/domain-events.template.md](./expanded/domain-events.template.md) | md | Domain Event Catalog Template | draft | - |
| [expanded/domain-model.template.md](./expanded/domain-model.template.md) | md | Domain Model Template | draft | - |
| [expanded/tactical-model.template.md](./expanded/tactical-model.template.md) | md | Tactical DDD Model Template | draft | - |
| [expanded/ubiquitous-language.template.md](./expanded/ubiquitous-language.template.md) | md | Ubiquitous Language Template | draft | - |

## Extended Templates (Technology-Specific, Optional)

Use only when the target project adopts the listed technology. Stored in `extended/` to signal optional scope.

| File | Type | Summary | Status | Last Modified |
| :--- | :--- | :--- | :--- | :--- |
| [extended/schema.template.graphql](./extended/schema.template.graphql) | graphql | GraphQL Schema Template (use if GraphQL scope) | active | 2026-05-03 |
| [extended/service.template.proto](./extended/service.template.proto) | proto | gRPC Proto Template (use if gRPC scope) | active | 2026-05-05 |

## Related Documents

- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md)
- [Template Document Lifecycle](../00.agent-governance/rules/template-document-lifecycle.md)

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
