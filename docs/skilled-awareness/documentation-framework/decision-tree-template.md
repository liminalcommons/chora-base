# SAP-007 Decision Tree Template

**Purpose**: Copy this decision tree to your project's AGENTS.md files to help agents and developers quickly categorize new documentation.

**Location**: Add to root AGENTS.md, dev-docs/AGENTS.md, user-docs/AGENTS.md, and project-docs/AGENTS.md

**Customization**: Replace `[PROJECT_SPECIFIC]` placeholders with your project's actual subdirectories and examples.

---

## Creating New Documentation (SAP-007 Decision Tree)

**Where should this doc go?**

### Step 1: Root Directory? (Only if Essential)

**Question**: Is this documentation so critical it requires maximum visibility?

**Allowed root files** (customize `ALLOWED_ROOT_FILES` in validation script):
- `README.md` - Project overview (first impression for new users)
- `AGENTS.md` - Agent awareness guide (SAP-009)
- `CLAUDE.md` - Claude-specific workflows (SAP-009)
- `CHANGELOG.md` - Version history (release tracking)
- `CONTRIBUTING.md` - Contribution guidelines (community onboarding)
- `LICENSE.md` - Legal license (legal requirement)
- `DOCUMENTATION_STANDARD.md` - Doc writing standards (SAP-007 reference)
- `ROADMAP.md` - Strategic vision (optional, planning)
- **[PROJECT_SPECIFIC.md]** - (document rationale in AGENTS.md if adding)

**Policy**: Root directory limited to ≤8 markdown files for navigability.

**If NO** → Continue to Step 2 (use 3-directory structure)

---

### Step 2: User-Facing Documentation? → `user-docs/`

**Question**: Is this documentation for end-users of the product/library?

**If YES**, choose subdirectory by Diataxis type:

#### Tutorial (Learning-oriented)
- **Purpose**: Teach through step-by-step lessons
- **Location**: `user-docs/tutorials/`
- **Example**: "Build your first MCP server", "Getting started with chora-base"
- **Structure**: Sequential steps with expected output

#### How-To Guide (Task-oriented)
- **Purpose**: Solve specific problems
- **Location**: `user-docs/how-to/`
- **Example**: "How to add custom error handling", "How to deploy to production"
- **Structure**: Problem → Solution with variations

#### Reference (Information-oriented)
- **Purpose**: Provide technical specifications
- **Location**: `user-docs/reference/`
- **Example**: "API Reference", "Configuration Schema", "CLI Commands"
- **Structure**: API docs, schemas, configurations

#### Explanation (Understanding-oriented)
- **Purpose**: Explain concepts and design decisions
- **Location**: `user-docs/explanation/`
- **Example**: "Why we use Diataxis", "Architecture overview"
- **Structure**: Context, rationale, trade-offs

**If NO** → Continue to Step 3

---

### Step 3: Developer Documentation? → `dev-docs/`

**Question**: Is this documentation for developers contributing to the project?

**If YES**, choose subdirectory:

#### Development Workflows
- **Purpose**: Development processes (DDD, BDD, TDD, etc.)
- **Location**: `dev-docs/workflows/`
- **Example**: "Test-Driven Development", "Git branching strategy"

#### Vision & Planning
- **Purpose**: Long-term plans, capability evolution
- **Location**: `dev-docs/vision/`
- **Example**: "Roadmap 2025", "Future capabilities"

#### Code Examples
- **Purpose**: Walkthroughs, code examples, patterns
- **Location**: `dev-docs/examples/`
- **Example**: "Custom tool implementation", "Advanced patterns"

