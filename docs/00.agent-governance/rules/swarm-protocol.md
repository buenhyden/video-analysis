# Swarm Protocol: Multi-Agent Collaboration

This protocol defines how multiple AI agents (Architect, Developer, QA, PM) collaborate sequentially to solve complex tasks within the `video-analysis` ecosystem.

## 1. Core Philosophy
- **Sequential Baton-Passing**: One agent finishes their "phase" and hands off a formal artifact to the next agent.
- **State Sovereignty**: Each agent has full control over their output, but must consume the previous agent's artifact as their primary source of truth.
- **Immutable Context**: Every handoff must be documented in `_workspace/swarm/<task_id>/`.

## 2. Roles & Responsibilities

| Role | Responsibility | Primary Output |
| :--- | :--- | :--- |
| **PM** | Requirement analysis & PRD refinement | `docs/01.requirements/` |
| **Architect** | Technical design & Stage 05 planning | `docs/02.architecture/requirements/` & `docs/04.execution/plans/` |
| **Developer** | Feature implementation & Unit testing | Source Code & `docs/04.execution/tasks/` |
| **QA** | E2E testing, security audit, and validation | `docs/04.execution/tasks/` evidence and, when user-facing, `docs/05.operations/guides/` |

## 3. Handoff Procedure

### Gate 1: PM -> Architect
- **Trigger**: PRD Status changed to `Ready for Design`.
- **Artifact**: `01_pm_output.md` containing refined requirements.

### Gate 2: Architect -> Developer
- **Trigger**: Stage 05 plan approved by User.
- **Artifact**: `02_architect_plan.md` or a linked `docs/04.execution/plans/<date>-<slug>.md` containing file-level change instructions.

### Gate 3: Developer -> QA
- **Trigger**: Feature implementation complete and linted.
- **Artifact**: `03_coder_result.md` containing TDD evidence.

## 4. Automation CLI (`ws swarm`)

- Canonical syntax: `ws swarm <task_id> <start|status|handoff|suggest> [next_role]`.
- `ws swarm <task_id> start`: Initializes a swarm directory.
- `ws swarm <task_id> status`: Checks the current active agent in the swarm.
- `ws swarm <task_id> handoff <next_role>`: Archives the current work and prepares the next agent's context.
- `ws swarm <task_id> suggest`: Suggests the next swarm role from transient intelligence output.
- Command-first swarm syntax is not supported.

## 5. Failure Recovery
If an agent fails their validation gate (e.g., QA fails), the baton is passed **back** to the previous role (e.g., back to Developer) with a `05_fail_report.md`.
## Role definition

- Applies to multi-agent collaboration and baton-passing for complex SDLC tasks.

## Procedure

- Follow the role responsibilities, handoff gates, automation CLI usage, and failure recovery procedure defined above.
- Store swarm handoff state only in transient `_workspace/swarm/<task_id>/` coordination paths.

## Constraints

- Do not treat `_workspace/swarm/**` as authoritative final documentation.
- Do not advance a handoff if the previous role has not produced the required artifact and validation evidence.

## File references

- `docs/01.requirements/`
- `docs/02.architecture/requirements/`
- `docs/04.execution/plans/`
- `docs/04.execution/tasks/`
