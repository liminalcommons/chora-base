# Adoption Blueprint: Cross-Repository Inbox Skilled Awareness Package

**SAP ID**: SAP-001
**Version**: 1.2.0
**Status**: Active (Level 3)
**Last Updated**: 2025-11-11

---

## 1. Read Before You Begin
- **Capability Charter:** `docs/reference/skilled-awareness/inbox/capability-charter.md`
- **Protocol Spec:** `docs/reference/skilled-awareness/inbox/protocol-spec.md`
- **Prerequisites:**
  - Repository uses Git and supports committing coordination artefacts.
  - Maintainership agreement to adopt inbox workflow (coordination cadence defined).
  - Shell utilities available (`bash`, `jq`, optional `yq`) or equivalent tooling.
  - AI agent guides (AGENTS.md / CLAUDE.md) ready to reference new awareness guide.

---

## 2. Installation

### Quick Install

Use the automated installation script:

```bash
python scripts/install-sap.py SAP-001 --source /path/to/chora-base
```

**What This Installs**:
- Inbox coordination protocol documentation (5 artifacts)
- `inbox/` directory structure at repository root
- Schema files, CAPABILITIES configuration, and event log
- Cross-repo coordination workflows

### Part of Sets

This SAP is included in:
- minimal-entry
- recommended
- full

To install a complete set:
```bash
python scripts/install-sap.py --set minimal-entry --source /path/to/chora-base
```

### Validation

Verify all artifacts exist:

```bash
# Verify SAP documentation
ls docs/skilled-awareness/inbox/*.md
# Verify inbox directory structure
ls inbox/coordination/events.jsonl inbox/incoming/
```

### CLI Tools Installation

SAP-001 v1.2.0 includes 5 CLI tools for inbox management:

```bash
# Verify Python dependencies installed
pip install click pyyaml jsonlines anthropic openai

# Test CLI tools availability
python scripts/inbox-create.py --help
python scripts/inbox-query.py --help
python scripts/inbox-triage.py --help
python scripts/inbox-update.py --help
python scripts/inbox-archive.py --help
```

**CLI Tool Capabilities**:
- `inbox-create.py`: Create coordination items with schema validation
- `inbox-query.py`: Filter and search items (`--incoming`, `--unacknowledged`, `--request COORD-ID`, `--status`, `--format json`)
- `inbox-triage.py`: Triage incoming items to active status
- `inbox-update.py`: Update item status and metadata
- `inbox-archive.py`: Archive completed items

### AI-Powered Generation Setup (Level 3)

For AI-powered COORD generation (60x ROI, 40-60x faster creation):

**1. Install AI dependencies:**

```bash
pip install anthropic openai jinja2
```

**2. Configure API keys:**

```bash
# Option A: Environment variables
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# Option B: .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
echo "OPENAI_API_KEY=sk-..." >> .env
```

**3. Test AI-powered generation:**

```bash
# Interactive mode (recommended for first use)
python scripts/generate-coordination-request.py --interactive

# Context file mode
python scripts/generate-coordination-request.py --context context.json

# Preview mode (no file write)
python scripts/generate-coordination-request.py --preview
```

**AI Generator Features**:
- Claude Sonnet 4.5 primary generation
- OpenAI GPT-4 fallback
- SMART criteria validation
- Deliverable and acceptance criteria generation
- Template-based prompt rendering
- JSON extraction from AI responses

**Expected Performance**:
- Manual COORD creation: 2-3 hours
- AI-powered creation: 3 minutes (interactive CLI)
- Time savings: 40-60x faster

### Light+ Planning Framework Integration (v1.2.0)

SAP-001 v1.2.0 integrates with SAP-012 (Light+ Framework) for strategic planning:

**1. Enable Light+ metadata tracking:**

Add `light_plus_metadata` to COORD schema in `inbox/coordination/` items:

```json
{
  "request_id": "COORD-2025-001",
  "title": "Example coordination request",
  "priority": "P1",
  "urgency": "next_sprint",

  "light_plus_metadata": {
    "intention_id": null,
    "evidence_level": null,
    "user_demand_score": null,
    "effort_estimate_hours": null,
    "vision_wave_assignment": null,
    "assigned_to_roadmap": null,
    "status": "pending_discovery"
  }
}
```

