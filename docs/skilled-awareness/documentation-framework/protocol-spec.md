# Protocol Specification: Documentation Framework

**SAP ID**: SAP-007
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Last Updated**: 2025-10-28

---

## 1. Overview

### Purpose

The documentation-framework capability provides **Diataxis-based documentation** with frontmatter validation, executable How-Tos, and test extraction. It defines structure, quality standards, and automation for all project documentation.

### Design Principles

1. **Diataxis-Based** - 4 document types organized by user intent (Tutorial, How-To, Reference, Explanation)
2. **Frontmatter-Validated** - YAML metadata with schema enforcement
3. **Executable How-Tos** - Code examples extractable to pytest tests
4. **Documentation-Driven** - Write docs before code (DDD workflow)
5. **Dual Audience** - Serves humans (learning) and AI agents (task execution)

---

## 2. Diataxis Framework

### 2.1 The Four Document Types

**Tutorial** (Learning-oriented):
- **Purpose**: Teach through step-by-step lessons
- **User Intent**: "Teach me how to use this"
- **Structure**: Sequential steps with expected output
- **Example**: "Build your first MCP server"

**How-To Guide** (Task-oriented):
- **Purpose**: Solve specific problems
- **User Intent**: "Show me how to solve X"
- **Structure**: Problem → Solution with variations
- **Example**: "How to add custom error handling"

**Reference** (Information-oriented):
- **Purpose**: Provide technical specifications
- **User Intent**: "What parameters does this take?"
- **Structure**: API docs, schemas, configurations
- **Example**: "MCP Protocol Schema Reference"

**Explanation** (Understanding-oriented):
- **Purpose**: Explain concepts and design decisions
- **User Intent**: "Why does this work this way?"
- **Structure**: Context, rationale, trade-offs
- **Example**: "Why we use Diataxis for documentation"

### 2.2 Decision Matrix

**When to Use Each Type**:

| Scenario | Document Type |
|----------|---------------|
| First-time user onboarding | Tutorial |
| Solving a specific problem | How-To Guide |
| Looking up API parameters | Reference |
| Understanding design decisions | Explanation |
| Learning a new feature | Tutorial |
| Multiple approaches to same problem | How-To Guide |
| Schema definitions | Reference |
| Architecture rationale | Explanation |

---

## 3. Directory Structure

### 3.1 Three Documentation Directories

```
project-root/
├── user-docs/           # User-facing documentation
│   ├── tutorials/       # Learning-oriented
│   ├── how-to/          # Task-oriented
│   ├── reference/       # Information-oriented
│   ├── explanation/     # Understanding-oriented
│   └── README.md        # User docs index
│
├── dev-docs/            # Developer documentation
│   ├── workflows/       # Development processes (DDD, BDD, TDD)
│   ├── vision/          # Long-term plans, capability evolution
│   ├── examples/        # Code examples, walkthroughs
│   └── README.md        # Dev docs index
│
└── project-docs/        # Project management
    ├── sprints/         # Sprint planning, retrospectives
    ├── releases/        # Release planning, upgrade guides
    ├── metrics/         # Process metrics, velocity tracking
    └── README.md        # Project docs index
```

### 3.2 File Naming Conventions

**Tutorials**: `NN-descriptive-name.md` (e.g., `01-first-mcp-server.md`)
**How-Tos**: `NN-verb-noun.md` (e.g., `01-generate-new-mcp-server.md`)
**Reference**: `noun-name.md` (e.g., `mcp-conventions.md`)
**Explanation**: `descriptive-topic.md` (e.g., `vision-driven-development.md`)

---

## 4. Frontmatter Schema

### 4.1 YAML Metadata Structure

Every document must include YAML frontmatter:

```yaml
---
title: String              # Document title (required)
type: Enum                 # Document type (required)
status: Enum               # Document status (required)
audience: Enum             # Target audience (required)
last_updated: Date         # YYYY-MM-DD (required)
trace_id: String           # CHORA_TRACE_ID from SAP-001 coordination (optional)
version: SemVer            # Document version (optional)
tags: [String]             # Keywords for search (optional)
test_extraction: Boolean   # Enable test extraction (optional, How-Tos only)
related: [String]          # Related doc paths (optional)
---
```

