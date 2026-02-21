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

## Extreme Programming (XP) Principles

### YAGNI (You Aren't Gonna Need It)
**Core Principle**: Don't implement features until they are actually needed

**Application**:
- **Magic Numbers Stay**: If a value hasn't changed, don't make it configurable
- **Parameters at Optimum**: If page_size=100 is the tested maximum, keep it hardcoded
- **No Speculative Abstraction**: Wait for real requirements, not imagined ones

```python
# ❌ Over-engineering for imaginary flexibility
class ConfigurableRetryHandler:
    def __init__(self, max_retries=3, backoff_factor=2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

# ✅ YAGNI - Direct implementation
async def fetch_with_retry(url):
    for attempt in range(3):  # This number has never needed to change
        try:
            return await fetch(url)
        except Exception:
            if attempt == 2: raise
            await asyncio.sleep(2 ** attempt)
```

### DRY with Three-Strikes Rule
**Principle**: Don't Repeat Yourself - but only after actual repetition occurs

**Implementation**:
- First occurrence: Write inline
- Second occurrence: Copy and modify
- Third occurrence: Extract common functionality

### Simple Design (XP's Four Rules)
1. **Passes all tests** - Works correctly for current requirements
2. **Reveals intention** - Code clearly expresses its purpose
3. **No duplication** - But only remove actual, not potential duplication
4. **Fewest elements** - Minimal classes, methods, and abstractions

### Continuous Refactoring
**Principle**: Refactor when you have evidence, not speculation

**Good Refactoring Triggers**:
- Actual code duplication (not similarity)
- Difficulty making required changes
- Confusion from team members

**Bad Refactoring Triggers**:
- "This might be useful later"
- "This could be more elegant"
- "What if we need to..."

### Embrace Change Through Simplicity
**Philosophy**: Simple code is easier to change than "flexible" code

```python
# ❌ Flexible but complex
class AbstractNewsProcessor(ABC):
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> ProcessedData:
        pass

class SinaNewsProcessor(AbstractNewsProcessor):
    def __init__(self, config: ProcessorConfig):
        self.config = config
    
    def process(self, data: Dict[str, Any]) -> ProcessedData:
        # Complex processing with many configuration options

# ✅ Simple and direct
def process_sina_news(articles):
    return [
        {
            "id": article["id"],
            "text": article["rich_text"],
            "time": article["create_time"]
        }
        for article in articles
        if article.get("id") and article.get("rich_text")
    ]
```

### XP's Feedback Loops
1. **Immediate Feedback**: Let errors fail fast and loud
2. **Frequent Releases**: Deploy working code, not perfect code
3. **Real User Feedback**: Build what users ask for, not what you think they need

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

### Function vs Class 决策指南

**优先考虑Function的场景**:
- 无状态计算和数据转换
- 简单的工具操作
- 纯函数式逻辑

**考虑使用Class的场景**:
- 需要管理内部状态
- 需要管理资源（数据库连接、文件句柄）
- 复杂配置需要封装
- 需要生命周期管理（setup/teardown）

**灵活处理**:
- 简单的有状态逻辑可以用闭包或模块级变量
- 复杂的无状态逻辑可以用类来组织（如策略模式）
- 不要机械套用规则，根据实际情况判断

**决策问题**:
1. 这段逻辑需要记住状态吗？
2. 需要管理外部资源吗？
3. 配置复杂到需要封装吗？
4. 需要多个相关方法协作吗？

