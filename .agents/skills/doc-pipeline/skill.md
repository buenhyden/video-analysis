---
name: doc-pipeline
description: Orchestrates the workspace documentation pipeline from PRD through operations artifacts. Use when a feature or governance change requires staged documents across the compact docs model: docs/01.requirements through docs/05.operations plus docs/90.references when needed. Triggers on 'generate documentation for this feature', 'run the doc pipeline', 'create all stage documents', 'update documentation across stages', 'write the technical documentation', 'document this change end-to-end', 'API documentation', 'user guide', 'README', 'operations guide', or any request to produce or update structured technical documents across multiple doc stages.
---

# Doc Pipeline

Coordinate the active documentation pipeline for this workspace.

## Scope

- Generate or update stage documents in order.
- Reuse approved upstream artifacts instead of recreating them.
- Route work to the owning agent for each stage.

## Stage Map

| Stage      | Output Path           | Owner Agent                              |
| ---------- | --------------------- | ---------------------------------------- |
| PRD        | `docs/01.requirements/`        | `product-manager`                        |
| ARD        | `docs/02.architecture/requirements/`        | `system-architect`                       |
| ADR        | `docs/02.architecture/decisions/`        | `system-architect`                       |
| Spec       | `docs/03.specs/`      | `backend-engineer` / `frontend-engineer` |
| Plan       | `docs/04.execution/plans/`      | `product-manager`                        |
| Tasks      | `docs/04.execution/tasks/`      | implementing engineers                   |
| Guides     | `docs/05.operations/guides/`     | `technical-writer`                       |
| Operations | `docs/05.operations/policies/` | `infra-devops` / `ops-manager`           |
| Runbooks   | `docs/05.operations/runbooks/`   | `sre-ops`                                |

## Execution Modes

| Request Pattern                           | Mode          | Stages Covered                            |
| ----------------------------------------- | ------------- | ----------------------------------------- |
| "Generate documentation for this feature" | Full Pipeline | All missing stages in order               |
| "Write the technical guide"               | Guide Mode    | Stage 07 only                             |
| "Create the API documentation"            | API Doc Mode  | Stage 04 spec + stage 07 guide            |
| "Update the operations manual"            | Ops Mode      | Stages 08–09 only                         |
| "Document this architecture decision"     | ADR Mode      | Stage 03 only                             |
| "Write a runbook for this incident"       | Runbook Mode  | Stage 09 only                             |
| "Generate diagrams for this doc"          | Diagram Mode  | Within active stage; add Mermaid diagrams |

## Workflow

### Phase 1: Scope Confirmation

1. Confirm product/software intake, requested stage range, and the latest approved upstream artifact.
2. Read the matching template in `docs/99.templates/` before drafting anything new.
3. Identify which stages already exist and which are missing — produce only the missing or explicitly requested stages.
4. For multi-stage runs, determine the dependency order (upstream stage must exist before downstream).
5. For derived projects, do not reuse Project-Template maintenance history as project-owned PRD, architecture, spec, plan, task, operations, or reference content.

### Phase 2: Document Structure Design

Before writing body content, produce a structure plan for each target document:

```
## Document Structure Plan

### Document Metadata
- Title:
- Type: Tutorial / How-to / Reference / Explanation  [Diátaxis classification]
- Target Audience: [role + technical level]
- Prerequisites: [what reader must know or have]
- Expected Outcome: [what reader achieves after reading]

### Table of Contents
1. [Section title]
   - Purpose: [what this section achieves]
   - Depth: overview / detailed
   1.1 [Sub-section]

### Content Strategy
| Section | Content Type | Key Elements | Diagram Needed |
|---------|-------------|-------------|----------------|
```

**Document type classification (Diátaxis):**

| Type        | Purpose            | Orientation | When to Use                      |
| ----------- | ------------------ | ----------- | -------------------------------- |
| Tutorial    | Learning           | Study       | Getting started, onboarding      |
| How-to      | Task completion    | Work        | Step-by-step procedures          |
| Reference   | Information lookup | Work        | API docs, configuration lists    |
| Explanation | Understanding      | Study       | Architecture overviews, concepts |

