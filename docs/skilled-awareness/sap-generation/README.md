# SAP-029: SAP Generation Automation

**Version:** 1.0.0 | **Status:** Pilot | **Maturity:** Pilot

> Template-based SAP artifact generation—automates creation of 5-artifact SAPs using Jinja2 templates and MVP schema, reducing creation time from 10 hours to 2 hours (80% savings), with batch generation support, validation integration, and regeneration safety tracking.

---

## Quick Start (5 minutes)

```bash
# Step 1: Add SAP to catalog (sap-catalog.json)
# Manually add entry with 9 MVP fields:
# - sap_id, name, description, problem, solution
# - principles, in_scope, out_of_scope, one_sentence_summary

# Step 2: Generate 5 artifacts from templates
python scripts/generate-sap.py SAP-030
# OR using justfile:
just generate-sap SAP-030
# Creates:
#   - docs/skilled-awareness/database-migrations/capability-charter.md
#   - docs/skilled-awareness/database-migrations/protocol-spec.md
#   - docs/skilled-awareness/database-migrations/awareness-guide.md (AGENTS.md)
#   - docs/skilled-awareness/database-migrations/adoption-blueprint.md
#   - docs/skilled-awareness/database-migrations/ledger.md

# Step 3: Fill TODOs manually (2-3 hours)
# Generated artifacts contain 60-105 TODO placeholders
# Focus on high-priority files: protocol-spec → awareness-guide → capability-charter

# Step 4: Validate completed SAP
python scripts/sap-evaluator.py SAP-030
# OR using justfile:
just validate-sap SAP-030

# Optional: Batch generate multiple SAPs
python scripts/generate-sap-batch.py SAP-030 SAP-031 SAP-032
```

**First time?** → Read [adoption-blueprint.md](adoption-blueprint.md) for complete setup guide (20-min read)

---

## What Is It?

SAP-029 provides **automated SAP artifact generation** using Jinja2 templates and an MVP schema. Eliminates repetitive boilerplate (80% of SAP creation time) by generating 5 standardized artifacts from 9-field catalog entries, allowing focus on domain-specific content.

**Key Innovation**: **MVP generation schema** (9 fields)—captures essential SAP metadata in sap-catalog.json, generates 80% complete artifacts with targeted TODOs, tracks completion progress via frontmatter metadata.

### How It Works

1. **Define SAP**: Add 9-field entry to sap-catalog.json (sap_id, name, problem, solution, principles, in/out-of-scope, one-sentence summary)
2. **Generate Artifacts**: Run generator script → Jinja2 renders 5 templates → Creates artifact directory with frontmatter metadata
3. **Fill TODOs**: Manual editing fills 60-105 TODO placeholders → 2-3 hours focused work vs 10 hours from scratch
4. **Track Progress**: Frontmatter tracks `todos_remaining`, `completion_percent`, `regeneration_safe`
5. **Validate**: sap-evaluator.py checks structure, links, frontmatter consistency

---

## When to Use

Use SAP-029 when you need to:

1. **Create New SAPs** - Generate standardized 5-artifact packages from catalog entries (80% time reduction)
2. **Batch Generate SAPs** - Create multiple SAPs at once for new capability waves (e.g., React ecosystem: SAP-020 through SAP-040)
3. **Update Templates** - Regenerate artifacts with new template versions (safe if `regeneration_safe: true`)
4. **Track Incomplete SAPs** - Query `todos_remaining > 0` to find SAPs needing manual completion
5. **Ensure Consistency** - All SAPs follow identical structure via shared templates

**Not needed for**: Hand-crafted SAPs (specialized capabilities), one-off documentation (use SAP-007), or non-SAP artifacts (README files, guides)

---

## Key Features

