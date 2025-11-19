# SAP-053: Conflict Resolution - Protocol Specification

**Document Type**: Protocol Specification
**SAP ID**: SAP-053
**SAP Name**: Conflict Resolution
**Version**: 1.0.0 (Phase 1 - Design)
**Status**: Draft
**Created**: 2025-11-18
**Last Updated**: 2025-11-18
**Author**: Claude (AI peer) + Victor Piper

---

## Document Purpose

This protocol specification defines the **technical implementation** of SAP-053 (Conflict Resolution). It provides:

1. **Conflict detection algorithms** - How to detect conflicts before merge
2. **Resolution strategies** - File-type-specific resolution approaches
3. **A-MEM integration schema** - Event logging for conflict tracking
4. **Auto-resolution logic** - Safe automated conflict resolution
5. **Escalation protocol** - Decision tree for manual resolution
6. **Tool interfaces** - Scripts, justfile recipes, CI/CD integration

**Audience**: AI agents implementing SAP-053, developers extending conflict resolution tooling

---

## 1. Conflict Detection Algorithms

### 1.1 Pre-Merge Conflict Checker

**Purpose**: Detect merge conflicts BEFORE creating PR or pushing to remote

**Algorithm**:
```python
# scripts/conflict-checker.py

def check_for_conflicts(branch="main"):
    """
    Pre-merge conflict detection.

    Returns:
        {
            "has_conflicts": bool,
            "conflicting_files": [str],
            "conflict_types": {file: type},
            "safe_to_merge": bool
        }
    """
    # Step 1: Fetch latest from remote
    run("git fetch origin")

    # Step 2: Attempt test merge (no-commit)
    result = run(f"git merge --no-commit --no-ff origin/{branch}", check=False)

    # Step 3: Parse conflict markers
    if result.returncode != 0:
        conflicting_files = parse_git_status()
        conflict_types = classify_conflicts(conflicting_files)

        # Step 4: Abort test merge
        run("git merge --abort")

        return {
            "has_conflicts": True,
            "conflicting_files": conflicting_files,
            "conflict_types": conflict_types,
            "safe_to_merge": False
        }
    else:
        # No conflicts, abort test merge
        run("git merge --abort")
        return {
            "has_conflicts": False,
            "conflicting_files": [],
            "conflict_types": {},
            "safe_to_merge": True
        }

def classify_conflicts(files):
    """
    Classify conflicts by type for resolution strategy selection.

    Returns:
        {file: conflict_type}

    Conflict types:
        - "content": Actual content conflict (manual review needed)
        - "whitespace": Whitespace-only conflict (auto-resolvable)
        - "formatting": Code formatting conflict (auto-resolvable)
        - "lockfile": Dependency lockfile conflict (regenerate)
        - "metadata": Generated metadata (regenerate)
    """
    conflict_types = {}

    for file in files:
        # Read conflicting file
        with open(file, 'r') as f:
            content = f.read()

        # Parse conflict markers
        conflicts = extract_conflict_blocks(content)

        # Classify each conflict
        if is_whitespace_only(conflicts):
            conflict_types[file] = "whitespace"
        elif is_formatting_only(conflicts):
            conflict_types[file] = "formatting"
        elif file.endswith(("package-lock.json", "poetry.lock", "Pipfile.lock")):
            conflict_types[file] = "lockfile"
        elif file.endswith((".pyc", ".class", "__pycache__")):
            conflict_types[file] = "metadata"
        else:
            conflict_types[file] = "content"

    return conflict_types
```

**Justfile Recipe**:
```bash
# justfile

# Check for merge conflicts before PR creation
conflict-check branch="main":
    python3 scripts/conflict-checker.py --branch {{branch}} --format text

# Check conflicts with JSON output (for CI/CD)
conflict-check-json branch="main":
    python3 scripts/conflict-checker.py --branch {{branch}} --format json
```

**Exit Codes**:
- `0`: No conflicts, safe to merge
- `1`: Conflicts detected, manual review needed
- `2`: Auto-resolvable conflicts detected
- `3`: Tool error (git command failed)

---

### 1.2 CI/CD Integration

**Purpose**: Prevent merging PRs with unresolved conflicts

**GitHub Actions Workflow** (`.github/workflows/conflict-check.yml`):
```yaml
name: Conflict Detection

on:
  pull_request:
    branches: [main]

jobs:
  conflict-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for merge simulation

      - name: Check for conflicts
        run: |
          python3 scripts/conflict-checker.py --branch main --format json > conflict-report.json

      - name: Analyze conflict report
        run: |
          HAS_CONFLICTS=$(jq -r '.has_conflicts' conflict-report.json)
          CONFLICT_COUNT=$(jq -r '.conflicting_files | length' conflict-report.json)

          if [ "$HAS_CONFLICTS" = "true" ]; then
            echo "❌ Conflicts detected in $CONFLICT_COUNT files"
            echo "Conflicting files:"
            jq -r '.conflicting_files[]' conflict-report.json
            exit 1
          else
            echo "✅ No conflicts detected, safe to merge"
            exit 0
          fi

      - name: Upload conflict report
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: conflict-report
          path: conflict-report.json
```

**Pre-commit Hook Integration** (SAP-051):
```bash
# .git/hooks/pre-push

#!/bin/bash
# SAP-053: Conflict detection before push

echo "Running conflict check..."
python3 scripts/conflict-checker.py --branch main --format text

EXIT_CODE=$?

if [ $EXIT_CODE -eq 1 ]; then
    echo "❌ Conflicts detected. Resolve before pushing."
    echo "Run 'just conflict-resolve' for resolution strategies."
    exit 1
elif [ $EXIT_CODE -eq 2 ]; then
    echo "⚠️  Auto-resolvable conflicts detected."
    echo "Run 'just conflict-auto-resolve' to resolve automatically."
    exit 0
else
    echo "✅ No conflicts detected."
    exit 0
fi
```

