# Structure vs Content Model

**Purpose**: Understanding the fundamental boundary between reusable structure and project-specific content in chora-base

**Audience**: Developers using chora-base, maintainers building ecosystem tools

---

## Overview

The **Structure vs Content Model** is a design principle that separates:

- **Structure**: Reusable patterns, standards, protocols, and templates that should be updated from upstream
- **Content**: Project-specific implementations, documentation, and customizations that belong to your project

This separation enables the **Clone & Merge Model** where projects can receive upstream improvements without losing their identity.

---

## The Core Problem

When you create a project from chora-base, you get:
1. A complete repository structure (directories, templates, standards)
2. Automation tools (scripts, CI/CD workflows)
3. Documentation frameworks (SAP system, 4-domain architecture)
4. Development protocols (testing, quality gates, versioning)

**The Challenge**: How do you receive updates to items 1-4 without overwriting your custom code, docs, and configurations?

**Traditional Solutions (and their problems)**:
- **Fork model**: Upstream updates require painful merge conflicts
- **Copy-paste model**: No systematic way to receive updates
- **Submodule model**: Too rigid, doesn't allow customization

**Chora-Base Solution**: Structure vs Content Model with intelligent merge

---

## Three File Categories

Every file in a chora-base project falls into one of three categories:

### 1. Structure-Only Files

**Definition**: Files that provide standards, protocols, or templates and should always be updated from upstream

**Characteristics**:
- ✅ No project-specific content
- ✅ Define standards or patterns
- ✅ Safe to overwrite with upstream version
- ✅ Changes are improvements or fixes, not customizations

**Examples**:
```
SKILLED_AWARENESS_PACKAGE_PROTOCOL.md  # SAP standard
DOCUMENTATION_STANDARD.md              # Doc structure standard
docs/skilled-awareness/sap-framework/  # SAP framework itself
scripts/install-sap.py                 # Automation tooling
scripts/merge-upstream-structure.py    # Merge tooling
.github/workflows/test.yml             # CI/CD template
```

**Merge Strategy**: `git checkout upstream/main -- <file>`
- Directly take the upstream version
- No conflicts possible (by design)

**Why This Works**:
- These files are **templates** or **specifications**, not implementations
- Your project uses them but doesn't modify them
- Improvements benefit all projects equally

### 2. Content-Only Files

**Definition**: Files that contain project-specific implementations and should never be merged from upstream

**Characteristics**:
- ✅ Unique to your project
- ✅ Contains your business logic, data, or customizations
- ✅ Would be destroyed by upstream merge
- ✅ Your intellectual property

**Examples**:
```
src/                                   # Your source code
tests/                                 # Your tests
docs/skilled-awareness/my-project/     # Your project SAPs
docs/user-docs/how-to/my-feature.md    # Your how-to guides
.env                                   # Your secrets
.gitignore                             # Your customizations
README.md (project-specific sections)  # Your project description
```

**Merge Strategy**: Never merge from upstream
- Git ignores these files during upstream merge
- You have complete control

**Why This Works**:
- These files define your project's unique identity
- No upstream changes should touch them
- You can evolve independently

### 3. Hybrid Files

**Definition**: Files that contain both structural patterns and project-specific content, requiring intelligent merge

**Characteristics**:
- ⚙️ Mix of templates and customizations
- ⚙️ Some sections from upstream, some project-specific
- ⚙️ Need special merge strategies
- ⚙️ Can't use simple file-level merge

**Examples**:
```
AGENTS.md          # Project overview + structural sections
README.md          # Project identity + template structure
INDEX.md           # Project SAPs + framework SAPs
CHANGELOG.md       # Append-only, preserve all entries
ROADMAP.md         # Too project-specific (manual merge only)
```

**Merge Strategies**:

| File | Strategy | How It Works |
|------|----------|-------------|
| **AGENTS.md** | `section-by-section` | Keep "Project Overview", merge "Project Structure" |
| **README.md** | `template-variables` | Preserve project name/description, update template |
| **INDEX.md** | `table-rows` | Update SAP-000 from upstream, keep SAP-001+ from project |
| **CHANGELOG.md** | `append-only` | Never overwrite entries, only add new ones |
| **ROADMAP.md** | `manual` | Too project-specific, manual review required |

**Why Hybrid Files Exist**:
- Some files need both standard structure and custom content
- Can't be purely structural (would lose project identity)
- Can't be purely content (would miss upstream improvements)
- Solution: Intelligent merge strategies

---

## How the Model Works

### Step 1: Classification

When you run `merge-upstream-structure.py`, it reads `.chorabase` to classify files:

```yaml
# .chorabase
structure_only:
  - SKILLED_AWARENESS_PACKAGE_PROTOCOL.md
  - scripts/install-sap.py
  - docs/skilled-awareness/sap-framework/**

content_only:
  - src/**
  - tests/**
  - docs/skilled-awareness/my-project/**

hybrid:
  AGENTS.md:
    merge_strategy: "section-by-section"
  README.md:
    merge_strategy: "template-variables"
```

### Step 2: Automated Merge (Structure-Only)

For structure-only files:
```bash
# For each file in structure_only:
git checkout chora-base/main -- <file>
```

**Result**: Your project gets the latest version of each structural file

### Step 3: Protection (Content-Only)

For content-only files:
```bash
# Skip entirely, no git operations
```

**Result**: Your project-specific files are untouched

### Step 4: Intelligent Merge (Hybrid)

For hybrid files:
```bash
# Use specialized merge tools
python scripts/merge-agents-md.py
python scripts/merge-readme-md.py
python scripts/merge-index-md.py
```

**Result**: Combined version with upstream structure + your content

---

## Design Principles

### 1. Default to Content (Safety First)

**Principle**: When in doubt, treat as content-only

**Why**: It's safer to preserve a file than to accidentally overwrite project work

**Example**:
```yaml
# If you're not sure, add to content_only:
content_only:
  - some/uncertain/file.md  # Default: preserve
```

You can always manually merge later if needed.

### 2. Structure Is Template, Not Implementation

**Principle**: Structure files define "how to" not "what we built"

**Why**: Enables upstream evolution without breaking projects

**Example**:
- ✅ Structure: "SAPs should have an adoption-blueprint.md"
- ❌ Content: "Our SAP-042 for neural networks does X"

### 3. Customization Through Composition, Not Modification

**Principle**: Don't modify structure files, compose from them

**Why**: Allows you to receive upstream updates without conflicts

**Example**:
```
❌ Don't modify:
docs/skilled-awareness/sap-framework/protocol-spec.md

✅ Do compose from it:
docs/skilled-awareness/my-sap/adoption-blueprint.md
  (follows the protocol-spec.md standard)
```

### 4. Explicit Boundaries

**Principle**: Every file's category should be obvious and documented

**Why**: Reduces errors, enables automation

**Example**:
```yaml
# .chorabase makes boundaries explicit
structure_only:
  - scripts/**              # All scripts are structural tools

content_only:
  - src/**                  # All src/ is project code
```

---

## Real-World Examples

### Example 1: Receiving a SAP Framework Update

**Scenario**: Upstream releases SAP Framework v2.0 with new adoption blueprint template

**What Happens**:
1. You run `merge-upstream-structure.py`
2. It updates `docs/skilled-awareness/sap-framework/adoption-blueprint-template.md`
3. Your existing SAPs in `docs/skilled-awareness/my-project/` are untouched
4. New SAPs you create use the v2.0 template

**Result**: You get the improvement without losing your work

### Example 2: Script Update

**Scenario**: Upstream fixes a bug in `scripts/install-sap.py`

**What Happens**:
1. You run `merge-upstream-structure.py`
2. It directly overwrites `scripts/install-sap.py` with the fixed version
3. No conflicts, no manual merge

**Result**: Bug fix propagates automatically

