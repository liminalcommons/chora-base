# Adoption Blueprint: Work Context Coordination (Multi-Tab/Multi-Developer)

**Modern Namespace**: `chora.coordination.work_context`
**Legacy Aliases**: SAP-054 (multi-tab), SAP-055 (multi-developer)
**Version**: 1.0.0
**Status**: Pilot (Level 1 - Lightweight)
**Last Updated**: 2025-11-20

---

## 1. Read Before You Begin

- **Capability Charter**: [capability-charter.md](capability-charter.md)
- **Protocol Spec**: [protocol-spec.md](protocol-spec.md)
- **Agent Patterns**: [AGENTS.md](AGENTS.md)
- **Prerequisites**:
  - Repository uses Git (for branch tracking)
  - Justfile installed (`just --version` to verify)
  - Optional: `yq` for YAML parsing (Python 3 fallback if unavailable)
  - Multiple concurrent work contexts (tabs, developers, or sessions)

---

## 2. Installation

### Quick Install (5 minutes)

**Option A: Manual Installation** (copy artifacts from chora-base)

```bash
# Step 1: Copy shell scripts
cp /path/to/chora-base/scripts/who-is-working-on.sh scripts/
cp /path/to/chora-base/scripts/detect-conflicts.sh scripts/
chmod +x scripts/who-is-working-on.sh scripts/detect-conflicts.sh

# Step 2: Copy justfile recipes
# Append lines 1779-1847 from chora-base/justfile to your justfile
# Or use:
curl https://raw.githubusercontent.com/.../chora-base/justfile | sed -n '1779,1847p' >> justfile

# Step 3: Create work context registry directory
mkdir -p .chora

# Step 4: Copy SAP documentation
mkdir -p docs/skilled-awareness/work-context-coordination
cp /path/to/chora-base/docs/skilled-awareness/work-context-coordination/*.md \
   docs/skilled-awareness/work-context-coordination/

# Step 5: Update .gitignore (optional - keep contexts in git for coordination)
# Add to .gitignore if you want local-only contexts:
# .chora/work-contexts.yaml
```

**Option B: Automated Installation** (using install-sap.py)

```bash
# If your project has SAP installation tooling:
python scripts/install-sap.py chora.coordination.work_context --source /path/to/chora-base
```

### Validation

Verify installation:

```bash
# Test justfile recipes exist
just --list | grep work-context
# Expected output:
#   work-context-register    # Register work context (tab, developer, session)
#   work-dashboard           # Show active contexts + conflict zones
#   who-is-working-on        # Query file ownership

# Test shell scripts are executable
bash scripts/who-is-working-on.sh
# Expected output: "Usage: ..." (error message showing script is executable)

# Test work context registration
just work-context-register test-context tab main "README.md"
# Expected output: "✅ Context test-context registered"

# Verify registry created
cat .chora/work-contexts.yaml
# Expected: YAML file with test-context entry

# Clean up test
rm .chora/work-contexts.yaml
```

---

## 3. Basic Usage

### Scenario: Single Developer, Multiple Tabs

**Tab 1 (SAP adoption work)**:
```bash
# Register context on session start
just work-context-register tab-1 tab main "docs/skilled-awareness/sap-xxx/**/*,justfile"

# Check who's working on justfile before editing
just who-is-working-on justfile
# Output: tab-1 (tab) → Safe to edit (I own it)
```

**Tab 2 (Bug fix work)**:
```bash
# Register context
just work-context-register tab-2 tab bugfix/auth-issue "src/auth/**/*,tests/test_auth.py"

# Check dashboard to see all active work
just work-dashboard
# Output:
#   Active Work Contexts:
#     tab-1 (tab) on main: docs/skilled-awareness/sap-xxx/**/*,justfile
#     tab-2 (tab) on bugfix/auth-issue: src/auth/**/*,tests/test_auth.py
#   Conflict Zones:
#     ✅ No conflicts detected
```