**示例**:
```python
# ✅ Function - 无状态转换
def calculate_tax(amount: float, rate: float = 0.08) -> float:
    return amount * rate

# ✅ Class - 有状态管理
class DatabaseConnection:
    def __init__(self, url: str):
        self.url = url
        self.connection = None

    def connect(self): ...
    def close(self): ...

# ✅ 灵活 - 简单状态用闭包
def create_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

**验证标准**:
- 代码易于测试吗？
- 命名清晰表达意图吗？
- 遵循单一职责原则吗？
- 易于理解和维护吗？

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

### 命名原则

**优先使用清晰的完整名称**:
- `user_count` 优于 `usr_cnt`
- `calculate_total_price` 优于 `calc_tot_prc`
- `process_payment` 优于 `proc_pmt`

**可接受的约定俗成缩写**:
- **领域通用**: `id`, `url`, `api`, `db`, `df` (DataFrame), `ctx` (context)
- **循环变量**: `i`, `j`, `k` (在明确的循环上下文中)
- **数学/科学**: `x`, `y`, `z`, `dx`, `dy` (在数学计算上下文中)
- **时间相关**: `ts` (timestamp), `dt` (datetime)

**避免类型前缀**:
```python
# ❌ 类型前缀（匈牙利命名法）
str_name = "John"
int_count = 10
list_items = []

# ✅ 清晰命名 + 类型提示
name: str = "John"
count: int = 10
items: list = []
```

**例外情况 - 需要区分同一概念的不同表示**:
```python
# ✅ 临时转换场景
price_str = "19.99"
price_float = float(price_str)

# ✅ 不同格式的同一数据
data_json = fetch_json()
data_df = pd.DataFrame(data_json)
```

### Direct Naming Principle
- 避免添加 `_clean`, `_new`, `_v2` 等限定词到生产代码
- 质量是默认期望，不是例外
- 用版本控制管理历史，不是命名
- **原则**: 如果代码不够好到成为主版本，就不应该存在

**例外**: 重构过程中的临时共存
```python
# ✅ 重构期间临时共存
def process_data_old(data): ...  # 待删除
def process_data(data): ...      # 新实现

# 重构完成后删除 _old 版本
```

### Design Patterns
- **Composition over Inheritance**: 优先组合而非继承
- **Dependency Injection**: 有效使用依赖注入
- **Flat Over Nested**: 避免深层继承，优先组合和依赖注入
- **Clear Naming**: 移除限定词，直接表达核心功能

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

## General Rules

### Documentation and Artifacts
- **No Unsolicited Documentation**: Do NOT create summary documents, README files, verification scripts, or markdown files unless I explicitly ask for them. Just do the work.
- **No Extra Files**: Avoid creating unnecessary files. Keep solutions focused on the actual requirement.

### Simplicity and Over-Engineering Prevention
- **Keep Solutions Simple**: Do not over-engineer with unnecessary abstractions, config formats (TOML, DAG, registry, CLI), or extra parameters. Start with the simplest approach that works. If I want more complexity, I'll ask.
- **No Unnecessary Additions**: Do not add method aliases, backward-compatibility wrappers, or extra parameters I didn't ask for.
- **Execute Directly**: When I give a concise instruction, execute it directly. Do not ask clarifying questions or explain options unless the request is genuinely ambiguous.
- **Context-Driven Architecture**: Refer to the "Architecture Decision Guide" section for choosing appropriate complexity levels. Don't apply patterns blindly.

### Project-Specific Conventions (Quant/Factor System)
- **Partition Format**: `month={YYYY-MM}/data.parquet` (data.parquet is the leaf file, no subdirectory wrapper)
- **Index vs Factor**: `market_dates` is an INDEX, not a factor
- **Data Types**: Factor data types are Float64 unless otherwise specified
- **Method Names**: Use `compute_and_save()` not `generate()` for factor computation

## Development Guidelines
- **UV Package Management**: Always use UV for Python package management
- **No Docker**: Explicitly avoid Docker for this project
- **No Python Tests**: Never write tests for Python code
- **No .env Comments**: Never use inline comments in .env files
- **Avoid node_modules**: Never look into node_modules
- **Code Quality: Ruff Only**: Use Ruff for linting and formatting, never Pylint

## Python Code Quality Standards

### Use Ruff, Not Pylint

**Core Rule**: Always use Ruff for code quality checks. Pylint is explicitly forbidden.

**Why Ruff?**
- **Speed**: 10-100x faster than Pylint (Rust implementation)
- **All-in-One**: Replaces Pylint + Flake8 + isort + Black + pyupgrade
- **Modern**: Better Python 3.11+ support, actively maintained
- **Simple Config**: Single `pyproject.toml` configuration

**Why Not Pylint?**
- Extremely slow on large codebases
- Complex configuration
- Redundant with Ruff's capabilities
- Outdated architecture

### Ruff Configuration Template

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py311"

exclude = [
    ".git",
    "__pycache__",
    ".venv",
    "build",
    "dist",
]

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["your_package"]

[tool.ruff.lint.per-file-ignores]
# Examples can modify sys.path before imports
"examples/**" = ["E402"]
```

