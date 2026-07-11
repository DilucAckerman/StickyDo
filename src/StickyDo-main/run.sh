#!/usr/bin/env bash
# StickyDo launcher — handles the LD_PRELOAD requirement for gtk4-layer-shell

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAYER_SHELL_LIB=$(find /usr/lib -name "libgtk4-layer-shell.so*" 2>/dev/null | head -n 1)

if [ -z "$LAYER_SHELL_LIB" ]; then
    echo "Error: libgtk4-layer-shell.so not found. Is gtk4-layer-shell installed?" >&2
    exit 1
fi

source "$PROJECT_DIR/venv/bin/activate"
LD_PRELOAD="$LAYER_SHELL_LIB" python3 -m stickydo.app
