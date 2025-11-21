# Adoption Blueprint: Actionable Quality Infrastructure

**Capability ID**: SAP-054
**Modern Namespace**: chora.quality.actionable_infrastructure
**Type**: Meta-Pattern
**Status**: Draft
**Version**: 1.0.0
**Last Updated**: 2025-11-20

---

## Overview

This blueprint provides step-by-step guidance for adopting **SAP-054: Actionable Quality Infrastructure** patterns across quality feedback loops.

**Purpose**: Transform quality checks from L0 (DETECT-only) to L4 (PREVENT-integrated) via incremental adoption.

**Adoption Path**:
- **L0 → L1**: Add CLASSIFICATION (2x toil reduction) - 2-3 hours per check
- **L1 → L2**: Add REMEDIATION (5x reduction) - 4-6 hours per check
- **L2 → L3**: Add TRACKING (1.2x improvement) - 2-3 hours per check
- **L3 → L4**: Add PREVENTION (1.3x improvement) - 2-4 hours per check

**Total Time Investment**: 10-16 hours per quality check (L0→L4)
**Expected ROI**: 430-650% over 12 months

---

## Quick Reference: Adoption Levels

| Level | Phase Added | Toil Reduction | Time Investment | Key Deliverable |
|-------|-------------|----------------|-----------------|-----------------|
| **L0** | DETECT only | Baseline | 0 hours | Detection script exists |
| **L1** | CLASSIFY | 2x (50% reduction) | 2-3 hours | JSON output with classifications |
| **L2** | REMEDIATE | 5x (80% reduction) | 4-6 hours | Auto-fix scripts + justfile recipes |
| **L3** | TRACK | 1.2x (20% improvement) | 2-3 hours | Metrics tracking + trend analysis |
| **L4** | PREVENT | 1.3x (30% improvement) | 2-4 hours | Pre-commit hook integration |

**Overall L0→L4**: 15-20x improvement over 12 months

---

## L0 → L1: Adding CLASSIFICATION

### Overview

**Goal**: Categorize each violation as auto-fixable, requires investigation, or false positive.

**Input**: Quality check at L0 (script produces list of violations)
**Output**: Same violations + classification metadata (JSON format)

**Benefits**:
- 50% reduction in triage time
- Clear action path for each violation
- Data for L2 prioritization

**Time Estimate**: 2-3 hours per quality check

---

### Prerequisites

Before starting L1 adoption:

- ✅ **L0 operational**: Detection script runs and produces violations
- ✅ **Quality check documented**: Agents know what check does and how to run it
- ✅ **Python 3.9+** installed (for JSON output)

**Validation**:
```bash
# Your quality check should produce output like:
python scripts/quality-check.py
# → List of violations (text format is OK for L0)
```

---

### Implementation Steps

#### Step 1.1: Define Classification Rules (30 minutes)

Create classification logic based on violation characteristics.

**Example** (manifest discovery):
```python
# scripts/manifest-discover.py

def classify_untracked_feature(feature_data: dict) -> dict:
    """
    Classify untracked feature as auto-fixable, investigation, or false-positive

    Classification Rules:
    1. False Positive: Feature already in manifest (cross-reference failed)
    2. Auto-fixable: Clear deliverables (commits > 10, notes > 0, no ambiguity)
    3. Investigation: Unclear boundaries or event-only features
    """
    feature_id = feature_data['id']
    evidence = feature_data.get('evidence', {})

    # Rule 1: Check if already documented
    if feature_exists_in_manifest(feature_id):
        return {
            "category": "false_positive",
            "reason": f"Feature {feature_id} already documented in manifest at line {get_manifest_line(feature_id)}",
            "auto_action": "skip",
            "suggestion": "Cross-reference check failed to find existing entry"
        }

    # Rule 2: Check for clear deliverables
    commits = evidence.get('commits', 0)
    notes = evidence.get('notes', 0)
    events = evidence.get('events', 0)

    if commits > 10 and notes > 0:
        return {
            "category": "auto_fixable",
            "reason": f"Feature has clear deliverables: {commits} commits, {notes} notes",
            "auto_action": "add_to_manifest",
            "suggestion": "Generate manifest entry from commits and notes"
        }

    # Rule 3: Default to investigation
    return {
        "category": "investigation",
        "reason": f"Unclear feature boundaries: {commits} commits, {notes} notes, {events} events",
        "auto_action": "none",
        "suggestion": "Manual review needed to determine feature scope"
    }
```

**Customization**: Adapt classification rules to your quality check's domain.

---

#### Step 1.2: Update Detection Script to Output JSON (45 minutes)

Modify existing detection script to include classification metadata.

**Before** (L0 - text output):
```python
# scripts/quality-check.py
def main():
    violations = detect_violations()

    for v in violations:
        print(f"❌ VIOLATION: {v['id']} - {v['description']}")
```

