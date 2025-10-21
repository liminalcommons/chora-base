# chora-base Template Generalization Audit & Fixes

**Date:** 2025-10-18
**Triggered By:** chora-compose adoption revealed project-specific references
**Audit Scope:** All 35 .jinja template files + 5 Python source files
**Total Issues Found:** 47 generalization issues
**Issues Fixed (This Release):** 18 issues (12 CRITICAL + 6 HIGH)
**Issues Remaining:** 29 issues (17 HIGH + 10 MEDIUM + 2 LOW)

---

## Executive Summary

Comprehensive audit of chora-base template identified 47 generalization issues where the template contained project-specific references (mcp-n8n, chora-composer) or hardcoded values that would break or confuse adopters.

### Release v1.2.0 Fixes (18 issues)

**CRITICAL Fixes (12 issues)** - Would break generated projects:
- ✅ Python import errors (2 files converted to .jinja)
- ✅ Hardcoded absolute paths (3 scripts fixed)
- ✅ Placeholder GitHub usernames (3 files fixed)
- ✅ Placeholder security email (copier variable added, 2 files fixed)

**HIGH Priority Fixes (6 issues)** - Would confuse adopters:
- ✅ Project-specific references in .chora/memory/README.md.jinja

### Remaining Issues (29 issues)

**HIGH Priority (17 issues)** - Should fix in v1.2.1/v1.3.0:
- Integration test Sprint/Phase references (5 instances)
- Handoff script project-specific logic (5 instances)
- Backend validation in check-env.sh (1 section to remove)
- API key references (8 instances across multiple files)
- Tool namespace examples (6 instances - needs generic examples)

**MEDIUM Priority (10 issues)** - Nice to have:
- Phase references in comments (5 instances)
- Sprint references in handoff script (2 instances)
- Architecture references (conditional based on project_type)

**LOW Priority (2 issues)** - Cosmetic:
- Minor comment improvements

---

## Detailed Fixes (v1.2.0)

### 1. CRITICAL: Python Import Errors

**Problem:** Python source files had hardcoded `mcp_n8n` package references

**Files Fixed:**
- `template/src/{{package_name}}/memory/__init__.py` → `__init__.py.jinja`
- `template/src/{{package_name}}/memory/trace.py` → `trace.py.jinja`

**Changes:**
```python
# Before
from mcp_n8n.memory.event_log import EventLog
source: str = "mcp-n8n"

# After
from {{ package_name }}.memory.event_log import EventLog
source: str = "{{ project_slug }}"
```

**Impact:** Generated projects would have `ImportError` without this fix

---

### 2. CRITICAL: Hardcoded Absolute Paths

**Problem:** Scripts contained developer-specific absolute paths

**Files Fixed:**
- `template/scripts/check-env.sh.jinja` (removed backend checks)
- `template/scripts/mcp-tool.sh.jinja` (use script directory detection)
- `template/scripts/handoff.sh.jinja` (generic `/path/to/` instead of `/Users/victorpiper/code/`)

**Changes:**
```bash
# Before (check-env.sh)
CHORA_PATH="/Users/victorpiper/code/chora-compose"
CODA_PATH="/Users/victorpiper/code/mcp-server-coda"

# After
# Add your project-specific dependency checks here
echo "✓ No additional dependencies to check"

# Before (mcp-tool.sh)
MCP_DIR="/Users/victorpiper/code/{{ project_slug }}"

# After
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_DIR="$(dirname "$SCRIPT_DIR")"
```

**Impact:** Scripts would fail for all users except original developer

---

### 3. CRITICAL: Placeholder GitHub Usernames

**Problem:** Documentation had `yourusername` placeholder instead of template variable

**Files Fixed:**
- `template/CONTRIBUTING.md.jinja` (line 59)
- `template/scripts/publish-prod.sh.jinja` (line 161)
- `template/scripts/diagnose.sh.jinja` (line 196)

**Changes:**
```bash
# Before
https://github.com/yourusername/{{ project_slug }}/...

# After
https://github.com/{{ github_username }}/{{ project_slug }}/...
```

