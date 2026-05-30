# Active Harness Governance Rule

> Policy SSOT for the migrated harness inventory used by this workspace.
> Architecture anchor: `docs/03.specs/README.md`; feature-level specs live under `docs/03.specs/<feature-id>/`.

## 1. Purpose

This workspace keeps only the migrated harness inventory that is active in the current runtime.
The inventory is implemented through flat governance agents in `.claude/agents/` and directory
skills in `.claude/skills/`. `.codex/agents/*.toml` is a synchronized Codex compatibility
view of the active agent inventory and copied instruction text, not a separate policy source.
Canonical hook implementations live in `.claude/hooks/**` and are wired by `.claude/settings.json`.
Other local agent runtimes, including Codex, must use `bash scripts/ws.sh hook <event> [matcher]`
to execute configured hook events instead of creating a separate hook policy file.
Local prerequisite classes for this harness are governed by `environment-readiness.md`;
missing optional or stack-conditional tools must not be treated as harness drift unless the
active task or derived-project intake requires them.

Do not reconstruct or reference inactive example inventory in governance outputs.

The harness exists to make AI Agent-first Engineering executable: agents must be discoverable,
stage-scoped, validation-aware, and synchronized with the canonical governance rules before they
are treated as active runtime assets.
The `main` release branch keeps project-content folders as README skeletons only.
Runtime and harness policy therefore lives in Stage 00, not in Stage 90 reference
artifacts.

## 2. Locked Active Mapping

| Harness ID       | Source Capability                                  | Active Runtime Target                                                       |
| ---------------- | -------------------------------------------------- | --------------------------------------------------------------------------- |
| `16`             | fullstack-webapp                                   | `backend-engineer.md`, `frontend-engineer.md`, `fullstack-webapp/skill.md`  |
| `20`             | cicd-pipeline                                      | `infra-devops.md`, `cicd-pipeline/skill.md`                                 |
| `21`             | code-reviewer                                      | `code-reviewer.md`, `code-review/skill.md`                                  |
| `23`             | microservice-designer                              | `system-architect.md`, `microservice-designer/skill.md`                     |
| `24`             | test-automation                                    | `qa-inspector.md`, `test-automation/skill.md`                               |
| `25`, `83`, `92` | incident-postmortem, sop-writer, operations-manual | `ops-manager.md`, `sre-ops.md`, `ops-sop/skill.md`                          |
| `28`             | security-audit                                     | `security-engineer.md`, `security-audit/skill.md`                           |
| `29`             | performance-optimizer                              | `code-reviewer.md`, `system-architect.md`, `performance-optimizer/skill.md` |
| `46`             | product-manager                                    | `product-manager.md`, `pm-pipeline/skill.md`                                |
| `63`             | research-assistant                                 | `researcher.md`, `research-brief/skill.md`                                  |
| `81`             | technical-writer                                   | `technical-writer.md`, `doc-pipeline/skill.md`, `template-patch/skill.md`   |
| `88`             | risk-register                                      | `risk-manager.md`, `risk-report/skill.md`                                   |
| `94`             | audit-report                                       | `governance-audit/skill.md`                                                 |
| `—`              | spec-driven-sdlc                                   | `spec-driven-sdlc/skill.md`                                                 |
| `—`              | stage-gate-review                                  | `stage-gate-review/skill.md`                                                |
| `—`              | doc-governance                                     | `docs-governance.md`, `doc-governance/skill.md`                             |
| `—`              | workspace-governance                               | `governance-architect.md`, `workspace-governance/skill.md`                  |
| `—`              | git-commit-runtime                                 | `git-commit.md`                                                             |
| `—`              | llm-wiki-curation                                  | `wiki-curator.md`                                                           |

## 3. Runtime Rules

