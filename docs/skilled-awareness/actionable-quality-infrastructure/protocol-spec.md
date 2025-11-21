# Protocol Specification: Actionable Quality Infrastructure

**Capability ID**: SAP-054
**Modern Namespace**: chora.quality.actionable_infrastructure
**Type**: Meta-Pattern
**Status**: Draft
**Version**: 1.0.0
**Protocol Version**: 1.0.0
**Last Updated**: 2025-11-20

---

## Overview

This document specifies the complete protocol for building actionable quality infrastructure that transforms detection-only checks (L0) into complete feedback loops (L1-L4).

**Protocol Goals**:
- **Complete Feedback Loops**: Define 5-phase schema (DETECT → CLASSIFY → REMEDIATE → TRACK → PREVENT)
- **Progressive Adoption**: Enable L0→L1→L2→L3→L4 progression with clear schemas at each level
- **Auto-Fix Safety**: Classification and confirmation workflows prevent destructive auto-fixes
- **Trend Detection**: Time-series metrics schema enables proactive quality monitoring
- **Pre-commit Integration**: Hook specification prevents new violations without blocking pre-existing issues

---

## 5-Phase Feedback Loop Schema

### Phase 1: DETECT (L0)

**Purpose**: Find violations via automated scripts/tools

**Output Schema** (JSON):
```json
{
  "check_name": "manifest-discovery",
  "check_version": "1.0.0",
  "timestamp": "2025-11-20T14:30:00Z",
  "phase": "DETECT",
  "violations": [
    {
      "id": "FEAT-SAP-012",
      "type": "untracked_feature",
      "confidence": "medium",
      "description": "Git commits found (35 commits) but no manifest entry",
      "evidence": {
        "commits": 35,
        "events": 12,
        "notes": 3
      }
    }
  ],
  "summary": {
    "total_violations": 12,
    "severity_breakdown": {
      "high": 2,
      "medium": 6,
      "low": 4
    }
  }
}
```

**Required Fields**:
- `check_name`: Unique identifier for quality check (kebab-case)
- `check_version`: Version of detection script (semver)
- `timestamp`: ISO 8601 timestamp with timezone
- `phase`: Must be "DETECT" for L0
- `violations`: Array of violation objects
  - `id`: Unique identifier for violation (e.g., feature ID, file path)
  - `type`: Violation type (e.g., "untracked_feature", "missing_utf8", "broken_link")
  - `confidence`: Detection confidence ("high" | "medium" | "low")
  - `description`: Human-readable description
  - `evidence`: Supporting data (flexible structure)

---

### Phase 2: CLASSIFY (L1)

**Purpose**: Categorize violations as auto-fixable, investigation-required, or false-positive

**Output Schema** (JSON):
```json
{
  "check_name": "manifest-discovery",
  "check_version": "1.1.0",
  "timestamp": "2025-11-20T14:35:00Z",
  "phase": "CLASSIFY",
  "violations": [
    {
      "id": "FEAT-SAP-012",
      "type": "untracked_feature",
      "confidence": "medium",
      "description": "Git commits found (35 commits) but no manifest entry",
      "evidence": {
        "commits": 35,
        "events": 12,
        "notes": 3
      },
      "classification": {
        "category": "false_positive",
        "reason": "Already documented in manifest at line 1583",
        "auto_action": "skip",
        "suggestion": "Cross-reference check failed to find existing entry"
      }
    },
    {
      "id": "FEAT-REPO-CURATION-2025-11",
      "type": "untracked_feature",
      "confidence": "low",
      "description": "32 events, 0 commits, 0 notes - may be cross-cutting work",
      "evidence": {
        "commits": 0,
        "events": 32,
        "notes": 0
      },
      "classification": {
        "category": "investigation",
        "reason": "Event-only feature, no clear deliverable",
        "auto_action": "none",
        "suggestion": "Review events to determine if feature tracking is appropriate"
      }
    },
    {
      "id": "FEAT-UNIFIED-DISCOVERY",
      "type": "untracked_feature",
      "confidence": "high",
      "description": "35 commits, 12 events, 3 notes - clear feature deliverable",
      "evidence": {
        "commits": 35,
        "events": 12,
        "notes": 3
      },
      "classification": {
        "category": "auto_fixable",
        "reason": "Feature has clear deliverables and traceability artifacts",
        "auto_action": "add_to_manifest",
        "suggestion": "Generate manifest entry from git/events/notes"
      }
    }
  ],
  "summary": {
    "total_violations": 12,
    "classification_breakdown": {
      "auto_fixable": 5,
      "investigation": 1,
      "false_positive": 6
    }
  }
}
```

