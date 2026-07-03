---
title: Operations Skeleton
version: 1.0.0
owner: Operations Lead
layer: operations
stage: 05
status: active
last-updated: 2026-05-21
---

# Operations Skeleton

> 새 프로젝트의 guides, policies, runbooks, incidents를 작성하기 위한 release skeleton.

## Overview

This hub groups stable user-facing guides and operational knowledge in the
compact docs model. It is folder 05 in the compact `docs/` tree, and it
contains the Stage 07-10 operational workflow outputs used by the stage-gate
matrix. These folders do not imply that the base template ships a production
application stack; derived projects create operational artifacts only when
stable behavior, policy, runbook, or incident evidence exists.

`dev` may retain video-analysis onboarding guides, policy/SLO history, or
operations evidence for traceability. Those records are not default operational
artifacts for derived projects; `main` keeps this area as skeleton guidance.

| Workflow Stage | Compact Path | Purpose |
| --- | --- | --- |
| Stage 07 | `docs/05.operations/guides/` | Stable human, developer, and operator guides |
| Stage 08 | `docs/05.operations/policies/` | Operational policies, controls, and SLOs |
| Stage 09 | `docs/05.operations/runbooks/` | Executable operational procedures |
| Stage 10 | `docs/05.operations/incidents/` | Incident records and postmortems |

## Audience

- Operations leads
- SRE, platform, and security engineers
- Project maintainers
- AI agents preparing guides, policies, runbooks, or incident records

## Scope

### In Scope

- Project-specific guides, policies, runbooks, incidents
- Operational controls, observability, release, escalation guidance
- Derived project operations folder initialization guidance

### Out of Scope

- Product requirements and architecture decisions
- Implementation task logs
- Template repository operations history
- Local-only agent handoff material

## Structure

```text
05.operations/
├── guides/      # Human-readable project operation guides
├── incidents/   # Incident and postmortem records
├── policies/    # Operational policies and controls
├── runbooks/    # Executable procedures
└── README.md    # This file
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- [guide.template.md](../99.templates/guide.template.md) - Stable guides.
- [operation.template.md](../99.templates/operation.template.md) - Operational policy.
- [slo.template.md](../99.templates/slo.template.md) - Service objective policy.
- [runbook.template.md](../99.templates/runbook.template.md) - Runbooks.
- [incident.template.md](../99.templates/incident.template.md) - Incident records.
- [postmortem.template.md](../99.templates/postmortem.template.md) - Postmortems.

## Naming Rules

- Guides: `<slug>.md` for evergreen guides, `YYYY-MM-DD-<slug>.md` for dated or historical guides.
- Policies: `<slug>.md`.
- Runbooks: `####-<topic>.md`.
- Incidents: `YYYY/INC-###-<title>/{record.md,postmortem.md}`.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

- Operations documents start as `draft`.
- Operational policies and runbooks become `active` only after owner and validation criteria are clear.
- Incidents become `completed` only after timeline, impact, action items, and follow-up ownership are recorded.
- On `main`, this folder remains a skeleton until a derived project creates project-specific operations docs.

## Cross-Reference Rules

- Stage 07 guides link to the spec or `docs/04.execution/tasks/` evidence that finalized behavior.
- Stage 08 policies link to relevant architecture, SLOs, monitoring evidence, and runbooks.
- Stage 09 runbooks link to the policy or incident that requires the procedure.
- Stage 10 incidents link to runbooks, postmortems, and follow-up execution tasks.

## Usage Examples

```bash
cp docs/99.templates/runbook.template.md docs/05.operations/runbooks/deploy-service.md
cp docs/99.templates/slo.template.md docs/05.operations/policies/YYYY-MM-DD-service-slo.md
```

## How to Work in This Area

1. Confirm the operations baseline from project initialization intake.
2. Choose the correct operations subfolder.
3. Create the document from the approved template.
4. Update child README `Documents` tables when files change.
5. Run validation and link execution evidence when operational behavior changes.

## AI Authoring Guidance

- Do not create SLO, runbook, or release policy assumptions before operations intake is complete.
- Do not preserve video-analysis operations history on `main`.
- Keep operational procedures executable and owner-aware.
- In a derived project, rewrite skeleton guidance to match the actual environment and release model.

## AI Execution Checklist

- [ ] Operations intake fields are known.
- [ ] The correct operations template is used.
- [ ] Owners, validation, rollback, and escalation are explicit where applicable.
- [ ] Related execution evidence is linked.
- [ ] The `Documents` table reflects actual child folders and files.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [guides](./guides/) | package | Guide seed package plus dev-only onboarding contract history | project-seed | 2026-05-21 |
| [incidents](./incidents/) | package | Incident seed package; no base-template incidents | project-seed | 2026-05-21 |
| [policies](./policies/) | package | Policy seed package plus dev-only SLO history | project-seed | 2026-05-21 |
| [runbooks](./runbooks/) | package | Runbook seed package; no base-template runbooks | project-seed | 2026-05-21 |

## Related Documents

- [03.specs](../03.specs/README.md) - Specifications
- [04.execution](../04.execution/README.md) - Execution plans and task evidence
- [Documentation Protocol](../00.agent-governance/rules/documentation-protocol.md) - Documentation governance

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
