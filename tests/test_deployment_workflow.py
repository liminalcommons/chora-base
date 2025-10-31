"""Unit tests for DeploymentWorkflow (TDD - RED state).

These tests are written BEFORE implementation (TDD RED → GREEN → REFACTOR).
All tests will FAIL until Phase 5 (implementation) is complete.

Test Coverage:
- Deployment basics (deploy latest, deploy by ID)
- Error handling (invalid client, invalid artifact)
- Security (signature verification)
- Filesystem operations (atomic writes, parent dirs)
- Logging (deployment records)
"""

import json
import tempfile
from pathlib import Path

import pytest
from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.crypto import ArtifactSigner
from mcp_orchestrator.registry import get_default_registry as get_client_registry
from mcp_orchestrator.servers import get_default_registry as get_server_registry
from mcp_orchestrator.storage import ArtifactStore


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
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


@pytest.fixture
def sample_artifact(temp_storage):
    """Create a sample published artifact for testing."""
    server_registry = get_server_registry()
    builder = ConfigBuilder("claude-desktop", "default", server_registry)
    builder.add_server("filesystem", params={"path": "/tmp"})

    artifact = builder.to_artifact(
        signing_key_id="default",
        private_key_path=str(temp_storage["private_key_path"]),
        changelog="Test artifact",
    )

    store = ArtifactStore(base_path=str(temp_storage["base"]))
    store.store(artifact)

    return artifact


class TestDeploymentWorkflowBasics:
    """Test basic deployment operations."""

    def test_deploy_latest_artifact_succeeds(self, temp_storage, sample_artifact):
        """Test deploying latest artifact when artifact_id not specified.

        BDD: Scenario: Deploy latest configuration successfully
        """
        from mcp_orchestrator.deployment import DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

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
            public_key_path=str(temp_storage["public_key_path"]),
        )

        result = workflow.deploy(
            client_id="claude-desktop",
            profile_id="default",
            # artifact_id not specified → should deploy latest
        )

        assert result.status == "deployed"
        assert result.artifact_id == sample_artifact.artifact_id
        assert "claude_desktop_config.json" in result.config_path
        assert result.deployed_at  # ISO 8601 timestamp

    def test_deploy_specific_artifact_by_id(self, temp_storage, sample_artifact):
        """Test deploying specific artifact when artifact_id specified.

        BDD: Scenario: Deploy specific artifact by ID
        """
        from mcp_orchestrator.deployment import DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

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
            public_key_path=str(temp_storage["public_key_path"]),
        )

        result = workflow.deploy(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id=sample_artifact.artifact_id,  # Explicit artifact
        )

        assert result.status == "deployed"
        assert result.artifact_id == sample_artifact.artifact_id

    def test_deploy_to_unknown_client_fails(self, temp_storage):
        """Test deploying to non-existent client raises error.

        BDD: Scenario: Deploy to non-existent client fails
        """
        from mcp_orchestrator.deployment import DeploymentError, DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

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
            public_key_path=str(temp_storage["public_key_path"]),
        )

        with pytest.raises(DeploymentError) as exc_info:
            workflow.deploy(client_id="unknown-client", profile_id="default")

        error = exc_info.value
        assert "unknown-client" in str(error)
        assert error.details.get("code") == "CLIENT_NOT_FOUND"

    def test_deploy_invalid_artifact_id_fails(self, temp_storage):
        """Test deploying non-existent artifact raises error.

        BDD: Scenario: Deploy with invalid artifact ID fails
        """
        from mcp_orchestrator.deployment import DeploymentError, DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

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
            public_key_path=str(temp_storage["public_key_path"]),
        )

        with pytest.raises(DeploymentError) as exc_info:
            workflow.deploy(
                client_id="claude-desktop",
                profile_id="default",
                artifact_id="invalid-sha256-hash",
            )

        error = exc_info.value
        assert error.details.get("code") == "ARTIFACT_NOT_FOUND"


class TestDeploymentWorkflowSecurity:
    """Test signature verification before deployment."""

    def test_signature_verification_before_deploy(self, temp_storage, sample_artifact):
        """Test that signature is verified before writing config.

        BDD: Scenario: Deploy verifies signature before writing
        """
        from mcp_orchestrator.deployment import DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

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
            public_key_path=str(temp_storage["public_key_path"]),
        )

        # Should succeed with valid signature
        result = workflow.deploy("claude-desktop", "default")
        assert result.status == "deployed"

    def test_invalid_signature_rejects_deployment(self, temp_storage, sample_artifact):
        """Test that invalid signature prevents deployment.

        BDD: Scenario: Deploy verifies signature before writing
        """
        from mcp_orchestrator.deployment import DeploymentError, DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

        client_registry = get_client_registry()
        store = ArtifactStore(base_path=str(temp_storage["base"]))

        # Corrupt the signature
        artifact_file = (
            temp_storage["artifacts_dir"] / f"{sample_artifact.artifact_id}.json"
        )
        with open(artifact_file) as f:
            artifact_data = json.load(f)

        artifact_data["signature"] = "invalid-signature-corrupted"

        with open(artifact_file, "w") as f:
            json.dump(artifact_data, f)

        deployment_log = DeploymentLog(
            deployments_dir=str(temp_storage["deployments_dir"])
        )

        workflow = DeploymentWorkflow(
            store=store,
            client_registry=client_registry,
            deployment_log=deployment_log,
            config_base_dir=str(temp_storage["config_dir"]),
            public_key_path=str(temp_storage["public_key_path"]),
        )

        with pytest.raises(DeploymentError) as exc_info:
            workflow.deploy("claude-desktop", "default")

        error = exc_info.value
        assert error.details.get("code") == "SIGNATURE_INVALID"


