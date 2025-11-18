---
sap_id: SAP-056
version: 1.0.0
status: Draft
last_updated: 2025-11-16
type: reference
feature_id: FEAT-SAP-056
requirement_refs:
  - REQ-SAP-056-001
  - REQ-SAP-056-002
  - REQ-SAP-056-003
---

# Protocol Specification: Lifecycle Traceability

**SAP ID**: SAP-056
**Version**: 1.0.0
**Status**: Draft (Phase 1)
**Last Updated**: 2025-11-16

---

## 1. Overview

This protocol defines the **Lifecycle Traceability architecture** for achieving 100% linkage across 10 artifact types in software development.

**Artifact Dependency Graph** (shows linkage, not creation order):
```
Vision → Features → Requirements
                   → Documentation (SAP-012: created FIRST)
                   → Tests (SAP-012: BDD from docs)
                   → Code (SAP-012: TDD implementation)
                   → Git Commits → Tasks → Events → Knowledge
```

**Important**: When following SAP-012 (development-lifecycle), artifacts are created in **Documentation-First** order: `Requirements → Docs → Tests → Code`. The manifest schema supports any creation order; validation only requires all artifacts are linked bidirectionally.

**Core Guarantee**: Every artifact has provenance (why it exists), implementation evidence (what implements it), and validation proof (how it's tested/documented).

**Governance Model**: SAP-056 governs traceability; individual SAPs implement linkage mechanisms.

---

## 2. Architecture

### 2.1 Traceability Artifact Types

**10 Core Artifact Types**:

1. **Vision** - High-level goals and outcomes (capability-charter.md)
2. **Features** - Deliverable capabilities (feature-manifest.yaml)
3. **Requirements** - Specific acceptance criteria (feature-manifest.yaml)
4. **Code** - Source files (src/*, scripts/*)
5. **Tests** - Automated tests (tests/*)
6. **Documentation** - User/dev docs (docs/*)
7. **Git Commits** - Version control history
8. **Tasks** - Work items (beads issues)
9. **Events** - Development milestones (A-MEM events)
10. **Knowledge** - Learned patterns (knowledge notes)

### 2.2 Linkage Mechanisms

| From | To | Mechanism | Artifact | Example |
|------|----|-----------|-----------| --------|
| Vision | Features | feature-manifest.yaml | `vision_ref` | `vision_ref: "CHARTER-001:Outcome-2"` |
| Features | Requirements | feature-manifest.yaml | `requirements` | `requirements: [REQ-001, REQ-002]` |
| Features | Code | feature-manifest.yaml | `code` | `code: [src/auth/providers.py]` |
| Features | Tests | feature-manifest.yaml | `tests` | `tests: [tests/test_auth.py::test_email_login]` |
| Features | Docs | feature-manifest.yaml | `docs` | `docs: [docs/how-to/auth.md]` |
| Tests | Requirements | pytest marker | `@pytest.mark.requirement()` | `@pytest.mark.requirement("REQ-001")` |
| Tests | Features | pytest marker | `@pytest.mark.feature()` | `@pytest.mark.feature("FEAT-001")` |
| Docs | Code | frontmatter | `code_references` | `code_references: [src/auth/providers.py]` |
| Docs | Tests | frontmatter | `test_references` | `test_references: [tests/test_auth.py]` |
| Docs | Features | frontmatter | `feature_id` | `feature_id: FEAT-001` |
| Git | Tasks | commit message | `[task-id]` suffix | `feat(auth): add OAuth [.beads-abc123]` |
| Tasks | Events | A-MEM event | `task_id` field | `{"event_type": "task_completed", "task_id": ".beads-abc123"}` |
| Tasks | Features | task title | `[Feature: FEAT-XXX]` | `[Feature: FEAT-001] Implement OAuth` |
| Events | Knowledge | wikilink | `[[task-id]]` | `See [[.beads-abc123]] for details` |
| Events | Features | event field | `feature_id` | `{"event_type": "feature_completed", "feature_id": "FEAT-001"}` |

### 2.3 Bidirectional Linkage Requirement

**Principle**: If artifact A references artifact B, then B's manifest MUST list A.

**Example**:
- Doc `docs/how-to/auth.md` frontmatter: `code_references: [src/auth/providers.py]`
- Feature manifest entry for FEAT-001: `docs: [docs/how-to/auth.md]`
- **Validation**: Both directions must be present (prevents drift)

---

## 3. Feature Manifest Schema

### 3.1 Structure

**File Location**: `feature-manifest.yaml` (project root)

**Schema Version**: 1.0.0

```yaml
# feature-manifest.yaml
schema_version: "1.0.0"
project:
  name: "chora-workspace"
  repository: "https://github.com/example/chora-workspace"

features:
  - id: FEAT-001
    name: "User Authentication"
    description: "Email/password and OAuth2 authentication"
    vision_ref: "CHARTER-001:Outcome-2"
    status: implemented
    created: "2025-10-01"
    completed: "2025-11-15"

    requirements:
      - id: REQ-001
        description: "Support email/password login"
        acceptance_criteria:
          - "User can register with email/password"
          - "Password must be hashed (bcrypt)"
          - "Login returns JWT token"
      - id: REQ-002
        description: "Support OAuth2 providers (Google, GitHub)"
        acceptance_criteria:
          - "User can authenticate via Google OAuth2"
          - "User can authenticate via GitHub OAuth2"
          - "OAuth tokens stored securely"

    code:
      - path: src/auth/providers.py
        lines_of_code: 256
        complexity: medium
      - path: src/auth/handlers.py
        lines_of_code: 142
        complexity: low

    tests:
      - path: tests/test_auth.py::test_email_login
        type: unit
        requirement: REQ-001
      - path: tests/test_auth.py::test_oauth_google
        type: integration
        requirement: REQ-002
      - path: tests/test_auth.py::test_oauth_github
        type: integration
        requirement: REQ-002

    documentation:
      - path: docs/user-docs/how-to/authentication.md
        type: how-to
        audience: users
      - path: docs/dev-docs/reference/auth-api.md
        type: reference
        audience: developers

    tasks:
      - id: .beads-abc123
        title: "Implement email/password auth"
        status: closed
      - id: .beads-def456
        title: "Add OAuth2 providers"
        status: closed

    commits:
      - sha: a7b3c9e2
        date: "2025-11-10"
        message: "feat(auth): implement email/password [.beads-abc123]"
      - sha: d4e5f6g7
        date: "2025-11-12"
        message: "feat(auth): add OAuth2 providers [.beads-def456]"

    metrics:
      test_coverage: 92.5
      documentation_completeness: 100
      code_quality_score: 8.5
```

### 3.2 Field Definitions

#### Feature-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique feature ID (format: `FEAT-XXX`) |
| `name` | string | Yes | Human-readable feature name |
| `description` | string | Yes | Brief feature description (1-2 sentences) |
| `vision_ref` | string | Yes | Reference to vision document outcome (format: `CHARTER-XXX:Outcome-N`) |
| `status` | enum | Yes | Feature status: `planned` \| `in_progress` \| `implemented` \| `deprecated` |
| `created` | date | Yes | Feature creation date (ISO 8601) |
| `completed` | date | No | Feature completion date (ISO 8601, required if status=implemented) |
| `requirements` | array | Yes | List of requirements (≥1 required) |
| `code` | array | Yes | List of source files (≥1 required if status=implemented) |
| `tests` | array | Yes | List of test cases (≥1 required if status=implemented) |
| `documentation` | array | Yes | List of docs (≥1 required if status=implemented) |
| `tasks` | array | No | List of beads tasks |
| `commits` | array | No | List of git commits |
| `metrics` | object | No | Quality metrics |

#### Requirement Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique requirement ID (format: `REQ-XXX`) |
| `description` | string | Yes | Requirement description |
| `acceptance_criteria` | array | Yes | List of acceptance criteria strings |

#### Code Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | Yes | Relative path from repo root |
| `lines_of_code` | integer | No | Total LOC in file |
| `complexity` | enum | No | `low` \| `medium` \| `high` |

#### Test Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | Yes | Pytest path format (file::test_name) |
| `type` | enum | Yes | `unit` \| `integration` \| `e2e` |
| `requirement` | string | Yes | Requirement ID this test validates |

#### Documentation Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | Yes | Relative path from repo root |
| `type` | enum | Yes | `how-to` \| `tutorial` \| `reference` \| `explanation` (Diátaxis) |
| `audience` | enum | Yes | `users` \| `developers` \| `operators` |

---

## 4. Frontmatter Specifications

### 4.1 Documentation Frontmatter

**Location**: All markdown files in `docs/`

**Required Fields** (for traceability):

```yaml
---
title: "How to Use Authentication"
type: how-to
feature_id: FEAT-001
code_references:
  - src/auth/providers.py
  - src/auth/handlers.py
test_references:
  - tests/test_auth.py::test_email_login
  - tests/test_auth.py::test_oauth_google
related_docs:
  - docs/dev-docs/reference/auth-api.md
last_updated: "2025-11-15"
---
```

**Field Definitions**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `feature_id` | string | Yes | Feature this doc explains (format: `FEAT-XXX`) |
| `code_references` | array | Yes (unless conceptual) | Source files referenced in doc |
| `test_references` | array | No | Test cases demonstrating concepts |
| `related_docs` | array | No | Links to related documentation |

**Conceptual Documents** (no code_references required):
- Vision documents
- Architectural decision records (ADRs)
- Glossaries, FAQs

**Validation Rule**: If doc includes code examples, `code_references` MUST list source files for those examples.

### 4.2 Test Frontmatter (via Docstrings)

**Location**: Test file docstrings

```python
# tests/test_auth.py
"""Tests for FEAT-001 (User Authentication)

Feature: FEAT-001
Sprint: sprint-13
Coverage Target: 90%
"""

import pytest

@pytest.mark.feature("FEAT-001")
@pytest.mark.requirement("REQ-001")
@pytest.mark.unit
def test_email_login():
    """Test email/password authentication."""
    # ... test code
```

**Pytest Markers**:

| Marker | Required | Description |
|--------|----------|-------------|
| `@pytest.mark.feature("FEAT-XXX")` | Yes | Feature this test validates |
| `@pytest.mark.requirement("REQ-XXX")` | Yes | Requirement this test validates |
| `@pytest.mark.unit` \| `.integration` \| `.e2e` | Yes | Test type |

---

## 5. Commit Message Conventions

### 5.1 Format

**Standard**: Conventional Commits + Task ID suffix

```
<type>(<scope>): <description> [<task-id>]

[optional body]

[optional footer]
```

**Example**:
```
feat(auth): implement OAuth2 providers [.beads-def456]

Add Google and GitHub OAuth2 authentication.

Closes: .beads-def456
Feature: FEAT-001
```

### 5.2 Task ID Placement

**Primary**: Suffix format (preferred for brevity)
```
feat(auth): add OAuth2 [.beads-abc123]
```

**Alternative**: Footer format (conventional commits compliant)
```
feat(auth): add OAuth2

Closes: .beads-abc123
Feature: FEAT-001
```

### 5.3 Validation

**Pre-commit Hook**: Suggest task ID if missing
```bash
# .git/hooks/prepare-commit-msg
if ! echo "$commit_msg" | grep -q "\[\.beads-"; then
    # Extract from branch name or prompt
    echo "# Suggested: Add task ID for traceability"
fi
```

---

## 6. Validation Rules

### 6.1 Rule Definitions

**Rule 1: Forward Linkage**
- **Requirement**: Every vision outcome → ≥1 feature
- **Validation**: Parse capability-charter.md, check all outcomes referenced in feature-manifest.yaml
- **Fix**: Add missing features or update vision_ref

**Rule 2: Bidirectional Linkage**
- **Requirement**: If doc references code, code manifest lists doc
- **Validation**: Cross-check frontmatter `code_references` with feature manifest `documentation`
- **Fix**: Add missing entry in feature manifest or remove stale reference

**Rule 3: Evidence Requirement**
- **Requirement**: Every feature (status=implemented) → ≥1 test AND ≥1 doc
- **Validation**: Check `tests` and `documentation` arrays non-empty
- **Fix**: Add missing tests or docs, or change status to `in_progress`

**Rule 4: Closed Loop**
- **Requirement**: Every git commit closing task → links to feature
- **Validation**: Parse commit messages for `[.beads-XXX]`, check beads task has `[Feature: FEAT-XXX]`
- **Fix**: Update beads task title with feature prefix

**Rule 5: Orphan Detection**
- **Requirement**: No artifact without parent linkage
- **Validation**: All code files appear in ≥1 feature manifest; all docs have `feature_id`
- **Fix**: Add to feature manifest or mark as deprecated

**Rule 6: Schema Compliance**
- **Requirement**: feature-manifest.yaml passes JSON Schema validation
- **Validation**: Validate against `schemas/feature-manifest.yaml`
- **Fix**: Correct schema violations (missing required fields, wrong types)

**Rule 7: Reference Integrity**
- **Requirement**: All vision_ref, code paths, doc paths, test paths exist
- **Validation**: Check file existence for all referenced paths
- **Fix**: Update paths or remove stale references

**Rule 8: Requirement Coverage**
- **Requirement**: Every requirement → ≥1 test with `@pytest.mark.requirement`
- **Validation**: Parse test files for markers, check all requirement IDs covered
- **Fix**: Add missing tests or mark requirement as `planned`

**Rule 9: Documentation Coverage**
- **Requirement**: Every feature → ≥1 doc in frontmatter with matching `feature_id`
- **Validation**: Check docs have frontmatter `feature_id` matching feature manifest
- **Fix**: Add frontmatter or create missing doc

**Rule 10: Event Correlation**
- **Requirement**: Every task completion → A-MEM event with `feature_id`
- **Validation**: Parse event logs for `task_completed` events, check `feature_id` present
- **Fix**: Emit events with `feature_id` field (SAP-010 enhancement)

### 6.2 Validation Output Format

**Markdown Report**:

```markdown
# Traceability Validation Report

**Date**: 2025-11-16
**Project**: chora-workspace
**Features Validated**: 12

## Summary

| Rule | Status | Pass Rate |
|------|--------|-----------|
| Rule 1: Forward Linkage | ✓ PASS | 100% (12/12) |
| Rule 2: Bidirectional Linkage | ✗ FAIL | 83% (10/12) |
| Rule 3: Evidence Requirement | ✓ PASS | 100% (12/12) |
| ... | ... | ... |

**Overall Pass Rate**: 92% (110/120 checks)

## Failures

### Rule 2: Bidirectional Linkage

**FEAT-002**: Doc `docs/how-to/backend.md` references `src/backend/server.py`, but feature manifest does not list this doc.

**Fix**: Add to FEAT-002 manifest:
```yaml
documentation:
  - path: docs/how-to/backend.md
    type: how-to
```

... (more failures)
```

---

## 7. Compliance Levels

### 7.1 Level Definitions

**Level 0 (No Traceability)**:
- No linkages defined
- No feature manifest
- No validation

**Level 1 (Partial Traceability)**:
- feature-manifest.yaml exists (≥1 feature)
- Vision→Features linked (Rule 1 passing)
- Code→Tests linked (Rule 8 passing, partial)
- **Target**: Initial adoption, 1-2 features documented

**Level 2 (Substantial Traceability)**:
- ≥5 features in manifest
- Features→Requirements defined
- Docs→Code linked via frontmatter
- Validation pass rate ≥80%
- **Target**: Active development, systematic linkage

**Level 3 (Complete Traceability)**:
- All features in manifest
- Git→Tasks linkage (commit messages)
- Tasks→Events linkage (A-MEM events)
- Events→Knowledge linkage (wikilinks)
- Validation pass rate 100%
- **Target**: Production-ready, audit-compliant

---

## 8. Integration with Existing SAPs

### 8.1 SAP-012 Enhancement (Development Lifecycle)

**Addition**: Feature Manifest Creation Step

**Existing DDD→BDD→TDD Workflow**:
1. DDD (Intent Document) → Describe system behavior
2. BDD (Validation Scripts) → Define success criteria
3. TDD (Tests First) → Write tests before code

**Enhancement** (new Step 1.5):
1. DDD (Intent Document)
2. **Feature Manifest Entry** ← NEW
   - Create feature-manifest.yaml entry
   - Define requirements from intent document
   - Set status=planned
3. BDD (Validation Scripts)
4. TDD (Tests First)

**Template**: `templates/feature-manifest-entry.j2`

### 8.2 SAP-007 Enhancement (Documentation Framework)

**Addition**: Frontmatter Traceability Fields

**Existing Frontmatter** (Diátaxis):
```yaml
---
title: "How to X"
type: how-to
audience: users
---
```

**Enhancement**:
```yaml
---
title: "How to X"
type: how-to
audience: users
feature_id: FEAT-001          # NEW
code_references:              # NEW
  - src/module.py
test_references:              # NEW
  - tests/test_module.py
---
```

**Validation**: Docs MUST reference ≥1 code file (or be marked conceptual)

### 8.3 SAP-015 Enhancement (Task Tracking)

**Addition**: Traceability Validation Subcommand

**Existing beads CLI**:
```bash
bd create "Task title"
bd list
bd show <task-id>
```

**Enhancement**:
```bash
bd validate-traceability           # NEW
# → Check all closed issues have git commits
# → Check all issues link to features via [Feature: FEAT-XXX]
```

### 8.4 SAP-010 Enhancement (Memory System)

**Addition**: Feature Completion Events

**Existing Event Types**:
- `task_started`, `task_completed`, `task_failed`, `task_blocked`

**Enhancement**:
```json
{
  "event_type": "feature_completed",  // NEW
  "feature_id": "FEAT-001",
  "vision_ref": "CHARTER-001:Outcome-2",
  "trace_id": "sprint-13",
  "evidence": {
    "tests_passing": 12,
    "docs_created": 3,
    "tasks_closed": 5
  }
}
```

**All development events** get `feature_id` field.

### 8.5 SAP-004 Enhancement (Testing Framework)

**Addition**: Requirement/Feature Pytest Markers

**Existing Pytest Conventions**:
```python
@pytest.mark.unit
def test_something():
    ...
```

**Enhancement**:
```python
@pytest.mark.feature("FEAT-001")        # NEW
@pytest.mark.requirement("REQ-001")     # NEW
@pytest.mark.unit
def test_something():
    ...
```

**Coverage Report**:
```bash
pytest --requirement-coverage
# → REQ-001: 100% (2/2 tests passing)
# → REQ-002: 50% (1/2 tests passing)
```

---

## 9. Examples

### 9.1 End-to-End Traceability Example

**Vision** (capability-charter.md):
```markdown
## Outcomes
1. Users can authenticate via OAuth2 (Google, GitHub)
```

**Feature Manifest** (feature-manifest.yaml):
```yaml
features:
  - id: FEAT-001
    name: "User Authentication"
    vision_ref: "CHARTER-001:Outcome-1"
    requirements:
      - id: REQ-001
        description: "Support Google OAuth2"
      - id: REQ-002
        description: "Support GitHub OAuth2"
    code:
      - path: src/auth/oauth.py
    tests:
      - path: tests/test_oauth.py::test_google_auth
        requirement: REQ-001
      - path: tests/test_oauth.py::test_github_auth
        requirement: REQ-002
    documentation:
      - path: docs/how-to/oauth-setup.md
```

**Code** (src/auth/oauth.py):
```python
# Feature: FEAT-001
def google_oauth_login():
    ...
```

**Tests** (tests/test_oauth.py):
```python
@pytest.mark.feature("FEAT-001")
@pytest.mark.requirement("REQ-001")
def test_google_auth():
    ...
```

**Documentation** (docs/how-to/oauth-setup.md):
```yaml
---
feature_id: FEAT-001
code_references:
  - src/auth/oauth.py
test_references:
  - tests/test_oauth.py::test_google_auth
---

# How to Set Up OAuth
...
```

**Git Commit**:
```
feat(auth): add Google OAuth2 [.beads-abc123]
```

**Beads Task** (.beads-abc123):
```
Title: [Feature: FEAT-001] Implement Google OAuth2
Status: closed
```

**A-MEM Event**:
```json
{
  "event_type": "task_completed",
  "task_id": ".beads-abc123",
  "feature_id": "FEAT-001",
  "trace_id": "sprint-13"
}
```

**Knowledge Note**:
```markdown
---
title: "OAuth2 Integration Pattern"
---

# OAuth2 Integration Pattern

Learned from [[.beads-abc123]] (FEAT-001 implementation)...
```

**Traceability Chain**:
Vision (Outcome 1) → Feature (FEAT-001) → Requirements (REQ-001, REQ-002) → Code (src/auth/oauth.py) → Tests (test_google_auth, test_github_auth) → Docs (oauth-setup.md) → Git (feat(auth): add Google OAuth2) → Task (.beads-abc123) → Event (task_completed) → Knowledge (OAuth2 Integration Pattern)

**Complete**: 100% traceability across 10 artifact types.

---

## 10. Schema Files

### 10.1 Feature Manifest JSON Schema

**File**: `schemas/feature-manifest.yaml`

```yaml
$schema: "http://json-schema.org/draft-07/schema#"
title: "Feature Manifest Schema"
version: "1.0.0"

type: object
required: [schema_version, project, features]

properties:
  schema_version:
    type: string
    const: "1.0.0"

  project:
    type: object
    required: [name, repository]
    properties:
      name:
        type: string
      repository:
        type: string
        format: uri

  features:
    type: array
    minItems: 1
    items:
      $ref: "#/definitions/Feature"

definitions:
  Feature:
    type: object
    required: [id, name, description, vision_ref, status, created, requirements]
    properties:
      id:
        type: string
        pattern: "^FEAT-[0-9]{3}$"
      name:
        type: string
        minLength: 5
      description:
        type: string
      vision_ref:
        type: string
        pattern: "^CHARTER-[0-9]{3}:Outcome-[0-9]+$"
      status:
        type: string
        enum: [planned, in_progress, implemented, deprecated]
      created:
        type: string
        format: date
      completed:
        type: string
        format: date
      requirements:
        type: array
        minItems: 1
        items:
          $ref: "#/definitions/Requirement"
      code:
        type: array
        items:
          $ref: "#/definitions/CodeFile"
      tests:
        type: array
        items:
          $ref: "#/definitions/Test"
      documentation:
        type: array
        items:
          $ref: "#/definitions/Documentation"
      tasks:
        type: array
        items:
          $ref: "#/definitions/Task"
      commits:
        type: array
        items:
          $ref: "#/definitions/Commit"

  Requirement:
    type: object
    required: [id, description, acceptance_criteria]
    properties:
      id:
        type: string
        pattern: "^REQ-[0-9]{3}$"
      description:
        type: string
      acceptance_criteria:
        type: array
        minItems: 1
        items:
          type: string

  CodeFile:
    type: object
    required: [path]
    properties:
      path:
        type: string
      lines_of_code:
        type: integer
        minimum: 0
      complexity:
        type: string
        enum: [low, medium, high]

  Test:
    type: object
    required: [path, type, requirement]
    properties:
      path:
        type: string
        pattern: "^tests/.*::test_.*$"
      type:
        type: string
        enum: [unit, integration, e2e]
      requirement:
        type: string
        pattern: "^REQ-[0-9]{3}$"

  Documentation:
    type: object
    required: [path, type, audience]
    properties:
      path:
        type: string
        pattern: "^docs/.*\.md$"
      type:
        type: string
        enum: [how-to, tutorial, reference, explanation]
      audience:
        type: string
        enum: [users, developers, operators]

  Task:
    type: object
    required: [id, title, status]
    properties:
      id:
        type: string
        pattern: "^\\.beads-[a-z0-9]+$"
      title:
        type: string
      status:
        type: string
        enum: [open, in_progress, closed]

  Commit:
    type: object
    required: [sha, date, message]
    properties:
      sha:
        type: string
        pattern: "^[a-f0-9]{7,40}$"
      date:
        type: string
        format: date
      message:
        type: string
```

---

## 11. Version History

**1.0.0** (2025-11-16): Initial protocol specification
- 10 artifact types
- 15 linkage mechanisms
- 10 validation rules
- 3 compliance levels (L0-L3)
- Feature manifest schema v1.0.0
- Integration specs for 5 SAPs (SAP-004, SAP-007, SAP-010, SAP-012, SAP-015)
