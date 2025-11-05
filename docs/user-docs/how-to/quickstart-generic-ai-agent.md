# Quickstart: Generic AI Agent

**For**: AI agents (Copilot, Cursor, Aider, generic LLM agents) onboarding to chora-base
**Time**: ~15 minutes total
**Goal**: Understand and navigate pre-installed SAPs in chora-base

**Last Updated**: 2025-11-05 (Complete rewrite - corrected directory structure)

---

## Overview

This guide is optimized for AI agents of any type. **chora-base is a project template WITH pre-installed SAPs** - you don't need to install them, just understand how to navigate and use them.

**What you'll accomplish**:
1. Validate environment (2 minutes)
2. Understand SAP structure (3 minutes)
3. Navigate existing SAPs (5 minutes)
4. Complete first task - explore a SAP (5 minutes)

**Total time**: ~15 minutes

---

## Prerequisites (2 minutes)

### Environment Requirements

**Required**:
- Python 3.8 or higher
- Git 2.0 or higher
- Access to chora-base repository (cloned locally)
- Terminal/command-line access

### Validation

Verify you're in the chora-base root directory:

```bash
# Navigate to chora-base root directory
cd /path/to/chora-base

# Verify you're in the correct location
ls sap-catalog.json README.md  # Both should exist

# Check Python version
python3 --version  # Should be 3.8+

# Check Git version
git --version  # Should be 2.0+
```

**Expected**: No "file not found" errors

