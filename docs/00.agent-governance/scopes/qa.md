# QA Layer Scope (March 2026)

`layer: qa`

This scope defines the validation constraints for the QA Engineer persona.

## 1. Core Responsibilities

- **Stage 04 (Test Strategy)**: Define feature test strategy in `docs/03.specs/<feature-id>/tests.md`. Use `tests.template.md`.
- **Stage 05 (Validation Plan)**: Define runnable validation strategy in `docs/04.execution/plans/`. Use `plan.template.md`.
- **Stage 06 (Evidence)**: Record test execution evidence in `docs/04.execution/tasks/`. Use `task.template.md`.
- **Definition of Done**: Verify all criteria from Stage 01 (PRD) and 04 (Spec) are met.

## 2. Standard Taxonomy

- **Test Strategy**: Grounded in `docs/03.specs/<feature-id>/tests.md` from `tests.template.md`.
- **Tasks**: Small, verifiable units of work in `docs/04.execution/tasks/`.
- **Bugs/Fixes**: Update the feature-local test strategy and record regression evidence in execution tasks.

## 3. Required Metadata

```markdown
---
layer: qa
stage: 00
---
```

## 4. Skills Engagement

- `qa-test-planner`
- Project-declared unit, integration, E2E, accessibility, and performance testing skills from intake only.
- Examples such as Playwright, JavaScript testing patterns, or webapp testing apply only after the derived project explicitly chooses that stack and surface.

## File Ownership

- **Allowed Write**: project-declared test paths · `docs/03.specs/**/tests.md` · `docs/04.execution/plans/**` · `docs/04.execution/tasks/**`
- **Forbidden Write**: production implementation paths · `docs/99.templates/**`
- **Pre-condition**: Implementation exists and spec acceptance criteria are defined before QA verification.
- **Template Note**: The minimal template does not provide a default test root. A consuming project must declare test paths before implementation verification.
- **Post-condition**: All PRD/Spec acceptance criteria verified; test evidence recorded in `docs/04.execution/tasks/`.

## Subagent Definition

- **Trigger**: Post-implementation verification gate; regression testing; test plan authoring.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/qa-inspector.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
