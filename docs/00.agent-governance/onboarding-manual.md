---
title: Onboarding Manual
version: 1.1.0
owner: Governance Architect
layer: governance
stage: 00
status: active
last-updated: 2026-05-17
---

# AI-Centric Onboarding Manual

## Overview

`video-analysis` is an audit-ready, language-agnostic template for human and AI collaboration. This manual explains the operating model agents must use before planning or implementation.

## 1. Repository Operating Model

The workspace uses exactly 8 allowed top-level `docs/` folders: `00.agent-governance`, `01.requirements`, `02.architecture`, `03.specs`, `04.execution`, `05.operations`, `90.references`, and `99.templates`.

- **00.agent-governance**: Agent rules, provider notes, scopes, memory, compliance, and data-governance policy.
- **01.requirements through 03.specs**: Product requirements, architecture requirements/decisions, and feature specifications.
- **04.execution**: Approved execution plans and task evidence.
- **05.operations**: User/operator guides, policies, runbooks, incidents, and postmortems.
- **90.references and 99.templates**: Reviewed references and canonical templates.

Agents must map every governed contribution to one of these stages. `_workspace/**` is scratch or generated intelligence, not final documentation.
On `main`, project-content folders (`01`, `02`, `03`, `04`, `05`, `90`) are release-template skeleton guides only until derived-project bootstrap creates project-specific documents.

## 2. Runtime Surfaces

- `AGENTS.md` is the concise workspace contract for all AI agents.
- `CLAUDE.md` and `GEMINI.md` are provider overlays.
- `.claude/**` is the canonical local runtime surface.
- `.codex/**` is a synchronized compatibility surface for Codex metadata.
- `.agents/**` is legacy compatibility guidance only when present; it is not an independent policy store.
- `.agent/**` and `.agent-work/**` are local/generated helper or handoff surfaces only.
- `docs/00.agent-governance/**` owns detailed governance policy.

## 3. Agent Behavior Policy

Agents use baton passing through canonical artifacts:

1. **Intake**: collect product/software and stack facts before new-project stage authoring.
2. **Plan**: create or update the Stage 05 plan in `docs/04.execution/plans/` before non-trivial implementation.
3. **Execute**: track work, verification, and remaining evidence in `docs/04.execution/tasks/`.
4. **Validate**: run the smallest relevant checks, then the canonical gate when governed surfaces changed.
5. **Sync**: update README indexes, `docs/LLM-WIKI.md`, and policy change history when the governed contract changes.

Agents must not push directly to `main` or `dev`, bypass PR review, ignore failed validation, or invent missing issue IDs.

## 4. Toolchain

Use `bash scripts/ws.sh help` as the command inventory. Common entrypoints:

- `bash scripts/ws.sh validate`: canonical governance and quality gate.
- `bash scripts/ws.sh info`: workspace health summary.
- `bash scripts/ws.sh intelligence`: repository intelligence refresh.
- `bash scripts/ws.sh bootstrap`: derived-project bootstrap.
- `bash scripts/ws.sh validate-distribution`: main release-template skeleton validation.
- `bash scripts/ws.sh dispatch` and `bash scripts/ws.sh swarm`: governed coordination records.

## AI Execution Checklist

- [ ] Read this manual, `AGENTS.md`, and the target stage README.
- [ ] Complete project initialization intake before new-project stage authoring.
- [ ] Confirm the work has the required Stage 01-05 anchors.
- [ ] Use `docs/99.templates/` for new governed documents.
- [ ] Record execution evidence in Stage 06 when implementation occurs.
- [ ] Run `ws validate` or `bash scripts/ws.sh validate` before final handoff for governed changes.
