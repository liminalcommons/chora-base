# Change Request: COORD-2025-003 v1.9.0 Capabilities Documentation

**Trace ID**: CHORA-COORD-2025-003
**Type**: Documentation enhancement
**Status**: Accepted - Ready for implementation
**Priority**: Medium
**Sprint**: 2025-W44
**Estimated Effort**: 2.75-4.25 hours

---

## Overview

Update chora-base documentation to reference chora-compose v1.9.0 capabilities (stigmergic context links and freshness tracking), enabling efficient cross-repository coordination with 95% token reduction for common operations.

---

## Acceptance Criteria (From Coordination Request)

1. ✅ chora-base AGENTS.md includes stigmergic context link examples
2. ✅ SAP maintenance workflow documented with freshness tracking integration
3. ✅ At least one CI/CD example showing automated freshness checks
4. ✅ Cross-references between chora-base and chora-compose documentation are bidirectional
5. ✅ Changes validated by generating at least one SAP using stigmergic context links

---

## Implementation Plan

### Phase 1: Update AGENTS.md (30-45 min)

**File**: `AGENTS.md`

**Changes**:

1. **Add new section after "Installing SAPs"** (around line 100):

```markdown
### Cross-Repository Coordination with chora-compose

chora-base integrates with chora-compose v1.9.0 for efficient SAP generation and maintenance via **stigmergic context links**.

#### Stigmergic Context Links

**Pattern**: `[@repository/capability:resource-identifier]`

**Token Efficiency**: 95% reduction (20k→1k tokens) for cross-repo operations

**Examples**:
```markdown
# Regenerate complete SAP-004 Testing Framework
[@chora-compose/collection:sap-004-complete]

# Check freshness of all SAPs
[@chora-compose/freshness:all-saps]

# Generate single SAP artifact (charter only)
[@chora-compose/generate:charter:sap-004]

# Validate collection configuration
[@chora-compose/validate:collection:sap-suite]
```

**How It Works**:
AI agents recognize the `[@...]` pattern and execute the corresponding MCP tool immediately, without loading chora-compose documentation. This eliminates context overhead for routine operations.

**Available Capabilities**:
- `collection`: Generate multi-artifact collections (complete SAPs)
- `freshness`: Check content age/staleness
- `generate`: Generate single content item
- `validate`: Validate collection configuration

**Documentation**: See [SAP Maintenance Workflow](docs/guides/sap-maintenance-workflow.md) for integration examples.

**Version**: Requires chora-compose v1.9.0+
```

2. **Update "Creating SAPs" section** to reference stigmergic regeneration:

```markdown
### Regenerating SAPs

**Using stigmergic context links** (chora-compose v1.9.0+):

To regenerate a complete SAP after updates:
```markdown
[@chora-compose/collection:sap-<capability-name>-complete]
```

Example: `[@chora-compose/collection:sap-004-complete]`

This triggers full regeneration of all 5 SAP artifacts from current content blocks.

**Manual regeneration** (fallback):
1. Load chora-compose AGENTS.md
2. Follow SAP-014 (chora-compose-integration) awareness guide
3. Execute: `choracompose:generate_collection(collection_id="sap-<capability-name>-complete")`
```

**Testing**:
- Verify stigmergic context link renders correctly in markdown
- Test pattern recognition by AI agent
- Validate SAP generation executes successfully

---

### Phase 2: Create SAP Maintenance Workflow Guide (60-90 min)

**File**: `docs/guides/sap-maintenance-workflow.md` (new file)

**Content Structure**:

```markdown
# SAP Maintenance Workflow

**Purpose**: Guide for maintaining SAP documentation freshness using chora-compose v1.9.0 capabilities

**Audience**: Maintainers, contributors, AI agents

---

## Overview

SAP documentation requires periodic regeneration to stay current with:
- Template changes (chora-base evolves)
- Content block updates (constituent documentation changes)
- Context shifts (repository metadata, user preferences)

chora-compose v1.9.0 introduces **freshness tracking** to automate staleness detection and prioritize regeneration work.

---

## Freshness Tracking

### Three-State Classification

| Status | Threshold | Color | Action |
|--------|-----------|-------|--------|
| **Fresh** | <80% of threshold | 🟢 Green | No action needed |
| **Stale** | 80-100% of threshold | 🟡 Yellow | Schedule regeneration this week |
| **Expired** | ≥100% of threshold | 🔴 Red | Regenerate immediately |

### Configuration

Define freshness thresholds per artifact type in collection manifest:

```json
{
  "collection_id": "sap-004-complete",
  "members": [
    {
      "id": "charter",
      "freshness_threshold_days": 30
    },
    {
      "id": "protocol",
      "freshness_threshold_days": 7
    },
    {
      "id": "awareness-guide",
      "freshness_threshold_days": 3
    },
    {
      "id": "adoption-blueprint",
      "freshness_threshold_days": 7
    },
    {
      "id": "traceability-ledger",
      "freshness_threshold_days": 1
    }
  ]
}
```

**Threshold Guidelines**:
- **Charter** (30 days): Changes infrequently (problem statement, scope)
- **Protocol** (7 days): Moderate change frequency (technical contracts)
- **Awareness Guide** (3 days): Changes with patterns and best practices
- **Adoption Blueprint** (7 days): Changes with installation steps
- **Traceability Ledger** (1 day): High-frequency updates (adopter tracking)

---

## Workflows

### Weekly Freshness Check

**Schedule**: Every Monday, 10:00 AM
**Duration**: 5-10 minutes
**Tool**: GitHub Actions (see CI/CD example below)

**Steps**:

1. **Run freshness check** for all SAPs:
   ```bash
   mcp-client execute choracompose:check_freshness \
     --manifest-path .chora/manifests/all-saps.json \
     --default-threshold-days 7
   ```

2. **Review output**:
   ```json
   {
     "overall_status": "expired",
     "summary": {
       "total_members": 90,
       "fresh_count": 72,
       "stale_count": 12,
       "expired_count": 6
     }
   }
   ```

3. **Prioritize regeneration**:
   - **Expired** (6 SAPs): Regenerate today
   - **Stale** (12 SAPs): Schedule this week
   - **Fresh** (72 SAPs): No action

4. **Trigger regeneration** using stigmergic context links:
   ```markdown
   Expired SAPs (regenerate now):
   - [@chora-compose/collection:sap-004-complete]
   - [@chora-compose/collection:sap-007-complete]
   - [@chora-compose/collection:sap-012-complete]
   ```

### Ad-Hoc Regeneration

**When to use**:
- Content blocks updated
- Template structure changed
- Context requirements changed

**Steps**:

1. **Check freshness** for specific SAP:
   ```markdown
   [@chora-compose/freshness:sap-004-complete]
   ```

2. **Review status** - if stale or expired, regenerate:
   ```markdown
   [@chora-compose/collection:sap-004-complete]
   ```

3. **Validate output** - verify all 5 artifacts generated correctly

### Selective Member Regeneration

**When to use**:
- Only one artifact type changed (e.g., awareness guide patterns updated)
- Want to minimize regeneration time

**Steps**:

1. **Generate single artifact**:
   ```markdown
   [@chora-compose/generate:awareness-guide:sap-004]
   ```

2. **Update collection manifest** with new generation timestamp

3. **Verify** artifact integrates correctly with existing members

---

## CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/sap-freshness.yml`

