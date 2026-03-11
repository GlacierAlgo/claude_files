# Claude Code Configuration Repository

This repository serves as a **single source of truth** for Claude Code configuration, using symbolic links to maintain consistency across your system.

## Purpose

This repo maintains all Claude Code configuration files in version control and uses symbolic links to connect them to `~/.claude/`:

- **Global development philosophy** (`CLAUDE.md`) - Core coding principles and patterns
- **Hooks** (`hooks/`) - Pre/post command execution scripts
- **Skills** (`skills/`) - Custom Claude Code skills
- **Status line** (`statusline-enhanced.sh`) - Custom status bar display
- **User settings** (`settings.json`) - Claude Code preferences

## Setup

Run the setup script to create symbolic links from `~/.claude/` to this repository:

```bash
./setup-symlinks.sh
```

This will:
1. Backup existing files to `~/.claude/backups/`
2. Create symlinks for: `CLAUDE.md`, `settings.json`, `statusline-enhanced.sh`, `hooks/`, `skills/`
3. Make this repository the single source of truth for your configuration

## File Structure

### Symlinked to ~/.claude/ (Single Source of Truth)
```
├── CLAUDE.md                    # Master development guidelines
├── settings.json                # Claude Code preferences
├── statusline-enhanced.sh       # Custom status bar
├── hooks/                       # Command execution hooks
│   ├── block-git-push.sh       # Prevent accidental pushes
│   ├── block-npm.sh            # Enforce package manager
│   ├── block-pip.sh            # Enforce uv for Python
│   └── notify-command-end.py   # macOS notifications
└── skills/                      # Custom Claude Code skills
    ├── cal-sync/               # Calendar sync skill
    ├── commit_auto/            # Auto commit skill
    ├── cprofile-speedup.md     # Performance profiling skill
    └── drawio.md               # Draw.io diagram generation skill
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

## Development Guidelines

### Adding New Skills

1. Create skill file in `skills/` directory (either as `.md` file or subdirectory with `SKILL.md`)
2. Follow the skill format with frontmatter:
   ```markdown
   ---
   name: skill-name
   description: Brief description
   allowed-tools: Bash, Write, Read
   ---
   ```
3. Test the skill with `/skill-name` in Claude Code
4. Commit and push changes

### Updating Configuration

All configuration changes should be made in this repository:
- Edit files directly in the repo
- Changes are immediately reflected in `~/.claude/` via symlinks
- Commit changes to version control
- No need to manually sync files

### Hook Development

Hooks are shell scripts that run before/after Claude Code commands:
- Place hooks in `hooks/` directory
- Make them executable: `chmod +x hooks/your-hook.sh`
- Configure in `settings.json` under `hooks` section
- Test thoroughly before committing
