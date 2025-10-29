# Tutorial: Installing Chora Compose

**Learning Goals:**
- Install Python 3.12+ and Poetry dependency manager
- Install Chora Compose and verify it works
- Run your first content generation example
- Troubleshoot common installation issues

**Prerequisites:**
- Basic command line familiarity
- 15-20 minutes of time

**Difficulty:** Beginner

---

## What You'll Install

**Chora Compose** is a configuration-driven framework for generating content and artifacts through Human-AI collaboration. You'll install:

- **Python 3.12+** - The runtime environment
- **Poetry** - Dependency management tool
- **Chora Compose v1.2.0** - The framework and all its dependencies
  - 13 MCP tools for content generation and storage management
  - 5 MCP resources for capability discovery
  - Conversational workflow authoring support
  - Ephemeral storage for drafts and experiments

---

## Step 1: Install Python 3.12+

Chora Compose requires Python 3.12 or higher for modern type hints and performance features.

### Check Existing Python Installation

Open your terminal:

```bash
python3 --version
```

**If you see `Python 3.12.x` or higher**, skip to Step 2.

**If you see a lower version or an error**, continue with installation below.

### Install Python 3.12+

#### macOS

**Recommended: Use Homebrew**

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12
brew install python@3.12

# Verify
python3.12 --version
```

**Alternative: Download from python.org**
- Visit [python.org/downloads](https://www.python.org/downloads/)
- Download the macOS installer
- Run and follow installation prompts

#### Linux (Ubuntu/Debian)

```bash
# Add deadsnakes PPA for latest Python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.12 and development tools
sudo apt install python3.12 python3.12-venv python3.12-dev

# Verify
python3.12 --version
```

#### Windows

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download the Windows installer (3.12 or higher)
3. **Important:** Check "Add Python to PATH" during installation
4. Complete installation and verify:

```powershell
python --version
```

---

## Step 2: Install Poetry

Poetry manages dependencies and virtual environments for Chora Compose.

### Install Poetry

**All platforms:**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Verify Installation

```bash
poetry --version
```

**Expected:** `Poetry (version 1.8.0 or higher)`

### Configure PATH (If Needed)

If `poetry` command isn't found:

**macOS/Linux:**
```bash
export PATH="$HOME/.local/bin:$PATH"

# Make permanent by adding to your shell profile
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc  # or ~/.bashrc
```

**Windows:**
- Poetry installer should add to PATH automatically
- If not working, add `%APPDATA%\Python\Scripts` to your system PATH

---

## Step 3: Get Chora Compose

### Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/liminalcommons/chora-compose.git

# Navigate into project directory
cd chora-compose
```

