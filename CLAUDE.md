# CLAUDE.md

Claude provider overlay. Follow [AGENTS.md](./AGENTS.md) as the workspace contract, then load the Claude-specific runtime below.

@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/claude.md
@.claude/CLAUDE.md
@AGENTS.md

## Claude Notes

- Use `.claude/CLAUDE.md` for local runtime bootstrap, active agents, skills, hooks, and known workspace gotchas.
- Use `.claude/commands/run-preflight.md` for Claude-side preflight checks; it must treat `docs/01.requirements/README.md` as skeleton guidance, not as a PRD anchor.
- Treat `RTK.md` as optional Codex CLI helper guidance; load it only when intentionally using token-filtered local command output.
- Use `bash scripts/ws.sh hook <event> [matcher]` only when manually replaying configured hook events; normal Claude Code hook execution reads `.claude/settings.json` directly. Codex/local replay may pass Claude-style JSON on stdin or `CODEX_TOOL_*` env vars.
- Load Stage 00 rules through `bootstrap.md`; detailed reusable policy stays in `docs/00.agent-governance/**`.
- For derived projects, follow `project-initialization-intake.md` and `template-document-lifecycle.md` before writing or reusing stage documents.
- Use `.github/PULL_REQUEST_TEMPLATE.md` as the PR body for `gh pr create`; fill every section before submitting.
- Keep AGENTS/CLAUDE/GEMINI drift small and intentional. For policy edits, apply `agent-md-refactor` and `claude-md-improver` guidance.
- Validate governed changes with `ws validate` or `bash scripts/ws.sh validate` before commit, push, or PR.
- Optional Graphify generated context is governed by `docs/00.agent-governance/rules/documentation-protocol.md` §11; use it only when current and relevant, and treat source files, Stage 00 governance, templates, and validators as authoritative.