- ✅ **80% Time Savings** - 10 hours → 2 hours (automated boilerplate + focused manual fill)
- ✅ **Jinja2 Templates** - 5 templates for 5 artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- ✅ **MVP Generation Schema** - 9 fields capture essential metadata (problem, solution, principles, scope, summary)
- ✅ **Batch Generation** - Generate multiple SAPs with single command
- ✅ **Generation Metadata** - Track `todos_remaining`, `completion_percent`, `regeneration_safe` in frontmatter
- ✅ **INDEX.md Auto-Update** - Keeps SAP catalog synchronized with generated artifacts
- ✅ **Validation Integration** - sap-evaluator.py checks structure, links, frontmatter

---

## Common Workflows

### SAP Generation Workflow

#### Step 1: Add to Catalog (5 minutes)

```bash
# Edit sap-catalog.json manually
cat >> sap-catalog.json <<'EOF'
{
  "id": "SAP-030",
  "name": "database-migrations",
  "description": "Database migration automation with version control and rollback safety",
  "tags": ["backend", "database"],
  "dependencies": ["SAP-000"],
  "metadata": {
    "problem": "Manual database migrations are error-prone and cause state drift",
    "solution": "Automated migration framework with versioning, rollback, and state tracking",
    "principles": [
      "Version control for all migrations",
      "Rollback safety (up/down migrations)",
      "State tracking and validation"
    ],
    "in_scope": ["SQL migrations", "Rollback scripts", "State validation"],
    "out_of_scope": ["ORM integration (separate SAP)", "Multi-DB support (v2.0)"],
    "one_sentence_summary": "Automated database migration framework with version control, rollback safety, and state tracking for Python projects"
  }
}
EOF
```

**9 MVP Fields** (required):
- `id`, `name`, `description` (basic metadata)
- `problem`, `solution` (capability charter content)
- `principles` (list of 3-5 guiding principles)
- `in_scope`, `out_of_scope` (scope boundaries)
- `one_sentence_summary` (elevator pitch)

---

#### Step 2: Generate Artifacts (30 seconds)

```bash
# Option 1: Generate single SAP
python scripts/generate-sap.py SAP-030

# Option 2: Using justfile
just generate-sap SAP-030

# Option 3: Batch generate multiple SAPs
python scripts/generate-sap-batch.py SAP-030 SAP-031 SAP-032

# Output:
# ✓ Created docs/skilled-awareness/database-migrations/capability-charter.md (80% complete)
# ✓ Created docs/skilled-awareness/database-migrations/protocol-spec.md (75% complete)
# ✓ Created docs/skilled-awareness/database-migrations/awareness-guide.md (85% complete)
# ✓ Created docs/skilled-awareness/database-migrations/adoption-blueprint.md (70% complete)
# ✓ Created docs/skilled-awareness/database-migrations/ledger.md (90% complete)
# ✓ Updated docs/skilled-awareness/INDEX.md
#
# TODO Count: 85 placeholders across 5 artifacts
# Estimated Manual Fill Time: 2-3 hours
```

**What Gets Generated**:
- 5 artifacts with complete frontmatter (sap_id, version, status, generation metadata)
- Boilerplate sections (headers, structure, integration tables)
- TODO placeholders for domain-specific content (60-105 TODOs)
- INDEX.md entry with correct alphabetical placement

---

#### Step 3: Fill TODOs (2-3 hours)

```bash
# Check TODO count
grep -r "TODO" docs/skilled-awareness/database-migrations/ | wc -l
# Output: 85 TODOs

# Priority order for manual fill:
# 1. protocol-spec.md (technical contracts, APIs, data models)
grep -n "TODO" docs/skilled-awareness/database-migrations/protocol-spec.md

# 2. awareness-guide.md (agent workflows, common patterns)
grep -n "TODO" docs/skilled-awareness/database-migrations/awareness-guide.md

# 3. capability-charter.md (problem statement, solution design)
grep -n "TODO" docs/skilled-awareness/database-migrations/capability-charter.md

# 4. adoption-blueprint.md (installation steps, validation)
grep -n "TODO" docs/skilled-awareness/database-migrations/adoption-blueprint.md

# 5. ledger.md (version history, adopters)
grep -n "TODO" docs/skilled-awareness/database-migrations/ledger.md

# Fill TODOs with domain-specific content:
# - Replace "TODO: Describe X" with actual descriptions
# - Add code examples, commands, workflows
# - Reference research reports for evidence (from SAP-027 research phase)
```