**After** (L1 - JSON output):
```python
# scripts/quality-check.py
import json

def main():
    violations = detect_violations()

    results = {
        "check_name": "manifest-discovery",
        "phase": "CLASSIFY",
        "timestamp": datetime.now().isoformat(),
        "violations": []
    }

    for v in violations:
        classification = classify_violation(v)
        results["violations"].append({
            "id": v['id'],
            "description": v['description'],
            "classification": classification
        })

    # Print JSON output
    print(json.dumps(results, indent=2))

    # Also print human-readable summary
    print("\n--- SUMMARY ---", file=sys.stderr)
    auto_fixable = sum(1 for v in results['violations'] if v['classification']['category'] == 'auto_fixable')
    investigation = sum(1 for v in results['violations'] if v['classification']['category'] == 'investigation')
    false_positive = sum(1 for v in results['violations'] if v['classification']['category'] == 'false_positive')

    print(f"Auto-fixable: {auto_fixable}", file=sys.stderr)
    print(f"Investigation: {investigation}", file=sys.stderr)
    print(f"False Positive: {false_positive}", file=sys.stderr)
```

**Schema**: See [protocol-spec.md](protocol-spec.md) Phase 2 (CLASSIFY) for JSON schema.

---

#### Step 1.3: Update Weekly Health Check (30 minutes)

Integrate classification summary into your weekly health check.

**Example** (justfile):
```makefile
# justfile

# Weekly health check with classification
weekly-health:
    @echo "=== Quality Check: Manifest Discovery ==="
    @python scripts/manifest-discover.py > /tmp/manifest-results.json
    @echo "Auto-fixable: $(cat /tmp/manifest-results.json | jq '.violations | map(select(.classification.category == "auto_fixable")) | length')"
    @echo "Investigation: $(cat /tmp/manifest-results.json | jq '.violations | map(select(.classification.category == "investigation")) | length')"
    @echo "False Positive: $(cat /tmp/manifest-results.json | jq '.violations | map(select(.classification.category == "false_positive")) | length')"
    @echo ""
    @echo "=== Next Steps ==="
    @echo "1. Review auto-fixable violations (ready for L2 automation)"
    @echo "2. Investigate unclear violations"
    @echo "3. Update cross-reference logic to eliminate false positives"
```

---

#### Step 1.4: Document Classification Rules (30 minutes)

Add classification rules to your quality check's AGENTS.md.

**Add to** `scripts/AGENTS.md` (or quality check docs):

```markdown
## Manifest Discovery (L1 - Classification)

**Classification Rules**:

1. **False Positive**: Feature already in manifest (cross-reference logic missed it)
   - Action: Skip
   - Fix: Improve cross-reference logic

2. **Auto-fixable**: Clear deliverables (≥10 commits, ≥1 note, no ambiguity)
   - Action: Add to manifest (ready for L2 automation)
   - Fix: Generate manifest entry from git/notes

3. **Investigation**: Unclear boundaries or event-only features
   - Action: Manual review
   - Fix: Human determines feature scope

**Usage**:
\```bash
# Run with classification
python scripts/manifest-discover.py > results.json

# Filter auto-fixable violations
jq '.violations | map(select(.classification.category == "auto_fixable"))' results.json
\```
```

---

### Validation

#### Test L1 Adoption

**Run quality check**:
```bash
python scripts/quality-check.py > results.json
```

**Expected output** (JSON):
```json
{
  "check_name": "manifest-discovery",
  "phase": "CLASSIFY",
  "timestamp": "2025-11-20T10:30:00Z",
  "violations": [
    {
      "id": "FEAT-EXAMPLE",
      "description": "Untracked feature with 12 commits",
      "classification": {
        "category": "auto_fixable",
        "reason": "Feature has clear deliverables: 12 commits, 2 notes",
        "auto_action": "add_to_manifest",
        "suggestion": "Generate manifest entry from commits and notes"
      }
    }
  ]
}
```

**Verify classification accuracy**:
```bash
# Count classifications
jq '.violations | group_by(.classification.category) | map({category: .[0].classification.category, count: length})' results.json

# Expected output:
# [
#   {"category": "auto_fixable", "count": 5},
#   {"category": "investigation", "count": 2},
#   {"category": "false_positive", "count": 3}
# ]
```

**Success Criteria**:
- ✅ JSON output valid (validates against Phase 2 schema)
- ✅ All violations have `classification` field
- ✅ Classification categories are accurate (manual review of 5-10 samples)
- ✅ False positive rate <20% (cross-reference working)

---

### Expected Impact

**Before (L0)**:
- Manual triage of all violations
- No clear action path
- 100% human time investment

**After (L1)**:
- Auto-fixable violations identified (60-80% of total)
- False positives filtered (10-20% of total)
- 50% reduction in triage time
- Clear roadmap for L2 automation

**ROI Calculation**:
```
Time Investment: 2-3 hours (L1 implementation)
Weekly Savings: 1-1.5 hours (50% triage reduction)
Payback Period: 2-3 weeks
12-Month ROI: 1,700-2,600%
```

---

## L1 → L2: Adding REMEDIATION

### Overview

**Goal**: Automate fixes for 60-80% of common violation patterns.

**Input**: Quality check at L1 (classifications identify auto-fixable violations)
**Output**: Auto-fix scripts + justfile recipes for one-command remediation

**Benefits**:
- 80% reduction in manual fix time
- Batch operations for common patterns
- Consistent fix quality

**Time Estimate**: 4-6 hours per quality check

---

### Prerequisites

Before starting L2 adoption:

- ✅ **L1 operational**: Classifications identify auto-fixable violations accurately
- ✅ **Auto-fixable patterns identified**: At least 60% of violations are auto-fixable
- ✅ **Fix logic validated**: Manual fixes tested on 5-10 samples

