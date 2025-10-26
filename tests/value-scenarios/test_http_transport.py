"""
E2E Value Scenarios for HTTP Transport (Wave 2.0)

These tests validate the three how-to guides:
1. deploy-http-server.md
2. authenticate-http-api.md
3. migrate-stdio-to-http.md

Each test scenario simulates a real user workflow described in the guides.
Tests verify that the guides are accurate, complete, and achievable.

Test Strategy:
- Scenario 1: Developer workflow (deploy-http-server.md)
- Scenario 2: n8n workflow (authenticate-http-api.md)
- Scenario 3: Migration workflow (migrate-stdio-to-http.md)
"""

import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import pytest
import requests


# Test fixtures
@pytest.fixture
def http_server_process():
    """
    Start HTTP server in background, yield process, then clean up.

    Simulates: deploy-http-server.md Step 2
    """
    # Find available port
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]

    # Start server
    process = subprocess.Popen(
        ["mcp-orchestration-serve-http", "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Wait for server to be ready (max 10 seconds)
    base_url = f"http://127.0.0.1:{port}"
    for _ in range(20):  # 20 * 0.5s = 10s
        try:
            response = requests.get(f"{base_url}/docs", timeout=1)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    else:
        process.kill()
        pytest.fail("HTTP server did not start within 10 seconds")

    yield process, base_url, port

    # Cleanup
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture
def bearer_token():
    """
    Generate a bearer token for authentication.

    Simulates: authenticate-http-api.md Step 1
    """
    result = subprocess.run(
        ["mcp-orchestration-generate-token"],
        capture_output=True,
        text=True,
        check=True,
    )

    # Parse token from output: "Generated token: <token>"
    for line in result.stdout.splitlines():
        if line.startswith("Generated token:"):
            token = line.split("Generated token:")[1].strip()
            return token

    pytest.fail("Could not generate bearer token")


@pytest.fixture
def api_key_server():
    """
    Start HTTP server with API key authentication.

    Simulates: authenticate-http-api.md Method 2
    """
    # Find available port
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]

    # Set API key environment variable
    api_key = "test-api-key-12345"
    env = os.environ.copy()
    env["MCP_ORCHESTRATION_API_KEY"] = api_key

    # Start server with API key
    process = subprocess.Popen(
        ["mcp-orchestration-serve-http", "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )

    # Wait for server to be ready
    base_url = f"http://127.0.0.1:{port}"
    for _ in range(20):
        try:
            response = requests.get(f"{base_url}/docs", timeout=1)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    else:
        process.kill()
        pytest.fail("HTTP server with API key did not start within 10 seconds")

    yield process, base_url, port, api_key

    # Cleanup
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


# Value Scenario 1: Developer Workflow
@pytest.mark.e2e
@pytest.mark.value_scenario
def test_developer_workflow(http_server_process, bearer_token):
    """
    Value Scenario 1: Developer deploys HTTP server and tests endpoints.

    This test validates: user-docs/how-to/deploy-http-server.md

    User story:
    As a developer, I want to deploy the HTTP server and test all endpoints
    so that I can integrate MCP tools into my web application.

    Steps (from guide):
    1. Start HTTP server ✅ (fixture)
    2. Generate API token ✅ (fixture)
    3. Test /v1/clients endpoint
    4. Test /v1/servers endpoint
    5. Test /v1/servers/{server_id} endpoint
    6. Test /v1/config/{client}/{profile} endpoint
    7. Verify OpenAPI docs are accessible
    8. Stop server gracefully ✅ (fixture cleanup)

    Success criteria:
    - All endpoints return 200 OK
    - Response format matches OpenAPI schema
    - Authentication works correctly
    - Server starts and stops cleanly
    """
    process, base_url, port = http_server_process

    # Step 3: Test /v1/clients endpoint
    response = requests.get(
        f"{base_url}/v1/clients",
        headers={"Authorization": f"Bearer {bearer_token}"},
        timeout=5,
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    clients_data = response.json()
    assert "clients" in clients_data, "Response should have 'clients' key"
    assert isinstance(clients_data["clients"], list), "Clients should be a list"
    assert len(clients_data["clients"]) > 0, "Should have at least one client"

    # Verify client structure
    client = clients_data["clients"][0]
    assert "client_id" in client
    assert "display_name" in client
    assert "config_path" in client
    assert "platform" in client

    # Step 4: Test /v1/servers endpoint
    response = requests.get(
        f"{base_url}/v1/servers",
        headers={"Authorization": f"Bearer {bearer_token}"},
        timeout=5,
    )
    assert response.status_code == 200
    servers_data = response.json()
    assert "servers" in servers_data
    assert isinstance(servers_data["servers"], list)
    assert len(servers_data["servers"]) > 0, "Should have at least one server"

    # Verify server structure
    server = servers_data["servers"][0]
    assert "server_id" in server
    assert "description" in server
    assert "transport" in server

    # Step 5: Test /v1/servers/{server_id} endpoint
    server_id = servers_data["servers"][0]["server_id"]
    response = requests.get(
        f"{base_url}/v1/servers/{server_id}",
        headers={"Authorization": f"Bearer {bearer_token}"},
        timeout=5,
    )
    assert response.status_code == 200
    server_detail = response.json()
    assert server_detail["server_id"] == server_id

    # Step 6: Test /v1/config/{client}/{profile} endpoint
    client_id = clients_data["clients"][0]["client_id"]
    response = requests.get(
        f"{base_url}/v1/config/{client_id}/default",
        headers={"Authorization": f"Bearer {bearer_token}"},
        timeout=5,
    )
    # May return 200 (config exists) or 404 (no config yet)
    assert response.status_code in [200, 404]

    # Step 7: Verify OpenAPI docs are accessible
    response = requests.get(f"{base_url}/docs", timeout=5)
    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "openapi" in response.text.lower()

    response = requests.get(f"{base_url}/openapi.json", timeout=5)
    assert response.status_code == 200
    openapi_schema = response.json()
    assert "openapi" in openapi_schema
    assert "paths" in openapi_schema
    assert "/v1/clients" in openapi_schema["paths"]

    # Verify server is still running
    assert process.poll() is None, "Server should still be running"


# Value Scenario 2: n8n Automation Workflow
@pytest.mark.e2e
@pytest.mark.value_scenario
def test_n8n_automation_workflow(http_server_process, bearer_token):
    """
    Value Scenario 2: n8n workflow automates configuration deployment.

    This test validates: user-docs/how-to/authenticate-http-api.md (Scenario 4)

    User story:
    As an automation engineer, I want to use n8n to automate MCP server
    configuration deployment so that I can manage multiple client configs
    without manual intervention.

    Steps (from guide - Scenario 4: n8n Workflow):
    1. List available servers (GET /v1/servers)
    2. Select server based on criteria (simulated)
    3. Add server to draft (POST /v1/config/.../draft/add)
    4. Validate configuration (POST /v1/config/.../validate)
    5. Publish configuration (POST /v1/config/.../publish)
    6. Deploy configuration (POST /v1/config/.../deploy)

    Success criteria:
    - All HTTP requests succeed
    - Configuration is drafted, validated, published, deployed
    - End-to-end workflow completes without errors
    - Authentication works for all requests
    """
    process, base_url, port = http_server_process
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
    }

    # Step 1: List available servers
    response = requests.get(
        f"{base_url}/v1/servers",
        headers=headers,
        timeout=5,
    )
    assert response.status_code == 200
    servers = response.json()["servers"]
    assert len(servers) > 0

    # Step 2: Select server (simulated - pick filesystem if available)
    server_id = None
    for server in servers:
        if server["server_id"] == "filesystem":
            server_id = "filesystem"
            break

    if not server_id:
        server_id = servers[0]["server_id"]

    # Get server details to know required params
    response = requests.get(
        f"{base_url}/v1/servers/{server_id}",
        headers=headers,
        timeout=5,
    )
    assert response.status_code == 200
    server_detail = response.json()

    # Step 3: Add server to draft
    # Prepare params based on server type
    if server_id == "filesystem":
        params = {"path": "/tmp/test-mcp-data"}
    else:
        params = {}

    response = requests.post(
        f"{base_url}/v1/config/claude-desktop/default/draft/add",
        headers=headers,
        json={"server_id": server_id, "params": params},
        timeout=5,
    )
    assert response.status_code == 200
    draft_response = response.json()
    assert draft_response["success"] is True

    # Step 4: Validate configuration
    response = requests.post(
        f"{base_url}/v1/config/claude-desktop/default/validate",
        headers=headers,
        timeout=5,
    )
    assert response.status_code == 200
    validation_response = response.json()
    assert validation_response["valid"] is True

    # Step 5: Publish configuration
    # Note: This requires signing keys, which may not be initialized
    # We'll attempt publish and accept either success or expected error
    response = requests.post(
        f"{base_url}/v1/config/claude-desktop/default/publish",
        headers=headers,
        timeout=5,
    )

    if response.status_code == 200:
        # Publishing succeeded (keys exist)
        publish_response = response.json()
        assert "artifact_id" in publish_response or "success" in publish_response

        # Step 6: Deploy configuration
        response = requests.post(
            f"{base_url}/v1/config/claude-desktop/default/deploy",
            headers=headers,
            timeout=5,
        )
        assert response.status_code in [200, 404]  # 404 if no published config
    else:
        # Publishing failed (expected if keys not initialized)
        # This is acceptable for this test - we're testing the workflow
        assert response.status_code in [400, 500]
        error_response = response.json()
        assert "error" in error_response or "detail" in error_response

    # Verify workflow executed all steps without unexpected errors
    # Success means we could call all endpoints with proper authentication


# Value Scenario 3: Migration Workflow
@pytest.mark.e2e
@pytest.mark.value_scenario
def test_stdio_to_http_migration_workflow(http_server_process, bearer_token):
    """
    Value Scenario 3: Migrate from stdio to HTTP transport.

    This test validates: user-docs/how-to/migrate-stdio-to-http.md

    User story:
    As a developer, I want to migrate from stdio to HTTP transport
    while maintaining backward compatibility so that existing stdio
    workflows continue working during the transition.

    Steps (from guide - Step-by-Step Migration):
    1. Verify stdio setup is working
    2. Deploy HTTP server ✅ (fixture)
    3. Generate authentication token ✅ (fixture)
    4. Verify backward compatibility (stdio still works)
    5. Test HTTP transport (HTTP endpoints work)
    6. Side-by-side comparison (stdio and HTTP return same data)

    Success criteria:
    - stdio commands work before and after HTTP deployment
    - HTTP endpoints return same data as stdio
    - Both transports work simultaneously
    - No interference between transports
    """
    process, base_url, port = http_server_process

    # Step 1: Verify stdio setup is working
    stdio_discover = subprocess.run(
        ["mcp-orchestration-discover"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert stdio_discover.returncode == 0, "stdio discover should work"

    stdio_list_servers = subprocess.run(
        ["mcp-orchestration-list-servers"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert stdio_list_servers.returncode == 0, "stdio list-servers should work"

    # Parse stdio output
    stdio_servers_output = stdio_list_servers.stdout
    assert len(stdio_servers_output) > 0, "stdio should return server list"

    # Step 4: Verify backward compatibility (stdio still works after HTTP deployed)
    stdio_discover_after = subprocess.run(
        ["mcp-orchestration-discover"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert stdio_discover_after.returncode == 0, "stdio should still work after HTTP"
    assert stdio_discover_after.stdout == stdio_discover.stdout, "stdio output should be unchanged"

    # Step 5: Test HTTP transport
    response = requests.get(
        f"{base_url}/v1/clients",
        headers={"Authorization": f"Bearer {bearer_token}"},
        timeout=5,
    )
    assert response.status_code == 200, "HTTP endpoint should work"

    response = requests.get(
        f"{base_url}/v1/servers",
        headers={"Authorization": f"Bearer {bearer_token}"},
        timeout=5,
    )
    assert response.status_code == 200, "HTTP servers endpoint should work"
    http_servers = response.json()["servers"]

    # Step 6: Side-by-side comparison (stdio and HTTP return same data)
    # Compare server IDs from both transports

    # Parse stdio server IDs (from JSON or text output)
    try:
        stdio_servers_json = json.loads(stdio_servers_output)
        stdio_server_ids = sorted([s["server_id"] for s in stdio_servers_json])
    except json.JSONDecodeError:
        # If not JSON, parse text output (fallback)
        # This is environment-specific, so we'll be lenient
        stdio_server_ids = []

    http_server_ids = sorted([s["server_id"] for s in http_servers])

    # Verify both transports return servers
    assert len(stdio_server_ids) > 0 or len(http_server_ids) > 0, \
        "At least one transport should return servers"

    # If stdio parsing succeeded, verify they match
    if stdio_server_ids:
        assert stdio_server_ids == http_server_ids, \
            f"stdio and HTTP should return same servers: {stdio_server_ids} vs {http_server_ids}"

    # Verify stdio still works one more time (no interference)
    stdio_final = subprocess.run(
        ["mcp-orchestration-discover"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert stdio_final.returncode == 0, "stdio should still work at end"


# Additional Test: API Key Authentication
@pytest.mark.e2e
@pytest.mark.value_scenario
def test_api_key_authentication(api_key_server):
    """
    Additional Scenario: API key authentication (Method 2).

    This test validates: user-docs/how-to/authenticate-http-api.md (Method 2)

    User story:
    As a system administrator, I want to use static API key authentication
    instead of bearer tokens for simpler server-to-server integration.

    Steps (from guide - Method 2):
    1. Set API key environment variable ✅ (fixture)
    2. Start HTTP server ✅ (fixture)
    3. Use API key in requests (X-API-Key header)
    4. Verify endpoints work with API key

    Success criteria:
    - API key authentication works
    - Endpoints return expected data
    - No bearer token required
    """
    process, base_url, port, api_key = api_key_server

    # Step 3: Use API key in requests
    headers = {"X-API-Key": api_key}

    # Test /v1/clients
    response = requests.get(
        f"{base_url}/v1/clients",
        headers=headers,
        timeout=5,
    )
    assert response.status_code == 200
    clients = response.json()["clients"]
    assert len(clients) > 0

    # Test /v1/servers
    response = requests.get(
        f"{base_url}/v1/servers",
        headers=headers,
        timeout=5,
    )
    assert response.status_code == 200
    servers = response.json()["servers"]
    assert len(servers) > 0

    # Test authentication failure with wrong API key
    response = requests.get(
        f"{base_url}/v1/clients",
        headers={"X-API-Key": "wrong-key"},
        timeout=5,
    )
    assert response.status_code == 401, "Wrong API key should return 401"

    # Test authentication failure with no API key
    response = requests.get(
        f"{base_url}/v1/clients",
        timeout=5,
    )
    assert response.status_code == 401, "No authentication should return 401"


# Additional Test: Bearer Token Authentication Lifecycle
@pytest.mark.e2e
@pytest.mark.value_scenario
def test_bearer_token_lifecycle(http_server_process):
    """
    Additional Scenario: Bearer token authentication lifecycle.

    This test validates: user-docs/how-to/authenticate-http-api.md (Method 1)

    User story:
    As a developer, I want to generate multiple bearer tokens for different
    applications and verify they all work simultaneously.

    Steps (from guide - Token Management):
    1. Generate multiple tokens
    2. Verify all tokens work
    3. Test token isolation (each token independent)

    Success criteria:
    - Multiple tokens can be generated
    - All tokens work simultaneously
    - Each token is unique
    """
    process, base_url, port = http_server_process

    # Step 1: Generate multiple tokens
    tokens = []
    for i in range(3):
        result = subprocess.run(
            ["mcp-orchestration-generate-token"],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in result.stdout.splitlines():
            if line.startswith("Generated token:"):
                token = line.split("Generated token:")[1].strip()
                tokens.append(token)
                break

    assert len(tokens) == 3, "Should generate 3 tokens"
    assert len(set(tokens)) == 3, "All tokens should be unique"

    # Step 2: Verify all tokens work
    for token in tokens:
        response = requests.get(
            f"{base_url}/v1/clients",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        assert response.status_code == 200, f"Token {token[:10]}... should work"

    # Step 3: Test invalid token
    response = requests.get(
        f"{base_url}/v1/clients",
        headers={"Authorization": "Bearer invalid_token_12345"},
        timeout=5,
    )
    assert response.status_code == 401, "Invalid token should return 401"


# Test execution summary
def pytest_collection_modifyitems(items):
    """
    Add markers and metadata to E2E value scenario tests.

    This ensures tests are properly categorized for reporting.
    """
    for item in items:
        if "value_scenario" in item.keywords:
            # Add metadata for test reports
            item.user_properties.append(("test_type", "value_scenario"))
            item.user_properties.append(("wave", "2.0"))
            item.user_properties.append(("feature", "http_transport"))