- `AGENTS.md`, `.claude/agents/`, `.codex/agents/`, and this rule must describe the same active inventory.
- Active agents live in `.claude/agents/*.md`.
- Codex compatibility agent metadata lives in `.codex/agents/*.toml` and must stay name-parity and description aligned with `.claude/agents/*.md`; copied instruction text can exist there for Codex consumption, but policy authority remains `.claude/**` and Stage 00 governance.
- `.codex/**` must not contain Codex-only policy surfaces outside the synchronized compatibility metadata. In particular, do not create `.codex/hooks.json` or `.codex/hooks/**`; provider-neutral hook replay goes through `bash scripts/ws.sh hook <event> [matcher]`.
- `.agents/**`, when tracked, is a legacy compatibility mirror allowlisted to `.agents/README.md`, `.agents/rules/graphify.md`, and `.agents/workflows/graphify.md`. It must point to `.claude/**` and `.codex/**` concepts and must not introduce legacy uppercase Codex paths, active skills, hooks, or independent policy. Do not restore `.agents/skills/**` as an active skill tree.
- `.agent/**` is local/generated helper guidance only. It can describe optional Graphify workflows, but it must not override Stage 00 governance or release-template skeleton policy.
- `.agent-work/**` is local handoff state and is not part of the reusable template contract.
- Configured hook events live in `.claude/settings.json`; provider-neutral execution for Codex and other local agents uses `bash scripts/ws.sh hook <event> [matcher]`. The dispatcher accepts Claude-style hook JSON on stdin and maps `CODEX_TOOL_*` environment variables into canonical hook inputs before running `.claude/hooks/**`. Runtime contract shape, dispatcher portability, required document-readiness hook commands, runtime policy-surface deny rules, and workflow safety deny rules are validated by `python3 scripts/validation/validate-runtime-contracts.py` plus focused hook replay.
- Active top-level skills live in `.claude/skills/<name>/skill.md`.
- Active top-level skills must match the skill inventory registered in this rule; `bash scripts/validation/validate-skill-quality.sh` fails on missing or unregistered active skills.
- Existing directory skills that support governance orchestration remain valid runtime assets.
- Governance files must not refer to removed source directories.
- Runtime commands must create transient coordination state only under ignored `_workspace/**` paths unless a governed document is explicitly being authored from a template. Tracked methodology, progress, and durable memory belong in `docs/00.agent-governance/memory/`.
- Persona definition overlays live in `.claude/personas/*.md`; they provide behavioral constraint definitions (Hard Stop rules, role responsibilities) as supplementary runtime assets, distinct from agent dispatcher files in `.claude/agents/`.
- Active persona files are recognized runtime assets and fall under Governance Architect ownership; changes to `.claude/personas/*.md` require updating `docs/00.agent-governance/rules/persona.md` and this rule.
- Persona overlay files do not require Codex compatibility entries in `.codex/agents/`; they are Claude Code runtime overlays, not standalone agent dispatchers.
- Agent files may reference persona overlays conceptually; explicit `@`-import integration is optional and governed by the agent's own instruction file.

## 4. Hook Inventory

Active hooks are wired in `.claude/settings.json` and executed by Claude Code automatically.
Codex and other local agents run the same events via `bash scripts/ws.sh hook <event> [matcher]`.
For pending writes, pass `tool_input.file_path` plus `tool_input.content`/`new_text` as JSON on stdin or set `CODEX_TOOL_INPUT_FILE_PATH` and `CODEX_TOOL_INPUT_CONTENT`.
When provider-neutral `PostToolUse` replay lacks a Claude target-file environment variable, `post-tool-validate.sh` must run repository-level document readiness validation instead of skipping the gate.

| File                     | Event              | Matcher                        | Enforcement Purpose                                                                                                               |
| :----------------------- | :----------------- | :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| `session-start.sh`       | SessionStart       | `*`                            | Injects workspace context: branch, changed files, governance health summary                                                       |
| `git-policy-enforce.sh`  | PreToolUse         | `Bash`                         | Blocks direct pushes to `main`/`dev`; enforces branch naming and Conventional Commits                                             |
| `pre-tool-validate.sh`   | PreToolUse         | `Read\|Write\|Edit\|MultiEdit` | Blocks sensitive files, forbidden runtime policy surfaces, unsafe workflow patterns, and pending stage-document writes that miss required `docs/99.templates` contracts |
| `docs-readme-sync.sh`    | PostToolUse        | `Write\|Edit\|MultiEdit`       | Auto-syncs `docs/` folder README indexes after file edits                                                                         |
| `post-tool-format.sh`    | PostToolUse        | `Write\|Edit\|MultiEdit`       | Applies safe whitespace normalization and optional local formatters after file edits                                                |
| `post-tool-validate.sh`  | PostToolUse        | `Write\|Edit\|MultiEdit`       | Validates governance, template-readiness, and workflow files immediately after each write                                           |
| `error-logger.sh`        | PostToolUseFailure | `*`                            | Logs tool failures (non-blocking) to `_workspace/diagnostics/hook-errors.log`                                                     |
| `pre-compact-context.sh` | PreCompact         | `*`                            | Saves branch/changes/active-task snapshot to `_workspace/diagnostics/pre-compact-context.txt` before context compaction           |
| `pr-template-enforce.sh` | —                  | —                              | Backward-compatibility alias for `git-policy-enforce.sh`; used via `ws hook` for Codex; not wired as a separate Claude Code event |

Stop event runs `scripts/validation/validate-doc-governance.sh` and `scripts/validation/validate-doc-readiness.py` directly (not a `.claude/hooks/` file).
Stop event also runs `stop-completion-governance.sh` to block silent completion when agent-owned changes remain uncommitted.
The PreToolUse file-safety hook calls `scripts/validation/validate-stage-template-write.py`
when pending write content is available.

