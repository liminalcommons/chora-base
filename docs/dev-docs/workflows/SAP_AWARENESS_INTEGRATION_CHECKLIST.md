# SAP Awareness Integration Checklist

**Workflow Type**: Quality Assurance (Supplement to SAP_AUDIT_WORKFLOW.md)
**Purpose**: Agent-executable checklist for validating AGENTS.md/CLAUDE.md hierarchy integration in SAP adoption blueprints
**Created**: 2025-10-29
**Version**: 1.0

---

## Overview

This checklist helps auditors (human or AI) systematically validate that SAP adoption blueprints include proper AGENTS.md/CLAUDE.md hierarchy updates. This ensures newly installed SAPs are **discoverable** by agents.

**Why This Matters**:
- AGENTS.md/CLAUDE.md serve as the **discoverability layer** for installed capabilities
- Without updates, agents cannot find newly installed SAPs
- Inconsistent implementation across SAPs blocks ecosystem usability

**When to Use**:
- During SAP audits (Step 4.5 of SAP_AUDIT_WORKFLOW.md)
- Before marking SAP as "Pilot" or "Active"
- When reviewing SAP adoption blueprint pull requests
- When creating new SAPs (self-validation)

**Time Required**: 10-15 minutes per SAP

---

## Prerequisites

Before using this checklist:
- [ ] Read SAP adoption blueprint completely
- [ ] Understand SAP's capability (what it does, what domains it touches)
- [ ] Have access to reference implementations (SAP-000, SAP-001)

---

## Part 1: Post-Install Section Existence

### Check 1.1: Does post-install section exist?

**Command**:
```bash
grep -i "post-install\|awareness enablement" docs/skilled-awareness/[sap]/adoption-blueprint.md
```

**Evaluation**:
- [ ] ✅ Section exists with heading (e.g., "## 6. Post-Install Tasks")
- [ ] ⚠️ Section mentioned but empty/placeholder
- [ ] ❌ No post-install section at all

**Priority**: If ❌, this is **CRITICAL** - create section in Step 5

---

### Check 1.2: Is post-install section structured?

**Look for**:
- [ ] Clear subsection for "Awareness Enablement" or similar
- [ ] Multiple tasks/steps organized (not just one line)
- [ ] References to both AGENTS.md and awareness integration

**Priority**: If missing structure, this is **HIGH** priority

---

## Part 2: Root AGENTS.md Update Instructions

### Check 2.1: Explicit AGENTS.md update step exists?

**Look for**:
- [ ] Step titled "Update AGENTS.md" or "Update Project AGENTS.md"
- [ ] OR bullet point explicitly mentioning AGENTS.md update
- [ ] Located in post-install section

**Evaluation**:
- [ ] ✅ Explicit step with clear title
- [ ] ⚠️ Mentioned but not dedicated step
- [ ] ❌ Not mentioned at all

**Priority**: If ❌, this is **CRITICAL**

---

### Check 2.2: Agent-executable instructions provided?

**Required elements**:
- [ ] Specifies tool to use (e.g., "use Edit tool", "open in editor")
- [ ] Specifies which file to open (`AGENTS.md`)
- [ ] Specifies where in file to add content (which section)
- [ ] Provides actual content template (not just "add reference")

**Good Example** (SAP-000):
```markdown
**For agents** (use Edit tool):
1. Open: `AGENTS.md`
2. Find appropriate section (e.g., "Project Structure" or "Capabilities")
3. Add:

```markdown
### Skilled Awareness Packages (SAPs)
[concrete content with actual SAP references]
```
```

**Bad Example**:
```markdown
Update AGENTS.md to reference this SAP
```

**Evaluation**:
- [ ] ✅ Agent-executable (specific tool, file, location, content)
- [ ] ⚠️ Partial (missing tool guidance or content template)
- [ ] ❌ Not agent-executable (vague instruction)

**Priority**: If ⚠️ or ❌, this is **HIGH** priority

---

### Check 2.3: Content template quality?

**Evaluate the content template provided**:

**Quality criteria**:
- [ ] Uses **concrete SAP references** (e.g., "SAP-004", "Testing Framework")
- [ ] NOT placeholder syntax (e.g., `<sap-name>`, `[capability]`)
- [ ] Includes clear section heading
- [ ] Provides context (what this SAP does)
- [ ] References detailed guide location

