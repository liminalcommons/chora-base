# Awareness Guide: Ownership Zones

**SAP ID**: SAP-052
**Version**: 1.0.0
**For**: AI Agents, LLM-Based Assistants (Claude, GPT, Codex)
**Last Updated**: 2025-11-17

---

## 📖 Quick Reference

**New to SAP-052?** → Read **capability-charter.md** first (10-min read)

The charter provides:
- 🎯 **Problem** - Review coordination overhead (10-15 min/PR asking "who reviews?")
- 🔧 **Solution** - CODEOWNERS-based domain ownership with automatic reviewer assignment
- 📊 **Impact** - 40-60% reduction in reviewer coordination time, 15-25% faster PR reviews
- 🗺️ **Domains** - 5 chora-workspace domains (docs/, scripts/, inbox/, .chora/, project-docs/)
- ⚖️ **Jurisdiction** - Clear conflict resolution authority based on ownership
- 🔄 **Rotation** - Quarterly ownership rotation for knowledge transfer

This awareness-guide.md provides: Agent-specific workflows, decision trees, and patterns for AI coding assistants using SAP-052 ownership zones.

---

## Quick Start for AI Agents

### One-Sentence Summary

**SAP-052 defines code ownership zones via CODEOWNERS file enabling automatic reviewer assignment, conflict jurisdiction rules, and 40-60% reduction in "who should review?" coordination overhead for multi-developer collaboration.**

### When to Use This SAP

Use SAP-052 when:
- ✅ User asks "who should review this PR?" (check CODEOWNERS file for domain owner)
- ✅ User creates PR touching specific domain (suggest appropriate reviewer based on ownership)
- ✅ Merge conflict occurs (apply ownership jurisdiction rules)
- ✅ User asks about code ownership (explain domain mapping)
- ✅ Setting up new repository (generate CODEOWNERS file via template generator)
- ✅ User wants ownership metrics (run coverage analysis tool)
- ✅ Multi-developer coordination questions (integrate with SAP-051, SAP-053, SAP-054)
- ✅ User onboarding (explain ownership structure from CODEOWNERS)

Don't use SAP-052 for:
- ❌ Single-developer repositories (no reviewer assignment needed)
- ❌ Non-git workflows (ownership is git-based)
- ❌ Organizational hierarchy (SAP-052 is code ownership, not reporting structure)
- ❌ Performance reviews (ownership for code quality, not employee evaluation)

---

## 1. Core Concepts for Agents

### Key Concepts

**Concept 1**: CODEOWNERS File
- **Description**: GitHub/GitLab-compatible file mapping file patterns to domain owners
- **When to use**: Check CODEOWNERS when user asks "who owns this file?" or "who should review?"
- **Example**: `/docs/ @victorpiper` means @victorpiper owns all files in docs/ directory
- **Agent action**: Parse CODEOWNERS file, identify owner for changed files in PR

**Concept 2**: Domain Ownership Mapping
- **Description**: chora-workspace has 5 domains (docs/, scripts/, inbox/, .chora/, project-docs/)
- **When to use**: Categorize work by domain, route questions to domain owners
- **Example**: Documentation changes → docs domain → @victorpiper (docs owner)
- **Agent action**: Map file paths to domains, suggest appropriate owner for review

**Concept 3**: Ownership Coverage
- **Description**: % of files covered by ownership patterns in CODEOWNERS
- **When to use**: User asks "how complete is our ownership?" or wants metrics dashboard
- **Example**: 80% coverage = 360/450 files have assigned owners, 90 orphan files
- **Agent action**: Run coverage analysis tool, report % coverage and orphan files

**Concept 4**: Conflict Jurisdiction
- **Description**: Domain owner has authority to resolve conflicts within their domain
- **When to use**: Merge conflict occurs, need to determine who decides resolution
- **Example**: Conflict in /docs/vision/mcp.md → docs owner (@victorpiper) has jurisdiction
- **Agent action**: Identify conflict file, lookup owner in CODEOWNERS, assign jurisdiction

