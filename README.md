# Claude Code Configuration Repository

This repository serves as a **dotfiles-style configuration hub** for Claude Code, containing personalized settings, commands, and session data that enhance AI-assisted development workflows.

## Purpose

Similar to how dotfiles repositories store terminal configurations, shell aliases, and development environment setups, this repo maintains:

- **Global development philosophy** (`CLAUDE.md`) - Core coding principles and patterns
- **Custom commands** (`commands/`) - Specialized workflow enhancements 
- **Project session history** (`projects/`) - Context and conversation logs per project
- **Task management data** (`todos/`) - Session-specific todo tracking
- **User settings** (`settings.json`) - Claude Code preferences

## File Structure

### Version Controlled (Shared)
```
├── CLAUDE.md              # Master development guidelines & philosophy
├── README.md              # This documentation
├── .gitignore             # Repository file management
└── commands/              # Custom command definitions
    ├── askmore.md         # Enhanced clarification protocol
    └── drawio.md          # Diagram generation workflows
```

### Local Only (Private)
```
├── projects/              # Per-project session logs (JSONL format)
├── todos/                 # Task management state files
├── settings.json          # Claude Code user preferences
├── statsig/              # Analytics & feature flags
└── commands/
    └── micropomodoro.md   # Local command experiments
```

## Dotfiles Similarity

Like traditional dotfiles, this repo:
- **Personalizes** the development environment for your workflow
- **Persists** preferences across sessions and projects
- **Centralizes** configuration in version control
- **Enables** rapid environment setup on new machines
- **Maintains** development context and history

## Key Features

- **Philosophy-Driven Development**: `CLAUDE.md` encodes development principles that guide all AI interactions
- **Session Persistence**: Project conversations and context survive across sessions
- **Custom Commands**: Specialized workflows for enhanced productivity
- **Structured Logging**: JSONL format for easy parsing and analysis

## Note on Repository State

This repo intentionally maintains more files locally than in git to preserve sensitive session data while keeping core configurations shareable.
