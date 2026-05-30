---
title: Governance Rules Index
version: 1.0.0
owner: Governance Architect
layer: governance
stage: 00
status: active
last-updated: 2026-05-21
---

# Governance Rules

## Overview

This directory contains the mandatory governance rule files loaded by all agents during the bootstrap sequence. Each file defines a specific policy domain and is loaded on demand using the lazy-load principle from `bootstrap.md`.

## Audience

AI agents performing any task in this workspace, and human maintainers managing governance policy.

## Scope

### In Scope

- Agent operating procedures, persona activation, and scope definitions.
- SDLC stage-gate rules, Git workflow policy, and CI/CD workflow governance.
- Documentation protocol, quality standards, and reference integrity checks.
- Sub-agent, swarm, and evolution protocol definitions.

### Out of Scope

- Project-specific feature specs (belong in `docs/03.specs/`).
- Execution plans and task evidence (belong in `docs/04.execution/`).
- Provider-specific notes (belong in `docs/00.agent-governance/providers/`).

## Structure

| File                              | Purpose                                                                                   |
| :-------------------------------- | :---------------------------------------------------------------------------------------- |
| `agentic.md`                      | Agent Operating Procedure (AOP) — core execution loop and hard stops                      |
| `bootstrap.md`                    | Bootstrap sequence — mandatory entry point for all agent sessions                         |
| `ci-cd-workflow.md`               | Branch-based CI/CD policy, job permissions, and workflow governance                       |
| `design-system.md`                | Frontend/mobile/app design-system gate — blocks UI work before `DESIGN.md` is initialized |
| `documentation-protocol.md`       | Documentation authoring protocol for human readability and AI execution                   |
| `environment-readiness.md`        | Local prerequisite classes, workspace asset boundary, and non-mutating setup contract     |
| `evolution-protocol.md`           | Automated intelligence-hub protocol for template evolution                                |
| `git-workflow.md`                 | Mandatory Git and PR strategy (branch model, merge policy, commit format)                 |
| `github-repository-governance.md` | GitHub repository security and operational policy SSOT                                    |
| `harness-library.md`              | Active harness inventory — canonical agent, hook, and skill registry                      |
| `persona.md`                      | Persona and scope activation protocol for all task types                                  |
| `postflight-checklist.md`         | Post-task checklist — run before marking any session complete                             |
| `preflight-checklist.md`          | Pre-task checklist contract — gates every work session entry                              |
| `project-initialization-intake.md` | New-project product/software and stack intake gate                                      |
| `quality-standards.md`            | Quality gate definitions for code, docs, and governance artifacts                         |
| `reference-integrity.md`          | Protocol for detecting and fixing broken internal references                              |
| `release-process.md`              | Dev-to-main release-template promotion, focused dev back-sync, and distribution validation process |
| `sdlc-procedure.md`               | SDLC Standard Operating Procedure — stage ownership and handoff flow                      |
| `stage-gate-matrix.md`            | Stage-Gate Matrix (00–10) — purpose, inputs, outputs, and completion criteria per stage   |
| `standards.md`                    | Root-router, context-loading, and policy-consistency standards                            |
| `subagent-protocol.md`            | Sub-agent creation rules, file-ownership enforcement, and acceptance criteria             |
| `swarm-protocol.md`               | Multi-agent swarm collaboration protocol for complex tasks                                |
| `template-document-lifecycle.md`   | Template document ownership, branch contract, and derived-project seed policy             |

## How to Work in This Area

