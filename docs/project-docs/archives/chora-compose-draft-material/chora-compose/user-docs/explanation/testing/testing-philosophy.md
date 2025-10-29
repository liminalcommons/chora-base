# Testing Philosophy

**Audience:** Developers and contributors
**Purpose:** Understand the testing approach, principles, and philosophy behind chora-compose

---

## Overview

Chora-compose's testing philosophy is built on three core principles:

1. **Validate early** - Catch errors before they propagate
2. **Fail fast** - Surface issues immediately
3. **Preview before execution** - Human review at critical points

This document explains why we test what we test, when to test, and the trade-offs we've made in building a testing strategy for AI-assisted content generation.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [The Test Pyramid for AI Workflows](#the-test-pyramid-for-ai-workflows)
3. [When to Test What](#when-to-test-what)
4. [Trade-offs](#trade-offs)
5. [Future of Testing in AI Workflows](#future-of-testing-in-ai-workflows)

---

## Core Principles

### 1. Validate Early, Fail Fast

**Principle:** Catch errors at the earliest possible stage

**Why:** Errors become exponentially more expensive to fix the later they're discovered.

```
Cost of Fixing Errors by Stage:

Config Creation   │ $1     │ Fix JSON, immediate feedback
Runtime Testing   │ $10    │ Debug generation, check dependencies
Post-Generation   │ $100   │ Review output, regenerate
Production        │ $1000  │ User impact, rollback, reputation
```

**Implementation:**

```python
# Layer 1: Schema validation (milliseconds)
validate_json_schema(config)  # Catch malformed configs

# Layer 2: Pydantic model validation (milliseconds)
ContentConfig(**config_data)  # Catch type errors

# Layer 3: Dry-run generation (seconds)
test_config(draft_id, dry_run=True)  # Catch runtime errors

# Layer 4: Preview validation (human review)
review_preview_content()  # Catch quality issues
```

**Result:** Most errors caught in Layer 1-2, before any generation occurs.

### 2. Fail Fast

**Principle:** Surface errors immediately, don't continue with invalid state

**Why:** Continuing with errors leads to cascading failures and harder debugging.

**Example:**

```python
# ✓ Good: Fail fast
def generate_artifact(config_path: Path) -> Artifact:
    # Validate first
    if not validate_config(config_path):
        raise ConfigValidationError("Invalid config")

    # Only proceed if valid
    return compose(config_path)


# ✗ Bad: Continue despite errors
def generate_artifact(config_path: Path) -> Artifact:
    try:
        validate_config(config_path)
    except Exception as e:
        print(f"Warning: {e}")  # Log but continue

    # Proceeds even if validation failed
    return compose(config_path)  # May fail with cryptic error
```

**Benefits:**
- Clear error messages at the source
- Easier debugging (error close to cause)
- No partial/corrupt state

### 3. Preview Before Execution

**Principle:** Humans review critical outputs before commit/deploy

**Why:** AI-generated content requires human judgment for quality, appropriateness, and accuracy.

**Where we preview:**

```
Config Creation   → Preview template structure
Draft Testing     → Preview generated output (first 10K chars)
Artifact Assembly → Preview assembled multi-part artifacts
Deployment        → Final review before publishing
```

**Example workflow:**

```python
# 1. Create draft
draft = create_draft(config_data)

# 2. Test with preview
result = test_config(draft.draft_id)
print(result["preview_content"])  # Human reviews

# 3. Human decision point
if input("Looks good? (y/n): ") == "y":
    save_config(draft.draft_id, "configs/content/final.json")
```

---

## The Test Pyramid for AI Workflows

Traditional test pyramid doesn't map cleanly to AI-assisted content generation. Here's our adapted pyramid:

```
                    ▲
                   ╱│╲
                  ╱ │ ╲
                 ╱  │  ╲  ← Manual Review (slowest, few)
                ╱───│───╲
               ╱    │    ╲
              ╱     │     ╲  ← Integration Tests (medium)
             ╱──────│──────╲
            ╱       │       ╲
           ╱        │        ╲  ← Validation Tests (fast, many)
          ╱─────────│─────────╲
         ╱          │          ╲
        ╱___________│___________╲  ← Schema Tests (fastest, most)

```

### Layer 1: Schema Tests (Fast, Many)

**What:** JSON schema validation
**Speed:** < 10ms per config
**Coverage:** 100% of configs
**Automation:** Fully automated (CI/CD)

**Example:**
```python
def test_schema_compliance():
    """Every config must pass schema validation."""
    for config_path in Path("configs/content").glob("*.json"):
        validate_json_schema(config_path)  # Fast, deterministic
```

**When to run:**
- Pre-commit hooks
- PR validation
- Continuous integration
- Manual config creation

### Layer 2: Validation Tests (Fast, Many)

**What:** Pydantic model validation, type checking
**Speed:** < 100ms per config
**Coverage:** 100% of configs
**Automation:** Fully automated (CI/CD)

**Example:**
```python
def test_pydantic_model():
    """Config must parse into Pydantic model."""
    config_data = load_json("config.json")
    ContentConfig(**config_data)  # Type validation
```

**When to run:**
- Same as schema tests
- Additional: Before saving configs

### Layer 3: Integration Tests (Medium Speed, Moderate Coverage)

**What:** Dry-run generation, dependency checks
**Speed:** 1-10 seconds per config
**Coverage:** Critical configs + smoke tests
**Automation:** Automated with selective coverage

**Example:**
```python
def test_generation_dry_run():
    """Critical configs must generate without errors."""
    critical_configs = [
        "api-docs",
        "user-guide",
        "release-notes"
    ]

    for config_id in critical_configs:
        draft = create_draft(config_id)
        result = test_config(draft.draft_id, dry_run=True)
        assert result["success"] is True
```

**When to run:**
- PR validation (critical configs)
- Pre-deployment (all configs)
- Scheduled (nightly regression)

### Layer 4: Manual Review (Slow, Selective)

**What:** Human review of generated content
**Speed:** Minutes to hours
**Coverage:** High-value or user-facing content
**Automation:** Not automated

**Example workflow:**
```python
def review_workflow(config_id: str):
    """Generate and prompt for human review."""
    draft = create_draft(config_id)
    result = test_config(draft.draft_id)

    print("Preview (first 500 chars):")
    print(result["preview_content"][:500])

    approved = input("\nApprove for deployment? (y/n): ")

    if approved == "y":
        deploy(config_id)
    else:
        print("Review rejected. Update config and retry.")
```

**When to use:**
- New generator types
- Critical documentation
- User-facing content
- First-time configs

---

## When to Test What

### Before Committing Configs

**What to test:**
- ✅ Schema validation
- ✅ Pydantic model parsing

**Why:** Prevent invalid configs from entering version control

**How:**
```bash
# Pre-commit hook
poetry run chora-compose validate configs/new-config.json
```

### On Pull Requests

**What to test:**
- ✅ All schema validation
- ✅ Smoke test critical configs (dry-run)
- ✅ Lint config formatting

**Why:** Ensure PR doesn't break existing functionality

**How:**
```yaml
# .github/workflows/pr-validation.yml
- name: Validate all configs
  run: poetry run chora-compose validate configs/

- name: Smoke test critical configs
  run: python scripts/smoke_test_configs.py
```

### Before Deployment

**What to test:**
- ✅ Full validation (all layers)
- ✅ Integration tests (all configs)
- ✅ Preview generation (select high-value content)
- ✅ Human review (critical content)

**Why:** Prevent broken or low-quality content from reaching users

**How:**
```python
def pre_deployment_checks():
    """Run all checks before deployment."""
    # 1. Validate all configs
    validate_all_configs()

    # 2. Test all configs (dry-run)
    test_all_configs()

    # 3. Generate previews for human review
    preview_critical_content()

    # 4. Deploy only if all pass
    deploy_if_approved()
```

### In Production

**What to monitor:**
- ✅ Generation success rate
- ✅ Error types and frequency
- ✅ Performance metrics (duration)
- ✅ User feedback

**Why:** Detect issues in real usage, inform improvements

**How:**
```python
# Monitor telemetry events
def monitor_production():
    events = read_telemetry_events()

    # Calculate metrics
    total_generations = len(events)
    failures = [e for e in events if e["status"] == "failed"]
    failure_rate = len(failures) / total_generations

    if failure_rate > 0.05:  # > 5% failure
        alert_team(f"High failure rate: {failure_rate:.2%}")
```

---

## Trade-offs

### Speed vs Completeness

**Trade-off:** Fast validation vs comprehensive testing

**Decision:** Use layered approach

- **Layer 1-2:** Fast, complete coverage (all configs)
- **Layer 3:** Medium speed, selective coverage (critical configs)
- **Layer 4:** Slow, manual coverage (high-value content)

**Why:** Different failure modes have different costs

```
Invalid schema      → Cheap to fix, fast to detect (Layer 1)
Runtime errors      → Medium cost, medium speed (Layer 3)
Low quality output  → Expensive, requires human (Layer 4)
```

### Automation vs Human Judgment

**Trade-off:** Fully automated testing vs human review

**Decision:** Automate structure, humans judge quality

**What we automate:**
- Schema validation (100%)
- Type checking (100%)
- Syntax validation (100%)
- Dependency checks (100%)

**What requires humans:**
- Content quality
- Appropriateness
- Accuracy of information
- Tone and style

**Why:** AI can validate structure, humans validate meaning.

**Example:**
```python
# ✓ Automated: Check structure
def validate_api_docs_structure(content: str) -> bool:
    """Validate API docs have required sections."""
    required = ["Parameters", "Returns", "Example", "Errors"]
    return all(section in content for section in required)

# ✗ Can't automate: Check quality
def validate_api_docs_quality(content: str) -> bool:
    """Check if API docs are high quality."""
    # How do you programmatically determine:
    # - Are examples clear and helpful?
    # - Is explanation sufficient?
    # - Are edge cases covered?
    # → Requires human expertise
```

### Coverage vs Cost

**Trade-off:** Test everything vs test strategically

**Decision:** 100% coverage for fast tests, selective for slow tests

**Coverage strategy:**

```
Schema validation:       100% of configs (fast)
Model validation:        100% of configs (fast)
Dry-run generation:      20% of configs (medium, critical ones)
Manual review:           5% of content (slow, high-value)
```

**Cost calculation:**

```
1000 configs in system

Schema validation:       1000 × 10ms    = 10 seconds
Model validation:        1000 × 100ms   = 100 seconds
Dry-run tests:           200 × 5s       = 1000 seconds (16 min)
Manual review:           50 × 5min      = 250 minutes (4 hours)

Total automated: ~18 minutes
Total with review: ~4.3 hours
```

**Why:** Optimize for signal-to-noise ratio

---

## Future of Testing in AI Workflows

### LLM-as-Judge Pattern

**Concept:** Use AI to validate AI-generated content

**Promise:**
- Automated quality checks
- Scalable content review
- Consistency in evaluation

**Challenges:**
- AI judging AI (circular problem)
- Hallucination risk in validation
- Cost (API calls for every validation)

**Example:**
```python
async def llm_validate_content(content: str) -> ValidationResult:
    """Use LLM to validate generated content."""
    prompt = f"""
    Review this generated API documentation for quality:

    {content}

    Evaluate:
    1. Are examples clear and correct?
    2. Is explanation sufficient?
    3. Are edge cases covered?
    4. Is terminology consistent?

    Return JSON: {{"passed": bool, "issues": [...]}}
    """

    response = await anthropic.complete(prompt)
    return ValidationResult(**response)
```

**When to use:**
- Not yet (experimental)
- Consider for non-critical validation
- Always with human oversight

### Differential Testing

**Concept:** Compare outputs across generator versions

**Use case:** Detect regressions when updating generators

**Example:**
```python
def differential_test(config: ContentConfig):
    """Test new generator against baseline."""
    # Generate with current version
    current_output = generator_v1.generate(config, context)

    # Generate with new version
    new_output = generator_v2.generate(config, context)

    # Compare
    similarity = calculate_similarity(current_output, new_output)

    if similarity < 0.8:  # 80% similarity threshold
        flag_for_review(config, current_output, new_output)
```

**Benefits:**
- Catch unintended changes
- Quantify impact of updates
- Inform rollback decisions

### Property-Based Testing

**Concept:** Test properties that should always hold

**Example:**
```python
from hypothesis import given, strategies as st

@given(st.text(min_size=1))
def test_content_id_roundtrip(content_id: str):
    """Content ID should survive save/load cycle."""
    config = create_config(content_id=content_id)
    saved_path = save_config(config)
    loaded_config = load_config(saved_path)

    assert loaded_config.content_id == content_id
```

**Properties for chora-compose:**
- Config serialization is idempotent
- Generation with same context is deterministic (for non-AI generators)
- All generated content passes format validation

---

## Conclusion

Chora-compose's testing philosophy prioritizes **early validation**, **fast feedback**, and **human judgment at critical points**. We've balanced speed vs completeness, automation vs human review, and coverage vs cost to create a pragmatic testing strategy for AI-assisted content generation.

**Key takeaways:**

1. **Test early** - Catch most errors in fast schema/model validation
2. **Fail fast** - Don't proceed with invalid state
3. **Layer testing** - Fast tests for all configs, slow tests for critical ones
4. **Humans judge quality** - Automate structure, humans validate meaning
5. **Monitor production** - Real-world usage informs improvements

**Further reading:**

- [Test Configs Before Deployment](../../how-to/testing/test-configs-before-deployment.md) - Practical testing guide
- [Validate Generated Content](../../how-to/testing/validate-generated-content.md) - Post-generation validation
- [Testing and Validation Approaches](../workflows/testing-validation-approaches.md) - Workflow-level testing
- [Integrate with GitHub Actions](../../how-to/ci-cd/integrate-with-github-actions.md) - CI/CD automation