### Example 3: AGENTS.md Update

**Scenario**: Upstream adds a new "SAP Framework" section to AGENTS.md template

**What Happens**:
1. You run `merge-agents-md.py`
2. It preserves your "Project Overview" section (project-specific)
3. It merges the new "SAP Framework" section (structural)
4. Result: AGENTS.md has both your project info and the new section

**Result**: You get new structure while keeping your content

---

## Comparison with Other Models

### vs Git Submodules

**Submodules**:
- ✅ Clean separation
- ❌ Can't customize submodule contents
- ❌ Rigid boundary, no hybrid files
- ❌ Complex to manage

**Structure vs Content**:
- ✅ Can customize anything
- ✅ Flexible boundaries
- ✅ Hybrid file support
- ✅ Simpler workflow

### vs Fork Model

**Fork**:
- ✅ Full control
- ❌ Painful merge conflicts
- ❌ Upstream divergence
- ❌ Manual conflict resolution

**Structure vs Content**:
- ✅ Full control
- ✅ Conflict-free for structure files
- ✅ Stays aligned with upstream
- ✅ Automated merge

### vs Copy-Paste

**Copy-Paste**:
- ✅ Simple initial setup
- ❌ No update mechanism
- ❌ Manual tracking of changes
- ❌ Drift inevitable

**Structure vs Content**:
- ✅ Simple setup
- ✅ Systematic updates
- ✅ Automated tracking
- ✅ Upstream alignment maintained

---

## When the Model Breaks Down

### Anti-Pattern 1: Modifying Structure Files

**Problem**: You edit `DOCUMENTATION_STANDARD.md` to add project-specific notes

**Why It's Bad**: Next upstream merge will overwrite your changes

**Solution**: Create `docs/project-docs/our-documentation-notes.md` instead

### Anti-Pattern 2: Treating Content as Structure

**Problem**: Adding `src/my-feature/` to `structure_only`

**Why It's Bad**: Upstream merge would overwrite your code (if upstream happened to have a file at that path)

**Solution**: Keep all `src/` in `content_only`

### Anti-Pattern 3: Avoiding Hybrid Files

**Problem**: Refusing to use hybrid merge tools, doing manual edits

**Why It's Bad**: Miss upstream improvements, create inconsistencies

**Solution**: Trust the hybrid merge tools, they're designed for this

---

## Evolution of the Model

### Phase 1: Manual Distinction (v3.x)

- Developers had to remember which files to merge
- No automation, high error rate
- Documentation-only guidance

### Phase 2: Automated Classification (v4.0)

- `.chorabase` file codifies boundaries
- Automated merge script
- Hybrid file strategies

### Phase 3: Intelligent Merge (v4.1)

- Specialized hybrid merge tools
- Section-level granularity
- Template variable preservation

### Future: Context-Aware Merge (v5.0+)

**Planned**:
- LLM-assisted merge conflict resolution
- Semantic understanding of customizations
- Automated migration guides

---

## Key Takeaways

1. **Three Categories**: structure-only, content-only, hybrid
2. **Explicit Boundaries**: Defined in `.chorabase`, not implicit
3. **Safe Defaults**: When in doubt, content-only
4. **Compose, Don't Modify**: Extend structure through project files
5. **Automated Tooling**: Scripts handle the complexity
6. **Upstream Alignment**: Receive improvements without conflicts

---

## Related Documentation

- [How to: Upgrade Structure from Upstream](../how-to/upgrade-structure-from-upstream.md) - Step-by-step merge guide
- [Reference: .chorabase Metadata Spec](../reference/chorabase-metadata-spec.md) - File format specification
- [SAP Framework](../../skilled-awareness/sap-framework/README.md) - Example of structural content
- [Project Bootstrap](../how-to/project-bootstrap.md) - Creating new projects

---

**Last Updated**: 2025-10-29
**Version**: 1.0 (matches chora-base v4.1.0)
**Maintenance**: Update when merge model evolves
