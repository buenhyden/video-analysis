---
title: Data Governance & Integrity Index
version: 1.1.0
owner: Data Protection Officer
layer: governance
stage: 00
status: active
last-updated: 2026-05-09
---

# Data Governance & Integrity Index

> [!NOTE]
> This directory was migrated to `docs/00.agent-governance/data-governance/` to comply with the 8-folder compact governance policy.

## Overview

This directory owns reusable data-governance policy for privacy, PII tracking, encryption standards, and schema integrity. It keeps source-template guidance separate from derived-project databases and migrations.

## Audience

This README is for data owners, security reviewers, backend implementers, and agents that need to determine whether data-policy material belongs in Stage 00 or a downstream implementation record.

## Scope

### In Scope

- Data privacy and PII handling guardrails.
- Encryption and key-management standards for derived projects.
- Schema integrity rules that downstream projects can adopt.
- README inventory for data-governance documents.

### Out of Scope

- Actual database migrations and rollback scripts.
- Runtime secrets, credentials, or environment-specific KMS configuration.
- Application-specific retention policy text that belongs in a derived project.

## Structure

| Area | Purpose |
| :--- | :--- |
| PII Tracking | Identifies sensitive data categories and required handling. |
| Migration Logs | Defines traceability expectations for derived-project schema changes. |
| Encryption & Access | Links reusable encryption and key-management standards. |

## How to Work in This Area

1. Confirm the change is reusable governance rather than application-specific data policy.
2. Create or update governed documents with Stage 00 scope and no secrets.
3. Keep the `Documents` table synchronized with actual files in this folder.
4. Run `python3 scripts/validation/validate-doc-readiness.py` and `bash scripts/validation/validate-cross-links.sh`.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [encryption-standards.md](./encryption-standards.md) | md | Data Encryption & Key Management Standards | active | - |

## Lifecycle Rules

1. **PII Isolation**: All PII must be identified and documented. No raw PII should be stored without encryption.
2. **Schema Integrity**: Every database migration must have a corresponding migration log in the derived project.
3. **Retention**: Data retention policies must be reviewed on the cadence required by the target project.

## Categories

### PII Tracking

- Inventory sensitive data fields and their approved storage locations.

### Migration Logs

- Preserve traceability for database schema changes across environments.

### Encryption & Access

- Apply data-at-rest and data-in-transit encryption standards before storing sensitive data.

## AI Execution Checklist

- [ ] **Target**: Verified data safety and schema integrity for `<topic>`.
- [ ] **Entry Gate**: Read Stage 04 specs and data-governance policies before proposing data changes.
- [ ] **Procedure**: Follow `docs/99.templates/extended/schema.template.graphql` only when GraphQL is in scope.
- [ ] **Exit Gate**: Update this index and verify PII impact.
- [ ] **Hard Stop**: STOP if a database migration is proposed without a rollback path.

## Related Documents

- [Stage 00 Governance](../README.md)
- [Compliance Hub](../compliance/README.md)
- [Encryption Standards](./encryption-standards.md)
- [Documentation Protocol](../rules/documentation-protocol.md)

---

## Docs 3 Global Rules Reference

> Active on every task. HALT conditions enforced by agents.
> Applies when creating or changing governed documentation in this folder.
> Full definitions: `docs/00.agent-governance/rules/documentation-protocol.md §7`

| Rule                       | Summary                                                                              | HALT If                                          |
| :------------------------- | :----------------------------------------------------------------------------------- | :----------------------------------------------- |
| **R1 — Content Creation**  | Read template before creating any stage doc. Fill all sections. Set `status: draft`. | Template missing or `[placeholder]` text remains |
| **R2 — Auto-Indexing**     | Update this README after every change to this folder.                                | README not updated after folder change           |
| **R3 — Cross-Referencing** | Every stage doc must have `## Related Documents` with relative upstream links.       | Required upstream links absent                   |
