# SAP Self-Evaluation - Awareness Guide

**Pattern ID**: SAP-019
**Pattern Name**: sap-self-evaluation
**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-10-30

**Target Audience**: AI agents (Claude, other LLMs) performing self-assessment of SAP adoption.

## Quick Reference (Essential Context, <2000 tokens)

### What is SAP Self-Evaluation?

A **progressive evaluation framework** enabling you (an AI agent) to:
1. **Assess** SAP adoption depth (Level 0/1/2/3)
2. **Identify** prioritized gaps blocking value
3. **Generate** actionable roadmaps for improvement

### When to Use

**Trigger scenarios**:
- User asks "How are we doing with SAPs?"
- Sprint planning (evaluate progress, plan next steps)
- After installing new SAP (validate installation)
- Quarterly reviews (strategic roadmap generation)
- Before major releases (capability maturity check)

**Do NOT use for**:
- SAP installation (use `install-sap.py` instead)
- Bug fixing (use normal debugging workflow)
- Performance optimization (separate concern)

### Three Evaluation Modes

| Mode | Time | Purpose | Output |
|------|------|---------|--------|
| **Quick Check** | 30s | Validate installation, run automated checks | Terminal status |
| **Deep Dive** | 5min | LLM content analysis, gap identification | Markdown report |
| **Strategic** | 30min | Roadmap generation, timeline analysis | YAML roadmap |

### Core Workflow (Agent-Executable)

**Quick Check** (use when user asks for status):
```bash
# Step 1: Run evaluator
python scripts/sap-evaluator.py --quick

# Step 2: Review output
# ✅ = passing, ❌ = failing, 🟡 = partial

# Step 3: Report to user
# Summarize: "X/Y SAPs at Level 2+, Z gaps identified"
```

**Deep Dive** (use when user asks "how can we improve?"):
```bash
# Step 1: Choose SAP to evaluate
python scripts/sap-evaluator.py --deep SAP-004

# Step 2: Read generated report
# (markdown file with gap analysis)

# Step 3: Extract actionable next steps
# Present top 3 prioritized actions to user
```

**Strategic** (use when user asks "what's our roadmap?"):
```bash
# Step 1: Run strategic analysis
python scripts/sap-evaluator.py --strategic --output sap-roadmap.yaml

# Step 2: Read roadmap
# Parse YAML for sprint breakdown

# Step 3: Integrate with project planning
# Update project-docs/ or create coordination request
```

### Key Files

```
docs/skilled-awareness/sap-self-evaluation/
├── capability-charter.md    # Problem statement
├── protocol-spec.md         # API, data models, evaluation logic
├── awareness-guide.md       # This file (agent guidance)
├── adoption-blueprint.md    # Installation instructions
├── ledger.md                # Adoption tracking
└── schemas/
    ├── evaluation-result.json
    ├── adoption-roadmap.json
    └── gap.json

scripts/
├── sap-evaluator.py         # CLI tool you'll execute
└── templates/
    ├── quick-check-prompt.md
    ├── deep-dive-prompt.md
    └── strategic-analysis-prompt.md

utils/
└── sap_evaluation.py        # Core evaluation engine (import in Python)
```

### Validation

**Installation check**:
```bash
test -f scripts/sap-evaluator.py && echo "✅ SAP-019 installed" || echo "❌ Not installed"
```

**Functional check**:
```bash
python scripts/sap-evaluator.py --quick SAP-000 && echo "✅ Evaluator working" || echo "❌ Error"
```

---

## Common Workflows

### Workflow 1: User Asks "How's Our SAP Adoption?"

**Scenario**: User wants quick status update.

**Your Actions**:
1. **Run quick check** (30 seconds):
   ```bash
   python scripts/sap-evaluator.py --quick
   ```

2. **Parse output** for key metrics:
   - Total SAPs installed: `X/18`
   - Distribution: Level 0/1/2/3 counts
   - Health indicators: ✅❌🟡

