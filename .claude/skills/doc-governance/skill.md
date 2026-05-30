---
name: doc-governance
description: Validates and enforces document governance for the active workspace. Checks reference integrity, README consistency, stage alignment, and language policy across governed documentation.
---

# Doc Governance

Validate the governed documentation surface for this workspace.

## Checks

### 1. Reference Integrity

- Confirm every `@` import and markdown link resolves.
- Confirm root router files point to the canonical governance files.

### 2. README Consistency

- Confirm each governed directory README reflects the files it indexes.
- Repair obvious README drift when the fix is mechanical and safe.

### 3. Stage Alignment

- Confirm stage documents live in the correct `docs/<stage>/` directory.
- Confirm stage-gate expectations still match the current document layout.

### 4. Language Policy

- `docs/00.agent-governance/` must stay English-only.
- Root governance router files must stay English-only.
- Report violations instead of silently rewriting broad content.

### 5. Thin Root Compliance

- `AGENTS.md`, `CLAUDE.md`, and provider overlays should remain thin routers.

## Output

Return a compact report with:

- passes
- warnings
- failures
- required follow-up actions
