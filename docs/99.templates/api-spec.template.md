---
title: <string>
version: <string>
owner: <string>
layer: backend
stage: 03
status: draft
last-updated: YYYY-MM-DD
---

# API Specification

<!-- Target: docs/03.specs/<feature-id>/api-spec.md -->

## Usage Guidance

- **When to use**: When a feature exposes an external or internal API contract.
- **Mandatory sections**: Overview, Endpoint Catalog, Request/Response Schemas, Error Model.
- **Naming rule**: `api-spec.md` (within the feature directory).
- **Hard Stops**: STOP if no parent Spec exists. STOP if machine-readable contract format (OpenAPI/proto) is undefined for public APIs.
- **Derived-project seed rule**: Create only when the parent spec declares an API boundary; do not infer REST, GraphQL, or gRPC from the base template.

## Purpose

The API Specification defines the technical contract for communication between systems. It ensures both provider and consumer align on schemas, authentication, and error handling.

---

## Overview (KR)

이 문서는 [기능명]이 외부에 노출하는 API 계약을 정의한다. 엔드포인트, 인증, 요청/응답 스키마, 에러, 버저닝, 비기능 요구를 상세히 기술한다.

## Parent Spec

- **Spec**: `[./spec.md]`

## Scope & Non-goals

- **Covers**:
- **Does Not Cover**:
- **Parent Design Context**: full design rationale remains in `spec.md`

## API Style

- **Type**: `REST | GraphQL | gRPC`
- **Audience**:
- **Versioning Strategy**:

## Authentication & Authorization

- **Auth Mechanism**:
- **Scopes / Roles**:
- **Rate Limit / Abuse Control**:

## Endpoint / Operation Catalog

| Operation ID | Method / Type | Path / Name | Purpose | Caller |
| --- | --- | --- | --- | --- |
| API-001 | GET | `/example` | [Purpose] | [Client] |

## Request / Response Schemas

### Request

```json
{
  "example": "value"
}
```

### Response

```json
{
  "id": "123",
  "status": "ok"
}
```

## Error Model

| Code | Meaning | Retryable | Notes |
| --- | --- | --- | --- |
| 400 | Bad Request | No | Validation error |

## Data Contract Compatibility

- **Backward Compatibility Rule**:
- **Breaking Change Rule**:
- **Deprecation Policy**:

## Non-Functional Requirements

- **Latency Budget**:
- **Availability Expectation**:
- **Observability**:
- **Audit / Traceability**:

## Machine-readable Contract Files

- `./contracts/openapi.yaml`
- `./contracts/service.proto`
- `./contracts/schema.graphql`

## Verification

- Contract lint
- Mock / integration test
- Consumer compatibility check

## Target-Relative Link Guidance

- This file lives at `docs/03.specs/<feature-id>/api-spec.md`; sibling links use `./`.
- Keep parent spec and tests as `[./spec.md]` and `[./tests.md]`.
- Link execution evidence as `[../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

### Entry Gate

- [ ] Parent Spec identifies an API or external contract change.
- [ ] API style, caller, auth boundary, and versioning strategy are known.

### Exit Gate

- [ ] Endpoints/operations, schemas, errors, auth, compatibility, and tests are complete.
- [ ] Machine-readable contracts are linked or explicitly not applicable.

### Hard Stop Conditions

- **STOP** if no parent Spec exists or if API style, caller, and auth boundary are undefined.
- **STOP** if machine-readable contract format (OpenAPI/proto/GraphQL) has not been agreed on for externally consumed APIs.

### Downstream Trigger

- [ ] Update tests, task validation, guides, and runbooks for contract changes.

### Evidence Rule

- [ ] Link contract lint, mock/integration test, or consumer compatibility evidence.

## Related Documents

- **Spec**: `[./spec.md]`
- **Test Strategy**: `[./tests.md]`
- **Plan**: `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`
