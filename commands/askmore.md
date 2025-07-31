# /askmore Command Specification

## Purpose
The `/askmore` command enables Claude Code to proactively ask clarifying questions when user requests are unclear, ambiguous, or lack sufficient detail for optimal implementation.

## Command Syntax
```
/askmore
```

## Behavior Enhancement
When the `/askmore` command is used, Claude Code should:

1. **Identify Ambiguity**: Recognize when requests contain:
   - Vague requirements ("make it better", "optimize this")
   - Missing technical specifications
   - Unclear scope or boundaries
   - Multiple possible interpretations
   - Insufficient context

2. **Ask Strategic Questions**: Pose specific, actionable questions such as:
   - "What specific performance metrics should I optimize for?"
   - "Which user roles should have access to this feature?"
   - "What's your preferred error handling approach?"
   - "Should I follow any specific coding standards or frameworks?"
   - "What's the expected input/output format?"

3. **Suggest Alternatives**: When multiple approaches exist:
   - Present 2-3 viable options with pros/cons
   - Ask for preference or additional constraints
   - Clarify trade-offs (performance vs. simplicity, etc.)

## Implementation Guidelines

### Enhanced System Prompt Addition
```
# Clarification Protocol (/askmore)

When the user activates /askmore or when encountering ambiguous requests:

1. **Stop and Clarify**: Don't proceed with assumptions. Ask specific questions.

2. **Question Categories**:
   - **Scope**: "Should I also handle edge case X?"
   - **Technical**: "Which framework/library should I use?"
   - **Design**: "What's the preferred architecture pattern?"
   - **Requirements**: "How should this behave when Y occurs?"
   - **Constraints**: "Are there performance/security requirements?"

3. **Question Format**:
   - Be specific, not generic
   - Offer concrete options when possible
   - Explain why the clarification matters
   - Limit to 3-5 most important questions

4. **Activation Triggers**:
   - User explicitly types `/askmore`
   - Request contains vague terms ("improve", "fix", "optimize")
   - Multiple implementation paths exist
   - Requirements seem incomplete

Example Response:
"I need to clarify a few things to implement this optimally:

1. **Performance target**: Are you optimizing for speed, memory usage, or both?
2. **Scope**: Should I also update the related authentication logic?
3. **Framework**: Do you prefer using React Query or native fetch for data handling?

Which approach aligns better with your goals?"
```

### Integration Points
- Activate automatically on ambiguous requests
- Manual activation via `/askmore` command
- Integrate with existing error handling and user feedback systems
- Maintain conversation context for follow-up questions

## Expected Outcomes
- Reduced implementation iterations
- More accurate solutions matching user intent
- Better requirement gathering
- Improved user satisfaction through precision

## Ultrathinking
Whenever user types /askmore, Claude Code should activate ultrathink mode to enhance thinking process.
