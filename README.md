# Grompt - Git for Prompts

**Version, test, and manage LLM prompts separately from code.**

Grompt lets you store prompts as YAML files, version them with git, test them with real data, and use them in your code by ID. Change prompts without deploying code.

---

## Quick Start

```bash
# Install
pip install -e .

# Initialize
grompt init

# Create a prompt
grompt add code-review --template "Review this code:\n{{ code }}"

# Test it with data
grompt test code-review --var code="def hello(): pass"

# Use in Python
from grompt import Prompt, TemplateRenderer
from grompt.infrastructure.storage.yaml_loader import YAMLLoader

loader = YAMLLoader()
prompt = loader.load_prompt("code-review")
rendered = TemplateRenderer.render(prompt.template, code="def add(a,b): return a+b")
print(rendered)
```

---

## Why Grompt?

**Problem:** Prompts buried in code are hard to version, test, and optimize.

```python
# ❌ Hard to change, test, or version
def analyze(code):
    prompt = f"Review this code:\n{code}\n\nProvide feedback on quality and bugs."
    return llm.complete(prompt)
```

**Solution:** Prompts as files, referenced by ID.

```yaml
# ✅ prompts/code-review.yaml
id: code-review
version: 2
model: gpt-4
template: |
  Review this code:
  {{ code }}
  
  Provide feedback on quality and bugs.
```

```python
# ✅ Code references prompt by ID
from grompt import Prompt

def analyze(code):
    prompt = Prompt.load("code-review")
    return prompt.render(code=code)
```

**Benefits:**
- ✅ Change prompts without touching code
- ✅ Version prompts with git
- ✅ Test prompts with real data
- ✅ Track which version is in production

---

## Defining Prompts

### Basic Prompt

```yaml
# prompts/summarize.yaml
id: summarize
version: 1
model: gpt-3.5-turbo
template: |
  Summarize this text in 3 sentences:
  
  {{ text }}
```

### Prompt with Variables

Variables use Jinja2 syntax: `{{ variable_name }}`

```yaml
# prompts/translate.yaml
id: translate
version: 1
model: gpt-3.5-turbo

# Document expected variables
variables:
  target_language:
    type: string
    required: true
    description: Language to translate to
  
  text:
    type: string
    required: true
    description: Text to translate

template: |
  Translate this text to {{ target_language }}:
  
  {{ text }}
```

### Prompt with System Message

```yaml
# prompts/chatbot.yaml
id: chatbot
version: 1
model: gpt-4

system: |
  You are a helpful assistant that answers questions concisely.
  Always be polite and professional.

template: |
  {{ user_message }}
```

### Prompt with Multiple Variables

```yaml
# prompts/code-review.yaml
id: code-review
version: 2
model: gpt-4
description: Reviews code for quality, bugs, and performance

variables:
  code:
    type: string
    required: true
    description: Code to review
  
  language:
    type: string
    required: false
    default: "Python"
    description: Programming language
  
  focus_areas:
    type: list
    required: false
    default: ["quality", "bugs", "performance"]
    description: Areas to focus on

template: |
  You are reviewing {{ language }} code.
  
  Code:
  ```{{ language.lower() }}
  {{ code }}
  ```
  
  Focus on:
  {% for area in focus_areas %}
  - {{ area }}
  {% endfor %}
  
  Provide detailed feedback.
```

### Advanced Jinja2 Features

```yaml
# prompts/advanced.yaml
id: advanced
version: 1
model: gpt-4

template: |
  # Conditionals
  {% if user_type == "admin" %}
  You have admin privileges.
  {% else %}
  You have standard privileges.
  {% endif %}
  
  # Loops
  {% for item in items %}
  - {{ item.name }}: {{ item.value }}
  {% endfor %}
  
  # Filters
  {{ text | upper }}
  {{ number | round(2) }}
  
  # Default values
  {{ optional_var | default("fallback value") }}
```

---

## Using Prompts with Variables

### CLI Testing

```bash
# Single variable
grompt test summarize --var text="Long article here..."

# Multiple variables
grompt test translate \
  --var target_language="Spanish" \
  --var text="Hello, world!"

# Variables from file
grompt test code-review --var code="$(cat myfile.py)"

# Complex variables (JSON)
grompt test advanced --var items='[{"name":"x","value":1}]'
```

