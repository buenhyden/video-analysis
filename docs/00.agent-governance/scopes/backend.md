# Backend Layer Scope (March 2026)

`layer: backend`

This scope defines the technical constraints for the Backend Engineer persona.

## 1. Core Responsibilities

- **Stage 04 (Specs)**: Implement technical specs in `docs/03.specs/`. Use `spec.template.md`.
- **Stage 05 (Plans)**: Create implementation plans in `docs/04.execution/plans/`. Use `plan.template.md`.
- **Contract-First**: Define machine-readable contracts in `contracts/` before any logic.

## 2. Standard Taxonomy

- **API Spec**: Use `api-spec.template.md` and `openapi.template.yaml`.
- **Data model**: Use `expanded/tactical-model.template.md` or `extended/schema.template.graphql` (if GraphQL is in scope).
- **Implementation**: MUST be grounded in `docs/03.specs/` and `docs/04.execution/plans/`.

## 3. Required Metadata

```markdown
---
layer: backend
stage: 00
---
```

## 4. Skills Engagement

- `api-design-principles`
- Project-declared backend language, framework, database, and runtime skills from intake only.
- Examples such as `nodejs-backend-patterns`, `postgresql-optimization`, or `fastapi-pro` apply only after the derived project explicitly chooses those technologies.

## File Ownership

- **Allowed Write**: project-declared backend implementation paths · `docs/04.execution/tasks/**`
- **Forbidden Write**: unrelated implementation paths · `.github/**` · `docs/99.templates/**`
- **Pre-condition**: Approved Spec exists in `docs/03.specs/` before writing implementation.
- **Template Note**: The minimal template does not provide a default backend root. A consuming project must declare backend paths before implementation work.
- **Post-condition**: Implementation evidence recorded in `docs/04.execution/tasks/`; tests pass.

## Subagent Definition

- **Trigger**: Backend implementation task after Spec approval; API or data-layer work.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/backend-engineer.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
