# Wave 2.0 Phase 1: Test Failure Resolution & Quality Gates

**Status**: Planning
**Created**: 2025-10-31
**Target Completion**: 1 week (4-6 days focused effort)
**Goal**: Fix 37 test failures, achieve 85%+ coverage, release v0.2.0

---

## Current Status (Baseline)

### Test Results
- ✅ **120 tests passing** (61% of 196 total)
- ❌ **37 tests failing** (19%)
- ⏸️ **39 tests skipped** (20% - backward compat environment issues)
- **Pass Rate**: 77% (target: 100%)

### Coverage Analysis
- **Current**: 35.37% overall, 21.80% when running individual tests
- **Target**: ≥85% for new HTTP code
- **Gap**: ~50 percentage points

### Quality Gates Status
| Gate | Status | Target | Current | Gap |
|------|--------|--------|---------|-----|
| **Test Pass Rate** | ❌ | 100% | 77% | -23% |
| **Coverage (HTTP)** | ❌ | ≥85% | ~35% | -50% |
| **Pre-commit Hooks** | ✅ | Pass | 5/7 pass | 2 warnings |
| **Integration Tests** | ❌ | Exists | None | Missing |
| **Smoke Tests** | ❌ | Exists | None | Missing |

---

## Test Failure Categorization

### Category 1: Server Initialization Issues (14 failures) - CRITICAL

**Tests Affected**: All `TestHTTPEndpointExposure` tests
- test_list_clients_endpoint_exists
- test_list_profiles_endpoint_exists
- test_get_config_endpoint_exists
- test_diff_config_endpoint_exists
- test_draft_add_endpoint_exists
- test_draft_remove_endpoint_exists
- test_draft_view_endpoint_exists
- test_draft_clear_endpoint_exists
- test_validate_config_endpoint_exists
- test_publish_config_endpoint_exists
- test_deploy_config_endpoint_exists
- test_list_servers_endpoint_exists
- test_describe_server_endpoint_exists
- test_initialize_keys_endpoint_exists

**Root Cause Hypothesis**:
The HTTP server is not properly exposing endpoints during test execution. Likely issues:
1. MCP tools not being imported/registered correctly in HTTP context
2. FastAPI app routes not being discovered
3. Test setup not initializing server correctly

**Impact**: HIGH - Blocks 14 tests, prevents basic server functionality validation

**Files to Investigate**:
- `src/mcp_orchestrator/http/server.py` (60.61% coverage, many untested lines)
- `tests/http/test_server.py` (test setup)
- `src/mcp_orchestrator/mcp/server.py` (0% coverage - not imported during tests!)

**Estimated Fix Time**: 4-6 hours

---

### Category 2: CORS Configuration (8 failures) - HIGH PRIORITY

**Tests Affected**: CORS-related tests
- test_preflight_request_returns_200
- test_preflight_has_allow_headers_header
- test_authorization_header_is_allowed
- test_content_type_header_is_allowed
- test_x_api_key_header_is_allowed
- test_multiple_headers_are_allowed
- test_authentication_still_required_despite_cors
- test_cors_middleware_is_configured

**Root Cause Hypothesis**:
CORS middleware configuration doesn't match test expectations. Likely issues:
1. TestClient vs actual HTTP client behavior differences
2. CORS headers not being set correctly for OPTIONS requests
3. Allow-Headers configuration incomplete

**Impact**: MEDIUM - Affects browser/web client integration, but doesn't block core functionality

**Files to Investigate**:
- `src/mcp_orchestrator/http/server.py` (CORS middleware setup)
- `tests/http/test_cors.py` (test expectations)

**Estimated Fix Time**: 2-3 hours

---

### Category 3: Token Generation CLI (5 failures) - MEDIUM PRIORITY

**Tests Affected**: CLI integration tests
- test_generate_token_cli_returns_token
- test_generate_token_cli_uses_auth_service
- test_token_uses_secrets_module
- test_token_is_url_safe
- test_token_generation_succeeds_without_server_running

**Root Cause Hypothesis**:
CLI command integration issues. Likely problems:
1. `http_cli/token.py` has 0% coverage - not being tested correctly
2. Import/execution path issues in test environment
3. CLI command not properly wired up

**Impact**: LOW - Affects developer experience for token generation, but API still works

**Files to Investigate**:
- `src/mcp_orchestrator/http_cli/token.py` (0% coverage)
- `tests/http/test_token_generation.py`

**Estimated Fix Time**: 2-3 hours

---

### Category 4: Server Integration (5 failures) - MEDIUM PRIORITY

**Tests Affected**: Integration validation tests
- test_stdio_list_clients_works
- test_http_server_does_not_interfere_with_stdio
- test_list_clients_returns_valid_json
- test_list_servers_returns_valid_json
- test_get_server_details_returns_valid_json
- test_error_handling_returns_valid_json