#### [PROJECT_SPECIFIC_DEV_SUBDIRS]
- **Purpose**: [Add your project's specific dev doc categories]
- **Location**: `dev-docs/[subdirectory]/`
- **Example**: [Add examples relevant to your project]

**If NO** → Continue to Step 4

---

### Step 4: Project Management Documentation? → `project-docs/`

**Question**: Is this documentation for project management, planning, or tracking?

**If YES**, choose subdirectory (customize for your project):

#### Sprint Planning & Retrospectives
- **Purpose**: Sprint planning, daily standups, retrospectives
- **Location**: `project-docs/sprints/`
- **Example**: "Sprint 23 plan", "Sprint 22 retrospective"

#### Release Planning
- **Purpose**: Release planning, upgrade guides, version tracking
- **Location**: `project-docs/releases/`
- **Example**: "v2.0.0 release plan", "Upgrade guide v1 → v2"

#### Process Metrics
- **Purpose**: Velocity tracking, team metrics, KPIs
- **Location**: `project-docs/metrics/`
- **Example**: "Q4 velocity report", "Team performance metrics"

#### Architecture Decisions
- **Purpose**: ADRs (Architecture Decision Records), design decisions
- **Location**: `project-docs/decisions/`
- **Example**: "ADR-001: Choose SQLite for persistence"

#### Project Retrospectives
- **Purpose**: Project-level retrospectives, lessons learned
- **Location**: `project-docs/retrospectives/`
- **Example**: "Q4 2024 retrospective", "Lessons learned from feature X"

#### [PROJECT_SPECIFIC_PROJECT_SUBDIRS]
- **Purpose**: [Add your project's specific project doc categories]
- **Location**: `project-docs/[subdirectory]/`
- **Example**: [Add examples relevant to your project]

---

## Validation & Enforcement

### Quick Validation

**Before committing**, run validation to check compliance:

```bash
# From repository root
python docs/skilled-awareness/documentation-framework/templates/validate-sap-007-structure.py
```

**Expected output** (if compliant):
```
[PASS] SAP-007 validation PASSED
- Root directory: Clean (≤8 files)
- project-docs/: Properly structured
- No orphaned docs
```

---

### Install Pre-Commit Hook (Level 3 Enforcement)

**Prevent violations automatically**:

```bash
# Option 1: Install to .git/hooks/
cp docs/skilled-awareness/documentation-framework/templates/sap-007-check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Option 2: Install to .githooks/ (recommended for team projects)
mkdir -p .githooks
cp docs/skilled-awareness/documentation-framework/templates/sap-007-check.sh .githooks/pre-commit
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

**Result**: Pre-commit hook blocks commits that violate SAP-007 structure.

**Bypass** (use only with valid reason):
```bash
git commit --no-verify -m "reason for bypassing SAP-007 validation"
```

---

## Common Scenarios

### Scenario 1: Completion Report
**Document**: "SAP-007 L2 adoption completed"
**Answer**: `project-docs/sprints/` or `project-docs/retrospectives/`
**Rationale**: Project management documentation (tracking adoption work)

### Scenario 2: API Reference
**Document**: "Server API reference"
**Answer**: `user-docs/reference/`
**Rationale**: User-facing, information-oriented (Diataxis: Reference)

### Scenario 3: Coding Standards
**Document**: "Python coding standards"
**Answer**: `dev-docs/workflows/` or `CONTRIBUTING.md`
**Rationale**: Developer workflow documentation

### Scenario 4: Architecture Decision
**Document**: "ADR-003: Why we chose FastAPI"
**Answer**: `project-docs/decisions/`
**Rationale**: Project management, architecture decision record

### Scenario 5: Tutorial
**Document**: "Build your first MCP server"
**Answer**: `user-docs/tutorials/`
**Rationale**: User-facing, learning-oriented (Diataxis: Tutorial)

---

## Resources

- **SAP-007 Full Documentation**: [docs/skilled-awareness/documentation-framework/](.)
- **Validation Script**: [templates/validate-sap-007-structure.py](templates/validate-sap-007-structure.py)
- **Pre-Commit Hook**: [templates/sap-007-check.sh](templates/sap-007-check.sh)
- **Diataxis Framework**: https://diataxis.fr/
- **SAP-031 Enforcement**: [docs/skilled-awareness/discoverability-based-enforcement/](../discoverability-based-enforcement/)

---

## Customization Guide

### 1. Customize Root Files

Edit `ALLOWED_ROOT_FILES` in [validate-sap-007-structure.py](templates/validate-sap-007-structure.py):

```python
ALLOWED_ROOT_FILES = [
    "README.md",
    "AGENTS.md",
    # Add your project-specific root files here
    "YOUR_ESSENTIAL_FILE.md",  # Document why this is essential
]
```

**Document rationale** in your project's AGENTS.md for any additions beyond the standard 8.

### 2. Customize project-docs/ Subdirectories

Edit `REQUIRED_PROJECT_DOCS_SUBDIRS` in [validate-sap-007-structure.py](templates/validate-sap-007-structure.py):

```python
REQUIRED_PROJECT_DOCS_SUBDIRS = [
    "sprints",
    "releases",
    # Add your project-specific subdirectories
    "your-custom-subdir",
]
```

### 3. Add Project-Specific Examples

Replace `[PROJECT_SPECIFIC]` placeholders in this decision tree with:
- Your actual subdirectory names
- Real examples from your project
- Project-specific guidance

---

**Version**: 1.0.0 (SAP-007 v1.1.0)
**Last Updated**: 2025-11-09
**SAP Integration**: Implements SAP-031 Layer 1 (Discoverability)