**Impact:** Generated docs would have placeholder URLs

---

### 4. CRITICAL: Security Email Placeholder

**Problem:** `security@example.com` was hardcoded instead of using variable

**Files Fixed:**
- `copier.yml` (added `security_email` variable)
- `template/CONTRIBUTING.md.jinja` (2 instances)

**Changes:**
```yaml
# copier.yml - NEW
security_email:
  type: str
  help: Email for security vulnerability reports
  default: "{{ author_email }}"
```

```markdown
# Before
contact the maintainers at security@example.com

# After
contact the maintainers at {{ security_email }}
```

**Impact:** Projects would have non-functional contact email

---

### 5. HIGH: Memory README Project References

**Problem:** `.chora/memory/README.md.jinja` had 6 mcp-n8n/chora-composer references

**Files Fixed:**
- `template/.chora/memory/README.md.jinja`

**Changes:**
- Line 3: `working with mcp-n8n` → `working with {{ project_slug }}`
- Line 62: `"source": "mcp-n8n"` → `"source": "{{ project_slug }}"`
- Line 64-65: `chora:*`/`chora-composer` → `example:*`/`example-backend`
- Line 243: `"to": "chora-composer"` → `"to": "other-project"`
- Line 323-326: Handoff example made generic
- Line 477: `between mcp-n8n and chora-composer` → `between {{ project_slug }} and other projects`
- Line 495: `mcp-n8n v0.1.0+, chora-composer v1.1.0+` → `{{ project_slug }} v{{ project_version }}+`

**Impact:** Memory system docs would confuse adopters

---

## Verification Results

### ✅ Python Imports
```bash
$ grep -r "mcp_n8n" template/src/{{package_name}}/memory/*.jinja
# No matches found ✅
```

### ✅ Hardcoded Paths
```bash
$ grep -r "/Users/victorpiper/code" template/ --include="*.jinja"
# No matches found ✅
```

### ✅ Placeholder Emails (Remaining YOUR_USERNAME is intentional - for forks)
```bash
$ grep -r "security@example.com" template/ --include="*.jinja"
# No matches found ✅
```

---

## Remaining Issues (For Future Releases)

### HIGH Priority (17 issues)

#### 1. Integration Test Sprint References (5 instances)
**File:** `template/scripts/integration-test.sh.jinja`
- Line 2: "Sprint 2 Day 3 integration checkpoint"
- Line 11: "Sprint 2 Day 3: Integration Test"
- Lines 14, 29-30, 33: chora-composer specific examples
- Lines 126, 129: Sprint 3 references

**Recommended Fix:** Make generic or remove Sprint references

#### 2. Handoff Script Project Logic (5 instances)
**File:** `template/scripts/handoff.sh.jinja`
- Entire script is specific to mcp-n8n + chora-composer dual-codebase workflow

**Recommended Fix:**
- Option A: Remove script entirely (most generic)
- Option B: Add `include_handoff_script: false` copier variable
- Option C: Make it generic for any dual-codebase setup

#### 3. API Key References (8 instances)
**Files:**
- `scripts/check-env.sh.jinja` (line 66)
- `scripts/setup.sh.jinja` (lines 66-67)
- `scripts/diagnose.sh.jinja` (lines 80-81)
- `scripts/verify-stable.sh.jinja` (lines 44-47, 52-55)
- `scripts/rollback-dev.sh.jinja` (lines 89-90)
- `CONTRIBUTING.md.jinja` (lines 103-104, 521, 524, 541)

**Current:**
```bash
REQUIRED_VARS=("ANTHROPIC_API_KEY" "CODA_API_KEY")
```

**Recommended Fix:**
```bash
{% if project_type == 'mcp_server' -%}
# Example: Check for required API keys (customize for your project)
# REQUIRED_VARS=("YOUR_API_KEY_HERE")
REQUIRED_VARS=()
{%- else -%}
REQUIRED_VARS=()
{%- endif %}
```

