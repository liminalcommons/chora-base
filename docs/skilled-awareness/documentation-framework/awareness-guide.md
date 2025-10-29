# Awareness Guide: Documentation Framework

**SAP ID**: SAP-007
**Version**: 1.0.1
**Target Audience**: AI agents
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

### When to Use This SAP

**Use the Documentation Framework when**:
- Writing user-facing or developer documentation
- Creating executable How-Tos that should become tests
- Structuring docs with Diataxis (Tutorial/How-To/Reference/Explanation)
- Validating documentation frontmatter and structure

**Don't use for**:
- API documentation (use Sphinx/MkDocs instead)
- Code comments (inline documentation)
- README files (unless applying Diataxis structure)
- Quick notes or scratch docs

### Choose Document Type

**Choose document type (Diataxis)**:
- Learning? → Tutorial (e.g., `tutorials/01-getting-started.md`)
- Solving problem? → How-To (e.g., `how-to/setup-dev-environment.md`)
- Looking up spec? → Reference (e.g., `reference/api-spec.md`)
- Understanding why? → Explanation (e.g., `explanation/architecture-decisions.md`)

**Validate docs**:
```bash
python scripts/validate_docs.py --check-frontmatter --check-links
```

**Extract tests from How-Tos**:
```bash
python scripts/extract_tests.py --input user-docs/how-to/myguide.md --output tests/docs/test_myguide.py
```

---

## 2. Agent Context Loading

**Essential Context (3-4k tokens)**:
- [protocol-spec.md](protocol-spec.md) Sections 2, 4, 5 - Diataxis types, frontmatter, test extraction

**For writing docs**:
- [protocol-spec.md](protocol-spec.md) Section 2 - Diataxis decision matrix

**For extracting tests**:
- [protocol-spec.md](protocol-spec.md) Section 5 - Executable How-Tos

---

## 3. Common Workflows

### 3.1 Write How-To Guide with Test Extraction

**Context**: 2k tokens (Protocol Sections 4, 5)

**Steps**:
1. **Create file** (user-docs/how-to/NN-verb-noun.md):
   ```markdown
   ---
   title: How to Validate Email Addresses
   type: how-to
   status: current
   audience: intermediate
   last_updated: 2025-10-28
   test_extraction: true
   ---

   ## Problem
   Need to validate email addresses before processing.

   ## Solution
   ```python
   from my_package.utils import validate_email

   def test_email_validation():
       assert validate_email("user@example.com") == True
       assert validate_email("invalid") == False
   ```
   ```

2. **Extract tests**:
   ```bash
   python scripts/extract_tests.py --input user-docs/how-to/01-validate-email.md --output tests/docs/test_validate_email.py
   ```

3. **Run tests**:
   ```bash
   pytest tests/docs/test_validate_email.py
   ```

4. **Success**: Tests pass, docs validated

### 3.2 Choose Correct Document Type

**Context**: 1k tokens (Protocol Section 2.2 - Decision Matrix)

**Decision Tree**:
```
User wants to...
├─ Learn feature end-to-end? → Tutorial
├─ Solve specific problem? → How-To
├─ Look up parameters/schema? → Reference
└─ Understand design decision? → Explanation
```

**Examples**:
- "Build your first MCP server" → Tutorial (learning-oriented)
- "How to add custom error handling" → How-To (task-oriented)
- "MCP Protocol Schema" → Reference (information-oriented)
- "Why we use Diataxis" → Explanation (understanding-oriented)

### 3.3 Validate Documentation

**Context**: 2k tokens (Protocol Section 7)

**Steps**:
1. **Check frontmatter**:
   ```bash
   python scripts/validate_docs.py --check-frontmatter
   ```
   Validates YAML syntax, required fields, enum values

2. **Check links**:
   ```bash
   python scripts/validate_docs.py --check-links
   ```
   Validates internal and external links

3. **Fix issues**:
   - Invalid YAML → Fix syntax
   - Missing fields → Add required frontmatter
   - Broken links → Update or remove

---

## 4. Integration Patterns

### 4.1 With Development Lifecycle (SAP-012)

**DDD Workflow**:
1. Write How-To guide (documentation first)
2. Extract tests from How-To (BDD scenarios)
3. Implement code to make tests pass (TDD)
4. Docs + tests + code all synchronized

### 4.2 With CI/CD (SAP-005)

**docs-quality.yml workflow**:
- Validates frontmatter on every PR
- Checks links on every PR
- Extracts and runs tests from How-Tos
- Blocks merge if docs invalid

---

## 5. Best Practices

**DO**:
- ✅ Add frontmatter to all docs
- ✅ Use `test_extraction: true` for How-Tos
- ✅ Update `last_updated` when editing
- ✅ Choose correct Diataxis type

**DON'T**:
- ❌ Mix document types (tutorial + reference)
- ❌ Skip frontmatter validation
- ❌ Leave untested code in How-Tos
- ❌ Forget to cross-reference related docs

---

## 6. Common Pitfalls

### Pitfall 1: Mixing Diataxis Types
**Scenario**: Creating a "tutorial" that's actually a reference manual with procedural steps

**Example**:
```markdown
# Tutorial: API Endpoints (WRONG)
- GET /users - Returns all users
- POST /users - Creates a user
- [List continues...]
```