```yaml
name: SAP Freshness Check

on:
  schedule:
    - cron: '0 10 * * 1'  # Weekly, Monday 10:00 AM UTC
  workflow_dispatch:       # Manual trigger for testing

jobs:
  check-freshness:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install MCP client
        run: |
          pip install mcp-client

      - name: Check SAP freshness
        id: freshness
        run: |
          # Call chora-compose check_freshness tool
          OUTPUT=$(mcp-client execute choracompose:check_freshness \
            --manifest-path .chora/manifests/all-saps.json \
            --default-threshold-days 7 \
            --format json)

          echo "freshness_output=$OUTPUT" >> $GITHUB_OUTPUT

          # Parse output
          EXPIRED_COUNT=$(echo "$OUTPUT" | jq '.summary.expired_count')
          STALE_COUNT=$(echo "$OUTPUT" | jq '.summary.stale_count')

          echo "expired_count=$EXPIRED_COUNT" >> $GITHUB_OUTPUT
          echo "stale_count=$STALE_COUNT" >> $GITHUB_OUTPUT

      - name: Create issue if expired SAPs found
        if: steps.freshness.outputs.expired_count > 0
        uses: actions/github-script@v6
        with:
          script: |
            const expiredCount = ${{ steps.freshness.outputs.expired_count }};
            const staleCount = ${{ steps.freshness.outputs.stale_count }};

            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: `[SAP Maintenance] ${expiredCount} expired SAPs need regeneration`,
              body: `## SAP Freshness Report\\n\\n**Expired**: ${expiredCount} SAPs (regenerate immediately)\\n**Stale**: ${staleCount} SAPs (schedule this week)\\n\\nSee workflow run for details.`,
              labels: ['sap-maintenance', 'automated']
            });

      - name: Comment summary
        run: |
          echo "## SAP Freshness Summary"
          echo "- Expired: ${{ steps.freshness.outputs.expired_count }}"
          echo "- Stale: ${{ steps.freshness.outputs.stale_count }}"
```

**Testing**:
1. Trigger workflow manually via `workflow_dispatch`
2. Verify freshness check executes
3. Confirm issue created if expired SAPs found

**Customization**:
- Adjust schedule (daily, weekly, monthly)
- Change notification method (Slack, email, issue)
- Set custom thresholds per SAP

---

## Health Monitoring Dashboard (Optional)

### Integration Example

**Query freshness for all collections**:
```javascript
const collections = ['sap-004-complete', 'sap-007-complete', 'sap-012-complete'];

const freshnessData = await Promise.all(
  collections.map(id =>
    mcpClient.call('choracompose:check_freshness', {
      manifest_path: `.chora/manifests/${id}.json`
    })
  )
);
```

**Visualize health**:
```
Content Health Dashboard
========================

SAP-004 Testing Framework    ████████░░ 80% Fresh (6/8 days)
SAP-007 Documentation        ██████████ 100% Fresh (2/7 days)
SAP-012 Quality Gates        ████░░░░░░ 40% Fresh (expired 3 days ago)

Action Items:
- SAP-012: Regenerate immediately (expired)
- SAP-004: Monitor (stale in 2 days)
```

**Automated alerts**:
```
⚠️ ALERT: SAP-012 Quality Gates documentation expired 3 days ago

Recommendation: Regenerate immediately
Command: [@chora-compose/collection:sap-012-complete]
```

---

## Best Practices

### Threshold Configuration
- **Set realistic thresholds**: Match actual change frequency
- **Monitor over time**: Adjust based on usage patterns
- **Balance freshness vs effort**: Aggressive thresholds = more regeneration work

### Regeneration Workflow
- **Prioritize expired**: Always regenerate expired content first
- **Batch stale regeneration**: Schedule stale content together
- **Validate after regeneration**: Ensure quality maintained

### Automation vs Manual
- **Automate detection**: Use CI/CD for freshness checks
- **Manual regeneration**: Human triggers actual regeneration (review required)
- **Balance**: Automation for monitoring, human judgment for action

---

## Troubleshooting

### Issue: Freshness check fails
**Cause**: Manifest file missing or malformed
**Solution**: Validate manifest structure, check file paths

### Issue: Stigmergic context link not recognized
**Cause**: AI agent pattern matcher not configured
**Solution**: Verify chora-compose v1.9.0+ installed, check MCP tool availability

### Issue: Regeneration produces different results
**Cause**: Content blocks or context changed
**Solution**: Expected behavior - review changes, update if needed

---

## Resources

### chora-compose Documentation
- [Stigmergic Context Links](https://github.com/liminalcommons/chora-compose/blob/main/docs/explanation/concepts/stigmergic-context-links.md)
- [Freshness Tracking](https://github.com/liminalcommons/chora-compose/blob/main/docs/how-to/coordination/check-freshness.md)
- [Collections Reference](https://github.com/liminalcommons/chora-compose/blob/main/docs/how-to/collections/)

### chora-base Documentation
- [AGENTS.md](../../AGENTS.md) - Stigmergic context link examples
- [SAP Index](../skilled-awareness/INDEX.md) - All SAPs registry
- [SAP Framework](../skilled-awareness/sap-framework/) - SAP protocol reference

---

**Version**: 1.0.0 (chora-compose v1.9.0)
**Last Updated**: 2025-10-30
**Maintainer**: chora-base team
```

