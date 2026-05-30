---
layer: meta
title: "Reference Integrity Protocol"
---

# Reference Integrity Protocol

Use this protocol to detect and fix broken internal references in governance files.

## 1. Scope

Apply to:

- root routers: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
- governance docs: `docs/00.agent-governance/**/*.md`
- human hub docs that route governance: `README.md`, `docs/README.md`

## 2. Required Checks

### 2.1 Broken Markdown Links

```bash
rg -n "\[[^]]+\]\(([^)]+)\)" AGENTS.md CLAUDE.md GEMINI.md README.md docs/README.md docs/00.agent-governance/**/*.md
```

Validate each local path resolves relative to the containing file.

### 2.2 Broken `@` Imports

```bash
rg -n "@[^[:space:])`\"]+" AGENTS.md CLAUDE.md GEMINI.md docs/00.agent-governance/**/*.md
```

Validate each imported path exists.
`python3 scripts/validation/validate-doc-readiness.py` also enforces root/provider
`@` imports in `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/CLAUDE.md`, and
`docs/00.agent-governance/**`.

### 2.3 Non-Existing Hardcoded Paths

```bash
rg -n "@/|docs/[^ )`\"]+\.md" docs/00.agent-governance/**/*.md AGENTS.md CLAUDE.md GEMINI.md README.md docs/README.md
```

Remove absolute machine-specific paths and replace with repository-relative paths.

### 2.4 Language Policy Check for Governance

```bash
rg -n "[\\uAC00-\\uD7A3]" docs/00.agent-governance || true
```

Expected: no matches.

## 3. Fix Rules

- Prefer repository-relative links over absolute filesystem links.
- Avoid links to non-existent example paths.
- Avoid speculative file references; use existing files or explicit patterns.
- Keep root shims minimal; move details to scoped governance files.

## 4. Exit Criteria

Reference integrity is complete only when:

- No broken local links remain in target files.
- No broken `@` imports remain.
- No machine-specific absolute path remains.
- Governance files pass language policy checks.

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
- `scripts/validation/validate-doc-readiness.py`
