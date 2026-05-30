---
layer: agentic
title: 'SDLC Standard Operating Procedure (SOP)'
---

# SDLC Standard Operating Procedure (SOP)

**Step-by-step procedural guide for AI agents to execute Stage-Gate SDLC phases in the workspace.**

## Overview

AI agents must execute each stage by following the specific procedures below. No stage can be bypassed without explicit justification and owner approval.

---

## Stage 01: Product Definition (PRD)

1. **Input**: Identify stakeholder needs, business goals, or feature requests.
2. **Procedure**:
   - Copy `docs/99.templates/prd.template.md` to `docs/01.requirements/YYYY-MM-DD-<feature>.md`.
   - Apply **Lean/Hybrid Overlay** if the domain is ambiguous or low-complexity.
   - Define **Acceptable Criteria (AC)** in Gherkin (Given/When/Then) format.
3. **Gate Check**:
   - **Hard Stop**: Stop if AC is non-TDD-mappable or if "Non-Goals" are missing.
4. **Output**: Approved PRD with `status: approved`.

## Stage 02: Architecture Reference (ARD)

1. **Input**: Approved Stage 01 PRD.
2. **Procedure**:
   - Copy `docs/99.templates/ard.template.md` to `docs/02.architecture/requirements/####-<system>.md`.
   - **DDD Strategic Decision**: Evaluate the `DDD Trigger Condition`.
   - If triggers fire: Create expanded documents for Bounded Context and Ubiquitous Language.
   - Create **C4 Context & Container** diagrams using Mermaid.
3. **Gate Check**:
   - **Hard Stop**: Stop if DDD triggers were not evaluated or C4 diagrams are missing.
4. **Output**: ARD defining system boundaries and quality attributes.

## Stage 03: Architecture Decision Records (ADR)

1. **Input**: Architectural uncertainty or a need for a significant trade-off.
2. **Procedure**:
   - Copy `docs/99.templates/adr.template.md` to `docs/02.architecture/decisions/####-<decision>.md`.
   - Document **Context**, **Alternatives**, **Rationale**, and **Consequences**.
3. **Gate Check**:
   - **Hard Stop**: Stop if "Alternative Rationale" is missing.
4. **Output**: Immutable decision record.

## Stage 04: Technical Specification (Specs)

1. **Input**: Approved PRD, ARD, and relevant ADRs.
2. **Procedure**:
   - Create directory `docs/03.specs/<feature-id>/`.
   - Create `spec.md` from `spec.template.md`.
   - **SDD Mandatory Rule**: Include a Mermaid `sequenceDiagram` for flows with 3+ components.
   - **TDD Preparation**: Map every implementation behavior to a test case in the **TDD Readiness** table.
   - **Design SSOT**: If UI/Frontend is in scope, link `DESIGN.md` and verify initialization.
3. **Gate Check**:
   - **Hard Stop**: Stop if sequence diagrams are missing for 3+ components OR if TDD mapping is absent.
   - **Hard Stop (Frontend)**: Stop if `DESIGN.md` version/name is still `<string>`.
4. **Output**: Complete spec package (spec, api, data, tests).

## Stage 05: Implementation Planning (Plans)

1. **Input**: Approved Stage 04 Spec package.
2. **Procedure**:
   - Create `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` from `plan.template.md`.
   - Apply **Scrum/Kanban Overlay** based on `docs/00.agent-governance/memory/methodology.md`.
   - Break down work into granular, verifiable tasks (WBS).
   - Define **Runnable Validation Commands** for every milestone.
3. **Gate Check**:
   - **Hard Stop**: Stop if validation commands are missing or non-runnable.
4. **Output**: Task-level execution roadmap.

## Stage 06: Work Execution (Tasks)

1. **Input**: Approved Stage 05 Plan.
2. **Procedure**:
   - Create `docs/04.execution/tasks/YYYY-MM-DD-<feature>.md` from `task.template.md`.
   - **TDD Cycle**: Execute RED -> GREEN -> REFACTOR.
   - **Evidence Rule**: Capture non-empty test execution logs/IDs for every `impl` task.
3. **Gate Check**:
   - **Hard Stop**: Stop if TDD evidence is empty or if tests fail without an approved exemption.
4. **Output**: Verified implementation with complete audit logs.

## Stage 07-10: Post-Implementation

1. **Stage 07 (Guides)**: Create user/developer guides once behavior stabilizes.
2. **Stage 08 (Ops)**: Define SLOs, controls, and promotion criteria before rollout.
3. **Stage 09 (Runbooks)**: Document executable procedures for diagnosis and recovery.
4. **Stage 10 (Incidents)**: Record facts and postmortems for any failure.
   - **Hard Stop**: Stop incident closure if root cause lacks evidence or actions lack owners.

---

## Universal Evidence Rule

Every stage transition must be accompanied by **Verifiable Evidence**:

- PRD: Approved AC
- ARD: C4 Diagrams
- Spec: TDD Readiness Table + SDD Diagrams
- Plan: Runnable Validation Commands
- Task: RED-GREEN-REFACTOR logs

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