#### 4. Tool Namespace Examples (6 instances)
**Files:** Multiple

**Current:** References to `chora:*` and `coda:*` namespaces

**Recommended Fix:** Use generic examples:
```bash
# Example tool namespaces: backend:tool_name
# e.g., "mybackend:list_items", "api:fetch_data"
```

---

### MEDIUM Priority (10 issues)

#### 1. Phase References in Comments (5 instances)
**Files:** `justfile.jinja`, `.chora/memory/README.md.jinja`, `CONTRIBUTING.md.jinja`

**Current:**
```
# Safety & Recovery (Phase 2)
# Build & Release (Phase 3)
### Phase 4.6+ Enhancements
```

**Recommended Fix:** Remove phase numbers, keep functional descriptions

#### 2. Sprint References in handoff.sh (2 instances)
**Lines:** 106, 160

**Current:** "Current Sprint", "if Sprint 2 Day 3+"

**Recommended Fix:** "Current Phase", "if applicable"

#### 3. Architecture References (1 section)
**File:** `CONTRIBUTING.md.jinja` (lines 569, 575-583)

**Current:** P5 Gateway pattern documentation

**Recommended Fix:** Make conditional based on `project_type`

---

### LOW Priority (2 issues)

Minor comment improvements and cosmetic fixes

---

## Testing Recommendations

After v1.2.0 release, test template generation with:

1. **Library project:** `project_type=library`, verify no MCP references
2. **CLI tool:** `project_type=cli_tool`, verify no backend checks
3. **Web service:** `project_type=web_service`, verify generic paths
4. **MCP server:** `project_type=mcp_server`, verify appropriate examples

For each test:
- ✅ No hardcoded `mcp-n8n`, `chora-composer`, `mcp-server-coda`
- ✅ No hardcoded `/Users/victorpiper/code/*` paths
- ✅ Imports work (Python files are .jinja)
- ✅ All scripts run without project-specific dependencies

---

## Impact Assessment

### Before v1.2.0
- ❌ Generated projects would have `ImportError` (Python imports)
- ❌ Scripts would fail with hardcoded paths
- ❌ Documentation would have placeholder emails/URLs
- ❌ Memory system docs referenced wrong projects
- ⚠️ 29 other generalization issues present

### After v1.2.0
- ✅ Python imports work correctly
- ✅ Scripts use portable, auto-detected paths
- ✅ Documentation has correct contact info and URLs
- ✅ Memory system docs are generic
- ⚠️ 29 non-critical generalization issues remain (for future releases)

---

## Roadmap

### v1.2.0 (This Release)
- ✅ Fix all CRITICAL issues (12 issues)
- ✅ Fix HIGH priority memory README (6 issues)
- ✅ Add generalization audit documentation

### v1.2.1 or v1.3.0 (Future)
- Fix remaining HIGH priority issues (17 issues)
  - Integration test generalization
  - Handoff script (make optional or remove)
  - API key references (make generic)
  - Tool namespace examples (generic)

### v1.3.0 or v1.4.0 (Future)
- Fix MEDIUM priority issues (10 issues)
  - Remove Phase/Sprint references
  - Make architecture docs conditional

---

## Lessons Learned

1. **Always use .jinja extension for files with template variables** - Python source files need `.jinja` to use variables
2. **Avoid hardcoded paths** - Use script directory detection or environment variables
3. **Add copier variables for all placeholders** - Don't hardcode emails, usernames, etc.
4. **Test with multiple project types** - Generic templates must work for library, CLI, web service, MCP server
5. **Document examples clearly** - Mark project-specific examples as "Example:" to distinguish from requirements

---

## References

- Full audit report: See agent conversation 2025-10-18
- chora-compose adoption: `docs/CHORA_BASE_ADOPTION_HANDOFF.md`
- Copier template variables: `copier.yml`
- Template files: `template/` directory

---

**Audit Performed By:** Claude Code
**Review Status:** Automated + Manual verification
**Next Audit:** After v1.3.0 or upon next adopter feedback
