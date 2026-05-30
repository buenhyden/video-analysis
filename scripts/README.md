# Scripts & Utilities

> Active minimal-governance automation, validation gates, and repository utilities.

## Overview

`scripts/` is the active automation surface for this language-agnostic project template. Keep scripts reusable for governance, documentation, CI validation, security checks, and optional repository intelligence. Stack-specific starters and cloud/deployment experiments belong under `examples/`, not active `scripts/`.

## Audience

This index is for humans and agents that need to run, validate, or update repository automation without guessing which scripts are active.

## Scope

### In Scope

- Active `ws` commands and the scripts they invoke.
- Direct helper commands that have explicit documentation and validation coverage.
- CI-only scripts used by active GitHub workflows.
- Script inventory rules enforced by `python3 scripts/validation/validate-script-inventory.py`.

### Out of Scope

- Application-stack scaffolding for derived projects.
- Unowned compatibility wrappers or speculative automation.
- Tool installation or environment mutation from setup commands.

## Structure

| Area          | Contents                                                               |
| :------------ | :--------------------------------------------------------------------- |
| `ws.sh`       | Canonical workspace command entry point.                               |
| `setup/`      | Template bootstrap and non-mutating local prerequisite status checks.  |
| `validation/` | Governance, docs, metadata, runtime, and conditional stack validation. |
| `ci/`         | CI-only context and security gate helpers.                             |
| `docs/`       | Documentation build and README index sync.                             |
| `harness/`    | Agent hook dispatch, subagent handoff, swarm, and self-heal helpers.   |
| `generation/` | Repository intelligence and SBOM generation helpers.                   |
| `qa/`         | Spec-test scaffolding and TDD evidence helpers.                        |

## Usage

```bash
bash scripts/ws.sh help
bash scripts/ws.sh validate
```

## Active Workspace Commands

`scripts/ws.sh` exposes only these active commands:

| Command            | Purpose                                                                        |
| :----------------- | :----------------------------------------------------------------------------- |
| `setup`            | Report core, optional, and stack-conditional local prerequisites without installing tools. |
| `validate`         | Run governance, script inventory, structure, dependency, and container checks. |
| `validate-derived` | Run the full gate plus derived-project placeholder validation after bootstrap. |
| `validate-distribution` | Verify the `main` release-template skeleton contains only allowed README guides. |
| `audit`            | Run dependency and container audits when stack manifests exist.                |
| `heal`             | Report local governance workspace consistency without modifying files.         |
| `info`             | Show repository, branch, architecture, security, and governance summary.       |
| `docs`             | Build or serve documentation.                                                  |
| `hook`             | Run the canonical agent hook dispatcher for a configured event and matcher.    |
| `sbom`             | Generate a minimal SBOM.                                                       |
| `intelligence`     | Generate repository intelligence artifacts.                                    |
| `dispatch`         | Create an ignored transient subagent dispatch packet.                          |
| `swarm`            | Run the governed swarm handoff helper with canonical task-first syntax.        |
| `bootstrap`        | Personalize the template for a new project.                                    |
| `help`             | Show the command list.                                                         |

## Script Inventory

The `Status` column and retention basis markers are validated by
`validation/validate-script-inventory.py`. Inventory presence means a script is owned and
wired; it does not by itself prove the script is always active in the base
template.

- `active-ws`: retained by **Basis: ws consumer** because it is wired through `scripts/ws.sh`.
- `active-ci`: retained by **Basis: CI consumer** because it is invoked by active GitHub workflows outside `ws validate`.
- `active-direct`: retained by **Basis: documented direct governance use** because humans or agents intentionally invoke a documented direct command.
- `reserved-direct`: retained by **Basis: reserved direct use** only when a local hook or future direct-use condition has an explicit owner and validation path.
- `optional-example`: retained outside active `scripts/` and must not be required by active workflows or `ws.sh`.
- **Basis: derived-project conditional value** marks scripts that may skip cleanly in this base template but become active after a derived project adds docs, dependency, container, or stack manifests.

