Feature: Bidirectional Translation Layer Integration
  As a user or agent
  I want to use natural language to interact with the system
  So that I can work conversationally while executing procedurally

  Background:
    Given the chora-base repository is initialized
    And all foundation tools are available

  # ============================================================================
  # Intent Recognition - Exact Matches
  # ============================================================================

  Scenario: Recognize exact inbox status query
    Given the intent router is initialized
    When user input is "show inbox"
    Then intent should be "run_inbox_status"
    And confidence should be >= 0.70
    And clarification should be empty

  Scenario: Recognize exact pending requests query
    Given the intent router is initialized
    When user input is "what's pending"
    Then intent should be "list_pending_coordination_requests"
    And confidence should be >= 0.70
    And clarification should be empty

  Scenario: Recognize exact test execution query
    Given the intent router is initialized
    When user input is "run tests"
    Then intent should be "pytest_run"
    And confidence should be >= 0.70
    And clarification should be empty

  Scenario: Recognize exact coverage check query
    Given the intent router is initialized
    When user input is "check coverage"
    Then intent should be "pytest_coverage_report"
    And confidence should be >= 0.70
    And clarification should be empty

  Scenario: Recognize exact ROI calculation query
    Given the intent router is initialized
    When user input is "calculate ROI"
    Then intent should be "run_claude_roi_calculator"
    And confidence should be >= 0.70
    And clarification should be empty

  # ============================================================================
  # Intent Recognition - Variations
  # ============================================================================

  Scenario: Recognize inbox status query variation
    Given the intent router is initialized
    When user input is "what's in the inbox?"
    Then intent should be "run_inbox_status"
    And confidence should be >= 0.70

  Scenario: Recognize coordination requests query variation
    Given the intent router is initialized
    When user input is "check coordination requests"
    Then intent should be "list_pending_coordination_requests"
    And confidence should be >= 0.70

  Scenario: Recognize test execution query variation
    Given the intent router is initialized
    When user input is "execute tests"
    Then intent should be "pytest_run"
    And confidence should be >= 0.70

  Scenario: Recognize coverage check query variation
    Given the intent router is initialized
    When user input is "how's our coverage"
    Then intent should be "pytest_coverage_report"
    And confidence should be >= 0.70

  Scenario: Recognize ROI calculation query variation
    Given the intent router is initialized
    When user input is "is this worth it"
    Then intent should be "run_claude_roi_calculator"
    And confidence should be >= 0.70

  # ============================================================================
  # Intent Recognition - Typos (Fuzzy Matching)
  # ============================================================================

  Scenario: Recognize query with typo in "show"
    Given the intent router is initialized
    When user input is "shwo inbox"
    Then intent should be "run_inbox_status"
    And confidence should be >= 0.50

  Scenario: Recognize query with typo in "check"
    Given the intent router is initialized
    When user input is "chek coverage"
    Then intent should be "pytest_coverage_report"
    And confidence should be >= 0.50

  Scenario: Recognize query with typo in "coordination"
    Given the intent router is initialized
    When user input is "coordnation request"
    Then intent should be "create_coordination_request"
    And confidence should be >= 0.50

  # ============================================================================
  # Intent Recognition - Ambiguous Queries
  # ============================================================================

  Scenario: Handle ambiguous "check status" query
    Given the intent router is initialized
    When user input is "check status"
    Then confidence should be between 0.50 and 0.70
    And clarification should contain "Did you mean"
    And alternatives should include at least 2 options

  Scenario: Handle ambiguous "review" query
    Given the intent router is initialized
    When user input is "review"
    Then confidence should be < 0.70
    And clarification should not be empty
    And alternatives should include "review coordination request"
    And alternatives should include "code review"

  Scenario: Handle ambiguous "validate" query
    Given the intent router is initialized
    When user input is "validate"
    Then confidence should be < 0.70
    And clarification should contain "what would you like to validate"

  # ============================================================================
  # Intent Recognition - Parameter Extraction
  # ============================================================================

  Scenario: Extract coordination request ID from query
    Given the intent router is initialized
    When user input is "review coord-005"
    Then intent should be "open_coordination_request"
    And confidence should be >= 0.70
    And parameter "id" should be "coord-005"

  Scenario: Extract test file path from query
    Given the intent router is initialized
    When user input is "run tests for test_intent_router.py"
    Then intent should be "pytest_run_file"
    And confidence should be >= 0.70
    And parameter "path" should contain "test_intent_router.py"

  # ============================================================================
  # Glossary Search - Exact Matches
  # ============================================================================

  Scenario: Search for exact term "Coordination Request"
    Given the glossary is loaded
    When searching for "Coordination Request"
    Then should return at least 1 result
    And top result term should be "Coordination Request"
    And top result score should be 1.0
    And top result definition should contain "Type 2 intake"
    And top result sap_reference should be "SAP-001"

  Scenario: Search for exact term "SAP"
    Given the glossary is loaded
    When searching for "SAP"
    Then should return at least 1 result
    And top result term should be "Skilled Awareness Package"
    And top result score should be 1.0

  Scenario: Search for exact term "DDD"
    Given the glossary is loaded
    When searching for "DDD"
    Then should return at least 1 result
    And top result should be one of:
      | Documentation Driven Design |
      | Skilled Awareness Package   |
    And top result score should be >= 0.80

  # ============================================================================
  # Glossary Search - Fuzzy Matching
  # ============================================================================

  Scenario: Search with typo using fuzzy matching
    Given the glossary is loaded
    When searching for "coordnation" with fuzzy matching
    Then should return at least 1 result
    And top result term should be "Coordination Request"
    And top result score should be >= 0.60

  Scenario: Search with partial term using fuzzy matching
    Given the glossary is loaded
    When searching for "coord" with fuzzy matching
    Then should return at least 2 results
    And results should include "Coordination Request"
    And all scores should be >= 0.60

  # ============================================================================
  # Glossary Search - Related Terms
  # ============================================================================

  Scenario: Get related terms for "Coordination Request"
    Given the glossary is loaded
    When getting related terms for "Coordination Request"
    Then results should include "Strategic Proposal"
    And results should include "Implementation Task"

  Scenario: Get terms by category
    Given the glossary is loaded
    When getting terms in category "Intake & Coordination"
    Then results should include "Coordination Request"
    And results should include "Strategic Proposal"
    And results should include "Implementation Task"

  Scenario: Get terms by SAP
    Given the glossary is loaded
    When getting terms for SAP "SAP-001"
    Then results should include "Coordination Request"
    And results should include "Inbox Protocol"

  # ============================================================================
  # Context-Aware Suggestions - Inbox Status
  # ============================================================================

  Scenario: Suggest reviewing pending coordination requests
    Given the suggestion engine is initialized
    And inbox has 3 pending coordination requests
    When requesting suggestions in "reactive" mode
    Then top suggestion should contain "Review" and "pending coordination request"
    And top suggestion priority should be "high"
    And top suggestion category should be "workflow"

  Scenario: Suggest resolving blockers
    Given the suggestion engine is initialized
    And inbox has 2 active blockers
    When requesting suggestions in "reactive" mode
    Then suggestions should include "Resolve" and "blocker"
    And blocker suggestion priority should be "high"

  Scenario: No inbox suggestions when empty
    Given the suggestion engine is initialized
    And inbox has 0 pending items
    And inbox has 0 blockers
    When requesting suggestions in "reactive" mode
    Then suggestions should not mention "inbox" or "coordination request"

  # ============================================================================
  # Context-Aware Suggestions - Quality Metrics
  # ============================================================================

  Scenario: Suggest improving coverage when below threshold
    Given the suggestion engine is initialized
    And test coverage is 78%
    When requesting suggestions in "reactive" mode
    Then suggestions should include "coverage"
    And coverage suggestion should mention "85%"
    And coverage suggestion priority should be "medium"

  Scenario: Suggest fixing broken links
    Given the suggestion engine is initialized
    And there are 5 broken links in documentation
    When requesting suggestions in "reactive" mode
    Then suggestions should include "broken link"
    And link suggestion priority should be "medium"

  # ============================================================================
  # Context-Aware Suggestions - Proactive Mode
  # ============================================================================

  Scenario: Proactive mode returns only high priority
    Given the suggestion engine is initialized
    And inbox has 1 pending request (high priority)
    And test coverage is 78% (medium priority)
    When requesting suggestions in "proactive" mode
    Then should return exactly 1 suggestion
    And suggestion priority should be "high"
    And suggestion should mention "coordination request"

  # ============================================================================
  # User Preferences - Verbosity Adaptation
  # ============================================================================

  Scenario: Adapt to verbose preference
    Given user preferences set verbosity to "verbose"
    When generating response for "explain AGENTS.md pattern"
    Then response word count should be > 150
    And response should contain "example"
    And response should contain "detailed"

  Scenario: Adapt to concise preference
    Given user preferences set verbosity to "concise"
    When generating response for "explain AGENTS.md pattern"
    Then response word count should be < 50
    And response should not contain multi-paragraph explanations

  Scenario: Adapt to standard verbosity (default)
    Given user preferences set verbosity to "standard"
    When generating response for "explain AGENTS.md pattern"
    Then response word count should be between 50 and 150

  # ============================================================================
  # User Preferences - Formality Adaptation
  # ============================================================================

  Scenario: Adapt to casual formality
    Given user preferences set formality to "casual"
    When generating response for any query
    Then response should contain contractions like "don't" or "can't"
    And tone should be conversational

  Scenario: Adapt to formal formality
    Given user preferences set formality to "formal"
    When generating response for any query
    Then response should not contain contractions
    And tone should be professional

  # ============================================================================
  # User Preferences - Workflow Adaptation
  # ============================================================================

  Scenario: Require confirmation for all actions when set to "always"
    Given user preferences set require_confirmation to "always"
    When executing action "read file.txt"
    Then should prompt for confirmation
    And action should not execute until confirmed

  Scenario: Require confirmation only for destructive actions
    Given user preferences set require_confirmation to "destructive"
    When executing action "delete file.txt"
    Then should prompt for confirmation
    When executing action "read file.txt"
    Then should not prompt for confirmation

  Scenario: Never require confirmation
    Given user preferences set require_confirmation to "never"
    When executing action "delete file.txt"
    Then should not prompt for confirmation

  # ============================================================================
  # User Preferences - Progressive Disclosure
  # ============================================================================

  Scenario: Enable progressive disclosure
    Given user preferences set progressive_disclosure to true
    When presenting complex information
    Then should show summary first
    And should offer "show more details" option

  Scenario: Disable progressive disclosure
    Given user preferences set progressive_disclosure to false
    When presenting complex information
    Then should show all details immediately

  # ============================================================================
  # Graceful Degradation - Missing Tools
  # ============================================================================

  Scenario: Fall back when intent router unavailable
    Given intent-router.py is not executable
    When user input is "show inbox"
    Then should fall back to INTENT_PATTERNS.yaml pattern matching
    And should return valid intent "run_inbox_status"
    And should log warning about missing tool

  Scenario: Fall back when glossary search unavailable
    Given chora-search.py is not executable
    When searching for "Coordination Request"
    Then should fall back to reading GLOSSARY.md directly
    And should return valid definition

  Scenario: Fall back when suggestion engine unavailable
    Given suggest-next.py is not executable
    When requesting suggestions
    Then should fall back to documented workflow patterns
    And should not block user from proceeding

  # ============================================================================
  # Pattern Learning - New Pattern Addition
  # ============================================================================

  Scenario: Add new pattern without breaking existing
    Given the intent router is initialized
    And pattern "archive_completed" does not exist
    When adding new pattern:
      | pattern_id | archive_completed |
      | action | archive_completed_coordination_requests |
      | trigger | archive completed work |
    Then pattern should be recognized
    And existing patterns should still work
    When user input is "show inbox"
    Then intent should still be "run_inbox_status"

  Scenario: New pattern with parameter extraction
    Given the intent router is initialized
    When adding pattern with parameter "sprint_id"
    And user input is "show sprint 5 status"
    Then should extract parameter "sprint_id" as "5"

  # ============================================================================
  # Pattern Learning - Pattern Conflicts
  # ============================================================================

  Scenario: Handle pattern conflict with multiple matches
    Given the intent router is initialized
    When user input is "check"
    Then should have multiple matches with similar confidence
    And confidence difference between top 2 should be < 0.20
    And should request clarification
    And clarification should mention alternatives

  # ============================================================================
  # Integration - Intent Router + Glossary
  # ============================================================================

  Scenario: Route unknown term to glossary search
    Given the intent router is initialized
    And the glossary is loaded
    When user input is "what's a coordination request"
    Then should recognize glossary query pattern
    And should search glossary for "coordination request"
    And should return definition

  # ============================================================================
  # Integration - Intent Router + Suggestions
  # ============================================================================

  Scenario: Route "what should I do next" to suggestion engine
    Given the intent router is initialized
    And the suggestion engine is initialized
    When user input is "what should i work on next"
    Then should recognize suggestion query pattern
    And should call suggestion engine in "reactive" mode
    And should return top 5 suggestions

  # ============================================================================
  # Integration - All Tools Working Together
  # ============================================================================

  Scenario: Complete workflow with all tools
    Given all bidirectional translation tools are available
    And user preferences are loaded
    When user input is "show me what's pending and suggest what to do"
    Then should route intent to multiple actions
    And should execute "run_inbox_status"
    And should execute "suggest_next_actions"
    And should format response according to user verbosity preference

  # ============================================================================
  # Quality Gates - Coverage
  # ============================================================================

  Scenario: Validate test coverage meets threshold
    Given the integration code is complete
    When running pytest with coverage
    Then coverage should be >= 85%

  # ============================================================================
  # Quality Gates - Lint
  # ============================================================================

  Scenario: Validate no lint errors
    Given the integration code is complete
    When running ruff check
    Then should have 0 errors

  # ============================================================================
  # Quality Gates - Type Checking
  # ============================================================================

  Scenario: Validate no type errors
    Given the integration code is complete
    When running mypy with strict mode
    Then should have 0 errors

  # ============================================================================
  # Backward Compatibility
  # ============================================================================

  Scenario: SAP-009 v1.0.0 features still work
    Given SAP-009 v1.1.0 is installed
    When using AGENTS.md dual-file pattern (v1.0.0 feature)
    Then should work without changes
    When using "Nearest File Wins" (v1.0.0 feature)
    Then should work without changes
    When using progressive context loading (v1.0.0 feature)
    Then should work without changes

  # ============================================================================
  # Documentation - Diátaxis Adherence
  # ============================================================================

  Scenario: Protocol spec follows reference documentation style
    Given SAP-009 protocol-spec.md Section 9 exists
    Then should define contracts clearly
    And should include input/output specifications
    And should include usage examples
    And should follow reference documentation style (Diátaxis)

  Scenario: Awareness guide follows how-to documentation style
    Given SAP-009 awareness-guide.md integration section exists
    Then should provide step-by-step integration instructions
    And should include usage examples
    And should follow how-to documentation style (Diátaxis)
