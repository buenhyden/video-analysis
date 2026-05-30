# Claude Provider Notes (March 2026)

## Scope

This file contains Claude Code-specific guidance only.
Shared repository routing stays in [`CLAUDE.md`](../../../CLAUDE.md), [`AGENTS.md`](../../../AGENTS.md), and the detailed [Claude runtime contract](../../../.claude/CLAUDE.md).

## 1. Memory and Instruction Hierarchy

Claude supports layered instruction sources (broader -> narrower):

- user-level (`~/.claude/CLAUDE.md`)
- project-level (`./CLAUDE.md` routing into `./.claude/CLAUDE.md`)
- subdirectory-level `CLAUDE.md` (loaded on demand)

Use narrower scope files for local behavior and avoid overloading root files.

## 2. AGENTS Bridge Strategy

When repository policy already lives in `AGENTS.md`, keep `CLAUDE.md` minimal and bridge using:

```text
@AGENTS.md
```

Add only Claude-specific deltas below that import.

## 3. Modular Expansion

For larger projects, keep durable policy in `docs/00.agent-governance/**` and keep
`.claude/**` focused on runtime bootstrap, hooks, commands, agents, skills, and
Claude-specific execution details. Do not add `.claude/rules/**` as a new policy
surface unless a future ADR changes the instruction hierarchy.

## 4. Auto Memory Usage

Use auto memory as operational assistance, not as canonical policy.
Authoritative repository policy remains in tracked governance documents.

## 5. Project Intake Gate

In newly derived projects, collect product/software intent and stack details
through `docs/00.agent-governance/rules/project-initialization-intake.md` before
writing PRD, ARD, ADR, spec, plan, task, operations, or reference documents.

## 6. GitHub Boundary

Do not treat `.github/**` as an instruction layer for Claude.
Repository AI instruction authority remains in `AGENTS.md`, `.claude/**`, and `docs/00.agent-governance/**`.

## 7. Hook Runtime

Claude Code consumes `.claude/settings.json` hooks directly. For manual replay or provider-neutral evidence, use `bash scripts/ws.sh hook <event> [matcher]`; do not add `.codex/hooks.json` or GitHub-native instruction files for hook policy.

## 8. Recommended Root Shim Pattern

```text
@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/claude.md
@.claude/CLAUDE.md
@AGENTS.md
```

## 9. References

- Claude memory and CLAUDE.md: <https://code.claude.com/docs/en/memory>
