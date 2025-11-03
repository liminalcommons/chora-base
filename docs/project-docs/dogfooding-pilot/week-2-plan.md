# Week 2: Template Creation Plan

**Dogfooding Pilot**: SAP Generation Automation
**Date**: 2025-11-02 (Planning)
**Phase**: Week 2 - Template Creation
**Estimated Time**: 3-4 hours total

---

## Overview

**Goal**: Create 5 Jinja2 templates for SAP artifact generation

**Approach**: Start with capability-charter.j2 (best understood), then proceed to other artifacts

**Success Criteria**:
- 5 working Jinja2 templates created
- Templates render without errors using SAP-028 metadata (dry run)
- Structure follows Week 1 pattern extraction findings
- MVP schema fields integrated

---

## Day-by-Day Breakdown

### Day 1 (Monday): Capability Charter Template (1.5-2 hours)

#### Morning Session (1-1.5 hours): Create capability-charter.j2

**Input**: Week 1 pattern extraction findings
- 11 core sections identified
- 6 template strategies defined
- MVP schema with 9 fields

**Tasks**:
1. **Setup template directory** (5 min)
   ```bash
   mkdir -p templates/sap
   touch templates/sap/capability-charter.j2
   ```

2. **Implement frontmatter** (10 min)
   - Use Strategy 2: Variable Substitution
   - Fields: id, full_name, version, status, owner, created_date
   ```jinja2
   # Capability Charter: {{ full_name }}

   **SAP ID**: {{ id }}
   **Version**: {{ version }}
   **Status**: {{ status }}
   **Owner**: {{ owner }}
   **Created**: {{ created_date }}
   **Last Updated**: {{ created_date }}
   ```

3. **Implement §1: Problem Statement** (15 min)
   - Use Strategy 1: Fixed Structure + Strategy 2: Variable Substitution
   ```jinja2
   ## 1. Problem Statement

   ### Current Challenge

   {{ problem_statement }}

   ### Evidence

   {% for item in evidence %}
   - {{ item }}
   {% endfor %}

   ### Business Impact

   {{ business_impact }}
   ```

4. **Implement §2: Proposed Solution** (15 min)
   - Use Strategy 5: Placeholder + Comment for free-form content
   ```jinja2
   ## 2. Proposed Solution

   ### {{ full_name }}

   {{ solution_overview }}

   ### Key Principles

   {% if key_principles %}
   {% for principle in key_principles %}
   - {{ principle }}
   {% endfor %}
   {% else %}
   <!-- TODO: List 4-8 key principles guiding this SAP -->
   - Principle 1: ...
   - Principle 2: ...
   {% endif %}
   ```

5. **Implement §3: Scope** (10 min)
   - Use Strategy 3: List Iteration
   ```jinja2
   ## 3. Scope

   ### In Scope

   {% for item in in_scope %}
   - {{ item }}
   {% endfor %}

   ### Out of Scope

   {% for item in out_of_scope %}
   - {{ item }}
   {% endfor %}
   ```

6. **Implement §4-11** (25 min)
   - §4: Outcomes - Placeholder structure
   - §5: Stakeholders - Placeholder
   - §6: Dependencies - Use Strategy 6: Dependency Linking
   - §7: Constraints - Optional section (Strategy 4)
   - §8: Risks - Optional section
   - §9: Lifecycle - Placeholder
   - §10: Related Documents - Placeholder
   - §11: Version History - Auto-generate "1.0.0 Initial release"

**Output**: `templates/sap/capability-charter.j2` (~150-200 lines)

#### Afternoon Session (30 min): Test Rendering

**Tasks**:
1. **Create test data** (10 min)
   - Extract SAP-028 metadata from sap-catalog.json
   - Add MVP generation fields manually
   - Save as `test-data/sap-028-test.json`

2. **Write minimal render script** (10 min)
   ```python
   # scripts/render-template-test.py
   import json
   from jinja2 import Template

   with open('test-data/sap-028-test.json') as f:
       data = json.load(f)

   with open('templates/sap/capability-charter.j2') as f:
       template = Template(f.read())

   output = template.render(**data)
   print(output)
   ```