3. **Summarize** for user:
   ```markdown
   ## SAP Adoption Status

   **Installed**: 12/18 SAPs (67%)
   **Maturity**: 2/12 at Level 2+ (17%)
   **Health**: 🟡 Progressing

   **Top Priority**: SAP-004 (Testing) - Coverage gap blocks CI/CD

   Run deep dive for detailed analysis:
   ```python scripts/sap-evaluator.py --deep SAP-004```
   ```

4. **Offer next steps**: "Would you like me to run a deep dive on SAP-004 to identify specific actions?"

### Workflow 2: User Asks "How Can We Improve SAP-X?"

**Scenario**: User wants actionable improvements for specific SAP.

**Your Actions**:
1. **Run deep dive** (5 minutes):
   ```bash
   python scripts/sap-evaluator.py --deep SAP-004 --output docs/adoption-reports/SAP-004-assessment.md
   ```

2. **Read generated report** (use Read tool):
   ```
   Read: docs/adoption-reports/SAP-004-assessment.md
   ```

3. **Extract prioritized gaps** from report:
   - Gap 1: Title, impact, effort, actions
   - Gap 2: ...
   - Gap 3: ...

4. **Present to user** with concrete actions:
   ```markdown
   ## SAP-004 (Testing Framework) - Improvement Plan

   **Current Level**: 1 (Basic)
   **Next Milestone**: Level 2 (85% coverage)

   ### Priority Gaps

   1. **Coverage Below 85%** (P0, 3 hours)
      - Write 8 tests for API handlers
      - Validation: `pytest --cov=src` shows ≥85%
      - Unblocks: SAP-005 (CI/CD coverage gates)

   2. **Missing Async Patterns** (P1, 1.5 hours)
      - Install pytest-asyncio
      - Create async fixtures in conftest.py
      - Write 4 async handler tests

   **This Sprint Focus**: Gap 1 (unblock CI/CD)
   **Next Sprint**: Gap 2 (async patterns)

   Shall I create a task list and begin implementation?
   ```

5. **Offer to execute**: If user agrees, use TodoWrite to create tasks, then begin implementation.

### Workflow 3: Sprint Planning - Generate Adoption Roadmap

**Scenario**: User planning next quarter, wants strategic SAP adoption plan.

**Your Actions**:
1. **Run strategic analysis** (30 minutes):
   ```bash
   python scripts/sap-evaluator.py --strategic --output project-docs/sap-roadmap.yaml
   ```

2. **Read generated roadmap** (use Read tool):
   ```
   Read: project-docs/sap-roadmap.yaml
   ```

3. **Parse roadmap structure**:
   - Current state (installed, levels, ROI)
   - Priority gaps (rank 1-5 with justifications)
   - Sprint breakdown (this sprint, next sprint, future)
   - Quarterly goals (targets)

4. **Summarize for user**:
   ```markdown
   ## Q1-2026 SAP Adoption Roadmap

   ### Current State
   - 12/18 SAPs installed (67%)
   - Average Level: 1.17
   - Current ROI: 1.46x (35h saved / 24h invested)

   ### Quarterly Goals
   - Target: 10/12 SAPs at Level 2+ (83% maturity)
   - Target ROI: 3.0x (130h saved / 43.5h invested)
   - Install: SAP-016, SAP-017, SAP-018

   ### This Sprint (Nov 1-14)
   **Focus**: Unblock CI/CD + Establish metrics baseline

   1. SAP-004 → Level 2 (3h) - Achieve 85% coverage
   2. SAP-013 → Level 1 (1h) - Install metrics tracking

   **Outcomes**: CI/CD unblocked, ROI evidence available

   ### Next Sprint (Nov 15-28)
   **Focus**: Agent efficiency + Async testing

   1. SAP-009 → Level 2 (2h) - Domain AGENTS.md files
   2. SAP-004 complete (1.5h) - Async test patterns

   ---

   Full roadmap saved to: project-docs/sap-roadmap.yaml

   Would you like me to create tasks for this sprint?
   ```