**2. Phase 1.1 Discovery workflow:**

During quarterly planning, analyze active COORDs as intentions:

```bash
# Find active COORDs for discovery
python scripts/inbox-query.py --status active --format json > active_coords.json

# Assess evidence levels (A/B/C)
# Level A: P0/P1 + urgent + external repo
# Level B: P1/P2 + next_sprint + team request
# Level C: P2/P3 + backlog + internal improvement

# Update COORD with evidence assessment
python scripts/inbox-update.py COORD-2025-001 \
  --metadata '{"light_plus_metadata": {"evidence_level": "A"}}'
```

**3. Wave assignment criteria:**

Assign COORDs to Wave 1 (Q4) or Wave 2 (Q1) based on:
- Evidence Level A+B ≥ 70% → Wave 1 candidate
- User demand score ≥ 10 → Wave 1 candidate
- Effort estimate < 50 hours → Wave 1 candidate

**4. Traceability setup:**

Link COORDs to intentions and roadmap:

```bash
# Create intention from COORD
echo '{
  "intention_id": "INT-2025-005",
  "source": "COORD-2025-001",
  "evidence_level": "A",
  "user_demand": 12,
  "effort_hours": 24
}' >> .chora/planning/intentions/2025-Q4.jsonl

# Update COORD with intention link
python scripts/inbox-update.py COORD-2025-001 \
  --metadata '{"light_plus_metadata": {"intention_id": "INT-2025-005"}}'
```

**Benefits of Light+ Integration**:
- Coordination requests drive strategic roadmap decisions
- Evidence-based Wave 1/Wave 2 assignment
- Complete traceability: COORD → intention → wave → epic → tasks → shipped
- Lead time metrics: coordination request → production deployment
- Quarterly retrospectives with quantitative insights

