# SAP-000: SAP Framework

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-10

---

## What Is It?

The **SAP (Skilled Awareness Package) Framework** is the foundational meta-infrastructure that defines how all capabilities are packaged, documented, and distributed within the chora-base ecosystem. It establishes standardized structures, documentation patterns, and quality requirements that ensure every capability is discoverable, adoptable, and maintainable by both humans and AI agents.

Think of SAP-000 as the "constitution" for all other SAPs. Just as a constitution defines how laws are created and enforced, SAP-000 defines how capabilities are structured and validated. It provides:

- **Structural Standards**: The 5 required artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- **Documentation Patterns**: README.md 9-section format, Quick Reference format, AGENTS.md/CLAUDE.md conventions
- **Quality Requirements**: Validation compliance, progressive loading, version consistency, discoverability
- **Lifecycle Governance**: Status promotion gates (Draft → Pilot → Active), deprecation policies

Without SAP-000, each capability would be documented differently, making it impossible for agents to efficiently discover and adopt patterns. The standardization enables **60-70% token savings** through predictable structures and progressive loading strategies.

---

## When to Use

**Use SAP-000 when**:

✅ **Creating a new capability** - Every new capability MUST follow SAP-000 structure
✅ **Documenting an existing pattern** - Formalize ad-hoc practices into standardized SAPs
✅ **Validating SAP compliance** - Check if a SAP meets all required standards
✅ **Upgrading SAP documentation** - Apply latest standards to older SAPs
✅ **Contributing to chora-base** - Understand structural requirements before submitting PRs

**Don't use SAP-000 for**:

❌ **Project-specific documentation** - Use project README.md, not SAP structure
❌ **One-off scripts or tools** - Simple utilities don't need full SAP packaging
❌ **Experimental prototypes** - Wait until pattern is validated before creating SAP
❌ **External library documentation** - SAPs document internal chora-base patterns only

---

## Quick Start (30 minutes)

### Step 1: Understand the 5 Required Artifacts (10 minutes)

Every SAP consists of 5 markdown files in `docs/skilled-awareness/<capability-name>/`:

```bash
# View SAP-034 as example
ls docs/skilled-awareness/react-database-integration/

# You'll see:
# - capability-charter.md    (Problem statement, scope, outcomes)
# - protocol-spec.md          (Technical contract, APIs, schemas)
# - awareness-guide.md        (Agent execution patterns, workflows)
# - adoption-blueprint.md     (Installation steps, validation)
# - ledger.md                 (Adopter registry, version history)
```

### Step 2: Read the Standards (10 minutes)

Read the core standards sections in protocol-spec.md:

```bash
# Open the protocol specification
cat docs/skilled-awareness/sap-framework/protocol-spec.md

# Key sections to understand:
# - Section 2.1: Required Artifacts
# - Section 2.4: README.md Standard (9-section pattern)
# - Section 2.5: Quick Reference Format Standard
# - Section 2.6: Cross-Cutting Quality Requirements
```

### Step 3: Generate Your First SAP (10 minutes)

Use SAP-029 to generate a new SAP from templates:

```bash
# 1. Add SAP entry to catalog
# Edit sap-catalog.json and add:
{
  "id": "SAP-042",
  "name": "my-capability",
  "status": "draft",
  "version": "0.1.0",
  "description": "Brief description"
}

# 2. Generate artifacts
python scripts/generate-sap.py SAP-042

# 3. Validate structure
python scripts/validate-readme-structure.py --sap my-capability
python scripts/validate-quick-reference.py --sap my-capability
```

**Result**: You now have a compliant SAP skeleton with all 5 artifacts and standard sections ready to be filled in.

---

## Key Features

