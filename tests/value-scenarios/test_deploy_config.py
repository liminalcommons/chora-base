"""E2E Value Scenario Tests for Config Deployment.

These tests execute the workflows described in user-docs/how-to/deploy-config.md,
ensuring the how-to guide remains accurate and tested (living documentation).

Test Coverage:
- test_value_scenario_deploy_latest_config: Full deployment workflow
- test_value_scenario_deploy_specific_version: Version pinning / rollback
- test_value_scenario_query_deployed_vs_latest: Configuration drift detection
"""

import json
import tempfile
from pathlib import Path

import pytest

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.crypto import ArtifactSigner
from mcp_orchestrator.deployment import DeploymentWorkflow
from mcp_orchestrator.registry import get_default_registry as get_client_registry
from mcp_orchestrator.servers import get_default_registry as get_server_registry
from mcp_orchestrator.storage import ArtifactStore


@pytest.fixture
def temp_storage():
    """Create temporary storage directories for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)

        # Storage directories
        artifacts_dir = base / "artifacts"
        index_dir = base / "index"
        keys_dir = base / "keys"
        deployments_dir = base / "deployments"
        config_dir = base / "client_configs"

        artifacts_dir.mkdir()
        index_dir.mkdir()
        keys_dir.mkdir()
        deployments_dir.mkdir()
        config_dir.mkdir()

        # Generate keys
        signer = ArtifactSigner.generate(key_id="default")
        private_key_path = keys_dir / "signing.key"
        public_key_path = keys_dir / "signing.pub"
        signer.save_private_key(str(private_key_path))
        signer.save_public_key(str(public_key_path))

        yield {
            "base": base,
            "artifacts_dir": artifacts_dir,
            "index_dir": index_dir,
            "keys_dir": keys_dir,
            "deployments_dir": deployments_dir,
            "config_dir": config_dir,
            "private_key_path": private_key_path,
            "public_key_path": public_key_path,
        }


def test_value_scenario_deploy_latest_config(temp_storage):
    """E2E test executing the deploy-config how-to guide.

    This test follows the complete workflow from user-docs/how-to/deploy-config.md:
    1. Initialize keys (done in fixture)
    2. Publish configuration
    3. Deploy configuration
    4. Verify deployment
    5. Query deployment status

    Validates: "Deploy Latest Configuration (MCP Tool)" section
    """
    from mcp_orchestrator.deployment.log import DeploymentLog

    # Setup
    server_registry = get_server_registry()
    client_registry = get_client_registry()
    store = ArtifactStore(base_path=str(temp_storage["base"]))
    deployment_log = DeploymentLog(
        deployments_dir=str(temp_storage["deployments_dir"])
    )

    # 1. Create and publish configuration
    builder = ConfigBuilder("claude-desktop", "default", server_registry)
    builder.add_server("filesystem", params={"path": "/tmp/docs"})
    builder.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test"})

    artifact = builder.to_artifact(
        signing_key_id="default",
        private_key_path=str(temp_storage["private_key_path"]),
        changelog="Added filesystem and github servers"
    )

    store.store(artifact)
    published_artifact_id = artifact.artifact_id

    # 2. Deploy configuration (this is the workflow we're testing)
    workflow = DeploymentWorkflow(
        store=store,
        client_registry=client_registry,
        deployment_log=deployment_log,
        config_base_dir=str(temp_storage["config_dir"]),  # Override for testing
        public_key_path=str(temp_storage["public_key_path"])
    )

    result = workflow.deploy(
        client_id="claude-desktop",
        profile_id="default"
        # artifact_id not specified → deploys latest
    )

    # 3. Verify deployment succeeded
    assert result.status == "deployed"
    assert result.artifact_id == published_artifact_id
    assert "claude_desktop_config.json" in result.config_path
    assert result.deployed_at  # ISO 8601 timestamp

    # 4. Verify config file was written
    config_file = Path(result.config_path)
    assert config_file.exists()

    with open(config_file) as f:
        deployed_config = json.load(f)

    assert "mcpServers" in deployed_config
    assert "filesystem" in deployed_config["mcpServers"]
    assert "github" in deployed_config["mcpServers"]

    # 5. Verify deployment was logged
    deployed_artifact = deployment_log.get_deployed_artifact("claude-desktop", "default")
    assert deployed_artifact == published_artifact_id


def test_value_scenario_deploy_specific_version(temp_storage):
    """E2E test for deploying specific artifact version (rollback scenario).

    This test validates version pinning / rollback workflow from the guide:
    1. Publish multiple versions (v1, v2, v3)
    2. Deploy specific version (v1)
    3. Verify correct version deployed
    4. Verify latest is still v3

    Validates: "Deploy Specific Version (Version Pinning)" section
    """
    from mcp_orchestrator.deployment.log import DeploymentLog

    # Setup
    server_registry = get_server_registry()
    client_registry = get_client_registry()
    store = ArtifactStore(base_path=str(temp_storage["base"]))
    deployment_log = DeploymentLog(
        deployments_dir=str(temp_storage["deployments_dir"])
    )
    workflow = DeploymentWorkflow(
        store=store,
        client_registry=client_registry,
        deployment_log=deployment_log,
        config_base_dir=str(temp_storage["config_dir"]),
        public_key_path=str(temp_storage["public_key_path"])
    )

    # 1. Publish v1
    builder_v1 = ConfigBuilder("claude-desktop", "default", server_registry)
    builder_v1.add_server("filesystem", params={"path": "/tmp"})

    artifact_v1 = builder_v1.to_artifact(
        signing_key_id="default",
        private_key_path=str(temp_storage["private_key_path"]),
        changelog="v1: Initial config"
    )
    store.store(artifact_v1)

    # 2. Publish v2
    builder_v2 = ConfigBuilder("claude-desktop", "default", server_registry)
    builder_v2.add_server("filesystem", params={"path": "/tmp"})
    builder_v2.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test"})

    artifact_v2 = builder_v2.to_artifact(
        signing_key_id="default",
        private_key_path=str(temp_storage["private_key_path"]),
        changelog="v2: Added github"
    )
    store.store(artifact_v2)

    # 3. Publish v3 (latest)
    builder_v3 = ConfigBuilder("claude-desktop", "default", server_registry)
    builder_v3.add_server("filesystem", params={"path": "/tmp"})
    builder_v3.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test"})
    builder_v3.add_server("brave-search", env_vars={"BRAVE_API_KEY": "test"})

    artifact_v3 = builder_v3.to_artifact(
        signing_key_id="default",
        private_key_path=str(temp_storage["private_key_path"]),
        changelog="v3: Added brave-search"
    )
    store.store(artifact_v3)

    # 4. Deploy v1 explicitly (rollback scenario)
    result = workflow.deploy(
        client_id="claude-desktop",
        profile_id="default",
        artifact_id=artifact_v1.artifact_id  # Pin to v1
    )

    # 5. Verify v1 was deployed
    assert result.status == "deployed"
    assert result.artifact_id == artifact_v1.artifact_id

    config_file = Path(result.config_path)
    with open(config_file) as f:
        deployed_config = json.load(f)

    # Should have only filesystem (v1), not github or brave-search
    assert len(deployed_config["mcpServers"]) == 1
    assert "filesystem" in deployed_config["mcpServers"]
    assert "github" not in deployed_config["mcpServers"]

    # 6. Verify latest is still v3
    latest = store.get("claude-desktop", "default")
    assert latest.artifact_id == artifact_v3.artifact_id

    # 7. Verify deployment log shows v1
    deployed_artifact = deployment_log.get_deployed_artifact("claude-desktop", "default")
    assert deployed_artifact == artifact_v1.artifact_id


def test_value_scenario_query_deployed_vs_latest(temp_storage):
    """E2E test for detecting configuration drift.

    This test validates the drift detection workflow from the guide:
    1. Deploy v1
    2. Publish v2 (without deploying)
    3. Query deployed → v1
    4. Query latest → v2
    5. Detect drift

    Validates: "Query Deployed vs Latest Configuration" section
    """
    from mcp_orchestrator.deployment.log import DeploymentLog

    # Setup
    server_registry = get_server_registry()
    client_registry = get_client_registry()
    store = ArtifactStore(base_path=str(temp_storage["base"]))
    deployment_log = DeploymentLog(
        deployments_dir=str(temp_storage["deployments_dir"])
    )
    workflow = DeploymentWorkflow(
        store=store,
        client_registry=client_registry,
        deployment_log=deployment_log,
        config_base_dir=str(temp_storage["config_dir"]),
        public_key_path=str(temp_storage["public_key_path"])
    )

    # 1. Publish and deploy v1
    builder_v1 = ConfigBuilder("claude-desktop", "default", server_registry)
    builder_v1.add_server("filesystem", params={"path": "/tmp"})

    artifact_v1 = builder_v1.to_artifact(
        signing_key_id="default",
        private_key_path=str(temp_storage["private_key_path"]),
        changelog="v1: Initial"
    )
    store.store(artifact_v1)

    workflow.deploy("claude-desktop", "default")

    # 2. Publish v2 (newer) without deploying
    builder_v2 = ConfigBuilder("claude-desktop", "default", server_registry)
    builder_v2.add_server("filesystem", params={"path": "/tmp"})
    builder_v2.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test"})

    artifact_v2 = builder_v2.to_artifact(
        signing_key_id="default",
        private_key_path=str(temp_storage["private_key_path"]),
        changelog="v2: Added github"
    )
    store.store(artifact_v2)

    # 3. Query deployed artifact
    deployed_artifact_id = deployment_log.get_deployed_artifact("claude-desktop", "default")
    assert deployed_artifact_id == artifact_v1.artifact_id

    # 4. Query latest artifact
    latest = store.get("claude-desktop", "default")
    assert latest.artifact_id == artifact_v2.artifact_id

    # 5. Detect drift
    drift_detected = (deployed_artifact_id != latest.artifact_id)
    assert drift_detected is True

    # This is the "configuration drift" scenario described in the guide:
    # - Deployed version: v1
    # - Latest version: v2
    # - User should run deploy_config() to update
