# Agent Onboarding: Adopting chora-base

**For AI Agents**: This guide provides step-by-step instructions for adopting chora-base's Skilled Awareness Package (SAP) system in your repository.

**Target Audience**: AI agents working in repositories that want to:
- Enable cross-repo coordination via inbox protocol
- Adopt structured documentation patterns (SAPs)
- Participate in the chora ecosystem
- Implement testing, MCP, or documentation best practices

**Time Investment**: 3-5 hours (minimal entry) to 2-4 weeks (full adoption)

---

## TL;DR - Quick Start (Minimal Entry)

```bash
# 1. Clone chora-base (if not already available)
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base

# 2. Install minimal-entry set (5 SAPs, ~29k tokens, 3-5 hours)
cd /path/to/your-repo
python /tmp/chora-base/scripts/install-sap.py \
  --source /tmp/chora-base \
  --set minimal-entry

# 3. Review installed SAPs
ls docs/skilled-awareness/

# 4. Read adoption blueprints
cat docs/skilled-awareness/*/adoption-blueprint.md

# 5. Update AGENTS.md with your project details
# (Template provided by SAP-009)
```

**Result**: Your repo now has:
- ✅ SAP framework understanding (SAP-000)
- ✅ Inbox coordination protocol (SAP-001)
- ✅ Agent awareness via AGENTS.md (SAP-009)
- ✅ Link validation tooling (SAP-016)
- ✅ chora-base meta documentation (SAP-002)

**Next**: Read the blueprints, customize AGENTS.md, optionally add domain-specific SAPs

---

## What to Communicate to Another Repo's Agent

**If you're instructing another repository's AI agent to adopt chora-base**, share this:

### Quick Instruction for AI Agents

```
I'd like you to adopt chora-base's minimal-entry SAP set for ecosystem coordination.

Step 1: Clone chora-base
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base

Step 2: Install minimal-entry set (5 SAPs, ~29k tokens, 3-5 hours)
python /tmp/chora-base/scripts/install-sap.py \
  --set minimal-entry \
  --source /tmp/chora-base

Step 3: Read the awareness guides
Start with: docs/skilled-awareness/sap-framework/awareness-guide.md

Step 4: Follow adoption blueprints
Each SAP has an adoption-blueprint.md with step-by-step instructions.

Step 5: Customize AGENTS.md
Update AGENTS.md with this project's details (structure, tech stack, common tasks).

Step 6: Create capabilities file (optional, for ecosystem coordination)
inbox/CAPABILITIES/your-repo-name.yaml

This will enable:
- Cross-repo coordination via inbox protocol
- Agent awareness via AGENTS.md
- Documentation quality via link validation
- Understanding of SAP framework
- Connection to chora ecosystem

Let me know if you encounter any issues during installation.
```

### Context to Provide

1. **Purpose**: "We're adopting chora-base to enable cross-repo coordination and structured documentation."

2. **Scope**: "Start with minimal-entry (5 SAPs). We can add more capabilities later if needed."

3. **Time**: "This should take 3-5 hours of agent time to review documentation and adopt patterns."

4. **Customization**: "Customize AGENTS.md for our project. Don't just copy the template - make it specific to our repo."

5. **Validation**: "After installation, run `python scripts/validate-links.py` to check documentation integrity."

---

## What is chora-base?

**chora-base** is a structured repository template and documentation framework that provides:

1. **Skilled Awareness Packages (SAPs)**: 18 capabilities for testing, documentation, MCP, CI/CD, etc.
2. **Installation Tooling**: One-line installation of individual SAPs or curated sets
3. **Clone & Merge Model**: Receive upstream structural updates while preserving your content
4. **Cross-repo Coordination**: Inbox protocol for ecosystem collaboration

**Philosophy**: Flexible adoption - choose capabilities that fit your project, not prescriptive tiers.

---

## Installation Options

### Option 1: Minimal Entry (Recommended for New Repos)