### Python API

```python
from grompt import TemplateRenderer
from grompt.infrastructure.storage.yaml_loader import YAMLLoader

# Load prompt
loader = YAMLLoader()
prompt = loader.load_prompt("code-review")

# Simple rendering
rendered = TemplateRenderer.render(
    prompt.template,
    code="def add(a, b): return a + b"
)

# Multiple variables
rendered = TemplateRenderer.render(
    prompt.template,
    code="def add(a, b): return a + b",
    language="Python",
    focus_areas=["quality", "type hints"]
)

# With system message
if prompt.system:
    system_msg = prompt.system
    user_msg = rendered
    # Use both with your LLM API
```

### Using with LLM APIs

```python
from grompt.infrastructure.storage.yaml_loader import YAMLLoader
from grompt import TemplateRenderer
import openai

# Load and render
loader = YAMLLoader()
prompt = loader.load_prompt("code-review")
message = TemplateRenderer.render(
    prompt.template,
    code=my_code,
    language="Python"
)

# Use with OpenAI
response = openai.ChatCompletion.create(
    model=prompt.model,
    messages=[
        {"role": "system", "content": prompt.system} if prompt.system else None,
        {"role": "user", "content": message}
    ]
)
```

---

## Testing Prompts with Data

### Inline Test Cases

Define test cases directly in your prompt file:

```yaml
# prompts/code-review.yaml
id: code-review
version: 1
model: gpt-4
template: |
  Review this code:
  {{ code }}

# Test cases with real data
test_cases:
  - name: "simple_function"
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "mentions code quality"
      - "identifies simple function"
      - "no critical issues"
  
  - name: "division_bug"
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
      - "suggests error handling"
  
  - name: "complex_class"
    input:
      code: |
        class Calculator:
            def __init__(self):
                self.history = []
            
            def add(self, a, b):
                result = a + b
                self.history.append(result)
                return result
    expected_meaning:
      - "mentions class structure"
      - "notes history tracking"
```

### Separate Test Files

For larger test suites, use separate files:

```yaml
# tests/code-review-tests.yaml
prompt: code-review

test_cases:
  - name: "sql_injection"
    input:
      code: "query = f'SELECT * FROM users WHERE id={user_id}'"
    expected_meaning:
      - "identifies SQL injection risk"
      - "suggests parameterized queries"
  
  - name: "performance_issue"
    input:
      code: |
        for i in range(len(items)):
            print(items[i])
    expected_meaning:
      - "suggests enumerate or direct iteration"
      - "mentions performance"
```

### Running Tests

```bash
# Run tests defined in prompt file
grompt test code-review

# Run tests from separate file
grompt test code-review --test-file tests/code-review-tests.yaml

# Run specific test case
grompt test code-review --case simple_function

# Show detailed output
grompt test code-review --verbose
```

### Test with Multiple Models

```yaml
# prompts/code-review.yaml
test_cases:
  - name: "cross_model_test"
    models: ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]
    input:
      code: "def calc(x,y): return x/y"
    expected_meaning:
      - "warns about division by zero"
```

```bash
# Test against specific models
grompt test code-review --models gpt-4,claude-3-opus

# Test against all configured models
grompt test code-review --models @all
```

### Weighted Test Cases

Prioritize important tests:

```yaml
test_cases:
  - name: "critical_security"
    weight: 3.0  # 3x more important
    input:
      code: "eval(user_input)"
    expected_meaning:
      - "warns about code injection"
  
  - name: "style_issue"
    weight: 1.0  # Normal importance
    input:
      code: "def add(a,b):return a+b"
    expected_meaning:
      - "mentions spacing"
  
  - name: "minor_suggestion"
    weight: 0.5  # Less important
    input:
      code: "def add(a, b): return a + b"
    expected_meaning:
      - "suggests type hints"
```

---

## Variable Validation

### Defining Variable Schema

```yaml
# prompts/api-call.yaml
id: api-call
version: 1
model: gpt-4

variables:
  endpoint:
    type: string
    required: true
    pattern: "^/api/.*"
    description: API endpoint path
  
  method:
    type: string
    required: true
    enum: ["GET", "POST", "PUT", "DELETE"]
    description: HTTP method
  
  params:
    type: object
    required: false
    description: Query parameters
  
  max_retries:
    type: integer
    required: false
    default: 3
    min: 1
    max: 10
    description: Maximum retry attempts

template: |
  Generate a {{ method }} request to {{ endpoint }}
  {% if params %}
  with parameters: {{ params }}
  {% endif %}
  
  Max retries: {{ max_retries }}
```

