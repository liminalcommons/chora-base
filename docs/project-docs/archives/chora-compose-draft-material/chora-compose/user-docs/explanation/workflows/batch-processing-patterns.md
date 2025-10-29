# Batch Processing Patterns in Chora Compose

**Purpose**: Understand the philosophy, architecture, and trade-offs of batch content generation in chora-compose.

**Audience**: Developers designing batch workflows, technical leads optimizing generation pipelines, users scaling content operations.

---

## Overview

Batch processing in chora-compose enables parallel content generation, reducing total execution time by 3-5× compared to sequential processing. However, batch operations introduce complexity around error handling, resource management, and workflow orchestration.

This document explains **WHY** batch processing works the way it does, **WHEN** to use different patterns, and **HOW** to make informed trade-offs for your use case.

---

## The Sequential vs Parallel Spectrum

### Sequential Processing (Default)

**Pattern**: Generate one piece of content at a time, wait for completion before starting next.

```python
# Sequential pattern
for config_id in config_ids:
    output = generate_content(config_id)
    save(output)
```

**Characteristics**:
- **Simple**: Straightforward control flow
- **Predictable**: Execution order guaranteed
- **Safe**: No resource contention
- **Slow**: Total time = sum of individual times

**Time complexity**: `O(n)` where n = number of items

**Example** (5 configs, 2 seconds each):
```
Config 1: [████████] 2s
Config 2:          [████████] 2s
Config 3:                   [████████] 2s
Config 4:                            [████████] 2s
Config 5:                                     [████████] 2s
Total: 10 seconds
```

### Parallel Processing (Batch)

**Pattern**: Start multiple generations simultaneously, wait for all to complete.

```python
# Parallel pattern
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(generate_content, id) for id in config_ids]
    results = [f.result() for f in futures]
```

**Characteristics**:
- **Fast**: Overlapping execution reduces total time
- **Complex**: Concurrent programming challenges
- **Resource-intensive**: Multiple operations in memory
- **Non-deterministic**: Completion order varies

**Time complexity**: `O(max(t1, t2, ..., tn))` where ti = time for item i

**Example** (5 configs, 2 seconds each, 5 workers):
```
Config 1: [████████]
Config 2: [████████]
Config 3: [████████]
Config 4: [████████]
Config 5: [████████]
Total: 2-3 seconds (3.3-5× speedup)
```

---

## Why Parallel Processing Works

### CPU-Bound vs I/O-Bound Operations

**I/O-bound** (waiting for external resources):
- API calls (Claude API for code_generation)
- File I/O (reading configs, writing output)
- Network requests (fetching external data)

**CPU-bound** (computation-intensive):
- Jinja2 template rendering
- JSON parsing/validation
- String manipulation

**Key insight**: Most chora-compose operations are **I/O-bound** (waiting for file system or APIs), making parallelism highly effective.

### Parallelism Strategies

#### 1. Threading (I/O-bound workloads)

**Best for**: File I/O, API calls, network operations

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(generate_content, id) for id in config_ids]
    results = [f.result() for f in futures]
```

**Why it works**:
- Threads share memory (low overhead)
- GIL released during I/O (true parallelism for I/O)
- Lightweight (thousands of threads possible)

**Trade-off**: Not effective for CPU-bound work (GIL limits parallelism)

#### 2. Multiprocessing (CPU-bound workloads)

**Best for**: Heavy computation, Jinja2 rendering at scale

```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(generate_content, id) for id in config_ids]
    results = [f.result() for f in futures]
```

**Why it works**:
- Each process has own Python interpreter (no GIL)
- True CPU parallelism
- Isolates failures (one crash doesn't affect others)

**Trade-off**: Higher overhead (process creation, memory duplication)

#### 3. Async/Await (I/O-bound, cooperative)

**Best for**: Many concurrent operations, event-driven workflows

```python
import asyncio

async def generate_all(config_ids):
    tasks = [generate_content_async(id) for id in config_ids]
    return await asyncio.gather(*tasks)

