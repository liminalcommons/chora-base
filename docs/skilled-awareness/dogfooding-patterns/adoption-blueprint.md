# Adoption Blueprint: Dogfooding Patterns

**SAP ID**: SAP-027
**Version**: 1.0.0
**Last Updated**: 2025-11-03

---

## Overview

This blueprint provides step-by-step instructions for adopting SAP-027 Dogfooding Patterns across three progressive levels.

### Adoption Levels

| Level | Approach | Setup Time | Maintenance | Suitable For |
|-------|----------|------------|-------------|--------------|
| **Level 1: Basic** | Simplified pilot (build+validate only) | 3-4 hours | Per pilot | First-time users, quick experiments, low-risk capabilities |
| **Level 2: Advanced** | Full 6-week pilot (research+build+validate+decide) | 6-8 hours | Per pilot | Serious capability validation, medium-risk capabilities |
| **Level 3: Mastery** | Multi-pilot infrastructure with automation | 12-16 hours initial | 1-2 hours/pilot | **Recommended for production** - Ongoing capability development at scale |

**Recommended Path**: Level 1 → Level 2 → Level 3 (progressive adoption)

---

## Level 1: Basic Adoption

### Purpose

Level 1 adoption is suitable for:
- **First-time users** new to dogfooding methodology
- **Quick experiments** validating low-risk capabilities (≤1 week build)
- **Learning the framework** before committing to full pilots
- **Small teams** (1-2 people) without dedicated research capacity
- **Internal tools** with limited blast radius if they fail

Level 1 skips the research phase (Week 0) and GO/NO-GO decision framework, focusing on a simplified build→validate→iterate loop.

### Time Estimate

- **Setup**: 3-4 hours (one-time, per project)
- **Per pilot**: 2-3 weeks (compressed timeline)
- **Learning Curve**: Low (simplified workflow, minimal documentation)

### Prerequisites

**Required**:
- Text editor or IDE for documenting pilot results
- Access to project codebase where capability will be built
- Ability to use capability yourself (dogfooding requires internal use)

**Recommended**:
- SAP-010 (Memory System) for logging pilot events to .chora/memory/events/dogfooding.jsonl
- SAP-015 (Task Tracking) for managing pilot tasks with beads

### Step-by-Step Instructions

#### Step 1.1: Identify Capability to Pilot

**Action**:
Choose a low-risk capability you want to build and validate internally. Ideal Level 1 candidates:
- Simple CLI tools or scripts
- Internal documentation patterns
- Development workflow improvements
- Small automation tasks

Create a simple pilot plan document:
```bash
# Create pilot plan (can be simple text file)
mkdir -p docs/pilots/
cat > docs/pilots/pilot-$(date +%Y-%m-%d)-{capability-name}.md <<EOF
# Pilot: {Capability Name}

## Goal
{What you want to achieve}

## Build Phase (Weeks 1-2)
- [ ] {Build task 1}
- [ ] {Build task 2}

## Validate Phase (Week 3)
- [ ] Use capability 2+ times
- [ ] Collect satisfaction feedback (1-5 scale)
- [ ] Note any bugs or issues

## Decision
- Continue? Yes/No
- Next steps: {What to do after pilot}
EOF
```

**Expected Output**:
```
Created: docs/pilots/pilot-2025-11-06-cli-helper.md
```

**Verification**:
```bash
# Verify pilot plan exists
ls -lh docs/pilots/pilot-*.md
cat docs/pilots/pilot-*.md  # Review content
```

#### Step 1.2: Build the Capability (Weeks 1-2)

**Action**:
Build your capability to minimum viable state. Track your time:
```bash
# Optional: Log start of build phase to A-MEM (if SAP-010 adopted)
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event_type\":\"pilot_build_start\",\"pilot\":\"pilot-2025-11-06-cli-helper\",\"phase\":\"build\"}" >> .chora/memory/events/dogfooding.jsonl

# Build your capability
# {Your actual build commands go here}

# Track time spent (use timer, calendar events, or beads)
```

**Expected Output**:
Working capability that you can use internally (even if rough around the edges).

#### Step 1.3: Validate the Capability (Week 3)

