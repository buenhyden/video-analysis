#!/usr/bin/env bash
# collect-context.sh
# Gathers deep diagnostic data (Logs, System, Network) for failure analysis.

set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DIAG_DIR="_workspace/diagnostics/$TIMESTAMP"
mkdir -p "$DIAG_DIR"

echo "=== Collecting Deep Diagnostic Context ==="

# 1. Logs
echo "[ Context 1 ] Tail of recent logs..."
if [[ -d "server/logs" ]]; then
  tail -n 100 server/logs/*.log > "$DIAG_DIR/server_logs.txt" 2>/dev/null || true
fi
if [[ -f "docker-compose.yml" ]] && command -v docker-compose >/dev/null 2>&1; then
  docker-compose logs --tail=100 > "$DIAG_DIR/docker_logs.txt" 2>/dev/null || true
fi

# 2. System Metrics (CPU/Mem)
echo "[ Context 2 ] System snapshot (top)..."
top -b -n 1 > "$DIAG_DIR/system_top.txt"

# 3. Network Status
echo "[ Context 3 ] Network snapshot (netstat)..."
if command -v netstat &> /dev/null; then
  netstat -tulpn > "$DIAG_DIR/network_ports.txt" 2>/dev/null || true
else
  lsof -i -P -n > "$DIAG_DIR/network_ports.txt" 2>/dev/null || true
fi

# 4. Git State
echo "[ Context 4 ] Git state..."
git log -n 5 --oneline > "$DIAG_DIR/git_history.txt"
git diff > "$DIAG_DIR/uncommitted_changes.diff"

echo ""
echo "✅ Diagnostic bundle created at: $DIAG_DIR"
echo "   Please provide this bundle to your AI agent for rapid debugging."
exit 0