results = asyncio.run(generate_all(config_ids))
```

**Why it works**:
- Single-threaded, cooperative multitasking
- Extremely lightweight (100K+ concurrent operations)
- Explicit control flow (await points)

**Trade-off**: Requires async-compatible libraries (chora-compose currently sync-only)

### Chora Compose's Choice: Threading

**Decision**: Use threading for batch operations.

**Rationale**:
1. **I/O-bound dominant**: 80% of time spent waiting (file I/O, API calls)
2. **Simplicity**: Easier to implement than multiprocessing
3. **Memory efficiency**: Shared memory, no data serialization
4. **Compatibility**: Works with existing sync codebase

**Future consideration**: Async support for 10K+ concurrent operations.

---

## Batch Size Optimization

### The Goldilocks Problem

**Too small** (batch_size = 1):
- No parallelism benefit
- Sequential execution time

**Too large** (batch_size = 1000):
- Memory exhaustion
- Resource contention
- Diminishing returns

**Just right** (batch_size = 5-10):
- Balance parallelism and resource usage
- Optimal for most workloads

### Determining Optimal Batch Size

**Formula**:
```
optimal_batch_size = min(
    num_cpu_cores * 2,  # CPU capacity
    available_memory / memory_per_operation,  # Memory limit
    api_rate_limit,  # External constraints
    10  # Chora Compose server limit
)
```

**Example calculations**:

| Constraint | Value | Limit |
|------------|-------|-------|
| CPU cores | 8 | 16 workers |
| Memory available | 8 GB | ~40 workers (200 MB/operation) |
| API rate limit | 60 req/min | 1 req/sec = ~5 concurrent |
| Server limit | N/A | 10 workers (hard limit) |

**Result**: `min(16, 40, 5, 10) = 5 workers` (API rate limit is bottleneck)

### Chora Compose Limits

**MCP batch_generate tool**:
- Max batch size: **10 items** (server enforced)
- Timeout: **5 minutes** total
- Memory: **1 GB** per batch

**Why these limits?**
1. **Prevent resource exhaustion** (protect server stability)
2. **Reasonable timeout** (users expect <5min response)
3. **Fair usage** (prevent monopolization in shared environments)

**Workaround for >10 items**: Chunk into multiple batches.

```python
# Chunking pattern
chunk_size = 10
for i in range(0, len(config_ids), chunk_size):
    chunk = config_ids[i:i + chunk_size]
    batch_generate(chunk)
```

---

## Error Handling Strategies

### Pattern 1: Fail-Fast (Default)

**Behavior**: Stop entire batch on first error.

```python
try:
    results = batch_generate(config_ids)
except GenerationError as e:
    # One failure stops all
    raise
```

**Pros**:
- ✅ Immediate feedback
- ✅ No partial results
- ✅ Clear error state

**Cons**:
- ❌ Wastes successful generations
- ❌ Cannot retry only failures
- ❌ All-or-nothing outcome

**When to use**: Critical operations where partial success is unacceptable (e.g., deploying interconnected docs).

### Pattern 2: Collect-Errors (Resilient)

**Behavior**: Continue batch, collect all errors, report at end.

```python
results = []
errors = []

for config_id in config_ids:
    try:
        result = generate_content(config_id)
        results.append(result)
    except GenerationError as e:
        errors.append((config_id, e))

# Summary
print(f"Successful: {len(results)}/{len(config_ids)}")
print(f"Failed: {len(errors)}/{len(config_ids)}")
```

**Pros**:
- ✅ Partial success useful
- ✅ Retry only failures
- ✅ Better resource utilization

**Cons**:
- ❌ Delayed error feedback
- ❌ Complex error reporting
- ❌ Partial state management

**When to use**: Independent operations where partial success is valuable (e.g., generating docs for 100 endpoints).

### Pattern 3: Retry-on-Failure (Robust)

**Behavior**: Automatically retry failed operations with backoff.

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def generate_with_retry(config_id):
    return generate_content(config_id)

# Use in batch
results = [generate_with_retry(id) for id in config_ids]
```

**Pros**:
- ✅ Handles transient failures
- ✅ Automatic recovery
- ✅ Configurable retry logic

**Cons**:
- ❌ Longer execution time
- ❌ May retry non-recoverable errors
- ❌ Complex timeout management

**When to use**: Operations with transient failures (e.g., API rate limits, network hiccups).

### Chora Compose's Approach

