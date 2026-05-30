---
title: Project Template Release Process
version: 1.0.0
owner: Governance Architect
layer: governance
stage: 00
status: active
last-updated: 2026-05-22
---

# Project Template Release Process

This rule defines how Project-Template promotes reusable template updates from
`dev` to the clean `main` release-template branch.

## Purpose

Project-Template keeps two different kinds of useful state:

- `dev` may retain maintenance PRDs, ARDs, ADRs, specs, plans, tasks,
  operations notes, and references that explain how the template was improved.
- `main` is the release-template surface for creating new projects and must keep
  new-project-owned document folders as README-driven skeletons only.

This rule prevents dev-only maintenance history from becoming accidental
project-owned content in a newly derived repository.

## Branch Contract

| Branch | Responsibility | Document expectation |
| --- | --- | --- |
| `dev` | Integration and template maintenance history | May contain classified template-maintenance and active-template-contract documents. |
| `main` | Clean reusable project-template release | `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/` contain README skeleton guides only. |
| feature/fix/docs branches | Reviewable template changes | Must state whether changes affect dev history, main release skeleton, or derived-project bootstrap. |

## Release Procedure

1. Start from `dev` and inspect `git status --short`.
2. Classify changed documents with `template-document-lifecycle.md` before moving,
   deleting, promoting, or treating any dev document as release content.
3. Normalize untracked or generated documents before validation. If a document is
   not reusable, convert local paths to placeholders or mark it local-only.
4. Run `bash scripts/ws.sh validate` on the integration branch.
5. Prepare the release PR to `main` so project-content folders contain only the
   allowed README skeleton guides unless the PR intentionally updates bootstrap
   output or Stage 00/template policy.
6. Run `bash scripts/ws.sh validate-distribution` against the release-template
   surface. A failure on raw `dev` is expected while maintenance documents remain
   present; a failure on the prepared release skeleton is blocking.
7. Fill `.github/PULL_REQUEST_TEMPLATE.md` completely and include validation
   evidence, migration notes, and any known residual risk.
8. Merge only through reviewed PR flow. Direct pushes to `main` or `dev` are
   prohibited by Git workflow policy and hook guardrails.

## Dev Back-Sync Policy

After a release-template PR is merged to `main`, do not merge `main` back into
`dev` when the release diff removes classified maintenance history from
project-content folders. `dev` intentionally preserves that history.

Use a separate PR targeting `dev` when a release uncovers reusable policy,
runtime, validator, script, or template changes that also belong on the
maintenance branch. That back-sync PR must:

- start from current `dev`,
- include only the reusable policy/runtime/script/template deltas,
- exclude release-skeleton document removals from `docs/01.requirements/`,
  `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`,
  `docs/05.operations/`, and `docs/90.references/`,
- state the reason any selected `main` delta is safe for `dev`,
- record a migration note when behavior changes, and
- validate with `bash scripts/ws.sh validate`.

`validate-distribution` is still expected to fail on raw `dev` while classified
maintenance documents remain present. Run it only against the prepared
release-template surface or with an explicit distribution-prep context.

Preservation is a deliberate action, not a cleanup failure. When a document is
kept on `dev`, its folder README or lifecycle inventory must identify it as
`template-maintenance`, `active-template-contract`, or `archive/reference` so a
future derived project does not inherit it as active project content.

## Migration Note Policy

Use a migration note when a release PR:

- removes a dev-maintenance document from the release skeleton,
- moves or renames a document,
- converts a document to `example` or `archive/reference`,
- drops generated reference history,
- changes bootstrap reset behavior, or
- changes document ownership policy.

The migration note may live in the PR body, `policy-change-log.md`, an execution
task, or the relevant lifecycle rule. It must include the reason, target branch
behavior, link impact, and validation evidence.

Minimum migration note format:

