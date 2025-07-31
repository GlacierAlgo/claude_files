# 🎯 CORE PHILOSOPHY

## Development Mindset
**"Practicality beats purity"** - Choose the most appropriate solution for each specific context, balancing simplicity with functionality.

### Trust-Based Programming
- **Trust Internal Systems** - Treat internal components as reliable collaborators, not external threats
- **Validate at Boundaries** - Input validation belongs at system edges, not everywhere
- **Fail Fast and Loud** - Let problems surface immediately where they can be fixed
- **Architectural Thinking** - Fix root causes instead of masking symptoms with defensive code
- **Complete System Design** - Trust internal APIs but verify system design completeness; missing functionality is not a trust issue but a design gap

### The Complete Implementation Standard
**Core Rule**: Every piece of code must be production-ready. No placeholders, no "TODO" implementations, no mock returns.

**Bottom Line**: If you can't implement it completely right now, don't implement it at all. Wait until you can do it properly.

---

# ⚡ DESIGN METHODOLOGY

## The SIMPLEX Principle
**Start Imperfect, Make Perfect, Extend X-wise**

### Core Rules (SIMPLEX)
- **S**imple First: Choose simplest appropriate pattern (function or class based on needs)
- **I**ncremental: Add complexity only when proven necessary
- **M**inimal: Fewest parameters, simplest return types
- **P**rogressive: Build working → improve → extend
- **L**azy Abstract: Three-strikes rule (3+ uses = abstraction)
- **E**legant Fail: Let exceptions propagate naturally to callers
- **X**tend Only: Open for extension, closed for modification

### The Three-Strikes Abstraction Rule
1. **First strike**: Write it directly
2. **Second strike**: Copy-paste with changes
3. **Third strike**: Now create abstraction

### Refactoring Philosophy
**Core Principle**: Refactor to eliminate duplication, not to achieve "better architecture"

**Good Refactoring Motivations**:
- Multiple files contain identical code blocks
- Same data transformation logic repeated across modules
- Identical error handling patterns duplicated

**Bad Refactoring Motivations**:
- "This function is too long" (if it has single responsibility)
- "Let's make this more modular" (without specific duplication to eliminate)
- "This should follow clean architecture" (without business justification)

```python
# ✅ Refactor when you see actual duplication
# tools.py and streaming.py both have:
{
    'id': result.id,
    'text': result.text,
    'embedding': result.embedding,
    # ... exact same transformation
}

# ❌ Don't refactor unique functionality
async def fill_gaps(start_id, end_id):
    # This function has a unique, specific purpose
    # Even if it's long, don't split it unless there's actual reuse
```

## Architecture Decision Framework

### Design Decision Matrix
```
Scenario              | State? | Resources? | Config? | Choice
---------------------|--------|------------|---------|--------
Data Processing      | No     | No         | Simple  | Function
API Client           | Yes    | Yes        | Complex | Class
Database Connection  | Yes    | Yes        | Complex | Class
Format Conversion    | No     | No         | Simple  | Function
Configuration Mgmt   | Yes    | No         | Complex | Class
Error Handling       | No     | No         | Simple  | Function
Session Management   | Yes    | Yes        | Complex | Class
Utility Operations   | No     | No         | Simple  | Function
```

### Decision Criteria
1. **State Management**: Does it need to remember information between calls?
2. **Resource Management**: Does it manage connections, files, or system resources?
3. **Complex Configuration**: Does it have multiple related settings?
4. **Lifecycle Management**: Does it need setup/teardown operations?

### Quality Standards
- **Classes**: When maintaining state, managing resources, or handling complex configuration
- **Functions**: When performing pure computation, simple transformation, or utility operations
- **Hybrid**: Classes provide state management, functions handle specific logic internally

**Validation Criteria**:
- Is the code easy to test?
- Does naming directly express intent?
- Does it follow single responsibility principle?
- Is it easy to understand and maintain?

---

# 📝 IMPLEMENTATION STANDARDS

## No Fake Implementations

