---
title: Environment Readiness
version: 1.0.0
owner: Governance Architect
layer: governance
stage: 00
status: active
last-updated: 2026-05-21
---

# Environment Readiness

## Purpose

Define the workspace assets and local prerequisites required for humans and AI agents to run this project template safely. This rule keeps environment checks report-only: agents may identify missing tools, but must not install tools, mutate local configuration, or assume stack-specific dependencies before project intake declares them.

## Built-In Workspace Assets

The base template provides these reusable assets:

- Root routers: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`, and `DESIGN.md`.
- Canonical runtime surface: `.claude/CLAUDE.md`, `.claude/agents/*.md`, `.claude/skills/**`, `.claude/settings.json`, and `.claude/hooks/**`.
- Compatibility runtime metadata: `.codex/agents/*.toml`. This is not an independent policy store.
- Optional legacy or helper surfaces: `.agents/**` and `.agent/**`, when present, are compatibility or generated guidance only.
- Governance rules, scopes, providers, memory, and policy history under `docs/00.agent-governance/**`.
- Canonical document templates under `docs/99.templates/**`.
- Workspace commands, setup, bootstrap, validation, docs, CI, QA, harness, and generation helpers under `scripts/**`.
- Clean release-template skeleton README guides under `docs/01.requirements/` through `docs/90.references/` on `main`.

## Local Prerequisite Classes

| Class | Tools | Required When | Failure Semantics |
| --- | --- | --- | --- |
| Core governance runtime | `git`, `bash`, `python3`, `rg`, Python `yaml` module | Every maintained template workspace and normal agent session | Missing tools block reliable local validation and must be reported before closure. |
| Review and publishing | `gh` | Local PR creation, PR inspection, and CI status review | Missing `gh` blocks local GitHub workflow actions only; it does not make the template invalid. |
| Documentation and lint | `markdownlint-cli2`, `yamllint`, `shellcheck`, `mkdocs` | Optional local linting or docs-site build/serve | Missing tools downgrade to skip/warn unless the task explicitly requires that check. |
| Security and dependency audit | `bandit`, `pip-audit`, `gitleaks`, `trivy` | Explicit local security validation or active stack manifests | Missing tools downgrade to skip/warn unless a security gate explicitly requires them. |
| Derived stack runtime | `node`, `npm`, `docker`, and any language/runtime declared by intake | Only after a derived project adopts the corresponding stack | Missing tools block only stack-specific tasks and must be tied to declared intake or manifests. |

`bash scripts/ws.sh setup` is the canonical local report command for these classes. It must remain non-mutating and must not install packages, write dotfiles, create environments, or change repository content.

## Local-Only Surfaces

The following surfaces must not be copied into reusable template policy or committed as portable defaults:

- `.claude/settings.local.json`
- `.codex/hooks.json` and `.codex/hooks/**`
- `.agents/skills/**`
- `_workspace/**`
- `.agent-work/**`
- Credential files, auth databases, shell history, local logs, private keys, tokens, or machine-specific absolute paths

Agents may mention these paths as local-only examples, but must not read credentials or promote local state into governance documents without explicit user approval and a clear task need.

## Readiness Checks

Use the smallest applicable check:

| Scenario | Command | Expected Interpretation |
| --- | --- | --- |
| Local prerequisite report | `bash scripts/ws.sh setup` | Reports required, optional, and conditional tools without mutating the workspace. |
| Base template validation | `bash scripts/ws.sh validate` | Validates governance, docs, scripts, runtime contracts, links, and conditional stack checks. |
| Derived project after bootstrap | `bash scripts/ws.sh validate-derived` | Adds strict derived-project placeholder and metadata validation. |
| Release-template skeleton | `bash scripts/ws.sh validate-distribution` | Must pass on prepared `main` release skeleton; expected to fail on raw `dev` while maintenance history remains. |

## Hard Stops

Stop and resolve before closing the task when any of these conditions apply:

- A core governance runtime prerequisite is missing and the task depends on repository inspection, docs validation, or script validation.
- A tool is installed or local configuration is mutated from `ws setup`.
- A stack-specific tool is treated as required before `project-initialization-intake.md` declares the stack.
- Local-only surfaces are committed, copied into reusable policy, or used as canonical runtime authority.
- Optional missing tools are presented as proof that the base template itself is invalid without tying them to a declared task or stack.

## Role definition

- Applies to all AI agents and maintainers validating whether the template can be used or maintained locally.

## Procedure

1. Load this rule when a task touches setup, validation, local tooling, runtime readiness, bootstrap, CI portability, or agent-environment consistency.
2. Run `bash scripts/ws.sh setup` before environment-sensitive work when tool availability is unknown or relevant to the requested change.
3. Classify missing tools using the Local Prerequisite Classes table before deciding whether the task is blocked.
4. Use `bash scripts/ws.sh validate` for the canonical local gate after governance, script, docs, runtime, or template changes.
5. Record skipped optional checks in the final report when the task depends on those checks.

## Constraints

- Keep setup commands report-only and non-mutating.
- Do not add default application stack requirements to the base template.
- Do not encode personal paths, local usernames, host-specific paths, secrets, or private endpoints in reusable files.
- Keep `.claude/**` canonical for runtime behavior and `.codex/**` compatibility-only unless a future governance change explicitly updates the contract.
- Update this rule, `scripts/setup/setup-environment.sh`, `scripts/README.md`, and `docs/LLM-WIKI.md` together when the prerequisite classes change.

## File references

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/CLAUDE.md`
- `scripts/ws.sh`
- `scripts/setup/setup-environment.sh`
- `scripts/README.md`
- `docs/LLM-WIKI.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/harness-library.md`
- `docs/00.agent-governance/rules/template-document-lifecycle.md`

## Related Documents

- [Bootstrap Governance](./bootstrap.md)
- [Preflight Checklist](./preflight-checklist.md)
- [Harness Library](./harness-library.md)
- [Template Document Lifecycle](./template-document-lifecycle.md)
- [Scripts & Utilities](../../../scripts/README.md)
- [Workspace Wiki](../../LLM-WIKI.md)
