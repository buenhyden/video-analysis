---
name: spec-driven-sdlc
description: Orchestrates the workspace SDLC from PRD through operations, using the active agent roster and stage-gate rules. Use for end-to-end document-driven delivery.
---

# Spec-Driven SDLC Orchestrator

Coordinate the stage-gated delivery flow for this workspace.

## Startup Check

Review `docs/00.agent-governance/memory/` before starting:

- missing `docs/00.agent-governance/memory/progress.md`: create it from `docs/99.templates/progress.template.md`
- no active progress state in `progress.md`: start a new run and record it there
- in-progress state in `progress.md`: resume from the next incomplete phase
- completed state in `progress.md`: archive durable context if needed, then start a new run
- **LLM-Wiki Initialization**: Read `docs/LLM-WIKI.md` to load workspace-wide SDLC, TDD, SDD, and DDD constraints before executing any phase.
- missing `docs/00.agent-governance/memory/methodology.md`: create it from `docs/99.templates/methodology.template.md` with `HYBRID` default; record the assumption in the PRD
- frontend/mobile/app/UI scope: fill root `DESIGN.md` in place before Stage 04 approval; do not create a `docs/99.templates` design-system template
- `_workspace/**` may be inspected as transient supporting input only; it cannot override Stage 00 governance or memory.
- new derived project with no intake: collect product/software and stack intake using `docs/00.agent-governance/rules/project-initialization-intake.md` before creating PRD, ARD, spec, plan, task, operations, or reference documents.

## Phase Map

0. Methodology selection: record choice in `docs/00.agent-governance/memory/methodology.md` — options: `SCRUM`, `LEAN`, `KANBAN`, `HYBRID`
1. Product definition: create or reuse `docs/01.requirements/YYYY-MM-DD-<feature>.md` after intake is complete
2. Architecture reference: create or reuse `docs/02.architecture/requirements/####-<system-or-domain>.md`; add DDD companion docs when triggered
3. Architecture decisions: create ADRs in `docs/02.architecture/decisions/` only for significant decisions
4. Specification: create `docs/03.specs/<feature-id>/spec.md` and companion API/data/tests/agent docs as needed
5. Planning: create `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`; use the `Methodology Overlay` section in `plan.template.md` for SCRUM/KANBAN/LEAN overlays (no standalone sprint or kanban templates)
6. Implementation tasks: create `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`; capture TDD evidence
7. Guides: create or update `docs/05.operations/guides/` after behavior stabilizes
8. Operations policy: create or update `docs/05.operations/policies/` before rollout
9. Runbooks: create or update `docs/05.operations/runbooks/` for executable procedures
10. Incidents and postmortems: use `docs/05.operations/incidents/YYYY/INC-###-<title>/record.md` and `postmortem.md`

## Stage-Gate Handoff

At the end of each stage:

1. Read `docs/00.agent-governance/rules/stage-gate-matrix.md`.
2. Run or simulate the `stage-gate-review` checklist against required inputs, outputs, and completion criteria.
3. Report the result in Korean: stage number, `PASS` / `PARTIAL` / `FAIL`, checklist summary, blockers, and proposed next stage.
4. Update `docs/00.agent-governance/memory/progress.md` with phase status, blockers, handoff state, and durable run notes.
5. On `PASS`, ask for approval before moving into the next human-gated stage.
6. On `PARTIAL` or `FAIL`, stop and wait for human decision.

## DDD Decision Tree

Use this decision tree at Stage 02 before freezing architecture or entering Stage 04:

1. If the feature changes domain vocabulary, update or link the ubiquitous language reference.
2. If the feature spans multiple business capabilities or ownership boundaries, create a bounded context document.
3. If aggregates, entities, value objects, or invariants drive correctness, create a domain model companion document in the Stage 04 spec package.
4. If integration behavior is expressed as business events, create a domain events companion document.
5. If none of the triggers apply, record the negative decision in the ARD and continue.

## SDD Mandatory Conditions

Stage 04 specs must include structural diagrams when these conditions are true:

- 3 or more components, systems, actors, tools, or services participate in one behavior: include a Mermaid `sequenceDiagram`.
- correctness depends on lifecycle or state transitions: include a Mermaid `stateDiagram-v2`.
- API/data/agent contracts are changed: include the matching companion template under `docs/03.specs/<feature-id>/`.
- if a diagram is intentionally omitted, record the reason and alternate evidence in the spec verification section.

## TDD Gate

Before closing Stage 06 implementation tasks:

- Stage 04 test strategy must map core behavior to Stage 06 task IDs.
- every `impl` task must capture RED, GREEN, and REFACTOR evidence.
- documentation, governance, operations, and pure configuration tasks may use validation evidence instead of TDD evidence.
- every exemption must include reason, owner, alternate evidence, and review status.

## Stage Transition Hard Stops

- Stop before Stage 02 when no approved PRD or explicit PRD creation task exists.
- Stop before Stage 04 when ARD is missing or DDD triggers were not evaluated.
- **Stop before Stage 04 (frontend layer)** when `DESIGN.md` `version` or `name` is still `<string>` — request design system definition before continuing.
- Stop before Stage 05 when the spec lacks required SDD evidence, companion contracts, or verification criteria.
- Stop before Stage 06 when the plan lacks task breakdown, risk controls, or validation commands.
- Stop before Stage 07 when tasks lack evidence, unresolved blockers remain, or TDD exemptions are incomplete.
- Stop before Stage 08/09 when operational policy or runbook needs are identified but not documented.
- Stop before Stage 10 closure when incident impact, timeline, actions, or postmortem requirements are incomplete.

## TDD, SDD, and DDD Execution

- TDD: follow the `TDD Gate`.
- SDD: follow the `SDD Mandatory Conditions`.
- DDD: follow the `DDD Decision Tree`.

## Rules

- Do not start a downstream phase without the required upstream artifact.
- Parallelize only when ownership paths do not overlap.
- Keep active methodology and progress in `docs/00.agent-governance/memory/`.
- Update `docs/00.agent-governance/memory/progress.md` at phase boundaries, handoffs, blockers, and task closure.
- Use `_workspace/` for transient coordination artifacts only.
- Route stage-gate validation through the dedicated review skill before advancing.
- Final authoritative outputs must be written to canonical compact `docs/` paths.
- Never use legacy ad hoc draft buckets as final destinations.
- Never use `_workspace/` as a final destination for authoritative stage deliverables.
- Do not create a new runtime skill for SDLC orchestration unless an ADR changes the active harness inventory.
