---
title: <string>
version: <string>
owner: <string>
layer: meta
stage: 00
status: active
last-updated: YYYY-MM-DD
---

# Methodology Selection

<!-- Target: docs/00.agent-governance/memory/methodology.md -->

## Usage Guidance

- **When to use**: Created or updated at Phase 0 of `spec-driven-sdlc` before any other phase runs.
- **Mandatory sections**: Active Methodology, Current Run State.
- **Naming rule**: `methodology.md` within `docs/00.agent-governance/memory/`.
- **Hard Stops**: STOP if Choice is not one of the allowed types. STOP if Reason is empty.

## Purpose

The Methodology Selection document defines the active process selection and run-state memory for the current project run. It ensures all agents align on the process (Scrum, Lean, etc.) and tracks the current SDLC phase.

`docs/00.agent-governance/memory/methodology.md` is authoritative. `_workspace/methodology.md` is not a canonical source.

Active methodology is not an independent policy store. Stage 00 rules and templates define allowed methodology options, hard stops, and required evidence; this file records which option is active for the current governed run.

---

## Active Methodology

- **Choice**: `HYBRID`
  <!-- options: SCRUM | LEAN | KANBAN | HYBRID -->
- **Reason**: [Why this methodology was chosen — e.g., "Short iteration cycles needed with stable backlog"]
- **Set by**: [Agent or human who made the selection]
- **Set on**: YYYY-MM-DD

## Methodology Descriptions

| Methodology | Best For | Key Templates |
| --- | --- | --- |
| `SCRUM` | Time-boxed sprints, defined team, recurring retrospectives | `plan.template.md` (Sprint Iteration overlay) |
| `LEAN` | Hypothesis-driven MVP, early-stage validation | `prd.template.md` (Lean Canvas overlay) |
| `KANBAN` | Continuous flow, ops/support work, no fixed sprints | `plan.template.md` (Kanban Board overlay) |
| `HYBRID` | Most projects — structured specs with flexible iteration | All templates; methodology overlays per stage |

## Current Run State

- **Phase**: `[0–10 or "completed"]`
- **Last completed phase**: [Phase number and name]
- **Next phase**: [Phase number and name]
- **Blockers**: [None | describe any blockers]

## Authority Boundary

| Surface | Responsibility |
| --- | --- |
| `methodology.md` | Active methodology selection, rationale, and current run-state memory. |
| `progress.md` | Current task progress, handoff state, blockers, and durable run notes. |
| Stage 00 rules/templates | Methodology taxonomy, hard stops, evidence requirements, and agent behavior rules. |
| `_workspace/**` | Transient supporting output only; never authoritative methodology state. |

## Notes

[Additional context about methodology choices, constraints, or deviations from standard flow.]

## Target-Relative Link Guidance

- This file lives at `docs/00.agent-governance/memory/methodology.md`.
- Link the template catalog as `[../../99.templates/README.md]`.
- Link memory siblings as `[./README.md]` and `[./progress.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

- **Entry Gate**: this file is created before any governed phase output is written.
- **Exit Gate**: `Choice`, `Reason`, and `Set on` fields are filled; phase state is current.
- **Hard Stop Conditions**: STOP if `Choice` is not one of `SCRUM`, `LEAN`, `KANBAN`, or `HYBRID`. STOP if `Reason` is empty or the current phase state conflicts with existing canonical stage documents.
- **Downstream Trigger**: `spec-driven-sdlc` skill reads the Stage 00 memory methodology state at startup; update `Current Run State` after each phase completes.
- **Evidence Rule**: methodology changes mid-run must record the previous choice and reason for the change.

## Related Documents

- **Template Index**: `[../../99.templates/README.md]`
- **Memory README**: `[./README.md]`
- **SDLC Skill**: `[../../../.claude/skills/spec-driven-sdlc/skill.md]`
