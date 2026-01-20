#!/usr/bin/env bash

# Exit on any error
set -e

# Determine repo root relative to this wrapper
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_SCRIPT="${SCRIPT_DIR}/scripts/setup.py"

if [ ! -f "$TARGET_SCRIPT" ]; then
    echo "Cannot find scripts/setup.py next to this wrapper." >&2
    exit 1
fi

echo "Delegating to scripts/setup.py..."
exec python "$TARGET_SCRIPT" "$@"