# Traceability Ledger: CI/CD Workflows

**SAP ID**: SAP-005
**Current Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Projects Using CI/CD Workflows

| Project | Workflows | Success Rate | Last Updated | Notes |
|---------|-----------|--------------|--------------|-------|
| chora-base | 10/10 | ~98% | 2025-10-28 | All workflows active |
| chora-compose | 10/10 | ~95% | 2025-10-20 | Occasional coverage failures |
| mcp-n8n | 10/10 | ~93% | 2025-10-22 | Working toward higher success rate |

---

## 2. Version History

| Version | Release Date | Type | Changes |
|---------|--------------|------|---------|
| 1.0.0 | 2025-10-28 | MAJOR | Initial SAP-005 release: 10 workflows documented |

---

## 3. Workflow Performance Tracking

| Workflow | Avg Duration | Success Rate | Status |
|----------|--------------|--------------|--------|
| test.yml | ~2-3 min | 96% | ✅ Active |
| lint.yml | ~1-2 min | 98% | ✅ Active |
| smoke.yml | ~30-60s | 99% | ✅ Active |
| codeql.yml | ~3-5 min | 100% | ✅ Active |
| docs-quality.yml | ~1-2 min | 95% | ✅ Active |

---

## 4. Known Issues

**Issue**: test.yml occasionally fails due to cache timeout
- **Severity**: Low
- **Workaround**: Re-run workflow
- **Fix**: Monitor cache performance

---

## 5. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [.github/workflows/](/static-template/.github/workflows/) - Workflow files

---

**Version History**:
- **1.0.0** (2025-10-28): Initial ledger
