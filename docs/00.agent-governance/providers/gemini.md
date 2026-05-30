# Gemini Provider Notes (April 2026)

## Scope

This file contains Gemini CLI-specific guidance only.
Shared repository routing stays in [`GEMINI.md`](../../../GEMINI.md) and [`AGENTS.md`](../../../AGENTS.md).

This workspace intentionally does not use a repo-local `.gemini/` directory. Root `GEMINI.md` is the checked-in Gemini entrypoint; add path-scoped Gemini files only after an approved provider-specific runtime need.

## 1. Memory and Instruction Hierarchy

Gemini CLI loads context in this order (broader → narrower):

- global (`~/.gemini/GEMINI.md`)
- root (`./GEMINI.md`) — this file's entry point
- ancestor directories (automatically included if `GEMINI.md` present)
- subdirectory `GEMINI.md` files (loaded on demand via JIT)

## 2. AGENTS Bridge Strategy

When repository policy already lives in `AGENTS.md`, keep `GEMINI.md` minimal:

```text
@AGENTS.md
```

Add only Gemini-specific deltas below that import.

## 3. File Import Syntax

Use `@` prefix for file imports (same as Claude Code):

```text
@docs/00.agent-governance/rules/bootstrap.md
```

For conditional JIT loading, reference files inline within task instructions.

## 4. Context Discovery

Gemini uses `context.fileName` and related settings for instruction discovery.
To inspect active context: run `/memory show` in the Gemini CLI session.
To refresh stale context: run `/memory refresh`.

## 5. Modular Expansion

For path-scoped instructions, place `GEMINI.md` files in subdirectories.
Ancestor `GEMINI.md` context is automatically cascaded to child directories.
Do not create a `.gemini/` directory as an independent policy store.

## 6. Auto Memory Usage

Use `/memory add` for session-specific facts.
Authoritative repository policy remains in tracked governance documents.

## 7. GitHub Boundary

Do not introduce `.github/copilot-instructions.md` or `.github/instructions/**` for repository AI policy.
Gemini-facing repository guidance remains rooted in `GEMINI.md`, `AGENTS.md`, and `docs/00.agent-governance/**`.

## 8. Project Intake Gate

In newly derived projects, collect product/software intent and stack details
through `docs/00.agent-governance/rules/project-initialization-intake.md` before
writing PRD, ARD, ADR, spec, plan, task, operations, or reference documents.

## 9. Hook Runtime

Gemini-facing local agents should use `bash scripts/ws.sh hook <event> [matcher]` when they need to run configured workspace hook events. The hook configuration remains canonical in `.claude/settings.json` and `.claude/hooks/**`.

## 10. Recommended Root Shim Pattern

```text
@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/gemini.md
@AGENTS.md
```

## 11. References

- Gemini CLI context loading: <https://geminicli.com/docs/cli/gemini-md/>
