---
title: Agent Scope Definitions Index
version: 1.0.0
owner: Governance Architect
layer: governance
stage: 00
status: active
last-updated: 2026-05-19
---

# Agent Scope Definitions

## Overview

This directory contains the scope definition files that map each specialist agent to its authorized work domain. Scopes are loaded during persona activation (see `rules/persona.md`) and define the file-ownership boundaries enforced during task execution.

## Audience

AI agents performing persona activation, and governance maintainers managing agent authority boundaries.

## Scope

### In Scope

- Layer-specific file ownership, tools, and stage access for each specialist persona.
- Metadata and taxonomy engineering scope for governance infrastructure.
- LLM-WIKI curation authority and update triggers.

### Out of Scope

- Agent runtime configuration (belongs in `.claude/agents/*.md`).
- Execution task assignment (belongs in `docs/04.execution/plans/`).
- Provider-specific behavioral notes (belongs in `docs/00.agent-governance/providers/`).

## Structure

| File              | Persona                            | Authority Domain                                                        |
| :---------------- | :--------------------------------- | :---------------------------------------------------------------------- |
| `architecture.md` | System Architect                   | Stage 02–03 — ARD, ADR, DDD modeling, structural integrity              |
| `backend.md`      | Backend Engineer                   | Stage 04, 06 — API contracts, domain logic, persistence                 |
| `docs.md`         | Docs Governance / Technical Writer | Stage 07 — documentation authoring, README governance                   |
| `frontend.md`     | Frontend Engineer                  | Stage 04, 06 — UI flows, client state, accessibility                    |
| `infra.md`        | Infra DevOps                       | Stage 08–09 — CI/CD, deployment workflows, operational readiness        |
| `meta.md`         | Metadata & Taxonomy Engineer       | Governance taxonomy, frontmatter standards, classification              |
| `ops.md`          | Ops Manager / SRE                  | Stage 08–10 — SOPs, runbooks, SLOs, incident tracking                   |
| `product.md`      | Product Manager                    | Stage 01, 05 — PRD creation, prioritization, planning                   |
| `qa.md`           | QA Inspector                       | Stage 05–06 — integration boundaries, regression, acceptance            |
| `security.md`     | Security Engineer                  | Stage 04, 10 — threat modeling, trust boundaries, incident security     |
| `wiki.md`         | Wiki Curator                       | `docs/LLM-WIKI.md` |

## How to Work in This Area

1. Load the scope file matching the active persona during task setup.
2. Confirm all planned file edits fall within the scope's authorized stage and path list.
3. Do not expand a scope file without a governance review; scope expansion requires an ADR or policy-change-log entry.
4. Run `bash scripts/ws.sh validate` after any scope-boundary change to confirm agent coverage parity.

## Documents

| File                                 | Type | Summary                                                      | Status | Last Modified |
| ------------------------------------ | ---- | ------------------------------------------------------------ | ------ | ------------- |
| [architecture.md](./architecture.md) | md   | System Architect scope — Stage 02–03, ARD, ADR, DDD          | active | 2026-05-10    |
| [backend.md](./backend.md)           | md   | Backend Engineer scope — Stage 04, 06, API and persistence   | active | 2026-05-19    |
| [docs.md](./docs.md)                 | md   | Docs Governance / Technical Writer scope — Stage 07          | active | 2026-05-10    |
| [frontend.md](./frontend.md)         | md   | Frontend Engineer scope — Stage 04, 06, UI and accessibility | active | 2026-05-10    |
| [infra.md](./infra.md)               | md   | Infra DevOps scope — Stage 08–09, CI/CD and deployment       | active | 2026-05-10    |
| [meta.md](./meta.md)                 | md   | Metadata & Taxonomy Engineering scope — governance taxonomy  | active | 2026-05-10    |
| [ops.md](./ops.md)                   | md   | Ops Manager / SRE scope — Stage 08–10, runbooks and SLOs     | active | 2026-05-19    |
| [product.md](./product.md)           | md   | Product Manager scope — Stage 01, 05, PRD and planning       | active | 2026-05-10    |
| [qa.md](./qa.md)                     | md   | QA Inspector scope — Stage 05–06, integration and acceptance | active | 2026-05-19    |
| [security.md](./security.md)         | md   | Security Engineer scope — Stage 04, 10, threat and incidents | active | 2026-05-10    |
| [wiki.md](./wiki.md)                 | md   | Wiki Curator scope — LLM-WIKI operating summary              | active | 2026-05-19    |

## AI Execution Checklist

- [ ] **Entry Gate**: Active persona scope loaded before any file edit.
- [ ] **Procedure**: Verify each planned file path is within the authorized domain listed above.
- [ ] **Exit Gate**: Scope boundaries respected throughout execution; no out-of-scope edits made.
- [ ] **Hard Stop**: STOP if the task requires editing a file outside the active persona's authorized stage range.

## Related Documents

- [Stage 00 Governance README](../README.md)
- [Persona Activation Protocol](../rules/persona.md)
- [Harness Library](../rules/harness-library.md)
- [Claude Agents](../../../.claude/agents/)

---

## Docs 3 Global Rules Reference

> Active on every task. HALT conditions enforced by agents.
> Applies when creating or changing governed documentation in this folder.
> Full definitions: `docs/00.agent-governance/rules/documentation-protocol.md §7`

| Rule                       | Summary                                                                              | HALT If                                          |
| :------------------------- | :----------------------------------------------------------------------------------- | :----------------------------------------------- |
| **R1 — Content Creation**  | Read template before creating any stage doc. Fill all sections. Set `status: draft`. | Template missing or `[placeholder]` text remains |
| **R2 — Auto-Indexing**     | Update this README after every change to this folder.                                | README not updated after folder change           |
| **R3 — Cross-Referencing** | Every stage doc must have `## Related Documents` with relative upstream links.       | Required upstream links absent                   |
