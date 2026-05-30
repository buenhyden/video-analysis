---
layer: meta
title: 'Stage-Gate Matrix (00-10)'
---

# Stage-Gate Matrix (00-10)

This matrix is the unified checklist source for document purpose, timing, ownership, dependencies, templates, and completion criteria.

For newly derived projects, project initialization intake is the Stage 00 entry
gate. Do not create Stage 01-10 or Stage 90 project documents until
product/software intent, stack, security/data constraints, and operations
baseline are captured.

Generated project documents start with `status: draft`. Bootstrap creates only
the Stage 01 PRD-shaped intake seed; ARD, ADR, spec, plan, task, operations, and
reference documents are generated later from their templates at the relevant
stage gate.

| Stage | Path | Purpose | When to Write | Primary Persona | Input Documents | Output Documents | Template | AI Hard Stop | Evidence Type | Completion Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 00 | `docs/00.agent-governance/` | Agent operating rules and routing | Before any execution | `meta`, `docs` | Repository policy, tool/runtime behavior | Rules, scopes, providers, checklists | N/A (governance markdown) | Stop if root routers or bootstrap rules are missing | Governance validation, link validation | Governance is consistent, link-valid, and actionable |
| 01 | `docs/01.requirements/` | Product intent (`what/why`) | Feature inception | `product` | Stakeholder goals, business constraints | PRD documents | `prd.template.md` (includes Lean Canvas overlay for Lean/Hybrid) | Stop if scope, acceptance criteria (AC), or non-goals are absent; OR if AC cannot be mapped to tests | PRD acceptance criteria, methodology record | Scope, acceptance criteria, and non-goals are explicit; AC is TDD-mappable |
| 02 | `docs/02.architecture/requirements/` | Architecture reference (`system blueprint`) | After PRD approval, before detailed spec | `architecture` | PRD, existing architecture constraints | ARD documents; optional Bounded Context and Ubiquitous Language docs | `ard.template.md` (includes Bounded Context / Ubiquitous Language overlay for simple domains) · `expanded/bounded-context.template.md` · `expanded/ubiquitous-language.template.md` | Stop if ARD is missing, DDD triggers are not evaluated, or mandatory C4 Context diagram is missing | Architecture boundary evidence, DDD decision table, C4 diagram | Architecture boundaries and quality attributes are defined; DDD contexts mapped; C4 diagram exists |
| 03 | `docs/02.architecture/decisions/` | Architectural decisions and rationale | When a significant decision is made | `architecture` | PRD, ARD, alternatives | ADR documents | `adr.template.md` | Stop significant irreversible decisions until ADR records alternatives | Decision record, alternatives, consequences | Decision, alternatives, and consequences are recorded |
| 04 | `docs/03.specs/` | Technical implementation specification | Before coding | `backend`, `frontend`, `architecture`, `security` | PRD, ARD, ADR | Spec package (spec/api/data/tests/contracts) | `spec.template.md` (primary, includes Domain Model/Events overlay for simple tactical design) · `api-spec.template.md` · `expanded/tactical-model.template.md` · `expanded/domain-model.template.md` · `expanded/domain-events.template.md` · `tests.template.md` · `openapi.template.yaml` · `extended/schema.template.graphql` · `extended/service.template.proto` | Stop if SDD diagrams (mandatory for 3+ components), contracts, TDD mapping, or verification criteria are missing | Mermaid sequence/state diagrams, API/data/contracts, test strategy | Implementation-ready design, verifiable criteria, sequence diagrams, and TDD mapping exist |
| 05 | `docs/04.execution/plans/` | Execution plan and verification flow | After spec freeze | `product`, `qa`, implementation lead persona | PRD, ARD/ADR, Spec | Plan documents | `plan.template.md` (includes Sprint/Kanban methodology overlay) | Stop if task breakdown, risk controls, or specific runnable validation commands are absent | Work breakdown, validation plan, rollback criteria | Tasks, risks, validation gates, and rollback path are clear |
| 06 | `docs/04.execution/tasks/` | Work execution tracking and evidence | During implementation/testing | `backend`, `frontend`, `qa`, `docs` | Approved plan and spec | Task records with evidence | `task.template.md` | Stop if implementation tasks lack non-empty TDD RED-GREEN-REFACTOR evidence or approved exemption | RED/GREEN/REFACTOR logs, validation commands, eval results, exemption records | Task status complete; TDD evidence (non-empty log) captured per impl task; no open blockers |
| 07 | `docs/05.operations/guides/` | Human-readable usage and how-to guides | After behavior stabilizes | `docs` | Spec, implemented behavior, operations policy | Guides/how-to documents | `guide.template.md` | Stop if behavior is unstable or audience/prerequisites are undefined | Reproducible steps, screenshots/logs if relevant | Steps are reproducible by intended audience |
| 08 | `docs/05.operations/policies/` | Operational policy and controls | Before production rollout | `ops`, `infra`, `security` | Spec, run requirements, compliance requirements | Operations policy docs | `operation.template.md` · `slo.template.md` | Stop if SLO, controls, ownership, or promotion criteria are absent | Policy checks, SLO/control definitions, risk acceptance | SLO, controls, and promotion criteria are defined |
| 09 | `docs/05.operations/runbooks/` | Executable operational procedures | Before or with production handoff | `ops`, `infra` | Operations policy, known risks | Runbooks | `runbook.template.md` | Stop if on-call cannot execute diagnosis, mitigation, rollback, and escalation | Dry-run evidence, command output, rollback rehearsal notes | On-call can execute recovery steps without ambiguity |
| 10 | `docs/05.operations/incidents/` | Incident fact tracking and postmortem | During incidents; postmortem after stabilization | `ops`, `security`, `architecture`, `product` | Alerts, traces, timelines | `INC-###/record.md`; optional `INC-###/postmortem.md` | `incident.template.md` · `postmortem.template.md` | Stop closure if impact, timeline, actions, severity review, or postmortem need is incomplete | Incident evidence, timeline, corrective actions, postmortem review | Impact, timeline, actions, and evidence captured; `postmortem.md` written and reviewed if severity ≥ P1 |

