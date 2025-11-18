# Protocol Specification: Ownership Zones

**SAP ID**: SAP-052
**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-17

---

## 1. Overview

Ownership Zones (SAP-052) defines code ownership patterns for multi-developer collaboration across the chora ecosystem. This protocol establishes CODEOWNERS file format, domain ownership mapping, ownership coverage metrics, conflict jurisdiction rules, and ownership rotation protocols.

### Key Capabilities

- GitHub/GitLab-compatible CODEOWNERS file format
- Domain ownership mapping (directory-level patterns)
- Automatic reviewer assignment via platform integration
- Ownership coverage metrics (% files covered, orphan file tracking)
- Conflict jurisdiction rules (owner-based resolution authority)
- Ownership rotation protocol (quarterly handoff process)
- Template generator for CODEOWNERS creation
- Coverage analysis tool for metrics dashboard
- Reviewer suggester for git history analysis

---

## 2. Core Contracts

### Contract 1: CODEOWNERS File Format

**Description**: GitHub/GitLab-compatible file defining code ownership patterns for automatic reviewer assignment.

**File Location**: Repository root (`/CODEOWNERS`)

**Format**:
```
# CODEOWNERS file format (GitHub/GitLab compatible)
# Pattern format: <file-pattern> @username1 @username2

# Syntax:
# - One pattern per line
# - Patterns use gitignore-style glob syntax
# - Later patterns override earlier patterns (last match wins)
# - @username or @org/team-name for owners
# - # for comments

# Pattern Types:
# 1. Directory-level: /docs/ @doc-owner
# 2. File-type: *.md @doc-owner
# 3. Specific file: /justfile @infra-owner
# 4. Nested directory: /docs/vision/** @vision-owner
```

**Example CODEOWNERS** (chora-workspace):
```
# chora-workspace CODEOWNERS
# Defines ownership for 5 primary domains

# Documentation domain
/docs/ @victorpiper
/docs/vision/ @victorpiper
/docs/research/ @victorpiper
*.md @victorpiper

# Scripts/Automation domain
/scripts/ @victorpiper
justfile @victorpiper
/scripts/sap-*.py @victorpiper

# Coordination/Inbox domain
/inbox/ @victorpiper
/inbox/templates/ @victorpiper
/inbox/incoming/ @victorpiper

# Memory system domain
/.chora/ @victorpiper
/.chora/memory/ @victorpiper

# Project management domain
/project-docs/ @victorpiper
/project-docs/sprints/ @victorpiper
/project-docs/metrics/ @victorpiper

# Shared/Cross-domain files (multiple owners)
/AGENTS.md @victorpiper
/CLAUDE.md @victorpiper
/README.md @victorpiper
```

**Validation Rules**:
- File must be named `CODEOWNERS` (case-sensitive, no extension)
- File must be at repository root (not in subdirectory)
- Patterns must use gitignore-style glob syntax
- Owner usernames must start with `@` (e.g., `@username`)
- Team names must use `@org/team` format
- Comments start with `#`
- Blank lines ignored
- Last matching pattern determines owners (later patterns override earlier)

**GitHub/GitLab Behavior**:
- GitHub: Automatically assigns reviewers on PR creation based on changed files
- GitLab: Suggests approvers based on file patterns
- If multiple patterns match, all matching owners are assigned/suggested
- If no pattern matches, no automatic assignment (manual assignment required)

**Enforcement**: GitHub/GitLab platform integration (automatic reviewer assignment on PR creation).

---

### Contract 2: Domain Ownership Mapping

**Description**: Standardized mapping of repository directories to domain owners for the chora ecosystem.

**chora-workspace Domains** (5 domains):

**1. Documentation Domain** (`/docs/`)
- **Owner**: Documentation lead
- **Scope**: All markdown files, documentation structure, vision docs, research notes
- **Patterns**: `/docs/**`, `*.md` (except domain-specific AGENTS.md)
- **Responsibilities**: Documentation quality, link validation, structure consistency

**2. Scripts/Automation Domain** (`/scripts/`)
- **Owner**: Automation lead
- **Scope**: Python scripts, justfile recipes, validation tools, metrics dashboards
- **Patterns**: `/scripts/**`, `/justfile`, `*.py` (in root)
- **Responsibilities**: Script quality, justfile maintenance, automation reliability

**3. Coordination/Inbox Domain** (`/inbox/`)
- **Owner**: Coordination lead
- **Scope**: Coordination requests, templates, intake workflows, ECOSYSTEM_STATUS.yaml
- **Patterns**: `/inbox/**`, `/inbox/templates/**`, `/inbox/incoming/**`
- **Responsibilities**: Coordination request review, template maintenance, intake triage