**Concept 5**: Ownership Rotation
- **Description**: Quarterly process for transferring ownership (knowledge transfer)
- **When to use**: User asks about ownership changes or quarterly rotation planning
- **Example**: Q1 → Q2: Transfer docs domain from @alice to @bob (with handoff)
- **Agent action**: Guide ownership rotation process, create knowledge transfer checklist

### Decision Tree

```
User request about code ownership
   │
   ├─ "Who should review this PR?"
   │   ├─ Check changed files in PR (git diff --name-only)
   │   ├─ Parse CODEOWNERS file (match file patterns)
   │   ├─ Identify matching owners for changed files
   │   └─ Suggest owner(s) as reviewers
   │
   ├─ "Who owns this file/directory?"
   │   ├─ Read CODEOWNERS file
   │   ├─ Match file path against patterns (last match wins)
   │   └─ Return owner username(s)
   │
   ├─ "Merge conflict - who decides?"
   │   ├─ Identify conflicted file paths (git diff --name-only --diff-filter=U)
   │   ├─ Check if all files in single domain → Domain owner has jurisdiction
   │   ├─ Check if files span multiple domains → All owners collaborate
   │   └─ If deadlock → Escalate to project lead
   │
   ├─ "Create CODEOWNERS file for new repo"
   │   ├─ Analyze directory structure (find domain boundaries)
   │   ├─ Run CODEOWNERS template generator (scripts/codeowners-generator.py)
   │   ├─ Review generated patterns with user
   │   └─ Commit CODEOWNERS to repository root
   │
   ├─ "What's our ownership coverage?"
   │   ├─ Run coverage analysis tool (scripts/ownership-coverage.py)
   │   ├─ Report % coverage, orphan files, domain metrics
   │   └─ Suggest patterns for uncovered files
   │
   └─ "Ownership rotation needed"
       ├─ Check quarterly rotation schedule (last rotation + 3 months)
       ├─ Create knowledge transfer document (domain patterns, gotchas)
       ├─ Pair outgoing/incoming owner (shadow reviews)
       └─ Update CODEOWNERS file (replace owner username)
```

---

## 2. Common Agent Workflows

### Workflow 1: Determine PR Reviewer

**User Request**: "Who should review this PR?"

**Agent Actions**:
1. **Analyze changed files** in PR:
   ```bash
   git diff --name-only main...feature-branch
   # Output:
   # docs/vision/mcp-ecosystem.md
   # docs/vision/architecture.md
   # scripts/validate-links.sh
   ```

2. **Parse CODEOWNERS** file to match owners:
   ```bash
   # CODEOWNERS file:
   /docs/ @victorpiper
   /scripts/ @victorpiper

   # Match:
   # docs/vision/mcp-ecosystem.md → @victorpiper (docs owner)
   # docs/vision/architecture.md → @victorpiper (docs owner)
   # scripts/validate-links.sh → @victorpiper (scripts owner)
   ```

3. **Suggest reviewer(s)**:
   "This PR touches the **docs** and **scripts** domains. Based on CODEOWNERS:
   - @victorpiper owns both domains
   - Suggested reviewer: @victorpiper
   - GitHub will auto-assign @victorpiper when you create the PR"

**Validation**:
```bash
# Verify CODEOWNERS patterns match correctly
git ls-files | while read file; do
  # Check if file matches /docs/ pattern
  if [[ "$file" == docs/* ]]; then
    echo "$file → @victorpiper"
  fi
done
```

**Expected Output**:
```
docs/vision/mcp-ecosystem.md → @victorpiper
docs/vision/architecture.md → @victorpiper
```

**Common Variations**:
- **Cross-domain PR**: Multiple domains → Multiple owners → "PR touches docs and scripts. Suggested reviewers: @victorpiper (both domains)"
- **Orphan files**: No CODEOWNERS match → "File `temp/analysis.md` has no owner. Suggest adding pattern to CODEOWNERS or request manual review"
- **Team ownership**: Pattern like `/docs/ @org/docs-team` → "Suggested reviewers: @org/docs-team (any team member can review)"

---

### Workflow 2: Resolve Merge Conflict Jurisdiction