**Action**:
Use your capability at least 2 times in real scenarios. After each use, note:
```bash
# Log each validation use (simple text notes work for Level 1)
cat >> docs/pilots/pilot-2025-11-06-cli-helper.md <<EOF

## Use Case {N}: {Date}
- **Scenario**: {What you used it for}
- **Time saved**: {Estimate, e.g., "5 minutes"}
- **Satisfaction**: {1-5}/5
- **Bugs**: {List any issues}
- **Notes**: {Any other observations}
EOF
```

**Expected Output**:
```markdown
## Use Case 1: 2025-11-07
- **Scenario**: Generated boilerplate for new API endpoint
- **Time saved**: ~10 minutes (vs manual)
- **Satisfaction**: 4/5
- **Bugs**: None
- **Notes**: Would be nice to have more templates

## Use Case 2: 2025-11-08
- **Scenario**: Created test fixtures
- **Time saved**: ~8 minutes
- **Satisfaction**: 4/5
- **Bugs**: Minor: template had typo
- **Notes**: Fixed typo, works great now
```

### Validation

#### Validation Checklist

After completing Level 1, verify:

- [ ] Capability was used at least 2 times in real scenarios
- [ ] Satisfaction ratings collected for each use (1-5 scale)
- [ ] Time savings estimated (even roughly)
- [ ] Any bugs or issues documented
- [ ] Simple decision made: continue vs abandon capability

#### Validation Commands

```bash
# Verify pilot documentation exists
ls docs/pilots/pilot-*.md

# Check that you have at least 2 use cases documented
grep -c "## Use Case" docs/pilots/pilot-*.md
# Expected: 2 or more

# Review pilot results
cat docs/pilots/pilot-$(ls docs/pilots/ | grep pilot- | tail -1)
```

### Common Issues (Level 1)

**Issue 1**: "I don't have time to use the capability 2+ times"
- **Cause**: Capability not solving a real problem you have, or pilot timeline too aggressive
- **Solution**: Choose capabilities you'll naturally use, or extend pilot by 1-2 weeks. Level 1 is flexible!

**Issue 2**: "I'm not sure if the capability is 'good enough' to continue"
- **Cause**: No clear success criteria defined upfront
- **Solution**: For Level 1, simple heuristic: If satisfaction ≥4/5 and you'd use it again → continue. Otherwise → abandon or redesign.

---

## Level 2: Advanced Adoption

### Purpose

Level 2 adoption adds the full 6-week pilot methodology with:
- **Week 0 Research Phase**: Evidence-based research before building (30-40% Level A evidence required)
- **GO/NO-GO Decision Framework**: Data-driven criteria (time savings ≥5x, satisfaction ≥85%, bugs = 0)
- **Formal Metrics Collection**: Structured validation reports, not just notes
- **Integration with Vision (SAP-006)**: Promote successful pilots from Wave 2 → Wave 1
- **ROI Calculation**: Track setup time vs time savings to prove business value

Level 2 is appropriate for medium-risk capabilities where evidence-based decisions matter.

### Time Estimate

- **Setup**: 3-4 hours (incremental from Level 1) - creating research templates, GO/NO-GO frameworks
- **Total from Start**: 6-8 hours
- **Per pilot**: 6 weeks (Week 0 research + Weeks 1-5 pilot phases)

### Prerequisites

**Required**:
- ✅ Level 1 adoption complete (understand basic dogfooding workflow)
- Access to Claude Code, Claude Desktop, or similar AI assistant for Week 0 research
- SAP-010 (Memory System) recommended for logging pilot events

**Recommended**:
- SAP-006 (Vision Synthesis) for strategic alignment scoring
- SAP-015 (Task Tracking) for managing pilot tasks as beads
- SAP-001 (Inbox) for capturing demand signals from coordination requests

### Step-by-Step Instructions

#### Step 2.1: Week -1 Pre-Pilot Discovery (Optional but Recommended)

**Action**:
Before committing to a 6-week pilot, validate that the capability is worth the investment:

```bash
# Query intention inventory for pilot candidates
cat .chora/memory/knowledge/notes/intention-inventory-*.md | grep -A 5 "^## "

# Score candidates using 4 criteria (evidence 40%, alignment 30%, demand 20%, feasibility 10%)
# Target: ≥7.0 weighted score for pilot consideration

# Document selection in pilot-candidates note
mkdir -p .chora/memory/knowledge/notes/
cat > .chora/memory/knowledge/notes/pilot-candidates-$(date +%Y-%m-%d).md <<EOF
# Pilot Candidates: $(date +%Y-%m-%d)

## Selected Candidate
- **Name**: {Capability name}
- **Weighted Score**: {X.X}/10
- **Rationale**: {Why this capability}

## Evidence (Score: X/10)
{Level A/B/C evidence available}

## Strategic Alignment (Score: X/10)
{Wave 1/2 priority}

## User Demand (Score: X/10)
{Coordination requests, user feedback}

## Feasibility (Score: X/10)
{Build estimate, technical risk}
EOF
```

**Expected Output**:
```
Created: .chora/memory/knowledge/notes/pilot-candidates-2025-11-06.md
Selected pilot has ≥7.0 weighted score
```

#### Step 2.2: Week 0 Research Phase

**Action**:
Execute evidence-based research before building:

```bash
# Use research prompt template
cp docs/templates/research-prompt-template.md docs/research/research-prompt-{capability}.md

# Fill in SAP domain context
# Execute research with Claude Code WebSearch or AI assistant

# Save research output (target: 10-20 pages)
# Generated: docs/research/{capability}-research.md

# Validate evidence levels
grep -i "level a\|level b\|level c" docs/research/{capability}-research.md | wc -l
# Target: ≥30% Level A, ≥40% Level B, ≤30% Level C
```

**Expected Output**:
```markdown
Research Report: {Capability Name}

### Executive Summary
- 10-12 bullet takeaways
- "Adopt now vs later" recommendations

### Principles (The Why)
- [Level A] SOLID principles [cite: Agile Manifesto]
- [Level B] Module boundary patterns [cite: Google Engineering]

[...full report structure per protocol-spec Contract 2]
```

#### Step 2.3: Weeks 1-3 Build Phase with Research Integration

**Action**:
Build capability using research insights to inform design:

```bash
# Log build start
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event_type\":\"pilot_build_start\",\"pilot\":\"pilot-2025-11-06-{capability}\",\"phase\":\"build\"}" >> .chora/memory/events/dogfooding.jsonl

# Build capability (cite research decisions in commit messages)
# Example: "Implement singleton pattern per docs/research/{capability}-research.md §3.2"

# Track setup time for ROI calculation
```

**Expected Output**:
Working capability with research-backed design decisions documented in commits.

### Configuration

#### Level 2 Configuration File

If using SAP-010 (Memory System), configure dogfooding event logging:

```yaml
# .chora/config.yaml
memory:
  events:
    dogfooding:
      enabled: true
      file: .chora/memory/events/dogfooding.jsonl
      schema_version: "1.0"
```

Optional: Configure GO/NO-GO criteria (defaults shown):
```yaml
# docs/pilots/go-no-go-criteria.yaml
criteria:
  time_savings:
    target: 5.0  # 5x minimum
    weight: 0.4
  satisfaction:
    target: 85  # 85% minimum (4.25/5)
    weight: 0.3
  bugs:
    target: 0  # Zero critical bugs
    weight: 0.3
```

### Validation

#### Validation Checklist

After completing Level 2, verify:

- [ ] All Level 1 checks still pass
- [ ] Week 0 research completed with ≥30% Level A evidence
- [ ] Weeks 1-3 build phase tracked setup time
- [ ] Week 4 validation has ≥2 adoption cases with metrics
- [ ] GO/NO-GO decision made with data (time savings, satisfaction, bugs)
- [ ] Pilot results logged to .chora/memory/events/dogfooding.jsonl

#### Validation Commands

```bash
# Verify research report exists and has Level A evidence
test -f docs/research/*-research.md && grep -c "Level A" docs/research/*-research.md
# Expected: ≥3 Level A citations

# Verify GO/NO-GO decision document exists
ls docs/pilots/go-no-go-decision-*.md

# Check dogfooding events logged
tail -5 .chora/memory/events/dogfooding.jsonl
```

### Common Issues (Level 2)

**Issue 1**: "Research phase took longer than expected (>2 hours)"
- **Cause**: Trying to research too broadly, or domain has limited Level A evidence
- **Solution**: Narrow research scope to key architectural decisions only. If <30% Level A available, consider whether pilot should proceed (higher risk).

**Issue 2**: "GO/NO-GO criteria not met, but capability feels useful"
- **Cause**: Criteria may be too strict for this capability type, or validation cases weren't representative
- **Solution**: Document as conditional GO with revised criteria, run extended validation (Week 5-6) with more adoption cases.

