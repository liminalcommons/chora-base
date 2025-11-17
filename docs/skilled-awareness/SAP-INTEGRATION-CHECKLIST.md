# SAP Integration Checklist

**Purpose**: Comprehensive checklist for integrating locally-developed SAPs into chora-base ecosystem

**Last Updated**: 2025-11-16
**Status**: Active

---

## Overview

When a SAP is developed locally (e.g., in chora-workspace) and needs to be integrated into chora-base, follow this checklist to ensure complete integration and discoverability.

**Integration Scope**:
1. Physical SAP directory in skilled-awareness/
2. SAP catalog metadata
3. INDEX.md discoverability
4. Dependency graph updates
5. Progressive Adoption Path references (when appropriate)

---

## Pre-Integration Verification

### 1. SAP Artifacts Complete

**Location**: `chora-base/docs/skilled-awareness/{sap-name}/`

Verify all 5 core SAP artifacts exist and are complete:

- [ ] `capability-charter.md` - SAP purpose, scope, governance
- [ ] `protocol-spec.md` - Technical specification, schemas, interfaces
- [ ] `awareness-guide.md` - Agent-facing documentation
- [ ] `adoption-blueprint.md` - Implementation guide, effort estimates
- [ ] `ledger.md` - Version history, change log

**Validation**:
```bash
# Check all artifacts exist
ls chora-base/docs/skilled-awareness/{sap-name}/

# Check artifacts are not empty
find chora-base/docs/skilled-awareness/{sap-name}/ -name "*.md" -size 0

# Verify frontmatter exists
head -20 chora-base/docs/skilled-awareness/{sap-name}/capability-charter.md
```

---

### 2. SAP Scripts/Schemas Complete

**Location**: `chora-base/docs/skilled-awareness/{sap-name}/scripts/` or `schemas/`

If SAP includes automation scripts or schemas, verify:

- [ ] Scripts have shebang (`#!/usr/bin/env python3`)
- [ ] Scripts have docstrings explaining purpose
- [ ] Schemas are valid JSON/YAML
- [ ] Scripts are executable (`chmod +x`)

**Validation**:
```bash
# Check scripts directory
ls chora-base/docs/skilled-awareness/{sap-name}/scripts/

# Verify shebang
head -1 chora-base/docs/skilled-awareness/{sap-name}/scripts/*.py

# Check schemas
python3 -m json.tool chora-base/docs/skilled-awareness/{sap-name}/schemas/*.json
```

---

## Integration Steps

### 3. SAP Catalog Entry

**File**: `chora-base/sap-catalog.json`

Verify SAP has complete catalog entry with all required fields:

**Required Fields**:
- [ ] `id` - SAP-XXX format
- [ ] `name` - kebab-case name
- [ ] `full_name` - Display name
- [ ] `status` - draft | pilot | active | deprecated
- [ ] `version` - Semantic version (e.g., "1.0.0")
- [ ] `included_by_default` - boolean
- [ ] `size_kb` - Estimated size
- [ ] `description` - One-line description
- [ ] `capabilities` - Array of capability strings
- [ ] `dependencies` - Array of SAP-XXX dependencies
- [ ] `tags` - Array of search tags
- [ ] `author` - "chora-base" or maintainer
- [ ] `location` - Path relative to skilled-awareness/
- [ ] `artifacts` - Object mapping core artifacts to boolean
- [ ] `system_files` - Array of script/schema paths

**Validation**:
```bash
# Extract SAP entry
grep -A 50 '"id": "SAP-XXX"' chora-base/sap-catalog.json

# Validate JSON
python3 -m json.tool chora-base/sap-catalog.json > /dev/null && echo "Valid JSON"

# Count fields
grep -A 50 '"id": "SAP-XXX"' chora-base/sap-catalog.json | grep -c '":"'
```

**Example Entry**:
```json
{
  "id": "SAP-056",
  "name": "lifecycle-traceability",
  "full_name": "Lifecycle Traceability",
  "status": "draft",
  "version": "1.0.0",
  "included_by_default": false,
  "size_kb": 450,
  "description": "Umbrella governance SAP for comprehensive traceability...",
  "capabilities": [
    "Traceability governance framework (10 artifact types)",
    "Feature manifest schema (YAML-based single source of truth)",
    "10 validation rules (forward linkage, bidirectional, evidence...)"
  ],
  "dependencies": [
    "SAP-000",
    "SAP-004",
    "SAP-007",
    "SAP-010",
    "SAP-012",
    "SAP-015"
  ],
  "tags": [
    "traceability",
    "governance",
    "lifecycle",
    "validation"
  ],
  "author": "chora-base",
  "location": "docs/skilled-awareness/lifecycle-traceability",
  "artifacts": {
    "capability_charter": true,
    "protocol_spec": true,
    "awareness_guide": true,
    "adoption_blueprint": true,
    "ledger": true
  },
  "system_files": [
    "schemas/feature-manifest.schema.json",
    "scripts/validate-traceability.py"
  ]
}
```

