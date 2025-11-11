---
type: coordination_request
status: draft
priority: high
target_repo: chora-base
target_sap: SAP-009 (Agent Awareness)
created: 2025-11-09
author: chora-workspace
impact: ecosystem-wide
---

# Coordination Request: Nested Awareness Pattern - Meta-Discoverability Solution

## Executive Summary

**Discovery**: chora-workspace identified a critical meta-discoverability problem - root AGENTS.md files were too large (2,766 lines, 15.4k tokens), causing critical workflows to be undiscoverable and frequently missed.

**Solution Implemented**: Research-backed nested AGENTS.md structure following "Agentic Coding Best Practices" (p. 5-6) - split monolithic files into modular, domain-specific files.

**Impact**: 70% file size reduction, critical workflows now highly discoverable, within Phase 1 token budget.

**Recommendation**: Update SAP-009 in chora-base to document this pattern and provide guidance for when/how to split awareness files.

---

## Problem Statement

### What Triggered This?

User feedback after I (Claude) missed a documented sprint completion workflow:

> "in another conversation you just now said: 'You're absolutely right! I got caught up in implementation and forgot to follow the chora-workspace development processes.' my point is that if our development process was 'discoverable' and integrated into our agent awareness files, then you would not have 'forgotten' i think. how curious. can you please audit?"

### Root Cause Analysis

**File Size Issue**:
- Root AGENTS.md: 2,766 lines (~15,398 tokens)
- Root CLAUDE.md: 1,059 lines (~5,345 tokens)
- **Total**: ~20,744 tokens vs stated Phase 1 budget of 5-10k tokens

**Workflow Burial**:
- Sprint completion workflow located at line 1878 (66% into file)
- Agents would read the file, but critical workflows were missed due to cognitive load
- Progressive loading broke down - couldn't load entire file within reasonable token budget

**Meta-Discoverability Paradox**:
> "By making everything discoverable in one place, we made nothing discoverable!"

The more comprehensive we made the root AGENTS.md, the harder it became to find critical information.

---

## Solution Implemented

### Research-Backed Approach

Consulted workspace research documents per user request:
- **Source**: "Agentic Coding Best Practices" (docs/research/Agentic Coding Best Practices Research.pdf)
- **Finding** (p. 5-6):
  > "For large projects or monorepos, a best practice is to use a **modular architecture with nested AGENTS.md files**. This approach **prevents the need for a single, giant file** and allows packages with different stacks to evolve independently."
- **Guideline** (p. 5): "Prefer **single-file artifacts for components under 500 lines**"

### Implementation

Created 3-tier nested structure:

#### 1. `/AGENTS.md` (Root) - 839 lines (~5.5k tokens)
**Purpose**: Orientation, critical workflows, navigation
**Key addition**: "⚠️ Critical Workflows (Read This First!)" section at top
**Content**:
- Sprint completion workflow (quick reference)
- Git conventions (quick reference)
- SAP quick reference with commands
- Navigation tree to nested files
- Progressive loading strategy
- Checkpoint patterns

**Removed**: ~2,000 lines of SAP detailed content (moved to nested files)

#### 2. `/saps/AGENTS.md` - 600 lines
**Purpose**: Complete SAP catalog
**Content**:
- All 13 SAP quick-reference sections
- "When to use", "Quick start", "What you get" for each SAP
- Cross-references to dev-process for SAP-012 details

#### 3. `/dev-process/AGENTS.md` - 450 lines
**Purpose**: Development workflows and processes
**Content**:
- **Sprint Completion Workflow** (7-step process with template and checklist) - prominently at top
- Sprint Planning & Execution (4-level hierarchy, velocity tracking)
- Git Commit Conventions (SAP-011 full specification)

### CLAUDE.md Updates

- Added "⚠️ Critical Workflows" section at top
- Updated frontmatter: v2.0.0, nested_structure: true
- Added references to nested structure
- Coordinates with restructured AGENTS.md

---

## Results & Metrics

### File Size Impact

| File | Before | After | Change |
|------|--------|-------|--------|
| **Root AGENTS.md** | 2,766 lines | 839 lines | **-70%** |
| **Token Budget** | ~15.4k tokens | ~5.5k tokens | **Within Phase 1** ✓ |
| **Sprint Workflow Location** | Line 1878 (66% buried) | Lines 32-50 (top 10%) | **Highly discoverable** ✓ |
| **Structure** | Monolithic | Modular (3 files) | **Research-backed** ✓ |

