---
description: Profile Python code with cProfile, identify bottlenecks, and propose speedup optimizations
skill_type: user-invocable
---

# cProfile Speedup Skill

When invoked, this skill will:
1. Insert cProfile instrumentation into the target code
2. Run performance analysis with real data
3. Identify the top bottlenecks (functions consuming most time)
4. Propose concrete optimization strategies

## Usage

```bash
/cprofile-speedup <script-path-or-description>
```

Examples:
- `/cprofile-speedup scripts/run_backtest.py`
- `/cprofile-speedup the backtest engine`
- `/cprofile-speedup data loading in WideTableProvider`

## What This Skill Does

### 1. Instrument with cProfile
- Wraps target code with `cProfile.Profile()`
- Captures all function calls and timing
- Sorts by both cumulative time and total time

### 2. Add Custom Tracking (when needed)
- Monkey-patches hot functions to track:
  - Call counts
  - Per-call timing
  - Cache hit/miss rates
  - Data access patterns
- Uses `time.perf_counter()` for precision

### 3. Analyze Results
- Identifies top 1-3 bottlenecks (80/20 rule)
- Calculates % of total runtime
- Shows call counts and per-call averages
- Explains root cause (not just symptoms)

### 4. Propose Optimizations
Based on the bottleneck type:
- **O(N) in loop** → Cache, index, or batch
- **Repeated work** → Memoization or pre-computation
- **Sequential I/O** → Parallel or async
- **Large data copies** → Views or in-place operations
- **Inefficient algorithms** → Better data structures

## Output Format

```
PROFILING RESULTS
================================================================================
Target: run_backtest() in scripts/benchmark.py
Total time: 35.43s

TOP BOTTLENECK:
  Function: get_stock_data()
  Time: 30.07s (84.9% of total)
  Calls: 8,796
  Per-call: 3.42ms
  Root cause: O(N) filter scan on 134K rows per call

OPTIMIZATION PROPOSAL:
  Strategy: Add per-date stock index cache
  Expected: 5-10x speedup
  Implementation:
    1. Cache daily data as {stock_code: row} dict
    2. Change get_stock_data() from O(N) filter to O(1) lookup
    3. Build index lazily on first access per date

  Code change:
    [具体代码示例]
```

## Workflow

1. **Profile** - Run cProfile + custom instrumentation
2. **Identify** - Find the #1 bottleneck
3. **Diagnose** - Understand why it's slow
4. **Propose** - Suggest concrete fix with code
5. **Verify** - Re-profile after fix to confirm improvement

## Notes

- Always uses real data, never mocks
- Focuses on the actual use case
- Proposes minimal, targeted fixes
- Provides before/after metrics
- Includes verification steps
