---
name: ops-sop
description: Drafts standard operating procedures, runbooks, first-response protocols, and operations manuals for the active workspace. Use for docs/05.operations/policies/ and docs/05.operations/runbooks/ authoring. Triggers on 'write an SOP', 'create a runbook', 'operations manual', 'standard operating procedure', 'first-response protocol', 'incident response procedure', 'process documentation', 'work instructions', 'checklist design', 'training materials', 'operations guide', 'procedure document', or any request to document repeatable work or incident triage steps.
---

# Ops SOP

Create operational procedures for stable service ownership.

## Document Type Selection

Select the right output type before drafting:

| Request Pattern                      | Output Type             | Target Path               |
| ------------------------------------ | ----------------------- | ------------------------- |
| Repeatable work process, onboarding  | SOP                     | `docs/05.operations/policies/`     |
| Incident response, on-call runbook   | Runbook                 | `docs/05.operations/runbooks/`       |
| First alert, triage steps            | First-Response Protocol | `docs/05.operations/runbooks/`       |
| Full process reference with training | Operations Manual       | `docs/05.operations/policies/`     |

## Outputs

- SOP documents in `docs/05.operations/policies/`
- Operational guides in `docs/05.operations/policies/`
- Runbooks in `docs/05.operations/runbooks/`
- First-response escalation flows for incidents

## Execution Modes

| Request Pattern                                | Mode           | Scope                                               |
| ---------------------------------------------- | -------------- | --------------------------------------------------- |
| "Write a complete SOP"                         | Full Pipeline  | Process analysis → procedure → checklist → training |
| "Write the procedure steps only"               | Procedure Mode | Steps + decision points only                        |
| "Design a checklist" (procedure exists)        | Checklist Mode | Execution checklist only                            |
| "Create training materials" (procedure exists) | Training Mode  | Guides + exercises + assessments                    |
| "Create an operations manual"                  | Manual Mode    | Analysis → flowcharts → step-by-step → FAQ          |
| "Write a runbook"                              | Runbook Mode   | Trigger → steps → rollback → escalation             |
| "First-response protocol"                      | Triage Mode    | Alert → triage → escalation tree                    |

## Workflow

### Phase 1: Preparation

1. Read the related architecture and spec documents first.
2. Identify whether the request is best served by an SOP, runbook, first-response protocol, or operations manual.
3. Extract from user input:
   - **Target process**: What work or system to document
   - **Scope**: Team, service, or environment in scope
   - **Audience**: New operators / experienced staff / on-call engineers
   - **Constraints** (optional): Compliance requirements (ISO, SOC 2), existing templates
   - **Existing materials** (optional): Current procedure docs, wikis, code
4. Create `_workspace/` at the project root; save organized inputs as `_workspace/00_input.md`.
5. If existing documents are provided, update rather than rewrite from scratch.

### Phase 2: Process Analysis

Before writing any procedure, map the process:

**SIPOC mapping:**

| Element   | Questions to Answer                          |
| --------- | -------------------------------------------- |
| Suppliers | Who provides inputs to this process?         |
| Inputs    | What triggers or feeds into this process?    |
| Process   | What are the core steps and decision points? |
| Outputs   | What artifacts or states result?             |
| Customers | Who consumes or acts on the outputs?         |

**RACI matrix per step:**

| Step | Responsible | Accountable | Consulted | Informed |
| ---- | ----------- | ----------- | --------- | -------- |

Identify every decision branch in the process (condition → action A / action B).

### Phase 3: Document Production

#### SOP Document Standard

```markdown
# [Process Name] — Standard Operating Procedure

## Purpose

[One sentence: what this procedure achieves]

## Scope

[Team, environment, trigger conditions]

## Roles (RACI)

[Table mapping steps to R/A/C/I roles]

## Prerequisites

- [ ] [Access or state required before starting]

## Procedure

### Step 1: [Action Name]

**Action**: [Precise, imperative instruction]
**Decision branch** (if any):

- If [condition A] → proceed to Step 2
- If [condition B] → proceed to Step 5
  **Expected result**: [Observable state after step completion]
  **Rollback**: [How to undo if the step produces an error]

## Verification Checklist

- [ ] [Post-procedure verification item]

## Escalation

- Escalate to [role/team] if [condition].
- Escalation contact: [on-call rotation / Slack channel]

## References

- Related spec: [link]
- Related runbook: [link]

> **Version**: v1.0 | **Created**: YYYY-MM-DD | **Review Cycle**: quarterly
```

