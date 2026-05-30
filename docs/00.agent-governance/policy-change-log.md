# Workspace Policy Change Log

This document records all significant changes to the workspace governance, SDLC protocols, and automated validation rules.

It is not active task memory or a workflow diagram. Use `docs/00.agent-governance/memory/progress.md` for current progress and handoff state, `docs/00.agent-governance/memory/methodology.md` for active methodology state, `docs/00.agent-governance/sdlc-workflow.md` for the stable human-agent collaboration flow, and dated memory files for durable lessons learned.

| Date       | Version | Type                | Summary                                                                                                                                                                                                                                                                                                                                                     | Related ADR/Plan                                                                                                                                                                               |
| :--------- | :------ | :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-05-22 | 1.56.0  | Governance Boundary | Implemented the preservation-plus-clarification reuse plan: documented derived-project reset semantics, kept `dev` maintenance history in place, softened Graphify authority wording, narrowed PRD preflight anchors to non-README PRDs, expanded target-relative template guidance, and added a tracked `.agents/**` legacy helper allowlist validator. | User-approved Project-Template reuse readiness implementation plan |
| 2026-05-21 | 1.55.0  | Agent Runtime       | Added the Environment Readiness rule to classify built-in workspace assets, core local prerequisites, optional review/docs/security tools, stack-conditional runtimes, local-only surfaces, and the non-mutating `ws setup` contract; expanded setup reporting to include `rg`, `gh`, docs, security, and stack tools without installing them. | User-requested AI agent environment and rule consistency review |
| 2026-05-21 | 1.54.0  | Script Governance   | Added focused `main` to `dev` back-sync policy so release-skeleton cleanup does not erase dev maintenance history, and replaced GNU-only `sed -i` bootstrap edits with Python-backed literal/line replacement helpers. | User-requested dev policy sync and bootstrap portability follow-up |
| 2026-05-21 | 1.53.0  | Governance Boundary | Added the release-template promotion rule for `dev` to `main`, updated lifecycle inventory counts for the release-prep plan, and clarified that `validate-distribution` is a release-skeleton gate rather than a raw `dev` health signal. | `docs/04.execution/plans/2026-05-21-template-readiness-release-prep.md` |
| 2026-05-21 | 1.52.0  | Governance Boundary | Clarified Project-Template reuse readiness: root/provider routers stay thin, dev maintenance history is labeled as template contract/history rather than project seed, generated stage documents default to draft, and forbidden runtime residue now includes `.codex/hooks/**` and `.agents/skills/**`. | User-requested Project-Template Reuse Readiness Plan |
| 2026-05-19 | 1.51.0  | Governance Boundary | Added the template document lifecycle rule, classified dev-only Project-Template history versus derived-project seed content, aligned Graphify as optional supporting context, and made bootstrap create a PRD-shaped intake seed instead of a non-template intake note.                       | User-requested Project-Template readiness audit and migration planning                                                                                                                         |
| 2026-05-19 | 1.50.0  | Agent Runtime       | Hardened provider-neutral hook replay so Codex/local agents can pass Claude-style hook JSON or `CODEX_TOOL_*` variables into the canonical `.claude/hooks/**` stage-template write gates, and added runtime validation for dispatcher portability.                                                       | User-requested dev branch cleanup and template hook enforcement                                                                                                                                |
| 2026-05-18 | 1.49.0  | Validation          | Added template README inventory-cell validation, narrow path-like Markdown label/href validation, durable template inventory summary generation, and README Docs 3 conformance sync while preserving intentional template source placeholders.                                                                                                                  | Template Catalog and README Conformance Plan (dev history)                                                                        |
| 2026-05-17 | 1.48.0  | Script Governance   | Added fail-on-missing TDD evidence enforcement to `ws validate`, documented the retained script categories including `reserved-direct`, tightened inventory drift checks for canonical `ws swarm <task_id>` syntax, deprecated the stale pre-deploy ADR, and removed ignored generated script cache residue. | User-approved Scripts Usage Cleanup and QA Gate Plan; ADR-0002 (dev history)                                                              |
| 2026-05-17 | 1.47.0  | Script Governance   | Removed the forbidden Codex hook surface, made the graphify hook timeout explicit in the canonical Claude settings, removed command-first swarm compatibility, and aligned QA test scaffolding with `docs/03.specs/<feature-id>/spec.md` and sibling `tests.md`.                              | User-approved Scripts / Runtime / QA Cleanup Plan                                                                                                                                              |
| 2026-05-16 | 1.46.0  | Governance Docs     | Applied the approved prompt-package and governance cleanup: added `.agent-work` phase/skill controls, clarified prompts 10-16 authority, documented root `GEMINI.md` as the Gemini entrypoint, scoped Graphify as optional generated intelligence, reconciled active memory/wiki state, and refreshed Stage 90 freshness metadata.                                | `.agent-work/report/17-plan-review-approval-gate-report.md`; `.agent-work/report/18-implementation-execution-report.md`                                                                        |
| 2026-05-13 | 1.45.0  | Governance Docs     | Periodic governance audit: enforced English-only policy in `data-governance/encryption-standards.md` (11 Korean prose lines translated), removed 6 stale migration `permissions.allow` entries from `settings.local.json`, and corrected stale `status: active` → `status: completed` in `docs/04.execution/tasks/2026-05-12-workspace-gap-remediation.md`. | Periodic audit cycle `periodic-governance-audit-2026-05-13`                                                                                                                                    |
| 2026-05-12 | 1.44.0  | Agent Runtime       | Updated `agent-hook-dispatch.py` argparse `event` help string to list all active wired events (`PostToolUseFailure`, `PreCompact` added alongside existing four). Updated `scripts/README.md` `ws hook` canonical syntax to match.                                                                                                                          | Implementation Executor Agent follow-up (2026-05-12 governance audit)                                                                                                                          |
| 2026-05-12 | 1.43.0  | Agent Runtime       | Added `PostToolUseFailure` → `error-logger.sh` (non-blocking failure log) and `PreCompact` → `pre-compact-context.sh` (workspace snapshot before compaction). Consolidated `.gitignore` `_workspace/` subdirectory patterns to single `_workspace/` entry. Updated harness-library.md Hook Inventory, LLM-WIKI §4, CLAUDE.md Enforcement Catalog.           | Hooks, Guardrails, Memory, Wiki Agent (2026-05-12 governance audit)                                                                                                                            |
| 2026-05-12 | 1.42.0  | Governance Docs     | Resolved `core-rules.md` duplication: absorbed SDD rule into `agentic.md` Execute step, added lazy-load section to `harness-library.md`, added archive trigger criteria to `archive/README.md`, removed `core-rules.md` references from `rules/README.md`, and deleted `core-rules.md`. Updated `memory/progress.md` active task.                           | Phase A/C/D governance-doc-alignment (2026-05-12 governance audit)                                                                                                                             |
| 2026-05-12 | 1.41.0  | Agent Runtime       | Added scoped Python script permission for the former generated LLM-WIKI navigation helper and added hook timeouts to prevent session hangs.                                                         | Phase B settings remediation (2026-05-12 governance audit)                                                                                                                                     |
| 2026-05-10 | 1.40.0  | Agent Runtime       | Added `ws hook` event dispatch so Claude, Codex, Gemini, and other local agents can execute the canonical `.claude/settings.json` command hooks by event without adding a second hook policy surface.                                                                                                                                                       | Agent Hook Event Dispatch Plan (dev history)                                                                                                |
| 2026-05-10 | 1.39.0  | Agent Runtime       | Hardened Claude hooks for sensitive path/content blocking, protected-branch Git policy enforcement, MultiEdit README synchronization, and dynamic session scope reporting.                                                                                                                                                                                  | Hook Policy Hardening Plan (dev history)                                                                                                        |
| 2026-05-10 | 1.38.0  | Agent Runtime       | Added the dedicated `wiki-curator` role, generated navigation workflow, freshness check, and stale compact-docs wording guardrails.                                                                                                                                                                                                     | LLM-WIKI Curator Runtime Closure Plan (dev history)                                                                                  |
| 2026-05-10 | 1.37.0  | Validation          | Aligned Security CI artifact upload with the workflow role matrix, normalized compact LLM-WIKI routing, and enforced QA test strategy ownership.                                                                                                                                                                                                            | Compact Docs Migration Plan (dev history)                                                                                                      |
| 2026-05-10 | 1.36.0  | Governance Boundary | Clarified that `00.agent-governance/sdlc-workflow.md` is docs-relative shorthand only and must not become a root-level duplicate workflow authority.                                                                                                                                                                                                        | User request                                                                                                                                                                                   |
| 2026-05-10 | 1.35.0  | Governance Boundary | Confirmed `00_System/sdlc-workflow.md` is not a Project-Template governance path and that `docs/00.agent-governance/sdlc-workflow.md` remains the canonical workflow reference.                                                                                                                                                                             | User request                                                                                                                                                                                   |
| 2026-05-10 | 1.34.0  | Governance Boundary | Clarified the `sdlc-workflow.md` boundary against Stage 00 memory, policy-change-log, and `_workspace/**`; added validator coverage for the workflow boundary contract.                                                                                                                                                                                     | User request                                                                                                                                                                                   |
| 2026-05-10 | 1.33.0  | Agent Memory        | Defined `_workspace/**` as transient runtime output, promoted active progress and methodology state to Stage 00 memory, added the dedicated progress template, and clarified the policy-change-log boundary.                                                                                                                                                | User request                                                                                                                                                                                   |
| 2026-05-09 | 1.32.0  | Script Governance   | Added retention-basis markers for active scripts so inventory validation distinguishes owned/wired scripts from conditional derived-project readiness overhead.                                                                                                                                                                                             | `docs/04.execution/archive/plans/2026-05-09-script-surface-audit-hardening.md` (archive purged in b8c007d)                                     |
| 2026-05-09 | 1.31.0  | CI/CD               | Aligned required merge-gate policy with protected branches `main` and `dev`, clarified active security gates, and excluded repository automation workflows from required branch-protection checks.                                                                                                                                                          | `docs/04.execution/archive/plans/2026-05-09-github-required-merge-gate-policy-alignment.md` (archive purged in b8c007d)           |
| 2026-05-09 | 1.30.0  | Agent Harness       | Closed harness/Agent-first evidence gaps by aligning validator scope claims, adding runtime compatibility ADR coverage, enforcing shim and Stage 90 freshness guardrails, and clarifying security validation semantics.                                                                                                                                     | `docs/04.execution/archive/plans/2026-05-09-harness-agent-first-evidence-closure.md` (archive purged in b8c007d)                         |
| 2026-05-09 | 1.29.0  | Validation          | Added content-hash template-conformance baseline validation for canonical stage documents and clarified legacy source-history handling.                                                                                                                                                                                                                     | `docs/04.execution/archive/plans/2026-05-09-agent-first-policy-validator-alignment.md` (archive purged in b8c007d)                     |
| 2026-05-09 | 1.28.0  | Agent Harness       | Added the Harness and Agent-first component matrix reference and enforced active skill inventory parity between `harness-library.md` and `.claude/skills/**`.                                                                                                                                                                                               | `docs/04.execution/archive/plans/2026-05-09-harness-agent-first-component-matrix-hardening.md` (archive purged in b8c007d)     |
| 2026-05-09 | 1.27.0  | Agent Runtime       | Repaired stale Claude hook naming and numbered AGENTS references, fixed preflight inline Markdown spacing, and hardened doc-readiness validation for runtime-router drift.                                                                                                                                                                                  | `docs/04.execution/archive/plans/2026-05-09-agent-runtime-router-harness-closure-hardening.md` (archive purged in b8c007d)     |
| 2026-05-09 | 1.26.0  | CI/CD               | Added GitHub workflow role-matrix validation for the 8 active workflows, stable workflow/job names, role-scoped actions/script refs, and expected `.github/ABOUT.md` classifications.                                                                                                                                                                       | `docs/04.execution/archive/plans/2026-05-09-github-qa-role-matrix-hardening.md` (archive purged in b8c007d)                                   |
| 2026-05-09 | 1.25.0  | Script Governance   | Made `ws heal` diagnostic-only, added script inventory guardrails against `.env` mutation, and synchronized command documentation.                                                                                                                                                                                                                          | `docs/04.execution/archive/plans/2026-05-09-script-surface-audit-hardening.md` (archive purged in b8c007d)                                     |
| 2026-05-09 | 1.24.0  | Validation          | Enforced the root README template contract, added docs subfolder registry drift detection, removed the bundled optional fullstack starter footprint, and synchronized LLM-WIKI/template guidance.                                                                                                                                                           | `docs/04.execution/archive/plans/2026-05-09-project-template-readiness-agent-first-hardening.md` (archive purged in b8c007d) |
| 2026-05-09 | 1.23.0  | CI/CD               | Added concurrency coverage for tag/schedule/write workflows, removed CodeQL Actions autobuild, updated existing changelog PRs, and tightened `.github` metadata drift validation.                                                                                                                                                                           | `docs/04.execution/archive/plans/2026-05-09-github-gitflow-qa-cicd-followup-hardening.md` (archive purged in b8c007d)               |
| 2026-05-09 | 1.22.0  | Agent Harness       | Added the AI Agent-first Engineering contract, hardened active harness lifecycle, removed the Codex-only hook policy surface, and aligned dispatch/swarm coordination commands with ignored transient workspace state.                                                                                                                                      | `docs/04.execution/archive/plans/2026-05-09-harness-agent-first-engineering-hardening.md` (archive purged in b8c007d)               |
| 2026-05-08 | 1.21.0  | Agent Runtime       | Aligned root/provider routers, synchronized `.claude` and `.codex` agent surfaces, refreshed Stage 00 governance wording, and expanded agent-runtime drift validators.                                                                                                                                                                                      | `docs/04.execution/archive/plans/2026-05-08-agent-instruction-surface-alignment.md` (archive purged in b8c007d)                           |
| 2026-05-08 | 1.20.0  | CI/CD               | Classified GitHub workflows by gate type, moved CI-only agent checks into canonical validation, split changelog PR body rendering into a workflow helper, and strengthened GitHub validators.                                                                                                                                                               | `docs/04.execution/archive/plans/2026-05-08-github-gitflow-qa-cicd-hardening.md` (archive purged in b8c007d)                                 |
| 2026-05-08 | 1.19.0  | Script Governance   | Removed obsolete script wrappers, promoted useful direct helpers, and strengthened script inventory validation for direct commands and removed-script drift.                                                                                                                                                                                                | `docs/04.execution/archive/plans/2026-05-08-script-inventory-pruning.md` (archive purged in b8c007d)                                                 |
| 2026-05-08 | 1.18.0  | Validation          | Made `ws validate` the canonical local governance gate, classified scripts by use mode, simplified CI validation, and documented PyYAML as a prerequisite.                                                                                                                                                                                                  | `docs/04.execution/archive/plans/2026-05-08-validation-canon-script-governance-hardening.md` (archive purged in b8c007d)         |
| 2026-05-08 | 1.17.0  | CI/CD               | Consolidated duplicate governance workflow checks into template CI, aligned `.github` metadata with the minimal template, and added GitHub metadata drift validation.                                                                                                                                                                                       | `docs/04.execution/archive/plans/2026-05-08-github-template-governance-readiness.md` (archive purged in b8c007d)                         |
| 2026-05-07 | 1.16.0  | Script Governance   | Reconciled the active `ws` command surface with minimal governance scripts; moved optional stack/cloud scripts to examples and added script inventory drift validation.                                                                                                                                                                                     | `docs/04.execution/archive/plans/2026-05-07-script-governance-command-surface-hardening.md` (archive purged in b8c007d)           |
| 2026-05-07 | 1.15.0  | Governance          | Hardened the active repository as a minimal language-agnostic governance template; isolated the prior fullstack starter under examples and removed active stack-specific workflow/script assumptions.                                                                                                                                                       | `docs/04.execution/archive/plans/2026-05-07-minimal-governance-template-hardening.md` (archive purged in b8c007d)                       |
| 2026-05-07 | 1.14.2  | Agent Harness       | Integrated the Workspace Governance Automation Architect v3 contract into the existing workspace-governance skill, adding context priority, inventory, task groups, output contract, and done definition.                                                                                                                                                   | `docs/04.execution/archive/plans/2026-05-07-workspace-governance-automation-architect-v3.md` (archive purged in b8c007d)         |
| 2026-05-07 | 1.14.1  | Agent Harness       | Aligned unified workspace governance runtime mode contracts, success criteria, and active optional issue-linking / PR-target policy summaries.                                                                                                                                                                                                              | `docs/04.execution/archive/plans/2026-05-07-unified-workspace-governance-runtime.md` (archive purged in b8c007d)                         |
| 2026-05-07 | 1.14.0  | Agent Harness       | Added unified workspace governance runtime skill owned by Governance Architect; synchronized harness inventory, agent runtime docs, LLM-WIKI, and optional issue-linking policy summaries.                                                                                                                                                                  | `docs/04.execution/archive/plans/2026-05-07-unified-workspace-governance-runtime.md` (archive purged in b8c007d)                         |
| 2026-05-06 | 1.13.0  | CI/CD               | Fixed intelligence generation and web CI gates by adding deterministic repo intelligence artifacts, synchronizing the web lockfile, hardening the Next.js Docker build contract, and clarifying package-manager verification behavior.                                                                                                                      | `docs/04.execution/archive/plans/2026-05-06-github-actions-intelligence-web-remediation.md` (archive purged in b8c007d)           |
| 2026-05-06 | 1.12.0  | CI/CD               | Remediated GitHub Actions governance failures by aligning workspace validation taxonomy, repairing workflow validator pattern checks, and documenting the `ws` fallback gate.                                                                                                                                                                               | `docs/04.execution/archive/plans/2026-05-06-github-actions-governance-failure-remediation.md` (archive purged in b8c007d)       |
| 2026-05-06 | 1.11.0  | CI/CD               | Added GitHub workflow governance validator, hardened workflow job permissions/timeouts/action pinning, and enforced agent workflow validation before commit/push/PR.                                                                                                                                                                                        | `docs/04.execution/archive/plans/2026-05-06-github-actions-governance-hardening.md` (archive purged in b8c007d)                           |
| 2026-05-06 | 1.10.0  | CI/CD               | Replaced tag-triggered changelog direct push to `main` with a reviewed PR flow targeting `main`, preserving PR-only protected branch governance.                                                                                                                                                                                                            | `docs/04.execution/archive/plans/2026-05-06-changelog-pr-governance-fix.md` (archive purged in b8c007d)                                           |
| 2026-05-06 | 1.9.0   | CI/CD               | Added official CI/CD workflow governance rule and synchronized CI/CD policy across AGENTS.md, CLAUDE.md, GEMINI.md, and Stage 05 governance plan index.                                                                                                                                                                                                     | `docs/04.execution/archive/plans/2026-05-06-workspace-governance-plan.md` (archive purged in b8c007d)                                               |
| 2026-05-05 | 1.8.0   | Agent Harness       | Added `docs-governance.md` and `git-commit.md` agents; enriched `governance-architect.md` with mission, policy domains table, and collaboration links; registered new agents in `harness-library.md` and `persona.md`.                                                                                                                                      | —                                                                                                                                                                                              |
| 2026-05-05 | 1.7.0   | Git Policy          | Added hotfix branch strategy and PR merge strategy to `git-workflow.md`; added explicit Git section to `GEMINI.md`; synced LLM-WIKI §7 with hotfix and merge-strategy rules.                                                                                                                                                                                | —                                                                                                                                                                                              |
| 2026-05-05 | 1.6.0   | Governance          | Moved language-specific templates (GraphQL, Proto) to `99.templates/extended/`; deleted misplaced summary file from `04.execution/plans/`; added template classification policy and plan doc-type restriction.                                                                                                                                              | —                                                                                                                                                                                              |
| 2026-05-05 | 1.5.0   | Governance          | Added subfolder authorization policy (now Section 13), fixed phantom stage labels, repaired AGENTS.md duplicate sections, fixed SLO template frontmatter order, and brought 05.operations/runbooks README to standard.                                                                                                                                      | `docs/04.execution/archive/plans/2026-05-05-subfolder-policy.md` (archive purged in b8c007d)                                                                 |
| 2026-05-04 | 1.4.0   | Cleanup             | Removed tech-specific ADRs, fixed broken cross-links, unified legacy integration branch naming to `dev`, deleted non-portable plan files.                                                                                                                                                                                                                   | `docs/04.execution/archive/plans/2026-05-04-workspace-policy-alignment.md` (archive purged in b8c007d)                                             |
| 2026-05-04 | 1.1.0   | Hardening           | Standardized root shims (AGENTS.md/CLAUDE.md), enforced branch naming, and added automated governance checks.                                                                                                                                                                                                                                               | `docs/04.execution/archive/plans/2026-05-04-workspace-governance-hardening.md` (archive purged in b8c007d)                                     |
| 2026-05-04 | 1.2.0   | Productivity        | Implemented intelligent README indexing, TDD scaffolding, and automated environment setup.                                                                                                                                                                                                                                                                  | `docs/04.execution/archive/plans/2026-05-04-workspace-productivity-automation.md` (archive purged in b8c007d)                               |
| 2026-05-04 | 1.3.0   | Production          | Initialized Fullstack "Hello World" slots, modular CI/CD, and strict security gates.                                                                                                                                                                                                                                                                        | `docs/04.execution/archive/plans/2026-05-04-production-readiness-hardening.md` (archive purged in b8c007d)                                     |

