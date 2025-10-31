# Quick Check Evaluation Prompt Template

Quickly validate **{sap_id}** ({sap_name}) installation and basic functionality.

## Checks to Perform

1. **Artifacts Present**: All 5 required files exist
   - capability-charter.md
   - protocol-spec.md
   - awareness-guide.md
   - adoption-blueprint.md
   - ledger.md

2. **Validation Commands**: Run basic checks from protocol-spec.md
   {validation_commands}

3. **Installation Status**: Determine if Level 0 (not installed) or Level 1+ (installed)

## Output Format

```json
{
  "sap_id": "{sap_id}",
  "is_installed": true,
  "current_level": 1,
  "validation_results": {
    "artifacts_complete": true,
    "validation_1": true,
    "validation_2": false
  },
  "blockers": ["List any immediate blockers"],
  "next_milestone": "Level 2",
  "estimated_effort_hours": 3.0
}
```

## Guidelines

- Quick checks should complete in <30 seconds
- Use boolean validation (pass/fail, exists/missing)
- Don't deep-dive into content quality (that's for deep evaluation)
- Identify blockers that prevent any usage