**4. Memory System Domain** (`/.chora/`)
- **Owner**: Memory system lead
- **Scope**: A-MEM events, knowledge notes, agent profiles, query templates
- **Patterns**: `/.chora/**`, `/.chora/memory/**`
- **Responsibilities**: Event schema validation, knowledge note quality, memory system health

**5. Project Management Domain** (`/project-docs/`)
- **Owner**: Project management lead
- **Scope**: Sprint plans, retrospectives, metrics reports, roadmaps
- **Patterns**: `/project-docs/**`, `/project-docs/sprints/**`, `/project-docs/metrics/**`
- **Responsibilities**: Sprint planning, metrics tracking, roadmap maintenance

**Cross-Domain Files** (shared ownership):
- `/AGENTS.md` - All domain leads (general agent patterns)
- `/CLAUDE.md` - All domain leads (Claude-specific workflows)
- `/README.md` - Documentation lead (primary) + all leads (review)
- `/justfile` - Automation lead (primary) + domain leads (for domain recipes)

**Validation Rules**:
- Each domain must have at least one assigned owner
- Owners can own multiple domains (especially in single-developer phase)
- Shared files must document primary owner + fallback owners
- Domain boundaries must be clear (no overlapping directory patterns)
- 80%+ of repository files should be covered by ownership patterns

**Enforcement**: Documented in CODEOWNERS file, validated by coverage analysis tool.

---

### Contract 3: Ownership Coverage Metrics Schema

**Description**: Metrics schema for tracking ownership coverage, orphan files, and review latency by domain.

**Metrics Schema** (JSON format):
```json
{
  "repository": "chora-workspace",
  "analysis_date": "2025-11-17T14:00:00Z",
  "total_files": 450,
  "covered_files": 360,
  "uncovered_files": 90,
  "coverage_percent": 80.0,

  "domain_coverage": [
    {
      "domain": "docs",
      "pattern": "/docs/**",
      "owner": "@victorpiper",
      "files_covered": 120,
      "percent_of_repo": 26.7,
      "avg_review_time_hours": 4.5
    },
    {
      "domain": "scripts",
      "pattern": "/scripts/**",
      "owner": "@victorpiper",
      "files_covered": 85,
      "percent_of_repo": 18.9,
      "avg_review_time_hours": 3.2
    }
  ],

  "orphan_files": [
    {
      "path": "temp/analysis.md",
      "size_bytes": 2048,
      "last_modified": "2025-11-10",
      "suggested_owner": "@victorpiper"
    }
  ],

  "recommendations": [
    {
      "type": "low_coverage",
      "message": "80% coverage meets target, but 90 orphan files should be assigned",
      "action": "Review orphan_files list and add patterns to CODEOWNERS"
    }
  ]
}
```

**Metrics Definitions**:

**Coverage Metrics**:
- `total_files`: Total tracked files in repository (excludes .git, node_modules, etc.)
- `covered_files`: Files matching at least one CODEOWNERS pattern
- `uncovered_files`: Files with no matching CODEOWNERS pattern (orphans)
- `coverage_percent`: (covered_files / total_files) × 100

**Domain Metrics**:
- `domain`: Human-readable domain name
- `pattern`: CODEOWNERS pattern defining domain
- `owner`: GitHub username(s) assigned to domain
- `files_covered`: Number of files matching this domain's pattern
- `percent_of_repo`: (files_covered / total_files) × 100
- `avg_review_time_hours`: Average time from PR creation to first review (requires GitHub API integration)

**Orphan Files**:
- `path`: File path relative to repository root
- `size_bytes`: File size in bytes
- `last_modified`: Last modification date (ISO 8601 format)
- `suggested_owner`: Recommended owner based on git history analysis

**Target Thresholds**:
- Minimum coverage: **80%** (production-ready)
- Target coverage: **90%+** (excellent)
- Orphan files: **<50 files** (acceptable), **<20 files** (excellent)
- Review time by domain: **<8 hours** (target), **<24 hours** (acceptable)

**Validation Rules**:
- Coverage analysis must run on git-tracked files only (exclude .git, build artifacts)
- Coverage percent must be calculated from actual file counts (not estimated)
- Orphan files must be sorted by last_modified (oldest first) for prioritization
- Suggested owners must be based on git log analysis (most commits in file)

**Enforcement**: Coverage analysis tool runs on-demand via `just ownership-coverage` recipe.

---

### Contract 4: Conflict Jurisdiction Rules

**Description**: Rules for determining conflict resolution authority based on code ownership.

**Jurisdiction Hierarchy**:

**Level 1: Domain Owner Authority** (primary)
- **Rule**: Domain owner has final decision authority for conflicts within their domain
- **Scope**: Conflicts where both versions modify files within single domain
- **Process**: Domain owner reviews both versions, makes final decision
- **Escalation**: None required (owner decides)

**Level 2: Cross-Domain Conflicts** (shared ownership)
- **Rule**: When conflict spans multiple domains, all affected domain owners collaborate
- **Scope**: Conflicts modifying files across 2+ domains
- **Process**: Affected owners review together, seek consensus
- **Escalation**: If no consensus after 24 hours, escalate to project lead

**Level 3: Project Lead Escalation** (final authority)
- **Rule**: Project lead makes final decision when domain owners cannot reach consensus
- **Scope**: Deadlocks, strategic conflicts, architecture-level decisions
- **Process**: Project lead reviews context, makes final call
- **Escalation**: No further escalation (project lead is final authority)

**Conflict Resolution Process**:

**Step 1: Identify Conflict Owner**
```bash
# For single-domain conflict
git diff --name-only main...feature-branch | head -1 | xargs -I {} grep {} CODEOWNERS
# Output: /docs/vision/mcp.md @victorpiper
# → Domain owner @victorpiper has jurisdiction
```

**Step 2: Domain Owner Review**
- Domain owner pulls both branches
- Reviews changes in context of domain standards
- Makes decision (accept version A, accept version B, or merge both)
- Documents decision rationale in PR comment

**Step 3: Cross-Domain Escalation** (if needed)
- If conflict spans multiple domains, tag all affected owners
- Owners collaborate on resolution (async discussion in PR)
- Seek consensus within 24 hours
- If consensus not reached, tag project lead for final decision

**Step 4: Project Lead Decision** (if escalated)
- Project lead reviews full context (code, discussion, domain impact)
- Makes final decision with architectural perspective
- Documents decision and rationale
- Decision is final (no further appeals)

**Example Scenarios**:

**Scenario 1: Single-domain conflict** (docs/)
```
Conflict: /docs/vision/mcp-ecosystem.md
Owner: @victorpiper (documentation lead)
Process: @victorpiper reviews both versions, chooses best for documentation clarity
Authority: @victorpiper has final say (no escalation)
```

**Scenario 2: Cross-domain conflict** (docs/ + scripts/)
```
Conflict: /justfile (shared between docs and scripts domains)
Owners: @victorpiper (scripts) + @victorpiper (docs, fallback)
Process: In pilot with single developer, same owner decides
Process (multi-dev): Both domain owners collaborate, seek consensus
Authority: Consensus required, else escalate to project lead
```

**Scenario 3: Strategic conflict** (architecture decision)
```
Conflict: Change affects multiple domains + architectural direction
Owners: All affected domain owners
Process: Owners discuss, but architectural implications unclear
Authority: Escalate to project lead for strategic decision
```

**Validation Rules**:
- Domain owner identification must be automated (based on CODEOWNERS file)
- Cross-domain conflicts must tag all affected owners (no owner left out)
- Escalation must occur within 24 hours if consensus not reached
- Project lead decisions must be documented with rationale (not arbitrary)

**Enforcement**: Documented process (not automated). Conflict resolution tracking in PR comments.

---

### Contract 5: Ownership Rotation Protocol

**Description**: Quarterly ownership rotation process for knowledge transfer and preventing burnout.

**Rotation Cadence**: Quarterly (every 3 months)

**Rotation Process**:

**Week 1: Ownership Review**
1. Review current ownership assignments (who owns what)
2. Identify domains needing rotation (high-load domains, burnout risk)
3. Identify candidates for ownership transfer (ready to take ownership)
4. Document rotation proposals in coordination request (SAP-001 inbox)

**Week 2: Knowledge Transfer**
1. Outgoing owner creates knowledge transfer document (domain-specific patterns, gotchas, tools)
2. Outgoing owner pairs with incoming owner (1-2 pairing sessions)
3. Incoming owner shadows outgoing owner on 1-2 PRs (review together)
4. Knowledge transfer document added to domain's AGENTS.md file

**Week 3: Ownership Handoff**
1. Update CODEOWNERS file (replace outgoing owner with incoming owner)
2. Announce ownership change in team communication (Slack, email, etc.)
3. Incoming owner takes primary responsibility (outgoing owner available for questions)
4. Outgoing owner becomes fallback reviewer for 1 month (backup)

**Week 4: Post-Rotation Validation**
1. Monitor incoming owner's review activity (ensure smooth transition)
2. Incoming owner provides feedback on knowledge transfer (what worked, what gaps)
3. Update ownership rotation playbook based on feedback
4. Document rotation in SAP-052 ledger (ownership change log)