Uncovered events (no hook wired): `UserPromptSubmit` (handled at user-global level), `PermissionRequest` (handled by settings.json deny list), `SessionEnd` (Stop covers final validation), `SubagentStop` (only needed with swarm — lazy-load trigger).

Lifecycle rule: adding or removing a hook requires updating `.claude/settings.json`, this table, and `docs/LLM-WIKI.md §Hook Runtime`.
Hook contract changes also require `python3 scripts/validation/validate-runtime-contracts.py` and `bash scripts/ws.sh validate`.

## 5. Lazy-Load Rule Files

The following rule files exist in `docs/00.agent-governance/rules/` but are **intentionally excluded**
from the `bootstrap.md` Required Rule Files list. They are loaded only when the specific workflow
that requires them is active. Do not add them to the bootstrap required list unless the workspace
adopts always-on swarm or evolution workflows.

| File                    | Load Trigger                                                                                                       |
| :---------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `evolution-protocol.md` | Loaded when a governance evolution proposal is under review or a template evolution workflow starts.               |
| `release-process.md`    | Loaded when preparing, reviewing, or validating a `dev` to `main` release-template PR.                             |
| `swarm-protocol.md`     | Loaded when `ws swarm <task_id> <command>` is used or a multi-agent sequential handoff is explicitly orchestrated. |

This lazy-load pattern keeps session context lean. Agents must not bulk-load these files during
standard bootstrap unless the active task explicitly requires swarm or evolution workflows.

## 6. Harness Lifecycle

Use this lifecycle for any active agent or skill addition, modification, or removal.

| Change Type           | Required Updates                                                                                                                                                        |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Add agent             | `.claude/agents/<name>.md`, `.codex/agents/<name>.toml`, `persona.md`, this rule, Stage 00 README, `docs/LLM-WIKI.md`, `validate-skill-quality.sh` model/scope coverage |
| Modify agent intent   | `.claude/agents/<name>.md`, matching `.codex/agents/<name>.toml`, owner rule or scope file when policy changes                                                          |
| Remove agent          | Delete `.claude` and `.codex` entries together, remove persona mapping, update this rule, run parity validation                                                         |
| Add skill             | `.claude/skills/<name>/skill.md`, this rule, Stage 00 README or LLM-WIKI when exposed to agents, validator coverage when it becomes a required gate                     |
| Modify skill contract | Skill file, owning rule, and any stage-gate matrix or README entry that advertises the behavior                                                                         |
| Remove skill          | Remove references before deleting the skill directory; record an ADR if orchestration behavior changes                                                                  |

Every lifecycle change must keep root/provider routers thin. Durable policy belongs in
`docs/00.agent-governance/**`, while `.claude/**` holds runtime bootstrap and `.codex/**`
holds compatibility metadata.

## 7. Ownership

| Path                                                                    | Owner                                   | Rule                                                     |
| ----------------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------- |
| `.claude/agents/`                                                       | Governance Architect                    | Runtime bridge files only                                |
| `.codex/agents/`                                                        | Governance Architect                    | Codex compatibility metadata only                        |
| `.codex/hooks*`                                                         | No owner                                | Forbidden provider-specific hook policy surface          |
| `.claude/skills/`                                                       | Governance Architect                    | Orchestration and audit skills only                      |
| `.agents/skills/`                                                       | No owner                                | Forbidden legacy skill tree                              |
| `docs/00.agent-governance/`                                             | Governance Architect                    | Canonical governance policy                              |
| `docs/03.specs/`                                                        | System Architect + Governance Architect | Architecture anchor for active runtime                   |
| `docs/LLM-WIKI.md`                                                       | Wiki Curator                            | Canonical AI operating summary freshness                 |

## 8. Change Control

Only the Governance Architect may expand or reduce the active inventory. Any structural change must:

1. update this rule
2. update `AGENTS.md`
3. update `.claude/agents/` and `.codex/agents/` together
4. update the architecture anchor docs when the change creates project-specific architecture content; otherwise keep release-template skeleton folders README-only
5. record an ADR if the instruction hierarchy or runtime structure changes
6. update `docs/LLM-WIKI.md`, Stage 00 README, and relevant validators before closing
7. capture Stage 05/06 evidence for non-trivial governance changes

## 9. References

- `AGENTS.md`
- `docs/00.agent-governance/rules/environment-readiness.md`
- `docs/03.specs/README.md`
- `docs/00.agent-governance/rules/subagent-protocol.md`
- `docs/00.agent-governance/rules/agentic.md`

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