### Validating Variables

```bash
# Validate prompt definition
grompt validate api-call

# Test with validation
grompt test api-call \
  --var endpoint="/api/users" \
  --var method="GET" \
  --var params='{"limit": 10}'
```

---

## Real-World Examples

### Example 1: Code Review with Context

```yaml
# prompts/code-review-contextual.yaml
id: code-review-contextual
version: 1
model: gpt-4

variables:
  code:
    type: string
    required: true
  file_path:
    type: string
    required: true
  language:
    type: string
    required: false
    default: "Python"
  project_context:
    type: string
    required: false
    description: "Brief description of the project"

template: |
  You are reviewing code from a {{ language }} project.
  
  {% if project_context %}
  Project context: {{ project_context }}
  {% endif %}
  
  File: {{ file_path }}
  
  Code:
  ```{{ language.lower() }}
  {{ code }}
  ```
  
  Provide a detailed review covering:
  1. Code quality and readability
  2. Potential bugs or edge cases
  3. Performance considerations
  4. Security issues
  5. Best practices for {{ language }}

test_cases:
  - name: "with_context"
    input:
      code: "def process_payment(amount): return amount * 1.1"
      file_path: "src/payments/processor.py"
      language: "Python"
      project_context: "E-commerce payment processing system"
    expected_meaning:
      - "mentions payment processing"
      - "suggests validation"
      - "considers security"
```

### Example 2: Data Transformation

```yaml
# prompts/transform-data.yaml
id: transform-data
version: 1
model: gpt-4

variables:
  input_format:
    type: string
    required: true
    enum: ["JSON", "CSV", "XML"]
  output_format:
    type: string
    required: true
    enum: ["JSON", "CSV", "XML"]
  data:
    type: string
    required: true
  schema:
    type: object
    required: false

template: |
  Convert this {{ input_format }} data to {{ output_format }}:
  
  Input:
  {{ data }}
  
  {% if schema %}
  Follow this schema:
  {{ schema | tojson }}
  {% endif %}
  
  Provide only the converted output, no explanations.

test_cases:
  - name: "json_to_csv"
    input:
      input_format: "JSON"
      output_format: "CSV"
      data: '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'
    expected_meaning:
      - "contains CSV format"
      - "includes headers"
```

### Example 3: Multi-Step Prompt

```yaml
# prompts/analysis-pipeline.yaml
id: analysis-pipeline
version: 1
model: gpt-4

variables:
  text:
    type: string
    required: true
  steps:
    type: list
    required: true
    description: "Analysis steps to perform"

template: |
  Analyze the following text through multiple steps:
  
  Text:
  """
  {{ text }}
  """
  
  Perform these analysis steps in order:
  {% for step in steps %}
  {{ loop.index }}. {{ step }}
  {% endfor %}
  
  Provide results for each step clearly labeled.

test_cases:
  - name: "sentiment_and_summary"
    input:
      text: "The product is amazing! Best purchase ever. Highly recommend."
      steps:
        - "Sentiment analysis"
        - "Key points extraction"
        - "Summary in one sentence"
    expected_meaning:
      - "identifies positive sentiment"
      - "extracts key points"
      - "provides summary"
```

---

## CLI Commands

### Initialization

```bash
# Initialize grompt in current directory
grompt init

# Initialize with custom config
grompt init --prompts-dir my-prompts --model gpt-4
```

### Creating Prompts

```bash
# Create basic prompt
grompt add summarize

# Create with template
grompt add code-review --template "Review: {{ code }}"

# Create with options
grompt add translate \
  --model gpt-3.5-turbo \
  --description "Translates text between languages"

# Create in subdirectory
grompt add backend/api-prompt --dir backend
```

### Testing Prompts