**User Request**: "Merge conflict in docs/vision/mcp.md - who should resolve?"

**Agent Actions**:
1. **Identify conflicted files**:
   ```bash
   git diff --name-only --diff-filter=U
   # Output: docs/vision/mcp.md
   ```

2. **Lookup owner in CODEOWNERS**:
   ```bash
   # CODEOWNERS file:
   /docs/ @victorpiper

   # Match:
   # docs/vision/mcp.md → @victorpiper
   ```

3. **Apply jurisdiction rules**:
   "Conflict in **single domain** (docs/):
   - Domain owner: @victorpiper
   - **Jurisdiction**: @victorpiper has authority to resolve
   - Process: @victorpiper reviews both versions, chooses best for documentation clarity
   - No escalation needed (domain owner decides)"

4. **If cross-domain conflict**:
   ```bash
   # Example: justfile (shared file)
   # CODEOWNERS:
   /justfile @victorpiper @automation-lead

   # Conflict resolution:
   # Both owners collaborate → Seek consensus within 24 hours
   # If no consensus → Escalate to project lead
   ```

**Expected Outcome**:
```
✅ Conflict resolved by domain owner
✅ Resolution documented in PR comment (rationale for choice)
✅ Changes committed with conflict resolution commit
```

**Common Variations**:
- **Cross-domain conflict**: "Conflict spans docs/ and scripts/. Both @victorpiper (docs) and @automation-lead (scripts) must collaborate."
- **No owner match**: "Conflict in `temp/analysis.md` (no CODEOWNERS match). Recommend manual reviewer assignment."
- **Deadlock**: "Owners cannot reach consensus after 24 hours. Escalating to project lead for final decision."

---

### Workflow 3: Generate CODEOWNERS File

**User Request**: "Create CODEOWNERS file for chora-workspace"

**Agent Actions**:
1. **Analyze directory structure**:
   ```bash
   ls -d */
   # Output:
   # docs/ scripts/ inbox/ .chora/ project-docs/ test-integration-all/ ...
   ```

2. **Identify primary domains** (filter out build/test directories):
   ```
   Primary domains:
   - docs/ (documentation)
   - scripts/ (automation)
   - inbox/ (coordination)
   - .chora/ (memory system)
   - project-docs/ (project management)
   ```

3. **Generate CODEOWNERS template**:
   ```bash
   # Run template generator
   python scripts/codeowners-generator.py --repo chora-workspace

   # Generated CODEOWNERS:
   # chora-workspace CODEOWNERS
   # Defines ownership for 5 primary domains

   # Documentation domain
   /docs/ @victorpiper
   *.md @victorpiper

   # Scripts/Automation domain
   /scripts/ @victorpiper
   justfile @victorpiper

   # Coordination/Inbox domain
   /inbox/ @victorpiper

   # Memory system domain
   /.chora/ @victorpiper

   # Project management domain
   /project-docs/ @victorpiper

   # Shared files
   /AGENTS.md @victorpiper
   /CLAUDE.md @victorpiper
   /README.md @victorpiper
   ```

4. **Review with user**:
   "I've generated a CODEOWNERS file with 5 domains. Review:
   - All domains currently assigned to @victorpiper (single developer)
   - 80%+ files covered (estimate)
   - Shared files (AGENTS.md, CLAUDE.md, README.md) explicitly assigned
   - Ready to commit to repository root"

**Validation**:
```bash
# Validate CODEOWNERS syntax (GitHub API)
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/codeowners/errors

# Expected: No errors (valid syntax)
```

**Common Variations**:
- **Multi-developer repo**: Assign different owners per domain ("docs/ → @alice, scripts/ → @bob")
- **Team ownership**: Use team names ("/docs/ @org/docs-team")
- **Nested domains**: Add specific patterns ("/docs/vision/ @vision-lead" overrides "/docs/ @doc-lead")

---

### Workflow 4: Check Ownership Coverage

**User Request**: "What's our ownership coverage?"

**Agent Actions**:
1. **Run coverage analysis tool**:
   ```bash
   python scripts/ownership-coverage.py --repo chora-workspace
   ```