**Use Case**: First-time adoption, ecosystem coordination, lightweight onboarding

**What You Get**:
- 5 SAPs: SAP-000, SAP-001, SAP-009, SAP-016, SAP-002
- ~29k tokens (71% reduction from full set)
- 3-5 hours estimated adoption time
- Enables inbox coordination and agent awareness

**Installation**:
```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Option 2: Recommended Set (Core Development Workflow)

**Use Case**: Active development, want testing + docs + git workflow

**What You Get**:
- 10 SAPs: All from minimal-entry, plus SAP-003, SAP-004, SAP-007, SAP-010, SAP-013
- ~58k tokens
- 1-2 weeks estimated adoption time
- Production-ready dev environment

**Installation**:
```bash
python scripts/install-sap.py --set recommended --source /path/to/chora-base
```

### Option 3: Testing-Focused Set

**Use Case**: QA contributors, test-driven development, quality focus

**What You Get**:
- 6 SAPs: SAP-000, SAP-003, SAP-004, SAP-011, SAP-012, SAP-016
- ~35k tokens
- 5-8 hours estimated adoption time

**Installation**:
```bash
python scripts/install-sap.py --set testing-focused --source /path/to/chora-base
```

### Option 4: MCP Server Development

**Use Case**: Building Model Context Protocol servers

**What You Get**:
- 10 SAPs: Core SAPs + MCP-specific patterns
- ~60k tokens
- 1-2 weeks estimated adoption time

**Installation**:
```bash
python scripts/install-sap.py --set mcp-server --source /path/to/chora-base
```

### Option 5: Full Adoption

**Use Case**: Comprehensive chora-base alignment, all capabilities

**What You Get**:
- All 18 SAPs
- ~100k tokens
- 2-4 weeks estimated adoption time

**Installation**:
```bash
python scripts/install-sap.py --set full --source /path/to/chora-base
```

---

## Step-by-Step Onboarding (Minimal Entry)

### Prerequisites
- Python 3.12+
- Git repository initialized
- Access to chora-base repository

### Step 1: Clone chora-base

```bash
# Option A: Clone to temporary location
git clone https://github.com/liminalcommons/chora-base.git /tmp/chora-base

# Option B: Clone as sibling directory (recommended for ecosystem work)
cd /path/to/your-projects
git clone https://github.com/liminalcommons/chora-base.git
```

### Step 2: Preview Installation (Dry Run)

```bash
cd /path/to/your-repo
python /tmp/chora-base/scripts/install-sap.py \
  --set minimal-entry \
  --source /tmp/chora-base \
  --dry-run
```

### Step 3: Install SAPs

```bash
# Remove --dry-run to actually install
python /tmp/chora-base/scripts/install-sap.py \
  --set minimal-entry \
  --source /tmp/chora-base
```

### Step 4: Review Installed SAPs

```bash
# List installed SAPs
ls docs/skilled-awareness/

# Read the SAP framework awareness guide (start here!)
cat docs/skilled-awareness/sap-framework/awareness-guide.md
```

**Each SAP has 5 artifacts**:
1. **capability-charter.md**: What this SAP enables
2. **protocol-spec.md**: Technical specification
3. **awareness-guide.md**: Conceptual overview (read this first!)
4. **adoption-blueprint.md**: Step-by-step adoption instructions
5. **ledger.md**: Adoption tracking and validation

### Step 5: Read Adoption Blueprints

```bash
# Read adoption blueprints in order
cat docs/skilled-awareness/sap-framework/adoption-blueprint.md
cat docs/skilled-awareness/inbox-coordination/adoption-blueprint.md
cat docs/skilled-awareness/agent-awareness/adoption-blueprint.md
cat docs/skilled-awareness/link-validation-reference-management/adoption-blueprint.md
cat docs/skilled-awareness/chora-base-meta/adoption-blueprint.md
```

### Step 6: Customize AGENTS.md

AGENTS.md template is provided by SAP-009. Customize it with your project's:
- Project overview and purpose
- Tech stack and frameworks
- Project structure
- Common tasks (testing, building, deployment)
- Development workflow
- Code standards
- Domain knowledge

### Step 7: Create Capabilities File (Optional)

**If you want to participate in cross-repo coordination**, create a capabilities file:

```bash
mkdir -p inbox/CAPABILITIES
```

**File**: `inbox/CAPABILITIES/your-repo-name.yaml`

```yaml
repo_id: "your-repo-name"
capabilities:
  - id: "your-repo.core.capability"
    name: "Your Core Capability"
    description: "What your repo provides to ecosystem"
    status: "active"
    contact: "maintainer@example.com"