**Validation**:
```bash
# Check auto-fixable percentage
python scripts/quality-check.py | jq '.violations | map(select(.classification.category == "auto_fixable")) | length'

# Should be ≥60% of total violations
```

---

### Implementation Steps

#### Step 2.1: Create Auto-Fix Script (2-3 hours)

Implement automated remediation for the most common violation patterns.

**Example** (manifest discovery - add missing features):
```python
# scripts/fix-manifest-discovery.py
#!/usr/bin/env python3
"""
Auto-fix manifest discovery violations (L2 REMEDIATE phase)

Usage:
    python scripts/fix-manifest-discovery.py results.json
"""

import json
import sys
from pathlib import Path
import yaml

def generate_manifest_entry(feature_data: dict) -> dict:
    """Generate feature manifest entry from evidence"""
    feature_id = feature_data['id']
    evidence = feature_data.get('evidence', {})

    # Extract data from commits and notes
    commits = evidence.get('commits', [])
    notes = evidence.get('notes', [])

    # Generate entry
    entry = {
        "id": feature_id,
        "title": extract_title(feature_id, commits, notes),
        "status": "completed",
        "created": extract_earliest_commit_date(commits),
        "last_updated": extract_latest_commit_date(commits),
        "code": {
            "paths": extract_code_paths(commits),
            "commits": [c['sha'] for c in commits[:10]]  # First 10 commits
        },
        "documentation": {
            "notes": [n['path'] for n in notes]
        }
    }

    return entry

def add_to_manifest(entry: dict, manifest_path: Path):
    """Add entry to feature-manifest.yaml"""
    with open(manifest_path, 'r') as f:
        manifest = yaml.safe_load(f)

    # Add entry (sorted by ID)
    manifest['features'].append(entry)
    manifest['features'].sort(key=lambda x: x['id'])

    # Write back
    with open(manifest_path, 'w') as f:
        yaml.dump(manifest, f, sort_keys=False, allow_unicode=True)

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/fix-manifest-discovery.py results.json")
        sys.exit(1)

    results_path = Path(sys.argv[1])
    results = json.loads(results_path.read_text())

    # Filter auto-fixable violations
    auto_fixable = [
        v for v in results['violations']
        if v['classification']['category'] == 'auto_fixable'
    ]

    if not auto_fixable:
        print("No auto-fixable violations found")
        return

    manifest_path = Path('feature-manifest.yaml')

    print(f"Processing {len(auto_fixable)} auto-fixable violations...")

    for violation in auto_fixable:
        entry = generate_manifest_entry(violation)
        add_to_manifest(entry, manifest_path)
        print(f"✅ Added {violation['id']} to manifest")

    print(f"\n✅ Fixed {len(auto_fixable)} violations")
    print(f"📝 Review changes: git diff {manifest_path}")

if __name__ == '__main__':
    main()
```

**Customization**: Adapt fix logic to your quality check's violations.

---

#### Step 2.2: Create Justfile Recipe (15 minutes)

Add one-command remediation to your justfile.

**Add to** `justfile`:
```makefile
# justfile

# Auto-fix manifest discovery violations (L2)
health-fix-manifest:
    @echo "=== Auto-fixing manifest discovery violations ==="
    @python scripts/manifest-discover.py > /tmp/manifest-results.json
    @python scripts/fix-manifest-discovery.py /tmp/manifest-results.json
    @echo ""
    @echo "✅ Auto-fixes applied. Review with: git diff feature-manifest.yaml"

# Fix specific category of violations
health-fix-manifest-category CATEGORY:
    @echo "=== Auto-fixing {{CATEGORY}} violations ==="
    @python scripts/manifest-discover.py | \
      jq '.violations | map(select(.classification.category == "{{CATEGORY}}"))' > /tmp/filtered.json
    @python scripts/fix-manifest-discovery.py /tmp/filtered.json
```

**Usage**:
```bash
# Fix all auto-fixable violations
just health-fix-manifest

# Fix only false positives (update cross-reference logic)
just health-fix-manifest-category false_positive
```

---

#### Step 2.3: Add Batch Operations (1-2 hours)

For quality checks with many similar violations, add batch fix support.

**Example** (script refactoring - UTF-8 header):
```python
# scripts/fix-script-refactoring.py

def fix_utf8_header(script_path: Path):
    """Add UTF-8 encoding header to Python script"""
    content = script_path.read_text()

    # Check if header already exists
    if content.startswith('#!/usr/bin/env python3\n# -*- coding: utf-8 -*-'):
        return False  # Already fixed

    # Add header
    header = '#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\n'
    new_content = header + content

    script_path.write_text(new_content)
    return True  # Fixed

def batch_fix_utf8():
    """Fix all scripts missing UTF-8 header"""
    scripts_dir = Path('scripts')
    fixed = 0

    for script_path in scripts_dir.glob('*.py'):
        if fix_utf8_header(script_path):
            print(f"✅ Fixed {script_path.name}")
            fixed += 1

    print(f"\n✅ Fixed {fixed} scripts")

# Justfile recipe:
# health-fix-scripts-utf8:
#     python scripts/fix-script-refactoring.py batch-utf8
```

---

#### Step 2.4: Update AGENTS.md (30 minutes)