## Change History

### v1.56.0 (2026-05-22) - Reuse Readiness Clarification

- **Derived-project reset**: Clarified that stage README skeletons and bootstrap-generated draft PRD intake seeds are the only new-project seed content, while `dev` non-README stage files remain template maintenance history unless separately migrated.
- **Runtime authority**: Kept `.claude/**` canonical, `.codex/**` compatibility-only, and `.agents/**` limited to the tracked Graphify helper allowlist; validator coverage rejects unapproved `.agents/**` files.
- **Graphify boundary**: Reworded Graphify usage as current, relevant supporting context that cannot override source files, Stage 00 governance, templates, or validators.
- **Template guidance**: Added target-relative link guidance to companion specification, operations, incident, SLO, runbook, session-memory, progress, and methodology templates.
- **Validation semantics**: Documented `validate-distribution` as expected to warn on `dev` maintenance history while remaining the blocking skeleton gate for `main` release-template promotion.

### v1.52.0 (2026-05-21) - Project-Template Reuse Readiness

- **Reuse boundary**: Strengthened root README, stage README indexes, and Stage 00 lifecycle guidance so `dev` maintenance history is visible as `active-template-contract`, `template-maintenance`, or `archive/reference`, not new-project seed content.
- **Runtime residue**: Kept `.claude/**` as canonical runtime, `.codex/agents/*.toml` as compatibility metadata, and expanded forbidden runtime validation to reject `.codex/hooks/**` and `.agents/skills/**`.
- **Template generation**: Aligned PRD, ARD, ADR, Plan, and Task template frontmatter with the generated-document rule that derived-project documents start as `status: draft`.
- **Validation**: Verified runtime contracts, doc readiness, doc governance, cross-links, canonical `ws validate`, bootstrap dry-run, and the expected `dev` failure for `validate-distribution`.

