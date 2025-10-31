"""Shared pytest fixtures for mcp-orchestration tests.

This module provides common fixtures used across multiple test files,
reducing code duplication and ensuring consistent test setup.
"""

from pathlib import Path
from typing import Any

import pytest
from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.crypto import ArtifactSigner
from mcp_orchestrator.servers import get_default_registry
from mcp_orchestrator.storage import ArtifactStore


@pytest.fixture
def tmp_storage(tmp_path: Path) -> dict[str, Path]:
    """Create temporary storage structure for testing.

    Returns:
        Dictionary with paths to temporary storage directories:
        - artifacts_dir: Artifact storage directory
        - index_dir: Index directory
        - keys_dir: Keys directory
        - deployments_dir: Deployments directory
        - config_dir: Client configs directory
        - private_key_path: Path to generated private key
        - public_key_path: Path to generated public key
    """
    artifacts_dir = tmp_path / "artifacts"
    index_dir = tmp_path / "index"
    keys_dir = tmp_path / "keys"
    deployments_dir = tmp_path / "deployments"
    config_dir = tmp_path / "client_configs"

    # Create directories
    for dir_path in [artifacts_dir, index_dir, keys_dir, deployments_dir, config_dir]:
        dir_path.mkdir(parents=True, exist_ok=True)

    # Generate test keypair
    private_key_path = keys_dir / "signing_key"
    public_key_path = keys_dir / "signing_key.pub"
    signer = ArtifactSigner.generate(key_id="test")
    signer.save_private_key(str(private_key_path))
    signer.save_public_key(str(public_key_path))

    return {
        "artifacts_dir": artifacts_dir,
        "index_dir": index_dir,
        "keys_dir": keys_dir,
        "deployments_dir": deployments_dir,
        "config_dir": config_dir,
        "private_key_path": private_key_path,
        "public_key_path": public_key_path,
    }


@pytest.fixture
def artifact_store(tmp_path: Path) -> ArtifactStore:
    """Create artifact store in temp directory.

    Returns:
        ArtifactStore: Initialized artifact store for testing
    """
    return ArtifactStore(base_path=tmp_path)


@pytest.fixture
def sample_config_payload() -> dict[str, Any]:
    """Sample MCP configuration payload.

    Returns:
        Dictionary with sample MCP server configuration
    """
    return {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem"],
                "env": {"PATH": "/tmp"},
            }
        }
    }


@pytest.fixture
def config_builder() -> ConfigBuilder:
    """Create ConfigBuilder with server registry.

    Returns:
        ConfigBuilder: Initialized config builder for claude-desktop/default
    """
    server_registry = get_default_registry()
    return ConfigBuilder("claude-desktop", "default", server_registry)


@pytest.fixture
def test_keypair(tmp_path: Path) -> dict[str, Path]:
    """Generate temporary test keypair.

    Returns:
        Dictionary with private_key_path and public_key_path
    """
    keys_dir = tmp_path / "keys"
    keys_dir.mkdir(parents=True, exist_ok=True)

    private_key_path = keys_dir / "test_signing_key"
    public_key_path = keys_dir / "test_signing_key.pub"

    signer = ArtifactSigner.generate(key_id="test")
    signer.save_private_key(str(private_key_path))
    signer.save_public_key(str(public_key_path))

    return {
        "private_key_path": private_key_path,
        "public_key_path": public_key_path,
    }
