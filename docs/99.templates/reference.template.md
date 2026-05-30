---
title: <string>
version: <string>
owner: <string>
layer: references
stage: 90
status: draft
last-updated: YYYY-MM-DD
---

# Reference

<!-- Target: docs/90.references/YYYY-MM-DD-<slug>.md OR docs/90.references/<slug>.md OR docs/90.references/knowledge/<slug>.md -->

## Usage Guidance

- **When to use**: For stable or slow-changing reference material, glossaries, factual matrices, provenance-backed summaries, or external standard summaries used across multiple stages.
- **Mandatory sections**: Purpose, Overview, Scope, Definitions / Facts, Sources, AI Execution Checklist, Related Documents.
- **Naming rule**: `<slug>.md` for evergreen facts, `YYYY-MM-DD-<slug>.md` for dated snapshots, or `knowledge/<slug>.md` for reviewed knowledge references.
- **Hard Stops**: STOP if content belongs in a stage-specific document. STOP if no source, owner, review basis, or provenance is identified. STOP if the reference would make generated `_workspace/**` output authoritative.
- **Generation rule**: For derived-project seeds, keep `status: draft`, replace bracketed prompts with project facts or `TODO:`, and do not copy Project-Template generated intelligence as authoritative project reference material.
- **Lifecycle reference**: Apply `docs/00.agent-governance/rules/template-document-lifecycle.md` before reusing inherited documents.

## Purpose

The Reference document provides a stable citation point for domain terms, standards, factual matrices, and static facts used across the workspace.

---

## Overview (KR)

이 문서는 [주제]에 대한 참고 문서다. 느리게 변하는 기준 정보, 용어, 외부 표준 요약, 출처가 확인된 사실을 정리한다.

## Objectives

[Why this reference exists.]

## Scope

### In Scope

- [What stable facts, terms, standards, or provenance this reference covers]

### Out of Scope

- [Requirements, decisions, execution plans, operational procedures, or other content owned by another docs stage]

## Reference Classification

| Field | Value |
| --- | --- |
| Reference type | [Glossary / Standard / Repository intelligence / External-source summary / Factual matrix / Other] |
| Stability | [Static / Slow-changing / Dated snapshot] |
| Freshness trigger | [When this document must be reviewed] |
| Owning source | [Internal owner or external source] |

## Definitions / Facts

- **Term / Fact 1**:
- **Term / Fact 2**:

## Sources

- [Source 1]
- [Source 2]

## Target-Relative Link Guidance

Keep placeholder paths as code spans until a generated document links to an existing file.

| Target Location | ARD Example | Spec Example | Documentation Protocol Example |
| --- | --- | --- | --- |
| `docs/90.references/<slug>.md` | `[../02.architecture/requirements/####-<system-or-domain-name>.md]` | `[../03.specs/<feature-id>/spec.md]` | `[../00.agent-governance/rules/documentation-protocol.md]` |
| `docs/90.references/knowledge/<slug>.md` | `[../../02.architecture/requirements/####-<system-or-domain-name>.md]` | `[../../03.specs/<feature-id>/spec.md]` | `[../../00.agent-governance/rules/documentation-protocol.md]` |

## Implementation Guidance

- [How agents or humans should use this reference]
- [What this reference must not be used to decide or authorize]

## AI Execution Checklist

### Entry Gate

- [ ] Content is stable reference material rather than a requirement, decision, plan, task, policy, runbook, incident, or procedure.
- [ ] Source or ownership basis is known.

### Exit Gate

- [ ] Ownership, source, freshness trigger, usage guidance, and related documents are clear.
- [ ] Terms or facts do not duplicate canonical stage documents.

### Hard Stop Conditions

- [ ] STOP if the content belongs in `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`, `docs/04.execution/`, `docs/05.operations/`, or `docs/00.agent-governance/memory/`.
- [ ] STOP if no source, owner, or provenance basis is available.
- [ ] STOP if generated `_workspace/**` output is being promoted without source inspection or governed review.

### Downstream Trigger

- [ ] Update stage documents that rely on this reference when it changes.

### Evidence Rule

- [ ] Record source, review basis, provenance, and freshness trigger.

## Related Documents

- **ARD**: `[../02.architecture/requirements/####-<system-or-domain-name>.md]`
- **Spec**: `[../03.specs/<feature-id>/spec.md]`
