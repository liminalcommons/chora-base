# How to Install a SAP Set

**Goal**: Install a curated bundle of Skilled Awareness Packages (SAPs) in one command.

**Prerequisites**:
- Python 3.12+
- Git repository initialized
- Access to chora-base repository (cloned locally or available)

**Time**: 5-10 minutes for installation, 3-5 hours to 2-4 weeks for adoption (depending on set)

---

## Overview

SAP sets are curated bundles of SAPs designed for specific use cases. Instead of installing SAPs one-by-one, you can install an entire set with a single command.

**Available Standard Sets**:
- **minimal-entry** (5 SAPs, 3-5 hours) - Ecosystem coordination
- **recommended** (10 SAPs, 1-2 weeks) - Core development workflow
- **testing-focused** (6 SAPs, 5-8 hours) - Testing and quality
- **mcp-server** (10 SAPs, 1-2 weeks) - MCP server development
- **full** (18 SAPs, 2-4 weeks) - Comprehensive coverage

See [Standard SAP Sets Reference](../reference/standard-sap-sets.md) for detailed comparison.

---

## Step-by-Step: Installing minimal-entry Set

### Step 1: Clone chora-base (if not already available)

```bash
# Option A: Clone to temporary location
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base

# Option B: Clone as sibling directory (recommended for ecosystem work)
cd /path/to/your-projects
git clone https://github.com/liminalcommons/chora-base.git
```

### Step 2: Preview Installation (Dry Run)

Before making any changes, preview what will be installed:

```bash
cd /path/to/your-repo

python /tmp/chora-base/scripts/install-sap.py \
  --set minimal-entry \
  --source /tmp/chora-base \
  --dry-run
```

**Expected Output**:
```
========================================
SAP Set: Minimal Ecosystem Entry
========================================
SAPs to install: 5 (SAP-000, SAP-001, SAP-009, SAP-016, SAP-002)
Estimated tokens: ~29,000
Estimated time: 3-5 hours

⚠ Warning: SAP-001 (inbox-coordination) is in Pilot status - may undergo changes

[DRY RUN] Would install:
  ✓ SAP-000: sap-framework
  ✓ SAP-001: inbox-coordination
  ✓ SAP-009: agent-awareness
  ✓ SAP-016: link-validation-reference-management
  ✓ SAP-002: chora-base-meta

[DRY RUN] Would create directories:
  docs/skilled-awareness/sap-framework/
  docs/skilled-awareness/inbox-coordination/
  docs/skilled-awareness/agent-awareness/
  docs/skilled-awareness/link-validation-reference-management/
  docs/skilled-awareness/chora-base-meta/

[DRY RUN] Would copy system files:
  inbox/README.md
  inbox/schemas/
  AGENTS.md (template)
  scripts/validate-links.py
```

**Review the output carefully**:
- Check which SAPs will be installed
- Note which directories will be created
- Review which system files will be copied
- Look for any warnings (e.g., Pilot status SAPs)

### Step 3: Install the SAP Set

If the dry run looks correct, proceed with installation:

```bash
python /tmp/chora-base/scripts/install-sap.py \
  --set minimal-entry \
  --source /tmp/chora-base
```

**Expected Output**:
```
========================================
Installing SAP Set: Minimal Ecosystem Entry
========================================

Installing SAP-000: sap-framework
  → docs/skilled-awareness/sap-framework/
  ✓ Copied 5 artifacts
  ✓ Validation passed

Installing SAP-001: inbox-coordination
  Dependency: SAP-000 already installed ✓
  → docs/skilled-awareness/inbox-coordination/
  → inbox/ (system files)
  ⚠ Note: Pilot status - may undergo changes
  ✓ Copied 5 artifacts + system files
  ✓ Validation passed

Installing SAP-009: agent-awareness
  Dependency: SAP-000 already installed ✓
  → docs/skilled-awareness/agent-awareness/
  → AGENTS.md (system file)
  ✓ Copied 5 artifacts + AGENTS.md
  ✓ Validation passed

Installing SAP-016: link-validation-reference-management
  Dependency: SAP-000 already installed ✓
  → docs/skilled-awareness/link-validation-reference-management/
  → scripts/validate-links.py (system file)
  ✓ Copied 5 artifacts + script
  ✓ Validation passed

Installing SAP-002: chora-base-meta
  Dependency: SAP-000 already installed ✓
  → docs/skilled-awareness/chora-base-meta/
  ✓ Copied 5 artifacts
  ✓ Validation passed

========================================
✅ Set installation complete!
========================================

Next steps:
1. Review installed SAPs in docs/skilled-awareness/
2. Read adoption blueprints for each SAP
3. Customize AGENTS.md for your project
4. Create inbox/CAPABILITIES/your-repo-name.yaml (optional)
5. Run link validation: python scripts/validate-links.py
```