**Default**: **Collect-Errors** pattern for batch operations.

**Implementation** (from MCP tools):
```python
# Pseudo-code from batch_generate
successful = []
failed = []

for config_id in config_ids:
    try:
        result = generate_content(config_id)
        successful.append(result)
    except Exception as e:
        failed.append({"config_id": config_id, "error": str(e)})

return BatchResult(
    total=len(config_ids),
    successful=len(successful),
    failed=len(failed),
    failures=failed
)
```

**Rationale**:
- Partial success is valuable (e.g., 9/10 docs generated is better than 0/10)
- Users can retry only failed items
- Better resource utilization

**User control**: Can implement fail-fast by checking results and raising exception if any failures.

---

## Progress Tracking Patterns

### Pattern 1: No Tracking (Simple)

**Behavior**: Wait for batch completion, report final status.

```python
results = batch_generate(config_ids)
print(f"Done: {results.successful}/{results.total}")
```

**Pros**:
- ✅ Simplest implementation
- ✅ No overhead

**Cons**:
- ❌ No visibility during execution
- ❌ Users don't know if system is working or hung

**When to use**: Small batches (<5 items, <30s total time).

### Pattern 2: Callback Progress (Intermediate)

**Behavior**: Callback function invoked on each completion.

```python
def on_progress(completed, total, config_id):
    print(f"[{completed}/{total}] Completed: {config_id}")

batch_generate(config_ids, on_progress=on_progress)
# [1/10] Completed: endpoint-users
# [2/10] Completed: endpoint-posts
# ...
```

**Pros**:
- ✅ Real-time feedback
- ✅ Low implementation complexity
- ✅ User can track progress

**Cons**:
- ❌ Blocking callback (slows execution slightly)
- ❌ No structured progress data

**When to use**: Medium batches (5-20 items, 1-5 minutes).

### Pattern 3: Event Streaming (Advanced)

**Behavior**: Emit events to telemetry/event bus, consume separately.

```python
# Producer
emit_event(BatchStartedEvent(batch_id, total=len(config_ids)))
for result in batch_generate_stream(config_ids):
    emit_event(ItemCompletedEvent(batch_id, config_id=result.id))
emit_event(BatchCompletedEvent(batch_id, successful, failed))

# Consumer
def watch_batch_progress(batch_id):
    for event in subscribe_events(batch_id):
        if event.type == "ItemCompleted":
            update_progress_bar(event)
```

**Pros**:
- ✅ Decoupled progress tracking
- ✅ Multiple consumers (UI, logs, metrics)
- ✅ Async, non-blocking

**Cons**:
- ❌ Requires event infrastructure
- ❌ Higher complexity
- ❌ Eventual consistency (slight delay)

**When to use**: Large batches (100+ items, >10 minutes), production workflows.

### Chora Compose's Approach

**Current**: **No Tracking** (Pattern 1) for simplicity.

**Future roadmap**:
- Pattern 2 (callback) for v1.2
- Pattern 3 (event streaming) for v1.3 (integrates with existing telemetry)

**Workaround**: Users can wrap batch operations with custom progress tracking:

```python
from tqdm import tqdm

for config_id in tqdm(config_ids, desc="Generating"):
    generate_content(config_id)  # Sequential with progress bar
```

---

## Resource Management

### Memory Management

**Problem**: Parallel generation increases memory usage (all operations in memory simultaneously).

**Pattern 1: Bounded Worker Pool**

```python
# Limit concurrent workers
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(generate_content, id) for id in config_ids]
    results = [f.result() for f in futures]
```

**Effect**: Max 5 concurrent operations, bounded memory usage.

**Pattern 2: Streaming Results**

```python
# Process results as they complete (don't accumulate in memory)
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(generate_content, id): id for id in config_ids}
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        save(result)  # Save immediately, free memory
```

**Effect**: Results processed incrementally, constant memory usage.

### API Rate Limiting

**Problem**: Parallel API calls can exceed rate limits (e.g., Claude API: 60 req/min).

**Pattern 1: Throttling**