**Required Classification Fields**:
- `classification.category`: One of:
  - `"auto_fixable"`: Can be remediated automatically (60-80% of violations)
  - `"investigation"`: Requires manual analysis
  - `"false_positive"`: Not a real violation, filter in future runs
- `classification.reason`: Why this classification was chosen (for audit trail)
- `classification.auto_action`: Action to take (e.g., "add_to_manifest", "skip", "none")
- `classification.suggestion`: Human-readable guidance for next steps

**Classification Rules Schema** (for documentation):
```yaml
classification_rules:
  - name: "manifest_cross_reference"
    pattern: "Feature already in manifest"
    category: "false_positive"
    auto_action: "skip"

  - name: "clear_deliverable"
    pattern: "commits > 10 AND notes > 0"
    category: "auto_fixable"
    auto_action: "add_to_manifest"

  - name: "event_only_feature"
    pattern: "commits == 0 AND events > 0"
    category: "investigation"
    auto_action: "none"
```

---

### Phase 3: REMEDIATE (L2)

**Purpose**: Auto-fix violations classified as "auto_fixable"

**Input Schema** (from CLASSIFY phase):
```json
{
  "violations": [
    {
      "id": "FEAT-UNIFIED-DISCOVERY",
      "classification": {
        "category": "auto_fixable",
        "auto_action": "add_to_manifest"
      }
    }
  ]
}
```

**Remediation Plan Schema** (JSON):
```json
{
  "check_name": "manifest-discovery",
  "check_version": "1.2.0",
  "timestamp": "2025-11-20T14:40:00Z",
  "phase": "REMEDIATE",
  "remediation_plan": [
    {
      "violation_id": "FEAT-UNIFIED-DISCOVERY",
      "action": "add_to_manifest",
      "target_file": "feature-manifest.yaml",
      "operation": "insert",
      "insert_after_line": 3406,
      "content_preview": "  - id: FEAT-002-UNIFIED-DISCOVERY\n    name: \"FEAT-002: Unified Traceability Discovery System\"...",
      "validation": {
        "pre_check": "yaml_syntax_valid",
        "post_check": "validate_traceability"
      }
    }
  ],
  "summary": {
    "total_remediations": 5,
    "estimated_time_seconds": 15,
    "requires_confirmation": true
  }
}
```

**Remediation Execution Schema** (JSON):
```json
{
  "check_name": "manifest-discovery",
  "timestamp": "2025-11-20T14:42:00Z",
  "phase": "REMEDIATE",
  "execution_status": "success",
  "remediations_applied": [
    {
      "violation_id": "FEAT-UNIFIED-DISCOVERY",
      "action": "add_to_manifest",
      "status": "applied",
      "diff": {
        "file": "feature-manifest.yaml",
        "added_lines": 127,
        "deleted_lines": 0
      },
      "validation_results": {
        "pre_check": "passed",
        "post_check": "passed"
      }
    }
  ],
  "summary": {
    "successful": 5,
    "failed": 0,
    "skipped": 1,
    "execution_time_seconds": 12.3
  }
}
```

