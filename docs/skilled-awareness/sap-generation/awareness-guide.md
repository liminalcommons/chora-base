# Awareness Guide: SAP Generation Automation

**SAP ID**: SAP-029
**Version**: 1.0.0
**For**: AI Agents, LLM-Based Assistants
**Last Updated**: 2025-11-02

---

## Quick Start for AI Agents

### One-Sentence Summary

SAP-029 defines template-based SAP artifact generation to reduce creation time from 10 hours to 2 hours (80% savings) through Jinja2 templates, INDEX.md auto-update, and validation integration.

### When to Use This SAP

Use SAP-029 when:
- ✅ Creating new SAPs for chora-base (or projects adopting chora-base patterns)
- ✅ Need to save 80-90% time on SAP structure generation (10 hours → 5 minutes)
- ✅ Want consistent SAP structure across multiple capabilities
- ✅ Generating 2+ SAPs (ROI positive after 1st SAP, break-even on setup investment)
- ✅ Have access to sap-catalog.json and can define 9 MVP generation fields
- ✅ Need automatic INDEX.md updates and validation integration

Don't use SAP-029 for:
- ❌ One-off documentation not following SAP format
- ❌ Non-chora projects without SAP framework structure
- ❌ Fully custom documentation requiring unique structure (templates are opinionated)
- ❌ Real-time collaborative editing (file-based generation, not collaborative docs)
- ❌ Projects requiring <50% TODO manual fill (80/20 rule: 20% manual work remains)

---

## 1. Core Concepts for Agents

<!-- TODO: Provide decision trees, key concepts, mental models for AI agents

This section helps agents quickly understand:
- Key decisions they need to make
- Common patterns and anti-patterns
- Mental models for this capability
-->

### Key Concepts

**Concept 1**: Template-Based Generation
- **Description**: SAP-029 uses Jinja2 templates to generate markdown artifacts. Each SAP artifact (capability-charter, protocol-spec, etc.) has a corresponding template with placeholder variables that get filled from sap-catalog.json and user input.
- **When to use**: When creating new SAPs that follow the standard SAP-000 structure. Saves 80-90% of manual writing time.
- **Example**: Template `capability-charter.j2` contains `{{ problem }}` placeholder. Generator reads `problem: "Manual SAP creation takes 10 hours"` from catalog and outputs rendered markdown.

**Concept 2**: MVP Schema (9 Fields)
- **Description**: Minimum viable SAP requires 9 metadata fields: sap_id, name, description, problem, solution, principles, in_scope, out_of_scope, one_sentence_summary. These fields populate 80% of generated content, leaving 20% manual TODOs.
- **When to use**: Level 1 (Basic) adoption. Sufficient for first SAP generation, understanding the system, ad-hoc generation.
- **Example**: SAP-030 entry in catalog provides 9 MVP fields → generates 5 artifacts with 60-80 TODOs remaining for manual refinement.

**Concept 3**: Progressive Adoption (3 Levels)
- **Description**: SAP-029 supports 3 adoption levels with increasing automation: Level 1 (Basic, 50-60% automation), Level 2 (Advanced, 70-80%), Level 3 (Mastery, 90-95%). Higher levels require more setup but reduce per-SAP TODO count.
- **When to use**: Choose level based on SAP count: Level 1 for 1-4 SAPs, Level 2 for 5-10 SAPs, Level 3 for 20+ SAPs (production ecosystems).
- **Example**: Level 1 setup takes 10-11h, generates SAPs with 60-105 TODOs. Level 3 setup takes 25-31h but enforces <10 TODOs per SAP via quality gates.

**Concept 4**: Quality Gates & TODO Thresholds
- **Description**: Level 3 enforces TODO threshold (<10 per SAP) before allowing production deployment. Prevents under-filled SAPs from entering ecosystem.
- **When to use**: Production SAP ecosystems requiring consistency. CI/CD integration blocks merges if TODO count exceeds threshold.
- **Example**: `python scripts/quality-gate-sap.py SAP-030 10` fails with exit code 1 if SAP-030 has >10 TODOs, preventing premature publication.

### Decision Tree