5. **Integrate with planning**: Offer to create coordination request (SAP-001) or update sprint board.

### Workflow 4: After Installing New SAP - Validate Installation

**Scenario**: You just installed SAP-013, need to verify it's working.

**Your Actions**:
1. **Run quick check** on specific SAP:
   ```bash
   python scripts/sap-evaluator.py --quick SAP-013
   ```

2. **Verify installation**:
   ```
   ✅ Installed (5/5 artifacts present)
   ✅ ClaudeROICalculator imports successfully
   ❌ No metrics collected yet

   Current Level: 0 (installed but not used)
   Next Milestone: Level 1 (collect 5 session metrics)
   Estimated Effort: 1 hour
   ```

3. **Report to user**:
   ```markdown
   SAP-013 (Metrics Tracking) installed successfully!

   **Status**: ✅ All artifacts present
   **Level**: 0 (ready to use)
   **Next Step**: Collect metrics for 5 sessions to reach Level 1

   Usage:
   ```python
   from utils.claude_metrics import ClaudeROICalculator
   calc = ClaudeROICalculator()
   # ... use during sessions ...
   ```

   Shall I begin tracking metrics for this session?
   ```

4. **Offer to activate**: If user agrees, start using SAP immediately.

### Workflow 5: Quarterly Review - Track Progress Over Time

**Scenario**: Q4 ends, user wants to see adoption progress this quarter.

**Your Actions**:
1. **Run strategic analysis** with history:
   ```bash
   python scripts/sap-evaluator.py --strategic --include-history
   ```

2. **Analyze timeline** (from git history + events.jsonl):
   - SAPs installed this quarter
   - Level progressions (1 → 2 → 3)
   - Adoption velocity (SAPs/month, levels/month)
   - ROI trends

3. **Generate comparison** (Q3 vs. Q4):
   ```markdown
   ## Q4-2025 SAP Adoption Progress

   ### Quarter Summary
   - **SAPs Installed**: 12 → 15 (+3)
   - **Level 2+ Count**: 2 → 8 (+6)
   - **Average Level**: 1.17 → 1.73 (+0.56)
   - **ROI**: 1.46x → 2.85x (+1.39x)

   ### Velocity
   - Adoption Rate: 1 SAP/month (steady)
   - Time to Level 2: 14 days avg (-3 days vs. Q3)
   - Trend: Accelerating

   ### Top Achievements
   1. SAP-004 → Level 3 (comprehensive testing, 95% coverage)
   2. SAP-013 → Level 2 (automated ROI tracking in CI)
   3. SAP-009 → Level 2 (5 domain AGENTS.md files)

   ### Q1-2026 Goals
   - Target: 13/15 SAPs at Level 2+ (87% maturity)
   - Install: SAP-016 (link validation)
   - Focus: Quality over quantity (Level 2 → Level 3)
   ```

4. **Archive report**: Commit to `docs/adoption-reports/Q4-2025-review.md` for historical tracking.

---

## Best Practices (Agent-Specific)

### DO: Progressive Evaluation

**Start quick, go deep only when needed**:
```python
# Quick check first (30s)
quick_result = run_quick_check("SAP-004")

if quick_result.has_gaps():
    # Deep dive for details (5min)
    deep_result = run_deep_dive("SAP-004")
    present_gaps(deep_result)
else:
    # All good!
    report_success()
```

**Rationale**: Respect user's time. Don't run 30-minute strategic analysis if quick check shows no issues.

### DO: Concrete Actions Over Scores

**Bad** (abstract scores):
```
SAP-004 adoption score: 65/100
Quality score: 7/10
Recommendation: Improve testing
```

**Good** (concrete actions):
```
SAP-004 current level: 1
Gap: Coverage 65% < 85% target
Action: Write 8 tests for API handlers (3 hours)
Validation: `pytest --cov=src` shows ≥85%
Blocks: SAP-005 (CI/CD coverage gates)
```