**Good Pattern** (concrete):
```markdown
### SAP-004: Testing Framework

**Quick Start**:
- Run tests: `pytest tests/`
- Coverage: `pytest --cov=src`

**Detailed Guide**: [tests/AGENTS.md](tests/AGENTS.md)
**Related SAPs**: SAP-005 (CI/CD), SAP-006 (Quality Gates)
```

**Bad Pattern** (hypothetical):
```markdown
### [SAP-NAME]
See docs for more info
```

**Evaluation**:
- [ ] ✅ Concrete, complete template
- [ ] ⚠️ Template exists but uses placeholders
- [ ] ❌ No template provided

**Priority**: If ⚠️, this is **HIGH**; if ❌, **CRITICAL**

---

### Check 2.4: Validation command included?

**Look for**:
- [ ] Bash command to verify update
- [ ] Uses grep or similar to check for actual content
- [ ] Includes success message

**Good Example**:
```bash
grep "SAP-004\|Testing Framework" AGENTS.md && echo "✅ AGENTS.md updated"
```

**Bad Example**:
```bash
ls AGENTS.md  # Only checks existence, not content
```

**Evaluation**:
- [ ] ✅ Validation command checks content
- [ ] ⚠️ Command exists but only checks file existence
- [ ] ❌ No validation command

**Priority**: If ❌, this is **HIGH** priority

---

## Part 3: Domain-Specific AGENTS.md (If Applicable)

### Check 3.1: Does this SAP need domain-specific AGENTS.md?

**Evaluate if SAP**:
- [ ] Creates/modifies files in `tests/` directory
- [ ] Creates/modifies files in `scripts/` directory
- [ ] Creates/modifies files in `docker/` directory
- [ ] Creates/modifies files in `.chora/memory/` directory
- [ ] Creates/modifies files in any other domain directory

**Decision**:
- If **YES** to any above: Domain-specific AGENTS.md likely needed
- If **NO** to all: Skip Part 3

---

### Check 3.2: Instructions to create domain-specific AGENTS.md?

**If domain-specific file needed, look for**:
- [ ] Instruction to copy template from `static-template/[domain]/AGENTS.md`
- [ ] OR instruction to create domain-specific file
- [ ] Destination path clearly specified
- [ ] Customization guidance provided

**Good Example** (SAP-004 Testing Framework):
```markdown
### Step 7: Create tests/AGENTS.md

Copy domain-specific testing guidance:

**For agents** (use Read + Write tools):
1. Read: `static-template/tests/AGENTS.md`
2. Write to: `tests/AGENTS.md`
3. Customize with project-specific test patterns
```

**Evaluation**:
- [ ] ✅ Domain-specific AGENTS.md instructions included
- [ ] ⚠️ Mentioned but no clear copy/create instructions
- [ ] ❌ Not mentioned (but needed based on Check 3.1)
- [ ] N/A (no domain-specific file needed)

**Priority**: If ❌, this is **MEDIUM** priority

---

## Part 4: CLAUDE.md References (If Applicable)

### Check 4.1: Should CLAUDE.md be mentioned?

**Evaluate**:
- [ ] Does capability involve Claude-specific optimizations?
- [ ] Does capability affect context loading?
- [ ] Does SAP create Claude-specific awareness content?

**Decision**:
- If **YES** to any: CLAUDE.md should be mentioned
- If **NO**: CLAUDE.md update is optional (nice-to-have)

---

### Check 4.2: CLAUDE.md update mentioned?

**Look for**:
- [ ] Explicit mention of CLAUDE.md update
- [ ] OR conditional language (e.g., "if CLAUDE.md exists, update...")
- [ ] Context loading guidance provided

**Good Example** (SAP-001):
```markdown
- **Awareness Enablement:**
  - Update root `CLAUDE.md` and `AGENTS.md` to reference inbox awareness guide.
```

**Good Example** (conditional):
```markdown
**Update CLAUDE.md** (if exists):
- Add cross-reference to new capability
- Update context loading guidance
```

**Evaluation**:
- [ ] ✅ CLAUDE.md explicitly mentioned
- [ ] ⚠️ Should mention but doesn't
- [ ] N/A (not needed for this SAP)

**Priority**: If ⚠️, this is **LOW** priority (can defer to Phase 5)