**Tab 2 (wants to edit justfile)**:
```bash
just who-is-working-on justfile
# Output: justfile is edited by multiple contexts: [CONFLICT]
#           - tab-1 (tab)
# Action: Coordinate with tab-1 before editing (switch tabs, or defer)
```

### Scenario: Multiple Developers

**Developer Alice**:
```bash
# Register context on workday start
just work-context-register alice dev alice/feat/new-feature "src/feature/**/*,docs/feature.md"
```

**Developer Bob**:
```bash
# Register context
just work-context-register bob dev bob/refactor/cleanup "src/utils/**/*,tests/test_utils.py,justfile"

# Check for conflicts before editing justfile
just who-is-working-on justfile
# Output: bob (dev) → I'm the only one editing, safe to proceed
```

**Alice (later wants to edit justfile)**:
```bash
just who-is-working-on justfile
# Output: [CONFLICT] bob (dev)
# Action: Message Bob: "Hey, I need to edit justfile for 15 minutes, can you pause?"
```

---

## 4. Configuration

### Work Context Types

Work contexts support three types:

| Type      | Use Case                              | Example ID       |
|-----------|---------------------------------------|------------------|
| `tab`     | Claude Code tabs, browser tabs        | `tab-1`, `tab-2` |
| `dev`     | Human developers                      | `alice`, `bob`   |
| `session` | Session-based work (morning/evening)  | `session-morning`, `session-evening` |

### File Pattern Syntax

File patterns use glob syntax:

```yaml
files:
  - "docs/**/*.md"              # All markdown in docs/
  - "src/feature/**/*"          # All files in src/feature/
  - "justfile"                  # Exact file match
  - "*.py"                      # All Python files in current directory
  - "scripts/*.{sh,py}"         # Shell or Python scripts in scripts/
```

### Work Context Registry Schema

`.chora/work-contexts.yaml`:
```yaml
work_contexts:
  - id: string              # Unique identifier (tab-1, alice, session-morning)
    type: enum              # "tab" | "dev" | "session"
    branch: string          # Current git branch
    files: list[string]     # File patterns (glob syntax)
    started_at: datetime    # ISO 8601 timestamp
    last_activity: datetime # Optional, for future real-time tracking
```

---

## 5. Integration with Existing SAPs

### SAP-051 (Git Workflow Patterns)

**Branch Naming**: Use context prefix

```bash
# Tab contexts
just work-context-register tab-1 tab tab1/feat/new-ui "src/ui/**/*"

# Developer contexts
just work-context-register alice dev alice/refactor/api "src/api/**/*"
```

**Benefits**:
- Branch name indicates work context ownership
- Natural conflict prevention via git branches
- Easy to identify which tab/developer created a branch

### SAP-052 (Code Ownership)

**Ownership Zones Guide Work Partitioning**:
```bash
# Alice owns docs/, Bob owns scripts/
# Minimal overlap reduces conflict risk
just work-context-register alice dev main "docs/**/*"
just work-context-register bob dev main "scripts/**/*"

# Dashboard shows clean separation:
just work-dashboard
# Output: ✅ No conflicts detected (different ownership zones)
```

### SAP-053 (Conflict Resolution)

**Pre-Merge Validation**:
```bash
# Before merging tab1/feat/x into main
just conflict-check main
# Detects git-level conflicts

# Combined with work context awareness:
just who-is-working-on src/utils/helpers.py
# Detects editing conflicts before commit
```

**Workflow**:
1. Check work context conflicts: `just who-is-working-on <file>`
2. If clear, edit and commit
3. Before merge: `just conflict-check main`
4. If clear, merge branch

---

## 6. Exit Code API

All `who-is-working-on` queries use standardized exit codes:

| Exit Code | Meaning         | Action                                    |
|-----------|-----------------|-------------------------------------------|
| 0         | Single owner    | Safe to edit (you own it)                 |
| 1         | Multiple owners | **CONFLICT** - Coordinate before editing  |
| 2         | No owner        | Unclaimed - Safe to claim and edit        |

