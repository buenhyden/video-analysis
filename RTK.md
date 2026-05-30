# RTK - Rust Token Killer (Codex CLI)

**Usage**: Optional token-optimized CLI proxy for local Codex shell commands.

## Scope

RTK is optional local Codex CLI tooling. It is not a universal workspace shell policy.

Use normal shell commands when following repository docs, running `bash scripts/ws.sh ...`, running tests, using Git, or when RTK is unavailable.

Use `rtk <command>` only when you intentionally want token-filtered output and the command does not require exact raw output.

## Examples

Examples:

```bash
rtk git status
rtk cargo test
rtk npm run build
rtk pytest -q
```

Use `rtk proxy <cmd>` when you need raw command output through RTK.

## Meta Commands

```bash
rtk gain            # Token savings analytics
rtk gain --history  # Recent command savings history
rtk proxy <cmd>     # Run raw command without filtering
```

## Verification

```bash
rtk --version
rtk gain
which rtk
```