---

### 1.3 Conflict Predictor (Optional Enhancement)

**Purpose**: Predict likelihood of conflicts BEFORE editing high-risk files

**Algorithm**:
```python
# scripts/conflict-predictor.py

def predict_conflict_risk(files):
    """
    Predict conflict risk based on:
    1. File edit frequency (high-traffic files = higher risk)
    2. Recent conflict history (A-MEM events)
    3. Multi-developer edit patterns

    Returns:
        {file: risk_level}

    Risk levels: "low" (0-30%), "medium" (30-70%), "high" (70-100%)
    """
    risk_scores = {}

    for file in files:
        # Factor 1: Edit frequency (last 30 days)
        edit_freq = get_commit_count(file, days=30)
        freq_score = min(edit_freq / 10, 1.0)  # Normalize to 0-1

        # Factor 2: Recent conflicts (A-MEM events)
        recent_conflicts = query_memory_events(
            event_type="conflict_resolved",
            file=file,
            days=90
        )
        conflict_score = min(len(recent_conflicts) / 5, 1.0)

        # Factor 3: Multi-developer activity
        contributors = get_recent_contributors(file, days=14)
        multi_dev_score = min(len(contributors) / 3, 1.0)

        # Weighted average
        risk_score = (
            0.4 * freq_score +
            0.4 * conflict_score +
            0.2 * multi_dev_score
        )

        # Classify risk level
        if risk_score < 0.3:
            risk_scores[file] = {"level": "low", "score": risk_score}
        elif risk_score < 0.7:
            risk_scores[file] = {"level": "medium", "score": risk_score}
        else:
            risk_scores[file] = {"level": "high", "score": risk_score}

    return risk_scores

def get_commit_count(file, days=30):
    """Count commits modifying file in last N days."""
    since = f"--since='{days} days ago'"
    result = run(f"git log {since} --oneline -- {file}")
    return len(result.stdout.strip().split('\n'))

def get_recent_contributors(file, days=14):
    """Get unique contributors to file in last N days."""
    since = f"--since='{days} days ago'"
    result = run(f"git log {since} --format='%ae' -- {file}")
    return set(result.stdout.strip().split('\n'))
```

**Justfile Recipe**:
```bash
# Predict conflict risk for staged files
conflict-predict:
    python3 scripts/conflict-predictor.py --files $(git diff --name-only --staged) --format text
```

**Output Example**:
```
Conflict Risk Prediction:

📄 project-docs/sprints/sprint-13.md
   Risk: 🔴 HIGH (85%)
   Reason: 12 commits in last 30 days, 2 conflicts in last 90 days, 2 active contributors
   Recommendation: Communicate with @victorpiper before editing

📄 docs/vision/mcp.md
   Risk: 🟡 MEDIUM (45%)
   Reason: 5 commits in last 30 days, 0 recent conflicts, 1 active contributor
   Recommendation: Standard workflow, monitor for conflicts

📄 scripts/new-script.py
   Risk: 🟢 LOW (15%)
   Reason: 1 commit in last 30 days, 0 recent conflicts, 1 active contributor
   Recommendation: Safe to edit without coordination
```

---

## 2. Resolution Strategies by File Type

### 2.1 Strategy Selection Algorithm

**Purpose**: Choose appropriate resolution strategy based on file type

**Decision Tree**:
```
Conflict detected in file X
│
├─ File type = .md (Markdown)
│  └─ Strategy: MANUAL_REVIEW (docs are semantic, need human judgment)
│
├─ File type = .py, .ts, .js (Code)
│  ├─ Conflict type = whitespace/formatting?
│  │  └─ Strategy: AUTO_RESOLVE_FORMATTING
│  └─ Conflict type = content?
│     └─ Strategy: MANUAL_REVIEW_WITH_OWNERSHIP (use SAP-052 CODEOWNERS)
│
├─ File type = .yaml, .json (Config)
│  ├─ Schema validation available?
│  │  └─ Strategy: SCHEMA_DRIVEN_MERGE
│  └─ No schema?
│     └─ Strategy: MANUAL_REVIEW
│
├─ File type = package-lock.json, poetry.lock (Lockfile)
│  └─ Strategy: REGENERATE_FROM_SOURCE
│
├─ File type = .DS_Store, __pycache__ (Metadata)
│  └─ Strategy: DELETE_AND_REGENERATE
│
└─ Unknown file type
   └─ Strategy: MANUAL_REVIEW (conservative default)
```