**Example: Pre-Edit Check in Scripts**

```bash
#!/usr/bin/env bash
if just who-is-working-on justfile 2>/dev/null; then
    echo "Safe to edit justfile"
    vim justfile
else
    exitcode=$?
    if [ $exitcode -eq 1 ]; then
        echo "❌ Conflict detected - justfile owned by another context"
        exit 1
    elif [ $exitcode -eq 2 ]; then
        echo "✅ justfile unclaimed, registering ownership..."
        just work-context-register my-context tab main "justfile"
        vim justfile
    fi
fi
```

---

## 7. High-Risk Files (Always Check Before Editing)

**Infrastructure Files** (frequent conflict zones):
- `justfile` - Automation recipes
- `AGENTS.md`, `CLAUDE.md` - Agent awareness guides
- `INDEX.md` - SAP catalog
- `.chora/work-contexts.yaml` - Work context registry itself

**Append-Only Logs** (merge conflict risk):
- `.chora/memory/events/*.jsonl` - A-MEM event logs

**Active Project Files**:
- Sprint plans: `project-docs/sprints/sprint-N.md` (where N is current sprint)
- Coordination requests: `inbox/incoming/coordination/*.json`

**Recommended Workflow**:
```bash
# Before editing any high-risk file:
just who-is-working-on <file>

# If conflict (exit code 1):
#   - Coordinate with other context (message, switch tabs, defer)
# If no owner (exit code 2):
#   - Claim it: add to your context's file patterns
# If you own it (exit code 0):
#   - Proceed safely
```

---

## 8. Troubleshooting

### "yq: command not found" Error

Work context coordination uses `yq` for YAML parsing (preferred) but falls back to Python if unavailable.

**Solution**: No action needed - Python fallback handles this automatically.

**Optional**: Install `yq` for faster YAML parsing:
```bash
# macOS
brew install yq

# Linux
snap install yq

# Or: https://github.com/mikefarah/yq/releases
```

### "No context editing <file>" (Exit Code 2)

This means the file isn't owned by any registered context - it's unclaimed.

**Action**: Safe to edit. Optionally register ownership:
```bash
just work-context-register my-context tab main "<file>"
```

### Multiple Contexts Claim Same File

This is **expected behavior** for shared files like `justfile`.