**Manual Fill Time**:
- **Protocol Spec**: 60-90 minutes (technical contracts, APIs)
- **Awareness Guide**: 30-45 minutes (agent workflows)
- **Capability Charter**: 30-45 minutes (problem/solution)
- **Adoption Blueprint**: 20-30 minutes (installation steps)
- **Ledger**: 5-10 minutes (version history)
- **Total**: 2-3 hours (vs 10 hours from scratch = 80% savings)

---

#### Step 4: Validate SAP (1 minute)

```bash
# Run SAP validator
python scripts/sap-evaluator.py SAP-030
# OR using justfile:
just validate-sap SAP-030

# Expected output (if complete):
# ✓ SAP-030 structure validation passed
# ✓ All 5 artifacts present
# ✓ Frontmatter valid (sap_id, version, status)
# ✓ No broken links
# ✓ Generation metadata consistent
# ✓ TODO count: 0 (100% complete)

# If TODOs remain:
# ⚠ TODO count: 12 (86% complete)
# ⚠ Incomplete sections:
#   - protocol-spec.md: Section 4 (API Reference)
#   - adoption-blueprint.md: Step 2.3 (Validation)
```

**Validation Checks**:
- Structure: 5 artifacts present with correct filenames
- Frontmatter: Valid YAML with required fields
- Links: No broken internal/external links
- Generation metadata: `generated: true`, `todos_remaining` accurate
- Completion: % complete based on TODOs filled

---

### Generation Metadata Tracking

**Frontmatter Example** (auto-generated):

```yaml
---
sap_id: SAP-030
artifact: protocol-spec
version: 1.0.0
status: draft
last_updated: 2025-11-09

# Generation Metadata (auto-populated by SAP-029)
generation:
  generated: true
  generator: "sap-generation"
  generator_version: "1.0.0"
  generated_date: "2025-11-09T14:32:15Z"
  template_version: "1.2.0"
  last_manual_edit: "2025-11-09T14:32:15Z"  # Updated on human edits
  todos_remaining: 25                        # Auto-counted
  completion_percent: 70                     # 30 / 43 TODOs filled
  regeneration_safe: false                   # true if no manual edits
---
```

**Query Examples**:

```bash
# Find SAPs with TODOs
grep -r "todos_remaining:" docs/skilled-awareness/ | grep -v ": 0"
# Output:
# docs/skilled-awareness/database-migrations/protocol-spec.md:  todos_remaining: 25

# Find SAPs safe to regenerate (no manual edits)
grep -r "regeneration_safe: true" docs/skilled-awareness/
# Output:
# docs/skilled-awareness/data-fetching/capability-charter.md:  regeneration_safe: true

# Find SAPs using old template versions
grep -r "template_version: \"1.0.0\"" docs/skilled-awareness/
# Output:
# docs/skilled-awareness/routing-navigation/protocol-spec.md:  template_version: "1.0.0"

# Calculate aggregate completion
python scripts/sap-completion-report.py
# Output:
# SAP-029 Completion Report:
# - Total SAPs: 32
# - Generated SAPs: 18 (56%)
# - Hand-Crafted SAPs: 14 (44%)
# - Average Completion: 82%
# - SAPs with TODOs: 5 (SAP-030, SAP-031, SAP-032, SAP-033, SAP-034)
```

**Use Cases**:
- **Track Progress**: Sort by `completion_percent` to prioritize low-completion SAPs
- **Safe Regeneration**: Only regenerate artifacts where `regeneration_safe: true`
- **Template Updates**: Identify artifacts using old `template_version`, regenerate with new templates
- **Sprint Planning**: Filter `todos_remaining > 0` to create backlog of SAP completion tasks

