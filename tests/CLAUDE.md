# Claude Test Generation Patterns - mcp-orchestration

**Purpose:** Claude-specific patterns for test generation and coverage optimization in mcp-orchestration.

**Parent:** See [../CLAUDE.md](../CLAUDE.md) for project-level Claude guidance and [AGENTS.md](AGENTS.md) for generic testing guide.

---

## Claude's Testing Strengths

Claude excels at mcp-orchestration test generation because:

- **Comprehensive edge case identification** - Cryptographic edge cases, signature validation scenarios
- **Pattern recognition** - Follows project test patterns (storage, crypto, registry)
- **Fixture generation** - Creates appropriate mocks for MCP tools, storage, signers
- **Documentation** - Writes clear test docstrings explaining cryptographic scenarios
- **Coverage optimization** - Targets untested code paths in storage/crypto layers

---

## mcp-orchestration Test Generation Template

### Complete Test Request Pattern

```markdown
# Test Generation Request - mcp-orchestration

## Code to Test
[Paste function/class/module from src/mcp_orchestrator/]

## Testing Requirements

**Coverage target:** 85%
**Framework:** pytest (with pytest-asyncio)
**Patterns:** Follow tests/conftest.py fixtures

### Test Categories
1. ✅ Happy path (valid configs, successful signatures)
2. ✅ Edge cases (empty configs, missing fields, boundary SHA-256 hashes)
3. ✅ Error conditions (invalid signatures, missing artifacts, bad client names)
4. ✅ Integration (MCP tool → storage → crypto flows)

### Specific Scenarios
- Valid Ed25519 signature verification
- Content-addressable storage retrieval with SHA-256
- MCP tool error handling for missing configs
- Multi-client registry lookups (claude-desktop, cursor)

### Mocking Strategy
Mock these external dependencies:
- Storage layer: Use storage fixture from conftest.py
- Crypto layer: Use signer fixture with test keypair
- Telemetry: Use mock_emitter fixture
- File I/O: Use tmp_path fixture

## Example Test Structure
```python
def test_get_config_with_valid_hash(storage, sample_artifact):
    """Test get_config retrieves and verifies signed artifact.

    Verifies:
    - Artifact retrieved from content-addressable storage
    - Ed25519 signature verified successfully
    - Configuration returned in expected format
    """
    # Arrange
    artifact_hash = sample_artifact.hash
    expected_config = sample_artifact.config

    # Act
    result = get_config("claude-desktop", artifact_hash)

    # Assert
    assert result["status"] == "success"
    assert result["config"] == expected_config
    assert result["signature_valid"] is True
```

---

Claude, generate tests following this pattern:
1. Use pytest fixtures from tests/conftest.py (storage, signer, sample_artifact)
2. Parametrize multiple scenarios where appropriate
3. Clear arrange-act-assert structure
4. Descriptive docstrings explaining cryptographic behavior
5. Target 85% coverage
6. Test both sync and async MCP tools
```

---

## Fixture Pattern Recognition

### Key Fixtures in tests/conftest.py

```python
# Storage fixtures
@pytest.fixture
def storage(tmp_path):
    """Content-addressable storage for testing."""
    return ContentAddressableStorage(tmp_path / "storage")

@pytest.fixture
def signer(tmp_path):
    """Ed25519 signer with test keypair."""
    key_path = tmp_path / "test_key"
    return Signer(key_path)

@pytest.fixture
def sample_artifact(storage, signer):
    """Complete signed artifact for testing."""
    config = {"mcpServers": {"test": {"command": "test"}}}
    artifact_hash = storage.store(json.dumps(config))
    signature = signer.sign(artifact_hash.encode())
    return SignedArtifact(hash=artifact_hash, config=config, signature=signature)

@pytest.fixture
def mock_emitter(monkeypatch):
    """Mock telemetry emitter."""
    emitter = Mock()
    monkeypatch.setattr("mcp_orchestrator.telemetry.get_emitter", lambda: emitter)
    return emitter
```

### Claude-Optimized Fixture Requests

**Pattern 1: Use Existing Fixtures**

```markdown
"Generate tests for add_server_to_config tool using:
- storage fixture (content-addressable storage)
- sample_artifact fixture (signed config)
- mock_emitter fixture (telemetry tracking)

Test scenarios:
1. Add server to empty config
2. Add server to existing config with other servers
3. Reject duplicate server name
4. Validate MCP server schema"
```

---

## Parametrized Test Pattern

### Cryptographic Scenarios

```python
@pytest.mark.parametrize("hash_value,should_exist", [
    ("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", True),  # Valid SHA-256
    ("invalid-hash", False),  # Invalid format
    ("a" * 64, False),  # Valid format but doesn't exist
])
def test_storage_retrieve_scenarios(storage, hash_value, should_exist):
    """Test content-addressable storage retrieval with various hashes."""
    if should_exist:
        storage.store("test content")
        result = storage.retrieve(hash_value)
        assert result is not None
    else:
        with pytest.raises(ArtifactNotFoundError):
            storage.retrieve(hash_value)
```

### Multi-Client Scenarios

