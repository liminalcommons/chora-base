# Standard SAP Sets Reference

**Quick Reference**: Comparison of all 5 standard SAP sets available in chora-base.

**Last Updated**: 2025-10-29
**Catalog Version**: 4.1.0

---

## Quick Comparison Table

| Set | SAPs | Tokens | Time | Best For |
|-----|------|--------|------|----------|
| **minimal-entry** | 5 | ~29k | 3-5 hours | First-time adoption, ecosystem coordination |
| **recommended** | 10 | ~60k | 1-2 days | Production-ready projects, core workflow |
| **testing-focused** | 6 | ~35k | 4-6 hours | Quality-first development, QA contributors |
| **mcp-server** | 10 | ~55k | 1 day | MCP server development with FastMCP |
| **full** | 18 | ~100k | 2-4 weeks | Advanced users, comprehensive coverage |

---

## 1. minimal-entry

### Overview
**Name**: Minimal Ecosystem Entry
**Version**: 1.0.0
**SAPs**: 5
**Tokens**: ~29,000 (71% reduction from full)
**Time**: 3-5 hours

### What You Get

| SAP | Name | Purpose |
|-----|------|---------|
| SAP-000 | sap-framework | Core SAP protocols and framework |
| SAP-001 | inbox-coordination | Cross-repo inbox protocol |
| SAP-009 | agent-awareness | AGENTS.md for agent discoverability |
| SAP-016 | link-validation | Link validation tooling |
| SAP-002 | chora-base-meta | Chora-base documentation |

### Capabilities

- **SAP Framework & Protocols** (SAP-000) - Understand how SAPs work
- **Cross-repo Inbox Coordination** (SAP-001) - Coordinate with ecosystem repos
- **Agent Awareness via AGENTS.md** (SAP-009) - Make repo discoverable to AI agents
- **Link Validation** (SAP-016) - Maintain documentation quality
- **Chora-base Meta Documentation** (SAP-002) - Understand chora-base itself

### Use Cases

- ✅ First-time chora ecosystem adoption
- ✅ Contributing to ecosystem repos via inbox protocol
- ✅ Cross-repo coordination
- ✅ Lightweight onboarding before full adoption
- ✅ Agents learning chora-base patterns

### Installation

