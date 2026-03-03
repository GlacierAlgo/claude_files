# Claude Code Configuration Repository

This repository serves as a **single source of truth** for Claude Code configuration, using symbolic links to maintain consistency across your system.

## Purpose

This repo maintains all Claude Code configuration files in version control and uses symbolic links to connect them to `~/.claude/`:

- **Global development philosophy** (`CLAUDE.md`) - Core coding principles and patterns
- **Hooks** (`hooks/`) - Pre/post command execution scripts
- **Status line** (`statusline-enhanced.sh`) - Custom status bar display
- **User settings** (`settings.json`) - Claude Code preferences

## Setup

Run the setup script to create symbolic links from `~/.claude/` to this repository:

```bash
./setup-symlinks.sh
```

This will:
1. Backup existing files to `~/.claude/backups/`
2. Create symlinks for: `CLAUDE.md`, `settings.json`, `statusline-enhanced.sh`, `hooks/`
3. Make this repository the single source of truth for your configuration

## File Structure

### Symlinked to ~/.claude/ (Single Source of Truth)
```
├── CLAUDE.md                    # Master development guidelines
├── settings.json                # Claude Code preferences
├── statusline-enhanced.sh       # Custom status bar
└── hooks/                       # Command execution hooks
    ├── block-git-push.sh       # Prevent accidental pushes
    ├── block-npm.sh            # Enforce package manager
    ├── block-pip.sh            # Enforce uv for Python
    └── notify-command-end.py   # macOS notifications
```

### Version Controlled
```
├── setup-symlinks.sh           # Symlink setup script
├── package.json                # Node dependencies for hooks
└── README.md                   # This documentation
```

## Benefits

- **Single Source of Truth**: All changes in this repo automatically apply to Claude Code
- **Version Control**: Track configuration changes over time
- **Easy Backup**: Clone this repo to restore your setup
- **Portable**: Run `setup-symlinks.sh` on any machine to replicate your environment
