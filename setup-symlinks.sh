#!/bin/bash
# Setup symbolic links from ~/.claude/ to claude_files repository
# This makes claude_files the single source of truth

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Setting up symbolic links..."
echo "Repository: $REPO_DIR"
echo "Claude config: $CLAUDE_DIR"
echo ""

# Files and directories to symlink
ITEMS=(
    "CLAUDE.md"
    "settings.json"
    "statusline-enhanced.sh"
    "hooks"
    "skills"
)

# Create backup directory with timestamp
BACKUP_DIR="$CLAUDE_DIR/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

for item in "${ITEMS[@]}"; do
    SOURCE="$REPO_DIR/$item"
    TARGET="$CLAUDE_DIR/$item"

    if [ ! -e "$SOURCE" ]; then
        echo "⚠️  Warning: $item not found in repository, skipping"
        continue
    fi

    # Backup existing file/directory if it exists and is not already a symlink
    if [ -e "$TARGET" ] && [ ! -L "$TARGET" ]; then
        echo "📦 Backing up existing $item"
        mv "$TARGET" "$BACKUP_DIR/"
    fi

    # Remove existing symlink if it exists
    if [ -L "$TARGET" ]; then
        echo "🔗 Removing old symlink: $item"
        rm "$TARGET"
    fi

    # Create new symlink
    echo "✅ Creating symlink: $item"
    ln -s "$SOURCE" "$TARGET"
done

echo ""
echo "✨ Setup complete!"
echo "Backup saved to: $BACKUP_DIR"
echo ""
echo "Symlinks created:"
ls -la "$CLAUDE_DIR" | grep " -> " | grep -E "$(IFS='|'; echo "${ITEMS[*]}")"
