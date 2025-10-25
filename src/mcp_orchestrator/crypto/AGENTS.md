# Cryptographic Operations Guide

**Purpose:** Guide for cryptographic operations (Ed25519 signing/verification).

**Parent:** See [../AGENTS.md](../AGENTS.md) for core orchestrator overview.

---

## Quick Reference

- **Key generation:** `mcp-orchestration init-configs` or `crypto.generate_keypair()`
- **Sign artifact:** `crypto.sign_artifact(payload, private_key)`
- **Verify signature:** `crypto.verify_signature(artifact, signature, public_key)`
- **Testing:** `pytest tests/unit/test_crypto.py -v` (100% coverage required)

---

## Architecture

**Path:** `src/mcp_orchestrator/crypto/`

**Cryptographic Scheme:** Ed25519 (RFC 8032)

**Why Ed25519?**
- **Fast:** ~100K signatures/sec, ~40K verifications/sec (pure Python)
- **Secure:** 128-bit security level, no timing attacks
- **Small:** 32-byte public keys, 64-byte signatures
- **Simple:** No parameters, no complexity, no side channels

### Files

```
crypto/
├── __init__.py           # Public API exports
├── signing.py            # Sign/verify operations
├── keys.py               # Key generation, storage, loading
└── validation.py         # Signature validation logic
```

---

## Key Management

### Storage Location

**Default:** `~/.mcp-orchestration/keys/`

**Files:**
- `signing.key` - Ed25519 private key (32 bytes, 0600 permissions)
- `signing.pub` - Ed25519 public key (32 bytes, 0644 permissions)

**Custom Path:** Set `MCP_ORCHESTRATION_KEY_PATH` environment variable

### Key Generation

**Via CLI (Recommended):**
```bash
# Generates keypair during initialization
mcp-orchestration init-configs

# Regenerate keys (WARNING: invalidates all existing signatures)
mcp-orchestration init-configs --regenerate-keys
```

**Programmatically:**
```python
from mcp_orchestrator.crypto import generate_keypair, save_keypair

# Generate
private_key, public_key = generate_keypair()

# Save to default location
save_keypair(private_key, public_key)

# Or custom path
save_keypair(private_key, public_key, key_dir="/custom/path")
```

### Loading Keys

```python
from mcp_orchestrator.crypto import load_keypair

# Load from default location
private_key, public_key = load_keypair()

# Or custom path
private_key, public_key = load_keypair(key_dir="/custom/path")
```

---

## Security Constraints

**CRITICAL RULES:**

❌ **NEVER:**
- Commit private keys to git (`.gitignore` must include `*.key`)
- Log private keys (even in debug mode)
- Send private keys over network (no remote signing)
- Store private keys with permissive permissions (must be 0600)
- Share private keys between environments (each env has its own keypair)

✅ **ALWAYS:**
- Store private keys with permissions 0600 (Unix) or equivalent (Windows)
- Use environment variable for custom key paths (avoid hardcoding)
- Verify signatures before trusting artifacts
- Use constant-time comparison to prevent timing attacks
- Log security events (key generation, signature verification failures)

---

## Signing Operations

### Sign Artifact

```python
from mcp_orchestrator.crypto import sign_artifact, load_keypair

# Load private key
private_key, _ = load_keypair()

# Artifact to sign
artifact = {
    "artifact_id": "aabbccddee...",  # SHA-256 of payload
    "client_id": "claude-desktop",
    "profile": "default",
    "payload": {
        "mcpServers": {...}
    },
    "metadata": {
        "created_at": "2025-10-24T12:00:00Z"
    }
}

# Sign
signature = sign_artifact(artifact, private_key)

# Signature structure
# {
#   "algorithm": "ed25519",
#   "value": "<base64-encoded 64-byte signature>",
#   "timestamp": "2025-10-24T12:00:00Z",
#   "signer": {
#     "public_key": "<base64-encoded 32-byte public key>",
#     "key_id": "optional-key-identifier"
#   }
# }
```

### Verify Signature

```python
from mcp_orchestrator.crypto import verify_signature, load_keypair

# Load public key
_, public_key = load_keypair()

# Artifact with signature
artifact_with_signature = {
    "artifact_id": "aabbccddee...",
    "payload": {...},
    "signature": {
        "algorithm": "ed25519",
        "value": "base64-signature...",
        ...
    }
}

# Verify
is_valid = verify_signature(artifact_with_signature, public_key)

if not is_valid:
    raise SecurityError("Signature verification failed - artifact tampered!")

# If valid, artifact is authentic and unmodified
```

---

## Signature Formats

### Detached Signature (Separate from Payload)

**Use case:** External signature file

