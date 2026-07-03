---
title: References Hub
version: 1.0.0
owner: Wiki Curator
layer: references
stage: 90
status: active
last-updated: 2026-05-21
---

# References Skeleton

> 새 프로젝트의 factual reference와 external knowledge를 정리하기 위한 release skeleton.

## Overview

`docs/90.references/`는 파생 프로젝트에서 factual reference, external system notes, research summaries, integration references를 보관하는 stage이다. `main` release branch에서는 generated navigation, intelligence dumps, video-analysis history, old reference documents를 보관하지 않는다.

파생 프로젝트에서는 product/software intake와 stack 선택 후 필요한 reference documents를 생성한다. Reference material은 정책이나 실행 지시의 source of truth가 아니며, governing docs는 Stage 00-05에 둔다.

아래 reference rows는 `dev`에서 유지하는 video-analysis contract 또는 archive/reference history다. 새 프로젝트에서는 필요한 사실 근거만 `reference.template.md`에서 새로 작성한다.

## Audience

이 README의 주요 독자:

- Knowledge curators
- Engineers and reviewers
- AI agents
- Project maintainers

## Scope

### In Scope

- Project-specific factual references
- External service, protocol, vendor, research, and integration notes
- Links that support requirements, architecture, specs, operations, or decisions

### Out of Scope

- Generated LLM navigation indexes
- Governance rules or active runtime policy
- Execution plans, task evidence, runbooks, incidents
- Template repository historical references

## Structure

```text
90.references/
└── README.md    # Release skeleton guide for reference authoring
```

## Mandatory Templates

- This README follows `docs/99.templates/readme.template.md`.
- New references must start from `docs/99.templates/reference.template.md`.

## Naming Rules

- Use `YYYY-MM-DD-<reference-slug>.md` for time-bound research or external context.
- Use stable kebab-case names for durable reference material.
- Do not store generated navigation or agent scratchpad output here.
- Path portability: keep generated relative paths <= 140 chars, current absolute paths <= 220 chars, path segments <= 80 chars, and use lowercase kebab-case slugs with no spaces or Windows-reserved characters.

## Lifecycle Rules

Documents in this folder follow the standard lifecycle:

1. **draft**: Initial creation from template. Not yet for implementation.
2. **active**: Reviewed and approved as a citation source for scoped facts, provenance, and slow-changing reference material. Active references do not own downstream requirements, decisions, plans, tasks, policies, or procedures.
3. **deprecated**: Replaced by a newer reference or no longer reliable.
4. **archived**: Retained only for historical audit.

Reference documents must declare a review trigger or freshness expectation when the facts can drift.

## Cross-Reference Rules

- Link the requirements, architecture, specs, plans, or operations documents that use the reference.
- Record source provenance and retrieval date where applicable.
- Do not let references override Stage 00 governance or current project docs.

## Usage Examples

```bash
cp docs/99.templates/reference.template.md docs/90.references/YYYY-MM-DD-external-service-reference.md
```

## How to Work in This Area

1. Confirm the reference is needed for the derived project.
2. Create the document from the approved template.
3. Keep source provenance and project relevance explicit.
4. Update this README when reference files are added, renamed, deprecated, or removed.

## Source and Provenance Guidance

- Prefer primary sources or owning repo-local documents over summaries.
- Record the source owner, retrieval date, reviewed snapshot, or internal evidence basis when facts can drift.
- Treat generated indexes, graph output, and `_workspace/**` material as supporting inputs until source inspection or governance review confirms the fact.
- Do not use references to approve requirements, make decisions, authorize execution, define policy, or close operational procedures.

## File Selection Guidance

The `main` release-template skeleton omits generated navigation and generated
intelligence history. Derived projects should create reviewed reference files
only when they have a concrete source, owner, retrieval or review date, and
project relevance.

| Need | Use | Do Not Use For |
| --- | --- | --- |
| Record sourced technical facts | New project-owned reference from `docs/99.templates/reference.template.md` | Requirements, decisions, execution approval, or policy ownership |
| Preserve generated or local intelligence | Local `_workspace/**` output until reviewed and promoted | Canonical docs, Stage 00 governance, or runtime policy |
| Navigate AI operating context | [LLM-WIKI](../LLM-WIKI.md) and Stage 00 governance | Replacing project-owned references after intake |

## AI Authoring Guidance

- Do not place generated wiki indexes or video-analysis intelligence history here.
- Do not treat reference notes as policy.
- In a derived project, rewrite skeleton rows to match actual reference materials.

## AI Execution Checklist

- [ ] Reference purpose and source are clear.
- [ ] Reference uses `docs/99.templates/reference.template.md`.
- [ ] Downstream documents that rely on the reference are linked.
- [ ] Stale or obsolete sources are marked or removed.
- [ ] The `Documents` table reflects actual files in this folder.

## Documents

| File | Type | Summary | Status | Last Modified |
| --- | --- | --- | --- | --- |
| _No documents yet_ | — | This stage has been reset for new project use. | — | — |

## Related Documents

- [LLM-WIKI.md](../LLM-WIKI.md) - Workspace SDLC Rules
- [00.agent-governance/rules/](../00.agent-governance/rules/) - Governance Standards

---

## Docs 3 Global Rules Reference

Docs 3 rules are authoritative in [Documentation Protocol §7](../00.agent-governance/rules/documentation-protocol.md). In short: read the matching template before creating governed docs, refresh README indexes after docs changes, and keep relative `## Related Documents` links valid.