**Justfile Recipe Interface**:
```makefile
# Remediate violations from CLASSIFY phase output
health-fix-manifest-discovery:
    #!/usr/bin/env bash
    # Read classification output
    CLASSIFY_OUTPUT=$(just manifest-discover --output json --phase classify)

    # Generate remediation plan
    python scripts/remediate-manifest-discovery.py \
        --input <(echo "$CLASSIFY_OUTPUT") \
        --output remediation-plan.json \
        --dry-run

    # Show plan and confirm
    cat remediation-plan.json | jq '.remediation_plan[]'
    read -p "Apply these fixes? [y/N] " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python scripts/remediate-manifest-discovery.py \
            --input remediation-plan.json \
            --execute
    fi
```

---

### Phase 4: TRACK (L3)

**Purpose**: Monitor quality metrics over time to detect trends

**Metrics Storage Schema** (A-MEM event format):
```json
{
  "event_type": "quality_metrics_snapshot",
  "timestamp": "2025-11-20T14:45:00Z",
  "check_name": "script-refactoring-audit",
  "metrics": {
    "utf8_compliance": {
      "value": 65.6,
      "unit": "percent",
      "numerator": 84,
      "denominator": 128,
      "target": 100.0
    },
    "jsonexporter_usage": {
      "value": 24.8,
      "unit": "percent",
      "numerator": 34,
      "denominator": 137,
      "target": 100.0
    },
    "emoji_removal": {
      "value": 38.8,
      "unit": "percent",
      "numerator": 57,
      "denominator": 147,
      "target": 100.0
    }
  },
  "metadata": {
    "trace_id": "weekly-health-2025-11-20",
    "context": "sprint-10"
  }
}
```

**Trend Analysis Schema** (JSON):
```json
{
  "check_name": "script-refactoring-audit",
  "metric_name": "utf8_compliance",
  "period": {
    "start": "2025-08-01",
    "end": "2025-11-20"
  },
  "trend": {
    "direction": "stable",
    "velocity": 0.2,
    "confidence": "high",
    "interpretation": "UTF-8 compliance stagnant at 65% for 3 months - remediation needed"
  },
  "snapshots": [
    {"date": "2025-08-01", "value": 65.2},
    {"date": "2025-09-01", "value": 65.4},
    {"date": "2025-10-01", "value": 65.6},
    {"date": "2025-11-01", "value": 65.6},
    {"date": "2025-11-20", "value": 65.6}
  ],
  "alert": {
    "severity": "warning",
    "message": "No improvement in 90 days - trigger remediation phase"
  }
}
```

**Trend Detection Rules**:
```yaml
trend_rules:
  - name: "improving"
    pattern: "velocity > 0.5 AND recent_snapshots_increasing"
    alert_severity: "info"

  - name: "stable"
    pattern: "abs(velocity) < 0.5 AND value < target"
    alert_severity: "warning"
    suggestion: "Trigger remediation phase"

  - name: "degrading"
    pattern: "velocity < -0.5"
    alert_severity: "error"
    suggestion: "Immediate investigation required"
```

---

### Phase 5: PREVENT (L4)

**Purpose**: Block new violations at source (pre-commit hooks)

**Pre-commit Hook Schema** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: local
    hooks:
      - id: manifest-discovery-prevent
        name: Prevent untracked features
        entry: scripts/prevent-untracked-features.py
        language: python
        stages: [commit]
        pass_filenames: false
        args:
          - --mode=prevent
          - --baseline=.quality-baseline.json
```

**Baseline Schema** (`.quality-baseline.json`):
```json
{
  "check_name": "manifest-discovery",
  "baseline_date": "2025-11-20",
  "known_violations": [
    {
      "id": "FEAT-LEGACY-001",
      "type": "untracked_feature",
      "acknowledged": true,
      "acknowledged_by": "victorpiper",
      "acknowledged_date": "2025-11-20",
      "reason": "Legacy feature from before manifest adoption"
    }
  ],
  "prevention_rules": {
    "block_new_violations": true,
    "allow_pre_existing": true,
    "require_acknowledgement": true
  }
}
```

**Prevention Hook Output Schema** (exit codes):
```bash
# Exit 0: No new violations
# Exit 1: New violations detected (blocks commit)
# Exit 2: Pre-existing violations (warning, commit allowed)

