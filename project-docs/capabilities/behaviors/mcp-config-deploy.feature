@behavior:MCP.CONFIG.DEPLOY
@status:ready
Feature: Deploy MCP configuration to client

  As a user
  I want to deploy configurations automatically
  So that I don't have to manually copy files to client config locations

  Background:
    Given I have initialized signing keys at "~/.mcp-orchestration/keys/"
    And I have a published configuration artifact for "claude-desktop/default"
    And the artifact has valid Ed25519 signature

  Scenario: Deploy latest configuration successfully
    Given I have published artifact "v1" for "claude-desktop/default"
    When I deploy the config without specifying an artifact ID
    Then the deployment succeeds
    And the config is written to "~/Library/Application Support/Claude/claude_desktop_config.json"
    And the deployment is recorded in the deployment log
    And the deployed artifact ID is "v1"

  Scenario: Deploy specific artifact by ID
    Given I have published artifacts "v1", "v2", "v3" for "claude-desktop/default"
    When I deploy artifact "v1" explicitly
    Then the deployment succeeds
    And artifact "v1" is written to disk
    And the deployment log shows artifact "v1"
    And the latest artifact is still "v3"

  Scenario: Deploy to non-existent client fails
    When I try to deploy to client "unknown-client" and profile "default"
    Then the deployment fails
    And I receive error code "CLIENT_NOT_FOUND"
    And I receive error message "Client 'unknown-client' not found in registry"

  Scenario: Deploy with invalid artifact ID fails
    When I try to deploy artifact "invalid-sha256-hash" for "claude-desktop/default"
    Then the deployment fails
    And I receive error code "ARTIFACT_NOT_FOUND"
    And I receive error message containing "Artifact"

  Scenario: Deploy verifies signature before writing
    Given I have an artifact with invalid signature
    When I try to deploy that artifact
    Then the deployment fails
    And I receive error code "SIGNATURE_INVALID"
    And I receive error message "Signature verification failed"
    And no config file is written to disk

  Scenario: Deployment creates parent directories if needed
    Given the client config directory "~/Library/Application Support/Claude/" does not exist
    When I deploy a config for "claude-desktop/default"
    Then the parent directories are created automatically
    And the config is written successfully
    And the deployment succeeds

  Scenario: Atomic deployment rolls back on write failure
    Given I have a valid artifact
    And writing to config path will fail with permission error
    When I try to deploy
    Then the deployment fails
    And no partial config is written
    And the deployment log shows status "failed"
    And I receive error code "WRITE_FAILED"

  Scenario: CLI deployment workflow
    Given I have a signed artifact for "claude-desktop/default"
    When I run CLI command "mcp-orchestration deploy-config --client claude-desktop --profile default"
    Then the CLI deployment succeeds
    And the config path is printed to stdout
    And the artifact ID is shown
    And the deployment timestamp is shown

  Scenario: MCP tool deployment workflow
    Given I am using the MCP tool from Claude Desktop
    When I call "deploy_config" with parameters:
      | parameter  | value           |
      | client_id  | claude-desktop  |
      | profile_id | default         |
    Then the tool returns JSON response
    And the response contains "status": "deployed"
    And the response contains "config_path"
    And the response contains "artifact_id"
    And the response contains "deployed_at" in ISO 8601 format

  Scenario: Query deployed vs latest artifact
    Given I have deployed artifact "v1" for "claude-desktop/default"
    And I have published newer artifact "v2"
    When I query the MCP resource "config://claude-desktop/default/deployed"
    Then I see artifact "v1"
    When I query the MCP resource "config://claude-desktop/default/latest"
    Then I see artifact "v2"
    And I can detect configuration drift

  Scenario: Deploy with changelog metadata
    Given I have an artifact with changelog "Added filesystem and github servers"
    When I deploy that artifact
    Then the deployment succeeds
    And the deployment log includes the changelog
    And I can query deployment history to see the changelog

  Scenario: Deploy to Cursor client
    Given I have a published artifact for "cursor/default"
    When I deploy the config
    Then the deployment succeeds
    And the config is written to "~/.cursor/mcp_config.json"
    And the deployment is recorded for client "cursor"
