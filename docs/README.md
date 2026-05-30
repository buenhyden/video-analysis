---
title: Documentation Hub Index
version: 1.3.0
owner: Docs Architect
layer: common
stage: N/A
status: active
last-updated: 2026-05-21
---

# Documentation Hub

> Minimal governance project template의 공식 문서 허브.

## Overview

이 허브는 새 프로젝트를 시작하기 위한 `Project-Template` workspace의 공식 문서 진입점이다. `docs/` 트리는 `00.agent-governance`, `01.requirements`, `02.architecture`, `03.specs`, `04.execution`, `05.operations`, `90.references`, `99.templates`의 8개 최상위 폴더만 허용한다.

현재 템플릿은 특정 언어나 프레임워크를 강제하지 않는다. 구현 스택 문서는 파생 프로젝트 intake 이후에만 생성한다. `main` release branch에서는 `docs/01`, `02`, `03`, `04`, `05`, `90`에 실제 프로젝트 문서나 템플릿 개발 이력을 남기지 않고 README skeleton guide만 유지한다.

새 프로젝트는 이 skeleton을 그대로 보존하는 것이 아니라, product/software와 stack intake를 완료한 뒤 해당 stage folder의 README와 문서 파일을 실제 프로젝트 목적, 구조, 스택, 운영 기준에 맞게 수정해야 한다. Stage README는 `docs/99.templates/readme.template.md`의 Base Structure를 기반으로 작성한다.

`dev` branch의 `docs/01.requirements`부터 `docs/90.references`까지에는 Project-Template 자체의 maintenance history가 남아 있을 수 있다. 이 문서들은 새 프로젝트 seed가 아니며, release-template 기준인 `main`에서는 해당 stage folder가 README skeleton guide만 유지해야 한다.

최근 GitHub hardening은 repository automation과 QA gate를 분리하면서 workflow drift를 명시적으로 드러낸다. branch, workflow-run, scheduled, tag-triggered, write-permission workflow는 concurrency를 요구한다. CodeQL GitHub Actions 분석은 stack-neutral 상태를 유지한다. release changelog automation은 `main` 대상 review PR을 생성하거나 갱신한다. `.github/ABOUT.md`와 `.github/SECURITY.md`는 operational metadata로 검증된다.

## Audience

이 허브의 주요 독자:

- repository documentation을 변경하기 전에 올바른 SDLC stage를 확인해야 하는 사람
- governance rule, template, validation command를 찾는 AI agent
- 문서 구조와 stage index를 유지하는 docs/governance 담당자

## Scope

### In Scope

- 8개 허용 `docs/` 최상위 폴더와 각 README index.
- governance부터 operations, references까지 이어지는 compact stage-gate documentation flow.
- template discovery, validation command, documentation maintenance rule.
- 새 프로젝트에서 skeleton folder와 README를 project-specific 문서로 전환하는 기준.

### Out of Scope

- 파생 프로젝트의 application stack documentation.
- 이 source template에 속하지 않는 product-specific requirement나 implementation record.
- `docs/00.agent-governance/`가 소유하는 runtime policy detail.
- `main` release skeleton에 Project-Template 수행 이력이나 generated reference index를 보존하는 행위.

## Structure

| Area   | Path                                                    | Purpose                                                                     | Primary Template                                                                               |
| :----- | :------------------------------------------------------ | :-------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| **00** | [00.agent-governance/](./00.agent-governance/README.md) | Governance rules, scopes, providers, runtime policy, agent operating manual | N/A                                                                                            |
| **01** | [01.requirements/](./01.requirements/README.md)         | Product와 feature 요구사항                                                  | `prd.template.md`                                                                              |
| **02** | [02.architecture/](./02.architecture/README.md)         | Architecture requirements와 decision records                                | `ard.template.md` / `adr.template.md`                                                          |
| **03** | [03.specs/](./03.specs/README.md)                       | Software, automation, agent design specification                            | `spec.template.md`                                                                             |
| **04** | [04.execution/](./04.execution/README.md)               | Execution plans and task evidence                                           | `plan.template.md` / `task.template.md`                                                        |
| **05** | [05.operations/](./05.operations/README.md)             | Guides, policies, runbooks, incidents, postmortems                          | `guide.template.md` / `operation.template.md` / `runbook.template.md` / `incident.template.md` |
| **90** | [90.references/](./90.references/README.md)             | Factual reference, repository intelligence, knowledge material              | `reference.template.md`                                                                        |
| **99** | [99.templates/](./99.templates/README.md)               | Canonical document template과 optional expanded/extended companion          | N/A                                                                                            |