**Implementation**:
```python
# scripts/conflict-resolver.py

RESOLUTION_STRATEGIES = {
    "markdown": "MANUAL_REVIEW",
    "code": "MANUAL_REVIEW_WITH_OWNERSHIP",
    "config": "SCHEMA_DRIVEN_MERGE",
    "lockfile": "REGENERATE_FROM_SOURCE",
    "metadata": "DELETE_AND_REGENERATE",
}

FILE_TYPE_MAP = {
    ".md": "markdown",
    ".py": "code",
    ".ts": "code",
    ".js": "code",
    ".yaml": "config",
    ".yml": "config",
    ".json": "config",
    ".toml": "config",
    "package-lock.json": "lockfile",
    "poetry.lock": "lockfile",
    "Pipfile.lock": "lockfile",
    ".DS_Store": "metadata",
    "__pycache__": "metadata",
}

def select_resolution_strategy(file, conflict_type):
    """
    Select resolution strategy based on file type and conflict type.

    Returns:
        {
            "strategy": str,
            "auto_resolvable": bool,
            "requires_ownership": bool,
            "steps": [str]
        }
    """
    # Determine file type
    file_type = get_file_type(file)

    # Special case: whitespace/formatting conflicts are always auto-resolvable
    if conflict_type in ["whitespace", "formatting"]:
        return {
            "strategy": "AUTO_RESOLVE_FORMATTING",
            "auto_resolvable": True,
            "requires_ownership": False,
            "steps": [
                "Accept both changes",
                "Run code formatter (black, prettier, etc.)",
                "Verify formatting consistency"
            ]
        }

    # Select strategy based on file type
    base_strategy = RESOLUTION_STRATEGIES.get(file_type, "MANUAL_REVIEW")

    # Build resolution plan
    if base_strategy == "MANUAL_REVIEW":
        return {
            "strategy": "MANUAL_REVIEW",
            "auto_resolvable": False,
            "requires_ownership": False,
            "steps": [
                "Open file in editor",
                "Review conflict markers (<<<<<<< ======= >>>>>>>)",
                "Choose correct version or merge manually",
                "Remove conflict markers",
                "Test changes",
                "Commit resolution"
            ]
        }

    elif base_strategy == "MANUAL_REVIEW_WITH_OWNERSHIP":
        owner = get_file_owner(file)  # SAP-052 integration
        return {
            "strategy": "MANUAL_REVIEW_WITH_OWNERSHIP",
            "auto_resolvable": False,
            "requires_ownership": True,
            "owner": owner,
            "steps": [
                f"Identify file owner: {owner} (from CODEOWNERS)",
                "Contact owner for resolution guidance",
                "Open file in editor",
                "Review conflict with owner's expertise",
                "Merge changes (owner has jurisdiction per SAP-052)",
                "Remove conflict markers",
                "Test changes",
                "Commit resolution (tag owner in commit message)"
            ]
        }

    elif base_strategy == "SCHEMA_DRIVEN_MERGE":
        return {
            "strategy": "SCHEMA_DRIVEN_MERGE",
            "auto_resolvable": True,  # If schema available
            "requires_ownership": False,
            "steps": [
                "Load config schema (YAML/JSON schema)",
                "Parse both versions (ours, theirs)",
                "Merge using schema rules (prefer non-default values)",
                "Validate merged config against schema",
                "If validation passes: auto-commit",
                "If validation fails: escalate to MANUAL_REVIEW"
            ]
        }

    elif base_strategy == "REGENERATE_FROM_SOURCE":
        return {
            "strategy": "REGENERATE_FROM_SOURCE",
            "auto_resolvable": True,
            "requires_ownership": False,
            "steps": [
                "Delete conflicting lockfile",
                "Regenerate from package.json / pyproject.toml",
                "Run: npm install / poetry lock",
                "Commit regenerated lockfile",
                "Note: This accepts dependency changes from both branches"
            ]
        }

    elif base_strategy == "DELETE_AND_REGENERATE":
        return {
            "strategy": "DELETE_AND_REGENERATE",
            "auto_resolvable": True,
            "requires_ownership": False,
            "steps": [
                "Delete conflicting metadata file",
                "Regenerate from source (or ignore if .DS_Store)",
                "Commit deletion (or add to .gitignore)"
            ]
        }

    else:
        # Unknown strategy, default to manual review
        return {
            "strategy": "MANUAL_REVIEW",
            "auto_resolvable": False,
            "requires_ownership": False,
            "steps": ["Manual resolution required (unknown file type)"]
        }
```

---

### 2.2 Detailed Resolution Strategies

#### Strategy 1: MANUAL_REVIEW

**Use Case**: Documentation (.md), unknown file types

**Process**:
1. Open file in editor
2. Locate conflict markers:
   ```
   <<<<<<< HEAD (your changes)
   Your version of the content
   =======
   Their version of the content
   >>>>>>> branch-name (their changes)
   ```
3. Choose one of:
   - **Accept ours**: Keep your version, discard theirs
   - **Accept theirs**: Keep their version, discard yours
   - **Merge manually**: Combine both versions (requires understanding content)
4. Remove conflict markers
5. Test changes (if applicable)
6. Commit resolution: `git add <file> && git commit -m "Resolve conflict in <file>"`

**Time Estimate**: 5-15 minutes per file

---

#### Strategy 2: MANUAL_REVIEW_WITH_OWNERSHIP (SAP-052 Integration)

**Use Case**: Code files (.py, .ts, .js) with assigned owners

**Process**:
1. Identify file owner using CODEOWNERS (SAP-052):
   ```bash
   just ownership-suggest-reviewers-staged
   ```
2. Contact owner: "I have a conflict in `file.py` (you're the owner). Can you review?"
3. Owner reviews conflict and provides guidance:
   - If owner's changes: Owner resolves
   - If your changes conflict with owner's code: Owner has jurisdiction (SAP-052 Contract 2)
   - If unclear: Pair programming session
4. Resolve conflict following owner's guidance
5. Commit with owner tag:
   ```bash
   git commit -m "Resolve conflict in file.py (reviewed by @owner)"
   ```

**Jurisdiction Rules** (from SAP-052):
- **Single-domain conflict**: Domain owner has jurisdiction
- **Cross-domain conflict**: Both owners collaborate (consensus required)
- **Deadlock**: Escalate to project lead

**Time Estimate**: 10-20 minutes per file (including coordination)

---

#### Strategy 3: SCHEMA_DRIVEN_MERGE

**Use Case**: Configuration files (.yaml, .json) with defined schemas

