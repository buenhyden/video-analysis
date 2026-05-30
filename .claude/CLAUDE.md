# CLAUDE.md

> [!IMPORTANT]
> Claude runtime bootstrap for this workspace. Follow [AGENTS.md](../AGENTS.md) first; this file only defines local Claude execution details.

## Load Order

@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/rules/agentic.md
@docs/00.agent-governance/rules/harness-library.md
@docs/00.agent-governance/rules/persona.md
@docs/00.agent-governance/rules/project-initialization-intake.md
@docs/00.agent-governance/rules/template-document-lifecycle.md
@docs/00.agent-governance/rules/standards.md
@AGENTS.md

## Runtime Surface

- Canonical runtime agents: `.claude/agents/*.md`
- Canonical runtime skills: `.claude/skills/*/skill.md`
- SDLC orchestration: `.claude/skills/spec-driven-sdlc/skill.md`
- Unified governance: `.claude/skills/workspace-governance/skill.md`
- Codex compatibility view: `.codex/agents/*.toml`
- Portable event hook dispatcher: `bash scripts/ws.sh hook <event> [matcher]`
- Agent-first and harness lifecycle rules: `docs/00.agent-governance/rules/agentic.md` and `docs/00.agent-governance/rules/harness-library.md`

## Execution Rules

- Analyze -> Plan -> Execute -> Validate -> Sync.
- For newly derived projects, collect product/software and stack intake before creating PRD, ARD, ADR, spec, plan, task, operations, or reference documents.
- Classify Project-Template documents with `template-document-lifecycle.md` before reusing, moving, or deleting template-maintenance history.
- On `main`, keep `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/` as release-template skeleton guides only.
- For non-README stage documents in `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/`, select the matching `docs/99.templates/` contract before writing and halt if required sections would be missing.
- Load `docs/00.agent-governance/rules/design-system.md` only when frontend, mobile, app, or UI work is in scope; root `DESIGN.md` remains the hard-stop router for that work.
- Create or update a Stage 05 plan in `docs/04.execution/plans/` before non-trivial implementation.
- Track execution evidence in `docs/04.execution/tasks/`.
- Use `docs/99.templates/` for new governed documents; `validate-doc-readiness.py` enforces stage-specific template markers for non-README docs.
- Run `ws validate` or `bash scripts/ws.sh validate` before commit, push, PR, or final handoff for governed changes.

## Git And PR Rules

- Use `dev` as the integration branch and `main` as production.
- Use PR-only changes to `main` and `dev`; do not push directly to protected branches.
- Use Conventional Commits and 1-commit-1-change.
- Use `.github/PULL_REQUEST_TEMPLATE.md` for PR bodies.

## Hook Enforcement Catalog

The following hooks run automatically. Do not re-implement what they already enforce.

| Event              | Matcher                        | Hook                                 | Enforces                                                                                 |
| :----------------- | :----------------------------- | :----------------------------------- | :--------------------------------------------------------------------------------------- |
| SessionStart       | `*`                            | `session-start.sh`                   | Workspace context summary (branch, changed files, governance health)                     |
| PreToolUse         | `Bash`                         | `git-policy-enforce.sh`              | Blocks direct pushes to `main`/`dev`; enforces branch naming and commit policy           |
| PreToolUse         | `Read\|Write\|Edit\|MultiEdit` | `pre-tool-validate.sh`               | Blocks sensitive files, forbidden runtime policy surfaces, unsafe workflow patterns, and pending stage-document writes that miss template contracts |
| PreToolUse         | `Bash`                         | inline hint                          | Surfaces optional generated Graphify context when search commands are run; canonical docs remain authoritative |
| PostToolUse        | `Write\|Edit\|MultiEdit`       | `docs-readme-sync.sh`                | Auto-syncs folder README indexes after docs/ edits — do not do this manually             |
| PostToolUse        | `Write\|Edit\|MultiEdit`       | `post-tool-format.sh`                | Applies safe whitespace normalization and optional local formatters after file edits      |
| PostToolUse        | `Write\|Edit\|MultiEdit`       | `post-tool-validate.sh`              | Validates governance, template readiness, and workflow files after each write             |
| PostToolUseFailure | `*`                            | `error-logger.sh`                    | Logs tool failures (non-blocking) to `_workspace/diagnostics/hook-errors.log`            |
| PreCompact         | `*`                            | `pre-compact-context.sh`             | Saves branch/changes/active-task snapshot to `_workspace/diagnostics/` before compaction |
| Stop               | `*`                            | governance validators + `stop-completion-governance.sh` | Runs docs governance/template-readiness checks and blocks silent stop with uncommitted changes |

Note: `pr-template-enforce.sh` is a backward-compatibility alias for `git-policy-enforce.sh`. It is used by `ws hook PreToolUse pr-template` for Codex compatibility and is not wired as a separate Claude Code event.

## Runtime Gotchas

- New agents must be reflected in `docs/00.agent-governance/rules/harness-library.md`, `docs/00.agent-governance/rules/persona.md`, `docs/00.agent-governance/policy-change-log.md`, and `docs/LLM-WIKI.md`.
- Workflow edits are guarded by `.claude/hooks/pre-tool-validate.sh` and `.claude/hooks/post-tool-validate.sh`; follow `docs/00.agent-governance/rules/ci-cd-workflow.md` for workflow policy.
- `.claude/settings.json` owns hook event configuration. Do not create `.codex/hooks.json` or `.codex/hooks/**`; use `bash scripts/ws.sh hook <event> [matcher]` when Codex or another local agent must run the same hook event. The dispatcher accepts Claude-style hook JSON on stdin and maps `CODEX_TOOL_*` env vars to canonical hook inputs, so `PreToolUse Write` can block non-template stage documents before write. `PostToolUse` replays without a Claude target-file environment still run repository-level template-readiness validation.
- `.agents/**` is legacy compatibility mirror content when present; do not treat it as an independent policy store, and do not restore `.agents/skills/**` as an active skill tree.
- `.agent/**` and `.agent-work/**` are local/generated helper or handoff surfaces only.
- Active `ws` commands must match `bash scripts/ws.sh help`; canonical validation checks the script inventory.
- For AGENTS/CLAUDE/GEMINI drift, apply `agent-md-refactor` and `claude-md-improver` guidance.
