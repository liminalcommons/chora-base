# How-To: Batch Generate Content

**Goal:** Generate multiple content pieces in parallel using batch operations for 3-5× performance improvement.

**Prerequisites:**
- Chora Compose v1.1.0+ with batch_generate support
- Multiple content configs ready
- Understanding of [basic content generation](./use-demonstration-generator.md)

**Time:** 15-25 minutes

---

## Overview

**Batch generation** executes multiple content generation tasks in parallel, dramatically improving performance compared to sequential processing.

**Benefits:**
- ⚡ **3-5× faster** than sequential generation
- 🔄 **Parallel execution** - multiple pieces generated simultaneously
- 🛡️ **Error isolation** - one failure doesn't block others
- 📊 **Progress tracking** - monitor batch progress
- 💾 **Resource efficient** - better CPU/memory utilization

**When to Use:**
- Generating docs for multiple API endpoints
- Batch updating all weekly/monthly reports
- Creating documentation in multiple languages
- Regenerating all configs after template changes

---

## Quick Reference

###Batch Operations

| Operation | Sequential Time | Batch Time | Speedup |
|-----------|----------------|------------|---------|
| 5 pieces (2s each) | 10s | 3-4s | 2.5-3.3× |
| 10 pieces (2s each) | 20s | 4-6s | 3.3-5× |
| 20 pieces (2s each) | 40s | 8-12s | 3.3-5× |

**Max batch size:** 10 items (server limit)

---

## Task 1: Basic Batch Generation

**Scenario:** Generate documentation for 5 API endpoints.

### Step 1: Prepare Content Configs

First, ensure you have multiple content configs ready:

```bash
configs/content/
├── endpoint-users.json
├── endpoint-posts.json
├── endpoint-comments.json
├── endpoint-auth.json
└── endpoint-search.json
```

---

### Step 2: Generate All Endpoints in Parallel

**Using Claude Desktop:**
```
You: Generate content for these 5 configs in parallel:
- endpoint-users
- endpoint-posts
- endpoint-comments
- endpoint-auth
- endpoint-search
```

**What Claude Does:**

Calls `batch_generate` tool:

```json
{
  "content_config_ids": [
    "endpoint-users",
    "endpoint-posts",
    "endpoint-comments",
    "endpoint-auth",
    "endpoint-search"
  ],
  "output_dir": "output/api-docs"
}
```

**Expected Response:**
```
Claude: ✅ Batch generation completed

Results:
- Successfully generated: 5/5
- Failed: 0/5
- Total time: 3.2 seconds
- Average per item: 0.64 seconds
- Speedup: 3.1× (vs 10 seconds sequential)

Output files:
- output/api-docs/endpoint-users.md
- output/api-docs/endpoint-posts.md
- output/api-docs/endpoint-comments.md
- output/api-docs/endpoint-auth.md
- output/api-docs/endpoint-search.md
```

**Time Saved:** 6.8 seconds (68% faster)

---

## Task 2: Batch with Different Contexts

**Scenario:** Generate the same report for different teams/months.

### Generate Monthly Reports for 3 Teams

```
You: Generate monthly-sales-report for:
- Engineering team, October 2025
- Product team, October 2025
- Marketing team, October 2025
```

**What Claude Does:**

```json
{
  "operations": [
    {
      "content_config_id": "monthly-sales-report",
      "context": {"team": "Engineering", "month": "October", "year": 2025},
      "output_path": "output/reports/engineering-oct-2025.md"
    },
    {
      "content_config_id": "monthly-sales-report",
      "context": {"team": "Product", "month": "October", "year": 2025},
      "output_path": "output/reports/product-oct-2025.md"
    },
    {
      "content_config_id": "monthly-sales-report",
      "context": {"team": "Marketing", "month": "October", "year": 2025},
      "output_path": "output/reports/marketing-oct-2025.md"
    }
  ]
}
```

**Expected Response:**
```
Claude: ✅ Batch generation with custom contexts completed

Results:
- Engineering team: ✅ Generated (3.2 KB)
- Product team: ✅ Generated (2.8 KB)
- Marketing team: ✅ Generated (3.5 KB)

Total time: 2.1 seconds
Sequential would take: 6.0 seconds
Speedup: 2.9×
```

---

## Task 3: Handle Partial Failures

**Scenario:** Some configs fail validation, but don't block the rest.

### Mixed Valid and Invalid Configs

