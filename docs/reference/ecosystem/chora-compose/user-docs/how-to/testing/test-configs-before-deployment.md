# How to Test Configs Before Deployment

**Goal:** Validate configurations and preview generated content before deploying to production

**When to use this:** Before committing configs to version control or deploying to production environments

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Pre-Deployment Testing Workflow](#pre-deployment-testing-workflow)
4. [Using test_config MCP Tool](#using-test_config-mcp-tool)
5. [Validation Strategies](#validation-strategies)
6. [Common Errors and Fixes](#common-errors-and-fixes)
7. [Automation with Scripts](#automation-with-scripts)
8. [CI/CD Integration](#cicd-integration)

---

## Overview

Testing configs before deployment prevents issues like:

- **Schema validation failures** in production
- **Template rendering errors** that halt generation
- **Missing dependencies** (API keys, source files)
- **Unexpected output** from generation
- **Performance issues** with large contexts

Chora-compose provides a three-layer validation approach:

1. **Schema validation** - Checks JSON structure
2. **Runtime validation** - Tests dependencies and execution
3. **Preview validation** - Reviews generated output

---

## Quick Start

### Basic Testing Workflow

```bash
# 1. Validate schema
poetry run chora-compose validate configs/content/my-config.json

# 2. Create draft for testing
poetry run chora-compose draft-config content my-config.json

# 3. Test generation (dry-run, no persistence)
poetry run chora-compose test-config <draft-id>

# 4. Review output, fix issues, repeat
```

**Time to first test:** ~2 minutes

---

## Pre-Deployment Testing Workflow

### Full Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Schema Validation                                        │
│    ├─ JSON structure valid?                                 │
│    ├─ Required fields present?                              │
│    └─ Field types correct?                                  │
└────────────────────┬────────────────────────────────────────┘
                     │ Pass
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Draft Creation                                           │
│    ├─ Create ephemeral draft                                │
│    ├─ Validate Pydantic model                               │
│    └─ Store in temporary storage                            │
└────────────────────┬────────────────────────────────────────┘
                     │ Success
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Runtime Testing                                          │
│    ├─ Check generator dependencies                          │
│    ├─ Resolve template paths                                │
│    ├─ Validate context data                                 │
│    └─ Test generation (dry-run)                             │
└────────────────────┬────────────────────────────────────────┘
                     │ Pass
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Output Preview                                           │
│    ├─ Review generated content                              │
│    ├─ Verify quality                                        │
│    └─ Check for issues                                      │
└────────────────────┬────────────────────────────────────────┘
                     │ Approved
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Save to Filesystem                                       │
│    └─ Persist to configs/                                   │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Instructions

#### Step 1: Schema Validation

Validate JSON structure against schema:

```bash
# Validate a single config
poetry run chora-compose validate configs/content/api-docs.json

# Validate all configs in directory
poetry run chora-compose validate configs/content/
```

**What it checks:**
- JSON is well-formed
- Required fields present (`content_id`, `format`, `generation`)
- Field types match schema (string, object, array)
- Enum values are valid (e.g., `format` must be "markdown", "json", etc.)

**Example output (success):**
```
✓ configs/content/api-docs.json is valid
  Schema: content/v3.1
  Content ID: api-docs
  Format: markdown
  Generator: jinja2
```

**Example output (failure):**
```
✗ configs/content/api-docs.json failed validation
  Error: 'content_id' is a required property
  Line: 1
  Schema: content/v3.1
```

#### Step 2: Create Draft

Create a temporary draft for testing:

**Using CLI:**
```bash
# Create draft from file
poetry run chora-compose draft-config content configs/content/api-docs.json

# Output:
# Draft created: draft_20251021_143022_abc123
# Preview path: /var/ephemeral/drafts/draft_20251021_143022_abc123.json
```

**Using MCP (via Claude Code or other MCP client):**
```python
# Via MCP tool
result = await mcp_client.call_tool("choracompose:draft_config", {
    "config_type": "content",
    "config_data": {
        "content_id": "api-docs",
        "format": "markdown",
        "generation": {
            "patterns": [{
                "type": "jinja2",
                "template_path": "templates/api-docs.md.j2"
            }]
        }
    },
    "description": "API documentation config"
})

draft_id = result["draft_id"]
```

**What it does:**
- Validates against JSON schema
- Validates against Pydantic models
- Stores in ephemeral storage (30-day retention)
- Returns draft ID for testing

#### Step 3: Test Generation (Dry-Run)

Test generation without persisting output:

**Using test_config tool:**
```bash
# Basic test
poetry run chora-compose test-config draft_20251021_143022_abc123

# Test with context
poetry run chora-compose test-config draft_20251021_143022_abc123 \
    --context '{"version": "1.0.0", "date": "2025-10-21"}'
```

**Using MCP:**
```python
result = await mcp_client.call_tool("choracompose:test_config", {
    "draft_id": "draft_20251021_143022_abc123",
    "context": {
        "version": "1.0.0",
        "date": "2025-10-21"
    },
    "dry_run": True  # Don't persist output
})

print(result["preview_content"])
print(f"Generated {result['content_length']} characters")
print(f"Generator used: {result['generator_used']}")
```

**What it checks:**
- Generator exists and is accessible
- Template files can be resolved
- Context data is valid
- Generation completes without errors
- Output meets expectations

**Example output:**
```json
{
  "success": true,
  "draft_id": "draft_20251021_143022_abc123",
  "preview_content": "# API Documentation\n\nVersion: 1.0.0\nDate: 2025-10-21\n\n...",
  "content_length": 1250,
  "generator_used": "jinja2",
  "validation_issues": [],
  "duration_ms": 45
}
```

#### Step 4: Review and Iterate

Review the preview and fix issues:

**Common review points:**
- Content quality and accuracy
- Formatting and structure
- Variable substitution correct
- No missing placeholders (e.g., `{{ undefined_var }}`)
- Appropriate length

**If issues found:**
1. Update config JSON
2. Create new draft (`draft-config` again)
3. Re-test (`test-config`)
4. Repeat until satisfied

#### Step 5: Save to Filesystem

Once validated, save to permanent location:

**Using save_config tool:**
```bash
# Save draft to filesystem
poetry run chora-compose save-config draft_20251021_143022_abc123 \
    configs/content/api-docs.json
```

**Using MCP:**
```python
result = await mcp_client.call_tool("choracompose:save_config", {
    "draft_id": "draft_20251021_143022_abc123",
    "target_path": "configs/content/api-docs.json",
    "overwrite": False  # Fail if file exists (safety)
})

print(f"Saved to: {result['saved_path']}")
```

**What it does:**
- Validates draft still exists
- Writes config to specified path
- Creates directories if needed
- Optionally overwrites existing file

---

## Using test_config MCP Tool

### Tool Signature

```python
async def test_config(
    draft_id: str,
    context: dict[str, Any] | str | None = None,
    dry_run: bool = True
) -> TestConfigResult
```

**Parameters:**

- **draft_id** (required): Draft configuration ID from `draft_config`
- **context** (optional): Variables for template rendering
  - Can be dict or JSON string
  - Used by generators (Jinja2, Template Fill)
- **dry_run** (optional): Don't persist output (default: True)
  - Always use `True` for testing
  - Set to `False` only for actual generation

**Returns:**

```typescript
{
  success: boolean,
  draft_id: string,
  preview_content: string,        // First 10,000 chars
  content_length: number,          // Total length
  generator_used: string,          // "jinja2", "template_fill", etc.
  validation_issues: string[],     // Warnings or issues
  estimated_cost: number | null,   // For AI generators (future)
  duration_ms: number              // Generation time
}
```

### Usage Examples

#### Example 1: Test Simple Jinja2 Config

```python
# Create draft
draft_result = await mcp_client.call_tool("choracompose:draft_config", {
    "config_type": "content",
    "config_data": {
        "content_id": "weekly-report",
        "format": "markdown",
        "generation": {
            "patterns": [{
                "type": "jinja2",
                "template_string": "# Weekly Report\n\nDate: {{ date }}\n\n## Summary\n{{ summary }}"
            }]
        }
    }
})

draft_id = draft_result["draft_id"]

# Test with context
test_result = await mcp_client.call_tool("choracompose:test_config", {
    "draft_id": draft_id,
    "context": {
        "date": "2025-10-21",
        "summary": "All systems operational. 10 new features deployed."
    }
})

print(test_result["preview_content"])
# Output:
# # Weekly Report
#
# Date: 2025-10-21
#
# ## Summary
# All systems operational. 10 new features deployed.
```

#### Example 2: Test BDD Scenario Generator

```python
# Create BDD config draft
draft_result = await mcp_client.call_tool("choracompose:draft_config", {
    "config_type": "content",
    "config_data": {
        "content_id": "user-login-tests",
        "format": "gherkin",
        "generation": {
            "patterns": [{
                "type": "bdd_scenario",
                "bdd_config": {
                    "feature": {
                        "name": "User Login",
                        "description": "As a user, I want to log in"
                    },
                    "scenarios": [
                        {
                            "name": "Successful login",
                            "steps": [
                                {"type": "Given", "text": "I am on the login page"},
                                {"type": "When", "text": "I enter valid credentials"},
                                {"type": "Then", "text": "I should see the dashboard"}
                            ]
                        }
                    ]
                }
            }]
        }
    }
})

# Test (BDD doesn't need context)
test_result = await mcp_client.call_tool("choracompose:test_config", {
    "draft_id": draft_result["draft_id"]
})

print(test_result["preview_content"])
# Output:
# Feature: User Login
#   As a user, I want to log in
#
#   Scenario: Successful login
#     Given I am on the login page
#     When I enter valid credentials
#     Then I should see the dashboard
```

#### Example 3: Test with Missing Dependencies

```python
# Config references template file that doesn't exist
draft_result = await mcp_client.call_tool("choracompose:draft_config", {
    "config_type": "content",
    "config_data": {
        "content_id": "missing-template-test",
        "format": "markdown",
        "generation": {
            "patterns": [{
                "type": "jinja2",
                "template_path": "templates/nonexistent.md.j2"  # File doesn't exist
            }]
        }
    }
})

# Test will fail gracefully
test_result = await mcp_client.call_tool("choracompose:test_config", {
    "draft_id": draft_result["draft_id"]
})

print(test_result)
# Output:
# {
#   "success": False,
#   "error": {
#     "code": "test_failed",
#     "message": "Template file not found: templates/nonexistent.md.j2",
#     "details": {"draft_id": "...", "duration_ms": 12}
#   }
# }
```

---

## Validation Strategies

### Layer 1: Schema Validation

**When:** Always run first, before any other validation

**Command:**
```bash
poetry run chora-compose validate configs/content/my-config.json
```

**What it catches:**
- Malformed JSON
- Missing required fields
- Wrong field types
- Invalid enum values

**Fast:** < 10ms per config

### Layer 2: Runtime Validation

**When:** After schema validation passes

**Method:** Create draft → test config

**What it catches:**
- Missing template files
- Missing API keys (for AI generators)
- Invalid generator type
- Context variable mismatches

**Medium:** 50-200ms depending on generator

### Layer 3: Preview Validation (Human Review)

**When:** After runtime validation passes

**Method:** Review `preview_content` from test

**What it catches:**
- Incorrect output
- Quality issues
- Logic errors in templates
- Unexpected formatting

**Slowest:** Human review time

### Choosing the Right Strategy

**Quick validation (CI/CD):**
```bash
# Schema only - fast, catches most issues
poetry run chora-compose validate configs/
```

**Pre-commit validation:**
```bash
# Schema + runtime test
poetry run chora-compose validate configs/
poetry run chora-compose test-all-configs  # Custom script
```

**Pre-deployment validation:**
```bash
# Full workflow with human review
poetry run chora-compose validate configs/
poetry run chora-compose test-with-preview configs/
# Manual review of preview outputs
```

---

## Common Errors and Fixes

### Error: Schema Validation Failed

**Symptom:**
```
✗ configs/content/api-docs.json failed validation
  Error: 'generation' is a required property
```

**Cause:** Missing required field in config JSON

**Fix:**
```json
{
  "content_id": "api-docs",
  "format": "markdown",
  "generation": {  // ← Add this required field
    "patterns": [{
      "type": "jinja2",
      "template_path": "templates/api-docs.md.j2"
    }]
  }
}
```

### Error: Template Not Found

**Symptom:**
```json
{
  "success": false,
  "error": {
    "code": "test_failed",
    "message": "Template file not found: templates/api-docs.md.j2"
  }
}
```

**Cause:** Template path in config doesn't exist

**Fix:**
1. Create the template file at specified path
2. Or update config to point to existing template

```bash
# Create missing template
mkdir -p templates
touch templates/api-docs.md.j2

# Or update config
# "template_path": "templates/existing-template.md.j2"
```

### Error: Generator Not Found

**Symptom:**
```json
{
  "success": false,
  "error": {
    "code": "test_failed",
    "message": "Generator not found: custom_generator"
  }
}
```

**Cause:** Generator type doesn't exist or isn't registered

**Fix:**
```bash
# List available generators
poetry run chora-compose list-generators

# Use a valid generator type
# Valid: jinja2, template_fill, bdd_scenario, code_generation, demonstration
```

**In config:**
```json
{
  "generation": {
    "patterns": [{
      "type": "jinja2"  // ← Use valid generator
    }]
  }
}
```

### Error: Missing Context Variable

**Symptom:**
```
# Preview shows: {{ undefined_variable }}
```

**Cause:** Template references variable not provided in context

**Fix:**
```python
# Provide missing variable in test context
test_result = await mcp_client.call_tool("choracompose:test_config", {
    "draft_id": draft_id,
    "context": {
        "undefined_variable": "actual_value"  // ← Add missing var
    }
})
```

### Error: Draft Not Found

**Symptom:**
```json
{
  "success": false,
  "error": {
    "code": "draft_not_found",
    "message": "Draft not found: draft_20251021_old"
  }
}
```

**Cause:** Draft expired (30-day retention) or wrong ID

**Fix:**
```bash
# Create a new draft
poetry run chora-compose draft-config content configs/content/my-config.json

# Use the new draft_id
```

---

## Automation with Scripts

### Batch Testing Script

Create `scripts/test_all_configs.sh`:

```bash
#!/bin/bash
#
# Test all content configs before deployment
#

set -e  # Exit on error

CONFIGS_DIR="configs/content"
FAILED=0

echo "=== Testing all configs in $CONFIGS_DIR ==="
echo

for config in "$CONFIGS_DIR"/*.json; do
    echo "Testing: $config"

    # 1. Schema validation
    if ! poetry run chora-compose validate "$config"; then
        echo "  ✗ Schema validation failed"
        FAILED=$((FAILED + 1))
        continue
    fi

    # 2. Create draft
    DRAFT_OUTPUT=$(poetry run chora-compose draft-config content "$config" 2>&1)
    DRAFT_ID=$(echo "$DRAFT_OUTPUT" | grep "Draft created:" | awk '{print $3}')

    if [ -z "$DRAFT_ID" ]; then
        echo "  ✗ Draft creation failed"
        FAILED=$((FAILED + 1))
        continue
    fi

    # 3. Test config
    if ! poetry run chora-compose test-config "$DRAFT_ID" > /dev/null 2>&1; then
        echo "  ✗ Test failed"
        FAILED=$((FAILED + 1))
        continue
    fi

    echo "  ✓ All checks passed"
done

echo
echo "=== Test Summary ==="
if [ $FAILED -eq 0 ]; then
    echo "✓ All configs passed"
    exit 0
else
    echo "✗ $FAILED config(s) failed"
    exit 1
fi
```

**Usage:**
```bash
chmod +x scripts/test_all_configs.sh
./scripts/test_all_configs.sh
```

### Python Testing Script

Create `scripts/test_configs.py`:

```python
#!/usr/bin/env python3
"""
Test all configs in configs/content/
"""

import json
import subprocess
import sys
from pathlib import Path


def test_config(config_path: Path) -> tuple[bool, str]:
    """
    Test a single config.

    Returns:
        (success, message) tuple
    """
    # 1. Schema validation
    result = subprocess.run(
        ["poetry", "run", "chora-compose", "validate", str(config_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return False, f"Schema validation failed: {result.stderr}"

    # 2. Create draft
    result = subprocess.run(
        ["poetry", "run", "chora-compose", "draft-config", "content", str(config_path)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return False, f"Draft creation failed: {result.stderr}"

    # Extract draft ID
    for line in result.stdout.split("\n"):
        if "Draft created:" in line:
            draft_id = line.split()[-1]
            break
    else:
        return False, "Could not find draft ID in output"

    # 3. Test config
    result = subprocess.run(
        ["poetry", "run", "chora-compose", "test-config", draft_id],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return False, f"Test failed: {result.stderr}"

    return True, "All checks passed"


def main():
    """Test all configs."""
    configs_dir = Path("configs/content")
    configs = list(configs_dir.glob("*.json"))

    print(f"=== Testing {len(configs)} configs ===\n")

    failed = 0
    for config in configs:
        print(f"Testing: {config}")
        success, message = test_config(config)

        if success:
            print(f"  ✓ {message}")
        else:
            print(f"  ✗ {message}")
            failed += 1

    print(f"\n=== Test Summary ===")
    if failed == 0:
        print("✓ All configs passed")
        return 0
    else:
        print(f"✗ {failed} config(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Usage:**
```bash
chmod +x scripts/test_configs.py
python scripts/test_configs.py
```

---

## CI/CD Integration

### GitHub Actions Workflow

Add to `.github/workflows/test-configs.yml`:

```yaml
name: Test Configs

on:
  pull_request:
    paths:
      - 'configs/**/*.json'
      - 'templates/**/*'
  push:
    branches:
      - main

jobs:
  test-configs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Install dependencies
        run: poetry install

      - name: Validate all configs (schema)
        run: poetry run chora-compose validate configs/

      - name: Test all configs (runtime)
        run: python scripts/test_configs.py

      - name: Report results
        if: failure()
        run: echo "Config testing failed. Review errors above."
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
#
# Pre-commit hook: Test changed configs
#

# Get changed config files
CHANGED_CONFIGS=$(git diff --cached --name-only --diff-filter=ACM | grep 'configs/.*\.json$')

if [ -z "$CHANGED_CONFIGS" ]; then
    echo "No config changes detected, skipping tests"
    exit 0
fi

echo "Testing changed configs..."

for config in $CHANGED_CONFIGS; do
    echo "  Validating: $config"

    if ! poetry run chora-compose validate "$config"; then
        echo "  ✗ Validation failed for $config"
        echo "  Fix errors before committing"
        exit 1
    fi
done

echo "✓ All changed configs passed validation"
exit 0
```

**Install:**
```bash
chmod +x .git/hooks/pre-commit
```

---

## Best Practices

### 1. Always Validate Before Testing

```bash
# ✓ Good: Validate first
poetry run chora-compose validate config.json && \
poetry run chora-compose test-config <draft-id>

# ✗ Bad: Skip validation
poetry run chora-compose test-config <draft-id>
```

### 2. Use Meaningful Draft Descriptions

```python
# ✓ Good: Descriptive
await mcp_client.call_tool("choracompose:draft_config", {
    "config_type": "content",
    "config_data": {...},
    "description": "API docs config for v2.0 release"
})

# ✗ Bad: No description
await mcp_client.call_tool("choracompose:draft_config", {
    "config_type": "content",
    "config_data": {...}
})
```

### 3. Test with Realistic Context

```python
# ✓ Good: Realistic test data
context = {
    "version": "2.0.0",
    "date": "2025-10-21",
    "features": ["feature1", "feature2"]
}

# ✗ Bad: Minimal/fake data
context = {"version": "test"}
```

### 4. Automate Repetitive Testing

```bash
# ✓ Good: Script for regression testing
./scripts/test_all_configs.sh

# ✗ Bad: Manual testing every time
poetry run chora-compose test-config draft1
poetry run chora-compose test-config draft2
# ... (tedious and error-prone)
```

---

## Related Documentation

- [Validate Configs](../configs/validate-configs.md) - Detailed validation guide
- [Create Content Configs](../configs/create-content-configs.md) - Config creation
- [Validate Generated Content](validate-generated-content.md) - Post-generation validation
- [Testing Philosophy](../../explanation/testing/testing-philosophy.md) - Testing approach
- [Integrate with GitHub Actions](../ci-cd/integrate-with-github-actions.md) - CI/CD setup
