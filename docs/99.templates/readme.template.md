---
title: <string>
version: <string>
owner: <string>
layer: common
stage: 99
status: draft
last-updated: YYYY-MM-DD
---

<!--
# README Template — Repository-wide Usage Guide

Target: README.md in the repository root, docs stage folder, implementation folder, operations folder, or incident folder being documented.

이 템플릿은 리포지토리 전반에서 공통으로 사용하는 README 원본 템플릿이다.
모든 README가 공유해야 하는 최소 구조(Base Structure)를 제공하고,
경로의 목적에 따라 필요한 확장 섹션(Snippet)만 선택적으로 추가할 수 있도록 설계되었다.

## Selection Guide
- Repository Root (`/`) -> `Base Structure` + `Root Snippet`
- Implementation Layer (`web/`, `server/`, `app/`, `packages/`, `gitops/`, `infra/`, `infrastructure/`) -> `Base Structure` + `Implementation Snippet`
- Documentation & Governance (`docs/`, `docs/99.templates/`, `.agent-work/`) -> `Base Structure` + `Docs & Governance Snippet`
- Operations & Procedures (`docs/05.operations/policies/`, `docs/05.operations/runbooks/`, `scripts/`) -> `Base Structure` + `Ops & Utils Snippet`
- Incident Learning (`docs/05.operations/incidents/`) -> `Base Structure` + `Incident / Postmortem Snippet`

## Root README contract
For a stack-neutral project template root, keep the Base Structure headings and add the Root Snippet sections that apply without inventing an application stack.
The required root README headings are:
- `## Overview`
- `## Audience`
- `## Scope` with `### In Scope` and `### Out of Scope`
- `## Structure`
- `## How to Work in This Area`
- `## Related Documents`

If the repository intentionally has no active app stack, omit `## Tech Stack` and `## Prerequisites` rather than filling placeholder technologies.
If a derived project adopts an implementation stack, add the applicable Root or Implementation snippet sections during bootstrap or the first stack PR.

## Stage README variant
Stage READMEs under `docs/00.agent-governance/`, `docs/01.requirements/` through `docs/05.operations/incidents/`, `docs/90.references/`, and `docs/99.templates/` use this Base Structure plus the Docs & Governance snippet and the stage-specific contract enforced by `scripts/validation/validate-doc-readiness.py`.
They must preserve overview, audience, scope, structure, work instructions, mandatory templates, naming/lifecycle/cross-reference rules, usage examples, AI authoring guidance, the `## Documents` table, and related documents.

Naming rules in stage READMEs must include path portability guidance: keep generated relative paths within the warning budget of 140 characters, current absolute paths within 220 characters, path segments within 80 characters, use lowercase kebab-case slugs, and avoid spaces or Windows-reserved characters (`<`, `>`, `:`, `"`, `|`, `?`, `*`).

For `main` release skeletons, README files under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, and `docs/90.references/` must state that `Project-Template` is the starting workspace for a new project. They must not contain product history. They must instruct derived projects to update the folder README and create project-specific documents after product/software and stack intake.

Branch contract: `dev` may retain Project-Template maintenance history, but `main` is the release-template branch for new projects. Do not copy dev-only PRD, ARD, ADR, spec, plan, task, operations, or reference records into `main` release skeleton READMEs.

## Target-relative link examples
Write links from the README file's final target location, not from `docs/99.templates/readme.template.md`.

| README Target | Example Link to Root `AGENTS.md` | Example Link to `docs/99.templates/readme.template.md` |
| --- | --- | --- |
| `README.md` | `[AGENTS.md](./AGENTS.md)` | `[docs/99.templates/readme.template.md](./docs/99.templates/readme.template.md)` |
| `docs/README.md` | `[AGENTS.md](../AGENTS.md)` | `[99.templates/readme.template.md](./99.templates/readme.template.md)` |
| `docs/00.agent-governance/README.md` | `[AGENTS.md](../../AGENTS.md)` | `[readme.template.md](../99.templates/readme.template.md)` |
| `docs/04.execution/README.md` | `[AGENTS.md](../../AGENTS.md)` | `[plan.template.md](../99.templates/plan.template.md)` |
| `docs/04.execution/plans/README.md` | `[AGENTS.md](../../../AGENTS.md)` | `[plan.template.md](../../99.templates/plan.template.md)` |
| `docs/05.operations/incidents/README.md` | `[AGENTS.md](../../../AGENTS.md)` | `[incident.template.md](../../99.templates/incident.template.md)` |
| `docs/90.references/knowledge/README.md` | `[AGENTS.md](../../../AGENTS.md)` | `[reference.template.md](../../99.templates/reference.template.md)` |
| `docs/99.templates/README.md` | `[AGENTS.md](../../AGENTS.md)` | `[readme.template.md](./readme.template.md)` |
| `docs/99.templates/expanded/README.md` | `[AGENTS.md](../../../AGENTS.md)` | `[Template Index](../README.md)` |

