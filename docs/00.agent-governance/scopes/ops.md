---
layer: ops
title: 'Operations & SRE Scope'
---

# Operations & SRE Scope

**Monitoring, alerting, incident response, and environment reliability standards.**

## 1. Context & Objective

- **Goal**: Minimize MTTR (Mean Time To Recovery) and maximize system availability.
- **Stack**: Use only the observability stack declared by the derived-project intake and documented in `docs/05.operations/policies/`.
- **Criteria**: Mandatory alignment with `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Observability**:
  - **Metrics**: Define metric names, owners, and collection method for all declared services. Prometheus exporters are an example only when the intake or operations policy chooses that stack.
  - **Logging**: JSON-structured logs with correlated Trace IDs.
  - **Tracing**: Define trace boundaries for distributed flows. Tempo is an example only when the intake or operations policy chooses that stack.
- **Reliability**: Define health checks and restart or recovery policy for every declared production runtime. Container restart policies apply only when the derived project declares containers.

## 3. Implementation Flow

1. **Monitor**: Define dashboards and telemetry ownership in `docs/05.operations/policies/`.
2. **Alert**: Define SLI/SLO and escalation criteria in operations policy docs.
3. **Recover**: Create and maintain runbooks in `docs/05.operations/runbooks/`.

## 4. Operational Procedures

- **Incident Response**: Follow the `docs/05.operations/incidents/` protocol for live tracking.
- **Postmortems**: Mandatory retrospective in `docs/05.operations/incidents/YYYY/INC-###-<title>/postmortem.md` for any SEV1/SEV2 incident.

## 5. Maintenance & Safety

- **Backups**: Define backup cadence and restore validation in operations documents.
- **Drills**: Periodically perform disaster recovery drills (Chaos Engineering).

## File Ownership

- **Allowed Write**: `docs/05.operations/policies/**` · `docs/05.operations/runbooks/**` · `docs/05.operations/incidents/**`
- **Forbidden Write**: implementation paths · runtime infrastructure paths · `docs/99.templates/**`
- **Pre-condition**: Incident record exists in `docs/05.operations/incidents/` before postmortem is authored.
- **Post-condition**: All prevention actions have owners and due dates; runbook is executable by on-call.

## Subagent Definition

- **Trigger**: Incident response, postmortem authoring, SLO definition, or runbook update.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/sre-ops.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
