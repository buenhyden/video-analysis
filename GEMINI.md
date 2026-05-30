# GEMINI.md

Gemini provider overlay. Follow [AGENTS.md](./AGENTS.md) as the workspace contract, then load the Gemini-specific governance note.

@docs/00.agent-governance/rules/bootstrap.md
@docs/00.agent-governance/providers/gemini.md
@AGENTS.md

## Gemini Notes

- Keep this file as a provider router. Detailed Git, CI, documentation, and runtime policy belongs in `AGENTS.md`, `.claude/**`, and `docs/00.agent-governance/**`.
- This workspace intentionally uses root `GEMINI.md` as the Gemini entrypoint. Do not add a `.gemini/` policy directory unless a future provider-specific runtime need is approved.
- Load Stage 00 rules through `bootstrap.md`; detailed template, lifecycle, git, CI, and harness policy stays in Stage 00 governance.
- Run configured local hook events through `bash scripts/ws.sh hook <event> [matcher]`; do not add `.gemini/**` or `.codex/hooks*` policy surfaces.
- Use `docs/99.templates/` before creating stage documents and root `DESIGN.md` before frontend, mobile, or app UI work.
- Validate governed changes with `ws validate` or `bash scripts/ws.sh validate` before completion.
