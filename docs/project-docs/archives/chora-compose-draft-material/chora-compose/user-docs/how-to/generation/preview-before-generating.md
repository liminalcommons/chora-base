# How-To: Preview Before Generating

**Goal:** Test content generation without creating files or side effects using preview capabilities.

**Prerequisites:**
- Chora Compose v1.1.0+ with preview_generation support
- At least one content config ready
- Understanding of [basic content generation](./use-demonstration-generator.md)

**Time:** 10-15 minutes

---

## Overview

**Preview generation** allows you to test templates, validate context data, and estimate costs before committing to file creation. This is essential for:

- Testing new templates without cluttering output directories
- Validating context data before batch operations
- Estimating costs for AI-powered generators
- Debugging template logic and syntax
- Iterating on designs without cleanup overhead

**Key Difference:**
```
preview_generation:  Template + Context → Preview (no files)
generate_content:    Template + Context → File on disk
```

---

## Quick Reference

### Preview vs Generate Comparison

| Aspect | preview_generation | generate_content |
|--------|-------------------|------------------|
| **Output** | Returns content as string | Writes to file on disk |
| **Side Effects** | None | Creates file, updates metadata |
| **Speed** | Slightly faster (no I/O) | Slower (disk writes) |
| **Use Case** | Testing, validation | Production generation |
| **Caching** | Not cached | Cached by default |
| **Idempotent** | Yes (always) | Yes (if cache enabled) |

### When to Use Preview

| Scenario | Use preview_generation | Use generate_content |
|----------|----------------------|---------------------|
| Testing new template | ✅ | ❌ |
| Validating context data | ✅ | ❌ |
| Production generation | ❌ | ✅ |
| Cost estimation | ✅ | ❌ |
| Debugging template logic | ✅ | ❌ |
| Batch operations | ❌ (use batch_generate) | ✅ |

---

## Task 1: Basic Preview Generation

**Scenario:** Test a new template before creating files.

### Step 1: Preview Content

**Using Claude Desktop:**
```
You: Preview content generation for 'user-guide' without creating files
```

**What Claude Does:**

Calls `preview_generation` tool:

```json
{
  "content_config_id": "user-guide"
}
```

**Expected Response:**
```
Claude: ✅ Preview generated successfully

Preview Output:
─────────────────────────────────────────
# User Guide

Welcome to the User Guide for MyApp v2.1.

## Getting Started

1. Install the application
2. Configure your settings
3. Start using the features

[... full content preview ...]
─────────────────────────────────────────

Length: 2,847 characters (~500 words)
Estimated file size: 2.8 KB

No files were created. Use generate_content to save to disk.
```

**What You Learned:**
- Preview shows exact output without side effects
- No files created, no cleanup needed
- Can iterate quickly on templates

---

## Task 2: Validate Context Data

**Scenario:** Test if context data renders correctly before batch generation.

### Step 1: Preview with Custom Context

```
You: Preview user-guide with context: {"version": "3.0", "release_date": "2025-10-16"}
```

**What Claude Does:**

```json
{
  "content_config_id": "user-guide",
  "context_override": {
    "version": "3.0",
    "release_date": "2025-10-16"
  }
}
```

**Expected Response:**
```
Claude: ✅ Preview with custom context

Preview Output:
─────────────────────────────────────────
# User Guide

Welcome to the User Guide for MyApp v3.0.
Released: 2025-10-16

[... content with custom context applied ...]
─────────────────────────────────────────

Context validation:
✅ version: "3.0" (rendered correctly)
✅ release_date: "2025-10-16" (formatted as expected)

All context fields rendered successfully.
```

**What You Learned:**
- Preview validates context data integration
- Catch missing or malformed context early
- Test different context values without file spam

---

## Task 3: Test Template Syntax

**Scenario:** Debug Jinja2 template logic before deployment.

### Step 1: Preview with Edge Case Context

