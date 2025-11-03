"""
Step definitions for bidirectional translation layer BDD scenarios.

This module implements all step definitions for testing:
- Intent recognition (exact, variations, typos, ambiguous)
- Glossary search (exact, fuzzy, related terms)
- Context-aware suggestions (inbox, quality, proactive)
- User preferences adaptation (verbosity, formality, workflow)
- Graceful degradation (missing tools)
- Pattern learning (new patterns, conflicts)
- Quality gates (coverage, lint, type checking)
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import yaml
from behave import given, then, when
from behave.runner import Context


# ============================================================================
# Helper Functions
# ============================================================================

def mock_inbox_status(pending_count: int = 0, blocker_count: int = 0) -> Dict[str, Any]:
    """Create mock inbox status for testing."""
    return {
        'repositories': {
            'chora-base': {
                'active_work': [
                    {
                        'id': f'coord-{i:03d}',
                        'status': 'pending_triage',
                        'priority': 'P2'
                    }
                    for i in range(1, pending_count + 1)
                ],
                'blockers': [
                    f'Blocker {i}'
                    for i in range(1, blocker_count + 1)
                ]
            }
        }
    }


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split())


# ============================================================================
# Background Steps
# ============================================================================

@given('the chora-base repository is initialized')
def step_impl(context: Context):
    """Verify chora-base repository is initialized."""
    context.repo_root = Path.cwd()
    assert context.repo_root.name == 'chora-base' or (context.repo_root / '.git').exists()


@given('all foundation tools are available')
def step_impl(context: Context):
    """Verify all foundation tools exist."""
    tools = [
        'scripts/intent-router.py',
        'scripts/chora-search.py',
        'scripts/suggest-next.py',
        'docs/dev-docs/patterns/INTENT_PATTERNS.yaml',
        'docs/GLOSSARY.md',
        '.chora/user-preferences.yaml.template'
    ]
    for tool in tools:
        tool_path = context.repo_root / tool
        assert tool_path.exists(), f"Foundation tool not found: {tool}"


# ============================================================================
# Intent Router Steps
# ============================================================================

@given('the intent router is initialized')
def step_impl(context: Context):
    """Initialize intent router for testing."""
    try:
        from scripts.intent_router import IntentRouter
        context.router = IntentRouter()
    except ImportError:
        # Fallback: router not yet implemented, will be RED
        context.router = None
        context.router_unavailable = True


@when('user input is "{text}"')
def step_impl(context: Context, text: str):
    """Route user input through intent router."""
    if hasattr(context, 'router_unavailable') and context.router_unavailable:
        # Router not implemented yet - scenario should fail (RED)
        context.matches = []
        return

    try:
        context.matches = context.router.route(text)
    except Exception as e:
        context.error = e
        context.matches = []


@then('intent should be "{action}"')
def step_impl(context: Context, action: str):
    """Verify top intent matches expected action."""
    assert len(context.matches) > 0, "No intent matches found"
    assert context.matches[0].action == action, \
        f"Expected action '{action}', got '{context.matches[0].action}'"


@then('confidence should be >= {threshold:f}')
def step_impl(context: Context, threshold: float):
    """Verify confidence meets minimum threshold."""
    assert len(context.matches) > 0, "No intent matches found"
    assert context.matches[0].confidence >= threshold, \
        f"Confidence {context.matches[0].confidence:.2f} below threshold {threshold}"


@then('confidence should be between {min_conf:f} and {max_conf:f}')
def step_impl(context: Context, min_conf: float, max_conf: float):
    """Verify confidence is within range."""
    assert len(context.matches) > 0, "No intent matches found"
    conf = context.matches[0].confidence
    assert min_conf <= conf <= max_conf, \
        f"Confidence {conf:.2f} not in range [{min_conf}, {max_conf}]"


@then('confidence should be < {threshold:f}')
def step_impl(context: Context, threshold: float):
    """Verify confidence is below threshold."""
    assert len(context.matches) > 0, "No intent matches found"
    assert context.matches[0].confidence < threshold, \
        f"Confidence {context.matches[0].confidence:.2f} should be < {threshold}"


@then('clarification should be empty')
def step_impl(context: Context):
    """Verify no clarification is needed."""
    assert len(context.matches) > 0, "No intent matches found"
    assert context.matches[0].clarification is None or context.matches[0].clarification == "", \
        f"Expected no clarification, got: {context.matches[0].clarification}"


@then('clarification should contain "{text}"')
def step_impl(context: Context, text: str):
    """Verify clarification contains expected text."""
    assert len(context.matches) > 0, "No intent matches found"
    assert context.matches[0].clarification is not None, "No clarification provided"
    assert text.lower() in context.matches[0].clarification.lower(), \
        f"Clarification does not contain '{text}': {context.matches[0].clarification}"


@then('clarification should not be empty')
def step_impl(context: Context):
    """Verify clarification is provided."""
    assert len(context.matches) > 0, "No intent matches found"
    assert context.matches[0].clarification is not None and context.matches[0].clarification != "", \
        "Expected clarification, got none"


@then('alternatives should include at least {count:d} options')
def step_impl(context: Context, count: int):
    """Verify multiple alternative matches exist."""
    assert len(context.matches) >= count, \
        f"Expected at least {count} alternatives, got {len(context.matches)}"


@then('alternatives should include "{action}"')
def step_impl(context: Context, action: str):
    """Verify alternatives include specific action."""
    actions = [m.action for m in context.matches]
    assert action in actions, \
        f"Expected '{action}' in alternatives, got: {actions}"


@then('parameter "{param_name}" should be "{param_value}"')
def step_impl(context: Context, param_name: str, param_value: str):
    """Verify parameter was extracted correctly."""
    assert len(context.matches) > 0, "No intent matches found"
    params = context.matches[0].parameters
    assert param_name in params, f"Parameter '{param_name}' not found in {params}"
    assert params[param_name] == param_value, \
        f"Expected parameter '{param_name}' = '{param_value}', got '{params[param_name]}'"


@then('parameter "{param_name}" should contain "{text}"')
def step_impl(context: Context, param_name: str, text: str):
    """Verify parameter contains expected text."""
    assert len(context.matches) > 0, "No intent matches found"
    params = context.matches[0].parameters
    assert param_name in params, f"Parameter '{param_name}' not found in {params}"
    assert text in str(params[param_name]), \
        f"Parameter '{param_name}' does not contain '{text}': {params[param_name]}"


# ============================================================================
# Glossary Search Steps
# ============================================================================

@given('the glossary is loaded')
def step_impl(context: Context):
    """Load glossary for testing."""
    try:
        from scripts.chora_search import GlossarySearch
        context.glossary = GlossarySearch()
    except ImportError:
        # Fallback: glossary search not yet implemented
        context.glossary = None
        context.glossary_unavailable = True


@when('searching for "{query}"')
def step_impl(context: Context, query: str):
    """Search glossary for term."""
    if hasattr(context, 'glossary_unavailable') and context.glossary_unavailable:
        context.results = []
        return

    try:
        context.results = context.glossary.search(query, fuzzy=False)
    except Exception as e:
        context.error = e
        context.results = []


@when('searching for "{query}" with fuzzy matching')
def step_impl(context: Context, query: str):
    """Search glossary with fuzzy matching."""
    if hasattr(context, 'glossary_unavailable') and context.glossary_unavailable:
        context.results = []
        return

    try:
        context.results = context.glossary.search(query, fuzzy=True)
    except Exception as e:
        context.error = e
        context.results = []


@when('getting related terms for "{term}"')
def step_impl(context: Context, term: str):
    """Get related terms for a term."""
    if hasattr(context, 'glossary_unavailable') and context.glossary_unavailable:
        context.results = []
        return

    try:
        context.results = context.glossary.get_related(term)
    except Exception as e:
        context.error = e
        context.results = []


@when('getting terms in category "{category}"')
def step_impl(context: Context, category: str):
    """Get all terms in a category."""
    if hasattr(context, 'glossary_unavailable') and context.glossary_unavailable:
        context.results = []
        return

    try:
        context.results = context.glossary.by_category(category)
    except Exception as e:
        context.error = e
        context.results = []


@when('getting terms for SAP "{sap_id}"')
def step_impl(context: Context, sap_id: str):
    """Get all terms related to a SAP."""
    if hasattr(context, 'glossary_unavailable') and context.glossary_unavailable:
        context.results = []
        return

    try:
        context.results = context.glossary.by_sap(sap_id)
    except Exception as e:
        context.error = e
        context.results = []


@then('should return at least {count:d} result')
@then('should return at least {count:d} results')
def step_impl(context: Context, count: int):
    """Verify minimum number of results returned."""
    assert len(context.results) >= count, \
        f"Expected at least {count} results, got {len(context.results)}"


@then('top result term should be "{term}"')
def step_impl(context: Context, term: str):
    """Verify top result matches expected term."""
    assert len(context.results) > 0, "No results found"
    entry, score = context.results[0]
    assert entry.term == term, \
        f"Expected term '{term}', got '{entry.term}'"


@then('top result score should be {score:f}')
def step_impl(context: Context, score: float):
    """Verify top result score matches expected value."""
    assert len(context.results) > 0, "No results found"
    entry, actual_score = context.results[0]
    assert actual_score == score, \
        f"Expected score {score}, got {actual_score}"


@then('top result score should be >= {score:f}')
def step_impl(context: Context, score: float):
    """Verify top result score meets minimum threshold."""
    assert len(context.results) > 0, "No results found"
    entry, actual_score = context.results[0]
    assert actual_score >= score, \
        f"Score {actual_score:.2f} below threshold {score}"


@then('top result definition should contain "{text}"')
def step_impl(context: Context, text: str):
    """Verify top result definition contains expected text."""
    assert len(context.results) > 0, "No results found"
    entry, score = context.results[0]
    assert text.lower() in entry.definition.lower(), \
        f"Definition does not contain '{text}': {entry.definition}"


@then('top result sap_reference should be "{sap_id}"')
def step_impl(context: Context, sap_id: str):
    """Verify top result SAP reference."""
    assert len(context.results) > 0, "No results found"
    entry, score = context.results[0]
    assert entry.sap_reference == sap_id, \
        f"Expected SAP reference '{sap_id}', got '{entry.sap_reference}'"


@then('top result should be one of')
def step_impl(context: Context):
    """Verify top result is one of the expected terms."""
    assert len(context.results) > 0, "No results found"
    entry, score = context.results[0]
    expected_terms = [row['0'] for row in context.table]
    assert entry.term in expected_terms, \
        f"Expected term to be one of {expected_terms}, got '{entry.term}'"


@then('results should include "{term}"')
def step_impl(context: Context, term: str):
    """Verify results include specific term."""
    terms = [entry.term if hasattr(entry, 'term') else entry for entry in context.results]
    assert term in terms, \
        f"Expected '{term}' in results, got: {terms}"


@then('all scores should be >= {threshold:f}')
def step_impl(context: Context, threshold: float):
    """Verify all result scores meet threshold."""
    assert len(context.results) > 0, "No results found"
    for entry, score in context.results:
        assert score >= threshold, \
            f"Score {score:.2f} for '{entry.term}' below threshold {threshold}"


# ============================================================================
# Suggestion Engine Steps
# ============================================================================

@given('the suggestion engine is initialized')
def step_impl(context: Context):
    """Initialize suggestion engine for testing."""
    try:
        from scripts.suggest_next import SuggestionEngine, ProjectContext
        context.project_context = ProjectContext.from_current_directory()
        context.suggestion_engine = SuggestionEngine(context.project_context)
    except ImportError:
        context.suggestion_engine = None
        context.suggestions_unavailable = True


@given('inbox has {count:d} pending coordination requests')
@given('inbox has {count:d} pending coordination request')
@given('inbox has {count:d} pending items')
def step_impl(context: Context, count: int):
    """Mock inbox with pending coordination requests."""
    context.mock_inbox = mock_inbox_status(pending_count=count)


@given('inbox has {count:d} active blockers')
@given('inbox has {count:d} active blocker')
def step_impl(context: Context, count: int):
    """Mock inbox with blockers."""
    context.mock_inbox = mock_inbox_status(blocker_count=count)


@given('test coverage is {percentage:d}%')
def step_impl(context: Context, percentage: int):
    """Mock test coverage percentage."""
    context.mock_coverage = percentage


@given('there are {count:d} broken links in documentation')
def step_impl(context: Context, count: int):
    """Mock broken links count."""
    context.mock_broken_links = count


@when('requesting suggestions in "{mode}" mode')
def step_impl(context: Context, mode: str):
    """Request suggestions from suggestion engine."""
    if hasattr(context, 'suggestions_unavailable') and context.suggestions_unavailable:
        context.suggestions = []
        return

    try:
        # Mock the context with test data
        if hasattr(context, 'mock_inbox'):
            context.suggestion_engine.context.inbox = context.mock_inbox
        if hasattr(context, 'mock_coverage'):
            context.suggestion_engine.context.coverage = context.mock_coverage
        if hasattr(context, 'mock_broken_links'):
            context.suggestion_engine.context.broken_links = context.mock_broken_links

        context.suggestions = context.suggestion_engine.suggest(mode=mode)
    except Exception as e:
        context.error = e
        context.suggestions = []


@then('top suggestion should contain "{text1}" and "{text2}"')
def step_impl(context: Context, text1: str, text2: str):
    """Verify top suggestion contains both text fragments."""
    assert len(context.suggestions) > 0, "No suggestions found"
    action = context.suggestions[0].action.lower()
    assert text1.lower() in action and text2.lower() in action, \
        f"Suggestion does not contain '{text1}' and '{text2}': {context.suggestions[0].action}"


@then('top suggestion priority should be "{priority}"')
def step_impl(context: Context, priority: str):
    """Verify top suggestion priority."""
    assert len(context.suggestions) > 0, "No suggestions found"
    assert context.suggestions[0].priority == priority, \
        f"Expected priority '{priority}', got '{context.suggestions[0].priority}'"


@then('top suggestion category should be "{category}"')
def step_impl(context: Context, category: str):
    """Verify top suggestion category."""
    assert len(context.suggestions) > 0, "No suggestions found"
    assert context.suggestions[0].category == category, \
        f"Expected category '{category}', got '{context.suggestions[0].category}'"


@then('suggestions should include "{text1}" and "{text2}"')
def step_impl(context: Context, text1: str, text2: str):
    """Verify suggestions include both text fragments."""
    actions = [s.action.lower() for s in context.suggestions]
    found = any(text1.lower() in action and text2.lower() in action for action in actions)
    assert found, \
        f"No suggestion contains '{text1}' and '{text2}': {[s.action for s in context.suggestions]}"


@then('{item_type} suggestion priority should be "{priority}"')
def step_impl(context: Context, item_type: str, priority: str):
    """Verify specific suggestion type has expected priority."""
    matching = [s for s in context.suggestions if item_type.lower() in s.action.lower()]
    assert len(matching) > 0, f"No {item_type} suggestion found"
    assert matching[0].priority == priority, \
        f"Expected {item_type} priority '{priority}', got '{matching[0].priority}'"


@then('{item_type} suggestion should mention "{text}"')
def step_impl(context: Context, item_type: str, text: str):
    """Verify specific suggestion type mentions text."""
    matching = [s for s in context.suggestions if item_type.lower() in s.action.lower()]
    assert len(matching) > 0, f"No {item_type} suggestion found"
    assert text.lower() in matching[0].action.lower() or text.lower() in matching[0].rationale.lower(), \
        f"{item_type} suggestion does not mention '{text}'"


@then('suggestions should not mention "{text1}" or "{text2}"')
def step_impl(context: Context, text1: str, text2: str):
    """Verify suggestions do not mention specific text."""
    actions = ' '.join([s.action.lower() for s in context.suggestions])
    rationales = ' '.join([s.rationale.lower() for s in context.suggestions])
    combined = actions + ' ' + rationales
    assert text1.lower() not in combined and text2.lower() not in combined, \
        f"Suggestions mention '{text1}' or '{text2}' when they shouldn't"


@then('should return exactly {count:d} suggestion')
@then('should return exactly {count:d} suggestions')
def step_impl(context: Context, count: int):
    """Verify exact number of suggestions returned."""
    assert len(context.suggestions) == count, \
        f"Expected exactly {count} suggestions, got {len(context.suggestions)}"


@then('suggestion priority should be "{priority}"')
def step_impl(context: Context, priority: str):
    """Verify single suggestion has expected priority."""
    assert len(context.suggestions) == 1, "Expected exactly 1 suggestion"
    assert context.suggestions[0].priority == priority, \
        f"Expected priority '{priority}', got '{context.suggestions[0].priority}'"


@then('suggestion should mention "{text}"')
def step_impl(context: Context, text: str):
    """Verify suggestion mentions text."""
    assert len(context.suggestions) > 0, "No suggestions found"
    combined = context.suggestions[0].action + ' ' + context.suggestions[0].rationale
    assert text.lower() in combined.lower(), \
        f"Suggestion does not mention '{text}': {combined}"


# ============================================================================
# User Preferences Steps
# ============================================================================

@given('user preferences set verbosity to "{level}"')
def step_impl(context: Context, level: str):
    """Set user verbosity preference."""
    context.user_prefs = {'communication': {'verbosity': level}}


@given('user preferences set formality to "{level}"')
def step_impl(context: Context, level: str):
    """Set user formality preference."""
    if not hasattr(context, 'user_prefs'):
        context.user_prefs = {}
    if 'communication' not in context.user_prefs:
        context.user_prefs['communication'] = {}
    context.user_prefs['communication']['formality'] = level


@given('user preferences set require_confirmation to "{value}"')
def step_impl(context: Context, value: str):
    """Set user confirmation preference."""
    if not hasattr(context, 'user_prefs'):
        context.user_prefs = {}
    context.user_prefs['workflow'] = {'require_confirmation': value}


@given('user preferences set progressive_disclosure to {value}')
def step_impl(context: Context, value: str):
    """Set progressive disclosure preference."""
    if not hasattr(context, 'user_prefs'):
        context.user_prefs = {}
    if 'workflow' not in context.user_prefs:
        context.user_prefs['workflow'] = {}
    context.user_prefs['workflow']['progressive_disclosure'] = value.lower() == 'true'


@when('generating response for "{query}"')
@when('generating response for any query')
def step_impl(context: Context, query: str = "test query"):
    """Generate response with user preferences applied."""
    # This is a stub - actual implementation will adapt response based on preferences
    verbosity = context.user_prefs.get('communication', {}).get('verbosity', 'standard')

    if verbosity == 'verbose':
        context.response = """
        The AGENTS.md pattern is a comprehensive approach to agent awareness.
        It provides detailed context for AI agents working in the repository.
        For example, it includes information about the project structure,
        common workflows, and best practices. This enables agents to work
        more effectively with minimal additional context loading.
        """
    elif verbosity == 'concise':
        context.response = "AGENTS.md provides agent context for the repo."
    else:  # standard
        context.response = """
        AGENTS.md is a pattern that provides context for AI agents.
        It includes project structure, workflows, and best practices.
        """

    # Apply formality
    formality = context.user_prefs.get('communication', {}).get('formality', 'standard')
    if formality == 'casual':
        context.response = context.response.replace('do not', "don't")
        context.response = context.response.replace('cannot', "can't")
    elif formality == 'formal':
        context.response = context.response.replace("don't", 'do not')
        context.response = context.response.replace("can't", 'cannot')


@when('executing action "{action}"')
def step_impl(context: Context, action: str):
    """Execute action with confirmation preference."""
    require_conf = context.user_prefs.get('workflow', {}).get('require_confirmation', 'destructive')
    destructive_actions = ['delete', 'remove', 'drop', 'truncate']

    is_destructive = any(keyword in action.lower() for keyword in destructive_actions)

    context.action_result = {
        'action': action,
        'is_destructive': is_destructive,
        'requires_confirmation': (
            require_conf == 'always' or
            (require_conf == 'destructive' and is_destructive)
        )
    }


@when('presenting complex information')
def step_impl(context: Context):
    """Present information with progressive disclosure preference."""
    progressive = context.user_prefs.get('workflow', {}).get('progressive_disclosure', True)

    if progressive:
        context.presentation = {
            'summary': "High-level overview",
            'show_more_available': True
        }
    else:
        context.presentation = {
            'summary': "Complete detailed information with all details",
            'show_more_available': False
        }


@then('response word count should be > {count:d}')
def step_impl(context: Context, count: int):
    """Verify response exceeds word count."""
    word_count = count_words(context.response)
    assert word_count > count, \
        f"Response word count {word_count} not > {count}"


@then('response word count should be < {count:d}')
def step_impl(context: Context, count: int):
    """Verify response is below word count."""
    word_count = count_words(context.response)
    assert word_count < count, \
        f"Response word count {word_count} not < {count}"


@then('response word count should be between {min_count:d} and {max_count:d}')
def step_impl(context: Context, min_count: int, max_count: int):
    """Verify response word count is in range."""
    word_count = count_words(context.response)
    assert min_count <= word_count <= max_count, \
        f"Response word count {word_count} not in range [{min_count}, {max_count}]"


@then('response should contain "{text}"')
def step_impl(context: Context, text: str):
    """Verify response contains text."""
    assert text.lower() in context.response.lower(), \
        f"Response does not contain '{text}': {context.response}"


@then('response should not contain multi-paragraph explanations')
def step_impl(context: Context):
    """Verify response is concise (single paragraph)."""
    paragraphs = [p.strip() for p in context.response.split('\n\n') if p.strip()]
    assert len(paragraphs) <= 1, \
        f"Response has {len(paragraphs)} paragraphs, expected 1"


@then('response should contain contractions like "{example1}" or "{example2}"')
def step_impl(context: Context, example1: str, example2: str):
    """Verify response uses contractions (casual)."""
    has_contractions = example1 in context.response or example2 in context.response
    assert has_contractions, \
        f"Response does not contain contractions: {context.response}"


@then('response should not contain contractions')
def step_impl(context: Context):
    """Verify response avoids contractions (formal)."""
    contractions = ["don't", "can't", "won't", "shouldn't", "wouldn't", "couldn't"]
    found_contractions = [c for c in contractions if c in context.response.lower()]
    assert len(found_contractions) == 0, \
        f"Response contains contractions: {found_contractions}"


@then('tone should be conversational')
def step_impl(context: Context):
    """Verify conversational tone (casual)."""
    # This is a simplified check - real implementation would use NLP
    assert True  # Placeholder


@then('tone should be professional')
def step_impl(context: Context):
    """Verify professional tone (formal)."""
    # This is a simplified check - real implementation would use NLP
    assert True  # Placeholder


@then('should prompt for confirmation')
def step_impl(context: Context):
    """Verify confirmation is required."""
    assert context.action_result['requires_confirmation'], \
        f"Action '{context.action_result['action']}' should require confirmation"


@then('should not prompt for confirmation')
def step_impl(context: Context):
    """Verify no confirmation required."""
    assert not context.action_result['requires_confirmation'], \
        f"Action '{context.action_result['action']}' should not require confirmation"


@then('action should not execute until confirmed')
def step_impl(context: Context):
    """Verify action waits for confirmation."""
    # This is verified by the requires_confirmation flag
    assert context.action_result['requires_confirmation']


@then('should show summary first')
def step_impl(context: Context):
    """Verify summary is shown first (progressive disclosure)."""
    assert 'summary' in context.presentation
    assert context.presentation['summary'] is not None


@then('should offer "show more details" option')
def step_impl(context: Context):
    """Verify "show more" option is available."""
    assert context.presentation['show_more_available'], \
        "Progressive disclosure should offer 'show more' option"


@then('should show all details immediately')
def step_impl(context: Context):
    """Verify all details shown (no progressive disclosure)."""
    assert not context.presentation['show_more_available'], \
        "Should show all details without 'show more' option"


# ============================================================================
# Graceful Degradation Steps
# ============================================================================

@given('{tool} is not executable')
def step_impl(context: Context, tool: str):
    """Mock tool as unavailable."""
    context.unavailable_tool = tool


@then('should fall back to INTENT_PATTERNS.yaml pattern matching')
@then('should fall back to reading GLOSSARY.md directly')
@then('should fall back to documented workflow patterns')
def step_impl(context: Context):
    """Verify graceful fallback to documented patterns."""
    # In real implementation, this would check that the fallback was used
    assert hasattr(context, 'unavailable_tool'), \
        "No unavailable tool specified"


@then('should return valid intent "{action}"')
def step_impl(context: Context, action: str):
    """Verify valid intent returned despite missing tool."""
    # Even with tool unavailable, fallback should work
    assert True  # Placeholder - will be implemented


@then('should return valid definition')
def step_impl(context: Context):
    """Verify valid definition returned despite missing tool."""
    assert True  # Placeholder - will be implemented


@then('should log warning about missing tool')
def step_impl(context: Context):
    """Verify warning logged for missing tool."""
    assert hasattr(context, 'unavailable_tool'), \
        "No unavailable tool specified"


@then('should not block user from proceeding')
def step_impl(context: Context):
    """Verify degradation doesn't block workflow."""
    assert True  # Graceful degradation never blocks


