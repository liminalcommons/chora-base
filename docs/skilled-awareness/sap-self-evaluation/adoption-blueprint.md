# SAP Self-Evaluation - Adoption Blueprint

**Pattern ID**: SAP-019
**Pattern Name**: sap-self-evaluation
**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-10-30

## Overview

This blueprint guides the installation and adoption of SAP Self-Evaluation across three progressive levels:

- **Level 1** (1-2 hours): Basic evaluation capability - quick checks working
- **Level 2** (4-6 hours cumulative): Standard usage - deep dive evaluations, reports generated
- **Level 3** (8-12 hours cumulative): Strategic capability - roadmap generation, tracking over time

## Prerequisites

### Required SAPs

- **SAP-000** (sap-framework) - Must be installed (defines SAP structure)
- **SAP-007** (documentation-framework) - Recommended (report formatting)
- **SAP-009** (agent-awareness) - Recommended (LLM-driven assessment patterns)

### System Requirements

**Python Environment**:
- Python 3.9+ installed
- pip package manager
- Virtual environment (recommended)

**Git Repository**:
- Git version control initialized
- Clean working directory (for tracking adoption events)

**File System Access**:
- Read access to `docs/skilled-awareness/` (SAP metadata)
- Write access to `scripts/`, `utils/` (installation)
- Write access to `docs/adoption-reports/` (output)

### Validation

**Check prerequisites**:
```bash
# Python version
python --version  # Should be 3.9+

# Git initialized
git status  # Should not error

# SAP-000 installed
test -d docs/skilled-awareness/sap-framework && echo "✅ SAP-000 present" || echo "❌ Install SAP-000 first"

# sap-catalog.json exists
test -f sap-catalog.json && echo "✅ Catalog present" || echo "❌ Missing catalog"
```

## Level 1: Basic Evaluation (1-2 hours)

**Goal**: Quick check functionality working for all installed SAPs.

**Time Investment**: 1-2 hours
**Outcome**: Run `sap-evaluator.py --quick` successfully, see status of installed SAPs

### Step 1.1: Install SAP-019 Artifacts (15 minutes)

**Using install-sap.py** (recommended):
```bash
# Install SAP-019
python scripts/install-sap.py SAP-019

# Verify installation
ls docs/skilled-awareness/sap-self-evaluation/
# Expected: capability-charter.md, protocol-spec.md, awareness-guide.md,
#           adoption-blueprint.md, ledger.md, schemas/
```

**Manual installation** (if install-sap.py unavailable):
```bash
# Create directory
mkdir -p docs/skilled-awareness/sap-self-evaluation/schemas

# Copy artifacts from chora-base
# (Download from chora-base repository or copy files)
# Required files:
# - capability-charter.md
# - protocol-spec.md
# - awareness-guide.md
# - adoption-blueprint.md (this file)
# - ledger.md
```

**Validation**:
```bash
# Check all 5 artifacts present
test -f docs/skilled-awareness/sap-self-evaluation/capability-charter.md && \
test -f docs/skilled-awareness/sap-self-evaluation/protocol-spec.md && \
test -f docs/skilled-awareness/sap-self-evaluation/awareness-guide.md && \
test -f docs/skilled-awareness/sap-self-evaluation/adoption-blueprint.md && \
test -f docs/skilled-awareness/sap-self-evaluation/ledger.md && \
echo "✅ All artifacts present" || echo "❌ Missing artifacts"
```

### Step 1.2: Install Core Evaluation Engine (20 minutes)

**Create utils/sap_evaluation.py**:
```bash
# File should be created by install-sap.py
test -f utils/sap_evaluation.py && echo "✅ Engine installed" || echo "⚠️  Need to create manually"
```

**If manual creation needed**, see [utils/sap_evaluation.py](../../../utils/sap_evaluation.py) in chora-base repository.

**Key components**:
```python
# utils/sap_evaluation.py contains:
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import json

@dataclass
class EvaluationResult:
    """Result of SAP evaluation"""
    sap_id: str
    current_level: int
    validation_results: dict[str, bool]
    # ... (see protocol-spec.md for full schema)

class SAPEvaluator:
    """Core evaluation engine"""

    def quick_check(self, sap_id: str) -> EvaluationResult:
        """Level 1: Quick automated checks"""
        pass

    def deep_dive(self, sap_id: str) -> EvaluationResult:
        """Level 2: LLM-driven analysis"""
        pass

    def strategic_analysis(self) -> AdoptionRoadmap:
        """Level 3: Full roadmap generation"""
        pass
```

