# Quickstart: Claude Code Agent

**For**: Claude Code AI agents onboarding to chora-base
**Time**: ~15 minutes total
**Goal**: Get productive with chora-base SAPs as quickly as possible

**Last Updated**: 2025-10-30 (COORD-003 Sprint 2)

---

## Overview

This guide is optimized for Claude Code agents. It's 60%+ shorter than the generic guide (500 lines vs 2000+), focusing only on what Claude Code needs to get started.

**What you'll accomplish**:
1. Validate environment (2 minutes)
2. Install minimal-entry SAP set (5 minutes)
3. Verify installation (2 minutes)
4. Complete first task: Read SAP-000 (5 minutes)

**Total time**: ~15 minutes

---

## Prerequisites (2 minutes)

### Required

- **Python 3.8+** (you likely already have this)
- **Git 2.0+** (you likely already have this)
- **chora-base cloned** (if reading this, you probably have it)

### Quick Check

```bash
# Verify you're in chora-base root
pwd  # Should end with /chora-base
ls sap-catalog.json  # Should exist

# Run pre-flight validation
bash scripts/validate-prerequisites.sh
```

**Expected**: `✓ Pre-flight validation PASSED`

**If failed**: See [Onboarding FAQ](../troubleshooting/onboarding-faq.md#installation-issues) for fixes

---

## Installation (5 minutes)

### Step 1: Choose SAP Set

**Recommendation for Claude Code**: Start with `minimal-entry`

**Why**:
- 5 essential SAPs (SAP-000, SAP-001, SAP-002, SAP-009, SAP-016)
- Covers SAP framework + inbox coordination
- 3-5 hour adoption time (vs weeks for full set)
- You can always add more SAPs later

**Not sure?** See [SAP Set Decision Tree](../reference/sap-set-decision-tree.md)

### Step 2: Dry-Run (Optional but Recommended)

```bash
python3 scripts/install-sap.py --set minimal-entry --dry-run
```

**What this does**: Shows what will be installed without making changes

**Expected output**:
```
Installing SAP Set: Minimal Ecosystem Entry
SAPs: 5 (SAP-000, SAP-001, SAP-009, SAP-016, SAP-002)
[DRY RUN] Would install:
  ✓ SAP-000: sap-framework
  ✓ SAP-001: inbox-coordination
  ✓ SAP-009: agent-awareness
  ✓ SAP-016: link-validation-reference-management
  ✓ SAP-002: chora-base-meta
```

### Step 3: Install

```bash
python3 scripts/install-sap.py --set minimal-entry
```

**What happens**:
- Installs 5 SAPs to `docs/skilled-awareness/`
- Shows progress bar: `[====>    ] 3/5 SAPs (60%) ~30s remaining`
- Takes ~1-2 minutes (actual installation, not adoption time)
- May show warnings for Pilot-status SAPs (this is normal)

**Expected output**:
```
Installing SAP-000: sap-framework
  ✓ Copied SAP directory
  ✓ Validation passed

Installing SAP-001: inbox-coordination
  ⚠ Note: Pilot status - may undergo changes
  ✓ Copied SAP directory
  ✓ Copied system files
  ✓ Validation passed

[Progress bar showing completion]

✅ Set installation complete!
```

---

## Validation (2 minutes)

### Step 1: Check SAP Directories

```bash
ls docs/skilled-awareness/ | grep SAP-
```

**Expected output** (5 directories):
```
SAP-000-sap-framework/
SAP-001-inbox/
SAP-002-chora-base/
SAP-009-agent-awareness/
SAP-016-link-validation-reference-management/
```

**Count check**:
```bash
ls -d docs/skilled-awareness/SAP-* | wc -l
# Should output: 5
```

### Step 2: Check SAP Artifacts

Each SAP should have 5 files:

```bash
ls docs/skilled-awareness/SAP-000-sap-framework/
```

**Expected output**:
```
BLUEPRINT.md          (or adoption-blueprint.md)
INDEX.md             (or awareness-guide.md)
AGENTS.md            (or capability-charter.md)
README.md            (or protocol-spec.md)
SPECIFICATION.md     (or ledger.md)
```

*Note: Exact filenames may vary by SAP version, but should have 5 markdown files*

### Step 3: Test Reading a SAP

```bash
cat docs/skilled-awareness/SAP-000-sap-framework/README.md | head -20
```

**Expected**: Readable markdown content about SAP framework

**If any validation fails**: See [Onboarding FAQ - Validation Issues](../troubleshooting/onboarding-faq.md#validation-issues)

---

## First Task: Understand SAP-000 (5 minutes)

Now that SAPs are installed, let's complete your first task: understanding the SAP framework.

### Task: Read SAP-000 Protocol Specification

**Goal**: Understand what SAPs are and how they work

**Steps**:

1. **Read the README** (1 minute):
   ```bash
   cat docs/skilled-awareness/SAP-000-sap-framework/README.md
   ```
   *Gives you a quick overview*

2. **Scan the INDEX** (1 minute):
   ```bash
   cat docs/skilled-awareness/SAP-000-sap-framework/INDEX.md
   ```
   *Shows the 5 artifact structure*

3. **Skim the SPECIFICATION** (2 minutes):
   ```bash
   cat docs/skilled-awareness/SAP-000-sap-framework/SPECIFICATION.md
   ```
   *Technical details of the SAP protocol*

4. **Check the BLUEPRINT** (1 minute):
   ```bash
   cat docs/skilled-awareness/SAP-000-sap-framework/BLUEPRINT.md
   ```
   *Step-by-step adoption guide*

### Key Concepts from SAP-000

After reading, you should understand:

- **What is a SAP?** Skilled Awareness Package - reusable protocol implementation
- **5 Artifacts**: Every SAP has 5 files (BLUEPRINT, INDEX, AGENTS, README, SPECIFICATION)
- **SAP Sets**: Curated bundles of SAPs for different use cases
- **Adoption Tiers**: Essential → Recommended → Advanced

### Quick Self-Check

Can you answer these?
- [ ] What does SAP stand for?
- [ ] How many standard artifacts does each SAP have?
- [ ] What's the difference between SAP-000 and SAP-001?
- [ ] Where are SAPs installed?
- [ ] How do you install additional SAPs?

**Answers**:
- SAP = Skilled Awareness Package
- 5 artifacts (BLUEPRINT, INDEX, AGENTS, README/SPECIFICATION.md, and one more)
- SAP-000 = Protocol framework, SAP-001 = Inbox coordination (specific implementation)
- `docs/skilled-awareness/SAP-XXX-name/`
- `python3 scripts/install-sap.py SAP-XXX`

---

## Next Steps (After This Quickstart)

### Immediate (Next 10 minutes)

**Explore other installed SAPs**:
```bash
# SAP-001: Inbox coordination protocol
cat docs/skilled-awareness/SAP-001-inbox/README.md

# SAP-009: Agent awareness (AGENTS.md pattern)
cat docs/skilled-awareness/SAP-009-agent-awareness/README.md
```

### Short-term (Next 1-2 hours)

**Read adoption blueprints**:
```bash
find docs/skilled-awareness -name "BLUEPRINT.md" -o -name "adoption-blueprint.md"
# Read each one for implementation guidance
```

**Complete minimal-entry adoption checklist**:
- See [adoption-blueprint-minimal-entry.md](../../skilled-awareness/adoption-blueprint-minimal-entry.md)

### Medium-term (Next 3-5 hours)

**Apply SAP knowledge**:
- Customize AGENTS.md for your project (from SAP-009)
- Set up inbox coordination (from SAP-001)
- Run link validation (from SAP-016)

**Install additional SAPs as needed**:
```bash
# List available SAPs
python3 scripts/install-sap.py --list

# Install specific SAP
python3 scripts/install-sap.py SAP-004  # Testing framework

# Or upgrade to larger set
python3 scripts/install-sap.py --set recommended
```

---

## Claude Code-Specific Tips

### Tip 1: Use Read Tool for SAP Documentation

You have the Read tool - use it to explore SAPs:
```bash
# Read entire SAP in one go
cat docs/skilled-awareness/SAP-000-sap-framework/*
```

### Tip 2: Leverage Glob for SAP Discovery

```bash
# Find all SAP READMEs
ls docs/skilled-awareness/*/README.md

# Find all blueprints
ls docs/skilled-awareness/*/{BLUEPRINT,adoption-blueprint}.md
```

### Tip 3: Process Inbox Coordination Requests

Once you understand SAP-001, you can:
```bash
# Check for coordination requests
ls inbox/incoming/coordination/

# Process a request using SAP-001 protocol
# (See SAP-001 BLUEPRINT for full workflow)
```

### Tip 4: Validate Your Understanding

After reading a SAP, use the ledger.md to track your progress:
```bash
cat docs/skilled-awareness/SAP-000-sap-framework/ledger.md
# Update it to mark your adoption progress
```

---

## Troubleshooting

### Issue: Installation Failed

**Check**:
```bash
# Verify prerequisites
bash scripts/validate-prerequisites.sh

# Check error messages
python3 scripts/install-sap.py --set minimal-entry 2>&1 | grep -i error
```

**Common Fixes**:
- **Permission denied**: `chmod -R u+w docs/skilled-awareness/`
- **Python version**: Upgrade to 3.8+ from [python.org](https://www.python.org/downloads/)
- **Git missing**: Install from [git-scm.com](https://git-scm.com/downloads/)

**Detailed help**: [Onboarding FAQ](../troubleshooting/onboarding-faq.md)

### Issue: Can't Find SAP Files

**Check current directory**:
```bash
pwd  # Should be chora-base root
ls sap-catalog.json  # Should exist
```

**If in wrong directory**:
```bash
cd /path/to/chora-base  # Go to root
python3 scripts/install-sap.py --set minimal-entry  # Re-run
```

### Issue: Unsure Which SAP Set to Install

**See visual decision tree**:
- [SAP Set Decision Tree](../reference/sap-set-decision-tree.md) - 3 questions → recommendation

**Default recommendation**: Start with `minimal-entry`, add more later

---

## Comparison: Claude vs Generic Guide

| Aspect | Claude Quickstart | Generic Guide |
|--------|------------------|---------------|
| **Length** | ~400 lines | 2000+ lines |
| **Time** | ~15 minutes | 2-4 hours |
| **Focus** | Fastest path to productivity | Comprehensive coverage |
| **Commands** | Copy-paste ready | Explanatory |
| **Validation** | Built-in checks | Manual verification |

**When to use generic guide**: Deep exploration, custom workflows, non-Claude agents

---

## Success Criteria

After completing this quickstart, you should be able to:

- [ ] Install a SAP set (`minimal-entry` or others)
- [ ] Validate installation succeeded
- [ ] Read SAP documentation (5 artifacts per SAP)
- [ ] Understand SAP-000 protocol framework
- [ ] Know where to find additional SAPs
- [ ] Know how to add more SAPs later

**Time to completion**: If you completed all steps in ~15 minutes, you're ready to adopt SAPs! ✅

---

## Related Resources

**For Claude Code Agents**:
- [Onboarding FAQ](../troubleshooting/onboarding-faq.md) - Troubleshooting guide
- [SAP Set Decision Tree](../reference/sap-set-decision-tree.md) - Visual flowchart
- [SAP Index](../../skilled-awareness/INDEX.md) - Complete SAP catalog

**For Deeper Learning**:
- [Install SAP Set (Full Guide)](install-sap-set.md) - Comprehensive 535-line guide
- [Agent Onboarding Guide](../guides/agent-onboarding-chora-base.md) - Complete walkthrough
- [Create Custom SAP Sets](create-custom-sap-sets.md) - Organization-specific sets

---

**Prepared by**: COORD-003 Sprint 2 - Agent-Specific Quickstarts
**Target**: 30%+ onboarding time reduction for Claude Code agents
**Feedback**: Open an issue at https://github.com/org/chora-base/issues