Document remediation patterns for agents.

**Add to** `scripts/AGENTS.md`:
```markdown
## Manifest Discovery (L2 - Remediation)

**Auto-Fix Patterns**:

1. **Add to Manifest** (60% of violations)
   - Pattern: Feature with ≥10 commits, ≥1 note
   - Fix: Generate manifest entry from git/notes
   - Recipe: `just health-fix-manifest`

2. **Update Cross-Reference** (20% of violations)
   - Pattern: False positive (feature already documented)
   - Fix: Improve cross-reference logic to find existing entry
   - Manual intervention required (update script)

**Usage**:
\```bash
# One-command fix for all auto-fixable violations
just health-fix-manifest

# Review before committing
git diff feature-manifest.yaml

# Commit if correct
git add feature-manifest.yaml
git commit -m "fix: Add untracked features to manifest (auto-fix)"
\```

**Rollback**:
\```bash
# If auto-fix produced incorrect results
git restore feature-manifest.yaml
\```
```

---

### Validation

#### Test L2 Adoption

**Run auto-fix**:
```bash
# Generate violations with classifications
python scripts/quality-check.py > results.json

# Count auto-fixable violations before fix
BEFORE=$(jq '.violations | map(select(.classification.category == "auto_fixable")) | length' results.json)

# Run auto-fix
just health-fix-manifest

# Re-run quality check
python scripts/quality-check.py > results-after.json

# Count auto-fixable violations after fix
AFTER=$(jq '.violations | map(select(.classification.category == "auto_fixable")) | length' results-after.json)

# Verify reduction
echo "Before: $BEFORE auto-fixable violations"
echo "After: $AFTER auto-fixable violations"
echo "Fixed: $(($BEFORE - $AFTER)) violations"
```

**Success Criteria**:
- ✅ Auto-fix script runs without errors
- ✅ 60-80% of auto-fixable violations fixed correctly
- ✅ No regressions introduced (quality check passes after fix)
- ✅ Changes reviewable (`git diff` shows expected modifications)
- ✅ Rollback works (`git restore` undoes changes)

---

### Expected Impact

**Before (L1)**:
- Manual fixes for all violations
- 50% triage time reduction (classification helps)
- Still 1-2 hours/week manual work

**After (L2)**:
- 60-80% of violations fixed automatically
- One-command remediation (`just health-fix-*`)
- 80% reduction in manual fix time
- **Total improvement from L0**: 10x reduction (2x from L1, 5x from L2)

**ROI Calculation**:
```
Time Investment: 4-6 hours (L2 implementation)
Weekly Savings: 1.5-2 hours (80% fix automation)
Payback Period: 3-4 weeks
12-Month ROI: 1,300-2,600%
```

---

## L2 → L3: Adding TRACKING

### Overview

**Goal**: Track quality metrics over time to detect degradation and measure improvement.

**Input**: Quality check at L2 (violations fixed automatically)
**Output**: Health metrics stored in A-MEM, trend analysis, dashboard

**Benefits**:
- Detect quality degradation early (before it becomes toil)
- Measure ROI of quality improvements
- Prioritize remediation work by impact

**Time Estimate**: 2-3 hours per quality check

---

### Prerequisites

Before starting L3 adoption:

- ✅ **L2 operational**: Auto-fix scripts reduce violations by 60-80%
- ✅ **A-MEM enabled**: Event logging system available (SAP-010)
- ✅ **Baseline established**: At least 2-4 weeks of L2 operation

**Validation**:
```bash
# Check A-MEM availability
ls .chora/memory/events/*.jsonl

# Check L2 effectiveness (should show declining violations)
python scripts/quality-check.py | jq '.violations | length'
```

---

### Implementation Steps

#### Step 3.1: Add Metrics Collection (1-2 hours)

Update quality check to emit A-MEM events with metrics.

**Example** (manifest discovery):
```python
# scripts/manifest-discover.py

import json
from datetime import datetime

def emit_health_metric(results: dict):
    """Emit quality health metric to A-MEM"""
    event = {
        "timestamp": datetime.now().isoformat(),
        "type": "quality_health_metric",
        "check_name": "manifest-discovery",
        "phase": results.get("phase", "CLASSIFY"),
        "metrics": {
            "total_violations": len(results['violations']),
            "auto_fixable": sum(1 for v in results['violations'] if v['classification']['category'] == 'auto_fixable'),
            "investigation": sum(1 for v in results['violations'] if v['classification']['category'] == 'investigation'),
            "false_positive": sum(1 for v in results['violations'] if v['classification']['category'] == 'false_positive')
        },
        "trace_id": f"health-check-{datetime.now().strftime('%Y-%m-%d')}"
    }

    # Append to A-MEM event log
    event_log_path = Path('.chora/memory/events') / f"{datetime.now().strftime('%Y-%m')}.jsonl"
    with open(event_log_path, 'a') as f:
        f.write(json.dumps(event) + '\n')

def main():
    # ... existing detection and classification logic ...

    results = {
        "check_name": "manifest-discovery",
        "phase": "CLASSIFY",
        "violations": classified_violations
    }

    # Emit metric to A-MEM
    emit_health_metric(results)

    # Print results
    print(json.dumps(results, indent=2))
```

---

#### Step 3.2: Create Trend Analysis Script (1-2 hours)

