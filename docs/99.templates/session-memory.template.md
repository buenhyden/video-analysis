---
title: <string>
version: <string>
owner: <string>
layer: meta
stage: 00
status: draft
last-updated: YYYY-MM-DD
---

# Durable Session Memory

<!-- Target: docs/00.agent-governance/memory/YYYY-MM-DD-<slug>.md -->

## Usage Guidance

- **When to use**: To record long-term technical insights, lessons learned, or focused memory notes that should survive the current run.
- **Mandatory sections**: Technical Memory, Decision & Blocker Log, AI Execution Checklist, Related Documents.
- **Naming rule**: `YYYY-MM-DD-<slug>.md`.
- **Hard Stops**: STOP if the note is active progress that belongs in `progress.md`. STOP if insights are trivial.

## Purpose

Durable Session Memory records technical knowledge gained during development. Active task state belongs in `docs/00.agent-governance/memory/progress.md`.

## 1. Active Task Progress (Session Context)

| Field | Value |
| :--- | :--- |
| Task ID | [ID] |
| Description | [Description] |
| Active Persona | [Persona] |
| Stage | [00-05 / 90 / 99 or docs path] |
| Started | [YYYY-MM-DD] |

### Completed Steps

- [x] Step 1
- [/] Step 2

### Pending Steps

- [ ] Step 3

---

## 2. Technical Memory (Lessons Learned)

- **Target Layer**: [Backend/Infra/etc.]
- **Tags**: #performance #bug #config

### Problem / Challenge

[Describe the issue or challenge encountered.]

### Solution / Implementation

[How was it solved? Provide code snippets or config changes.]

### Prevention / Guidance

[How to avoid this in the future? Checklists, refactoring, etc.]

---

## 3. Decision & Blocker Log

### Key Decisions

| Decision | Rationale | Impact |
| :--- | :--- | :--- |
| [Decision] | [Rationale] | [Impact] |

### Blockers

| Blocker | Owner | Resolution |
| :--- | :--- | :--- |
| [Blocker] | [Owner] | [Resolution] |

---

## Target-Relative Link Guidance

- This file lives under `docs/00.agent-governance/memory/`; Stage 00 siblings use `../`.
- Link active task evidence as `[../../04.execution/tasks/YYYY-MM-DD-<task-name>.md]`.
- Link incident postmortems as `[../../05.operations/incidents/YYYY/INC-###/postmortem.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

### Entry Gate

- [ ] A non-obvious technical insight or lesson learned has been identified.

### Exit Gate

- [ ] Technical Memory sections are complete and actionable.

### Hard Stop Conditions

- **STOP** if the content is active task progress for `progress.md`.
- **STOP** if the insight is trivial or already documented.
- **STOP** if the solution contains secrets or absolute local paths.

### Downstream Trigger

- [ ] Update parent task/plan on milestone completion.

### Evidence Rule

- [ ] MUST include links to the original issue, PR, or incident postmortem.

## Related Documents

- **Governance README**: `[./README.md]`
- **Active Task**: `[../../04.execution/tasks/YYYY-MM-DD-<task-name>.md]`
- **Incident Postmortem**: `[../../05.operations/incidents/YYYY/INC-###/postmortem.md]` (if applicable)