```bash
# Test with single variable
grompt test summarize --var text="Long article..."

# Test with multiple variables
grompt test code-review \
  --var code="def hello(): pass" \
  --var language="Python"

# Test with file content
grompt test code-review --var code="$(cat src/main.py)"

# Run all test cases
grompt test code-review

# Run specific test case
grompt test code-review --case simple_function

# Test with different model
grompt test code-review --model gpt-3.5-turbo
```

### Validation

```bash
# Validate single prompt
grompt validate code-review

# Validate all prompts
grompt validate --all

# Check for missing variables
grompt validate code-review --check-vars
```

### Version Management

```bash
# Commit changes (increments version)
grompt commit code-review "Improved clarity"

# Show version history
grompt log code-review

# Compare versions
grompt diff code-review --from v1 --to v2
```

---

## Python API Reference

### Loading Prompts

```python
from grompt.infrastructure.storage.yaml_loader import YAMLLoader

loader = YAMLLoader()

# Load by ID
prompt = loader.load_prompt("code-review")

# Access properties
print(prompt.id)          # "code-review"
print(prompt.version)     # 2
print(prompt.model)       # "gpt-4"
print(prompt.template)    # Template string
print(prompt.variables)   # Variable definitions
```

### Rendering Templates

```python
from grompt import TemplateRenderer

# Simple rendering
rendered = TemplateRenderer.render(
    "Hello {{ name }}!",
    name="World"
)

# With prompt
rendered = TemplateRenderer.render(
    prompt.template,
    code="def add(a, b): return a + b",
    language="Python"
)

# Validate template
is_valid = TemplateRenderer.validate(prompt.template)
```

### Working with Variables

```python
# Get required variables
required_vars = [
    name for name, spec in prompt.variables.items()
    if spec.get('required', False)
]

# Get variable with default
def get_var_value(var_name, user_input):
    spec = prompt.variables.get(var_name, {})
    return user_input.get(var_name, spec.get('default'))

# Validate variable types
def validate_vars(user_input):
    for name, spec in prompt.variables.items():
        if spec.get('required') and name not in user_input:
            raise ValueError(f"Missing required variable: {name}")
```

---

## Configuration

### Global Config (.grompt)

```yaml
version: 1
prompts_dir: prompts
tests_dir: tests
default_model: gpt-4

# Model configurations
models:
  gpt-4:
    provider: openai
    api_key_env: OPENAI_API_KEY
    max_tokens: 8192
  
  gpt-3.5-turbo:
    provider: openai
    api_key_env: OPENAI_API_KEY
    max_tokens: 4096
  
  claude-3-opus:
    provider: anthropic
    api_key_env: ANTHROPIC_API_KEY
    max_tokens: 200000

# Model groups
model_groups:
  openai: ["gpt-4", "gpt-3.5-turbo"]
  anthropic: ["claude-3-opus", "claude-3-sonnet"]
  all: ["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]
```

---

## Best Practices

### 1. Document Variables

Always document expected variables:

```yaml
variables:
  code:
    type: string
    required: true
    description: "Code to review"
  language:
    type: string
    required: false
    default: "Python"
    description: "Programming language of the code"
```

### 2. Provide Test Cases

Include test cases with realistic data:

```yaml
test_cases:
  - name: "realistic_example"
    input:
      code: |
        # Real code example
        def process_payment(amount, currency="USD"):
            if amount <= 0:
                raise ValueError("Amount must be positive")
            return {"amount": amount, "currency": currency}
    expected_meaning:
      - "validates input"
      - "handles currency"
```

### 3. Use Defaults Wisely

Provide sensible defaults for optional variables:

```yaml
variables:
  max_length:
    type: integer
    required: false
    default: 100
    description: "Maximum response length"
```

### 4. Version Incrementally

Commit changes with clear messages:

```bash
grompt commit code-review "Added language parameter for multi-language support"
```

### 5. Test Before Deploying

Always test prompts with real data before using in production:

```bash
grompt test code-review --var code="$(cat production_example.py)"
```

---

## Directory Structure

```
your-project/
├── .grompt                    # Configuration
├── prompts/                   # Your prompts
│   ├── code-review.yaml
│   ├── summarize.yaml
│   └── translate.yaml
├── tests/                     # Test files
│   ├── code-review-tests.yaml
│   └── common/
│       └── edge-cases.yaml
└── your_code.py              # Your application
```

---

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black grompt/

# Type check
mypy grompt/
```

---

## License

MIT