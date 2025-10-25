---
title: Understanding Cryptographic Signing
audience: end-users
difficulty: intermediate
wave: 1.0
version: v0.1.3
---

# Understanding Cryptographic Signing

When you publish a configuration with mcp-orchestration, it gets cryptographically signed. This document explains why signatures matter and how they protect your work.

## The Core Problem

Configuration files control which tools your AI assistant can use. A malicious configuration could:
- Grant access to sensitive files
- Expose your private API keys
- Execute arbitrary commands on your system

**The question:** How do you know a configuration came from who you think it did?

## What Signing Accomplishes

Cryptographic signatures provide two guarantees:

### 1. Authenticity

**"This configuration came from me, not someone else."**

When you sign a configuration with your private key, only you could have created that signature. Anyone can verify it came from you using your public key, but they cannot create signatures pretending to be you.

### 2. Integrity

**"This configuration hasn't been tampered with."**

If even one character changes in the configuration, the signature becomes invalid. You can detect if someone modified the configuration after you signed it.

## How It Works

mcp-orchestration uses **Ed25519**, a modern cryptographic signature algorithm.

### Key Generation

When you run `initialize_keys`, two keys are created:

**Private Key** (`~/.mcp-orchestration/keys/signing.key`)
- Secret, never shared
- Used to create signatures
- Protected with file permissions (0600 = only you can read)

**Public Key** (`~/.mcp-orchestration/keys/signing.pub`)
- Shareable, published openly
- Used by others to verify your signatures
- No security risk if exposed

**Analogy:** Like a wax seal on a letter - your signet ring (private key) creates the seal, anyone can verify it matches your known seal pattern (public key), but only you can create new seals.

### The Signing Process

When you publish a configuration:

1. **Hash the content** - The configuration is reduced to a SHA-256 hash (a unique fingerprint)
2. **Sign the hash** - Your private key transforms the hash into a signature
3. **Attach signature** - The signature is stored alongside the configuration
4. **Content-address** - The SHA-256 hash becomes the artifact ID

### The Verification Process

When someone retrieves your configuration:

1. **Recompute hash** - Hash the configuration payload
2. **Check signature** - Use your public key to verify the signature matches the hash
3. **Compare IDs** - Verify the artifact ID matches the recomputed hash

If verification passes: The configuration is authentic and unmodified.
If verification fails: Either someone tampered with it, or it was signed with a different key.

## Why Ed25519?

mcp-orchestration uses Ed25519 specifically because:

- **Fast** - Signing and verification are very quick
- **Small** - Keys and signatures are compact (32-byte keys, 64-byte signatures)
- **Secure** - Resistant to known cryptographic attacks
- **Deterministic** - Same input always produces same signature (important for content-addressing)
- **Modern** - Designed in 2011 with lessons from earlier algorithms

**Alternatives considered:**
- **RSA** - Older, larger keys (2048+ bits), slower
- **ECDSA** - Requires randomness (non-deterministic), more complex
- **GPG** - Overcomplicated for this use case, poor UX

## Content-Addressable Storage

mcp-orchestration combines signatures with **content-addressing**.

### What is Content-Addressing?

The artifact ID is the SHA-256 hash of the configuration payload:

```
8e91a062ff85a4180e571fd3821941aafa1b41d582582275aec426dae657c6de
```

This means:
- **Same content = same ID** - Identical configurations always have identical IDs
- **Different content = different ID** - Even a one-character change produces a completely different ID
- **Immutable** - You can't change the content without changing the ID
- **Verifiable** - Anyone can recompute the hash to verify the ID is correct

**Benefit:** You can refer to configurations by their hash and be certain you're talking about the exact same bytes.

## Trust Model

### Who Do You Trust?

When using mcp-orchestration, you trust:

1. **Yourself** - Your private key signs configurations you create
2. **The cryptographic algorithms** - Ed25519 and SHA-256 are peer-reviewed and widely trusted
3. **The storage system** - Artifacts are stored locally under your control