**Rationale**: Users need actionable next steps, not just numbers.

### DO: Link Gaps to Business Value

**Bad** (technical focus only):
```
Gap: No async test patterns
Action: Install pytest-asyncio
```

**Good** (value-focused):
```
Gap: Async code untested (4 functions, 0 tests)
Risk: Production async bugs (API handlers)
Action: Install pytest-asyncio, write 4 async tests (1.5h)
Value: Prevent async-related outages, improve reliability
```

**Rationale**: Help user prioritize by showing business impact.

### DO: Track Progress Visibly

**After completing actions**, update tracking:
```bash
# 1. Log event
echo '{"event_type": "sap_level_completed", "sap_id": "SAP-004", "level": 2, "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> adoption-history.jsonl

# 2. Update ledger
# (use Edit tool to add changelog entry to ledger.md)

# 3. Re-evaluate to confirm
python scripts/sap-evaluator.py --quick SAP-004
```

**Rationale**: Version-controlled progress tracking creates accountability.

### DON'T: Hallucinate Gaps

**Bad** (guessing):
```
Gap: Test coverage probably low
Action: Maybe write more tests?
Confidence: Low
```

**Good** (validated):
```bash
# 1. Run actual validation
pytest --cov=src --cov-report=term

# 2. Parse output
Coverage: 65%

# 3. State facts
Gap: Coverage 65% < 85% target (validated)
Action: Write 8 tests to reach 85%
Confidence: High
```

**Rationale**: Only report gaps you can verify with automation or file reads.

### DON'T: Over-Evaluate

**Bad** (unnecessary deep dive):
```
User: "Is SAP-004 installed?"
Agent: *Runs 30-minute strategic analysis*
```

**Good** (match depth to question):
```
User: "Is SAP-004 installed?"
Agent: *Runs 5-second file check*
Agent: "Yes, SAP-004 installed. All 5 artifacts present. Run quick check for validation?"
```

**Rationale**: Progressive evaluation - start minimal, expand as needed.

### DON'T: Ignore Dependencies

**Bad** (isolated recommendations):
```
Priority 1: SAP-005 → Level 2 (enable coverage gates)
Priority 2: SAP-004 → Level 2 (achieve 85% coverage)
```

**Good** (dependency-aware):
```
Priority 1: SAP-004 → Level 2 (85% coverage) - BLOCKS SAP-005
Priority 2: SAP-005 → Level 2 (coverage gates) - BLOCKED BY SAP-004

Recommended order:
1. SAP-004 first (3 hours)
2. SAP-005 second (30 minutes) - unblocked after #1
```

**Rationale**: Dependency-aware prioritization prevents wasted effort.

---

## Common Pitfalls (Avoid These)

### Pitfall 1: Confusing Evaluation with Implementation

**Wrong**:
```
User: "Evaluate SAP-004"
Agent: *Starts writing tests to improve coverage*
```

**Right**:
```
User: "Evaluate SAP-004"
Agent: *Runs evaluation, generates gap report*
Agent: "Gap identified: Coverage 65% < 85%. Shall I implement the fix (write 8 tests)?"
*Waits for user confirmation*
```

**Why**: Evaluation identifies gaps. Implementation fixes gaps. Two separate steps.

### Pitfall 2: Reporting Stale Evaluation Results

**Wrong**:
```
Agent: "According to evaluation from 3 months ago, SAP-004 is at Level 1"
```

**Right**:
```bash
# 1. Check if evaluation is recent
if last_evaluation_age > 30_days:
    # 2. Re-run evaluation
    python scripts/sap-evaluator.py --quick SAP-004

# 3. Report fresh results
Agent: "SAP-004 current level: 2 (evaluated just now)"
```

**Why**: Adoption state changes. Always use fresh data.

### Pitfall 3: Generic Recommendations

**Wrong**:
```
Recommendation: Adopt best practices for testing
Action: Improve code quality
```