2. **Parse coverage metrics**:
   ```json
   {
     "repository": "chora-workspace",
     "total_files": 450,
     "covered_files": 360,
     "uncovered_files": 90,
     "coverage_percent": 80.0,
     "domain_coverage": [
       {"domain": "docs", "files_covered": 120, "percent_of_repo": 26.7},
       {"domain": "scripts", "files_covered": 85, "percent_of_repo": 18.9},
       {"domain": "inbox", "files_covered": 55, "percent_of_repo": 12.2},
       {"domain": ".chora", "files_covered": 70, "percent_of_repo": 15.6},
       {"domain": "project-docs", "files_covered": 30, "percent_of_repo": 6.7}
     ],
     "orphan_files": [
       {"path": "temp/analysis.md", "last_modified": "2025-11-10"},
       {"path": "test-integration-all/Lib/site-packages/...", "last_modified": "2025-10-15"}
     ]
   }
   ```

3. **Report to user**:
   "**Ownership Coverage Report**:
   - **80% coverage** (360/450 files) ✅ Meets target (≥80%)
   - **90 orphan files** (no assigned owner)
   - **Top orphans**: temp/, test-integration-all/ (build artifacts)

   **Domain Breakdown**:
   - docs: 120 files (26.7%) - @victorpiper
   - scripts: 85 files (18.9%) - @victorpiper
   - inbox: 55 files (12.2%) - @victorpiper
   - .chora: 70 files (15.6%) - @victorpiper
   - project-docs: 30 files (6.7%) - @victorpiper

   **Recommendations**:
   1. Add pattern for temp/ files (or exclude from coverage)
   2. Exclude test-integration-all/ (build artifacts, not source code)
   3. Coverage is production-ready (≥80%)"

**Common Variations**:
- **Low coverage (<80%)**: "Coverage is 65% (below 80% target). Review orphan files and add patterns to CODEOWNERS."
- **High coverage (>90%)**: "Coverage is 95% (excellent). Only 22 orphan files remaining."
- **Domain imbalance**: "Docs domain owns 50% of repo. Consider splitting into sub-domains."

---

### Workflow 5: Ownership Rotation

**User Request**: "Quarterly rotation - transfer docs domain from @alice to @bob"

**Agent Actions**:
1. **Create knowledge transfer checklist**:
   ```markdown
   # Ownership Rotation: docs domain (@alice → @bob)

   ## Knowledge Transfer Checklist
   - [ ] Domain overview documented (scope, boundaries, key files)
   - [ ] Common patterns documented (style guide, link validation)
   - [ ] Gotchas documented (vision/ is aspirational, research/ is archived)
   - [ ] Tools documented (validate-links.sh, doc-search.py)
   - [ ] 1-2 pairing sessions completed (shadow doc reviews)
   - [ ] @bob has write access to docs/ directory
   - [ ] @bob added to CODEOWNERS file
   - [ ] Team notified of ownership change
   ```

2. **Guide pairing process**:
   "**Week 1-2: Knowledge Transfer**
   - @alice creates knowledge note: `docs-domain-ownership-guide.md`
   - @alice and @bob pair on 1-2 doc PRs (shadow reviews)
   - @bob reviews guide, asks clarifying questions

   **Week 3: Ownership Handoff**
   - Update CODEOWNERS: `/docs/ @bob` (replace @alice)
   - Announce change to team
   - @bob takes primary responsibility
   - @alice available as fallback for 1 month"

3. **Update CODEOWNERS**:
   ```bash
   # Before:
   /docs/ @alice

   # After:
   /docs/ @bob
   /docs/ @alice  # Fallback for 1 month (optional)
   ```

4. **Log rotation in ledger**:
   ```json
   {
     "timestamp": "2025-12-01T00:00:00Z",
     "type": "ownership_rotation",
     "domain": "docs",
     "from_owner": "@alice",
     "to_owner": "@bob",
     "knowledge_transfer_complete": true,
     "pairing_sessions": 2
   }
   ```

