# Awareness Guide: chora-base Template Repository

**SAP ID**: SAP-002
**Version**: 1.0.1
**Target Audience**: AI agents (Claude Code, Cursor, etc.)
**Last Updated**: 2025-10-28

---

## 1. Quick Reference

### When to Use This SAP

**Use the chora-base Meta-SAP when**:
- Starting a new Python project and want production-ready scaffolding
- Understanding all capabilities chora-base provides (single source of truth)
- Checking status of specific SAP (testing, CI/CD, docs, etc.)
- Learning how chora-base applies SAP framework to itself (meta-dogfooding example)
- Coordinating across chora-base ecosystem (chora-meta, chora-governance)

**Don't use for**:
- Non-Python projects (chora-base is Python-specific)
- Minimal templates (chora-base is comprehensive, not minimal)
- Projects that don't need AI agent support
- Quick prototypes (chora-base optimized for production)

### Common Agent Tasks

**Generate new project**:
```bash
python setup.py my-project --author "Name" --email "email@example.com"
```

**Understand chora-base**:
1. Read: [protocol-spec.md](protocol-spec.md) (all 14 capabilities)
2. Check: [INDEX.md](../INDEX.md) (capability status)
3. Study: [inbox/](../inbox/) (example SAP)

**Create new SAP**:
1. Read: [document-templates.md](../document-templates.md)
2. Follow: [sap-framework/awareness-guide.md](../sap-framework/awareness-guide.md)
3. Update: [INDEX.md](../INDEX.md)

### Quick Commands

**Find capabilities**:
```bash
cat docs/skilled-awareness/INDEX.md
```

**Generate project**:
```bash
python setup.py <name>
```

**Validate generation**:
```bash
cd <project> && pytest --collect-only
```

---

## 2. Agent Context Loading

### Essential Context (5-10k tokens)

**For understanding chora-base**:
1. [README.md](/README.md) (2k tokens) - Overview
2. [protocol-spec.md](protocol-spec.md) (12k tokens) - All capabilities
3. [INDEX.md](../INDEX.md) (5k tokens) - Capability status

**For generating projects**:
1. [AGENTS.md](/AGENTS.md) (3k tokens) - Agent guidance
2. Generation workflow (in Protocol Spec, Section 6.1)

**For creating SAPs**:
1. [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) (5k tokens)
2. [document-templates.md](../document-templates.md) (4k tokens)
3. [sap-framework/](../sap-framework/) (reference, 15k tokens)

### What to Skip

- ❌ Example projects (unless studying specific feature)
- ❌ CHANGELOG details (just read current version)
- ❌ Individual capability SAPs (unless working on that capability)

---

## 3. Common Workflows

### 3.1 Generate New Project

**Context**: 5k tokens (setup.py logic + blueprint variables)

**Steps**:
1. Run: `python setup.py <project-name> [options]`
2. Inputs: Project name, author, email, optional features
3. Process: Copy static-template → Process blueprints → Rename dirs → Init git
4. Validate: `cd <project> && pytest --collect-only`
5. Success: Project generated, tests loadable

**Time**: 20-40 seconds (Claude-optimized)

### 3.2 Understand Capability

**Context**: 3-5k tokens (capability section from Protocol Spec)

**Steps**:
1. Find capability in Protocol Spec (Section 3)
2. Read: Purpose, Includes, Interfaces, Guarantees
3. Check status in INDEX.md
4. If SAP exists, read Charter for full details

**Example** (understanding testing-framework):
```markdown
Read: protocol-spec.md Section 3.2 "SAP-004: testing-framework"
Check: INDEX.md → Status: Planned (Phase 2)
Result: pytest, coverage ≥85%, conftest.py patterns
```

### 3.3 Create New SAP

**Context**: 10-20k tokens (framework + templates + reference)

**Steps**:
1. Identify capability (add to INDEX.md as Planned)
2. Read framework: [sap-framework/](../sap-framework/)
3. Create directory: `mkdir docs/skilled-awareness/<capability>/`
4. Create 5 artifacts using templates
5. Update INDEX.md (status: Draft)
6. Update chora-base-meta Protocol Spec (add capability overview)

**Time**: 8-20 hours (varies by complexity)

### 3.4 Update chora-base Version

**Context**: 8-12k tokens (CHANGELOG + affected files)

**Steps**:
1. Update version: `pyproject.toml`, `README.md`, `CHANGELOG.md`
2. Create upgrade guide: `docs/upgrades/vX.Y-to-vA.B.md`
3. Update SAP versions if capabilities changed
4. Update chora-base-meta ledger
5. Git commit with version tag

---

## 4. Troubleshooting

### Problem: Generation fails (placeholders not substituted)

**Symptoms**:
- Generated files contain `{{variable}}`
- Tests fail with "undefined variable"

**Solution**:
- Check blueprints/ for typos
- Verify variable names match (project_name, package_name, etc.)
- Re-run generation with `--force`

### Problem: Can't find capability