```python
@pytest.mark.parametrize("client,config_key", [
    ("claude-desktop", "mcpServers"),
    ("cursor", "mcp_servers"),
])
def test_client_config_formats(client, config_key):
    """Test config format varies by client type."""
    config = get_client_config_template(client)
    assert config_key in config
```

---

## Coverage Optimization with Claude

### Target Specific Layers

```markdown
"Current test coverage for mcp_orchestrator/crypto/signing.py: 78%

Uncovered lines: 45-52, 67-70

Generate tests to cover:
1. Lines 45-52: Ed25519 signature verification with invalid public key
2. Lines 67-70: Signer initialization with missing key file

Follow pattern in tests/test_crypto.py"
```

### Cryptographic Edge Cases

```python
def test_signature_verification_with_tampered_hash():
    """Test Ed25519 verification detects tampered artifact hash.

    This covers the critical security path where a valid signature
    is presented but the artifact hash has been modified.
    """
    # Arrange
    signer = Signer(test_key_path)
    original_hash = "abc123"
    tampered_hash = "xyz789"
    signature = signer.sign(original_hash.encode())

    # Act & Assert
    is_valid = signer.verify(tampered_hash.encode(), signature, signer.public_key)
    assert is_valid is False  # Must detect tampering
```

---

## Integration Test Patterns

### MCP Tool End-to-End Tests

```markdown
"Generate integration test for get_config MCP tool:

Full workflow:
1. MCP tool receives get_config request with client and hash
2. Retrieves artifact from content-addressable storage (SHA-256 lookup)
3. Verifies Ed25519 signature
4. Emits telemetry event
5. Returns config to caller

Mock only external I/O (file system via storage fixture).
Test real crypto verification logic."
```

### Pattern for MCP Tools

```python
@pytest.mark.asyncio
async def test_get_config_integration(storage, signer, mock_emitter):
    """Test get_config tool end-to-end workflow.

    Verifies:
    - Tool accepts MCP protocol request
    - Retrieves from content-addressable storage
    - Verifies Ed25519 signature
    - Emits telemetry event
    - Returns valid MCP response
    """
    # Arrange
    config = {"mcpServers": {"test": {"command": "test"}}}
    artifact_hash = storage.store(json.dumps(config))
    signature = signer.sign(artifact_hash.encode())

    # Store signed artifact
    storage.store_signed(artifact_hash, config, signature, signer.public_key)

    # Act
    result = await mcp.call_tool("get_config", {
        "client": "claude-desktop",
        "artifact_hash": artifact_hash
    })

    # Assert
    assert result["status"] == "success"
    assert result["config"] == config
    assert result["signature_valid"] is True
    mock_emitter.emit.assert_called_with(
        "config.retrieved",
        client="claude-desktop",
        hash=artifact_hash
    )
```

---

## Async Test Patterns for MCP Tools

### Claude Async Test Generation

```markdown
"Generate async tests for check_for_updates MCP tool:

Use pytest-asyncio
Test async/await patterns
Tool performs async diff comparison
Returns async MCP response"
```

### Expected Async Pattern

```python
import pytest

@pytest.mark.asyncio
async def test_check_for_updates_async():
    """Test check_for_updates async MCP tool."""
    # Arrange
    current_hash = "abc123"
    latest_hash = "def456"

    # Act
    result = await mcp.call_tool("check_for_updates", {
        "client": "claude-desktop",
        "current_hash": current_hash
    })

    # Assert
    assert result["status"] == "success"
    assert "updates_available" in result
    assert "diff" in result if result["updates_available"] else True
```

---

## Error Testing Patterns

### Cryptographic Error Scenarios

```markdown
"Generate tests for signature verification errors:

Error scenarios:
1. Invalid signature format → SignatureError
2. Mismatched public key → VerificationError
3. Tampered artifact hash → VerificationError
4. Empty signature → ValueError

Use pytest.raises with match for error messages."
```

### Claude Error Test Pattern

```python
def test_verify_signature_raises_on_invalid_format():
    """Test that verify raises SignatureError for malformed signature."""
    signer = Signer(test_key_path)
    invalid_signature = b"not-a-valid-signature"

    with pytest.raises(SignatureError, match="Invalid signature format"):
        signer.verify(b"data", invalid_signature, signer.public_key)

def test_storage_retrieve_raises_on_missing_artifact():
    """Test that retrieve raises ArtifactNotFoundError for unknown hash."""
    storage = ContentAddressableStorage(tmp_path)

    with pytest.raises(ArtifactNotFoundError, match="Artifact .* not found"):
        storage.retrieve("nonexistent-hash")
```

---

## Test-Driven Development with Claude

### TDD Workflow for mcp-orchestration Features