**Algorithm**:
```python
def schema_driven_merge(file, schema_path):
    """
    Merge config files using schema rules.

    Rules:
    1. For scalar values: Prefer non-default value
    2. For lists: Union (combine unique items)
    3. For objects: Recursive merge
    4. For conflicts with same non-default value: Manual review
    """
    # Load schema
    with open(schema_path) as f:
        schema = yaml.safe_load(f)

    # Parse both versions
    ours = parse_conflict_section(file, section="ours")
    theirs = parse_conflict_section(file, section="theirs")

    # Merge using schema
    merged = {}
    for key in set(list(ours.keys()) + list(theirs.keys())):
        our_value = ours.get(key)
        their_value = theirs.get(key)

        # Get default from schema
        default = schema.get("properties", {}).get(key, {}).get("default")

        # Merge logic
        if our_value == their_value:
            merged[key] = our_value
        elif our_value == default:
            merged[key] = their_value  # Prefer their non-default
        elif their_value == default:
            merged[key] = our_value  # Prefer our non-default
        elif isinstance(our_value, list) and isinstance(their_value, list):
            merged[key] = list(set(our_value + their_value))  # Union
        elif isinstance(our_value, dict) and isinstance(their_value, dict):
            merged[key] = schema_driven_merge_recursive(our_value, their_value)
        else:
            # Both are non-default and different: manual review needed
            return None  # Escalate to MANUAL_REVIEW

    # Validate merged config
    if validate_schema(merged, schema):
        return merged
    else:
        return None  # Validation failed, escalate
```

**Time Estimate**: 2-5 minutes (automated) or 10-15 minutes (manual fallback)

---

#### Strategy 4: REGENERATE_FROM_SOURCE

**Use Case**: Dependency lockfiles (package-lock.json, poetry.lock, Pipfile.lock)

**Process**:
```bash
# Example: poetry.lock conflict

# Step 1: Delete conflicting lockfile
git rm poetry.lock

# Step 2: Regenerate from pyproject.toml
poetry lock

# Step 3: Commit regenerated lockfile
git add poetry.lock
git commit -m "Regenerate poetry.lock (resolve conflict)"

# Note: This accepts dependency updates from both branches
# If dependency versions are incompatible, poetry lock will fail
# → Escalate to manual review of pyproject.toml
```

**Justfile Recipe**:
```bash
# Auto-resolve lockfile conflicts
conflict-resolve-lockfile file:
    #!/usr/bin/env bash
    set -euo pipefail

    if [[ "{{file}}" == "package-lock.json" ]]; then
        git rm package-lock.json
        npm install
        git add package-lock.json
    elif [[ "{{file}}" == "poetry.lock" ]]; then
        git rm poetry.lock
        poetry lock
        git add poetry.lock
    elif [[ "{{file}}" == "Pipfile.lock" ]]; then
        git rm Pipfile.lock
        pipenv lock
        git add Pipfile.lock
    else
        echo "Unknown lockfile type: {{file}}"
        exit 1
    fi

    git commit -m "Regenerate {{file}} (auto-resolve conflict)"
```

**Time Estimate**: 1-3 minutes (automated)

---

#### Strategy 5: DELETE_AND_REGENERATE

**Use Case**: Generated metadata (.DS_Store, __pycache__, build artifacts)

**Process**:
```bash
# Step 1: Delete conflicting file
git rm .DS_Store

# Step 2: Add to .gitignore if not already present
echo ".DS_Store" >> .gitignore

# Step 3: Commit deletion
git add .gitignore
git commit -m "Remove .DS_Store from tracking (resolve conflict)"
```

**Time Estimate**: 1-2 minutes

---

#### Strategy 6: AUTO_RESOLVE_FORMATTING

**Use Case**: Whitespace-only or formatting-only conflicts

**Algorithm**:
```python
def auto_resolve_formatting(file):
    """
    Auto-resolve formatting conflicts by:
    1. Accepting both changes
    2. Running code formatter
    3. Verifying result
    """
    # Step 1: Accept both changes (union merge)
    run(f"git checkout --ours {file}")  # Start with our version
    their_changes = extract_their_changes(file)
    apply_changes(file, their_changes)

    # Step 2: Run appropriate formatter
    if file.endswith(".py"):
        run(f"black {file}")
    elif file.endswith((".ts", ".js")):
        run(f"prettier --write {file}")
    elif file.endswith((".yaml", ".yml")):
        run(f"yamlfmt {file}")
    else:
        # No formatter available, manual review needed
        return False

    # Step 3: Verify no semantic changes
    if verify_semantic_equivalence(file):
        run(f"git add {file}")
        run(f"git commit -m 'Auto-resolve formatting conflict in {file}'")
        return True
    else:
        # Semantic changes detected, revert and escalate
        run(f"git checkout HEAD {file}")
        return False
```

**Time Estimate**: 1-2 minutes (automated)

---

## 3. A-MEM Integration Schema

### 3.1 Event Types

SAP-053 introduces 2 new event types for A-MEM (SAP-010):

#### Event Type 1: `conflict_detected`

**Purpose**: Log when a conflict is detected (pre-merge or during merge)

**Schema**:
```json
{
  "timestamp": "2025-11-18T14:32:15.123456Z",
  "type": "conflict_detected",
  "trace_id": "cord-2025-019-feature-branch",
  "branch": "feature/new-docs",
  "target_branch": "main",
  "conflicting_files": [
    "docs/vision/mcp.md",
    "project-docs/sprints/sprint-13.md"
  ],
  "conflict_types": {
    "docs/vision/mcp.md": "content",
    "project-docs/sprints/sprint-13.md": "content"
  },
  "auto_resolvable": false,
  "detection_method": "pre_merge_check",
  "developer": "alice"
}
```

**Fields**:
- `branch`: Feature branch with conflicts
- `target_branch`: Branch being merged into (usually `main`)
- `conflicting_files`: List of files with conflicts
- `conflict_types`: Conflict classification per file (content, whitespace, formatting, lockfile, metadata)
- `auto_resolvable`: Can conflicts be auto-resolved? (true/false)
- `detection_method`: How conflict was detected (pre_merge_check, ci_cd, manual)
- `developer`: Who triggered the conflict detection

---

#### Event Type 2: `conflict_resolved`

**Purpose**: Log when a conflict is successfully resolved