```python
import time

def rate_limited_generate(config_id, min_interval=1.0):
    """Ensure minimum interval between API calls."""
    global last_call_time
    now = time.time()
    elapsed = now - last_call_time
    if elapsed < min_interval:
        time.sleep(min_interval - elapsed)
    last_call_time = time.time()
    return generate_content(config_id)
```

**Effect**: Respects rate limit, may increase total time.

**Pattern 2: Semaphore (Concurrent Limit)**

```python
from threading import Semaphore

api_semaphore = Semaphore(5)  # Max 5 concurrent API calls

def generate_with_limit(config_id):
    with api_semaphore:
        return generate_content(config_id)

# Use in batch
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(generate_with_limit, id) for id in config_ids]
    results = [f.result() for f in futures]
```

**Effect**: Only 5 concurrent API calls, others queued.

### Chora Compose's Resource Limits

**MCP batch_generate**:
- Max workers: **10** (threading)
- Memory limit: **1 GB** per batch
- Timeout: **5 minutes** (300s)

**code_generation** (uses Claude API):
- Implicit rate limit: **Respects API throttling**
- Semaphore: **Not implemented** (users must manage externally)

**Recommendation**: For code_generation batches, reduce batch_size to 3-5 to stay under API rate limits.

---

## Combining Generators in Batches

### Homogeneous Batches (Single Generator)

**Pattern**: All items use same generator type.

```python
# All use jinja2
batch_generate([
    "endpoint-users",     # jinja2
    "endpoint-posts",     # jinja2
    "endpoint-comments"   # jinja2
])
```

**Characteristics**:
- Predictable performance (all operations similar duration)
- Simpler error handling (same failure modes)
- Easier to optimize

### Heterogeneous Batches (Multiple Generators)

**Pattern**: Items use different generators.

```python
# Mixed generators
batch_generate([
    "readme",             # demonstration (fast, <1ms)
    "release-notes",      # template_fill (fast, <5ms)
    "api-docs",           # jinja2 (medium, 10-50ms)
    "utility-function"    # code_generation (slow, 10-30s)
])
```

**Characteristics**:
- Unpredictable completion time (dominated by slowest)
- Complex resource requirements (API vs local)
- Harder to optimize

**Trade-off**: Fast operations (demonstration, template_fill) wait for slow operations (code_generation).

**Optimization**: Separate batches by generator type.

```python
# Batch 1: Fast generators
batch_generate(["readme", "release-notes", "api-docs"])  # <1s

# Batch 2: Slow generators
batch_generate(["utility-function", "test-helpers"])  # 30-60s
```

**Benefit**: Fast operations complete quickly, don't wait for slow operations.

---

## Best Practices

### Do ✅

1. **Batch similar operations together**
   ```python
   # ✅ Good: All jinja2, predictable performance
   batch_generate(["endpoint-1", "endpoint-2", "endpoint-3"])
   ```

2. **Use collect-errors for independent operations**
   ```python
   # ✅ Good: Partial success useful
   result = batch_generate(endpoint_ids)
   if result.failed > 0:
       retry_failed(result.failures)
   ```

3. **Respect rate limits**
   ```python
   # ✅ Good: Small batches for API-heavy operations
   for chunk in chunks(config_ids, chunk_size=3):
       batch_generate(chunk)  # Stays under API rate limit
   ```

4. **Monitor memory usage**
   ```python
   # ✅ Good: Stream results, don't accumulate
   for result in batch_generate_stream(config_ids):
       save(result)  # Immediately free memory
   ```

### Don't ❌

1. **Don't batch tiny operations**
   ```python
   # ❌ Bad: Overhead > benefit
   batch_generate(["one-line-readme"])  # Takes longer than sequential
   ```

2. **Don't mix fast and slow generators**
   ```python
   # ❌ Bad: Fast operations wait for slow
   batch_generate([
       "readme",  # <1ms
       "ai-code"  # 30s
   ])  # Total time: 30s (no benefit for readme)
   ```

3. **Don't exceed batch limits**
   ```python
   # ❌ Bad: Exceeds server limit
   batch_generate(range(100))  # Server rejects >10 items
   ```

4. **Don't ignore error patterns**
   ```python
   # ❌ Bad: Silent failures
   result = batch_generate(config_ids)
   # Doesn't check result.failed, misses errors
   ```

---

## Performance Benchmarks