### v1.51.0 (2026-05-19) - Template Document Lifecycle and Bootstrap Seed Policy

- **Lifecycle rule**: Added `template-document-lifecycle.md` to classify reusable template contracts, dev maintenance history, archive/reference material, examples, remove candidates, and new-project seed documents.
- **Bootstrap seed**: Updated bootstrap to generate a draft PRD-shaped Stage 01 intake seed at `docs/01.requirements/YYYY-MM-DD-project-intake-prd.md`.
- **Router sync**: Aligned root/provider/runtime guidance so Graphify remains optional supporting context and `.agents` legacy guidance does not require a local user-global skill path.
- **Stack neutrality**: Reworded backend, QA, and operations scope examples so stack-specific tools apply only after derived-project intake declares them.

### v1.49.0 (2026-05-18) - Template Catalog and README Conformance

- **Template inventory generation**: Updated `scripts/docs/update-doc-readme-index.sh` so template README Documents tables use Purpose/H1-derived summaries or curated machine-readable summaries instead of intentional source placeholders such as `<string>` and `YYYY-MM-DD`.
- **Readiness validator coverage**: Added checks for uninitialized inventory cells only in `docs/99.templates/**/README.md` Documents tables and path-like Markdown link labels whose visible label disagrees with the href.
- **README conformance**: Added the short Docs 3 global rules reference block to governed README files while preserving local folder prose.
- **Evidence**: Recorded the follow-up spec, test strategy, plan, and task under `docs/03.specs/template-catalog-readme-conformance/` and `docs/04.execution/`.