**Schema**:
```json
{
  "timestamp": "2025-11-18T14:45:32.987654Z",
  "type": "conflict_resolved",
  "trace_id": "cord-2025-019-feature-branch",
  "branch": "feature/new-docs",
  "target_branch": "main",
  "resolved_files": [
    "docs/vision/mcp.md",
    "project-docs/sprints/sprint-13.md"
  ],
  "resolution_strategies": {
    "docs/vision/mcp.md": "MANUAL_REVIEW",
    "project-docs/sprints/sprint-13.md": "MANUAL_REVIEW_WITH_OWNERSHIP"
  },
  "resolution_time_minutes": 12.5,
  "auto_resolved": false,
  "owner_consulted": "@victorpiper",
  "escalation_level": 1,
  "developer": "alice",
  "commit_sha": "a1b2c3d4"
}
```

**Fields**:
- `resolved_files`: Files successfully resolved
- `resolution_strategies`: Strategy used per file
- `resolution_time_minutes`: Time from detection to resolution (float)
- `auto_resolved`: Was resolution automated? (true/false)
- `owner_consulted`: CODEOWNERS owner consulted (if applicable)
- `escalation_level`: 1 (developer), 2 (pair programming), 3 (project lead)
- `commit_sha`: Git commit hash of resolution

---

### 3.2 A-MEM Query Examples

**Query 1: Recent conflicts in last 30 days**
```bash
grep '"type": "conflict_' .chora/memory/events/2025-11.jsonl | \
  jq 'select(.timestamp > "2025-10-18")'
```

**Query 2: Most frequently conflicting files**
```bash
grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | \
  jq -r '.resolved_files[]' | \
  sort | uniq -c | sort -rn | head -10
```

**Output**:
```
5 project-docs/sprints/sprint-13.md
3 docs/vision/mcp.md
2 feature-manifest.yaml
1 justfile
```

**Query 3: Average resolution time by strategy**
```bash
grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | \
  jq -r '[.resolution_strategies[], .resolution_time_minutes] | @tsv' | \
  awk '{sum[$1]+=$2; count[$1]++} END {for (s in sum) print s, sum[s]/count[s]}'
```

**Output**:
```
MANUAL_REVIEW 18.3
MANUAL_REVIEW_WITH_OWNERSHIP 12.5
REGENERATE_FROM_SOURCE 2.1
AUTO_RESOLVE_FORMATTING 1.3
```

---

### 3.3 Knowledge Note Trigger

**Rule**: If a file has ≥2 conflicts within 90 days, create a knowledge note documenting the pattern.

**Automation**:
```python
# scripts/conflict-pattern-detector.py

def check_for_recurring_conflicts():
    """
    Query A-MEM events for recurring conflicts.
    Create knowledge notes for patterns.
    """
    # Query conflict events (last 90 days)
    events = query_memory_events(
        event_type="conflict_resolved",
        days=90
    )

    # Count conflicts per file
    file_conflicts = {}
    for event in events:
        for file in event["resolved_files"]:
            if file not in file_conflicts:
                file_conflicts[file] = []
            file_conflicts[file].append(event)

    # Identify recurring conflicts (≥2 in 90 days)
    recurring_files = {
        file: conflicts
        for file, conflicts in file_conflicts.items()
        if len(conflicts) >= 2
    }

    # Create knowledge notes
    for file, conflicts in recurring_files.items():
        create_conflict_knowledge_note(file, conflicts)

def create_conflict_knowledge_note(file, conflicts):
    """
    Create knowledge note documenting conflict pattern.

    Template:
    - File path
    - Conflict frequency (N conflicts in 90 days)
    - Common conflict types
    - Resolution strategies used
    - Recommended prevention (coordination, domain ownership, etc.)
    - Related events (wikilinks to A-MEM trace IDs)
    """
    # Extract pattern
    conflict_types = [c["conflict_types"].get(file) for c in conflicts]
    strategies = [c["resolution_strategies"].get(file) for c in conflicts]
    avg_time = sum(c["resolution_time_minutes"] for c in conflicts) / len(conflicts)

    # Generate knowledge note
    note_content = f"""---
title: "Conflict Pattern: {file}"
created: {datetime.now().strftime("%Y-%m-%d")}
tags: [conflict-pattern, recurring-conflict, sap-053]
related: {[c["trace_id"] for c in conflicts]}
---

# Conflict Pattern: {file}

**Conflict Frequency**: {len(conflicts)} conflicts in last 90 days
**Average Resolution Time**: {avg_time:.1f} minutes

## Conflict Analysis

**Common Conflict Types**:
{format_list(set(conflict_types))}

**Resolution Strategies Used**:
{format_list(set(strategies))}

## Prevention Recommendations

{generate_prevention_recommendations(file, conflict_types, strategies)}

## Related Events

{format_wikilinks([c["trace_id"] for c in conflicts])}
"""

    # Write knowledge note
    note_path = f".chora/memory/knowledge/notes/conflict-pattern-{sanitize_filename(file)}.md"
    with open(note_path, 'w') as f:
        f.write(note_content)

    print(f"Created knowledge note: {note_path}")
```

**Justfile Recipe**:
```bash
# Detect recurring conflict patterns and create knowledge notes
conflict-patterns:
    python3 scripts/conflict-pattern-detector.py
```

---

## 4. Auto-Resolution Logic

### 4.1 Safety Criteria

**Auto-resolution is ONLY safe when**:
1. Conflict type is `whitespace`, `formatting`, `lockfile`, or `metadata`
2. No semantic changes are introduced
3. Resolution can be validated programmatically
4. Rollback is trivial (git revert)

**Never auto-resolve**:
- Content conflicts in code or documentation
- Conflicts in critical config files (without schema validation)
- Conflicts where owner jurisdiction is unclear
- Conflicts with failed validation

