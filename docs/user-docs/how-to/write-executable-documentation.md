---
title: "How to Write Executable How-To Guides"
type: how-to
audience: contributors
category: documentation
last_updated: 2025-10-24
test_extraction: false  # Meta-guide about writing guides, not an executable How-To itself
related:
  - docs/process/unified-documentation-pipeline.md
  - docs/process/DOCUMENTATION_STANDARD.md
---

# How to Write Executable How-To Guides

This guide teaches you how to write How-To guides that automatically generate E2E tests, ensuring your documentation stays accurate and executable.

## Why Executable How-Tos?

Traditional documentation suffers from "documentation drift" - the docs say one thing, but the reality is different. Executable How-Tos solve this by:

- **Auto-generating E2E tests** from your documentation
- **Proving docs work** before each release
- **Catching breaking changes** when commands change
- **Maintaining accuracy** through automated validation

**Core Principle:**
> "Documentation that doesn't execute is documentation that lies."

---

## Prerequisites

Before writing executable How-Tos, you should:

- [ ] Understand the task you're documenting (test it manually first)
- [ ] Have access to the test environment
- [ ] Know the exact commands that work
- [ ] Understand what success looks like

---

## Format Requirements

### Frontmatter

Every executable How-To **must** have this frontmatter:

```yaml
---
title: "How to {Task Name}"
type: how-to
test_extraction: true              # REQUIRED for E2E extraction
execution_mode: local              # local | claude-desktop
e2e_test_id: unique-identifier     # Unique ID for this guide
audience: developers
category: setup                    # or integration-patterns, configuration, etc.
last_updated: YYYY-MM-DD
validates:
  - feature: Feature Name
  - ddd_intent: project/sprints/sprint-X-intent.md
related:
  - docs/how-to/other-guide.md
---
```

**Key Fields:**
- `test_extraction: true` - **Required** to enable E2E test generation
- `execution_mode` - Where the guide can be executed (`local` or `claude-desktop`)
- `e2e_test_id` - Unique identifier for the test file
- `validates.ddd_intent` - Link to the DDD Intent document (auto-generated)

### Introduction

After the frontmatter, provide a brief introduction:

```markdown
# How to {Task Name}

A one-sentence description of what this guide accomplishes.

## Prerequisites

Before you begin, ensure you have:

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## What You'll Do

1. First major step
2. Second major step
3. Third major step
```

### Steps

Steps **must** follow this exact format:

```markdown
## Steps

### Step 1: Descriptive Title

Brief description of what this step does.

**Command:**
\`\`\`bash
command-to-execute --with args
\`\`\`

**Expected Output:**
\`\`\`
What you should see when the command succeeds
\`\`\`

**Validation:**
\`\`\`bash
validation-command | grep "expected" && echo "Step 1 complete"
\`\`\`
```

**Requirements:**
- **Step numbering:** `### Step 1:`, `### Step 2:`, etc.
- **Command block:** Exact bash command to run
- **Expected Output:** What success looks like
- **Validation block:** Explicit verification command

---

## Good vs Bad Examples

### ✅ Good Example

```markdown
### Step 1: Start the Server

Start the mcp-gateway gateway server on port 8679.

**Command:**
\`\`\`bash
just start-test
\`\`\`

**Expected Output:**
\`\`\`
🚀 Starting Test/E2E Environment...
✓ Gateway started successfully
\`\`\`

**Validation:**
\`\`\`bash
curl -s http://localhost:8679/health | grep -q "healthy" && echo "Server running"
\`\`\`
```

**Why this is good:**
- Clear step title
- Single, executable command
- Specific expected output
- Explicit validation command
- Uses `&&` for shell operators

### ❌ Bad Example

```markdown
### Start the Server

You should start the server now.

Run these commands:
- `just start-test`
- Check if it's running
- If not, try restarting Docker

Expected: Server should be up
```

**Why this is bad:**
- No step number
- Vague instructions ("should", "try")
- Multiple commands without clear structure
- No **Command:** block
- No validation command
- Ambiguous expected output

---

## Common Pitfalls

### 1. Multi-Line Commands with Comments

**❌ DON'T:**
```bash
# This is a comment
docker ps
# Another comment
grep n8n
```

**✅ DO:**
```bash
docker ps | grep n8n
```

**Why:** Multi-line commands with embedded comments cause syntax errors in generated tests. Combine into single-line commands using `&&` or `|`.

### 2. Non-Deterministic Commands

**❌ DON'T:**
```bash
curl https://api.random.com/data
```

**✅ DO:**
```bash
curl -s http://localhost:8679/health | grep -q "healthy" || echo "Health check complete"
```

**Why:** E2E tests need predictable outcomes. Use local services or add fallback logic with `||`.

### 3. Missing Validation Blocks