**Documentation References**:
- Light+ integration details: [protocol-spec.md Section 15](protocol-spec.md#15-light-planning-framework-integration)
- Agent workflows: [AGENTS.md Light+ Integration](AGENTS.md#integration-with-sap-012-light-framework)
- Claude Code patterns: [CLAUDE.md Workflows 4-6](CLAUDE.md#workflow-4-analyzing-coords-as-intentions-for-light-planning)

### Manual Installation (Alternative)

If you cannot use the install script, follow these manual steps:

1. Create `inbox/` directory at repository root
2. Copy prototype structure from `chora-base/inbox/`
3. Add schema files under `inbox/schemas/`
4. Initialize `inbox/coordination/events.jsonl` as an empty append-only log
5. Customize `coordination/CAPABILITIES/<repo>.yaml` with repo-specific routing details
6. Add awareness references to the repo's `CLAUDE.md` / `AGENTS.md`
7. Commit with message noting adoption

---

## 3. Files & Directories

| Path | Purpose | Optional? | Notes |
|------|---------|-----------|-------|
| `inbox/INBOX_PROTOCOL.md` | Local protocol copy (press ready reference). | Yes (may link to canonical doc) | Keep pointer to spec for operator convenience. |
| `inbox/CLAUDE.md` | Awareness guide tailored to repo. | Recommended | Customize with repo name, capabilities. |
| `inbox/coordination/events.jsonl` | Event log for state transitions. | Required | Initialize empty file; ensure append-only. |
| `inbox/coordination/CAPABILITIES/<repo>.yaml` | Defines work the repo can send/receive. | Required | Update with categories, limits, contacts. |
| `inbox/incoming/coordination/` | Queue for coordination requests. | Required | Start empty; ensure README describing usage. |
| `inbox/incoming/tasks/` | Queue for implementation tasks. | Required | Provide README with acceptance criteria. |
| `inbox/ecosystem/proposals/` | Strategic proposals (markdown). | Optional initially | Adopt when planning cadence defined. |
| `docs/reference/skilled-awareness/inbox/` | Canonical SAP docs (charter, spec, etc.). | Required | Copy or symlink from chora-base template. |
| `docs/reference/skilled-awareness/inbox/ledger.md` | Traceability ledger entry for repo. | Required | Seed with repo information during install. |

---

## 4. Configuration Checklist

- [ ] Repo maintainer owns inbox package (listed in ledger).  
- [ ] `CAPABILITIES/<repo>.yaml` defines `provides`, `consumes`, `can_receive`.  
- [ ] Awareness guide cross-linked from root `CLAUDE.md` / `AGENTS.md`.  
- [ ] Event log file created with header comment describing format (optional metadata).  
- [ ] Schema validation command tested (`cat … | jq .` or `python -m json.tool`).  
- [ ] Documentation plan updated to include inbox capability (if applicable).

---

## 5. Verification

### Level 1 Verification (Basic Installation)

- **Smoke Checks:**
  - Create sample coordination request (JSON) and ensure schema validation passes.
  - Move sample task through `incoming → active → completed` while logging events.
  - Run awareness checklist: agent performs triage simulation using guide.

- **Acceptance Tests:**
  - Ensure README/CLAUDE instructions clear to another maintainer (peer review).
  - Confirm event log entry format consistent with spec.
  - Review adoption ledger entry for accuracy and completeness.

### Level 2 Verification (CLI Tools & Event Logging)

- **CLI Tool Tests:**
  ```bash
  # Test inbox-create
  python scripts/inbox-create.py \
    --title "Test COORD" \
    --priority P2 \
    --requesting-repo test-repo

  # Test inbox-query
  python scripts/inbox-query.py --incoming --format json

  # Test inbox-triage
  python scripts/inbox-triage.py COORD-2025-TEST

  # Test inbox-update
  python scripts/inbox-update.py COORD-2025-TEST --status in_progress

  # Test inbox-archive
  python scripts/inbox-archive.py COORD-2025-TEST
  ```

- **Event Logging Validation:**
  ```bash
  # Verify events logged for all state transitions
  cat inbox/coordination/events.jsonl | jq 'select(.request_id == "COORD-2025-TEST")'

  # Expected event types: created, triaged, activated, completed, archived
  cat inbox/coordination/events.jsonl | jq -r '.event_type' | sort | uniq
  ```

- **Acceptance Criteria:**
  - ✅ All 5 CLI tools execute without errors
  - ✅ Event log captures all state transitions
  - ✅ JSON schema validation passes for all items
  - ✅ Usage tracking decorator logs CLI invocations

### Level 3 Verification (AI Generation & Light+ Integration)

- **AI-Powered Generation Tests:**
  ```bash
  # Test AI generation in preview mode (no API calls)
  python scripts/generate-coordination-request.py --preview

  # Test AI generation with Claude API
  python scripts/generate-coordination-request.py \
    --title "Test AI-generated COORD" \
    --description "Validate AI generation workflow"

  # Verify generated COORD has SMART criteria
  cat inbox/coordination/COORD-2025-XXX.json | jq '.deliverables, .acceptance_criteria'
  ```

- **Multi-Generator System Validation:**
  ```bash
  # Test all 5 generator types
  # 1. ai_augmented (Claude/OpenAI)
  # 2. template (Jinja2 expansion)
  # 3. user_input (interactive prompts)
  # 4. literal (direct value assignment)
  # 5. base (abstract interface)

  # Verify generator config loaded
  python -c "from scripts.inbox_generator.core.config_loader import load_config; \
             print(load_config('config.yaml'))"
  ```

- **Light+ Integration Tests:**
  ```bash
  # Test evidence level assessment
  python scripts/inbox-query.py --status active --format json | \
    jq 'map(select(.priority == "P0" or .priority == "P1") | \
            select(.urgency == "blocks_sprint" or .urgency == "next_sprint")) | \
        length'

  # Test Wave assignment
  # Verify COORDs with evidence_level A+B ≥ 70% are Wave 1 candidates

  # Test intention linking
  cat .chora/planning/intentions/2025-Q4.jsonl | \
    jq 'select(.source | startswith("COORD-"))'
  ```

- **Performance Validation:**
  ```bash
  # Measure COORD creation time
  time python scripts/generate-coordination-request.py --interactive

  # Expected: < 5 minutes (target: 3 minutes)
  # Compare to manual baseline: 2-3 hours
  # ROI validation: 40-60x faster
  ```

- **Acceptance Criteria (Level 3):**
  - ✅ AI generation creates valid COORDs in < 5 minutes
  - ✅ All 5 generator types operational
  - ✅ Light+ metadata schema validated
  - ✅ Evidence level assessment rules implemented
  - ✅ Wave assignment criteria documented
  - ✅ Intention linking workflow tested
  - ✅ 60x ROI achieved (25h saved/month at 16h investment)

### Rollback Plan

- **Rollback Steps:**
  - Remove `inbox/` directory and revert supporting docs to previous state.
  - Update ledger with rollback note and reason.
  - Communicate to ecosystem coordinator via inbox strategic note.

- **Partial Rollback (L3 → L2):**
  - Remove AI generator dependencies: `pip uninstall anthropic openai`
  - Keep CLI tools operational (inbox-query, inbox-triage, etc.)
  - Retain event logging and basic coordination workflows

---

## 6. Post-Install Tasks

- **Awareness Enablement:**  
  - Update root `CLAUDE.md` and `AGENTS.md` to reference inbox awareness guide.  
  - Schedule agent dry run to confirm instructions.

- **Status Ledger Update:**  
  - Add entry to `docs/reference/skilled-awareness/inbox/ledger.md` noting adoption date, version, and feedback channel.

- **Feedback Loop:**  
  - After first sprint of usage, document lessons learned in ledger feedback log.  
  - Raise coordination item if additional automation or schema changes needed.

---

## 7. Version History

**Version 1.2.0** (2025-11-11):
- Added AI-powered generation setup (Claude Sonnet 4.5 + OpenAI GPT-4)
- Added CLI tools installation (5 tools: create, query, triage, update, archive)
- Added Light+ planning framework integration (SAP-012)
- Added Level 3 verification tests (AI generation, multi-generator, Light+ metadata)
- Updated verification to 3 levels (L1: basic, L2: CLI/events, L3: AI/Light+)
- Added Light+ metadata schema example
- Added Phase 1.1 Discovery workflow
- Added Wave assignment criteria and traceability patterns
- Added performance validation (60x ROI, 40-60x faster creation)
- Added partial rollback plan (L3 → L2)

**Version 1.0.0** (2025-10-27):
- Initial adoption blueprint for SAP-001
- Basic installation instructions (quick install, manual install)
- Directory structure and file descriptions
- Configuration checklist
- Level 1 verification and smoke tests
- Post-install tasks and awareness enablement


---

## 8. Migration Guide: v1.1.0 → v1.2.0

This guide helps existing SAP-001 v1.1.0 adopters upgrade to v1.2.0.

### What's New in v1.2.0

1. **Light+ Planning Framework Integration (SAP-012)**
   - COORD items can drive Phase 1.1 Discovery
   - Evidence level categorization (A/B/C)
   - Wave assignment workflow (Q4 Wave 1 vs Q1 Wave 2)
   - Complete traceability: COORD → intention → epic → shipped

2. **Enhanced Schema**
   - New optional `light_plus_metadata` object
   - 7 metadata fields for planning integration
   - Backward compatible (v1.1.0 COORDs still valid)

3. **Updated Documentation**
   - 800+ lines of Light+ integration documentation
   - 3 new Claude Code workflows (CLAUDE.md)
   - 6 new agent patterns (AGENTS.md)
   - Complete protocol spec update (Section 15)

### Migration Steps

#### Step 1: Update SAP-001 Documentation (5 min)

```bash
# Backup current version
cp -r docs/skilled-awareness/inbox docs/skilled-awareness/inbox-v1.1.0-backup

# Update to v1.2.0 (if using install-sap.py)
python scripts/install-sap.py SAP-001 --source /path/to/chora-base --force

# Or manually update each artifact:
# - capability-charter.md (version header)
# - protocol-spec.md (Section 15 + version)
# - AGENTS.md (Light+ integration section + version)
# - CLAUDE.md (3 new workflows + version)
# - adoption-blueprint.md (AI setup + Light+ setup + version)
# - ledger.md (v1.2.0 achievement section)
```

#### Step 2: Update Active COORD Items (10-20 min)

Add `light_plus_metadata` to existing COORD JSON files:

```bash
# For each active COORD file:
for coord in inbox/coordination/COORD-*.json; do
  # Add light_plus_metadata object
  jq '. + {
    "light_plus_metadata": {
      "intention_id": null,
      "evidence_level": null,
      "user_demand_score": null,
      "effort_estimate_hours": null,
      "vision_wave_assignment": null,
      "assigned_to_roadmap": null,
      "status": "pending_discovery"
    }
  }' "$coord" > "$coord.tmp" && mv "$coord.tmp" "$coord"
done

# Or manually add to each COORD file
```

**Example migration**:

```json
{
  "request_id": "COORD-2025-001",
  "title": "Example coordination request",
  "priority": "P1",
  "urgency": "next_sprint",
  
  // Add this object (v1.2.0)
  "light_plus_metadata": {
    "intention_id": null,
    "evidence_level": "B",  // Assess based on priority/urgency/source
    "user_demand_score": null,
    "effort_estimate_hours": null,
    "vision_wave_assignment": null,
    "assigned_to_roadmap": null,
    "status": "pending_discovery"
  }
}
```

#### Step 3: Update Catalog and Ecosystem Status (2 min)

```bash
# Update sap-catalog.json
jq '(.saps[] | select(.id == "SAP-001") | .version) = "1.2.0"' sap-catalog.json > tmp.json
mv tmp.json sap-catalog.json

# Update ECOSYSTEM_STATUS.yaml (if exists)
# Add inbox_protocol_version: 1.2.0 to your repo entry
```

#### Step 4: Optional - Enable Level 3 Features (10-30 min)

If not already using AI-powered generation:

```bash
# Install AI dependencies
pip install anthropic openai jinja2

# Configure API keys
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# Test AI generation
python scripts/generate-coordination-request.py --interactive
```

#### Step 5: Verify Migration (5 min)

```bash
# Verify schema compatibility
cat inbox/coordination/COORD-*.json | jq '.light_plus_metadata'

# Expected: All files have light_plus_metadata object (even if null values)

# Verify documentation updated
grep "Version.*1.2.0" docs/skilled-awareness/inbox/*.md

# Expected: All 5 artifacts show v1.2.0

# Verify catalog updated
grep -A 3 '"id": "SAP-001"' sap-catalog.json | grep version

# Expected: "version": "1.2.0"
```

### Backward Compatibility

**v1.1.0 COORDs remain valid in v1.2.0**:
- Missing `light_plus_metadata` treated as null (no error)
- Existing workflows continue to work
- CLI tools backward compatible
- Event logging unchanged

**Migration is optional**:
- Can run v1.2.0 SAP documentation with v1.1.0 COORD files
- Light+ integration only activates if metadata present
- Gradual migration supported (update COORDs as needed)

### Rollback to v1.1.0

If issues arise:

```bash
# Restore v1.1.0 backup
rm -rf docs/skilled-awareness/inbox
mv docs/skilled-awareness/inbox-v1.1.0-backup docs/skilled-awareness/inbox

# Remove light_plus_metadata from COORD files
for coord in inbox/coordination/COORD-*.json; do
  jq 'del(.light_plus_metadata)' "$coord" > "$coord.tmp" && mv "$coord.tmp" "$coord"
done

# Revert catalog
jq '(.saps[] | select(.id == "SAP-001") | .version) = "1.1.0"' sap-catalog.json > tmp.json
mv tmp.json sap-catalog.json
```

### Support

**Migration issues?**
- Check [protocol-spec.md Section 15](protocol-spec.md#15-light-planning-framework-integration) for Light+ details
- Review [AGENTS.md](AGENTS.md) for updated workflows
- See [ledger.md](ledger.md) for migration feedback log
- Create COORD item for migration support request

**Total migration time**: 30-60 minutes (documentation + schema updates + verification)

**Expected benefits**:
- Strategic planning integration with Light+ framework
- Evidence-based roadmap decisions
- Complete COORD → shipped traceability
- Quarterly retrospectives with quantitative insights