**Validation**:
```bash
# Test import
python -c "from utils.sap_evaluation import SAPEvaluator; print('✅ Import successful')"
```

### Step 1.3: Install CLI Tool (20 minutes)

**Create scripts/sap-evaluator.py**:
```bash
# File should be created by install-sap.py
test -f scripts/sap-evaluator.py && echo "✅ CLI installed" || echo "⚠️  Need to create manually"
```

**CLI structure**:
```python
#!/usr/bin/env python3
"""
SAP Self-Evaluation CLI Tool

Usage:
  python scripts/sap-evaluator.py --quick [SAP-ID]
  python scripts/sap-evaluator.py --deep SAP-004
  python scripts/sap-evaluator.py --strategic
"""

import argparse
from pathlib import Path
from utils.sap_evaluation import SAPEvaluator

def main():
    parser = argparse.ArgumentParser(description="Evaluate SAP adoption")
    parser.add_argument("--quick", nargs="?", const="all", help="Quick check")
    parser.add_argument("--deep", help="Deep dive for specific SAP")
    parser.add_argument("--strategic", action="store_true", help="Strategic analysis")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()
    evaluator = SAPEvaluator(repo_root=Path.cwd())

    if args.quick:
        # Run quick check
        if args.quick == "all":
            results = evaluator.quick_check_all()
        else:
            results = evaluator.quick_check(args.quick)
        print_quick_results(results)

    elif args.deep:
        # Run deep dive
        result = evaluator.deep_dive(args.deep)
        if args.output:
            save_markdown_report(result, args.output)
        print_deep_results(result)

    elif args.strategic:
        # Run strategic analysis
        roadmap = evaluator.strategic_analysis()
        if args.output:
            save_yaml_roadmap(roadmap, args.output)
        print_roadmap_summary(roadmap)

if __name__ == "__main__":
    main()
```

**Validation**:
```bash
# Test CLI help
python scripts/sap-evaluator.py --help

# Expected output:
# usage: sap-evaluator.py [-h] [--quick [QUICK]] [--deep DEEP] [--strategic]
# ...
```

### Step 1.4: Install JSON Schemas (10 minutes)

**Create schema files**:
```bash
mkdir -p docs/skilled-awareness/sap-self-evaluation/schemas

# Create evaluation-result.json
cat > docs/skilled-awareness/sap-self-evaluation/schemas/evaluation-result.json <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["sap_id", "evaluation_type", "timestamp", "current_level"],
  "properties": {
    "sap_id": {"type": "string", "pattern": "^SAP-[0-9]{3}$"},
    "sap_name": {"type": "string"},
    "evaluation_type": {"enum": ["quick", "deep", "strategic"]},
    "timestamp": {"type": "string", "format": "date-time"},
    "current_level": {"type": "integer", "minimum": 0, "maximum": 3},
    "completion_percent": {"type": "number", "minimum": 0, "maximum": 100},
    "validation_results": {"type": "object"},
    "gaps": {"type": "array"},
    "recommended_actions": {"type": "array"}
  }
}
EOF
```

**Validation**:
```bash
ls docs/skilled-awareness/sap-self-evaluation/schemas/
# Expected: evaluation-result.json, gap.json, action.json
```

### Step 1.5: Run First Quick Check (10 minutes)

**Test on SAP-000** (framework, should always be installed):
```bash
# Run quick check
python scripts/sap-evaluator.py --quick SAP-000
```

**Expected output**:
```
SAP-000 (sap-framework) - Quick Check
======================================
✅ Installed (5/5 artifacts present)
✅ sap-catalog.json exists
✅ SAP governance documented

Current Level: 1
Next Milestone: Level 2 (adopt 10+ SAPs)
Estimated Effort: Varies

Run deep dive for detailed analysis:
  python scripts/sap-evaluator.py --deep SAP-000
```

**If errors occur**, check:
- Python path issues (`PYTHONPATH` includes repo root)
- Missing dependencies (`pip install -r requirements.txt`)
- File permissions (scripts executable)

