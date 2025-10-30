# Adoption Blueprint: Minimal Ecosystem Entry Set

**SAP Set**: minimal-entry
**SAP Count**: 5 SAPs (SAP-000, SAP-001, SAP-009, SAP-016, SAP-002)
**Target Audience**: First-time chora-base adopters, ecosystem participants
**Adoption Time**: 3-5 hours
**Last Updated**: 2025-10-30 (COORD-003 Sprint 2)

---

## Overview

The **minimal-entry** set provides essential SAPs for quick ecosystem onboarding and cross-repo coordination. This is the recommended starting point for first-time adopters.

**What's Included**:
- SAP-000: SAP Framework & Protocols
- SAP-001: Inbox Coordination Protocol ⚠️ *Pilot*
- SAP-002: Chora-Base Meta Package
- SAP-009: Agent Awareness (AGENTS.md)
- SAP-016: Link Validation

**Key Capabilities**:
- ✅ Understand SAP framework
- ✅ Participate in cross-repo coordination
- ✅ Create agent-aware documentation
- ✅ Validate documentation quality
- ✅ Access chora-base architecture knowledge

---

## Success Criteria

Use these checklists to validate your adoption at each tier.

### Essential Tier ✅

**Time Target**: 5-10 minutes
**Goal**: SAPs installed and accessible

- [ ] Installation completed without errors
- [ ] All 5 SAP directories exist in `docs/skilled-awareness/`
- [ ] Each SAP has 5 artifacts (*.md files)
- [ ] Can read SAP-000 protocol specification
- [ ] Pre-flight validation passes: `bash scripts/validate-prerequisites.sh`

**Validation Commands**:
```bash
# Count installed SAPs (should be 5)
ls -d docs/skilled-awareness/SAP-* | wc -l

# Verify SAP-000 is readable
cat docs/skilled-awareness/SAP-000-sap-framework/README.md | head -10

# Check artifact count for each SAP (should be 5 each)
for dir in docs/skilled-awareness/SAP-*; do
    echo "$dir: $(ls $dir/*.md | wc -l) artifacts"
done
```

**Pass Criteria**: All commands execute without errors, counts match expected values

---

### Recommended Tier ⭐

**Time Target**: 30-60 minutes
**Goal**: Understand SAP concepts and patterns

- [ ] Read SAP-000 awareness guide (understand SAP framework)
- [ ] Read SAP-001 protocol spec (understand inbox coordination)
- [ ] Read SAP-009 adoption blueprint (understand AGENTS.md pattern)
- [ ] Can explain what a SAP is in your own words
- [ ] Can explain the 5-artifact structure
- [ ] Can describe the difference between SAP-000 and SAP-001
- [ ] Understand SAP dependency relationships
- [ ] Know how to install additional SAPs

**Knowledge Check Questions**:
1. What does SAP stand for?
2. What are the 5 standard artifacts in every SAP?
3. Why use SAP sets instead of installing SAPs individually?
4. What is the inbox coordination protocol used for?
5. Where would you look to understand how to adopt a specific SAP?

**Pass Criteria**: Can answer all 5 questions correctly

**Answers**:
1. Skilled Awareness Package
2. BLUEPRINT, INDEX, AGENTS, README/SPECIFICATION, Ledger
3. SAP sets are curated bundles optimized for specific use cases
4. Cross-repository coordination and capability discovery
5. The SAP's adoption-blueprint.md file

---

### Advanced Tier 🚀

**Time Target**: 3-5 hours
**Goal**: Apply SAP patterns to your project

- [ ] Customize AGENTS.md for your project (from SAP-009)
- [ ] Create inbox/CAPABILITIES/ file for your repository (from SAP-001, if applicable)
- [ ] Run link validation on your documentation (from SAP-016)
- [ ] Read all 5 SAP adoption blueprints
- [ ] Track your adoption progress in each SAP's ledger.md
- [ ] Can process a coordination request using inbox protocol
- [ ] Can install additional individual SAPs as needed
- [ ] Understand when to upgrade to larger SAP sets

**Implementation Checklist**:

**AGENTS.md Customization** (SAP-009):
```bash
# 1. Review the template
cat AGENTS.md

# 2. Customize with your project details
nano AGENTS.md
# - Update project overview
# - Add your tech stack
# - Document your directory structure
# - List common tasks
# - Describe development workflow

# 3. Validate AGENTS.md is helpful
# (Have an AI agent read it and give feedback)
```

**Inbox Coordination** (SAP-001, optional):
```bash
# 1. Create capabilities directory
mkdir -p inbox/CAPABILITIES

# 2. Create your repository's capability file
cat > inbox/CAPABILITIES/your-repo.yaml <<'YAML'
repo_id: "your-repo-name"
capabilities:
  - id: "your-repo.core.capability"
    name: "Your Core Capability"
    description: "What your repo provides"
    status: "active"

tech_stack:
  languages: ["Python"]
  frameworks: []

coordination_preferences:
  inbox_monitoring: true
  response_sla_hours: 72
YAML

# 3. Read inbox protocol documentation
cat docs/skilled-awareness/SAP-001-inbox/README.md
```

**Link Validation** (SAP-016):
```bash
# 1. Run validation on your docs
bash scripts/validate-links.sh

# 2. Fix any broken links reported
# 3. Re-run until all links valid
```

**Pass Criteria**: All implementation tasks completed, can demonstrate SAP usage

---

## Installation Guide

### Prerequisites

```bash
# Verify environment
bash scripts/validate-prerequisites.sh
```

**Required**:
- Python 3.8+
- Git 2.0+
- 100MB+ disk space

### Installation Steps

```bash
# 1. Preview installation (dry-run)
python3 scripts/install-sap.py --set minimal-entry --dry-run

# 2. Install SAP set
python3 scripts/install-sap.py --set minimal-entry

# 3. Verify installation
ls -d docs/skilled-awareness/SAP-* | wc -l  # Should output: 5
```

**Installation Time**: ~1-2 minutes (copying files)

---

## Adoption Workflow

### Phase 1: Installation & Validation (10 minutes)

1. Run pre-flight validation
2. Install minimal-entry set
3. Verify all 5 SAPs installed
4. Check Essential Tier checklist

### Phase 2: Learning & Understanding (1-2 hours)

1. Read SAP-000 (framework)
2. Read SAP-001 (inbox coordination)
3. Read SAP-009 (agent awareness)
4. Skim SAP-016 (link validation)
5. Skim SAP-002 (chora-base meta)
6. Complete Recommended Tier knowledge check

### Phase 3: Application & Integration (2-3 hours)

1. Customize AGENTS.md for your project
2. Set up inbox/ directory (if coordinating across repos)
3. Run link validation
4. Read all adoption blueprints
5. Track progress in ledgers
6. Complete Advanced Tier checklist

### Phase 4: Mastery & Expansion (Ongoing)

1. Process first coordination request
2. Install additional SAPs as needed
3. Consider upgrading to `recommended` set
4. Contribute back to ecosystem

---

## Common Patterns

### Pattern 1: Reading a SAP

```bash
# Always read in this order for fastest comprehension:
# 1. README or INDEX (overview)
# 2. adoption-blueprint.md (how to use it)
# 3. protocol-spec.md or SPECIFICATION.md (technical details)
# 4. awareness-guide.md or AGENTS.md (AI agent guidance)
# 5. ledger.md (track your progress)

# Example for SAP-000:
cat docs/skilled-awareness/SAP-000-sap-framework/README.md
cat docs/skilled-awareness/SAP-000-sap-framework/adoption-blueprint.md
```

### Pattern 2: Installing Additional SAPs

```bash
# List available SAPs
python3 scripts/install-sap.py --list

# Install a specific SAP
python3 scripts/install-sap.py SAP-004  # Testing framework

# Verify installation
ls docs/skilled-awareness/SAP-004*/
```

### Pattern 3: Upgrading to Larger Set

```bash
# Upgrade from minimal-entry to recommended
# (Only installs new SAPs, skips already-installed ones)
python3 scripts/install-sap.py --set recommended

# Verify new total (should be 10)
ls -d docs/skilled-awareness/SAP-* | wc -l
```

