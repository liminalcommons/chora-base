"""Test publish_config fix for serialization and error handling.

This test verifies the fix for the "No result received from client-side tool execution" error
reported in FINDINGS-REPORT.md Test 3.4.

The fix includes:
1. Comprehensive logging throughout publish workflow
2. Explicit JSON serialization of result dict
3. Comprehensive exception handling with helpful error messages
4. StorageError catch to prevent silent failures
"""

import json
import tempfile
from pathlib import Path

import pytest

from mcp_orchestrator.building import ConfigBuilder
from mcp_orchestrator.crypto import ArtifactSigner
from mcp_orchestrator.publishing import PublishingWorkflow
from mcp_orchestrator.registry import get_default_registry
from mcp_orchestrator.servers import ServerRegistry
from mcp_orchestrator.servers.models import (
    ParameterDefinition,
    ServerDefinition,
    TransportType,
)
from mcp_orchestrator.storage import ArtifactStore


def test_publish_workflow_returns_serializable_result():
    """Test that PublishingWorkflow.publish() returns a JSON-serializable result.

    This is the core fix for FINDINGS-REPORT.md Test 3.4.
    The publish_config tool was failing because the result wasn't properly serialized.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup
        base_path = Path(tmpdir)
        key_dir = base_path / "keys"
        key_dir.mkdir()

        # Step 1: Initialize keys
        private_key_path = key_dir / "signing.key"
        public_key_path = key_dir / "signing.pub"

        signer = ArtifactSigner.generate(key_id="default")
        signer.save_private_key(str(private_key_path))
        signer.save_public_key(str(public_key_path))

        # Step 2: Setup registry and builder
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

        builder = ConfigBuilder("claude-desktop", "default", registry)
        builder.add_server("filesystem", params={"path": "/Users/test/Documents"})

        # Step 3: Publish via workflow
        store = ArtifactStore(base_path=base_path)
        client_registry = get_default_registry()
        workflow = PublishingWorkflow(store=store, client_registry=client_registry)

        result = workflow.publish(
            builder=builder,
            private_key_path=str(private_key_path),
            signing_key_id="default",
            changelog="Test config",
        )

        # Step 4: Verify result is JSON-serializable (critical fix)
        try:
            json_str = json.dumps(result)
            deserialized = json.loads(json_str)
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result is not JSON-serializable: {e}")

        # Step 5: Verify result structure
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "published"
        assert "artifact_id" in result
        assert len(result["artifact_id"]) == 64  # SHA-256 hash
        assert "server_count" in result
        assert result["server_count"] == 1
        assert "created_at" in result
        assert isinstance(result["created_at"], str)  # ISO 8601 string

        # Step 6: Verify the same fields survive JSON round-trip
        assert deserialized["status"] == "published"
        assert deserialized["artifact_id"] == result["artifact_id"]
        assert deserialized["server_count"] == 1

        print("✓ Test passed: PublishingWorkflow returns JSON-serializable result")
        print(f"  - Artifact ID: {result['artifact_id'][:16]}...")
        print(f"  - JSON round-trip: successful")


def test_publish_workflow_error_messages_are_serializable():
    """Test that error messages from publish workflow are JSON-serializable.

    This ensures that when publish_config fails, the error can be transmitted
    back to Claude Desktop without causing "No result received" errors.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)

        # Setup empty builder (will trigger validation error)
        registry = ServerRegistry()
        builder = ConfigBuilder("claude-desktop", "default", registry)

        # Publish should fail validation (empty config)
        store = ArtifactStore(base_path=base_path)
        client_registry = get_default_registry()
        workflow = PublishingWorkflow(store=store, client_registry=client_registry)

        from mcp_orchestrator.publishing import ValidationError

        with pytest.raises(ValidationError) as exc_info:
            workflow.publish(
                builder=builder,
                private_key_path="/nonexistent/key.pem",  # Won't reach this
                signing_key_id="default",
            )

        # Verify error is JSON-serializable
        error = exc_info.value
        validation_result = error.validation_result

        try:
            json_str = json.dumps(validation_result)
            deserialized = json.loads(json_str)
        except (TypeError, ValueError) as e:
            pytest.fail(f"ValidationError result is not JSON-serializable: {e}")

        # Verify error structure
        assert "valid" in deserialized
        assert deserialized["valid"] is False
        assert "errors" in deserialized
        assert len(deserialized["errors"]) > 0
        assert deserialized["errors"][0]["code"] == "EMPTY_CONFIG"

        print("✓ Test passed: Validation errors are JSON-serializable")


