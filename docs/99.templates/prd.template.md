---
title: <string>
version: <string>
owner: <string>
layer: product
stage: 01
status: draft
last-updated: YYYY-MM-DD
methodology: HYBRID
---

# Product Requirements Document (PRD)

<!-- Target: docs/01.requirements/YYYY-MM-DD-<slug>.md -->

## Usage Guidance

- **When to use**: At project start or before adding a major feature.
- **Mandatory sections**: Overview, Success Criteria, Acceptance Criteria.
- **Naming rule**: `YYYY-MM-DD-<slug>.md`.
- **Hard Stops**: STOP if AC are not testable. STOP if `DESIGN.md` is uninitialized for frontend features.
- **Generation rule**: For derived-project seeds, keep `status: draft`, replace bracketed prompts with project facts or `TODO:`, and do not copy Project-Template maintenance history as active product scope.
- **Lifecycle reference**: Apply `docs/00.agent-governance/rules/template-document-lifecycle.md` before reusing inherited documents.

## Purpose

The PRD defines the product intent, scope, and success criteria. It acts as the canonical source of truth for "what" we are building and "why".

---

## Overview (KR)

이 문서는 [기능 또는 시스템명]의 제품 요구사항을 정의한다. 사용자 가치, 문제 정의, 성공 기준을 명확히 하여 후속 설계와 구현의 기준으로 사용한다.

## Vision

[State the user or business outcome in one sentence.]

## Problem Statement

[What problem exists now and why it matters. Be specific about the pain point.]

## Personas

| Persona | Role               | Primary Need                   | Pain Point                       |
| :------ | :----------------- | :----------------------------- | :------------------------------- |
| [Name]  | [Role description] | [What they want to accomplish] | [Friction they experience today] |

## Key Use Cases

> Format: As a [Persona], I want to [action] so that [outcome].

- **STORY-01**: As a [Persona], I want to [action] so that [outcome].
- **STORY-02**: As a [Persona], I want to [action] so that [outcome].

## Epics & Story Breakdown (SCRUM / HYBRID)

> Use this section when methodology is SCRUM or HYBRID. Skip for LEAN or KANBAN.

| Epic ID | Epic Name   | Stories            | Priority    |
| :------ | :---------- | :----------------- | :---------- |
| EPIC-01 | [Epic name] | STORY-01, STORY-02 | Must-have   |
| EPIC-02 | [Epic name] | STORY-03           | Should-have |

## Priority Matrix (MoSCoW)

| Priority                      | Items                                            |
| :---------------------------- | :----------------------------------------------- |
| **Must-have**                 | [Features without which the product fails]       |
| **Should-have**               | [Important but not critical for initial release] |
| **Could-have**                | [Nice-to-have if time and resources allow]       |
| **Won't-have (this release)** | [Explicitly deferred]                            |

## Functional Requirements

- **REQ-PRD-FUN-01**: [Requirement — describe behavior, not implementation]
- **REQ-PRD-FUN-02**: [Requirement]

## Non-Functional Requirements

- **Performance**: [e.g., p95 latency < 200ms under 1 000 RPS]
- **Security**: [e.g., auth required, PII handling policy]
- **Scalability**: [e.g., must support 10× current load without redesign]
- **Reliability**: [e.g., 99.9% uptime SLO]
- **Accessibility**: [e.g., WCAG 2.1 AA compliance for all UI]

## Acceptance Criteria

| ID     | Given          | When     | Then               | Story Ref |
| :----- | :------------- | :------- | :----------------- | :-------- |
| AC-001 | [precondition] | [action] | [expected outcome] | STORY-01  |
| AC-002 | [precondition] | [action] | [expected outcome] | STORY-02  |

## Success Criteria & Metrics

| ID             | Metric        | Baseline | Target | Measurement Method |
| :------------- | :------------ | :------- | :----- | :----------------- |
| REQ-PRD-MET-01 | [Metric name] | [Now]    | [Goal] | [How to measure]   |
| REQ-PRD-MET-02 | [Metric name] | [Now]    | [Goal] | [How to measure]   |

## Scope and Non-goals

- **In Scope**: [What this PRD covers]
- **Out of Scope**: [What is explicitly excluded]
- **Non-goals**: [Valid goals that are intentionally deferred]

## Risks, Dependencies, and Assumptions

| Assumption | [What we assume to be true]     | [How to validate]  |
| :--------- | :------------------------------ | :----------------- |
| Risk       | [Risk description]              | [Mitigation]       |
| Dependency | [External system / team / data] | [Owner / timeline] |
| Assumption | [What we assume to be true]     | [How to validate]  |

## SDLC Governance Triggers (TDD / SDD / DDD)

> Identify potential complexity triggers for downstream design stages.

| Type    | Trigger Condition                                        | Status       | Target Doc                                                          |
| :------ | :------------------------------------------------------- | :----------- | :------------------------------------------------------------------ |
| **DDD** | Multiple domain collaboration or complex business logic? | [Yes / No]   | `docs/02.architecture/requirements/`                                |
| **SDD** | Flow involves 3+ components/services?                    | [Yes / No]   | `docs/03.specs/`                                                    |
| **TDD** | Core business logic requiring high reliability?          | [Always Yes] | `docs/03.specs/` (strategy) → `docs/04.execution/tasks/` (evidence) |

