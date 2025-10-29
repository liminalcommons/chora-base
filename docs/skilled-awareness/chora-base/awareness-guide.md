# Awareness Guide: chora-base Template Repository

**SAP ID**: SAP-002
**Version**: 1.0.0
**Target Audience**: AI agents (Claude Code, Cursor, etc.)
**Last Updated**: 2025-10-27

---

## 1. Quick Reference

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
cat docs/reference/skilled-awareness/INDEX.md
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
1. [README.md](../../../../README.md) (2k tokens) - Overview
2. [protocol-spec.md](protocol-spec.md) (12k tokens) - All capabilities
3. [INDEX.md](../INDEX.md) (5k tokens) - Capability status

**For generating projects**:
1. [AGENTS.md](../../../../AGENTS.md) (3k tokens) - Agent guidance
2. Generation workflow (in Protocol Spec, Section 6.1)

**For creating SAPs**:
1. [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) (5k tokens)
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
3. Create directory: `mkdir docs/reference/skilled-awareness/<capability>/`
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
  1. Create SAP: docs/reference/skilled-awareness/project-bootstrap/
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

## 6. Best Practices

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

## 8. Related Resources

**chora-base-meta SAP**:
- [capability-charter.md](capability-charter.md) - This SAP's charter
- [protocol-spec.md](protocol-spec.md) - All 14 capabilities
- [adoption-blueprint.md](adoption-blueprint.md) - How to adopt chora-base
- [ledger.md](ledger.md) - Adopter tracking

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](../../../../SKILLED_AWARENESS_PACKAGE_PROTOCOL.md)
- [sap-framework/](../sap-framework/)
- [INDEX.md](../INDEX.md)

**Core Docs**:
- [README.md](../../../../README.md)
- [AGENTS.md](../../../../AGENTS.md)
- [CHANGELOG.md](../../../../CHANGELOG.md)

**Claude Patterns**:
- [claude/CONTEXT_MANAGEMENT.md](../../../../claude/CONTEXT_MANAGEMENT.md)
- [claude/CHECKPOINT_PATTERNS.md](../../../../claude/CHECKPOINT_PATTERNS.md)

---

**Version History**:
- **1.0.0** (2025-10-27): Initial awareness guide for chora-base meta-SAP
