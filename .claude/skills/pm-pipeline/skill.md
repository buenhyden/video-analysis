---
name: pm-pipeline
description: Full product management pipeline where an agent team collaborates to produce a roadmap, PRD, user stories, sprint plan, and PM review. Use for 'write a PRD', 'product roadmap', 'user stories', 'sprint planning', 'product requirements', 'feature specification', 'backlog grooming', 'product strategy', 'release planning', 'agile planning'. Also supports single-artifact mode (PRD only, user stories only, etc.) for existing products.
---

# PM Pipeline — Roadmap, PRD, User Stories, Sprint Plan, and Review

An agent team collaborates through: strategy → PRD → user stories + sprint plan → review.

## Execution Mode

**Agent Team** — agents communicate via SendMessage and cross-validate deliverables.

## Agent Composition

| Agent           | File                                | Role                                                                                     | Type            |
| --------------- | ----------------------------------- | ---------------------------------------------------------------------------------------- | --------------- |
| product-manager | `.claude/agents/product-manager.md` | Product strategy; roadmap; PRD authoring; user story writing; sprint plan design         | general-purpose |
| qa-inspector    | `.claude/agents/qa-inspector.md`    | Acceptance criteria validation; testability review; edge case coverage in stories        | general-purpose |
| code-reviewer   | `.claude/agents/code-reviewer.md`   | Consistency review — strategy ↔ PRD ↔ stories ↔ sprint plan; feasibility and scope check | general-purpose |

## Workflow

### Phase 1: Preparation (Orchestrator)

1. Extract from user input:
   - **Product Description**: What is being built and for whom
   - **Business Goal**: Metric to improve or problem to solve
   - **Scope** (optional): MVP / feature / full product
   - **Constraints** (optional): Timeline, team size, tech stack
   - **Existing Artifacts** (optional): Existing PRD, roadmap, or stories to extend
2. Create `_workspace/` at the project root.
3. Save organized input to `_workspace/00_input.md`.
4. If existing artifacts are provided, analyze them and skip corresponding phases.

### Phase 2: Team Assembly and Execution

| Order | Task              | Owner           | Dependencies | Artifact                           |
| ----- | ----------------- | --------------- | ------------ | ---------------------------------- |
| 1     | Product Roadmap   | product-manager | None         | `_workspace/01_product_roadmap.md` |
| 2     | PRD               | product-manager | Task 1       | `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md` |
| 3a    | User Stories      | product-manager | Task 2       | `_workspace/03_user_stories.md`    |
| 3b    | Acceptance Review | qa-inspector    | Task 2       | (informs 3a via SendMessage)       |
| 4     | Sprint Plan       | product-manager | Task 3a      | `docs/04.execution/plans/YYYY-MM-DD-<feature>.md` |
| 5     | PM Review         | code-reviewer   | Tasks 1–4    | `_workspace/05_review_report.md`   |

Tasks 3a and 3b can run **in parallel**.

**Inter-team Communication Flow:**

- Roadmap completes → delivers theme priorities and milestone targets to PRD; delivers business goals to code-reviewer for feasibility framing.
- PRD completes → delivers functional requirements to user story phase; delivers scope boundaries to qa-inspector for acceptance criteria design.
- qa-inspector → delivers testability requirements and edge case list to user story phase via SendMessage before stories are finalized.
- code-reviewer cross-validates strategy ↔ PRD ↔ stories ↔ sprint alignment. On blocking finding: requests fix from product-manager → rework → re-verify (max 2 rounds).

### Phase 3: Integration and Final Deliverables

1. Verify scratch artifacts in `_workspace/` and authoritative outputs in `docs/`.
2. Confirm all blocking findings from the review have been addressed.
3. Report final summary to the user.

## Execution Modes by Scope

| User Request Pattern                   | Execution Mode    | Agents Deployed                                |
| -------------------------------------- | ----------------- | ---------------------------------------------- |
| "Full PM workflow", "plan a product"   | **Full Pipeline** | All 3 agents                                   |
| "Write a PRD" (strategy exists)        | **PRD Mode**      | product-manager + qa-inspector + code-reviewer |
| "Write user stories" (PRD exists)      | **Stories Mode**  | product-manager + qa-inspector + code-reviewer |
| "Create a sprint plan" (stories exist) | **Sprint Mode**   | product-manager + code-reviewer                |
| "Review this PRD or roadmap"           | **Review Mode**   | code-reviewer only                             |

**Extending Existing Artifacts**: When existing artifacts are provided, product-manager analyzes gaps and generates only the missing or outdated sections.

## Data Transfer Protocol

| Strategy      | Method                  | Purpose                                       |
| ------------- | ----------------------- | --------------------------------------------- |
| File-based    | `docs/` + `_workspace/` | canonical final deliverables + transient coordination files |
| Message-based | SendMessage             | Acceptance criteria, edge cases, fix requests |
| Task-based    | TaskCreate/TaskUpdate   | Progress tracking, dependency management      |

## Error Handling

| Error Type                    | Strategy                                                                            |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| Ambiguous product description | Apply common SaaS/CRUD pattern; document assumptions in roadmap                     |
| No business goal specified    | Default to user engagement and retention; request validation before PRD             |
| Stories not testable          | qa-inspector flags and requests rewrite; document acceptance criteria first         |
| Agent failure                 | Retry once → if still failing, proceed without deliverable, note omission in review |
| Blocking finding in review    | Request fix from product-manager → rework → re-verify (max 2 rounds)                |
| Scope creep detected          | Flag in review report; recommend deferring to next milestone                        |

## Output Routing Rules

- Final PRDs must be stored in `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md`.
- Final sprint or implementation plans must be stored in `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`.
- `_workspace/` may keep drafts, review notes, and coordination artifacts only.