---

### Batch Generation

```bash
# Generate Wave 1: Foundation SAPs (5 SAPs)
python scripts/generate-sap-batch.py \
  SAP-030 SAP-031 SAP-032 SAP-033 SAP-034

# Output:
# Batch Generation Report:
# ✓ SAP-030 (database-migrations): 5 artifacts, 85 TODOs
# ✓ SAP-031 (routing-navigation): 5 artifacts, 92 TODOs
# ✓ SAP-032 (performance-optimization): 5 artifacts, 78 TODOs
# ✓ SAP-033 (authentication): 5 artifacts, 95 TODOs
# ✓ SAP-034 (file-upload): 5 artifacts, 88 TODOs
#
# Total: 25 artifacts, 438 TODOs
# Estimated Manual Fill Time: 10-15 hours (vs 50 hours from scratch)
# Time Savings: 80%

# Generate Wave 2: Advanced SAPs (3 SAPs)
python scripts/generate-sap-batch.py SAP-035 SAP-036 SAP-037

# Validate all generated SAPs
python scripts/sap-evaluator.py --all
```

**When to Use Batch Generation**:
- New capability waves (e.g., React ecosystem: 16 SAPs)
- Coordinated releases (all SAPs share same version)
- Template updates (regenerate multiple SAPs with new templates)
- Migration projects (porting SAPs from other frameworks)

**Time Savings**:
- **Single SAP**: 10 hours → 2 hours (80% savings)
- **Batch (5 SAPs)**: 50 hours → 10 hours (80% savings)
- **Batch (16 SAPs)**: 160 hours → 32 hours (80% savings, 128 hours saved)

---

### Regeneration Workflow

```bash
# Scenario: New template version 1.3.0 released

# Step 1: Find SAPs using old template version
grep -r "template_version: \"1.2.0\"" docs/skilled-awareness/ | cut -d: -f1 | sort -u
# Output:
# docs/skilled-awareness/database-migrations/protocol-spec.md
# docs/skilled-awareness/routing-navigation/capability-charter.md
# docs/skilled-awareness/data-fetching/awareness-guide.md

# Step 2: Check if regeneration is safe (no manual edits)
grep -B 10 "template_version: \"1.2.0\"" docs/skilled-awareness/database-migrations/protocol-spec.md | grep "regeneration_safe"
# Output:
# regeneration_safe: true  # ✅ Safe to regenerate

# Step 3: Regenerate with --force flag
python scripts/generate-sap.py SAP-030 --force --template-version 1.3.0
# OR using justfile:
just regenerate-sap SAP-030

# Step 4: Validate regenerated artifact
just validate-sap SAP-030

# ⚠️ WARNING: Regeneration OVERWRITES existing files
# Only regenerate if regeneration_safe: true
# Manual edits will be LOST if regeneration_safe: false
```

**Regeneration Use Cases**:
- Template bug fixes (typos, formatting corrections)
- Template enhancements (new sections, improved structure)
- Schema changes (new MVP fields added)
- Consistency updates (align all SAPs with latest standards)

**Safety Rules**:
- Only regenerate if `regeneration_safe: true`
- Always run validation after regeneration
- Commit regenerated artifacts separately (easy rollback)
- Review diffs before committing (verify no content loss)

---

## Integration

| SAP | Integration | How It Works |
|-----|-------------|--------------|
| **SAP-000** (SAP Framework) | Foundation | SAP-029 implements SAP-000 artifact standards (5 artifacts, frontmatter schema) |
| **SAP-027** (Dogfooding Patterns) | Research → Generate Workflow | Week 0 research generates metadata → SAP-029 generates artifacts from metadata |
| **SAP-004** (Testing Framework) | Validation Tests | sap-evaluator.py uses pytest for structure/link validation |
| **SAP-005** (CI/CD Workflows) | GitHub Actions Automation | Level 3 adoption: auto-generate SAPs on catalog updates, validate in CI/CD |
| **SAP-016** (Link Validation) | Broken Link Detection | sap-evaluator.py integrates link validation for generated artifacts |
| **SAP-007** (Documentation Framework) | Diátaxis Compliance | Generated artifacts follow Diátaxis structure (tutorial, how-to, reference, explanation) |

