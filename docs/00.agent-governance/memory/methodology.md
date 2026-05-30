---
title: Workspace Methodology State
version: 1.0.0
owner: Governance Architect
layer: meta
stage: 00
status: active
last-updated: 2026-05-17
---

# Workspace Methodology State

## Purpose

This file records the active methodology selection and run-state memory for governed SDLC work in this template.

## Overview

`docs/00.agent-governance/memory/methodology.md` is the canonical tracked location for active methodology state. `_workspace/methodology.md` must not be used as the authoritative methodology source.

Active methodology is a run-state record, not an independent policy store. Stage 00 rules and templates define the allowed methodology options, hard stops, and required evidence; this file records which option is active for the current governed run.

## Active Methodology

- **Choice**: `HYBRID`
- **Reason**: The source template combines structured stage-gate artifacts with flexible iteration.
- **Set by**: Governance baseline
- **Set on**: 2026-05-10

## Methodology Descriptions

| Methodology | Best For                                                   | Key Templates       |
| ----------- | ---------------------------------------------------------- | ------------------- |
| `SCRUM`     | Time-boxed sprints, defined team, recurring retrospectives | `plan.template.md`  |
| `LEAN`      | Hypothesis-driven MVP and early validation                 | `prd.template.md`   |
| `KANBAN`    | Continuous flow, operations, or support work               | `plan.template.md`  |
| `HYBRID`    | Structured specs with flexible iteration                   | All stage templates |

## Current Run State

- **Phase**: `task-complete`
- **Last completed phase**: Scripts usage cleanup and QA evidence gate validation
- **Next phase**: None - user-approved cleanup plan complete
- **Blockers**: None recorded

## Authority Boundary

| Surface                  | Responsibility                                                                     |
| ------------------------ | ---------------------------------------------------------------------------------- |
| `methodology.md`         | Active methodology selection, rationale, and current run-state memory.             |
| `progress.md`            | Current task progress, handoff state, blockers, and durable run notes.             |
| Stage 00 rules/templates | Methodology taxonomy, hard stops, evidence requirements, and agent behavior rules. |
| `_workspace/**`          | Transient supporting output only; never authoritative methodology state.           |

## AI Execution Checklist

- [x] **Entry Gate**: Methodology state is tracked in Stage 00 memory.
- [x] **Exit Gate**: `Choice`, `Reason`, `Set by`, and `Set on` fields are populated.
- [x] **Hard Stop Conditions**: STOP if `_workspace/methodology.md` conflicts with this file.
- [x] **Evidence Rule**: Methodology changes must link to the related plan, task, ADR, or user request.

## Related Documents

- [Memory README](./README.md)
- [Session Progress](./progress.md)
- [Documentation Protocol](../rules/documentation-protocol.md)
- [Methodology Template](../../99.templates/methodology.template.md)