```markdown
# TDD Workflow - Add New MCP Tool

## Step 1: Write Failing Test
"Write failing test for new MCP tool 'deploy_config':

Should:
- Input: client name, config draft
- Output: success status, deployed hash, signature
- Error if: invalid client, malformed config
- Emit telemetry: 'config.deployed' event

Don't implement the tool yet, just the test."

## Step 2: Implement to Pass
"Now implement deploy_config tool in src/mcp_orchestrator/mcp/server.py:
- Minimal implementation to make test pass
- Store config in content-addressable storage
- Sign with Ed25519
- Return hash and signature"

## Step 3: Refactor
"Refactor deploy_config to extract common logic:
- Use shared storage client
- Use shared signer instance
- All tests must still pass"

## Step 4: Add Edge Cases
"Add tests for edge cases:
- Duplicate config (same content hash)
- Very large config (>1MB)
- Invalid MCP server schema

Then update implementation to handle them."
```

---

## Common Test Patterns in mcp-orchestration

### Pattern 1: Content-Addressable Storage Tests

```python
def test_storage_sha256_hashing():
    """Test storage generates correct SHA-256 content hash."""
    storage = ContentAddressableStorage(tmp_path)
    content = '{"test": "data"}'

    hash_result = storage.store(content)

    # Verify SHA-256 format (64 hex characters)
    assert len(hash_result) == 64
    assert all(c in "0123456789abcdef" for c in hash_result)

    # Verify same content yields same hash (content-addressable property)
    hash_result2 = storage.store(content)
    assert hash_result == hash_result2
```

### Pattern 2: Ed25519 Signature Tests

```python
def test_ed25519_signature_round_trip():
    """Test Ed25519 signing and verification round trip."""
    signer = Signer(test_key_path)
    data = b"artifact-hash-to-sign"

    # Sign
    signature = signer.sign(data)

    # Verify with correct public key
    is_valid = signer.verify(data, signature, signer.public_key)
    assert is_valid is True

    # Verify fails with wrong public key
    other_signer = Signer(other_key_path)
    is_valid_wrong_key = signer.verify(data, signature, other_signer.public_key)
    assert is_valid_wrong_key is False
```

### Pattern 3: Registry Multi-Client Tests

```python
@pytest.mark.parametrize("client,expected_profile_path", [
    ("claude-desktop", Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"),
    ("cursor", Path.home() / ".cursor/config.json"),
])
def test_registry_client_profile_paths(client, expected_profile_path):
    """Test registry returns correct profile path for each client."""
    registry = ClientRegistry()
    profile = registry.get_profile(client)

    assert profile.config_path == expected_profile_path
```

---

## Metrics Tracking for Tests

### Test Quality Metrics for mcp-orchestration

```python
# Track test quality in checkpoints
"""
Test Metrics - Wave 1.5:
- Coverage: 87.3% (target 85% ✅)
- Tests added: 23
  - Storage layer: 8
  - Crypto layer: 7
  - MCP tools: 6
  - Registry: 2
- Edge cases: 12
- Error paths: 8
- Integration tests: 3

Quality:
- All tests pass ✅
- No flaky tests ✅
- Clear docstrings ✅
- Appropriate mocks ✅
- Cryptographic scenarios covered ✅
"""
```

---

## Best Practices for mcp-orchestration Tests

### ✅ Do's

1. **Test cryptographic edge cases** - Invalid signatures, tampered hashes, wrong keys
2. **Use content-addressable fixtures** - Leverage storage and signer fixtures
3. **Test multi-client scenarios** - claude-desktop, cursor have different formats
4. **Mock telemetry** - Use mock_emitter to verify event emission
5. **Test MCP protocol compliance** - Verify tool input/output schemas
6. **Document security implications** - Explain why signature verification tests matter

### ❌ Don'ts

1. **Don't skip signature verification tests** - Security critical
2. **Don't ignore storage hash collisions** - Test content-addressable properties
3. **Don't forget async patterns** - Many MCP tools are async
4. **Don't mock crypto primitives** - Test real Ed25519 verification
5. **Don't skip telemetry verification** - Events used for monitoring

---

## Troubleshooting mcp-orchestration Tests

### Problem: Cryptographic Tests Failing

**Solution:** Verify key generation

```markdown
"Ed25519 signature tests failing with VerificationError.

Debug:
1. Check test keypair generation in conftest.py
2. Verify public key derivation from private key
3. Test with known good Ed25519 test vectors

Show me the signer fixture and verification test."
```

### Problem: Storage Tests Intermittent

**Solution:** Use isolated tmp_path

```markdown
"Storage tests occasionally fail with FileNotFoundError.

Issue: Tests sharing storage directory causing conflicts.

Fix: Ensure each test uses isolated tmp_path:
```python
@pytest.fixture
def isolated_storage(tmp_path):
    \"\"\"Isolated storage for each test.\"\"\"
    return ContentAddressableStorage(tmp_path / f\"storage-{uuid.uuid4()}\")
```
```

---

**See Also:**
- [../CLAUDE.md](../CLAUDE.md) - Project-level Claude patterns for mcp-orchestration
- [AGENTS.md](AGENTS.md) - Generic testing guide with project conventions
- [../claude/FRAMEWORK_TEMPLATES.md](../claude/FRAMEWORK_TEMPLATES.md) - Test generation template library

---

**Version:** 3.3.0 (chora-base)
**Project:** mcp-orchestration v0.1.5
**Last Updated:** 2025-10-25
