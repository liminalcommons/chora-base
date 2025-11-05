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
# Core Fields (Required)
title: String              # Document title (required)
type: Enum                 # Document type (required)
status: Enum               # Document status (required)
audience: Enum             # Target audience (required)
last_updated: Date         # YYYY-MM-DD (required)

# Optional Metadata
trace_id: String           # CHORA_TRACE_ID from SAP-001 coordination (optional)
version: SemVer            # Document version (optional)
tags: [String]             # Keywords for search - use .chora/conventions/tag-vocabulary.yaml (optional)
test_extraction: Boolean   # Enable test extraction (optional, How-Tos only)
related: [String]          # Related doc paths (optional)

# NEW: Curatorial Metadata (Phase 2.2) - Optional but recommended
sap_id: String             # SAP ID if doc is part of SAP (e.g., "SAP-015")
complexity: Enum           # "beginner", "intermediate", "advanced" (optional)
prerequisites:             # Prerequisites for understanding this doc (optional)
  saps: [String]           # Required SAPs (e.g., ["SAP-000", "SAP-001"])
  knowledge: [String]      # Required knowledge (e.g., ["git", "python"])
estimated_reading_time: Int  # Minutes to read (optional)
related_to:                # Explicit cross-references (optional)
  saps: [String]           # Related SAPs (e.g., ["SAP-015", "SAP-009"])
  docs: [String]           # Related docs (paths relative to repo root)
diataxis_category: Enum    # Explicit category: "tutorial", "how-to", "reference", "explanation" (optional, should match type)
content_blocks: [String]   # Major sections (e.g., ["installation", "validation", "troubleshooting"]) (optional)
progressive_loading:       # Progressive loading hints for agents (optional)
  phase_1: String          # Quick reference section (e.g., "lines 1-50")
  phase_2: String          # Implementation details (e.g., "lines 51-200")
  phase_3: String          # Deep dive (e.g., "full" or "lines 201-end")
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

### 4.3 Curatorial Metadata Fields (Phase 2.2)

The following fields enable better content discovery, dependency tracking, and progressive loading for agents:

**sap_id** (String):
- SAP identifier if document is part of a SAP (e.g., `"SAP-015"`)
- Links documentation to SAP catalog entry
- Enables filtering: "Show all docs for SAP-015"

**complexity** (Enum):
- `"beginner"` - Minimal prerequisites, simple concepts
- `"intermediate"` - Some experience required
- `"advanced"` - Expert knowledge needed
- Helps agents select appropriate docs for user skill level

**prerequisites** (Object):
- `prerequisites.saps` - Array of required SAP IDs (e.g., `["SAP-000", "SAP-001"]`)
- `prerequisites.knowledge` - Array of required skills/concepts (e.g., `["git", "python", "regex"]`)
- Enables dependency-aware documentation navigation
- Agents can suggest reading prerequisite docs first

**estimated_reading_time** (Integer):
- Estimated minutes to read this document
- Helps agents estimate context loading time
- Used for progressive loading decisions

**related_to** (Object):
- `related_to.saps` - Array of related SAP IDs (e.g., `["SAP-015", "SAP-009"]`)
- `related_to.docs` - Array of related doc paths (e.g., `["/docs/user-docs/tutorials/beads-intro.md"]`)
- Explicit cross-references for navigation
- More structured than plain `related` field

**diataxis_category** (Enum):
- Explicit Diataxis category: `"tutorial"`, `"how-to"`, `"reference"`, `"explanation"`
- Should match `type` field
- Used for Diataxis compliance validation

**content_blocks** (Array):
- Major sections/topics in this document (e.g., `["installation", "validation", "troubleshooting"]`)
- Enables snippet-level curation
- Agents can search: "Find docs with 'troubleshooting' section"

**progressive_loading** (Object):
- `progressive_loading.phase_1` - Quick reference section (e.g., `"lines 1-50"` or `"## Quick Start only"`)
- `progressive_loading.phase_2` - Implementation details (e.g., `"lines 51-200"` or `"through ## Configuration"`)
- `progressive_loading.phase_3` - Deep dive (e.g., `"full"` or `"lines 201-end"`)
- Helps agents load exactly what they need for current context
- Reduces token usage for large documents

**Example with Curatorial Metadata**:

```yaml
---
# Core Fields
title: "Task Tracking with Beads"
type: "how-to"
status: "current"
audience: "intermediate"
last_updated: "2025-11-04"

# Optional Metadata
tags: ["task-tracking", "beads", "git-native"]
test_extraction: false

# Curatorial Metadata
sap_id: "SAP-015"
complexity: "intermediate"
prerequisites:
  saps: ["SAP-000"]
  knowledge: ["git", "cli"]
estimated_reading_time: 15
related_to:
  saps: ["SAP-001", "SAP-010"]
  docs: ["/docs/user-docs/reference/beads-cli.md"]
diataxis_category: "how-to"
content_blocks: ["installation", "basic-usage", "advanced-workflows", "troubleshooting"]
progressive_loading:
  phase_1: "lines 1-80"      # Quick start through basic usage
  phase_2: "lines 81-250"    # Advanced workflows
  phase_3: "full"            # Including troubleshooting
---
```

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

## 11. Self-Evaluation: Awareness File Coverage

### Workflow Coverage Analysis

**Protocol Spec Workflows**: 5 (specified in this document)
1. Choose Diataxis type (decision matrix)
2. Add frontmatter (YAML schema)
3. Write executable How-To (test extraction)
4. Validate documentation (frontmatter, structure)
5. Organize by directory (user/dev/project docs)

**AGENTS.md Workflows**: 5 (implemented)
1. Choose Correct Diataxis Type
2. Add and Validate Frontmatter
3. Write Executable How-To with Test Extraction
4. Refactor Duplicated Documentation
5. Validate Documentation Structure

**CLAUDE.md Workflows**: 3 (implemented)
1. Create Documentation with Frontmatter (Write tool)
2. Extract and Run Tests from How-Tos (Bash + Read + Edit tools)
3. Validate and Fix Documentation Quality (Bash + Edit tools)

**Coverage**: 5/5 = 100% (all protocol-spec workflows covered in AGENTS.md)

**Variance**: 40% (5 generic workflows vs 3 Claude-specific workflows)

**Rationale**:
- AGENTS.md provides comprehensive step-by-step guidance for all agents (5 workflows)
- CLAUDE.md focuses on tool-specific patterns (Bash/Read/Write/Edit) for Claude Code (3 workflows)
- Both files cover all protocol-spec workflows but with different levels of detail
- CLAUDE.md consolidates "Add Frontmatter", "Write How-To", and "Validate" into integrated tool-focused workflows
- Variance is acceptable: both provide equivalent support for SAP-007 adoption

**Conclusion**: ✅ Equivalent support across agent types

---

**Version History**:
- **1.0.0** (2025-10-28): Initial protocol specification for documentation-framework
- **1.0.1** (2025-11-05): Added self-evaluation section for awareness file coverage
