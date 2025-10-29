# Adopter Learnings: Executable How-To Guides (mcp-server-n8n)

**Source:** mcp-server-n8n adopter plan
**Created:** 2025-10-26
**Status:** Integration recommendations approved
**Integration Target:** chora-base v3.4.0 or later

---

## Executive Summary

### The Innovation

The mcp-server-n8n adopter developed a **dual-purpose documentation pattern** where how-to guides serve as:

1. **User documentation** - Help users accomplish real tasks with clear, step-by-step instructions
2. **E2E test scenarios** - Claude Desktop can execute them as integration tests with validation

### Why This Matters

**Problem Solved:**
- Documentation drifts from implementation (documentation rot)
- Tests exist but aren't readable as user guides
- No automated way to validate that documentation actually works

**Solution:**
- Documentation that's guaranteed to stay accurate (it's tested!)
- Test scenarios that are guaranteed to be readable (they're docs!)
- AI agents can execute guides directly as validation
- Perfect alignment with Documentation-Driven Design (DDD) workflow

### Value Proposition for chora-base

This approach **extends our existing documentation standard** (v1.6.0+) with:
- Executable documentation pattern
- Coverage matrix generation (visibility into doc/test gaps)
- Test report templates (standardized validation output)
- Bidirectional traceability (docs ↔ BDD ↔ tests)

**Compatibility:** Builds on our existing extract_tests.py, DOCUMENTATION_STANDARD.md, and Diataxis structure.

---

## Detailed Analysis of Their Approach

### 1. Enhanced Frontmatter Schema

**Their Innovation:**
```yaml
---
title: "How to Discover Available Workflows"
type: how-to
test_extraction: true
execution_mode: claude-desktop
e2e_test_id: discover-workflows-basic
audience: beginners
category: workflows
estimated_time: 5 minutes
last_updated: 2025-10-26
validates:
  - feature: Sprint 2 Story 5 - List Workflows
  - tool: list_workflows
  - tool: get_workflow
related:
  - path/to/related-guide.md
prerequisites:
  - n8n instance running with API access
  - mcp-server-n8n configured in Claude Desktop
---
```

**Key Fields:**
- `test_extraction: true` - Mark as executable documentation
- `execution_mode` - How to execute (claude-desktop, api, manual)
- `e2e_test_id` - Unique identifier for test tracking
- `validates` - Links to features, stories, tools being validated
- `estimated_time` - User expectation setting
- `prerequisites` - Clear requirements checklist

**Learning for chora-base:**
Our frontmatter schema (DOCUMENTATION_STANDARD.md) already supports most of this! We just need to add:
- `execution_mode` field
- `e2e_test_id` field
- Extend `validates` to support feature/story/tool references

---

### 2. Natural Language Execution Pattern

**Their Innovation:**

```markdown
### Step 1: Discover Available Workflows

**Using Claude Desktop:**
You: "List all available workflows in my n8n instance"

**What Claude Does:**

Calls `list_workflows` with:
```json
{
  "active_only": false
}
```

Expected Response:
Claude: "I found 12 workflows in your n8n instance:

1. Daily Backup (ID: 123, active)
2. Email Processing (ID: 456, active)
..."

Validation:
You: "Verify that the backup workflow is in the list"
```

**Pattern Breakdown:**

1. **Natural language command** - What user actually types to Claude
2. **Implementation details** - What Claude does under the hood (tool call + parameters)
3. **Expected response** - What user should see (templated)
4. **Validation step** - How to verify it worked

**Learning for chora-base:**

This pattern is **perfect for:**
- Claude Desktop users (MCP server interaction)
- Claude Code users (executing documented workflows)
- API users (validating integration behavior)

**Template for chora-base:**
```markdown
### Step [N]: [Action Verb] [Object]

**Using [Interface]:**
You: "[Natural language command]"

**What Claude Does:**
[Implementation details - optional for users, required for validation]

Expected Response:
Claude: "[Expected output with placeholders]"

Validation:
You: "[How to verify success]"
```

---

### 3. Bidirectional Traceability

**Their Innovation:**

```markdown
## Related BDD Scenarios

This how-to validates these BDD scenarios:
- [list-workflows.feature](../../tests/bdd/features/list-workflows.feature)
  - Scenario: List all workflows
  - Scenario: Filter by active status
  - Scenario: Filter by tags
```

**Traceability Chain:**

1. **Feature/Story** → BDD Scenario (Given/When/Then)
2. **BDD Scenario** → How-To Guide (executable documentation)
3. **How-To Guide** → E2E Test (Claude execution)
4. **E2E Test** → Test Report (validation results)
5. **Test Report** → Feature Validation (close the loop!)

**Learning for chora-base:**

This creates a **closed-loop validation system**:
- Features are specified (stories/requirements)
- Behaviors are tested (BDD scenarios)
- Usage is documented (how-to guides)
- Documentation is validated (E2E execution)
- Results inform improvements (test reports)

**Integration opportunity:**
- Add `validates.bdd_scenario: path/to/feature.feature` to frontmatter
- Create `scripts/validate_traceability.py` to check links
- Generate traceability matrix showing coverage

---

### 4. Coverage Matrix

**Their Innovation:**

```markdown
## Test Coverage Matrix

| Tool | Unit Tests | BDD Scenarios | How-To Guides | E2E Validated |
|------|-----------|---------------|---------------|---------------|
| list_workflows | 23 | 12 | 3 | ✅ |
| get_workflow | 27 | 15 | 2 | ✅ |
| search_workflows | 32 | 18 | 1 | ✅ |
| execute_workflow | 26 | 20 | 3 | ✅ |
| get_execution_status | 23 | 14 | 2 | ✅ |
| list_recent_executions | 20 | 16 | 2 | ✅ |
```

**Benefits:**

1. **Gap Analysis** - See what's tested but not documented (or vice versa)
2. **Completeness Tracking** - Visual indicator of coverage goals
3. **Prioritization** - Focus documentation efforts on gaps
4. **Stakeholder Communication** - Show progress toward 100% coverage

**Learning for chora-base:**

We should create a **coverage matrix generator** that:
- Scans codebase for unit tests (pytest files)
- Parses how-to guides (frontmatter with `validates` field)
- Detects BDD scenarios (if using behave/pytest-bdd)
- Identifies E2E validated guides (`test_extraction: true`)
- Generates markdown table

**Implementation:**
```python
# scripts/generate_coverage_matrix.py
def scan_unit_tests(test_dir: Path) -> dict[str, int]:
    """Count unit tests per module/tool."""
    pass

def scan_howto_guides(docs_dir: Path) -> dict[str, list[str]]:
    """Find how-to guides validating each tool."""
    pass

def scan_bdd_scenarios(features_dir: Path) -> dict[str, int]:
    """Count BDD scenarios per feature."""
    pass

def generate_matrix(output_path: Path) -> None:
    """Generate coverage matrix markdown table."""
    pass
```

---

### 5. Test Report Structure

**Their Innovation:**

When Claude executes a guide, it generates this report:

```markdown
# Test Execution Report
## How-To: Discover Available Workflows
**Test ID:** discover-workflows-basic
**Executed:** 2025-10-26 14:30:00
**Duration:** 45s
**Result:** ✅ PASSED

---

## Step Results

### Step 1: List all workflows ✅
- **Command:** `list_workflows(active_only=False)`
- **Response:** OK (12 workflows found)
- **Validation:** ✅ PASSED - Backup workflow present
- **Duration:** 12s

### Step 2: Examine workflow details ✅
- **Command:** `get_workflow(workflow_id=123)`
- **Response:** OK
- **Validation:** ✅ PASSED - All fields populated
- **Duration:** 8s

---

## Summary

**Total Steps:** 2
**Passed:** 2 (100%)
**Failed:** 0 (0%)
**Warnings:** 0 (0%)
**Total Duration:** 45s

---

## Tool Coverage

| Tool | Called | Success | Errors |
|------|--------|---------|--------|
| list_workflows | 1 | 1 | 0 |
| get_workflow | 1 | 1 | 0 |

---

## Recommendations

✅ All tool integrations working
✅ Documentation accurate
ℹ️ Consider adding pagination example
```

**Learning for chora-base:**

This report format provides:
- **Immediate feedback** - Developers see what failed
- **Metrics** - Duration, success rate for optimization
- **Actionable recommendations** - What to improve
- **Coverage tracking** - Which tools were exercised

**Template for chora-base:**

Create `templates/test-report-template.md` with:
- Header section (metadata)
- Step results (per-step breakdown with status icons)
- Summary section (aggregate metrics)
- Tool coverage table
- Issues found section (errors/warnings)
- Recommendations section (next steps)

---

## Integration Recommendations for chora-base

### ✅ Phase 1: Documentation Standard Enhancement (HIGH PRIORITY)

**Goal:** Enable executable documentation pattern in chora-base.

**Changes:**

1. **Update DOCUMENTATION_STANDARD.md**
   - Add `execution_mode` field to frontmatter schema
   - Add `e2e_test_id` field to frontmatter schema
   - Extend `validates` field to support feature/story/tool references
   - Add section "Writing Executable How-To Guides"
   - Include examples from mcp-n8n approach

2. **Update validate_docs.py**
   - Validate new frontmatter fields
   - Check `e2e_test_id` uniqueness
   - Validate `validates` references (if BDD features exist)

3. **Create user-docs/how-to/write-executable-how-to-guides.md**
   - Template for executable how-to guides
   - Natural language execution pattern
   - Expected output specification
   - Validation step format
   - Complete example end-to-end

4. **Create templates/test-report-template.md**
   - Standard report format for Claude execution
   - Sections for metadata, steps, summary, coverage, recommendations
   - Markdown template with placeholders

5. **Update 1-2 existing how-to guides as examples**
   - Add new frontmatter fields
   - Apply natural language execution pattern
   - Show validation steps

**Effort:** 8-10 hours

**Deliverables:**
- ✅ Enhanced schema supports executable docs
- ✅ Validation enforces quality
- ✅ Template and examples for adopters
- ✅ Test report template for standardization

**Benefits:**
- Adopters can write living documentation
- Documentation can't drift from implementation
- AI agents have clear execution patterns

---

### ✅ Phase 2: Coverage Matrix Generator (MEDIUM PRIORITY)

**Goal:** Give adopters visibility into documentation/test coverage gaps.

**Changes:**

1. **Create scripts/generate_coverage_matrix.py**
   - Scan codebase for unit tests (pytest discovery)
   - Parse how-to guide frontmatter (`validates` field)
   - Detect BDD scenarios (if using behave/pytest-bdd)
   - Identify E2E validated guides (`test_extraction: true`)
   - Generate COVERAGE_MATRIX.md with table

2. **Update .github/workflows/docs-quality.yml**
   - Add optional job: `generate-coverage-matrix`
   - Run on push to main (not PRs)
   - Upload matrix as artifact
   - Display summary in logs

3. **Update DOCUMENTATION_STANDARD.md**
   - Add section "Coverage Matrix"
   - Document usage: `python scripts/generate_coverage_matrix.py`
   - Show example matrix table

4. **Generate example coverage matrix**
   - Run script on chora-base itself
   - Include in documentation as example

**Effort:** 5-6 hours

**Deliverables:**
- ✅ Script generates coverage matrix
- ✅ CI integration available (opt-in)
- ✅ Documentation updated
- ✅ Example matrix generated

**Benefits:**
- Visual gap analysis
- Prioritization tool for documentation efforts
- Stakeholder communication aid

---

### ✅ Phase 3: Claude Integration (MEDIUM PRIORITY)

**Goal:** Make it easy for Claude users to execute how-to guides.

**Changes:**

1. **Update CLAUDE_SETUP_GUIDE.md**
   - Add section "Executing How-To Guides"
   - Natural language execution pattern
   - Test report generation
   - Example of Claude executing a guide

2. **Update blueprints/CLAUDE.md.blueprint**
   - Add section "Executable Documentation"
   - Reference to write-executable-how-to-guides.md
   - Project-specific execution tips

3. **Update claude/FRAMEWORK_TEMPLATES.md**
   - Add template for test execution
   - Add template for test report generation
   - Include validation patterns

4. **Create complete example**
   - Pick an existing how-to guide
   - Show Claude executing it
   - Show generated test report
   - Include in examples/

**Effort:** 4-5 hours

**Deliverables:**
- ✅ Claude users know how to execute guides
- ✅ Examples demonstrate the pattern
- ✅ Integration with Claude-specific features

**Benefits:**
- Claude Desktop users can validate MCP servers
- Claude Code users can execute documented workflows
- Living documentation becomes executable

---

### 🤔 Future Considerations (Optional)

#### BDD Integration (IF adopters use BDD)

**What:** Deep integration with Behave or pytest-bdd.

**Features:**
- Auto-generate how-to guides from BDD scenarios
- Validate bidirectional links (BDD ↔ How-To)
- Generate traceability matrix

**Decision:** Wait for adopter feedback. Not all projects use BDD.

---

#### Enhanced extract_tests.py

**What:** Extend test extraction to handle natural language patterns.

**Features:**
- Detect "Using Claude Desktop:" sections
- Generate mock Claude responses
- Create expected output assertions
- Natural language test descriptions

**Decision:** Low priority. Our Phase 4 extract_tests.py is already powerful.

---

## Alignment with chora-base Philosophy

### ✅ Perfect Fit with Existing Features

1. **DOCUMENTATION_STANDARD.md (v1.6.0)**
   - Already has frontmatter schema ✅
   - Already validates documentation ✅
   - Just needs extension for execution fields

2. **extract_tests.py (v1.7.0 Phase 4)**
   - Already extracts tests from docs ✅
   - Already handles fixtures, async, parameterized ✅
   - Can be enhanced for natural language patterns

3. **Diataxis Structure**
   - user-docs/how-to/ already exists ✅
   - How-to guides already task-oriented ✅
   - Perfect fit for executable pattern

4. **CLAUDE.md Integration**
   - Claude-specific setup guide exists ✅
   - Pattern library exists (/claude/) ✅
   - Natural extension for execution patterns

5. **Documentation-Driven Design (v3.2.0)**
   - DDD workflow already established ✅
   - Write docs first, then implement ✅
   - Executable docs = ultimate DDD validation!

### 🎯 Key Philosophical Alignment

**Their Approach:**
- Documentation-as-Product → We agree! (v1.6.0)
- Living Documentation → We do this! (extract_tests.py)
- Diataxis compliance → We follow this!
- AI agent as first-class user → AGENTS.md and CLAUDE.md

**New Insight:**
- **Executable how-to guides** = E2E test scenarios
- Natural language execution pattern for AI agents
- Bidirectional traceability closes validation loop

**This is our DDD philosophy taken to its logical conclusion!**

---

## What We Learn from Their Approach

### 1. Documentation-Driven Testing (DDT)

**Traditional:**
1. Write requirements
2. Write code
3. Write tests
4. Write documentation (maybe)
5. Documentation drifts over time ❌

**mcp-n8n Approach (DDT):**
1. Write how-to guide (with test_extraction: true)
2. Execute guide as E2E test
3. Implementation must match documented behavior
4. Guide stays accurate (because it's tested!) ✅

**Insight:** Documentation can DRIVE testing, not just describe it.

---

### 2. Natural Language as Test DSL

**Traditional Test Code:**
```python
def test_list_workflows():
    response = client.post("/list_workflows", json={"active_only": False})
    assert response.status_code == 200
    assert len(response.json()["workflows"]) > 0
```

**mcp-n8n Approach:**
```markdown
You: "List all available workflows"

Expected Response:
Claude: "I found 12 workflows..."

Validation:
You: "Verify backup workflow is present"
```

**Insight:** Natural language = executable spec for AI agents.

---

### 3. Coverage as First-Class Metric

**Traditional:**
- Code coverage: 85% ✅
- Test coverage: 90% ✅
- Documentation coverage: ??? ❓

**mcp-n8n Approach:**
```
| Tool | Unit | BDD | How-To | E2E |
|------|------|-----|--------|-----|
| list | 23   | 12  | 3      | ✅  |
```

**Insight:** Track documentation like you track code coverage.

---

### 4. AI Agent as QA Engineer

**Traditional:**
- Human writes tests
- CI runs tests
- Human reviews failures

**mcp-n8n Approach:**
- Human writes how-to guide
- Claude executes guide
- Claude generates test report
- Human reviews recommendations

**Insight:** AI can be both user AND validator.

---

## Implementation Priority

### Immediate (v3.4.0)
1. ✅ Enhanced frontmatter schema
2. ✅ Executable how-to guide template
3. ✅ Test report template
4. ✅ Updated validation scripts
5. ✅ Examples

**Rationale:** Low-hanging fruit, high value, builds on existing features.

---

### Next Release (v3.5.0)
1. ✅ Coverage matrix generator
2. ✅ CI integration for coverage
3. ✅ Claude execution patterns
4. ✅ Enhanced extract_tests.py

**Rationale:** More sophisticated tooling once basic pattern is established.

---

### Future (Post v3.5.0)
1. 🤔 BDD bidirectional linking (if demand exists)
2. 🤔 Auto-generation from BDD scenarios
3. 🤔 Traceability matrix generation
4. 🤔 Dashboard for coverage visualization

**Rationale:** Wait for adopter feedback on value.

---

## Success Criteria

### Quantitative
- ✅ Enhanced frontmatter schema with 5+ execution fields
- ✅ Coverage matrix generator script (<300 lines)
- ✅ Test report template created
- ✅ 1-2 example executable how-to guides
- ✅ All new features documented (500+ lines)
- ✅ Zero breaking changes to existing docs

### Qualitative
- ✅ Adopters can write executable how-to guides (with template)
- ✅ Claude can execute guides and generate reports (with examples)
- ✅ Coverage gaps are visible (with matrix)
- ✅ Pattern is well-documented (comprehensive guide)
- ✅ Integration with existing features is seamless (DRY principle)

### User Experience
- ✅ Clear value proposition (living documentation!)
- ✅ Easy to adopt (templates + examples)
- ✅ Optional (doesn't force complexity)
- ✅ Scales well (works for 10 docs or 100 docs)

---

## Risks and Mitigations

### Risk 1: Complexity Creep
**Concern:** Adding too many fields overwhelms new users.

**Mitigation:**
- Make execution fields optional
- Provide simple and advanced examples
- Clear documentation showing when to use what

---

### Risk 2: BDD Assumption
**Concern:** Not all projects use BDD (Behave, pytest-bdd).

**Mitigation:**
- BDD integration is optional
- Coverage matrix works without BDD
- `validates` field supports any reference type

---

### Risk 3: Claude Desktop Only
**Concern:** Pattern seems specific to Claude Desktop + MCP.

**Mitigation:**
- `execution_mode` supports: claude-desktop, api, manual
- Natural language pattern works for any AI agent
- Test extraction works regardless of execution mode

---

### Risk 4: Maintenance Burden
**Concern:** Executable docs need maintenance as implementation changes.

**Mitigation:**
- That's the point! (documentation stays accurate)
- Failing E2E tests alert to documentation drift
- Less maintenance than separate docs + tests

---

## Conclusion

The mcp-server-n8n adopter has **validated our Documentation-Driven Design philosophy** by taking it to its logical conclusion:

1. **Documentation drives implementation** (DDD) ✅
2. **Documentation drives testing** (DDT - their innovation!) ✅
3. **Documentation is tested** (extract_tests.py) ✅
4. **Documentation is executable** (AI agent execution) ✅

**This creates a virtuous cycle:**
- Write how-to guide → Implementation follows guide → Tests validate guide → Guide stays accurate → Users trust documentation

**Integration is straightforward:**
- Extend existing frontmatter schema ✅
- Create templates and examples ✅
- Generate coverage matrix ✅
- Document Claude execution pattern ✅

**Result:** chora-base enables the most sophisticated documentation-driven development workflow available in any template.

---

**Next Steps:**
1. Implement Phase 1 (enhanced schema + templates)
2. Get adopter feedback on coverage matrix value
3. Implement Phase 2 if feedback is positive
4. Document in v3.4.0 release notes

**This is a perfect example of learning from adopters to improve the template!** 🎉

---

**Document Version:** 1.0
**Status:** Approved for integration
**Target Release:** v3.4.0 (Phase 1), v3.5.0 (Phases 2-3)
**Related:**
- [DOCUMENTATION_PLAN.md](../DOCUMENTATION_PLAN.md)
- [DOCUMENTATION_STANDARD.md](../../static-template/DOCUMENTATION_STANDARD.md)
- [CLAUDE_SETUP_GUIDE.md](../CLAUDE_SETUP_GUIDE.md)
