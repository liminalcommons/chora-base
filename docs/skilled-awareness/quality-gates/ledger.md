# Traceability Ledger: Quality Gates

**SAP ID**: SAP-006
**Current Version**: 1.0.0
**Status**: Draft (Phase 2)
**Last Updated**: 2025-10-28

---

## 1. Projects Using Quality Gates

| Project | Hooks Installed | Pre-commit Pass Rate | Last Updated |
|---------|-----------------|----------------------|--------------|
| chora-base | ✅ All 7 hooks | ~98% | 2025-10-28 |
| chora-compose | ✅ All 7 hooks | ~95% | 2025-10-20 |
| mcp-n8n | ✅ All 7 hooks | ~93% | 2025-10-22 |

---

## 2. Version History

| Version | Release Date | Type | Changes |
|---------|--------------|------|---------|
| 1.0.0 | 2025-10-28 | MAJOR | Initial SAP-006 release: 7 hooks documented, ruff-based |

---

## 3. Hook Performance Tracking

| Hook | Avg Duration | Status |
|------|--------------|--------|
| check-yaml | <0.1s | ✅ Active |
| trailing-whitespace | <0.1s | ✅ Active |
| ruff (check) | ~0.5s | ✅ Active |
| ruff-format | ~0.3s | ✅ Active |
| mypy | ~1-3s | ✅ Active |

**Total**: <5 seconds per commit

---

## 4. Tool Versions

| Tool | Version | Purpose |
|------|---------|---------|
| pre-commit | 4.0.1 | Hook framework |
| ruff | 0.7.0 | Linter + formatter |
| mypy | 1.11.0 | Type checker |
| black | 24.10.0 | Backup formatter |

---

## 5. Related Documents

- [protocol-spec.md](protocol-spec.md) - Technical contract
- [.pre-commit-config.yaml](/static-template/.pre-commit-config.yaml)

---

**Version History**:
- **1.0.0** (2025-10-28): Initial ledger
