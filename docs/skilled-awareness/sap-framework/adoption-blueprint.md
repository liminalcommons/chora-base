# Adoption Blueprint: SAP Framework

**SAP ID**: SAP-000
**Version**: 1.0.0
**Status**: Draft → Active (Phase 1)
**Last Updated**: 2025-10-27

---

## 1. Overview

This blueprint guides **adopters** (humans and AI agents) through installing the SAP Framework capability into their chora-base-derived projects.

**What You'll Get**:
- Root SAP protocol document
- SAP framework documentation
- Templates for creating SAPs
- SAP Index (registry)

**Time Estimate**: 30-45 minutes (agent-assisted)

---

## 2. Prerequisites

### Required Versions

- **chora-base**: v3.0.0 or later
- **Git**: v2.0+ (for version tracking)
- **AI Agent**: Claude Code, Cursor, or equivalent

### Required Knowledge

- Basic understanding of chora-base structure
- Familiarity with markdown and YAML

### Required Access

- Write access to project repository
- Ability to create directories and files

---

## 3. Installation Paths

### Path A: Full SAP Framework (Recommended)

Install complete SAP framework with all documentation and templates.

**Use When**:
- You plan to create SAPs for your capabilities
- You want to adopt chora-base capabilities formally
- You need structured capability governance

**Result**: Full SAP framework installed, ready to create/adopt SAPs

### Path B: Reference Only

Read SAP framework documentation without installing.

**Use When**:
- You want to understand SAP structure
- You're evaluating SAP framework
- You don't need to create SAPs yet

**Result**: Understanding of SAP framework, no files installed

---

## 4. Installation (Path A: Full Framework)

### Step 1: Create SAP Framework Directory

Create the skilled awareness directory structure:

```bash
mkdir -p docs/reference/skilled-awareness
```

**Validation**:
```bash
ls docs/reference/skilled-awareness && echo "✅ Directory created"
```

### Step 2: Copy Root Protocol

Copy the SAP protocol from chora-base to your project root:

**For agents**:
1. Read: `/path/to/chora-base/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md`
2. Write to: `SKILLED_AWARENESS_PACKAGE_PROTOCOL.md` (project root)

**For humans**:
```bash
cp /path/to/chora-base/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md \
   SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
```

**Validation**:
```bash
test -f SKILLED_AWARENESS_PACKAGE_PROTOCOL.md && echo "✅ Protocol copied"
```

### Step 3: Copy Framework SAP

Copy the sap-framework SAP directory:

**For agents**:
1. Read all files in: `/path/to/chora-base/docs/skilled-awareness/sap-framework/`
2. Write to: `docs/skilled-awareness/sap-framework/`

Files to copy:
- `capability-charter.md`
- `protocol-spec.md`
- `awareness-guide.md`
- `adoption-blueprint.md` (this file)
- `ledger.md`

**For humans**:
```bash
cp -r /path/to/chora-base/docs/skilled-awareness/sap-framework \
      docs/skilled-awareness/
```

**Validation**:
```bash
ls docs/skilled-awareness/sap-framework/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md && echo "✅ Framework SAP copied"
```

### Step 4: Copy Document Templates

Copy SAP templates:

**For agents**:
1. Read: `/path/to/chora-base/docs/skilled-awareness/document-templates.md`
2. Write to: `docs/skilled-awareness/document-templates.md`

**For humans**:
```bash
cp /path/to/chora-base/docs/skilled-awareness/document-templates.md \
   docs/skilled-awareness/
```

**Validation**:
```bash
test -f docs/skilled-awareness/document-templates.md && echo "✅ Templates copied"
```

### Step 5: Create SAP Index

Create the SAP Index file:

**For agents**:
1. Write to: `docs/skilled-awareness/INDEX.md`
2. Content (initial):

```markdown
# SAP Index

**Purpose**: Central registry of all Skilled Awareness Packages in this project.

**Last Updated**: <today's date>

---

## Active SAPs

| SAP ID | Capability | Version | Status | Location |
|--------|------------|---------|--------|----------|
| SAP-000 | sap-framework | 1.0.0 | Active | docs/skilled-awareness/sap-framework/ |

---

## Planned SAPs

| Capability | Priority | Phase | Notes |
|------------|----------|-------|-------|
| _None yet_ | - | - | Add planned SAPs here |

---

## Legend

**Status Values**:
- **Draft**: In development
- **Pilot**: Ready for limited adoption
- **Active**: Production-ready
- **Deprecated**: Upgrade recommended
- **Archived**: No longer maintained

**Priority Values**:
- **P0**: Critical, required immediately
- **P1**: High value, next phase
- **P2**: Nice to have, future

---

**See Also**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- [document-templates.md](../document-templates.md)
```

