Feature: Coordination Request Generation via chora-compose
  As a developer using chora-base
  I want to generate coordination request artifacts from high-level context
  So that I can create valid SAP-001 artifacts in 5-10 minutes instead of 30-60 minutes

  Background:
    Given chora-compose is installed and configured
    And the content block library exists in "docs/content-blocks/inbox-coordination/"
    And content configs exist in "configs/content/coordination-request/"
    And the artifact assembly config exists at "configs/artifact/coordination-request.json"
    And the post-processing wrapper exists at "scripts/process-generated-artifact.py"

  # ============================================================================
  # SCENARIO 1: Exploratory Request Generation
  # ============================================================================

  Scenario: Generate exploratory coordination request from minimal context
    Given I have a context file "context-examples/coordination/example-exploratory.json"
    And the context specifies request_type as "exploratory"
    And the context includes:
      | field       | value                                                |
      | from_repo   | github.com/liminalcommons/chora-base                 |
      | to_repo     | github.com/liminalcommons/chora-compose              |
      | purpose     | Explore chora-compose integration for inbox automation |
      | priority    | P2                                                   |
      | urgency     | backlog                                              |
    And the context includes 4 deliverables

    When I run "chora-compose generate coordination-request --context context-examples/coordination/example-exploratory.json --output inbox/draft/"

    Then a draft artifact should be created at "inbox/draft/coordination-request.json"
    And the draft should include all 6 HIGH priority fields:
      | field                | expected                  |
      | type                 | coordination              |
      | request_id           | PENDING                   |
      | title                | matches purpose           |
      | from_repo            | github.com/liminalcommons/chora-base |
      | to_repo              | github.com/liminalcommons/chora-compose |
      | priority             | P2                        |
      | urgency              | backlog                   |
      | deliverables         | array with 4 items        |
      | acceptance_criteria  | array with ≥4 items       |
      | created              | current date (YYYY-MM-DD) |
      | context.background   | 200-400 word narrative    |

    And the draft should include MEDIUM priority fields:
      | field             | expected                                    |
      | trace_id          | chora-compose-inbox-integration-2025        |
      | context.rationale | 150-300 word decision reasoning             |
      | estimated_effort  | 12-18 hours                                 |

    And the draft should include LOW priority fields for exploratory:
      | field                   | expected                        |
      | questions               | object with 4 topic groups      |
      | collaboration_modes     | array with 5 modes              |
      | context.not_requesting  | boundaries statement            |

    When I run "python scripts/process-generated-artifact.py inbox/draft/coordination-request.json"

    Then the artifact should pass JSON schema validation
    And request_id should be allocated as "COORD-2025-NNN"
    And an event should be emitted to "inbox/coordination/events.jsonl" with:
      | field       | value                              |
      | event_type  | coordination_request_created       |
      | request_id  | COORD-2025-NNN                     |
      | trace_id    | chora-compose-inbox-integration-2025 |

    And the final artifact should exist at "inbox/incoming/coordination/COORD-2025-NNN.json"
    And the draft file should be deleted
    And inbox-status.py should validate the artifact without errors

  # ============================================================================
  # SCENARIO 2: Prescriptive Request Generation
  # ============================================================================

  Scenario: Generate prescriptive coordination request with concrete deliverables
    Given I have a context file "context-examples/coordination/example-prescriptive.json"
    And the context specifies request_type as "prescriptive"
    And the context includes:
      | field       | value                                        |
      | from_repo   | github.com/liminalcommons/chora-base         |
      | to_repo     | github.com/liminalcommons/chora-base         |
      | purpose     | Implement bidirectional translation for SAP-009 |
      | priority    | P1                                           |
      | urgency     | next_sprint                                  |
    And the context includes 10 specific deliverables with version numbers
    And the context includes 12 acceptance criteria with quantitative thresholds

    When I run "chora-compose generate coordination-request --context context-examples/coordination/example-prescriptive.json --output inbox/draft/"

    Then a draft artifact should be created at "inbox/draft/coordination-request.json"
    And the draft should include all 6 HIGH priority fields
    And deliverables should include specific versions:
      | deliverable                                              |
      | SAP-009 v1.1.0 with bidirectional translation protocol   |
      | Implementation in scripts/translate-bidirectional.py with ≥80% test coverage |
      | CHANGELOG.md entry documenting v1.1.0 changes            |

    And acceptance_criteria should include measurable thresholds:
      | criterion                                                        |
      | scripts/translate-bidirectional.py achieves ≥80% test coverage   |
      | Performance benchmarks demonstrate <100ms translation time       |
      | Documentation clarity review achieves ≥85% score                |

    And the draft should include MEDIUM priority fields:
      | field                | expected                                |
      | trace_id             | bidirectional-translation-sap009-2025   |
      | context.rationale    | explains why bidirectional vs alternatives |
      | estimated_effort     | 40-59 hours                             |
      | timeline             | Needed by 2025-11-15                    |
      | dependencies         | array with 3 completed dependencies     |
      | related              | array with 5 related items              |

    And the draft should NOT include LOW priority exploratory fields:
      | field               |
      | questions           |
      | collaboration_modes |
      | context.not_requesting |

    When I run "python scripts/process-generated-artifact.py inbox/draft/coordination-request.json"

    Then the artifact should pass all validation steps
    And the final artifact should be ready for internal triage

  # ============================================================================
  # SCENARIO 3: Peer Review Request Generation
  # ============================================================================

  Scenario: Generate peer review coordination request with review criteria
    Given I have a context file "context-examples/coordination/example-peer-review.json"
    And the context specifies request_type as "peer_review"
    And the context includes:
      | field       | value                                            |
      | from_repo   | github.com/liminalcommons/chora-workspace        |
      | to_repo     | github.com/liminalcommons/chora-base             |
      | purpose     | Request peer review of React SAPs for ecosystem alignment |
      | priority    | P1                                               |
      | urgency     | backlog                                          |
    And the context includes 5 deliverables focused on review and recommendations

    When I run "chora-compose generate coordination-request --context context-examples/coordination/example-peer-review.json --output inbox/draft/"

    Then a draft artifact should be created
    And deliverables should focus on feedback:
      | deliverable                                              |
      | Technical review of React SAP architecture and patterns  |
      | Assessment of alignment with chora-base standards        |
      | Recommendations for improving clarity                    |
      | Identification of potential gaps or edge cases           |

    And acceptance_criteria should be review-focused:
      | criterion                                                    |
      | Alignment assessment compares against ≥3 chora-base SAPs     |
      | Recommendations include ≥5 specific improvement suggestions  |
      | Review feedback is constructive with specific examples       |

    And the draft should include peer-review-specific LOW priority fields:
      | field                   | expected                        |
      | questions               | grouped by review topics        |
      | collaboration_modes     | review depth options (4 modes)  |
      | context.not_requesting  | scope boundaries for review     |

    When I run post-processing
    Then the artifact should be valid for cross-repository peer review

  # ============================================================================
  # SCENARIO 4: Quality Validation
  # ============================================================================

  Scenario: Generated artifact meets quality rubric threshold
    Given I have generated a coordination request from "context-examples/coordination/example-exploratory.json"
    And the artifact exists at "inbox/incoming/coordination/COORD-2025-NNN.json"

    When I run "python scripts/evaluate-pilot-quality.py --generated inbox/incoming/coordination/COORD-2025-NNN.json --reference context-examples/coordination/example-exploratory.json --rubric docs/pilots/quality-rubric.json"

    Then the quality assessment should include scores for all 10 criteria:
      | criterion              | weight | threshold |
      | Structure Match        | 10%    | 100%      |
      | Technical Accuracy     | 20%    | ≥80%      |
      | Coherence              | 15%    | ≥75%      |
      | Completeness           | 15%    | ≥80%      |
      | JSON Schema            | 10%    | 100%      |
      | inbox-status.py        | 10%    | 100%      |
      | Time Reduction         | 5%     | ≥70%      |
      | Maintainability        | 5%     | ≥70%      |
      | Flexibility            | 5%     | ≥70%      |
      | Scalability            | 5%     | ≥70%      |

    And the overall weighted score should be ≥80%
    And the assessment should include specific feedback for criteria <80%

  # ============================================================================
  # SCENARIO 5: Error Handling
  # ============================================================================

  Scenario: Invalid context input is rejected
    Given I have a context file "test-contexts/invalid-missing-required.json"
    And the context is missing required field "deliverables"

    When I run "chora-compose generate coordination-request --context test-contexts/invalid-missing-required.json"

    Then the generation should fail with error "Missing required context field: deliverables"
    And no draft artifact should be created

  Scenario: Post-processing catches schema violations
    Given I have a malformed draft at "inbox/draft/coordination-request.json"
    And the draft has invalid priority value "P5" (not in enum)

    When I run "python scripts/process-generated-artifact.py inbox/draft/coordination-request.json"

    Then validation should fail with error "priority must be P0, P1, or P2"
    And the draft should remain in "inbox/draft/" for debugging
    And an error should be logged to "inbox/draft/errors.log"
    And no artifact should be promoted to "inbox/incoming/"

  # ============================================================================
  # SCENARIO 6: Time Performance
  # ============================================================================

  Scenario: Generation completes within target time
    Given I have a valid context file
    And I start a timer

    When I run the complete generation pipeline:
      """
      chora-compose generate coordination-request --context context.json --output inbox/draft/
      python scripts/process-generated-artifact.py inbox/draft/coordination-request.json
      """

    Then the total execution time should be ≤10 minutes
    And the time should be logged for metrics
    And the time reduction vs manual baseline (30-60 min) should be ≥70%

  # ============================================================================
  # SCENARIO 7: Conditional Content Inclusion
  # ============================================================================

  Scenario Outline: Optional fields are included only when appropriate
    Given I have a context with request_type "<type>"
    And from_repo is "<from>" and to_repo is "<to>"
    And trace_id is "<trace>"

    When I generate the coordination request

    Then questions field should be <questions>
    And collaboration_modes field should be <collab_modes>
    And context.not_requesting field should be <boundaries>
    And trace_id field should be <trace_included>

    Examples:
      | type        | from                              | to                                | trace                        | questions | collab_modes | boundaries | trace_included |
      | exploratory | github.com/liminalcommons/chora-base | github.com/liminalcommons/chora-compose | defined    | included  | included     | included   | included       |
      | exploratory | github.com/liminalcommons/chora-base | github.com/liminalcommons/chora-base    | defined    | included  | omitted      | omitted    | included       |
      | prescriptive| github.com/liminalcommons/chora-base | github.com/liminalcommons/chora-base    | defined    | omitted   | omitted      | omitted    | included       |
      | peer_review | github.com/liminalcommons/chora-workspace | github.com/liminalcommons/chora-base | undefined | included  | included     | included   | omitted        |

  # ============================================================================
  # SCENARIO 8: AI Augmentation Quality
  # ============================================================================

  Scenario: AI-generated fields maintain quality and consistency
    Given I provide minimal context:
      """json
      {
        "request_type": "exploratory",
        "purpose": "Explore chora-compose integration",
        "deliverables": ["Feasibility assessment", "Options comparison"],
        "priority": "P2",
        "urgency": "backlog"
      }
      """

    When I generate the coordination request

    Then the AI-generated title should:
      | requirement                           | example                                      |
      | be 50-80 characters                   | "Exploring chora-compose Integration for Inbox Automation" |
      | use title case                        | Not "exploring chora-compose integration"    |
      | avoid redundant prefixes              | Not "Request to Explore..."                  |
      | capture essence of purpose            | Includes "chora-compose" and "Integration"   |

    And the AI-generated context.background should:
      | requirement                           |
      | be 200-400 words (exploratory)        |
      | have 3 paragraphs (current → problem → request) |
      | define acronyms on first use          |
      | be accessible to external readers     |
      | explain why this request matters      |

    And the AI-generated acceptance_criteria should:
      | requirement                                     |
      | derive from deliverables                        |
      | include ≥4 criteria for exploratory             |
      | be measurable with thresholds (≥N, <N, %)      |
      | be independently verifiable                     |
      | map 1:1 or N:1 with deliverables                |

  # ============================================================================
  # SCENARIO 9: Reusability and Scalability
  # ============================================================================

  Scenario: Content blocks are reusable across request types
    Given I analyze all 15 content blocks

    Then 6 content blocks should be marked "universal" reusability:
      | block                        | reusable_for            |
      | core-metadata                | coordination, task, proposal |
      | repository-fields            | coordination, task, proposal |
      | priority-urgency             | coordination, task, proposal |
      | deliverables-structure       | coordination, task, proposal |
      | acceptance-criteria-patterns | coordination, task, proposal |
      | context-background           | coordination, task, proposal |

    And 9 content blocks should be marked "moderate" or "inbox-specific":
      | block                   | reusability_note                     |
      | exploratory-questions   | Exploratory coordination primarily   |
      | collaboration-modes     | Cross-repo coordination              |
      | context-boundaries      | External coordination                |

    And content blocks should enable task generation with 60-70% reuse
    And content blocks should enable proposal generation with 60-70% reuse