Query A-MEM events to analyze quality trends over time.

**Create** `scripts/quality-trends.py`:
```python
#!/usr/bin/env python3
"""
Analyze quality trends from A-MEM events (L3 TRACK phase)

Usage:
    python scripts/quality-trends.py manifest-discovery --days 30
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

def query_health_metrics(check_name: str, days: int = 30) -> list:
    """Query A-MEM events for health metrics"""
    events_dir = Path('.chora/memory/events')
    cutoff = datetime.now() - timedelta(days=days)

    metrics = []

    for event_file in sorted(events_dir.glob('*.jsonl')):
        with open(event_file, 'r') as f:
            for line in f:
                event = json.loads(line)

                # Filter quality_health_metric events
                if event.get('type') != 'quality_health_metric':
                    continue
                if event.get('check_name') != check_name:
                    continue

                event_time = datetime.fromisoformat(event['timestamp'])
                if event_time < cutoff:
                    continue

                metrics.append(event)

    return sorted(metrics, key=lambda e: e['timestamp'])

def analyze_trend(metrics: list) -> dict:
    """Analyze trend: improving, stable, or degrading"""
    if len(metrics) < 2:
        return {"trend": "insufficient_data", "reason": "Need at least 2 data points"}

    # Calculate trend slope (simple linear regression)
    total_violations = [m['metrics']['total_violations'] for m in metrics]

    # First half vs second half
    mid = len(total_violations) // 2
    first_half_avg = sum(total_violations[:mid]) / mid
    second_half_avg = sum(total_violations[mid:]) / (len(total_violations) - mid)

    change_pct = ((second_half_avg - first_half_avg) / first_half_avg) * 100 if first_half_avg > 0 else 0

    if change_pct < -20:
        return {"trend": "improving", "change_pct": change_pct, "reason": f"{abs(change_pct):.1f}% reduction"}
    elif change_pct > 20:
        return {"trend": "degrading", "change_pct": change_pct, "reason": f"{change_pct:.1f}% increase (ALERT!)"}
    else:
        return {"trend": "stable", "change_pct": change_pct, "reason": f"{abs(change_pct):.1f}% variance"}

def print_trend_report(check_name: str, metrics: list, trend: dict):
    """Print human-readable trend report"""
    print(f"=== Quality Trend Report: {check_name} ===")
    print(f"Period: {metrics[0]['timestamp'][:10]} to {metrics[-1]['timestamp'][:10]}")
    print(f"Data Points: {len(metrics)}")
    print()

    print(f"Trend: {trend['trend'].upper()}")
    print(f"Change: {trend.get('change_pct', 0):.1f}%")
    print(f"Reason: {trend['reason']}")
    print()

    if trend['trend'] == 'degrading':
        print("⚠️ WARNING: Quality degrading! Investigate root cause.")
        print("Recommended Actions:")
        print("1. Review recent commits for quality regressions")
        print("2. Check if auto-fix recipes are still effective")
        print("3. Consider adding new classification rules")
    elif trend['trend'] == 'improving':
        print("✅ Quality improving! Good work.")
    else:
        print("📊 Quality stable. Continue monitoring.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/quality-trends.py <check-name> [--days N]")
        sys.exit(1)

    check_name = sys.argv[1]
    days = 30

    if '--days' in sys.argv:
        days = int(sys.argv[sys.argv.index('--days') + 1])

    metrics = query_health_metrics(check_name, days)

    if not metrics:
        print(f"No metrics found for {check_name} in last {days} days")
        sys.exit(1)

    trend = analyze_trend(metrics)
    print_trend_report(check_name, metrics, trend)

if __name__ == '__main__':
    main()
```

**Justfile recipe**:
```makefile
# justfile

# Show quality trends for the last 30 days
health-trends CHECK days="30":
    python scripts/quality-trends.py {{CHECK}} --days {{days}}

# Example: just health-trends manifest-discovery 60
```

---

#### Step 3.3: Add Dashboard to Weekly Health Check (30 minutes)

Integrate trend analysis into your weekly health check.

**Update** `justfile`:
```makefile
# justfile

# Weekly health check with trends (L3)
weekly-health:
    @echo "=== Quality Health Check (Week of $(date +%Y-%m-%d)) ==="
    @echo ""

    @echo "=== Manifest Discovery ==="
    @python scripts/manifest-discover.py > /tmp/manifest-results.json
    @echo "Current Violations: $(cat /tmp/manifest-results.json | jq '.violations | length')"
    @echo "Trend (30 days):"
    @python scripts/quality-trends.py manifest-discovery --days 30 | grep "Trend:"
    @echo ""

    @echo "=== Script Refactoring ==="
    @python scripts/audit-script-refactoring.py > /tmp/script-results.json
    @echo "Current Violations: $(cat /tmp/script-results.json | jq '.violations | length')"
    @echo "Trend (30 days):"
    @python scripts/quality-trends.py script-refactoring --days 30 | grep "Trend:"
    @echo ""

    # ... other quality checks ...
```

---

### Validation

#### Test L3 Adoption

**Collect baseline metrics** (run weekly for 2-4 weeks):
```bash
# Week 1
just weekly-health

# Week 2
just weekly-health

# Week 3
just weekly-health

# Week 4
just weekly-health
```