## Documents

| File                                          | Type    | Summary                                                 | Status | Last Modified |
| :-------------------------------------------- | :------ | :------------------------------------------------------ | :----- | :------------ |
| [00.agent-governance](./00.agent-governance/) | package | Governance rules, scopes, providers, and runtime policy | active | 2026-05-09    |
| [01.requirements](./01.requirements/)         | package | Release skeleton guide plus dev-only template contract history | project-seed | 2026-05-21    |
| [02.architecture](./02.architecture/)         | package | Release skeleton guide plus dev-only template architecture history | project-seed | 2026-05-21    |
| [03.specs](./03.specs/)                       | package | Release skeleton guide plus dev-only remediation specs | project-seed | 2026-05-21    |
| [04.execution](./04.execution/)               | package | Release skeleton guide plus dev-only plans and task evidence | project-seed | 2026-05-21    |
| [05.operations](./05.operations/)             | package | Release skeleton guide plus dev-only operations history | project-seed | 2026-05-21    |
| [90.references](./90.references/)             | package | Release skeleton guide plus dev-only reference history | project-seed | 2026-05-21    |
| [99.templates](./99.templates/)               | package | Canonical document templates and optional companions    | active | 2026-05-09    |
| [LLM-WIKI.md](./LLM-WIKI.md)                  | md      | Central AI agent reference                              | active | 2026-05-19    |

## How to Work in This Area

1. 대상 stage README를 먼저 읽고 해당 폴더가 작업을 소유하는지 확인한다.
2. 새 프로젝트에서는 먼저 `docs/00.agent-governance/rules/project-initialization-intake.md`에 정의된 product/software와 stack intake를 완료한다.
3. `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, `docs/90.references/`의 README는 `docs/99.templates/readme.template.md`를 기준으로 프로젝트별 내용으로 수정한다.
4. 새 governed document는 `docs/99.templates/`의 matching template에서 시작한다.
5. 모든 stage document는 `## Related Documents`로 upstream/downstream context에 연결한다.
6. non-trivial implementation 전에는 `docs/04.execution/plans/`의 실행 계획을 만들거나 갱신하고, 실행 중 `docs/04.execution/tasks/`에 evidence를 남긴다.
7. 문서 추가, 삭제, 이름 변경, metadata 변경 후에는 해당 stage README index를 갱신한다.
8. 작업 종료 전 필요한 validation gate를 실행한다.

README index는 다음 명령으로 갱신한다.

```bash
bash scripts/docs/update-doc-readme-index.sh <docs-relative-dir>
```

## Validation & Maintenance

일반 완료 기준은 canonical gate를 사용한다.

```bash
bash scripts/ws.sh validate
```

문서만 변경할 때는 필요한 focused check를 함께 사용한다.