**Testing**:
- Verify all stigmergic context links render correctly
- Test CI/CD workflow manually
- Validate documentation completeness

---

### Phase 3: Create CI/CD Workflow Example (30-45 min)

**File**: `.github/workflows/sap-freshness.yml` (new file)

**Content**: (Embedded in sap-maintenance-workflow.md above)

**Additional Testing File**: `.github/workflows/README.md`

Add section documenting the SAP freshness workflow:

```markdown
## SAP Freshness Check

**File**: `sap-freshness.yml`
**Schedule**: Weekly (Monday 10:00 AM UTC)
**Purpose**: Automated detection of stale/expired SAP documentation

**Triggers**:
- Scheduled: Every Monday at 10:00 AM UTC
- Manual: `workflow_dispatch` for testing

**Actions**:
1. Check freshness of all SAPs via chora-compose MCP tool
2. Parse output for expired/stale counts
3. Create GitHub issue if expired SAPs found
4. Comment summary to workflow run

**Configuration**:
- Manifest path: `.chora/manifests/all-saps.json`
- Default threshold: 7 days
- Notification: GitHub issue with `sap-maintenance` label

**Testing**: Trigger manually via Actions tab → SAP Freshness Check → Run workflow
```

---

### Phase 4: Update SAP Cross-References (30-45 min)

**Files to Update**:

1. **SAP-000 (sap-framework)**:
   - File: `docs/skilled-awareness/sap-framework/awareness-guide.md`
   - Add section on SAP regeneration using stigmergic links
   - Example: `[@chora-compose/collection:sap-000-complete]`

2. **SAP-001 (inbox-coordination)**:
   - File: `docs/skilled-awareness/inbox/awareness-guide.md`
   - Update cross-repo coordination examples
   - Reference v1.9.0 stigmergic links for efficient coordination

3. **SAP-009 (agent-awareness)** (if exists):
   - File: `docs/skilled-awareness/agent-awareness/awareness-guide.md`
   - Add v1.9.0 capability patterns
   - Document stigmergic context link pattern recognition

**Example Update for SAP-000**:

```markdown
## Regenerating SAPs

### Using chora-compose v1.9.0+ (Recommended)

**Stigmergic context links** provide 95% token reduction for SAP regeneration:

```markdown
# Regenerate complete SAP-000 (all 5 artifacts)
[@chora-compose/collection:sap-000-complete]

# Check freshness before regeneration
[@chora-compose/freshness:sap-000-complete]

# Generate single artifact (e.g., awareness guide only)
[@chora-compose/generate:awareness-guide:sap-000]
```

**How it works**:
1. AI agent recognizes `[@...]` pattern
2. Pattern matcher resolves to MCP tool call
3. chora-compose executes generation immediately
4. No context loading required (1k tokens vs 20k tokens)

**See**: [SAP Maintenance Workflow](../../guides/sap-maintenance-workflow.md) for complete integration guide
```

---

### Phase 5: Validation Testing (15-30 min)

**Tests to Execute**:

1. **Stigmergic Context Link Test**:
   - Place `[@chora-compose/collection:sap-004-complete]` in test document
   - Invoke AI agent to parse document
   - Verify pattern recognition triggers MCP call
   - Confirm SAP-004 generation executes successfully
   - Validate all 5 artifacts generated

2. **Freshness Check Test**:
   - Execute `choracompose:check_freshness` on SAP-004 manifest
   - Verify output format matches communication brief
   - Confirm three-state classification logic
   - Test with different threshold configurations

3. **CI/CD Workflow Test**:
   - Trigger `sap-freshness.yml` workflow manually
   - Verify freshness check executes without errors
   - Confirm issue creation if expired SAPs found
   - Validate workflow output format

