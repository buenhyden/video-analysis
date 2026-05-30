#!/usr/bin/env bash
# dispatch-subagent.sh
# Creates a transient, governed dispatch packet for an isolated subagent.

set -euo pipefail

TYPE="${1:-}"
SLUG="${2:-}"
MODE="${3:-}"
DATE="$(date +%Y-%m-%d)"

if [[ -z "$TYPE" || -z "$SLUG" ]]; then
  echo "Usage: bash scripts/harness/dispatch-subagent.sh <type> <slug> [--dry-run]"
  echo "Example: bash scripts/harness/dispatch-subagent.sh docs agent-runtime-sync --dry-run"
  exit 1
fi

if [[ "$TYPE" =~ [^a-z0-9_-] ]] || [[ "$SLUG" =~ [^a-z0-9_-] ]]; then
  echo "ERROR: type and slug may contain only lowercase letters, numbers, hyphen, or underscore." >&2
  exit 2
fi

if [[ -n "$MODE" && "$MODE" != "--dry-run" ]]; then
  echo "ERROR: unsupported option '$MODE'." >&2
  exit 2
fi

PACKET_DIR="_workspace/dispatch/${DATE}-${SLUG}"
PACKET_FILE="${PACKET_DIR}/dispatch.md"

render_packet() {
  cat <<EOF
# Subagent Dispatch Packet

## Mission

- Type: \`${TYPE}\`
- Slug: \`${SLUG}\`
- Stage: identify from \`docs/00.agent-governance/rules/stage-gate-matrix.md\`
- Scope: identify from \`docs/00.agent-governance/rules/persona.md\`

## Required Reading

- \`AGENTS.md\`
- \`docs/00.agent-governance/rules/bootstrap.md\`
- \`docs/00.agent-governance/rules/persona.md\`
- \`docs/00.agent-governance/rules/subagent-protocol.md\`
- Target stage README and parent Stage 05/06 documents

## Constraints

- Write only inside the assigned paths from the lead agent.
- Do not create branches, commits, PRs, or protected-branch pushes.
- Do not write authoritative final outputs under \`_workspace/**\`.
- Use relative repository paths only; do not emit machine-specific absolute links.
- Report back to the lead agent with changed paths and validation evidence.

## Validation

- Run the narrowest relevant checks.
- For governed changes, run \`bash scripts/ws.sh validate\` before final handoff when feasible.

## Transient Record

- Packet path: \`${PACKET_FILE}\`
- This packet is local coordination state and is ignored by Git.
EOF
}

if [[ "$MODE" == "--dry-run" ]]; then
  render_packet
  exit 0
fi

mkdir -p "$PACKET_DIR"
render_packet > "$PACKET_FILE"

echo "=== Subagent Dispatch Packet ==="
echo "Packet: $PACKET_FILE"
echo "Type: $TYPE"
echo "Slug: $SLUG"
echo "Status: created"