```
You: Preview api-endpoint with context: {"methods": [], "auth_required": null}
```

**Expected Response (Success Case):**
```
Claude: ✅ Preview successful with edge case context

Preview Output:
─────────────────────────────────────────
# API Endpoint Documentation

**Methods:** None defined
**Authentication:** Not specified

[... gracefully handled empty/null values ...]
─────────────────────────────────────────

Template handled edge cases correctly.
```

**Expected Response (Failure Case):**
```
Claude: ❌ Preview failed - Template error

Error: UndefinedError at line 42
  {% for method in methods %}
  'NoneType' object is not iterable

Suggested fix:
  {% for method in methods|default([]) %}

No files were created. Fix template and retry.
```

**What You Learned:**
- Preview safely tests edge cases
- Template errors caught without file creation
- Immediate feedback for debugging

---

## Task 4: Estimate AI Generation Costs

**Scenario:** Estimate costs for AI-powered generation before running batch.

### Step 1: Preview AI-Powered Generation

```
You: Preview technical-spec with AI generator to estimate cost
```

**What Claude Does:**

```json
{
  "content_config_id": "technical-spec",
  "generator_override": "ai-powered"
}
```

**Expected Response:**
```
Claude: ✅ Preview completed (AI-powered generator)

Preview Output:
─────────────────────────────────────────
# Technical Specification

## Overview
[... AI-generated content ...]

## Architecture
[... detailed technical content ...]
─────────────────────────────────────────

Generation Statistics:
- Input tokens: 1,245
- Output tokens: 3,892
- Total tokens: 5,137
- Estimated cost: $0.026 (at $0.005/1K tokens)

For 100 similar documents:
- Total tokens: ~513,700
- Estimated cost: ~$2.60

Would you like to proceed with batch generation?
```

**What You Learned:**
- Preview provides cost estimates for AI generators
- Plan batch operations based on budget
- Optimize prompts before expensive operations

---

## Task 5: Compare Preview vs Generate

**Scenario:** Understand when preview differs from final generation.

### Side-by-Side Comparison

**Preview:**
```json
{
  "content_config_id": "changelog",
  "context": {"version": "2.0.0"}
}
```

**Response:**
```
Preview Output: [content as string]
No cache check
No file I/O
No metadata updates
```

**Generate:**
```json
{
  "content_config_id": "changelog",
  "context": {"version": "2.0.0"}
}
```

**Response:**
```
✅ Generated: output/changelog-2.0.0.md

Checks cache first
Writes to disk
Updates metadata
Triggers post-generation hooks (if any)
```

**Key Differences:**

| Operation | Preview | Generate |
|-----------|---------|----------|
| Cache check | ❌ | ✅ |
| File creation | ❌ | ✅ |
| Metadata | ❌ | ✅ |
| Hooks/Events | ❌ | ✅ |
| Output location | String return | File path |

**When They're Identical:**
- Template rendering logic
- Context variable substitution
- Content transformation
- Generator execution (same output)

**When They Differ:**
- Generate may return cached result (preview never caches)
- Generate creates persistent files (preview ephemeral)
- Generate updates last_generated timestamps

---

## Task 6: Force Regeneration (Cache Bypass)

**Scenario:** Content is cached, but you need fresh generation.

### Step 1: Check Current Behavior

```
You: Generate content for 'daily-report'
```

**Expected Response:**
```
Claude: ✅ Content generated (from cache)

Output: output/daily-report-2025-10-16.md
Source: Cache (generated 2 hours ago)
```

### Step 2: Force Regeneration

```
You: Regenerate 'daily-report' bypassing cache
```

**What Claude Does:**

Calls `regenerate_content` instead of `generate_content`:

```json
{
  "content_config_id": "daily-report"
}
```

**Expected Response:**
```
Claude: ✅ Content regenerated (fresh generation)

Output: output/daily-report-2025-10-16.md
Source: Fresh generation (cache bypassed)
Template executed: 1.2 seconds
File updated: 2025-10-16 14:23:45
```