## AI Agent Requirements (If Applicable)

> Include when the feature involves AI / LLM agents. Otherwise remove this section.

- **Allowed Actions**: [What the agent may do autonomously]
- **Disallowed Actions**: [Hard boundaries — never cross]
- **Human-in-the-loop Requirement**: [When human approval is required]
- **Evaluation Expectation**: [How agent quality will be measured]
- **Safety / Guardrail Notes**: [Any content or output guardrails required]

## Lean Canvas (If Applicable)

> Fill this section when methodology is LEAN or HYBRID.

### Problem

- **Top 3 Problems**:
  1. [Problem 1]
  2. [Problem 2]
  3. [Problem 3]
- **Existing Alternatives**: [How customers solve this today]

### Customer Segments

- **Target Customers**: [Who has this problem most acutely]
- **Early Adopters**: [Who will be the first to try this]

### Unique Value Proposition

- **Single clear message**: [What makes this different]
- **High-Level Concept**: [X for Y — one sentence elevator pitch]

### Solution

- **Top 3 Features**:
  1. [Feature 1]
  2. [Feature 2]
  3. [Feature 3]

### Channels

- **Path to Customers**: [How you reach them]

### Revenue Streams

- **Revenue Model**: [Subscription / Transactional / Freemium / etc.]

### Cost Structure

- **Customer Acquisition Cost (CAC)**: [Estimated]
- **Infrastructure / Hosting**: [Monthly cost estimate]

### Key Metrics

| Metric     | Definition                 | Target | How to Measure |
| :--------- | :------------------------- | :----- | :------------- |
| Activation | [What counts as activated] | [X%]   | [Tool/query]   |
| Retention  | [What counts as retained]  | [X%]   | [Tool/query]   |

### Unfair Advantage

[What you have that cannot be easily copied]

### MVP Scope

- **Included in MVP**: [Feature 1, Feature 2 — minimum viable version]
- **Excluded from MVP (v2+)**: [Feature N]
- **Riskiest Assumption**: [The single thing most likely to make this fail]
- **MVP Hypothesis**: [We believe that [capability] will result in [outcome] for [persona].]
- **Validation Method**: [How we will test the hypothesis]

## Target-Relative Link Guidance

Keep placeholder paths as code spans until a generated document links to an existing file.

| Target Location                             | Governance Example                                                | Common Upstream/Downstream                                                               |
| ------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `docs/01.requirements/YYYY-MM-DD-<slug>.md` | `[../00.agent-governance/rules/project-initialization-intake.md]` | `[../02.architecture/requirements/####-<slug>.md]`, `[../03.specs/<feature-id>/spec.md]` |

## AI Execution Checklist

### Entry Gate

- [ ] Read `docs/00.agent-governance/memory/methodology.md`; if absent, create it from `docs/99.templates/methodology.template.md` using `HYBRID` and record that assumption here.
- [ ] Scan `docs/01.requirements/` for overlapping PRDs before creating a new one.
- [ ] Confirm this PRD is the upstream anchor for any ARD, Spec, Plan, and Task documents.
- [ ] If methodology is `LEAN` or `HYBRID`, decide whether a companion Lean Canvas is required.
- [ ] **SCRUM / HYBRID**: Populate `## Epics & Story Breakdown` before Stage 04.
- [ ] **Frontend/UI scope check**: If frontend or mobile UI work is included, verify `DESIGN.md` `version` and `name` are defined (not `<string>`). If not, flag for design system definition before Stage 04 Spec.

### Exit Gate

- [ ] All placeholders removed.
- [ ] Acceptance criteria are testable (Given/When/Then or condition/result form).
- [ ] MoSCoW priority table populated.
- [ ] Downstream links in `## Related Documents` filled or explicitly marked absent.
- [ ] `docs/01.requirements/README.md` updated (Documents table).
- [ ] Run `stage-gate-review` before moving to Stage 02 or Stage 04.

### Hard Stop Conditions

- **STOP** before Stage 02 if no approved PRD exists or PRD scope is undefined.
- **STOP** before Stage 04 (frontend) if `DESIGN.md` `version` or `name` is still `<string>`.
- **STOP** if Acceptance Criteria are not structured in a way that can be mapped to test cases (Given/When/Then or Input/Output).

### Downstream Trigger

When the PRD stage gate passes, continue via `spec-driven-sdlc`:

- Stage 02 ARD — when architecture boundaries, quality attributes, or DDD context are needed.
- Stage 03 ADR — when a significant technology or architecture decision is made.
- Stage 04 Spec — when implementation detail is ready to design.

### Evidence Rule

- [ ] Acceptance criteria, success metrics, and methodology assumptions MUST cite specific stakeholder input, discovery findings, or research data.

## Related Documents

- **ARD**: `[../02.architecture/requirements/####-system-or-domain.md]`
- **Spec**: `[../03.specs/<feature-id>/spec.md]`
- **Plan**: `[../04.execution/plans/YYYY-MM-DD-<feature>.md]`
- **ADR**: `[../02.architecture/decisions/####-<short-title>.md]`
