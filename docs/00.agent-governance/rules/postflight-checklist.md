# Postflight Checklist (April 2026)

Run this checklist after every task closes, before marking a session complete.

## 1. Policy Consistency

- [ ] No new policy duplication introduced between root shims and governance files.
- [ ] All governance additions are in `docs/00.agent-governance/`; root files route only.
- [ ] No Non-Negotiable Rule from `AGENTS.md` was violated during execution.
- [ ] `docs/00.agent-governance/memory/progress.md` records final task status, blockers, next sync, and durable run notes.
- [ ] Policy changes are recorded in `docs/00.agent-governance/policy-change-log.md`, not only in memory.
- [ ] `ws intelligence` was run if structural changes were made; `repo_map.json` is updated.
- [ ] If a Swarm mission was active: `ws swarm <task_id> handoff <next_role>` was called to close the stage.

## 2. Language Policy

- [ ] All files written to `docs/00.agent-governance/` are in English.
- [ ] All user-facing communication delivered in Korean.
- [ ] No Korean text in governance markdown files.

## 3. Docs 3 Global Rules Compliance

- [ ] **R1**: Every new or modified stage document was created from the matching `docs/99.templates/` contract. Required template-specific sections remain present, no `[placeholder]` text remains, and `status: draft` is set for new documents.
- [ ] **R2**: Every modified `docs/` folder has an updated `README.md`.
- [ ] **R3**: Every new stage document includes a `## Related Documents` section with relative upstream links.

## 4. Reference Integrity

- [ ] Run `scripts/validation/validate-cross-links.sh` — zero broken links.
- [ ] All `@` imports in root shims resolve to existing files.
- [ ] All `.claude/agents/*.md` role names remain synchronized with `docs/00.agent-governance/rules/harness-library.md` and `docs/00.agent-governance/rules/persona.md`.

## 5. Lint Check

- [ ] No manual formatter was run (prettier / eslint / markdownlint / ruff).
- [ ] Pre-commit hook is intact (`.pre-commit-config.yaml` unchanged unless task explicitly targeted it).
- [ ] Hook failures recorded in completion summary only; not auto-fixed outside declared scope.

## 6. Scope Boundary Verification

- [ ] No writes occurred outside the active persona's declared Allowed Write paths.
- [ ] If parallel subagents were used: no file ownership overlap occurred.
- [ ] `docs/99.templates/` was not edited except by `meta` / Governance Architect persona.
- [ ] `_workspace/**` was used only for transient coordination, generated diagnostics, generated intelligence, or scratch output.

## 7. Completion Report

Emit a completion report in the format defined in `AGENTS.md` or the system directive before closing.

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
