---
name: code-review
description: Full automated code review pipeline. An agent team systematically reviews four domains — style, security, performance, and architecture — and synthesizes findings into a final verdict. Use for 'review this code', 'code inspection', 'PR review', 'code quality analysis', 'security review', 'performance review', 'architecture review', 'code style check'. Also supports single-domain reviews. Actual CI/CD integration, auto-fix, and Git commit/merge operations are outside scope.
---

# Code Review — Automated Multi-Domain Review Pipeline

An agent team systematically reviews code across style, security, performance, and architecture, then synthesizes a final verdict.

## Execution Mode

**Agent Team** — agents run parallel domain reviews, then the synthesizer produces the final report.

## Agent Composition

| Agent             | File                                  | Role                                                                | Type            |
| ----------------- | ------------------------------------- | ------------------------------------------------------------------- | --------------- |
| code-reviewer     | `.Codex/agents/code-reviewer.md`     | Orchestrates review; owns style, performance, and synthesis domains | general-purpose |
| security-engineer | `.Codex/agents/security-engineer.md` | Security vulnerabilities, injection, authentication, data exposure  | general-purpose |
| system-architect  | `.Codex/agents/system-architect.md`  | Design patterns, SOLID principles, dependencies, coupling           | general-purpose |

## Workflow

### Phase 1: Preparation (Orchestrator)

1. Extract from user input:
   - **Target Code**: File paths, PR number, diff, or directory
   - **Language/Framework**: Auto-detect or user-specified
   - **Review Scope** (optional): Specific domains only
   - **Context** (optional): PR description, related issues, change rationale
   - **Style Guide** (optional): Team-specific conventions
2. Create `_workspace/` at the project root.
3. Save organized input to `_workspace/00_input.md`.
4. Identify target code and determine review scope.
5. Determine **execution mode** based on request scope.

### Phase 2: Team Assembly and Execution

| Order | Task                    | Owner             | Dependencies | Artifact                               |
| ----- | ----------------------- | ----------------- | ------------ | -------------------------------------- |
| 1a    | Style Review            | code-reviewer     | None         | `_workspace/01_style_review.md`        |
| 1b    | Security Review         | security-engineer | None         | `_workspace/02_security_review.md`     |
| 1c    | Performance Review      | code-reviewer     | None         | `_workspace/03_performance_review.md`  |
| 1d    | Architecture Review     | system-architect  | None         | `_workspace/04_architecture_review.md` |
| 2     | Comprehensive Synthesis | code-reviewer     | Tasks 1a–1d  | `_workspace/05_review_summary.md`      |

Tasks 1a–1d (all domain reviews) run **in parallel**.

**Inter-team Communication Flow:**

- Style review → flags sensitive info in comments to security-engineer; flags complex functions to performance pass.
- Security review → flags security-measure performance impacts and authentication architecture to system-architect.
- Performance review → flags structural bottlenecks to system-architect.
- code-reviewer synthesizes all domain findings, resolves cross-domain conflicts, and renders the final verdict.

### Phase 3: Integration and Final Artifacts

1. Verify all domain reviews in `_workspace/`.
2. Determine final verdict: Approve / Request Changes / Reject.
3. Report final summary to the user.

## Execution Modes by Scope

| User Request Pattern              | Execution Mode        | Agents Deployed                               |
| --------------------------------- | --------------------- | --------------------------------------------- |
| "Review this code", "full review" | **Full Review**       | All 3 agents                                  |
| "Security review only"            | **Security Mode**     | security-engineer + code-reviewer (synthesis) |
| "Analyze performance"             | **Performance Mode**  | code-reviewer only                            |
| "Architecture review"             | **Architecture Mode** | system-architect + code-reviewer (synthesis)  |
| "Just check code style"           | **Style Mode**        | code-reviewer only                            |

**PR Review**: When a PR number is provided, extract the diff and focus review on changed code. Reference full file context but concentrate on the diff.

## Data Transfer Protocol

| Strategy      | Method                  | Purpose                                                   |
| ------------- | ----------------------- | --------------------------------------------------------- |
| File-based    | `_workspace/` directory | Store transient review coordination artifacts             |
| Message-based | SendMessage             | Real-time findings transfer, additional analysis requests |
| Task-based    | TaskCreate/TaskUpdate   | Progress tracking, dependency management                  |

## Error Handling

| Error Type              | Strategy                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------ |
| Language not identified | Auto-detect from file extensions and code patterns                                   |
| Large codebase          | Focus on changed or core files; note scope in review report                          |
| Agent failure           | Retry once → if still failing, proceed without that domain, note omission in summary |
| Cross-domain conflict   | code-reviewer performs trade-off analysis and renders verdict                        |
| Insufficient context    | Review based on code alone; note limitations in summary                              |