class TestDeploymentWorkflowFilesystem:
    """Test filesystem operations."""

    def test_creates_parent_directories_if_needed(self, temp_storage, sample_artifact):
        """Test that parent directories are created automatically.

        BDD: Scenario: Deployment creates parent directories if needed
        """
        from mcp_orchestrator.deployment import DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

        client_registry = get_client_registry()
        store = ArtifactStore(base_path=str(temp_storage["base"]))
        deployment_log = DeploymentLog(
            deployments_dir=str(temp_storage["deployments_dir"])
        )

        # Use a config dir that doesn't exist yet
        nonexistent_config_dir = (
            temp_storage["base"] / "nonexistent" / "nested" / "path"
        )
        assert not nonexistent_config_dir.exists()

        workflow = DeploymentWorkflow(
            store=store,
            client_registry=client_registry,
            deployment_log=deployment_log,
            config_base_dir=str(nonexistent_config_dir),
            public_key_path=str(temp_storage["public_key_path"]),
        )

        result = workflow.deploy("claude-desktop", "default")
        assert result.status == "deployed"

        # Parent directories should have been created
        config_file = Path(result.config_path)
        assert config_file.parent.exists()

    def test_atomic_deployment_rollback_on_failure(self, temp_storage, sample_artifact):
        """Test that deployment rolls back on write failure (atomic operation).

        BDD: Scenario: Atomic deployment rolls back on write failure
        """
        from mcp_orchestrator.deployment import DeploymentError, DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

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
            public_key_path=str(temp_storage["public_key_path"]),
        )

        # Make config directory read-only to cause write failure
        temp_storage["config_dir"].chmod(0o444)

        try:
            with pytest.raises(DeploymentError) as exc_info:
                workflow.deploy("claude-desktop", "default")

            error = exc_info.value
            assert error.details.get("code") == "WRITE_FAILED"

            # No config file should exist (rollback)
            config_dir = temp_storage["config_dir"]
            config_files = list(config_dir.glob("**/*.json"))
            assert len(config_files) == 0  # No partial writes

        finally:
            # Restore permissions for cleanup
            temp_storage["config_dir"].chmod(0o755)


class TestDeploymentWorkflowLogging:
    """Test deployment logging and history."""

    def test_deployment_logged_to_deployment_log(self, temp_storage, sample_artifact):
        """Test that successful deployment is logged.

        BDD: Scenario: Deploy latest configuration successfully
        """
        from mcp_orchestrator.deployment import DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

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
            public_key_path=str(temp_storage["public_key_path"]),
        )

        workflow.deploy("claude-desktop", "default")

        # Check deployment was logged
        deployed_artifact = deployment_log.get_deployed_artifact(
            "claude-desktop", "default"
        )
        assert deployed_artifact == sample_artifact.artifact_id

    def test_query_deployed_vs_latest_resources(self, temp_storage):
        """Test querying deployed vs latest artifact (drift detection).

        BDD: Scenario: Query deployed vs latest artifact
        """
        from mcp_orchestrator.deployment import DeploymentWorkflow
        from mcp_orchestrator.deployment.log import DeploymentLog

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
            public_key_path=str(temp_storage["public_key_path"]),
        )

        # Publish and deploy v1
        builder_v1 = ConfigBuilder("claude-desktop", "default", server_registry)
        builder_v1.add_server("filesystem", params={"path": "/tmp"})
        artifact_v1 = builder_v1.to_artifact(
            signing_key_id="default",
            private_key_path=str(temp_storage["private_key_path"]),
            changelog="v1",
        )
        store.store(artifact_v1)
        workflow.deploy("claude-desktop", "default")

        # Publish v2 (without deploying)
        builder_v2 = ConfigBuilder("claude-desktop", "default", server_registry)
        builder_v2.add_server("filesystem", params={"path": "/tmp"})
        builder_v2.add_server("github", env_vars={"GITHUB_TOKEN": "test"})
        artifact_v2 = builder_v2.to_artifact(
            signing_key_id="default",
            private_key_path=str(temp_storage["private_key_path"]),
            changelog="v2",
        )
        store.store(artifact_v2)

        # Query deployed (should be v1)
        deployed = deployment_log.get_deployed_artifact("claude-desktop", "default")
        assert deployed == artifact_v1.artifact_id

        # Query latest (should be v2)
        latest = store.get("claude-desktop", "default")
        assert latest.artifact_id == artifact_v2.artifact_id

        # Drift detected
        assert deployed != latest.artifact_id