## docs 디렉터리 상세 역할

The links in this snippet are target-relative for `docs/README.md`. If you paste
the snippet into root `README.md`, prefix each target with `docs/`. If you paste
it into a nested stage README, add the required `../` depth from that target.

- [01.requirements](01.requirements/README.md): 제품 요구사항 정의 (Vision, Use Case, Requirements)
- [02.architecture/requirements](02.architecture/requirements/README.md): 아키텍처 참조 모델 및 품질 속성 정의
- [02.architecture/decisions](02.architecture/decisions/README.md): 기술적 의사결정 기록 (Decision, Status, Context, Consequence)
- [03.specs](03.specs/README.md): 컴포넌트/기능별 상세 설계 명세 (Data, API, Logic, Agent-Design)
- [04.execution/plans](04.execution/plans/README.md): 실행 계획 및 마일스톤 (Work Breakdown, Risks)
- [04.execution/tasks](04.execution/tasks/README.md): 실제 구현 및 검증 작업 단위 (Task Table, Evidence)
- [05.operations/policies](05.operations/policies/README.md): 시스템 운영 정책 및 거버넌스
- [05.operations/runbooks](05.operations/runbooks/README.md): 반복적 운영 작업의 실행 지침 (Step-by-step)
- [05.operations/incidents](05.operations/incidents/README.md): 사고의 사실 기록, 대응 흐름, 사후 분석

## Assembly Rules
1. 아래의 `Base Structure`를 먼저 복사한다.
2. `{}` 자리표시자를 실제 내용으로 교체한다.
3. 현재 경로의 목적에 맞는 `Snippet`만 추가한다.
4. 사용하지 않는 스니펫과 이 안내 주석은 최종 `README.md`에서 제거한다.

## Writing Principles
- README는 소개문이 아니라 이 경로의 진입 문서여야 한다.
- README는 책임 범위(In Scope / Out of Scope)를 명확히 보여줘야 한다.
- README는 사람과 AI Agent 모두가 읽어도 목적을 오해하지 않도록 작성해야 한다.
- README는 상위 문서와 하위 산출물 간 연결을 드러내야 한다.
- README는 생성, 수정, 검토 시 따라야 하는 최소 작업 규칙을 포함해야 한다.
-->

# {Folder or Project Name}

> {이 경로가 왜 존재하는지 설명하는 한 줄 목적문}

## Overview

{이 폴더 또는 프로젝트가 전체 리포지토리나 시스템에서 맡는 책임을 설명한다.
무엇을 위한 경로인지, 어떤 산출물이나 역할을 담당하는지 1~2문단으로 정리한다.}

## Audience

이 README의 주요 독자:

- {Developers}
- {Operators}
- {Documentation Writers}
- {AI Agents}

## Scope

### In Scope

- {이 경로에 포함되어야 하는 문서, 코드, 스크립트, 산출물}
- {이 경로가 담당하는 책임}
- {이 경로에서 관리하는 핵심 항목}

### Out of Scope

- {이 경로에 두면 안 되는 것}
- {다른 디렉터리 또는 다른 문서 계층이 담당하는 것}
- {임시 산출물, 중복 산출물 등 배제 대상}

## Structure

```text
{folder-name}/
├── {file-or-dir-1}    # {Purpose}
├── {file-or-dir-2}    # {Purpose}
├── {file-or-dir-3}    # {Purpose}
└── README.md          # This file
```

## How to Work in This Area

1. {이 영역을 이해하기 위해 가장 먼저 읽어야 할 문서 또는 파일}
2. {새 항목을 만들기 전에 확인해야 할 기존 구조 또는 상위 문서}
3. {따라야 하는 템플릿, 규칙, 표준}
4. {변경 후 함께 갱신해야 하는 링크, 메타데이터, 관련 문서}