### What Counts as Fake Implementation
- **Placeholder Functions**: `def process_data(): return "TODO"` or `pass`
- **Mock Data Returns**: Returning hardcoded values instead of real computation
- **Incomplete Logic**: Functions that handle only the "happy path" 
- **Dummy Responses**: `return {"success": True}` without actual work
- **Skeleton Code**: Empty classes or methods waiting to be "filled in later"

### The Complete Implementation Standard
```python
# ❌ FAKE - Placeholder implementation
def calculate_tax(amount: float) -> float:
    # TODO: Implement tax calculation
    return 0.0

# ✅ REAL - Complete functional implementation
def calculate_tax(amount: float, tax_rate: float = 0.08) -> float:
    return amount * tax_rate
```

### Exception Policy
**The Only Acceptable "Incomplete" Code**: When a function needs external dependencies that don't exist yet, it should **fail explicitly** rather than return fake data:

```python  
# ✅ ACCEPTABLE - Explicit failure until real implementation
def get_payment_status(transaction_id: str) -> str:
    raise NotImplementedError("Payment gateway integration pending")

# ❌ NEVER - Fake success response
def get_payment_status(transaction_id: str) -> str:
    return "success"  # Lies about actual payment status
```

## Naming Conventions

### Core Standards
- **Full Names**: Never abbreviate variable or function names
- **No Type in Names**: Don't include type information in variable names
- **Units in Variables**: Add units to variables unless type already indicates them
- **No Type in Type Definitions**: Don't redundantly include type info in type definitions

### Direct Naming Principle
- Never add qualifiers like `_clean`, `_new`, `_v2` to production code names
- Quality is the default expectation, not an exception
- Replace old code entirely rather than creating parallel versions
- Let version control handle history, not naming conventions
- **Rule**: If it's not good enough to be the main version, it shouldn't exist

### Design Patterns
- **Composition over Inheritance**: Prefer composition design patterns
- **Dependency Injection**: Use dependency injection effectively
- **Flat Over Nested**: Avoid deep inheritance, prefer composition and dependency injection
- **Clear Naming**: Remove qualifiers, directly express core functionality

## Exception Handling Philosophy

### Core Principles
- **Trust Your Collaborators** - Internal APIs already handle edge cases properly
- **Let Exceptions Propagate** - Don't wrap exceptions unless you can meaningfully handle them
- **Fail Fast** - Problems should surface immediately, not be hidden

### Boundary Management
- **External Boundaries** - Validate all user inputs, API requests, external data
- **Internal Trust** - Functions should trust their parameters from internal callers
- **Clear Separation** - Don't treat internal calls like untrusted external APIs
- **Single Validation Point** - Each input should be validated once at the boundary

### Exception Best Practices
```python
# ✅ Trust collaboration + elegant failure
def get_max_id(self) -> int:
    collection = self.connection.get_collection(self.collection_name)
    results = collection.query(expr="id >= 0", output_fields=["id"], 
                              limit=100, order_by="id desc")
    return max(int(item["id"]) for item in results)

# ❌ Over-defensive + exception masking
def get_max_id(self) -> int:
    try:
        if not self.connection.connected: return 0  # Duplicate checking
        if not collection.exists(): return 0        # Duplicate checking
        # ... wrap exceptions, return default values
    except Exception: return 0  # Masks real problems
```

### Anti-Patterns to Avoid
- **Imaginary Edge Cases** - Don't handle hypothetical problems that never occur
- **Defensive Duplication** - Don't repeat validation across internal layers
- **Error Masking** - Don't hide real problems with generic error handling
- **Responsibility Diffusion** - Don't make every function handle every possible error

### Practical Guidelines
- **YAGNI for Error Handling** - You aren't gonna need most defensive checks
- **Trust Your Dependencies** - Well-designed libraries handle their own edge cases
- **Types Over Runtime Checks** - Use type hints to catch issues at development time
- **Real Problems Only** - Focus on actual business logic failures, not technical paranoia

**Core Insight**: Most "edge cases" developers worry about are either already handled by underlying systems or indicate serious design flaws that need architectural fixes, not defensive programming.

## Logging Philosophy

