# Skilled Awareness (SAP Framework)

**Purpose**: Meta-layer of cross-cutting capability packages

**Audience**: All roles (developers, PMs, users, AI agents, external adopters)

---

## What's Here

This directory contains the **SAP (Skilled Awareness Package) Framework**:

- **[sap-framework/](sap-framework/)** - SAP-000: The framework itself
  - capability-charter.md - SAP framework overview
  - protocol-spec.md - SAP protocol specification
  - awareness-guide.md - How to use SAPs
  - adoption-blueprint.md - How to create new SAPs
  - ledger.md - SAP adoption tracking

- **[INDEX.md](INDEX.md)** - Central registry of all SAPs (14 total)

- **[document-templates.md](document-templates.md)** - Templates for SAP artifacts

- **Capability SAPs** - 13 additional SAPs (see INDEX.md for complete list)
  - Each SAP has the same 5 artifacts
  - Each SAP references content across all 4 domains

---

## What is a SAP?

A **Skilled Awareness Package (SAP)** is a portable capability package containing:

### The 5 Artifacts

1. **capability-charter.md** - High-level overview, business value
2. **protocol-spec.md** - Technical contracts, inputs/outputs, guarantees
3. **awareness-guide.md** - How to use, references to all 4 domains
4. **adoption-blueprint.md** - Step-by-step installation instructions
5. **ledger.md** - Adoption tracking (who uses this SAP, when adopted)

### Cross-Domain References

SAPs are **meta-layer** - they reference content in all other domains:

**Example: SAP-004 (Testing Framework)** references:
- `dev-docs/workflows/TDD_WORKFLOW.md` - Development process
- `project-docs/metrics/test-coverage.md` - Quality tracking
- `user-docs/reference/testing-conventions.md` - User-facing conventions
- `tests/` - Actual test suite (system code)

This makes SAPs **cross-cutting** - they touch all aspects of a capability.

---

## Current SAPs (v3.3.0)

See [INDEX.md](INDEX.md) for the complete registry. Highlights:

**Core Framework**:
- **SAP-000**: SAP Framework (this directory)
- **SAP-002**: Chora-Base (the project itself)

**Development Infrastructure**:
- **SAP-001**: Inbox Protocol
- **SAP-003**: Project Bootstrap
- **SAP-004**: Testing Framework
- **SAP-005**: CI/CD Workflows
- **SAP-006**: Quality Gates
- **SAP-012**: Development Lifecycle

**Documentation & Tooling**:
- **SAP-007**: Documentation Framework
- **SAP-008**: Automation Scripts
- **SAP-009**: Agent Awareness

**Advanced Capabilities**:
- **SAP-010**: Memory System
- **SAP-011**: Docker Operations
- **SAP-013**: Metrics Tracking

---

## How to Use SAPs

### For Adopters (Installing a SAP)

1. **Browse** [INDEX.md](INDEX.md) to find desired capability
2. **Read** the SAP's capability-charter.md to understand business value
3. **Follow** the SAP's adoption-blueprint.md for installation steps
4. **Reference** the SAP's awareness-guide.md during use
5. **Record** your adoption in the SAP's ledger.md

### For Contributors (Creating a SAP)

1. **Identify** a reusable capability pattern
2. **Use** [document-templates.md](document-templates.md) to create 5 artifacts
3. **Follow** [sap-framework/adoption-blueprint.md](sap-framework/adoption-blueprint.md) for SAP creation process
4. **Update** [INDEX.md](INDEX.md) with new SAP entry
5. **Cross-reference** content in all 4 domains from awareness-guide.md

### For Maintainers (Updating a SAP)

1. **Update** relevant artifact(s) in the SAP directory
2. **Increment** version in protocol-spec.md
3. **Document** changes in capability-charter.md
4. **Update** cross-references in awareness-guide.md if paths changed
5. **Announce** update (if breaking changes)

---

## SAP Anatomy Deep Dive

### 1. capability-charter.md

**Purpose**: High-level overview for non-technical stakeholders

**Contains**:
- What the capability is
- Why it exists (business value)
- Who should use it
- Dependencies on other SAPs
- Version history

**Audience**: All roles, especially decision-makers

---

### 2. protocol-spec.md

**Purpose**: Technical contract definition

**Contains**:
- Inputs (what the capability requires)
- Outputs (what the capability delivers)
- Guarantees (what the capability promises)
- Constraints (limitations and boundaries)
- API specifications (if applicable)

**Audience**: Technical implementers, integrators

---

### 3. awareness-guide.md

**Purpose**: Comprehensive usage guide