**Common Variations**:
- **Emergency handoff**: "Developer departure requires immediate rotation (skip pairing, prioritize knowledge doc)"
- **Cross-training**: "Developer wants to learn new domain (proactive rotation for skill development)"
- **Burnout prevention**: "Domain owner requests rotation due to workload (respect request, find replacement)"

---

## 3. Integration with Other SAPs

### SAP-001 (Inbox): Coordination Request Routing

**Integration Point**: Route coordination requests based on domain ownership

**Workflow**:
```
User creates coordination request
   │
   ├─ Request targets specific domain (e.g., docs/)
   ├─ Check CODEOWNERS for domain owner
   ├─ Route request to domain owner for review
   └─ Domain owner reviews and approves/rejects
```

**Agent Action**: "This coordination request affects **docs/** domain. Routing to @victorpiper (docs owner) for review."

---

### SAP-010 (Memory): Knowledge Note Categorization

**Integration Point**: Categorize knowledge notes by domain ownership

**Workflow**:
```
User creates knowledge note
   │
   ├─ Determine note topic (e.g., ownership-zone-patterns)
   ├─ Map topic to domain (ownership patterns → .chora/ memory system)
   ├─ Assign ownership to domain owner (.chora/ → @victorpiper)
   └─ Domain owner reviews knowledge note quality
```

**Agent Action**: "This knowledge note about ownership zones belongs to **.chora/** domain. Owner @victorpiper will maintain note quality."

---

### SAP-015 (Beads): Task Assignment

**Integration Point**: Assign beads tasks based on domain ownership

**Workflow**:
```
User creates beads task
   │
   ├─ Task targets specific domain (e.g., "Fix docs/ links")
   ├─ Check CODEOWNERS for domain owner
   ├─ Suggest domain owner as assignee
   └─ Domain owner accepts and completes task
```

**Agent Action**: "This beads task affects **docs/** domain. Suggested assignee: @victorpiper (docs owner)."

---

### SAP-051 (Git Workflow): PR Automation

**Integration Point**: Combine branch naming with ownership for automatic reviewer assignment

**Workflow**:
```
User creates feature branch
   │
   ├─ Branch name: feature/SAP-052-ownership-zones
   ├─ Changed files: docs/skilled-awareness/ownership-zones/*.md
   ├─ Check CODEOWNERS: /docs/ @victorpiper
   ├─ GitHub auto-assigns @victorpiper as reviewer
   └─ @victorpiper reviews PR based on docs domain expertise
```

**Agent Action**: "Feature branch **feature/SAP-052-ownership-zones** touches **docs/** domain. GitHub will auto-assign @victorpiper as reviewer."

---

## 4. Edge Cases & Troubleshooting

### Edge Case 1: No CODEOWNERS Match (Orphan File)

**Scenario**: User asks "who should review changes to `temp/analysis.md`?"

**Agent Response**:
"File `temp/analysis.md` has **no owner** in CODEOWNERS (orphan file).

**Options**:
1. **Add pattern to CODEOWNERS**: If temp/ files should be reviewed, add `/temp/ @owner`
2. **Exclude from coverage**: If temp/ is build artifacts, add to .gitignore
3. **Manual assignment**: Request specific reviewer manually for this PR

**Recommendation**: Check if temp/ contains important files. If yes, add owner. If no, exclude from git."

---

### Edge Case 2: Cross-Domain Conflict Deadlock

**Scenario**: Two domain owners cannot agree on conflict resolution after 24 hours

**Agent Response**:
"**Escalation Required**: Cross-domain conflict deadlock

- Conflicted file: `/justfile` (shared between docs and scripts domains)
- Owners: @victorpiper (docs), @automation-lead (scripts)
- Status: No consensus after 24 hours
- **Next step**: Escalate to project lead for final decision

**Escalation Process**:
1. Tag project lead in PR comment
2. Summarize both perspectives (docs vs scripts concerns)
3. Request final decision with architectural context
4. Project lead's decision is final (no further appeals)"

---

### Edge Case 3: CODEOWNERS Syntax Error

**Scenario**: GitHub doesn't auto-assign reviewers (CODEOWNERS invalid)

**Agent Response**:
"**CODEOWNERS syntax error detected**

