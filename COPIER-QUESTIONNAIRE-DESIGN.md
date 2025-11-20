# Copier Questionnaire Design

**Created**: 2025-11-21
**Origin**: OPP-2025-022 → CORD-2025-023 → chora-workspace-q3p7
**Purpose**: Document copier.yml design decisions and usage patterns

---

## Design Goals

1. **<3 minute completion time**: Questionnaire must be fast to complete
2. **Progressive complexity**: Simple modes for quick start, custom mode for advanced users
3. **Sensible defaults**: Standard mode (4 SAPs) recommended for most projects
4. **Clear descriptions**: Each SAP has help text explaining its purpose
5. **Conditional logic**: Dependencies respected, relevant questions only shown when needed

---

## Questionnaire Structure

### Section 1: Project Basics (3 questions)
- **project_name**: Required, validated, lowercase-hyphenated
- **project_description**: Optional, default generated from project name
- **project_author**: Optional, default "Anonymous"

**Completion time**: 30-60 seconds

---

### Section 2: SAP Selection (1 primary question)
- **sap_selection_mode**: Choose mode (minimal, standard, comprehensive, custom)
  - **Minimal (2 SAPs)**: SAP-001 (Inbox) + SAP-015 (Beads) - Quick start, essential coordination
  - **Standard (4 SAPs)**: Adds SAP-053 (Conflict Resolution) + SAP-010 (Memory) - Recommended for most projects
  - **Comprehensive (8 SAPs)**: Adds SAP-051, SAP-052, SAP-056, SAP-008 - Full suite for advanced projects
  - **Custom**: Individual SAP selection (shows 8 additional questions)

**Completion time**:
- Minimal/Standard/Comprehensive: 10 seconds (1 question)
- Custom: 60-90 seconds (1 mode + 8 individual SAP questions)

---

### Section 3: Project Configuration (2-3 questions, conditional)
- **python_version**: Shown if Python-dependent SAPs selected (SAP-053, SAP-056, SAP-008)
- **use_git**: Initialize git repository? (default: true)
- **use_poetry**: Use Poetry for Python dependency management? (shown if Python SAPs selected)

**Completion time**: 20-40 seconds

---

## Total Completion Time Estimate

| Mode | Questions | Estimated Time |
|------|-----------|----------------|
| Minimal | 5-6 | 1.5-2 min |
| Standard | 5-6 | 1.5-2 min |
| Comprehensive | 6-7 | 2-2.5 min |
| Custom | 11-13 | 2.5-3 min |

**Target**: <3 minutes (✅ All modes meet target)

---

## SAP Priority Tiers

### P0: Essential (Always included)
- **SAP-001: Inbox Workflow** - Coordination request management
- **SAP-015: Beads Task Management** - Git-backed issue tracking

### P1: Standard (Recommended for most projects)
- **SAP-053: Conflict Resolution** - Pre-merge conflict detection (v1.0.0)
- **SAP-010: Memory System** - A-MEM event logging and knowledge notes

### P2: Comprehensive (Advanced projects)
- **SAP-051: Pre-merge Validation** - Git hooks for pre-push checks
- **SAP-052: Code Ownership** - CODEOWNERS and PR reviewer suggestions
- **SAP-056: Lifecycle Traceability** - Feature manifest and artifact linkage
- **SAP-008: Automation Dashboard** - Justfile recipes and metrics tracking

---

## Derived Variables

The questionnaire calculates several derived variables for use in template rendering:

### Boolean Flags (per SAP)
- `_sap_001_enabled`, `_sap_015_enabled`, etc.
- Calculated based on `sap_selection_mode` + individual selections in custom mode
- Used in Jinja2 templates to conditionally include SAP artifacts

### Aggregate Variables
- `_sap_count`: Total number of SAPs enabled (used in post-generation message)
- `_project_slug`: Normalized project name (lowercase, hyphenated)

---

## Conditional Logic Examples

