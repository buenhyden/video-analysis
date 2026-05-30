---
title: <string>
version: <string>
owner: <string>
layer: architecture
stage: 03
status: draft
last-updated: YYYY-MM-DD
---

# Tactical Model

<!-- Target: docs/03.specs/<feature-id>/tactical-model.md -->

## Usage Guidance

- **When to use**: To define both the logical domain model (DDD) and the physical data model (SQL/NoSQL) in a single document for medium-complexity features.
- **Mandatory sections**: Overview, Domain Model, Data Model, Migration & Compatibility.
- **Naming rule**: `tactical-model.md`.
- **Hard Stops**: STOP if aggregate roots and invariants are undefined. STOP if no rollback strategy exists for schema changes.

## Purpose

The Tactical Model bridges the gap between high-level domain design and physical implementation. It ensures that the software implementation (data storage, transactions, migrations) remains faithful to the domain's business rules.

## 1. Domain Model (Logical)

- **Bounded Context**: [BoundedContextName]
- **Bounded Context Doc**: `[../../02.architecture/requirements/####-<bounded-context-name>.md]`

### Aggregates & Invariants

| Aggregate Root | Invariants | Commands | Events Raised |
| :--- | :--- | :--- | :--- |
| [AggregateName] | [Business rule that must always hold] | [CreateX, UpdateX] | [XCreated, XUpdated] |

### Entities & Value Objects

- **Entities**: [Entity1, Entity2] (identify by ID)
- **Value Objects**: [VO1, VO2] (identify by attributes, immutable)

---

## 2. Data Model (Physical)

### Storage Strategy

- **Primary Store**: [e.g., PostgreSQL, DynamoDB]
- **Caching**: [e.g., Redis for high-frequency lookups]

### Schema / Structures

```sql
-- Implementation-ready schema
CREATE TABLE [table_name] (
  id UUID PRIMARY KEY,
  -- [fields]
);
```

### Validation & Integrity

- [Rule 1: Required fields]
- [Rule 2: Referential integrity]

---

## 3. Migration & Compatibility

- **Backward Compatibility**: [How to handle old data]
- **Migration Path**: [Step-by-step rollout]
- **Rollback Strategy**: [How to revert schema changes]

---

## AI Execution Checklist

### Entry Gate

- [ ] Parent Spec identifies domain complexity or data storage changes.
- [ ] Bounded context in `02.architecture/requirements/` is identified.

### Exit Gate

- [ ] Aggregates and invariants are defined.
- [ ] Physical schema and migration strategy are implementation-ready.
- [ ] No single transaction crosses aggregate roots (unless justified by ADR).

### Hard Stop Conditions

- **STOP** if aggregate roots and invariants are undefined.
- **STOP** if no parent Spec identifies a data structure or storage change.
- **STOP** if ownership, privacy, or rollback requirements are unknown.

### Downstream Trigger

- [ ] Update domain events, tests, and execution tasks.

### Evidence Rule

- [ ] Link migration rehearsal, validation query, or domain expert review evidence.

## Related Documents

- **Spec**: `[./spec.md]`
- **Bounded Context**: `[../../02.architecture/requirements/####-<bounded-context-name>.md]`
- **Domain Events**: `[./domain-events.md]`
- **Runbook**: `[../../05.operations/runbooks/####-<topic>.md]`
