---
name: workspace-governance
description: Unified workspace governance runtime for planning, executing, validating, and synchronizing docs, Git policy, CI/CD, agent docs, scripts, environment consistency, and commit/PR message work.
---

# Workspace Governance

Mode-based governance orchestration for the Project-Template workspace. This skill is owned by `governance-architect` and coordinates existing governance agents and skills; it does not replace their scope boundaries.

## When to Use

Use this skill for workspace governance work involving one or more of:

- docs structure, templates, READMEs, or documentation policy
- Git workflow, Conventional Commits, PR policy, or commit-runtime output
- CI/CD workflows, quality gates, scripts, or environment consistency
- AGENTS.md, CLAUDE.md, GEMINI.md, `.claude/**`, or governance runtime sync
- cross-domain governance plans that must be grouped into logical commit units

## Global Rules

- Keep this repository language-agnostic. Do not introduce a default application stack.
- Use `AGENTS.md` as the primary workspace policy router.
- Keep `CLAUDE.md` and `GEMINI.md` thin provider wrappers.
- Store durable governance policy in `docs/00.agent-governance/`.
- Store templates only in `docs/99.templates/`.
- Treat `main` as the release-template skeleton: project-content folders keep README guides only until derived-project intake creates project docs.
- Require product/software and stack intake before creating new-project stage documents.
- Keep `dev` as the active integration branch.
- Treat issue IDs as optional: include them when known or available; do not invent one.
- Do not push directly to `main` or `dev`; use PRs.
- Group all proposed or executed work into 1-commit-1-change units.
- Do not add AI review, issue triage, rebase, rollback, branch cleanup, or deployment workflows unless explicitly requested.

## Context Priority

Read and reconcile policy in this order:

1. `AGENTS.md`
2. `docs/00.agent-governance/`
3. `.claude/`
4. `.codex/`
5. `CLAUDE.md`, `GEMINI.md`
6. Stage docs under `docs/01.requirements/` through `docs/99.templates/`
7. `.github/workflows/`
8. `scripts/`, `ci/`, `tools/`
9. Relevant local skills: `agent-md-refactor`, `claude-md-improver`, `cicd-automation-workflow-automate`, `github-workflow-automation`

Conflict rule: preserve `AGENTS.md` as SSOT, then update dependent files instead of duplicating policy.

## Non-Negotiables

- Do not invent files, folders, workflows, scripts, tools, or stack requirements.
- Do not add language-specific scaffolding unless the current workspace already requires it.
- Do not push directly to protected branches (`main` and `dev`) or legacy integration branch names.
- Do not delete, move, merge, or rename files until references are searched and replacement references are planned.
- Prefer minimal reusable governance over application-specific implementation.

## Required Reading

For every mode, read only the minimum relevant subset first:

- Root routers: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- Runtime: `.claude/CLAUDE.md`, `.claude/agents/`, `.claude/skills/`
- Compatibility: `.codex/agents/`; `.agents/**` may exist only as a legacy mirror and must not define independent policy.
- Governance: `docs/00.agent-governance/`
- CI/CD: `.github/workflows/`, `scripts/README.md`, referenced scripts
- Stage docs: target `docs/<stage>/README.md`, `docs/99.templates/`

## Inventory Checklist

For every cross-domain request, inventory and report the current state before proposing changes:

- Git state: branch, changed files, staged files, and untracked files.
- Docs: top-level `docs/` folders, required README files, templates, and allowed subfolders.
- Agent docs: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/**`, and `docs/00.agent-governance/**`.
- CI/CD: `.github/workflows/*.yml`, triggers, protected-branch behavior, permissions, timeouts, and quality gates.
- Scripts: `scripts/`, `ci/`, `tools/`, and workflow references; document absent `ci/` or `tools/` instead of creating them.
- Environment: declared tool versions and settings from manifests, lockfiles, Dockerfiles, workflow setup steps, and validation scripts.
- Templates: `docs/99.templates/` metadata, status, usage target, and duplicate or obsolete candidates.

## Shared Execution Pattern

1. Read required files.
2. Inventory current state.
3. Detect gaps, conflicts, duplication, drift, and policy violations.
4. Group work by purpose and logical commit unit.
5. Produce a plan or execute scoped changes according to mode.
6. Sync policy changes to root/provider/runtime docs.
7. Validate with the required gates.
8. Output findings, changed paths or target paths, validation evidence, and commit groups.

## Mode Contract Rules

- Inputs must name the mode, target paths or domains, and any known issue IDs.
- Constraints must preserve the Global Rules and mode-specific boundaries.
- Outputs must use the listed contract keys; do not invent alternate schemas.
- Success criteria must be explicit, verifiable, and tied to validation gates.

## Task Groups

Use these task groups to keep work commit-sized:

| Group | Purpose |
| --- | --- |
| docs-governance | Normalize docs structure, README files, templates, and latest-state documentation. |
| agent-docs-governance | Align root/provider/runtime agent docs and detailed governance rules. |
| git-governance | Document Git Flow, PR-only policy, Conventional Commits, issue traceability, and 1 commit = 1 logical change. |
| cicd-governance | Improve workflows, release promotion, reusable components, and quality gates. |
| script-governance | Inventory, deduplicate, consolidate, and validate scripts and references. |
| environment-governance | Align dev, QA, and CI/CD versions/settings without adding stack defaults. |
| commit-pr-runtime | Produce logical commit groups, Conventional Commit messages, validation summary, and PR body. |

## Modes

### `plan-docs`

Plan docs structure cleanup, template normalization, and latest-state documentation updates.

Input: target docs paths or domains.

Output:

- overview
- findings
- grouped_tasks: `[{id, category, target_paths, expected_result}]`
- sync_targets

Success criteria: invalid docs structure, template gaps, README drift, sync targets, and commit-sized tasks are identified without editing files.

### `execute-docs`

Analyze docs structure and execute or propose concrete docs governance changes.

Rules:

- Do not introduce language-specific scaffolding.
- Preserve useful content when consolidating.

Output:

- findings
- structure_actions
- template_actions
- documentation_updates
- agent_doc_sync
- suggested_commit_groups

Success criteria: docs changes preserve the allowed folder policy, template SSOT, useful content, README indexes, agent-doc sync, and validation evidence.

### `plan-git`

Plan Git policy standardization for AI agents and workspace docs.

Input: target Git policy files or known conflict areas.

Must cover:

- git-flow with `main` and `dev`
- PR-only protected branches
- 1 commit = 1 logical change
- Conventional Commits
- optional issue linking when known or available

Output:

- findings
- target_sections
- grouped_tasks

Success criteria: branch naming, PR-only rules, Conventional Commits, optional issue linking, and commit-sized doc tasks are unambiguous.

### `execute-git`

Produce concise Git governance content updates and commit-runtime alignment.

Input: target Git policy files and known drift findings.

Output:

- policy_drafts
- file_targets
- suggested_commit_groups

Success criteria: active Git policy uses `dev`, treats issue IDs as optional when known or available, preserves PR-only protected branches, and syncs root/provider/runtime references.

### `plan-ci-cd`

Plan CI/CD improvements, workflow normalization, quality gates, scripts, and environment consistency.

Input: workflow files, referenced scripts, and environment/version sources.

Must cover:

- desired branch and PR pipeline behavior
- required workflows and reusable components
- quality gates
- duplication reduction
- script cleanup
- local, QA, and CI/CD version/settings alignment
- agent-doc sync targets

Output:

- desired_pipeline_model
- workflow_plan
- quality_gate_plan
- duplication_reduction_plan
- script_cleanup_plan
- environment_alignment_plan
- sync_targets

Success criteria: workflow gaps, quality gates, duplication, script reuse, environment drift, and agent-doc sync tasks are planned without adding unrelated automation.

### `execute-ci-cd`

Analyze workflows, scripts, and environment consistency, then execute or propose concrete governance improvements.

Rules:

- Avoid duplicate workflow logic.
- Prefer reusable workflows, composite actions, matrices, or shared scripts where appropriate.
- Treat secrets, deployment behavior, and environment changes as high risk.

Output:

- workflow_inventory
- duplication_findings
- script_findings
- quality_gate_gaps
- environment_drift_findings
- proposed_changes
- agent_doc_sync
- suggested_commit_groups

Success criteria: workflow behavior remains PR-only for protected branches, no workflow self-merges, duplicate logic is reduced, scripts are consistently referenced, and validation evidence is produced.

### `plan-agent-docs`

Plan synchronization of `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.

Input: root/provider/runtime docs and known drift findings.

Output:

- target_doc_model
- section_plan
- grouped_tasks

Success criteria: `AGENTS.md` stays the SSOT, provider docs stay thin, detailed rules route to governance docs, and planned updates are commit-sized.

### `execute-agent-docs`

Produce concise governance content updates for root and provider agent docs.

Rules:

- `AGENTS.md` remains the primary policy router.
- `CLAUDE.md` and `GEMINI.md` summarize or reference it.
- Use progressive disclosure; move detail to governance docs.

Output:

- AGENTS_md_proposal
- CLAUDE_md_proposal
- GEMINI_md_proposal
- suggested_commit_groups

Success criteria: root/provider/runtime docs agree on required reading, docs policy, Git policy, CI/CD gates, validation commands, and progressive disclosure.

### `plan-workspace`

Create an integrated governance plan across docs, Git, agent docs, CI/CD, scripts, and environment consistency.

Input: findings or plans from docs, Git, CI/CD, and agent-doc domains.

Output:

- roadmap
- dependency_order
- validation_points
- commit_boundaries

Success criteria: cross-domain dependencies, risks, validation checkpoints, and logical commit boundaries are decision-complete.

### `execute-workspace`

Produce or execute an integrated governance proposal across all governance areas.

Input: domain findings, target paths, branch context, and known issue IDs if available.

Output:

- consolidated_findings
- resolved_conflicts
- final_task_groups
- final_validation_checklist

Success criteria: conflicts are resolved once, active docs/workflows/scripts/runtime references are mutually consistent, and final task groups are independently committable.

### `commit-runtime`

Generate commit and PR messages from grouped changes under workspace Git policy.

Input:

```yaml
grouped_changes:
  - paths: []
    purpose: string
    issue_ids: [] # optional
branch_name: string
target_branch: dev | main
```

Rules:

- Reject mixed-scope change groups.
- Use Conventional Commits: `<type>(<optional-scope>): <summary>`.
- Keep subject lines at or below 72 characters.
- Include issue IDs when available; do not fail when absent.
- Never suggest direct push to `main` or `dev`.
- Prefer PR titles that follow Conventional Commits.

Output:

```yaml
commits:
  - message: string
    included_paths: []
pr:
  title: string
  description: string
  target_branch: dev | main
  issue_ids: []
```

Success criteria: mixed-scope groups are rejected, commit subjects are conventional and <= 72 characters, issue IDs are included only when supplied, and PR output targets `dev` or `main` through review.

## Output Contract

For workspace-level responses, return:

1. Workspace summary.
2. Inventory findings.
3. Policy violations and risks.
4. Proposed commit-sized task groups.
5. Files to create, update, move, or remove.
6. Validation checklist and results.
7. Agent docs sync requirements.
8. Suggested Conventional Commit messages.
9. Suggested PR title and body.

If required information is missing, add an inventory task instead of guessing.

## Done Definition

Complete governance work only when:

- `docs/` has only allowed top-level folders and each has `README.md`.
- Root/provider/runtime agent docs and `docs/00.agent-governance/` are consistent.
- CI/CD quality gates are defined, runnable, and free of unnecessary duplicate jobs or steps.
- Scripts are inventoried and workflow references are valid.
- Tech-stack versions are aligned or drift is documented; stack gates remain conditional unless the stack exists.
- Changes are grouped into logical commits and PR output includes validation results.

## Validation Gates

Use the relevant subset, and run all for cross-domain governance changes:

```bash
bash scripts/validation/validate-skill-quality.sh
bash scripts/validation/validate-docs.sh
bash scripts/validation/validate-doc-governance.sh
bash scripts/validation/validate-cross-links.sh
python3 scripts/validation/validate-github-workflows.py
bash scripts/ws.sh validate
```

## File References

- `AGENTS.md`
- `.claude/agents/governance-architect.md`
- `docs/00.agent-governance/rules/harness-library.md`
- `docs/00.agent-governance/rules/git-workflow.md`
- `docs/00.agent-governance/rules/ci-cd-workflow.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
