# Product Layer Scope (March 2026)

`layer: product`

This scope defines requirements for the Product Manager persona.

## 1. Core Responsibilities

- **Stage 01 (PRD)**: define product intent, value, and acceptance criteria.
- **Stage 05 (Plans)**: ensure execution plans align with approved product scope.
- **Cross-Stage Traceability**: maintain explicit links from PRD to Spec/Plan/Task.

## 2. Canonical Paths

- PRD index and artifacts: `docs/01.requirements/`
- Execution plans: `docs/04.execution/plans/`
- Supporting references: `docs/90.references/`

## 3. Template Mapping

- `prd.template.md`
- `plan.template.md`
- `task.template.md` (for plan-to-execution tracing)

## 4. Quality Focus

- scope clarity (in/out)
- measurable acceptance criteria
- decision traceability from product intent to implementation

## File Ownership

- **Allowed Write**: `docs/01.requirements/**` · `docs/04.execution/plans/**`
- **Forbidden Write**: implementation paths · runtime infrastructure paths · `docs/99.templates/**`
- **Pre-condition**: Stakeholder goals and business constraints confirmed before PRD authoring.
- **Post-condition**: PRD contains explicit scope (in/out), measurable acceptance criteria, and non-goals.

## Subagent Definition

- **Trigger**: Feature inception, PRD update, or execution plan alignment task.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/product-manager.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
