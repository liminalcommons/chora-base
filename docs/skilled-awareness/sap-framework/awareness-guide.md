# Awareness Guide: SAP Framework

**SAP ID**: SAP-000
**Version**: 1.0.0
**Target Audience**: AI agents (Claude Code, Cursor, etc.)
**Last Updated**: 2025-10-27

---

## 1. Quick Reference

### When to Use This SAP

**Use the SAP Framework when**:
- Creating a new capability that will be reused across projects
- Standardizing an existing capability for external adoption
- Documenting a complex capability that needs clear contracts
- Coordinating a capability across multiple repositories

**Don't use SAPs for**:
- One-off scripts or utilities (use `scripts/` directly)
- Project-specific configurations (use project docs)
- Experimental features (wait for stability)
- Simple documentation updates (edit docs directly)

### Common Agent Tasks

**Create new SAP** (Example: Creating SAP-016 Link Validation):
1. Read: [document-templates.md](../document-templates.md)
2. Create directory: `docs/skilled-awareness/link-validation-reference-management/`
3. Create 5 artifacts using templates (charter, protocol, awareness-guide, blueprint, ledger)
4. Update SAP Index: [INDEX.md](../INDEX.md)

**Install SAP** (Example: Installing SAP-001 Inbox):
1. Read: `docs/skilled-awareness/inbox/adoption-blueprint.md`
2. Execute installation steps sequentially
3. Run validation commands
4. Update ledger: `docs/skilled-awareness/inbox/ledger.md`

**Upgrade SAP** (Future example when upgrades exist):
1. Check current version in ledger
2. Locate upgrade blueprint: `docs/skilled-awareness/testing-framework/upgrades/v1.0-to-v1.5.md`
3. Execute upgrade steps
4. Update ledger with new version

### Quick Commands

**Find all SAPs**:
```bash
ls docs/skilled-awareness/*/capability-charter.md
```

**Check SAP status**:
```bash
grep "^status:" docs/skilled-awareness/<sap>/capability-charter.md
```

**Validate SAP completeness**:
```bash
# Check for all 5 artifacts
ls docs/skilled-awareness/<sap>/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md
```

---

## 2. Agent Context Loading

### Essential Context (0-10k tokens)