```
User request: "Create new SAP" or "Generate SAP documentation"
   │
   ├─ Is this a chora-base project with SAP-000 installed?
   │   ├─ NO → Don't use SAP-029 (requires SAP framework structure)
   │   │        Recommend: Manual documentation or different template tool
   │   │
   │   └─ YES → Continue to next check
   │
   ├─ Is SAP metadata available in sap-catalog.json?
   │   ├─ NO → Ask user to add SAP entry first
   │   │        Action: "Please add SAP-030 entry to sap-catalog.json with MVP fields"
   │   │
   │   └─ YES → Continue to next check
   │
   ├─ How many SAPs will be generated?
   │   ├─ 1-4 SAPs → Recommend Level 1 (Basic)
   │   │              Setup: 10-11h, Per-SAP: 2-4h manual work (60-105 TODOs)
   │   │              Action: python scripts/generate-sap.py {sap_id}
   │   │
   │   ├─ 5-10 SAPs → Recommend Level 2 (Advanced)
   │   │               Setup: 12-15h, Per-SAP: 1-2h manual work (40-80 TODOs)
   │   │               Action: Setup batch generation + extended schema
   │   │
   │   └─ 20+ SAPs → Recommend Level 3 (Mastery)
   │                  Setup: 25-31h, Per-SAP: <30min manual work (<10 TODOs enforced)
   │                  Action: Setup CI/CD pipeline + quality gates
   │
   └─ Does project require custom artifact structure?
       ├─ YES (non-standard) → Don't use SAP-029 (opinionated templates)
       │                        Recommend: Custom templates or manual creation
       │
       └─ NO (follows SAP-000) → ✅ Use SAP-029
                                  Break-even: After 1st SAP (ROI positive)
```

---

## 2. Common Agent Workflows

<!-- TODO: Define step-by-step workflows for common agent tasks

Each workflow should include:
- User request (trigger)
- Agent actions (numbered steps)
- Validation (how to verify)
- Common variations
-->

### Workflow 1: Generate First SAP (Level 1 Basic)

**User Request**: "Create a new SAP for database migrations" or "Generate SAP-030 documentation"

**Agent Actions**:
1. Verify SAP entry exists in catalog:
   ```bash
   grep -A 10 '"id": "SAP-030"' sap-catalog.json
   ```
2. Check prerequisites installed:
   ```bash
   python --version  # Should be 3.8+
   python -c "import jinja2; print(jinja2.__version__)"  # Should succeed
   ls templates/sap/*.j2  # Should show 5 template files
   ```
3. Generate SAP artifacts:
   ```bash
   python scripts/generate-sap.py SAP-030
   ```

**Validation**:
```bash
# Verify 5 artifacts were created
ls docs/skilled-awareness/database-migrations/

# Check TODO count (should be 60-105 for Level 1)
grep -r "TODO" docs/skilled-awareness/database-migrations/ | wc -l

# Run quick validation
python scripts/sap-evaluator.py --quick SAP-030
```

**Expected Output**:
```
✅ Generated 5 artifacts for SAP-030 (database-migrations):
   - capability-charter.md (12 TODOs)
   - protocol-spec.md (25 TODOs)
   - awareness-guide.md (18 TODOs)
   - adoption-blueprint.md (22 TODOs)
   - ledger.md (8 TODOs)

Total TODOs: 85 (within Level 1 range: 60-105)
Generation time: 4.2 seconds

Next steps:
1. Review generated files
2. Fill TODOs manually (estimated 2-4 hours)
3. Run full validation: python scripts/sap-evaluator.py --deep SAP-030
```

**Common Variations**:
- **Variation 1**: If SAP not in catalog, instruct user: "Please add SAP-030 entry to sap-catalog.json with MVP fields first"
- **Variation 2**: If templates missing, instruct: "Install templates: git clone templates/sap/ or copy from chora-base reference"
- **Variation 3**: If generation fails with encoding error (Windows), set environment: `$env:PYTHONIOENCODING="utf-8"` then retry

### Workflow 2: Batch Generate Multiple SAPs (Level 2 Advanced)

**User Request**: "Generate SAP-030, SAP-031, and SAP-032 in one command" or "Bulk create SAPs for React ecosystem"

