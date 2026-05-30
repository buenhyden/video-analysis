---
title: AI Provider Notes Index
version: 1.0.0
owner: Governance Architect
layer: governance
stage: 00
status: active
last-updated: 2026-05-12
---

# AI Provider Notes

## Overview

This directory contains provider-specific behavioral notes for each AI runtime supported by this workspace. These files document provider deltas — behaviors, constraints, and integration patterns that differ from the shared `AGENTS.md` contract. They are loaded on demand and do not define policy independently.

## Audience

AI agents that need provider-specific runtime guidance, and workspace maintainers managing multi-provider compatibility.

## Scope

### In Scope

- Runtime-specific instruction hierarchy and memory model notes.
- Hook execution and settings wiring for each provider.
- AGENTS bridge strategy and modular expansion guidance per provider.

### Out of Scope

- Shared workspace policy (belongs in `AGENTS.md` and `docs/00.agent-governance/rules/`).
- Application stack configuration (belongs in implementation layer).
- GitHub-native AI instruction files (explicitly prohibited by `AGENTS.md §Non-Negotiable Rules`).

## Structure

| File           | Provider      | Purpose                                                                                |
| :------------- | :------------ | :------------------------------------------------------------------------------------- |
| `agents-md.md` | All providers | Notes on `AGENTS.md` usage, bridge strategy, and cross-provider policy routing         |
| `claude.md`    | Claude Code   | Claude-specific instruction hierarchy, hook runtime, memory model, and GitHub boundary |
| `gemini.md`    | Gemini CLI    | Gemini-specific tool mapping, skill activation, and AGENTS.md bridge                   |

## How to Work in This Area

1. Load the provider note file matching the active AI runtime at session start.
2. Keep provider notes minimal and delta-only — shared policy belongs in `AGENTS.md`.
3. Apply `project-initialization-intake.md` before a provider creates project stage documents in a derived workspace.
4. Do not add GitHub-native AI instruction layers (e.g., `.github/copilot-instructions.md`) as alternatives to these files.
5. When adding a new provider, create `<provider>.md` following the existing file structure and link it from `AGENTS.md §Runtime Entrypoints`.

## AI Execution Checklist

- [ ] **Entry Gate**: Correct provider note loaded for the active runtime.
- [ ] **Procedure**: Apply only provider-specific deltas; do not duplicate shared `AGENTS.md` policy here.
- [ ] **Exit Gate**: Any new provider file is linked from `AGENTS.md` and `docs/LLM-WIKI.md`.
- [ ] **Hard Stop**: STOP if a provider note contradicts `AGENTS.md` — provider notes must extend, not override, the shared contract.

## Documents

| File                           | Type | Summary                                                              | Status | Last Modified |
| ------------------------------ | ---- | -------------------------------------------------------------------- | ------ | ------------- |
| [agents-md.md](./agents-md.md) | md   | AGENTS.md usage, bridge strategy, and cross-provider policy routing  | active | 2026-05-10    |
| [claude.md](./claude.md)       | md   | Claude-specific instruction hierarchy, hook runtime, memory model    | active | 2026-05-22    |
| [gemini.md](./gemini.md)       | md   | Gemini-specific tool mapping, skill activation, and AGENTS.md bridge | active | 2026-05-10    |

## Related Documents

- [Stage 00 Governance README](../README.md)
- [AGENTS.md](../../../AGENTS.md)
- [Claude Runtime](../../../.claude/CLAUDE.md)
- [Bootstrap Protocol](../rules/bootstrap.md)
- [Project Initialization Intake](../rules/project-initialization-intake.md)
- [Harness Library](../rules/harness-library.md)

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