**Common Issues**:
1. **Missing @**: Owner must start with @ (e.g., `@username`, not `username`)
2. **Invalid pattern**: Patterns use gitignore syntax (e.g., `/docs/`, not `docs`)
3. **File location**: CODEOWNERS must be at repository root (not in subdirectory)
4. **Team name format**: Teams must use `@org/team-name` (not `@team-name`)

**Validation**:
```bash
# Use GitHub API to check for errors
curl -H \"Authorization: token $GITHUB_TOKEN\" \\
  https://api.github.com/repos/owner/repo/codeowners/errors
```

**Expected**: No errors (empty array)"

---

### Edge Case 4: Single Owner for All Domains (Pilot Phase)

**Scenario**: chora-workspace pilot has @victorpiper owning all 5 domains

**Agent Response**:
"**Single-owner configuration** (pilot phase):

- All 5 domains owned by @victorpiper
- **Impact**: No automatic load balancing (all reviews go to one person)
- **Benefit**: Simplifies ownership during pilot validation
- **Future**: Add second developer → split ownership across domains

**When to split ownership**:
1. Second developer joins → Assign 2-3 domains to new developer
2. Workload imbalance → Original owner keeps 2 domains, transfers 3 domains
3. Expertise alignment → Assign domains based on developer strengths (docs → writer, scripts → automation expert)"

---

## 5. Performance Considerations

### CODEOWNERS File Size

**Guideline**: Keep CODEOWNERS <1000 lines

**Reason**: GitHub parses CODEOWNERS on every PR creation. Very large files (>1000 lines) may cause slow reviewer assignment.

**Best Practice**:
- Use **directory-level patterns** (`/docs/` not `docs/file1.md`, `docs/file2.md`, ...)
- Avoid file-level patterns unless necessary (shared files only)
- Combine patterns with wildcards (`*.md` not individual .md files)

---

### Coverage Analysis Performance

**Guideline**: Coverage analysis scales to 10k+ files

**Performance**:
- Small repo (< 1k files): <5 seconds
- Medium repo (1k-10k files): 5-30 seconds
- Large repo (10k-100k files): 30-120 seconds

**Optimization**:
- Run analysis on CI/CD (not locally) for large repos
- Exclude build artifacts from analysis (.git, node_modules, test-integration-all)
- Cache analysis results (re-run only when CODEOWNERS or file structure changes)

---

## 6. Security Considerations

### CODEOWNERS as Security Boundary

**NOT a security control**: CODEOWNERS does not prevent unauthorized commits

**What it provides**:
- ✅ **Review guidance**: Suggests appropriate reviewers based on expertise
- ✅ **Accountability**: Documents who is responsible for code quality
- ✅ **Process**: Defines conflict resolution authority

**What it does NOT provide**:
- ❌ **Access control**: Does not prevent users from editing files they don't own
- ❌ **Enforcement**: Does not block commits to files outside ownership
- ❌ **Security**: Not a substitute for branch protection rules or CI/CD checks

**Security Best Practices**:
- Use GitHub branch protection (require reviews before merge)
- Combine CODEOWNERS with CI/CD validation (tests must pass)
- Use GitHub required reviewers (block merge without owner approval) - requires GitHub Pro/Enterprise

---

## 7. Tools Reference

### CODEOWNERS Template Generator

**Command**: `python scripts/codeowners-generator.py --repo <repo-name>`

**Purpose**: Generate CODEOWNERS file from directory structure

**Output**: CODEOWNERS file with directory-level patterns

---

### Ownership Coverage Analysis

**Command**: `python scripts/ownership-coverage.py --repo <repo-name>`

**Purpose**: Calculate ownership coverage metrics

**Output**: JSON report with coverage %, orphan files, domain breakdown

---

### Reviewer Suggester

**Command**: `python scripts/reviewer-suggester.py --file <path>`

**Purpose**: Suggest reviewer based on git history

**Output**: Username of developer with most commits to file

---

**Created**: 2025-11-17 by chora-base maintainer + Claude (AI peer)
**Document Status**: Draft
**Last Updated**: 2025-11-17