### v1.48.0 (2026-05-17) - Script Usage Cleanup and QA Evidence Gate

- **QA evidence gate**: Added `scripts/qa/summarize-tdd-coverage.sh --fail-on-missing` and wired it into `bash scripts/ws.sh validate`; zero implementation tasks still pass, while implementation tasks without TDD evidence fail.
- **Script governance**: Clarified retained script categories, including `reserved-direct`, and tightened script inventory validation for category drift and canonical `ws swarm <task_id>` placeholder syntax.
- **Docs cleanup**: Deprecated stale ADR-0002 for the base template and aligned script inventory guidance in `scripts/README.md` and `docs/LLM-WIKI.md`.
- **Generated cache cleanup**: Removed ignored local `scripts/graphify-out/` residue from the workspace without deleting tracked scripts.

### v1.47.0 (2026-05-17) - Scripts, Runtime, and QA Scaffold Cleanup

- **Runtime boundary**: Removed the tracked `.codex/hooks.json` hook surface; `.codex/**` remains compatibility metadata only.
- **Hook contract**: Added an explicit timeout to the graphify `PreToolUse` hook in `.claude/settings.json`.
- **Swarm command surface**: Removed command-first `ws swarm` compatibility and tightened script inventory validation to reject stale command-first references.
- **QA scaffold**: Aligned `scaffold-tests-from-spec.sh` with `docs/03.specs/<feature-id>/spec.md` and sibling `tests.md`, preserving existing test strategies by failing on overwrite.