**Installation takes 10-30 seconds** depending on SAP set size.

### Step 4: Verify Installation

Check that SAPs were installed correctly:

```bash
# List installed SAPs
ls docs/skilled-awareness/

# Expected output:
# agent-awareness
# chora-base-meta
# inbox-coordination
# link-validation-reference-management
# sap-framework

# Check that each SAP has 5 artifacts
ls docs/skilled-awareness/sap-framework/

# Expected output:
# adoption-blueprint.md
# awareness-guide.md
# capability-charter.md
# ledger.md
# protocol-spec.md
```

### Step 5: Review Adoption Blueprints

Each SAP includes an adoption blueprint with step-by-step instructions:

```bash
# Start with the SAP framework
cat docs/skilled-awareness/sap-framework/awareness-guide.md

# Then read each adoption blueprint
cat docs/skilled-awareness/sap-framework/adoption-blueprint.md
cat docs/skilled-awareness/inbox-coordination/adoption-blueprint.md
cat docs/skilled-awareness/agent-awareness/adoption-blueprint.md
cat docs/skilled-awareness/link-validation-reference-management/adoption-blueprint.md
cat docs/skilled-awareness/chora-base-meta/adoption-blueprint.md
```

**Recommended reading order**:
1. **awareness-guide.md** - Conceptual overview (read first!)
2. **adoption-blueprint.md** - Step-by-step implementation
3. **capability-charter.md** - What this SAP enables
4. **protocol-spec.md** - Technical specification
5. **ledger.md** - Track your adoption progress

### Step 6: Customize System Files

Some SAPs install system files that you should customize:

#### AGENTS.md (from SAP-009)

```bash
# Review the template
cat AGENTS.md

# Customize with your project details:
# - Project overview
# - Tech stack
# - Project structure
# - Common tasks
# - Development workflow
```

#### inbox/CAPABILITIES/your-repo.yaml (optional, from SAP-001)

If you want cross-repo coordination:

```bash
mkdir -p inbox/CAPABILITIES

cat > inbox/CAPABILITIES/your-repo.yaml <<'YAML'
repo_id: "your-repo-name"
capabilities:
  - id: "your-repo.core.capability"
    name: "Your Core Capability"
    description: "What your repo provides"
    status: "active"

tech_stack:
  languages: ["Python"]
  frameworks: ["Django"]

coordination_preferences:
  inbox_monitoring: true
  response_sla_hours: 72
YAML
```

### Step 7: Run Validation (from SAP-016)

```bash
# Validate all documentation links
python scripts/validate-links.py

# Expected output if successful:
# ✅ All links valid (0 broken links)
```

### Step 8: Commit Your Changes

```bash
git add .
git commit -m "feat: Adopt chora-base minimal-entry set (5 SAPs)

Installed SAPs:
- SAP-000: sap-framework
- SAP-001: inbox-coordination
- SAP-009: agent-awareness
- SAP-016: link-validation-reference-management
- SAP-002: chora-base-meta

Enables:
- Cross-repo coordination via inbox
- Agent awareness via AGENTS.md
- Link validation
- SAP framework understanding

Next: Customize AGENTS.md and create capabilities file"
```

---

## Installing Other SAP Sets

The process is identical for all sets - just change the `--set` parameter:

### Recommended Set (10 SAPs, 1-2 weeks)

```bash
python /tmp/chora-base/scripts/install-sap.py \
  --set recommended \
  --source /tmp/chora-base
```

**Includes**: All from minimal-entry, plus:
- SAP-003: github-actions-ci-cd
- SAP-004: testing-framework
- SAP-007: documentation-structure
- SAP-010: changelog-management
- SAP-013: git-workflow-patterns

### Testing-Focused Set (6 SAPs, 5-8 hours)

```bash
python /tmp/chora-base/scripts/install-sap.py \
  --set testing-focused \
  --source /tmp/chora-base
```

**Includes**:
- SAP-000: sap-framework
- SAP-003: github-actions-ci-cd
- SAP-004: testing-framework
- SAP-011: type-safety-mypy
- SAP-012: code-quality-ruff
- SAP-016: link-validation-reference-management

### MCP Server Set (10 SAPs, 1-2 weeks)

```bash
python /tmp/chora-base/scripts/install-sap.py \
  --set mcp-server \
  --source /tmp/chora-base
```

**Includes**: Testing-focused set, plus:
- SAP-007: documentation-structure
- SAP-009: agent-awareness
- SAP-012: code-quality-ruff
- SAP-014: mcp-server-development

### Full Set (18 SAPs, 2-4 weeks)

```bash
python /tmp/chora-base/scripts/install-sap.py \
  --set full \
  --source /tmp/chora-base
```

**Includes**: All 18 SAPs for comprehensive coverage.