### Step 1.6: Update AGENTS.md (15 minutes)

**Add to AGENTS.md** (or create if missing):
```markdown
## SAP Self-Evaluation

**Purpose**: Assess SAP adoption depth, identify gaps, generate improvement roadmaps.

### Quick Usage

**Check adoption status**:
```bash
python scripts/sap-evaluator.py --quick
```

**Evaluate specific SAP**:
```bash
python scripts/sap-evaluator.py --deep SAP-004
```

### When to Use

- Sprint planning (generate adoption roadmap)
- After installing new SAP (validate installation)
- Quarterly reviews (track progress over time)
- User asks "How's our SAP adoption?"

### Key Files

- `scripts/sap-evaluator.py` - CLI tool
- `utils/sap_evaluation.py` - Core engine
- `docs/skilled-awareness/sap-self-evaluation/` - Documentation
```

**Validation**:
```bash
grep -q "SAP Self-Evaluation" AGENTS.md && echo "✅ AGENTS.md updated" || echo "❌ Add section to AGENTS.md"
```

### Step 1.7: Commit Installation (10 minutes)

**Create git commit**:
```bash
# Stage files
git add docs/skilled-awareness/sap-self-evaluation/
git add scripts/sap-evaluator.py
git add utils/sap_evaluation.py
git add AGENTS.md

# Commit
git commit -m "feat(sap-019): Install SAP Self-Evaluation (Level 1)

- Add evaluation framework artifacts (5 docs)
- Install CLI tool (sap-evaluator.py)
- Install core engine (utils/sap_evaluation.py)
- Update AGENTS.md with usage guidance

Quick check now available for all installed SAPs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Validation**:
```bash
git log -1 --oneline | grep -q "sap-019" && echo "✅ Committed" || echo "❌ Commit failed"
```

---

## Level 2: Standard Usage (4-6 hours cumulative)

**Goal**: Deep dive evaluations working, markdown reports generated, gaps prioritized.

**Time Investment**: +3-4 hours (4-6 hours total)
**Outcome**: Generate detailed assessment reports, identify actionable improvements

### Step 2.1: Install LLM Prompt Templates (20 minutes)

**Create template directory**:
```bash
mkdir -p scripts/templates
```

**Create quick-check-prompt.md**:
```bash
cat > scripts/templates/quick-check-prompt.md <<'EOF'
# Quick Check Evaluation Prompt

Evaluate {sap_id} ({sap_name}) installation and basic validation.

## Context
- Repository: {repo_root}
- Installed SAPs: {installed_count}
- Evaluation type: Quick check (automated)

## Tasks
1. Verify 5 artifacts present in docs/skilled-awareness/{sap_dir}/
2. Run validation commands from protocol-spec.md
3. Determine adoption level (0/1/2/3) based on results
4. Identify immediate blockers (if any)

## Output Format
```json
{
  "sap_id": "{sap_id}",
  "current_level": 0,
  "validation_results": {
    "artifacts_complete": false,
    "validation_1": false
  },
  "blockers": []
}
```
EOF
```

**Create deep-dive-prompt.md** (similar structure, more detailed).

**Validation**:
```bash
ls scripts/templates/
# Expected: quick-check-prompt.md, deep-dive-prompt.md, strategic-analysis-prompt.md
```

### Step 2.2: Enhance Evaluation Engine with LLM Support (1 hour)

**Extend utils/sap_evaluation.py** to support LLM-driven analysis:

```python
# Add to SAPEvaluator class

def deep_dive(self, sap_id: str, llm_model: str = "claude-3-5-sonnet") -> EvaluationResult:
    """
    Level 2: LLM-driven content analysis

    Process:
    1. Read adoption criteria from adoption-blueprint.md
    2. Run quick check first (automated validation)
    3. Read relevant files (AGENTS.md, tests/, etc.)
    4. Send to LLM for gap analysis
    5. Parse LLM response, structure gaps
    6. Prioritize by impact × effort
    7. Generate actionable recommendations
    """

    # 1. Load SAP metadata
    sap = self.get_sap_metadata(sap_id)

    # 2. Run quick check
    quick_result = self.quick_check(sap_id)

    # 3. Read adoption criteria
    criteria = self.load_adoption_criteria(sap_id)

    # 4. Read relevant files
    files_content = self.read_relevant_files(sap_id)

    # 5. Generate LLM prompt
    prompt = self.generate_deep_dive_prompt(
        sap_id=sap_id,
        quick_results=quick_result,
        criteria=criteria,
        files=files_content
    )

    # 6. Call LLM (Note: Requires LLM API access)
    # For now, this is a placeholder - actual implementation
    # would integrate with Claude API or other LLM
    llm_response = self.call_llm(prompt, model=llm_model)

    # 7. Parse response into structured EvaluationResult
    result = self.parse_llm_response(llm_response)

    return result