**Right**:
```
Recommendation: Achieve 85% coverage (SAP-004 Level 2 criteria)
Action: Write 8 tests for API handlers in tests/test_api.py
Files: src/api/handlers.py (lines 45-92, currently untested)
Template: tests/test_example.py (copy pattern)
Validation: pytest --cov=src --cov-report=html && open htmlcov/index.html
```

**Why**: Specific, agent-executable instructions. No ambiguity.

### Pitfall 4: Ignoring Blockers

**Wrong**:
```
Plan:
- Sprint 1: Install SAP-017 (chora-compose integration)
- Sprint 2: Install SAP-011 (docker operations)
```

**Right**:
```
Blocker detected: SAP-017 depends on SAP-011

Corrected plan:
- Sprint 1: Install SAP-011 (docker operations) - DEPENDENCY
- Sprint 2: Install SAP-017 (chora-compose integration) - UNBLOCKED
```

**Why**: Check sap-catalog.json for dependencies before planning.

### Pitfall 5: Analysis Paralysis

**Wrong**:
```
Agent: *Runs 30-minute strategic analysis*
Agent: *Generates 50-page report*
Agent: *Lists 47 gaps across 18 SAPs*
User: *Overwhelmed, takes no action*
```

**Right**:
```
Agent: *Runs quick check*
Agent: "Top 3 priorities identified. Focus on Priority 1 this sprint?"
User: "Yes"
Agent: *Deep dive on Priority 1 only*
Agent: "Here are 3 concrete actions for Priority 1. Shall I create tasks?"
```

**Why**: Actionable > Comprehensive. Start small, iterate.

---

## LLM-Specific Guidance

### Token Budget Management

**Quick Check**: 5-10k tokens
- Read sap-catalog.json (2k)
- Run validation commands (1k output)
- Format terminal output (2k)

**Deep Dive**: 30-50k tokens
- Read adoption-blueprint.md (5k)
- Read relevant files (10-20k)
- LLM analysis prompt (5k)
- Format markdown report (10k)

**Strategic**: 100-150k tokens
- Read all SAP metadata (20k)
- Git history analysis (30k)
- LLM roadmap generation (30k)
- Format YAML + markdown (20k)

**Checkpoint Pattern**: Every 5-10 interactions, summarize progress to free context.

### Context Loading Strategy

**Phase 1 (Essential)**: Load first
1. sap-catalog.json (SAP metadata)
2. Target SAP's protocol-spec.md (evaluation criteria)
3. Current repo state (quick file checks)

**Phase 2 (Analysis)**: Load if deep dive
1. adoption-blueprint.md (Level criteria)
2. Relevant codebase files (tests, config, etc.)
3. Git history (ledger updates, commits)

**Phase 3 (Planning)**: Load if strategic
1. All SAP ledgers (historical data)
2. events.jsonl (timeline)
3. Project roadmap docs (integration)

### Self-Assessment Prompt

**When evaluating your own SAP usage** (meta-evaluation):

```markdown
As an AI agent, evaluate your own use of SAP-009 (Agent Awareness):

1. Do you read AGENTS.md at session start? (Level 1 criterion)
2. Do you use domain-specific AGENTS.md files? (Level 2 criterion)
3. Do you optimize context loading based on task complexity? (Level 3 criterion)

Evidence:
- [Check your own tool usage history this session]
- [Did you Read AGENTS.md? Yes/No]
- [Token budget: X/200k used]

Self-assessment result:
- Current level: [0/1/2/3]
- Gaps: [What you're not doing]
- Actions: [How to improve]
```

**Why**: Agents should self-optimize SAP usage patterns.

### Error Recovery

**If evaluation fails**:
```python
try:
    result = run_deep_dive("SAP-004")
except LLMTimeoutError:
    # Fallback: Quick check only
    result = run_quick_check("SAP-004")
    warn_user("Deep dive failed, showing quick check results only")
except SAPNotFoundError:
    suggest_installation("SAP-004")
except ValidationCommandError as e:
    report_validation_failure(e)
```