- ✅ **Standardized Structure** - Every SAP has identical file organization (5 artifacts + README + AGENTS.md), eliminating discovery overhead
- ✅ **Progressive Loading** - Three-tier token usage (300-500 → 2-5k → 10-50k tokens) enables agents to load only what they need
- ✅ **60-70% Token Savings** - Quick Reference format provides essential context in ~15 lines vs 500+ line README.md
- ✅ **Validation Automation** - Automated scripts enforce README structure, Quick Reference format, and link integrity with 100/100 scoring
- ✅ **Multi-Platform Support** - AGENTS.md for generic patterns, CLAUDE.md for Claude-specific optimizations, extensible to other agent platforms
- ✅ **Quality Gates by Status** - Clear requirements for Draft (≥70%), Pilot (≥90%), and Active (100%) SAPs ensure production readiness
- ✅ **Integration Framework** - Dependency tracking, relationship types (Required/Recommended/Optional), and cross-SAP validation prevent integration issues

---

## Quick Reference

### Creating a New SAP

```bash
# 1. Add to catalog
# Edit sap-catalog.json

# 2. Generate skeleton
python scripts/generate-sap.py SAP-XXX

# 3. Fill in artifacts
# Edit the 5 generated markdown files

# 4. Validate compliance
python scripts/validate-readme-structure.py --sap <name>
python scripts/validate-quick-reference.py --sap <name>
python scripts/validate-links.py --path docs/skilled-awareness/<name>/

# 5. Update ledger with first adopter
# Edit ledger.md to add yourself
```

### Validating an Existing SAP

```bash
# Quick validation (30 seconds)
python scripts/sap-evaluator.py --quick SAP-XXX

# Deep validation (5 minutes)
python scripts/sap-evaluator.py --deep SAP-XXX

# Full compliance check
python scripts/validate-readme-structure.py --sap <name>  # Target: 100/100
python scripts/validate-quick-reference.py --sap <name>   # Target: 100/100
python scripts/validate-links.py --path docs/skilled-awareness/<name>/  # Target: 0 broken
```

### Upgrading SAP to Next Status

```bash
# Draft → Pilot requirements:
# - ≥70% validation passing
# - 1+ adopter in ledger.md
# - No critical blockers

# Pilot → Active requirements:
# - ≥90% validation passing
# - 3+ adopters in ledger.md
# - No TODO comments in artifacts
# - All examples tested

# Update status in all frontmatters:
# Edit all 5 artifacts YAML frontmatter
# status: pilot → status: active
```

---

## Integration

| SAP | Relationship | Description |
|-----|--------------|-------------|
| SAP-019 | Recommended | SAP Self-Evaluation validates compliance with SAP-000 standards |
| SAP-029 | Recommended | SAP Generation creates new SAPs conformant to SAP-000 templates |
| SAP-009 | Optional | Agent Awareness uses SAP-000 nested hierarchy pattern |
| SAP-016 | Optional | Link Validation enforces SAP-000 link integrity requirements |
| All SAPs | Required | Every SAP in the ecosystem depends on SAP-000 for structural standards |

**Integration Pattern**: SAP-000 is the foundation layer. All other SAPs are built on top of it. When creating a new SAP:

1. SAP-000 defines the structure
2. SAP-029 generates the skeleton
3. SAP-019 validates compliance
4. SAP-016 ensures link integrity
5. SAP-009 provides discoverability patterns

---

## Success Metrics

### Documentation Quality

- **Target**: 100% of Active SAPs score 100/100 on README validation
- **Current Baseline**: 2.6% (1/39 SAPs) - significant improvement opportunity
- **Measurement**: `python scripts/validate-readme-structure.py --summary-only`

### Discoverability

- **Target**: 60-70% token reduction through Quick Reference usage
- **Current Baseline**: 13.6% (6/44 SAPs) have standardized Quick References
- **Measurement**: Compare tokens used (Quick Reference only vs full README read)

### Adoption Efficiency

- **Target**: New SAPs generated with ≥90% compliance out-of-the-box
- **Measurement**: Validation scores on freshly generated SAPs (SAP-029)
- **ROI**: 90% time reduction (30 hours manual documentation → 3 hours with templates)

### Consistency

- **Target**: 100% version consistency across all SAP artifacts
- **Measurement**: All 5 artifacts have matching YAML frontmatter (sap_id, version, status, last_updated)
- **Validation**: `python scripts/validate-sap-versions.py --all`

---

## Troubleshooting

### Problem 1: Validation Script Fails with "Missing Required Section"

**Symptoms**:
```
❌ README.md validation failed
   Missing section: Quick Start
   Score: 75/100
```

