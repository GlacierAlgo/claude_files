#!/usr/bin/env bash
# PreToolUse hook - block git push commands
# Exit 2 to block the tool call, exit 0 to allow

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# Strip quoted strings before scanning, so 'git push' inside -m "..." is ignored
STRIPPED=$(echo "$COMMAND" | sed "s/\"[^\"]*\"//g; s/'[^']*'//g")

if echo "$STRIPPED" | awk '
{
    n = split($0, tokens, /[[:space:]]+/)
    for (i = 1; i <= n; i++) {
        t = tokens[i]
        gsub(/^[;&|]+/, "", t)
        if (t == "git" && i < n) {
            next_t = tokens[i+1]
            gsub(/^[;&|]+/, "", next_t)
            if (next_t == "push") { exit 0 }
        }
    }
    exit 1
}'; then
    echo "git push is blocked. Push manually after reviewing changes." >&2
    exit 2
fi

exit 0  # let it proceed
