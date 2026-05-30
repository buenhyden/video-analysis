---
title: Session Progress
version: 1.0.0
owner: Governance Architect
layer: meta
stage: 00
status: active
last-updated: YYYY-MM-DD
---

# Session Progress

<!-- Target: docs/00.agent-governance/memory/progress.md -->

## Usage Guidance

- **When to use**: Update this file during governed AI-agent work when the task spans multiple steps, stages, or handoffs.
- **Mandatory sections**: Active Task, Phase Progress, Durable Memory Notes, Key Decisions, Blockers, Next Sync.
- **Naming rule**: This template is only for `docs/00.agent-governance/memory/progress.md`.
- **Hard Stops**: STOP if progress is being written to `_workspace/progress.md` or another transient path as authoritative memory. STOP if the note is policy rather than progress or durable memory.

## Purpose

`progress.md` is the canonical tracked progress surface for the current governed AI-agent run. It records active task state, phase progress, and durable memory notes that help the next agent resume without treating transient `_workspace/**` output as authority.

## Active Task

| Field | Value |
| :--- | :--- |
| Task ID | [short id or request summary] |
| Description | [current task] |
| Active Persona | [persona or agent role] |
| Stage | [00-05 / 90 / 99 or docs path] |
| Status | [not-started / in-progress / blocked / completed] |
| Started | YYYY-MM-DD |
| Last Updated | YYYY-MM-DD |

## Phase Progress

| Phase | Status | Evidence |
| :--- | :--- | :--- |
| Investigate | [pending / in-progress / complete] | [repo scan, command, or source link] |
| Plan | [pending / in-progress / complete] | [plan or criteria] |
| Execute | [pending / in-progress / complete] | [changed docs or code] |
| Validate | [pending / in-progress / complete] | [validation command] |
| Sync | [pending / in-progress / complete] | [README, LLM-WIKI, policy log, or memory update] |

## Durable Memory Notes

- [Only non-obvious context that should survive this run.]

## Key Decisions

| Decision | Rationale | Impact |
| :--- | :--- | :--- |
| [Decision] | [Rationale] | [Impact] |

## Blockers

| Blocker | Owner | Resolution |
| :--- | :--- | :--- |
| [Blocker] | [Owner] | [Resolution] |

## Next Sync

- [What the next agent should read or update next.]

## Target-Relative Link Guidance

- This file lives at `docs/00.agent-governance/memory/progress.md`.
- Link Stage 00 sibling rules with `../rules/<rule>.md`.
- Link execution evidence as `[../../04.execution/tasks/YYYY-MM-DD-<task-name>.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

### Entry Gate

- [ ] A governed task is in progress or a durable memory note is needed.
- [ ] `docs/00.agent-governance/memory/` is the correct authority for this information.

### Exit Gate

- [ ] Active task status, phase progress, and next sync are current.
- [ ] Durable notes are non-obvious, source-backed, and free of secrets.

### Hard Stop Conditions

- [ ] STOP if `_workspace/**` is being used as authoritative progress, methodology, or memory.
- [ ] STOP if the entry is actually a policy change; update `docs/00.agent-governance/policy-change-log.md` instead.
- [ ] STOP if the entry contains secrets, credentials, tokens, private keys, or sensitive logs.

### Downstream Trigger

- [ ] Update this file at phase boundaries, handoffs, blockers, and task closure.

### Evidence Rule

- [ ] Link or name the source task, plan, validation command, ADR, or user request that justifies the progress/memory note.

## Related Documents

- [Memory README](./README.md)
- [Documentation Protocol](../rules/documentation-protocol.md)
- [Policy Change Log](../policy-change-log.md)