---

## Part 5: Overall Integration Quality

### Check 5.1: Integration completeness score

**Calculate score**:
- Root AGENTS.md update step: 4 points
- Agent-executable instructions: 3 points
- Concrete content template: 3 points
- Validation command: 2 points
- Domain-specific AGENTS.md (if needed): 2 points
- CLAUDE.md mention (if applicable): 1 point

**Total possible**: 15 points (or less if domain-specific/CLAUDE.md not applicable)

**Score bands**:
- **13-15 points**: ✅ **PASS** - Excellent integration
- **9-12 points**: ⚠️ **PARTIAL** - Usable but needs improvement
- **0-8 points**: ❌ **FAIL** - Critical gaps, must fix

---

### Check 5.2: Discoverability test

**Mental simulation**:

Imagine an agent (like Claude) installs this SAP following the blueprint. After installation:

- [ ] Can agent find the SAP by reading root AGENTS.md?
- [ ] Does AGENTS.md section provide clear quick reference?
- [ ] Does it link to detailed guidance (awareness-guide or domain-specific AGENTS.md)?
- [ ] Can agent validate the update was successful?

**If answer is NO to any**:
- Discoverability is compromised
- Mark as **HIGH** priority gap

---

## Part 6: Gap Documentation

### Document findings in audit report

**Template**:

```markdown
## Awareness Hierarchy Integration: [PASS/PARTIAL/FAIL]

**Score**: X/15 points

**Findings**:
- ✅ Root AGENTS.md update step exists (Step N)
- ✅ Agent-executable instructions provided
- ⚠️ Content template uses placeholders (needs concrete examples)
- ❌ No validation command included
- N/A Domain-specific AGENTS.md not needed
- N/A CLAUDE.md not applicable

**Priority Gaps**:
1. [CRITICAL] Add validation command for AGENTS.md update
2. [HIGH] Replace placeholder `<sap-name>` with concrete SAP-XXX reference
3. [MEDIUM] Consider adding CLAUDE.md update guidance

**Recommendation**:
[PASS/PARTIAL/FAIL] - [Brief recommendation]
```

---

## Reference Examples

### Excellent Example: SAP-000 (SAP Framework)

**Location**: [docs/skilled-awareness/sap-framework/adoption-blueprint.md:208-239](docs/skilled-awareness/sap-framework/adoption-blueprint.md)

**Why excellent**:
- ✅ Dedicated "Step 6: Update Project AGENTS.md"
- ✅ Explicit "For agents (use Edit tool)" guidance
- ✅ Complete content template with concrete SAP references
- ✅ Clear location guidance ("find appropriate section")
- ✅ Validation command with grep check
- ✅ Additional Step 7 for README update (bonus)

**Score**: 15/15 points

---

### Good Example: SAP-001 (Inbox Coordination)

**Location**: [docs/skilled-awareness/inbox/adoption-blueprint.md:82-85](docs/skilled-awareness/inbox/adoption-blueprint.md)

**Why good**:
- ✅ Post-install section with "Awareness Enablement" subsection
- ✅ Mentions both CLAUDE.md and AGENTS.md
- ✅ References inbox awareness guide
- ⚠️ Could benefit from more detailed instructions
- ⚠️ No validation command

**Score**: 10/15 points (PARTIAL - could be enhanced)

---

### Example to Avoid: Minimal/Vague Pattern

```markdown
## Post-Install
- Update AGENTS.md with reference to this capability
```

**Why problematic**:
- ❌ No agent-executable instructions
- ❌ No content template
- ❌ No validation command
- ❌ Vague ("reference to this capability")

**Score**: 2/15 points (FAIL)

---

## Decision Trees

### Decision 1: Is domain-specific AGENTS.md needed?

```
Does SAP create/modify files in domain directory (tests/, scripts/, docker/)?
├─ YES → Domain-specific AGENTS.md likely needed
│         ├─ Check if adoption blueprint includes copy/create instructions
│         ├─ If NO → MEDIUM priority gap
│         └─ If YES → Continue validation
└─ NO → Domain-specific AGENTS.md not needed (N/A)
```

### Decision 2: Should CLAUDE.md be mentioned?