**Knowledge Transfer Checklist**:
- [ ] Domain overview documented (scope, boundaries, key files)
- [ ] Common patterns documented (coding standards, documentation style, etc.)
- [ ] Gotchas documented (edge cases, known issues, workarounds)
- [ ] Tools documented (scripts, justfile recipes, validation commands)
- [ ] 1-2 pairing sessions completed (shadow reviews)
- [ ] Incoming owner has write access to domain directories
- [ ] Incoming owner added to CODEOWNERS file
- [ ] Team notified of ownership change

**Rotation Triggers** (non-quarterly):
- **Developer departure**: Immediate rotation required (emergency handoff)
- **Burnout risk**: Domain owner requests rotation due to workload
- **Skill development**: Developer wants to learn new domain (proactive rotation)
- **Strategic shift**: Organizational priority changes require ownership realignment

**Anti-Patterns** (avoid):
- ❌ **Rotating all domains simultaneously** - Disrupts continuity, rotate 1-2 domains per quarter
- ❌ **No knowledge transfer** - Incoming owner struggles, quality degrades
- ❌ **Permanent ownership** - Creates knowledge silos, prevents skill development
- ❌ **Forced rotation** - Respect domain owner expertise, rotate when beneficial

**Validation Rules**:
- Ownership rotation must be documented in coordination request (SAP-001)
- Knowledge transfer must be completed before CODEOWNERS update
- Outgoing owner must be available as fallback for 1 month post-rotation
- Rotation must be logged in SAP-052 ledger (audit trail)

**Enforcement**: Quarterly review process (documented in project management domain), tracked in SAP-052 ledger.

---

## 3. Data Schemas

### CODEOWNERS File Schema

**Format**: Plain text, gitignore-style patterns

**Line Types**:
1. **Comment**: `# <comment text>`
2. **Pattern**: `<file-pattern> <owner1> [owner2] [owner3]`
3. **Blank**: Empty line (ignored)

**Pattern Syntax** (gitignore-compatible):
- `*` - Matches zero or more characters (except `/`)
- `**` - Matches zero or more directories
- `?` - Matches single character
- `[abc]` - Matches any character in set
- `[0-9]` - Matches any digit
- `!<pattern>` - Negation (exclude pattern)

**Owner Syntax**:
- `@username` - Individual GitHub/GitLab user
- `@org/team-name` - GitHub/GitLab team (requires organization)
- Multiple owners space-separated: `@user1 @user2 @org/team`

**Example**:
```
# Documentation
/docs/ @doc-lead @doc-team

# Scripts (multiple individuals)
/scripts/ @automation-lead @devops-engineer

# Shared file (team ownership)
/justfile @org/infrastructure-team
```

---

### Ownership Coverage Report Schema

**Format**: JSON