---

## Level 3: Mastery - **RECOMMENDED**

### Purpose

Level 3 adoption provides **multi-pilot infrastructure at scale** with:
- **Automated Pilot Tracking**: Manage multiple concurrent pilots with status dashboard
- **Vision Integration (SAP-006)**: Auto-promote successful pilots from Wave 2 → Wave 1 based on GO decisions
- **ROI Portfolio View**: Track cumulative time savings across all pilots
- **Template Automation**: Reusable pilot templates and scripts (reduce per-pilot setup from 6h → 1-2h)
- **Strategic Feedback Loops**: Failed pilots inform Wave 2 → Wave 3 demotions

Level 3 is **essential for organizations** running 3+ pilots per quarter or treating dogfooding as continuous capability development process.

### Time Estimate

- **Setup**: 8-12 hours (incremental from Level 2) - building automation scripts, dashboard, templates
- **Total from Start**: 12-16 hours
- **Maintenance**: 1-2 hours per pilot (vs 6-8 hours at Level 2)
- **ROI**: Break-even after 3rd pilot, 5x time savings by 10th pilot

### Prerequisites

**Required**:
- ✅ Level 2 adoption complete (run at least 1 full pilot successfully)
- SAP-006 (Vision Synthesis) for Wave promotion/demotion integration
- SAP-010 (Memory System) for dogfooding event aggregation
- SAP-015 (Task Tracking) recommended for pilot task management

**Recommended**:
- Python 3.9+ for automation scripts
- justfile or make for pilot workflow automation

### Step-by-Step Instructions

#### Step 3.1: Create Pilot Automation Scripts

**Action**:
Create reusable scripts to bootstrap new pilots in seconds:

```bash
# Create scripts directory
mkdir -p scripts/pilots/

# Create pilot bootstrap script
cat > scripts/pilots/start-pilot.sh <<'EOF'
#!/bin/bash
# Usage: ./scripts/pilots/start-pilot.sh "capability-name" "SAP-NNN"

CAPABILITY="$1"
SAP_ID="$2"
DATE=$(date +%Y-%m-%d)

# Create pilot directory structure
mkdir -p docs/pilots/${DATE}-${CAPABILITY}
mkdir -p docs/research/

# Generate pilot plan from template
cp templates/pilot-plan-template.md docs/pilots/${DATE}-${CAPABILITY}/pilot-plan.md
sed -i "s/{CAPABILITY}/${CAPABILITY}/g" docs/pilots/${DATE}-${CAPABILITY}/pilot-plan.md
sed -i "s/{SAP_ID}/${SAP_ID}/g" docs/pilots/${DATE}-${CAPABILITY}/pilot-plan.md

# Log pilot start to A-MEM
echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event_type\":\"pilot_started\",\"pilot\":\"pilot-${DATE}-${CAPABILITY}\",\"sap_id\":\"${SAP_ID}\"}" >> .chora/memory/events/dogfooding.jsonl

echo "✅ Pilot started: docs/pilots/${DATE}-${CAPABILITY}/"
EOF

chmod +x scripts/pilots/start-pilot.sh
```

**Expected Output**:
```bash
$ ./scripts/pilots/start-pilot.sh "advanced-search" "SAP-034"
✅ Pilot started: docs/pilots/2025-11-06-advanced-search/
```

#### Step 3.2: Build Pilot Dashboard

**Action**:
Create Python script to aggregate pilot metrics:

```bash
# Create pilot dashboard script
cat > scripts/pilots/dashboard.py <<'EOF'
#!/usr/bin/env python3
"""Pilot Dashboard - Track all active and completed pilots"""
import json
from pathlib import Path
from collections import defaultdict

def load_pilots():
    pilots = []
    dogfooding_log = Path(".chora/memory/events/dogfooding.jsonl")
    if dogfooding_log.exists():
        with open(dogfooding_log) as f:
            for line in f:
                event = json.loads(line)
                if event["event_type"] in ["pilot_started", "pilot_completed", "pilot_go_decision", "pilot_no_go_decision"]:
                    pilots.append(event)
    return pilots

def print_dashboard(pilots):
    # Group by status
    active = [p for p in pilots if p["event_type"] == "pilot_started"]
    completed = [p for p in pilots if p["event_type"] in ["pilot_go_decision", "pilot_no_go_decision"]]

    print("=" * 60)
    print("PILOT DASHBOARD")
    print("=" * 60)
    print(f"Active Pilots: {len(active)}")
    print(f"Completed Pilots: {len(completed)}")
    print()

    go_count = len([p for p in completed if p["event_type"] == "pilot_go_decision"])
    no_go_count = len([p for p in completed if p["event_type"] == "pilot_no_go_decision"])
    success_rate = (go_count / len(completed) * 100) if completed else 0

    print(f"Success Rate: {success_rate:.0f}% ({go_count} GO, {no_go_count} NO-GO)")
    print()

    print("Recent Pilots:")
    for pilot in pilots[-5:]:
        print(f"  - {pilot.get('pilot', 'Unknown')}: {pilot['event_type']}")

if __name__ == "__main__":
    pilots = load_pilots()
    print_dashboard(pilots)
EOF

chmod +x scripts/pilots/dashboard.py
```

**Expected Output**:
```
============================================================
PILOT DASHBOARD
============================================================
Active Pilots: 2
Completed Pilots: 5

Success Rate: 80% (4 GO, 1 NO-GO)

Recent Pilots:
  - pilot-2025-10-15-advanced-search: pilot_go_decision
  - pilot-2025-10-22-code-generation: pilot_no_go_decision
  [...]
```

#### Step 3.3: Integrate with Vision Synthesis (SAP-006)

**Action**:
Automate Wave promotions/demotions based on pilot outcomes:

```bash
# Create vision integration script
cat > scripts/pilots/sync-to-vision.sh <<'EOF'
#!/bin/bash
# Sync pilot GO/NO-GO decisions to vision document

VISION_FILE=".chora/memory/knowledge/notes/vision-chora-base-$(date +%Y).md"
LATEST_DECISION=$(cat .chora/memory/events/dogfooding.jsonl | grep "pilot_.*_decision" | tail -1)

if [ -z "$LATEST_DECISION" ]; then
  echo "No pilot decisions found"
  exit 1
fi

# Parse decision
PILOT_ID=$(echo $LATEST_DECISION | jq -r '.pilot')
DECISION=$(echo $LATEST_DECISION | jq -r '.event_type' | grep -o "go\|no_go")
SAP_NAME=$(echo $LATEST_DECISION | jq -r '.capability')

if [ "$DECISION" = "go" ]; then
  echo "✅ Promoting $SAP_NAME from Wave 2 → Wave 1"
  # Update vision file (manual edit recommended, script prints suggestion)
  echo "Suggested vision update:"
  echo "  Move '$SAP_NAME' from ## Wave 2 to ## Wave 1"
  echo "  Evidence: Pilot $PILOT_ID met GO criteria"
elif [ "$DECISION" = "no_go" ]; then
  echo "⚠️ Demoting $SAP_NAME from Wave 2 → Wave 3"
  echo "Suggested vision update:"
  echo "  Move '$SAP_NAME' from ## Wave 2 to ## Wave 3"
  echo "  Rationale: Pilot $PILOT_ID failed GO criteria"
fi
EOF

chmod +x scripts/pilots/sync-to-vision.sh
```

**Expected Output**:
```bash
$ ./scripts/pilots/sync-to-vision.sh
✅ Promoting Advanced Search Patterns from Wave 2 → Wave 1
Suggested vision update:
  Move 'Advanced Search Patterns' from ## Wave 2 to ## Wave 1
  Evidence: Pilot pilot-2025-11-06-advanced-search met GO criteria
```

### Production Configuration

#### Level 3 Configuration File

Complete dogfooding infrastructure configuration:

```yaml
# .chora/config.yaml - Production configuration for Level 3
memory:
  events:
    dogfooding:
      enabled: true
      file: .chora/memory/events/dogfooding.jsonl
      schema_version: "1.0"
      retention_days: 730  # 2 years of pilot history

dogfooding:
  level: 3
  automation:
    enabled: true
    scripts_dir: scripts/pilots/
    templates_dir: templates/pilots/
  dashboard:
    enabled: true
    refresh_on_commit: true
  vision_integration:
    enabled: true
    auto_promote: false  # Manual approval recommended
    vision_file: .chora/memory/knowledge/notes/vision-chora-base-2025.md
  go_no_go_criteria:
    time_savings: 5.0
    satisfaction: 85
    bugs: 0
```

