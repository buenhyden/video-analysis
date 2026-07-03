---
title: Requirements Hub
version: 1.0.0
owner: Product Manager
layer: product
stage: 01
status: active
last-updated: 2026-05-21
---

# Requirements Skeleton

## Overview

`docs/01.requirements/`는 이 `video-analysis`을 기반으로 새 프로젝트를 시작할 때 product/software 요구사항을 작성하는 stage이다. `main` release branch에서는 실제 PRD나 video-analysis 수행 이력을 보관하지 않고, 새 프로젝트가 수정해서 사용할 README guide만 유지한다.

파생 프로젝트에서는 project initialization intake를 완료한 뒤 이 폴더에 프로젝트별 PRD와 요구사항 문서를 생성한다. 생성된 문서는 제품 목적, 대상 사용자, 핵심 기능, 성공 기준, acceptance criteria, non-goals, testability를 프로젝트 맥락에 맞게 채워야 한다.

`dev`에 남아 있는 non-README PRD는 video-analysis 거버넌스 요구사항을 설명하는 `active-template-contract`다. 새 프로젝트 seed는 이 README skeleton과 bootstrap이 생성하는 draft `YYYY-MM-DD-project-intake-prd.md`뿐이다.

## Audience

이 README의 주요 독자:

- Product managers
- Project owners
- Requirements authors
- AI agents

## Scope

### In Scope

- Intake 결과를 바탕으로 한 project-specific PRD 작성 가이드
- 제품 목적, 사용자, 핵심 기능, 성공 기준, acceptance criteria 정리
- architecture, specs, execution 단계로 전달되는 요구사항 기준점
- 새 프로젝트에서 이 폴더와 문서를 어떻게 수정해야 하는지에 대한 안내

### Out of Scope

- video-analysis 자체 개발 이력, 이전 PRD, 완료된 task evidence
- architecture requirements, ADR, technical spec, implementation plan
- stack이 확정되기 전의 framework, runtime, deployment 세부 결정
- 임시 agent scratchpad 또는 local-only handoff 자료

## Structure

```text
01.requirements/
├── README.md                         # Release skeleton guide and folder contract
└── YYYY-MM-DD-project-intake-prd.md  # Bootstrap-generated draft seed after intake
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- New PRD documents must start from `docs/99.templates/prd.template.md`.
- If the required template is missing, stop and restore the template before authoring.

## Naming Rules

- Time-bound records: `YYYY-MM-DD-<slug>.md`
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

Documents in this folder follow the standard lifecycle:

1. **draft**: Initial creation from template. Not yet for implementation.
2. **review**: Ready for stakeholder, product, or technical owner review.
3. **approved**: Stage 01 gate passed; source of truth for downstream ARD, ADR, Spec, Plan, or Task handoff.
4. **active**: Still authoritative after downstream work has started.
5. **completed**: Implementation finished and verified.
6. **deprecated**: Replaced by a newer version or no longer relevant.

## Cross-Reference Rules

- Every PRD must be linked in the [Documents](#documents) table below.
- Every PRD must have a `## Related Documents` section.
- Existing downstream documents must be linked with target-relative Markdown links.
- Missing downstream documents must be explicitly marked absent, planned, or not yet created without pretending the path is already link-valid.
- Upstream dependencies (if any) should be noted in the PRD itself.

## Usage Examples

```bash
cp docs/99.templates/prd.template.md docs/01.requirements/YYYY-MM-DD-project-prd.md
```

## How to Work in This Area

1. Read `docs/00.agent-governance/rules/project-initialization-intake.md`.
2. Confirm product/software name, purpose, target users, core features, success criteria, app type, stack, security/data constraints, and operations baseline.
3. Create the first PRD from `docs/99.templates/prd.template.md`.
4. Replace skeleton guidance with project-specific document rows as PRDs are added.
5. Update this README `Documents` table and related links whenever requirements documents change.

## AI Authoring Guidance

1. **Phase 0: Research**: Scan existing PRDs to avoid duplication.
2. **Phase 1: Draft**: Create the document from `prd.template.md`. Set `status: draft`.
3. **Phase 2: Review**: Populate all mandatory sections (Success Criteria, MoSCoW, AC).
4. **Phase 3: Finalize**: Update the document index in this README and move to `status: approved` after the Stage 01 gate passes.

## AI Execution Checklist

- **Entry Gate**: Folder purpose, ownership, and template mapping are known.
- **Exit Gate**: Document index is updated, existing downstream links are verified, and absent downstream documents are explicitly marked.
- **Hard Stop Conditions**: STOP if document index cannot be reconciled with folder contents. STOP if a new PRD implies a downstream ARD, Spec, Plan, or Task exists when it has not been created.
- **Downstream Trigger**: Update the Documents table and Related Documents section when adding, moving, or retiring a PRD in this folder.
- **Evidence Rule**: PRD updates must be reflected in this README immediately.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| [2026-05-30-project-intake-prd.md](./2026-05-30-project-intake-prd.md) | md | Project Initialization Intake | draft | 2026-05-30 |

## Related Documents

- [02.architecture/requirements](../02.architecture/requirements/README.md) - Architecture Reference Models
- [03.specs](../03.specs/README.md) - Technical Specifications
- [04.execution/plans](../04.execution/plans/README.md) - Execution Plans

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
