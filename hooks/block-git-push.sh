#!/usr/bin/env bash
# PreToolUse hook - block git push commands
# Exit 2 to block the tool call, exit 0 to allow

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -qE "(^|[;&|[:space:]])git\s+push([[:space:]]|$)"; then
    echo "git push is blocked. Push manually after reviewing changes." >&2
    exit 2
fi

exit 0  # let it proceed
