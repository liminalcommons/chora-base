# Strategic Analysis Prompt Template

Generate a quarterly SAP adoption roadmap for **{repo_name}**.

## Current State

- **Total SAPs**: {total_saps_available}
- **Installed**: {total_saps_installed}
- **Distribution**: {level_distribution}
- **Average Level**: {average_adoption_level}

## All SAP Results

{all_sap_results}

## Your Task

1. **Analyze Aggregate Metrics**: Calculate adoption maturity, velocity trends
2. **Identify Cross-SAP Dependencies**: Which gaps block multiple SAPs?
3. **Prioritize Globally**: Rank all gaps by impact × effort × blocked count
4. **Generate Sprint Breakdown**: This sprint, next sprint, future sprints
5. **Project ROI**: Estimate hours invested vs. hours saved

## Output Format

```yaml
metadata:
  generated_at: {timestamp}
  target_quarter: Q1-2026
  next_review_date: {next_review}

current_state:
  total_saps_installed: 12
  adoption_percentage: 67%
  distribution:
    level_0: 6
    level_1: 10
    level_2: 2
    level_3: 0
  average_adoption_level: 1.17

priority_gaps:
  - rank: 1
    sap_id: SAP-004
    gap_id: coverage-below-target
    gap_title: "Test coverage 65% < 85%"
    impact: high
    effort: medium
    priority_score: 0.85
    reason: "Blocks SAP-005 (CI/CD coverage gates)"
    sprint: current
    estimated_hours: 3
    blocks: [SAP-005]
    deliverables:
      - "85% test coverage achieved"
      - "8 new tests for API handlers"

sprints:
  current_sprint:
    name: "Sprint 23"
    start_date: 2025-11-01
    end_date: 2025-11-14
    focus: "Unblock CI/CD and establish metrics"
    focus_saps: [SAP-004, SAP-013]
    target_levels:
      SAP-004: 2
      SAP-013: 1
    total_estimated_hours: 4
    expected_outcomes:
      - "SAP-005 unblocked (coverage gates enabled)"
      - "ROI evidence available"

  next_sprint:
    name: "Sprint 24"
    focus: "Agent efficiency + async testing"
    focus_saps: [SAP-009, SAP-004]
    total_estimated_hours: 3.5
```

## Priority Scoring

**Priority Score** = (Impact / Effort) × Blocker Multiplier

- **Impact**: 0.3 (low) | 0.6 (medium) | 1.0 (high)
- **Effort**: 1.0 (low) | 0.6 (medium) | 0.3 (high)
- **Blocker Multiplier**: 1.0 + (0.2 × # SAPs blocked)

**Sprint Assignment**:
- **Current**: Priority score >0.7 OR blocks_sprint urgency
- **Next**: Priority score 0.4-0.7
- **Future**: Priority score <0.4

## Guidelines

- Focus on top 10 gaps (most impactful)
- Balance quick wins (low effort) with high impact (unblock multiple SAPs)
- Realistic sprint estimates (4-8 hours per 2-week sprint)
- Clear success criteria (how to verify sprint goals met)