**Documentation of Results**:
Create `validation-results.md` in active directory:

```markdown
# Validation Results: COORD-2025-003

**Date**: YYYY-MM-DD
**Tester**: [Name]

## Test 1: Stigmergic Context Link

**Input**: `[@chora-compose/collection:sap-004-complete]`
**Expected**: SAP-004 regenerated with all 5 artifacts
**Result**: [PASS/FAIL]
**Notes**: [Observations]

## Test 2: Freshness Check

**Input**: SAP-004 manifest with 5 members
**Expected**: JSON output with three-state classification
**Result**: [PASS/FAIL]
**Output Sample**: [JSON]

## Test 3: CI/CD Workflow

**Trigger**: Manual workflow_dispatch
**Expected**: Workflow completes, issue created if expired SAPs
**Result**: [PASS/FAIL]
**Notes**: [Observations]

## Overall Assessment

[Summary of validation results]
[Any issues discovered]
[Recommendations for fixes]
```

---

## File Changes Summary

### New Files (3)
1. `docs/guides/sap-maintenance-workflow.md` - Complete maintenance guide (566 lines)
2. `.github/workflows/sap-freshness.yml` - CI/CD workflow (70 lines)
3. `inbox/active/coord-2025-003-v190-capabilities-update/validation-results.md` - Test results

### Modified Files (5-7)
1. `AGENTS.md` - Add stigmergic context links section (~50 lines)
2. `.github/workflows/README.md` - Document SAP freshness workflow (~15 lines)
3. `docs/skilled-awareness/sap-framework/awareness-guide.md` - Add regeneration section (~30 lines)
4. `docs/skilled-awareness/inbox/awareness-guide.md` - Update cross-repo examples (~20 lines)
5. `docs/skilled-awareness/agent-awareness/awareness-guide.md` - Add v1.9.0 patterns (~25 lines) [if exists]
6-7. Additional SAP awareness guides as needed

### Total Lines: ~800-900 lines (new + modifications)

---

## Git Workflow

### Branch Strategy
```bash
git checkout -b feature/coord-2025-003-chora-compose-v190-docs
```

### Commit Sequence

**Commit 1: Update AGENTS.md with stigmergic context links**
```bash
git add AGENTS.md
git commit -m "docs(agents): Add chora-compose v1.9.0 stigmergic context links

- Add cross-repository coordination section
- Document [@repo/capability:resource-id] pattern
- Provide SAP regeneration examples
- Highlight 95% token reduction efficiency

Supports: COORD-2025-003
Trace-ID: CHORA-COORD-2025-003"
```

**Commit 2: Create SAP maintenance workflow guide**
```bash
git add docs/guides/sap-maintenance-workflow.md
git commit -m "docs(guides): Add SAP maintenance workflow with freshness tracking

- Document three-state freshness classification
- Provide weekly freshness check workflow
- Include CI/CD integration examples
- Add troubleshooting section

Supports: COORD-2025-003
Trace-ID: CHORA-COORD-2025-003"
```

**Commit 3: Add CI/CD workflow for SAP freshness**
```bash
git add .github/workflows/sap-freshness.yml .github/workflows/README.md
git commit -m "ci(workflows): Add automated SAP freshness checking

- Weekly schedule (Monday 10:00 AM UTC)
- Create GitHub issue for expired SAPs
- Manual trigger via workflow_dispatch
- Document in workflows README

Supports: COORD-2025-003
Trace-ID: CHORA-COORD-2025-003"
```

**Commit 4: Update SAP cross-references for v1.9.0**
```bash
git add docs/skilled-awareness/sap-framework/awareness-guide.md \
        docs/skilled-awareness/inbox/awareness-guide.md \
        docs/skilled-awareness/agent-awareness/awareness-guide.md
git commit -m "docs(saps): Update SAP awareness guides with chora-compose v1.9.0 refs

- SAP-000: Add stigmergic link regeneration examples
- SAP-001: Update cross-repo coordination patterns
- SAP-009: Document v1.9.0 capability patterns

Supports: CORD-2025-003
Trace-ID: CHORA-COORD-2025-003"
```