**Symptoms**:
- Capability mentioned but no SAP exists
- INDEX.md shows "Planned" status

**Solution**:
- Check Protocol Spec Section 3 for overview
- Capability may not have dedicated SAP yet
- Reference implementation in static-template/

### Problem: Meta-SAP diverges from implementation

**Symptoms**:
- Protocol Spec describes feature that doesn't exist
- Version mismatch

**Solution**:
- Check chora-base version (README.md)
- Meta-SAP Protocol should match current version
- File issue if inconsistency found

---

## 5. Integration Patterns

### 5.1 With Project Generation

**Pattern**: Meta-SAP as reference during generation

```
User: "Generate project with testing framework"
Agent:
  1. Load: chora-base-meta Protocol Spec (Section 3.2, SAP-004)
  2. Understand: Testing framework includes pytest, coverage ≥85%
  3. Generate: python setup.py my-project
  4. Validate: pytest --collect-only (verify tests loadable)
```

### 5.2 With SAP Creation

**Pattern**: Meta-SAP Protocol updated when SAP created

```
SAP Created: SAP-003 (project-bootstrap)
Agent:
  1. Create SAP: docs/skilled-awareness/project-bootstrap/
  2. Update INDEX.md: Status Planned → Draft
  3. Update chora-base-meta Protocol: Add link to SAP-003
  4. Commit: "feat(SAP-003): Create project-bootstrap SAP"
```

### 5.3 With Ecosystem Coordination

**Pattern**: Meta-SAP referenced by other repos

```
Adopter (chora-compose): "What capabilities does chora-base provide?"
Agent:
  1. Read: chora-base-meta Protocol Spec
  2. Find: All 14 capabilities with status
  3. Report: Active SAPs, Planned SAPs, dependencies
```

---

## 6. Common Pitfalls

### Pitfall 1: Generating Without Understanding Capabilities
**Scenario**: Agent generates project without reading protocol-spec first, misses key features

**Example** (from Wave 2 audit experience):
```
Agent: "I'll generate a project quickly"
Result: Generated without --no-docker flag, included Docker files user didn't need
Problem: Didn't know optional features exist (--no-docker, --no-memory, --no-claude)
```

**Fix**: Always read protocol-spec.md Section 4.1 (Project Generation Interface) first:
```markdown
Read: protocol-spec.md → Section 4.1 → Optional flags
Generate: python setup.py my-project --no-docker --no-memory
```

**Why it matters**: Unnecessary files clutter project, confuse adopters

### Pitfall 2: Meta-SAP Divergence from Implementation
**Scenario**: Protocol spec describes capability that doesn't exist in actual static-template/

**Example**:
```
Protocol says: "SAP-014 (advanced-metrics) provides X, Y, Z"
Reality: SAP-014 doesn't exist yet (status: Planned in INDEX.md)
Problem: Agent tries to use non-existent capability
```

**Fix**: Always cross-reference INDEX.md for status:
```markdown
Read protocol-spec → See SAP-014 mentioned
Check INDEX.md → Status: Planned (Phase 5)
Result: Don't rely on it yet, wait for Active status
```

**Why it matters**: Prevents errors, sets correct expectations

### Pitfall 3: Skipping SAP Updates After Capability Changes
**Scenario**: New capability added to static-template/ but meta-SAP protocol not updated

**Example** (from SAP development):
```
Developer adds: static-template/scripts/new-tool.sh
Forgets to: Update chora-base-meta protocol-spec Section 3 (capabilities)
Result: Tool exists but undiscovered, violates "single source of truth"
```

**Fix**: Always update meta-SAP when changing capabilities:
```markdown
1. Add feature to static-template/
2. Update chora-base-meta protocol-spec.md
3. Update INDEX.md if new SAP
4. Update ledger.md version history
5. Commit: "feat(capability): Add X, update meta-SAP"
```

**Why it matters**: Meta-SAP must remain single source of truth

### Pitfall 4: Wrong Path References After Wave 1 Migration
**Scenario**: Using old `docs/reference/skilled-awareness/` path instead of new `docs/skilled-awareness/`

**Example** (discovered in Wave 2 SAP-002 audit):
```
OLD (broken): Link path docs/reference/skilled-awareness/INDEX.md
PROBLEM: Wave 1 restructured to docs/skilled-awareness/INDEX.md
```

**Fix**: Always use absolute paths from repo root:
```markdown
CORRECT: [INDEX.md](/docs/skilled-awareness/INDEX.md)
WRONG: Link path ../../../../docs/reference/skilled-awareness/INDEX.md
```

**Why it matters**: Broken links damage user experience, discovered during Wave 2 SAP-002 audit (34 broken links fixed)

### Pitfall 5: Generating Into Existing Directory Without --force
**Scenario**: Re-generating project without --force flag, setup.py fails

**Example**:
```bash
python setup.py my-project
# Oops, need to change options
python setup.py my-project --no-docker
# ERROR: Directory my-project already exists
```

**Fix**: Use --force to overwrite:
```bash
python setup.py my-project --no-docker --force
```