---

## Success Metrics

- **Time Savings**: 80% reduction (10 hours → 2 hours per SAP, 8 hours saved)
- **Batch Efficiency**: 16 SAPs generated in 32 hours (vs 160 hours manual, 128 hours saved)
- **Consistency**: 100% of generated SAPs follow identical structure
- **Completion Tracking**: Average 82% completion across generated SAPs
- **Template Updates**: 90% of SAPs use latest template version
- **Validation Pass Rate**: 95%+ of generated SAPs pass structure validation

---

## Troubleshooting

### Problem 1: SAP Not Found in Catalog

**Symptom**: `python scripts/generate-sap.py SAP-030` fails with "SAP-030 not found in sap-catalog.json"

**Common Causes**:
1. SAP not added to sap-catalog.json
2. Typo in SAP ID (SAP-30 vs SAP-030)
3. Invalid JSON syntax in catalog

**Solutions**:

```bash
# 1. Verify SAP exists in catalog
grep "SAP-030" sap-catalog.json
# If empty: Add SAP entry to catalog first

# 2. Validate JSON syntax
python -m json.tool sap-catalog.json > /dev/null
# If error: Fix JSON syntax (missing comma, bracket, quote)

# 3. Use correct SAP ID format
python scripts/generate-sap.py SAP-030  # ✅ Correct (with zero-padding)
python scripts/generate-sap.py SAP-30   # ❌ Wrong (missing zero)

# 4. Regenerate with correct ID
# Fix sap-catalog.json entry, then:
python scripts/generate-sap.py SAP-030
```

**Validation**: SAP artifacts created in `docs/skilled-awareness/database-migrations/`

---

### Problem 2: Template Syntax Error

**Symptom**: `jinja2.exceptions.TemplateSyntaxError: unexpected end of statement`

**Common Causes**:
1. Malformed Jinja2 syntax in templates
2. Missing closing tags ({% endfor %}, {% endif %})
3. Invalid variable names in templates

**Solutions**:

```bash
# 1. Validate template syntax
python -c "from jinja2 import Environment, FileSystemLoader; \
  env = Environment(loader=FileSystemLoader('templates/sap/')); \
  env.get_template('protocol-spec.md.j2').render()"
# If error: Fix template syntax at indicated line

# 2. Check for missing closing tags
grep -n "{% for" templates/sap/protocol-spec.md.j2
grep -n "{% endfor" templates/sap/protocol-spec.md.j2
# Count should match (equal number of {% for %} and {% endfor %})

# 3. Test template rendering with sample data
python scripts/test-template-rendering.py protocol-spec.md.j2
# Output: Rendered template or syntax error details

# 4. Regenerate after fixing template
python scripts/generate-sap.py SAP-030
```

**Validation**: Template renders successfully without errors

---

### Problem 3: Generation Metadata Not Updated

**Symptom**: Manual edits made but `regeneration_safe: true` (should be `false`)

**Common Causes**:
1. Frontmatter not updated after manual edits
2. Incorrect manual edit of generation metadata
3. Old template version without metadata tracking

**Solutions**:

```bash
# 1. Manually update generation metadata after edits
# Edit artifact, then update frontmatter:
cat > docs/skilled-awareness/database-migrations/protocol-spec.md <<'EOF'
---
# ... existing fields ...
generation:
  # ... existing fields ...
  last_manual_edit: "2025-11-09T16:45:00Z"  # ← Update to current time
  todos_remaining: 20                        # ← Recount TODOs
  completion_percent: 75                     # ← Recalculate
  regeneration_safe: false                   # ← Set to false after manual edits
---
EOF

# 2. Use metadata update script (automates counting)
python scripts/update-generation-metadata.py SAP-030
# Output: Updated all 5 artifacts with current metadata

# 3. Regenerate with template version 1.2.0+ (includes metadata tracking)
python scripts/generate-sap.py SAP-030 --force --template-version 1.2.0
```

