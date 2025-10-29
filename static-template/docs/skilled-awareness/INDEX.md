# SAP Index

**Project**: [Your Project Name]
**Last Updated**: [Date]
**Total SAPs**: 1 (base installation)

---

## Installed SAPs

| SAP ID | Name | Version | Status | Adopted | Notes |
|--------|------|---------|--------|---------|-------|
| SAP-000 | SAP Framework | 1.0.0 | Active | [Date] | Core framework (always included) |

---

## Available SAPs (from chora-base)

To install additional SAPs, see the [chora-base SAP catalog](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/INDEX.md).

**Core Infrastructure**:
- SAP-001: Inbox Protocol
- SAP-003: Project Bootstrap
- SAP-004: Testing Framework
- SAP-005: CI/CD Workflows
- SAP-006: Quality Gates

**Development & Documentation**:
- SAP-007: Documentation Framework
- SAP-008: Automation Scripts
- SAP-009: Agent Awareness
- SAP-012: Development Lifecycle

**Advanced Capabilities**:
- SAP-010: Memory System
- SAP-011: Docker Operations
- SAP-013: Metrics Tracking

**MCP-Specific** (Wave 3+):
- SAP-014: MCP Server Development (planned)

---

## Installation Instructions

### Installing a SAP from chora-base

**Option 1: Manual Installation**
1. Copy SAP directory from chora-base:
   ```bash
   cp -r /path/to/chora-base/docs/skilled-awareness/[sap-name] \
         docs/skilled-awareness/
   ```

2. Copy any system files (if SAP includes them):
   ```bash
   # Example for SAP-004 (Testing)
   cp -r /path/to/chora-base/static-template/tests tests/
   ```

3. Update this INDEX.md with new SAP entry

4. Update the SAP's ledger.md with your adoption

**Option 2: Automated Installation (v4.0+)**
```bash
# Future: SAP installation script
python scripts/install-sap.py SAP-004
```

### Creating a Project-Specific SAP

1. Use [document-templates.md](document-templates.md) to create 5 artifacts
2. Place in `docs/skilled-awareness/[your-sap-name]/`
3. Update this INDEX.md
4. Follow [sap-framework/adoption-blueprint.md](sap-framework/adoption-blueprint.md) for guidance

---

## SAP Status Definitions

- **Active**: Currently in use and maintained
- **Planned**: Identified for future adoption
- **Deprecated**: No longer recommended, migration path available
- **Archived**: Historical, not actively used

---

## Related Documentation

- [SAP Framework](sap-framework/) - SAP-000 documentation
- [Document Templates](document-templates.md) - Templates for creating SAPs
- [Chora-Base SAP Catalog](https://github.com/liminalcommons/chora-base/blob/main/docs/skilled-awareness/INDEX.md) - All available SAPs

---

**Index Version**: 1.0
**Created**: [Date]
**Owner**: [Your Team]
