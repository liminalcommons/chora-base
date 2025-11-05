# Quickstart: Claude Code Agent

**For**: Claude Code AI agents onboarding to chora-base
**Time**: ~12 minutes total
**Goal**: Leverage Claude Code's Read/Bash tools to navigate pre-installed SAPs

**Last Updated**: 2025-11-05 (Complete rewrite - corrected directory structure + Claude-specific optimizations)

---

## Overview

This guide is optimized specifically for **Claude Code agents**. **chora-base is a project template WITH 29 pre-installed SAPs** - you leverage Claude Code's tools to explore and adopt them.

**What you'll accomplish**:
1. Validate environment with Bash tool (1 minute)
2. Understand SAP structure (2 minutes)
3. Navigate SAPs with Read tool (4 minutes)
4. Complete first task: Explore SAP-000 (5 minutes)

**Total time**: ~12 minutes

**Claude Code Advantage**: 3 minutes faster than generic guide thanks to Read/Bash tools

---

## Prerequisites (1 minute)

### Quick Environment Check

Use Claude Code's **Bash tool** to validate:

```bash
# Verify you're in chora-base root
pwd  # Should end with /chora-base

# Check key files exist
ls sap-catalog.json README.md CLAUDE.md  # All should exist

# Verify Python and Git
python3 --version  # Should be 3.8+
git --version  # Should be 2.0+
```

**Expected**: No "file not found" errors, versions meet requirements

