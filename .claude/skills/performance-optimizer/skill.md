---
name: performance-optimizer
description: Full performance optimization pipeline where an agent team performs profiling, bottleneck analysis, optimization implementation, and benchmarking. Use for 'optimize performance', 'profiling', 'bottleneck analysis', 'slow queries', 'memory leak', 'CPU optimization', 'benchmark', 'performance regression', 'latency reduction', 'throughput improvement', 'caching strategy'. Also supports targeted single-layer optimization and regression prevention for existing systems.
---

# Performance Optimizer — Profiling, Analysis, Optimization, and Benchmarking Pipeline

An agent team collaborates through: profiling → bottleneck analysis → optimization → benchmarking → review.

## Execution Mode

**Agent Team** — agents communicate via SendMessage and cross-validate deliverables.

## Agent Composition

| Agent            | File                                 | Role                                                                                         | Type            |
| ---------------- | ------------------------------------ | -------------------------------------------------------------------------------------------- | --------------- |
| code-reviewer    | `.claude/agents/code-reviewer.md`    | Profiling analysis; bottleneck identification; optimization implementation; benchmark design | general-purpose |
| system-architect | `.claude/agents/system-architect.md` | Architecture-level optimization; query redesign; caching strategy; regression prevention     | general-purpose |

## Workflow

### Phase 1: Preparation (Orchestrator)

1. Extract from user input:
   - **Target System**: File paths, service names, or system description
   - **Performance Concern**: Latency, throughput, CPU, memory, I/O, or specific slow path
   - **Baseline Metrics** (optional): Current measured performance numbers
   - **Performance Target** (optional): Desired SLA, p99, or throughput goal
   - **Constraints** (optional): Cannot change DB schema, must stay on current framework, etc.
2. Create `_workspace/` at the project root.
3. Save organized input to `_workspace/00_input.md`.
4. If existing profiling data or benchmark results are provided, skip to bottleneck analysis.

### Phase 2: Team Assembly and Execution

| Order | Task                | Owner            | Dependencies | Artifact                               |
| ----- | ------------------- | ---------------- | ------------ | -------------------------------------- |
| 1     | Profiling Report    | code-reviewer    | None         | `_workspace/01_profiling_report.md`    |
| 2     | Bottleneck Analysis | code-reviewer    | Task 1       | `_workspace/02_bottleneck_analysis.md` |
| 3a    | Optimization Plan   | code-reviewer    | Task 2       | `docs/04.execution/plans/YYYY-MM-DD-<target>-optimization.md` |
| 3b    | Architecture Review | system-architect | Task 2       | (informs 3a via SendMessage)           |
| 4     | Benchmark Results   | code-reviewer    | Task 3a      | `_workspace/04_benchmark_results.md`   |
| 5     | Review Report       | system-architect | Tasks 1–4    | `_workspace/05_review_report.md`       |

Tasks 3a and 3b can run **in parallel**.

**Inter-team Communication Flow:**

- Profiling report → delivers hotspot map to bottleneck analysis; delivers I/O and query patterns to system-architect.
- Bottleneck analysis → delivers root causes and impact estimates to optimization plan; sends architecture-level blockers to system-architect.
- system-architect → delivers architecture trade-offs, query redesign options, and caching recommendations to optimization plan via SendMessage.
- code-reviewer synthesizes all findings into the final review, checking for regression risk and validating benchmark results.

### Phase 3: Integration and Final Deliverables

1. Verify authoritative plan output in `docs/04.execution/plans/` plus transient artifacts in `_workspace/`.
2. Confirm benchmark results show improvement relative to baseline.
3. Report final summary to the user.

## Execution Modes by Scope

| User Request Pattern                        | Execution Mode     | Agents Deployed                  |
| ------------------------------------------- | ------------------ | -------------------------------- |
| "Full performance optimization"             | **Full Pipeline**  | Both agents                      |
| "Profile this code"                         | **Profiling Mode** | code-reviewer only               |
| "Find the bottleneck"                       | **Analysis Mode**  | code-reviewer + system-architect |
| "Optimize these queries"                    | **Query Mode**     | code-reviewer + system-architect |
| "Design a caching strategy"                 | **Caching Mode**   | system-architect + code-reviewer |
| "Run benchmarks" (optimization plan exists) | **Benchmark Mode** | code-reviewer only               |

**Using Existing Data**: If profiling data or benchmark baselines are provided, `code-reviewer` skips the profiling phase and begins directly at bottleneck analysis.

## Data Transfer Protocol

| Strategy      | Method                  | Purpose                                     |
| ------------- | ----------------------- | ------------------------------------------- |
| File-based    | `docs/04.execution/plans/` + `_workspace/` | authoritative optimization artifact + transient analysis files |
| Message-based | SendMessage             | Architecture trade-offs, real-time findings |
| Task-based    | TaskCreate/TaskUpdate   | Progress tracking, dependency management    |

## Error Handling

| Error Type                        | Strategy                                                                            |
| --------------------------------- | ----------------------------------------------------------------------------------- |
| No profiling access               | Perform static analysis; estimate hotspots from code structure                      |
| No baseline metrics               | Establish synthetic baseline before optimization; document assumptions              |
| Optimization conflicts            | system-architect performs trade-off analysis; document decisions in review report   |
| Agent failure                     | Retry once → if still failing, proceed without deliverable, note omission in report |
| Benchmark regression detected     | Block optimization; investigate regression cause before proceeding                  |
| Architecture constraint violation | Offer constraint-respecting alternative; note trade-off in review                   |

## Output Routing Rules

- Final optimization plans must be stored in `docs/04.execution/plans/`.
- `_workspace/` may retain profiling, bottleneck, and benchmark notes only as transient working artifacts.