| Command                                        | Documentation Role                                                                                                                                   |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bash scripts/validation/validate-docs.sh`                | Template frontmatter, README lifecycle rule, optional Markdown/YAML/Shell lint, doc-readiness check를 검증한다.                                      |
| `python3 scripts/validation/validate-doc-readiness.py`    | Canonical frontmatter position, README contract, stage-specific template contract, nested index coverage, stale template/runtime reference를 검증한다. |
| `python3 scripts/validation/validate-stage-template-write.py` | PreToolUse hook에서 pending stage document write가 `docs/99.templates` 계약을 만족하는지 검증한다.                                                |
| `bash scripts/validation/validate-cross-links.sh`         | 내부 documentation link를 검증한다.                                                                                                                  |
| `python3 scripts/validation/validate-path-portability.py` | Repository path length, segment length, spaces, and Windows-reserved character warnings를 출력한다. Warning-only gate다.                             |
| `bash scripts/validation/validate-code-style.sh`          | Whitespace, line ending, and configured style hook checks를 실행한다.                                                                                |
| `python3 scripts/validation/validate-script-inventory.py` | documented script command와 active workflow reference 정합성을 검증한다.                                                                             |
| `python3 scripts/validation/validate-github-workflows.py` | GitHub Actions syntax, branch policy, least-privilege permission, concurrency, duplicate workflow surface, changelog automation behavior를 검증한다. |
| `python3 scripts/validation/validate-github-metadata.py`  | GitHub metadata coverage, CODEOWNERS path, workflow inventory classification, SECURITY branch support, duplicate `.github` surface를 검증한다.       |
| `python3 scripts/validation/validate-runtime-contracts.py` | Claude/Codex 공유 hook contract와 template-readiness hook command 연결을 검증한다.                                                               |
| `python3 scripts/validation/validate-version-drift.py`    | tracked 또는 non-empty stack root가 있을 때만 active stack version drift를 확인한다.                                                                 |
| `bash scripts/ws.sh validate`                  | docs, links, scripts, GitHub metadata, runtime quality, architecture, conditional audit를 포함한 full local governance gate를 실행한다.              |
| `bash scripts/ws.sh validate-distribution`     | `main` release skeleton에서 허용 README 외 project-content 문서가 남아 있지 않은지 검증한다.                                                       |

## Template Footprint

- **Core folders**: 8개 허용 `docs/` 최상위 폴더와 각 README contract. `main` release branch의 project-content stage는 README skeleton만 포함한다.
- **Release skeleton README**: `docs/01`, `02`, `03`, `04`, `05`, `90` README는 `docs/99.templates/readme.template.md`의 Base Structure와 stage-specific sections를 함께 따른다.
- **Derived project rewrite**: bootstrap 이후 skeleton README와 stage documents는 실제 product/software, stack, environments, release model에 맞게 수정한다.
- **Core templates**: Stage 01-10, 90에 직접 매핑되는 stage-gate Markdown template.
- **Optional templates**: `docs/99.templates/expanded/`의 DDD companion template과 `docs/99.templates/extended/`의 technology-specific contract.

## New-project Reset Summary

새 프로젝트로 전환할 때 `docs/01.requirements/`부터 `docs/90.references/`까지의
README는 시작 안내로 유지하되, `dev`에 남은 non-README maintenance history는
project-owned 문서가 아니다. Bootstrap은 Stage 01 draft PRD intake seed만 만들며,
ARD, ADR, spec, plan, task, operations, reference 문서는 실제 upstream evidence가
생긴 뒤 matching template에서 생성한다.

| Ownership | Where it belongs | New-project action |
| :--- | :--- | :--- |
| `project-seed` | Stage README skeletons and bootstrap PRD seed | Keep and replace TODOs with project facts. |
| `template-maintenance` | `dev` maintenance history | Do not copy into ordinary derived projects. |
| `active-template-contract` | Stage 00, templates, or dev decision history | Use the stable Stage 00 rule, not the historical doc, as authority. |
| `archive/reference` | Clearly marked reference areas | Keep only when intentionally retained as non-authoritative history. |

## AI Execution Checklist

- [ ] **Entry Gate**: The SDLC stage and folder purpose are identified.
- [ ] **Template Gate**: New governed documents start from `docs/99.templates/`.
- [ ] **Index Gate**: The relevant README `Documents` table is synchronized.
- [ ] **Exit Gate**: The documentation chain is verified and links are valid.
- [ ] **Hard Stop**: STOP if a document index cannot be reconciled with folder contents.
- [ ] **Evidence Rule**: Every change must adhere to `documentation-protocol.md` and link to the relevant execution evidence when implementation occurred.

## Related References

- [LLM-WIKI.md](./LLM-WIKI.md) - AI agent용 central reference
- [AGENTS.md](../AGENTS.md) - Workspace agent contract
- [DESIGN.md](../DESIGN.md) - Target project용 UI design router
- [Documentation Protocol](./00.agent-governance/rules/documentation-protocol.md) - Documentation governance rule
- [GitHub Configuration Hub](../.github/ABOUT.md) - Workflow classification과 repository metadata map
- [CI/CD Governance](./00.agent-governance/rules/ci-cd-workflow.md) - Git-flow workflow safety rule
- [Scripts & Utilities](../scripts/README.md) - Workspace command inventory
- [ws CLI](../scripts/ws.sh) - Workspace validation entry point

---

## Docs 3 Global Rules Reference

> Active on every task. HALT conditions enforced by agents.
> Applies when creating or changing governed documentation in this folder.
> Full definitions: `docs/00.agent-governance/rules/documentation-protocol.md §7`

| Rule                       | Summary                                                                              | HALT If                                          |
| :------------------------- | :----------------------------------------------------------------------------------- | :----------------------------------------------- |
| **R1 — Content Creation**  | Read template before creating any stage doc. Fill all sections. Set `status: draft`. | Template missing or `[placeholder]` text remains |
| **R2 — Auto-Indexing**     | Update this README after every change to this folder.                                | README not updated after folder change           |
| **R3 — Cross-Referencing** | Every stage doc must have `## Related Documents` with relative upstream links.       | Required upstream links absent                   |