3. **Test rendering** (10 min)
   ```bash
   python scripts/render-template-test.py > /tmp/test-charter.md
   # Manually review output, check for:
   # - Correct frontmatter
   # - No Jinja2 syntax errors
   # - TODO placeholders present
   # - Structure matches SAP-028 charter
   ```

**Success Criteria**:
- ✅ Template renders without errors
- ✅ Frontmatter correctly populated
- ✅ MVP fields render properly
- ✅ Placeholders present for manual content
- ✅ Structure matches Week 1 pattern extraction

---

### Day 2 (Tuesday): Protocol Spec Template (1-1.5 hours)

#### Morning Session (30 min): Analyze Protocol Pattern

**Tasks**:
1. **Read protocol-spec.md from reference SAPs** (20 min)
   - SAP-028: publishing-automation/protocol-spec.md
   - SAP-020: react-foundation/protocol-spec.md
   - Extract common structure (similar to Week 1 charter analysis)

2. **Document protocol structure** (10 min)
   - Create `week-2-protocol-structure.md` (mini-doc)
   - Identify: Sections, subsections, common patterns
   - Note: More technical, more code blocks, more examples

**Expected Structure** (hypothesis from charters):
```markdown
# Protocol Specification: {full_name}

**SAP ID**: {id}
**Version**: {version}

## 1. Overview
## 2. Core Contracts
## 3. {Domain-Specific Sections}
## 4. Integration Patterns
## 5. Error Handling (optional)
## 6. Security Considerations (optional)
## 7. Performance Requirements (optional)
## 8. Examples
## 9. Related SAPs
```

#### Afternoon Session (30-60 min): Create protocol-spec.j2

**Tasks**:
1. **Implement frontmatter** (5 min)
   - Similar to charter frontmatter
   - Simpler (no owner, created date)

2. **Implement §1: Overview** (10 min)
   - Description field + capabilities list
   ```jinja2
   ## 1. Overview

   {{ description }}

   **Key Capabilities**:
   {% for capability in capabilities %}
   - {{ capability }}
   {% endfor %}
   ```

3. **Implement §2: Core Contracts** (10 min)
   - Placeholder (free-form technical content)
   ```jinja2
   ## 2. Core Contracts

   <!-- TODO: Define main protocol contracts, interfaces, APIs -->

   {{ core_contracts | default("### Contract 1\n\n[Description]\n\n### Contract 2\n\n[Description]") }}
   ```

4. **Implement §3-9** (15-30 min)
   - Domain-specific: Large placeholder block
   - Integration patterns: Placeholder
   - Examples: Placeholder with code block structure
   - Related SAPs: Dependency linking
   ```jinja2
   ## 8. Examples

   ### Example 1: Basic Usage

   {% if examples and examples|length > 0 %}
   {% for example in examples %}
   #### {{ example.title }}

   ```{{ example.language | default("python") }}
   {{ example.code }}
   ```
   {% endfor %}
   {% else %}
   <!-- TODO: Add code examples -->
   ```python
   # Example code here
   ```
   {% endif %}
   ```

5. **Test rendering** (10 min)
   - Use SAP-028 test data
   - Verify structure

**Output**: `templates/sap/protocol-spec.j2` (~100-150 lines)

---

### Day 3 (Wednesday): Awareness Guide Template (45-60 min)

#### Full Session: Create awareness-guide.j2

**Tasks**:
1. **Analyze awareness-guide.md pattern** (15 min)
   - Read awareness-guide.md from SAP-028, SAP-020
   - Extract structure
   - Note: Heavily agent-focused, decision trees, checklists

**Expected Structure**:
```markdown
# Awareness Guide: {full_name}

**SAP ID**: {id}
**For**: AI Agents, LLM-Based Assistants

## Quick Start for AI Agents

### One-Sentence Summary
### When to Use This SAP
### When NOT to Use This SAP

## Core Concepts for Agents
## Common Agent Workflows
## Quick Reference
## Integration Points
## Edge Cases & Gotchas
```

