# SAP Sets Migration Guide

**Version**: 2.0.0
**Date**: 2025-11-06
**Status**: Active

---

## What Changed?

chora-base SAP sets have been redesigned with a **domain-based architecture** in v5.0.0. This provides better separation of concerns and scalability.

### Old Architecture (v1.0.0 - Deprecated)

```
minimal-entry (5 SAPs)      → Quick onboarding
recommended (10 SAPs)        → Production projects
full (18 SAPs)               → Comprehensive (but incomplete - only 18/29 SAPs!)
testing-focused (6 SAPs)     → Quality-first
mcp-server (10 SAPs)         → MCP development
react-development (10 SAPs)  → React projects
```

**Problems**:
- "full" set only included 18/29 SAPs (missing 11 SAPs including SAP-015, SAP-019, SAP-027-029)
- Overlapping SAPs between sets (80% overlap between recommended and mcp-server)
- Maintenance burden (every new SAP → update 3+ sets)
- Unclear semantics (what does "full" mean?)

### New Architecture (v2.0.0 - Current)

```
ecosystem (20 SAPs)         → Universal foundation (works everywhere)
domain-mcp (1 SAP)          → MCP server development only
domain-react (7 SAPs)       → React/Next.js development only
domain-chora-compose (2)    → chora-compose integration only

Complete project = ecosystem + domain-X
```

**Benefits**:
- Clear separation: Universal vs technology-specific
- Composable: `ecosystem + domain-mcp` = complete MCP project
- Low maintenance: New domain SAPs → new domain sets (ecosystem unchanged)
- Scalable: Easy to add `domain-python-cli`, `domain-web-api`, etc.
- No overlap: Each SAP belongs to exactly one set

---

## Migration Table

| Old Set (v1.0.0) | New Equivalent (v2.0.0) | Command | Notes |
|------------------|-------------------------|---------|-------|
| `minimal-entry` | ecosystem subset | `install-sap.py SAP-000 SAP-001 SAP-002 SAP-009 SAP-016` | Use progressive_adoption_guide.minimal_quickstart |
| `recommended` | ecosystem subset | `install-sap.py SAP-000 SAP-001 SAP-002 SAP-003 SAP-004 SAP-005 SAP-006 SAP-007 SAP-009 SAP-016` | Use progressive_adoption_guide.production_core |
| `full` | `ecosystem` | `install-sap.py --set ecosystem` | Now includes ALL 20 ecosystem SAPs (vs old 18) |
| `testing-focused` | Cherry-pick from ecosystem | `install-sap.py SAP-000 SAP-003 SAP-004 SAP-005 SAP-006 SAP-016` | Not a coherent domain |
| `mcp-server` | `ecosystem + domain-mcp` | `install-sap.py --set ecosystem --set domain-mcp` | Composable sets |
| `react-development` | `ecosystem + domain-react` | `install-sap.py --set ecosystem --set domain-react` | Composable sets |

---

## Detailed Migration Instructions

### Scenario 1: You used `minimal-entry`

**Old command**:
```bash
python scripts/install-sap.py --set minimal-entry
```

**New equivalent**:
```bash
# Option A: Install 5 minimal SAPs individually
python scripts/install-sap.py SAP-000 SAP-001 SAP-002 SAP-009 SAP-016

# Option B: Install full ecosystem (20 SAPs) for future-proofing
python scripts/install-sap.py --set ecosystem
```

**Recommendation**: Start with Option A (5 SAPs) if you only need coordination. Upgrade to ecosystem when you need more capabilities.

---

### Scenario 2: You used `recommended`

**Old command**:
```bash
python scripts/install-sap.py --set recommended
```

**New equivalent**:
```bash
# Option A: Install 10 production-core SAPs individually
python scripts/install-sap.py SAP-000 SAP-001 SAP-002 SAP-003 SAP-004 SAP-005 SAP-006 SAP-007 SAP-009 SAP-016

# Option B: Install full ecosystem (20 SAPs)
python scripts/install-sap.py --set ecosystem
```

**Recommendation**: Use Option B (full ecosystem) for production projects. You get 10 additional SAPs (SAP-008, SAP-010-013, SAP-015, SAP-019, SAP-027-029) at no extra setup cost.

---

### Scenario 3: You used `full`

**Old command**:
```bash
python scripts/install-sap.py --set full
```

