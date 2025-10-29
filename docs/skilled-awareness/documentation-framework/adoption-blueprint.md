# Adoption Blueprint: Documentation Framework

**SAP ID**: SAP-007
**Version**: 1.0.0
**Last Updated**: 2025-10-28

---

## 1. Overview

This blueprint guides using chora-base's Diataxis documentation framework.

**Time Estimate**: 10-15 minutes to learn, 5-10 min per document

---

## 2. Prerequisites

- Generated project from chora-base (SAP-003)
- Documentation directories exist (user-docs/, dev-docs/, project-docs/)

---

## 3. Quick Start

### Step 1: Choose Document Type

**Ask**: What does the user want to do?
- **Learn** → Tutorial (e.g., "Build your first MCP server")
- **Solve problem** → How-To (e.g., "How to add error handling")
- **Look up spec** → Reference (e.g., "API Parameters")
- **Understand why** → Explanation (e.g., "Why Diataxis?")

### Step 2: Create Document with Frontmatter

**Example** (user-docs/how-to/01-my-guide.md):
```markdown
---
title: How to Add Custom Error Handling
type: how-to
status: current
audience: intermediate
last_updated: 2025-10-28
test_extraction: true
---

## Problem
Need to handle custom error types gracefully.

## Solution
```python
from my_package.utils.errors import CustomError

def test_custom_error_handling():
    with pytest.raises(CustomError):
        raise CustomError("Test error")
```
```

### Step 3: Extract Tests (for How-Tos)

```bash
python scripts/extract_tests.py \
  --input user-docs/how-to/01-my-guide.md \
  --output tests/docs/test_my_guide.py

pytest tests/docs/test_my_guide.py
```

**Success**: Tests extracted and pass

---

## 4. Document Types Guide

### Tutorial

**When**: First-time user learning
**Structure**: Step 1 → Step 2 → Step 3 (with expected output)
**Example**: user-docs/tutorials/01-first-mcp-server.md

### How-To

**When**: Solving specific problem
**Structure**: Problem → Solution → Variations
**Example**: user-docs/how-to/01-generate-new-mcp-server.md
**Enable**: `test_extraction: true`

### Reference

**When**: Looking up specifications
**Structure**: API docs, schemas, parameters
**Example**: user-docs/reference/mcp-conventions.md

### Explanation

**When**: Understanding concepts
**Structure**: Context → Rationale → Trade-offs
**Example**: user-docs/explanation/vision-driven-development.md

---

## 5. Frontmatter Fields

**Required**:
```yaml
title: String              # Document title
type: tutorial|how-to|reference|explanation|process|vision
status: draft|current|deprecated|archived
audience: beginner|intermediate|advanced|all|maintainer|agent
last_updated: YYYY-MM-DD   # When last edited
```

**Optional**:
```yaml
version: X.Y.Z             # Semver
tags: [keyword1, keyword2] # For search
test_extraction: true      # For How-Tos
related: ["path/to/doc.md"]  # Related docs
```

---

## 6. Test Extraction

**Enable in frontmatter**:
```yaml
test_extraction: true
```

**Write testable code**:
```python
def test_example():
    result = my_function("input")
    assert result == "expected"
```

**Extract**:
```bash
python scripts/extract_tests.py --input <doc> --output <test-file>
```

**Validate**:
```bash
pytest <test-file>
```

---

## 7. Validation

**Check frontmatter**:
```bash
python scripts/validate_docs.py --check-frontmatter
```

**Check links**:
```bash
python scripts/validate_docs.py --check-links
```

**CI validates automatically** (docs-quality.yml workflow)

---

## 8. Troubleshooting

**Problem**: Frontmatter validation fails
**Solution**: Check YAML syntax, ensure required fields present

**Problem**: Test extraction fails
**Solution**: Ensure code blocks have `python` language tag, check syntax

**Problem**: Tests don't pass
**Solution**: Code examples must be runnable standalone, include all imports

---

## 9. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [DOCUMENTATION_STANDARD.md](../../../../static-template/DOCUMENTATION_STANDARD.md)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (docs-quality.yml)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial adoption blueprint
