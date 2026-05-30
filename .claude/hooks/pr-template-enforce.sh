#!/usr/bin/env bash
# Compatibility wrapper for the broader Git policy enforcement hook.

set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$HOOK_DIR/git-policy-enforce.sh"