### Best Practices (Level 3)

**Best Practice 1**: Run Concurrent Pilots with Staggered Timelines
- **Why**: Avoid Week 4 validation bottlenecks when all pilots need validation simultaneously
- **How**: Start pilots on rotating 2-week schedule (Pilot A Week 0, Pilot B Week 2, Pilot C Week 4)

**Best Practice 2**: Use Pilot Dashboard Daily
- **Why**: Catch pilots falling behind schedule early, maintain momentum
- **How**: Add `python scripts/pilots/dashboard.py` to daily standup or weekly planning

**Best Practice 3**: Archive Completed Pilots After 90 Days
- **Why**: Keep docs/pilots/ directory focused on active work
- **How**: `mv docs/pilots/2025-*-completed docs/pilots/archive/2025-Q4/`

### Validation

#### Validation Checklist

After completing Level 3, verify:

- [ ] All Level 1 and Level 2 checks pass
- [ ] Automation scripts created and executable (start-pilot.sh, dashboard.py, sync-to-vision.sh)
- [ ] Run 1 pilot using automation (verify <2 hour setup vs 6 hour manual)
- [ ] Pilot dashboard shows accurate metrics
- [ ] Vision integration tested (at least 1 GO decision synced)
- [ ] ROI positive (cumulative time saved > setup investment)

#### Validation Commands

```bash
# Verify automation scripts exist
ls -lh scripts/pilots/*.{sh,py}
# Expected: start-pilot.sh, dashboard.py, sync-to-vision.sh

# Test pilot dashboard
python scripts/pilots/dashboard.py
# Should show pilot history

# Verify vision integration
./scripts/pilots/sync-to-vision.sh
# Should suggest wave promotion/demotion

# Check ROI (compare setup time vs time saved)
grep "pilot_go_decision" .chora/memory/events/dogfooding.jsonl | wc -l
# Expected: ≥3 successful pilots for break-even
```

### Common Issues (Level 3)

**Issue 1**: "Automation scripts are too rigid for our specific workflow"
- **Cause**: Scripts designed for chora-base conventions, may not fit all projects
- **Solution**: Fork scripts to scripts/pilots/custom/ and adapt. Keep originals for reference.

**Issue 2**: "Vision file promotion/demotion creates merge conflicts"
- **Cause**: Multiple pilots completing simultaneously trying to update same vision file
- **Solution**: Batch vision updates weekly instead of per-pilot. Use sync-to-vision.sh to generate suggestions, apply manually in batch.

---

## Troubleshooting Guide

### General Troubleshooting

**Problem**: "Pilot is taking longer than expected (>6 weeks)"
- **Symptoms**: Week 4 validation incomplete, build phase extending into Week 5+
- **Diagnosis**:
  ```bash
  # Check pilot timeline
  grep "pilot_build_start\|pilot_validation_start" .chora/memory/events/dogfooding.jsonl | tail -5
  ```
- **Solution**:
  - If build phase too long: Reduce scope, focus on MVP only
  - If validation delayed: Block calendar time, treat as committed work
  - Consider downgrading to Level 1 (simpler workflow)

### Debugging Commands

```bash
# Check SAP-027 adoption status
ls -R docs/pilots/ .chora/memory/events/dogfooding.jsonl scripts/pilots/

# View recent dogfooding events
tail -20 .chora/memory/events/dogfooding.jsonl | jq '.'

# Test pilot automation (Level 3 only)
./scripts/pilots/dashboard.py
./scripts/pilots/sync-to-vision.sh --dry-run
```

### Error Messages

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "No pilot decisions found" (sync-to-vision.sh) | No completed pilots yet, or dogfooding.jsonl missing events | Complete at least 1 pilot through Week 4 decision phase |
| "Research report has <30% Level A evidence" | Domain lacks standards/academic research | Document as risk, proceed with caution or pivot to different capability |

---

## Migration Paths

### From Other Solutions

#### Migrating from Ad-Hoc "Try It and See" Approach

**Overview**: Many teams informally try new tools/patterns without structured validation. SAP-027 adds rigor.

