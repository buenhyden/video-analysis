---
title: Template Document Lifecycle and Ownership
version: 1.0.0
owner: Governance Architect
layer: governance
stage: 00
status: active
last-updated: 2026-05-22
---

# Template Document Lifecycle and Ownership

This rule defines how video-analysis separates reusable template assets from
documents that belong to a newly derived project.

## Purpose

video-analysis is a reusable starting workspace. It provides governance,
documentation structure, templates, validation, local agent runtime defaults, and
safe bootstrap automation. It does not provide a default product, application
stack, deployment target, SLO, or completed project documentation.

## Ownership Labels

| Label | Meaning | Allowed in a newly derived project |
| --- | --- | --- |
| `project-seed` | Minimal README skeleton or bootstrap-generated draft PRD seed with TODOs and no completed decisions. | Yes, only stage README skeletons plus the bootstrap PRD seed after intake. |
| `template-maintenance` | Evidence or plans for maintaining video-analysis itself. | No. Keep on `dev` or move to Stage 00 governance. |
| `example` | Reusable example clearly marked as non-authoritative. | Optional, only under an examples or reference area. |
| `archive/reference` | Historical or supporting reference material. | Optional, only if clearly marked and linked as reference. |
| `remove-candidate` | Duplicated, stale, unsafe, or no longer useful content. | No. Remove only after reference search and migration note. |
| `active-template-contract` | Canonical rule, decision, or reference that defines this template. | No as project content. Keep in Stage 00, templates, or `dev` maintenance history. |

## Branch Contract