### v1.46.0 (2026-05-16) - Approved Prompt Package and Governance Cleanup

- **Prompt package controls**: Added `.agent-work/phase-gate.toml` for prompt-chain handoff state and `.agent-work/skill-map.md` for shared prompt skill discovery, with `skillify` recorded as a `GAP`.
- **Authority wording**: Clarified prompts 10-16 as plan-only in the normal pre-approval sequence and implementation-capable only when rerun after prompt 17 with the exact approval phrase recorded.
- **Provider and optional aids**: Documented root `GEMINI.md` as the Gemini entrypoint without a `.gemini/` policy directory, and updated Graphify wording so generated graph context remains optional and non-authoritative.
- **Docs and wiki cleanup**: Refreshed `docs/LLM-WIKI.md` prompt-control and generated-intelligence wording and synchronized Stage 90 freshness metadata.
- **Memory sync**: Updated active progress and methodology state through prompt 19 final verification; non-local and optional follow-up items remain carried in the final report.

### v1.43.0 (2026-05-12) - Hook Coverage Expansion and gitignore Consolidation

- **PostToolUseFailure hook**: Added `error-logger.sh` — non-blocking failure logger that appends to `_workspace/diagnostics/hook-errors.log`. Wired to `PostToolUseFailure/*` in `settings.json`. Provides per-session tool failure diagnostics without blocking agent execution.
- **PreCompact hook**: Added `pre-compact-context.sh` — saves branch, changed files, last 5 commits, and active task snippet to `_workspace/diagnostics/pre-compact-context.txt` before context compaction. Wired to `PreCompact` in `settings.json`. Preserves workspace state so sessions can resume with less re-investigation.
- **gitignore consolidation**: Replaced five `_workspace/<subdirectory>/` patterns with a single `_workspace/` entry, aligning the ignore contract with the memory note ("transient coordination state only under ignored `_workspace/**` paths").
- **Harness sync**: Updated `harness-library.md` Hook Inventory, `LLM-WIKI.md §4` Hook Runtime bullet and `§6.1` `ws hook` event list, and `.claude/CLAUDE.md` Hook Enforcement Catalog.
- **Uncovered events documented**: `UserPromptSubmit` (handled at user-global level), `PermissionRequest` (deny list in settings.json), `SessionEnd` (Stop covers final validation), `SubagentStop` (swarm lazy-load only) — documented as intentional non-wired events in harness-library.md Hook Inventory note.

### v1.42.0 (2026-05-12) - Governance Documentation Alignment

- **core-rules.md removal**: Absorbed the unique SDD (Structure-Driven Design) methodology rule into `agentic.md` Execute step; removed all references from `rules/README.md` Structure and Documents tables; deleted `core-rules.md`. Eliminates the commit-policy conflict ("Mandatory issue tracking reference" vs AGENTS.md "only when known").
- **Lazy-load documentation**: Added Section 5 "Lazy-Load Rule Files" to `harness-library.md` documenting that `evolution-protocol.md` and `swarm-protocol.md` are intentionally excluded from `bootstrap.md` Required Rule Files and their load triggers.
- **Archive trigger criteria**: Added "Archive Trigger Criteria" subsection to the execution archive README (archive subsequently purged in b8c007d) with three concrete conditions for moving plans/tasks to archive.
- **Progress tracking**: Updated `memory/progress.md` active task to `governance-doc-alignment` and preserved completed `workspace-gap-remediation` as previous task.
- **Validation**: `ws validate` 0 failures, 0 warnings confirmed after deletion.

### v1.41.0 (2026-05-12) - Agent Runtime Settings Remediation

- **python3 Permission**: Added `Bash(python3 scripts/:*)` to `settings.json` permissions.allow for scoped governance helper execution.
- **Hook Timeouts**: Added `timeout: 15` to PostToolUse `docs-readme-sync.sh` and `timeout: 60` to Stop `validate-doc-governance.sh` to prevent session hangs on slow filesystems.

### v1.40.0 (2026-05-10) - Agent Hook Event Dispatch

- **Portable Event Dispatch**: Added `scripts/harness/agent-hook-dispatch.py` and `ws hook <event> [matcher]` so local agent runtimes can execute configured command hooks by event.
- **Provider Boundary**: Kept `.claude/settings.json` and `.claude/hooks/**` canonical, kept `.codex/agents/*.toml` compatibility-only, and did not restore `.codex/hooks.json`.
- **Harness Sync**: Updated AGENTS, Claude, Gemini, Agent-first, harness, ADR, Stage 90, LLM-WIKI, and script inventory guidance so agents can discover the hook contract.
- **Validation**: Recorded hook smoke tests plus script inventory, docs readiness, docs governance, cross-link, security, and canonical `ws validate` evidence in the execution task.

### v1.39.0 (2026-05-10) - Hook Policy Hardening

- **Sensitive File Guardrail**: Extended pre-tool validation to `Read` and blocked agent access to credential files, private keys, shell history, auth files, and local log databases.
- **Secret Content Guardrail**: Added private-key content blocking alongside existing GitHub token literal checks.
- **Git Policy Hook**: Added `git-policy-enforce.sh` for PR template enforcement, protected branch push blocks, force-push blocks, protected branch deletion blocks, and `--no-verify` commit blocks.
- **Runtime Sync**: Replaced the inline docs README sync hook with a dedicated script that also handles `MultiEdit`, and changed session-start scope reporting to count actual scope files.

### v1.38.0 (2026-05-10) - LLM-WIKI Curator Runtime Closure