```
Does SAP involve Claude-specific patterns or context optimization?
├─ YES → CLAUDE.md should be mentioned
│         ├─ Check if adoption blueprint mentions CLAUDE.md
│         ├─ If NO → LOW priority gap (defer to Phase 5)
│         └─ If YES → Continue validation
└─ NO → CLAUDE.md mention optional (N/A)
```

### Decision 3: What priority for missing validation command?

```
Is validation command included?
├─ YES → ✅ Good
├─ NO, but agent-executable instructions exist → HIGH priority
└─ NO, and instructions vague → CRITICAL priority
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Assuming template was followed
❌ **Don't assume**: "Template includes post-install section, so SAP probably has it"
✅ **Do**: Explicitly check each SAP, even if created after template

### Anti-Pattern 2: Accepting vague instructions
❌ **Don't accept**: "Update AGENTS.md to reference this SAP"
✅ **Do**: Require agent-executable instructions with tool, file, location, content

### Anti-Pattern 3: Skipping validation commands
❌ **Don't skip**: "Instructions are clear enough, validation not needed"
✅ **Do**: Insist on validation command that checks actual content

### Anti-Pattern 4: Ignoring domain-specific needs
❌ **Don't ignore**: "Root AGENTS.md is enough"
✅ **Do**: Check if domain-specific AGENTS.md needed based on SAP scope

### Anti-Pattern 5: Placeholder tolerance
❌ **Don't accept**: Templates with `<sap-name>`, `[capability]`, `TODO`
✅ **Do**: Require concrete examples with actual SAP-XXX references

---

## Integration with SAP Audit Workflow

This checklist is used during:

**Step 4.5** of [SAP_AUDIT_WORKFLOW.md](SAP_AUDIT_WORKFLOW.md):
- "Awareness Hierarchy Integration Check (15 minutes)"
- This checklist provides detailed validation criteria
- Reference this document when executing Step 4.5

**Step 5** (Create Critical Content):
- Use gap findings from this checklist to prioritize content creation
- Focus on CRITICAL and HIGH priority gaps

**Quality Gates**:
- SAP audit PASSING criteria includes: "Adoption blueprint includes post-install awareness enablement with validation commands"
- Use this checklist to verify that criterion

---

## Quick Reference Card

**For auditors**: Use this quick checklist during Step 4.5:

```
[ ] Post-install section exists?
[ ] Root AGENTS.md update step?
[ ] Agent-executable instructions (tool, file, location, content)?
[ ] Content template concrete (not placeholders)?
[ ] Validation command included?
[ ] Domain-specific AGENTS.md addressed (if needed)?
[ ] CLAUDE.md mentioned (if applicable)?
[ ] Score: ___/15 points
[ ] Overall: PASS / PARTIAL / FAIL
```

---

## Versioning

**Version 1.0** (2025-10-29):
- Initial checklist
- Integrated with SAP_AUDIT_WORKFLOW.md Step 4.5
- Covers root AGENTS.md, domain-specific AGENTS.md, CLAUDE.md

**Future Enhancements**:
- Add examples from more SAPs as ecosystem matures
- Create automated scoring tool (if pattern becomes stable)
- Integrate with CI/CD for SAP pull requests

---

## Related Documentation

**Workflows**:
- [SAP_AUDIT_WORKFLOW.md](SAP_AUDIT_WORKFLOW.md) - Parent workflow (Step 4.5 uses this checklist)
- [DOCUMENTATION_MIGRATION_WORKFLOW.md](DOCUMENTATION_MIGRATION_WORKFLOW.md) - Related to AGENTS.md updates

**SAP Framework**:
- [SAP-000 (SAP Framework)](../../skilled-awareness/sap-framework/) - Reference implementation
- [SAP-001 (Inbox)](../../skilled-awareness/inbox/) - Good example
- [Document Templates](../../skilled-awareness/document-templates.md) - Post-install section template

**AGENTS.md Pattern**:
- [SAP-009 (Agent Awareness)](../../skilled-awareness/agent-awareness/) - Defines AGENTS.md/CLAUDE.md patterns
- [Root AGENTS.md](/AGENTS.md) - chora-base example

---

**Checklist Version**: 1.0
**Created**: 2025-10-29
**Owner**: chora-base development team
**Status**: Active

This checklist ensures systematic validation of awareness hierarchy integration across all SAPs, maintaining discoverability and ecosystem usability.
