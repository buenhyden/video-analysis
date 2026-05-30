# AGENTS.md

> [!IMPORTANT]
> Workspace-level source of truth for AI agents. Read this before changing files, then follow the linked governance documents for detailed rules.

## Workspace Contract

`Project-Template` is a language-agnostic, AI-native project template for autonomous SDLC. It provides reusable governance, documentation, workflow, CI/CD, quality-gate, template, and operations structure without adding a default application stack.

## Non-Negotiable Rules

- `docs/` has exactly 8 allowed top-level folders: `00.agent-governance`, `01.requirements`, `02.architecture`, `03.specs`, `04.execution`, `05.operations`, `90.references`, and `99.templates`.
- Use `docs/99.templates/` for templates. Halt if the required template is missing.
- New or modified non-README documents under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/` must match the stage-specific template contract from `docs/99.templates/`.
- Use root `DESIGN.md` as the UI design-system router. Do not start frontend, mobile, or app UI work before it exists and is initialized.
- Keep detailed policy in `docs/00.agent-governance/**`; keep root/provider files as routers and concise operating summaries.
- Do not add GitHub-native AI instruction layers such as `.github/copilot-instructions.md` or `.github/instructions/**`.
- Treat `.claude/**` as the canonical local runtime surface. Treat `.codex/**` as synchronized Codex compatibility metadata, not an independent policy store.
- Do not create or commit `.codex/hooks.json`, `.codex/hooks/**`, `.agents/skills/**`, or new `.agents/**` policy files; the tracked `.agents` allowlist is limited to `README.md`, `rules/graphify.md`, and `workflows/graphify.md`.
- Treat `main` as the clean release-template branch: `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/` keep README skeleton guides only.
- Before creating new-project stage documents, collect product/software and stack intake using `docs/00.agent-governance/rules/project-initialization-intake.md`.
- Classify documents using `docs/00.agent-governance/rules/template-document-lifecycle.md` before moving, deleting, promoting, or treating template-maintenance history as new-project content.

## Document Ownership For Reuse

- `project-seed`: only stage README skeletons and bootstrap-generated draft PRD intake seeds.
- `active-template-contract`: keep in Stage 00, templates, or template-maintenance history; do not reuse as active new-project content.
- `template-maintenance`: keep on `dev` or maintenance branches; omit from `main` release skeleton and ordinary derived projects.
- `archive/reference`: keep only when clearly marked and linked as reference.
- `example`: allowed only after explicit conversion to non-authoritative sample content.
- `remove-candidate`: remove only after reference search and migration note.

## Operating Flow

1. Read `docs/00.agent-governance/rules/bootstrap.md`, the relevant provider note, `project-initialization-intake.md`, and the target stage README before writing.
2. For new projects, complete product/software and stack intake before authoring requirements, architecture, specs, plans, tasks, operations, or references.
3. For setup, validation prerequisites, local tooling, or runtime readiness changes, classify tools through `environment-readiness.md` before treating a missing optional or stack-specific tool as blocking.
4. Select the required template from `docs/99.templates/` using `stage-gate-matrix.md`; stop if the template is absent or the document would not match the stage contract.
5. Anchor implementation in the numbered stages: requirements in `docs/01.requirements/`, architecture in `docs/02.architecture/requirements/` and `docs/02.architecture/decisions/`, specs in `docs/03.specs/`, plans in `docs/04.execution/plans/`, and execution evidence in `docs/04.execution/tasks/`.
6. Keep active methodology and progress in `docs/00.agent-governance/memory/`; update `memory/progress.md` at phase boundaries, blockers, handoffs, and closure.
7. Execute as Analyze -> Plan -> Execute -> Validate -> Sync. The hooks block invalid stage-template writes when possible, auto-sync `docs/` README indexes, and run template-readiness validation after writes.
8. Run `ws validate` before completion when available; otherwise run `bash scripts/ws.sh validate`.

## Git And CI

- Strategy: git-flow with `main` as production, `dev` as integration, and feature/fix/docs/chore/ci branches from `dev`.
- Hotfixes branch from `main`, then return through reviewed PRs to both `main` and `dev`.
- Merge policy: PR-only to `main` and `dev`; no direct pushes and no workflow-managed auto-merge.
- Commits: Conventional Commits, issue references only when known, and 1-commit-1-change.
- PRs: `gh pr create` must use `.github/PULL_REQUEST_TEMPLATE.md` as the body and fill every section.
- Workflow changes must follow `docs/00.agent-governance/rules/ci-cd-workflow.md`: job-level permissions, timeouts, explicit branch filters, and scoped evidence commands.

## Runtime Entrypoints

- Claude runtime: `.claude/CLAUDE.md`
- Claude agents: `.claude/agents/*.md`
- Gemini runtime: `GEMINI.md`
- Local SDLC skill: `.claude/skills/spec-driven-sdlc/skill.md`
- Local governance skill: `.claude/skills/workspace-governance/skill.md`
- Codex compatibility agents: `.codex/agents/*.toml`
- Agent hook dispatcher: `bash scripts/ws.sh hook <event> [matcher]`
- Legacy mirror, if present: `.agents/**` is compatibility-only, allowlisted to the tracked Graphify helper files, and must not define independent policy.
- Local helper, if present: `.agent/**` is optional generated/local guidance only.

## Required References

- Governance manual: `docs/00.agent-governance/onboarding-manual.md`
- Agent operating procedure: `docs/00.agent-governance/rules/agentic.md`
- Active harness inventory (agents, skills, hooks): `docs/00.agent-governance/rules/harness-library.md`
- Environment readiness: `docs/00.agent-governance/rules/environment-readiness.md`
- Documentation protocol: `docs/00.agent-governance/rules/documentation-protocol.md`
- Template document lifecycle: `docs/00.agent-governance/rules/template-document-lifecycle.md`
- Project initialization intake: `docs/00.agent-governance/rules/project-initialization-intake.md`
- Quality standards: `docs/00.agent-governance/rules/quality-standards.md`
- Git workflow: `docs/00.agent-governance/rules/git-workflow.md`
- CI/CD governance: `docs/00.agent-governance/rules/ci-cd-workflow.md`
- Human-agent collaboration flow: `docs/00.agent-governance/sdlc-workflow.md`
- Workspace wiki: `docs/LLM-WIKI.md`
- Workspace commands: `bash scripts/ws.sh help`

## graphify

Optional Graphify output is generated supporting context only. Follow `docs/00.agent-governance/rules/documentation-protocol.md` §11; canonical source files, Stage 00 governance, templates, and validators always win.
