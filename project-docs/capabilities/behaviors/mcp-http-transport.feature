Feature: HTTP/SSE Transport for MCP Tools
  As a developer, automation engineer, or web application
  I want to access MCP orchestration tools via HTTP API
  So that I can integrate with remote systems, workflows, and web clients

  Background:
    Given mcp-orchestration is installed with version 0.2.0 or higher
    And the HTTP transport module is available

  # ============================================================================
  # @behavior:http-transport-expose
  # All 10 MCP tools accessible via HTTP endpoints
  # ============================================================================

  @behavior:http-transport-expose @status:planned @priority:high
  Scenario: Access list_clients via HTTP GET
    Given the HTTP server is running on port 8000
    And I have a valid bearer token "test_token_123"
    When I send GET request to "http://localhost:8000/v1/clients"
    And I include header "Authorization: Bearer test_token_123"
    Then I receive HTTP status 200 OK
    And the response Content-Type is "application/json"
    And the response body contains a list of clients
    And each client has fields: client_id, display_name, config_path

  @behavior:http-transport-expose @status:planned @priority:high
  Scenario: Access get_config via HTTP GET
    Given the HTTP server is running
    And I have a valid bearer token
    And a config exists for client "claude-desktop" profile "default"
    When I send GET to "/v1/config/claude-desktop/default"
    And I include Authorization header with bearer token
    Then I receive HTTP status 200 OK
    And the response contains the config artifact
    And the artifact has fields: artifact_id, payload, signature, metadata

  @behavior:http-transport-expose @status:planned @priority:high
  Scenario: Create draft config via HTTP POST
    Given the HTTP server is running
    And I have a valid bearer token
    When I send POST to "/v1/config/claude-desktop/default/draft/add"
    And I include Authorization header
    And I include JSON body:
      """
      {
        "server_id": "filesystem",
        "params": {"path": "/Users/test/Documents"}
      }
      """
    Then I receive HTTP status 200 OK
    And the response contains: status = "added"
    And the response contains: server_count = 1

  @behavior:http-transport-expose @status:planned @priority:high
  Scenario: Validate config via HTTP POST
    Given the HTTP server is running
    And I have a valid bearer token
    And a draft config exists with 2 servers
    When I send POST to "/v1/config/claude-desktop/default/validate"
    And I include Authorization header
    Then I receive HTTP status 200 OK
    And the response contains: valid = true
    And the response contains: errors = []
    And the response contains: server_count = 2

  @behavior:http-transport-expose @status:planned @priority:high
  Scenario: Publish config via HTTP POST
    Given the HTTP server is running
    And I have a valid bearer token
    And signing keys are initialized
    And a valid draft config exists
    When I send POST to "/v1/config/claude-desktop/default/publish"
    And I include Authorization header
    And I include JSON body:
      """
      {
        "changelog": "Test configuration"
      }
      """
    Then I receive HTTP status 200 OK
    And the response contains: status = "published"
    And the response contains a valid artifact_id (64 character SHA-256)
    And the response contains: created_at (ISO 8601 timestamp)

  @behavior:http-transport-expose @status:planned @priority:high
  Scenario: Deploy config via HTTP POST
    Given the HTTP server is running
    And I have a valid bearer token
    And a published config exists for "claude-desktop/default"
    When I send POST to "/v1/config/claude-desktop/default/deploy"
    And I include Authorization header
    Then I receive HTTP status 200 OK
    And the response contains: status = "deployed"
    And the response contains: config_path
    And the config file is written to the client's config location

  @behavior:http-transport-expose @status:planned @priority:medium
  Scenario: List available servers via HTTP GET
    Given the HTTP server is running
    And I have a valid bearer token
    When I send GET to "/v1/servers"
    And I include Authorization header
    Then I receive HTTP status 200 OK
    And the response contains a list of available MCP servers
    And each server has fields: server_id, display_name, description, transport

  @behavior:http-transport-expose @status:planned @priority:medium
  Scenario: Get server details via HTTP GET
    Given the HTTP server is running
    And I have a valid bearer token
    When I send GET to "/v1/servers/filesystem"
    And I include Authorization header
    Then I receive HTTP status 200 OK
    And the response contains server details for "filesystem"
    And the details include: command, args, parameters, documentation_url

  @behavior:http-transport-expose @status:planned @priority:low
  Scenario: Initialize keys via HTTP POST
    Given the HTTP server is running
    And I have a valid bearer token
    And signing keys do not exist
    When I send POST to "/v1/keys/initialize"
    And I include Authorization header
    Then I receive HTTP status 200 OK
    And the response contains: status = "initialized"
    And signing keys are created in ~/.mcp-orchestration/keys/

  # ============================================================================
  # @behavior:http-transport-auth
  # Bearer token and API key authentication enforced
  # ============================================================================

  @behavior:http-transport-auth @status:planned @priority:critical
  Scenario: Reject request without authentication
    Given the HTTP server is running
    When I send GET to "/v1/clients"
    And I do NOT include an Authorization header
    Then I receive HTTP status 401 Unauthorized
    And the response contains error: "Authentication required"
    And the response suggests using "Authorization: Bearer <token>"

  @behavior:http-transport-auth @status:planned @priority:critical
  Scenario: Reject request with invalid bearer token
    Given the HTTP server is running
    When I send GET to "/v1/clients"
    And I include header "Authorization: Bearer invalid_token_xyz"
    Then I receive HTTP status 401 Unauthorized
    And the response contains error: "Invalid authentication credentials"

  @behavior:http-transport-auth @status:planned @priority:high
  Scenario: Accept request with valid bearer token
    Given the HTTP server is running
    And a bearer token "valid_token_abc123" exists in the token store
    When I send GET to "/v1/clients"
    And I include header "Authorization: Bearer valid_token_abc123"
    Then I receive HTTP status 200 OK
    And the request is authenticated successfully
    And the token usage count is incremented

  @behavior:http-transport-auth @status:planned @priority:high
  Scenario: Accept request with valid API key
    Given the HTTP server is running
    And environment variable MCP_ORCHESTRATION_API_KEY is set to "api_key_xyz"
    When I send GET to "/v1/clients"
    And I include header "X-API-Key: api_key_xyz"
    Then I receive HTTP status 200 OK
    And the request is authenticated successfully

  @behavior:http-transport-auth @status:planned @priority:medium
  Scenario: Reject request with invalid API key
    Given the HTTP server is running
    And environment variable MCP_ORCHESTRATION_API_KEY is set to "api_key_xyz"
    When I send GET to "/v1/clients"
    And I include header "X-API-Key: wrong_api_key"
    Then I receive HTTP status 401 Unauthorized
    And the response contains error: "Invalid authentication credentials"

  @behavior:http-transport-auth @status:planned @priority:medium
  Scenario: Track token usage metadata
    Given the HTTP server is running
    And a bearer token "tracked_token" was created at "2025-10-26T10:00:00Z"
    And the token has usage_count = 0
    When I send GET to "/v1/clients" with "Authorization: Bearer tracked_token"
    Then I receive HTTP status 200 OK
    And the token's last_used timestamp is updated
    And the token's usage_count is incremented to 1

  # ============================================================================
  # @behavior:http-transport-token-generate
  # Generate new API tokens
  # ============================================================================

  @behavior:http-transport-token-generate @status:planned @priority:high
  Scenario: Generate new API token via CLI
    Given mcp-orchestration is installed
    When I run command "mcp-orchestration-generate-token"
    Then the command exits with status 0
    And a new bearer token is printed to stdout
    And the token is 43 characters long (base64-encoded 32 bytes)
    And the token is stored in the token store
    And the output includes usage instructions

  @behavior:http-transport-token-generate @status:planned @priority:medium
  Scenario: Generate multiple tokens
    Given the token store is empty
    When I run "mcp-orchestration-generate-token" 3 times
    Then 3 different tokens are generated
    And all 3 tokens are valid for authentication
    And all 3 tokens are stored in the token store

  @behavior:http-transport-token-generate @status:planned @priority:low
  Scenario: Token generation is cryptographically secure
    Given I run "mcp-orchestration-generate-token"
    When I inspect the generated token
    Then the token uses secrets.token_urlsafe (not random.random)
    And the token has sufficient entropy (>= 256 bits)
    And the collision probability is negligible

  # ============================================================================
  # @behavior:http-transport-cors
  # CORS configured for web client access
  # ============================================================================

  @behavior:http-transport-cors @status:planned @priority:high
  Scenario: CORS preflight request succeeds
    Given the HTTP server is running
    When I send OPTIONS to "/v1/clients"
    And I include header "Origin: https://app.example.com"
    And I include header "Access-Control-Request-Method: GET"
    Then I receive HTTP status 200 OK
    And response includes header "Access-Control-Allow-Origin: *"
    And response includes header "Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS"
    And response includes header "Access-Control-Allow-Headers: *"
    And response includes header "Access-Control-Allow-Credentials: true"

  @behavior:http-transport-cors @status:planned @priority:high
  Scenario: Actual request includes CORS headers
    Given the HTTP server is running
    And I have a valid bearer token
    When I send GET to "/v1/clients" from origin "https://app.example.com"
    And I include Authorization header
    Then I receive HTTP status 200 OK
    And response includes header "Access-Control-Allow-Origin: *"
    And the response body is returned successfully

  @behavior:http-transport-cors @status:planned @priority:medium
  Scenario: CORS works with POST requests
    Given the HTTP server is running
    And I have a valid bearer token
    When I send POST to "/v1/config/claude-desktop/default/validate"
    And I include header "Origin: https://app.example.com"
    And I include Authorization header
    Then I receive HTTP status 200 OK
    And response includes CORS headers
    And the POST operation completes successfully

  # ============================================================================
  # @behavior:http-transport-backward-compat
  # stdio transport continues to work (no breaking changes)
  # ============================================================================

  @behavior:http-transport-backward-compat @status:planned @priority:critical
  Scenario: stdio transport still works after HTTP module added
    Given mcp-orchestration 0.2.0 is installed
    And the HTTP server is NOT running
    And Claude Desktop is configured to use stdio transport
    When Claude Desktop connects via stdio
    Then all 10 MCP tools work via stdio
    And no functionality is broken
    And no errors occur

  @behavior:http-transport-backward-compat @status:planned @priority:critical
  Scenario: HTTP server is opt-in, not started by default
    Given mcp-orchestration 0.2.0 is installed
    And I have NOT run "mcp-orchestration-serve-http"
    When I use mcp-orchestration via stdio
    Then the HTTP server is NOT listening on any port
    And no HTTP-related processes are running
    And the system behaves exactly like version 0.1.5

  @behavior:http-transport-backward-compat @status:planned @priority:high
  Scenario: Both stdio and HTTP transports work simultaneously
    Given mcp-orchestration 0.2.0 is installed
    And the HTTP server is running on port 8000
    And Claude Desktop is connected via stdio
    When I call list_clients via stdio
    And I call list_clients via HTTP at the same time
    Then both calls succeed
    And both return the same data
    And there is no interference between transports

  @behavior:http-transport-backward-compat @status:planned @priority:high
  Scenario: Existing configurations continue to work
    Given I have an existing Claude Desktop config for stdio transport
    When I upgrade to mcp-orchestration 0.2.0
    Then my existing config still works
    And I do not need to change anything
    And stdio transport functions identically to 0.1.5

  # ============================================================================
  # @behavior:http-transport-lifecycle
  # Start and stop HTTP server gracefully
  # ============================================================================

  @behavior:http-transport-lifecycle @status:planned @priority:high
  Scenario: Start HTTP server successfully
    Given mcp-orchestration 0.2.0 is installed
    When I run "mcp-orchestration-serve-http --port 8000"
    Then the server starts within 5 seconds
    And the server logs "Server running on http://0.0.0.0:8000"
    And the server logs "API docs: http://0.0.0.0:8000/docs"
    And the server is accepting connections

  @behavior:http-transport-lifecycle @status:planned @priority:high
  Scenario: Server responds to health check
    Given the HTTP server is running on port 8000
    When I send GET to "http://localhost:8000/health" (if health endpoint exists)
    Then I receive HTTP status 200 OK
    And the response contains: status = "healthy"

  @behavior:http-transport-lifecycle @status:planned @priority:high
  Scenario: Graceful shutdown on SIGINT
    Given the HTTP server is running
    And there is 1 in-flight request
    When I send SIGINT (Ctrl+C) to the server process
    Then the server logs "Shutting down gracefully..."
    And the in-flight request completes successfully
    And the server stops within 5 seconds
    And the server logs "Server shut down gracefully"

  @behavior:http-transport-lifecycle @status:planned @priority:medium
  Scenario: Customize server host and port
    Given mcp-orchestration is installed
    When I run "mcp-orchestration-serve-http --host 127.0.0.1 --port 9000"
    Then the server starts on 127.0.0.1:9000
    And requests to localhost:9000 succeed
    And requests to 0.0.0.0:9000 fail (not listening on all interfaces)

  @behavior:http-transport-lifecycle @status:planned @priority:medium
  Scenario: Configure log level
    Given mcp-orchestration is installed
    When I run "mcp-orchestration-serve-http --log-level debug"
    Then the server starts with DEBUG log level
    And detailed request logs are printed
    And debug messages are visible in output

  @behavior:http-transport-lifecycle @status:planned @priority:low
  Scenario: Handle port already in use
    Given the HTTP server is running on port 8000
    When I try to start another server on port 8000
    Then the second server fails to start
    And the error message says "Address already in use"
    And the first server continues running

  # ============================================================================
  # Error Handling Scenarios
  # ============================================================================

  @behavior:http-transport-expose @status:planned @priority:medium
  Scenario: Handle invalid JSON in POST body
    Given the HTTP server is running
    And I have a valid bearer token
    When I send POST to "/v1/config/claude-desktop/default/draft/add"
    And I include Authorization header
    And I include invalid JSON in body: "{ invalid json }"
    Then I receive HTTP status 400 Bad Request
    And the response contains error: "Invalid JSON"

  @behavior:http-transport-expose @status:planned @priority:medium
  Scenario: Handle missing required parameters
    Given the HTTP server is running
    And I have a valid bearer token
    When I send POST to "/v1/config/claude-desktop/default/draft/add"
    And I include Authorization header
    And I include JSON body: "{}" (missing server_id)
    Then I receive HTTP status 400 Bad Request
    And the response contains error about missing "server_id"

  @behavior:http-transport-expose @status:planned @priority:medium
  Scenario: Handle non-existent resource
    Given the HTTP server is running
    And I have a valid bearer token
    When I send GET to "/v1/config/nonexistent-client/nonexistent-profile"
    And I include Authorization header
    Then I receive HTTP status 404 Not Found
    And the response contains error: "Client not found"

  @behavior:http-transport-expose @status:planned @priority:medium
  Scenario: Handle validation errors in publish
    Given the HTTP server is running
    And I have a valid bearer token
    And a draft config exists with validation errors
    When I send POST to "/v1/config/claude-desktop/default/publish"
    And I include Authorization header
    Then I receive HTTP status 400 Bad Request
    And the response contains validation error details
    And the response includes error code and field information

  # ============================================================================
  # Performance Scenarios
  # ============================================================================

  @behavior:http-transport-expose @status:planned @priority:medium @nfr:performance
  Scenario: p95 latency under 300ms for GET requests
    Given the HTTP server is running
    And I have a valid bearer token
    When I send 1000 GET requests to "/v1/clients"
    And I measure response times
    Then the p95 latency is less than 300ms
    And the p99 latency is less than 500ms

  @behavior:http-transport-expose @status:planned @priority:medium @nfr:performance
  Scenario: Handle 100 concurrent requests
    Given the HTTP server is running
    And I have a valid bearer token
    When I send 100 concurrent GET requests to "/v1/clients"
    Then all 100 requests complete successfully
    And no requests timeout
    And no errors occur

  @behavior:http-transport-expose @status:planned @priority:low @nfr:performance
  Scenario: No memory leaks under sustained load
    Given the HTTP server is running
    When I send 10,000 requests over 10 minutes
    Then the server memory usage remains stable
    And there are no memory leaks
    And the server continues to respond normally

  # ============================================================================
  # OpenAPI Documentation Scenarios
  # ============================================================================

  @behavior:http-transport-expose @status:planned @priority:medium
  Scenario: OpenAPI schema is auto-generated
    Given the HTTP server is running
    When I send GET to "/openapi.json"
    Then I receive HTTP status 200 OK
    And the response is valid OpenAPI 3.0 schema
    And the schema includes all 14 endpoints
    And each endpoint has description and parameters

  @behavior:http-transport-expose @status:planned @priority:medium
  Scenario: Swagger UI is available
    Given the HTTP server is running
    When I visit "http://localhost:8000/docs" in a browser
    Then the Swagger UI page loads
    And all 14 endpoints are listed
    And I can test endpoints interactively
    And authentication can be configured

  @behavior:http-transport-expose @status:planned @priority:low
  Scenario: ReDoc UI is available
    Given the HTTP server is running
    When I visit "http://localhost:8000/redoc" in a browser
    Then the ReDoc page loads
    And the API documentation is rendered beautifully
    And all endpoints are documented

# =============================================================================
# Scenario Summary
# =============================================================================
# Total Scenarios: 47
# - @behavior:http-transport-expose: 15 scenarios
# - @behavior:http-transport-auth: 6 scenarios
# - @behavior:http-transport-token-generate: 3 scenarios
# - @behavior:http-transport-cors: 3 scenarios
# - @behavior:http-transport-backward-compat: 4 scenarios
# - @behavior:http-transport-lifecycle: 6 scenarios
# - Error Handling: 4 scenarios
# - Performance: 3 scenarios
# - OpenAPI: 3 scenarios
#
# Priority Distribution:
# - Critical: 2
# - High: 17
# - Medium: 20
# - Low: 8
#
# Status: All @status:planned (Wave 2.0 implementation phase)
# =============================================================================
