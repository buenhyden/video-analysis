---
title: <string>
version: <string>
owner: <string>
layer: architecture
stage: 02
status: draft
last-updated: YYYY-MM-DD
---

# Bounded Context

<!-- Target: docs/02.architecture/requirements/####-<bounded-context-name>.md -->

## Usage Guidance

- **When to use**: When a system involves multiple domain boundaries that require separate definition.
- **Mandatory sections**: Overview, Purpose & Responsibility, Ubiquitous Language, Context Boundaries.
- **Naming rule**: `####-<slug>.md`.
- **Hard Stops**: STOP if no DDD trigger was confirmed in the parent ARD. STOP if context overlaps without resolution.

## Purpose

The Bounded Context document defines a linguistic and functional boundary within a domain. It ensures that terms and models remain consistent and unambiguous within that boundary.

---

## Overview (KR)

이 문서는 [컨텍스트명] Bounded Context의 경계, 도메인 언어, 통합 계약을 정의한다.
DDD 전략 설계의 산출물로, 이후 ARD와 Spec의 도메인 기준이 된다.

## Context Summary

- **Context Name**: [BoundedContextName]
- **Domain**: [Core Domain / Supporting Domain / Generic Subdomain]
- **Team / Owner**: [Team or owner]
- **Status**: `draft | active | completed`

## Purpose & Responsibility

[What this context is responsible for. One paragraph.]

## Ubiquitous Language

> All terms below are authoritative within this context only.
> Terms with the same name in other contexts may have different meanings.

| Term | Definition | Notes |
| :--- | :--- | :--- |
| [Term 1] | [Definition within this context] | |
| [Term 2] | [Definition within this context] | |

## Aggregates & Key Domain Concepts

| Aggregate / Entity | Role | Invariants | Root Entity |
| :--- | :--- | :--- | :--- |
| [Aggregate 1] | [What it enforces] | [Business rule] | Yes / No |
| [Entity 1] | [Role] | | No |

## Domain Events

| Event | Trigger | Payload (key fields) | Consumers |
| :--- | :--- | :--- | :--- |
| [EventName] | [What triggers it] | [key fields] | [Other context or service] |

## Context Boundaries

### Owns

- [What data, processes, and decisions this context exclusively owns]

### Does Not Own

- [What is explicitly outside this context]

## Context Map — Integration Patterns

| Upstream Context | Integration Pattern | Notes |
| :--- | :--- | :--- |
| [Context A] | `Shared Kernel / Customer-Supplier / Conformist / ACL / OHS / Published Language` | [Notes] |

| Downstream Context | Integration Pattern | Notes |
| :--- | :--- | :--- |
| [Context B] | [Pattern] | [Notes] |

### Anti-Corruption Layer (if applicable)

- **Needed**: Yes / No
- **Reason**: [Why translation is needed]
- **Key translations**: [e.g., ContextA.Order → this.PurchaseRequest]

## Domain Events — Publishing Contract

```yaml
event: '[EventName]'
source: '[AggregateName]'
trigger: '[business trigger]'
schema:
  eventId: uuid
  occurredAt: ISO8601
  field1: '[type]'
consumerContract: '[what guarantees downstream consumers can rely on]'
```

## Quality Attributes (Context-level)

- **Consistency model**: [strong / eventual]
- **Transaction boundary**: [single aggregate / saga / process manager]
- **Latency sensitivity**: [real-time / batch / async]

## AI Execution Checklist

- [ ] **Entry Gate**: The parent ARD triggered separate DDD documentation, and a matching ubiquitous language document exists or will be created.
- [ ] **Exit Gate**: Owns/does-not-own boundaries and upstream/downstream integration patterns are defined.

### Hard Stop Conditions

- **STOP** if no DDD trigger was confirmed in the parent ARD. STOP if this bounded context overlaps an existing context in `docs/02.architecture/requirements/` and no ADR resolves it.
- [ ] **Downstream Trigger**: Create feature-local `domain-model.md` and `domain-events.md` under `docs/03.specs/<feature-id>/` during Stage 04.
- [ ] **Evidence Rule**: Cite domain expert review, source docs, or accepted architecture constraints for boundaries and integration patterns.

## Related Documents

- **Parent ARD**: `[./####-<system-or-domain>.md]`
- **PRD**: `[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`
- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Data Model**: `[../../03.specs/<feature-id>/data-model.md]`
- **Ubiquitous Language**: `[./####-ubiquitous-language.md]`
- **Related ADR**: `[../decisions/####-<short-title>.md]`