**When to Use `regenerate_content`:**
- Data source changed (e.g., database updated)
- Template modified but config unchanged
- Cache suspected to be stale
- Testing template changes
- Debugging generation issues

**When to Use `generate_content`:**
- Normal operations (cache is good)
- Batch operations (performance critical)
- Idempotent workflows

---

## Advanced Patterns

### Pattern 1: Preview-Test-Generate Workflow

**Scenario:** Safe deployment of new templates.

```
Step 1: Preview with test data
  You: Preview new-template with test context

Step 2: Validate output
  [Review preview output]

Step 3: Preview with production data
  You: Preview new-template with production context

Step 4: Generate for real
  You: Generate content using new-template
```

**Benefits:**
- Zero risk of bad output reaching production
- Iterative refinement without cleanup
- Confidence before deployment

---

### Pattern 2: Cost-Aware Batch Generation

**Scenario:** Estimate costs before running expensive AI batch.

```python
# Agent pseudo-code
batch_items = [...]  # 50 items

# Step 1: Preview one representative item
preview_result = preview_generation(batch_items[0])
cost_per_item = preview_result.estimated_cost

# Step 2: Calculate total cost
total_cost = cost_per_item * len(batch_items)

# Step 3: Decide based on budget
if total_cost > budget:
    print(f"Batch would cost ${total_cost:.2f}, exceeds budget")
    # Reduce batch size or optimize prompts
else:
    batch_generate(batch_items)
```

---

### Pattern 3: Context Validation Before Batch

**Scenario:** Validate all context variations before batch generation.

```
You: Preview report-template with these 5 context variations:
1. {"team": "Engineering", "month": "Oct"}
2. {"team": "Product", "month": "Oct"}
3. {"team": "Marketing", "month": "Oct"}
4. {"team": "Sales", "month": "Oct"}
5. {"team": "Support", "month": "Oct"}
```

**What Claude Does:**

Previews all 5 variations, validates:
- All context fields render correctly
- No template errors
- Output format consistent

**Expected Response:**
```
Claude: ✅ All 5 context variations validated

Preview 1 (Engineering): ✅ Valid (2.1 KB)
Preview 2 (Product): ✅ Valid (1.9 KB)
Preview 3 (Marketing): ✅ Valid (2.3 KB)
Preview 4 (Sales): ✅ Valid (2.0 KB)
Preview 5 (Support): ✅ Valid (1.8 KB)

All templates render successfully. Safe to batch generate.

Would you like to proceed with batch_generate?
```

---

## Best Practices

### ✅ Do's

1. **Always Preview New Templates**
   ```
   ✅ Good: Preview → Validate → Generate
   ❌ Bad: Generate → Delete → Fix → Generate
   ```

2. **Preview Edge Cases**
   ```python
   edge_cases = [
       {},                           # Empty context
       {"field": None},              # Null values
       {"list": []},                 # Empty lists
       {"text": "A" * 10000}        # Large values
   ]
   for context in edge_cases:
       preview_generation(config, context)
   ```

3. **Use Preview for Cost Estimation**
   ```
   ✅ Good: Preview → Estimate → Decide → Batch
   ❌ Bad: Batch → Surprise bill
   ```

4. **Preview Before Batch Operations**
   ```
   For batch_size > 5: Preview one item first
   For batch_size > 20: Preview multiple representative items
   ```

---

### ❌ Don'ts

1. **Don't Use Preview for Production**
   ```
   ❌ Bad: preview_generation → save to file manually
   ✅ Good: generate_content (handles everything)
   ```

2. **Don't Assume Preview = Generate**
   ```
   ❌ Bad: Preview looks good → assume generate will match exactly
   ✅ Good: Preview validates logic, but generate is source of truth
   ```