**If validation fails**: See [Onboarding FAQ](../troubleshooting/onboarding-faq.md#installation-issues)

---

## Understanding chora-base (2 minutes)

### What is chora-base?

**chora-base** is a **Python project template** that includes **29 pre-installed SAPs**.

**Key Concept for Claude Code**:
- ✅ SAPs are already installed - use **Read tool** to explore them
- ✅ Use **Bash tool** to navigate directories
- ❌ No need to run installation scripts (SAPs pre-exist)

### SAP Structure

**SAP = Skilled Awareness Package**

Each SAP has 5-7 standardized artifacts:
1. **capability-charter.md** - Problem statement, solution design
2. **protocol-spec.md** - Complete technical specification
3. **AGENTS.md** or **awareness-guide.md** - AI agent patterns
4. **adoption-blueprint.md** - Step-by-step adoption guide
5. **ledger.md** - Adoption tracking and version history
6. **CLAUDE.md** (optional) - Claude-specific patterns

### Directory Structure

SAPs live in `docs/skilled-awareness/` with **simple names** (no `SAP-XXX-` prefix):

```
docs/skilled-awareness/
├── sap-framework/           # SAP-000: Foundation
├── inbox/                   # SAP-001: Cross-repo coordination
├── testing-framework/       # SAP-004: pytest patterns
├── ci-cd-workflows/         # SAP-005: GitHub Actions
├── agent-awareness/         # SAP-009: AGENTS.md/CLAUDE.md pattern
├── memory-system/           # SAP-010: Event-sourced memory
├── task-tracking/           # SAP-015: Beads task management
└── ... (22 more SAPs)
```

**Important**: Use lowercase-with-hyphens (e.g., `sap-framework/`), NOT `SAP-000-sap-framework/`

---

## Navigating SAPs with Claude Code Tools (4 minutes)

### Step 1: List All SAPs (Bash Tool)

```bash
# Count total SAPs
ls -d docs/skilled-awareness/*/ | wc -l
# Output: 29+ directories

# List all SAP directories
ls docs/skilled-awareness/
```

**You should see**:
- agent-awareness
- ci-cd-workflows
- documentation-framework
- inbox
- mcp-server-development
- sap-framework
- task-tracking
- testing-framework
- ... (21 more)

### Step 2: View SAP Catalog (Read Tool)

Use Claude Code's **Read tool** to examine the catalog:

```bash
# Or use Bash to preview
cat sap-catalog.json | head -100
```

**Catalog structure** (for each SAP):
```json
{
  "id": "SAP-000",
  "name": "sap-framework",
  "full_name": "SAP Framework",
  "status": "active",
  "version": "1.0.0",
  "location": "docs/skilled-awareness/sap-framework",
  "dependencies": [],
  "tags": ["meta", "foundation"]
}
```

### Step 3: Check SAP Status Levels

SAPs have three status levels:

| Status | Meaning | Recommendation |
|--------|---------|----------------|
| **active** | Production-ready, battle-tested | Use freely |
| **pilot** | Functional but may change | Use with caution, give feedback |
| **draft** | Experimental, unstable | Only use if explicitly exploring |

**Find active SAPs** (safest to adopt):
```bash
grep -B 2 '"status": "active"' sap-catalog.json | grep '"name"'
```

**Active SAPs**:
- SAP-000 (sap-framework)
- SAP-005 (ci-cd-workflows)
- SAP-006 (quality-gates)
- SAP-013 (metrics-tracking)
- SAP-016 (link-validation)
- SAP-019 (sap-self-evaluation)

### Step 4: Understand SAP Sets (Curated Bundles)

**SAP Sets** are pre-defined bundles for specific use cases:

```bash
# View SAP set definitions
grep -A 30 '"sap_sets"' sap-catalog.json
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
- SAP-000 (sap-framework) → `sap-framework/`
- SAP-001 (inbox) → `inbox/`
- SAP-002 (chora-base) → `chora-base/`
- SAP-009 (agent-awareness) → `agent-awareness/`
- SAP-016 (link-validation) → `link-validation-reference-management/`

---

## First Task: Explore SAP-000 with Read Tool (5 minutes)

### Task Overview

**Goal**: Understand the SAP framework by reading SAP-000 documentation
**Time**: 5 minutes
**Claude Code Advantage**: Use Read tool to quickly scan artifacts

### Step 1: List SAP-000 Files (Bash)

```bash
ls -la docs/skilled-awareness/sap-framework/
```

**You should see 7 files**:
- AGENTS.md (agent patterns)
- CLAUDE.md (Claude-specific patterns)
- adoption-blueprint.md (step-by-step adoption)
- awareness-guide.md (operating patterns)
- capability-charter.md (problem/solution design)
- ledger.md (adoption tracking)
- protocol-spec.md (complete technical spec)

### Step 2: Read AGENTS.md (Quick Reference)

**Use Read tool** to scan the agent-focused overview:

```
Read file: docs/skilled-awareness/sap-framework/AGENTS.md
```

**Key Takeaways**:
- Quick reference for AI agents
- Common commands and workflows
- Integration with other SAPs

### Step 3: Read protocol-spec.md (Technical Details)

**Use Read tool** to get complete technical specification:

```
Read file: docs/skilled-awareness/sap-framework/protocol-spec.md
```

**Key Takeaways**:
- Technical specification of SAP protocol
- Artifact naming conventions (capability-charter.md, protocol-spec.md, etc.)
- SAP versioning and governance

### Step 4: Skim adoption-blueprint.md (Implementation Guide)

**Use Read tool** to understand adoption process:

```
Read file: docs/skilled-awareness/sap-framework/adoption-blueprint.md
```

**Key Takeaways**:
- Step-by-step adoption instructions
- Prerequisites and dependencies
- Success criteria for adoption

### Step 5: Check CLAUDE.md (Claude-Specific Patterns)

**SAP-000 has Claude-specific guidance!**

```
Read file: docs/skilled-awareness/sap-framework/CLAUDE.md
```

**Key Takeaways**:
- Claude Code-specific navigation patterns
- Progressive context loading strategy
- Tool usage recommendations (Read, Bash, Glob, Grep)

### Core Concepts Summary

After exploring SAP-000, you should understand:

**What is a SAP?**
- Skilled Awareness Package
- Reusable protocol implementation
- Self-contained documentation bundle with 5-7 standardized artifacts

**Standard Artifacts** (most SAPs have):
1. **capability-charter.md**: Problem statement and solution design
2. **protocol-spec.md**: Complete technical specification
3. **AGENTS.md** or **awareness-guide.md**: AI agent patterns
4. **adoption-blueprint.md**: Step-by-step adoption guide
5. **ledger.md**: Adoption tracking and version history

**Optional Artifacts**:
- **CLAUDE.md**: Claude-specific patterns (highly valuable!)
- **README.md**: Human-readable overview

**SAP IDs vs Directory Names**:
- SAP ID format: `SAP-000`, `SAP-001` (used in catalog and references)
- Directory format: `sap-framework/`, `inbox/` (actual filesystem)
- Mapping: See `sap-catalog.json` → `"location"` field

---

## Next Steps

### Immediate Actions (Next 10 minutes)

**1. Explore SAPs with Claude-specific guidance**:

SAPs with CLAUDE.md files (prioritize these!):
```bash
# Find all SAPs with Claude-specific docs
find docs/skilled-awareness -name "CLAUDE.md"
```

**Read these first** (have Claude optimizations):
```
Read file: docs/skilled-awareness/sap-framework/CLAUDE.md
Read file: docs/skilled-awareness/agent-awareness/CLAUDE.md
Read file: docs/skilled-awareness/inbox/CLAUDE.md
```

**2. Explore SAPs relevant to your goal**:

For **Testing & Quality**:
```
Read file: docs/skilled-awareness/testing-framework/AGENTS.md
Read file: docs/skilled-awareness/quality-gates/AGENTS.md
Read file: docs/skilled-awareness/ci-cd-workflows/AGENTS.md
```

For **Documentation**:
```
Read file: docs/skilled-awareness/documentation-framework/AGENTS.md
Read file: docs/skilled-awareness/agent-awareness/AGENTS.md
```

For **MCP Server Development**:
```
Read file: docs/skilled-awareness/mcp-server-development/AGENTS.md
```

For **Task Tracking** (persistent memory across sessions):
```
Read file: docs/skilled-awareness/task-tracking/AGENTS.md
```

**3. Read root navigation files**:

```
Read file: /CLAUDE.md  # Root navigation for Claude agents
Read file: /AGENTS.md  # Project-wide agent patterns
Read file: docs/skilled-awareness/AGENTS.md  # SAP domain patterns
```

### Short-term Actions (Next 1-3 hours)

**Adopt specific SAPs into your workflow**:

1. Choose SAPs relevant to your project goals
2. Use **Read tool** to read each SAP's adoption-blueprint.md
3. Follow implementation steps
4. Track progress in each SAP's ledger.md

**Example - Adopting SAP-004 (testing-framework)**:
```
# 1. Read the blueprint
Read file: docs/skilled-awareness/testing-framework/adoption-blueprint.md

# 2. Read the protocol spec for technical details
Read file: docs/skilled-awareness/testing-framework/protocol-spec.md

# 3. Implement pytest patterns from the spec
# (Use Write/Edit tools to create tests)

# 4. Track your adoption progress
# (Update ledger.md with your adoption tier: Essential/Recommended/Advanced)
```

### Medium-term Actions (Next 1-2 days)

**Integrate multiple SAPs**:

Many SAPs work together:
- **SAP-001 (inbox) + SAP-015 (task-tracking)**: Decompose coordination requests into beads tasks
- **SAP-010 (memory-system) + SAP-015 (task-tracking)**: Correlate tasks with event traces
- **SAP-009 (agent-awareness) + all SAPs**: Every SAP uses nested awareness pattern

**Explore integration patterns**:
```bash
# Find SAPs that integrate well together
grep -A 5 "Integration with Other SAPs" docs/skilled-awareness/*/AGENTS.md
```

---

## Claude Code-Specific Tips

### Tip 1: Use Read Tool for Entire SAPs

Claude Code's **Read tool** can handle large files - read entire SAP artifacts:

```
Read file: docs/skilled-awareness/sap-framework/protocol-spec.md
# Returns full specification, not truncated
```

### Tip 2: Use Glob for SAP Discovery

**Glob tool** quickly finds patterns across SAPs:

```
Glob pattern: docs/skilled-awareness/*/CLAUDE.md
# Finds all SAPs with Claude-specific guidance
```

```
Glob pattern: docs/skilled-awareness/*/adoption-blueprint.md
# Finds all adoption guides
```

### Tip 3: Use Grep for Keyword Search

**Grep tool** searches SAP content:

```
Grep pattern: "pytest" in docs/skilled-awareness/
# Finds all SAPs mentioning pytest
```

```
Grep pattern: "MCP" in docs/skilled-awareness/
# Finds MCP-related SAPs
```

### Tip 4: Leverage Bash for Navigation

**Bash tool** quickly explores structure:

```bash
# Find all SAPs with specific tag
grep -B 5 '"tags".*"testing"' sap-catalog.json | grep '"name"'

# Check SAP dependencies
grep -A 10 '"id": "SAP-014"' sap-catalog.json | grep dependencies

# List SAPs by status
grep -B 2 '"status": "pilot"' sap-catalog.json | grep '"name"'
```

### Tip 5: Use Task Tool for Complex Exploration

For **open-ended exploration**, use **Task tool with Explore subagent**:

```
Task: Explore all SAPs related to testing and find best adoption order
Subagent: Explore
Thoroughness: medium
```

### Tip 6: Persistent Memory with SAP-015 (Beads)

If you adopt **SAP-015 (task-tracking)**, Claude Code can maintain **persistent memory across sessions**:

```bash
# Check for unblocked work from previous session
bd ready --json

# Show task details
bd show {task_id} --json

# Update task status
bd update {task_id} --status in_progress
```

**This eliminates context re-establishment overhead between Claude Code sessions!**

---

## Common Workflows for Claude Code

### Workflow 1: Finding a SAP for Your Need

```
# 1. Use Grep to search catalog by keyword
Bash: grep -i "testing" sap-catalog.json

# 2. Use Glob to find the SAP directory
Glob: docs/skilled-awareness/testing-framework/

# 3. Use Read to explore AGENTS.md
Read file: docs/skilled-awareness/testing-framework/AGENTS.md

# 4. Use Read to get technical details
Read file: docs/skilled-awareness/testing-framework/protocol-spec.md
```

### Workflow 2: Understanding SAP Dependencies

```
# 1. Grep for SAP dependencies
Bash: grep -A 10 '"id": "SAP-014"' sap-catalog.json | grep dependencies

# 2. Read each dependency's AGENTS.md
Read file: docs/skilled-awareness/sap-framework/AGENTS.md  # SAP-000
Read file: docs/skilled-awareness/project-bootstrap/AGENTS.md  # SAP-003
Read file: docs/skilled-awareness/testing-framework/AGENTS.md  # SAP-004
```

### Workflow 3: Adopting a SAP Set

For **curated bundle** adoption (e.g., MCP server development):

```
# 1. Bash - view SAP set definition
Bash: grep -A 30 '"mcp-server"' sap-catalog.json

# 2. This shows included SAPs:
# SAP-000, SAP-003, SAP-004, SAP-005, SAP-006,
# SAP-007, SAP-009, SAP-012, SAP-014, SAP-016

# 3. Read each SAP's AGENTS.md in order
Read file: docs/skilled-awareness/sap-framework/AGENTS.md  # Foundation
Read file: docs/skilled-awareness/project-bootstrap/AGENTS.md
Read file: docs/skilled-awareness/testing-framework/AGENTS.md
# ... etc

# 4. Read adoption blueprints sequentially
Read file: docs/skilled-awareness/sap-framework/adoption-blueprint.md
# Follow steps, then move to next SAP
```

### Workflow 4: Using chora-base as Template

```
# 1. Clone chora-base for new project
Bash: git clone https://github.com/org/chora-base.git my-new-project
Bash: cd my-new-project

# 2. Remove unwanted SAPs
Bash: rm -rf docs/skilled-awareness/react-*  # If not React project
Bash: rm -rf docs/skilled-awareness/mcp-server-development  # If not MCP

# 3. Customize root awareness files
Edit file: AGENTS.md  # Update for your project
Edit file: README.md  # Update project details

# 4. Start developing with adopted SAP patterns!
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

**Explanation**: SAP IDs (SAP-000) are for catalog/references. Directory names are lowercase-with-hyphens.

### Issue: Understanding SAP ID vs Directory Name

**Mapping**:
- SAP-000 → `sap-framework/`
- SAP-001 → `inbox/`
- SAP-004 → `testing-framework/`
- SAP-009 → `agent-awareness/`
- SAP-014 → `mcp-server-development/`
- SAP-015 → `task-tracking/`

**To find mapping for any SAP**:
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
- **pilot**: Yes, but expect changes and give feedback
- **draft**: Only if explicitly exploring experimental features

### Issue: Read Tool Returns Too Much Content

**Solution**: Use Bash with `head` or `tail` for previews:
```bash
# Preview first 50 lines
cat docs/skilled-awareness/sap-framework/protocol-spec.md | head -50

# Preview last 50 lines
cat docs/skilled-awareness/sap-framework/ledger.md | tail -50
```

Or use Read tool with line limits (if supported).

### Issue: Need to Search Across All SAPs

**Solution**: Use Grep tool:
```
Grep pattern: "adoption tier"
Path: docs/skilled-awareness/
Output mode: files_with_matches
```

This finds all SAPs documenting adoption tiers.

**More Help**: See [Onboarding FAQ](../troubleshooting/onboarding-faq.md) for 10+ common issues

---

## Success Criteria

After completing this quickstart, you should be able to:

- [ ] Navigate to chora-base root and verify environment with Bash tool
- [ ] Understand chora-base is a template WITH pre-installed SAPs
- [ ] List all 29+ SAP directories with Bash tool
- [ ] Map SAP IDs (SAP-000) to directory names (sap-framework/)
- [ ] Check SAP status (active/pilot/draft) in sap-catalog.json
- [ ] Use Read tool to explore AGENTS.md files
- [ ] Use Read tool to read protocol-spec.md for technical details
- [ ] Use Read tool to read adoption-blueprint.md for implementation
- [ ] Find SAPs with Claude-specific CLAUDE.md files
- [ ] Know where to find help and resources

**Time Check**: If you completed all steps in ~12 minutes, you're ready to adopt SAPs! ✅

**Claude Code Advantage**: 3 minutes faster than generic guide thanks to Read/Bash/Glob tools

---

## Comparison: Claude Code vs Generic Guide

| Feature | Claude Code Guide | Generic Guide |
|---------|------------------|---------------|
| **Time** | ~12 minutes | ~15 minutes |
| **Tool Leverage** | Read/Bash/Glob/Grep | Manual commands |
| **SAP Discovery** | Glob for CLAUDE.md files | Manual search |
| **Content Reading** | Read tool (fast) | cat/less (slower) |
| **Validation** | Built-in tools | Manual verification |
| **Focus** | Claude-specific patterns | Generic patterns |
| **CLAUDE.md Priority** | Highlighted | Not mentioned |

**When to use generic guide**: If you're not Claude Code, or need non-Claude-specific patterns

---

## Related Resources

**Essential Guides**:
- [Onboarding FAQ](../troubleshooting/onboarding-faq.md) - Common issues and solutions
- [Understanding SAPs](../explanation/understanding-saps.md) - Conceptual deep-dive
- [SAP Framework Protocol](../../skilled-awareness/sap-framework/protocol-spec.md) - Complete specification

**Navigation Guides (Claude-Optimized)**:
- [Root CLAUDE.md](/CLAUDE.md) - Progressive context loading strategy for Claude
- [Root AGENTS.md](/AGENTS.md) - Agent patterns for chora-base
- [SAP Domain CLAUDE.md](../../skilled-awareness/CLAUDE.md) - SAP-specific Claude patterns
- [SAP Domain AGENTS.md](../../skilled-awareness/AGENTS.md) - SAP-specific agent patterns

**SAP Catalog**:
- [sap-catalog.json](/sap-catalog.json) - Machine-readable SAP registry (29 SAPs)
- [SAP Index](../../skilled-awareness/INDEX.md) - Human-readable catalog

**SAPs with Claude-Specific Guidance** (prioritize these!):
```bash
# Find all CLAUDE.md files
find docs/skilled-awareness -name "CLAUDE.md"
```

**Adoption Blueprints**:
- Browse individual SAPs in `docs/skilled-awareness/*/adoption-blueprint.md`
- Follow step-by-step adoption instructions per SAP

---

## Feedback & Support

**Found an Issue?**
- Open an issue: https://github.com/org/chora-base/issues
- Include: OS, Python version, Claude Code version, error messages, steps to reproduce

**Have Suggestions?**
- This quickstart was completely rewritten (2025-11-05) to fix broken paths
- Previous version assumed non-existent directory structure
- Now optimized for Claude Code's Read/Bash/Glob/Grep tools
- We welcome improvements and clarifications

**Need Help?**
- Check [Onboarding FAQ](../troubleshooting/onboarding-faq.md) first
- Search existing issues
- Review SAP-specific AGENTS.md files
- Read root CLAUDE.md for navigation strategy
- Look for CLAUDE.md files in individual SAPs (contain Claude-specific tips)

---

**Version**: 2.0.0 (Complete rewrite)
**Last Updated**: 2025-11-05
**Changes**: Fixed all directory paths, removed broken installation workflow, clarified chora-base as template with pre-installed SAPs, optimized for Claude Code tools (Read/Bash/Glob/Grep)
**Target Audience**: Claude Code AI agents specifically
**Goal**: Accurate, working quickstart in ~12 minutes leveraging Claude Code's tool advantages
**Claude Code Optimizations**: Read tool priority, Glob/Grep discovery, Bash navigation, CLAUDE.md file highlighting, Task tool integration for complex exploration