```json
{
  "algorithm": "ed25519",
  "value": "base64-encoded-signature...",
  "timestamp": "2025-10-24T12:00:00Z",
  "signer": {
    "public_key": "base64-encoded-public-key...",
    "key_id": "optional-identifier"
  }
}
```

### Embedded Signature (Included in Artifact)

**Use case:** Self-contained artifact (mcp-orchestration default)

```json
{
  "artifact_id": "aabbccddee...",
  "client_id": "claude-desktop",
  "payload": {
    "mcpServers": {...}
  },
  "signature": {
    "algorithm": "ed25519",
    "value": "base64-signature...",
    "timestamp": "2025-10-24T12:00:00Z",
    "signer": {
      "public_key": "base64-public-key..."
    }
  }
}
```

---

## Common Tasks

### Generate New Keypair

```bash
# Via CLI
mcp-orchestration init-configs --regenerate-keys

# Via Python
python -c "
from mcp_orchestrator.crypto import generate_keypair, save_keypair
private, public = generate_keypair()
save_keypair(private, public)
print('Keypair generated at ~/.mcp-orchestration/keys/')
"
```

### Rotate Keys

**WARNING:** Rotating keys invalidates all existing signatures.

**Process:**
1. Generate new keypair
2. Re-sign all artifacts with new key
3. Update public key distribution
4. Deprecate old key (grace period for verification)

```python
from mcp_orchestrator.crypto import generate_keypair, save_keypair
from mcp_orchestrator.storage import list_artifacts, get_artifact, save_artifact
from mcp_orchestrator.crypto import sign_artifact

# 1. Generate new keypair
new_private, new_public = generate_keypair()
save_keypair(new_private, new_public, key_dir="/new/keys")

# 2. Re-sign all artifacts
for artifact_info in list_artifacts():
    artifact = get_artifact(artifact_info["artifact_id"])

    # Sign with new key
    new_signature = sign_artifact(artifact, new_private)
    artifact["signature"] = new_signature

    # Save (creates new artifact_id due to immutability)
    new_artifact_id = save_artifact(artifact)

    print(f"Re-signed: {artifact_info['artifact_id']} → {new_artifact_id}")

# 3. Update profiles to point to new artifacts
# 4. Deprecate old key after grace period
```

### Verify Artifact Integrity

```python
from mcp_orchestrator.crypto import verify_artifact_integrity

# Full verification:
# 1. Signature valid?
# 2. Content hash matches artifact_id?
# 3. Timestamp not expired?
is_valid = verify_artifact_integrity(artifact)

if not is_valid:
    print("Artifact integrity check failed!")
    # Check individual components
    print(f"Signature valid: {verify_signature(artifact, public_key)}")
    print(f"Hash matches: {compute_hash(artifact['payload']) == artifact['artifact_id']}")
```

---

## Testing Cryptographic Code

**CRITICAL:** 100% coverage required for crypto module.

### Test Categories

1. **Happy Path:** Valid signatures verify correctly
```python
def test_valid_signature_verifies():
    private, public = generate_keypair()
    artifact = {"payload": "test"}
    signature = sign_artifact(artifact, private)
    assert verify_signature(artifact, signature, public) is True
```

2. **Tampered Payload:** Modified artifact fails verification
```python
def test_tampered_artifact_fails_verification():
    private, public = generate_keypair()
    artifact = {"payload": "original"}
    signature = sign_artifact(artifact, private)

    # Tamper with artifact
    artifact["payload"] = "modified"

    # Verification should fail
    assert verify_signature(artifact, signature, public) is False
```

3. **Wrong Key:** Signature from different key fails
```python
def test_wrong_public_key_fails():
    private_a, _ = generate_keypair()
    _, public_b = generate_keypair()  # Different keypair

    artifact = {"payload": "test"}
    signature = sign_artifact(artifact, private_a)

    # Verification with wrong public key should fail
    assert verify_signature(artifact, signature, public_b) is False
```

4. **Invalid Format:** Malformed signatures rejected
```python
def test_invalid_signature_format_rejected():
    artifact = {"payload": "test"}
    invalid_signature = {"algorithm": "invalid", "value": "not-base64"}

    with pytest.raises(CryptoError):
        verify_signature(artifact, invalid_signature, public_key)
```

5. **Edge Cases:** Empty payloads, max size artifacts
```python
def test_empty_payload_can_be_signed():
    private, public = generate_keypair()
    artifact = {"payload": ""}
    signature = sign_artifact(artifact, private)
    assert verify_signature(artifact, signature, public) is True

def test_large_payload_can_be_signed():
    private, public = generate_keypair()
    artifact = {"payload": "x" * 1_000_000}  # 1MB payload
    signature = sign_artifact(artifact, private)
    assert verify_signature(artifact, signature, public) is True
```

---

## Security Considerations

### Threat Model