- **Dedicated Wiki Role**: Added `wiki-curator` as a narrow Sonnet specialist for `docs/LLM-WIKI.md` and the reviewed Stage 90 navigation index.
- **Navigation Index**: Added a former generated navigation helper and Stage 90 navigation artifact with explicit navigation-only authority boundaries. The `main` release skeleton no longer keeps that generated artifact.
- **Runtime Sync**: Updated harness inventory, persona mapping, model policy, LLM-WIKI, Stage 90 matrix, and Codex compatibility metadata to the 17/17/18 runtime count.
- **Validator Coverage**: Expanded active-surface stale checks for old 13-folder and compressed compact-docs path wording.

### v1.37.0 (2026-05-10) - Harness and Agent-first Closure Alignment

- **Security CI Artifact Contract**: Kept the short-retention Gitleaks report upload and aligned `ci-security.yml`, `.github/ABOUT.md`, CI/CD governance, and workflow role validation.
- **Compact Routing Cleanup**: Normalized active runtime references to `docs/LLM-WIKI.md` and corrected the operations stage rows in LLM-WIKI.
- **QA Ownership Guardrail**: Clarified that `tests.template.md` creates feature-local `docs/03.specs/<feature-id>/tests.md`, while execution plans own validation strategy and tasks own evidence.
- **Validator Coverage**: Expanded doc-readiness checks for LLM-WIKI stale references, compact legacy path drift, and QA test strategy ownership.

### v1.36.0 (2026-05-10) - Stage 00 Workflow Path Shorthand Boundary

- **Canonical Expansion**: Treat `00.agent-governance/sdlc-workflow.md` as docs-relative shorthand for `docs/00.agent-governance/sdlc-workflow.md` only.
- **Duplicate Authority Block**: Do not create root `00.agent-governance/` or use it as a separate workflow, policy, methodology, progress, or memory surface.
- **Validator Coverage**: Added readiness validation so root-level `00.agent-governance/sdlc-workflow.md` fails as duplicate workflow authority.

### v1.35.0 (2026-05-10) - External 00_System Workflow Boundary

- **Canonical Workflow Path**: Confirmed `docs/00.agent-governance/sdlc-workflow.md` is the Project-Template workflow reference.
- **External Path Boundary**: Confirmed `00_System/sdlc-workflow.md` is not a Project-Template governance path and must not be introduced as a duplicate authority surface.
- **Derived Workspace Rule**: If a derived or Vault-style workspace carries `00_System/sdlc-workflow.md`, it is downstream control-plane documentation and must defer to this Stage 00 docs contract.

### v1.34.0 (2026-05-10) - SDLC Workflow Boundary

- **Workflow Boundary**: Defined `docs/00.agent-governance/sdlc-workflow.md` as the stable human-agent collaboration flow and baton-passing reference.
- **Memory Separation**: Confirmed active progress, methodology state, and durable run notes remain under `docs/00.agent-governance/memory/`.
- **Policy Log Separation**: Confirmed versioned governance, SDLC protocol, runtime contract, and validator changes remain in this file.
- **Workspace Boundary**: Reaffirmed `_workspace/**` as transient runtime output only.

### v1.33.0 (2026-05-10) - Agent Memory and Runtime Workspace Boundary

- **Runtime Workspace Boundary**: Defined `_workspace/**` as transient coordination, generated diagnostics, generated intelligence, and local scratch output only.
- **Stage 00 Memory**: Made `docs/00.agent-governance/memory/` the canonical tracked home for active methodology, active progress, and durable agent memory.
- **Progress Template**: Added `docs/99.templates/progress.template.md` as the source template for `memory/progress.md`.
- **Policy Log Boundary**: Clarified that this file records versioned governance, SDLC protocol, runtime contract, and validator changes, not active task progress.

### v1.30.0 (2026-05-09) - Harness and Agent-first Evidence Closure

- **Evidence Scope**: Calibrated LLM-WIKI, Stage 90, and related Stage 06 records so validator-backed claims do not overstate TDD evidence, semantic parity, cross-stage traceability, or behavior preservation coverage.
- **Runtime Decision**: Added ADR 0004 for `.claude/**` canonical runtime, `.codex/agents/*.toml` compatibility-only metadata, removed `.codex/hooks.json`, and transient `ws dispatch` packets.
- **Validator Guardrails**: Added root/provider shim section-threshold enforcement and Stage 90 runtime count freshness validation.
- **Security Semantics**: Clarified that `validate-security.sh` enforces local lock-file and focused secret checks while optional inactive-stack SAST remains N/A or warning output.

### v1.29.0 (2026-05-09) - Agent-first Policy and Validator Alignment

- **Template Baseline**: Added doc-readiness validation for required canonical stage frontmatter, `## AI Execution Checklist`, and `## Related Documents`.
- **Legacy Handling**: Preserved existing source-history mismatches only through explicit content-hash baseline entries that fail when the file changes.
- **Policy Sync**: Updated documentation protocol and LLM-WIKI guidance so template requirements and validator behavior describe the same contract.
- **Evidence**: Recorded Stage 05/06 implementation evidence without adding agents, skills, workflows, application stacks, or a new `.codex` policy layer.

### v1.28.0 (2026-05-09) - Harness and Agent-first Component Matrix Hardening

- **Component Matrix**: Added a Stage 90 readiness matrix for Harness Engineering and AI Agent-first Engineering components.
- **Skill Inventory Guardrail**: Hardened `validate-skill-quality.sh` so the active `.claude/skills/*/skill.md` set must match skill entries registered in `harness-library.md`.
- **Runtime Sync**: Linked the matrix from LLM-WIKI, `agentic.md`, and `harness-library.md` without adding a new runtime layer.
- **Evidence**: Recorded Stage 05/06 implementation evidence and kept existing completed harness records as audit history.

### v1.27.0 (2026-05-09) - Agent Runtime Router and Harness Closure Hardening

- **Router Cleanup**: Replaced the removed security reminder hook reference with the active pre-tool and post-tool Claude hook surface plus CI/CD governance rule.
- **Stable References**: Replaced numbered `AGENTS.md` section references with stable section names and canonical harness/persona governance files.
- **Markdown Repair**: Fixed malformed inline spacing in the GitHub preflight checklist.
- **Validation**: Added doc-readiness stale-reference checks for the repaired runtime-router drift classes.

### v1.26.0 (2026-05-09) - GitHub QA Role Matrix Hardening

- **Role Matrix**: Added exact active workflow, workflow name, job id, job display name, allowed action, script-ref, and required marker validation for the 8 base-template workflows.
- **Metadata Classification**: Hardened `.github/ABOUT.md` validation so each workflow classification must match the expected role matrix.
- **Boundary**: Kept workflow YAML behavior unchanged; no new workflows, deployment gates, stack-specific CI, or GitHub-native AI instruction layer were added.
- **Validation**: Kept base-template placeholders valid in normal metadata validation and reserved owner/repo/security placeholder failures for `--strict-derived`.

