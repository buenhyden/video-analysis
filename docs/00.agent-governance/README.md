# 00.agent-governance

> Persona, rules, and memory for autonomous SDLC execution by AI agents.

## Purpose & Scope

This layer establishes the rules of engagement for all AI agents operating within the workspace. It defines "Who" the agents are (Personas), "How" they must work (Rules/SDLC), and "What" they have learned (Memory).

### In Scope

- Root routers (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`).
- SDLC stage-gate procedures and TDD/SDD/DDD rules.
- Agent personas and capability scopes.
- Active methodology, progress, durable agent memory, and policy change traceability.

### Out of Scope

- Implementation code (see root implementation directories).
- Product requirements (see `docs/01.requirements/`).
- Transient runtime output or generated diagnostics (see `_workspace/**`, which is not authoritative).

## Mandatory Templates

- [progress.template.md](../99.templates/progress.template.md) - For `memory/progress.md` active task progress.
- [methodology.template.md](../99.templates/methodology.template.md) - For defining the run state.
- [session-memory.template.md](../99.templates/session-memory.template.md) - For dated durable memory notes.

## Subfolder Policy

Subfolders are allowed only when:
1. They are defined by policy in this directory.
2. Their purpose and relationship to the parent folder are documented in the [Documents](#documents) section.
3. No deeper nesting than one level is permitted without a specific Architecture Decision Record (ADR).

## Naming Rules

- Rules/Scopes: `<slug>.md`
- Memory: `YYYY-MM-DD-<slug>.md`
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and avoid spaces or Windows-reserved characters.

## Lifecycle Rules

Documents in this folder follow the standard lifecycle:

1. **draft**: Initial creation from template. Not yet for implementation.
2. **active**: Reviewed and approved. Source of truth for downstream stages.
3. **completed**: Implementation finished and verified.
4. **deprecated**: Replaced by a newer version or no longer relevant.

## Cross-Reference Rules

- Every Governance rule or persona must be linked in the [Documents](#documents) table below.
- Every rule must be cross-referenced in the root `AGENTS.md` or `CLAUDE.md`.

## Usage Examples

- Update `rules/agentic.md` when the AI Agent-first Engineering contract changes.
- Update `rules/harness-library.md` when an agent, skill, or compatibility runtime surface changes.
- Update `memory/progress.md` when governed AI-agent work crosses a phase boundary, hits a blocker, hands off, or closes.
- Update `policy-change-log.md` only for versioned governance, SDLC protocol, runtime contract, or validator changes.
- Update `sdlc-workflow.md` only when the stable human-agent collaboration flow or baton-passing model changes.
- Use `wiki-curator` only for `docs/LLM-WIKI.md` and reviewed Stage 90 navigation freshness; policy and template changes remain with their owning roles.
- Use `rules/project-initialization-intake.md` before creating any new-project PRD, ARD, spec, plan, task, operations, or reference document.
- Use `rules/template-document-lifecycle.md` before reusing, moving, or deleting template-maintenance history or creating derived-project seed documents.
- Use `rules/environment-readiness.md` before changing setup, validation prerequisites, local tooling assumptions, or runtime readiness policy.
- Use `rules/release-process.md` before preparing a `dev` to `main` release-template PR.
- Update this README and `docs/LLM-WIKI.md` when the active governance surface changes.

## AI Authoring Guidance

1. **Phase 0: Bootstrap**: Always read `rules/bootstrap.md` and root routers first.
2. **Phase 1: Preflight**: Execute `rules/preflight-checklist.md` before any task.
3. **Phase 2: Execution**: Adhere to `git-workflow.md` and `documentation-protocol.md`.
4. **Phase 3: Postflight**: Update `memory/progress.md`, promote durable lessons into `memory/`, record policy changes in `policy-change-log.md`, and run validation scripts.

## AI Execution Checklist

- **Entry Gate**: Root routers (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) are present.
- **Exit Gate**: All governance changes are reflected in this README and linked to relevant rules.
- **Hard Stop Conditions**: STOP if root routers are missing or inconsistent.
- **Evidence Rule**: Every agent action must adhere to the `documentation-protocol.md`.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [compliance](./compliance/) | package | Compliance & Audit Hub | active | 2026-05-09 |
| [data-governance](./data-governance/) | package | Data Governance & Integrity Index | active | 2026-05-09 |
| [memory](./memory/) | package | Memory Hub | active | 2026-05-14 |
| [onboarding-manual.md](./onboarding-manual.md) | md | Onboarding Manual | active | 2026-05-17 |
| [policy-change-log.md](./policy-change-log.md) | md | Workspace Policy Change Log | active | - |
| [providers](./providers/) | package | AI Provider Notes Index | active | 2026-05-12 |
| [rules](./rules/) | package | Governance Rules Index | active | 2026-05-21 |
| [scopes](./scopes/) | package | Agent Scope Definitions Index | active | 2026-05-12 |
| [sdlc-workflow.md](./sdlc-workflow.md) | md | Visual SDLC & Baton Passing | active | 2026-05-10 |

## Core Rules

- [rules/agentic.md](./rules/agentic.md) - Agent Operating Procedure and AI Agent-first Engineering contract.
- [rules/bootstrap.md](./rules/bootstrap.md) - Mandatory session bootstrap order and stage-gate authority.
- [rules/environment-readiness.md](./rules/environment-readiness.md) - Built-in workspace assets, local prerequisite classes, setup policy, and local-only surface boundaries.
- [rules/harness-library.md](./rules/harness-library.md) - Active harness inventory and lifecycle contract.
- [rules/persona.md](./rules/persona.md) - Persona activation, scope mapping, and write boundary contract.
- [rules/preflight-checklist.md](./rules/preflight-checklist.md) - Entry, execution, and exit checks before governed work closes.
- [rules/project-initialization-intake.md](./rules/project-initialization-intake.md) - Required product/software and stack intake before derived-project stage authoring.
- [rules/release-process.md](./rules/release-process.md) - Release-template promotion process from `dev` maintenance history to clean `main` skeleton.
- [rules/stage-gate-matrix.md](./rules/stage-gate-matrix.md) - Stage ownership, template selection, hard stops, and evidence criteria.
- [rules/standards.md](./rules/standards.md) - Balanced router, lazy-loading, runtime inventory, model, and provider standards.
- [rules/subagent-protocol.md](./rules/subagent-protocol.md) - Bounded subagent dispatch, file ownership, and acceptance protocol.
- [rules/template-document-lifecycle.md](./rules/template-document-lifecycle.md) - Ownership labels, branch contract, cleanup rules, and derived-project seed policy.

## Related Documents

- [AGENTS.md](../../AGENTS.md) - Workspace Root Router
- [LLM-Wiki](../../docs/LLM-WIKI.md) - Workspace SDLC Rules

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
