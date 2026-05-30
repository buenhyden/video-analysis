# Project-Template

> 언어와 프레임워크를 강제하지 않는 AI-native 프로젝트 거버넌스 템플릿.

`layer: common`

![Repository](https://img.shields.io/badge/repository-template-blue.svg)
![Workflow](https://img.shields.io/badge/workflow-spec--driven-success.svg)
![CI](https://img.shields.io/badge/ci-GitHub%20Actions-black.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

`Project-Template`은 새 프로젝트가 복제해 사용할 수 있는 language-agnostic AI-native governance template workspace입니다. 기본 앱 스택을 제공하지 않고, 문서 구조, AI agent instruction surface, Git Flow, CI/CD 품질 게이트, 템플릿, 운영 절차를 표준화합니다.

프레임워크별 구현은 파생 프로젝트가 선택한 뒤 추가합니다. 이전 fullstack starter 자료는 현재 baseline에서 제거되었으며, 활성 루트 템플릿의 필수 구조가 아닙니다.

`docs/` 최상위 구조는 `00.agent-governance`, `01.requirements`, `02.architecture`, `03.specs`, `04.execution`, `05.operations`, `90.references`, `99.templates`로 구성된 8-folder compact model이 canonical입니다. `main` release branch에서는 `docs/01`, `02`, `03`, `04`, `05`, `90`에 README skeleton guide만 남기며, 템플릿 개발 이력은 `dev` 또는 maintenance branch에서 보존합니다.

새 프로젝트는 이 workspace를 출발점으로 사용하되, product/software와 stack intake를 먼저 완료한 뒤 `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, `docs/90.references/`의 README와 문서 파일을 실제 프로젝트 내용으로 수정하거나 새로 작성해야 합니다.

## Audience

이 README의 주요 독자:

- 새 저장소를 이 템플릿에서 파생하려는 프로젝트 소유자
- Stage-gate 문서 체계를 유지하는 문서/거버넌스 담당자
- `.claude/**` 및 `.codex/**` 런타임 표면을 사용하는 AI agents
- CI/CD, GitHub metadata, validation gate를 검토하는 운영자

## Scope

### In Scope

- Language-agnostic project template governance and stage-gate documentation.
- AI Agent-first Engineering runtime contracts through `.claude/**` and `.codex/agents/*.toml`.
- Bootstrap, validation, GitHub metadata, and reusable workspace automation.
- Core `docs/` folders, templates, stage README contracts, and release-template skeleton guides.

| Area | Purpose |
| :--- | :--- |
| Governance | Stage gates, Git/CI rules, provider routers, workspace policy |
| Documentation | 8-folder compact canonical docs tree |
| Runtime | `.claude/**` canonical runtime and `.codex/**` compatibility metadata |
| Templates | Reusable document templates in `docs/99.templates/` |
| CI/CD | Governance, docs, workflow, security, and pre-commit validation |
| Scripts | Workspace validation, bootstrap, intelligence, and maintenance commands |

### Out of Scope

- A default application stack, database, deployment platform, or production app scaffold.
- GitHub-native AI instruction files such as `.github/copilot-instructions.md`.
- Bundled optional starter applications under `examples/`.
- User-global Claude, Codex, or shell configuration.

## Template Footprint

- **Core**: root routers, `.claude/**`, `.codex/agents/*.toml`, `.github/**`, `scripts/**`, and the 8 allowed `docs/` folders.
- **Optional**: technology-specific templates under `docs/99.templates/extended/`.
- **Main release skeleton**: `docs/01`, `02`, `03`, `04`, `05`, and `90` contain only README guides until a derived project bootstrap creates project-specific documents.
- **README basis**: release skeleton README files under `docs/01`, `02`, `03`, `04`, `05`, and `90` follow [docs/99.templates/readme.template.md](./docs/99.templates/readme.template.md).
- **Derived baseline**: provide product/software and stack intake, run `bash scripts/ws.sh bootstrap --dry-run ...` first, then `bash scripts/ws.sh validate-derived` after metadata and design placeholders are initialized.
- **Environment readiness**: run `bash scripts/ws.sh setup` to report core, optional, and stack-conditional local prerequisites. The command is report-only and must not install tools or mutate local configuration.
- **Dev maintenance history**: `dev` may contain Project-Template PRDs, ARDs, ADRs, specs, plans, tasks, SLOs, and references that document template maintenance work. These files are evidence for maintaining the template, not seed content for new projects.
- **Runtime boundary**: `.claude/**` is reusable runtime configuration. `.codex/agents/*.toml` is synchronized Codex compatibility metadata. `.codex/hooks*`, `.agents/skills/**`, `.claude/settings.local.json`, `_workspace/**`, `.agent/**`, and `.agent-work/**` are not reusable template policy surfaces.

## Quick Start for New Projects

Use this sequence when creating an ordinary derived project from the template.

1. Read [AGENTS.md](./AGENTS.md), [Project Initialization Intake](./docs/00.agent-governance/rules/project-initialization-intake.md), and [Template Document Lifecycle](./docs/00.agent-governance/rules/template-document-lifecycle.md).
2. Run `bash scripts/ws.sh bootstrap --dry-run ...` with complete product/software, stack, security, operations, GitHub owner, and security-contact intake flags.
3. Review the reset plan, then run the same bootstrap command without `--dry-run` only if the README-only stage reset is intended.
4. Replace TODOs in `docs/01.requirements/YYYY-MM-DD-project-intake-prd.md`, update root metadata, and initialize `DESIGN.md` if UI work is in scope.
5. Run `bash scripts/ws.sh validate-derived`; then create ARD, ADR, spec, plan, task, operations, and reference documents only when their stage gate is reached.

| Keep from template | Customize or regenerate | Keep local-only |
| :--- | :--- | :--- |
| `AGENTS.md`, thin provider routers, `.claude/**`, `.codex/agents/*.toml`, `docs/00.agent-governance/**`, `docs/99.templates/**`, `scripts/**` | `README.md`, `DESIGN.md`, `.github/ABOUT.md`, `.github/SECURITY.md`, `.github/CODEOWNERS`, bootstrap PRD TODOs, all downstream non-README stage docs | `.claude/settings.local.json`, `.codex/hooks*`, `.agents/skills/**`, `_workspace/**`, `.agent/**`, `.agent-work/**`, logs, tokens, auth files |

## New Project Start Policy

새 프로젝트를 만들 때 이 저장소의 `dev` branch에 남아 있는 PRD, ARD, ADR, spec, plan, task, operations, reference 문서를 그대로 프로젝트 문서로 취급하지 않는다. 해당 문서들은 Project-Template 자체를 정비한 maintenance history 또는 template contract evidence다.

새 프로젝트의 project-owned seed는 다음 두 종류뿐이다.

- `docs/01.requirements/`부터 `docs/90.references/`까지의 README skeleton guide.
- intake 이후 bootstrap이 생성하는 draft PRD-shaped seed: `docs/01.requirements/YYYY-MM-DD-project-intake-prd.md`.

그 외 non-README 문서는 stage gate에 도달했을 때 `docs/99.templates/`에서 새로 만든다. 완료된 Project-Template remediation 문서를 복사하거나 이름만 바꿔 새 프로젝트 문서로 쓰지 않는다.

기본 정책은 다음과 같다.

| Area | 새 프로젝트에서의 처리 |
| :--- | :--- |
| `docs/01.requirements/` | README skeleton을 유지하고, bootstrap이 intake 기반 draft PRD seed를 생성한다. |
| `docs/02.architecture/` | PRD가 검토된 뒤 ARD/ADR을 템플릿에서 새로 만든다. |
| `docs/03.specs/` | 기능별 spec package를 템플릿에서 새로 만든다. |
| `docs/04.execution/` | 승인된 spec 이후 plan/task evidence를 새로 만든다. |
| `docs/05.operations/` | 실제 환경, SLO, 운영 절차가 생긴 뒤 guide/policy/runbook/incident 문서를 새로 만든다. |
| `docs/90.references/` | 출처가 확인된 프로젝트 reference만 새로 만든다. |

문서 소유권과 reset 기준은 [Template Document Lifecycle](./docs/00.agent-governance/rules/template-document-lifecycle.md)에 정리되어 있다.

### Reset Contract For Derived Projects

When this workspace is copied or cloned to create a new project, use the reset
contract below before treating any stage document as project-owned truth.

| Question | Template-safe answer |
| :--- | :--- |
| What starts a new project? | Complete product/software and stack intake, then run `bash scripts/ws.sh bootstrap --dry-run ...` before mutating files. |
| What remains as seed content? | Stage README skeletons and the bootstrap-generated draft PRD intake seed only. |
| What is not seed content? | Existing `dev` PRDs, ARDs, ADRs, specs, plans, tasks, SLOs, onboarding guides, generated intelligence, and references. |
| What must be customized immediately? | `README.md`, `DESIGN.md`, GitHub metadata, security contact, CODEOWNERS, and the draft PRD seed TODOs. |
| What remains reusable? | `AGENTS.md`, thin provider routers, `.claude/**`, `.codex/agents/*.toml`, `docs/00.agent-governance/**`, `docs/99.templates/**`, and `scripts/**`. |
| What must stay local-only? | `.claude/settings.local.json`, `.codex/hooks*`, `.agents/skills/**`, `.agent/**`, `.agent-work/**`, `_workspace/**`, logs, auth files, tokens, and credentials. |
| How is readiness verified? | Run `bash scripts/ws.sh validate-derived` after metadata, design identity, and bootstrap intake seed are initialized. |

### Document Ownership At A Glance

| Label | Meaning | New-project behavior |
| :--- | :--- | :--- |
| `project-seed` | Minimal draft starting point with TODOs and no approved decisions. | Keep README skeletons and bootstrap-generated PRD seed. |
| `active-template-contract` | Canonical rule or decision that defines Project-Template behavior. | Keep in Stage 00, templates, or template maintenance history; do not treat as project content. |
| `template-maintenance` | Completed work record for maintaining this template. | Keep on `dev`; omit from `main` release skeleton and derived projects unless intentionally preserved with `--keep-template-history`. |
| `archive/reference` | Historical or generated reference material. | Keep only as clearly marked reference; do not use as active requirement, spec, plan, operation, or project reference. |
| `example` | Reusable sample marked non-authoritative. | Optional only after explicit conversion to example content. |
| `remove-candidate` | Stale, duplicated, unsafe, or policy-violating content. | Remove only after reference search and migration note. |

## Customization Checklist

복제 또는 템플릿 생성 후 최소한 다음 항목을 프로젝트 값으로 바꾼다.

- `README.md`: 프로젝트 이름, 목적, 사용자, stack, 실행 명령.
- `DESIGN.md`: UI가 있으면 `version`, `name`, design token, component policy.
- `.github/CODEOWNERS`, `.github/ABOUT.md`, `.github/SECURITY.md`: owner, repository, security contact.
- `docs/01.requirements/*`: bootstrap이 만든 draft PRD seed의 TODO.
- `docs/02.architecture/` 이후: 실제 stage gate에 도달한 문서만 템플릿에서 생성.
- `.claude/settings.local.json` 같은 local override: 커밋하지 않거나 파생 프로젝트 정책에 맞게 새로 생성.
- 외부 서비스, secret, API key, endpoint: 실제 값은 repository에 커밋하지 않고 환경/secret store에서 관리.

### Keep As Template Defaults

다음 파일과 폴더는 새 프로젝트가 보통 그대로 시작해도 되는 reusable default다.

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`: provider router and shared agent entrypoints. 프로젝트 정책이 바뀔 때만 얇게 수정한다.
- `.claude/agents/**`, `.claude/skills/**`, `.claude/hooks/**`, `.claude/settings.json`: canonical local runtime defaults.
- `.codex/agents/*.toml`: Codex compatibility metadata. `.codex/hooks*`는 만들거나 커밋하지 않는다.
- `docs/00.agent-governance/**`: reusable governance policy and template lifecycle rules.
- `docs/99.templates/**`: canonical document templates.
- `scripts/**`: bootstrap, validation, docs index, hook replay, and maintenance commands.

### Replace Or Regenerate For A New Project

다음 영역은 새 프로젝트의 실제 목적과 stack으로 다시 채운다.

- Root `README.md`, `.github/ABOUT.md`, `.github/SECURITY.md`, `.github/CODEOWNERS`.
- `DESIGN.md`의 `version`, `name`, product design-system values.
- `docs/01.requirements/YYYY-MM-DD-project-intake-prd.md`의 TODO와 intake snapshot.
- Stage 02-05 및 Stage 90 non-README documents. 필요할 때 matching template에서 새로 생성한다.

### Local-only Or Non-reusable Surfaces

다음 파일은 template-level default로 커밋하거나 복사하지 않는다.

- `.claude/settings.local.json`, `.claude/*.local.md`.
- `.codex/hooks.json`, `.codex/hooks/**`.
- `.agents/skills/**` or any legacy skill tree that reintroduces `.codex/**` paths.
- `_workspace/**`, `.agent/**`, `.agent-work/**`, generated diagnostics, local logs, auth files, tokens, and shell history.

## Agent Tooling Map

| Surface | Responsibility |
| :--- | :--- |
| `AGENTS.md` | 모든 AI agent가 공유하는 얇은 workspace contract. |
| `CLAUDE.md` | Claude Code provider overlay. 세부 런타임은 `.claude/CLAUDE.md`로 위임한다. |
| `GEMINI.md` | Gemini provider overlay. |
| `.claude/**` | canonical local runtime: agents, skills, personas, hooks, commands. |
| `.codex/agents/*.toml` | Codex compatibility metadata. 독립 policy store가 아니다. |
| `.codex/hooks*` | 금지된 runtime policy surface. hook replay는 `bash scripts/ws.sh hook <event> [matcher]`를 사용한다. |
| `.agents/**` | legacy compatibility mirror. Stage 00과 `.claude/**`를 넘어서는 정책을 정의하지 않는다. |
| `.agent/**` | optional/generated helper guidance. 없거나 local tool이 없어도 template 사용은 계속 가능해야 한다. |
| `docs/00.agent-governance/**` | agent governance, instruction hierarchy, hooks, safety, documentation lifecycle의 canonical policy. |
| `RTK.md` | Optional Codex CLI helper guidance for token-filtered command output. It is not loaded by default provider routers. |

## Structure

```text
/
├── .claude/                  # Canonical local runtime agents, hooks, and skills
├── .codex/                   # Synchronized Codex compatibility metadata
├── .github/                  # GitHub metadata, templates, and governance workflows
├── docs/                     # Canonical stage-gate documentation
│   ├── 00.agent-governance/  # Workspace policy and agent governance
│   ├── 01.requirements/      # Product requirements
│   ├── 02.architecture/      # Architecture requirements and decisions
│   ├── 03.specs/             # Technical specs
│   ├── 04.execution/         # Execution plan/task guides and derived-project evidence
│   ├── 05.operations/        # Guides, policies, runbooks, and incidents
│   ├── 90.references/        # Reference guide and derived-project reference docs
│   └── 99.templates/         # Document templates
├── scripts/                  # Governance and workspace automation
├── AGENTS.md                 # Balanced workspace contract for AI agents
├── CLAUDE.md                 # Claude provider overlay
├── GEMINI.md                 # Gemini provider overlay
└── DESIGN.md                 # UI design router, initialized by target projects
```

## Getting Started

```bash
bash scripts/ws.sh help
bash scripts/ws.sh validate
```

For a new derived project:

1. Read [Project Initialization Intake](./docs/00.agent-governance/rules/project-initialization-intake.md).
2. Fill product/software and stack intake fields.
3. Run bootstrap in dry-run mode first.
4. Run bootstrap without `--dry-run` only after the dry-run output matches the intended reset.
5. Replace TODOs in the generated draft PRD seed.
6. Initialize metadata and design placeholders.
7. Run `bash scripts/ws.sh validate-derived`.

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

After bootstrap, replace skeleton guidance with project-specific content. At minimum, update the README files and create the first governed documents for the stages that apply to the new project.

Bootstrap resets Project-Template maintenance history unless `--keep-template-history` is explicitly passed. The generated Stage 01 seed is a draft PRD-shaped intake document, not an approved project decision.

Do not use `--keep-template-history` for ordinary new projects. Use it only when maintaining Project-Template itself or intentionally carrying audit history into a template-maintenance branch.

Useful scoped checks:

```bash
bash scripts/ci/validate-security.sh
python3 scripts/validation/validate-github-workflows.py
python3 scripts/validation/validate-github-metadata.py
bash scripts/docs/update-doc-readme-index.sh <docs-relative-dir>
```

## How to Work in This Area

AI agents and humans share the same governance loop:

1. Read [AGENTS.md](./AGENTS.md), the provider overlay, and the target stage README.
2. Complete product/software and stack intake before creating project stage documents.
3. Use `docs/99.templates/` for governed documents.
4. Use [docs/99.templates/readme.template.md](./docs/99.templates/readme.template.md) for root, folder, and stage README contract checks.
5. Create or update the appropriate execution plan in `docs/04.execution/plans/` before non-trivial implementation.
6. Track execution and validation evidence in `docs/04.execution/tasks/`.
7. Keep README indexes, `docs/LLM-WIKI.md`, root/provider routers, and governance docs synchronized when the governed surface changes.
8. Run the required local gate before commit, push, or PR. CI also runs pre-commit, workflow, metadata, docs, and security gates.

## Stage Flow

`docs/` folder numbers are compact storage roots; the SDLC stage-gate flow still runs from Stage 00 through Stage 10. Start new governed documents from `docs/99.templates/` with `status: draft`, then promote to `active` or `completed` only after the required gate, plan, task, or validation evidence exists.

| Flow | Location | Evidence Boundary |
| :--- | :--- | :--- |
| Intent | `docs/01.requirements/` | PRD scope, requirements, and acceptance criteria |
| Architecture | `docs/02.architecture/` | ARD boundaries and ADR decisions |
| Specification | `docs/03.specs/` | Implementation-ready spec and test strategy |
| Execution | `docs/04.execution/` | Stage 05 plans and Stage 06 task evidence |
| Operations | `docs/05.operations/` | Stage 07 guides, Stage 08 policies, Stage 09 runbooks, Stage 10 incidents |
| Support | `docs/90.references/`, `docs/99.templates/` | Provenance-backed references and reusable templates |

## Validation Model

- `bash scripts/ws.sh validate` is the canonical local gate for base-template work.
- `bash scripts/ws.sh setup` reports local prerequisite status for agent/runtime work without installing tools. The readiness classes are defined in [Environment Readiness](./docs/00.agent-governance/rules/environment-readiness.md).
- `bash scripts/ws.sh validate-derived` is the post-bootstrap gate for derived projects with replaced metadata.
- `bash scripts/ws.sh validate-distribution` checks that `main` release skeleton folders contain only the allowed README guide files. It is expected to fail on `dev` while template-maintenance history remains present.
- `bash scripts/ci/validate-security.sh` runs the explicit local/Security CI security gate for lock-file policy, focused hardcoded-secret checks with sanitized output, changed governance/runtime files, and optional SAST only when active stack tooling exists.
- `python3 scripts/validation/validate-doc-readiness.py` checks the canonical docs folder contract, README contracts, nested index coverage, template inventory, active-surface stale template/runtime references, and Codex compatibility-only surface rules.
- `python3 scripts/validation/validate-github-workflows.py` verifies workflow syntax, least-privilege jobs, action pinning, protected-branch safety, duplicate job/step drift, required concurrency for branch/workflow-run/schedule/tag/write workflows, CodeQL Actions analysis shape, and changelog PR update behavior.
- `python3 scripts/validation/validate-github-metadata.py` verifies CODEOWNERS policy, `.github/ABOUT.md` exact workflow inventory, `.github/SECURITY.md` `main`/`dev` branch support, placeholder policy, GitHub-native instruction bans, and unapproved duplicate `.github` surfaces.
- `python3 scripts/validation/validate-version-drift.py` runs conditional stack-version checks only when an active stack root exists.
- GitHub workflows are classified as CI/CD gates, security gates, diagnostics, release automation, repository intelligence, or repository automation in [.github/ABOUT.md](./.github/ABOUT.md). Repository automation is not a required status check unless governance explicitly promotes it.
- README index tables are maintained by `bash scripts/docs/update-doc-readme-index.sh <docs-relative-dir>` and must remain markdownlint-compatible.

Use this interpretation when validating template reuse:

| Command | Use for | Expected result on `dev` |
| :--- | :--- | :--- |
| `bash scripts/ws.sh setup` | Local prerequisite report | Core tools pass; optional lint/security/stack tools may warn. |
| `bash scripts/ws.sh validate` | Current maintenance branch integrity | Must pass before handoff. |
| `bash scripts/ws.sh validate-distribution` | Prepared release-template skeleton | Warns on `dev` for classified maintenance history; must pass on the prepared `main` surface. |
| `bash scripts/ws.sh validate-derived` | A project after bootstrap | Must pass only after project metadata and `DESIGN.md` are initialized. |

## Related Documents

- [AGENTS.md](./AGENTS.md) - AI agent workspace contract
- [Documentation Hub](./docs/README.md) - Stage-gate documentation index
- [Governance Hub](./docs/00.agent-governance/README.md) - Workspace rules
- [Environment Readiness](./docs/00.agent-governance/rules/environment-readiness.md) - Local prerequisite and runtime readiness contract
- [LLM-WIKI](./docs/LLM-WIKI.md) - High-density agent reference
- [GitHub Configuration Hub](./.github/ABOUT.md) - Workflow and repository metadata map
- [Scripts & Utilities](./scripts/README.md) - Workspace command and script inventory
- [CI/CD Governance](./docs/00.agent-governance/rules/ci-cd-workflow.md) - Workflow safety and validation rules

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](./docs/00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