**Contains**:
- How to use the capability
- Cross-references to all 4 domains:
  - dev-docs/ (development workflows)
  - project-docs/ (metrics, integration)
  - user-docs/ (end-user guides)
  - System files (code, tests, scripts)
- Examples and demonstrations
- Common patterns and anti-patterns

**Audience**: All roles during active use

---

### 4. adoption-blueprint.md

**Purpose**: Step-by-step installation guide

**Contains**:
- Prerequisites
- Installation steps
- Validation checklist
- Troubleshooting
- Next steps after adoption

**Audience**: Teams installing the SAP

---

### 5. ledger.md

**Purpose**: Track adoption across projects/teams

**Contains**:
- Table of adoptions (who, when, version)
- Adoption notes and feedback
- Migration history (version upgrades)

**Audience**: Framework maintainers, analytics

---

## Relationship to 4-Domain Architecture

**SAPs sit ABOVE the 4 domains**:

```
┌─────────────────────────────────────────┐
│    skilled-awareness/ (Meta-Layer)      │
│    - SAPs reference all domains         │
└─────────────────────────────────────────┘
               ↓ references
┌──────────────┬──────────────┬──────────────┐
│  dev-docs/   │ project-docs/│  user-docs/  │
│  (Process)   │ (Lifecycle)  │  (Product)   │
└──────────────┴──────────────┴──────────────┘
               ↓ references
┌─────────────────────────────────────────┐
│    System (src/, tests/, scripts/)      │
└─────────────────────────────────────────┘
```

**Example Flow**:

User wants to adopt **SAP-004 (Testing Framework)**:

1. **Read**: `skilled-awareness/testing-framework/capability-charter.md` → Understand value
2. **Follow**: `skilled-awareness/testing-framework/adoption-blueprint.md` → Install steps
3. **Reference during use**:
   - `dev-docs/workflows/TDD_WORKFLOW.md` → How to practice TDD
   - `user-docs/reference/testing-conventions.md` → Test structure spec
   - `tests/` → Actual test examples
   - `project-docs/metrics/` → Track test coverage

The SAP ties it all together.

---

## Not Here

**SAPs are NOT**:
- General documentation (that goes in other domains)
- Implementation code (that goes in src/, tests/, scripts/)
- Project-specific content (SAPs are reusable patterns)

**SAPs ARE**:
- Reusable capability packages
- Cross-cutting concerns
- Meta-documentation that references other domains
- Portable across projects

---

## Related Documentation

**Other Domains**:
- [Developer Documentation](../dev-docs/) - Development processes
- [Project Documentation](../project-docs/) - Project lifecycle
- [User Documentation](../user-docs/) - Product usage

**Root Documentation**:
- [Architecture](../ARCHITECTURE.md) - 4-domain model explained
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - SAP protocol spec (root)
- [AGENTS.md](../../AGENTS.md) - Agent guidance

**SAP Framework**:
- [sap-framework/](sap-framework/) - SAP-000 (the framework itself)
- [INDEX.md](INDEX.md) - Complete SAP registry
- [document-templates.md](document-templates.md) - SAP templates

---

## Future Evolution

**Wave 2**: SAP Content Audit & Enhancement
- Ensure all SAPs reference actual implementation files
- Add missing cross-domain references
- Enhance awareness-guides with examples

**Wave 3+**: Additional SAPs
- SAP-014: MCP Server Development (MCP-specific patterns)
- SAP-015: Documentation Migration (from Wave 1 learnings)
- SAP-016: Link Validation & Reference Management
- More SAPs as patterns emerge

**v4.0**: SAP Installation Tooling
- `install-sap.py` script for automated installation
- SAP catalog for discovery
- Dependency resolution

---

## Meta-Demonstration

Wave 1 demonstrates SAP awareness:

**This migration created**:
- **dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md** - Process
- **project-docs/sprints/wave-1-sprint-plan.md** - Planning
- **user-docs/explanation/benefits-of-chora-base.md** - User value

**A future SAP-015 (Documentation Migration) would**:
- Reference the workflow in its awareness-guide.md
- Point to Wave 1 sprint as example in capability-charter.md
- Include migration scripts in protocol-spec.md
- Track adoptions in ledger.md

This is how SAPs capture emergent patterns as reusable capabilities.

---

## Contributing New SAPs

See [sap-framework/adoption-blueprint.md](sap-framework/adoption-blueprint.md) for:
- When to create a new SAP
- How to structure the 5 artifacts
- How to integrate with INDEX.md
- How to version and maintain SAPs

---

**Domain Version**: 1.0 (Wave 1)
**Last Updated**: 2025-10-28
**Status**: Active
**Total SAPs**: 14 (v3.3.0)
