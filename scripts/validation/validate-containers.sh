#!/usr/bin/env bash
# validate-containers.sh
# Scans Docker images for vulnerabilities and misconfigurations.

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
FAILURES=0

echo "=== Container Security Validation ==="

# Function to scan an image
scan_image() {
  local IMAGE_NAME=$1
  echo "[ Scan ] Checking $IMAGE_NAME..."

  if command -v trivy &> /dev/null; then
    if trivy image --severity HIGH,CRITICAL --exit-code 1 "$IMAGE_NAME"; then
      echo "  ✅ $IMAGE_NAME: OK"
    else
      echo "  ❌ FAIL: High-severity vulnerabilities found in $IMAGE_NAME."
      FAILURES=$((FAILURES + 1))
    fi
  else
    echo "  ⚠️ Trivy not installed. Performing basic image existence check."
    if docker image inspect "$IMAGE_NAME" &> /dev/null; then
      echo "  ✅ $IMAGE_NAME: Exists (Scan skipped)"
    else
      echo "  ⚠️ $IMAGE_NAME: Not found locally."
    fi
  fi
}

if [[ -f "$REPO_ROOT/web/Dockerfile" ]]; then
  scan_image "project-template-web:latest"
else
  echo "  ✅ Web image scan: not required; no active web/Dockerfile."
fi

if [[ -f "$REPO_ROOT/server/Dockerfile" ]]; then
  scan_image "project-template-server:latest"
else
  echo "  ✅ Server image scan: not required; no active server/Dockerfile."
fi

echo ""
if [[ $FAILURES -gt 0 ]]; then
  echo "❌ Container validation FAILED with $FAILURES issues."
  exit 1
else
  echo "✅ All container validations passed (or skipped due to missing tools/images)."
  exit 0
fi