---

### 4.2 Auto-Resolver Implementation

**Script**: `scripts/conflict-auto-resolver.py`

```python
def auto_resolve_conflicts(files):
    """
    Attempt auto-resolution for safe conflict types.

    Returns:
        {
            "resolved": [files],
            "failed": [files],
            "skipped": [files]
        }
    """
    resolved = []
    failed = []
    skipped = []

    for file in files:
        conflict_type = classify_conflict(file)

        if conflict_type in ["whitespace", "formatting"]:
            if auto_resolve_formatting(file):
                resolved.append(file)
            else:
                failed.append(file)

        elif conflict_type == "lockfile":
            if regenerate_lockfile(file):
                resolved.append(file)
            else:
                failed.append(file)

        elif conflict_type == "metadata":
            if delete_and_ignore(file):
                resolved.append(file)
            else:
                failed.append(file)

        else:
            # Content conflict, skip auto-resolution
            skipped.append(file)

    return {
        "resolved": resolved,
        "failed": failed,
        "skipped": skipped
    }
```

**Justfile Recipe**:
```bash
# Auto-resolve safe conflicts
conflict-auto-resolve:
    python3 scripts/conflict-auto-resolver.py --format text
```

**Output**:
```
Auto-Resolve Conflicts

✅ Resolved (3 files):
   - poetry.lock (REGENERATE_FROM_SOURCE)
   - .DS_Store (DELETE_AND_REGENERATE)
   - scripts/format-check.py (AUTO_RESOLVE_FORMATTING)

❌ Failed (1 file):
   - feature-manifest.yaml (validation failed)

⏭️  Skipped (2 files):
   - docs/vision/mcp.md (content conflict, manual review needed)
   - project-docs/sprints/sprint-13.md (content conflict, manual review needed)

Next Steps:
1. Review failed file: feature-manifest.yaml
2. Manually resolve skipped files (2 remaining)
3. Run 'git status' to verify resolution
```

---

## 5. Escalation Protocol

### 5.1 Escalation Levels

**Level 1: Developer Resolution** (default)
- **Who**: Developer who created the PR
- **When**: All content conflicts
- **Timeout**: 30 minutes
- **Process**: Follow resolution strategy for file type
- **Escalate if**: Stuck for >30 minutes OR unclear which version is correct

**Level 2: Pair Programming** (collaboration)
- **Who**: Developer + file owner (CODEOWNERS) OR peer developer
- **When**: Escalated from Level 1 OR cross-domain conflict
- **Timeout**: 1 hour
- **Process**:
  1. Schedule 30-minute pairing session
  2. Review conflict together (screen share)
  3. Discuss semantic intent of both changes
  4. Merge collaboratively
  5. Document decision in commit message
- **Escalate if**: Still unclear after 1 hour OR fundamental design disagreement

**Level 3: Project Lead Arbitration** (final decision)
- **Who**: Project lead (@victorpiper for chora-workspace)
- **When**: Escalated from Level 2 OR deadlock between domain owners
- **Timeout**: 24 hours (asynchronous)
- **Process**:
  1. Provide context: file, conflict, both versions, rationale
  2. Project lead reviews and makes final decision
  3. Decision is binding (no further escalation)
  4. Document in knowledge note if pattern emerges

---

### 5.2 Escalation Decision Tree

```
Conflict detected
│
├─ Auto-resolvable? (whitespace, formatting, lockfile, metadata)
│  ├─ YES → Auto-resolve (Level 0)
│  │  ├─ Success? → Done
│  │  └─ Failed? → Escalate to Level 1
│  │
│  └─ NO → Manual resolution required
│     │
│     ├─ Developer resolves (Level 1)
│     │  ├─ Resolved in <30 min? → Done
│     │  └─ Stuck for >30 min? → Escalate to Level 2
│     │
│     ├─ Pair programming (Level 2)
│     │  ├─ Has file owner (CODEOWNERS)? → Pair with owner
│     │  └─ No owner? → Pair with peer developer
│     │  │
│     │  ├─ Resolved in 1 hour? → Done
│     │  └─ Still stuck OR design disagreement? → Escalate to Level 3
│     │
│     └─ Project lead arbitration (Level 3)
│        ├─ Lead makes final decision (24 hours)
│        └─ Decision is binding → Done
```

---

### 5.3 Escalation Logging

**Log escalation events to A-MEM**:

```json
{
  "timestamp": "2025-11-18T15:00:00Z",
  "type": "conflict_escalation",
  "trace_id": "cord-2025-019-feature-branch",
  "file": "docs/vision/mcp.md",
  "from_level": 1,
  "to_level": 2,
  "reason": "Stuck for >30 minutes, unclear which version is correct",
  "developer": "alice",
  "consulted": "@victorpiper"
}
```

---

## 6. Tool Interfaces

### 6.1 Justfile Recipes

**Complete SAP-053 recipe set**:

```bash
# Conflict detection
conflict-check branch="main":
    python3 scripts/conflict-checker.py --branch {{branch}} --format text

conflict-check-json branch="main":
    python3 scripts/conflict-checker.py --branch {{branch}} --format json

conflict-predict:
    python3 scripts/conflict-predictor.py --files $(git diff --name-only --staged) --format text

# Conflict resolution
conflict-resolve file:
    python3 scripts/conflict-resolver.py --file {{file}} --interactive

conflict-auto-resolve:
    python3 scripts/conflict-auto-resolver.py --format text

conflict-resolve-lockfile file:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ "{{file}}" == "package-lock.json" ]]; then
        git rm package-lock.json && npm install && git add package-lock.json
    elif [[ "{{file}}" == "poetry.lock" ]]; then
        git rm poetry.lock && poetry lock && git add poetry.lock
    elif [[ "{{file}}" == "Pipfile.lock" ]]; then
        git rm Pipfile.lock && pipenv lock && git add Pipfile.lock
    fi
    git commit -m "Regenerate {{file}} (auto-resolve conflict)"

# Pattern detection
conflict-patterns:
    python3 scripts/conflict-pattern-detector.py

conflict-history file days="90":
    grep '"type": "conflict_resolved"' .chora/memory/events/*.jsonl | \
      jq -r 'select(.timestamp > (now - {{days}}*86400 | todate)) | select(.resolved_files[] | contains("{{file}}"))'

# Metrics
conflict-stats days="30":
    python3 scripts/conflict-stats.py --days {{days}} --format text
```