# JSON output format (stdout):
{
  "hook_name": "manifest-discovery-prevent",
  "timestamp": "2025-11-20T14:50:00Z",
  "phase": "PREVENT",
  "status": "blocked",
  "new_violations": [
    {
      "id": "FEAT-NEW-UNTRACKED",
      "type": "untracked_feature",
      "evidence": {
        "commits_in_diff": 5
      },
      "suggestion": "Add to feature-manifest.yaml or run: just health-fix-manifest-discovery"
    }
  ],
  "pre_existing_violations": [
    {
      "id": "FEAT-LEGACY-001",
      "type": "untracked_feature",
      "acknowledged": true,
      "baseline_reference": ".quality-baseline.json:15"
    }
  ]
}
```

---

## Reference Implementations

### 1. Manifest Discovery (L0 → L2)

**L0 (DETECT)**: Find untracked features via git/events/notes analysis

```bash
# Detection script
python scripts/manifest-discover.py --output json

# Output (12 violations detected)
{
  "check_name": "manifest-discovery",
  "violations": [
    {"id": "FEAT-SAP-012", "confidence": "medium", ...},
    {"id": "FEAT-002", "confidence": "high", ...},
    # ... 10 more
  ]
}
```

**L1 (CLASSIFY)**: Cross-reference with manifest, categorize

```python
# Classification logic
def classify_manifest_violation(violation):
    # Check if already in manifest
    if feature_exists_in_manifest(violation['id']):
        return {
            "category": "false_positive",
            "reason": f"Already documented in manifest",
            "auto_action": "skip"
        }

    # Check if has clear deliverables
    if (violation['evidence']['commits'] > 10 and
        violation['evidence']['notes'] > 0):
        return {
            "category": "auto_fixable",
            "reason": "Clear deliverable with traceability",
            "auto_action": "add_to_manifest"
        }

    # Default to investigation
    return {
        "category": "investigation",
        "reason": "Unclear feature boundaries",
        "auto_action": "none"
    }
```

**L2 (REMEDIATE)**: Auto-add to manifest

```bash
# Remediation recipe
just health-fix-manifest-discovery

# Generates FEAT-002 entry with 127 lines
# Prompts for confirmation
# Inserts into feature-manifest.yaml
# Validates with: python scripts/validate-traceability.py
```

---

### 2. Script Refactoring Audit (L0 → L2)

**L0 (DETECT)**: Audit 147 scripts for UTF-8/emoji/JSONExporter

```bash
python scripts/audit-script-refactoring.py --output json

# Output
{
  "check_name": "script-refactoring-audit",
  "metrics": {
    "utf8_compliance": {"value": 65.6, "numerator": 84, "denominator": 128},
    "jsonexporter_usage": {"value": 24.8, "numerator": 34, "denominator": 137},
    "emoji_removal": {"value": 38.8, "numerator": 57, "denominator": 147}
  },
  "violations": [
    {
      "id": "scripts/sap-evaluator.py",
      "type": "missing_utf8_header",
      "confidence": "high"
    },
    # ... 63 more
  ]
}
```

**L1 (CLASSIFY)**: Categorize by fix pattern

```python
def classify_script_violation(violation):
    if violation['type'] == 'missing_utf8_header':
        return {
            "category": "auto_fixable",
            "reason": "UTF-8 header addition is deterministic",
            "auto_action": "add_utf8_header",
            "fix_pattern": "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-"
        }

    if violation['type'] == 'emoji_present':
        return {
            "category": "auto_fixable",
            "reason": "Emoji removal is safe (cosmetic change)",
            "auto_action": "remove_emoji"
        }

    if violation['type'] == 'missing_jsonexporter':
        return {
            "category": "auto_fixable",
            "reason": "JSONExporter refactor is standardized",
            "auto_action": "convert_to_jsonexporter"
        }
```

**L2 (REMEDIATE)**: Batch fix 44 UTF-8 headers

```bash
just health-fix-scripts --fix-type utf8

