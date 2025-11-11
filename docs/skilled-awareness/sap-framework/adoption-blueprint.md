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

### Quick Install

Use the automated installation script:

```bash
python scripts/install-sap.py SAP-000 --source /path/to/chora-base
```

**What This Installs**:
- SAP framework documentation (5 artifacts)
- Root protocol document (SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- Document templates for creating SAPs
- No system files (framework is documentation-only)

### Part of Sets

This SAP is included in:
- minimal-entry
- recommended
- full
- testing-focused
- mcp-server

To install a complete set:
```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Manual Installation (Alternative)

If you cannot use the install script, follow these manual steps:

**Step 1: Create SAP Framework Directory**

```bash
mkdir -p docs/reference/skilled-awareness
```

**Step 2: Copy Root Protocol**

```bash
cp /path/to/chora-base/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md \
   SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
```

**Step 3: Copy Framework SAP**

```bash
cp -r /path/to/chora-base/docs/skilled-awareness/sap-framework \
      docs/skilled-awareness/
```

**Step 4: Copy Document Templates**

```bash
cp /path/to/chora-base/docs/skilled-awareness/document-templates.md \
   docs/skilled-awareness/
```

### Validation

Verify all 5 artifacts exist:

```bash
ls docs/skilled-awareness/sap-framework/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md && echo "✅ Framework SAP installed"
test -f SKILLED_AWARENESS_PACKAGE_PROTOCOL.md && echo "✅ Protocol copied"
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

**Why This Step Matters**:
AGENTS.md serves as the **discoverability layer** for installed SAPs. Without this update, agents cannot find the SAP Framework capability, making it invisible to AI assistants like Claude. This step ensures:
- Agents can discover installed SAPs by reading root AGENTS.md
- Quick reference for common SAP operations
- Links to detailed documentation

**Quality Requirements** (validated by SAP audit):
- Agent-executable instructions (specify tool, file, location, content)
- Concrete content template (not placeholders)
- Validation command to verify update
- See: [SAP_AWARENESS_INTEGRATION_CHECKLIST.md](../../../dev-docs/workflows/SAP_AWARENESS_INTEGRATION_CHECKLIST.md)

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

## 5. L1 Requirement: Discoverability

### Overview

**Goal**: Make this SAP discoverable via root awareness files

**Why This Matters**: Implementation quality is irrelevant if agents cannot discover the capability exists. Without strong discoverability, excellent implementations remain invisible, creating a "meta-discoverability paradox" where sophisticated patterns become liabilities instead of assets.

**Success Criteria**:
- Discoverability score ≥80/100 (see SAP-019 evaluation framework)
- Agents can discover SAP in <5 minutes from root files
- All touchpoints complete (README, AGENTS, CLAUDE, justfile, docs)

**Time Investment**: 3-5 hours (one-time)
**ROI**: 10-15 minutes saved per session per agent (break-even: 20-30 sessions)

---

### 5.1 README.md Section (30 points)

**Requirement**: Add dedicated section to project README.md (30+ lines minimum)

**For agents** (use Edit tool):
1. Open: `README.md`
2. Find appropriate section (e.g., "Features" or "Capabilities")
3. Add section with this template:

```markdown
### [SAP Name]

**When to use SAP-XXX**:
- [Use case 1]
- [Use case 2]
- [Use case 3]
- [Use case 4]
- [Use case 5]

**What you get**:
- [Feature 1 with details]
- [Feature 2 with details]
- [Feature 3 with details]

**Quick start**:
\```bash
# [Command 1 with comment]
just command-1

# [Command 2 with comment]
just command-2

# [Command 3 with comment]
just command-3
\```

**Documentation**: [Link to docs or nested AGENTS.md]

**ROI**: [Time saved or value delivered per session]
```

**Validation**:
```bash
# Check section exists and meets length requirement
grep -A 40 "### SAP-XXX" README.md | wc -l
# Target: ≥30 lines
```

---

### 5.2 AGENTS.md Section (20 points)

**Requirement**: Add dedicated section to project AGENTS.md (60+ lines minimum)

**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Capabilities" or "Workflows")
3. Add section with this template:

```markdown
### [SAP Name] (SAP-XXX)

**When to use SAP-XXX**:
- [Scenario 1 with context]
- [Scenario 2 with context]
- [Scenario 3 with context]
- [Scenario 4 with context]
- [Scenario 5 with context]

**Quick-start approach** (recommended):
\```bash
# [Step 1 with explanation]
just step-1

# [Step 2 with explanation]
just step-2

# [Step 3 with explanation]
just step-3
\```

**What you get**:
- **[Feature 1 category]**: [Detailed explanation]
- **[Feature 2 category]**: [Detailed explanation]
- **[Feature 3 category]**: [Detailed explanation]

**Example workflow**:
\```bash
# Scenario: [Complete use case description]

# 1. [Step description]
just command-1

# 2. [Step description]
just command-2

# 3. [Step description]
just command-3

# Result: [Expected outcome]
\```

**Integration with other SAPs**:
- **SAP-XXX ([name])**: [Integration pattern]
- **SAP-YYY ([name])**: [Integration pattern]

**Documentation**: [Links to detailed docs]

**ROI**: [Time/value saved per session]
```

**Validation**:
```bash
# Check section exists and meets length requirement
grep -A 70 "### SAP-XXX" AGENTS.md | wc -l
# Target: ≥60 lines
```

---

### 5.3 CLAUDE.md Coverage (15 points)

**Requirement**: Add dedicated section OR ensure domain section has direct links (if using SAP-009 nested hierarchy)

**Option A: Dedicated Section** (if SAP has Claude-specific patterns):
```markdown
### [SAP Name] Claude Workflows

**Token budget guidance**:
- Phase 1 (orientation): [X]k tokens
- Phase 2 (implementation): [Y]k tokens

**Claude-specific tips**:
- [Tip 1 for Claude Code or Claude Desktop]
- [Tip 2 for Claude Code or Claude Desktop]

**Example workflow**:
\```markdown
User: "[Common request]"

Claude:
1. [Step 1 with tool usage]
2. [Step 2 with tool usage]
3. [Step 3 with tool usage]
\```
```

**Option B: Domain Section with Direct Links** (if using nested hierarchy):
```markdown
### Domain X: [Domain Name] (path/)

**Path**: [path/AGENTS.md](path/AGENTS.md) + [path/CLAUDE.md](path/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [path/CLAUDE.md](path/CLAUDE.md) - Claude workflows (X-min, Yk tokens)
- [path/AGENTS.md](path/AGENTS.md) - [Domain] patterns (X-min, Yk tokens)

**Use when**:
- [Scenario 1]
- [Scenario 2]
```

**Validation**:
```bash
grep -i "SAP-XXX\|[sap-name]" CLAUDE.md && echo "✅ CLAUDE.md coverage exists"
```

---

### 5.4 justfile Recipes (15 points)

**Requirement**: Add ≥3 recipes with section header, comments, and examples

**For agents** (use Edit tool):
1. Open: `justfile`
2. Add section with this template:

```bash
# ============================================================================
# SAP-XXX: [SAP Name]
# ============================================================================
# [Brief description of SAP purpose, 1-2 sentences]
# See: [Link to AGENTS.md or nested files]

# [Recipe 1 description with details]
# Example: just recipe-1 arg-value
recipe-1 ARG="default":
    @command {{ARG}}

# [Recipe 2 description with details]
# Example: just recipe-2 arg-value
recipe-2 ARG="default":
    @command {{ARG}}

# [Recipe 3 description with details]
# Example: just recipe-3
recipe-3:
    @command
```

**Best Practices**:
- Section header with SAP reference (# === SAP-XXX: Name ===)
- Section comment explaining SAP purpose
- Inline comment for each recipe (# Description)
- Usage example for complex recipes (# Example: just ...)
- Default values for arguments when appropriate

**Validation**:
```bash
# Check recipes exist
grep -A 20 "SAP-XXX" justfile | grep "^[a-z]" | wc -l
# Target: ≥3 recipes
```

---

### 5.5 Documentation (10 points)

**Requirement**: Create ≥1 how-to guide, organize per SAP-007 structure (if applicable)

**For agents**:
1. Create: `docs/how-to/using-[sap-name].md`
2. Content template:

```markdown
# How to Use [SAP Name]

**Audience**: Developers and AI agents
**Time**: [X] minutes
**Prerequisites**: [List]

---

## Quick Start

[5-step quick start with commands]

---

## Common Tasks

### Task 1: [Name]

\```bash
# [Commands with explanations]
\```

### Task 2: [Name]

\```bash
# [Commands with explanations]
\```

---

## Troubleshooting

**Problem**: [Common issue]
**Solution**: [Fix]
```

**Optional** (for complex SAPs):
- Create: `docs/explanation/understanding-[sap-name].md` (concept explanation)
- Create: `docs/reference/[sap-name]-reference.md` (API/schema reference)

**Validation**:
```bash
ls docs/how-to/using-[sap-name].md && echo "✅ How-to guide exists"
```

---

### 5.6 Direct Links (Required if using SAP-009 nested hierarchy)

**Requirement**: If SAP uses nested AGENTS.md/CLAUDE.md files, add direct links in root files

**For agents** (use Edit tool):
1. Update root CLAUDE.md domain section:

```markdown
### Domain X: [Domain Name] (path/)

**Path**: [path/AGENTS.md](path/AGENTS.md) + [path/CLAUDE.md](path/CLAUDE.md)

**Navigation tip**: Read domain-specific files for 60-70% token savings
- [path/CLAUDE.md](path/CLAUDE.md) - Claude workflows (X-min, Yk tokens)
- [path/AGENTS.md](path/AGENTS.md) - [Domain] patterns (X-min, Yk tokens)

**Use when**:
- [Working in path/ directory]
- [Need domain-specific guidance]
```

2. Update root AGENTS.md to reference nested file:

```markdown
**For detailed patterns**: See [path/AGENTS.md](path/AGENTS.md)
```

**Validation**:
```bash
# Check links exist and are clickable
grep -o "\[.*AGENTS.md\](.*AGENTS.md)" CLAUDE.md && echo "✅ Direct links exist"
```

---

### 5.7 Validation Checklist

Before marking L1 complete, verify all discoverability requirements:

**Touchpoints Checklist**:
- [ ] README.md section added (≥30 lines)
- [ ] AGENTS.md section added (≥60 lines)
- [ ] CLAUDE.md coverage exists (dedicated section OR domain links)
- [ ] justfile recipes added (≥3 recipes with comments)
- [ ] Documentation created (≥1 how-to guide)
- [ ] Direct links added (if using nested hierarchy)

**Quality Checklist**:
- [ ] All code examples tested and working
- [ ] All links are clickable and resolve correctly
- [ ] No placeholder text (e.g., "TODO", "[TBD]")
- [ ] Concrete examples provided (not abstract descriptions)
- [ ] ROI statement included with quantified value

**Discovery Test**:
- [ ] Agent can find SAP by reading README.md alone (<2 min)
- [ ] Agent can find SAP by reading AGENTS.md alone (<2 min)
- [ ] Agent can discover recipes via `just --list` (<1 min)
- [ ] Navigation time from root to SAP docs <5 min total

**Validation Command**:
```bash
# Run discoverability audit (if available)
just disc | grep SAP-XXX
# Target: ≥80/100

# Or manual validation
echo "README.md: $(grep -A 40 '### SAP-XXX' README.md | wc -l) lines (target: ≥30)"
echo "AGENTS.md: $(grep -A 70 '### SAP-XXX' AGENTS.md | wc -l) lines (target: ≥60)"
echo "justfile recipes: $(grep -A 20 'SAP-XXX' justfile | grep '^[a-z]' | wc -l) (target: ≥3)"
echo "How-to guide: $(ls docs/how-to/*[sap-name]* 2>/dev/null | wc -l) (target: ≥1)"
```

---

### 5.8 The Meta-Discoverability Principle

**Key Insight**: "The better the pattern, the worse the impact if undiscoverable"

**Anti-Pattern** (common mistake):
1. Implement SAP (excellent quality, 20 hours)
2. Use SAP internally (works great)
3. Mark L1 complete
4. Discoverability score: 40/100
5. Other agents can't find it
6. ROI: $0 (invisible capability)

**Correct Pattern**:
1. Implement SAP (excellent quality, 20 hours)
2. Add discoverability (README, AGENTS, justfile, 3-5 hours)
3. Validate discoverability ≥80/100
4. Mark L1 complete
5. Natural adoption (agents discover via root files)
6. ROI: Projected value realized from day 1

**Time Investment**: 3-5 hours (12-20% overhead on implementation)
**Returns**: 10-15 min saved per session per agent
**Break-even**: 20-30 sessions (1-2 months for single agent)
**12-Month ROI**: 250-400% (typical)

---

### 5.9 Discoverability for Advanced Patterns

**Special Case: Nested Hierarchies (SAP-009)**

If your SAP uses nested AGENTS.md/CLAUDE.md files:
- **Requires higher discoverability** (target: ≥85/100 vs ≥80/100)
- **Must include direct links** in root CLAUDE.md (not optional)
- **Must state token savings** explicitly (e.g., "60-70% reduction")
- **Must provide read time estimates** (e.g., "8-min, 5k tokens")

**Rationale**: Without strong discoverability, navigation tax exceeds token savings, making the advanced pattern a net negative.

---

## 6. Validation

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

## 7. Post-Install: Enabling Agent Awareness

After installing the SAP Framework, ensure agents can discover and use this capability:

### Step 1: Update Root AGENTS.md

Add reference to SAP-000 in your project's root AGENTS.md file:

```markdown
## Skilled Awareness Packages (SAPs)

This project uses the SAP Framework (SAP-000) to package development capabilities.

### Using SAPs

1. **Browse available SAPs**: See `docs/skilled-awareness/INDEX.md`
2. **Install a SAP**: `python scripts/install-sap.py SAP-XXX`
3. **Read SAP documentation**: Each SAP has 5 artifacts (charter, protocol, awareness guide, adoption blueprint, ledger)

### SAP Framework
- **Documentation**: [docs/skilled-awareness/sap-framework/](docs/skilled-awareness/sap-framework/)
- **Protocol**: [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
```

### Step 2: Validate Awareness Integration

Run the awareness integration checker:

```bash
bash scripts/check-sap-awareness-integration.sh SAP-000
```

**Expected result**: PASS with 4/4 checks:
- ✅ Root AGENTS.md mentions SAP-000
- ✅ SAP-000 adoption blueprint has post-install section
- ✅ SAP-000 awareness guide exists
- ✅ SAP-000 referenced in INDEX.md

### Step 3: Test Agent Discovery

Verify agents can find SAP Framework guidance:

1. Open root AGENTS.md
2. Search for "SAP" or "Skilled Awareness"
3. Confirm link to SAP documentation works
4. Verify INDEX.md lists all available SAPs

### Success Criteria

After completing post-install awareness:
- ✅ Agents know where to find SAP documentation
- ✅ SAP Framework discoverable via root AGENTS.md
- ✅ Validation script passes all checks
- ✅ Future SAPs will be automatically discoverable

---

## 8. Upgrade Path

### Future Versions

**When framework updates**:
1. Check chora-base releases for SAP framework updates
2. Look for upgrade blueprints in `sap-framework/upgrades/`
3. Follow sequential upgrade path (v1.0 → v1.1 → v2.0)

**Current Version**: 1.0.0 (initial release)

**Next Expected Version**: 1.1.0 (minor enhancements, TBD)

---

## 9. Troubleshooting

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

## 10. Next Steps

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

## 11. Support

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

## 12. Related Documents

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
