---
layer: agentic
title: 'Agent Operating Procedure (AOP)'
---

# Agent Operating Procedure (AOP)

**Canonical protocols for AI agent behavior, ensuring predictable, high-quality, and traceable autonomous work.**

## 1. Core Methodology: RPEVU

Every task, regardless of scale, must follow the **RPEVU** cycle:

1. **Research (R)**:
   - Thoroughly investigate the context, upstream documents, and existing codebase.
   - Identify all relevant "Hard Stop" conditions and methodology triggers (TDD/SDD/DDD).
   - **Stop** if information is missing or ambiguous.
2. **Plan (P)**:
   - Draft an implementation plan (or a mental model for trivial tasks).
   - Ensure the plan is traceably linked to Stage 01 (PRD) and Stage 04 (Spec) anchors.
   - Define specific verification criteria and success metrics.
3. **Execute (E)**:
   - Implement changes in bite-sized, verifiable increments.
   - Follow the TDD cycle (RED-GREEN-REFACTOR) for all implementation tasks.
   - Apply SDD (Structure-Driven Design): create Mermaid diagrams for any component, service, or module with 3 or more dependencies or interfaces before writing implementation code.
   - Maintain strictly English governance but Korean user-facing communication.
4. **Verify (V)**:
   - Run tests, validation scripts, and manual checks.
   - Capture evidence (logs, screenshots, command outputs) as required by the stage.
   - Confirm no regression in reference integrity or design tokens.
5. **Update (U)**:
   - Finalize documentation (Sub-stage READMEs, LLM-WIKI, etc.).
   - Commit changes with clear, standard-compliant messages.
   - Provide a concise "Postflight" summary of the work performed.

## 2. Reasoning Discipline

- **Thought-Driven Development**: Always perform deep "Thinking" before proposing any code change. Surface trade-offs and assumptions explicitly.
- **Minimalism**: Implement only what is requested. No speculative abstractions or unasked features.
- **Surgical Precision**: Touch only what is necessary. Clean up orphans created by your changes, but do not "improve" adjacent unrelated code.

## 3. AI Agent-First Engineering Contract

AI Agent-first Engineering means the workspace is designed so agents can plan, implement, verify, and hand off work from repository-local contracts without inventing process or hidden context.
Harness inventory and runtime readiness are owned by `docs/00.agent-governance/rules/harness-library.md`.

| Principle            | Required Behavior                                                                                                                 | Canonical Stage / Surface                                     |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| Intake-first         | Derived projects collect product/software intent, stack, data/security constraints, and operations baseline before stage authoring. | `project-initialization-intake.md`                            |
| Spec-first           | Implementation starts from approved or explicitly waived PRD, ARD/ADR, Spec, Plan, and Task anchors.                              | `docs/01.requirements/` through `docs/04.execution/tasks/`    |
| Persona-scoped       | Every non-trivial task declares persona, layer, stage, allowed writes, and validation path.                                       | `persona.md`, `scopes/*.md`, `.claude/agents/*.md`            |
| Context-minimized    | Load bootstrap, preflight, persona, scope, then only task-relevant rules and stage docs.                                          | `bootstrap.md`, `preflight-checklist.md`                      |
| Tool-contract driven | Tool and script use must follow documented command surfaces and avoid side effects outside the declared task.                     | `scripts/ws.sh help`, `scripts/README.md`                     |
| Evidence-driven      | Every closed task records runnable validation or TDD/eval evidence; empty assertions do not satisfy a gate.                       | `docs/04.execution/tasks/`, `stage-gate-matrix.md`            |
| Guardrailed          | Secrets, protected branch pushes, missing or mismatched templates, uninitialized `DESIGN.md`, broken links, and scope conflicts are hard stops. | `quality-standards.md`, `git-workflow.md`, `design-system.md` |
| Human-escalated      | Ambiguous ownership, missing anchors, or conflicting rules stop execution and escalate instead of guessing.                       | `preflight-checklist.md`, `postflight-checklist.md`           |

Agent-specific specs must complete the `Agent Role & IO Contract`, `Tools & Tool Contract`, `Prompt / Policy Contract`, `Memory & Context Strategy`, `Guardrails`, and `Evaluation` sections in the Stage 04 spec when the change affects agent behavior, prompts, tools, memory, or runtime policy.

Event-driven guardrails are part of the tool contract. Claude Code reads `.claude/settings.json`
directly, while Codex and other local agents use `bash scripts/ws.sh hook <event> [matcher]`
to run the same configured command hooks without introducing another policy surface.

## 4. Communication & Handoff

- **Persona Alignment**: Always announce your active persona, scope, and stage before non-trivial execution.
- **Progress Reporting**: Update the user/orchestrator at meaningful task boundaries.
- **Escalation**: Stop and resolve conflicts immediately if governance rules or stage ownership are ambiguous.

## 5. Safety & Integrity

- **Secrets**: ZERO TOLERANCE for secrets in the repository. Proactively scan for and remove accidental exposures.
- **Absolute Paths**: Never use machine-specific absolute paths. Use relative paths for all cross-document and code references.
- **Traceability**: Every output must map to a canonical compact docs input under `docs/01.requirements` through `docs/05.operations`.

## 6. Hard Stop Enforcement

Every agent is a **Gatekeeper**. You MUST enforce the "Hard Stop" conditions defined in:

- `docs/00.agent-governance/rules/stage-gate-matrix.md`
- `docs/99.templates/*.template.md`
- stage-specific template conformance enforced by `scripts/validation/validate-doc-readiness.py`
- `DESIGN.md` (for frontend work)

Do not proceed with any phase if the previous phase's exit criteria are not met.

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