**Root Cause Hypothesis**:
Related to Category 1 - MCP tools not being properly accessible. Additional issues:
1. stdio transport interference
2. JSON serialization problems
3. Error handling edge cases

**Impact**: MEDIUM - Affects stdio compatibility and error handling

**Estimated Fix Time**: 3-4 hours

---

### Category 5: Workflow Endpoints (3 failures) - LOW PRIORITY

**Tests Affected**: Specific endpoint functionality
- test_validate_config_returns_200
- test_initialize_keys_returns_200_or_400
- test_initialize_keys_creates_keys

**Root Cause Hypothesis**:
Specific endpoint implementation issues, possibly:
1. Missing error handling
2. Incorrect status codes
3. Incomplete functionality

**Impact**: LOW - Specific endpoints affected, not systemic

**Estimated Fix Time**: 1-2 hours

---

### Category 6: Auth Error Messages (1 failure) - TRIVIAL

**Tests Affected**:
- test_invalid_token_error_message

**Root Cause Hypothesis**: Error message format doesn't match test expectation

**Impact**: TRIVIAL - Cosmetic issue

**Estimated Fix Time**: 15 minutes

---

## Phase 1 Execution Plan

### Day 1: Fix Critical Server Initialization (Category 1)

**Goal**: Enable 14 endpoint exposure tests

**Tasks**:
1. **Investigate MCP tool import** (2 hours)
   - Check why `src/mcp_orchestrator/mcp/server.py` has 0% coverage
   - Verify MCP tools are properly imported in HTTP server context
   - Fix import/initialization issues

2. **Fix FastAPI route registration** (2 hours)
   - Ensure all 14 endpoints are properly registered
   - Validate route paths match test expectations
   - Test endpoint discovery mechanism

3. **Update test setup** (1 hour)
   - Fix test initialization if needed
   - Ensure server starts correctly in test environment

4. **Validate fixes** (1 hour)
   - Run `TestHTTPEndpointExposure` test suite
   - Verify all 14 tests pass
   - Check coverage improvement

**Expected Outcome**: 14 failures → 0 failures (+14 passing tests)

---

### Day 2: Fix CORS and Server Integration (Categories 2 & 4)

**Goal**: Enable 13 CORS + integration tests

**Tasks**:
1. **Fix CORS middleware configuration** (2 hours)
   - Review CORS setup in `http/server.py`
   - Align CORS headers with test expectations
   - Handle OPTIONS preflight requests correctly

2. **Fix CORS header allowlist** (1 hour)
   - Add Authorization, Content-Type, X-API-Key to allow-headers
   - Validate multiple headers work
   - Ensure authentication still required despite CORS

3. **Fix stdio compatibility** (2 hours)
   - Investigate stdio transport interference
   - Ensure HTTP server doesn't break stdio mode
   - Fix `test_stdio_list_clients_works`

4. **Fix JSON serialization** (1 hour)
   - Ensure all endpoints return valid JSON
   - Fix error handling JSON responses

**Expected Outcome**: 13 failures → 0 failures (+13 passing tests)

---

### Day 3: Fix CLI and Workflow Endpoints (Categories 3, 5, 6)

**Goal**: Enable remaining 9 failures

**Tasks**:
1. **Fix token generation CLI** (3 hours)
   - Wire up `http_cli/token.py` command
   - Ensure CLI uses auth service correctly
   - Validate token generation without server running

2. **Fix workflow endpoints** (2 hours)
   - Fix `validate_config` endpoint (return 200)
   - Fix `initialize_keys` endpoint (return correct status)
   - Ensure key creation works correctly

3. **Fix auth error message** (15 min)
   - Update error message format to match test

4. **Validate all fixes** (1 hour)
   - Run full HTTP test suite
   - Verify 0 failures, 157 passing (37 failures fixed + 120 already passing)

**Expected Outcome**: 9 failures → 0 failures (+9 passing tests)

**Total passing tests**: 157/196 = 80% (39 still skipped for environment reasons)

---

### Day 4: Coverage & Integration Tests

**Goal**: Achieve ≥85% coverage for HTTP code, add missing tests

**Tasks**:
1. **Run coverage analysis** (30 min)
   ```bash
   pytest tests/http/ --cov=src/mcp_orchestrator/http --cov-report=html --cov-report=term-missing
   ```
   - Identify uncovered lines in HTTP modules
   - Focus on: `http/server.py` (60.61%), `http/endpoints.py`, `http/auth.py`

2. **Write missing unit tests** (3 hours)
   - Cover untested lines in `http/server.py`
   - Cover untested error paths
   - Cover edge cases

3. **Write integration tests** (2 hours)
   - Test: stdio + HTTP both work simultaneously
   - Test: HTTP server startup/shutdown lifecycle
   - Test: End-to-end workflow (draft → validate → publish → deploy)