### Business Value-Oriented Logging
**Principle**: Logs should answer operational questions, not satisfy development curiosity

**Good Logging**:
- Current system state and progress
- Business metrics and completion rates  
- Error conditions that require action
- Performance bottlenecks affecting users

**Avoid Logging**:
- Pure debug information ("entering function X")
- Variable dumps without context
- Technical details that don't help operations

```python
# ✅ Operational value
logger.info(f"✅ 第 1 页: 100 条数据 (ID: 4312819-4312799)")
logger.info(f"📊 Total processed: 500, Pending: 200")
logger.warning(f"⚠️ 覆盖率 (66.7%) - 部分ID可能在API中不存在")

# ❌ Development noise  
logger.debug("Starting batch processing")
logger.debug(f"Variable batch_size = {batch_size}")
```

### Configuration Management Strategy
**Principle**: Distinguish between operational parameters and implementation details

**Configuration Hierarchy**:
1. **Frequently Adjusted** → Environment variables (BATCH_SIZE, MAX_CONCURRENT)
2. **Occasionally Tuned** → Function parameters (max_pages, timeout)
3. **Rarely Changed** → Code constants (API endpoints, field mappings)

```python
# ✅ Right level of configuration
STREAMING_BATCH_SIZE=100     # Operators adjust this
max_pages: int = 50          # Sometimes tuned for special cases
page_size = 100             # Implementation detail, rarely changes

# ❌ Over-configuration
DEBUG_LOG_ENABLED=true      # Internal systems don't need this granularity
MAX_RETRY_ATTEMPTS=3        # This kind of constant rarely needs adjustment
```

---

# 🛠️ PRACTICAL WORKFLOW

## Command Dispatcher Pattern (tools.py approach)
**Pattern**: Single entry point for multiple related operations

**When to Use**:
- System has multiple operational modes (sync, stream, setup, etc.)
- Need consistent parameter handling and error reporting
- Operations share infrastructure (logging, config, connections)
- Operators prefer fewer entry points to remember

```python
# ✅ Unified command interface
python tools.py sync
python tools.py stream
python tools.py fill-gaps --start-id 1000 --end-id 2000
python tools.py detect-gaps

# vs ❌ Scattered scripts
python sync_data.py
python streaming_service.py  
python gap_processor.py --start 1000 --end 2000
```

**Design Principles**:
- **Single Responsibility per Command**: Each command does one complete operation
- **Shared Infrastructure**: Common argument parsing, logging setup, error handling
- **Business Logic Separation**: tools.py dispatches, real logic lives in domain modules
- **Fail-Fast Validation**: Validate parameters before calling business functions

**Implementation Pattern**:
```python
async def main():
    parser = argparse.ArgumentParser()
    # ... unified argument setup
    
    if args.command == "sync":
        success = await sync_incremental()  # Business logic in separate module
    elif args.command == "stream":
        await start_streaming_processing()
    # Command dispatch, not implementation
```

## Development Guidelines
- **UV Package Management**: Always use UV for Python package management
- **No Docker**: Explicitly avoid Docker for this project
- **No Python Tests**: Never write tests for Python code
- **No .env Comments**: Never use inline comments in .env files
- **Avoid node_modules**: Never look into node_modules

## Documentation Links
- **SiliconCloud/SiliconFlow LLMs Documentation**:
  - Navigation: https://docs.siliconflow.cn/llms.txt
  - Fast Grep: https://docs.siliconflow.cn/llms-full.txt

---

# 🎯 DEVELOPMENT INTERACTION PRINCIPLES

## Purpose: Prevent Over-Engineering Through Clear Communication

### The Problem
AI assistants often make assumptions about user needs, leading to over-engineered solutions with unnecessary complexity, unused features, and bloated codebases.

### The Solution: Ask-First Development

## Core Interaction Rules

### 1. Clarification Before Implementation (Ask Before Assume)
**Purpose**: Eliminate assumptions that lead to over-engineering

**When to Ask**:
- User request contains ambiguous terms ("process", "support", "optimize", "handle")
- Multiple implementation approaches exist
- Technical choices affect system complexity
- External integrations or APIs involved