---

### 4. INDEX.md Entry

**File**: `chora-base/docs/skilled-awareness/INDEX.md`

Add SAP entry to appropriate domain section:

**4a. Add SAP Entry**

Location depends on domain:
- **Infrastructure**: Lines ~100-200
- **Developer Experience**: Lines ~200-350
- **Application Development**: Lines ~350-450
- **Specialized**: Lines ~450-550
- **Advanced**: Lines ~550-600

**Entry Template**:
```markdown
### SAP-XXX: {Full Name}

- **Status**: {draft|pilot|active} | **Version**: {X.Y.Z} | **Domain**: {Domain}
- **Description**: {One-line description with key features}
- **Dependencies**: SAP-AAA, SAP-BBB, SAP-CCC
- **Location**: [{sap-name}/]({sap-name}/)
- **Key Features**: {Comma-separated list of 5-7 key capabilities}
```

**Example** (SAP-056):
```markdown
### SAP-056: Lifecycle Traceability

- **Status**: draft | **Version**: 1.0.0 | **Domain**: Specialized
- **Description**: Umbrella governance SAP for comprehensive traceability across 10 artifact types (Vision → Features → Requirements → Code → Tests → Docs → Git → Tasks → Events → Knowledge). Defines linkage schemas, validation rules, and compliance levels to achieve 100% traceability coverage
- **Dependencies**: SAP-000, SAP-004, SAP-007, SAP-010, SAP-012, SAP-015
- **Location**: [lifecycle-traceability/](lifecycle-traceability/)
- **Key Features**: Feature manifest schema (YAML single source of truth), 10 validation rules (forward linkage, bidirectional, evidence, closed loop, orphan detection, schema, integrity, coverage), 4 adoption levels (L0-L3: no/partial/substantial/complete), automated validation script with 100% pass rate, auto-generation from git/beads, HTML dashboard, JSON Schema validation
```

**4b. Update Statistics**

Location: Lines ~10-30 (Overview section)

- [ ] Update **total SAP count** (e.g., 45 → 46)
- [ ] Update **domain count** (e.g., Specialized: 10 → 11)
- [ ] Update **status breakdown** if needed (e.g., draft: 8 → 9)

**Before**:
```markdown
| Domain | SAPs | Percentage | Status Breakdown |
|--------|------|------------|------------------|
| Specialized | 10 | 22% | 7 active, 2 pilot, 1 draft |
| **Total** | **45** | **100%** | **24 active, 12 pilot, 8 draft, 1 deprecated** |
```

**After**:
```markdown
| Domain | SAPs | Percentage | Status Breakdown |
|--------|------|------------|------------------|
| Specialized | 11 | 24% | 7 active, 3 pilot, 1 draft |
| **Total** | **46** | **100%** | **24 active, 12 pilot, 9 draft, 1 deprecated** |
```

**Validation**:
```bash
# Count total SAPs in catalog
grep '"id": "SAP-' chora-base/sap-catalog.json | wc -l

# Count by status
grep '"status": "active"' chora-base/sap-catalog.json | wc -l
grep '"status": "pilot"' chora-base/sap-catalog.json | wc -l
grep '"status": "draft"' chora-base/sap-catalog.json | wc -l

# Verify percentages add to 100%
# Specialized: 11/46 = 23.9% ≈ 24%
```

**4c. Update Dependency Graph**

Location: Lines ~600-680 (SAP Dependency Graph section)

Add SAP to appropriate domain subtree with dependencies:

**Template**:
```markdown
{Domain} Domain
├─ SAP-XXX ({sap-name})
   └─ Depends on: SAP-AAA, SAP-BBB, SAP-CCC
```

**Example** (SAP-056):
```markdown
Specialized Domain                         │
├─ SAP-056 (lifecycle-traceability)
   └─ Depends on: SAP-004, SAP-007, SAP-010, SAP-012, SAP-015
```

