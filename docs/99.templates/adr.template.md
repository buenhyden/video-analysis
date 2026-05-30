---
title: <string>
version: <string>
owner: <string>
layer: architecture
stage: 02
status: draft
last-updated: YYYY-MM-DD
---

# Architecture Decision Record (ADR)

<!-- Target: docs/02.architecture/decisions/####-<slug>.md -->

## Usage Guidance

- **When to use**: To record a significant architecture or technology choice.
- **Mandatory sections**: Context, Decision, Alternatives, Consequences.
- **Naming rule**: `####-<slug>.md` (sequenced).
- **Hard Stops**: STOP if alternatives are not evaluated. STOP if it's just an implementation spec.
- **Generation rule**: For derived-project seeds, keep `status: draft`, replace bracketed prompts with project facts or `TODO:`, and record only real decision triggers.
- **Lifecycle reference**: Apply `docs/00.agent-governance/rules/template-document-lifecycle.md` before reusing inherited decisions.

## Purpose

The ADR captures the rationale for a specific architectural decision, including the context and the trade-offs considered.

---

## Overview (KR)

이 문서는 [결정 주제]에 대한 아키텍처 결정 기록이다. 특정 선택의 배경, 대안, 결과를 추적하기 위해 사용한다.

## Status

`Proposed` | `Accepted` | `Superseded`

- **Decision Date**: YYYY-MM-DD
- **Superseded by**: _(link to superseding ADR, if applicable)_

## Context

[Why a formal decision is needed now.]

## Decision

- [Decision point 1]
- [Decision point 2]

## Explicit Non-goals

- [What this ADR does not cover]

## Consequences

- **Positive**:
- **Trade-offs**:

## Alternatives

### [Alternative 1]

- Good:
- Bad:

### [Alternative 2]

- Good:
- Bad:

## Agent-related Example Decisions (If Applicable)

- Model selection
- Tool gating
- Guardrail strategy
- Planner / executor pattern
- Fallback model policy

## Target-Relative Link Guidance

Keep placeholder paths as code spans until a generated document links to an existing file.

| Target Location                                 | Governance Example                                       | Common Upstream/Downstream                                                  |
| ----------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------- |
| `docs/02.architecture/decisions/####-<slug>.md` | `[../../00.agent-governance/rules/stage-gate-matrix.md]` | `[../requirements/####-<slug>.md]`, `[../../03.specs/<feature-id>/spec.md]` |

## AI Execution Checklist

- **Entry Gate**: PRD/ARD/Spec context and decision trigger are linked.
- **Exit Gate**: decision, alternatives, consequences, and status are complete.
- **Hard Stop Conditions**: STOP if no concrete architecture decision trigger exists — exploratory notes are not ADRs. STOP if an ADR for the same scope already exists and this would duplicate it without superseding the earlier record.
- **Downstream Trigger**: update Spec/Plan/Runbook when the decision changes implementation or operations.
- **Evidence Rule**: MUST cite specific trade-off data, experiment results, or architecture review logs.

## Related Documents

- **PRD**: `[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`
- **ARD**: `[../requirements/####-<system-or-domain>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Plan**: `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`
- **Related ADR**: `[./####-<related-decision>.md]`