---

## Progressive Installation

You can install sets progressively. Already-installed SAPs will be skipped automatically:

```bash
# Start with minimal-entry
python scripts/install-sap.py --set minimal-entry --source /tmp/chora-base

# Later, upgrade to recommended
python scripts/install-sap.py --set recommended --source /tmp/chora-base
# Only installs 5 new SAPs (skips the 5 already installed)

# Later, upgrade to full
python scripts/install-sap.py --set full --source /tmp/chora-base
# Only installs remaining 8 SAPs
```

**The script is idempotent** - you can run it multiple times safely.

---

## Listing Available Sets

To see all available sets without installing:

```bash
python /tmp/chora-base/scripts/install-sap.py --list-sets
```

**Expected Output**:
```
Available SAP Sets:

1. minimal-entry
   Name: Minimal Ecosystem Entry
   SAPs: 5 (SAP-000, SAP-001, SAP-009, SAP-016, SAP-002)
   Estimated tokens: ~29,000
   Estimated time: 3-5 hours
   Use cases:
   - First-time chora ecosystem adoption
   - Cross-repo coordination
   - Lightweight onboarding

2. recommended
   Name: Recommended Development Set
   SAPs: 10
   Estimated tokens: ~58,000
   Estimated time: 1-2 weeks
   Use cases:
   - Production development workflow
   - Full-featured project setup

[... continues for all 5 sets]
```

---

## Troubleshooting

### Issue: Command not found

**Symptom**:
```
python: command not found
```

**Solution**: Use `python3` instead:
```bash
python3 /tmp/chora-base/scripts/install-sap.py --set minimal-entry --source /tmp/chora-base
```

### Issue: Source directory not found

**Symptom**:
```
Error: Source directory /tmp/chora-base does not exist
```

**Solution**: Clone chora-base first:
```bash
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base
```

Or use the correct path if you cloned it elsewhere:
```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/your/chora-base
```

### Issue: SAP catalog not found

**Symptom**:
```
Error: sap-catalog.json not found in source directory
```

**Solution**: Ensure `--source` points to the **root** of chora-base:
```bash
# Correct - points to root directory
--source /tmp/chora-base

# Incorrect - points to subdirectory
--source /tmp/chora-base/scripts
```

### Issue: Permission denied when copying files

**Symptom**:
```
PermissionError: [Errno 13] Permission denied: 'docs/skilled-awareness'
```

**Solution**: Ensure you have write permissions in the current directory:
```bash
# Check permissions
ls -ld docs/

# If needed, fix permissions
chmod -R u+w docs/
```

### Issue: Git conflicts after installation

**Symptom**: Uncommitted changes conflict with SAP installation.

**Solution**: Commit or stash your changes first:
```bash
# Option 1: Commit existing changes
git add .
git commit -m "chore: Save work before SAP installation"

# Option 2: Stash changes
git stash
```

Then run the installation.

### Issue: Already-installed SAPs not detected

**Symptom**: Script tries to reinstall SAPs that are already present.

**Solution**: The script checks for existence of `docs/skilled-awareness/{sap-name}/`. If the directory exists, it skips installation. If you see this issue:

```bash
# Check if SAP directory exists
ls docs/skilled-awareness/

# If directory exists but installation still attempts, check for errors in previous installation
# Remove incomplete SAP and reinstall:
rm -rf docs/skilled-awareness/sap-framework
python scripts/install-sap.py SAP-000 --source /tmp/chora-base
```

---

## Next Steps

After installing a SAP set:

1. **Read the adoption blueprints** - Each SAP has detailed implementation steps
2. **Customize system files** - Update AGENTS.md, capabilities files, etc.
3. **Follow the patterns** - Implement the practices documented in each SAP
4. **Track your progress** - Use ledger.md in each SAP to track adoption
5. **Add more SAPs** - Install individual SAPs or upgrade to larger sets as needed

---

## Related Documentation

- [Agent Onboarding Guide](../guides/agent-onboarding-chora-base.md) - Complete onboarding walkthrough
- [Create Custom SAP Sets](create-custom-sap-sets.md) - Define organization-specific sets
- [Standard SAP Sets Reference](../reference/standard-sap-sets.md) - Detailed comparison table
- [install-sap.py CLI Reference](../reference/install-sap-script.md) - Complete command reference

---

## Summary

**Quick installation**:
```bash
# 1. Clone chora-base
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base

# 2. Install SAP set
cd /path/to/your-repo
python /tmp/chora-base/scripts/install-sap.py --set minimal-entry --source /tmp/chora-base

# 3. Review and customize
ls docs/skilled-awareness/
cat docs/skilled-awareness/*/adoption-blueprint.md
```

**Result**: Curated bundle of SAPs installed and ready for adoption, with step-by-step blueprints for each capability.
