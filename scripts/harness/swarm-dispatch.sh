#!/usr/bin/env bash
# swarm-dispatch.sh
# Orchestrates a sequential multi-agent workflow based on the Swarm Protocol.

set -euo pipefail

TASK_ID="${1:-}"
COMMAND="${2:-}"
NEXT_ROLE="${3:-NEXT}"

usage() {
  echo "Usage: ws swarm <task_id> <start|status|handoff|suggest> [next_role]" >&2
}

case "$TASK_ID" in
  start|status|handoff|suggest)
    echo "ERROR: command-first swarm syntax is no longer supported." >&2
    usage
    exit 2
    ;;
esac

if [[ -z "$TASK_ID" || -z "$COMMAND" ]]; then
  usage
  exit 2
fi

SWARM_ROOT="_workspace/swarm/$TASK_ID"

echo "=== Swarm Orchestrator: $TASK_ID ==="

init_swarm() {
  if [[ -d "$SWARM_ROOT" ]]; then
    echo "  ⚠️ Swarm '$TASK_ID' already exists."
  else
    mkdir -p "$SWARM_ROOT"
    echo "status: PM" > "$SWARM_ROOT/swarm_state.yaml"
    echo "  ✅ Swarm initialized for role: PM"
  fi
}

show_status() {
  if [[ ! -f "$SWARM_ROOT/swarm_state.yaml" ]]; then
    echo "  ❌ Error: Swarm '$TASK_ID' not initialized."
    return
  fi
  grep "status:" "$SWARM_ROOT/swarm_state.yaml"
  echo "  Artifacts: $(find "$SWARM_ROOT" -maxdepth 1 | wc -l)"
}

handoff() {
  local NEXT_ROLE="$1"
  local CURRENT_ROLE
  CURRENT_ROLE=$(grep "status:" "$SWARM_ROOT/swarm_state.yaml" | cut -d' ' -f2)

  echo "  Handoff: $CURRENT_ROLE -> $NEXT_ROLE"

  # Archive current state
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  cp "$SWARM_ROOT/swarm_state.yaml" "$SWARM_ROOT/history_${TIMESTAMP}_${CURRENT_ROLE}.yaml"

  # Update state
  echo "status: $NEXT_ROLE" > "$SWARM_ROOT/swarm_state.yaml"
  echo "last_handoff: $TIMESTAMP" >> "$SWARM_ROOT/swarm_state.yaml"

  echo "  ✅ Handoff complete. Next agent should read $SWARM_ROOT/"
}

suggest() {
  echo "🔍 Analyzing proposal for optimal swarm role..."
  PROPOSAL="_workspace/intelligence/proposal.json"
  if [[ -f "$PROPOSAL" ]]; then
    ORPHANS=$(grep -c "path" "$PROPOSAL" || echo 0)
    if [[ $ORPHANS -gt 5 ]]; then
      echo "  💡 Recommendation: [ARCHITECT] (High orphan count detected)"
    else
      echo "  💡 Recommendation: [FULLSTACK] (Standard maintenance)"
    fi
  else
    echo "  💡 Recommendation: [DEVOPS] (Environment hardening suggested)"
  fi
}

case "$COMMAND" in
  start) init_swarm ;;
  status) show_status ;;
  handoff) handoff "$NEXT_ROLE" ;;
  suggest) suggest ;;
  *)
    usage
    exit 1
    ;;
esac
