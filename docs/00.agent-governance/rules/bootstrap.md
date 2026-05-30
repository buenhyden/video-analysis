# Agent Bootstrap Governance (March 2026)

> [!NOTE]
> `Project-Template` is a spec-driven repository. New derived projects must complete project initialization intake before PRD, architecture, spec, plan, task, operations, or reference documents are authored.

This file is the mandatory entry point for all agent sessions.

## 1. Bootstrap Sequence (Mandatory)

1. Load this file.
2. Read `docs/00.agent-governance/memory/methodology.md` and `docs/00.agent-governance/memory/progress.md`; initialize or repair progress from `docs/99.templates/progress.template.md` if missing.
3. Run `preflight-checklist.md`.
4. Activate persona/scope using `persona.md` + `scopes/*.md`.
5. Resolve stage ownership and procedural flow using `stage-gate-matrix.md` and `sdlc-procedure.md`.
6. Apply the project initialization gate in `project-initialization-intake.md`.
7. Classify inherited Project-Template documents with `template-document-lifecycle.md` before reusing, moving, or deleting them.
8. Load `environment-readiness.md` before changing setup, validation prerequisites, local tooling assumptions, or runtime readiness policy.
9. Select the required document template from `docs/99.templates/` before any stage authoring.
10. Adopt the **Git Workflow** from `git-workflow.md`.
11. Adopt the **Agent Operating Procedure (AOP)** from `agentic.md`.
12. Confirm standards from `standards.md`, `documentation-protocol.md`, and `quality-standards.md`.

## 2. Core Principles

- **Spec-Anchored**: Implementation depends on approved PRD + Spec.
- **Intake-First**: Derived projects collect product/software intent and stack facts before any project stage document is written.
- **Lifecycle-Classified**: Template-maintenance history is classified before it is reused, moved, or deleted.
- **Environment-Classified**: Local tools are classified as core, optional, or stack-conditional before a task is blocked or a prerequisite is added.
- **Template-First**: Stage documents are authored from the matching `docs/99.templates/` contract before content is customized.
- **Persona-Scoped**: Each task requires an explicit persona/scope match.
- **Lazy-Loaded**: Load only the rules and scopes required for the active task.
- **Reference-Safe**: Validate links/imports using `reference-integrity.md`.
- **Traceable**: Outputs must be traceable to stage input documents.
- **Memory-Aware**: Active methodology and progress are tracked in Stage 00 memory, never in `_workspace/**`.

## 3. Stage-Gate Authority

Use `stage-gate-matrix.md` as the single source for:

- purpose per stage
- when to write
- primary persona
- required inputs/outputs
- template selection
- completion criteria

## 4. Required Rule Files

- `preflight-checklist.md`
- `persona.md`
- `environment-readiness.md` — load when setup, local tooling, validation prerequisites, or runtime readiness is in scope
- `project-initialization-intake.md`
- `template-document-lifecycle.md`
- `stage-gate-matrix.md`
- `agentic.md` (AOP)
- `sdlc-procedure.md` (SOP)
- `standards.md`
- `design-system.md` — load when frontend, mobile, app, or UI work is in scope
- `documentation-protocol.md`
- `quality-standards.md`
- `reference-integrity.md`
- `git-workflow.md`
- `github-repository-governance.md` — load when any `.github/**` or GitHub policy change is in scope

## 5. Hard Requirements

- Do not start implementation without PRD and Spec anchors.
- Do not start new-project PRD, ARD, Spec, Plan, Task, Operations, or Reference authoring until product/software and stack intake is complete.
- Do not reuse Project-Template maintenance documents as active derived-project content without classification through `template-document-lifecycle.md`.
- Do not treat optional or stack-specific tools as required before `environment-readiness.md` classification and project intake justify them.
- Do not mutate local environments, install tools, or write dotfiles from `bash scripts/ws.sh setup`.
- Do not create or update non-README documents under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, or `docs/90.references/` without the matching `docs/99.templates/` contract.
- Do not bypass persona/scope activation.
- Do not proceed with broken references.
- Do not violate language policy for governance files.
- If `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or any file in `docs/00.agent-governance/` already exists, refactor in-place — never blind-overwrite.

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