---

### 6.2 Python Script Interfaces

**All scripts follow this interface**:

```python
# scripts/{script-name}.py

import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="SAP-053: {script purpose}")

    # Common arguments
    parser.add_argument("--format", choices=["text", "json"], default="text",
                      help="Output format (text for humans, json for automation)")
    parser.add_argument("--verbose", action="store_true",
                      help="Verbose output")

    # Script-specific arguments
    # ...

    args = parser.parse_args()

    # Execute logic
    result = execute_logic(args)

    # Output
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print_text_output(result)

    # Exit code
    # 0 = success, 1 = conflicts/issues, 2 = auto-resolvable, 3 = error
    sys.exit(result["exit_code"])

if __name__ == "__main__":
    main()
```

**Exit Code Convention**:
- `0`: Success (no conflicts OR conflicts fully resolved)
- `1`: Conflicts detected, manual review needed
- `2`: Auto-resolvable conflicts detected
- `3`: Tool error (git command failed, invalid arguments)

---

## 7. Integration with SAP-051 and SAP-052

### 7.1 SAP-051 (Git Workflow) Integration

**Pre-push Hook** (`.git/hooks/pre-push`):
```bash
#!/bin/bash
# SAP-053: Conflict detection before push

# Check for conflicts
python3 scripts/conflict-checker.py --branch main --format json > /tmp/conflict-report.json

HAS_CONFLICTS=$(jq -r '.has_conflicts' /tmp/conflict-report.json)
AUTO_RESOLVABLE=$(jq -r '.auto_resolvable' /tmp/conflict-report.json)

if [ "$HAS_CONFLICTS" = "true" ]; then
    if [ "$AUTO_RESOLVABLE" = "true" ]; then
        echo "⚠️  Auto-resolvable conflicts detected."
        echo "Run 'just conflict-auto-resolve' to resolve automatically."
        echo "Or push with --no-verify to skip (not recommended)."
        exit 0  # Allow push, but warn
    else
        echo "❌ Conflicts detected. Resolve before pushing."
        echo "Run 'just conflict-check' for details."
        exit 1  # Block push
    fi
else
    echo "✅ No conflicts detected."
    exit 0
fi
```

---

### 7.2 SAP-052 (Ownership Zones) Integration

**Conflict resolution with owner jurisdiction**:

```python
# scripts/conflict-resolver.py

from ownership_coverage import get_file_owner  # SAP-052 tool

def resolve_with_ownership(file):
    """
    Resolve conflict using CODEOWNERS jurisdiction.

    SAP-052 Jurisdiction Rules:
    - Single domain: Domain owner has jurisdiction
    - Multiple domains: All owners collaborate (consensus)
    - Deadlock: Escalate to project lead
    """
    owner = get_file_owner(file)

    if owner:
        print(f"File owner: {owner} (from CODEOWNERS)")
        print(f"Contact {owner} for resolution guidance.")
        print(f"Per SAP-052 Contract 2: Owner has jurisdiction in their domain.")

        # Suggest contacting owner
        return {
            "strategy": "MANUAL_REVIEW_WITH_OWNERSHIP",
            "owner": owner,
            "steps": [
                f"Contact {owner} for conflict review",
                "Resolve following owner's guidance",
                "Commit with owner tag in message"
            ]
        }
    else:
        # No owner assigned, escalate to project lead
        print(f"⚠️  No owner assigned for {file}")
        print("Escalating to project lead for resolution.")
        return {
            "strategy": "ESCALATE_TO_LEAD",
            "steps": [
                "Contact project lead for arbitration",
                "Provide context: file, conflict, both versions",
                "Follow lead's decision"
            ]
        }
```

---

## 8. Testing Strategy

### 8.1 Conflict Detection Tests

**Test Suite**: `tests/test_conflict_detection.py`

```python
import pytest
from scripts.conflict_checker import check_for_conflicts, classify_conflicts

def test_detect_content_conflict():
    """Test detection of content conflicts."""
    # Setup: Create branch with conflicting changes
    # ...
    result = check_for_conflicts(branch="main")
    assert result["has_conflicts"] == True
    assert "test_file.py" in result["conflicting_files"]

def test_classify_whitespace_conflict():
    """Test classification of whitespace-only conflicts."""
    # Setup: Create conflict with only whitespace differences
    # ...
    types = classify_conflicts(["test_file.py"])
    assert types["test_file.py"] == "whitespace"

def test_classify_lockfile_conflict():
    """Test classification of lockfile conflicts."""
    types = classify_conflicts(["poetry.lock"])
    assert types["poetry.lock"] == "lockfile"
```

---

### 8.2 Resolution Strategy Tests

**Test Suite**: `tests/test_resolution_strategies.py`

```python
def test_auto_resolve_formatting():
    """Test auto-resolution of formatting conflicts."""
    # Setup: Create formatting conflict
    # ...
    result = auto_resolve_formatting("test_file.py")
    assert result == True  # Successfully auto-resolved

def test_regenerate_lockfile():
    """Test lockfile regeneration."""
    # Setup: Create lockfile conflict
    # ...
    result = regenerate_lockfile("poetry.lock")
    assert result == True
    assert Path("poetry.lock").exists()

def test_manual_review_required():
    """Test that content conflicts require manual review."""
    # Setup: Create content conflict
    # ...
    strategy = select_resolution_strategy("docs/README.md", "content")
    assert strategy["auto_resolvable"] == False
    assert strategy["strategy"] == "MANUAL_REVIEW"
```