## Related Documents

- {상위 문서 또는 상위 컨텍스트}
- {같은 계층의 관련 문서}
- {하위 구현, 계획, 작업, 운영 문서}

---

# SNIPPET LIBRARY

# <!--

# SNIPPET: ROOT

-->

## Repository Map

- `docs/` - 공식 문서 체계, 요구사항, 아키텍처, 스펙, 운영 지식
- `{implementation-dir}/` - 구현 코드와 런타임 구성
- `{ops-dir}/` - 운영 자산, 스크립트, 절차
- `.agent-work/` - 에이전트 프롬프트 패키지와 핸드오프 리포트

## Tech Stack

| Category   | Technology                                | Notes                     |
| ---------- | ----------------------------------------- | ------------------------- |
| Language   | {TypeScript / Python / Go / etc.}         | {Version or build target} |
| Framework  | {Next.js / FastAPI / Spring / etc.}       | {Primary runtime}         |
| Database   | {PostgreSQL / Valkey / OpenSearch / etc.} | {Primary persistence}     |
| Deployment | {Docker / Kubernetes / etc.}              | {Standard delivery track} |

## Prerequisites

- {Tool 1} >= {Version}
- {Tool 2} >= {Version}
- {Tool 3} >= {Version}

## Getting Started

### 1. Clone and Setup

```bash
git clone {repository-url}
cd {project-name}
{install-command}
```

### 2. Repository Entry Points

리포지토리 작업 전에 다음 진입점을 우선 확인한다.

1. [README.md](./README.md) - 저장소 개요
2. [docs/README.md](./docs/README.md) - 문서 체계 개요
3. [AGENTS.md](./AGENTS.md) - Agent 규칙
4. [docs/02.architecture/README.md](./docs/02.architecture/README.md) - 아키텍처 단계 구조 설명
5. [DESIGN.md](./DESIGN.md) - UI 작업이 범위에 포함될 때 사용하는 디자인 시스템 라우터

# <!--

# SNIPPET: IMPLEMENTATION

-->

## Available Scripts

| Command           | Description        |
| ----------------- | ------------------ |
| `{dev-command}`   | 개발 모드 실행     |
| `{build-command}` | 배포용 산출물 빌드 |
| `{test-command}`  | 테스트 실행        |
| `{lint-command}`  | 정적 검사 실행     |

## Configuration

### Environment Variables

| Variable  | Required | Description |
| --------- | -------: | ----------- |
| `{ENV_1}` |      Yes | {설명}      |
| `{ENV_2}` |      Yes | {설명}      |
| `{ENV_3}` |       No | {설명}      |

## Testing

```bash
{test-command}
```

## Change Impact

- 이 영역의 변경은 `{related-module-or-service}` 에 영향을 줄 수 있다.
- 공개 인터페이스 변경 시 `{contract-or-spec-doc}` 를 함께 갱신해야 한다.
- 설정 변경 시 `{deployment-or-ops-doc}` 와 일치해야 한다.

# <!--

# SNIPPET: DOCS & GOVERNANCE

-->

## Documentation Standards

이 영역의 문서는 다음 기준을 따라야 한다.

- 가능한 경우 승인된 템플릿에서 시작한다.
- 기존 SSoT (Single Source of Truth, 단일 진실 원천) 문서를 중복 생성하지 않는다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## Traceability Rules

이 영역의 각 문서는 가능한 경우 다음 중 하나 이상과 연결되어야 한다.

- Product Requirements Document (PRD)
- Architecture Requirements Document (ARD)
- Architecture Decision Record (ADR)
- Specification (Spec)
- Plan
- Task
- Runbook
- Incident / Postmortem

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| {file-or-dir} | {type} | {summary} | {status} | YYYY-MM-DD |

## Template Usage

- 새 문서를 만들 때는 `{template-path}` 또는 `templates/` 아래의 적절한 템플릿을 사용한다.
- 템플릿 없이 새 형식을 임의로 추가하기 전에 기존 문서 체계를 먼저 검토한다.
- 동일 목적의 문서가 이미 존재하면 새 문서를 만들기보다 기존 문서를 확장하는 방식을 우선한다.
- 템플릿에 있는 관련 문서 예시는 최종 README target 위치 기준의 실제 Markdown 링크로 변환한다. 예: `docs/README.md`에서는 `[99.templates/readme.template.md](./99.templates/readme.template.md)`, root `README.md`에서는 `[docs/99.templates/readme.template.md](./docs/99.templates/readme.template.md)`.

