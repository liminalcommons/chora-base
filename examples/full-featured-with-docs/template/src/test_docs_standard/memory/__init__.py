"""Agent memory system for cross-session learning and knowledge persistence.

This module provides stateful memory infrastructure for AI coding agents,
implementing the A-MEM (Agentic Memory) principles from agentic coding best practices.
"""

from test_docs_standard.memory.event_log import EventLog, query_events
from test_docs_standard.memory.knowledge_graph import KnowledgeGraph
from test_docs_standard.memory.profiles import AgentProfile, AgentProfileManager
from test_docs_standard.memory.trace import TraceContext, emit_event, get_trace_id

__all__ = [
    "EventLog",
    "query_events",
    "KnowledgeGraph",
    "TraceContext",
    "get_trace_id",
    "emit_event",
    "AgentProfile",
    "AgentProfileManager",
]