**Steps**:
1. **Inventory existing experiments**: Find undocumented capability experiments from past 6 months
2. **Retroactively document**: Create pilot-YYYY-MM-DD-{capability}.md for any still in use
3. **Prospectively adopt**: Use SAP-027 (start with Level 1) for all new capability experiments

**Validation**:
```bash
# Verify historical experiments documented
ls docs/pilots/pilot-*-retro-*.md
# Count: Should match number of identified experiments

# Verify new experiments use SAP-027
grep "pilot_started" .chora/memory/events/dogfooding.jsonl | wc -l
# Expected: ≥1 new formal pilot
```

### Between Levels

#### From Level 1 to Level 2

**Steps**:
1. Complete Level 1 validation
2. [Upgrade step 1]
3. [Upgrade step 2]
4. Validate Level 2

#### From Level 2 to Level 3

**Steps**:
1. Complete Level 2 validation
2. [Upgrade step 1]
3. [Upgrade step 2]
4. Validate Level 3

---

## Additional Resources

### Documentation

- **SAP-027 Protocol Spec**: [protocol-spec.md](./protocol-spec.md) - Technical contracts
- **SAP-027 Awareness Guide**: [awareness-guide.md](./awareness-guide.md) - AI agent instructions
- **SAP-027 Capability Charter**: [capability-charter.md](./capability-charter.md) - Problem and scope

### External Resources

- [Eating Your Own Dog Food (Wikipedia)](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) - History and examples of dogfooding
- [Google's SRE Book](https://sre.google/workbook/) - SRE approaches to internal validation
- [Evidence Levels in Research (Oxford CEBM)](https://www.cebm.ox.ac.uk/resources/levels-of-evidence) - Framework for evaluating research quality

### Community Support

- GitHub Discussions: [Link to discussions]
- Issue Tracker: [Link to issues]
- Coordination: See [SAP-001 Inbox](../inbox/) for cross-repo support

---

## Adoption Metrics

### Success Criteria by Level

**Level 1 Success**:
- [ ] Completed at least 1 pilot (build + validate)
- [ ] Time estimate: ≤ 4 hours setup + 2-3 weeks pilot
- [ ] Simple decision made (continue vs abandon)

**Level 2 Success**:
- [ ] Completed at least 1 full 6-week pilot (research + build + validate + GO/NO-GO)
- [ ] Time estimate: ≤ 8 hours setup + 6 weeks pilot
- [ ] GO/NO-GO criteria met and documented
- [ ] ≥30% Level A evidence in research phase

**Level 3 Success**:
- [ ] Completed at least 3 pilots using automation
- [ ] Time estimate: ≤ 16 hours initial setup, then 1-2 hours per pilot
- [ ] Pilot dashboard operational
- [ ] Vision integration tested (at least 1 promotion/demotion)
- [ ] ROI positive (time saved > setup investment)

### Time Savings

**Before SAP-027** (ad-hoc validation):
- Pilot setup: ~6-8 hours of manual planning per experiment
- Inconsistent validation approach
- No structured decision framework
- Estimated 30-40% of pilots fail silently (no formal decision)

**After SAP-027 (Level 3)**:
- Pilot setup: 1-2 hours (automated)
- Consistent validation with data-driven decisions
- 100% of pilots reach GO/NO-GO decision
- Time savings: 75-85% on pilot overhead

**Cumulative Savings** (10 pilots):
- Manual: 10 × 6h = 60 hours
- Level 3: 16h setup + (10 × 1.5h) = 31 hours
- **Savings: 29 hours (48%)**

---

## Adoption Comparison

| Aspect | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| **Setup Time** | 3-4 hours | 6-8 hours | 12-16 hours |
| **Per-Pilot Time** | 2-3 weeks | 6 weeks | 1-2 hours setup + 6 weeks |
| **Research Phase** | No | Yes (Week 0) | Yes (automated) |
| **GO/NO-GO Framework** | Informal | Formal | Automated |
| **Vision Integration** | No | Manual | Automated |
| **Features** | Basic (build+validate) | Advanced (research+decide) | Complete (multi-pilot automation) |
| **Production Ready** | No | Partial | **Yes** |
| **Recommended For** | First-timers, experiments | Serious validation | **Production at scale** |

**Target**: Achieve Level 3 for organizations running 3+ pilots per quarter.

---

**Version History**:
- **1.0.0** (2025-11-03): Initial adoption blueprint for Dogfooding Patterns