---

## Troubleshooting

### Issue: Installation Failed

**Check**:
```bash
bash scripts/validate-prerequisites.sh
```

**Common fixes**:
- Python version: Upgrade to 3.8+ from [python.org](https://www.python.org/downloads/)
- Permissions: `chmod -R u+w docs/skilled-awareness/`
- Disk space: `df -h .`

**Detailed help**: [Onboarding FAQ](../user-docs/troubleshooting/onboarding-faq.md)

### Issue: Missing SAPs After Installation

**Verify installation**:
```bash
python3 scripts/install-sap.py --set minimal-entry 2>&1 | grep -i error
```

**Re-install if needed**:
```bash
python3 scripts/install-sap.py SAP-000
```

### Issue: Don't Understand a SAP

**Reading order**:
1. README.md first (quick overview)
2. adoption-blueprint.md second (how to use)
3. Ask for clarification in issues/discussions

---

## Metrics & Progress Tracking

### Time Estimates

| Phase | Essential | Recommended | Advanced |
|-------|-----------|-------------|----------|
| Installation | 5-10 min | 5-10 min | 5-10 min |
| Learning | - | 1-2 hours | 1-2 hours |
| Application | - | - | 2-3 hours |
| **Total** | **10 min** | **1-2 hours** | **3-5 hours** |

### Progress Tracking

Track your progress in each SAP's ledger.md:

```bash
# Example: SAP-000 ledger
nano docs/skilled-awareness/SAP-000-sap-framework/ledger.md

# Mark sections as complete:
# - [x] Read README
# - [x] Read adoption blueprint
# - [ ] Implemented in project (pending)
```

---

## Next Steps

### After Completing Minimal-Entry

**Option 1: Add Specific SAPs**
- Need testing? Install SAP-004 (testing-framework)
- Need CI/CD? Install SAP-006 (continuous-integration)
- Need MCP servers? Install SAP-014 (mcp-server-development)

**Option 2: Upgrade to Recommended Set**
```bash
python3 scripts/install-sap.py --set recommended
```

**Option 3: Create Custom SAP Set**
- Define in `.chorabase` file
- See [Create Custom SAP Sets](../user-docs/how-to/create-custom-sap-sets.md)

---

## Related Documentation

**Quickstart Guides**:
- [Quickstart: Claude Code](../user-docs/how-to/quickstart-claude.md) - 15-minute agent onboarding
- [Quickstart: Generic AI Agent](../user-docs/how-to/quickstart-generic-ai-agent.md) - 20-minute onboarding

**Installation**:
- [Install SAP Set (Full Guide)](../user-docs/how-to/install-sap-set.md) - Comprehensive guide
- [SAP Set Decision Tree](../user-docs/reference/sap-set-decision-tree.md) - Choose the right set

**Troubleshooting**:
- [Onboarding FAQ](../user-docs/troubleshooting/onboarding-faq.md) - Common issues

**Individual SAP Blueprints**:
- [SAP-000 adoption-blueprint.md](SAP-000-sap-framework/adoption-blueprint.md)
- [SAP-001 adoption-blueprint.md](SAP-001-inbox/adoption-blueprint.md)
- [SAP-009 adoption-blueprint.md](SAP-009-agent-awareness/adoption-blueprint.md)
- [SAP-016 adoption-blueprint.md](SAP-016-link-validation-reference-management/adoption-blueprint.md)
- [SAP-002 adoption-blueprint.md](SAP-002-chora-base/adoption-blueprint.md)

---

## Summary

**minimal-entry** is the fastest path to chora-base ecosystem participation. Complete the Essential Tier in 10 minutes, Recommended Tier in 1-2 hours, or Advanced Tier in 3-5 hours depending on your goals.

**Success = Can explain SAPs + Can use inbox protocol + AGENTS.md customized**

---

**Prepared by**: COORD-003 Sprint 2 - Success Criteria Checklists
**Target**: Clear pass/fail criteria for each adoption tier
**Validation**: Measurable time targets and actionable checklists