2. **Create template** (30 min)
   - Frontmatter (5 min)
   - Quick Start section (10 min)
     - Use `one_sentence_summary` from MVP schema
     - Placeholder for when to use/not use
   - Core Concepts (5 min) - Placeholder
   - Workflows (5 min) - Placeholder with structure
   - Quick Reference (5 min) - Placeholder

3. **Test rendering** (10 min)
   - Use SAP-028 test data
   - Verify structure

**Output**: `templates/sap/awareness-guide.j2` (~100-120 lines)

---

### Day 4 (Thursday): Adoption Blueprint Template (1 hour)

#### Full Session: Create adoption-blueprint.j2

**Tasks**:
1. **Analyze adoption-blueprint.md pattern** (15 min)
   - Read adoption-blueprint.md from SAP-028
   - Note 3-level structure (always present)
   - Each level: Prerequisites → Steps → Validation → Time Estimate

**Structure** (highly consistent):
```markdown
# Adoption Blueprint: {full_name}

**SAP ID**: {id}

## Overview

### Adoption Levels
[Table comparing Level 1/2/3]

## Level 1: Basic Adoption

### Prerequisites
### Step-by-Step Instructions
### Validation
### Time Estimate

## Level 2: Advanced Adoption
[Same subsections]

## Level 3: Mastery
[Same subsections]

## Troubleshooting Guide
## Migration Paths (optional)
## Additional Resources
```

2. **Create template** (35 min)
   - Frontmatter (5 min)
   - Overview + Adoption Levels Table (10 min)
     - Hardcode table structure (always 3 levels)
   - Level 1/2/3 sections (15 min)
     - Use MVP schema if `adoption_levels` exists
     - Otherwise placeholder structure
   ```jinja2
   ## Level 1: Basic Adoption

   **Time Estimate**: {% if adoption_levels and adoption_levels.level_1 %}{{ adoption_levels.level_1.time_estimate }}{% else %}1-2 hours{% endif %}

   ### Prerequisites

   {% if adoption_levels and adoption_levels.level_1 and adoption_levels.level_1.prerequisites %}
   {% for prereq in adoption_levels.level_1.prerequisites %}
   - {{ prereq }}
   {% endfor %}
   {% else %}
   <!-- TODO: List prerequisites -->
   - Prerequisite 1
   {% endif %}
   ```
   - Troubleshooting (5 min) - Placeholder table

3. **Test rendering** (10 min)

**Output**: `templates/sap/adoption-blueprint.j2` (~150-180 lines, longest template)

---

### Day 5 (Friday): Ledger Template (30-45 min)

#### Full Session: Create ledger.j2

**Tasks**:
1. **Analyze ledger.md pattern** (10 min)
   - Already analyzed SAP-028 ledger in Week 1
   - Review structure: 12-13 sections, heavy tables
   - Note: Most content generated AFTER SAP is in use

**Structure**:
```markdown
# Traceability Ledger: {full_name}

**SAP ID**: {id}
**Current Version**: {version}
**Status**: {status}

## 1. Version History

### v{version} (YYYY-MM-DD) - Initial Release

**Status**: {status}
**Release Type**: Major (Initial SAP formalization)
**Summary**: [Initial release summary]
**Key Features**: [Capabilities list]
**Rationale**: [Why this SAP was created]
**Dependencies**: [Dependencies list]

## 2. Adoption Tracking
[Empty tables - populated later]

## 3-12. Other Sections
[Empty or placeholder - populated over time]

## 13. Appendix: SAP Metadata
[JSON snippet from catalog]
```

2. **Create template** (20 min)
   - Frontmatter (5 min)
   - §1: Version History (10 min)
     - Pre-fill initial release using catalog data
     - Use `generation.initial_release_summary` if exists
   - §2-12: Empty section headers (5 min)
     - Just headers with "No entries yet" placeholders
   - §13: Appendix with JSON metadata (5 min)
     - Serialize catalog entry as JSON

3. **Test rendering** (10 min)

