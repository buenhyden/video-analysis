# AI Agent Standards (May 2026)

Repository-wide standards for root routers, context loading, and policy consistency.

## 1. Balanced Router Standard

- `AGENTS.md` is the concise workspace contract for all AI agents.
- `CLAUDE.md` and `GEMINI.md` are provider overlays, not policy warehouses.
- Root/provider files may summarize universal constraints, but detailed behavior belongs in `docs/00.agent-governance/*`.
- Provider overlays must contain only:
  - bootstrap route
  - provider route
  - repository identity import
  - provider-specific operational notes
- Keep detailed behavior in `docs/00.agent-governance/*`.

## 2. Lazy Loading Standard

- Load minimum required governance first (`bootstrap -> preflight -> persona -> scope`).
- Load provider notes only in provider-specific runtimes.
- Do not duplicate identical instructions across root/provider/rules files.

## 2.1 Active Runtime Inventory (Workspace-Only)

Maintain `.claude/**`, `.codex/**`, and `docs/00.agent-governance/**` so they reflect **only**
what is used in the current workspace. Treat an agent/skill as **active** if it is:

1. Present in `.claude/agents/*.md` or `.claude/skills/*/skill.md`, and
2. Referenced by runtime docs, hooks, commands, or governance inventory.

Remove legacy catalog references (for example external harness labels) that are not used by the
current workspace. Do not introduce new external taxonomy references.

`.codex/agents/*.toml` must stay synchronized with `.claude/agents/*.md` by name and role intent.
Do not add Codex-only policy that is absent from `.claude/**` or `docs/00.agent-governance/**`.
`.agents/**`, when present, is a legacy compatibility mirror only and must not contain active skill
inventory that diverges from `.claude/skills/**`. `.agent/**` is optional generated/local helper
guidance and cannot override Stage 00 policy.

Local tooling assumptions are not runtime inventory. Classify them through
`environment-readiness.md`: core governance tools are prerequisites for reliable local validation,
while review, docs/lint, security, and derived-stack tools are optional or conditional unless the
task or intake declares them required.

## 2.2 Model Policy (Claude Agents)

- Use `model: opus` for supervising, managing, and review authority roles:
  - `governance-architect`
  - `product-manager`
  - `system-architect`
  - `infra-devops`
  - `ops-manager`
  - `sre-ops`
  - `code-reviewer`
  - `risk-manager`
- Use `model: sonnet` for regular worker and specialist roles:
  - `backend-engineer`
  - `frontend-engineer`
  - `qa-inspector`
  - `security-engineer`
  - `researcher`
  - `technical-writer`
  - `docs-governance`
  - `git-commit`
  - `wiki-curator`
- Preserve this exact split unless an ADR changes the runtime model hierarchy.

## 2.3 Skill Layout Policy

- Active top-level skills must use directory form: `.claude/skills/<name>/skill.md`.
- Do not reintroduce flat top-level skill files for active runtime skills.
- Existing directory-based governance skills remain valid and should stay in directory form.

## 3. Cross-Provider Guidance (2026-03)

### 3.1 OpenAI Codex / AGENTS

- Support nested instruction discovery with nearest-file precedence.
- Consider fallback instruction filenames when configured:
  - `AGENTS.override.md`, `AGENTS.md`, `TEAM_GUIDE.md`, `.agents.md`.
- Respect instruction size controls (`project_doc_max_bytes`, default 32 KiB in Codex docs).
- Use `~/.codex/AGENTS.md` for global defaults when needed.
- In this repository, `.codex/agents/*.toml` is a compatibility view of `.claude/agents/*.md`.

### 3.2 Claude Code / CLAUDE

- Use `@AGENTS.md` bridge to avoid duplicate guidance across tools.
- Keep `CLAUDE.md` concise and route detail into scoped files.
- Keep durable policy in `docs/00.agent-governance/**`; `.claude/**` is for runtime bootstrap, hooks, commands, agents, skills, and Claude-specific execution details.
- Do not add `.claude/rules/**` as a new policy surface unless a future ADR changes the instruction hierarchy.
- Use auto memory as supplemental context, not as policy replacement.

### 3.3 Gemini CLI / GEMINI

- Maintain hierarchical context strategy (global -> root/ancestors -> subdirectories).
- Use `/memory` commands to inspect and refresh effective context.
- Use `@` imports for modularization.
- Use `context.fileName` and related `context.*` settings for instruction discovery tuning.

## 4. Documentation and Traceability

- All execution rules must point to canonical compact docs outputs (`docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, and `docs/99.templates`).
- On `main`, project-content outputs remain README skeleton guides until a derived-project intake creates actual documents.
- Use `stage-gate-matrix.md` for stage ownership, templates, and completion criteria.
- Use `reference-integrity.md` for link/import checks.

## 4.1 Path Portability Standard

- Keep new generated document paths short enough for common Windows and deep-clone environments.
- Warning budgets:
  - relative repository path: 140 characters
  - current absolute workspace path: 220 characters
  - single path segment: 80 characters
- Use lowercase, kebab-case slugs for generated Markdown documents.
- Do not use spaces or Windows-reserved characters in reusable template paths: `<`, `>`, `:`, `"`, `|`, `?`, `*`.
- `python3 scripts/validation/validate-path-portability.py` is warning-only. Treat warnings as rename prompts for new files, not as a reason to rewrite reviewed maintenance history.

## 5. GitHub-Native Instruction Policy

- Do not introduce GitHub-native AI instruction files into `.github/`.
- Prohibited paths include:
  - `.github/copilot-instructions.md`
  - `.github/instructions/**`
- Repository AI instruction ownership stays split between:
  - `.claude/**` for runtime hooks, commands, and agent files
  - `.codex/**` for synchronized Codex compatibility metadata
  - `docs/00.agent-governance/**` for canonical governance rules
- Any exception requires an ADR because it changes the repository instruction hierarchy.

## 6. Sources

- OpenAI Codex AGENTS: <https://developers.openai.com/codex/guides/agents-md>
- Anthropic Claude memory/CLAUDE: <https://code.claude.com/docs/en/memory>
- Gemini CLI GEMINI.md: <https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html>
- Gemini CLI configuration: <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html>
- AGENTS.md open format: <https://agents.md/>

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