### VS Code Integration

```json
// .vscode/settings.json
{
  "python.linting.enabled": false,
  "python.linting.pylintEnabled": false,
  "ruff.enable": true,
  "ruff.lint.enable": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "explicit",
      "source.fixAll": "explicit"
    }
  }
}
```

### Disable Pylint Completely

Create `.pylintrc` to prevent accidental usage:

```ini
# .pylintrc
[MASTER]
disable=all  # Pylint is disabled - use Ruff instead
```

### Daily Commands

```bash
# Check code quality
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Pre-commit workflow
uv run ruff check --fix . && uv run ruff format .
```

### Installation

```bash
# Add Ruff to dev dependencies
uv add --dev ruff

# Install VS Code extension: "Ruff" by Astral Software
# Uninstall Pylint extension if present
```

## Python CLI Standards

### Package Management with UV
- **Primary Tool**: Use `uv` for all Python package management operations
- **Installation**: `uv add package_name` instead of pip install
- **Dependencies**: Use `uv lock` to generate lock files
- **Virtual Environments**: `uv` automatically manages virtual environments
- **Scripts**: Define scripts in `pyproject.toml` under `[project.scripts]`

### CLI Development with Click
- **Framework**: Use `click` instead of `argparse` for CLI applications
- **Pattern**: Create `cli.py` as the main command interface
- **Structure**: Use click groups for multiple commands
- **Integration**: Combine click with the Command Dispatcher Pattern

```python
# ✅ Click-based CLI structure
import click
from .operations import sync_data, stream_data, fill_gaps

@click.group()
def cli():
    """Quantitative finance data processing tools."""
    pass

@cli.command()
@click.option('--batch-size', default=100, help='Batch size for processing')
def sync(batch_size: int):
    """Synchronize data incrementally."""
    sync_data(batch_size)

@cli.command() 
@click.option('--start-id', required=True, type=int)
@click.option('--end-id', required=True, type=int)
def fill_gaps(start_id: int, end_id: int):
    """Fill missing data for ID range."""
    fill_gaps(start_id, end_id)

if __name__ == '__main__':
    cli()
```

### Environment Management with dotenv
- **Files**: Use `.env` for defaults, `.env.local` for local overrides
- **Loading**: Use `python-dotenv` to load environment variables
- **Hierarchy**: `.env.local` > `.env` > system environment
- **Frequency-Based Configuration**:
  - `.env`: Parameters that change frequently (BATCH_SIZE, API_KEYS)
  - Code constants: Implementation details that rarely change

```python
# ✅ Environment configuration pattern
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env, then .env.local if it exists

# Frequently adjusted parameters
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))
MAX_CONCURRENT = int(os.getenv('MAX_CONCURRENT', 10))
API_KEY = os.getenv('API_KEY')

# Implementation constants (rarely change)
API_BASE_URL = "https://api.example.com/v1"
DEFAULT_TIMEOUT = 30
```

### Project Structure for Python CLI Tools

**原则**: 根据项目实际需求组织结构，不要照搬模板

#### 简单项目 (< 5模块)
```
project/
├── cli.py
├── core.py
├── storage.py
└── utils.py
```

#### 中等项目 (5-15模块)
```
project/
├── cli.py
├── core/
├── storage/
└── utils/
```

#### 复杂项目 (> 15模块)
```
project/
├── project/
│   ├── core/
│   ├── clients/
│   ├── database/
│   ├── business_domain/  # 根据实际业务命名
│   └── workflows/
├── pyproject.toml
└── .env
```

