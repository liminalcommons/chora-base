# chora-compose Modality Selector

**Interactive tool to help you choose the right chora-compose integration modality.**

---

## Quick Start

```bash
# Run interactive selector
python select-modality.py

# Quick mode (fewer questions)
python select-modality.py --quick

# Export recommendation as markdown guide
python select-modality.py --export md --output my-guide.md
```

**Time to completion**: < 2 minutes

---

## What is This?

chora-compose supports 4 integration modalities:

1. **pip** - Python library integration
2. **MCP** - Model Context Protocol for AI agents
3. **CLI** - Command-line interface
4. **Docker** - Container-based deployment

Choosing the right modality depends on your use case, environment, team size, and constraints.

This interactive tool asks 4 simple questions and recommends the best modality for your situation with:
- Confidence score (0-20)
- Reasons for recommendation
- Key considerations
- Setup instructions
- Next steps

---

## Example Session

```
$ python select-modality.py

======================================================================
chora-compose Modality Selector
======================================================================

This tool will help you choose the right integration modality
for your use case. Answer a few questions to get a recommendation.

Question 1: What is your primary use case?

  1. AI agent (Claude Desktop/Cursor) generating content
  2. Python project needing programmatic content generation
  3. Command-line testing and experimentation
  4. Team automation (n8n workflows, scheduled generation)
  5. CI/CD integration for automated builds

Your choice (1-5): 1

Question 2: What is your development environment?

  1. Python development environment (venv/conda)
  2. Claude Desktop or AI-enabled IDE (Cursor, VSCode)
  3. Docker Desktop installed
  4. CI/CD system (GitHub Actions, GitLab CI)
  5. No Python installed (CLI/Docker only)

Your choice (1-5): 2

======================================================================
RECOMMENDATION
======================================================================

✅ Recommended Modality: MCP
   Confidence Score: 17/20

Why this modality?
  • AI agent use case (primary MCP scenario)
  • AI-enabled IDE (MCP native integration)

Key Considerations:
  • Requires Docker Desktop installed
  • Provides 24 MCP tools for AI agents
  • Best for AI-assisted content generation
  • Setup time: 10-15 minutes

Next Steps:
  1. See protocol-spec.md §2 for detailed MCP setup
  2. Follow adoption-blueprint.md Workflow 2 (AI Agent)
  3. Complete setup in < 30 minutes

======================================================================
Thank you for using the chora-compose modality selector!
======================================================================
```

---

## Questions Asked

### Full Mode (4 questions)

1. **Primary use case**: AI agent, Python project, testing, team automation, CI/CD
2. **Development environment**: Python, AI IDE, Docker, CI/CD, no Python
3. **Team size**: Solo, small (2-5), medium (6-15), large (15+)
4. **Technical constraints**: Offline, security, reproducibility, disk space, none

### Quick Mode (2 questions)

1. Primary use case
2. Development environment

---

## Export Options

Generate a personalized markdown guide with your recommendation:

```bash
python select-modality.py --export md --output modality-guide.md
```

The exported guide includes:
- Your selected modality
- Reasons for selection
- Key considerations
- Step-by-step setup instructions
- Quick start code examples
- Next steps

---

## Use Cases

### Use Case 1: New User

**Scenario**: Never used chora-compose before, unsure which modality to choose.

**Solution**:
```bash
python select-modality.py --export md
# Follow generated modality-guide.md
```

### Use Case 2: Team Decision

**Scenario**: Team needs to standardize on one modality.

**Solution**:
1. Each team member runs selector independently
2. Share results and confidence scores
3. Choose modality with highest average score
4. Export shared guide for team onboarding

### Use Case 3: Migration

**Scenario**: Currently using pip, considering Docker for team consistency.

**Solution**:
```bash
python select-modality.py --quick
# Compare recommendation to current modality
# If Docker recommended with higher score, plan migration
```

---

## Scoring Algorithm

Each question adds points to modality scores (0-10 per question):

- **Use case** (0-10 points): Primary driver of recommendation
- **Environment** (0-7 points): Environment constraints and capabilities
- **Team size** (0-5 points): Collaboration and consistency needs
- **Constraints** (0-5 points): Technical requirements and limitations

**Total possible score**: 20 points (best match)

**Interpretation**:
- **15-20**: Strong recommendation
- **10-14**: Good fit with some trade-offs
- **5-9**: Acceptable but consider alternatives
- **0-4**: Poor fit, choose different modality

---

## Alternatives

If you prefer manual selection, see [protocol-spec.md §4.1](./protocol-spec.md#workflow-1-first-success--30-minutes) for decision trees.

---

## Requirements

- **Python**: 3.12+ (uses dataclasses, Enum)
- **Dependencies**: None (stdlib only)
- **Platforms**: macOS, Linux, Windows

---

## Exit Codes

- `0`: Successful completion
- `1`: User canceled (Ctrl+C, 'quit', 'exit')

---

##FAQ

**Q: Can I run this multiple times?**
A: Yes! Try different scenarios to explore recommendations.

**Q: Does this install anything?**
A: No, it's a pure Python script with no side effects.

**Q: Can I customize questions?**
A: Yes, edit `select-modality.py` and add/modify questions in `_ask_*` methods.

**Q: What if two modalities have similar scores?**
A: The tool shows an "Alternative" if the second-best score is within 30% of the top score.

**Q: Can I automate this for CI/CD?**
A: Yes, but recommendations are designed for human decision-making. For automated selection, use environment detection logic instead.

---

## Troubleshooting

**Issue**: `ModuleNotFoundError` when running

**Solution**: Ensure Python 3.12+ is installed:
```bash
python --version  # Should show 3.12 or higher
```

**Issue**: Script hangs waiting for input

**Solution**: Press `q` + Enter to exit gracefully, or use Ctrl+C

**Issue**: Want to skip questions

**Solution**: Use `--quick` mode for fewer questions

---

## Related Documentation

- [protocol-spec.md](./protocol-spec.md) - Complete integration specifications for all modalities
- [adoption-blueprint.md](./adoption-blueprint.md) - Role-based workflows and step-by-step guides
- [awareness-guide.md](./awareness-guide.md) - AI agent guidance for using chora-compose

---

**Version**: 1.0.0
**Last Updated**: 2025-11-04
**Maintainer**: chora-base team