**New equivalent**:
```bash
# Install full ecosystem (20 SAPs, vs old 18)
python scripts/install-sap.py --set ecosystem
```

**What you gain**: 2 additional SAPs (SAP-019 sap-self-evaluation, SAP-027 dogfooding-patterns) + SAP-015, SAP-028, SAP-029 which were missing from old "full" set.

---

### Scenario 4: You used `mcp-server`

**Old command**:
```bash
python scripts/install-sap.py --set mcp-server
```

**New equivalent**:
```bash
# Install ecosystem + MCP domain (composable sets)
python scripts/install-sap.py --set ecosystem --set domain-mcp
```

**What's different**:
- Old `mcp-server` had 10 SAPs (mixed universal + MCP-specific)
- New approach: 20 ecosystem SAPs + 1 MCP SAP = 21 total
- You get 11 additional ecosystem SAPs (SAP-008, SAP-010, SAP-011, SAP-013, SAP-015, SAP-019, SAP-027, SAP-028, SAP-029, etc.)

---

### Scenario 5: You used `react-development`

**Old command**:
```bash
python scripts/install-sap.py --set react-development
```

**New equivalent**:
```bash
# Install ecosystem + React domain (composable sets)
python scripts/install-sap.py --set ecosystem --set domain-react
```

**What's different**:
- Old `react-development` had 10 SAPs (SAP-000, 003, 004, 020-026)
- New approach: 20 ecosystem SAPs + 7 React SAPs = 27 total
- You get full infrastructure (CI/CD, Docker, memory, task tracking, etc.)

---

### Scenario 6: You used `testing-focused`

**Old command**:
```bash
python scripts/install-sap.py --set testing-focused
```

**New equivalent**:
```bash
# Cherry-pick testing SAPs from ecosystem
python scripts/install-sap.py SAP-000 SAP-003 SAP-004 SAP-005 SAP-006 SAP-016

# Or install full ecosystem
python scripts/install-sap.py --set ecosystem
```

**Rationale**: "testing-focused" wasn't a coherent domain - it was just a subset of ecosystem SAPs. Either cherry-pick the 6 SAPs you need, or install the full ecosystem.

---

## Progressive Adoption Paths

The new ecosystem set includes a `progressive_adoption_guide` for flexible adoption:

### Path 1: Minimal Quickstart (5 SAPs, 3-5 hours)

**Use case**: First-time coordination, lightweight onboarding

```bash
python scripts/install-sap.py SAP-000 SAP-001 SAP-002 SAP-009 SAP-016
```

**What you get**:
- SAP framework (SAP-000)
- Cross-repo inbox coordination (SAP-001)
- chora-base meta documentation (SAP-002)
- Agent awareness (SAP-009)
- Link validation (SAP-016)

---

### Path 2: Production Core (10 SAPs, 1-2 days)

**Use case**: Standalone projects, full development lifecycle

```bash
python scripts/install-sap.py SAP-000 SAP-001 SAP-002 SAP-003 SAP-004 SAP-005 SAP-006 SAP-007 SAP-009 SAP-016
```

**What you get**:
- All minimal quickstart SAPs
- Project scaffolding (SAP-003)
- Testing framework (SAP-004)
- CI/CD workflows (SAP-005)
- Quality gates (SAP-006)
- Documentation framework (SAP-007)

---

### Path 3: Full Ecosystem (20 SAPs, 3-5 days)

**Use case**: Advanced users, comprehensive adoption

```bash
python scripts/install-sap.py --set ecosystem
```

**What you get**:
- All production core SAPs
- Automation scripts (SAP-008)
- Memory system (SAP-010)
- Docker operations (SAP-011)
- Development lifecycle (SAP-012)
- Metrics tracking (SAP-013)
- Task tracking (SAP-015)
- SAP self-evaluation (SAP-019)
- Dogfooding patterns (SAP-027)
- Publishing automation (SAP-028)
- SAP generation (SAP-029)

---

## New Multi-Set Installation

The updated `install-sap.py` now supports **multiple `--set` arguments**:

### Example 1: MCP Server Project

```bash
# Install universal foundation + MCP-specific SAPs
python scripts/install-sap.py --set ecosystem --set domain-mcp

# What gets installed:
# - 20 ecosystem SAPs (testing, CI/CD, docs, memory, etc.)
# - 1 MCP SAP (SAP-014: FastMCP patterns)
# Total: 21 SAPs
```