**不要**:
- ❌ 所有项目都用同一套目录结构
- ❌ 为了"看起来专业"而创建空目录
- ❌ 照搬别人的目录名（如`equity/`如果不是金融项目）

**应该**:
- ✅ 根据实际业务领域命名目录
- ✅ 根据模块数量决定是否分组
- ✅ 保持结构简单直到复杂度要求增加

### GitHub协作项目架构决策

**注意**: 以下原则适用于中大型团队协作项目

#### 核心原则
1. 模块边界清晰 - 便于代码审查
2. 导入路径一致
3. 扩展性友好

#### 何时应用？
- 团队 > 3人，需要频繁PR审查
- 不适用：个人项目、短期项目

#### 结构对比
- **平铺**: 简单直接，适合小团队
- **模块化**: 清晰分组，适合团队协作
- **过度嵌套**: 导入复杂，不推荐

---

# 🏗️ COMPLEXITY-DRIVEN ARCHITECTURE

## 核心原则

**按复杂度分层**:
- 简单功能 → 单文件模块
- 中等复杂 → 子目录 + 主文件
- 高度复杂 → 深层子目录结构

**统一导出策略**: 通过`__init__.py`隐藏内部复杂性，用户只需简单导入

**领域内聚**: 相关功能聚合在同一子目录，而非按技术层分散

---

# 🏗️ ARCHITECTURE DECISION GUIDE

## 核心原则：决策驱动，而非模式驱动

**不要**: 所有项目都用同一套架构模式
**应该**: 根据项目特点选择合适的架构

## 1. 复杂度驱动的架构选择

### 简单项目 (< 5个模块，1-2人团队，< 3个月)

```python
# ✅ 扁平结构 - 快速开发
project/
├── cli.py          # 命令入口
├── core.py         # 核心逻辑
├── storage.py      # 数据存储
└── utils.py        # 工具函数
```

**特点**:
- 直接依赖，易于理解
- 快速迭代，无架构负担
- 适合原型验证、小工具

**何时使用**:
- 功能单一明确
- 短期项目或实验性项目
- 团队规模小

### 中等项目 (5-15个模块，3-5人团队，3-12个月)

```python
# ✅ 功能分组 - 平衡组织性与灵活性
project/
├── cli.py
├── core/           # 核心逻辑群
│   ├── processor.py
│   └── calculator.py
├── storage/        # 存储层
│   ├── reader.py
│   └── writer.py
└── utils/
```

**特点**:
- 按功能域分组
- 2-3层浅层结构
- 保持灵活性

**何时使用**:
- 功能模块开始增多
- 需要多人协作
- 中期维护项目

### 复杂项目 (> 15个模块，> 5人团队，> 1年维护)

```python
# ✅ 分层架构 - 清晰边界与职责
project/
├── cli.py          # Layer 5: CLI
├── scheduler/      # Layer 4: 调度编排
├── registry/       # Layer 3: 元数据管理
├── operators/      # Layer 2: 核心算子
└── storage/        # Layer 1: 数据持久化
```

**特点**:
- 单向依赖（上层依赖下层）
- 每层职责明确
- 独立测试

**何时使用**:
- 模块间依赖复杂
- 长期维护需求
- 多团队协作

**案例**: Shadow Factor (5层架构，143GB数据，15+模块)

### 何时增加架构复杂度？

**触发信号**:
- ⚠️ 模块间依赖混乱，修改一处影响多处
- ⚠️ 测试需要mock大量依赖
- ⚠️ 新人理解代码需要超过1周
- ⚠️ 功能扩展需要修改多个不相关文件

**不要过早分层**:
- ❌ 项目初期，功能未稳定
- ❌ 依赖关系简单清晰
- ❌ 团队规模小（1-2人）
- ❌ 为了"看起来专业"而分层

## 2. 性能优化决策树

### 原则：先测量，再优化

```python
# ❌ 过早优化
def read_data():
    # 立即使用零拷贝、内存映射、并行读取...
    # 但数据量只有100行

# ✅ 根据实际需求优化
def read_data():
    # 先用简单方式实现
    # 测量发现瓶颈后再优化
```

### 何时需要零拷贝优化？