**Why it matters**: Common during iteration, --force makes generation idempotent

---

## 7. Best Practices

### DO

- ✅ Read chora-base-meta Protocol first (single source of truth)
- ✅ Check INDEX.md for capability status
- ✅ Use templates for SAP creation
- ✅ Update meta-SAP when capabilities change
- ✅ Validate generated projects (pytest --collect-only)

### DON'T

- ❌ Generate without understanding capabilities (read Protocol first)
- ❌ Create SAP without framework (follow templates)
- ❌ Skip INDEX.md update (keep registry current)
- ❌ Forget meta-SAP update (keep Protocol synchronized)

---

## 7. Claude-Specific Optimizations

### Context Management

**Load Order** (progressive):
1. Protocol Spec (12k) → Understand all capabilities
2. INDEX.md (5k) → Check status
3. Specific SAP (if needed, 10k) → Deep dive

**Token Budget**:
- Essential: 5-10k (Protocol + INDEX)
- Extended: 15-20k (+ specific SAP)
- Full: 30-40k (+ examples + implementation)

### Parallel Operations

**Project Generation**:
```
Parallel:
  - Copy static-template/
  - Read all blueprints
  - Check git config

Sequential:
  - Rename directories
  - Process blueprints
  - Initialize git
```

**Result**: 20-40 second setup (vs 30-60s for generic agents)

---

## 9. Related Content

### Within This SAP (skilled-awareness/chora-base/)
- [capability-charter.md](capability-charter.md) - Business value and scope of chora-base meta-SAP
- [protocol-spec.md](protocol-spec.md) - Complete technical specification (all 14 capabilities!)
- [adoption-blueprint.md](adoption-blueprint.md) - Step-by-step project generation guide
- [ledger.md](ledger.md) - Adopter tracking and version history

### Developer Process (dev-docs/)
**Workflows**:
- [/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD → BDD → TDD workflow (8-phase lifecycle)

**Setup**:
- [/static-template/scripts/setup.sh](/static-template/scripts/setup.sh) - Environment setup automation
- [/static-template/justfile](/static-template/justfile) - Unified command interface (30+ tasks)

### Project Lifecycle (project-docs/)
**Audits**:
- `/docs/project-docs/audits/wave-2-sap-002-audit.md` - This SAP's audit report (to be created after completion)

**Planning** (to be referenced when created):
- Wave 2 Sprint Plan - SAP audit activities (includes SAP-002)
- Project roadmap - Documentation improvements in Wave 1 and Wave 2

### User Guides (user-docs/)
**Existing**:
- [/docs/user-docs/explanation/architecture-clarification.md](/docs/user-docs/explanation/architecture-clarification.md) - Architecture overview including 4-domain structure
- [/docs/user-docs/explanation/benefits-of-chora-base.md](/docs/user-docs/explanation/benefits-of-chora-base.md) - ROI analysis, time savings, business value

**Planned** (to be created in Wave 2 Phase 5):
- Tutorial: Generate your first chora-base project end-to-end
- How-To: Choose the right optional features (--no-docker, --no-memory, --no-claude)
- Reference: Complete setup.py CLI reference

### Other SAPs (skilled-awareness/)
**Framework**:
- [/docs/skilled-awareness/sap-framework/](/docs/skilled-awareness/sap-framework/) - SAP-000, defines how SAPs work (used to create this meta-SAP!)
- [/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root SAP protocol
- [/docs/skilled-awareness/INDEX.md](/docs/skilled-awareness/INDEX.md) - All 14 SAPs with status

**Related Capabilities**:
- [/docs/skilled-awareness/inbox/](/docs/skilled-awareness/inbox/) - SAP-001, cross-repo coordination
- [/docs/skilled-awareness/documentation-framework/](/docs/skilled-awareness/documentation-framework/) - SAP-007, Diataxis structure
- [/docs/skilled-awareness/testing-framework/](/docs/skilled-awareness/testing-framework/) - SAP-004, pytest and coverage

**Core Documentation**:
- [/README.md](/README.md) - Project overview and quick start
- [/AGENTS.md](/AGENTS.md) - Generic agent guidance (all agents)
- [/CLAUDE_SETUP_GUIDE.md](/CLAUDE_SETUP_GUIDE.md) - Claude-specific setup and patterns
- [/CHANGELOG.md](/CHANGELOG.md) - Version history (currently v3.3.0)

**Claude-Specific Patterns**:
- [/claude/CONTEXT_MANAGEMENT.md](/claude/CONTEXT_MANAGEMENT.md) - Token optimization strategies
- [/claude/CHECKPOINT_PATTERNS.md](/claude/CHECKPOINT_PATTERNS.md) - Save-and-resume patterns

---

**Version History**:
- **1.0.1** (2025-10-28): Added "When to Use" section, "Common Pitfalls" with Wave 2 learnings, enhanced "Related Content" with 4-domain coverage
- **1.0.0** (2025-10-27): Initial awareness guide for chora-base meta-SAP
