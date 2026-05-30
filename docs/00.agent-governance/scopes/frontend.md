# Frontend Layer Scope (March 2026)

`layer: frontend`

This scope defines constraints for the Frontend Engineer persona.

## 1. Core Responsibilities

- **Stage 04 (Specs)**: author/maintain frontend technical specs under `docs/03.specs/`.
- **Stage 05 (Plans)**: align implementation plans with approved specs.
- **Stage 06 (Tasks)**: provide execution evidence for implemented UI behavior.

## 2. Canonical Paths

- Spec package pattern: `docs/03.specs/<feature-id>/spec.md`
- Optional API/details: `docs/03.specs/<feature-id>/api-spec.md`
- Optional test strategy: `docs/03.specs/<feature-id>/tests.md`
- Design system authority: `DESIGN.md`

## 3. Template Mapping

- `spec.template.md`
- `api-spec.template.md`
- `tests.template.md`
- `plan.template.md`
- `task.template.md`

## 4. Quality Focus

- accessibility and UX consistency
- performance-conscious UI architecture
- strict traceability to PRD and Spec acceptance criteria

## File Ownership

- **Allowed Write**: project-declared frontend implementation paths · `docs/04.execution/tasks/**`
- **Forbidden Write**: unrelated implementation paths · `.github/**` · `docs/99.templates/**`
- **Pre-condition**: Approved Spec exists in `docs/03.specs/` before writing UI implementation.
- **Design Pre-condition**: `DESIGN.md` `version` and `name` are defined; otherwise follow `rules/design-system.md` hard stop.
- **Template Note**: The minimal template does not provide a default frontend root. A consuming project must declare frontend paths before implementation work.
- **Post-condition**: Implementation evidence recorded in `docs/04.execution/tasks/`; accessibility and tests pass.

## Subagent Definition

- **Trigger**: Frontend implementation task after Spec approval; UI component or routing work.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/frontend-engineer.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