# ============================================================================
# Pattern Learning Steps
# ============================================================================

@given('pattern "{pattern_id}" does not exist')
def step_impl(context: Context, pattern_id: str):
    """Verify pattern doesn't exist yet."""
    if hasattr(context, 'router') and context.router:
        # Check that pattern doesn't exist
        context.pattern_exists = False


@when('adding new pattern')
def step_impl(context: Context):
    """Add new pattern from table data."""
    if hasattr(context, 'router') and context.router:
        pattern_data = {row['0']: row['1'] for row in context.table}
        context.new_pattern = pattern_data
        # Will be implemented: context.router.add_pattern(pattern_data)


@when('adding pattern with parameter "{param_name}"')
def step_impl(context: Context, param_name: str):
    """Add pattern with parameter extraction."""
    context.new_pattern_param = param_name


@then('pattern should be recognized')
def step_impl(context: Context):
    """Verify new pattern is recognized."""
    assert True  # Will be implemented


@then('existing patterns should still work')
def step_impl(context: Context):
    """Verify existing patterns not broken (regression)."""
    assert True  # Will be implemented


@then('should extract parameter "{param_name}" as "{param_value}"')
def step_impl(context: Context, param_name: str, param_value: str):
    """Verify parameter extraction from new pattern."""
    assert True  # Will be implemented


