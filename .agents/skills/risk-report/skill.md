---
name: risk-report
description: Builds risk registers for governance, architecture, and release decisions. Use when a change needs explicit risk scoring, mitigation plans, and monitoring actions. Triggers on requests like "assess the risk of this change", "risk register", "risk matrix", "risk assessment", "mitigation plan", or "risk monitoring".
---

# Risk Report

Assess and document change risk for the active workspace using a systematic five-phase pipeline.

## Risk Categories

- Technical — architecture, performance, security, integration
- Operational — process gaps, tooling, deployment, personnel
- Governance — missing ADRs, policy violations, inventory drift, compliance
- External — vendor changes, regulatory requirements, third-party dependencies

## Execution Modes

| Request Pattern                     | Mode           | Phases       |
| ----------------------------------- | -------------- | ------------ |
| "Full risk assessment"              | Full pipeline  | All 5 phases |
| "Identify risks only"               | Identification | Phase 1 only |
| "Score this risk list"              | Assessment     | Phases 2–3   |
| "Response strategy for these risks" | Response       | Phases 3–4   |
| "Risk status report"                | Reporting      | Phase 5 only |

## Workflow

### Phase 1: Risk Identification

1. Review the proposed change set and its affected documents or systems.
2. Apply the Risk Breakdown Structure (RBS) across categories: Technical / Operational / Governance / External.
3. For each risk: assign ID, write a one-line summary, record evidence source.
4. Save to `_workspace/01_risk_identification.md`.

### Phase 2: Probability × Impact Assessment

1. Score each risk on a 5-point scale for probability and impact.
2. Plot on a 5×5 matrix; classify as Critical (20–25) / High (12–19) / Medium (6–11) / Low (1–5).
3. Calculate EMV (probability% × impact $) for quantifiable risks.
4. Save to `_workspace/02_risk_assessment.md`.

### Phase 3: Response Strategy

1. For Critical/High: select Avoid or Mitigate; document SMART action plan.
2. For Medium: Mitigate or Monitor with documented contingency trigger.
3. For Low: Accept with explicit awareness note.
4. Calculate residual risk score after response.
5. Save to `_workspace/03_response_strategy.md`.

### Phase 4: Monitoring Plan

1. Define Key Risk Indicators (KRIs) for Critical and High risks.
2. Set review cadence: Critical = weekly, High = bi-weekly, Medium/Low = monthly.
3. Specify escalation path and trigger conditions for each KRI.
4. Save the authoritative monitoring plan to `docs/04.execution/plans/YYYY-MM-DD-<change>-risk-monitoring.md`.

### Phase 5: Risk Status Report

1. Produce executive summary: total risks by priority, top 3 risks, overall risk level.
2. Include action item tracking table with owner and due date.
3. Save to `_workspace/05_risk_report.md`.

## Output

Produce a register with:

- risk ID, category, summary
- likelihood (1–5), impact (1–5), score
- EMV where quantifiable
- treatment strategy with SMART action items
- owner, due date, KRI, review cadence

## Rules

- Structural governance changes require explicit downstream impact analysis.
- Missing ADR coverage for architecture-level change is a critical governance risk.
- Every Critical/High risk must have an assigned owner before the report is closed.
- Residual risk must be re-scored after response actions are defined.
- Final monitoring or mitigation plans must live under canonical `docs/04.execution/plans/`.
- `_workspace/` may be used only for transient identification, assessment, and reporting artifacts.

## Error Handling

| Scenario                         | Strategy                                                                  |
| -------------------------------- | ------------------------------------------------------------------------- |
| Insufficient project information | Use general project risk templates; mark items as "[verification needed]" |
| No quantitative impact data      | Use qualitative assessment; note "re-assess after data available"         |
| Risks between categories overlap | Assign to primary category; note cross-category dependency                |
| Agent/phase failure              | Proceed without that output; mark gap in final report                     |