### 4.2 Field Specifications

**type** (Enum):
- `tutorial` - Learning-oriented
- `how-to` - Task-oriented
- `reference` - Information-oriented
- `explanation` - Understanding-oriented
- `process` - Process documentation (workflows)
- `vision` - Strategic planning

**status** (Enum):
- `draft` - Work in progress
- `current` - Active, up-to-date
- `deprecated` - Superseded, use alternative
- `archived` - Historical reference only

**audience** (Enum):
- `beginner` - New users
- `intermediate` - Experienced users
- `advanced` - Expert users
- `all` - All audiences
- `maintainer` - Project maintainers only
- `agent` - AI agents only

**test_extraction** (Boolean):
- `true` - Extract code blocks to pytest tests
- `false` - Do not extract (default)
- Only applicable to How-To guides

**trace_id** (String):
- CHORA_TRACE_ID from originating coordination request (SAP-001)
- Format: `{domain}-{yyyy}-{nnn}` (e.g., `mcp-taskmgr-2025-003`)
- Enables end-to-end traceability from coordination → documentation → implementation → metrics
- Optional but recommended for all docs created from coordination workflow
- See GAP-001 resolution for trace propagation protocol

---

## 5. Executable How-Tos

### 5.1 Purpose

How-To guides can include **executable code examples** that are automatically extracted to pytest tests, ensuring documentation stays synchronized with code.

### 5.2 Code Block Format

**Extractable code blocks** must:
1. Use triple-backtick fenced code blocks with language identifier
2. Include all necessary imports and setup
3. Produce deterministic output
4. Be runnable as standalone pytest tests

**Example**:

```markdown
## How to Validate Email Addresses

Enable test extraction in frontmatter:
```yaml
test_extraction: true
```

Add code example:
```python
from my_package.utils.validation import validate_email

def test_validate_email():
    # Valid email
    assert validate_email("user@example.com") == True

    # Invalid email
    assert validate_email("invalid-email") == False
```
```

### 5.3 Test Extraction Workflow

**Process**:
1. Write How-To guide with `test_extraction: true` frontmatter
2. Include executable code blocks with `python` language tag
3. Run `python scripts/extract_tests.py --input user-docs/how-to/validate-email.md --output tests/docs/test_validate_email.py`
4. Generated test file includes all code blocks as test functions
5. Run `pytest tests/docs/` to validate documentation examples

**Command**:
```bash
python scripts/extract_tests.py \
  --input user-docs/how-to/01-generate-new-mcp-server.md \
  --output tests/docs/test_generate_server.py
```

**Generated Test**:
```python
"""
Auto-generated tests from: user-docs/how-to/01-generate-new-mcp-server.md
Last updated: 2025-10-28
"""

import pytest

# Test extracted from section "How to Generate Server"
def test_generate_server():
    from my_package import generate_server

    server = generate_server("my-server")
    assert server.name == "my-server"
```

---

## 6. Documentation Quality Standards

### 6.1 Required Elements

**All Documents**:
- ✅ Valid YAML frontmatter
- ✅ Meaningful title
- ✅ Clear audience targeting
- ✅ Last updated date (within 6 months for current docs)

**Tutorials**:
- ✅ Step-by-step structure
- ✅ Expected output for each step
- ✅ Success criteria

**How-To Guides**:
- ✅ Problem statement
- ✅ Solution with code examples
- ✅ Alternative approaches (when applicable)

**Reference**:
- ✅ Complete API/schema documentation
- ✅ Parameter types and defaults
- ✅ Examples

**Explanation**:
- ✅ Context and background
- ✅ Rationale for decisions
- ✅ Trade-offs discussed

### 6.2 Quality Metrics

**Tracked Metrics**:
- Documentation coverage (% of features documented)
- Staleness (docs older than 6 months)
- Test extraction rate (% of How-Tos with tests)
- Cross-reference density (avg links per doc)
- Readability score (Flesch reading ease)