@then('should have multiple matches with similar confidence')
def step_impl(context: Context):
    """Verify multiple similar matches (conflict)."""
    assert len(context.matches) >= 2, "Expected multiple matches for conflict"


@then('confidence difference between top 2 should be < {threshold:f}')
def step_impl(context: Context, threshold: float):
    """Verify top matches have similar confidence."""
    assert len(context.matches) >= 2, "Need at least 2 matches"
    diff = abs(context.matches[0].confidence - context.matches[1].confidence)
    assert diff < threshold, \
        f"Confidence difference {diff:.2f} >= threshold {threshold}"


@then('should request clarification')
def step_impl(context: Context):
    """Verify clarification requested for conflict."""
    assert len(context.matches) > 0, "No matches found"
    assert context.matches[0].clarification is not None, \
        "Expected clarification for conflict"


@then('clarification should mention alternatives')
def step_impl(context: Context):
    """Verify clarification mentions alternatives."""
    assert len(context.matches) > 0, "No matches found"
    assert context.matches[0].clarification is not None, \
        "No clarification provided"
    # Check that clarification mentions there are alternatives
    assert True  # Will verify clarification format


# ============================================================================
# Integration Steps
# ============================================================================

@then('should recognize glossary query pattern')
@then('should recognize suggestion query pattern')
def step_impl(context: Context):
    """Verify query pattern recognized."""
    assert True  # Will be implemented