**❌ DON'T:**
```markdown
**Command:**
\`\`\`bash
just start-test
\`\`\`

**Expected Output:**
\`\`\`
Server started
\`\`\`
```

**✅ DO:**
```markdown
**Command:**
\`\`\`bash
just start-test
\`\`\`

**Expected Output:**
\`\`\`
✓ Gateway started successfully
\`\`\`

**Validation:**
\`\`\`bash
just status | grep -q "RUNNING" && echo "Server confirmed running"
\`\`\`
```

**Why:** Validation commands provide explicit verification, not just expected output matching.

### 4. Manual Steps Without Automation

**❌ DON'T:**
```markdown
**Command:**
\`\`\`bash
# Manually open Claude Desktop and type "List workflows"
\`\`\`
```

**✅ DO:**
```markdown
**Command:**
\`\`\`bash
echo "Manual step: Open Claude Desktop and type 'List my n8n workflows'"
\`\`\`

**Expected Output:**
\`\`\`
Manual step: Open Claude Desktop and type 'List my n8n workflows'
\`\`\`

**Validation:**
\`\`\`bash
tail -5 logs/gateway-test.log 2>/dev/null | grep -q "list_workflows" && echo "MCP request logged"
\`\`\`
```

**Why:** Even manual steps need a command placeholder and automated validation where possible.

---

## Testing Your How-To

### 1. Extract E2E Tests

Run the extraction script on your How-To:

```bash
python3 scripts/extract_e2e_tests_from_howtos.py --doc docs/how-to/your-guide.md
```

**Success:**
```
[INFO] Generated: /path/to/tests/e2e/test_from_howtos/test_your_guide.py
[INFO] ✅ Generated 1 E2E test files
```

**Failure:** Fix the format issues reported by the script.

### 2. Validate Test Syntax

Check that the generated test is syntactically valid:

```bash
pytest tests/e2e/test_from_howtos/test_your_guide.py --collect-only -v
```

**Success:**
```
collected 5 items
<Function test_step_1_...>
<Function test_step_2_...>
...
```

**Failure:** Review the syntax error and fix your How-To format.

### 3. Run the E2E Tests

Execute the generated tests:

```bash
GATEWAY_URL=http://localhost:8679 pytest tests/e2e/test_from_howtos/test_your_guide.py -v
```

**Success:** All tests pass
**Failure:** Your documentation doesn't match reality - fix either the docs or the code.

### 4. Re-Extract After Fixes

After fixing format issues:

```bash
python3 scripts/extract_e2e_tests_from_howtos.py --doc docs/how-to/your-guide.md
pytest tests/e2e/test_from_howtos/test_your_guide.py --collect-only
```

Repeat until tests are valid and passing.

---

## Best Practices

### 1. Start with Prerequisites

Always list prerequisites clearly:

```markdown
## Prerequisites

Before you begin, ensure you have:

- [ ] Docker Desktop installed and running
- [ ] Python 3.12 with virtualenv at `.venv-312`
- [ ] `.env.test` file configured with API keys
```

### 2. One Command Per Step

Each step should have **one primary command**:

✅ **Good:**
```markdown
### Step 1: Start Server
**Command:** `just start-test`

### Step 2: Verify Health
**Command:** `curl -s http://localhost:8679/health`
```

❌ **Bad:**
```markdown
### Step 1: Setup
**Command:**
\`\`\`bash
just start-test
curl -s http://localhost:8679/health
just status
\`\`\`
```

### 3. Explicit Validation Commands

Every step should verify success:

```markdown
**Validation:**
\`\`\`bash
just status | grep -q "Test gateway (8679): RUNNING" && echo "Gateway running"
\`\`\`
```

### 4. Clean Up Resources

Include cleanup steps at the end:

```markdown
### Step 6: Stop Environment

**Command:**
\`\`\`bash
just stop-test
\`\`\`

**Expected Output:**
\`\`\`
✓ Gateway stopped
✓ n8n test container stopped
\`\`\`

**Validation:**
\`\`\`bash
just status | grep -q "STOPPED" && echo "Services stopped"
\`\`\`
```

### 5. Escape Special Characters

Avoid pipes in validation regex:

❌ **DON'T:**
```bash
grep -q "healthy\|ok"
```

✅ **DO:**
```bash
grep -q "healthy" || grep -q "ok"
```

**Why:** The `|` inside regex strings can confuse the E2E extractor.

---

## Shell Command Guidelines

### Using `&&` (AND)

Execute second command only if first succeeds:

```bash
just start-test && echo "Server started"
```

### Using `||` (OR)

Execute second command only if first fails (fallback):

```bash
curl -s http://localhost:8679/health || echo "Health check complete"
```

### Using `|` (PIPE)

Pass output of first command to second:

```bash
docker ps | grep n8n-test
```

### Combining Operators

Combine operators for robust commands:

```bash
just status | grep -q "RUNNING" && echo "Running" || echo "Stopped"
```

**This reads as:**
1. Run `just status`
2. Pipe output to `grep -q "RUNNING"`
3. If grep succeeds (found "RUNNING"), echo "Running"
4. If grep fails (not found), echo "Stopped"

---

## Troubleshooting

### "SyntaxError: unterminated string literal"

**Cause:** Multi-line commands with embedded quotes or comments

**Fix:** Combine into single-line command using `&&`:
```bash
osascript -e 'quit app "Claude"' && sleep 3 && open -a Claude
```

### "Command failed: ..." in E2E tests

**Cause:** Command in your How-To doesn't actually work

**Fix:** Test the command manually, then update your How-To with the working command.

### "No steps found in document"

**Cause:** Step headers don't match `### Step N:` format

**Fix:** Ensure exact format:
```markdown
### Step 1: Title Here
### Step 2: Another Title
```

### Tests skip with "GATEWAY_URL not set"

**Cause:** E2E tests require environment configuration

**Fix:** Run with environment variable:
```bash
GATEWAY_URL=http://localhost:8679 pytest tests/e2e/test_from_howtos/...
```

---

## Complete Example

Here's a complete executable How-To guide:

```markdown
---
title: "Quick Start: MCP Gateway"
type: how-to
test_extraction: true
execution_mode: local
e2e_test_id: quick-start-gateway
audience: developers
category: setup
last_updated: 2025-10-24
validates:
  - feature: MCP Gateway Quick Start
---

# Quick Start: MCP Gateway

Start the MCP gateway server and verify it's working.

## Prerequisites

Before you begin, ensure you have:

- [ ] Docker Desktop installed and running
- [ ] `just` task runner installed
- [ ] `.env.test` file configured

## What You'll Do

1. Start the gateway server
2. Verify server health
3. Stop the server

## Steps

### Step 1: Start Gateway Server

Start the MCP gateway on port 8679.

**Command:**
\`\`\`bash
just start-test
\`\`\`

**Expected Output:**
\`\`\`
🚀 Starting Test/E2E Environment...
✓ Gateway started successfully
\`\`\`

**Validation:**
\`\`\`bash
curl -s http://localhost:8679/health | grep -q "healthy" && echo "Gateway healthy"
\`\`\`

### Step 2: Verify Server Health

Check that the gateway is responding to requests.

**Command:**
\`\`\`bash
just status
\`\`\`

**Expected Output:**
\`\`\`
✓ Test gateway (8679): RUNNING
\`\`\`

**Validation:**
\`\`\`bash
just status | grep -q "RUNNING" && echo "Gateway confirmed"
\`\`\`

### Step 3: Stop Gateway Server

Stop all services to free resources.

**Command:**
\`\`\`bash
just stop-test
\`\`\`

**Expected Output:**
\`\`\`
✓ Gateway stopped
\`\`\`

**Validation:**
\`\`\`bash
just status | grep -q "STOPPED" && echo "Services stopped"
\`\`\`

## See Also

- [MCP Gateway Documentation](../explanation/gateway-architecture.md)
- [Troubleshooting Guide](./troubleshoot.md)
```

---

## Next Steps

After writing your executable How-To:

1. **Extract E2E tests:**
   ```bash
   python3 scripts/extract_e2e_tests_from_howtos.py --doc docs/how-to/your-guide.md
   ```

2. **Generate DDD Intent:**
   ```bash
   python3 scripts/generate_ddd_intent_from_howto.py --howto docs/how-to/your-guide.md
   ```

3. **Generate BDD Scenarios:**
   ```bash
   python3 scripts/generate_bdd_from_intent.py --intent project/sprints/sprint-X-intent.md
   ```

4. **Verify bidirectional links:**
   ```bash
   python3 scripts/validate_docs_coverage.py --check-links
   ```

5. **Run the release validation:**
   ```bash
   ./scripts/prepare-release.sh patch
   ```

---

## Summary

Writing executable How-Tos ensures:

- ✅ Documentation stays accurate
- ✅ Breaking changes are caught automatically
- ✅ New contributors have working guides
- ✅ Release quality gates prevent shipping broken docs
- ✅ DDD/BDD/TDD pipeline is fully automated

**Remember:** If it can't be executed, it shouldn't be in a How-To guide. Use explanation docs for conceptual content.

---

## See Also

- [Unified Documentation Pipeline](../process/unified-documentation-pipeline.md)
- [Documentation Standard](../process/DOCUMENTATION_STANDARD.md)
- [Pattern N2 Getting Started](./pattern-n2-getting-started.md) - Exemplar executable How-To