```

**Note**: LLM integration requires API credentials. For Level 2, focus on structure. Level 3 adds actual LLM calls.

### Step 2.3: Generate First Deep Dive Report (30 minutes)

**Run deep dive on installed SAP**:
```bash
# Choose a SAP you have installed (e.g., SAP-004, SAP-009, SAP-013)
python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
```

**Review generated report** (should include):
- Current adoption level
- Level 1/2/3 completion percentages
- Prioritized gaps (P0/P1/P2)
- Concrete actions with time estimates
- Sprint recommendations

**Example report structure**:
```markdown
# SAP-004 (Testing Framework) - Deep Dive Assessment
**Generated**: 2025-10-30 16:00:00
**Evaluation Time**: 4.2 minutes

## Current State
- **Adoption Level**: 1 (Basic)
- **Level 2 Completion**: 45%

## Validation Results
✅ Artifacts complete
❌ Coverage below 85%

## Gap Analysis
### Gap 1: Coverage Below Target (P0)
**Actions**:
1. Generate coverage report (5 min)
2. Write 8 tests (3 hours)
3. Validate ≥85% (2 min)

**Total Effort**: 3 hours
```

**Validation**:
```bash
test -f docs/adoption-reports/SAP-004-assessment.md && echo "✅ Report generated" || echo "❌ Generation failed"
```

### Step 2.4: Create Adoption Reports Directory (10 minutes)

**Set up report storage**:
```bash
# Create directory
mkdir -p docs/adoption-reports

# Create README
cat > docs/adoption-reports/README.md <<'EOF'
# SAP Adoption Reports

This directory contains evaluation reports generated by SAP-019 (Self-Evaluation).

## Report Types

- **{SAP-ID}-assessment.md** - Deep dive evaluation (5 min analysis)
- **sap-roadmap.yaml** - Strategic adoption roadmap (quarterly)
- **Q{X}-{YEAR}-review.md** - Quarterly progress review

## Usage

**Generate report**:
```bash
python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
```

**Review reports**:
```bash
ls -lt docs/adoption-reports/  # Newest first
```

## Tracking

Reports are git-tracked to show adoption progress over time.
EOF
```

**Validation**:
```bash
test -d docs/adoption-reports && echo "✅ Directory created" || echo "❌ Failed"
```

### Step 2.5: Add Report Generation to Workflow (20 minutes)

**Update AGENTS.md workflow**:
```markdown
## SAP Evaluation Workflow

### When User Asks "How can we improve SAP-X?"

1. **Run deep dive**:
   ```bash
   python scripts/sap-evaluator.py --deep SAP-X --output docs/adoption-reports/SAP-X-assessment.md
   ```

2. **Read report** (use Read tool):
   ```
   Read: docs/adoption-reports/SAP-X-assessment.md
   ```

3. **Extract top 3 gaps** from report

4. **Present to user**:
   - Gap 1 (P0): Title, actions, effort
   - Gap 2 (P1): ...
   - Gap 3 (P2): ...

5. **Offer to execute**: "Shall I create tasks and implement Gap 1?"
```

### Step 2.6: Test on 3 Different SAPs (45 minutes)

**Run evaluations on diverse SAPs**:
```bash
# SAP-004 (Testing) - Technical capability
python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md

# SAP-009 (Agent Awareness) - Documentation quality
python scripts/sap-evaluator.py --deep SAP-009 --output docs/adoption-reports/SAP-009-assessment.md