```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Next Steps

1. Add domain-specific SAP:
   - SAP-004 for testing
   - SAP-014 for MCP development
2. Upgrade to `recommended` set for full productivity
3. Customize AGENTS.md for your project
4. Create capabilities file in inbox/CAPABILITIES/

### Warnings

⚠️ **SAP-001 (inbox-coordination) is in Pilot status** - May undergo changes before reaching Active status

---

## 2. recommended

### Overview
**Name**: Recommended Foundation
**Version**: 1.0.0
**SAPs**: 10
**Tokens**: ~60,000
**Time**: 1-2 days

### What You Get

| SAP | Name | Purpose |
|-----|------|---------|
| SAP-000 | sap-framework | Core framework |
| SAP-001 | inbox-coordination | Cross-repo protocol |
| SAP-002 | chora-base-meta | Meta documentation |
| SAP-003 | project-scaffolding | Copier templates |
| SAP-004 | testing-framework | pytest with 85%+ coverage |
| SAP-005 | ci-cd-workflows | GitHub Actions automation |
| SAP-006 | quality-gates | ruff + mypy pre-commit hooks |
| SAP-007 | documentation-structure | Diátaxis framework |
| SAP-009 | agent-awareness | AGENTS.md |
| SAP-016 | link-validation | Link validation |

### Capabilities

- **All minimal-entry capabilities**, plus:
- **Project Scaffolding with Copier** (SAP-003) - Template generation
- **Testing Framework** (SAP-004) - pytest patterns, 85%+ coverage targets
- **CI/CD Workflows** (SAP-005) - GitHub Actions for automated testing/deployment
- **Quality Gates** (SAP-006) - Pre-commit hooks with ruff and mypy
- **Documentation Framework** (SAP-007) - 4-domain Diátaxis structure

### Use Cases

- ✅ Standalone projects built on chora-base
- ✅ Full development lifecycle support
- ✅ Production-ready projects
- ✅ Teams wanting standardized workflows
- ✅ Projects requiring CI/CD and quality gates

### Installation

```bash
python scripts/install-sap.py --set recommended --source /path/to/chora-base
```

### Next Steps

1. Add advanced capabilities:
   - SAP-010 (memory system with A-MEM)
   - SAP-011 (docker operations)
2. Add technology-specific SAPs:
   - SAP-014 (MCP server development)
3. Customize CI/CD workflows for your tech stack
4. Configure pre-commit hooks for your project

### Warnings

⚠️ **SAP-001 (inbox-coordination) is in Pilot status**

---

## 3. testing-focused

### Overview
**Name**: Testing & Quality Focused
**Version**: 1.0.0
**SAPs**: 6
**Tokens**: ~35,000
**Time**: 4-6 hours

### What You Get

| SAP | Name | Purpose |
|-----|------|---------|
| SAP-000 | sap-framework | Core framework |
| SAP-003 | project-scaffolding | Copier templates |
| SAP-004 | testing-framework | pytest with 85%+ coverage |
| SAP-005 | ci-cd-workflows | GitHub Actions |
| SAP-006 | quality-gates | ruff + mypy pre-commit |
| SAP-016 | link-validation | Link validation |

### Capabilities

- **SAP Framework** (SAP-000)
- **Project Scaffolding** (SAP-003) - Generate test structures
- **Testing Framework** (SAP-004) - pytest patterns, 85%+ coverage
- **CI/CD Workflows** (SAP-005) - Automated test runs
- **Quality Gates** (SAP-006) - Pre-commit type checking and linting
- **Link Validation** (SAP-016) - Documentation quality

### Use Cases

- ✅ Projects prioritizing test coverage and quality
- ✅ CI/CD-heavy workflows
- ✅ Quality-first development (TDD/BDD)
- ✅ QA-focused contributors
- ✅ Teams requiring 85%+ test coverage

### Installation

```bash
python scripts/install-sap.py --set testing-focused --source /path/to/chora-base
```

### Next Steps

1. Add documentation framework (SAP-007) for quality docs
2. Add development lifecycle (SAP-012) for BDD/TDD workflows
3. Consider metrics tracking (SAP-013) for quality metrics
4. Add agent awareness (SAP-009) if working in ecosystem

### Warnings

*None*

### Key Difference from recommended

**Excludes**:
- SAP-001 (inbox coordination) - Not needed for QA-focused work
- SAP-002 (chora-base meta) - Not essential for testing focus
- SAP-007 (documentation) - Can add later if needed
- SAP-009 (agent awareness) - Not needed for testing focus

**Result**: Leaner set focused purely on quality and testing.

---

## 4. mcp-server

### Overview
**Name**: MCP Server Development
**Version**: 1.0.0
**SAPs**: 10
**Tokens**: ~55,000
**Time**: 1 day

### What You Get

| SAP | Name | Purpose |
|-----|------|---------|
| SAP-000 | sap-framework | Core framework |
| SAP-003 | project-scaffolding | Copier templates |
| SAP-004 | testing-framework | pytest patterns |
| SAP-005 | ci-cd-workflows | GitHub Actions |
| SAP-006 | quality-gates | ruff + mypy |
| SAP-007 | documentation-structure | Diátaxis docs |
| SAP-009 | agent-awareness | AGENTS.md |
| SAP-012 | development-lifecycle | DDD/BDD/TDD patterns |
| SAP-014 | mcp-server-development | FastMCP patterns |
| SAP-016 | link-validation | Link validation |

### Capabilities

- **All testing-focused capabilities**, plus:
- **Documentation Framework** (SAP-007) - For MCP server docs
- **Agent Awareness** (SAP-009) - AGENTS.md for MCP discoverability
- **Development Lifecycle** (SAP-012) - DDD/BDD/TDD workflows
- **MCP Server Development** (SAP-014) - FastMCP templates and patterns

### Use Cases

- ✅ Building MCP servers with FastMCP
- ✅ Creating Claude Desktop integrations
- ✅ Developing custom MCP tools and resources
- ✅ MCP-first projects
- ✅ Contributing to Claude ecosystem

### Installation

```bash
python scripts/install-sap.py --set mcp-server --source /path/to/chora-base
```

### Next Steps

1. Add chora-compose integration (SAP-017/018) for content generation
2. Add automation scripts (SAP-008) for MCP deployment
3. Consider memory system (SAP-010) for stateful MCP servers
4. Consider docker operations (SAP-011) for containerized servers

### Warnings

*None*

### Key Difference from recommended

**Includes**:
- SAP-012 (development lifecycle) - Essential for MCP architecture
- SAP-014 (MCP server development) - Core MCP patterns

**Excludes**:
- SAP-001 (inbox coordination) - Not needed for MCP focus
- SAP-002 (chora-base meta) - Not essential for MCP

**Result**: Tailored specifically for Model Context Protocol development.

---

## 5. full

### Overview
**Name**: Complete Capability Suite
**Version**: 1.0.0
**SAPs**: 18 (all SAPs)
**Tokens**: ~100,000
**Time**: 2-4 weeks

### What You Get

**All 18 SAPs**:

| SAP | Name | Category |
|-----|------|----------|
| SAP-000 | sap-framework | Meta |
| SAP-001 | inbox-coordination | Meta |
| SAP-002 | chora-base-meta | Meta |
| SAP-003 | project-scaffolding | Foundation |
| SAP-004 | testing-framework | Quality |
| SAP-005 | ci-cd-workflows | Quality |
| SAP-006 | quality-gates | Quality |
| SAP-007 | documentation-structure | Documentation |
| SAP-008 | automation-scripts | Automation |
| SAP-009 | agent-awareness | Meta |
| SAP-010 | memory-system | Advanced |
| SAP-011 | docker-operations | Infrastructure |
| SAP-012 | development-lifecycle | Process |
| SAP-013 | metrics-tracking | Analytics |
| SAP-014 | mcp-server-development | Technology |
| SAP-016 | link-validation | Quality |
| SAP-017 | chora-compose-integration | Ecosystem |
| SAP-018 | chora-compose-meta | Ecosystem |

### Capabilities

- **All recommended capabilities**, plus:
- **Automation Scripts with justfile** (SAP-008)
- **Memory System with A-MEM** (SAP-010)
- **Docker Operations** (SAP-011) - Multi-stage builds
- **Development Lifecycle** (SAP-012) - DDD/BDD/TDD
- **Metrics Tracking** (SAP-013) - ROI calculator
- **MCP Server Development** (SAP-014) - FastMCP patterns
- **chora-compose Integration** (SAP-017, SAP-018) - Content generation

### Use Cases

- ✅ Advanced users wanting all capabilities
- ✅ Organizations standardizing on chora-base
- ✅ Reference implementations
- ✅ chora-base contributors
- ✅ Comprehensive project templates

### Installation

```bash
python scripts/install-sap.py --set full --source /path/to/chora-base
```

### Next Steps

- No additional SAPs needed (you have all 18!)
- Customize capabilities for your domain
- Consider contributing new SAPs back to chora-base
- Create custom sets for specific use cases

### Warnings

⚠️ **SAP-001 (inbox-coordination) is in Pilot status**
⚠️ **Large token footprint** - Consider progressive adoption (start with minimal-entry, upgrade to recommended, then full)

---

## Choosing the Right Set

### Decision Tree

```
┌─ New to chora-base?
│  └─ Start with: minimal-entry
│     ├─ Need testing? → Upgrade to testing-focused
│     ├─ Building MCP? → Upgrade to mcp-server
│     └─ Production project? → Upgrade to recommended
│
├─ QA/Testing focus?
│  └─ Use: testing-focused
│
├─ Building MCP servers?
│  └─ Use: mcp-server
│
├─ Production project?
│  └─ Use: recommended
│     └─ Want everything? → Upgrade to full
│
└─ Advanced user / Contributor?
   └─ Use: full