---

### Example 2: React Project

```bash
# Install universal foundation + React-specific SAPs
python scripts/install-sap.py --set ecosystem --set domain-react

# What gets installed:
# - 20 ecosystem SAPs
# - 7 React SAPs (SAP-020-026: Next.js, Vitest, ESLint, state, styling, perf, a11y)
# Total: 27 SAPs
```

---

### Example 3: Content Generation with chora-compose

```bash
# Install universal foundation + chora-compose integration
python scripts/install-sap.py --set ecosystem --set domain-chora-compose

# What gets installed:
# - 20 ecosystem SAPs
# - 2 chora-compose SAPs (SAP-017, SAP-018)
# Total: 22 SAPs
```

---

### Example 4: Python CLI Tool (No Domain-Specific SAPs)

```bash
# Just ecosystem (no domain-specific needs)
python scripts/install-sap.py --set ecosystem

# Total: 20 SAPs (sufficient for Python CLI tools)
```

---

## Frequently Asked Questions

### Q1: Can I still use the old set names?

**A**: No, old sets are deprecated as of v5.0.0. The install script will show an error if you try to use `--set minimal-entry` or `--set recommended`. Use the migration table above to find the new equivalent.

You can check the `deprecated_sets` section in `sap-catalog.json` for migration paths.

---

### Q2: What if I only need a few SAPs from ecosystem?

**A**: Cherry-pick individual SAPs:

```bash
# Example: Testing infrastructure only
python scripts/install-sap.py SAP-000 SAP-004 SAP-005 SAP-006
```

The ecosystem set is designed for comprehensive adoption, but you can always install individual SAPs.

---

### Q3: Why does ecosystem include 20 SAPs but there are 29 total?

**A**: The 9 remaining SAPs are domain-specific:
- 1 MCP SAP (SAP-014)
- 7 React SAPs (SAP-020-026)
- 2 chora-compose SAPs (SAP-017-018)

These are technology-specific and only relevant if you're building MCP servers, React apps, or using chora-compose.

---

### Q4: Can I install multiple domain sets together?

**A**: Technically yes, but it's unusual:

```bash
# Both React + chora-compose (if you need content generation in React app)
python scripts/install-sap.py --set ecosystem --set domain-react --set domain-chora-compose

# Total: 20 + 7 + 2 = 29 SAPs (all SAPs!)
```

Most projects only need one domain set.

---

### Q5: How do I evaluate my SAP adoption after migration?

**A**: Use SAP-019 (sap-self-evaluation):

```bash
# Quick check (30 seconds)
python scripts/sap-evaluator.py --quick

# Deep dive on specific SAP
python scripts/sap-evaluator.py --deep SAP-004

# Strategic roadmap generation
python scripts/sap-evaluator.py --strategic --output roadmap.yaml
```

SAP-019 is included in the ecosystem set and helps track adoption maturity.

---

## Checking Current Sets

To see available sets and their contents:

```bash
# List all SAP sets
python scripts/install-sap.py --list-sets

# Expected output:
# ecosystem (20 SAPs)
# domain-mcp (1 SAP)
# domain-react (7 SAPs)
# domain-chora-compose (2 SAPs)
```

---

## Rollback Instructions

If you need to rollback to the old set structure:

```bash
# 1. Checkout previous version of sap-catalog.json
git checkout v4.9.0 -- sap-catalog.json

# 2. Checkout previous version of install-sap.py
git checkout v4.9.0 -- scripts/install-sap.py

# 3. Use old set names
python scripts/install-sap.py --set recommended
```

**Warning**: This is not recommended. The old "full" set was incomplete (only 18/29 SAPs).

---

## Support

If you encounter issues during migration:

1. Check the [sap-catalog.json](../../sap-catalog.json) `deprecated_sets` section for migration paths
2. Run `python scripts/install-sap.py --list-sets` to see available sets
3. File an issue: [chora-base/issues](https://github.com/liminalcommons/chora-base/issues)

---

## Version History

- **2.0.0** (2025-11-06): Domain-based architecture
  - New sets: ecosystem, domain-mcp, domain-react, domain-chora-compose
  - Deprecated: minimal-entry, recommended, full, testing-focused, mcp-server, react-development
  - Multi-set installation support (`--set ecosystem --set domain-mcp`)
- **1.0.0** (2025-11-02): Original tier-based architecture (deprecated)