**Agent Actions**:
1. Verify all SAPs exist in catalog:
   ```bash
   for id in SAP-030 SAP-031 SAP-032; do
     grep -q "\"id\": \"$id\"" sap-catalog.json && echo "✅ $id" || echo "❌ $id missing"
   done
   ```
2. Create batch generation script (Level 2 feature):
   ```bash
   python scripts/generate-sap-batch.py SAP-030 SAP-031 SAP-032
   ```
3. Monitor generation progress:
   ```bash
   tail -f .chora/logs/sap-generation.log
   ```

**Validation**:
```bash
# Verify all SAPs generated
for id in SAP-030 SAP-031 SAP-032; do
  name=$(grep -A 1 "\"id\": \"$id\"" sap-catalog.json | grep '"name"' | cut -d'"' -f4)
  ls docs/skilled-awareness/$name/*.md | wc -l  # Should be 5
done

# Check aggregate TODO count (should be 40-80 per SAP for Level 2)
grep -r "TODO" docs/skilled-awareness/{database-migrations,routing-navigation,data-fetching}/ | wc -l

# Run validation on all
python scripts/sap-evaluator.py --quick SAP-030 SAP-031 SAP-032
```

### Workflow 3: Troubleshoot Generation Errors

**User Request**: "SAP generation failed with error" or "Generated files are incomplete"

**Agent Actions**:
1. Check error code from generation output:
   ```bash
   python scripts/generate-sap.py SAP-030 2>&1 | tee generation-error.log
   ```
2. Diagnose based on error code:
   ```bash
   # SAP-029-001: SAP Not Found
   grep -q '"id": "SAP-030"' sap-catalog.json || echo "Missing catalog entry"

   # SAP-029-002: Template Not Found
   ls templates/sap/*.j2 | grep -E "(capability-charter|protocol-spec|awareness-guide|adoption-blueprint|ledger).j2"

   # SAP-029-003: Template Syntax Error
   python -m jinja2 templates/sap/capability-charter.j2 --format=json -D sap_id=TEST

   # SAP-029-007: Unicode Encoding Error (Windows)
   python -c "import sys; print(sys.getdefaultencoding())"
   ```
3. Apply fix based on diagnosis:
   ```bash
   # Fix missing catalog: Add SAP entry
   # Fix missing templates: Copy from reference repo
   # Fix template syntax: Validate Jinja2 syntax
   # Fix encoding: export PYTHONIOENCODING=utf-8
   ```

**Validation**:
```bash
# Retry generation after fix
python scripts/generate-sap.py SAP-030

# Verify no errors in output
echo $?  # Should be 0

# Check generated files exist
ls -lh docs/skilled-awareness/*/capability-charter.md
```

---

## 3. Quick Reference for Agents

<!-- TODO: Provide cheat sheet for agents

Include:
- Key commands
- File paths
- Configuration snippets
- Common patterns
-->

### Key Commands

```bash
# Generate single SAP (Level 1 Basic)
python scripts/generate-sap.py SAP-030

# Batch generate multiple SAPs (Level 2 Advanced)
python scripts/generate-sap-batch.py SAP-030 SAP-031 SAP-032

# Validate generated SAP
python scripts/sap-evaluator.py --quick SAP-030       # Quick validation
python scripts/sap-evaluator.py --deep SAP-030        # Deep validation

# Check TODO count
grep -r "TODO" docs/skilled-awareness/database-migrations/ | wc -l

# Quality gate enforcement (Level 3)
python scripts/quality-gate-sap.py SAP-030 10         # Fail if >10 TODOs

# Update INDEX.md after generation
python scripts/update-sap-index.py

# Check SAP exists in catalog
grep -A 10 '"id": "SAP-030"' sap-catalog.json

# List all SAPs in catalog
jq -r '.saps[] | "\(.id) - \(.name) (\(.status))"' sap-catalog.json
```

### Important File Paths