**Schema**:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["repository", "analysis_date", "total_files", "covered_files", "coverage_percent"],
  "properties": {
    "repository": { "type": "string" },
    "analysis_date": { "type": "string", "format": "date-time" },
    "total_files": { "type": "integer", "minimum": 0 },
    "covered_files": { "type": "integer", "minimum": 0 },
    "uncovered_files": { "type": "integer", "minimum": 0 },
    "coverage_percent": { "type": "number", "minimum": 0, "maximum": 100 },
    "domain_coverage": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["domain", "pattern", "owner", "files_covered"],
        "properties": {
          "domain": { "type": "string" },
          "pattern": { "type": "string" },
          "owner": { "type": "string" },
          "files_covered": { "type": "integer", "minimum": 0 },
          "percent_of_repo": { "type": "number", "minimum": 0, "maximum": 100 },
          "avg_review_time_hours": { "type": "number", "minimum": 0 }
        }
      }
    },
    "orphan_files": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path"],
        "properties": {
          "path": { "type": "string" },
          "size_bytes": { "type": "integer", "minimum": 0 },
          "last_modified": { "type": "string", "format": "date" },
          "suggested_owner": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 4. Integration Points

### GitHub Integration

**CODEOWNERS Support**:
- Place CODEOWNERS file at repository root
- GitHub automatically parses file on PR creation
- GitHub assigns reviewers based on changed files in PR
- Multiple matches → all matching owners assigned as reviewers
- Team ownership requires GitHub organization (not personal repos)

**GitHub API Integration** (optional):
- Pull Requests API: Fetch review metrics (time to first review)
- Repository API: Validate CODEOWNERS syntax
- Teams API: Resolve team membership for ownership validation

**Example GitHub API Usage**:
```bash
# Validate CODEOWNERS syntax via GitHub API
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/codeowners/errors

# Fetch PR review metrics
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/pulls/123/reviews
```

---

### GitLab Integration

**CODEOWNERS Support**:
- Place CODEOWNERS file at repository root (or in `.gitlab/` directory)
- GitLab suggests approvers based on file patterns
- Requires GitLab Premium/Ultimate for full CODEOWNERS support
- Similar syntax to GitHub (gitignore-style patterns)

**Differences from GitHub**:
- GitLab uses CODEOWNERS for **approval rules** (not just suggestions)
- Can enforce "approvals required from code owners" (blocking rule)
- Supports sections for different approval logic

---

### SAP Integrations

**SAP-001 (Inbox)**:
- Coordination requests routed based on domain ownership
- CODEOWNERS mapping guides request assignment
- Ownership changes documented via coordination requests

**SAP-010 (Memory)**:
- Knowledge notes categorized by domain ownership
- Event logs track ownership changes (rotation, transfers)
- Domain owners responsible for knowledge note quality in their domain

**SAP-015 (Beads)**:
- Beads tasks assigned based on domain ownership
- Task ownership aligns with code ownership (docs tasks → docs owner)
- Ownership coverage metrics inform task distribution

**SAP-051 (Git Workflow)**:
- Branch naming conventions integrate with ownership (feature/docs-* → docs owner)
- PR workflows use automatic reviewer assignment from CODEOWNERS
- Merge conflicts resolved using ownership jurisdiction rules

---

## 5. Compatibility & Constraints

### Platform Requirements

**GitHub**:
- ✅ Full CODEOWNERS support (automatic reviewer assignment)
- ✅ Works on all GitHub plans (Free, Team, Enterprise)
- ✅ Supports individual and team ownership
- ⚠️ Team ownership requires GitHub organization (not personal repos)

**GitLab**:
- ✅ CODEOWNERS support (approval rules)
- ⚠️ Full support requires GitLab Premium/Ultimate (not Free tier)
- ✅ Supports individual and group ownership
- ✅ Can enforce approvals from code owners (blocking)

**Self-Hosted Git**:
- ⚠️ No automatic reviewer assignment (manual process)
- ✅ CODEOWNERS file still useful as documentation
- ✅ Coverage analysis tools work (git-based, not platform-dependent)
- ⚠️ Reviewer suggester requires git log access (works with any git)

---

### File Size Limitations

**CODEOWNERS File**:
- Recommended: <1000 lines (GitHub performance)
- Maximum: No hard limit, but GitHub may timeout on very large files
- Best practice: Use directory-level patterns (not file-level) to keep file small

**Repository Size**:
- Coverage analysis scales to repositories with 10k+ files
- Orphan file detection may be slow on very large repositories (>100k files)
- Recommend running coverage analysis on CI/CD (not locally) for large repos

---

## 6. Versioning & Evolution

**Current Version**: 1.0.0

**Versioning Scheme**: Semantic Versioning (MAJOR.MINOR.PATCH)
- **MAJOR**: Breaking changes to CODEOWNERS format or ownership schema
- **MINOR**: New features (additional metrics, new tools)
- **PATCH**: Bug fixes, documentation updates

**Future Enhancements** (post-1.0.0):
- **Dynamic ownership**: Ownership based on git history (not static CODEOWNERS)
- **Workload balancing**: Auto-suggest ownership rotation based on review load
- **Cross-repo ownership**: Federated ownership across chora ecosystem repos
- **Ownership analytics**: Dashboard showing ownership trends, bottlenecks, rotation history

**Deprecation Policy**:
- 6-month notice for breaking changes to CODEOWNERS format
- Migration guide provided for schema changes
- Backward compatibility maintained for at least 2 major versions

---

## 7. References

**External Standards**:
- GitHub CODEOWNERS: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitLab CODEOWNERS: https://docs.gitlab.com/ee/user/project/codeowners/
- Gitignore patterns: https://git-scm.com/docs/gitignore

**Related SAPs**:
- SAP-001 (Inbox): Coordination request routing
- SAP-010 (Memory): Knowledge note categorization
- SAP-015 (Beads): Task assignment
- SAP-051 (Git Workflow): PR automation, branch naming

**Tools**:
- CODEOWNERS template generator: `scripts/codeowners-generator.py` (to be created)
- Ownership coverage analysis: `scripts/ownership-coverage.py` (to be created)
- Reviewer suggester: `scripts/reviewer-suggester.py` (to be created)

---

**Created**: 2025-11-17 by chora-base maintainer + Claude (AI peer)
**Document Status**: Draft
**Last Updated**: 2025-11-17