- `main` is the release-template branch for new projects.
- On `main`, `docs/01.requirements/`, `docs/02.architecture/`,
  `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and
  `docs/90.references/` must contain README skeleton guides only.
- `dev` may retain video-analysis maintenance history for review and
  traceability.
- A newly derived project must not inherit `dev` maintenance history unless the
  maintainer intentionally keeps it with `--keep-template-history`.
- The current `dev` inventory contains 55 dev-only entries under
  new-project-owned folders: 8 `active-template-contract`, 41
  `template-maintenance`, and 6 `archive/reference`. It also contains 14
  `project-seed` README skeleton guides that remain release-template content.
  None of the dev-only entries are `project-seed`, `example`, or tracked
  `remove-candidate` content.
- Release promotion from `dev` to `main` follows `release-process.md`.

## New Project Bootstrap Flow

1. Complete product/software and stack intake.
2. Run `bash scripts/ws.sh bootstrap --dry-run ...`.
3. Run bootstrap without `--dry-run` only after the dry-run output is understood.
4. Let bootstrap reset project-content folders to README-driven state unless
   `--keep-template-history` is intentionally used for template maintenance.
5. Use the generated Stage 01 intake PRD seed as the first project-owned non-README document.
6. Create ARD, ADR, spec, plan, task, operations, and reference documents only
   when their stage gate is reached.
7. Run `bash scripts/ws.sh validate-derived`.

## Derived-project Reset Contract

Use this contract when deciding whether content can remain in a newly created
project:

| Surface | Keep in a derived project? | Required action |
| --- | --- | --- |
| Stage README skeletons | Yes | Rewrite overview, scope, and Documents rows for the actual project as content appears. |
| Bootstrap PRD intake seed | Yes, after intake | Replace TODOs before using it as an upstream gate. |
| video-analysis PRDs, ARDs, ADRs, specs, plans, tasks, SLOs, onboarding guides, and references on `dev` | No by default | Omit from `main` release skeleton and derived projects unless `--keep-template-history` is intentional. |
| Stage 00 governance and `docs/99.templates/**` | Yes | Keep as reusable defaults; update only through governance/template maintenance. |
| `.claude/**` and `.codex/agents/*.toml` | Yes | Keep `.claude/**` canonical and `.codex/**` compatibility-only. |
| Local-only runtime or helper output | No | Do not commit or reuse blindly; regenerate locally if needed. |

## Seed Document Policy

Seed documents are not completed decisions. They must use `status: draft`, include
TODO language where facts are still unknown, and avoid claims that architecture,
specification, rollout, SLO, or operational readiness has already been approved.
Bootstrap creates only the Stage 01 intake PRD seed. ARD, ADR, spec, plan, task,
operations, and reference seeds must be generated later from the matching
template only when their stage gate is reached.

| Seed type | Target | Source template | Creation rule |
| --- | --- | --- | --- |
| Requirements intake PRD | `docs/01.requirements/YYYY-MM-DD-project-intake-prd.md` | `docs/99.templates/prd.template.md` | Created by bootstrap from intake values. |
| PRD | `docs/01.requirements/YYYY-MM-DD-<slug>.md` | `docs/99.templates/prd.template.md` | Create after intake when a real project scope exists. |
| ARD | `docs/02.architecture/requirements/####-<slug>.md` | `docs/99.templates/ard.template.md` | Create after PRD scope is reviewable. |
| ADR | `docs/02.architecture/decisions/####-<slug>.md` | `docs/99.templates/adr.template.md` | Create only for an actual decision trigger. |
| Spec | `docs/03.specs/<feature-id>/spec.md` | `docs/99.templates/spec.template.md` | Create after PRD/ARD inputs exist or are explicitly waived. |
| Test strategy | `docs/03.specs/<feature-id>/tests.md` | `docs/99.templates/tests.template.md` | Create before Stage 04 execution planning for `impl` work. |
| Plan | `docs/04.execution/plans/YYYY-MM-DD-<slug>.md` | `docs/99.templates/plan.template.md` | Create before non-trivial execution. |
| Task | `docs/04.execution/tasks/YYYY-MM-DD-<slug>.md` | `docs/99.templates/task.template.md` | Create before implementation starts. |
| Operations guide | `docs/05.operations/guides/<slug>.md` | `docs/99.templates/guide.template.md` | Create after verified behavior exists. |
| Operations policy or SLO | `docs/05.operations/policies/<slug>.md` or `SLO.md` | `operation.template.md` or `slo.template.md` | Create only when the derived project declares operational targets. |
| Runbook | `docs/05.operations/runbooks/####-<topic>.md` | `docs/99.templates/runbook.template.md` | Create after an operations policy or known risk exists. |
| Incident/postmortem | `docs/05.operations/incidents/YYYY/INC-###-<title>/` | `incident.template.md`, `postmortem.template.md` | Create only for real incidents. |
| Reference | `docs/90.references/<slug>.md` or `knowledge/<slug>.md` | `docs/99.templates/reference.template.md` | Create only for sourced, reviewed facts. |

## Current Dev Inventory Classification

On the `main` release-template skeleton, this section intentionally contains no
concrete video-analysis maintenance-history path table. The detailed inventory
lives on `dev`, where those files exist and can be reviewed before the next
release-prep branch is cut.

Release skeleton branches must not keep hardcoded references to omitted
maintenance files under new-project-owned folders. Stable rules belong in Stage
00 governance, templates, validators, and root/provider runtime routers.

## Cross-Stage Ownership Summary

| Ownership label | Count | Release-template behavior |
| --- | ---: | --- |
| `project-seed` | 14 | Keep only the stage README skeleton guides plus bootstrap-generated draft PRD seed after intake. |
| `active-template-contract` | 0 project-content files | Keep stable contract text in Stage 00, templates, validators, or runtime routers, not as project-content history on `main`. |
| `template-maintenance` | 0 project-content files | Keep on `dev`; omit from ordinary derived projects and the clean `main` skeleton. |
| `archive/reference` | 0 project-content files | Add only after a derived project creates sourced, reviewed reference content. |
| `example` | 0 | Add only after explicit non-authoritative example conversion. |
| `remove-candidate` | 0 tracked docs | Remove only after reference search and migration note. |

| Release-skeleton file | Ownership | Behavior |
| --- | --- | --- |
| `docs/01.requirements/README.md` | `project-seed` | Intake and PRD authoring guide. |
| `docs/02.architecture/README.md` | `project-seed` | Architecture hub guide. |
| `docs/02.architecture/requirements/README.md` | `project-seed` | ARD authoring guide. |
| `docs/02.architecture/decisions/README.md` | `project-seed` | ADR authoring guide. |
| `docs/03.specs/README.md` | `project-seed` | Spec package authoring guide. |
| `docs/04.execution/README.md` | `project-seed` | Execution hub guide. |
| `docs/04.execution/plans/README.md` | `project-seed` | Plan authoring guide. |
| `docs/04.execution/tasks/README.md` | `project-seed` | Task evidence authoring guide. |
| `docs/05.operations/README.md` | `project-seed` | Operations hub guide. |
| `docs/05.operations/guides/README.md` | `project-seed` | Guide authoring guide. |
| `docs/05.operations/policies/README.md` | `project-seed` | Operations policy authoring guide. |
| `docs/05.operations/runbooks/README.md` | `project-seed` | Runbook authoring guide. |
| `docs/05.operations/incidents/README.md` | `project-seed` | Incident/postmortem authoring guide. |
| `docs/90.references/README.md` | `project-seed` | Reference authoring guide. |

README skeletons under `docs/01.requirements/`, `docs/02.architecture/`,
`docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and
`docs/90.references/` are `project-seed` guides. They may remain in new projects,
but their `Documents` tables must be refreshed after bootstrap.

Nested package READMEs under project-content folders are not release-skeleton
seeds unless bootstrap or a derived project creates the package.

## Cleanup And Migration Rules

- Search references before moving or deleting any classified file.
- Prefer policy promotion to Stage 00 when a document defines stable template
  behavior.
- Prefer omission from `main` over deletion when the file is useful dev history.
- Convert to `example` only when the document is explicitly rewritten as a
  non-authoritative sample.
- Convert to `project-seed` only by regenerating from the matching
  `docs/99.templates/` template after project intake.
- Remove only after all links are migrated and a policy-change-log note records
  the reason.
- If the chosen action is to preserve `dev` history in place, make the ownership
  label and `main` omission behavior explicit in the folder README instead of
  moving the document.
- A migration note must name the reason, ownership label, target branch behavior,
  link impact, and validation command evidence.

## Runtime Residue Migration Notes

The following untracked generated surfaces are `remove-candidate` residue, not
reusable template content:

| Surface | Classification | Required action |
| --- | --- | --- |
| `.codex/hooks.json` | `remove-candidate` | Remove after approval. Hook policy is owned by `.claude/settings.json`; provider-neutral replay uses `bash scripts/ws.sh hook <event> [matcher]`. |
| `.codex/hooks/**` | `remove-candidate` | Remove after approval. Do not create Codex-only hook policy files. |
| `.agents/skills/**` | `remove-candidate` | Remove after approval. Active skills live under `.claude/skills/**`; tracked `.agents/**` is legacy/helper surface only. |

Tracked legacy helper files such as `.agents/README.md`,
`.agents/rules/graphify.md`, and `.agents/workflows/graphify.md` are not
automatic removal candidates. Decide their future in a separate lifecycle change.

## Local And Personal Surface Policy

- Template-safe examples may mention placeholder emails such as
  `security@example.org`.
- Local helper paths such as `~/.agent/...` or `~/.claude/...` must be described
  as optional user-global paths, never required template dependencies.
- Do not commit `auth.json`, private keys, shell history, log databases, tokens,
  `.env` values, or machine-specific absolute paths.
- `.claude/settings.local.json`, if present, is local-only and must not be reused
  blindly by derived projects.
- Do not commit `.codex/hooks.json`, `.codex/hooks/**`, or `.agents/skills/**`
  as template policy or active runtime inventory.

## Verification

Use these checks before declaring the template ready for reuse:

```bash
git status --short
bash scripts/ws.sh validate
bash scripts/ws.sh validate-distribution
```

Run `validate-distribution` against the release-template surface. It is expected
to fail on `dev` while dev-only maintenance documents remain present.
Run `validate-derived` only after a derived project has initialized metadata,
`DESIGN.md`, GitHub placeholders, and the bootstrap intake PRD seed.

For routine `dev` maintenance, `bash scripts/ws.sh validate` must pass and
`validate-distribution` may list the classified dev-only files in warn-only mode.
For a release-template PR to `main`, the same classified files become blocking
unless they are intentionally transformed into README skeleton guidance.

## Role definition

- Applies to governance architects, docs-governance maintainers, and agents
  initializing or auditing a derived project.

## Procedure

- Classify documents before changing their path or ownership.
- Keep base-template release content README-driven.
- Generate project-owned seed documents from templates only after intake.
- Record migration decisions in this rule, `policy-change-log.md`, or the
  relevant execution task.

## Constraints

- Do not leave template-maintenance documents in a newly derived project without
  explicit `--keep-template-history`.
- Do not promote a completed video-analysis plan, task, spec, or reference as
  a new project's active requirement, architecture, operation, or reference.
- Do not create stack-specific seed documents before the intake declares a stack.

## File references

- `AGENTS.md`
- `README.md`
- `scripts/setup/bootstrap-project.sh`
- `scripts/validation/validate-template-distribution.sh`
- `docs/00.agent-governance/rules/release-process.md`
- `docs/00.agent-governance/rules/project-initialization-intake.md`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/99.templates/`

## Related Documents

- [Project Initialization Intake](./project-initialization-intake.md)
- [Release Process](./release-process.md)
- [Documentation Protocol](./documentation-protocol.md)
- [Stage-Gate Matrix](./stage-gate-matrix.md)
- [Template Catalog](../../99.templates/README.md)