**Validation**:
```bash
test -f docs/skilled-awareness/INDEX.md && echo "✅ Index created"
```

### Step 6: Update Project AGENTS.md

Add SAP Framework section to your project's `AGENTS.md`:

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### Skilled Awareness Packages (SAPs)

This project uses the SAP Framework for capability packaging and governance.

**SAP Index**: [docs/skilled-awareness/INDEX.md](/docs/skilled-awareness/INDEX.md)

**Root Protocol**: [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)

**Creating SAPs**:
- Use templates: [docs/skilled-awareness/document-templates.md](/docs/skilled-awareness/document-templates.md)
- Follow framework: [docs/skilled-awareness/sap-framework/](/docs/skilled-awareness/sap-framework/)

**Installing SAPs**:
- Read adoption blueprint: `docs/skilled-awareness/<sap>/adoption-blueprint.md`
- Execute steps sequentially
- Update ledger when complete
```

**Validation**:
```bash
grep "Skilled Awareness Packages" AGENTS.md && echo "✅ AGENTS.md updated"
```

### Step 7: Update Project README (Optional)

Add SAP Framework mention to README:

**For agents** (use Edit tool):
1. Open: `README.md`
2. Find "Features" or "Capabilities" section
3. Add:

```markdown
- **📦 SAP Framework** - Structured capability packaging with contracts, blueprints, and governance
```

**Validation**:
```bash
grep "SAP Framework" README.md && echo "✅ README updated"
```

### Step 8: Update Ledger

Update the sap-framework ledger to record your adoption:

**For agents** (use Edit tool):
1. Open: `docs/skilled-awareness/sap-framework/ledger.md`
2. Find "Adopter Registry" table
3. Add row:

```markdown
| <your-project-name> | 1.0.0 | Active | <today's date> | Initial adoption |
```

**Note**: If this is in your own project (not chora-base), create PR to chora-base to update the ledger there.

**Validation**:
```bash
grep "<your-project-name>" docs/skilled-awareness/sap-framework/ledger.md && echo "✅ Ledger updated"
```

### Step 9: Commit Changes

Commit the SAP Framework installation:

```bash
git add docs/skilled-awareness/ SKILLED_AWARENESS_PACKAGE_PROTOCOL.md AGENTS.md README.md
git commit -m "feat: Install SAP Framework v1.0.0

- Add root SAP protocol
- Copy sap-framework SAP
- Copy document templates
- Create SAP Index
- Update AGENTS.md and README

SAP-000 v1.0.0"
```

**Validation**:
```bash
git log -1 --oneline | grep "SAP Framework" && echo "✅ Changes committed"
```

---

## 5. Validation

### Full Installation Checklist

Run all validation commands:

```bash
# Check directory
ls docs/reference/skilled-awareness && echo "✅ Directory exists"

# Check root protocol
test -f SKILLED_AWARENESS_PACKAGE_PROTOCOL.md && echo "✅ Protocol exists"

# Check framework SAP (5 artifacts)
ls docs/skilled-awareness/sap-framework/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md && echo "✅ Framework SAP complete"

# Check templates
test -f docs/skilled-awareness/document-templates.md && echo "✅ Templates exist"

# Check index
test -f docs/skilled-awareness/INDEX.md && echo "✅ Index exists"

# Check AGENTS.md updated
grep "Skilled Awareness Packages" AGENTS.md && echo "✅ AGENTS.md updated"

# Check ledger updated
grep "<your-project-name>" docs/skilled-awareness/sap-framework/ledger.md && echo "✅ Ledger updated"
```

**Expected Output**: All checks show ✅

### Post-Installation Tests

**Test 1: Read Root Protocol**
```bash
head -20 SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
```
Should show SAP protocol header.

**Test 2: View SAP Index**
```bash
cat docs/skilled-awareness/INDEX.md
```
Should show SAP-000 (sap-framework) in Active SAPs table.

**Test 3: Check Framework SAP**
```bash
head -10 docs/skilled-awareness/sap-framework/capability-charter.md
```
Should show charter frontmatter with `sap_id: SAP-000`.

---

## 6. Configuration

### Required Configuration

**SAP Index Customization**:
1. Open: `docs/skilled-awareness/INDEX.md`
2. Update "Planned SAPs" table with your capabilities
3. Set priorities (P0, P1, P2) and phases

**Example**:
```markdown
## Planned SAPs