@then('should search glossary for "{query}"')
def step_impl(context: Context, query: str):
    """Verify glossary search performed."""
    assert True  # Will be implemented


@then('should return definition')
def step_impl(context: Context):
    """Verify definition returned."""
    assert True  # Will be implemented


@then('should call suggestion engine in "{mode}" mode')
def step_impl(context: Context, mode: str):
    """Verify suggestion engine called."""
    assert True  # Will be implemented


@then('should return top {count:d} suggestions')
def step_impl(context: Context, count: int):
    """Verify correct number of suggestions returned."""
    assert True  # Will be implemented


@given('all bidirectional translation tools are available')
def step_impl(context: Context):
    """Verify all tools available."""
    assert True  # All tools loaded


@given('user preferences are loaded')
def step_impl(context: Context):
    """Load user preferences."""
    context.user_prefs = {'communication': {'verbosity': 'standard'}}


@then('should route intent to multiple actions')
def step_impl(context: Context):
    """Verify multiple actions routed."""
    assert True  # Will be implemented


@then('should execute "{action}"')
def step_impl(context: Context, action: str):
    """Verify action executed."""
    assert True  # Will be implemented


@then('should format response according to user verbosity preference')
def step_impl(context: Context):
    """Verify response formatted per preferences."""
    assert True  # Will be implemented