tech_stack:
  languages: ["Python"]
  frameworks: ["Django"]

coordination_preferences:
  inbox_monitoring: true
  response_sla_hours: 72
```

### Step 8: Run Link Validation

```bash
# Validate all documentation links
python scripts/validate-links.py
```

### Step 9: Commit Your Adoption

```bash
git add .
git commit -m "feat: Adopt chora-base minimal-entry set (5 SAPs)

Installed SAPs:
- SAP-000: sap-framework
- SAP-001: inbox-coordination
- SAP-009: agent-awareness
- SAP-016: link-validation-reference-management
- SAP-002: chora-base-meta

Next steps:
- Customize AGENTS.md with project details
- Create inbox/CAPABILITIES/your-repo-name.yaml
- Progressively adopt additional SAPs as needed"
```

---

## Progressive Adoption Path

### After Minimal Entry

**If your project involves testing**, add:
```bash
python scripts/install-sap.py SAP-004 --source /path/to/chora-base
```

**If your project needs CI/CD**, add:
```bash
python scripts/install-sap.py SAP-003 --source /path/to/chora-base
```

**If documentation is priority**, add:
```bash
python scripts/install-sap.py SAP-007 --source /path/to/chora-base
```

### Upgrade to Recommended Set

```bash
# Install remaining SAPs from recommended set
python scripts/install-sap.py --set recommended --source /path/to/chora-base
# (Already-installed SAPs will be skipped automatically)
```

---

## Custom SAP Sets (For Organizations)

**If you want to define organization-specific sets**, create `.chorabase`:

```yaml
# your-repo/.chorabase
version: "4.1.0"
project_type: "custom"

sap_sets:
  your-org-minimal:
    name: "YourOrg Minimal Entry"
    description: "Our standard minimal set"
    saps:
      - SAP-000  # Framework
      - SAP-001  # Inbox
      - SAP-004  # Testing (required by our org)
      - SAP-009  # Agent awareness
      - SAP-016  # Link validation
    estimated_tokens: 34000
    estimated_hours: "4-6"
    use_cases:
      - "New repos in our organization"
      - "Ecosystem participation with testing focus"