### v1.25.0 (2026-05-09) - Script Surface Audit and Heal Hardening

- **Script Audit**: Confirmed active scripts are already inventoried and connected through `ws`, GitHub workflows, or documented direct commands.
- **Heal Contract**: Converted `ws heal` to diagnostic-only behavior so it reports `.env` drift without creating or modifying local environment files.
- **Validator Coverage**: Added script inventory guardrails that fail if `self-heal.sh` reintroduces `.env` copy, append, redirection, `tee`, `sed -i`, or move behavior.
- **Documentation Sync**: Updated script, reference, LLM-WIKI, and operations docs to describe `heal` as detect/report only.

### v1.24.0 (2026-05-09) - Project Template Readiness and Agent-first Hardening

- **README Contract**: Aligned the root README with `docs/99.templates/readme.template.md` and added readiness validation for required root sections.
- **Subfolder Registry**: Added doc-readiness validation for authorized `docs/` subfolders and clarified that tracked, non-empty local, and empty local-only unregistered directories are HALT conditions.
- **Template Footprint**: Removed the bundled optional fullstack starter footprint from the active baseline and updated active script/docs references so validators do not require it.
- **Guidance Sync**: Updated the README template and LLM-WIKI so agents use the same root README, subfolder enforcement, and template footprint contract.

### v1.23.0 (2026-05-09) - GitHub Git-Flow QA/CI/CD Follow-up Hardening

- **Workflow Concurrency**: Added top-level concurrency to release tag and scheduled repository automation workflows.
- **Security CI Alignment**: Removed the CodeQL autobuild step from GitHub Actions analysis because it is not a compiled-language scan.
- **Release Automation**: Updated changelog automation so existing open release PRs get refreshed with the current title and PR body.
- **Metadata Validation**: Hardened `.github` validators for exact workflow inventory coverage, SECURITY `main`/`dev` policy alignment, and unapproved duplicate GitHub surfaces.

### v1.22.0 (2026-05-09) - Harness and AI Agent-first Engineering Hardening

- **Agent-first Contract**: Added a Stage 00 operating contract for spec-first, persona-scoped, context-minimized, tool-contract, evidence-driven, guardrailed, and human-escalated work.
- **Harness Lifecycle**: Updated active harness governance so agent/skill changes keep `.claude`, `.codex`, persona mappings, Stage 00 README, LLM-WIKI, and validators synchronized.
- **Command Surface**: Converted `ws dispatch` into a transient dispatch packet generator and documented canonical `ws swarm` syntax.
- **Validation**: Added drift checks for hardcoded missing doc paths, Codex-only policy files, dispatch side effects, and machine-specific shared links.

### v1.21.0 (2026-05-08) - Agent Instruction Surface Alignment

- **Router Alignment**: Kept `AGENTS.md` as the balanced workspace contract while reducing `CLAUDE.md`, `GEMINI.md`, and `.claude/CLAUDE.md` to their runtime routing responsibilities.
- **Runtime Sync**: Treated `.claude/**` as canonical runtime and `.codex/**` as synchronized Codex compatibility metadata.
- **Governance Cleanup**: Replaced legacy plan/task marker wording with Stage 05 and Stage 06 artifact paths.
- **Validation**: Expanded doc-readiness and skill-quality checks to catch stale runtime and provider drift.

### v1.20.0 (2026-05-08) - GitHub Git-Flow QA/CI/CD Hardening

- **Workflow Classification**: Documented all active `.github/workflows/*.yml` files and separated QA/CI/CD gates from repository automation.
- **Ownership**: Added explicit CODEOWNERS coverage for GitHub workflows, gate helpers, workflow helper scripts, and workflow scanner config.
- **Validation Canon**: Moved agent scope and settings separation checks into `validate-skill-quality.sh` so `ws validate` remains the canonical CI gate.
- **Workflow Hardening**: Removed an unused diagnostics token env, added missing concurrency, and split changelog PR body rendering into `.github/scripts/render-changelog-pr-body.mjs`.
- **Validator Coverage**: Expanded GitHub workflow and metadata validators to catch branch-policy, permission, checkout credential, workflow coverage, and GitHub-native instruction-layer drift.

### v1.19.0 (2026-05-08) - Script Inventory Pruning

- **Script Pruning**: Removed obsolete direct wrappers that duplicated `ws bootstrap`, `ws intelligence`, or the canonical commit-message validator.
- **Direct Helpers**: Promoted Stage 06 TDD summary and commit-message validation helpers as documented `active-direct` commands.
- **Validation**: Strengthened script inventory validation to require all active `scripts/` files to be inventoried, active direct commands to be documented, and removed script names to stay out of active surfaces.

### v1.18.0 (2026-05-08) - Validation Canon & Script Governance Hardening

- **Canonical Gate**: Expanded `ws validate` to run docs, governance, links, script inventory, GitHub workflow/metadata, skill quality, architecture, and conditional dependency/container checks.
- **Script Roles**: Replaced the broad script `active` bucket with `active-ws`, `active-ci`, `active-direct`, `reserved-direct`, and `optional-example`.
- **CI Alignment**: Simplified template CI to call the canonical validation command and removed duplicate workspace validation from repository intelligence.
- **Agent Docs**: Synced root/provider routers to direct agents to `ws validate` as the final local gate.

### v1.17.0 (2026-05-08) - GitHub Template Governance Readiness

- **Metadata Alignment**: Rewrote `.github` summaries, labels, CODEOWNERS paths, issue template paths, and PR coverage wording for minimal governance.
- **Workflow Consolidation**: Folded duplicate governance checks into `ci-global.yml` and kept security/intelligence workflows aligned with `main` and `dev`.
- **Validation**: Added `scripts/validation/validate-github-metadata.py` and wired it into workspace and CI validation.
- **Agent Docs**: Synced root/provider routers and governance rules with the new GitHub metadata gate.

### v1.16.0 (2026-05-07) - Script Governance Command Surface Hardening

- **Command Surface**: Kept active `ws` commands limited to governance, docs, validation, inventory, bootstrap, dispatch, swarm, and repository intelligence.
- **Example Isolation**: Moved optional package, K3S, chaos, cost, and speculative orchestration helpers under `examples/fullstack-starter/scripts/`.
- **Validation**: Added script inventory drift validation to local and CI gates.
- **Agent Docs**: Synced active command references and stack-neutral runtime wording.

