#!/usr/bin/env bash
# PreToolUse hook - block pip install commands
# Exit 2 to block the tool call, exit 0 to allow

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -qE "(^|[;&|[:space:]])pip([0-9]*)([[:space:]]|$)"; then
    echo "pip is blocked. Use uv for Python package management instead (e.g. 'uv add <package>' or 'uv pip install <package>')." >&2
    exit 2
fi

exit 0