| File | Purpose | Agent Action |
|------|---------|--------------|
| `sap-catalog.json` | SAP metadata registry (source of truth) | Read SAP entries before generation, validate MVP fields present |
| `templates/sap/*.j2` | Jinja2 templates for 5 SAP artifacts | Verify existence before generation, customize for Level 2+ |
| `scripts/generate-sap.py` | Single SAP generation script (Level 1) | Execute with SAP ID argument, check exit code |
| `scripts/generate-sap-batch.py` | Batch generation script (Level 2) | Execute with multiple SAP IDs, monitor logs |
| `scripts/quality-gate-sap.py` | TODO threshold enforcer (Level 3) | Run in CI/CD, fail build if threshold exceeded |
| `scripts/sap-evaluator.py` | SAP validation tool (from SAP-019) | Run after generation to check completeness |
| `docs/skilled-awareness/INDEX.md` | SAP capability index | Update after generation with new SAP entry |
| `.github/workflows/generate-sap.yml` | CI/CD workflow for SAP generation (Level 3) | Configure for automated generation on catalog updates |
| `.chora/logs/sap-generation.log` | Generation logs for debugging | Check on errors, monitor batch progress |

### Configuration Snippets

**Configuration 1**: Level 1 Basic Setup
```yaml
# .chora/config.yaml (if using chora configuration)
sap-generation:
  enabled: true
  level: 1  # Basic: Manual generation

  templates:
    path: templates/sap/
    version: "1.0.0"
    cache_enabled: false

  schema:
    mvp_fields:  # 9 required fields for Level 1
      - sap_id
      - name
      - description
      - problem
      - solution
      - principles
      - in_scope
      - out_of_scope
      - one_sentence_summary

  validation:
    auto_validate: false  # Manual validation in Level 1
```

**Configuration 2**: Level 3 Production Setup
```yaml
# .chora/config.yaml
sap-generation:
  enabled: true
  level: 3  # Mastery: Automated pipeline

  templates:
    path: templates/sap/
    version: "1.2.0"
    cache_enabled: true  # Performance optimization

  schema:
    mvp_fields: [...]  # Same as Level 1
    extended_fields:  # Level 3 additions
      - design_principles
      - api_contracts
      - integration_patterns

  validation:
    auto_validate: true  # Validate on generation
    todo_threshold: 10  # Enforce <10 TODOs
    quality_gate_enabled: true

  ci_cd:
    trigger_on_catalog_update: true
    parallel_generation: true
    notification_webhook: "https://example.com/notify"
```

### Common Patterns

**Pattern 1**: Template Variable Access in Jinja2
```python
# In Python generation script
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates/sap/'))
template = env.get_template('capability-charter.j2')

# Render with catalog data
output = template.render(
    sap_id="SAP-030",
    name="database-migrations",
    problem="Manual schema changes cause inconsistency",
    solution="Automated migration framework with rollback",
    # ... other MVP fields
)
```

**Pattern 2**: Batch Generation with Error Handling
```python
# scripts/generate-sap-batch.py pattern
sap_ids = ["SAP-030", "SAP-031", "SAP-032"]
results = []

for sap_id in sap_ids:
    try:
        generate_sap(sap_id)
        results.append({"sap_id": sap_id, "status": "success"})
    except SAPNotFoundError as e:
        results.append({"sap_id": sap_id, "status": "failed", "error": str(e)})
        continue  # Continue with next SAP

# Report results
success_count = sum(1 for r in results if r["status"] == "success")
print(f"Generated {success_count}/{len(sap_ids)} SAPs successfully")
```

**Pattern 3**: Quality Gate Integration (Level 3)
```python
# In CI/CD workflow or pre-commit hook
def enforce_quality_gate(sap_id, threshold=10):
    todo_count = count_todos(sap_id)
    if todo_count > threshold:
        raise QualityGateError(
            f"SAP {sap_id} has {todo_count} TODOs (threshold: {threshold})"
        )
    return True

# Usage in GitHub Actions
if __name__ == "__main__":
    enforce_quality_gate("SAP-030", threshold=10)
    # Exits with code 1 if quality gate fails
```

---

## 4. Integration with Other SAPs

<!-- TODO: Describe how this SAP works with other SAPs

Help agents understand:
- Which SAPs to use together
- Integration points
- Workflow combinations
-->


### Required Dependencies

#### SAP-000 (SAP Framework)

**Relationship**: SAP-029 requires SAP-000 because it generates artifacts following the SAP-000 5-artifact structure (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger).