**Analyze trends**:
```bash
# Show trend over 30 days
python scripts/quality-trends.py manifest-discovery --days 30

# Expected output:
# === Quality Trend Report: manifest-discovery ===
# Period: 2025-10-20 to 2025-11-20
# Data Points: 4
#
# Trend: IMPROVING
# Change: -35.2%
# Reason: 35.2% reduction
#
# ✅ Quality improving! Good work.
```

**Success Criteria**:
- ✅ Metrics collected weekly (A-MEM events exist)
- ✅ Trend analysis runs without errors
- ✅ Trend accurately reflects quality changes (manual validation)
- ✅ Dashboard integrated into weekly health check

---

### Expected Impact

**Before (L2)**:
- No visibility into quality trends
- Cannot detect degradation until it becomes toil
- No data to justify quality investments

**After (L3)**:
- Weekly quality trends visible
- Early warning for degradation (20% threshold)
- ROI measurement for quality improvements
- **Total improvement from L0**: 12x reduction (10x from L2, 1.2x from L3)

**ROI Calculation**:
```
Time Investment: 2-3 hours (L3 implementation)
Weekly Savings: 15-20 minutes (early detection prevents larger issues)
Payback Period: 6-10 weeks
12-Month ROI: 260-520%
```

---

## L3 → L4: Adding PREVENTION

### Overview

**Goal**: Integrate quality checks into pre-commit hooks to prevent new violations at source.

**Input**: Quality check at L3 (metrics track improvement)
**Output**: Pre-commit hook that blocks new violations while allowing pre-existing ones

**Benefits**:
- Zero new violations introduced
- Quality baseline maintained automatically
- Developer feedback <5 seconds

**Time Estimate**: 2-4 hours per quality check

---

### Prerequisites

Before starting L4 adoption:

- ✅ **L3 operational**: Metrics show quality stable or improving
- ✅ **Quality baseline low**: <10 violations remaining (or all violations are investigation-only)
- ✅ **Pre-commit framework**: SAP-006 (Quality Gates) adopted

**Validation**:
```bash
# Check pre-commit installed
pre-commit --version

# Check current violation count (should be low)
python scripts/quality-check.py | jq '.violations | length'
# → Should be <10 or all investigation-only
```

---

### Implementation Steps

#### Step 4.1: Create Quality Baseline (30 minutes)

Capture current violations as "allowed" baseline.

**Create** `.quality-baseline.json`:
```python
# scripts/create-quality-baseline.py
#!/usr/bin/env python3
"""
Create quality baseline for L4 PREVENT phase

This captures current violations as "allowed" so pre-commit hook
can block NEW violations while tolerating pre-existing ones.
"""

import json
from pathlib import Path

def create_baseline():
    """Create quality baseline from current state"""

    # Run all quality checks
    checks = [
        'manifest-discover',
        'script-refactoring',
        'link-validation',
        'traceability-validation'
    ]

    baseline = {
        "created": datetime.now().isoformat(),
        "checks": {}
    }

    for check in checks:
        # Run check
        result = subprocess.run(
            ['python', f'scripts/{check}.py'],
            capture_output=True,
            text=True
        )
        results = json.loads(result.stdout)

        # Extract violation IDs (to allow these specific violations)
        allowed_violations = [
            v['id'] for v in results['violations']
            if v['classification']['category'] == 'investigation'
        ]

        baseline['checks'][check] = {
            "allowed_violations": allowed_violations,
            "count": len(allowed_violations)
        }

    # Write baseline
    baseline_path = Path('.quality-baseline.json')
    baseline_path.write_text(json.dumps(baseline, indent=2))

    print(f"✅ Created quality baseline: {baseline_path}")
    print(f"Allowed violations: {sum(c['count'] for c in baseline['checks'].values())}")

if __name__ == '__main__':
    create_baseline()
```

**Run**:
```bash
python scripts/create-quality-baseline.py

# Output:
# ✅ Created quality baseline: .quality-baseline.json
# Allowed violations: 8
```

**Commit baseline**:
```bash
git add .quality-baseline.json
git commit -m "chore: Create quality baseline for L4 prevention"
```

---

#### Step 4.2: Create Pre-Commit Hook (1-2 hours)

Add quality check to pre-commit configuration.

**Update** `.pre-commit-config.yaml`:
```yaml
# .pre-commit-config.yaml

repos:
  # ... existing hooks (ruff, mypy, etc.) ...

  # SAP-054 L4 prevention hooks
  - repo: local
    hooks:
      - id: quality-check-manifest
        name: Quality Check (Manifest Discovery)
        entry: python scripts/pre-commit/quality-check-manifest.py
        language: python
        pass_filenames: false
        always_run: false
        files: '^(feature-manifest\.yaml|\.chora/memory/.*\.jsonl)$'

      - id: quality-check-scripts
        name: Quality Check (Script Refactoring)
        entry: python scripts/pre-commit/quality-check-scripts.py
        language: python
        pass_filenames: false
        files: '^scripts/.*\.py$'

      - id: quality-check-links
        name: Quality Check (Link Validation)
        entry: python scripts/pre-commit/quality-check-links.py
        language: python
        pass_filenames: false
        files: '\.md$'
```

