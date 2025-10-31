"""Tests for DeploymentLog (deployment/log.py).

This module tests deployment logging and history tracking:
- Recording deployment events
- Querying deployed artifacts
- Retrieving deployment history
- Log file structure and format

Testing patterns:
- Use tmp_path for isolated test directories
- Test JSON log file persistence
- Test chronological history ordering
- Test history limits
"""

import json
from datetime import datetime
from pathlib import Path

import pytest

from mcp_orchestrator.deployment.log import DeploymentLog, DeploymentRecord


@pytest.fixture
def deployment_log(tmp_path):
    """Create DeploymentLog in temporary directory."""
    deployments_dir = tmp_path / "deployments"
    return DeploymentLog(deployments_dir=str(deployments_dir))


class TestDeploymentLogInitialization:
    """Test DeploymentLog initialization."""

    def test_creates_deployments_directory(self, tmp_path):
        """Test that DeploymentLog creates deployments directory."""
        deployments_dir = tmp_path / "new_deployments"
        assert not deployments_dir.exists()

        DeploymentLog(deployments_dir=str(deployments_dir))

        assert deployments_dir.exists()
        assert deployments_dir.is_dir()


class TestRecordDeployment:
    """Test recording deployment events."""

    def test_record_deployment_creates_log_file(self, deployment_log, tmp_path):
        """Test recording deployment creates log file."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="abc123",
            config_path="/path/to/config.json"
        )

        log_path = tmp_path / "deployments" / "claude-desktop" / "default.json"
        assert log_path.exists()

    def test_record_deployment_with_changelog(self, deployment_log):
        """Test recording deployment with changelog."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="abc123",
            config_path="/path/to/config.json",
            changelog="Added filesystem server"
        )

        deployed = deployment_log.get_deployed_artifact("claude-desktop", "default")
        assert deployed == "abc123"

    def test_record_deployment_creates_client_directory(self, deployment_log, tmp_path):
        """Test that recording deployment creates client directory if needed."""
        client_dir = tmp_path / "deployments" / "cursor"
        assert not client_dir.exists()

        deployment_log.record_deployment(
            client_id="cursor",
            profile_id="default",
            artifact_id="def456",
            config_path="/path/to/config.json"
        )

        assert client_dir.exists()
        assert client_dir.is_dir()

    def test_record_deployment_updates_existing_log(self, deployment_log):
        """Test that recording deployment updates existing log."""
        # Record first deployment
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="v1",
            config_path="/path/v1.json"
        )

        # Record second deployment
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="v2",
            config_path="/path/v2.json"
        )

        # Current deployment should be v2
        deployed = deployment_log.get_deployed_artifact("claude-desktop", "default")
        assert deployed == "v2"

    def test_record_deployment_moves_current_to_history(self, deployment_log):
        """Test that new deployment moves current to history."""
        # Record first deployment
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="v1",
            config_path="/path/v1.json"
        )

        # Record second deployment
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="v2",
            config_path="/path/v2.json"
        )

        # Get history (includes current + historical)
        history = deployment_log.get_deployment_history("claude-desktop", "default")

        assert len(history) == 2
        assert history[0].artifact_id == "v2"  # Current (most recent)
        assert history[1].artifact_id == "v1"  # Historical

    def test_record_deployment_limits_history_to_10(self, deployment_log):
        """Test that deployment history is limited to 10 entries."""
        # Record 15 deployments
        for i in range(15):
            deployment_log.record_deployment(
                client_id="claude-desktop",
                profile_id="default",
                artifact_id=f"v{i}",
                config_path=f"/path/v{i}.json"
            )

        # Get history (should include current + 9 historical = 10 total)
        history = deployment_log.get_deployment_history("claude-desktop", "default")

        assert len(history) == 10
        assert history[0].artifact_id == "v14"  # Most recent (current)
        assert history[9].artifact_id == "v5"   # Oldest kept in history

    def test_record_deployment_creates_valid_timestamp(self, deployment_log):
        """Test that deployment record has valid ISO 8601 timestamp."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="abc123",
            config_path="/path/to/config.json"
        )

        history = deployment_log.get_deployment_history("claude-desktop", "default")
        timestamp = history[0].deployed_at

        # Verify ISO 8601 format with Z suffix
        assert timestamp.endswith("Z")
        # Should be parseable
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


class TestGetDeployedArtifact:
    """Test querying currently deployed artifact."""

    def test_get_deployed_artifact_returns_current(self, deployment_log):
        """Test get_deployed_artifact returns current deployment."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="abc123",
            config_path="/path/to/config.json"
        )

        deployed = deployment_log.get_deployed_artifact("claude-desktop", "default")
        assert deployed == "abc123"

    def test_get_deployed_artifact_no_log_returns_none(self, deployment_log):
        """Test get_deployed_artifact returns None when no log exists."""
        deployed = deployment_log.get_deployed_artifact("nonexistent", "profile")
        assert deployed is None

    def test_get_deployed_artifact_empty_current_returns_none(self, deployment_log, tmp_path):
        """Test get_deployed_artifact returns None when current_deployment is None."""
        # Manually create log with null current_deployment
        log_dir = tmp_path / "deployments" / "claude-desktop"
        log_dir.mkdir(parents=True)
        log_file = log_dir / "default.json"

        log_data = {
            "client_id": "claude-desktop",
            "profile_id": "default",
            "current_deployment": None,
            "history": []
        }

        with open(log_file, "w") as f:
            json.dump(log_data, f)

        deployed = deployment_log.get_deployed_artifact("claude-desktop", "default")
        assert deployed is None