**Agent Workflow**:
1. When user requests SAP generation, first check if SAP-000 is installed:
   ```bash
   ls docs/skilled-awareness/sap-framework/protocol-spec.md
   ```
2. If not found, recommend: "SAP-029 requires SAP-000 (SAP Framework). Please install SAP-000 first to establish the 5-artifact structure."
3. If SAP-000 installed, verify artifact structure is documented:
   ```bash
   grep -q "capability-charter" docs/skilled-awareness/sap-framework/protocol-spec.md
   ```
4. Proceed with generation only after SAP-000 verification




### Complementary SAPs

**SAP-019 (Self-Evaluation)**
- **Use together when**: Validating generated SAPs for completeness and quality
- **Benefit**: SAP-029 generates artifacts with TODO markers; SAP-019 evaluates completion status, TODO count, and link validity. Use `python scripts/sap-evaluator.py --deep SAP-030` after generation.

**SAP-005 (CI/CD Workflows)**
- **Use together when**: Adopting Level 3 (Mastery) with automated SAP generation pipelines
- **Benefit**: SAP-029 defines generation commands; SAP-005 provides GitHub Actions integration patterns. Combine to trigger generation on sap-catalog.json updates, enforce quality gates, and auto-commit generated artifacts.

**SAP-016 (Link Validation)**
- **Use together when**: Ensuring generated SAP artifacts maintain valid internal/external links
- **Benefit**: SAP-029 generates artifacts with placeholder links; SAP-016 validates link integrity. Run `bash scripts/validate-awareness-links.sh` after generation to catch broken references.

**SAP-027 (Dogfooding Patterns)**
- **Use together when**: Validating SAP-029 itself through internal use before recommending to ecosystem
- **Benefit**: SAP-027 provides 6-week pilot methodology with GO/NO-GO criteria. Use to measure SAP-029's time savings, satisfaction, and adoption metrics. Example: SAP-029 pilot achieved 120x time savings (vs 5x target), leading to GO decision.

**SAP-001 (Inbox)**
- **Use together when**: Coordinating multi-SAP generation across teams or projects
- **Benefit**: SAP-001 provides coordination request tracking; SAP-029 fulfills SAP creation requests. Use inbox to track "Generate SAP-030" requests, decompose into tasks, log completion.

---

## 5. Error Patterns & Troubleshooting

<!-- TODO: Common errors agents encounter and how to fix them

Help agents:
- Recognize error patterns
- Provide solutions
- Avoid common mistakes
-->

### Error Pattern 1: SAP Not Found in Catalog (SAP-029-001)

**Symptoms**:
- Error message: `KeyError: 'SAP-030' not found in sap-catalog.json`
- Generation script exits with code 1
- No artifacts created in docs/skilled-awareness/

**Cause**: SAP ID specified in generation command doesn't have a corresponding entry in sap-catalog.json. This happens when user tries to generate a SAP before adding its metadata to the catalog.

**Agent Solution**:
1. Verify SAP is missing from catalog:
   ```bash
   grep -q '"id": "SAP-030"' sap-catalog.json || echo "SAP-030 not found"
   ```
2. Instruct user to add SAP entry with MVP fields:
   ```json
   {
     "id": "SAP-030",
     "name": "database-migrations",
     "description": "Automated database schema migration framework",
     "problem": "Manual schema changes cause inconsistency",
     "solution": "Version-controlled migrations with rollback",
     "principles": ["Idempotency", "Rollback safety", "State tracking"],
     "in_scope": ["SQL migrations", "Schema versioning", "Rollback"],
     "out_of_scope": ["Data seeding", "ORM integration"],
     "one_sentence_summary": "Automated database migration framework with rollback support"
   }
   ```
3. Verify catalog entry added:
   ```bash
   jq '.saps[] | select(.id == "SAP-030")' sap-catalog.json
   ```
4. Retry generation:
   ```bash
   python scripts/generate-sap.py SAP-030
   ```

**Prevention**: Always add SAP to sap-catalog.json BEFORE running generation script. Use catalog as source of truth for SAP metadata.

### Error Pattern 2: Template Syntax Error (SAP-029-003)