**How to Ask**:
```
"I understand you need [core requirement]. To implement the right solution:
1. [Specific technical question]
2. [Scope/boundary question]
3. [Format/interface question]
Which approach fits your actual needs?"
```

**Example**:
- User: "Download news from Sina"
- Ask: "Which Sina API? What data format? JSON or XML? Which fields do you need?"
- Don't assume: RSS support + scheduling + multiple sources + enterprise features

### 2. Minimal Viable Implementation (Start Simple)
**Purpose**: Deliver value quickly without unnecessary complexity

**Implementation Strategy**:
- Solve the core problem first, ignore edge cases
- One file per distinct problem
- Single responsibility per module
- Defer optimization and features until requested

**Complexity Budgets**:
- Single file: aim for <100 lines unless complexity is essential
- New modules: maximum 2 files unless user explicitly needs more
- Dependencies: only add what's immediately necessary

**Layered Approach**:
```
Layer 1: Core functionality (must have)
Layer 2: Convenience features (ask user)
Layer 3: Advanced capabilities (user must explicitly request)
```

### 3. Incremental Validation (Validate Early, Validate Often)
**Purpose**: Ensure development stays aligned with actual needs

**Validation Points**:
- After requirement clarification: "Is my understanding correct?"
- After core implementation: "Does this solve your problem?"
- Before adding features: "Do you need [specific enhancement]?"
- When complexity increases: "This requires [cost]. Still needed?"

**Feedback Loop**:
```
Requirement → Clarify → Minimal Implementation → User Validation → 
Enhancement Decision → Implementation → Validation → Continue
```

### 4. Complexity Transparency (Honest Cost Communication)
**Purpose**: Help users make informed decisions about feature complexity

**Alert Triggers**:
- File count > 2 for single feature
- Line count > 150 for single module
- New significant dependencies
- Additional configuration requirements

**Communication Template**:
```
"Implementing [feature] requires:
- [X] additional files
- [Y] new dependencies  
- [Z] configuration steps
- [Time] development effort

Simple version handles [core use case]. 
Full version adds [advanced capabilities].
Which do you prefer?"
```

### 5. Scope Boundary Management (Clear Limits)
**Purpose**: Prevent feature creep and maintain module coherence

**Boundary Principles**:
- One module = one problem domain
- Cross-cutting concerns need explicit user approval
- Feature overlap requires consolidation decision
- Integration complexity needs justification

**Decision Framework**:
- New feature in existing module: preferred approach
- New module creation: requires clear separation of concerns  
- Cross-module functionality: needs explicit user requirement

### 6. Technical Debt Transparency (Honest Trade-offs)
**Purpose**: Set proper expectations about implementation choices

**What to Communicate**:
- Current implementation limitations
- Future extension costs
- Alternative approaches available
- Performance/scalability implications

**Example Communication**:
```
"This implementation handles your current needs but has limitations:
- [Specific constraint 1]
- [Specific constraint 2]
- [Scaling consideration]

For full requirements, would need [specific changes].
Is the current approach sufficient?"
```

## Daily Development Checklist

**Before Implementation**:
- [ ] Are user requirements 100% clear?
- [ ] Am I making assumptions about unstated needs?
- [ ] What's the simplest solution that works?
- [ ] Does complexity match actual requirements?

**During Implementation**:
- [ ] Am I solving problems the user didn't mention?
- [ ] Is code complexity justified by real requirements?
- [ ] Can this be simplified without losing functionality?

**After Implementation**:
- [ ] Have I confirmed the solution meets user needs?
- [ ] Are there obvious next steps the user might want?
- [ ] Should I ask about additional requirements?

## Success Metrics

**Good Development Session**:
- User gets exactly what they need
- No unused features or complexity
- Clear path for future enhancements
- Minimal surprise or confusion

**Failed Development Session**:
- User overwhelmed by unexpected complexity
- Features implemented that user doesn't need
- Solution requires explanation to understand
- User has to remove or simplify delivered code

---

# 🌐 FRAMEWORK-SPECIFIC GUIDELINES

