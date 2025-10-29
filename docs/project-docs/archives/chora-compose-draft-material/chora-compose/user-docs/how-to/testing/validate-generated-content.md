# How to Validate Generated Content

**Goal:** Verify that generated content meets quality, structure, and business rule requirements

**When to use this:** After content generation, before publishing or deploying artifacts

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Validation Approaches](#validation-approaches)
4. [Schema Validation](#schema-validation)
5. [Business Rule Validation](#business-rule-validation)
6. [Automated Testing](#automated-testing)
7. [Quality Gates](#quality-gates)
8. [Common Validation Scenarios](#common-validation-scenarios)

---

## Overview

Content validation ensures generated output is:

- **Structurally correct** - Valid format (Markdown, JSON, Gherkin, etc.)
- **Complete** - All required sections present
- **Accurate** - Data substitutions correct
- **Consistent** - Follows style and conventions
- **Business-compliant** - Meets organizational rules

### Validation vs Testing

| Aspect | Config Testing | Content Validation |
|--------|----------------|-------------------|
| **When** | Before generation | After generation |
| **What** | Config structure, dependencies | Generated output quality |
| **Tool** | `test_config`, schema validators | Custom validators, parsers |
| **Scope** | Configuration correctness | Content correctness |

---

## Quick Start

### Basic Validation Workflow

```python
# 1. Generate content
from chora_compose.generators.registry import GeneratorRegistry
from chora_compose.core.models import ContentConfig

config = ContentConfig(...)
generator = GeneratorRegistry().get("jinja2")
content = generator.generate(config, context={})

# 2. Validate structure
assert content is not None
assert len(content) > 0

# 3. Validate format-specific requirements
if config.format == "markdown":
    assert content.startswith("#")  # Has heading
    assert "##" in content  # Has subsections

# 4. Validate business rules
assert "CONFIDENTIAL" not in content  # No sensitive data
assert len(content) < 50000  # Within size limit
```

---

## Validation Approaches

### 1. Structure Validation

**Purpose:** Verify format correctness

**Methods:**
- Parse with format-specific parser (JSON, YAML, Gherkin)
- Check for required elements (headings, sections)
- Validate syntax correctness

**Example (Markdown):**
```python
def validate_markdown_structure(content: str) -> list[str]:
    """Validate Markdown structure."""
    issues = []

    # Must have at least one heading
    if not content.strip().startswith("#"):
        issues.append("Missing top-level heading")

    # Check for common Markdown errors
    if "```" in content:
        code_blocks = content.count("```")
        if code_blocks % 2 != 0:
            issues.append("Unclosed code block")

    # Check for broken links
    import re
    links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    for text, url in links:
        if not url.strip():
            issues.append(f"Empty link URL: [{text}]()")

    return issues
```

**Example (JSON):**
```python
import json

def validate_json_structure(content: str) -> list[str]:
    """Validate JSON structure."""
    issues = []

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        issues.append(f"Invalid JSON: {e}")
        return issues

    # Check for required keys (example)
    required_keys = ["version", "data"]
    for key in required_keys:
        if key not in data:
            issues.append(f"Missing required key: {key}")

    return issues
```

**Example (Gherkin/BDD):**
```python
def validate_gherkin_structure(content: str) -> list[str]:
    """Validate Gherkin/BDD scenario structure."""
    issues = []

    # Must start with Feature
    if not content.strip().startswith("Feature:"):
        issues.append("Missing 'Feature:' declaration")

    # Check for scenario structure
    if "Scenario:" not in content:
        issues.append("Missing 'Scenario:' declaration")

    # Check for steps
    required_steps = ["Given", "When", "Then"]
    for step in required_steps:
        if step not in content:
            issues.append(f"Missing '{step}' step")

    return issues
```

### 2. Completeness Validation

**Purpose:** Ensure all required content is present

**Methods:**
- Check for required sections
- Verify minimum content length
- Ensure no placeholder variables remain

**Example:**
```python
def validate_completeness(content: str, config: ContentConfig) -> list[str]:
    """Validate content completeness."""
    issues = []

    # Check for unexpanded variables
    import re
    placeholders = re.findall(r'\{\{([^}]+)\}\}', content)
    if placeholders:
        issues.append(f"Unexpanded variables: {', '.join(placeholders)}")

    # Check minimum length
    min_length = 100  # Example threshold
    if len(content.strip()) < min_length:
        issues.append(f"Content too short: {len(content)} < {min_length} chars")

    # Check for required keywords (example for API docs)
    if config.content_id.startswith("api-"):
        required_keywords = ["Parameters", "Returns", "Example"]
        for keyword in required_keywords:
            if keyword not in content:
                issues.append(f"Missing required section: {keyword}")

    return issues
```

### 3. Quality Validation

**Purpose:** Check content quality and readability

**Methods:**
- Grammar and spelling (optional, using external tools)
- Readability metrics
- Code example validation

**Example:**
```python
def validate_quality(content: str) -> list[str]:
    """Validate content quality."""
    issues = []

    # Check for very long lines (readability)
    max_line_length = 120
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        if len(line) > max_line_length and not line.strip().startswith("|"):
            issues.append(f"Line {i} too long: {len(line)} > {max_line_length} chars")

    # Check for code blocks (should have language specifier)
    import re
    code_blocks = re.findall(r'```(\w*)\n', content)
    for i, lang in enumerate(code_blocks, 1):
        if not lang:
            issues.append(f"Code block {i} missing language specifier")

    # Check for common typos (example)
    common_typos = ["teh", "recieve", "seperate"]
    for typo in common_typos:
        if typo in content.lower():
            issues.append(f"Possible typo: '{typo}'")

    return issues
```

### 4. Business Rule Validation

**Purpose:** Enforce organizational policies

**Methods:**
- Check for sensitive data
- Verify compliance with standards
- Validate against brand guidelines

**Example:**
```python
def validate_business_rules(content: str, config: ContentConfig) -> list[str]:
    """Validate business rules."""
    issues = []

    # No sensitive data
    sensitive_patterns = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b(?:\d{4}[-\s]?){3}\d{4}\b',  # Credit card
    ]

    import re
    for pattern in sensitive_patterns:
        if re.search(pattern, content):
            issues.append(f"Possible sensitive data detected: {pattern}")

    # Brand guidelines (example: company name capitalization)
    if "chora-compose" in content.lower():
        correct_instances = content.count("chora-compose")
        total_instances = content.lower().count("chora-compose")
        if correct_instances < total_instances:
            issues.append("Inconsistent capitalization of 'chora-compose'")

    # Size limits
    max_size = 100000  # 100KB
    if len(content) > max_size:
        issues.append(f"Content exceeds size limit: {len(content)} > {max_size} bytes")

    return issues
```

---

## Schema Validation

For structured formats (JSON, YAML), validate against schemas:

### JSON Schema Validation

```python
import json
import jsonschema

def validate_json_schema(content: str, schema_path: str) -> list[str]:
    """Validate generated JSON against schema."""
    issues = []

    # Parse JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    # Load schema
    with open(schema_path) as f:
        schema = json.load(f)

    # Validate
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        issues.append(f"Schema validation failed: {e.message}")

    return issues
```

**Usage:**
```python
content = generator.generate(config, context)

# Validate against JSON schema
issues = validate_json_schema(
    content,
    schema_path="schemas/api-response-v1.json"
)

if issues:
    print("Validation failed:")
    for issue in issues:
        print(f"  - {issue}")
```

### Example Schema

`schemas/api-response-v1.json`:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "data", "timestamp"],
  "properties": {
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "data": {
      "type": "object"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

---

## Business Rule Validation

Create custom validators for organization-specific rules:

### Example: API Documentation Validator

```python
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    """Validation result."""
    passed: bool
    issues: List[str]
    warnings: List[str]


class APIDocValidator:
    """Validate generated API documentation."""

    def validate(self, content: str) -> ValidationResult:
        """Run all validation checks."""
        issues = []
        warnings = []

        # 1. Structure validation
        issues.extend(self._validate_structure(content))

        # 2. Required sections
        issues.extend(self._validate_required_sections(content))

        # 3. Code examples
        example_issues = self._validate_code_examples(content)
        issues.extend(example_issues)

        # 4. Quality checks
        warnings.extend(self._validate_quality(content))

        passed = len(issues) == 0

        return ValidationResult(
            passed=passed,
            issues=issues,
            warnings=warnings
        )

    def _validate_structure(self, content: str) -> List[str]:
        """Validate document structure."""
        issues = []

        # Must start with # heading
        if not content.strip().startswith("#"):
            issues.append("Missing top-level heading")

        # Must have ## subsections
        if "##" not in content:
            issues.append("Missing subsections")

        return issues

    def _validate_required_sections(self, content: str) -> List[str]:
        """Validate required API doc sections."""
        issues = []

        required_sections = [
            "Parameters",
            "Returns",
            "Example",
            "Errors"
        ]

        for section in required_sections:
            if f"## {section}" not in content and f"### {section}" not in content:
                issues.append(f"Missing required section: {section}")

        return issues

    def _validate_code_examples(self, content: str) -> List[str]:
        """Validate code examples."""
        issues = []

        # Check for code blocks
        if "```" not in content:
            issues.append("No code examples found")
            return issues

        # Check code blocks have language
        import re
        code_blocks = re.findall(r'```(\w*)\n(.*?)```', content, re.DOTALL)

        for i, (lang, code) in enumerate(code_blocks, 1):
            if not lang:
                issues.append(f"Code block {i} missing language specifier")

            # Check for common errors in examples
            if lang in ["python", "py"]:
                if "import" not in code and len(code.strip()) > 50:
                    issues.append(f"Python example {i} missing imports")

        return issues

    def _validate_quality(self, content: str) -> List[str]:
        """Validate quality (warnings, not blockers)."""
        warnings = []

        # Check line length
        max_length = 120
        for i, line in enumerate(content.split("\n"), 1):
            if len(line) > max_length:
                warnings.append(f"Line {i} exceeds {max_length} chars")

        # Check for TODO markers
        if "TODO" in content or "FIXME" in content:
            warnings.append("Contains TODO/FIXME markers")

        return warnings
```

**Usage:**
```python
# Generate content
content = generator.generate(config, context)

# Validate
validator = APIDocValidator()
result = validator.validate(content)

if not result.passed:
    print("Validation failed:")
    for issue in result.issues:
        print(f"  ✗ {issue}")

if result.warnings:
    print("\nWarnings:")
    for warning in result.warnings:
        print(f"  ⚠ {warning}")

# Only proceed if passed
if result.passed:
    save_content(content)
```

---

## Automated Testing

Integrate validation into test suites:

### pytest Integration

Create `tests/validation/test_generated_content.py`:

```python
import pytest
from chora_compose.generators.registry import GeneratorRegistry
from chora_compose.core.models import ContentConfig


@pytest.fixture
def jinja2_generator():
    """Get Jinja2 generator."""
    return GeneratorRegistry().get("jinja2")


def test_api_docs_structure(jinja2_generator):
    """Test API documentation has correct structure."""
    config = ContentConfig(
        content_id="test-api-docs",
        format="markdown",
        generation={
            "patterns": [{
                "type": "jinja2",
                "template_string": """# API Reference

## Parameters
- param1: Description

## Returns
Return value

## Example
```python
example_code()
```

## Errors
Error conditions
"""
            }]
        }
    )

    content = jinja2_generator.generate(config, {})

    # Validate structure
    assert content.startswith("# API Reference")
    assert "## Parameters" in content
    assert "## Returns" in content
    assert "## Example" in content
    assert "## Errors" in content


def test_no_unexpanded_variables(jinja2_generator):
    """Test generated content has no unexpanded variables."""
    config = ContentConfig(
        content_id="test-variables",
        format="markdown",
        generation={
            "patterns": [{
                "type": "jinja2",
                "template_string": "Version: {{ version }}\nDate: {{ date }}"
            }]
        }
    )

    context = {
        "version": "1.0.0",
        "date": "2025-10-21"
    }

    content = jinja2_generator.generate(config, context)

    # No unexpanded variables
    assert "{{" not in content
    assert "}}" not in content

    # Correct substitution
    assert "Version: 1.0.0" in content
    assert "Date: 2025-10-21" in content


def test_generated_json_valid(jinja2_generator):
    """Test generated JSON is valid."""
    import json

    config = ContentConfig(
        content_id="test-json",
        format="json",
        generation={
            "patterns": [{
                "type": "jinja2",
                "template_string": """{
  "version": "{{ version }}",
  "timestamp": "{{ timestamp }}",
  "data": {
    "count": {{ count }}
  }
}"""
            }]
        }
    )

    context = {
        "version": "1.0.0",
        "timestamp": "2025-10-21T10:00:00Z",
        "count": 42
    }

    content = jinja2_generator.generate(config, context)

    # Valid JSON
    data = json.loads(content)  # Should not raise
    assert data["version"] == "1.0.0"
    assert data["data"]["count"] == 42


def test_markdown_code_blocks_have_language():
    """Test Markdown code blocks specify language."""
    content = """# Example

```python
def example():
    pass
```

```javascript
function example() {}
```
"""

    # Find code blocks
    import re
    code_blocks = re.findall(r'```(\w+)', content)

    # All blocks have language
    assert len(code_blocks) == 2
    assert "python" in code_blocks
    assert "javascript" in code_blocks


@pytest.mark.parametrize("content,expected_issues", [
    ("# Title\n\n## Section\n\nContent", []),
    ("No heading", ["Missing top-level heading"]),
    ("# Title\n\nNo subsections", ["Missing subsections"]),
])
def test_markdown_structure_validation(content, expected_issues):
    """Test Markdown structure validation."""
    from docs.how_to.testing.validate_generated_content import validate_markdown_structure

    issues = validate_markdown_structure(content)
    assert issues == expected_issues
```

**Run tests:**
```bash
poetry run pytest tests/validation/
```

---

## Quality Gates

Define quality gates for different content types:

### Example: Documentation Quality Gate

```python
class DocumentationQualityGate:
    """Quality gate for documentation."""

    def __init__(self):
        self.min_length = 500  # chars
        self.max_length = 50000  # chars
        self.required_sections = ["Overview", "Example"]

    def check(self, content: str) -> tuple[bool, list[str]]:
        """
        Check if content passes quality gate.

        Returns:
            (passed, issues) tuple
        """
        issues = []

        # Length check
        length = len(content.strip())
        if length < self.min_length:
            issues.append(f"Too short: {length} < {self.min_length} chars")

        if length > self.max_length:
            issues.append(f"Too long: {length} > {self.max_length} chars")

        # Required sections
        for section in self.required_sections:
            if f"## {section}" not in content:
                issues.append(f"Missing section: {section}")

        # Code examples
        if "```" not in content:
            issues.append("No code examples")

        # No TODOs
        if "TODO" in content or "FIXME" in content:
            issues.append("Contains TODO/FIXME markers")

        passed = len(issues) == 0
        return passed, issues
```

**Usage in pipeline:**
```python
def generate_with_quality_gate(config: ContentConfig, context: dict) -> str:
    """Generate content with quality gate."""
    # Generate
    generator = GeneratorRegistry().get(config.generation["patterns"][0]["type"])
    content = generator.generate(config, context)

    # Quality gate
    gate = DocumentationQualityGate()
    passed, issues = gate.check(content)

    if not passed:
        raise ValueError(f"Quality gate failed:\n" + "\n".join(f"  - {i}" for i in issues))

    return content
```

---

## Common Validation Scenarios

### Scenario 1: Validate BDD Scenarios

```python
def validate_bdd_scenario(content: str) -> list[str]:
    """Validate BDD scenario structure and completeness."""
    issues = []

    # Required keywords
    required = ["Feature:", "Scenario:", "Given", "When", "Then"]
    for keyword in required:
        if keyword not in content:
            issues.append(f"Missing required keyword: {keyword}")

    # Feature name not empty
    import re
    feature_match = re.search(r'Feature: (.+)', content)
    if feature_match and not feature_match.group(1).strip():
        issues.append("Feature name is empty")

    # Scenarios have names
    scenario_matches = re.findall(r'Scenario: (.+)', content)
    for i, name in enumerate(scenario_matches, 1):
        if not name.strip():
            issues.append(f"Scenario {i} has empty name")

    # Steps are indented
    for line in content.split("\n"):
        if any(line.strip().startswith(step) for step in ["Given", "When", "Then", "And"]):
            if not line.startswith("  "):
                issues.append(f"Step not indented: {line.strip()}")

    return issues
```

### Scenario 2: Validate API Response JSON

```python
def validate_api_response_json(content: str) -> list[str]:
    """Validate generated API response JSON."""
    import json
    from datetime import datetime

    issues = []

    # Parse JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    # Required fields
    required_fields = ["version", "timestamp", "data"]
    for field in required_fields:
        if field not in data:
            issues.append(f"Missing required field: {field}")

    # Version format
    if "version" in data:
        import re
        if not re.match(r'^\d+\.\d+\.\d+$', data["version"]):
            issues.append(f"Invalid version format: {data['version']}")

    # Timestamp format (ISO 8601)
    if "timestamp" in data:
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            issues.append(f"Invalid timestamp format: {data['timestamp']}")

    return issues
```

### Scenario 3: Validate Code Generation Output

```python
def validate_generated_code(content: str, language: str) -> list[str]:
    """Validate generated code."""
    issues = []

    # Language-specific validation
    if language == "python":
        issues.extend(_validate_python_code(content))
    elif language == "javascript":
        issues.extend(_validate_javascript_code(content))

    return issues


def _validate_python_code(code: str) -> list[str]:
    """Validate Python code."""
    issues = []

    # Check syntax
    import ast
    try:
        ast.parse(code)
    except SyntaxError as e:
        issues.append(f"Python syntax error: {e}")

    # Check for common issues
    if "import" not in code and len(code) > 100:
        issues.append("No imports found (might be missing)")

    # Check for docstrings (if functions defined)
    if "def " in code and '"""' not in code:
        issues.append("Functions missing docstrings")

    return issues


def _validate_javascript_code(code: str) -> list[str]:
    """Validate JavaScript code."""
    issues = []

    # Basic checks (syntax checking requires external tools)

    # Check for semicolons (style check)
    lines = [l.strip() for l in code.split("\n") if l.strip()]
    code_lines = [l for l in lines if not l.startswith("//")]

    missing_semicolons = 0
    for line in code_lines:
        if line and not line.endswith((";", "{", "}", ",")):
            missing_semicolons += 1

    if missing_semicolons > len(code_lines) * 0.5:
        issues.append("Many lines missing semicolons (style issue)")

    return issues
```

---

## Best Practices

### 1. Validate Early and Often

```python
# ✓ Good: Validate at multiple stages
content = generator.generate(config, context)
validate_structure(content)
validate_completeness(content)
validate_business_rules(content)

# ✗ Bad: Only validate at the end
# (Issues discovered late, harder to debug)
```

### 2. Use Type-Specific Validators

```python
# ✓ Good: Format-specific validation
if config.format == "markdown":
    validate_markdown(content)
elif config.format == "json":
    validate_json_schema(content, schema_path)
elif config.format == "gherkin":
    validate_gherkin(content)

# ✗ Bad: Generic validation for all formats
assert len(content) > 0
```

### 3. Provide Actionable Error Messages

```python
# ✓ Good: Specific, actionable
issues.append("Missing required section 'Parameters' - add ## Parameters heading")

# ✗ Bad: Vague
issues.append("Invalid content")
```

### 4. Separate Blockers from Warnings

```python
# ✓ Good: Distinguish severity
class ValidationResult:
    blockers: list[str]  # Must fix
    warnings: list[str]  # Should fix

# ✗ Bad: Everything is a blocker
issues: list[str]  # Unclear what's critical
```

---

## Related Documentation

- [Test Configs Before Deployment](test-configs-before-deployment.md) - Pre-generation testing
- [Testing Philosophy](../../explanation/testing/testing-philosophy.md) - Testing approach
- [Integrate with GitHub Actions](../ci-cd/integrate-with-github-actions.md) - CI/CD validation
- [Generate Content](../generation/generate-content.md) - Content generation basics