### Generator Performance Profiles

| Generator | Avg Time | Parallelism Benefit | Notes |
|-----------|----------|---------------------|-------|
| `demonstration` | <1ms | Low | Too fast to benefit |
| `template_fill` | <5ms | Low | Minimal I/O |
| `bdd_scenario` | <10ms | Low-Medium | Some I/O |
| `jinja2` | 10-50ms | Medium | File I/O, template parsing |
| `code_generation` | 10-30s | High | API calls, I/O-bound |

**Interpretation**:
- **demonstration/template_fill**: Batch overhead > benefit (use sequential)
- **jinja2**: Moderate benefit (2-3× speedup typical)
- **code_generation**: High benefit (3-5× speedup, limited by API rate)

### Real-World Benchmarks

**Scenario**: Generate docs for 10 API endpoints (jinja2)

| Approach | Time | Speedup | Notes |
|----------|------|---------|-------|
| Sequential | 500ms | 1× | Baseline |
| Batch (5 workers) | 150ms | 3.3× | Optimal |
| Batch (10 workers) | 120ms | 4.2× | Diminishing returns |
| Batch (20 workers) | 110ms | 4.5× | Overhead increases |

**Takeaway**: Sweet spot is 5-10 workers for jinja2.

**Scenario**: Generate 5 utility functions (code_generation)

| Approach | Time | Speedup | Notes |
|----------|------|---------|-------|
| Sequential | 150s | 1× | Baseline |
| Batch (3 workers) | 50s | 3× | Under API rate limit |
| Batch (5 workers) | 45s | 3.3× | Near API rate limit |
| Batch (10 workers) | 45s | 3.3× | Hit API rate limit (no benefit) |

**Takeaway**: API rate limit caps benefit at 3-5 workers for code_generation.

---

## Trade-offs Summary

| Aspect | Sequential | Parallel (Batch) |
|--------|-----------|------------------|
| **Performance** | Slow (linear time) | Fast (3-5× speedup) |
| **Complexity** | Simple | Complex (concurrency) |
| **Resource Usage** | Low (one operation at a time) | High (multiple in memory) |
| **Error Handling** | Simple (fail immediately) | Complex (collect/retry) |
| **Debugging** | Easy (linear execution) | Hard (race conditions) |
| **Use Case** | Small batches, simple ops | Large batches, I/O-bound |

**Decision rule**:
- **<5 items OR <10s total time**: Use sequential (simplicity > speed)
- **5-50 items AND I/O-bound**: Use batch with 5-10 workers
- **>50 items**: Chunk into batches of 10, process sequentially

---

## Related Documentation

### How-To Guides
- [Batch Generate Content](../../how-to/generation/batch-generate-content.md) - Step-by-step batch generation
- [Generate Multiple Artifacts](../../how-to/generation/generate-multiple-artifacts.md) - Artifact batch patterns

### Explanation
- [Testing and Validation Approaches](testing-validation-approaches.md) - Validation in batch workflows
- [Event-Driven Telemetry](../design-decisions/event-driven-telemetry.md) - Progress tracking via events

### Reference
- [MCP Tool Catalog](../../reference/api/mcp/tool-catalog.md) - batch_generate tool API

---

## Summary

**Key Principles**:

1. **Parallelism works for I/O-bound operations** (file I/O, API calls)
2. **Optimal batch size is 5-10 workers** (balance parallelism and resources)
3. **Collect errors, don't fail fast** (partial success is valuable)
4. **Respect rate limits** (especially for code_generation)
5. **Separate fast and slow generators** (don't mix in same batch)

**When to use batch processing**:
- ✅ Multiple configs to generate (>5 items)
- ✅ I/O-bound operations (jinja2, code_generation)
- ✅ Independent operations (failures don't cascade)
- ✅ Total time >30 seconds sequential

**When to use sequential processing**:
- ✅ Small batches (<5 items)
- ✅ Fast generators (demonstration, template_fill)
- ✅ Dependent operations (order matters)
- ✅ Total time <10 seconds

**Philosophy**: Start simple (sequential), optimize when measured performance is insufficient.

---

**Last Updated**: 2025-10-21 | **Phase**: Sprint 4 - Ecosystem Expansion
