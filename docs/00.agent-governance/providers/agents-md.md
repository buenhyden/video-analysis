# AGENTS.md Provider Notes (April 2026)

## Scope

This file defines how `AGENTS.md` must be structured for provider-neutral agent interoperability.
It applies to Claude Code, Gemini CLI, Codex, and any future coding agent platform.

## 1. AGENTS.md as SSOT

`AGENTS.md` is the concise source of truth for workspace-level agent behavior in this repository.
Platform-specific files (`CLAUDE.md`, `GEMINI.md`) are thin overlays that import `AGENTS.md`
and add only platform-specific deltas.

Never duplicate policy from `AGENTS.md` into platform overlays.

## 2. Required Sections

Every root `AGENTS.md` in this repository MUST contain:

| Section              | Purpose                                                                           |
| :------------------- | :-------------------------------------------------------------------------------- |
| Workspace Contract   | Identify this repository as the language-neutral SDLC template.                   |
| Non-Negotiable Rules | Summarize docs, templates, governance, runtime, and design-system constraints.    |
| Operating Flow       | Define analyze, plan, execute, validate, sync workflow.                           |
| Git And CI           | Summarize git-flow, atomic commits, PR-only merge, and workflow safety gates.     |
| Runtime Entrypoints  | Point agents to `.claude/**` and `.codex/**` compatibility metadata.              |
| Required References  | Point agents to onboarding, active plans, governance rules, references, and WIKI. |

## 3. Runtime Agent Catalog

Runtime agent inventory belongs in `.claude/agents/`, `.codex/agents/`, and
`docs/00.agent-governance/rules/harness-library.md`, not in root `AGENTS.md`.
Keep root policy focused on universal behavior and route persona detail to governance files.

Derived projects must complete project initialization intake before any provider
runtime creates stage documents. The intake rule lives in
`docs/00.agent-governance/rules/project-initialization-intake.md`.

Hook policy belongs in `.claude/settings.json`, `.claude/hooks/**`, and Stage 00 governance.
Provider-neutral agents, including Codex, use `bash scripts/ws.sh hook <event> [matcher]`
to execute configured command hooks without adding another repo-local hook policy file.
They may pass Claude-style hook JSON on stdin or `CODEX_TOOL_*` environment variables;
the dispatcher maps those inputs to the canonical hook environment before running
`.claude/hooks/**`.
The hook contract must keep document-readiness gates wired for both Claude and provider-neutral
replay: `PreToolUse` runs `pre-tool-validate.sh` with stage-template write checks,
`PostToolUse` runs `post-tool-validate.sh`, and `Stop` runs `validate-doc-governance.sh`
plus `validate-doc-readiness.py`.

## 4. Thin-Root Contract

`AGENTS.md` must remain navigable at a glance. Policy detail belongs in `docs/00.agent-governance/`.
If a section exceeds 20 lines, extract the detail to a governance file and add a pointer.

## 5. Platform Overlay Pattern

```text
# CLAUDE.md
@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/claude.md
@AGENTS.md
# Claude-specific deltas only below this line
```

```text
# GEMINI.md
@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/gemini.md
@AGENTS.md
# Gemini-specific deltas only below this line
```

## 6. Validation

After any change to `AGENTS.md`:

1. Verify all `@` imports resolve.
2. Verify agent names match between `.claude/agents/*.md` and `.codex/agents/*.toml`.
3. Run `scripts/validation/validate-doc-governance.sh`.