**触发条件**:
- 数据量 > 1GB
- 查询频率 > 100次/秒
- 延迟要求 < 100ms
- 内存受限环境

**实现方式**:
```python
# PyArrow零拷贝 + 内存映射
dataset = ds.dataset(
    data_path,
    format="parquet",
    partitioning="hive"
)

table = dataset.to_table(
    columns=["date", "code", "factor"],  # 列裁剪
    filter=date_filter,                   # 谓词下推
    use_threads=True                      # 并行读取
)
```

**收益**: Shadow Factor案例 - 34.45M rows/sec，500x回测加速

**成本**: 需要PyArrow、内存映射逻辑、预加载机制

**适用**: 回测系统、批量计算、实时交易

### 何时需要智能格式选择？

**触发条件**:
- 用户类型多样（技术用户 + 非技术用户）
- 数据量跨度大（KB到GB级别）
- 网络环境不确定

**实现方式**:
```python
def _smart_response(df, request, threshold=None):
    """根据数据量自动选择格式

    Args:
        threshold: 格式切换阈值，默认根据项目特点决定
    """
    data_size = len(df)

    # 阈值需要根据实际测量调整
    # Shadow Factor项目的经验值是10,000行
    # 你的项目可能不同
    if threshold is None:
        threshold = 10_000  # 示例值，需要根据实际情况调整

    if data_size < threshold:
        return json_response(df)  # 小数据：易用性优先
    else:
        return arrow_response(df)  # 大数据：性能优先
```

**收益**: 用户无需理解技术细节，API自动优化

**适用**: 面向多类用户的API服务

**如何确定阈值**:
1. 测量JSON和Arrow在不同数据量下的性能
2. 考虑网络带宽和延迟
3. 考虑客户端解析能力
4. 从保守值开始，根据监控数据调整

**反模式**:
- ❌ 所有项目都实现智能选择（过度设计）
- ❌ 没有测量就优化（premature optimization）
- ❌ 为单一用户群体做智能选择（增加复杂度无收益）
- ❌ 照搬别人的阈值（10,000不是魔法数字）

## 3. 部署场景设计

### 单一场景项目

**适用**: 明确的单一用户群体

```python
# 纯API服务
@app.get("/api/data")
def get_data():
    return data

# 纯本地工具
def process_local_files():
    pass

# 纯Python库
def calculate(x, y):
    return x + y
```

**何时使用**:
- 用户需求一致
- 部署环境单一
- 性能要求统一

### 双场景项目

**适用**: 两类不同需求的用户

```python
# 统一接口，不同实现
def create_client(mode: str = "auto", **kwargs):
    if mode == "remote":
        return RemoteClient(**kwargs)  # HTTP API
    elif mode == "local":
        return LocalReader(**kwargs)   # 零拷贝读取
```

**案例**: Shadow Factor
- **场景1**: 远程API服务（Web用户，网络传输，访问控制）
- **场景2**: 本地极速访问（回测系统，零拷贝，微秒级延迟）

**何时使用**:
- 远程用户 + 本地用户
- 交互式 + 批量处理
- 实时 + 离线分析

### 多场景项目

**适用**: 复杂的企业级系统

- API + CLI + SDK + Web UI
- 实时 + 批量 + 流式处理
- 多租户 + 多环境

**何时使用**:
- 用户群体复杂
- 部署环境多样
- 企业级需求

## 4. 实战经验库

### 经验1: 智能默认值优于显式配置

**场景**: Shadow Factor API格式选择

**问题**: 用户需要理解JSON vs Arrow IPC的技术区别

**解决**:
```python
# ❌ 之前：用户需要指定
df = api.query_factor("net_profit", format="arrow")

# ✅ 之后：自动选择
df = api.query_factor("net_profit")  # API根据数据量自动选择
```

**适用条件**:
- 技术细节对用户无价值
- 有明确的优化规则
- 高级用户可覆盖

**不适用**:
- 用户需要精确控制
- 没有明确的默认规则
- 选择影响业务逻辑

### 经验2: 零拷贝优化的ROI

