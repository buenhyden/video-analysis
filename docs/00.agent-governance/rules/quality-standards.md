---
layer: agentic
---

# Agent Quality and Safety Standards (March 2026)

Repository-wide quality gates for governance and execution artifacts.

## 1. Quality Rubric

| Grade | Description | Expected State |
| :--- | :--- | :--- |
| A | Excellent | Actionable, traceable, link-valid, no policy conflicts |
| B | Good | Minor clarity gaps, still fully executable |
| C | Acceptable | Usable but missing depth in verification or traceability |
| D | Weak | Significant ambiguity, incomplete routing, or stale references |
| F | Failing | Unsafe, contradictory, or broken governance |

## 2. Mandatory Quality Gates

Before completion:

1. Run `preflight-checklist.md` exit gate.
2. Run reference checks from `reference-integrity.md`.
3. Confirm language policy compliance.
4. Confirm stage ownership and template mapping remain consistent.
5. Confirm root shim files still behave as thin routers.

## 3. Safety Baselines

- Never store secrets (tokens, API keys, passwords, private keys) in any repository-local file. This includes:
  - `docs/**`, `.github/**`, `.claude/**`, including `.claude/settings.local.json`
  - Workflow files (`.github/workflows/`), root config files, templates, and shims
  - Specifically prohibited patterns: `ghp_`, `gho_`, `github_pat_` (GitHub tokens), `sk-`, `AKIA` (AWS), and equivalent for other providers
  - See `rules/github-repository-governance.md` §4–§5 for GitHub-specific PAT policy and secret exposure response
- Do not include destructive instructions without explicit safeguards.
- Keep references environment-agnostic (no machine-specific absolute paths).
- Record assumptions and unresolved risks explicitly.

## 4. Test Coverage Gates (TDD)

Minimum requirements for task closure at Stage 06:

| Layer | Minimum Threshold | Evidence Required |
| :--- | :--- | :--- |
| Unit tests | All core behavior covered once an implementation stack exists | Test run log with pass/fail count |
| Integration tests | Critical paths covered | Integration test report |
| Agent evals (if applicable) | Defined metrics ≥ threshold | Eval run output |
| TDD cycle | RED → GREEN → REFACTOR documented | Task evidence field |

**Coverage target**: The base template may have no coverage artifact before a derived project declares an implementation stack. After a stack exists, every PR must provide parseable coverage evidence and meet the 90% line coverage gate. For each `impl` task, the corresponding `test` task must be recorded in the same task document with evidence of test passage before the `impl` task can be marked `done`.

## 5. Completion Standard

A governance update is complete only when:

- no broken internal references remain
- no rule conflicts remain unresolved
- no language policy violation remains
- stage-gate checklist can be executed without additional decisions

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
