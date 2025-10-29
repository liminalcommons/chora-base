# How to Use the AI Code Generation Generator

> **Goal:** Generate code using Anthropic Claude AI from natural language specifications.

⚠️ **REQUIRES:**
- Anthropic API Key ([Get one here](https://console.anthropic.com/settings/keys))
- `anthropic` Python package
- Budget for API costs ($0.01-0.10 per generation)

## When to Use This

You need the CodeGenerationGenerator when:
- You want to generate code from natural language descriptions
- You need boilerplate or utility functions quickly
- You're prototyping and need scaffolding
- You want AI to handle edge cases intelligently
- You're willing to pay for quality code generation

**Don't use this if:**
- Cost is a concern (frequent generation) → Use [template_fill](use-template-fill-generator.md) with code templates
- Need instant results (this takes 10-30s) → Use [jinja2](../generation/debug-jinja2-templates.md)
- Generating non-code content → Use [template_fill](use-template-fill-generator.md) or [jinja2](../generation/debug-jinja2-templates.md)
- Security-critical code without review → **Always review AI-generated code**
- No internet available → Use template-based generators

## Prerequisites

- Chora Compose installed with `anthropic` package
- Anthropic API key
- Understanding of API concepts
- Budget for API costs (~$0.02-0.05 per generation)
- Code review process in place

---

## Setup

### 1. Install Dependencies

```bash
# If not already installed
poetry add anthropic

# Or with pip
pip install anthropic
```

### 2. Get API Key

1. Sign up at [https://console.anthropic.com](https://console.anthropic.com)
2. Navigate to **Settings → API Keys**
3. Click **Create Key**
4. Copy the key immediately (you won't see it again!)
5. Set spending limits (recommended: $10/month for testing)

### 3. Secure Your API Key

⚠️ **CRITICAL SECURITY:**

**Use environment variables:**
```bash
# Option 1: Export in shell
export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Option 2: Add to .env file (gitignored!)
echo "ANTHROPIC_API_KEY=sk-ant-api03-your-key-here" > .env

# Option 3: System keychain (most secure)
# Use your OS keychain manager
```

**Never:**
- ❌ Commit API keys to git
- ❌ Share keys in chat/email
- ❌ Hardcode in source files
- ❌ Use production keys for development

**Always:**
- ✅ Use environment variables
- ✅ Add `.env` to `.gitignore`
- ✅ Rotate keys regularly
- ✅ Set spending limits
- ✅ Monitor usage

---

## Solution

### Quick Version

```python
import os
from chora_compose.core.config_loader import ConfigLoader
from chora_compose.generators.code_generation import CodeGenerationGenerator

# Load config
loader = ConfigLoader()
config = loader.load_content_config("your-function-generator")

# Context with specifications
context = {
    "function_name": "validate_email",
    "description": "Validate email addresses using regex. Handle edge cases."
}

# Generate (requires API key in environment)
generator = CodeGenerationGenerator(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    enable_cost_tracking=True
)

output = generator.generate(config, context=context)
print(output)

# Check cost
if generator._last_cost:
    print(f"Cost: ${generator._last_cost:.4f}")
```

### Detailed Steps

#### 1. Create Content Configuration

```json
{
  "type": "content",
  "id": "function-generator",
  "schemaRef": {
    "id": "content-schema",
    "version": "3.1"
  },
  "metadata": {
    "description": "AI-powered function generation",
    "version": "1.0.0",
    "generation_frequency": "on_demand",
    "output_format": "python"
  },
  "elements": [
    {
      "name": "code",
      "description": "Generated code",
      "format": "code",
      "example_output": ""
    }
  ],
  "generation": {
    "patterns": [
      {
        "id": "code-gen",
        "type": "code_generation",
        "generation_config": {
          "model": "claude-3-5-sonnet-20241022",
          "temperature": 0.0,
          "max_tokens": 2048,
          "prompt": "Generate a {{language}} function to {{description}}",
          "language": "python",
          "system_prompt": "You are an expert programmer. Generate clean, documented code."
        }
      }
    ]
  }
}
```

#### 2. Prepare Function Specifications

```python
context = {
    "language": "python",
    "description": "validate email addresses with proper regex and edge case handling",
    "style_hints": [
        "Use type hints",
        "Include docstrings",
        "Follow PEP 8",
        "Add input validation"
    ]
}
```

#### 3. Generate Code

```python
from chora_compose.generators.code_generation import CodeGenerationGenerator
import os

# Initialize with API key
generator = CodeGenerationGenerator(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    default_model="claude-3-5-sonnet-20241022",
    default_temperature=0.0,  # Deterministic
    default_max_tokens=2048,
    enable_cost_tracking=True
)

# Generate
try:
    result = generator.generate(config, context=context)
    print("Generated code:")
    print(result)

    # Cost tracking
    if generator._last_usage:
        usage = generator._last_usage
        cost = generator._last_cost
        print(f"\nTokens: {usage['input_tokens']} in, {usage['output_tokens']} out")
        print(f"Cost: ${cost:.4f}")

except Exception as e:
    print(f"Generation failed: {e}")
```

#### 4. Review and Test Generated Code

**Always:**
1. ✅ Read the generated code carefully
2. ✅ Test with various inputs
3. ✅ Check edge cases
4. ✅ Verify security implications
5. ✅ Add additional tests
6. ✅ Refactor if needed

---

## Configuration Options

### Model Selection

| Model | Speed | Quality | Cost/M tokens | Best For |
|-------|-------|---------|---------------|----------|
| claude-3-5-sonnet-20241022 | Medium | Best | $3/$15 | Production code |
| claude-3-opus-20240229 | Slow | Excellent | $15/$75 | Complex algorithms |
| claude-3-haiku-20240307 | Fast | Good | $0.25/$1.25 | Simple utilities |

**Example:**
```python
generator = CodeGenerationGenerator(
    default_model="claude-3-haiku-20240307"  # Cheaper for testing
)
```

### Temperature (Creativity)

| Value | Behavior | Use Case |
|-------|----------|----------|
| 0.0 | Deterministic | Production code (recommended) |
| 0.3 | Slight variation | Boilerplate with options |
| 0.7 | Creative | Prototyping, exploration |
| 1.0 | Maximum creativity | Experimental, alternative approaches |

**Recommendation:** Always use 0.0 for code generation to ensure consistency.

```json
{
  "temperature": 0.0  // Deterministic, repeatable
}
```

### Max Tokens (Length)

| Tokens | ~Lines of Code | Cost (Sonnet output) |
|--------|----------------|---------------------|
| 512 | ~130 lines | ~$0.008 |
| 1024 | ~250 lines | ~$0.015 |
| 2048 | ~500 lines | ~$0.031 |
| 4096 | ~1000 lines | ~$0.061 |

**Formula:** 1 token ≈ 0.75 words ≈ 0.25 lines of code

```json
{
  "max_tokens": 2048  // Enough for most functions
}
```

---

## Prompt Engineering

### Effective Prompts

**Good prompts are:**
- ✅ Specific about requirements
- ✅ Include input/output examples
- ✅ Mention edge cases to handle
- ✅ Specify coding standards
- ✅ Clear about error handling

**Example of good prompt:**
```
Generate a Python function to validate email addresses.

Requirements:
- Use regex pattern matching
- Return True if valid, False otherwise
- Handle edge cases: multiple @, missing domain, invalid TLD
- Include type hints
- Add docstring with examples
- Follow PEP 8 style

Example:
  validate_email("user@example.com") -> True
  validate_email("invalid.email") -> False
```

**Example of bad prompt:**
```
Make an email validator
```

### Prompt Templates

**For utility functions:**
```
Generate a {{language}} function named {{function_name}} that {{description}}.

Requirements:
{{requirements}}

Edge cases to handle:
{{edge_cases}}

Style:
{{style_hints}}
```

**For class methods:**
```
Generate a {{language}} class method for {{class_name}} that {{description}}.

The method should:
- {{requirement_1}}
- {{requirement_2}}
- {{requirement_3}}

Return: {{return_description}}
Raises: {{exceptions}}
```

---

## Cost Management

### Pricing (as of 2025)

**Input tokens (per 1M):**
- Claude 3.5 Sonnet: $3.00
- Claude 3 Opus: $15.00
- Claude 3 Haiku: $0.25

**Output tokens (per 1M):**
- Claude 3.5 Sonnet: $15.00
- Claude 3 Opus: $75.00
- Claude 3 Haiku: $1.25

### Real-World Costs

**Typical function generation:**
- Input: 200-300 tokens (~$0.001)
- Output: 500-1000 tokens (~$0.015)
- **Total: ~$0.02 per function**

**Daily usage estimates:**
- 10 functions/day × 30 days = **$6/month**
- 100 functions/day × 30 days = **$60/month**

### Cost Optimization

**1. Use cheaper models for simple tasks:**
```python
# For simple utilities
generator = CodeGenerationGenerator(default_model="claude-3-haiku-20240307")

# For complex algorithms
generator = CodeGenerationGenerator(default_model="claude-3-opus-20240229")
```

**2. Reduce max_tokens:**
```json
{
  "max_tokens": 1024  // Instead of 4096
}
```

**3. Cache common results:**
```python
import hashlib
import json

def generate_with_cache(generator, config, context):
    # Create cache key from prompt
    cache_key = hashlib.md5(
        json.dumps(context, sort_keys=True).encode()
    ).hexdigest()

    cache_file = f"cache/{cache_key}.py"

    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return f.read()

    # Generate and cache
    result = generator.generate(config, context)
    with open(cache_file, "w") as f:
        f.write(result)

    return result
```

**4. Batch similar requests:**
```python
# Instead of 5 separate calls
prompts = [
    "validate_email",
    "validate_phone",
    "validate_url",
    "validate_ip",
    "validate_domain"
]

# Make one call with all
prompt = "Generate 5 validation functions: " + ", ".join(prompts)
```

**5. Monitor usage:**
```python
generator = CodeGenerationGenerator(enable_cost_tracking=True)

# After generation
if generator._last_cost:
    log_cost_to_monitoring(generator._last_cost)

    # Alert if over budget
    if generator._last_cost > 0.10:
        send_alert(f"High cost generation: ${generator._last_cost:.4f}")
```

### Spending Limits

Set in Anthropic console:
1. Go to **Settings → Billing**
2. Set **Monthly spending limit**
3. Enable **Usage alerts**
4. Monitor at **Usage dashboard**

---

## Quality Assurance

### Code Review Checklist

**Before using generated code:**
- [ ] Read and understand the code
- [ ] Check for security vulnerabilities
- [ ] Verify edge case handling
- [ ] Test with various inputs
- [ ] Check performance implications
- [ ] Validate error handling
- [ ] Ensure documentation is accurate
- [ ] Run linters (ruff, pylint)
- [ ] Run type checkers (mypy)
- [ ] Add additional tests

### Testing Strategy

```python
# Always add tests for generated code
import pytest
from generated_code import validate_email  # AI-generated

def test_valid_emails():
    """Test valid email addresses."""
    assert validate_email("user@example.com")
    assert validate_email("first.last@domain.co.uk")
    assert validate_email("user+tag@example.com")

def test_invalid_emails():
    """Test invalid email addresses."""
    assert not validate_email("invalid")
    assert not validate_email("@example.com")
    assert not validate_email("user@@example.com")
    assert not validate_email("")

def test_edge_cases():
    """Test edge cases."""
    assert not validate_email(None)  # May need to add this handling
    assert not validate_email(123)   # May need to add this handling
```

### Security Considerations

⚠️ **CRITICAL:**

**Never use AI-generated code for:**
- Authentication/authorization logic
- Cryptography
- Security-critical operations
- Payment processing
- Data sanitization (without review)

**Always:**
- ✅ Review for SQL injection vulnerabilities
- ✅ Check for XSS vulnerabilities
- ✅ Verify input validation
- ✅ Check for race conditions
- ✅ Validate error handling
- ✅ Run security scanners

---

## Advanced Usage

### Multi-Language Generation

```python
languages = ["python", "javascript", "typescript", "go"]

for lang in languages:
    context = {
        "language": lang,
        "function_name": "validateEmail",
        "description": "validate email addresses"
    }

    result = generator.generate(config, context)
    with open(f"validators/validate_email.{lang_ext[lang]}", "w") as f:
        f.write(result)
```

### Retry Logic

Built-in retry with exponential backoff:

```python
generator = CodeGenerationGenerator(
    api_key=api_key,
    # Retry configuration
    retry_count=3,       # Number of retries
    retry_delay=1.0,     # Initial delay (doubles each retry)
    timeout=30.0         # Request timeout
)
```

**Retry sequence:**
- Attempt 1: Immediate
- Attempt 2: Wait 1s
- Attempt 3: Wait 2s
- Attempt 4: Wait 4s

### Fallback Templates

```python
generator = CodeGenerationGenerator(
    api_key=api_key,
    fallback_template="# TODO: Implement {{function_name}}\npass"
)

# If API fails, uses fallback instead of raising error
```

### Custom System Prompts

```json
{
  "system_prompt": "You are a senior Python developer with 10+ years experience. Generate production-ready code following Google Python Style Guide. Include comprehensive error handling and type hints. Add docstrings in Google format."
}
```

---

## Error Handling

### Common Errors

**1. Missing API Key**
```
CodeGenerationError: No API key provided
```

**Solution:**
```python
import os
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("Set ANTHROPIC_API_KEY environment variable")
```

**2. Rate Limit**
```
RateLimitError: Rate limit exceeded
```

**Solution:** Automatic retry with exponential backoff (built-in)

**3. Invalid API Key**
```
AuthenticationError: Invalid API key
```

**Solution:**
- Check key hasn't been revoked
- Verify no extra spaces/characters
- Generate new key if needed

**4. Timeout**
```
TimeoutError: Request timed out
```

**Solution:**
```python
generator = CodeGenerationGenerator(
    api_key=api_key,
    timeout=60.0  # Increase timeout
)
```

**5. Cost Exceeded**
```
# Custom error from monitoring
```

**Solution:** Set spending limits in Anthropic console

### Error Recovery

```python
def generate_with_fallback(generator, config, context):
    """Generate code with fallback on error."""
    try:
        return generator.generate(config, context)
    except RateLimitError:
        print("Rate limited, waiting 60s...")
        time.sleep(60)
        return generator.generate(config, context)
    except TimeoutError:
        print("Timeout, retrying with simpler prompt...")
        context["description"] = simplify_description(context["description"])
        return generator.generate(config, context)
    except Exception as e:
        print(f"Generation failed: {e}")
        return generate_template_based_fallback(context)
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow generation | Large max_tokens | Reduce max_tokens to 1024-2048 |
| Poor code quality | Vague prompt | Add specific requirements, examples |
| Inconsistent output | High temperature | Set temperature=0.0 |
| High costs | Frequent calls | Implement caching, use Haiku model |
| Missing imports | Incomplete prompt | Specify "include all imports" |
| Wrong language | Context mismatch | Verify language in context |

---

## Example Workflows

### CI/CD Code Generation

```yaml
# .github/workflows/generate-utilities.yml
name: Generate Utility Functions

on:
  workflow_dispatch:
    inputs:
      function_spec:
        description: 'Function specification'
        required: true

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Generate code
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python scripts/generate_function.py \
            --spec "${{ github.event.inputs.function_spec }}"

      - name: Test generated code
        run: pytest tests/test_generated.py

      - name: Create PR
        if: success()
        run: |
          git checkout -b generated-code-${{ github.run_id }}
          git add .
          git commit -m "Generated code: ${{ github.event.inputs.function_spec }}"
          gh pr create --title "Generated code" --body "Auto-generated"
```

---

## Examples

**Full working example:**
- See: [examples/03-ai-code-generation/](../../examples/03-ai-code-generation/)
- Use case: Python utility functions
- Includes: Config, context, API key setup, cost tracking

**Quick links:**
- [README](../../examples/03-ai-code-generation/README.md) - Complete guide
- [Config](../../examples/03-ai-code-generation/configs/content/function-generator.json)
- [Context](../../examples/03-ai-code-generation/context.json)
- [Script](../../examples/03-ai-code-generation/generate.py)
- [Sample Output](../../examples/03-ai-code-generation/sample-output.py)

---

## Related Documentation

- [Generator Comparison Guide](comparison.md) - Choose the right generator
- [Template Fill Generator](template-fill.md) - For template-based code
- [Jinja2 Generator](../how-to/generation/debug-jinja2-templates.md) - For code templates
- [Anthropic API Docs](https://docs.anthropic.com) - Official API reference

---

## API Reference

```python
class CodeGenerationGenerator(GeneratorStrategy):
    """AI-powered code generation using Anthropic Claude."""

    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = "claude-3-5-sonnet-20241022",
        default_temperature: float = 0.0,
        default_max_tokens: int = 4096,
        enable_cost_tracking: bool = True
    ) -> None:
        """Initialize code generation generator."""

    def generate(
        self,
        config: ContentConfig,
        context: dict[str, Any] | None = None
    ) -> str:
        """Generate code from specifications."""
```

**Parameters:**
- `api_key`: Anthropic API key (or from ANTHROPIC_API_KEY env var)
- `default_model`: Claude model to use
- `default_temperature`: 0.0-1.0 (0.0 recommended for code)
- `default_max_tokens`: Maximum output length
- `enable_cost_tracking`: Track token usage and costs

**Cost Tracking:**
```python
generator._last_usage  # {"input_tokens": 250, "output_tokens": 800}
generator._last_cost   # 0.0195 (in USD)
```

---

**Last Updated:** 2025-10-12 | **Phase:** 3.2 Complete
