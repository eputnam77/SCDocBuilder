#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${1:-scdocbuilder}"
REGISTRY="${2:-}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

docker build -t "$IMAGE_NAME" "$REPO_ROOT"

if [ -n "$REGISTRY" ]; then
  docker tag "$IMAGE_NAME" "$REGISTRY/$IMAGE_NAME"
  docker push "$REGISTRY/$IMAGE_NAME"
fi
