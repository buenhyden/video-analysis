---
title: <string>
version: <string>
owner: <string>
layer: architecture
stage: 02
status: draft
last-updated: YYYY-MM-DD
---

# Ubiquitous Language Glossary

<!-- Target: docs/02.architecture/requirements/####-ubiquitous-language-<domain>.md -->

## Usage Guidance

- **When to use**: When domain vocabulary is complex, ambiguous, or shared across multiple teams/contexts.
- **Mandatory sections**: Overview, Glossary, Homonyms & Context Collisions.
- **Naming rule**: `####-ubiquitous-language-<domain>.md`.
- **Hard Stops**: STOP if no parent ARD/Bounded Context identifies vocabulary ambiguity. STOP if terms are not scoped to a specific context.

## Purpose

The Ubiquitous Language Glossary ensures that every person (and agent) working in a domain uses the same terms for the same concepts. It eliminates ambiguity and ensures that the language of the business is reflected in the code.

---

## Overview (KR)

이 문서는 [도메인명]의 유비쿼터스 언어 용어집이다. 팀 전체가 동일한 언어로 도메인을 이해하고
설계·구현·테스트에 일관성을 유지하기 위한 기준 문서다.

## Bounded Context

- **Context**: [BoundedContextName]
- **Domain**: [Domain name]
- **Owner**: [Team or owner]
- **Last Reviewed**: YYYY-MM-DD

## Glossary

### Core Terms

| Term | Korean | Definition | Example | Notes |
| :--- | :--- | :--- | :--- | :--- |
| [Term] | [한국어] | [Precise domain definition] | [Concrete example] | [Disambiguation if needed] |

### Aggregates & Entities

| Name | Korean | Type | Invariant | Lifecycle |
| :--- | :--- | :--- | :--- | :--- |
| [AggregateName] | [한국어] | Aggregate Root | [Core business rule] | [created → active → closed] |
| [EntityName] | [한국어] | Entity | [Rule] | [lifecycle] |
| [ValueName] | [한국어] | Value Object | [Equality rule] | Immutable |

### Domain Events

| Event | Korean | Meaning | When Raised |
| :--- | :--- | :--- | :--- |
| [EventName] | [한국어] | [What happened in the domain] | [Trigger condition] |

### Commands & Queries

| Command / Query | Korean | Intent | Actor |
| :--- | :--- | :--- | :--- |
| [CommandName] | [한국어] | [What it requests] | [Who initiates] |

### Policies & Rules

| Policy | Korean | Definition | Source |
| :--- | :--- | :--- | :--- |
| [PolicyName] | [한국어] | [The business rule] | [PRD/Spec reference] |

## Homonyms & Context Collisions

> Terms that appear in multiple contexts with different meanings.

| Term | This Context Meaning | Other Context | Other Meaning |
| :--- | :--- | :--- | :--- |
| [Term] | [Meaning here] | [ContextName] | [Different meaning] |

## AI Execution Checklist

- [ ] **Entry Gate**: ARD DDD trigger identifies vocabulary ambiguity or domain language changes.
- [ ] **Exit Gate**: Core terms, synonyms, forbidden terms, and open questions are recorded.

### Hard Stop Conditions

- **STOP** if no parent ARD or bounded context identifies vocabulary ambiguity. STOP if terms are not tied to an owning context.
- [ ] **Downstream Trigger**: Update ARD, bounded context, domain model, Spec, and user-facing guides.
- [ ] **Evidence Rule**: Term decisions cite domain expert review, source docs, or accepted usage.

## Related Documents

- **Bounded Context**: `[./####-<bounded-context-name>.md]`
- **Parent ARD**: `[./####-<system-or-domain>.md]`
- **PRD**: `[../../01.requirements/YYYY-MM-DD-<feature-or-system>.md]`
- **Data Model**: `[../../03.specs/<feature-id>/data-model.md]`