You do NOT need to trust:
- Third-party repositories (you verify signatures locally)
- Network infrastructure (tampering is detected)
- Other users (they can't forge your signatures)

### Future: Multi-Party Trust

While not yet implemented, the signing infrastructure supports future scenarios:

**Team configurations:**
- Multiple people sign the same config (multi-signature)
- Requires M-of-N signatures to be valid

**Publisher trust:**
- Community members publish server configurations
- You choose which public keys to trust
- Verify published configs before use

## Threat Model

### What Signatures Protect Against

✅ **Tampering** - Configuration modified in transit or storage
✅ **Impersonation** - Someone publishing configs pretending to be you
✅ **Rollback** - Old, vulnerable configs replacing newer ones (detected via timestamps)
✅ **Substitution** - Different config swapped in with same name

### What Signatures Don't Protect Against

❌ **Key theft** - If someone steals your private key, they can sign as you
❌ **Implementation bugs** - Vulnerabilities in the signing code itself
❌ **Social engineering** - Tricking you into signing a malicious config
❌ **Initial trust** - First time you see a public key, you must verify it's authentic (key verification problem)

## Key Management

### Key Lifecycle

**Generation** - `initialize_keys` creates a fresh key pair
**Usage** - Private key signs configs, public key verifies
**Rotation** - Not yet supported (coming in future wave)
**Revocation** - Not yet supported (coming in future wave)

### Best Practices

**Do:**
- Keep private key file permissions restrictive (0600)
- Back up your private key securely
- Use different keys for different purposes (personal vs team)

**Don't:**
- Commit private keys to version control
- Share private keys via email or Slack
- Reuse keys across different systems

### If Your Key Is Compromised

Currently, if your private key is stolen:
1. Delete the compromised key immediately
2. Generate new keys with `initialize_keys(regenerate=True)`
3. Re-publish all configurations with new signature
4. Notify anyone using your configurations

*Note: Future waves will add key revocation mechanisms.*

## Comparison with Other Systems

### Git Commit Signing

**Similarities:**
- Both use Ed25519 (Git supports it as of v2.34)
- Both sign content hashes
- Both provide authenticity and integrity

**Differences:**
- Git signs commits (history), mcp-orchestration signs artifacts (configuration snapshots)
- Git uses PGP by default, mcp-orchestration uses Ed25519 exclusively
- Git has complex key management (keyring), mcp-orchestration has simple files

### Package Managers (npm, PyPI)

**Similarities:**
- Both sign published artifacts
- Both use content-addressing (checksums)
- Both have trust/verification workflows

**Differences:**
- Package managers sign packages, mcp-orchestration signs configs
- Package managers have centralized registries, mcp-orchestration is local-first
- Package managers require account management, mcp-orchestration is file-based

### Docker Image Signing (Sigstore)

**Similarities:**
- Both sign content-addressable artifacts
- Both aim for supply-chain security
- Both use modern cryptography

**Differences:**
- Docker uses Sigstore (ephemeral keys, transparency logs), mcp-orchestration uses long-lived keys
- Docker signs container images, mcp-orchestration signs JSON configs
- Docker integrates with PKI infrastructure, mcp-orchestration is self-contained

## When Signatures Matter Most

Signatures become critical in these scenarios:

### Scenario 1: Shared Configurations

You publish configurations for your team to use. Signatures prove:
- The config came from you, not a malicious teammate
- Nobody modified it after you published it

### Scenario 2: Public Registries

When publishing to shared registries (future wave):
- Community members verify your signature before trusting your config
- You verify publisher signatures before using their servers

### Scenario 3: Compliance & Audit

For regulated environments:
- Signatures provide non-repudiation (you can't deny signing a config)
- Audit trails show who signed what and when
- Tampering attempts are detectable

### Scenario 4: Long-Term Storage

Configurations stored for years:
- Verify they haven't been corrupted
- Prove they haven't been backdated or forged
- Maintain chain of custody

## The Bigger Picture

Cryptographic signing is part of a **secure-by-design** philosophy:

1. **Default security** - Signing is automatic, not opt-in
2. **Fail securely** - Invalid signatures are rejected, not ignored
3. **Transparent operation** - You can inspect signatures, verify independently
4. **Minimal trust** - Rely on math, not authority

This foundation enables future features:
- Decentralized configuration sharing
- Automated update verification
- Supply-chain security for AI tooling
- Compliance-ready audit trails

## Learn More

**For deeper cryptography:**
- [Ed25519 specification](https://ed25519.cr.yp.to/)
- [Content-Addressable Storage](https://en.wikipedia.org/wiki/Content-addressable_storage)
- [How SHA-256 works](https://sha256algorithm.com/)

**For practical usage:**
- [Tutorial: Your First Configuration](../tutorials/01-first-configuration.md) - Use signing in practice
- [How-To: Verify Signatures](../how-to/verify-signatures.md) - Verify artifacts
- [Reference: initialize_keys](../reference/mcp-tools.md#initialize_keys) - Key generation API

---

**Remember:** Signatures don't make bad configurations good - they just prove who created them. Always review what you're signing.