| Field | Required content |
| --- | --- |
| Reason | Why the file is removed, moved, archived, converted, or preserved as dev-only history. |
| Ownership | One of `project-seed`, `template-maintenance`, `example`, `archive/reference`, `remove-candidate`, or `active-template-contract`. |
| Target branch behavior | Whether the content remains on `dev`, is omitted from `main`, or is regenerated after bootstrap. |
| Link impact | References updated, intentionally broken links avoided, or why no link migration is needed. |
| Validation | Commands run, including `ws validate` and release-skeleton `validate-distribution` when applicable. |

## Hard Stops

- Stop if non-README Project-Template maintenance documents remain in
  new-project-owned folders on the prepared `main` release surface.
- Stop if `docs/99.templates/` is missing a required template for a governed
  document that the release creates or modifies.
- Stop if local absolute paths, secrets, tokens, private endpoints, or personal
  machine settings are required for template use.
- Stop if `validate-distribution` fails on the prepared release skeleton.
- Stop if a release PR omits migration notes for removed, moved, archived, or
  converted documents.

## Validation Commands

```bash
git status --short
bash scripts/ws.sh validate
bash scripts/ws.sh validate-distribution
```

For derived-project smoke checks after bootstrap:

```bash
bash scripts/ws.sh bootstrap --dry-run --name "SampleProject" \
  --product-purpose "..." --target-users "..." --core-features "..." \
  --success-criteria "..." --app-type "..." --language "..." \
  --framework "..." --runtime "..." --package-manager "..." \
  --database "..." --deployment-target "..." --ci-target "..." \
  --data-constraints "..." --security-constraints "..." \
  --external-services "..." --environments "..." --observability "..." \
  --slo-needed "..." --release-model "..." \
  --github-owner sample --security-email security@example.org
bash scripts/ws.sh validate-derived
```

## AI Execution Checklist

- [ ] **Entry Gate**: Branch role, changed files, and document ownership labels are known.
- [ ] **Procedure**: Classify dev-only documents before cleanup and run the canonical validation gate.
- [ ] **Exit Gate**: Release skeleton contains only allowed project-seed README guides and bootstrap behavior is documented.
- [ ] **Hard Stop**: Stop on unclassified non-README stage documents, unresolved local-only paths, or failed release-skeleton distribution validation.
- [ ] **Downstream Trigger**: Update README, Stage 00 indexes, lifecycle rules, and validators when release criteria change.
- [ ] **Evidence Rule**: Record `ws validate`, `validate-distribution`, and migration notes in the PR or task evidence.

## Role definition

- Applies to governance architects, docs-governance maintainers, release owners,
  and AI agents preparing or reviewing a Project-Template release PR.

## Procedure

- Keep `dev` maintenance history classified and reviewable.
- Keep `main` release skeleton clean for new-project reuse.
- Back-sync reusable policy, runtime, validator, script, or template changes
  through a focused PR to `dev` instead of merging release-skeleton deletions
  back into `dev`.
- Use PR-only promotion and document all cleanup, movement, archive, conversion,
  or removal decisions.
- Prefer omitting dev history from `main` over deleting useful maintenance
  evidence from `dev`.

## Constraints

- Do not promote Project-Template maintenance history as active derived-project
  requirements, architecture, specs, execution, operations, or references.
- Do not bypass `validate-distribution` for a release-template PR.
- Do not introduce a stack, deployment target, SLO, API, or product assumption
  unless derived-project intake declares it.
- Do not merge release-skeleton cleanup from `main` into `dev` when that would
  remove classified maintenance history.
- Do not use destructive Git cleanup commands without explicit human approval.

## File references

- `AGENTS.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `scripts/setup/bootstrap-project.sh`
- `scripts/validation/validate-template-distribution.sh`
- `docs/00.agent-governance/rules/git-workflow.md`
- `docs/00.agent-governance/rules/template-document-lifecycle.md`
- `docs/00.agent-governance/rules/project-initialization-intake.md`

## Related Documents

- [Template Document Lifecycle](./template-document-lifecycle.md)
- [Project Initialization Intake](./project-initialization-intake.md)
- [Git Workflow](./git-workflow.md)
- [CI/CD Workflow](./ci-cd-workflow.md)
- [Template Catalog](../../99.templates/README.md)
