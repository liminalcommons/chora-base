# Quickstart: Generic AI Agent

**For**: AI agents (Copilot, Cursor, Aider, generic LLM agents) onboarding to chora-base
**Time**: ~20 minutes total
**Goal**: Get productive with chora-base SAPs quickly

**Last Updated**: 2025-10-30 (COORD-003 Sprint 2)

---

## Overview

This guide is optimized for AI agents of any type. It's 60%+ shorter than comprehensive documentation, focusing on essential onboarding steps.

**What you'll accomplish**:
1. Validate environment (2 minutes)
2. Choose and install a SAP set (8 minutes)
3. Verify installation (3 minutes)
4. Complete first task (7 minutes)

**Total time**: ~20 minutes

---

## Prerequisites (2 minutes)

### Environment Requirements

**Required**:
- Python 3.8 or higher
- Git 2.0 or higher
- Access to chora-base repository (cloned locally)
- Terminal/command-line access

**Optional**:
- PyYAML (for custom SAP sets)

### Validation

Run the pre-flight validator:

```bash
# Navigate to chora-base root directory
cd /path/to/chora-base

# Verify you're in the correct location
ls sap-catalog.json  # Should exist

# Run validation
bash scripts/validate-prerequisites.sh
```

**Expected Output**:
```
✓ Python 3.12.0 (OK)
✓ Git 2.39.5 (OK)
✓ Directory structure (OK)
✓ SAP catalog (OK)
✓ Disk space: 62254MB available (OK)
✓ Write permissions (OK)
✓ install-sap.py script (OK)

✓ Pre-flight validation PASSED
```