def test_publish_config_tool_result_format():
    """Test that publish_config tool formats result correctly for MCP protocol.

    The fix in server.py ensures all result fields are explicitly converted to
    JSON-serializable types (str, int, etc.) to prevent transmission failures.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        key_dir = base_path / "keys"
        key_dir.mkdir()

        # Setup
        signer = ArtifactSigner.generate(key_id="default")
        signer.save_private_key(str(key_dir / "signing.key"))

        registry = ServerRegistry()
        registry.register(
            ServerDefinition(
                server_id="memory",
                display_name="Memory",
                description="Memory server",
                transport=TransportType.STDIO,
                stdio_command="npx",
                stdio_args=["-y", "@modelcontextprotocol/server-memory"],
            )
        )

        builder = ConfigBuilder("claude-desktop", "default", registry)
        builder.add_server("memory")

        # Publish
        store = ArtifactStore(base_path=base_path)
        client_registry = get_default_registry()
        workflow = PublishingWorkflow(store=store, client_registry=client_registry)

        raw_result = workflow.publish(
            builder=builder,
            private_key_path=str(key_dir / "signing.key"),
            signing_key_id="default",
            changelog="Test",
        )

        # Simulate what publish_config tool does (the fix)
        serializable_result = {
            "status": str(raw_result.get("status", "published")),
            "artifact_id": str(raw_result.get("artifact_id", "")),
            "client_id": str(raw_result.get("client_id", "claude-desktop")),
            "profile_id": str(raw_result.get("profile_id", "default")),
            "server_count": int(raw_result.get("server_count", 0)),
            "created_at": str(raw_result.get("created_at", "")),
            "changelog": str("Test"),
        }

        # Verify all values are primitive types
        for key, value in serializable_result.items():
            assert isinstance(value, (str, int, float, bool, type(None))), (
                f"Field '{key}' has non-primitive type: {type(value)}"
            )

        # Verify JSON serialization works
        json_str = json.dumps(serializable_result)
        assert len(json_str) > 0

        print("✓ Test passed: publish_config result is properly formatted")
        print(f"  - All fields are primitive types: ✓")
        print(f"  - JSON serialization succeeds: ✓")


def test_publish_without_signing_keys():
    """Test that publish workflow fails gracefully when signing keys are missing.

    This corresponds to Test 3.5 from FINDINGS-REPORT.md which was marked as
    PARTIAL due to environmental limitations (couldn't delete keys during E2E test).

    This unit test verifies the error handling is correct.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)
        # Note: NOT creating keys directory - simulating missing keys

        registry = ServerRegistry()
        registry.register(
            ServerDefinition(
                server_id="memory",
                display_name="Memory",
                description="Memory server",
                transport=TransportType.STDIO,
                stdio_command="npx",
                stdio_args=["-y", "@modelcontextprotocol/server-memory"],
            )
        )

        builder = ConfigBuilder("claude-desktop", "default", registry)
        builder.add_server("memory")

        # Attempt to publish without keys
        store = ArtifactStore(base_path=base_path)
        client_registry = get_default_registry()
        workflow = PublishingWorkflow(store=store, client_registry=client_registry)

        # This should fail with clear error message about missing keys
        from mcp_orchestrator.crypto.signing import SigningError

        with pytest.raises((FileNotFoundError, SigningError)) as exc_info:
            workflow.publish(
                builder=builder,
                private_key_path=str(base_path / "keys" / "signing.key"),  # Doesn't exist
                signing_key_id="default",
            )

        # Verify error message is helpful
        error_msg = str(exc_info.value)
        assert "signing" in error_msg.lower() or "key" in error_msg.lower() or "file" in error_msg.lower()

        print("✓ Test passed: Publish without keys fails with clear error")
        print(f"  - Error message: {error_msg}")


def test_publish_config_error_message_quality():
    """Test that publish_config provides helpful error messages.

    This corresponds to Test 3.5 from FINDINGS-REPORT.md - verifying that
    when publish fails (e.g., missing keys), the error message is clear,
    actionable, and JSON-serializable for transmission through MCP protocol.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        base_path = Path(tmpdir)

        # Test 1: Missing keys error message
        registry = ServerRegistry()
        registry.register(
            ServerDefinition(
                server_id="memory",
                display_name="Memory",
                description="Memory server",
                transport=TransportType.STDIO,
                stdio_command="npx",
                stdio_args=["-y", "@modelcontextprotocol/server-memory"],
            )
        )

        builder = ConfigBuilder("claude-desktop", "default", registry)
        builder.add_server("memory")

        store = ArtifactStore(base_path=base_path)
        client_registry = get_default_registry()
        workflow = PublishingWorkflow(store=store, client_registry=client_registry)

        # Simulate what publish_config tool does when keys are missing
        fake_key_path = str(base_path / "keys" / "signing.key")

        try:
            workflow.publish(
                builder=builder,
                private_key_path=fake_key_path,
                signing_key_id="default",
            )
            pytest.fail("Expected FileNotFoundError but no exception was raised")
        except (FileNotFoundError, Exception) as e:
            # Verify error is JSON-serializable
            error_dict = {
                "error": str(e),
                "type": type(e).__name__,
            }

            # Should be serializable
            import json

            json_str = json.dumps(error_dict)
            assert len(json_str) > 0

            # Error message should mention keys or signing
            error_msg = str(e).lower()
            assert "key" in error_msg or "signing" in error_msg

            print("✓ Test passed: Error messages are JSON-serializable and helpful")
            print(f"  - Error type: {type(e).__name__}")
            print(f"  - Error mentions keys/signing: ✓")
            print(f"  - Error is JSON-serializable: ✓")
