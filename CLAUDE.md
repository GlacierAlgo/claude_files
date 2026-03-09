# 🎯 CORE PHILOSOPHY

## Development Mindset
**"Practicality beats purity"** - Choose the most appropriate solution for each specific context.

### Trust-Based Programming
- **Trust Internal Systems** - Treat internal components as reliable collaborators, not external threats
- **Validate at Boundaries** - Input validation belongs at system edges, not everywhere
- **Fail Fast and Loud** - Let problems surface immediately where they can be fixed
- **Architectural Thinking** - Fix root causes instead of masking symptoms with defensive code

### The Complete Implementation Standard
**Core Rule**: Every piece of code must be production-ready. No placeholders, no "TODO" implementations, no mock returns. If you can't implement it completely right now, don't implement it at all.

---

# ⚡ DESIGN METHODOLOGY

## The SIMPLEX Principle
- **Simple First**: Choose simplest appropriate pattern
- **Incremental**: Add complexity only when proven necessary
- **Minimal**: Fewest parameters, simplest return types
- **Progressive**: Build working → improve → extend
- **Lazy Abstract**: Three-strikes rule (3+ uses = abstraction)
- **Elegant Fail**: Let exceptions propagate naturally to callers
- **Extend Only**: Open for extension, closed for modification

## YAGNI
Don't implement features until actually needed. Magic numbers stay. No speculative abstraction.

## DRY with Three-Strikes Rule
- First occurrence: Write inline
- Second occurrence: Copy and modify
- Third occurrence: Extract common functionality

## Function vs Class
- **Function**: stateless computation, simple utilities, pure logic
- **Class**: internal state, resource management (DB connections, file handles), lifecycle management

---

# 📝 IMPLEMENTATION STANDARDS

## No Fake Implementations
- No placeholder functions (`pass`, `return "TODO"`)
- No mock data returns
- No skeleton code waiting to be filled in
- When external dependency missing: `raise NotImplementedError(...)` not fake returns

## Naming Conventions
- Full clear names over abbreviations (`user_count` not `usr_cnt`)
- Accepted abbreviations: `id`, `url`, `api`, `db`, `df`, `ctx`, `ts`, `dt`, loop vars `i/j/k`
- No type prefixes (Hungarian notation)
- No `_clean`, `_new`, `_v2` suffixes in production code

## Exception Handling
- Let exceptions propagate — don't wrap unless you can meaningfully handle them
- Don't handle imaginary edge cases
- Don't repeat validation across internal layers
- Focus on actual business logic failures

## Logging
- Logs should answer operational questions, not satisfy development curiosity
- Log: system state, business metrics, errors requiring action
- Don't log: "entering function X", variable dumps, pure debug noise

---

# 🛠️ PRACTICAL WORKFLOW

## General Rules
- **No Unsolicited Documentation**: Do NOT create summary documents, README files, or markdown files unless explicitly asked
- **No Extra Files**: Keep solutions focused on the actual requirement
- **Execute Directly**: When given a concise instruction, execute it. Don't ask clarifying questions unless genuinely ambiguous
- **No Unnecessary Additions**: No method aliases, backward-compatibility wrappers, or extra parameters not asked for

## Project-Specific Conventions (Quant/Factor System)
- **Partition Format**: `month={YYYY-MM}/data.parquet` (data.parquet is the leaf file, no subdirectory wrapper)
- **Index vs Factor**: `market_dates` is an INDEX, not a factor
- **Data Types**: Factor data types are Float64 unless otherwise specified
- **Method Names**: Use `compute_and_save()` not `generate()` for factor computation

## Development Guidelines
- **UV Package Management**: Always use UV for Python package management
- **No Docker**: Explicitly avoid Docker for this project
- **No pytest / mock-based tests**: Never write pytest or unittest style tests. Tests that mock dependencies and verify return values test implementation details, not behavior — they break on refactors and provide false confidence.
- **Scenario-based regression scripts instead**: When verification is needed, write scripts in `scripts/verify_*.py`. A valid scenario states *why* a behavior should hold (the business invariant), uses real or minimal synthetic data without mocks, survives internal refactors, and fails only when a business contract is broken. Each scenario has an explicit `hypothesis` string answering "why should this behavior hold", not "what output do I expect".
- **No .env Comments**: Never use inline comments in .env files
- **Avoid node_modules**: Never look into node_modules
- **Code Quality**: Use Ruff for linting and formatting, never Pylint

## CLI Standards
- Use `click` instead of `argparse` for CLI applications
- Use `python-dotenv` for environment management (`.env.local` overrides `.env`)

## Architecture by Complexity
- **< 5 modules**: flat structure (cli.py, core.py, storage.py, utils.py)
- **5–15 modules**: functional grouping (core/, storage/, utils/)
- **> 15 modules**: layered architecture with clear single-direction dependencies
- Don't add layers speculatively — wait for actual complexity signals

---

# 🔧 GIT OPERATIONS

- Always verify directory with `pwd` before git commands
- Never push without explicit user instruction (push manually after reviewing)

---

# 🌐 FRAMEWORK-SPECIFIC GUIDELINES

## FastAPI
- Use `APIRouter` per domain, extract business logic from endpoints
- Set up health endpoint before building features
- External API: full validation, rate limiting, auth (SlowAPI)
- Internal operations: trust parameters, let frameworks handle errors

---

# Final Rules
- My Obsidian vault is at /Users/yanghh/obs. Save summaries, notes, knowledge pages there.
- NEVER GIT COMMIT WITH CLAUDE CODE COAUTHORSHIP
- Let errors fail naturally. Never use try-except before the user asks.
- SiliconFlow docs: https://docs.siliconflow.cn/llms.txt
