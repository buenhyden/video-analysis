---
name: test-automation
description: Full test automation pipeline where an agent team collaborates on strategy, unit testing, integration testing, and coverage analysis. Use for 'automate tests', 'write unit tests', 'integration testing', 'test coverage', 'TDD setup', 'test strategy', 'test pyramid', 'write test cases', 'CI test integration', 'QA automation'. Also supports single-layer test creation and coverage improvement for existing codebases.
---

# Test Automation — Strategy, Writing, Integration, and Coverage Pipeline

An agent team collaborates through: test strategy → unit testing + integration testing → coverage analysis → review.

## Execution Mode

**Agent Team** — agents communicate via SendMessage and cross-validate deliverables.

## Agent Composition

| Agent         | File                              | Role                                                                          | Type            |
| ------------- | --------------------------------- | ----------------------------------------------------------------------------- | --------------- |
| qa-inspector  | `.claude/agents/qa-inspector.md`  | Test strategy; unit test writing; integration test writing; coverage analysis | general-purpose |
| code-reviewer | `.claude/agents/code-reviewer.md` | Cross-validation — strategy vs. tests vs. coverage consistency; final review  | general-purpose |

## Workflow

### Phase 1: Preparation (Orchestrator)

1. Extract from user input:
   - **Target Code**: File paths, directories, or modules to test
   - **Language/Framework**: Auto-detect or user-specified
   - **Test Scope** (optional): Unit, integration, E2E, or all
   - **Coverage Target** (optional): Line coverage %, branch coverage %
   - **Existing Tests** (optional): Existing test files to extend
2. Create `_workspace/` at the project root.
3. Save organized input to `_workspace/00_input.md`.
4. If existing tests are provided, analyze gaps before proceeding.

### Phase 2: Team Assembly and Execution

| Order | Task              | Owner         | Dependencies | Artifact                             |
| ----- | ----------------- | ------------- | ------------ | ------------------------------------ |
| 1     | Test Strategy     | qa-inspector  | None         | `_workspace/01_test_strategy.md`     |
| 2a    | Unit Tests        | qa-inspector  | Task 1       | `_workspace/02_unit_tests.md`        |
| 2b    | Integration Tests | qa-inspector  | Task 1       | `_workspace/03_integration_tests.md` |
| 3     | Coverage Analysis | qa-inspector  | Tasks 2a, 2b | `_workspace/04_coverage_report.md`   |
| 4     | Review            | code-reviewer | Tasks 1–3    | `_workspace/05_review_report.md`     |

Tasks 2a and 2b can run **in parallel**.

**Inter-team Communication Flow:**

- Test strategy completes → delivers test pyramid design and tool selection to unit/integration test phases; delivers scope and risk areas to coverage analysis.
- Unit tests complete → flag complex mock-heavy areas to integration test phase.
- Integration tests complete → flag slow or flaky tests to coverage analyst.
- code-reviewer cross-validates strategy ↔ test quality ↔ coverage. On blocking finding: requests fix → rework → re-verify (max 2 rounds).

### Phase 3: Integration and Final Deliverables

1. Verify transient coordination files in `_workspace/`.
2. Promote authoritative test strategy and execution evidence to `docs/03.specs/<feature-id>/tests.md` and `docs/04.execution/tasks/` before handoff.
3. Confirm all blocking findings from the review have been addressed.
4. Report final summary to the user.

## Execution Modes by Scope

| User Request Pattern                    | Execution Mode       | Agents Deployed              |
| --------------------------------------- | -------------------- | ---------------------------- |
| "Automate all tests", "full test suite" | **Full Pipeline**    | Both agents                  |
| "Write unit tests only"                 | **Unit Mode**        | qa-inspector + code-reviewer |
| "Write integration tests only"          | **Integration Mode** | qa-inspector + code-reviewer |
| "Analyze coverage gaps"                 | **Coverage Mode**    | qa-inspector + code-reviewer |
| "Review our test strategy"              | **Strategy Mode**    | qa-inspector + code-reviewer |

**Extending Existing Tests**: If existing tests are provided, qa-inspector analyzes gaps first and only generates missing coverage.

## Data Transfer Protocol

| Strategy      | Method                  | Purpose                                          |
| ------------- | ----------------------- | ------------------------------------------------ |
| File-based    | `_workspace/` directory | Store transient test coordination artifacts      |
| Message-based | SendMessage             | Real-time key information delivery, fix requests |
| Task-based    | TaskCreate/TaskUpdate   | Progress tracking, dependency management         |

## Error Handling

| Error Type                        | Strategy                                                                            |
| --------------------------------- | ----------------------------------------------------------------------------------- |
| Target code not specified         | Request clarification; offer to analyze the full project directory                  |
| Language/framework not identified | Auto-detect from file extensions and import statements                              |
| Untestable code (no DI, globals)  | Note in strategy; provide refactoring suggestions alongside tests                   |
| Agent failure                     | Retry once → if still failing, proceed without deliverable, note omission in review |
| Blocking finding in review        | Request fix from qa-inspector → rework → re-verify (max 2 rounds)                   |
| Coverage target unreachable       | Document gap with risk assessment; prioritize by business criticality               |