**If Validation Fails**:
- Python version issues: Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Git missing: Install from [git-scm.com](https://git-scm.com/downloads/)
- Permission errors: Run `chmod -R u+w docs/skilled-awareness/`
- See [Onboarding FAQ](../troubleshooting/onboarding-faq.md) for detailed troubleshooting

---

## Choose SAP Set (3 minutes)

### Decision Tree

Answer these questions to choose your SAP set:

**Question 1: Are you new to chora-base?**
- **YES** → Use `minimal-entry` (5 SAPs, 3-5 hours adoption)
- **NO** → Continue to Question 2

**Question 2: What's your primary goal?**
- **Testing & Quality** → Use `testing-focused` (6 SAPs, 4-6 hours)
- **MCP Server Development** → Use `mcp-server` (10 SAPs, ~1 day)
- **Production Project** → Use `recommended` (10 SAPs, 1-2 days)
- **Complete Reference** → Use `full` (18 SAPs, 2-4 weeks)

### SAP Set Quick Reference

| Set | SAPs | Time | Best For |
|-----|------|------|----------|
| **minimal-entry** | 5 | 3-5h | First-timers, ecosystem coordination |
| **testing-focused** | 6 | 4-6h | Quality-first development, CI/CD |
| **mcp-server** | 10 | ~1d | Building MCP servers with FastMCP |
| **recommended** | 10 | 1-2d | Production-ready projects |
| **full** | 18 | 2-4w | Complete reference, all capabilities |

**Default Recommendation**: Start with `minimal-entry`

**Need more help?** See [SAP Set Decision Tree](../reference/sap-set-decision-tree.md) for visual flowchart

### List Available Sets

```bash
python3 scripts/install-sap.py --list-sets
```

---

## Installation (5 minutes)

### Step 1: Dry-Run (Recommended)

Preview what will be installed without making changes:

```bash
python3 scripts/install-sap.py --set minimal-entry --dry-run
```

**Output Shows**:
- Which SAPs will be installed
- Which directories will be created
- Which system files will be copied
- Any warnings (e.g., Pilot status SAPs)

### Step 2: Install

```bash
python3 scripts/install-sap.py --set minimal-entry
```

**What Happens**:
- SAPs are copied to `docs/skilled-awareness/`
- Progress bar shows real-time status
- System files are installed (if applicable)
- Validation runs automatically

**Example Output**:
```
Installing SAP Set: Minimal Ecosystem Entry
SAPs: 5 (SAP-000, SAP-001, SAP-009, SAP-016, SAP-002)

Installing SAP-000: sap-framework
  ✓ Copied SAP directory
  ✓ Validation passed

Installing SAP-001: inbox-coordination
  Dependency: SAP-000 already installed ✓
  ⚠ Note: Pilot status - may undergo changes
  ✓ Copied SAP directory
  ✓ Copied system files
  ✓ Validation passed

[====================================>] 5/5 SAPs (100%)

✅ Set installation complete!
```

**Installation Time**: ~1-2 minutes (actual copying, not adoption time)

### Step 3: Handle Warnings

Some SAPs may show warnings:
- **Pilot status**: SAP is functional but may change in future versions
- **Missing dependencies**: Usually auto-installed, but verify

These are informational - installation can proceed.

---

## Validation (3 minutes)

### Check 1: Verify SAP Directories

```bash
ls docs/skilled-awareness/ | grep SAP-
```

**For minimal-entry, expect 5 directories**:
```
SAP-000-sap-framework/
SAP-001-inbox/
SAP-002-chora-base/
SAP-009-agent-awareness/
SAP-016-link-validation-reference-management/
```

**Count verification**:
```bash
ls -d docs/skilled-awareness/SAP-* | wc -l
# Output should match your SAP set size
# minimal-entry: 5
# testing-focused: 6
# recommended: 10
# full: 18
```

### Check 2: Verify SAP Artifacts

Each SAP should have 5 artifacts:

```bash
ls docs/skilled-awareness/SAP-000-sap-framework/
```

**Expected files** (names may vary slightly):
- `BLUEPRINT.md` or `adoption-blueprint.md`
- `INDEX.md` or `awareness-guide.md`
- `AGENTS.md` or `capability-charter.md`
- `README.md` or `protocol-spec.md`
- `SPECIFICATION.md` or `ledger.md`

**Verify all SAPs**:
```bash
for dir in docs/skilled-awareness/SAP-*; do
    echo "Checking $dir..."
    ls "$dir"/*.md | wc -l
    # Should output: 5
done
```

### Check 3: Test File Access

```bash
cat docs/skilled-awareness/SAP-000-sap-framework/README.md | head -20
```

**Expected**: Readable markdown content (not errors)

**If Validation Fails**: See [Onboarding FAQ - Validation Issues](../troubleshooting/onboarding-faq.md#validation-issues)

---

## First Task: Understand the SAP Framework (7 minutes)

### Task Overview

**Goal**: Understand what SAPs are and how they work
**SAP to Read**: SAP-000 (protocol specification)
**Time**: 5-7 minutes

### Reading Order

#### 1. README.md (2 minutes)
```bash
cat docs/skilled-awareness/SAP-000-sap-framework/README.md
```

**Key Takeaways**:
- What is a Skilled Awareness Package (SAP)?
- Why use SAPs?
- How SAPs are structured

#### 2. INDEX.md (2 minutes)
```bash
cat docs/skilled-awareness/SAP-000-sap-framework/INDEX.md
```

**Key Takeaways**:
- The 5-artifact structure (BLUEPRINT, INDEX, AGENTS, README, SPECIFICATION)
- SAP metadata and organization
- Quick reference information

#### 3. SPECIFICATION.md (3 minutes - skim)
```bash
cat docs/skilled-awareness/SAP-000-sap-framework/SPECIFICATION.md
```

**Key Takeaways**:
- Technical details of SAP protocol
- File naming conventions
- Governance and versioning

#### 4. BLUEPRINT.md (Optional - for later)
```bash
cat docs/skilled-awareness/SAP-000-sap-framework/BLUEPRINT.md
```

**What it contains**: Step-by-step adoption instructions

### Core Concepts

After reading SAP-000, you should understand:

**What is a SAP?**
- Skilled Awareness Package
- Reusable protocol implementation
- Self-contained documentation bundle

**5 Standard Artifacts** (every SAP has these):
1. **BLUEPRINT.md**: Step-by-step adoption guide
2. **INDEX.md**: Overview and quick reference
3. **AGENTS.md**: How AI agents should use this SAP
4. **README.md** or **SPECIFICATION.md**: Technical specification
5. **Ledger**: Progress tracking

**SAP Sets**:
- Curated bundles of SAPs for specific use cases
- `minimal-entry`, `testing-focused`, `mcp-server`, `recommended`, `full`
- Installable with single command

**Adoption Tiers**:
- **Essential**: Basic setup (~5 minutes)
- **Recommended**: Standard usage (~15 minutes)
- **Advanced**: Full integration (~30 minutes)

### Knowledge Check

Can you answer these questions?

- [ ] What does SAP stand for?
- [ ] How many artifacts does each SAP have?
- [ ] Where are SAPs installed in the directory structure?
- [ ] What's the difference between SAP-000 and SAP-001?
- [ ] How do you install additional individual SAPs?

**Answers**:
- SAP = Skilled Awareness Package
- 5 artifacts per SAP
- `docs/skilled-awareness/SAP-XXX-name/`
- SAP-000 = Framework/protocol, SAP-001 = Inbox coordination (specific implementation)
- `python3 scripts/install-sap.py SAP-XXX`

---

## Next Steps

### Immediate Actions (Next 15 minutes)

**Explore other installed SAPs**:

```bash
# If you installed minimal-entry, explore:

# SAP-001: Inbox coordination protocol
cat docs/skilled-awareness/SAP-001-inbox/README.md

# SAP-009: Agent awareness (AGENTS.md pattern)
cat docs/skilled-awareness/SAP-009-agent-awareness/README.md

# SAP-016: Link validation
cat docs/skilled-awareness/SAP-016-link-validation-reference-management/README.md
```

**Read adoption blueprints**:
```bash
# Find all blueprints
find docs/skilled-awareness -name "*blueprint.md"

# Read them for implementation guidance
```

### Short-term Actions (Next 1-3 hours)

**Complete adoption tier checklist**:
- See your SAP set's adoption blueprint:
  - [minimal-entry](../../skilled-awareness/adoption-blueprint-minimal-entry.md)
  - [testing-focused](../../skilled-awareness/adoption-blueprint-testing-focused.md)
  - [recommended](../../skilled-awareness/adoption-blueprint-recommended.md)

**Apply SAP patterns**:
- Customize AGENTS.md for your project (from SAP-009)
- Set up inbox/ directory (from SAP-001, if applicable)
- Run link validation (from SAP-016, if installed)

### Medium-term Actions (Next 1-2 days)

**Install additional SAPs**:
```bash
# List all available SAPs
python3 scripts/install-sap.py --list

# Install specific SAP by ID
python3 scripts/install-sap.py SAP-004  # Testing framework
python3 scripts/install-sap.py SAP-014  # MCP server

# Or upgrade to larger set (additive, won't reinstall existing)
python3 scripts/install-sap.py --set recommended
```

**Implement SAP workflows**:
- Follow each SAP's BLUEPRINT.md for adoption steps
- Track progress in each SAP's ledger.md
- Customize system files as needed

---

## AI Agent-Specific Guidance

### For Code-Generating Agents

**Key Capabilities**:
- Read SAP documentation files
- Generate code following SAP patterns
- Validate implementations against specifications

**Recommended SAPs**:
- SAP-003: Project Bootstrap (scaffolding patterns)
- SAP-004: Testing Framework (pytest patterns)
- SAP-005: Python Type Checking (mypy/pyright)

### For Documentation Agents

**Key Capabilities**:
- Generate AGENTS.md files
- Create adoption blueprints
- Maintain documentation consistency

**Recommended SAPs**:
- SAP-007: Documentation Framework (Sphinx/MkDocs)
- SAP-009: Agent Awareness (AGENTS.md pattern)
- SAP-016: Link Validation (quality checks)

### For Workflow Automation Agents

**Key Capabilities**:
- Process inbox coordination requests
- Automate SAP adoption workflows
- Generate progress reports

**Recommended SAPs**:
- SAP-001: Inbox Coordination (cross-repo workflow)
- SAP-006: Continuous Integration (GitHub Actions)
- SAP-010: SDLC-Flow (8-phase development)

### For Integration Agents

**Key Capabilities**:
- Connect multiple tools/services
- Implement MCP servers
- Handle cross-system communication

**Recommended SAPs**:
- SAP-014: MCP Server Implementation
- SAP-015: FastMCP Patterns
- SAP-008: Deployment Patterns (Docker, Railway)

---

## Common Workflows

### Workflow 1: Adding a New SAP

```bash
# 1. List available SAPs
python3 scripts/install-sap.py --list

# 2. Install specific SAP
python3 scripts/install-sap.py SAP-004

# 3. Verify installation
ls docs/skilled-awareness/SAP-004*/

# 4. Read the blueprint
cat docs/skilled-awareness/SAP-004*/BLUEPRINT.md
```

### Workflow 2: Upgrading to Larger Set

```bash
# Started with minimal-entry, now want recommended

# 1. Check what's currently installed
ls -d docs/skilled-awareness/SAP-* | wc -l  # Shows: 5

# 2. Install recommended set (additive)
python3 scripts/install-sap.py --set recommended

# 3. Verify new total
ls -d docs/skilled-awareness/SAP-* | wc -l  # Shows: 10

# Only new SAPs were installed (5 added, 5 skipped)
```

### Workflow 3: Customizing for Your Project

```bash
# 1. Update AGENTS.md with your project details
# (This file was installed by SAP-009)
nano AGENTS.md

# 2. Create inbox capabilities file (if using SAP-001)
mkdir -p inbox/CAPABILITIES
nano inbox/CAPABILITIES/your-project.yaml

# 3. Validate links (if you installed SAP-016)
python3 scripts/validate-links.sh
```

---

## Troubleshooting

### Issue: Command Not Found

**Symptom**:
```
python: command not found
```

**Solution**: Use `python3` instead:
```bash
python3 scripts/install-sap.py --set minimal-entry
```

### Issue: Permission Denied

**Symptom**:
```
PermissionError: [Errno 13] Permission denied
```

**Solution**: Fix file permissions:
```bash
chmod -R u+w docs/skilled-awareness/
```

**Don't use sudo** unless absolutely necessary (it can cause ownership issues)

### Issue: SAP Already Installed

**Symptom**:
```
✓ SAP-000 (sap-framework) already installed - skipping
```

**Explanation**: This is normal - the installer skips SAPs that already exist

**To Force Reinstall**:
```bash
rm -rf docs/skilled-awareness/SAP-000-sap-framework/
python3 scripts/install-sap.py SAP-000
```

### Issue: Missing sap-catalog.json

**Symptom**:
```
Error: Catalog not found: sap-catalog.json
```

**Solution**: Ensure you're in chora-base root directory:
```bash
pwd  # Should end with /chora-base
cd /path/to/chora-base
python3 scripts/install-sap.py --set minimal-entry
```

### Issue: Installation Hangs

**Symptom**: Command doesn't complete after several minutes

**Solution**:
1. Press Ctrl+C to cancel
2. Check error messages
3. Verify disk space: `df -h .`
4. Check permissions: `ls -la docs/`
5. Run pre-flight validation: `bash scripts/validate-prerequisites.sh`

**More Help**: See [Onboarding FAQ](../troubleshooting/onboarding-faq.md) for 10+ common issues

---

## Success Criteria

After completing this quickstart, you should be able to:

- [ ] Validate your environment with pre-flight checks
- [ ] Choose appropriate SAP set for your needs
- [ ] Install a SAP set successfully
- [ ] Verify installation with multiple checks
- [ ] Read and understand SAP documentation structure
- [ ] Explain the 5-artifact SAP pattern
- [ ] Install additional individual SAPs
- [ ] Know where to find help and resources

**Time Check**: If you completed all steps in ~20 minutes, you're ready to adopt SAPs! ✅

**Slower than Expected?** That's okay - comprehension is more important than speed

---

## Comparison: Agent Types

| Feature | Claude Code | Generic AI | Human Developer |
|---------|-------------|------------|-----------------|
| **Quickstart Time** | ~15 min | ~20 min | ~30 min |
| **Tool Access** | Read, Bash, etc. | Varies | Terminal |
| **Validation** | Built-in checks | Manual | Manual |
| **Learning Style** | Fast scanning | Varies | Thorough reading |
| **Guide Length** | 400 lines | 500 lines | 2000+ lines |

---

## Related Resources

**Essential Guides**:
- [Onboarding FAQ](../troubleshooting/onboarding-faq.md) - Common issues and solutions
- [SAP Set Decision Tree](../reference/sap-set-decision-tree.md) - Visual flowchart
- [Install SAP Set (Full Guide)](install-sap-set.md) - Comprehensive 535-line guide

**SAP Documentation**:
- [SAP Index](../../skilled-awareness/INDEX.md) - Complete SAP catalog
- [Adoption Blueprints](../../skilled-awareness/) - Per-set adoption guides

**For Specific Goals**:
- Testing focus: [testing-focused adoption blueprint](../../skilled-awareness/adoption-blueprint-testing-focused.md)
- MCP servers: [mcp-server adoption blueprint](../../skilled-awareness/adoption-blueprint-mcp-server.md)
- Production projects: [recommended adoption blueprint](../../skilled-awareness/adoption-blueprint-recommended.md)

---

## Feedback & Support

**Found an Issue?**
- Open an issue: https://github.com/org/chora-base/issues
- Include: OS, Python version, error messages, steps to reproduce

**Have Suggestions?**
- This quickstart was created based on pilot feedback (COORD-003)
- We welcome improvements and clarifications

**Need Help?**
- Check [Onboarding FAQ](../troubleshooting/onboarding-faq.md) first
- Search existing issues
- Ask in discussions (if enabled)

---

**Prepared by**: COORD-003 Sprint 2 - Agent-Specific Quickstarts
**Target Audience**: AI agents (Copilot, Cursor, Aider, generic LLM agents)
**Goal**: 60%+ reduction in documentation reading time (500 lines vs 2000+)
**Success Metric**: 30%+ faster onboarding vs generic comprehensive guide
