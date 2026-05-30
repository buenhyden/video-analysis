---
title: Memory Hub
version: 1.0.0
owner: Governance Architect
layer: meta
stage: 00
status: active
last-updated: 2026-05-14
---

# Memory

## Overview

This directory stores active methodology, active task progress, durable agent memory, lessons learned, and non-obvious findings that should survive across implementation cycles. Memory records reduce repeated mistakes without replacing canonical governance documents.

## Audience

This README is for agents and maintainers deciding whether an insight belongs in a governed memory record or in a more authoritative Stage 00 rule.

## Scope

### In Scope

- Active methodology and run-state tracking.
- Active task progress for governed AI-agent work.
- Non-obvious lessons from completed work.
- Regression risks discovered during validation.
- Historical context that helps future agents understand prior decisions.
- README inventory for memory documents.

### Out of Scope

- Secrets, credentials, tokens, private keys, or sensitive logs.
- Temporary status updates that belong only in the current conversation.
- Durable policy rules that should be promoted to Stage 00 governance.
- Versioned policy, SDLC protocol, runtime contract, or validator changes, which belong in `../policy-change-log.md`.

## Structure

| Area                | Purpose                                                            |
| :------------------ | :----------------------------------------------------------------- |
| `methodology.md`    | Canonical methodology and run-state memory for governed SDLC work. |
| `progress.md`       | Active session progress and durable notes.                         |
| Future memory files | Focused records created from the session memory template.          |

## Authority Boundaries

| Surface                       | Owns                                                                                             | Does Not Own                                                                          |
| :---------------------------- | :----------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `memory/methodology.md`       | Current methodology choice and run-state memory.                                                 | Allowed methodology taxonomy or policy hard stops.                                    |
| `memory/progress.md`          | Active task status, phase progress, handoff state, blockers, and durable run notes.              | Versioned policy history or final stage evidence.                                     |
| `memory/YYYY-MM-DD-<slug>.md` | Focused durable lessons and non-obvious context.                                                 | Obvious status updates or active task checklists.                                     |
| `../policy-change-log.md`     | Versioned governance, SDLC protocol, runtime contract, and validator changes.                    | Active progress, methodology selection, or lessons learned.                           |
| `../sdlc-workflow.md`         | Stable human-agent collaboration flow and baton-passing model.                                   | Active progress, methodology selection, lessons learned, or versioned policy history. |
| `_workspace/**`               | Transient coordination, generated diagnostics, generated intelligence, and local scratch output. | Policy, methodology, progress, durable memory, or final governed deliverables.        |

## How to Work in This Area

1. Update `progress.md` at phase boundaries, blockers, handoffs, and task closure for governed AI-agent work.
2. Add dated memory files only for information that is durable and likely to prevent future errors.
3. Prefer updating canonical governance and `policy-change-log.md` when the note is actually a policy or validator change.
4. Link the source incident, task, ADR, plan, validation command, or user request that generated the memory.
5. Keep this README `Documents` table synchronized after adding or removing memory files.

## Templates

- **Progress**: `../../99.templates/progress.template.md`
- **Methodology**: `../../99.templates/methodology.template.md`
- **Durable memory note**: `../../99.templates/session-memory.template.md`

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [methodology.md](./methodology.md) | md | Workspace Methodology State | active | 2026-05-17 |
| [progress.md](./progress.md) | md | Session Progress | active | 2026-05-18 |

## Lifecycle Rules

- **Naming**: `methodology.md`, `progress.md`, or dated focused memory files (`YYYY-MM-DD-<slug>.md`).
- **Status**: `active` -> `archived`
- **Cleanup**: Archive or merge memories that are integrated into core standards.
- **Authority**: `docs/00.agent-governance/memory/` is the canonical tracked home for active methodology, progress, and durable agent memory. `_workspace/**` may support transient coordination, but it is not authoritative memory.

## AI Execution Checklist

- [ ] **Entry Gate**: Governed task progress, methodology state, non-obvious insight, complex issue resolution, or postmortem complete.
- [ ] **Exit Gate**: `progress.md`, `methodology.md`, or a dated memory record is current and linked to relevant evidence.
- [ ] **Hard Stop Conditions**: STOP if the entry is redundant, obvious, transient, policy history, or belongs in `_workspace/**`.
- [ ] **Evidence Rule**: Link to the original incident, task, ADR, validation command, or user request that generated the memory.

## Related Documents

- [Stage 00 Governance](../README.md)
- [Progress Template](../../99.templates/progress.template.md)
- [Methodology Template](../../99.templates/methodology.template.md)
- [Session Memory Template](../../99.templates/session-memory.template.md)
- [Documentation Protocol](../rules/documentation-protocol.md)
- [Policy Change Log](../policy-change-log.md)
- [SDLC Workflow](../sdlc-workflow.md)

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