### v1.15.0 (2026-05-07) - Minimal Governance Template Hardening

- **Template Core**: Aligned active root documentation with the language-agnostic governance template identity.
- **Example Isolation**: Moved the previous fullstack starter profile under `examples/fullstack-starter/`.
- **Workflow Boundary**: Removed active stack-specific app/deploy workflows from `.github/workflows/`.
- **Script Governance**: Reconciled `ws` help/routes with scripts that actually exist.

### v1.14.2 (2026-05-07) - Workspace Governance Automation Architect v3

- **Runtime Contract**: Added context priority, non-negotiables, inventory checklist, task groups, output contract, and done definition to `workspace-governance/skill.md`.
- **Ownership**: Kept ownership with `governance-architect`; no duplicate agent was added.
- **Boundary**: Kept active `dev` branch policy, optional issue linking, conditional stack gates, and no new workflows/scripts/folders.

### v1.14.1 (2026-05-07) - Unified Governance Runtime Alignment

- **Mode Contracts**: Added compact input, output, and success criteria rules to `workspace-governance/skill.md`.
- **Policy Summary**: Reaffirmed optional issue linking and PR-only targeting for `dev` or `main` according to branch policy.
- **Boundary**: Kept unified governance as a skill owned by `governance-architect`; no duplicate agent or extra workflow automation was added.

### v1.14.0 (2026-05-07) - Unified Workspace Governance Runtime

- **Runtime Skill**: Added `.claude/skills/workspace-governance/skill.md` as the mode-based governance orchestration entry point.
- **Ownership**: Kept ownership with `governance-architect`; no duplicate workspace-governance agent was added.
- **Policy Sync**: Updated harness inventory, governance README, LLM-WIKI, and optional issue-linking summaries.
- **Boundary**: Kept example AI review, issue triage, rebase, rollback, and branch cleanup workflows out of active CI.

### v1.13.0 (2026-05-06) - GitHub Actions Intelligence Web Remediation

- **Intelligence**: Added deterministic offline `scripts/generation/generate-repo-intelligence.py` for `ws.sh intelligence`.
- **Web Gate**: Pinned web dependencies, regenerated `package-lock.json`, and added a minimal Next.js app shell.
- **Docker Build**: Rebuilt `web/Dockerfile` around `npm ci`, `npm run build`, and standalone Next.js artifacts.
- **Agent Gate**: Added scoped evidence requirements for intelligence, package-lock, web build, and Docker changes.

### v1.12.0 (2026-05-06) - GitHub Actions Governance Failure Remediation

- **Workspace Validation**: Updated architecture validation from legacy `02.research` and `10.post-launch` folders to canonical `02.architecture/requirements` and `05.operations/incidents`.
- **Workflow Validator**: Repaired protected branch push and auto-merge regex checks.
- **Agent Gate**: Documented `bash scripts/ws.sh validate` as the fallback when the `ws` binary is not available.

### v1.11.0 (2026-05-06) - GitHub Actions Governance Hardening

- **Workflow Validator**: Added `scripts/validation/validate-github-workflows.py` and wired it into `governance-check.yml`.
- **Workflow Hardening**: Added job-level permissions and timeouts, pinned remaining third-party actions, and repaired stale workflow references.
- **Agent Gate**: Updated root/provider routers to require workflow, governance, and link validation before commit, push, or PR.

### v1.10.0 (2026-05-06) - Changelog PR Governance Fix

- **Workflow Safety**: Replaced `generate-changelog.yml` direct push to `main` with generated-branch PR creation.
- **Protected Branch Policy**: Preserved reviewed PR-only updates for `main` while keeping release-tag changelog generation.
- **Traceability**: Added a Stage 05 plan record for the CI/CD governance fix.

### v1.9.0 (2026-05-06) - CI/CD Governance Synchronization

- **CI/CD Rule**: Added `rules/ci-cd-workflow.md` as the official branch-based workflow governance policy.
- **Root Router Sync**: Updated `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` with CI/CD workflow governance references.
- **Plan Index**: Added the workspace governance orchestration plan to the Stage 05 README.

### v1.5.0 (2026-05-05) - Docs Structure & Governance Hardening

- **Subfolder Policy**: Added `documentation-protocol.md` subfolder registry, addition procedure, and HALT condition.
- **LLM-WIKI Sync**: Added subfolder policy summary to LLM-WIKI Section 1.
- **Phantom Stage Labels**: Removed "Stage 11/12/13" H1 headers from migrated subdirectory READMEs; replaced with actual document titles.
- **Empty Directory**: Deleted the empty governance experts folder (0 files).
- **AGENTS.md**: Fixed duplicate section 5 numbering; removed broken `experts/` reference; removed non-existent `KNOWLEDGE_HUB.md` link; renumbered Expert Toolkits as section 6.
- **05.operations/runbooks README**: Rebuilt from 24 lines to 76 lines with full lifecycle, template, cross-reference, and checklist coverage.
- **SLO Template**: Moved H1 after frontmatter block to comply with YAML frontmatter parsing rules.
- **Templates Index**: Marked `service.template.proto` as optional in `99.templates/README.md`.

### v1.3.0 (2026-05-04) - Production Readiness & Security

- **Fullstack Slots**: Initialized `web/` (Next.js), `server/` (FastAPI), and `app/` (Flutter) with minimal "Hello World" boilerplate.
- **Security Gate**: Implemented `validate-security.sh` with a "Fail-on-any-warning" policy.
- **Modular CI**: Split CI workflows into `ci-web.yml`, `ci-server.yml`, and `ci-security.yml`.
- **Observability**: Added SLO templates and base Monitoring configurations.

### v1.2.0 (2026-05-04) - Productivity & Automation

- **README Indexer**: Upgraded `update-doc-readme-index.sh` to parse YAML frontmatter for status and dates.
- **TDD Scaffolding**: Added `scaffold-tests-from-spec.sh` to automate `docs/03.specs/<feature-id>/tests.md` creation.
- **Environment Setup**: Added `setup-environment.sh` for linter installation.
- **LLM-WIKI**: Integrated automated validation script documentation.

### v1.1.0 (2026-05-04) - Workspace Hardening

- **Root Shims**: Promoted `AGENTS.md` to SSOT; aligned `CLAUDE.md` and `GEMINI.md`.
- **Validation**: Added `validate-doc-governance.sh` with 10 strict checks.
- **Protocol**: Mandated atomic conventional commits and PR-only development.
- **Templates**: Hardened ARD and Spec templates with mandatory architecture sections.
