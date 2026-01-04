#!/bin/bash
set -euo pipefail

# Only run in remote Claude Code environment
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Install Python dependencies from requirements.txt
# Using --ignore-installed to avoid conflicts with system packages
pip install --ignore-installed -r "$CLAUDE_PROJECT_DIR/requirements.txt"

# Install development tools for linting and testing
pip install ruff pytest