**Resolution**:
1. View conflict: `just who-is-working-on justfile`
2. Coordinate: Message other context or switch tabs
3. Edit when safe (other context confirms they're not editing)

**Prevention**: Use work partitioning (different domains, branches, or file groups).

### Work Context Registry Merge Conflict

If two developers simultaneously edit `.chora/work-contexts.yaml`:

**Recovery**:
```bash
# Accept both changes (YAML list append is safe)
git checkout --ours .chora/work-contexts.yaml
git show :3:.chora/work-contexts.yaml >> .chora/work-contexts.yaml

# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('.chora/work-contexts.yaml'))"

# Commit merged registry
git add .chora/work-contexts.yaml
git commit -m "Merge work contexts: append both registrations"
```

---

## 9. Advanced Usage (Future L3 - Capability Server)

**Current Status**: L1 (Pilot) - Shell scripts + YAML

**Future L3** (not yet implemented):
- Real-time conflict notifications via WebSocket
- Automated work partitioning suggestions
- Cross-repo coordination (workspace-level visibility)
- REST API: `/api/v1/contexts/register`, `/api/v1/conflicts`
- MCP tools integration: `work-context-register()`, `who-is-working-on()`

**ROI Projection**:
- L1 (Current): 420% Year 1 ($3,900 savings on $750 investment)
- L3 (Future): 204% Year 1 ($6,390 savings on $2,100 investment)

To upgrade to L3 when available:
1. Generate chora-coordination capability server from SAP-047 template (5 min)
2. Install and configure capability server (1 hour)
3. Migrate work-contexts.yaml to capability server storage
4. Update justfile recipes to call capability server API

---

## 10. Adoption Checklist

**Pre-Adoption** (5 min):
- [ ] Read capability-charter.md
- [ ] Read protocol-spec.md
- [ ] Verify prerequisites (Git, justfile, Python 3)

**Installation** (5 min):
- [ ] Copy shell scripts to `scripts/`
- [ ] Make scripts executable (`chmod +x`)
- [ ] Copy justfile recipes (lines 1779-1847)
- [ ] Create `.chora/` directory
- [ ] Copy SAP documentation to `docs/skilled-awareness/work-context-coordination/`

**Validation** (2 min):
- [ ] Test `just work-context-register` (create test context)
- [ ] Test `just work-dashboard` (view contexts)
- [ ] Test `just who-is-working-on` (query ownership)
- [ ] Verify `.chora/work-contexts.yaml` created

**Integration** (5 min):
- [ ] Update AGENTS.md with multi-context coordination section
- [ ] Document high-risk files for your project
- [ ] Communicate workflow to team (if multi-developer)

**Ongoing Usage** (2 min/session):
- [ ] Register work context at session start
- [ ] Check `just who-is-working-on <file>` before editing high-risk files
- [ ] Run `just work-dashboard` periodically to see all active work

**L2 Adoption Complete**:
- [ ] Update ledger.md (add your project as adopter)
- [ ] Create knowledge note documenting learnings
- [ ] Emit A-MEM event: `work_context_coordination_adopted`

---

## 11. Support & Resources

**Documentation**:
- Capability Charter: [capability-charter.md](capability-charter.md)
- Protocol Spec: [protocol-spec.md](protocol-spec.md)
- Agent Patterns: [AGENTS.md](AGENTS.md)

**Integration References**:
- SAP-051 (Git Workflow): [../git-workflow-patterns/](../git-workflow-patterns/)
- SAP-052 (Code Ownership): [../code-ownership/](../code-ownership/)
- SAP-053 (Conflict Resolution): [../conflict-resolution/](../conflict-resolution/)

**Knowledge Notes**:
- L1 Pilot Validation: [.chora/memory/knowledge/notes/2025-11-20-work-context-coordination-pilot.md](../../../.chora/memory/knowledge/notes/2025-11-20-work-context-coordination-pilot.md)

**Questions or Issues**:
- Check ledger.md for adopter experiences
- Search knowledge notes for patterns: `grep -r "work.*context" .chora/memory/knowledge/notes/`
- Review A-MEM events: `grep "work_context" .chora/memory/events/*.jsonl`

---

## 12. Migration Path (Future)

**From L1 (Current) to L3 (Capability Server)**:

When chora-coordination capability server is released:

1. **Install capability server** (5 min + 1 hour setup):
   ```bash
   # Generate capability server from SAP-047 template
   just generate-capability-server chora-coordination

   # Deploy locally via Docker
   docker-compose -f packages/chora-coordination/docker-compose.yml up -d
   ```

2. **Migrate registry** (10 min):
   ```bash
   # Import existing work-contexts.yaml to capability server
   curl -X POST http://localhost:8080/api/v1/contexts/import \
     -H "Content-Type: application/yaml" \
     --data-binary @.chora/work-contexts.yaml
   ```

3. **Update justfile recipes** (15 min):
   ```bash
   # Replace shell script calls with capability server API calls
   # Justfile recipes stay the same (interface unchanged)
   # Backend switches from scripts to REST API
   ```

4. **Enable real-time features** (optional, 30 min):
   - WebSocket conflict notifications
   - Automated work partitioning suggestions
   - Cross-repo workspace-level coordination

**Backward Compatibility**: L1 justfile recipes remain functional (same interface, different backend).

---

**Version History**:
- **1.0.0** (2025-11-20): Initial L1 pilot adoption blueprint