**Cause**: README.md doesn't have all 9 required sections in the correct format.

**Solution**:
1. Read the required sections in [protocol-spec.md section 2.4.2](protocol-spec.md#242-required-sections)
2. Add missing section header: `## Quick Start (X minutes)`
3. Ensure time estimate is 5-60 minutes (not 1-2 minutes)
4. Re-run validation: `python scripts/validate-readme-structure.py --sap <name>`

---

### Problem 2: Quick Reference Score is Low (<80/100)

**Symptoms**:
```
⚠️ Quick Reference validation: 65/100
   Missing: Time savings quantification
   Missing: Integration list
```

**Cause**: Quick Reference section doesn't follow the standardized 6-bullet format.

**Solution**:
1. Read the Quick Reference format in [protocol-spec.md section 2.5.2](protocol-spec.md#252-required-format)
2. Ensure you have:
   - 📖 emoji header
   - "New to SAP-XXX?" prompt
   - 6 emoji bullets (🚀📚🎯🔧📊🔗)
   - Time savings metrics (e.g., "90% reduction (30h → 3h)")
   - Integration list with SAP IDs
3. Re-run validation: `python scripts/validate-quick-reference.py --sap <name>`

---

### Problem 3: Version Mismatch Across Artifacts

**Symptoms**:
```
❌ Version inconsistency detected
   capability-charter.md: 1.2.0
   protocol-spec.md: 1.1.0
   Status: SAP excluded from catalog
```

**Cause**: Frontmatter versions not updated uniformly across all 5 artifacts.

**Solution**:
1. Decide on the correct version (use semantic versioning: MAJOR.MINOR.PATCH)
2. Update YAML frontmatter in all 5 files:
   ```yaml
   ---
   sap_id: SAP-XXX
   version: 1.2.0        # ← Update this
   status: active
   last_updated: 2025-11-10  # ← Update this too
   ---
   ```
3. Update sap-catalog.json to match
4. Commit all files together: `git add . && git commit -m "chore(SAP-XXX): Bump version to 1.2.0"`

---

### Problem 4: Generated SAP Has Placeholder Text

**Symptoms**:
Generated SAP contains `[Description]`, `[TBD]`, or `TODO:` markers in artifacts.

**Cause**: SAP-029 templates use placeholders that must be filled in manually.

**Solution**:
1. This is expected behavior for Draft SAPs (placeholders allowed)
2. Search for placeholders: `grep -r "\[Description\]\|TODO\|TBD" docs/skilled-awareness/<name>/`
3. Replace each placeholder with actual content
4. Before promoting to Active status, ensure 0 placeholders remain
5. Validate: `python scripts/validate-production-quality.py --sap <name>`

---

## Learn More

### Core Artifacts

- **[Protocol Specification](protocol-spec.md)** - Complete technical reference for all SAP standards
- **[Capability Charter](capability-charter.md)** - Problem statement, solution design, and lifecycle
- **[Awareness Guide (AGENTS.md)](AGENTS.md)** - Agent-specific patterns and workflows
- **[Adoption Blueprint](adoption-blueprint.md)** - Step-by-step installation guide
- **[Ledger](ledger.md)** - Adopter registry and version history

### Related SAPs

- **[SAP-019: SAP Self-Evaluation](../sap-self-evaluation/)** - Validate SAP compliance
- **[SAP-029: SAP Generation](../sap-generation/)** - Generate new SAPs from templates
- **[SAP-009: Agent Awareness](../agent-awareness/)** - Nested hierarchy discoverability pattern
- **[SAP-016: Link Validation](../link-validation/)** - Link integrity enforcement

### External Resources

- [Diataxis Framework](https://diataxis.fr/) - Documentation philosophy (Tutorials, How-To, Reference, Explanation)
- [Semantic Versioning](https://semver.org/) - Version numbering convention (MAJOR.MINOR.PATCH)
- [YAML Specification](https://yaml.org/spec/1.2.2/) - Frontmatter format reference

---

**Version**: 1.0.0 (2025-11-10)
**Status**: Active
**Compliance Score**: 100/100 (self-validated)