```

### By Use Case

| Use Case | Recommended Set |
|----------|----------------|
| First-time adoption | minimal-entry |
| Ecosystem coordination | minimal-entry |
| QA contributor | testing-focused |
| MCP server development | mcp-server |
| Production web app | recommended |
| Production library | recommended |
| Organization standardization | recommended or full |
| Reference implementation | full |
| chora-base contributor | full |

### By Time Available

| Time Budget | Recommended Set |
|-------------|----------------|
| 3-5 hours | minimal-entry |
| 4-6 hours | testing-focused |
| 1 day | recommended or mcp-server |
| 1-2 days | recommended |
| 2-4 weeks | full |

### By Token Budget

| Token Budget | Recommended Set |
|--------------|----------------|
| ~30k tokens | minimal-entry |
| ~35k tokens | testing-focused |
| ~55k tokens | mcp-server |
| ~60k tokens | recommended |
| ~100k tokens | full |

---

## Progressive Adoption

You can install sets progressively. The install script automatically skips already-installed SAPs:

### Path 1: Minimal → Recommended → Full

```bash
# Week 1: Get started (3-5 hours)
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base

# Week 2: Production workflow (1-2 days)
python scripts/install-sap.py --set recommended --source /path/to/chora-base
# Installs 5 additional SAPs (SAP-003, 004, 005, 006, 007)