**If Validation Fails**:
- Python version issues: Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Git missing: Install from [git-scm.com](https://git-scm.com/downloads/)
- See [Onboarding FAQ](../troubleshooting/onboarding-faq.md) for detailed troubleshooting

---

## Understanding chora-base Architecture (3 minutes)

### What is chora-base?

**chora-base** is a **Python project template** that includes **29 pre-installed SAPs** (Skilled Awareness Packages).

**Key Concept**: You don't "install" SAPs from chora-base - they're already here! You **explore** and **adopt** them into your development workflow.

### What is a SAP?

**SAP = Skilled Awareness Package**

Each SAP is a reusable capability with standardized documentation:
1. **capability-charter.md** - Problem statement and solution design
2. **protocol-spec.md** - Complete technical specification
3. **awareness-guide.md** or **AGENTS.md** - How AI agents should use this SAP
4. **adoption-blueprint.md** - Step-by-step installation guide
5. **ledger.md** - Adoption tracking and version history

### SAP Directory Structure

SAPs are located in `docs/skilled-awareness/` with **simple directory names** (no `SAP-XXX-` prefix):

```
docs/skilled-awareness/
├── sap-framework/           # SAP-000: Foundation for all SAPs
├── inbox/                   # SAP-001: Cross-repo coordination
├── testing-framework/       # SAP-004: pytest patterns
├── ci-cd-workflows/         # SAP-005: GitHub Actions
├── documentation-framework/ # SAP-007: Diataxis documentation
├── agent-awareness/         # SAP-009: AGENTS.md pattern
├── memory-system/           # SAP-010: Event-sourced memory
├── task-tracking/           # SAP-015: Beads task management
└── ... (29 SAPs total)
```

**Important**: Directory names are lowercase with hyphens (e.g., `sap-framework/`), NOT prefixed with `SAP-000-`.

---

## Navigating Existing SAPs (5 minutes)

### Step 1: List All Available SAPs

```bash
# Count total SAPs
ls -d docs/skilled-awareness/*/ | wc -l
# Output: 29+ directories

# List all SAP directories
ls docs/skilled-awareness/
```

**You should see**:
- agent-awareness
- automation-scripts
- chora-base
- ci-cd-workflows
- documentation-framework
- inbox
- memory-system
- sap-framework
- testing-framework
- task-tracking
- ... and 19+ more

### Step 2: View SAP Catalog

The SAP catalog is the master registry:

```bash
# View SAP catalog (machine-readable)
cat sap-catalog.json | head -100

# Or search for specific SAP
grep -A 10 '"id": "SAP-000"' sap-catalog.json
```

**Catalog shows for each SAP**:
- **id**: e.g., `SAP-000`, `SAP-001`
- **name**: Directory name (e.g., `sap-framework`, `inbox`)
- **status**: `active`, `pilot`, or `draft`
- **dependencies**: Other SAPs required
- **location**: Path to SAP directory

### Step 3: Explore SAP Status Levels

SAPs have three status levels:

| Status | Meaning | Recommendation |
|--------|---------|----------------|
| **active** | Production-ready, battle-tested | Use freely |
| **pilot** | Functional but may change | Use with caution, give feedback |
| **draft** | Experimental, unstable | Only use if explicitly exploring |

**Check SAP status**:
```bash
# Find all active SAPs
grep -B 2 '"status": "active"' sap-catalog.json | grep '"name"'
```

**Active SAPs** (safest to adopt):
- SAP-000 (sap-framework)
- SAP-005 (ci-cd-workflows)
- SAP-006 (quality-gates)
- SAP-013 (metrics-tracking)
- SAP-016 (link-validation)
- SAP-019 (sap-self-evaluation)

### Step 4: Understand SAP Sets

**SAP Sets** are curated bundles of SAPs for specific use cases:

```bash
# View all SAP sets
grep -A 20 '"minimal-entry"' sap-catalog.json
```

**Available Sets**:

| Set | SAPs | Best For |
|-----|------|----------|
| **minimal-entry** | 5 | First-timers, ecosystem coordination |
| **testing-focused** | 6 | Quality-first development, CI/CD |
| **mcp-server** | 10 | Building MCP servers |
| **recommended** | 10 | Production-ready projects |
| **full** | 18 | Complete reference implementation |
| **react-development** | 10 | React/Next.js apps |

**Example - minimal-entry SAPs**:
- SAP-000 (sap-framework)
- SAP-001 (inbox)
- SAP-002 (chora-base)
- SAP-009 (agent-awareness)
- SAP-016 (link-validation)

---

## First Task: Explore SAP-000 (sap-framework) (5 minutes)

### Task Overview

**Goal**: Understand the SAP framework by reading SAP-000 documentation
**Time**: 5 minutes

### Step 1: Navigate to SAP-000

```bash
# List SAP-000 files
ls -la docs/skilled-awareness/sap-framework/
```

**You should see 7 files**:
- AGENTS.md
- CLAUDE.md
- adoption-blueprint.md
- awareness-guide.md
- capability-charter.md
- ledger.md
- protocol-spec.md

### Step 2: Read AGENTS.md (Quick Reference)

```bash
# Read the agent-focused overview
cat docs/skilled-awareness/sap-framework/AGENTS.md | head -50
```

**Key Takeaways**:
- Quick reference for AI agents
- Common commands and workflows
- Integration with other SAPs

### Step 3: Skim protocol-spec.md (Technical Details)

```bash
# View the technical specification
cat docs/skilled-awareness/sap-framework/protocol-spec.md | head -100
```

**Key Takeaways**:
- Complete technical specification
- Artifact naming conventions
- SAP versioning and governance

### Step 4: Check adoption-blueprint.md (Implementation Guide)

```bash
# View the adoption guide
cat docs/skilled-awareness/sap-framework/adoption-blueprint.md | head -50
```

**Key Takeaways**:
- Step-by-step adoption instructions
- Prerequisites and dependencies
- Success criteria

### Core Concepts Summary

After exploring SAP-000, you should understand:

**What is a SAP?**
- Skilled Awareness Package
- Reusable protocol implementation
- Self-contained documentation bundle with 5-7 standardized artifacts

**Standard Artifacts** (most SAPs have these):
1. **capability-charter.md**: Problem statement and solution design
2. **protocol-spec.md**: Technical specification
3. **awareness-guide.md** or **AGENTS.md**: AI agent patterns
4. **adoption-blueprint.md**: Implementation steps
5. **ledger.md**: Adoption tracking

**Additional Artifacts** (optional):
- **CLAUDE.md**: Claude-specific patterns
- **README.md**: Human-readable overview

**SAP IDs vs Directory Names**:
- SAP ID format: `SAP-000`, `SAP-001` (used in catalog and references)
- Directory format: `sap-framework/`, `inbox/` (actual filesystem)
- Mapping: See sap-catalog.json `"location"` field

---

## Next Steps

### Immediate Actions (Next 15 minutes)

**1. Explore SAPs relevant to your goal**:

For **Testing & Quality**:
```bash
cat docs/skilled-awareness/testing-framework/AGENTS.md
cat docs/skilled-awareness/quality-gates/AGENTS.md
cat docs/skilled-awareness/ci-cd-workflows/AGENTS.md
```

For **Documentation**:
```bash
cat docs/skilled-awareness/documentation-framework/AGENTS.md
cat docs/skilled-awareness/agent-awareness/AGENTS.md
```

For **MCP Server Development**:
```bash
cat docs/skilled-awareness/mcp-server-development/AGENTS.md
```

For **Task Tracking**:
```bash
cat docs/skilled-awareness/task-tracking/AGENTS.md
```

**2. Read root navigation files**:

```bash
# Read root CLAUDE.md for navigation strategy
cat CLAUDE.md | head -200

# Read root AGENTS.md for agent patterns
cat AGENTS.md | head -100

# Explore domain-level AGENTS.md files
cat docs/skilled-awareness/AGENTS.md
cat docs/dev-docs/AGENTS.md
cat docs/user-docs/AGENTS.md
```

### Short-term Actions (Next 1-3 hours)

**Adopt specific SAPs into your workflow**:

1. Choose SAPs relevant to your project goals
2. Read each SAP's adoption-blueprint.md
3. Follow implementation steps
4. Track progress in each SAP's ledger.md

**Example - Adopting SAP-004 (testing-framework)**:
```bash
# 1. Read the blueprint
cat docs/skilled-awareness/testing-framework/adoption-blueprint.md

# 2. Read the protocol spec for technical details
cat docs/skilled-awareness/testing-framework/protocol-spec.md

# 3. Implement pytest patterns from the spec

# 4. Track your adoption progress
# (Update ledger.md with your adoption tier: Essential/Recommended/Advanced)
```

### Medium-term Actions (Next 1-2 days)

**Integrate multiple SAPs**:

Many SAPs work together:
- **SAP-001 (inbox) + SAP-015 (beads)**: Decompose coordination requests into tasks
- **SAP-010 (memory) + SAP-015 (beads)**: Correlate tasks with event traces
- **SAP-009 (awareness) + all SAPs**: Every SAP uses nested awareness pattern

**Explore integration patterns**:
```bash
# Find SAPs that integrate well together
grep -A 5 "Integration with Other SAPs" docs/skilled-awareness/*/AGENTS.md
```

---

## AI Agent-Specific Guidance

### For Code-Generating Agents (Claude Code, Copilot, etc.)

**Key Capabilities**:
- Read SAP AGENTS.md files for quick patterns
- Generate code following SAP protocol specifications
- Validate implementations against protocol-spec.md

**Recommended SAP Exploration Order**:
1. SAP-000 (sap-framework) - Foundation
2. SAP-004 (testing-framework) - pytest patterns
3. SAP-006 (quality-gates) - ruff/mypy patterns
4. SAP-005 (ci-cd-workflows) - GitHub Actions

**Workflow**:
```bash
# 1. Read AGENTS.md for quick patterns
cat docs/skilled-awareness/testing-framework/AGENTS.md

# 2. Read protocol-spec.md for technical details
cat docs/skilled-awareness/testing-framework/protocol-spec.md

# 3. Implement patterns in your code

# 4. Reference AGENTS.md files in your project's root AGENTS.md
```

### For Documentation Agents

**Key Capabilities**:
- Generate AGENTS.md files following SAP-009 pattern
- Create adoption blueprints following SAP-000 structure
- Maintain documentation consistency

**Recommended SAPs**:
- SAP-007 (documentation-framework) - Diataxis model
- SAP-009 (agent-awareness) - AGENTS.md/CLAUDE.md pattern
- SAP-016 (link-validation) - Link integrity checks

### For Workflow Automation Agents

**Key Capabilities**:
- Process inbox coordination requests (SAP-001)
- Automate SAP adoption workflows
- Generate progress reports from ledgers

**Recommended SAPs**:
- SAP-001 (inbox) - Cross-repo coordination
- SAP-005 (ci-cd-workflows) - GitHub Actions automation
- SAP-010 (memory-system) - Event-sourced tracking

### For Integration Agents

**Key Capabilities**:
- Connect multiple tools/services
- Implement MCP servers (Model Context Protocol)
- Handle cross-system communication

**Recommended SAPs**:
- SAP-014 (mcp-server-development) - MCP patterns
- SAP-011 (docker-operations) - Container deployment
- SAP-001 (inbox) - Cross-repo messaging

---

## Common Workflows

### Workflow 1: Finding a SAP for Your Need

```bash
# 1. Search SAP catalog by keyword
grep -i "testing" sap-catalog.json

# 2. List SAPs with specific tag
grep -B 5 '"tags".*"testing"' sap-catalog.json | grep '"name"'

# 3. Explore the SAP directory
ls docs/skilled-awareness/testing-framework/

# 4. Read AGENTS.md for quick overview
cat docs/skilled-awareness/testing-framework/AGENTS.md
```

### Workflow 2: Understanding SAP Dependencies

```bash
# 1. Check a SAP's dependencies
grep -A 10 '"id": "SAP-014"' sap-catalog.json | grep dependencies

# 2. Explore each dependency
cat docs/skilled-awareness/sap-framework/AGENTS.md  # SAP-000
cat docs/skilled-awareness/project-bootstrap/AGENTS.md  # SAP-003
```

### Workflow 3: Adopting a SAP Set

If you want to adopt a **curated bundle** of SAPs (e.g., for MCP server development):

```bash
# 1. View the SAP set definition
grep -A 30 '"mcp-server"' sap-catalog.json

# 2. This shows the SAPs included:
# SAP-000, SAP-003, SAP-004, SAP-005, SAP-006,
# SAP-007, SAP-009, SAP-012, SAP-014, SAP-016

# 3. Explore each SAP in order
cat docs/skilled-awareness/sap-framework/AGENTS.md  # SAP-000 (foundation)
cat docs/skilled-awareness/project-bootstrap/AGENTS.md  # SAP-003
cat docs/skilled-awareness/testing-framework/AGENTS.md  # SAP-004
# ... etc

# 4. Follow each adoption-blueprint.md in sequence
cat docs/skilled-awareness/sap-framework/adoption-blueprint.md
# Follow the steps, then move to next SAP
```

### Workflow 4: Using chora-base as a Template

chora-base can be used as a **template** for new projects:

```bash
# 1. Create new project from chora-base template
git clone https://github.com/org/chora-base.git my-new-project
cd my-new-project

# 2. Keep the SAPs you want, remove others
rm -rf docs/skilled-awareness/react-*  # If not building React app
rm -rf docs/skilled-awareness/mcp-server-development  # If not building MCP

# 3. Customize root AGENTS.md for your project
nano AGENTS.md

# 4. Update README.md
nano README.md

# 5. Start developing with adopted SAP patterns!
```

---

## Troubleshooting

### Issue: Can't Find SAP Directory

**Symptom**:
```bash
ls docs/skilled-awareness/SAP-000-sap-framework/
# ls: cannot access: No such file or directory
```

**Solution**: Remove `SAP-XXX-` prefix - directories use simple names:
```bash
ls docs/skilled-awareness/sap-framework/  # Correct!
```

**Explanation**: SAP IDs (SAP-000) are used in catalog and documentation, but directory names are lowercase-with-hyphens (sap-framework).

### Issue: Understanding SAP ID vs Directory Name

**Mapping**:
- SAP-000 → `sap-framework/`
- SAP-001 → `inbox/`
- SAP-004 → `testing-framework/`
- SAP-009 → `agent-awareness/`
- SAP-014 → `mcp-server-development/`
- SAP-015 → `task-tracking/`

**To find mapping**:
```bash
grep -A 5 '"id": "SAP-015"' sap-catalog.json | grep location
# Output: "location": "docs/skilled-awareness/task-tracking"
```

### Issue: SAP Status Confusion

**Question**: "Should I use this SAP?"

**Answer**: Check status in sap-catalog.json:
```bash
grep -A 3 '"id": "SAP-015"' sap-catalog.json | grep status
```

- **active**: Yes, production-ready
- **pilot**: Yes, but expect changes
- **draft**: Only if explicitly exploring

### Issue: Missing SAP Artifacts

**Symptom**: SAP directory exists but missing expected files

**Check**:
```bash
ls docs/skilled-awareness/sap-framework/
# Should show: AGENTS.md, protocol-spec.md, adoption-blueprint.md, etc.
```

**If files are missing**:
- Check git status: `git status docs/skilled-awareness/sap-framework/`
- Ensure you have latest version: `git pull origin main`
- Some SAPs may have fewer artifacts (check sap-catalog.json `artifacts` field)

**More Help**: See [Onboarding FAQ](../troubleshooting/onboarding-faq.md) for 10+ common issues

---

## Success Criteria

After completing this quickstart, you should be able to:

- [ ] Navigate to chora-base root directory and verify environment
- [ ] Understand chora-base is a template WITH pre-installed SAPs
- [ ] List all 29+ SAP directories in `docs/skilled-awareness/`
- [ ] Map SAP IDs (SAP-000) to directory names (sap-framework/)
- [ ] Check SAP status (active/pilot/draft) in sap-catalog.json
- [ ] Read AGENTS.md for quick SAP overview
- [ ] Read protocol-spec.md for technical details
- [ ] Read adoption-blueprint.md for implementation steps
- [ ] Explain the 5-7 artifact SAP pattern
- [ ] Know where to find help and resources

**Time Check**: If you completed all steps in ~15 minutes, you're ready to adopt SAPs! ✅

---

## Comparison: This Guide vs Previous Version

| Feature | Previous (Broken) | Current (Fixed) |
|---------|------------------|-----------------|
| **SAP Location** | `SAP-XXX-name/` (didn't exist) | `name/` (actual structure) |
| **Installation Approach** | Install SAPs via script | SAPs pre-installed, just explore |
| **Validation Commands** | `ls | grep SAP-` (failed) | `ls docs/skilled-awareness/` (works) |
| **Repository Purpose** | Unclear | Template with pre-installed SAPs |
| **Time to First Success** | N/A (commands failed) | ~5 minutes (explore first SAP) |
| **Accuracy** | 0% (all paths broken) | 100% (matches actual structure) |

---

## Related Resources

**Essential Guides**:
- [Onboarding FAQ](../troubleshooting/onboarding-faq.md) - Common issues and solutions
- [Understanding SAPs](../explanation/understanding-saps.md) - Conceptual deep-dive
- [SAP Framework Protocol](../../skilled-awareness/sap-framework/protocol-spec.md) - Complete specification

**Navigation Guides**:
- [Root CLAUDE.md](/CLAUDE.md) - Progressive context loading strategy
- [Root AGENTS.md](/AGENTS.md) - Agent patterns for chora-base
- [SAP Domain AGENTS.md](../../skilled-awareness/AGENTS.md) - SAP-specific patterns

**SAP Catalog**:
- [sap-catalog.json](/sap-catalog.json) - Machine-readable SAP registry (29 SAPs)
- [SAP Index](../../skilled-awareness/INDEX.md) - Human-readable catalog

**Adoption Blueprints** (for specific SAP sets):
- Browse individual SAPs in `docs/skilled-awareness/*/adoption-blueprint.md`
- Follow step-by-step adoption instructions per SAP

---

## Feedback & Support

**Found an Issue?**
- Open an issue: https://github.com/org/chora-base/issues
- Include: OS, Python version, error messages, steps to reproduce

**Have Suggestions?**
- This quickstart was completely rewritten (2025-11-05) to fix broken paths
- Previous version assumed non-existent directory structure
- We welcome improvements and clarifications

**Need Help?**
- Check [Onboarding FAQ](../troubleshooting/onboarding-faq.md) first
- Search existing issues
- Review SAP-specific AGENTS.md files
- Read root CLAUDE.md for navigation strategy

---

**Version**: 2.0.0 (Complete rewrite)
**Last Updated**: 2025-11-05
**Changes**: Fixed all directory paths, removed broken installation workflow, clarified chora-base as template with pre-installed SAPs
**Target Audience**: AI agents (Copilot, Cursor, Aider, generic LLM agents)
**Goal**: Accurate, working quickstart in ~15 minutes