class TestGetDeploymentHistory:
    """Test retrieving deployment history."""

    def test_get_deployment_history_returns_all_deployments(self, deployment_log):
        """Test get_deployment_history returns current + historical."""
        # Record 3 deployments
        for i in range(3):
            deployment_log.record_deployment(
                client_id="claude-desktop",
                profile_id="default",
                artifact_id=f"v{i}",
                config_path=f"/path/v{i}.json",
                changelog=f"Version {i}"
            )

        history = deployment_log.get_deployment_history("claude-desktop", "default")

        assert len(history) == 3
        assert all(isinstance(record, DeploymentRecord) for record in history)

    def test_get_deployment_history_most_recent_first(self, deployment_log):
        """Test get_deployment_history returns most recent first."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="v1",
            config_path="/path/v1.json"
        )

        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="v2",
            config_path="/path/v2.json"
        )

        history = deployment_log.get_deployment_history("claude-desktop", "default")

        assert history[0].artifact_id == "v2"  # Most recent
        assert history[1].artifact_id == "v1"  # Older

    def test_get_deployment_history_respects_limit(self, deployment_log):
        """Test get_deployment_history respects limit parameter."""
        # Record 5 deployments
        for i in range(5):
            deployment_log.record_deployment(
                client_id="claude-desktop",
                profile_id="default",
                artifact_id=f"v{i}",
                config_path=f"/path/v{i}.json"
            )

        history = deployment_log.get_deployment_history("claude-desktop", "default", limit=3)

        assert len(history) == 3
        assert history[0].artifact_id == "v4"  # Most recent
        assert history[2].artifact_id == "v2"  # Third most recent

    def test_get_deployment_history_no_log_returns_empty(self, deployment_log):
        """Test get_deployment_history returns empty list when no log exists."""
        history = deployment_log.get_deployment_history("nonexistent", "profile")
        assert history == []

    def test_get_deployment_history_includes_changelog(self, deployment_log):
        """Test get_deployment_history includes changelog in records."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="abc123",
            config_path="/path/to/config.json",
            changelog="Added filesystem and github servers"
        )

        history = deployment_log.get_deployment_history("claude-desktop", "default")

        assert history[0].changelog == "Added filesystem and github servers"


class TestDeploymentRecordModel:
    """Test DeploymentRecord Pydantic model."""

    def test_deployment_record_required_fields(self):
        """Test DeploymentRecord requires artifact_id, config_path, deployed_at."""
        record = DeploymentRecord(
            artifact_id="abc123",
            config_path="/path/to/config.json",
            deployed_at="2025-10-31T12:00:00Z"
        )

        assert record.artifact_id == "abc123"
        assert record.config_path == "/path/to/config.json"
        assert record.deployed_at == "2025-10-31T12:00:00Z"
        assert record.changelog is None

    def test_deployment_record_with_changelog(self):
        """Test DeploymentRecord with optional changelog."""
        record = DeploymentRecord(
            artifact_id="abc123",
            config_path="/path/to/config.json",
            deployed_at="2025-10-31T12:00:00Z",
            changelog="Test changelog"
        )

        assert record.changelog == "Test changelog"


class TestLogFileStructure:
    """Test deployment log file structure and format."""

    def test_log_file_has_correct_structure(self, deployment_log, tmp_path):
        """Test that log file has expected JSON structure."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="abc123",
            config_path="/path/to/config.json"
        )

        log_file = tmp_path / "deployments" / "claude-desktop" / "default.json"
        with open(log_file) as f:
            log_data = json.load(f)

        assert "client_id" in log_data
        assert "profile_id" in log_data
        assert "current_deployment" in log_data
        assert "history" in log_data

        assert log_data["client_id"] == "claude-desktop"
        assert log_data["profile_id"] == "default"
        assert isinstance(log_data["current_deployment"], dict)
        assert isinstance(log_data["history"], list)

    def test_log_file_persists_between_instances(self, tmp_path):
        """Test that log file persists and can be read by new instance."""
        deployments_dir = tmp_path / "deployments"

        # Create first instance and record deployment
        log1 = DeploymentLog(deployments_dir=str(deployments_dir))
        log1.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="abc123",
            config_path="/path/to/config.json"
        )

        # Create second instance and read deployment
        log2 = DeploymentLog(deployments_dir=str(deployments_dir))
        deployed = log2.get_deployed_artifact("claude-desktop", "default")

        assert deployed == "abc123"


class TestMultiClientMultiProfile:
    """Test logging for multiple clients and profiles."""

    def test_separate_logs_for_different_clients(self, deployment_log):
        """Test that different clients have separate logs."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="claude-abc",
            config_path="/path/claude.json"
        )

        deployment_log.record_deployment(
            client_id="cursor",
            profile_id="default",
            artifact_id="cursor-def",
            config_path="/path/cursor.json"
        )

        claude_deployed = deployment_log.get_deployed_artifact("claude-desktop", "default")
        cursor_deployed = deployment_log.get_deployed_artifact("cursor", "default")

        assert claude_deployed == "claude-abc"
        assert cursor_deployed == "cursor-def"

    def test_separate_logs_for_different_profiles(self, deployment_log):
        """Test that different profiles have separate logs."""
        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="default",
            artifact_id="default-abc",
            config_path="/path/default.json"
        )

        deployment_log.record_deployment(
            client_id="claude-desktop",
            profile_id="dev",
            artifact_id="dev-def",
            config_path="/path/dev.json"
        )

        default_deployed = deployment_log.get_deployed_artifact("claude-desktop", "default")
        dev_deployed = deployment_log.get_deployed_artifact("claude-desktop", "dev")

        assert default_deployed == "default-abc"
        assert dev_deployed == "dev-def"
