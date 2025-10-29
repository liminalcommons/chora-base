# Awareness Guide: Documentation Framework

**SAP ID**: SAP-007
**Version**: 1.0.0
**Target Audience**: AI agents
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

**Choose document type**:
- Learning? → Tutorial
- Solving problem? → How-To
- Looking up spec? → Reference
- Understanding why? → Explanation

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

## 6. Related Resources

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [DOCUMENTATION_STANDARD.md](../../../../static-template/DOCUMENTATION_STANDARD.md)
- [scripts/extract_tests.py](../../../../static-template/scripts/extract_tests.py)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial awareness guide