# SAP-013 (Metrics) - Process integration
python scripts/sap-evaluator.py --deep SAP-013 --output docs/adoption-reports/SAP-013-assessment.md
```

**Review each report** for:
- Accuracy (gaps match reality)
- Actionability (concrete steps, not vague advice)
- Prioritization (P0 gaps truly block progress)

**Refine prompts** based on findings:
- If gaps are vague → Add more specific criteria to prompts
- If priorities wrong → Adjust impact/effort scoring
- If actions unhelpful → Improve action generation logic

### Step 2.7: Commit Level 2 Adoption (15 minutes)

```bash
git add docs/adoption-reports/
git add scripts/templates/
git add utils/sap_evaluation.py  # Enhanced version
git add AGENTS.md  # Updated workflow

git commit -m "feat(sap-019): Achieve Level 2 adoption (deep dive capability)

- Add LLM prompt templates (quick/deep/strategic)
- Enhance evaluation engine with gap analysis
- Generate 3 assessment reports (SAP-004, SAP-009, SAP-013)
- Add report storage (docs/adoption-reports/)
- Update AGENTS.md with evaluation workflow

Deep dive evaluations now operational.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Level 3: Strategic Capability (8-12 hours cumulative)

**Goal**: Generate quarterly roadmaps, track adoption over time, integrate with planning.

**Time Investment**: +4-6 hours (8-12 hours total)
**Outcome**: Strategic roadmaps guide SAP adoption, progress visible quarter-over-quarter

### Step 3.1: Install Timeline Tracking (30 minutes)

**Create adoption-history.jsonl**:
```bash
# Initialize event log
touch adoption-history.jsonl

# Add initial event
echo '{"event_type": "evaluation_system_initialized", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "saps_installed": 12}' >> adoption-history.jsonl
```

**Create tracking utilities**:
```python
# Add to utils/sap_evaluation.py

def log_adoption_event(event_type: str, **kwargs):
    """Log SAP adoption event to JSONL timeline"""
    event = {
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **kwargs
    }

    with open("adoption-history.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")

def analyze_adoption_timeline() -> dict:
    """Parse adoption-history.jsonl for trends"""
    events = []
    with open("adoption-history.jsonl") as f:
        for line in f:
            events.append(json.loads(line))

    # Calculate metrics
    saps_per_month = calculate_velocity(events)
    time_to_level_2 = calculate_avg_time_to_level(events, target_level=2)

    return {
        "velocity": saps_per_month,
        "time_to_level_2_avg_days": time_to_level_2
    }
```

**Validation**:
```bash
test -f adoption-history.jsonl && echo "✅ Timeline tracking initialized" || echo "❌ Failed"
```

### Step 3.2: Implement Strategic Analysis (2 hours)

**Enhance SAPEvaluator.strategic_analysis()**:

```python
def strategic_analysis(
    self,
    quarterly_goals: Optional[dict] = None,
    include_history: bool = True
) -> AdoptionRoadmap:
    """
    Level 3: Comprehensive roadmap generation

    Process:
    1. Evaluate all installed SAPs (quick check)
    2. Calculate aggregate metrics (distribution, avg level)
    3. Analyze timeline (git history + events.jsonl)
    4. Identify cross-SAP dependencies
    5. Prioritize gaps globally (impact × blockers)
    6. Generate sprint breakdown
    7. Project ROI (integrate with SAP-013)
    8. Output YAML roadmap
    """

    # 1. Quick check all SAPs
    all_results = self.quick_check_all()

    # 2. Aggregate metrics
    total_installed = len([r for r in all_results if r.is_installed])
    level_distribution = self.calculate_level_distribution(all_results)
    avg_level = sum(r.current_level for r in all_results) / total_installed

    # 3. Timeline analysis (if enabled)
    timeline_metrics = {}
    if include_history:
        timeline_metrics = self.analyze_adoption_timeline()

    # 4. Dependency analysis
    dependencies = self.analyze_dependencies(all_results)

    # 5. Global gap prioritization
    all_gaps = self.collect_all_gaps(all_results)
    prioritized = self.prioritize_gaps_globally(all_gaps, dependencies)

    # 6. Sprint breakdown
    this_sprint, next_sprint, future = self.generate_sprint_plans(prioritized)

    # 7. ROI projection
    roi_projection = self.project_roi(all_results, prioritized)

    # 8. Build roadmap
    roadmap = AdoptionRoadmap(
        generated_at=datetime.now(),
        target_quarter=self.calculate_next_quarter(),
        total_saps_installed=total_installed,
        adoption_distribution=level_distribution,
        average_adoption_level=avg_level,
        priority_gaps=prioritized[:10],  # Top 10
        this_sprint=this_sprint,
        next_sprint=next_sprint,
        future_sprints=future,
        **timeline_metrics,
        **roi_projection
    )

    return roadmap
```