**场景**: Shadow Factor回测系统

**收益**:
- 单次查询: 12x提升 (500ms → 40ms)
- 批量预加载: 12x提升 (5s → 0.4s)
- 回测循环: 500x提升 (500s → 1s)

**成本**:
- PyArrow依赖
- 内存映射逻辑
- 预加载机制
- 代码复杂度增加

**适用条件**:
- 数据量大（> 1GB）
- 查询频繁（反复读取）
- 延迟敏感（< 100ms）

**不适用**:
- 数据量小（< 100MB）
- 一次性查询
- 延迟不敏感

### 经验3: 分层架构的演进时机

**场景**: Shadow Factor从扁平到5层架构

**触发条件**:
- 模块数 > 15
- 依赖关系复杂
- 多人协作困难

**收益**:
- 测试性提升（每层独立测试）
- 可维护性提升（职责清晰）
- 扩展性提升（新功能有明确归属）

**成本**:
- 初期开发速度下降
- 学习曲线增加
- 重构成本

**适用**: 长期维护的复杂系统

**不适用**: 短期项目、原型验证

### 经验4: Parquet分区策略

**场景**: Shadow Factor 143GB因子数据存储

**策略**:
```
factor_database/data/
├── base_field=net_profit/    # 第一级分区
│   └── month=2024-01/         # 第二级分区
│       └── data.parquet       # 叶子文件
```

**收益**:
- 查询只扫描相关分区（分区裁剪）
- 列裁剪 + 谓词下推
- 并行读取

**适用**: 大规模时序数据、按时间/类别查询

**不适用**: 小数据集、随机访问模式

## 5. 架构决策检查清单

### 开始新项目时

**复杂度评估**:
- [ ] 预计模块数量？(< 5 / 5-15 / > 15)
- [ ] 团队规模？(1-2人 / 3-5人 / > 5人)
- [ ] 维护周期？(< 3个月 / 3-12个月 / > 1年)
- [ ] 依赖关系复杂度？(简单 / 中等 / 复杂)

**架构选择**:
- 简单项目 → 扁平结构
- 中等项目 → 功能分组
- 复杂项目 → 考虑分层（但不要过早）

### 遇到性能问题时

**先测量**:
- [ ] 实际数据量？(KB / MB / GB)
- [ ] 查询频率？(次/秒)
- [ ] 当前延迟？(ms)
- [ ] 目标延迟？(ms)
- [ ] 瓶颈在哪？(IO / CPU / 网络)

**再优化**:
- 数据量小 → 不需要优化
- 数据量大但查询少 → 简单缓存即可
- 数据量大且查询频繁 → 考虑零拷贝、预加载

### 设计API时

**用户分析**:
- [ ] 用户技术水平？(技术 / 非技术 / 混合)
- [ ] 数据量范围？(KB / MB / GB)
- [ ] 使用场景？(交互 / 批量 / 实时)
- [ ] 网络环境？(内网 / 公网 / 混合)

**设计选择**:
- 技术用户 → 可以暴露细节，提供精确控制
- 非技术用户 → 智能默认值，隐藏技术细节
- 混合用户 → 智能默认 + 高级覆盖选项

## 6. 反模式警示

### 架构反模式

❌ **过早分层**: 5个模块就搞5层架构
❌ **教条主义**: 所有项目都用同一套架构
❌ **过度抽象**: 为了"灵活性"增加3层间接层
❌ **盲目模仿**: 看到大公司用微服务就拆分

### 性能反模式

❌ **过早优化**: 没测量就优化
❌ **过度优化**: 100行数据用零拷贝
❌ **盲目优化**: 优化非瓶颈部分
❌ **技术炫技**: 为了用新技术而优化

### API设计反模式

❌ **暴露实现**: 让用户选择JSON vs Arrow
❌ **参数爆炸**: 20个配置参数
❌ **一刀切**: 所有场景用同一个API
❌ **过度灵活**: 支持100种组合但没人用

## 7. 如何使用这些经验？

### 正确方式

