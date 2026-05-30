---
name: template-patch
description: Applies controlled updates to `docs/99.templates/` without breaking template structure or governance requirements. Use when a template needs a new required section or metadata fix.
---

# Template Patch

Patch documentation templates safely and minimally.

## Workflow

1. Read the target template before editing.
2. Identify whether the request is a field fix, a section addition, or a structural change.
3. Stop and require an ADR if the template change alters the workspace architecture or stage contract.
4. Apply the smallest viable patch.
5. Verify that downstream documents can still conform to the updated template.
6. Keep Stage 10 incident/postmortem paths unified; do not reintroduce retired postmortem-stage paths.

## Rules

- Never rewrite a template from scratch unless the task explicitly requires it.
- Preserve existing sections unless they conflict with active governance.
- Prefer additive changes over reordering.
- Align template metadata, target comments, and `Related Documents` with `stage-gate-matrix.md`.