**Create** `scripts/pre-commit/quality-check-manifest.py`:
```python
#!/usr/bin/env python3
"""
Pre-commit hook for manifest discovery (L4 PREVENT)

Blocks commits that introduce NEW untracked features while allowing
pre-existing violations (from .quality-baseline.json).
"""

import json
import sys
from pathlib import Path
import subprocess

def load_baseline():
    """Load allowed violations from baseline"""
    baseline_path = Path('.quality-baseline.json')
    if not baseline_path.exists():
        print("⚠️ WARNING: No quality baseline found. Run: python scripts/create-quality-baseline.py")
        return {"checks": {}}

    return json.loads(baseline_path.read_text())

def check_manifest_discovery():
    """Run manifest discovery and compare to baseline"""

    # Run quality check
    result = subprocess.run(
        ['python', 'scripts/manifest-discover.py'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Quality check failed: {result.stderr}")
        return False

    results = json.loads(result.stdout)
    baseline = load_baseline()

    # Get allowed violations from baseline
    allowed = set(baseline.get('checks', {}).get('manifest-discover', {}).get('allowed_violations', []))

    # Get current violations
    current = {v['id'] for v in results['violations']}

    # Check for NEW violations (not in baseline)
    new_violations = current - allowed

    if new_violations:
        print("❌ QUALITY CHECK FAILED: New untracked features detected")
        print()
        print("New violations:")
        for vid in new_violations:
            violation = next(v for v in results['violations'] if v['id'] == vid)
            print(f"  - {vid}: {violation.get('description', 'No description')}")
        print()
        print("Fix:")
        print("  1. Add features to manifest: just health-fix-manifest")
        print("  2. Re-run commit")
        print()
        print("Or update baseline if intentional:")
        print("  python scripts/create-quality-baseline.py")
        return False

    # Check if violations REDUCED (praise!)
    resolved = allowed - current
    if resolved:
        print(f"✅ Quality improved! Resolved {len(resolved)} violations")

    return True

if __name__ == '__main__':
    success = check_manifest_discovery()
    sys.exit(0 if success else 1)
```

**Install hooks**:
```bash
pre-commit install
```

---

#### Step 4.3: Test Pre-Commit Hook (30 minutes)

Validate that hook blocks new violations and allows baseline.

**Test 1: Baseline violations allowed**:
```bash
# Make innocuous change
echo "# Comment" >> README.md
git add README.md
git commit -m "test: Baseline violations should pass"

# Expected: ✅ Commit succeeds (baseline violations allowed)
```

**Test 2: New violations blocked**:
```bash
# Introduce new untracked feature (simulate new commits without manifest entry)
# (This test requires actually creating commits, so simulate by updating baseline)

# Temporarily remove violation from baseline
jq '.checks["manifest-discover"].allowed_violations = []' .quality-baseline.json > /tmp/baseline.json
mv /tmp/baseline.json .quality-baseline.json

# Try to commit
git add .
git commit -m "test: New violations should fail"

# Expected: ❌ Commit blocked
# ❌ QUALITY CHECK FAILED: New untracked features detected
#
# New violations:
#   - FEAT-EXAMPLE: Untracked feature with 5 commits
#
# Fix:
#   1. Add features to manifest: just health-fix-manifest
#   2. Re-run commit

# Restore baseline
git restore .quality-baseline.json
```

**Success Criteria**:
- ✅ Pre-commit hook runs in <5 seconds
- ✅ Baseline violations allowed (no false positives)
- ✅ New violations blocked with clear error message
- ✅ Fix instructions provided in error message

---

#### Step 4.4: Update Developer Documentation (30 minutes)

Add L4 prevention to your CONTRIBUTING.md or AGENTS.md.

**Add to** `AGENTS.md`:
```markdown
## Quality Gates (L4 - Prevention)

**Pre-Commit Hooks**: Prevent new quality violations at source.

**What's Checked**:
1. **Manifest Discovery**: Block new untracked features
2. **Script Refactoring**: Block new non-compliant scripts
3. **Link Validation**: Block new broken links
4. **Traceability**: Block new traceability violations

**Quality Baseline**:
- `.quality-baseline.json` defines allowed pre-existing violations
- Pre-commit hooks block NEW violations only
- Update baseline when violations are intentionally resolved:
  \```bash
  python scripts/create-quality-baseline.py
  git add .quality-baseline.json
  git commit -m "chore: Update quality baseline"
  \```

**When Hooks Fail**:
\```bash
# Auto-fix violations
just health-fix-manifest

# Re-run commit
git commit -m "feat: Add new feature"
\```

**Disable Hooks** (emergency only):
\```bash
# Skip hooks for this commit (use sparingly!)
git commit --no-verify -m "feat: Emergency fix"
\```
```

---

### Validation

#### Test L4 Adoption

**Daily workflow validation** (1 week):
```bash
# Day 1-7: Make normal commits
git add .
git commit -m "feat: Normal development work"

# Monitor:
# - Pre-commit hooks should run on every commit
# - Hooks should complete in <5 seconds
# - No false positives (baseline violations allowed)
# - New violations caught and blocked
```

**Metrics validation**:
```bash
# After 1 week, check quality trend
python scripts/quality-trends.py manifest-discovery --days 7

# Expected: Trend should be STABLE or IMPROVING
# (New violations prevented, baseline may slowly improve)
```

