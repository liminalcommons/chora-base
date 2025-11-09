# Traceability Ledger: Documentation Framework

**SAP ID**: SAP-007
**Current Version**: 1.1.0
**Status**: Pilot
**Last Updated**: 2025-11-09

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
| 1.1.0 | 2025-11-09 | MINOR | Added Level 3 enforcement layer (COORD-2025-011): validation script template, pre-commit hook template, decision tree template, SAP-031 integration |
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
| **validate-sap-007-structure.py** | **1.0.0** | **SAP-007 structure enforcement (NEW v1.1.0)** |
| **sap-007-check.sh** | **1.0.0** | **Pre-commit hook for SAP-007 (NEW v1.1.0)** |

---

## 7. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [AGENTS.md](AGENTS.md) - Agent workflows and patterns
- [templates/validate-sap-007-structure.py](templates/validate-sap-007-structure.py) - Structure validation script (NEW v1.1.0)
- [templates/sap-007-check.sh](templates/sap-007-check.sh) - Pre-commit hook (NEW v1.1.0)
- [decision-tree-template.md](decision-tree-template.md) - Doc categorization guide (NEW v1.1.0)
- [DOCUMENTATION_STANDARD.md](/static-template/DOCUMENTATION_STANDARD.md)
- [SAP-031 (Enforcement)](../discoverability-based-enforcement/) - Enforcement methodology used in v1.1.0

---

## 8. SAP-031 Integration (NEW v1.1.0)

**Enforcement Architecture**: SAP-007 v1.1.0 implements SAP-031 (Discoverability-Based Enforcement) pattern:

**Layer 1 (Discoverability)**:
- Decision tree template added to AGENTS.md files
- Patterns placed where agents naturally look during workflow
- Prevention contribution: ~70%

**Layer 2 (Pre-Commit Validation)**:
- `validate-sap-007-structure.py` checks root directory policy (≤8 files)
- `sap-007-check.sh` blocks commits that violate structure
- Prevention contribution: ~20%

**Layer 4 (Documentation)**:
- Workflow 4 in AGENTS.md documents enforcement setup
- Decision tree template guides categorization
- Support layer

**Validation Case**: SAP-007 serves as **second reference implementation** of SAP-031 (after cross-platform enforcement in SAP-030).

**Lessons Learned (from chora-workspace pilot)**:
- ✅ L2 (structure) without L3 (enforcement) degrades within days
- ✅ Pre-commit hooks prevent 90%+ violations
- ✅ Decision trees reduce categorization errors
- ✅ Template-driven adoption faster than manual implementation

See: [SAP-031 ledger.md](../discoverability-based-enforcement/ledger.md) for cross-SAP enforcement metrics

---

## 9. Adoption Feedback (v1.1.0)

**chora-workspace** (2025-11-09):
- **Scenario**: L2 adoption (41→8 root files), but violations occurred within hours
- **Solution**: Implemented enforcement layer (validation + pre-commit hook)
- **Result**: 0 violations after hook installation
- **Feedback**: "L3 enforcement should be mandatory, not optional"
- **Contribution**: Submitted COORD-2025-011 requesting enforcement templates in chora-base

**Impact**: COORD-2025-011 accepted → SAP-007 v1.1.0 includes enforcement templates

---

**Version History**:
- **1.1.0** (2025-11-09): Added enforcement layer (COORD-2025-011), SAP-031 integration, pilot status
- **1.0.0** (2025-10-28): Initial ledger