4. **Write smoke tests** (1 hour)
   - Test: Can discover clients via HTTP
   - Test: Can list servers via HTTP
   - Test: Can build config via HTTP
   - Test: Authentication works via HTTP

**Expected Outcome**: Coverage 35% → ≥85%

---

### Day 5: Performance Testing & Quality Gates

**Goal**: Validate performance, run all quality checks

**Tasks**:
1. **Performance testing** (2 hours)
   - Write benchmark tests for all 14 endpoints
   - Validate p95 < 300ms (target from WAVE_2X_PLAN.md)
   - Optimize slow endpoints if needed

2. **Run quality gates** (1 hour)
   ```bash
   ruff check src/mcp_orchestrator/http tests/http
   mypy src/mcp_orchestrator/http
   pre-commit run --all-files
   ```
   - Fix any ruff violations
   - Fix any mypy type errors
   - Ensure pre-commit hooks pass

3. **Documentation review** (2 hours)
   - Verify user guides accurate
   - Update API documentation if endpoints changed
   - Ensure OpenAPI schema correct

4. **Final validation** (1 hour)
   - Run full test suite: `pytest tests/`
   - Verify HTTP tests: 100% pass rate
   - Verify overall tests: ≥85% coverage, no regressions

**Expected Outcome**: All quality gates pass

---

### Day 6: Release Preparation

**Goal**: Prepare v0.2.0 release

**Tasks**:
1. **Version bump** (30 min)
   - Update `pyproject.toml`: version = "0.2.0"
   - Update `src/mcp_orchestrator/__init__.py`: __version__ = "0.2.0"

2. **Update CHANGELOG.md** (1 hour)
   - Document all Wave 2.0 features
   - List breaking changes (if any)
   - Add migration guide

3. **Build package** (30 min)
   ```bash
   python -m build
   twine check dist/*
   ```

4. **Publish to PyPI** (30 min)
   ```bash
   twine upload dist/*
   ```

5. **Create git tag** (15 min)
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

6. **Update documentation** (1 hour)
   - Update README.md with v0.2.0 features
   - Update installation instructions
   - Announce release (GitHub Discussions, etc.)

**Expected Outcome**: v0.2.0 released to PyPI

---

## Success Criteria

### Must-Have (Blocking Release)
- ✅ All HTTP tests passing (0 failures, 157+ passing)
- ✅ Coverage ≥85% for HTTP code
- ✅ All quality gates pass (ruff, mypy, pre-commit)
- ✅ Integration tests written and passing
- ✅ Performance tests validate p95 < 300ms
- ✅ CHANGELOG.md updated
- ✅ Version bumped to v0.2.0

### Should-Have (Nice to Have)
- ✅ Smoke tests written and passing
- ✅ User documentation reviewed and accurate
- ✅ OpenAPI schema verified
- ✅ No test regressions in non-HTTP tests

### Could-Have (Future Work)
- ⏸️ Fix 39 skipped tests (environment setup issues)
- ⏸️ Docker support (Wave 2.0 optional feature)
- ⏸️ Advanced CORS configuration (Wave 2.1)

---

## Risk Mitigation

### Risk 1: Endpoint Exposure Fix Takes Longer Than Expected
- **Impact**: Delays Day 1, cascades to other days
- **Mitigation**: If >6 hours on Day 1, defer to Day 2
- **Fallback**: Focus on most critical endpoints first (list_clients, list_servers)

### Risk 2: Coverage Gap Requires More Tests Than Estimated
- **Impact**: Day 4 extends into Day 5
- **Mitigation**: Prioritize high-value tests first, defer edge cases if needed
- **Fallback**: Accept 80% coverage for v0.2.0, achieve 85% in v0.2.1

### Risk 3: Performance Tests Reveal Bottlenecks
- **Impact**: Day 5 requires optimization work
- **Mitigation**: Document bottlenecks, create tickets for v0.2.1 optimization
- **Fallback**: Adjust p95 target if 300ms unrealistic for complex endpoints

### Risk 4: Pre-existing Test Regressions
- **Impact**: Non-HTTP tests break during refactoring
- **Mitigation**: Run full test suite daily, catch regressions early
- **Fallback**: Revert breaking changes, defer to separate PR

---

## Dependencies & Blockers

### External Dependencies
- ✅ None - all work is self-contained

### Internal Dependencies
- ✅ chora-base SAP-012 (Development Lifecycle) - adopted
- ✅ chora-base SAP-004 (Testing Framework) - adopted
- ✅ chora-base SAP-006 (Quality Gates) - adopted

### Potential Blockers
- ⚠️ If MCP tool refactoring required (Category 1 fix) - could impact non-HTTP functionality
- ⚠️ If FastAPI/uvicorn incompatibilities discovered - may require library upgrades

