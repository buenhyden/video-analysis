---
title: <string>
version: <string>
owner: <string>
layer: architecture
stage: 03
status: draft
last-updated: YYYY-MM-DD
---

# Domain Model

<!-- Target: docs/03.specs/<feature-id>/domain-model.md -->

## Usage Guidance

- **When to use**: To define the tactical DDD design (Aggregates, Entities, Value Objects) for a complex feature.
- **Mandatory sections**: Overview, Aggregates, Entities, Value Objects, Repository Contracts.
- **Naming rule**: `domain-model.md`.
- **Hard Stops**: STOP if no parent Bounded Context doc exists. STOP if invariants are undefined.

## Purpose

The Domain Model provides a technical blueprint of the domain logic. It ensures that business invariants are protected within transaction boundaries (Aggregates) and that the language matches the Ubiquitous Language.

---

## Overview (KR)

이 문서는 [기능명]의 도메인 모델을 정의한다. Aggregate, Entity, Value Object, Repository 계약을 명세한다.

## Bounded Context Reference

- **Context**: [BoundedContextName]
- **Bounded Context Doc**: `[../../02.architecture/requirements/####-<bounded-context-name>.md]`

## Aggregates

| Aggregate Root | Invariants | Commands | Events Raised |
| :--- | :--- | :--- | :--- |
| [AggregateName] | [Business rule that must always hold] | [CreateX, UpdateX] | [XCreated, XUpdated] |

### [AggregateName] Detail

```typescript
interface [AggregateName] {
  id: [AggregateId];         // identity
  // [fields]
}
```

**Invariants:**

- [Rule 1: expressed as a constraint]
- [Rule 2]

## Entities

| Entity | Identity By | Lifecycle | Parent Aggregate |
| :--- | :--- | :--- | :--- |
| [EntityName] | `[entityId]` | [created → active → archived] | [AggregateName] |

## Value Objects

| Value Object | Equality By | Validation Rule | Immutable |
| :--- | :--- | :--- | :--- |
| [ValueName] | All attributes | [e.g., non-empty, format regex] | Yes |

## Domain Services (If Applicable)

| Service | Responsibility | Input | Output |
| :--- | :--- | :--- | :--- |
| [ServiceName] | [Cross-aggregate operation] | [Params] | [Result] |

## Repository Contracts

| Repository | Methods | Storage Hint |
| :--- | :--- | :--- |
| [AggregateName]Repository | `findById`, `save`, `delete` | [e.g., PostgreSQL table `aggregate_name`] |

## Aggregate Boundary Rules

Use these rules before finalizing aggregate boundaries.

### Keep in One Aggregate

- Objects that must preserve invariants inside one transaction.
- Objects whose business rules are always checked together.
- Child entities that cannot be valid without the aggregate root.

### Split into Separate Aggregates

- Objects that can change independently.
- Objects where eventual consistency is acceptable.
- Objects owned by different bounded contexts or teams.

### Entity vs Value Object Decision Tree

```text
Does the concept need stable identity?
├── YES: Does it own lifecycle and invariants?
│   ├── YES: Aggregate Root or Entity
│   └── NO: Entity reference inside an aggregate
└── NO: Is equality based on attributes?
    ├── YES: Value Object
    └── NO: Revisit with domain expert
```

## AI Execution Checklist

- [ ] **Entry Gate**: Link the parent bounded context, identify aggregate roots, and list invariants.
- [ ] **Exit Gate**: Confirm no single transaction crosses aggregate roots (unless justified by ADR). Repository contracts align with the Spec and Data Model.

### Hard Stop Conditions

- **STOP** if no parent bounded context document exists in `docs/02.architecture/requirements/`. STOP if aggregate roots and invariants are undefined.
- [ ] **Downstream Trigger**: Update domain events, data model, tests, and execution tasks when aggregate boundaries change.
- [ ] **Evidence Rule**: Cite bounded-context decisions, domain expert review, or test/eval evidence for invariants and boundaries.

## Related Documents

- **Spec**: `[./spec.md]`
- **Bounded Context**: `[../../02.architecture/requirements/####-<bounded-context-name>.md]`
- **Data Model**: `[./data-model.md]`
- **Domain Events**: `[./domain-events.md]`