**Fix**: This is Reference material. Tutorials teach end-to-end learning:
```markdown
# Tutorial: Building Your First API Client (RIGHT)
Learn to interact with the API by building a simple user management client.
```

**Why it matters**: Users searching for "how to get started" get an API spec instead

### Pitfall 2: Untested How-Tos
**Scenario**: How-To guide shows code that doesn't actually work

**Example** (from Wave 2 SAP audit):
```markdown
## How to Validate Frontmatter
Run: python scripts/validate_docs.py --check-frontmatter
```
**Problem**: Script didn't exist, or had different flags

**Fix**: Add `test_extraction: true` to frontmatter, write executable examples:
```python
# This code runs as part of CI/CD
def test_validate_frontmatter():
    result = run_validation("--check-frontmatter")
    assert result.exit_code == 0
```

**Why it matters**: Broken How-Tos damage user trust

### Pitfall 3: Missing Frontmatter
**Scenario**: Documentation file created without required frontmatter

**Example**:
```markdown
# How to Set Up CI/CD
(No frontmatter at all)
```

**Fix**: Always add complete frontmatter:
```markdown
---
title: How to Set Up CI/CD
type: how-to
status: current
audience: intermediate
last_updated: 2025-10-28
test_extraction: false
---
```

**Why it matters**: Documentation tooling relies on frontmatter for validation, categorization, indexing

### Pitfall 4: Broken Cross-References
**Scenario**: Documentation references moved/renamed files after restructure

**Example** (from Wave 1 migration):
```
OLD (broken): Link path ../../reference/DOCUMENTATION_STANDARD.md
PROBLEM: Wave 1 moved to /static-template/DOCUMENTATION_STANDARD.md
```

**Fix**: Use absolute paths from repo root:
```markdown
See [DOCUMENTATION_STANDARD.md](/static-template/DOCUMENTATION_STANDARD.md)
```

**Why it matters**: Broken links create poor user experience, discovered during Wave 2 SAP-007 audit

### Pitfall 5: Stale last_updated Dates
**Scenario**: Document edited but frontmatter not updated

**Example**:
```markdown
---
title: How to Deploy
last_updated: 2024-01-15
---
# How to Deploy
(Content updated in October 2025, date not changed)
```

**Fix**: Always update `last_updated` when editing:
```markdown
---
title: How to Deploy
last_updated: 2025-10-28
---
```

**Why it matters**: Users can't assess document freshness, automated tools flag as stale

---

## 7. Related Content

### Within This SAP (skilled-awareness/documentation-framework/)
- [capability-charter.md](capability-charter.md) - Business value and scope of Documentation Framework
- [protocol-spec.md](protocol-spec.md) - Complete technical specification for Diataxis and frontmatter
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step adoption guide for new projects
- [ledger.md](ledger.md) - Adoption tracking and feedback

### Developer Process (dev-docs/)
**Standards**:
- [/static-template/DOCUMENTATION_STANDARD.md](/static-template/DOCUMENTATION_STANDARD.md) - Implementation of Diataxis framework

**Tools**:
- [/static-template/scripts/extract_tests.py](/static-template/scripts/extract_tests.py) - Executable How-To test extraction

### Project Lifecycle (project-docs/)
**Audits**:
- `/docs/project-docs/audits/wave-2-sap-007-audit.md` - This SAP's audit report (to be created after SAP-007 completion)

**Planning** (to be referenced when created):
- Wave 2 Sprint Plan - SAP audit activities (includes SAP-007)
- Project roadmap - Documentation improvements in Wave 1 and Wave 2

### User Guides (user-docs/)
**Existing**:
- [/docs/user-docs/explanation/architecture-clarification.md](/docs/user-docs/explanation/architecture-clarification.md) - Architecture overview including documentation structure
- [/docs/user-docs/explanation/benefits-of-chora-base.md](/docs/user-docs/explanation/benefits-of-chora-base.md) - Benefits of structured documentation approach

**Planned** (to be created in Wave 2 Phase 5):
- Tutorial: Write your first executable How-To guide
- How-To: Choose the correct Diataxis type for your doc
- Reference: Complete frontmatter field schema

### Other SAPs (skilled-awareness/)
**Framework**:
- [/docs/skilled-awareness/sap-framework/protocol-spec.md](/docs/skilled-awareness/sap-framework/protocol-spec.md) - SAP structure specification (used to create SAP-007)

**Related Capabilities**:
- [/docs/skilled-awareness/link-validation-reference-management/](/docs/skilled-awareness/link-validation-reference-management/) - SAP-016, validates documentation links
- [/docs/skilled-awareness/testing-framework/](/docs/skilled-awareness/testing-framework/) - SAP-004, runs tests extracted from How-Tos
- [/docs/skilled-awareness/development-lifecycle/](/docs/skilled-awareness/development-lifecycle/) - SAP-012, DDD workflow integration

---

**Version History**:
- **1.0.1** (2025-10-28): Added "When to Use" section, "Common Pitfalls" with Wave 2 learnings, enhanced "Related Content" with 4-domain coverage
- **1.0.0** (2025-10-28): Initial awareness guide
