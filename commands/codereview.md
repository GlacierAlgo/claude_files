# /codereview Command Specification

## Purpose
The `/codereview` command enables Claude Code to perform comprehensive code reviews aligned with the development philosophy in `CLAUDE.md`, focusing on practical improvements rather than theoretical perfection.

## Command Syntax
```
/codereview [file_path|directory_path]
```

## Review Framework

### Core Review Principles
Based on CLAUDE.md philosophy:

1. **Trust-Based Programming Assessment**
   - Evaluate boundary validation vs internal trust patterns
   - Identify over-defensive programming that masks real issues
   - Check for appropriate exception propagation

2. **Complete Implementation Standard**
   - Flag placeholder implementations, TODOs, mock returns
   - Verify all functions provide real functionality
   - Ensure no fake success responses

3. **SIMPLEX Principle Evaluation**
   - Assess if complexity matches actual requirements
   - Check for premature abstraction (violation of three-strikes rule)
   - Evaluate function vs class design decisions

## Review Categories

### 1. Architecture & Design
- **Function vs Class Usage**: Verify appropriate choice based on state/resources/config complexity
- **Abstraction Level**: Check if abstractions solve actual duplication vs theoretical "clean architecture"
- **Trust Boundaries**: Ensure validation happens at system edges, not internally

### 2. Implementation Quality
- **Complete Functionality**: No placeholders, TODOs, or mock implementations
- **Exception Handling**: Appropriate propagation vs masking
- **Business Logic Focus**: Code serves real requirements, not imaginary edge cases

### 3. Maintainability
- **Duplication**: Identify actual repeated code blocks requiring abstraction
- **Naming**: Full names, no abbreviations, units included where relevant
- **Responsibility Clarity**: Functions serve single business purpose

### 4. Anti-Pattern Detection
- **Over-Engineering**: Unnecessary complexity without business justification
- **Defensive Duplication**: Redundant validation across internal layers
- **Imaginary Edge Cases**: Handling problems that don't actually occur
- **Fake Implementations**: Placeholder code masquerading as real functionality

## Review Output Format

```markdown
## Code Review Summary

### ✅ Strengths
- [Specific positive observations aligned with CLAUDE.md principles]

### ⚠️ Concerns
- [Issues categorized by severity and philosophy alignment]

### 🔧 Recommendations
- [Specific, actionable improvements with business justification]

### 📊 Philosophy Alignment Score
- Trust-Based Programming: [Score/5]
- Complete Implementation: [Score/5] 
- SIMPLEX Adherence: [Score/5]
- Practical Focus: [Score/5]

### 🎯 Priority Actions
1. [Highest impact improvement]
2. [Second priority improvement]
3. [Third priority improvement]
```

## Implementation Guidelines

### Automated Checks
1. **Scan for Anti-Patterns**:
   - `TODO`, `FIXME`, `HACK` comments
   - Functions returning hardcoded success values
   - Excessive try-catch blocks masking exceptions
   - Generic error handling that hides real issues

2. **Architecture Analysis**:
   - Function length vs responsibility focus
   - Class usage appropriateness (state/resources/config criteria)
   - Duplication patterns across files

3. **Naming Convention Validation**:
   - Check for abbreviations in variable/function names
   - Verify units in measurement variables
   - Flag qualifiers like `_clean`, `_new`, `_v2`

### Context-Aware Review
- **Project Type**: Adjust standards for tools vs libraries vs applications
- **Team Size**: Consider maintenance burden relative to team capacity
- **Business Context**: Prioritize improvements with clear operational value

### Review Depth Levels
- **Quick Scan**: Anti-patterns and major philosophy violations
- **Standard Review**: Full framework application
- **Deep Analysis**: Include performance, security, and scaling considerations

## Integration Points
- Trigger automatically on pull request creation
- Manual activation via `/codereview` command
- Integrate with existing git workflow
- Support both single file and directory review

## Expected Outcomes
- Code that follows CLAUDE.md philosophy consistently
- Reduced over-engineering and defensive programming
- Focus on solving real business problems
- Improved maintainability through practical patterns

## Example Usage
```bash
/codereview src/api/handlers.py
/codereview src/utils/
/codereview  # Review current git diff
```