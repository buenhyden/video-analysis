---
name: governance-audit
description: Audits workspace governance for drift, broken references, scope mismatches, and settings duplication. Use after governance edits and before deleting legacy harness sources. Also triggers on "internal audit", "audit checklist", "audit findings", "compliance audit", "audit report", or "corrective action plan".
---

# Governance Audit

Audit the active governance runtime for consistency and drift, and generate structured audit reports for internal governance reviews.

## Audit Modes

| Mode             | Trigger                        | Scope                                                            |
| ---------------- | ------------------------------ | ---------------------------------------------------------------- |
| Governance Drift | After governance edits         | `.Codex/`, `AGENTS.md`, `docs/00.agent-governance/`             |
| Pre-cleanup      | Before deleting legacy sources | Full reference integrity check                                   |
| Internal Audit   | Requested audit report         | Scope design → checklist → findings → recommendations → tracking |
| Follow-up        | Prior audit results exist      | Scope (reduced) + findings + tracking                            |

## Workflow: Governance Drift Audit

### Audit Areas

1. **Agent-to-scope alignment** in `.Codex/agents/` — every agent imports its scope file unless intentionally cross-layer.
2. **Thin-root compliance** for `AGENTS.md`, `AGENTS.md`, and provider overlays — no policy duplication.
3. **Skill layout compliance** in `.Codex/skills/` — directory layout with `skill.md` per skill.
4. **Settings separation** — team policy in `.Codex/settings.json`; personal overrides in `.Codex/settings.local.json`.
5. **English-only policy** in `docs/00.agent-governance/`.
6. **Cross-reference integrity** for governance and architecture anchor documents.
7. **Harness inventory alignment** — `AGENTS.md` and `harness-library.md` describe the same active inventory.
8. **Model hierarchy correctness** — Opus for supervisors; Sonnet for specialists.

### Checks

- Every governed agent imports its scope file, unless it is intentionally cross-layer.
- Active skills use directory layout with `skill.md`.
- No legacy source references remain in the migrated governance surface.
- Governance docs describe the active workspace inventory only.
- Personal local settings do not carry stale migration commands.

## Workflow: Internal Audit Report Pipeline

### Phase 1: Scope Design

1. Extract from user input: audit target, audit type (regular/special/follow-up), applicable criteria.
2. Define audit scope, risk assessment, and audit schedule.
3. Save to `_workspace/01_audit_scope.md`.

### Phase 2: Checklist Creation

1. Build control items from applicable framework (COSO, ISO 27001, or governance-specific criteria).
2. For each control: test procedure, evidence required, pass/fail criteria.
3. Save to `_workspace/02_audit_checklist.md`.

### Phase 3: Findings Analysis

Apply the 4C framework to each finding:

| Component   | Content                          |
| ----------- | -------------------------------- |
| Condition   | What was observed                |
| Criteria    | What should be (standard/policy) |
| Cause       | Why the gap exists               |
| Consequence | Impact of the gap                |

Save to `_workspace/03_audit_findings.md`.

### Phase 4: Recommendations

1. For each finding: corrective action, implementation plan, priority, deadline, owner.
2. Use SMART criteria for all corrective actions.
3. Build priority matrix: impact × ease of implementation.
4. Save to `_workspace/04_recommendations.md`.

### Phase 5: Tracking Ledger

1. Map every finding to its recommendation with implementation deadline and owner.
2. Include escalation criteria and closure conditions.
3. Save to `_workspace/05_tracking_ledger.md`.

### Phase 6: Final Report

Generate `_workspace/06_audit_report.md` as transient run state. If the audit changes governance policy or stage behavior, promote the authoritative outcome to the relevant `docs/00.agent-governance/`, `docs/02.architecture/decisions/`, or `docs/04.execution/tasks/` artifact.

```
# Audit Report: [Target]

## Executive Summary (1 page)
- Audit scope and methodology
- Overall assessment: 🟢 Conforming / 🟡 Improvement Needed / 🔴 Urgent Action Required
- Total findings: Critical X / High Y / Medium Z / Low W

## Findings Summary
| ID | Finding | Severity | Root Cause | Recommendation | Owner | Deadline |
|----|---------|----------|-----------|---------------|-------|---------|

## Findings Detail
[4C analysis per finding]

## Implementation Tracking Plan
[Tracking ledger summary]
```

**Cross-validation before closing:**

- [ ] Every finding has a corresponding recommendation.
- [ ] Every recommendation has an implementation deadline and owner.
- [ ] The tracking ledger includes all findings.
- [ ] Risk ratings are consistently applied across all artifacts.

## Output

Produce a report with:

- `PASS`: requirements satisfied.
- `WARN`: non-blocking drift.
- `FAIL`: blocking governance issues that must be fixed before cleanup.

## Rules

- Auto-fix only low-risk index or path drift.
- Report policy conflicts instead of guessing.
- Preserve unrelated local settings and personal MCP configuration.
- Apply COSO framework as default when audit criteria are unspecified.

## Error Handling

| Scenario                       | Strategy                                                                   |
| ------------------------------ | -------------------------------------------------------------------------- |
| Unclear audit criteria         | Apply COSO as default; request criteria confirmation                       |
| Insufficient audit target info | Present interview question list; proceed from answers                      |
| No findings                    | Report "conforming" conclusion; include preventive improvement suggestions |
| Missing evidence               | Record as provisional finding; establish evidence collection plan          |
