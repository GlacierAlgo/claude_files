#!/usr/bin/env bash
# PreToolUse hook - block npm commands
# Exit 2 to block the tool call, exit 0 to allow

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -qE "(^|[;&|[:space:]])npm([[:space:]]|$)"; then
    # stderr becomes Claude's feedback
    echo "npm is blocked. Use pnpm for JS/TS instead." >&2
    # exit 2 = block this action
    exit 2
fi

exit 0  # let it proceed