```
You: Batch generate:
- valid-config-1
- invalid-config-missing-template
- valid-config-2
- invalid-config-bad-context
- valid-config-3
```

**Expected Response:**
```
Claude: ⚠️  Batch generation completed with partial failures

Results:
✅ valid-config-1: Generated (2.4 KB)
❌ invalid-config-missing-template: Failed
   Error: Template file not found: missing.jinja
✅ valid-config-2: Generated (3.1 KB)
❌ invalid-config-bad-context: Failed
   Error: Missing required context field: 'title'
✅ valid-config-3: Generated (2.8 KB)

Summary:
- Successful: 3/5 (60%)
- Failed: 2/5 (40%)
- Total time: 2.5 seconds

Would you like to fix the failed configs and retry?
```

**What You Learned:**
- Errors are isolated - failures don't block successful generations
- Detailed error messages for each failed item
- Can retry just the failed items

---

## Task 4: Progress Monitoring

**Scenario:** Track progress of long-running batch operations.

### Large Batch with Progress Updates

```
You: Generate content for all 20 API endpoint configs. Show progress.
```

**Expected Response:**
```
Claude: Starting batch generation for 20 items...

Progress:
[████░░░░░░] 40% (8/20) - 4.2s elapsed
[████████░░] 80% (16/20) - 8.1s elapsed
[██████████] 100% (20/20) - 10.3s complete

Results:
- Successful: 19/20
- Failed: 1/20 (endpoint-deprecated - config not found)
- Total time: 10.3 seconds
- Sequential estimate: 40 seconds
- Speedup: 3.9×

All successful outputs in: output/api-docs/
```

---

## Task 5: Performance Optimization Strategies

### Strategy 1: Chunk Large Batches

**Problem:** Batch size limited to 10 items.

**Solution:** Split into chunks.

```python
# Agent pseudo-code
items = [...20 configs...]
max_batch_size = 10

chunks = [items[i:i+max_batch_size] for i in range(0, len(items), max_batch_size)]

for chunk in chunks:
    batch_generate(chunk)

# Result: 2 batches of 10 each
# Time: ~6-8 seconds (vs 40 seconds sequential)
```

---

### Strategy 2: Prioritize Critical Items

**Scenario:** Generate high-priority items first.

```
You: Batch generate these in priority order:
- High priority: user-guide, api-reference
- Medium priority: developer-guide, installation
- Low priority: changelog, contributing
```

**What Claude Does:**

Executes 3 batches in order:

```
Batch 1 (high): user-guide, api-reference (2 items, 2.1s)
Batch 2 (medium): developer-guide, installation (2 items, 2.3s)
Batch 3 (low): changelog, contributing (2 items, 2.2s)

Total: 6.6s (vs 12s sequential)
Critical docs available in 2.1s!
```

---

### Strategy 3: Resource Management

**Limit Concurrent Operations:**

```python
# For resource-intensive generators (e.g., AI-powered)
batch_size = min(server_limits["max_batch_size"], 5)  # Cap at 5 for heavy operations

# For lightweight generators (e.g., demonstration, jinja2)
batch_size = server_limits["max_batch_size"]  # Use full limit
```

---

## Task 6: Error Recovery Patterns

### Pattern 1: Retry Failed Items

```
You: Retry just the failed items from the previous batch
```

**What Claude Does:**

```json
{
  "content_config_ids": [
    "invalid-config-missing-template",  // Now fixed
    "invalid-config-bad-context"       // Now fixed
  ]
}
```

**Expected Response:**
```
Claude: ✅ Retry successful

Results:
✅ invalid-config-missing-template: Generated (2.7 KB)
   (Template file was added)
✅ invalid-config-bad-context: Generated (3.2 KB)
   (Context fixed)

All items from original batch now completed!
```

---

### Pattern 2: Fallback to Sequential

```python
# Try batch first
try:
    results = batch_generate(items)
except BatchNotSupported:
    # Fallback to sequential
    results = []
    for item in items:
        results.append(generate_content(item))
```

---

## Common Scenarios

### Scenario 1: Multi-Language Documentation

**Generate docs in 3 languages:**

```
You: Generate user-guide in English, Spanish, and French
```

**What Claude Does:**