### New File Structure

```
/AGENTS.md (Root)
  ├─ ⚠️ Critical Workflows (NEW - at top!)
  │  ├─ Sprint Completion (7-step quick ref)
  │  ├─ Git Conventions (quick ref)
  │  └─ SAP Quick Reference
  ├─ Project Overview
  ├─ Progressive Loading Strategy
  └─ → Navigation to nested files

/saps/AGENTS.md
  └─ 13 SAP quick references (detailed)

/dev-process/AGENTS.md
  ├─ Sprint Completion Workflow (full template)
  ├─ Sprint Planning & Execution
  └─ Git Conventions (full spec)

/CLAUDE.md (v2.0)
  ├─ Critical Workflows section
  └─ → Coordinates with AGENTS.md
```

### Discoverability Impact

**Problem Solved**: Critical workflows (especially sprint completion) are now:
1. ✅ **At the top** of root AGENTS.md (lines 32-50 vs line 1878)
2. ✅ **Repeated** in dev-process/AGENTS.md with full template
3. ✅ **Referenced** in root CLAUDE.md with quick access
4. ✅ **Within token budget** - agents can load root files in Phase 1

**Expected Outcome**: Agents will no longer "forget" critical workflows because they're prominently featured instead of buried.

---

## Recommendations for chora-base

### 1. Update SAP-009 Documentation

**Current State**: SAP-009 documents nested awareness pattern but doesn't provide clear guidance on **when** to split files or **how** to structure splits.

**Proposed Enhancement**: Add section to SAP-009 Awareness Guide:

#### "When to Split AGENTS.md Files"

**Indicators you need to split**:
- File exceeds 1,000 lines (2,000+ lines = critical)
- Token estimate exceeds 10k (15k+ = critical)
- Critical workflows are buried >50% into file
- Multiple distinct domains/concerns in one file
- Agents report missing documented workflows

**Splitting Strategy** (research-backed):
1. **Keep root file <1,000 lines** (target: 500-800 lines)
2. **Create domain-specific nested files** for specialized content
3. **Surface critical workflows at top** of root file
4. **Add "Critical Workflows" section** if workflows exist
5. **Target <500 lines per nested file** (research guideline)

**Example Split Pattern** (from chora-workspace):
```
Root AGENTS.md (~800 lines)
  ├─ Critical Workflows section (new)
  ├─ Project overview
  ├─ Navigation tree
  └─ → Points to nested files

Domain Files:
  ├─ /saps/AGENTS.md (SAP catalog)
  ├─ /dev-process/AGENTS.md (workflows)
  ├─ /docs/AGENTS.md (documentation patterns)
  ├─ /scripts/AGENTS.md (automation patterns)
  └─ /[domain]/AGENTS.md (as needed)
```

### 2. Add "Critical Workflows" Pattern

**Pattern**: Add dedicated "⚠️ Critical Workflows (Read This First!)" section to SAP-009 template

**Purpose**: Surface workflows that agents frequently miss

**Location**: Immediately after frontmatter and title, before other content

**Content Structure**:
```markdown
## ⚠️ Critical Workflows (Read This First!)

**Problem solved**: [Describe what workflows were being missed]

### [Workflow 1 Name]
**When**: [Trigger condition]
**Quick reference**: [Bash commands or steps]
**Full details**: [Link to nested file with template]

### [Workflow 2 Name]
...
```

**Example** (from chora-workspace):
- Sprint Completion Workflow (7-step process)
- Git Commit Conventions (format reference)
- SAP Quick Reference (common commands)

### 3. Add Frontmatter Fields for Nested Structure

Enhance SAP-009 frontmatter standard to support nested structure:

```yaml
---
sap_id: SAP-009
version: 2.0.0
nested_structure: true  # NEW FIELD
nested_files:           # NEW FIELD
  - "saps/AGENTS.md"
  - "dev-process/AGENTS.md"
  - "docs/AGENTS.md"
---
```

**Benefits**:
- Agents can detect nested structure programmatically
- Clear documentation of file relationships
- Supports tooling/validation of nested patterns

### 4. Update SAP-009 Adoption Blueprint

