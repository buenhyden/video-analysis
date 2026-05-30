---
title: <string>
version: <string>
owner: <string>
layer: operations
stage: 05
status: draft
last-updated: YYYY-MM-DD
---

# SLO Specification: <Service Name>

<!-- Target: docs/05.operations/policies/SLO.md -->

## Usage Guidance

- **When to use**: Before production rollout or when defining measurable operational quality targets for a service.
- **Mandatory sections**: Service Context, Service Level Objectives, Error Budget Policy, Monitoring Implementation.
- **Naming rule**: `SLO.md` or `<service>-slo.md` under `docs/05.operations/policies/`.
- **Hard Stops**: STOP if the service, SLI measurement source, or error-budget consequence is undefined.
- **Derived-project seed rule**: Create only after the project declares a real service and SLO need; bootstrap must not create a default SLO.

## Purpose

The SLO Specification defines measurable service quality targets, how they are monitored, and what operational action follows when the error budget is exhausted.

---

## 1. Service Context

- **Service Name**: <Name of the service>
- **Criticality**: [High / Medium / Low]
- **User Journey**: <Description of what users are trying to achieve>

## 2. Service Level Objectives (SLOs)

| Indicator (SLI) | Target | Window | Measurement Method |
| :--- | :--- | :--- | :--- |
| **Availability** | 99.9% | 30 days | (Success Requests / Total Requests) |
| **Latency (p95)** | < 200ms | 30 days | Time from request to first byte |
| **Error Rate** | < 0.1% | 30 days | HTTP 5xx count |

## 3. Error Budget Policy

- **Total Budget**: <Remaining percentage for the period>
- **Consequence of Exhaustion**:
  1. Freeze on feature deployments.
  2. Immediate priority to reliability tasks.
  3. Post-mortem required if exhaustion happens > 2 times.

## 4. Monitoring Implementation

- **Metrics Source**: [Prometheus / Datadog / CloudWatch]
- **Dashboard Link**: [Link to Grafana Dashboard]
- **Alerting Channel**: [#ops-alerts Slack]

## Evidence / Verification

- [Monitoring query, dashboard snapshot, alert test, or review artifact proving each SLI can be measured.]

## Target-Relative Link Guidance

- This file lives under `docs/05.operations/policies/`; links to runbooks and incidents use `../`.
- Link upstream architecture/spec evidence as `[../../02.architecture/requirements/####-<system-or-domain>.md]` or `[../../03.specs/<feature-id>/spec.md]`.
- Link operational procedures as `[../runbooks/####-<topic>.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## Related Documents

- [AGENTS.md](../../../AGENTS.md)
- [Operations Policies README](./README.md)

---

## AI Execution Checklist

### Entry Gate

- [ ] Confirm upstream PRD/ARD exists.
- [ ] Read performance specs from Stage 04.

### Exit Gate

- [ ] Update `docs/05.operations/policies/README.md` index.
- [ ] Verify monitoring dashboard JSON exists in `monitoring/`.

### Hard Stop Conditions

- **STOP** if no health endpoint exists in the target service.
- **STOP** if Error Budget consequences are not explicitly defined.

### Downstream Trigger

- [ ] Update operations post-launch evidence rules with these SLOs.
- [ ] Update runbooks and incident severity rules when SLO thresholds change.

### Evidence Rule

- [ ] TDD Readiness for operations: SLOs must be verifiable via `monitoring/` configurations.