✅ **参考，不照搬**: 理解背后的原因，根据项目调整
✅ **测量，再决策**: 用数据支持架构决策
✅ **渐进演化**: 从简单开始，根据需要增加复杂度
✅ **问题驱动**: 遇到具体问题时参考相关经验

### 错误方式

❌ **直接复制**: 把Shadow Factor的5层架构复制到所有项目
❌ **盲目应用**: 不管项目特点，套用所有优化
❌ **教条执行**: 把经验当成必须遵守的规则
❌ **过度设计**: 为了"未来可能需要"而增加复杂度

## 总结

**核心思想**:
1. **决策驱动，而非模式驱动** - 根据实际情况选择架构
2. **测量驱动，而非假设驱动** - 用数据支持优化决策
3. **问题驱动，而非技术驱动** - 解决实际问题，不炫技
4. **渐进演化，而非一步到位** - 从简单开始，逐步优化

**记住**:
- 简单项目用简单架构
- 复杂项目才需要复杂架构
- 先让它工作，再让它快
- 架构为业务服务，不是反过来

## Documentation Links
- **SiliconCloud/SiliconFlow LLMs Documentation**:
  - Navigation: https://docs.siliconflow.cn/llms.txt
  - Fast Grep: https://docs.siliconflow.cn/llms-full.txt

---

# 🎯 DEVELOPMENT INTERACTION PRINCIPLES

## Core Rules

### 1. Clarification Before Implementation
Ask when request contains ambiguous terms, multiple approaches exist, or technical choices affect complexity

### 2. Minimal Viable Implementation
- Solve core problem first, ignore edge cases
- One file per distinct problem (unless complexity requires more)
- Single responsibility per module
- Defer optimization until requested

**复杂度指引**:
- 文件超过300行且难以理解 → 考虑拆分
- 一个模块有10+个文件但功能简单 → 可能过度拆分
- 依赖超过核心功能需要 → 可能过度设计

**渐进式开发**: 让它工作 → 让它好用 → 让它强大

### 3. Incremental Validation
Validate after clarification, after core implementation, before adding features

### 4. Complexity Transparency
Alert when file count > 2, line count > 150, new dependencies, or additional config needed

### 5. Scope Boundary Management
One module = one problem domain. Cross-cutting concerns need explicit approval.

### 6. Technical Debt Transparency
Communicate current limitations, future costs, alternative approaches, and performance implications

## Daily Checklist

**Before**: Requirements clear? Making assumptions? Simplest solution? Complexity justified?
**During**: Solving unmentioned problems? Complexity justified? Can simplify?
**After**: Confirmed solution meets needs? Obvious next steps? Ask about requirements?

---

# 📋 SESSION MANAGEMENT & WORKFLOW

## Break Tasks into Focused Sessions
Mega-sessions accumulate errors. Split into: design → implementation → validation → git

## Lead with Reference Files
Provide reference data upfront for validation tasks to enable pattern-matching

## Use Explicit Stop Constraints
Set clear boundaries: "Edit ONLY file X. Do not create new files."

---

# 🔧 GIT OPERATIONS

Always verify directory with `pwd` before git commands to avoid wrong directory errors.

---

# 🌐 FRAMEWORK-SPECIFIC GUIDELINES

## FastAPI Production Standards

### Router Organization
Use `APIRouter` for multiple endpoint groups, one router per domain

### Operation Separation
Extract business logic from endpoints - endpoints route, operations implement

### Deployment-First
Set up health endpoint + deployment pipeline before building features

### Access Control
Implement both authentication and rate limiting (use SlowAPI)

### Boundary Rules
- External API: Full validation, rate limiting, auth
- Internal operations: Trust parameters, let frameworks handle errors
- Use dependency injection for database sessions

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
- My Obsidian vault is at /Users/yanghh/obs. If you need to write down any summaries, notes, or knowledge pages, this is where you want to save them.
- NEVER GIT COMMIT WITH CLAUDE CODE COAUTHORSHIP
- Let errors fail naturally. Never use try-except pattern before the user asks you to.
- NEVER GIT COMMIT WITH CLAUDE CODE COAUTHORSHIP.