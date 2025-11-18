---
sap_id: SAP-056
version: 1.0.0
status: Draft
last_updated: 2025-11-16
type: explanation
audience: ai_agents
feature_id: FEAT-SAP-056
requirement_refs:
  - REQ-SAP-056-001
  - REQ-SAP-056-002
---

# Awareness Guide: Lifecycle Traceability (AGENTS.md)

**SAP ID**: SAP-056
**Version**: 1.0.0
**For**: AI Agents (Claude Code, Cursor Composer, etc.)
**Last Updated**: 2025-11-16

---

## 1. Overview for Agents

**What is Lifecycle Traceability?**

A governance system ensuring every artifact (code, test, doc, task) has provenance (why it exists), implementation evidence (what implements it), and validation proof (how it's tested).

**Why Agents Need This**:
- **Context Restoration**: Query feature manifest instead of manual git log search (15 min → <1 min)
- **Impact Analysis**: Understand what breaks if you change feature X (automated dependency graph)
- **Completeness Validation**: Verify feature has tests+docs before marking done
- **Compliance**: Generate audit reports showing requirements→code→tests→docs linkage

**Core Concept**: `feature-manifest.yaml` is single source of truth linking Vision, Features, Requirements, Documentation, Tests, and Code.

**SAP-012 Alignment**: When creating features, follow Documentation-First workflow: write docs, extract BDD tests, implement with TDD. The manifest links all artifacts bidirectionally regardless of creation order

---

## 2. Agent Execution Patterns

### 2.1 Pattern: Context Restoration

**Scenario**: Agent resumes work on existing feature, needs full context

**Without Traceability** (Manual, 15-20 min):
```bash
# Agent must manually search:
git log --grep "auth" | head -20
bd list | grep -i "auth"
find docs -name "*auth*"
grep -r "OAuth" src/
# → Fragmented, incomplete, time-consuming
```

**With Traceability** (<1 min):
```bash
# Agent queries feature manifest:
grep -A 50 "id: FEAT-001" feature-manifest.yaml

# Result: Complete context in one place
# - Vision reference (why feature exists)
# - Requirements (what it must do)
# - Code files (where implemented)
# - Tests (how validated)
# - Docs (where explained)
# - Tasks (work breakdown)
# - Commits (change history)
```

**Agent Implementation**:
```python
import yaml

def restore_feature_context(feature_id: str) -> dict:
    """Restore complete context for feature."""
    with open("feature-manifest.yaml") as f:
        manifest = yaml.safe_load(f)

    for feature in manifest["features"]:
        if feature["id"] == feature_id:
            return {
                "vision": feature["vision_ref"],
                "requirements": [r["description"] for r in feature["requirements"]],
                "code_files": [c["path"] for c in feature["code"]],
                "test_cases": [t["path"] for t in feature["tests"]],
                "documentation": [d["path"] for d in feature["documentation"]],
                "status": feature["status"]
            }
    return None

# Usage:
context = restore_feature_context("FEAT-001")
# → Agent has complete context in <1 second
```

---

### 2.2 Pattern: Impact Analysis

**Scenario**: Agent needs to understand "what breaks if I change feature X?"

**Agent Workflow**:

1. **Load feature manifest**
2. **Identify dependencies** (code files, tests, docs)
3. **Check cross-references** (other features using this code)
4. **Generate impact report**

**Implementation**:
```python
def analyze_feature_impact(feature_id: str) -> dict:
    """Analyze impact of changing a feature."""
    manifest = load_manifest()
    feature = find_feature(manifest, feature_id)

    # Direct impact
    direct_impact = {
        "code_files": len(feature["code"]),
        "test_cases": len(feature["tests"]),
        "documentation": len(feature["documentation"])
    }

    # Downstream dependencies
    downstream = []
    for other_feature in manifest["features"]:
        if other_feature["id"] == feature_id:
            continue
        # Check if other feature references same code files
        shared_code = set(f["path"] for f in feature["code"]) & \
                      set(f["path"] for f in other_feature.get("code", []))
        if shared_code:
            downstream.append({
                "feature_id": other_feature["id"],
                "feature_name": other_feature["name"],
                "shared_files": list(shared_code)
            })

    return {
        "feature": feature_id,
        "direct_impact": direct_impact,
        "downstream_dependencies": downstream,
        "risk_level": "HIGH" if len(downstream) > 0 else "LOW"
    }

# Usage:
impact = analyze_feature_impact("FEAT-001")
# → {
#     "feature": "FEAT-001",
#     "direct_impact": {"code_files": 2, "test_cases": 3, "documentation": 2},
#     "downstream_dependencies": [
#         {"feature_id": "FEAT-002", "shared_files": ["src/auth/providers.py"]}
#     ],
#     "risk_level": "HIGH"
# }
```

---

### 2.3 Pattern: Completeness Validation

**Scenario**: Agent finishes implementing feature, must verify completeness before closing

**Validation Checklist**:
1. ✓ All requirements have ≥1 test with `@pytest.mark.requirement`
2. ✓ All code files listed in manifest
3. ✓ All tests passing
4. ✓ Documentation exists for feature
5. ✓ Git commits link to beads tasks
6. ✓ Beads tasks link to feature

**Agent Implementation**:
```python
def validate_feature_completeness(feature_id: str) -> dict:
    """Validate feature completeness before closing."""
    manifest = load_manifest()
    feature = find_feature(manifest, feature_id)

    # Check 1: Requirements coverage
    requirements_coverage = {}
    for req in feature["requirements"]:
        req_id = req["id"]
        # Count tests for this requirement
        tests_for_req = [t for t in feature["tests"] if t["requirement"] == req_id]
        requirements_coverage[req_id] = {
            "tests_count": len(tests_for_req),
            "passing": all(run_test(t["path"]) for t in tests_for_req)
        }

    # Check 2: Documentation exists
    has_docs = len(feature.get("documentation", [])) > 0

    # Check 3: All tests passing
    all_tests_passing = all(
        run_test(t["path"]) for t in feature["tests"]
    )

    # Check 4: Feature referenced in git commits
    has_commits = len(feature.get("commits", [])) > 0

    return {
        "feature_id": feature_id,
        "complete": all([
            all(c["tests_count"] > 0 for c in requirements_coverage.values()),
            has_docs,
            all_tests_passing,
            has_commits
        ]),
        "requirements_coverage": requirements_coverage,
        "documentation": has_docs,
        "tests_passing": all_tests_passing,
        "commits": has_commits
    }

# Usage:
validation = validate_feature_completeness("FEAT-001")
if not validation["complete"]:
    print(f"⚠️ Feature {feature_id} incomplete:")
    # → Show missing items
```

---

### 2.4 Pattern: Traceability Query

**Scenario**: Agent needs to answer user question "which code implements requirement REQ-001?"

**Query Pattern**:
```python
def query_requirement_implementation(requirement_id: str) -> dict:
    """Find all artifacts implementing a requirement."""
    manifest = load_manifest()

    results = {
        "requirement_id": requirement_id,
        "features": [],
        "code_files": [],
        "tests": [],
        "documentation": []
    }

    for feature in manifest["features"]:
        for req in feature["requirements"]:
            if req["id"] == requirement_id:
                results["features"].append({
                    "id": feature["id"],
                    "name": feature["name"],
                    "status": feature["status"]
                })
                results["code_files"].extend(c["path"] for c in feature["code"])
                results["tests"].extend(
                    t["path"] for t in feature["tests"]
                    if t["requirement"] == requirement_id
                )
                results["documentation"].extend(d["path"] for d in feature["documentation"])

    return results

# Usage:
impl = query_requirement_implementation("REQ-001")
# → {
#     "requirement_id": "REQ-001",
#     "features": [{"id": "FEAT-001", "name": "User Auth", "status": "implemented"}],
#     "code_files": ["src/auth/providers.py"],
#     "tests": ["tests/test_auth.py::test_email_login"],
#     "documentation": ["docs/how-to/auth.md"]
# }
```

---

### 2.5 Pattern: Automated Validation

**Scenario**: Agent runs pre-commit validation to ensure traceability compliance

**Agent Workflow**:

1. **Load feature manifest**
2. **Run 10 validation rules**
3. **Generate report** (markdown)
4. **Block commit if failures** (configurable)

**Implementation** (calls `scripts/validate-traceability.py`):
```bash
# Agent runs before git commit:
python scripts/validate-traceability.py --output validation-report.md

# If failures:
# → Agent shows report to user
# → Suggests fixes
# → Blocks commit (if configured)
```

**Example Report**:
```markdown
# Traceability Validation Report

**Overall Pass Rate**: 92% (110/120 checks)

## Failures

### Rule 2: Bidirectional Linkage (2 failures)

**FEAT-002**: Doc `docs/how-to/backend.md` references `src/backend/server.py`, but feature manifest missing this doc.

**Fix**: Add to FEAT-002:
\`\`\`yaml
documentation:
  - path: docs/how-to/backend.md
    type: how-to
\`\`\`

### Rule 8: Requirement Coverage (1 failure)

**REQ-003**: No tests found with `@pytest.mark.requirement("REQ-003")`

**Fix**: Add test:
\`\`\`python
@pytest.mark.requirement("REQ-003")
def test_requirement_003():
    ...
\`\`\`
```

---

## 3. Agent Tools & Helpers

### 3.1 Manifest Query Helper

**File**: `scripts/query-manifest.py`

```python
#!/usr/bin/env python3
"""Query feature manifest from command line."""

import argparse
import yaml
import json

def query_manifest(query_type: str, query_value: str):
    """Query manifest for traceability information."""
    with open("feature-manifest.yaml") as f:
        manifest = yaml.safe_load(f)

    if query_type == "feature":
        # Find feature by ID
        for feature in manifest["features"]:
            if feature["id"] == query_value:
                print(json.dumps(feature, indent=2))
                return

    elif query_type == "requirement":
        # Find all features implementing requirement
        results = []
        for feature in manifest["features"]:
            for req in feature["requirements"]:
                if req["id"] == query_value:
                    results.append({
                        "feature_id": feature["id"],
                        "feature_name": feature["name"],
                        "code": [c["path"] for c in feature["code"]],
                        "tests": [t["path"] for t in feature["tests"] if t["requirement"] == query_value]
                    })
        print(json.dumps(results, indent=2))

    elif query_type == "code":
        # Find which feature owns code file
        for feature in manifest["features"]:
            for code in feature.get("code", []):
                if code["path"] == query_value:
                    print(json.dumps({
                        "feature_id": feature["id"],
                        "feature_name": feature["name"],
                        "file": query_value
                    }, indent=2))
                    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query feature manifest")
    parser.add_argument("type", choices=["feature", "requirement", "code"])
    parser.add_argument("value", help="ID or path to query")
    args = parser.parse_args()

    query_manifest(args.type, args.value)
```

**Usage**:
```bash
# Find feature by ID:
python scripts/query-manifest.py feature FEAT-001

# Find implementations of requirement:
python scripts/query-manifest.py requirement REQ-001

# Find which feature owns code file:
python scripts/query-manifest.py code src/auth/providers.py
```

---

### 3.2 Validation Script

**File**: `scripts/validate-traceability.py` (provided in SAP-056)

**Agent Usage**:
```bash
# Validate all features:
python scripts/validate-traceability.py

# Validate specific feature:
python scripts/validate-traceability.py --feature FEAT-001

# Output to file:
python scripts/validate-traceability.py --output validation-report.md

# JSON output (for programmatic use):
python scripts/validate-traceability.py --json
```

---

### 3.3 Manifest Generation

**File**: `scripts/generate-feature-manifest.py` (provided in SAP-056)

**Agent Usage** (auto-generate manifest from existing code):
```bash
# Generate manifest entry for feature:
python scripts/generate-feature-manifest.py FEAT-001

# Scan git history + beads tasks to populate:
# - Code files (from git log)
# - Tests (from pytest discovery)
# - Docs (from frontmatter feature_id)
# - Tasks (from beads query with [Feature: FEAT-001])
# - Commits (from git log with [.beads-XXX])
```

---

## 4. Agent Workflows

### 4.1 Workflow: Implementing New Feature

**Steps**:

1. **Create feature manifest entry** (status=planned):
   ```bash
   python scripts/generate-feature-manifest.py --new FEAT-003 \
     --name "Email Notifications" \
     --vision "CHARTER-001:Outcome-3"
   ```

2. **Define requirements**:
   - Edit feature-manifest.yaml
   - Add requirements with acceptance criteria

3. **Create beads tasks**:
   ```bash
   bd create "[Feature: FEAT-003] Implement email service"
   bd create "[Feature: FEAT-003] Add notification templates"
   ```

4. **Implement code**:
   - Write code in src/notifications/
   - Update feature manifest `code` array

5. **Write tests**:
   - Add tests with `@pytest.mark.feature("FEAT-003")` and `@pytest.mark.requirement("REQ-XXX")`
   - Update feature manifest `tests` array

6. **Create documentation**:
   - Write docs/how-to/notifications.md
   - Add frontmatter: `feature_id: FEAT-003`
   - Update feature manifest `documentation` array

7. **Validate completeness**:
   ```bash
   python scripts/validate-traceability.py --feature FEAT-003
   ```

8. **Mark feature complete**:
   - Update status=implemented
   - Set completed date

9. **Emit A-MEM event**:
   ```bash
   # Emit feature_completed event
   python scripts/emit-feature-event.py FEAT-003 completed
   ```

---

### 4.2 Workflow: Refactoring Code

**Steps**:

1. **Identify impacted features**:
   ```bash
   python scripts/query-manifest.py code src/auth/providers.py
   # → FEAT-001, FEAT-002
   ```

2. **Check downstream dependencies**:
   ```bash
   python scripts/analyze-impact.py FEAT-001
   # → Shows FEAT-005 depends on FEAT-001
   ```

3. **Run tests before refactor**:
   ```bash
   pytest --feature FEAT-001 --feature FEAT-002
   ```

4. **Perform refactor**:
   - Modify code
   - Update feature manifest if files added/removed

5. **Run tests after refactor**:
   ```bash
   pytest --feature FEAT-001 --feature FEAT-002 --feature FEAT-005
   ```

6. **Validate traceability intact**:
   ```bash
   python scripts/validate-traceability.py
   ```

7. **Commit with task linkage**:
   ```bash
   git commit -m "refactor(auth): simplify OAuth flow [.beads-xyz789]"
   ```

---

### 4.3 Workflow: Answering User Questions

**Question**: "Which code implements requirement REQ-002?"

**Agent Response**:
```python
impl = query_requirement_implementation("REQ-002")
print(f"Requirement REQ-002 is implemented in:")
print(f"  Feature: {impl['features'][0]['name']} (FEAT-001)")
print(f"  Code: {', '.join(impl['code_files'])}")
print(f"  Tests: {', '.join(impl['tests'])}")
print(f"  Docs: {', '.join(impl['documentation'])}")
```

**Output**:
```
Requirement REQ-002 is implemented in:
  Feature: User Authentication (FEAT-001)
  Code: src/auth/providers.py, src/auth/handlers.py
  Tests: tests/test_auth.py::test_oauth_google, tests/test_auth.py::test_oauth_github
  Docs: docs/user-docs/how-to/authentication.md, docs/dev-docs/reference/auth-api.md
```

---

## 5. Common Agent Mistakes

### 5.1 Mistake: Assuming Manifest is Auto-Updated

**Incorrect Assumption**:
> "I added code file src/new_module.py, manifest will auto-update"

**Reality**: Feature manifest is **manually maintained** (or updated via scripts)

**Correct Approach**:
```yaml
# Agent must explicitly update feature-manifest.yaml:
features:
  - id: FEAT-001
    code:
      - path: src/auth/providers.py
      - path: src/new_module.py        # MUST ADD MANUALLY
```

**Alternative**: Use generation script to sync:
```bash
python scripts/generate-feature-manifest.py --sync FEAT-001
# → Scans git log, updates manifest automatically
```

---

### 5.2 Mistake: Forgetting Bidirectional Links

**Incorrect**:
```yaml
# Doc frontmatter references code:
---
feature_id: FEAT-001
code_references:
  - src/auth/providers.py
---

# But feature manifest doesn't list doc → VALIDATION FAILS
```

**Correct**:
```yaml
# Feature manifest MUST list doc:
features:
  - id: FEAT-001
    documentation:
      - path: docs/how-to/auth.md  # MUST ADD
```

**Agent Rule**: Always update **both directions** when creating linkage.

---

### 5.3 Mistake: Missing Pytest Markers

**Incorrect**:
```python
def test_oauth_login():
    """Test OAuth login."""
    # Missing markers → validation fails
    ...
```

**Correct**:
```python
@pytest.mark.feature("FEAT-001")
@pytest.mark.requirement("REQ-002")
@pytest.mark.integration
def test_oauth_login():
    """Test OAuth login."""
    ...
```

**Agent Rule**: Every test MUST have feature + requirement + type markers.

---

## 6. Performance Optimization

### 6.1 Caching Manifest Queries

**Problem**: Repeated manifest parsing slow for large manifests

**Solution**: Cache parsed manifest in memory

```python
import yaml
from functools import lru_cache

@lru_cache(maxsize=1)
def load_manifest():
    """Load manifest with caching."""
    with open("feature-manifest.yaml") as f:
        return yaml.safe_load(f)

# Usage: load_manifest() only parses once
```

---

### 6.2 Incremental Validation

**Problem**: Validating all features on every commit slow (100+ features = minutes)

**Solution**: Validate only changed features

```bash
# Get changed files since last commit:
git diff --name-only HEAD^

# Identify impacted features:
python scripts/find-impacted-features.py $(git diff --name-only HEAD^)

# Validate only those features:
python scripts/validate-traceability.py --features FEAT-001 FEAT-002
```

---

## 7. Integration with Other SAPs

### 7.1 SAP-010 (Memory System) Integration

**Agent Pattern**: Query past feature implementations for learning

```python
def learn_from_similar_features(feature_id: str):
    """Find similar past features for learning."""
    # Query A-MEM events for feature completions
    events = query_events(event_type="feature_completed")

    # Find features with similar code files
    current_feature = find_feature(load_manifest(), feature_id)
    current_code = set(c["path"] for c in current_feature["code"])

    similar_features = []
    for event in events:
        past_feature_id = event["feature_id"]
        past_feature = find_feature(load_manifest(), past_feature_id)
        past_code = set(c["path"] for c in past_feature.get("code", []))

        # Check overlap
        overlap = len(current_code & past_code) / max(len(current_code), 1)
        if overlap > 0.3:  # 30%+ overlap
            similar_features.append({
                "feature_id": past_feature_id,
                "overlap": overlap,
                "knowledge_notes": event.get("knowledge_notes", [])
            })

    return similar_features
```

---

### 7.2 SAP-015 (Beads) Integration

**Agent Pattern**: Auto-create beads tasks from feature requirements

```python
def create_tasks_from_feature(feature_id: str):
    """Create beads tasks for all requirements."""
    feature = find_feature(load_manifest(), feature_id)

    for req in feature["requirements"]:
        task_title = f"[Feature: {feature_id}] {req['description']}"
        # Create beads task
        subprocess.run(["bd", "create", task_title])
```

---

## 8. Version History

**1.0.0** (2025-11-16): Initial awareness guide
- 5 core agent patterns (context restoration, impact analysis, validation, queries, automated validation)
- 3 agent workflows (new feature, refactoring, answering questions)
- 3 helper scripts (query, validate, generate)
- Common mistakes and performance optimizations