### Example 1: Standard Mode
```yaml
sap_selection_mode: standard
# Auto-enables: SAP-001, SAP-015, SAP-053, SAP-010
# Result: 4 SAPs, no additional questions
```

### Example 2: Custom Mode (Select Individual SAPs)
```yaml
sap_selection_mode: custom
include_sap_001: true   # Inbox (recommended)
include_sap_015: true   # Beads (recommended)
include_sap_053: true   # Conflict Resolution
include_sap_010: false  # Memory (skip)
include_sap_051: false  # Pre-merge Validation (skip)
include_sap_052: true   # Code Ownership
include_sap_056: false  # Lifecycle Traceability (skip)
include_sap_008: true   # Automation Dashboard
# Result: 5 SAPs (SAP-001, SAP-015, SAP-053, SAP-052, SAP-008)
```

### Example 3: Python Version Question (Conditional)
```yaml
# Only shown if Python-dependent SAPs selected:
# SAP-053 (Conflict Resolution - conflict-checker.py)
# SAP-056 (Lifecycle Traceability - validate-manifest.py)
# SAP-008 (Automation Dashboard - track-recipe-usage.py)
python_version: "3.11"
```

---

## Template Rendering

Template files use Jinja2 syntax to conditionally include SAP artifacts:

```jinja2
# In template/justfile.jinja
{% if _sap_053_enabled %}
# SAP-053: Conflict Resolution
conflict-check BRANCH='main':
    python scripts/conflict-checker.py --branch {{BRANCH}}
{% endif %}

{% if _sap_001_enabled %}
# SAP-001: Inbox Workflow
inbox-status:
    python scripts/inbox-status.py
{% endif %}
```

```jinja2
# In template/README.md.jinja
# {{ project_name }}

{{ project_description }}

## SAPs Included

{% if _sap_001_enabled %}
- **SAP-001: Inbox Workflow** - Coordination request management (`just inbox-status`)
{% endif %}
{% if _sap_053_enabled %}
- **SAP-053: Conflict Resolution** - Pre-merge conflict detection (`just conflict-check`)
{% endif %}
```

---

## Post-Generation Messages

### After Copy (New Project)
- ✅ Success confirmation with project name
- 📦 List of SAPs included (dynamic based on selections)
- 🚀 Next steps (conditional based on git, poetry, SAPs enabled)
- 📚 Documentation links
- 🎯 Template version and origin tracking

### After Update (Existing Project)
- ✅ Update confirmation
- 📦 Changes applied summary
- ⚠️ Manual review checklist (merge conflicts, config changes)
- 📚 Update guide reference

---

## Validation Rules

### Project Name
```yaml
validator: "{% if not project_name %}Project name is required{% endif %}"
```
- Required field
- Should be lowercase, hyphenated
- Auto-normalized to `_project_slug` for directory name

### SAP Dependencies
- SAP-001 and SAP-015 always enabled (P0 essential SAPs)
- No explicit dependency validation needed (SAPs are independent at template level)
- Runtime dependencies (e.g., Python, git) documented in post-generation message

---

## Usage Examples

### Minimal Project (Quick Start)
```bash
copier copy gh:liminalcommons/chora-base my-project
# Answer: sap_selection_mode = minimal
# Result: 2 SAPs (Inbox + Beads), <2 min setup
```

### Standard Project (Recommended)
```bash
copier copy gh:liminalcommons/chora-base my-project
# Answer: sap_selection_mode = standard (default)
# Result: 4 SAPs (Inbox + Beads + Conflict Resolution + Memory), <2 min setup
```

### Comprehensive Project (Full Suite)
```bash
copier copy gh:liminalcommons/chora-base my-project
# Answer: sap_selection_mode = comprehensive
# Result: 8 SAPs (all included), <3 min setup
```

### Custom Project (Pick SAPs)
```bash
copier copy gh:liminalcommons/chora-base my-project
# Answer: sap_selection_mode = custom
# Then select individual SAPs
# Result: Custom SAP combination, <3 min setup
```