**Validation**: `regeneration_safe: false` after manual edits, TODO count accurate

---

### Problem 4: Batch Generation Fails Partially

**Symptom**: `python scripts/generate-sap-batch.py SAP-030 SAP-031 SAP-032` generates SAP-030 successfully but fails on SAP-031

**Common Causes**:
1. SAP-031 missing from sap-catalog.json
2. Directory permission issues
3. Template rendering error for specific SAP

**Solutions**:

```bash
# 1. Check which SAPs failed
python scripts/generate-sap-batch.py SAP-030 SAP-031 SAP-032 2>&1 | tee batch-generation.log
# Review log for error messages

# 2. Generate failed SAPs individually (isolate errors)
python scripts/generate-sap.py SAP-031  # Test SAP-031 alone
# If error: Fix specific issue (missing catalog entry, template error)

# 3. Use --continue-on-error flag
python scripts/generate-sap-batch.py --continue-on-error SAP-030 SAP-031 SAP-032
# Generates successful SAPs, reports failures at end

# 4. Validate batch generation
python scripts/sap-evaluator.py SAP-030 SAP-031 SAP-032
```

**Validation**: All SAPs in batch generated successfully, no partial failures

---

### Problem 5: INDEX.md Not Updated After Generation

**Symptom**: SAP-030 generated successfully but not listed in `docs/skilled-awareness/INDEX.md`

**Common Causes**:
1. INDEX.md update disabled in config
2. INDEX.md file locked (permission issue)
3. Alphabetical insertion logic error

**Solutions**:

```bash
# 1. Check INDEX.md update setting
grep "update_index" .chora/config.yaml
# If false: Enable INDEX.md auto-update
sed -i 's/update_index: false/update_index: true/' .chora/config.yaml

# 2. Manually update INDEX.md
python scripts/update-sap-index.py
# Output: Added SAP-030 to INDEX.md

# 3. Verify alphabetical order
grep "^- \[SAP-" docs/skilled-awareness/INDEX.md | sort -V
# Should be in order: SAP-001, SAP-002, ..., SAP-030, ...

# 4. Regenerate with INDEX.md update
python scripts/generate-sap.py SAP-030 --update-index
```

**Validation**: SAP-030 appears in INDEX.md in correct alphabetical position

---

## Learn More

- **[protocol-spec.md](protocol-spec.md)** - SAP generation specification (30KB, 15-min read, pilot status)
- **[AGENTS.md](AGENTS.md)** - Agent generation workflows (25KB, 12-min read)
- **[CLAUDE.md](CLAUDE.md)** - Claude Code patterns (20KB, 10-min read)
- **[adoption-blueprint.md](adoption-blueprint.md)** - Complete setup guide (35KB, 18-min read)

### Templates & Scripts

- **templates/sap/*.j2** - Jinja2 templates for 5 artifacts
- **scripts/generate-sap.py** - Single SAP generator
- **scripts/generate-sap-batch.py** - Batch SAP generator
- **scripts/sap-evaluator.py** - SAP validator
- **scripts/update-generation-metadata.py** - Metadata updater

### External Resources

- [Jinja2 Documentation](https://jinja.palletsprojects.com/) - Template engine reference
- [SAP-000 Protocol Spec](../sap-framework/protocol-spec.md) - SAP framework standards
- [SAP-027 README](../dogfooding-patterns/README.md) - Research → Generate workflow

---

**Version History**:
- **1.0.0** (2025-11-02) - Initial SAP Generation with Jinja2 templates, MVP schema, batch generation, metadata tracking

---

*Part of the [Skilled Awareness Package (SAP) Framework](../sap-framework/) - See [INDEX.md](../INDEX.md) for all 32+ capabilities*
