# Using Justfile for Automation

**Audience**: Developers using Just for task automation
**Related**: [SAP-008: Automation Scripts](../../skilled-awareness/automation-scripts/)

---

## Quick Start

```bash
# Install Just
brew install just  # macOS
# or
cargo install just # Rust

# List available commands
just --list

# Run common tasks
just test          # Run tests
just lint          # Run linting
just format        # Format code
just ci            # Run all CI checks
```

---

## Justfile Overview

**Justfile** (in repo root):
```makefile
# Run tests with coverage
test:
    pytest --cov=src --cov-report=term --cov-fail-under=85

# Run linting
lint:
    ruff check .
    mypy src

# Format code
format:
    ruff check --fix .
    ruff format .

# Run all CI checks
ci: lint test
    @echo "✅ All checks passed!"

# Clean build artifacts
clean:
    rm -rf build/ dist/ *.egg-info
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Install dependencies
install:
    pip install -e ".[dev]"

# Run dev server
serve:
    python -m myproject

# Build Docker image
docker-build:
    docker build -t myproject:latest .

# Run in Docker
docker-run:
    docker run -p 8000:8000 myproject:latest
```

---

## Common Recipes

### Parameterized Recipes

```makefile
# Run specific test file
test-file FILE:
    pytest {{FILE}} -v

# Usage: just test-file tests/test_api.py
```

### Default Recipe

```makefile
# Default recipe (runs with just `just`)
default:
    @just --list
```

### Recipe Dependencies

```makefile
# Deploy depends on test passing
deploy: test
    ./scripts/deploy.sh
```

---

## Advantages Over Makefiles

1. **Clearer syntax** (no tab vs. space issues)
2. **Better error messages**
3. **Cross-platform** (works same on Windows/macOS/Linux)
4. **Parameter support**
5. **Built-in command listing** (`just --list`)

---

## Related Documentation

- [SAP-008: Automation Scripts](../../skilled-awareness/automation-scripts/)
- [Just Documentation](https://github.com/casey/just)

---

**Last Updated**: 2025-10-29