### Phase 3: Content Production

Write documents stage by stage. For each stage:

1. Read the upstream stage document to preserve traceability.
2. Apply the Diátaxis classification selected in Phase 2.
3. Follow the step-by-step procedure standard for any procedural content:

```markdown
#### Step N: [Task Name]

**How to:**

1. [Specific action]
2. [Specific action]

**Expected Result:** [What you observe after completing this step]

> Warning: [Common mistake or caution]
> Tip: [Optional efficiency note]
```

4. Add diagrams immediately before the prose that describes them:
   - `graph LR` for process flows
   - `sequenceDiagram` for API interactions
   - `erDiagram` for data models
   - Keep diagrams under 15 nodes; split complex flows into sub-diagrams

5. End every document with a version metadata block:

```
> **Version**: v1.0 | **Created**: YYYY-MM-DD | **Review Cycle**: quarterly
> **Target Audience**: [role]
> **Related Specs**: [links to upstream documents]
```

### Phase 4: Stage-Gate Review

Before handing off to the next stage:

| Review Item        | Check                                                   |
| ------------------ | ------------------------------------------------------- |
| Technical accuracy | Code examples run; API specs match implementation       |
| Completeness       | All ToC sections written; error states documented       |
| Consistency        | Terminology uniform; code style consistent throughout   |
| Audience fit       | Target reader can follow without unstated prerequisites |
| Diagram accuracy   | Diagrams match body text; Mermaid syntax is valid       |
| Cross-references   | Links to upstream specs and decision docs present       |
| Traceability       | Every behavioral claim traces to a PRD or Spec anchor   |

### Phase 5: Multi-Stage Tracking

Record durable progress in `docs/00.agent-governance/memory/progress.md` when the work spans multiple stages. If `progress.md` is missing or structurally incomplete, initialize or repair it from `docs/99.templates/progress.template.md`. Use `_workspace/` only for transient scratch files that are not authoritative:

```
_workspace/
  00_scope.md          — confirmed stage range, owner assignments
  01_prd_status.md     — existing / produced / skipped
  02_ard_status.md
  ...
  review_report.md     — stage-gate findings and resolution log
```

## API Documentation Standard

For API reference documents at stage 04 or 07:

````markdown
## [Endpoint Name]

`METHOD /api/v1/[resource]`

**Description:** [What this endpoint does]
**Authentication:** Required / None — [method]

### Request

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |

### Response

```json
{ "success": true, "data": {} }
```
````

### Error Codes

| Code | Meaning | Resolution |
| ---- | ------- | ---------- |

```

## Rules

- Never skip a required upstream document silently — flag the gap and halt.
- Never overwrite an approved document without merging existing content.
- Treat all documents in `docs/00.agent-governance/` as English-only outputs.
- Escalate structural changes to `system-architect` or `governance-architect`.
- Do not document unstable behavior as if it were final — mark with `[subject to change]`.
- Final authoritative stage deliverables must live under canonical compact `docs/` paths, never under legacy ad hoc draft buckets or `_workspace/`.
- `docs/00.agent-governance/memory/` owns tracked methodology, progress, and durable agent memory.
- `docs/00.agent-governance/memory/progress.md` must be updated at phase boundaries, handoffs, blockers, and task closure.
- `_workspace/` is for transient tracking files only and cannot override Stage 00 governance or memory.

## Error Handling

| Scenario | Strategy |
|----------|---------|
| Missing upstream anchor (no PRD for a spec request) | Flag gap; halt and request the upstream document |
| Template missing from `docs/99.templates/` | Alert `governance-architect`; do not invent structure |
| Technical behavior unclear | Mark section `[technical validation needed]`; request review from owning engineer |
| Mermaid diagram too complex | Split into Level 0 + Level 1 sub-diagrams with cross-references |
| Diagram/prose mismatch found in review | Fix diagram to match prose; never silently drop either |
```