3. **Don't Skip Preview for Complex Templates**
   ```
   ❌ Bad: Complex Jinja2 → generate → debug → cleanup → repeat
   ✅ Good: Complex Jinja2 → preview → fix → preview → generate
   ```

4. **Don't Use regenerate_content by Default**
   ```
   ❌ Bad: Always bypass cache (slow, wasteful)
   ✅ Good: Use generate_content (cache is good), regenerate only when needed
   ```

---

## Common Scenarios

### Scenario 1: New Template Development

**Workflow:**
```
1. Write template skeleton
2. Preview with minimal context → Fix syntax errors
3. Preview with full context → Validate rendering
4. Preview with edge cases → Handle nulls/empties
5. Preview with production data → Final validation
6. Generate for real → Deploy
```

**Time Saved:** 10-15 minutes vs generate→delete→fix cycle

---

### Scenario 2: Template Migration

**Old template (v1)** → **New template (v2)**

```
You: Compare old-template vs new-template using same context

Claude will:
1. Preview with old-template
2. Preview with new-template
3. Show diff of outputs
4. Highlight breaking changes
```

**Expected Response:**
```
Claude: ✅ Template comparison complete

Differences:
+ New section: "Prerequisites" (127 lines)
~ Updated section: "Installation" (formatting changes)
- Removed section: "Legacy API" (deprecated)

Breaking changes: None detected
Safe to migrate: ✅
```

---

### Scenario 3: AI Prompt Optimization

**Problem:** AI generator producing too much content (expensive).

**Solution:** Iterate on prompts using preview.

```
Iteration 1: Preview → 5,000 tokens → Too long
Iteration 2: Add "Keep under 500 words" → Preview → 3,000 tokens → Still long
Iteration 3: Add "Bullet points only" → Preview → 800 tokens → Perfect!

Final cost: $0.004 per item (vs $0.025 original)
Savings: 84% cost reduction
```

---

## Troubleshooting

### Issue: Preview Shows Different Output Than Generate

**Symptoms:**
```
Preview: [Content A]
Generate: [Content B]  (different!)
```

**Possible Causes:**

1. **Cache Staleness**
   - Generate returned cached result
   - Solution: Use `regenerate_content` to bypass cache

2. **Time-Based Context**
   - Template uses `now()` or timestamps
   - Solution: Lock time in context for consistent results

3. **Non-Deterministic Generator**
   - AI generators have randomness
   - Solution: Set temperature=0 or seed for reproducibility

---

### Issue: Preview Takes Too Long

**Problem:** Preview of AI-powered generator takes 30+ seconds.

**Solutions:**

1. **Use Simpler Generator for Testing**
   ```json
   {
     "generator_override": "demonstration"  // Fast, deterministic
   }
   ```

2. **Reduce AI Context Window**
   ```
   Optimize prompt to use fewer input tokens
   ```

3. **Preview with Minimal Context**
   ```
   Test template logic with small data first
   ```

---

### Issue: Preview Fails but Generate Succeeds

**Symptoms:**
```
preview_generation: ❌ Template error
generate_content: ✅ Success
```

**Cause:** Preview and generate use slightly different validation.

**Solution:** This is a bug. Report with details:
- Config ID
- Context used
- Error message from preview
- Generate output

---

## Related Documentation

- **[Tutorial: MCP Integration Deep Dive](../../tutorials/advanced/01-mcp-integration-deep-dive.md)** - Part 2.4 covers preview workflows
- **[How-To: Batch Generate Content](./batch-generate-content.md)** - Use preview before batch operations
- **[How-To: Create Content Conversationally](../configs/create-config-conversationally.md)** - test_config uses preview internally
- **[Reference: MCP Tool Catalog](../../reference/api/mcp/tool-catalog.md)** - Complete preview_generation and regenerate_content reference
- **[E2E Test Suite: Content Generation](../../mcp/E2E_CONTENT_GENERATION.md)** - Test cases for preview and regenerate

---

**You can now safely test templates and validate generation before creating files!**