**Output**: `templates/sap/ledger.j2` (~120-150 lines)

---

### Day 6 (Saturday): Integration & Testing (30-45 min)

#### Full Session: Create generator script foundation

**Tasks**:
1. **Create scripts/generate-sap.py skeleton** (20 min)
   ```python
   #!/usr/bin/env python3
   """SAP artifact generator from catalog metadata."""

   import json
   import sys
   from pathlib import Path
   from jinja2 import Environment, FileSystemLoader

   def load_catalog():
       """Load sap-catalog.json"""
       with open('sap-catalog.json') as f:
           return json.load(f)

   def get_sap_entry(catalog, sap_id):
       """Find SAP entry by ID"""
       for sap in catalog['saps']:
           if sap['id'] == sap_id:
               return sap
       raise ValueError(f"SAP {sap_id} not found in catalog")

   def render_template(template_name, data):
       """Render Jinja2 template"""
       env = Environment(loader=FileSystemLoader('templates/sap'))
       template = env.get_template(template_name)
       return template.render(**data)

   def generate_sap(sap_id):
       """Generate all 5 artifacts for a SAP"""
       catalog = load_catalog()
       sap_data = get_sap_entry(catalog, sap_id)

       # Merge generation fields into top-level for template access
       if 'generation' in sap_data:
           sap_data.update(sap_data['generation'])

       artifacts = [
           ('capability-charter.j2', 'capability-charter.md'),
           ('protocol-spec.j2', 'protocol-spec.md'),
           ('awareness-guide.j2', 'awareness-guide.md'),
           ('adoption-blueprint.j2', 'adoption-blueprint.md'),
           ('ledger.j2', 'ledger.md'),
       ]

       output_dir = Path(sap_data['location'])
       output_dir.mkdir(parents=True, exist_ok=True)

       for template_name, output_name in artifacts:
           content = render_template(template_name, sap_data)
           output_path = output_dir / output_name
           output_path.write_text(content)
           print(f"✅ Generated {output_path}")

   if __name__ == '__main__':
       if len(sys.argv) != 2:
           print("Usage: python scripts/generate-sap.py SAP-029")
           sys.exit(1)

       sap_id = sys.argv[1]
       generate_sap(sap_id)
       print(f"\n✅ All artifacts generated for {sap_id}")
   ```

2. **Test with SAP-028** (10 min)
   ```bash
   # Dry run: Generate to /tmp to avoid overwriting SAP-028
   python scripts/generate-sap.py SAP-028
   # Manually compare generated vs actual SAP-028 artifacts
   # Check for:
   # - Correct frontmatter
   # - Proper structure
   # - No Jinja2 errors
   ```

3. **Fix any template bugs found** (10 min)
   - Iterate on templates based on SAP-028 test

**Output**: `scripts/generate-sap.py` (~80-100 lines)

---

### Day 7 (Sunday): End-to-End Validation (Optional, 30 min)

#### Session: Generate Mock SAP-029

**Tasks**:
1. **Create SAP-029 mock entry in catalog** (15 min)
   - Copy SAP-028 structure
   - Change ID to SAP-029
   - Modify description, capabilities
   - Add minimal `generation` fields
   ```json
   {
     "id": "SAP-029",
     "name": "example-capability",
     "full_name": "Example Capability for Pilot",
     "version": "1.0.0",
     "status": "draft",
     "description": "Example SAP to test generation workflow",
     "capabilities": ["Capability 1", "Capability 2"],
     "dependencies": ["SAP-000"],
     "tags": ["example", "pilot"],
     "author": "chora-base",
     "location": "docs/skilled-awareness/example-capability",
     "phase": "Pilot",
     "priority": "P2",
     "generation": {
       "owner": "Victor",
       "created_date": "2025-11-10",
       "problem_statement": "Example problem statement for testing template generation.",
       "evidence": ["Evidence 1", "Evidence 2"],
       "business_impact": "Example business impact description.",
       "solution_overview": "Example solution overview for testing.",
       "key_principles": ["Principle 1", "Principle 2"],
       "in_scope": ["Feature 1", "Feature 2"],
       "out_of_scope": ["Feature 3", "Feature 4"],
       "one_sentence_summary": "SAP-029 defines an example capability for pilot testing."
     }
   }
   ```