# Applies UTF-8 headers to 44 scripts
# Shows diff preview
# Prompts for confirmation
# Validates with: ruff check scripts/
```

---

### 3. Link Validation (L0 → L2)

**L0 (DETECT)**: Find >100 broken links

```bash
just validate-links --output json

# Output
{
  "check_name": "link-validation",
  "violations": [
    {
      "id": "inbox/README.md:15",
      "type": "broken_link",
      "link": "ecosystem/ECOSYSTEM_COORDINATION_ANNOUNCEMENT.md",
      "confidence": "high"
    },
    # ... 99 more
  ]
}
```

**L1 (CLASSIFY)**: Detect moved/renamed/deleted files

```python
def classify_link_violation(violation):
    link_target = violation['link']

    # Check if file exists elsewhere (moved)
    similar_files = find_files_by_name(os.path.basename(link_target))
    if similar_files:
        return {
            "category": "auto_fixable",
            "reason": "File moved to new location",
            "auto_action": "rewrite",
            "correct_path": similar_files[0]
        }

    # Check if file was renamed (edit distance < 3)
    renamed_candidates = find_similar_filenames(link_target, threshold=3)
    if renamed_candidates:
        return {
            "category": "auto_fixable",
            "reason": "File renamed with minor changes",
            "auto_action": "rewrite",
            "correct_path": renamed_candidates[0]
        }

    # File deleted - manual review
    return {
        "category": "investigation",
        "reason": "File deleted, manual review needed",
        "auto_action": "none"
    }
```

**L2 (REMEDIATE)**: Auto-rewrite 60 moved file references

```bash
just health-fix-links

# Rewrites moved file references
# Shows diff preview
# Prompts for confirmation
# Validates with: just validate-links
```

---

### 4. Traceability Validation (L0 → L2)

**L0 (DETECT)**: 60% pass rate (40% violations)

```bash
python scripts/validate-traceability.py --output json

# Output
{
  "check_name": "traceability-validation",
  "pass_rate": 60.0,
  "violations": [
    {
      "id": "FEAT-SAP-LIFECYCLE-META-SAPS",
      "type": "missing_vision_ref",
      "rule": "Rule 1: Forward Linkage",
      "confidence": "high"
    },
    # ... 39 more
  ]
}
```

**L1 (CLASSIFY)**: Detect auto-fixable patterns

```python
def classify_traceability_violation(violation):
    if violation['type'] == 'missing_vision_ref':
        # Infer vision ref from feature name
        inferred_ref = infer_vision_ref(violation['id'])
        if inferred_ref:
            return {
                "category": "auto_fixable",
                "reason": "Vision ref can be inferred from feature name",
                "auto_action": "add_vision_ref",
                "suggested_value": inferred_ref
            }

    if violation['type'] == 'missing_test_type':
        return {
            "category": "auto_fixable",
            "reason": "Test type MANUAL can be added for process features",
            "auto_action": "add_test_type",
            "suggested_value": "manual"
        }

    if violation['type'] == 'missing_test':
        return {
            "category": "investigation",
            "reason": "Test implementation requires manual work",
            "auto_action": "none"
        }
```

**L2 (REMEDIATE)**: Auto-add missing vision_ref fields

```bash
just health-fix-traceability --fix-type vision_ref

# Adds vision_ref to 20 features
# Shows diff preview
# Prompts for confirmation
# Validates with: python scripts/validate-traceability.py
```

---

## Integration Interfaces

### Justfile Recipe Pattern

**Standard Recipe Interface**:
```makefile
# Pattern: health-{action}-{check-name}
# Actions: check, classify, fix, track, prevent

# DETECT (L0)
health-check-manifest-discovery:
    python scripts/manifest-discover.py --output json

# CLASSIFY (L1)
health-classify-manifest-discovery:
    python scripts/manifest-discover.py --output json --phase classify

# REMEDIATE (L2)
health-fix-manifest-discovery:
    python scripts/remediate-manifest-discovery.py --interactive

# TRACK (L3)
health-track-manifest-discovery:
    python scripts/track-quality-metrics.py \
        --check manifest-discovery \
        --output .chora/memory/events/2025-11.jsonl