**Symptoms**:
- Error message: `jinja2.exceptions.TemplateSyntaxError: unexpected '}'`
- Generation script crashes mid-render
- Partial artifacts created (some files written, others missing)
- Stack trace pointing to templates/sap/*.j2 files

**Cause**: Jinja2 template contains invalid syntax (unclosed tags, mismatched braces, invalid variable names). This happens when templates are manually edited and syntax errors are introduced.

**Agent Solution**:
1. Identify problematic template from error message:
   ```bash
   # Error message shows: "Error in capability-charter.j2, line 42"
   cat -n templates/sap/capability-charter.j2 | sed -n '35,50p'  # Show context
   ```
2. Validate template syntax:
   ```bash
   python -m jinja2 templates/sap/capability-charter.j2 --format=json -D sap_id=TEST
   # Should fail with same error, confirming template issue
   ```
3. Common fixes:
   - Unclosed tag: `{% if condition %}` missing `{% endif %}`
   - Mismatched braces: `{{ variable }` missing closing `}`
   - Invalid variable: `{{ sap-id }}` should be `{{ sap_id }}` (underscores, not hyphens)
4. Fix template syntax and verify:
   ```bash
   python -m jinja2 templates/sap/capability-charter.j2 --format=json -D sap_id=TEST -D name=test
   # Should render without errors
   ```
5. Retry generation:
   ```bash
   python scripts/generate-sap.py SAP-030
   ```

**Prevention**:
- Use syntax-aware editor (VSCode with Jinja2 extension) when editing templates
- Run `python -m jinja2 <template>` to validate before committing template changes
- Use template versioning to roll back breaking changes

---

## 6. Agent Communication Patterns

<!-- TODO: How agents should communicate about this SAP to users

Guide agents on:
- How to explain concepts
- What details to include
- Common user questions
-->

### Explaining SAP Generation Automation to Users

**Simple Explanation** (for beginners):
> SAP-029 is a template system that automatically creates documentation for new capabilities. Instead of writing 5 files from scratch (10 hours), you provide 9 pieces of information and get 80% of the documentation generated in 5 minutes. You then fill in the remaining 20% manually.

**Technical Explanation** (for experienced users):
> SAP-029 uses Jinja2 templates to generate the 5 SAP artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger) from sap-catalog.json metadata. Level 1 (Basic) provides 50-60% automation with 60-105 TODOs per SAP; Level 3 (Mastery) achieves 90-95% automation with <10 TODOs enforced via CI/CD quality gates.

### Common User Questions

**Q: How long does it take to generate a SAP?**

**Agent Response**:
Generation itself takes 5 minutes. However, total time depends on adoption level:
- Level 1 (Basic): 5min generation + 2-4h manual TODO completion = ~3h total per SAP
- Level 2 (Advanced): 5min generation + 1-2h manual TODO completion = ~1.5h total per SAP
- Level 3 (Mastery): 30sec generation + <30min manual TODO completion = ~30min total per SAP

Initial setup time: Level 1 (10-11h), Level 2 (12-15h), Level 3 (25-31h). ROI is positive after 1st SAP for Level 1, and break-even occurs at 2-4 SAPs for Level 3.

**Q: Can I customize the generated templates?**

**Agent Response**:
Yes. Level 1 uses default templates as-is. Level 2+ allows template customization:
- Edit templates/sap/*.j2 files to change structure or content
- Add extended schema fields in .chora/config.yaml
- Create domain-specific template variations (e.g., frontend-sap.j2, backend-sap.j2)
- Template changes propagate to all future generations

Caution: Test template syntax with `python -m jinja2 <template>` before using in production.

**Q: What if I want to regenerate a SAP after manual edits?**

**Agent Response**:
Check the YAML frontmatter in generated files:
- `regeneration_safe: false` (default) → Regeneration will overwrite manual edits. Don't regenerate.
- `regeneration_safe: true` (Level 3 only) → Regeneration preserves manual sections. Safe to regenerate.

Best practice: Complete all manual TODOs first, then mark `completion_status: complete` in frontmatter. This signals "don't regenerate."

If you must regenerate with manual edits:
1. Backup existing files: `cp -r docs/skilled-awareness/database-migrations docs/skilled-awareness/database-migrations.backup`
2. Regenerate: `python scripts/generate-sap.py SAP-030 --force`
3. Manually merge changes: `diff -r database-migrations.backup database-migrations`

**Q: How do I know if my generated SAP is complete enough?**

**Agent Response**:
Use SAP-019 (Self-Evaluation) to validate:
```bash
python scripts/sap-evaluator.py --quick SAP-030  # Quick check
python scripts/sap-evaluator.py --deep SAP-030   # Comprehensive check
```

Criteria for "complete enough":
- Level 1: 60-105 TODOs per SAP (acceptable for internal use)
- Level 2: 40-80 TODOs per SAP (acceptable for team use)
- Level 3: <10 TODOs per SAP (required for production/ecosystem release)

Check TODO count: `grep -r "TODO" docs/skilled-awareness/database-migrations/ | wc -l`

If TODO count exceeds level target, continue manual filling. If below, run validation and consider promoting to next level.

---

## 7. Best Practices for Agents

<!-- TODO: Guidelines for agents using this SAP

Include:
- Best practices
- Anti-patterns to avoid
- Efficiency tips
- Quality checks
-->

### Do's ✅

- ✅ **Always validate SAP metadata in catalog before generation** - Prevents SAP-029-001 errors and ensures MVP fields are complete
- ✅ **Run sap-evaluator.py after generation** - Catches structural issues, broken links, and validates TODO count
- ✅ **Start with Level 1 (Basic) for first SAP** - Understand the system before investing in Level 2/3 setup
- ✅ **Use batch generation for 5+ SAPs** - Level 2's `generate-sap-batch.py` saves time vs multiple individual commands
- ✅ **Commit generated artifacts to git immediately** - Preserves generation provenance in YAML frontmatter, enables rollback
- ✅ **Fill TODO markers progressively** - Complete high-priority sections (protocol-spec) before low-priority (adoption-blueprint trivia)
- ✅ **Adopt Level 3 for production ecosystems** - Quality gates prevent under-filled SAPs from being published

### Don'ts ❌

- ❌ **Don't skip SAP-000 dependency check** - SAP-029 requires SAP framework structure; generation will fail without it
- ❌ **Don't regenerate SAPs with manual edits** - Unless `regeneration_safe: true`, you'll lose manual work. Backup first.
- ❌ **Don't customize templates without syntax validation** - Run `python -m jinja2 <template>` to catch errors before committing
- ❌ **Don't deploy Level 1 SAPs to production** - 60-105 TODOs is too many for ecosystem release; use Level 3 (<10 TODOs)
- ❌ **Don't ignore quality gate failures** - If CI/CD blocks merge due to TODO threshold, complete TODOs before forcing merge
- ❌ **Don't use SAP-029 for non-SAP documentation** - Templates are opinionated for SAP-000 structure; use different tool for custom docs

### Efficiency Tips

**Tip 1**: Use Parallel Batch Generation (Level 3)
- **Why**: Reduces batch generation time from 5min × N SAPs to ~5-10min total (70-85% time savings for 10+ SAPs)
- **How**: Enable `parallel_generation: true` in .chora/config.yaml. Modify `generate-sap-batch.py` to use Python's `concurrent.futures.ProcessPoolExecutor` for multi-core utilization.

**Tip 2**: Enable Template Caching (Level 2+)
- **Why**: 50-70% performance improvement for large SAP ecosystems by avoiding repeated template parsing
- **How**: Set `cache_enabled: true` in templates config. Jinja2 Environment will cache compiled templates in memory between generations.

**Tip 3**: Complete Protocol-Spec TODOs First
- **Why**: protocol-spec.md is the most critical artifact (agents rely on it for implementation). Completing it first maximizes value if time runs out.
- **How**: After generation, prioritize filling TODOs in this order: (1) protocol-spec, (2) awareness-guide, (3) capability-charter, (4) adoption-blueprint, (5) ledger.

**Tip 4**: Use Extended Schema for Domain-Specific SAPs (Level 2)
- **Why**: Reduces TODO count from 60-105 to 40-80 by pre-filling domain-specific fields (e.g., `frontend_framework`, `api_contracts`)
- **How**: Add `extended_fields` to .chora/config.yaml with domain-specific metadata. Update templates to consume these fields. Example: React ecosystem SAPs can include `component_patterns`, `state_management_approach` in extended schema.

**Tip 5**: Automate INDEX.md Updates
- **Why**: Manual INDEX.md updates are error-prone and time-consuming (5-10 min per SAP)
- **How**: Run `python scripts/update-sap-index.py` after generation to automatically add SAP entry to docs/skilled-awareness/INDEX.md. Integrate into CI/CD workflow for Level 3.

---

## 8. Validation & Quality Checks

<!-- TODO: How agents should validate their work

Help agents:
- Verify correct implementation
- Check quality
- Confirm success
-->

### Agent Self-Check Checklist

Before completing a task with SAP-029, agents should verify:

- [ ] SAP entry exists in sap-catalog.json with all 9 MVP fields
- [ ] SAP-000 (SAP Framework) is installed and accessible
- [ ] Templates exist in templates/sap/ (5 .j2 files)
- [ ] Generation command executed without errors (exit code 0)
- [ ] All 5 artifacts created in docs/skilled-awareness/{sap-name}/
- [ ] TODO count within expected range for adoption level (Level 1: 60-105, Level 2: 40-80, Level 3: <10)
- [ ] sap-evaluator.py validation passed (--quick mode minimum)
- [ ] YAML frontmatter present in generated files (generation_method, generated_at, completion_status)
- [ ] No template syntax errors or encoding issues encountered
- [ ] INDEX.md updated with new SAP entry (if applicable)
- [ ] Validation command executed successfully
- [ ] User confirmed expected behavior or acknowledged TODO completion requirements

### Validation Commands

```bash
# Primary validation: Verify generation succeeded
python scripts/sap-evaluator.py --quick SAP-030
# Expected: "✅ SAP-030 validation passed" (or specific issues to address)

# Secondary validation: Check TODO count
grep -r "TODO" docs/skilled-awareness/database-migrations/ | wc -l
# Expected: 60-105 (Level 1), 40-80 (Level 2), <10 (Level 3)

# Tertiary validation: Verify artifact structure
ls -1 docs/skilled-awareness/database-migrations/*.md
# Expected: 5 files (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)

# Quality gate check (Level 3 only)
python scripts/quality-gate-sap.py SAP-030 10
# Expected: Exit code 0 (passes) or 1 (fails with TODO count)

# Link validation (if SAP-016 adopted)
bash scripts/validate-awareness-links.sh docs/skilled-awareness/database-migrations/
# Expected: No broken links reported
```

---

## 9. Version Compatibility

**Current Version**: 1.0.0

### Compatibility Notes

- **SAP-029 1.0.0** is compatible with:


  - SAP-000 1.0.0+



### Breaking Changes

<!-- TODO: Document any breaking changes from previous versions -->

**No breaking changes** (initial release)

---

## 10. Additional Resources

### Within chora-base

- [Protocol Specification](./protocol-spec.md) - Technical contracts
- [Adoption Blueprint](./adoption-blueprint.md) - Step-by-step installation
- [Capability Charter](./capability-charter.md) - Problem statement and scope

### External Resources

- [Jinja2 Official Documentation](https://jinja.palletsprojects.com/en/3.1.x/) - Template engine syntax, filters, and best practices for SAP-029 templates
- [Cookiecutter Documentation](https://cookiecutter.readthedocs.io/) - Reference for template-based project generation patterns (inspiration for SAP-029 design)
- [Yeoman Generator Guide](https://yeoman.io/authoring/) - Alternative template system with scaffolding patterns (comparison for migration paths)
- [Template Method Pattern](https://refactoring.guru/design-patterns/template-method) - Design pattern underlying SAP-029's template architecture
- [Semantic Versioning 2.0.0](https://semver.org/) - Versioning strategy for SAP-029 templates and generated artifacts
- [GitHub Actions Documentation](https://docs.github.com/en/actions) - CI/CD integration patterns for Level 3 automated pipelines

---

**For Agents**: This awareness guide is your quick reference. For detailed technical specifications, see [protocol-spec.md](./protocol-spec.md). For installation instructions, see [adoption-blueprint.md](./adoption-blueprint.md).

**Version**: 1.0.0 (2025-11-02)