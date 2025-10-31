# Cross-Session Memory Guide

**Audience**: Developers using chora-base memory patterns
**Related**: [SAP-010: Memory System](../../skilled-awareness/memory-system/)

---

## Overview

Cross-session memory allows your application to persist and retrieve information across multiple user sessions, enabling:
- User preferences and settings
- Conversation context and history
- Learning from past interactions
- Personalization patterns

---

## Quick Start

```python
from myproject.memory import MemoryManager

# Initialize memory manager
memory = MemoryManager()

# Store information
memory.store("user_123", "preference", {"theme": "dark", "language": "en"})

# Retrieve information
preferences = memory.retrieve("user_123", "preference")
# Returns: {"theme": "dark", "language": "en"}

# Update information
memory.update("user_123", "preference", {"theme": "light"})

# Delete information
memory.delete("user_123", "preference")
```

---

## Memory Patterns

### 1. User Preferences

```python
class UserPreferences:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def get_preference(self, user_id: str, key: str) -> Any:
        """Get user preference with fallback to default."""
        prefs = self.memory.retrieve(user_id, "preferences") or {}
        return prefs.get(key, self._defaults.get(key))

    def set_preference(self, user_id: str, key: str, value: Any):
        """Set user preference."""
        prefs = self.memory.retrieve(user_id, "preferences") or {}
        prefs[key] = value
        self.memory.store(user_id, "preferences", prefs)
```

### 2. Conversation History

```python
class ConversationMemory:
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to conversation history."""
        history = self.memory.retrieve(session_id, "history") or []
        history.append({"role": role, "content": content, "timestamp": datetime.now()})
        self.memory.store(session_id, "history", history)

    def get_context(self, session_id: str, last_n: int = 10) -> List[dict]:
        """Get recent conversation context."""
        history = self.memory.retrieve(session_id, "history") or []
        return history[-last_n:]
```

### 3. Learning Patterns

```python
class LearningMemory:
    def record_interaction(self, user_id: str, action: str, result: dict):
        """Record user interaction for learning."""
        interactions = self.memory.retrieve(user_id, "interactions") or []
        interactions.append({
            "action": action,
            "result": result,
            "timestamp": datetime.now()
        })
        self.memory.store(user_id, "interactions", interactions)

    def get_patterns(self, user_id: str) -> dict:
        """Analyze interaction patterns."""
        interactions = self.memory.retrieve(user_id, "interactions") or []
        # Analyze patterns...
        return {
            "common_actions": self._find_common(interactions),
            "success_rate": self._calculate_success(interactions)
        }
```

---

## Storage Backends

### In-Memory (Development)

```python
class InMemoryStorage:
    def __init__(self):
        self._data = {}

    def store(self, key: str, value: Any):
        self._data[key] = value

    def retrieve(self, key: str) -> Any:
        return self._data.get(key)
```

### File-Based (Simple Persistence)

```python
import json
from pathlib import Path

class FileStorage:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)

    def store(self, key: str, value: Any):
        file_path = self.data_dir / f"{key}.json"
        with open(file_path, 'w') as f:
            json.dump(value, f)

    def retrieve(self, key: str) -> Any:
        file_path = self.data_dir / f"{key}.json"
        if not file_path.exists():
            return None
        with open(file_path) as f:
            return json.load(f)
```

### Database (Production)

```python
from sqlalchemy import Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Memory(Base):
    __tablename__ = "memory"

    key = Column(String, primary_key=True)
    value = Column(JSON)

class DatabaseStorage:
    def __init__(self, session):
        self.session = session

    def store(self, key: str, value: Any):
        memory = self.session.query(Memory).filter_by(key=key).first()
        if memory:
            memory.value = value
        else:
            memory = Memory(key=key, value=value)
            self.session.add(memory)
        self.session.commit()

    def retrieve(self, key: str) -> Any:
        memory = self.session.query(Memory).filter_by(key=key).first()
        return memory.value if memory else None
```

---

## Best Practices

1. **Namespace keys** to avoid collisions:
```python
# Good
memory.store(f"user:{user_id}:preferences", prefs)
memory.store(f"session:{session_id}:history", history)

# Bad
memory.store("preferences", prefs)  # Which user?
```

2. **Set expiration** for temporary data:
```python
memory.store(key, value, ttl=3600)  # Expire after 1 hour
```

3. **Handle missing data gracefully**:
```python
preferences = memory.retrieve(key) or DEFAULT_PREFERENCES
```

4. **Implement cleanup**:
```python
def cleanup_old_sessions():
    """Remove sessions older than 30 days."""
    cutoff = datetime.now() - timedelta(days=30)
    old_sessions = memory.query_by_timestamp(before=cutoff)
    for session_id in old_sessions:
        memory.delete(f"session:{session_id}:*")
```

---

## Testing

```python
def test_memory_store_retrieve():
    """Test basic store and retrieve."""
    memory = MemoryManager(storage=InMemoryStorage())

    memory.store("test_key", {"value": 123})
    result = memory.retrieve("test_key")

    assert result == {"value": 123}

def test_memory_expiration():
    """Test TTL expiration."""
    memory = MemoryManager(storage=InMemoryStorage())

    memory.store("temp_key", "value", ttl=1)
    time.sleep(2)
    result = memory.retrieve("temp_key")

    assert result is None  # Expired
```

---

## Related Documentation

- [SAP-010: Memory System](../../skilled-awareness/memory-system/)
- [SAP-004: Testing Framework](../../skilled-awareness/testing-framework/)

---

**Last Updated**: 2025-10-29