2. **Generate SAP-029** (5 min)
   ```bash
   python scripts/generate-sap.py SAP-029
   # Check output in docs/skilled-awareness/example-capability/
   ```

3. **Review generated artifacts** (10 min)
   - Open all 5 artifacts
   - Check for:
     - ✅ Correct frontmatter
     - ✅ MVP fields populated
     - ✅ TODO placeholders present
     - ✅ Structure matches reference SAPs
     - ✅ No Jinja2 syntax visible (all rendered)
   - Note any issues for iteration

**Output**:
- SAP-029 mock entry in catalog
- 5 generated artifacts (example-capability/)

---

## Week 2 Deliverables Checklist

### Templates Created
- [ ] `templates/sap/capability-charter.j2` (~150-200 lines)
- [ ] `templates/sap/protocol-spec.j2` (~100-150 lines)
- [ ] `templates/sap/awareness-guide.j2` (~100-120 lines)
- [ ] `templates/sap/adoption-blueprint.j2` (~150-180 lines)
- [ ] `templates/sap/ledger.j2` (~120-150 lines)

**Total Template Lines**: ~620-800 lines

### Scripts Created
- [ ] `scripts/generate-sap.py` (~80-100 lines)
- [ ] `scripts/render-template-test.py` (optional, ~20 lines)

### Test Data Created
- [ ] `test-data/sap-028-test.json` (SAP-028 with generation fields)
- [ ] SAP-029 mock entry in sap-catalog.json

### Documentation Created
- [ ] `week-2-protocol-structure.md` (mini-doc, optional)
- [ ] This plan document

---

## Success Criteria for Week 2

### Template Quality
- ✅ All 5 templates render without Jinja2 errors
- ✅ Frontmatter correctly populated from catalog
- ✅ MVP fields (9 fields) integrated and rendering
- ✅ Structure matches Week 1 pattern extraction
- ✅ Placeholders present for manual content (TODO comments)

### Generator Functionality
- ✅ generate-sap.py accepts SAP ID as argument
- ✅ Reads sap-catalog.json correctly
- ✅ Renders all 5 templates
- ✅ Writes files to correct location
- ✅ Handles missing `generation` fields gracefully (defaults)

### Testing Results
- ✅ SAP-028 re-generation matches structure of actual SAP-028
- ✅ SAP-029 mock generation produces valid artifacts
- ✅ No file corruption or encoding issues
- ✅ Generated markdown passes basic validation (no syntax errors)

### Time Target
- ✅ Total time: 3-4 hours (within budget)
- ✅ No single day exceeds 2 hours

---

## Risk Mitigation

### Risk 1: Templates Too Complex
**Symptom**: Taking >2 hours per template
**Mitigation**:
- Simplify: Use more placeholders, less pre-fill
- Focus on structure automation (80/20 rule)
- Defer complex sections to manual fill