| Capability | Priority | Phase | Notes |
|------------|----------|-------|-------|
| testing-framework | P0 | Phase 1 | pytest, coverage, fixtures |
| docker-operations | P1 | Phase 2 | Dockerfile, compose, optimization |
```

### Optional Configuration

**Create SAP Roadmap** (recommended):
1. Create: `docs/skilled-awareness/<project>-sap-roadmap.md`
2. Use template: [chora-base-sap-roadmap.md](../chora-base-sap-roadmap.md)
3. Define phases, deliverables, success metrics

**Add to Git Hooks** (recommended):
- Add SAP validation to pre-commit hooks
- Check YAML frontmatter validity
- Enforce 5-artifact completeness

---

## 7. Upgrade Path

### Future Versions

**When framework updates**:
1. Check chora-base releases for SAP framework updates
2. Look for upgrade blueprints in `sap-framework/upgrades/`
3. Follow sequential upgrade path (v1.0 → v1.1 → v2.0)

**Current Version**: 1.0.0 (initial release)

**Next Expected Version**: 1.1.0 (minor enhancements, TBD)

---

## 8. Troubleshooting

### Problem: Directory already exists

**Symptom**:
```
mkdir: docs/reference/skilled-awareness: File exists
```

**Solution**:
- Check if SAP framework already installed
- If yes, skip to Step 3 (copy framework SAP)
- If partial install, remove and start over

### Problem: Protocol file conflicts

**Symptom**:
```
SKILLED_AWARENESS_PACKAGE_PROTOCOL.md already exists
```

**Solution**:
- Check version of existing file: `head -5 SKILLED_AWARENESS_PACKAGE_PROTOCOL.md`
- If older version, backup and replace:
  ```bash
  mv SKILLED_AWARENESS_PACKAGE_PROTOCOL.md SKILLED_AWARENESS_PACKAGE_PROTOCOL.md.bak
  # Then copy new version
  ```

### Problem: AGENTS.md section placement unclear

**Symptom**:
- Not sure where to add SAP Framework section

**Solution**:
- Look for existing "Capabilities" or "Project Structure" section
- If none exists, add after "Project Overview"
- Create new "## Capabilities" section if needed

### Problem: Ledger update fails (permission denied)

**Symptom**:
- Can't edit ledger in chora-base

**Solution**:
- If installing in your own project (not chora-base):
  - Edit local ledger copy
  - Create PR to chora-base repo to update origin ledger
  - Reference PR in local ledger notes
- If installing in chora-base:
  - Should have write access as maintainer

### Problem: Validation commands fail

**Symptom**:
- One or more validation commands show errors

**Solution**:
- Review failed step
- Re-execute that step
- Check file paths (relative vs absolute)
- Verify you're in project root directory

---

## 9. Next Steps

After installing SAP Framework:

### 9.1 Create Your First SAP

**Identify Capability**:
- Choose a capability from your project (e.g., testing-framework, docker-operations)
- Add to SAP Index "Planned SAPs" table

**Create SAP**:
1. Read: [awareness-guide.md](awareness-guide.md) - Section 3.1 "Create New SAP"
2. Follow workflow to create 5 artifacts
3. Use templates: [document-templates.md](../document-templates.md)

**Example**: Study [inbox SAP](../inbox/) as reference

### 9.2 Adopt Existing SAPs

**Browse Available SAPs**:
- Check chora-base: [docs/skilled-awareness/](../)
- Review SAP Index: [INDEX.md](../INDEX.md)

**Install SAP**:
1. Read SAP's adoption blueprint: `<sap>/adoption-blueprint.md`
2. Follow installation steps
3. Update ledger when complete

**Example**: Install inbox SAP for cross-repo coordination

### 9.3 Integrate with Development Workflow

**DDD → BDD → TDD**:
- Use SAP framework during DDD phase (create Charter + Protocol)
- Create infrastructure during TDD phase
- Document patterns in Awareness Guide

**Sprint Planning**:
- Plan SAP creation as sprint tasks
- Allocate time for 5 artifacts (8-12 hours per SAP)
- Track progress in SAP Index

---

## 10. Support

### Getting Help

**Documentation**:
- Read: [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- Study: [inbox SAP](../inbox/) (reference implementation)
- Review: [awareness-guide.md](awareness-guide.md)

**Issues**:
- Open issue in chora-base repository
- Tag with `sap-framework` label
- Include version and error details

**Community**:
- Check existing issues for similar problems
- Share learnings in your SAP ledger notes

---

## 11. Related Documents

**SAP Framework**:
- [capability-charter.md](capability-charter.md) - Framework overview
- [protocol-spec.md](protocol-spec.md) - Technical specification
- [awareness-guide.md](awareness-guide.md) - Agent guidance
- [ledger.md](ledger.md) - Adopter tracking

**Templates & Tools**:
- [document-templates.md](../document-templates.md) - SAP templates
- [INDEX.md](../INDEX.md) - SAP registry

**Root Protocol**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)

---

**Version History**:
- **1.0.0** (2025-10-27): Initial adoption blueprint