**Don't have git?**
- **macOS:** `brew install git`
- **Linux:** `sudo apt install git`
- **Windows:** Download from [git-scm.com](https://git-scm.com/downloads)

**Alternative:** Download ZIP from GitHub and extract.

---

## Step 4: Install Dependencies

Inside the `chora-compose` directory:

```bash
poetry install
```

**What happens:**
1. Poetry creates an isolated virtual environment
2. Installs core dependencies (Pydantic, Jinja2, jsonschema)
3. Installs development tools (pytest, ruff, mypy)
4. Links the `chora_compose` module for development

**Expected output:**
```
Creating virtualenv chora-compose in ...
Installing dependencies from lock file

Package operations: 15 installs, 0 updates, 0 removals

  • Installing pydantic (2.x.x)
  • Installing jinja2 (3.x.x)
  • Installing jsonschema (4.x.x)
  ...

Installing the current project: chora-compose (1.2.0)
```

**Duration:** 2-3 minutes

---

## Step 5: Verify Installation

### Check Chora Compose Version

```bash
poetry run python -c "from chora_compose import __version__; print(f'Chora Compose v{__version__}')"
```

**Expected output:**
```
Chora Compose v1.2.0
```

### Verify Core Modules Load

```bash
poetry run python -c "from chora_compose.core import ConfigLoader; from chora_compose.generators import Jinja2Generator; print('✓ Core modules loaded successfully')"
```

**Expected:**
```
✓ Core modules loaded successfully
```

---

## Step 6: Run Your First Example

Let's generate API documentation from an OpenAPI specification using the included example.

### Navigate to Example

```bash
cd examples/jinja2-api-docs
```

### Run Generation

```bash
poetry run python generate.py
```

### Expected Output

```
======================================================================
Chora Compose - Jinja2 Generator Example
Generating API Documentation from OpenAPI Specification
======================================================================

[1/4] Loading OpenAPI spec: data/openapi-petstore.json
      ✓ Loaded spec for Petstore API v1.0.0

[2/4] Loading content configuration: configs/content/api-docs-content.json
      ✓ Config loaded: petstore-api-docs

[3/4] Generating documentation with Jinja2Generator
      ✓ Generated 4,963 characters

[4/4] Writing output: output/API_REFERENCE.md
      ✓ Documentation written successfully

======================================================================
Generation Complete! ✓
======================================================================
```

### View Generated Documentation

```bash
# macOS/Linux
cat output/API_REFERENCE.md | head -50

# Windows
type output\API_REFERENCE.md | more
```

**You should see** a well-formatted API reference document with endpoints, parameters, and schemas!

---

## Troubleshooting Common Issues

### Poetry Command Not Found

**Symptom:** `poetry: command not found` or `command not recognized`

**Solution:**
1. Verify Poetry installation: Re-run the install script
2. Add Poetry to PATH (see Step 2)
3. Restart your terminal/shell
4. Try: `$HOME/.local/bin/poetry --version` (use full path)

### Wrong Python Version

**Symptom:** `Python version 3.11.x does not satisfy requirement >=3.12`

**Solution:**
- Install Python 3.12 following Step 1
- Verify with: `python3.12 --version`
- Recreate virtual environment: `poetry env remove python && poetry install`

### SSL/Certificate Errors During Install

**Symptom:** `SSL: CERTIFICATE_VERIFY_FAILED` or similar during `poetry install`

**Solution:**
```bash
# Update Poetry itself
poetry self update

# Clear cache
poetry cache clear pypi --all

# Retry
poetry install
```

### Module Import Errors

**Symptom:** `ModuleNotFoundError: No module named 'chora_compose'`

**Solution:**
- Always use `poetry run` prefix:
  ```bash
  # Wrong
  python script.py

  # Correct
  poetry run python script.py
  ```
- Alternative: Enter Poetry shell
  ```bash
  poetry shell
  python script.py  # Now works without prefix
  exit              # Leave shell when done
  ```

### Permission Errors (macOS/Linux)

**Symptom:** Permission denied errors during installation

**Solution:**
**Never use `sudo` with Poetry!** Fix ownership instead:
```bash
sudo chown -R $USER:$USER ~/.cache/pypoetry
sudo chown -R $USER:$USER ~/.local/share/pypoetry
```

Then retry: `poetry install`

### Example Fails to Run

**Symptom:** Example script produces errors or unexpected output

**Solution:**
1. Ensure you're in the correct directory: `cd examples/jinja2-api-docs`
2. Verify dependencies: `poetry install` from project root
3. Check Python version: `python3 --version` (must be 3.12+)
4. Run with verbose errors: `poetry run python generate.py --verbose` (if supported)

---

## Optional: Install Pre-Commit Hooks

If you plan to explore or modify Chora Compose, install pre-commit hooks for code quality:

```bash
# Return to project root
cd ../..  # or cd /path/to/chora-compose

# Install hooks
poetry run pre-commit install
```

**Expected:**
```
pre-commit installed at .git/hooks/pre-commit
```

**What this does:** Automatically runs quality checks before each git commit:
- Code formatting (ruff)
- Type checking (mypy)
- Linting
- Trailing whitespace removal

---

## Verify Complete Installation

Run this comprehensive verification:

```bash
# Run test suite
poetry run pytest

# Check test coverage
poetry run pytest --cov=chora_compose

# Verify type checking
poetry run mypy src/

# Run linter
poetry run ruff check .
```

**All checks should pass** ✓

If tests fail, verify:
- Python 3.12+ is active
- All dependencies installed
- No conflicting global packages

---

## Installation Checklist

Mark each as you complete it:

- [ ] Python 3.12+ installed (`python3 --version`)
- [ ] Poetry installed and in PATH (`poetry --version`)
- [ ] Chora Compose repository cloned
- [ ] Dependencies installed (`poetry install` completed)
- [ ] Version check passed (Chora Compose v1.2.0+)
- [ ] Example ran successfully
- [ ] Generated output looks correct
- [ ] (Optional) Pre-commit hooks installed
- [ ] (Optional) Test suite passes

**All checked?** 🎉 You're ready to use Chora Compose!

---

## Next Steps

Now that Chora Compose is installed:

### 1. Learn the Fundamentals

Start with these tutorials in order:
- **[Your First Config](02-your-first-config.md)** - Create a content configuration
- **[Generate Your First Content](03-generate-your-first-content.md)** - Generate content from config
- **[Compose Your First Artifact](04-compose-your-first-artifact.md)** - Assemble a final artifact

**Want to try conversational workflows? (v1.1.0)**
- **[Conversational Config Creation](../intermediate/02-conversational-config-creation.md)** - Create configs through natural conversation with Claude

### 2. Explore More Examples

Browse `examples/` directory:
- Jinja2 template-based generation
- Demonstration generator examples
- Multi-artifact compositions

### 3. Read the Documentation

- **[How-To Guides](../../how-to/)** - Task-oriented recipes
- **[API Reference](../../reference/)** - Complete API documentation
- **[MCP Server](../../mcp/)** - Integrate with Claude Desktop

---

## Getting Help

### Documentation
- Browse all [tutorials](../)
- Check [troubleshooting guides](../../how-to/troubleshooting/)
- Review [API reference](../../reference/)

### Community Support
- **Search issues:** [github.com/liminalcommons/chora-compose/issues](https://github.com/liminalcommons/chora-compose/issues)
- **Report a bug:** Open a new issue with:
  - Your OS and Python version
  - Complete error message
  - Steps to reproduce
  - What you expected vs. what happened

---

**Tutorial Complete!** ✅

**Time invested:** 15-20 minutes

**You learned:**
- ✅ Install Python 3.12+ and Poetry
- ✅ Install Chora Compose
- ✅ Verify installation works
- ✅ Run first generation example
- ✅ Troubleshoot common problems

**Next tutorial:** [Your First Config →](02-your-first-config.md)