```

**Installation**:
```bash
python scripts/install-sap.py --set your-org-minimal
```

---

## Troubleshooting

### Issue: "SAP not found in catalog"

**Cause**: install-sap.py can't find sap-catalog.json

**Solution**:
```bash
# Ensure --source points to chora-base root directory
python scripts/install-sap.py --set minimal-entry --source /correct/path/to/chora-base
```

### Issue: "Dependency SAP-XXX not installed"

**Cause**: Missing prerequisite SAP

**Solution**: install-sap.py handles this automatically via recursive dependency installation. If you see this error, it's a bug - please report.

### Issue: "Validation failed: Missing artifact"

**Cause**: SAP directory incomplete (should have 5 artifacts)

**Solution**:
```bash
# Re-install the SAP
python scripts/install-sap.py SAP-XXX --source /path/to/chora-base
```

### Issue: "Warning: SAP-001 is Pilot status"

**Explanation**: SAP-001 (inbox-coordination) may undergo changes before reaching Active status.

**Recommendation**:
- ✅ Still safe to adopt for ecosystem coordination
- ⚠️ Be aware that inbox protocol may evolve
- 📢 Check for updates when upgrading chora-base

---

## FAQ

### Q: Can I adopt chora-base in an existing project with established patterns?

**A**: Yes! chora-base is designed for flexible adoption. Start with minimal-entry, then:
1. Review each SAP's adoption-blueprint.md
2. Adopt patterns that align with your project
3. Skip SAPs that conflict with existing patterns
4. Use custom sets to define your project's standard

### Q: Do I need to adopt all 18 SAPs?

**A**: No. chora-base v4.0 philosophy is flexible adoption - choose capabilities that fit your project. minimal-entry (5 SAPs) is sufficient for ecosystem coordination.

### Q: How do I receive upstream updates from chora-base?

**A**: Wave 4 (Clone & Merge Model) provides tooling for this:
1. Add chora-base as git remote upstream
2. Run `python scripts/merge-upstream-structure.py`
3. Structural updates (SAP framework, scripts) merge automatically
4. Your project content (src/, tests/) remains untouched

See: `docs/user-docs/how-to/upgrade-structure-from-upstream.md`

### Q: Can I customize SAP content for my project?

**A**: Yes:
- **Awareness guides**: Read-only reference - don't customize
- **System files** (AGENTS.md, scripts/, inbox/): Customize freely
- **Your code** (src/, tests/): Implement patterns your way

SAPs provide structure and patterns, not rigid rules.

### Q: What if I only want testing patterns, not ecosystem coordination?

**A**: Use the `testing-focused` set:
```bash
python scripts/install-sap.py --set testing-focused --source /path/to/chora-base
```

This installs SAP-004 (testing) and its dependencies without SAP-001 (inbox).

### Q: How do I contribute back to chora-base?

**A**:
1. Use inbox protocol (SAP-001) to propose improvements
2. Create coordination request in your repo's `inbox/outgoing/`
3. chora-base will respond via their `inbox/incoming/`

See: `docs/skilled-awareness/inbox-coordination/awareness-guide.md`

### Q: Is chora-base only for Python projects?

**A**: Currently, most SAPs focus on Python (pytest, mypy, ruff). However:
- SAP-000, SAP-001, SAP-007, SAP-009 are language-agnostic
- You can adopt structure patterns and create language-specific SAPs
- Ecosystem coordination (inbox) works for any tech stack

---

## Additional Resources

### Documentation
- [SAP Framework Overview](../skilled-awareness/sap-framework/awareness-guide.md)
- [Inbox Coordination Protocol](../skilled-awareness/inbox-coordination/awareness-guide.md)
- [Agent Awareness Pattern](../skilled-awareness/agent-awareness/awareness-guide.md)
- [chora-base Vision Document](../../project-docs/CHORA-BASE-4.0-VISION.md)

### Installation Reference
- [Standard SAP Sets](../reference/standard-sap-sets.md) (to be created)
- [Custom SAP Sets Guide](../how-to/create-custom-sap-sets.md) (to be created)
- [install-sap.py Script Reference](../reference/install-sap-script.md) (to be created)

### Ecosystem Coordination
- [Inbox Protocol Schema](../../skilled-awareness/inbox-coordination/protocol-spec.md)
- [COORD-2025-001 Response](../../inbox/outgoing/COORD-2025-001-response-summary.md)

---

## Summary

**For AI agents adopting chora-base**:

1. **Start small**: minimal-entry set (5 SAPs, 3-5 hours)
2. **Read blueprints**: Each SAP has step-by-step adoption instructions
3. **Customize deliberately**: AGENTS.md, capabilities file, system files
4. **Validate thoroughly**: Run link validation, check ledgers
5. **Grow progressively**: Add SAPs as project needs evolve

**One-line installation**:
```bash
python /path/to/chora-base/scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

**Result**: Ecosystem-ready repository with structured documentation, cross-repo coordination, and agent discoverability.

---

**Questions?** Create a coordination request in your `inbox/outgoing/` directory following SAP-001 protocol.

**Welcome to the chora ecosystem!**