**Protects Against:**
- ✅ Tampering: Modified artifacts detected via signature verification
- ✅ Forgery: Cannot create valid signature without private key
- ✅ Repudiation: Signature proves artifact origin
- ✅ Replay: Timestamp in signature (optional validation)

**Does NOT Protect:**
- ❌ Confidentiality: Artifacts NOT encrypted (plaintext)
- ❌ Key Compromise: If private key stolen, all signatures compromised
- ❌ Side Channels: Implementation must use constant-time comparison

### Best Practices

1. **Always Verify:** Check signatures before trusting artifacts
```python
artifact = get_artifact(artifact_id)
if not verify_signature(artifact, public_key):
    raise SecurityError("Untrusted artifact")
# Safe to use artifact
```

2. **Constant-Time Comparison:** Prevent timing attacks
```python
import hmac

def constant_time_compare(a: bytes, b: bytes) -> bool:
    """Constant-time byte comparison."""
    return hmac.compare_digest(a, b)
```

3. **Validate Inputs:** Check artifact structure before signing
```python
def validate_artifact_structure(artifact: dict):
    """Validate artifact has required fields."""
    required = ["artifact_id", "client_id", "payload"]
    for field in required:
        if field not in artifact:
            raise ValueError(f"Missing required field: {field}")
```

4. **Log Security Events:** Track sign/verify operations
```python
from mcp_orchestrator.memory import emit_event

# After signing
emit_event("crypto.artifact_signed", status="success",
           metadata={"artifact_id": artifact["artifact_id"]})

# After verification failure
emit_event("crypto.verification_failed", status="failure",
           metadata={"artifact_id": artifact["artifact_id"], "reason": "invalid_signature"})
```

5. **Key Rotation Plan:** Plan for key expiration/renewal
- **Frequency:** Annually or on compromise
- **Grace Period:** Allow old keys to verify during transition
- **Automation:** Script key rotation process

---

## Memory Integration

**Emit events for:**

```python
from mcp_orchestrator.memory import emit_event

# Key generation
emit_event("crypto.key_generated", status="success",
           metadata={"key_type": "ed25519", "key_path": key_path})

# Signing operations
emit_event("crypto.artifact_signed", status="success",
           metadata={"artifact_id": artifact_id, "timestamp": timestamp})

# Verification failures (security events)
emit_event("crypto.verification_failed", status="failure",
           metadata={"artifact_id": artifact_id, "reason": "tampered"})

# Key rotation
emit_event("crypto.key_rotated", status="success",
           metadata={"old_key_deprecated": True, "new_key_active": True})
```

**Create knowledge notes for:**
- Cryptographic vulnerabilities discovered
- Key rotation procedures and lessons learned
- Security audit findings
- Performance optimization for signing/verification

**Tag pattern:** `crypto`, `security`, `ed25519`, `[operation]`

---

## Related Documentation

- **[../AGENTS.md](../AGENTS.md)** - Core orchestrator
- **[../../AGENTS.md](../../AGENTS.md)** - Project overview
- **[../storage/AGENTS.md](../storage/AGENTS.md)** - Storage (artifact_id hashing uses SHA-256)
- **[RFC 8032](https://datatracker.ietf.org/doc/html/rfc8032)** - Ed25519 specification
- **[../../DOCUMENTATION_STANDARD.md](../../DOCUMENTATION_STANDARD.md)** - Docstring format

---

## Common Errors & Solutions

### Error: "Private key not found"

**Cause:** Keys not generated

**Solution:**
```bash
mcp-orchestration init-configs
```

### Error: "Signature verification failed"

**Possible Causes:**
1. Artifact modified after signing
2. Wrong public key used
3. Signature corrupted

**Debug:**
```python
# Check artifact_id hash
from mcp_orchestrator.storage import compute_hash
expected_id = compute_hash(artifact["payload"])
if expected_id != artifact["artifact_id"]:
    print("Artifact payload modified!")

# Compare public keys
print(f"Expected: {expected_public_key}")
print(f"Actual: {artifact['signature']['signer']['public_key']}")
```

### Error: "Invalid signature format"

**Cause:** Signature not base64-encoded 64-byte Ed25519 signature

**Solution:**
```python
import base64

# Check signature format
sig_bytes = base64.b64decode(signature["value"])
assert len(sig_bytes) == 64, "Ed25519 signature must be 64 bytes"
```

### Error: "Permission denied" (loading private key)

**Cause:** Private key permissions too restrictive or too permissive

**Solution:**
```bash
# Set correct permissions (Unix)
chmod 600 ~/.mcp-orchestration/keys/signing.key
```

---

**End of Cryptographic Operations Guide**

For questions not covered here, see [../AGENTS.md](../AGENTS.md) or [../../AGENTS.md](../../AGENTS.md).
