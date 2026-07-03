---
title: Project Initialization Intake
version: 1.0.0
owner: Governance Architect
layer: governance
stage: 00
status: active
last-updated: 2026-05-21
---

# Project Initialization Intake

This rule defines the first gate for any new project derived from this template.
Agents must collect product/software intent and stack facts before writing PRD,
ARD, spec, plan, task, operation, or reference documents.

## Required Intake Fields

The first project input must include:

- Product/software name, purpose, target users, core features, and success criteria.
- Application type: web, mobile, backend, library, CLI, infra, AI/RAG/agent, or another explicit type.
- Technical stack: language, framework, runtime, package manager, database, deployment target, and CI/CD target.
- Data and security constraints: PII, secrets, authentication, compliance, and external services.
- Operations baseline: environments, observability, SLO need, and release model.

## Intake Sources

The intake may be supplied as:

- a reviewed intake Markdown file passed to `bash scripts/ws.sh bootstrap --intake-file <path>`, or
- explicit bootstrap flags that cover all required fields.

Do not infer absent stack choices from this template. This template is language-agnostic
until the derived project intake declares a stack.

Bootstrap writes the first Stage 01 seed as
`docs/01.requirements/YYYY-MM-DD-project-intake-prd.md`. That file is a draft
PRD-shaped intake record, not an approved PRD, architecture decision, spec,
plan, SLO, or runbook. Replace TODOs with reviewed project facts before using it
as an upstream stage gate.

Bootstrap must not create ARD, ADR, spec, plan, task, operations, or reference
seeds by default. Those documents are generated from `docs/99.templates/` only
after their stage gate is reached and the required upstream context exists or is
explicitly waived.

## Main Release Skeleton Policy

The `main` branch is the release-template surface for new projects. In `main`,
these folders contain README skeleton guides only:

- `docs/01.requirements/`
- `docs/02.architecture/`
- `docs/03.specs/`
- `docs/04.execution/`
- `docs/05.operations/`
- `docs/90.references/`

video-analysis development history, completed PRDs, ARDs, ADRs, specs, plans,
tasks, operational guides, SLOs, generated intelligence, and reference artifacts
belong on `dev` or another maintenance branch, not in the `main` release skeleton.

## Runtime Surface Policy

- `.claude/**` is the canonical local runtime surface.
- `.codex/agents/*.toml` is synchronized Codex compatibility metadata only.
- `.codex/hooks.json` and `.codex/hooks/**` are forbidden policy surfaces; use `bash scripts/ws.sh hook <event> [matcher]` for provider-neutral replay.
- `.agents/**`, when present, is a legacy compatibility mirror and must not define independent policy.
- `.agents/skills/**` is not an active skill tree; active skills live under `.claude/skills/**`.
- `.agent/**` is local/generated helper guidance only and must not override Stage 00 governance.
- `.agent-work/**` is local handoff state and is not part of the reusable template contract.

## Hard Stops

- Stop before authoring project stage documents if the intake is missing or incomplete.
- Stop before authoring or modifying project stage documents if the matching `docs/99.templates/` contract has not been loaded.
- Stop if a stack-specific rule, command, CI target, or framework is introduced before it appears in the intake.
- Stop if `main` contains project-history documents in the skeleton-only folders above.
- Stop if a video-analysis maintenance document is reused as active derived-project content without classification through `template-document-lifecycle.md`.

## Related Documents

- [Bootstrap Governance](./bootstrap.md)
- [Documentation Protocol](./documentation-protocol.md)
- [Harness Library](./harness-library.md)
- [Stage-Gate Matrix](./stage-gate-matrix.md)
- [Template Document Lifecycle](./template-document-lifecycle.md)

## Role definition

- Applies to agents and humans initializing a derived project from the release template.

## Procedure

- Complete the intake before stage authoring.
- Use bootstrap intake flags or `--intake-file`.
- Treat the bootstrap-generated intake PRD as a seed document until reviewed.
- Translate the intake into project-specific stage documents using the stage-specific contracts in `docs/99.templates/`.

## Constraints

- Do not infer a stack that the intake did not declare.
- Do not restore video-analysis history documents into the `main` release skeleton.
- Do not treat bootstrap-generated TODO rows as approved requirements.
- Do not restore `.codex/hooks*` or `.agents/skills/**` as reusable runtime policy.

## File references

- `AGENTS.md`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/template-document-lifecycle.md`
- `scripts/setup/bootstrap-project.sh`