Current audit result: there are no unowned or unwired tracked `.sh` / `.py`
files in `scripts/`. Conditional no-op behavior is accepted template-readiness
overhead, not a deletion signal.

| Status        | Script                              | Purpose                                                                                                                                                                                                                   |
| :------------ | :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| active-ws     | `harness/agent-hook-dispatch.py`            | Basis: ws consumer. Dispatch canonical `.claude/settings.json` command hooks by event for Claude, Codex, and other local agent runtimes without adding another hook policy surface; maps portable hook JSON and `CODEX_TOOL_*` env vars into canonical hook inputs. |
| active-ws     | `validation/audit-dependencies.sh`             | Basis: ws consumer; derived-project conditional value. Audit active dependency manifests when present via `ws validate` and `ws audit`.                                                                                   |
| active-ws     | `setup/bootstrap-project.sh`              | Basis: ws consumer. Personalize a new project from the template via `ws bootstrap`, including optional GitHub metadata replacement.                                                                                       |
| active-ws     | `docs/build-docs.sh`                     | Basis: ws consumer; derived-project conditional value. Build or serve documentation via `ws docs` when MkDocs is configured; otherwise exit cleanly.                                                                      |
| active-ci     | `ci/collect-context.sh`                | Basis: CI consumer. Collect failure diagnostics for GitHub workflow diagnostics.                                                                                                                                          |
| active-ws     | `harness/dispatch-subagent.sh`              | Basis: ws consumer. Create ignored transient subagent dispatch packets via `ws dispatch`.                                                                                                                                 |
| active-ws     | `generation/generate-repo-intelligence.py`     | Basis: ws consumer. Generate repository intelligence artifacts via `ws intelligence`.                                                                                                                                     |
| active-ws     | `generation/generate-sbom.sh`                  | Basis: ws consumer; derived-project conditional value. Generate a minimal SBOM via `ws sbom`.                                                                                                                             |
| active-direct | `qa/scaffold-tests-from-spec.sh`       | Basis: documented direct governance use. Direct command for generating sibling `tests.md` from `docs/03.specs/<feature-id>/spec.md`.                                                                                      |
| active-ws     | `harness/self-heal.sh`                      | Basis: ws consumer. Report local governance workspace consistency via `ws heal` without modifying files.                                                                                                                  |
| active-ws     | `setup/setup-environment.sh`              | Basis: ws consumer; derived-project conditional value. Report core governance runtime, review/publishing, docs/lint, security, and stack-conditional prerequisite status without installing tools via `ws setup`.                                                                                                |
| active-ws     | `qa/summarize-tdd-coverage.sh`         | Basis: ws consumer; documented direct governance use. Summarize Stage 06 implementation task TDD evidence through `ws validate` and as a scoped direct command.                                                          |
| active-ws     | `harness/swarm-dispatch.sh`                 | Basis: ws consumer. Run governed swarm helper commands via `ws swarm <task_id> <command>`.                                                                                                                                |
| active-direct | `docs/update-doc-readme-index.sh`        | Basis: documented direct governance use. Direct command for refreshing docs-relative README indexes after doc inventory changes.                                                                                          |
| active-ws     | `validation/validate-architecture.sh`          | Basis: ws consumer. Validate architecture/governance constraints via `ws validate`.                                                                                                                                       |
| active-ws     | `validation/validate-code-style.sh`            | Basis: ws consumer; documented direct governance use. Validate whitespace, line endings, and configured style hooks through `ws validate` without introducing a default application stack.                                |
| active-direct | `validation/validate-commit-msg.sh`            | Basis: documented direct governance use. Direct command for validating a commit message file against repository Conventional Commit policy.                                                                               |
| active-ws     | `validation/validate-containers.sh`            | Basis: ws consumer; derived-project conditional value. Audit active container files when present via `ws validate` and `ws audit`.                                                                                        |
| active-ws     | `validation/validate-cross-links.sh`           | Basis: ws consumer. Validate internal Markdown links via `ws validate`.                                                                                                                                                   |
| active-direct | `validation/validate-design-initialization.sh` | Basis: documented direct governance use. Direct command for enforcing root `DESIGN.md` initialization before UI work.                                                                                                     |
| active-ws     | `validation/validate-doc-governance.sh`        | Basis: ws consumer. Validate docs governance, root/provider shim thresholds, and stage indexes via `ws validate`.                                                                                                         |
| active-ws     | `validation/validate-docs.sh`                  | Basis: ws consumer. Validate docs frontmatter and optional linting via `ws validate`.                                                                                                                                     |
| active-direct | `validation/validate-doc-readiness.py`         | Basis: documented direct governance use. Direct helper invoked by `validation/validate-docs.sh` for frontmatter, README contract, stage-specific template contract, index, active-surface stale-reference, Codex surface, and Stage 90 runtime count-freshness checks. |
| active-direct | `validation/validate-stage-template-write.py`  | Basis: documented direct governance use. Direct helper invoked by `.claude/hooks/pre-tool-validate.sh` to block pending stage-document writes that do not satisfy their `docs/99.templates` contract.                    |
| active-ws     | `validation/validate-folders.sh`               | Basis: ws consumer. Validate allowed docs folder structure via `ws validate`.                                                                                                                                             |
| active-ws     | `validation/validate-github-metadata.py`       | Basis: ws consumer. Validate non-workflow GitHub metadata for template drift via `ws validate`; use `--strict-derived` after bootstrap.                                                                                   |
| active-ws     | `validation/validate-github-workflows.py`      | Basis: ws consumer. Validate GitHub Actions governance rules via `ws validate`.                                                                                                                                           |
| active-ws     | `validation/validate-path-portability.py`      | Basis: ws consumer; documented direct governance use. Warn when repository paths exceed portability budgets or use Windows-hostile naming; warnings are advisory in the base template.                                      |
| active-ws     | `validation/validate-runtime-contracts.py`     | Basis: ws consumer. Validate `.claude/settings.json` hook contract shape, runtime policy-surface boundaries, and local settings separation via `ws validate`.                                                            |
| active-ws     | `validation/validate-script-inventory.py`      | Basis: ws consumer. Validate this inventory and active `ws` command drift via `ws validate`.                                                                                                                              |
| active-ws     | `validation/validate-template-distribution.sh` | Basis: ws consumer. Validate the main release-template skeleton via `ws validate-distribution` and optional `TEMPLATE_DISTRIBUTION=1 ws validate`.                                                                        |
| active-ci     | `ci/validate-security.sh`              | Basis: CI consumer; derived-project conditional value. Run explicit local/Security CI lock-file, focused secret scan with sanitized output, changed governance/runtime file, and optional active-stack SAST checks.       |
| active-ws     | `validation/validate-skill-quality.sh`         | Basis: ws consumer. Validate runtime skill and agent quality via `ws validate`.                                                                                                                                           |
| active-ws     | `validation/validate-version-drift.py`         | Basis: ws consumer; derived-project conditional value. Validate active stack version drift only when tracked or non-empty stack roots exist.                                                                              |
| active-ws     | `ws.sh`                             | Basis: ws consumer. Unified workspace command entry point.                                                                                                                                                                |