---

## Communication Plan

### Daily Standups
- **When**: End of each day
- **Format**: Update TODO list with completed/in-progress items
- **Share**: Test pass rate, coverage %, blockers

### Checkpoints
- **Day 3**: Mid-point review - are we on track for Day 6 release?
- **Day 5**: Final validation - are all quality gates passing?
- **Day 6**: Release decision - Go/NoGo for v0.2.0

### Escalation
- **If >1 day behind schedule**: Re-evaluate scope, consider deferring features to v0.2.1
- **If quality gates not passing by Day 5**: Delay release to Week 2

---

## Post-Release (Day 7+)

### Immediate (Week 2)
1. Monitor PyPI downloads, track adoption
2. Respond to user feedback/issues
3. Begin ecosystem coordination onboarding (Full Onboarding response by Nov 14)

### Short-Term (Week 3-4)
1. Monitor ecosystem-manifest progress via coordination dashboard
2. Review chora-base templates for W3 health patterns
3. Submit coordination requests to 3 teams (clarifying questions)

### Medium-Term (Week 5+)
1. Make W3 Go/NoGo decision based on ecosystem-manifest status
2. If Go: Start W3 Health Monitoring implementation
3. If NoGo: Focus on Wave 2.1 enhancements

---

## Metrics & Tracking

### Daily Metrics
| Day | Tests Passing | Tests Failing | Coverage % | Status |
|-----|---------------|---------------|------------|--------|
| Day 0 (Baseline) | 120 | 37 | 35% | Planning |
| Day 1 (Target) | 134 | 23 | 45% | In Progress |
| Day 2 (Target) | 147 | 10 | 60% | In Progress |
| Day 3 (Target) | 157 | 0 | 70% | In Progress |
| Day 4 (Target) | 170+ | 0 | 85%+ | In Progress |
| Day 5 (Target) | 170+ | 0 | 85%+ | Quality Gates |
| Day 6 (Target) | 170+ | 0 | 85%+ | Release |

### Success Indicators
- ✅ Test pass rate increases daily
- ✅ Coverage increases daily
- ✅ No new regressions introduced
- ✅ All quality gates green by Day 5
- ✅ Release candidate ready by Day 6

---

## Appendix A: Command Reference

### Run HTTP Tests
```bash
# All HTTP tests
pytest tests/http/ -v

# Specific category
pytest tests/http/test_server.py::TestHTTPEndpointExposure -v

# With coverage
pytest tests/http/ --cov=src/mcp_orchestrator/http --cov-report=html

# Fast run (no coverage)
pytest tests/http/ -v --tb=short -q
```

### Quality Gates
```bash
# Lint
ruff check src/mcp_orchestrator/http tests/http

# Type check
mypy src/mcp_orchestrator/http

# Pre-commit
pre-commit run --all-files

# Full validation
pytest tests/ --cov=src/mcp_orchestrator --cov-report=term
```

### Performance Testing
```bash
# Run performance tests
pytest tests/http/test_performance.py -v

# Benchmark specific endpoint
pytest tests/http/test_performance.py::test_list_clients_performance -v
```

### Release Commands
```bash
# Build
python -m build

# Check
twine check dist/*

# Upload (test)
twine upload --repository testpypi dist/*

# Upload (prod)
twine upload dist/*

# Tag
git tag v0.2.0
git push origin v0.2.0
```

---

## Appendix B: SAP-012 Alignment

This plan follows SAP-012 Development Lifecycle phases:

| Phase | Wave 2.0 Status | This Plan |
|-------|----------------|-----------|
| **Phase 1: Vision** | ✅ Complete | Already done (WAVE_2X_PLAN.md) |
| **Phase 2: Planning** | ✅ Complete | This document |
| **Phase 3: Requirements** | ✅ Complete | Already done (API specs) |
| **Phase 4: Development** | ⚠️ 80% | Days 1-3 (TDD RED → GREEN → REFACTOR) |
| **Phase 5: Testing** | ❌ Not Started | Day 4 (Coverage, integration, smoke tests) |
| **Phase 6: Review** | ❌ Not Started | Day 5 (Quality gates, documentation) |
| **Phase 7: Release** | ❌ Not Started | Day 6 (Version bump, PyPI publish) |
| **Phase 8: Monitoring** | 📋 Planned | Post-release (PyPI downloads, feedback) |

**Current Stuck Point**: Phase 4/5 boundary (Development → Testing)

**This Plan**: Unsticks by completing Phase 4 (fix failures), executing Phase 5 (add tests), and delivering through Phase 7 (release)

---

**Document Created**: 2025-10-31
**Owner**: mcp-orchestration team
**Timeline**: 6 days (1 week sprint)
**Success Criteria**: v0.2.0 released with 0 failures, 85%+ coverage, all quality gates passing