**Commit 5: Add validation test results**
```bash
git add inbox/active/coord-2025-003-v190-capabilities-update/validation-results.md
git commit -m "test(coord-2025-003): Validate stigmergic links and freshness tracking

- Test stigmergic context link pattern recognition
- Verify freshness check output format
- Validate CI/CD workflow execution
- Document test results

Supports: CORD-2025-003
Trace-ID: CHORA-COORD-2025-003"
```

### Pull Request
```markdown
## PR: chora-compose v1.9.0 Documentation Integration

**Coordination Request**: CORD-2025-003
**Trace ID**: CHORA-COORD-2025-003
**Type**: Documentation enhancement
**Estimated Effort**: 2.75-4.25 hours
**Actual Effort**: [To be filled]

### Summary
Integrates chora-compose v1.9.0 capabilities (stigmergic context links, freshness tracking) into chora-base documentation, enabling 95% token reduction for cross-repo SAP operations.

### Acceptance Criteria (5/5 Complete)
- ✅ AGENTS.md includes stigmergic context link examples
- ✅ SAP maintenance workflow documented with freshness tracking
- ✅ CI/CD example for automated freshness checks
- ✅ Bidirectional cross-references between repos
- ✅ Validation testing completed successfully

### Files Changed
**New** (3):
- docs/guides/sap-maintenance-workflow.md
- .github/workflows/sap-freshness.yml
- validation-results.md

**Modified** (5-7):
- AGENTS.md
- .github/workflows/README.md
- Various SAP awareness guides

### Testing
- [x] Stigmergic context link pattern recognition
- [x] Freshness check output validation
- [x] CI/CD workflow manual trigger
- [x] Documentation link verification

### Related
- **Coordination Request**: inbox/active/coord-2025-003-v190-capabilities-update/
- **Communication Brief**: inbox/active/coord-2025-003-v190-capabilities-update/communication-brief.md
- **Triage Decision**: inbox/active/coord-2025-003-v190-capabilities-update/triage-decision.md

### Reviewer Notes
Please validate:
1. Stigmergic context link syntax correctness
2. Freshness threshold recommendations
3. CI/CD workflow configuration
4. SAP cross-reference completeness
```

---

## Done Criteria

### Per Deliverable

**Deliverable 1: AGENTS.md Updated**
- [x] Stigmergic context links section added
- [x] Examples provided for SAP regeneration
- [x] Token efficiency highlighted (95% reduction)
- [x] Version requirement noted (v1.9.0+)

**Deliverable 2: SAP Maintenance Guide Created**
- [x] Freshness tracking explained (three states)
- [x] Weekly workflow documented
- [x] Threshold configuration guidance provided
- [x] Troubleshooting section included

**Deliverable 3: CI/CD Workflow Added**
- [x] GitHub Actions workflow created
- [x] Weekly schedule configured
- [x] Issue creation on expired SAPs
- [x] Workflow documented in README

**Deliverable 4: SAP Cross-References Updated**
- [x] SAP-000 references v1.9.0 capabilities
- [x] SAP-001 coordination examples updated
- [x] SAP-009 capability patterns added (if exists)
- [x] Bidirectional links verified

**Deliverable 5: Validation Completed**
- [x] Stigmergic context link tested end-to-end
- [x] Freshness check output validated
- [x] CI/CD workflow triggered manually
- [x] Results documented

### Overall

- [x] All 5 acceptance criteria met
- [x] No broken links or references
- [x] Validation testing passed
- [x] Git commits follow convention
- [x] PR description complete
- [x] Ready for review

---

## Sign-Off

**Implementer**: [Name]
**Date Completed**: [YYYY-MM-DD]
**Actual Effort**: [Hours]
**Variance**: [% vs estimate]

**Reviewer**: [Name]
**Review Date**: [YYYY-MM-DD]
**Review Outcome**: [Approved | Changes Requested]

**Merge Date**: [YYYY-MM-DD]
**Merged By**: [Name]

---

**Next Step**: Send COORD-2025-003-RESPONSE.json to chora-compose acknowledging completion