```json
{
  "operations": [
    {
      "content_config_id": "user-guide",
      "context": {"language": "en"},
      "output_path": "output/docs/user-guide-en.md"
    },
    {
      "content_config_id": "user-guide",
      "context": {"language": "es"},
      "output_path": "output/docs/user-guide-es.md"
    },
    {
      "content_config_id": "user-guide",
      "context": {"language": "fr"},
      "output_path": "output/docs/user-guide-fr.md"
    }
  ]
}
```

**Result:** 3 language versions in ~2-3 seconds

---

### Scenario 2: Batch Regeneration After Template Update

**Template changed, regenerate all content using it:**

```
You: Find all configs using api-endpoint.md.jinja and regenerate them
```

**What Claude Does:**

1. Lists all content configs
2. Filters by template: api-endpoint.md.jinja
3. Batch regenerates all matches

**Expected Response:**
```
Claude: Found 12 configs using api-endpoint.md.jinja

Regenerating all 12 in batches...

Batch 1 (10 items): ✅ Complete (4.2s)
Batch 2 (2 items): ✅ Complete (1.1s)

All 12 configs regenerated with updated template.
Total time: 5.3 seconds (vs 24 seconds sequential)
```

---

## Best Practices

### ✅ Do's

1. **Use Batch for Similar Items**
   ```
   ✅ Good: 10 API endpoint docs (same template, different data)
   ❌ Bad: Mixed configs with different generators/complexity
   ```

2. **Respect Server Limits**
   ```python
   limits = fetch("capabilities://server")["limits"]
   batch_size = min(len(items), limits["max_batch_size"])
   ```

3. **Handle Partial Failures Gracefully**
   ```python
   results = batch_generate(items)
   failed = [r for r in results if not r.success]
   if failed:
       retry(failed)
   ```

4. **Monitor Progress for Large Batches**
   ```
   For >5 items: Show progress updates
   For >10 items: Use chunking
   ```

---

### ❌ Don'ts

1. **Don't Batch Dissimilar Items**
   ```
   ❌ Bad: Mix jinja2 + AI-powered generators
   ✅ Good: Batch same generator type together
   ```

2. **Don't Ignore Batch Size Limits**
   ```
   ❌ Bad: batch_generate(100_items)  // Fails!
   ✅ Good: chunk_and_batch(100_items, max_size=10)
   ```

3. **Don't Block on Batch Failures**
   ```python
   ❌ Bad:
   try:
       batch_generate(items)
   except BatchError:
       exit()  # Give up entirely

   ✅ Good:
   results = batch_generate(items)
   successful = [r for r in results if r.success]
   # Continue with successful items
   ```

---

## Performance Comparison

**Benchmark: 10 API Endpoint Docs (2 seconds each)**

| Method | Time | Speedup | Use Case |
|--------|------|---------|----------|
| Sequential | 20s | 1× (baseline) | Small number of items |
| Batch (no chunking) | 4-5s | 4-5× | ≤10 items |
| Batch (with chunking) | 8-10s | 2-2.5× | >10 items |
| Parallel manual | Varies | Unpredictable | Not recommended |

**Recommendation:** Always use batch_generate when available and have 2+ items.

---

## Troubleshooting

### Issue: Batch Times Out

**Error:**
```
Batch generation timed out after 30 seconds
```

**Cause:** Items take too long individually.

**Solutions:**
1. Reduce batch size
   ```python
   batch_size = 5  # Instead of 10
   ```

2. Optimize templates (remove expensive operations)

3. Use preview_generation first to estimate time

---

### Issue: High Memory Usage

**Problem:** Server memory spikes during batch.

**Solutions:**
1. Lower batch size
2. Stagger batches with delays
3. Check for memory leaks in templates

---

### Issue: Inconsistent Results

**Problem:** Same batch sometimes succeeds, sometimes fails.

**Cause:** Race conditions or resource contention.

**Solutions:**
1. Add small delays between batches
2. Reduce batch size
3. Check system resources (CPU, RAM)

---

## Related Documentation

- **[Tutorial: MCP Integration Deep Dive](../../tutorials/advanced/01-mcp-integration-deep-dive.md)** - Complete batch workflow example
- **[How-To: Preview Before Generating](./preview-before-generating.md)** - Test before batch execution
- **[Reference: MCP Tool Catalog](../../reference/api/mcp/tool-catalog.md)** - batch_generate tool reference
- **[E2E Test Suite: Batch Operations](../../mcp/E2E_BATCH_OPERATIONS.md)** - Comprehensive test examples

---

**You can now use batch operations to generate content 3-5× faster!**
