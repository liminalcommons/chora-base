# Deep Dive Evaluation Prompt Template

You are assessing **{sap_id}** ({sap_name}) adoption depth for an AI agent.

## Context

- **Repository**: {repo_root}
- **SAP Installed**: {is_installed}
- **Evaluation Date**: {timestamp}

## Quick Check Results

{quick_check_results}

## Adoption Criteria

### Level 1: Basic Adoption
{level_1_criteria}

### Level 2: Standard Adoption
{level_2_criteria}

### Level 3: Advanced Adoption
{level_3_criteria}

## Files Analyzed

{files_summary}

## Your Task

Assess the current adoption state and identify gaps:

1. **Determine Current Level**: Which level criteria are fully met?
2. **Calculate Completion**: What % of next level criteria are satisfied?
3. **Identify Gaps**: What's missing for the next level?
4. **Prioritize Gaps**: Rank by impact × effort
5. **Suggest Actions**: Provide concrete, executable steps

## Output Format

Return a JSON object with this structure:

```json
{
  "current_level": 1,
  "level_1_completion": 100,
  "level_2_completion": 45,
  "level_3_completion": 0,
  "gaps": [
    {
      "gap_id": "unique-identifier",
      "gap_type": "installation|integration|quality|optimization",
      "title": "Short description",
      "description": "Detailed explanation",
      "impact": "high|medium|low",
      "effort": "high|medium|low",
      "priority": "P0|P1|P2",
      "urgency": "blocks_sprint|next_sprint|future",
      "current_state": "What exists now",
      "desired_state": "What should exist",
      "blocks": ["SAP-IDs blocked by this gap"],
      "blocked_by": ["Dependencies"],
      "actions": [
        {
          "action_id": "action-1",
          "description": "What to do",
          "tool": "Read|Write|Edit|Bash",
          "file_path": "/path/to/file (if applicable)",
          "command": "bash command (if tool=Bash)",
          "rationale": "Why this helps",
          "expected_outcome": "What changes",
          "validation_command": "How to verify",
          "estimated_minutes": 30,
          "sequence": 1
        }
      ],
      "estimated_hours": 2.5,
      "validation": "How to verify gap is fixed"
    }
  ],
  "next_milestone": "Level 2 adoption",
  "estimated_effort_hours": 5.0
}
```

## Evaluation Guidelines

**Impact Assessment**:
- **High**: Blocks other SAPs, prevents critical functionality, affects multiple areas
- **Medium**: Improves efficiency, enables optional features, affects single area
- **Low**: Nice-to-have optimization, cosmetic improvement

**Effort Assessment**:
- **High**: >4 hours, requires significant learning, complex implementation
- **Medium**: 2-4 hours, straightforward with templates, moderate complexity
- **Low**: <2 hours, quick fix with clear instructions

**Priority Calculation**:
- **P0**: High impact + Low/Medium effort, or blocks sprint progress
- **P1**: High impact + High effort, or Medium impact + Low effort
- **P2**: Low impact or future optimization

**Action Specificity**:
- Include exact file paths, line numbers where possible
- Provide copy-pasteable commands
- Reference templates or examples
- Include validation steps

## Example Gap (for reference)

```json
{
  "gap_id": "coverage-below-target",
  "gap_type": "quality",
  "title": "Test coverage 65% < 85% target",
  "description": "Current test coverage is 20% below Level 2 requirement of 85%. 8 additional tests needed for core API handlers.",
  "impact": "high",
  "effort": "medium",
  "priority": "P0",
  "urgency": "blocks_sprint",
  "current_state": "65% coverage (18 tests)",
  "desired_state": "85% coverage (26 tests, +8)",
  "blocks": ["SAP-005"],
  "blocked_by": [],
  "actions": [
    {
      "action_id": "coverage-action-1",
      "description": "Generate HTML coverage report to identify gaps",
      "tool": "Bash",
      "command": "pytest --cov=src --cov-report=html && open htmlcov/index.html",
      "rationale": "Visual coverage report shows exactly which lines/modules need tests",
      "expected_outcome": "HTML report opens showing uncovered code in red",
      "validation_command": "test -f htmlcov/index.html && echo 'Report generated'",
      "estimated_minutes": 5,
      "sequence": 1
    },
    {
      "action_id": "coverage-action-2",
      "description": "Write 8 tests for API handlers (40% uncovered)",
      "tool": "Write",
      "file_path": "tests/test_api_handlers.py",
      "rationale": "API handlers are critical path, need test coverage",
      "expected_outcome": "8 new tests covering POST/PUT/DELETE handlers",
      "validation_command": "pytest tests/test_api_handlers.py -v",
      "estimated_minutes": 150,
      "sequence": 2
    },
    {
      "action_id": "coverage-action-3",
      "description": "Validate 85% coverage achieved",
      "tool": "Bash",
      "command": "pytest --cov=src --cov-report=term | grep TOTAL",
      "rationale": "Confirm gap is closed",
      "expected_outcome": "TOTAL line shows ≥85%",
      "validation_command": "pytest --cov=src --cov-report=json && jq '.totals.percent_covered' coverage.json",
      "estimated_minutes": 2,
      "sequence": 3
    }
  ],
  "estimated_hours": 3.0,
  "validation": "pytest --cov=src shows ≥85%"
}
```

---

**Important**: Be specific, actionable, and realistic. Every gap should have concrete steps an AI agent can execute immediately.