### Risk 2: Jinja2 Syntax Errors
**Symptom**: Templates fail to render
**Mitigation**:
- Test each section incrementally (don't write entire template at once)
- Use simple variable substitution first, add logic later
- Keep test data ready for immediate feedback

### Risk 3: Catalog Schema Mismatch
**Symptom**: Generator can't find expected fields
**Mitigation**:
- Use Jinja2 defaults: `{{ field | default("fallback") }}`
- Make all `generation` fields optional
- Provide clear error messages when required fields missing

### Risk 4: Generated Output Quality Issues
**Symptom**: Generated artifacts don't match reference SAPs
**Mitigation**:
- Compare generated SAP-028 against actual SAP-028
- Iterate on templates based on comparison
- Accept imperfection (80% automation is success)

---

## Dependencies & Prerequisites

### Tools Required
- Python 3.9+ (for Jinja2 support)
- Jinja2 library (`pip install jinja2`)
- sap-catalog.json (v4.8.0+)
- Week 1 pattern extraction findings

### Files Needed
- `templates/sap/` directory (created Day 1)
- `scripts/` directory (exists)
- `test-data/` directory (created Day 1)

### Knowledge Prerequisites
- Jinja2 template syntax (basic: variables, loops, conditionals)
- SAP structure from Week 1 analysis
- sap-catalog.json schema

---

## Next Steps After Week 2

### If Week 2 Succeeds
**Week 3**: Generator Implementation
- Add justfile integration (`just generate-sap`)
- Add INDEX.md auto-update
- Add validation integration
- Error handling improvements
- Dry-run mode

### If Week 2 Partially Succeeds
**Iterate**:
- Complete remaining templates
- Fix Jinja2 errors
- Adjust MVP schema if needed
- Continue to Week 3 with working templates

### If Week 2 Fails
**Pivot**:
- Reduce scope to 1-2 artifacts (charter + protocol only)
- Simplify schema (fewer fields)
- Consider manual template fill instead of generation
- Re-evaluate pilot goals

---

## Time Budget Summary

| Day | Activity | Estimated Time | Cumulative |
|-----|----------|---------------|------------|
| 1 AM | Create capability-charter.j2 | 1-1.5h | 1-1.5h |
| 1 PM | Test rendering | 0.5h | 1.5-2h |
| 2 AM | Analyze protocol pattern | 0.5h | 2-2.5h |
| 2 PM | Create protocol-spec.j2 | 0.5-1h | 2.5-3.5h |
| 3 | Create awareness-guide.j2 | 0.75-1h | 3.25-4.5h |
| 4 | Create adoption-blueprint.j2 | 1h | 4.25-5.5h |
| 5 | Create ledger.j2 | 0.5-0.75h | 4.75-6.25h |
| 6 | Generator script + testing | 0.5-0.75h | 5.25-7h |
| 7 | End-to-end validation (optional) | 0.5h | 5.75-7.5h |

**Target**: 3-4 hours (core activities: Day 1-5)
**With optional activities**: 5.75-7.5 hours
**Buffer**: 1-2 hours for debugging/iteration

**Recommendation**: Focus on Day 1-5 (3.5-5 hours), skip Day 6-7 if time-constrained

---

## Appendix A: Template Complexity Estimates

| Template | Lines | Complexity | Effort | Priority |
|----------|-------|------------|--------|----------|
| capability-charter.j2 | 150-200 | Medium | 1.5h | P0 (Critical) |
| protocol-spec.j2 | 100-150 | Low-Medium | 1h | P0 (Critical) |
| awareness-guide.j2 | 100-120 | Low | 0.75h | P1 (High) |
| adoption-blueprint.j2 | 150-180 | Medium | 1h | P1 (High) |
| ledger.j2 | 120-150 | Low | 0.5h | P2 (Medium) |

**Rationale**:
- Charter is highest effort (most sections, most variation)
- Protocol is moderate (technical but fewer sections)
- Awareness is simple (predictable structure)
- Adoption is moderate-high (3-level repetition, but predictable)
- Ledger is low (mostly empty placeholders for initial release)

---

## Appendix B: Jinja2 Quick Reference

### Variable Substitution
```jinja2
{{ variable_name }}
{{ variable_name | default("fallback value") }}
```

### List Iteration
```jinja2
{% for item in list_variable %}
- {{ item }}
{% endfor %}
```

### Conditional Sections
```jinja2
{% if variable %}
Content when variable exists
{% else %}
Fallback content
{% endif %}
```

### Nested Data Access
```jinja2
{{ generation.problem_statement }}
{{ adoption_levels.level_1.time_estimate }}
```

### Loop Metadata
```jinja2
{% for item in list %}
{{ loop.index }}. {{ item }}  <!-- 1-indexed -->
{{ loop.index0 }}. {{ item }}  <!-- 0-indexed -->
{% endfor %}
```

---

**Week 2 Status**: ⏳ **READY TO START**
**Prerequisites**: ✅ Week 1 complete
**Next Action**: Day 1 AM - Create capability-charter.j2 template