Add step for "File Size Assessment and Splitting":

```markdown
## Step 5: Assess File Size and Split if Needed

**Check if splitting is needed**:
```bash
wc -l AGENTS.md CLAUDE.md
# AGENTS.md > 1000 lines? Consider splitting
# CLAUDE.md > 800 lines? Consider splitting
```

**If splitting needed**:
1. Identify distinct domains/concerns
2. Create nested directory structure
3. Extract domain-specific content
4. Add "Critical Workflows" section to root
5. Update frontmatter with nested_structure: true
6. Test navigation and cross-references
```

---

## Evidence & Validation

### User Feedback (Direct Quote)

Initial problem identification:
> "if our development process was 'discoverable' and integrated into our agent awareness files, then you would not have 'forgotten' i think. how curious. can you please audit?"

Root cause diagnosis:
> "i'm guessing that we need to do a better job of distributing discoverabilty with progressive whatzit. if the root adents and claude files are so big then you will not use them effectively."

Consultation request:
> "personally i do not know what appraoch is best but maybe our research has suggestions."

Solution approval:
> "yes, proceed but we need it for both AGENTS.md and CLAUDE.md"

### Research Citations

**Primary Source**: "The Agentic Revolution: A Report on Modern Agentic Coding Practices"

**Key Quotes**:
- **Page 5-6**: "For large projects or monorepos, a best practice is to use a **modular architecture with nested AGENTS.md files**"
- **Page 5**: "Prefer **single-file artifacts for components under 500 lines**"
- **Page 6**: "**Be Concise and Concrete**: Agents process information more effectively when it is simple and direct"
- **Page 6**: "This approach **prevents the need for a single, giant file with complex conditionals**"

### Implementation Files

**Created in chora-workspace** (2025-11-09):
- `/saps/AGENTS.md` - [Link](https://github.com/[org]/chora-workspace/blob/main/saps/AGENTS.md)
- `/dev-process/AGENTS.md` - [Link](https://github.com/[org]/chora-workspace/blob/main/dev-process/AGENTS.md)
- Updated `/AGENTS.md` - [Link](https://github.com/[org]/chora-workspace/blob/main/AGENTS.md)
- Updated `/CLAUDE.md` - [Link](https://github.com/[org]/chora-workspace/blob/main/CLAUDE.md)

---

## Proposed Timeline

1. **Week 1**: Review coordination request, discuss with chora-base maintainers
2. **Week 2**: Update SAP-009 documentation with nested structure guidance
3. **Week 3**: Update SAP-009 templates and adoption blueprint
4. **Week 4**: Test updated SAP-009 in new chora-base adoptions

---

## Questions for chora-base Team

1. **Pattern Generalization**: Does this nested structure pattern apply to most/all projects adopting SAP-009, or is it specific to large meta-repositories like chora-workspace?

2. **Threshold Guidance**: Are the thresholds we identified (1,000 lines, 10k tokens) appropriate as general guidelines, or should they be adjusted?

3. **Domain Taxonomy**: Should SAP-009 provide a standard set of domain names (saps/, dev-process/, etc.) or leave this flexible per project?

4. **Backward Compatibility**: How should existing SAP-009 adoptions handle migration to nested structure? Optional or recommended?

5. **Tooling Support**: Should we create automation for file splitting or structure validation?

---

## Next Steps (chora-workspace)

1. ✅ **Completed**: Implement nested structure in workspace
2. ✅ **Completed**: Create coordination request for chora-base
3. ⏳ **Pending**: Test nested structure over 2-4 weeks
4. ⏳ **Pending**: Gather metrics on discoverability improvement
5. ⏳ **Pending**: Create knowledge note documenting pattern
6. ⏳ **Pending**: Update workspace SAP-009 adoption to L3+ if pattern proves successful

---

## Contact & Discussion

**Primary Contact**: [User] via chora-workspace
**Discussion Channel**: [GitHub Issue, PR, or communication channel]
**Timeline**: Response requested within 1-2 weeks
**Priority**: High - impacts core SAP-009 pattern and agent effectiveness

---

**Created**: 2025-11-09
**Author**: chora-workspace team (Claude + User)
**Target**: chora-base SAP-009 maintainers
**Type**: Pattern enhancement proposal with implementation evidence
