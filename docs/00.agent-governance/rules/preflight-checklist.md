---
layer: agentic
title: 'Preflight Checklist Contract'
---

# Preflight Checklist Contract

Use this checklist before, during, and before closing every task.

## 1. Before Task (Entry Gate)

- [ ] For a newly derived project, confirm product/software and stack intake is complete before creating PRD, ARD, Spec, Plan, Task, Operations, or Reference documents.
- [ ] Confirm task anchor documents exist in `docs/01.requirements/` and `docs/03.specs/`, unless the task is the initial intake or governance setup itself.
- [ ] Identify target layer and compact docs path (`00.agent-governance`, `01.requirements` through `05.operations`, plus supporting `90.references`/`99.templates` when relevant) using `rules/stage-gate-matrix.md`.
- [ ] Read `docs/00.agent-governance/memory/methodology.md` and `docs/00.agent-governance/memory/progress.md`; initialize or repair `progress.md` from `docs/99.templates/progress.template.md` if missing.
- [ ] Activate matching persona and scope from `rules/persona.md` and `scopes/*.md`.
- [ ] Confirm constraints:
  - immutable areas (`docs/01~99` when explicitly protected by task policy)
  - language policy
  - safety constraints
- [ ] Confirm required template(s) from `docs/99.templates/` exist before creating any stage doc.
- [ ] Confirm the target stage document can satisfy the template-specific section contract enforced by `validate-doc-readiness.py`.
- [ ] Confirm stack-specific commands, frameworks, CI targets, and deployment assumptions are present in the intake before using them.
- [ ] If setup, validation prerequisites, local tooling, or runtime readiness are in scope, load `environment-readiness.md` and classify required versus optional tools before treating a missing tool as blocking.
- [ ] Read the template's `Hard Stop Conditions`, downstream trigger, and evidence rule before writing stage content.
- [ ] If frontend/mobile/app work is in scope: load `rules/design-system.md` and confirm `DESIGN.md` readiness.
- [ ] If running parallel agents: verify file ownership is non-overlapping across all active personas.

## 2. During Task (Execution Gate)

- [ ] Keep scope bounded to requested files and stage responsibilities.
- [ ] Keep root shims thin; move detail into `docs/00.agent-governance/*`.
- [ ] Update `docs/00.agent-governance/memory/progress.md` at phase boundaries, blockers, handoffs, and closure.
- [ ] Treat `_workspace/**` as transient runtime output only; promote durable findings before citing them as authority.
- [ ] Avoid policy duplication across root/provider/scope files.
- [ ] Maintain reference traceability to PRD/Spec.
- [ ] Record assumptions explicitly when source facts are unavailable.
- [ ] **If task touches `.github/**` or GitHub operational policy**: verify compliance with `rules/github-repository-governance.md`:
  - Branch protection rules still satisfied after change
  - CODEOWNERS paths match current repo structure; placeholder warning present if real owners not set
  - Required status check names unchanged (or branch protection rules updated accordingly)
  - No literal secrets (`ghp_`, `gho_`, `github_pat_`) in any tracked or shared file
  - Third-party actions pinned to full-length commit SHA (not tag or branch reference)

## 3. Before Close (Exit Gate)

- [ ] Run reference integrity checks from `rules/reference-integrity.md`.
- [ ] Verify no prohibited language in `docs/00.agent-governance/`.
- [ ] Verify all new/updated governance links resolve.
- [ ] If environment readiness was in scope, run `bash scripts/ws.sh setup` or record why the report was not needed.
- [ ] Verify stage-gate mapping remains decision-complete.
- [ ] Verify completion criteria for affected stage(s) are satisfied.
- [ ] Verify `docs/00.agent-governance/memory/progress.md` reflects the final task status or next handoff.
- [ ] **If creating a PR**: use `.github/PULL_REQUEST_TEMPLATE.md` as the PR body. Fill every section. Do not submit with placeholder text.

## 4. Hard Stop Conditions

Stop and resolve before proceeding if any condition is true:

- Missing project initialization intake for new-project stage authoring.
- Missing PRD/Spec anchors for implementation work.
- Persona/scope not selected.
- Broken internal references.
- Conflicting governance rules with no precedence.
- Missing core governance runtime prerequisites for a task that depends on local repository inspection or validation.
- Language policy violation in mutable files.

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
