# Capability Charter: Documentation Framework

**SAP ID**: SAP-007
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Owner**: Victor (chora-base maintainer)
**Created**: 2025-10-28
**Last Updated**: 2025-10-28

---

## 1. Problem Statement

chora-base provides **Diataxis-based documentation framework** with frontmatter, executable How-Tos, and test extraction, but lacks:

1. **Explicit Documentation Contracts** - No documented guarantees about structure, frontmatter, validation
2. **Diataxis Rationale** - Why 4 types (Tutorial, How-To, Reference, Explanation) not explained
3. **Test Extraction Clarity** - How executable How-Tos → pytest tests unclear
4. **Quality Standards** - Documentation quality metrics not defined

**Result**: Inconsistent docs, unclear which type to use, test extraction underutilized

---

## 2. Proposed Solution

A **comprehensive SAP describing Diataxis framework, frontmatter schema, executable How-Tos, and test extraction**.

**Key Principles**:
1. **Diataxis-Based** - 4 document types by user intent
2. **Frontmatter-Validated** - YAML metadata with schema
3. **Executable How-Tos** - Code examples → pytest tests
4. **Documentation-Driven** - Write docs before code (DDD)

---

## 3. Scope

**In Scope**: DOCUMENTATION_STANDARD.md (~700 lines), Diataxis structure (user-docs/, dev-docs/, project-docs/), frontmatter schema, scripts/extract_tests.py

**Out of Scope**: API documentation generators (Sphinx, MkDocs)

---

## 4. Outcomes

**Success Criteria** (Phase 3):
- ✅ SAP-007 complete (all 5 artifacts)
- ✅ All 4 Diataxis types documented
- ✅ Frontmatter schema validated
- ✅ Test extraction workflow explained

---

## 5. Stakeholders

**Template Maintainer**: Victor
**AI Agents**: Use SAP-007 to write docs, extract tests
**Project Developers**: Use Diataxis for documentation

---

## 6. Dependencies

- ✅ SAP-000 (sap-framework)
- SAP-012 (development-lifecycle) - DDD uses documentation framework

---

## 7. Lifecycle

**Phase 3**: Create SAP-007 (all 5 artifacts)
**Phase 4**: Enhance with automated validation

---

## 8. Related Documents

- [DOCUMENTATION_STANDARD.md](../../../../static-template/DOCUMENTATION_STANDARD.md)
- [scripts/extract_tests.py](../../../../static-template/scripts/extract_tests.py)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial charter for documentation-framework SAP