---

## Design Trade-offs

### ✅ Chose: Mode-based Selection (minimal/standard/comprehensive/custom)
**Why**: Faster completion for most users (1 question vs 8)
**Trade-off**: Less granular control in preset modes (mitigated by custom mode)

### ✅ Chose: SAP-001 and SAP-015 Always Enabled
**Why**: Essential SAPs for chora ecosystem projects (coordination + task tracking)
**Trade-off**: Users can't opt-out (acceptable: these are foundational)

### ✅ Chose: Jinja2 Templates (not Python hooks)
**Why**: Simpler, faster, easier to maintain
**Trade-off**: Less dynamic logic (acceptable: conditional inclusion sufficient)

### ✅ Chose: Post-generation Messages (not Interactive Wizard)
**Why**: Non-blocking, users can proceed immediately
**Trade-off**: Users might miss next steps (mitigated by clear README and messages)

---

## Future Enhancements (v1.1+)

### Potential Additions:
1. **SAP version selection**: Choose SAP versions (e.g., SAP-053 v1.0.0 vs v1.1.0)
2. **Project type detection**: Auto-select SAPs based on project type (Python, Node.js, Docker)
3. **Dependency validation**: Warn if conflicting SAPs selected
4. **Profile presets**: Save custom SAP selections as profiles for reuse
5. **Update preview**: Show what will change before running `copier update`

### Not Planned (Out of Scope):
- GUI-based questionnaire (CLI-only for v1.0)
- IDE integrations (VSCode extension, etc.)
- Non-Python project templates (focus on Python initially)
- Enterprise features (SSO, organization templates)

---

## Validation Tests

### Test 1: Minimal Mode (<2 min completion)
```bash
# Provide answers via file:
echo "project_name: test-minimal
sap_selection_mode: minimal
use_git: true" > answers-minimal.yml

copier copy packages/chora-base test-minimal --answers-file answers-minimal.yml
# Expected: Project created in <2 min, 2 SAPs included
```

### Test 2: Standard Mode (<2 min completion)
```bash
echo "project_name: test-standard
sap_selection_mode: standard
python_version: '3.11'
use_git: true
use_poetry: true" > answers-standard.yml

copier copy packages/chora-base test-standard --answers-file answers-standard.yml
# Expected: Project created in <2 min, 4 SAPs included
```

### Test 3: Comprehensive Mode (<3 min completion)
```bash
echo "project_name: test-comprehensive
sap_selection_mode: comprehensive
python_version: '3.11'
use_git: true
use_poetry: true" > answers-comprehensive.yml

copier copy packages/chora-base test-comprehensive --answers-file answers-comprehensive.yml
# Expected: Project created in <3 min, 8 SAPs included
```

### Test 4: Custom Mode (<3 min completion)
```bash
echo "project_name: test-custom
sap_selection_mode: custom
include_sap_001: true
include_sap_015: true
include_sap_053: true
include_sap_010: false
include_sap_051: false
include_sap_052: true
include_sap_056: false
include_sap_008: true
python_version: '3.11'
use_git: true
use_poetry: true" > answers-custom.yml

copier copy packages/chora-base test-custom --answers-file answers-custom.yml
# Expected: Project created in <3 min, 5 SAPs included (001, 015, 053, 052, 008)
```

---

## Related Artifacts

**Origin**: OPP-2025-022 (Priority 28.5) → CORD-2025-023 → chora-workspace-q3p7
**Template**: packages/chora-base/copier.yml
**Template Directory**: packages/chora-base/template/ (to be created in Phase 1.2)
**Documentation**: This file + packages/chora-base/README.md (template usage section)
**Tests**: packages/chora-base/tests/test_template_generation.py (Phase 2)

---

**Status**: Phase 1.1 Complete (2025-11-21)
**Next**: Phase 1.2 - Build template/ directory structure (chora-workspace-f2si)
**Trace ID**: sap-distribution-copier-2025-11-21
