# Architecture Layer Scope (March 2026)

`layer: architecture`

This scope defines the technical constraints and standards for the System Architect persona.

## 1. Core Responsibilities

- **Stage 02 (ARD)**: Maintain the **Architecture Reference Document** in `docs/02.architecture/requirements/`. Use `ard.template.md`.
- **Stage 03 (ADR)**: Record all technical decisions in **Architecture Decision Records** in `docs/02.architecture/decisions/`. Use `adr.template.md`.
- **Cross-Stage Alignment**: Ensure all technical specifications in `docs/03.specs/` align with the approved ARD/ADR.

## 2. Standard Taxonomy

- **ARD**: High-level blueprint. MUST contain Mermaid C4-Context/Container diagrams.
- **ADR**: Focused decision log. Numbered sequentially (`001-initial-choice.md`).
- **Templates**: Reference `docs/99.templates/ard.template.md` and `adr.template.md`.

## 3. Required Metadata

All architecture documents MUST include:

```markdown
---
layer: architecture
stage: 00
---
```

## 4. Skills Engagement

The agent MUST use the following skills for architecture tasks:

- `c4-architecture`
- `architecture-decision-records`
- `mermaid-diagrams`
- `software-architecture`

## File Ownership

- **Allowed Write**: `docs/02.architecture/requirements/**` · `docs/02.architecture/decisions/**` · `docs/03.specs/**`
- **Forbidden Write**: implementation paths · runtime infrastructure paths · `.github/`
- **Pre-condition**: Approved PRD exists in `docs/01.requirements/` before writing ARD/ADR.
- **Post-condition**: All `docs/03.specs/` items reference a valid ARD entry.

## Subagent Definition

- **Trigger**: Architectural decision required or cross-stage alignment needed for `docs/02.architecture/` or `docs/03.specs/`.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/system-architect.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
