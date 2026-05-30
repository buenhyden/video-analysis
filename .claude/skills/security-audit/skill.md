---
name: security-audit
description: Full security audit pipeline where an agent team performs vulnerability scanning, code security analysis, penetration test reporting, and remediation planning. Use for 'security audit', 'vulnerability scan', 'OWASP audit', 'SAST analysis', 'pentest report', 'security review', 'CVE scan', 'dependency vulnerabilities', 'secure code review', 'threat modeling', 'remediation roadmap'. Also supports targeted single-domain audits and compliance gap assessments.
---

# Security Audit — Vulnerability Scanning, Code Analysis, and Remediation Pipeline

An agent team collaborates through: vulnerability scanning → code analysis + pentest scenarios → remediation planning → final audit report.

## Execution Mode

**Agent Team** — agents communicate via SendMessage and cross-validate deliverables.

## Agent Composition

| Agent             | File                                  | Role                                                                                           | Type            |
| ----------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------- |
| security-engineer | `.claude/agents/security-engineer.md` | Vulnerability scanning; code security analysis; pentest scenarios; remediation recommendations | general-purpose |
| code-reviewer     | `.claude/agents/code-reviewer.md`     | Cross-validation — risk level calibration, finding consistency, final audit report synthesis   | general-purpose |

## Workflow

### Phase 1: Preparation (Orchestrator)

1. Extract from user input:
   - **Audit Target**: File paths, directories, repository, or system description
   - **Scope** (optional): Web app, API, infrastructure, dependencies, or all
   - **Compliance Framework** (optional): OWASP, PCI-DSS, HIPAA, SOC2, ISO 27001
   - **Existing Reports** (optional): Previous audit findings to re-verify or extend
   - **Risk Appetite** (optional): Conservative / Balanced / Aggressive
2. Create `_workspace/` at the project root.
3. Save organized input to `_workspace/00_input.md`.
4. If existing audit reports are provided, focus on delta analysis and unresolved findings.

### Phase 2: Team Assembly and Execution

| Order | Task               | Owner             | Dependencies | Artifact                              |
| ----- | ------------------ | ----------------- | ------------ | ------------------------------------- |
| 1a    | Vulnerability Scan | security-engineer | None         | `_workspace/01_vulnerability_scan.md` |
| 1b    | Code Analysis      | security-engineer | None         | `_workspace/02_code_analysis.md`      |
| 2     | Pentest Report     | security-engineer | Tasks 1a, 1b | `_workspace/03_pentest_report.md`     |
| 3     | Remediation Plan   | security-engineer | Task 2       | `docs/04.execution/plans/YYYY-MM-DD-<audit-scope>-remediation.md` |
| 4     | Final Audit Report | code-reviewer     | Tasks 1a–3   | `_workspace/05_audit_report.md`       |

Tasks 1a and 1b can run **in parallel**.

**Inter-team Communication Flow:**

- Vulnerability scan → delivers CVE findings and severity scores to code analysis; delivers attack surface map to pentest phase.
- Code analysis → delivers SAST findings and insecure patterns to pentest phase; delivers high-risk code regions to remediation planning.
- Pentest report → delivers exploitability evidence to remediation planning; delivers critical findings to code-reviewer for immediate escalation.
- code-reviewer cross-validates all findings, calibrates risk levels, and synthesizes the final report. On blocking finding: requests fix → rework → re-verify (max 2 rounds).

### Phase 3: Integration and Final Deliverables

1. Verify canonical remediation plan output plus transient audit artifacts in `_workspace/`.
2. Confirm all Critical and High findings have remediation entries.
3. Report final summary to the user.

## Execution Modes by Scope

| User Request Pattern                        | Execution Mode         | Agents Deployed                   |
| ------------------------------------------- | ---------------------- | --------------------------------- |
| "Full security audit"                       | **Full Pipeline**      | Both agents                       |
| "Scan dependencies for CVEs"                | **Dependency Mode**    | security-engineer + code-reviewer |
| "SAST / code security review"               | **Code Analysis Mode** | security-engineer + code-reviewer |
| "Write a pentest report"                    | **Pentest Mode**       | security-engineer + code-reviewer |
| "Build a remediation plan" (findings exist) | **Remediation Mode**   | security-engineer + code-reviewer |
| "Review this audit report"                  | **Review Mode**        | code-reviewer only                |

**Compliance Mapping**: When a compliance framework is specified, findings are mapped to relevant controls (e.g., OWASP Top 10, PCI-DSS requirements) in each artifact.

## Data Transfer Protocol

| Strategy      | Method                  | Purpose                                             |
| ------------- | ----------------------- | --------------------------------------------------- |
| File-based    | `docs/04.execution/plans/` + `_workspace/` | authoritative remediation artifact + transient audit artifacts |
| Message-based | SendMessage             | Real-time critical finding escalation, fix requests |
| Task-based    | TaskCreate/TaskUpdate   | Progress tracking, dependency management            |

## Error Handling

| Error Type                  | Strategy                                                                            |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Audit target not specified  | Request clarification; default to current project directory                         |
| No source code access       | Perform black-box analysis; note limitations in report                              |
| False positive saturation   | Apply risk-based filtering; document suppression rationale                          |
| Agent failure               | Retry once → if still failing, proceed without deliverable, note omission in report |
| Blocking finding in review  | Request fix from security-engineer → rework → re-verify (max 2 rounds)              |
| Critical finding discovered | Escalate immediately via SendMessage before completing current phase                |

## Output Routing Rules

- Final remediation plans must be stored in `docs/04.execution/plans/`.
- `_workspace/` is reserved for transient scan, analysis, pentest, and audit-report coordination files.
