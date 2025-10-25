# Research: n8n API Key Storage and Management

**Status:** 🔴 Active
**Priority:** P0 (Critical)
**Blocks:** E2E testing, consistent configuration
**Context:** [dev-docs/ecosystem/ALIGNMENT.md](../ecosystem/ALIGNMENT.md)
**Assigned:** Victor
**Timeline:** Implement this week
**Created:** 2025-10-22
**Updated:** 2025-10-22 - **Scope Change:** Manual key creation is acceptable, focus on storage

---

## Problem Statement

**Current Blocker:**
E2E tests cannot proceed because we don't have a clear way to store and manage n8n API keys.

**Current State:**
1. E2E tests require running `./tests/e2e/fixtures/n8n/setup_n8n_tests.sh`
2. Setup script requires `N8N_API_KEY` environment variable
3. API key is manually created via n8n UI (http://localhost:5678)
4. **Problem:** No documented way to store the key for reuse across:
   - Multiple terminal sessions
   - E2E test runs
   - Gateway startup
   - Different environments (dev, test)

**Acceptable Workflow:**
- User manually creates API key via n8n UI (one-time setup per environment)
- Key is **stored securely** for reuse
- Key is **automatically available** to scripts, tests, gateway

**Desired State:**
- Clear documentation: "Create API key in n8n UI, store it in X"
- API key persists across terminal sessions, system restarts
- E2E tests can run without re-entering the key each time
- Different environments (dev, test) can have different keys

**Impact:**
- **Blocks E2E testing** - No persistent storage for test API key
- **Reduces UX** - Need to manually export `N8N_API_KEY` every terminal session
- **Confusing for friends** - Unclear where/how to store the key

---

## Research Questions

### Q1: n8n API/CLI for API Key Creation

**Question:** Does n8n provide a programmatic interface for API key management?

**Sub-questions:**
1. Is there a REST API endpoint for creating API keys?
   - Check n8n API documentation (https://docs.n8n.io/api/)
   - Inspect n8n source code (GitHub: n8n-io/n8n)
   - Test API endpoints with curl/Postman

2. Does n8n provide a CLI command for key generation?
   - Check `n8n --help` output
   - Review n8n CLI documentation
   - Look for `n8n api-key create` or similar

3. Is there an internal SDK/library we can call from init script?
   - Review n8n source code architecture
   - Identify API key generation logic
   - Check if it's callable from Node.js script

**Research Method:**
1. Read n8n official documentation
2. Search n8n GitHub issues for "api key automation"
3. Review n8n source code (`packages/cli/src/` likely location)
4. Test documented approaches with local n8n instance

**Expected Outcome:**
- Document any official n8n API/CLI for key management
- If exists: Test and validate it works
- If not exists: Document why and explore alternatives

---

### Q2: Environment Variable Pre-Configuration

**Question:** Can API keys be pre-seeded via Docker environment variables or configuration files?

**Sub-questions:**
1. Does n8n honor `N8N_API_KEY` environment variable on startup?
   - Test with docker-compose.test.yml
   - Check if pre-seeding the env var bypasses UI creation

2. Is there a configuration file where API keys can be pre-populated?
   - Check n8n config file locations (`~/.n8n/config`)
   - Review n8n config schema
   - Test manual config modification

3. What is the format/structure of API keys?
   - Length, character set, encoding?
   - Is it a simple string or JWT/signed token?
   - Can we generate valid keys externally?

**Research Method:**
1. Review n8n Docker image entrypoint script
2. Check n8n environment variable documentation
3. Inspect n8n configuration file format
4. Test with custom environment variables

**Expected Outcome:**
- Document if env var pre-seeding is supported
- If yes: Provide working docker-compose example
- If no: Document why and explore alternatives

---

### Q3: Internal Database Injection

**Question:** Can we inject API keys directly into n8n's database during container initialization?

**Sub-questions:**
1. What is n8n's database schema for API keys?
   - Database type (SQLite, PostgreSQL, MySQL)?
   - Table name, column names, constraints?
   - Encryption/hashing applied to keys?

2. Where is the n8n database located?
   - Docker volume mount path?
   - File path inside container?
   - Accessible during init script execution?

3. Is there a safe injection approach?
   - Init script that runs before n8n starts?
   - SQL INSERT statement to add key?
   - Idempotent (safe to run multiple times)?

4. What risks/trade-offs exist?
   - Database schema changes in n8n updates?
   - Key format requirements (hash, salt, etc.)?
   - n8n integrity checks that might fail?

**Research Method:**
1. Inspect n8n Docker volume (`docker volume inspect n8n_data`)
2. Examine database file/schema (SQLite browser, psql)
3. Review n8n migration files (GitHub: n8n-io/n8n migrations)
4. Test manual key insertion with stopped n8n container

**Expected Outcome:**
- Document n8n database schema for API keys
- If safe injection exists: Provide init script example
- If risky: Document risks and recommend against

---

### Q4: n8n Recommended Approach

**Question:** What is n8n's documented approach for automated/headless deployments?

**Sub-questions:**
1. Does n8n official documentation cover automation?
   - Deployment guides for CI/CD?
   - Docker best practices?
   - Headless/automated setup instructions?

2. Have others solved this problem?
   - GitHub issues discussing automation?
   - Community forum discussions?
   - Stack Overflow questions?
   - Blog posts about n8n automation?

3. Is there an "official" workaround?
   - Environment variables for initial setup?
   - Pre-configured Docker images?
   - Initialization webhooks/callbacks?

**Research Method:**
1. Search n8n documentation for "automation", "headless", "CI/CD", "API key"
2. Search GitHub issues: `repo:n8n-io/n8n api key automation`
3. Search n8n community forum: https://community.n8n.io
4. Search Stack Overflow: `[n8n] api key automation`

**Expected Outcome:**
- Document official n8n recommendation (if exists)
- Compile community workarounds and evaluate
- Identify best practice for our use case

---

### Q5: Security Implications

**Question:** How do we generate unique, secure API keys per installation while maintaining adequate security?

**Sub-questions:**
1. What are the security requirements for API keys?
   - Minimum length, entropy?
   - Character set (alphanumeric, symbols)?
   - Collision resistance needed?

2. How do we generate keys securely?
   - Python `secrets` module?
   - OpenSSL random generation?
   - UUID vs. random bytes vs. hash-based?

3. Where/how do we store generated keys?
   - Plain text in `.env` file (adequate for laptop security)?
   - Encrypted at rest (overkill for local dev)?
   - Docker secrets (better for cloud deployment)?

4. What's the threat model for local deployment?
   - Local laptop compromise (physical access)?
   - Network-based attacks (localhost only)?
   - Malicious processes on same machine?

5. What's the migration path to cloud security?
   - How do we upgrade from `.env` to secrets manager?
   - When do we require key rotation?
   - Can we design for future hardening now?

**Research Method:**
1. Review n8n API key security documentation
2. Check n8n source code for key generation logic
3. Research Python best practices for API key generation
4. Consult ecosystem-intent.md security baseline (Part 7)

**Expected Outcome:**
- Document minimum security requirements for local deployment
- Provide secure key generation approach (Python code)
- Document storage strategy (`.env` vs. secrets manager)
- Plan migration path to cloud security tiers

---

## Success Criteria

✅ **Automated E2E Tests**
```bash
just e2e-all  # No manual intervention required
```

✅ **Unique API Key Per Installation**
- Each `docker-compose up` generates fresh API key
- Or: Installer generates key during first-run setup
- No shared/hardcoded keys across installations

✅ **Secure Enough for Local Development**
- API key entropy adequate (128+ bits recommended)
- Generated using cryptographically secure random (Python `secrets`)
- Stored securely for local threat model (`.env` with proper permissions)

✅ **Cloud Migration Path Exists**
- Design supports future upgrade to secrets manager
- Documentation explains how to harden for production
- No architectural decisions that block cloud security

✅ **Documented and Tested**
- Research findings document explains chosen approach
- Prototype implementation works in docker-compose.test.yml
- E2E tests pass end-to-end
- Documentation updated (platform-operations.md, E2E test guide)

---

## Deliverables

### 1. Research Findings Document

**Filename:** `dev-docs/research/n8n-api-key-bootstrap-findings.md`

**Content:**
- Answers to Q1-Q5 (research questions)
- Pros/cons of each approach discovered
- Recommendation with rationale
- Security analysis and threat modeling
- Implementation complexity comparison

**Format:**
```markdown
# n8n API Key Bootstrap: Research Findings

## Executive Summary
[Recommended approach with 1-paragraph rationale]

## Q1: n8n API/CLI Findings
[Detailed findings...]

## Q2: Environment Variable Findings
[...]

## Q3: Database Injection Findings
[...]

## Q4: n8n Official Approach
[...]

## Q5: Security Analysis
[...]

## Recommendation
[Chosen approach with full justification]

## Risks and Mitigations
[...]

## Implementation Plan
[High-level steps]
```

### 2. Prototype Implementation

**Deliverable:** Working code demonstrating chosen approach

**Possible Approaches** (choose based on research):

**Approach A: Dockerfile with Init Script**
```dockerfile
# Dockerfile.n8n-test
FROM n8nio/n8n:latest
COPY init-api-key.sh /docker-entrypoint-init.d/
RUN chmod +x /docker-entrypoint-init.d/init-api-key.sh
```

**Approach B: docker-compose.test.yml with Environment Config**
```yaml
services:
  n8n-test:
    image: n8nio/n8n:latest
    environment:
      - N8N_API_KEY=${N8N_API_KEY:-$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")}
```

**Approach C: Custom Entrypoint Script**
```bash
#!/bin/bash
# entrypoint-with-api-key.sh
if [ -z "$N8N_API_KEY" ]; then
  export N8N_API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
  echo "N8N_API_KEY=${N8N_API_KEY}" >> /app/.env
fi
exec /docker-entrypoint.sh "$@"
```

**Selection Criteria:**
- Least complexity (prefer simple over clever)
- Most maintainable (survives n8n version upgrades)
- Best security (adequate for local, upgradeable for cloud)
- Docker-friendly (works in docker-compose)

### 3. Integration

**Files to Update:**

**docker-compose.test.yml**
- Implement chosen approach for n8n-test service
- Ensure API key available to mcp-gateway service
- Document in comments how it works

**tests/e2e/fixtures/n8n/setup_n8n_tests.sh**
- Remove manual "Please create API key" instructions
- Auto-detect or generate N8N_API_KEY if missing
- Update prerequisites section

**docs/how-to/platform-operations.md**
- Add "n8n API Key Management" section
- Explain automated bootstrap for local/test
- Document manual creation for production (if different)

**tests/e2e/E2E_N8N_INTEGRATION.md**
- Update prerequisites (no manual UI step)
- Explain API key auto-generation
- Update success criteria

### 4. Testing

**Test Plan:**

**Test 1: Fresh Environment**
```bash
docker-compose -f docker-compose.test.yml down -v  # Clean slate
just e2e-all  # Should complete without manual intervention
```

**Test 2: Unique Keys Per Environment**
```bash
just e2e-down && just e2e-up  # First run
echo $N8N_API_KEY_1 > /tmp/key1.txt
just e2e-down && just e2e-up  # Second run
echo $N8N_API_KEY_2 > /tmp/key2.txt
diff /tmp/key1.txt /tmp/key2.txt  # Should differ
```

**Test 3: E2E Tests Pass**
```bash
just e2e-test  # All 18 automated tests should pass
```

**Test 4: Key Security**
```bash
python3 << EOF
import sys
key = open('.env').read().split('N8N_API_KEY=')[1].split()[0]
assert len(key) >= 32, "Key too short"
assert key.isalnum() or '-' in key or '_' in key, "Unexpected characters"
print(f"✓ Key length: {len(key)} characters")
print(f"✓ Key format valid")
EOF
```

---

## Timeline

### Week 1: Research (Nov 4-8, 2025)

**Monday-Tuesday (Q1-Q3):**
- Research n8n API/CLI capabilities
- Test environment variable pre-configuration
- Explore database injection approach
- **Deliverable:** Draft findings for Q1-Q3

**Wednesday (Q4-Q5):**
- Search n8n documentation and community
- Security analysis and key generation research
- **Deliverable:** Complete findings document

**Thursday:**
- Evaluate all approaches (pros/cons)
- Make recommendation with rationale
- Draft implementation plan
- **Deliverable:** Finalized findings document

**Friday:**
- Review findings with stakeholder (Victor)
- Adjust based on feedback
- Prepare for implementation week

### Week 2: Implementation (Nov 11-15, 2025)

**Monday-Tuesday:**
- Implement prototype based on chosen approach
- Test in isolated environment
- Iterate until working

**Wednesday:**
- Integrate into docker-compose.test.yml
- Update setup_n8n_tests.sh script
- Test `just e2e-all` end-to-end

**Thursday:**
- Update documentation (platform-ops, E2E guide)
- Run full test suite
- Address any failures

**Friday:**
- Create PR with all changes
- Code review
- Merge to main

---

## Context

This research task is part of the **Phase 2: Friend Distribution** effort documented in [dev-docs/ecosystem/ALIGNMENT.md](../ecosystem/ALIGNMENT.md#phase-2-friend-distribution-months-1-3).

**Architectural Context:**
- mcp-n8n operates as a **peer-to-peer ecosystem node**
- Each installation must be **autonomous** (works offline)
- Security posture: **Progressive hardening** (laptop security → cloud hardening)
- Installer must be **beginner-friendly** (no manual configuration)

**Related Work:**
- **E2E Test Suite:** [tests/e2e/E2E_N8N_INTEGRATION.md](../../tests/e2e/E2E_N8N_INTEGRATION.md)
- **Platform Operations:** [docs/how-to/platform-operations.md](../../docs/how-to/platform-operations.md)
- **Sprint 7 Completion:** [docs/sprints/SPRINT_7_COMPLETION_SUMMARY.md](../../docs/sprints/SPRINT_7_COMPLETION_SUMMARY.md)
- **n8n Backend Implementation:** [src/mcp_n8n/backends/n8n_backend.py](../../src/mcp_n8n/backends/n8n_backend.py)

**Dependencies:**
- Blocks: E2E testing automation (highest priority)
- Blocks: CI/CD in GitHub Actions
- Blocks: Friend distribution (Phase 2)
- Enables: Automated installer development

---

## Notes

**Assumptions:**
1. n8n runs in Docker container (n8nio/n8n:latest)
2. Local deployment threat model = personal laptop security
3. Friends will use same Docker-based deployment
4. Future cloud deployment will require security hardening

**Constraints:**
1. Must work with current n8n version (latest stable)
2. Should survive n8n version upgrades (avoid brittle hacks)
3. Must not compromise n8n functionality
4. Should be documented well enough for friends to understand

**Open Questions:**
- Does n8n have plans for official automation support? (Check roadmap/issues)
- Are there security implications we're missing? (Consult n8n security docs)
- Will this approach work for cloud deployment? (Design for migration)

---

**Status:** 🔴 Active - Research starting this week
**Next Review:** After research findings document complete
**Last Updated:** 2025-10-22
