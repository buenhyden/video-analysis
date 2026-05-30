# Subagent Protocol (April 2026)

This document defines when and how to create subagents, their hierarchy, file ownership enforcement, and acceptance criteria.

## 1. When to Create Subagents

Create an isolated subagent when ALL of the following are true:

1. The task maps to a single persona/scope boundary (e.g., pure backend work, pure frontend work).
2. The task has well-defined inputs (files, specs) available before spawn.
3. The task output can be verified independently (tests, lint, ref integrity).
4. The task does not require real-time coordination with another active agent.

Do NOT spawn a subagent for:

- Exploratory or ambiguous tasks (use lead agent).
- Tasks that require reading main-context session history.
- Tasks with overlapping file ownership with another active agent.

## 2. Lead / Subagent Hierarchy

```text
Lead Agent (persistent context)
├── decomposes task into bounded subtasks
├── verifies file ownership non-overlap before spawn
├── spawns subagents via Task tool
├── collects and integrates results
└── runs postflight after all subtasks complete

Subagent (isolated context)
├── receives: task description + input paths + scope file
├── reads input documents independently
├── writes only to declared Allowed Write paths
├── reports result summary to lead only
└── does NOT communicate with other subagents
```

## 3. Concurrency Limits

- **Maximum concurrent subagents**: 5
- **Recommended**: 3
- More agents increases coordination overhead; prefer fewer, focused agents.

## 4. File Ownership Enforcement

Before spawning parallel subagents, the lead agent MUST verify:

| Check | Rule |
| :--- | :--- |
| Path overlap | No two active subagents share a write path |
| Upstream dependency | Downstream subagent waits for upstream output |
| Scope match | Each subagent's scope file declares the write paths used |

Resolve overlaps by sequencing (not parallelizing) the conflicting agents.

## 5. Subagent Spawn Format

When using the Task tool, include in the system prompt:

```text
Role: <Persona Name>
Scope: <layer>
Stage: <XX>
Allowed Write: <paths>
Forbidden Write: <paths>
Input Documents: <paths>
Task: <single bounded description>
Report to: lead agent only
```

Reference the matching `.claude/agents/<role>.md` file for full persona definition.

## 6. Context Isolation Rules

- Subagents start with a fresh context window — never paste raw session history.
- Pass only the minimum required: task description + input file paths + scope constraints.
- Subagents must not read each other's outputs directly; lead agent integrates results.

## 7. Acceptance Checklist

The lead agent must verify before accepting a subagent result:

- [ ] All declared output files exist at the expected paths.
- [ ] Tests pass (if applicable to the task scope).
- [ ] Lint passes (hook reports no failures).
- [ ] Reference integrity check passes (`scripts/validation/validate-cross-links.sh`).
- [ ] Completion summary matches the task description.
- [ ] No writes outside declared Allowed Write paths.

Reject and re-spawn (max 2 retries) if any check fails. After 2 failures, escalate to human.

## 8. Escalation

Escalate to `meta` / Governance Architect if:

- Two subagents produce conflicting outputs for the same file.
- A subagent's scope file does not cover the required write paths.
- Acceptance checklist fails after 2 retries.

## Role definition

- Applies generally to the workspace.

## Procedure

- Follow instructions outlined above.

## Constraints

- Ensure compliance with overall workspace SDLC.

## File references

- `docs/LLM-WIKI.md`