**Validation**:
```bash
# Check dependency graph section
grep -A 100 "## SAP Dependency Graph" chora-base/docs/skilled-awareness/INDEX.md | grep "SAP-056"

# Verify dependencies match catalog
grep -A 20 '"id": "SAP-056"' chora-base/sap-catalog.json | grep dependencies
```

---

### 5. Progressive Adoption Paths (Optional)

**File**: `chora-base/docs/skilled-awareness/INDEX.md`
**Location**: Lines ~530-605

**When to Include**:
- SAP status is **pilot** or **active** (not draft)
- SAP fits thematically into an adoption path
- SAP provides significant value for the path's goal

**Available Paths**:
- **PATH 1**: Capability Server Development (New)
- **PATH 2**: React Application Development
- **PATH 3**: Legacy MCP Server Development
- **PATH 4**: Cross-Repository Coordination
- **PATH 5**: Process Maturity & Best Practices

**Integration Example** (if SAP-056 becomes pilot/active):

**PATH 5: Process Maturity & Best Practices** (Line ~593-601)
```markdown
### Path 5: Process Maturity & Best Practices

**Goal**: Improve development processes and team productivity

1. **Infrastructure** (SAP-000, 002) - Framework foundation
2. **Developer Experience** (SAP-004, 005, 006, 007, 008) - Testing, CI/CD, quality, docs
3. **Specialized** (SAP-009, 010, 012, 015, 019, 027, 056) - Full process stack

**Estimated Setup**: 4-6 days
```

**Note**: SAP-056 (lifecycle-traceability) is currently **draft** status, so it should NOT be added to adoption paths yet. Add when status reaches **pilot** or **active**.

---

## Post-Integration Verification

### 6. Validation Checks

Run these checks to verify complete integration:

**6a. Catalog Validation**
```bash
# Validate JSON syntax
python3 -m json.tool chora-base/sap-catalog.json > /dev/null

# Check SAP-XXX entry exists
grep '"id": "SAP-XXX"' chora-base/sap-catalog.json

# Verify dependencies exist in catalog
for dep in $(grep -A 20 '"id": "SAP-XXX"' chora-base/sap-catalog.json | grep -oP 'SAP-\d+'); do
  grep -q "\"id\": \"$dep\"" chora-base/sap-catalog.json && echo "$dep: OK" || echo "$dep: MISSING"
done
```

**6b. INDEX.md Validation**
```bash
# Check SAP-XXX entry exists in INDEX.md
grep "SAP-XXX:" chora-base/docs/skilled-awareness/INDEX.md

# Verify statistics updated
grep "Total.*46" chora-base/docs/skilled-awareness/INDEX.md

# Check dependency graph includes SAP-XXX
grep -A 100 "SAP Dependency Graph" chora-base/docs/skilled-awareness/INDEX.md | grep "SAP-XXX"
```

**6c. Link Validation**
```bash
# Validate markdown links in INDEX.md
# (Requires markdown link checker or manual review)

# Check SAP directory link
ls chora-base/docs/skilled-awareness/{sap-name}/

# Verify relative links work
cd chora-base/docs/skilled-awareness/ && cat INDEX.md | grep -oP '\[.*\]\(\K[^)]+' | while read link; do
  [ -e "$link" ] && echo "$link: OK" || echo "$link: BROKEN"
done
```

**6d. Discoverability Test**
```bash
# Search for SAP by ID
grep -r "SAP-XXX" chora-base/docs/skilled-awareness/

# Search by tag
grep -r "tag-keyword" chora-base/sap-catalog.json

# Verify location path
ls chora-base/docs/skilled-awareness/{sap-name}/capability-charter.md
```

---

## Integration Checklist Summary

Copy this checklist for each SAP integration:

### Pre-Integration
- [ ] All 5 core SAP artifacts exist and are complete
- [ ] Scripts/schemas are valid and functional
- [ ] SAP dependencies are identified

### Catalog Integration
- [ ] SAP entry exists in `sap-catalog.json`
- [ ] All required fields are populated (14+ fields)
- [ ] Dependencies array is accurate
- [ ] Tags are comprehensive and searchable
- [ ] System files are listed

### INDEX.md Integration
- [ ] SAP entry added to appropriate domain section
- [ ] Entry follows template format
- [ ] Description is concise and informative
- [ ] Total SAP count updated in Overview
- [ ] Domain count updated in Statistics table
- [ ] Status breakdown updated
- [ ] Percentages recalculated (add to 100%)
- [ ] SAP added to Dependency Graph
- [ ] Dependencies listed correctly

