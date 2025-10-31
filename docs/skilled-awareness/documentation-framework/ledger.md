# Traceability Ledger: Documentation Framework

**SAP ID**: SAP-007
**Current Version**: 1.0.0
**Status**: Draft (Phase 3)
**Last Updated**: 2025-10-28

---

## 1. Projects Using Documentation Framework

| Project | Diataxis Adopted | Test Extraction Enabled | Last Updated |
|---------|------------------|-------------------------|--------------|
| chora-base | ✅ Yes | ✅ Yes | 2025-10-28 |
| chora-compose | ⚠️ Partial | ❌ No | 2025-10-20 |
| mcp-n8n | ❌ No | ❌ No | 2025-10-22 |

---

## 2. Version History

| Version | Release Date | Type | Changes |
|---------|--------------|------|---------|
| 1.0.0 | 2025-10-28 | MAJOR | Initial SAP-007 release: Diataxis framework, frontmatter schema, test extraction |

---

## 3. Documentation Coverage Metrics

### By Project

| Project | Total Docs | With Frontmatter | Test Extraction Enabled | Coverage |
|---------|------------|------------------|-------------------------|----------|
| chora-base | ~50 | ~50 (100%) | ~10 (20%) | ✅ Complete |
| chora-compose | ~15 | ~5 (33%) | 0 (0%) | ⚠️ Partial |

### By Document Type

| Type | Count (chora-base) | % of Total |
|------|--------------------|------------|
| Tutorial | ~5 | 10% |
| How-To | ~20 | 40% |
| Reference | ~15 | 30% |
| Explanation | ~10 | 20% |

---

## 4. Test Extraction Metrics

**chora-base**:
- How-To guides: ~20
- Test extraction enabled: ~10 (50%)
- Generated tests: ~10 files
- Test pass rate: 100%

**Target**: 80% of How-Tos with test extraction by Phase 4

---

## 5. Quality Metrics

**Staleness** (docs >6 months old):
- chora-base: <5% (well-maintained)
- Target: <10%

**Frontmatter Compliance**:
- chora-base: 100%
- Target: 100%

**Link Validity**:
- chora-base: ~98%
- Target: 100%

---

## 6. Tool Versions

| Tool | Version | Purpose |
|------|---------|---------|
| validate_docs.py | 1.0.0 | Frontmatter + link validation |
| extract_tests.py | 1.0.0 | Test extraction from How-Tos |
| docs_metrics.py | 1.0.0 | Documentation metrics tracking |

---

## 7. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [DOCUMENTATION_STANDARD.md](/static-template/DOCUMENTATION_STANDARD.md)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial ledger