**Success Criteria**:
- ✅ Pre-commit hooks active for all developers
- ✅ Zero new violations introduced (trend stable)
- ✅ <5 second hook execution time
- ✅ No bypass culture (`--no-verify` not normalized)
- ✅ Quality baseline updated when violations resolved

---

### Expected Impact

**Before (L3)**:
- Quality tracked but not enforced
- New violations can be introduced
- Reactive fixes after violations occur

**After (L4)**:
- Zero new violations introduced (proactive prevention)
- Quality baseline maintained automatically
- Developer feedback immediate (<5 seconds)
- **Total improvement from L0**: 15-20x reduction (12x from L3, 1.3x from L4)

**ROI Calculation**:
```
Time Investment: 2-4 hours (L4 implementation)
Weekly Savings: 20-30 minutes (prevented violations + reduced remediation)
Payback Period: 4-8 weeks
12-Month ROI: 260-650%
```

**Overall L0→L4 ROI**: 430-650% over 12 months

---

## Troubleshooting

### Issue: Classification Accuracy Low (<60% auto-fixable)

**Symptoms**: L1 classifications mark too many violations as "investigation"

**Cause**: Classification rules too conservative

**Fix**:
```python
# Review classification thresholds
def classify_violation(v):
    # Before: Too strict (commits > 10)
    if v['commits'] > 10 and v['notes'] > 0:
        return "auto_fixable"

    # After: More permissive (commits > 5)
    if v['commits'] > 5 and v['notes'] > 0:
        return "auto_fixable"
```

**Validate**: Re-run classification and check auto-fixable percentage

---

### Issue: Auto-Fix Script Produces Incorrect Results

**Symptoms**: L2 auto-fix creates wrong entries or breaks files

**Cause**: Fix logic incomplete or edge cases not handled

**Fix**:
1. **Add dry-run mode**:
   ```python
   # scripts/fix-quality-check.py
   if '--dry-run' in sys.argv:
       print("DRY RUN: Would fix:")
       for violation in auto_fixable:
           print(f"  - {violation['id']}")
       sys.exit(0)
   ```

2. **Test on small batch**:
   ```bash
   # Fix only 1 violation for testing
   python scripts/fix-quality-check.py --limit 1
   git diff  # Review changes
   ```

3. **Add validation**:
   ```python
   # After fix, re-run quality check
   subprocess.run(['python', 'scripts/quality-check.py'])
   # Verify violation count decreased
   ```

---

### Issue: Trend Analysis Shows "Insufficient Data"

**Symptoms**: L3 trend analysis fails with <2 data points

**Cause**: Quality check not run frequently enough

**Fix**:
```bash
# Add to cron or CI to run weekly automatically
# crontab -e
0 9 * * 1 cd /path/to/project && just weekly-health

# Or GitHub Actions:
# .github/workflows/weekly-health.yml
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am
jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: just weekly-health
```

---

### Issue: Pre-Commit Hook Too Slow (>10 seconds)

**Symptoms**: L4 hooks delay commits, tempting `--no-verify` bypass

**Cause**: Quality check runs on entire codebase

**Fix**:
```python
# scripts/pre-commit/quality-check.py

# Before: Check entire codebase
violations = check_all_files()

# After: Check only modified files
import subprocess

# Get staged files
staged = subprocess.run(
    ['git', 'diff', '--cached', '--name-only'],
    capture_output=True, text=True
).stdout.splitlines()

# Filter to relevant files
relevant = [f for f in staged if f.endswith('.md')]

# Check only relevant files
violations = check_files(relevant)
```

**Target**: <5 seconds for typical commit

---

### Issue: Quality Baseline Grows Over Time

**Symptoms**: `.quality-baseline.json` has 50+ violations and increasing

**Cause**: L4 prevention without L2 remediation (only blocks NEW violations)

**Fix**:
1. **Adopt L2 first**: Auto-fix existing violations before L4 prevention
   ```bash
   # Reduce baseline to <10 violations
   just health-fix-manifest
   just health-fix-scripts

   # Update baseline
   python scripts/create-quality-baseline.py
   ```

2. **Set baseline reduction goal**:
   ```bash
   # Track baseline size monthly
   jq '[.checks[].count] | add' .quality-baseline.json
   # Goal: Reduce by 20% per month
   ```

---

## References

- [Capability Charter](capability-charter.md) - Problem statement and L0-L4 adoption levels
- [Protocol Specification](protocol-spec.md) - JSON schemas for each phase (DETECT, CLASSIFY, REMEDIATE, TRACK, PREVENT)
- [AGENTS.md](AGENTS.md) - Agent workflows for implementing L1-L4
- [SAP-006: Quality Gates](../quality-gates/README.md) - Pre-commit hook integration
- [SAP-010: Memory System](../memory-system/README.md) - A-MEM event logging for L3 tracking
- [SAP-050: SAP Adoption Verification](../sap-adoption-verification/README.md) - Quality verification patterns

---

**Version**: 1.0.0
**Status**: Draft
**Estimated Adoption Time**:
- L0→L1: 2-3 hours per check
- L1→L2: 4-6 hours per check
- L2→L3: 2-3 hours per check
- L3→L4: 2-4 hours per check
- **Total L0→L4**: 10-16 hours per check

**Expected ROI**: 430-650% over 12 months (per quality check)