1. Load rules via `bootstrap.md` using the lazy-load principle — load only the rules required for the active task.
2. Do not add new rule files without a governance review and `harness-library.md` update.
3. Do not rename or relocate rule files without updating all `@import` references in `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `.claude/CLAUDE.md`.
4. Run `bash scripts/validation/validate-cross-links.sh` after any path change to confirm no broken references.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [agentic.md](./agentic.md) | md | Agent Operating Procedure (AOP) | active | - |
| [bootstrap.md](./bootstrap.md) | md | Agent Bootstrap Governance (March 2026) | active | - |
| [ci-cd-workflow.md](./ci-cd-workflow.md) | md | CI/CD Workflow Governance (May 2026) | active | - |
| [design-system.md](./design-system.md) | md | Design System Governance | active | - |
| [documentation-protocol.md](./documentation-protocol.md) | md | Documentation Protocol (March 2026) | active | - |
| [environment-readiness.md](./environment-readiness.md) | md | Environment Readiness | active | 2026-05-21 |
| [evolution-protocol.md](./evolution-protocol.md) | md | Evolution Protocol: AI-Driven Improvements | active | - |
| [git-workflow.md](./git-workflow.md) | md | Git Workflow Governance (May 2026) | active | - |
| [github-repository-governance.md](./github-repository-governance.md) | md | GitHub Repository Governance (April 2026) | active | - |
| [harness-library.md](./harness-library.md) | md | Active Harness Governance Rule | active | - |
| [persona.md](./persona.md) | md | AI Agent Persona Protocol (March 2026) | active | - |
| [postflight-checklist.md](./postflight-checklist.md) | md | Postflight Checklist (April 2026) | active | - |
| [preflight-checklist.md](./preflight-checklist.md) | md | Preflight Checklist Contract | active | - |
| [project-initialization-intake.md](./project-initialization-intake.md) | md | Project Initialization Intake | active | 2026-05-21 |
| [quality-standards.md](./quality-standards.md) | md | quality-standards.md | active | - |
| [reference-integrity.md](./reference-integrity.md) | md | Reference Integrity Protocol | active | - |
| [release-process.md](./release-process.md) | md | Project Template Release Process | active | 2026-05-22 |
| [sdlc-procedure.md](./sdlc-procedure.md) | md | SDLC Standard Operating Procedure (SOP) | active | - |
| [stage-gate-matrix.md](./stage-gate-matrix.md) | md | Stage-Gate Matrix (00-10) | active | - |
| [standards.md](./standards.md) | md | AI Agent Standards (May 2026) | active | 2026-05-22 |
| [subagent-protocol.md](./subagent-protocol.md) | md | Subagent Protocol (April 2026) | active | - |
| [swarm-protocol.md](./swarm-protocol.md) | md | Swarm Protocol: Multi-Agent Collaboration | active | - |
| [template-document-lifecycle.md](./template-document-lifecycle.md) | md | Template Document Lifecycle and Ownership | active | 2026-05-22 |

## AI Execution Checklist

- [ ] **Entry Gate**: Confirm the rule file needed for the active task is loaded via `bootstrap.md`.
- [ ] **Procedure**: Load only the rules required. Do not bulk-load all 23 files unless performing a governance audit.
- [ ] **Exit Gate**: Confirm rule changes are reflected in `harness-library.md` and `policy-change-log.md`.
- [ ] **Hard Stop**: STOP if a rule file is missing a `## Role definition`, `## Procedure`, or `## Constraints` section.

## Role definition

- Applies to all agents loading governance rules and human maintainers managing policy files in this directory.

## Procedure

- Follow the bootstrap load order in `bootstrap.md`: load only the rule files required for the active task.
- Do not add, rename, or remove rule files without updating `harness-library.md` when runtime inventory changes and `policy-change-log.md` when the governance contract changes.

## Constraints

- Ensure compliance with overall workspace SDLC as defined in `sdlc-procedure.md` and `stage-gate-matrix.md`.
- All rule files in this directory must maintain the 4-part agent instruction structure (Role definition, Procedure, Constraints, File references).

## File references

- `docs/LLM-WIKI.md`
- `docs/00.agent-governance/rules/harness-library.md`
- `docs/00.agent-governance/rules/bootstrap.md`

## Related Documents

- [Stage 00 Governance README](../README.md)
- [Bootstrap Protocol](./bootstrap.md)
- [Environment Readiness](./environment-readiness.md)
- [Harness Library](./harness-library.md)
- [Agent Operating Procedure](./agentic.md)
- [Release Process](./release-process.md)
- [Stage-Gate Matrix](./stage-gate-matrix.md)
- [Template Document Lifecycle](./template-document-lifecycle.md)

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