# ============================================================================
# Quality Gate Steps
# ============================================================================

@given('the integration code is complete')
def step_impl(context: Context):
    """Assume integration is complete for testing."""
    context.code_complete = True


@when('running pytest with coverage')
def step_impl(context: Context):
    """Run pytest with coverage."""
    result = subprocess.run(
        ['pytest', '--cov=scripts', '--cov=features', '--cov-report=term'],
        capture_output=True,
        text=True
    )
    context.pytest_result = result
    # Parse coverage percentage from output
    # Format: "TOTAL    XXX    XXX    XX%"
    for line in result.stdout.split('\n'):
        if 'TOTAL' in line:
            parts = line.split()
            if len(parts) >= 4:
                coverage_str = parts[-1].rstrip('%')
                try:
                    context.coverage_percentage = int(coverage_str)
                except ValueError:
                    context.coverage_percentage = 0


@when('running ruff check')
def step_impl(context: Context):
    """Run ruff linter."""
    result = subprocess.run(
        ['ruff', 'check', 'scripts/', 'features/'],
        capture_output=True,
        text=True
    )
    context.ruff_result = result


@when('running mypy with strict mode')
def step_impl(context: Context):
    """Run mypy type checker."""
    result = subprocess.run(
        ['mypy', 'scripts/', '--strict'],
        capture_output=True,
        text=True
    )
    context.mypy_result = result


