"""Tests for PublishingWorkflow (Wave 1.4).

This module tests the publishing workflow following BDD scenarios from
project-docs/capabilities/behaviors/mcp-config-publish.feature

Following TDD: These tests are written BEFORE implementation.
"""

import tempfile
from pathlib import Path

import pytest

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.crypto import ArtifactSigner
from mcp_orchestrator.registry import ClientRegistry
from mcp_orchestrator.servers.models import (
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)
from mcp_orchestrator.servers.registry import ServerRegistry
from mcp_orchestrator.storage import ArtifactStore


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)

        # Create keys
        key_dir = base_path / "keys"
        key_dir.mkdir()
        private_key_path = key_dir / "signing.key"
        public_key_path = key_dir / "signing.pub"

        signer = ArtifactSigner.generate(key_id="default")
        signer.save_private_key(str(private_key_path))
        signer.save_public_key(str(public_key_path))

        yield {
            "base_path": base_path,
            "private_key_path": private_key_path,
            "public_key_path": public_key_path,
        }


@pytest.fixture
def sample_registry():
    """Create sample server registry."""
    registry = ServerRegistry()
    registry.register(
        ServerDefinition(
            server_id="filesystem",
            display_name="Filesystem",
            description="File access",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-filesystem", "{path}"],
            parameters=[
                ParameterDefinition(
                    name="path", type="path", description="Root path", required=True
                )
            ],
        )
    )
    registry.register(
        ServerDefinition(
            server_id="github",
            display_name="GitHub",
            description="GitHub integration",
            transport=TransportType.STDIO,
            stdio_command="npx",
            stdio_args=["-y", "@modelcontextprotocol/server-github"],
            required_env=["GITHUB_TOKEN"],
        )
    )
    return registry


class TestPublishingWorkflowValidation:
    """Test validation integration in publishing workflow.

    References BDD scenarios:
    - Scenario: Publish valid configuration
    - Scenario: Reject configuration with validation errors
    - Scenario: Validation runs before signing
    """

    def test_publish_valid_config_succeeds(self, temp_storage, sample_registry):
        """Test publishing a valid configuration succeeds.

        BDD: Scenario: Publish valid configuration
        """
        from mcp_orchestrator.publishing import PublishingWorkflow

        # Arrange
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test"})

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act
        result = workflow.publish(
            builder=builder,
            private_key_path=str(temp_storage["private_key_path"]),
            signing_key_id="default",
            changelog="Test publish",
        )

        # Assert
        assert result["status"] == "published"
        assert "artifact_id" in result
        assert result["server_count"] == 2
        assert result["changelog"] == "Test publish"

    def test_publish_invalid_config_fails(self, temp_storage, sample_registry):
        """Test publishing invalid config fails with validation errors.

        BDD: Scenario: Reject configuration with validation errors
        """
        from mcp_orchestrator.publishing import PublishingWorkflow, ValidationError

        # Arrange - create config with validation error
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        # Manually corrupt the config
        builder._servers["filesystem"].pop("command")

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            workflow.publish(
                builder=builder,
                private_key_path=str(temp_storage["private_key_path"]),
                signing_key_id="default",
                changelog="Should fail",
            )

        assert "MISSING_COMMAND" in str(exc_info.value)

    def test_publish_empty_config_rejected(self, temp_storage, sample_registry):
        """Test empty config is rejected.

        BDD: Scenario: Reject empty configuration
        """
        from mcp_orchestrator.publishing import PublishingWorkflow, ValidationError

        # Arrange - empty config
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            workflow.publish(
                builder=builder,
                private_key_path=str(temp_storage["private_key_path"]),
                signing_key_id="default",
                changelog="Should fail",
            )

        assert "EMPTY_CONFIG" in str(exc_info.value)

    def test_validation_runs_before_signing(self, temp_storage, sample_registry):
        """Test validation runs before signing operation.

        BDD: Scenario: Validation runs before signing
        """
        from mcp_orchestrator.publishing import PublishingWorkflow, ValidationError

        # Arrange - invalid config
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder._servers["filesystem"].pop("args")  # Make invalid

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act
        try:
            workflow.publish(
                builder=builder,
                private_key_path=str(temp_storage["private_key_path"]),
                signing_key_id="default",
                changelog="Should fail",
            )
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

        # Assert - no artifacts should be created
        artifacts_dir = temp_storage["base_path"] / "artifacts"
        if artifacts_dir.exists():
            assert len(list(artifacts_dir.iterdir())) == 0, "No artifacts should be created"