### Step 3.3: Generate First Strategic Roadmap (45 minutes)

**Run strategic analysis**:
```bash
python scripts/sap-evaluator.py --strategic --output project-docs/sap-roadmap.yaml
```

**Expected output** (YAML):
```yaml
# SAP Adoption Roadmap
# Generated: 2025-10-30T17:00:00Z

metadata:
  generated_at: 2025-10-30T17:00:00Z
  target_quarter: Q1-2026
  next_review_date: 2026-01-15

current_state:
  total_saps_installed: 12
  adoption_percentage: 67%
  distribution:
    level_1: 10
    level_2: 2
    level_3: 0
  average_adoption_level: 1.17

priority_gaps:
  - rank: 1
    sap_id: SAP-004
    gap_title: "Coverage below 85%"
    priority_score: 0.85
    sprint: current
    estimated_hours: 3

sprints:
  current_sprint:
    name: "Sprint 23"
    focus_saps: [SAP-004, SAP-013]
    total_estimated_hours: 4
```

**Review roadmap** for:
- Accuracy (matches current state)
- Prioritization (most impactful gaps first)
- Feasibility (sprint estimates realistic)

### Step 3.4: Integrate with SAP-013 Metrics (30 minutes)

**Extend SAP-013 ClaudeROICalculator**:

```python
# Add to utils/claude_metrics.py (if SAP-013 installed)

@dataclass
class SAPAdoptionMetric:
    """Track SAP adoption progress"""
    sap_id: str
    adoption_level: int
    hours_invested: float
    estimated_hours_saved: float
    timestamp: datetime

class ClaudeROICalculator:
    # Existing methods...

    def track_sap_adoption(self, metric: SAPAdoptionMetric):
        """Add SAP adoption to ROI tracking"""
        self.sap_adoption_metrics.append(metric)

    def generate_sap_adoption_report(self) -> str:
        """Include SAP adoption in ROI analysis"""
        total_invested = sum(m.hours_invested for m in self.sap_adoption_metrics)
        total_saved = sum(m.estimated_hours_saved for m in self.sap_adoption_metrics)
        roi = total_saved / total_invested if total_invested > 0 else 0

        return f"""
## SAP Adoption ROI

**Investment**: {total_invested:.1f} hours (SAP learning & integration)
**Return**: {total_saved:.1f} hours (productivity gains from SAPs)
**ROI**: {roi:.2f}x

**Adopted SAPs**: {len(self.sap_adoption_metrics)}
**Average Level**: {sum(m.adoption_level for m in self.sap_adoption_metrics) / len(self.sap_adoption_metrics):.1f}
"""
```

**Validation**:
```python
# Test integration (if SAP-013 installed)
from utils.claude_metrics import ClaudeROICalculator

calc = ClaudeROICalculator()
calc.track_sap_adoption(SAPAdoptionMetric(
    sap_id="SAP-004",
    adoption_level=2,
    hours_invested=3.5,
    estimated_hours_saved=12.0,
    timestamp=datetime.now()
))

print(calc.generate_sap_adoption_report())
# Should show ROI calculation
```

### Step 3.5: Create Quarterly Review Process (30 minutes)

**Add to AGENTS.md**:
```markdown
## Quarterly SAP Adoption Review

**When**: End of each quarter (Q1: Mar, Q2: Jun, Q3: Sep, Q4: Dec)

**Process**:
1. **Generate roadmap**:
   ```bash
   python scripts/sap-evaluator.py --strategic --output project-docs/sap-roadmap-Q{X}-{YEAR}.yaml
   ```

2. **Create review document**:
   ```bash
   python scripts/sap-evaluator.py --strategic --format md --output docs/adoption-reports/Q{X}-{YEAR}-review.md
   ```

3. **Analyze progress**:
   - Compare to previous quarter
   - Calculate velocity (SAPs/month, levels/month)
   - Identify successes and blockers

4. **Update goals**:
   - Set targets for next quarter
   - Prioritize 3-5 focus SAPs
   - Estimate ROI potential

5. **Commit review**:
   ```bash
   git add project-docs/sap-roadmap-Q{X}-{YEAR}.yaml
   git add docs/adoption-reports/Q{X}-{YEAR}-review.md
   git commit -m "docs(sap-019): Q{X}-{YEAR} adoption review"
   ```
```