#### Runbook Standard

```markdown
# [Runbook Name]

## Trigger

Alert: [alert name or threshold that activates this runbook]
Severity: P[1-3]

## Triage (< 5 minutes)

1. [First check]
2. [Second check]

## Diagnosis

| Symptom | Likely Cause | Check Command |
| ------- | ------------ | ------------- |

## Remediation Steps

1. [Step with expected result]
2. [Step with rollback option]

## Rollback Procedure

1. [How to revert if remediation makes things worse]

## Escalation

- Escalate to [team] after [N] minutes without improvement.
- Call tree: [on-call contact chain]

## Post-Incident

- Open postmortem if P1/P2 — hand off to `sre-ops`.
- Update this runbook with any new failure modes discovered.
```

#### First-Response Protocol Standard

```markdown
## First-Response Protocol: [Service/Alert Name]

### Detection (T+0)

- Alert fires: [alert name]
- On-call acknowledges within: 5 minutes

### Initial Triage (T+5)

- [ ] Check service health dashboard
- [ ] Identify blast radius (users affected, services down)
- [ ] Declare severity: P1 / P2 / P3

### Communication (T+10 for P1/P2)

- Post to [incident Slack channel]: "Investigating [service] degradation. Severity: P[N]."
- Page secondary on-call if P1.

### Handoff

- Transfer to runbook: `docs/05.operations/runbooks/[service]-[symptom].md`
```

### Phase 4: Checklist Design

Apply these principles to every checklist:

| Principle           | Application                                       |
| ------------------- | ------------------------------------------------- |
| One action per item | Never combine two steps in one checkbox           |
| Observable result   | Each item can be verified as done or not done     |
| Ordering            | Pre-execution → execution → post-execution groups |
| Failure annotation  | Mark items where failure requires escalation      |
| Version tied        | Include checklist version and last-reviewed date  |

Checklist types:

- **Pre-execution**: conditions that must be true before starting
- **Execution**: steps to perform in order
- **Verification**: confirm the process succeeded
- **Rollback**: steps to undo if something went wrong

### Phase 5: Operations Manual Assembly

When producing a full operations manual, include:

| Section                 | Content                                             |
| ----------------------- | --------------------------------------------------- |
| Process Inventory       | All processes covered; SIPOC per process            |
| Flowcharts              | Mermaid `graph LR` per process; Level 0 and Level 1 |
| Step-by-step Procedures | Each process as a numbered procedure                |
| FAQ / Troubleshooting   | Top 10 exception scenarios with resolution paths    |
| Training Materials      | Exercises, quizzes, hands-on scenarios              |

Cross-validation before closing the manual:

- [ ] Every flowchart process has a corresponding procedure.
- [ ] Every procedure exception is covered in the FAQ.
- [ ] All glossary terms are used consistently throughout.
- [ ] Quiz content matches the step-by-step manual.

### Phase 6: Hand-off

- Hand off SLO ownership and postmortem work to `sre-ops` when needed.
- Cross-link the produced document from the spec or ADR that motivated it.
- Record document version and review cadence in the metadata block.

## Boundaries

- Do not hardcode secrets or credentials.
- Do not define production SLO targets inside this skill — delegate to `sre-ops`.
- Do not make infrastructure changes directly.
- Keep procedures concrete, reversible, and auditable.

## Error Handling

| Scenario                                | Strategy                                                                    |
| --------------------------------------- | --------------------------------------------------------------------------- |
| No existing process documentation       | Interview the process owner; reconstruct from code and artifacts            |
| Process too complex for one SOP         | Split into sub-SOPs; create a master index document                         |
| Compliance requirements unknown         | Mark sections "[compliance review needed]"; escalate to `security-engineer` |
| Procedure steps untestable in isolation | Mark as "[verification needed]"; request owner to validate                  |
| Contradictions between sources          | Prioritize code-observable behavior; record contradictions explicitly       |
