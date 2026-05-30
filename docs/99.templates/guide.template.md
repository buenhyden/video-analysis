---
title: <string>
version: <string>
owner: <string>
layer: docs
stage: 05
status: draft
last-updated: YYYY-MM-DD
---

# Guide

<!-- Target: docs/05.operations/guides/<slug>.md OR docs/05.operations/guides/YYYY-MM-DD-<slug>.md -->

## Usage Guidance

- **When to use**: To explain "how to" do something or "how to" understand a system.
- **Mandatory sections**: Overview, Target Audience, Step-by-step Instructions.
- **Naming rule**: `<slug>.md` for evergreen guides, `YYYY-MM-DD-<slug>.md` for dated or historical guides.
- **Hard Stops**: STOP if behavior hasn't passed execution verification. STOP if command order is critical (use Runbook).
- **Generation rule**: For derived-project seeds, keep `status: draft`, replace bracketed prompts with project facts or `TODO:`, and do not copy Project-Template maintenance guides as active project guidance.
- **Lifecycle reference**: Apply `docs/00.agent-governance/rules/template-document-lifecycle.md` before reusing inherited documents.

## Purpose

The Guide provides educational and procedural information for developers or operators to successfully interact with a system or feature.

---

## Overview (KR)

이 문서는 [주제]에 대한 가이드다. 특정 대상 독자가 작업을 이해하고 재현할 수 있도록 단계별 절차와 주의사항을 제공한다.

## Version & Applies To

- **Version**: 1.0
- **Applies To**: [System / feature / tool name and version range]
- **Last Reviewed**: YYYY-MM-DD

## Guide Type

`onboarding | how-to | style-guide | troubleshooting-guide | system-guide`

## Target Audience

- Developer
- Operator
- Contributor
- Agent-tuner

## Objectives

[What this guide helps the reader achieve.]

## Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]

## Step-by-step Instructions

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Common Pitfalls

- [Pitfall 1]
- [Pitfall 2]

## Troubleshooting

| Symptom | Likely Cause | Resolution |
| --- | --- | --- |
| [Symptom 1] | [Cause] | [Fix / command] |
| [Symptom 2] | [Cause] | [Fix / command] |

## Evidence / Verification

- [Command output, task evidence, reviewer sign-off, screenshot, or dry-run log proving the guide is accurate.]

## Target-Relative Link Guidance

- This file lives under `docs/05.operations/guides/`; links to sibling operations folders use `../`.
- Link upstream behavior evidence as `[../../03.specs/<feature-id>/spec.md]` or `[../../04.execution/tasks/YYYY-MM-DD-<feature>.md]`.
- Link policy and runbook companions as `[../policies/<policy-or-standard>.md]` and `[../runbooks/<topic>.md]`.
- Keep placeholder paths as code spans until the generated target exists.

## AI Execution Checklist

- **Entry Gate**: behavior is stable and upstream Spec/Task evidence exists.
- **Exit Gate**: audience, prerequisites, steps, pitfalls, and troubleshooting are reproducible.
- **Hard Stop Conditions**: STOP if the behavior being documented has not passed `docs/04.execution/tasks/` evidence. STOP if prerequisite steps reference system behavior that is undocumented or still changing.
- **Downstream Trigger**: update operations or runbooks if the guide includes operational action.
- **Evidence Rule**: MUST capture specific dry-run logs, reviewer sign-off links, or verification screenshots.

## Related Documents

- **Spec**: `[../../03.specs/<feature-id>/spec.md]`
- **Operation**: `[../policies/<policy-or-standard>.md]`
- **Runbook**: `[../runbooks/<topic>.md]`