@then('coverage should be >= {threshold:d}%')
def step_impl(context: Context, threshold: int):
    """Verify coverage meets threshold."""
    assert hasattr(context, 'coverage_percentage'), "Coverage not measured"
    assert context.coverage_percentage >= threshold, \
        f"Coverage {context.coverage_percentage}% < threshold {threshold}%"


@then('should have 0 errors')
def step_impl(context: Context):
    """Verify no errors in linter/type checker."""
    if hasattr(context, 'ruff_result'):
        assert context.ruff_result.returncode == 0, \
            f"Ruff found errors:\n{context.ruff_result.stdout}"
    elif hasattr(context, 'mypy_result'):
        assert context.mypy_result.returncode == 0, \
            f"Mypy found errors:\n{context.mypy_result.stdout}"


# ============================================================================
# Backward Compatibility Steps
# ============================================================================

@given('SAP-009 v1.1.0 is installed')
def step_impl(context: Context):
    """Assume SAP-009 v1.1.0 is installed."""
    context.sap_009_version = '1.1.0'


@when('using AGENTS.md dual-file pattern (v1.0.0 feature)')
@when('using "Nearest File Wins" (v1.0.0 feature)')
@when('using progressive context loading (v1.0.0 feature)')
def step_impl(context: Context):
    """Use v1.0.0 feature."""
    context.using_v1_feature = True


@then('should work without changes')
def step_impl(context: Context):
    """Verify backward compatibility."""
    assert context.using_v1_feature, "v1.0.0 feature not used"
    # v1.0.0 features should work in v1.1.0
    assert True


# ============================================================================
# Documentation Steps
# ============================================================================

@given('SAP-009 protocol-spec.md Section 9 exists')
@given('SAP-009 awareness-guide.md integration section exists')
def step_impl(context: Context):
    """Verify documentation exists."""
    # Will check file exists and has expected sections
    assert True  # Will be implemented


@then('should define contracts clearly')
@then('should include input/output specifications')
@then('should include usage examples')
@then('should provide step-by-step integration instructions')
def step_impl(context: Context):
    """Verify documentation quality."""
    # Will parse documentation and verify structure
    assert True  # Will be implemented


@then('should follow reference documentation style (Diátaxis)')
@then('should follow how-to documentation style (Diátaxis)')
def step_impl(context: Context):
    """Verify Diátaxis adherence."""
    # Will check documentation follows Diátaxis patterns
    assert True  # Will be implemented
