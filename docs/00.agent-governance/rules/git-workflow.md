# Git Workflow Governance (May 2026)

> This document defines the mandatory Git and PR strategy for all agents in the `video-analysis` workspace.

## Role definition

All AI agents and human contributors MUST adhere to the `git-flow` strategy and Conventional Commits. The goal is to maintain a high-quality, traceable, and revertible history where every change is accounted for.

## Procedure

1. **Branching**:
   - **Feature/Fix/Docs**: Branch from `dev`. Naming: `<type>/<ticket-or-domain>-<slug>` (e.g., `feat/PROJ-123-add-auth`).
   - **Hotfix** (production bug): Branch from `main`. Naming: `hotfix/<slug>`. After fix: (1) open PR targeting `main` and merge it first; (2) only after the `main` PR is merged, open a second PR targeting `dev` and merge it. Do not open the `dev` PR before the `main` PR is merged.
   - Never branch directly from another feature branch.
2. **Commit**:
   - **1 Commit = 1 Logical Change**: Do not bundle unrelated features, fixes, or refactors.
   - **Conventional Commits**: Format MUST be `<type>(<scope>): <summary>`.
   - **Allowed Types**: `feat`, `fix`, `docs`, `refactor`, `style`, `perf`, `test`, `build`, `ci`, `chore`, `deps`, `revert`.
   - **Work Type Mapping**: Use `feat` for new user-visible capability, `fix` for behavior correction, `refactor` for behavior-preserving restructuring, `docs` for documentation-only changes, `test` for tests or evaluation evidence, `ci` for workflow/gate changes, and `chore` for maintenance with no user-facing behavior change.
   - **Issue Linking**: Reference issue IDs when known or available (e.g., `#123`).
   - **WIP Checkpoints**: Incomplete but valuable work must record WIP state in `docs/04.execution/tasks/`, `docs/00.agent-governance/memory/progress.md`, or the PR description before handoff. Do not create WIP commits unless explicitly requested; do not merge WIP work until it is converted to a reviewable conventional change.
3. **Pull Request**:
   - Push branch to origin.
   - Create a PR targeting `dev`.
   - **PR Template**: Always use `.github/PULL_REQUEST_TEMPLATE.md` as the PR body template. Fill every section; do not submit with placeholder text.
   - Use `gh pr create --base dev --body "$(cat .github/PULL_REQUEST_TEMPLATE.md)"` as the starting point, then fill in the content.
   - Ensure all CI/validation checks pass.
4. **Merge**:
   - Merge via PR only; direct push to `main` or `dev` is prohibited.
   - **Merge strategy**: Squash merge for feature/fix/docs branches (keeps integration branch history clean). Merge commit for `hotfix/*` (preserves commit identity on both `main` and `dev`).
   - Delete the feature branch after merge.

## Constraints

- **Atomicity**: Every commit must leave the repository in a working (green) state.
- **Mood**: Use the imperative mood in commit summaries ("add", "fix", not "added", "fixed").
- **Length**: Limit subject line to 72 characters.
- **HARD STOP**: HALT if an agent attempts to push directly to protected branches, force-push, delete protected branches, or bypass local hooks with `--no-verify`.
- **HARD STOP**: HALT if `gh pr create` is called without `.github/PULL_REQUEST_TEMPLATE.md` as the PR body. Every section of the template must be filled before submission. Git and PR policy are enforced by `PreToolUse` hook `.claude/hooks/git-policy-enforce.sh`.

## File references

- [AGENTS.md](../../../AGENTS.md) - Root Governance Router
- [LLM-WIKI.md](../../LLM-WIKI.md) - SDLC Reference
- [documentation-protocol.md](./documentation-protocol.md) - Documentation Standards
