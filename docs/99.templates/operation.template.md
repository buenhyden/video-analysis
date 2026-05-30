---
title: <string>
version: <string>
owner: <string>
layer: infra
stage: 05
status: draft
last-updated: YYYY-MM-DD
---

# Operations Policy

<!-- Target: docs/05.operations/policies/<slug>.md -->

## Usage Guidance

- **When to use**: To define policy, controls, and approval rules.
- **Mandatory sections**: Overview, Policy Scope, Controls, SLO/SLA.
- **Naming rule**: `<slug>.md`.
- **Hard Stops**: STOP if SLO targets are undefined for availability/latency policies. STOP if no upstream Spec/ARD exists.
- **Generation rule**: For derived-project seeds, keep `status: draft`, replace bracketed prompts with project facts or `TODO:`, and do not copy Project-Template maintenance policies as active operations policy.
- **Lifecycle reference**: Apply `docs/00.agent-governance/rules/template-document-lifecycle.md` before reusing inherited documents.

## Purpose

The Operations Policy defines the standards and constraints for operating a system. it establishes the "rules of engagement" for production environments.

---

## Overview (KR)

이 문서는 [정책명] 운영 정책을 정의한다. 적용 범위, 통제 기준, 예외, 검증 방법을 규정한다.

## Policy Scope

[What this policy governs.]

## Applies To

- **Systems**:
- **Agents**:
- **Environments**:

## Controls

- **Required**:
- **Allowed**:
- **Disallowed**:

## Exceptions

- [Exception rule and approval path]

## Verification

- [How compliance is checked]

## SLO / SLA

| Dimension | Target | Error Budget |
| --- | --- | --- |
| Availability | [e.g., 99.9%] | [e.g., 43.8 min/month] |
| Latency p95 | [e.g., < 500ms] | — |
| Error Rate | [e.g., < 0.1%] | — |

## Review Cadence

- [Monthly / Quarterly / Per release]

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**:
- **Eval / Guardrail Threshold**:
- **Log / Trace Retention**:
- **Safety Incident Thresholds**:

## Target-Relative Link Guidance

- This file lives under `docs/05.operations/policies/`; links to runbooks and incidents use `../`.
- Link upstream architecture/spec evidence as `[../../02.architecture/requirements/####-<system-or-domain>.md]` or `[../../03.specs/<feature-id>/spec.md]`.
- Link executable procedures as `[../runbooks/####-<topic>.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

- **Entry Gate**: Spec/Plan identifies production, compliance, security, or SLO impact.
- **Exit Gate**: ownership, controls, SLOs, rollout, and rollback criteria are complete.
- **Hard Stop Conditions**: STOP if no system Spec or ARD exists to justify the policy scope. STOP if SLO targets are undefined when the policy governs availability, latency, or error rate. STOP if policy controls reference undocumented system behavior.
- **Downstream Trigger**: create or update runbooks for executable procedures.
- **Evidence Rule**: MUST link specific policy review artifacts, control check logs, or risk acceptance sign-offs.

## Related Documents

- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Runbook**: `[../runbooks/####-<topic>.md]`
- **Postmortem**: `[../incidents/YYYY/INC-###-<incident-title>/postmortem.md]`
