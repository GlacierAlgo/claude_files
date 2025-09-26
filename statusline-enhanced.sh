#!/bin/bash

# Enhanced status line for Claude Code with git version and detailed folder info
# GitHub: https://github.com/GlacierAlgo/claude_files
# Version: 1.1.0
# Author: yanghh
#
# Features:
# - Shell prompt-style display (user@host:path)
# - Smart directory display with project context
# - Git branch, version (short hash), and status indicators
# - Claude model and output style integration
# - Fallback support for systems without jq
#
# Installation: Place in ~/.claude/ and configure in settings.json:
# {
#   "statusLine": {
#     "type": "command",
#     "command": "bash ~/.claude/statusline-enhanced.sh"
#   }
# }
#
# Debug output goes to stderr, status line goes to stdout

# Read Claude Code session data from stdin with timeout
input=$(timeout 1s cat 2>/dev/null || echo '{}')

# Check if jq is available, fallback to basic parsing if not
if command -v jq >/dev/null 2>&1; then
    model_name=$(echo "$input" | jq -r '.model.display_name // empty' 2>/dev/null)
    output_style=$(echo "$input" | jq -r '.output_style.name // empty' 2>/dev/null)
    current_dir=$(echo "$input" | jq -r '.workspace.current_dir // empty' 2>/dev/null)
    project_dir=$(echo "$input" | jq -r '.workspace.project_dir // empty' 2>/dev/null)
else
    # Fallback parsing without jq (basic grep/sed approach)
    model_name=$(echo "$input" | grep -o '"display_name":"[^"]*"' | sed 's/"display_name":"//; s/"//' 2>/dev/null || echo "")
    output_style=$(echo "$input" | grep -o '"name":"[^"]*"' | sed 's/"name":"//; s/"//' 2>/dev/null || echo "")
    current_dir=""
    project_dir=""
fi

# Get directory info - use workspace current_dir if available, otherwise pwd
if [ -n "$current_dir" ] && [ "$current_dir" != "null" ] && [ -d "$current_dir" ]; then
    dir_full="$current_dir"
else
    dir_full="$(pwd)"
fi

# Base status line components
user_host_part=$(printf '\033[32m%s@%s\033[0m' "$(whoami)" "$(hostname -s)")

# Enhanced directory display with project context
if [ -n "$project_dir" ] && [ "$project_dir" != "null" ] && [ "$project_dir" != "empty" ] && [ "$dir_full" != "$project_dir" ]; then
    # Show project/relative_path format
    project_name=$(basename "$project_dir")
    if command -v realpath >/dev/null 2>&1; then
        rel_path=$(realpath --relative-to="$project_dir" "$dir_full" 2>/dev/null || basename "$dir_full")
    else
        # Fallback: simple string replacement
        rel_path=$(echo "$dir_full" | sed "s|^${project_dir}/||" 2>/dev/null || basename "$dir_full")
    fi

    if [ "$rel_path" = "$dir_full" ]; then
        # Fallback to simple basename if relative path calculation failed
        dir_part=$(printf '\033[1;34m%s\033[0m' "$(basename "$dir_full")")
    else
        dir_part=$(printf '\033[1;34m%s\033[0m/\033[36m%s\033[0m' "$project_name" "$rel_path")
    fi
else
    # Show parent/current format as fallback
    parent_dir=$(basename "$(dirname "$dir_full")")
    current_dir_name=$(basename "$dir_full")
    dir_part=$(printf '\033[1;34m%s\033[0m/\033[36m%s\033[0m' "$parent_dir" "$current_dir_name")
fi

# Git information (with optional locks skip for performance)
git_info=""
cd "$dir_full" 2>/dev/null || cd "$(pwd)"
if git rev-parse --git-dir >/dev/null 2>&1; then
    # Get git version (short commit hash)
    git_version=$(git rev-parse --short HEAD 2>/dev/null || echo "no-commits")

    # Get branch name
    git_branch=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "detached")

    # Get status indicators (quick check, skip optional locks)
    git_status=""
    if ! git diff --quiet 2>/dev/null; then
        git_status="${git_status}*"  # Modified files
    fi
    if ! git diff --cached --quiet 2>/dev/null; then
        git_status="${git_status}+"  # Staged files
    fi
    # Quick untracked files check (may timeout on large repos)
    if timeout 0.5s git ls-files --others --exclude-standard >/dev/null 2>&1 && [ -n "$(git ls-files --others --exclude-standard 2>/dev/null | head -1)" ]; then
        git_status="${git_status}?"  # Untracked files
    fi

    # Format git info: branch@version with status
    if [ -n "$git_status" ]; then
        git_info=$(printf ' \033[33m%s\033[0m@\033[32m%s\033[0m\033[31m%s\033[0m' "$git_branch" "$git_version" "$git_status")
    else
        git_info=$(printf ' \033[33m%s\033[0m@\033[32m%s\033[0m' "$git_branch" "$git_version")
    fi
fi

# Claude Code session info (if available)
claude_info=""
if [ -n "$model_name" ] && [ "$model_name" != "null" ] && [ "$model_name" != "empty" ]; then
    # Short model name for display
    short_model=$(echo "$model_name" | sed 's/Claude //g; s/ Sonnet//g; s/3\.5/3.5/g; s/^[[:space:]]*//; s/[[:space:]]*$//')

    if [ -n "$short_model" ]; then
        claude_info=$(printf ' \033[90m[%s' "$short_model")

        if [ -n "$output_style" ] && [ "$output_style" != "null" ] && [ "$output_style" != "default" ] && [ "$output_style" != "empty" ]; then
            claude_info=$(printf '%s|%s' "$claude_info" "$output_style")
        fi

        claude_info=$(printf '%s]\033[0m' "$claude_info")
    fi
fi

# Output the complete enhanced status line
printf '%s:%s%s%s' "$user_host_part" "$dir_part" "$git_info" "$claude_info"