## Direct Commands

Use these direct commands only for the documented scoped task. Use `bash scripts/ws.sh validate` for the canonical full gate. Run `bash scripts/ci/validate-security.sh` separately when validating the explicit local/Security CI security gate.

| Command                                                       | Use                                                                                                                                                                                |
| :------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bash scripts/qa/scaffold-tests-from-spec.sh docs/03.specs/<feature-id>/spec.md` | Generate sibling `docs/03.specs/<feature-id>/tests.md` scaffolding without overwriting an existing test strategy.                                                                   |
| `bash scripts/qa/summarize-tdd-coverage.sh [--fail-on-missing] [--tasks-dir <path>]` | Summarize Stage 06 implementation task TDD evidence; `--fail-on-missing` makes missing implementation evidence fail validation.                              |
| `bash scripts/docs/update-doc-readme-index.sh <docs-relative-dir>` | Refresh a docs-relative README `Documents` table after doc inventory changes.                                                                                                      |
| `bash scripts/validation/validate-code-style.sh`                   | Validate whitespace, line endings, and configured style hooks for repository content.                                                                                              |
| `bash scripts/validation/validate-commit-msg.sh <commit-message-file>`   | Validate one commit message file against the repository commit policy.                                                                                                             |
| `bash scripts/validation/validate-design-initialization.sh`              | Enforce the root `DESIGN.md` initialization hard stop before UI work.                                                                                                              |
| `python3 scripts/validation/validate-doc-readiness.py`                   | Check canonical docs frontmatter, README contracts, stage-specific template contract markers, index coverage, active-surface stale template-readiness references, and Codex surface rules. |
| `python3 scripts/validation/validate-path-portability.py`                | Warn about repository paths that exceed relative, absolute, segment, spacing, or Windows-reserved-character portability budgets.                             |
| `python3 scripts/validation/validate-stage-template-write.py`            | Check pending hook write input for stage-specific `docs/99.templates` conformance before the file is written.                                                                      |
| `python3 scripts/validation/validate-runtime-contracts.py`               | Check `.claude/settings.json` hook contract shape, required doc-readiness hook commands, referenced repo-local hook files, prohibited policy surfaces, and local settings separation. |

## How to Work in This Area

- Do not add a `ws` command unless the target script exists and is listed as active here.
- `ws dispatch` must not create branches, scaffold Stage 06 task files, or emit machine-specific links.
- `ws hook` canonical syntax is `bash scripts/ws.sh hook <SessionStart|PreToolUse|PostToolUse|PostToolUseFailure|PreCompact|Stop> [matcher]`. Use Claude-style hook JSON on stdin or the same `CLAUDE_TOOL_*` environment variables that Claude hooks receive. Codex and local runtimes may use equivalent `CODEX_TOOL_*` variables; the dispatcher maps them before running canonical hooks.
- `ws swarm` canonical syntax is `bash scripts/ws.sh swarm <task_id> <start|status|handoff|suggest> [next_role]`.
- Do not reference removed optional starter paths such as `examples/fullstack-starter/**` from active workflows.
- Do not install tools or create runtime environments from `ws setup`; report prerequisite classes from `docs/00.agent-governance/rules/environment-readiness.md` instead.
- Keep stack-specific scripts conditional or move them to examples.
- Do not keep compatibility wrappers in active `scripts/` unless they have a current owner, direct command, and validator coverage.
- Treat historical Stage 05/06 references to removed scripts as source-history unless the same reference appears in an active instruction, governance, workflow, or command surface.

## Governance Rules

- `scripts/README.md` is the script inventory source validated by `python3 scripts/validation/validate-script-inventory.py`.
- `bash scripts/ws.sh validate` is the canonical full local gate.
- Direct commands must stay listed in both the inventory and the Direct Commands table.
- Every active inventory row must carry a `Basis:` marker explaining why the script remains in the active `scripts/` surface.

## Related References

- [Docs Home](../docs/README.md)
- [Operations Index](../docs/05.operations/policies/README.md)
- [Environment Readiness](../docs/00.agent-governance/rules/environment-readiness.md)
- [Documentation Protocol](../docs/00.agent-governance/rules/documentation-protocol.md)

---

## Docs 3 Global Rules Reference

> Active on every task. HALT conditions enforced by agents.
> Applies when creating or changing governed documentation in this folder.
> Full definitions: `docs/00.agent-governance/rules/documentation-protocol.md §7`

| Rule                       | Summary                                                                              | HALT If                                          |
| :------------------------- | :----------------------------------------------------------------------------------- | :----------------------------------------------- |
| **R1 — Content Creation**  | Read template before creating any stage doc. Fill all sections. Set `status: draft`. | Template missing or `[placeholder]` text remains |
| **R2 — Auto-Indexing**     | Update this README after every change to this folder.                                | README not updated after folder change           |
| **R3 — Cross-Referencing** | Every stage doc must have `## Related Documents` with relative upstream links.       | Required upstream links absent                   |
