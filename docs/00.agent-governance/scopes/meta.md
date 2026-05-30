---
layer: meta
title: 'Metadata & Taxonomy Engineering Scope'
---

# Metadata & Taxonomy Engineering Scope

**Rules for repository structure, document frontmatter, and taxonomy enforcement.**

## 1. Context & Objective

- **Goal**: Maintain a highly organized, searchable, and AI-optimized documentation ecosystem.
- **Standards**: Strict adherence to the `01.requirements - 05.operations/incidents` Stage-Gate Taxonomy.
- **Runtime inventory**: Keep `.claude/**` aligned to the active workspace inventory rules.

## 2. Requirements & Constraints

- **Frontmatter**: Every Markdown file MUST include a `layer` attribute in YAML frontmatter.
- **File Naming**: Use `YYYY-MM-DD-<feature-id>.md` for time-sensitive docs (Plans, PRDs).
- **Hierarchy**: No orphans; all files must be linked from a directory README or Central Hub.

## 3. Implementation Flow

1. **Placement**: Determine the correct taxonomy folder (`01.requirements - 05.operations/incidents`) for new documents.
2. **Template**: Use the corresponding template from `docs/99.templates/`.
3. **Linking**: Update the parent README and any related cross-links (e.g., ADR <-> Spec).

## 4. Operational Procedures

- **Validation**: Use repository-governed validation flows only; do not introduce manual formatter or linter steps that conflict with `.pre-commit-config.yaml`.
- **Broken Links**: Periodically scan for and fix dead internal links.

## 5. Maintenance & Safety

- **Pruning**: Archived or outdated docs must be moved to an `archive/` subfolder, not deleted.
- **Refactoring**: Significant changes to folder structure require a `Meta ADR`.
- **Local-Only File Consistency**: `.claude/settings.local.json` is gitignored and personal; never commit it or duplicate team-shared settings from `settings.json` into it. Verify `git ls-files` does not track it.
- **Thin-Root Consistency**: root shim files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) must remain routers only; policy must live in `docs/00.agent-governance/`. Audit periodically for inline policy drift.
- **Stale Path Detection**: after any taxonomy refactor, scan `docs/00.agent-governance/**`, `.claude/**`, and `.github/**` for references to old paths using `rg` before closing the task.
- **Instruction Layer Boundary**: AI instruction hierarchy is owned by `.claude/**` and `docs/00.agent-governance/**`. Do not create `.github/copilot-instructions.md` or `.github/instructions/**` without an ADR.

## File Ownership

- **Allowed Write**: `docs/00.agent-governance/**` · `docs/99.templates/**` · `.claude/**` · `AGENTS.md` · `CLAUDE.md` · `GEMINI.md`
- **Forbidden Write**: implementation paths unless explicitly assigned for governance alignment
- **Pre-condition**: Governance change must be preceded by conflict-check against existing rules.
- **Post-condition**: All `@` imports and internal links validated; lint passes.

## Subagent Definition

- **Trigger**: Governance or template change, rule conflict resolution, or archetype structural update requiring ADR.
- **Context**: isolated — no main-context pollution
- **Reports to**: lead agent only

## Subagent Bridge

**Runtime agent**: `.claude/agents/governance-architect.md`
**Role separation**: This scope is the policy SSOT. The agent file @imports this scope and adds operational runtime behavior only. Do not duplicate policy from this scope into the agent file. If the two conflict, this scope wins.
