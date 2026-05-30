# Documentation Layer Scope (March 2026)

`layer: docs`

This scope defines the requirements and standards for the Technical Writer and Documentation Specialist personas.

## 1. Core Responsibilities

- **Taxonomy Stewardship**: Maintain the compact Stage-Gate Taxonomy plus supporting `docs/90.references/` and `docs/99.templates/` integrity.
- **Stage 07 (Guides)**: Maintain user/developer guides in `docs/05.operations/guides/`. Use `guide.template.md`.
- **Metadata Audit**: Ensure `layer`, `stage`, and `status` are correct for JIT loading.
- **Template Standards**: Enforce usage of `docs/99.templates/` for ALL documentation.

## 2. Standard Taxonomy

- **Guides**: Grounded in `guide.template.md`.
- **References**: Found in `docs/90.references/`. Use `reference.template.md`.
- **Operations**: Maintenance knowledge in `docs/05.operations/policies/` using `operation.template.md`.

## 3. Required Metadata

```markdown
---
layer: docs
stage: 00
---
```

## 4. Skills Engagement

- `help-skill`
- `technical-writing`
- `writing-plans`
- `doc-coauthoring`
- `code-documentation-doc-generate`
- `mermaid-diagrams`

## File Ownership

- **Allowed Write**: `docs/05.operations/guides/**` · `docs/05.operations/policies/**` · `docs/05.operations/runbooks/**` · `docs/90.references/**`
- **Forbidden Write**: `docs/99.templates/**` · implementation paths unless explicitly assigned
- **Pre-condition**: Implemented behavior is stable before guide authoring begins.
- **Post-condition**: Guide is reproducible by intended audience; README updated in modified folder.

## Subagent Definition

- **Trigger**: Guide authoring after behavior stabilizes, or reference documentation update.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/technical-writer.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