**Always have fallback**: Quick check is lightweight, always works.

---

## Integration with Other SAPs

### SAP-009 (Agent Awareness) Integration

**This SAP extends SAP-009**:
- SAP-009 teaches you to read AGENTS.md
- SAP-019 teaches you to evaluate if you're reading it well

**Self-evaluation checklist**:
- [ ] Did I read AGENTS.md at session start? (SAP-009 Level 1)
- [ ] Am I using domain-specific AGENTS.md? (SAP-009 Level 2)
- [ ] Am I optimizing context budget? (SAP-009 Level 3)

### SAP-013 (Metrics Tracking) Integration

**Evaluation metrics feed into SAP-013**:
```python
from utils.claude_metrics import ClaudeROICalculator

# Track SAP adoption as part of ROI
calc = ClaudeROICalculator()
calc.track_sap_adoption(SAPAdoptionMetric(
    sap_id="SAP-004",
    adoption_level=2,
    hours_invested=3.5,
    estimated_hours_saved=12.0  # From improved testing efficiency
))
```

### SAP-001 (Inbox Coordination) Integration

**Use coordination requests for cross-repo adoption**:
```bash
# If evaluation identifies need for coordination
python scripts/create-coordination-request.py \
  --title "Adopt SAP-016 in chora-compose" \
  --priority P1 \
  --deliverables "Install link validation, fix 12 broken links"
```

### SAP-012 (Development Lifecycle) Integration

**Evaluation fits into lifecycle phases**:
- **Phase 2 (Sprint Planning)**: Run strategic analysis → generate roadmap
- **Phase 5 (Implementation)**: Use deep dive results to guide coding
- **Phase 8 (Monitoring)**: Track adoption progress over sprints

---

## Quick Decision Tree

```
User asks about SAPs
    ├─> "Is SAP-X installed?" → File check (5s)
    ├─> "How's SAP adoption?" → Quick check all SAPs (30s)
    ├─> "How can we improve SAP-X?" → Deep dive (5min)
    ├─> "What should we adopt next?" → Strategic analysis (30min)
    └─> "Show adoption progress" → Historical analysis (30min)

Gap identified
    ├─> Impact: High + Effort: Low → Priority P0 (this sprint)
    ├─> Impact: High + Effort: High → Priority P1 (plan carefully)
    ├─> Impact: Low + Effort: Low → Priority P2 (next sprint)
    └─> Impact: Low + Effort: High → Defer (future)

User wants to fix gap
    ├─> Use TodoWrite → Create task list
    ├─> Execute actions → Implement fixes
    ├─> Validate → Run evaluation again
    └─> Track → Update ledger, log event
```

---

## Validation Checklist (For Agents)

Before reporting evaluation results, verify:

- [ ] Evaluation is recent (<30 days old) or freshly run
- [ ] All gaps are validated (not guessed/hypothetical)
- [ ] Actions are concrete (tool, file, location, content specified)
- [ ] Priorities consider dependencies (no blocked items ranked first)
- [ ] Effort estimates are realistic (based on adoption-blueprint)
- [ ] Validation commands are provided (user can verify)
- [ ] Reports are saved (git-committable format)
- [ ] Events are logged (adoption-history.jsonl updated)

---

## Summary (Commit to Memory)

**SAP-019 Self-Evaluation** enables you to:
1. **Assess** adoption depth (3 levels: quick/deep/strategic)
2. **Identify** gaps (prioritized by impact/effort)
3. **Generate** roadmaps (sprint-ready action plans)

**Core principle**: Progressive evaluation - start quick, go deep only when needed.

**Key tool**: `scripts/sap-evaluator.py`

**Integration**: Feeds into SAP-013 (metrics), SAP-001 (coordination), SAP-012 (lifecycle).

**Your role**: Run evaluations, parse results, present actionable recommendations, track progress.