# PREVENT (L4) - integrated into pre-commit, not direct recipe
```

### Agent Workflow Integration (AGENTS.md)

**Quick Reference Pattern**:
```markdown
## Quality Infrastructure Workflows

### Weekly Health Check (L1-L3)

**Goal**: Triage quality violations with minimal toil

**Steps**:
1. Run `just weekly-health` (executes all CLASSIFY checks)
2. Review classification summary (auto-fixable vs investigation)
3. Run `just health-fix-*` for auto-fixable items
4. Create beads tasks for investigation items
5. Review trend analysis (L3) for degrading metrics

**Time Budget**: 30-60 min (down from 2-3 hours at L0)
```

### Pre-commit Hook Integration (L4)

**Hook Configuration Pattern**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      # Pattern: prevent-{check-name}
      - id: prevent-manifest-discovery
        name: Prevent untracked features
        entry: scripts/prevent-untracked-features.py
        language: python
        stages: [commit]
        pass_filenames: false
        args:
          - --baseline=.quality-baseline.json

      - id: prevent-script-regression
        name: Prevent script quality regression
        entry: scripts/prevent-script-regression.py
        language: python
        types: [python]
        stages: [commit]
        args:
          - --baseline=.quality-baseline.json
```

---

## Performance Characteristics

### Time Budgets by Phase

| Phase | Time Budget | Example (Manifest Discovery) |
|-------|-------------|-------------------------------|
| DETECT | 10-30s | 15s to scan git/events/notes |
| CLASSIFY | +5-15s | 8s to cross-reference manifest |
| REMEDIATE | +30-120s | 60s to generate + insert 127 lines |
| TRACK | +1-5s | 2s to append metrics event to JSONL |
| PREVENT | <1s | <1s pre-commit hook (only changed files) |

**Total L0→L4 overhead**: ~2 minutes (detection + classification + remediation + tracking)

**Toil Reduction Calculation**:
- L0: 2-3 hours/week manual triage
- L1: 1-1.5 hours/week (classification filters false positives)
- L2: 20-30 min/week (auto-fix 60-80% of violations)
- **Savings**: 2.5 hours/week → 10 hours/month → 130 hours/year per quality check

---

## Error Handling

### Classification Errors

**Scenario**: Classification rule produces false classification

**Handling**:
```json
{
  "violation_id": "FEAT-XYZ",
  "classification": {
    "category": "auto_fixable",
    "confidence": 0.65,
    "fallback_category": "investigation",
    "error_note": "Low confidence - recommend manual review"
  }
}
```

**Threshold**: confidence < 0.70 → fallback to "investigation"

### Remediation Errors

**Scenario**: Auto-fix script fails validation

**Handling**:
```json
{
  "violation_id": "FEAT-XYZ",
  "remediation_status": "failed",
  "error": {
    "type": "validation_failure",
    "message": "Post-fix validation failed: traceability check returned 9/10 rules",
    "suggested_action": "Rollback changes and investigate manually"
  },
  "rollback_status": "completed"
}
```

**Rollback Strategy**: Auto-fix failures trigger automatic rollback to pre-fix state

### Trend Detection Errors

**Scenario**: Insufficient data for trend analysis

**Handling**:
```json
{
  "check_name": "new-quality-check",
  "metric_name": "compliance_rate",
  "trend": {
    "direction": "unknown",
    "error": "Insufficient snapshots (2 < 5 required)",
    "suggestion": "Collect ≥5 snapshots before trend analysis"
  }
}
```

---

## Backward Compatibility

**Version**: 1.0.0

**Breaking Changes**: None (initial version)

**Deprecation Policy**:
- Phase schema changes: 6-month deprecation period
- Classification category changes: 3-month deprecation period
- JSON field renames: 12-month backward compatibility guarantee

**Migration Path**: N/A (initial version)

---

**Version**: 1.0.0
**Protocol Version**: 1.0.0
**Status**: Draft
**Next Review**: After L1 reference implementation validation (OPP-2025-040)