# Month 2: Complete coverage (2-4 weeks)
python scripts/install-sap.py --set full --source /path/to/chora-base
# Installs remaining 8 SAPs
```

### Path 2: Testing → MCP → Full

```bash
# Week 1: Testing foundation (4-6 hours)
python scripts/install-sap.py --set testing-focused --source /path/to/chora-base

# Week 2: Add MCP capabilities (1 day)
python scripts/install-sap.py --set mcp-server --source /path/to/chora-base
# Installs 4 additional SAPs (SAP-007, 009, 012, 014)

# Month 2: Complete (2-4 weeks)
python scripts/install-sap.py --set full --source /path/to/chora-base
# Installs remaining 8 SAPs
```

### Path 3: Minimal → Custom

```bash
# Week 1: Foundation
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base

# Week 2+: Add individual SAPs as needed
python scripts/install-sap.py SAP-004 --source /path/to/chora-base  # Testing
python scripts/install-sap.py SAP-007 --source /path/to/chora-base  # Docs
python scripts/install-sap.py SAP-014 --source /path/to/chora-base  # MCP
```

---

## Set Composition Comparison

### Venn Diagram (Conceptual)

```
┌─────────────────────────────────────┐
│ full (18 SAPs)                      │
│ ┌─────────────────────────────────┐ │
│ │ recommended (10 SAPs)           │ │
│ │ ┌───────────────────────────┐   │ │
│ │ │ minimal-entry (5 SAPs)    │   │ │
│ │ │ • SAP-000, 001, 002       │   │ │
│ │ │ • SAP-009, 016            │   │ │
│ │ └───────────────────────────┘   │ │
│ │ + SAP-003, 004, 005, 006, 007   │ │
│ └─────────────────────────────────┘ │
│ + SAP-008, 010, 011, 012, 013,      │
│   014, 017, 018                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ testing-focused (6 SAPs)            │
│ • SAP-000                           │
│ • SAP-003, 004, 005, 006           │
│ • SAP-016                           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ mcp-server (10 SAPs)                │
│ • SAP-000                           │
│ • SAP-003, 004, 005, 006, 007      │
│ • SAP-009, 012, 014, 016           │
└─────────────────────────────────────┘
```

### SAP Distribution

| SAP | minimal | recommended | testing | mcp | full |
|-----|---------|-------------|---------|-----|------|
| 000 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 001 | ✓ | ✓ |  |  | ✓ |
| 002 | ✓ | ✓ |  |  | ✓ |
| 003 |  | ✓ | ✓ | ✓ | ✓ |
| 004 |  | ✓ | ✓ | ✓ | ✓ |
| 005 |  | ✓ | ✓ | ✓ | ✓ |
| 006 |  | ✓ | ✓ | ✓ | ✓ |
| 007 |  | ✓ |  | ✓ | ✓ |
| 008 |  |  |  |  | ✓ |
| 009 | ✓ | ✓ |  | ✓ | ✓ |
| 010 |  |  |  |  | ✓ |
| 011 |  |  |  |  | ✓ |
| 012 |  |  |  | ✓ | ✓ |
| 013 |  |  |  |  | ✓ |
| 014 |  |  |  | ✓ | ✓ |
| 016 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 017 |  |  |  |  | ✓ |
| 018 |  |  |  |  | ✓ |

---

## Related Documentation

- [Install SAP Set](../how-to/install-sap-set.md) - Step-by-step installation guide
- [Create Custom SAP Sets](../how-to/create-custom-sap-sets.md) - Define your own sets
- [Agent Onboarding Guide](../guides/agent-onboarding-chora-base.md) - Complete onboarding
- [SAP Catalog](../../sap-catalog.json) - Machine-readable catalog

---

## Summary

**5 Standard Sets**:
1. **minimal-entry** - 5 SAPs, 3-5 hours, ecosystem entry
2. **recommended** - 10 SAPs, 1-2 days, production projects
3. **testing-focused** - 6 SAPs, 4-6 hours, quality-first
4. **mcp-server** - 10 SAPs, 1 day, MCP development
5. **full** - 18 SAPs, 2-4 weeks, comprehensive

**Installation**:
```bash
python scripts/install-sap.py --set <set-name> --source /path/to/chora-base
```

**Recommendation**: Start with **minimal-entry**, then progressively upgrade based on needs.