### Adoption Path Integration (Optional)
- [ ] SAP status is pilot/active (not draft)
- [ ] Appropriate path identified
- [ ] SAP added to path section
- [ ] Effort estimates updated if needed

### Post-Integration Validation
- [ ] `sap-catalog.json` is valid JSON
- [ ] SAP entry found by grep
- [ ] Dependencies exist in catalog
- [ ] INDEX.md entry found by grep
- [ ] Statistics counts match catalog
- [ ] Dependency graph includes SAP
- [ ] Markdown links are valid
- [ ] SAP directory is discoverable

---

## Common Issues

### Issue 1: Statistics Don't Match Catalog

**Problem**: INDEX.md says 45 SAPs, catalog has 46 entries

**Solution**:
```bash
# Count catalog entries
grep -c '"id": "SAP-' chora-base/sap-catalog.json

# Update INDEX.md statistics to match
# Line ~13: Total count
# Line ~520: Domain breakdown
```

### Issue 2: Dependency Graph Missing SAP

**Problem**: SAP-XXX not shown in dependency graph

**Solution**:
```bash
# Find domain section in dependency graph (lines ~605-680)
# Add entry:
# {Domain} Domain
# ├─ SAP-XXX ({sap-name})
#    └─ Depends on: SAP-AAA, SAP-BBB
```

### Issue 3: Broken Relative Links

**Problem**: INDEX.md links to SAP directory show 404

**Solution**:
```bash
# Verify SAP directory exists
ls chora-base/docs/skilled-awareness/{sap-name}/

# Check INDEX.md uses correct relative path
# Should be: [{sap-name}/]({sap-name}/)
# NOT: [docs/skilled-awareness/{sap-name}/](docs/...)
```

### Issue 4: Catalog Dependencies Invalid

**Problem**: SAP-XXX lists SAP-YYY as dependency, but SAP-YYY doesn't exist

**Solution**:
```bash
# Verify all dependencies exist
for dep in SAP-004 SAP-007 SAP-010; do
  grep -q "\"id\": \"$dep\"" chora-base/sap-catalog.json && echo "$dep: OK" || echo "$dep: MISSING"
done

# Remove or correct invalid dependencies
```

---

## Success Criteria

Integration is complete when:

1. ✅ SAP appears in `sap-catalog.json` with complete metadata
2. ✅ SAP appears in INDEX.md domain section with description
3. ✅ Statistics in INDEX.md reflect updated SAP count
4. ✅ Dependency graph includes SAP with correct dependencies
5. ✅ All markdown links are valid and resolve
6. ✅ SAP is discoverable by search (grep, catalog tags, INDEX.md)
7. ✅ (Optional) SAP appears in relevant Progressive Adoption Path

---

## Example: SAP-056 Integration

**SAP**: SAP-056 (Lifecycle Traceability)
**Domain**: Specialized
**Status**: draft
**Date**: 2025-11-16

### Completed Steps

1. ✅ SAP artifacts verified at `chora-base/docs/skilled-awareness/lifecycle-traceability/`
2. ✅ Catalog entry complete in `sap-catalog.json` (lines 2514-2565)
3. ✅ INDEX.md entry added to Specialized Domain (lines 499-505)
4. ✅ Statistics updated: 45 → 46 SAPs total, Specialized 10 → 11
5. ✅ Dependency graph updated (lines 662-663)
6. ⏸️ Adoption Path integration deferred (status: draft, not pilot/active)
7. ✅ Validation checks passed

### Integration Time

- **Total Time**: ~20 minutes
- Breakdown:
  - Catalog verification: 5 min
  - INDEX.md entry: 5 min
  - Statistics update: 3 min
  - Dependency graph: 3 min
  - Validation: 4 min

---

## References

- **SAP Catalog Schema**: `chora-base/sap-catalog.json`
- **INDEX.md Template**: `chora-base/docs/skilled-awareness/INDEX.md`
- **SAP Framework**: [SAP-000](sap-framework/)
- **Progressive Adoption Paths**: INDEX.md lines 530-605
- **Dependency Graph**: INDEX.md lines 605-680

---

**Version**: 1.0.0
**Created**: 2025-11-16
**Status**: Active
**Maintainer**: chora-base