### Step 3.6: Set Up Dashboard Generation (1.5 hours)

**Create HTML dashboard template**:
```bash
mkdir -p scripts/templates/dashboard
```

**Create basic dashboard** (scripts/generate-dashboard.py):
```python
#!/usr/bin/env python3
"""Generate HTML adoption dashboard"""

def generate_dashboard(roadmap: AdoptionRoadmap) -> str:
    """Generate HTML dashboard from roadmap"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SAP Adoption Dashboard</title>
    <style>
        body {{ font-family: sans-serif; margin: 40px; }}
        .metric {{ display: inline-block; margin: 20px; padding: 20px;
                  border: 1px solid #ccc; border-radius: 5px; }}
        .metric h3 {{ margin-top: 0; }}
        .metric .value {{ font-size: 2em; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>SAP Adoption Dashboard</h1>
    <p>Generated: {roadmap.generated_at}</p>

    <div class="metrics">
        <div class="metric">
            <h3>Total SAPs</h3>
            <div class="value">{roadmap.total_saps_installed}/18</div>
        </div>
        <div class="metric">
            <h3>Average Level</h3>
            <div class="value">{roadmap.average_adoption_level:.1f}</div>
        </div>
        <div class="metric">
            <h3>ROI</h3>
            <div class="value">{roadmap.current_roi:.1f}x</div>
        </div>
    </div>

    <h2>Priority Gaps</h2>
    <ol>
    """

    for gap in roadmap.priority_gaps[:5]:
        html += f"<li><strong>{gap.sap_id}</strong>: {gap.gap.title} (P{gap.gap.priority})</li>"

    html += """
    </ol>
</body>
</html>
    """

    return html
```

**Generate dashboard**:
```bash
python scripts/sap-evaluator.py --strategic --dashboard --output adoption-dashboard.html
```

**Open in browser**:
```bash
open adoption-dashboard.html  # macOS
# or: xdg-open adoption-dashboard.html  # Linux
# or: start adoption-dashboard.html  # Windows
```

### Step 3.7: Commit Level 3 Adoption (15 minutes)

```bash
git add adoption-history.jsonl
git add project-docs/sap-roadmap.yaml
git add scripts/generate-dashboard.py
git add adoption-dashboard.html
git add utils/sap_evaluation.py  # Strategic analysis added
git add utils/claude_metrics.py  # SAP-013 integration (if installed)
git add AGENTS.md  # Quarterly review process

git commit -m "feat(sap-019): Achieve Level 3 adoption (strategic capability)

- Add timeline tracking (adoption-history.jsonl)
- Implement strategic analysis (roadmap generation)
- Generate first quarterly roadmap (project-docs/sap-roadmap.yaml)
- Integrate with SAP-013 metrics (adoption ROI)
- Add quarterly review process to AGENTS.md
- Create HTML dashboard generator

Strategic roadmap capability operational.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Post-Installation

### Update Ledger

**Record adoption in ledger.md**:
```bash
# Add entry to docs/skilled-awareness/sap-self-evaluation/ledger.md

## 7. Changelog

### 2025-10-30 - Level 3 Adoption Achieved
**Repository**: chora-base
**Adoption Level**: 3 (Strategic capability)
**Time Invested**: 10 hours (1.5h Level 1 + 3.5h Level 2 + 5h Level 3)

**Milestones**:
- Level 1: Quick check operational (1.5 hours)
- Level 2: Deep dive reports generated (4.5 hours total)
- Level 3: Strategic roadmap created (10 hours total)

**Outcomes**:
- 12 SAPs evaluated with quick check
- 3 deep dive assessments completed (SAP-004, SAP-009, SAP-013)
- First quarterly roadmap generated (Q1-2026 targets)
- ROI tracking integrated with SAP-013

