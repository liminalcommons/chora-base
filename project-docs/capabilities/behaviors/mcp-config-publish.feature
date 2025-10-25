@behavior:MCP.CONFIG.PUBLISH
@status:ready
Feature: Publish MCP configuration with validation
  As a developer
  I want to publish validated configurations
  So that I can deploy safe, cryptographically signed configs

  Background:
    Given signing keys are initialized at "~/.mcp-orchestration/keys/"
    And the client "claude-desktop" is configured
    And the profile "default" exists

  Scenario: Publish valid configuration
    Given I have a draft configuration with servers:
      | server_id  | params              | env_vars              |
      | filesystem | path=/tmp/docs      |                       |
      | github     |                     | GITHUB_TOKEN=ghp_test |
    And the draft configuration is valid
    When I publish the config with changelog "Added filesystem and github servers"
    Then the publish operation succeeds
    And the config is signed with Ed25519
    And the config is stored as content-addressable artifact
    And the artifact metadata includes:
      | field     | value                                      |
      | generator | ConfigBuilder                              |
      | changelog | Added filesystem and github servers        |
    And the profile index points to the new artifact

  Scenario: Reject configuration with validation errors
    Given I have a draft configuration with servers:
      | server_id  | params         |
      | filesystem | path=/tmp/docs |
    And the draft configuration has validation errors:
      | error_code       | server     | message                                    |
      | MISSING_COMMAND  | filesystem | Server 'filesystem' is missing 'command'   |
    When I attempt to publish the config
    Then the publish operation fails
    And I see the error code "VALIDATION_FAILED"
    And I see validation errors:
      | error_code      | server     |
      | MISSING_COMMAND | filesystem |

  Scenario: Reject empty configuration
    Given I have an empty draft configuration
    When I attempt to publish the config
    Then the publish operation fails
    And I see the error code "VALIDATION_FAILED"
    And I see the error "EMPTY_CONFIG"

  Scenario: Include changelog in metadata
    Given I have a valid draft configuration with 1 server
    When I publish the config with changelog "Initial configuration for dev environment"
    Then the publish operation succeeds
    And the artifact metadata["changelog"] equals "Initial configuration for dev environment"

  Scenario: Auto-generate metadata fields
    Given I have a valid draft configuration with 2 servers
    When I publish the config with changelog "Added two servers"
    Then the publish operation succeeds
    And the artifact metadata includes:
      | field        | value         |
      | generator    | ConfigBuilder |
      | server_count | 2             |

  Scenario: Publish via MCP tool
    Given I have a valid draft configuration
    And I am connected to the MCP server
    When I call the MCP tool "publish_config" with:
      | parameter  | value                    |
      | client_id  | claude-desktop           |
      | profile_id | default                  |
      | changelog  | Published via MCP tool   |
    Then the tool returns success
    And the response includes "artifact_id"
    And the response includes "status: published"

  Scenario: Publish via CLI command
    Given I have a valid config file "test-config.json" with content:
      """
      {
        "mcpServers": {
          "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
          }
        }
      }
      """
    When I run the CLI command:
      """
      mcp-orchestration publish-config \
        --client claude-desktop \
        --profile default \
        --file test-config.json \
        --changelog "Published via CLI"
      """
    Then the CLI command succeeds
    And I see output containing "artifact_id"
    And I see output containing "Published successfully"

  Scenario: Validation runs before signing
    Given I have a draft configuration with validation errors
    When I attempt to publish the config
    Then the validation check runs first
    And the signing operation is not executed
    And the storage operation is not executed

  Scenario: Publishing is atomic
    Given I have a valid draft configuration
    And the storage operation will fail
    When I attempt to publish the config
    Then the entire publish operation is rolled back
    And no artifact is created
    And the profile index is not updated

  Scenario: Content-addressable artifact ID
    Given I have a valid draft configuration with payload:
      """
      {"mcpServers": {"test": {"command": "test", "args": []}}}
      """
    When I publish the config
    Then the artifact_id is the SHA-256 hash of the payload
    And the artifact_id matches "[a-f0-9]{64}"

  Scenario: Validate before publishing (workflow integration)
    Given I have a draft configuration with 3 servers
    When I explicitly validate the config using "validate_config"
    Then the validation returns:
      | field  | value |
      | valid  | true  |
      | errors | []    |
    When I then publish the config
    Then the publish operation succeeds
    And the validation was run during publish as well

  Scenario: Fix validation errors then publish
    Given I have a draft configuration with validation errors
    When I validate the config
    Then I see specific validation errors
    When I fix the errors in the draft
    And I validate again
    Then validation passes
    When I publish the config
    Then the publish operation succeeds
