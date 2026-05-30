---
name: stage-gate-review
description: Reviews whether a stage has met its completion criteria before progression. Use before moving between SDLC stages or when auditing a stage package.
---

# Stage-Gate Review

Validate stage completion against the workspace stage-gate matrix.

## Workflow

1. Determine the target stage explicitly or from `docs/00.agent-governance/memory/progress.md`.
2. Read `docs/00.agent-governance/rules/stage-gate-matrix.md`.
3. Verify that the current state adheres to the global constraints defined in `docs/LLM-WIKI.md` (e.g., TDD evidence presence, DESIGN.md initialization for UI work).
4. Verify required inputs, outputs, and completion criteria.
5. Return one of `PASS`, `PARTIAL`, or `FAIL`.
6. List blockers before any next-stage handoff.
7. For Stage 06, verify TDD evidence or documented exemptions for implementation tasks.
8. For Stage 10, verify incident record and postmortem expectations in the unified incident folder.
9. Update `docs/00.agent-governance/memory/progress.md` with the stage-gate result, blockers, and next sync point.

## Output

Include:

- required inputs
- completion checks
- blockers
- progression decision

## Rules

- A failed gate blocks progression.
- A skipped stage must be justified explicitly in downstream artifacts.
- Do not silently infer approval when required documents are missing.
- `PASS` allows proposing the next stage; it does not override human approval requirements.
- `progress.md` is the durable handoff state; `_workspace/**` is transient and cannot override it.