## Skills Reference by Stage

Active skills to invoke at each stage. Skills live in `.claude/skills/`.

| Stage | Primary Skill(s) | Review / Gate Skill | Notes |
| :--- | :--- | :--- | :--- |
| 00 | `governance-audit`, `doc-governance` | — | Run after any governance change |
| 01 | `pm-pipeline` | `stage-gate-review` | Gate review required before Stage 02 |
| 02 | `microservice-designer` | `stage-gate-review` | Gate review required before Stage 04 |
| 03 | — | `stage-gate-review` | Triggered by any significant architectural choice |
| 04 | `spec-driven-sdlc`, `security-audit` | `stage-gate-review` | Use `fullstack-webapp` only when the derived project declares a web/app stack |
| 05 | `pm-pipeline` | `stage-gate-review` | Gate review required before Stage 06 |
| 06 | `test-automation` | `code-review` | Add stack-specific skills only when declared |
| 07 | `doc-pipeline`, `template-patch` | — | After behavior stabilizes |
| 08 | `ops-sop` | — | Before production rollout |
| 09 | `ops-sop` | — | Before or with production handoff |
| 10 | — | — | Incident tracking + postmortem; no skill gate |

For end-to-end orchestration across all stages, use the `spec-driven-sdlc` skill (`.claude/skills/spec-driven-sdlc/`).

## Notes

- `docs/90.references/` and `docs/99.templates/` support all stages but are outside the 00-10 gate flow.
- Template names are relative to `docs/99.templates/`.
- Non-README documents in each stage path must preserve the required sections from the listed template contract. Agents must stop if a document cannot satisfy the matching template contract.
- If a stage is skipped, record explicit justification in the next stage artifact.
- Stage-gate review (`stage-gate-review` skill) returns `PASS`, `PARTIAL`, or `FAIL`. A `FAIL` blocks progression.
- ADRs (Stage 03) are cross-stage artifacts. They may be written at Stage 01, 02, 03, or 04. The `02.architecture/decisions/` folder number indicates storage location, not execution timing.
- DESIGN.md is the workspace design-system source for frontend/mobile/app work; Stage 04 UI specs must link it and stop if `version` or `name` is uninitialized.
- Machine-readable API/schema/proto templates inherit their gates from the parent Stage 04 companion Markdown template.

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