## Metadata Expectations

필요한 경우 문서에는 다음 메타데이터를 포함한다.

- `title`
- `type`
- `status`
- `owner`
- `updated`
- `links` 또는 관련 상위/하위 문서 정보

예시:

```yaml
---
title: { title }
type: { document-type }
status: draft
owner: { team-or-person }
updated: YYYY-MM-DD
links:
  - { related-doc }
---
```

## SSoT References

- {PRD link}
- {ARD link}
- {ADR link}
- {Spec link}
- {Plan link}
- {Task link}

# <!--

# SNIPPET: OPS & UTILS

-->

## Usage Instructions

{이 경로의 스크립트, 도구, 절차 또는 운영 기준을 어떻게 실행하거나 적용하는지 설명한다.
정책 중심 경로라면 적용 및 검증 방식으로, 실행 중심 경로라면 단계별 절차로 작성한다.}

예시:

```bash
{example-command}
```

## Verification and Monitoring

- 로그 위치: `{log-path}`
- 상태 점검 방법: `{command-or-dashboard}`
- 모니터링 또는 알림 기준: `{monitoring-location}`
- 운영 이상 징후 발생 시 참조 문서: `{runbook-link}`

## Incident and Recovery Links

- Runbooks: {runbook-link}
- Incident Records: {incident-link}
- Postmortems: {postmortem-link}

# <!--

# SNIPPET: INCIDENT / POSTMORTEM

-->

## Record Purpose

이 영역은 운영 중 학습과 대응 기록을 저장한다.

- `incidents/` 는 장애 또는 이상 상황에서 **무슨 일이 발생했는지**, **영향 범위가 무엇인지**, **즉시 어떤 대응을 했는지**를 기록한다.
- `postmortems/` 는 사건 이후 **근본 원인**, **기여 요인**, **재발 방지 조치**, **학습 내용**을 정리한다.

## Expected Record Shape

기록 문서는 가능한 경우 다음 항목을 포함한다.

- Summary
- Impact
- Affected Systems / Routes
- Timeline
- Root Cause
- Immediate Remediation
- Follow-up Actions
- Related Specs / ADRs / Runbooks / Policies

## Review Expectations

- Incident는 사실 기록과 대응 경위를 빠르게 복원할 수 있어야 한다.
- Postmortem은 비난보다 학습과 재발 방지에 초점을 맞춘다.
- 후속 조치는 Plan 또는 Task와 연결되어야 한다.

# <!--

# SNIPPET: AI AGENT GUIDANCE

-->

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. 이 README를 먼저 읽는다.
2. 상위 SSoT 문서와 관련 링크를 식별한다.
3. 기존 구조를 확인하여 중복 산출물 생성을 피한다.
4. 새 산출물 생성 시 링크, 메타데이터, 네이밍 규칙을 유지한다.

### Allowed Outputs

- {이 경로에서 생성 가능한 문서 또는 코드 산출물}
- {예: requirement docs, specs, plans, tasks, runbooks}

### Guardrails

- `{protected-files-or-generated-assets}` 는 직접 수정하지 않는다.
- 기존 구조 확인 없이 새 파일을 만들지 않는다.
- 추적성 링크가 필요한 영역에서는 상위/하위 문서 연결을 누락하지 않는다.

### Validation

- {필수 검토 기준}
- {필수 테스트 또는 Eval 기준}
- {문서 무결성 또는 링크 검증 기준}

## AI Execution Checklist

- **Entry Gate**: folder purpose, ownership, and template mapping are known.
- **Exit Gate**: purpose, document index, dependencies, methodology overlay, and AI hints are present.
- **Hard Stop Conditions**: STOP if the README target folder is unknown. STOP if the document index cannot be reconciled with files that exist in the folder.
- **Downstream Trigger**: update the README when adding, moving, or retiring documents in the folder.
- **Evidence Rule**: README entries link to canonical files and match actual document status.

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in `docs/00.agent-governance/rules/documentation-protocol.md` §7. In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.

---

## License

{필요한 경우에만 작성한다. 일반적으로 하위 README에서는 생략 가능하며, 저장소 루트의 LICENSE 파일을 우선한다.}