**For creating a new SAP**:
1. [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) (5k tokens)
2. [document-templates.md](../document-templates.md) (4k tokens)
3. [capability-charter.md](capability-charter.md) (this SAP's charter, 3k tokens)

**For installing a SAP**:
1. Target SAP's `adoption-blueprint.md` (2-4k tokens)
2. Target SAP's `protocol-spec.md` (3-5k tokens)

**For understanding SAPs**:
1. [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) (5k tokens)
2. [inbox SAP](../inbox/) as reference (10k tokens)

### Extended Context (10-50k tokens)

**For SAP development**:
1. All 5 framework SAP artifacts (this directory)
2. Inbox SAP (reference implementation)
3. SAP roadmap
4. DDD → BDD → TDD workflows

**For ecosystem understanding**:
1. All SAPs in INDEX.md
2. Cross-SAP dependencies
3. Adopter ledgers

### What to Skip

- ❌ SAP infrastructure files (load only if needed)
- ❌ SAP examples (load only if working on that capability)
- ❌ Archived SAPs (unless migrating from them)
- ❌ Upgrade blueprints (unless upgrading)

---

## 3. Common Workflows

### 3.1 Create New SAP

**Context Needed**:
- Capability name (kebab-case)
- Problem statement (from requirements)
- Scope (what's included/excluded)

**Steps**:

1. **Create SAP directory**:
   ```bash
   mkdir -p docs/skilled-awareness/<capability-name>
   ```

2. **Create capability-charter.md**:
   - Read template: [document-templates.md](../document-templates.md#capability-charter)
   - Fill in all 11 sections
   - Include YAML frontmatter:
     ```yaml
     ---
     sap_id: SAP-NNN
     version: 0.1.0
     status: Draft
     last_updated: YYYY-MM-DD
     ---
     ```

3. **Create protocol-spec.md**:
   - Read template: [document-templates.md](../document-templates.md#protocol-specification)
   - Define technical contract
   - Include interfaces, data models, behavior

4. **Create awareness-guide.md**:
   - Read template: [document-templates.md](../document-templates.md#awareness-guide)
   - Write for AI agent audience
   - Include quick reference, workflows, troubleshooting

5. **Create adoption-blueprint.md**:
   - Read template: [document-templates.md](../document-templates.md#adoption-blueprint)
   - Write installation steps (agent-executable)
   - Include validation commands

6. **Create ledger.md**:
   - Read template: [document-templates.md](../document-templates.md#traceability-ledger)
   - Initialize adopter registry (empty)
   - Document version history

7. **Update SAP Index**:
   - Edit: [INDEX.md](../INDEX.md)
   - Add row for new SAP

**Validation**:
```bash
# Check all 5 artifacts exist
ls docs/skilled-awareness/<capability-name>/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md

# Check frontmatter valid
grep "^---$" docs/skilled-awareness/<capability-name>/capability-charter.md | wc -l
# Should output: 2 (opening and closing ---)
```

**Output**: ✅ New SAP created (status: Draft)

### 3.2 Install SAP (Agent Execution)

**Context Needed**:
- Target project directory
- SAP to install
- Current project state

**Steps**:

1. **Read adoption blueprint**:
   ```bash
   cat docs/skilled-awareness/<sap>/adoption-blueprint.md
   ```

2. **Check prerequisites**:
   - Verify versions (e.g., chora-base v3.0+, Python 3.11+)
   - Check dependencies (other SAPs)
   - Confirm environment ready

3. **Execute installation steps sequentially**:
   - For each step in blueprint:
     - **Create directories**: Use `Bash(mkdir)` or `Write`
     - **Copy files**: Use `Read` (source) + `Write` (target)
     - **Update files**: Use `Edit` (for existing files like AGENTS.md)
     - **Run commands**: Use `Bash`

4. **Run validation commands**:
   - Execute validation commands from blueprint
   - Verify output matches expected (e.g., `✅ Installed`)

5. **Update ledger** (if applicable):
   - Edit ledger: `docs/skilled-awareness/<sap>/ledger.md`
   - Add adopter record:
     ```markdown
     | <project-name> | <version> | Pilot | <date> | Initial installation |
     ```
   - Create PR if in chora-base repo

6. **Report success**:
   - Output: `✅ SAP <capability-name> v<version> installed successfully`

**Example** (inbox SAP installation):
```markdown
# Step 1: Read blueprint
cat docs/skilled-awareness/inbox/adoption-blueprint.md

# Step 2: Create directory
mkdir -p inbox/coordination/CAPABILITIES

# Step 3: Copy schema
cp inbox/schemas/coordination-request.json <target>/inbox/schemas/

# Step 4: Validate
ls inbox/coordination/CAPABILITIES && echo "✅ Inbox installed"
```

**Validation**:
- All validation commands succeed
- No error messages
- Ledger updated (if applicable)

**Output**: ✅ SAP installed

### 3.3 Upgrade SAP

**Context Needed**:
- Current SAP version (from ledger)
- Target SAP version
- Project directory

**Steps**:

1. **Check current version**:
   ```bash
   # Find current version in ledger or project metadata
   grep "<project-name>" docs/skilled-awareness/<sap>/ledger.md
   ```

2. **Determine upgrade path**:
   - Current: v1.0.0
   - Target: v2.0.0
   - Path: v1.0.0 → v1.5.0 → v2.0.0 (if intermediate versions exist)

3. **Locate upgrade blueprints**:
   ```bash
   ls docs/skilled-awareness/<sap>/upgrades/v1.0-to-v1.5.md
   ls docs/skilled-awareness/<sap>/upgrades/v1.5-to-v2.0.md
   ```

4. **Execute each upgrade sequentially**:
   - Read upgrade blueprint
   - Execute steps (same process as installation)
   - Validate upgrade
   - Repeat for next upgrade

5. **Update ledger**:
   - Edit ledger: `docs/skilled-awareness/<sap>/ledger.md`
   - Update version and upgrade date

6. **Report success**:
   - Output: `✅ Upgraded to v<version>`

**Error Handling**:
- Missing intermediate version → Report required upgrade path
- Validation failure → Follow rollback instructions
- Breaking change → Show migration notes from upgrade blueprint

**Output**: ✅ SAP upgraded

### 3.4 Create SAP Release

**Context Needed**:
- SAP directory
- Changes since last version
- Version number (semantic versioning)

**Steps**:

1. **Determine version bump**:
   - Breaking changes → MAJOR (v1.0.0 → v2.0.0)
   - New features → MINOR (v1.0.0 → v1.1.0)
   - Bug fixes → PATCH (v1.0.0 → v1.0.1)

2. **Update version in all artifacts**:
   ```bash
   # Update YAML frontmatter in all 5 artifacts
   # Change: version: X.Y.Z
   ```

3. **Create upgrade blueprint (if MAJOR)**:
   - Create: `<sap>/upgrades/vX.Y-to-vA.B.md`
   - Document breaking changes
   - Provide migration steps
   - Include rollback instructions

4. **Update ledger**:
   - Add version to history table
   - Document changes

5. **Create PR**:
   - Commit changes
   - Create PR with title: `SAP-NNN: Release v<version>`
   - Include changelog in PR description

6. **Notify adopters** (if Active SAP):
   - Use inbox broadcast workflow
   - Send notification to adopter repos

**Output**: ✅ SAP release created

---

## 4. Common Pitfalls

### Pitfall 1: Broken Path References After Restructure

**Symptom**: SAP references files using old path structure, links break after docs restructure

**Example from Wave 1/2**:
```
<!-- OLD (broken after Wave 1): -->
Link: ../../reference/skilled-awareness/document-templates.md

<!-- NEW (correct): -->
Link: ../document-templates.md
```

**Cause**: Hard-coded paths break when directory structure changes

**Solution**:
- Use relative paths from current file location
- Use absolute paths from repo root (`/docs/...`) for critical references
- Run link validation after any file moves: `./scripts/validate-links.sh docs/skilled-awareness/`

**Prevention**: Always validate links before releasing SAP

---

### Pitfall 2: Missing Cross-Domain References

**Symptom**: SAP only references skilled-awareness/ files, missing integration with dev-docs/, user-docs/, project-docs/

**Example from SAP-000 audit**:
```markdown
<!-- BEFORE (limited): -->
Cross-domain coverage: 1/4 domains (25%)

<!-- AFTER (enhanced): -->
Cross-domain coverage: 3/4 domains (75%)
- dev-docs/workflows/ - SAP creation workflow
- user-docs/explanation/ - What are SAPs concept guide
- skilled-awareness/ - Templates, index, protocol
```

**Cause**: Focusing only on SAP-to-SAP references, forgetting wider ecosystem

**Solution**:
- Explicitly reference dev-docs/ workflows
- Create user-facing explanation docs in user-docs/
- Link to project-docs/ for lifecycle tracking
- Add "Related Content" section showing all 4 domains

**Prevention**: Use SAP Audit Workflow Step 2 (Cross-Domain Gap Analysis)

---

### Pitfall 3: Placeholder Examples Instead of Concrete Ones

**Symptom**: Awareness guide uses generic placeholders like `<sap>/`, hard for users to understand

**Example**:
```markdown
<!-- BAD (placeholder): -->
Read: `<sap>/adoption-blueprint.md`

<!-- GOOD (concrete): -->
Read: `docs/skilled-awareness/inbox/adoption-blueprint.md` (for SAP-001)
```

**Cause**: Copy-pasting template examples without customizing

**Solution**:
- Replace all `<sap>/` with actual SAP names (inbox, testing-framework, etc.)
- Use recent SAPs as examples (SAP-016 Link Validation from Wave 2)
- Reference actual files that exist in repository

**Prevention**: Step 6 of SAP Audit Workflow (Enhance Awareness Guide)

---

### Pitfall 4: Creating SAPs Too Early

**Symptom**: SAP created for experimental feature, then feature changes significantly

**Example**: Don't create SAP for "AI feature X" until it's stable

**Cause**: Premature standardization

**Solution**:
- Wait for capability to stabilize (used in 2-3 projects)
- Pilot in one project first
- Mark as "Draft" until proven
- Use "Experimental" tag for early-stage capabilities

**Prevention**: Follow SAP lifecycle (Draft → Pilot → Active)

---

### Pitfall 5: Skipping Ledger Updates

**Symptom**: Can't track who's using which version of SAP

**Example**: External project adopts SAP-004 but never updates ledger

**Cause**: Forgetting to update ledger after installation

**Solution**:
- Make ledger update a required step in adoption blueprint
- Automate ledger updates where possible
- Review ledgers during quarterly SAP reviews

**Prevention**: Include ledger update in validation commands

---

## 5. Troubleshooting

### Problem: Blueprint step fails during installation

**Symptoms**:
- Command returns error
- File not found
- Permission denied

**Diagnosis**:
1. Check prerequisites (versions, dependencies)
2. Verify current directory
3. Check file permissions
4. Review blueprint instructions

**Solutions**:
- **Missing prerequisites**: Install required dependencies
- **Wrong directory**: Navigate to correct location
- **Permission denied**: Use `chmod` or run as appropriate user
- **Blueprint error**: Report issue to SAP maintainer

**Prevention**:
- Always check prerequisites before starting
- Use validation commands after each step
- Read troubleshooting section in blueprint

### Problem: SAP version conflict

**Symptoms**:
- Installed version doesn't match ledger
- Upgrade blueprint not found
- Dependency version mismatch

**Diagnosis**:
1. Check installed version (ledger or project metadata)
2. Check required version (dependency specification)
3. Check available upgrade blueprints

**Solutions**:
- **Version mismatch**: Upgrade to required version
- **Missing upgrade path**: Upgrade sequentially (v1.0 → v1.5 → v2.0)
- **Dependency conflict**: Upgrade dependency SAP first

**Prevention**:
- Keep ledger updated
- Follow sequential upgrade paths
- Check dependencies before upgrading

### Problem: Incomplete SAP artifacts

**Symptoms**:
- Missing artifact (e.g., no adoption-blueprint.md)
- Invalid YAML frontmatter
- Incomplete sections

**Diagnosis**:
1. Check for all 5 artifacts:
   ```bash
   ls <sap>/{capability-charter,protocol-spec,awareness-guide,adoption-blueprint,ledger}.md
   ```
2. Validate YAML frontmatter:
   ```bash
   grep "^---$" <sap>/capability-charter.md | wc -l
   # Should output: 2
   ```

**Solutions**:
- **Missing artifact**: Create from template
- **Invalid frontmatter**: Fix YAML syntax
- **Incomplete sections**: Fill in missing content

**Prevention**:
- Use templates for new SAPs
- Validate completeness before marking as Pilot
- Follow quality gates

### Problem: Agent can't parse blueprint

**Symptoms**:
- Unclear instructions
- Ambiguous steps
- Missing validation commands

**Diagnosis**:
1. Review blueprint format
2. Check for clear, numbered steps
3. Verify validation commands present

**Solutions**:
- **Unclear instructions**: Rewrite for clarity
- **Ambiguous steps**: Add detailed sub-steps
- **Missing validation**: Add validation commands

**Prevention**:
- Test blueprints with agent before release
- Use simple, explicit language
- Include validation for every step

---

## 5. Integration with Other Capabilities

### 5.1 Integration with DDD → BDD → TDD

**DDD Phase**:
- Create Charter (problem, scope, outcomes)
- Create Protocol Spec (technical contract)
- Get stakeholder approval

**BDD Phase**:
- Extract acceptance criteria from Charter
- Write acceptance tests (optional for SAPs)

**TDD Phase**:
- Create infrastructure
- Write Awareness Guide (document patterns as you implement)
- Write Adoption Blueprint (document installation as you test)
- Create Ledger (initialize tracking)

**Result**: Complete SAP with all artifacts

### 5.2 Integration with Inbox Coordination

**Scenario**: Multi-repo capability (like inbox SAP itself)

**Steps**:
1. Create SAP in owning repo
2. Create coordination request in inbox system
3. Triage coordination request during sprint planning
4. Notify dependent repos when SAP reaches Active status
5. Track adoption in ledger

**Example**: inbox SAP coordinated across chora-base, ecosystem-manifest, mcp-orchestration, mcp-gateway

### 5.3 Integration with Documentation Framework

**SAP artifacts follow Diataxis**:
- **Capability Charter** = Explanation (understanding)
- **Protocol Specification** = Reference (information)
- **Awareness Guide** = How-To (tasks)
- **Adoption Blueprint** = Tutorial (learning)
- **Traceability Ledger** = Reference (tracking)

**Result**: SAPs naturally fit into Diataxis documentation structure

---

## 6. Best Practices for Agents

### 6.1 Creating SAPs

**DO**:
- ✅ Start with Charter (understand problem before solving)
- ✅ Use templates (consistency)
- ✅ Write for both humans and agents (dual audience)
- ✅ Include examples (reference implementations)
- ✅ Test blueprints (install in clean environment)

**DON'T**:
- ❌ Skip sections (all sections required)
- ❌ Write shell scripts (use blueprints)
- ❌ Hardcode values (use templates/placeholders)
- ❌ Assume prerequisites (explicitly list)
- ❌ Forget validation (always include)

### 6.2 Installing SAPs

**DO**:
- ✅ Read entire blueprint before starting
- ✅ Check prerequisites first
- ✅ Execute steps sequentially
- ✅ Run validation after each step
- ✅ Report issues clearly

**DON'T**:
- ❌ Skip steps (even if they seem redundant)
- ❌ Modify blueprint instructions (follow exactly)
- ❌ Continue after validation failure (troubleshoot first)
- ❌ Forget to update ledger (track adoption)

### 6.3 Upgrading SAPs

**DO**:
- ✅ Check current version first
- ✅ Follow sequential upgrade path
- ✅ Read upgrade blueprint completely
- ✅ Backup before major upgrades
- ✅ Test after upgrade

**DON'T**:
- ❌ Skip versions (v1.0 → v3.0 directly)
- ❌ Ignore breaking changes (read upgrade notes)
- ❌ Forget rollback plan (have escape hatch)
- ❌ Upgrade multiple SAPs simultaneously (one at a time)

### 6.4 Context Management (Claude-Specific)

**Progressive Loading**:
1. Load protocol (5k tokens) → Understand SAP structure
2. Load target SAP charter (3k tokens) → Understand capability
3. Load blueprint (2-4k tokens) → Execute installation
4. Load additional artifacts as needed

**Context Optimization**:
- Use summaries for completed steps
- Drop infrastructure files after understanding structure
- Cache common patterns (blueprint format, YAML frontmatter)

**Token Budget**:
- Essential: 10-15k tokens (protocol + charter + blueprint)
- Extended: 30-40k tokens (all 5 artifacts + examples)
- Full: 50-60k tokens (all SAPs + dependencies)

---

## 7. Related Content

This SAP integrates with content across all 4 chora-base domains:

### Developer Process (dev-docs/)

**Workflows**:
- [SAP Audit Workflow](/docs/dev-docs/workflows/SAP_AUDIT_WORKFLOW.md) - Systematic SAP quality assurance (Wave 2)
- [Documentation Migration Workflow](/docs/dev-docs/workflows/DOCUMENTATION_MIGRATION_WORKFLOW.md) - File restructuring patterns
- [Development Lifecycle](/static-template/dev-docs/workflows/DEVELOPMENT_LIFECYCLE.md) - DDD → BDD → TDD integration

**Future** (to be created in Phase 5):
- `dev-docs/workflows/SAP_CREATION_WORKFLOW.md` - Step-by-step SAP creation process
- `dev-docs/examples/creating-sap-016.md` - Walkthrough of link validation SAP creation

### Project Lifecycle (project-docs/)

**Planning**:
- [chora-base SAP Roadmap](../chora-base-sap-roadmap.md) - Phased 14-SAP adoption plan (Phases 1-4)
- [Wave 2 Sprint Plan](/docs/project-docs/sprints/wave-2-sprint-plan.md) - SAP audit execution plan

**Audits** (Wave 2):
- [SAP-000 Audit Report](/docs/project-docs/audits/wave-2-sap-000-audit.md) - This SAP's audit results
- Additional SAP audits to be created in Wave 2 Phases 2-4

**Metrics** (future):
- `project-docs/metrics/sap-adoption-metrics.md` - Track SAP usage across projects

### Product Documentation (user-docs/)

**Future** (to be created in Phase 5):
- `user-docs/explanation/what-are-saps.md` - Conceptual overview for end users
- `user-docs/how-to/create-a-sap.md` - User-facing creation guide
- `user-docs/reference/sap-artifact-structure.md` - Quick reference guide

**Existing**:
- [How to Write Executable Documentation](/docs/user-docs/how-to/write-executable-documentation.md) - Patterns used in SAP blueprints

### Skilled Awareness (SAPs)

**SAP Framework**:
- [SKILLED_AWARENESS_PACKAGE_PROTOCOL.md](/SKILLED_AWARENESS_PACKAGE_PROTOCOL.md) - Root protocol (single source of truth)
- [capability-charter.md](capability-charter.md) - Framework charter (this SAP)
- [protocol-spec.md](protocol-spec.md) - Technical specification
- [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- [ledger.md](ledger.md) - Adopter tracking

**Templates & Index**:
- [document-templates.md](../document-templates.md) - SAP artifact templates
- [INDEX.md](../INDEX.md) - SAP registry (15 SAPs as of Wave 2)

**Reference SAPs**:
- [SAP-001: Inbox Coordination](../inbox/) - Complete pilot SAP (multi-repo)
- [SAP-016: Link Validation](../link-validation-reference-management/) - Latest SAP (Wave 2)
- [SAP-007: Documentation Framework](../documentation-framework/) - Diátaxis integration

**All SAPs**: See [INDEX.md](../INDEX.md) for complete list

### System Files

**Scripts**:
- `scripts/validate-links.sh` - Link validation (from SAP-016, used in SAP audits)
- `scripts/inventory-chora-base.py` - Coherence validation

**Root Files**:
- `SKILLED_AWARENESS_PACKAGE_PROTOCOL.md` - Protocol document
- `AGENTS.md` - References SAP structure for AI agents
- `README.md` - Project overview with SAP mentions

---

**Version History**:
- **1.0.1** (2025-10-28): Wave 2 enhancements - Added "When to Use", Common Pitfalls (5 concrete scenarios), explicit 4-domain Related Content section, replaced placeholder examples with concrete SAP references
- **1.0.0** (2025-10-27): Initial awareness guide