**Quality Gates**:
- All public APIs must have reference docs
- Critical workflows must have How-To guides
- Major features must have tutorials
- All How-Tos should have `test_extraction: true` when possible

---

## 7. Automation & Validation

### 7.1 Frontmatter Validation

**Command**:
```bash
python scripts/validate_docs.py --check-frontmatter
```

**Checks**:
- ✅ YAML syntax valid
- ✅ Required fields present (title, type, status, audience, last_updated)
- ✅ Enum values valid
- ✅ Dates in YYYY-MM-DD format
- ✅ Version in semver format (if present)

### 7.2 Link Validation

**Command**:
```bash
python scripts/validate_docs.py --check-links
```

**Checks**:
- ✅ Internal links resolve (relative paths exist)
- ✅ External links respond (HTTP 200)
- ✅ Anchor links exist in target documents

### 7.3 Test Extraction

**Command**:
```bash
python scripts/extract_tests.py --input-dir user-docs/how-to/ --output-dir tests/docs/
```

**Process**:
- Scans all How-To guides with `test_extraction: true`
- Extracts code blocks to pytest tests
- Generates test file with source reference
- Reports extraction statistics

---

## 8. Integration with Development Workflow

### 8.1 Documentation-Driven Design (DDD)

**Workflow**:
1. **Write Documentation First** - Create How-To or Tutorial before coding
2. **Extract Tests** - Generate pytest tests from How-To examples
3. **Implement Code** - Write code to make tests pass (TDD)
4. **Validate Docs** - Ensure tests pass, docs accurate

**Benefits**:
- Documentation drives implementation
- Examples always tested
- Docs never drift from code

### 8.2 CI/CD Integration

**GitHub Actions** (.github/workflows/docs-quality.yml):
```yaml
- name: Validate documentation
  run: |
    python scripts/validate_docs.py --check-frontmatter --check-links
    python scripts/extract_tests.py --input-dir user-docs/how-to/ --output-dir tests/docs/
    pytest tests/docs/
```

**Enforces**:
- Frontmatter validation on all PRs
- Link checking on all PRs
- Test extraction and execution

---

## 9. Best Practices

### 9.1 Writing Guidelines

**DO**:
- ✅ Use active voice ("Click the button" not "The button should be clicked")
- ✅ Include code examples for How-Tos and Tutorials
- ✅ Cross-reference related documents
- ✅ Update `last_updated` when editing
- ✅ Target specific audience (don't write for "everyone")

**DON'T**:
- ❌ Mix document types (don't put tutorials in How-To guides)
- ❌ Leave docs without frontmatter
- ❌ Include untested code examples in How-Tos
- ❌ Create orphan docs (no links to/from other docs)

### 9.2 Maintenance

**Review Cadence**:
- **Monthly**: Check for stale docs (>6 months old)
- **Quarterly**: Validate all links
- **Per Release**: Update version-specific docs
- **Continuous**: Update docs when code changes

**Staleness Warning**:
```yaml
# Add to frontmatter if doc is stale
status: deprecated
related: ["path/to/updated-doc.md"]
```

---

## 10. Related Documents

**SAP-007 Artifacts**:
- [capability-charter.md](capability-charter.md)
- [awareness-guide.md](awareness-guide.md)
- [adoption-blueprint.md](adoption-blueprint.md)
- [ledger.md](ledger.md)

**Documentation Components**:
- [DOCUMENTATION_STANDARD.md](/static-template/DOCUMENTATION_STANDARD.md) (~700 lines)
- [scripts/validate_docs.py](/static-template/scripts/validate_docs.py)
- [scripts/extract_tests.py](/static-template/scripts/extract_tests.py)
- [scripts/docs_metrics.py](/static-template/scripts/docs_metrics.py)

**Related SAPs**:
- [sap-framework/](../sap-framework/) - SAP-000
- [development-lifecycle/](../development-lifecycle/) - SAP-012 (DDD workflow)
- [ci-cd-workflows/](../ci-cd-workflows/) - SAP-005 (docs-quality.yml)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for documentation-framework