## FastAPI Production Standards
**Apply only when building FastAPI applications**

### 1. Router Organization
- **Mandatory**: Use `APIRouter` for multiple endpoint groups
- **Structure**: One router per domain (items, users, auth, etc.)
- **Prefixes**: Clear, RESTful prefixes (`/items`, `/users`)

```python
# ✅ Organized routing
from fastapi import APIRouter

router = APIRouter(prefix="/items")

@router.get("/{item_id}")
def get_item(item_id: int):
    return get_database_item(item_id)
```

### 2. Operation Separation
- **Rule**: Extract business logic from endpoint functions
- **Pattern**: Endpoints only handle routing, operations handle business logic
- **Benefits**: Better testing, code reuse, cleaner separation of concerns

```python
# ✅ Separated concerns
@router.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_database)):
    return create_database_item(item, db)  # Operation in separate module

# ❌ Mixed concerns
@router.post("/items") 
def create_item(item: ItemCreate):
    # Database logic, validation, business rules all mixed here...
```

### 3. Deployment-First Development
- **Priority**: Set up deployment pipeline before building features
- **Start**: Health check endpoint + Docker + CI/CD
- **Reason**: Deployment issues are the hardest to debug and most time-consuming

**Deployment Checklist**:
- [ ] Basic health endpoint (`/health`)
- [ ] Dockerfile with proper dependencies
- [ ] Cloud deployment configuration
- [ ] CI/CD pipeline setup
- [ ] Then build actual features

### 4. Access Control Implementation
**Both authentication and rate limiting are required**

#### Rate Limiting (SlowAPI)
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

@router.get("/items/{item_id}")
@limiter.limit("10/second")
def get_item(request: Request, item_id: int):
    return get_database_item(item_id)
```

#### Dependency Injection Pattern
```python
def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use in endpoints
def create_item(item: ItemCreate, db: Session = Depends(get_database)):
    return create_database_item(item, db)
```

### FastAPI Boundary Rules
- **External API boundaries**: Full validation, rate limiting, authentication
- **Internal operations**: Trust parameters, let SQLAlchemy handle database errors
- **Database sessions**: Always use dependency injection
- **Return types**: Pydantic models for API responses, not raw database objects

---

**Core Philosophy**: Build what users actually need, not what we think they might want. When in doubt, ask. When simple works, stop. When complexity grows, justify it.

**Guiding Principle**: Let code structure serve clear expression of business logic, not dogmatic pursuit of paradigm "purity". Trust your collaborators, let errors propagate elegantly, and focus on solving real problems rather than imaginary edge cases.

## Unified Development Principles

**Quality Code = Solving Real Problems + Right Abstraction Level + Easy Maintenance**

### The Professional Context Assumption
- **Trust Professional Operations**: Internal systems managed by competent teams don't need excessive defensive programming
- **Focus on Business Logic**: Spend complexity budget on domain problems, not imaginary edge cases  
- **Operational Efficiency**: Tools should be easy to use and understand, architecture should be easy to modify

### Function Responsibility Clarity
**Principle**: Judge functions by their business purpose, not their length or internal complexity

```python
# ✅ Complex but focused - serves one business purpose
async def fill_gaps(start_id: int, end_id: int):
    # 50+ lines of API pagination, filtering, boundary detection
    # But it does ONE thing: get news data for specific ID range
    
# ❌ Simple but unfocused - serves multiple purposes  
def process_and_store(data):
    # 10 lines that do embedding AND storage AND logging
    # Multiple responsibilities in a short function
```

### The Maintenance-First Mindset
- **Reduce Repetition**: Same code in multiple places creates maintenance debt
- **Preserve Unique Logic**: Don't break up code that serves a single, specific purpose
- **Tool Usability**: Command-line interfaces should be discoverable and consistent
- **Configuration Pragmatism**: Make frequently-adjusted parameters configurable, leave stable implementation details as constants

### Development Success Metrics
1. **Solves the stated problem completely**
2. **Easy for operators to use and troubleshoot**  
3. **Changes to business requirements require minimal code changes**
4. **New team members can understand and modify the system quickly**