---

### 8.3 A-MEM Integration Tests

**Test Suite**: `tests/test_amem_logging.py`

```python
def test_log_conflict_detected():
    """Test logging of conflict_detected event."""
    # Setup: Create conflict
    # ...
    log_conflict_detected(files=["test.py"], branch="feature/test")

    # Verify event logged
    events = query_memory_events(event_type="conflict_detected")
    assert len(events) > 0
    assert events[-1]["conflicting_files"] == ["test.py"]

def test_log_conflict_resolved():
    """Test logging of conflict_resolved event."""
    # Setup: Resolve conflict
    # ...
    log_conflict_resolved(
        files=["test.py"],
        strategy="MANUAL_REVIEW",
        resolution_time_minutes=12.5
    )

    # Verify event logged
    events = query_memory_events(event_type="conflict_resolved")
    assert events[-1]["resolution_time_minutes"] == 12.5
```

---

## 9. Performance Considerations

### 9.1 Conflict Checker Performance

**Optimization**: Cache git diff results to avoid repeated computation

```python
# scripts/conflict-checker.py

import functools
import hashlib

@functools.lru_cache(maxsize=128)
def check_for_conflicts_cached(branch, commit_sha):
    """
    Cached conflict detection.
    Cache key: (branch, commit_sha)
    Invalidate cache when HEAD changes.
    """
    return check_for_conflicts(branch)

def get_current_commit_sha():
    """Get current HEAD commit SHA for cache key."""
    result = run("git rev-parse HEAD")
    return result.stdout.strip()

# Usage
commit_sha = get_current_commit_sha()
result = check_for_conflicts_cached(branch="main", commit_sha=commit_sha)
```

**Performance Target**: <5 seconds for conflict detection (typical repo with <1000 changed files)

---

### 9.2 A-MEM Query Performance

**Optimization**: Index event files by type for faster queries

```python
# scripts/memory-indexer.py (future enhancement)

def create_event_index():
    """
    Create index of event types for faster queries.

    Index format:
    {
      "conflict_detected": ["2025-11.jsonl:line42", ...],
      "conflict_resolved": ["2025-11.jsonl:line108", ...],
      ...
    }
    """
    index = {}

    for event_file in Path(".chora/memory/events/").glob("*.jsonl"):
        with open(event_file) as f:
            for line_num, line in enumerate(f, 1):
                event = json.loads(line)
                event_type = event["type"]

                if event_type not in index:
                    index[event_type] = []

                index[event_type].append(f"{event_file.name}:line{line_num}")

    # Save index
    with open(".chora/memory/.event_index.json", 'w') as f:
        json.dumps(index, f, indent=2)

def query_events_with_index(event_type):
    """Use index for fast event queries."""
    with open(".chora/memory/.event_index.json") as f:
        index = json.load(f)

    locations = index.get(event_type, [])

    events = []
    for loc in locations:
        file, line = loc.split(":")
        line_num = int(line.replace("line", ""))

        # Read specific line from file
        with open(f".chora/memory/events/{file}") as f:
            event = json.loads(f.readlines()[line_num - 1])
            events.append(event)

    return events
```

**Performance Target**: <1 second for event queries (even with 10k+ events)

---

## 10. Next Steps

### Phase 1 (Design) - Remaining Tasks

1. ✅ Draft capability-charter.md (COMPLETE)
2. ✅ Draft protocol-spec.md (COMPLETE - this file)
3. ⏳ Draft awareness-guide.md (agent workflows, decision trees)
4. ⏳ Draft adoption-blueprint.md (4-phase adoption plan)
5. ⏳ Draft ledger.md (adoption tracking template)

### Phase 2 (Infrastructure) - Upcoming

1. Implement conflict-checker.py (pre-merge detection)
2. Implement conflict-resolver.py (interactive resolution)
3. Implement conflict-auto-resolver.py (safe auto-resolution)
4. Implement conflict-predictor.py (risk prediction)
5. Implement conflict-pattern-detector.py (A-MEM integration)
6. Write test suite (100+ test cases)
7. Create justfile recipes
8. Integrate with SAP-051 (pre-push hook)

### Phase 3 (Pilot) - After Infrastructure

1. Pilot in chora-workspace (2-developer scenario simulation)
2. Generate 10+ test conflicts (various file types)
3. Validate resolution strategies
4. Measure resolution time reduction
5. Create knowledge notes for patterns
6. Generate pilot report

### Phase 4 (Distribution) - Final

1. Distribute to chora-base (SAP template)
2. Integrate with chora-compose (auto-install hooks)
3. Create public documentation
4. Monitor adoption metrics

---

## Document Metadata

**Version**: 1.0.0
**Status**: Draft (Phase 1 - Design)
**Last Updated**: 2025-11-18
**Next Review**: After Phase 2 (Infrastructure) completion
**Related Documents**:
- [capability-charter.md](capability-charter.md) - SAP-053 charter
- [awareness-guide.md](awareness-guide.md) - Agent workflows (to be created)
- [adoption-blueprint.md](adoption-blueprint.md) - Adoption plan (to be created)
- [ledger.md](ledger.md) - Adoption tracking (to be created)

**SAP Dependencies**:
- SAP-051 (Git Workflow) - ✅ Complete
- SAP-052 (Ownership Zones) - ✅ Complete
- SAP-010 (A-MEM) - ✅ Complete (L4)

---

**Created**: 2025-11-18
**Author**: Claude (AI peer) + Victor Piper
**Trace ID**: sap-053-phase1-design-2025-11-18