**Next Steps**:
- Run quarterly reviews (every 3 months)
- Evaluate new SAPs as they're installed
- Refine LLM prompts based on accuracy feedback
```

### Validation Commands

**Full system check**:
```bash
# Level 1: Quick check works
python scripts/sap-evaluator.py --quick && echo "✅ Level 1 operational"

# Level 2: Deep dive works
python scripts/sap-evaluator.py --deep SAP-000 --output /tmp/test-report.md && \
test -f /tmp/test-report.md && echo "✅ Level 2 operational"

# Level 3: Strategic analysis works
python scripts/sap-evaluator.py --strategic --output /tmp/test-roadmap.yaml && \
test -f /tmp/test-roadmap.yaml && echo "✅ Level 3 operational"
```

### Update sap-catalog.json

**Add SAP-019 to catalog** (if not already present):
```json
{
  "id": "SAP-019",
  "name": "sap-self-evaluation",
  "status": "active",
  "version": "1.0.0",
  "location": "docs/skilled-awareness/sap-self-evaluation",
  "dependencies": ["SAP-000"],
  "capabilities": [
    "Progressive SAP adoption evaluation",
    "Gap identification and prioritization",
    "Strategic roadmap generation",
    "Timeline tracking and trend analysis"
  ],
  "phase": "wave-3",
  "priority": 85,
  "size_kb": 150
}
```

## Troubleshooting

### Issue: CLI tool not found

**Symptom**: `python scripts/sap-evaluator.py` fails with "No such file"

**Solution**:
```bash
# Check file exists
ls scripts/sap-evaluator.py

# If missing, reinstall
python scripts/install-sap.py SAP-019

# Or create manually from chora-base repository
```

### Issue: Import error (utils.sap_evaluation)

**Symptom**: `ModuleNotFoundError: No module named 'utils.sap_evaluation'`

**Solution**:
```bash
# Check PYTHONPATH includes repo root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or run from repo root
cd /path/to/repo
python scripts/sap-evaluator.py --quick
```

### Issue: LLM analysis fails

**Symptom**: Deep dive returns "LLM analysis failed"

**Solution**:
```bash
# Fallback to quick check
python scripts/sap-evaluator.py --quick SAP-004

# For deep dive, ensure LLM API configured
# (Level 2 may require API keys - see protocol-spec.md)
```

### Issue: Roadmap generation timeout

**Symptom**: Strategic analysis takes >30 minutes

**Solution**:
```bash
# Reduce scope: Evaluate fewer SAPs
python scripts/sap-evaluator.py --strategic --saps SAP-004,SAP-009,SAP-013

# Or skip history analysis
python scripts/sap-evaluator.py --strategic --no-history
```

## Success Criteria

**Level 1 Complete** when:
- [ ] All 5 artifacts present in `docs/skilled-awareness/sap-self-evaluation/`
- [ ] CLI tool runs: `python scripts/sap-evaluator.py --quick`
- [ ] Quick check completes in <30 seconds for all installed SAPs
- [ ] AGENTS.md updated with usage guidance
- [ ] Installation committed to git

**Level 2 Complete** when:
- [ ] Deep dive generates markdown report
- [ ] Report contains prioritized gaps (P0/P1/P2)
- [ ] Actions are concrete (tool, file, location, content)
- [ ] 3+ assessment reports generated and reviewed
- [ ] Reports stored in `docs/adoption-reports/`

**Level 3 Complete** when:
- [ ] Strategic analysis generates YAML roadmap
- [ ] Roadmap includes sprint breakdown (this/next/future)
- [ ] Timeline tracking active (`adoption-history.jsonl`)
- [ ] Integration with SAP-013 (if installed)
- [ ] Quarterly review process documented in AGENTS.md
- [ ] HTML dashboard generated

## Next Steps

After Level 3 adoption:

1. **Run quarterly reviews** (every 3 months)
2. **Evaluate new SAPs** as they're installed
3. **Refine prompts** based on evaluation accuracy
4. **Share roadmaps** with stakeholders
5. **Track ROI** (SAP-013 integration)
6. **Contribute improvements** back to chora-base

## Additional Resources

- [Protocol Specification](protocol-spec.md) - Detailed API and data models
- [Awareness Guide](awareness-guide.md) - Agent-specific usage patterns
- [Capability Charter](capability-charter.md) - Problem statement and scope
- [chora-base SAP Framework](../sap-framework/) - Foundational SAP concepts