class TestPublishingWorkflowMetadata:
    """Test metadata enrichment during publishing.

    References BDD scenarios:
    - Scenario: Include changelog in metadata
    - Scenario: Auto-generate metadata fields
    """

    def test_changelog_included_in_metadata(self, temp_storage, sample_registry):
        """Test changelog is included in published artifact.

        BDD: Scenario: Include changelog in metadata
        """
        from mcp_orchestrator.publishing import PublishingWorkflow

        # Arrange
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        changelog = "Added filesystem server for testing"

        # Act
        result = workflow.publish(
            builder=builder,
            private_key_path=str(temp_storage["private_key_path"]),
            signing_key_id="default",
            changelog=changelog,
        )

        # Assert
        artifact = store.get_by_id(result["artifact_id"])
        assert artifact.metadata["changelog"] == changelog

    def test_auto_generated_metadata(self, temp_storage, sample_registry):
        """Test metadata fields are auto-generated.

        BDD: Scenario: Auto-generate metadata fields
        """
        from mcp_orchestrator.publishing import PublishingWorkflow

        # Arrange
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})
        builder.add_server("github", env_vars={"GITHUB_TOKEN": "ghp_test"})

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act
        result = workflow.publish(
            builder=builder,
            private_key_path=str(temp_storage["private_key_path"]),
            signing_key_id="default",
            changelog="Test",
        )

        # Assert
        artifact = store.get_by_id(result["artifact_id"])
        assert artifact.metadata["generator"] == "PublishingWorkflow"
        assert artifact.metadata["server_count"] == 2


class TestPublishingWorkflowAtomicity:
    """Test atomic publishing operations.

    References BDD scenario:
    - Scenario: Publishing is atomic
    """

    def test_publish_rollback_on_storage_error(self, temp_storage, sample_registry):
        """Test publish operation is rolled back on storage failure.

        BDD: Scenario: Publishing is atomic
        """
        from mcp_orchestrator.publishing import PublishingWorkflow

        # Arrange
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        # Create a store that will fail on store()
        class FailingStore(ArtifactStore):
            def store(self, artifact):
                raise IOError("Simulated storage failure")

        store = FailingStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act & Assert
        with pytest.raises(IOError):
            workflow.publish(
                builder=builder,
                private_key_path=str(temp_storage["private_key_path"]),
                signing_key_id="default",
                changelog="Should fail",
            )

        # Verify no artifacts created and profile index not updated
        artifacts_dir = temp_storage["base_path"] / "artifacts"
        if artifacts_dir.exists():
            assert len(list(artifacts_dir.iterdir())) == 0


class TestPublishingWorkflowSigning:
    """Test cryptographic signing during publishing.

    References BDD scenarios:
    - Scenario: Publish valid configuration (signing aspect)
    - Scenario: Content-addressable artifact ID
    """

    def test_artifact_is_signed(self, temp_storage, sample_registry):
        """Test published artifact is cryptographically signed."""
        from mcp_orchestrator.publishing import PublishingWorkflow
        from mcp_orchestrator.crypto import verify_signature

        # Arrange
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act
        result = workflow.publish(
            builder=builder,
            private_key_path=str(temp_storage["private_key_path"]),
            signing_key_id="default",
            changelog="Test",
        )

        # Assert
        artifact = store.get_by_id(result["artifact_id"])
        is_valid = verify_signature(
            artifact.payload,
            artifact.signature,
            str(temp_storage["public_key_path"]),
        )
        assert is_valid is True

    def test_artifact_id_is_content_addressable(self, temp_storage, sample_registry):
        """Test artifact ID is SHA-256 hash of payload.

        BDD: Scenario: Content-addressable artifact ID
        """
        from mcp_orchestrator.publishing import PublishingWorkflow
        import hashlib
        import json

        # Arrange
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act
        result = workflow.publish(
            builder=builder,
            private_key_path=str(temp_storage["private_key_path"]),
            signing_key_id="default",
            changelog="Test",
        )

        # Assert
        artifact = store.get_by_id(result["artifact_id"])

        # Compute expected SHA-256
        canonical_json = json.dumps(
            artifact.payload, sort_keys=True, separators=(",", ":")
        )
        expected_id = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

        assert result["artifact_id"] == expected_id
        assert len(result["artifact_id"]) == 64  # SHA-256 hex length


class TestPublishingWorkflowProfileIndex:
    """Test profile index updates during publishing.

    References BDD scenario:
    - Scenario: Publish valid configuration (index update aspect)
    """

    def test_profile_index_updated(self, temp_storage, sample_registry):
        """Test profile index points to new artifact after publish."""
        from mcp_orchestrator.publishing import PublishingWorkflow

        # Arrange
        builder = ConfigBuilder("claude-desktop", "default", sample_registry)
        builder.add_server("filesystem", params={"path": "/tmp"})

        store = ArtifactStore(base_path=temp_storage["base_path"])
        client_registry = ClientRegistry()

        workflow = PublishingWorkflow(
            store=store,
            client_registry=client_registry,
        )

        # Act
        result = workflow.publish(
            builder=builder,
            private_key_path=str(temp_storage["private_key_path"]),
            signing_key_id="default",
            changelog="Test",
        )

        # Assert
        index = store.get_profile_metadata("claude-desktop", "default")
        assert index.latest_artifact_id == result["artifact_id"]
