# LLM-Wiki: video-analysis SDLC Governance

> **AI Agent Context File**: This is the canonical reference for workspace policies. This document synthesizes the entire workspace structure, SDLC implementation details, and governance constraints into a single, high-density format optimized for LLMs. Read this file to understand how to operate within this repository.
>
> **Authority boundary**: `docs/LLM-WIKI.md` is the canonical operating summary for AI agents. `docs/90.references/` is a release-template reference skeleton on `main`; it must not contain generated navigation or template-history documents.

## 1. Workspace Architecture & Stage-Gate Flow

This language-agnostic project template enforces a strict **Stage-Gate SDLC** (Software Development Life Cycle) model. It is a template workspace for starting new product/software projects, not a completed application or project-history archive. It defines reusable governance, documentation, workflow, CI/CD, quality-gate, template, and operations structure without enforcing a default application stack.

Derived projects must complete product/software and stack intake first, then rewrite the relevant skeleton README files and create project-specific documents under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/`.

| Stage  | Path                                 | Purpose                                | Template Used                                                                                                                                   | AI Hard Stop Condition                                        |
| :----- | :----------------------------------- | :------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| **00** | `docs/00.agent-governance/`          | Rules, scopes, and personas            | N/A                                                                                                                                             | Stop if root routers or bootstrap rules are missing           |
| **01** | `docs/01.requirements/`              | Product Intent                         | `prd.template.md`                                                                                                                               | Scope/AC missing OR non-TDD-mappable AC                       |
| **02** | `docs/02.architecture/requirements/` | Architecture Blueprint                 | `ard.template.md`                                                                                                                               | DDD triggers not evaluated OR missing mandatory C4 diagrams   |
| **03** | `docs/02.architecture/decisions/`    | Decision Records                       | `adr.template.md`                                                                                                                               | Alternative rationale missing                                 |
| **04** | `docs/03.specs/`                     | Tech Specs                             | `spec.template.md` + supplementary: `api-spec`, `tactical-model` (expanded), `domain-model`/`domain-events` (expanded), `tests`, `openapi.yaml` | SDD sequence missing for 3+ components OR TDD mapping missing |
| **05** | `docs/04.execution/plans/`           | Execution Plan                         | `plan.template.md`                                                                                                                              | Validation plan missing OR non-runnable commands              |
| **06** | `docs/04.execution/tasks/`           | Work Tracking                          | `task.template.md`                                                                                                                              | TDD Evidence missing OR empty logs                            |
| **07** | `docs/05.operations/guides/`         | Human-readable usage and how-to guides | `guide.template.md`                                                                                                                             | Stable behavior or audience/prerequisites missing             |
| **08** | `docs/05.operations/policies/`       | Operational policies and controls      | `operation.template.md`, `slo.template.md`                                                                                                      | SLO, controls, ownership, or promotion criteria missing       |
| **09** | `docs/05.operations/runbooks/`       | Executable operational procedures      | `runbook.template.md`                                                                                                                           | Diagnosis, mitigation, rollback, or escalation steps missing  |
| **10** | `docs/05.operations/incidents/`      | Incident records and postmortems       | `incident.template.md`, `postmortem.template.md`                                                                                                | Impact, timeline, actions, or postmortem decision missing     |

- **Naming Conventions**: Use `YYYY-MM-DD-<slug>.md` (time-bound) or `####-<slug>.md` (sequenced).
- **Lifecycle Rules**: Documents transition through `draft` -> `active` -> `completed` -> `deprecated` via frontmatter. Standard rules are defined in every folder README. Consolidate, deprecate, archive, or remove obsolete files with justification and reference cleanup.
- **Cross-Reference Rules**: Every stage document MUST link to upstream/downstream dependencies in `## Related Documents`. Every folder README enforces these rules via a dedicated section.
- **Templates**: All `docs/99.templates/*.md` enforce unified frontmatter (`title`, `version`, `owner`, `status`). Core templates are technology-agnostic (markdown + yaml only).
- **Stage Template Enforcement**: Non-README documents under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/` must match the stage-specific template contract from `docs/99.templates/`. Agents must halt if the template is missing or the document would fail required template markers.
- **Extended Templates**: `docs/99.templates/extended/` holds optional technology-specific templates (GraphQL, gRPC/Proto). Use only when the target project adopts that technology. **Do not treat as required.**
- **Memory Templates**: `progress.template.md` owns `docs/00.agent-governance/memory/progress.md` active progress tracking, `methodology.template.md` owns active methodology state, and `session-memory.template.md` owns dated durable memory notes. `expanded/tactical-model.template.md` covers both domain and data modeling.
- **Project Intake Gate**: Derived projects must collect product/software intent, stack, data/security constraints, and operations baseline before authoring PRD, ARD, ADR, spec, plan, task, operations, or reference documents.
- **Template Document Lifecycle**: Use `docs/00.agent-governance/rules/template-document-lifecycle.md` to classify inherited documents as `project-seed`, `template-maintenance`, `active-template-contract`, `archive/reference`, `example`, or `remove-candidate` before moving, deleting, or reusing them.
- **Environment Readiness**: Use `docs/00.agent-governance/rules/environment-readiness.md` before changing setup, validation prerequisites, local tooling assumptions, or runtime readiness policy. Core governance runtime prerequisites are `git`, `bash`, `python3`, `rg`, and the Python `yaml` module; `gh`, docs/lint, security, and stack runtimes are optional or conditional unless the task or derived-project intake requires them.
- **Release Process**: Use `docs/00.agent-governance/rules/release-process.md` before preparing a `dev` to `main` release-template PR. `validate-distribution` must pass on the prepared release skeleton, even though it is expected to fail on raw `dev` while maintenance history remains present.
- **Template Footprint**: New or modified non-README stage documents in `docs/01.requirements/` through `docs/05.operations/incidents/` and `docs/90.references/` must include required frontmatter, `## AI Execution Checklist`, and `## Related Documents`. On `main`, those project-content folders contain README skeleton guides only.
- **README Contract**: Every allowed top-level docs folder must include purpose/scope, in-scope and out-of-scope boundaries, mandatory template mapping, naming/lifecycle/cross-reference rules, usage examples, the Documents index, AI authoring guidance, and related documents.
- **Root README Contract**: The repository root README must follow `docs/99.templates/readme.template.md` by including overview, audience, scope, structure, work instructions, and related documents. Stack-neutral template roots omit tech-stack placeholders until a derived project adopts an implementation stack.
- **Release Skeleton README Contract**: README files under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/` follow `docs/99.templates/readme.template.md` Base Structure plus stage-specific governance sections. They explain that the base template is a starting workspace and that derived projects must replace skeleton guidance with project-specific content.
- **Supporting README Contract**: `docs/README.md`, `scripts/README.md`, and approved nested README files must include the base README sections. Supporting README files under `docs/` must keep `Documents` tables synchronized with actual child files and folders, including `.yaml`, `.yml`, `.graphql`, and `.proto` templates when present. YAML metadata blocks in README files must start at line 1.
- **Plan Doc-Type Rule**: `docs/04.execution/plans/` accepts only `plan.template.md`-derived documents. Summary or retrospective records belong in `docs/05.operations/guides/`.
- **Subfolder Policy**: Subfolders within `docs/` stage folders are permitted only when listed in `documentation-protocol.md` Section 13. Authorized subfolders include `00.agent-governance/{rules,scopes,providers,memory,compliance,data-governance}`, `02.architecture/requirements/`, `02.architecture/decisions/`, `03.specs/<feature-id>/`, `04.execution/{plans,tasks}/`, `05.operations/{guides,policies,runbooks,incidents}/`, and `99.templates/{expanded,extended}/`. **HALT** if an unlisted subfolder is found, including tracked, non-empty local, or empty local-only directories.

## 2. Methodology Integration (TDD, SDD, DDD)

### TDD (Test-Driven Development)

- **Rule**: RED-GREEN-REFACTOR evidence is **mandatory** for all implementation (`impl`) tasks.
- **Spec Gate**: `docs/03.specs/<feature-id>/tests.md` must be created at Stage 04 and linked in the TDD Readiness table.
- **Task Gate**: Execution tasks in `docs/04.execution/tasks/` cannot be closed without specific, non-empty test execution logs.

### SDD (System Design Document)

- **Rule**: Mermaid `sequenceDiagram` is **mandatory** for any flow with 3+ components.
- **State Rule**: `stateDiagram-v2` is required when lifecycle or state transitions affect correctness.
- **Enforcement**: Validated during Stage 04 (`docs/03.specs/`).

### DDD (Domain-Driven Design)

- **Rule**: Every ARD must evaluate the `DDD Trigger Condition`.
- **Strategic**: Populate Bounded Context and Ubiquitous Language overlays in Stage 02.
- **Tactical**: Populate Domain Model/Events overlays in Stage 04 if triggers fire.

## 3. DESIGN.md (Single Source of Truth)

- **SSOT**: Root `DESIGN.md` is the SOT for all UI/Frontend/Mobile/App visual design.
- **Project Rule**: For the `video-analysis` itself, `version` and `name` are `<string>`.
- **AI HARD STOP**: If `version` or `name` is `<string>`, **HALT** any UI/frontend work (Stage 04/06) and request design system definition.

## 4. Agent Governance & Runtime

- **Bootstrap**: Load `docs/00.agent-governance/rules/bootstrap.md` first.
- **Routers**: Root `AGENTS.md` is the balanced workspace contract; provider `CLAUDE.md` / `GEMINI.md` files are overlays.
- **Agent Instructions**: `docs/00.agent-governance/` and `.claude/agents/*.md` define canonical agent runtime behavior. `.codex/agents/*.toml` is a compatibility metadata view, not an independent policy layer; it may include copied instruction text for Codex consumption, but policy authority remains `.claude/**` and Stage 00. Structure: Mission (optional), Role definition, Procedure, Constraints, Collaboration, File references.
- **Gemini Runtime Boundary**: Root `GEMINI.md` is the checked-in Gemini entrypoint. The workspace intentionally does not use `.gemini/` as an independent policy directory unless a future provider-specific runtime need is approved.
- **Prompt Package Controls**: `.agent-work/phase-gate.toml` records prompt-chain state and approval handoff, while `.agent-work/skill-map.md` records local discovery for the shared prompt skill list and missing exact prompt skills. These are handoff aids under `.agent-work/`; they do not override Stage 00 governance, root routers, provider runtime settings, or the active prompt.
- **Optional Generated Intelligence**: Graphify output under `graphify-out/` is optional generated context. Use it only when present, current, and relevant; it must not override source inspection, Stage 00 governance, root routers, templates, validators, or current workspace evidence.
- **AI Agent-first Engineering**: `docs/00.agent-governance/rules/agentic.md` maps intake-first, spec-first, persona-scoped, context-minimized, tool-contract, evidence-driven, guardrailed, and human-escalated work to the requirements-through-execution flow. Harness inventory is owned by `docs/00.agent-governance/rules/harness-library.md`.
- **Harness Inventory**: 17 active agents in `.claude/agents/`, 17 compatibility metadata files in `.codex/agents/`, and 18 active runtime skills in `.claude/skills/`. Canonical registry: `docs/00.agent-governance/rules/harness-library.md`. Adding an agent requires updating harness-library.md, persona.md, Stage 00 README, LLM-WIKI, validators, and Codex compatibility metadata; adding a skill requires updating harness-library.md and governance indexes. Active skill inventory parity and Codex name/schema/description/scope-marker compatibility are enforced by `bash scripts/validation/validate-skill-quality.sh`; semantic body equivalence requires manual review.
- **Hook Runtime**: `.claude/settings.json` is the canonical hook event configuration and `.claude/hooks/**` is the canonical hook implementation surface. Claude Code consumes those hooks directly; Codex and other local agents use `bash scripts/ws.sh hook <event> [matcher]` to run the same command hooks. Provider-neutral replay accepts Claude-style hook JSON on stdin and maps `CODEX_TOOL_*` env vars before running canonical hooks, so Codex can trigger the same pending stage-template write gate. Runtime hook/settings contract shape, dispatcher portability, required document-readiness hook commands, prohibited policy surfaces, and the tracked `.agents/**` legacy helper allowlist are validated by `python3 scripts/validation/validate-runtime-contracts.py`. Do not restore `.codex/hooks.json`, `.codex/hooks/**`, `.agents/skills/**`, unapproved `.agents/**` policy files, or GitHub-native AI instruction files for hook policy. Active wired events: `SessionStart` (context injection), `PreToolUse` (git policy, file safety, forbidden runtime policy surfaces, unsafe workflow pattern blocks, and pending stage-template write gate), `PostToolUse` (README sync, safe formatting, and governance/template-readiness validation, including repository-level readiness when provider-neutral replay has no target file), `PostToolUseFailure` (non-blocking error log to `_workspace/diagnostics/`), `PreCompact` (workspace snapshot to `_workspace/diagnostics/`), `Stop` (doc-governance, template-readiness, and dirty-tree completion gate).
- **Governance Policy Domains**: Enforced by `@governance-architect`.
  - docs/ folder structure → `rules/documentation-protocol.md`
  - Template usage → `docs/99.templates/` (mandatory for all stage docs)
  - Template document ownership → `rules/template-document-lifecycle.md`
  - Agent instruction sections → `AGENTS.md` balanced router contract
  - Git workflow → `rules/git-workflow.md`
  - CI/CD workflow governance → `rules/ci-cd-workflow.md`
  - Harness inventory → `rules/harness-library.md`
- **Meta Agents (Stage 00)**:
  - `governance-architect`: Workspace policy owner. Maintains root routers, rules, scopes, harness inventory.
  - `docs-governance`: Documentation & template governance. Enforces docs/ structure; integrates with `doc-governance/skill.md`.
  - `git-commit`: Commit & PR message generator. Outputs Conventional Commit messages from grouped changes.
- **Wiki Agent (Stage 90)**:
  - `wiki-curator`: Maintains `docs/LLM-WIKI.md` without deciding policy, changing templates, restructuring docs, or recreating generated Stage 90 indexes on `main`.
- **Skills**: Use `spec-driven-sdlc` for end-to-end SDLC orchestration. Use `workspace-governance` for mode-based governance planning, execution, inventory, automation architecture, validation, and commit-runtime message generation.
- **Methodology and Progress Memory**: `docs/00.agent-governance/memory/methodology.md` defines the active methodology run state (Scrum, Lean, Kanban, Hybrid), and `docs/00.agent-governance/memory/progress.md` records active task progress, handoffs, blockers, and durable run notes. `_workspace/**` is transient and cannot override Stage 00 memory or governance.
- **Policy Change Log Boundary**: `docs/00.agent-governance/policy-change-log.md` records versioned governance, SDLC protocol, runtime contract, and validator changes. It is not active progress or methodology memory.
- **SDLC Workflow Boundary**: `docs/00.agent-governance/sdlc-workflow.md` records the stable human-agent collaboration flow and baton-passing model. It is not active progress, methodology state, policy history, or `_workspace/**` output.
- **SDLC Workflow Path Shorthand**: `00.agent-governance/sdlc-workflow.md` without a `docs/` prefix is docs-relative shorthand only. Do not create root `00.agent-governance/` or treat it as a separate governance surface.

## 5. Validation & CI/CD

- **Canonical Local Gate**: `bash scripts/ws.sh validate` is the authoritative local validation entrypoint before commit, push, or PR.
- **Environment Report**: `bash scripts/ws.sh setup` reports core, optional, and stack-conditional local prerequisites without installing tools or mutating local configuration.
- **Linting & Formatting**: `bash scripts/validation/validate-docs.sh` verifies markdown, YAML, and bash script formatting and is run by the canonical gate.
- **Template Schema**: `bash scripts/validation/validate-docs.sh` also verifies frontmatter across `99.templates/` and lifecycle rules in folder READMEs.
- **Governance Audit**: `bash scripts/validation/validate-doc-governance.sh` — checks the 8-folder compact policy, DESIGN placeholder state, root/provider shim section-size heuristic, mandatory Git keywords in agent routers, and required Stage README sections. It does not prove complete TDD evidence or full cross-stage traceability.
- **Doc Readiness**: `python3 scripts/validation/validate-doc-readiness.py` — checks canonical docs folders, root README contract, stage and supporting README contracts, nested README index coverage, stage-specific template conformance, machine-readable spec contract markers, template inventory, docs subfolder registry drift, active-surface stale references through `STALE_SCAN_PATHS`, runtime-router stale references, Stage 00 rule coverage, hardcoded doc paths, QA test strategy ownership, and Codex compatibility-only surface rules.
- **Distribution Validation**: `bash scripts/ws.sh validate-distribution` or `TEMPLATE_DISTRIBUTION=1 bash scripts/validation/validate-template-distribution.sh` checks that `main` release-template stage folders contain only the allowed README skeleton guides and that those README files follow the required template-based skeleton sections.
- **Cross-Link Validation**: `bash scripts/validation/validate-cross-links.sh` — detects broken internal links.
- **Path Portability**: `python3 scripts/validation/validate-path-portability.py` — warning-only check for repository path length, segment length, spaces, and Windows-reserved characters.
- **Code Style Validation**: `bash scripts/validation/validate-code-style.sh` — checks whitespace, line endings, and configured style hooks without declaring a default application stack.
- **Design Check**: `bash scripts/validation/validate-design-initialization.sh`
- **Script Inventory**: `python3 scripts/validation/validate-script-inventory.py` keeps active `ws` commands, script role categories, direct helper commands, `scripts/README.md`, retention basis markers, and removed-script references aligned. Valid retention categories are `active-ws`, `active-ci`, `active-direct`, `reserved-direct`, and `optional-example`. A tracked script is retained only when it has a `ws` consumer, CI consumer, documented direct governance use, reserved direct use, or derived-project conditional value.
- **GitHub Metadata**: `python3 scripts/validation/validate-github-metadata.py` keeps `.github` metadata, templates, labeler paths, CODEOWNERS, workflow role classifications, and conditional 90% PR coverage wording aligned with the template. Use `--strict-derived` after bootstrap to fail unresolved owner/repo/security placeholders.
- **Coverage Gate**: every PR must pass `.github/gates/check-coverage.sh` with a parseable coverage artifact and at least 90% line coverage after an active implementation stack manifest exists. The base template may skip only when no active stack manifest is present.
- **Workflow Governance**: `docs/00.agent-governance/rules/ci-cd-workflow.md` defines branch-based GitHub Actions gates, `dev` to `main` template promotion, workflow role-matrix ownership, and workflow safety hard stops.
- **Security Validation Semantics**: `bash scripts/ws.sh validate` runs the canonical local governance gate and conditional dependency/container audits. `bash scripts/ci/validate-security.sh` is an explicit local or Security CI gate for lock-file policy, focused hardcoded-secret checks with sanitized location/count output, changed governance/runtime files except the validator itself, short-retention Gitleaks report artifact upload in Security CI, and optional SAST when active stack tooling exists; inactive stacks or missing optional SAST tooling are reported as N/A/warnings, not as proof of coverage. Changes to `scripts/ci/validate-security.sh` require separate diff and syntax evidence.
- **Promotion Gate**: active workflows validate template governance, docs, workflow YAML, security, conditional coverage, and cross-links before promotion PRs. Application deployment workflows belong in derived projects, not the base template.
- **Concurrency**: active governance workflows use explicit concurrency only when duplicate runs would create stale validation results.
- **Change Type and WIP Evidence**: PRs and CI evidence distinguish `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, and `chore` work. Incomplete but valuable checkpoints must record WIP state in the governed task/progress surface or PR body and must not be promoted as completed work.
- **Evidence**: All stage transitions require verifiable evidence (logs, links, or command outputs).
- **Optional Starters**: The base template no longer tracks a bundled fullstack starter profile. Active workflows, script inventory, and validation gates must not require `examples/fullstack-starter/**`.

## 6. Automated Validation Procedures

Agents SHOULD run `bash scripts/ws.sh validate` before finalizing any stage document or code change. The following scripts are the component gates run by the canonical command or used for scoped validation.

| Script                                                         | Purpose                                                                                                                                                             |
| :------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `bash scripts/ws.sh validate`                                  | Canonical local gate for docs, governance, links, scripts, GitHub workflow/metadata, runtime contracts, skill quality, TDD evidence, architecture, and conditional audits. |
| `bash scripts/ws.sh hook <event> [matcher]`                    | Runs configured `.claude/settings.json` command hooks for Claude, Codex, and other local agent runtimes.                                                            |
| `bash scripts/validation/validate-docs.sh`                                | General markdown/YAML linting and frontmatter checks.                                                                                                               |
| `bash scripts/validation/validate-doc-governance.sh`                      | Checks 8-folder compact policy, DESIGN placeholders, shim section-size heuristic, mandatory Git router keywords, and Stage README sections.                         |
| `bash scripts/validation/validate-cross-links.sh`                         | Detects broken relative links across the entire `docs/` suite.                                                                                                      |
| `python3 scripts/validation/validate-path-portability.py`                  | Emits advisory warnings for repository paths that exceed portability budgets or use Windows-hostile naming.                                                         |
| `bash scripts/validation/validate-code-style.sh`                           | Validates whitespace, line endings, and configured style hooks without introducing a default application stack.                                                      |
| `bash scripts/validation/validate-design-initialization.sh`               | Enforces the DESIGN.md hard-stop rule for frontend tasks.                                                                                                           |
| `bash scripts/ci/validate-security.sh`                            | Explicit local/Security CI gate for lock-file policy, focused secret scans with sanitized output, changed governance/runtime files, and optional active-stack SAST. |
| `python3 scripts/validation/validate-script-inventory.py`                 | Verifies active script inventory, retention basis markers, direct-command coverage, and stale `ws` command references.                                              |
| `python3 scripts/validation/validate-github-workflows.py`                 | Verifies GitHub Actions permissions, timeouts, protected-branch safety, action pinning, role matrix ownership, and script references.                               |
| `python3 scripts/validation/validate-github-metadata.py`                  | Verifies non-workflow GitHub metadata stays stack-neutral, path-accurate, and aligned to expected workflow classifications.                                         |
| `python3 scripts/validation/validate-github-metadata.py --strict-derived` | Verifies bootstrapped projects have replaced required owner/repo/security/CODEOWNERS placeholders.                                                                  |
| `python3 scripts/validation/validate-runtime-contracts.py`                | Verifies `.claude/settings.json` hook contract shape, required doc-readiness hook commands, referenced repo-local hook files, prohibited policy surfaces, and local settings separation. |
| `python3 scripts/validation/validate-stage-template-write.py`             | Validates pending hook write input against the matching `docs/99.templates` contract before governed stage documents are written.                                  |
| `python3 scripts/validation/validate-version-drift.py`                    | Checks version drift for active stack manifests only when root stack directories are tracked or non-empty.                                                          |
| `bash scripts/validation/validate-commit-msg.sh <file>`                   | Validates one commit message file against the repository Conventional Commit policy.                                                                                |
| `bash scripts/qa/summarize-tdd-coverage.sh [--fail-on-missing] [--tasks-dir <path>]` | Summarizes execution task TDD evidence; `--fail-on-missing` fails when implementation tasks lack evidence.                                      |

## 6.1 Active Workspace Commands

Use `bash scripts/ws.sh help` as the source of truth. Active commands are `setup`, `validate`, `validate-derived`, `validate-distribution`, `audit`, `heal`, `info`, `docs`, `hook`, `sbom`, `intelligence`, `dispatch`, `swarm`, `bootstrap`, and `help`.

- `dispatch`: creates an ignored transient dispatch packet under `_workspace/dispatch/`; it does not create branches or scaffold execution task documents.
- `heal`: reports local workspace consistency issues only; it must not create or modify `.env` or other repository files.
- `hook`: runs configured `.claude/settings.json` command hooks by event and matcher. Use `bash scripts/ws.sh hook <SessionStart|PreToolUse|PostToolUse|PostToolUseFailure|PreCompact|Stop> [matcher]`.
- `setup`: reports core governance runtime, review/publishing, docs/lint, security, and stack-conditional prerequisite status without installing tools or mutating the workspace.
- `swarm`: uses `bash scripts/ws.sh swarm <task_id> <start|status|handoff|suggest> [next_role]` as the canonical syntax and stores ignored transient state under `_workspace/swarm/`.

`_workspace/**` is local runtime output only. Promote durable findings into `docs/00.agent-governance/memory/` or the owning governed stage document before citing them as authority.

## 7. Git Workflow & Commit Policy

- **git-flow**: Strategy using `main` (production) and `dev` (integration).
- **1-commit-1-change**: 1 commit = 1 logical feature, bugfix, or refactor. Atomic and logical commits only. Repository must remain working (green) and leave the repo in a state that is independently reviewable.
- **Conventional Commits**: `<type>(<scope>): <summary>` format required. Reference issue IDs when known or available (e.g., `#123`).
- **Allowed Types**: `feat, fix, docs, refactor, style, perf, test, build, ci, chore, deps, revert`.
- **Work Type Mapping**: `feat` adds user-visible capability, `fix` corrects behavior, `refactor` preserves behavior while restructuring, `docs` changes documentation only, `test` changes tests/evaluation evidence, `ci` changes workflows or validation gates, and `chore` covers maintenance without user-facing behavior change.
- **WIP State**: Incomplete but valuable checkpoints must record WIP state in `docs/04.execution/tasks/`, `docs/00.agent-governance/memory/progress.md`, or the PR body before handoff and must not be merged as completed work.
- **Subject**: Imperative mood ("add", "fix"), concise (<= 72 chars).
- **Body**: Explains "what" and "why" (not how) for complex changes.
- **Hotfix**: Branch from `main` (`hotfix/<slug>`). Open two PRs: first to `main`, then to `dev`. Merge `main` PR first; use merge commit (not squash) to preserve commit identity.
- **Merge Strategy**: Squash merge for feature/fix/docs branches; merge commit for `hotfix/*`.
- **PR-Only**: Direct push to `main` or `dev` is strictly prohibited. Merge only via PR targeting `dev` or `main` according to the branch policy.
- **Issue Tracking**: Reference issue IDs (e.g., `#123`) in commits and PRs when known or available. Do not invent issue IDs.
